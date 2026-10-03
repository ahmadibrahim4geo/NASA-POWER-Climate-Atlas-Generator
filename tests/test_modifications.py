# -*- coding: utf-8 -*-
"""
Verification suite for the Climate Toolbox modifications:
1. Removal of R_Max_Daily_Month and R_Annual_Rain_Days_Total (6 core precipitation fields).
2. Wind Vector Spacing parameter and wind vector generation (Wind_Vector_*).
3. Strict boundary masking & clipping (arcpy.env.mask & extent, raster ExtractByMask, wind vector Clip).
"""

import io
import os
import sys
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYT_PATH = os.path.join(ROOT_DIR, "POWER_Climate_Atlas_Generator_10_8.pyt")

# Mock arcpy for headless unit testing
class MockFilter(object):
    def __init__(self):
        self.type = ""
        self.list = []

class MockParameter(object):
    def __init__(self, displayName="", name="", datatype="", parameterType="Optional", direction="Input"):
        self.displayName = displayName
        self.name = name
        self.datatype = datatype
        self.parameterType = parameterType
        self.direction = direction
        self._val = None
        self._val_text = None
        self.category = ""
        self.description = ""
        self.enabled = True
        self.filter = MockFilter()
        self.multiValue = False
        self.error_message = None
        self.warning_message = None

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, v):
        self._val = v
        self._val_text = str(v) if v is not None else ""

    @property
    def valueAsText(self):
        if self._val_text is not None:
            return self._val_text
        return str(self._val) if self._val is not None else ""

    @valueAsText.setter
    def valueAsText(self, v):
        self._val_text = v

    def setErrorMessage(self, msg):
        self.error_message = msg

    def setWarningMessage(self, msg):
        self.warning_message = msg


class MockArcPy(object):
    Parameter = MockParameter

    def AddFieldDelimiters(self, fc, fld):
        return fld

    def Exists(self, path):
        return True

    def ClearEnvironment(self, name):
        pass


mock_arcpy = MockArcPy()

# Load pyt module dynamically
pyt_mod = type(sys)("power_atlas_pyt")
pyt_mod.__dict__["arcpy"] = mock_arcpy
exec(compile(open(PYT_PATH, "rb").read(), PYT_PATH, "exec"), pyt_mod.__dict__)
pyt_mod.arcpy = mock_arcpy

import raster_atlas_generator as rag
rag.arcpy = mock_arcpy


class TestClimateToolboxModifications(unittest.TestCase):

    def test_01_pyt_precipitation_fields_removed(self):
        """Test R_Max_Daily_Month and R_Annual_Rain_Days_Total are removed from pyt."""
        # 1. FIELD_DEFS
        field_names = [r[0] for r in pyt_mod.FIELD_DEFS]
        self.assertNotIn("R_Max_Daily_Month", field_names)
        self.assertNotIn("R_Annual_Rain_Days_Total", field_names)

        # Precipitation fields in FIELD_DEFS must be exactly the 8 core fields
        precip_field_defs = [r[0] for r in pyt_mod.FIELD_DEFS if r[4] == "Precipitation"]
        expected_8 = [
            "R_Annual_Mean",
            "R_Month_Mean",
            "R_Annual_Range",
            "R_Seasonal_Range",
            "R_Winter_Mean",
            "R_Spring_Mean",
            "R_Summer_Mean",
            "R_Autumn_Mean"
        ]
        self.assertEqual(precip_field_defs, expected_8)

        # 2. REQUIRED_COLUMNS
        self.assertNotIn("R_Max_Daily_Month", pyt_mod.REQUIRED_COLUMNS)
        self.assertNotIn("R_Annual_Rain_Days_Total", pyt_mod.REQUIRED_COLUMNS)
        precip_req = [f for f in pyt_mod.REQUIRED_COLUMNS if f.startswith("R_") and "Trend" not in f and "Anom" not in f]
        self.assertEqual(precip_req, expected_8)

        # 3. SHP_FIELD_MAP
        self.assertNotIn("R_Max_Daily_Month", pyt_mod.SHP_FIELD_MAP)
        self.assertNotIn("R_Annual_Rain_Days_Total", pyt_mod.SHP_FIELD_MAP)
        self.assertIn("R_Seasonal_Range", pyt_mod.SHP_FIELD_MAP)

        # 4. compute_point_fields
        monthly = {
            "PRECTOTCORR": dict(((2025, m), 10.0) for m in range(1, 13)),
        }
        res = pyt_mod.compute_point_fields(
            monthly, [2025], ["Precipitation"], "Daily",
            daily_raw={"PRECTOTCORR": {(2025, 1, 1): 5.0, (2025, 1, 2): 15.0}}
        )
        self.assertNotIn("R_Max_Daily_Month", res)
        self.assertNotIn("R_Annual_Rain_Days_Total", res)
        for exp_f in expected_8:
            self.assertIn(exp_f, res)

    def test_02_raster_generator_precipitation_fields_removed(self):
        """Test R_Max_Daily_Month and R_Annual_Rain_Days_Total are removed from raster_atlas_generator."""
        # 1. MODULE_INDICATOR_FIELDS["Precipitation"]
        precip_indicators = [f[0] for f in rag.MODULE_INDICATOR_FIELDS.get("Precipitation", [])]
        expected_8 = [
            "R_Annual_Mean",
            "R_Month_Mean",
            "R_Annual_Range",
            "R_Seasonal_Range",
            "R_Winter_Mean",
            "R_Spring_Mean",
            "R_Summer_Mean",
            "R_Autumn_Mean"
        ]
        self.assertEqual(precip_indicators, expected_8)
        self.assertNotIn("R_Max_Daily_Month", precip_indicators)
        self.assertNotIn("R_Annual_Rain_Days_Total", precip_indicators)

        # 2. SHP_FIELD_MAP
        self.assertNotIn("R_Max_Daily_Month", rag.SHP_FIELD_MAP)
        self.assertNotIn("R_Annual_Rain_Days_Total", rag.SHP_FIELD_MAP)
        self.assertIn("R_Seasonal_Range", rag.SHP_FIELD_MAP)

    def test_03_pyt_wind_spacing_parameter(self):
        """Test Wind Vector Spacing parameter displayName and behavior in pyt."""
        tool = pyt_mod.PowerClimateAtlasGenerator()
        params = tool.getParameterInfo()
        pdict = dict((p.name, p) for p in params)
        self.assertIn("Wind_Factor_Cell_Size", pdict)
        p_wind = pdict["Wind_Factor_Cell_Size"]
        self.assertEqual(p_wind.displayName, "Wind Vector Spacing / Cell Size (Meters)")

        # Verify resolve_submodel_name does not hijack Wind into Wind Chill
        self.assertIsNone(pyt_mod.resolve_submodel_name("Wind"))
        self.assertIsNone(pyt_mod.resolve_submodel_name("Temperature"))
        self.assertIsNotNone(pyt_mod.resolve_submodel_name("Wind Chill"))

        # Test dynamic enable/disable in updateParameters
        pdict["Climate_Modules"].value = "Temperature;Precipitation"
        tool.updateParameters(params)
        self.assertFalse(p_wind.enabled)

        pdict["Climate_Modules"].value = "Temperature;Wind"
        tool.updateParameters(params)
        self.assertTrue(p_wind.enabled)

        pdict["Climate_Modules"].value = "Wind"
        tool.updateParameters(params)
        self.assertTrue(p_wind.enabled)

    def test_04_raster_generator_wind_spacing_parameter(self):
        """Test Wind Vector Spacing parameter in RasterDataClimateAtlasGenerator."""
        tool = rag.RasterDataClimateAtlasGenerator()
        params = tool.getParameterInfo()
        pdict = dict((p.name, p) for p in params)
        self.assertIn("Wind_Factor_Cell_Size", pdict)
        p_wind = pdict["Wind_Factor_Cell_Size"]
        self.assertEqual(p_wind.displayName, "Wind Vector Spacing / Cell Size (Meters)")
        self.assertEqual(p_wind.category, "Cartography & Spatial Interpolation")

        # Test dynamic enable/disable in updateParameters
        # When Wind is NOT selected
        pdict["Climate_Modules"].value = "Temperature;Precipitation"
        tool.updateParameters(params)
        self.assertFalse(p_wind.enabled)

        # When Wind IS selected
        pdict["Climate_Modules"].value = "Temperature;Wind"
        tool.updateParameters(params)
        self.assertTrue(p_wind.enabled)

    def test_05_raster_generator_has_build_wind_vectors(self):
        """Verify _build_wind_vectors method exists in RasterDataClimateAtlasGenerator."""
        tool = rag.RasterDataClimateAtlasGenerator()
        self.assertTrue(hasattr(tool, "_build_wind_vectors"))

    def test_06_wind_vector_standard_naming(self):
        """Verify standard naming for the 5 wind vector layers in code."""
        # Check in POWER_Climate_Atlas_Generator_10_8.pyt
        with io.open(PYT_PATH, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        self.assertIn('fc = os.path.join(gdb_path, "Wind_Vector_%s" % suffix)', content)

        # Check in raster_atlas_generator.py
        with io.open(os.path.join(ROOT_DIR, "raster_atlas_generator.py"), "r", encoding="utf-8", errors="ignore") as f:
            rag_content = f.read()
        self.assertIn('fc = os.path.join(gdb_path, "Wind_Vector_%s" % suffix)', rag_content)
        self.assertIn('arcpy.analysis.Clip(fish_pts, in_clip_layer, clipped_pts)', rag_content)

    def test_07_strict_mask_and_clip_in_code(self):
        """Verify arcpy.env.extent and ExtractByMask usage."""
        # In POWER_Climate_Atlas_Generator_10_8.pyt
        with io.open(PYT_PATH, "r", encoding="utf-8", errors="ignore") as f:
            pyt_content = f.read()
        self.assertIn('arcpy.env.extent = mask', pyt_content)
        self.assertIn('ExtractByMask(surf, effective_mask)', pyt_content)

        # In raster_atlas_generator.py
        with io.open(os.path.join(ROOT_DIR, "raster_atlas_generator.py"), "r", encoding="utf-8", errors="ignore") as f:
            rag_content = f.read()
        self.assertIn('arcpy.env.extent = clip_layer', rag_content)
        self.assertIn('clipped = ExtractByMask(raw_interp, clip_layer)', rag_content)

    def test_08_dew_point_module_separated(self):
        """Verify Dew Point is an independent module with 6 indicators and own folder."""
        # Check pyt
        self.assertIn("Dew Point", pyt_mod.PRIMARY_MODULES_ALL)
        self.assertEqual(pyt_mod.MODULE_FOLDER.get("Dew Point"), "07_Dew_Point")
        self.assertEqual(pyt_mod.MODULE_SHORT.get("Dew Point"), "Dew_Point")
        td_defs = [r[0] for r in pyt_mod.FIELD_DEFS if r[4] == "Dew Point"]
        expected_td = [
            "Td_Annual_Mean",
            "Td_Winter_Mean",
            "Td_Spring_Mean",
            "Td_Summer_Mean",
            "Td_Autumn_Mean",
            "Td_Annual_Range"
        ]
        self.assertEqual(td_defs, expected_td)
        # Ensure no Td_* in Temperature
        temp_defs = [r[0] for r in pyt_mod.FIELD_DEFS if r[4] == "Temperature"]
        self.assertTrue(all(not f.startswith("Td_") for f in temp_defs))

        # Check raster_atlas_generator
        self.assertIn("Dew Point", rag.PRIMARY_MODULES_ALL)
        self.assertEqual(rag.MODULE_FOLDER.get("Dew Point"), "07_Dew_Point")
        self.assertEqual(rag.MODULE_SHORT.get("Dew Point"), "Dew_Point")
        self.assertIn("Dew Point", rag.MODULE_INDICATOR_FIELDS)
        rag_td = [f[0] for f in rag.MODULE_INDICATOR_FIELDS["Dew Point"]]
        self.assertEqual(rag_td, expected_td)
        rag_temp = [f[0] for f in rag.MODULE_INDICATOR_FIELDS["Temperature"]]
        self.assertTrue(all(not f.startswith("Td_") for f in rag_temp))

    def test_09_evapotranspiration_unification(self):
        """Verify Evapotranspiration (ET) unification: 8 seasonal & annual indicators, folder 14_Evapotranspiration."""
        expected_et = [
            "ET_Annual_Total",
            "ET_Annual_Mean",
            "ET_Annual_Range",
            "ET_Seasonal_Range",
            "ET_Winter_Total",
            "ET_Spring_Total",
            "ET_Summer_Total",
            "ET_Autumn_Total"
        ]
        # In pyt
        self.assertIn("Evapotranspiration", pyt_mod.DERIVED_MODULES_ALL)
        self.assertEqual(pyt_mod.MODULE_FOLDER.get("Evapotranspiration"), "14_Evapotranspiration")
        self.assertEqual(pyt_mod.MODULE_SHORT.get("Evapotranspiration"), "Evapotranspiration")
        et_defs = [r[0] for r in pyt_mod.FIELD_DEFS if r[4] == "Evapotranspiration" and r[0] != "PET_Hargreaves_Annual"]
        self.assertEqual(et_defs, expected_et)

        # In raster_atlas_generator
        self.assertIn("Evapotranspiration", rag.DERIVED_MODULES_ALL)
        self.assertEqual(rag.MODULE_FOLDER.get("Evapotranspiration"), "14_Evapotranspiration")
        self.assertEqual(rag.MODULE_SHORT.get("Evapotranspiration"), "Evapotranspiration")
        self.assertIn("Evapotranspiration", rag.MODULE_INDICATOR_FIELDS)
        rag_et = [f[0] for f in rag.MODULE_INDICATOR_FIELDS["Evapotranspiration"]]
        self.assertEqual(rag_et, expected_et)


if __name__ == "__main__":
    unittest.main()

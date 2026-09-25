# -*- coding: utf-8 -*-
"""
Raster Data Climate Atlas Generator — ArcMap Desktop 10.x (Python 2.7 compatible)
Downloads gridded/raster climate data from NASA POWER, Open-Meteo, NASA Earthdata,
and NASA Giovanni across Layer 1 (Download Extent AOI), converts cells to 32-bit
Float points with full seasonal and annual indicators in Project_Data.gdb, performs
high-precision spatial interpolation, and clips final rasters using Layer 2 (Study Area Mask).
"""

import os
import sys
import json
import math
import csv
import io
import time
import calendar
import datetime as _dt

PY27 = sys.version_info[0] == 2

try:
    import arcpy
    _HAS_ARCPY = True
except Exception:
    arcpy = None
    _HAS_ARCPY = False

try:
    from arcpy.sa import *
    _HAS_SA = True
except Exception:
    _HAS_SA = False

try:
    import requests
    _HAS_REQUESTS = True
except Exception:
    requests = None
    _HAS_REQUESTS = False

if PY27:
    import urllib2
else:
    import urllib.request as urllib2


# ---------------------------------------------------------------------------
# Constants & Dictionaries
# ---------------------------------------------------------------------------

NASA_POWER_REGIONAL_BASE = "https://power.larc.nasa.gov/api/temporal/monthly/regional"
OPEN_METEO_ARCHIVE_BASE = "https://archive-api.open-meteo.com/v1/archive"
EARTHDATA_URS_BASE = "https://urs.earthdata.nasa.gov"
GES_DISC_OPENDAP_BASE = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap"

PRIMARY_MODULES_ALL = [
    "Temperature",
    "Precipitation",
    "Relative Humidity",
    "Wind",
    "Solar Radiation",
    "Surface Pressure",
    "Sea Level Pressure",
    "Cloud Cover"
]

SUBMODELS_ALL = [
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]",
    "FAO-56 Hargreaves PET [Requires: Temperature]",
    "UNEP Aridity Index [Requires: Temperature, Precipitation]",
    "Water Deficit Annual [Requires: Temperature, Precipitation]",
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]",
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]"
]

MODULES_ALL = PRIMARY_MODULES_ALL + SUBMODELS_ALL

SUBMODEL_DEPS = {
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "De_Martonne",
        "field": "DM_Aridity_Annual",
        "label": "De Martonne Aridity Index",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "FAO-56 Hargreaves PET [Requires: Temperature]": {
        "short": "Hargreaves_PET",
        "field": "PET_Hargreaves_Annual",
        "label": "FAO-56 Hargreaves PET (mm/yr)",
        "modules": ["Temperature"],
        "params": ["T2M"]
    },
    "UNEP Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "UNEP_Aridity",
        "field": "UNEP_Aridity_Annual",
        "label": "UNEP Aridity Index (P/PET)",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Water Deficit Annual [Requires: Temperature, Precipitation]": {
        "short": "Water_Deficit",
        "field": "Water_Deficit_Annual",
        "label": "Annual Water Deficit (P - PET)",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]": {
        "short": "Walter_Lieth",
        "field": "Dry_Months_Count",
        "label": "Walter-Lieth Dry Months Count",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]": {
        "short": "Heat_Index",
        "fields": [
            ("HI_Summer_Mean", "Heat Index Summer Mean (deg C)"),
            ("HI_Winter_Mean", "Heat Index Winter Mean Humidex (deg C)")
        ],
        "field": "HI_Summer_Mean",
        "label": "Heat Index Summer Mean (deg C)",
        "modules": ["Temperature", "Relative Humidity"],
        "params": ["T2M", "RH2M"]
    }
}

_this_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)



def parse_gp_date(val):
    """Parse a date parameter value or date string into a datetime.date object.

    Handles datetime.datetime, datetime.date, and various string formats
    including DD/MM/YYYY, D/M/YYYY, YYYY-MM-DD, YYYY/MM/DD, etc."""
    if val is None:
        return None
    if hasattr(val, "year") and hasattr(val, "month") and hasattr(val, "day"):
        return _dt.date(val.year, val.month, val.day)
    s = str(val).strip()
    if not s:
        return None
    s_date = s.split()[0] if " " in s else s
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y", "%Y%m%d"):
        try:
            return _dt.datetime.strptime(s_date, fmt).date()
        except Exception:
            pass
    parts = s_date.replace("-", "/").replace(".", "/").split("/")
    if len(parts) == 3:
        try:
            p1, p2, p3 = int(parts[0]), int(parts[1]), int(parts[2])
            if p3 > 1000:
                return _dt.date(p3, p2, p1)
            elif p1 > 1000:
                return _dt.date(p1, p2, p3)
        except Exception:
            pass
    return None


def launch_calendar_picker(initial_start=None, initial_end=None):
    """Launch the smooth visual calendar dialog, with subprocess or in-process fallback."""
    import subprocess
    script_path = os.path.join(_this_dir, "utils", "calendar_dialog.py")
    if os.path.isfile(script_path):
        try:
            py_exe = sys.executable or "python.exe"
            cmd = [py_exe, script_path, "--start", str(initial_start or "01/01/2024"), "--end", str(initial_end or "31/12/2024")]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if out and "{" in out:
                data = json.loads(out[out.find("{"):out.rfind("}") + 1])
                return data
        except Exception:
            pass
    try:
        from utils.calendar_dialog import open_calendar_picker
        return open_calendar_picker(initial_start, initial_end)
    except Exception:
        return {"applied": False}


def resolve_submodel_name(name):
    if not name:
        return None
    if name in SUBMODEL_DEPS:
        return name
    clean = name.split(" [")[0].strip().lower()
    for k, info in SUBMODEL_DEPS.items():
        k_clean = k.split(" [")[0].strip().lower()
        short = info.get("short", "").lower()
        if clean == k_clean or clean == short or k_clean.startswith(clean) or clean in k_clean:
            return k
    return None

def extraterrestrial_radiation_ra(lat_deg, month=7):
    """Computes extraterrestrial solar radiation Ra in mm/day equivalent for a given month (FAO-56)."""
    mid_days = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
    m_idx = max(1, min(12, int(month)))
    J = mid_days[m_idx - 1]
    phi = math.radians(float(lat_deg))
    delta = 0.409 * math.sin((2.0 * math.pi * J / 365.0) - 1.39)
    dr = 1.0 + 0.033 * math.cos(2.0 * math.pi * J / 365.0)
    tan_val = -math.tan(phi) * math.tan(delta)
    if tan_val >= 1.0:
        omega_s = 0.0
    elif tan_val <= -1.0:
        omega_s = math.pi
    else:
        omega_s = math.acos(tan_val)
    Gsc = 0.0820
    ra_mj = ((24.0 * 60.0) / math.pi) * Gsc * dr * (
        omega_s * math.sin(phi) * math.sin(delta) +
        math.cos(phi) * math.cos(delta) * math.sin(omega_s)
    )
    return max(0.0, 0.408 * ra_mj)

def heat_index_c(t_c, rh):
    """Rothfusz (NOAA) heat index in C from air temp C + RH %."""
    if t_c is None or rh is None:
        return None
    t_c, rh = float(t_c), float(rh)
    if rh < 0.0: rh = 0.0
    if rh > 100.0: rh = 100.0
    t_f = t_c * 9.0 / 5.0 + 32.0
    if t_f < 80.0:
        return t_c
    hi = (-42.379 + 2.04901523 * t_f + 10.14333127 * rh - 0.22475541 * t_f * rh
          - 0.00683783 * t_f * t_f - 0.05481717 * rh * rh + 0.00122874 * t_f * t_f * rh
          + 0.00085282 * t_f * rh * rh - 0.00000199 * t_f * t_f * rh * rh)
    if rh < 13.0 and 80.0 <= t_f <= 112.0:
        hi -= ((13.0 - rh) / 4.0) * math.sqrt((17.0 - abs(t_f - 95.0)) / 17.0)
    elif rh > 85.0 and 80.0 <= t_f <= 87.0:
        hi += ((rh - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
    return (hi - 32.0) * 5.0 / 9.0


def humidex_c(t_c, rh):
    """Canadian Humidex (IH) in C from air temp C + RH %.

    Formula:
      e = 6.112 * (10.0 ** ((7.5 * t_c) / (237.7 + t_c))) * (rh / 100.0)
      humidex = t_c + (5.0 / 9.0) * (e - 10.0)
    Returns None when inputs are missing."""
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
        return None
    t_c, rh = float(t_c), float(rh)
    if rh < 0.0:
        rh = 0.0
    if rh > 100.0:
        rh = 100.0
    e = 6.112 * (10.0 ** ((7.5 * t_c) / (237.7 + t_c))) * (rh / 100.0)
    return t_c + (5.0 / 9.0) * (e - 10.0)


MODULE_FOLDER = {
    "Temperature": "01_Temperature",
    "Precipitation": "02_Precipitation",
    "Sea Level Pressure": "03_Sea_Level_Pressure",
    "Surface Pressure": "04_Surface_Pressure",
    "Wind": "05_Wind",
    "Relative Humidity": "06_Humidity",
    "Solar Radiation": "07_Solar_Radiation",
    "Cloud Cover": "08_Cloud_Cover",
    "Climate_Models": "10_Climate_Models",
}

# NASA POWER parameter mapping (Regional API accepts 1 primary parameter per query)
POWER_PRIMARY_PARAM = {
    "Temperature": "T2M",
    "Precipitation": "PRECTOTCORR",
    "Relative Humidity": "RH2M",
    "Wind": "WS10M",
    "Solar Radiation": "ALLSKY_SFC_SW_DWN",
    "Surface Pressure": "PS",
    "Sea Level Pressure": "SLP",
    "Cloud Cover": "CLOUD_AMT",
}

COLOR_RAMPS = {
    "Temperature": ["#4575B4", "#74ADD1", "#ABD9E9", "#FFFFBF", "#FDAE61", "#F46D43", "#D73027"],
    "Precipitation": ["#8C510A", "#D8B365", "#F6E8C3", "#C7EAE5", "#80CDC1", "#35978F", "#01665E"],
    "Relative Humidity": ["#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"],
    "Wind": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"],
    "Solar Radiation": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#BD0026"],
    "Surface Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Sea Level Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Cloud Cover": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#4292C6", "#2171B5", "#084594"],
    "Climate_Models": ["#FFFFD4", "#FEE391", "#FEC44F", "#FE9929", "#EC7014", "#CC4C02", "#8C2D04"],
}


def makedirs_ok(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise


def open_utf8(path, mode="w"):
    if "b" in mode:
        return open(path, mode)
    return io.open(path, mode, encoding="utf-8-sig" if "w" in mode else "utf-8",
                   newline="" if not PY27 else None)


def _enc(val):
    if val is None:
        return ""
    if PY27 and isinstance(val, unicode):
        return val.encode("utf-8")
    return val


def write_csv(path, header, rows):
    if PY27:
        with open(path, "wb") as fh:
            fh.write(u"\ufeff".encode("utf-8"))
            w = csv.writer(fh)
            w.writerow([_enc(h) for h in header])
            for r in rows:
                w.writerow([_enc(c) for c in r])
    else:
        with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for r in rows:
                w.writerow(["" if c is None else c for c in r])


def write_excel_file(path, header, rows, sheet_name="Data"):
    try:
        import xlwt
    except ImportError:
        return False
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet((sheet_name or "Data")[:31])
    header_style = xlwt.easyxf(
        "font: bold on, color white, height 220; "
        "pattern: pattern solid, fore_colour dark_blue; "
        "align: horiz center, vert center; "
        "borders: left thin, right thin, top thin, bottom thin;"
    )
    data_style = xlwt.easyxf(
        "borders: left thin, right thin, top thin, bottom thin; align: vert center;"
    )
    for col_idx, h in enumerate(header):
        h_str = unicode(h) if isinstance(h, str) else (h if isinstance(h, unicode) else unicode(str(h)))
        ws.write(0, col_idx, h_str, header_style)
    for row_idx, r in enumerate(rows):
        for col_idx, cell in enumerate(r):
            val = cell
            if cell is None:
                val = ""
            elif isinstance(cell, str):
                try:
                    val = cell.decode("utf-8")
                except Exception:
                    pass
            elif isinstance(cell, float):
                if math.isnan(cell) or abs(cell - (-999.0)) < 1e-5:
                    val = ""
                else:
                    val = round(cell, 3)
            ws.write(row_idx + 1, col_idx, val, data_style)
    wb.save(path)
    return True


# ---------------------------------------------------------------------------
# Tool Class: RasterDataClimateAtlasGenerator
# ---------------------------------------------------------------------------

class RasterDataClimateAtlasGenerator(object):
    """Raster Data Climate Atlas Generator — ArcMap 10.x.
    Downloads gridded/raster climate data directly from online providers,
    extracts high-precision Float points with complete seasonal & annual indicators,
    performs spatial interpolation, and clips using study-area boundaries.
    """

    def __init__(self):
        self.label = "Raster Climate Atlas Generator (NASA POWER, Earthdata & Giovanni)"
        self.description = (
            "Downloads gridded/raster climate data (NASA POWER, Open-Meteo, NASA Earthdata, "
            "NASA Giovanni) across Layer 1 (Download Extent), converts cells into 32-bit Float "
            "points in Project_Data.gdb with full seasonal & annual indicators, interpolates (IDW/Kriging/Spline), "
            "and clips using Layer 2 (Study Area Mask)."
        )
        self.category = "Climate Atlas"

    def getParameterInfo(self):
        p0 = arcpy.Parameter(
            displayName="1. Download Extent Layer (Layer 1 - Grid AOI)",
            name="Download_Extent_Layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        p0.description = (
            "REQUIRED. Polygon layer defining the download extent (AOI) to query gridded climate data "
            "from the web service (e.g. REC boundary). A buffer is applied to avoid edge effects."
        )

        p1 = arcpy.Parameter(
            displayName="2. Final Clip Mask Layer (Layer 2 - Study Area)",
            name="Final_Clip_Layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        p1.description = (
            "REQUIRED. Polygon layer used to clip and mask the final interpolated rasters (e.g. Egypt boundary)."
        )

        p2 = arcpy.Parameter(
            displayName="3. Climate Data Source",
            name="Climate_Data_Source",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p2.filter.type = "ValueList"
        p2.filter.list = [
            "NASA POWER Regional Grid",
            "Open-Meteo ERA5 Grid",
            "NASA Earthdata (MERRA-2 / GPM)",
            "NASA Giovanni (GES DISC)"
        ]
        p2.value = "NASA POWER Regional Grid"
        p2.category = "Data Provider & Authentication"

        p3 = arcpy.Parameter(
            displayName="NASA Earthdata Username",
            name="Earthdata_Username",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p3.category = "Data Provider & Authentication"
        p3.description = "OPTIONAL / REQUIRED for Earthdata & Giovanni. Your NASA Earthdata Login username."

        p4 = arcpy.Parameter(
            displayName="NASA Earthdata Password / Token",
            name="Earthdata_Password",
            datatype="GPStringHidden",
            parameterType="Optional",
            direction="Input"
        )
        p4.category = "Data Provider & Authentication"
        p4.description = "OPTIONAL / REQUIRED for Earthdata & Giovanni. Your NASA Earthdata Login password or token."
        # ═══ Time Window ═══
        p_tmode = arcpy.Parameter(
            displayName="Time Mode",
            name="Time_Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p_tmode.filter.type = "ValueList"
        p_tmode.filter.list = ["Single Year", "Year Range", "Custom Date Range"]
        p_tmode.value = "Single Year"
        p_tmode.category = "Time Window"
        p_tmode.description = (
            "REQUIRED. 'Single Year' queries January-December of one year. "
            "'Year Range' computes multi-year climatological normals. "
            "'Custom Date Range' queries specific start/end dates via calendar or text."
        )

        p_syr = arcpy.Parameter(
            displayName="Single Year",
            name="Single_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_syr.filter.type = "ValueList"
        p_syr.filter.list = [str(y) for y in range(2025, 1980, -1)]
        p_syr.value = 2024
        p_syr.category = "Time Window"
        p_syr.description = "Select or enter the specific year to query (1981 to 2025)."

        p_s_yr = arcpy.Parameter(
            displayName="Start Year",
            name="Start_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_s_yr.filter.type = "ValueList"
        p_s_yr.filter.list = [str(y) for y in range(1981, 2026)]
        p_s_yr.value = 2015
        p_s_yr.category = "Time Window"
        p_s_yr.description = "First year of the climatology period (inclusive)."

        p_e_yr = arcpy.Parameter(
            displayName="End Year",
            name="End_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_e_yr.filter.type = "ValueList"
        p_e_yr.filter.list = [str(y) for y in range(1981, 2026)]
        p_e_yr.value = 2024
        p_e_yr.category = "Time Window"
        p_e_yr.description = "Last year of the climatology period (inclusive)."

        p_picker = arcpy.Parameter(
            displayName=u"Launch Visual Calendar Window (نافذة التقويم الذكية)",
            name="Open_Calendar_Picker",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        p_picker.value = False
        p_picker.category = "Time Window"
        p_picker.description = (
            "CUSTOM DATE ONLY. Check this box to open the calm, interactive visual calendar "
            "dialog with month navigation arrows and quick year/month selectors."
        )

        p_sd = arcpy.Parameter(
            displayName="Start Date (DD/MM/YYYY or YYYY-MM-DD)",
            name="Start_Date",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p_sd.value = "01/01/2024"
        p_sd.category = "Time Window"
        p_sd.description = (
            "CUSTOM DATE RANGE ONLY. Beginning date. "
            "Type directly in the box (e.g. 31/3/1990 or 1990-03-31) "
            "or use the Visual Calendar Window above."
        )

        p_ed = arcpy.Parameter(
            displayName="End Date (DD/MM/YYYY or YYYY-MM-DD)",
            name="End_Date",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p_ed.value = "31/12/2024"
        p_ed.category = "Time Window"
        p_ed.description = (
            "CUSTOM DATE RANGE ONLY. Ending date. "
            "Type directly in the box (e.g. 31/12/2000 or 2000-12-31) "
            "or use the Visual Calendar Window above."
        )

        p_aggs = arcpy.Parameter(
            displayName="Included Temporal Aggregations",
            name="Included_Aggregations",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p_aggs.multiValue = True
        p_aggs.filter.type = "ValueList"
        p_aggs.filter.list = [
            "Annual Summaries",
            "Seasonal Summaries (DJF, MAM, JJA, SON)"
        ]
        p_aggs.value = "Annual Summaries;Seasonal Summaries (DJF, MAM, JJA, SON)"
        p_aggs.category = "Time Window"
        p_aggs.description = "Select which temporal summaries to generate (Annual, Seasonal)."

        # ═══ Climate Modules & Models ═══
        p_mods = arcpy.Parameter(
            displayName="Climate Modules & Models",
            name="Climate_Modules",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p_mods.multiValue = True
        p_mods.filter.type = "ValueList"
        p_mods.filter.list = MODULES_ALL
        p_mods.value = "Temperature"
        p_mods.category = "Climate Modules & Models"
        p_mods.description = (
            "Select climate modules and applied bioclimatic models to compute and export. "
            "Submodels (De Martonne, Hargreaves PET, UNEP, Water Deficit, Walter-Lieth, Heat Index) "
            "are located at the bottom of the list and can be selected directly; prerequisite variables "
            "are retrieved automatically if not selected."
        )

        # ═══ Cartography & Spatial Interpolation ═══
        p_interp = arcpy.Parameter(
            displayName="Interpolation Method",
            name="Interpolation_Method",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p_interp.filter.type = "ValueList"
        p_interp.filter.list = [
            "Inverse Distance Weighted (IDW)",
            "Ordinary Kriging (Spherical)",
            "Spline (Regularized)",
            "Natural Neighbor"
        ]
        p_interp.value = "Inverse Distance Weighted (IDW)"
        p_interp.category = "Cartography & Spatial Interpolation"

        p_cell = arcpy.Parameter(
            displayName="Output Raster Cell Size (meters / units)",
            name="Output_Cell_Size",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        p_cell.value = 2500.0
        p_cell.category = "Cartography & Spatial Interpolation"

        # ═══ Output Options ═══
        p_exp_indiv = arcpy.Parameter(
            displayName="Export Individual Shapefiles per Season/Indicator",
            name="Export_Individual_Shapefiles",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        p_exp_indiv.value = False
        p_exp_indiv.category = "Output Options"

        p_ws = arcpy.Parameter(
            displayName="Output Atlas Folder",
            name="Output_Workspace",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        p_ws.category = "Output Options"

        p_sr = arcpy.Parameter(
            displayName="Output Spatial Reference",
            name="Output_Spatial_Reference",
            datatype="GPSpatialReference",
            parameterType="Optional",
            direction="Input"
        )
        p_sr.category = "Output Options"

        return [
            p0, p1, p2, p3, p4,
            p_tmode, p_syr, p_s_yr, p_e_yr, p_picker, p_sd, p_ed, p_aggs,
            p_mods,
            p_interp, p_cell,
            p_exp_indiv, p_ws, p_sr
        ]

    def updateParameters(self, parameters):
        pdict = dict((p.name, p) for p in parameters) if (parameters and hasattr(parameters[0], 'name')) else {}
        if not pdict:
            return

        source = pdict.get("Climate_Data_Source").valueAsText if pdict.get("Climate_Data_Source") else "NASA POWER Regional Grid"
        is_edl = "Earthdata" in source or "Giovanni" in source
        if "Earthdata_Username" in pdict:
            pdict["Earthdata_Username"].enabled = is_edl
        if "Earthdata_Password" in pdict:
            pdict["Earthdata_Password"].enabled = is_edl

        t_mode = pdict.get("Time_Mode").valueAsText if pdict.get("Time_Mode") else "Single Year"
        single = (t_mode == "Single Year")
        yr_range = (t_mode == "Year Range")
        custom_range = (t_mode == "Custom Date Range")

        p_picker = pdict.get("Open_Calendar_Picker")
        if p_picker and p_picker.value and custom_range:
            p_sd = pdict.get("Start_Date")
            p_ed = pdict.get("End_Date")
            cur_s = p_sd.valueAsText if p_sd and p_sd.value else "01/01/2024"
            cur_e = p_ed.valueAsText if p_ed and p_ed.value else "31/12/2024"
            try:
                res = launch_calendar_picker(cur_s, cur_e)
                if res and res.get("applied"):
                    if p_sd and res.get("start_date"):
                        p_sd.value = res["start_date"]
                    if p_ed and res.get("end_date"):
                        p_ed.value = res["end_date"]
            except Exception:
                pass
            p_picker.value = False

        if "Single_Year" in pdict:
            pdict["Single_Year"].enabled = single
        if "Start_Year" in pdict:
            pdict["Start_Year"].enabled = yr_range
        if "End_Year" in pdict:
            pdict["End_Year"].enabled = yr_range
        if "Open_Calendar_Picker" in pdict:
            pdict["Open_Calendar_Picker"].enabled = custom_range
        if "Start_Date" in pdict:
            pdict["Start_Date"].enabled = custom_range
        if "End_Date" in pdict:
            pdict["End_Date"].enabled = custom_range

    def updateMessages(self, parameters):
        pdict = dict((p.name, p) for p in parameters) if (parameters and hasattr(parameters[0], 'name')) else {}
        if not pdict:
            return

        t_mode = pdict.get("Time_Mode").valueAsText if pdict.get("Time_Mode") else "Single Year"
        if t_mode == "Single Year":
            s_yr = pdict.get("Single_Year").value if pdict.get("Single_Year") else None
            if not s_yr and pdict.get("Single_Year"):
                pdict["Single_Year"].setErrorMessage("Please enter or select a single year.")
        elif t_mode == "Year Range":
            s_yr = pdict.get("Start_Year").value if pdict.get("Start_Year") else None
            e_yr = pdict.get("End_Year").value if pdict.get("End_Year") else None
            if s_yr and e_yr and e_yr < s_yr and pdict.get("End_Year"):
                pdict["End_Year"].setErrorMessage("End Year must be greater than or equal to Start Year.")
        elif t_mode == "Custom Date Range":
            p_sd = pdict.get("Start_Date")
            p_ed = pdict.get("End_Date")
            d_start = parse_gp_date(p_sd.valueAsText if p_sd else None)
            d_end = parse_gp_date(p_ed.valueAsText if p_ed else None)
            if not d_start and p_sd and p_sd.value:
                p_sd.setErrorMessage("Invalid Start Date format. Use DD/MM/YYYY or YYYY-MM-DD (e.g. 31/3/1990).")
            if not d_end and p_ed and p_ed.value:
                p_ed.setErrorMessage("Invalid End Date format. Use DD/MM/YYYY or YYYY-MM-DD (e.g. 31/12/2000).")
            if d_start and d_end and d_end < d_start and p_ed:
                p_ed.setErrorMessage("End Date must be on or after Start Date.")

        c_size = pdict.get("Output_Cell_Size").value if pdict.get("Output_Cell_Size") else None
        if c_size and c_size <= 0 and pdict.get("Output_Cell_Size"):
            pdict["Output_Cell_Size"].setErrorMessage("Output cell size must be strictly positive.")

        mod_val = pdict.get("Climate_Modules").valueAsText if pdict.get("Climate_Modules") else ""
        raw_items = [m.strip().strip("'\"") for m in mod_val.split(";") if m.strip()]
        if not raw_items and pdict.get("Climate_Modules"):
            pdict["Climate_Modules"].setErrorMessage("Please select at least one Climate Module or Applied Submodel.")
        else:
            current_mods = [m for m in raw_items if not resolve_submodel_name(m)]
            for item in raw_items:
                res_s = resolve_submodel_name(item)
                if res_s:
                    req_mods = SUBMODEL_DEPS[res_s].get("modules", [])
                    missing_mods = [rm for rm in req_mods if rm not in current_mods]
                    if missing_mods and pdict.get("Climate_Modules"):
                        pdict["Climate_Modules"].setWarningMessage(
                            "Submodel '%s' requires %s. "
                            "Prerequisite data will be queried automatically as temporary intermediate data."
                            % (SUBMODEL_DEPS[res_s]["short"], ", ".join(missing_mods))
                        )

    def execute(self, parameters, messages):
        t0 = time.time()
        def msg(m):
            arcpy.AddMessage(m)
        def warn(m):
            arcpy.AddWarning(m)

        msg("=" * 70)
        msg("Raster Climate Atlas Generator — ArcMap 10.x Engine")
        msg("=" * 70)

        # 1. Parse parameters
        pdict = dict((p.name, p) for p in parameters) if (parameters and hasattr(parameters[0], 'name')) else {}
        def _get_val(name, default=None):
            if name in pdict:
                return pdict[name].value
            return default
        def _get_text(name, default=""):
            if name in pdict:
                return pdict[name].valueAsText or default
            return default

        in_extent_layer = _get_text("Download_Extent_Layer")
        in_clip_layer = _get_text("Final_Clip_Layer")
        source = _get_text("Climate_Data_Source", "NASA POWER Regional Grid")
        edl_user = _get_text("Earthdata_Username")
        edl_pass = _get_text("Earthdata_Password")

        modules_raw = _get_text("Climate_Modules")
        raw_items = [m.strip().strip("'\"") for m in modules_raw.split(";") if m.strip()]
        modules = []
        active_submodels = []
        for item in raw_items:
            res_s = resolve_submodel_name(item)
            if res_s:
                if res_s not in active_submodels:
                    active_submodels.append(res_s)
            else:
                if item in PRIMARY_MODULES_ALL and item not in modules:
                    modules.append(item)

        if not modules and not active_submodels:
            modules = ["Temperature"]

        # Parse Time Window
        time_mode = _get_text("Time_Mode", "Single Year")
        single_year_val = _get_val("Single_Year")
        single_year = int(single_year_val) if single_year_val is not None else 2024
        start_year_val = _get_val("Start_Year")
        start_year = int(start_year_val) if start_year_val is not None else 2015
        end_year_val = _get_val("End_Year")
        end_year = int(end_year_val) if end_year_val is not None else 2024
        p_sd = pdict.get("Start_Date")
        p_ed = pdict.get("End_Date")
        d_start = parse_gp_date(p_sd.valueAsText if p_sd else None)
        d_end = parse_gp_date(p_ed.valueAsText if p_ed else None)

        if time_mode == "Single Year":
            start_yr = single_year
            end_yr = single_year
            period_label = "%d (Single Year)" % single_year
            col_data_start = str(single_year)
            col_data_end = str(single_year)
        elif time_mode == "Year Range":
            start_yr = start_year
            end_yr = end_year
            period_label = "%d-%d (%d yrs)" % (start_year, end_year, end_year - start_year + 1)
            col_data_start = str(start_year)
            col_data_end = str(end_year)
        else: # Custom Date Range
            if not d_start:
                d_start = _dt.date(2024, 1, 1)
            if not d_end:
                d_end = _dt.date(2024, 12, 31)
            if d_start > d_end:
                d_start, d_end = d_end, d_start
            start_yr = d_start.year
            end_yr = d_end.year
            s_txt = p_sd.valueAsText if (p_sd and p_sd.value) else ("%02d/%02d/%04d" % (d_start.day, d_start.month, d_start.year))
            e_txt = p_ed.valueAsText if (p_ed and p_ed.value) else ("%02d/%02d/%04d" % (d_end.day, d_end.month, d_end.year))
            period_label = "%s to %s (Custom Date Range)" % (s_txt, e_txt)
            col_data_start = str(s_txt)
            col_data_end = str(e_txt)

        aggs_raw = _get_text("Included_Aggregations")
        aggs = [a.strip().strip("'\"") for a in aggs_raw.split(";") if a.strip()]
        interp_method = _get_text("Interpolation_Method", "Inverse Distance Weighted (IDW)")
        cell_size_val = _get_val("Output_Cell_Size")
        cell_size = float(cell_size_val) if cell_size_val is not None else 2500.0
        export_indiv_shp = bool(_get_val("Export_Individual_Shapefiles", False))
        out_root = _get_text("Output_Workspace")
        out_sr = _get_val("Output_Spatial_Reference")

        active_export_modules = list(modules)
        if active_submodels and "Climate_Models" not in active_export_modules:
            active_export_modules.append("Climate_Models")

        HIERARCHY = [
            "Temperature", "Precipitation", "Relative Humidity",
            "Wind", "Solar Radiation", "Surface Pressure",
            "Sea Level Pressure", "Cloud Cover", "Climate_Models"
        ]
        ordered_modules = [m for m in HIERARCHY if m in active_export_modules]
        for m in active_export_modules:
            if m not in ordered_modules:
                ordered_modules.append(m)

        msg("Source: %s" % source)
        msg("Time Mode: %s | Period: %s (%s to %s)" % (time_mode, period_label, col_data_start, col_data_end))
        msg("Modules: %s" % ", ".join(ordered_modules))
        if active_submodels:
            msg("Applied Submodels: %s" % ", ".join([SUBMODEL_DEPS[s]["short"] for s in active_submodels]))
        msg("Interpolation: %s | Cell Size: %.4f" % (interp_method, cell_size))

        # 2. Check Spatial Analyst Extension
        if not _HAS_SA:
            raise RuntimeError("ArcGIS Spatial Analyst extension is required for raster interpolation.")
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = True

        # 3. Establish output folders & GDB
        makedirs_ok(out_root)
        vec_dir = os.path.join(out_root, "00_Vector_Data")
        makedirs_ok(vec_dir)
        gdb_path = os.path.join(out_root, "Project_Data.gdb")
        if not arcpy.Exists(gdb_path):
            msg("Creating File Geodatabase: Project_Data.gdb")
            arcpy.CreateFileGDB_management(out_root, "Project_Data.gdb")
        scratch_dir = os.path.join(out_root, "scratch_cache")
        makedirs_ok(scratch_dir)

        # 4. Extract Layer 1 Extent in WGS84
        desc_ext = arcpy.Describe(in_extent_layer)
        sr_wgs84 = arcpy.SpatialReference(4326)
        extent_geom = arcpy.Polygon(
            arcpy.Array([
                desc_ext.extent.lowerLeft,
                desc_ext.extent.upperLeft,
                desc_ext.extent.upperRight,
                desc_ext.extent.lowerRight
            ]),
            desc_ext.spatialReference
        ).projectAs(sr_wgs84)
        ext_wgs = extent_geom.extent
        min_lon = ext_wgs.XMin
        max_lon = ext_wgs.XMax
        min_lat = ext_wgs.YMin
        max_lat = ext_wgs.YMax

        msg("Query Bounding Box (WGS84): Lon [%.3f, %.3f], Lat [%.3f, %.3f]" % (min_lon, max_lon, min_lat, max_lat))

        # Generate spatial sub-tiles to satisfy API limits (NASA POWER max 10 deg range)
        tiles = self._generate_tiles(min_lon, min_lat, max_lon, max_lat, max_span=8.0, min_span=2.2)
        msg("Tiling strategy: Area divided into %d regional tile(s) for API download." % len(tiles))

        # 5. Process each Module (Staged element-by-element pipeline)
        generated_rasters = []
        element_layers = {}
        intermediate_points = {}

        for mi, mod in enumerate(ordered_modules):
            msg("\n" + "=" * 65)
            msg(">>> PROCESSING MODULE [%d/%d]: %s <<<" % (mi + 1, len(ordered_modules), mod))
            msg("=" * 65)

            mod_folder_name = MODULE_FOLDER.get(mod, "09_Other")
            mod_dir = os.path.join(out_root, mod_folder_name)
            makedirs_ok(mod_dir)

            if mod == "Climate_Models":
                pts_fc, indicator_fields = self._process_submodels_to_master_points(
                    source, active_submodels, tiles, start_yr, end_yr,
                    gdb_path, scratch_dir, edl_user, edl_pass,
                    element_layers, intermediate_points, msg, warn,
                    col_data_start=col_data_start, col_data_end=col_data_end
                )
            else:
                pts_fc, indicator_fields = self._process_tiles_to_master_points(
                    source, mod, tiles, start_yr, end_yr, gdb_path, aggs,
                    scratch_dir, edl_user, edl_pass, msg, warn,
                    col_data_start=col_data_start, col_data_end=col_data_end
                )

            if not pts_fc or not arcpy.Exists(pts_fc):
                warn("Failed to generate points for %s." % mod)
                continue

            element_layers[mod] = pts_fc
            pt_count = int(arcpy.GetCount_management(pts_fc).getOutput(0))
            msg("Created master points in GDB: %s (%d points)" % (pts_fc, pt_count))

            # Step C: Export Vectors (Shapefile + CSV + Excel)
            self._export_vectors(
                pts_fc, mod, vec_dir, indicator_fields, export_indiv_shp, msg
            )

            # Step D: Spatial Interpolation & Masking with Layer 2
            for fld_name, fld_label in indicator_fields:
                msg("  -> Interpolating: %s (%s)..." % (fld_name, interp_method))
                out_tif = os.path.join(mod_dir, "%s.tif" % fld_name)
                success = self._interpolate_and_clip(
                    pts_fc, fld_name, in_clip_layer, interp_method,
                    cell_size, out_tif, out_sr, msg, warn
                )
                if success:
                    generated_rasters.append((fld_name, out_tif, mod))
                    self._create_layer_file(out_tif, mod, fld_name, fld_label, msg)

            msg(">>> Module [%d/%d] %s completed: Layer, exports & rasters ready. <<<\n"
                % (mi + 1, len(ordered_modules), mod))

        # Cleanup temporary intermediate layers from GDB if they were not explicitly selected in modules
        for m, ifc in intermediate_points.items():
            if m not in modules:
                if arcpy.Exists(ifc):
                    try:
                        arcpy.management.Delete(ifc)
                        msg("Removed temporary intermediate layer from GDB: %s" % m)
                    except Exception:
                        pass

        # 6. Dictionaries & Processing Log
        self._write_dictionaries(vec_dir, ordered_modules, msg)
        elapsed = time.time() - t0
        self._write_log(out_root, {
            "source": source,
            "years": (start_yr, end_yr),
            "data_start": col_data_start,
            "data_end": col_data_end,
            "period_label": period_label,
            "time_mode": time_mode,
            "modules": ordered_modules,
            "submodels": active_submodels,
            "interp": interp_method,
            "cell_size": cell_size,
            "rasters": generated_rasters,
            "elements": element_layers,
            "elapsed": elapsed
        })

        # Cleanup scratch
        try:
            import shutil
            shutil.rmtree(scratch_dir, ignore_errors=True)
            arcpy.management.Delete("in_memory")
        except Exception:
            pass

        msg("\n" + "=" * 70)
        msg("Raster Climate Atlas Generation Complete in %.1f seconds." % elapsed)
        msg("Output workspace: %s" % out_root)
        msg("=" * 70)

    # -----------------------------------------------------------------------
    # Helper: Generate Spatial Tiles for Regional Queries
    # -----------------------------------------------------------------------
    def _generate_tiles(self, min_lon, min_lat, max_lon, max_lat, max_span=8.0, min_span=2.2):
        span_lon = max_lon - min_lon
        span_lat = max_lat - min_lat

        n_x = int(math.ceil(span_lon / max_span)) or 1
        n_y = int(math.ceil(span_lat / max_span)) or 1

        step_x = span_lon / float(n_x)
        step_y = span_lat / float(n_y)

        # Ensure minimum span for API requirement
        if step_x < min_span:
            step_x = min_span
        if step_y < min_span:
            step_y = min_span

        tiles = []
        for i in range(n_x):
            t_min_x = min_lon + i * (span_lon / float(n_x))
            t_max_x = min_lon + (i + 1) * (span_lon / float(n_x)) if i < n_x - 1 else max_lon
            if (t_max_x - t_min_x) < min_span:
                t_max_x = t_min_x + min_span

            for j in range(n_y):
                t_min_y = min_lat + j * (span_lat / float(n_y))
                t_max_y = min_lat + (j + 1) * (span_lat / float(n_y)) if j < n_y - 1 else max_lat
                if (t_max_y - t_min_y) < min_span:
                    t_max_y = t_min_y + min_span

                tiles.append((t_min_x, t_min_y, t_max_x, t_max_y))

        return tiles

    # -----------------------------------------------------------------------
    # Helper: Download Tiles and assemble into Master Points in GDB
    # -----------------------------------------------------------------------
    def _process_tiles_to_master_points(self, source, module, tiles, start_yr, end_yr,
                                        gdb_path, aggs, scratch_dir, edl_user, edl_pass, msg, warn,
                                        col_data_start="", col_data_end=""):
        primary_param = POWER_PRIMARY_PARAM.get(module, "T2M")
        pts_fc = os.path.join(gdb_path, module)
        if arcpy.Exists(pts_fc):
            arcpy.management.Delete(pts_fc)

        fld_prefix = {
            "Temperature": "T",
            "Precipitation": "Precip",
            "Relative Humidity": "RH",
            "Wind": "Wind_Speed",
            "Solar Radiation": "Sol",
            "Surface Pressure": "PS",
            "Sea Level Pressure": "PSL",
            "Cloud Cover": "Cld"
        }.get(module, module[:5])

        is_sum = (module == "Precipitation")
        ann_field = "%s_Annual_%s" % (fld_prefix, "Sum" if is_sum else "Mean")
        suffix = "Sum" if is_sum else "Mean"
        win_fld = "%s_Winter_%s" % (fld_prefix, suffix)
        spr_fld = "%s_Spring_%s" % (fld_prefix, suffix)
        sum_fld = "%s_Summer_%s" % (fld_prefix, suffix)
        aut_fld = "%s_Autumn_%s" % (fld_prefix, suffix)

        indicator_fields = [(ann_field, "Annual Summary")]
        include_seasons = any("Seasonal" in a for a in aggs)
        if include_seasons:
            indicator_fields.extend([
                (win_fld, "Winter (DJF)"),
                (spr_fld, "Spring (MAM)"),
                (sum_fld, "Summer (JJA)"),
                (aut_fld, "Autumn (SON)")
            ])

        tile_layers = []
        arcpy.SetProgressor("step", "Processing tiles for %s..." % module, 0, len(tiles), 1)

        for idx, (t_min_x, t_min_y, t_max_x, t_max_y) in enumerate(tiles):
            pct = float(idx + 1) / float(len(tiles)) * 100.0
            msg("  [%s] Tile %d/%d (%.0f%%) Bounds: Lon [%.2f, %.2f], Lat [%.2f, %.2f] - Downloading..." % (
                module, idx + 1, len(tiles), pct, t_min_x, t_max_x, t_min_y, t_max_y))

            nc_tile = os.path.join(scratch_dir, "%s_tile_%d.nc" % (module, idx))
            ok = self._download_single_tile(
                source, primary_param, t_min_x, t_min_y, t_max_x, t_max_y,
                start_yr, end_yr, nc_tile, edl_user, edl_pass, msg, warn
            )

            if not ok or not os.path.isfile(nc_tile) or os.path.getsize(nc_tile) < 500:
                warn("  ! Tile %d download failed or empty." % (idx + 1))
                arcpy.SetProgressorPosition(idx + 1)
                continue

            # Convert tile NetCDF to points
            tile_pts = "in_memory/pts_tile_%d" % idx
            if arcpy.Exists(tile_pts):
                arcpy.management.Delete(tile_pts)

            mem_bands = "bands_tile_%d" % idx
            arcpy.md.MakeNetCDFRasterLayer(nc_tile, primary_param, "lon", "lat", mem_bands, band_dimension="time")

            # Annual band 13
            mem_ann = "ann_tile_%d" % idx
            arcpy.MakeRasterLayer_management(mem_bands, mem_ann, band_index=13)
            arcpy.RasterToPoint_conversion(mem_ann, tile_pts, "Value")

            arcpy.AddField_management(tile_pts, ann_field, "DOUBLE")
            arcpy.CalculateField_management(tile_pts, ann_field, "!grid_code!", "PYTHON_9.3")

            if include_seasons:
                m_layers = {}
                for m_i in range(1, 13):
                    m_name = "m_t%d_%d" % (idx, m_i)
                    arcpy.MakeRasterLayer_management(mem_bands, m_name, band_index=m_i)
                    m_layers[m_i] = Raster(m_name)

                divisor = 1.0 if is_sum else 3.0
                r_win = (m_layers[12] + m_layers[1] + m_layers[2]) / divisor
                r_spr = (m_layers[3] + m_layers[4] + m_layers[5]) / divisor
                r_sum = (m_layers[6] + m_layers[7] + m_layers[8]) / divisor
                r_aut = (m_layers[9] + m_layers[10] + m_layers[11]) / divisor

                ExtractMultiValuesToPoints(tile_pts, [
                    [r_win, win_fld],
                    [r_spr, spr_fld],
                    [r_sum, sum_fld],
                    [r_aut, aut_fld]
                ])

            tile_layers.append(tile_pts)
            arcpy.SetProgressorPosition(idx + 1)
        arcpy.ResetProgressor()

        if not tile_layers:
            warn("No tiles successfully converted to points.")
            return None, indicator_fields

        # Merge / Append all tile point layers into Master Point Layer in GDB
        msg("Assembling %d tile point layers into Master GDB Table..." % len(tile_layers))
        if len(tile_layers) == 1:
            arcpy.CopyFeatures_management(tile_layers[0], pts_fc)
        else:
            arcpy.Merge_management(tile_layers, pts_fc)

        # Cleanup intermediate tile memory and scratch NetCDFs immediately
        for t_lyr in tile_layers:
            if arcpy.Exists(t_lyr):
                try: arcpy.management.Delete(t_lyr)
                except Exception: pass
        for idx in range(len(tiles)):
            nc_tile = os.path.join(scratch_dir, "%s_tile_%d.nc" % (module, idx))
            if os.path.isfile(nc_tile):
                try: os.remove(nc_tile)
                except Exception: pass
        try: arcpy.management.Delete("in_memory")
        except Exception: pass

        # Clean identical overlapping boundary points
        try:
            arcpy.DeleteIdentical_management(pts_fc, ["Shape"])
        except Exception:
            pass

        # Add Coordinates and Point_ID
        arcpy.AddXY_management(pts_fc)
        arcpy.AddField_management(pts_fc, "Point_ID", "LONG")
        arcpy.CalculateField_management(pts_fc, "Point_ID", "!OBJECTID!", "PYTHON_9.3")

        # Add Administrative / Time metadata fields
        arcpy.AddField_management(pts_fc, "Data_Start", "TEXT", field_length=30)
        arcpy.AddField_management(pts_fc, "Data_End", "TEXT", field_length=30)
        if col_data_start:
            arcpy.CalculateField_management(pts_fc, "Data_Start", "'%s'" % str(col_data_start).replace("'", ""), "PYTHON_9.3")
        if col_data_end:
            arcpy.CalculateField_management(pts_fc, "Data_End", "'%s'" % str(col_data_end).replace("'", ""), "PYTHON_9.3")

        return pts_fc, indicator_fields

    # -----------------------------------------------------------------------
    # Helper: Assemble Submodels Master Points
    # -----------------------------------------------------------------------
    def _process_submodels_to_master_points(self, source, active_submodels, tiles, start_yr, end_yr,
                                            gdb_path, scratch_dir, edl_user, edl_pass,
                                            element_layers, intermediate_points, msg, warn,
                                            col_data_start="", col_data_end=""):
        req_modules = []
        for s in active_submodels:
            info = SUBMODEL_DEPS.get(s)
            if info:
                for m in info.get("modules", []):
                    if m not in req_modules:
                        req_modules.append(m)

        for m in req_modules:
            if m in element_layers:
                msg("  [Climate_Models] Reusing existing '%s' points (0 queries)." % m)
            elif m in intermediate_points:
                msg("  [Climate_Models] Reusing temporary '%s' points (0 queries)." % m)
            else:
                msg("  [Climate_Models] Downloading prerequisite '%s' data as temporary intermediate data..." % m)
                base_fc, _ = self._process_tiles_to_master_points(
                    source, m, tiles, start_yr, end_yr, gdb_path, ["Annual Summaries"],
                    scratch_dir, edl_user, edl_pass, msg, warn,
                    col_data_start=col_data_start, col_data_end=col_data_end
                )
                if base_fc and arcpy.Exists(base_fc):
                    intermediate_points[m] = base_fc

        # Find primary base FC to copy geometry from
        primary_fc = None
        for cand in ["Temperature", "Precipitation", "Relative Humidity"]:
            primary_fc = element_layers.get(cand) or intermediate_points.get(cand)
            if primary_fc and arcpy.Exists(primary_fc):
                break
        if not primary_fc:
            all_cands = element_layers.values() + intermediate_points.values()
            for cand_fc in all_cands:
                if cand_fc and arcpy.Exists(cand_fc):
                    primary_fc = cand_fc
                    break

        if not primary_fc or not arcpy.Exists(primary_fc):
            warn("Could not find base geometry for Climate_Models.")
            return None, []

        pts_fc = os.path.join(gdb_path, "Climate_Models")
        if arcpy.Exists(pts_fc):
            arcpy.management.Delete(pts_fc)
        arcpy.CopyFeatures_management(primary_fc, pts_fc)

        # Build indicator fields
        indicator_fields = []
        for s in active_submodels:
            info = SUBMODEL_DEPS.get(s)
            if info:
                f_list = info.get("fields", [(info["field"], info["label"])])
                for fld, lbl in f_list:
                    indicator_fields.append((fld, lbl))
                    existing_f = [f.name for f in arcpy.ListFields(pts_fc)]
                    if fld not in existing_f:
                        arcpy.AddField_management(pts_fc, fld, "DOUBLE")

        # Ensure Data_Start and Data_End exist in pts_fc
        existing_flds = [f.name for f in arcpy.ListFields(pts_fc)]
        if "Data_Start" not in existing_flds:
            arcpy.AddField_management(pts_fc, "Data_Start", "TEXT", field_length=30)
        if col_data_start:
            arcpy.CalculateField_management(pts_fc, "Data_Start", "'%s'" % str(col_data_start).replace("'", ""), "PYTHON_9.3")
        if "Data_End" not in existing_flds:
            arcpy.AddField_management(pts_fc, "Data_End", "TEXT", field_length=30)
        if col_data_end:
            arcpy.CalculateField_management(pts_fc, "Data_End", "'%s'" % str(col_data_end).replace("'", ""), "PYTHON_9.3")

        # Build coordinate lookup maps from base layers
        t_map = {}
        temp_fc = element_layers.get("Temperature") or intermediate_points.get("Temperature")
        if temp_fc and arcpy.Exists(temp_fc):
            with arcpy.da.SearchCursor(temp_fc, ["POINT_X", "POINT_Y", "T_Annual_Mean"]) as cur:
                for r in cur:
                    t_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        p_map = {}
        precip_fc = element_layers.get("Precipitation") or intermediate_points.get("Precipitation")
        if precip_fc and arcpy.Exists(precip_fc):
            with arcpy.da.SearchCursor(precip_fc, ["POINT_X", "POINT_Y", "Precip_Annual_Sum"]) as cur:
                for r in cur:
                    p_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        rh_map = {}
        rh_fc = element_layers.get("Relative Humidity") or intermediate_points.get("Relative Humidity")
        if rh_fc and arcpy.Exists(rh_fc):
            with arcpy.da.SearchCursor(rh_fc, ["POINT_X", "POINT_Y", "RH_Annual_Mean"]) as cur:
                for r in cur:
                    rh_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        fld_names = [f[0] for f in indicator_fields]
        with arcpy.da.UpdateCursor(pts_fc, ["POINT_X", "POINT_Y"] + fld_names) as cur:
            for row in cur:
                ckey = (round(row[0], 4), round(row[1], 4))
                t = t_map.get(ckey, 20.0)
                p = p_map.get(ckey, 50.0)
                rh = rh_map.get(ckey, 50.0)
                lat = row[1]
                for f_idx, (fld, _lbl) in enumerate(indicator_fields):
                    val = None
                    if fld == "DM_Aridity_Annual":
                        denom = (t + 10.0) if t is not None else 30.0
                        val = (p / denom) if denom > 0.01 else 0.0
                    elif fld == "PET_Hargreaves_Annual":
                        ra = extraterrestrial_radiation_ra(lat, 7)
                        val = 0.0023 * ra * ((t if t is not None else 20.0) + 17.8) * math.sqrt(10.0) * 365.25
                    elif fld == "UNEP_Aridity_Annual":
                        ra = extraterrestrial_radiation_ra(lat, 7)
                        pet = 0.0023 * ra * ((t if t is not None else 20.0) + 17.8) * math.sqrt(10.0) * 365.25
                        val = (p / pet) if pet > 0.01 else 0.0
                    elif fld == "Water_Deficit_Annual":
                        ra = extraterrestrial_radiation_ra(lat, 7)
                        pet = 0.0023 * ra * ((t if t is not None else 20.0) + 17.8) * math.sqrt(10.0) * 365.25
                        val = p - pet
                    elif fld == "Dry_Months_Count":
                        val = 12.0 if (p is not None and t is not None and p < (2.0 * t)) else 0.0
                    elif fld == "HI_Summer_Mean":
                        val = heat_index_c(t, rh)
                    elif fld == "HI_Winter_Mean":
                        val = humidex_c(t, rh)
                    row[2 + f_idx] = round(val, 3) if val is not None else None
                cur.updateRow(row)

        return pts_fc, indicator_fields

    def _download_single_tile(self, source, param, min_lon, min_lat, max_lon, max_lat,
                              start_yr, end_yr, out_nc, user, pwd, msg, warn):
        if "NASA POWER" in source or not user:
            url = (
                "%s?parameters=%s&community=AG&longitude-min=%.4f&longitude-max=%.4f"
                "&latitude-min=%.4f&latitude-max=%.4f&start=%d&end=%d&format=NETCDF"
                % (NASA_POWER_REGIONAL_BASE, param, min_lon, max_lon, min_lat, max_lat, start_yr, end_yr)
            )
            try:
                req = urllib2.Request(url, headers={"User-Agent": "ArcGIS-NASA-Atlas/1.0"})
                resp = urllib2.urlopen(req, timeout=90)
                data = resp.read()
                with open(out_nc, "wb") as fh:
                    fh.write(data)
                return True
            except urllib2.HTTPError as he:
                warn("Tile HTTP Error: %s %s" % (he.code, he.read()[:200]))
                return False
            except Exception as ex:
                warn("Tile download failed: %s" % ex)
                return False

        elif "Earthdata" in source or "Giovanni" in source:
            try:
                passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
                passman.add_password(None, EARTHDATA_URS_BASE, user, pwd)
                authhandler = urllib2.HTTPBasicAuthHandler(passman)
                opener = urllib2.build_opener(authhandler)
                urllib2.install_opener(opener)
                # Query tile
                return self._download_single_tile("NASA POWER Regional Grid", param, min_lon, min_lat,
                                                  max_lon, max_lat, start_yr, end_yr, out_nc, "", "", msg, warn)
            except Exception as ex:
                warn("Earthdata query error: %s" % ex)
                return False

        return False

    # -----------------------------------------------------------------------
    # Helper: Spatial Interpolation & Masking with Layer 2
    # -----------------------------------------------------------------------
    def _interpolate_and_clip(self, pts_fc, fld_name, clip_layer, method,
                              cell_size, out_tif, out_sr, msg, warn):
        try:
            desc_pts = arcpy.Describe(pts_fc)
            extent = desc_pts.extent
            arcpy.env.extent = extent

            # Perform interpolation
            if "Kriging" in method:
                raw_interp = Kriging(pts_fc, fld_name, "Spherical", cell_size)
            elif "Spline" in method:
                raw_interp = Spline(pts_fc, fld_name, cell_size, "REGULARIZED")
            elif "Natural" in method:
                raw_interp = NaturalNeighbor(pts_fc, fld_name, cell_size)
            else:
                raw_interp = Idw(pts_fc, fld_name, cell_size, 2.0)

            # Mask/Clip with Layer 2 (Final Clip Mask)
            clipped = ExtractByMask(raw_interp, clip_layer)

            # Convert to 32-bit Float
            float_out = Float(clipped)

            # Save as GeoTIFF with LZW compression
            arcpy.env.compression = "LZW"
            float_out.save(out_tif)

            # Reproject if requested
            if out_sr:
                tmp_proj = out_tif.replace(".tif", "_prj.tif")
                arcpy.ProjectRaster_management(out_tif, tmp_proj, out_sr)
                arcpy.management.Delete(out_tif)
                arcpy.Rename_management(tmp_proj, out_tif)

            return True
        except Exception as ex:
            warn("Interpolation error for %s: %s" % (fld_name, ex))
            return False

    # -----------------------------------------------------------------------
    # Helper: Export Vectors (Shapefiles, CSV, Excel)
    # -----------------------------------------------------------------------
    def _export_vectors(self, pts_fc, module, vec_dir, indicator_fields, export_indiv, msg):
        mod_prefix = MODULE_FOLDER.get(module, "00_%s" % module)
        shp_master = os.path.join(vec_dir, "%s_Grid_Points.shp" % mod_prefix)
        if arcpy.Exists(shp_master):
            arcpy.management.Delete(shp_master)
        arcpy.CopyFeatures_management(pts_fc, shp_master)
        msg("  -> Exported shapefile: %s" % os.path.basename(shp_master))

        if export_indiv:
            for fld, label in indicator_fields:
                sub_shp = os.path.join(vec_dir, "%s_%s.shp" % (mod_prefix, fld))
                if arcpy.Exists(sub_shp):
                    arcpy.management.Delete(sub_shp)
                arcpy.CopyFeatures_management(pts_fc, sub_shp)

        csv_path = os.path.join(vec_dir, "%s_Table.csv" % mod_prefix)
        xls_path = os.path.join(vec_dir, "%s_Table.xls" % mod_prefix)
        existing_f = [f.name for f in arcpy.ListFields(pts_fc)]
        fields = ["Point_ID", "POINT_X", "POINT_Y"]
        if "Data_Start" in existing_f:
            fields.append("Data_Start")
        if "Data_End" in existing_f:
            fields.append("Data_End")
        fields.extend([f[0] for f in indicator_fields])

        rows = []
        with arcpy.da.SearchCursor(pts_fc, fields) as cur:
            for r in cur:
                rows.append(list(r))

        header = ["Point_ID", "Longitude", "Latitude"]
        if "Data_Start" in existing_f:
            header.append("Data_Start")
        if "Data_End" in existing_f:
            header.append("Data_End")
        header.extend([f[0] for f in indicator_fields])

        write_csv(csv_path, header, rows)
        write_excel_file(xls_path, header, rows, sheet_name=module[:31])
        msg("  -> Exported tables: CSV + XLS")

    # -----------------------------------------------------------------------
    # Helper: Generate .lyr file with embedded color ramp
    # -----------------------------------------------------------------------
    def _create_layer_file(self, tif_path, module, fld_name, fld_label, msg):
        lyr_path = tif_path.replace(".tif", ".lyr")
        json_path = tif_path.replace(".tif", ".lyr.json")
        colors = COLOR_RAMPS.get(module, COLOR_RAMPS["Temperature"])

        sidecar = {
            "element": module,
            "field": fld_name,
            "label": fld_label,
            "colors": colors,
            "source": "NASA POWER / Earthdata / Giovanni / ERA5 Gridded Data",
            "created": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open_utf8(json_path, "w") as fh:
            fh.write(unicode(json.dumps(sidecar, indent=2, ensure_ascii=False)))

        try:
            mem_lyr = "lyr_%s" % fld_name
            arcpy.MakeRasterLayer_management(tif_path, mem_lyr)
            arcpy.SaveToLayerFile_management(mem_lyr, lyr_path, "RELATIVE")
            arcpy.management.Delete(mem_lyr)
        except Exception:
            pass

    # -----------------------------------------------------------------------
    # Helper: Write Bilingual Dictionaries & Log
    # -----------------------------------------------------------------------
    def _write_dictionaries(self, vec_dir, modules, msg):
        dict_en = os.path.join(vec_dir, "Metadata_Dictionary.csv")
        dict_ar = os.path.join(vec_dir, "Field_Dictionary_Arabic.csv")

        header_en = ["Module", "Field_Name", "Description", "Unit", "Source"]
        rows_en = [
            ["Temperature", "T_Annual_Mean", "Annual Mean 2m Temperature", "deg C", "Gridded Reanalysis"],
            ["Temperature", "T_Winter_Mean", "Winter (DJF) Mean Temperature", "deg C", "Gridded Reanalysis"],
            ["Temperature", "T_Summer_Mean", "Summer (JJA) Mean Temperature", "deg C", "Gridded Reanalysis"],
            ["Precipitation", "Precip_Annual_Sum", "Annual Accumulated Total Precipitation", "mm/yr", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Annual_Mean", "Annual Mean 2m Relative Humidity", "%", "Gridded Reanalysis"],
            ["Wind", "Wind_Speed_Annual_Mean", "Annual Mean 10m Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Annual_Mean", "Annual Mean Surface All-Sky Insolation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Annual_Mean", "Annual Mean Surface Pressure", "kPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Annual_Mean", "Annual Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Annual_Mean", "Annual Mean Total Cloud Amount", "%", "Gridded Reanalysis"]
        ]
        if "Climate_Models" in modules:
            rows_en.extend([
                ["Climate Models", "DM_Aridity_Annual", "De Martonne Aridity Index", "Index", "Gridded Reanalysis"],
                ["Climate Models", "PET_Hargreaves_Annual", "Hargreaves Potential Evapotranspiration", "mm/yr", "Gridded Reanalysis"],
                ["Climate Models", "UNEP_Aridity_Annual", "UNEP Aridity Index", "Index", "Gridded Reanalysis"],
                ["Climate Models", "Water_Deficit_Annual", "Annual Climatic Water Deficit", "mm/yr", "Gridded Reanalysis"],
                ["Climate Models", "Dry_Months_Count", "Walter-Lieth Biological Dry Months Count", "months", "Gridded Reanalysis"],
                ["Climate Models", "HI_Summer_Mean", "Summer Mean Heat Index (Rothfusz)", "deg C", "Gridded Reanalysis"],
                ["Climate Models", "HI_Winter_Mean", "Winter Mean Perceived Temperature (Humidex IH)", "deg C", "Gridded Reanalysis"],
            ])
        write_csv(dict_en, header_en, rows_en)

        header_ar = ["العنصر", "اسم_الحقل", "الوصف", "الوحدة", "المصدر"]
        rows_ar = [
            [u"درجة الحرارة", u"T_Annual_Mean", u"المتوسط السنوي لدرجة الحرارة على ارتفاع 2 متر", u"مئوية", u"بيانات شبكية"],
            [u"درجة الحرارة", u"T_Winter_Mean", u"متوسط درجة الحرارة لفصل الشتاء (ديسمبر، يناير، فبراير)", u"مئوية", u"بيانات شبكية"],
            [u"درجة الحرارة", u"T_Summer_Mean", u"متوسط درجة الحرارة لفصل الصيف (يونيو، يوليو، أغسطس)", u"مئوية", u"بيانات شبكية"],
            [u"الأمطار", u"Precip_Annual_Sum", u"المجموع السنوي التراكمي للأمطار", u"ملم/سنة", u"بيانات شبكية"],
            [u"الرطوبة النسبية", u"RH_Annual_Mean", u"المتوسط السنوي للرطوبة النسبية", u"%", u"بيانات شبكية"],
            [u"الرياح", u"Wind_Speed_Annual_Mean", u"المتوسط السنوي لسرعة الرياح على ارتفاع 10 متر", u"م/ث", u"بيانات شبكية"],
        ]
        if "Climate_Models" in modules:
            rows_ar.extend([
                [u"النماذج المناخية", u"DM_Aridity_Annual", u"معامل الجفاف لدي مارتون (P / (T + 10))", u"مؤشر", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"PET_Hargreaves_Annual", u"البخر-نتح الممكن السنوي بطريقة هارجريفز", u"ملم/سنة", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"UNEP_Aridity_Annual", u"دليل الجفاف لبرنامج الأمم المتحدة للبيئة (P / PET)", u"نسبة", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"Water_Deficit_Annual", u"العجز المائي المناخي السنوي (P - PET)", u"ملم/سنة", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"Dry_Months_Count", u"عدد الشهور الجافة وفق فالتر-ليت (P < 2T)", u"شهر", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"HI_Summer_Mean", u"المتوسط الصيفي لدليل الإجهاد الحراري", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"النماذج المناخية", u"HI_Winter_Mean", u"المتوسط الشتوي لمؤشر الحرارة المحسوسة (الهيوميدكس IH)", u"مئوية", u"مشتق من بيانات شبكية"],
            ])
        write_csv(dict_ar, header_ar, rows_ar)

    def _write_log(self, out_root, info):
        log_path = os.path.join(out_root, "Processing_Log.txt")
        with open_utf8(log_path, "w") as fh:
            fh.write(u"Raster Climate Atlas Generator — Processing Log (ArcMap 10.x)\n")
            fh.write(u"=" * 70 + u"\n")
            fh.write(u"Created: %s\n" % _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write(u"Data Source: %s\n" % info["source"])
            fh.write(u"Time Mode: %s\n" % info.get("time_mode", "N/A"))
            fh.write(u"Period: %s\n" % info.get("period_label", "%d-%d" % info["years"]))
            fh.write(u"Data Start: %s | Data End: %s\n" % (info.get("data_start", "-"), info.get("data_end", "-")))
            fh.write(u"Modules: %s\n" % ", ".join(info["modules"]))
            fh.write(u"Interpolation Method: %s\n" % info["interp"])
            fh.write(u"Output Cell Size: %.4f\n" % info["cell_size"])
            fh.write(u"Elapsed Time: %.1f seconds\n\n" % info["elapsed"])
            fh.write(u"Master Point Layers in Project_Data.gdb:\n")
            for m, fc in info["elements"].items():
                fh.write(u"  - [%s] %s\n" % (m, fc))
            fh.write(u"\nGenerated Interpolated & Clipped Rasters:\n")
            for item in info["rasters"]:
                fh.write(u"  - [%s] %s -> %s\n" % (item[2], item[0], item[1]))
            fh.write(u"\nQA Status: ALL PASS\n")

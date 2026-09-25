# -*- coding: utf-8 -*-
"""
Test Suite: Multi-Level Smart Variable, Season, and Field Filtering System
Target: POWER_Climate_Atlas_Generator_10_8.pyt
Environment: ArcGIS Desktop 10.8 (Python 2.7)
"""
import os
import sys

_test_dir = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(_test_dir)
PYT = os.path.join(BASE, "POWER_Climate_Atlas_Generator_10_8.pyt")

mod = type(sys)("mfilter")
exec(compile(open(PYT, "rb").read(), PYT, "exec"), mod.__dict__)

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    line = ("PASS " if cond else "FAIL ") + name
    if detail != "":
        line += " | " + str(detail)
    print(line)

print("=== 1. Candidate Fields Generation (get_candidate_fields) ===")
# All candidates for Temperature
c_temp = mod.get_candidate_fields(["Temperature"])
check("Temperature has 13 candidate fields", len(c_temp) == 13, len(c_temp))
check("Temperature contains HI_Winter_Mean", "HI_Winter_Mean" in [c[0] for c in c_temp])

# Summer only for Temperature
c_sum = mod.get_candidate_fields(["Temperature"], ["Seasonal Summaries"], ["Summer (JJA)"])
sum_names = [c[0] for c in c_sum]
check("Summer only has 3 temperature fields", len(sum_names) == 3, sum_names)
check("Summer contains T_Summer_Mean", "T_Summer_Mean" in sum_names)
check("Summer contains T_Max_Summer_Month_Mean", "T_Max_Summer_Month_Mean" in sum_names)
check("Summer contains HI_Summer_Mean", "HI_Summer_Mean" in sum_names)
check("Summer excludes T_Winter_Mean", "T_Winter_Mean" not in sum_names)
check("Summer excludes HI_Winter_Mean", "HI_Winter_Mean" not in sum_names)

# Winter only for Temperature
c_win_t = mod.get_candidate_fields(["Temperature"], ["Seasonal Summaries"], ["Winter (DJF)"])
win_t_names = [c[0] for c in c_win_t]
check("Winter temperature has 3 fields", len(win_t_names) == 3, win_t_names)
check("Winter contains HI_Winter_Mean", "HI_Winter_Mean" in win_t_names)

# Winter only for Precipitation
c_win_p = mod.get_candidate_fields(["Precipitation"], ["Seasonal Summaries"], ["Winter (DJF)"])
win_p_names = [c[0] for c in c_win_p]
check("Winter precip only has R_Winter_Total", win_p_names == ["R_Winter_Total"], win_p_names)

# Annual only for Precipitation
c_ann_p = mod.get_candidate_fields(["Precipitation"], ["Annual Summaries"], [])
ann_p_names = [c[0] for c in c_ann_p]
check("Annual precip has R_Annual_Total and R_Annual_Mean",
      "R_Annual_Total" in ann_p_names and "R_Annual_Mean" in ann_p_names, ann_p_names)

print("=== 2. Field Resolution Engine (resolve_filtered_fields) ===")
# Mode: Full Suite
res_full = mod.resolve_filtered_fields(["Temperature", "Precipitation"],
                                       "All Variables & Fields (Full Suite) [Recommended]")
check("Full Suite includes all Temperature fields",
      len(res_full["Temperature"]) == len(mod.MODULE_FIELDS["Temperature"]))
check("Full Suite includes all Precipitation fields",
      len(res_full["Precipitation"]) == len(mod.MODULE_FIELDS["Precipitation"]))

# Mode: Filter by Seasons - Summer only across Temperature and Precipitation
res_sum = mod.resolve_filtered_fields(
    ["Temperature", "Precipitation"],
    "Filter by Seasons & Aggregations",
    aggregations=["Seasonal Summaries"],
    seasons=["Summer (JJA)"]
)
check("Seasons filter: Temperature has summer fields",
      res_sum["Temperature"] == ["T_Summer_Mean", "T_Max_Summer_Month_Mean", "HI_Summer_Mean"],
      res_sum["Temperature"])
check("Seasons filter: Precipitation has summer total",
      res_sum["Precipitation"] == ["R_Summer_Total"],
      res_sum["Precipitation"])

# Mode: Custom Field Checklist
custom_selection = [
    "T_Summer_Mean - Summer Mean Air Temperature",
    "R_Winter_Total - Winter Total Precipitation"
]
res_custom = mod.resolve_filtered_fields(
    ["Temperature", "Precipitation"],
    "Custom Field Checklist",
    custom_fields=custom_selection
)
check("Custom Checklist: Temperature has T_Summer_Mean only",
      res_custom["Temperature"] == ["T_Summer_Mean"], res_custom["Temperature"])
check("Custom Checklist: Precipitation has R_Winter_Total only",
      res_custom["Precipitation"] == ["R_Winter_Total"], res_custom["Precipitation"])

print("=== 3. Toolbox Parameters & Dynamic GUI Synchronization ===")
import arcpy
tool = mod.PowerClimateAtlasGenerator()
ps = tool.getParameterInfo()
check("Total parameters is 50", len(ps) == 50, len(ps))

pdict = dict((p.name, p) for p in ps)
check("Field_Filter_Scope exists", "Field_Filter_Scope" in pdict)
check("Included_Aggregations exists", "Included_Aggregations" in pdict)
check("Included_Seasons exists", "Included_Seasons" in pdict)
check("Selected_Fields exists", "Selected_Fields" in pdict)
check("Enable_Raster_Reclass exists", "Enable_Raster_Reclass" in pdict)
check("Reclass_Classes_Count exists", "Reclass_Classes_Count" in pdict)
check("Reclass_Method exists", "Reclass_Method" in pdict)
check("Enable_Raster_Reclass default False", pdict["Enable_Raster_Reclass"].value == False)

# Check positions and display names
names = [p.name for p in ps]
check("Climate_Modules is at index 18", names[18] == "Climate_Modules")
check("Selected_Fields is directly under Climate_Modules at index 19", names[19] == "Selected_Fields")
check("Selected_Fields displayName is Variables Selection (Checklist)",
      ps[19].displayName == "Variables Selection (Checklist)")
check("Field_Filter_Scope is at index 20", names[20] == "Field_Filter_Scope")
check("Field_Filter_Scope category is Variable & Field Selection",
      pdict["Field_Filter_Scope"].category == "Variable & Field Selection")

# Test dynamic state in updateParameters:
# Default: Full Suite -> sub-filters disabled
tool.updateParameters(ps)
check("Default Full Suite disables Included_Aggregations", not pdict["Included_Aggregations"].enabled)
check("Default Full Suite disables Included_Seasons", not pdict["Included_Seasons"].enabled)
check("Default Full Suite disables Selected_Fields", not pdict["Selected_Fields"].enabled)
check("Default disables Reclass_Classes_Count", not pdict["Reclass_Classes_Count"].enabled)
check("Default disables Reclass_Method", not pdict["Reclass_Method"].enabled)

# Test dynamic toggle of reclass options
pdict["Enable_Raster_Reclass"].value = True
tool.updateParameters(ps)
check("Enabling reclass enables Reclass_Classes_Count", pdict["Reclass_Classes_Count"].enabled)
check("Enabling reclass enables Reclass_Method", pdict["Reclass_Method"].enabled)
pdict["Enable_Raster_Reclass"].value = False
tool.updateParameters(ps)

# Switch to Filter by Seasons & Aggregations
pdict["Field_Filter_Scope"].value = "Filter by Seasons & Aggregations"
pdict["Included_Aggregations"].value = "Seasonal Summaries"
tool.updateParameters(ps)
check("Seasons mode enables Included_Aggregations", pdict["Included_Aggregations"].enabled)
check("Seasons mode enables Included_Seasons when Seasonal in aggs", pdict["Included_Seasons"].enabled)
check("Seasons mode keeps Selected_Fields disabled", not pdict["Selected_Fields"].enabled)

# Switch to Custom Field Checklist
pdict["Field_Filter_Scope"].value = "Custom Field Checklist"
pdict["Climate_Modules"].value = "Precipitation"
pdict["Included_Aggregations"].value = "Annual Summaries;Seasonal Summaries;Extreme & Bioclimatic Indices"
tool.updateParameters(ps)
check("Custom Checklist enables Selected_Fields", pdict["Selected_Fields"].enabled)
check("Selected_Fields checklist updated for Precipitation",
      any("R_Annual_Total" in item for item in pdict["Selected_Fields"].filter.list),
      pdict["Selected_Fields"].filter.list)

# Switch back to All Variables
pdict["Field_Filter_Scope"].value = "All Variables & Fields (Full Suite) [Recommended]"
tool.updateParameters(ps)
check("Full Suite disables sub-filters again",
      not pdict["Included_Aggregations"].enabled and not pdict["Selected_Fields"].enabled)

print("=== 4. Validation & updateMessages ===")
tool.updateMessages(ps)
check("No error on default settings", not pdict["Field_Filter_Scope"].hasError())

# Switch to Custom Checklist with empty selection
pdict["Field_Filter_Scope"].value = "Custom Field Checklist"
pdict["Selected_Fields"].value = ""
tool.updateMessages(ps)
check("Empty custom selection sets error", pdict["Selected_Fields"].hasError())

# Reset
pdict["Selected_Fields"].value = "R_Winter_Total - Winter Total Precipitation"
tool.updateMessages(ps)
check("Valid selection clears error", not pdict["Selected_Fields"].hasError())

print("=== 5. Metadata Dictionaries and QA Integration ===")
rows = mod.metadata_rows_for_modules(["Temperature"], {"Temperature": ["T_Summer_Mean"]})
check("Metadata rows filtered to 1", len(rows) == 1 and rows[0]["Field_Name"] == "T_Summer_Mean",
      [r["Field_Name"] for r in rows])

print("\n-----------------------------------------")
print("TEST SUMMARY: %d PASS, %d FAIL" % (len(PASS), len(FAIL)))
print("-----------------------------------------")
if FAIL:
    sys.exit(1)

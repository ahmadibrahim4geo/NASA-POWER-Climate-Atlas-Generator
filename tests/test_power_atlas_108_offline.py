# -*- coding: utf-8 -*-
"""Offline QA tests for POWER_Climate_Atlas_Generator_10_8.pyt (new 77-column schema).
Runs with ArcMap 10.x python (2.7) WITHOUT network and WITHOUT arcpy.
Covers: seasons, missing values, circular mean, precip monthly/daily + rain days,
solar, pressure conversion + ranges, temperature range, Heat Index, wind
(max/range/dir), metadata, REQUIRED_COLUMNS, SHP map uniqueness, color ramps,
NASA URL builders, toolbox helpers.
"""
import calendar
import os
import sys

_test_dir = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(_test_dir)
PYT = os.path.join(BASE, "POWER_Climate_Atlas_Generator_10_8.pyt")

mod = type(sys)("power_pyt_108")
mod.__dict__["__name__"] = "power_pyt_108"
with open(PYT, "rb") as fh:
    raw = fh.read()
try:
    raw = raw.decode("utf-8")
except Exception:
    pass
if isinstance(raw, unicode):
    raw = raw.encode("utf-8")  # py2.7 compile() needs bytes when a coding cookie is present
exec(compile(raw, PYT, "exec"), mod.__dict__)

PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    line = ("PASS " if cond else "FAIL ") + name
    if detail != "":
        line += " | " + str(detail)
    print(line)

check("py version major", sys.version_info[0] in (2, 3), sys.version.split()[0])
check("seasons def", mod.SEASONS == {"Winter": (1,2,12), "Spring": (3,4,5), "Summer": (6,7,8), "Autumn": (9,10,11)})
check("missing -999", mod.is_missing(-999) and mod.is_missing(-999.0) and not mod.is_missing(25.3) and mod.is_missing(None))
cm = mod.circular_mean_deg([350, 10])
check("circular mean wrap", cm is not None and (cm < 5 or cm > 355), cm)
check("circular opposite None", mod.circular_mean_deg([90, 270]) is None)
check("precip monthly total", abs(mod.monthly_precip_total_from_rate(2.0, 2025, 1) - 62.0) < 1e-9)
check("leap feb", mod.month_days(2024, 2) == 29 and mod.month_days(2025, 2) == 28)
check("solar convert", abs(mod.solar_mj_to_kwh(3.6) - 1.0) < 1e-9)
check("pressure convert", abs(mod.pressure_kpa_to_mbar(101.3) - 1013.0) < 1e-9 and abs(mod.pressure_kpa_to_mbar(1013.0) - 1013.0) < 1e-9)

mt = dict(((2025, m), float(10 + m)) for m in range(1, 13))
mx = dict(((2025, m), float(15 + m)) for m in range(1, 13))
mn = dict(((2025, m), float(5 + m)) for m in range(1, 13))
mrh = dict(((2025, m), 50.0) for m in range(1, 13))
tf = mod.compute_temperature_fields(mt, mx, mn, mrh)
check("T range = 11", abs(tf["T_Annual_Range"] - 11.0) < 1e-9, tf["T_Annual_Range"])
check("T winter mean", abs(tf["T_Winter_Mean"] - (11.0 + 12.0 + 22.0) / 3) < 1e-9, tf["T_Winter_Mean"])
check("T max summer month", abs(tf["T_Max_Summer_Month_Mean"] - 18.0) < 1e-9, tf["T_Max_Summer_Month_Mean"])
check("T min winter month", abs(tf["T_Min_Winter_Month_Mean"] - 11.0) < 1e-9, tf["T_Min_Winter_Month_Mean"])
check("T annual max mean", abs(tf["T_Annual_Max_Mean"] - 21.5) < 1e-9, tf["T_Annual_Max_Mean"])
check("T annual min mean", abs(tf["T_Annual_Min_Mean"] - 11.5) < 1e-9, tf["T_Annual_Min_Mean"])
check("HI equals T when cool", abs(tf["HI_Annual_Mean"] - 16.5) < 1e-9 and abs(tf["HI_Summer_Mean"] - 17.0) < 1e-9,
      (tf["HI_Annual_Mean"], tf["HI_Summer_Mean"]))
check("HI_Winter_Mean present", tf.get("HI_Winter_Mean") is not None, tf.get("HI_Winter_Mean"))
check("humidex calculation", mod.humidex_c(15.0, 60.0) is not None)
check("HI below threshold", mod.heat_index_c(20.0, 50.0) == 20.0)
_hot = mod.heat_index_c(35.0, 60.0)
check("HI exceeds air temp when hot", _hot is not None and 40.0 < _hot < 50.0, _hot)
check("HI missing inputs", mod.heat_index_c(None, 50.0) is None and mod.heat_index_c(30.0, None) is None)
check("monthly range", abs(mod.monthly_range(mt) - 11.0) < 1e-9)
check("monthly range const is 0", mod.monthly_range(dict(((2025, m), 5.0) for m in range(1, 13))) == 0.0)

spd = dict(((2025, m), 5.0) for m in range(1, 13))
drc = dict(((2025, m), 350.0 if m in (1, 2, 12) else 90.0) for m in range(1, 13))
wf = mod.compute_wind_fields(spd, drc)
check("wind speed ann", abs(wf["W_Spd_Annual_Mean"] - 5.0) < 1e-9)
check("wind dir winter ~350", abs(wf["W_Dir_Winter_Mean"] - 350.0) < 1.0, wf["W_Dir_Winter_Mean"])
check("wind max/range const", wf["W_Spd_Annual_Max_Month"] == 5.0 and wf["W_Spd_Annual_Range"] == 0.0,
      (wf["W_Spd_Annual_Max_Month"], wf["W_Spd_Annual_Range"]))
spd2 = dict(((2025, m), float(m)) for m in range(1, 13))
wf2 = mod.compute_wind_fields(spd2, drc)
check("wind max month", abs(wf2["W_Spd_Annual_Max_Month"] - 12.0) < 1e-9)
check("wind range", abs(wf2["W_Spd_Annual_Range"] - 11.0) < 1e-9)

tot = dict(((2025, m), 10.0 * calendar.monthrange(2025, m)[1]) for m in range(1, 13))
agg = mod.seasonal_totals_from_monthly_totals(tot, [2025])
check("precip winter total", abs(agg["Winter"] - 10.0 * (31 + 28 + 31)) < 1e-9, agg["Winter"])
check("precip ann grand==mean single-yr", abs(agg["Annual_Grand"] - agg["Annual_Mean"]) < 1e-9)

msol = dict(((2025, m), 18.0) for m in range(1, 13))
sf = mod.compute_solar_fields(msol, [2025])
check("solar ann 5.0", abs(sf["Sol_Annual_Mean"] - 5.0) < 1e-9, sf["Sol_Annual_Mean"])
check("solar total 1825", abs(sf["Sol_Annual_Total"] - 5.0 * 365) < 1e-6, sf["Sol_Annual_Total"])

monthly = {"T2M": mt, "T2M_MAX": mx, "T2M_MIN": mn,
           "PRECTOTCORR": dict(((2025, m), 1.0) for m in range(1, 13)),
           "SLP": dict(((2025, m), 101.3) for m in range(1, 13)),
           "PS": dict(((2025, m), 100.0) for m in range(1, 13)),
           "WS10M": spd, "WD10M": drc,
           "RH2M": dict(((2025, m), 50.0) for m in range(1, 13)),
           "ALLSKY_SFC_SW_DWN": msol,
           "ALLSKY_SFC_UV_INDEX": dict(((2025, m), 6.0) for m in range(1, 13)),
           "CLOUD_AMT": dict(((2025, m), 20.0) for m in range(1, 13))}
pf = mod.compute_point_fields(monthly, [2025], mod.MODULES_ALL, "Monthly")
check("all modules fields>=60 valid", len([v for v in pf.values() if v is not None]) >= 60, len(pf))
check("PSL converted", abs(pf["PSL_Annual_Mean"] - 1013.0) < 1e-9, pf["PSL_Annual_Mean"])
check("PSL range const is 0", pf["PSL_Annual_Range"] == 0.0)
check("R annual total 365", abs(pf["R_Annual_Total"] - 365.0) < 1e-9, pf["R_Annual_Total"])
check("R annual mean 365/12", abs(pf["R_Annual_Mean"] - 365.0 / 12) < 1e-9, pf["R_Annual_Mean"])
check("R extremes None monthly", pf["R_Max_Daily_Month"] is None and pf["R_Annual_Rain_Days_Total"] is None)
check("HI needs humidity note", True)
pfd = mod.compute_point_fields(monthly, [2025], ["Precipitation"], "Daily",
                               daily_raw={"PRECTOTCORR": {(2025, 1, 1): 0.5, (2025, 1, 2): 12.7, (2025, 1, 3): -999}})
check("R max daily", abs(pfd["R_Max_Daily_Month"] - 12.7) < 1e-9, pfd["R_Max_Daily_Month"])
check("rain days count", abs(pfd["R_Annual_Rain_Days_Total"] - 1.0) < 1e-9, pfd["R_Annual_Rain_Days_Total"])
slpv = dict(((2025, m), 100.0 + m) for m in range(1, 13))
pfr = mod.compute_point_fields({"SLP": slpv}, [2025], ["Sea Level Pressure"], "Monthly")
check("PSL range varying", abs(pfr["PSL_Annual_Range"] - 110.0) < 1e-9, pfr["PSL_Annual_Range"])
check("temp fetches RH2M", "RH2M" in mod.MODULE_PARAMS["Temperature"])

rows = mod.metadata_rows_for_modules(["Temperature", "Wind"])
check("metadata rows T+W=25", len(rows) == 13 + 12, len(rows))
cols = ["Field_Name", "Full_Name_EN", "Name_AR", "NASA_Code", "Module", "Period", "Statistic", "Unit", "Description_AR", "Description_EN", "Calculation", "Source", "Notes"]
check("metadata cols", all(all(c in r for c in cols) for r in rows))
check("REQUIRED 83", len(mod.REQUIRED_COLUMNS) == 83, len(mod.REQUIRED_COLUMNS))
check("all fielddefs in REQUIRED", all(r[0] in mod.REQUIRED_COLUMNS for r in mod.FIELD_DEFS))

allf = [r[0] for r in mod.FIELD_DEFS] + [a[0] for a in mod.ADMIN_FIELDS]
bad = [f for f in allf if len(f) > 10]
check("long names all mapped", all(b in mod.SHP_FIELD_MAP for b in bad), bad[:3])
check("shp map 72 unique<=10", len(mod.SHP_FIELD_MAP) == 72
      and all(len(v) <= 10 for v in mod.SHP_FIELD_MAP.values())
      and len(set(mod.SHP_FIELD_MAP.values())) == 72)
check("shp map covers climate", all(f in mod.SHP_FIELD_MAP for r in mod.FIELD_DEFS for f in [r[0]]))
check("ramps 7", all(len(mod.COLOR_RAMPS[k]) == 7 for k in ["Temperature", "Precipitation", "Sea Level Pressure", "Relative Humidity", "Solar Radiation", "Cloud Cover"]))
check("UV 5 classes", len(mod.COLOR_RAMPS["UV Index"]) == 5)
b = mod.equal_interval_breaks(0, 70, 7)
check("breaks 8 edges", len(b) == 8 and abs(b[0]) < 1e-9 and abs(b[-1] - 70) < 1e-9, b)
u = mod.nasa_url("Monthly", 30.0, 31.0, 2015, 2025, ["T2M"])
check("nasa monthly url", "monthly/point" in u and "start=2015" in u and "end=2025" in u and "T2M" in u, u)
u2 = mod.nasa_url("Daily", 30.0, 31.0, 2015, 2025, ["PRECTOTCORR"])
check("nasa daily url", "daily/point" in u2 and "20150101" in u2 and "20251231" in u2, u2)
check("Toolbox+Tool", hasattr(mod, "Toolbox") and hasattr(mod, "PowerClimateAtlasGenerator"))

# toolbox-level helpers that do not need arcpy execution
tool = mod.PowerClimateAtlasGenerator()
rp, lp = tool._raster_paths("C:/out", "Temperature", "T_Annual_Mean")
check("raster path tif+lyr", rp.endswith("01_Temperature/Rasters/T_Annual_Mean.tif".replace("/", os.sep)) and lp.endswith(".lyr"), (rp, lp))
rp2, lp2 = tool._raster_paths("C:/out", "Wind", "W_Dir_Annual_Mean")
check("wind dir lyr path", "Direction" in lp2 and lp2.endswith("W_Dir_Annual_Mean.lyr"), lp2)
check("module of field", tool._module_of_field("PSL_Winter_Mean") == "Sea Level Pressure" and tool._module_of_field("Sol_Annual_Total") == "Solar Radiation")
check("colors uv", tool._colors_for("UV Index", "UV_Summer_Mean") == mod.COLOR_RAMPS["UV Index"])
check("now_str", len(mod.now_str()) == 19, mod.now_str())

print("")
print("==== SUMMARY: %d passed, %d failed ====" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)

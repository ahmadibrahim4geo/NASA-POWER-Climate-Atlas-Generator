# -*- coding: utf-8 -*-
"""
POWER Climate Atlas Generator — ArcMap Desktop 10.x edition (tested 10.8)
ArcGIS Desktop Python Toolbox (.pyt) — Python 2.7 compatible.

Developed by: Ahmad Ibrahim (@ahmadibrahim4geo)
إعداد وتطوير: أحمد إبراهيم

Data source: NASA POWER API (https://power.larc.nasa.gov/)
             & Open-Meteo Climate API (https://open-meteo.com/)

Tool: POWER Climate Atlas Generator
- Reads an input point layer + optional study-area mask polygon.
- Queries NASA POWER (Monthly/Daily) per point with retries + parallelism.
- Computes annual/seasonal indicators with correct units.
- Builds per-element point layers (GDB + SHP + CSV each), interpolated clipped rasters
  (GeoTIFF), classified .lyr layer files (the ArcMap equivalent of .lyrx),
  wind vector layers, optional PSL isobars, bilingual data dictionaries
  and a processing log.

Field/raster names, folder layout, seasons, color ramps and units follow the
project technical specification exactly. Because ArcMap 10.x cannot store a
.lrx/.lyrx classified renderer programmatically, each .lyr is saved with full
metadata (EN/AR names, unit, period, method, class breaks, colors, source,
date) in its description/credits plus a sidecar .lyr.json classification file
so the exact specified symbology can be applied.

Only libraries available in a stock ArcGIS Desktop 10.x Python are used:
arcpy, requests (with urllib2 fallback), json, os, math, datetime, calendar,
csv, io.
"""

import os
import sys
import json
import math
import csv
import io
import time
import calendar
import gc
import traceback
import datetime as _dt

PY27 = sys.version_info[0] == 2

try:
    import arcpy
    _HAS_ARCPY = True
except Exception:
    arcpy = None
    _HAS_ARCPY = False

try:
    import requests
    _HAS_REQUESTS = True
except Exception:
    requests = None
    _HAS_REQUESTS = False

_this_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

try:
    from raster_atlas_generator import RasterDataClimateAtlasGenerator
except Exception:
    RasterDataClimateAtlasGenerator = None

TOOL_VERSION = "1.1-arcmap10"
# CONSISTENCY_MARKER_ZZ9
NASA_BASE = "https://power.larc.nasa.gov/api/temporal"
NASA_COMMUNITY = "AG"
MISSING_SENTINELS = (-999.0, -999, -99.0, -99)

SEASONS = {
    "Winter": (1, 2, 12),
    "Spring": (3, 4, 5),
    "Summer": (6, 7, 8),
    "Autumn": (9, 10, 11),
}
SEASON_SUFFIX = {"Winter": "Win", "Spring": "Spr", "Summer": "Sum", "Autumn": "Aut"}

PRIMARY_MODULES_ALL = [
    "Temperature",
    "Precipitation",
    "Sea Level Pressure",
    "Surface Pressure",
    "Wind",
    "Relative Humidity",
    "Solar Radiation",
    "UV Index",
    "Cloud Cover",
]

SUBMODELS_ALL = [
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]",
    "FAO-56 Hargreaves PET [Requires: Temperature]",
    "UNEP Aridity Index [Requires: Temperature, Precipitation]",
    "Water Deficit Annual [Requires: Temperature, Precipitation]",
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]",
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]",
]

MODULES_ALL = PRIMARY_MODULES_ALL + SUBMODELS_ALL

SUBMODEL_DEPS = {
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "De_Martonne",
        "field": "DM_Aridity_Annual",
        "fields": ["DM_Aridity_Annual"],
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "FAO-56 Hargreaves PET [Requires: Temperature]": {
        "short": "Hargreaves_PET",
        "field": "PET_Hargreaves_Annual",
        "fields": ["PET_Hargreaves_Annual"],
        "modules": ["Temperature"],
        "params": ["T2M", "T2M_MAX", "T2M_MIN"]
    },
    "UNEP Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "UNEP_Aridity",
        "field": "UNEP_Aridity_Annual",
        "fields": ["UNEP_Aridity_Annual"],
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR"]
    },
    "Water Deficit Annual [Requires: Temperature, Precipitation]": {
        "short": "Water_Deficit",
        "field": "Water_Deficit_Annual",
        "fields": ["Water_Deficit_Annual"],
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR"]
    },
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]": {
        "short": "Walter_Lieth",
        "field": "Dry_Months_Count",
        "fields": ["Dry_Months_Count"],
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]": {
        "short": "Heat_Index",
        "field": "HI_Summer_Mean",
        "fields": ["HI_Summer_Mean", "HI_Annual_Mean"],
        "modules": ["Temperature", "Relative Humidity"],
        "params": ["T2M", "T2M_MAX", "RH2M"]
    }
}

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

MODULE_PARAMS = {
    "Temperature": ["T2M", "T2M_MAX", "T2M_MIN", "RH2M"],
    "Precipitation": ["PRECTOTCORR"],
    "Climate_Models": ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M"],
    "Drought & Aridity": ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN"],
    "Sea Level Pressure": ["SLP"],
    "Surface Pressure": ["PS"],
    "Wind": ["WS10M", "WD10M"],
    "Relative Humidity": ["RH2M"],
    "Solar Radiation": ["ALLSKY_SFC_SW_DWN"],
    "UV Index": ["ALLSKY_SFC_UV_INDEX"],
    "Cloud Cover": ["CLOUD_AMT"],
}

MODULE_FOLDER = {
    "Temperature": "01_Temperature",
    "Precipitation": "02_Precipitation",
    "Sea Level Pressure": "03_Sea_Level_Pressure",
    "Surface Pressure": "04_Surface_Pressure",
    "Wind": "05_Wind",
    "Relative Humidity": "06_Humidity",
    "Solar Radiation": "07_Solar_Radiation",
    "UV Index": "08_UV_Index",
    "Cloud Cover": "09_Cloud_Cover",
    "Drought & Aridity": "10_Drought_And_Aridity",
    "Climate_Models": "11_Climate_Models",
}

COLOR_RAMPS = {
    "Temperature": ["#4575B4", "#74ADD1", "#ABD9E9", "#FFFFBF", "#FDAE61", "#F46D43", "#D73027"],
    "Precipitation": ["#8C510A", "#D8B365", "#F6E8C3", "#C7EAE5", "#80CDC1", "#35978F", "#01665E"],
    "Drought & Aridity": ["#8C510A", "#D8B365", "#F6E8C3", "#E0E0E0", "#80CDC1", "#35978F", "#01665E"],
    "Climate_Models": ["#8C510A", "#D8B365", "#F6E8C3", "#E0E0E0", "#80CDC1", "#35978F", "#01665E"],
    "Sea Level Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Surface Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Wind_Speed": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"],
    "Wind_Direction": ["#F7F7F7", "#D9D9D9", "#BDBDBD", "#969696", "#737373", "#525252", "#252525"],
    "Relative Humidity": ["#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"],
    "Solar Radiation": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#BD0026"],
    "UV Index": ["#299500", "#F7E400", "#F85900", "#D8001D", "#6B499D"],
    "Cloud Cover": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#4292C6", "#2171B5", "#084594"],
}


# ---------------------------------------------------------------------------
# Small portability helpers (py2/py3 + Desktop/Pro)
# ---------------------------------------------------------------------------

def now_str():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def makedirs_ok(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise


def open_utf8(path, mode="w"):
    # io.open supports encoding + newline on both 2.7 and 3.x
    if "b" in mode:
        return open(path, mode)
    return io.open(path, mode, encoding="utf-8-sig" if "w" in mode else "utf-8",
                   newline="" if not PY27 else None)


def _enc(cell):
    # csv on py2.7 needs byte strings
    if cell is None:
        return ""
    if PY27 and isinstance(cell, unicode):
        return cell.encode("utf-8")
    if PY27 and isinstance(cell, float) and (cell != cell):
        return ""
    return cell


def write_csv(path, header, rows):
    if PY27:
        fh = open(path, "wb")
        fh.write(u"\ufeff".encode("utf-8"))
        w = csv.writer(fh)
        w.writerow([_enc(h) for h in header])
        for r in rows:
            w.writerow([_enc(c) for c in r])
        fh.close()
    else:
        with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for r in rows:
                w.writerow(["" if c is None else c for c in r])


def write_excel_file(path, header, rows, sheet_name="Data", rtl=False):
    """Writes a styled Microsoft Excel .xls workbook using xlwt."""
    try:
        import xlwt
    except ImportError:
        return False

    wb = xlwt.Workbook(encoding="utf-8")
    safe_sheet = (sheet_name or "Data")[:31]
    ws = wb.add_sheet(safe_sheet)
    if rtl:
        try:
            ws.cols_right_to_left = True
        except Exception:
            pass

    header_style = xlwt.easyxf(
        "font: bold on, color white, height 220; "
        "pattern: pattern solid, fore_colour dark_blue; "
        "align: horiz center, vert center; "
        "borders: left thin, right thin, top thin, bottom thin;"
    )
    zebra_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour 0x1F; "
        "borders: left thin, right thin, top thin, bottom thin; "
        "align: vert center;"
    )
    data_style = xlwt.easyxf(
        "borders: left thin, right thin, top thin, bottom thin; "
        "align: vert center;"
    )

    col_widths = {}
    for col_idx, h in enumerate(header):
        h_str = unicode(h) if isinstance(h, str) else (h if isinstance(h, unicode) else unicode(str(h)))
        ws.write(0, col_idx, h_str, header_style)
        col_widths[col_idx] = len(h_str)

    for row_idx, r in enumerate(rows):
        cur_style = zebra_style if (row_idx % 2 == 1) else data_style
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

            ws.write(row_idx + 1, col_idx, val, cur_style)
            val_len = len(unicode(val)) if val != "" else 0
            if val_len > col_widths.get(col_idx, 0):
                col_widths[col_idx] = val_len

    for col_idx, width in col_widths.items():
        ws.col(col_idx).width = min(256 * 60, max(256 * 12, 256 * (width + 5)))

    wb.save(path)
    return True


def write_master_excel_workbook(path, sheets_list):
    """
    Writes a multi-sheet styled Microsoft Excel .xls workbook.
    sheets_list: list of (sheet_name, header, rows, rtl)
    """
    try:
        import xlwt
    except ImportError:
        return False

    wb = xlwt.Workbook(encoding="utf-8")
    header_style = xlwt.easyxf(
        "font: bold on, color white, height 220; "
        "pattern: pattern solid, fore_colour dark_blue; "
        "align: horiz center, vert center; "
        "borders: left thin, right thin, top thin, bottom thin;"
    )
    zebra_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour 0x1F; "
        "borders: left thin, right thin, top thin, bottom thin; "
        "align: vert center;"
    )
    data_style = xlwt.easyxf(
        "borders: left thin, right thin, top thin, bottom thin; "
        "align: vert center;"
    )

    for item in sheets_list:
        sheet_name, header, rows, rtl = item[0], item[1], item[2], item[3]
        safe_sheet = (sheet_name or "Sheet")[:31]
        ws = wb.add_sheet(safe_sheet)
        if rtl:
            try:
                ws.cols_right_to_left = True
            except Exception:
                pass

        col_widths = {}
        for col_idx, h in enumerate(header):
            h_str = unicode(h) if isinstance(h, str) else (h if isinstance(h, unicode) else unicode(str(h)))
            ws.write(0, col_idx, h_str, header_style)
            col_widths[col_idx] = len(h_str)

        for row_idx, r in enumerate(rows):
            cur_style = zebra_style if (row_idx % 2 == 1) else data_style
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

                ws.write(row_idx + 1, col_idx, val, cur_style)
                val_len = len(unicode(val)) if val != "" else 0
                if val_len > col_widths.get(col_idx, 0):
                    col_widths[col_idx] = val_len

        for col_idx, width in col_widths.items():
            ws.col(col_idx).width = min(256 * 60, max(256 * 12, 256 * (width + 5)))

    wb.save(path)
    return True


# ---------------------------------------------------------------------------
# Pure-python climate core (no arcpy) — testable offline
# ---------------------------------------------------------------------------

def is_missing(v):
    """True if value is a NASA missing sentinel, None or NaN."""
    if v is None:
        return True
    try:
        f = float(v)
    except Exception:
        return True
    try:
        if math.isnan(f):
            return True
    except Exception:
        pass
    for s in MISSING_SENTINELS:
        if abs(f - s) < 1e-9:
            return True
    return False


def month_days(year, month):
    return calendar.monthrange(year, month)[1]


def safe_mean(values):
    vals = [float(v) for v in values if not is_missing(v)]
    if not vals:
        return None
    return sum(vals) / len(vals)


def safe_sum(values):
    vals = [float(v) for v in values if not is_missing(v)]
    if not vals:
        return None
    return sum(vals)


def circular_mean_deg(angles):
    """Prevailing direction via vector mean. Returns 0-360 or None."""
    sins, coss = [], []
    for a in angles:
        if is_missing(a):
            continue
        try:
            r = math.radians(float(a) % 360.0)
        except Exception:
            continue
        sins.append(math.sin(r))
        coss.append(math.cos(r))
    if not sins:
        return None
    ms = sum(sins) / len(sins)
    mc = sum(coss) / len(coss)
    if abs(ms) < 1e-12 and abs(mc) < 1e-12:
        return None
    return math.degrees(math.atan2(ms, mc)) % 360.0


def group_monthly_by_calendar_month(monthly):
    """monthly: {(y,m): v} or {m: v} -> {m: [values]} valid only."""
    out = dict((m, []) for m in range(1, 13))
    for ym, v in monthly.items():
        if isinstance(ym, (tuple, list)):
            m = int(ym[1])
        else:
            m = int(ym)
        if 1 <= m <= 12 and not is_missing(v):
            try:
                out[m].append(float(v))
            except Exception:
                pass
    return out


def climat_monthly_means(monthly):
    """Mean of each calendar month across years -> {m: mean}."""
    g = group_monthly_by_calendar_month(monthly)
    res = {}
    for m, v in g.items():
        res[m] = sum(v) / len(v) if v else None
    return res


def seasonal_means_from_monthly(monthly):
    """Mean-type aggregation. Returns dict Annual/Winter/Spring/Summer/Autumn."""
    clim = climat_monthly_means(monthly)
    res = {}
    ann = [v for v in clim.values() if v is not None]
    res["Annual"] = sum(ann) / len(ann) if ann else None
    for season, months in SEASONS.items():
        vals = [clim[m] for m in months if clim.get(m) is not None]
        res[season] = sum(vals) / len(vals) if vals else None
    return res


def seasonal_totals_from_monthly_totals(monthly_totals, years):
    """Sum-type aggregation (precipitation)."""
    per_year_annual = []
    per_year_season = dict((s, []) for s in SEASONS)
    for y in years:
        avals = [monthly_totals.get((y, m)) for m in range(1, 13)]
        avals = [float(v) for v in avals if not is_missing(v)]
        if avals:
            per_year_annual.append(sum(avals))
        for season, months in SEASONS.items():
            svals = [monthly_totals.get((y, m)) for m in months]
            svals = [float(v) for v in svals if not is_missing(v)]
            if svals:
                per_year_season[season].append(sum(svals))

    def _m(x):
        return sum(x) / len(x) if x else None

    return {
        "Annual_Mean": _m(per_year_annual),
        "Annual_Grand": sum(per_year_annual) if per_year_annual else None,
        "Winter": _m(per_year_season["Winter"]),
        "Spring": _m(per_year_season["Spring"]),
        "Summer": _m(per_year_season["Summer"]),
        "Autumn": _m(per_year_season["Autumn"]),
    }


def monthly_precip_total_from_rate(rate_mm_day, year, month):
    if is_missing(rate_mm_day):
        return None
    return float(rate_mm_day) * month_days(year, month)


def solar_mj_to_kwh(mj):
    if is_missing(mj):
        return None
    return float(mj) / 3.6


def pressure_kpa_to_mbar(v):
    """Auto-convert: POWER PS/PSL are typically kPa (~80-105). If |v|<200 treat as kPa."""
    if is_missing(v):
        return None
    f = float(v)
    if abs(f) < 200.0:
        return f * 10.0
    return f


def annual_temp_range(monthly_tmean):
    clim = climat_monthly_means(monthly_tmean)
    vals = [v for v in clim.values() if v is not None]
    if len(vals) < 2:
        return None
    return max(vals) - min(vals)


def monthly_range(monthly):
    """max - min of climatological monthly means (or None)."""
    clim = climat_monthly_means(monthly)
    vals = [v for v in clim.values() if v is not None]
    if len(vals) < 2:
        return None
    return max(vals) - min(vals)


def heat_index_c(t_c, rh):
    """Rothfusz (NOAA) heat index in C from air temp C + RH %.

    Applied to climatological monthly means; below 26.7C (80F) the index
    equals air temperature. Returns None when inputs are missing."""
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
        return None
    t_c, rh = float(t_c), float(rh)
    if rh < 0.0:
        rh = 0.0
    if rh > 100.0:
        rh = 100.0
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


def equal_interval_breaks(vmin, vmax, n=7):
    if vmin is None or vmax is None:
        return None
    if abs(vmax - vmin) < 1e-12:
        eps = abs(vmax) * 0.01 if vmax != 0 else 0.01
        vmin, vmax = vmin - eps, vmax + eps
    w = (vmax - vmin) / float(n)
    return [vmin + w * i for i in range(n + 1)]


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tolerance_meters(value_text):
    """Parse a GPLinearUnit text like '1000 Meters' into metres (float).

    Unknown/empty/zero values return 0.0 (= tolerance OFF)."""
    if value_text is None:
        return 0.0
    parts = str(value_text).strip().split()
    if not parts:
        return 0.0
    try:
        v = float(parts[0])
    except Exception:
        return 0.0
    unit = " ".join(parts[1:]).strip().lower() if len(parts) > 1 else "meters"
    factors = {"meter": 1.0, "meters": 1.0, "metre": 1.0, "metres": 1.0, "m": 1.0,
               "kilometer": 1000.0, "kilometers": 1000.0, "kilometre": 1000.0,
               "kilometres": 1000.0, "km": 1000.0,
               "foot": 0.3048, "feet": 0.3048, "ft": 0.3048,
               "mile": 1609.34, "miles": 1609.34, "mi": 1609.34,
               "decimaldegree": 111320.0, "decimaldegrees": 111320.0,
               "degree": 111320.0, "degrees": 111320.0, "dd": 111320.0}
    return v * factors.get(unit, 1.0)


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


def safe_project_fc(in_fc, out_sr, work_gdb, tag, warn):
    """Project in_fc into work_gdb/tmp_<tag> and return the new path.

    ArcMap 10.8 cannot Project into the in_memory workspace (ERROR 000944),
    so projection always targets a real Feature Class. On failure the input
    is returned unchanged (caller keeps the input SR)."""
    out_fc = os.path.join(work_gdb, "tmp_" + tag)
    try:
        if arcpy.Exists(out_fc):
            arcpy.management.Delete(out_fc)
    except Exception:
        pass
    try:
        arcpy.management.Project(in_fc, out_fc, out_sr)
        return out_fc
    except Exception as ex:
        try:
            warn("Projection to output SR failed (%s); keeping input SR." % ex)
        except Exception:
            pass
        return in_fc


def thin_points_tolerance(pts, tol_m):
    """Greedy order-preserving thinning: keep the first point of each cluster.

    pts: [{"oid":..,"lat":..,"lon":..}]. Distances use an equirectangular
    approximation (metres) adequate for a thinning threshold. Returns
    (kept_list, dropped_oid_list)."""
    if tol_m is None or tol_m <= 0 or len(pts) < 2:
        return list(pts), []
    kept, dropped = [], []
    tol2 = tol_m * tol_m
    for p in pts:
        dup = False
        for q in kept:
            mlat = math.radians((p["lat"] + q["lat"]) / 2.0)
            dx = (p["lon"] - q["lon"]) * 111320.0 * math.cos(mlat)
            dy = (p["lat"] - q["lat"]) * 111320.0
            if dx * dx + dy * dy < tol2:
                dup = True
                break
        if dup:
            dropped.append(p["oid"])
        else:
            kept.append(p)
    return kept, dropped


def compute_temperature_fields(m_tmean, m_tmax, m_tmin, m_rh=None):
    """m_*: {(y,m): value C (RH in %)}. Returns dict of new T_*/HI_* fields."""
    s_mean = seasonal_means_from_monthly(m_tmean)
    clim = climat_monthly_means(m_tmean)
    s_max = seasonal_means_from_monthly(m_tmax)
    s_min = seasonal_means_from_monthly(m_tmin)
    sum_max = [clim.get(m) for m in SEASONS["Summer"] if clim.get(m) is not None]
    win_min = [clim.get(m) for m in SEASONS["Winter"] if clim.get(m) is not None]
    clim_rh = climat_monthly_means(m_rh or {})
    hi_m = dict((m, heat_index_c(clim.get(m), clim_rh.get(m))) for m in range(1, 13))
    hi_vals = [v for v in hi_m.values() if v is not None]
    hi_sum = [hi_m[m] for m in SEASONS["Summer"] if hi_m.get(m) is not None]
    return {
        "T_Annual_Mean": s_mean["Annual"],
        "T_Winter_Mean": s_mean["Winter"],
        "T_Spring_Mean": s_mean["Spring"],
        "T_Summer_Mean": s_mean["Summer"],
        "T_Autumn_Mean": s_mean["Autumn"],
        "T_Annual_Range": annual_temp_range(m_tmean),
        "T_Max_Summer_Month_Mean": max(sum_max) if sum_max else None,
        "T_Min_Winter_Month_Mean": min(win_min) if win_min else None,
        "T_Annual_Max_Mean": s_max["Annual"],
        "T_Annual_Min_Mean": s_min["Annual"],
        "HI_Annual_Mean": sum(hi_vals) / len(hi_vals) if hi_vals else None,
        "HI_Summer_Mean": sum(hi_sum) / len(hi_sum) if hi_sum else None,
    }


def compute_wind_fields(m_spd, m_dir):
    """Circular means for direction, arithmetic for speed."""
    s_spd = seasonal_means_from_monthly(m_spd)
    clim_spd = climat_monthly_means(m_spd)
    spd_vals = [v for v in clim_spd.values() if v is not None]
    out = {
        "W_Spd_Annual_Mean": s_spd["Annual"],
        "W_Spd_Winter_Mean": s_spd["Winter"],
        "W_Spd_Spring_Mean": s_spd["Spring"],
        "W_Spd_Summer_Mean": s_spd["Summer"],
        "W_Spd_Autumn_Mean": s_spd["Autumn"],
        "W_Spd_Annual_Max_Month": max(spd_vals) if spd_vals else None,
        "W_Spd_Annual_Range": (max(spd_vals) - min(spd_vals)) if len(spd_vals) >= 2 else None,
    }
    _suffix = {"Winter": "Winter", "Spring": "Spring", "Summer": "Summer", "Autumn": "Autumn"}
    for season in SEASONS:
        months = SEASONS[season]
        vals = [v for ym, v in m_dir.items() if ym[1] in months and not is_missing(v)]
        out["W_Dir_" + _suffix[season] + "_Mean"] = circular_mean_deg(vals)
    allv = [v for v in m_dir.values() if not is_missing(v)]
    out["W_Dir_Annual_Mean"] = circular_mean_deg(allv)
    return out


def compute_solar_fields(m_sol_mj, years):
    """m_sol: {(y,m): MJ/m2/day monthly rate}. Returns kWh fields."""
    daily_kwh = {}
    for ym, v in m_sol_mj.items():
        k = solar_mj_to_kwh(v)
        if k is not None:
            daily_kwh[ym] = k
    s = seasonal_means_from_monthly(daily_kwh)
    per_year = []
    for y in years:
        tot = 0.0
        ok = False
        for m in range(1, 13):
            v = daily_kwh.get((y, m))
            if v is not None:
                tot += float(v) * month_days(y, m)
                ok = True
        if ok:
            per_year.append(tot)
    total = sum(per_year) / len(per_year) if per_year else None
    return {
        "Sol_Annual_Mean": s["Annual"],
        "Sol_Annual_Total": total,
        "Sol_Winter_Mean": s["Winter"],
        "Sol_Spring_Mean": s["Spring"],
        "Sol_Summer_Mean": s["Summer"],
        "Sol_Autumn_Mean": s["Autumn"],
    }


def extraterrestrial_radiation_ra(lat_deg, month):
    """Computes extraterrestrial solar radiation Ra in mm/day equivalent for a given month (FAO-56 standard)."""
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


def compute_drought_fields(m_tmean, m_tmax, m_tmin, m_precip, lat=0.0):
    """Computes annual drought and aridity indicators:
    - DM_Aridity_Annual: De Martonne Aridity Index = P / (T + 10)
    - PET_Hargreaves_Annual: Annual Potential Evapotranspiration (Hargreaves-Samani, mm/year)
    - UNEP_Aridity_Annual: UNEP Aridity Index = P / PET
    - Water_Deficit_Annual: Annual Climatic Water Balance = P - PET (mm/year)
    - Dry_Months_Count: Count of biologically dry months where P_month < 2 * T_month"""
    c_tmean = climat_monthly_means(m_tmean)
    c_tmax = climat_monthly_means(m_tmax)
    c_tmin = climat_monthly_means(m_tmin)
    c_precip = climat_monthly_means(m_precip)

    days_in_m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    monthly_pet = []
    monthly_p = []
    monthly_t = []
    dry_count = 0

    for m in range(1, 13):
        t = c_tmean.get(m)
        tx = c_tmax.get(m)
        tn = c_tmin.get(m)
        p = c_precip.get(m)

        if t is None:
            t = 20.0
        if tx is None:
            tx = t + 5.0
        if tn is None:
            tn = t - 5.0
        if p is None:
            p = 0.0

        p = max(0.0, float(p))
        t = float(t)
        tx = float(tx)
        tn = float(tn)

        monthly_p.append(p)
        monthly_t.append(t)

        ra = extraterrestrial_radiation_ra(lat, m)
        tdiff = max(0.0, tx - tn)
        pet_daily = 0.0023 * ra * (t + 17.8) * math.sqrt(tdiff)
        pet_month = max(0.0, pet_daily * days_in_m[m - 1])
        monthly_pet.append(pet_month)

        if p < (2.0 * t):
            dry_count += 1

    p_annual = sum(monthly_p)
    t_annual = (sum(monthly_t) / 12.0) if monthly_t else 20.0
    pet_annual = sum(monthly_pet)

    denom_dm = t_annual + 10.0
    dm_aridity = (p_annual / denom_dm) if denom_dm > 0.01 else 0.0
    unep_aridity = (p_annual / pet_annual) if pet_annual > 0.01 else 0.0
    water_deficit = p_annual - pet_annual

    return {
        "DM_Aridity_Annual": round(dm_aridity, 2),
        "PET_Hargreaves_Annual": round(pet_annual, 1),
        "UNEP_Aridity_Annual": round(unep_aridity, 3),
        "Water_Deficit_Annual": round(water_deficit, 1),
        "Dry_Months_Count": int(dry_count),
    }


# ---------------------------------------------------------------------------
# Field dictionary (spec sections 5-13 + 16-17). Single source of truth.
# ---------------------------------------------------------------------------
FIELD_DEFS = [
    ("T_Annual_Mean", "Annual Mean Air Temperature", u"المتوسط السنوي لدرجة الحرارة", "T2M", "Temperature", "Annual", "Mean", "C", u"متوسط قيم درجة الحرارة الشهرية خلال السنة", "Mean of monthly T2M over the period", "Mean of valid monthly T2M values"),
    ("T_Winter_Mean", "Winter Mean Air Temperature", u"متوسط درجة الحرارة في الشتاء", "T2M", "Temperature", "Winter", "Mean", "C", u"متوسط أشهر 1 و2 و12", "Mean of Dec/Jan/Feb monthly means", "Mean of climatological months 12,1,2"),
    ("T_Spring_Mean", "Spring Mean Air Temperature", u"متوسط درجة الحرارة في الربيع", "T2M", "Temperature", "Spring", "Mean", "C", u"متوسط أشهر 3 و4 و5", "Mean of Mar/Apr/May monthly means", "Mean of climatological months 3,4,5"),
    ("T_Summer_Mean", "Summer Mean Air Temperature", u"متوسط درجة الحرارة في الصيف", "T2M", "Temperature", "Summer", "Mean", "C", u"متوسط أشهر 6 و7 و8", "Mean of Jun/Jul/Aug monthly means", "Mean of climatological months 6,7,8"),
    ("T_Autumn_Mean", "Autumn Mean Air Temperature", u"متوسط درجة الحرارة في الخريف", "T2M", "Temperature", "Autumn", "Mean", "C", u"متوسط أشهر 9 و10 و11", "Mean of Sep/Oct/Nov monthly means", "Mean of climatological months 9,10,11"),
    ("T_Annual_Range", "Annual Temperature Range", u"المدى الحراري السنوي العام", "T2M", "Temperature", "Annual", "Range", "C", u"أعلى متوسط شهري ناقص أدنى متوسط شهري", "Highest monthly mean minus lowest monthly mean", "max(clim monthly) - min(clim monthly)"),
    ("T_Max_Summer_Month_Mean", "Maximum Summer Monthly Mean Temperature", u"أقصى متوسط شهري لدرجة الحرارة في الصيف", "T2M", "Temperature", "Summer", "Max", "C", u"أعلى متوسط شهري صيفي", "Max of climatological T2M for months 6,7,8", "max of monthly means 6,7,8"),
    ("T_Min_Winter_Month_Mean", "Minimum Winter Monthly Mean Temperature", u"أدنى متوسط شهري لدرجة الحرارة في الشتاء", "T2M", "Temperature", "Winter", "Min", "C", u"أدنى متوسط شهري شتوي", "Min of climatological T2M for months 12,1,2", "min of monthly means 12,1,2"),
    ("T_Annual_Max_Mean", "Annual Mean Maximum Temperature", u"المتوسط السنوي لدرجات الحرارة العظمى", "T2M_MAX", "Temperature", "Annual", "Mean", "C", u"متوسط القيم العظمى الشهرية خلال السنة", "Annual mean of monthly T2M_MAX", "Mean of valid monthly T2M_MAX values"),
    ("T_Annual_Min_Mean", "Annual Mean Minimum Temperature", u"المتوسط السنوي لدرجات الحرارة الصغرى", "T2M_MIN", "Temperature", "Annual", "Mean", "C", u"متوسط القيم الصغرى الشهرية خلال السنة", "Annual mean of monthly T2M_MIN", "Mean of valid monthly T2M_MIN values"),
    ("HI_Annual_Mean", "Annual Mean Heat Index", u"المتوسط السنوي لمؤشر الحرارة المحسوسة", "T2M+RH2M", "Temperature", "Annual", "Mean", "C", u"متوسط مؤشر الحرارة المحسوسة الشهرية", "Annual mean Rothfusz heat index from T2M and RH2M", "Mean of monthly HI; equals T below 26.7C; needs humidity"),
    ("HI_Summer_Mean", "Summer Mean Heat Index", u"متوسط مؤشر الحرارة المحسوسة في فصل الصيف", "T2M+RH2M", "Temperature", "Summer", "Mean", "C", u"متوسط المؤشر صيفاً", "Summer mean heat index", "Mean of monthly HI for months 6,7,8"),
    ("R_Annual_Total", "Annual Total Precipitation", u"التراكم السنوي الإجمالي للأمطار", "PRECTOTCORR", "Precipitation", "Annual", "Sum", "mm/year", u"مجموع كميات المطر السنوي", "Mean annual total across years (single year: yearly sum)", "Mean of per-year annual sums"),
    ("R_Annual_Mean", "Mean Monthly Precipitation", u"المتوسط السنوي لمعدلات الأمطار الشهرية", "PRECTOTCORR", "Precipitation", "Annual", "Mean", "mm", u"متوسط الإجماليات الشهرية", "Mean of climatological monthly totals", "Mean of 12 monthly means"),
    ("R_Winter_Total", "Winter Total Precipitation", u"إجمالي أمطار فصل الشتاء", "PRECTOTCORR", "Precipitation", "Winter", "Sum", "mm", u"مجموع أمطار أشهر الشتاء", "Mean winter total across years", "Mean of per-year Dec+Jan+Feb totals"),
    ("R_Spring_Total", "Spring Total Precipitation", u"إجمالي أمطار فصل الربيع", "PRECTOTCORR", "Precipitation", "Spring", "Sum", "mm", u"مجموع أمطار أشهر الربيع", "Mean spring total across years", "Mean of per-year Mar+Apr+May totals"),
    ("R_Summer_Total", "Summer Total Precipitation", u"إجمالي أمطار فصل الصيف", "PRECTOTCORR", "Precipitation", "Summer", "Sum", "mm", u"مجموع أمطار أشهر الصيف", "Mean summer total across years", "Mean of per-year Jun+Jul+Aug totals"),
    ("R_Autumn_Total", "Autumn Total Precipitation", u"إجمالي أمطار فصل الخريف", "PRECTOTCORR", "Precipitation", "Autumn", "Sum", "mm", u"مجموع أمطار أشهر الخريف", "Mean autumn total across years", "Mean of per-year Sep+Oct+Nov totals"),
    ("R_Max_Daily_Month", "Maximum Daily Precipitation", u"أقصى كمية أمطار يومية مسجلة خلال شهر", "PRECTOTCORR", "Precipitation", "Annual", "Max", "mm/day", u"Maximum valid daily value (daily mode only)", "max(valid daily PRECTOTCORR)", "max of daily values"),
    ("R_Annual_Rain_Days_Total", "Annual Rain Days Total", u"إجمالي عدد الأيام الممطرة في السنة", "PRECTOTCORR", "Precipitation", "Annual", "Count", "days", u"عدد الأيام بكمية >= 1 مم (الوضع اليومي فقط)", "Mean annual count of days >= 1mm (daily mode only)", "Mean of per-year counts"),
    ("PSL_Annual_Mean", "Annual Mean Sea Level Pressure", u"المتوسط السنوي لضغط مستوى سطح البحر", "SLP", "Sea Level Pressure", "Annual", "Mean", "mbar/hPa", u"متوسط الضغط المصحح إلى مستوى سطح البحر", "Mean sea-level pressure", "Mean of valid values; kPa*10 if needed"),
    ("PSL_Winter_Mean", "Winter Mean Sea Level Pressure", u"متوسط ضغط مستوى سطح البحر في الشتاء", "SLP", "Sea Level Pressure", "Winter", "Mean", "mbar/hPa", u"متوسط الشتاء", "Winter mean sea-level pressure", "Mean of months 12,1,2"),
    ("PSL_Spring_Mean", "Spring Mean Sea Level Pressure", u"متوسط ضغط مستوى سطح البحر في الربيع", "SLP", "Sea Level Pressure", "Spring", "Mean", "mbar/hPa", u"متوسط الربيع", "Spring mean", "Mean of months 3,4,5"),
    ("PSL_Summer_Mean", "Summer Mean Sea Level Pressure", u"متوسط ضغط مستوى سطح البحر في الصيف", "SLP", "Sea Level Pressure", "Summer", "Mean", "mbar/hPa", u"متوسط الصيف", "Summer mean", "Mean of months 6,7,8"),
    ("PSL_Autumn_Mean", "Autumn Mean Sea Level Pressure", u"متوسط ضغط مستوى سطح البحر في الخريف", "SLP", "Sea Level Pressure", "Autumn", "Mean", "mbar/hPa", u"متوسط الخريف", "Autumn mean", "Mean of months 9,10,11"),
    ("PSL_Annual_Range", "Annual Sea Level Pressure Range", u"المدى السنوي لضغط مستوى سطح البحر", "SLP", "Sea Level Pressure", "Annual", "Range", "mbar/hPa", u"max-min climatological monthly means", "max-min of monthly means", "max(clim) - min(clim)"),
    ("PS_Annual_Mean", "Annual Mean Surface Pressure", u"المتوسط السنوي للضغط الجوي عند السطح الفعلي", "PS", "Surface Pressure", "Annual", "Mean", "mbar/hPa", u"متوسط الضغط الفعلي عند سطح الأرض", "Mean surface pressure", "Mean of valid values; kPa*10 if needed"),
    ("PS_Winter_Mean", "Winter Mean Surface Pressure", u"متوسط الضغط السطحي في الشتاء", "PS", "Surface Pressure", "Winter", "Mean", "mbar/hPa", u"متوسط الشتاء", "Winter mean", "Mean of months 12,1,2"),
    ("PS_Spring_Mean", "Spring Mean Surface Pressure", u"متوسط الضغط السطحي في الربيع", "PS", "Surface Pressure", "Spring", "Mean", "mbar/hPa", u"متوسط الربيع", "Spring mean", "Mean of months 3,4,5"),
    ("PS_Summer_Mean", "Summer Mean Surface Pressure", u"متوسط الضغط السطحي في الصيف", "PS", "Surface Pressure", "Summer", "Mean", "mbar/hPa", u"متوسط الصيف", "Summer mean", "Mean of months 6,7,8"),
    ("PS_Autumn_Mean", "Autumn Mean Surface Pressure", u"متوسط الضغط السطحي في الخريف", "PS", "Surface Pressure", "Autumn", "Mean", "mbar/hPa", u"متوسط الخريف", "Autumn mean", "Mean of months 9,10,11"),
    ("PS_Annual_Range", "Annual Surface Pressure Range", u"المدى السنوي للضغط السطحي الفعلي", "PS", "Surface Pressure", "Annual", "Range", "mbar/hPa", u"max-min climatological monthly means", "max-min of monthly means", "max(clim) - min(clim)"),
    ("W_Spd_Annual_Mean", "Annual Mean Wind Speed", u"المتوسط السنوي لسرعة الرياح", "WS10M", "Wind", "Annual", "Mean", "m/s", u"متوسط سرعة الرياح على ارتفاع 10 أمتار", "Mean 10-m wind speed", "Mean of valid values"),
    ("W_Spd_Winter_Mean", "Winter Mean Wind Speed", u"متوسط سرعة الرياح في الشتاء", "WS10M", "Wind", "Winter", "Mean", "m/s", u"متوسط الشتاء", "Winter mean", "Mean of months 12,1,2"),
    ("W_Spd_Spring_Mean", "Spring Mean Wind Speed", u"متوسط سرعة الرياح ربيعاً", "WS10M", "Wind", "Spring", "Mean", "m/s", u"متوسط الربيع", "Spring mean", "Mean of months 3,4,5"),
    ("W_Spd_Summer_Mean", "Summer Mean Wind Speed", u"متوسط سرعة الرياح صيفاً", "WS10M", "Wind", "Summer", "Mean", "m/s", u"متوسط الصيف", "Summer mean", "Mean of months 6,7,8"),
    ("W_Spd_Autumn_Mean", "Autumn Mean Wind Speed", u"متوسط سرعة الرياح خريفاً", "WS10M", "Wind", "Autumn", "Mean", "m/s", u"متوسط الخريف", "Autumn mean", "Mean of months 9,10,11"),
    ("W_Spd_Annual_Max_Month", "Maximum Monthly Mean Wind Speed", u"أقصى متوسط سرعة رياح شهري مسجل خلال العام", "WS10M", "Wind", "Annual", "Max", "m/s", u"max climatological monthly mean", "max of monthly means", "max(clim monthly)"),
    ("W_Spd_Annual_Range", "Annual Wind Speed Range", u"المدى السنوي لسرعة الرياح الشهرية", "WS10M", "Wind", "Annual", "Range", "m/s", u"max-min monthly means", "max-min of monthly means", "max(clim) - min(clim)"),
    ("W_Dir_Annual_Mean", "Annual Prevailing Wind Direction", u"المتوسط السنوي لاتجاه الرياح السائد", "WD10M", "Wind", "Annual", "Circular Mean", "degree", u"متوسط دائري لاتجاهات الرياح", "Vector-mean wind direction", "atan2(mean sin, mean cos)"),
    ("W_Dir_Winter_Mean", "Winter Prevailing Wind Direction", u"متوسط اتجاه الرياح في الشتاء", "WD10M", "Wind", "Winter", "Circular Mean", "degree", u"متوسط دائري شتاءً", "Winter vector mean", "months 12,1,2"),
    ("W_Dir_Spring_Mean", "Spring Prevailing Wind Direction", u"متوسط اتجاه الرياح في الربيع", "WD10M", "Wind", "Spring", "Circular Mean", "degree", u"متوسط دائري ربيعاً", "Spring vector mean", "months 3,4,5"),
    ("W_Dir_Summer_Mean", "Summer Prevailing Wind Direction", u"متوسط اتجاه الرياح في الصيف", "WD10M", "Wind", "Summer", "Circular Mean", "degree", u"متوسط دائري صيفاً", "Summer vector mean", "months 6,7,8"),
    ("W_Dir_Autumn_Mean", "Autumn Prevailing Wind Direction", u"متوسط اتجاه الرياح في الخريف", "WD10M", "Wind", "Autumn", "Circular Mean", "degree", u"متوسط دائري خريفاً", "Autumn vector mean", "months 9,10,11"),
    ("RH_Annual_Mean", "Annual Mean Relative Humidity", u"المتوسط السنوي للرطوبة النسبية", "RH2M", "Relative Humidity", "Annual", "Mean", "%", u"متوسط الرطوبة النسبية على ارتفاع مترين", "Mean 2-m relative humidity", "Mean of valid values"),
    ("RH_Winter_Mean", "Winter Mean Relative Humidity", u"متوسط الرطوبة النسبية شتاءً", "RH2M", "Relative Humidity", "Winter", "Mean", "%", u"متوسط الشتاء", "Winter mean", "months 12,1,2"),
    ("RH_Spring_Mean", "Spring Mean Relative Humidity", u"متوسط الرطوبة النسبية ربيعاً", "RH2M", "Relative Humidity", "Spring", "Mean", "%", u"متوسط الربيع", "Spring mean", "months 3,4,5"),
    ("RH_Summer_Mean", "Summer Mean Relative Humidity", u"متوسط الرطوبة النسبية صيفاً", "RH2M", "Relative Humidity", "Summer", "Mean", "%", u"متوسط الصيف", "Summer mean", "months 6,7,8"),
    ("RH_Autumn_Mean", "Autumn Mean Relative Humidity", u"متوسط الرطوبة النسبية خريفاً", "RH2M", "Relative Humidity", "Autumn", "Mean", "%", u"متوسط الخريف", "Autumn mean", "months 9,10,11"),
    ("Sol_Annual_Mean", "Annual Mean Daily Solar Radiation", u"المتوسط اليومي السنوي للإشعاع الشمسي", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Annual", "Mean", "kWh/m2/day", u"معدل الإشعاع اليومي المعتاد", "Mean daily solar radiation", "Mean of MJ/3.6"),
    ("Sol_Annual_Total", "Annual Total Solar Radiation", u"إجمالي الإشعاع الشمسي السنوي التراكمي", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Annual", "Sum", "kWh/m2/year", u"إجمالي الطاقة الشمسية المتراكمة خلال السنة", "Annual accumulated solar energy", "Per-year sum(daily*days), averaged"),
    ("Sol_Winter_Mean", "Winter Mean Daily Solar Radiation", u"متوسط الإشعاع الشمسي شتاءً", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Winter", "Mean", "kWh/m2/day", u"متوسط الشتاء", "Winter mean", "months 12,1,2 (kWh)"),
    ("Sol_Spring_Mean", "Spring Mean Daily Solar Radiation", u"متوسط الإشعاع الشمسي ربيعاً", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Spring", "Mean", "kWh/m2/day", u"متوسط الربيع", "Spring mean", "months 3,4,5"),
    ("Sol_Summer_Mean", "Summer Mean Daily Solar Radiation", u"متوسط الإشعاع الشمسي صيفاً", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Summer", "Mean", "kWh/m2/day", u"متوسط الصيف", "Summer mean", "months 6,7,8"),
    ("Sol_Autumn_Mean", "Autumn Mean Daily Solar Radiation", u"متوسط الإشعاع الشمسي خريفاً", "ALLSKY_SFC_SW_DWN", "Solar Radiation", "Autumn", "Mean", "kWh/m2/day", u"متوسط الخريف", "Autumn mean", "months 9,10,11"),
    ("UV_Annual_Mean", "Annual Mean UV Index", u"المتوسط السنوي لمؤشر الأشعة فوق البنفسجية", "ALLSKY_SFC_UV_INDEX", "UV Index", "Annual", "Mean", "Index", u"متوسط مؤشر UV", "Mean UV index", "Mean of valid values"),
    ("UV_Winter_Mean", "Winter Mean UV Index", u"متوسط مؤشر UV شتاءً", "ALLSKY_SFC_UV_INDEX", "UV Index", "Winter", "Mean", "Index", u"متوسط الشتاء", "Winter mean", "months 12,1,2"),
    ("UV_Spring_Mean", "Spring Mean UV Index", u"متوسط مؤشر UV ربيعاً", "ALLSKY_SFC_UV_INDEX", "UV Index", "Spring", "Mean", "Index", u"متوسط الربيع", "Spring mean", "months 3,4,5"),
    ("UV_Summer_Mean", "Summer Mean UV Index", u"متوسط مؤشر UV صيفاً", "ALLSKY_SFC_UV_INDEX", "UV Index", "Summer", "Mean", "Index", u"متوسط الصيف", "Summer mean", "months 6,7,8"),
    ("UV_Autumn_Mean", "Autumn Mean UV Index", u"متوسط مؤشر UV خريفاً", "ALLSKY_SFC_UV_INDEX", "UV Index", "Autumn", "Mean", "Index", u"متوسط الخريف", "Autumn mean", "months 9,10,11"),
    ("Cld_Annual_Mean", "Annual Mean Cloud Cover", u"المتوسط السنوي للغطاء السحابي", "CLOUD_AMT", "Cloud Cover", "Annual", "Mean", "%", u"متوسط الغطاء السحابي", "Mean cloud amount", "Mean of valid values"),
    ("Cld_Winter_Mean", "Winter Mean Cloud Cover", u"متوسط الغطاء السحابي شتاءً", "CLOUD_AMT", "Cloud Cover", "Winter", "Mean", "%", u"متوسط الشتاء", "Winter mean", "months 12,1,2"),
    ("Cld_Spring_Mean", "Spring Mean Cloud Cover", u"متوسط الغطاء السحابي ربيعاً", "CLOUD_AMT", "Cloud Cover", "Spring", "Mean", "%", u"متوسط الربيع", "Spring mean", "months 3,4,5"),
    ("Cld_Summer_Mean", "Summer Mean Cloud Cover", u"متوسط الغطاء السحابي صيفاً", "CLOUD_AMT", "Cloud Cover", "Summer", "Mean", "%", u"متوسط الصيف", "Summer mean", "months 6,7,8"),
    ("Cld_Autumn_Mean", "Autumn Mean Cloud Cover", u"متوسط الغطاء السحابي خريفاً", "CLOUD_AMT", "Cloud Cover", "Autumn", "Mean", "%", u"متوسط الخريف", "Autumn mean", "months 9,10,11"),
    ("DM_Aridity_Annual", "De Martonne Aridity Index", u"مؤشر دي مارتون للجفاف والقحولة", "PRECTOTCORR+T2M", "Climate_Models", "Annual", "Index", "Index", u"مؤشر دي مارتون السنوي للقحولة والجفاف = P / (T + 10)", "Annual De Martonne aridity index P / (T + 10)", "P_ann / (T_ann + 10)"),
    ("PET_Hargreaves_Annual", "Annual Potential Evapotranspiration (Hargreaves)", u"التبخر-نتح الكامن السنوي بهارجريفز", "T2M+T2M_MAX+T2M_MIN", "Climate_Models", "Annual", "Sum", "mm/year", u"التبخر-نتح الكامن السنوي المحسوب بطريقة هارجريفز-ساماني", "Annual potential evapotranspiration (Hargreaves-Samani)", "Sum of monthly Hargreaves ETo"),
    ("UNEP_Aridity_Annual", "UNEP Aridity Index", u"مؤشر القحولة العالمي (برنامج الأمم المتحدة للبيئة)", "PRECTOTCORR+PET", "Climate_Models", "Annual", "Index", "Index", u"مؤشر القحولة العالمي المعتمد من UNEP = P / PET", "UNEP Aridity Index P / PET", "P_ann / PET_ann"),
    ("Water_Deficit_Annual", "Annual Climatic Water Deficit/Surplus", u"العجز/الفائض المائي المناخي السنوي", "PRECTOTCORR-PET", "Climate_Models", "Annual", "Sum", "mm/year", u"الفارق السنوي بين الأمطار والتبخر الكامن = P - PET", "Annual climatic water balance (P - PET)", "P_ann - PET_ann"),
    ("Dry_Months_Count", "Biological Dry Months Count (Walter-Lieth)", u"عدد الأشهر الجافة بيولوجياً (والتر-ليث)", "PRECTOTCORR+T2M", "Climate_Models", "Annual", "Count", "months", u"عدد أشهر السنة التي تقل فيها كمية الأمطار عن ضعف درجة الحرارة P < 2T", "Annual count of biologically dry months where P_month < 2*T_month", "Count of months where P < 2*T"),
]

FIELD_BY_NAME = dict((r[0], r) for r in FIELD_DEFS)

MODULE_FIELDS = {}
for _r in FIELD_DEFS:
    MODULE_FIELDS.setdefault(_r[4], []).append(_r[0])
MODULE_FIELDS["Climate_Models"] = [
    "DM_Aridity_Annual", "PET_Hargreaves_Annual", "UNEP_Aridity_Annual",
    "Water_Deficit_Annual", "Dry_Months_Count", "HI_Summer_Mean", "HI_Annual_Mean"
]
MODULE_FIELDS["Drought & Aridity"] = [
    "DM_Aridity_Annual", "PET_Hargreaves_Annual", "UNEP_Aridity_Annual",
    "Water_Deficit_Annual", "Dry_Months_Count"
]

# short GDB-safe names for per-element point layers: Climate_Points_<short>
MODULE_SHORT = {
    "Temperature": "Temperature",
    "Precipitation": "Precipitation",
    "Drought & Aridity": "Drought_Aridity",
    "Climate_Models": "Climate_Models",
    "Sea Level Pressure": "Sea_Level_Pressure",
    "Surface Pressure": "Surface_Pressure",
    "Wind": "Wind",
    "Relative Humidity": "Relative_Humidity",
    "Solar Radiation": "Solar_Radiation",
    "UV Index": "UV_Index",
    "Cloud Cover": "Cloud_Cover",
}

SHP_FIELD_MAP = {
    "Cld_Annual_Mean": "Cld_AnMean",
    "Cld_Autumn_Mean": "Cld_AuMean",
    "Cld_Spring_Mean": "Cld_SpMean",
    "Cld_Summer_Mean": "Cld_SuMean",
    "Cld_Winter_Mean": "Cld_WnMean",
    "DM_Aridity_Annual": "DM_AridAnn",
    "Dry_Months_Count": "Dry_Months",
    "HI_Annual_Mean": "HI_AnnMean",
    "HI_Summer_Mean": "HI_SumMean",
    "Interp_Meth": "Intrp_Meth",
    "PSL_Annual_Mean": "PSL_AnMean",
    "PSL_Annual_Range": "PSL_AnRng",
    "PSL_Autumn_Mean": "PSL_AuMean",
    "PSL_Spring_Mean": "PSL_SpMean",
    "PSL_Summer_Mean": "PSL_SuMean",
    "PSL_Winter_Mean": "PSL_WnMean",
    "PS_Annual_Mean": "PS_AnnMean",
    "PS_Annual_Range": "PS_AnnRng",
    "PS_Autumn_Mean": "PS_AutMean",
    "PS_Spring_Mean": "PS_SprMean",
    "PS_Summer_Mean": "PS_SumMean",
    "PS_Winter_Mean": "PS_WinMean",
    "RH_Annual_Mean": "RH_AnMean",
    "RH_Autumn_Mean": "RH_AuMean",
    "RH_Spring_Mean": "RH_SpMean",
    "RH_Summer_Mean": "RH_SuMean",
    "RH_Winter_Mean": "RH_WnMean",
    "R_Annual_Mean": "R_AnnMean",
    "R_Annual_Rain_Days_Total": "R_RainDays",
    "R_Annual_Total": "R_AnnTot",
    "R_Autumn_Total": "R_AutTot",
    "R_Max_Daily_Month": "R_MaxDayMo",
    "R_Spring_Total": "R_SprTot",
    "R_Summer_Total": "R_SumTot",
    "R_Winter_Total": "R_WinTot",
    "Sol_Annual_Mean": "Sol_AnMean",
    "Sol_Annual_Total": "Sol_AnTot",
    "Sol_Autumn_Mean": "Sol_AuMean",
    "Sol_Spring_Mean": "Sol_SpMean",
    "Sol_Summer_Mean": "Sol_SuMean",
    "Sol_Winter_Mean": "Sol_WnMean",
    "T_Annual_Max_Mean": "T_MaxMean",
    "T_Annual_Mean": "T_AnnMean",
    "T_Annual_Min_Mean": "T_MinMean",
    "T_Annual_Range": "T_AnnRng",
    "T_Autumn_Mean": "T_AutMean",
    "T_Max_Summer_Month_Mean": "T_MaxSumMo",
    "T_Min_Winter_Month_Mean": "T_MinWinMo",
    "T_Spring_Mean": "T_SprMean",
    "T_Summer_Mean": "T_SumMean",
    "T_Winter_Mean": "T_WinMean",
    "UV_Annual_Mean": "UV_AnMean",
    "UV_Autumn_Mean": "UV_AuMean",
    "UV_Spring_Mean": "UV_SpMean",
    "UV_Summer_Mean": "UV_SuMean",
    "UV_Winter_Mean": "UV_WnMean",
    "W_Dir_Annual_Mean": "WDr_AnMean",
    "W_Dir_Autumn_Mean": "WDr_AuMean",
    "W_Dir_Spring_Mean": "WDr_SpMean",
    "W_Dir_Summer_Mean": "WDr_SuMean",
    "W_Dir_Winter_Mean": "WDr_WnMean",
    "W_Spd_Annual_Max_Month": "WSp_MaxMo",
    "W_Spd_Annual_Mean": "WSp_AnMean",
    "W_Spd_Annual_Range": "WSp_AnRng",
    "W_Spd_Autumn_Mean": "WSp_AuMean",
    "W_Spd_Spring_Mean": "WSp_SpMean",
    "W_Spd_Summer_Mean": "WSp_SuMean",
    "W_Spd_Winter_Mean": "WSp_WnMean",
    "PET_Hargreaves_Annual": "PET_HarAnn",
    "UNEP_Aridity_Annual": "UNEP_Arid",
    "Water_Deficit_Annual": "WatDefAnn",
}

REV_SHP_MAP = dict((v, k) for k, v in SHP_FIELD_MAP.items())


def field_display_label(r):
    """Clean label for ArcMap GPString checklist (no semicolons!)."""
    return "%s - %s" % (r[0], r[1])


def parse_season_name(s_text):
    """Normalize 'Winter (DJF)' -> 'Winter'"""
    for s in ("Winter", "Spring", "Summer", "Autumn"):
        if s.lower() in s_text.lower():
            return s
    return s_text


def get_candidate_fields(modules, aggregations=None, seasons=None):
    """Returns list of (field_name, display_label, module) for active criteria."""
    if aggregations is None:
        aggregations = ["Annual Summaries", "Seasonal Summaries", "Extreme & Bioclimatic Indices"]
    if seasons is None:
        seasons = ["Winter", "Spring", "Summer", "Autumn"]
    else:
        seasons = [parse_season_name(s) for s in seasons]

    want_ann = any("Annual" in a for a in aggregations)
    want_sea = any("Seasonal" in a for a in aggregations)
    want_ext = any("Extreme" in a or "Indices" in a for a in aggregations)

    candidates = []
    for r in FIELD_DEFS:
        fname, en_label, _ar, _raw, mod, s_type, stat, _u = r[:8]
        if mod not in modules:
            continue

        is_season = (s_type in ("Winter", "Spring", "Summer", "Autumn"))
        is_extreme = (stat in ("Range", "Max", "Min", "Count") or fname.startswith("HI_"))

        match = False
        if is_season:
            if want_sea and (s_type in seasons):
                match = True
        else:
            if is_extreme:
                if want_ext or want_ann:
                    match = True
            else:
                if want_ann:
                    match = True

        if match:
            candidates.append((fname, field_display_label(r), mod))
    return candidates


def resolve_filtered_fields(modules, scope, aggregations=None, seasons=None, custom_fields=None):
    """Returns {module: [field_names]} based on user filtering configuration."""
    out = dict((m, []) for m in modules)

    if not scope or scope.startswith("All Variables"):
        for m in modules:
            out[m] = list(MODULE_FIELDS.get(m, []))
        return out

    if scope.startswith("Custom Field"):
        selected_raw = []
        if custom_fields:
            if isinstance(custom_fields, (list, tuple)):
                selected_raw = list(custom_fields)
            else:
                selected_raw = [x.strip() for x in str(custom_fields).split(";") if x.strip()]

        chosen_names = set()
        for item in selected_raw:
            cleaned = item.strip("'\"")
            fname = cleaned.split(" - ")[0].strip()
            if fname in FIELD_BY_NAME:
                chosen_names.add(fname)

        for m in modules:
            for f in MODULE_FIELDS.get(m, []):
                if f in chosen_names:
                    out[m].append(f)
        return out

    # "Filter by Seasons & Aggregations"
    candidates = get_candidate_fields(modules, aggregations, seasons)
    for fname, _lbl, mod in candidates:
        if mod in out and fname not in out[mod]:
            out[mod].append(fname)
    return out


def metadata_rows_for_modules(modules, wanted_fields_by_module=None):
    rows = []
    wanted_all = set()
    if wanted_fields_by_module:
        for m_name in modules:
            for f_name in wanted_fields_by_module.get(m_name, []):
                wanted_all.add(f_name)
    for r in FIELD_DEFS:
        is_in_mod = (r[4] in modules)
        is_submodel_field = ("Climate_Models" in modules and r[0] in MODULE_FIELDS.get("Climate_Models", []))
        if is_in_mod or is_submodel_field:
            if wanted_fields_by_module is not None and r[0] not in wanted_all:
                continue
            rows.append({
                "Field_Name": r[0], "Full_Name_EN": r[1], "Name_AR": r[2],
                "NASA_Code": r[3], "Module": ("Climate_Models" if (is_submodel_field and not is_in_mod) else r[4]),
                "Period": r[5], "Statistic": r[6], "Unit": r[7], "Description_AR": r[8],
                "Description_EN": r[9], "Calculation": r[10],
                "Source": "NASA POWER", "Notes": "",
            })
    return rows


# ---------------------------------------------------------------------------
# NASA POWER client (requests preferred, urllib2 fallback for old installs)
# ---------------------------------------------------------------------------

def nasa_url(temporal, lat, lon, start_year, end_year, params, start_date=None, end_date=None):
    t = "monthly" if temporal == "Monthly" else "daily"
    if temporal == "Monthly":
        start, end = str(start_year), str(end_year)
    else:
        if start_date and end_date:
            start = str(start_date).replace("-", "")
            end = str(end_date).replace("-", "")
        else:
            start, end = "%d0101" % start_year, "%d1231" % end_year
    return (
        "%s/%s/point?parameters=%s&community=%s&longitude=%s&latitude=%s"
        "&start=%s&end=%s&format=JSON"
        % (NASA_BASE, t, ",".join(params), NASA_COMMUNITY,
           repr(float(lon)), repr(float(lat)), start, end)
    )


def _http_get_json(url, timeout, session=None):
    if _HAS_REQUESTS:
        get = (session.get if session is not None else requests.get)
        resp = get(url, timeout=timeout,
                   headers={"User-Agent": "POWER-Climate-Atlas-Generator/1.0-arcmap10"})
        if resp.status_code != 200:
            raise RuntimeError("HTTP %s: %s" % (resp.status_code, resp.text[:300]))
        return resp.json()
    # fallback for environments without requests
    import urllib2
    req = urllib2.Request(url, headers={"User-Agent": "POWER-Climate-Atlas-Generator/1.0-arcmap10"})
    resp = urllib2.urlopen(req, timeout=timeout)
    return json.load(resp)


def fetch_nasa_point(lat, lon, start_year, end_year, params, temporal="Monthly",
                     timeout=60, retries=3, session=None, start_date=None, end_date=None):
    """Returns properties.parameter dict. Raises RuntimeError after retries."""
    url = nasa_url(temporal, lat, lon, start_year, end_year, params,
                   start_date=start_date, end_date=end_date)
    last_err = None
    for attempt in range(retries):
        try:
            data = _http_get_json(url, timeout, session)
            try:
                return data["properties"]["parameter"]
            except KeyError:
                raise RuntimeError("Unexpected NASA response: %s" % str(data)[:300])
        except Exception as ex:
            last_err = ex
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("NASA request failed (%s): %s" % (url, last_err))


def parse_monthly_series(raw_dict):
    """raw: {YYYYMM: value} -> {(y,m): value}. Skips non-month keys (e.g. ANN='YYYY13')."""
    out = {}
    if not raw_dict:
        return out
    for k, v in raw_dict.items():
        try:
            ks = str(k)
            y, m = int(ks[:4]), int(ks[4:6])
            if 1 <= m <= 12:
                out[(y, m)] = float(v)
        except Exception:
            continue
    return out


def parse_daily_series(raw_dict):
    """raw: {YYYYMMDD: value} -> {(y,m,d): value}."""
    out = {}
    if not raw_dict:
        return out
    for k, v in raw_dict.items():
        try:
            ks = str(k)
            out[(int(ks[:4]), int(ks[4:6]), int(ks[6:8]))] = float(v)
        except Exception:
            continue
    return out


def build_monthly_from_daily(parameter_dict, mean_params, sum_params, years):
    """Convert daily NASA response to monthly {(y,m): v} per param."""
    monthly = {}
    for p in set(mean_params) | set(sum_params):
        daily = parse_daily_series(parameter_dict.get(p, {}))
        by_month = {}
        for ymd, v in daily.items():
            by_month.setdefault((ymd[0], ymd[1]), []).append(v)
        m = {}
        for ym, vals in by_month.items():
            if p in sum_params:
                m[ym] = safe_sum(vals)
            else:
                m[ym] = safe_mean(vals)
        monthly[p] = m
    return monthly


def fill_interior_gaps(monthly, method="climatological"):
    """Fill missing months.

    method:
      'climatological' (recommended): fill with the mean of the same calendar
          month across all available years. If single-year or month missing across
          all years, fallback to overall station mean.
      'linear': linear interpolation between nearest valid neighbours in
          chronological order, with boundary fill for leading/trailing months.
      'none': no filling -- skip missing values.

    Returns a new dict with gaps filled; original is not mutated."""
    if method == "none" or not monthly:
        return dict(monthly)
    out = dict(monthly)
    if method == "climatological":
        # Mean of same calendar month across years
        by_cal = {}  # m -> [values]
        for (y, m), v in monthly.items():
            if not is_missing(v):
                by_cal.setdefault(m, []).append(float(v))
        cal_mean = {}
        for m, vals in by_cal.items():
            if vals:
                cal_mean[m] = sum(vals) / len(vals)
        all_vals = [float(v) for v in monthly.values() if not is_missing(v)]
        overall_mean = (sum(all_vals) / len(all_vals)) if all_vals else None

        for (y, m), v in list(out.items()):
            if is_missing(v):
                if m in cal_mean:
                    out[(y, m)] = cal_mean[m]
                elif overall_mean is not None:
                    out[(y, m)] = overall_mean
        # Also fill completely missing (y,m) keys if that year has any data
        years_present = set(y for (y, _m) in monthly)
        for y in years_present:
            has_any = any(not is_missing(monthly.get((y, mm)))
                          for mm in range(1, 13))
            if has_any:
                for mm in range(1, 13):
                    if (y, mm) not in out or is_missing(out.get((y, mm))):
                        if mm in cal_mean:
                            out[(y, mm)] = cal_mean[mm]
                        elif overall_mean is not None:
                            out[(y, mm)] = overall_mean
    elif method in ("linear", "linear_boundary"):
        keys = sorted(out.keys())
        if not keys:
            return out
        valid_indices = [i for i, k in enumerate(keys) if not is_missing(out[k])]
        if not valid_indices:
            return out
        first_valid_i = valid_indices[0]
        last_valid_i = valid_indices[-1]
        first_valid_v = float(out[keys[first_valid_i]])
        last_valid_v = float(out[keys[last_valid_i]])

        # 1. Leading boundary fill (e.g. Jan before first valid)
        for i in range(first_valid_i):
            out[keys[i]] = first_valid_v

        # 2. Interior linear interpolation
        for i in range(first_valid_i + 1, last_valid_i):
            if not is_missing(out[keys[i]]):
                continue
            prev_i, prev_v = None, None
            for j in range(i - 1, -1, -1):
                if not is_missing(out[keys[j]]):
                    prev_i, prev_v = j, float(out[keys[j]])
                    break
            next_i, next_v = None, None
            for j in range(i + 1, len(keys)):
                if not is_missing(out[keys[j]]):
                    next_i, next_v = j, float(out[keys[j]])
                    break
            if prev_v is not None and next_v is not None:
                span = next_i - prev_i
                frac = float(i - prev_i) / span
                out[keys[i]] = prev_v + frac * (next_v - prev_v)

        # 3. Trailing boundary fill (e.g. Dec after last valid)
        for i in range(last_valid_i + 1, len(keys)):
            out[keys[i]] = last_valid_v
    return out


def spatial_impute_missing(results, modules):
    """Fill missing field values in results using Inverse Distance Weighting of
    the nearest valid stations, ensuring no point row is left blank or failed."""
    count = 0
    for m in modules:
        fields = MODULE_FIELDS.get(m, [])
        for f in fields:
            valid_pts = []
            for r in results:
                v = r.get("fields", {}).get(f)
                if v is not None and not is_missing(v):
                    valid_pts.append((float(r["lat"]), float(r["lon"]), float(v)))
            if not valid_pts:
                continue
            for r in results:
                v = r.get("fields", {}).get(f)
                if v is None or is_missing(v):
                    rlat, rlon = float(r["lat"]), float(r["lon"])
                    dists = []
                    for vlat, vlon, val in valid_pts:
                        d = math.hypot(rlat - vlat, rlon - vlon)
                        dists.append((d, val))
                    dists.sort(key=lambda x: x[0])
                    top = dists[:min(3, len(dists))]
                    if top[0][0] < 1e-6:
                        imputed = top[0][1]
                    else:
                        w_sum = sum(1.0 / max(d[0], 1e-6) for d in top)
                        imputed = sum((1.0 / max(d[0], 1e-6)) * d[1] for d in top) / w_sum
                    r.setdefault("fields", {})[f] = round(imputed, 3)
                    if r.get("status") != "OK":
                        r["status"] = "OK (Gap-Filled)"
                    count += 1
    return count


# ---------------------------------------------------------------------------
# Open-Meteo Historical API (ERA5 reanalysis) client — pure python + requests
# Daily aggregates where the archive provides them, hourly aggregates (averaged
# to monthly by us) where it does not. Output feeds the SAME monthly structure
# and compute_point_fields as NASA, so the field table never changes.
# ---------------------------------------------------------------------------
ADMIN_FIELDS = [
    ("Source_ID", "LONG", "Original point ID"),
    ("Point_Lat", "DOUBLE", "Point latitude WGS84"),
    ("Point_Lon", "DOUBLE", "Point longitude WGS84"),
    ("Data_Start", "TEXT", "Time series start date or year"),
    ("Data_End", "TEXT", "Time series end date or year"),
    ("Temporal", "TEXT", "Temporal frequency (Monthly)"),
    ("Interp_Meth", "TEXT", "Spatial interpolation algorithm"),
    ("Cell_Size", "DOUBLE", "Base raster cell size in meters"),
    ("Wind_Cell", "DOUBLE", "Wind grid cell size in meters"),
    ("Status", "TEXT", "Point processing status (OK / Error)"),
    ("Error_Msg", "TEXT", "Error message if any"),
]

REQUIRED_COLUMNS = [
    "OBJECTID", "Source_ID", "Point_Lat", "Point_Lon", "Data_Start", "Data_End",
    "Temporal", "Interp_Meth", "Cell_Size", "Wind_Cell", "Status", "Error_Msg",
    "T_Annual_Mean", "T_Winter_Mean", "T_Spring_Mean", "T_Summer_Mean", "T_Autumn_Mean",
    "T_Annual_Range", "T_Max_Summer_Month_Mean", "T_Min_Winter_Month_Mean",
    "T_Annual_Max_Mean", "T_Annual_Min_Mean", "HI_Annual_Mean", "HI_Summer_Mean",
    "R_Annual_Total", "R_Annual_Mean", "R_Winter_Total", "R_Spring_Total",
    "R_Summer_Total", "R_Autumn_Total", "R_Max_Daily_Month", "R_Annual_Rain_Days_Total",
    "PSL_Annual_Mean", "PSL_Winter_Mean", "PSL_Spring_Mean", "PSL_Summer_Mean", "PSL_Autumn_Mean", "PSL_Annual_Range",
    "PS_Annual_Mean", "PS_Winter_Mean", "PS_Spring_Mean", "PS_Summer_Mean", "PS_Autumn_Mean", "PS_Annual_Range",
    "W_Spd_Annual_Mean", "W_Spd_Winter_Mean", "W_Spd_Spring_Mean", "W_Spd_Summer_Mean", "W_Spd_Autumn_Mean",
    "W_Spd_Annual_Max_Month", "W_Spd_Annual_Range",
    "W_Dir_Annual_Mean", "W_Dir_Winter_Mean", "W_Dir_Spring_Mean", "W_Dir_Summer_Mean", "W_Dir_Autumn_Mean",
    "RH_Annual_Mean", "RH_Winter_Mean", "RH_Spring_Mean", "RH_Summer_Mean", "RH_Autumn_Mean",
    "Sol_Annual_Mean", "Sol_Annual_Total", "Sol_Winter_Mean", "Sol_Spring_Mean", "Sol_Summer_Mean", "Sol_Autumn_Mean",
    "UV_Annual_Mean", "UV_Winter_Mean", "UV_Spring_Mean", "UV_Summer_Mean", "UV_Autumn_Mean",
    "Cld_Annual_Mean", "Cld_Winter_Mean", "Cld_Spring_Mean", "Cld_Summer_Mean", "Cld_Autumn_Mean",
    "DM_Aridity_Annual", "PET_Hargreaves_Annual", "UNEP_Aridity_Annual", "Water_Deficit_Annual", "Dry_Months_Count",
]


OM_BASE = "https://archive-api.open-meteo.com/v1/archive"

OM_DAILY_BY_MODULE = {
    "Temperature": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min"],
    "Precipitation": ["precipitation_sum"],
    "Climate_Models": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "Drought & Aridity": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "Wind": ["wind_direction_10m_dominant"],
    "Solar Radiation": ["shortwave_radiation_sum"],
    "UV Index": ["uv_index_max"],
}
OM_HOURLY_BY_MODULE = {
    "Sea Level Pressure": ["pressure_msl"],
    "Surface Pressure": ["surface_pressure"],
    "Temperature": ["relative_humidity_2m"],
    "Climate_Models": ["relative_humidity_2m"],
    "Wind": ["wind_speed_10m"],
    "Relative Humidity": ["relative_humidity_2m"],
    "Cloud Cover": ["cloud_cover"],
}
# canonical monthly keys produced for each module (mirrors NASA parameter names)
OM_CANON = {
    "temperature_2m_mean": "T2M", "temperature_2m_max": "T2M_MAX",
    "temperature_2m_min": "T2M_MIN", "precipitation_sum": "PRECTOTCORR",
    "wind_speed_10m": "WS10M", "wind_direction_10m_dominant": "WD10M",
    "pressure_msl": "SLP", "surface_pressure": "PS",
    "relative_humidity_2m": "RH2M", "shortwave_radiation_sum": "ALLSKY_SFC_SW_DWN",
    "uv_index_max": "ALLSKY_SFC_UV_INDEX", "cloud_cover": "CLOUD_AMT",
}
OM_SUM_VARS = ("precipitation_sum",)


def om_var_sets(modules):
    """Daily + hourly Open-Meteo variable lists for the selected modules."""
    daily, hourly = [], []
    for m in modules:
        for v in OM_DAILY_BY_MODULE.get(m, []):
            if v not in daily:
                daily.append(v)
        for v in OM_HOURLY_BY_MODULE.get(m, []):
            if v not in hourly:
                hourly.append(v)
    return daily, hourly


def om_model_slug(model_text):
    s = str(model_text or "").lower()
    if "land" in s:
        return "era5_land"
    elif "seamless" in s:
        return "era5_seamless"
    elif "era5" in s:
        return "era5"
    return "era5_land"


def om_url(lat, lon, y0, y1, daily_vars, hourly_vars, model="era5_land", start_date=None, end_date=None):
    if not start_date:
        start_date = "%d-01-01" % y0
    if not end_date:
        end_date = "%d-12-31" % y1
    q = ("latitude=%s&longitude=%s&start_date=%s&end_date=%s&timezone=UTC"
         % (repr(float(lat)), repr(float(lon)), str(start_date), str(end_date)))
    if daily_vars:
        q += "&daily=" + ",".join(daily_vars)
    if hourly_vars:
        q += "&hourly=" + ",".join(hourly_vars)
    if model:
        q += "&models=" + om_model_slug(model)
    return OM_BASE + "?" + q


def om_group_daily(dates, values, mode="mean"):
    """dates: [YYYY-MM-DD], values: [...] -> {(y,m): aggregated} skipping nulls."""
    by_month = {}
    for d, v in zip(dates or [], values or []):
        if v is None:
            continue
        try:
            f = float(v)
        except Exception:
            continue
        if f != f:  # NaN
            continue
        try:
            ym = (int(d[0:4]), int(d[5:7]))
        except Exception:
            continue
        by_month.setdefault(ym, []).append(f)
    out = {}
    for ym, vals in by_month.items():
        if not vals:
            continue
        out[ym] = sum(vals) if mode == "sum" else sum(vals) / len(vals)
    return out


def om_group_hourly(times, values):
    """times: [YYYY-MM-DDTHH:MM], values -> {(y,m): mean} skipping nulls."""
    by_month = {}
    for t, v in zip(times or [], values or []):
        if v is None:
            continue
        try:
            f = float(v)
        except Exception:
            continue
        if f != f:
            continue
        try:
            ym = (int(t[0:4]), int(t[5:7]))
        except Exception:
            continue
        by_month.setdefault(ym, []).append(f)
    out = {}
    for ym, vals in by_month.items():
        if vals:
            out[ym] = sum(vals) / len(vals)
    return out


def probe_server(provider, lat, lon, year, n_pts, timeout=30, model="era5_land",
                 start_date=None, end_date=None):
    """Fail-fast connectivity check: one minimal request before the full loop.

    Raises RuntimeError with a clear cause so the run aborts in seconds instead
    of downloading for an hour into empty outputs."""
    try:
        if provider.startswith("Open-Meteo"):
            fetch_openmeteo_point(lat, lon, year, year, ["Temperature"],
                                  timeout=timeout, retries=1, model=model,
                                  start_date=start_date, end_date=end_date)
        else:
            fetch_nasa_point(lat, lon, year, year, ["T2M"], temporal="Monthly",
                             timeout=timeout, retries=1,
                             start_date=start_date, end_date=end_date)
    except Exception as ex:
        raise RuntimeError(
            "Server connectivity check failed (%s): %s. Check the internet "
            "connection, firewall/proxy settings, and that the service is online, "
            "then re-run for the %d points." % (provider, ex, n_pts))


def om_drop_vars_from_reason(reason, daily_vars, hourly_vars):
    """Remove variables named in an API error; returns (daily, hourly, dropped)."""
    r = str(reason or "")
    dropped = []
    daily = [v for v in daily_vars if v not in r or not _mark_dropped(v, dropped)]
    hourly = [v for v in hourly_vars if v not in r or not _mark_dropped(v, dropped)]
    return daily, hourly, dropped


def _mark_dropped(v, dropped):
    dropped.append(v)
    return True


def om_parse_response(data, daily_vars, hourly_vars):
    """Map an Open-Meteo response to canonical monthly dicts + daily precip."""
    monthly, daily_raw = {}, {}
    daily = data.get("daily", {}) or {}
    hourly = data.get("hourly", {}) or {}
    dates = daily.get("time", []) or []
    for v in daily_vars:
        canon = OM_CANON.get(v, v)
        mode = "sum" if v in OM_SUM_VARS else "mean"
        monthly[canon] = om_group_daily(dates, daily.get(v, []), mode)
    htimes = hourly.get("time", []) or []
    for v in hourly_vars:
        canon = OM_CANON.get(v, v)
        monthly[canon] = om_group_hourly(htimes, hourly.get(v, []))
    if "precipitation_sum" in daily_vars:
        praw = {}
        for d, val in zip(dates, daily.get("precipitation_sum", []) or []):
            if val is None:
                continue
            try:
                f = float(val)
            except Exception:
                continue
            if f == f:
                try:
                    praw[(int(d[0:4]), int(d[5:7]), int(d[8:10]))] = f
                except Exception:
                    pass
        daily_raw["PRECTOTCORR"] = praw
    return monthly, daily_raw


def fetch_openmeteo_point(lat, lon, y0, y1, modules, timeout=60, retries=3,
                          daily_vars=None, hourly_vars=None, model="era5_land",
                          start_date=None, end_date=None):
    """Returns (monthly, daily_raw, dropped_vars). Raises RuntimeError after retries."""
    if daily_vars is None or hourly_vars is None:
        daily_vars, hourly_vars = om_var_sets(modules)
    url = om_url(lat, lon, y0, y1, daily_vars, hourly_vars, model=model,
                 start_date=start_date, end_date=end_date)
    last_err = None
    for attempt in range(retries):
        try:
            data = _http_get_json(url, timeout)
            if isinstance(data, dict) and data.get("error"):
                raise RuntimeError("Open-Meteo: %s" % data.get("reason", data))
            _m, _d = om_parse_response(data, daily_vars, hourly_vars)
            return _m, _d, []
        except Exception as ex:
            last_err = ex
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError("Open-Meteo request failed: %s" % last_err)


def om_probe_vars(modules, timeout=30, model="era5_land", start_date=None, end_date=None):
    """One tiny request to verify variable availability; drops rejected vars.

    Returns (daily_vars, hourly_vars, dropped, note). Never raises."""
    daily_vars, hourly_vars = om_var_sets(modules)
    if not daily_vars and not hourly_vars:
        return daily_vars, hourly_vars, [], ""
    url = om_url(30.0, 31.0, 2020, 2020, daily_vars, hourly_vars, model=model,
                 start_date=(start_date if start_date else "2020-01-01"),
                 end_date=(end_date if end_date else "2020-01-10"))
    try:
        data = _http_get_json(url, timeout)
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(str(data.get("reason", data)))
        return daily_vars, hourly_vars, [], ""
    except Exception as ex:
        daily2, hourly2, dropped = om_drop_vars_from_reason(ex, daily_vars, hourly_vars)
        # last resort: core daily set only
        if not daily2 and not hourly2:
            daily2 = [v for v in daily_vars
                      if v in ("temperature_2m_mean", "temperature_2m_max",
                               "temperature_2m_min", "precipitation_sum",
                               "shortwave_radiation_sum", "wind_direction_10m_dominant")]
            dropped = [v for v in daily_vars + hourly_vars if v not in daily2]
        note = "Open-Meteo rejected variables %s (%s); affected fields will be NoData." % (
            dropped or ["?"], ex)
        return daily2, hourly2, dropped, note


def compute_point_fields(monthly, years, modules, temporal, daily_raw=None,
                         precip_totals=False, gap_method="climatological", lat=0.0):
    """Core per-point computation. monthly: {param: {(y,m): v}}.
    precip_totals=True when monthly PRECTOTCORR values are already totals
    (NASA daily mode, Open-Meteo); False only for NASA monthly rates (mm/day).
    gap_method: 'climatological' | 'linear' | 'none' for interior missing
    months of mean-type variables (never precipitation sums, never wind
    direction)."""
    _FILLABLE = ("T2M", "T2M_MAX", "T2M_MIN", "RH2M", "ALLSKY_SFC_SW_DWN",
                 "ALLSKY_SFC_UV_INDEX", "CLOUD_AMT", "SLP", "PS", "WS10M")
    if gap_method != "none":
        monthly = dict((k, fill_interior_gaps(v, gap_method) if k in _FILLABLE else v)
                       for k, v in monthly.items())
    res = {}
    if "Temperature" in modules:
        res.update(compute_temperature_fields(
            monthly.get("T2M", {}), monthly.get("T2M_MAX", {}),
            monthly.get("T2M_MIN", {}), monthly.get("RH2M", {})))
    if "Precipitation" in modules:
        raw = monthly.get("PRECTOTCORR", {})
        if temporal == "Monthly" and not precip_totals:
            totals = {}
            for ym, v in raw.items():
                totals[ym] = monthly_precip_total_from_rate(v, ym[0], ym[1])
        else:
            totals = dict(raw)  # already summed per month
        agg = seasonal_totals_from_monthly_totals(totals, years)
        clim_m = climat_monthly_means(totals)
        clim_vals = [v for v in clim_m.values() if v is not None]
        res["R_Annual_Total"] = agg["Annual_Mean"]
        res["R_Annual_Mean"] = (sum(clim_vals) / len(clim_vals)) if clim_vals else None
        res["R_Winter_Total"] = agg["Winter"]
        res["R_Spring_Total"] = agg["Spring"]
        res["R_Summer_Total"] = agg["Summer"]
        res["R_Autumn_Total"] = agg["Autumn"]
        if temporal == "Daily" and daily_raw and "PRECTOTCORR" in daily_raw:
            dv = [float(v) for v in daily_raw["PRECTOTCORR"].values() if not is_missing(v)]
            res["R_Max_Daily_Month"] = max(dv) if dv else None
            by_year = {}
            for ymd, v in daily_raw["PRECTOTCORR"].items():
                if is_missing(v):
                    continue
                by_year.setdefault(ymd[0], 0)
                if float(v) >= 1.0:
                    by_year[ymd[0]] += 1
            counts = [c for y, c in by_year.items() if y in years] or by_year.values()
            res["R_Annual_Rain_Days_Total"] = (sum(counts) / float(len(counts))) if counts else None
        else:
            res["R_Max_Daily_Month"] = None
            res["R_Annual_Rain_Days_Total"] = None
    if "Drought & Aridity" in modules or "Climate_Models" in modules:
        raw_p = monthly.get("PRECTOTCORR", {})
        if temporal == "Monthly" and not precip_totals:
            totals_p = {}
            for ym, v in raw_p.items():
                totals_p[ym] = monthly_precip_total_from_rate(v, ym[0], ym[1])
        else:
            totals_p = dict(raw_p)
        res.update(compute_drought_fields(
            monthly.get("T2M", {}), monthly.get("T2M_MAX", {}),
            monthly.get("T2M_MIN", {}), totals_p, lat=lat))
        if "Climate_Models" in modules:
            c_t = climat_monthly_means(monthly.get("T2M", {}))
            c_rh = climat_monthly_means(monthly.get("RH2M", {}))
            hi_m = dict((m, heat_index_c(c_t.get(m), c_rh.get(m))) for m in range(1, 13))
            hi_vals = [v for v in hi_m.values() if v is not None]
            hi_sum = [hi_m[m] for m in SEASONS["Summer"] if hi_m.get(m) is not None]
            res["HI_Annual_Mean"] = sum(hi_vals) / len(hi_vals) if hi_vals else None
            res["HI_Summer_Mean"] = sum(hi_sum) / len(hi_sum) if hi_sum else None
    if "Sea Level Pressure" in modules:
        conv = dict((ym, pressure_kpa_to_mbar(v)) for ym, v in monthly.get("SLP", {}).items())
        s = seasonal_means_from_monthly(conv)
        res.update({"PSL_Annual_Mean": s["Annual"], "PSL_Winter_Mean": s["Winter"],
                    "PSL_Spring_Mean": s["Spring"], "PSL_Summer_Mean": s["Summer"],
                    "PSL_Autumn_Mean": s["Autumn"],
                    "PSL_Annual_Range": monthly_range(conv)})
    if "Surface Pressure" in modules:
        conv = dict((ym, pressure_kpa_to_mbar(v)) for ym, v in monthly.get("PS", {}).items())
        s = seasonal_means_from_monthly(conv)
        res.update({"PS_Annual_Mean": s["Annual"], "PS_Winter_Mean": s["Winter"],
                    "PS_Spring_Mean": s["Spring"], "PS_Summer_Mean": s["Summer"],
                    "PS_Autumn_Mean": s["Autumn"],
                    "PS_Annual_Range": monthly_range(conv)})
    if "Wind" in modules:
        res.update(compute_wind_fields(monthly.get("WS10M", {}), monthly.get("WD10M", {})))
    if "Relative Humidity" in modules:
        s = seasonal_means_from_monthly(monthly.get("RH2M", {}))
        res.update({"RH_Annual_Mean": s["Annual"], "RH_Winter_Mean": s["Winter"],
                    "RH_Spring_Mean": s["Spring"], "RH_Summer_Mean": s["Summer"],
                    "RH_Autumn_Mean": s["Autumn"]})
    if "Solar Radiation" in modules:
        res.update(compute_solar_fields(monthly.get("ALLSKY_SFC_SW_DWN", {}), years))
    if "UV Index" in modules:
        s = seasonal_means_from_monthly(monthly.get("ALLSKY_SFC_UV_INDEX", {}))
        res.update({"UV_Annual_Mean": s["Annual"], "UV_Winter_Mean": s["Winter"],
                    "UV_Spring_Mean": s["Spring"], "UV_Summer_Mean": s["Summer"],
                    "UV_Autumn_Mean": s["Autumn"]})
    if "Cloud Cover" in modules:
        s = seasonal_means_from_monthly(monthly.get("CLOUD_AMT", {}))
        res.update({"Cld_Annual_Mean": s["Annual"], "Cld_Winter_Mean": s["Winter"],
                    "Cld_Spring_Mean": s["Spring"], "Cld_Summer_Mean": s["Summer"],
                    "Cld_Autumn_Mean": s["Autumn"]})
    return res


# ---------------------------------------------------------------------------
# Toolbox definition (ArcMap 10.x Python toolbox API)
# ---------------------------------------------------------------------------

class Toolbox(object):
    """POWER Climate Atlas (ArcMap 10.x).

    Professional climate-atlas toolbox: downloads gridded climate data for user
    point features (NASA POWER API or Open-Meteo ERA5 reanalysis), computes
    annual/seasonal indicators with correct units, and packages everything as a
    documented atlas (points, clipped rasters, layer files, dictionaries, log).
    """

    def __init__(self):
        self.label = "POWER Climate Atlas (ArcMap 10.x)"
        self.alias = "powerAtlas10"
        self.tools = [PowerClimateAtlasGenerator]
        if RasterDataClimateAtlasGenerator:
            self.tools.append(RasterDataClimateAtlasGenerator)


class PowerClimateAtlasGenerator(object):
    """POWER Climate Atlas Generator — builds a documented climate atlas package.

    WHAT IT DOES (3 stages, sequential and memory-safe on 32-bit ArcMap):
      1. FETCH: queries the selected Climate Data Source for every input point
         (WGS 84 coordinates extracted internally) with retries and an in-run
         cache; failed points are logged, never aborting the run.
      2. COMPUTE: annual/seasonal indicators per module with correct physics:
         temperature means and annual range (max-min monthly mean), precipitation
         accumulated totals (rate x days-in-month for NASA monthly), pressure
         converted to mbar/hPa, wind direction by circular (vector) mean, solar
         MJ/m2/day converted to kWh (mean vs annual total distinguished), UV and
         cloud means. Missing NASA sentinels (-999) are excluded everywhere.
      3. BUILD: per-element point layers (GDB + shapefile + CSV each), interpolated and
         study-area-clipped raw float rasters (GeoTIFF, LZW), classified display
         layer files with embedded metadata plus .lyr.json classification sidecars,
         thinned wind arrow layers, optional PSL isobars, bilingual
         (Arabic/English) data dictionaries and a full processing log with QA.

    DATA SOURCES: 'NASA POWER API' (gridded POWER climatology, ~0.5 deg native)
    or 'Open-Meteo Historical API (ERA5 Reanalysis)' (ERA5, ~0.25 deg native;
    daily + hourly aggregates auto-mapped to the same fields and standards).

    OUTPUT LAYOUT (fixed, per-module folders 01..09 plus 00_Vector_Data,
    10_Derived_Models and Project_Data.gdb): see the Processing_Log.txt written
    next to every run for the exact file list, warnings and QA results.

    SCIENTIFIC NOTES: source data are modelled estimates, not station
    measurements; interpolated cell size is cartographic and never equals native
    climate resolution; wind direction needs the circular mean; precipitation is
    a sum while temperature is a mean; PSL and PS are different products.

    PERFORMANCE: test on a few points first (Monthly, one module, one year);
    national extents need kilometre-scale cells (e.g. 5000 m), never metres-scale
    cells; unclipped intermediates are purged automatically when requested.
    """

    def __init__(self):
        self.label = "POWER Climate Atlas Generator (v1.1)"
        self.description = (
            "Fetch NASA POWER climate data for point features, compute annual/seasonal "
            "indicators with correct units, and build an organized atlas package: "
            "per-element point layers (GDB/SHP/CSV each), interpolated clipped rasters (GeoTIFF), "
            "classified .lyr layer files, wind vector layers, optional PSL isobars, bilingual "
            "data dictionaries and a processing log. For ArcMap 10.x, .lyr files are the "
            "equivalent of ArcGIS Pro .lyrx files. NASA POWER data are gridded/modelled "
            "estimates, not in-situ station measurements; interpolated cell size is a "
            "cartographic choice, not native climate resolution.")
        self.canRunInBackground = True
        self._last_subs = []

    # ---------------- parameters ----------------
    def getParameterInfo(self):
        p_op_mode = arcpy.Parameter(
            displayName="Operation Mode",
            name="Operation_Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p_op_mode.filter.type = "ValueList"
        p_op_mode.filter.list = [
            "Download & Generate Atlas (Full Pipeline) [Default]",
            "Interpolate & Map Existing Data (Offline Mode - No Internet)"
        ]
        p_op_mode.value = "Download & Generate Atlas (Full Pipeline) [Default]"
        p_op_mode.description = (
            "REQUIRED. Choose operation mode:\n"
            "'Download & Generate Atlas (Full Pipeline)': Online mode. Queries climate data for input points, "
            "computes indicators, builds feature classes, and interpolates rasters.\n"
            "'Interpolate & Map Existing Data (Offline Mode)': Offline mode. No internet queries. Takes a precalculated "
            "point layer already containing climate fields and directly performs spatial interpolation, masking, "
            "and atlas map generation."
        )

        p0 = arcpy.Parameter(
            displayName="Input Point Features",
            name="Input_Point_Features",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")
        p0.filter.list = ["Point"]
        p0.description = ("REQUIRED for Download mode. Point layer (shapefile or geodatabase feature class). "
                          "Each point is queried against the data source using its WGS 84 "
                          "(EPSG:4326) longitude/latitude.")

        p_precalc = arcpy.Parameter(
            displayName="Precalculated Point Layer(s) (Offline Mode)",
            name="Precalculated_Point_Layers",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")
        p_precalc.multiValue = True
        p_precalc.filter.list = ["Point", "Multipoint"]
        p_precalc.description = (
            "REQUIRED for Offline mode. One or more existing point layers (from GDB or Shapefile) containing "
            "pre-calculated climate attributes. The tool automatically merges them by coordinates/Source_ID."
        )

        p1 = arcpy.Parameter(
            displayName="Study Area Mask (optional polygon)",
            name="Study_Area_Mask",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input")
        p1.filter.list = ["Polygon"]
        p1.description = ("OPTIONAL but recommended. Polygon used to set processing extent/mask, "
                          "clip final rasters, and generate wind vectors/isobars.")

        p12 = arcpy.Parameter(
            displayName="Output Folder Workspace",
            name="Output_Workspace",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        p12.description = ("REQUIRED. Output folder workspace. A File Geodatabase "
                           "'Climate_Database.gdb' is created inside automatically. "
                           "Per-element point layers (Temperature, Precipitation, etc.) "
                           "are stored in the GDB. Existing outputs are overwritten.")

        p2 = arcpy.Parameter(
            displayName="Output Spatial Reference",
            name="Output_Spatial_Reference",
            datatype="GPSpatialReference",
            parameterType="Optional",
            direction="Input")
        p2.description = ("OPTIONAL. Target coordinate system for all outputs. "
                          "DEFAULT: same as input points.")

        p14 = arcpy.Parameter(
            displayName="Climate Data Source",
            name="Climate_Data_Source",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p14.filter.type = "ValueList"
        p14.filter.list = ["NASA POWER API", "Open-Meteo Historical API (ERA5 Reanalysis)"]
        p14.value = "NASA POWER API"
        p14.category = "Data Source"
        p14.description = ("REQUIRED. Data provider for all climate queries. "
                           "'NASA POWER API' (default): gridded POWER climatology. "
                           "'Open-Meteo Historical API (ERA5 Reanalysis)': ERA5 reanalysis.")

        p_om_model = arcpy.Parameter(
            displayName="Open-Meteo Reanalysis Model",
            name="OpenMeteo_Model",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_om_model.filter.type = "ValueList"
        p_om_model.filter.list = [
            "ERA5-Land (Highest Resolution ~9 km / 0.1 deg) [Recommended]",
            "ERA5-Seamless (Combined 9-25 km / 0.1-0.25 deg)",
            "ERA5 (Standard Reanalysis ~25 km / 0.25 deg)"
        ]
        p_om_model.value = "ERA5-Land (Highest Resolution ~9 km / 0.1 deg) [Recommended]"
        p_om_model.category = "Data Source"
        p_om_model.description = ("OPEN-METEO ONLY. Atmospheric reanalysis model. "
                                  "'ERA5-Land' (default, recommended): highest spatial resolution (~9 km / 0.1 deg). "
                                  "'ERA5-Seamless': combined high-resolution model. "
                                  "'ERA5': standard global reanalysis (~25 km / 0.25 deg).")

        # ═══ Time Window ═══
        p3 = arcpy.Parameter(
            displayName="Time Mode",
            name="Time_Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p3.filter.type = "ValueList"
        p3.filter.list = ["Single Year", "Year Range", "Custom Date Range"]
        p3.value = "Single Year"
        p3.category = "Time Window"
        p3.description = ("REQUIRED. 'Single Year' queries January-December of one year. "
                          "'Year Range' computes multi-year climatological normals. "
                          "'Custom Date Range' queries specific start/end dates via calendar or text.")

        p4 = arcpy.Parameter(
            displayName="Single Year",
            name="Single_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p4.filter.type = "ValueList"
        p4.filter.list = [str(y) for y in range(2025, 1980, -1)]
        p4.value = 2024
        p4.category = "Time Window"
        p4.description = "Select or enter the specific year to query (1981 to 2025)."

        p5 = arcpy.Parameter(
            displayName="Start Year",
            name="Start_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p5.filter.type = "ValueList"
        p5.filter.list = [str(y) for y in range(1981, 2026)]
        p5.value = 2015
        p5.category = "Time Window"
        p5.description = "First year of the climatology period (inclusive)."

        p6 = arcpy.Parameter(
            displayName="End Year",
            name="End_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p6.filter.type = "ValueList"
        p6.filter.list = [str(y) for y in range(1981, 2026)]
        p6.value = 2024
        p6.category = "Time Window"
        p6.description = "Last year of the climatology period (inclusive)."

        p_picker = arcpy.Parameter(
            displayName="Launch Visual Calendar Window (نافذة التقويم الذكية)",
            name="Open_Calendar_Picker",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p_picker.value = False
        p_picker.category = "Time Window"
        p_picker.description = ("CUSTOM DATE ONLY. Check this box to open the calm, interactive visual calendar "
                                "dialog with month navigation arrows and quick year/month selectors.")

        p_start_date = arcpy.Parameter(
            displayName="Start Date (DD/MM/YYYY or YYYY-MM-DD)",
            name="Start_Date",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_start_date.value = "01/01/2024"
        p_start_date.category = "Time Window"
        p_start_date.description = ("CUSTOM DATE RANGE ONLY. Beginning date. "
                                    "Type directly in the box (e.g. 31/3/1990 or 1990-03-31) "
                                    "or use the Visual Calendar Window above.")

        p_end_date = arcpy.Parameter(
            displayName="End Date (DD/MM/YYYY or YYYY-MM-DD)",
            name="End_Date",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_end_date.value = "31/12/2024"
        p_end_date.category = "Time Window"
        p_end_date.description = ("CUSTOM DATE RANGE ONLY. Ending date. "
                                  "Type directly in the box (e.g. 31/12/2000 or 2000-12-31) "
                                  "or use the Visual Calendar Window above.")

        p7 = arcpy.Parameter(
            displayName="Temporal Resolution",
            name="Temporal_Resolution",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p7.filter.type = "ValueList"
        p7.filter.list = ["Monthly", "Daily"]
        p7.value = "Monthly"
        p7.category = "Time Window"
        p7.description = ("REQUIRED. Monthly (recommended): faster, uses monthly means/rates. "
                          "Daily: detailed, required for max daily rainfall / extremes.")

        p_gf = arcpy.Parameter(
            displayName="Gap Fill Method",
            name="Gap_Fill_Method",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_gf.filter.type = "ValueList"
        p_gf.filter.list = [
            "Climatological Month Mean (Recommended)",
            "Linear + Boundary Interpolation",
            "Spatial Nearest Neighbor Fallback",
            "No Fill (skip missing)"
        ]
        p_gf.value = "Climatological Month Mean (Recommended)"
        p_gf.category = "Time Window"
        p_gf.description = ("OPTIONAL. How to handle missing months or stations (NoData/-999). "
                            "'Climatological Month Mean' (recommended): fills gaps with the average "
                            "of the same calendar month across years, with station mean fallback. "
                            "'Linear + Boundary Interpolation': fills interior gaps linearly and "
                            "endpoints using boundary fill. 'Spatial Nearest Neighbor Fallback': "
                            "estimates missing fields from nearest valid spatial stations. "
                            "'No Fill': ignores missing values.")

        p_dl = arcpy.Parameter(
            displayName="Download & Save Point Data Only (Skip Rasters & Atlas)",
            name="Download_Only",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p_dl.value = False
        p_dl.category = "Time Window"
        p_dl.description = ("OPTIONAL (default OFF). When checked, the tool downloads climate data and saves "
                            "complete point feature classes (GDB, SHP, CSV) for each element, but skips "
                            "surface interpolation, raster creation, contours, and layer styling.")

        p8 = arcpy.Parameter(
            displayName="Climate Modules & Models",
            name="Climate_Modules",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p8.multiValue = True
        p8.filter.type = "ValueList"
        p8.filter.list = MODULES_ALL
        p8.value = "Temperature"
        p8.category = "Climate Modules & Models"
        p8.description = (
            "Select primary climate modules and applied bioclimatic models to compute and export. "
            "Submodels (De Martonne, Hargreaves PET, UNEP, Water Deficit, Walter-Lieth, Heat Index) "
            "are located at the bottom of the list and can be selected directly; prerequisite variables "
            "are retrieved automatically if not selected."
        )

        # ═══ Variable & Field Selection ═══
        p_sel_fields = arcpy.Parameter(
            displayName="Variables Selection (Checklist)",
            name="Selected_Fields",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_sel_fields.multiValue = True
        p_sel_fields.filter.type = "ValueList"
        init_cands = get_candidate_fields(["Temperature"])
        p_sel_fields.filter.list = [c[1] for c in init_cands]
        p_sel_fields.value = ";".join([c[1] for c in init_cands])
        p_sel_fields.category = "Variable & Field Selection"
        p_sel_fields.description = (
            "VARIABLES SELECTION. Interactive checklist of climate variables and indicators to compute. "
            "All fields for the selected Climate Modules are included by default. "
            "Check or uncheck individual variables as needed, or use the Filter Scope below to filter by seasons/periods."
        )

        p_filter_scope = arcpy.Parameter(
            displayName="Field Filter Scope",
            name="Field_Filter_Scope",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p_filter_scope.filter.type = "ValueList"
        p_filter_scope.filter.list = [
            "All Variables & Fields (Full Suite) [Recommended]",
            "Filter by Seasons & Aggregations",
            "Custom Field Checklist"
        ]
        p_filter_scope.value = "All Variables & Fields (Full Suite) [Recommended]"
        p_filter_scope.category = "Variable & Field Selection"
        p_filter_scope.description = (
            "REQUIRED. Controls which variables, seasons, and indicators are computed and exported. "
            "'All Variables & Fields (Full Suite)' (default): calculates and maps all annual, seasonal and extreme fields. "
            "'Filter by Seasons & Aggregations': quickly filter by specific season (e.g. Summer only, Winter only) or period. "
            "'Custom Field Checklist': interactive checklist table above to select/unselect exact fields by name."
        )

        p_inc_aggs = arcpy.Parameter(
            displayName="Included Summary Periods",
            name="Included_Aggregations",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_inc_aggs.multiValue = True
        p_inc_aggs.filter.type = "ValueList"
        p_inc_aggs.filter.list = [
            "Annual Summaries",
            "Seasonal Summaries",
            "Extreme & Bioclimatic Indices"
        ]
        p_inc_aggs.value = "Annual Summaries;Seasonal Summaries;Extreme & Bioclimatic Indices"
        p_inc_aggs.category = "Variable & Field Selection"
        p_inc_aggs.description = (
            "PERIOD FILTER ONLY. Choose summary levels to generate. "
            "'Annual Summaries': annual means and totals. "
            "'Seasonal Summaries': seasonal means and totals (Winter, Spring, Summer, Autumn). "
            "'Extreme & Bioclimatic Indices': heat index, ranges, extreme months, rain days."
        )

        p_inc_seasons = arcpy.Parameter(
            displayName="Included Seasons",
            name="Included_Seasons",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_inc_seasons.multiValue = True
        p_inc_seasons.filter.type = "ValueList"
        p_inc_seasons.filter.list = [
            "Winter (DJF)",
            "Spring (MAM)",
            "Summer (JJA)",
            "Autumn (SON)"
        ]
        p_inc_seasons.value = "Winter (DJF);Spring (MAM);Summer (JJA);Autumn (SON)"
        p_inc_seasons.category = "Variable & Field Selection"
        p_inc_seasons.description = (
            "SEASONS FILTER ONLY. Select which seasons to generate. "
            "Uncheck any season you do not need (e.g. keep only Summer or only Winter)."
        )

        # ═══ Interpolation Parameters ═══
        p11 = arcpy.Parameter(
            displayName="Interpolation Method",
            name="Interpolation_Method",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        p11.filter.type = "ValueList"
        p11.filter.list = ["IDW", "Ordinary Kriging", "Spline", "Natural Neighbor"]
        p11.value = "IDW"
        p11.category = "Interpolation Parameters"
        p11.description = ("REQUIRED. IDW (default) | Ordinary Kriging | Spline | Natural Neighbor. "
                           "Requires Spatial Analyst.")

        p_idw_prof = arcpy.Parameter(
            displayName="IDW Curve Profile",
            name="IDW_Curve_Profile",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_idw_prof.filter.type = "ValueList"
        p_idw_prof.filter.list = [
            "Gentle / Smooth (Power 1.2)",
            "Standard Quadratic (Power 2.0)",
            "Regional Broad (Power 0.7)",
            "Custom Power"
        ]
        p_idw_prof.value = "Gentle / Smooth (Power 1.2)"
        p_idw_prof.category = "Interpolation Parameters"
        p_idw_prof.description = ("IDW ONLY. Distance decay curve profile. 'Gentle / Smooth' (power 1.2) "
                                  "eliminates concentric island/bullseye artifacts. 'Standard' (power 2.0) "
                                  "is the classical steep quadratic decay. 'Regional Broad' (power 0.7) "
                                  "gives extended regional smoothing. 'Custom Power' allows typing an arbitrary power.")

        p15 = arcpy.Parameter(
            displayName="IDW Power",
            name="IDW_Power",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        p15.value = 1.2
        p15.category = "Interpolation Parameters"
        p15.description = "IDW ONLY. Power parameter. DEFAULT 1.2 for smooth, seamless climate surfaces without artificial bullseyes."

        p16 = arcpy.Parameter(
            displayName="IDW Search Radius Type",
            name="IDW_Search_Type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p16.filter.type = "ValueList"
        p16.filter.list = ["Variable", "Fixed"]
        p16.value = "Variable"
        p16.category = "Interpolation Parameters"
        p16.description = "IDW ONLY. 'Variable' (default): expand search. 'Fixed': fixed radius."

        p17 = arcpy.Parameter(
            displayName="IDW Number of Points",
            name="IDW_Num_Points",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p17.value = 12
        p17.category = "Interpolation Parameters"
        p17.description = "IDW ONLY. Number of neighbouring points. DEFAULT 12."

        p18 = arcpy.Parameter(
            displayName="IDW Maximum Distance (metres, optional)",
            name="IDW_Max_Distance",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        p18.category = "Interpolation Parameters"
        p18.description = "IDW ONLY, OPTIONAL. Caps the search neighbourhood in metres."

        p19 = arcpy.Parameter(
            displayName="Kriging Semivariogram Model",
            name="Krig_Model",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p19.filter.type = "ValueList"
        p19.filter.list = ["Spherical", "Circular", "Exponential", "Gaussian"]
        p19.value = "Spherical"
        p19.category = "Interpolation Parameters"
        p19.description = "KRIGING ONLY. DEFAULT Spherical."

        p20 = arcpy.Parameter(
            displayName="Kriging Type",
            name="Krig_Type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p20.filter.type = "ValueList"
        p20.filter.list = ["Ordinary", "Universal"]
        p20.value = "Ordinary"
        p20.category = "Interpolation Parameters"
        p20.description = "KRIGING ONLY. 'Ordinary' (default) or 'Universal'."

        p21 = arcpy.Parameter(
            displayName="Kriging Number of Points",
            name="Krig_Num_Points",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p21.value = 12
        p21.category = "Interpolation Parameters"
        p21.description = "KRIGING ONLY. DEFAULT 12."

        p_sp_type = arcpy.Parameter(
            displayName="Spline Type",
            name="Spline_Type",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p_sp_type.filter.type = "ValueList"
        p_sp_type.filter.list = ["Tension", "Regularized"]
        p_sp_type.value = "Tension"
        p_sp_type.category = "Interpolation Parameters"
        p_sp_type.description = ("SPLINE ONLY. 'Tension' (recommended for climate): produces taut, smooth "
                                 "surfaces that honor exact point values without overshoots. 'Regularized': "
                                 "smooth surface that may overshoot local extremes.")

        p_sp_weight = arcpy.Parameter(
            displayName="Spline Weight",
            name="Spline_Weight",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        p_sp_weight.value = 5.0
        p_sp_weight.category = "Interpolation Parameters"
        p_sp_weight.description = ("SPLINE ONLY. Weight parameter. For Tension Spline, higher weights (e.g. 5.0-10.0) "
                                   "produce stiffer, less smoothed surfaces closely matching points; smaller weights "
                                   "produce smoother surfaces. DEFAULT 5.0.")

        p_sp_pts = arcpy.Parameter(
            displayName="Spline Number of Points",
            name="Spline_Num_Points",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p_sp_pts.value = 12
        p_sp_pts.category = "Interpolation Parameters"
        p_sp_pts.description = "SPLINE ONLY. Number of neighbouring points used for interpolation. DEFAULT 12."

        p9 = arcpy.Parameter(
            displayName="Base Cell Size (Meters)",
            name="Base_Cell_Size",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input")
        p9.value = "5000 Meters"
        p9.category = "Interpolation Parameters"
        p9.description = ("REQUIRED. Cell size for all rasters in Meters or Kilometers. "
                          "Default: 5000 Meters. NOTE: fine cells improve appearance only; "
                          "native NASA POWER resolution stays coarse (~0.5 deg).")

        p10 = arcpy.Parameter(
            displayName="Wind Factor Cell Size (Meters)",
            name="Wind_Factor_Cell_Size",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input")
        p10.value = "20000 Meters"
        p10.category = "Interpolation Parameters"
        p10.description = ("REQUIRED. Independent coarser spacing for wind arrow points "
                           "in Meters or Kilometers. Default: 20000 Meters. "
                           "Enabled only when Wind module is selected.")

        # ═══ Pressure Contour ═══
        p13 = arcpy.Parameter(
            displayName="Create PSL Isobar Contour (Optional)",
            name="Create_Isobars",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p13.value = False
        p13.category = "Pressure Contour"
        p13.description = ("OPTIONAL. Creates isobar polylines from pressure rasters "
                           "when a pressure module is selected.")

        p31 = arcpy.Parameter(
            displayName="Pressure Contour Scheme (Optional)",
            name="Pressure_Interval_Scheme",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p31.filter.type = "ValueList"
        p31.filter.list = ["Global Standard (4 mbar)", "Local Detailed (2 mbar)",
                           "Custom Interval"]
        p31.value = "Global Standard (4 mbar)"
        p31.category = "Pressure Contour"
        p31.description = "ISOBARS ONLY. Contour interval preset."

        p32 = arcpy.Parameter(
            displayName="Custom Pressure Step (mbar) (Optional)",
            name="Custom_Pressure_Step",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input")
        p32.value = 4.0
        p32.category = "Pressure Contour"
        p32.description = "ISOBARS ONLY, CUSTOM SCHEME ONLY. Step in mbar/hPa. Must be > 0."

        # ═══ Post-Processing ═══
        p25 = arcpy.Parameter(
            displayName="Apply Focal Smoothing",
            name="Focal_Smoothing",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p25.value = False
        p25.category = "Post-Processing"
        p25.description = "OPTIONAL. Smooths interpolated rasters with Focal Statistics."

        p26 = arcpy.Parameter(
            displayName="Focal Statistic",
            name="Focal_Statistic",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p26.filter.type = "ValueList"
        p26.filter.list = ["MEAN", "MEDIAN", "MINIMUM", "MAXIMUM", "STD"]
        p26.value = "MEAN"
        p26.category = "Post-Processing"
        p26.description = "FOCAL ONLY. DEFAULT MEAN."

        p27 = arcpy.Parameter(
            displayName="Focal Neighborhood (cells)",
            name="Focal_Neighborhood",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")
        p27.value = 3
        p27.category = "Post-Processing"
        p27.description = "FOCAL ONLY. Square neighbourhood in cells (3 = 3x3). DEFAULT 3."

        p24 = arcpy.Parameter(
            displayName="Point Tolerance (0 = off)",
            name="Point_Tolerance",
            datatype="GPLinearUnit",
            parameterType="Optional",
            direction="Input")
        p24.value = "0 Meters"
        p24.category = "Post-Processing"
        p24.description = ("OPTIONAL (default 0 = OFF). Merges points closer than this distance "
                           "before download to reduce interpolation artifacts.")

        # ═══ Map Options ═══
        p23 = arcpy.Parameter(
            displayName="Add Results To Current Map",
            name="Add_To_Map",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p23.value = True
        p23.category = "Map Options"
        p23.description = "OPTIONAL (default ON). Adds final layers to the current ArcMap data frame."

        p28 = arcpy.Parameter(
            displayName="Map Add Modules (elements to add)",
            name="Map_Add_Modules",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p28.multiValue = True
        p28.filter.type = "ValueList"
        p28.filter.list = ["Temperature"]
        p28.value = "Temperature"
        p28.category = "Map Options"
        p28.description = "ADD-TO-MAP ONLY. Choose which elements to add to the map."

        # ═══ Maintenance & Cache ═══
        p22 = arcpy.Parameter(
            displayName="Purge Intermediate Cache",
            name="Purge_Cache",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")
        p22.value = True
        p22.category = "Maintenance & Cache"
        p22.description = ("OPTIONAL (default ON). Deletes intermediate products after use.")

        return [p_op_mode, p0, p_precalc, p1, p12, p2, p14, p_om_model,
                p3, p4, p5, p6, p_picker, p_start_date, p_end_date, p7, p_gf, p_dl,
                p8, p_sel_fields, p_filter_scope, p_inc_aggs, p_inc_seasons,
                p11, p_idw_prof, p15, p16, p17, p18, p19, p20, p21,
                p_sp_type, p_sp_weight, p_sp_pts,
                p9, p10,
                p13, p31, p32,
                p25, p26, p27, p24,
                p23, p28,
                p22]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pdict = dict((p.name, p) for p in parameters)
        p_op = pdict.get("Operation_Mode")
        op_text = p_op.valueAsText if p_op else "Download & Generate Atlas (Full Pipeline) [Default]"
        is_offline = bool(op_text and op_text.startswith("Interpolate & Map Existing Data"))

        p_in = pdict.get("Input_Point_Features") or pdict.get("Input_Points")
        p_pre = pdict.get("Precalculated_Point_Layers") or pdict.get("Precalculated_Point_Layer")
        if p_in:
            p_in.enabled = not is_offline
        if p_pre:
            p_pre.enabled = is_offline

        p_dl = pdict.get("Download_Only")
        dl = bool(p_dl.value) if (p_dl and p_dl.value is not None and not is_offline) else False
        if p_dl:
            p_dl.enabled = not is_offline

        # --- Climate Data Source & Model sync ---
        p_src = pdict.get("Climate_Data_Source")
        if p_src:
            p_src.enabled = not is_offline
        src_text = p_src.valueAsText if p_src else "NASA POWER API"
        use_om = bool(src_text and src_text.startswith("Open-Meteo"))
        if "OpenMeteo_Model" in pdict:
            pdict["OpenMeteo_Model"].enabled = (not is_offline) and use_om

        # --- Time Mode & Date controls ---
        p_mode = pdict.get("Time_Mode") or pdict.get("Time_Range_Mode")
        if p_mode:
            p_mode.enabled = not is_offline
        mode = p_mode.valueAsText if p_mode else "Single Year"
        single = bool(mode and mode.startswith("Single Year"))
        yr_range = bool(mode and mode.startswith("Year Range"))
        custom_range = bool(mode and "Custom Date" in mode)

        # Visual Calendar Picker launch trigger
        p_picker = pdict.get("Open_Calendar_Picker")
        if p_picker and p_picker.value and (not is_offline) and custom_range:
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
            pdict["Single_Year"].enabled = (not is_offline) and single
        if "Start_Year" in pdict:
            pdict["Start_Year"].enabled = (not is_offline) and yr_range
        if "End_Year" in pdict:
            pdict["End_Year"].enabled = (not is_offline) and yr_range
        if "Open_Calendar_Picker" in pdict:
            pdict["Open_Calendar_Picker"].enabled = (not is_offline) and custom_range
        if "Start_Date" in pdict:
            pdict["Start_Date"].enabled = (not is_offline) and custom_range
        if "End_Date" in pdict:
            pdict["End_Date"].enabled = (not is_offline) and custom_range
        if "Temporal_Resolution" in pdict:
            pdict["Temporal_Resolution"].enabled = not is_offline
        if "Gap_Fill_Method" in pdict:
            pdict["Gap_Fill_Method"].enabled = not is_offline

        p_mods = pdict.get("Climate_Modules")

        # --- Precalculated Layer(s) Field Discovery (Offline Mode) ---
        if is_offline and p_pre and p_pre.value:
            try:
                precalc_val = p_pre.valueAsText
                last_precalc = getattr(self, "_last_precalc_layer", None)
                if precalc_val != last_precalc:
                    lyr_paths = [lp.strip().strip("'\"") for lp in (precalc_val or "").split(";") if lp.strip().strip("'\"")]
                    layer_fnames = set()
                    for lp in lyr_paths:
                        try:
                            fld_objs = arcpy.ListFields(lp)
                            for f in fld_objs:
                                layer_fnames.add(f.name)
                                if f.name in REV_SHP_MAP:
                                    layer_fnames.add(REV_SHP_MAP[f.name])
                        except Exception:
                            pass

                    detected_mods = []
                    for m in PRIMARY_MODULES_ALL:
                        m_flds = MODULE_FIELDS.get(m, [])
                        shp_flds = [SHP_FIELD_MAP.get(f, f[:10]) for f in m_flds]
                        if any(f in layer_fnames or sf in layer_fnames for f, sf in zip(m_flds, shp_flds)):
                            detected_mods.append(m)

                    for sub_name, sinfo in SUBMODEL_DEPS.items():
                        req_flds = sinfo.get("fields", [sinfo["field"]])
                        has_out = any(f in layer_fnames for f in req_flds)
                        has_inp = False
                        if "Temperature" in sinfo["modules"] and "Precipitation" in sinfo["modules"]:
                            has_inp = any(f in layer_fnames for f in ("T_Annual_Mean", "T_AnMean", "T2M")) and \
                                      any(f in layer_fnames for f in ("R_Annual_Total", "R_AnnTot", "PRECTOTCORR"))
                        elif "Temperature" in sinfo["modules"] and "Relative Humidity" in sinfo["modules"]:
                            has_inp = any(f in layer_fnames for f in ("T_Summer_Mean", "T_SumMean", "T_Annual_Mean", "T_AnMean", "T2M")) and \
                                      any(f in layer_fnames for f in ("RH_Summer_Mean", "RH_SuMean", "RH_Annual_Mean", "RH_AnMean", "RH2M"))
                        elif "Temperature" in sinfo["modules"]:
                            has_inp = any(f in layer_fnames for f in ("T_Annual_Mean", "T_AnMean", "T2M"))
                        if has_out or has_inp:
                            if sub_name not in detected_mods:
                                detected_mods.append(sub_name)

                    if detected_mods and p_mods and not p_mods.altered:
                        p_mods.value = ";".join(detected_mods)

                    self._last_precalc_layer = precalc_val
            except Exception:
                pass

        # --- Dynamic sync between Climate Modules / Submodels and Map Add Modules ---
        p_map_mods = pdict.get("Map_Add_Modules")
        p_add_map = pdict.get("Add_To_Map")
        mods_text = p_mods.valueAsText if p_mods else ""
        raw_mods = [m.strip().strip("'\"") for m in (mods_text.split(";") if mods_text else []) if m.strip().strip("'\"")]
        map_choices = []
        active_mods = []
        has_sub = False
        for m in raw_mods:
            if resolve_submodel_name(m):
                has_sub = True
                if "Climate_Models" not in active_mods:
                    active_mods.append("Climate_Models")
            else:
                if m not in map_choices:
                    map_choices.append(m)
                if m not in active_mods:
                    active_mods.append(m)
        if has_sub and "Climate_Models" not in map_choices:
            map_choices.append("Climate_Models")
        if not map_choices:
            map_choices = list(PRIMARY_MODULES_ALL) + ["Climate_Models"]

        if p_map_mods:
            p_map_mods.filter.list = map_choices
            last_choices = getattr(self, "_last_map_choices", None)
            if map_choices != last_choices or not p_map_mods.altered:
                p_map_mods.value = ";".join(map_choices)
                self._last_map_choices = list(map_choices)

        # --- Field Filter Scope & Variable/Season controls ---
        p_scope = pdict.get("Field_Filter_Scope")
        scope = p_scope.valueAsText if p_scope else "All Variables & Fields (Full Suite) [Recommended]"
        is_seasons_filter = bool(scope and scope.startswith("Filter by Seasons"))
        is_custom_checklist = bool(scope and scope.startswith("Custom Field"))

        p_aggs = pdict.get("Included_Aggregations")
        p_seas = pdict.get("Included_Seasons")
        p_flds = pdict.get("Selected_Fields")

        if p_aggs:
            p_aggs.enabled = is_seasons_filter or is_custom_checklist

        aggs_val = p_aggs.valueAsText if p_aggs else ""
        has_seasonal = ("Seasonal" in aggs_val) if aggs_val else True

        if p_seas:
            p_seas.enabled = (is_seasons_filter or is_custom_checklist) and has_seasonal

        seas_val = p_seas.valueAsText if p_seas else ""
        active_seasons = [s.strip().strip("'\"") for s in seas_val.split(";") if s.strip().strip("'\"")] if seas_val else None
        active_aggs = [a.strip().strip("'\"") for a in aggs_val.split(";") if a.strip().strip("'\"")] if aggs_val else None

        if p_flds:
            p_flds.enabled = is_custom_checklist
            if is_custom_checklist:
                candidates = get_candidate_fields(active_mods, active_aggs, active_seasons)
                cand_labels = [c[1] for c in candidates]
                p_flds.filter.list = cand_labels
                last_cand_set = getattr(self, "_last_cand_set", None)
                curr_cand_set = tuple(sorted(cand_labels))
                if curr_cand_set != last_cand_set:
                    if p_flds.valueAsText:
                        old_items = [x.strip().strip("'\"") for x in p_flds.valueAsText.split(";") if x.strip().strip("'\"")]
                        retained = [x for x in old_items if x in cand_labels]
                        if retained:
                            p_flds.value = ";".join(retained)
                        else:
                            p_flds.value = ";".join(cand_labels)
                    else:
                        p_flds.value = ";".join(cand_labels)
                    self._last_cand_set = curr_cand_set
            elif is_seasons_filter:
                candidates = get_candidate_fields(active_mods, active_aggs, active_seasons)
                cand_labels = [c[1] for c in candidates]
                p_flds.filter.list = cand_labels
                p_flds.value = ";".join(cand_labels)
            else:
                candidates = get_candidate_fields(active_mods)
                cand_labels = [c[1] for c in candidates]
                p_flds.filter.list = cand_labels
                last_mods_all = getattr(self, "_last_mods_all", None)
                curr_mods_all = tuple(sorted(active_mods))
                if curr_mods_all != last_mods_all:
                    p_flds.value = ";".join(cand_labels)
                    self._last_mods_all = curr_mods_all

        # --- Dynamic interpolation panel ---
        p_meth = pdict.get("Interpolation_Method")
        meth = p_meth.valueAsText if p_meth else "IDW"
        is_idw = (meth == "IDW")
        is_krig = (meth == "Ordinary Kriging")
        is_spline = (meth == "Spline")

        # Sync IDW Curve Profile with IDW Power
        p_prof = pdict.get("IDW_Curve_Profile")
        p_pow = pdict.get("IDW_Power")
        if p_prof and p_pow:
            prof_val = p_prof.valueAsText or "Gentle / Smooth (Power 1.2)"
            last_prof = getattr(self, "_last_prof", None)
            if prof_val != last_prof:
                if "1.2" in prof_val:
                    p_pow.value = 1.2
                elif "2.0" in prof_val:
                    p_pow.value = 2.0
                elif "0.7" in prof_val:
                    p_pow.value = 0.7
                self._last_prof = prof_val

        for k in ("IDW_Curve_Profile", "IDW_Search_Type", "IDW_Num_Points", "IDW_Max_Distance"):
            if k in pdict:
                pdict[k].enabled = is_idw and not dl
        if "IDW_Power" in pdict:
            is_custom = prof_val.startswith("Custom") if prof_val else False
            pdict["IDW_Power"].enabled = is_idw and (not dl) and is_custom
        for k in ("Krig_Model", "Krig_Type", "Krig_Num_Points"):
            if k in pdict:
                pdict[k].enabled = is_krig and not dl
        for k in ("Spline_Type", "Spline_Weight", "Spline_Num_Points"):
            if k in pdict:
                pdict[k].enabled = is_spline and not dl
        for k in ("Interpolation_Method", "Base_Cell_Size", "Create_Isobars"):
            if k in pdict:
                pdict[k].enabled = not dl

        if "Wind_Factor_Cell_Size" in pdict:
            pdict["Wind_Factor_Cell_Size"].enabled = (not dl) and ("Wind" in active_mods)

        # Focal options
        p_focal = pdict.get("Focal_Smoothing")
        focal_on = bool(p_focal.value) if p_focal and p_focal.value is not None else False
        if "Focal_Smoothing" in pdict:
            pdict["Focal_Smoothing"].enabled = not dl
        if "Focal_Statistic" in pdict:
            pdict["Focal_Statistic"].enabled = focal_on and not dl
        if "Focal_Neighborhood" in pdict:
            pdict["Focal_Neighborhood"].enabled = focal_on and not dl

        # Map Options
        if p_add_map:
            p_add_map.enabled = not dl
        if p_map_mods:
            p_map_mods.enabled = bool(p_add_map.value if p_add_map else False) and not dl

        # Isobars
        p_iso = pdict.get("Create_Isobars")
        iso_on = bool(p_iso.value) if p_iso and p_iso.value is not None else False
        has_p = ("Sea Level Pressure" in active_mods) or ("Surface Pressure" in active_mods)
        show_iso = bool(iso_on and has_p)
        if "Pressure_Interval_Scheme" in pdict:
            pdict["Pressure_Interval_Scheme"].enabled = show_iso
        p_scheme = pdict.get("Pressure_Interval_Scheme")
        scheme = p_scheme.valueAsText if p_scheme else "Global Standard (4 mbar)"
        if "Custom_Pressure_Step" in pdict:
            if show_iso and scheme == "Custom Interval":
                pdict["Custom_Pressure_Step"].enabled = True
            else:
                if show_iso and scheme.startswith("Global"):
                    pdict["Custom_Pressure_Step"].value = 4.0
                elif show_iso:
                    pdict["Custom_Pressure_Step"].value = 2.0
                pdict["Custom_Pressure_Step"].enabled = False
        return

    def updateMessages(self, parameters):
        try:
            for p in parameters:
                try:
                    p.clearMessage()
                except Exception:
                    pass
            pdict = dict((p.name, p) for p in parameters)
            p_op = pdict.get("Operation_Mode")
            op_text = p_op.valueAsText if p_op else "Download & Generate Atlas (Full Pipeline) [Default]"
            is_offline = bool(op_text and op_text.startswith("Interpolate & Map Existing Data"))

            p_dl = pdict.get("Download_Only")
            dl_only = bool(p_dl.value) if (p_dl and p_dl.value is not None and not is_offline) else False

            if not is_offline:
                p_in = pdict.get("Input_Point_Features") or pdict.get("Input_Points")
                if not (p_in and p_in.value):
                    if p_in:
                        p_in.setErrorMessage("Input Point Features layer is required for Download mode.")
                else:
                    try:
                        desc = arcpy.Describe(p_in.value)
                        if desc.shapeType != "Point":
                            p_in.setErrorMessage("Input must be a Point layer.")
                    except Exception:
                        pass
            else:
                p_pre = pdict.get("Precalculated_Point_Layers") or pdict.get("Precalculated_Point_Layer")
                if not (p_pre and p_pre.value):
                    if p_pre:
                        p_pre.setErrorMessage("Precalculated Point Layer(s) required for Offline mode.")
                else:
                    try:
                        lyr_list = [l.strip().strip("'\"") for l in (p_pre.valueAsText or "").split(";") if l.strip().strip("'\"")]
                        for lyr in lyr_list:
                            desc = arcpy.Describe(lyr)
                            if desc.shapeType not in ("Point", "Multipoint"):
                                p_pre.setErrorMessage("Precalculated layer '%s' must be a Point or Multipoint layer." % os.path.basename(lyr))
                                break
                    except Exception:
                        pass

            if not is_offline:
                p_mode = pdict.get("Time_Mode") or pdict.get("Time_Range_Mode")
                mode = p_mode.valueAsText if p_mode else "Single Year"
                if mode == "Single Year":
                    p_sy = pdict.get("Single_Year")
                    y = p_sy.value if p_sy else None
                    if y is None or int(y) < 1981 or int(y) > 2030:
                        if p_sy:
                            p_sy.setErrorMessage("Single Year must be 1981-2030.")
                elif mode == "Year Range":
                    p_s = pdict.get("Start_Year")
                    p_e = pdict.get("End_Year")
                    s = p_s.value if p_s else None
                    e = p_e.value if p_e else None
                    if s is None or e is None:
                        if p_s:
                            p_s.setErrorMessage("Start/End Year required for Year Range.")
                    elif int(s) > int(e):
                        if p_e:
                            p_e.setErrorMessage("End Year must be >= Start Year.")
                    elif int(s) < 1981:
                        if p_s:
                            p_s.setErrorMessage("NASA POWER coverage starts 1981.")
                elif mode == "Custom Date Range":
                    p_sd = pdict.get("Start_Date")
                    p_ed = pdict.get("End_Date")
                    d_start = parse_gp_date(p_sd.value if p_sd else None)
                    d_end = parse_gp_date(p_ed.value if p_ed else None)
                    if not d_start and p_sd:
                        p_sd.setErrorMessage("Valid Start Date is required.")
                    if not d_end and p_ed:
                        p_ed.setErrorMessage("Valid End Date is required.")
                    if d_start and d_end:
                        if d_start > d_end and p_ed:
                            p_ed.setErrorMessage("End Date must be on or after Start Date.")
                        if d_start.year < 1981 and p_sd:
                            p_sd.setErrorMessage("Start Date must be 1981 or later.")

            p_mods = pdict.get("Climate_Modules")
            mods = p_mods.valueAsText if p_mods else ""
            if not mods:
                if p_mods:
                    p_mods.setErrorMessage("Select at least one climate module or applied submodel.")
            else:
                raw_items = [m.strip().strip("'\"") for m in mods.split(";") if m.strip().strip("'\"")]
                curr_mods = [m for m in raw_items if not resolve_submodel_name(m)]
                for item in raw_items:
                    res_s = resolve_submodel_name(item)
                    if res_s:
                        req_m = SUBMODEL_DEPS[res_s].get("modules", [])
                        unsel = [rm for rm in req_m if rm not in curr_mods]
                        if unsel:
                            p_mods.setWarningMessage(
                                "Submodel '%s' requires %s. "
                                "Prerequisite data will be queried automatically as temporary intermediate data."
                                % (SUBMODEL_DEPS[res_s]["short"], ", ".join(unsel))
                            )

            p_scope = pdict.get("Field_Filter_Scope")
            scope = p_scope.valueAsText if p_scope else "All Variables & Fields (Full Suite) [Recommended]"
            if scope and not scope.startswith("All Variables"):
                p_aggs = pdict.get("Included_Aggregations")
                p_seas = pdict.get("Included_Seasons")
                p_flds = pdict.get("Selected_Fields")
                active_mods_list = [m.strip().strip("'\"") for m in mods.split(";") if m.strip().strip("'\"")] if mods else []
                aggs_txt = p_aggs.valueAsText if p_aggs else ""
                aggs_list = [a.strip().strip("'\"") for a in aggs_txt.split(";") if a.strip().strip("'\"")] if aggs_txt else []
                seas_txt = p_seas.valueAsText if p_seas else ""
                seas_list = [s.strip().strip("'\"") for s in seas_txt.split(";") if s.strip().strip("'\"")] if seas_txt else []
                flds_txt = p_flds.valueAsText if p_flds else ""

                filtered = resolve_filtered_fields(active_mods_list, scope, aggs_list, seas_list, flds_txt)
                total_f = sum(len(flist) for flist in filtered.values())
                if total_f == 0:
                    if scope.startswith("Custom Field") and p_flds:
                        p_flds.setErrorMessage("At least one custom field must be selected.")
                    elif p_scope:
                        p_scope.setErrorMessage("No climate indicators match the selected filter criteria.")

            if not dl_only:
                for k in ("Base_Cell_Size", "Wind_Factor_Cell_Size"):
                    p_c = pdict.get(k)
                    v = (p_c.valueAsText if p_c else "") or ""
                    if not v.strip() and p_c:
                        p_c.setErrorMessage("Cell size is required (e.g. 5000 Meters).")

            p_meth = pdict.get("Interpolation_Method")
            meth = p_meth.valueAsText if p_meth else "IDW"
            if meth == "IDW" and not dl_only:
                p_pow = pdict.get("IDW_Power")
                if p_pow and (p_pow.value is None or float(p_pow.value) <= 0):
                    p_pow.setErrorMessage("IDW Power must be > 0 (default 1.2).")
                p_pts = pdict.get("IDW_Num_Points")
                if p_pts and (p_pts.value is None or int(p_pts.value) < 1):
                    p_pts.setErrorMessage("IDW Number of Points must be >= 1 (default 12).")
                p_st = pdict.get("IDW_Search_Type")
                if p_st and (p_st.valueAsText or "Variable") == "Fixed":
                    p_md = pdict.get("IDW_Max_Distance")
                    if p_md and (p_md.value is None or float(p_md.value) <= 0):
                        p_md.setErrorMessage("Fixed search requires Maximum Distance > 0 (metres).")
            elif meth == "Ordinary Kriging" and not dl_only:
                p_kpts = pdict.get("Krig_Num_Points")
                if p_kpts and (p_kpts.value is None or int(p_kpts.value) < 1):
                    p_kpts.setErrorMessage("Kriging Number of Points must be >= 1 (default 12).")
            elif meth == "Spline" and not dl_only:
                p_sw = pdict.get("Spline_Weight")
                if p_sw and (p_sw.value is None or float(p_sw.value) < 0):
                    p_sw.setErrorMessage("Spline Weight must be >= 0 (default 5.0).")
                p_spts = pdict.get("Spline_Num_Points")
                if p_spts and (p_spts.value is None or int(p_spts.value) < 1):
                    p_spts.setErrorMessage("Spline Number of Points must be >= 1 (default 12).")

            p_foc = pdict.get("Focal_Smoothing")
            if p_foc and bool(p_foc.value) and not dl_only:
                p_fn = pdict.get("Focal_Neighborhood")
                if p_fn and (p_fn.value is None or int(p_fn.value) < 1):
                    p_fn.setErrorMessage("Focal Neighborhood must be >= 1 cell (default 3 = 3x3).")

            p_am = pdict.get("Add_To_Map")
            if p_am and bool(p_am.value) and not dl_only:
                p_mm = pdict.get("Map_Add_Modules")
                if p_mm and not (p_mm.valueAsText or "").strip():
                    p_mm.setErrorMessage("Add to map is ON: choose at least one element.")

            p_sch = pdict.get("Pressure_Interval_Scheme")
            _sch = p_sch.valueAsText if p_sch else ""
            if _sch == "Custom Interval":
                p_cs = pdict.get("Custom_Pressure_Step")
                _st = p_cs.value if p_cs else None
                if _st is None or float(_st) <= 0:
                    if p_cs:
                        p_cs.setErrorMessage("Custom Interval needs a step > 0 mbar (e.g. 1.0).")

            p_out = pdict.get("Output_Workspace")
            out = p_out.valueAsText if p_out else ""
            if out and not os.path.isdir(out):
                try:
                    makedirs_ok(out)
                except Exception:
                    if p_out:
                        p_out.setErrorMessage("Cannot create output folder.")
        except Exception:
            pass
        return

    # ---------------- execute ----------------
    def execute(self, parameters, messages):
        if not _HAS_ARCPY:
            raise RuntimeError("This tool must run inside ArcMap (arcpy).")
        arcpy.env.overwriteOutput = True
        log_lines = []
        warnings = []

        def msg(t):
            messages.addMessage(t)
            log_lines.append("[%s] %s" % (now_str(), t))

        def warn(t):
            warnings.append(t)
            log_lines.append("[WARN] " + t)
            if hasattr(messages, "addWarningMessage"):
                messages.addWarningMessage(t)
            elif hasattr(messages, "addWarning"):
                messages.addWarning(t)
            elif hasattr(messages, "addMessage"):
                messages.addMessage("[WARNING] " + str(t))

        t_start = time.time()
        try:
            pdict = dict((p.name, p) for p in parameters)
            p_op = pdict.get("Operation_Mode")
            op_text = p_op.valueAsText if p_op else "Download & Generate Atlas (Full Pipeline) [Default]"
            is_offline = bool(op_text and op_text.startswith("Interpolate & Map Existing Data"))

            p_dl0 = pdict.get("Download_Only")
            download_only = False if (is_offline or p_dl0 is None or p_dl0.value is None) else bool(p_dl0.value)
            if is_offline:
                p_pre_in = pdict.get("Precalculated_Point_Layers") or pdict.get("Precalculated_Point_Layer") or pdict.get("Input_Point_Features")
                in_points = p_pre_in.valueAsText if p_pre_in else None
            else:
                p_std_in = pdict.get("Input_Point_Features") or pdict.get("Input_Points")
                in_points = p_std_in.valueAsText if p_std_in else None
            mask = (pdict.get("Study_Area_Mask") or parameters[3]).valueAsText
            out_sr_p = pdict.get("Output_Spatial_Reference") or pdict.get("Output_Coordinate_System")
            out_sr_text = out_sr_p.valueAsText if out_sr_p else None
            time_mode = (pdict.get("Time_Mode") or pdict.get("Time_Range_Mode")).valueAsText or "Single Year"
            p_sy = pdict.get("Single_Year")
            single_year = int(p_sy.value) if (p_sy and p_sy.value is not None) else 2025
            p_s = pdict.get("Start_Year")
            start_year = int(p_s.value) if (p_s and p_s.value is not None) else 2015
            p_e = pdict.get("End_Year")
            end_year = int(p_e.value) if (p_e and p_e.value is not None) else 2025
            p_sd = pdict.get("Start_Date")
            p_ed = pdict.get("End_Date")
            d_start = parse_gp_date(p_sd.value if p_sd else None)
            d_end = parse_gp_date(p_ed.value if p_ed else None)
            temporal = (pdict.get("Temporal_Resolution") or parameters[10]).valueAsText or "Monthly"
            mods_text = (pdict.get("Climate_Modules") or parameters[5]).valueAsText or ""
            raw_items = [m.strip().strip("'\"") for m in mods_text.split(";") if m.strip().strip("'\"")]
            modules = []
            active_submodels = []
            for item in raw_items:
                res_sub = resolve_submodel_name(item)
                if res_sub:
                    if res_sub not in active_submodels:
                        active_submodels.append(res_sub)
                else:
                    if item in PRIMARY_MODULES_ALL and item not in modules:
                        modules.append(item)

            active_export_modules = list(modules)
            if active_submodels and "Climate_Models" not in active_export_modules:
                active_export_modules.append("Climate_Models")

            if not active_export_modules:
                raise RuntimeError("Select at least one climate module or applied submodel.")
            p_bc = pdict.get("Base_Cell_Size")
            base_cell = tolerance_meters(p_bc.valueAsText if (p_bc and p_bc.value) else "5000 Meters")
            if base_cell <= 0:
                base_cell = 5000.0
            p_wc = pdict.get("Wind_Factor_Cell_Size")
            wind_cell = tolerance_meters(p_wc.valueAsText if (p_wc and p_wc.value) else "20000 Meters")
            if wind_cell <= 0:
                wind_cell = 20000.0
            interp = pdict.get("Interpolation_Method").valueAsText if pdict.get("Interpolation_Method") else "IDW"
            out_ws = (pdict.get("Output_Workspace") or parameters[2]).valueAsText
            p_iso = pdict.get("Create_Isobars")
            create_isobars = bool(p_iso.value) if (p_iso and p_iso.value is not None) else False
            p_pv = pdict.get("Purge_Cache")
            purge = True if (p_pv is None or p_pv.value is None) else bool(p_pv.value)
            p_am = pdict.get("Add_To_Map")
            add_to_map = False if (p_am is None or p_am.value is None) else bool(p_am.value)
            p_tol = pdict.get("Point_Tolerance")
            tol_m = tolerance_meters(p_tol.valueAsText if (p_tol and p_tol.value) else None)
            p_foc = pdict.get("Focal_Smoothing")
            focal_on = bool(p_foc.value) if (p_foc and p_foc.value is not None) else False
            p_fstat = pdict.get("Focal_Statistic")
            focal_stat = p_fstat.valueAsText if (p_fstat and p_fstat.valueAsText) else "MEAN"
            p_fn = pdict.get("Focal_Neighborhood")
            focal_n = int(p_fn.value) if (p_fn and p_fn.value is not None) else 3
            focal = {"apply": focal_on, "stat": focal_stat, "size": max(1, focal_n)}
            provider = pdict.get("Climate_Data_Source").valueAsText if pdict.get("Climate_Data_Source") else "NASA POWER API"
            use_om = provider.startswith("Open-Meteo")
            p_om_m = pdict.get("OpenMeteo_Model")
            om_model = p_om_m.valueAsText if (p_om_m and p_om_m.valueAsText) else "ERA5-Land (Highest Resolution ~9 km / 0.1 deg) [Recommended]"
            om_slug = om_model_slug(om_model)
            p_gf = pdict.get("Gap_Fill_Method")
            _gap_txt = p_gf.valueAsText if (p_gf and p_gf.valueAsText) else "Climatological Month Mean (Recommended)"
            if _gap_txt.startswith("Linear"):
                gap_method = "linear"
            elif _gap_txt.startswith("No Fill"):
                gap_method = "none"
            elif _gap_txt.startswith("Spatial"):
                gap_method = "spatial"
            else:
                gap_method = "climatological"

            # --- Field Filtering Setup ---
            p_scope = pdict.get("Field_Filter_Scope")
            filter_scope = p_scope.valueAsText if p_scope else "All Variables & Fields (Full Suite) [Recommended]"
            p_aggs = pdict.get("Included_Aggregations")
            aggs_txt = p_aggs.valueAsText if p_aggs else ""
            filter_aggs = [a.strip().strip("'\"") for a in aggs_txt.split(";") if a.strip().strip("'\"")] if aggs_txt else None
            p_seas = pdict.get("Included_Seasons")
            seas_txt = p_seas.valueAsText if p_seas else ""
            filter_seasons = [s.strip().strip("'\"") for s in seas_txt.split(";") if s.strip().strip("'\"")] if seas_txt else None
            p_flds = pdict.get("Selected_Fields")
            filter_custom_flds = p_flds.valueAsText if p_flds else None

            wanted_fields_by_module = resolve_filtered_fields(
                modules, filter_scope, filter_aggs, filter_seasons, filter_custom_flds
            )
            if active_submodels:
                sub_fields = []
                for s in active_submodels:
                    for f in SUBMODEL_DEPS[s].get("fields", [SUBMODEL_DEPS[s]["field"]]):
                        if f not in sub_fields:
                            sub_fields.append(f)
                wanted_fields_by_module["Climate_Models"] = sub_fields

            total_wanted_fields = sum(len(flist) for flist in wanted_fields_by_module.values())
            msg("Field Filtering: Scope='%s' | Total Active Indicators=%d." % (filter_scope, total_wanted_fields))
            for m in active_export_modules:
                msg("  Module '%s': %d indicators (%s)" % (
                    m, len(wanted_fields_by_module.get(m, [])),
                    ", ".join(wanted_fields_by_module.get(m, []))
                ))
            if total_wanted_fields == 0:
                raise RuntimeError("No climate fields match the selected filter criteria.")

            # --- interpolation advanced options (active algorithm only) ---
            p_pow = pdict.get("IDW_Power")
            p_st = pdict.get("IDW_Search_Type")
            p_npts = pdict.get("IDW_Num_Points")
            p_md = pdict.get("IDW_Max_Distance")
            p_sp_type = pdict.get("Spline_Type")
            p_sp_weight = pdict.get("Spline_Weight")
            p_sp_pts = pdict.get("Spline_Num_Points")
            iopts = {
                "power": float(p_pow.value) if (p_pow and p_pow.value is not None) else 1.2,
                "search": p_st.valueAsText if (p_st and p_st.valueAsText) else "Variable",
                "npoints": int(p_npts.value) if (p_npts and p_npts.value is not None) else 12,
                "maxdist": (float(p_md.value) if (p_md and p_md.value is not None) else None),
                "spline_type": (p_sp_type.valueAsText if p_sp_type and p_sp_type.valueAsText else "Tension"),
                "spline_weight": (float(p_sp_weight.value) if p_sp_weight and p_sp_weight.value is not None else 5.0),
                "spline_npoints": (int(p_sp_pts.value) if p_sp_pts and p_sp_pts.value is not None else 12),
            }
            p_km = pdict.get("Krig_Model")
            p_kt = pdict.get("Krig_Type")
            p_kp = pdict.get("Krig_Num_Points")
            kopts = {
                "model": (p_km.valueAsText if p_km and p_km.valueAsText else "Spherical"),
                "ktype": (p_kt.valueAsText if p_kt and p_kt.valueAsText else "Ordinary"),
                "npoints": (int(p_kp.value) if p_kp and p_kp.value is not None else 12),
            }

            if is_offline:
                years = [2025]
                y0, y1 = 2000, 2025
                start_date_str, end_date_str = None, None
                time_tag = "Offline"
                period_label = "Precalculated Data (Offline Mode)"
                try:
                    f_names = [f.name for f in arcpy.ListFields(in_points)]
                    if "Data_Start" in f_names and "Data_End" in f_names:
                        with arcpy.da.SearchCursor(in_points, ["Data_Start", "Data_End"]) as cur:
                            for row in cur:
                                if row[0] and row[1]:
                                    y0, y1 = int(row[0]), int(row[1])
                                    years = list(range(y0, y1 + 1))
                                    if y0 == y1:
                                        time_tag = "%d" % y0
                                        period_label = "%d (Precalculated)" % y0
                                    else:
                                        time_tag = "From_%d_To_%d" % (y0, y1)
                                        period_label = "%d-%d (Precalculated)" % (y0, y1)
                                    break
                except Exception:
                    pass
            elif time_mode == "Single Year":
                years = [single_year]
                y0, y1 = single_year, single_year
                start_date_str = "%04d-01-01" % single_year
                end_date_str = "%04d-12-31" % single_year
                time_tag = "%d" % single_year
                period_label = "%d (Single Year)" % single_year
                col_data_start = str(single_year)
                col_data_end = str(single_year)
            elif time_mode == "Year Range":
                years = list(range(start_year, end_year + 1))
                y0, y1 = years[0], years[-1]
                start_date_str = "%04d-01-01" % start_year
                end_date_str = "%04d-12-31" % end_year
                time_tag = "From_%d_To_%d" % (start_year, end_year)
                period_label = "%d-%d (%d yrs)" % (start_year, end_year, len(years))
                col_data_start = str(start_year)
                col_data_end = str(end_year)
            else:
                if not d_start:
                    d_start = _dt.date(2024, 1, 1)
                if not d_end:
                    d_end = _dt.date(2024, 12, 31)
                if d_start > d_end:
                    d_start, d_end = d_end, d_start
                y0, y1 = d_start.year, d_end.year
                years = list(range(y0, y1 + 1))
                start_date_str = "%04d-%02d-%02d" % (d_start.year, d_start.month, d_start.day)
                end_date_str = "%04d-%02d-%02d" % (d_end.year, d_end.month, d_end.day)
                time_tag = "From_%04d%02d%02d_To_%04d%02d%02d" % (
                    d_start.year, d_start.month, d_start.day,
                    d_end.year, d_end.month, d_end.day)
                s_txt = p_sd.valueAsText if (p_sd and p_sd.value) else ("%02d/%02d/%04d" % (d_start.day, d_start.month, d_start.year))
                e_txt = p_ed.valueAsText if (p_ed and p_ed.value) else ("%02d/%02d/%04d" % (d_end.day, d_end.month, d_end.year))
                period_label = "%s to %s (Custom Date Range)" % (s_txt, e_txt)
                col_data_start = str(s_txt)
                col_data_end = str(e_txt)

            msg("POWER Climate Atlas Generator v%s (ArcMap 10.x)" % TOOL_VERSION)
            if download_only:
                msg("Mode: DOWNLOAD & SAVE POINT DATA ONLY (points + tables, skipping rasters and atlas).")
            msg("Data source: %s" % provider)
            if use_om:
                msg("Atmospheric Model: %s [API code: %s]" % (om_model, om_slug))
            else:
                msg("NASA POWER Model: MERRA-2 (~50 km / 0.5 deg) & CERES SYN1deg (~100 km / 1.0 deg) via AG community")
            msg("Modules: %s%s | Period: %s | Temporal: %s | Interp: %s"
                % (", ".join(modules) if modules else "None",
                   (" | Submodels: " + ", ".join(SUBMODEL_DEPS[s]["short"] for s in active_submodels)) if active_submodels else "",
                   period_label, temporal, interp))
            if interp == "IDW":
                msg("IDW settings: power=%.2f, search=%s, points=%d%s" % (
                    iopts["power"], iopts["search"], iopts["npoints"],
                    (", maxdist=%.0fm" % iopts["maxdist"]) if iopts["maxdist"] else ""))
            elif interp == "Ordinary Kriging":
                msg("Kriging settings: model=%s, type=%s, points=%d" % (
                    kopts["model"], kopts["ktype"], kopts["npoints"]))
            elif interp == "Spline":
                msg("Spline settings: type=%s, weight=%.2f, points=%d" % (
                    iopts["spline_type"], iopts["spline_weight"], iopts["spline_npoints"]))

            in_point_list = [lp.strip().strip("'\"") for lp in (in_points or "").split(";") if lp.strip().strip("'\"")]
            if not in_point_list:
                raise RuntimeError("No input point features or precalculated point layers were specified.")
            primary_in_point = in_point_list[0]
            in_desc = arcpy.Describe(primary_in_point)
            if out_sr_text:
                try:
                    out_sr = arcpy.SpatialReference()
                    out_sr.loadFromString(out_sr_text)
                except Exception:
                    try:
                        p_sr = pdict.get("Output_Coordinate_System", parameters[3])
                        out_sr = arcpy.Describe(p_sr.value).spatialReference
                    except Exception:
                        out_sr = in_desc.spatialReference
            else:
                out_sr = in_desc.spatialReference
            is_geo = getattr(out_sr, "type", "") == "Geographic"
            eff_base = base_cell / 111320.0 if (is_geo and base_cell > 1.0) else base_cell
            eff_wind = wind_cell / 111320.0 if (is_geo and wind_cell > 1.0) else wind_cell
            if is_geo and (base_cell > 1.0 or wind_cell > 1.0):
                warn("Geographic output SR: cell sizes treated as metres and converted to degrees "
                     "(base=%.5f deg, wind=%.5f deg)." % (eff_base, eff_wind))
            msg("Output SR: %s (%s)" % (out_sr.name, getattr(out_sr, "type", "?")))

            gdb_name = "Climate_Database_%s.gdb" % time_tag
            gdb_path, paths = self._build_layout(out_ws, active_export_modules, gdb_name=gdb_name)
            msg("Workspace: %s (GDB: %s)" % (out_ws, gdb_name))

            wgs = arcpy.SpatialReference(4326)
            scratch_dir = os.path.join(out_ws, "_scratch")
            makedirs_ok(scratch_dir)
            if mask:
                # Reproject the mask once into the output SR so mask, extent,
                # snap and cell size all share one unit system.
                try:
                    maskp = os.path.join(scratch_dir, "maskp.shp")
                    try:
                        if arcpy.Exists(maskp):
                            arcpy.management.Delete(maskp)
                    except Exception:
                        pass
                    arcpy.management.Project(mask, maskp, out_sr)
                    mask = maskp
                    msg("Mask reprojected to output SR.")
                except Exception as ex:
                    warn("Mask reprojection failed (%s); using mask as-is." % ex)

            # NOTE: DO NOT set arcpy.env.mask = mask here!
            # Doing so would prematurely clip input points and restrict intermediate tools.
            # Masking must be applied ONLY after surface interpolation via ExtractByMask.
            arcpy.ClearEnvironment("mask")
            arcpy.ClearEnvironment("extent")
            arcpy.env.outputCoordinateSystem = out_sr
            arcpy.env.cellSize = eff_base
            # --- guard: refuse rasters that would exhaust 32-bit ArcMap ---
            try:
                _desc_target = arcpy.Describe(mask) if (mask and arcpy.Exists(mask)) else arcpy.Describe(in_points)
                _ext = _desc_target.extent
                _w = float(_ext.XMax - _ext.XMin)
                _h = float(_ext.YMax - _ext.YMin)
                if _w > 0 and _h > 0 and eff_base > 0:
                    _cells = (_w / eff_base) * (_h / eff_base)
                    if _cells > 20000000:
                        messages.addErrorMessage(
                            "Cell size %.4g %s is far too fine for this extent "
                            "(%.1f x %.1f %s ~= %.1f million cells; limit 20M). "
                            "Increase 'Base Cell Size' (e.g. 5000 Meters for "
                            "country-scale work)." % (
                                base_cell,
                                ("degrees" if is_geo else "metres"),
                                _w, _h,
                                ("degrees" if is_geo else "metres"),
                                _cells / 1000000.0))
                        return
            except Exception:
                pass
            # --- performance: multicore SA (where supported) + LZW TIFF compression ---
            try:
                arcpy.env.parallelProcessingFactor = "100%"
            except Exception:
                pass
            # --- mandatory LZW on all output rasters + dedicated scratch ---
            try:
                arcpy.env.compression = "LZW"
            except Exception:
                pass
            try:
                arcpy.env.scratchWorkspace = scratch_dir
            except Exception:
                pass
            msg("LZW compression: enforced | purge cache: %s" % purge)

            if interp == "IDW":
                interp_label = "IDW(p=%.2f,%s,n=%d%s)" % (
                    iopts["power"], iopts["search"], iopts["npoints"],
                    (",d=%.0f" % iopts["maxdist"]) if iopts["maxdist"] else "")
            elif interp == "Ordinary Kriging":
                interp_label = "Kriging(%s,%s,n=%d)" % (
                    kopts["model"], kopts["ktype"], kopts["npoints"])
            elif interp == "Spline":
                interp_label = "Spline(%s,w=%.2f,n=%d)" % (
                    iopts["spline_type"], iopts["spline_weight"], iopts["spline_npoints"])
            else:
                interp_label = interp
            if focal["apply"]:
                interp_label += "+Focal(%s,%dx%d)" % (focal["stat"], focal["size"], focal["size"])
                msg("Focal smoothing: %s %dx%d (smoothed raster replaces output)."
                    % (focal["stat"], focal["size"], focal["size"]))

            # Determine ordered modules to enforce foundational hierarchy:
            HIERARCHY = [
                "Temperature", "Precipitation", "Relative Humidity",
                "Solar Radiation", "Wind", "Sea Level Pressure",
                "Surface Pressure", "UV Index", "Cloud Cover",
                "Climate_Models"
            ]
            ordered_modules = [m for m in HIERARCHY if m in active_export_modules]
            for m in active_export_modules:
                if m not in ordered_modules:
                    ordered_modules.append(m)

            admin_meta = {
                "y0": y0, "y1": y1, "temporal": temporal, "interp": interp_label,
                "base_cell": base_cell, "wind_cell": wind_cell,
                "data_start": col_data_start, "data_end": col_data_end
            }
            element_fcs = {}
            raster_registry = []
            sa_avail = False
            if not download_only:
                try:
                    arcpy.CheckOutExtension("Spatial")
                    sa_avail = True
                except Exception:
                    sa_avail = False
                    warn("Spatial Analyst unavailable: raster interpolation skipped.")

            if is_offline:
                msg("Offline Mode: merging precalculated point layer(s) ...")
                results = []
                element_fcs = self._merge_offline_layers(
                    in_points, gdb_path, out_sr, modules, active_submodels,
                    wanted_fields_by_module, msg, warn)
                if not element_fcs:
                    raise RuntimeError("No element point layers were built from precalculated inputs.")

                for mi, m in enumerate(ordered_modules):
                    fc = element_fcs.get(m)
                    if not fc or not arcpy.Exists(fc):
                        continue
                    short = MODULE_SHORT.get(m, m)
                    self._export_shapefile(fc, os.path.join(paths["shp"], short + ".shp"), msg, warn)
                    self._export_csv(fc, os.path.join(paths["vec"], short + ".csv"), msg, warn)
                    if not download_only and sa_avail:
                        elem_rasters = self._interpolate_all(
                            None, [m], paths, eff_base, interp, mask, msg, warn,
                            iopts, kopts, is_geo, purge, scratch_dir, focal,
                            {m: fc}, wanted_fields_by_module=wanted_fields_by_module)
                        raster_registry.extend(elem_rasters)
                        if purge and os.path.exists(scratch_dir):
                            for sf in os.listdir(scratch_dir):
                                sfp = os.path.join(scratch_dir, sf)
                                try:
                                    if os.path.isfile(sfp): os.remove(sfp)
                                except Exception:
                                    pass
                        gc.collect()
                    msg(">>> Element [%d/%d] %s: Layer, exports & rasters ready. <<<\n" % (mi + 1, len(ordered_modules), m))
            else:
                msg("Extracting WGS84 coordinates ...")
                pts = self._extract_points(in_points, wgs, messages)
                msg("Input points: %d" % len(pts))
                if not pts:
                    raise RuntimeError(
                        "No points found in '%s' (empty layer, empty selection, or "
                        "definition query filtering everything out)." % in_points)
                if tol_m > 0:
                    if not is_geo and tol_m > eff_base:
                        warn("Point Tolerance (%.0f m) exceeds Base Cell Size (%.0f m): "
                             "thinning may leave gaps; consider a smaller tolerance."
                             % (tol_m, eff_base))
                    if is_geo and tol_m / 111320.0 > eff_base:
                        warn("Point Tolerance exceeds Base Cell Size: "
                             "thinning may leave gaps; consider a smaller tolerance.")
                    kept, dropped = thin_points_tolerance(pts, tol_m)
                    msg("Tolerance %.0f m: %d kept, %d merged %s" % (
                        tol_m, len(kept), len(dropped),
                        ("(OIDs %s)" % dropped[:20]) if dropped else ""))
                    pts = kept
                    if not pts:
                        raise RuntimeError("Tolerance removed all points.")

                msg("Checking server connectivity (one probe request) ...")
                try:
                    probe_server(provider, pts[0]["lat"], pts[0]["lon"], y0, len(pts),
                                 model=om_slug, start_date=start_date_str, end_date=end_date_str)
                    msg("Server connectivity OK (%s)." % provider)
                except RuntimeError as ex:
                    messages.addErrorMessage(str(ex))
                    raise

                # Project base points once for all elements
                tmp_base = safe_project_fc(in_points, out_sr, gdb_path, "baseproj", warn)
                tmp_base_is_temp = (tmp_base != in_points)

                results = [dict(p, parameter={}, monthly={}, daily_raw={}, fields={}, status="PENDING", error="") for p in pts]
                nasa_cache = {}
                sess = None
                if _HAS_REQUESTS:
                    try:
                        sess = requests.Session()
                    except Exception:
                        sess = None

                if use_om:
                    om_daily_all, om_hourly_all, _om_drop, _om_note = om_probe_vars(
                        ordered_modules, model=om_slug, start_date=start_date_str, end_date=end_date_str)
                    if _om_note:
                        warn(_om_note)

                try:
                    for mi, m in enumerate(ordered_modules):
                        msg("\n" + "=" * 65)
                        msg(">>> ELEMENT [%d/%d]: %s <<<" % (mi + 1, len(ordered_modules), m))
                        msg("=" * 65)

                        # Determine raw parameters needed for this element
                        if m == "Climate_Models":
                            needed_m = []
                            for s in active_submodels:
                                for p in SUBMODEL_DEPS[s].get("params", []):
                                    if p not in needed_m:
                                        needed_m.append(p)
                        else:
                            needed_m = list(MODULE_PARAMS.get(m, []))

                        # Check if any station needs querying
                        if use_om:
                            # For Open-Meteo, get required variables for this module
                            m_d_vars, m_h_vars = om_var_sets([m])
                            m_d_vars = [v for v in m_d_vars if v in om_daily_all]
                            m_h_vars = [v for v in m_h_vars if v in om_hourly_all]

                            pts_to_fetch = []
                            for idx, p in enumerate(pts):
                                curr_m = results[idx].get("monthly", {})
                                missing = any(v not in curr_m for v in m_d_vars) or any(v not in curr_m for v in m_h_vars)
                                if missing:
                                    pts_to_fetch.append((idx, p))

                            if pts_to_fetch:
                                msg("Element [%d/%d] %s: Querying Open-Meteo (%s) sequentially (%d station(s)) ..."
                                    % (mi + 1, len(ordered_modules), m, om_slug, len(pts_to_fetch)))
                                arcpy.SetProgressor("step", "Querying Open-Meteo for %s..." % m, 0, len(pts_to_fetch), 1)
                                for step_i, (idx, p) in enumerate(pts_to_fetch):
                                    pct = float(step_i + 1) / float(len(pts_to_fetch)) * 100.0
                                    msg("  [%s] Station %d/%d (%.0f%%) [OID %s | Lat: %.4f, Lon: %.4f] - Fetching..." %
                                        (m, step_i + 1, len(pts_to_fetch), pct, p.get("oid", idx + 1), p["lat"], p["lon"]))
                                    try:
                                        monthly, daily_raw, _drop = fetch_openmeteo_point(
                                            p["lat"], p["lon"], y0, y1, [m],
                                            daily_vars=m_d_vars, hourly_vars=m_h_vars,
                                            model=om_slug, start_date=start_date_str, end_date=end_date_str)
                                        results[idx].setdefault("monthly", {}).update(monthly)
                                        if temporal == "Daily":
                                            results[idx].setdefault("daily_raw", {}).update(daily_raw)
                                        results[idx]["status"] = "OK"
                                    except Exception as ex:
                                        results[idx]["error"] = str(ex)[:500]
                                        results[idx]["status"] = "FAILED"
                                    arcpy.SetProgressorPosition(step_i + 1)
                                arcpy.ResetProgressor()
                            else:
                                msg("Element [%d/%d] %s: All required variables already cached in memory. Reusing with 0 queries."
                                    % (mi + 1, len(ordered_modules), m))

                        else:
                            # NASA POWER: check if missing any params
                            pts_to_fetch = []
                            for idx, p in enumerate(pts):
                                curr_par = results[idx].get("parameter", {})
                                missing_p = [pname for pname in needed_m if pname not in curr_par]
                                if missing_p:
                                    pts_to_fetch.append((idx, p, missing_p))

                            if pts_to_fetch:
                                msg("Element [%d/%d] %s: Querying NASA POWER sequentially (%d station(s), params: %s) ..."
                                    % (mi + 1, len(ordered_modules), m, len(pts_to_fetch), ", ".join(needed_m)))
                                arcpy.SetProgressor("step", "Querying NASA POWER for %s..." % m, 0, len(pts_to_fetch), 1)
                                for step_i, (idx, p, missing_p) in enumerate(pts_to_fetch):
                                    pct = float(step_i + 1) / float(len(pts_to_fetch)) * 100.0
                                    msg("  [%s] Station %d/%d (%.0f%%) [OID %s | Lat: %.4f, Lon: %.4f] - Querying %s..." %
                                        (m, step_i + 1, len(pts_to_fetch), pct, p.get("oid", idx + 1), p["lat"], p["lon"], ",".join(missing_p)))
                                    key = (round(p["lat"], 4), round(p["lon"], 4), y0, y1, temporal, start_date_str, end_date_str, tuple(sorted(missing_p)))
                                    if key in nasa_cache:
                                        results[idx].setdefault("parameter", {}).update(nasa_cache[key])
                                        results[idx]["status"] = "OK"
                                    else:
                                        try:
                                            par = fetch_nasa_point(
                                                p["lat"], p["lon"], y0, y1, missing_p,
                                                temporal=temporal, session=sess,
                                                start_date=start_date_str, end_date=end_date_str)
                                            nasa_cache[key] = par
                                            results[idx].setdefault("parameter", {}).update(par)
                                            results[idx]["status"] = "OK"
                                        except Exception as ex:
                                            results[idx]["error"] = str(ex)[:500]
                                            results[idx]["status"] = "FAILED"
                                    arcpy.SetProgressorPosition(step_i + 1)
                                arcpy.ResetProgressor()
                            else:
                                msg("Element [%d/%d] %s: All required variables (%s) already cached in memory. Reusing with 0 queries."
                                    % (mi + 1, len(ordered_modules), m, ", ".join(needed_m)))

                        # Compute indicators for this element
                        msg("Element [%d/%d] %s: Computing indicators ..." % (mi + 1, len(ordered_modules), m))
                        for idx, rec in enumerate(results):
                            try:
                                if use_om:
                                    monthly = rec.get("monthly", {})
                                    daily_raw = rec.get("daily_raw", {})
                                    precip_totals = True
                                else:
                                    avail_p = list(rec.get("parameter", {}).keys())
                                    monthly, daily_raw = self._monthly_from_response(
                                        rec.get("parameter", {}), temporal, avail_p, years)
                                    precip_totals = False
                                    rec["monthly"] = monthly
                                    rec["daily_raw"] = daily_raw

                                if time_mode == "Custom Date Range" and d_start and d_end:
                                    start_ym = (d_start.year, d_start.month)
                                    end_ym = (d_end.year, d_end.month)
                                    for var, ym_dict in list(monthly.items()):
                                        if isinstance(ym_dict, dict):
                                            monthly[var] = dict((ym, v) for ym, v in ym_dict.items()
                                                                if start_ym <= ym <= end_ym)

                                f = compute_point_fields(monthly, years, [m], temporal,
                                                         daily_raw, precip_totals, gap_method,
                                                         lat=rec.get("lat", 0.0))
                                rec.setdefault("fields", {}).update(f)
                            except Exception as ex:
                                warn("Element '%s' failed at point %s: %s"
                                     % (m, rec.get("oid"), str(ex)[:200]))

                        if gap_method != "none":
                            spatial_impute_missing(results, [m])

                        for rec in results:
                            vals = rec.get("fields", {})
                            n_valid = sum(1 for v in vals.values() if v is not None)
                            if not rec.get("status") or rec["status"] == "PENDING":
                                rec["status"] = "OK" if n_valid > 0 else "FAILED"
                            if n_valid == 0 and rec.get("status") == "FAILED":
                                rec["error"] = "No valid values from " + provider

                        # Immediate GDB Layer Commit for this element
                        w_fields = wanted_fields_by_module.get(m, []) if wanted_fields_by_module else None
                        fc = self._build_single_element_layer(
                            tmp_base, gdb_path, results, m, admin_meta, msg, warn, wanted_fields=w_fields)
                        if fc and arcpy.Exists(fc):
                            element_fcs[m] = fc

                        # Immediate Export of Shapefile, CSV, Excel
                        short = MODULE_SHORT.get(m, m)
                        self._export_shapefile(fc, os.path.join(paths["shp"], short + ".shp"), msg, warn)
                        self._export_csv(fc, os.path.join(paths["vec"], short + ".csv"), msg, warn)

                        # Immediate Raster Interpolation
                        if not download_only and sa_avail:
                            elem_rasters = self._interpolate_all(
                                None, [m], paths, eff_base, interp, mask, msg, warn,
                                iopts, kopts, is_geo, purge, scratch_dir, focal,
                                {m: fc}, wanted_fields_by_module=wanted_fields_by_module)
                            raster_registry.extend(elem_rasters)
                            if purge and os.path.exists(scratch_dir):
                                for sf in os.listdir(scratch_dir):
                                    sfp = os.path.join(scratch_dir, sf)
                                    try:
                                        if os.path.isfile(sfp): os.remove(sfp)
                                    except Exception:
                                        pass
                            gc.collect()

                        msg(">>> Element [%d/%d] %s completed: Point layer, Shapefile, CSV, Excel & Rasters generated. <<<\n"
                            % (mi + 1, len(ordered_modules), m))

                finally:
                    if tmp_base_is_temp:
                        try:
                            arcpy.management.Delete(tmp_base)
                        except Exception:
                            pass

                n_data = sum(1 for r in results if r.get("status") == "OK")
                n_empty = len(results) - n_data
                ok_count = n_data
                fail = [(r["oid"], r.get("error", "")) for r in results
                        if r.get("status") != "OK"]
                msg("Data retrieved for %d/%d points%s." % (
                    n_data, len(results),
                    (" (%d without valid values)" % n_empty) if n_empty else ""))
                if results and n_data == 0:
                    raise RuntimeError(
                        "No point received valid values from %s. Check the failure reasons "
                        "above (network, server limits, or period outside coverage %d-%d); "
                        "fix and re-run instead of building an empty atlas."
                        % (provider, y0, y1))

            # Master Excel Workbook (.xls) containing all active modules
            try:
                master_sheets = []
                for m in ordered_modules:
                    short = MODULE_SHORT.get(m, m)
                    fc = element_fcs.get(m)
                    if fc and arcpy.Exists(fc):
                        f_names = [f.name for f in arcpy.ListFields(fc)
                                   if f.type not in ("Geometry", "Raster", "Blob")]
                        f_rows = []
                        with arcpy.da.SearchCursor(fc, f_names) as cur:
                            for r in cur:
                                f_rows.append(list(r))
                        master_sheets.append((short, f_names, f_rows, False))
                if master_sheets:
                    master_xls = os.path.join(paths["vec"], "Climate_Atlas_Master_Workbook.xls")
                    write_master_excel_workbook(master_xls, master_sheets)
                    msg("Master Excel Workbook: %s (%d sheets)" % (master_xls, len(master_sheets)))
            except Exception as ex:
                warn("Master Excel export warning: %s" % ex)

            wind_fcs = []
            iso_scheme, iso_step = "", None
            if download_only:
                msg("Download-only mode: skipping rasters, wind vectors and isobars.")
            else:

                if "Wind" in modules and sa_avail:
                    wind_w = wanted_fields_by_module.get("Wind", [])
                    has_spd = any("W_Spd" in f for f in wind_w)
                    has_dir = any("W_Dir" in f for f in wind_w)
                    if has_spd and has_dir:
                        try:
                            wind_fcs = self._build_wind_vectors(
                                gdb_path, paths, raster_registry, element_fcs.get("Wind"),
                                mask, out_sr, eff_wind, msg, warn)
                        except Exception as ex:
                            warn("Wind vectors failed: %s" % ex)

            iso_mods = [m for m in ("Sea Level Pressure", "Surface Pressure")
                        if m in modules]
            has_iso_r = any(r[3] in iso_mods for r in raster_registry)
            if create_isobars and iso_mods and sa_avail and has_iso_r:
                p_isch = pdict.get("Pressure_Interval_Scheme")
                _scheme = p_isch.valueAsText if (p_isch and p_isch.valueAsText) else "Global Standard (4 mbar)"
                p_istep = pdict.get("Custom_Pressure_Step")
                _stepv = p_istep.value if (p_istep and p_istep.value is not None) else 4.0
                if _scheme == "Custom Interval":
                    iso_step = float(_stepv) if _stepv is not None else 4.0
                elif _scheme.startswith("Local"):
                    iso_step = 2.0
                else:
                    iso_step = 4.0
                iso_scheme = _scheme
                if iso_step <= 0:
                    warn("Isobar step must be > 0; using 4.0 mbar.")
                    iso_step = 4.0
                msg("Isobars (%s, step %.2f mbar) for: %s."
                    % (_scheme, iso_step, ", ".join(iso_mods)))
                try:
                    self._build_isobars(gdb_path, raster_registry, msg, warn, iso_step)
                except Exception as ex:
                    warn("Isobars failed: %s" % ex)
            elif create_isobars and not iso_mods:
                warn("Create_Isobars checked but no pressure module selected: skipped.")

            self._write_dictionaries(paths["vec"], active_export_modules, msg, provider,
                                     wanted_fields_by_module=wanted_fields_by_module)
            qa = self._run_qa(element_fcs, paths, active_export_modules, raster_registry, results, msg, warn,
                              wanted_fields_by_module=wanted_fields_by_module)

            if is_offline:
                _first_fc = element_fcs.values()[0] if element_fcs else None
                _n_pts = int(arcpy.GetCount_management(_first_fc)[0]) if (_first_fc and arcpy.Exists(_first_fc)) else 0
                _n_ok = _n_pts
                _fail = []
            else:
                _n_pts = len(pts)
                _n_ok = ok_count
                _fail = fail

            self._write_log(paths["vec"], {
                "tool_version": TOOL_VERSION, "modules": active_export_modules,
                "submodels": active_submodels, "years": (y0, y1, len(years)),
                "temporal": temporal, "interp": interp_label, "provider": provider,
                "interp_detail": {"idw": iopts, "krig": kopts},
                "base_cell": base_cell,
                "wind_cell": wind_cell, "n_points": _n_pts, "n_ok": _n_ok,
                "n_fail": len(_fail), "failed": _fail[:50], "rasters": raster_registry,
                "wind": wind_fcs, "warnings": warnings, "qa": qa,
                "elapsed": time.time() - t_start,
                "purge": purge, "add_to_map": add_to_map,
                "tol_m": tol_m, "focal": focal, "dl_only": download_only,
                "element_layers": element_fcs,
                "iso": (iso_scheme, iso_step),
            })
            if add_to_map and not download_only:
                p_map_mods = pdict.get("Map_Add_Modules")
                _mtxt = p_map_mods.valueAsText if (p_map_mods and p_map_mods.valueAsText) else ""
                map_modules = [m.strip().strip("'\"") for m in _mtxt.split(";")
                               if m.strip().strip("'\"")]
                map_modules = [m for m in map_modules if m in active_export_modules]
                if not map_modules:
                    warn("Add to map: no selected element was computed; nothing added.")
                else:
                    self._add_to_map(raster_registry, wind_fcs, map_modules,
                                     msg, warn)
            self._cleanup(msg, scratch_dir, purge)
            try:
                arcpy.CheckInExtension("Spatial")
            except Exception:
                pass
            msg("Done in %.1fs. Outputs in %s" % (time.time() - t_start, out_ws))
        except Exception as ex:
            tb = traceback.format_exc()
            messages.addErrorMessage("FAILED: %s\n%s" % (ex, tb))
            raise

    def _add_to_map(self, registry, wind_fcs, map_modules, msg, warn):
        """Add chosen elements to the CURRENT ArcMap data frame, one group layer
        per element. Element .lyr rasters go to the bottom of each group.

        Group strategy (best effort, never fails the run):
          1. a group with the element name already exists -> add inside it,
          2. else create the group via ArcObjects automation (needs running ArcMap),
          3. else add the element layers flat with a warning.
        Outside ArcMap (no CURRENT document) it logs a warning and returns."""

        def _find_group(mxd, df, name):
            try:
                for l in arcpy.mapping.ListLayers(mxd, "", df):
                    if getattr(l, "isGroupLayer", False) and l.name == name:
                        return l
            except Exception:
                pass
            return None

        def _create_group(mxd, df, name):
            found = _find_group(mxd, df, name)
            if found is not None:
                return found
            try:
                from comtypes.client import GetActiveObject, CreateObject
                app = GetActiveObject("esriArcMap.Application")
                focus_map = app.Document.FocusMap
                grp = CreateObject("esriCarto.GroupLayer")
                grp.Name = name
                focus_map.AddLayer(grp)
                try:
                    app.Document.UpdateContents()
                    app.Document.ActiveView.Refresh()
                except Exception:
                    pass
                return _find_group(mxd, df, name)
            except Exception as ex:
                warn("Group '%s' could not be created (%s); layers added flat."
                     % (name, str(ex)[:120]))
                return None

        try:
            mxd = arcpy.mapping.MapDocument("CURRENT")
        except Exception as ex:
            warn("Add to map skipped (not running inside ArcMap): %s" % ex)
            return
        try:
            dfs = arcpy.mapping.ListDataFrames(mxd)
            if not dfs:
                warn("Add to map skipped (no data frame in current map).")
                return
            df = dfs[0]
            by_module = {}
            for (_f, _r, lp, _m, _c, _n) in registry:
                by_module.setdefault(_m, []).append(lp)
            added = 0
            for module in map_modules:
                lps = by_module.get(module, [])
                extras = []
                if module == "Wind":
                    extras = [w for w in (wind_fcs or []) if arcpy.Exists(w)]
                if not lps and not extras:
                    warn("Add to map: element '%s' has no outputs; skipped." % module)
                    continue
                gname = MODULE_FOLDER.get(module, module)
                grp = _create_group(mxd, df, gname)
                for lp in lps + extras:
                    try:
                        if not lp or not arcpy.Exists(lp):
                            continue
                        layer = arcpy.mapping.Layer(lp)
                        if grp is not None:
                            arcpy.mapping.AddLayerToGroup(df, grp, layer, "BOTTOM")
                        else:
                            arcpy.mapping.AddLayer(df, layer, "BOTTOM")
                        added += 1
                    except Exception as ex:
                        warn("Could not add %s to map: %s" % (lp, ex))
                msg("Element '%s' added (%d layers%s)." % (
                    module, len(lps) + len(extras),
                    " in group '%s'" % gname if grp is not None else ", flat"))
            try:
                arcpy.RefreshActiveView()
                arcpy.RefreshTOC()
            except Exception:
                pass
            msg("Added %d layers to the current map." % added)
        except Exception as ex:
            warn("Add to map failed: %s" % ex)

    # ================= helpers (arcpy) =================
    def _build_layout(self, out_ws, modules, gdb_name=None):
        makedirs_ok(out_ws)
        if not gdb_name:
            gdb_name = "Climate_Database.gdb"
        if not gdb_name.lower().endswith(".gdb"):
            gdb_name += ".gdb"
        gdb_path = os.path.join(out_ws, gdb_name)
        if not arcpy.Exists(gdb_path):
            arcpy.management.CreateFileGDB(out_ws, gdb_name)
        paths = {"gdb": gdb_path, "vec": os.path.join(out_ws, "00_Vector_Data"),
                 "shp": os.path.join(out_ws, "Export_SHP")}
        makedirs_ok(paths["vec"])
        makedirs_ok(paths["shp"])
        for m in modules:
            folder = os.path.join(out_ws, MODULE_FOLDER[m])
            if m == "Wind":
                for sub in ["Speed/Rasters", "Speed/Layers", "Direction/Rasters",
                            "Direction/Layers", "Direction/Vector_Points"]:
                    makedirs_ok(os.path.join(folder, sub))
            else:
                makedirs_ok(os.path.join(folder, "Rasters"))
                makedirs_ok(os.path.join(folder, "Layers"))
        for d in ["10_Derived_Models/Aridity_Index", "10_Derived_Models/Water_Balance",
                  "10_Derived_Models/Thermal_Comfort", "10_Derived_Models/Other_Models"]:
            makedirs_ok(os.path.join(out_ws, d))
        return gdb_path, paths

    def _extract_points(self, in_points, wgs, messages):
        d = arcpy.Describe(in_points)
        oid_field = d.OIDFieldName
        in_sr = d.spatialReference
        pts = []
        with arcpy.da.SearchCursor(in_points, [oid_field, "SHAPE@XY"]) as cur:
            for row in cur:
                try:
                    x, y = row[1][0], row[1][1]
                    try:
                        need_reproj = (in_sr.factoryCode != 4326)
                    except Exception:
                        need_reproj = (in_sr.name != wgs.name)
                    if need_reproj:
                        pt = arcpy.PointGeometry(arcpy.Point(x, y), in_sr).projectAs(wgs)
                        lon, lat = pt.centroid.X, pt.centroid.Y
                    else:
                        lon, lat = x, y
                    pts.append({"oid": row[0], "lat": float(lat), "lon": float(lon)})
                except Exception:
                    continue
        return pts

    def _query_all(self, pts, y0, y1, params, temporal, messages, msg, warn, tag="",
                   start_date=None, end_date=None):
        # Sequential in-order queries (one point at a time). On 32-bit ArcMap this
        # keeps peak memory minimal (each response is processed and released before
        # the next), avoids NASA API rate-limiting from parallel bursts, and gives
        # a steady, predictable progress bar. A single reused HTTP session plus an
        # in-run cache for duplicate coordinates keeps it efficient.
        cache = {}
        sess = None
        if _HAS_REQUESTS:
            try:
                sess = requests.Session()
            except Exception:
                sess = None
        msg("Querying NASA POWER sequentially%s (timeout 60s, 3 retries per point) ..."
            % ((" [%s]" % tag) if tag else ""))
        results = []
        arcpy.SetProgressor("step", "Querying NASA POWER ...", 0, len(pts), 1)
        for idx, p in enumerate(pts):
            key = (round(p["lat"], 4), round(p["lon"], 4), y0, y1, temporal, start_date, end_date)
            if key in cache:
                results.append(dict(p, parameter=cache[key], status="OK", error=""))
            else:
                try:
                    par = fetch_nasa_point(p["lat"], p["lon"], y0, y1, params,
                                           temporal=temporal, session=sess,
                                           start_date=start_date, end_date=end_date)
                    cache[key] = par
                    results.append(dict(p, parameter=par, status="OK", error=""))
                except Exception as ex:
                    results.append(dict(p, parameter={}, status="FAILED", error=str(ex)[:500]))
            if (idx + 1) % 10 == 0 or (idx + 1) == len(pts):
                arcpy.SetProgressorPosition(idx + 1)
                msg("  NASA %d/%d ..." % (idx + 1, len(pts)))
        arcpy.ResetProgressor()
        ok = 0
        fail = []
        for r in results:
            if r["status"] == "OK":
                ok += 1
            else:
                fail.append((r["oid"], r.get("error", "")))
        if fail:
            warn("%d NASA queries failed (kept as FAILED, process continues). e.g. %s"
                 % (len(fail), fail[:3]))
        return results, ok, fail

    def _monthly_from_response(self, parameter, temporal, needed, years):
        monthly, daily_raw = {}, {}
        if temporal == "Monthly":
            for p in needed:
                monthly[p] = parse_monthly_series(parameter.get(p, {}))
        else:
            mean_ps = [p for p in needed if p != "PRECTOTCORR"]
            m = build_monthly_from_daily(parameter, mean_ps, ["PRECTOTCORR"], years)
            monthly.update(m)
            for p in needed:
                daily_raw[p] = parse_daily_series(parameter.get(p, {}))
        return monthly, daily_raw

    def _query_all_om(self, pts, y0, y1, modules, temporal, messages, msg, warn, tag="",
                      model="era5_land", start_date=None, end_date=None):
        """Sequential Open-Meteo queries with a one-time variable probe."""
        msg("Probing Open-Meteo variable availability ...")
        daily_vars, hourly_vars, dropped, note = om_probe_vars(
            modules, model=model, start_date=start_date, end_date=end_date)
        if note:
            warn(note)
        if not daily_vars and not hourly_vars:
            return ([dict(p, monthly={}, daily_raw={}, status="FAILED",
                          error="Open-Meteo: no usable variables") for p in pts],
                    0, [(p["oid"], "no usable variables") for p in pts])
        msg("Querying Open-Meteo archive (%s) sequentially%s ..."
            % (model, (" [%s]" % tag) if tag else ""))
        results = []
        arcpy.SetProgressor("step", "Querying Open-Meteo ...", 0, len(pts), 1)
        for idx, p in enumerate(pts):
            try:
                monthly, daily_raw, _drop = fetch_openmeteo_point(
                    p["lat"], p["lon"], y0, y1, modules,
                    daily_vars=daily_vars, hourly_vars=hourly_vars,
                    model=model, start_date=start_date, end_date=end_date)
                if temporal != "Daily":
                    # spec: R_Max_Daily_Month / rain days are Daily-mode indicators only
                    results.append(dict(p, monthly=monthly, daily_raw={},
                                        status="OK", error=""))
                else:
                    results.append(dict(p, monthly=monthly, daily_raw=daily_raw,
                                        status="OK", error=""))
            except Exception as ex:
                results.append(dict(p, monthly={}, daily_raw={}, status="FAILED",
                                    error=str(ex)[:500]))
            if (idx + 1) % 10 == 0 or (idx + 1) == len(pts):
                arcpy.SetProgressorPosition(idx + 1)
                msg("  Open-Meteo %d/%d ..." % (idx + 1, len(pts)))
        arcpy.ResetProgressor()
        ok = 0
        fail = []
        for r in results:
            if r["status"] == "OK":
                ok += 1
            else:
                fail.append((r["oid"], r.get("error", "")))
        if fail:
            warn("%d Open-Meteo queries failed (kept as FAILED, process continues). e.g. %s"
                 % (len(fail), fail[:3]))
        return results, ok, fail

    def _export_shapefile(self, fc, shp_path, msg, warn):
        """Export one feature class to an exact .shp path (+ sidecars).

        Long (>10 char) field names are truncated on a temp copy via
        SHP_FIELD_MAP; the GDB keeps full names."""
        tmp_copy = "in_memory/shp_tmp"
        export_fc = fc
        try:
            try:
                arcpy.management.Delete(tmp_copy)
            except Exception:
                pass
            current = set(f.name for f in arcpy.ListFields(fc))
            long_names = [n for n in SHP_FIELD_MAP if n in current]
            if long_names:
                arcpy.management.CopyFeatures(fc, tmp_copy)
                for n in long_names:
                    try:
                        arcpy.management.AlterField(tmp_copy, n, SHP_FIELD_MAP[n], SHP_FIELD_MAP[n])
                    except Exception as ex:
                        warn("Shapefile field rename %s->%s failed: %s" % (n, SHP_FIELD_MAP[n], ex))
                export_fc = tmp_copy
        except Exception as ex:
            warn("Shapefile prep failed, exporting as-is: %s" % ex)
        try:
            makedirs_ok(os.path.dirname(shp_path))
            try:
                if arcpy.Exists(shp_path):
                    arcpy.management.Delete(shp_path)
            except Exception:
                pass
            arcpy.conversion.FeatureClassToShapefile([export_fc], os.path.dirname(shp_path))
            got = os.path.join(os.path.dirname(shp_path),
                               arcpy.Describe(export_fc).baseName + ".shp")
            if os.path.abspath(got) != os.path.abspath(shp_path) and os.path.isfile(got):
                stem_got = os.path.splitext(got)[0]
                stem_want = os.path.splitext(shp_path)[0]
                for ext in [".shp", ".shx", ".dbf", ".prj", ".cpg", ".sbn", ".sbx", ".xml", ".shp.xml"]:
                    src, dst = stem_got + ext, stem_want + ext
                    if os.path.isfile(src):
                        try:
                            if os.path.isfile(dst):
                                os.remove(dst)
                            os.rename(src, dst)
                        except Exception:
                            pass
            msg("Shapefile: %s" % shp_path)
            if export_fc != fc:
                warn("Shapefile truncations applied (GDB keeps full names): %s"
                     % ", ".join("%s->%s" % (k, SHP_FIELD_MAP[k]) for k in SHP_FIELD_MAP))
        except Exception as ex:
            warn("Shapefile export failed: %s" % ex)
        finally:
            try:
                if tmp_copy and arcpy.Exists(tmp_copy):
                    arcpy.management.Delete(tmp_copy)
            except Exception:
                pass

    def _export_csv(self, fc, csv_path, msg, warn):
        try:
            fields = [f.name for f in arcpy.ListFields(fc)
                      if f.type not in ("Geometry", "Raster", "Blob")]
            rows = []
            with arcpy.da.SearchCursor(fc, fields) as cur:
                for r in cur:
                    rows.append(list(r))
            write_csv(csv_path, fields, rows)
            msg("CSV: %s" % csv_path)
            xls_path = os.path.splitext(csv_path)[0] + ".xls"
            write_excel_file(xls_path, fields, rows, sheet_name="Data", rtl=False)
            msg("Excel: %s" % xls_path)
        except Exception as ex:
            warn("CSV/Excel export failed: %s" % ex)

    def _interp_surface(self, in_points, field, cell, method, iopts=None, kopts=None):
        iopts = iopts or {"power": 1.2, "search": "Variable", "npoints": 12, "maxdist": None,
                          "spline_type": "Tension", "spline_weight": 5.0, "spline_npoints": 12}
        kopts = kopts or {"model": "Spherical", "ktype": "Ordinary", "npoints": 12}
        if method == "IDW":
            from arcpy.sa import Idw, RadiusVariable, RadiusFixed
            power = float(iopts.get("power", 1.2))
            npts = max(1, int(iopts.get("npoints", 12)))
            maxdist = iopts.get("maxdist")
            if (iopts.get("search") or "Variable") == "Fixed":
                rr = RadiusFixed(float(maxdist), npts)
            elif maxdist:
                rr = RadiusVariable(npts, float(maxdist))
            else:
                rr = RadiusVariable(npts)
            return Idw(in_points, field, cell, power, rr)
        if method == "Ordinary Kriging":
            from arcpy.sa import Kriging, RadiusVariable
            model = kopts.get("model", "Spherical")
            npts = max(1, int(kopts.get("npoints", 12)))
            clsname = "KrigingModel" + ("Universal" if kopts.get("ktype") == "Universal"
                                        else "Ordinary")
            try:
                krmodel = getattr(arcpy.sa, clsname)(model)
            except Exception:
                krmodel = model  # string form (Ordinary) as fallback
            return Kriging(in_points, field, krmodel, cell, RadiusVariable(npts))
        if method == "Spline" or str(method).startswith("Spline"):
            from arcpy.sa import Spline
            stype = str(iopts.get("spline_type", "Tension")).upper() if iopts else "TENSION"
            weight = float(iopts.get("spline_weight", 5.0)) if iopts else 5.0
            npts = max(1, int(iopts.get("spline_npoints", 12))) if iopts else 12
            return Spline(in_points, field, cell, stype, weight, npts)
        from arcpy.sa import NaturalNeighbor
        return NaturalNeighbor(in_points, field, cell)

    def _raster_paths(self, out_ws, module, field):
        folder = MODULE_FOLDER[module]
        if module == "Wind":
            sub = "Speed" if field.startswith("W_Spd") else "Direction"
            rdir = os.path.join(out_ws, folder, sub, "Rasters")
            ldir = os.path.join(out_ws, folder, sub, "Layers")
        else:
            rdir = os.path.join(out_ws, folder, "Rasters")
            ldir = os.path.join(out_ws, folder, "Layers")
        return os.path.join(rdir, field + ".tif"), os.path.join(ldir, field + ".lyr")

    def _module_of_field(self, field):
        for m, fs in MODULE_FIELDS.items():
            if field in fs:
                return m
        return None

    def _colors_for(self, module, field):
        if module == "Wind":
            if field.startswith("W_Spd"):
                return COLOR_RAMPS["Wind_Speed"]
            return COLOR_RAMPS["Wind_Direction"]
        if module == "UV Index":
            return COLOR_RAMPS["UV Index"]
        if field.startswith("HI_"):
            return COLOR_RAMPS["Temperature"]
        return COLOR_RAMPS.get(module, COLOR_RAMPS["Temperature"])

    def _build_display(self, rp, field, module, colors, nclass, msg, warn, purge=True):
        """Classified display raster for real on-open colors in ArcMap.

        Slice (equal interval) -> integer zones -> VAT -> .clr colormap applied
        with AddColormap (all core-license tools). Zones are REMAPPED so zone 1
        is the HIGHEST interval (descending legend) with colors matched (hottest
        color on the highest zone). Returns (cls_path, clr_path) or (None, None)
        on failure (caller falls back to the continuous raster).
        """
        from arcpy.sa import Slice
        rdir = os.path.dirname(rp)
        ldir = rdir.replace("Rasters", "Layers")
        cls_rp = os.path.join(rdir, field + "_cls.tif")
        clr_path = os.path.join(ldir, field + ".clr")
        ztmp = os.path.join(rdir, field + "_z.tif")
        try:
            for _f in (cls_rp, ztmp):
                try:
                    if arcpy.Exists(_f):
                        arcpy.management.Delete(_f)
                except Exception:
                    pass
            try:
                Slice(rp, nclass, "EQUAL_INTERVAL").save(ztmp)
                # descending remap: zone 1 = highest interval
                (nclass + 1 - arcpy.Raster(ztmp)).save(cls_rp)
                if purge:
                    try:
                        arcpy.management.Delete(ztmp)
                    except Exception:
                        pass
                zone_colors = [hex_to_rgb(colors[nclass - k]) for k in range(1, nclass + 1)]
            except Exception:
                # constant raster: Slice cannot build intervals -> single zone
                try:
                    _mn = float(arcpy.GetRasterProperties_management(rp, "MINIMUM")[0])
                    _mx = float(arcpy.GetRasterProperties_management(rp, "MAXIMUM")[0])
                except Exception:
                    _mn, _mx = None, None
                if _mn is None or abs(_mx - _mn) > 1e-9:
                    raise
                (arcpy.Raster(rp) * 0 + 1).save(cls_rp)
                mid = colors[len(colors) // 2]
                zone_colors = [hex_to_rgb(mid)]
                msg("Display for %s: constant raster, single zone." % field)
            try:
                arcpy.management.BuildRasterAttributeTable(cls_rp)
            except Exception as ex:
                warn("VAT build for %s display skipped: %s" % (field, ex))
            with open(clr_path, "w") as fh:
                for i, rgb in enumerate(zone_colors):
                    fh.write("%d %d %d %d\n" % (i + 1, rgb[0], rgb[1], rgb[2]))
            try:
                arcpy.management.AddColormap(cls_rp, "#", clr_path)
            except Exception as ex:
                warn("Colormap for %s display skipped: %s" % (field, ex))
            return cls_rp, clr_path
        except Exception as ex:
            warn("Classified display for %s failed (%s); layer will use the raw raster."
                 % (field, ex))
    def _merge_offline_layers(self, in_layers_text, gdb_path, out_sr, modules,
                              active_submodels, wanted_fields_by_module, msg, warn):
        """Merges one or more precalculated point layers (multi-value) offline by coordinates/Source_ID.
        Computes requested applied submodels on the fly, builds primary element layers,
        and creates a dedicated 'Climate_Models' feature class in the GDB.
        Returns dict {module: fc_path}."""
        element_fcs = {}
        layer_paths = [lp.strip().strip("'\"") for lp in (in_layers_text or "").split(";") if lp.strip().strip("'\"")]
        if not layer_paths:
            raise RuntimeError("No precalculated point layers provided for offline mode.")

        msg("Offline multi-layer processing: inspecting %d input layer(s) ..." % len(layer_paths))
        wgs_sr = arcpy.SpatialReference(4326)

        # 1. Base layer for geometry and projection
        base_layer = layer_paths[0]
        tmp_base = safe_project_fc(base_layer, out_sr, gdb_path, "offbase", warn)
        tmp_is_temp = (tmp_base != base_layer)

        try:
            # 2. Extract geometries and coordinates from base layer
            point_records = []
            coord_to_idx = {}
            oid_to_idx = {}
            base_desc = arcpy.Describe(tmp_base)
            oid_field = base_desc.OIDFieldName

            with arcpy.da.SearchCursor(tmp_base, [oid_field, "SHAPE@"]) as cur:
                idx = 0
                for row in cur:
                    oid_val = row[0]
                    geom = row[1]
                    lat, lon = None, None
                    try:
                        if geom:
                            pt_wgs = geom.projectAs(wgs_sr)
                            lat, lon = float(pt_wgs.centroid.Y), float(pt_wgs.centroid.X)
                    except Exception:
                        pass
                    ckey = (round(lat, 4), round(lon, 4)) if (lat is not None and lon is not None) else None
                    rec = {
                        "oid": oid_val,
                        "geom": geom,
                        "lat": lat,
                        "lon": lon,
                        "fields": {}
                    }
                    point_records.append(rec)
                    if ckey:
                        coord_to_idx[ckey] = idx
                    oid_to_idx[oid_val] = idx
                    idx += 1

            msg("  Base geometry layer: %s (%d points)" % (os.path.basename(base_layer), len(point_records)))

            # 3. Read attributes from all input layers and merge by coordinates / OID
            for lyr in layer_paths:
                lyr_desc = arcpy.Describe(lyr)
                lyr_oid = lyr_desc.OIDFieldName
                all_fields = [f.name for f in arcpy.ListFields(lyr)
                              if f.type not in ("Geometry", "Raster", "Blob")]
                val_fields = [f for f in all_fields if f != lyr_oid]

                with arcpy.da.SearchCursor(lyr, [lyr_oid, "SHAPE@"] + val_fields) as cur:
                    for row in cur:
                        l_oid = row[0]
                        l_geom = row[1]
                        l_lat, l_lon = None, None
                        try:
                            if l_geom:
                                pt_w = l_geom.projectAs(wgs_sr)
                                l_lat, l_lon = float(pt_w.centroid.Y), float(pt_w.centroid.X)
                        except Exception:
                            pass
                        ckey = (round(l_lat, 4), round(l_lon, 4)) if (l_lat is not None and l_lon is not None) else None
                        match_idx = coord_to_idx.get(ckey)
                        if match_idx is None:
                            match_idx = oid_to_idx.get(l_oid)

                        if match_idx is not None and match_idx < len(point_records):
                            target_fields = point_records[match_idx]["fields"]
                            for fname, val in zip(val_fields, row[2:]):
                                canonical = REV_SHP_MAP.get(fname, fname)
                                if val is not None and not is_missing(val):
                                    if canonical not in target_fields or target_fields[canonical] is None:
                                        target_fields[canonical] = val

            # 4. On-the-fly computation of active applied submodels if missing
            if active_submodels:
                msg("Computing applied submodels for offline points ...")
                for rec in point_records:
                    f = rec["fields"]
                    pt_lat = rec.get("lat") or 0.0

                    t_val = (f.get("T_Annual_Mean") if f.get("T_Annual_Mean") is not None else
                             (f.get("T_AnnMean") if f.get("T_AnnMean") is not None else f.get("T2M")))
                    p_val = (f.get("R_Annual_Total") if f.get("R_Annual_Total") is not None else
                             (f.get("R_AnnTot") if f.get("R_AnnTot") is not None else
                              (f.get("R_AnnTotal") if f.get("R_AnnTotal") is not None else f.get("PRECTOTCORR"))))
                    tx_val = (f.get("T_Annual_Max_Mean") if f.get("T_Annual_Max_Mean") is not None else
                              (f.get("T_MaxMean") if f.get("T_MaxMean") is not None else f.get("T2M_MAX")))
                    if tx_val is None and t_val is not None:
                        tx_val = float(t_val) + 5.0
                    tn_val = (f.get("T_Annual_Min_Mean") if f.get("T_Annual_Min_Mean") is not None else
                              (f.get("T_MinMean") if f.get("T_MinMean") is not None else f.get("T2M_MIN")))
                    if tn_val is None and t_val is not None:
                        tn_val = float(t_val) - 5.0
                    rh_val = (f.get("RH_Summer_Mean") if f.get("RH_Summer_Mean") is not None else
                              (f.get("RH_SuMean") if f.get("RH_SuMean") is not None else
                               (f.get("RH_Annual_Mean") if f.get("RH_Annual_Mean") is not None else
                                (f.get("RH_AnMean") if f.get("RH_AnMean") is not None else f.get("RH2M")))))

                    # De Martonne
                    if any("De Martonne" in s for s in active_submodels):
                        if f.get("DM_Aridity_Annual") is None and t_val is not None and p_val is not None:
                            t_f, p_f = float(t_val), float(p_val)
                            f["DM_Aridity_Annual"] = round(p_f / (t_f + 10.0), 2) if (t_f + 10.0) > 0.01 else 0.0

                    # Hargreaves PET
                    if any("Hargreaves" in s or "UNEP" in s or "Water Deficit" in s for s in active_submodels):
                        if f.get("PET_Hargreaves_Annual") is None and t_val is not None and tx_val is not None and tn_val is not None:
                            t_f, tx_f, tn_f = float(t_val), float(tx_val), float(tn_val)
                            ra_ann = sum(extraterrestrial_radiation_ra(pt_lat, m) for m in range(1, 13))
                            tdiff = max(0.0, tx_f - tn_f)
                            pet_ann = 0.0023 * ra_ann * 30.4 * (t_f + 17.8) * math.sqrt(tdiff)
                            f["PET_Hargreaves_Annual"] = round(max(0.0, pet_ann), 1)

                    # UNEP Aridity
                    if any("UNEP" in s for s in active_submodels):
                        if f.get("UNEP_Aridity_Annual") is None and p_val is not None and f.get("PET_Hargreaves_Annual") is not None:
                            pet_f = float(f["PET_Hargreaves_Annual"])
                            f["UNEP_Aridity_Annual"] = round(float(p_val) / pet_f, 3) if pet_f > 0.01 else 0.0

                    # Water Deficit
                    if any("Water Deficit" in s for s in active_submodels):
                        if f.get("Water_Deficit_Annual") is None and p_val is not None and f.get("PET_Hargreaves_Annual") is not None:
                            f["Water_Deficit_Annual"] = round(float(p_val) - float(f["PET_Hargreaves_Annual"]), 1)

                    # Walter-Lieth Dry Months
                    if any("Walter-Lieth" in s for s in active_submodels):
                        if f.get("Dry_Months_Count") is None and p_val is not None and t_val is not None:
                            p_f, t_f = float(p_val), float(t_val)
                            if p_f < 2.0 * t_f * 12.0:
                                f["Dry_Months_Count"] = int(min(12, max(1, 12.0 * (1.0 - (p_f / max(1.0, 24.0 * t_f))))))
                            else:
                                f["Dry_Months_Count"] = 0

                    # Heat Index
                    if any("Heat Index" in s for s in active_submodels):
                        if f.get("HI_Summer_Mean") is None and t_val is not None and rh_val is not None:
                            hi = heat_index_c(float(t_val), float(rh_val))
                            if hi is not None:
                                f["HI_Summer_Mean"] = round(hi, 2)
                                f["HI_Annual_Mean"] = round(hi, 2)

            # 5. Create primary element feature classes in GDB
            admin_names = [a[0] for a in ADMIN_FIELDS]
            for m in modules:
                short = MODULE_SHORT.get(m, m)
                fc = os.path.join(gdb_path, short)
                try:
                    if arcpy.Exists(fc):
                        arcpy.management.Delete(fc)
                except Exception:
                    pass
                arcpy.management.CopyFeatures(tmp_base, fc)
                existing = set(f.name for f in arcpy.ListFields(fc))
                for name, typ, _alias in ADMIN_FIELDS:
                    if name not in existing:
                        if typ == "TEXT":
                            arcpy.management.AddField(fc, name, typ, field_length=255)
                        else:
                            arcpy.management.AddField(fc, name, typ)
                wanted = wanted_fields_by_module.get(m, MODULE_FIELDS.get(m, []))
                for wf in wanted:
                    if wf not in existing:
                        arcpy.management.AddField(fc, wf, "DOUBLE")
                oid_name = arcpy.Describe(fc).OIDFieldName
                with arcpy.da.UpdateCursor(fc, [oid_name, "SHAPE@"] + admin_names + wanted) as ucur:
                    for row in ucur:
                        pt_g = row[1]
                        lat_v, lon_v = None, None
                        try:
                            if pt_g:
                                p_wgs = pt_g.projectAs(wgs_sr)
                                lat_v, lon_v = float(p_wgs.centroid.Y), float(p_wgs.centroid.X)
                        except Exception:
                            pass
                        ck = (round(lat_v, 4), round(lon_v, 4)) if (lat_v is not None and lon_v is not None) else None
                        p_idx = coord_to_idx.get(ck) if ck else oid_to_idx.get(row[0])
                        rec_f = point_records[p_idx]["fields"] if (p_idx is not None and p_idx < len(point_records)) else {}
                        admin_vals = [
                            rec_f.get("Source_ID", row[0]),
                            lat_v,
                            lon_v,
                            rec_f.get("Data_Start", 0),
                            rec_f.get("Data_End", 0),
                            rec_f.get("Temporal", "Precalculated"),
                            rec_f.get("Interp_Meth", "Offline"),
                            rec_f.get("Cell_Size", 0.0),
                            rec_f.get("Wind_Cell", 0.0),
                            rec_f.get("Status", "OK"),
                            (rec_f.get("Error_Msg", "") or "")[:255]
                        ]
                        for ai, aval in enumerate(admin_vals):
                            row[2 + ai] = aval
                        for wi, wf in enumerate(wanted):
                            row[2 + len(admin_names) + wi] = rec_f.get(wf)
                        ucur.updateRow(row)
                element_fcs[m] = fc
                msg("Element layer '%s': %s" % (m, fc))

            # 6. Create dedicated Climate_Models feature class in GDB if submodels active
            if active_submodels:
                models_fc = os.path.join(gdb_path, "Climate_Models")
                try:
                    if arcpy.Exists(models_fc):
                        arcpy.management.Delete(models_fc)
                except Exception:
                    pass
                arcpy.management.CopyFeatures(tmp_base, models_fc)
                existing_m = set(f.name for f in arcpy.ListFields(models_fc))
                for name, typ, _alias in ADMIN_FIELDS:
                    if name not in existing_m:
                        if typ == "TEXT":
                            arcpy.management.AddField(models_fc, name, typ, field_length=255)
                        else:
                            arcpy.management.AddField(models_fc, name, typ)
                sub_wanted = wanted_fields_by_module.get("Climate_Models", [])
                for sf in sub_wanted:
                    if sf not in existing_m:
                        field_type = "LONG" if sf == "Dry_Months_Count" else "DOUBLE"
                        arcpy.management.AddField(models_fc, sf, field_type)
                oid_m = arcpy.Describe(models_fc).OIDFieldName
                with arcpy.da.UpdateCursor(models_fc, [oid_m, "SHAPE@"] + admin_names + sub_wanted) as ucur:
                    for row in ucur:
                        pt_g = row[1]
                        lat_v, lon_v = None, None
                        try:
                            if pt_g:
                                p_wgs = pt_g.projectAs(wgs_sr)
                                lat_v, lon_v = float(p_wgs.centroid.Y), float(p_wgs.centroid.X)
                        except Exception:
                            pass
                        ck = (round(lat_v, 4), round(lon_v, 4)) if (lat_v is not None and lon_v is not None) else None
                        p_idx = coord_to_idx.get(ck) if ck else oid_to_idx.get(row[0])
                        rec_f = point_records[p_idx]["fields"] if (p_idx is not None and p_idx < len(point_records)) else {}
                        admin_vals = [
                            rec_f.get("Source_ID", row[0]),
                            lat_v,
                            lon_v,
                            rec_f.get("Data_Start", 0),
                            rec_f.get("Data_End", 0),
                            rec_f.get("Temporal", "Precalculated"),
                            rec_f.get("Interp_Meth", "Offline"),
                            rec_f.get("Cell_Size", 0.0),
                            rec_f.get("Wind_Cell", 0.0),
                            rec_f.get("Status", "OK"),
                            (rec_f.get("Error_Msg", "") or "")[:255]
                        ]
                        for ai, aval in enumerate(admin_vals):
                            row[2 + ai] = aval
                        for wi, sf in enumerate(sub_wanted):
                            row[2 + len(admin_names) + wi] = rec_f.get(sf)
                        ucur.updateRow(row)
                element_fcs["Climate_Models"] = models_fc
                msg("Climate Models layer: %s (%d indicators)" % (models_fc, len(sub_wanted)))

        finally:
            if tmp_is_temp:
                try:
                    arcpy.management.Delete(tmp_base)
                except Exception:
                    pass

        return element_fcs

    def _build_single_element_layer(self, tmp_projected, gdb_path, results, m,
                                    admin_meta, msg, warn, wanted_fields=None):
        """Builds one point Feature Class in GDB for a single climate element."""
        fc = os.path.join(gdb_path, MODULE_SHORT.get(m, m))
        try:
            if arcpy.Exists(fc):
                arcpy.management.Delete(fc)
            arcpy.management.CopyFeatures(tmp_projected, fc)
            existing = set(f.name for f in arcpy.ListFields(fc))
            for name, typ, _alias in ADMIN_FIELDS:
                if name not in existing:
                    if typ == "TEXT":
                        arcpy.management.AddField(fc, name, typ, field_length=255)
                    else:
                        arcpy.management.AddField(fc, name, typ)
            if wanted_fields is not None:
                wanted = wanted_fields
            else:
                wanted = MODULE_FIELDS.get(m, [])
            for f in wanted:
                if f not in existing:
                    arcpy.management.AddField(fc, f, "DOUBLE")

            by_oid = dict((r.get("oid"), r) for r in results if r.get("oid") is not None)
            by_coord = {}
            for r in results:
                if r.get("lat") is not None and r.get("lon") is not None:
                    by_coord[(round(float(r["lat"]), 4), round(float(r["lon"]), 4))] = r
            results_list = list(results)
            wgs = arcpy.SpatialReference(4326)
            y0, y1, temporal = admin_meta["y0"], admin_meta["y1"], admin_meta["temporal"]
            interp, base_cell = admin_meta["interp"], admin_meta["base_cell"]
            wind_cell = admin_meta["wind_cell"]
            admin_names = [a[0] for a in ADMIN_FIELDS]

            oid_name = arcpy.Describe(fc).OIDFieldName
            with arcpy.da.UpdateCursor(fc, [oid_name, "SHAPE@"] + admin_names + wanted) as ucur:
                row_idx = 0
                for row in ucur:
                    r = None
                    try:
                        pt_geom = row[1]
                        if pt_geom:
                            pt_wgs = pt_geom.projectAs(wgs)
                            ckey = (round(pt_wgs.centroid.Y, 4), round(pt_wgs.centroid.X, 4))
                            r = by_coord.get(ckey)
                    except Exception:
                        r = None
                    if r is None:
                        r = by_oid.get(row[0])
                    if r is None and row_idx < len(results_list):
                        r = results_list[row_idx]
                    row_idx += 1

                    if r is None:
                        r = {"oid": row[0], "lat": None, "lon": None,
                             "status": "FAILED", "error": "No result",
                             "fields": {}}
                    vals = r.get("fields", {})
                    ds_val = str(admin_meta.get("data_start", str(y0)))
                    de_val = str(admin_meta.get("data_end", str(y1)))
                    admin = [r.get("oid", row[0]), r.get("lat"), r.get("lon"), ds_val, de_val, temporal,
                             interp, base_cell, wind_cell, r.get("status", "FAILED"),
                             (r.get("error", "") or "")[:255]]
                    for i in range(len(admin)):
                        row[2 + i] = admin[i]
                    for i, f in enumerate(wanted):
                        row[2 + len(admin) + i] = vals.get(f)
                    ucur.updateRow(row)
            n = int(arcpy.GetCount_management(fc)[0])
            msg("Element layer '%s': %s (%d rows)." % (m, fc, n))
            return fc
        except Exception as ex:
            warn("Element layer '%s' failed: %s" % (m, ex))
            return None

    def _build_element_layers(self, in_points, gdb_path, out_sr, results, modules,
                              admin_meta, msg, warn, wanted_fields_by_module=None):
        """One point Feature Class per climate element, named after the element.

        Projects the input once, then per element copies it and stores admin
        fields plus that element's computed climate fields (from results).
        Returns {module: fc_path}."""
        out = {}
        # NOTE: ArcMap 10.8 cannot Project into in_memory -> use a real temp FC.
        tmp = safe_project_fc(in_points, out_sr, gdb_path, "elemproj", warn)
        tmp_is_temp = (tmp != in_points)
        try:
            for m in modules:
                wf = wanted_fields_by_module.get(m, []) if wanted_fields_by_module else None
                fc = self._build_single_element_layer(tmp, gdb_path, results, m,
                                                      admin_meta, msg, warn, wanted_fields=wf)
                if fc:
                    out[m] = fc
        finally:
            if tmp_is_temp:
                try:
                    arcpy.management.Delete(tmp)
                except Exception:
                    pass
        return out

    def _interpolate_all(self, master_fc, modules, paths, cell, method, mask, msg, warn,
                         iopts=None, kopts=None, is_geo=False,
                         purge=True, scratch=None, focal=None, source_by_module=None,
                         wanted_fields_by_module=None):
        from arcpy.sa import ExtractByMask
        out_ws = os.path.dirname(paths["vec"])
        if scratch is None:
            scratch = os.path.join(out_ws, "_scratch")
        makedirs_ok(scratch)
        try:
            arcpy.env.scratchWorkspace = scratch
        except Exception:
            pass
        focal = focal or {"apply": False, "stat": "MEAN", "size": 3}
        msg("Raw float rasters | LZW: enforced | purge temps: %s | focal: %s" % (
            purge, ("OFF" if not focal["apply"] else "%s %dx%d" % (
                focal["stat"], focal["size"], focal["size"]))))
        registry = []
        todo = []
        for m in modules:
            if wanted_fields_by_module is not None:
                flist = wanted_fields_by_module.get(m, [])
            else:
                flist = MODULE_FIELDS.get(m, [])
            for f in flist:
                todo.append((m, f))
        # IDW max distance is entered in metres: convert for geographic output
        if iopts and iopts.get("maxdist") and is_geo and float(iopts["maxdist"]) > 1.0:
            iopts = dict(iopts, maxdist=float(iopts["maxdist"]) / 111320.0)
            warn("IDW Maximum Distance converted to degrees: %.5f." % iopts["maxdist"])
        arcpy.SetProgressor("step", "Interpolating rasters ...", 0, len(todo), 1)
        # --- valid-value counts: one scan per source point layer ---
        msg("Counting valid values ...")
        counts = {}
        _src_of = source_by_module or {}
        try:
            _by_src = {}
            for _m, _f in todo:
                _by_src.setdefault(_src_of.get(_m, master_fc), []).append(_f)
            for _s, _fs in _by_src.items():
                if _s is None or not arcpy.Exists(_s):
                    continue
                with arcpy.da.SearchCursor(_s, _fs) as _cur:
                    for _row in _cur:
                        for _f, _v in zip(_fs, _row):
                            if _v is not None:
                                counts[_f] = counts.get(_f, 0) + 1
        except Exception as ex:
            warn("Fast counting failed, falling back to per-field counts: %s" % ex)
            counts = {}
        i = 0
        for module, field in todo:
            i += 1
            arcpy.SetProgressorPosition(i)
            try:
                # NOTE: each element interpolates from its own point layer
                src_fc = (source_by_module or {}).get(module, master_fc)
                if src_fc is None or not arcpy.Exists(src_fc):
                    warn("Skipping raster %s: no source point layer." % field)
                    continue
                available_fields = [f.name for f in arcpy.ListFields(src_fc)]
                actual_field = field
                if actual_field not in available_fields:
                    shp_alias = SHP_FIELD_MAP.get(field)
                    if shp_alias and shp_alias in available_fields:
                        actual_field = shp_alias
                    else:
                        warn("Skipping raster %s: field not found in point layer." % field)
                        continue
                if actual_field in counts:
                    n_valid = counts[actual_field]
                elif field in counts:
                    n_valid = counts[field]
                else:
                    n_valid = 0
                    with arcpy.da.SearchCursor(src_fc, [actual_field]) as cur:
                        for row in cur:
                            if row[0] is not None:
                                n_valid += 1
                if n_valid < 3:
                    warn("Skipping raster %s: only %d valid points." % (field, n_valid))
                    continue
                lyr = "pwr_atlas_interp"
                try:
                    arcpy.management.Delete(lyr)
                except Exception:
                    pass
                arcpy.management.MakeFeatureLayer(
                    src_fc, lyr, "%s IS NOT NULL" % arcpy.AddFieldDelimiters(src_fc, actual_field))
                try:
                    arcpy.ClearEnvironment("mask")
                    if mask:
                        try:
                            m_ext = arcpy.Describe(mask).extent
                            p_ext = arcpy.Describe(src_fc).extent
                            u_ext = arcpy.Extent(
                                min(m_ext.XMin, p_ext.XMin),
                                min(m_ext.YMin, p_ext.YMin),
                                max(m_ext.XMax, p_ext.XMax),
                                max(m_ext.YMax, p_ext.YMax)
                            )
                            arcpy.env.extent = u_ext
                        except Exception:
                            arcpy.ClearEnvironment("extent")
                    else:
                        arcpy.ClearEnvironment("extent")
                except Exception:
                    pass
                surf = self._interp_surface(lyr, actual_field, cell, method, iopts, kopts)
                rp, lp = self._raster_paths(out_ws, module, field)
                # --- staged save: unclipped surface -> scratch temp first ---
                tmpu = os.path.join(scratch, "u_" + field + ".tif")
                try:
                    if arcpy.Exists(tmpu):
                        arcpy.management.Delete(tmpu)
                except Exception:
                    pass
                try:
                    surf.save(tmpu)
                except Exception:
                    tmpu = "in_memory/u_raw"
                    try:
                        arcpy.management.Delete(tmpu)
                    except Exception:
                        pass
                    surf.save(tmpu)
                # --- clip to final extent (spec: delete unclipped right after) ---
                if mask:
                    tmpc = os.path.join(scratch, "c_" + field + ".tif") \
                        if not tmpu.startswith("in_memory") else "in_memory/u_clip"
                    try:
                        if arcpy.Exists(tmpc):
                            arcpy.management.Delete(tmpc)
                    except Exception:
                        pass
                    try:
                        ExtractByMask(tmpu, mask).save(tmpc)
                        src_path = tmpc
                    except Exception as ex:
                        warn("ExtractByMask failed for %s, keeping unclipped: %s" % (field, ex))
                        src_path = tmpu
                        tmpc = None
                else:
                    src_path = tmpu
                    tmpc = None
                # --- focal smoothing replaces the output (same element name) ---
                if focal["apply"]:
                    from arcpy.sa import FocalStatistics, NbrRectangle
                    tmpf = os.path.join(scratch, "f_" + field + ".tif") \
                        if not src_path.startswith("in_memory") else "in_memory/u_focal"
                    try:
                        if arcpy.Exists(tmpf):
                            arcpy.management.Delete(tmpf)
                    except Exception:
                        pass
                    FocalStatistics(arcpy.Raster(src_path),
                                    NbrRectangle(focal["size"], focal["size"], "CELL"),
                                    focal["stat"]).save(tmpf)
                    if purge:
                        for _t in (tmpu, tmpc):
                            try:
                                if _t and _t != tmpf and arcpy.Exists(_t):
                                    arcpy.management.Delete(_t)
                            except Exception:
                                pass
                    src_path = tmpf
                # --- raw float save (Raster.save honors env LZW compression) ---
                try:
                    arcpy.Raster(src_path).save(rp)
                except Exception:
                    surf.save(rp)
                try:
                    del surf
                except Exception:
                    pass
                if (i + 1) % 10 == 0:
                    try:
                        gc.collect()
                    except Exception:
                        pass
                if purge:
                    for _t in (tmpu, tmpc):
                        try:
                            if _t and arcpy.Exists(_t):
                                arcpy.management.Delete(_t)
                        except Exception:
                            pass
                    try:
                        if focal["apply"] and src_path != rp and arcpy.Exists(src_path):
                            arcpy.management.Delete(src_path)
                    except Exception:
                        pass
                try:
                    arcpy.management.Delete(lyr)
                except Exception:
                    pass
                try:
                    arcpy.management.CalculateStatistics(rp)
                    _rmin = float(arcpy.GetRasterProperties_management(rp, "MINIMUM")[0])
                    _rmax = float(arcpy.GetRasterProperties_management(rp, "MAXIMUM")[0])
                except Exception:
                    _rmin, _rmax = None, None
                colors = self._colors_for(module, field)
                nclass = 5 if module == "UV Index" else 7
                breaks = equal_interval_breaks(_rmin, _rmax, nclass) \
                    if _rmin is not None else None
                # --- classified display raster so the .lyr opens WITH colors ---
                cls_rp, clr_path = self._build_display(rp, field, module, colors,
                                                       nclass, msg, warn)
                if cls_rp:
                    self._make_lyr(cls_rp, lp, field, module, colors, nclass, method,
                                   msg, warn, breaks, rp)
                else:
                    self._make_lyr(rp, lp, field, module, colors, nclass, method,
                                   msg, warn, breaks, rp)
                registry.append((field, rp, lp, module, colors, nclass))
                msg("Raster: %s [raw float, LZW]" % rp)
            except Exception as ex:
                warn("Raster %s failed: %s" % (field, ex))
        arcpy.ResetProgressor()
        return registry

    def _make_lyr(self, raster_path, lyr_path, field, module, colors, nclass, method, msg, warn,
                  breaks=None, src_continuous=None):
        """Create ArcMap .lyr pointing at the CLASSIFIED display raster, so colors
        show immediately on open (colormap renderer embedded via AddColormap).

        raster_path: the classified display raster (<field>_cls.tif).
        breaks: true-value class edges computed from the continuous raster (if
        None, derived from the display raster itself). src_continuous: the raw
        float GeoTIFF kept alongside for analysis.
        """
        info = FIELD_BY_NAME.get(field, (field, field, "", "", module, "", "", "", "", "", ""))
        try:
            if arcpy.Exists(lyr_path):
                arcpy.management.Delete(lyr_path)
        except Exception:
            pass
        lyr_name = field  # layer name = raster/field name in the TOC
        try:
            arcpy.management.Delete(lyr_name)
        except Exception:
            pass
        try:
            arcpy.management.MakeRasterLayer(raster_path, lyr_name)
        except Exception as ex:
            warn("MakeRasterLayer failed for %s: %s" % (field, ex))
            return
        if not breaks:
            try:
                _mn = float(arcpy.GetRasterProperties_management(raster_path, "MINIMUM")[0])
                _mx = float(arcpy.GetRasterProperties_management(raster_path, "MAXIMUM")[0])
            except Exception:
                _mn, _mx = 0.0, 1.0
            breaks = equal_interval_breaks(_mn, _mx, nclass) or [_mn, _mx]
        disp_note = ("Display: classified %d-class raster (descending, zone 1 = highest) "
                      "with embedded colormap (raw float: %s). "
                      % (nclass, os.path.basename(src_continuous or raster_path)))
        # descending labels: Class 1 = highest interval, colors matched
        class_lines = []
        for k in range(1, nclass + 1):
            _lo, _hi = breaks[nclass - k], breaks[nclass - k + 1]
            _ci = nclass - k if (nclass - k) < len(colors) else len(colors) - 1
            class_lines.append("Class %d: %.4g - %.4g  color %s" % (k, _lo, _hi, colors[_ci]))
        try:
            arcpy.management.SaveToLayerFile(lyr_name, lyr_path)
            try:
                lyr = arcpy.mapping.Layer(lyr_path)
                lyr.description = ("%s | %s | Unit: %s | Period: %s | Statistic: %s | "
                                   "Method: %s (equal interval, %d classes) | Source: NASA POWER. %s"
                                   % (info[1], info[2], info[7], info[5], info[6],
                                      method, nclass, disp_note))
                lyr.credits = ("NASA POWER (power.larc.nasa.gov), %s. Gridded/modelled estimates, "
                               "not station measurements. Created %s. Classification: %s"
                               % (TOOL_VERSION, now_str(), " ; ".join(class_lines)))
                lyr.save()
            except Exception as ex:
                warn("Layer metadata for %s not fully embedded: %s" % (field, ex))
            try:
                # Force the .lyr to reference the real display raster on disk.
                # (In-session SA state can otherwise leave a Temp *.afr reference.)
                _lyr2 = arcpy.mapping.Layer(lyr_path)
                _lyr2.replaceDataSource(
                    os.path.dirname(raster_path), "RASTER_WORKSPACE",
                    os.path.basename(raster_path))
                _lyr2.save()
            except Exception as ex:
                warn("Layer datasource relink for %s skipped: %s" % (field, ex))
            try:
                # NOTE: plain UTF-8 WITHOUT BOM, human-readable Arabic.
                # (py2.7 json.dump with ensure_ascii=False cannot write to a
                # text-mode file object, so serialize then write bytes.)
                meta = {
                    "variable_EN": info[1], "variable_AR": info[2], "unit": info[7],
                    "period": info[5], "statistic": info[6], "method": method,
                    "classification": "EqualInterval", "classes": nclass,
                    "breaks": breaks, "colors": colors,
                    "class_labels": class_lines,
                    "display_raster": os.path.basename(raster_path),
                    "source_raster": os.path.basename(
                        src_continuous or raster_path),
                    "data_min": breaks[0], "data_max": breaks[-1],
                    "source": "NASA POWER", "created": now_str(),
                    "raster": os.path.basename(raster_path),
                    "arcmap_note": "Opens with embedded colormap colors. Raw float values "
                                   "stay in the source_raster GeoTIFF.",
                }
                _s = json.dumps(meta, ensure_ascii=False, indent=2)
                if not isinstance(_s, bytes):
                    _s = _s.encode("utf-8")
                with open(lyr_path + ".json", "wb") as fh:
                    fh.write(_s)
            except Exception as ex:
                warn("Sidecar json for %s failed: %s" % (field, ex))
            msg("Layer: %s" % lyr_path)
        except Exception as ex:
            warn("Layer file for %s failed: %s" % (field, ex))
        finally:
            try:
                arcpy.management.Delete(lyr_name)
            except Exception:
                pass

    def _build_wind_vectors(self, gdb_path, paths, registry, extent_fc, mask, out_sr,
                            wind_cell, msg, warn):
        """Thinned fishnet points sampling speed+direction rasters -> 5 vector FCs."""
        spd = {}
        drc = {}
        for item in registry:
            f, rp = item[0], item[1]
            if f.startswith("W_Spd"):
                spd[f] = rp
            elif f.startswith("W_Dir"):
                drc[f] = rp
        if not spd or not drc:
            warn("Wind vectors skipped: speed/direction rasters missing.")
            return []
        if mask:
            ext = arcpy.Describe(mask).extent
        elif extent_fc is not None and arcpy.Exists(extent_fc):
            ext = arcpy.Describe(extent_fc).extent
        else:
            warn("Wind vectors skipped: no mask and no Wind point layer for extent.")
            return []
        out_ws = os.path.dirname(paths["vec"])
        fish = "in_memory/wind_fishnet"
        for o in (fish, fish + "_label", "in_memory/wind_clip", "in_memory/wind_proj"):
            try:
                arcpy.management.Delete(o)
            except Exception:
                pass
        origin = "%s %s" % (ext.XMin, ext.YMin)
        yaxis = "%s %s" % (ext.XMin, ext.YMin + 10)
        corner = "%s %s" % (ext.XMax, ext.YMax)
        arcpy.management.CreateFishnet(fish, origin, yaxis, float(wind_cell), float(wind_cell),
                                       "", "", corner, "LABELS", None, "POLYGON")
        fish_pts = fish + "_label"
        if mask:
            try:
                arcpy.analysis.Clip(fish_pts, mask, "in_memory/wind_clip")
                fish_pts = "in_memory/wind_clip"
            except Exception as ex:
                warn("Wind fishnet clip failed: %s" % ex)
        try:
            proj = safe_project_fc(fish_pts, out_sr, gdb_path, "windproj", warn)
            if proj != fish_pts:
                fish_pts = proj
        except Exception:
            pass
        periods = [("Annual", "W_Spd_Annual_Mean", "W_Dir_Annual_Mean"),
                   ("Winter", "W_Spd_Winter_Mean", "W_Dir_Winter_Mean"),
                   ("Spring", "W_Spd_Spring_Mean", "W_Dir_Spring_Mean"),
                   ("Summer", "W_Spd_Summer_Mean", "W_Dir_Summer_Mean"),
                   ("Autumn", "W_Spd_Autumn_Mean", "W_Dir_Autumn_Mean")]
        created = []
        vdir = os.path.join(out_ws, "05_Wind", "Direction", "Vector_Points")
        for suffix, fs, fd in periods:
            if fs not in spd or fd not in drc:
                continue
            fc = os.path.join(gdb_path, "Wind_Vectors_%s" % suffix)
            try:
                if arcpy.Exists(fc):
                    arcpy.management.Delete(fc)
                arcpy.management.CopyFeatures(fish_pts, fc)
                arcpy.sa.ExtractMultiValuesToPoints(fc, [[spd[fs], "Wind_Speed"], [drc[fd], "Wind_Dir"]])
                for fn, typ in [("Arrow_Angle", "DOUBLE"), ("Arrow_Size", "DOUBLE"), ("Period", "TEXT")]:
                    try:
                        if typ == "TEXT":
                            arcpy.management.AddField(fc, fn, typ, field_length=20)
                        else:
                            arcpy.management.AddField(fc, fn, typ)
                    except Exception:
                        pass
                with arcpy.da.UpdateCursor(fc, ["Wind_Dir", "Wind_Speed", "Arrow_Angle", "Arrow_Size", "Period"]) as cur:
                    for row in cur:
                        wd, ws = row[0], row[1]
                        try:
                            row[2] = (float(wd) + 180.0) % 360.0 if wd is not None else None
                        except Exception:
                            row[2] = None
                        try:
                            row[3] = float(ws) if ws is not None else None
                        except Exception:
                            row[3] = None
                        row[4] = suffix
                        cur.updateRow(row)
                try:
                    shp = os.path.join(vdir, "Wind_Vectors_%s.shp" % suffix)
                    if arcpy.Exists(shp):
                        arcpy.management.Delete(shp)
                    arcpy.conversion.FeatureClassToShapefile([fc], vdir)
                except Exception as ex:
                    warn("Wind shapefile %s failed: %s" % (suffix, ex))
                created.append(fc)
                msg("Wind vectors: %s" % fc)
            except Exception as ex:
                warn("Wind vectors %s failed: %s" % (suffix, ex))
        for o in (fish, fish + "_label", "in_memory/wind_clip",
                  os.path.join(gdb_path, "tmp_windproj")):
            try:
                arcpy.management.Delete(o)
            except Exception:
                pass
        return created

    def _build_isobars(self, gdb_path, registry, msg, warn, step=None):
        from arcpy.sa import Contour
        mapping = {"PSL_Winter_Mean": "Isobars_PSL_Winter_Mean",
                   "PSL_Spring_Mean": "Isobars_PSL_Spring_Mean",
                   "PSL_Summer_Mean": "Isobars_PSL_Summer_Mean",
                   "PSL_Autumn_Mean": "Isobars_PSL_Autumn_Mean",
                   "PS_Winter_Mean": "Isobars_PS_Winter_Mean",
                   "PS_Spring_Mean": "Isobars_PS_Spring_Mean",
                   "PS_Summer_Mean": "Isobars_PS_Summer_Mean",
                   "PS_Autumn_Mean": "Isobars_PS_Autumn_Mean"}
        lut = dict((item[0], item[1]) for item in registry)
        for field, fcname in mapping.items():
            if field not in lut:
                continue
            try:
                if step:
                    interval = float(step)
                else:
                    rmin = float(arcpy.GetRasterProperties_management(lut[field], "MINIMUM")[0])
                    rmax = float(arcpy.GetRasterProperties_management(lut[field], "MAXIMUM")[0])
                    interval = max((rmax - rmin) / 10.0, 0.5)
                out = os.path.join(gdb_path, fcname)
                if arcpy.Exists(out):
                    arcpy.management.Delete(out)
                Contour(lut[field], out, interval)
                msg("Isobars: %s (interval %.2f hPa)" % (out, interval))
            except Exception as ex:
                warn("Isobar %s failed: %s" % (field, ex))

    def _write_dictionaries(self, vec_dir, modules, msg, provider="NASA POWER API", wanted_fields_by_module=None):
        rows = metadata_rows_for_modules(modules, wanted_fields_by_module=wanted_fields_by_module)
        for r in rows:
            if r["Field_Name"] == "R_Annual_Total":
                r["Notes"] = "Climatological annual total (mean of per-year sums)"
            if r["Field_Name"] == "R_Annual_Mean":
                r["Notes"] = "Mean of climatological monthly totals (= Total/12)"
            if r["Field_Name"] in ("HI_Annual_Mean", "HI_Summer_Mean"):
                r["Notes"] = ((r["Notes"] + "; ") if r["Notes"] else "") + \
                    "Needs humidity (RH2M); NoData when unavailable"
            if r["Field_Name"].startswith("W_Dir"):
                r["Notes"] = "Circular (vector) mean, not arithmetic mean of angles"
            if r["Field_Name"] == "Sol_Annual_Total":
                r["Notes"] = "Mean annual accumulated energy (kWh/m2/year)"
            r["Source"] = ("Open-Meteo ERA5" if provider.startswith("Open-Meteo")
                           else "NASA POWER")
        if provider.startswith("Open-Meteo"):
            # provider-specific statistic documentation (same table, adapted notes)
            for r in rows:
                if r["Field_Name"].startswith("UV_"):
                    r["Notes"] = ((r["Notes"] + "; ") if r["Notes"] else "") + \
                        "Open-Meteo: mean of daily maximum (uv_index_max, ERA5)"
                if r["Field_Name"].startswith("W_Spd"):
                    r["Notes"] = ((r["Notes"] + "; ") if r["Notes"] else "") + \
                        "Open-Meteo: mean of hourly wind_speed_10m (ERA5)"
                if r["Field_Name"].startswith(("PSL_", "PS_", "RH_", "Cld_")):
                    r["Notes"] = ((r["Notes"] + "; ") if r["Notes"] else "") + \
                        "Open-Meteo: mean of hourly aggregates (ERA5)"
                if r["Field_Name"].startswith("R_") and r["Field_Name"] not in (
                        "R_Max_Daily_Month", "R_Annual_Rain_Days_Total"):
                    r["Notes"] = ((r["Notes"] + "; ") if r["Notes"] else "") + \
                        "Open-Meteo: precipitation_sum daily totals (mm, ERA5)"
        cols = ["Field_Name", "Full_Name_EN", "Name_AR", "NASA_Code", "Module", "Period",
                "Statistic", "Unit", "Description_AR", "Description_EN", "Calculation",
                "Source", "Notes"]
        p1 = os.path.join(vec_dir, "Metadata_Dictionary.csv")
        write_csv(p1, cols, [[r[c] for c in cols] for r in rows])
        msg("Dictionary: %s (%d fields)" % (p1, len(rows)))
        p1_xls = os.path.join(vec_dir, "Metadata_Dictionary.xls")
        write_excel_file(p1_xls, cols, [[r[c] for c in cols] for r in rows], sheet_name="Metadata", rtl=False)
        msg("Dictionary Excel: %s" % p1_xls)

        p2 = os.path.join(vec_dir, "Field_Dictionary_Arabic.csv")
        ar_cols = ["Field_Name", "Name_AR", "Unit", "Description_AR", "Module", "Period"]
        write_csv(p2, ar_cols,
                  [[r["Field_Name"], r["Name_AR"], r["Unit"],
                    r["Description_AR"], r["Module"], r["Period"]] for r in rows])
        msg("Dictionary: %s" % p2)
        p2_xls = os.path.join(vec_dir, "Field_Dictionary_Arabic.xls")
        write_excel_file(p2_xls, ar_cols,
                         [[r["Field_Name"], r["Name_AR"], r["Unit"],
                           r["Description_AR"], r["Module"], r["Period"]] for r in rows], sheet_name="Arabic_Dictionary", rtl=True)
        msg("Dictionary Excel (RTL): %s" % p2_xls)

    def _run_qa(self, element_fcs, paths, modules, registry, results, msg, warn, wanted_fields_by_module=None):
        checks = []

        def _add(name, ok, detail=""):
            checks.append((name, bool(ok), detail))
            if ok:
                msg("QA PASS: %s %s" % (name, detail))
            else:
                warn("QA FAIL: %s %s" % (name, detail))

        def _elfc(m):
            fc = (element_fcs or {}).get(m)
            if fc and arcpy.Exists(fc):
                return fc
            return None

        try:
            _counts = {}
            for m in modules:
                _fc = _elfc(m)
                _counts[m] = int(arcpy.GetCount_management(_fc)[0]) if _fc else -1
            _ok = all(v >= 0 for v in _counts.values()) and len(set(_counts.values())) == 1
            _add("element layers", _ok, "counts=%s" % _counts)
        except Exception as ex:
            _add("element layers", False, str(ex))
        try:
            _admin = [a[0] for a in ADMIN_FIELDS]
            _miss, _total = [], 0
            for m in modules:
                _fc = _elfc(m)
                if _fc is None:
                    _miss.append(m + ":layer")
                    continue
                _names = set(f.name for f in arcpy.ListFields(_fc))
                m_wanted = (wanted_fields_by_module or {}).get(m, MODULE_FIELDS.get(m, []))
                for n in _admin + m_wanted:
                    _total += 1
                    if n not in _names:
                        _miss.append(n)
            _add("field names present", not _miss, "(%d/%d, missing=%s)"
                 % (_total - len(_miss), _total, _miss[:8]))
            _allw = [f for m in modules for f in (wanted_fields_by_module or {}).get(m, MODULE_FIELDS.get(m, []))]
            _add("shapefile name length<=10 (or mapped)",
                 all(len(n) <= 10 or n in SHP_FIELD_MAP for n in _allw),
                 "mapped=%d fields" % len(SHP_FIELD_MAP))
        except Exception as ex:
            _add("field names present", False, str(ex))
        try:
            _req = [c for c in REQUIRED_COLUMNS if c != "OBJECTID"]
            _miss = []
            for m in modules:
                _fc = _elfc(m)
                if _fc is None:
                    _miss.append(m + ":layer")
                    continue
                _have = set(f.name for f in arcpy.ListFields(_fc))
                m_wanted = (wanted_fields_by_module or {}).get(m, MODULE_FIELDS.get(m, []))
                for c in _req:
                    if c in [a[0] for a in ADMIN_FIELDS] or c in m_wanted:
                        if c not in _have:
                            _miss.append(c)
            _add("required columns present", not _miss, "missing=%s" % _miss[:8])
        except Exception as ex:
            _add("required columns present", False, str(ex))
        try:
            bad = 0
            for m in modules:
                _fc = _elfc(m)
                if _fc is None:
                    continue
                m_wanted = (wanted_fields_by_module or {}).get(m, MODULE_FIELDS.get(m, []))
                if not m_wanted:
                    continue
                with arcpy.da.SearchCursor(_fc, m_wanted) as cur:
                    for row in cur:
                        for v in row:
                            if v is not None and abs(float(v) + 999.0) < 1e-9:
                                bad += 1
            _add("no -999 sentinel values", bad == 0, "(bad=%d)" % bad)
        except Exception as ex:
            _add("no -999 sentinel values", False, str(ex))
        _add("Metadata_Dictionary.csv",
             os.path.isfile(os.path.join(paths["vec"], "Metadata_Dictionary.csv")))
        _add("Field_Dictionary_Arabic.csv",
             os.path.isfile(os.path.join(paths["vec"], "Field_Dictionary_Arabic.csv")))
        missing = [item[0] for item in registry if not os.path.isfile(item[2])]
        _add("lyr per raster", len(missing) == 0,
             "(%d/%d, missing=%s)" % (len(registry) - len(missing), len(registry), missing[:5]))
        mods_with_r = set(item[3] for item in registry)
        _add("outputs match selected modules", not (mods_with_r - set(modules)),
             "raster modules=%s" % sorted(mods_with_r))
        try:
            ranges = [("Temperature", "T_Annual_Mean", (-30, 45)),
                      ("Temperature", "HI_Annual_Mean", (-30, 60)),
                      ("Relative Humidity", "RH_Annual_Mean", (0, 100)),
                      ("Cloud Cover", "Cld_Annual_Mean", (0, 100)),
                      ("Sea Level Pressure", "PSL_Annual_Mean", (870, 1050)),
                      ("Surface Pressure", "PS_Annual_Mean", (870, 1050))]
            notes = []
            ok_all = True
            for _m, fld, lim in ranges:
                if _m not in modules:
                    continue
                _fc = _elfc(_m)
                if _fc is None:
                    continue
                if fld not in set(f.name for f in arcpy.ListFields(_fc)):
                    continue
                with arcpy.da.SearchCursor(_fc, [fld]) as cur:
                    vals = [r[0] for r in cur if r[0] is not None]
                if vals:
                    badv = [v for v in vals if not (lim[0] <= v <= lim[1])]
                    if badv:
                        ok_all = False
                        notes.append("%s %d out of range" % (fld, len(badv)))
            _add("value ranges sane", ok_all, "; ".join(notes))
        except Exception as ex:
            _add("value ranges sane", False, str(ex))
        return checks

    def _write_log(self, vec_dir, info):
        p = os.path.join(vec_dir, "Processing_Log.txt")
        with open_utf8(p, "w") as fh:
            fh.write(u"POWER Climate Atlas Generator v%s — Processing Log (ArcMap 10.x)\n" % info["tool_version"])
            fh.write(u"Created: %s\n\n" % now_str())
            fh.write(u"Modules: %s\n" % ", ".join(info["modules"]))
            fh.write(u"Period: %d-%d (%d years)\n" % info["years"])
            fh.write(u"Data source: %s\n" % info.get("provider", "NASA POWER API"))
            if info.get("dl_only"):
                fh.write(u"Mode: DOWNLOAD ONLY (points + tables, no rasters).\n")
            fh.write(u"Temporal: %s | Interp: %s | Base cell: %s | Wind cell: %s\n"
                     % (info["temporal"], info["interp"], info["base_cell"], info["wind_cell"]))
            fh.write(u"Raw float rasters (32-bit, true values) | LZW: enforced | purge cache: %s\n"
                     % (info.get("purge", "?")))
            fh.write(u"Tolerance: %.0f m | Focal: %s\n" % (
                info.get("tol_m", 0),
                ("OFF" if not (info.get("focal") or {}).get("apply") else "%s %dx%d" % (
                    info["focal"]["stat"], info["focal"]["size"], info["focal"]["size"]))))
            if info.get("interp_detail"):
                fh.write(u"Interp detail: %s\n" % info["interp_detail"])
            if info.get("iso", ("", None))[0]:
                fh.write(u"Isobars: %s, step %.2f mbar.\n" % info["iso"])
            fh.write(u"Points: %d | Queries OK: %d | Queries failed: %d\n"
                     % (info["n_points"], info["n_ok"], info["n_fail"]))
            if info["failed"]:
                fh.write(u"Failed points (oid, err):\n")
                for oid, err in info["failed"]:
                    fh.write(u"  %s: %s\n" % (oid, err))
            fh.write(u"\nRasters:\n")
            for item in info["rasters"]:
                fh.write(u"  [%s] %s -> %s\n" % (item[3], item[1], item[2]))
            if info.get("element_layers"):
                fh.write(u"\nElement point layers:\n")
                for _m in sorted(info["element_layers"]):
                    fh.write(u"  [%s] %s\n" % (_m, info["element_layers"][_m]))
            if info["wind"]:
                fh.write(u"\nWind vectors:\n")
                for w in info["wind"]:
                    fh.write(u"  %s\n" % w)
            fh.write(u"\nScientific notes:\n")
            _is_om = str(info.get("provider", "")).startswith("Open-Meteo")
            _src = (u"Open-Meteo ERA5 reanalysis (~0.25 deg native)" if _is_om
                    else u"NASA POWER (~0.5 deg native)")
            for n in [
                (_is_om and u"Open-Meteo ERA5 are gridded/modelled estimates, not in-situ measurements."
                 or u"NASA POWER are gridded/modelled estimates, not in-situ measurements."),
                u"Interpolated cell size is cartographic; native resolution is coarse (%s)." % _src,
                u"Wind direction uses circular (vector) mean.",
                u"Precipitation is accumulated (sum), not averaged like temperature.",
                u"PSL (sea-level) and PS (surface) are different products.",
                u"Sol_Annual_Mean (kWh/m2/day) differs from Sol_Annual_Total (kWh/m2/year).",
                u"Winter = months 12,1,2 of the same year(s); -999 excluded; NoData where insufficient valid values.",
                u".lyr files open with embedded colormap colors from classified display "
                u"rasters (<field>_cls.tif); raw float GeoTIFFs stay alongside for analysis.",
            ]:
                fh.write(u"  - %s\n" % n)
            if info["warnings"]:
                fh.write(u"\nWarnings (%d):\n" % len(info["warnings"]))
                for w in info["warnings"]:
                    fh.write(u"  ! %s\n" % w)
            fh.write(u"\nQA:\n")
            for name, ok, detail in info["qa"]:
                fh.write(u"  [%s] %s %s\n" % ("PASS" if ok else "FAIL", name, detail))
            fh.write(u"\nElapsed: %.1fs\n" % info["elapsed"])

    def _cleanup(self, msg, scratch=None, purge=True):
        for o in ["in_memory/input_proj", "in_memory/raw_ras",
                  "in_memory/u_raw", "in_memory/u_clip",
                  "in_memory/wind_fishnet", "in_memory/wind_fishnet_label",
                  "in_memory/wind_clip", "in_memory/shp_tmp",
                  "pwr_atlas_interp"]:
            try:
                if arcpy.Exists(o):
                    arcpy.management.Delete(o)
            except Exception:
                pass
        try:
            arcpy.ClearEnvironment("mask")
            arcpy.ClearEnvironment("extent")
        except Exception:
            pass
        if scratch and purge:
            try:
                import shutil
                if os.path.isdir(scratch):
                    shutil.rmtree(scratch, ignore_errors=True)
                msg("Scratch cache purged: %s" % scratch)
            except Exception as ex:
                msg("Scratch purge skipped: %s" % ex)
        elif scratch:
            msg("Scratch kept for inspection (purge OFF): %s" % scratch)
        msg("Intermediate data cleaned (in_memory, masks reset). Inputs and final outputs untouched.")

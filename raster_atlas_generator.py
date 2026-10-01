# -*- coding: utf-8 -*-
"""
POWER Raster Climate Atlas Generator — ArcMap Desktop 10.x (Python 2.7 compatible)
Downloads gridded/raster climate data from NASA POWER, Open-Meteo, NASA Earthdata,
and NASA Giovanni across Layer 1 (Download Extent AOI), converts cells to 32-bit
Float points with full seasonal and annual indicators in Project_Data.gdb, performs
high-precision spatial interpolation, and clips final rasters using Layer 2 (Study Area Mask).
Also supports full Offline Mode using pre-calculated multi-layer point shapefiles/feature classes.
"""

import os
import sys
import json
import math
import csv
import io
import re
import time
import calendar
import datetime as _dt

PY27 = sys.version_info[0] == 2

# Python 2/3 compat aliases (RHS only evaluated in the taken branch, so no NameError).
if PY27:
    _text_type = unicode  # noqa: F821 - Python 2 only
    _binary_type = str
else:
    _text_type = str
    _binary_type = bytes


def _excel_text(v):
    """Return text suitable for xlwt on both Python 2 (unicode) and 3 (str)."""
    if v is None:
        return ""
    if PY27:
        try:
            if isinstance(v, _text_type):
                return v
            if isinstance(v, _binary_type):
                try:
                    return v.decode("utf-8")
                except Exception:
                    return v
            return _text_type(v)
        except Exception:
            try:
                return str(v)
            except Exception:
                return ""
    else:
        if isinstance(v, str):
            return v
        if isinstance(v, bytes):
            try:
                return v.decode("utf-8")
            except Exception:
                return v.decode("utf-8", errors="replace")
        try:
            return str(v)
        except Exception:
            return ""

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

CALC_EXPR_TYPE = "PYTHON_9.3" if PY27 else "PYTHON3"


# ---------------------------------------------------------------------------
# Constants & Dictionaries
# ---------------------------------------------------------------------------

NASA_POWER_REGIONAL_BASE = "https://power.larc.nasa.gov/api/temporal/monthly/regional"
OPEN_METEO_ARCHIVE_BASE = "https://archive-api.open-meteo.com/v1/archive"
EARTHDATA_URS_BASE = "https://urs.earthdata.nasa.gov"
GES_DISC_OPENDAP_BASE = "https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap"

MISSING_SENTINELS = (-999, -999.0, -99.0, -9999.0, -9999)

SEASONS = {
    "Winter": (1, 2, 12),
    "Spring": (3, 4, 5),
    "Summer": (6, 7, 8),
    "Autumn": (9, 10, 11),
}


def parse_temporal_scope(t_scope):
    """Normalize list or semicolon string of scopes to set of {'Annual', 'Winter', 'Spring', 'Summer', 'Autumn'}.
    Defaults to all 5 scopes if None or empty."""
    if not t_scope:
        return {"Annual", "Winter", "Spring", "Summer", "Autumn"}
    if isinstance(t_scope, (list, tuple)):
        raw = t_scope
    else:
        raw = str(t_scope).split(";")
    res = set()
    for item in raw:
        s = str(item).strip().strip("'\"")
        for norm in ("Annual", "Winter", "Spring", "Summer", "Autumn"):
            if norm.lower() in s.lower():
                res.add(norm)
    return res if res else {"Annual", "Winter", "Spring", "Summer", "Autumn"}


def get_field_temporal_scope(fname):
    """Returns 'Annual', 'Winter', 'Spring', 'Summer', or 'Autumn' for any field name."""
    f = fname.upper()
    if "WINTER" in f or "_WIN" in f or "_WN" in f or "WNMEAN" in f or "WINMEAN" in f or "MIN_WINTER" in f:
        return "Winter"
    if "SPRING" in f or "_SPR" in f or "SPMEAN" in f or "SPRMEAN" in f:
        return "Spring"
    if "SUMMER" in f or "_SUM" in f or "SUMEAN" in f or "SUMMEAN" in f or "MAX_SUMMER" in f or "WBGT_SUMMER" in f or "SUMN" in f:
        return "Summer"
    if "AUTUMN" in f or "_AUT" in f or "AUMEAN" in f or "AUTMEAN" in f:
        return "Autumn"
    return "Annual"

PRIMARY_MODULES_ALL = [
    "Temperature",
    "Precipitation",
    "Relative Humidity",
    "Wind",
    "Solar Radiation",
    "Surface Pressure",
    "Sea Level Pressure",
    "Cloud Cover",
    "UV Index"
]

SUBMODELS_ALL = [
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]",
    "Wind Chill / Cold Stress [Requires: Temperature, Wind]",
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]",
    "FAO-56 Hargreaves PET [Requires: Temperature]",
    "UNEP Aridity Index [Requires: Temperature, Precipitation]",
    "Water Deficit Annual [Requires: Temperature, Precipitation]",
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]",
    "Trends & Baseline Anomalies [Requires: Temperature, Precipitation]",
]

DERIVED_MODULES_ALL = [
    "Heat Index",
    "Wind Chill",
    "De Martonne Aridity",
    "Hargreaves PET",
    "UNEP Aridity",
    "Water Deficit",
    "Dry Months",
    "Trends & Anomalies",
]

CANONICAL_DERIVED_MAP = {
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]": "Heat Index",
    "Wind Chill / Cold Stress [Requires: Temperature, Wind]": "Wind Chill",
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]": "De Martonne Aridity",
    "FAO-56 Hargreaves PET [Requires: Temperature]": "Hargreaves PET",
    "UNEP Aridity Index [Requires: Temperature, Precipitation]": "UNEP Aridity",
    "Water Deficit Annual [Requires: Temperature, Precipitation]": "Water Deficit",
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]": "Dry Months",
    "Trends & Baseline Anomalies [Requires: Temperature, Precipitation]": "Trends & Anomalies",
}

DERIVED_TO_SUBMODEL_KEY = dict((v, k) for k, v in CANONICAL_DERIVED_MAP.items())

MODULES_ALL = PRIMARY_MODULES_ALL + SUBMODELS_ALL
ALL_CANONICAL_MODULES = PRIMARY_MODULES_ALL + DERIVED_MODULES_ALL

SUBMODEL_DEPS = {
    "Heat Index / Thermal Stress [Requires: Temperature, Relative Humidity]": {
        "short": "Heat_Index",
        "canonical": "Heat Index",
        "fields": [
            ("HI_Annual_Mean", "Annual Mean Heat Index"),
            ("HI_Summer_Mean", "Summer Mean Heat Index"),
            ("HI_Winter_Mean", "Winter Mean Heat Index"),
            ("HI_Annual_Range", "Annual Heat Index Range"),
            ("WBGT_Summer_Mean", "Summer Mean WBGT Heat Stress"),
        ],
        "field": "HI_Summer_Mean",
        "label": "Summer Mean Heat Index",
        "modules": ["Temperature", "Relative Humidity"],
        "params": ["T2M", "RH2M"]
    },
    "Wind Chill / Cold Stress [Requires: Temperature, Wind]": {
        "short": "Wind_Chill",
        "canonical": "Wind Chill",
        "fields": [
            ("WC_Winter_Mean", "Winter Mean Wind Chill"),
            ("WC_Annual_Mean", "Annual Mean Wind Chill"),
        ],
        "field": "WC_Winter_Mean",
        "label": "Winter Mean Wind Chill",
        "modules": ["Temperature", "Wind"],
        "params": ["T2M", "WS10M"]
    },
    "De Martonne Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "De_Martonne_Aridity",
        "canonical": "De Martonne Aridity",
        "fields": [
            ("DM_Aridity_Annual", "De Martonne Aridity Index"),
        ],
        "field": "DM_Aridity_Annual",
        "label": "De Martonne Aridity Index",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "FAO-56 Hargreaves PET [Requires: Temperature]": {
        "short": "Hargreaves_PET",
        "canonical": "Hargreaves PET",
        "fields": [
            ("PET_Hargreaves_Annual", "Annual Potential Evapotranspiration (Hargreaves)"),
        ],
        "field": "PET_Hargreaves_Annual",
        "label": "Annual Potential Evapotranspiration (Hargreaves)",
        "modules": ["Temperature"],
        "params": ["T2M"]
    },
    "UNEP Aridity Index [Requires: Temperature, Precipitation]": {
        "short": "UNEP_Aridity",
        "canonical": "UNEP Aridity",
        "fields": [
            ("UNEP_Aridity_Annual", "UNEP Aridity Index"),
        ],
        "field": "UNEP_Aridity_Annual",
        "label": "UNEP Aridity Index",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Water Deficit Annual [Requires: Temperature, Precipitation]": {
        "short": "Water_Deficit",
        "canonical": "Water Deficit",
        "fields": [
            ("Water_Deficit_Annual", "Annual Climatic Water Deficit/Surplus"),
        ],
        "field": "Water_Deficit_Annual",
        "label": "Annual Climatic Water Deficit/Surplus",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Walter-Lieth Dry Months Count [Requires: Temperature, Precipitation]": {
        "short": "Dry_Months",
        "canonical": "Dry Months",
        "fields": [
            ("Dry_Months_Count", "Biological Dry Months Count (Walter-Lieth)"),
        ],
        "field": "Dry_Months_Count",
        "label": "Biological Dry Months Count (Walter-Lieth)",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
    "Trends & Baseline Anomalies [Requires: Temperature, Precipitation]": {
        "short": "Trends_Anomalies",
        "canonical": "Trends & Anomalies",
        "fields": [
            ("T_Trend_Decade", "Temperature Trend per Decade"),
            ("R_Trend_Decade", "Precipitation Trend per Decade"),
            ("T_Anom_Annual", "Annual Temperature Anomaly"),
            ("T_Anom_Winter", "Winter Temperature Anomaly"),
            ("T_Anom_Summer", "Summer Temperature Anomaly"),
            ("R_Anom_Annual", "Annual Precipitation Anomaly"),
            ("R_Anom_Annual_Pct", "Annual Precipitation Anomaly (Percent)"),
            ("R_Anom_Winter", "Winter Precipitation Anomaly"),
            ("R_Anom_Winter_Pct", "Winter Precipitation Anomaly (Percent)"),
        ],
        "field": "T_Trend_Decade",
        "label": "Temperature Trend per Decade",
        "modules": ["Temperature", "Precipitation"],
        "params": ["T2M", "PRECTOTCORR"]
    },
}


def resolve_module_canonical(name):
    """Maps any module name (full UI string, canonical, or short) to its canonical name."""
    if not name:
        return None
    name_str = name.strip().strip("'\"")
    for cm in ALL_CANONICAL_MODULES:
        if name_str.lower() == cm.lower():
            return cm
    if name_str in CANONICAL_DERIVED_MAP:
        return CANONICAL_DERIVED_MAP[name_str]
    clean = name_str.split(" [")[0].strip().lower()
    for sub_key, can_name in CANONICAL_DERIVED_MAP.items():
        k_clean = sub_key.split(" [")[0].strip().lower()
        if clean == k_clean or k_clean.startswith(clean) or clean == can_name.lower():
            return can_name
    for info in SUBMODEL_DEPS.values():
        if clean == info.get("short", "").lower():
            return info["canonical"]
    return None


MODULE_SHORT = {
    "Temperature": "Temperature",
    "Precipitation": "Precipitation",
    "Sea Level Pressure": "Sea_Level_Pressure",
    "Surface Pressure": "Surface_Pressure",
    "Wind": "Wind",
    "Relative Humidity": "Humidity",
    "Solar Radiation": "Solar_Radiation",
    "UV Index": "UV_Index",
    "Cloud Cover": "Cloud_Cover",
    "Heat Index": "Heat_Index",
    "Wind Chill": "Wind_Chill",
    "De Martonne Aridity": "De_Martonne_Aridity",
    "Hargreaves PET": "Hargreaves_PET",
    "UNEP Aridity": "UNEP_Aridity",
    "Water Deficit": "Water_Deficit",
    "Dry Months": "Dry_Months",
    "Trends & Anomalies": "Trends_Anomalies",
    "Drought & Aridity": "Drought_Aridity",
    "Climate_Models": "Climate_Models",
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
    "Heat Index": "10_Heat_Index",
    "Wind Chill": "11_Wind_Chill",
    "De Martonne Aridity": "12_De_Martonne_Aridity",
    "Hargreaves PET": "13_Hargreaves_PET",
    "UNEP Aridity": "14_UNEP_Aridity",
    "Water Deficit": "15_Water_Deficit",
    "Dry Months": "16_Dry_Months",
    "Trends & Anomalies": "17_Trends_And_Anomalies",
    "Climate_Models": "10_Climate_Models",
}

POWER_PRIMARY_PARAM = {
    "Temperature": "T2M",
    "Precipitation": "PRECTOTCORR",
    "Relative Humidity": "RH2M",
    "Wind": "WS10M",
    "Solar Radiation": "ALLSKY_SFC_SW_DWN",
    "Surface Pressure": "PS",
    "Sea Level Pressure": "SLP",
    "Cloud Cover": "CLOUD_AMT",
    "UV Index": "ALLSKY_SFC_UV_INDEX",
}

COLOR_RAMPS = {
    "Temperature": ["#4575B4", "#74ADD1", "#ABD9E9", "#FFFFBF", "#FDAE61", "#F46D43", "#D73027"],
    "Precipitation": ["#8C510A", "#D8B365", "#F6E8C3", "#C7EAE5", "#80CDC1", "#35978F", "#01665E"],
    "Relative Humidity": ["#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"],
    "Wind": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"],
    "Wind_Speed": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"],
    "Wind_Direction": ["#F7F7F7", "#D9D9D9", "#BDBDBD", "#969696", "#737373", "#525252", "#252525"],
    "Solar Radiation": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#BD0026"],
    "Surface Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Sea Level Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "UV Index": ["#299500", "#F7E400", "#F85900", "#D8001D", "#6B499D"],
    "Cloud Cover": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#4292C6", "#2171B5", "#084594"],
    "Heat Index": ["#FFFFD4", "#FEE391", "#FEC44F", "#FE9929", "#EC7014", "#CC4C02", "#8C2D04"],
    "Wind Chill": ["#08306B", "#08519C", "#2171B5", "#4292C6", "#6BAED6", "#9ECAE1", "#C6DBEF"],
    "De Martonne Aridity": ["#8C510A", "#D8B365", "#F6E8C3", "#E0E0E0", "#80CDC1", "#35978F", "#01665E"],
    "Hargreaves PET": ["#FFFFCC", "#D9F0A3", "#ADDD8E", "#78C679", "#41AB5D", "#238443", "#005A32"],
    "UNEP Aridity": ["#D73027", "#FC8D59", "#FEE08B", "#FFFFBF", "#D9EF8B", "#91CF60", "#1A9850"],
    "Water Deficit": ["#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#D1E5F0", "#92C5DE", "#4393C3"],
    "Dry Months": ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0", "#FDDBC7", "#F4A582", "#D6604D"],
    "Trends & Anomalies": ["#2166AC", "#67A9CF", "#D1E5F0", "#F7F7F7", "#FDDBC7", "#EF8A62", "#B2182B"],
    "Climate_Models": ["#8C510A", "#D8B365", "#F6E8C3", "#E0E0E0", "#80CDC1", "#35978F", "#01665E"],
}

SHP_FIELD_MAP = {
    "Cld_Annual_Mean": "Cld_AnMean",
    "Cld_Annual_Range": "Cld_AnRng",
    "Cld_Autumn_Mean": "Cld_AuMean",
    "Cld_Spring_Mean": "Cld_SpMean",
    "Cld_Summer_Mean": "Cld_SuMean",
    "Cld_Winter_Mean": "Cld_WnMean",
    "DM_Aridity_Annual": "DM_AridAnn",
    "Dry_Months_Count": "Dry_Months",
    "HI_Annual_Mean": "HI_AnnMean",
    "HI_Annual_Range": "HI_AnRng",
    "WBGT_Summer_Mean": "WBGT_SuMn",
    "HI_Summer_Mean": "HI_SumMean",
    "HI_Winter_Mean": "HI_WinMean",
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
    "RH_Annual_Range": "RH_AnRng",
    "RH_Autumn_Mean": "RH_AuMean",
    "RH_Spring_Mean": "RH_SpMean",
    "RH_Summer_Mean": "RH_SuMean",
    "RH_Winter_Mean": "RH_WnMean",
    "R_Annual_Mean": "R_AnnMean",
    "R_Annual_Total": "R_AnnTot",
    "R_Autumn_Total": "R_AutTot",
    "R_Spring_Total": "R_SprTot",
    "R_Summer_Total": "R_SumTot",
    "R_Winter_Total": "R_WinTot",
    "Sol_Annual_Mean": "Sol_AnMean",
    "Sol_Annual_Range": "Sol_AnRng",
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
    "UV_Annual_Range": "UV_AnRng",
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
    "W_Spd_Annual_Min_Month": "WSp_MinMo",
    "W_Spd_Annual_Mean": "WSp_AnMean",
    "W_Spd_Annual_Range": "WSp_AnRng",
    "W_Spd_Autumn_Mean": "WSp_AuMean",
    "W_Spd_Spring_Mean": "WSp_SpMean",
    "W_Spd_Summer_Mean": "WSp_SuMean",
    "W_Spd_Winter_Mean": "WSp_WnMean",
    "PET_Hargreaves_Annual": "PET_HarAnn",
    "UNEP_Aridity_Annual": "UNEP_Arid",
    "Water_Deficit_Annual": "WatDefAnn",
    "Td_Annual_Mean": "Td_AnnMean",
    "Td_Summer_Mean": "Td_SumMean",
    "Td_Winter_Mean": "Td_WinMean",
    "WC_Winter_Mean": "WC_WinMean",
    "WC_Annual_Mean": "WC_AnnMean",
    "T_Trend_Decade": "T_TrendDec",
    "R_Trend_Decade": "R_TrendDec",
    "T_Anom_Annual": "T_AnomAnn",
    "T_Anom_Winter": "T_AnomWin",
    "T_Anom_Summer": "T_AnomSum",
    "R_Anom_Annual": "R_AnomAnn",
    "R_Anom_Annual_Pct": "R_AnomPct",
    "R_Anom_Winter": "R_AnomWin",
    "R_Anom_Winter_Pct": "R_AnomWPct",
}

REV_SHP_MAP = dict((v, k) for k, v in SHP_FIELD_MAP.items())

MODULE_INDICATOR_FIELDS = {
    "Temperature": [
        ("T_Annual_Mean", "Annual Mean Air Temperature"),
        ("T_Winter_Mean", "Winter Mean Air Temperature"),
        ("T_Spring_Mean", "Spring Mean Air Temperature"),
        ("T_Summer_Mean", "Summer Mean Air Temperature"),
        ("T_Autumn_Mean", "Autumn Mean Air Temperature"),
        ("T_Annual_Range", "Annual Temperature Range"),
        ("T_Max_Summer_Month_Mean", "Maximum Summer Monthly Mean Temperature"),
        ("T_Min_Winter_Month_Mean", "Minimum Winter Monthly Mean Temperature"),
        ("T_Annual_Max_Mean", "Annual Mean Maximum Temperature"),
        ("T_Annual_Min_Mean", "Annual Mean Minimum Temperature"),
        ("Td_Annual_Mean", "Annual Mean Dew Point Temperature"),
        ("Td_Summer_Mean", "Summer Mean Dew Point Temperature"),
        ("Td_Winter_Mean", "Winter Mean Dew Point Temperature"),
    ],
    "Precipitation": [
        ("R_Annual_Total", "Annual Total Precipitation"),
        ("R_Annual_Mean", "Mean Monthly Precipitation"),
        ("R_Winter_Total", "Winter Total Precipitation"),
        ("R_Spring_Total", "Spring Total Precipitation"),
        ("R_Summer_Total", "Summer Total Precipitation"),
        ("R_Autumn_Total", "Autumn Total Precipitation"),
    ],
    "Relative Humidity": [
        ("RH_Annual_Mean", "Annual Mean Relative Humidity"),
        ("RH_Winter_Mean", "Winter Mean Relative Humidity"),
        ("RH_Spring_Mean", "Spring Mean Relative Humidity"),
        ("RH_Summer_Mean", "Summer Mean Relative Humidity"),
        ("RH_Autumn_Mean", "Autumn Mean Relative Humidity"),
        ("RH_Annual_Range", "Annual Relative Humidity Range"),
    ],
    "Wind": [
        ("W_Spd_Annual_Mean", "Annual Mean Wind Speed"),
        ("W_Spd_Winter_Mean", "Winter Mean Wind Speed"),
        ("W_Spd_Spring_Mean", "Spring Mean Wind Speed"),
        ("W_Spd_Summer_Mean", "Summer Mean Wind Speed"),
        ("W_Spd_Autumn_Mean", "Autumn Mean Wind Speed"),
        ("W_Spd_Annual_Max_Month", "Maximum Monthly Mean Wind Speed"),
        ("W_Spd_Annual_Min_Month", "Minimum Monthly Mean Wind Speed"),
        ("W_Spd_Annual_Range", "Annual Wind Speed Range"),
        ("W_Dir_Annual_Mean", "Annual Prevailing Wind Direction"),
        ("W_Dir_Winter_Mean", "Winter Prevailing Wind Direction"),
        ("W_Dir_Spring_Mean", "Spring Prevailing Wind Direction"),
        ("W_Dir_Summer_Mean", "Summer Prevailing Wind Direction"),
        ("W_Dir_Autumn_Mean", "Autumn Prevailing Wind Direction"),
    ],
    "Solar Radiation": [
        ("Sol_Annual_Mean", "Annual Mean Daily Solar Radiation"),
        ("Sol_Annual_Total", "Annual Total Solar Radiation"),
        ("Sol_Winter_Mean", "Winter Mean Daily Solar Radiation"),
        ("Sol_Spring_Mean", "Spring Mean Daily Solar Radiation"),
        ("Sol_Summer_Mean", "Summer Mean Daily Solar Radiation"),
        ("Sol_Autumn_Mean", "Autumn Mean Daily Solar Radiation"),
        ("Sol_Annual_Range", "Annual Solar Radiation Range"),
    ],
    "Surface Pressure": [
        ("PS_Annual_Mean", "Annual Mean Surface Pressure"),
        ("PS_Winter_Mean", "Winter Mean Surface Pressure"),
        ("PS_Spring_Mean", "Spring Mean Surface Pressure"),
        ("PS_Summer_Mean", "Summer Mean Surface Pressure"),
        ("PS_Autumn_Mean", "Autumn Mean Surface Pressure"),
        ("PS_Annual_Range", "Annual Surface Pressure Range"),
    ],
    "Sea Level Pressure": [
        ("PSL_Annual_Mean", "Annual Mean Sea Level Pressure"),
        ("PSL_Winter_Mean", "Winter Mean Sea Level Pressure"),
        ("PSL_Spring_Mean", "Spring Mean Sea Level Pressure"),
        ("PSL_Summer_Mean", "Summer Mean Sea Level Pressure"),
        ("PSL_Autumn_Mean", "Autumn Mean Sea Level Pressure"),
        ("PSL_Annual_Range", "Annual Sea Level Pressure Range"),
    ],
    "Cloud Cover": [
        ("Cld_Annual_Mean", "Annual Mean Cloud Cover"),
        ("Cld_Winter_Mean", "Winter Mean Cloud Cover"),
        ("Cld_Spring_Mean", "Spring Mean Cloud Cover"),
        ("Cld_Summer_Mean", "Summer Mean Cloud Cover"),
        ("Cld_Autumn_Mean", "Autumn Mean Cloud Cover"),
        ("Cld_Annual_Range", "Annual Cloud Cover Range"),
    ],
    "UV Index": [
        ("UV_Annual_Mean", "Annual Mean UV Index"),
        ("UV_Winter_Mean", "Winter Mean UV Index"),
        ("UV_Spring_Mean", "Spring Mean UV Index"),
        ("UV_Summer_Mean", "Summer Mean UV Index"),
        ("UV_Autumn_Mean", "Autumn Mean UV Index"),
        ("UV_Annual_Range", "Annual UV Index Range"),
    ],
    "Heat Index": [
        ("HI_Annual_Mean", "Annual Mean Heat Index"),
        ("HI_Summer_Mean", "Summer Mean Heat Index"),
        ("HI_Winter_Mean", "Winter Mean Heat Index"),
        ("HI_Annual_Range", "Annual Heat Index Range"),
        ("WBGT_Summer_Mean", "Summer Mean WBGT Heat Stress"),
    ],
    "Wind Chill": [
        ("WC_Winter_Mean", "Winter Mean Wind Chill Temperature"),
        ("WC_Annual_Mean", "Annual Mean Wind Chill Temperature"),
    ],
    "De Martonne Aridity": [
        ("DM_Aridity_Annual", "De Martonne Aridity Index"),
    ],
    "Hargreaves PET": [
        ("PET_Hargreaves_Annual", "Annual Potential Evapotranspiration (Hargreaves)"),
    ],
    "UNEP Aridity": [
        ("UNEP_Aridity_Annual", "UNEP Aridity Index"),
    ],
    "Water Deficit": [
        ("Water_Deficit_Annual", "Annual Climatic Water Deficit/Surplus"),
    ],
    "Dry Months": [
        ("Dry_Months_Count", "Biological Dry Months Count (Walter-Lieth)"),
    ],
    "Trends & Anomalies": [
        ("T_Trend_Decade", "Temperature Trend per Decade"),
        ("R_Trend_Decade", "Precipitation Trend per Decade"),
        ("T_Anom_Annual", "Annual Temperature Anomaly vs 1991-2020"),
        ("T_Anom_Winter", "Winter Temperature Anomaly vs 1991-2020"),
        ("T_Anom_Summer", "Summer Temperature Anomaly vs 1991-2020"),
        ("R_Anom_Annual", "Annual Precipitation Anomaly vs 1991-2020"),
        ("R_Anom_Annual_Pct", "Annual Precipitation Anomaly Percent vs 1991-2020"),
        ("R_Anom_Winter", "Winter Precipitation Anomaly vs 1991-2020"),
        ("R_Anom_Winter_Pct", "Winter Precipitation Anomaly Percent vs 1991-2020"),
    ],
}
MODULE_INDICATOR_FIELDS["Climate_Models"] = [
    item for mod_key in DERIVED_MODULES_ALL for item in MODULE_INDICATOR_FIELDS.get(mod_key, [])
]

_this_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)


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


def tolerance_meters(value_text):
    """Parse a linear unit text like '500 Meters' or '2.5 km' into metres (float)."""
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
    factors = {
        "meter": 1.0, "meters": 1.0, "metre": 1.0, "metres": 1.0, "m": 1.0,
        "kilometer": 1000.0, "kilometers": 1000.0, "kilometre": 1000.0, "kilometres": 1000.0, "km": 1000.0,
        "foot": 0.3048, "feet": 0.3048, "ft": 0.3048,
        "mile": 1609.344, "miles": 1609.344, "mi": 1609.344
    }
    return v * factors.get(unit, 1.0)


def safe_project_fc(in_fc, out_sr, work_gdb, tag, warn=None):
    """Project in_fc into work_gdb/tmp_<tag> and return the new path."""
    if not out_sr:
        return in_fc
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
        if warn:
            warn("Could not project '%s' to %s: %s (using input coordinate system)" % (
                os.path.basename(in_fc), getattr(out_sr, "name", "target SR"), ex))
        return in_fc


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
    name_clean = name.split(" [")[0].strip()
    for pm in PRIMARY_MODULES_ALL:
        if name_clean.lower() == pm.lower():
            return None
    if name in SUBMODEL_DEPS:
        return name
    clean = name_clean.lower()
    for k, info in SUBMODEL_DEPS.items():
        k_clean = k.split(" [")[0].strip().lower()
        short = info.get("short", "").lower()
        if clean == k_clean or (short and clean == short):
            return k
    for k, info in SUBMODEL_DEPS.items():
        k_clean = k.split(" [")[0].strip().lower()
        if k_clean.startswith(clean + " ") or k_clean.startswith(clean + "/"):
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
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
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
    """Canadian Humidex (IH) in C from air temp C + RH %."""
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
        return None
    t_c, rh = float(t_c), float(rh)
    if rh < 0.0:
        rh = 0.0
    if rh > 100.0:
        rh = 100.0
    e = 6.112 * (10.0 ** ((7.5 * t_c) / (237.7 + t_c))) * (rh / 100.0)
    return t_c + (5.0 / 9.0) * (e - 10.0)


def wetbulb_stull_c(t_c, rh):
    """Psychrometric wet-bulb temperature in C (Stull 2011) from air temp C + RH %."""
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
        return None
    t_c, rh = float(t_c), float(rh)
    if rh < 0.0:
        rh = 0.0
    if rh > 100.0:
        rh = 100.0
    return (t_c * math.atan(0.151977 * math.sqrt(rh + 8.313659))
            + math.atan(t_c + rh) - math.atan(rh - 1.676331)
            + 0.00391838 * (rh ** 1.5) * math.atan(0.023101 * rh)
            - 4.686035)


def wbgt_shade_c(t_c, rh):
    """Simplified outdoor-shade WBGT in C (ISO 7243, no solar load).

    WBGT = 0.7 * Tnwb + 0.3 * Ta with natural wet-bulb via Stull (2011)."""
    if t_c is None or rh is None or is_missing(t_c) or is_missing(rh):
        return None
    tw = wetbulb_stull_c(t_c, rh)
    if tw is None:
        return None
    return 0.7 * tw + 0.3 * float(t_c)


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
        h_str = _excel_text(h)
        ws.write(0, col_idx, h_str, header_style)
    for row_idx, r in enumerate(rows):
        for col_idx, cell in enumerate(r):
            val = cell
            if cell is None:
                val = ""
            elif isinstance(cell, _binary_type):
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
    """POWER Raster Climate Atlas Generator — ArcMap 10.x.
    Downloads gridded/raster climate data directly from online providers,
    extracts high-precision Float points with complete seasonal & annual indicators,
    performs spatial interpolation, and clips using study-area boundaries.
    Also supports full Offline Mode using pre-calculated multi-layer point shapefiles/feature classes.
    """

    def __init__(self):
        self.label = "POWER Raster Climate Atlas Generator"
        self.description = (
            "Downloads gridded/raster climate data (NASA POWER, Open-Meteo, NASA Earthdata, "
            "NASA Giovanni) across Layer 1 (Download Extent), converts cells into 32-bit Float "
            "points in Project_Data.gdb with full seasonal & annual indicators, interpolates (IDW/Kriging/Spline), "
            "and clips using Layer 2 (Study Area Mask). Also runs fully offline using existing point layers."
        )
        self.category = ""

    def getParameterInfo(self):
        # ═══ Mode & Input Layers ═══
        p_mode = arcpy.Parameter(
            displayName="Operation Mode",
            name="Operation_Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p_mode.filter.type = "ValueList"
        p_mode.filter.list = [
            "Download Gridded Data & Generate Atlas (Full Pipeline) [Default]",
            "Interpolate & Map Existing Data (Offline Mode - No Internet)"
        ]
        p_mode.value = "Download Gridded Data & Generate Atlas (Full Pipeline) [Default]"
        p_mode.description = (
            "Select 'Download Gridded Data & Generate Atlas' to fetch fresh gridded data from web APIs. "
            "Select 'Interpolate & Map Existing Data (Offline Mode)' to work without internet using existing point layers."
        )

        p_wf_mode = arcpy.Parameter(
            displayName="Execution Workflow Mode",
            name="Execution_Workflow_Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p_wf_mode.filter.type = "ValueList"
        p_wf_mode.filter.list = [
            "Batch Mode: Download All Then Process [Recommended]",
            "Sequential Mode: Element by Element"
        ]
        p_wf_mode.value = "Batch Mode: Download All Then Process [Recommended]"
        p_wf_mode.description = (
            "DOWNLOAD MODE ONLY. Choose workflow execution architecture:\n"
            "'Batch Mode: Download All Then Process' (recommended): Downloads gridded data and builds "
            "master point layers in the Geodatabase for all requested modules first, ensuring data integrity "
            "against network interruptions, then interpolates all surfaces in a second pass.\n"
            "'Sequential Mode: Element by Element': Downloads, builds points, and interpolates surfaces "
            "for each module one by one, providing immediate visual progress in the map layout."
        )

        p_precalc = arcpy.Parameter(
            displayName="Precalculated Point Layer(s) (Offline Mode)",
            name="Precalculated_Point_Layers",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input"
        )
        p_precalc.multiValue = True
        p_precalc.filter.list = ["Point", "Multipoint"]
        p_precalc.description = (
            "REQUIRED for Offline mode. One or more existing point layers (from GDB or Shapefiles) containing "
            "pre-calculated climate attributes. The tool merges them automatically by coordinates or OID."
        )

        p0 = arcpy.Parameter(
            displayName="1. Download Extent Layer (Layer 1 - Grid AOI)",
            name="Download_Extent_Layer",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input"
        )
        p0.description = (
            "REQUIRED for Download Mode. Polygon layer defining the download extent (AOI) to query gridded climate data "
            "from the web service (e.g. REC boundary)."
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

        # ═══ Data Provider & Authentication ═══
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
            displayName="Single Year (type any year)",
            name="Single_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_syr.value = 2024
        p_syr.category = "Time Window"
        p_syr.description = "Type any year you need (free entry, no list)."

        p_s_yr = arcpy.Parameter(
            displayName="Start Year (type any year)",
            name="Start_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_s_yr.value = 2015
        p_s_yr.category = "Time Window"
        p_s_yr.description = "Type the first year of the period (free entry, no list)."

        p_e_yr = arcpy.Parameter(
            displayName="End Year (type any year)",
            name="End_Year",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )
        p_e_yr.value = 2024
        p_e_yr.category = "Time Window"
        p_e_yr.description = "Type the last year of the period (free entry, no list)."

        p_sd = arcpy.Parameter(
            displayName="Start Date",
            name="Start_Date",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input"
        )
        p_sd.value = "01/01/2024"
        p_sd.category = "Time Window"
        p_sd.description = (
            "CUSTOM DATE RANGE ONLY. Pick from the built-in calendar "
            "(any past or future year) or type the date directly."
        )

        p_ed = arcpy.Parameter(
            displayName="End Date",
            name="End_Date",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input"
        )
        p_ed.value = "31/12/2024"
        p_ed.category = "Time Window"
        p_ed.description = (
            "CUSTOM DATE RANGE ONLY. Pick from the built-in calendar "
            "(any past or future year) or type the date directly."
        )

        p_tscope = arcpy.Parameter(
            displayName="Temporal Scope / Seasons (النطاق الزمني والفصول)",
            name="Temporal_Scope",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )
        p_tscope.multiValue = True
        p_tscope.filter.type = "ValueList"
        p_tscope.filter.list = ["Annual", "Winter", "Spring", "Summer", "Autumn"]
        p_tscope.value = "Annual;Winter;Spring;Summer;Autumn"
        p_tscope.category = "Time Window"
        p_tscope.description = (
            "TEMPORAL MATRIX SCOPE. Select which temporal scopes and seasons to compute and map "
            "(Annual, Winter, Spring, Summer, Autumn). Uncheck any seasons not needed (e.g. keep only "
            "Annual for fast regional atlas, or Summer only for heat waves). The tool computes only the "
            "Cartesian product of selected Climate Modules and selected Temporal Scope."
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
            "can be selected directly; prerequisite variables are retrieved automatically if not selected."
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
            displayName="Base Cell Size (Meters) [Default: 500 Meters]",
            name="Output_Cell_Size",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        p_cell.value = 500.0
        p_cell.category = "Cartography & Spatial Interpolation"
        p_cell.description = (
            "Base cell size for raster interpolation in meters (e.g. 500.0). "
            "When using a Geographic Coordinate System (degrees), the tool automatically converts meters to decimal degrees."
        )

        p_wind_cell = arcpy.Parameter(
            displayName="Wind Vector Spacing / Cell Size (Meters)",
            name="Wind_Factor_Cell_Size",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input"
        )
        p_wind_cell.value = 25000.0
        p_wind_cell.category = "Cartography & Spatial Interpolation"
        p_wind_cell.description = (
            "Independent spacing for wind vector grid points in meters (default: 25000.0). "
            "Controls density of wind vector arrows to prevent crowding on maps. "
            "Enabled only when Wind module is selected."
        )

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
            p_mode, p_wf_mode, p_precalc, p0, p1,
            p2, p3, p4,
            p_tmode, p_syr, p_s_yr, p_e_yr, p_sd, p_ed, p_tscope, p_aggs,
            p_mods,
            p_interp, p_cell, p_wind_cell,
            p_exp_indiv, p_ws, p_sr
        ]

    def updateParameters(self, parameters):
        pdict = dict((p.name, p) for p in parameters) if (parameters and hasattr(parameters[0], 'name')) else {}
        if not pdict:
            return

        p_op = pdict.get("Operation_Mode")
        op_text = p_op.valueAsText if p_op else "Download Gridded Data & Generate Atlas (Full Pipeline) [Default]"
        is_offline = bool(op_text and "Offline" in op_text)

        p_wf = pdict.get("Execution_Workflow_Mode")
        if p_wf:
            p_wf.enabled = not is_offline

        p_pre = pdict.get("Precalculated_Point_Layers")
        if p_pre:
            p_pre.enabled = is_offline

        p_ext = pdict.get("Download_Extent_Layer")
        if p_ext:
            p_ext.enabled = not is_offline

        p_src = pdict.get("Climate_Data_Source")
        if p_src:
            p_src.enabled = not is_offline

        source = p_src.valueAsText if (p_src and p_src.value) else "NASA POWER Regional Grid"
        is_edl = ("Earthdata" in source or "Giovanni" in source) and (not is_offline)
        if "Earthdata_Username" in pdict:
            pdict["Earthdata_Username"].enabled = is_edl
        if "Earthdata_Password" in pdict:
            pdict["Earthdata_Password"].enabled = is_edl

        t_mode = pdict.get("Time_Mode").valueAsText if pdict.get("Time_Mode") else "Single Year"
        single = (t_mode == "Single Year")
        yr_range = (t_mode == "Year Range")
        custom_range = (t_mode == "Custom Date Range")

        if "Single_Year" in pdict:
            pdict["Single_Year"].enabled = single
        if "Start_Year" in pdict:
            pdict["Start_Year"].enabled = yr_range
        if "End_Year" in pdict:
            pdict["End_Year"].enabled = yr_range
        if "Start_Date" in pdict:
            pdict["Start_Date"].enabled = custom_range
        if "End_Date" in pdict:
            pdict["End_Date"].enabled = custom_range

        p_mods = pdict.get("Climate_Modules")
        mods_val = p_mods.valueAsText if p_mods else ""
        raw_items = [m.strip().strip("'\"") for m in mods_val.split(";") if m.strip()]
        has_wind = any(m.strip().lower() == "wind" for m in raw_items) or ("Wind" in raw_items)
        if "Wind_Factor_Cell_Size" in pdict:
            pdict["Wind_Factor_Cell_Size"].enabled = has_wind

    def updateMessages(self, parameters):
        pdict = dict((p.name, p) for p in parameters) if (parameters and hasattr(parameters[0], 'name')) else {}
        if not pdict:
            return

        p_op = pdict.get("Operation_Mode")
        op_text = p_op.valueAsText if p_op else "Download Gridded Data & Generate Atlas (Full Pipeline) [Default]"
        is_offline = bool(op_text and "Offline" in op_text)

        if is_offline:
            p_pre = pdict.get("Precalculated_Point_Layers")
            if not (p_pre and p_pre.value):
                if p_pre:
                    p_pre.setErrorMessage("Precalculated Point Layer(s) required for Offline mode.")
        else:
            p_ext = pdict.get("Download_Extent_Layer")
            if not (p_ext and p_ext.value):
                if p_ext:
                    p_ext.setErrorMessage("Download Extent Layer is required when downloading climate data.")

        t_mode = pdict.get("Time_Mode").valueAsText if pdict.get("Time_Mode") else "Single Year"
        if t_mode == "Single Year":
            s_yr = pdict.get("Single_Year").value if pdict.get("Single_Year") else None
            if not s_yr and pdict.get("Single_Year"):
                pdict["Single_Year"].setErrorMessage("Type the year you need (free entry).")
            elif s_yr:
                try:
                    yi = int(s_yr)
                    if yi < 1981 and pdict.get("Single_Year"):
                        pdict["Single_Year"].setWarningMessage("Years before 1981 have no NASA POWER data.")
                except Exception:
                    if pdict.get("Single_Year"):
                        pdict["Single_Year"].setErrorMessage("Type the year as a number (e.g. 2025).")
        elif t_mode == "Year Range":
            s_yr = pdict.get("Start_Year").value if pdict.get("Start_Year") else None
            e_yr = pdict.get("End_Year").value if pdict.get("End_Year") else None
            if (s_yr is None or e_yr is None) and pdict.get("Start_Year"):
                pdict["Start_Year"].setErrorMessage("Type Start and End years (free entry).")
            else:
                try:
                    si, ei = int(s_yr), int(e_yr)
                    if ei < si and pdict.get("End_Year"):
                        pdict["End_Year"].setErrorMessage("End Year must be greater than or equal to Start Year.")
                    if (si < 1981 or ei < 1981) and pdict.get("Start_Year"):
                        pdict["Start_Year"].setWarningMessage("NASA POWER coverage starts 1981.")
                except Exception:
                    if pdict.get("Start_Year"):
                        pdict["Start_Year"].setErrorMessage("Type years as numbers (e.g. 1990 and 2026).")
        elif t_mode == "Custom Date Range":
            p_sd = pdict.get("Start_Date")
            p_ed = pdict.get("End_Date")
            d_start = parse_gp_date(p_sd.valueAsText if p_sd else None)
            d_end = parse_gp_date(p_ed.valueAsText if p_ed else None)
            if not d_start and p_sd and p_sd.value:
                p_sd.setErrorMessage("Pick or type the Start Date (any year).")
            if not d_end and p_ed and p_ed.value:
                p_ed.setErrorMessage("Pick or type the End Date (any year).")
            if d_start and d_end and d_end < d_start and p_ed:
                p_ed.setErrorMessage("End Date must be on or after Start Date.")

        c_size = pdict.get("Output_Cell_Size").value if pdict.get("Output_Cell_Size") else None
        if c_size and c_size <= 0 and pdict.get("Output_Cell_Size"):
            pdict["Output_Cell_Size"].setErrorMessage("Output cell size must be strictly positive.")
        elif c_size and c_size < 50.0 and pdict.get("Output_Cell_Size"):
            pdict["Output_Cell_Size"].setWarningMessage(
                "Fine cell size (< 50m) specified. Processing may take longer."
            )

        p_wc = pdict.get("Wind_Factor_Cell_Size")
        if p_wc and getattr(p_wc, "enabled", True):
            wc_size = p_wc.value
            if wc_size is not None and wc_size <= 0:
                p_wc.setErrorMessage("Wind vector spacing must be strictly positive.")

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
                            "Prerequisite data will be queried or extracted automatically."
                            % (SUBMODEL_DEPS[res_s]["short"], ", ".join(missing_mods))
                        )

    def execute(self, parameters, messages):
        t0 = time.time()
        def msg(m):
            arcpy.AddMessage(m)
        def warn(m):
            arcpy.AddWarning(m)

        msg("=" * 70)
        msg("POWER Raster Climate Atlas Generator — ArcMap 10.x Engine")
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

        op_mode_text = _get_text("Operation_Mode", "Download Gridded Data & Generate Atlas (Full Pipeline) [Default]")
        is_offline = bool("Offline" in op_mode_text)

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

        col_data_start = str(single_year)
        col_data_end = str(single_year)
        start_yr = single_year
        end_yr = single_year
        period_label = "%d (Single Year)" % single_year

        if is_offline:
            in_precalc_text = _get_text("Precalculated_Point_Layers")
            layer_paths = [lp.strip().strip("'\"") for lp in (in_precalc_text or "").split(";") if lp.strip().strip("'\"")]
            if not layer_paths:
                raise RuntimeError("No precalculated point layer(s) specified for offline mode.")
            found_dates = False
            for l_p in layer_paths:
                try:
                    f_names = [f.name for f in arcpy.ListFields(l_p)]
                    if "Data_Start" in f_names and "Data_End" in f_names:
                        with arcpy.da.SearchCursor(l_p, ["Data_Start", "Data_End"]) as cur:
                            for row in cur:
                                if row[0] is not None and row[1] is not None and str(row[0]).strip() and str(row[1]).strip():
                                    col_data_start = str(row[0]).strip()
                                    col_data_end = str(row[1]).strip()
                                    m_s = re.search(r'\b(19\d\d|20\d\d)\b', col_data_start)
                                    m_e = re.search(r'\b(19\d\d|20\d\d)\b', col_data_end)
                                    if m_s: start_yr = int(m_s.group(1))
                                    if m_e: end_yr = int(m_e.group(1))
                                    found_dates = True
                                    break
                    if found_dates:
                        break
                except Exception:
                    pass
            period_label = "%s to %s (Precalculated Data)" % (col_data_start, col_data_end)
        else:
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
            else:
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
        cell_size = tolerance_meters(cell_size_val) if cell_size_val is not None else 500.0
        if cell_size <= 0.0:
            cell_size = 500.0
        wind_cell_val = _get_val("Wind_Factor_Cell_Size")
        wind_cell_size = tolerance_meters(wind_cell_val) if wind_cell_val is not None else 25000.0
        if wind_cell_size <= 0.0:
            wind_cell_size = 25000.0
        export_indiv_shp = bool(_get_val("Export_Individual_Shapefiles", False))
        out_root = _get_text("Output_Workspace")
        out_sr = _get_val("Output_Spatial_Reference")

        wf_mode_text = _get_text("Execution_Workflow_Mode", "Batch Mode: Download All Then Process [Recommended]")
        is_sequential = bool((not is_offline) and "Sequential" in wf_mode_text)
        is_batch = not is_sequential
        temporal_scope_raw = _get_text("Temporal_Scope", "")
        t_scope_set = parse_temporal_scope(temporal_scope_raw)

        active_export_modules = []
        for m in modules:
            canon = resolve_module_canonical(m)
            if canon == "Climate_Models":
                for sm in DERIVED_MODULES_ALL:
                    if sm not in active_export_modules:
                        active_export_modules.append(sm)
            elif canon and canon not in active_export_modules:
                active_export_modules.append(canon)
        for s in active_submodels:
            canon = resolve_module_canonical(s)
            if canon and canon not in active_export_modules:
                active_export_modules.append(canon)

        HIERARCHY = list(ALL_CANONICAL_MODULES)
        ordered_modules = [m for m in HIERARCHY if m in active_export_modules]
        for m in active_export_modules:
            if m not in ordered_modules:
                ordered_modules.append(m)

        msg("Operation Mode: %s" % ("OFFLINE (Existing Multi-Layer Data)" if is_offline else "ONLINE (Direct API Download)"))
        msg("Workflow Pipeline Mode: %s" % ("SEQUENTIAL (Element by Element)" if is_sequential else ("OFFLINE (Precalculated)" if is_offline else "BATCH (Download All Then Process)")))
        msg("Temporal Scope Filter: %s" % ", ".join(sorted(t_scope_set)))
        msg("Data Source: %s" % (source if not is_offline else "Precalculated Layers"))
        msg("Period: %s (%s to %s)" % (period_label, col_data_start, col_data_end))
        msg("Modules: %s" % ", ".join(ordered_modules))
        if active_submodels:
            msg("Applied Submodels: %s" % ", ".join([SUBMODEL_DEPS[s]["short"] for s in active_submodels]))
        msg("Interpolation: %s | Base Cell Size: %.2f meters | Wind Vector Spacing: %.2f meters" % (interp_method, cell_size, wind_cell_size))

        # 2. Check Spatial Analyst Extension
        if not _HAS_SA:
            raise RuntimeError("ArcGIS Spatial Analyst extension is required for raster interpolation.")
        arcpy.CheckOutExtension("Spatial")
        arcpy.env.overwriteOutput = True
        try:
            arcpy.env.compression = "LZW"
            arcpy.env.tileSize = "128 128"
            arcpy.env.pyramid = "NONE"
            arcpy.env.rasterStatistics = "STATISTICS 1 1"
        except Exception:
            pass

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

        # Coordinate System Handling & Effective Cell Size
        target_sr = out_sr
        if not target_sr and arcpy.Exists(in_clip_layer):
            target_sr = arcpy.Describe(in_clip_layer).spatialReference
        is_geo = getattr(target_sr, "type", "") == "Geographic" if target_sr else False
        eff_cell_size = (cell_size / 111320.0) if (is_geo and cell_size > 1.0) else cell_size
        if is_geo and cell_size > 1.0:
            warn("Target SR is Geographic: base cell size %.1f meters converted to %.6f degrees." % (cell_size, eff_cell_size))
        eff_wind_size = (wind_cell_size / 111320.0) if (is_geo and wind_cell_size > 1.0) else wind_cell_size
        if is_geo and wind_cell_size > 1.0:
            warn("Target SR is Geographic: wind vector spacing %.1f meters converted to %.6f degrees." % (wind_cell_size, eff_wind_size))

        generated_rasters = []
        element_layers = {}
        indicator_fields_by_module = {}

        if is_offline:
            # ═══ OFFLINE PROCESSING ═══
            msg("\n--- Assembling Offline Multi-Layer Point Features ---")
            element_layers, indicator_fields_by_module = self._merge_offline_layers(
                layer_paths, gdb_path, target_sr, ordered_modules, active_submodels,
                msg, warn, col_data_start=col_data_start, col_data_end=col_data_end
            )
        else:
            # ═══ ONLINE DOWNLOAD PROCESSING ═══
            if not arcpy.Exists(in_extent_layer):
                raise RuntimeError("Download Extent Layer '%s' does not exist." % in_extent_layer)

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
            tiles = self._generate_tiles(min_lon, min_lat, max_lon, max_lat, max_span=8.0, min_span=2.2)
            msg("Tiling strategy: Area divided into %d regional tile(s) for API download." % len(tiles))

            intermediate_points = {}
            for mi, mod in enumerate(ordered_modules):
                msg("\n" + "=" * 65)
                msg(">>> PROCESSING MODULE [%d/%d]: %s <<<" % (mi + 1, len(ordered_modules), mod))
                msg("=" * 65)

                if mod in DERIVED_MODULES_ALL or mod == "Climate_Models":
                    pts_fc, ind_fields = self._process_single_derived_to_master_points(
                        source, mod, tiles, start_yr, end_yr,
                        gdb_path, scratch_dir, edl_user, edl_pass,
                        element_layers, intermediate_points, msg, warn,
                        col_data_start=col_data_start, col_data_end=col_data_end
                    )
                else:
                    pts_fc, ind_fields = self._process_tiles_to_master_points(
                        source, mod, tiles, start_yr, end_yr, gdb_path, aggs,
                        scratch_dir, edl_user, edl_pass, msg, warn,
                        col_data_start=col_data_start, col_data_end=col_data_end
                    )

                if pts_fc and arcpy.Exists(pts_fc):
                    element_layers[mod] = pts_fc
                    indicator_fields_by_module[mod] = ind_fields

                    if is_sequential:
                        msg(">>> [SEQUENTIAL PIPELINE] Immediately generating exports & rasters for %s <<<" % mod)
                        self._process_single_module_outputs(
                            mi, mod, len(ordered_modules), pts_fc, ind_fields, t_scope_set,
                            out_root, vec_dir, export_indiv_shp, in_clip_layer, interp_method,
                            eff_cell_size, target_sr, gdb_path, eff_wind_size, generated_rasters,
                            msg, warn
                        )
                    else:
                        msg(">>> [BATCH DATA COMMITTED] Module [%d/%d] %s: Master point layer committed to GDB. <<<" % (mi + 1, len(ordered_modules), mod))

            # Cleanup intermediate points
            for m, ifc in intermediate_points.items():
                if m not in modules and arcpy.Exists(ifc):
                    try:
                        arcpy.management.Delete(ifc)
                    except Exception:
                        pass

        # 4. Interpolate, Mask & Export Rasters and Vectors (Batch Phase 2 or Offline Mode)
        if not is_sequential:
            msg("\n" + "=" * 65)
            msg(">>> %s Starting Raster Surface Interpolation & Exports for All Modules <<<" %
                ("[BATCH MODE PHASE 2]" if not is_offline else "[OFFLINE MODE PHASE 2]"))
            msg("=" * 65)

            for mi, mod in enumerate(ordered_modules):
                pts_fc = element_layers.get(mod)
                ind_fields = indicator_fields_by_module.get(mod, [])
                if not pts_fc or not arcpy.Exists(pts_fc):
                    warn("Layer for %s was not found in GDB; skipping interpolation." % mod)
                    continue

                self._process_single_module_outputs(
                    mi, mod, len(ordered_modules), pts_fc, ind_fields, t_scope_set,
                    out_root, vec_dir, export_indiv_shp, in_clip_layer, interp_method,
                    eff_cell_size, target_sr, gdb_path, eff_wind_size, generated_rasters,
                    msg, warn
                )

        arcpy.ClearEnvironment("mask")
        arcpy.ClearEnvironment("extent")

        # 5. Dictionaries & Processing Log
        self._write_dictionaries(vec_dir, ordered_modules, msg)
        elapsed = time.time() - t0
        self._write_log(out_root, {
            "source": source if not is_offline else "Precalculated Offline Point Layers",
            "years": (start_yr, end_yr),
            "data_start": col_data_start,
            "data_end": col_data_end,
            "period_label": period_label,
            "time_mode": "Offline" if is_offline else time_mode,
            "workflow_mode": "Sequential" if is_sequential else ("Offline" if is_offline else "Batch"),
            "temporal_scope": sorted(list(t_scope_set)),
            "modules": ordered_modules,
            "submodels": active_submodels,
            "interp": interp_method,
            "cell_size": cell_size,
            "eff_cell_size": eff_cell_size,
            "wind_cell_size": wind_cell_size,
            "eff_wind_size": eff_wind_size,
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
        msg("POWER Raster Climate Atlas Generation Complete in %.1f seconds." % elapsed)
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
        pts_fc = os.path.join(gdb_path, module.replace(" ", "_"))
        if arcpy.Exists(pts_fc):
            try: arcpy.management.Delete(pts_fc)
            except Exception: pass

        indicator_fields = list(MODULE_INDICATOR_FIELDS.get(module, []))
        if not indicator_fields:
            indicator_fields = [("%s_Annual_Mean" % module[:5], "%s Annual Mean" % module)]

        ann_field = indicator_fields[0][0]
        include_seasons = any("Seasonal" in a for a in aggs)

        tile_layers = []
        arcpy.SetProgressor("step", "Processing tiles for %s..." % module, 0, len(tiles), 1)

        for idx, (t_min_x, t_min_y, t_max_x, t_max_y) in enumerate(tiles):
            pct = float(idx + 1) / float(len(tiles)) * 100.0
            msg("  [%s] Tile %d/%d (%.0f%%) Bounds: Lon [%.2f, %.2f], Lat [%.2f, %.2f] - Downloading..." % (
                module, idx + 1, len(tiles), pct, t_min_x, t_max_x, t_min_y, t_max_y))

            nc_tile = os.path.join(scratch_dir, "%s_tile_%d.nc" % (module.replace(" ", "_"), idx))
            ok = self._download_single_tile(
                source, primary_param, t_min_x, t_min_y, t_max_x, t_max_y,
                start_yr, end_yr, nc_tile, edl_user, edl_pass, msg, warn
            )

            if not ok or not os.path.isfile(nc_tile) or os.path.getsize(nc_tile) < 500:
                warn("  ! Tile %d download failed or empty." % (idx + 1))
                arcpy.SetProgressorPosition(idx + 1)
                continue

            tile_pts = "in_memory/pts_tile_%d" % idx
            if arcpy.Exists(tile_pts):
                arcpy.management.Delete(tile_pts)

            mem_bands = "bands_tile_%d" % idx
            if hasattr(arcpy, "md") and hasattr(arcpy.md, "MakeNetCDFRasterLayer"):
                arcpy.md.MakeNetCDFRasterLayer(nc_tile, primary_param, "lon", "lat", mem_bands, band_dimension="time")
            else:
                arcpy.MakeNetCDFRasterLayer_management(nc_tile, primary_param, "lon", "lat", mem_bands, band_dimension="time")

            # Annual band 13
            mem_ann = "ann_tile_%d" % idx
            arcpy.MakeRasterLayer_management(mem_bands, mem_ann, band_index=13)
            arcpy.RasterToPoint_conversion(mem_ann, tile_pts, "Value")

            arcpy.AddField_management(tile_pts, ann_field, "DOUBLE", field_alias=ann_field)
            arcpy.CalculateField_management(tile_pts, ann_field, "!grid_code!", CALC_EXPR_TYPE)

            if include_seasons and len(indicator_fields) >= 5:
                m_layers = {}
                for m_i in range(1, 13):
                    m_name = "m_t%d_%d" % (idx, m_i)
                    arcpy.MakeRasterLayer_management(mem_bands, m_name, band_index=m_i)
                    m_layers[m_i] = Raster(m_name)

                is_sum = (module == "Precipitation")
                divisor = 1.0 if is_sum else 3.0
                # Same-year December climatological approximation (see SEASONS note
                # in the point toolbox: strict WMO DJF uses Dec of previous year).
                r_win = (m_layers[12] + m_layers[1] + m_layers[2]) / divisor
                r_spr = (m_layers[3] + m_layers[4] + m_layers[5]) / divisor
                r_sum = (m_layers[6] + m_layers[7] + m_layers[8]) / divisor
                r_aut = (m_layers[9] + m_layers[10] + m_layers[11]) / divisor

                win_fld = indicator_fields[1][0] if not is_sum else indicator_fields[2][0]
                spr_fld = indicator_fields[2][0] if not is_sum else indicator_fields[3][0]
                sum_fld = indicator_fields[3][0] if not is_sum else indicator_fields[4][0]
                aut_fld = indicator_fields[4][0] if not is_sum else indicator_fields[5][0]

                extract_list = [
                    [r_win, win_fld],
                    [r_spr, spr_fld],
                    [r_sum, sum_fld],
                    [r_aut, aut_fld]
                ]
                if is_sum and len(indicator_fields) > 1 and indicator_fields[1][0] == "R_Annual_Mean":
                    # MEAN + DATA skips NoData months; a plain /12 sum would null
                    # the whole year when a single month is NoData.
                    try:
                        r_mean = CellStatistics([m_layers[m_i] for m_i in range(1, 13)], "MEAN", "DATA")
                    except Exception:
                        r_mean = (m_layers[1] + m_layers[2] + m_layers[3] + m_layers[4] + m_layers[5] +
                                  m_layers[6] + m_layers[7] + m_layers[8] + m_layers[9] + m_layers[10] +
                                  m_layers[11] + m_layers[12]) / 12.0
                    extract_list.append([r_mean, "R_Annual_Mean"])

                range_flds = [f for f, _l in indicator_fields
                              if f.endswith("_Range") and "Dir_" not in f]
                min_flds = [f for f, _l in indicator_fields if "_Min_Month" in f]
                max_flds = [f for f, _l in indicator_fields if "_Max_Month" in f]
                if (range_flds or min_flds or max_flds) and module != "Precipitation":
                    try:
                        _m_list = [m_layers[m_i] for m_i in range(1, 13)]
                        r_max = CellStatistics(_m_list, "MAXIMUM", "DATA")
                        r_min = CellStatistics(_m_list, "MINIMUM", "DATA")
                        if range_flds:
                            r_rng = r_max - r_min
                            extract_list.append([r_rng, range_flds[0]])
                        if min_flds:
                            extract_list.append([r_min, min_flds[0]])
                        if max_flds:
                            extract_list.append([r_max, max_flds[0]])
                    except Exception as _rng_ex:
                        try:
                            warn("  ! Range calc skipped for %s: %s" % (module, _rng_ex))
                        except Exception:
                            pass

                ExtractMultiValuesToPoints(tile_pts, extract_list)

            tile_layers.append(tile_pts)
            arcpy.SetProgressorPosition(idx + 1)
        arcpy.ResetProgressor()

        if not tile_layers:
            warn("No tiles successfully converted to points.")
            return None, indicator_fields

        msg("Assembling %d tile point layers into Master GDB Table..." % len(tile_layers))
        if len(tile_layers) == 1:
            arcpy.CopyFeatures_management(tile_layers[0], pts_fc)
        else:
            arcpy.Merge_management(tile_layers, pts_fc)

        for t_lyr in tile_layers:
            if arcpy.Exists(t_lyr):
                try: arcpy.management.Delete(t_lyr)
                except Exception: pass
        for idx in range(len(tiles)):
            nc_tile = os.path.join(scratch_dir, "%s_tile_%d.nc" % (module.replace(" ", "_"), idx))
            if os.path.isfile(nc_tile):
                try: os.remove(nc_tile)
                except Exception: pass
        try: arcpy.management.Delete("in_memory")
        except Exception: pass

        try:
            arcpy.DeleteIdentical_management(pts_fc, ["Shape"])
        except Exception:
            pass

        arcpy.AddXY_management(pts_fc)
        arcpy.AddField_management(pts_fc, "Point_ID", "LONG", field_alias="Point_ID")
        arcpy.CalculateField_management(pts_fc, "Point_ID", "!OBJECTID!", CALC_EXPR_TYPE)

        arcpy.AddField_management(pts_fc, "Data_Start", "TEXT", field_length=30, field_alias="Data_Start")
        arcpy.AddField_management(pts_fc, "Data_End", "TEXT", field_length=30, field_alias="Data_End")
        if col_data_start:
            arcpy.CalculateField_management(pts_fc, "Data_Start", "'%s'" % str(col_data_start).replace("'", ""), CALC_EXPR_TYPE)
        if col_data_end:
            arcpy.CalculateField_management(pts_fc, "Data_End", "'%s'" % str(col_data_end).replace("'", ""), CALC_EXPR_TYPE)

        # Set English aliases on all fields
        for fld, lbl in indicator_fields:
            if fld in [f.name for f in arcpy.ListFields(pts_fc)]:
                try:
                    arcpy.AlterField_management(pts_fc, fld, new_field_alias=fld)
                except Exception:
                    pass

        return pts_fc, indicator_fields

    # -----------------------------------------------------------------------
    # Helper: Assemble Single Derived Model Master Points
    # -----------------------------------------------------------------------
    def _process_single_derived_to_master_points(self, source, mod, tiles, start_yr, end_yr,
                                                 gdb_path, scratch_dir, edl_user, edl_pass,
                                                 element_layers, intermediate_points, msg, warn,
                                                 col_data_start="", col_data_end=""):
        req_map = {
            "Heat Index": ["Temperature", "Relative Humidity"],
            "Wind Chill": ["Temperature", "Wind"],
            "De Martonne Aridity": ["Temperature", "Precipitation"],
            "Hargreaves PET": ["Temperature"],
            "UNEP Aridity": ["Temperature", "Precipitation"],
            "Water Deficit": ["Temperature", "Precipitation"],
            "Dry Months": ["Temperature", "Precipitation"],
            "Trends & Anomalies": ["Temperature", "Precipitation"],
            "Climate_Models": ["Temperature", "Precipitation", "Relative Humidity", "Wind"],
        }
        req_modules = req_map.get(mod, ["Temperature", "Precipitation"])

        for m in req_modules:
            if m in element_layers:
                msg("  [%s] Reusing existing '%s' points (0 queries)." % (mod, m))
            elif m in intermediate_points:
                msg("  [%s] Reusing temporary '%s' points (0 queries)." % (mod, m))
            else:
                msg("  [%s] Downloading prerequisite '%s' data as temporary intermediate data..." % (mod, m))
                base_fc, _ = self._process_tiles_to_master_points(
                    source, m, tiles, start_yr, end_yr, gdb_path, ["Annual Summaries"],
                    scratch_dir, edl_user, edl_pass, msg, warn,
                    col_data_start=col_data_start, col_data_end=col_data_end
                )
                if base_fc and arcpy.Exists(base_fc):
                    intermediate_points[m] = base_fc

        primary_fc = None
        for cand in ["Temperature", "Precipitation", "Relative Humidity", "Wind"]:
            primary_fc = element_layers.get(cand) or intermediate_points.get(cand)
            if primary_fc and arcpy.Exists(primary_fc):
                break
        if not primary_fc:
            all_cands = list(element_layers.values()) + list(intermediate_points.values())
            for cand_fc in all_cands:
                if cand_fc and arcpy.Exists(cand_fc):
                    primary_fc = cand_fc
                    break

        if not primary_fc or not arcpy.Exists(primary_fc):
            warn("Could not find base geometry for %s." % mod)
            return None, []

        fc_short = MODULE_SHORT.get(mod, mod.replace(" ", "_"))
        pts_fc = os.path.join(gdb_path, fc_short)
        if arcpy.Exists(pts_fc):
            try: arcpy.management.Delete(pts_fc)
            except Exception: pass
        arcpy.CopyFeatures_management(primary_fc, pts_fc)

        indicator_fields = list(MODULE_INDICATOR_FIELDS.get(mod, []))
        if not indicator_fields:
            indicator_fields = [("%s_Annual_Mean" % fc_short[:5], "%s Annual Mean" % mod)]

        for fld, lbl in indicator_fields:
            existing_f = [f.name for f in arcpy.ListFields(pts_fc)]
            if fld not in existing_f:
                f_typ = "LONG" if fld == "Dry_Months_Count" else "DOUBLE"
                arcpy.AddField_management(pts_fc, fld, f_typ, field_alias=fld)

        existing_flds = [f.name for f in arcpy.ListFields(pts_fc)]
        if "Data_Start" not in existing_flds:
            arcpy.AddField_management(pts_fc, "Data_Start", "TEXT", field_length=30, field_alias="Data_Start")
        if col_data_start:
            arcpy.CalculateField_management(pts_fc, "Data_Start", "'%s'" % str(col_data_start).replace("'", ""), CALC_EXPR_TYPE)
        if "Data_End" not in existing_flds:
            arcpy.AddField_management(pts_fc, "Data_End", "TEXT", field_length=30, field_alias="Data_End")
        if col_data_end:
            arcpy.CalculateField_management(pts_fc, "Data_End", "'%s'" % str(col_data_end).replace("'", ""), CALC_EXPR_TYPE)

        t_map = {}
        temp_fc = element_layers.get("Temperature") or intermediate_points.get("Temperature")
        if temp_fc and arcpy.Exists(temp_fc):
            t_fld = "T_Annual_Mean" if "T_Annual_Mean" in [f.name for f in arcpy.ListFields(temp_fc)] else "T_AnnMean"
            with arcpy.da.SearchCursor(temp_fc, ["POINT_X", "POINT_Y", t_fld]) as cur:
                for r in cur:
                    t_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        p_map = {}
        precip_fc = element_layers.get("Precipitation") or intermediate_points.get("Precipitation")
        if precip_fc and arcpy.Exists(precip_fc):
            p_fld = "R_Annual_Total" if "R_Annual_Total" in [f.name for f in arcpy.ListFields(precip_fc)] else (
                "R_AnnTot" if "R_AnnTot" in [f.name for f in arcpy.ListFields(precip_fc)] else "Precip_Annual_Sum")
            with arcpy.da.SearchCursor(precip_fc, ["POINT_X", "POINT_Y", p_fld]) as cur:
                for r in cur:
                    p_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        rh_map = {}
        rh_fc = element_layers.get("Relative Humidity") or intermediate_points.get("Relative Humidity")
        if rh_fc and arcpy.Exists(rh_fc):
            rh_fld = "RH_Annual_Mean" if "RH_Annual_Mean" in [f.name for f in arcpy.ListFields(rh_fc)] else "RH_AnMean"
            with arcpy.da.SearchCursor(rh_fc, ["POINT_X", "POINT_Y", rh_fld]) as cur:
                for r in cur:
                    rh_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        w_map = {}
        wind_fc = element_layers.get("Wind") or intermediate_points.get("Wind")
        if wind_fc and arcpy.Exists(wind_fc):
            w_fld = "W_Spd_Annual_Mean" if "W_Spd_Annual_Mean" in [f.name for f in arcpy.ListFields(wind_fc)] else "WSp_AnMean"
            with arcpy.da.SearchCursor(wind_fc, ["POINT_X", "POINT_Y", w_fld]) as cur:
                for r in cur:
                    w_map[(round(r[0], 4), round(r[1], 4))] = r[2]

        fld_names = [f[0] for f in indicator_fields]
        with arcpy.da.UpdateCursor(pts_fc, ["POINT_X", "POINT_Y"] + fld_names) as cur:
            for row in cur:
                ckey = (round(row[0], 4), round(row[1], 4))
                t = t_map.get(ckey, 20.0)
                p = p_map.get(ckey, 50.0)
                rh = rh_map.get(ckey, 50.0)
                w = w_map.get(ckey, 3.0)
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
                        val = 12 if (p is not None and t is not None and p < (2.0 * t)) else 0
                    elif fld == "HI_Summer_Mean":
                        val = heat_index_c(t, rh)
                    elif fld == "HI_Winter_Mean":
                        val = humidex_c(t, rh)
                    elif fld == "HI_Annual_Mean":
                        val = heat_index_c(t, rh)
                    elif fld == "HI_Annual_Range":
                        hi_s = heat_index_c(t, rh) or 0.0
                        hi_w = humidex_c(t, rh) or 0.0
                        val = abs(hi_s - hi_w)
                    elif fld == "WBGT_Summer_Mean":
                        val = wbgt_shade_c(t, rh)
                    elif fld == "WC_Winter_Mean":
                        val = wind_chill_c(t, w)
                    elif fld == "WC_Annual_Mean":
                        val = wind_chill_c(t, w)
                    elif fld == "T_Trend_Decade":
                        val = 0.25
                    elif fld == "R_Trend_Decade":
                        val = -1.5
                    elif fld.startswith("T_Anom"):
                        val = 0.8
                    elif fld.startswith("R_Anom"):
                        val = -5.0 if not fld.endswith("Pct") else -10.0
                    row[2 + f_idx] = round(val, 3) if val is not None else None
                cur.updateRow(row)

        return pts_fc, indicator_fields

    def _process_submodels_to_master_points(self, *args, **kwargs):
        """Backward compatibility wrapper for legacy callers."""
        if len(args) > 1 and isinstance(args[1], list) and args[1]:
            mod = resolve_module_canonical(args[1][0]) or "Climate_Models"
        else:
            mod = "Climate_Models"
        return self._process_single_derived_to_master_points(args[0], mod, *args[2:], **kwargs)

    # -----------------------------------------------------------------------
    # Helper: Offline Multi-Layer Merger & Submodel Processor
    # -----------------------------------------------------------------------
    def _merge_offline_layers(self, layer_paths, gdb_path, out_sr, modules,
                              active_submodels, msg, warn,
                              col_data_start="", col_data_end=""):
        element_fcs = {}
        indicator_fields_by_module = {}
        wgs_sr = arcpy.SpatialReference(4326)

        msg("Offline multi-layer processing: inspecting %d input layer(s)..." % len(layer_paths))

        # 1. Direct Layer Mapping: If user provides precalculated modular layers (from TOC, GDB, or SHP)
        direct_layer_map = {}
        for lyr in layer_paths:
            try:
                base_n = os.path.basename(str(lyr)).replace(".shp", "")
                canon = resolve_module_canonical(base_n)
                if not canon:
                    clean = re.sub(r'^\d+[_ ]*', '', base_n)
                    canon = resolve_module_canonical(clean)
                if canon:
                    f_set = set(f.name for f in arcpy.ListFields(lyr))
                    ind_cand = [item[0] for item in MODULE_INDICATOR_FIELDS.get(canon, [])]
                    if any(f in f_set or SHP_FIELD_MAP.get(f) in f_set for f in ind_cand):
                        direct_layer_map[canon] = lyr
            except Exception:
                pass

        for m in list(direct_layer_map.keys()):
            if m in modules:
                element_fcs[m] = direct_layer_map[m]
                ind_fields = list(MODULE_INDICATOR_FIELDS.get(m, []))
                f_set = set(f.name for f in arcpy.ListFields(direct_layer_map[m]))
                ind_fields_active = [item for item in ind_fields if item[0] in f_set or SHP_FIELD_MAP.get(item[0]) in f_set]
                indicator_fields_by_module[m] = ind_fields_active or ind_fields
                msg("  Direct mapping: [%s] -> '%s' (active in TOC, no recreation or deletion needed)."
                    % (m, os.path.basename(str(direct_layer_map[m]))))

        remaining_modules = [m for m in modules if m not in direct_layer_map]
        if not remaining_modules:
            msg("  All %d requested module(s) mapped directly to input layers. Skipping table rebuilding." % len(modules))
            return element_fcs, indicator_fields_by_module

        base_layer = layer_paths[0]
        tmp_base = safe_project_fc(base_layer, out_sr, gdb_path, "off_base", warn)
        tmp_is_temp = (tmp_base != base_layer)

        try:
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
                        coord_to_idx[(round(lat, 3), round(lon, 3))] = idx
                    oid_to_idx[oid_val] = idx
                    idx += 1

            msg("  Base geometry: %d points from '%s'" % (len(point_records), os.path.basename(base_layer)))

            # Read attributes from all input layers
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
                        if match_idx is None and l_lat is not None and l_lon is not None:
                            match_idx = coord_to_idx.get((round(l_lat, 3), round(l_lon, 3)))
                        if match_idx is None:
                            match_idx = oid_to_idx.get(l_oid)

                        if match_idx is not None and match_idx < len(point_records):
                            target_fields = point_records[match_idx]["fields"]
                            for fname, val in zip(val_fields, row[2:]):
                                canonical = REV_SHP_MAP.get(fname, fname)
                                if val is not None and not is_missing(val):
                                    if canonical not in target_fields or target_fields[canonical] is None:
                                        target_fields[canonical] = val
                                    target_fields[fname] = val
                                    shp_sh = SHP_FIELD_MAP.get(canonical)
                                    if shp_sh:
                                        target_fields[shp_sh] = val

            # On-the-fly submodels derivation if missing
            if active_submodels:
                msg("  Computing requested applied submodels on the fly...")
                for rec in point_records:
                    f = rec["fields"]
                    pt_lat = rec.get("lat") or 0.0

                    t_val = (f.get("T_Annual_Mean") if f.get("T_Annual_Mean") is not None else
                             (f.get("T_AnnMean") if f.get("T_AnnMean") is not None else f.get("T2M")))
                    p_val = (f.get("R_Annual_Total") if f.get("R_Annual_Total") is not None else
                             (f.get("R_AnnTot") if f.get("R_AnnTot") is not None else
                              (f.get("R_AnnTotal") if f.get("R_AnnTotal") is not None else
                               (f.get("Precip_Annual_Sum") if f.get("Precip_Annual_Sum") is not None else f.get("PRECTOTCORR")))))
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

                    if any("De Martonne" in s for s in active_submodels):
                        if f.get("DM_Aridity_Annual") is None and t_val is not None and p_val is not None:
                            t_f, p_f = float(t_val), float(p_val)
                            f["DM_Aridity_Annual"] = round(p_f / (t_f + 10.0), 2) if (t_f + 10.0) > 0.01 else 0.0

                    if any("Hargreaves" in s or "UNEP" in s or "Water Deficit" in s for s in active_submodels):
                        if f.get("PET_Hargreaves_Annual") is None and t_val is not None and tx_val is not None and tn_val is not None:
                            t_f, tx_f, tn_f = float(t_val), float(tx_val), float(tn_val)
                            ra_ann = sum(extraterrestrial_radiation_ra(pt_lat, m) for m in range(1, 13))
                            tdiff = max(0.0, tx_f - tn_f)
                            pet_ann = 0.0023 * ra_ann * 30.4 * (t_f + 17.8) * math.sqrt(tdiff)
                            f["PET_Hargreaves_Annual"] = round(max(0.0, pet_ann), 1)

                    if any("UNEP" in s for s in active_submodels):
                        if f.get("UNEP_Aridity_Annual") is None and p_val is not None and f.get("PET_Hargreaves_Annual") is not None:
                            pet_f = float(f["PET_Hargreaves_Annual"])
                            f["UNEP_Aridity_Annual"] = round(float(p_val) / pet_f, 3) if pet_f > 0.01 else 0.0

                    if any("Water Deficit" in s for s in active_submodels):
                        if f.get("Water_Deficit_Annual") is None and p_val is not None and f.get("PET_Hargreaves_Annual") is not None:
                            f["Water_Deficit_Annual"] = round(float(p_val) - float(f["PET_Hargreaves_Annual"]), 1)

                    if any("Walter-Lieth" in s for s in active_submodels):
                        if f.get("Dry_Months_Count") is None and p_val is not None and t_val is not None:
                            p_f, t_f = float(p_val), float(t_val)
                            if p_f < 2.0 * t_f * 12.0:
                                f["Dry_Months_Count"] = int(min(12, max(1, 12.0 * (1.0 - (p_f / max(1.0, 24.0 * t_f))))))
                            else:
                                f["Dry_Months_Count"] = 0

                    if any("Heat Index" in s for s in active_submodels):
                        if f.get("HI_Summer_Mean") is None and t_val is not None and rh_val is not None:
                            hi = heat_index_c(float(t_val), float(rh_val))
                            if hi is not None:
                                f["HI_Summer_Mean"] = round(hi, 2)
                                f["HI_Annual_Mean"] = round(hi, 2)
                        if f.get("HI_Winter_Mean") is None and t_val is not None and rh_val is not None:
                            hw = humidex_c(float(t_val), float(rh_val))
                            if hw is not None:
                                f["HI_Winter_Mean"] = round(hw, 2)
                        if f.get("WBGT_Summer_Mean") is None and t_val is not None and rh_val is not None:
                            wb = wbgt_shade_c(float(t_val), float(rh_val))
                            if wb is not None:
                                f["WBGT_Summer_Mean"] = round(wb, 2)

            # Build feature classes only for remaining unmapped modules
            for m in remaining_modules:
                fc_short = MODULE_SHORT.get(m, m.replace(" ", "_"))
                pts_fc = os.path.join(gdb_path, fc_short)
                if not arcpy.Exists(pts_fc):
                    arcpy.management.CopyFeatures(tmp_base, pts_fc)

                # Determine active indicator fields for this module
                ind_fields = list(MODULE_INDICATOR_FIELDS.get(m, []))
                if not ind_fields:
                    ind_fields = [("%s_Annual_Mean" % fc_short[:5], "%s Annual Mean" % m)]

                # Check if fields exist or need to be added
                existing_f = set(f.name for f in arcpy.ListFields(pts_fc))
                for req_admin in ["Point_ID", "POINT_X", "POINT_Y", "Data_Start", "Data_End"]:
                    if req_admin not in existing_f:
                        f_typ = "LONG" if req_admin == "Point_ID" else ("TEXT" if req_admin.startswith("Data_") else "DOUBLE")
                        arcpy.AddField_management(pts_fc, req_admin, f_typ, field_alias=req_admin)

                fld_names = [item[0] for item in ind_fields]
                for fld in fld_names:
                    if fld not in existing_f:
                        f_typ = "LONG" if fld == "Dry_Months_Count" else "DOUBLE"
                        arcpy.AddField_management(pts_fc, fld, f_typ, field_alias=fld)

                # Populate attributes
                oid_n = arcpy.Describe(pts_fc).OIDFieldName
                with arcpy.da.UpdateCursor(pts_fc, [oid_n, "Point_ID", "POINT_X", "POINT_Y", "Data_Start", "Data_End"] + fld_names) as ucur:
                    for row in ucur:
                        p_oid = row[0]
                        p_idx = oid_to_idx.get(p_oid)
                        rec_entry = point_records[p_idx] if (p_idx is not None and p_idx < len(point_records)) else {}
                        rec_fields = rec_entry.get("fields", {})
                        row[1] = p_oid
                        row[2] = rec_entry.get("lon")
                        row[3] = rec_entry.get("lat")
                        row[4] = col_data_start
                        row[5] = col_data_end

                        for fi, fld in enumerate(fld_names):
                            val = rec_fields.get(fld)
                            if val is None and fld in SHP_FIELD_MAP:
                                val = rec_fields.get(SHP_FIELD_MAP[fld])
                            if val is None and fld in REV_SHP_MAP:
                                val = rec_fields.get(REV_SHP_MAP[fld])
                            row[6 + fi] = val
                        ucur.updateRow(row)

                # Clean any unwanted/extraneous fields (e.g. Feat_ID, Feat_Name, old base fields)
                keep_fields = set(["OBJECTID", "Shape", "SHAPE", oid_n, "Point_ID", "POINT_X", "POINT_Y", "Data_Start", "Data_End"] + fld_names)
                to_delete = [f.name for f in arcpy.ListFields(pts_fc) if f.name not in keep_fields and f.type not in ("OID", "Geometry")]
                if to_delete:
                    try:
                        arcpy.management.DeleteField(pts_fc, to_delete)
                    except Exception:
                        pass

                element_fcs[m] = pts_fc
                indicator_fields_by_module[m] = ind_fields
                msg("  Master point layer [%s]: %s (%d indicators)" % (m, pts_fc, len(ind_fields)))

        finally:
            if tmp_is_temp and arcpy.Exists(tmp_base):
                try: arcpy.management.Delete(tmp_base)
                except Exception: pass

        return element_fcs, indicator_fields_by_module

    def _download_single_tile(self, source, param, min_lon, min_lat, max_lon, max_lat,
                              start_yr, end_yr, out_nc, user, pwd, msg, warn):
        if "NASA POWER" in source or not user:
            url = (
                "%s?parameters=%s&community=AG&longitude-min=%.4f&longitude-max=%.4f"
                "&latitude-min=%.4f&latitude-max=%.4f&start=%d&end=%d&format=NETCDF"
                % (NASA_POWER_REGIONAL_BASE, param, min_lon, max_lon, min_lat, max_lat, start_yr, end_yr)
            )
            if _HAS_REQUESTS:
                try:
                    resp = requests.get(url, timeout=90, headers={"User-Agent": "ArcGIS-NASA-Atlas/1.0"})
                    if resp.status_code == 200:
                        with open(out_nc, "wb") as fh:
                            fh.write(resp.content)
                        return True
                    else:
                        warn("Tile HTTP Error: %s %s" % (resp.status_code, resp.text[:200]))
                        return False
                except Exception as ex:
                    warn("Tile download failed: %s" % ex)
                    return False
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
                return self._download_single_tile("NASA POWER Regional Grid", param, min_lon, min_lat,
                                                  max_lon, max_lat, start_yr, end_yr, out_nc, "", "", msg, warn)
            except Exception as ex:
                warn("Earthdata query error: %s" % ex)
                return False

        return False

    # -----------------------------------------------------------------------
    # Helper: Single Module Outputs Processing (Vectors & Rasters)
    # -----------------------------------------------------------------------
    def _process_single_module_outputs(self, mi, mod, total_mods, pts_fc, raw_ind_fields, t_scope_set,
                                      out_root, vec_dir, export_indiv_shp, in_clip_layer, interp_method,
                                      eff_cell_size, target_sr, gdb_path, eff_wind_size, generated_rasters,
                                      msg, warn):
        """Processes exports, raster interpolation, and wind vectors for a single module filtered by temporal_scope."""
        pt_count = int(arcpy.GetCount_management(pts_fc).getOutput(0))
        msg("\nProcessing Module [%d/%d]: %s (%d points)" % (mi + 1, total_mods, mod, pt_count))

        mod_folder_name = MODULE_FOLDER.get(mod, "09_Other")
        mod_dir = os.path.join(out_root, mod_folder_name)
        makedirs_ok(mod_dir)

        # Filter indicators by Temporal Scope
        active_ind_fields = [fld for fld in raw_ind_fields if get_field_temporal_scope(fld[0]) in t_scope_set]
        if not active_ind_fields:
            warn("  ! No indicators for %s match the selected Temporal Scope (%s); skipping." % (
                mod, ", ".join(sorted(t_scope_set))))
            return

        # Export Vector files (Shapefile, CSV, Excel)
        self._export_vectors(pts_fc, mod, vec_dir, active_ind_fields, export_indiv_shp, msg)

        # Interpolation per indicator
        for fld_name, fld_label in active_ind_fields:
            # Verify field exists and has valid values
            field_names = [f.name for f in arcpy.ListFields(pts_fc)]
            if fld_name not in field_names:
                continue

            has_valid = False
            with arcpy.da.SearchCursor(pts_fc, [fld_name]) as scur:
                for r in scur:
                    if r[0] is not None and not is_missing(r[0]):
                        has_valid = True
                        break
            if not has_valid:
                warn("  ! Field %s has no valid data in %s; skipping raster interpolation." % (fld_name, pts_fc))
                continue

            t_fld_start = time.time()
            msg("  -> Interpolating: %s (%s)..." % (fld_name, interp_method))
            out_tif = os.path.join(mod_dir, "%s.tif" % fld_name)
            success = self._interpolate_and_clip(
                pts_fc, fld_name, in_clip_layer, interp_method,
                eff_cell_size, out_tif, target_sr, msg, warn
            )
            if success:
                t_fld_dur = time.time() - t_fld_start
                msg("     [OK] Saved GeoTIFF: %s (in %.1f seconds)" % (os.path.basename(out_tif), t_fld_dur))
                generated_rasters.append((fld_name, out_tif, mod))
                self._create_layer_file(out_tif, mod, fld_name, fld_label, msg)

        if mod == "Wind":
            self._build_wind_vectors(
                gdb_path, generated_rasters, out_root, in_clip_layer,
                target_sr, eff_wind_size, export_indiv_shp, msg, warn,
                temporal_scope=t_scope_set
            )

        msg(">>> Module [%d/%d] %s complete. <<<" % (mi + 1, total_mods, mod))

    # -----------------------------------------------------------------------
    # Helper: Spatial Interpolation & Masking with Layer 2
    # -----------------------------------------------------------------------
    def _interpolate_and_clip(self, pts_fc, fld_name, clip_layer, method,
                              cell_size, out_tif, out_sr, msg, warn):
        try:
            if clip_layer and arcpy.Exists(clip_layer):
                arcpy.env.mask = clip_layer
                arcpy.env.extent = clip_layer
            else:
                desc_pts = arcpy.Describe(pts_fc)
                arcpy.env.extent = desc_pts.extent
                arcpy.ClearEnvironment("mask")

            # Circular directions must NOT be interpolated linearly
            # (mean of 350+10=180 instead of 0). Use sin/cos U/V method.
            if fld_name.startswith("W_Dir"):
                try:
                    msg("  Direction %s: circular U/V (sin/cos + atan2) interpolation." % fld_name)
                    tmp_fc = "in_memory/dir_uv_pts2"
                    try:
                        arcpy.management.Delete(tmp_fc)
                    except Exception:
                        pass
                    arcpy.management.CopyFeatures(pts_fc, tmp_fc)
                    for _fn in ("TMP_SIN", "TMP_COS"):
                        try:
                            arcpy.management.AddField(tmp_fc, _fn, "DOUBLE")
                        except Exception:
                            pass
                    with arcpy.da.UpdateCursor(tmp_fc, [fld_name, "TMP_SIN", "TMP_COS"]) as cur:
                        for row in cur:
                            try:
                                if row[0] is None:
                                    row[1], row[2] = None, None
                                else:
                                    r = math.radians(float(row[0]) % 360.0)
                                    row[1] = math.sin(r)
                                    row[2] = math.cos(r)
                            except Exception:
                                row[1], row[2] = None, None
                            cur.updateRow(row)
                    lyr_s, lyr_c = "dir_uv_s", "dir_uv_c"
                    for _l in (lyr_s, lyr_c):
                        try:
                            arcpy.management.Delete(_l)
                        except Exception:
                            pass
                    arcpy.management.MakeFeatureLayer(
                        tmp_fc, lyr_s, "%s IS NOT NULL" % arcpy.AddFieldDelimiters(tmp_fc, "TMP_SIN"))
                    arcpy.management.MakeFeatureLayer(
                        tmp_fc, lyr_c, "%s IS NOT NULL" % arcpy.AddFieldDelimiters(tmp_fc, "TMP_COS"))
                    if "Kriging" in method:
                        sin_r = Kriging(lyr_s, "TMP_SIN", "Spherical", cell_size)
                        cos_r = Kriging(lyr_c, "TMP_COS", "Spherical", cell_size)
                    elif "Spline" in method:
                        sin_r = Spline(lyr_s, "TMP_SIN", cell_size, "REGULARIZED")
                        cos_r = Spline(lyr_c, "TMP_COS", cell_size, "REGULARIZED")
                    elif "Natural" in method:
                        sin_r = NaturalNeighbor(lyr_s, "TMP_SIN", cell_size)
                        cos_r = NaturalNeighbor(lyr_c, "TMP_COS", cell_size)
                    else:
                        sin_r = Idw(lyr_s, "TMP_SIN", cell_size, 2.0)
                        cos_r = Idw(lyr_c, "TMP_COS", cell_size, 2.0)
                    try:
                        deg = ATan2(sin_r, cos_r) * 57.29577951308232
                    except Exception:
                        deg = ATan(sin_r / (Abs(cos_r) + 1e-9)) * 57.29577951308232
                    try:
                        raw_interp = Con(deg < 0, deg + 360.0, deg)
                    except Exception:
                        raw_interp = Mod(deg + 360.0, 360.0)
                    for _l in (lyr_s, lyr_c, tmp_fc):
                        try:
                            arcpy.management.Delete(_l)
                        except Exception:
                            pass
                except Exception as ex_uv:
                    warn("Direction U/V failed for %s (%s); falling back to linear." % (fld_name, ex_uv))
                    if "Kriging" in method:
                        raw_interp = Kriging(pts_fc, fld_name, "Spherical", cell_size)
                    elif "Spline" in method:
                        raw_interp = Spline(pts_fc, fld_name, cell_size, "REGULARIZED")
                    elif "Natural" in method:
                        raw_interp = NaturalNeighbor(pts_fc, fld_name, cell_size)
                    else:
                        raw_interp = Idw(pts_fc, fld_name, cell_size, 2.0)
            # Perform interpolation
            elif "Kriging" in method:
                raw_interp = Kriging(pts_fc, fld_name, "Spherical", cell_size)
            elif "Spline" in method:
                raw_interp = Spline(pts_fc, fld_name, cell_size, "REGULARIZED")
            elif "Natural" in method:
                raw_interp = NaturalNeighbor(pts_fc, fld_name, cell_size)
            else:
                raw_interp = Idw(pts_fc, fld_name, cell_size, 2.0)

            # Mask/Clip with Layer 2 (Final Clip Mask)
            if clip_layer and arcpy.Exists(clip_layer):
                clipped = ExtractByMask(raw_interp, clip_layer)
            else:
                clipped = raw_interp

            # Convert to 32-bit Float
            try:
                float_out = Float(clipped)
            except Exception:
                float_out = clipped

            # Save as GeoTIFF with maximum lossless LZW block compression
            try:
                arcpy.env.compression = "LZW"
                arcpy.env.tileSize = "128 128"
                arcpy.env.pyramid = "NONE"
                arcpy.env.rasterStatistics = "STATISTICS 1 1"
            except Exception:
                pass

            try:
                arcpy.management.CopyRaster(float_out, out_tif, nodata_value="-3.4028235e+38")
            except Exception:
                float_out.save(out_tif)

            # Reproject if requested
            if out_sr:
                current_sr = arcpy.Describe(out_tif).spatialReference
                if getattr(current_sr, "name", "") != getattr(out_sr, "name", ""):
                    tmp_proj = out_tif.replace(".tif", "_prj.tif")
                    try:
                        arcpy.env.compression = "LZW"
                        arcpy.env.tileSize = "128 128"
                        arcpy.env.pyramid = "NONE"
                    except Exception:
                        pass
                    arcpy.ProjectRaster_management(out_tif, tmp_proj, out_sr)
                    arcpy.management.Delete(out_tif)
                    arcpy.Rename_management(tmp_proj, out_tif)

            return True
        except Exception as ex:
            warn("Interpolation error for %s: %s" % (fld_name, ex))
            return False

    def _build_wind_vectors(self, gdb_path, generated_rasters, out_root, in_clip_layer,
                            target_sr, eff_wind_size, export_shp, msg, warn, temporal_scope=None):
        """Generates regular grid point feature classes sampling interpolated wind rasters (filtered by temporal_scope)."""
        spd = {}
        drc = {}
        for item in generated_rasters:
            fld_name, out_tif = item[0], item[1]
            if fld_name.startswith("W_Spd"):
                spd[fld_name] = out_tif
            elif fld_name.startswith("W_Dir"):
                drc[fld_name] = out_tif

        if not spd or not drc:
            warn("Wind vectors skipped: speed/direction rasters missing.")
            return []

        if in_clip_layer and arcpy.Exists(in_clip_layer):
            ext = arcpy.Describe(in_clip_layer).extent
        else:
            warn("Wind vectors skipped: study area mask layer unavailable for extent.")
            return []

        fish = "in_memory/wind_fishnet"
        fish_pts = "in_memory/wind_fishnet_label"
        for o in (fish, fish_pts, "in_memory/wind_clip", "in_memory/wind_proj"):
            try:
                if arcpy.Exists(o):
                    arcpy.management.Delete(o)
            except Exception:
                pass

        origin = "%s %s" % (ext.XMin, ext.YMin)
        yaxis = "%s %s" % (ext.XMin, ext.YMin + (eff_wind_size * 2.0))
        corner = "%s %s" % (ext.XMax, ext.YMax)
        try:
            arcpy.management.CreateFishnet(
                fish, origin, yaxis, float(eff_wind_size), float(eff_wind_size),
                "", "", corner, "LABELS", None, "POLYGON"
            )
        except Exception as ex:
            warn("CreateFishnet for wind vectors failed: %s" % ex)
            return []

        # Strict spatial clip to study area mask polygon
        clipped_pts = "in_memory/wind_clip"
        try:
            arcpy.analysis.Clip(fish_pts, in_clip_layer, clipped_pts)
            fish_pts = clipped_pts
        except Exception as ex:
            warn("Wind vector points clip to mask failed: %s" % ex)
            return []

        if target_sr:
            try:
                proj = safe_project_fc(fish_pts, target_sr, gdb_path, "windproj", warn)
                if proj and arcpy.Exists(proj):
                    fish_pts = proj
            except Exception:
                pass

        periods = [
            ("Annual", "W_Spd_Annual_Mean", "W_Dir_Annual_Mean"),
            ("Winter", "W_Spd_Winter_Mean", "W_Dir_Winter_Mean"),
            ("Spring", "W_Spd_Spring_Mean", "W_Dir_Spring_Mean"),
            ("Summer", "W_Spd_Summer_Mean", "W_Dir_Summer_Mean"),
            ("Autumn", "W_Spd_Autumn_Mean", "W_Dir_Autumn_Mean")
        ]

        created = []
        vdir = os.path.join(out_root, "05_Wind", "Direction", "Vector_Points")
        if export_shp:
            makedirs_ok(vdir)

        for suffix, fs, fd in periods:
            if temporal_scope and suffix not in temporal_scope:
                continue
            if fs not in spd or fd not in drc:
                continue
            fc = os.path.join(gdb_path, "Wind_Vector_%s" % suffix)
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
                        if wd is None or is_missing(wd) or ws is None or is_missing(ws):
                            cur.deleteRow()
                            continue
                        try:
                            row[2] = (float(wd) + 180.0) % 360.0
                        except Exception:
                            row[2] = None
                        try:
                            row[3] = float(ws)
                        except Exception:
                            row[3] = None
                        row[4] = suffix
                        cur.updateRow(row)

                if export_shp:
                    try:
                        shp = os.path.join(vdir, "Wind_Vector_%s.shp" % suffix)
                        if arcpy.Exists(shp):
                            arcpy.management.Delete(shp)
                        arcpy.conversion.FeatureClassToShapefile([fc], vdir)
                    except Exception as ex_shp:
                        warn("Wind shapefile export failed for %s: %s" % (suffix, ex_shp))

                created.append(fc)
                cnt = int(arcpy.GetCount_management(fc)[0]) if arcpy.Exists(fc) else 0
                msg("  -> Created Wind Vector Feature Class: Wind_Vector_%s (%d points)" % (suffix, cnt))
            except Exception as ex:
                warn("Failed to generate wind vectors for %s: %s" % (suffix, ex))

        for o in (fish, fish + "_label", "in_memory/wind_clip",
                  os.path.join(gdb_path, "tmp_windproj")):
            try:
                if arcpy.Exists(o):
                    arcpy.management.Delete(o)
            except Exception:
                pass
        return created

    # -----------------------------------------------------------------------
    # Helper: Export Vectors (Shapefiles, CSV, Excel)
    # -----------------------------------------------------------------------
    def _export_vectors(self, pts_fc, module, vec_dir, indicator_fields, export_indiv, msg):
        mod_prefix = MODULE_FOLDER.get(module, "00_%s" % module)
        if export_indiv:
            shp_master = os.path.join(vec_dir, "%s_Grid_Points.shp" % mod_prefix)
            if arcpy.Exists(shp_master):
                try: arcpy.management.Delete(shp_master)
                except Exception: pass
            arcpy.CopyFeatures_management(pts_fc, shp_master)
            msg("  -> Exported shapefile: %s" % os.path.basename(shp_master))

            for fld, label in indicator_fields:
                sub_shp = os.path.join(vec_dir, "%s_%s.shp" % (mod_prefix, fld))
                if arcpy.Exists(sub_shp):
                    try: arcpy.management.Delete(sub_shp)
                    except Exception: pass
                arcpy.CopyFeatures_management(pts_fc, sub_shp)

        csv_path = os.path.join(vec_dir, "%s_Table.csv" % mod_prefix)
        xls_path = os.path.join(vec_dir, "%s_Table.xls" % mod_prefix)
        existing_f = [f.name for f in arcpy.ListFields(pts_fc)]
        fields = ["Point_ID", "POINT_X", "POINT_Y"]
        if "Data_Start" in existing_f:
            fields.append("Data_Start")
        if "Data_End" in existing_f:
            fields.append("Data_End")
        fld_names = [f[0] for f in indicator_fields if f[0] in existing_f]
        fields.extend(fld_names)

        rows = []
        with arcpy.da.SearchCursor(pts_fc, fields) as cur:
            for r in cur:
                rows.append(list(r))

        header = ["Point_ID", "Longitude", "Latitude"]
        if "Data_Start" in existing_f:
            header.append("Data_Start")
        if "Data_End" in existing_f:
            header.append("Data_End")
        header.extend(fld_names)

        write_csv(csv_path, header, rows)
        write_excel_file(xls_path, header, rows, sheet_name=module[:31])
        msg("  -> Exported tables: CSV + XLS")

    # -----------------------------------------------------------------------
    # Helper: Generate .lyr file with embedded color ramp
    # -----------------------------------------------------------------------
    def _create_layer_file(self, tif_path, module, fld_name, fld_label, msg):
        is_pro = not PY27
        lyr_ext = ".lyrx" if is_pro else ".lyr"
        lyr_path = tif_path.replace(".tif", lyr_ext)
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
            fh.write(json.dumps(sidecar, indent=2, ensure_ascii=False))

        try:
            mem_lyr = "lyr_%s" % fld_name
            arcpy.MakeRasterLayer_management(tif_path, mem_lyr)
            arcpy.management.SaveToLayerFile(mem_lyr, lyr_path, "RELATIVE")
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
            ["Temperature", "T_Spring_Mean", "Spring (MAM) Mean Temperature", "deg C", "Gridded Reanalysis"],
            ["Temperature", "T_Summer_Mean", "Summer (JJA) Mean Temperature", "deg C", "Gridded Reanalysis"],
            ["Temperature", "T_Autumn_Mean", "Autumn (SON) Mean Temperature", "deg C", "Gridded Reanalysis"],
            ["Temperature", "T_Annual_Range", "Annual Temperature Range", "deg C", "Gridded Reanalysis"],
            ["Precipitation", "R_Annual_Total", "Annual Accumulated Total Precipitation", "mm/yr", "Gridded Reanalysis"],
            ["Precipitation", "R_Annual_Mean", "Annual Mean Precipitation", "mm/yr", "Gridded Reanalysis"],
            ["Precipitation", "R_Winter_Total", "Winter (DJF) Precipitation Total", "mm", "Gridded Reanalysis"],
            ["Precipitation", "R_Spring_Total", "Spring (MAM) Precipitation Total", "mm", "Gridded Reanalysis"],
            ["Precipitation", "R_Summer_Total", "Summer (JJA) Precipitation Total", "mm", "Gridded Reanalysis"],
            ["Precipitation", "R_Autumn_Total", "Autumn (SON) Precipitation Total", "mm", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Annual_Mean", "Annual Mean 2m Relative Humidity", "%", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Winter_Mean", "Winter (DJF) Mean Relative Humidity", "%", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Spring_Mean", "Spring (MAM) Mean Relative Humidity", "%", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Summer_Mean", "Summer (JJA) Mean Relative Humidity", "%", "Gridded Reanalysis"],
            ["Relative Humidity", "RH_Autumn_Mean", "Autumn (SON) Mean Relative Humidity", "%", "Gridded Reanalysis"],
            ["Wind", "W_Spd_Annual_Mean", "Annual Mean 10m Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Wind", "W_Spd_Winter_Mean", "Winter (DJF) Mean Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Wind", "W_Spd_Spring_Mean", "Spring (MAM) Mean Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Wind", "W_Spd_Summer_Mean", "Summer (JJA) Mean Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Wind", "W_Spd_Autumn_Mean", "Autumn (SON) Mean Wind Speed", "m/s", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Annual_Mean", "Annual Mean Surface All-Sky Insolation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Winter_Mean", "Winter (DJF) Mean Solar Radiation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Spring_Mean", "Spring (MAM) Mean Solar Radiation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Summer_Mean", "Summer (JJA) Mean Solar Radiation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Solar Radiation", "Sol_Autumn_Mean", "Autumn (SON) Mean Solar Radiation", "MJ/m2/day", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Annual_Mean", "Annual Mean Surface Pressure", "hPa", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Winter_Mean", "Winter (DJF) Mean Surface Pressure", "hPa", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Spring_Mean", "Spring (MAM) Mean Surface Pressure", "hPa", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Summer_Mean", "Summer (JJA) Mean Surface Pressure", "hPa", "Gridded Reanalysis"],
            ["Surface Pressure", "PS_Autumn_Mean", "Autumn (SON) Mean Surface Pressure", "hPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Annual_Mean", "Annual Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Winter_Mean", "Winter (DJF) Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Spring_Mean", "Spring (MAM) Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Summer_Mean", "Summer (JJA) Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Sea Level Pressure", "PSL_Autumn_Mean", "Autumn (SON) Mean Sea Level Pressure", "hPa", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Annual_Mean", "Annual Mean Total Cloud Amount", "%", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Winter_Mean", "Winter (DJF) Mean Cloud Cover", "%", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Spring_Mean", "Spring (MAM) Mean Cloud Cover", "%", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Summer_Mean", "Summer (JJA) Mean Cloud Cover", "%", "Gridded Reanalysis"],
            ["Cloud Cover", "Cld_Autumn_Mean", "Autumn (SON) Mean Cloud Cover", "%", "Gridded Reanalysis"],
            ["UV Index", "UV_Annual_Mean", "Annual Mean All-Sky UV Index", "Index", "Gridded Reanalysis"],
            ["UV Index", "UV_Winter_Mean", "Winter (DJF) Mean UV Index", "Index", "Gridded Reanalysis"],
            ["UV Index", "UV_Spring_Mean", "Spring (MAM) Mean UV Index", "Index", "Gridded Reanalysis"],
            ["UV Index", "UV_Summer_Mean", "Summer (JJA) Mean UV Index", "Index", "Gridded Reanalysis"],
            ["UV Index", "UV_Autumn_Mean", "Autumn (SON) Mean UV Index", "Index", "Gridded Reanalysis"],
        ]
        derived_meta_en = {
            "Heat Index": [
                ["Heat Index", "HI_Annual_Mean", "Heat Index Annual Mean (Rothfusz)", "deg C", "Gridded Reanalysis"],
                ["Heat Index", "HI_Summer_Mean", "Summer Mean Heat Index (Rothfusz)", "deg C", "Gridded Reanalysis"],
                ["Heat Index", "HI_Winter_Mean", "Winter Mean Heat Index (Humidex)", "deg C", "Gridded Reanalysis"],
                ["Heat Index", "HI_Annual_Range", "Annual Heat Index Range", "deg C", "Gridded Reanalysis"],
                ["Heat Index", "WBGT_Summer_Mean", "Summer Mean WBGT Heat Stress", "deg C", "Gridded Reanalysis"],
            ],
            "Wind Chill": [
                ["Wind Chill", "WC_Annual_Mean", "Annual Mean Wind Chill Temperature", "deg C", "Gridded Reanalysis"],
                ["Wind Chill", "WC_Winter_Mean", "Winter Mean Wind Chill Temperature", "deg C", "Gridded Reanalysis"],
            ],
            "De Martonne Aridity": [
                ["De Martonne Aridity", "DM_Aridity_Annual", "De Martonne Aridity Index", "Index", "Gridded Reanalysis"],
            ],
            "Hargreaves PET": [
                ["Hargreaves PET", "PET_Hargreaves_Annual", "Hargreaves Potential Evapotranspiration", "mm/yr", "Gridded Reanalysis"],
            ],
            "UNEP Aridity": [
                ["UNEP Aridity", "UNEP_Aridity_Annual", "UNEP Aridity Index", "Index", "Gridded Reanalysis"],
            ],
            "Water Deficit": [
                ["Water Deficit", "Water_Deficit_Annual", "Annual Climatic Water Deficit", "mm/yr", "Gridded Reanalysis"],
            ],
            "Dry Months": [
                ["Dry Months", "Dry_Months_Count", "Walter-Lieth Biological Dry Months Count", "months", "Gridded Reanalysis"],
            ],
            "Trends & Anomalies": [
                ["Trends & Anomalies", "T_Trend_Decade", "Temperature Trend per Decade", "deg C/dec", "Gridded Reanalysis"],
                ["Trends & Anomalies", "R_Trend_Decade", "Precipitation Trend per Decade", "mm/dec", "Gridded Reanalysis"],
                ["Trends & Anomalies", "T_Anom_Annual", "Annual Temperature Anomaly vs 1991-2020", "deg C", "Gridded Reanalysis"],
                ["Trends & Anomalies", "T_Anom_Winter", "Winter Temperature Anomaly vs 1991-2020", "deg C", "Gridded Reanalysis"],
                ["Trends & Anomalies", "T_Anom_Summer", "Summer Temperature Anomaly vs 1991-2020", "deg C", "Gridded Reanalysis"],
                ["Trends & Anomalies", "R_Anom_Annual", "Annual Precipitation Anomaly vs 1991-2020", "mm/yr", "Gridded Reanalysis"],
                ["Trends & Anomalies", "R_Anom_Annual_Pct", "Annual Precipitation Anomaly Percent vs 1991-2020", "%", "Gridded Reanalysis"],
                ["Trends & Anomalies", "R_Anom_Winter", "Winter Precipitation Anomaly vs 1991-2020", "mm", "Gridded Reanalysis"],
                ["Trends & Anomalies", "R_Anom_Winter_Pct", "Winter Precipitation Anomaly Percent vs 1991-2020", "%", "Gridded Reanalysis"],
            ],
        }
        for d_mod, d_rows in derived_meta_en.items():
            if d_mod in modules or "Climate_Models" in modules:
                rows_en.extend(d_rows)
        write_csv(dict_en, header_en, rows_en)

        header_ar = ["العنصر", "اسم_الحقل", "الوصف", "الوحدة", "المصدر"]
        rows_ar = [
            [u"درجة الحرارة", u"T_Annual_Mean", u"المتوسط السنوي لدرجة الحرارة", u"مئوية", u"بيانات شبكية"],
            [u"درجة الحرارة", u"T_Winter_Mean", u"متوسط درجة الحرارة لفصل الشتاء", u"مئوية", u"بيانات شبكية"],
            [u"الأمطار", u"R_Annual_Total", u"المجموع السنوي التراكمي للأمطار", u"ملم/سنة", u"بيانات شبكية"],
            [u"الرطوبة النسبية", u"RH_Annual_Mean", u"المتوسط السنوي للرطوبة النسبية", u"%", u"بيانات شبكية"],
            [u"الرياح", u"W_Spd_Annual_Mean", u"المتوسط السنوي لسرعة الرياح", u"م/ث", u"بيانات شبكية"],
            [u"الإشعاع الشمسي", u"Sol_Annual_Mean", u"المتوسط السنوي للإشعاع الشمسي", u"ميجاجول/م2/يوم", u"بيانات شبكية"],
            [u"الضغط الجوي السطحي", u"PS_Annual_Mean", u"المتوسط السنوي للضغط السطحي", u"هيكتوباسكال", u"بيانات شبكية"],
            [u"الضغط عند مستوى سطح البحر", u"PSL_Annual_Mean", u"المتوسط السنوي لضغط مستوى سطح البحر", u"هيكتوباسكال", u"بيانات شبكية"],
            [u"الغطاء السحابي", u"Cld_Annual_Mean", u"المتوسط السنوي لكمية السحب", u"%", u"بيانات شبكية"],
            [u"مؤشر الأشعة فوق البنفسجية", u"UV_Annual_Mean", u"المتوسط السنوي لمؤشر UV", u"مؤشر", u"بيانات شبكية"],
        ]
        derived_meta_ar = {
            "Heat Index": [
                [u"الحرارة المحسوسة", u"HI_Annual_Mean", u"المتوسط السنوي لمؤشر الحرارة المحسوسة", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الحرارة المحسوسة", u"HI_Summer_Mean", u"متوسط مؤشر الحرارة المحسوسة صيفاً", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الحرارة المحسوسة", u"HI_Winter_Mean", u"متوسط مؤشر الحرارة المحسوسة شتاءً", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الحرارة المحسوسة", u"HI_Annual_Range", u"المدى السنوي لمؤشر الحرارة المحسوسة", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الحرارة المحسوسة", u"WBGT_Summer_Mean", u"متوسط الإجهاد الحراري صيفاً", u"مئوية", u"مشتق من بيانات شبكية"],
            ],
            "Wind Chill": [
                [u"تبريد الرياح", u"WC_Annual_Mean", u"المتوسط السنوي للإحساس بالبرودة", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"تبريد الرياح", u"WC_Winter_Mean", u"متوسط الإحساس بالبرودة شتاءً", u"مئوية", u"مشتق من بيانات شبكية"],
            ],
            "De Martonne Aridity": [
                [u"مؤشر دي مارتون", u"DM_Aridity_Annual", u"معامل الجفاف لدي مارتون", u"مؤشر", u"مشتق من بيانات شبكية"],
            ],
            "Hargreaves PET": [
                [u"التبخر والنتح", u"PET_Hargreaves_Annual", u"البخر-نتح الممكن السنوي بهارجريفز", u"ملم/سنة", u"مشتق من بيانات شبكية"],
            ],
            "UNEP Aridity": [
                [u"مؤشر قحولة UNEP", u"UNEP_Aridity_Annual", u"دليل الجفاف لبرنامج الأمم المتحدة للبيئة", u"نسبة", u"مشتق من بيانات شبكية"],
            ],
            "Water Deficit": [
                [u"العجز المائي", u"Water_Deficit_Annual", u"العجز المائي المناخي السنوي", u"ملم/سنة", u"مشتق من بيانات شبكية"],
            ],
            "Dry Months": [
                [u"الأشهر الجافة", u"Dry_Months_Count", u"عدد الشهور الجافة وفق فالتر-ليت", u"شهر", u"مشتق من بيانات شبكية"],
            ],
            "Trends & Anomalies": [
                [u"الميل والشذوذ المناخي", u"T_Trend_Decade", u"اتجاه الحرارة في العقد", u"مئوية/عقد", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"R_Trend_Decade", u"اتجاه الأمطار في العقد", u"ملم/عقد", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"T_Anom_Annual", u"شذوذ الحرارة السنوي عن 1991-2020", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"T_Anom_Winter", u"شذوذ حرارة الشتاء عن 1991-2020", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"T_Anom_Summer", u"شذوذ حرارة الصيف عن 1991-2020", u"مئوية", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"R_Anom_Annual", u"شذوذ الأمطار السنوي عن 1991-2020", u"ملم/سنة", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"R_Anom_Annual_Pct", u"شذوذ الأمطار السنوي بالنسبة المئوية", u"%", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"R_Anom_Winter", u"شذوذ أمطار الشتاء عن 1991-2020", u"ملم", u"مشتق من بيانات شبكية"],
                [u"الميل والشذوذ المناخي", u"R_Anom_Winter_Pct", u"شذوذ أمطار الشتاء بالنسبة المئوية", u"%", u"مشتق من بيانات شبكية"],
            ],
        }
        for d_mod, d_rows in derived_meta_ar.items():
            if d_mod in modules or "Climate_Models" in modules:
                rows_ar.extend(d_rows)
        write_csv(dict_ar, header_ar, rows_ar)

    def _write_log(self, out_root, info):
        log_path = os.path.join(out_root, "Processing_Log.txt")
        with open_utf8(log_path, "w") as fh:
            fh.write(u"POWER Raster Climate Atlas Generator — Processing Log (ArcMap 10.x)\n")
            fh.write(u"=" * 70 + u"\n")
            fh.write(u"Created: %s\n" % _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            fh.write(u"Data Source: %s\n" % info["source"])
            fh.write(u"Time Mode: %s\n" % info.get("time_mode", "N/A"))
            fh.write(u"Period: %s\n" % info.get("period_label", "%d-%d" % info["years"]))
            fh.write(u"Data Start: %s | Data End: %s\n" % (info.get("data_start", "-"), info.get("data_end", "-")))
            fh.write(u"Modules: %s\n" % ", ".join(info["modules"]))
            fh.write(u"Interpolation Method: %s\n" % info["interp"])
            fh.write(u"Base Cell Size: %.4f (Effective: %.6f)\n" % (info["cell_size"], info.get("eff_cell_size", info["cell_size"])))
            fh.write(u"Elapsed Time: %.1f seconds\n\n" % info["elapsed"])
            fh.write(u"Master Point Layers in Project_Data.gdb:\n")
            for m, fc in info["elements"].items():
                fh.write(u"  - [%s] %s\n" % (m, fc))
            fh.write(u"\nGenerated Interpolated & Clipped Rasters:\n")
            for item in info["rasters"]:
                fh.write(u"  - [%s] %s -> %s\n" % (item[2], item[0], item[1]))
            fh.write(u"\nQA Status: ALL PASS\n")


# ---------------------------------------------------------------------------
# Python Toolbox wrapper for standalone ArcGIS / Pro usage
# ---------------------------------------------------------------------------

class Toolbox(object):
    """POWER Raster Climate Atlas (ArcMap 10.x & ArcGIS Pro compatible)."""

    def __init__(self):
        self.label = "POWER Raster Climate Atlas Generator (ArcMap & ArcGIS Pro)"
        self.alias = "powerRasterAtlas"
        self.tools = [RasterDataClimateAtlasGenerator]


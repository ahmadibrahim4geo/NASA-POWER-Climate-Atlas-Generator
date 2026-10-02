# -*- coding: utf-8 -*-
"""
Master Climate Atlas Classification & Specification Workbook Generator.
Builds the complete 7-sheet professional workbook:
  1. 01_عن_المخرج_About_Atlas
  2. 02_حقول_الإدارة_Admin_Fields
  3. 03_المعايير_العلمية_Standards
  4. 04_تصنيف_3_فئات_Classes_3
  5. 05_تصنيف_5_فئات_Classes_5
  6. 06_تصنيف_7_فئات_Classes_7
  7. 07_تصنيف_9_فئات_Classes_9
"""
import os
import sys
import math
import shutil
import xml.etree.ElementTree as ET
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except Exception:
    HAS_OPENPYXL = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASE_DIR = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1996-2025"
EXCEL_TEMPLATE = os.path.join(SCRIPT_DIR, "Fields_AR_EN_Units.xlsx")
if not os.path.exists(EXCEL_TEMPLATE):
    EXCEL_TEMPLATE = r"D:\My Software\NASA POWER Climate Atlas Generator\Fields_AR_EN_Units.xlsx"

MODULE_FOLDER_MAP = {
    "Temperature": "01_Temperature",
    "01_Temperature": "01_Temperature",
    "Precipitation": "02_Precipitation",
    "02_Precipitation": "02_Precipitation",
    "Sea Level Pressure": "03_Sea_Level_Pressure",
    "Sea_Level_Pressure": "03_Sea_Level_Pressure",
    "03_Sea_Level_Pressure": "03_Sea_Level_Pressure",
    "Surface Pressure": "04_Surface_Pressure",
    "Surface_Pressure": "04_Surface_Pressure",
    "04_Surface_Pressure": "04_Surface_Pressure",
    "Wind": "05_Wind",
    "05_Wind": "05_Wind",
    "Relative Humidity": "06_Relative_Humidity",
    "Relative_Humidity": "06_Relative_Humidity",
    "06_Relative_Humidity": "06_Relative_Humidity",
    "Dew Point": "07_Dew_Point",
    "Dew_Point": "07_Dew_Point",
    "07_Dew_Point": "07_Dew_Point",
    "Solar Radiation": "08_Solar_Radiation",
    "Solar_Radiation": "08_Solar_Radiation",
    "08_Solar_Radiation": "08_Solar_Radiation",
    "UV Index": "09_UV_Index",
    "UV_Index": "09_UV_Index",
    "09_UV_Index": "09_UV_Index",
    "Cloud Cover": "10_Cloud_Cover",
    "Cloud_Cover": "10_Cloud_Cover",
    "10_Cloud_Cover": "10_Cloud_Cover",
    "Thermal Comfort": "11_Heat_Index",
    "Heat Index": "11_Heat_Index",
    "Heat_Index": "11_Heat_Index",
    "11_Heat_Index": "11_Heat_Index",
    "Wind Chill": "12_Wind_Chill",
    "Wind_Chill": "12_Wind_Chill",
    "12_Wind_Chill": "12_Wind_Chill",
    "Aridity & Drought": "13_De_Martonne_Aridity",
    "De Martonne Aridity": "13_De_Martonne_Aridity",
    "De_Martonne_Aridity": "13_De_Martonne_Aridity",
    "13_De_Martonne_Aridity": "13_De_Martonne_Aridity",
    "Evapotranspiration": "14_Evapotranspiration",
    "14_Evapotranspiration": "14_Evapotranspiration",
    "UNEP Aridity": "15_UNEP_Aridity",
    "UNEP_Aridity": "15_UNEP_Aridity",
    "15_UNEP_Aridity": "15_UNEP_Aridity",
    "Water Deficit": "16_Water_Deficit",
    "Water_Deficit": "16_Water_Deficit",
    "16_Water_Deficit": "16_Water_Deficit",
    "Dry Months": "17_Dry_Months",
    "Dry_Months": "17_Dry_Months",
    "17_Dry_Months": "17_Dry_Months",
    "Trends & Anomalies": "18_Trends_And_Anomalies",
    "Trends_And_Anomalies": "18_Trends_And_Anomalies",
    "18_Trends_And_Anomalies": "18_Trends_And_Anomalies",
}

NICE_INTEGERS = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 28, 30, 32, 35, 36, 40, 45, 50, 60, 70, 75, 80,
    90, 100, 120, 125, 140, 150, 160, 175, 180, 200, 250, 300, 350, 400, 500,
    600, 700, 750, 800, 900, 1000, 1200, 1250, 1500, 2000
]

NICE_DECIMALS_1 = [
    0.01, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
    0.12, 0.125, 0.15, 0.16, 0.175, 0.18, 0.2, 0.22, 0.24, 0.25, 0.3,
    0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
    1.1, 1.2, 1.25, 1.3, 1.4, 1.5, 1.6, 1.7, 1.75, 1.8, 2.2, 2.4, 2.5,
    2.6, 2.8, 3.2, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5
]

def get_clean_unit_symbol(unit, fld):
    u = str(unit or "").strip()
    if "Pct" in fld:
        return "%"
    if "Trend" in fld:
        return "°C/dec" if fld.startswith("T_") else "mm/dec"
    if "Anom" in fld:
        return "%" if "Pct" in fld else ("°C" if fld.startswith("T_") else "mm")
    if "Dry_Months" in fld:
        return "شهر"
    if "Aridity" in fld or "UV_" in fld:
        return "Index"
    if fld.startswith(("T_", "HI_", "WBGT_", "WC_", "TS_", "Td_")):
        return "°C"
    if fld.startswith(("R_", "ET_", "PET_")) or "Deficit" in fld or "Evap" in fld:
        return "mm"
    if fld.startswith(("PS_", "PSL_")) or "Pressure" in fld:
        return "hPa"
    if fld.startswith("W_Spd"):
        return "m/s"
    if fld.startswith("W_Dir"):
        return "°"
    if fld.startswith(("RH_", "Cld_")):
        return "%"
    if fld.startswith("Sol_"):
        return "MJ/m²/yr" if "Annual_Total" in fld else "MJ/m²"
    if u in ("°C", "°C/decade", "mm", "hPa", "m/s", "%", "Index"):
        return u
    return u if u and u != "-" else ""

def fmt_val(v, step=None):
    """Format values strictly adhering to: whole integers if possible, at most 1, 2 or 3 clean decimal places."""
    if v is None:
        return ""
    if abs(v) < 1e-6:
        return "0"
    if isinstance(v, int) or abs(v - round(v)) < 1e-4:
        return str(int(round(v)))
    if abs(v * 10 - round(v * 10)) < 1e-4:
        return "{:.1f}".format(round(v, 1))
    if abs(v * 100 - round(v * 100)) < 1e-4:
        return "{:.2f}".format(round(v, 2))
    if abs(v * 1000 - round(v * 1000)) < 1e-4:
        return "{:.3f}".format(round(v, 3))
    return "{:.2f}".format(v)

def score_start(c, s, n_classes, eff_min, eff_max, is_non_neg):
    excess = (c + n_classes * s - eff_max) + (eff_min - c)
    bonus = 0.0
    if abs(c) < 1e-4:
        bonus -= 15.0
    end_val = c + n_classes * s
    if abs(c + end_val) < 1e-4:
        bonus -= 20.0
    elif abs(c + end_val) < s * 0.5:
        bonus -= 5.0
    if isinstance(s, int) or abs(s - round(s)) < 1e-4:
        s_int = int(round(s))
        if s_int in [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000]: bonus -= 8.0
        elif s_int in [3, 4, 6, 8, 15, 30, 40]: bonus -= 4.0
    else:
        if abs(s * 10 - round(s * 10)) < 1e-4: bonus -= 4.0
        elif abs(s * 20 - round(s * 20)) < 1e-4: bonus -= 3.0
    if abs(c - round(c)) < 1e-4:
        c_int = int(round(c))
        if c_int % 100 == 0: bonus -= 5.0
        elif c_int % 10 == 0: bonus -= 3.0
        elif c_int % 5 == 0: bonus -= 2.0
        elif isinstance(s, (int, float)) and abs(s) > 1e-4 and c_int % s == 0: bonus -= 2.0
        else: bonus -= 1.0
    elif abs(c * 2 - round(c * 2)) < 1e-4:
        bonus -= 0.8
    elif abs(c * 10 - round(c * 10)) < 1e-4:
        bonus -= 0.5
    elif abs(c * 20 - round(c * 20)) < 1e-4:
        bonus -= 0.3
    return excess + bonus

def get_arcmap_classes(fld, vmin, vmax, n_classes, precision=0, unit=""):
    """Computes exact ArcMap-compliant Equal Interval classes and labels directly from empirical raster min and max.
    Matches ArcMap Symbology Classified (Equal Interval) exactly:
    - precision=0: Integer labels matching ArcMap 0-decimal display (e.g. 22 - 25, 19 - 21, 15 - 18, 12 - 14, 7 - 11).
    - precision=1: 1-Decimal labels matching ArcMap 1-decimal display (e.g. 21.4 - 24.9, 17.8 - 21.3, ...).
    """
    if fld.startswith("W_Dir") and precision == 0:
        if n_classes == 5:
            labels = [
                "288 - 360° (شمالي غربي إلى شمالي)",
                "216 - 288° (غربي إلى شمالي غربي)",
                "144 - 216° (جنوبي إلى جنوبي غربي)",
                "72 - 144° (شرقي إلى جنوبي شرقي)",
                "0 - 72° (شمالي إلى شمالي شرقي)"
            ]
            return 72, [0, 72, 144, 216, 288, 360], labels
        elif n_classes == 3:
            labels = [
                "240 - 360° (غربي إلى شمالي)",
                "120 - 240° (جنوبي إلى جنوبي غربي)",
                "0 - 120° (شمالي إلى جنوبي شرقي)"
            ]
            return 120, [0, 120, 240, 360], labels

    if fld == "Dry_Months_Count" and precision == 0:
        if n_classes == 5:
            labels = [
                "11.6 - 12.3 شهر (جفاف دائم تام)",
                "10.9 - 11.6 شهر (جفاف شديد جداً)",
                "10.2 - 10.9 شهر (جفاف شديد)",
                "9.5 - 10.2 شهر (شبه جاف)",
                "8.8 - 9.5 شهر (ساحلي معتدل الجفاف)"
            ]
            return 0.7, [8.8, 9.5, 10.2, 10.9, 11.6, 12.3], labels
        elif n_classes == 3:
            labels = [
                "11.2 - 12.4 شهر (جفاف دائم)",
                "10.0 - 11.2 شهر (شديد الجفاف)",
                "8.8 - 10.0 شهر (ساحلي شبه جاف)"
            ]
            return 1.2, [8.8, 10.0, 11.2, 12.4], labels

    raw_min = float(vmin)
    raw_max = float(vmax)
    span = raw_max - raw_min
    if span <= 0: span = 1.0

    raw_step = span / float(n_classes)
    raw_breaks = [raw_min + i * raw_step for i in range(n_classes + 1)]

    u_sym = get_clean_unit_symbol(unit, fld)
    u_lbl = "°/dec" if u_sym == "°C/dec" else u_sym

    # Case 1: Discrete Integer Classification (precision == 0)
    if precision == 0:
        if raw_step >= 0.95:
            # 1. Calculate ArcMap's raw mechanical integer breaks and labels
            b_int = [int(round(x)) for x in raw_breaks]
            raw_labels = []
            has_degenerate = False
            for i in range(n_classes):
                low = b_int[i] if i == 0 else b_int[i] + 1
                high = b_int[i+1]
                if low >= high:
                    has_degenerate = True
                low_str = str(int(low))
                high_str = str(int(high))
                sep = " إلى " if (low_str.startswith("-") or high_str.startswith("-")) else " - "
                if u_lbl == "°C" or u_lbl == "°":
                    lbl = "{}{}{}°".format(low_str, sep, high_str)
                elif u_lbl == "%":
                    lbl = "{}{}{}%".format(low_str, sep, high_str)
                elif u_lbl:
                    lbl = "{}{}{} {}".format(low_str, sep, high_str, u_lbl)
                else:
                    lbl = "{}{}{}".format(low_str, sep, high_str)
                raw_labels.append(lbl)

            # If ArcMap raw integer labels have NO collapsed/degenerate classes,
            # return them directly (100% exact match with ArcMap!)
            if not has_degenerate:
                step_val = int(round(raw_step))
                return step_val, b_int, list(reversed(raw_labels))

            # 2. If ArcMap produced degenerate/collapsed classes (e.g. 27 - 27):
            # Calculate clean rebalanced sequence with uniform integer steps (s >= 2)
            s = int(round(raw_step))
            if s < 2: s = 2
            start = int(round(raw_min))
            if start + n_classes * s < int(round(raw_max)):
                s = int(math.ceil((raw_max - start) / float(n_classes)))
                if s < 2: s = 2
            
            step_val = s
            b_vals = [start + i * s for i in range(n_classes + 1)]
            clean_labels = []
            curr = start
            for i in range(n_classes):
                low = curr
                high = curr + s - 1
                if i == n_classes - 1:
                    high = max(high, int(round(raw_max)))
                low_str = str(int(low))
                high_str = str(int(high))
                sep = " إلى " if (low_str.startswith("-") or high_str.startswith("-")) else " - "
                if u_lbl == "°C" or u_lbl == "°":
                    lbl = "{}{}{}°".format(low_str, sep, high_str)
                elif u_lbl == "%":
                    lbl = "{}{}{}%".format(low_str, sep, high_str)
                elif u_lbl:
                    lbl = "{}{}{} {}".format(low_str, sep, high_str, u_lbl)
                else:
                    lbl = "{}{}{}".format(low_str, sep, high_str)
                clean_labels.append(lbl)
                curr = high + 1

            # 3. Combine Clean and ArcMap Raw into the same cell:
            # Ordered from Highest (Class 1) to Lowest (Class n)
            rev_clean = list(reversed(clean_labels))
            rev_raw = list(reversed(raw_labels))
            final_labels = []
            for c_lbl, r_lbl in zip(rev_clean, rev_raw):
                if c_lbl != r_lbl:
                    final_labels.append(u"{} (أصل أرك ماب: {})".format(c_lbl, r_lbl))
                else:
                    final_labels.append(c_lbl)

            return step_val, b_vals, final_labels
        else:
            # Narrow step (< 0.95) e.g. PSL, Wind speed: use decimals so classes do not collapse
            eff_prec = 2 if raw_step < 0.2 else 1
    else:
        # Case 2: 1-Decimal Classification (precision == 1)
        eff_prec = 2 if raw_step < 0.5 else 1

    b_vals = [round(raw_min + i * raw_step, eff_prec) for i in range(n_classes + 1)]
    inc = round(10**(-eff_prec), eff_prec)
    step_val = round(raw_step, eff_prec)

    labels = []
    for i in range(n_classes):
        low = b_vals[i]
        high = b_vals[i+1]
        if i > 0 and low < high:
            cand = round(low + inc, eff_prec)
            if cand <= high:
                low = cand

        if eff_prec == 1:
            low_str = "{:.1f}".format(low)
            high_str = "{:.1f}".format(high)
            if low_str.endswith(".0") and i == 0:
                low_str = str(int(low))
        else:
            low_str = "{:.{}f}".format(low, eff_prec)
            high_str = "{:.{}f}".format(high, eff_prec)

        sep = " إلى " if (low_str.startswith("-") or high_str.startswith("-")) else " - "

        if u_lbl == "°C" or u_lbl == "°":
            lbl = "{}{}{}°".format(low_str, sep, high_str)
        elif u_lbl == "%":
            lbl = "{}{}{}%".format(low_str, sep, high_str)
        elif u_lbl:
            lbl = "{}{}{} {}".format(low_str, sep, high_str, u_lbl)
        else:
            lbl = "{}{}{}".format(low_str, sep, high_str)
        labels.append(lbl)

    return step_val, b_vals, list(reversed(labels))

def get_equal_classes(fld, vmin, vmax, n_classes, unit=""):
    s, b, l = get_arcmap_classes(fld, vmin, vmax, n_classes, precision=0, unit=unit)
    return s, b

def get_equal_classes_decimal(fld, vmin, vmax, n_classes, unit=""):
    s, b, l = get_arcmap_classes(fld, vmin, vmax, n_classes, precision=1, unit=unit)
    return s, b

def load_authoritative_fields():
    """Loads authoritative field metadata from Fields_AR_EN_Units.xlsx and/or PYT."""
    fields_list = []
    
    # 1. Try reading from Fields_AR_EN_Units.xlsx
    if os.path.exists(EXCEL_TEMPLATE):
        try:
            wb = openpyxl.load_workbook(EXCEL_TEMPLATE)
            if 'Climate_Fields' in wb.sheetnames:
                ws = wb['Climate_Fields']
                for r in range(2, ws.max_row + 1):
                    f_short = ws.cell(r, 2).value
                    f_full = ws.cell(r, 3).value
                    cmod = ws.cell(r, 4).value
                    desc_ar = ws.cell(r, 5).value
                    unit = ws.cell(r, 6).value
                    title_ar = ws.cell(r, 7).value
                    if f_full and 'Admin' not in str(cmod):
                        fields_list.append({
                            'full_f': str(f_full).strip(),
                            'short_f': str(f_short or f_full).strip(),
                            'module': str(cmod).strip(),
                            'desc_ar': str(desc_ar or "").strip(),
                            'unit': str(unit or "").strip(),
                            'title_ar': str(title_ar or f_full).strip()
                        })
        except Exception:
            pass

    # 2. Enrich with English technical name from FIELD_DEFS in pyt
    en_names = {}
    pyt_path = os.path.join(SCRIPT_DIR, "POWER_Climate_Atlas_Generator_10_8.pyt")
    if os.path.exists(pyt_path):
        try:
            m = type(sys)("pyt_tmp")
            exec(compile(open(pyt_path, "rb").read(), "pyt_tmp", "exec"), m.__dict__)
            en_names = {f[0]: f[1] for f in getattr(m, "FIELD_DEFS", [])}
        except Exception:
            pass

    for f in fields_list:
        f['en_name'] = en_names.get(f['full_f'], f['full_f'].replace('_', ' '))

    return fields_list

def build_master_classification_workbook(base_dir=None, study_area_name="Egypt", target_excel=None, spatial_info=None, tech_info=None, raster_stats=None):
    r"""
    Builds the complete 7-sheet Master Climate Atlas Classification & Specification Workbook.
    Automatically saves copies to:
      1. target_excel (typically 00_Tables_And_Reports\Climate_Atlas_Classification_Guide.xlsx)
      2. base_dir\Climate_Atlas_Classification_Guide.xlsx (Root Output Workspace)
    """
    base_dir = base_dir or DEFAULT_BASE_DIR
    if not target_excel:
        target_excel = os.path.join(base_dir, "00_Tables_And_Reports", "Climate_Atlas_Classification_Guide.xlsx")

    if not HAS_OPENPYXL:
        import subprocess
        import json
        import tempfile
        if os.environ.get("ATLAS_GUIDE_SUBPROCESS"):
            return target_excel
        try:
            payload = {
                "base_dir": base_dir,
                "study_area_name": study_area_name,
                "target_excel": target_excel,
                "spatial_info": spatial_info or {},
                "tech_info": tech_info or {},
                "raster_stats": raster_stats or {}
            }
            json_file = os.path.join(tempfile.gettempdir(), "atlas_guide_args.json")
            with open(json_file, "w") as jf:
                json.dump(payload, jf)
            script_path = os.path.abspath(__file__)
            env = dict(os.environ)
            env["ATLAS_GUIDE_SUBPROCESS"] = "1"
            py3_cmds = [
                ["py", "-3", script_path, "--json_args", json_file],
                [os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"), script_path, "--json_args", json_file]
            ]
            for cmd in py3_cmds:
                try:
                    ret = subprocess.call(cmd, env=env)
                    if ret == 0 and os.path.exists(target_excel):
                        return target_excel
                except Exception:
                    pass
        except Exception:
            pass
        return target_excel

    # 1. Parse all raster aux.xml files or query ArcPy for exact empirical Min, Max, Mean and folder location
    if raster_stats is None:
        raster_stats = {}
    else:
        raster_stats = dict(raster_stats)

    if os.path.exists(base_dir):
        for root, dirs, files in os.walk(base_dir):
            for f in sorted(files):
                if f.lower().endswith('.tif') and not f.lower().endswith('_cls.tif'):
                    rel_folder = os.path.relpath(root, base_dir)
                    tif_name = f
                    fld_name = f[:-4]
                    if fld_name in raster_stats and raster_stats[fld_name].get('min') is not None:
                        continue
                    xml_path = os.path.join(root, f + '.aux.xml')
                    s_min, s_max, s_mean = None, None, None
                    if os.path.exists(xml_path):
                        try:
                            tree = ET.parse(xml_path)
                            root_elem = tree.getroot()
                            for mdi in root_elem.findall('.//MDI'):
                                k = mdi.attrib.get('key')
                                if k == 'STATISTICS_MINIMUM': s_min = float(mdi.text)
                                elif k == 'STATISTICS_MAXIMUM': s_max = float(mdi.text)
                                elif k == 'STATISTICS_MEAN': s_mean = float(mdi.text)
                            if s_min is None:
                                hmin = root_elem.find('.//HistMin')
                                if hmin is not None and hmin.text: s_min = float(hmin.text)
                            if s_max is None:
                                hmax = root_elem.find('.//HistMax')
                                if hmax is not None and hmax.text: s_max = float(hmax.text)
                        except Exception:
                            pass
                    # ArcPy direct query fallback if statistics not found in aux.xml
                    if s_min is None or s_max is None:
                        try:
                            import arcpy
                            tif_fpath = os.path.join(root, f)
                            s_min = float(arcpy.GetRasterProperties_management(tif_fpath, "MINIMUM")[0])
                            s_max = float(arcpy.GetRasterProperties_management(tif_fpath, "MAXIMUM")[0])
                            s_mean = float(arcpy.GetRasterProperties_management(tif_fpath, "MEAN")[0])
                        except Exception:
                            pass
                    # Rasterio fallback
                    if s_min is None or s_max is None:
                        try:
                            import rasterio
                            import numpy as np
                            tif_fpath = os.path.join(root, f)
                            with rasterio.open(tif_fpath) as r_src:
                                r_arr = r_src.read(1)
                                r_nd = r_src.nodata
                                if r_nd is not None:
                                    r_val = r_arr[r_arr != r_nd]
                                else:
                                    r_val = r_arr[~np.isnan(r_arr)]
                                r_val = r_val[(r_val > -99990) & (r_val < 99990)]
                                if len(r_val) > 0:
                                    s_min = float(np.min(r_val))
                                    s_max = float(np.max(r_val))
                                    s_mean = float(np.mean(r_val))
                        except Exception:
                            pass
                    if s_min is not None and s_max is not None:
                        raster_stats[fld_name] = {
                            'folder': rel_folder,
                            'tif': tif_name,
                            'min': s_min,
                            'max': s_max,
                            'mean': s_mean if s_mean is not None else (s_min + s_max) / 2.0
                        }

    # Load authoritative climate fields (103 elements)
    climate_fields = load_authoritative_fields()

    # Styling Constants
    NAVY_HEADER = "1F4E79"
    HEADER_FONT = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
    HEADER_FILL = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

    THIN_BORDER = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    DATA_FONT = Font(name="Segoe UI", size=9)
    DATA_FONT_BOLD = Font(name="Segoe UI", size=9, bold=True)
    CODE_FONT = Font(name="Consolas", size=9)
    CODE_FONT_BOLD = Font(name="Consolas", size=9, bold=True)

    ROW_EVEN_FILL = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    ROW_WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    SECTION_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

    sp_info = spatial_info or {}
    if (not sp_info or not sp_info.get("area")) and base_dir and os.path.exists(base_dir):
        try:
            import arcpy
            gdbs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if d.endswith(".gdb")]
            if gdbs:
                gdb = gdbs[0]
                arcpy.env.workspace = gdb
                fcs = arcpy.ListFeatureClasses() or []
                sname_lower = str(study_area_name).lower()
                bnd_fcs = [fc for fc in fcs if fc.lower() in (sname_lower, str(sname_lower) + "_boundary", "boundary", "study_area", "mask")]
                if not bnd_fcs:
                    for fc in fcs:
                        try:
                            if arcpy.Describe(fc).shapeType == "Polygon":
                                bnd_fcs.append(fc)
                                break
                        except Exception:
                            pass
                if bnd_fcs:
                    b_fc = os.path.join(gdb, bnd_fcs[0])
                    total_sqkm = 0.0
                    total_perim_km = 0.0
                    with arcpy.da.SearchCursor(b_fc, ["SHAPE@"]) as cur:
                        for row in cur:
                            g = row[0]
                            if g:
                                try:
                                    total_sqkm += g.getArea("GEODESIC", "SQUAREKILOMETERS")
                                    total_perim_km += g.getLength("GEODESIC", "KILOMETERS")
                                except Exception:
                                    total_sqkm += (g.area / 1e6)
                                    total_perim_km += (g.length / 1e3)
                    if total_sqkm > 0:
                        sp_info["area"] = "{:,.2f} كم² ({:,.2f} مليون هكتار)".format(total_sqkm, total_sqkm / 10000.0) if total_sqkm >= 10000 else "{:,.2f} كم² ({:,.2f} هكتار)".format(total_sqkm, total_sqkm * 100)
                    if total_perim_km > 0:
                        sp_info["perimeter"] = "{:,.2f} كم".format(total_perim_km)
                    
                    desc = arcpy.Describe(b_fc)
                    ext = desc.extent
                    sr = desc.spatialReference
                    sr_wgs = arcpy.SpatialReference(4326)
                    p_min = arcpy.PointGeometry(arcpy.Point(ext.XMin, ext.YMin), sr).projectAs(sr_wgs)
                    p_max = arcpy.PointGeometry(arcpy.Point(ext.XMax, ext.YMax), sr).projectAs(sr_wgs)
                    sp_info["extent"] = u"{:.4f}°N إلى {:.4f}°N | {:.4f}°E إلى {:.4f}°E".format(p_min.firstPoint.Y, p_max.firstPoint.Y, p_min.firstPoint.X, p_max.firstPoint.X)
                
                pt_fcs = [fc for fc in fcs if "point" in fc.lower() or "grid" in fc.lower() or "sample" in fc.lower()]
                if pt_fcs:
                    p_fc = os.path.join(gdb, pt_fcs[0])
                    cnt = int(arcpy.management.GetCount(p_fc)[0])
                    sp_info["points"] = u"{:,} محطة رصد مناخية".format(cnt)
        except Exception:
            pass

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # ==============================================================================
    # SHEET 1: 01_عن_المخرج_About_Atlas
    # ==============================================================================
    ws1 = wb.create_sheet(title="01_عن_المخرج_About_Atlas")
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:G1")
    study_display = sp_info.get("display_name") or study_area_name
    tcell = ws1.cell(1, 1, u"أطلس المناخ الرقمي لـ {}\nDigital Climate Atlas of {} — NASA POWER Atlas Engine".format(study_display, study_area_name))
    tcell.font = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    tcell.fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    tcell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws1.row_dimensions[1].height = 45

    # Section 1: Spatial & Boundary Profile
    ws1.merge_cells("A3:G3")
    s1 = ws1.cell(3, 1, "1. بطاقة الهوية المكانية لمنطقة الدراسة (Spatial & Boundary Profile)")
    s1.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    s1.fill = SECTION_FILL
    s1.alignment = Alignment(horizontal="right", vertical="center")
    ws1.row_dimensions[3].height = 24

    def_area = "محسوبة هندسياً من مضلع قناع منطقة الدراسة"
    def_perim = "محسوبة هندسياً من مضلع قناع منطقة الدراسة"
    def_extent = "مستخرج من نطاق حدود منطقة الدراسة WGS84"
    def_points = "محسوبة من شبكة نقاط الرصد المعتمدة"

    spatial_meta = [
        ("اسم منطقة الدراسة (Study Area Name)", sp_info.get("name", study_area_name), "النطاق الإقليمي المعتمد في التحميل والمعالجة"),
        ("المساحة الكلية لمنطقة الدراسة (Total Area)", sp_info.get("area", def_area), "محسوبة هندسياً بدقة من مضلع قناع منطقة الدراسة"),
        ("المحيط الكلي للحدود (Total Perimeter)", sp_info.get("perimeter", def_perim), "شاملاً الحدود المحيطة لمنطقة الدراسة"),
        ("الامتداد الجغرافي الفلكي (Coordinates Extent)", sp_info.get("extent", def_extent), "النطاق المرجعي العالمي WGS 1984 (EPSG:4326)"),
        ("عدد محطات / نقاط شبكة الرصد (Sampling Grid)", sp_info.get("points", def_points), "موزعة بانتظام جغرافي على كامل نطاق منطقة الدراسة"),
    ]

    for idx, (prop, val, note) in enumerate(spatial_meta, 4):
        ws1.cell(idx, 1, idx - 3).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(idx, 1).font = DATA_FONT_BOLD
        ws1.cell(idx, 2, prop).alignment = Alignment(horizontal="right", vertical="center")
        ws1.cell(idx, 2).font = DATA_FONT_BOLD
        ws1.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=4)
        c3 = ws1.cell(idx, 3, val)
        c3.alignment = Alignment(horizontal="center", vertical="center")
        c3.font = CODE_FONT_BOLD
        ws1.merge_cells(start_row=idx, start_column=5, end_row=idx, end_column=7)
        c5 = ws1.cell(idx, 5, note)
        c5.alignment = Alignment(horizontal="right", vertical="center")
        c5.font = DATA_FONT
        for c in range(1, 8):
            ws1.cell(idx, c).border = THIN_BORDER
            ws1.cell(idx, c).fill = ROW_EVEN_FILL if idx % 2 == 0 else ROW_WHITE_FILL
        ws1.row_dimensions[idx].height = 22

    # Section 2: Technical & Raster Processing Profile
    r_start = 10
    ws1.merge_cells("A{0}:G{0}".format(r_start))
    s2 = ws1.cell(r_start, 1, "2. مواصفات المعالجة الفنية والكارتوجرافية (Technical Processing Parameters)")
    s2.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    s2.fill = SECTION_FILL
    s2.alignment = Alignment(horizontal="right", vertical="center")
    ws1.row_dimensions[r_start].height = 24

    tc_info = tech_info or {}
    tech_meta = [
        ("دقة خلية الراستر الكارتوجرافية (Raster Cell Size)", tc_info.get("cell_size", "500 متر (500 Meters)"), "مخرجات شبكية منتظمة ملساء خالية من حواف التكسير البصري"),
        ("تباعد شبكة متجهات الرياح (Wind Vector Spacing)", tc_info.get("wind_cell", "25,000 متر (25 كم)"), "شبكة أسهم متجهات اتجاه وسرعة الرياح السطحية"),
        ("فاصل خطوط تساوي الضغط (Isobar Step)", tc_info.get("isobar_step", "4.0 mbar (Global Standard)"), "فاصل الآيزوبار المعتمد أرصادياً عالمياً"),
        ("طريقة الاستيفاء المكاني (Interpolation Algorithm)", tc_info.get("interp", "IDW (Inverse Distance Weighted)"), "خوارزمية مقلوب مربع المسافة الموزونة"),
        ("تنسيق ونمط ملفات الراستر (Raster Format)", tc_info.get("format", "GeoTIFF 32-bit Float (LZW Compressed)"), "راسترات عائمة أصلية مقصوصة تماماً على حدود منطقة الدراسة"),
        ("فترة الرصد المناخي القياسية (Climate Period)", tc_info.get("period", "1996 – 2025 (30 عاماً)"), "تطابق المعدل المناخي القياسي العالمي (Climate Normal)"),
        ("مزود ومصدر البيانات المناخية (Data Source)", tc_info.get("source", "NASA POWER API (CERES & MERRA-2)"), "نماذج إعادة التحليل والرصد الفضائي الدقيق لناسا"),
    ]

    for idx, (prop, val, note) in enumerate(tech_meta, r_start + 1):
        ws1.cell(idx, 1, idx - r_start).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(idx, 1).font = DATA_FONT_BOLD
        ws1.cell(idx, 2, prop).alignment = Alignment(horizontal="right", vertical="center")
        ws1.cell(idx, 2).font = DATA_FONT_BOLD
        ws1.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=4)
        c3 = ws1.cell(idx, 3, val)
        c3.alignment = Alignment(horizontal="center", vertical="center")
        c3.font = CODE_FONT_BOLD
        ws1.merge_cells(start_row=idx, start_column=5, end_row=idx, end_column=7)
        c5 = ws1.cell(idx, 5, note)
        c5.alignment = Alignment(horizontal="right", vertical="center")
        c5.font = DATA_FONT
        for c in range(1, 8):
            ws1.cell(idx, c).border = THIN_BORDER
            ws1.cell(idx, c).fill = ROW_EVEN_FILL if idx % 2 == 0 else ROW_WHITE_FILL
        ws1.row_dimensions[idx].height = 22

    # Section 3: Recommendation Matrix
    r_rec = 19
    ws1.merge_cells("A{0}:G{0}".format(r_rec))
    s3 = ws1.cell(r_rec, 1, "3. مصفوفة التوصية الذكية لعدد الفئات وفقاً لتباين البيانات والمدى الرقمي (Intelligent Recommendation Based on Data Variance & Range)")
    s3.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    s3.fill = SECTION_FILL
    s3.alignment = Alignment(horizontal="right", vertical="center")
    ws1.row_dimensions[r_rec].height = 24

    variance_guide_text = (
        "القاعدة الكارتوجرافية والإحصائية في اختيار عدد الفئات لا تتقيد بالمساحة الجغرافية وحدها؛ بل إن المعيار الجوهري والحاسم هو "
        "درجة التباين الإحصائي والمدى الرقمي الحقيقي للبيانات (Data Variance & Dynamic Range):\n"
        "• إذا كان التباين في البيانات كبيراً والمدى واسعاً (سواء كانت المساحة شاسعة أو رقعة محدودة ذات تضاريس متباينة): "
        "يُتاح للمستخدم كامل الحرية في الاختيار بين (3، 5، 7، أو 9 فئات)، حيث يستوعب التباين الكبير التدرجات المتعددة دون تداخل بصري.\n"
        "• إذا كان التباين في البيانات صغيراً والمدى ضيقاً أو شبه متجانس (حتى لو كانت المساحة هائلة كهضبة صحراوية أو سهل منبسط): "
        "يجب الاكتفاء بـ (3 فئات) أو كحد أقصى (5 فئات)، وتجنب (7 و 9 فئات) لتفادي تجزئة قيم متقاربة جداً وخلق حدود مصطنعة ووهمية تشوه مفتاح الخريطة."
    )

    rec_rows = [
        ("3 فئات (Executive & Low Variance)", "3", "المعيار الأساسي للتباين المنخفض والتقارير التنفيذية ★",
         "البيانات ذات المدى الرقمي الضيق والمناطق المتجانسة مناخياً، والتقارير التنفيذية والملخصات السريعة (بغض النظر عن مساحة المنطقة).",
         "وضوح كارتوجرافي فائق، قراءة بصرية فورية وسهلة، ومنع توليد حدود مصطنعة بين قيم متقاربة.",
         "دمج بعض التدرجات والتفاصيل المحلية إذا كانت البيانات ذات تباين ومجال واسع.",
         "04_تصنيف_3_فئات_Classes_3"),

        ("5 فئات (Standard & Balanced)", "5", "المعيار الكارتوجرافي الذهبي العام (الأكثر توازناً) ★",
         "البيانات ذات التباين الطبيعي والمتوسط والمرتفع (الخيار القياسي المعتمد لأكثر من 90% من خرائط الأطلس للباحثين والمخططين).",
         "التوازن الكارتوجرافي الأمثل بين إبراز التباين المكاني وسهولة تمييز درجات الألوان وتوافقها مع المعايير الدولية (WMO).",
         "تغطي النمط العام بكفاءة، ولكنها قد تتطلب النزول لـ 3 فئات إذا كان تباين المتغير شديد الضيق.",
         "05_تصنيف_5_فئات_Classes_5"),

        ("7 فئات (Academic & High Variance)", "7", "موصى به في حالات التباين الرقمي والتضاريسي الكبير",
         "المتغيرات ذات التباين المكاني الواسع، ومناطق التضاريس الجبلية والساحلية، والأبحاث الأكاديمية ودراسات التغير المناخي والزراعة.",
         "إبراز التدرجات الدقيقة والتغيرات الانتقالية الحساسة عبر نطاق منطقة الدراسة.",
         "تتطلب تمايزاً حقيقياً في البيانات؛ ولا تناسب البيانات ذات التباين الضعيف لتجنب التشتت والتقارب اللوني المربك.",
         "06_تصنيف_7_فئات_Classes_7"),

        ("9 فئات (Specialized & Extreme)", "9", "خاص بالتباين الشديد جداً والمدى الرقمي فائق الاتساع",
         "المتغيرات ذات المدى الرقمي الفائق (مثل الإشعاع الشمسي الكلي، التساقط في الأقاليم ذات التباين الحاد، وسرعات الرياح العاصفة).",
         "تغطية طيفية فائقة الدقة تظهر أدق التفاصيل المكانية للبيانات المستمرة.",
         "محظور استخدامها مع المتغيرات ذات التباين الصغير لتفادي خلق فئات ميكروية غير ذات دلالة وتوليد فئات خالية من المساحة.",
         "07_تصنيف_9_فئات_Classes_9"),
    ]

    ws1.merge_cells("A20:G20")
    rec_desc = ws1.cell(20, 1, variance_guide_text)
    rec_desc.font = Font(name="Segoe UI", size=9.5, italic=True)
    rec_desc.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    ws1.row_dimensions[20].height = 54

    rec_headers = [
        (1, "خيار التصنيف\nTier", 16),
        (2, "عدد الفئات\nClasses", 12),
        (3, "مستوى التوصية\nRecommendation", 22),
        (4, "أفضل حالات الاستخدام والتطبيق\nBest Use Case", 42),
        (5, "المزايا والخصائص الكارتوجرافية\nCartographic Advantages", 38),
        (6, "المحددات والملاحظات الفنية\nLimitations & Warnings", 38),
        (7, "اسم ورقة العمل في الملف\nTarget Sheet", 26),
    ]

    for col_idx, h_text, width in rec_headers:
        cell = ws1.cell(22, col_idx, h_text)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER
        col_letter = get_column_letter(col_idx)
        ws1.column_dimensions[col_letter].width = max(ws1.column_dimensions[col_letter].width or 0, width)
    ws1.row_dimensions[22].height = 28

    for r_idx, r_vals in enumerate(rec_rows, 23):
        is_rec = "المعيار الذهبي" in r_vals[2]
        bg = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") if is_rec else (ROW_EVEN_FILL if r_idx % 2 == 0 else ROW_WHITE_FILL)
        for c_idx, val in enumerate(r_vals, 1):
            cell = ws1.cell(r_idx, c_idx, val)
            cell.border = THIN_BORDER
            cell.fill = bg
            if c_idx in (1, 2, 7):
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = DATA_FONT_BOLD if c_idx == 1 else (CODE_FONT_BOLD if c_idx == 7 else DATA_FONT)
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Segoe UI", size=9, bold=True, color="276A3C" if is_rec else "1F4E79")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.font = DATA_FONT
        ws1.row_dimensions[r_idx].height = 25

    # Section 4: Project Output Hierarchy & File Catalog
    r_hier = 28
    ws1.merge_cells("A{0}:G{0}".format(r_hier))
    s4 = ws1.cell(r_hier, 1, "4. دليل الهيكل التنظيمي ومستويات المخرجات والملفات (Project Output Hierarchy & File Catalog)")
    s4.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    s4.fill = SECTION_FILL
    s4.alignment = Alignment(horizontal="right", vertical="center")
    ws1.row_dimensions[r_hier].height = 24

    ws1.merge_cells("A{0}:G{0}".format(r_hier + 1))
    hier_desc = ws1.cell(r_hier+1, 1,
        "يوضح هذا الجدول المستويات الهرمية للمخرجات، بدءاً من مجلد العمل الجذري، ثم مجلد منطقة الدراسة المسمى تلقائياً، "
        "يليه تفصيل المجلدات والملفات الفرعية وامتداداتها (.gdb, .tif, .aux.xml, .ovr, .lyr/.lyrx, .xlsx, .xls, .txt) ومعناها الوظيفي والكارتوجرافي:"
    )
    hier_desc.font = Font(name="Segoe UI", size=9.5, italic=True)
    hier_desc.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    ws1.row_dimensions[r_hier+1].height = 32

    hier_headers = [
        (1, "المستوى الهرمي\nLevel", 16),
        (2, "المسار واسم المجلد أو الملف\nRelative Path & Name", 36),
        (3, "نوع الكائن والامتداد\nObject Type & Ext", 22),
        (4, "المعنى الوظيفي والوصف الفني التفصيلي\nFunctional Meaning & Technical Specification", 52),
        (5, "الدور والاستخدام في برمجيات الـ GIS\nRole & Application in GIS / Cartography", 45),
    ]

    r_hhead = r_hier + 3
    for col_idx, h_text, width in hier_headers:
        if col_idx == 4:
            ws1.merge_cells(start_row=r_hhead, start_column=4, end_row=r_hhead, end_column=5)
            cell = ws1.cell(r_hhead, 4, h_text)
        elif col_idx == 5:
            ws1.merge_cells(start_row=r_hhead, start_column=6, end_row=r_hhead, end_column=7)
            cell = ws1.cell(r_hhead, 6, h_text)
        else:
            cell = ws1.cell(r_hhead, col_idx, h_text)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        target_cols = range(4, 6) if col_idx == 4 else (range(6, 8) if col_idx == 5 else [col_idx])
        for c in target_cols:
            ws1.cell(r_hhead, c).border = THIN_BORDER
            ws1.cell(r_hhead, c).fill = HEADER_FILL
    ws1.row_dimensions[r_hhead].height = 28

    hier_rows = [
        ("المستوى 0\nRoot Workspace", "[Output_Workspace]", "Directory (مجلد رئيسي)",
         "مسار مجلد العمل الأساسي الذي يحدده المستخدم في واجهة الأداة لحفظ كافة مخرجات الأطلس المناخي.",
         "الحاوية الرئيسية الشاملة لكافة مشاريع ونطاقات التحليل المكاني."),

        ("المستوى 1\nStudy Area Folder", "[Output_Workspace]\\ [{}]".format(study_area_name), "Directory (مجلد منطقة الدراسة)",
         u"المجلد الرئيسي الخاص بمنطقة الدراسة المحددة ({})؛ يضم داخله كافة قواعد البيانات والراسترات والجداول والتقارير المنظمة.".format(study_area_name),
         "عزل وتنظيم مشاريع الدول والأقاليم المختلفة لمنع تداخل ملفات التحميل والمعالجة."),

        ("المستوى 2\nGeodatabase", "[{}]\\Climate_Database_From_1996_To_2025.gdb".format(study_area_name), ".gdb (Esri File GDB)",
         "قاعدة البيانات الجغرافية الرئيسية الشاملة؛ تضم 31+ طبقة نقطية لكافة عناصر المناخ، وحقول الإدارة، والتحليلات الفصلية والسنوية، ووحدة القياس (Measurement_Unit)، وشبكة أسهم الرياح وخطوط تساوي الضغط (Isobars) وحدود منطقة الدراسة.",
         "المصدر الجغرافي المعياري المرجعي للبيانات المتجهة والتحليلات المكانية داخل ArcGIS Pro و ArcMap."),

        ("المستوى 2\nTables & Reports", "[{}]\\00_Tables_And_Reports".format(study_area_name), "Directory (مجلد الجداول)",
         "المجلد المخصص لحفظ جداول البيانات المنظمة بصيغة Excel، وقواميس البيانات، ودليل التصنيف وسجل المعالجة الفني، بدون أي ملفات CSV مؤقتة لتقليل التشتت والازدحام.",
         "الحاوية الوثائقية والجدولية للأطلس للاستعراض السريع وإرفاق التقارير."),

        ("المستوى 3\nClassification Guide", "00_Tables_And_Reports\\Climate_Atlas_Classification_Guide.xlsx", ".xlsx (مصنف إكسل شامل)",
         "دليل التصنيف الكارتوجرافي المتكامل؛ يضم مواصفات المعالجة، مصفوفة التوصيات، دليل حقول الإدارة، المعايير العلمية، وتصنيفات 3 و 5 و 7 و 9 فئات وقيم الفواصل ومفاتيح الخريطة الجاهزة للنسخ مع رموز الوحدات (°C، mm، إلخ).",
         "المرجع الأساسي لمهندس الكارتوجرافيا لضبط وترميز وتوحيد مفاتيح خرائط الأطلس."),

        ("المستوى 3\nData Tables", "00_Tables_And_Reports\\[Element]_Table.xls", ".xls (جداول إكسل منظمة)",
         "جداول بيانات منسقة لكل عنصر مناخي تتضمن إحداثيات محطات الرصد، وكود النقطة، وفترة الرصد، ووحدة القياس المعتمدة (Measurement_Unit)، وكافة المتغيرات.",
         "تداول البيانات المناخية واستيرادها المباشر في برمجيات الجداول والتحليل الإحصائي (SPSS/R)."),

        ("المستوى 3\nMetadata Dictionaries", "00_Tables_And_Reports\\*Dictionary*.xls", ".xls (قواميس البيانات)",
         "قواميس المصطلحات والبيانات الوصفية (Metadata_Dictionary.xls & Field_Dictionary_Arabic.xls) التي توثق الاسم الإنجليزي والعربي والوحدة والمعادلة الرياضية والمصدر لكل حقل.",
         "قاموس البيانات المعتمد (Data Dictionary) للأطلس المناخي لضمان المعيارية وتوثيق البيانات."),

        ("المستوى 3\nProcessing Log", "00_Tables_And_Reports\\Processing_Log.txt", ".txt (سجل المعالجة الفني)",
         "السجل الزمني والتقني التفصيلي لعملية التشغيل؛ يوثق الخوارزميات، ودقة الخلايا، وفترة السلسلة، وتدقيق الجودة الشامل (QA Status: ALL PASS) مع خلو البيانات من قيم الفقد الشاذة (-999).",
         "شهادة ضبط الجودة والأصالة الفنية للبيانات المصدرة."),

        ("المستوى 2\nRaster Thematic Folders", u"[{}]\\01_Temperature إلى 18_Trends_And_Anomalies".format(study_area_name), "Directory (مجلدات الراستر)",
         "مجلدات موضوعية مستقلة ومرتبة كارتوجرافياً لكل عنصر مناخي؛ يحتوي كل مجلد على كافة صور الراستر وطبقات التمثيل الخاصة به.",
         "التنظيم الموضوعي الكارتوجرافي للمشروع وسهولة أرشفة وتداول الطبقات."),

        ("المستوى 3\nContinuous Raster", "[Folder]\\[Field_Name].tif", ".tif (GeoTIFF 32-bit Float)",
         "خريطة السطح المناخي الشبكي المستمر للمتغير؛ محسوبة بدقة خلية فائقة وبضغط LZW وبقيم عائمة حقيقية مقصوصة هندسياً تماماً على قناع حدود منطقة الدراسة.",
         "الطبقة الجغرافية التحليلية الأساسية للخرائط والنمذجة المكانية والتحليل الطبوغرافي."),

        ("المستوى 3\nRaster Statistics Sidecar", "[Folder]\\[Field_Name].tif.aux.xml", ".aux.xml (بيانات مرافقة)",
         "ملف ميتاداتا مصاحب للراستر؛ يحفظ الإسناد المكاني والإحصائيات الرقمية الدقيقة (Min, Max, Mean, StdDev) وجداول الفئات دون المساس بملف الراستر الأصلي.",
         "قراءة الإحصائيات الفورية وتحديد فواصل الفئات تلقائياً في برمجيات الـ GIS دون الحاجة لحسابها مجدداً."),

        ("المستوى 3\nPyramid Overviews", "[Folder]\\[Field_Name].tif.ovr", ".ovr (أهرامات الراستر)",
         "طبقات الاستعراض الهرمي المتعدد الدقات (Pyramid Layers) المنشأة بنمط Bilinear؛ تسرع فتح وتكبير وتصفح الراسترات ذات الملايين من الخلايا دون أي بطء في العرض.",
         "كفاءة وسلاسة التصفح البصري الفوري في بيئات العرض الجغرافي والكارتوجرافي."),

        ("المستوى 3\nLayer Symbology", "[Folder]\\[Field_Name].lyr / .lyrx", ".lyr / .lyrx (ملف الطبقة)",
         "ملف حفظ ترميز الطبقة وخصائص التمثيل؛ يحفظ درجات الألوان القياسية (Color Ramp) والفئات الكارتوجرافية المعتمدة للعرض الفوري.",
         "سحب الطبقة مباشرة إلى جدول المحتويات (TOC) برمزيتها وألوانها الجاهزة دون الحاجة لأي ضبط يدوي."),
    ]

    for h_i, h_data in enumerate(hier_rows, r_hhead + 1):
        bg = ROW_EVEN_FILL if h_i % 2 == 0 else ROW_WHITE_FILL
        ws1.cell(h_i, 1, h_data[0]).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws1.cell(h_i, 1).font = DATA_FONT_BOLD
        ws1.cell(h_i, 2, h_data[1]).alignment = Alignment(horizontal="left", vertical="center")
        ws1.cell(h_i, 2).font = CODE_FONT_BOLD
        ws1.cell(h_i, 3, h_data[2]).alignment = Alignment(horizontal="center", vertical="center")
        ws1.cell(h_i, 3).font = DATA_FONT_BOLD

        ws1.merge_cells(start_row=h_i, start_column=4, end_row=h_i, end_column=5)
        c4 = ws1.cell(h_i, 4, h_data[3])
        c4.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
        c4.font = DATA_FONT

        ws1.merge_cells(start_row=h_i, start_column=6, end_row=h_i, end_column=7)
        c6 = ws1.cell(h_i, 6, h_data[4])
        c6.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
        c6.font = DATA_FONT

        for c in range(1, 8):
            ws1.cell(h_i, c).border = THIN_BORDER
            ws1.cell(h_i, c).fill = bg
        ws1.row_dimensions[h_i].height = 36

    # ==============================================================================
    # SHEET 2: 02_حقول_الإدارة_Admin_Fields
    # ==============================================================================
    ws2 = wb.create_sheet(title="02_حقول_الإدارة_Admin_Fields")
    ws2.views.sheetView[0].showGridLines = True

    admin_headers = [
        (1, "م\nNo.", 6),
        (2, "اسم الحقل المختصر (Shapefile)\nShort Field Name", 22),
        (3, "اسم الحقل الكامل (Geodatabase)\nFull Field Name (EN)", 26),
        (4, "نوع البيانات\nData Type", 14),
        (5, "وحدة القياس\nUnit", 14),
        (6, "الشرح والتوصيف العلمي باللغة العربية\nArabic Scientific Description", 55),
        (7, "الوصف الفني باللغة الإنجليزية\nEnglish Technical Description", 50),
    ]

    for col_idx, h_text, width in admin_headers:
        cell = ws2.cell(1, col_idx, h_text)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER
        col_letter = get_column_letter(col_idx)
        ws2.column_dimensions[col_letter].width = width
    ws2.row_dimensions[1].height = 30

    admin_meta_expanded = [
        (1, "OBJECTID", "OBJECTID", "Integer (OID)", "-", "المعرف الرقمي الفريد التلقائي لطبقة المعالم داخل قاعدة البيانات الجيوداتابيز.", "Unique primary key identifier generated by File Geodatabase."),
        (2, "Source_ID", "Source_ID", "Integer", "-", "المعرف المرجعي الأصلي الثابت لنقطة شبكة الرصد المناخي.", "Stable reference ID of the meteorological sampling grid point."),
        (3, "Point_Lat", "Point_Lat", "Double", "درجة (°)", "دائرة العرض الجغرافية للنقطة بنظام الإحداثيات العالمي WGS 1984.", "Geographic Latitude in decimal degrees (WGS 1984 / EPSG:4326)."),
        (4, "Point_Lon", "Point_Lon", "Double", "درجة (°)", "خط الطول الجغرافي للنقطة بنظام الإحداثيات العالمي WGS 1984.", "Geographic Longitude in decimal degrees (WGS 1984 / EPSG:4326)."),
        (5, "Data_Start", "Data_Start", "Text (Date)", "سنة / شهر", "تاريخ وسنة بداية سلسلة الرصد المناخي المسترجعة من سيرفر ناسا.", "Start date/year of the retrieved NASA POWER climate observation series."),
        (6, "Data_End", "Data_End", "Text (Date)", "سنة / شهر", "تاريخ وسنة نهاية سلسلة الرصد المناخي المسترجعة من سيرفر ناسا.", "End date/year of the retrieved NASA POWER climate observation series."),
        (7, "Temporal", "Temporal", "Text", "فترة", "النمط والمدى الزمني المستخدم في المعالجة (شهري / يومي / معدلات قياسية).", "Temporal processing resolution (Daily / Monthly / Climatological Normals)."),
        (8, "Intrp_Meth", "Interp_Meth", "Text", "خوارزمية", "خوارزمية الاستيفاء والاشتقاق المكاني المطبقة لإنشاء أسطح الراستر.", "Spatial interpolation method applied (IDW / Kriging / Spline)."),
        (9, "Cell_Size", "Cell_Size", "Double", "متر / درجة", "حجم ودقة خلية الراستر الكارتوجرافية المنتجة.", "Output cartographic raster pixel resolution in linear meters or degrees."),
        (10, "Wind_Cell", "Wind_Cell", "Double", "متر / درجة", "تباعد شبكة متجهات وأسهم الرياح الكارتوجرافية.", "Cartographic fishnet spacing for wind vector arrows and direction points."),
        (11, "Measurement_Unit", "Measurement_Unit", "Text (25)", "رمز الوحدة", "وحدة القياس المعتمدة للمتغير في الطبقة (°C، mm، hPa، m/s، إلخ).", "Standard measurement unit assigned to the climate variable in the layer."),
        (12, "Status", "Status", "Text", "حالة", "حالة نجاح استرجاع ومعالجة بيانات النقطة من السيرفر (OK / FAILED).", "Data query status for the station point (OK or FAILED)."),
        (13, "Error_Msg", "Error_Msg", "Text", "رسالة", "رسالة الخطأ التفصيلية في حال تعذر الاتصال بالنقطة أو وجود قيم غير صالحة.", "Detailed error description if query timed out or returned invalid data."),
    ]

    for row_idx, rdata in enumerate(admin_meta_expanded, 2):
        for col_idx, val in enumerate(rdata, 1):
            cell = ws2.cell(row_idx, col_idx, val)
            cell.border = THIN_BORDER
            cell.fill = ROW_EVEN_FILL if row_idx % 2 == 0 else ROW_WHITE_FILL
            if col_idx in (1, 4, 5):
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = DATA_FONT_BOLD if col_idx == 1 else DATA_FONT
            elif col_idx in (2, 3):
                cell.alignment = Alignment(horizontal="left", vertical="center")
                cell.font = CODE_FONT_BOLD if col_idx == 2 else CODE_FONT
            elif col_idx == 6:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.font = DATA_FONT
            elif col_idx == 7:
                cell.alignment = Alignment(horizontal="left", vertical="center")
                cell.font = DATA_FONT
        ws2.row_dimensions[row_idx].height = 24

    # ==============================================================================
    # SHEET 3: 03_المعايير_العلمية_Standards
    # ==============================================================================
    ws3 = wb.create_sheet(title="03_المعايير_العلمية_Standards")
    ws3.views.sheetView[0].showGridLines = True

    standards_headers = [
        (1, "الرقم\nNo.", 6),
        (2, "اسم العنصر في الأداة\nTool Parameter & Layer", 25),
        (3, "الاسم باللغة العربية\nModule Arabic Name", 28),
        (4, "مجلد الراستر (1:1)\nOutput Raster Folder", 26),
        (5, "طبقة المعالم (1:1)\nFeature Class Name", 26),
        (6, "المؤشرات\nIndicators", 12),
        (7, "الوحدة\nMain Unit", 14),
        (8, "المنهجية والمعادلة العلمية (بالعربية)\nArabic Scientific Methodology & Formula", 55),
        (9, "المعايير والمراجع الدولية (بالإنجليزية)\nScientific Method & Standards (EN)", 45),
    ]

    for col_idx, h_text, width in standards_headers:
        cell = ws3.cell(1, col_idx, h_text)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER
        col_letter = get_column_letter(col_idx)
        ws3.column_dimensions[col_letter].width = width
    ws3.row_dimensions[1].height = 32

    modules_data_expanded = [
        ("01", "01_Temperature", "درجة الحرارة", "01_Temperature", "01_Temperature", 10, "°C",
         "حساب المتوسطات الحسابية لدرجات الحرارة T2M وفق معايير WMO للأطلس المناخي (سنوي، فصلي DJF/MAM/JJA/SON، نهايات عظمى وصغرى يومية).",
         "NASA POWER T2M, T2M_MAX, T2M_MIN / WMO Climatological Normals Standard"),
        ("02", "02_Precipitation", "الأمطار والتساقط", "02_Precipitation", "02_Precipitation", 8, "mm",
         "تجميع التساقط التراكمي PRECTOTCORR سنوياً وفصلياً، مع حساب المدى السنوي والفصلي للأمطار ومجموع الفصول الأربعة.",
         "NASA POWER PRECTOTCORR / Annual, Seasonal Totals & Cumulative Ranges"),
        ("03", "03_Sea_Level_Pressure", "ضغط مستوى سطح البحر", "03_Sea_Level_Pressure", "03_Sea_Level_Pressure", 6, "hPa / mbar",
         "متوسطات ضغط مستوى سطح البحر SLP المعدل طبوغرافياً وفق المعيار البارومتري الدولي لمقارنة الأنظمة الجوية.",
         "NASA POWER SLP / Reduced to Standard Mean Sea Level (MSLP)"),
        ("04", "04_Surface_Pressure", "الضغط السطحي الفعلي", "04_Surface_Pressure", "04_Surface_Pressure", 6, "hPa / mbar",
         "متوسطات الضغط الجوي السطحي الحقيقي PS عند منسوب الارتفاع الطبوغرافي الفعلي للموقع الجغرافي.",
         "NASA POWER PS / Actual Local Topographic Station Surface Pressure"),
        ("05", "05_Wind", "الرياح السطحية (سرعة واتجاه)", "05_Wind", "05_Wind", 13, "m/s, °",
         "متوسطات سرعة الرياح WS10M، والمتوسط الشعاعي الدائري لاتجاه الرياح WD10M باستخدام دالة الظل العكسي atan2(U,V).",
         "NASA POWER WS10M, WD10M / Circular Mean Vector Trigonometry atan2(U,V)"),
        ("06", "06_Relative_Humidity", "الرطوبة النسبية", "06_Relative_Humidity", "06_Relative_Humidity", 6, "%",
         "نسبة بخار الماء الفعلي إلى التشبع RH2M عند درجة حرارة الهواء السطحي (سنوي، فصلي، والمدى السنوي).",
         "NASA POWER RH2M / WMO Psychrometric Standards"),
        ("07", "07_Dew_Point", "نقطة الندى", "07_Dew_Point", "07_Dew_Point", 6, "°C",
         "درجة الحرارة T2MDEW التي يتكثف عندها بخار الماء في الهواء الجوي تحت ضغط ثابت مع حساب عجز نقطة الندى.",
         "NASA POWER T2MDEW / Magnus-Tetens Equation Standard"),
        ("08", "08_Solar_Radiation", "الإشعاع الشمسي", "08_Solar_Radiation", "08_Solar_Radiation", 7, "MJ/m²/day",
         "الإشعاع الشمسي الكلي الساقط على سطح أفقي ALLSKY_SFC_SW_DWN، مع المجموع السنوي التراكمي الساقط.",
         "NASA POWER ALLSKY_SFC_SW_DWN / Total Downward Shortwave Flux"),
        ("09", "09_UV_Index", "مؤشر الأشعة فوق البنفسجية", "09_UV_Index", "09_UV_Index", 6, "Index",
         "مؤشر الأشعة فوق البنفسجية القصوى السطحية لحماية الصحة العامة والتخطيط السياحي والبيئي.",
         "WHO Global Solar UV Index Specification"),
        ("10", "10_Cloud_Cover", "الغطاء السحابي", "10_Cloud_Cover", "10_Cloud_Cover", 6, "%",
         "نسبة تغطية السحب الكلية في قبة السماء السنوية والفصلية من بيانات الاستشعار CERES.",
         "NASA CERES Total Cloud Area Fraction Standard"),
        ("11", "11_Heat_Index", "الراحة الحرارية والرطوبة", "11_Heat_Index", "11_Heat_Index", 5, "°C",
         "دليل الحرارة والرطوبة Humidex، ودليل درجة حرارة البصيلة الرطبة الكروية WBGT لتقييم الإجهاد الحراري البشري.",
         "Masterton & Richardson (1979) Humidex, Liljegren (2008) WBGT Standard"),
        ("12", "12_Wind_Chill", "لسعة الرياح والبرودة", "12_Wind_Chill", "12_Wind_Chill", 2, "°C",
         "مؤشر التبريد الرياحي الشتوي والسنوي لتقييم فقدان الحرارة السطحي للإنسان.",
         "Osczevski & Bluestein (2005) Wind Chill Standard"),
        ("13", "13_De_Martonne_Aridity", "دليل دومارتون للجفاف", "13_De_Martonne_Aridity", "13_De_Martonne_Aridity", 1, "Index",
         "معادلة De Martonne Aridity السنوية I = P / (T + 10) لتحديد درجات الجفاف الإقليمي.",
         "De Martonne (1926) Aridity Index"),
        ("14", "14_Evapotranspiration", "البخر-نتح المرجعي", "14_Evapotranspiration", "14_Evapotranspiration", 9, "mm",
         "معدل البخر-نتح المرجعي المحسوب وفق صيغة Hargreaves-Samani السنوية والفصلية.",
         "Hargreaves & Samani (1985) Reference Evapotranspiration FAO-56"),
        ("15", "15_UNEP_Aridity", "مؤشر الجفاف العالمي UNEP", "15_UNEP_Aridity", "15_UNEP_Aridity", 1, "Index",
         "مؤشر الجفاف الدولي UNEP AI = P / PET لتصنيف المناطق الجافة وشبه الجافة وفق أطلس التصحر العالمي.",
         "UNEP World Atlas of Desertification Standard"),
        ("16", "16_Water_Deficit", "العجز المائي المناخي", "16_Water_Deficit", "16_Water_Deficit", 1, "mm",
         "العجز المائي الصافي (P - PET) لتقييم الاحتياجات المائية والري التكميلي.",
         "Thornthwaite & Mather (1955) Climatic Water Balance"),
        ("17", "17_Dry_Months", "عدد شهور الجفاف", "17_Dry_Months", "17_Dry_Months", 1, "Months",
         "عدد شهور السنة التي يقل فيها المطر عن ضعف درجة الحرارة (P < 2T) وفق معيار Bagnouls & Gaussen.",
         "Bagnouls & Gaussen (1957) Xerothermic Index"),
        ("18", "18_Trends_And_Anomalies", "اتجاهات وشذوذ المناخ", "18_Trends_And_Anomalies", "18_Trends_And_Anomalies", 8, "°C, mm, %",
         "اتجاهات التغير لعقد من الزمان وشذوذ المناخ مقارنة بالمعدل القياسي الطبيعي 1991-2020.",
         "WMO Climate Anomaly Standard & Least-Squares Linear Trends"),
    ]

    for row_idx, rdata in enumerate(modules_data_expanded, 2):
        for col_idx, val in enumerate(rdata, 1):
            cell = ws3.cell(row_idx, col_idx, val)
            cell.border = THIN_BORDER
            cell.fill = ROW_EVEN_FILL if row_idx % 2 == 0 else ROW_WHITE_FILL
            if col_idx in (1, 6, 7):
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = DATA_FONT_BOLD if col_idx == 1 else DATA_FONT
            elif col_idx in (2, 4, 5, 9):
                cell.alignment = Alignment(horizontal="left", vertical="center")
                cell.font = CODE_FONT_BOLD if col_idx in (2, 4, 5) else DATA_FONT
            elif col_idx in (3, 8):
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.font = DATA_FONT_BOLD if col_idx == 3 else DATA_FONT
        ws3.row_dimensions[row_idx].height = 28

    # Total Summary row
    ws3.cell(20, 3, "الإجمالي العام للمؤشرات المناخية الخرائطية:").alignment = Alignment(horizontal="right", vertical="center")
    ws3.cell(20, 3).font = Font(name="Segoe UI", size=10, bold=True, color="1F4E79")
    ws3.cell(20, 6, 103).alignment = Alignment(horizontal="center", vertical="center")
    ws3.cell(20, 6).font = Font(name="Consolas", size=10, bold=True, color="1F4E79")
    for c in range(1, 10):
        ws3.cell(20, c).border = THIN_BORDER
        ws3.cell(20, c).fill = SECTION_FILL
    ws3.row_dimensions[20].height = 25

    # ==============================================================================
    # FUNCTION TO BUILD A CLASSIFICATION SHEET (Classes_3, Classes_5, Classes_7, Classes_9)
    # ==============================================================================
    def build_class_sheet(target_wb, sheet_title, n_classes, tier_label):
        ws = target_wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True

        headers = [
            (1, "م\nNo.", 6),
            (2, "الموديول المناخي\nClimate Module", 25),
            (3, "المسار النسبي وهيئة ملف الراستر\nRelative Raster Path & Format", 46),
            (4, "اسم الحقل في قاعدة البيانات\nField Name (EN)", 26),
            (5, "الاسم الفني بالإنجليزية\nTechnical Name (EN)", 35),
            (6, "اسم الخريطة المقترح للأطلس (بالعربية)\nSuggested Atlas Map Title (AR)", 40),
            (7, "التوصيف العلمي باللغة العربية\nArabic Scientific Description", 48),
            (8, "وحدة القياس\nUnit", 14),
            (9, "طريقة التصنيف\nMethod", 18),
            (10, "طول الخطوة (صحيح)\nStep (Integer)", 16),
            (11, "طول الخطوة (عشري)\nStep (1 Decimal)", 16),
            (12, "أدنى قيمة بالمنطقة\nMin", 15),
            (13, "أقصى قيمة بالمنطقة\nMax", 15),
            (14, "متوسط المنطقة\nMean", 15),
        ]

        base_c = 14
        for ci in range(1, n_classes + 1):
            if ci == 1:
                lbl_int = u"الفئة 1 - أرقام صحيحة (الأعلى)\nClass 1 - Integer (Highest)"
                lbl_dec = u"الفئة 1 - كسر عشري واحد (الأعلى)\nClass 1 - 1 Decimal (Highest)"
            elif ci == n_classes:
                lbl_int = u"الفئة {} - أرقام صحيحة (الأدنى)\nClass {} - Integer (Lowest)".format(ci, ci)
                lbl_dec = u"الفئة {} - كسر عشري واحد (الأدنى)\nClass {} - 1 Decimal (Lowest)".format(ci, ci)
            else:
                lbl_int = u"الفئة {} - أرقام صحيحة\nClass {} - Integer".format(ci, ci)
                lbl_dec = u"الفئة {} - كسر عشري واحد\nClass {} - 1 Decimal".format(ci, ci)
            headers.append((base_c + (ci - 1) * 2 + 1, lbl_int, 30))
            headers.append((base_c + (ci - 1) * 2 + 2, lbl_dec, 20))

        for col_idx, h_text, width in headers:
            cell = ws.cell(1, col_idx, h_text)
            cell.font = HEADER_FONT
            cell.fill = HEADER_FILL
            cell.alignment = HEADER_ALIGN
            cell.border = THIN_BORDER
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width
        ws.row_dimensions[1].height = 32

        for map_idx, fentry in enumerate(climate_fields, 1):
            full_f = fentry['full_f']
            mod = fentry['module']
            unit = fentry['unit']
            title_ar = fentry['title_ar']
            desc_ar = fentry['desc_ar']
            en_name = fentry.get('en_name', full_f.replace('_', ' '))

            # Lookup actual raster stats
            st = raster_stats.get(full_f, {'min': 0.0, 'max': 1.0, 'mean': 0.5, 'tif': full_f + '.tif'})
            
            # Determine relative path
            mod_clean = mod.split('(')[0].strip() if '(' in mod else mod
            default_folder = MODULE_FOLDER_MAP.get(mod_clean, mod_clean.replace(' ', '_'))
            folder = st.get('folder') or default_folder
            rel_path_str = u"[{}] \\ {} \\ {} (GeoTIFF Float32)".format(study_area_name, folder, st['tif'])

            vmin, vmax, vmean = st['min'], st['max'], st['mean']
            step_int, breaks_int, labels_int = get_arcmap_classes(full_f, vmin, vmax, n_classes, precision=0, unit=unit)
            step_dec, breaks_dec, labels_dec = get_arcmap_classes(full_f, vmin, vmax, n_classes, precision=1, unit=unit)

            u_sym = get_clean_unit_symbol(unit, full_f)
            if u_sym == "°C" or u_sym == "°":
                u_suf = "°"
            elif u_sym == "°C/dec":
                u_suf = " °/dec"
            elif u_sym == "%":
                u_suf = "%"
            elif u_sym:
                u_suf = " " + u_sym
            else:
                u_suf = ""

            r_num = map_idx + 1
            bg_fill = ROW_EVEN_FILL if r_num % 2 == 0 else ROW_WHITE_FILL

            step_dec_val = "{:.2f}".format(step_dec) if (isinstance(step_dec, float) and step_dec < 0.5) else ("{:.1f}".format(step_dec) if isinstance(step_dec, float) else str(step_dec))
            step_int_val = str(step_int)

            row_cells = [
                (1, map_idx, Alignment(horizontal="center", vertical="center"), DATA_FONT_BOLD),
                (2, mod, Alignment(horizontal="left", vertical="center"), DATA_FONT),
                (3, rel_path_str, Alignment(horizontal="left", vertical="center"), CODE_FONT_BOLD),
                (4, full_f, Alignment(horizontal="left", vertical="center"), CODE_FONT_BOLD),
                (5, en_name, Alignment(horizontal="left", vertical="center"), DATA_FONT),
                (6, title_ar, Alignment(horizontal="right", vertical="center"), DATA_FONT_BOLD),
                (7, desc_ar, Alignment(horizontal="right", vertical="center"), DATA_FONT),
                (8, u_sym or unit, Alignment(horizontal="center", vertical="center"), DATA_FONT_BOLD),
                (9, "Equal Interval", Alignment(horizontal="center", vertical="center"), DATA_FONT),
                (10, "{}{}".format(step_int_val, u_suf), Alignment(horizontal="center", vertical="center"), CODE_FONT_BOLD),
                (11, "{}{}".format(step_dec_val, u_suf), Alignment(horizontal="center", vertical="center"), CODE_FONT),
                (12, "{:.2f}{}".format(vmin, u_suf), Alignment(horizontal="center", vertical="center"), CODE_FONT),
                (13, "{:.2f}{}".format(vmax, u_suf), Alignment(horizontal="center", vertical="center"), CODE_FONT_BOLD),
                (14, "{:.2f}{}".format(vmean, u_suf), Alignment(horizontal="center", vertical="center"), CODE_FONT),
            ]

            for ci in range(1, n_classes + 1):
                lbl_i = labels_int[ci - 1]
                lbl_d = labels_dec[ci - 1]
                is_extreme = (ci == 1 or ci == n_classes)
                fnt_i = DATA_FONT_BOLD if is_extreme else DATA_FONT
                fnt_d = CODE_FONT_BOLD if is_extreme else CODE_FONT
                row_cells.append((base_c + (ci - 1) * 2 + 1, lbl_i, Alignment(horizontal="center", vertical="center", wrap_text=True), fnt_i))
                row_cells.append((base_c + (ci - 1) * 2 + 2, lbl_d, Alignment(horizontal="center", vertical="center", wrap_text=True), fnt_d))

            for cidx, val, align, fnt in row_cells:
                cell = ws.cell(r_num, cidx, val)
                cell.alignment = align
                cell.font = fnt
                cell.fill = bg_fill
                cell.border = THIN_BORDER
            ws.row_dimensions[r_num].height = 26

    # Build classification sheets (3, 5, 7, 9 classes)
    build_class_sheet(wb, "04_تصنيف_3_فئات_Classes_3", 3, "المعيار التنفيذي")
    build_class_sheet(wb, "05_تصنيف_5_فئات_Classes_5", 5, "المعيار الذهبي القياسي")
    build_class_sheet(wb, "06_تصنيف_7_فئات_Classes_7", 7, "المعيار الأكاديمي التفصيلي")
    build_class_sheet(wb, "07_تصنيف_9_فئات_Classes_9", 9, "المعيار المكثف للمدى الواسع")

    # 1. Save primary copy to target_excel (typically 00_Tables_And_Reports\Climate_Atlas_Classification_Guide.xlsx)
    os.makedirs(os.path.dirname(target_excel), exist_ok=True)
    wb.save(target_excel)
    print("Successfully generated Climate Atlas Classification Guide: " + str(target_excel))

    # 2. Save root copy directly to base_dir (Root Output Workspace)
    root_copy = os.path.join(base_dir, "Climate_Atlas_Classification_Guide.xlsx")
    try:
        shutil.copy2(target_excel, root_copy)
        print("Successfully saved root workspace copy: " + str(root_copy))
    except Exception as ex_rc:
        try:
            wb.save(root_copy)
            print("Successfully saved direct root copy: " + str(root_copy))
        except Exception:
            pass

    return target_excel

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_args", default=None)
    parser.add_argument("--base_dir", default=None)
    parser.add_argument("--study_area", default="Egypt")
    parser.add_argument("--target_excel", default=None)
    args = parser.parse_args()
    if args.json_args and os.path.exists(args.json_args):
        with open(args.json_args, "r") as jf:
            data = json.load(jf)
        build_master_classification_workbook(
            base_dir=data.get("base_dir"),
            study_area_name=data.get("study_area_name", "Egypt"),
            target_excel=data.get("target_excel"),
            spatial_info=data.get("spatial_info"),
            tech_info=data.get("tech_info"),
            raster_stats=data.get("raster_stats")
        )
    else:
        build_master_classification_workbook(base_dir=args.base_dir, study_area_name=args.study_area, target_excel=args.target_excel)

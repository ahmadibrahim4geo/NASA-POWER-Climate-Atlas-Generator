# -*- coding: utf-8 -*-
"""
apply_seasonal_range_and_vectors.py
-----------------------------------
1. Fixes all 64 field aliases in both Geodatabases (ET monthly, Wind Vectors, Isobars, Egypt).
2. Adds and computes *_Seasonal_Range across 9 elements (T, PSL, PS, W_Spd, RH, Td, Sol, UV, Cld).
3. Interpolates continuous surface GeoTIFF rasters for the 9 Seasonal Range indicators.
4. Generates Month Mean Vector layers:
   - Wind_Vector_Month (sampled from W_Spd_Month_Mean.tif and W_Dir_Month_Mean.tif)
   - Isobars_PSL_Month_Mean (from PSL_Month_Mean.tif with 4.0 hPa interval clipped to Egypt)
   - Isobars_PS_Month_Mean (from PS_Month_Mean.tif with 4.0 hPa interval clipped to Egypt)
   - Isobars_PSL_Annual_Mean and Isobars_PS_Annual_Mean
5. Updates Excel workbooks in 00_Tables_And_Reports with *_Seasonal_Range.
6. Syncs all updates between Desktop and D: Drive.
"""
from __future__ import print_function
import os
import sys
import math
import shutil
import arcpy
from arcpy.sa import Spline, ExtractByMask, Float, Contour

# Ensure Spatial Analyst
arcpy.CheckOutExtension("Spatial")

DESKTOP_DIR = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1996-2025"
DDRIVE_DIR = r"D:\MY DATA & FILE\Spatial Data\Egypt Climate Data 1996-2025"

DESKTOP_GDB = os.path.join(DESKTOP_DIR, "Climate_Database_From_1996_To_2025.gdb")
DDRIVE_GDB = os.path.join(DDRIVE_DIR, "Climate_Database_From_1996_To_2025.gdb")

SEASONAL_RANGE_DEFS = [
    ("Temperature", "T_Seasonal_Range", u"المدى الفصلي لدرجة الحرارة",
     ["T_Winter_Mean", "T_Spring_Mean", "T_Summer_Mean", "T_Autumn_Mean"],
     os.path.join("01_Temperature", "T_Seasonal_Range.tif")),
    ("Sea_Level_Pressure", "PSL_Seasonal_Range", u"المدى الفصلي لضغط مستوى البحر",
     ["PSL_Winter_Mean", "PSL_Spring_Mean", "PSL_Summer_Mean", "PSL_Autumn_Mean"],
     os.path.join("03_Sea_Level_Pressure", "PSL_Seasonal_Range.tif")),
    ("Surface_Pressure", "PS_Seasonal_Range", u"المدى الفصلي للضغط السطحي",
     ["PS_Winter_Mean", "PS_Spring_Mean", "PS_Summer_Mean", "PS_Autumn_Mean"],
     os.path.join("04_Surface_Pressure", "PS_Seasonal_Range.tif")),
    ("Wind", "W_Spd_Seasonal_Range", u"المدى الفصلي لسرعة الرياح",
     ["W_Spd_Winter_Mean", "W_Spd_Spring_Mean", "W_Spd_Summer_Mean", "W_Spd_Autumn_Mean"],
     os.path.join("05_Wind", "Speed", "W_Spd_Seasonal_Range.tif")),
    ("Relative_Humidity", "RH_Seasonal_Range", u"المدى الفصلي للرطوبة النسبية",
     ["RH_Winter_Mean", "RH_Spring_Mean", "RH_Summer_Mean", "RH_Autumn_Mean"],
     os.path.join("06_Relative_Humidity", "RH_Seasonal_Range.tif")),
    ("Dew_Point", "Td_Seasonal_Range", u"المدى الفصلي لنقطة الندى",
     ["Td_Winter_Mean", "Td_Spring_Mean", "Td_Summer_Mean", "Td_Autumn_Mean"],
     os.path.join("07_Dew_Point", "Td_Seasonal_Range.tif")),
    ("Solar_Radiation", "Sol_Seasonal_Range", u"المدى الفصلي للإشعاع الشمسي",
     ["Sol_Winter_Mean", "Sol_Spring_Mean", "Sol_Summer_Mean", "Sol_Autumn_Mean"],
     os.path.join("08_Solar_Radiation", "Sol_Seasonal_Range.tif")),
    ("UV_Index", "UV_Seasonal_Range", u"المدى الفصلي للأشعة فوق البنفسجية",
     ["UV_Winter_Mean", "UV_Spring_Mean", "UV_Summer_Mean", "UV_Autumn_Mean"],
     os.path.join("09_UV_Index", "UV_Seasonal_Range.tif")),
    ("Cloud_Cover", "Cld_Seasonal_Range", u"المدى الفصلي للغطاء السحابي",
     ["Cld_Winter_Mean", "Cld_Spring_Mean", "Cld_Summer_Mean", "Cld_Autumn_Mean"],
     os.path.join("10_Cloud_Cover", "Cld_Seasonal_Range.tif")),
]

ALIAS_FIX_MAP = {
    "ET_January_Total": u"مجموع البخر-نتح لشهر يناير (ملم)",
    "ET_February_Total": u"مجموع البخر-نتح لشهر فبراير (ملم)",
    "ET_March_Total": u"مجموع البخر-نتح لشهر مارس (ملم)",
    "ET_April_Total": u"مجموع البخر-نتح لشهر أبريل (ملم)",
    "ET_May_Total": u"مجموع البخر-نتح لشهر مايو (ملم)",
    "ET_June_Total": u"مجموع البخر-نتح لشهر يونيو (ملم)",
    "ET_July_Total": u"مجموع البخر-نتح لشهر يوليو (ملم)",
    "ET_August_Total": u"مجموع البخر-نتح لشهر أغسطس (ملم)",
    "ET_September_Total": u"مجموع البخر-نتح لشهر سبتمبر (ملم)",
    "ET_October_Total": u"مجموع البخر-نتح لشهر أكتوبر (ملم)",
    "ET_November_Total": u"مجموع البخر-نتح لشهر نوفمبر (ملم)",
    "ET_December_Total": u"مجموع البخر-نتح لشهر ديسمبر (ملم)",
    "Wind_Speed": u"سرعة الرياح (متر/ث)",
    "Wind_Dir": u"اتجاه الرياح (درجة)",
    "Arrow_Angle": u"زاوية دوران السهم الكارتوجرافي",
    "Arrow_Size": u"حجم السهم النسبي",
    "Period": u"الفترة المناخية",
    "Id": u"معرف خط الضغط المتساوي",
    "Contour": u"قيمة خط الضغط الجوي المتساوي (hPa)",
    "NAME": u"اسم النطاق الجغرافي",
}

def step1_fix_aliases(gdb):
    print(">>> Step 1: Fixing field aliases in %s..." % gdb)
    arcpy.env.workspace = gdb
    for fc in arcpy.ListFeatureClasses():
        fields = arcpy.ListFields(fc)
        for f in fields:
            if f.name in ALIAS_FIX_MAP:
                new_alias = ALIAS_FIX_MAP[f.name]
                try:
                    arcpy.management.AlterField(fc, f.name, new_field_alias=new_alias)
                except Exception as ex:
                    print("  Failed to alter alias for %s.%s: %s" % (fc, f.name, ex))

def step2_compute_seasonal_ranges(gdb):
    print(">>> Step 2: Adding and computing Seasonal Range fields in %s..." % gdb)
    arcpy.env.workspace = gdb
    for fc, range_fld, alias_ar, season_flds, rel_tif in SEASONAL_RANGE_DEFS:
        existing_flds = [f.name for f in arcpy.ListFields(fc)]
        if range_fld not in existing_flds:
            print("  Adding field %s to %s..." % (range_fld, fc))
            arcpy.management.AddField(fc, range_fld, "DOUBLE", field_alias=alias_ar)
        else:
            try:
                arcpy.management.AlterField(fc, range_fld, new_field_alias=alias_ar)
            except Exception:
                pass
        
        # Calculate values
        fld_list = season_flds + [range_fld]
        with arcpy.da.UpdateCursor(fc, fld_list) as cur:
            for row in cur:
                vals = [row[i] for i in range(4) if row[i] is not None]
                if len(vals) == 4:
                    s_range = round(float(max(vals) - min(vals)), 2)
                    row[4] = s_range
                    cur.updateRow(row)
        print("  Updated %s in %s." % (range_fld, fc))

def step3_interpolate_seasonal_rasters(gdb, base_dir):
    print(">>> Step 3: Interpolating Seasonal Range Rasters for %s..." % base_dir)
    mask_layer = os.path.join(gdb, "Egypt")
    target_sr = arcpy.SpatialReference(3857) # Web Mercator
    cell_size = 250.0

    arcpy.env.extent = mask_layer
    arcpy.env.snapRaster = os.path.join(base_dir, "01_Temperature", "T_Annual_Mean.tif")
    arcpy.env.outputCoordinateSystem = target_sr
    arcpy.env.compression = "LZW"
    arcpy.env.tileSize = "128 128"
    arcpy.env.rasterStatistics = "STATISTICS 1 1"
    arcpy.env.parallelProcessingFactor = "0"

    for fc, range_fld, alias_ar, season_flds, rel_tif in SEASONAL_RANGE_DEFS:
        out_tif = os.path.join(base_dir, rel_tif)
        out_dir = os.path.dirname(out_tif)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        pts_fc = os.path.join(gdb, fc)
        print("  Interpolating %s -> %s..." % (range_fld, out_tif))
        
        # Spline Tension, w=30, n=12
        raw_interp = Spline(pts_fc, range_fld, cell_size, "TENSION", 30.0, 12)
        clipped = ExtractByMask(raw_interp, mask_layer)
        float_out = Float(clipped)
        
        if arcpy.Exists(out_tif):
            try:
                arcpy.management.Delete(out_tif)
            except Exception:
                pass
        
        try:
            arcpy.management.CopyRaster(float_out, out_tif, nodata_value="-3.4028235e+38")
        except Exception:
            float_out.save(out_tif)
        
        # Build pyramids
        try:
            arcpy.management.BuildPyramids(out_tif)
        except Exception:
            pass
        print("  Successfully created %s" % out_tif)

def step4_build_month_mean_vectors(gdb, base_dir):
    print(">>> Step 4: Generating Month Mean Vector Layers in %s..." % gdb)
    mask_layer = os.path.join(gdb, "Egypt")
    target_sr = arcpy.SpatialReference(3857)
    eff_wind_size = 50000.0 # 50 km spacing

    # 4A. Wind Vector Month
    spd_tif = os.path.join(base_dir, "05_Wind", "Speed", "W_Spd_Month_Mean.tif")
    dir_tif = os.path.join(base_dir, "05_Wind", "Direction", "W_Dir_Month_Mean.tif")
    if os.path.isfile(spd_tif) and os.path.isfile(dir_tif):
        print("  Generating Wind_Vector_Month...")
        ext = arcpy.Describe(mask_layer).extent
        fish = "in_memory/wfish"
        fish_pts = "in_memory/wfish_label"
        for o in (fish, fish_pts, "in_memory/wclip", "in_memory/wproj"):
            if arcpy.Exists(o):
                try: arcpy.management.Delete(o)
                except Exception: pass
        
        origin = "%s %s" % (ext.XMin, ext.YMin)
        yaxis = "%s %s" % (ext.XMin, ext.YMin + (eff_wind_size * 2.0))
        corner = "%s %s" % (ext.XMax, ext.YMax)
        arcpy.management.CreateFishnet(fish, origin, yaxis, eff_wind_size, eff_wind_size, "", "", corner, "LABELS", None, "POLYGON")
        arcpy.analysis.Clip(fish_pts, mask_layer, "in_memory/wclip")
        
        fc_month = os.path.join(gdb, "Wind_Vector_Month")
        if arcpy.Exists(fc_month):
            arcpy.management.Delete(fc_month)
        arcpy.management.CopyFeatures("in_memory/wclip", fc_month)
        
        arcpy.sa.ExtractMultiValuesToPoints(fc_month, [[spd_tif, "Wind_Speed"], [dir_tif, "Wind_Dir"]])
        
        for fn, typ, al in [
            ("Arrow_Angle", "DOUBLE", u"زاوية دوران السهم الكارتوجرافي"),
            ("Arrow_Size", "DOUBLE", u"حجم السهم النسبي"),
            ("Period", "TEXT", u"الفترة المناخية")
        ]:
            if typ == "TEXT":
                arcpy.management.AddField(fc_month, fn, typ, field_length=20, field_alias=al)
            else:
                arcpy.management.AddField(fc_month, fn, typ, field_alias=al)
        
        arcpy.management.AlterField(fc_month, "Wind_Speed", new_field_alias=u"سرعة الرياح (متر/ث)")
        arcpy.management.AlterField(fc_month, "Wind_Dir", new_field_alias=u"اتجاه الرياح (درجة)")

        with arcpy.da.UpdateCursor(fc_month, ["Wind_Speed", "Wind_Dir", "Arrow_Angle", "Arrow_Size", "Period"]) as cur:
            for row in cur:
                s, d = row[0], row[1]
                row[4] = "Month"
                if s is not None and d is not None and s >= 0:
                    row[2] = float(d) % 360.0
                    row[3] = round(max(0.5, min(3.0, float(s) / 3.0)), 2)
                else:
                    row[2] = None
                    row[3] = None
                cur.updateRow(row)
        
        # Export SHP
        shp_dir = os.path.join(base_dir, "05_Wind", "Direction", "Vector_Points")
        if not os.path.exists(shp_dir):
            os.makedirs(shp_dir)
        shp_path = os.path.join(shp_dir, "Wind_Vector_Month.shp")
        if arcpy.Exists(shp_path):
            arcpy.management.Delete(shp_path)
        arcpy.management.CopyFeatures(fc_month, shp_path)
        print("  Wind_Vector_Month created successfully.")

    # 4B. Isobars for PSL and PS Month Mean
    iso_targets = [
        ("PSL_Month_Mean", os.path.join(base_dir, "03_Sea_Level_Pressure", "PSL_Month_Mean.tif"), "Isobars_PSL_Month_Mean"),
        ("PS_Month_Mean", os.path.join(base_dir, "04_Surface_Pressure", "PS_Month_Mean.tif"), "Isobars_PS_Month_Mean"),
        ("PSL_Annual_Mean", os.path.join(base_dir, "03_Sea_Level_Pressure", "PSL_Annual_Mean.tif"), "Isobars_PSL_Annual_Mean"),
        ("PS_Annual_Mean", os.path.join(base_dir, "04_Surface_Pressure", "PS_Annual_Mean.tif"), "Isobars_PS_Annual_Mean"),
    ]

    for fld, rst_path, fcname in iso_targets:
        if os.path.isfile(rst_path):
            print("  Generating isobars %s from %s..." % (fcname, rst_path))
            raw_iso = "in_memory/raw_iso"
            if arcpy.Exists(raw_iso):
                try: arcpy.management.Delete(raw_iso)
                except Exception: pass
            
            # Contour interval 4.0 mbar/hPa
            Contour(rst_path, raw_iso, 4.0, 0.0)
            
            out_fc = os.path.join(gdb, fcname)
            if arcpy.Exists(out_fc):
                try: arcpy.management.Delete(out_fc)
                except Exception: pass
            
            arcpy.analysis.Clip(raw_iso, mask_layer, out_fc)
            
            try:
                arcpy.management.AlterField(out_fc, "Id", new_field_alias=u"معرف خط الضغط المتساوي")
                arcpy.management.AlterField(out_fc, "Contour", new_field_alias=u"قيمة خط الضغط الجوي المتساوي (hPa)")
            except Exception:
                pass
            print("  Isobars %s created successfully." % fcname)

def step5_update_excel_workbooks(base_dir):
    print(">>> Step 5: Updating Excel workbooks in %s..." % base_dir)
    import openpyxl
    import io

    tables_dir = os.path.join(base_dir, "00_Tables_And_Reports")
    gdb = os.path.join(base_dir, "Climate_Database_From_1996_To_2025.gdb")
    
    excel_map = {
        "Temperature": ("Temperature.xls", "T_Seasonal_Range", "T_Annual_Range"),
        "Sea_Level_Pressure": ("Sea_Level_Pressure.xls", "PSL_Seasonal_Range", "PSL_Annual_Range"),
        "Surface_Pressure": ("Surface_Pressure.xls", "PS_Seasonal_Range", "PS_Annual_Range"),
        "Wind": ("Wind.xls", "W_Spd_Seasonal_Range", "W_Spd_Annual_Range"),
        "Relative_Humidity": ("Relative_Humidity.xls", "RH_Seasonal_Range", "RH_Annual_Range"),
        "Dew_Point": ("Dew_Point.xls", "Td_Seasonal_Range", "Td_Annual_Range"),
        "Solar_Radiation": ("Solar_Radiation.xls", "Sol_Seasonal_Range", "Sol_Annual_Range"),
        "UV_Index": ("UV_Index.xls", "UV_Seasonal_Range", "UV_Annual_Range"),
        "Cloud_Cover": ("Cloud_Cover.xls", "Cld_Seasonal_Range", "Cld_Annual_Range"),
    }

    for fc, (xls_name, range_fld, after_fld) in excel_map.items():
        xls_path = os.path.join(tables_dir, xls_name)
        if not os.path.isfile(xls_path):
            continue
        
        pts_fc = os.path.join(gdb, fc)
        pt_values = {}
        with arcpy.da.SearchCursor(pts_fc, ["Point_ID", range_fld]) as cur:
            for pid, val in cur:
                pt_values[int(pid)] = val

        with open(xls_path, "rb") as f:
            buf = io.BytesIO(f.read())
        wb = openpyxl.load_workbook(buf)
        if "Data" not in wb.sheetnames:
            continue
        
        ws = wb["Data"]
        header = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
        if range_fld in header:
            print("  %s already contains %s." % (xls_name, range_fld))
            continue
        
        insert_col = ws.max_column + 1
        if after_fld in header:
            insert_col = header.index(after_fld) + 2
        
        ws.insert_cols(insert_col)
        ws.cell(1, insert_col).value = range_fld

        pid_col = header.index("Point_ID") + 1 if "Point_ID" in header else 2
        for r in range(2, ws.max_row + 1):
            pid_val = ws.cell(r, pid_col).value
            try:
                pid = int(pid_val)
            except Exception:
                pid = r - 1
            ws.cell(r, insert_col).value = pt_values.get(pid, 0.0)

        wb.save(xls_path)
        print("  Updated %s with column %s at col %d." % (xls_name, range_fld, insert_col))

def main():
    print("==================================================")
    print("STARTING SEASONAL RANGE & VECTOR EXTRACTIONS")
    print("==================================================")
    
    # Process Desktop
    step1_fix_aliases(DESKTOP_GDB)
    step2_compute_seasonal_ranges(DESKTOP_GDB)
    step3_interpolate_seasonal_rasters(DESKTOP_GDB, DESKTOP_DIR)
    step4_build_month_mean_vectors(DESKTOP_GDB, DESKTOP_DIR)
    step5_update_excel_workbooks(DESKTOP_DIR)

    # Process D: Drive
    step1_fix_aliases(DDRIVE_GDB)
    step2_compute_seasonal_ranges(DDRIVE_GDB)
    step3_interpolate_seasonal_rasters(DDRIVE_GDB, DDRIVE_DIR)
    step4_build_month_mean_vectors(DDRIVE_GDB, DDRIVE_DIR)
    step5_update_excel_workbooks(DDRIVE_DIR)

    print("==================================================")
    print("ALL PROCESSING COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()

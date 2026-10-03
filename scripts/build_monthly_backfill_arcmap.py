# -*- coding: utf-8 -*-
"""
Monthly Climatology Backfill — ArcMap 10.x (Python 2.7 + arcpy).

Fills the missing Month/ rasters for an existing atlas workspace WITHOUT
re-downloading anything. MODE 2 first injects any missing 12 monthly fields
(*_January_Mean ... *_December_Mean) into the GDB point layers from
00_Tables_And_Reports/Monthly_Climatology/*.csv (join on Source_ID, alias =
field name), then interpolates them with the SAME settings recorded in the
atlas Processing_Log:

  Method .... Spline (Tension, weight=30, points=12)
  Cell ...... 250 m | Wind vector spacing 50000 m | Isobars 2 mbar
  Output .... LZW, 128x128 tiles, statistics + pyramids
  Direction . circular U/V (sin/cos + atan2), never linear

Rules (per user requirements):
  * Alias of every created field = the field name itself (Latin).
  * Monthly rasters go to <element>/Month/ (Wind: Speed/Month, Direction/Month).
  * One unified color stretch per element (global min/max over 12 months),
    stored in Month/<element>_monthly_stretch.json + optional _cls display.
  * Wind_Vector_Month is sampled from the W_*_Month_Mean rasters.
  * PSL/PS Month isobars are contoured from the PSL/PS_Month_Mean rasters.
  * Elements whose 12 Month/ rasters already exist are SKIPPED untouched.

If a monthly CSV is unavailable for an element, this script reports it and
the tool itself (with "Generate Monthly Climatology Rasters" checked,
period >= 2 years) remains the reference path.

Run inside ArcMap Python window or:
  C:\\Python27\\ArcGIS10.8\\python.exe build_monthly_backfill_arcmap.py
"""

import os
import sys
import json
import math
import time

try:
    import arcpy
    from arcpy.sa import ExtractByMask
    arcpy.CheckOutExtension("Spatial")
except Exception as ex:
    raise SystemExit("arcpy/Spatial Analyst required (run inside ArcMap): %s" % ex)

# ============================== CONFIG ======================================
OUT_WS = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1996-2025"
GDB_NAME = "Climate_Database_From_1996_To_2025.gdb"
MASK = ""  # "" = auto-detect Egypt mask under OUT_WS\_scratch\maskp.shp
CELL = 250.0
WIND_CELL = 50000.0
SPLINE_WEIGHT = 30.0
SPLINE_NPOINTS = 12
ISOBAR_STEP = 2.0
BUILD_DISPLAY = False   # True = extra unified _cls display rasters (atlas default OFF)
NCLASS = 7
OVERWRITE = False       # False = skip elements whose 12 Month/ rasters exist
MONTH_CSV_DIR = os.path.join(OUT_WS, "00_Tables_And_Reports", "Monthly_Climatology")
CSV_BY_MODULE = {
    "Temperature": "Temperature.csv", "Precipitation": "Precipitation.csv",
    "Sea Level Pressure": "Sea_Level_Pressure.csv", "Surface Pressure": "Surface_Pressure.csv",
    "Wind": "Wind.csv", "Relative Humidity": "Relative_Humidity.csv",
    "Dew Point": "Dew_Point.csv", "Solar Radiation": "Solar_Radiation.csv",
    "UV Index": "UV_Index.csv", "Cloud Cover": "Cloud_Cover.csv",
    "Evapotranspiration": "Evapotranspiration.csv",
}
# ============================================================================

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# module -> (gdb_fc, out_folder, [(field_prefix, is_direction)])
MODULES = {
    "Temperature": ("Temperature", "01_Temperature", [("T", False)]),
    "Precipitation": ("Precipitation", "02_Precipitation", [("R", False)]),
    "Sea Level Pressure": ("Sea_Level_Pressure", "03_Sea_Level_Pressure", [("PSL", False)]),
    "Surface Pressure": ("Surface_Pressure", "04_Surface_Pressure", [("PS", False)]),
    "Wind": ("Wind", "05_Wind", [("W_Spd", False), ("W_Dir", True)]),
    "Relative Humidity": ("Relative_Humidity", "06_Relative_Humidity", [("RH", False)]),
    "Dew Point": ("Dew_Point", "07_Dew_Point", [("Td", False)]),
    "Solar Radiation": ("Solar_Radiation", "08_Solar_Radiation", [("Sol", False)]),
    "UV Index": ("UV_Index", "09_UV_Index", [("UV", False)]),
    "Cloud Cover": ("Cloud_Cover", "10_Cloud_Cover", [("Cld", False)]),
}

COLORS = {
    "Temperature": ["#4575B4", "#74ADD1", "#ABD9E9", "#FFFFBF", "#FDAE61", "#F46D43", "#D73027"],
    "Precipitation": ["#8C510A", "#D8B365", "#F6E8C3", "#C7EAE5", "#80CDC1", "#35978F", "#01665E"],
    "Sea Level Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Surface Pressure": ["#762A83", "#9970AB", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#5AAE61", "#1B7837"],
    "Wind_Speed": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"],
    "Wind_Direction": ["#F7F7F7", "#D9D9D9", "#BDBDBD", "#969696", "#737373", "#525252", "#252525"],
    "Relative Humidity": ["#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"],
    "Dew Point": ["#FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"],
    "Solar Radiation": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#BD0026"],
    "UV Index": ["#299500", "#F7E400", "#F85900", "#D8001D", "#6B499D"],
    "Cloud Cover": ["#F7FBFF", "#DEEBF7", "#C6DBEF", "#9ECAE1", "#4292C6", "#2171B5", "#084594"],
}


def msg(t):
    print(t)
    sys.stdout.flush()


def month_fields(prefix):
    return ["%s_%s_Mean" % (prefix, m) for m in MONTHS]


def interp_surface(lyr, field):
    from arcpy.sa import Spline
    return Spline(lyr, field, CELL, "TENSION", SPLINE_WEIGHT, SPLINE_NPOINTS)


def interp_direction_uv(src_fc, dir_field):
    """Mirror of PowerClimateAtlasGenerator._interp_direction_uv (Spline)."""
    tmp_fc, lyr_s, lyr_c = "in_memory/bk_uv", "bk_sin", "bk_cos"
    for o in (tmp_fc, lyr_s, lyr_c):
        try:
            arcpy.management.Delete(o)
        except Exception:
            pass
    arcpy.management.CopyFeatures(src_fc, tmp_fc)
    for _fn in ("TMP_SIN", "TMP_COS"):
        try:
            arcpy.management.AddField(tmp_fc, _fn, "DOUBLE")
        except Exception:
            pass
    n_valid = 0
    with arcpy.da.UpdateCursor(tmp_fc, [dir_field, "TMP_SIN", "TMP_COS"]) as cur:
        for row in cur:
            try:
                if row[0] is None:
                    row[1], row[2] = None, None
                else:
                    r = math.radians(float(row[0]) % 360.0)
                    row[1], row[2] = math.sin(r), math.cos(r)
                    n_valid += 1
            except Exception:
                row[1], row[2] = None, None
            cur.updateRow(row)
    if n_valid < 3:
        raise RuntimeError("only %d valid direction points" % n_valid)
    arcpy.management.MakeFeatureLayer(tmp_fc, lyr_s, "TMP_SIN IS NOT NULL")
    arcpy.management.MakeFeatureLayer(tmp_fc, lyr_c, "TMP_COS IS NOT NULL")
    from arcpy.sa import ATan2, Con
    sin_r = interp_surface(lyr_s, "TMP_SIN")
    cos_r = interp_surface(lyr_c, "TMP_COS")
    rad = ATan2(sin_r, cos_r)
    deg = rad * 57.29577951308232
    return Con(deg < 0, deg + 360.0, deg)


def save_raster(src_raster, out_tif, mask):
    from arcpy.sa import ExtractByMask
    if mask and arcpy.Exists(mask):
        try:
            clipped = ExtractByMask(src_raster, mask)
        except Exception:
            clipped = src_raster
    else:
        clipped = src_raster
    if os.path.exists(out_tif):
        try:
            arcpy.management.Delete(out_tif)
        except Exception:
            pass
    arcpy.management.CopyRaster(clipped, out_tif, nodata_value="-3.4028235e+38")
    try:
        arcpy.management.CalculateStatistics(out_tif)
    except Exception:
        pass
    try:
        arcpy.management.BuildPyramids(out_tif, "-1", "BILINEAR", "DEFAULT", "75")
    except Exception as ex:
        msg("    pyramid warning: %s" % ex)


def inject_monthly_fields(gdb):
    """MODE 2: add missing 12 monthly fields to each GDB point layer and fill
    them from Monthly_Climatology/*.csv (join on Source_ID).

    Alias of every created field = the field name itself (Latin). Existing
    values are never overwritten: only NULLs are filled."""
    import csv as _csv
    for module, (fc_short, _folder, prefixes) in MODULES.items():
        fc = os.path.join(gdb, fc_short)
        if not arcpy.Exists(fc):
            continue
        have = set(f.name for f in arcpy.ListFields(fc))
        wanted = []
        for prefix, _is_dir in prefixes:
            wanted.extend(month_fields(prefix))
        missing = [f for f in wanted if f not in have]
        csv_path = os.path.join(MONTH_CSV_DIR, CSV_BY_MODULE.get(module, ""))
        if not missing:
            continue
        if not csv_path or not os.path.exists(csv_path):
            msg("[%s] fields %s missing and no CSV available - skipped." % (module, missing[0]))
            continue
        for fld in missing:
            try:
                arcpy.management.AddField(fc, fld, "DOUBLE", field_alias=fld)
            except Exception as ex:
                msg("[%s] AddField %s failed: %s" % (module, fld, ex))
        table = {}
        with open(csv_path, "r") as fh:
            rd = _csv.DictReader(fh)
            for row in rd:
                try:
                    sid = int(float(row["Source_ID"]))
                except Exception:
                    continue
                table[sid] = row
        cur_fields = ["Source_ID"] + missing
        n_fill = 0
        try:
            with arcpy.da.UpdateCursor(fc, cur_fields) as cur:
                for row in cur:
                    try:
                        sid = int(row[0])
                    except Exception:
                        continue
                    rec = table.get(sid)
                    if not rec:
                        continue
                    dirty = False
                    for i, fld in enumerate(missing, 1):
                        if row[i] is None:
                            try:
                                v = rec.get(fld)
                                row[i] = float(v) if v not in (None, "") else None
                                dirty = True
                            except Exception:
                                pass
                    if dirty:
                        cur.updateRow(row)
                        n_fill += 1
        except Exception as ex:
            msg("[%s] fill failed: %s" % (module, ex))
            continue
        msg("[%s] injected %d monthly fields (%d rows filled, alias=field name)." % (module, len(missing), n_fill))


def main():
    t0 = time.time()
    gdb = os.path.join(OUT_WS, GDB_NAME)
    mask = MASK
    if not mask:
        cand = os.path.join(OUT_WS, "_scratch", "maskp.shp")
        if os.path.exists(cand):
            mask = cand
    arcpy.env.overwriteOutput = True
    arcpy.env.compression = "LZW"
    arcpy.env.tileSize = "128 128"
    arcpy.env.parallelProcessingFactor = "0"
    arcpy.env.scratchWorkspace = os.path.join(OUT_WS, "_scratch")
    if mask and arcpy.Exists(mask):
        arcpy.env.extent = mask

    # MODE 2: inject the 12 monthly fields into the GDB layers from CSVs.
    inject_monthly_fields(gdb)

    # Small repair: pyramids missing on two seasonal rasters.
    for _fix in [os.path.join(OUT_WS, "02_Precipitation", "R_Seasonal_Range.tif"),
                 os.path.join(OUT_WS, "14_Evapotranspiration", "ET_Seasonal_Range.tif")]:
        if os.path.exists(_fix) and not os.path.exists(_fix + ".ovr"):
            try:
                arcpy.management.BuildPyramids(_fix, "-1", "BILINEAR", "DEFAULT", "75")
                msg("Pyramids built: %s" % os.path.basename(_fix))
            except Exception as ex:
                msg("Pyramid failed %s: %s" % (_fix, ex))

    for module, (fc_short, folder, prefixes) in MODULES.items():
        fc = os.path.join(gdb, fc_short)
        if not arcpy.Exists(fc):
            msg("[%s] point layer missing, skipped." % module)
            continue
        have = set(f.name for f in arcpy.ListFields(fc))
        targets = []  # (field, out_tif, is_dir)
        for prefix, is_dir in prefixes:
            sub = os.path.join(folder, "Speed" if prefix == "W_Spd" else
                               ("Direction" if prefix == "W_Dir" else ""))
            mdir = os.path.join(OUT_WS, sub, "Month")
            if not os.path.isdir(mdir):
                os.makedirs(mdir)
            for fld in month_fields(prefix):
                targets.append((fld, os.path.join(mdir, fld + ".tif"), is_dir))
        missing = [f for f, _p, _d in targets if f not in have]
        if missing:
            msg("[%s] %d/12 monthly FIELDS missing in GDB (e.g. %s)." % (module, len(missing), missing[0]))
            msg("  -> re-run the atlas tool with 'Generate Monthly Climatology Rasters' checked (period >= 2 yrs).")
            continue
        done = [p for _f, p, _d in targets if os.path.exists(p)]
        if len(done) == len(targets) and not OVERWRITE:
            msg("[%s] Month/ complete (%d rasters) - skipped." % (module, len(done)))
            continue
        # Unified stretch from point data (global min/max over 12 months).
        gmin, gmax = None, None
        try:
            with arcpy.da.SearchCursor(fc, [f for f, _p, _d in targets]) as cur:
                for row in cur:
                    for v in row:
                        if v is None:
                            continue
                        try:
                            fv = float(v)
                        except Exception:
                            continue
                        if gmin is None or fv < gmin:
                            gmin = fv
                        if gmax is None or fv > gmax:
                            gmax = fv
        except Exception as ex:
            msg("[%s] stretch scan failed: %s" % (module, ex))
        msg("[%s] interpolating %d monthly rasters (stretch %.4g..%.4g)..." % (module, len(targets), gmin, gmax))
        with open(os.path.join(os.path.dirname(targets[0][1]),
                               "%s_monthly_stretch.json" % fc_short), "w") as fh:
            json.dump({"element": module, "min": gmin, "max": gmax,
                       "method": "Spline(Tension,w=%s,n=%s)" % (SPLINE_WEIGHT, SPLINE_NPOINTS),
                       "cell": CELL}, fh, indent=2)
        for fld, out_tif, is_dir in targets:
            if os.path.exists(out_tif) and not OVERWRITE:
                continue
            lyr = "bk_interp"
            try:
                arcpy.management.Delete(lyr)
            except Exception:
                pass
            arcpy.management.MakeFeatureLayer(fc, lyr, "%s IS NOT NULL" % arcpy.AddFieldDelimiters(fc, fld))
            try:
                surf = interp_direction_uv(fc, fld) if is_dir else interp_surface(lyr, fld)
            except Exception as ex:
                msg("    %s FAILED: %s" % (fld, ex))
                continue
            save_raster(surf, out_tif, mask)
            try:
                del surf
            except Exception:
                pass
            try:
                arcpy.management.Delete(lyr)
            except Exception:
                pass
            msg("    [OK] %s" % os.path.basename(out_tif))

    # Wind_Vector_Month from the *_Month_Mean rasters (never from annual).
    try:
        spd_r = os.path.join(OUT_WS, "05_Wind", "Speed", "W_Spd_Month_Mean.tif")
        dir_r = os.path.join(OUT_WS, "05_Wind", "Direction", "W_Dir_Month_Mean.tif")
        if os.path.exists(spd_r) and os.path.exists(dir_r) and mask and arcpy.Exists(mask):
            ext = arcpy.Describe(mask).extent
            fish, fish_pts = "in_memory/bk_fish", "in_memory/bk_fish_label"
            for o in (fish, fish_pts):
                try:
                    arcpy.management.Delete(o)
                except Exception:
                    pass
            arcpy.management.CreateFishnet(fish, "%s %s" % (ext.XMin, ext.YMin),
                                           "%s %s" % (ext.XMin, ext.YMin + 10),
                                           WIND_CELL, WIND_CELL, "", "",
                                           "%s %s" % (ext.XMax, ext.YMax),
                                           "LABELS", None, "POLYGON")
            arcpy.analysis.Clip(fish_pts, mask, "in_memory/bk_clip")
            out_fc = os.path.join(gdb, "Wind_Vector_Month")
            if arcpy.Exists(out_fc):
                arcpy.management.Delete(out_fc)
            arcpy.management.CopyFeatures("in_memory/bk_clip", out_fc)
            arcpy.sa.ExtractMultiValuesToPoints(out_fc, [[spd_r, "Wind_Speed"], [dir_r, "Wind_Dir"]])
            for fn, typ in [("Arrow_Angle", "DOUBLE"), ("Arrow_Size", "DOUBLE"), ("Period", "TEXT")]:
                try:
                    if typ == "TEXT":
                        arcpy.management.AddField(out_fc, fn, typ, field_length=20, field_alias=fn)
                    else:
                        arcpy.management.AddField(out_fc, fn, typ, field_alias=fn)
                except Exception:
                    pass
            with arcpy.da.UpdateCursor(out_fc, ["Wind_Dir", "Wind_Speed", "Arrow_Angle", "Arrow_Size", "Period"]) as cur:
                for row in cur:
                    try:
                        row[2] = (float(row[0]) + 180.0) % 360.0 if row[0] is not None else None
                    except Exception:
                        row[2] = None
                    try:
                        row[3] = float(row[1]) if row[1] is not None else None
                    except Exception:
                        row[3] = None
                    row[4] = "Month"
                    cur.updateRow(row)
            vdir = os.path.join(OUT_WS, "05_Wind", "Direction", "Vector_Points")
            if not os.path.isdir(vdir):
                os.makedirs(vdir)
            arcpy.conversion.FeatureClassToShapefile([out_fc], vdir)
            # Alias = field name on the exported shapefile copy.
            shp = os.path.join(vdir, "Wind_Vector_Month.shp")
            try:
                for f in arcpy.ListFields(shp):
                    if f.type in ("OID", "Geometry"):
                        continue
                    arcpy.management.AlterField(shp, f.name, new_field_alias=f.name)
            except Exception:
                pass
            msg("Wind vectors: Wind_Vector_Month (from Month_Mean rasters).")
        else:
            msg("Wind_Vector_Month skipped (Month_Mean rasters or mask missing).")
    except Exception as ex:
        msg("Wind_Vector_Month failed: %s" % ex)

    # PSL/PS Month isobars from the *_Month_Mean rasters.
    try:
        from arcpy.sa import Contour
        for fld, tif, fcname in [
                ("PSL", os.path.join(OUT_WS, "03_Sea_Level_Pressure", "PSL_Month_Mean.tif"), "Isobars_PSL_Month_Mean"),
                ("PS", os.path.join(OUT_WS, "04_Surface_Pressure", "PS_Month_Mean.tif"), "Isobars_PS_Month_Mean")]:
            if not os.path.exists(tif):
                msg("Isobars %s skipped (raster missing)." % fcname)
                continue
            out = os.path.join(gdb, fcname)
            if arcpy.Exists(out):
                arcpy.management.Delete(out)
            Contour(tif, out, ISOBAR_STEP)
            if mask and arcpy.Exists(mask):
                try:
                    raw = out + "_raw"
                    if arcpy.Exists(raw):
                        arcpy.management.Delete(raw)
                    arcpy.management.Rename(out, os.path.basename(raw))
                    arcpy.Clip_analysis(raw, mask, out)
                    arcpy.management.Delete(raw)
                except Exception:
                    pass
            try:
                for f in arcpy.ListFields(out):
                    if f.type in ("OID", "Geometry"):
                        continue
                    arcpy.management.AlterField(out, f.name, new_field_alias=f.name)
            except Exception:
                pass
            msg("Isobars: %s (%.2f hPa, from Month_Mean raster)." % (fcname, ISOBAR_STEP))
    except Exception as ex:
        msg("Month isobars failed: %s" % ex)

    msg("Done in %.1f min." % ((time.time() - t0) / 60.0))


if __name__ == "__main__":
    main()

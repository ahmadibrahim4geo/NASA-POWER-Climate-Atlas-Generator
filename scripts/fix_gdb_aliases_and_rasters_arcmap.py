# -*- coding: utf-8 -*-
"""
Fix GDB after manual agent edits — ArcMap 10.x (Python 2.7 + arcpy).

Two repairs, as requested:
  1. FIELD ALIASES: every field alias in every feature class becomes the
     field name itself (Latin). The previous manual agent set Arabic
     aliases directly in the MAIN gdb (wrong: Arabic belongs only in the
     optional <base>_AR.gdb copy).
  2. RASTERS INSIDE THE GDB: lists every raster / mosaic dataset stored
     inside the FileGDB and deletes it. Rasters belong ONLY in the element
     folders on disk (01_Temperature/ ... Month/), never in the database.

Run inside ArcMap Python window or:
  C:\\Python27\\ArcGIS10.8\\python.exe fix_gdb_aliases_and_rasters_arcmap.py

Safety: DRY_RUN = True only reports. Set CONFIRM_DELETE_RASTERS = True to
actually delete the rasters. Aliases are always safe to fix (metadata only).
"""

import os
import sys

try:
    import arcpy
except Exception as ex:
    raise SystemExit("arcpy required (run inside ArcMap): %s" % ex)

# ============================== CONFIG ======================================
GDB = r"C:\Users\ahmad\Desktop\Egypt Climate Data 1996-2025\Climate_Database_From_1996_To_2025.gdb"
DRY_RUN = True                # True = report only, change nothing
CONFIRM_DELETE_RASTERS = False  # must be True (with DRY_RUN False) to delete
FIX_SHAPEFILES_TOO = False    # also reset aliases in sibling .shp exports
SHAPE_ROOTS = [
    r"C:\Users\ahmad\Desktop\Egypt Climate Data 1996-2025\05_Wind\Direction\Vector_Points",
]
# ============================================================================


def msg(t):
    print(t)
    sys.stdout.flush()


def fix_aliases(fc):
    """Set every field alias = field name. Returns (n_fixed, n_total)."""
    n_fixed, n_total = 0, 0
    try:
        fields = arcpy.ListFields(fc)
    except Exception as ex:
        msg("  !! cannot list fields: %s (%s)" % (fc, ex))
        return 0, 0
    for f in fields:
        if f.type in ("OID", "Geometry"):
            continue
        n_total += 1
        if (f.aliasName or "") != f.name:
            if DRY_RUN:
                n_fixed += 1
                continue
            try:
                arcpy.management.AlterField(fc, f.name, new_field_alias=f.name)
                n_fixed += 1
            except Exception as ex:
                msg("  !! alias fix failed %s.%s: %s" % (os.path.basename(fc), f.name, ex))
    return n_fixed, n_total


def list_gdb_rasters(gdb):
    """Returns (raster_datasets, mosaic_datasets) resident in the GDB."""
    arcpy.env.workspace = gdb
    rasters, mosaics = [], []
    try:
        for r in (arcpy.ListRasters("*", "All") or []):
            rasters.append(os.path.join(gdb, r))
    except Exception as ex:
        msg("  !! ListRasters failed: %s" % ex)
    for dtype in ("Mosaic",):
        try:
            for d in (arcpy.ListDatasets("*", dtype) or []):
                mosaics.append(os.path.join(gdb, d))
        except Exception as ex:
            msg("  !! ListDatasets(%s) failed: %s" % (dtype, ex))
    return rasters, mosaics


def main():
    msg("GDB: %s" % GDB)
    msg("DRY_RUN=%s CONFIRM_DELETE_RASTERS=%s" % (DRY_RUN, CONFIRM_DELETE_RASTERS))

    # ---- 1. aliases ---------------------------------------------------------
    fcs = []
    try:
        arcpy.env.workspace = GDB
        for fc in (arcpy.ListFeatureClasses() or []):
            fcs.append(os.path.join(GDB, fc))
    except Exception as ex:
        msg("FATAL: cannot list feature classes: %s" % ex)
        return
    msg("Feature classes found: %d" % len(fcs))
    tot_fixed, tot_fields = 0, 0
    for fc in sorted(fcs):
        n_fixed, n_total = fix_aliases(fc)
        tot_fixed += n_fixed
        tot_fields += n_total
        if n_fixed:
            msg("  %-28s aliases to reset: %d/%d" % (os.path.basename(fc), n_fixed, n_total))
    if DRY_RUN:
        msg("Aliases needing reset (no change made): %d of %d fields." % (tot_fixed, tot_fields))
    else:
        msg("Aliases reset to field names: %d of %d fields." % (tot_fixed, tot_fields))

    if FIX_SHAPEFILES_TOO:
        import glob
        for root in SHAPE_ROOTS:
            for shp in glob.glob(os.path.join(root, "*.shp")):
                n_fixed, n_total = fix_aliases(shp)
                if n_fixed:
                    msg("  SHP %-24s aliases %s: %d/%d" % (
                        os.path.basename(shp), "to reset" if DRY_RUN else "reset", n_fixed, n_total))

    # ---- 2. rasters inside the GDB ------------------------------------------
    rasters, mosaics = list_gdb_rasters(GDB)
    targets = rasters + mosaics
    if not targets:
        msg("No raster/mosaic datasets inside the GDB. Nothing to delete.")
    else:
        msg("Raster/mosaic datasets inside the GDB (%d):" % len(targets))
        for t in targets:
            msg("  - %s" % os.path.basename(t))
        if DRY_RUN or not CONFIRM_DELETE_RASTERS:
            msg("Deletion SKIPPED (set DRY_RUN=False and CONFIRM_DELETE_RASTERS=True to delete).")
        else:
            for t in targets:
                try:
                    arcpy.management.Delete(t)
                    msg("  DELETED: %s" % os.path.basename(t))
                except Exception as ex:
                    msg("  !! delete failed %s: %s" % (os.path.basename(t), ex))
            try:
                arcpy.management.Compact(GDB)
                msg("GDB compacted.")
            except Exception as ex:
                msg("  !! compact failed: %s" % ex)
    msg("Done.")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Build 05_Wind_Arrows.style — North-oriented wind arrow markers for ArcMap 10.8
- All symbols point NORTH at Angle=0, so Geographic rotation with Arrow_Angle works.
- Arrow_Angle = (Wind_Dir + 180) % 360  (FROM -> TO)
- Run with: C:\Python27\ArcGIS10.8\python.exe Build_Wind_Arrows_Style.py
"""
from __future__ import unicode_literals
import os, sys, shutil, time, gc

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RAW_DIR = os.path.join(BASE_DIR, "style", "Raw_Climate_Styles")
TEMPLATE_STYLE = os.path.join(RAW_DIR, "Meteorological.style")

OUT_NAME = "05_Wind_Arrows.style"
DESTS = [
    os.path.join(BASE_DIR, "style", "05_Wind", OUT_NAME),
    os.path.join(BASE_DIR, "style", "05_Wind", "STYLE", OUT_NAME),
    os.path.join(BASE_DIR, "style", "ArcMap_Style_Files", OUT_NAME),
    os.path.join(BASE_DIR, "style", "All_ArcMap_Styles_Consolidated", OUT_NAME),
]

import arcpy
import comtypes.client

com_dir = r"C:\Program Files (x86)\ArcGIS\Desktop10.8\com"
m_sys = comtypes.client.GetModule(os.path.join(com_dir, "esriSystem.olb"))
m_disp = comtypes.client.GetModule(os.path.join(com_dir, "esriDisplay.olb"))
m_fw = comtypes.client.GetModule(os.path.join(com_dir, "esriFramework.olb"))

def make_rgb(r, g, b):
    c_obj = comtypes.client.CreateObject("esriDisplay.RgbColor")
    c = c_obj.QueryInterface(m_disp.IRgbColor)
    c.Red = r; c.Green = g; c.Blue = b
    return c_obj.QueryInterface(m_disp.IColor)

def make_font(name, size, bold=True):
    f_obj = comtypes.client.CreateObject("StdFont")
    try:
        f_obj.Name = name
        f_obj.Size = size
        f_obj.Bold = bold
    except Exception as ex:
        print("  font set failed %s: %s" % (name, ex))
    return f_obj

def make_char_marker(font_name, char_code, size, rgb, angle=0.0):
    """CharacterMarkerSymbol pointing NORTH (uses north glyphs only)."""
    r, g, b = rgb
    f = make_font(font_name, size, True)
    cms_obj = comtypes.client.CreateObject("esriDisplay.CharacterMarkerSymbol")
    cms = cms_obj.QueryInterface(m_disp.ICharacterMarkerSymbol)
    cms.Font = f  # StdFont IS IFontDisp
    cms.CharacterIndex = int(char_code)
    cms.Size = float(size)
    cms.Color = make_rgb(r, g, b)
    cms.Angle = float(angle)
    return cms_obj

def make_arrow_shaft(rgb, length=18.0, width=2.0, angle=-90.0):
    """ArrowMarkerSymbol with fixed direction angle."""
    r, g, b = rgb
    a_obj = comtypes.client.CreateObject("esriDisplay.ArrowMarkerSymbol")
    am = a_obj.QueryInterface(m_disp.IArrowMarkerSymbol)
    try:
        am.Style = int(m_disp.esriAMSPlain)
    except Exception:
        pass
    am.Length = float(length)
    am.Width = float(width)
    am.Color = make_rgb(r, g, b)
    am.Angle = float(angle)
    return a_obj

def make_simple_triangle(rgb, size):
    """Fallback: SimpleMarker diamond (symmetric, non-directional, last resort)."""
    r, g, b = rgb
    s_obj = comtypes.client.CreateObject("esriDisplay.SimpleMarkerSymbol")
    sm = s_obj.QueryInterface(m_disp.ISimpleMarkerSymbol)
    sm.Style = int(m_disp.esriSMSDiamond)
    sm.Size = float(size)
    sm.Color = make_rgb(r, g, b)
    return s_obj

# 25 base designs x 4 fixed directions (N/E/S/W) = 100 mixed symbols.
# CHAR_BASES: (stem, font, char, size, rgb, north_native)
#  north_native=True  -> glyph points NORTH at angle 0
#  north_native=False -> glyph points EAST at angle 0 (needs -90 for north)
# North: 9650=▲ 9652=▴ 8593=↑ 8657=⇑ 11014=⬆ | East: 8594=→ 9654=▶ 10140=➤ 10148=➧ 10172=➜
CHAR_BASES = [
    ("Tri_Black",       "Arial", 9650, 14, (0, 0, 0), True),
    ("Tri_Navy",        "Arial", 9650, 16, (0, 51, 102), True),
    ("Tri_Red_Khamsin", "Arial", 9650, 16, (189, 0, 38), True),
    ("Tri_Blue",        "Arial", 9650, 16, (0, 102, 204), True),
    ("Tri_Orange_Dust", "Arial", 9650, 14, (230, 85, 13), True),
    ("Tri_Green_Calm",  "Arial", 9650, 14, (65, 171, 93), True),
    ("SmlTri_Black", "Segoe UI Symbol", 9652, 14, (0, 0, 0), True),
    ("SmlTri_Navy",  "Segoe UI Symbol", 9652, 16, (0, 51, 102), True),
    ("Arrow_Thin_Black", "Arial", 8593, 14, (0, 0, 0), True),
    ("Arrow_Bold_Navy",  "Arial", 8593, 18, (0, 51, 102), True),
    ("Arrow_Red",        "Arial", 8593, 18, (240, 59, 32), True),
    ("Dbl_Black", "Segoe UI Symbol", 8657, 16, (0, 0, 0), True),
    ("Dbl_Blue",  "Segoe UI Symbol", 8657, 18, (0, 102, 204), True),
    ("Heavy_Black", "Segoe UI Symbol", 11014, 18, (0, 0, 0), True),
    ("Heavy_Red",   "Segoe UI Symbol", 11014, 20, (189, 0, 38), True),
    ("Barb_Black", "Segoe UI Symbol", 10140, 16, (0, 0, 0), False),
    ("Barb_Navy",  "Segoe UI Symbol", 10140, 18, (0, 51, 102), False),
    ("Tail_Blue",  "Segoe UI Symbol", 10172, 18, (0, 102, 204), False),
    ("Wedge_Orange", "Segoe UI Symbol", 10148, 18, (230, 85, 13), False),
    ("Play_Black", "Arial", 9654, 16, (0, 0, 0), False),
    ("Simple_Black", "Arial", 8594, 16, (0, 0, 0), False),
]
# SHAFT_BASES: (stem, rgb, length, width) — ArrowMarker rest E, so N=-90
SHAFT_BASES = [
    ("Shaft_Black", (0, 0, 0), 22.0, 2.5),
    ("Shaft_Navy",  (0, 51, 102), 22.0, 2.5),
    ("Shaft_Red",   (189, 0, 38), 22.0, 3.0),
    ("Shaft_Blue",  (0, 102, 204), 22.0, 2.5),
]
# fixed direction angles: (suffix, angle_for_north_native, angle_for_east_native/shaft)
DIRS = [("N", 0.0, -90.0), ("E", 90.0, 0.0), ("S", 180.0, 90.0), ("W", 270.0, 180.0)]
DIR_CATS = {"N": "Wind Arrows - North", "E": "Wind Arrows - East",
            "S": "Wind Arrows - South", "W": "Wind Arrows - West"}

def build_one(target_path):
    ldb = target_path[:-6] + ".ldb" if target_path.endswith(".style") else target_path + ".ldb"
    for p in (ldb, target_path):
        if os.path.isfile(p):
            try: os.remove(p)
            except: pass
    time.sleep(0.05)
    shutil.copyfile(TEMPLATE_STYLE, target_path)

    # clean Marker Symbols table only (keep other template content)
    conn = comtypes.client.CreateObject("ADODB.Connection")
    conn.Open("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + target_path)
    try:
        rs = comtypes.client.CreateObject("ADODB.Recordset")
        rs.Open("SELECT * FROM [Marker Symbols]", conn, 1, 3)
        while not rs.EOF:
            rs.Delete()
            rs.MoveNext()
        rs.Close()
    except Exception as ex:
        print("  note: Marker Symbols clean skipped: %s" % ex)
    conn.Close()
    del conn
    gc.collect()

    sg_obj = comtypes.client.CreateObject("esriFramework.StyleGallery")
    sg = sg_obj.QueryInterface(m_disp.IStyleGallery)
    sg_storage = sg_obj.QueryInterface(m_disp.IStyleGalleryStorage)
    sg_storage.TargetFile = target_path
    sg_storage.AddFile(target_path)

    added = 0
    # 21 char bases x 4 dirs = 84
    for stem, font, char, size, rgb, north_native in CHAR_BASES:
        for suffix, a_north, a_east in DIRS:
            ang = a_north if north_native else a_east
            name = "Wind_%s_%s" % (stem, suffix)
            try:
                sym = make_char_marker(font, char, size, rgb, ang)
            except Exception as ex:
                print("  char marker failed %s (%s), fallback diamond" % (name, ex))
                try:
                    sym = make_simple_triangle(rgb, size)
                except Exception as ex2:
                    print("  fallback failed %s: %s" % (name, ex2))
                    continue
            item = comtypes.client.CreateObject("esriFramework.StyleGalleryItem")
            it = item.QueryInterface(m_disp.IStyleGalleryItem)
            it.Name = name
            it.Category = DIR_CATS[suffix]
            it.Item = sym
            sg.AddItem(it)
            added += 1
        print("  + Wind_%s_[N/E/S/W] (U+%04X)" % (stem, char))

    # 4 shaft bases x 4 dirs = 16  -> total 100
    for stem, rgb, ln, wd in SHAFT_BASES:
        for suffix, a_north, a_east in DIRS:
            name = "Wind_%s_%s" % (stem, suffix)
            try:
                sym = make_arrow_shaft(rgb, ln, wd, a_east)
            except Exception as ex:
                print("  shaft failed %s: %s" % (name, ex))
                continue
            item = comtypes.client.CreateObject("esriFramework.StyleGalleryItem")
            it = item.QueryInterface(m_disp.IStyleGalleryItem)
            it.Name = name
            it.Category = DIR_CATS[suffix]
            it.Item = sym
            sg.AddItem(it)
            added += 1
        print("  + Wind_%s_[N/E/S/W] (shaft)" % stem)

    sg.SaveStyle(target_path, "Marker Symbols", "")
    del sg, sg_storage, sg_obj
    gc.collect()
    time.sleep(0.05)
    return added

if __name__ == "__main__":
    print("Building %s ..." % OUT_NAME)
    if not os.path.isfile(TEMPLATE_STYLE):
        print("ERROR: template not found: %s" % TEMPLATE_STYLE)
        sys.exit(1)
    first = DESTS[0]
    d = os.path.dirname(first)
    if not os.path.isdir(d):
        os.makedirs(d)
    n = build_one(first)
    print("SUCCESS: %d markers -> %s" % (n, first))
    for dst in DESTS[1:]:
        dd = os.path.dirname(dst)
        if not os.path.isdir(dd):
            os.makedirs(dd)
        shutil.copyfile(first, dst)
        print("copied -> %s" % dst)
    print("DONE. In ArcMap: Customize > Style Manager > Add Style to List > 05_Wind_Arrows.style")

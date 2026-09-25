# -*- coding: utf-8 -*-
"""
NASA POWER & Open-Meteo Climate Atlas Generator
Comprehensive Climate Styles & Cartographic Color Palette Generator

Generates high-precision, cartographically balanced, perceptually uniform styles
for ArcGIS Desktop (10.x / 10.8), ArcGIS Pro, and QGIS.
Supported Formats: .style (ArcMap Style Database), .clr, .qml, .sld, .json, .csv.

Contains 125 Scientific Palettes across 11 Climate Elements.
Each palette supports 9 class tiers: 3, 4, 5, 6, 7, 8, 9, 10, 11 classes!
Total Color Ramps: 125 x 9 x 2 (Stepped + Smooth) = 2,250 Color Ramps!
"""
from __future__ import unicode_literals
import sys
import os
import io
import json

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def open_utf8(path, mode="w"):
    if PY2:
        return io.open(path, mode, encoding="utf-8")
    else:
        return open(path, mode, encoding="utf-8")

def hex_to_rgb(hex_code):
    h = hex_code.strip().lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def write_clr(path, hex_colors, start_val=1):
    with open_utf8(path, "w") as f:
        for idx, hex_c in enumerate(hex_colors):
            r, g, b = hex_to_rgb(hex_c)
            f.write(u"%d %d %d %d\n" % (start_val + idx, r, g, b))

TEMPERATURE_STYLES = [
  {
    "category": "Sequential",
    "name_ar": "تدرج أصفر برتقالي أحمر كلاسيكي",
    "name_en": "ColorBrewer YlOrRd Classic",
    "id": "Temp_Seq_YlOrRd",
    "source": "ColorBrewer YlOrRd",
    "classes": {
      "3": ["#FFEDA0", "#FEB24C", "#F03B20"],
      "4": ["#FFFFB2", "#FECC5C", "#FD8D3C", "#E31A1C"],
      "5": ["#FFFFB2", "#FECC5C", "#FD8D3C", "#F03B20", "#BD0026"],
      "6": ["#FFFFB2", "#FED976", "#FEB24C", "#FD8D3C", "#F03B20", "#BD0026"],
      "7": ["#FFFFB2", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#B10026"],
      "8": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#B10026"],
      "9": ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C", "#BD0026", "#800026"],
      "10": ["#FFFFCC", "#FFF0A3", "#FED976", "#FEC157", "#FEA144", "#FD7B36", "#F54826", "#E31A1C", "#BD0026", "#800026"],
      "11": ["#FFFFCC", "#FFF2A8", "#FFE187", "#FECB67", "#FEAC4A", "#FD8D3C", "#FD632F", "#F03722", "#D71321", "#B10026", "#800026"]
    }
  },
  {
    "category": "Sequential",
    "name_ar": "تدرج برتقالي أحمر متتابع",
    "name_en": "ColorBrewer OrRd Classic",
    "id": "Temp_Seq_OrRd",
    "source": "ColorBrewer OrRd",
    "classes": {
      "3": ["#FEE8C8", "#FDBB84", "#E34A33"],
      "4": ["#FEF0D9", "#FDCC8A", "#FC8D59", "#D7301F"],
      "5": ["#FEF0D9", "#FDBB84", "#FC8D59", "#E34A33", "#B30000"],
      "6": ["#FEF0D9", "#FDD49E", "#FDBB84", "#FC8D59", "#E34A33", "#B30000"],
      "7": ["#FEF0D9", "#FDD49E", "#FDBB84", "#FC8D59", "#EF6548", "#D7301F", "#990000"],
      "8": ["#FFF7EC", "#FEE8C8", "#FDD49E", "#FDBB84", "#FC8D59", "#EF6548", "#D7301F", "#990000"],
      "9": ["#FFF7EC", "#FEE8C8", "#FDD49E", "#FDBB84", "#FC8D59", "#EF6548", "#D7301F", "#B30000", "#7F0000"],
      "10": ["#FFF7EC", "#FEF0D9", "#FEE0B6", "#FDC590", "#FCA76E", "#F57D4F", "#E65239", "#CE261B", "#A80000", "#7F0000"],
      "11": ["#FFF7EC", "#FEF0D9", "#FEE3BE", "#FDCFA0", "#FDBB84", "#FC9F67", "#F78051", "#EA593C", "#D7301F", "#B10000", "#7F0000"]
    }
  },
  {
    "category": "Sequential", 
    "name_ar": "تدرج أحمر دافئ متتابع", 
    "source": "ColorBrewer Reds", 
    "classes": {
      "3": [
        "#FEE5D9", 
        "#ED4E38", 
        "#67000D"
      ], 
      "4": [
        "#FEE5D9", 
        "#FD8261", 
        "#CB2420", 
        "#67000D"
      ], 
      "5": [
        "#FEE5D9", 
        "#FD9E7F", 
        "#ED4E38", 
        "#B31719", 
        "#67000D"
      ], 
      "6": [
        "#FEE5D9", 
        "#FCAE91", 
        "#FB6A4A", 
        "#DE2D26", 
        "#A50F15", 
        "#67000D"
      ], 
      "7": [
        "#FEE5D9", 
        "#FDB79D", 
        "#FD8261", 
        "#ED4E38", 
        "#CB2420", 
        "#9A0C14", 
        "#67000D"
      ], 
      "8": [
        "#FEE5D9", 
        "#FEBEA5", 
        "#FD9272", 
        "#F76245", 
        "#E2382B", 
        "#BD1D1C", 
        "#930913", 
        "#67000D"
      ], 
      "9": [
        "#FEE5D9", 
        "#FEC3AC", 
        "#FD9E7F", 
        "#FC7353", 
        "#ED4E38", 
        "#D72A24", 
        "#B31719", 
        "#8D0812", 
        "#67000D"
      ], 
      "10": [
        "#FEE5D9", 
        "#FEC6B1", 
        "#FDA789", 
        "#FD8261", 
        "#F55E42", 
        "#E53D2E", 
        "#CB2420", 
        "#AB1317", 
        "#890712", 
        "#67000D"
      ], 
      "11": [
        "#FEE5D9", 
        "#FFCAB5", 
        "#FCAE91", 
        "#FD8D6D", 
        "#FB6A4A", 
        "#ED4E38", 
        "#DE2D26", 
        "#C11F1D", 
        "#A50F15", 
        "#850612", 
        "#67000D"
      ]
    }, 
    "name_en": "Sequential Warm Red", 
    "id": "Temp_Seq_WarmRed"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "تدرج برتقالي عنبري حراري", 
    "source": "ColorBrewer Oranges", 
    "classes": {
      "3": [
        "#FFF5EB", 
        "#F98D43", 
        "#7F2704"
      ], 
      "4": [
        "#FFF5EB", 
        "#FEB97D", 
        "#E95E0D", 
        "#7F2704"
      ], 
      "5": [
        "#FFF5EB", 
        "#FEC894", 
        "#F98D43", 
        "#DF5105", 
        "#7F2704"
      ], 
      "6": [
        "#FFF5EB", 
        "#FDD0A2", 
        "#FDAE6B", 
        "#F16913", 
        "#D94801", 
        "#7F2704"
      ], 
      "7": [
        "#FFF5EB", 
        "#FED6AE", 
        "#FEB97D", 
        "#F98D43", 
        "#E95E0D", 
        "#C94202", 
        "#7F2704"
      ], 
      "8": [
        "#FFF5EB", 
        "#FFDAB7", 
        "#FEC18A", 
        "#FCA560", 
        "#F37423", 
        "#E35708", 
        "#BE3E03", 
        "#7F2704"
      ], 
      "9": [
        "#FFF5EB", 
        "#FFDEBD", 
        "#FEC894", 
        "#FDB272", 
        "#F98D43", 
        "#EE6511", 
        "#DF5105", 
        "#B63B03", 
        "#7F2704"
      ], 
      "10": [
        "#FFF5EB", 
        "#FFE0C2", 
        "#FDCC9C", 
        "#FEB97D", 
        "#FC9F59", 
        "#F5792B", 
        "#E95E0D", 
        "#DC4C03", 
        "#B03903", 
        "#7F2704"
      ], 
      "11": [
        "#FFF5EB", 
        "#FFE2C6", 
        "#FDD0A2", 
        "#FEBF86", 
        "#FDAE6B", 
        "#F98D43", 
        "#F16913", 
        "#E5590A", 
        "#D94801", 
        "#AB3704", 
        "#7F2704"
      ]
    }, 
    "name_en": "Thermal Amber Orange", 
    "id": "Temp_Seq_AmberOrange"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "تدرج أزرق بارد للحرارة الصغرى", 
    "source": "ColorBrewer Blues", 
    "classes": {
      "3": [
        "#F7FBFF", 
        "#5198C9", 
        "#08306B"
      ], 
      "4": [
        "#F7FBFF", 
        "#8CBDDE", 
        "#2771B2", 
        "#08306B"
      ], 
      "5": [
        "#F7FBFF", 
        "#B1D0E9", 
        "#5198C9", 
        "#175DA4", 
        "#08306B"
      ], 
      "6": [
        "#F7FBFF", 
        "#C6DBEF", 
        "#6BAED6", 
        "#3182BD", 
        "#08519C", 
        "#08306B"
      ], 
      "7": [
        "#F7FBFF", 
        "#CEE0F2", 
        "#8CBDDE", 
        "#5198C9", 
        "#2771B2", 
        "#084B94", 
        "#08306B"
      ], 
      "8": [
        "#F7FBFF", 
        "#D4E4F4", 
        "#A1C8E4", 
        "#64A8D2", 
        "#3B88C1", 
        "#1F66AA", 
        "#09478E", 
        "#08306B"
      ], 
      "9": [
        "#F7FBFF", 
        "#D8E7F5", 
        "#B1D0E9", 
        "#78B4D9", 
        "#5198C9", 
        "#2D7CB9", 
        "#175DA4", 
        "#094489", 
        "#08306B"
      ], 
      "10": [
        "#F7FBFF", 
        "#DCE9F6", 
        "#BDD6EC", 
        "#8CBDDE", 
        "#60A4D0", 
        "#408CC3", 
        "#2771B2", 
        "#1056A0", 
        "#094286", 
        "#08306B"
      ], 
      "11": [
        "#F7FBFF", 
        "#DFEBF7", 
        "#C6DBEF", 
        "#9BC4E3", 
        "#6BAED6", 
        "#5198C9", 
        "#3182BD", 
        "#2169AC", 
        "#08519C", 
        "#094083", 
        "#08306B"
      ]
    }, 
    "name_en": "Minimum Cold Temperature", 
    "id": "Temp_Seq_CoolBlue"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "تدرج بنفسجي للصقيع الشديد والتجمد", 
    "source": "ColorBrewer Purples", 
    "classes": {
      "3": [
        "#FCFBFD", 
        "#8A82BD", 
        "#3F007D"
      ], 
      "4": [
        "#FCFBFD", 
        "#B2AFD4", 
        "#6B55A6", 
        "#3F007D"
      ], 
      "5": [
        "#FCFBFD", 
        "#CBCAE2", 
        "#8A82BD", 
        "#5D3997", 
        "#3F007D"
      ], 
      "6": [
        "#FCFBFD", 
        "#DADAEB", 
        "#9E9AC8", 
        "#756BB1", 
        "#54278F", 
        "#3F007D"
      ], 
      "7": [
        "#FCFBFD", 
        "#E0DFEE", 
        "#B2AFD4", 
        "#8A82BD", 
        "#6B55A6", 
        "#51228C", 
        "#3F007D"
      ], 
      "8": [
        "#FCFBFD", 
        "#E4E3F0", 
        "#C0BEDC", 
        "#9893C5", 
        "#7B72B4", 
        "#63459E", 
        "#4E1E8A", 
        "#3F007D"
      ], 
      "9": [
        "#FCFBFD", 
        "#E7E6F2", 
        "#CBCAE2", 
        "#A5A2CC", 
        "#8A82BD", 
        "#7163AD", 
        "#5D3997", 
        "#4C1B88", 
        "#3F007D"
      ], 
      "10": [
        "#FCFBFD", 
        "#E9E9F3", 
        "#D3D3E7", 
        "#B2AFD4", 
        "#958FC3", 
        "#7E75B6", 
        "#6B55A6", 
        "#582F93", 
        "#4B1887", 
        "#3F007D"
      ], 
      "11": [
        "#FCFBFD", 
        "#EBEAF4", 
        "#DADAEB", 
        "#BCB9D9", 
        "#9E9AC8", 
        "#8A82BD", 
        "#756BB1", 
        "#654AA0", 
        "#54278F", 
        "#4A1686", 
        "#3F007D"
      ]
    }, 
    "name_en": "Severe Frost & Cryosphere", 
    "id": "Temp_Seq_DeepPurple"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "تدرج الشذوذ الحراري المعتمد لتقرير المناخ السادس", 
    "source": "IPCC AR6 / Nature (Crameri)", 
    "classes": {
      "3": [
        "#4393C3", 
        "#F7F7F7", 
        "#B2182B"
      ], 
      "4": [
        "#053061", 
        "#92C5DE", 
        "#F4A582", 
        "#67001F"
      ], 
      "5": [
        "#053061", 
        "#92C5DE", 
        "#F7F7F7", 
        "#F4A582", 
        "#67001F"
      ], 
      "6": [
        "#053061", 
        "#347CB8", 
        "#92C5DE", 
        "#F4A582", 
        "#C4413C", 
        "#67001F"
      ], 
      "7": [
        "#053061", 
        "#347CB8", 
        "#92C5DE", 
        "#F7F7F7", 
        "#F4A582", 
        "#C4413C", 
        "#67001F"
      ], 
      "8": [
        "#053061", 
        "#2166AC", 
        "#4393C3", 
        "#92C5DE", 
        "#F4A582", 
        "#D6604D", 
        "#B2182B", 
        "#67001F"
      ], 
      "9": [
        "#053061", 
        "#2166AC", 
        "#4393C3", 
        "#92C5DE", 
        "#F7F7F7", 
        "#F4A582", 
        "#D6604D", 
        "#B2182B", 
        "#67001F"
      ], 
      "10": [
        "#053061", 
        "#1A5899", 
        "#347CB8", 
        "#5A9FCA", 
        "#92C5DE", 
        "#F4A582", 
        "#DE725A", 
        "#C4413C", 
        "#9F1128", 
        "#67001F"
      ], 
      "11": [
        "#053061", 
        "#1A5899", 
        "#347CB8", 
        "#5A9FCA", 
        "#92C5DE", 
        "#F7F7F7", 
        "#F4A582", 
        "#DE725A", 
        "#C4413C", 
        "#9F1128", 
        "#67001F"
      ]
    }, 
    "name_en": "IPCC AR6 Temperature Anomaly", 
    "id": "Temp_Div_RdBu_IPCC"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "تدرج كولور بروير الكلاسيكي المتباعد", 
    "source": "ColorBrewer 2.0 (Cynthia Brewer)", 
    "classes": {
      "3": [
        "#74ADD1", 
        "#FFFFBF", 
        "#D73027"
      ], 
      "4": [
        "#313695", 
        "#ABD9E9", 
        "#FDAE61", 
        "#A50026"
      ], 
      "5": [
        "#313695", 
        "#ABD9E9", 
        "#FFFFBF", 
        "#FDAE61", 
        "#A50026"
      ], 
      "6": [
        "#313695", 
        "#5E91C3", 
        "#ABD9E9", 
        "#FDAE61", 
        "#E65135", 
        "#A50026"
      ], 
      "7": [
        "#313695", 
        "#5E91C3", 
        "#ABD9E9", 
        "#FFFFBF", 
        "#FDAE61", 
        "#E65135", 
        "#A50026"
      ], 
      "8": [
        "#313695", 
        "#4575B4", 
        "#74ADD1", 
        "#ABD9E9", 
        "#FDAE61", 
        "#F46D43", 
        "#D73027", 
        "#A50026"
      ], 
      "9": [
        "#313695", 
        "#4575B4", 
        "#74ADD1", 
        "#ABD9E9", 
        "#FFFFBF", 
        "#FDAE61", 
        "#F46D43", 
        "#D73027", 
        "#A50026"
      ], 
      "10": [
        "#313695", 
        "#4265AC", 
        "#5E91C3", 
        "#82B8D7", 
        "#ABD9E9", 
        "#FDAE61", 
        "#F77E4A", 
        "#E65135", 
        "#CA2727", 
        "#A50026"
      ], 
      "11": [
        "#313695", 
        "#4265AC", 
        "#5E91C3", 
        "#82B8D7", 
        "#ABD9E9", 
        "#FFFFBF", 
        "#FDAE61", 
        "#F77E4A", 
        "#E65135", 
        "#CA2727", 
        "#A50026"
      ]
    }, 
    "name_en": "ColorBrewer RdYlBu Classic", 
    "id": "Temp_Div_RdYlBu_Brewer"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "طيف إزري الناعم المريح بصرياً", 
    "source": "Esri Better Colors for Better Mapping", 
    "classes": {
      "3": [
        "#64ABB0", 
        "#FFFFBF", 
        "#EA633E"
      ], 
      "4": [
        "#2B83BA", 
        "#ABDDA4", 
        "#FDAE61", 
        "#D7191C"
      ], 
      "5": [
        "#2B83BA", 
        "#ABDDA4", 
        "#FFFFBF", 
        "#FDAE61", 
        "#D7191C"
      ], 
      "6": [
        "#2B83BA", 
        "#64ABB0", 
        "#ABDDA4", 
        "#FDAE61", 
        "#EA633E", 
        "#D7191C"
      ], 
      "7": [
        "#2B83BA", 
        "#64ABB0", 
        "#ABDDA4", 
        "#FFFFBF", 
        "#FDAE61", 
        "#EA633E", 
        "#D7191C"
      ], 
      "8": [
        "#2B83BA", 
        "#569DB4", 
        "#7EBBAC", 
        "#ABDDA4", 
        "#FDAE61", 
        "#F17D49", 
        "#E45032", 
        "#D7191C"
      ], 
      "9": [
        "#2B83BA", 
        "#569DB4", 
        "#7EBBAC", 
        "#ABDDA4", 
        "#FFFFBF", 
        "#FDAE61", 
        "#F17D49", 
        "#E45032", 
        "#D7191C"
      ], 
      "10": [
        "#2B83BA", 
        "#4D97B5", 
        "#64ABB0", 
        "#8AC4AB", 
        "#ABDDA4", 
        "#FDAE61", 
        "#F48A4F", 
        "#EA633E", 
        "#E1452D", 
        "#D7191C"
      ], 
      "11": [
        "#2B83BA", 
        "#4D97B5", 
        "#64ABB0", 
        "#8AC4AB", 
        "#ABDDA4", 
        "#FFFFBF", 
        "#FDAE61", 
        "#F48A4F", 
        "#EA633E", 
        "#E1452D", 
        "#D7191C"
      ]
    }, 
    "name_en": "Esri Soft Spectral", 
    "id": "Temp_Multi_SpectralMuted"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "تدرج التركواز إلى المرجاني المريح للعين", 
    "source": "Esri Cartographic Design", 
    "classes": {
      "3": [
        "#48D1CC", 
        "#F5F5F5", 
        "#FF5722"
      ], 
      "4": [
        "#006666", 
        "#B2EBF2", 
        "#FFCCBC", 
        "#D84315"
      ], 
      "5": [
        "#006666", 
        "#B2EBF2", 
        "#F5F5F5", 
        "#FFCCBC", 
        "#D84315"
      ], 
      "6": [
        "#006666", 
        "#2BADAB", 
        "#B2EBF2", 
        "#FFCCBC", 
        "#FF7245", 
        "#D84315"
      ], 
      "7": [
        "#006666", 
        "#2BADAB", 
        "#B2EBF2", 
        "#F5F5F5", 
        "#FFCCBC", 
        "#FF7245", 
        "#D84315"
      ], 
      "8": [
        "#006666", 
        "#008B8B", 
        "#48D1CC", 
        "#B2EBF2", 
        "#FFCCBC", 
        "#FF8A65", 
        "#FF5722", 
        "#D84315"
      ], 
      "9": [
        "#006666", 
        "#008B8B", 
        "#48D1CC", 
        "#B2EBF2", 
        "#F5F5F5", 
        "#FFCCBC", 
        "#FF8A65", 
        "#FF5722", 
        "#D84315"
      ], 
      "10": [
        "#006666", 
        "#008282", 
        "#2BADAB", 
        "#69D8D5", 
        "#B2EBF2", 
        "#FFCCBC", 
        "#FF9B7A", 
        "#FF7245", 
        "#F5521F", 
        "#D84315"
      ], 
      "11": [
        "#006666", 
        "#008282", 
        "#2BADAB", 
        "#69D8D5", 
        "#B2EBF2", 
        "#F5F5F5", 
        "#FFCCBC", 
        "#FF9B7A", 
        "#FF7245", 
        "#F5521F", 
        "#D84315"
      ]
    }, 
    "name_en": "Teal to Coral Ergonomic", 
    "id": "Temp_Div_TealCoral"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "تدرج التباين الحراري البنفسجي-البرتقالي", 
    "source": "CPT-City Archive (J.J. Green)", 
    "classes": {
      "3": [
        "#8073AC", 
        "#F7F7F7", 
        "#B35806"
      ], 
      "4": [
        "#2D004B", 
        "#B2ABD2", 
        "#FDB863", 
        "#7F3B08"
      ], 
      "5": [
        "#2D004B", 
        "#B2ABD2", 
        "#F7F7F7", 
        "#FDB863", 
        "#7F3B08"
      ], 
      "6": [
        "#2D004B", 
        "#6B4E9A", 
        "#B2ABD2", 
        "#FDB863", 
        "#C96D0D", 
        "#7F3B08"
      ], 
      "7": [
        "#2D004B", 
        "#6B4E9A", 
        "#B2ABD2", 
        "#F7F7F7", 
        "#FDB863", 
        "#C96D0D", 
        "#7F3B08"
      ], 
      "8": [
        "#2D004B", 
        "#542788", 
        "#8073AC", 
        "#B2ABD2", 
        "#FDB863", 
        "#E08214", 
        "#B35806", 
        "#7F3B08"
      ], 
      "9": [
        "#2D004B", 
        "#542788", 
        "#8073AC", 
        "#B2ABD2", 
        "#F7F7F7", 
        "#FDB863", 
        "#E08214", 
        "#B35806", 
        "#7F3B08"
      ], 
      "10": [
        "#2D004B", 
        "#4A1D78", 
        "#6B4E9A", 
        "#8C81B5", 
        "#B2ABD2", 
        "#FDB863", 
        "#E88F2C", 
        "#C96D0D", 
        "#A65107", 
        "#7F3B08"
      ], 
      "11": [
        "#2D004B", 
        "#4A1D78", 
        "#6B4E9A", 
        "#8C81B5", 
        "#B2ABD2", 
        "#F7F7F7", 
        "#FDB863", 
        "#E88F2C", 
        "#C96D0D", 
        "#A65107", 
        "#7F3B08"
      ]
    }, 
    "name_en": "Extreme Temperature Variance", 
    "id": "Temp_Div_PuOr"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "مقياس باتلو العلمي المحايد إدراكياً", 
    "source": "Fabio Crameri Scientific Colour Maps", 
    "classes": {
      "3": [
        "#000000", 
        "#7EB124", 
        "#FFFFFF"
      ], 
      "4": [
        "#000000", 
        "#007F66", 
        "#FFCC00", 
        "#FFFFFF"
      ], 
      "5": [
        "#000000", 
        "#0D5F7A", 
        "#7EB124", 
        "#FF8300", 
        "#FFFFFF"
      ], 
      "6": [
        "#000000", 
        "#104A7B", 
        "#42944B", 
        "#C9C500", 
        "#FF5A00", 
        "#FFFFFF"
      ], 
      "7": [
        "#000000", 
        "#1A3A73", 
        "#007F66", 
        "#7EB124", 
        "#FFCC00", 
        "#FF4600", 
        "#FFFFFF"
      ], 
      "8": [
        "#000000", 
        "#1D2E6D", 
        "#116D72", 
        "#4F9E3C", 
        "#B1C100", 
        "#FFA300", 
        "#FF3400", 
        "#FFFFFF"
      ], 
      "9": [
        "#000000", 
        "#1E2569", 
        "#0D5F7A", 
        "#348C56", 
        "#7EB124", 
        "#DDC800", 
        "#FF8300", 
        "#FF2000", 
        "#FFFFFF"
      ], 
      "10": [
        "#000000", 
        "#1E1E66", 
        "#005580", 
        "#007F66", 
        "#55A333", 
        "#A3BF00", 
        "#FFCC00", 
        "#FF6600", 
        "#FF0000", 
        "#FFFFFF"
      ], 
      "11": [
        "#000000", 
        "#1D1C5C", 
        "#104A7B", 
        "#0F726E", 
        "#42944B", 
        "#7EB124", 
        "#C9C500", 
        "#FFB000", 
        "#FF5A00", 
        "#FF3E22", 
        "#FFFFFF"
      ]
    }, 
    "name_en": "Crameri Batlow Scientific", 
    "id": "Temp_Multi_Thermal_Crameri"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "مقياس روما العلمي المتباعد", 
    "source": "Fabio Crameri Scientific Colour Maps", 
    "classes": {
      "3": [
        "#4393C3", 
        "#FFFFBF", 
        "#F46D43"
      ], 
      "4": [
        "#7E1E7B", 
        "#92C5DE", 
        "#FEE090", 
        "#A50026"
      ], 
      "5": [
        "#7E1E7B", 
        "#92C5DE", 
        "#FFFFBF", 
        "#FEE090", 
        "#A50026"
      ], 
      "6": [
        "#7E1E7B", 
        "#555FA5", 
        "#92C5DE", 
        "#FEE090", 
        "#F98F52", 
        "#A50026"
      ], 
      "7": [
        "#7E1E7B", 
        "#555FA5", 
        "#92C5DE", 
        "#FFFFBF", 
        "#FEE090", 
        "#F98F52", 
        "#A50026"
      ], 
      "8": [
        "#7E1E7B", 
        "#542788", 
        "#4393C3", 
        "#92C5DE", 
        "#FEE090", 
        "#FDAE61", 
        "#F46D43", 
        "#A50026"
      ], 
      "9": [
        "#7E1E7B", 
        "#542788", 
        "#4393C3", 
        "#92C5DE", 
        "#FFFFBF", 
        "#FEE090", 
        "#FDAE61", 
        "#F46D43", 
        "#A50026"
      ], 
      "10": [
        "#7E1E7B", 
        "#602585", 
        "#555FA5", 
        "#5A9FCA", 
        "#92C5DE", 
        "#FEE090", 
        "#FEBB6D", 
        "#F98F52", 
        "#E0583C", 
        "#A50026"
      ], 
      "11": [
        "#7E1E7B", 
        "#602585", 
        "#555FA5", 
        "#5A9FCA", 
        "#92C5DE", 
        "#FFFFBF", 
        "#FEE090", 
        "#FEBB6D", 
        "#F98F52", 
        "#E0583C", 
        "#A50026"
      ]
    }, 
    "name_en": "Crameri Roma Diverging", 
    "id": "Temp_Multi_Roma_Crameri"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "مقياس درجات الحرارة السطحية للمنظمة العالمية للأرصاد", 
    "source": "WMO Technical Regulations WMO-No. 306", 
    "classes": {
      "3": [
        "#000080", 
        "#00FF00", 
        "#800000"
      ], 
      "4": [
        "#000080", 
        "#13E9FF", 
        "#FFE100", 
        "#800000"
      ], 
      "5": [
        "#000080", 
        "#00BFFF", 
        "#00FF00", 
        "#FFA500", 
        "#800000"
      ], 
      "6": [
        "#000080", 
        "#3D82FF", 
        "#3AFFD8", 
        "#E1FF00", 
        "#FF7A00", 
        "#800000"
      ], 
      "7": [
        "#000080", 
        "#3858FF", 
        "#13E9FF", 
        "#00FF00", 
        "#FFE100", 
        "#FF5800", 
        "#800000"
      ], 
      "8": [
        "#000080", 
        "#2734FF", 
        "#12D1FF", 
        "#46FFAA", 
        "#BBFF00", 
        "#FFBF00", 
        "#FF3800", 
        "#800000"
      ], 
      "9": [
        "#000080", 
        "#0000FF", 
        "#00BFFF", 
        "#00FFFF", 
        "#00FF00", 
        "#FFFF00", 
        "#FFA500", 
        "#FF0000", 
        "#800000"
      ], 
      "10": [
        "#000080", 
        "#0000F0", 
        "#349EFF", 
        "#13E9FF", 
        "#45FF90", 
        "#A3FF00", 
        "#FFE100", 
        "#FF8E00", 
        "#F00001", 
        "#800000"
      ], 
      "11": [
        "#000080", 
        "#0000E4", 
        "#3D82FF", 
        "#14D8FF", 
        "#3AFFD8", 
        "#00FF00", 
        "#E1FF00", 
        "#FFCA00", 
        "#FF7A00", 
        "#E40001", 
        "#800000"
      ]
    }, 
    "name_en": "WMO Synoptic Temperature", 
    "id": "Temp_Multi_WMO_Standard"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "المقياس المعتمد للتنبؤات الحرارية بهيئة الأرصاد الأمريكية", 
    "source": "NOAA National Weather Service (NWS)", 
    "classes": {
      "3": [
        "#2C1E5C", 
        "#98FB98", 
        "#8B0000"
      ], 
      "4": [
        "#2C1E5C", 
        "#76ABE8", 
        "#FFE100", 
        "#8B0000"
      ], 
      "5": [
        "#2C1E5C", 
        "#4169E1", 
        "#98FB98", 
        "#FFA500", 
        "#8B0000"
      ], 
      "6": [
        "#2C1E5C", 
        "#4757BE", 
        "#8ED7DB", 
        "#EEFE3D", 
        "#FF8400", 
        "#8B0000"
      ], 
      "7": [
        "#2C1E5C", 
        "#494BA7", 
        "#76ABE8", 
        "#98FB98", 
        "#FFE100", 
        "#FF6B00", 
        "#8B0000"
      ], 
      "8": [
        "#2C1E5C", 
        "#494397", 
        "#5C85E4", 
        "#94E1C9", 
        "#DAFE5D", 
        "#FFBF00", 
        "#FF5700", 
        "#8B0000"
      ], 
      "9": [
        "#2C1E5C", 
        "#483D8B", 
        "#4169E1", 
        "#87CEEB", 
        "#98FB98", 
        "#FFFF00", 
        "#FFA500", 
        "#FF4500", 
        "#8B0000"
      ], 
      "10": [
        "#2C1E5C", 
        "#453986", 
        "#455FCD", 
        "#76ABE8", 
        "#96E7BE", 
        "#CDFD6B", 
        "#FFE100", 
        "#FF9300", 
        "#F23E01", 
        "#8B0000"
      ], 
      "11": [
        "#2C1E5C", 
        "#423781", 
        "#4757BE", 
        "#6590E6", 
        "#8ED7DB", 
        "#98FB98", 
        "#EEFE3D", 
        "#FFCA00", 
        "#FF8400", 
        "#E73901", 
        "#8B0000"
      ]
    }, 
    "name_en": "NOAA NWS Heat Scale", 
    "id": "Temp_Multi_NOAA_NWS"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "تدرج حرارة سطح الأرض من أقمار ناسا", 
    "source": "NASA Earth Science Data Systems (LST)", 
    "classes": {
      "3": [
        "#0C0887", 
        "#CB4679", 
        "#F0F921"
      ], 
      "4": [
        "#0C0887", 
        "#9B199C", 
        "#EC7955", 
        "#F0F921"
      ], 
      "5": [
        "#0C0887", 
        "#7D03A8", 
        "#CB4679", 
        "#F89441", 
        "#F0F921"
      ], 
      "6": [
        "#0C0887", 
        "#6A02A5", 
        "#B02A90", 
        "#E06463", 
        "#FAA43A", 
        "#F0F921"
      ], 
      "7": [
        "#0C0887", 
        "#5D02A3", 
        "#9B199C", 
        "#CB4679", 
        "#EC7955", 
        "#FCAE35", 
        "#F0F921"
      ], 
      "8": [
        "#0C0887", 
        "#5303A2", 
        "#8A0DA3", 
        "#B8328A", 
        "#DA5C6A", 
        "#F3894A", 
        "#FCB631", 
        "#F0F921"
      ], 
      "9": [
        "#0C0887", 
        "#4B03A1", 
        "#7D03A8", 
        "#A82296", 
        "#CB4679", 
        "#E56B5D", 
        "#F89441", 
        "#FDBB2D", 
        "#F0F921"
      ], 
      "10": [
        "#0C0887", 
        "#46049E", 
        "#7302A6", 
        "#9B199C", 
        "#BC3786", 
        "#D7576D", 
        "#EC7955", 
        "#F99D3E", 
        "#FCC22C", 
        "#F0F921"
      ], 
      "11": [
        "#0C0887", 
        "#41049C", 
        "#6A02A5", 
        "#9011A1", 
        "#B02A90", 
        "#CB4679", 
        "#E06463", 
        "#F1844E", 
        "#FAA43A", 
        "#FBC82B", 
        "#F0F921"
      ]
    }, 
    "name_en": "NASA MODIS Land Surface Temp", 
    "id": "Temp_Multi_NASA_LST"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "مقياس مخاطر الموجات الحارة الشديدة والإجهاد الحيوي", 
    "source": "WMO / WHO Health Heatwave Guidance", 
    "classes": {
      "3": [
        "#FFFFB2", 
        "#FC4E2A", 
        "#490000"
      ], 
      "4": [
        "#FFFFB2", 
        "#FE9A41", 
        "#D21220", 
        "#490000"
      ], 
      "5": [
        "#FFFFB2", 
        "#FEB24C", 
        "#FC4E2A", 
        "#B10026", 
        "#490000"
      ], 
      "6": [
        "#FFFFB2", 
        "#FFC25D", 
        "#FD8238", 
        "#E8281F", 
        "#93001C", 
        "#490000"
      ], 
      "7": [
        "#FFFFB2", 
        "#FFCC68", 
        "#FE9A41", 
        "#FC4E2A", 
        "#D21220", 
        "#7F0016", 
        "#490000"
      ], 
      "8": [
        "#FFFFB2", 
        "#FED370", 
        "#FEA847", 
        "#FD7534", 
        "#EE3522", 
        "#BF0724", 
        "#710011", 
        "#490000"
      ], 
      "9": [
        "#FFFFB2", 
        "#FED976", 
        "#FEB24C", 
        "#FD8D3C", 
        "#FC4E2A", 
        "#E31A1C", 
        "#B10026", 
        "#67000D", 
        "#490000"
      ], 
      "10": [
        "#FFFFB2", 
        "#FEDD7D", 
        "#FEBB55", 
        "#FE9A41", 
        "#FD6D32", 
        "#F13B24", 
        "#D21220", 
        "#A00020", 
        "#64000C", 
        "#490000"
      ], 
      "11": [
        "#FFFFB2", 
        "#FFE182", 
        "#FFC25D", 
        "#FEA445", 
        "#FD8238", 
        "#FC4E2A", 
        "#E8281F", 
        "#C50B23", 
        "#93001C", 
        "#61000B", 
        "#490000"
      ]
    }, 
    "name_en": "Extreme Heatwave Stress", 
    "id": "Temp_Multi_HeatwaveRisk"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "تدرج شذوذ الحرارة السطحية العالمي لمرصد غودارد", 
    "source": "NASA Goddard Institute for Space Studies (GISS)", 
    "classes": {
      "3": [
        "#73B3D8", 
        "#FFFFFF", 
        "#C51B17"
      ], 
      "4": [
        "#08306B", 
        "#C6DBEF", 
        "#FDD0A2", 
        "#67000D"
      ], 
      "5": [
        "#08306B", 
        "#C6DBEF", 
        "#FFFFFF", 
        "#FDD0A2", 
        "#67000D"
      ], 
      "6": [
        "#08306B", 
        "#5295C9", 
        "#C6DBEF", 
        "#FDD0A2", 
        "#DB4716", 
        "#67000D"
      ], 
      "7": [
        "#08306B", 
        "#5295C9", 
        "#C6DBEF", 
        "#FFFFFF", 
        "#FDD0A2", 
        "#DB4716", 
        "#67000D"
      ], 
      "8": [
        "#08306B", 
        "#2879B9", 
        "#73B3D8", 
        "#C6DBEF", 
        "#FDD0A2", 
        "#F16913", 
        "#C51B17", 
        "#67000D"
      ], 
      "9": [
        "#08306B", 
        "#2879B9", 
        "#73B3D8", 
        "#C6DBEF", 
        "#FFFFFF", 
        "#FDD0A2", 
        "#F16913", 
        "#C51B17", 
        "#67000D"
      ], 
      "10": [
        "#08306B", 
        "#2166A5", 
        "#5295C9", 
        "#89BDDE", 
        "#C6DBEF", 
        "#FDD0A2", 
        "#F7843C", 
        "#DB4716", 
        "#AC1315", 
        "#67000D"
      ], 
      "11": [
        "#08306B", 
        "#2166A5", 
        "#5295C9", 
        "#89BDDE", 
        "#C6DBEF", 
        "#FFFFFF", 
        "#FDD0A2", 
        "#F7843C", 
        "#DB4716", 
        "#AC1315", 
        "#67000D"
      ]
    }, 
    "name_en": "NASA GISTEMP Global Anomaly", 
    "id": "Temp_Div_NASA_GISTEMP"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "تدرج حرارة الهواء 2م لإعادة التحليل الأوروبي ERA5", 
    "source": "ECMWF Copernicus Climate Change Service (C3S)", 
    "classes": {
      "3": [
        "#00204D", 
        "#86B285", 
        "#E15759"
      ], 
      "4": [
        "#00204D", 
        "#358A88", 
        "#D5CE8A", 
        "#E15759"
      ], 
      "5": [
        "#00204D", 
        "#1E7084", 
        "#86B285", 
        "#F5D983", 
        "#E15759"
      ], 
      "6": [
        "#00204D", 
        "#105F7F", 
        "#559B86", 
        "#B7C487", 
        "#FECD6F", 
        "#E15759"
      ], 
      "7": [
        "#00204D", 
        "#0C547B", 
        "#358A88", 
        "#86B285", 
        "#D5CE8A", 
        "#FBB557", 
        "#E15759"
      ], 
      "8": [
        "#00204D", 
        "#074C77", 
        "#297B86", 
        "#61A286", 
        "#AAC086", 
        "#E7D486", 
        "#F7A544", 
        "#E15759"
      ], 
      "9": [
        "#00204D", 
        "#034775", 
        "#1E7084", 
        "#4A9487", 
        "#86B285", 
        "#C3C888", 
        "#F5D983", 
        "#F49837", 
        "#E15759"
      ], 
      "10": [
        "#00204D", 
        "#004273", 
        "#126782", 
        "#358A88", 
        "#67A685", 
        "#A3BE85", 
        "#D5CE8A", 
        "#FFDC80", 
        "#F28E2B", 
        "#E15759"
      ], 
      "11": [
        "#00204D", 
        "#003E6F", 
        "#105F7F", 
        "#2D7F86", 
        "#559B86", 
        "#86B285", 
        "#B7C487", 
        "#E2D287", 
        "#FECD6F", 
        "#F18932", 
        "#E15759"
      ]
    }, 
    "name_en": "ECMWF ERA5 2m Air Temp", 
    "id": "Temp_Multi_ERA5_Thermal"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "مقياس مركز التنبؤات المناخية الأمريكي CPC", 
    "source": "NOAA Climate Prediction Center", 
    "classes": {
      "3": [
        "#313695", 
        "#FFFFBF", 
        "#A50026"
      ], 
      "4": [
        "#313695", 
        "#BDE2EE", 
        "#FEBF70", 
        "#A50026"
      ], 
      "5": [
        "#313695", 
        "#90C3DD", 
        "#FFFFBF", 
        "#F98F52", 
        "#A50026"
      ], 
      "6": [
        "#313695", 
        "#74ADD1", 
        "#E0F3F8", 
        "#FEE090", 
        "#F46D43", 
        "#A50026"
      ], 
      "7": [
        "#313695", 
        "#659AC7", 
        "#BDE2EE", 
        "#FFFFBF", 
        "#FEBF70", 
        "#EB5B39", 
        "#A50026"
      ], 
      "8": [
        "#313695", 
        "#5A8DC0", 
        "#A3D3E6", 
        "#EAF6E8", 
        "#FFE99D", 
        "#FCA55D", 
        "#E44D33", 
        "#A50026"
      ], 
      "9": [
        "#313695", 
        "#5283BB", 
        "#90C3DD", 
        "#D3ECF4", 
        "#FFFFBF", 
        "#FED484", 
        "#F98F52", 
        "#DE422E", 
        "#A50026"
      ], 
      "10": [
        "#313695", 
        "#4B7BB7", 
        "#81B7D6", 
        "#BDE2EE", 
        "#EFF8DF", 
        "#FFEEA5", 
        "#FEBF70", 
        "#F77C49", 
        "#DA382A", 
        "#A50026"
      ], 
      "11": [
        "#313695", 
        "#4575B4", 
        "#74ADD1", 
        "#ABD9E9", 
        "#E0F3F8", 
        "#FFFFBF", 
        "#FEE090", 
        "#FDAE61", 
        "#F46D43", 
        "#D73027", 
        "#A50026"
      ]
    }, 
    "name_en": "NOAA CPC Climatological Scale", 
    "id": "Temp_Multi_NOAA_CPC"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "مقياس نوك العلمي للمناطق القطبية والجليد", 
    "source": "Fabio Crameri Scientific Colour Maps (Nuuk)", 
    "classes": {
      "3": [
        "#3A7EB0", 
        "#F7F7F7", 
        "#DF5842"
      ], 
      "4": [
        "#0D253A", 
        "#B5DBF2", 
        "#FAD3BD", 
        "#610012"
      ], 
      "5": [
        "#0D253A", 
        "#B5DBF2", 
        "#F7F7F7", 
        "#FAD3BD", 
        "#610012"
      ], 
      "6": [
        "#0D253A", 
        "#3A7EB0", 
        "#B5DBF2", 
        "#FAD3BD", 
        "#DF5842", 
        "#610012"
      ], 
      "7": [
        "#0D253A", 
        "#3A7EB0", 
        "#B5DBF2", 
        "#F7F7F7", 
        "#FAD3BD", 
        "#DF5842", 
        "#610012"
      ], 
      "8": [
        "#0D253A", 
        "#265E88", 
        "#639ECC", 
        "#B5DBF2", 
        "#FAD3BD", 
        "#EF8765", 
        "#BD332E", 
        "#610012"
      ], 
      "9": [
        "#0D253A", 
        "#265E88", 
        "#639ECC", 
        "#B5DBF2", 
        "#F7F7F7", 
        "#FAD3BD", 
        "#EF8765", 
        "#BD332E", 
        "#610012"
      ], 
      "10": [
        "#0D253A", 
        "#1C4E75", 
        "#3A7EB0", 
        "#76AFDA", 
        "#B5DBF2", 
        "#FAD3BD", 
        "#F59D77", 
        "#DF5842", 
        "#AC1C24", 
        "#610012"
      ], 
      "11": [
        "#0D253A", 
        "#1C4E75", 
        "#3A7EB0", 
        "#76AFDA", 
        "#B5DBF2", 
        "#F7F7F7", 
        "#FAD3BD", 
        "#F59D77", 
        "#DF5842", 
        "#AC1C24", 
        "#610012"
      ]
    }, 
    "name_en": "Crameri Nuuk Cryosphere", 
    "id": "Temp_Div_Nuuk_Cryo"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "عتبات خطر الصقيع والتجمد الزراعي", 
    "source": "WMO Agricultural Meteorology Guidelines", 
    "classes": {
      "3": [
        "#E0F3F8", 
        "#347CB8", 
        "#021A3B"
      ], 
      "4": [
        "#E0F3F8", 
        "#61A3CC", 
        "#185392", 
        "#021A3B"
      ], 
      "5": [
        "#E0F3F8", 
        "#80B8D7", 
        "#347CB8", 
        "#0C3D73", 
        "#021A3B"
      ], 
      "6": [
        "#E0F3F8", 
        "#92C5DE", 
        "#4393C3", 
        "#2166AC", 
        "#053061", 
        "#021A3B"
      ], 
      "7": [
        "#E0F3F8", 
        "#A0CDE2", 
        "#61A3CC", 
        "#347CB8", 
        "#185392", 
        "#042C5A", 
        "#021A3B"
      ], 
      "8": [
        "#E0F3F8", 
        "#A9D2E5", 
        "#73AFD2", 
        "#3F8CC0", 
        "#276CAF", 
        "#114680", 
        "#042A56", 
        "#021A3B"
      ], 
      "9": [
        "#E0F3F8", 
        "#B0D6E8", 
        "#80B8D7", 
        "#4F99C6", 
        "#347CB8", 
        "#1E5FA2", 
        "#0C3D73", 
        "#042852", 
        "#021A3B"
      ], 
      "10": [
        "#E0F3F8", 
        "#B5D9EA", 
        "#8ABFDB", 
        "#61A3CC", 
        "#3D89BE", 
        "#2A70B1", 
        "#185392", 
        "#083669", 
        "#032650", 
        "#021A3B"
      ], 
      "11": [
        "#E0F3F8", 
        "#BADCEB", 
        "#92C5DE", 
        "#6EACD1", 
        "#4393C3", 
        "#347CB8", 
        "#2166AC", 
        "#134A86", 
        "#053061", 
        "#03254E", 
        "#021A3B"
      ]
    }, 
    "name_en": "WMO Frost & Freeze Hazard", 
    "id": "Temp_Seq_FrostThreshold"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "الأقاليم الحرارية المعيارية لتصنيف كوبن-جيجر", 
    "source": "Köppen-Geiger World Climate Classification", 
    "classes": {
      "3": [
        "#960000", 
        "#AEFF00", 
        "#800080"
      ], 
      "4": [
        "#960000", 
        "#FFA500", 
        "#00FFFF", 
        "#800080"
      ], 
      "5": [
        "#960000", 
        "#FF7993", 
        "#AEFF00", 
        "#2A9EFF", 
        "#800080"
      ], 
      "6": [
        "#960000", 
        "#FF5B93", 
        "#FFDC00", 
        "#43FF87", 
        "#196DFF", 
        "#800080"
      ], 
      "7": [
        "#960000", 
        "#FF4562", 
        "#FFA500", 
        "#AEFF00", 
        "#00FFFF", 
        "#2051FF", 
        "#800080"
      ], 
      "8": [
        "#960000", 
        "#FF323F", 
        "#FF8D66", 
        "#FFF200", 
        "#2DFF49", 
        "#33C7FF", 
        "#1C39FF", 
        "#800080"
      ], 
      "9": [
        "#960000", 
        "#FF1E22", 
        "#FF7993", 
        "#FFC700", 
        "#AEFF00", 
        "#45FFB5", 
        "#2A9EFF", 
        "#1223FF", 
        "#800080"
      ], 
      "10": [
        "#960000", 
        "#FF0000", 
        "#FF69B4", 
        "#FFA500", 
        "#FFFF00", 
        "#00FF00", 
        "#00FFFF", 
        "#007FFF", 
        "#0000FF", 
        "#800080"
      ], 
      "11": [
        "#960000", 
        "#F40000", 
        "#FF5B93", 
        "#FF9452", 
        "#FFDC00", 
        "#AEFF00", 
        "#43FF87", 
        "#2FD8FF", 
        "#196DFF", 
        "#3600F2", 
        "#800080"
      ]
    }, 
    "name_en": "Köppen-Geiger Thermal Regimes", 
    "id": "Temp_Multi_KoppenThermal"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "شذوذ الاحترار التاريخي لمركز هادلي البريطاني", 
    "source": "UK Met Office / Climatic Research Unit (CRU)", 
    "classes": {
      "3": [
        "#6BAED6", 
        "#F0F0F0", 
        "#DE2D26"
      ], 
      "4": [
        "#08519C", 
        "#BDD7E7", 
        "#FCAE91", 
        "#A50F15"
      ], 
      "5": [
        "#08519C", 
        "#BDD7E7", 
        "#F0F0F0", 
        "#FCAE91", 
        "#A50F15"
      ], 
      "6": [
        "#08519C", 
        "#5198C9", 
        "#BDD7E7", 
        "#FCAE91", 
        "#ED4E38", 
        "#A50F15"
      ], 
      "7": [
        "#08519C", 
        "#5198C9", 
        "#BDD7E7", 
        "#F0F0F0", 
        "#FCAE91", 
        "#ED4E38", 
        "#A50F15"
      ], 
      "8": [
        "#08519C", 
        "#3182BD", 
        "#6BAED6", 
        "#BDD7E7", 
        "#FCAE91", 
        "#FB6A4A", 
        "#DE2D26", 
        "#A50F15"
      ], 
      "9": [
        "#08519C", 
        "#3182BD", 
        "#6BAED6", 
        "#BDD7E7", 
        "#F0F0F0", 
        "#FCAE91", 
        "#FB6A4A", 
        "#DE2D26", 
        "#A50F15"
      ], 
      "10": [
        "#08519C", 
        "#2A75B5", 
        "#5198C9", 
        "#82B8DA", 
        "#BDD7E7", 
        "#FCAE91", 
        "#FD7C5B", 
        "#ED4E38", 
        "#CF2622", 
        "#A50F15"
      ], 
      "11": [
        "#08519C", 
        "#2A75B5", 
        "#5198C9", 
        "#82B8DA", 
        "#BDD7E7", 
        "#F0F0F0", 
        "#FCAE91", 
        "#FD7C5B", 
        "#ED4E38", 
        "#CF2622", 
        "#A50F15"
      ]
    }, 
    "name_en": "HadCRUT5 Historical Warming", 
    "id": "Temp_Div_HadCRUT5"
  }, 
  {
    "category": "Multi-Hue", 
    "name_ar": "درجة الحرارة المحسوسة الفعلية لستيدمان", 
    "source": "Steadman Biometeorological Formula", 
    "classes": {
      "3": [
        "#2B83BA", 
        "#FFD78F", 
        "#7F0000"
      ], 
      "4": [
        "#2B83BA", 
        "#E3F4B6", 
        "#F38649", 
        "#7F0000"
      ], 
      "5": [
        "#2B83BA", 
        "#C0E6AB", 
        "#FFD78F", 
        "#E24D2C", 
        "#7F0000"
      ], 
      "6": [
        "#2B83BA", 
        "#ABDDA4", 
        "#FFFFBF", 
        "#FDAE61", 
        "#D7191C", 
        "#7F0000"
      ], 
      "7": [
        "#2B83BA", 
        "#9CCDA9", 
        "#E3F4B6", 
        "#FFD78F", 
        "#F38649", 
        "#C81518", 
        "#7F0000"
      ], 
      "8": [
        "#2B83BA", 
        "#90C2AC", 
        "#D0ECAF", 
        "#FFF3B1", 
        "#FFBA6E", 
        "#EA6738", 
        "#BD1114", 
        "#7F0000"
      ], 
      "9": [
        "#2B83BA", 
        "#87BAAE", 
        "#C0E6AB", 
        "#F5FBBC", 
        "#FFD78F", 
        "#F99F58", 
        "#E24D2C", 
        "#B50F12", 
        "#7F0000"
      ], 
      "10": [
        "#2B83BA", 
        "#7FB4AF", 
        "#B5E1A7", 
        "#E3F4B6", 
        "#FFEDAA", 
        "#FFC076", 
        "#F38649", 
        "#DC3523", 
        "#AF0D10", 
        "#7F0000"
      ], 
      "11": [
        "#2B83BA", 
        "#79AFB1", 
        "#ABDDA4", 
        "#D5EEB1", 
        "#FFFFBF", 
        "#FFD78F", 
        "#FDAE61", 
        "#ED703D", 
        "#D7191C", 
        "#AA0B0F", 
        "#7F0000"
      ]
    }, 
    "name_en": "Steadman Apparent Temperature", 
    "id": "Temp_Multi_SteadmanApparent"
  }, 
  {
    "category": "Diverging", 
    "name_ar": "المدى الحراري السنوي للمناطق القارية", 
    "source": "Climatological Continental Range Index", 
    "classes": {
      "3": [
        "#78A3C8", 
        "#FFFFE0", 
        "#FC8D59"
      ], 
      "4": [
        "#1B385C", 
        "#B8D4E8", 
        "#FDD49E", 
        "#B30000"
      ], 
      "5": [
        "#1B385C", 
        "#B8D4E8", 
        "#FFFFE0", 
        "#FDD49E", 
        "#B30000"
      ], 
      "6": [
        "#1B385C", 
        "#5A85B0", 
        "#B8D4E8", 
        "#FDD49E", 
        "#FC8D59", 
        "#B30000"
      ], 
      "7": [
        "#1B385C", 
        "#5A85B0", 
        "#B8D4E8", 
        "#FFFFE0", 
        "#FDD49E", 
        "#FC8D59", 
        "#B30000"
      ], 
      "8": [
        "#1B385C", 
        "#3B6998", 
        "#78A3C8", 
        "#B8D4E8", 
        "#FDD49E", 
        "#FDAC75", 
        "#EC623F", 
        "#B30000"
      ], 
      "9": [
        "#1B385C", 
        "#3B6998", 
        "#78A3C8", 
        "#B8D4E8", 
        "#FFFFE0", 
        "#FDD49E", 
        "#FDAC75", 
        "#EC623F", 
        "#B30000"
      ], 
      "10": [
        "#1B385C", 
        "#335C89", 
        "#5A85B0", 
        "#88AFD0", 
        "#B8D4E8", 
        "#FDD49E", 
        "#FDBB84", 
        "#FC8D59", 
        "#E34A33", 
        "#B30000"
      ], 
      "11": [
        "#1B385C", 
        "#335C89", 
        "#5A85B0", 
        "#88AFD0", 
        "#B8D4E8", 
        "#FFFFE0", 
        "#FDD49E", 
        "#FDBB84", 
        "#FC8D59", 
        "#E34A33", 
        "#B30000"
      ]
    }, 
    "name_en": "Continental Annual Range", 
    "id": "Temp_Div_ContinentalThermal"
  }, 
  {
    "category": "Sequential", 
    "name_ar": "مؤشر الليالي الاستوائية وتراكم الحرارة الليلية", 
    "source": "WMO Expert Team on Climate Change Indices (ETCCDI)", 
    "classes": {
      "3": [
        "#FFF7BC", 
        "#F5851F", 
        "#662506"
      ], 
      "4": [
        "#FFF7BC", 
        "#FFB643", 
        "#D75807", 
        "#662506"
      ], 
      "5": [
        "#FFF7BC", 
        "#FFCC60", 
        "#F5851F", 
        "#BF4603", 
        "#662506"
      ], 
      "6": [
        "#FFF7BC", 
        "#FFD777", 
        "#FEA231", 
        "#E66910", 
        "#AD3D04", 
        "#662506"
      ], 
      "7": [
        "#FFF7BC", 
        "#FFDE86", 
        "#FFB643", 
        "#F5851F", 
        "#D75807", 
        "#A13804", 
        "#662506"
      ], 
      "8": [
        "#FFF7BC", 
        "#FEE391", 
        "#FEC44F", 
        "#FE9929", 
        "#EC7014", 
        "#CC4C02", 
        "#993404", 
        "#662506"
      ], 
      "9": [
        "#FFF7BC", 
        "#FEE596", 
        "#FFCC60", 
        "#FFA938", 
        "#F5851F", 
        "#E0630D", 
        "#BF4603", 
        "#923205", 
        "#662506"
      ], 
      "10": [
        "#FFF7BC", 
        "#FEE79B", 
        "#FFD26D", 
        "#FFB643", 
        "#FC9527", 
        "#EE7516", 
        "#D75807", 
        "#B54103", 
        "#8D3105", 
        "#662506"
      ], 
      "11": [
        "#FFF7BC", 
        "#FFE99E", 
        "#FFD777", 
        "#FEC04B", 
        "#FEA231", 
        "#F5851F", 
        "#E66910", 
        "#CF5003", 
        "#AD3D04", 
        "#892F05", 
        "#662506"
      ]
    }, 
    "name_en": "Tropical Nights Accumulation", 
    "id": "Temp_Seq_TropicalNights"
  }
]

OTHER_ELEMENTS = [
  {
    "name_ar": "الأمطار والتساقط", 
    "styles": [
      {
        "category": "Sequential", 
        "name_ar": "تدرج الهطول المطري التراكمي القياسي", 
        "source": "ColorBrewer Blues", 
        "classes": {
          "3": [
            "#F7FBFF", 
            "#6BAED6", 
            "#08306B"
          ], 
          "4": [
            "#F7FBFF", 
            "#ACD0E6", 
            "#3987C0", 
            "#08306B"
          ], 
          "5": [
            "#F7FBFF", 
            "#C6DBEF", 
            "#6BAED6", 
            "#2171B5", 
            "#08306B"
          ], 
          "6": [
            "#F7FBFF", 
            "#D0E1F2", 
            "#94C4DF", 
            "#4B98C9", 
            "#1964AB", 
            "#08306B"
          ], 
          "7": [
            "#F7FBFF", 
            "#D6E6F4", 
            "#ACD0E6", 
            "#6BAED6", 
            "#3987C0", 
            "#135BA4", 
            "#08306B"
          ], 
          "8": [
            "#F7FBFF", 
            "#DBE9F6", 
            "#BBD6EB", 
            "#89BEDC", 
            "#559ECD", 
            "#2C7ABA", 
            "#0D55A0", 
            "#08306B"
          ], 
          "9": [
            "#F7FBFF", 
            "#DEEBF7", 
            "#C6DBEF", 
            "#9ECAE1", 
            "#6BAED6", 
            "#4292C6", 
            "#2171B5", 
            "#08519C", 
            "#08306B"
          ], 
          "10": [
            "#F7FBFF", 
            "#E1EDF8", 
            "#CBDFF1", 
            "#ACD0E6", 
            "#83BADB", 
            "#5AA1CF", 
            "#3987C0", 
            "#1D6AAF", 
            "#084D96", 
            "#08306B"
          ], 
          "11": [
            "#F7FBFF", 
            "#E3EEF9", 
            "#D0E1F2", 
            "#B6D4E9", 
            "#94C4DF", 
            "#6BAED6", 
            "#4B98C9", 
            "#307EBC", 
            "#1964AB", 
            "#084A92", 
            "#08306B"
          ]
        }, 
        "name_en": "Cumulative Rainfall Blues", 
        "id": "Precip_Seq_Blues"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تدرج الهطول المناخي السنوي والفصلي", 
        "source": "NOAA ROC / ColorBrewer YlGnBu", 
        "classes": {
          "3": [
            "#FFFFCC", 
            "#41B6C4", 
            "#081D58"
          ], 
          "4": [
            "#FFFFCC", 
            "#99D6B9", 
            "#2280B8", 
            "#081D58"
          ], 
          "5": [
            "#FFFFCC", 
            "#C7E9B4", 
            "#41B6C4", 
            "#225EA8", 
            "#081D58"
          ], 
          "6": [
            "#FFFFCC", 
            "#D6EFB3", 
            "#75C8BD", 
            "#2798C1", 
            "#264DA0", 
            "#081D58"
          ], 
          "7": [
            "#FFFFCC", 
            "#E1F3B2", 
            "#99D6B9", 
            "#41B6C4", 
            "#2280B8", 
            "#26429B", 
            "#081D58"
          ], 
          "8": [
            "#FFFFCC", 
            "#E8F6B1", 
            "#B4E1B6", 
            "#69C3BF", 
            "#30A1C2", 
            "#236CAF", 
            "#263A97", 
            "#081D58"
          ], 
          "9": [
            "#FFFFCC", 
            "#EDF8B1", 
            "#C7E9B4", 
            "#7FCDBB", 
            "#41B6C4", 
            "#1D91C0", 
            "#225EA8", 
            "#253494", 
            "#081D58"
          ], 
          "10": [
            "#FFFFCC", 
            "#EFF9B4", 
            "#D0ECB3", 
            "#99D6B9", 
            "#61C0C0", 
            "#34A5C2", 
            "#2280B8", 
            "#2455A4", 
            "#22318D", 
            "#081D58"
          ], 
          "11": [
            "#FFFFCC", 
            "#F1F9B6", 
            "#D6EFB3", 
            "#ACDEB7", 
            "#75C8BD", 
            "#41B6C4", 
            "#2798C1", 
            "#2372B2", 
            "#264DA0", 
            "#1F2F88", 
            "#081D58"
          ]
        }, 
        "name_en": "Climatological Precipitation", 
        "id": "Precip_Seq_YlGnBu"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تدرج أمطار الرياح الموسمية والهطول الغزير", 
        "source": "ColorBrewer BuPu", 
        "classes": {
          "3": [
            "#F7FCFD", 
            "#8C96C6", 
            "#4D004B"
          ], 
          "4": [
            "#F7FCFD", 
            "#A9C4DE", 
            "#8B5EAA", 
            "#4D004B"
          ], 
          "5": [
            "#F7FCFD", 
            "#BFD3E6", 
            "#8C96C6", 
            "#88419D", 
            "#4D004B"
          ], 
          "6": [
            "#F7FCFD", 
            "#CCDDEC", 
            "#9AB4D6", 
            "#8C74B5", 
            "#863190", 
            "#4D004B"
          ], 
          "7": [
            "#F7FCFD", 
            "#D5E4EF", 
            "#A9C4DE", 
            "#8C96C6", 
            "#8B5EAA", 
            "#842487", 
            "#4D004B"
          ], 
          "8": [
            "#F7FCFD", 
            "#DBE8F2", 
            "#B6CCE3", 
            "#96ACD1", 
            "#8D7EBA", 
            "#8A4EA3", 
            "#821A81", 
            "#4D004B"
          ], 
          "9": [
            "#F7FCFD", 
            "#E0ECF4", 
            "#BFD3E6", 
            "#9EBCDA", 
            "#8C96C6", 
            "#8C6BB1", 
            "#88419D", 
            "#810F7C", 
            "#4D004B"
          ], 
          "10": [
            "#F7FCFD", 
            "#E3EEF5", 
            "#C6D9E9", 
            "#A9C4DE", 
            "#94A7CF", 
            "#8D83BD", 
            "#8B5EAA", 
            "#873896", 
            "#7B0D76", 
            "#4D004B"
          ], 
          "11": [
            "#F7FCFD", 
            "#E5EFF6", 
            "#CCDDEC", 
            "#B2CAE1", 
            "#9AB4D6", 
            "#8C96C6", 
            "#8C74B5", 
            "#8A53A5", 
            "#863190", 
            "#760B72", 
            "#4D004B"
          ]
        }, 
        "name_en": "Monsoon & Heavy Downpours", 
        "id": "Precip_Seq_BuPu"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ وفائض وعجز الأمطار عن المعدل الطبيعي", 
        "source": "ColorBrewer BrBG", 
        "classes": {
          "3": [
            "#BF812D", 
            "#F5F5F5", 
            "#01665E"
          ], 
          "4": [
            "#543005", 
            "#DFC27D", 
            "#80CDC1", 
            "#003C30"
          ], 
          "5": [
            "#543005", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#003C30"
          ], 
          "6": [
            "#543005", 
            "#A5691C", 
            "#DFC27D", 
            "#80CDC1", 
            "#1F7E76", 
            "#003C30"
          ], 
          "7": [
            "#543005", 
            "#A5691C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#1F7E76", 
            "#003C30"
          ], 
          "8": [
            "#543005", 
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#80CDC1", 
            "#35978F", 
            "#01665E", 
            "#003C30"
          ], 
          "9": [
            "#543005", 
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#35978F", 
            "#01665E", 
            "#003C30"
          ], 
          "10": [
            "#543005", 
            "#7E4809", 
            "#A5691C", 
            "#C89142", 
            "#DFC27D", 
            "#80CDC1", 
            "#4AA49B", 
            "#1F7E76", 
            "#015B52", 
            "#003C30"
          ], 
          "11": [
            "#543005", 
            "#7E4809", 
            "#A5691C", 
            "#C89142", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#4AA49B", 
            "#1F7E76", 
            "#015B52", 
            "#003C30"
          ]
        }, 
        "name_en": "Precipitation Departure Anomaly", 
        "id": "Precip_Div_BrBG"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر الهطول القياسي (SPI) للجفاف والرطوبة", 
        "source": "WMO Commission for Agricultural Meteorology (SPI)", 
        "classes": {
          "3": [
            "#FFAA00", 
            "#FFFFFF", 
            "#0070FF"
          ], 
          "4": [
            "#730000", 
            "#FFFF00", 
            "#A6F28F", 
            "#002673"
          ], 
          "5": [
            "#730000", 
            "#FFFF00", 
            "#FFFFFF", 
            "#A6F28F", 
            "#002673"
          ], 
          "6": [
            "#730000", 
            "#F56E00", 
            "#FFFF00", 
            "#A6F28F", 
            "#5F8D92", 
            "#002673"
          ], 
          "7": [
            "#730000", 
            "#F56E00", 
            "#FFFF00", 
            "#FFFFFF", 
            "#A6F28F", 
            "#5F8D92", 
            "#002673"
          ], 
          "8": [
            "#730000", 
            "#E60000", 
            "#FFAA00", 
            "#FFFF00", 
            "#A6F28F", 
            "#38A800", 
            "#0070FF", 
            "#002673"
          ], 
          "9": [
            "#730000", 
            "#E60000", 
            "#FFAA00", 
            "#FFFF00", 
            "#FFFFFF", 
            "#A6F28F", 
            "#38A800", 
            "#0070FF", 
            "#002673"
          ], 
          "10": [
            "#730000", 
            "#C80002", 
            "#F56E00", 
            "#FFC000", 
            "#FFFF00", 
            "#A6F28F", 
            "#58BA33", 
            "#5F8D92", 
            "#015CDA", 
            "#002673"
          ], 
          "11": [
            "#730000", 
            "#C80002", 
            "#F56E00", 
            "#FFC000", 
            "#FFFF00", 
            "#FFFFFF", 
            "#A6F28F", 
            "#58BA33", 
            "#5F8D92", 
            "#015CDA", 
            "#002673"
          ]
        }, 
        "name_en": "Standardized Precipitation Index", 
        "id": "Precip_Div_SPI"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس انعكاسية رادار الطقس الوطني للسيول", 
        "source": "NOAA NWS Radar Operations Center (ROC)", 
        "classes": {
          "3": [
            "#04E9E7", 
            "#E5BC00", 
            "#FFFFFF"
          ], 
          "4": [
            "#04E9E7", 
            "#00A000", 
            "#EF0000", 
            "#FFFFFF"
          ], 
          "5": [
            "#04E9E7", 
            "#01E101", 
            "#E5BC00", 
            "#C80000", 
            "#FFFFFF"
          ], 
          "6": [
            "#04E9E7", 
            "#65D263", 
            "#A9CE00", 
            "#FF6F00", 
            "#CE0038", 
            "#FFFFFF"
          ], 
          "7": [
            "#04E9E7", 
            "#726CBD", 
            "#00A000", 
            "#E5BC00", 
            "#EF0000", 
            "#EE00A7", 
            "#FFFFFF"
          ], 
          "8": [
            "#04E9E7", 
            "#0300F4", 
            "#01C501", 
            "#FDF802", 
            "#FD9500", 
            "#D40000", 
            "#F800FD", 
            "#FFFFFF"
          ], 
          "9": [
            "#04E9E7", 
            "#283FF4", 
            "#01E101", 
            "#5CA900", 
            "#E5BC00", 
            "#FE4500", 
            "#C80000", 
            "#E031EF", 
            "#FFFFFF"
          ], 
          "10": [
            "#04E9E7", 
            "#2F5AF5", 
            "#02F702", 
            "#00A000", 
            "#F8EB01", 
            "#F89E00", 
            "#EF0000", 
            "#BF0000", 
            "#CE3FE4", 
            "#FFFFFF"
          ], 
          "11": [
            "#04E9E7", 
            "#306EF5", 
            "#65D263", 
            "#01BA01", 
            "#A9CE00", 
            "#E5BC00", 
            "#FF6F00", 
            "#DC0000", 
            "#CE0038", 
            "#BF47DC", 
            "#FFFFFF"
          ]
        }, 
        "name_en": "Doppler Radar Reflectivity dBZ", 
        "id": "Precip_Multi_DopplerRadar"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس مخاطر السيول الجارفة والفيضانات المفاجئة", 
        "source": "NOAA National Water Center (NWC)", 
        "classes": {
          "3": [
            "#EDF8FB", 
            "#006D2C", 
            "#7F0000"
          ], 
          "4": [
            "#EDF8FB", 
            "#43AD76", 
            "#FBBF6E", 
            "#7F0000"
          ], 
          "5": [
            "#EDF8FB", 
            "#66C2A4", 
            "#006D2C", 
            "#E78AC3", 
            "#7F0000"
          ], 
          "6": [
            "#EDF8FB", 
            "#86CFBC", 
            "#259755", 
            "#D2C330", 
            "#ED667F", 
            "#7F0000"
          ], 
          "7": [
            "#EDF8FB", 
            "#9AD7CD", 
            "#43AD76", 
            "#006D2C", 
            "#FBBF6E", 
            "#EB4B54", 
            "#7F0000"
          ], 
          "8": [
            "#EDF8FB", 
            "#A8DDD9", 
            "#58B990", 
            "#1C8B49", 
            "#A0AB31", 
            "#F2A1A1", 
            "#E83335", 
            "#7F0000"
          ], 
          "9": [
            "#EDF8FB", 
            "#B2E2E2", 
            "#66C2A4", 
            "#2CA25F", 
            "#006D2C", 
            "#FFD92F", 
            "#E78AC3", 
            "#E41A1C", 
            "#7F0000"
          ], 
          "10": [
            "#EDF8FB", 
            "#B9E4E5", 
            "#78C9B2", 
            "#43AD76", 
            "#178442", 
            "#849D30", 
            "#FBBF6E", 
            "#EC769D", 
            "#D81719", 
            "#7F0000"
          ], 
          "11": [
            "#EDF8FB", 
            "#BEE6E7", 
            "#86CFBC", 
            "#52B588", 
            "#259755", 
            "#006D2C", 
            "#D2C330", 
            "#F6AA92", 
            "#ED667F", 
            "#CF1417", 
            "#7F0000"
          ]
        }, 
        "name_en": "Flash Flood Guidance Risk", 
        "id": "Precip_Multi_FlashFlood"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج تراكم الثلوج والكتل الجليدية", 
        "source": "National Snow and Ice Data Center (NSIDC)", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#63B7C7", 
            "#1F1A3A"
          ], 
          "4": [
            "#FFFFFF", 
            "#A7DCBF", 
            "#257BB6", 
            "#1F1A3A"
          ], 
          "5": [
            "#FFFFFF", 
            "#C4E8CB", 
            "#63B7C7", 
            "#095EA1", 
            "#1F1A3A"
          ], 
          "6": [
            "#FFFFFF", 
            "#D1EDE0", 
            "#89D1C2", 
            "#3B96C4", 
            "#095092", 
            "#1F1A3A"
          ], 
          "7": [
            "#FFFFFF", 
            "#DAF1EE", 
            "#A7DCBF", 
            "#63B7C7", 
            "#257BB6", 
            "#094688", 
            "#1F1A3A"
          ], 
          "8": [
            "#FFFFFF", 
            "#E0F3F8", 
            "#BAE4BC", 
            "#7BCCC4", 
            "#43A2CA", 
            "#0868AC", 
            "#084081", 
            "#1F1A3A"
          ], 
          "9": [
            "#FFFFFF", 
            "#E4F5F9", 
            "#C4E8CB", 
            "#95D5C1", 
            "#63B7C7", 
            "#348CBF", 
            "#095EA1", 
            "#123B78", 
            "#1F1A3A"
          ], 
          "10": [
            "#FFFFFF", 
            "#E7F6FA", 
            "#CBEBD7", 
            "#A7DCBF", 
            "#76C7C5", 
            "#4BA7C9", 
            "#257BB6", 
            "#0A5699", 
            "#163770", 
            "#1F1A3A"
          ], 
          "11": [
            "#FFFFFF", 
            "#E9F7FA", 
            "#D1EDE0", 
            "#B4E2BD", 
            "#89D1C2", 
            "#63B7C7", 
            "#3B96C4", 
            "#146EAF", 
            "#095092", 
            "#19346B", 
            "#1F1A3A"
          ]
        }, 
        "name_en": "Cryospheric Snow & Glacial", 
        "id": "Precip_Multi_SnowIce"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج قياس الهطول العالمي عبر أقمار ناسا GPM", 
        "source": "NASA Global Precipitation Measurement (GPM)", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#163E89", 
            "#3A0CA3"
          ], 
          "4": [
            "#FFFFFF", 
            "#079FCD", 
            "#AE1279", 
            "#3A0CA3"
          ], 
          "5": [
            "#FFFFFF", 
            "#42BFDE", 
            "#163E89", 
            "#DA1A92", 
            "#3A0CA3"
          ], 
          "6": [
            "#FFFFFF", 
            "#6BCEE6", 
            "#0483BD", 
            "#480366", 
            "#AF0CA3", 
            "#3A0CA3"
          ], 
          "7": [
            "#FFFFFF", 
            "#81D9EB", 
            "#079FCD", 
            "#163E89", 
            "#AE1279", 
            "#8E08AF", 
            "#3A0CA3"
          ], 
          "8": [
            "#FFFFFF", 
            "#90E0EF", 
            "#00B4D8", 
            "#0077B6", 
            "#03045E", 
            "#F72585", 
            "#7209B7", 
            "#3A0CA3"
          ], 
          "9": [
            "#FFFFFF", 
            "#A0E4F1", 
            "#42BFDE", 
            "#078DC3", 
            "#163E89", 
            "#70056D", 
            "#DA1A92", 
            "#6C09B4", 
            "#3A0CA3"
          ], 
          "10": [
            "#FFFFFF", 
            "#ABE7F3", 
            "#5BC7E2", 
            "#079FCD", 
            "#0D6AAC", 
            "#0A1367", 
            "#AE1279", 
            "#C3129C", 
            "#670AB3", 
            "#3A0CA3"
          ], 
          "11": [
            "#FFFFFF", 
            "#B5E9F4", 
            "#6BCEE6", 
            "#03AED5", 
            "#0483BD", 
            "#163E89", 
            "#480366", 
            "#E11F81", 
            "#AF0CA3", 
            "#630AB1", 
            "#3A0CA3"
          ]
        }, 
        "name_en": "NASA GPM IMERG Precipitation", 
        "id": "Precip_Multi_NASA_GPM"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تدرج مراقبة الأمطار عالي الدقة CHIRPS", 
        "source": "Climate Hazards Center / UCSB", 
        "classes": {
          "3": [
            "#E8F6F3", 
            "#31A991", 
            "#0B4C3F"
          ], 
          "4": [
            "#E8F6F3", 
            "#65C0AE", 
            "#13856F", 
            "#0B4C3F"
          ], 
          "5": [
            "#E8F6F3", 
            "#7FCBBC", 
            "#31A991", 
            "#10725F", 
            "#0B4C3F"
          ], 
          "6": [
            "#E8F6F3", 
            "#90D1C4", 
            "#4FB7A2", 
            "#15987E", 
            "#0F6B59", 
            "#0B4C3F"
          ], 
          "7": [
            "#E8F6F3", 
            "#9AD6CA", 
            "#65C0AE", 
            "#31A991", 
            "#13856F", 
            "#0F6654", 
            "#0B4C3F"
          ], 
          "8": [
            "#E8F6F3", 
            "#A2D9CE", 
            "#73C6B6", 
            "#45B39D", 
            "#16A085", 
            "#117864", 
            "#0E6251", 
            "#0B4C3F"
          ], 
          "9": [
            "#E8F6F3", 
            "#ABDDD3", 
            "#7FCBBC", 
            "#58BAA6", 
            "#31A991", 
            "#149178", 
            "#10725F", 
            "#0E5F4F", 
            "#0B4C3F"
          ], 
          "10": [
            "#E8F6F3", 
            "#B2DFD6", 
            "#89CEC1", 
            "#65C0AE", 
            "#41B19A", 
            "#1EA288", 
            "#13856F", 
            "#106E5B", 
            "#0D5D4D", 
            "#0B4C3F"
          ], 
          "11": [
            "#E8F6F3", 
            "#B7E2D9", 
            "#90D1C4", 
            "#6FC4B3", 
            "#4FB7A2", 
            "#31A991", 
            "#15987E", 
            "#127C67", 
            "#0F6B59", 
            "#0D5B4C", 
            "#0B4C3F"
          ]
        }, 
        "name_en": "CHIRPS High-Resolution Rainfall", 
        "id": "Precip_Seq_CHIRPS_Rain"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج إجمالي الهطول المطري لنموذج ERA5 العالمي", 
        "source": "ECMWF Copernicus Climate Change Service", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#347CB8", 
            "#49006A"
          ], 
          "4": [
            "#FFFFFF", 
            "#7AB4D5", 
            "#0E4179", 
            "#49006A"
          ], 
          "5": [
            "#FFFFFF", 
            "#A2CDE3", 
            "#347CB8", 
            "#19275B", 
            "#49006A"
          ], 
          "6": [
            "#FFFFFF", 
            "#B8D8E9", 
            "#569DC8", 
            "#1B5B9C", 
            "#261854", 
            "#49006A"
          ], 
          "7": [
            "#FFFFFF", 
            "#C7E0ED", 
            "#7AB4D5", 
            "#347CB8", 
            "#0E4179", 
            "#2A0B4F", 
            "#49006A"
          ], 
          "8": [
            "#FFFFFF", 
            "#D1E5F0", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061", 
            "#2D004B", 
            "#49006A"
          ], 
          "9": [
            "#FFFFFF", 
            "#D7E8F2", 
            "#A2CDE3", 
            "#64A5CD", 
            "#347CB8", 
            "#17518F", 
            "#19275B", 
            "#30004F", 
            "#49006A"
          ], 
          "10": [
            "#FFFFFF", 
            "#DBEBF3", 
            "#AFD3E6", 
            "#7AB4D5", 
            "#408EC0", 
            "#266BAF", 
            "#0E4179", 
            "#211F57", 
            "#330052", 
            "#49006A"
          ], 
          "11": [
            "#FFFFFF", 
            "#DFEDF4", 
            "#B8D8E9", 
            "#8BC0DB", 
            "#569DC8", 
            "#347CB8", 
            "#1B5B9C", 
            "#073568", 
            "#261854", 
            "#350054", 
            "#49006A"
          ]
        }, 
        "name_en": "ECMWF ERA5 Total Precipitation", 
        "id": "Precip_Multi_ERA5_Total"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مقياس شدة الأمطار الساعية للمنظمة العالمية للأرصاد", 
        "source": "WMO-No. 8 Guide to Meteorological Instruments", 
        "classes": {
          "3": [
            "#E0F7FA", 
            "#17B9CD", 
            "#006064"
          ], 
          "4": [
            "#E0F7FA", 
            "#4ECEDF", 
            "#009EB0", 
            "#006064"
          ], 
          "5": [
            "#E0F7FA", 
            "#6FD8E6", 
            "#17B9CD", 
            "#008D9B", 
            "#006064"
          ], 
          "6": [
            "#E0F7FA", 
            "#80DEEA", 
            "#26C6DA", 
            "#00ACC1", 
            "#00838F", 
            "#006064"
          ], 
          "7": [
            "#E0F7FA", 
            "#92E2ED", 
            "#4ECEDF", 
            "#17B9CD", 
            "#009EB0", 
            "#007D88", 
            "#006064"
          ], 
          "8": [
            "#E0F7FA", 
            "#9FE5EF", 
            "#62D4E3", 
            "#22C2D6", 
            "#08B0C5", 
            "#0094A4", 
            "#007982", 
            "#006064"
          ], 
          "9": [
            "#E0F7FA", 
            "#A7E8F0", 
            "#6FD8E6", 
            "#38C9DC", 
            "#17B9CD", 
            "#00A7BB", 
            "#008D9B", 
            "#00767F", 
            "#006064"
          ], 
          "10": [
            "#E0F7FA", 
            "#AEE9F1", 
            "#79DBE8", 
            "#4ECEDF", 
            "#20C0D4", 
            "#0CB2C7", 
            "#009EB0", 
            "#008794", 
            "#00737C", 
            "#006064"
          ], 
          "11": [
            "#E0F7FA", 
            "#B3EBF2", 
            "#80DEEA", 
            "#5CD2E2", 
            "#26C6DA", 
            "#17B9CD", 
            "#00ACC1", 
            "#0097A8", 
            "#00838F", 
            "#007179", 
            "#006064"
          ]
        }, 
        "name_en": "WMO Hourly Rainfall Intensity", 
        "id": "Precip_Seq_Intensity_WMO"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر الجفاف والفيضان متعدد المقاييس الزمنية SPEI", 
        "source": "Vicente-Serrano et al. (SPEI Global)", 
        "classes": {
          "3": [
            "#DFC27D", 
            "#F5F5F5", 
            "#35978F"
          ], 
          "4": [
            "#8C510A", 
            "#F6E8C3", 
            "#C7EAE5", 
            "#01665E"
          ], 
          "5": [
            "#8C510A", 
            "#F6E8C3", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#01665E"
          ], 
          "6": [
            "#8C510A", 
            "#D0A155", 
            "#F6E8C3", 
            "#C7EAE5", 
            "#5CB2A8", 
            "#01665E"
          ], 
          "7": [
            "#8C510A", 
            "#D0A155", 
            "#F6E8C3", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#5CB2A8", 
            "#01665E"
          ], 
          "8": [
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F6E8C3", 
            "#C7EAE5", 
            "#80CDC1", 
            "#35978F", 
            "#01665E"
          ], 
          "9": [
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F6E8C3", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#80CDC1", 
            "#35978F", 
            "#01665E"
          ], 
          "10": [
            "#8C510A", 
            "#B27525", 
            "#D0A155", 
            "#E5CB8E", 
            "#F6E8C3", 
            "#C7EAE5", 
            "#93D4CA", 
            "#5CB2A8", 
            "#2A8A82", 
            "#01665E"
          ], 
          "11": [
            "#8C510A", 
            "#B27525", 
            "#D0A155", 
            "#E5CB8E", 
            "#F6E8C3", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#93D4CA", 
            "#5CB2A8", 
            "#2A8A82", 
            "#01665E"
          ]
        }, 
        "name_en": "Multi-scalar SPEI Drought/Wet", 
        "id": "Precip_Div_SPEI_Multi"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "المكافئ المائي للغطاء الثلجي والهيدرولوجيا", 
        "source": "USDA NRCS SNOTEL / NASA SnowEx", 
        "classes": {
          "3": [
            "#F7FBFF", 
            "#86BCDC", 
            "#084594"
          ], 
          "4": [
            "#F7FBFF", 
            "#B9D5EA", 
            "#519BCB", 
            "#084594"
          ], 
          "5": [
            "#F7FBFF", 
            "#CCDFF1", 
            "#86BCDC", 
            "#3B8AC2", 
            "#084594"
          ], 
          "6": [
            "#F7FBFF", 
            "#D4E5F4", 
            "#A6CDE4", 
            "#63A8D3", 
            "#307EBC", 
            "#084594"
          ], 
          "7": [
            "#F7FBFF", 
            "#DAE8F6", 
            "#B9D5EA", 
            "#86BCDC", 
            "#519BCB", 
            "#2876B8", 
            "#084594"
          ], 
          "8": [
            "#F7FBFF", 
            "#DEEBF7", 
            "#C6DBEF", 
            "#9ECAE1", 
            "#6BAED6", 
            "#4292C6", 
            "#2171B5", 
            "#084594"
          ], 
          "9": [
            "#F7FBFF", 
            "#E1EDF8", 
            "#CCDFF1", 
            "#ADD0E6", 
            "#86BCDC", 
            "#5DA3D0", 
            "#3B8AC2", 
            "#1F6BB1", 
            "#084594"
          ], 
          "10": [
            "#F7FBFF", 
            "#E4EFF9", 
            "#D1E2F3", 
            "#B9D5EA", 
            "#99C7E0", 
            "#71B1D7", 
            "#519BCB", 
            "#3583BE", 
            "#1D67AE", 
            "#084594"
          ], 
          "11": [
            "#F7FBFF", 
            "#E6F0F9", 
            "#D4E5F4", 
            "#C2D9EE", 
            "#A6CDE4", 
            "#86BCDC", 
            "#63A8D3", 
            "#4795C8", 
            "#307EBC", 
            "#1C64AB", 
            "#084594"
          ]
        }, 
        "name_en": "Snow Water Equivalent SWE", 
        "id": "Precip_Seq_SWE_Snowpack"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس السحب الحملية الركامية والسيول الوميضية", 
        "source": "NOAA Storm Prediction Center (SPC)", 
        "classes": {
          "3": [
            "#C7EAE5", 
            "#FF9C00", 
            "#4A004A"
          ], 
          "4": [
            "#C7EAE5", 
            "#738751", 
            "#DD3200", 
            "#4A004A"
          ], 
          "5": [
            "#C7EAE5", 
            "#1F7971", 
            "#FF9C00", 
            "#B70002", 
            "#4A004A"
          ], 
          "6": [
            "#C7EAE5", 
            "#3C948C", 
            "#D6B730", 
            "#F55800", 
            "#9A0002", 
            "#4A004A"
          ], 
          "7": [
            "#C7EAE5", 
            "#4EA69E", 
            "#738751", 
            "#FF9C00", 
            "#DD3200", 
            "#870001", 
            "#4A004A"
          ], 
          "8": [
            "#C7EAE5", 
            "#5AB4AC", 
            "#01665E", 
            "#FFCC00", 
            "#FF6600", 
            "#CC0000", 
            "#7A0000", 
            "#4A004A"
          ], 
          "9": [
            "#C7EAE5", 
            "#69BBB3", 
            "#1F7971", 
            "#B1A540", 
            "#FF9C00", 
            "#EC4B00", 
            "#B70002", 
            "#75000E", 
            "#4A004A"
          ], 
          "10": [
            "#C7EAE5", 
            "#74C0B8", 
            "#308880", 
            "#738751", 
            "#FFC200", 
            "#FF7300", 
            "#DD3200", 
            "#A70002", 
            "#710016", 
            "#4A004A"
          ], 
          "11": [
            "#C7EAE5", 
            "#7DC4BD", 
            "#3C948C", 
            "#38705B", 
            "#D6B730", 
            "#FF9C00", 
            "#F55800", 
            "#D11700", 
            "#9A0002", 
            "#6E001C", 
            "#4A004A"
          ]
        }, 
        "name_en": "Severe Convective Cloudburst", 
        "id": "Precip_Multi_ConvectiveStorm"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ الرياح الموسمية المدارية وفترات الانقطاع", 
        "source": "Indian Meteorological Department / WMO Monsoon", 
        "classes": {
          "3": [
            "#DFC27D", 
            "#F5F5F5", 
            "#018571"
          ], 
          "4": [
            "#A6611A", 
            "#DFC27D", 
            "#80CDC1", 
            "#018571"
          ], 
          "5": [
            "#A6611A", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#018571"
          ], 
          "6": [
            "#A6611A", 
            "#C4914C", 
            "#DFC27D", 
            "#80CDC1", 
            "#4EA898", 
            "#018571"
          ], 
          "7": [
            "#A6611A", 
            "#C4914C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#4EA898", 
            "#018571"
          ], 
          "8": [
            "#A6611A", 
            "#BA813B", 
            "#CDA15C", 
            "#DFC27D", 
            "#80CDC1", 
            "#5FB5A5", 
            "#3C9D8B", 
            "#018571"
          ], 
          "9": [
            "#A6611A", 
            "#BA813B", 
            "#CDA15C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#5FB5A5", 
            "#3C9D8B", 
            "#018571"
          ], 
          "10": [
            "#A6611A", 
            "#B57933", 
            "#C4914C", 
            "#D2A964", 
            "#DFC27D", 
            "#80CDC1", 
            "#67BBAC", 
            "#4EA898", 
            "#319784", 
            "#018571"
          ], 
          "11": [
            "#A6611A", 
            "#B57933", 
            "#C4914C", 
            "#D2A964", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#67BBAC", 
            "#4EA898", 
            "#319784", 
            "#018571"
          ]
        }, 
        "name_en": "Tropical Monsoon Anomaly", 
        "id": "Precip_Div_MonsoonAnomaly"
      }
    ], 
    "folder": "02_Precipitation", 
    "name_en": "Precipitation"
  }, 
  {
    "name_ar": "الضغط عند مستوى سطح البحر", 
    "styles": [
      {
        "category": "Diverging", 
        "name_ar": "مقياس الضغط الجوي المتباعد عند 1013.25 مليبار", 
        "source": "WMO Synoptic Standards (1013.25 hPa)", 
        "classes": {
          "3": [
            "#D6604D", 
            "#F7F7F7", 
            "#2166AC"
          ], 
          "4": [
            "#67001F", 
            "#F4A582", 
            "#92C5DE", 
            "#053061"
          ], 
          "5": [
            "#67001F", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#053061"
          ], 
          "6": [
            "#67001F", 
            "#C4413C", 
            "#F4A582", 
            "#92C5DE", 
            "#347CB8", 
            "#053061"
          ], 
          "7": [
            "#67001F", 
            "#C4413C", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#347CB8", 
            "#053061"
          ], 
          "8": [
            "#67001F", 
            "#B2182B", 
            "#D6604D", 
            "#F4A582", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061"
          ], 
          "9": [
            "#67001F", 
            "#B2182B", 
            "#D6604D", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061"
          ], 
          "10": [
            "#67001F", 
            "#9F1128", 
            "#C4413C", 
            "#DE725A", 
            "#F4A582", 
            "#92C5DE", 
            "#5A9FCA", 
            "#347CB8", 
            "#1A5899", 
            "#053061"
          ], 
          "11": [
            "#67001F", 
            "#9F1128", 
            "#C4413C", 
            "#DE725A", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#5A9FCA", 
            "#347CB8", 
            "#1A5899", 
            "#053061"
          ]
        }, 
        "name_en": "WMO MSLP Diverging", 
        "id": "Pres_Div_WMO_MSLP"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "تدرج المنخفضات والمرتفعات الجوية السينوبتيكية", 
        "source": "NOAA Ocean Prediction Center (OPC)", 
        "classes": {
          "3": [
            "#F46D43", 
            "#FFFFBF", 
            "#4575B4"
          ], 
          "4": [
            "#A50026", 
            "#FDAE61", 
            "#ABD9E9", 
            "#313695"
          ], 
          "5": [
            "#A50026", 
            "#FDAE61", 
            "#FFFFBF", 
            "#ABD9E9", 
            "#313695"
          ], 
          "6": [
            "#A50026", 
            "#E65135", 
            "#FDAE61", 
            "#ABD9E9", 
            "#5E91C3", 
            "#313695"
          ], 
          "7": [
            "#A50026", 
            "#E65135", 
            "#FDAE61", 
            "#FFFFBF", 
            "#ABD9E9", 
            "#5E91C3", 
            "#313695"
          ], 
          "8": [
            "#A50026", 
            "#D73027", 
            "#F46D43", 
            "#FDAE61", 
            "#ABD9E9", 
            "#74ADD1", 
            "#4575B4", 
            "#313695"
          ], 
          "9": [
            "#A50026", 
            "#D73027", 
            "#F46D43", 
            "#FDAE61", 
            "#FFFFBF", 
            "#ABD9E9", 
            "#74ADD1", 
            "#4575B4", 
            "#313695"
          ], 
          "10": [
            "#A50026", 
            "#CA2727", 
            "#E65135", 
            "#F77E4A", 
            "#FDAE61", 
            "#ABD9E9", 
            "#82B8D7", 
            "#5E91C3", 
            "#4265AC", 
            "#313695"
          ], 
          "11": [
            "#A50026", 
            "#CA2727", 
            "#E65135", 
            "#F77E4A", 
            "#FDAE61", 
            "#FFFFBF", 
            "#ABD9E9", 
            "#82B8D7", 
            "#5E91C3", 
            "#4265AC", 
            "#313695"
          ]
        }, 
        "name_en": "Synoptic Highs & Lows", 
        "id": "Pres_Synoptic_HighLow"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج المنخفضات المدارية العميقة ومراكز الأعاصير", 
        "source": "National Hurricane Center (NHC)", 
        "classes": {
          "3": [
            "#49006A", 
            "#F768A1", 
            "#FFFFFF"
          ], 
          "4": [
            "#49006A", 
            "#CD278F", 
            "#FBACB9", 
            "#FFFFFF"
          ], 
          "5": [
            "#49006A", 
            "#AE017E", 
            "#F768A1", 
            "#FCC5C0", 
            "#FFFFFF"
          ], 
          "6": [
            "#49006A", 
            "#99017B", 
            "#E24099", 
            "#FA95B1", 
            "#FDD0CC", 
            "#FFFFFF"
          ], 
          "7": [
            "#49006A", 
            "#8B0179", 
            "#CD278F", 
            "#F768A1", 
            "#FBACB9", 
            "#FDD7D3", 
            "#FFFFFF"
          ], 
          "8": [
            "#49006A", 
            "#820178", 
            "#BB1585", 
            "#E84D9B", 
            "#F989AC", 
            "#FCBABD", 
            "#FDDCD9", 
            "#FFFFFF"
          ], 
          "9": [
            "#49006A", 
            "#7A0177", 
            "#AE017E", 
            "#DD3497", 
            "#F768A1", 
            "#FA9FB5", 
            "#FCC5C0", 
            "#FDE0DD", 
            "#FFFFFF"
          ], 
          "10": [
            "#49006A", 
            "#750176", 
            "#A3017C", 
            "#CD278F", 
            "#EC539D", 
            "#F982AA", 
            "#FBACB9", 
            "#FCCBC6", 
            "#FDE3E1", 
            "#FFFFFF"
          ], 
          "11": [
            "#49006A", 
            "#700074", 
            "#99017B", 
            "#C11B88", 
            "#E24099", 
            "#F768A1", 
            "#FA95B1", 
            "#FBB6BC", 
            "#FDD0CC", 
            "#FEE6E4", 
            "#FFFFFF"
          ]
        }, 
        "name_en": "Tropical Cyclones & Depressions", 
        "id": "Pres_Multi_Cyclones"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تدرج كثافة الهواء والباروكلينيكية الجوية", 
        "source": "CPT-City Isobaric Archive", 
        "classes": {
          "3": [
            "#FFF7EC", 
            "#FC8D59", 
            "#7F0000"
          ], 
          "4": [
            "#FFF7EC", 
            "#FDC38D", 
            "#E7553A", 
            "#7F0000"
          ], 
          "5": [
            "#FFF7EC", 
            "#FDD49E", 
            "#FC8D59", 
            "#D7301F", 
            "#7F0000"
          ], 
          "6": [
            "#FFF7EC", 
            "#FEDCAF", 
            "#FDB27B", 
            "#F26D4B", 
            "#C92113", 
            "#7F0000"
          ], 
          "7": [
            "#FFF7EC", 
            "#FEE1BA", 
            "#FDC38D", 
            "#FC8D59", 
            "#E7553A", 
            "#BF160A", 
            "#7F0000"
          ], 
          "8": [
            "#FFF7EC", 
            "#FEE5C2", 
            "#FDCD97", 
            "#FDA871", 
            "#F5774F", 
            "#DE412B", 
            "#B80A04", 
            "#7F0000"
          ], 
          "9": [
            "#FFF7EC", 
            "#FEE8C8", 
            "#FDD49E", 
            "#FDBB84", 
            "#FC8D59", 
            "#EF6548", 
            "#D7301F", 
            "#B30000", 
            "#7F0000"
          ], 
          "10": [
            "#FFF7EC", 
            "#FEEACC", 
            "#FDD8A7", 
            "#FDC38D", 
            "#FDA26C", 
            "#F67C51", 
            "#E7553A", 
            "#CF2818", 
            "#AD0000", 
            "#7F0000"
          ], 
          "11": [
            "#FFF7EC", 
            "#FEEBCF", 
            "#FEDCAF", 
            "#FDCA94", 
            "#FDB27B", 
            "#FC8D59", 
            "#F26D4B", 
            "#E1472F", 
            "#C92113", 
            "#A80001", 
            "#7F0000"
          ]
        }, 
        "name_en": "Isobaric Air Density", 
        "id": "Pres_Seq_Density"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "المنخفضات الجوية الشديدة والأعاصير الحلزونية", 
        "source": "WMO Severe Weather Information Centre", 
        "classes": {
          "3": [
            "#998EC3", 
            "#F7F7F7", 
            "#F1A340"
          ], 
          "4": [
            "#542788", 
            "#D8DAEB", 
            "#FEE0B6", 
            "#B35806"
          ], 
          "5": [
            "#542788", 
            "#D8DAEB", 
            "#F7F7F7", 
            "#FEE0B6", 
            "#B35806"
          ], 
          "6": [
            "#542788", 
            "#998EC3", 
            "#D8DAEB", 
            "#FEE0B6", 
            "#F1A340", 
            "#B35806"
          ], 
          "7": [
            "#542788", 
            "#998EC3", 
            "#D8DAEB", 
            "#F7F7F7", 
            "#FEE0B6", 
            "#F1A340", 
            "#B35806"
          ], 
          "8": [
            "#542788", 
            "#836CAF", 
            "#AEA7D0", 
            "#D8DAEB", 
            "#FEE0B6", 
            "#F8B769", 
            "#DC8A2E", 
            "#B35806"
          ], 
          "9": [
            "#542788", 
            "#836CAF", 
            "#AEA7D0", 
            "#D8DAEB", 
            "#F7F7F7", 
            "#FEE0B6", 
            "#F8B769", 
            "#DC8A2E", 
            "#B35806"
          ], 
          "10": [
            "#542788", 
            "#785BA5", 
            "#998EC3", 
            "#B9B3D7", 
            "#D8DAEB", 
            "#FEE0B6", 
            "#FAC17C", 
            "#F1A340", 
            "#D27D25", 
            "#B35806"
          ], 
          "11": [
            "#542788", 
            "#785BA5", 
            "#998EC3", 
            "#B9B3D7", 
            "#D8DAEB", 
            "#F7F7F7", 
            "#FEE0B6", 
            "#FAC17C", 
            "#F1A340", 
            "#D27D25", 
            "#B35806"
          ]
        }, 
        "name_en": "Severe Cyclone Deep Core", 
        "id": "Pres_Div_SevereCyclone"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "المرتفعات شبه المدارية وحزام الضغط المرتفع الآزوري", 
        "source": "Hadley Circulation Pressure Climatology", 
        "classes": {
          "3": [
            "#EDF8FB", 
            "#8C96C6", 
            "#810F7C"
          ], 
          "4": [
            "#EDF8FB", 
            "#A6BAD9", 
            "#8B6CB1", 
            "#810F7C"
          ], 
          "5": [
            "#EDF8FB", 
            "#B3CDE3", 
            "#8C96C6", 
            "#8856A7", 
            "#810F7C"
          ], 
          "6": [
            "#EDF8FB", 
            "#BFD5E8", 
            "#9CACD2", 
            "#8C7DBA", 
            "#874B9E", 
            "#810F7C"
          ], 
          "7": [
            "#EDF8FB", 
            "#C6DBEB", 
            "#A6BAD9", 
            "#8C96C6", 
            "#8B6CB1", 
            "#874398", 
            "#810F7C"
          ], 
          "8": [
            "#EDF8FB", 
            "#CCDFED", 
            "#ADC5DF", 
            "#97A5CE", 
            "#8C84BD", 
            "#8960AB", 
            "#863D94", 
            "#810F7C"
          ], 
          "9": [
            "#EDF8FB", 
            "#D0E2EF", 
            "#B3CDE3", 
            "#A0B1D4", 
            "#8C96C6", 
            "#8B77B6", 
            "#8856A7", 
            "#863991", 
            "#810F7C"
          ], 
          "10": [
            "#EDF8FB", 
            "#D3E5F0", 
            "#B9D2E6", 
            "#A6BAD9", 
            "#95A2CC", 
            "#8C88BF", 
            "#8B6CB1", 
            "#8850A2", 
            "#85358F", 
            "#810F7C"
          ], 
          "11": [
            "#EDF8FB", 
            "#D6E7F1", 
            "#BFD5E8", 
            "#ABC2DD", 
            "#9CACD2", 
            "#8C96C6", 
            "#8C7DBA", 
            "#8A63AD", 
            "#874B9E", 
            "#85328D", 
            "#810F7C"
          ]
        }, 
        "name_en": "Subtropical High Belts", 
        "id": "Pres_Synoptic_Subtropical"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "المرتفع السيبيري الشتوي مقابل منخفضات المتوسط", 
        "source": "Synoptic Climatology of Eurasia & North Africa", 
        "classes": {
          "3": [
            "#4575B4", 
            "#FFFFBF", 
            "#F46D43"
          ], 
          "4": [
            "#313695", 
            "#74ADD1", 
            "#FDAE61", 
            "#A50026"
          ], 
          "5": [
            "#313695", 
            "#74ADD1", 
            "#FFFFBF", 
            "#FDAE61", 
            "#A50026"
          ], 
          "6": [
            "#313695", 
            "#4575B4", 
            "#74ADD1", 
            "#FDAE61", 
            "#F46D43", 
            "#A50026"
          ], 
          "7": [
            "#313695", 
            "#4575B4", 
            "#74ADD1", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F46D43", 
            "#A50026"
          ], 
          "8": [
            "#313695", 
            "#4060AA", 
            "#5687BE", 
            "#74ADD1", 
            "#FDAE61", 
            "#F8844D", 
            "#D95039", 
            "#A50026"
          ], 
          "9": [
            "#313695", 
            "#4060AA", 
            "#5687BE", 
            "#74ADD1", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F8844D", 
            "#D95039", 
            "#A50026"
          ], 
          "10": [
            "#313695", 
            "#3D55A5", 
            "#4575B4", 
            "#5E91C3", 
            "#74ADD1", 
            "#FDAE61", 
            "#F98F52", 
            "#F46D43", 
            "#CC4234", 
            "#A50026"
          ], 
          "11": [
            "#313695", 
            "#3D55A5", 
            "#4575B4", 
            "#5E91C3", 
            "#74ADD1", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F98F52", 
            "#F46D43", 
            "#CC4234", 
            "#A50026"
          ]
        }, 
        "name_en": "Siberian High vs Mediterranean", 
        "id": "Pres_Div_SiberianAnticyclone"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج خطوط تساوي الضغط عالي الدقة (2 مليبار)", 
        "source": "NOAA High-Resolution Rapid Refresh (HRRR)", 
        "classes": {
          "3": [
            "#2B83BA", 
            "#FFFFBF", 
            "#D53E4F"
          ], 
          "4": [
            "#2B83BA", 
            "#D3ED9C", 
            "#FECF7D", 
            "#D53E4F"
          ], 
          "5": [
            "#2B83BA", 
            "#ABDDA4", 
            "#FFFFBF", 
            "#FDAE61", 
            "#D53E4F"
          ], 
          "6": [
            "#2B83BA", 
            "#91C9A9", 
            "#EBF7A0", 
            "#FFE695", 
            "#FA9555", 
            "#D53E4F"
          ], 
          "7": [
            "#2B83BA", 
            "#7EBBAC", 
            "#D3ED9C", 
            "#FFFFBF", 
            "#FECF7D", 
            "#F8844D", 
            "#D53E4F"
          ], 
          "8": [
            "#2B83BA", 
            "#70B2AF", 
            "#BDE4A1", 
            "#F1F9A9", 
            "#FFEDA1", 
            "#FEBC6D", 
            "#F67747", 
            "#D53E4F"
          ], 
          "9": [
            "#2B83BA", 
            "#64ABB0", 
            "#ABDDA4", 
            "#E6F598", 
            "#FFFFBF", 
            "#FEE08B", 
            "#FDAE61", 
            "#F46D43", 
            "#D53E4F"
          ], 
          "10": [
            "#2B83BA", 
            "#5FA6B1", 
            "#9DD2A7", 
            "#D3ED9C", 
            "#F4FBAE", 
            "#FFF1A8", 
            "#FECF7D", 
            "#FCA05A", 
            "#F16845", 
            "#D53E4F"
          ], 
          "11": [
            "#2B83BA", 
            "#5CA3B2", 
            "#91C9A9", 
            "#C3E79F", 
            "#EBF7A0", 
            "#FFFFBF", 
            "#FFE695", 
            "#FEC272", 
            "#FA9555", 
            "#EE6446", 
            "#D53E4F"
          ]
        }, 
        "name_en": "High-Resolution Microbar Isobars", 
        "id": "Pres_Multi_MicrobarIsobars"
      }
    ], 
    "folder": "03_Sea_Level_Pressure", 
    "name_en": "Sea Level Pressure"
  }, 
  {
    "name_ar": "الضغط الجوي السطحي", 
    "styles": [
      {
        "category": "Sequential", 
        "name_ar": "تدرج الضغط السطحي الهبسومتري المرتبط بالتضاريس", 
        "source": "ICAO Standard Atmosphere Model", 
        "classes": {
          "3": [
            "#003C30", 
            "#E0E9D4", 
            "#543005"
          ], 
          "4": [
            "#003C30", 
            "#80CDC1", 
            "#DFC27D", 
            "#543005"
          ], 
          "5": [
            "#003C30", 
            "#4AA49B", 
            "#E0E9D4", 
            "#C89142", 
            "#543005"
          ], 
          "6": [
            "#003C30", 
            "#2C8D85", 
            "#ABDED6", 
            "#EDD9A7", 
            "#B57726", 
            "#543005"
          ], 
          "7": [
            "#003C30", 
            "#1F7E76", 
            "#80CDC1", 
            "#E0E9D4", 
            "#DFC27D", 
            "#A5691C", 
            "#543005"
          ], 
          "8": [
            "#003C30", 
            "#14746C", 
            "#62B6AB", 
            "#BDE6E0", 
            "#F3E2B9", 
            "#D2A65B", 
            "#9A5E15", 
            "#543005"
          ], 
          "9": [
            "#003C30", 
            "#0A6C64", 
            "#4AA49B", 
            "#9CD8CE", 
            "#E0E9D4", 
            "#E8D097", 
            "#C89142", 
            "#92570F", 
            "#543005"
          ], 
          "10": [
            "#003C30", 
            "#01665E", 
            "#35978F", 
            "#80CDC1", 
            "#C7EAE5", 
            "#F6E8C3", 
            "#DFC27D", 
            "#BF812D", 
            "#8C510A", 
            "#543005"
          ], 
          "11": [
            "#003C30", 
            "#016259", 
            "#2C8D85", 
            "#6BBDB2", 
            "#ABDED6", 
            "#E0E9D4", 
            "#EDD9A7", 
            "#D6AE65", 
            "#B57726", 
            "#864E0A", 
            "#543005"
          ]
        }, 
        "name_en": "Hypsometric Topographic Pressure", 
        "id": "SPres_Seq_Hypsometric"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "تدرج الضغط الطبوغرافي المعقد للمرتفعات والوديان", 
        "source": "USGS / NASA SRTM Digital Elevation", 
        "classes": {
          "3": [
            "#2D004B", 
            "#EDDDD1", 
            "#7F3B08"
          ], 
          "4": [
            "#2D004B", 
            "#B2ABD2", 
            "#FDB863", 
            "#7F3B08"
          ], 
          "5": [
            "#2D004B", 
            "#8C81B5", 
            "#EDDDD1", 
            "#E88F2C", 
            "#7F3B08"
          ], 
          "6": [
            "#2D004B", 
            "#7864A5", 
            "#C9C7E1", 
            "#FFD095", 
            "#D77911", 
            "#7F3B08"
          ], 
          "7": [
            "#2D004B", 
            "#6B4E9A", 
            "#B2ABD2", 
            "#EDDDD1", 
            "#FDB863", 
            "#C96D0D", 
            "#7F3B08"
          ], 
          "8": [
            "#2D004B", 
            "#613E92", 
            "#9C93C2", 
            "#D3D3E7", 
            "#FFDAAA", 
            "#F1A145", 
            "#C0640A", 
            "#7F3B08"
          ], 
          "9": [
            "#2D004B", 
            "#5A318D", 
            "#8C81B5", 
            "#C0BCDB", 
            "#EDDDD1", 
            "#FFC782", 
            "#E88F2C", 
            "#B95D07", 
            "#7F3B08"
          ], 
          "10": [
            "#2D004B", 
            "#542788", 
            "#8073AC", 
            "#B2ABD2", 
            "#D8DAEB", 
            "#FEE0B6", 
            "#FDB863", 
            "#E08214", 
            "#B35806", 
            "#7F3B08"
          ], 
          "11": [
            "#2D004B", 
            "#502382", 
            "#7864A5", 
            "#A39AC7", 
            "#C9C7E1", 
            "#EDDDD1", 
            "#FFD095", 
            "#F5A84E", 
            "#D77911", 
            "#AE5506", 
            "#7F3B08"
          ]
        }, 
        "name_en": "Orographic Relief Column", 
        "id": "SPres_Multi_Terrain"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ الضغط الجوي السطحي عن المعدل التضاريسي", 
        "source": "ECMWF Surface Pressure Diagnostics", 
        "classes": {
          "3": [
            "#67A9CF", 
            "#F7F7F7", 
            "#EF6548"
          ], 
          "4": [
            "#2166AC", 
            "#BDC9E1", 
            "#FDBB84", 
            "#B30000"
          ], 
          "5": [
            "#2166AC", 
            "#BDC9E1", 
            "#F7F7F7", 
            "#FDBB84", 
            "#B30000"
          ], 
          "6": [
            "#2166AC", 
            "#67A9CF", 
            "#BDC9E1", 
            "#FDBB84", 
            "#EF6548", 
            "#B30000"
          ], 
          "7": [
            "#2166AC", 
            "#67A9CF", 
            "#BDC9E1", 
            "#F7F7F7", 
            "#FDBB84", 
            "#EF6548", 
            "#B30000"
          ], 
          "8": [
            "#2166AC", 
            "#5392C3", 
            "#86B4D5", 
            "#BDC9E1", 
            "#FDBB84", 
            "#F5835B", 
            "#DB4C31", 
            "#B30000"
          ], 
          "9": [
            "#2166AC", 
            "#5392C3", 
            "#86B4D5", 
            "#BDC9E1", 
            "#F7F7F7", 
            "#FDBB84", 
            "#F5835B", 
            "#DB4C31", 
            "#B30000"
          ], 
          "10": [
            "#2166AC", 
            "#4987BE", 
            "#67A9CF", 
            "#95B9D8", 
            "#BDC9E1", 
            "#FDBB84", 
            "#F89265", 
            "#EF6548", 
            "#D13E25", 
            "#B30000"
          ], 
          "11": [
            "#2166AC", 
            "#4987BE", 
            "#67A9CF", 
            "#95B9D8", 
            "#BDC9E1", 
            "#F7F7F7", 
            "#FDBB84", 
            "#F89265", 
            "#EF6548", 
            "#D13E25", 
            "#B30000"
          ]
        }, 
        "name_en": "Surface Pressure Anomaly", 
        "id": "SPres_Div_Anomaly"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مقياس الارتفاع البارومتري للطيران والملاحة الجوية", 
        "source": "Federal Aviation Administration (FAA)", 
        "classes": {
          "3": [
            "#F7FCF5", 
            "#74C476", 
            "#00441B"
          ], 
          "4": [
            "#F7FCF5", 
            "#AEDEA7", 
            "#37A055", 
            "#00441B"
          ], 
          "5": [
            "#F7FCF5", 
            "#C7E9C0", 
            "#74C476", 
            "#238B45", 
            "#00441B"
          ], 
          "6": [
            "#F7FCF5", 
            "#D3EECD", 
            "#98D594", 
            "#4CB062", 
            "#177F3B", 
            "#00441B"
          ], 
          "7": [
            "#F7FCF5", 
            "#DBF1D5", 
            "#AEDEA7", 
            "#74C476", 
            "#37A055", 
            "#0E7734", 
            "#00441B"
          ], 
          "8": [
            "#F7FCF5", 
            "#E1F3DB", 
            "#BCE4B5", 
            "#8ED08B", 
            "#58B668", 
            "#2C944C", 
            "#067130", 
            "#00441B"
          ], 
          "9": [
            "#F7FCF5", 
            "#E5F5E0", 
            "#C7E9C0", 
            "#A1D99B", 
            "#74C476", 
            "#41AB5D", 
            "#238B45", 
            "#006D2C", 
            "#00441B"
          ], 
          "10": [
            "#F7FCF5", 
            "#E7F6E2", 
            "#CEECC7", 
            "#AEDEA7", 
            "#88CD86", 
            "#5FB96B", 
            "#37A055", 
            "#1D843F", 
            "#00682A", 
            "#00441B"
          ], 
          "11": [
            "#F7FCF5", 
            "#E9F6E4", 
            "#D3EECD", 
            "#B8E3B1", 
            "#98D594", 
            "#74C476", 
            "#4CB062", 
            "#30984E", 
            "#177F3B", 
            "#006529", 
            "#00441B"
          ]
        }, 
        "name_en": "Barometric Altimeter QNH", 
        "id": "SPres_Seq_Altimeter"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "الضغط السطحي للهضاب العالية (هضبة التبت وإثيوبيا)", 
        "source": "High-Altitude Meteorology Research", 
        "classes": {
          "3": [
            "#313695", 
            "#E0F3F8", 
            "#F46D43"
          ], 
          "4": [
            "#313695", 
            "#99CAE1", 
            "#FFF5AF", 
            "#F46D43"
          ], 
          "5": [
            "#313695", 
            "#74ADD1", 
            "#E0F3F8", 
            "#FEE090", 
            "#F46D43"
          ], 
          "6": [
            "#313695", 
            "#6296C5", 
            "#B6DEEC", 
            "#FAFDCB", 
            "#FFCC7D", 
            "#F46D43"
          ], 
          "7": [
            "#313695", 
            "#5687BE", 
            "#99CAE1", 
            "#E0F3F8", 
            "#FFF5AF", 
            "#FEBF70", 
            "#F46D43"
          ], 
          "8": [
            "#313695", 
            "#4C7DB8", 
            "#84B9D8", 
            "#C2E4EF", 
            "#F3FAD8", 
            "#FFE99D", 
            "#FEB568", 
            "#F46D43"
          ], 
          "9": [
            "#313695", 
            "#4575B4", 
            "#74ADD1", 
            "#ABD9E9", 
            "#E0F3F8", 
            "#FFFFBF", 
            "#FEE090", 
            "#FDAE61", 
            "#F46D43"
          ], 
          "10": [
            "#313695", 
            "#446EB1", 
            "#6AA0CB", 
            "#99CAE1", 
            "#C9E7F1", 
            "#EFF8DF", 
            "#FFF5AF", 
            "#FED585", 
            "#FCA75E", 
            "#F46D43"
          ], 
          "11": [
            "#313695", 
            "#4268AE", 
            "#6296C5", 
            "#8BBEDB", 
            "#B6DEEC", 
            "#E0F3F8", 
            "#FAFDCB", 
            "#FFECA3", 
            "#FFCC7D", 
            "#FCA25B", 
            "#F46D43"
          ]
        }, 
        "name_en": "Tibetan & Ethiopian Plateau", 
        "id": "SPres_Multi_PlateauHigh"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الضغط السطحي للمنخفضات العميقة (القطارة والبحر الميت)", 
        "source": "Dead Sea & Qattara Basin Barometric Studies", 
        "classes": {
          "3": [
            "#FFFFD4", 
            "#FE9929", 
            "#993404"
          ], 
          "4": [
            "#FFFFD4", 
            "#FFC46E", 
            "#E67317", 
            "#993404"
          ], 
          "5": [
            "#FFFFD4", 
            "#FED98E", 
            "#FE9929", 
            "#D95F0E", 
            "#993404"
          ], 
          "6": [
            "#FFFFD4", 
            "#FFE19C", 
            "#FFB354", 
            "#EF821E", 
            "#CC560C", 
            "#993404"
          ], 
          "7": [
            "#FFFFD4", 
            "#FFE6A5", 
            "#FFC46E", 
            "#FE9929", 
            "#E67317", 
            "#C3500A", 
            "#993404"
          ], 
          "8": [
            "#FFFFD4", 
            "#FFE9AC", 
            "#FFD080", 
            "#FFAC49", 
            "#F48921", 
            "#DE6812", 
            "#BD4C09", 
            "#993404"
          ], 
          "9": [
            "#FFFFD4", 
            "#FFECB1", 
            "#FED98E", 
            "#FFB95E", 
            "#FE9929", 
            "#EC7C1C", 
            "#D95F0E", 
            "#B94908", 
            "#993404"
          ], 
          "10": [
            "#FFFFD4", 
            "#FFEEB5", 
            "#FFDD96", 
            "#FFC46E", 
            "#FFA742", 
            "#F68C23", 
            "#E67317", 
            "#D25A0D", 
            "#B54708", 
            "#993404"
          ], 
          "11": [
            "#FFFFD4", 
            "#FFF0B8", 
            "#FFE19C", 
            "#FFCC7B", 
            "#FFB354", 
            "#FE9929", 
            "#EF821E", 
            "#E16B14", 
            "#CC560C", 
            "#B24507", 
            "#993404"
          ]
        }, 
        "name_en": "Deep Depression & Rift Valley", 
        "id": "SPres_Seq_ValleyBasin"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "انحراف تدرج الضغط الشاقولي عن الغلاف المعياري", 
        "source": "WMO Upper-Air Sounding Standards", 
        "classes": {
          "3": [
            "#2166AC", 
            "#F7F7F7", 
            "#D6604D"
          ], 
          "4": [
            "#053061", 
            "#4393C3", 
            "#F4A582", 
            "#67001F"
          ], 
          "5": [
            "#053061", 
            "#4393C3", 
            "#F7F7F7", 
            "#F4A582", 
            "#67001F"
          ], 
          "6": [
            "#053061", 
            "#2166AC", 
            "#4393C3", 
            "#F4A582", 
            "#D6604D", 
            "#67001F"
          ], 
          "7": [
            "#053061", 
            "#2166AC", 
            "#4393C3", 
            "#F7F7F7", 
            "#F4A582", 
            "#D6604D", 
            "#67001F"
          ], 
          "8": [
            "#053061", 
            "#185392", 
            "#2E75B4", 
            "#4393C3", 
            "#F4A582", 
            "#E1785E", 
            "#B0433D", 
            "#67001F"
          ], 
          "9": [
            "#053061", 
            "#185392", 
            "#2E75B4", 
            "#4393C3", 
            "#F7F7F7", 
            "#F4A582", 
            "#E1785E", 
            "#B0433D", 
            "#67001F"
          ], 
          "10": [
            "#053061", 
            "#134A86", 
            "#2166AC", 
            "#347CB8", 
            "#4393C3", 
            "#F4A582", 
            "#E68367", 
            "#D6604D", 
            "#9D3435", 
            "#67001F"
          ], 
          "11": [
            "#053061", 
            "#134A86", 
            "#2166AC", 
            "#347CB8", 
            "#4393C3", 
            "#F7F7F7", 
            "#F4A582", 
            "#E68367", 
            "#D6604D", 
            "#9D3435", 
            "#67001F"
          ]
        }, 
        "name_en": "Atmospheric Lapse Rate Departure", 
        "id": "SPres_Div_LapseRate"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "الضغط السطحي للتضاريس الدقيقة والمنحدرات", 
        "source": "Complex Terrain Mesoscale Meteorology", 
        "classes": {
          "3": [
            "#00441B", 
            "#FFFFCC", 
            "#800026"
          ], 
          "4": [
            "#00441B", 
            "#ACDDA7", 
            "#FFC062", 
            "#800026"
          ], 
          "5": [
            "#00441B", 
            "#74C476", 
            "#FFFFCC", 
            "#FD8D3C", 
            "#800026"
          ], 
          "6": [
            "#00441B", 
            "#56AD62", 
            "#D2EDC2", 
            "#FFE087", 
            "#F4692E", 
            "#800026"
          ], 
          "7": [
            "#00441B", 
            "#419E55", 
            "#ACDDA7", 
            "#FFFFCC", 
            "#FFC062", 
            "#ED4D26", 
            "#800026"
          ], 
          "8": [
            "#00441B", 
            "#31934C", 
            "#8DCF8B", 
            "#DFF2C5", 
            "#FFE99B", 
            "#FFA34C", 
            "#E73520", 
            "#800026"
          ], 
          "9": [
            "#00441B", 
            "#238B45", 
            "#74C476", 
            "#C7E9C0", 
            "#FFFFCC", 
            "#FED976", 
            "#FD8D3C", 
            "#E31A1C", 
            "#800026"
          ], 
          "10": [
            "#00441B", 
            "#1F8340", 
            "#64B76B", 
            "#ACDDA7", 
            "#E6F5C7", 
            "#FFEEA6", 
            "#FFC062", 
            "#F87934", 
            "#D8171E", 
            "#800026"
          ], 
          "11": [
            "#00441B", 
            "#1C7C3C", 
            "#56AD62", 
            "#96D393", 
            "#D2EDC2", 
            "#FFFFCC", 
            "#FFE087", 
            "#FFAC53", 
            "#F4692E", 
            "#CF141F", 
            "#800026"
          ]
        }, 
        "name_en": "Micro-relief Surface Pressure", 
        "id": "SPres_Multi_MicroRelief"
      }
    ], 
    "folder": "04_Surface_Pressure", 
    "name_en": "Surface Pressure"
  }, 
  {
    "name_ar": "سرعة واتجاه الرياح", 
    "styles": [
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس بوفورت الدولي لسرعة وطاقة الرياح", 
        "source": "WMO-No. 306 Beaufort Scale", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#FFD78F", 
            "#49006A"
          ], 
          "4": [
            "#FFFFFF", 
            "#1A9641", 
            "#F46D43", 
            "#49006A"
          ], 
          "5": [
            "#FFFFFF", 
            "#88C85F", 
            "#FFD78F", 
            "#DF3625", 
            "#49006A"
          ], 
          "6": [
            "#FFFFFF", 
            "#B4DE87", 
            "#ADD58B", 
            "#FA9555", 
            "#C71132", 
            "#49006A"
          ], 
          "7": [
            "#FFFFFF", 
            "#C6E6B2", 
            "#1A9641", 
            "#FFD78F", 
            "#F46D43", 
            "#AD054D", 
            "#49006A"
          ], 
          "8": [
            "#FFFFFF", 
            "#D2ECD0", 
            "#61B352", 
            "#E2F0AC", 
            "#FCA55D", 
            "#E85032", 
            "#99005F", 
            "#49006A"
          ], 
          "9": [
            "#FFFFFF", 
            "#DAF0E6", 
            "#88C85F", 
            "#7EBE6E", 
            "#FFD78F", 
            "#F8874E", 
            "#DF3625", 
            "#89006D", 
            "#49006A"
          ], 
          "10": [
            "#FFFFFF", 
            "#E0F3F8", 
            "#A6D96A", 
            "#1A9641", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F46D43", 
            "#D7191C", 
            "#7A0177", 
            "#49006A"
          ], 
          "11": [
            "#FFFFFF", 
            "#E3F4F9", 
            "#B4DE87", 
            "#50AA4D", 
            "#ADD58B", 
            "#FFD78F", 
            "#FA9555", 
            "#EC5937", 
            "#C71132", 
            "#750176", 
            "#49006A"
          ]
        }, 
        "name_en": "WMO Beaufort Wind Scale", 
        "id": "Wind_Seq_Beaufort"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "سرعة الرياح القطرية لرادار الدوبلر (اقتراب/ابتعاد)", 
        "source": "NOAA ROC Doppler Radial Velocity", 
        "classes": {
          "3": [
            "#008000", 
            "#FFFFFF", 
            "#CC0000"
          ], 
          "4": [
            "#00FF00", 
            "#004000", 
            "#660000", 
            "#FF0000"
          ], 
          "5": [
            "#00FF00", 
            "#004000", 
            "#FFFFFF", 
            "#660000", 
            "#FF0000"
          ], 
          "6": [
            "#00FF00", 
            "#009F00", 
            "#004000", 
            "#660000", 
            "#B20001", 
            "#FF0000"
          ], 
          "7": [
            "#00FF00", 
            "#009F00", 
            "#004000", 
            "#FFFFFF", 
            "#660000", 
            "#B20001", 
            "#FF0000"
          ], 
          "8": [
            "#00FF00", 
            "#00BF00", 
            "#008000", 
            "#004000", 
            "#660000", 
            "#990000", 
            "#CC0000", 
            "#FF0000"
          ], 
          "9": [
            "#00FF00", 
            "#00BF00", 
            "#008000", 
            "#004000", 
            "#FFFFFF", 
            "#660000", 
            "#990000", 
            "#CC0000", 
            "#FF0000"
          ], 
          "10": [
            "#00FF00", 
            "#00CF00", 
            "#009F00", 
            "#006F01", 
            "#004000", 
            "#660000", 
            "#8C0001", 
            "#B20001", 
            "#D90000", 
            "#FF0000"
          ], 
          "11": [
            "#00FF00", 
            "#00CF00", 
            "#009F00", 
            "#006F01", 
            "#004000", 
            "#FFFFFF", 
            "#660000", 
            "#8C0001", 
            "#B20001", 
            "#D90000", 
            "#FF0000"
          ]
        }, 
        "name_en": "Doppler Radial Velocity", 
        "id": "Wind_Multi_DopplerVelocity"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس سافير-سيمبسون لشدة الأعاصير المدارية", 
        "source": "NOAA National Hurricane Center (NHC)", 
        "classes": {
          "3": [
            "#41B6C4", 
            "#FD8D3C", 
            "#4D004B"
          ], 
          "4": [
            "#41B6C4", 
            "#FED976", 
            "#E31A1C", 
            "#4D004B"
          ], 
          "5": [
            "#41B6C4", 
            "#A3818B", 
            "#FD8D3C", 
            "#B00B23", 
            "#4D004B"
          ], 
          "6": [
            "#41B6C4", 
            "#655192", 
            "#FFBB5F", 
            "#EE5528", 
            "#930325", 
            "#4D004B"
          ], 
          "7": [
            "#41B6C4", 
            "#253494", 
            "#FED976", 
            "#FD8D3C", 
            "#E31A1C", 
            "#800026", 
            "#4D004B"
          ], 
          "8": [
            "#41B6C4", 
            "#2F469B", 
            "#CBA584", 
            "#FFAE55", 
            "#F3662D", 
            "#C61221", 
            "#7A002C", 
            "#4D004B"
          ], 
          "9": [
            "#41B6C4", 
            "#3554A0", 
            "#A3818B", 
            "#FFC767", 
            "#FD8D3C", 
            "#EA4323", 
            "#B00B23", 
            "#750030", 
            "#4D004B"
          ], 
          "10": [
            "#41B6C4", 
            "#395EA4", 
            "#82658F", 
            "#FED976", 
            "#FFA74F", 
            "#F56F31", 
            "#E31A1C", 
            "#A00624", 
            "#710033", 
            "#4D004B"
          ], 
          "11": [
            "#41B6C4", 
            "#3B67A8", 
            "#655192", 
            "#DAB581", 
            "#FFBB5F", 
            "#FD8D3C", 
            "#EE5528", 
            "#CF141F", 
            "#930325", 
            "#6D0035", 
            "#4D004B"
          ]
        }, 
        "name_en": "Saffir-Simpson Hurricane Scale", 
        "id": "Wind_Multi_Hurricanes"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مخاطر الاضطرابات الجوية لطيران الخطوط الجوية", 
        "source": "ICAO / FAA Aviation Turbulence Scale", 
        "classes": {
          "3": [
            "#2B83BA", 
            "#FDAE61", 
            "#4A0000"
          ], 
          "4": [
            "#2B83BA", 
            "#FFFFBF", 
            "#D7191C", 
            "#4A0000"
          ], 
          "5": [
            "#2B83BA", 
            "#D5EEB1", 
            "#FDAE61", 
            "#B80C14", 
            "#4A0000"
          ], 
          "6": [
            "#2B83BA", 
            "#BCE4A9", 
            "#FFDF99", 
            "#E96336", 
            "#A50410", 
            "#4A0000"
          ], 
          "7": [
            "#2B83BA", 
            "#ABDDA4", 
            "#FFFFBF", 
            "#FDAE61", 
            "#D7191C", 
            "#99000D", 
            "#4A0000"
          ], 
          "8": [
            "#2B83BA", 
            "#9ECFA8", 
            "#E7F5B7", 
            "#FFD189", 
            "#EF7A42", 
            "#C51218", 
            "#8D000C", 
            "#4A0000"
          ], 
          "9": [
            "#2B83BA", 
            "#93C5AB", 
            "#D5EEB1", 
            "#FFEBA7", 
            "#FDAE61", 
            "#E24D2C", 
            "#B80C14", 
            "#84000B", 
            "#4A0000"
          ], 
          "10": [
            "#2B83BA", 
            "#8BBEAD", 
            "#C7E8AD", 
            "#FFFFBF", 
            "#FFC980", 
            "#F38649", 
            "#D7191C", 
            "#AD0812", 
            "#7D000B", 
            "#4A0000"
          ], 
          "11": [
            "#2B83BA", 
            "#84B8AE", 
            "#BCE4A9", 
            "#EEF8BA", 
            "#FFDF99", 
            "#FDAE61", 
            "#E96336", 
            "#CA1419", 
            "#A50410", 
            "#78000A", 
            "#4A0000"
          ]
        }, 
        "name_en": "Clear Air Turbulence Risk", 
        "id": "Wind_Multi_AviationTurbulence"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مقياس الأنواء البحرية والرياح العاتية في عرض البحر", 
        "source": "National Data Buoy Center (NDBC)", 
        "classes": {
          "3": [
            "#EDF8FB", 
            "#66C2A4", 
            "#006D2C"
          ], 
          "4": [
            "#EDF8FB", 
            "#9AD7CD", 
            "#43AD76", 
            "#006D2C"
          ], 
          "5": [
            "#EDF8FB", 
            "#B2E2E2", 
            "#66C2A4", 
            "#2CA25F", 
            "#006D2C"
          ], 
          "6": [
            "#EDF8FB", 
            "#BEE6E7", 
            "#86CFBC", 
            "#52B588", 
            "#259755", 
            "#006D2C"
          ], 
          "7": [
            "#EDF8FB", 
            "#C6E9EA", 
            "#9AD7CD", 
            "#66C2A4", 
            "#43AD76", 
            "#20904E", 
            "#006D2C"
          ], 
          "8": [
            "#EDF8FB", 
            "#CCEBED", 
            "#A8DDD9", 
            "#7DCBB5", 
            "#58B990", 
            "#36A769", 
            "#1C8B49", 
            "#006D2C"
          ], 
          "9": [
            "#EDF8FB", 
            "#D0EDEE", 
            "#B2E2E2", 
            "#8DD2C3", 
            "#66C2A4", 
            "#4CB281", 
            "#2CA25F", 
            "#198745", 
            "#006D2C"
          ], 
          "10": [
            "#EDF8FB", 
            "#D3EEF0", 
            "#B9E4E5", 
            "#9AD7CD", 
            "#78C9B2", 
            "#5BBB94", 
            "#43AD76", 
            "#289C59", 
            "#178442", 
            "#006D2C"
          ], 
          "11": [
            "#EDF8FB", 
            "#D6EFF1", 
            "#BEE6E7", 
            "#A3DCD5", 
            "#86CFBC", 
            "#66C2A4", 
            "#52B588", 
            "#3AA86D", 
            "#259755", 
            "#158240", 
            "#006D2C"
          ]
        }, 
        "name_en": "Marine Offshore Gale Scale", 
        "id": "Wind_Seq_MarineGale"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس فوجيتا المطور للأعاصير القمعية التدميرية", 
        "source": "NOAA Storm Prediction Center (EF-Scale)", 
        "classes": {
          "3": [
            "#C7E9C0", 
            "#FD8D3C", 
            "#490000"
          ], 
          "4": [
            "#C7E9C0", 
            "#FEB24C", 
            "#FC4E2A", 
            "#490000"
          ], 
          "5": [
            "#C7E9C0", 
            "#C2BD62", 
            "#FD8D3C", 
            "#D62F29", 
            "#490000"
          ], 
          "6": [
            "#C7E9C0", 
            "#97C26E", 
            "#FEA445", 
            "#FD6A31", 
            "#C01827", 
            "#490000"
          ], 
          "7": [
            "#C7E9C0", 
            "#74C476", 
            "#FEB24C", 
            "#FD8D3C", 
            "#FC4E2A", 
            "#B10026", 
            "#490000"
          ], 
          "8": [
            "#C7E9C0", 
            "#81C980", 
            "#DDB959", 
            "#FE9D43", 
            "#FD7534", 
            "#E63D29", 
            "#A10021", 
            "#490000"
          ], 
          "9": [
            "#C7E9C0", 
            "#8ACD88", 
            "#C2BD62", 
            "#FEA948", 
            "#FD8D3C", 
            "#FD602E", 
            "#D62F29", 
            "#95001E", 
            "#490000"
          ], 
          "10": [
            "#C7E9C0", 
            "#91D08E", 
            "#ABC069", 
            "#FEB24C", 
            "#FE9A41", 
            "#FD7A36", 
            "#FC4E2A", 
            "#CA2328", 
            "#8C001B", 
            "#490000"
          ], 
          "11": [
            "#C7E9C0", 
            "#96D393", 
            "#97C26E", 
            "#E7B755", 
            "#FEA445", 
            "#FD8D3C", 
            "#FD6A31", 
            "#ED422A", 
            "#C01827", 
            "#850019", 
            "#490000"
          ]
        }, 
        "name_en": "Enhanced Fujita Tornado Scale", 
        "id": "Wind_Multi_EF_Tornado"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مؤشر التبريد بالرياح ومخاطر التجمد البشري", 
        "source": "NOAA National Weather Service (Wind Chill)", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#4292C6", 
            "#67001F"
          ], 
          "4": [
            "#FFFFFF", 
            "#9ECAE1", 
            "#08519C", 
            "#67001F"
          ], 
          "5": [
            "#FFFFFF", 
            "#BEDAEC", 
            "#4292C6", 
            "#33328C", 
            "#67001F"
          ], 
          "6": [
            "#FFFFFF", 
            "#D1E4F3", 
            "#7DB3D6", 
            "#276AAD", 
            "#3C1A83", 
            "#67001F"
          ], 
          "7": [
            "#FFFFFF", 
            "#DEEBF7", 
            "#9ECAE1", 
            "#4292C6", 
            "#08519C", 
            "#3F007D", 
            "#67001F"
          ], 
          "8": [
            "#FFFFFF", 
            "#E3EEF8", 
            "#B1D3E7", 
            "#6EAAD2", 
            "#3075B4", 
            "#294093", 
            "#4B006F", 
            "#67001F"
          ], 
          "9": [
            "#FFFFFF", 
            "#E6F0F9", 
            "#BEDAEC", 
            "#8ABCDA", 
            "#4292C6", 
            "#1E61A6", 
            "#33328C", 
            "#520064", 
            "#67001F"
          ], 
          "10": [
            "#FFFFFF", 
            "#E9F2FA", 
            "#C9E0F0", 
            "#9ECAE1", 
            "#65A4CF", 
            "#347CB8", 
            "#08519C", 
            "#392687", 
            "#57005C", 
            "#67001F"
          ], 
          "11": [
            "#FFFFFF", 
            "#EBF3FA", 
            "#D1E4F3", 
            "#ABD1E5", 
            "#7DB3D6", 
            "#4292C6", 
            "#276AAD", 
            "#234596", 
            "#3C1A83", 
            "#590056", 
            "#67001F"
          ]
        }, 
        "name_en": "NOAA NWS Wind Chill Index", 
        "id": "Wind_Multi_WindChill"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "كثافة طاقة الرياح لتوليد الكهرباء على ارتفاع 100م", 
        "source": "Global Wind Atlas / DTU Wind Energy", 
        "classes": {
          "3": [
            "#F7FCF0", 
            "#7BCCC4", 
            "#084081"
          ], 
          "4": [
            "#F7FCF0", 
            "#B4E2BA", 
            "#44A6CC", 
            "#084081"
          ], 
          "5": [
            "#F7FCF0", 
            "#CCEBC5", 
            "#7BCCC4", 
            "#2B8CBE", 
            "#084081"
          ], 
          "6": [
            "#F7FCF0", 
            "#D4EECE", 
            "#A0DAB8", 
            "#59B8D0", 
            "#217DB7", 
            "#084081"
          ], 
          "7": [
            "#F7FCF0", 
            "#D9F0D4", 
            "#B4E2BA", 
            "#7BCCC4", 
            "#44A6CC", 
            "#1974B2", 
            "#084081"
          ], 
          "8": [
            "#F7FCF0", 
            "#DDF2D8", 
            "#C2E7C0", 
            "#96D6BC", 
            "#64BECD", 
            "#3697C4", 
            "#116DAF", 
            "#084081"
          ], 
          "9": [
            "#F7FCF0", 
            "#E0F3DB", 
            "#CCEBC5", 
            "#A8DDB5", 
            "#7BCCC4", 
            "#4EB3D3", 
            "#2B8CBE", 
            "#0868AC", 
            "#084081"
          ], 
          "10": [
            "#F7FCF0", 
            "#E3F4DD", 
            "#D0EDCA", 
            "#B4E2BA", 
            "#90D4BD", 
            "#6AC1CB", 
            "#44A6CC", 
            "#2684BA", 
            "#0963A7", 
            "#084081"
          ], 
          "11": [
            "#F7FCF0", 
            "#E5F5DF", 
            "#D4EECE", 
            "#BEE5BF", 
            "#A0DAB8", 
            "#7BCCC4", 
            "#59B8D0", 
            "#3B9BC6", 
            "#217DB7", 
            "#0960A3", 
            "#084081"
          ]
        }, 
        "name_en": "Wind Power Density at 100m", 
        "id": "Wind_Seq_PowerDensity"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "سرعات التيار النفاث في طبقات الجو العليا (250 hPa)", 
        "source": "Aviation High-Altitude Jet Stream Climatology", 
        "classes": {
          "3": [
            "#313695", 
            "#FFD78F", 
            "#4A0000"
          ], 
          "4": [
            "#313695", 
            "#ABD9E9", 
            "#F46D43", 
            "#4A0000"
          ], 
          "5": [
            "#313695", 
            "#82B8D7", 
            "#FFD78F", 
            "#DE422E", 
            "#4A0000"
          ], 
          "6": [
            "#313695", 
            "#6BA1CB", 
            "#E0F0D0", 
            "#FA9555", 
            "#CD2927", 
            "#4A0000"
          ], 
          "7": [
            "#313695", 
            "#5E91C3", 
            "#ABD9E9", 
            "#FFD78F", 
            "#F46D43", 
            "#BE1D27", 
            "#4A0000"
          ], 
          "8": [
            "#313695", 
            "#5385BC", 
            "#94C6DF", 
            "#F4F9C5", 
            "#FCA55D", 
            "#E85537", 
            "#B31227", 
            "#4A0000"
          ], 
          "9": [
            "#313695", 
            "#4B7CB8", 
            "#82B8D7", 
            "#CEE7DA", 
            "#FFD78F", 
            "#F8874E", 
            "#DE422E", 
            "#AB0826", 
            "#4A0000"
          ], 
          "10": [
            "#313695", 
            "#4575B4", 
            "#74ADD1", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027", 
            "#A50026", 
            "#4A0000"
          ], 
          "11": [
            "#313695", 
            "#446FB1", 
            "#6BA1CB", 
            "#9BCCE2", 
            "#E0F0D0", 
            "#FFD78F", 
            "#FA9555", 
            "#EC5D3A", 
            "#CD2927", 
            "#9B0023", 
            "#4A0000"
          ]
        }, 
        "name_en": "Jet Stream Core Isotachs", 
        "id": "Wind_Multi_JetStream"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس دوغلاس لحالة البحر وارتفاع الأمواج", 
        "source": "WMO Marine Meteorology Guide (Douglas Scale)", 
        "classes": {
          "3": [
            "#E0F3F8", 
            "#2166AC", 
            "#67001F"
          ], 
          "4": [
            "#E0F3F8", 
            "#4393C3", 
            "#053061", 
            "#67001F"
          ], 
          "5": [
            "#E0F3F8", 
            "#6EACD1", 
            "#2166AC", 
            "#231C56", 
            "#67001F"
          ], 
          "6": [
            "#E0F3F8", 
            "#84BBD9", 
            "#3781BA", 
            "#10457E", 
            "#2A0D4F", 
            "#67001F"
          ], 
          "7": [
            "#E0F3F8", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061", 
            "#2D004B", 
            "#67001F"
          ], 
          "8": [
            "#E0F3F8", 
            "#9ECBE2", 
            "#5DA1CB", 
            "#3279B6", 
            "#154E8B", 
            "#1B255B", 
            "#390045", 
            "#67001F"
          ], 
          "9": [
            "#E0F3F8", 
            "#A6D0E4", 
            "#6EACD1", 
            "#3C88BD", 
            "#2166AC", 
            "#0C3D73", 
            "#231C56", 
            "#400040", 
            "#67001F"
          ], 
          "10": [
            "#E0F3F8", 
            "#ADD4E7", 
            "#7AB4D5", 
            "#4393C3", 
            "#2E75B4", 
            "#185392", 
            "#053061", 
            "#271552", 
            "#45003C", 
            "#67001F"
          ], 
          "11": [
            "#E0F3F8", 
            "#B2D7E8", 
            "#84BBD9", 
            "#569DC8", 
            "#3781BA", 
            "#2166AC", 
            "#10457E", 
            "#17295D", 
            "#2A0D4F", 
            "#49003A", 
            "#67001F"
          ]
        }, 
        "name_en": "Douglas Sea State & Waves", 
        "id": "Wind_Multi_SeaState"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "نسيم البر والبحر ودورة الرياح اليومية الساحلية", 
        "source": "Coastal Boundary Layer Meteorology", 
        "classes": {
          "3": [
            "#EFF3FF", 
            "#6BAED6", 
            "#08519C"
          ], 
          "4": [
            "#EFF3FF", 
            "#A4C9E1", 
            "#4790C5", 
            "#08519C"
          ], 
          "5": [
            "#EFF3FF", 
            "#BDD7E7", 
            "#6BAED6", 
            "#3182BD", 
            "#08519C"
          ], 
          "6": [
            "#EFF3FF", 
            "#C7DDEC", 
            "#8EBEDD", 
            "#569CCC", 
            "#2B78B6", 
            "#08519C"
          ], 
          "7": [
            "#EFF3FF", 
            "#CEE0EF", 
            "#A4C9E1", 
            "#6BAED6", 
            "#4790C5", 
            "#2771B2", 
            "#08519C"
          ], 
          "8": [
            "#EFF3FF", 
            "#D2E3F1", 
            "#B2D1E5", 
            "#85BADB", 
            "#5CA1CF", 
            "#3B88C1", 
            "#246DAF", 
            "#08519C"
          ], 
          "9": [
            "#EFF3FF", 
            "#D6E5F3", 
            "#BDD7E7", 
            "#96C2DF", 
            "#6BAED6", 
            "#5198C9", 
            "#3182BD", 
            "#2169AC", 
            "#08519C"
          ], 
          "10": [
            "#EFF3FF", 
            "#D9E7F4", 
            "#C3DAEA", 
            "#A4C9E1", 
            "#7FB7DA", 
            "#60A4D0", 
            "#4790C5", 
            "#2E7CB9", 
            "#1F66AB", 
            "#08519C"
          ], 
          "11": [
            "#EFF3FF", 
            "#DBE8F5", 
            "#C7DDEC", 
            "#AECFE4", 
            "#8EBEDD", 
            "#6BAED6", 
            "#569CCC", 
            "#3F8BC2", 
            "#2B78B6", 
            "#1E64A9", 
            "#08519C"
          ]
        }, 
        "name_en": "Diurnal Coastal Breeze", 
        "id": "Wind_Seq_ThermalBreeze"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "رياح الخماسين والعواصف الغبارية الصحراوية", 
        "source": "Middle East & North Africa Dust Climatology", 
        "classes": {
          "3": [
            "#FFF7BC", 
            "#EC7C1C", 
            "#3D1703"
          ], 
          "4": [
            "#FFF7BC", 
            "#FFB643", 
            "#AE4207", 
            "#3D1703"
          ], 
          "5": [
            "#FFF7BC", 
            "#FFCC60", 
            "#EC7C1C", 
            "#8C3005", 
            "#3D1703"
          ], 
          "6": [
            "#FFF7BC", 
            "#FFD777", 
            "#FEA231", 
            "#CC560C", 
            "#7A2B06", 
            "#3D1703"
          ], 
          "7": [
            "#FFF7BC", 
            "#FFDE86", 
            "#FFB643", 
            "#EC7C1C", 
            "#AE4207", 
            "#6E2706", 
            "#3D1703"
          ], 
          "8": [
            "#FFF7BC", 
            "#FEE391", 
            "#FEC44F", 
            "#FE9929", 
            "#D95F0E", 
            "#993404", 
            "#662506", 
            "#3D1703"
          ], 
          "9": [
            "#FFF7BC", 
            "#FEE596", 
            "#FFCC60", 
            "#FFA938", 
            "#EC7C1C", 
            "#C14F0A", 
            "#8C3005", 
            "#612306", 
            "#3D1703"
          ], 
          "10": [
            "#FFF7BC", 
            "#FEE79B", 
            "#FFD26D", 
            "#FFB643", 
            "#FA9326", 
            "#DD6611", 
            "#AE4207", 
            "#822D06", 
            "#5D2206", 
            "#3D1703"
          ], 
          "11": [
            "#FFF7BC", 
            "#FFE99E", 
            "#FFD777", 
            "#FEC04B", 
            "#FEA231", 
            "#EC7C1C", 
            "#CC560C", 
            "#9F3805", 
            "#7A2B06", 
            "#592106", 
            "#3D1703"
          ]
        }, 
        "name_en": "Khamsin Sandstorm Gales", 
        "id": "Wind_Multi_KhamsinDust"
      }
    ], 
    "folder": "05_Wind", 
    "name_en": "Wind"
  }, 
  {
    "name_ar": "الرطوبة النسبية وبخار الماء", 
    "styles": [
      {
        "category": "Sequential", 
        "name_ar": "تدرج الرطوبة النسبية السطحية من الجفاف للتشبع", 
        "source": "ColorBrewer YlGnBu Climatology", 
        "classes": {
          "3": [
            "#FFFFD9", 
            "#41B6C4", 
            "#081D58"
          ], 
          "4": [
            "#FFFFD9", 
            "#99D6B9", 
            "#2280B8", 
            "#081D58"
          ], 
          "5": [
            "#FFFFD9", 
            "#C7E9B4", 
            "#41B6C4", 
            "#225EA8", 
            "#081D58"
          ], 
          "6": [
            "#FFFFD9", 
            "#D6EFB3", 
            "#75C8BD", 
            "#2798C1", 
            "#264DA0", 
            "#081D58"
          ], 
          "7": [
            "#FFFFD9", 
            "#E1F3B2", 
            "#99D6B9", 
            "#41B6C4", 
            "#2280B8", 
            "#26429B", 
            "#081D58"
          ], 
          "8": [
            "#FFFFD9", 
            "#E8F6B1", 
            "#B4E1B6", 
            "#69C3BF", 
            "#30A1C2", 
            "#236CAF", 
            "#263A97", 
            "#081D58"
          ], 
          "9": [
            "#FFFFD9", 
            "#EDF8B1", 
            "#C7E9B4", 
            "#7FCDBB", 
            "#41B6C4", 
            "#1D91C0", 
            "#225EA8", 
            "#253494", 
            "#081D58"
          ], 
          "10": [
            "#FFFFD9", 
            "#EFF9B5", 
            "#D0ECB3", 
            "#99D6B9", 
            "#61C0C0", 
            "#34A5C2", 
            "#2280B8", 
            "#2455A4", 
            "#22318D", 
            "#081D58"
          ], 
          "11": [
            "#FFFFD9", 
            "#F1F9B9", 
            "#D6EFB3", 
            "#ACDEB7", 
            "#75C8BD", 
            "#41B6C4", 
            "#2798C1", 
            "#2372B2", 
            "#264DA0", 
            "#1F2F88", 
            "#081D58"
          ]
        }, 
        "name_en": "Surface Relative Humidity", 
        "id": "RH_Seq_YlGnBu"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "قناة بخار الماء بالأشعة تحت الحمراء للأقمار الاصطناعية", 
        "source": "EUMETSAT / GOES Water Vapor Channel", 
        "classes": {
          "3": [
            "#000000", 
            "#7E7E7E", 
            "#FFFFFF"
          ], 
          "4": [
            "#000000", 
            "#545454", 
            "#A8A8A8", 
            "#FFFFFF"
          ], 
          "5": [
            "#000000", 
            "#3F3F3F", 
            "#7E7E7E", 
            "#BDBDBD", 
            "#FFFFFF"
          ], 
          "6": [
            "#000000", 
            "#323232", 
            "#656565", 
            "#979797", 
            "#CACACA", 
            "#FFFFFF"
          ], 
          "7": [
            "#000000", 
            "#2A2A2A", 
            "#545454", 
            "#7E7E7E", 
            "#A8A8A8", 
            "#D2D2D2", 
            "#FFFFFF"
          ], 
          "8": [
            "#000000", 
            "#242424", 
            "#484848", 
            "#6C6C6C", 
            "#909090", 
            "#B4B4B4", 
            "#D8D8D8", 
            "#FFFFFF"
          ], 
          "9": [
            "#000000", 
            "#1F1F1F", 
            "#3F3F3F", 
            "#5E5E5E", 
            "#7E7E7E", 
            "#9D9D9D", 
            "#BDBDBD", 
            "#DCDCDC", 
            "#FFFFFF"
          ], 
          "10": [
            "#000000", 
            "#1C1C1C", 
            "#383838", 
            "#545454", 
            "#707070", 
            "#8C8C8C", 
            "#A8A8A8", 
            "#C4C4C4", 
            "#E0E0E0", 
            "#FFFFFF"
          ], 
          "11": [
            "#000000", 
            "#1A1A1A", 
            "#323232", 
            "#4B4B4B", 
            "#656565", 
            "#7E7E7E", 
            "#979797", 
            "#B0B0B0", 
            "#CACACA", 
            "#E3E3E3", 
            "#FFFFFF"
          ]
        }, 
        "name_en": "Satellite Water Vapor IR", 
        "id": "RH_Multi_SatWaterVapor"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "فرق درجة الحرارة ونقطة الندى (تحديد تشبع الهواء)", 
        "source": "WMO Radiosonde & Synoptic Observations", 
        "classes": {
          "3": [
            "#5AAE61", 
            "#F7F7F7", 
            "#B35806"
          ], 
          "4": [
            "#00441B", 
            "#A6DBA0", 
            "#FDB863", 
            "#7F3B08"
          ], 
          "5": [
            "#00441B", 
            "#A6DBA0", 
            "#F7F7F7", 
            "#FDB863", 
            "#7F3B08"
          ], 
          "6": [
            "#00441B", 
            "#3D934C", 
            "#A6DBA0", 
            "#FDB863", 
            "#C96D0D", 
            "#7F3B08"
          ], 
          "7": [
            "#00441B", 
            "#3D934C", 
            "#A6DBA0", 
            "#F7F7F7", 
            "#FDB863", 
            "#C96D0D", 
            "#7F3B08"
          ], 
          "8": [
            "#00441B", 
            "#1B7837", 
            "#5AAE61", 
            "#A6DBA0", 
            "#FDB863", 
            "#E08214", 
            "#B35806", 
            "#7F3B08"
          ], 
          "9": [
            "#00441B", 
            "#1B7837", 
            "#5AAE61", 
            "#A6DBA0", 
            "#F7F7F7", 
            "#FDB863", 
            "#E08214", 
            "#B35806", 
            "#7F3B08"
          ], 
          "10": [
            "#00441B", 
            "#146B30", 
            "#3D934C", 
            "#6EB970", 
            "#A6DBA0", 
            "#FDB863", 
            "#E88F2C", 
            "#C96D0D", 
            "#A65107", 
            "#7F3B08"
          ], 
          "11": [
            "#00441B", 
            "#146B30", 
            "#3D934C", 
            "#6EB970", 
            "#A6DBA0", 
            "#F7F7F7", 
            "#FDB863", 
            "#E88F2C", 
            "#C96D0D", 
            "#A65107", 
            "#7F3B08"
          ]
        }, 
        "name_en": "Dew Point Depression", 
        "id": "RH_Div_DewPointDepression"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تدرج تشبع الضباب والندى الكثيف الساحلي", 
        "source": "Aviation Surface Weather Observation (Fog/Mist)", 
        "classes": {
          "3": [
            "#F7FBFF", 
            "#6BAED6", 
            "#08306B"
          ], 
          "4": [
            "#F7FBFF", 
            "#ACD0E6", 
            "#3987C0", 
            "#08306B"
          ], 
          "5": [
            "#F7FBFF", 
            "#C6DBEF", 
            "#6BAED6", 
            "#2171B5", 
            "#08306B"
          ], 
          "6": [
            "#F7FBFF", 
            "#D0E1F2", 
            "#94C4DF", 
            "#4B98C9", 
            "#1964AB", 
            "#08306B"
          ], 
          "7": [
            "#F7FBFF", 
            "#D6E6F4", 
            "#ACD0E6", 
            "#6BAED6", 
            "#3987C0", 
            "#135BA4", 
            "#08306B"
          ], 
          "8": [
            "#F7FBFF", 
            "#DBE9F6", 
            "#BBD6EB", 
            "#89BEDC", 
            "#559ECD", 
            "#2C7ABA", 
            "#0D55A0", 
            "#08306B"
          ], 
          "9": [
            "#F7FBFF", 
            "#DEEBF7", 
            "#C6DBEF", 
            "#9ECAE1", 
            "#6BAED6", 
            "#4292C6", 
            "#2171B5", 
            "#08519C", 
            "#08306B"
          ], 
          "10": [
            "#F7FBFF", 
            "#E1EDF8", 
            "#CBDFF1", 
            "#ACD0E6", 
            "#83BADB", 
            "#5AA1CF", 
            "#3987C0", 
            "#1D6AAF", 
            "#084D96", 
            "#08306B"
          ], 
          "11": [
            "#F7FBFF", 
            "#E3EEF9", 
            "#D0E1F2", 
            "#B6D4E9", 
            "#94C4DF", 
            "#6BAED6", 
            "#4B98C9", 
            "#307EBC", 
            "#1964AB", 
            "#084A92", 
            "#08306B"
          ]
        }, 
        "name_en": "Fog & Condensation Saturation", 
        "id": "RH_Seq_FogSaturation"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مؤشر عجز ضغط البخار لإجهاد المحاصيل الزراعية", 
        "source": "FAO-56 Irrigation / Agriculture & Forest Fire", 
        "classes": {
          "3": [
            "#F7FCF5", 
            "#74C476", 
            "#B10026"
          ], 
          "4": [
            "#F7FCF5", 
            "#AEDEA7", 
            "#FEA647", 
            "#B10026"
          ], 
          "5": [
            "#F7FCF5", 
            "#C7E9C0", 
            "#74C476", 
            "#FD8D3C", 
            "#B10026"
          ], 
          "6": [
            "#F7FCF5", 
            "#D3EECD", 
            "#98D594", 
            "#E7B755", 
            "#FD7634", 
            "#B10026"
          ], 
          "7": [
            "#F7FCF5", 
            "#DBF1D5", 
            "#AEDEA7", 
            "#74C476", 
            "#FEA647", 
            "#FD6630", 
            "#B10026"
          ], 
          "8": [
            "#F7FCF5", 
            "#E1F3DB", 
            "#BCE4B5", 
            "#8ED08B", 
            "#CBBC5F", 
            "#FE9840", 
            "#FC592C", 
            "#B10026"
          ], 
          "9": [
            "#F7FCF5", 
            "#E5F5E0", 
            "#C7E9C0", 
            "#A1D99B", 
            "#74C476", 
            "#FEB24C", 
            "#FD8D3C", 
            "#FC4E2A", 
            "#B10026"
          ], 
          "10": [
            "#F7FCF5", 
            "#E7F6E2", 
            "#CEECC7", 
            "#AEDEA7", 
            "#88CD86", 
            "#BABE64", 
            "#FEA647", 
            "#FD8138", 
            "#F3472A", 
            "#B10026"
          ], 
          "11": [
            "#F7FCF5", 
            "#E9F6E4", 
            "#D3EECD", 
            "#B8E3B1", 
            "#98D594", 
            "#74C476", 
            "#E7B755", 
            "#FE9C42", 
            "#FD7634", 
            "#ED422A", 
            "#B10026"
          ]
        }, 
        "name_en": "Vapor Pressure Deficit VPD", 
        "id": "RH_Seq_VPD_Agricultural"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس درجة حرارة نقطة الندى المطلقة (°C)", 
        "source": "NOAA National Weather Service (Dew Point)", 
        "classes": {
          "3": [
            "#800080", 
            "#3FDFC2", 
            "#FF0000"
          ], 
          "4": [
            "#800080", 
            "#3858FF", 
            "#CEFF45", 
            "#FF0000"
          ], 
          "5": [
            "#800080", 
            "#3300DE", 
            "#3FDFC2", 
            "#FFE000", 
            "#FF0000"
          ], 
          "6": [
            "#800080", 
            "#4600B2", 
            "#32A1FF", 
            "#71FF70", 
            "#FFB500", 
            "#FF0000"
          ], 
          "7": [
            "#800080", 
            "#4A0096", 
            "#3858FF", 
            "#3FDFC2", 
            "#CEFF45", 
            "#FF9600", 
            "#FF0000"
          ], 
          "8": [
            "#800080", 
            "#4B0082", 
            "#0000FF", 
            "#00BFFF", 
            "#00FF7F", 
            "#FFFF00", 
            "#FF7F00", 
            "#FF0000"
          ], 
          "9": [
            "#800080", 
            "#530082", 
            "#3300DE", 
            "#3C86FF", 
            "#3FDFC2", 
            "#9AFF61", 
            "#FFE000", 
            "#FF7600", 
            "#FF0000"
          ], 
          "10": [
            "#800080", 
            "#580082", 
            "#4000C6", 
            "#3858FF", 
            "#27C6F2", 
            "#26F88F", 
            "#CEFF45", 
            "#FFC800", 
            "#FF6E00", 
            "#FF0000"
          ], 
          "11": [
            "#800080", 
            "#5C0081", 
            "#4600B2", 
            "#2129FF", 
            "#32A1FF", 
            "#3FDFC2", 
            "#71FF70", 
            "#F1FF23", 
            "#FFB500", 
            "#FF6800", 
            "#FF0000"
          ]
        }, 
        "name_en": "Absolute Dew Point Scale", 
        "id": "RH_Multi_DewPointTemp"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الرطوبة النوعية ونسبة محتوى بخار الماء (جم/كجم)", 
        "source": "Atmospheric Boundary Layer Thermodynamics", 
        "classes": {
          "3": [
            "#FFF7FB", 
            "#74A9CF", 
            "#023858"
          ], 
          "4": [
            "#FFF7FB", 
            "#B4C4DF", 
            "#2B85BB", 
            "#023858"
          ], 
          "5": [
            "#FFF7FB", 
            "#D0D1E6", 
            "#74A9CF", 
            "#0570B0", 
            "#023858"
          ], 
          "6": [
            "#FFF7FB", 
            "#DBDAEB", 
            "#9DB9D9", 
            "#4595C3", 
            "#0567A2", 
            "#023858"
          ], 
          "7": [
            "#FFF7FB", 
            "#E3E0EE", 
            "#B4C4DF", 
            "#74A9CF", 
            "#2B85BB", 
            "#046199", 
            "#023858"
          ], 
          "8": [
            "#FFF7FB", 
            "#E8E4F0", 
            "#C4CBE3", 
            "#91B4D6", 
            "#549BC6", 
            "#1B79B5", 
            "#045D92", 
            "#023858"
          ], 
          "9": [
            "#FFF7FB", 
            "#ECE7F2", 
            "#D0D1E6", 
            "#A6BDDB", 
            "#74A9CF", 
            "#3690C0", 
            "#0570B0", 
            "#045A8D", 
            "#023858"
          ], 
          "10": [
            "#FFF7FB", 
            "#EEE9F3", 
            "#D6D6E9", 
            "#B4C4DF", 
            "#8BB2D4", 
            "#5C9EC8", 
            "#2B85BB", 
            "#056BA8", 
            "#045687", 
            "#023858"
          ], 
          "11": [
            "#FFF7FB", 
            "#F0EAF4", 
            "#DBDAEB", 
            "#BFC9E2", 
            "#9DB9D9", 
            "#74A9CF", 
            "#4595C3", 
            "#207DB6", 
            "#0567A2", 
            "#045382", 
            "#023858"
          ]
        }, 
        "name_en": "Specific Humidity g/kg", 
        "id": "RH_Seq_SpecificHumidity"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مؤشر البصيلة الرطبة المعياري للإجهاد الحراري", 
        "source": "ISO 7243 / OSHA Heat Stress Standards", 
        "classes": {
          "3": [
            "#006D2C", 
            "#FFD300", 
            "#7F0000"
          ], 
          "4": [
            "#006D2C", 
            "#C2E03D", 
            "#FF8200", 
            "#7F0000"
          ], 
          "5": [
            "#006D2C", 
            "#71B956", 
            "#FFD300", 
            "#FF4B00", 
            "#7F0000"
          ], 
          "6": [
            "#006D2C", 
            "#2CA25F", 
            "#FFFF00", 
            "#FFA500", 
            "#FF0000", 
            "#7F0000"
          ], 
          "7": [
            "#006D2C", 
            "#269956", 
            "#C2E03D", 
            "#FFD300", 
            "#FF8200", 
            "#E90001", 
            "#7F0000"
          ], 
          "8": [
            "#006D2C", 
            "#229250", 
            "#95CA4D", 
            "#FFF200", 
            "#FFB200", 
            "#FF6500", 
            "#D90002", 
            "#7F0000"
          ], 
          "9": [
            "#006D2C", 
            "#1E8E4B", 
            "#71B956", 
            "#E8F325", 
            "#FFD300", 
            "#FF9800", 
            "#FF4B00", 
            "#CD0002", 
            "#7F0000"
          ], 
          "10": [
            "#006D2C", 
            "#1B8A48", 
            "#50AC5B", 
            "#C2E03D", 
            "#FFEB00", 
            "#FFBA00", 
            "#FF8200", 
            "#FF3000", 
            "#C40003", 
            "#7F0000"
          ], 
          "11": [
            "#006D2C", 
            "#198745", 
            "#2CA25F", 
            "#A3D049", 
            "#FFFF00", 
            "#FFD300", 
            "#FFA500", 
            "#FF6E00", 
            "#FF0000", 
            "#BD0003", 
            "#7F0000"
          ]
        }, 
        "name_en": "Wet Bulb Globe Temp WBGT", 
        "id": "RH_Multi_WBGT_Stress"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "الماء القابل للتساقط وخرائط الأنهار الجوية", 
        "source": "NASA AIRS / NOAA Atmospheric Rivers", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#4393C3", 
            "#49006A"
          ], 
          "4": [
            "#FFFFFF", 
            "#92C5DE", 
            "#2166AC", 
            "#49006A"
          ], 
          "5": [
            "#FFFFFF", 
            "#BADCEB", 
            "#4393C3", 
            "#134A86", 
            "#49006A"
          ], 
          "6": [
            "#FFFFFF", 
            "#D1EAF3", 
            "#75B1D3", 
            "#3178B5", 
            "#0A3A6F", 
            "#49006A"
          ], 
          "7": [
            "#FFFFFF", 
            "#E0F3F8", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061", 
            "#49006A"
          ], 
          "8": [
            "#FFFFFF", 
            "#E4F5F9", 
            "#A9D2E5", 
            "#68A8CF", 
            "#367FB9", 
            "#195696", 
            "#192C62", 
            "#49006A"
          ], 
          "9": [
            "#FFFFFF", 
            "#E8F6FA", 
            "#BADCEB", 
            "#80B8D7", 
            "#4393C3", 
            "#2B71B2", 
            "#134A86", 
            "#222963", 
            "#49006A"
          ], 
          "10": [
            "#FFFFFF", 
            "#EAF7FA", 
            "#C7E3EF", 
            "#92C5DE", 
            "#61A3CC", 
            "#3984BB", 
            "#2166AC", 
            "#0E4179", 
            "#282764", 
            "#49006A"
          ], 
          "11": [
            "#FFFFFF", 
            "#ECF8FB", 
            "#D1EAF3", 
            "#A2CEE3", 
            "#75B1D3", 
            "#4393C3", 
            "#3178B5", 
            "#1B5B9C", 
            "#0A3A6F", 
            "#2C2565", 
            "#49006A"
          ]
        }, 
        "name_en": "Precipitable Water PWAT", 
        "id": "RH_Multi_PWAT_AtmRiver"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "تقارب وتباعد تدفق الرطوبة الجوية", 
        "source": "Dynamic Meteorology Moisture Convergence", 
        "classes": {
          "3": [
            "#DFC27D", 
            "#F5F5F5", 
            "#01665E"
          ], 
          "4": [
            "#8C510A", 
            "#DFC27D", 
            "#80CDC1", 
            "#01665E"
          ], 
          "5": [
            "#8C510A", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#01665E"
          ], 
          "6": [
            "#8C510A", 
            "#B78845", 
            "#DFC27D", 
            "#80CDC1", 
            "#49988E", 
            "#01665E"
          ], 
          "7": [
            "#8C510A", 
            "#B78845", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#49988E", 
            "#01665E"
          ], 
          "8": [
            "#8C510A", 
            "#A97532", 
            "#C49B57", 
            "#DFC27D", 
            "#80CDC1", 
            "#5BA99F", 
            "#36877E", 
            "#01665E"
          ], 
          "9": [
            "#8C510A", 
            "#A97532", 
            "#C49B57", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#5BA99F", 
            "#36877E", 
            "#01665E"
          ], 
          "10": [
            "#8C510A", 
            "#A26C29", 
            "#B78845", 
            "#CBA560", 
            "#DFC27D", 
            "#80CDC1", 
            "#65B2A7", 
            "#49988E", 
            "#2C7F76", 
            "#01665E"
          ], 
          "11": [
            "#8C510A", 
            "#A26C29", 
            "#B78845", 
            "#CBA560", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#65B2A7", 
            "#49988E", 
            "#2C7F76", 
            "#01665E"
          ]
        }, 
        "name_en": "Moisture Flux Convergence", 
        "id": "RH_Div_MoistureFlux"
      }
    ], 
    "folder": "06_Relative_Humidity", 
    "name_en": "Relative Humidity"
  }, 
  {
    "name_ar": "الإشعاع الشمسي والطاقة الكلية", 
    "styles": [
      {
        "category": "Sequential", 
        "name_ar": "تدرج الإشعاع الشمسي الكلي التراكمي", 
        "source": "ColorBrewer YlOrRd", 
        "classes": {
          "3": [
            "#FFFFCC", 
            "#FD8D3C", 
            "#800026"
          ], 
          "4": [
            "#FFFFCC", 
            "#FFBF5A", 
            "#F44025", 
            "#800026"
          ], 
          "5": [
            "#FFFFCC", 
            "#FED976", 
            "#FD8D3C", 
            "#E31A1C", 
            "#800026"
          ], 
          "6": [
            "#FFFFCC", 
            "#FFE187", 
            "#FEAB49", 
            "#FD5D2D", 
            "#D41121", 
            "#800026"
          ], 
          "7": [
            "#FFFFCC", 
            "#FFE692", 
            "#FFBF5A", 
            "#FD8D3C", 
            "#F44025", 
            "#CA0923", 
            "#800026"
          ], 
          "8": [
            "#FFFFCC", 
            "#FFEA9A", 
            "#FFCE6A", 
            "#FEA245", 
            "#FD6C31", 
            "#EA2D20", 
            "#C20425", 
            "#800026"
          ], 
          "9": [
            "#FFFFCC", 
            "#FFEDA0", 
            "#FED976", 
            "#FEB24C", 
            "#FD8D3C", 
            "#FC4E2A", 
            "#E31A1C", 
            "#BD0026", 
            "#800026"
          ], 
          "10": [
            "#FFFFCC", 
            "#FFEFA5", 
            "#FEDD7F", 
            "#FFBF5A", 
            "#FE9E43", 
            "#FD7434", 
            "#F44025", 
            "#DA151F", 
            "#B60026", 
            "#800026"
          ], 
          "11": [
            "#FFFFCC", 
            "#FFF1A9", 
            "#FFE187", 
            "#FFC965", 
            "#FEAB49", 
            "#FD8D3C", 
            "#FD5D2D", 
            "#ED3321", 
            "#D41121", 
            "#B10026", 
            "#800026"
          ]
        }, 
        "name_en": "Global Solar Radiation", 
        "id": "Solar_Seq_YlOrRd"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الإشعاع الشمسي الأفقي الكلي للبنك الدولي", 
        "source": "World Bank ESMAP / Solargis Global Solar Atlas", 
        "classes": {
          "3": [
            "#FFFFB2", 
            "#F7692D", 
            "#7A0000"
          ], 
          "4": [
            "#FFFFB2", 
            "#FEA346", 
            "#DF2C23", 
            "#7A0000"
          ], 
          "5": [
            "#FFFFB2", 
            "#FFBD54", 
            "#F7692D", 
            "#CA1625", 
            "#7A0000"
          ], 
          "6": [
            "#FFFFB2", 
            "#FECC5C", 
            "#FD8D3C", 
            "#F03B20", 
            "#BD0026", 
            "#7A0000"
          ], 
          "7": [
            "#FFFFB2", 
            "#FFD46B", 
            "#FEA346", 
            "#F7692D", 
            "#DF2C23", 
            "#B10020", 
            "#7A0000"
          ], 
          "8": [
            "#FFFFB2", 
            "#FFDA75", 
            "#FFB24E", 
            "#FC8338", 
            "#F24A24", 
            "#D32124", 
            "#A9001C", 
            "#7A0000"
          ], 
          "9": [
            "#FFFFB2", 
            "#FFDF7D", 
            "#FFBD54", 
            "#FE9540", 
            "#F7692D", 
            "#EA3621", 
            "#CA1625", 
            "#A30019", 
            "#7A0000"
          ], 
          "10": [
            "#FFFFB2", 
            "#FFE383", 
            "#FEC558", 
            "#FEA346", 
            "#FB7D35", 
            "#F35126", 
            "#DF2C23", 
            "#C30B26", 
            "#9F0017", 
            "#7A0000"
          ], 
          "11": [
            "#FFFFB2", 
            "#FFE587", 
            "#FECC5C", 
            "#FFAD4C", 
            "#FD8D3C", 
            "#F7692D", 
            "#F03B20", 
            "#D62424", 
            "#BD0026", 
            "#9B0015", 
            "#7A0000"
          ]
        }, 
        "name_en": "Global Horizontal Irradiance GHI", 
        "id": "Solar_Seq_ESMAP_GHI"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "القدرة الإنتاجية لتوليد الكهرباء الكهروضوئية", 
        "source": "Global Solar Atlas Photovoltaic Electricity", 
        "classes": {
          "3": [
            "#FFF7BC", 
            "#FE9929", 
            "#8C2D04"
          ], 
          "4": [
            "#FFF7BC", 
            "#FEC44F", 
            "#EC7014", 
            "#8C2D04"
          ], 
          "5": [
            "#FFF7BC", 
            "#FFD371", 
            "#FE9929", 
            "#DC5E0B", 
            "#8C2D04"
          ], 
          "6": [
            "#FFF7BC", 
            "#FFDD84", 
            "#FFB340", 
            "#F3811D", 
            "#D25305", 
            "#8C2D04"
          ], 
          "7": [
            "#FFF7BC", 
            "#FEE391", 
            "#FEC44F", 
            "#FE9929", 
            "#EC7014", 
            "#CC4C02", 
            "#8C2D04"
          ], 
          "8": [
            "#FFF7BC", 
            "#FEE697", 
            "#FFCD63", 
            "#FFAC3A", 
            "#F68820", 
            "#E3660F", 
            "#C34703", 
            "#8C2D04"
          ], 
          "9": [
            "#FFF7BC", 
            "#FFE89C", 
            "#FFD371", 
            "#FEB946", 
            "#FE9929", 
            "#F17A19", 
            "#DC5E0B", 
            "#BC4403", 
            "#8C2D04"
          ], 
          "10": [
            "#FFF7BC", 
            "#FFEA9F", 
            "#FFD97C", 
            "#FEC44F", 
            "#FFA836", 
            "#F88C22", 
            "#EC7014", 
            "#D75807", 
            "#B64103", 
            "#8C2D04"
          ], 
          "11": [
            "#FFF7BC", 
            "#FFEBA2", 
            "#FFDD84", 
            "#FFCA5D", 
            "#FFB340", 
            "#FE9929", 
            "#F3811D", 
            "#E66910", 
            "#D25305", 
            "#B23F03", 
            "#8C2D04"
          ]
        }, 
        "name_en": "Photovoltaic Potential PVOUT", 
        "id": "Solar_Seq_PVOUT"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الإشعاع المباشر لمحطات الطاقة الشمسية المركزة", 
        "source": "NREL National Solar Radiation Database (NSRDB)", 
        "classes": {
          "3": [
            "#FFFFE5", 
            "#FE9929", 
            "#662506"
          ], 
          "4": [
            "#FFFFE5", 
            "#FFCE66", 
            "#E1640E", 
            "#662506"
          ], 
          "5": [
            "#FFFFE5", 
            "#FEE391", 
            "#FE9929", 
            "#CC4C02", 
            "#662506"
          ], 
          "6": [
            "#FFFFE5", 
            "#FFEBA2", 
            "#FEBC48", 
            "#F07818", 
            "#B74203", 
            "#662506"
          ], 
          "7": [
            "#FFFFE5", 
            "#FFF0AE", 
            "#FFCE66", 
            "#FE9929", 
            "#E1640E", 
            "#AA3C04", 
            "#662506"
          ], 
          "8": [
            "#FFFFE5", 
            "#FFF4B6", 
            "#FFDA7F", 
            "#FFB23F", 
            "#F4821D", 
            "#D55606", 
            "#A03704", 
            "#662506"
          ], 
          "9": [
            "#FFFFE5", 
            "#FFF7BC", 
            "#FEE391", 
            "#FEC44F", 
            "#FE9929", 
            "#EC7014", 
            "#CC4C02", 
            "#993404", 
            "#662506"
          ], 
          "10": [
            "#FFFFE5", 
            "#FFF8C1", 
            "#FEE79B", 
            "#FFCE66", 
            "#FFAC3A", 
            "#F68720", 
            "#E1640E", 
            "#C04703", 
            "#933205", 
            "#662506"
          ], 
          "11": [
            "#FFFFE5", 
            "#FFF9C4", 
            "#FFEBA2", 
            "#FFD777", 
            "#FEBC48", 
            "#FE9929", 
            "#F07818", 
            "#D95B09", 
            "#B74203", 
            "#8F3105", 
            "#662506"
          ]
        }, 
        "name_en": "Direct Normal Irradiance DNI", 
        "id": "Solar_Seq_DNI_Thermal"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "ساعات سطوع الشمس اليومية الفعلية (0-14 ساعة)", 
        "source": "WMO Sunshine Duration Climatological Standard", 
        "classes": {
          "3": [
            "#FFFFD4", 
            "#FE9929", 
            "#8C2D04"
          ], 
          "4": [
            "#FFFFD4", 
            "#FEC44F", 
            "#EC7014", 
            "#8C2D04"
          ], 
          "5": [
            "#FFFFD4", 
            "#FFD371", 
            "#FE9929", 
            "#DC5E0B", 
            "#8C2D04"
          ], 
          "6": [
            "#FFFFD4", 
            "#FFDD84", 
            "#FFB340", 
            "#F3811D", 
            "#D25305", 
            "#8C2D04"
          ], 
          "7": [
            "#FFFFD4", 
            "#FEE391", 
            "#FEC44F", 
            "#FE9929", 
            "#EC7014", 
            "#CC4C02", 
            "#8C2D04"
          ], 
          "8": [
            "#FFFFD4", 
            "#FFE79B", 
            "#FFCD63", 
            "#FFAC3A", 
            "#F68820", 
            "#E3660F", 
            "#C34703", 
            "#8C2D04"
          ], 
          "9": [
            "#FFFFD4", 
            "#FFEAA2", 
            "#FFD371", 
            "#FEB946", 
            "#FE9929", 
            "#F17A19", 
            "#DC5E0B", 
            "#BC4403", 
            "#8C2D04"
          ], 
          "10": [
            "#FFFFD4", 
            "#FFECA7", 
            "#FFD97C", 
            "#FEC44F", 
            "#FFA836", 
            "#F88C22", 
            "#EC7014", 
            "#D75807", 
            "#B64103", 
            "#8C2D04"
          ], 
          "11": [
            "#FFFFD4", 
            "#FFEEAC", 
            "#FFDD84", 
            "#FFCA5D", 
            "#FFB340", 
            "#FE9929", 
            "#F3811D", 
            "#E66910", 
            "#D25305", 
            "#B23F03", 
            "#8C2D04"
          ]
        }, 
        "name_en": "Daily Sunshine Hours", 
        "id": "Solar_Seq_SunshineDuration"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الإشعاع الشمسي المشتت في الغلاف الجوي", 
        "source": "Solar Energy Engineering Diffuse Radiation", 
        "classes": {
          "3": [
            "#F7FCF0", 
            "#A8DDB5", 
            "#2B8CBE"
          ], 
          "4": [
            "#F7FCF0", 
            "#CCEBC5", 
            "#7BCCC4", 
            "#2B8CBE"
          ], 
          "5": [
            "#F7FCF0", 
            "#D6EFD0", 
            "#A8DDB5", 
            "#67BFCC", 
            "#2B8CBE"
          ], 
          "6": [
            "#F7FCF0", 
            "#DCF1D7", 
            "#BEE5BF", 
            "#8ED3BE", 
            "#59B8D0", 
            "#2B8CBE"
          ], 
          "7": [
            "#F7FCF0", 
            "#E0F3DB", 
            "#CCEBC5", 
            "#A8DDB5", 
            "#7BCCC4", 
            "#4EB3D3", 
            "#2B8CBE"
          ], 
          "8": [
            "#F7FCF0", 
            "#E3F4DE", 
            "#D2EDCB", 
            "#B8E3BC", 
            "#96D6BC", 
            "#70C5C8", 
            "#4AADD0", 
            "#2B8CBE"
          ], 
          "9": [
            "#F7FCF0", 
            "#E6F5E0", 
            "#D6EFD0", 
            "#C3E8C1", 
            "#A8DDB5", 
            "#87D0C0", 
            "#67BFCC", 
            "#46A9CE", 
            "#2B8CBE"
          ], 
          "10": [
            "#F7FCF0", 
            "#E8F6E2", 
            "#D9F0D4", 
            "#CCEBC5", 
            "#B4E2BA", 
            "#9AD7BA", 
            "#7BCCC4", 
            "#60BBCE", 
            "#44A6CC", 
            "#2B8CBE"
          ], 
          "11": [
            "#F7FCF0", 
            "#E9F7E3", 
            "#DCF1D7", 
            "#D0EDC9", 
            "#BEE5BF", 
            "#A8DDB5", 
            "#8ED3BE", 
            "#74C7C7", 
            "#59B8D0", 
            "#41A3CB", 
            "#2B8CBE"
          ]
        }, 
        "name_en": "Diffuse Horizontal Irradiance", 
        "id": "Solar_Seq_DHI_Diffuse"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الإشعاع الشمسي للألواح الكهروضوئية المائلة", 
        "source": "PVGIS European Commission Photovoltaic Platform", 
        "classes": {
          "3": [
            "#FFFFE5", 
            "#FEC44F", 
            "#A50F15"
          ], 
          "4": [
            "#FFFFE5", 
            "#FEE391", 
            "#FB6A4A", 
            "#A50F15"
          ], 
          "5": [
            "#FFFFE5", 
            "#FFEDA7", 
            "#FEC44F", 
            "#ED4E38", 
            "#A50F15"
          ], 
          "6": [
            "#FFFFE5", 
            "#FFF3B3", 
            "#FFD777", 
            "#FE914C", 
            "#E43C2D", 
            "#A50F15"
          ], 
          "7": [
            "#FFFFE5", 
            "#FFF7BC", 
            "#FEE391", 
            "#FEC44F", 
            "#FB6A4A", 
            "#DE2D26", 
            "#A50F15"
          ], 
          "8": [
            "#FFFFE5", 
            "#FFF8C2", 
            "#FFE99D", 
            "#FFD16C", 
            "#FEA04D", 
            "#F35B3F", 
            "#D62923", 
            "#A50F15"
          ], 
          "9": [
            "#FFFFE5", 
            "#FFF9C6", 
            "#FFEDA7", 
            "#FFDB81", 
            "#FEC44F", 
            "#FD834C", 
            "#ED4E38", 
            "#CF2622", 
            "#A50F15"
          ], 
          "10": [
            "#FFFFE5", 
            "#FFFACA", 
            "#FFF0AE", 
            "#FEE391", 
            "#FFCE66", 
            "#FEA84E", 
            "#FB6A4A", 
            "#E84432", 
            "#CB2420", 
            "#A50F15"
          ], 
          "11": [
            "#FFFFE5", 
            "#FFFACC", 
            "#FFF3B3", 
            "#FEE79A", 
            "#FFD777", 
            "#FEC44F", 
            "#FE914C", 
            "#F55F43", 
            "#E43C2D", 
            "#C7221F", 
            "#A50F15"
          ]
        }, 
        "name_en": "Global Tilted Irradiance GTI", 
        "id": "Solar_Seq_GTI_Tilted"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الإشعاع الشمسي الفعال في البناء الضوئي الزراعي", 
        "source": "Agrometeorology Crop Photosynthesis Scale", 
        "classes": {
          "3": [
            "#F7FCF5", 
            "#A1D99B", 
            "#006D2C"
          ], 
          "4": [
            "#F7FCF5", 
            "#C7E9C0", 
            "#74C476", 
            "#006D2C"
          ], 
          "5": [
            "#F7FCF5", 
            "#D6EFD0", 
            "#A1D99B", 
            "#55B365", 
            "#006D2C"
          ], 
          "6": [
            "#F7FCF5", 
            "#DFF3DA", 
            "#B8E3B1", 
            "#86CC85", 
            "#41AA5B", 
            "#006D2C"
          ], 
          "7": [
            "#F7FCF5", 
            "#E5F5E0", 
            "#C7E9C0", 
            "#A1D99B", 
            "#74C476", 
            "#31A354", 
            "#006D2C"
          ], 
          "8": [
            "#F7FCF5", 
            "#E8F6E3", 
            "#D0ECC9", 
            "#B1E0AB", 
            "#8ED08B", 
            "#63BB6C", 
            "#2B9B4E", 
            "#006D2C"
          ], 
          "9": [
            "#F7FCF5", 
            "#EAF7E5", 
            "#D6EFD0", 
            "#BEE5B7", 
            "#A1D99B", 
            "#80C97F", 
            "#55B365", 
            "#27954A", 
            "#006D2C"
          ], 
          "10": [
            "#F7FCF5", 
            "#EBF7E7", 
            "#DBF1D5", 
            "#C7E9C0", 
            "#AEDEA7", 
            "#92D28F", 
            "#74C476", 
            "#4AAE5F", 
            "#239146", 
            "#006D2C"
          ], 
          "11": [
            "#F7FCF5", 
            "#ECF8E8", 
            "#DFF3DA", 
            "#CDEBC6", 
            "#B8E3B1", 
            "#A1D99B", 
            "#86CC85", 
            "#68BD6F", 
            "#41AA5B", 
            "#208D44", 
            "#006D2C"
          ]
        }, 
        "name_en": "Photosynthetically Active PAR", 
        "id": "Solar_Seq_PAR_Agronomy"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "معامل صفاء السماء ونفاذية الغلاف الجوي للإشعاع", 
        "source": "Solar Radiation Clearness Index Modeling", 
        "classes": {
          "3": [
            "#EDF8FB", 
            "#8C96C6", 
            "#810F7C"
          ], 
          "4": [
            "#EDF8FB", 
            "#A6BAD9", 
            "#8B6CB1", 
            "#810F7C"
          ], 
          "5": [
            "#EDF8FB", 
            "#B3CDE3", 
            "#8C96C6", 
            "#8856A7", 
            "#810F7C"
          ], 
          "6": [
            "#EDF8FB", 
            "#BFD5E8", 
            "#9CACD2", 
            "#8C7DBA", 
            "#874B9E", 
            "#810F7C"
          ], 
          "7": [
            "#EDF8FB", 
            "#C6DBEB", 
            "#A6BAD9", 
            "#8C96C6", 
            "#8B6CB1", 
            "#874398", 
            "#810F7C"
          ], 
          "8": [
            "#EDF8FB", 
            "#CCDFED", 
            "#ADC5DF", 
            "#97A5CE", 
            "#8C84BD", 
            "#8960AB", 
            "#863D94", 
            "#810F7C"
          ], 
          "9": [
            "#EDF8FB", 
            "#D0E2EF", 
            "#B3CDE3", 
            "#A0B1D4", 
            "#8C96C6", 
            "#8B77B6", 
            "#8856A7", 
            "#863991", 
            "#810F7C"
          ], 
          "10": [
            "#EDF8FB", 
            "#D3E5F0", 
            "#B9D2E6", 
            "#A6BAD9", 
            "#95A2CC", 
            "#8C88BF", 
            "#8B6CB1", 
            "#8850A2", 
            "#85358F", 
            "#810F7C"
          ], 
          "11": [
            "#EDF8FB", 
            "#D6E7F1", 
            "#BFD5E8", 
            "#ABC2DD", 
            "#9CACD2", 
            "#8C96C6", 
            "#8C7DBA", 
            "#8A63AD", 
            "#874B9E", 
            "#85328D", 
            "#810F7C"
          ]
        }, 
        "name_en": "Atmosphere Clearness Index Kt", 
        "id": "Solar_Seq_ClearnessIndex"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "معامل انعكاس سطح الأرض للإشعاع الشمسي (الألبيدو)", 
        "source": "NASA MODIS / VIIRS Surface Albedo", 
        "classes": {
          "3": [
            "#000000", 
            "#999999", 
            "#FFFFFF"
          ], 
          "4": [
            "#000000", 
            "#666666", 
            "#CCCCCC", 
            "#FFFFFF"
          ], 
          "5": [
            "#000000", 
            "#4C4C4C", 
            "#999999", 
            "#DDDDDD", 
            "#FFFFFF"
          ], 
          "6": [
            "#000000", 
            "#3D3D3D", 
            "#7A7A7A", 
            "#B7B7B7", 
            "#E7E7E7", 
            "#FFFFFF"
          ], 
          "7": [
            "#000000", 
            "#333333", 
            "#666666", 
            "#999999", 
            "#CCCCCC", 
            "#EEEEEE", 
            "#FFFFFF"
          ], 
          "8": [
            "#000000", 
            "#2C2C2C", 
            "#575757", 
            "#838383", 
            "#AFAFAF", 
            "#D6D6D6", 
            "#F0F0F0", 
            "#FFFFFF"
          ], 
          "9": [
            "#000000", 
            "#282828", 
            "#4C4C4C", 
            "#727272", 
            "#999999", 
            "#BFBFBF", 
            "#DDDDDD", 
            "#F2F2F2", 
            "#FFFFFF"
          ], 
          "10": [
            "#000000", 
            "#242424", 
            "#434343", 
            "#666666", 
            "#888888", 
            "#AAAAAA", 
            "#CCCCCC", 
            "#E3E3E3", 
            "#F4F4F4", 
            "#FFFFFF"
          ], 
          "11": [
            "#000000", 
            "#212121", 
            "#3D3D3D", 
            "#5B5B5B", 
            "#7A7A7A", 
            "#999999", 
            "#B7B7B7", 
            "#D3D3D3", 
            "#E7E7E7", 
            "#F5F5F5", 
            "#FFFFFF"
          ]
        }, 
        "name_en": "Surface Shortwave Albedo", 
        "id": "Solar_Multi_SolarAlbedo"
      }
    ], 
    "folder": "07_Solar_Radiation", 
    "name_en": "Solar Radiation"
  }, 
  {
    "name_ar": "مؤشر الأشعة فوق البنفسجية", 
    "styles": [
      {
        "category": "Multi-Hue", 
        "name_ar": "المعيار الدولي الإلزامي لمنظمة الصحة العالمية", 
        "source": "WHO / WMO / UNEP (ISBN 92 4 159007 6)", 
        "classes": {
          "3": [
            "#289500", 
            "#E83A0A", 
            "#452494"
          ], 
          "4": [
            "#289500", 
            "#FBBA00", 
            "#B80010", 
            "#452494"
          ], 
          "5": [
            "#289500", 
            "#D0D900", 
            "#E83A0A", 
            "#A51C3E", 
            "#452494"
          ], 
          "6": [
            "#289500", 
            "#96C900", 
            "#FA7A00", 
            "#CE0010", 
            "#98337C", 
            "#452494"
          ], 
          "7": [
            "#289500", 
            "#6CBD00", 
            "#FBBA00", 
            "#E83A0A", 
            "#B80010", 
            "#8440A8", 
            "#452494"
          ], 
          "8": [
            "#289500", 
            "#48B500", 
            "#F7E400", 
            "#F85900", 
            "#D80010", 
            "#A80010", 
            "#6B49C8", 
            "#452494"
          ], 
          "9": [
            "#289500", 
            "#44B100", 
            "#D0D900", 
            "#FC9300", 
            "#E83A0A", 
            "#C60010", 
            "#A51C3E", 
            "#6644C1", 
            "#452494"
          ], 
          "10": [
            "#289500", 
            "#41AE00", 
            "#B0D000", 
            "#FBBA00", 
            "#F45303", 
            "#DC160F", 
            "#B80010", 
            "#A02960", 
            "#6241BC", 
            "#452494"
          ], 
          "11": [
            "#289500", 
            "#3FAB00", 
            "#96C900", 
            "#F9D700", 
            "#FA7A00", 
            "#E83A0A", 
            "#CE0010", 
            "#AD0010", 
            "#98337C", 
            "#603EB8", 
            "#452494"
          ]
        }, 
        "name_en": "WHO Global Solar UV Index", 
        "id": "UV_Standard_WHO"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس الحماية الصحية من أضرار الأشعة الحارقة", 
        "source": "US Environmental Protection Agency (EPA)", 
        "classes": {
          "3": [
            "#38A800", 
            "#FFAA00", 
            "#4C005C"
          ], 
          "4": [
            "#38A800", 
            "#FFFF00", 
            "#FF0000", 
            "#4C005C"
          ], 
          "5": [
            "#38A800", 
            "#BEE400", 
            "#FFAA00", 
            "#CD0060", 
            "#4C005C"
          ], 
          "6": [
            "#38A800", 
            "#95D400", 
            "#FFDD00", 
            "#FF6400", 
            "#A7008B", 
            "#4C005C"
          ], 
          "7": [
            "#38A800", 
            "#79C900", 
            "#FFFF00", 
            "#FFAA00", 
            "#FF0000", 
            "#8400A8", 
            "#4C005C"
          ], 
          "8": [
            "#38A800", 
            "#71C400", 
            "#DAF000", 
            "#FFCF00", 
            "#FF7A00", 
            "#E40040", 
            "#7C009D", 
            "#4C005C"
          ], 
          "9": [
            "#38A800", 
            "#6AC100", 
            "#BEE400", 
            "#FFEA00", 
            "#FFAA00", 
            "#FF4D00", 
            "#CD0060", 
            "#760094", 
            "#4C005C"
          ], 
          "10": [
            "#38A800", 
            "#65BE00", 
            "#A8DB00", 
            "#FFFF00", 
            "#FFC700", 
            "#FF8600", 
            "#FF0000", 
            "#B90078", 
            "#71008E", 
            "#4C005C"
          ], 
          "11": [
            "#38A800", 
            "#61BC00", 
            "#95D400", 
            "#E5F400", 
            "#FFDD00", 
            "#FFAA00", 
            "#FF6400", 
            "#EC0032", 
            "#A7008B", 
            "#6D0089", 
            "#4C005C"
          ]
        }, 
        "name_en": "EPA Erythemal Damage Spectrum", 
        "id": "UV_EPA_HealthRisk"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الجرعة اليومية للأشعة فوق البنفسجية المؤثرة حيوياً", 
        "source": "CIE S 007/E-1998 Erythemal Action Spectrum", 
        "classes": {
          "3": [
            "#FFFFCC", 
            "#FD7033", 
            "#800026"
          ], 
          "4": [
            "#FFFFCC", 
            "#FEA647", 
            "#EB3021", 
            "#800026"
          ], 
          "5": [
            "#FFFFCC", 
            "#FEBC57", 
            "#FD7033", 
            "#D9141F", 
            "#800026"
          ], 
          "6": [
            "#FFFFCC", 
            "#FFC965", 
            "#FD953F", 
            "#F74627", 
            "#CC0B23", 
            "#800026"
          ], 
          "7": [
            "#FFFFCC", 
            "#FED36F", 
            "#FEA647", 
            "#FD7033", 
            "#EB3021", 
            "#C30425", 
            "#800026"
          ], 
          "8": [
            "#FFFFCC", 
            "#FED976", 
            "#FEB24C", 
            "#FD8D3C", 
            "#FC4E2A", 
            "#E31A1C", 
            "#BD0026", 
            "#800026"
          ], 
          "9": [
            "#FFFFCC", 
            "#FFDE81", 
            "#FEBC57", 
            "#FE9B42", 
            "#FD7033", 
            "#F33E25", 
            "#D9141F", 
            "#B50026", 
            "#800026"
          ], 
          "10": [
            "#FFFFCC", 
            "#FFE189", 
            "#FFC35F", 
            "#FEA647", 
            "#FD873A", 
            "#FC562C", 
            "#EB3021", 
            "#D21021", 
            "#AF0026", 
            "#800026"
          ], 
          "11": [
            "#FFFFCC", 
            "#FFE490", 
            "#FFC965", 
            "#FEAE4A", 
            "#FD953F", 
            "#FD7033", 
            "#F74627", 
            "#E6221D", 
            "#CC0B23", 
            "#AA0026", 
            "#800026"
          ]
        }, 
        "name_en": "Daily Erythemal UV Dose", 
        "id": "UV_ErythemalDose"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "ذروة الأشعة فوق البنفسجية الشديدة في ظهيرة الصيف", 
        "source": "Tropical & Desert UV Radiation Monitoring", 
        "classes": {
          "3": [
            "#229954", 
            "#EA7545", 
            "#512E5F"
          ], 
          "4": [
            "#229954", 
            "#EFAB4A", 
            "#D04863", 
            "#512E5F"
          ], 
          "5": [
            "#229954", 
            "#F2C244", 
            "#EA7545", 
            "#AB4591", 
            "#512E5F"
          ], 
          "6": [
            "#229954", 
            "#F4D03F", 
            "#EB984E", 
            "#E74C3C", 
            "#8E44AD", 
            "#512E5F"
          ], 
          "7": [
            "#229954", 
            "#D7C844", 
            "#EFAB4A", 
            "#EA7545", 
            "#D04863", 
            "#83409F", 
            "#512E5F"
          ], 
          "8": [
            "#229954", 
            "#C2C147", 
            "#F1B847", 
            "#EB8E4B", 
            "#E8593E", 
            "#BC467E", 
            "#7C3E96", 
            "#512E5F"
          ], 
          "9": [
            "#229954", 
            "#B2BD4A", 
            "#F2C244", 
            "#EC9F4D", 
            "#EA7545", 
            "#DF4A4B", 
            "#AB4591", 
            "#773C8F", 
            "#512E5F"
          ], 
          "10": [
            "#229954", 
            "#A6B94B", 
            "#F3CA41", 
            "#EFAB4A", 
            "#EB894A", 
            "#E96040", 
            "#D04863", 
            "#9C44A1", 
            "#723A89", 
            "#512E5F"
          ], 
          "11": [
            "#229954", 
            "#9BB64C", 
            "#F4D03F", 
            "#F0B448", 
            "#EB984E", 
            "#EA7545", 
            "#E74C3C", 
            "#C24676", 
            "#8E44AD", 
            "#6F3985", 
            "#512E5F"
          ]
        }, 
        "name_en": "Tropical Summer Noon Peak UV", 
        "id": "UV_SummerPeak"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس فيتزباتريك لتحمل الجلد وسرعة حروق الشمس", 
        "source": "Harvard Medical School / Fitzpatrick Phototypes", 
        "classes": {
          "3": [
            "#FCEFE6", 
            "#CF8F66", 
            "#452514"
          ], 
          "4": [
            "#FCEFE6", 
            "#EBB897", 
            "#A4663E", 
            "#452514"
          ], 
          "5": [
            "#FCEFE6", 
            "#F5CCB2", 
            "#CF8F66", 
            "#8A512F", 
            "#452514"
          ], 
          "6": [
            "#FCEFE6", 
            "#FAD8C3", 
            "#E3A882", 
            "#BA774B", 
            "#7A4526", 
            "#452514"
          ], 
          "7": [
            "#FCEFE6", 
            "#FBDCC9", 
            "#EBB897", 
            "#CF8F66", 
            "#A4663E", 
            "#713F23", 
            "#452514"
          ], 
          "8": [
            "#FCEFE6", 
            "#FBDFCD", 
            "#F1C3A7", 
            "#DDA17A", 
            "#C07E53", 
            "#955A35", 
            "#6A3C21", 
            "#452514"
          ], 
          "9": [
            "#FCEFE6", 
            "#FBE1D0", 
            "#F5CCB2", 
            "#E6AE8A", 
            "#CF8F66", 
            "#B27146", 
            "#8A512F", 
            "#66391F", 
            "#452514"
          ], 
          "10": [
            "#FCEFE6", 
            "#FBE2D2", 
            "#F8D3BC", 
            "#EBB897", 
            "#DA9D75", 
            "#C38257", 
            "#A4663E", 
            "#814A2A", 
            "#62361E", 
            "#452514"
          ], 
          "11": [
            "#FCEFE6", 
            "#FBE3D4", 
            "#FAD8C3", 
            "#EFC0A2", 
            "#E3A882", 
            "#CF8F66", 
            "#BA774B", 
            "#995D38", 
            "#7A4526", 
            "#5F351D", 
            "#452514"
          ]
        }, 
        "name_en": "Fitzpatrick Skin Phototypes", 
        "id": "UV_Multi_Fitzpatrick"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "مؤشر الأشعة فوق البنفسجية في المرتفعات والجبال", 
        "source": "Alpine Solar Radiation Amplification Studies", 
        "classes": {
          "3": [
            "#289500", 
            "#D80010", 
            "#1F0445"
          ], 
          "4": [
            "#289500", 
            "#F85900", 
            "#6B49C8", 
            "#1F0445"
          ], 
          "5": [
            "#289500", 
            "#FCA400", 
            "#D80010", 
            "#5330A1", 
            "#1F0445"
          ], 
          "6": [
            "#289500", 
            "#FACB00", 
            "#EB4108", 
            "#AD367F", 
            "#44228A", 
            "#1F0445"
          ], 
          "7": [
            "#289500", 
            "#F7E400", 
            "#F85900", 
            "#D80010", 
            "#6B49C8", 
            "#3B187B", 
            "#1F0445"
          ], 
          "8": [
            "#289500", 
            "#DCD900", 
            "#FB8600", 
            "#E6350B", 
            "#BD2D61", 
            "#5D3BB1", 
            "#371573", 
            "#1F0445"
          ], 
          "9": [
            "#289500", 
            "#C8D100", 
            "#FCA400", 
            "#F04A06", 
            "#D80010", 
            "#9B3D9A", 
            "#5330A1", 
            "#34136D", 
            "#1F0445"
          ], 
          "10": [
            "#289500", 
            "#B9CA00", 
            "#FBBA00", 
            "#F85900", 
            "#E32D0D", 
            "#C42751", 
            "#6B49C8", 
            "#4B2894", 
            "#311168", 
            "#1F0445"
          ], 
          "11": [
            "#289500", 
            "#ACC500", 
            "#FACB00", 
            "#FA7A00", 
            "#EB4108", 
            "#D80010", 
            "#AD367F", 
            "#613FB8", 
            "#44228A", 
            "#2F0F65", 
            "#1F0445"
          ]
        }, 
        "name_en": "High-Altitude Alpine UV", 
        "id": "UV_Multi_HighAltitude"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "النطاق الشمسي الحيوي الآمن لتكوين فيتامين د", 
        "source": "Photobiology & Endocrine Society Guidelines", 
        "classes": {
          "3": [
            "#EDF8FB", 
            "#66C2A4", 
            "#006D2C"
          ], 
          "4": [
            "#EDF8FB", 
            "#9AD7CD", 
            "#43AD76", 
            "#006D2C"
          ], 
          "5": [
            "#EDF8FB", 
            "#B2E2E2", 
            "#66C2A4", 
            "#2CA25F", 
            "#006D2C"
          ], 
          "6": [
            "#EDF8FB", 
            "#BEE6E7", 
            "#86CFBC", 
            "#52B588", 
            "#259755", 
            "#006D2C"
          ], 
          "7": [
            "#EDF8FB", 
            "#C6E9EA", 
            "#9AD7CD", 
            "#66C2A4", 
            "#43AD76", 
            "#20904E", 
            "#006D2C"
          ], 
          "8": [
            "#EDF8FB", 
            "#CCEBED", 
            "#A8DDD9", 
            "#7DCBB5", 
            "#58B990", 
            "#36A769", 
            "#1C8B49", 
            "#006D2C"
          ], 
          "9": [
            "#EDF8FB", 
            "#D0EDEE", 
            "#B2E2E2", 
            "#8DD2C3", 
            "#66C2A4", 
            "#4CB281", 
            "#2CA25F", 
            "#198745", 
            "#006D2C"
          ], 
          "10": [
            "#EDF8FB", 
            "#D3EEF0", 
            "#B9E4E5", 
            "#9AD7CD", 
            "#78C9B2", 
            "#5BBB94", 
            "#43AD76", 
            "#289C59", 
            "#178442", 
            "#006D2C"
          ], 
          "11": [
            "#EDF8FB", 
            "#D6EFF1", 
            "#BEE6E7", 
            "#A3DCD5", 
            "#86CFBC", 
            "#66C2A4", 
            "#52B588", 
            "#3AA86D", 
            "#259755", 
            "#158240", 
            "#006D2C"
          ]
        }, 
        "name_en": "Vitamin D Optimal Synthesis", 
        "id": "UV_Seq_VitaminDSynthesis"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ الأشعة الناتج عن ترقق طبقة الأوزون", 
        "source": "WMO/UNEP Scientific Assessment of Ozone Depletion", 
        "classes": {
          "3": [
            "#74ADD1", 
            "#FFFFBF", 
            "#F46D43"
          ], 
          "4": [
            "#4575B4", 
            "#ABD9E9", 
            "#FDAE61", 
            "#D73027"
          ], 
          "5": [
            "#4575B4", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#D73027"
          ], 
          "6": [
            "#4575B4", 
            "#74ADD1", 
            "#ABD9E9", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027"
          ], 
          "7": [
            "#4575B4", 
            "#74ADD1", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027"
          ], 
          "8": [
            "#4575B4", 
            "#659AC7", 
            "#87BBD9", 
            "#ABD9E9", 
            "#FDAE61", 
            "#F8844D", 
            "#EB5B39", 
            "#D73027"
          ], 
          "9": [
            "#4575B4", 
            "#659AC7", 
            "#87BBD9", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F8844D", 
            "#EB5B39", 
            "#D73027"
          ], 
          "10": [
            "#4575B4", 
            "#5E91C3", 
            "#74ADD1", 
            "#90C3DD", 
            "#ABD9E9", 
            "#FDAE61", 
            "#F98F52", 
            "#F46D43", 
            "#E65135", 
            "#D73027"
          ], 
          "11": [
            "#4575B4", 
            "#5E91C3", 
            "#74ADD1", 
            "#90C3DD", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F98F52", 
            "#F46D43", 
            "#E65135", 
            "#D73027"
          ]
        }, 
        "name_en": "Stratospheric Ozone UV Anomaly", 
        "id": "UV_Div_OzoneDepletion"
      }
    ], 
    "folder": "08_UV_Index", 
    "name_en": "UV Index"
  }, 
  {
    "name_ar": "الغطاء السحابي ونقاء السماء", 
    "styles": [
      {
        "category": "Multi-Hue", 
        "name_ar": "مقياس الأوكتا العالمي للسحب (من 0 إلى 8 أوكتا)", 
        "source": "WMO International Cloud Atlas (Okta Scale)", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#6AA6CE", 
            "#17202A"
          ], 
          "4": [
            "#FFFFFF", 
            "#A9CCE3", 
            "#2980B9", 
            "#17202A"
          ], 
          "5": [
            "#FFFFFF", 
            "#C9DFEE", 
            "#6AA6CE", 
            "#2575A8", 
            "#17202A"
          ], 
          "6": [
            "#FFFFFF", 
            "#D9E9F3", 
            "#90BDDB", 
            "#458FC1", 
            "#226A99", 
            "#17202A"
          ], 
          "7": [
            "#FFFFFF", 
            "#E0EDF6", 
            "#A9CCE3", 
            "#6AA6CE", 
            "#2980B9", 
            "#20608A", 
            "#17202A"
          ], 
          "8": [
            "#FFFFFF", 
            "#E4F1F8", 
            "#BCD7E9", 
            "#85B7D7", 
            "#4F95C5", 
            "#277AB0", 
            "#1E5880", 
            "#17202A"
          ], 
          "9": [
            "#FFFFFF", 
            "#E8F3FA", 
            "#C9DFEE", 
            "#9AC3DE", 
            "#6AA6CE", 
            "#3C89BE", 
            "#2575A8", 
            "#1C5378", 
            "#17202A"
          ], 
          "10": [
            "#FFFFFF", 
            "#EBF5FB", 
            "#D4E6F1", 
            "#A9CCE3", 
            "#7FB3D5", 
            "#5499C7", 
            "#2980B9", 
            "#2471A3", 
            "#1B4F72", 
            "#17202A"
          ], 
          "11": [
            "#FFFFFF", 
            "#EDF6FB", 
            "#D9E9F3", 
            "#B6D4E7", 
            "#90BDDB", 
            "#6AA6CE", 
            "#458FC1", 
            "#277BB2", 
            "#226A99", 
            "#1C4A6A", 
            "#17202A"
          ]
        }, 
        "name_en": "WMO Okta Cloud Scale", 
        "id": "Cloud_Seq_Okta"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "نسبة الغطاء السحابي الكلي المئوية (0% - 100%)", 
        "source": "MODIS / EUMETSAT Cloud Fraction", 
        "classes": {
          "3": [
            "#F7FBFF", 
            "#6BAED6", 
            "#08306B"
          ], 
          "4": [
            "#F7FBFF", 
            "#ACD0E6", 
            "#3987C0", 
            "#08306B"
          ], 
          "5": [
            "#F7FBFF", 
            "#C6DBEF", 
            "#6BAED6", 
            "#2171B5", 
            "#08306B"
          ], 
          "6": [
            "#F7FBFF", 
            "#D0E1F2", 
            "#94C4DF", 
            "#4B98C9", 
            "#1964AB", 
            "#08306B"
          ], 
          "7": [
            "#F7FBFF", 
            "#D6E6F4", 
            "#ACD0E6", 
            "#6BAED6", 
            "#3987C0", 
            "#135BA4", 
            "#08306B"
          ], 
          "8": [
            "#F7FBFF", 
            "#DBE9F6", 
            "#BBD6EB", 
            "#89BEDC", 
            "#559ECD", 
            "#2C7ABA", 
            "#0D55A0", 
            "#08306B"
          ], 
          "9": [
            "#F7FBFF", 
            "#DEEBF7", 
            "#C6DBEF", 
            "#9ECAE1", 
            "#6BAED6", 
            "#4292C6", 
            "#2171B5", 
            "#08519C", 
            "#08306B"
          ], 
          "10": [
            "#F7FBFF", 
            "#E1EDF8", 
            "#CBDFF1", 
            "#ACD0E6", 
            "#83BADB", 
            "#5AA1CF", 
            "#3987C0", 
            "#1D6AAF", 
            "#084D96", 
            "#08306B"
          ], 
          "11": [
            "#F7FBFF", 
            "#E3EEF9", 
            "#D0E1F2", 
            "#B6D4E9", 
            "#94C4DF", 
            "#6BAED6", 
            "#4B98C9", 
            "#307EBC", 
            "#1964AB", 
            "#084A92", 
            "#08306B"
          ]
        }, 
        "name_en": "Total Cloud Fraction %", 
        "id": "Cloud_Seq_Fraction"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "درجات حرارة قمم السحب بالأشعة تحت الحمراء", 
        "source": "NOAA GOES-R Advanced Baseline Imager (ABI)", 
        "classes": {
          "3": [
            "#FFFFFF", 
            "#333333", 
            "#FF0000"
          ], 
          "4": [
            "#FFFFFF", 
            "#777777", 
            "#766EC5", 
            "#FF0000"
          ], 
          "5": [
            "#FFFFFF", 
            "#999999", 
            "#333333", 
            "#00FF00", 
            "#FF0000"
          ], 
          "6": [
            "#FFFFFF", 
            "#ADADAD", 
            "#5B5B5B", 
            "#371BD3", 
            "#9BFF00", 
            "#FF0000"
          ], 
          "7": [
            "#FFFFFF", 
            "#BBBBBB", 
            "#777777", 
            "#333333", 
            "#766EC5", 
            "#CBFF00", 
            "#FF0000"
          ], 
          "8": [
            "#FFFFFF", 
            "#C5C5C5", 
            "#8A8A8A", 
            "#4F4F4F", 
            "#4327A2", 
            "#73C27A", 
            "#E9FF00", 
            "#FF0000"
          ], 
          "9": [
            "#FFFFFF", 
            "#CCCCCC", 
            "#999999", 
            "#666666", 
            "#333333", 
            "#0000FF", 
            "#00FF00", 
            "#FFFF00", 
            "#FF0000"
          ], 
          "10": [
            "#FFFFFF", 
            "#D2D2D2", 
            "#A4A4A4", 
            "#777777", 
            "#494949", 
            "#442C88", 
            "#766EC5", 
            "#73FF00", 
            "#FFEB00", 
            "#FF0000"
          ], 
          "11": [
            "#FFFFFF", 
            "#D6D6D6", 
            "#ADADAD", 
            "#848484", 
            "#5B5B5B", 
            "#333333", 
            "#371BD3", 
            "#7CA993", 
            "#9BFF00", 
            "#FFDB00", 
            "#FF0000"
          ]
        }, 
        "name_en": "Satellite IR Cloud Top Temp", 
        "id": "Cloud_Multi_IR_CloudTop"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "السمك البصري للغيوم وكثافة حجب الضوء", 
        "source": "NASA MODIS Cloud Optical Properties", 
        "classes": {
          "3": [
            "#F7FCF0", 
            "#7BCCC4", 
            "#084081"
          ], 
          "4": [
            "#F7FCF0", 
            "#B4E2BA", 
            "#44A6CC", 
            "#084081"
          ], 
          "5": [
            "#F7FCF0", 
            "#CCEBC5", 
            "#7BCCC4", 
            "#2B8CBE", 
            "#084081"
          ], 
          "6": [
            "#F7FCF0", 
            "#D4EECE", 
            "#A0DAB8", 
            "#59B8D0", 
            "#217DB7", 
            "#084081"
          ], 
          "7": [
            "#F7FCF0", 
            "#D9F0D4", 
            "#B4E2BA", 
            "#7BCCC4", 
            "#44A6CC", 
            "#1974B2", 
            "#084081"
          ], 
          "8": [
            "#F7FCF0", 
            "#DDF2D8", 
            "#C2E7C0", 
            "#96D6BC", 
            "#64BECD", 
            "#3697C4", 
            "#116DAF", 
            "#084081"
          ], 
          "9": [
            "#F7FCF0", 
            "#E0F3DB", 
            "#CCEBC5", 
            "#A8DDB5", 
            "#7BCCC4", 
            "#4EB3D3", 
            "#2B8CBE", 
            "#0868AC", 
            "#084081"
          ], 
          "10": [
            "#F7FCF0", 
            "#E3F4DD", 
            "#D0EDCA", 
            "#B4E2BA", 
            "#90D4BD", 
            "#6AC1CB", 
            "#44A6CC", 
            "#2684BA", 
            "#0963A7", 
            "#084081"
          ], 
          "11": [
            "#F7FCF0", 
            "#E5F5DF", 
            "#D4EECE", 
            "#BEE5BF", 
            "#A0DAB8", 
            "#7BCCC4", 
            "#59B8D0", 
            "#3B9BC6", 
            "#217DB7", 
            "#0960A3", 
            "#084081"
          ]
        }, 
        "name_en": "Cloud Optical Thickness Tau", 
        "id": "Cloud_Seq_OpticalDepth"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "السحب المنخفضة وحزام الضباب ومخاطر الرؤية", 
        "source": "Aviation Weather Center Ceiling & Fog Hazard", 
        "classes": {
          "3": [
            "#F8F9F9", 
            "#C0C5CA", 
            "#566573"
          ], 
          "4": [
            "#F8F9F9", 
            "#DCDFE2", 
            "#9CA5AA", 
            "#566573"
          ], 
          "5": [
            "#F8F9F9", 
            "#E5E8EA", 
            "#C0C5CA", 
            "#8A9598", 
            "#566573"
          ], 
          "6": [
            "#F8F9F9", 
            "#EBEDEF", 
            "#D5D8DC", 
            "#ABB2B9", 
            "#7F8C8D", 
            "#566573"
          ], 
          "7": [
            "#F8F9F9", 
            "#EDEFF1", 
            "#DCDFE2", 
            "#C0C5CA", 
            "#9CA5AA", 
            "#788589", 
            "#566573"
          ], 
          "8": [
            "#F8F9F9", 
            "#EFF0F2", 
            "#E2E4E7", 
            "#CFD2D7", 
            "#B1B7BE", 
            "#929CA0", 
            "#738186", 
            "#566573"
          ], 
          "9": [
            "#F8F9F9", 
            "#F0F1F3", 
            "#E5E8EA", 
            "#D8DBDE", 
            "#C0C5CA", 
            "#A5ADB3", 
            "#8A9598", 
            "#707D83", 
            "#566573"
          ], 
          "10": [
            "#F8F9F9", 
            "#F1F2F3", 
            "#E9EBED", 
            "#DCDFE2", 
            "#CCCFD4", 
            "#B4BAC1", 
            "#9CA5AA", 
            "#849092", 
            "#6D7A81", 
            "#566573"
          ], 
          "11": [
            "#F8F9F9", 
            "#F1F3F4", 
            "#EBEDEF", 
            "#E0E2E5", 
            "#D5D8DC", 
            "#C0C5CA", 
            "#ABB2B9", 
            "#959FA3", 
            "#7F8C8D", 
            "#6A7880", 
            "#566573"
          ]
        }, 
        "name_en": "Low Stratus & Fog Ceiling", 
        "id": "Cloud_Seq_LowCloudFog"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "القمم الركامية المخترقة وعواصف البرد الشديدة", 
        "source": "NASA Convective Storm Research", 
        "classes": {
          "3": [
            "#000080", 
            "#FFFF00", 
            "#FFFFFF"
          ], 
          "4": [
            "#000080", 
            "#4FE97C", 
            "#FF6500", 
            "#FFFFFF"
          ], 
          "5": [
            "#000080", 
            "#00BFFF", 
            "#FFFF00", 
            "#FF0000", 
            "#FFFFFF"
          ], 
          "6": [
            "#000080", 
            "#3D82FF", 
            "#6DFF00", 
            "#FF9B00", 
            "#D10042", 
            "#FFFFFF"
          ], 
          "7": [
            "#000080", 
            "#3858FF", 
            "#4FE97C", 
            "#FFFF00", 
            "#FF6500", 
            "#B1005E", 
            "#FFFFFF"
          ], 
          "8": [
            "#000080", 
            "#2734FF", 
            "#4ED1C9", 
            "#A0FF00", 
            "#FFB800", 
            "#FF4000", 
            "#960071", 
            "#FFFFFF"
          ], 
          "9": [
            "#000080", 
            "#0000FF", 
            "#00BFFF", 
            "#00FF00", 
            "#FFFF00", 
            "#FF7F00", 
            "#FF0000", 
            "#800080", 
            "#FFFFFF"
          ], 
          "10": [
            "#000080", 
            "#0000F0", 
            "#349EFF", 
            "#4FE97C", 
            "#B8FF00", 
            "#FFC800", 
            "#FF6500", 
            "#E6002D", 
            "#902F8E", 
            "#FFFFFF"
          ], 
          "11": [
            "#000080", 
            "#0000E4", 
            "#3D82FF", 
            "#54D8B3", 
            "#6DFF00", 
            "#FFFF00", 
            "#FF9B00", 
            "#FF4D00", 
            "#D10042", 
            "#9C4699", 
            "#FFFFFF"
          ]
        }, 
        "name_en": "Overshooting Tops & Hailstorms", 
        "id": "Cloud_Multi_ConvectiveTops"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "عمق الهباء الجوي البصري والعواصف الترابية الصحراوية", 
        "source": "NASA AERONET / MODIS Aerosol Optical Depth", 
        "classes": {
          "3": [
            "#313695", 
            "#FFD78F", 
            "#8C510A"
          ], 
          "4": [
            "#313695", 
            "#CAE5DC", 
            "#F8844D", 
            "#8C510A"
          ], 
          "5": [
            "#313695", 
            "#93BFDC", 
            "#FFD78F", 
            "#ED5F3C", 
            "#8C510A"
          ], 
          "6": [
            "#313695", 
            "#719CC9", 
            "#F0F7C8", 
            "#FCA25B", 
            "#E34B32", 
            "#8C510A"
          ], 
          "7": [
            "#313695", 
            "#5885BD", 
            "#CAE5DC", 
            "#FFD78F", 
            "#F8844D", 
            "#DC3C2B", 
            "#8C510A"
          ], 
          "8": [
            "#313695", 
            "#4575B4", 
            "#ABD9E9", 
            "#FFFFBF", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027", 
            "#8C510A"
          ], 
          "9": [
            "#313695", 
            "#436DB0", 
            "#93BFDC", 
            "#E2F0CF", 
            "#FFD78F", 
            "#FA9755", 
            "#ED5F3C", 
            "#CE3824", 
            "#8C510A"
          ], 
          "10": [
            "#313695", 
            "#4267AD", 
            "#80ABD1", 
            "#CAE5DC", 
            "#FFF6B4", 
            "#FEB76B", 
            "#F8844D", 
            "#E75436", 
            "#C63C21", 
            "#8C510A"
          ], 
          "11": [
            "#313695", 
            "#4162AB", 
            "#719CC9", 
            "#B5DDE5", 
            "#F0F7C8", 
            "#FFD78F", 
            "#FCA25B", 
            "#F57446", 
            "#E34B32", 
            "#C0401F", 
            "#8C510A"
          ]
        }, 
        "name_en": "Aerosol Optical Depth 550nm", 
        "id": "Cloud_Multi_AOD_Aerosol"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "سحب السمحاق العالية ومسار الجليد السحابي", 
        "source": "Cirrus Cloud Radiation & Cryosphere Climatology", 
        "classes": {
          "3": [
            "#F7FBFF", 
            "#6BAED6", 
            "#08306B"
          ], 
          "4": [
            "#F7FBFF", 
            "#AACCE7", 
            "#4085C0", 
            "#08306B"
          ], 
          "5": [
            "#F7FBFF", 
            "#C6DBEF", 
            "#6BAED6", 
            "#2171B5", 
            "#08306B"
          ], 
          "6": [
            "#F7FBFF", 
            "#D0E1F2", 
            "#92C0E0", 
            "#5295C9", 
            "#1D63A6", 
            "#08306B"
          ], 
          "7": [
            "#F7FBFF", 
            "#D6E6F4", 
            "#AACCE7", 
            "#6BAED6", 
            "#4085C0", 
            "#1A5A9C", 
            "#08306B"
          ], 
          "8": [
            "#F7FBFF", 
            "#DBE9F6", 
            "#BAD4EB", 
            "#87BBDD", 
            "#5A9CCD", 
            "#3079BA", 
            "#185494", 
            "#08306B"
          ], 
          "9": [
            "#F7FBFF", 
            "#DFEBF7", 
            "#C6DBEF", 
            "#9BC4E3", 
            "#6BAED6", 
            "#4C8FC6", 
            "#2171B5", 
            "#164F8F", 
            "#08306B"
          ], 
          "10": [
            "#F7FBFF", 
            "#E1EDF8", 
            "#CBDFF1", 
            "#AACCE7", 
            "#81B8DC", 
            "#5EA0CF", 
            "#4085C0", 
            "#1F69AC", 
            "#144C8B", 
            "#08306B"
          ], 
          "11": [
            "#F7FBFF", 
            "#E4EEF9", 
            "#D0E1F2", 
            "#B5D2EA", 
            "#92C0E0", 
            "#6BAED6", 
            "#5295C9", 
            "#357DBC", 
            "#1D63A6", 
            "#134988", 
            "#08306B"
          ]
        }, 
        "name_en": "High Cirrus Ice Water Path", 
        "id": "Cloud_Seq_CirrusIce"
      }
    ], 
    "folder": "09_Cloud_Cover", 
    "name_en": "Cloud Cover"
  }, 
  {
    "name_ar": "مؤشرات الجفاف والقحولة", 
    "styles": [
      {
        "category": "Multi-Hue", 
        "name_ar": "مؤشر القحولة العالمي المعتمد لأطلس التصحر", 
        "source": "UNEP World Atlas of Desertification (AI = P/PET)", 
        "classes": {
          "3": [
            "#D73027", 
            "#ECF7A5", 
            "#006837"
          ], 
          "4": [
            "#D73027", 
            "#FEE08B", 
            "#A6D96A", 
            "#006837"
          ], 
          "5": [
            "#D73027", 
            "#FEBB6B", 
            "#ECF7A5", 
            "#77C465", 
            "#006837"
          ], 
          "6": [
            "#D73027", 
            "#FCA25B", 
            "#FFF3AA", 
            "#C5E67E", 
            "#5AB65F", 
            "#006837"
          ], 
          "7": [
            "#D73027", 
            "#F98F52", 
            "#FEE08B", 
            "#ECF7A5", 
            "#A6D96A", 
            "#46AA59", 
            "#006837"
          ], 
          "8": [
            "#D73027", 
            "#F7814B", 
            "#FECB79", 
            "#FFFBB8", 
            "#D2EC86", 
            "#8CCD67", 
            "#36A255", 
            "#006837"
          ], 
          "9": [
            "#D73027", 
            "#F57647", 
            "#FEBB6B", 
            "#FFEC9E", 
            "#ECF7A5", 
            "#B9E176", 
            "#77C465", 
            "#289D52", 
            "#006837"
          ], 
          "10": [
            "#D73027", 
            "#F46D43", 
            "#FDAE61", 
            "#FEE08B", 
            "#FFFFBF", 
            "#D9EF8B", 
            "#A6D96A", 
            "#66BD63", 
            "#1A9850", 
            "#006837"
          ], 
          "11": [
            "#D73027", 
            "#F16840", 
            "#FCA25B", 
            "#FED17E", 
            "#FFF3AA", 
            "#ECF7A5", 
            "#C5E67E", 
            "#94D168", 
            "#5AB65F", 
            "#18934D", 
            "#006837"
          ]
        }, 
        "name_en": "UNEP World Aridity Index", 
        "id": "Aridity_UNEP_World"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر الجفاف والتبخر المعياري المتعدد", 
        "source": "Global SPEI Drought Monitor (Vicente-Serrano)", 
        "classes": {
          "3": [
            "#D6604D", 
            "#F7F7F7", 
            "#2166AC"
          ], 
          "4": [
            "#67001F", 
            "#F4A582", 
            "#92C5DE", 
            "#053061"
          ], 
          "5": [
            "#67001F", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#053061"
          ], 
          "6": [
            "#67001F", 
            "#C4413C", 
            "#F4A582", 
            "#92C5DE", 
            "#347CB8", 
            "#053061"
          ], 
          "7": [
            "#67001F", 
            "#C4413C", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#347CB8", 
            "#053061"
          ], 
          "8": [
            "#67001F", 
            "#B2182B", 
            "#D6604D", 
            "#F4A582", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061"
          ], 
          "9": [
            "#67001F", 
            "#B2182B", 
            "#D6604D", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#4393C3", 
            "#2166AC", 
            "#053061"
          ], 
          "10": [
            "#67001F", 
            "#9F1128", 
            "#C4413C", 
            "#DE725A", 
            "#F4A582", 
            "#92C5DE", 
            "#5A9FCA", 
            "#347CB8", 
            "#1A5899", 
            "#053061"
          ], 
          "11": [
            "#67001F", 
            "#9F1128", 
            "#C4413C", 
            "#DE725A", 
            "#F4A582", 
            "#F7F7F7", 
            "#92C5DE", 
            "#5A9FCA", 
            "#347CB8", 
            "#1A5899", 
            "#053061"
          ]
        }, 
        "name_en": "SPEI Drought Severity", 
        "id": "Drought_SPEI_Index"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر بالمر الهيدرولوجي والزراعي لشدة الجفاف", 
        "source": "NOAA National Centers for Environmental Information", 
        "classes": {
          "3": [
            "#E66101", 
            "#FFFFBF", 
            "#542788"
          ], 
          "4": [
            "#730000", 
            "#FDB863", 
            "#B2ABD2", 
            "#2D004B"
          ], 
          "5": [
            "#730000", 
            "#FDB863", 
            "#FFFFBF", 
            "#B2ABD2", 
            "#2D004B"
          ], 
          "6": [
            "#730000", 
            "#D64310", 
            "#FDB863", 
            "#B2ABD2", 
            "#6B4E9A", 
            "#2D004B"
          ], 
          "7": [
            "#730000", 
            "#D64310", 
            "#FDB863", 
            "#FFFFBF", 
            "#B2ABD2", 
            "#6B4E9A", 
            "#2D004B"
          ], 
          "8": [
            "#730000", 
            "#C51B17", 
            "#E66101", 
            "#FDB863", 
            "#B2ABD2", 
            "#8073AC", 
            "#542788", 
            "#2D004B"
          ], 
          "9": [
            "#730000", 
            "#C51B17", 
            "#E66101", 
            "#FDB863", 
            "#FFFFBF", 
            "#B2ABD2", 
            "#8073AC", 
            "#542788", 
            "#2D004B"
          ], 
          "10": [
            "#730000", 
            "#B01412", 
            "#D64310", 
            "#ED7822", 
            "#FDB863", 
            "#B2ABD2", 
            "#8C81B5", 
            "#6B4E9A", 
            "#4A1D78", 
            "#2D004B"
          ], 
          "11": [
            "#730000", 
            "#B01412", 
            "#D64310", 
            "#ED7822", 
            "#FDB863", 
            "#FFFFBF", 
            "#B2ABD2", 
            "#8C81B5", 
            "#6B4E9A", 
            "#4A1D78", 
            "#2D004B"
          ]
        }, 
        "name_en": "Palmer Drought Severity PDSI", 
        "id": "Drought_PDSI_Palmer"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مؤشر استنزاف وعجز رطوبة التربة الجذرية", 
        "source": "European Drought Observatory (EDO / Copernicus)", 
        "classes": {
          "3": [
            "#543005", 
            "#E0E9D4", 
            "#003C30"
          ], 
          "4": [
            "#543005", 
            "#DFC27D", 
            "#80CDC1", 
            "#003C30"
          ], 
          "5": [
            "#543005", 
            "#C89142", 
            "#E0E9D4", 
            "#4AA49B", 
            "#003C30"
          ], 
          "6": [
            "#543005", 
            "#B57726", 
            "#EDD9A7", 
            "#ABDED6", 
            "#2C8D85", 
            "#003C30"
          ], 
          "7": [
            "#543005", 
            "#A5691C", 
            "#DFC27D", 
            "#E0E9D4", 
            "#80CDC1", 
            "#1F7E76", 
            "#003C30"
          ], 
          "8": [
            "#543005", 
            "#9A5E15", 
            "#D2A65B", 
            "#F3E2B9", 
            "#BDE6E0", 
            "#62B6AB", 
            "#14746C", 
            "#003C30"
          ], 
          "9": [
            "#543005", 
            "#92570F", 
            "#C89142", 
            "#E8D097", 
            "#E0E9D4", 
            "#9CD8CE", 
            "#4AA49B", 
            "#0A6C64", 
            "#003C30"
          ], 
          "10": [
            "#543005", 
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F6E8C3", 
            "#C7EAE5", 
            "#80CDC1", 
            "#35978F", 
            "#01665E", 
            "#003C30"
          ], 
          "11": [
            "#543005", 
            "#864E0A", 
            "#B57726", 
            "#D6AE65", 
            "#EDD9A7", 
            "#E0E9D4", 
            "#ABDED6", 
            "#6BBDB2", 
            "#2C8D85", 
            "#016259", 
            "#003C30"
          ]
        }, 
        "name_en": "Soil Moisture Depletion", 
        "id": "Aridity_SoilMoistureDeficit"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "معدل البخر-نتح المرجعي بهارجريفز (ملم/يوم)", 
        "source": "FAO-56 Irrigation and Drainage Guidelines", 
        "classes": {
          "3": [
            "#FFFFB2", 
            "#F7692D", 
            "#7A0000"
          ], 
          "4": [
            "#FFFFB2", 
            "#FEA346", 
            "#DF2C23", 
            "#7A0000"
          ], 
          "5": [
            "#FFFFB2", 
            "#FFBD54", 
            "#F7692D", 
            "#CA1625", 
            "#7A0000"
          ], 
          "6": [
            "#FFFFB2", 
            "#FECC5C", 
            "#FD8D3C", 
            "#F03B20", 
            "#BD0026", 
            "#7A0000"
          ], 
          "7": [
            "#FFFFB2", 
            "#FFD46B", 
            "#FEA346", 
            "#F7692D", 
            "#DF2C23", 
            "#B10020", 
            "#7A0000"
          ], 
          "8": [
            "#FFFFB2", 
            "#FFDA75", 
            "#FFB24E", 
            "#FC8338", 
            "#F24A24", 
            "#D32124", 
            "#A9001C", 
            "#7A0000"
          ], 
          "9": [
            "#FFFFB2", 
            "#FFDF7D", 
            "#FFBD54", 
            "#FE9540", 
            "#F7692D", 
            "#EA3621", 
            "#CA1625", 
            "#A30019", 
            "#7A0000"
          ], 
          "10": [
            "#FFFFB2", 
            "#FFE383", 
            "#FEC558", 
            "#FEA346", 
            "#FB7D35", 
            "#F35126", 
            "#DF2C23", 
            "#C30B26", 
            "#9F0017", 
            "#7A0000"
          ], 
          "11": [
            "#FFFFB2", 
            "#FFE587", 
            "#FECC5C", 
            "#FFAD4C", 
            "#FD8D3C", 
            "#F7692D", 
            "#F03B20", 
            "#D62424", 
            "#BD0026", 
            "#9B0015", 
            "#7A0000"
          ]
        }, 
        "name_en": "Reference Evapotranspiration", 
        "id": "Drought_ETo_Hargreaves"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر الطلب التبخري لرصد الجفاف الوميضي السريع", 
        "source": "NOAA Physical Sciences Laboratory (EDDI)", 
        "classes": {
          "3": [
            "#35978F", 
            "#F5F5F5", 
            "#8C510A"
          ], 
          "4": [
            "#01665E", 
            "#80CDC1", 
            "#DFC27D", 
            "#543005"
          ], 
          "5": [
            "#01665E", 
            "#80CDC1", 
            "#F5F5F5", 
            "#DFC27D", 
            "#543005"
          ], 
          "6": [
            "#01665E", 
            "#35978F", 
            "#80CDC1", 
            "#DFC27D", 
            "#A5691C", 
            "#543005"
          ], 
          "7": [
            "#01665E", 
            "#35978F", 
            "#80CDC1", 
            "#F5F5F5", 
            "#DFC27D", 
            "#A5691C", 
            "#543005"
          ], 
          "8": [
            "#01665E", 
            "#27867E", 
            "#50A99F", 
            "#80CDC1", 
            "#DFC27D", 
            "#BF812D", 
            "#8C510A", 
            "#543005"
          ], 
          "9": [
            "#01665E", 
            "#27867E", 
            "#50A99F", 
            "#80CDC1", 
            "#F5F5F5", 
            "#DFC27D", 
            "#BF812D", 
            "#8C510A", 
            "#543005"
          ], 
          "10": [
            "#01665E", 
            "#1F7E76", 
            "#35978F", 
            "#5CB2A8", 
            "#80CDC1", 
            "#DFC27D", 
            "#C89142", 
            "#A5691C", 
            "#7E4809", 
            "#543005"
          ], 
          "11": [
            "#01665E", 
            "#1F7E76", 
            "#35978F", 
            "#5CB2A8", 
            "#80CDC1", 
            "#F5F5F5", 
            "#DFC27D", 
            "#C89142", 
            "#A5691C", 
            "#7E4809", 
            "#543005"
          ]
        }, 
        "name_en": "Evaporative Demand Drought EDDI", 
        "id": "Drought_EDDI_Evaporative"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر رطوبة المحاصيل الزراعية الأسبوعي", 
        "source": "USDA / NOAA Joint Agricultural Weather Facility", 
        "classes": {
          "3": [
            "#BF812D", 
            "#F5F5F5", 
            "#80CDC1"
          ], 
          "4": [
            "#8C510A", 
            "#DFC27D", 
            "#C7EAE5", 
            "#01665E"
          ], 
          "5": [
            "#8C510A", 
            "#DFC27D", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#01665E"
          ], 
          "6": [
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#C7EAE5", 
            "#80CDC1", 
            "#01665E"
          ], 
          "7": [
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#80CDC1", 
            "#01665E"
          ], 
          "8": [
            "#8C510A", 
            "#AE7122", 
            "#CB9648", 
            "#DFC27D", 
            "#C7EAE5", 
            "#99D7CD", 
            "#5BA99F", 
            "#01665E"
          ], 
          "9": [
            "#8C510A", 
            "#AE7122", 
            "#CB9648", 
            "#DFC27D", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#99D7CD", 
            "#5BA99F", 
            "#01665E"
          ], 
          "10": [
            "#8C510A", 
            "#A5691C", 
            "#BF812D", 
            "#D0A155", 
            "#DFC27D", 
            "#C7EAE5", 
            "#A4DCD3", 
            "#80CDC1", 
            "#49988E", 
            "#01665E"
          ], 
          "11": [
            "#8C510A", 
            "#A5691C", 
            "#BF812D", 
            "#D0A155", 
            "#DFC27D", 
            "#F5F5F5", 
            "#C7EAE5", 
            "#A4DCD3", 
            "#80CDC1", 
            "#49988E", 
            "#01665E"
          ]
        }, 
        "name_en": "Crop Moisture Index CMI", 
        "id": "Drought_CMI_CropMoisture"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "عجز البخر-نتح الفعلي عن المرجعي للمحاصيل", 
        "source": "USGS FEWS NET Water Balance Evapotranspiration", 
        "classes": {
          "3": [
            "#FFFFD4", 
            "#EC7C1C", 
            "#542788"
          ], 
          "4": [
            "#FFFFD4", 
            "#FFAF4E", 
            "#C3500A", 
            "#542788"
          ], 
          "5": [
            "#FFFFD4", 
            "#FFC976", 
            "#EC7C1C", 
            "#A93F06", 
            "#542788"
          ], 
          "6": [
            "#FFFFD4", 
            "#FED98E", 
            "#FE9929", 
            "#D95F0E", 
            "#993404", 
            "#542788"
          ], 
          "7": [
            "#FFFFD4", 
            "#FFDF9A", 
            "#FFAF4E", 
            "#EC7C1C", 
            "#C3500A", 
            "#933022", 
            "#542788"
          ], 
          "8": [
            "#FFFFD4", 
            "#FFE4A2", 
            "#FFBE65", 
            "#F99125", 
            "#DE6812", 
            "#B44607", 
            "#8D2E32", 
            "#542788"
          ], 
          "9": [
            "#FFFFD4", 
            "#FFE7A8", 
            "#FFC976", 
            "#FFA138", 
            "#EC7C1C", 
            "#D15A0C", 
            "#A93F06", 
            "#892C3D", 
            "#542788"
          ], 
          "10": [
            "#FFFFD4", 
            "#FFEAAD", 
            "#FFD283", 
            "#FFAF4E", 
            "#F68C23", 
            "#E16C14", 
            "#C3500A", 
            "#A03905", 
            "#852B45", 
            "#542788"
          ], 
          "11": [
            "#FFFFD4", 
            "#FFECB1", 
            "#FED98E", 
            "#FFB95E", 
            "#FE9929", 
            "#EC7C1C", 
            "#D95F0E", 
            "#B94908", 
            "#993404", 
            "#822B4C", 
            "#542788"
          ]
        }, 
        "name_en": "Actual ET Deficit Index", 
        "id": "Drought_ETa_ActualDeficit"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "مؤشر اختلاف المياه المعياري للغطاء النباتي والتربة", 
        "source": "Gao (1996) Remote Sensing Water Index", 
        "classes": {
          "3": [
            "#DFC27D", 
            "#F5F5F5", 
            "#01665E"
          ], 
          "4": [
            "#8C510A", 
            "#DFC27D", 
            "#80CDC1", 
            "#003C30"
          ], 
          "5": [
            "#8C510A", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#003C30"
          ], 
          "6": [
            "#8C510A", 
            "#B78845", 
            "#DFC27D", 
            "#80CDC1", 
            "#01665E", 
            "#003C30"
          ], 
          "7": [
            "#8C510A", 
            "#B78845", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#01665E", 
            "#003C30"
          ], 
          "8": [
            "#8C510A", 
            "#A97532", 
            "#C49B57", 
            "#DFC27D", 
            "#80CDC1", 
            "#36877E", 
            "#01584E", 
            "#003C30"
          ], 
          "9": [
            "#8C510A", 
            "#A97532", 
            "#C49B57", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#36877E", 
            "#01584E", 
            "#003C30"
          ], 
          "10": [
            "#8C510A", 
            "#A26C29", 
            "#B78845", 
            "#CBA560", 
            "#DFC27D", 
            "#80CDC1", 
            "#49988E", 
            "#01665E", 
            "#015146", 
            "#003C30"
          ], 
          "11": [
            "#8C510A", 
            "#A26C29", 
            "#B78845", 
            "#CBA560", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#49988E", 
            "#01665E", 
            "#015146", 
            "#003C30"
          ]
        }, 
        "name_en": "Normalized Difference Water NDWI", 
        "id": "Drought_NDWI_WaterIndex"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "زحف الكثبان الرملية وتدهور أطراف الواحات", 
        "source": "UNCCD Global Land Outlook / Sahara Encroachment", 
        "classes": {
          "3": [
            "#8C510A", 
            "#E0D0B0", 
            "#0868AC"
          ], 
          "4": [
            "#8C510A", 
            "#DFC27D", 
            "#A8DDB5", 
            "#0868AC"
          ], 
          "5": [
            "#8C510A", 
            "#D0A155", 
            "#E0D0B0", 
            "#7EBFC0", 
            "#0868AC"
          ], 
          "6": [
            "#8C510A", 
            "#C68E3E", 
            "#E0C891", 
            "#C0D8B3", 
            "#5FADC6", 
            "#0868AC"
          ], 
          "7": [
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#E0D0B0", 
            "#A8DDB5", 
            "#43A2CA", 
            "#0868AC"
          ], 
          "8": [
            "#8C510A", 
            "#B87A28", 
            "#D7AF66", 
            "#E0CA9A", 
            "#CAD6B2", 
            "#91CCBC", 
            "#3D99C6", 
            "#0868AC"
          ], 
          "9": [
            "#8C510A", 
            "#B27525", 
            "#D0A155", 
            "#E0C58A", 
            "#E0D0B0", 
            "#B7DAB4", 
            "#7EBFC0", 
            "#3993C3", 
            "#0868AC"
          ], 
          "10": [
            "#8C510A", 
            "#AE7122", 
            "#CB9648", 
            "#DFC27D", 
            "#E0CB9F", 
            "#CFD5B2", 
            "#A8DDB5", 
            "#6EB5C4", 
            "#358EC0", 
            "#0868AC"
          ], 
          "11": [
            "#8C510A", 
            "#AA6D20", 
            "#C68E3E", 
            "#D9B56D", 
            "#E0C891", 
            "#E0D0B0", 
            "#C0D8B3", 
            "#98D1BA", 
            "#5FADC6", 
            "#328ABE", 
            "#0868AC"
          ]
        }, 
        "name_en": "Desert Biome Encroachment", 
        "id": "Drought_Multi_DesertBoundaries"
      }
    ], 
    "folder": "10_Drought_And_Aridity", 
    "name_en": "Drought and Aridity"
  }, 
  {
    "name_ar": "نماذج التغير المناخي والسيناريوهات", 
    "styles": [
      {
        "category": "Diverging", 
        "name_ar": "خطوط الاحترار العالمي لجامعة ريدينج (1850-2025)", 
        "source": "Prof. Ed Hawkins / University of Reading (Warming Stripes)", 
        "classes": {
          "3": [
            "#6BAED6", 
            "#F7F7F7", 
            "#CB181D"
          ], 
          "4": [
            "#08306B", 
            "#BDD7E7", 
            "#FCAE91", 
            "#67000D"
          ], 
          "5": [
            "#08306B", 
            "#BDD7E7", 
            "#F7F7F7", 
            "#FCAE91", 
            "#67000D"
          ], 
          "6": [
            "#08306B", 
            "#4C8FC6", 
            "#BDD7E7", 
            "#FCAE91", 
            "#E34733", 
            "#67000D"
          ], 
          "7": [
            "#08306B", 
            "#4C8FC6", 
            "#BDD7E7", 
            "#F7F7F7", 
            "#FCAE91", 
            "#E34733", 
            "#67000D"
          ], 
          "8": [
            "#08306B", 
            "#2171B5", 
            "#6BAED6", 
            "#BDD7E7", 
            "#FCAE91", 
            "#FB6A4A", 
            "#CB181D", 
            "#67000D"
          ], 
          "9": [
            "#08306B", 
            "#2171B5", 
            "#6BAED6", 
            "#BDD7E7", 
            "#F7F7F7", 
            "#FCAE91", 
            "#FB6A4A", 
            "#CB181D", 
            "#67000D"
          ], 
          "10": [
            "#08306B", 
            "#1C60A2", 
            "#4C8FC6", 
            "#82B8DA", 
            "#BDD7E7", 
            "#FCAE91", 
            "#FD7C5B", 
            "#E34733", 
            "#B11119", 
            "#67000D"
          ], 
          "11": [
            "#08306B", 
            "#1C60A2", 
            "#4C8FC6", 
            "#82B8DA", 
            "#BDD7E7", 
            "#F7F7F7", 
            "#FCAE91", 
            "#FD7C5B", 
            "#E34733", 
            "#B11119", 
            "#67000D"
          ]
        }, 
        "name_en": "Ed Hawkins Warming Stripes", 
        "id": "Model_Div_WarmingStripes"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ درجات الحرارة المتوقعة لنماذج CMIP6 المناخية", 
        "source": "World Climate Research Programme (WCRP / CMIP6)", 
        "classes": {
          "3": [
            "#4393C3", 
            "#FFFFE5", 
            "#F46D43"
          ], 
          "4": [
            "#053061", 
            "#92C5DE", 
            "#FEE090", 
            "#A50026"
          ], 
          "5": [
            "#053061", 
            "#92C5DE", 
            "#FFFFE5", 
            "#FEE090", 
            "#A50026"
          ], 
          "6": [
            "#053061", 
            "#347CB8", 
            "#92C5DE", 
            "#FEE090", 
            "#F46D43", 
            "#A50026"
          ], 
          "7": [
            "#053061", 
            "#347CB8", 
            "#92C5DE", 
            "#FFFFE5", 
            "#FEE090", 
            "#F46D43", 
            "#A50026"
          ], 
          "8": [
            "#053061", 
            "#2166AC", 
            "#4393C3", 
            "#92C5DE", 
            "#FEE090", 
            "#FB9957", 
            "#E14730", 
            "#A50026"
          ], 
          "9": [
            "#053061", 
            "#2166AC", 
            "#4393C3", 
            "#92C5DE", 
            "#FFFFE5", 
            "#FEE090", 
            "#FB9957", 
            "#E14730", 
            "#A50026"
          ], 
          "10": [
            "#053061", 
            "#1A5899", 
            "#347CB8", 
            "#5A9FCA", 
            "#92C5DE", 
            "#FEE090", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027", 
            "#A50026"
          ], 
          "11": [
            "#053061", 
            "#1A5899", 
            "#347CB8", 
            "#5A9FCA", 
            "#92C5DE", 
            "#FFFFE5", 
            "#FEE090", 
            "#FDAE61", 
            "#F46D43", 
            "#D73027", 
            "#A50026"
          ]
        }, 
        "name_en": "CMIP6 Temperature Anomaly", 
        "id": "Model_Div_TempAnomaly"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "نسبة التغير المتوقعة في الأمطار المستقبلية (%)", 
        "source": "IPCC Working Group I Interactive Atlas", 
        "classes": {
          "3": [
            "#BF812D", 
            "#F5F5F5", 
            "#01665E"
          ], 
          "4": [
            "#543005", 
            "#DFC27D", 
            "#80CDC1", 
            "#003C30"
          ], 
          "5": [
            "#543005", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#003C30"
          ], 
          "6": [
            "#543005", 
            "#A5691C", 
            "#DFC27D", 
            "#80CDC1", 
            "#1F7E76", 
            "#003C30"
          ], 
          "7": [
            "#543005", 
            "#A5691C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#1F7E76", 
            "#003C30"
          ], 
          "8": [
            "#543005", 
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#80CDC1", 
            "#35978F", 
            "#01665E", 
            "#003C30"
          ], 
          "9": [
            "#543005", 
            "#8C510A", 
            "#BF812D", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#35978F", 
            "#01665E", 
            "#003C30"
          ], 
          "10": [
            "#543005", 
            "#7E4809", 
            "#A5691C", 
            "#C89142", 
            "#DFC27D", 
            "#80CDC1", 
            "#4AA49B", 
            "#1F7E76", 
            "#015B52", 
            "#003C30"
          ], 
          "11": [
            "#543005", 
            "#7E4809", 
            "#A5691C", 
            "#C89142", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#4AA49B", 
            "#1F7E76", 
            "#015B52", 
            "#003C30"
          ]
        }, 
        "name_en": "CMIP6 Precipitation % Change", 
        "id": "Model_Div_PrecipChange"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "سيناريوهات مسارات التطور المشتركة (SSP1 إلى SSP5)", 
        "source": "IPCC AR6 Cross-Working Group Scenario Palette", 
        "classes": {
          "3": [
            "#005A32", 
            "#FED976", 
            "#7F0000"
          ], 
          "4": [
            "#005A32", 
            "#74C476", 
            "#FD8D3C", 
            "#7F0000"
          ], 
          "5": [
            "#005A32", 
            "#4FA75D", 
            "#FED976", 
            "#F15F2B", 
            "#7F0000"
          ], 
          "6": [
            "#005A32", 
            "#36964E", 
            "#B0CD76", 
            "#FFAC53", 
            "#E93D22", 
            "#7F0000"
          ], 
          "7": [
            "#005A32", 
            "#238B45", 
            "#74C476", 
            "#FED976", 
            "#FD8D3C", 
            "#E31A1C", 
            "#7F0000"
          ], 
          "8": [
            "#005A32", 
            "#1F8442", 
            "#5FB368", 
            "#C7D176", 
            "#FFB95D", 
            "#F77432", 
            "#D41618", 
            "#7F0000"
          ], 
          "9": [
            "#005A32", 
            "#1B7E40", 
            "#4FA75D", 
            "#9BCA76", 
            "#FED976", 
            "#FFA14A", 
            "#F15F2B", 
            "#C91315", 
            "#7F0000"
          ], 
          "10": [
            "#005A32", 
            "#187A3F", 
            "#419E55", 
            "#74C476", 
            "#D4D376", 
            "#FFC062", 
            "#FD8D3C", 
            "#ED4D26", 
            "#C01013", 
            "#7F0000"
          ], 
          "11": [
            "#005A32", 
            "#16773D", 
            "#36964E", 
            "#65B86C", 
            "#B0CD76", 
            "#FED976", 
            "#FFAC53", 
            "#F97B35", 
            "#E93D22", 
            "#BA0F11", 
            "#7F0000"
          ]
        }, 
        "name_en": "IPCC Shared Socioeconomic SSPs", 
        "id": "Model_Multi_SSPSenarios"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "مؤشر تكرار وشدة الظواهر المناخية المتطرفة", 
        "source": "WMO Commission for Climatology / ETCCDI", 
        "classes": {
          "3": [
            "#FFFFCC", 
            "#FD7033", 
            "#490000"
          ], 
          "4": [
            "#FFFFCC", 
            "#FEA647", 
            "#D22528", 
            "#490000"
          ], 
          "5": [
            "#FFFFCC", 
            "#FEBC57", 
            "#FD7033", 
            "#A70020", 
            "#490000"
          ], 
          "6": [
            "#FFFFCC", 
            "#FFC965", 
            "#FD953F", 
            "#EF432A", 
            "#880017", 
            "#490000"
          ], 
          "7": [
            "#FFFFCC", 
            "#FED36F", 
            "#FEA647", 
            "#FD7033", 
            "#D22528", 
            "#750012", 
            "#490000"
          ], 
          "8": [
            "#FFFFCC", 
            "#FED976", 
            "#FEB24C", 
            "#FD8D3C", 
            "#FC4E2A", 
            "#BD0026", 
            "#67000D", 
            "#490000"
          ], 
          "9": [
            "#FFFFCC", 
            "#FFDE81", 
            "#FEBC57", 
            "#FE9B42", 
            "#FD7033", 
            "#E43829", 
            "#A70020", 
            "#63000C", 
            "#490000"
          ], 
          "10": [
            "#FFFFCC", 
            "#FFE189", 
            "#FFC35F", 
            "#FEA647", 
            "#FD873A", 
            "#FC562C", 
            "#D22528", 
            "#96001B", 
            "#60000B", 
            "#490000"
          ], 
          "11": [
            "#FFFFCC", 
            "#FFE490", 
            "#FFC965", 
            "#FEAE4A", 
            "#FD953F", 
            "#FD7033", 
            "#EF432A", 
            "#C30F27", 
            "#880017", 
            "#5E000A", 
            "#490000"
          ]
        }, 
        "name_en": "Climate Extremes ETCCDI", 
        "id": "Model_Multi_ExtremesIndex"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "الزيادة المتوقعة في عدد الليالي الاستوائية الحارة", 
        "source": "CMIP6 Future Extreme Temperature Projections", 
        "classes": {
          "3": [
            "#FFF7BC", 
            "#F5851F", 
            "#662506"
          ], 
          "4": [
            "#FFF7BC", 
            "#FFB643", 
            "#D75807", 
            "#662506"
          ], 
          "5": [
            "#FFF7BC", 
            "#FFCC60", 
            "#F5851F", 
            "#BF4603", 
            "#662506"
          ], 
          "6": [
            "#FFF7BC", 
            "#FFD777", 
            "#FEA231", 
            "#E66910", 
            "#AD3D04", 
            "#662506"
          ], 
          "7": [
            "#FFF7BC", 
            "#FFDE86", 
            "#FFB643", 
            "#F5851F", 
            "#D75807", 
            "#A13804", 
            "#662506"
          ], 
          "8": [
            "#FFF7BC", 
            "#FEE391", 
            "#FEC44F", 
            "#FE9929", 
            "#EC7014", 
            "#CC4C02", 
            "#993404", 
            "#662506"
          ], 
          "9": [
            "#FFF7BC", 
            "#FEE596", 
            "#FFCC60", 
            "#FFA938", 
            "#F5851F", 
            "#E0630D", 
            "#BF4603", 
            "#923205", 
            "#662506"
          ], 
          "10": [
            "#FFF7BC", 
            "#FEE79B", 
            "#FFD26D", 
            "#FFB643", 
            "#FC9527", 
            "#EE7516", 
            "#D75807", 
            "#B54103", 
            "#8D3105", 
            "#662506"
          ], 
          "11": [
            "#FFF7BC", 
            "#FFE99E", 
            "#FFD777", 
            "#FEC04B", 
            "#FEA231", 
            "#F5851F", 
            "#E66910", 
            "#CF5003", 
            "#AD3D04", 
            "#892F05", 
            "#662506"
          ]
        }, 
        "name_en": "Projected Tropical Nights TR20", 
        "id": "Model_Seq_TropicalNightsTR20"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "أيام الجفاف المتتالية واتساع الفترات الجافة", 
        "source": "IPCC AR6 Drought Projections Index", 
        "classes": {
          "3": [
            "#FFFFD4", 
            "#EC7C1C", 
            "#542788"
          ], 
          "4": [
            "#FFFFD4", 
            "#FFAF4E", 
            "#C3500A", 
            "#542788"
          ], 
          "5": [
            "#FFFFD4", 
            "#FFC976", 
            "#EC7C1C", 
            "#A93F06", 
            "#542788"
          ], 
          "6": [
            "#FFFFD4", 
            "#FED98E", 
            "#FE9929", 
            "#D95F0E", 
            "#993404", 
            "#542788"
          ], 
          "7": [
            "#FFFFD4", 
            "#FFDF9A", 
            "#FFAF4E", 
            "#EC7C1C", 
            "#C3500A", 
            "#933022", 
            "#542788"
          ], 
          "8": [
            "#FFFFD4", 
            "#FFE4A2", 
            "#FFBE65", 
            "#F99125", 
            "#DE6812", 
            "#B44607", 
            "#8D2E32", 
            "#542788"
          ], 
          "9": [
            "#FFFFD4", 
            "#FFE7A8", 
            "#FFC976", 
            "#FFA138", 
            "#EC7C1C", 
            "#D15A0C", 
            "#A93F06", 
            "#892C3D", 
            "#542788"
          ], 
          "10": [
            "#FFFFD4", 
            "#FFEAAD", 
            "#FFD283", 
            "#FFAF4E", 
            "#F68C23", 
            "#E16C14", 
            "#C3500A", 
            "#A03905", 
            "#852B45", 
            "#542788"
          ], 
          "11": [
            "#FFFFD4", 
            "#FFECB1", 
            "#FED98E", 
            "#FFB95E", 
            "#FE9929", 
            "#EC7C1C", 
            "#D95F0E", 
            "#B94908", 
            "#993404", 
            "#822B4C", 
            "#542788"
          ]
        }, 
        "name_en": "Consecutive Dry Days CDD", 
        "id": "Model_Seq_ConsecutiveDryDays"
      }, 
      {
        "category": "Diverging", 
        "name_ar": "شذوذ الأيام شديدة المطر والأمطار الغزيرة القصوى", 
        "source": "WMO ETCCDI Extreme Precipitation Indices", 
        "classes": {
          "3": [
            "#DFC27D", 
            "#F5F5F5", 
            "#018571"
          ], 
          "4": [
            "#A6611A", 
            "#DFC27D", 
            "#80CDC1", 
            "#003C30"
          ], 
          "5": [
            "#A6611A", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#003C30"
          ], 
          "6": [
            "#A6611A", 
            "#C4914C", 
            "#DFC27D", 
            "#80CDC1", 
            "#018571", 
            "#003C30"
          ], 
          "7": [
            "#A6611A", 
            "#C4914C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#018571", 
            "#003C30"
          ], 
          "8": [
            "#A6611A", 
            "#BA813B", 
            "#CDA15C", 
            "#DFC27D", 
            "#80CDC1", 
            "#3C9D8B", 
            "#016C5A", 
            "#003C30"
          ], 
          "9": [
            "#A6611A", 
            "#BA813B", 
            "#CDA15C", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#3C9D8B", 
            "#016C5A", 
            "#003C30"
          ], 
          "10": [
            "#A6611A", 
            "#B57933", 
            "#C4914C", 
            "#D2A964", 
            "#DFC27D", 
            "#80CDC1", 
            "#4EA898", 
            "#018571", 
            "#005F4F", 
            "#003C30"
          ], 
          "11": [
            "#A6611A", 
            "#B57933", 
            "#C4914C", 
            "#D2A964", 
            "#DFC27D", 
            "#F5F5F5", 
            "#80CDC1", 
            "#4EA898", 
            "#018571", 
            "#005F4F", 
            "#003C30"
          ]
        }, 
        "name_en": "Very Wet Days R95p Index", 
        "id": "Model_Div_ExtremePrecipR95p"
      }, 
      {
        "category": "Sequential", 
        "name_ar": "تحول أيام درجات التدفئة والتبريد لاستهلاك الطاقة", 
        "source": "Energy Climatology Heating & Cooling Degree Days", 
        "classes": {
          "3": [
            "#EFF3FF", 
            "#3182BD", 
            "#BD0026"
          ], 
          "4": [
            "#EFF3FF", 
            "#6BAED6", 
            "#08519C", 
            "#BD0026"
          ], 
          "5": [
            "#EFF3FF", 
            "#96C2DF", 
            "#3182BD", 
            "#A95367", 
            "#BD0026"
          ], 
          "6": [
            "#EFF3FF", 
            "#AECFE4", 
            "#569CCC", 
            "#1E64A9", 
            "#DC5245", 
            "#BD0026"
          ], 
          "7": [
            "#EFF3FF", 
            "#BDD7E7", 
            "#6BAED6", 
            "#3182BD", 
            "#08519C", 
            "#FC4E2A", 
            "#BD0026"
          ], 
          "8": [
            "#EFF3FF", 
            "#C4DBEA", 
            "#85BADB", 
            "#4D95C8", 
            "#246DAF", 
            "#7E537E", 
            "#F3462A", 
            "#BD0026"
          ], 
          "9": [
            "#EFF3FF", 
            "#CADEED", 
            "#96C2DF", 
            "#5EA3D0", 
            "#3182BD", 
            "#175DA4", 
            "#A95367", 
            "#EC4029", 
            "#BD0026"
          ], 
          "10": [
            "#EFF3FF", 
            "#CEE0EF", 
            "#A4C9E1", 
            "#6BAED6", 
            "#4790C5", 
            "#2771B2", 
            "#08519C", 
            "#C65355", 
            "#E73B29", 
            "#BD0026"
          ], 
          "11": [
            "#EFF3FF", 
            "#D1E2F1", 
            "#AECFE4", 
            "#7DB6D9", 
            "#569CCC", 
            "#3182BD", 
            "#1E64A9", 
            "#695387", 
            "#DC5245", 
            "#E33729", 
            "#BD0026"
          ]
        }, 
        "name_en": "Degree Days Heating/Cooling Shift", 
        "id": "Model_Seq_DegreeDays"
      }, 
      {
        "category": "Multi-Hue", 
        "name_ar": "سيناريوهات غمر وارتفاع منسوب البحر الساحلي حتى 2100", 
        "source": "IPCC Special Report on Ocean and Cryosphere (SROCC)", 
        "classes": {
          "3": [
            "#08519C", 
            "#FEE5D9", 
            "#A50F15"
          ], 
          "4": [
            "#08519C", 
            "#A4C9E1", 
            "#FD9879", 
            "#A50F15"
          ], 
          "5": [
            "#08519C", 
            "#6BAED6", 
            "#FEE5D9", 
            "#FB6A4A", 
            "#A50F15"
          ], 
          "6": [
            "#08519C", 
            "#569CCC", 
            "#CBDAE4", 
            "#FDB99F", 
            "#F0543B", 
            "#A50F15"
          ], 
          "7": [
            "#08519C", 
            "#4790C5", 
            "#A4C9E1", 
            "#FEE5D9", 
            "#FD9879", 
            "#E84432", 
            "#A50F15"
          ], 
          "8": [
            "#08519C", 
            "#3B88C1", 
            "#85BADB", 
            "#DADDE1", 
            "#FEC6AF", 
            "#FD7F5E", 
            "#E2382B", 
            "#A50F15"
          ], 
          "9": [
            "#08519C", 
            "#3182BD", 
            "#6BAED6", 
            "#BDD7E7", 
            "#FEE5D9", 
            "#FCAE91", 
            "#FB6A4A", 
            "#DE2D26", 
            "#A50F15"
          ], 
          "10": [
            "#08519C", 
            "#2E7CB9", 
            "#60A4D0", 
            "#A4C9E1", 
            "#E2DFDF", 
            "#FFCDB9", 
            "#FD9879", 
            "#F55E42", 
            "#D82A24", 
            "#A50F15"
          ], 
          "11": [
            "#08519C", 
            "#2B78B6", 
            "#569CCC", 
            "#8EBEDD", 
            "#CBDAE4", 
            "#FEE5D9", 
            "#FDB99F", 
            "#FD8766", 
            "#F0543B", 
            "#D22723", 
            "#A50F15"
          ]
        }, 
        "name_en": "Coastal Sea Level Rise Scenarios", 
        "id": "Model_Multi_SeaLevelRise"
      }
    ], 
    "folder": "11_Climate_Models", 
    "name_en": "Climate Models"
  }
]

CLIMATE_ELEMENTS_STYLES = [{'folder': '01_Temperature', 'name_en': 'Temperature', 'name_ar': 'درجات الحرارة', 'styles': TEMPERATURE_STYLES}] + OTHER_ELEMENTS
print("Mega Climate Styles Configured: 125 Palettes with 9 Class Tiers (3 to 11) across 11 Elements.")

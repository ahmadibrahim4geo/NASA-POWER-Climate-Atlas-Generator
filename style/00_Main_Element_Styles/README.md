# -*- coding: utf-8 -*-
# README — Folder roles (Arabic / English)
# مجلدات الأنماط — أدوار كل مجلد

## 1) style/01_Temperature ... style/11_Climate_Models (11 مجلداً مرقماً)
# - كل مجلد يمثل عنصراً مناخياً رئيسياً.
# - داخله: النمط الرئيسي (Main .style يضم كافة palettes العنصر) + الأنماط الفرعية التابعة + مجلد STYLE/ نسخة مطابقة للنمط الرئيسي.
# - Each element folder holds the Main style (superset of all palettes) + thematic Sub-styles + STYLE/ copy of the Main.

## 2) style/00_Main_Element_Styles/ (جديد — فولدر يجمع الرئيسية مرتبة)
# - يجمع الـ 11 نمطاً رئيسياً فقط (كل واحد يضم الفرعية بداخله) + الماستر، مرتبة من 01 إلى 12.
# - Collects the 11 Main element styles (each embedding its sub-palettes) + Master, ordered 01..12.
# - الحالة بعد التحديث: 29 لوحة حرارية (Temperature) + 129 لوحة إجمالية | الماستر: 2322 Ramp و1419 Color و1419 Fill | كل رئيسي يضم فرعياته بالكامل + Colors/Fills بتسلسل 11 فئة.

## 3) style/ArcMap_Style_Files/ مقابل style/All_ArcMap_Styles_Consolidated/
# - نتيجة الفحص (MD5): ملفات الـ 53 المولدة متطابقة تماماً (SAME) في المجلدين.
# - الفرق الوحيد: All_Consolidated يضم +9 ملفات ESRI رسمية (ESRI, Meteorological, Weather, Environmental, Conservation, Forestry, Military METOC, Soils EURO, Water Wastewater) + وثائق.
# - التوصية: الإبقاء على الاثنين بأدوار متميزة وعدم الحذف:
#   * ArcMap_Style_Files = بيئة العمل (53 ملفاً مولداً فقط).
#   * All_Consolidated = المكتبة الشاملة للتوزيع (53 + 9 رسمية + وثائق).
# - Audit (MD5): the 53 generated files are byte-identical in both folders.
#   Only difference: All_Consolidated adds 9 official ESRI styles + docs.
#   Recommendation: keep both with distinct roles; do NOT delete.

## 4) style/Raw_Climate_Styles/ — ممنوع التعديل/الحذف (مرجع فقط + قالب Meteorological.style للبناء).

## 5) style/Source_of_Style_and_Color/ — المصادر والمراجع اللونية المعتمدة.

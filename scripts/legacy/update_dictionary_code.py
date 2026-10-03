# -*- coding: utf-8 -*-
"""
Update generate_excel_dictionary.py to include the 11 new *_Month_Mean indicators,
then execute it and sync the resulting Excel file to Desktop and D: Drive.
"""

import os
import shutil
import re

DICT_PY = r"d:\My Software\NASA POWER Climate Atlas Generator\generate_excel_dictionary.py"

NEW_ENTRIES = {
    "T_Annual_Mean": '''    {
        "short_name": "T_MonMean",
        "full_name": "T_Month_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الشهري لدرجة حرارة الهواء عند ارتفاع 2 متر (متوسط الـ 12 شهراً المناخي).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط الشهري لدرجة الحرارة (°C)"
    },''',
    "PSL_Annual_Mean": '''    {
        "short_name": "PSL_MonMea",
        "full_name": "PSL_Month_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"المتوسط الشهري للضغط الجوي المصحح عند مستوى سطح البحر القياسي (متوسط الـ 12 شهراً).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المتوسط الشهري لضغط مستوى سطح البحر (hPa)"
    },''',
    "PS_Annual_Mean": '''    {
        "short_name": "PS_MonMean",
        "full_name": "PS_Month_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المتوسط الشهري للضغط الجوي السطحي الفعلي للمحطة (متوسط الـ 12 شهراً).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المتوسط الشهري للضغط الجوي السطحي (hPa)"
    },''',
    "W_Spd_Annual_Mean": '''    {
        "short_name": "WSp_MonMea",
        "full_name": "W_Spd_Month_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح السطحية)",
        "desc_ar": u"المتوسط الشهري لسرعة الرياح على ارتفاع 10 أمتار (متوسط الـ 12 شهراً).",
        "unit": u"m/s",
        "map_title": u"خريطة المتوسط الشهري لسرعة الرياح (m/s)"
    },''',
    "W_Dir_Annual_Mean": '''    {
        "short_name": "WDr_MonMea",
        "full_name": "W_Dir_Month_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح السطحية)",
        "desc_ar": u"المتوسط الشهري لاتجاه الرياح السائدة (المتوسط الدائري للشهور الـ 12).",
        "unit": u"°",
        "map_title": u"خريطة المتوسط الشهري لاتجاه الرياح السائدة (°)"
    },''',
    "RH_Annual_Mean": '''    {
        "short_name": "RH_MonMean",
        "full_name": "RH_Month_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المتوسط الشهري للرطوبة النسبية عند ارتفاع 2 متر (متوسط الـ 12 شهراً).",
        "unit": u"%",
        "map_title": u"خريطة المتوسط الشهري للرطوبة النسبية (%)"
    },''',
    "Td_Annual_Mean": '''    {
        "short_name": "Td_MonMean",
        "full_name": "Td_Month_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (درجة حرارة نقطة الندى)",
        "desc_ar": u"المتوسط الشهري لدرجة حرارة نقطة الندى عند ارتفاع 2 متر (متوسط الـ 12 شهراً).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط الشهري لنقطة الندى (°C)"
    },''',
    "Sol_Annual_Mean": '''    {
        "short_name": "Sol_MonMea",
        "full_name": "Sol_Month_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المتوسط الشهري للإشعاع الشمسي اليومي الساقط على السطح الأفقي (متوسط الـ 12 شهراً).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المتوسط الشهري للإشعاع الشمسي اليومي (kWh/m²/day)"
    },''',
    "UV_Annual_Mean": '''    {
        "short_name": "UV_MonMean",
        "full_name": "UV_Month_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (مؤشر الأشعة فوق البنفسجية)",
        "desc_ar": u"المتوسط الشهري لمؤشر الأشعة فوق البنفسجية في سماء صافية (متوسط الـ 12 شهراً).",
        "unit": u"Index",
        "map_title": u"خريطة المتوسط الشهري لمؤشر الأشعة فوق البنفسجية"
    },''',
    "Cld_Annual_Mean": '''    {
        "short_name": "Cld_MonMea",
        "full_name": "Cld_Month_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المتوسط الشهري لكمية الغطاء السحابي الكلي (متوسط الـ 12 شهراً).",
        "unit": u"%",
        "map_title": u"خريطة المتوسط الشهري للغطاء السحابي (%)"
    },''',
    "ET_Annual_Mean": '''    {
        "short_name": "ET_MonMean",
        "full_name": "ET_Month_Mean",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر-نتح المرجعي)",
        "desc_ar": u"المعدل الشهري للبخر-نتح المرجعي المحسوب بطريقة هارجريفز (متوسط الشهور = المجموع السنوي / 12).",
        "unit": u"mm/month",
        "map_title": u"خريطة المتوسط الشهري للبخر والنتح المرجعي (mm/month)"
    },'''
}

COUNT_REPLACEMENTS = [
    ('"num": "01",\n        "name_en": "01_Temperature",\n        "name_ar": u"درجة الحرارة",\n        "folder": "01_Temperature",\n        "fc": "01_Temperature",\n        "count": 22,',
     '"num": "01",\n        "name_en": "01_Temperature",\n        "name_ar": u"درجة الحرارة",\n        "folder": "01_Temperature",\n        "fc": "01_Temperature",\n        "count": 23,'),
    ('"num": "03",\n        "name_en": "03_Sea_Level_Pressure",\n        "name_ar": u"ضغط مستوى سطح البحر",\n        "folder": "03_Sea_Level_Pressure",\n        "fc": "03_Sea_Level_Pressure",\n        "count": 18,',
     '"num": "03",\n        "name_en": "03_Sea_Level_Pressure",\n        "name_ar": u"ضغط مستوى سطح البحر",\n        "folder": "03_Sea_Level_Pressure",\n        "fc": "03_Sea_Level_Pressure",\n        "count": 19,'),
    ('"num": "04",\n        "name_en": "04_Surface_Pressure",\n        "name_ar": u"الضغط السطحي الفعلي",\n        "folder": "04_Surface_Pressure",\n        "fc": "04_Surface_Pressure",\n        "count": 18,',
     '"num": "04",\n        "name_en": "04_Surface_Pressure",\n        "name_ar": u"الضغط السطحي الفعلي",\n        "folder": "04_Surface_Pressure",\n        "fc": "04_Surface_Pressure",\n        "count": 19,'),
    ('"num": "05",\n        "name_en": "05_Wind",\n        "name_ar": u"الرياح السطحية (سرعة واتجاه)",\n        "folder": "05_Wind",\n        "fc": "05_Wind",\n        "count": 37,',
     '"num": "05",\n        "name_en": "05_Wind",\n        "name_ar": u"الرياح السطحية (سرعة واتجاه)",\n        "folder": "05_Wind",\n        "fc": "05_Wind",\n        "count": 39,'),
    ('"num": "06",\n        "name_en": "06_Relative_Humidity",\n        "name_ar": u"الرطوبة النسبية",\n        "folder": "06_Relative_Humidity",\n        "fc": "06_Relative_Humidity",\n        "count": 18,',
     '"num": "06",\n        "name_en": "06_Relative_Humidity",\n        "name_ar": u"الرطوبة النسبية",\n        "folder": "06_Relative_Humidity",\n        "fc": "06_Relative_Humidity",\n        "count": 19,'),
    ('"num": "07",\n        "name_en": "07_Dew_Point",\n        "name_ar": u"نقطة الندى",\n        "folder": "07_Dew_Point",\n        "fc": "07_Dew_Point",\n        "count": 18,',
     '"num": "07",\n        "name_en": "07_Dew_Point",\n        "name_ar": u"نقطة الندى",\n        "folder": "07_Dew_Point",\n        "fc": "07_Dew_Point",\n        "count": 19,'),
    ('"num": "08",\n        "name_en": "08_Solar_Radiation",\n        "name_ar": u"الإشعاع الشمسي",\n        "folder": "08_Solar_Radiation",\n        "fc": "08_Solar_Radiation",\n        "count": 19,',
     '"num": "08",\n        "name_en": "08_Solar_Radiation",\n        "name_ar": u"الإشعاع الشمسي",\n        "folder": "08_Solar_Radiation",\n        "fc": "08_Solar_Radiation",\n        "count": 20,'),
    ('"num": "09",\n        "name_en": "09_UV_Index",\n        "name_ar": u"مؤشر الأشعة فوق البنفسجية",\n        "folder": "09_UV_Index",\n        "fc": "09_UV_Index",\n        "count": 19,',
     '"num": "09",\n        "name_en": "09_UV_Index",\n        "name_ar": u"مؤشر الأشعة فوق البنفسجية",\n        "folder": "09_UV_Index",\n        "fc": "09_UV_Index",\n        "count": 20,'),
    ('"num": "10",\n        "name_en": "10_Cloud_Cover",\n        "name_ar": u"الغطاء السحابي",\n        "folder": "10_Cloud_Cover",\n        "fc": "10_Cloud_Cover",\n        "count": 19,',
     '"num": "10",\n        "name_en": "10_Cloud_Cover",\n        "name_ar": u"الغطاء السحابي",\n        "folder": "10_Cloud_Cover",\n        "fc": "10_Cloud_Cover",\n        "count": 20,'),
    ('"num": "14",\n        "name_en": "14_Evapotranspiration",\n        "name_ar": u"البخر-نتح المرجعي (ET)",\n        "folder": "14_Evapotranspiration",\n        "fc": "14_Evapotranspiration",\n        "count": 9,',
     '"num": "14",\n        "name_en": "14_Evapotranspiration",\n        "name_ar": u"البخر-نتح المرجعي (ET)",\n        "folder": "14_Evapotranspiration",\n        "fc": "14_Evapotranspiration",\n        "count": 10,'),
]

with open(DICT_PY, "r", encoding="utf-8") as f:
    content = f.read()

for target_fld, entry_code in NEW_ENTRIES.items():
    # Find full_name": target_fld block
    pattern = r'(\{[^\{\}]*?"full_name":\s*"' + target_fld + r'"[^\{\}]*?\},\n)'
    m = re.search(pattern, content)
    if m:
        matched_str = m.group(1)
        # Insert entry right after matched_str
        content = content.replace(matched_str, matched_str + entry_code + "\n")
        print("Inserted entry for %s" % target_fld)
    else:
        print("[WARN] Could not find %s" % target_fld)

for old_s, new_s in COUNT_REPLACEMENTS:
    if old_s in content:
        content = content.replace(old_s, new_s)
        print("Updated module summary count")

with open(DICT_PY, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated %s successfully!" % DICT_PY)

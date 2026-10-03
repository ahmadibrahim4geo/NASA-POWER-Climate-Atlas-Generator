# -*- coding: utf-8 -*-
import io

with io.open("generate_excel_dictionary.py", "r", encoding="utf-8") as f:
    text = f.read()

new_entries = [
    ("T_Annual_Range", """    {
        "short_name": "T_SeaRng",
        "full_name": "T_Seasonal_Range",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجات الحرارة)",
        "desc_ar": u"المدى الفصلي لدرجة الحرارة (الفارق بين أدفأ فصول السنة وأبردها).",
        "unit": u"°C",
        "map_title": u"خريطة المدى الفصلي لدرجة الحرارة (°C)"
    },"""),
    ("PSL_Annual_Range", """    {
        "short_name": "PSL_SeaRng",
        "full_name": "PSL_Seasonal_Range",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"المدى الفصلي لضغط مستوى البحر (الفارق بين أعلى وأدنى فصول السنة ضغطاً).",
        "unit": u"hPa",
        "map_title": u"خريطة المدى الفصلي لضغط مستوى البحر (hPa)"
    },"""),
    ("PS_Annual_Range", """    {
        "short_name": "PS_SeaRng",
        "full_name": "PS_Seasonal_Range",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المدى الفصلي للضغط السطحي (الفارق بين فصول السنة).",
        "unit": u"hPa",
        "map_title": u"خريطة المدى الفصلي للضغط السطحي (hPa)"
    },"""),
    ("W_Spd_Annual_Range", """    {
        "short_name": "WSp_SeaRng",
        "full_name": "W_Spd_Seasonal_Range",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"المدى الفصلي لسرعة الرياح (الفارق بين أشد فصول السنة ريحاً وأهدأها).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة المدى الفصلي لسرعة الرياح (م/ث)"
    },"""),
    ("RH_Annual_Range", """    {
        "short_name": "RH_SeaRng",
        "full_name": "RH_Seasonal_Range",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المدى الفصلي للرطوبة النسبية (الفارق بين أكثر فصول السنة رطوبة وأجفها).",
        "unit": u"%",
        "map_title": u"خريطة المدى الفصلي للرطوبة النسبية (%)"
    },"""),
    ("Td_Annual_Range", """    {
        "short_name": "Td_SeaRng",
        "full_name": "Td_Seasonal_Range",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"المدى الفصلي لنقطة الندى (الفارق بين أعلى وأدنى فصول السنة).",
        "unit": u"°C",
        "map_title": u"خريطة المدى الفصلي لنقطة الندى (°C)"
    },"""),
    ("Sol_Annual_Range", """    {
        "short_name": "Sol_SeaRng",
        "full_name": "Sol_Seasonal_Range",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المدى الفصلي للإشعاع الشمسي اليومي (الفارق بين فصول السنة).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المدى الفصلي للإشعاع الشمسي (kWh/m²/day)"
    },"""),
    ("UV_Annual_Range", """    {
        "short_name": "UV_SeaRng",
        "full_name": "UV_Seasonal_Range",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"المدى الفصلي لمؤشر الأشعة فوق البنفسجية (الفارق بين فصول السنة).",
        "unit": u"مؤشر (Index)",
        "map_title": u"خريطة المدى الفصلي لمؤشر الأشعة فوق البنفسجية"
    },"""),
    ("Cld_Annual_Range", """    {
        "short_name": "Cld_SeaRng",
        "full_name": "Cld_Seasonal_Range",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المدى الفصلي للغطاء السحابي (الفارق بين أعلى فصول السنة غيوماً وأصفاها).",
        "unit": u"%",
        "map_title": u"خريطة المدى الفصلي للغطاء السحابي (%)"
    },"""),
]

for after_name, snippet in new_entries:
    token = '"full_name": "' + after_name + '"'
    pos = text.find(token)
    if pos != -1:
        end_brace = text.find("},", pos)
        if end_brace != -1:
            insert_pos = end_brace + 2
            text = text[:insert_pos] + "\n" + snippet + text[insert_pos:]
            print("Inserted " + after_name + " seasonal range!")

with io.open("generate_excel_dictionary.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated dictionary script.")

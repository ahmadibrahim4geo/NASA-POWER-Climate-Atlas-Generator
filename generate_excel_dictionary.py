# -*- coding: utf-8 -*-
"""
Script to build and format the comprehensive Fields_AR_EN_Units.xlsx
workbook for the NASA POWER Climate Atlas Generator.
"""
from __future__ import print_function
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FIELDS_DATA = [
    # --- 1. الحقول الإدارية والوصفية (Administrative & Metadata Fields) ---
    {
        "short_name": "OBJECTID",
        "full_name": "OBJECTID",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"المعرف الرقمي التسلسلي الفريد للظاهرة في قاعدة البيانات الجغرافية (Geodatabase OID).",
        "unit": "-",
        "map_title": u"-"
    },
    {
        "short_name": "Source_ID",
        "full_name": "Source_ID",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"المعرف الفريد لمحطة الرصد أو النقطة المناخية المصدرية المدخلة في المعالجة.",
        "unit": "-",
        "map_title": u"-"
    },
    {
        "short_name": "Point_Lat",
        "full_name": "Point_Lat",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"دائرة العرض الجغرافية للنقطة بالنظام الإحداثي العالمي WGS 1984 بالدرجات العشرية.",
        "unit": u"درجة (°)",
        "map_title": u"خريطة توزيع دوائر العرض للمحطات"
    },
    {
        "short_name": "Point_Lon",
        "full_name": "Point_Lon",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"خط الطول الجغرافي للنقطة بالنظام الإحداثي العالمي WGS 1984 بالدرجات العشرية.",
        "unit": u"درجة (°)",
        "map_title": u"خريطة توزيع خطوط الطول للمحطات"
    },
    {
        "short_name": "Data_Start",
        "full_name": "Data_Start",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"سنة أو تاريخ بداية السلسلة الزمنية المناخية المسحوبة من وكالة ناسا POWER.",
        "unit": u"سنة / تاريخ",
        "map_title": u"-"
    },
    {
        "short_name": "Data_End",
        "full_name": "Data_End",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"سنة أو تاريخ نهاية السلسلة الزمنية المناخية المسحوبة من وكالة ناسا POWER.",
        "unit": u"سنة / تاريخ",
        "map_title": u"-"
    },
    {
        "short_name": "Temporal",
        "full_name": "Temporal",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"الدقة الزمنية للبيانات المدخلة في المعالجة (Daily يومي / Monthly شهري / Precalc محسوب مسبقاً).",
        "unit": u"نص",
        "map_title": u"-"
    },
    {
        "short_name": "Intrp_Meth",
        "full_name": "Interp_Meth",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"خوارزمية الاستيفاء المكاني المستخدمة في توليد أسطح الراستر (IDW / Kriging / Spline).",
        "unit": u"نص",
        "map_title": u"-"
    },
    {
        "short_name": "Cell_Size",
        "full_name": "Cell_Size",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"حجم ودقة خلية الراستر الناتجة عن الاستيفاء المكاني بوحدات الإسقاط المعتمد.",
        "unit": u"متر / درجات",
        "map_title": u"-"
    },
    {
        "short_name": "Wind_Cell",
        "full_name": "Wind_Cell",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"المسافة التباعدية بين خلايا شبكة متجهات وأسهم اتجاه وسرعة الرياح.",
        "unit": u"متر / درجات",
        "map_title": u"-"
    },
    {
        "short_name": "Status",
        "full_name": "Status",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"حالة إتمام المعالجة الحسابية المناخية للنقطة بنجاح (OK أو FAILED).",
        "unit": u"نص",
        "map_title": u"-"
    },
    {
        "short_name": "Error_Msg",
        "full_name": "Error_Msg",
        "module_code": "00_Admin",
        "module_name": "Admin / بيانات إدارية",
        "desc_ar": u"نص رسالة الخطأ أو التشخيص التحذيري في حال تعثر معالجة بيانات النقطة.",
        "unit": u"نص",
        "map_title": u"-"
    },

    # --- 2. درجات الحرارة (01_Temperature) ---
    {
        "short_name": "T_AnnMean",
        "full_name": "T_Annual_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي السنوي لدرجة حرارة الهواء عند ارتفاع 2 متر لجميع شهور السنة.",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي لدرجة الحرارة (°C)"
    },
    {
        "short_name": "T_WinMean",
        "full_name": "T_Winter_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة حرارة الهواء لفصل الشتاء الأرصادي (شهور ديسمبر، يناير، فبراير - DJF).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة خلال فصل الشتاء (°C)"
    },
    {
        "short_name": "T_SprMean",
        "full_name": "T_Spring_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة حرارة الهواء لفصل الربيع الأرصادي (شهور مارس، أبريل، مايو - MAM).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة خلال فصل الربيع (°C)"
    },
    {
        "short_name": "T_SumMean",
        "full_name": "T_Summer_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة حرارة الهواء لفصل الصيف الأرصادي (شهور يونيو، يوليو، أغسطس - JJA).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة خلال فصل الصيف (°C)"
    },
    {
        "short_name": "T_AutMean",
        "full_name": "T_Autumn_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة حرارة الهواء لفصل الخريف الأرصادي (شهور سبتمبر، أكتوبر، نوفمبر - SON).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة خلال فصل الخريف (°C)"
    },
    {
        "short_name": "T_AnnRng",
        "full_name": "T_Annual_Range",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المدى الحراري السنوي (الفارق بين متوسط أدفأ شهور السنة ومتوسط أبرد شهور السنة).",
        "unit": u"°C",
        "map_title": u"خريطة المدى الحراري السنوي لدرجات الحرارة (°C)"
    },
    {
        "short_name": "T_MaxSumMo",
        "full_name": "T_Max_Summer_Month_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة الحرارة لأدفأ شهور فصل الصيف (أعلى متوسط شهري مسجل في الصيف).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط أدفأ شهور فصل الصيف (°C)"
    },
    {
        "short_name": "T_MinWinMo",
        "full_name": "T_Min_Winter_Month_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"متوسط درجة الحرارة لأبرد شهور فصل الشتاء (أدنى متوسط شهري مسجل في الشتاء).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط أبرد شهور فصل الشتاء (°C)"
    },
    {
        "short_name": "T_MaxMean",
        "full_name": "T_Annual_Max_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط السنوي للنهايات العظمى اليومية لدرجة حرارة الهواء (T2M_MAX).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي للنهايات العظمى لدرجة الحرارة (°C)"
    },
    {
        "short_name": "T_MinMean",
        "full_name": "T_Annual_Min_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط السنوي للنهايات الصغرى اليومية لدرجة حرارة الهواء (T2M_MIN).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي للنهايات الصغرى لدرجة الحرارة (°C)"
    },

    # --- 3. مؤشر الحرارة والراحة البيومناخية (11_Heat_Index) ---
    {
        "short_name": "HI_AnnMean",
        "full_name": "HI_Annual_Mean",
        "module_code": "11_Heat_Index",
        "module_name": "11_Heat_Index (مؤشر الحرارة)",
        "desc_ar": u"المتوسط السنوي لمؤشر الحرارة المحسوسة المحسوب بمعادلة روتفوش وستيدمان للحرارة والرطوبة.",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي لمؤشر الحرارة المحسوسة (°C)"
    },
    {
        "short_name": "HI_SumMean",
        "full_name": "HI_Summer_Mean",
        "module_code": "11_Heat_Index",
        "module_name": "11_Heat_Index (مؤشر الحرارة)",
        "desc_ar": u"متوسط مؤشر الحرارة المحسوسة خلال فصل الصيف (مقياس الإجهاد الحراري الفعلي).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط مؤشر الحرارة المحسوسة خلال فصل الصيف (°C)"
    },
    {
        "short_name": "HI_WinMean",
        "full_name": "HI_Winter_Mean",
        "module_code": "11_Heat_Index",
        "module_name": "11_Heat_Index (مؤشر الحرارة)",
        "desc_ar": u"متوسط مؤشر الحرارة الظاهرية/الهيوميدكس خلال فصل الشتاء في الأجواء الباردة والرطبة.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة المحسوسة خلال فصل الشتاء (°C)"
    },
    {
        "short_name": "HI_AnRng",
        "full_name": "HI_Annual_Range",
        "module_code": "11_Heat_Index",
        "module_name": "11_Heat_Index (مؤشر الحرارة)",
        "desc_ar": u"المدى السنوي لمؤشر الحرارة المحسوسة (الفارق بين أعلى شهر إجهاد حراري وأدنى شهر).",
        "unit": u"°C",
        "map_title": u"خريطة المدى السنوي لمؤشر الحرارة المحسوسة (°C)"
    },
    {
        "short_name": "WBGT_SuMn",
        "full_name": "WBGT_Summer_Mean",
        "module_code": "11_Heat_Index",
        "module_name": "11_Heat_Index (مؤشر الحرارة)",
        "desc_ar": u"متوسط درجة حرارة البصيلة الرطبة الكروية الصيفي في الظل (معيار ISO 7243 للإجهاد المهني والرياضي).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط مؤشر الإجهاد الحراري الصيفي (WBGT) (°C)"
    },

    # --- 4. نقطة الندى (07_Dew_Point) ---
    {
        "short_name": "Td_AnnMean",
        "full_name": "Td_Annual_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"المتوسط الحسابي السنوي لدرجة حرارة نقطة الندى عند ارتفاع 2 متر.",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي لدرجة حرارة نقطة الندى (°C)"
    },
    {
        "short_name": "Td_WinMean",
        "full_name": "Td_Winter_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى خلال فصل الشتاء الأرصادي (DJF).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى خلال فصل الشتاء (°C)"
    },
    {
        "short_name": "Td_SprMean",
        "full_name": "Td_Spring_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى خلال فصل الربيع الأرصادي (MAM).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى خلال فصل الربيع (°C)"
    },
    {
        "short_name": "Td_SumMean",
        "full_name": "Td_Summer_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى خلال فصل الصيف الأرصادي (JJA - مؤشر مباشر للرطوبة الخانقة والكتمة).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى خلال فصل الصيف (°C)"
    },
    {
        "short_name": "Td_AutMean",
        "full_name": "Td_Autumn_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى خلال فصل الخريف الأرصادي (SON).",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى خلال فصل الخريف (°C)"
    },
    {
        "short_name": "Td_AnnRng",
        "full_name": "Td_Annual_Range",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"المدى السنوي لدرجة حرارة نقطة الندى (الفارق بين أعلى وأدنى متوسط شهري لنقطة الندى).",
        "unit": u"°C",
        "map_title": u"خريطة المدى السنوي لدرجة حرارة نقطة الندى (°C)"
    },

    # --- 5. التساقط والأمطار (02_Precipitation) ---
    {
        "short_name": "R_AnnMean",
        "full_name": "R_Annual_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المتوسط السنوي لتساقط الأمطار (متوسط مجاميع السنين على مدار فترة الرصد 1996–2025).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المتوسط السنوي لتساقط الأمطار (ملم)"
    },
    {
        "short_name": "R_MonMean",
        "full_name": "R_Month_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المتوسط الشهري لتساقط الأمطار (المتوسط السنوي مقسوماً على 12 شهراً).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المتوسط الشهري لتساقط الأمطار (ملم)"
    },
    {
        "short_name": "R_AnnRng",
        "full_name": "R_Annual_Range",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المدى السنوي لتساقط الأمطار (الفارق بين أعلى شهر مطراً وأقل شهر مطراً في السنة).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المدى السنوي لتساقط الأمطار (ملم)"
    },
    {
        "short_name": "R_SeaRng",
        "full_name": "R_Seasonal_Range",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المدى الفصلي لتساقط الأمطار (الفارق بين مجموع أعلى فصول السنة مطراً ومجموع أقلها مطراً).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المدى الفصلي لتساقط الأمطار (ملم)"
    },
    {
        "short_name": "R_WinTot",
        "full_name": "R_Winter_Total",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المجموع التراكمي لأمطار فصل الشتاء الأرصادي (شهور ديسمبر، يناير، فبراير - DJF).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع تساقط الأمطار خلال فصل الشتاء (ملم)"
    },
    {
        "short_name": "R_SprTot",
        "full_name": "R_Spring_Total",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المجموع التراكمي لأمطار فصل الربيع الأرصادي (شهور مارس، أبريل، مايو - MAM).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع تساقط الأمطار خلال فصل الربيع (ملم)"
    },
    {
        "short_name": "R_SumTot",
        "full_name": "R_Summer_Total",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المجموع التراكمي لأمطار فصل الصيف الأرصادي (شهور يونيو، يوليو، أغسطس - JJA).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع تساقط الأمطار خلال فصل الصيف (ملم)"
    },
    {
        "short_name": "R_AutTot",
        "full_name": "R_Autumn_Total",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"المجموع التراكمي لأمطار فصل الخريف الأرصادي (شهور سبتمبر، أكتوبر، نوفمبر - SON).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع تساقط الأمطار خلال فصل الخريف (ملم)"
    },

    # --- 6. ضغط مستوى سطح البحر (03_Sea_Level_Pressure) ---
    {
        "short_name": "PSL_AnMean",
        "full_name": "PSL_Annual_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي السنوي المصحح عند مستوى سطح البحر القياسي (Sea Level Pressure).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط الجوي عند مستوى سطح البحر (hPa)"
    },
    {
        "short_name": "PSL_WnMean",
        "full_name": "PSL_Winter_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي عند مستوى سطح البحر لفصل الشتاء الأرصادي (DJF).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر خلال فصل الشتاء (hPa)"
    },
    {
        "short_name": "PSL_SpMean",
        "full_name": "PSL_Spring_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي عند مستوى سطح البحر لفصل الربيع الأرصادي (MAM).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر خلال فصل الربيع (hPa)"
    },
    {
        "short_name": "PSL_SuMean",
        "full_name": "PSL_Summer_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي عند مستوى سطح البحر لفصل الصيف الأرصادي (JJA).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر خلال فصل الصيف (hPa)"
    },
    {
        "short_name": "PSL_AuMean",
        "full_name": "PSL_Autumn_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي عند مستوى سطح البحر لفصل الخريف الأرصادي (SON).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر خلال فصل الخريف (hPa)"
    },
    {
        "short_name": "PSL_AnRng",
        "full_name": "PSL_Annual_Range",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"المدى البارومتري السنوي لضغط مستوى البحر (الفارق بين أعلى وأدنى متوسط شهري للضغط).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المدى السنوي لضغط مستوى سطح البحر (hPa)"
    },

    # --- 7. الضغط الجوي السطحي الفعلي (04_Surface_Pressure) ---
    {
        "short_name": "PS_AnnMean",
        "full_name": "PS_Annual_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المتوسط السنوي للضغط الجوي السطحي الفعلي الحقيقي عند منسوب تضاريس المحطة.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المتوسط السنوي للضغط الجوي السطحي (hPa)"
    },
    {
        "short_name": "PS_WinMean",
        "full_name": "PS_Winter_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي لفصل الشتاء الأرصادي (DJF).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي خلال فصل الشتاء (hPa)"
    },
    {
        "short_name": "PS_SprMean",
        "full_name": "PS_Spring_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي لفصل الربيع الأرصادي (MAM).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي خلال فصل الربيع (hPa)"
    },
    {
        "short_name": "PS_SumMean",
        "full_name": "PS_Summer_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي لفصل الصيف الأرصادي (JJA).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي خلال فصل الصيف (hPa)"
    },
    {
        "short_name": "PS_AutMean",
        "full_name": "PS_Autumn_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي لفصل الخريف الأرصادي (SON).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي خلال فصل الخريف (hPa)"
    },
    {
        "short_name": "PS_AnnRng",
        "full_name": "PS_Annual_Range",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المدى البارومتري السنوي للضغط السطحي (الفارق بين أعلى وأدنى متوسط شهري للضغط السطحي).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المدى السنوي للضغط الجوي السطحي (hPa)"
    },

    # --- 8. سرعة واتجاه الرياح (05_Wind) ---
    {
        "short_name": "WSp_AnMean",
        "full_name": "W_Spd_Annual_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"المتوسط السنوي لسرعة الرياح عند ارتفاع 10 أمتار فوق سطح الأرض.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة المتوسط السنوي لسرعة الرياح (م/ث)"
    },
    {
        "short_name": "WSp_WnMean",
        "full_name": "W_Spd_Winter_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح لفصل الشتاء الأرصادي عند ارتفاع 10 أمتار (DJF).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح خلال فصل الشتاء (م/ث)"
    },
    {
        "short_name": "WSp_SpMean",
        "full_name": "W_Spd_Spring_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح لفصل الربيع الأرصادي عند ارتفاع 10 أمتار (MAM).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح خلال فصل الربيع (م/ث)"
    },
    {
        "short_name": "WSp_SuMean",
        "full_name": "W_Spd_Summer_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح لفصل الصيف الأرصادي عند ارتفاع 10 أمتار (JJA).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح خلال فصل الصيف (م/ث)"
    },
    {
        "short_name": "WSp_AuMean",
        "full_name": "W_Spd_Autumn_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح لفصل الخريف الأرصادي عند ارتفاع 10 أمتار (SON).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح خلال فصل الخريف (م/ث)"
    },
    {
        "short_name": "WSp_MaxMo",
        "full_name": "W_Spd_Annual_Max_Month",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"أقصى متوسط شهري مسجل لسرعة الرياح في السنة (ذروة النشاط الريحي).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة أقصى متوسط شهري لسرعة الرياح (م/ث)"
    },
    {
        "short_name": "WSp_MinMo",
        "full_name": "W_Spd_Annual_Min_Month",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"أدنى متوسط شهري مسجل لسرعة الرياح في السنة (فترة الهدوء الريحي).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة أدنى متوسط شهري لسرعة الرياح (م/ث)"
    },
    {
        "short_name": "WSp_AnRng",
        "full_name": "W_Spd_Annual_Range",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"المدى السنوي لسرعة الرياح (الفارق بين أشد شهور السنة رياحاً وأهدأها سرعة).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة المدى السنوي لسرعة الرياح (م/ث)"
    },
    {
        "short_name": "WDr_AnMean",
        "full_name": "W_Dir_Annual_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"الاتجاه السائد السنوي للرياح بالدرجات الزاوية (محسوب بالمتوسط الدائري للمتجهات الدائرية atan2).",
        "unit": u"درجة (°)",
        "map_title": u"خريطة الاتجاه السائد السنوي للرياح (درجات)"
    },
    {
        "short_name": "WDr_WnMean",
        "full_name": "W_Dir_Winter_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"اتجاه الرياح السائد خلال فصل الشتاء الأرصادي بالدرجات الزاوية (DJF).",
        "unit": u"درجة (°)",
        "map_title": u"خريطة اتجاه الرياح السائد خلال فصل الشتاء (درجات)"
    },
    {
        "short_name": "WDr_SpMean",
        "full_name": "W_Dir_Spring_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"اتجاه الرياح السائد خلال فصل الربيع الأرصادي بالدرجات الزاوية (MAM).",
        "unit": u"درجة (°)",
        "map_title": u"خريطة اتجاه الرياح السائد خلال فصل الربيع (درجات)"
    },
    {
        "short_name": "WDr_SuMean",
        "full_name": "W_Dir_Summer_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"اتجاه الرياح السائد خلال فصل الصيف الأرصادي بالدرجات الزاوية (JJA).",
        "unit": u"درجة (°)",
        "map_title": u"خريطة اتجاه الرياح السائد خلال فصل الصيف (درجات)"
    },
    {
        "short_name": "WDr_AuMean",
        "full_name": "W_Dir_Autumn_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"اتجاه الرياح السائد خلال فصل الخريف الأرصادي بالدرجات الزاوية (SON).",
        "unit": u"درجة (°)",
        "map_title": u"خريطة اتجاه الرياح السائد خلال فصل الخريف (درجات)"
    },

    # --- 9. الرطوبة النسبية (06_Relative_Humidity) ---
    {
        "short_name": "RH_AnMean",
        "full_name": "RH_Annual_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المتوسط الحسابي السنوي للرطوبة النسبية للهواء عند ارتفاع 2 متر كنسبة مئوية.",
        "unit": u"%",
        "map_title": u"خريطة المتوسط السنوي للرطوبة النسبية (%)"
    },
    {
        "short_name": "RH_WnMean",
        "full_name": "RH_Winter_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية لفصل الشتاء الأرصادي (DJF).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية خلال فصل الشتاء (%)"
    },
    {
        "short_name": "RH_SpMean",
        "full_name": "RH_Spring_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية لفصل الربيع الأرصادي (MAM).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية خلال فصل الربيع (%)"
    },
    {
        "short_name": "RH_SuMean",
        "full_name": "RH_Summer_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية لفصل الصيف الأرصادي (JJA).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية خلال فصل الصيف (%)"
    },
    {
        "short_name": "RH_AuMean",
        "full_name": "RH_Autumn_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية لفصل الخريف الأرصادي (SON).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية خلال فصل الخريف (%)"
    },
    {
        "short_name": "RH_AnRng",
        "full_name": "RH_Annual_Range",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المدى السنوي للرطوبة النسبية (الفارق بين أعلى شهر رطوبة وأدنى شهر رطوبة).",
        "unit": u"%",
        "map_title": u"خريطة المدى السنوي للرطوبة النسبية (%)"
    },

    # --- 10. الإشعاع الشمسي (08_Solar_Radiation) ---
    {
        "short_name": "Sol_AnMean",
        "full_name": "Sol_Annual_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المتوسط اليومي السنوي للإشعاع الشمسي الكلي السطحي الواصل لسطح الأرض في كافة ظروف السماء.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المتوسط اليومي السنوي للإشعاع الشمسي (kWh/m²/day)"
    },
    {
        "short_name": "Sol_AnTot",
        "full_name": "Sol_Annual_Total",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"إجمالي الطاقة الشمسية السنوية التراكمية الساقطة على المتر المربع في السنة كاملة.",
        "unit": u"kWh/m²/year",
        "map_title": u"خريطة إجمالي الطاقة الشمسية السنوية التراكمية (kWh/m²/year)"
    },
    {
        "short_name": "Sol_WnMean",
        "full_name": "Sol_Winter_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"متوسط الإشعاع الشمسي اليومي لفصل الشتاء الأرصادي (DJF).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة متوسط الإشعاع الشمسي خلال فصل الشتاء (kWh/m²/day)"
    },
    {
        "short_name": "Sol_SpMean",
        "full_name": "Sol_Spring_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"متوسط الإشعاع الشمسي اليومي لفصل الربيع الأرصادي (MAM).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة متوسط الإشعاع الشمسي خلال فصل الربيع (kWh/m²/day)"
    },
    {
        "short_name": "Sol_SuMean",
        "full_name": "Sol_Summer_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"متوسط الإشعاع الشمسي اليومي لفصل الصيف الأرصادي (JJA).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة متوسط الإشعاع الشمسي خلال فصل الصيف (kWh/m²/day)"
    },
    {
        "short_name": "Sol_AuMean",
        "full_name": "Sol_Autumn_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"متوسط الإشعاع الشمسي اليومي لفصل الخريف الأرصادي (SON).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة متوسط الإشعاع الشمسي خلال فصل الخريف (kWh/m²/day)"
    },
    {
        "short_name": "Sol_AnRng",
        "full_name": "Sol_Annual_Range",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المدى السنوي للإشعاع الشمسي (الفارق بين ذروة الإشعاع في الصيف وأدناه في الشتاء).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المدى السنوي للإشعاع الشمسي (kWh/m²/day)"
    },

    # --- 11. مؤشر الأشعة فوق البنفسجية (09_UV_Index) ---
    {
        "short_name": "UV_AnMean",
        "full_name": "UV_Annual_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"المتوسط السنوي لمؤشر الأشعة فوق البنفسجية عند الظهيرة وفق منظومة منظمة الصحة العالمية.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة المتوسط السنوي لمؤشر الأشعة فوق البنفسجية (UV)"
    },
    {
        "short_name": "UV_WnMean",
        "full_name": "UV_Winter_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية لفصل الشتاء الأرصادي (DJF).",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية خلال فصل الشتاء"
    },
    {
        "short_name": "UV_SpMean",
        "full_name": "UV_Spring_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية لفصل الربيع الأرصادي (MAM).",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية خلال فصل الربيع"
    },
    {
        "short_name": "UV_SuMean",
        "full_name": "UV_Summer_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية لفصل الصيف الأرصادي (JJA - ذروة مخاطر الحروق الشمسية).",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية خلال فصل الصيف"
    },
    {
        "short_name": "UV_AuMean",
        "full_name": "UV_Autumn_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية لفصل الخريف الأرصادي (SON).",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية خلال فصل الخريف"
    },
    {
        "short_name": "UV_AnRng",
        "full_name": "UV_Annual_Range",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"المدى السنوي لمؤشر الأشعة فوق البنفسجية (الفارق بين ذروة الصيف وأدنى مستويات الشتاء).",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة المدى السنوي لمؤشر الأشعة فوق البنفسجية"
    },

    # --- 12. الغطاء السحابي (10_Cloud_Cover) ---
    {
        "short_name": "Cld_AnMean",
        "full_name": "Cld_Annual_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المتوسط السنوي لنسبة تغطية السماء بالغيوم والسحب كنسبة مئوية.",
        "unit": u"%",
        "map_title": u"خريطة المتوسط السنوي لنسبة الغطاء السحابي (%)"
    },
    {
        "short_name": "Cld_WnMean",
        "full_name": "Cld_Winter_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة تغطية السحب لفصل الشتاء الأرصادي (DJF).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي خلال فصل الشتاء (%)"
    },
    {
        "short_name": "Cld_SpMean",
        "full_name": "Cld_Spring_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة تغطية السحب لفصل الربيع الأرصادي (MAM).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي خلال فصل الربيع (%)"
    },
    {
        "short_name": "Cld_SuMean",
        "full_name": "Cld_Summer_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة تغطية السحب لفصل الصيف الأرصادي (JJA).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي خلال فصل الصيف (%)"
    },
    {
        "short_name": "Cld_AuMean",
        "full_name": "Cld_Autumn_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة تغطية السحب لفصل الخريف الأرصادي (SON).",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي خلال فصل الخريف (%)"
    },
    {
        "short_name": "Cld_AnRng",
        "full_name": "Cld_Annual_Range",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المدى السنوي لتغطية السحب (الفارق بين أكثر شهور السنة غيوماً وأكثرها صفاءً).",
        "unit": u"%",
        "map_title": u"خريطة المدى السنوي لنسبة الغطاء السحابي (%)"
    },

    # --- 13. مؤشر البرودة الريحية (12_Wind_Chill) ---
    {
        "short_name": "WC_WinMean",
        "full_name": "WC_Winter_Mean",
        "module_code": "12_Wind_Chill",
        "module_name": "12_Wind_Chill (مبرد الرياح)",
        "desc_ar": u"متوسط درجة البرودة الريحية لفصل الشتاء المحسوبة بمعادلة NWS لخفض الحرارة بفعل سرعة الرياح.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط مبرد الرياح خلال فصل الشتاء (°C)"
    },
    {
        "short_name": "WC_AnnMean",
        "full_name": "WC_Annual_Mean",
        "module_code": "12_Wind_Chill",
        "module_name": "12_Wind_Chill (مبرد الرياح)",
        "desc_ar": u"المتوسط الحسابي السنوي لتأثير البرودة الريحية على حرارة الهواء المحسوسة.",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط السنوي لمبرد الرياح (°C)"
    },

    # --- 14. مؤشر دي مارتون للقحولة (13_De_Martonne_Aridity) ---
    {
        "short_name": "DM_AridAnn",
        "full_name": "DM_Aridity_Annual",
        "module_code": "13_De_Martonne_Aridity",
        "module_name": "13_De_Martonne_Aridity (دليل دي مارتون)",
        "desc_ar": u"دليل القحولة والجفاف السنوي لدي مارتون I = P / (T + 10) لتصنيف الأقاليم من القاحل فائق الجفاف إلى الرطب.",
        "unit": u"مؤشر (Index)",
        "map_title": u"خريطة دليل دي مارتون السنوي للقحولة والجفاف"
    },

    # --- 15. البخر والنتح (14_Evapotranspiration) ---
    {
        "short_name": "ET_AnnTot",
        "full_name": "ET_Annual_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"المجموع التراكمي السنوي للبخر والنتح المرجعي الكامن المحسوب بمعادلة Hargreaves-Samani (FAO-56).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المجموع السنوي للبخر والنتح (ملم)"
    },
    {
        "short_name": "ET_AnnMean",
        "full_name": "ET_Annual_Mean",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"المعدل الشهري للبخر والنتح المرجعي (المجموع التراكمي السنوي مقسوماً على 12 شهراً).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المعدل الشهري للبخر والنتح (ملم)"
    },
    {
        "short_name": "ET_AnnRng",
        "full_name": "ET_Annual_Range",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"المدى السنوي للبخر والنتح (الفارق بين أعلى شهور السنة فقداً للماء بالبخر والنتح وأدناها).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المدى السنوي للبخر والنتح (ملم)"
    },
    {
        "short_name": "ET_SeaRng",
        "full_name": "ET_Seasonal_Range",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"المدى الفصلي للبخر والنتح (الفارق بين مجموع أعلى فصول السنة في البخر والنتح ومجموع أقلها).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة المدى الفصلي للبخر والنتح (ملم)"
    },
    {
        "short_name": "ET_WinTot",
        "full_name": "ET_Winter_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"مجموع البخر والنتح لفصل الشتاء الأرصادي (شهور ديسمبر، يناير، فبراير - DJF).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع البخر والنتح خلال فصل الشتاء (ملم)"
    },
    {
        "short_name": "ET_SprTot",
        "full_name": "ET_Spring_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"مجموع البخر والنتح لفصل الربيع الأرصادي (شهور مارس، أبريل، مايو - MAM).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع البخر والنتح خلال فصل الربيع (ملم)"
    },
    {
        "short_name": "ET_SumTot",
        "full_name": "ET_Summer_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"مجموع البخر والنتح لفصل الصيف الأرصادي (شهور يونيو، يوليو، أغسطس - JJA).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع البخر والنتح خلال فصل الصيف (ملم)"
    },
    {
        "short_name": "ET_AutTot",
        "full_name": "ET_Autumn_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"مجموع البخر والنتح لفصل الخريف الأرصادي (شهور سبتمبر، أكتوبر، نوفمبر - SON).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة مجموع البخر والنتح خلال فصل الخريف (ملم)"
    },
    {
        "short_name": "PET_HarAnn",
        "full_name": "PET_Hargreaves_Annual",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"التبخر-نتح الكامن السنوي بهارجريفز (حقل رديف مطابق تماماً لـ ET_Annual_Total للتوافقية العكسية).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة التبخر والنتح الكامن السنوي بهارجريفز (ملم)"
    },

    # --- 16. مؤشر القحولة العالمي (15_UNEP_Aridity) ---
    {
        "short_name": "UNEP_Arid",
        "full_name": "UNEP_Aridity_Annual",
        "module_code": "15_UNEP_Aridity",
        "module_name": "15_UNEP_Aridity (مؤشر UNEP)",
        "desc_ar": u"مؤشر القحولة العالمي لبرنامج الأمم المتحدة للبيئة AI = P / ET_ann لتحديد المناطق القاحلة وشبه القاحلة.",
        "unit": u"نسبة (Ratio)",
        "map_title": u"خريطة مؤشر القحولة العالمي لبرنامج الأمم المتحدة للبيئة"
    },

    # --- 17. الموازنة والعجز المائي المناخي (16_Water_Deficit) ---
    {
        "short_name": "WatDefAnn",
        "full_name": "Water_Deficit_Annual",
        "module_code": "16_Water_Deficit",
        "module_name": "16_Water_Deficit (العجز المائي)",
        "desc_ar": u"الموازنة المائية المناخية السنوية الصافية WD = P - ET_ann (القيم السالبة تعبر عن عجز مائي والموجبة فائض مائي).",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة الموازنة والعجز المائي المناخي السنوي (ملم)"
    },

    # --- 18. الأشهر الجافة بيولوجياً (17_Dry_Months) ---
    {
        "short_name": "Dry_Months",
        "full_name": "Dry_Months_Count",
        "module_code": "17_Dry_Months",
        "module_name": "17_Dry_Months (الأشهر الجافة)",
        "desc_ar": u"عدد أشهر السنة الجافة بيولوجياً ومناخياً وفق معيار والتر-ليث البيومناخي الشهير (P < 2T).",
        "unit": u"شهر (0-12)",
        "map_title": u"خريطة عدد الأشهر الجافة بيولوجياً في السنة"
    },

    # --- 19. الاتجاهات والشذوذ المناخي (18_Trends_And_Anomalies) ---
    {
        "short_name": "T_TrendDec",
        "full_name": "T_Trend_Decade",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"معدل تغير واتجاه درجة الحرارة لكل عقد زمني (10 سنوات) باستخدام انحدار المربعات الصغرى الخطي.",
        "unit": u"°C/decade",
        "map_title": u"خريطة اتجاه تغير درجة الحرارة في العقد الزمني (°C/decade)"
    },
    {
        "short_name": "R_TrendDec",
        "full_name": "R_Trend_Decade",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"معدل تغير واتجاه تساقط الأمطار لكل عقد زمني (10 سنوات) باستخدام انحدار المربعات الصغرى الخطي.",
        "unit": u"mm/decade",
        "map_title": u"خريطة اتجاه تغير تساقط الأمطار في العقد الزمني (mm/decade)"
    },
    {
        "short_name": "T_AnomAnn",
        "full_name": "T_Anom_Annual",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"الشذوذ الحراري السنوي لدرجة الحرارة مقارنة بخط الأساس المناخي العالمي 1991–2020.",
        "unit": u"°C",
        "map_title": u"خريطة الشذوذ الحراري السنوي مقارنة بخط أساس 1991–2020 (°C)"
    },
    {
        "short_name": "T_AnomWin",
        "full_name": "T_Anom_Winter",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"الشذوذ الحراري لفصل الشتاء مقارنة بمتوسط شهور الشتاء لخط الأساس المناخي 1991–2020.",
        "unit": u"°C",
        "map_title": u"خريطة الشذوذ الحراري لفصل الشتاء مقارنة بخط أساس 1991–2020 (°C)"
    },
    {
        "short_name": "T_AnomSum",
        "full_name": "T_Anom_Summer",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"الشذوذ الحراري لفصل الصيف مقارنة بمتوسط شهور الصيف لخط الأساس المناخي 1991–2020.",
        "unit": u"°C",
        "map_title": u"خريطة الشذوذ الحراري لفصل الصيف مقارنة بخط أساس 1991–2020 (°C)"
    },
    {
        "short_name": "R_AnomAnn",
        "full_name": "R_Anom_Annual",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"شذوذ الأمطار السنوي المطلق مقارنة بمتوسط الأمطار لخط الأساس المناخي 1991–2020.",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة شذوذ تساقط الأمطار السنوي مقارنة بخط أساس 1991–2020 (ملم)"
    },
    {
        "short_name": "R_AnomPct",
        "full_name": "R_Anom_Annual_Pct",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"شذوذ الأمطار السنوي كنسبة مئوية من خط الأساس المناخي 1991–2020 (فرق نسبي مئوي).",
        "unit": u"%",
        "map_title": u"خريطة الشذوذ النسبي المئوي للأمطار مقارنة بخط أساس 1991–2020 (%)"
    },
    {
        "short_name": "R_AnomWin",
        "full_name": "R_Anom_Winter",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"شذوذ أمطار فصل الشتاء المطلق مقارنة بأمطار شتاء خط الأساس المناخي 1991–2020.",
        "unit": u"ملم (mm)",
        "map_title": u"خريطة شذوذ أمطار الشتاء مقارنة بخط أساس 1991–2020 (ملم)"
    },
    {
        "short_name": "R_AnomWPct",
        "full_name": "R_Anom_Winter_Pct",
        "module_code": "18_Trends_And_Anomalies",
        "module_name": "18_Trends_And_Anomalies (الاتجاهات والشذوذ)",
        "desc_ar": u"شذوذ أمطار فصل الشتاء كنسبة مئوية مقارنة بأمطار شتاء خط الأساس المناخي 1991–2020.",
        "unit": u"%",
        "map_title": u"خريطة الشذوذ النسبي المئوي لأمطار الشتاء مقارنة بخط أساس 1991–2020 (%)"
    }
]

MODULES_SUMMARY = [
    {
        "num": "01",
        "name_en": "01_Temperature",
        "name_ar": u"درجة الحرارة",
        "folder": "01_Temperature",
        "fc": "01_Temperature",
        "count": 10,
        "unit": u"°C",
        "method": u"NASA POWER T2M, T2M_MAX, T2M_MIN / WMO Climatological Normals"
    },
    {
        "num": "02",
        "name_en": "02_Precipitation",
        "name_ar": u"الأمطار والتساقط",
        "folder": "02_Precipitation",
        "fc": "02_Precipitation",
        "count": 8,
        "unit": u"mm",
        "method": u"NASA POWER PRECTOTCORR / Annual, Seasonal Totals & Ranges"
    },
    {
        "num": "03",
        "name_en": "03_Sea_Level_Pressure",
        "name_ar": u"ضغط مستوى سطح البحر",
        "folder": "03_Sea_Level_Pressure",
        "fc": "03_Sea_Level_Pressure",
        "count": 6,
        "unit": u"hPa / mbar",
        "method": u"NASA POWER SLP / Reduced to Standard Mean Sea Level"
    },
    {
        "num": "04",
        "name_en": "04_Surface_Pressure",
        "name_ar": u"الضغط السطحي الفعلي",
        "folder": "04_Surface_Pressure",
        "fc": "04_Surface_Pressure",
        "count": 6,
        "unit": u"hPa / mbar",
        "method": u"NASA POWER PS / Actual Local Topographic Station Pressure"
    },
    {
        "num": "05",
        "name_en": "05_Wind",
        "name_ar": u"الرياح السطحية (سرعة واتجاه)",
        "folder": "05_Wind",
        "fc": "05_Wind",
        "count": 13,
        "unit": u"m/s, °",
        "method": u"NASA POWER WS10M, WD10M / Circular Mean Vector atan2"
    },
    {
        "num": "06",
        "name_en": "06_Relative_Humidity",
        "name_ar": u"الرطوبة النسبية",
        "folder": "06_Relative_Humidity",
        "fc": "06_Relative_Humidity",
        "count": 6,
        "unit": u"%",
        "method": u"NASA POWER RH2M / Climatological Relative Humidity at 2m"
    },
    {
        "num": "07",
        "name_en": "07_Dew_Point",
        "name_ar": u"نقطة الندى",
        "folder": "07_Dew_Point",
        "fc": "07_Dew_Point",
        "count": 6,
        "unit": u"°C",
        "method": u"NASA POWER T2MDEW / Dew Point Temperature at 2m"
    },
    {
        "num": "08",
        "name_en": "08_Solar_Radiation",
        "name_ar": u"الإشعاع الشمسي والطاقة",
        "folder": "08_Solar_Radiation",
        "fc": "08_Solar_Radiation",
        "count": 7,
        "unit": u"kWh/m²/day",
        "method": u"NASA POWER ALLSKY_SFC_SW_DWN / Daily Mean & Cumulative Annual"
    },
    {
        "num": "09",
        "name_en": "09_UV_Index",
        "name_ar": u"مؤشر الأشعة فوق البنفسجية",
        "folder": "09_UV_Index",
        "fc": "09_UV_Index",
        "count": 6,
        "unit": u"Index (0–16+)",
        "method": u"WHO / WMO Global Solar UV Index Standard"
    },
    {
        "num": "10",
        "name_en": "10_Cloud_Cover",
        "name_ar": u"الغطاء السحابي",
        "folder": "10_Cloud_Cover",
        "fc": "10_Cloud_Cover",
        "count": 6,
        "unit": u"%",
        "method": u"NASA POWER CLOUD_AMT / Total Sky Cloud Fraction"
    },
    {
        "num": "11",
        "name_en": "11_Heat_Index",
        "name_ar": u"مؤشر الحرارة والإجهاد الحراري",
        "folder": "11_Heat_Index",
        "fc": "11_Heat_Index",
        "count": 5,
        "unit": u"°C",
        "method": u"Steadman-Rothfusz NWS Formula + Humidex + ISO 7243 WBGT"
    },
    {
        "num": "12",
        "name_en": "12_Wind_Chill",
        "name_ar": u"مبرد الرياح",
        "folder": "12_Wind_Chill",
        "fc": "12_Wind_Chill",
        "count": 2,
        "unit": u"°C",
        "method": u"US National Weather Service (NWS) Wind Chill Equivalent"
    },
    {
        "num": "13",
        "name_en": "13_De_Martonne_Aridity",
        "name_ar": u"دليل الجفاف لدي مارتون",
        "folder": "13_De_Martonne_Aridity",
        "fc": "13_De_Martonne_Aridity",
        "count": 1,
        "unit": u"Index",
        "method": u"De Martonne (1926) Aridity Index: I = P / (T + 10)"
    },
    {
        "num": "14",
        "name_en": "14_Evapotranspiration",
        "name_ar": u"البخر والنتح المرجعي (ET)",
        "folder": "14_Evapotranspiration",
        "fc": "14_Evapotranspiration",
        "count": 9,
        "unit": u"mm",
        "method": u"FAO-56 Hargreaves-Samani (1985) Extraterrestrial Radiation Ra"
    },
    {
        "num": "15",
        "name_en": "15_UNEP_Aridity",
        "name_ar": u"مؤشر القحولة UNEP",
        "folder": "15_UNEP_Aridity",
        "fc": "15_UNEP_Aridity",
        "count": 1,
        "unit": u"Ratio",
        "method": u"UNEP Global Aridity Index: AI = P / ETo"
    },
    {
        "num": "16",
        "name_en": "16_Water_Deficit",
        "name_ar": u"الموازنة والعجز المائي",
        "folder": "16_Water_Deficit",
        "fc": "16_Water_Deficit",
        "count": 1,
        "unit": u"mm",
        "method": u"Climatic Water Balance: WD = P - ETo (Negative = Deficit)"
    },
    {
        "num": "17",
        "name_en": "17_Dry_Months",
        "name_ar": u"عدد الأشهر الجافة بيولوجياً",
        "folder": "17_Dry_Months",
        "fc": "17_Dry_Months",
        "count": 1,
        "unit": u"Months (0–12)",
        "method": u"Walter-Lieth Bioclimatic Standard: P < 2 * T"
    },
    {
        "num": "18",
        "name_en": "18_Trends_And_Anomalies",
        "name_ar": u"الاتجاهات والشذوذ المناخي",
        "folder": "18_Trends_And_Anomalies",
        "fc": "18_Trends_And_Anomalies",
        "count": 9,
        "unit": u"°C, mm, %",
        "method": u"OLS Linear Regression Trends & WMO 1991–2020 Baseline Anomalies"
    }
]


def build_excel(output_path):
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Styles
    # ----------------------------------------------------
    navy_dark = "1F4E79"
    navy_med = "2F5597"
    header_fill = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    summary_fill = PatternFill(start_color=navy_med, end_color=navy_med, fill_type="solid")
    zebra_even = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    zebra_odd = PatternFill(start_color="F2F6FA", end_color="F2F6FA", fill_type="solid")
    admin_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_title = Font(name="Segoe UI", size=14, bold=True, color="1F4E79")
    font_bold = Font(name="Segoe UI", size=10, bold=True, color="000000")
    font_regular = Font(name="Segoe UI", size=10, color="000000")
    font_code = Font(name="Consolas", size=10, bold=True, color="1F4E79")
    font_map_title = Font(name="Segoe UI", size=10, bold=True, color="165B33")
    font_unit = Font(name="Segoe UI", size=10, bold=True, color="7F3F98")
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)
    
    # ----------------------------------------------------
    # Sheet 1: Climate Fields
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "Climate_Fields"
    
    headers_ws1 = [
        u"م",
        u"اسم الحقل المختصر (Shapefile)\nShort Field Name",
        u"اسم الحقل الكامل (Geodatabase / API)\nFull Field Name (EN)",
        u"الموديول / العنصر المناخي\nClimate Module",
        u"الشرح والتوصيف العلمي باللغة العربية\nScientific Description (AR)",
        u"وحدة القياس\nUnit",
        u"اسم الخريطة المقترح\nSuggested Map Title (AR)"
    ]
    
    ws1.row_dimensions[1].height = 36
    for col_idx, h_text in enumerate(headers_ws1, 1):
        cell = ws1.cell(row=1, column=col_idx, value=h_text)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = thin_border
    
    for row_idx, item in enumerate(FIELDS_DATA, 2):
        ws1.row_dimensions[row_idx].height = 24
        is_admin = item["module_code"].startswith("00")
        row_fill = admin_fill if is_admin else (zebra_even if row_idx % 2 == 0 else zebra_odd)
        
        # Col 1: Serial
        c1 = ws1.cell(row=row_idx, column=1, value=row_idx - 1)
        c1.font = font_bold
        c1.alignment = align_center
        c1.fill = row_fill
        c1.border = thin_border
        
        # Col 2: Short Name
        c2 = ws1.cell(row=row_idx, column=2, value=item["short_name"])
        c2.font = font_code
        c2.alignment = align_center
        c2.fill = row_fill
        c2.border = thin_border
        
        # Col 3: Full Name
        c3 = ws1.cell(row=row_idx, column=3, value=item["full_name"])
        c3.font = font_bold
        c3.alignment = align_left
        c3.fill = row_fill
        c3.border = thin_border
        
        # Col 4: Module Name
        c4 = ws1.cell(row=row_idx, column=4, value=item["module_name"])
        c4.font = font_regular
        c4.alignment = align_left
        c4.fill = row_fill
        c4.border = thin_border
        
        # Col 5: Description AR
        c5 = ws1.cell(row=row_idx, column=5, value=item["desc_ar"])
        c5.font = font_regular
        c5.alignment = align_right
        c5.fill = row_fill
        c5.border = thin_border
        
        # Col 6: Unit
        c6 = ws1.cell(row=row_idx, column=6, value=item["unit"])
        c6.font = font_unit
        c6.alignment = align_center
        c6.fill = row_fill
        c6.border = thin_border
        
        # Col 7: Suggested Map Title AR
        c7 = ws1.cell(row=row_idx, column=7, value=item["map_title"])
        c7.font = font_map_title if item["map_title"] != "-" else font_regular
        c7.alignment = align_right if item["map_title"] != "-" else align_center
        c7.fill = row_fill
        c7.border = thin_border

    # Freeze panes on Header
    ws1.freeze_panes = "A2"
    
    # Auto-filter
    ws1.auto_filter.ref = "A1:G{}".format(len(FIELDS_DATA) + 1)
    
    # Column widths for Sheet 1
    col_widths_1 = {
        1: 6,   # م
        2: 24,  # Short Name
        3: 28,  # Full Name
        4: 30,  # Module Name
        5: 65,  # Description AR
        6: 18,  # Unit
        7: 48   # Map Title AR
    }
    for col_idx, width in col_widths_1.items():
        ws1.column_dimensions[get_column_letter(col_idx)].width = width

    # ----------------------------------------------------
    # Sheet 2: Modules Summary
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Modules_18_Summary")
    
    headers_ws2 = [
        u"الرقم\nNo.",
        u"اسم العنصر في الأداة\nTool Parameter & Layer",
        u"الاسم باللغة العربية\nModule Arabic Name",
        u"مجلد الراستر (1:1)\nOutput Raster Folder",
        u"طبقة المعالم (1:1)\nFeature Class Name",
        u"عدد المؤشرات\nIndicators",
        u"الوحدة الرئيسية\nMain Unit",
        u"المنهجية والمعادلة العلمية\nScientific Method & Standards"
    ]
    
    ws2.row_dimensions[1].height = 36
    for col_idx, h_text in enumerate(headers_ws2, 1):
        cell = ws2.cell(row=1, column=col_idx, value=h_text)
        cell.font = font_header
        cell.fill = summary_fill
        cell.alignment = align_center
        cell.border = thin_border
        
    for row_idx, item in enumerate(MODULES_SUMMARY, 2):
        ws2.row_dimensions[row_idx].height = 24
        row_fill = zebra_even if row_idx % 2 == 0 else zebra_odd
        
        c1 = ws2.cell(row=row_idx, column=1, value=item["num"])
        c1.font = font_bold
        c1.alignment = align_center
        c1.fill = row_fill
        c1.border = thin_border
        
        c2 = ws2.cell(row=row_idx, column=2, value=item["name_en"])
        c2.font = font_code
        c2.alignment = align_left
        c2.fill = row_fill
        c2.border = thin_border
        
        c3 = ws2.cell(row=row_idx, column=3, value=item["name_ar"])
        c3.font = font_bold
        c3.alignment = align_right
        c3.fill = row_fill
        c3.border = thin_border
        
        c4 = ws2.cell(row=row_idx, column=4, value=item["folder"])
        c4.font = font_code
        c4.alignment = align_left
        c4.fill = row_fill
        c4.border = thin_border
        
        c5 = ws2.cell(row=row_idx, column=5, value=item["fc"])
        c5.font = font_code
        c5.alignment = align_left
        c5.fill = row_fill
        c5.border = thin_border
        
        c6 = ws2.cell(row=row_idx, column=6, value=item["count"])
        c6.font = font_bold
        c6.alignment = align_center
        c6.fill = row_fill
        c6.border = thin_border
        
        c7 = ws2.cell(row=row_idx, column=7, value=item["unit"])
        c7.font = font_unit
        c7.alignment = align_center
        c7.fill = row_fill
        c7.border = thin_border
        
        c8 = ws2.cell(row=row_idx, column=8, value=item["method"])
        c8.font = font_regular
        c8.alignment = align_left
        c8.fill = row_fill
        c8.border = thin_border

    # Row 20: Total Summary
    total_row = len(MODULES_SUMMARY) + 2
    ws2.row_dimensions[total_row].height = 26
    c_tot_label = ws2.cell(row=total_row, column=3, value=u"الإجمالي العام للمؤشرات المناخية:")
    c_tot_label.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    c_tot_label.alignment = align_right
    
    total_indicators = sum(m["count"] for m in MODULES_SUMMARY)
    c_tot_val = ws2.cell(row=total_row, column=6, value=total_indicators)
    c_tot_val.font = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    c_tot_val.alignment = align_center
    
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = "A1:H{}".format(len(MODULES_SUMMARY) + 1)
    
    col_widths_2 = {
        1: 8,   # No.
        2: 26,  # Name EN
        3: 26,  # Name AR
        4: 26,  # Folder
        5: 26,  # FC
        6: 15,  # Count
        7: 16,  # Unit
        8: 55   # Method
    }
    for col_idx, width in col_widths_2.items():
        ws2.column_dimensions[get_column_letter(col_idx)].width = width

    # Save
    wb.save(output_path)
    print("Successfully built Excel dictionary at:", output_path)
    print("Sheet 1 'Climate_Fields' total rows:", len(FIELDS_DATA) + 1)
    print("Sheet 2 'Modules_18_Summary' total rows:", len(MODULES_SUMMARY) + 1)


if __name__ == "__main__":
    import os
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(cur_dir, "docs")
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    out_file = os.path.join(docs_dir, "Climate_Atlas_Fields_Dictionary_AR_EN_Units.xlsx")
    build_excel(out_file)

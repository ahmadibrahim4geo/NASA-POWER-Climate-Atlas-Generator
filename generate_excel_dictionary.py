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
        "short_name": "T_MonMean",
        "full_name": "T_Month_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الشهري لدرجة حرارة الهواء عند ارتفاع 2 متر (متوسط الـ 12 شهراً المناخي).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط الشهري لدرجة الحرارة (°C)"
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
        "short_name": "T_SeaRng",
        "full_name": "T_Seasonal_Range",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجات الحرارة)",
        "desc_ar": u"المدى الفصلي لدرجة الحرارة (الفارق بين أدفأ فصول السنة وأبردها).",
        "unit": u"°C",
        "map_title": u"خريطة المدى الفصلي لدرجة الحرارة (°C)"
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
    {
        "short_name": "T_JanMean",
        "full_name": "T_January_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر يناير عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر يناير (°C)"
    },
    {
        "short_name": "T_FebMean",
        "full_name": "T_February_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر فبراير عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر فبراير (°C)"
    },
    {
        "short_name": "T_MarMean",
        "full_name": "T_March_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر مارس عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر مارس (°C)"
    },
    {
        "short_name": "T_AprMean",
        "full_name": "T_April_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر أبريل عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر أبريل (°C)"
    },
    {
        "short_name": "T_MayMean",
        "full_name": "T_May_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر مايو عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر مايو (°C)"
    },
    {
        "short_name": "T_JunMean",
        "full_name": "T_June_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر يونيو عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر يونيو (°C)"
    },
    {
        "short_name": "T_JulMean",
        "full_name": "T_July_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر يوليو عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر يوليو (°C)"
    },
    {
        "short_name": "T_AugMean",
        "full_name": "T_August_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر أغسطس عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر أغسطس (°C)"
    },
    {
        "short_name": "T_SepMean",
        "full_name": "T_September_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر سبتمبر عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر سبتمبر (°C)"
    },
    {
        "short_name": "T_OctMean",
        "full_name": "T_October_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر أكتوبر عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر أكتوبر (°C)"
    },
    {
        "short_name": "T_NovMean",
        "full_name": "T_November_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر نوفمبر عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر نوفمبر (°C)"
    },
    {
        "short_name": "T_DecMean",
        "full_name": "T_December_Mean",
        "module_code": "01_Temperature",
        "module_name": "01_Temperature (درجة الحرارة)",
        "desc_ar": u"المتوسط الحسابي لدرجة حرارة الهواء عند ارتفاع 2 متر لشهر ديسمبر عبر فترة الرصد 1996–2025.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة الحرارة لشهر ديسمبر (°C)"
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
        "short_name": "Td_MonMean",
        "full_name": "Td_Month_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (درجة حرارة نقطة الندى)",
        "desc_ar": u"المتوسط الشهري لدرجة حرارة نقطة الندى عند ارتفاع 2 متر (متوسط الـ 12 شهراً).",
        "unit": u"°C",
        "map_title": u"خريطة المتوسط الشهري لنقطة الندى (°C)"
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
    {
        "short_name": "Td_SeaRng",
        "full_name": "Td_Seasonal_Range",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"المدى الفصلي لنقطة الندى (الفارق بين أعلى وأدنى فصول السنة).",
        "unit": u"°C",
        "map_title": u"خريطة المدى الفصلي لنقطة الندى (°C)"
    },
    {
        "short_name": "Td_JanMean",
        "full_name": "Td_January_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر يناير.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر يناير (°C)"
    },
    {
        "short_name": "Td_FebMean",
        "full_name": "Td_February_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر فبراير.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر فبراير (°C)"
    },
    {
        "short_name": "Td_MarMean",
        "full_name": "Td_March_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر مارس.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر مارس (°C)"
    },
    {
        "short_name": "Td_AprMean",
        "full_name": "Td_April_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر أبريل.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر أبريل (°C)"
    },
    {
        "short_name": "Td_MayMean",
        "full_name": "Td_May_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر مايو.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر مايو (°C)"
    },
    {
        "short_name": "Td_JunMean",
        "full_name": "Td_June_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر يونيو.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر يونيو (°C)"
    },
    {
        "short_name": "Td_JulMean",
        "full_name": "Td_July_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر يوليو.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر يوليو (°C)"
    },
    {
        "short_name": "Td_AugMean",
        "full_name": "Td_August_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر أغسطس.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر أغسطس (°C)"
    },
    {
        "short_name": "Td_SepMean",
        "full_name": "Td_September_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر سبتمبر.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر سبتمبر (°C)"
    },
    {
        "short_name": "Td_OctMean",
        "full_name": "Td_October_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر أكتوبر.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر أكتوبر (°C)"
    },
    {
        "short_name": "Td_NovMean",
        "full_name": "Td_November_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر نوفمبر.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر نوفمبر (°C)"
    },
    {
        "short_name": "Td_DecMean",
        "full_name": "Td_December_Mean",
        "module_code": "07_Dew_Point",
        "module_name": "07_Dew_Point (نقطة الندى)",
        "desc_ar": u"متوسط درجة حرارة نقطة الندى عند ارتفاع 2 متر لشهر ديسمبر.",
        "unit": u"°C",
        "map_title": u"خريطة متوسط درجة حرارة نقطة الندى لشهر ديسمبر (°C)"
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
        "short_name": "R_WinMean",
        "full_name": "R_Winter_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط هطول الأمطار خلال فصل الشتاء (شهور ديسمبر، يناير، فبراير - DJF).",
        "unit": u"مم/فصل (mm/season)",
        "map_title": u"خريطة متوسط هطول الأمطار خلال فصل الشتاء (مم/فصل)"
    },
    {
        "short_name": "R_SprMean",
        "full_name": "R_Spring_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط هطول الأمطار خلال فصل الربيع (شهور مارس، أبريل، مايو - MAM).",
        "unit": u"مم/فصل (mm/season)",
        "map_title": u"خريطة متوسط هطول الأمطار خلال فصل الربيع (مم/فصل)"
    },
    {
        "short_name": "R_SumMean",
        "full_name": "R_Summer_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط هطول الأمطار خلال فصل الصيف (شهور يونيو، يوليو، أغسطس - JJA).",
        "unit": u"مم/فصل (mm/season)",
        "map_title": u"خريطة متوسط هطول الأمطار خلال فصل الصيف (مم/فصل)"
    },
    {
        "short_name": "R_AutMean",
        "full_name": "R_Autumn_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط هطول الأمطار خلال فصل الخريف (شهور سبتمبر، أكتوبر، نوفمبر - SON).",
        "unit": u"مم/فصل (mm/season)",
        "map_title": u"خريطة متوسط هطول الأمطار خلال فصل الخريف (مم/فصل)"
    },
    {
        "short_name": "R_JanMean",
        "full_name": "R_January_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر يناير عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر يناير (ملم/شهر)"
    },
    {
        "short_name": "R_FebMean",
        "full_name": "R_February_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر فبراير عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر فبراير (ملم/شهر)"
    },
    {
        "short_name": "R_MarMean",
        "full_name": "R_March_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر مارس عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر مارس (ملم/شهر)"
    },
    {
        "short_name": "R_AprMean",
        "full_name": "R_April_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر أبريل عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر أبريل (ملم/شهر)"
    },
    {
        "short_name": "R_MayMean",
        "full_name": "R_May_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر مايو عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر مايو (ملم/شهر)"
    },
    {
        "short_name": "R_JunMean",
        "full_name": "R_June_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر يونيو عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر يونيو (ملم/شهر)"
    },
    {
        "short_name": "R_JulMean",
        "full_name": "R_July_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر يوليو عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر يوليو (ملم/شهر)"
    },
    {
        "short_name": "R_AugMean",
        "full_name": "R_August_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر أغسطس عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر أغسطس (ملم/شهر)"
    },
    {
        "short_name": "R_SepMean",
        "full_name": "R_September_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر سبتمبر عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر سبتمبر (ملم/شهر)"
    },
    {
        "short_name": "R_OctMean",
        "full_name": "R_October_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر أكتوبر عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر أكتوبر (ملم/شهر)"
    },
    {
        "short_name": "R_NovMean",
        "full_name": "R_November_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر نوفمبر عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر نوفمبر (ملم/شهر)"
    },
    {
        "short_name": "R_DecMean",
        "full_name": "R_December_Mean",
        "module_code": "02_Precipitation",
        "module_name": "02_Precipitation (الأمطار)",
        "desc_ar": u"متوسط مجموع كميات الأمطار التراكمية لشهر ديسمبر عبر سنوات فترة الرصد 1996–2025.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة متوسط مجموع أمطار شهر ديسمبر (ملم/شهر)"
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
        "short_name": "PSL_MonMea",
        "full_name": "PSL_Month_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"المتوسط الشهري للضغط الجوي المصحح عند مستوى سطح البحر القياسي (متوسط الـ 12 شهراً).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المتوسط الشهري لضغط مستوى سطح البحر (hPa)"
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
    {
        "short_name": "PSL_SeaRng",
        "full_name": "PSL_Seasonal_Range",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"المدى الفصلي لضغط مستوى البحر (الفارق بين أعلى وأدنى فصول السنة ضغطاً).",
        "unit": u"hPa",
        "map_title": u"خريطة المدى الفصلي لضغط مستوى البحر (hPa)"
    },
    {
        "short_name": "PSL_JanMn",
        "full_name": "PSL_January_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر يناير (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر يناير (hPa)"
    },
    {
        "short_name": "PSL_FebMn",
        "full_name": "PSL_February_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر فبراير (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر فبراير (hPa)"
    },
    {
        "short_name": "PSL_MarMn",
        "full_name": "PSL_March_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر مارس (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر مارس (hPa)"
    },
    {
        "short_name": "PSL_AprMn",
        "full_name": "PSL_April_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر أبريل (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر أبريل (hPa)"
    },
    {
        "short_name": "PSL_MayMn",
        "full_name": "PSL_May_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر مايو (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر مايو (hPa)"
    },
    {
        "short_name": "PSL_JunMn",
        "full_name": "PSL_June_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر يونيو (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر يونيو (hPa)"
    },
    {
        "short_name": "PSL_JulMn",
        "full_name": "PSL_July_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر يوليو (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر يوليو (hPa)"
    },
    {
        "short_name": "PSL_AugMn",
        "full_name": "PSL_August_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر أغسطس (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر أغسطس (hPa)"
    },
    {
        "short_name": "PSL_SepMn",
        "full_name": "PSL_September_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر سبتمبر (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر سبتمبر (hPa)"
    },
    {
        "short_name": "PSL_OctMn",
        "full_name": "PSL_October_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر أكتوبر (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر أكتوبر (hPa)"
    },
    {
        "short_name": "PSL_NovMn",
        "full_name": "PSL_November_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر نوفمبر (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر نوفمبر (hPa)"
    },
    {
        "short_name": "PSL_DecMn",
        "full_name": "PSL_December_Mean",
        "module_code": "03_Sea_Level_Pressure",
        "module_name": "03_Sea_Level_Pressure (ضغط مستوى البحر)",
        "desc_ar": u"متوسط الضغط الجوي المصحح لمستوى سطح البحر القياسي لشهر ديسمبر (SLP).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط ضغط مستوى سطح البحر لشهر ديسمبر (hPa)"
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
        "short_name": "PS_MonMean",
        "full_name": "PS_Month_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المتوسط الشهري للضغط الجوي السطحي الفعلي للمحطة (متوسط الـ 12 شهراً).",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة المتوسط الشهري للضغط الجوي السطحي (hPa)"
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
    {
        "short_name": "PS_SeaRng",
        "full_name": "PS_Seasonal_Range",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"المدى الفصلي للضغط السطحي (الفارق بين فصول السنة).",
        "unit": u"hPa",
        "map_title": u"خريطة المدى الفصلي للضغط السطحي (hPa)"
    },
    {
        "short_name": "PS_JanMean",
        "full_name": "PS_January_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر يناير.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر يناير (hPa)"
    },
    {
        "short_name": "PS_FebMean",
        "full_name": "PS_February_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر فبراير.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر فبراير (hPa)"
    },
    {
        "short_name": "PS_MarMean",
        "full_name": "PS_March_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر مارس.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر مارس (hPa)"
    },
    {
        "short_name": "PS_AprMean",
        "full_name": "PS_April_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر أبريل.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر أبريل (hPa)"
    },
    {
        "short_name": "PS_MayMean",
        "full_name": "PS_May_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر مايو.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر مايو (hPa)"
    },
    {
        "short_name": "PS_JunMean",
        "full_name": "PS_June_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر يونيو.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر يونيو (hPa)"
    },
    {
        "short_name": "PS_JulMean",
        "full_name": "PS_July_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر يوليو.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر يوليو (hPa)"
    },
    {
        "short_name": "PS_AugMean",
        "full_name": "PS_August_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر أغسطس.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر أغسطس (hPa)"
    },
    {
        "short_name": "PS_SepMean",
        "full_name": "PS_September_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر سبتمبر.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر سبتمبر (hPa)"
    },
    {
        "short_name": "PS_OctMean",
        "full_name": "PS_October_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر أكتوبر.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر أكتوبر (hPa)"
    },
    {
        "short_name": "PS_NovMean",
        "full_name": "PS_November_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر نوفمبر.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر نوفمبر (hPa)"
    },
    {
        "short_name": "PS_DecMean",
        "full_name": "PS_December_Mean",
        "module_code": "04_Surface_Pressure",
        "module_name": "04_Surface_Pressure (الضغط السطحي)",
        "desc_ar": u"متوسط الضغط الجوي السطحي الفعلي الحقيقي عند منسوب المحطة لشهر ديسمبر.",
        "unit": u"hPa / mbar",
        "map_title": u"خريطة متوسط الضغط السطحي الفعلي لشهر ديسمبر (hPa)"
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
        "short_name": "WSp_MonMea",
        "full_name": "W_Spd_Month_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح السطحية)",
        "desc_ar": u"المتوسط الشهري لسرعة الرياح على ارتفاع 10 أمتار (متوسط الـ 12 شهراً).",
        "unit": u"m/s",
        "map_title": u"خريطة المتوسط الشهري لسرعة الرياح (m/s)"
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
        "short_name": "WSp_SeaRng",
        "full_name": "W_Spd_Seasonal_Range",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"المدى الفصلي لسرعة الرياح (الفارق بين أشد فصول السنة ريحاً وأهدأها).",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة المدى الفصلي لسرعة الرياح (م/ث)"
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
        "short_name": "WDr_MonMea",
        "full_name": "W_Dir_Month_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح السطحية)",
        "desc_ar": u"المتوسط الشهري لاتجاه الرياح السائدة (المتوسط الدائري للشهور الـ 12).",
        "unit": u"°",
        "map_title": u"خريطة المتوسط الشهري لاتجاه الرياح السائدة (°)"
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
    {
        "short_name": "WSp_JanMn",
        "full_name": "W_Spd_January_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر يناير عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر يناير (م/ث)"
    },
    {
        "short_name": "WSp_FebMn",
        "full_name": "W_Spd_February_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر فبراير عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر فبراير (م/ث)"
    },
    {
        "short_name": "WSp_MarMn",
        "full_name": "W_Spd_March_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر مارس عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر مارس (م/ث)"
    },
    {
        "short_name": "WSp_AprMn",
        "full_name": "W_Spd_April_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر أبريل عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر أبريل (م/ث)"
    },
    {
        "short_name": "WSp_MayMn",
        "full_name": "W_Spd_May_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر مايو عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر مايو (م/ث)"
    },
    {
        "short_name": "WSp_JunMn",
        "full_name": "W_Spd_June_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر يونيو عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر يونيو (م/ث)"
    },
    {
        "short_name": "WSp_JulMn",
        "full_name": "W_Spd_July_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر يوليو عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر يوليو (م/ث)"
    },
    {
        "short_name": "WSp_AugMn",
        "full_name": "W_Spd_August_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر أغسطس عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر أغسطس (م/ث)"
    },
    {
        "short_name": "WSp_SepMn",
        "full_name": "W_Spd_September_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر سبتمبر عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر سبتمبر (م/ث)"
    },
    {
        "short_name": "WSp_OctMn",
        "full_name": "W_Spd_October_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر أكتوبر عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر أكتوبر (م/ث)"
    },
    {
        "short_name": "WSp_NovMn",
        "full_name": "W_Spd_November_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر نوفمبر عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر نوفمبر (م/ث)"
    },
    {
        "short_name": "WSp_DecMn",
        "full_name": "W_Spd_December_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط سرعة الرياح على ارتفاع 10 أمتار لشهر ديسمبر عبر فترة الرصد.",
        "unit": u"م/ث (m/s)",
        "map_title": u"خريطة متوسط سرعة الرياح لشهر ديسمبر (م/ث)"
    },
    {
        "short_name": "WDr_JanMn",
        "full_name": "W_Dir_January_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر يناير محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر يناير (°)"
    },
    {
        "short_name": "WDr_FebMn",
        "full_name": "W_Dir_February_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر فبراير محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر فبراير (°)"
    },
    {
        "short_name": "WDr_MarMn",
        "full_name": "W_Dir_March_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر مارس محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر مارس (°)"
    },
    {
        "short_name": "WDr_AprMn",
        "full_name": "W_Dir_April_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر أبريل محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر أبريل (°)"
    },
    {
        "short_name": "WDr_MayMn",
        "full_name": "W_Dir_May_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر مايو محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر مايو (°)"
    },
    {
        "short_name": "WDr_JunMn",
        "full_name": "W_Dir_June_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر يونيو محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر يونيو (°)"
    },
    {
        "short_name": "WDr_JulMn",
        "full_name": "W_Dir_July_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر يوليو محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر يوليو (°)"
    },
    {
        "short_name": "WDr_AugMn",
        "full_name": "W_Dir_August_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر أغسطس محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر أغسطس (°)"
    },
    {
        "short_name": "WDr_SepMn",
        "full_name": "W_Dir_September_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر سبتمبر محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر سبتمبر (°)"
    },
    {
        "short_name": "WDr_OctMn",
        "full_name": "W_Dir_October_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر أكتوبر محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر أكتوبر (°)"
    },
    {
        "short_name": "WDr_NovMn",
        "full_name": "W_Dir_November_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر نوفمبر محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر نوفمبر (°)"
    },
    {
        "short_name": "WDr_DecMn",
        "full_name": "W_Dir_December_Mean",
        "module_code": "05_Wind",
        "module_name": "05_Wind (الرياح)",
        "desc_ar": u"متوسط اتجاه الرياح السائد لشهر ديسمبر محسوب بالمتوسط الدائري المتجهي (atan2).",
        "unit": u"درجة (°) / Degree",
        "map_title": u"خريطة اتجاه الرياح السائد لشهر ديسمبر (°)"
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
        "short_name": "RH_MonMean",
        "full_name": "RH_Month_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المتوسط الشهري للرطوبة النسبية عند ارتفاع 2 متر (متوسط الـ 12 شهراً).",
        "unit": u"%",
        "map_title": u"خريطة المتوسط الشهري للرطوبة النسبية (%)"
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
    {
        "short_name": "RH_SeaRng",
        "full_name": "RH_Seasonal_Range",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"المدى الفصلي للرطوبة النسبية (الفارق بين أكثر فصول السنة رطوبة وأجفها).",
        "unit": u"%",
        "map_title": u"خريطة المدى الفصلي للرطوبة النسبية (%)"
    },
    {
        "short_name": "RH_JanMean",
        "full_name": "RH_January_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر يناير عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر يناير (%)"
    },
    {
        "short_name": "RH_FebMean",
        "full_name": "RH_February_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر فبراير عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر فبراير (%)"
    },
    {
        "short_name": "RH_MarMean",
        "full_name": "RH_March_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر مارس عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر مارس (%)"
    },
    {
        "short_name": "RH_AprMean",
        "full_name": "RH_April_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر أبريل عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر أبريل (%)"
    },
    {
        "short_name": "RH_MayMean",
        "full_name": "RH_May_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر مايو عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر مايو (%)"
    },
    {
        "short_name": "RH_JunMean",
        "full_name": "RH_June_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر يونيو عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر يونيو (%)"
    },
    {
        "short_name": "RH_JulMean",
        "full_name": "RH_July_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر يوليو عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر يوليو (%)"
    },
    {
        "short_name": "RH_AugMean",
        "full_name": "RH_August_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر أغسطس عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر أغسطس (%)"
    },
    {
        "short_name": "RH_SepMean",
        "full_name": "RH_September_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر سبتمبر عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر سبتمبر (%)"
    },
    {
        "short_name": "RH_OctMean",
        "full_name": "RH_October_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر أكتوبر عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر أكتوبر (%)"
    },
    {
        "short_name": "RH_NovMean",
        "full_name": "RH_November_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر نوفمبر عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر نوفمبر (%)"
    },
    {
        "short_name": "RH_DecMean",
        "full_name": "RH_December_Mean",
        "module_code": "06_Relative_Humidity",
        "module_name": "06_Relative_Humidity (الرطوبة النسبية)",
        "desc_ar": u"متوسط الرطوبة النسبية عند ارتفاع 2 متر لشهر ديسمبر عبر فترة الرصد.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الرطوبة النسبية لشهر ديسمبر (%)"
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
        "short_name": "Sol_MonMea",
        "full_name": "Sol_Month_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المتوسط الشهري للإشعاع الشمسي اليومي الساقط على السطح الأفقي (متوسط الـ 12 شهراً).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المتوسط الشهري للإشعاع الشمسي اليومي (kWh/m²/day)"
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
    {
        "short_name": "Sol_SeaRng",
        "full_name": "Sol_Seasonal_Range",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المدى الفصلي للإشعاع الشمسي اليومي (الفارق بين فصول السنة).",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المدى الفصلي للإشعاع الشمسي (kWh/m²/day)"
    },
    {
        "short_name": "Sol_JanMn",
        "full_name": "Sol_January_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر يناير.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر يناير (kWh/m²/day)"
    },
    {
        "short_name": "Sol_FebMn",
        "full_name": "Sol_February_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر فبراير.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر فبراير (kWh/m²/day)"
    },
    {
        "short_name": "Sol_MarMn",
        "full_name": "Sol_March_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر مارس.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر مارس (kWh/m²/day)"
    },
    {
        "short_name": "Sol_AprMn",
        "full_name": "Sol_April_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر أبريل.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر أبريل (kWh/m²/day)"
    },
    {
        "short_name": "Sol_MayMn",
        "full_name": "Sol_May_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر مايو.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر مايو (kWh/m²/day)"
    },
    {
        "short_name": "Sol_JunMn",
        "full_name": "Sol_June_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر يونيو.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر يونيو (kWh/m²/day)"
    },
    {
        "short_name": "Sol_JulMn",
        "full_name": "Sol_July_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر يوليو.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر يوليو (kWh/m²/day)"
    },
    {
        "short_name": "Sol_AugMn",
        "full_name": "Sol_August_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر أغسطس.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر أغسطس (kWh/m²/day)"
    },
    {
        "short_name": "Sol_SepMn",
        "full_name": "Sol_September_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر سبتمبر.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر سبتمبر (kWh/m²/day)"
    },
    {
        "short_name": "Sol_OctMn",
        "full_name": "Sol_October_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر أكتوبر.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر أكتوبر (kWh/m²/day)"
    },
    {
        "short_name": "Sol_NovMn",
        "full_name": "Sol_November_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر نوفمبر.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر نوفمبر (kWh/m²/day)"
    },
    {
        "short_name": "Sol_DecMn",
        "full_name": "Sol_December_Mean",
        "module_code": "08_Solar_Radiation",
        "module_name": "08_Solar_Radiation (الإشعاع الشمسي)",
        "desc_ar": u"المعدل اليومي للإشعاع الشمسي الكلي الساقط على السطح الأفقي لشهر ديسمبر.",
        "unit": u"kWh/m²/day",
        "map_title": u"خريطة المعدل اليومي للإشعاع الشمسي لشهر ديسمبر (kWh/m²/day)"
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
        "short_name": "UV_MonMean",
        "full_name": "UV_Month_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (مؤشر الأشعة فوق البنفسجية)",
        "desc_ar": u"المتوسط الشهري لمؤشر الأشعة فوق البنفسجية في سماء صافية (متوسط الـ 12 شهراً).",
        "unit": u"Index",
        "map_title": u"خريطة المتوسط الشهري لمؤشر الأشعة فوق البنفسجية"
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
    {
        "short_name": "UV_SeaRng",
        "full_name": "UV_Seasonal_Range",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"المدى الفصلي لمؤشر الأشعة فوق البنفسجية (الفارق بين فصول السنة).",
        "unit": u"مؤشر (Index)",
        "map_title": u"خريطة المدى الفصلي لمؤشر الأشعة فوق البنفسجية"
    },
    {
        "short_name": "UV_JanMean",
        "full_name": "UV_January_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر يناير وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر يناير"
    },
    {
        "short_name": "UV_FebMean",
        "full_name": "UV_February_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر فبراير وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر فبراير"
    },
    {
        "short_name": "UV_MarMean",
        "full_name": "UV_March_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر مارس وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر مارس"
    },
    {
        "short_name": "UV_AprMean",
        "full_name": "UV_April_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر أبريل وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر أبريل"
    },
    {
        "short_name": "UV_MayMean",
        "full_name": "UV_May_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر مايو وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر مايو"
    },
    {
        "short_name": "UV_JunMean",
        "full_name": "UV_June_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر يونيو وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر يونيو"
    },
    {
        "short_name": "UV_JulMean",
        "full_name": "UV_July_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر يوليو وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر يوليو"
    },
    {
        "short_name": "UV_AugMean",
        "full_name": "UV_August_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر أغسطس وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر أغسطس"
    },
    {
        "short_name": "UV_SepMean",
        "full_name": "UV_September_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر سبتمبر وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر سبتمبر"
    },
    {
        "short_name": "UV_OctMean",
        "full_name": "UV_October_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر أكتوبر وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر أكتوبر"
    },
    {
        "short_name": "UV_NovMean",
        "full_name": "UV_November_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر نوفمبر وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر نوفمبر"
    },
    {
        "short_name": "UV_DecMean",
        "full_name": "UV_December_Mean",
        "module_code": "09_UV_Index",
        "module_name": "09_UV_Index (الأشعة فوق البنفسجية)",
        "desc_ar": u"متوسط مؤشر الأشعة فوق البنفسجية القصوى لشهر ديسمبر وفق معيار WHO.",
        "unit": u"مؤشر (0-16+)",
        "map_title": u"خريطة متوسط مؤشر الأشعة فوق البنفسجية لشهر ديسمبر"
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
        "short_name": "Cld_MonMea",
        "full_name": "Cld_Month_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المتوسط الشهري لكمية الغطاء السحابي الكلي (متوسط الـ 12 شهراً).",
        "unit": u"%",
        "map_title": u"خريطة المتوسط الشهري للغطاء السحابي (%)"
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
    {
        "short_name": "Cld_SeaRng",
        "full_name": "Cld_Seasonal_Range",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"المدى الفصلي للغطاء السحابي (الفارق بين أعلى فصول السنة غيوماً وأصفاها).",
        "unit": u"%",
        "map_title": u"خريطة المدى الفصلي للغطاء السحابي (%)"
    },
    {
        "short_name": "Cld_JanMn",
        "full_name": "Cld_January_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر يناير.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر يناير (%)"
    },
    {
        "short_name": "Cld_FebMn",
        "full_name": "Cld_February_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر فبراير.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر فبراير (%)"
    },
    {
        "short_name": "Cld_MarMn",
        "full_name": "Cld_March_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر مارس.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر مارس (%)"
    },
    {
        "short_name": "Cld_AprMn",
        "full_name": "Cld_April_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر أبريل.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر أبريل (%)"
    },
    {
        "short_name": "Cld_MayMn",
        "full_name": "Cld_May_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر مايو.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر مايو (%)"
    },
    {
        "short_name": "Cld_JunMn",
        "full_name": "Cld_June_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر يونيو.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر يونيو (%)"
    },
    {
        "short_name": "Cld_JulMn",
        "full_name": "Cld_July_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر يوليو.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر يوليو (%)"
    },
    {
        "short_name": "Cld_AugMn",
        "full_name": "Cld_August_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر أغسطس.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر أغسطس (%)"
    },
    {
        "short_name": "Cld_SepMn",
        "full_name": "Cld_September_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر سبتمبر.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر سبتمبر (%)"
    },
    {
        "short_name": "Cld_OctMn",
        "full_name": "Cld_October_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر أكتوبر.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر أكتوبر (%)"
    },
    {
        "short_name": "Cld_NovMn",
        "full_name": "Cld_November_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر نوفمبر.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر نوفمبر (%)"
    },
    {
        "short_name": "Cld_DecMn",
        "full_name": "Cld_December_Mean",
        "module_code": "10_Cloud_Cover",
        "module_name": "10_Cloud_Cover (الغطاء السحابي)",
        "desc_ar": u"متوسط نسبة الغطاء السحابي الكلي للسماء لشهر ديسمبر.",
        "unit": u"%",
        "map_title": u"خريطة متوسط الغطاء السحابي لشهر ديسمبر (%)"
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
        "short_name": "ET_MonMean",
        "full_name": "ET_Month_Mean",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر-نتح المرجعي)",
        "desc_ar": u"المعدل الشهري للبخر-نتح المرجعي المحسوب بطريقة هارجريفز (متوسط الشهور = المجموع السنوي / 12).",
        "unit": u"mm/month",
        "map_title": u"خريطة المتوسط الشهري للبخر والنتح المرجعي (mm/month)"
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
    {
        "short_name": "ET_JanTot",
        "full_name": "ET_January_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر يناير بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر يناير (ملم/شهر)"
    },
    {
        "short_name": "ET_FebTot",
        "full_name": "ET_February_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر فبراير بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر فبراير (ملم/شهر)"
    },
    {
        "short_name": "ET_MarTot",
        "full_name": "ET_March_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر مارس بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر مارس (ملم/شهر)"
    },
    {
        "short_name": "ET_AprTot",
        "full_name": "ET_April_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر أبريل بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر أبريل (ملم/شهر)"
    },
    {
        "short_name": "ET_MayTot",
        "full_name": "ET_May_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر مايو بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر مايو (ملم/شهر)"
    },
    {
        "short_name": "ET_JunTot",
        "full_name": "ET_June_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر يونيو بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر يونيو (ملم/شهر)"
    },
    {
        "short_name": "ET_JulTot",
        "full_name": "ET_July_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر يوليو بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر يوليو (ملم/شهر)"
    },
    {
        "short_name": "ET_AugTot",
        "full_name": "ET_August_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر أغسطس بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر أغسطس (ملم/شهر)"
    },
    {
        "short_name": "ET_SepTot",
        "full_name": "ET_September_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر سبتمبر بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر سبتمبر (ملم/شهر)"
    },
    {
        "short_name": "ET_OctTot",
        "full_name": "ET_October_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر أكتوبر بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر أكتوبر (ملم/شهر)"
    },
    {
        "short_name": "ET_NovTot",
        "full_name": "ET_November_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر نوفمبر بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر نوفمبر (ملم/شهر)"
    },
    {
        "short_name": "ET_DecTot",
        "full_name": "ET_December_Total",
        "module_code": "14_Evapotranspiration",
        "module_name": "14_Evapotranspiration (البخر والنتح)",
        "desc_ar": u"متوسط مجموع البخر والنتح المرجعي الكامن لشهر ديسمبر بطريقة هارجريفز-ساماني FAO-56.",
        "unit": u"ملم/شهر (mm/month)",
        "map_title": u"خريطة مجموع البخر والنتح لشهر ديسمبر (ملم/شهر)"
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
        "count": 23,
        "unit": u"°C",
        "method": u"NASA POWER T2M, T2M_MAX, T2M_MIN / WMO Climatological Normals"
    },
    {
        "num": "02",
        "name_en": "02_Precipitation",
        "name_ar": u"الأمطار والتساقط",
        "folder": "02_Precipitation",
        "fc": "02_Precipitation",
        "count": 20,
        "unit": u"mm",
        "method": u"NASA POWER PRECTOTCORR / Annual, Seasonal Totals & Ranges"
    },
    {
        "num": "03",
        "name_en": "03_Sea_Level_Pressure",
        "name_ar": u"ضغط مستوى سطح البحر",
        "folder": "03_Sea_Level_Pressure",
        "fc": "03_Sea_Level_Pressure",
        "count": 19,
        "unit": u"hPa / mbar",
        "method": u"NASA POWER SLP / Reduced to Standard Mean Sea Level"
    },
    {
        "num": "04",
        "name_en": "04_Surface_Pressure",
        "name_ar": u"الضغط السطحي الفعلي",
        "folder": "04_Surface_Pressure",
        "fc": "04_Surface_Pressure",
        "count": 19,
        "unit": u"hPa / mbar",
        "method": u"NASA POWER PS / Actual Local Topographic Station Pressure"
    },
    {
        "num": "05",
        "name_en": "05_Wind",
        "name_ar": u"الرياح السطحية (سرعة واتجاه)",
        "folder": "05_Wind",
        "fc": "05_Wind",
        "count": 39,
        "unit": u"m/s, °",
        "method": u"NASA POWER WS10M, WD10M / Circular Mean Vector atan2"
    },
    {
        "num": "06",
        "name_en": "06_Relative_Humidity",
        "name_ar": u"الرطوبة النسبية",
        "folder": "06_Relative_Humidity",
        "fc": "06_Relative_Humidity",
        "count": 19,
        "unit": u"%",
        "method": u"NASA POWER RH2M / Climatological Relative Humidity at 2m"
    },
    {
        "num": "07",
        "name_en": "07_Dew_Point",
        "name_ar": u"نقطة الندى",
        "folder": "07_Dew_Point",
        "fc": "07_Dew_Point",
        "count": 19,
        "unit": u"°C",
        "method": u"NASA POWER T2MDEW / Dew Point Temperature at 2m"
    },
    {
        "num": "08",
        "name_en": "08_Solar_Radiation",
        "name_ar": u"الإشعاع الشمسي والطاقة",
        "folder": "08_Solar_Radiation",
        "fc": "08_Solar_Radiation",
        "count": 19,
        "unit": u"kWh/m²/day",
        "method": u"NASA POWER ALLSKY_SFC_SW_DWN / Daily Mean & Cumulative Annual"
    },
    {
        "num": "09",
        "name_en": "09_UV_Index",
        "name_ar": u"مؤشر الأشعة فوق البنفسجية",
        "folder": "09_UV_Index",
        "fc": "09_UV_Index",
        "count": 18,
        "unit": u"Index (0–16+)",
        "method": u"WHO / WMO Global Solar UV Index Standard"
    },
    {
        "num": "10",
        "name_en": "10_Cloud_Cover",
        "name_ar": u"الغطاء السحابي",
        "folder": "10_Cloud_Cover",
        "fc": "10_Cloud_Cover",
        "count": 18,
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
        "count": 21,
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
    
    section_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    font_section = Font(name="Segoe UI", size=11, bold=True, color="1F4E79")
    font_banner = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")

    # ----------------------------------------------------
    # Sheet 1: 01_عن_القاموس_About_Dictionary
    # ----------------------------------------------------
    ws0 = wb.active
    ws0.title = "01_عن_القاموس_About_Dictionary"
    ws0.views.sheetView[0].showGridLines = True

    # Title Banner (Row 1)
    ws0.merge_cells("A1:G1")
    tcell = ws0.cell(1, 1, u"القاموس المرجعي الشامل لحقول ومؤشرات أطلس المناخ الرقمي\nComprehensive Data Dictionary — NASA POWER Climate Atlas Engine")
    tcell.font = font_banner
    tcell.fill = header_fill
    tcell.alignment = align_center
    ws0.row_dimensions[1].height = 45

    # Section 1: Engine Profile (Row 3)
    ws0.merge_cells("A3:G3")
    s1 = ws0.cell(3, 1, u"1. بطاقة الهوية الفنية ومصدر البيانات المناخية (Technical Engine & Data Source Profile)")
    s1.font = font_section
    s1.fill = section_fill
    s1.alignment = align_right
    ws0.row_dimensions[3].height = 24

    engine_meta = [
        (u"اسم الأداة والمنصة البرمجية (Software Platform)", u"NASA POWER Climate Atlas Generator (ArcGIS 10.8 & Pro)", u"أداة المعالجة الكارتوجرافية والتحليل المناخي الآلي لمنظومة ArcGIS"),
        (u"مزود ونماذج البيانات المناخية (Data Source & Models)", u"NASA POWER API (CERES & MERRA-2 Gridded Reanalysis)", u"نماذج الاستشعار الفضائي وإعادة التحليل المناخي المعتمدة لوكالة ناسا"),
        (u"الفترة الزمنية المناخية القياسية (Climate Normal Period)", u"1996 – 2025 (سلسلة 30 عاماً تشمل المتوسطات الشهرية والفصلية والسنوية)", u"تطابق المعيار الدولي للمعدلات المناخية القياسية (WMO 30-Year Normal)"),
        (u"المعايير العلمية والمرجعيات الدولية (Scientific Standards)", u"WMO-No. 1203 / FAO-56 Irrigation / Steadman & ISO 7243", u"المنهجيات المعتمدة عالمياً لحساب الراحة الحرارية والقحولة والتبخر"),
        (u"التغطية الجغرافية ونظام الإحداثيات (Spatial Scope & Coordinate System)", u"Global Coverage (WGS 1984 / EPSG:4326)", u"تغطية عالمية شاملة بدقة شبكية منتظمة وقابلة للقص على أي دولة أو إقليم"),
        (u"إجمالي الحقول الموصوفة في القاموس (Total Defined Fields)", u"259 حقلاً معيارياً (247 مؤشراً مناخياً + 12 حقلاً إدارياً)", u"تشمل الحقول الإدارية والفيزيائية والفصلية ومتجهات الرياح والموديلات"),
        (u"عدد الحزم والعناصر المناخية (Climate Modules)", u"18 حزمة موديولية متكاملة (18 Complete Modules)", u"مجلدات راسترات وطبقات معالم بقاعدة البيانات الجغرافية متطابقة 1:1"),
    ]

    for idx, (prop, val, note) in enumerate(engine_meta, 4):
        ws0.row_dimensions[idx].height = 22
        r_fill = zebra_odd if idx % 2 == 0 else zebra_even
        c1 = ws0.cell(idx, 1, idx - 3)
        c1.alignment = align_center
        c1.font = font_bold
        c1.fill = r_fill
        c1.border = thin_border
        
        c2 = ws0.cell(idx, 2, prop)
        c2.alignment = align_right
        c2.font = font_bold
        c2.fill = r_fill
        c2.border = thin_border
        
        ws0.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=4)
        c3 = ws0.cell(idx, 3, val)
        c3.alignment = align_center
        c3.font = font_code
        c3.fill = r_fill
        c3.border = thin_border
        ws0.cell(idx, 4).border = thin_border
        ws0.cell(idx, 4).fill = r_fill
        
        ws0.merge_cells(start_row=idx, start_column=5, end_row=idx, end_column=7)
        c5 = ws0.cell(idx, 5, note)
        c5.alignment = align_right
        c5.font = font_regular
        c5.fill = r_fill
        c5.border = thin_border
        for c_i in (6, 7):
            ws0.cell(idx, c_i).border = thin_border
            ws0.cell(idx, c_i).fill = r_fill

    # Section 2: 18 Modules Summary Table (Row 12)
    ws0.merge_cells("A12:G12")
    s2 = ws0.cell(12, 1, u"2. هيكل حزم البيانات والموديلات الـ 18 المتطابقة 1:1 (The 18 Climate Modules Architecture)")
    s2.font = font_section
    s2.fill = section_fill
    s2.alignment = align_right
    ws0.row_dimensions[12].height = 24

    headers_sec2 = [
        u"م",
        u"كود الموديول في الأداة\nModule Code",
        u"الاسم باللغة العربية\nArabic Module Name",
        u"الاسم بالإنجليزية\nEnglish Module Name",
        u"المؤشرات\nIndicators",
        u"الوحدة الرئيسية\nMain Unit",
        u"المنهجية والمعيار العلمي المعتمد\nScientific Methodology & Standards"
    ]
    ws0.row_dimensions[13].height = 28
    for col_idx, h_text in enumerate(headers_sec2, 1):
        c = ws0.cell(row=13, column=col_idx, value=h_text)
        c.font = font_header
        c.fill = summary_fill
        c.alignment = align_center
        c.border = thin_border

    for idx, mod in enumerate(MODULES_SUMMARY, 14):
        ws0.row_dimensions[idx].height = 22
        r_fill = zebra_odd if idx % 2 == 0 else zebra_even
        
        c1 = ws0.cell(idx, 1, mod["num"])
        c1.alignment = align_center
        c1.font = font_bold
        c1.fill = r_fill
        c1.border = thin_border
        
        c2 = ws0.cell(idx, 2, mod["folder"])
        c2.alignment = align_left
        c2.font = font_code
        c2.fill = r_fill
        c2.border = thin_border
        
        c3 = ws0.cell(idx, 3, mod["name_ar"])
        c3.alignment = align_right
        c3.font = font_bold
        c3.fill = r_fill
        c3.border = thin_border
        
        c4 = ws0.cell(idx, 4, mod["name_en"])
        c4.alignment = align_left
        c4.font = font_regular
        c4.fill = r_fill
        c4.border = thin_border
        
        c5 = ws0.cell(idx, 5, mod["count"])
        c5.alignment = align_center
        c5.font = font_bold
        c5.fill = r_fill
        c5.border = thin_border
        
        c6 = ws0.cell(idx, 6, mod["unit"])
        c6.alignment = align_center
        c6.font = font_unit
        c6.fill = r_fill
        c6.border = thin_border
        
        c7 = ws0.cell(idx, 7, mod["method"])
        c7.alignment = align_left
        c7.font = font_regular
        c7.fill = r_fill
        c7.border = thin_border

    # Section 3: Columns Guide (Row 33)
    ws0.merge_cells("A33:G33")
    s3 = ws0.cell(33, 1, u"3. دليل قراءة أعمدة القاموس المرجعي واستخدامها في نظم المعلومات الجغرافية (Field Dictionary Columns Guide)")
    s3.font = font_section
    s3.fill = section_fill
    s3.alignment = align_right
    ws0.row_dimensions[33].height = 24

    cols_meta = [
        (u"اسم الحقل المختصر (Short Field Name)", u"صيغة Shapefile / DBF (حتى 10 أحرف)", u"متوافق 100% مع طبقات الشيب فايل لمنع اقتطاع الأسماء وتشوهها عند التصدير."),
        (u"اسم الحقل الكامل (Full Field Name)", u"صيغة Geodatabase و NASA POWER API", u"الاسم المعياري الشامل المعتمد في قواعد البيانات الجغرافية (GDB) وبرمجية الأداة."),
        (u"الموديول / العنصر المناخي (Climate Module)", u"الحزمة المناخية (1 من 18 موديول)", u"يتطابق بنسبة 1:1 مع اسم مجلد الراستر واسم طبقة المعالم في قاعدة البيانات."),
        (u"الشرح والتوصيف العلمي (Scientific Description)", u"البيان الفيزيائي والمعادلة الرياضية", u"التوصيف الرياضي والفيزيائي الدقيق لكيفية حساب المؤشر وفترته الزمنية المعتمدة."),
        (u"وحدة القياس القياسية (Measurement Unit)", u"الوحدات الدولية المعتمدة (SI Units)", u"درجات مئوية (°C)، ملم، هيكتوباسكال (hPa)، م/ث، ميجاجول/م²، نسب مئوية (%)."),
        (u"اسم الخريطة المقترح (Suggested Map Title)", u"الصياغة الكارتوجرافية الاحترافية", u"العنوان الكارتوجرافي الرسمي المعتمد لوضعه في عنوان الخريطة ومفتاح المصطلحات (Legend)."),
    ]

    for idx, (prop, val, note) in enumerate(cols_meta, 34):
        ws0.row_dimensions[idx].height = 22
        r_fill = zebra_odd if idx % 2 == 0 else zebra_even
        c1 = ws0.cell(idx, 1, idx - 33)
        c1.alignment = align_center
        c1.font = font_bold
        c1.fill = r_fill
        c1.border = thin_border
        
        c2 = ws0.cell(idx, 2, prop)
        c2.alignment = align_right
        c2.font = font_bold
        c2.fill = r_fill
        c2.border = thin_border
        
        ws0.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=4)
        c3 = ws0.cell(idx, 3, val)
        c3.alignment = align_center
        c3.font = font_code
        c3.fill = r_fill
        c3.border = thin_border
        ws0.cell(idx, 4).border = thin_border
        ws0.cell(idx, 4).fill = r_fill
        
        ws0.merge_cells(start_row=idx, start_column=5, end_row=idx, end_column=7)
        c5 = ws0.cell(idx, 5, note)
        c5.alignment = align_right
        c5.font = font_regular
        c5.fill = r_fill
        c5.border = thin_border
        for c_i in (6, 7):
            ws0.cell(idx, c_i).border = thin_border
            ws0.cell(idx, c_i).fill = r_fill

    # Set column widths for Sheet 1
    col_widths_0 = {
        1: 6,   # م
        2: 32,  # Module / Property
        3: 28,  # Value / Code
        4: 28,  # Sub-value / English
        5: 14,  # Count
        6: 18,  # Unit
        7: 48   # Note / Method
    }
    for col_idx, width in col_widths_0.items():
        ws0.column_dimensions[get_column_letter(col_idx)].width = width

    # ----------------------------------------------------
    # Sheet 2: Climate Fields
    # ----------------------------------------------------
    ws1 = wb.create_sheet(title="Climate_Fields")
    
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

# NASA POWER & Open-Meteo Climate Atlas Generator
## منظومة مولد أطلس المناخ الشامل ومكتبة الستايلات الكارتوجرافية المعتمدة لبرنامجي ArcGIS Pro و ArcMap 10.8

[![Developer](https://img.shields.io/badge/Developer-Ahmad%20Ibrahim-1F4E79.svg?style=for-the-badge&logo=github)](https://github.com/ahmadibrahim4geo)
[![المطور](https://img.shields.io/badge/المطور-أحمد%20إبراهيم-2E75B6.svg?style=for-the-badge)](https://github.com/ahmadibrahim4geo)
[![ArcGIS Pro](https://img.shields.io/badge/ArcGIS%20Pro-3.x%20%7C%202.x-0079c1.svg)](https://pro.arcgis.com/)
[![ArcMap](https://img.shields.io/badge/ArcGIS%20Desktop-10.8%20%7C%2010.x-0079c1.svg)](https://desktop.arcgis.com/)
[![Python Version](https://img.shields.io/badge/Python-3.x%20%7C%202.7-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-NASA%20POWER%20%7C%20Open--Meteo-blue.svg)](https://power.larc.nasa.gov/)
[![Modular Architecture](https://img.shields.io/badge/Elements-18%20Modular%20Layers-darkgreen.svg)](#٣-العناصر-والمؤشرات-المناخية-الـ-18-الموديلية-والربط-الموحد-11-unified-mapping)

> **إعداد وتطوير:** **أحمد إبراهيم (Ahmad Ibrahim)**  
> **حساب المطور على GitHub:** [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)  
> **مستودع المشروع:** [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)

---

## 📌 الفهرس السريع | Quick Navigation
- [🇪🇬 دليل الاستخدام والتوثيق الشامل باللغة العربية](#-دليل-الاستخدام-والتوثيق-الشامل-باللغة-العربية)
  - [١. ما هي منظومة أطلس المناخ؟](#١-ما-هي-منظومة-أطلس-المناخ؟)
  - [٢. التوافقية المزدوجة التامة (ArcGIS Pro & ArcMap 10.8)](#٢-التوافقية-المزدوجة-التامة-arcgis-pro--arcmap-108)
  - [٣. العناصر والمؤشرات المناخية الـ 18 الموديلية والربط الموحد (1:1 Unified Mapping)](#٣-العناصر-والمؤشرات-المناخية-الـ-18-الموديلية-والربط-الموحد-11-unified-mapping)
  - [٤. نمطا التشغيل الرئيسيان (Online & Offline) وسلوك التخطي الذكي](#٤-نمطا-التشغيل-الرئيسيان-online--offline-وسلوك-التخطي-الذكي)
  - [٥. تقنية الضغط القوي فائق الأداء للراستر (Lossless LZW Block Tiling)](#٥-تقنية-الضغط-القوي-فائق-الأداء-للراستر-lossless-lzw-block-tiling)
  - [٦. المعالجة المكانية غير الهدامة والماسك وأسهم الرياح](#٦-المعالجة-المكانية-غير-الهدامة-والماسك-وأسهم-الرياح)
  - [٧. المنظومة الكارتوجرافية والستايلات المعتمدة](#٧-المنظومة-الكارتوجرافية-والستايلات-المعتمدة)
  - [٨. خطوات التثبيت والتشغيل خطوة بخطوة](#٨-خطوات-التثبيت-والتشغيل-خطوة-بخطوة)
- [🇬🇧 English Documentation](#-english-documentation)
  - [Overview & Architecture](#-overview--architecture)
  - [Dual Platform Support (ArcGIS Pro 3.x & Desktop 10.8)](#-dual-platform-support-arcgis-pro-3x--desktop-108)
  - [The 18 Modular Climate Layers & 1:1 Standardized Architecture](#-the-18-modular-climate-layers--11-standardized-architecture)
  - [Online Pipeline vs. Offline Precalculated Mode](#-online-pipeline-vs-offline-precalculated-mode)
  - [High-Efficiency Lossless Raster Compression](#-high-efficiency-lossless-raster-compression)
  - [Non-Destructive Spatial Masking & Vector Dynamics](#-non-destructive-spatial-masking--vector-dynamics)
  - [Cartographic Mega System](#-cartographic-mega-system)
  - [Getting Started & Verification](#-getting-started--verification)

---

# 🇪🇬 دليل الاستخدام والتوثيق الشامل باللغة العربية

### ١. ما هي منظومة أطلس المناخ؟
منظومة **NASA POWER & Open-Meteo Climate Atlas Generator** هي حزمة برمجية جغرافية متقدمة ومفتوحة المصدر صُممت وهُندست لتوفير حل متكامل لأتمتة إنشاء الأطالس المناخية الإقليمية والوطنية، واستخراج وتحليل البيانات متعددة العقود ونمذجة أسطح الراستر المناخية بدقة علمية وفيزيائية فائقة.

تتكون المنظومة من أداتين رئيسيتين تعملان بتناغم كامل:
1. **صندوق أدوات معالم المناخ (`POWER_Climate_Atlas_Generator_10_8.pyt`)**: أداة الواجهة الرسومية التفاعلية (Geoprocessing Tool) لإدارة الاتصال السحابي، وسحب السلاسل الزمنية، وتطبيق ضوابط الجودة (QA/QC)، وحساب كافة المؤشرات المناخية وتوليد الطبقات النقطية وقواعد البيانات الجغرافية (`File Geodatabase`).
2. **محرك الأطلس الراستري (`raster_atlas_generator.py`)**: المحرك الحسابي المتقدم للاستيفاء المكاني للأسطح المناخية المستمرة (Spatial Interpolation via IDW, Kriging, Spline, Natural Neighbor)، والتقطيع على الماسك، وبناء خطوط الضغط المتساوي (Isobars)، وحساب شبكات متجهات الرياح، وتطبيق أحدث تقنيات الضغط بدون أي فقدان للبيانات.

---

### ٢. التوافقية المزدوجة التامة (ArcGIS Pro & ArcMap 10.8)
تمت ترقية المنظومة بالكامل لتعمل بكفاءة مطلقة واستقرار تام عبر بيئتي عمل Esri:
* **ArcGIS Pro (إصدارات 2.x و 3.x)** تحت بيئة **Python 3**:
  - معالجة متقدمة لترميز النصوص بدون أخطاء `unicode()` أو `str.decode()`.
  - توافق كامل لمصفوفات `dict.values()` ككائنات قابلة للتكرار (Iterators/Views).
  - حماية كاملة لجدول المحتويات (TOC / Contents Pane) لمنع اختفاء الطبقات أثناء المعالجة أو تشغيل الأوفلاين.
* **ArcGIS Desktop 10.8 (ArcMap)** تحت بيئة **Python 2.7**:
  - دعم كامل لبيئة ArcObjects ومكتبات COM المعمارية القياسية.
  - نوافذ التقويم المرئي التفاعلي المدمجة (`Tkinter GUI`).
  - مصنفات الإكسيل المهيكلة بصيغة `.xls` مع دعم كامل للترميز العربي (`UTF-8 BOM`).

---

### ٣. العناصر والمؤشرات المناخية الـ 18 الموديلية والربط الموحد (1:1 Unified Mapping)
تمت إعادة هيكلة المنظومة بالكامل لتعتمد معيار **الربط الموحد بنسبة 1:1** بين اسم العنصر في واجهة الأداة (`Climate Modules & Models`)، واسم طبقة المعالم داخل قاعدة البيانات (`Feature Class`)، واسم المجلد المخصص لمخرجات الراستر (`Output Raster Folder`).

تتكون المنظومة من **18 عنصراً وموديولاً مناخياً وبيومناخياً مستقلاً**:

| رقم | اسم العنصر في واجهة الأداة | اسم طبقة المعالم (Feature Class) | اسم مجلد الراستر (Raster Folder) | عدد المؤشرات | تفصيل المؤشرات (سنوي/فصلي + شهري) | الوحدة الفيزيائية |
|:---:|---|---|---|:---:|---|:---:|
| **01** | `Temperature` | `01_Temperature` | `01_Temperature` | **23** | 11 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | °C |
| **02** | `Precipitation` | `02_Precipitation` | `02_Precipitation` | **20** | 8 سنوي وفصلي + 12 شهري تراكمي | mm, mm/month |
| **03** | `Sea Level Pressure` | `03_Sea_Level_Pressure` | `03_Sea_Level_Pressure` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | hPa / mbar |
| **04** | `Surface Pressure` | `04_Surface_Pressure` | `04_Surface_Pressure` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | hPa / mbar |
| **05** | `Wind` | `05_Wind` | `05_Wind` | **39** | 15 سنوي وفصلي ومعدل شهري + 24 شهري (سرعة + اتجاه) | m/s, degrees (°) |
| **06** | `Relative Humidity` | `06_Relative_Humidity` | `06_Relative_Humidity` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | % |
| **07** | `Dew Point` | `07_Dew_Point` | `07_Dew_Point` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | °C |
| **08** | `Solar Radiation` | `08_Solar_Radiation` | `08_Solar_Radiation` | **20** | 8 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | kWh/m²/day |
| **09** | `UV Index` | `09_UV_Index` | `09_UV_Index` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | مؤشر (0–16+) |
| **10** | `Cloud Cover` | `10_Cloud_Cover` | `10_Cloud_Cover` | **19** | 7 سنوي وفصلي ومعدل شهري + 12 شهري مناخي | % |
| **11** | `Heat Index` | `11_Heat_Index` | `11_Heat_Index` | **5** | 5 مؤشرات سنوية وفصلية ومجمعة | °C |
| **12** | `Wind Chill` | `12_Wind_Chill` | `12_Wind_Chill` | **2** | مؤشران شتويان للبرودة الريحية | °C |
| **13** | `De Martonne Aridity` | `13_De_Martonne_Aridity` | `13_De_Martonne_Aridity` | **1** | مؤشر جفاف سنوي لدي مارتون | مؤشر لا بُعدي |
| **14** | `Evapotranspiration` | `14_Evapotranspiration` | `14_Evapotranspiration` | **22** | 10 سنوي وفصلي ومعدل شهري + 12 شهري FAO-56 | mm, mm/month |
| **15** | `UNEP Aridity` | `15_UNEP_Aridity` | `15_UNEP_Aridity` | **1** | مؤشر قحولة سنوي لبرنامج الأمم المتحدة | نسبة |
| **16** | `Water Deficit` | `16_Water_Deficit` | `16_Water_Deficit` | **1** | عجز وموازنة مائية سنوية | mm/year |
| **17** | `Dry Months` | `17_Dry_Months` | `17_Dry_Months` | **1** | عدد شهور الجفاف البيولوجي | شهور (0–12) |
| **18** | `Trends & Baseline Anomalies` | `18_Trends_And_Anomalies` | `18_Trends_And_Anomalies` | **9** | اتجاهات وشذوذ خط الأساس 1991–2020 | °C/decade, mm/decade, % |
| **الإجمالي** | **18 عنصراً وموديولاً** | **18 Feature Class** | **18 مجلد راستر** | **258** | **114 مؤشراً سنوياً وفصلياً ومعدلاً شهرياً + 144 متوسطاً شهرياً** | — |

---

#### 🌟 تفصيل المؤشرات المستحدثة والموحدة:

##### 1. البخر والنتح (Evapotranspiration - ET):
* **التسمية والرمز**: تم اعتماد مسمى **البخر والنتح (Evapotranspiration)** واختصاره داخل الأداة بـ **`ET`**، ويُنشأ في مجلد وطبقة مستقلة: `14_Evapotranspiration`.
* **الأساس العلمي والمنهجية**: يعتمد المؤشر كلياً على معادلة **هارجريفز-ساماني (Hargreaves & Samani, 1985)** والمعتمدة رسمياً لدى منظمة الأغذية والزراعة للأمم المتحدة (**FAO**) في الدليل الإرشادي للري والصرف رقم 56 (**FAO Irrigation and Drainage Paper No. 56**)، وهي الصيغة المثلى لحساب البخر والنتح المرجعي ($ET_o$) من بيانات درجات الحرارة والإشعاع الشمسي الفلكي خارج الغلاف الجوي ($R_a$):
  $$ET_o = 0.0023 \cdot R_a \cdot (T_{mean} + 17.8) \cdot \sqrt{T_{max} - T_{min}} \cdot \text{Days}$$
* **المؤشرات الثمانية على المستويين السنوي والفصلي**:
  1. `ET_Annual_Total`: المجموع السنوي للبخر والنتح (ملم/سنة).
  2. `ET_Annual_Mean`: المتوسط الشهري السنوي للبخر والنتح (ملم/شهر).
  3. `ET_Annual_Range`: المدى الشهري السنوي للبخر والنتح (أعلى شهر ملم - أدنى شهر ملم).
  4. `ET_Seasonal_Range`: المدى الفصلي للبخر والنتح (أعلى فصل ملم - أدنى فصل ملم).
  5. `ET_Winter_Total`: مجموع البخر والنتح لفصل الشتاء (DJF) (ملم).
  6. `ET_Spring_Total`: مجموع البخر والنتح لفصل الربيع (MAM) (ملم).
  7. `ET_Summer_Total`: مجموع البخر والنتح لفصل الصيف (JJA) (ملم).
  8. `ET_Autumn_Total`: مجموع البخر والنتح لفصل الخريف (SON) (ملم).
  * **التوافق العكسي**: يتم تصدير الحقل الرديف `PET_Hargreaves_Annual` تلقائياً لضمان استمرارية تشغيل أي مشاريع أو أدوات تحليلية سابقة.

##### 2. استقلال نقطة الندى (Dew Point):
* تم إفراد **نقطة الندى** كعنصر رئيسي مستقل تماماً تحت الرقم **07** (`07_Dew_Point`) بـ 6 مؤشرات متكاملة:
  - `Td_Annual_Mean`: المتوسط السنوي لنقطة الندى (°C).
  - `Td_Winter_Mean`: متوسط نقطة الندى لشتاء (DJF).
  - `Td_Spring_Mean`: متوسط نقطة الندى لربيع (MAM).
  - `Td_Summer_Mean`: متوسط نقطة الندى لصيف (JJA).
  - `Td_Autumn_Mean`: متوسط نقطة الندى لخريف (SON).
  - `Td_Annual_Range`: المدى السنوي لنقطة الندى (°C).

##### 3. تعزيز مؤشرات الأمطار (Precipitation):
* إضافة المدى السنوي `R_Annual_Range` والمدى الفصلي `R_Seasonal_Range` لمراقبة التفاوت الفصلي والشهري في الهطول مع إزالة الحقول القديمة غير المتوافقة مع نمط الشهر.

##### 4. المتوسطات المناخية الشهرية المعيارية (12 شهراً لكل عنصر) وهيكلية الإكسيل المزدوجة:
* **توسعة شاملة لقواعد البيانات**: تم دعم حساب وتخزين **144 مؤشراً شهرياً مناخياً** يغطي الشهور الـ 12 (يناير – ديسمبر) عبر العناصر المناخية الـ 11 الرئيسية:
  - **الحرارة**: متوسط درجة حرارة الهواء لكل شهر (`T_January_Mean` .. `T_December_Mean`) (°C).
  - **الأمطار**: متوسط مجموع الأمطار التراكمي لكل شهر عبر السنوات (`R_January_Mean` .. `R_December_Mean`) (ملم/شهر).
  - **ضغط مستوى سطح البحر**: متوسط الضغط المصحح لمستوى البحر (`PSL_January_Mean` .. `PSL_December_Mean`) (hPa).
  - **الضغط السطحي الفعلي**: متوسط الضغط عند منسوب المحطة (`PS_January_Mean` .. `PS_December_Mean`) (hPa).
  - **سرعة الرياح**: متوسط سرعة الرياح على ارتفاع 10 م (`W_Spd_January_Mean` .. `W_Spd_December_Mean`) (م/ث).
  - **اتجاه الرياح السائد**: الاتجاه السائد الدائري المتجهي (`W_Dir_January_Mean` .. `W_Dir_December_Mean`) باستخدام خوارزمية المتجهات الدائرية `atan2(mean_sin, mean_cos)`.
  - **الرطوبة النسبية**: متوسط الرطوبة عند 2 م (`RH_January_Mean` .. `RH_December_Mean`) (%).
  - **نقطة الندى**: متوسط درجة حرارة نقطة الندى (`Td_January_Mean` .. `Td_December_Mean`) (°C).
  - **الإشعاع الشمسي**: المعدل اليومي للإشعاع الساقط على السطح الأفقي (`Sol_January_Mean` .. `Sol_December_Mean`) (kWh/m²/day).
  - **مؤشر UV**: متوسط مؤشر الأشعة فوق البنفسجية القصوى (`UV_January_Mean` .. `UV_December_Mean`) وفق معيار منظمة الصحة العالمية.
  - **الغطاء السحابي**: متوسط نسبة الغطاء السحابي (`Cld_January_Mean` .. `Cld_December_Mean`) (%).
  - **البخر والنتح (ET)**: مجموع البخر والنتح الكامن لكل شهر وفق صيغة FAO-56 Hargreaves-Samani (`ET_January_Total` .. `ET_December_Total`) (ملم/شهر).
* **هيكلة مصنفات الإكسيل المهنية المزدوجة (Dual-Sheet Workbooks)**:
  - تحتوي كافة ملفات الإكسيل الخاصة بالعناصر المناخية (`00_Tables_And_Reports\*.xls`) على صفحتين مستقلتين:
    1. **صفحة `Data`**: تضم المؤشرات السنوية والفصلية والمدى والمتغيرات المشتقة.
    2. **صفحة `Month`**: تضم المؤشرات الشهرية الـ 12 المكتملة عبر كافة محطات ونقاط الرصد.
* **حفظ الأرشيف الخام الزمني المكتمل**: يتم حفظ وتحديث السلسلة الزمنية الشهرية الكاملة لـ 30 عاماً (1996–2025) لكل المتغيرات في ملف JSON محلي دائم (`Egypt_Monthly_Raw_1996_2025.json`) لتسريع المعالجة وإتاحة التحليلات المتقدمة بدون الحاجة لإعادة التحميل.
* **ضبط التوليد الكارتوجرافي للراستر**: تلتزم المنظومة بتوليد أسطح الراستر للاستيفاء المكاني للمؤشرات السنوية والفصلية والبيومناخية المعتمدة، مع الاحتفاظ التام بكافة البيانات الشهرية داخل قواعد البيانات الجغرافية وجداول الإكسيل المهيكلة.

---

### ٤. نمطا التشغيل الرئيسيان (Online & Offline) وسلوك التخطي الذكي

#### أ. نمط الاتصال السحابي المباشر (`Download & Generate Atlas`)
- يبدأ من نقاط جغرافية خام أو محطات رصد محددة.
- يتصل بالخوادم العالمية (NASA POWER API لبيانات الأقمار الصناعية و MERRA-2، و Open-Meteo ERA5-Land بدقة 9 كم).
- يقوم بإجراء فحص الجودة وملء الفجوات البيانية آلياً وتحويل علامات الفقدان `-999` إلى قيم خالية، ثم حساب كافة المؤشرات الرياضية.
- ينشئ قاعدة البيانات الجغرافية `Climate_Database.gdb` ويصدر كافة المعالم والخرائط.

#### ب. نمط الاستيفاء المحلي التام للأوفلاين (`Interpolate & Map Existing Data`)
- **بدون الحاجة لأي اتصال بالإنترنت نهائياً**.
- يستقبل طبقة نقاط محسوبة مسبقاً (Feature Layer أو Shapefile أو قاعدة بيانات سابقة).
- **سلوك التخطي الذكي وحماية البيانات**:
  - إذا كانت قاعدة البيانات أو المخرجات موجودة في المجلد، تتخطى الأداة إعادة إنشاء الداتابيز من الصفر ولا تقوم بمسحها أو الكتابة العشوائية فوقها.
  - **حماية طبقات المستخدم في جدول المحتويات (TOC)**: تم إلغاء كافة عمليات الحذف البرمجي للطبقات المؤقتة التي كانت تتسبب في اختفاء الطبقات من واجهة ArcGIS Pro / ArcMap. تظل الطبقات مستقرة وظاهرة في الخريطة دون انقطاع.
  - التعرف التلقائي الذكي على الحقول (Automatic Field Discovery) لتفعيل الموديولات المناخية فورياً بمجرد اختيار الطبقة.

---

### ٥. تقنية الضغط القوي فائق الأداء للراستر (Lossless LZW Block Tiling)
أحد أهم التحديثات المحورية في المنظومة هو تحسين وضبط خوارزميات تخزين راستر الاستيفاء المكاني:
* **المشكلة السابقة:** كانت أسطح الراستر الناتجة عن الاستيفاء والقص تُحفظ بصيغ تستهلك مساحات تخزين كبيرة، وتثقل حركة الخريطة داخل برامج نظم المعلومات الجغرافية.
* **الحل الهندسي المطبق:**
  - تم اعتماد أسلوب النسخ التخطيطي عبر `arcpy.management.CopyRaster`.
  - تطبيق ضغط **LZW** القوي وتفعيل تقسيم البلوكات الشبكية بحجم **`128x128` خلية** (`tileSize="128 128"`).
  - تعطيل الأهرامات المؤقتة (`arcpy.env.pyramid = "NONE"`) أثناء مراحل التوليد والقص.
* **النتائج المعيارية للاختبار العلمي:**
  - **انخفاض فوري في حجم ملفات الراستر بنسبة 34.8%** مقارنة بالأسطح غير المضغوطة.
  - **عدم فقدان أي بيانات نهائياً (100% Bit-for-Bit Lossless)**: تم التحقق عبر فحص مصفوفات NumPy الرياضية لخلايا الراستر قبل وبعد الضغط، وسجل أقصى فارق رقمي قيمة صفرية مطلقة (`max_diff = 0.000000000000000`)، مما يعني الحفاظ الكامل على دقة الأرقام العشرية والكسور والخصائص الفيزيائية للخلايا.

---

### ٦. المعالجة المكانية غير الهدامة والماسك وأسهم الرياح

#### أ. مبدأ عدم قص النقاط (Non-Destructive Points Processing)
- **قاعدة صارمة ومؤكدة**: طبقة النقاط المدخلة أو المحسوبة **لا يتم قصها نهائياً** بواسطة مضلع الماسك (`Study Area Mask`). تظل طبقة النقاط محتفظة بكامل معالمها خارج وداخل النطاق لضمان إمكانية إعادة استخدامها، وتدقيق حسابات الجوار المكاني، والحفاظ على سلامة محطات الرصد الإقليمية.
- **الطبقات التي تخضع للقص بواسطة الماسك فقط هي**:
  1. أسطح الراستر الناتجة عن الاستيفاء المكاني (`Continuous Interpolated Rasters`).
  2. خطوط تساوي الضغط الجوي (`Isobars Contours`).
  3. طبقة شبكة أسهم الرياح المتجهة (`Wind Vector Arrows Grid`).

#### ب. شبكة أسهم واتجاهات الرياح الديناميكية
- تنتج الأداة راسترين مستمرين: أحدهما لسرعة الرياح (`Wind Speed`) والآخر للاتجاه السائد المرجح بالدرجات الزاوية (`Wind Direction Azimuth`).
- تقوم الأداة بإنشاء شبكة نقاط منتظمة متباعدة بناءً على معامل حجم الخلية المخصص (`Wind_Factor_Cell_Size`)، ثم تسقط قيم السرعة وزوايا الاتجاه عليها، وتطبق عليها مضلع الماسك، لتمكين العرض الكارتوجرافي المتكامل لأسهم حركة الرياح فوق خرائط سرعة الرياح.

---

### ٧. المنظومة الكارتوجرافية والستايلات ودليل التصنيف المعتمد
* **أ. مكتبة الستايلات العلمية المعتمدة (مجلد `style/`)**:
  - **125 ستايلاً كارتوجرافياً علمياً** يغطي كافة المجالات المناخية، مسنداً للمراجع الدولية (WMO, IPCC AR6, NOAA NCEI, ECMWF ERA5, WHO).
  - **2,250 تدرجاً لونياً (Color Ramps)** تدعم التصنيف من 3 إلى 11 فئة، بنمطين رئيسيين:
    - نمط **`[Stepped]`**: فئات لونية مصمتة ومنفصلة لخرائط الراستر المصنفة (`Classified`).
    - نمط **`[Smooth]`**: تدرجات لونية انسيابية متصلة لخرائط الراستر الممتدة (`Stretched`).
  - مصنف الإكسيل الماستر المرئي الملون (`NASA_POWER_Climate_Atlas_Master_Styles.xlsx`).
  - قاموس الحقول والوحدات المعتمد باللغتين العربية والإنجليزية (`Fields_AR_EN_Units.xlsx`).

* **ب. دليل التصنيف الكارتوجرافي الشامل للأطلس (`Climate_Atlas_Classification_Guide.xlsx`)**:
  تنتج الأداة تلقائياً دليلاً معيارياً فائق الدقة في مجلد `00_Tables_And_Reports` والمسار الجذري، يتضمن:
  1. **مستويات الفئات الأربعة القياسية**: أوراق عمل مخصصة لـ (3 فئات - تنفيذي)، (5 فئات - المعيار الذهبي)، (7 فئات - أكاديمي تفصيلي)، (9 فئات - مدى واسع مكثف).
  2. **خوارزمية إنقاذ الفئات المنهارة (Degenerate Class Recovery Engine)**:
     - عند تشغيل تصنيف الفئات المتساوية (Equal Interval) بأرقام صحيحة في ArcMap للراسترات ذات المدى الضيق، يُسفر التقريب الميكانيكي أحياناً عن فئات شاذة أو منهارة مثل (`27 - 27°` أو `6 - 6`).
     - تقوم المنظومة تلقائياً بكشف هذه الفئات وإعادة موازنة السلسلة بالكامل من الأسفل إلى الأعلى بخطوة صحيحة منتظمة متساوية (درجتين أو أكثر: `20 - 21°`، `22 - 23°`، `24 - 25°`، `26 - 27°`، `28 - 29°`).
  3. **التوثيق المزدوج فائق الشفافية في نفس الخلية**:
     - لمنع تشتت الباحث، يُعرض في خلية الأرقام الصحيحة: **الحل الكارتوجرافي المتوازن الموصى به** يليه مباشرة بين قوسين **أصل أرك ماب الميكانيكي**، مثل:
       `26 - 27° (أصل أرك ماب: 27 - 27°)`
     - عندما تكون الفئة سليمة ومتطابقة أصلاً مع أرك ماب (مثل `22 - 25°`) تُعرض مباشرة دون أقواس إضافية.
  4. **عمود الكسور العشرية الدقيق (1 Decimal)**:
     - يوفر فواصل أرك ماب الحرفية بدقة `0.1` بجوار كل فئة، لتمكين الباحثين من المقارنة الرقمية أو استخدام الفئات الكسرية.
  5. **توحيد الرموز والوحدات الفيزيائية المعيارية**:
     - رمز الدرجة المئوية يظهر كرمز منفرد `°` في نهاية فئات الحرارة فقط دون تكرار ودون إلحاق حرف `C`، مع ضبط باقي الوحدات (`mm`، `%`، `hPa`، `m/s`، `°/dec`).

---

### ٨. خطوات التثبيت والتشغيل خطوة بخطوة

#### التشغيل داخل ArcGIS Pro:
1. افتح مشروعك في **ArcGIS Pro**.
2. من لوحة الكتالوج (**Catalog Pane**)، اضغط بزر الفأرة الأيمن على **Toolboxes** واختر **Add Toolbox**.
3. توجه لمجلد المشروع واختر الملف: `POWER_Climate_Atlas_Generator_10_8.pyt`.
4. افتح أداة **NASA POWER Climate Atlas Generator**، وحدد نمط التشغيل (Online أو Offline)، ثم حدد طبقة النقاط ومضلع منطقة الدراسة، واضغط **Run**.

#### التشغيل داخل ArcMap 10.8:
1. افتح نافذة **ArcToolbox**.
2. اضغط بزر الفأرة الأيمن واختر **Add Toolbox...** وحدد `POWER_Climate_Atlas_Generator_10_8.pyt`.
3. انقر نقراً مزدوجاً لفتح الأداة، واختر المعاملات، واضغط **OK**.

---

# 🇬🇧 English Documentation

An enterprise-grade, peer-reviewed Climate Atlas Generator and scientific spatial modeling suite engineered for **both ArcGIS Pro (3.x / 2.x, Python 3)** and **Esri ArcMap Desktop 10.8 (Python 2.7)**.

Developed by **Ahmad Ibrahim** ([@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)).  
Repository: [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator).

---

## 🌟 Overview & Architecture

The system automates the acquisition, quality control, climatological calculations, spatial interpolation, and standardized cartographic rendering of multi-decadal historical climate records and future projections directly inside Esri GIS environments.

### Core Components:
1. **`POWER_Climate_Atlas_Generator_10_8.pyt`**: Primary Python Toolbox interface managing data acquisition pipelines, calendar GUI dialogs, indicator modeling, and Geodatabase generation.
2. **`raster_atlas_generator.py`**: High-performance backend engine managing spatial interpolations (IDW, Kriging, Spline, Natural Neighbor), focal neighborhood smoothing, mask clipping, isobar contour generation, wind vector field modeling, and lossless LZW raster compression.

---

## ⚡ Dual Platform Support (ArcGIS Pro 3.x & Desktop 10.8)

Engineered with dual Python 2/3 cross-compatibility:
- **ArcGIS Pro**: Native Python 3 string and unicode handling, view-safe dictionary evaluation, and protection against Table of Contents (TOC) layer disappearance.
- **ArcMap 10.8**: Native Python 2.7 support, interactive Tkinter calendar modals, and backward-compatible `.xls` formatting via `xlwt` with full UTF-8 BOM encoding.

---

## 🗺️ The 18 Modular Climate Layers & 1:1 Standardized Architecture

The platform enforces a strict **1:1 unified naming convention** connecting UI parameters, geodatabase feature classes, and raster output folders across all **18 discrete thematic modules**:

| # | Parameter Name (UI) | Feature Class Name | Raster Folder | Indicators | Units |
|:---:|---|---|---|:---:|:---:|
| **01** | `Temperature` | `01_Temperature` | `01_Temperature` | 10 | °C |
| **02** | `Precipitation` | `02_Precipitation` | `02_Precipitation` | 8 | mm |
| **03** | `Sea Level Pressure` | `03_Sea_Level_Pressure` | `03_Sea_Level_Pressure` | 6 | hPa / mbar |
| **04** | `Surface Pressure` | `04_Surface_Pressure` | `04_Surface_Pressure` | 6 | hPa / mbar |
| **05** | `Wind` | `05_Wind` | `05_Wind` | 13 | m/s, degrees (°) |
| **06** | `Relative Humidity` | `06_Relative_Humidity` | `06_Relative_Humidity` | 6 | % |
| **07** | `Dew Point` | `07_Dew_Point` | `07_Dew_Point` | 6 | °C |
| **08** | `Solar Radiation` | `08_Solar_Radiation` | `08_Solar_Radiation` | 7 | kWh/m²/day, kWh/m²/year |
| **09** | `UV Index` | `09_UV_Index` | `09_UV_Index` | 6 | Index (0–15+) |
| **10** | `Cloud Cover` | `10_Cloud_Cover` | `10_Cloud_Cover` | 6 | % |
| **11** | `Heat Index` | `11_Heat_Index` | `11_Heat_Index` | 5 | °C |
| **12** | `Wind Chill` | `12_Wind_Chill` | `12_Wind_Chill` | 2 | °C |
| **13** | `De Martonne Aridity` | `13_De_Martonne_Aridity` | `13_De_Martonne_Aridity` | 1 | Dimensionless Index |
| **14** | `Evapotranspiration` | `14_Evapotranspiration` | `14_Evapotranspiration` | 8 | mm/year, mm/month, mm |
| **15** | `UNEP Aridity` | `15_UNEP_Aridity` | `15_UNEP_Aridity` | 1 | Ratio |
| **16** | `Water Deficit` | `16_Water_Deficit` | `16_Water_Deficit` | 1 | mm/year |
| **17** | `Dry Months` | `17_Dry_Months` | `17_Dry_Months` | 1 | Months (0–12) |
| **18** | `Trends & Baseline Anomalies` | `18_Trends_And_Anomalies` | `18_Trends_And_Anomalies` | 9 | °C/decade, mm/decade, % |

### Scientific Focus: Evapotranspiration (ET)
- **Methodological Origin**: Implements the globally recognized **FAO-56 Hargreaves-Samani method** (Hargreaves & Samani, 1985), estimating reference evapotranspiration ($ET_o$) using extraterrestrial solar radiation ($R_a$), mean temperature, and diurnal temperature range:
  $$ET_o = 0.0023 \cdot R_a \cdot (T_{mean} + 17.8) \cdot \sqrt{T_{max} - T_{min}} \cdot \text{Days}$$
- **8 Climatological & Seasonal Indicators**:
  - `ET_Annual_Total`: Total cumulative annual evapotranspiration (mm/year).
  - `ET_Annual_Mean`: Mean monthly evapotranspiration (mm/month).
  - `ET_Annual_Range`: Monthly range between peak and minimum ET months (mm/month).
  - `ET_Seasonal_Range`: Seasonal range between maximum and minimum season totals (mm).
  - `ET_Winter_Total` / `ET_Spring_Total` / `ET_Summer_Total` / `ET_Autumn_Total`: Seasonal accumulated totals (DJF, MAM, JJA, SON) (mm).
  - Full backward compatibility maintained via `PET_Hargreaves_Annual`.

---

## 🔄 Online Pipeline vs. Offline Precalculated Mode

### Online Pipeline (`Download & Generate Atlas`)
- Connects directly to **NASA POWER API** (satellite & MERRA-2 reanalysis) and **Open-Meteo API** (ERA5-Land ~9 km).
- Automatically converts `-999` sentinels to `None`, performs climatological gap filling, and builds the standardized `Climate_Database.gdb`.

### Offline Mode (`Interpolate & Map Existing Data`)
- **100% Offline execution**: No internet connection required.
- Automatically discovers existing fields, skipping database creation if it already exists.
- **TOC Integrity**: Eliminates intermediate layer deletion, ensuring user layers remain permanently visible in the ArcGIS Pro Contents pane / ArcMap Table of Contents.

---

## 💾 High-Efficiency Lossless Raster Compression

- Utilizes `arcpy.management.CopyRaster` with **LZW compression** and **`128x128` block tiling**.
- Suppresses intermediate pyramid overhead during pipeline processing (`arcpy.env.pyramid = "NONE"`).
- **Benchmark Performance**:
  - **34.8% reduction in raster disk storage footprint**.
  - **100% Bit-for-Bit Lossless Precision**: Verified via NumPy array difference testing (`max_diff = 0.000000000000000`). Floating-point scientific precision is preserved completely without loss or degradation of fractional values.

---

## 🎯 Non-Destructive Spatial Masking & Vector Dynamics

- **Points Preservation**: Point feature layers are **NEVER clipped** by the study area mask. All observation stations remain intact for subsequent spatial querying and statistical integrity.
- **Mask-Clipped Products**: Only spatial derivatives are clipped to the study boundary:
  1. Continuous raster surfaces (GeoTIFFs).
  2. Atmospheric pressure isobars (Contours).
  3. Directional wind vector arrows grid.
- **Wind Vector Dynamics**: Generates continuous wind speed and azimuth direction rasters, and extracts a regularized point grid with user-configurable arrow spacing (`Wind_Factor_Cell_Size`) rotated to flow angles.

---

## 🎨 Cartographic Mega System & Classification Guide

- **125 Scientific Styles** conforming to WMO, IPCC AR6, NOAA NCEI, and ECMWF standards.
- **2,250 Color Ramps** across 9 class tiers (3 to 11 classes) with `[Stepped]` and `[Smooth]` modes.
- Master Excel visual palette catalog: `NASA_POWER_Climate_Atlas_Master_Styles.xlsx`.
- Complete bilingual field dictionary and units reference: `Fields_AR_EN_Units.xlsx`.
- **Automated Cartographic Classification Guide (`Climate_Atlas_Classification_Guide.xlsx`)**:
  - Generates comprehensive classification guide sheets across 3, 5, 7, and 9 classes.
  - **Intelligent Degenerate Class Recovery Engine**: Automatically detects and rescues collapsed mechanical classes (e.g., `27 - 27°` or `6 - 6`) into balanced, non-overlapping uniform ranges (e.g., `26 - 27°`, `28 - 29°`) with bottom-to-top chain consistency.
  - **Transparent Dual In-Cell Annotation**: Cells present the recommended clean cartographic range followed by ArcMap's raw mechanical output in parentheses (e.g., `26 - 27° (أصل أرك ماب: 27 - 27°)`), preventing user confusion.
  - **Dual Representation Columns**: Integer discrete intervals alongside high-precision 1-decimal intervals for exact numerical reference.
  - **Strict International Unit & Symbol Standardization**: Clean degree symbol `°` without duplicate `C` notation, plus `mm`, `%`, `hPa`, `m/s`, and `°/dec`.

---

## 🚀 Getting Started & Verification

### Running in ArcGIS Pro
1. Add `POWER_Climate_Atlas_Generator_10_8.pyt` via **Catalog -> Toolboxes -> Add Toolbox**.
2. Select your operation mode, assign your station layer and study area mask, and click **Run**.

### Running in ArcMap 10.8
1. Open ArcToolbox -> Right-click -> **Add Toolbox...** -> Select `POWER_Climate_Atlas_Generator_10_8.pyt`.
2. Launch the tool, configure parameters, and execute.

---

## 👨‍💻 Developer & Attribution

- **Developer:** **Ahmad Ibrahim** (أحمد إبراهيم)
- **GitHub:** [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)
- **Repository:** [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)
- **License:** MIT License

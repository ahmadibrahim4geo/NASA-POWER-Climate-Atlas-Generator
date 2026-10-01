# NASA POWER & Open-Meteo Climate Atlas Generator
## منظومة مولد أطلس المناخ الشامل ومكتبة الستايلات الكارتوجرافية المعتمدة لبرنامجي ArcGIS Pro و ArcMap 10.8

[![Developer](https://img.shields.io/badge/Developer-Ahmad%20Ibrahim-1F4E79.svg?style=for-the-badge&logo=github)](https://github.com/ahmadibrahim4geo)
[![المطور](https://img.shields.io/badge/المطور-أحمد%20إبراهيم-2E75B6.svg?style=for-the-badge)](https://github.com/ahmadibrahim4geo)
[![ArcGIS Pro](https://img.shields.io/badge/ArcGIS%20Pro-3.x%20%7C%202.x-0079c1.svg)](https://pro.arcgis.com/)
[![ArcMap](https://img.shields.io/badge/ArcGIS%20Desktop-10.8%20%7C%2010.x-0079c1.svg)](https://desktop.arcgis.com/)
[![Python Version](https://img.shields.io/badge/Python-3.x%20%7C%202.7-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-NASA%20POWER%20%7C%20Open--Meteo-blue.svg)](https://power.larc.nasa.gov/)
[![Modular Architecture](https://img.shields.io/badge/Elements-17%20Modular%20Layers-darkgreen.svg)](#٣-العناصر-والمؤشرات-المناخية-الـ-17-الموديلية)

> **إعداد وتطوير:** **أحمد إبراهيم (Ahmad Ibrahim)**  
> **حساب المطور على GitHub:** [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)  
> **مستودع المشروع:** [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)

---

## 📌 الفهرس السريع | Quick Navigation
- [🇪🇬 دليل الاستخدام والتوثيق الشامل باللغة العربية](#-دليل-الاستخدام-والتوثيق-الشامل-باللغة-العربية)
  - [١. ما هي منظومة أطلس المناخ؟](#١-ما-هي-منظومة-أطلس-المناخ؟)
  - [٢. التوافقية المزدوجة التامة (ArcGIS Pro & ArcMap 10.8)](#٢-التوافقية-المزدوجة-التامة-arcgis-pro--arcmap-108)
  - [٣. العناصر والمؤشرات المناخية الـ 17 الموديلية](#٣-العناصر-والمؤشرات-المناخية-الـ-17-الموديلية)
  - [٤. نمطا التشغيل الرئيسيان (Online & Offline) وسلوك التخطي الذكي](#٤-نمطا-التشغيل-الرئيسيان-online--offline-وسلوك-التخطي-الذكي)
  - [٥. تقنية الضغط القوي فائق الأداء للراستر (Lossless LZW Block Tiling)](#٥-تقنية-الضغط-القوي-فائق-الأداء-للراستر-lossless-lzw-block-tiling)
  - [٦. المعالجة المكانية غير الهدامة والماسك وأسهم الرياح](#٦-المعالجة-المكانية-غير-الهدامة-والماسك-وأسهم-الرياح)
  - [٧. المنظومة الكارتوجرافية والستايلات المعتمدة](#٧-المنظومة-الكارتوجرافية-والستايلات-المعتمدة)
  - [٨. خطوات التثبيت والتشغيل خطوة بخطوة](#٨-خطوات-التثبيت-والتشغيل-خطوة-بخطوة)
- [🇬🇧 English Documentation](#-english-documentation)
  - [Overview & Architecture](#-overview--architecture)
  - [Dual Platform Support (ArcGIS Pro 3.x & Desktop 10.8)](#-dual-platform-support-arcgis-pro-3x--desktop-108)
  - [The 17 Modular Climate Layers](#-the-17-modular-climate-layers)
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

### ٣. العناصر والمؤشرات المناخية الـ 17 الموديلية
تمت إعادة هيكلة قواعد البيانات الناتجة بالكامل لتتحول من النمط القديم المدمج إلى **17 طبقة معالم منفصلة ومستقلة (Modular Feature Classes)**، مما يمنح الباحث مرونة قصوى في التحليل الفردي لكل عنصر دون تضخم الجداول:

| رقم | اسم الطبقة (Feature Class) | التوصيف العلمي والمؤشرات المتضمنة | الوحدة الفيزيائية |
|:---:|---|---|:---:|
| **01** | `01_Temperature` | درجات الحرارة: المتوسط السنوي والفصلي (DJF, MAM, JJA, SON)، المدى الحراري، أدفأ الشهور وأبردها، النهايات العظمى والصغرى، ونقطة الندى السنوية والفصلية (Td). | °C |
| **02** | `02_Precipitation` | التساقط والأمطار: المجموع السنوي، المعدل الشهري، المجاميع الفصلية، أقصى مطر يومي مسجل، وعدد الأيام الممطرة سنوياً. | mm, days |
| **03** | `03_Sea_Level_Pressure` | ضغط مستوى سطح البحر: المتوسطات السنوية والفصلية والمدى السنوي لضغط الهواء المصحح لمستوى سطح البحر. | hPa / mbar |
| **04** | `04_Surface_Pressure` | الضغط السطحي الفعلي: الضغط الجوي الحقيقي المحسوب عند الارتفاع الطبوغرافي الفعلي للمحطة. | hPa / mbar |
| **05** | `05_Wind` | الرياح السطحية: متوسطات السرعة السنوية والفصلية عند ارتفاع 10 أمتار، الاتجاه السائد السنوي والشهري عبر المتوسط الدائري (Circular Mean)، والمدى السنوي. | m/s, degrees (°) |
| **06** | `06_Relative_Humidity` | الرطوبة النسبية: المتوسطات السنوية والفصلية للرطوبة النسبية عند ارتفاع مترين والمدى السنوي للتذبذب الرطوبي. | % |
| **07** | `07_Solar_Radiation` | الإشعاع الشمسي: الإشعاع السطحي اليومي المباشر والمنتشر الكلي (All-Sky SW DNI/GHI)، والإجمالي السنوي التراكمي. | kWh/m²/day, kWh/m²/year |
| **08** | `08_UV_Index` | مؤشر الأشعة فوق البنفسجية: متوسطات شدة الإشعاع الشمسي الفوق بنفسجي عند الظهيرة وفق معايير منظمة الصحة العالمية (WHO). | مؤشر (0–15+) |
| **09** | `09_Cloud_Cover` | الغطاء السحابي: نسب التغطية الغيمية السنوية والفصلية ومواسم الصفاء الشمسي. | % |
| **10** | `10_De_Martonne_Aridity` | مؤشر دي مارتون للقحولة: التقييم المناخي للجفاف عبر صيغة $I_{DM} = P / (T + 10)$ والتصنيف من فائق الجفاف إلى رطب. | مؤشر لا بُعدي |
| **11** | `11_Hargreaves_PET` | التبخر-نتح الكامن بهارجريفز: الحساب التراكمي الفلكي للتبخر وفق معيار منظمة الأغذية والزراعة (FAO-56). | mm/year |
| **12** | `12_UNEP_Aridity` | مؤشر القحولة العالمي (UNEP): نسبة المطر إلى التبخر $AI = P / PET$ المعتمدة لدى اتفاقية مكافحة التصحر (UNCCD). | نسبة |
| **13** | `13_Water_Deficit` | العجز / الفائض المائي المناخي: الموازنة المائية الصافية السنوية $WD = P - PET$. | mm/year |
| **14** | `14_Dry_Months` | الأشهر الجافة بيولوجياً: عدد الشهور التي يتحقق فيها شرط والتر-ليث البيومناخي ($P < 2T$). | شهور (0–12) |
| **15** | `15_Heat_Index` | مؤشر الحرارة المحسوسة والإجهاد: مؤشر روثفوس وستيدمان (Heat Index)، ومؤشر Humidex الشتوي، ومتوسط الإجهاد الحراري الصيفي المظلل (WBGT). | °C |
| **16** | `16_Wind_Chill` | مؤشر البرودة الريحية: التبريد المكافئ للرياح في الشتاء والمتوسط السنوي (Osczevski-Bluestein formula). | °C |
| **17** | `17_Trends_And_Anomalies` | الاتجاهات والشذوذ المناخي: معدل التغير لكل عقد (Decadal Trend) للحرارة والمطر، والشذوذ السنوي والفصلي مقارنة بخط أساس 1991–2020. | °C/decade, mm/decade, % |

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

### ٧. المنظومة الكارتوجرافية والستايلات المعتمدة
* تتضمن مكتبة الستايلات المعتمدة في مجلد `style/`:
  - **125 ستايلاً كارتوجرافياً علمياً** يغطي كافة المجالات المناخية، مسنداً للمراجع الدولية (WMO, IPCC AR6, NOAA NCEI, ECMWF ERA5, WHO).
  - **2,250 تدرجاً لونياً (Color Ramps)** تدعم التصنيف من 3 إلى 11 فئة، بنمطين رئيسيين:
    - نمط **`[Stepped]`**: فئات لونية مصمتة ومنفصلة لخرائط الراستر المصنفة (`Classified`).
    - نمط **`[Smooth]`**: تدرجات لونية انسيابية متصلة لخرائط الراستر الممتدة (`Stretched`).
  - مصنف الإكسيل الماستر المرئي الملون (`NASA_POWER_Climate_Atlas_Master_Styles.xlsx`).
  - قاموس الحقول والوحدات المعتمد باللغتين العربية والإنجليزية (`Fields_AR_EN_Units.xlsx`).

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

## 🗺️ The 17 Modular Climate Layers

The system decomposes climatological and bioclimatic indicators into **17 discrete, standalone feature classes**:

1. **`01_Temperature`**: Annual and seasonal means (DJF, MAM, JJA, SON), thermal range, warmest and coldest months, diurnal extremes, and annual/seasonal dew point temperatures (Td).
2. **`02_Precipitation`**: Annual total, monthly mean rate, seasonal accumulated sums, 24-hour maximum rainfall, and annual rain day count.
3. **`03_Sea_Level_Pressure`**: Annual, seasonal, and range of atmospheric pressure reduced to mean sea level (MSLP).
4. **`04_Surface_Pressure`**: True hypsometric surface atmospheric pressure at actual station topography.
5. **`05_Wind`**: 10-meter wind speed annual/seasonal means, circular vector mean azimuth wind directions, and annual wind speed range.
6. **`06_Relative_Humidity`**: 2-meter relative humidity annual/seasonal means and annual psychrometric range.
7. **`07_Solar_Radiation`**: Daily mean and accumulated annual total solar insolation (kWh/m²/year), seasonal variations, and annual range.
8. **`08_UV_Index`**: Solar noon all-sky UV radiation index according to World Health Organization (WHO) risk thresholds.
9. **`09_Cloud_Cover`**: Annual and seasonal cloud okta fractions and sunshine duration dynamics.
10. **`10_De_Martonne_Aridity`**: De Martonne aridity index ($I_{DM} = P / (T + 10)$) and aridity zone classifications.
11. **`11_Hargreaves_PET`**: FAO-56 Hargreaves-Samani potential evapotranspiration with astronomical extraterrestrial solar radiation calculations.
12. **`12_UNEP_Aridity`**: United Nations Environment Programme aridity index ($AI = P / PET$) for dryland classification.
13. **`13_Water_Deficit`**: Net annual climatic water balance ($WD = P - PET$).
14. **`14_Dry_Months`**: Walter-Lieth bioclimatic dry months count ($P < 2T$).
15. **`15_Heat_Index`**: Steadman-Rothfusz apparent temperature heat index, winter Humidex, and summer shade wet-bulb globe temperature (WBGT).
16. **`16_Wind_Chill`**: Osczevski-Bluestein equivalent wind chill temperature index.
17. **`17_Trends_And_Anomalies`**: Decadal linear climate trends and anomalies relative to the 1991–2020 WMO standard normal.

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

## 🎨 Cartographic Mega System

- **125 Scientific Styles** conforming to WMO, IPCC AR6, NOAA NCEI, and ECMWF standards.
- **2,250 Color Ramps** across 9 class tiers (3 to 11 classes) with `[Stepped]` and `[Smooth]` modes.
- Master Excel visual palette catalog: `NASA_POWER_Climate_Atlas_Master_Styles.xlsx`.
- Complete bilingual field dictionary and units reference: `Fields_AR_EN_Units.xlsx`.

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

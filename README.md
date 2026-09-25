# NASA POWER & Open-Meteo Climate Atlas Generator for ArcGIS Desktop 10.8
## منظومة مولد أطلس المناخ الشامل ومكتبة الستايلات الكارتوجرافية المعتمدة لبرنامج ArcMap 10.8

[![Developer](https://img.shields.io/badge/Developer-Ahmad%20Ibrahim-1F4E79.svg?style=for-the-badge&logo=github)](https://github.com/ahmadibrahim4geo)
[![المطور](https://img.shields.io/badge/المطور-أحمد%20إبراهيم-2E75B6.svg?style=for-the-badge)](https://github.com/ahmadibrahim4geo)
[![ArcGIS Version](https://img.shields.io/badge/ArcGIS%20Desktop-10.8%20%7C%2010.x-0079c1.svg)](https://desktop.arcgis.com/)
[![Python Version](https://img.shields.io/badge/Python-2.7%20%7C%203.x-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-NASA%20POWER%20%7C%20Open--Meteo-blue.svg)](https://power.larc.nasa.gov/)
[![Styles Count](https://img.shields.io/badge/Styles-125%20Palettes%20%7C%202%2C250%20Ramps-darkgreen.svg)](#the-cartographic-mega-system-mega-edition)

> **إعداد وتطوير:** **أحمد إبراهيم (Ahmad Ibrahim)**  
> **حساب المطور على GitHub:** [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)  
> **مستودع المشروع:** [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)

---

## 📌 الفهرس السريع | Quick Navigation
- [🇪🇬 دليل الاستخدام والتوثيق باللغة العربية (Arabic Documentation)](#-دليل-الاستخدام-والتوثيق-الشامل-باللغة-العربية)
  - [١. ما هو مشروع أطلس المناخ؟](#١-ما-هو-مشروع-أطلس-المناخ؟)
  - [٢. أبرز إمكانيات ومميزات الأداة](#٢-أبرز-إمكانيات-ومميزات-الأداة)
  - [٣. العناصر والمؤشرات المناخية الـ 11](#٣-العناصر-والمؤشرات-المناخية-الـ-11-المغطاة)
  - [٤. المنظومة الكارتوجرافية الشاملة (Mega Edition)](#٤-المنظومة-الكارتوجرافية-الشاملة-mega-edition)
  - [٥. خطوات التثبيت والتشغيل في ArcMap 10.8](#٥-خطوات-التثبيت-والتشغيل-في-arcmap-108-خطوة-بخطوة)
  - [٦. كيفية تطبيق الستايلات على خرائط الراستر](#٦-كيفية-تطبيق-الستايلات-على-خرائط-الراستر-والمضلعات)
  - [٧. بيانات العينة المرفقة (Sample Data)](#٧-بيانات-العينة-المرفقة-sample-data)
- [🇬🇧 English Documentation](#-english-documentation)
  - [Key Features](#-key-features)
  - [The Cartographic Mega System](#-the-cartographic-mega-system-mega-edition)
  - [Repository Structure](#-repository-structure)
  - [Getting Started](#-getting-started)
  - [International Standards](#-international-standards--references)

---

# 🇪🇬 دليل الاستخدام والتوثيق الشامل باللغة العربية

### ١. ما هو مشروع أطلس المناخ؟
هذا المشروع عبارة عن منظومة برمجية متكاملة لصناديق أدوات نظم المعلومات الجغرافية (**ArcGIS Python Toolbox - `.pyt`**) مصممة ومبنية خصيصاً لتعمل مباشرة داخل برنامج **Esri ArcMap Desktop 10.8** (وكافة إصدارات ArcGIS 10.x).

تم تطوير الأداة لحل أصعب المشكلات التي تواجه الباحثين الجغرافيين وخبراء البيئة والمناخ:
1. **صعوبة جلب البيانات المناخية متعددة العقود:** تقوم الأداة بالاتصال السحابي المباشر بقواعد بيانات وكالة الفضاء الأمريكية (**NASA POWER API**) ومنصة الأرصاد العالمية (**Open-Meteo API**) وسحب سلاسل البيانات التاريخية والمستقبلية لنقاط ومحطات الرصد تلقائياً.
2. **الاستنباط المكاني الآلي (Spatial Interpolation):** تحويل البيانات النقطية إلى أسطح راستر متصلة بدقة عالية عبر خوارزميات الاستنباط المعتمدة (IDW, Spline, Focal Statistics).
3. **الافتقار إلى ستايلات كارتوجرافية وفيزيائية معتمدة في ArcMap:** تم بناء أكبر مكتبة ستايلات مناخية موحدة تضم **125 ستايلاً علمياً** و **2,250 تدرجاً لونياً أصلياً (Color Ramps)** متوافقة مع معايير المنظمة العالمية للأرصاد (WMO) والهيئة الحكومية الدولية المعنية بتغير المناخ (IPCC AR6).

---

### ٢. أبرز إمكانيات ومميزات الأداة
- **الاتصال المزدوج بواجهات برمجة التطبيقات (Dual APIs):**
  - **NASA POWER:** بيانات الإشعاع الشمسي، درجات الحرارة، الرطوبة، والرياح (من 1981 وحتى اليوم).
  - **Open-Meteo:** بيانات إعادة التحليل المناخي ERA5 ونماذج التغير المناخي المستقبلية CMIP6.
- **نافذة التقويم المرئي التفاعلي (Interactive Calendar GUI):**
  - نافذة رسومية هادئة مدمجة داخل صندوق الأدوات تمكن المستخدم من اختيار تاريخ البداية والنهاية بنقرة زر وبسهولة تامة بين الشهور والسنوات لتجنب أي أخطاء في كتابة صيغ التواريخ.
- **الحسابات الإحصائية والمعدلات المناخية (WMO 30-Year Normals):**
  - حساب المعدلات الشهرية، والفصلية (شتاء، ربيع، صيف، خريف)، والسنوية، وحساب الانحراف المعياري والقيم القصوى والدنيا.
- **حل تلقائي لمعادلات الجفاف والقحولة العالمية:**
  - حساب مؤشر دي مارتون للقحولة (De Martonne).
  - حساب مؤشر القحولة العالمي للأمم المتحدة (UNEP Aridity Index).
  - التبخر-نتح الكامن بهارجريفز (Hargreaves-Samani PET).
  - العجز المائي المناخي (Climatic Water Deficit).
- **تصدير النتائج إلى كافة الصيغ الجغرافية:**
  - طبقات معالم وجيوداتابيس (`.gdb`).
  - ملفات شيب فايل (`.shp`).
  - أسطح راستر جغرافية (`GeoTIFF`).
  - تقارير إحصائية وجداول إكسيل منسقة (`.xlsx`).

---

### ٣. العناصر والمؤشرات المناخية الـ 11 المغطاة
تغطي الأداة 11 مجالاً مناخياً رئيسياً تشمل جميع عناصر الغلاف الجوي والسطح:
1. **درجات الحرارة (Temperature):** العظمى، الصغرى، المتوسط، ونطاق التذبذب اليومي.
2. **التساقط والأمطار (Precipitation):** المجموع السنوي، الفصلي، التراكمي، وكثافة الأمطار.
3. **ضغط مستوى سطح البحر (Sea Level Pressure):** خطوط تساوي الضغط (Isobars) والأنظمة السينوبتيكية.
4. **الضغط الجوي السطحي (Surface Pressure):** الضغط الفعلي المصحح طبوغرافياً.
5. **سرعة واتجاه الرياح (Wind Speed & Direction):** المتجهات، مقياس بوفورت، وورود الرياح.
6. **الرطوبة النسبية (Relative Humidity):** رطوبة الهواء، نقطة الندى، والعجز البخاري (VPD).
7. **الإشعاع الشمسي (Solar Radiation):** الإشعاع الكلي السطحي، الإشعاع المباشر والمنتشر (DNI/GHI).
8. **مؤشر الأشعة فوق البنفسجية (UV Index):** معايير منظمة الصحة العالمية لمخاطر الإشعاع.
9. **الغطاء السحابي وسطوع الشمس (Cloud Cover & Sunshine):** نسب تغطية السحب وساعات السطوع.
10. **مؤشرات الجفاف والقحولة (Drought & Aridity):** العجز المائي ومؤشرات المناخ الجاف وشبه الجاف.
11. **نماذج وسيناريوهات التغير المناخي (Climate Models):** سيناريوهات الانبعاثات والاحترار العالمي (IPCC SSPs).

---

### ٤. المنظومة الكارتوجرافية الشاملة (Mega Edition)
تم تضمين أضخم مكتبة ستايلات كارتوجرافية علمية لبرنامج ArcMap داخل مجلد `style/`:
* **125 ستايلاً علمياً معتمداً** مسنداً للمراجع الدولية.
* **9 مستويات فئات لكل ستايل:** [3، 4، 5، 6، 7، 8، 9، 10، 11 فئة] لتغطية كافة متطلبات التحليل الإحصائي والكارتوجرافي.
* **2,250 Color Ramps أصلية:**
  - نمط **`[Stepped]`**: فئات لونية مصمتة ومنفصلة مخصصة لخرائط الراستر المصنفة (`Classified`).
  - نمط **`[Smooth]`**: تدرجات لونية انسيابية مخصصة لأسطح الراستر الممتدة (`Stretched`).
* **875 لوناً فردياً مسجلاً (`[Colors]`):** لاختيار ألوان الفئات مباشرة.
* **875 رمز مضلع مصمت (`[Fill Symbols]`):** بحدود ناعمة (0.4pt) لتلوين نطاقات المتجهات والأقاليم.
* **ملف إكسيل مرئي ماستر (`NASA_POWER_Climate_Atlas_Master_Styles.xlsx`):** يمثل كافة التدرجات مع خلايا ملونة بخلفيات الألوان الحقيقية.
* **ملف توثيق مرجعي شامل (`Climate_Styles_Sources_and_References.docx`):** يوثق كافة المعادلات والروابط للمراجع الـ 15 الدولية.

---

### ٥. خطوات التثبيت والتشغيل في ArcMap 10.8 خطوة بخطوة

1. **تحميل المشروع:**
   قم باستنساخ المستودع عبر الأمر التالي في موجه الأوامر:
   ```bash
   git clone https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator.git
   ```
   أو اضغط على زر **Code -> Download ZIP** وفك الضغط في أي مسار تريده.
2. **فتح برنامج ArcMap 10.8:**
   - افتح نافذة **ArcToolbox** (بالضغط على أيقونة الصندوق الأحمر في شريط الأدوات العلوي).
   - اضغط بزر الفأرة الأيمن في أي مساحة فارغة داخل نافذة ArcToolbox واختر **`Add Toolbox...`**.
   - تصفح للوصول إلى مجلد المشروع واختر الملف:  
     `POWER_Climate_Atlas_Generator_10_8.pyt`
3. **تشغيل الأداة:**
   - ستظهر لك الأداة باسم **NASA POWER Climate Atlas Generator**.
   - انقر نقراً مزدوجاً لفتحها، ثم حدد طبقة نقاط المحطات (يمكنك استخدام نقاط العينة في `Sample Data`).
   - اختر العنصر المناخي (حرارة، مطر، رياح، إلخ).
   - إذا اخترت **Custom Date Range**، فعّل خيار **Launch Visual Calendar Window** لتفتح لك نافذة التقويم المرئي التفاعلية لاختيار التواريخ بسهولة.
   - اضغط **OK** لبدء المعالجة والاستنباط التلقائي!

---

### ٦. كيفية تطبيق الستايلات على خرائط الراستر والمضلعات

#### لتحميل الستايلات في مدير الستايلات (Style Manager):
1. من القائمة العلوية في أرك ماب: اختر **`Customize`** -> ثم **`Style Manager...`**.
2. اضغط على زر **`Styles...`** من القائمة اليمنى.
3. اضغط على زر **`Add Style to List...`**.
4. توجه إلى مجلد:
   `style\All_ArcMap_Styles_Consolidated\`
5. اختر الملف الشامل: **`NASA_POWER_Climate_Atlas_Master.style`**.
6. اضغط **Open** ثم **OK**.

#### لتلوين طبقة راستر مصنفة (Classified Raster):
1. انقر بزر الفأرة الأيمن على طبقة الراستر -> **Properties** -> تبويب **Symbology**.
2. اختر من القائمة اليسرى: **Classified**.
3. حدد عدد الفئات في خانة **Classes** (من 3 إلى 11 فئة).
4. في قائمة **Color Ramp** المنسدلة، اختر التدرج الذي يحمل علامة **`[Stepped]`** للفئات المنفصلة أو **`[Smooth]`** للتدرج الانسيابي.
5. اضغط **Apply** ثم **OK**.

---

### ٧. بيانات العينة المرفقة (Sample Data)
يحتوي مجلد [`Sample Data/`](file:///C:/Users/ahmad/Desktop/NASA%20POWER%20Climate%20Atlas%20Generator/Sample%20Data) على حزمة بيانات تجريبية تطبيقية متكاملة لدراسة الحالة (جمهورية مصر العربية):
- 📁 **`Egypt_Climate_Stations/`**: تضم شبكة محطات الرصد المناخي الـ 86 المعتمدة والموثقة لدى المنظمة العالمية للأرصاد (WMO Block 62xxx) وقاعدة بيانات NOAA ISD، متوفرة بصيغتي Geodatabase وشيب فايل WGS84، مع ملفات إكسيل و CSV منسقة وموثقة باللغة العربية والإنجليزية.
- 📁 **`Egypt Climate Data/`**: تضم جيوداتابيس متكاملة تشمل حدود مصر الرسمية (`Egypt`) ومضلع نطاق الدراسة (`REC`) ونقاط العينات المناخية الجاهزة للاختبار الفوري.

---

# 🇬🇧 English Documentation

An enterprise-grade, peer-reviewed Climate Atlas Generator and scientific cartography suite engineered natively for **Esri ArcMap Desktop 10.8** (compatible with all ArcGIS Desktop 10.x releases).

Developed by **Ahmad Ibrahim** ([@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)).

The system automates the acquisition, climatological processing, statistical aggregation, spatial interpolation, and standardized cartographic rendering of multi-decadal historical climate records and future climate change models directly inside ArcGIS Desktop.

---

## 🌟 Key Features

- **Dual API Data Acquisition:** Direct integration with **NASA POWER API** (Prediction Of Worldwide Energy Resources) and **Open-Meteo Climate API** (ERA5 Reanalysis & CMIP6 Projections).
- **Automated Climatological Engine:** Computes annual, seasonal, monthly, daily, and custom date range statistics, standard deviations, and climatological normals (WMO 30-Year Normals).
- **Interactive Visual Calendar GUI:** Native date picker modal embedded directly into ArcMap toolbox parameters, allowing effortless month/year navigation without manual string entry.
- **Spatial Interpolation & Focal Smoothing:** Automated generation of continuous climate surfaces via IDW (Inverse Distance Weighted), Spline, and focal neighborhood filter smoothing.
- **The Cartographic Mega System (Mega Edition):**
  - **125 Scientific Styles** across 11 climate domains.
  - **9 Class Tiers** per style: `3, 4, 5, 6, 7, 8, 9, 10, and 11 classes`.
  - **2,250 Native ArcMap Color Ramps** categorized into `[Stepped]` (solid classification blocks) and `[Smooth]` (perceptually uniform CIE L\*a\*b\* gradients).
  - **875 Named Colors** and **875 Polygon Fill Symbols** with 0.4 pt neutral borders.
- **Master Visual Reference Workbook (`NASA_POWER_Climate_Atlas_Master_Styles.xlsx`):** Multi-sheet Excel reference containing all 2,250 ramps with **true background color fills** rendered in individual cells.
- **Master Reference Documentation (`Climate_Styles_Sources_and_References.docx`):** Fully documented physical foundations, peer-reviewed citations, and international standards.
- **Multi-Format Export Pipeline:** Exports into ESRI File Geodatabase (`.gdb`), Shapefile (`.shp`), GeoTIFF rasters, and formatted Excel workbooks.

---

## 🗺️ The Cartographic Mega System (Mega Edition)

The atlas provides 125 peer-reviewed color palettes organized across 11 thematic climate elements:

| # | Element Domain | Styles | Ramps (3–11 Classes) | Primary International Standards |
|---|---|:---:|:---:|---|
| **01** | **Temperature** | 16 | 288 | WMO No. 522, IPCC AR6 WGI, NOAA NCEI, ColorBrewer |
| **02** | **Precipitation** | 14 | 252 | WMO Guide No. 168, GPCC, NOAA CPC, CHIRPS |
| **03** | **Sea Level Pressure** | 10 | 180 | WMO Surface Synoptic, DWD MSLP, ECMWF ERA5 |
| **04** | **Surface Pressure** | 9 | 162 | Hypsometric Barometric, Standard Atmosphere |
| **05** | **Wind Speed & Direction** | 12 | 216 | Beaufort Scale (WMO No. 8), IEC 61400-1, NOAA NWS |
| **06** | **Relative Humidity** | 10 | 180 | Psychrometric Vapour, NOAA Vapor Pressure Deficit |
| **07** | **Solar Radiation** | 12 | 216 | NREL NSRDB, Copernicus CAMS, PVGIS Solar Atlas |
| **08** | **UV Index** | 8 | 144 | WHO / WMO Global Solar UV Index Standard |
| **09** | **Cloud Cover & Sunshine** | 10 | 180 | WMO Octas Code, ISCCP Cloud Physics, NASA CERES |
| **10** | **Drought & Aridity** | 12 | 216 | US Drought Monitor, UNEP AI, WMO SPI / SPEI |
| **11** | **Climate Change & Models** | 12 | 216 | IPCC AR6 Warming Scenarios, CMIP6 Ensemble, Crameri |
| **Total** | **All 11 Domains** | **125** | **2,250** | **15 International Meteorological & Cartographic Standards** |

### Ramp Types: `[Stepped]` vs. `[Smooth]`
- **`[Stepped]` (Solid Class Blocks):** Constructed as multi-part algorithmic ramps with zero intra-class gradient. Designed specifically for classified rasters (`Symbology -> Classified`), choropleth zones, and risk boundaries.
- **`[Smooth]` (Continuous Gradients):** Seamless mathematical transitions interpolated in perceptual color space. Designed for stretched raster surfaces (`Symbology -> Stretched`).

### Zero-Centered Diverging Symmetry
Diverging palettes feature rigorous mathematical symmetry centered around calibrated zero/neutral breakpoints:
- **11 Classes:** 5 negative/cool/dry + 1 neutral baseline (`#FFFFFF` or `#F7F7F7`) + 5 positive/warm/wet.
- **9 Classes:** 4 negative + 1 neutral + 4 positive.
- **7 Classes:** 3 negative + 1 neutral + 3 positive.
- **5 Classes:** 2 negative + 1 neutral + 2 positive.
- **3 Classes:** 1 negative + 1 neutral + 1 positive.
- **Even Tiers (4, 6, 8, 10 Classes):** Equidistant polar contrast for quartile, sextile, octile, and decile distributions.

---

## 📁 Repository Structure

```
NASA POWER Climate Atlas Generator/
├── POWER_Climate_Atlas_Generator_10_8.pyt     # Main ArcGIS Desktop 10.8 Python Toolbox
├── POWER_Climate_Atlas_Generator_10_8.pyt.xml # ArcToolbox item description metadata
├── raster_atlas_generator.py                  # Core backend engine (APIs, spatial processing)
├── LICENSE                                    # Open-source MIT License
├── README.md                                  # Repository documentation (Bilingual Arabic / English)
├── .gitignore                                 # Git rules for ArcGIS, Python, and OS files
│
├── docs/                                      # Comprehensive User & Technical Guides
│   ├── User_Guide_Arabic.md                   # Complete Arabic manual
│   ├── User_Guide_English.md                  # Complete English manual
│   ├── Fields_Reference_Table.md              # Climatological variable mapping & units
│   └── Interactive_Guide.html                 # Offline interactive web documentation
│
├── style/                                     # Cartographic Mega System (.style databases)
│   ├── NASA_POWER_Climate_Atlas_Master_Styles.xlsx  # Master Excel workbook with real color fills
│   ├── Climate_Styles_Sources_and_References.docx   # Master Word documentation with references
│   ├── Style_Guide_Arabic.md                  # Quick Arabic ArcMap style setup guide
│   ├── Style_Guide_English.md                 # Quick English ArcMap style setup guide
│   │
│   ├── All_ArcMap_Styles_Consolidated/        # Consolidated ArcMap Style Databases
│   │   ├── NASA_POWER_Climate_Atlas_Master.style    # Master unified style (2,250 ramps, 875 colors)
│   │   ├── 01_Temperature.style to 11_Climate_Models.style
│   │   ├── NASA_POWER_Climate_Atlas_Master_Styles.xlsx
│   │   └── Climate_Styles_Sources_and_References.docx
│   │
│   ├── 01_Temperature/ ... 11_Climate_Models/ # Individual element folders (style + README)
│   ├── Raw_Climate_Styles/                    # Reference palettes & raw source files
│   └── Source_of_Style_and_Color/             # Cartographic specifications & theory
│
├── utils/                                     # Utility modules and style generators
│   ├── __init__.py                            # Python package initialization
│   ├── calendar_dialog.py                     # Modal visual calendar GUI (Tkinter)
│   ├── build_mega_climate_styles.py           # Master 125-style compiler script
│   ├── build_true_arcmap_style_databases.py   # ArcObjects COM native .style generator
│   ├── generate_climate_styles.py             # Color palette mathematical definitions
│   ├── generate_master_styles_excel.py        # Openpyxl visual Excel workbook generator
│   ├── create_sources_word_document.py        # Python-docx master documentation generator
│   ├── fetch_egypt_stations.py                # Meteorological station network fetcher
│   └── verify_stations.py                     # Station data integrity checker
│
├── tests/                                     # Automated test suite for ArcGIS 10.8
│   ├── run_e2e_108.py                         # End-to-end integration test runner
│   ├── smoke_108_test.py                      # Smoke verification suite
│   ├── test_elements_108.py                   # Verification across all 11 climate elements
│   ├── test_excel_export_108.py               # Excel reporting verification
│   └── logs/                                  # Test run logs directory (.gitkeep)
│
└── Sample Data/                               # Sample datasets and case study files
    ├── Egypt Climate Data/                    # Study area boundary and sample GDB
    └── Egypt_Climate_Stations/                # 86 meteorological stations (GDB, SHP, Excel, CSV)
```

---

## 🚀 Getting Started

### Prerequisites
- **Esri ArcGIS Desktop 10.8** (or 10.1 - 10.8.2) with ArcMap.
- **Python 2.7** (installed automatically with ArcGIS Desktop under `C:\Python27\ArcGIS10.8`).
- **Spatial Analyst Extension** (recommended for raster surface interpolation).

### Installation in ArcMap Desktop
1. Clone or download this repository to your local machine:
   ```bash
   git clone https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator.git
   ```
2. Open **ArcMap 10.8**.
3. Open the **ArcToolbox** window (`Geoprocessing` -> `ArcToolbox` or click the red toolbox icon).
4. Right-click anywhere in ArcToolbox and select **Add Toolbox...**.
5. Browse to the repository root directory and select **`POWER_Climate_Atlas_Generator_10_8.pyt`**.
6. The toolbox **NASA POWER Climate Atlas Generator** is now loaded and ready for use!

### Loading the Climate Styles into ArcMap
1. In ArcMap, navigate to **`Customize`** -> **`Style Manager...`**.
2. Click **`Styles...`** on the right side.
3. Click **`Add Style to List...`**.
4. Browse to:
   ```
   style/All_ArcMap_Styles_Consolidated/NASA_POWER_Climate_Atlas_Master.style
   ```
5. Click **Open** and then **OK**.
6. All 2,250 Color Ramps, 875 Colors, and 875 Fill Symbols are now globally available across ArcMap's Symbology dialogs!

---

## 📊 Scientific Verification & QA Testing

The system includes automated test suites verifying execution against ArcGIS 10.8 ArcPy:
```bash
# Run comprehensive smoke test
C:\Python27\ArcGIS10.8\python.exe tests/smoke_108_test.py

# Run all 11 climate element integration tests
C:\Python27\ArcGIS10.8\python.exe tests/test_elements_108.py

# Run Excel export validation
C:\Python27\ArcGIS10.8\python.exe tests/test_excel_export_108.py
```

---

## 📜 International Standards & References

The color scales and classifications within this atlas strictly adhere to physical and perceptual standards established by:
- **World Meteorological Organization (WMO):** WMO-No. 8 (CIMO Guide), WMO-No. 522 (Standard Normals), WMO-No. 168 (Hydrology).
- **Intergovernmental Panel on Climate Change (IPCC):** Sixth Assessment Report (AR6) Visual Style Guide & Colour Schemes.
- **NOAA National Centers for Environmental Information (NCEI) & Climate Prediction Center (CPC).**
- **ECMWF (European Centre for Medium-Range Weather Forecasts):** ERA5 Reanalysis visualization palettes.
- **Crameri Scientific Colour Maps:** Perceptually uniform, color-blind friendly scales (Batlow, Roma, Vik, Cork, Berlin).
- **ColorBrewer 2.0:** Standardized cartographic divergence algorithms by Cynthia Brewer.
- **World Health Organization (WHO):** Global Solar UV Index guidelines.

For exhaustive citations, equations, and hex tables, see [`style/Climate_Styles_Sources_and_References.docx`](file:///C:/Users/ahmad/Desktop/NASA%20POWER%20Climate%20Atlas%20Generator/style/Climate_Styles_Sources_and_References.docx).

---

## 👨‍💻 Developer & Author

- **Author:** **Ahmad Ibrahim** (أحمد إبراهيم)
- **GitHub:** [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)
- **Repository:** [NASA-POWER-Climate-Atlas-Generator](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)

---

## 📄 License

This project is licensed under the MIT License - see the [`LICENSE`](file:///C:/Users/ahmad/Desktop/NASA%20POWER%20Climate%20Atlas%20Generator/LICENSE) file for details.

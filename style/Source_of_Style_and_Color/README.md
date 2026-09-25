# دليل ومستودع المصادر والمراجع الرسمية لتصميم الستايلات والألوان المناخية
## Official Scientific Sources, International Standards & Cartographic References

**المشروع:** NASA POWER & Open-Meteo Climate Atlas Generator  
**المجلد:** `style/Source_of_Style_and_Color/`  
**الغرض:** التوثيق العلمي والأكاديمي الصارم لجميع المصادر، البحوث، الأدلة التشغيلية، والروابط الرسمية التي تم الاستناد إليها في بناء واختيار التدرجات والألوان.

---

## 1. جدول الفهرس السريع للمصادر والجهات الدولية المصدرة

| المعيار / المصدر | الجهة الدولية المصدرة | التصنيف الكارتوجرافي | العناصر المطبقة | الرابط الرسمي المباشر |
| :--- | :--- | :--- | :--- | :--- |
| **مدونة إزري: ألوان أفضل لتخريط أفضل (Better Colors for Better Mapping)** | Environmental Systems Research Institute (Esri Inc.) | تصميم الألوان والإرشادات الكارتوجرافية لنظم المعلومات الجغرافية | `All Modules (خصوصاً درجات الحرارة والراستر)` | [الرابط الرسمي](https://www.esri.com/arcgis-blog/products/js-api-arcgis/mapping/better-colors-for-better-mapping) |
| **أرشيف CPT-City العالمي للتدرجات اللونية المناخية والكارتوجرافية** | University of Sheffield / Generic Mapping Tools (GMT) | أرشيف التدرجات اللونية لعلوم الأرض والأرصاد | `Temperature, Precipitation, Pressure, Relief, Bathymetry` | [الرابط الرسمي](https://phillips.shef.ac.uk/pub/cpt-city/) |
| **معايير الهيئة الحكومية الدولية المعنية بتغير المناخ (IPCC AR6) والتدرجات العلمية المحايدة إدراكياً** | Intergovernmental Panel on Climate Change (IPCC) / University of Oslo | المعايير البصرية العلمية للتقارير المناخية الدولية | `Temperature Anomalies, Climatological Means, Climate Models (01, 11)` | [الرابط الرسمي](https://www.fabiocrameri.ch/colourmaps/) |
| **نظام كولور بروير للكارتوجرافيا وتمايز الفئات (ColorBrewer 2.0)** | Pennsylvania State University / National Science Foundation (NSF) | المعيار الأكاديمي الكارتوجرافي العالمي للخرائط الموضوعية | `All Modules (Sequential, Diverging, Qualitative 3, 5, 7, 9 classes)` | [الرابط الرسمي](https://colorbrewer2.org/) |
| **معايير المنظمة العالمية للأرصاد الجوية (WMO-No. 306 & WMO-No. 8)** | World Meteorological Organization (WMO) - United Nations | المعايير الدولية للأرصاد الجوية والمناخ | `Temperature, Wind, Pressure, Cloud Cover (01, 03, 04, 05, 09)` | [الرابط الرسمي](https://library.wmo.int/records/item/35625-manual-on-codes) |
| **المعايير التشغيلية للإدارة الوطنية الأمريكية للمحيطات والغلاف الجوي (NOAA & NWS)** | National Oceanic and Atmospheric Administration (NOAA) | المعايير التشغيلية للتنبؤات والرصد المناخي | `Temperature, Heat Index, Precipitation, Radar Reflectivity (01, 02)` | [الرابط الرسمي](https://www.wpc.ncep.noaa.gov/) |
| **المعيار الدولي الموحد لمؤشر الأشعة فوق البنفسجية (WHO / WMO / UNEP)** | World Health Organization (WHO) | المعايير الدولية للصحة والسلامة الإشعاعية | `UV Index (08_UV_Index)` | [الرابط الرسمي](https://www.who.int/publications/i/item/9241590076) |
| **معايير القحولة والتصحر الدولية (أطلس التصحر العالمي UNEP / ودليل FAO-56)** | UN Environment Programme / Food and Agriculture Organization (FAO) | معايير القحولة والجفاف والهيدرولوجيا الزراعية | `Drought & Aridity, PET, Water Deficit (10_Drought_And_Aridity)` | [الرابط الرسمي](https://wad.jrc.ec.europa.eu/) |
| **معايير أطلس الطاقة الشمسية العالمي (World Bank / ESMAP / Solargis)** | World Bank Group | كارتوجرافيا الإشعاع الشمسي والطاقة المتجددة | `Solar Radiation (07_Solar_Radiation)` | [الرابط الرسمي](https://globalsolaratlas.info/) |
| **مبادرة خطوط الاحترار العالمي (Ed Hawkins Warming Stripes)** | University of Reading / National Centre for Atmospheric Science (NCAS) | التواصل العلمي الكارتوجرافي للتغير المناخي | `Climate Models & Temperature Anomalies (11_Climate_Models)` | [الرابط الرسمي](https://showyourstripes.info/) |

---

## 2. الشرح التفصيلي لكل مصدر والأسس الكارتوجرافية المعتمدة منه

### 1. مدونة إزري: ألوان أفضل لتخريط أفضل (Better Colors for Better Mapping)
* **الاسم بالإنجليزية:** Better Colors for Better Mapping (Esri ArcGIS Blog)
* **المؤلف والباحث المسؤول:** Kristian Ekenes / Esri Cartography Team
* **المنظمة الدولية / الناشر:** Environmental Systems Research Institute (Esri Inc.)
* **الرابط الرسمي المباشر:** [https://www.esri.com/arcgis-blog/products/js-api-arcgis/mapping/better-colors-for-better-mapping](https://www.esri.com/arcgis-blog/products/js-api-arcgis/mapping/better-colors-for-better-mapping)
* **نطاق التطبيق في المشروع:** `All Modules (خصوصاً درجات الحرارة والراستر)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Multi_SpectralMuted, Temp_Div_TealCoral, Temp_Seq_AmberOrange`

**الوصف والدور العلمي:**  
المرجع الكارتوجرافي الرسمي المطور من إزري لاختيار تدرجات لونية متناغمة ومريحة للعين، والابتعاد عن الألوان الفاقعة والمشوهة في خرائط الويب والراستر وتطبيقات GIS.

**أهم القواعد والأسس المستفادة:**
* تجنب الألوان الفاقعة المشبعة (Neon/Saturated) التي تجهد بصر متخذ القرار.
* مراعاة السطوع الإدراكي (Perceptual Lightness) وتوازن التدرج عند التقاء الفئات.
* توفير خيارات ملائمة لفاقدي تمييز الألوان (Colorblind accessibility).
* استخدام خلفيات لونية محايدة في الفئات الوسطى للتدرجات ثنائية الاتجاه.

---

### 2. أرشيف CPT-City العالمي للتدرجات اللونية المناخية والكارتوجرافية
* **الاسم بالإنجليزية:** cpt-city: An Archive of Colour Gradients for Cartography & Climatology
* **المؤلف والباحث المسؤول:** J.J. Green / University of Sheffield
* **المنظمة الدولية / الناشر:** University of Sheffield / Generic Mapping Tools (GMT)
* **الرابط الرسمي المباشر:** [https://phillips.shef.ac.uk/pub/cpt-city/](https://phillips.shef.ac.uk/pub/cpt-city/)
* **نطاق التطبيق في المشروع:** `Temperature, Precipitation, Pressure, Relief, Bathymetry`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Div_PuOr, Temp_Multi_Thermal_Crameri, Precip_Div_BrBG`

**الوصف والدور العلمي:**  
المستودع الرقمي العالمي الأكبر لتدرجات الألوان المستخدمة في نظم GMT وQGIS والأرصاد الجوية؛ يحتوي على آلاف التدرجات العلمية المصممة بواسطة كبار علماء الكارتوجرافيا.

**أهم القواعد والأسس المستفادة:**
* توفير تدرجات مخصصة لكل عنصر فيزيائي (درجات الحرارة، الرطوبة، الضغط، الهطول).
* التمييز الصارم بين التدرجات المتتابعة (Sequential) وثنائية الاتجاه (Diverging).
* توثيق التدرجات بصيغ رياضية تتيح إعادة بناء الفئات بأي عدد (3، 5، 7، 9 فئات).

---

### 3. معايير الهيئة الحكومية الدولية المعنية بتغير المناخ (IPCC AR6) والتدرجات العلمية المحايدة إدراكياً
* **الاسم بالإنجليزية:** IPCC AR6 Visual Guide & Scientific Colour Maps (Fabio Crameri)
* **المؤلف والباحث المسؤول:** Dr. Fabio Crameri / IPCC Working Group I
* **المنظمة الدولية / الناشر:** Intergovernmental Panel on Climate Change (IPCC) / University of Oslo
* **الرابط الرسمي المباشر:** [https://www.fabiocrameri.ch/colourmaps/](https://www.fabiocrameri.ch/colourmaps/)
* **نطاق التطبيق في المشروع:** `Temperature Anomalies, Climatological Means, Climate Models (01, 11)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Div_RdBu_IPCC, Temp_Multi_Thermal_Crameri, Anomaly_Div_IPCC`

**الوصف والدور العلمي:**  
المنظومة العلمية الصادرة في مجلة Nature Communications (Crameri et al., 2020) والمتبناة كلياً في التقرير السادس لـ IPCC؛ تضمن خلو التدرجات من أي تشوهات بصرية زائفة ناتجة عن التغير غير المنتظم للسطوع.

**أهم القواعد والأسس المستفادة:**
* الحظر الصارم لتدرجات قوس قزح التقليدية (Rainbow/Jet) التي تخلق حدوداً وهمية وتضلل التحليل المناخي.
* التدرج المنتظم تماماً في السطوع الخطي (Linear Lightness Gradient).
* إمكانية قراءة الخريطة بدقة تامة حتى بعد تحويلها للأبيض والأسود بالكامل (Greyscale Printable).

---

### 4. نظام كولور بروير للكارتوجرافيا وتمايز الفئات (ColorBrewer 2.0)
* **الاسم بالإنجليزية:** ColorBrewer 2.0: Color Advice for Cartography
* **المؤلف والباحث المسؤول:** Dr. Cynthia Brewer / Mark Harrower
* **المنظمة الدولية / الناشر:** Pennsylvania State University / National Science Foundation (NSF)
* **الرابط الرسمي المباشر:** [https://colorbrewer2.org/](https://colorbrewer2.org/)
* **نطاق التطبيق في المشروع:** `All Modules (Sequential, Diverging, Qualitative 3, 5, 7, 9 classes)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Seq_WarmRed, Temp_Seq_AmberOrange, Temp_Seq_CoolBlue, Temp_Div_RdYlBu_Brewer, Precip_Seq_YlGnBu`

**الوصف والدور العلمي:**  
المعيار الأكاديمي القياسي الأول عالمياً في برامج GIS (ArcGIS, QGIS) لتحديد الفئات اللونية المنفصلة والمتتابعة وثنائية الاتجاه، مع اختبارات معملية دقيقة للسطوع والتباين في الفضاء اللوني CIE Lab.

**أهم القواعد والأسس المستفادة:**
* توفير خطوات تمايز محددة ومدروسة كارتوجرافياً للفئات (3، 5، 7، 9 فئات).
* اختبار التوافق مع فئات عمى الألوان المختلفة (Deuteranopia, Protanopia, Tritanopia).
* توازن تشبع الألوان لضمان وضوح معالم الخريطة الأساسية (Base map) وتسميات النصوص.

---

### 5. معايير المنظمة العالمية للأرصاد الجوية (WMO-No. 306 & WMO-No. 8)
* **الاسم بالإنجليزية:** World Meteorological Organization Synoptic & Climatological Standards
* **المؤلف والباحث المسؤول:** WMO Commission for Instruments and Methods of Observation (CIMO)
* **المنظمة الدولية / الناشر:** World Meteorological Organization (WMO) - United Nations
* **الرابط الرسمي المباشر:** [https://library.wmo.int/records/item/35625-manual-on-codes](https://library.wmo.int/records/item/35625-manual-on-codes)
* **نطاق التطبيق في المشروع:** `Temperature, Wind, Pressure, Cloud Cover (01, 03, 04, 05, 09)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Multi_WMO_Standard, PSL_Div_Standard, Wind_Seq_Beaufort, Cloud_Seq_Okta`

**الوصف والدور العلمي:**  
اللوائح الدولية الملزمة للترميز الكارتوجرافي للمحطات السطحية، خطوط تساوي الضغط (Isobars)، متجهات وسرعات الرياح (Beaufort Scale)، ومقياس الأوكتا للغيوم والسحب.

**أهم القواعد والأسس المستفادة:**
* الارتكاز على قيمة الضغط المعياري عند مستوى سطح البحر (1013.25 hPa) في الخرائط السينوبتيكية.
* مقياس بوفورت المعياري للرياح بألوان متدرجة تعكس شدة الخطورة الميكانيكية.
* ترجمة مقياس الأوكتا (0/8 سماء صافية إلى 8/8 سماء ملبدة كلياً) لتدرج أزرق إلى رمادي رصاصي.

---

### 6. المعايير التشغيلية للإدارة الوطنية الأمريكية للمحيطات والغلاف الجوي (NOAA & NWS)
* **الاسم بالإنجليزية:** NOAA National Weather Service Operational Scales & National Blend of Models (NBM)
* **المؤلف والباحث المسؤول:** NOAA / National Weather Service / Weather Prediction Center (WPC)
* **المنظمة الدولية / الناشر:** National Oceanic and Atmospheric Administration (NOAA)
* **الرابط الرسمي المباشر:** [https://www.wpc.ncep.noaa.gov/](https://www.wpc.ncep.noaa.gov/)
* **نطاق التطبيق في المشروع:** `Temperature, Heat Index, Precipitation, Radar Reflectivity (01, 02)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Temp_Multi_NOAA_NWS, Precip_Seq_YlGnBu`

**الوصف والدور العلمي:**  
المقاييس اللونية المعتمدة في رادارات NEXRAD ونماذج NBM ومؤشر الحرارة المحسوسة (Heat Index) وفق معادلة Steadman-Rothfusz.

**أهم القواعد والأسس المستفادة:**
* فئات مؤشر الحرارة المحسوسة: حذر (27-32°C)، حذر شديد (32-41°C)، خطر (41-54°C)، خطر داهم (>54°C).
* تدرجات الهطول المطري المتدرجة من الأخضر الشاحب إلى الأزرق النيلي والبنفسجي للأمطار الاستوائية.
* التوازن اللوني المريح للمعينات البصرية في غرف العمليات المناخية.

---

### 7. المعيار الدولي الموحد لمؤشر الأشعة فوق البنفسجية (WHO / WMO / UNEP)
* **الاسم بالإنجليزية:** Global Solar UV Index: A Practical Guide (ISBN 92 4 159007 6)
* **المؤلف والباحث المسؤول:** World Health Organization / WMO / UNEP / ICNIRP
* **المنظمة الدولية / الناشر:** World Health Organization (WHO)
* **الرابط الرسمي المباشر:** [https://www.who.int/publications/i/item/9241590076](https://www.who.int/publications/i/item/9241590076)
* **نطاق التطبيق في المشروع:** `UV Index (08_UV_Index)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `UV_Standard_WHO`

**الوصف والدور العلمي:**  
الدليل العالمي الإلزامي الذي يحدد بدقة متناهية 5 فئات لونية معيارية محددة بالأكواد السداسية لحماية صحة الإنسان من أخطار الإشعاع الشمسي.

**أهم القواعد والأسس المستفادة:**
* فئة 1 منخفض (0 - 2.9): أخضر نقي (#289500).
* فئة 2 متوسط (3 - 5.9): أصفر صريح (#F7E400).
* فئة 3 مرتفع (6 - 7.9): برتقالي ساطع (#F85900).
* فئة 4 مرتفع جداً (8 - 10.9): أحمر قاني (#D80010).
* فئة 5 خطر متطرف (11+): بنفسجي أرجواني (#6B49C8).

---

### 8. معايير القحولة والتصحر الدولية (أطلس التصحر العالمي UNEP / ودليل FAO-56)
* **الاسم بالإنجليزية:** UNEP World Atlas of Desertification & FAO-56 Irrigation Guidelines
* **المؤلف والباحث المسؤول:** UNEP / UNESCO / FAO (Allen, Pereira, Raes, Smith)
* **المنظمة الدولية / الناشر:** UN Environment Programme / Food and Agriculture Organization (FAO)
* **الرابط الرسمي المباشر:** [https://wad.jrc.ec.europa.eu/](https://wad.jrc.ec.europa.eu/)
* **نطاق التطبيق في المشروع:** `Drought & Aridity, PET, Water Deficit (10_Drought_And_Aridity)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Aridity_UNEP_DeMartonne`

**الوصف والدور العلمي:**  
التصنيف الدولي المعتمد للأراضي الجافة بناءً على مؤشر القحولة العالمي (AI = P / PET) ومعامل دي مارتون لحساب درجات الجفاف وعجز الموازنة المائية.

**أهم القواعد والأسس المستفادة:**
* شديد القحولة (AI < 0.05): بني محروق وقرمزي غامق.
* قاحل (0.05 <= AI < 0.20): أحمر داكن وبرتقالي محروق.
* شبه قاحل (0.20 <= AI < 0.50): أصفر رملي شاحب.
* شبه رطب وجاف (0.50 <= AI < 0.65): أخضر ليموني فاتح.
* رطب وفير (AI >= 0.65): أخضر زمردي داكن إلى أزرق مائي.

---

### 9. معايير أطلس الطاقة الشمسية العالمي (World Bank / ESMAP / Solargis)
* **الاسم بالإنجليزية:** Global Solar Atlas Standards & Benchmarks
* **المؤلف والباحث المسؤول:** Energy Sector Management Assistance Program (ESMAP) / Solargis
* **المنظمة الدولية / الناشر:** World Bank Group
* **الرابط الرسمي المباشر:** [https://globalsolaratlas.info/](https://globalsolaratlas.info/)
* **نطاق التطبيق في المشروع:** `Solar Radiation (07_Solar_Radiation)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Solar_Seq_YlOrRd`

**الوصف والدور العلمي:**  
المقياس المرجعي العالمي المعتمد لتمثيل الإشعاع الشمسي الكلي المباشر والأفقي (GHI / DNI) والتوليد الكهروضوئي الكامن.

**أهم القواعد والأسس المستفادة:**
* التدرج المتتابع من الأصفر الباهت إلى الذهبي ثم البرتقالي فالأحمر الياقوتي.
* التوافق مع عتبات الجدوى الاقتصادية لمزارع الطاقة الشمسية الكهروضوئية والحرارية.

---

### 10. مبادرة خطوط الاحترار العالمي (Ed Hawkins Warming Stripes)
* **الاسم بالإنجليزية:** Warming Stripes Climate Visualization Initiative
* **المؤلف والباحث المسؤول:** Prof. Ed Hawkins / University of Reading
* **المنظمة الدولية / الناشر:** University of Reading / National Centre for Atmospheric Science (NCAS)
* **الرابط الرسمي المباشر:** [https://showyourstripes.info/](https://showyourstripes.info/)
* **نطاق التطبيق في المشروع:** `Climate Models & Temperature Anomalies (11_Climate_Models)`
* **الستايلات المستمدة مباشرة من هذا المصدر:** `Anomaly_Div_IPCC`

**الوصف والدور العلمي:**  
الرمز البصري العالمي المعترف به دولياً لتصوير اتجاهات التغير المناخي من التبريد التاريخي (أزرق متدرج) إلى الاحترار المعاصر والقياسي (أحمر متدرج).

**أهم القواعد والأسس المستفادة:**
* البساطة المطلقة والوضوح البصري الفوري لغير المتخصصين ومتخذي القرار.
* الارتكاز على خط الصفر المناخي (0.0°C Anomaly) كفاصل رمادي أو أبيض محايد.

---

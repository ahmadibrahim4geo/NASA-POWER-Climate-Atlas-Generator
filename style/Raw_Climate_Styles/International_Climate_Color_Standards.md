# المعايير والأسس المناخية الدولية لاختيار وتصميم التدرجات اللونية
## International Climatological Standards & Scientific Rationale for Color Palettes

**مشروع:** NASA POWER & Open-Meteo Climate Atlas Generator  
**البرنامج المستهدف:** ArcGIS Desktop (ArcMap 10.x / 10.8)  
**الغرض:** التوثيق العلمي والمنهجي الدقيق للمعايير الصادرة عن المنظمات الدولية (IPCC, WMO, NOAA, WHO, UNEP, FAO) التي استُند إليها في تصميم واختيار تدرجات وألوان الستايلات المناخية.

---

## 1. جدول الربط الشامل: كل عنصر مناخي والمعيار الدولي المعتمد له

| العنصر المناخي (Climate Indicator) | المعيار الدولي المعتمد (Standard) | الجهة الدولية المصدرة (Organization) | نمط التدرج (Type) | الرابط الرسمي (Official Link) |
| :--- | :--- | :--- | :--- | :--- |
| **درجات الحرارة والشذوذ الحراري** | IPCC AR6 Visual Guide & Scientific Colour Maps | IPCC / Fabio Crameri / Ed Hawkins | متواصل + ثنائي الاتجاه (Diverging) | [IPCC AR6](https://www.ipcc.ch/) \| [Fabio Crameri](https://www.fabiocrameri.ch/colourmaps/) |
| **الأمطار والتساقط التراكمي** | NWS Operational Precipitation Scales | NOAA / National Weather Service | متتابع (Sequential) + ثنائي الاتجاه | [NOAA ROC](https://www.roc.noaa.gov/) \| [NOAA CPC](https://www.cpc.ncep.noaa.gov/) |
| **مؤشر الحرارة المحسوسة (Heat Index)** | Steadman-Rothfusz Risk Categories | NOAA National Weather Service | 4-5 فئات خطورة محددة | [NOAA Heat Index](https://www.wpc.ncep.noaa.gov/html/heatindex.shtml) |
| **سرعات ومتجهات الرياح** | Beaufort Wind Scale & WMO-No. 306 | WMO (World Meteorological Org.) | متتابع متدرج السطوع | [WMO Manual on Codes](https://library.wmo.int/records/item/35625-manual-on-codes) |
| **الضغط الجوي وسطح البحر** | WMO MSL Standard (1013.25 hPa Reference) | WMO / Synoptic Meteorology | ثنائي الاتجاه حول 1013.25 hPa | [WMO CIMO Guide](https://library.wmo.int/records/item/41650-guide-to-instruments-and-methods-of-observation) |
| **الغطاء السحابي (Cloud Cover)** | Okta Scale (0-8 Oktas) to % Standard | WMO International Cloud Atlas | متتابع من الأزرق الصافي للرمادي | [WMO Cloud Atlas](https://cloudatlas.wmo.int/) |
| **مؤشر الأشعة فوق البنفسجية (UV Index)** | Global Solar UV Index (ISBN 92 4 159007 6) | WHO / WMO / UNEP / ICNIRP | 5 فئات لونية معيارية دولياً | [WHO UV Index Guide](https://www.who.int/publications/i/item/9241590076) |
| **معامل القحولة والجفاف (UNEP / De Martonne)** | World Atlas of Desertification & UNESCO 1979 | UNEP / UNESCO / FAO | فئات من قاحل جداً إلى رطب | [UNEP Desertification Atlas](https://wad.jrc.ec.europa.eu/) |
| **البخر-نتح والعجز المائي (PET / Water Deficit)** | FAO-56 Irrigation & Drainage Guidelines | FAO (منظمة الأغذية والزراعة) | ثنائي الاتجاه (عجز سالب / وفرة موجبة) | [FAO-56 Guide](https://www.fao.org/land-water/databases-and-software/cropwat/en/) |
| **الإشعاع الشمسي والطاقة التراكمية** | Global Solar Atlas & ESMAP Benchmarks | World Bank / ESMAP / Solargis | متتابع أصفر/ذهبي/برتقالي | [Global Solar Atlas](https://globalsolaratlas.info/) |
| **التصميم الكارتوجرافي للفئات (3، 5، 7، 9)** | ColorBrewer 2.0 Perceptual Systems | Cynthia Brewer / Penn State / NSF | فئات متوازنة السطوع $\Delta L^*$ | [ColorBrewer 2.0](https://colorbrewer2.org/) |

---

## 2. تفاصيل المعايير العلمية والمحددات اللونية

### 1. معايير الهيئة الحكومية الدولية المعنية بتغير المناخ (IPCC)
* **المبدأ الأساسي**: التدرجات اللونية العلمية المحايدة إدراكياً (Perceptually Uniform Colour Maps).
* **السبب العلمي**: تجنب التدرجات الطيفية المشوهة (مثل Rainbow / Jet) التي تخلق حدوداً غير حقيقية في البيانات وتضلل متخذي القرار.
* **التطبيق**: استخدام تدرج أزرق داكن للبرودة الشديدة $\leftrightarrow$ أبيض رمادي محايد لنقطة الأساس $\leftrightarrow$ أحمر داكن وقرمزي للارتفاع الحراري القياسي.
* **المراجع الرسمية**:
  * [IPCC Official Site](https://www.ipcc.ch/)
  * [Scientific Colour Maps by Fabio Crameri](https://www.fabiocrameri.ch/colourmaps/)
  * [Ed Hawkins Warming Stripes Initiative](https://showyourstripes.info/)

### 2. معايير المنظمة العالمية للأرصاد الجوية (WMO)
* **المبدأ الأساسي**: الترميز الكارتوجرافي للمحطات السطحية ومحددات الرياح والضغط والسحب.
* **الرموز والتدرج**:
  * **الرياح**: مقياس بوفورت (Beaufort Scale) بألوان تبدأ بالأخضر النعناعي الفاتح للنسيم الخفيف وتصل إلى البنفسجي الداكن للرياح العاصفة.
  * **الضغط**: ارتكاز ثنائي الاتجاه على قيمة الضغط المعياري عند سطح البحر (1013.25 hPa).
  * **السحب**: ترجمة مقياس الأوكتا (Okta 0/8 إلى 8/8) لتدرج يبدأ بالأزرق السماوي وينتهي بالرمادي الرصاصي الداكن.
* **المراجع الرسمية**:
  * [WMO Manual on Codes (WMO-No. 306)](https://library.wmo.int/records/item/35625-manual-on-codes)
  * [WMO Guide to Meteorological Instruments (WMO-No. 8)](https://library.wmo.int/records/item/41650-guide-to-instruments-and-methods-of-observation)
  * [WMO International Cloud Atlas](https://cloudatlas.wmo.int/)

### 3. معايير الإدارة الوطنية الأمريكية للمحيطات والغلاف الجوي (NOAA & NWS)
* **المبدأ الأساسي**: عتبات الهطول المطري ومؤشر الإجهاد الحراري (Heat Index).
* **الرموز والتدرج**:
  * **الأمطار**: أخضر مصفر شاحب للأمطار الخفيفة $\rightarrow$ أزرق سماوي للمتوسطة $\rightarrow$ أزرق ملكي كحلي للأمطار الغزيرة والسيول.
  * **مؤشر الحرارة (HI)**: أصفر (حذر 27-32°C) $\rightarrow$ برتقالي ذهبي (حذر شديد 32-41°C) $\rightarrow$ أحمر (خطر 41-54°C) $\rightarrow$ قرمزي داكن (خطر شديد >54°C).
* **المراجع الرسمية**:
  * [NOAA Heat Index Guidelines](https://www.wpc.ncep.noaa.gov/html/heatindex.shtml)
  * [NOAA Climate Prediction Center (CPC)](https://www.cpc.ncep.noaa.gov/)
  * [NOAA Radar Operations Center (ROC)](https://www.roc.noaa.gov/)

### 4. المعيار الدولي المشترك لمؤشر الأشعة فوق البنفسجية (WHO / WMO / UNEP)
* **المبدأ الأساسي**: خمس فئات لونية معيارية ملزمة دولياً لحماية الصحة العامة (ISBN 92 4 159007 6):
  1. **منخفض (0 - 2.9)**: أخضر نقي (`#289500`).
  2. **متوسط (3 - 5.9)**: أصفر صريح (`#F7E400`).
  3. **مرتفع (6 - 7.9)**: برتقالي ساطع (`#F85900`).
  4. **مرتفع جداً (8 - 10.9)**: أحمر قاني (`#D80010`).
  5. **خطر متطرف (11+)**: أرجواني / بنفسجي (`#6B49C8`).
* **المراجع الرسمية**:
  * [WHO Global Solar UV Index Publication](https://www.who.int/publications/i/item/9241590076)
  * [WHO UV Radiation Information Page](https://www.who.int/news-room/fact-sheets/detail/ultraviolet-radiation)

### 5. معايير القحولة والجفاف (UNEP / UNESCO / FAO-56)
* **المبدأ الأساسي**: تصنيف الأراضي الجافة وفق مؤشر القحولة العالمي ($AI = P / PET$) ومعامل دي مارتون ($I = P / (T + 10)$):
  * **شديد القحولة ($AI < 0.05$)**: بني محروق وقرمزي غامق (`#67000D`).
  * **قاحل ($0.05 \le AI < 0.20$)**: أحمر داكن (`#D73027`).
  * **شبه قاحل ($0.20 \le AI < 0.50$)**: برتقالي وأصفر دافئ (`#F46D43` $\rightarrow$ `#FDAE61`).
  * **شبه رطب جاف ($0.50 \le AI < 0.65$)**: أخضر ليموني فاتح (`#A6D96A`).
  * **رطب وفير ($AI \ge 0.65$)**: أخضر زمردي داكن إلى أزرق مائي (`#1A9850` $\rightarrow$ `#006837`).
* **المراجع الرسمية**:
  * [UNEP World Atlas of Desertification](https://wad.jrc.ec.europa.eu/)
  * [FAO Irrigation and Drainage Paper No. 56](https://www.fao.org/land-water/databases-and-software/cropwat/en/)

### 6. معايير ColorBrewer 2.0 للكارتوجرافيا وتمايز الفئات
* **المبدأ الأساسي**: التوازن البصري لخطوات السطوع (Luminance Steps $\Delta L^*$) في الفضاء اللوني CIE Lab.
* **التقسيمات**: توفير سلاسل لونية مدروسة بدقة لـ **3 و 5 و 7 و 9 فئات** تضمن قابلية القراءة والطباعة وملاءمتها للمصابين بعمى الألوان.
* **المراجع الرسمية**:
  * [ColorBrewer 2.0 Web Tool](https://colorbrewer2.org/)
  * [Designing Better Maps - Cynthia Brewer (Esri Press)](https://www.esri.com/en-us/esri-press/browse/designing-better-maps)

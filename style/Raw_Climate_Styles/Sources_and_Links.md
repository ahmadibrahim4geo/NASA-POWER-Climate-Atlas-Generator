# دليل المصادر والروابط الرسمية للستايلات المناخية الخام (`.style`) لبرنامج ArcGIS Desktop

مستودع شامل لجميع ملفات الستايل الكارتوجرافية المناخية الخام الأصلية بصيغة **`.style`** المتوافقة كلياً مع برنامج **ArcGIS Desktop (ArcMap 10.0 - 10.8.2)**.

---

## 1. فهرس ملفات الستايل المناخية الخام المتاحة بالمجلد

| اسم الملف | الحجم | التدرجات اللونية (Color Ramps) | الألوان (Colors) | رموز الملء (Fill Symbols) | الخطوط (Lines) | النقاط (Markers) | التطبيق المناخي والبيئي |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`Meteorological.style`** | 1.04 MB | **15** | 59 | 43 | 27 | 214 | رادارات الطقس، درجات حرارة الهواء والتربة، بخار الماء، الثلوج |
| **`Weather.style`** | 872 KB | **15** | 59 | 43 | 27 | 281 | توقعات الأرصاد الجوية، الحالات الخطرة، الأمطار، المحطات السطحية |
| **`Military METOC.style`** | 1.84 MB | — | 5 | — | — | 196 | نماذج محطات الطقس WMO، متجهات الرياح، خطوط الضغط والجبهات |
| **`Environmental.style`** | 816 KB | — | 53 | 20 | 17 | 196 | النظم الإيكولوجية، القحولة، الجفاف، التصحر، الرطوبة الحيوية |
| **`Conservation.style`** | 744 KB | — | 32 | 27 | 34 | 120 | المحميات المناخية، مصادر المياه السطحية، الغابات وحمايتها |
| **`Forestry.style`** | 860 KB | — | 48 | 16 | 17 | 239 | الأقاليم النباتية والغطاء الحيوي وتأثره بالجفاف والحرارة |
| **`Water Wastewater.style`** | 696 KB | — | 47 | 27 | 33 | 97 | الهيدرولوجيا، مخرات السيول، شبكات التصريف، أحواض التبخر |
| **`Soils EURO.style`** | 664 KB | — | 146 | 146 | — | — | تصنيفات التربة الدولية وعلاقتها بالنطاقات المناخية والرطوبة |
| **`ESRI.style`** | 1.76 MB | **84** | 120 | 53 | 88 | 114 | تدرجات الحرارة والمطر والتدرجات ثنائية الاتجاه والأطياف الكاملة |

---

## 2. تفاصيل التدرجات اللونية في `Meteorological.style` و `Weather.style`

تحتوي هذه الملفات على التدرجات اللونية الرسمية المعتمدة من الهيئات العالمية للطقس:
1. **Air temperature**: تدرج قياسي عالمي لتوزيع درجات حرارة الهواء.
2. **Water vapor**: تدرج قياس نسب بخار الماء والرطوبة الجوية في طبقات الجو.
3. **Dangerous conditions**: تدرج التحذيرات القصوى والتطرف الحراري والمطري.
4. **Conventional Radar**: مقياس رادارات الطقس التقليدية.
5. **Doppler radar velocity**: تدرج سرعات الرياح الشعاعية لرادارات دوبلر.
6. **Doppler radar reflectivity**: تدرج انعكاسية السحب والهطول.
7. **NEXRAD reflectivity**: تدرج شبكة رادارات الطقس الوطنية الأمريكية (NEXRAD).
8. **NEXRAD Relative Mean Radial Velocity**: متوسط السرعات للكتل الهوائية.
9. **Precipitation (Weather Service Forecast)**: تدرج توقعات الهطول المطري لهيئة الأرصاد.
10. **Soil temperature**: تدرج قياس درجات حرارة التربة عند أعماق مختلفة.
11. **Water temperature**: تدرج حرارة المياه السطحية والبحار.
12. **Snowfall accumulation**: تدرج سماكة الثلوج وتراكم التساقط المتجمد.
13. **Radar Loop Mixed / Snow / Rain**: سلاسل رادارية ديناميكية للأمطار والثلوج.

---

## 3. الروابط والمصادر الرسمية المعتمدة

### أ. معهد أبحاث النظم البيئية الأمريكي (ESRI Inc.)
* [ArcGIS Style Manager Documentation](https://desktop.arcgis.com/en/arcmap/latest/map/working-with-styles/using-the-style-manager.htm) — الدليل الرسمي لإدارة واستخدام ملفات الستايل في ArcMap.
* [Working with Color Ramps in ArcGIS](https://desktop.arcgis.com/en/arcmap/latest/map/working-with-styles/working-with-color-ramps.htm) — الدليل الرسمي لاستخدام التدرجات اللونية في بيانات الراستر.
* [ArcGIS Online Meteorological Style Item](https://www.arcgis.com/home/item.html?id=a641da02580c44b391781297e6826dc6) — صفحة توثيق ستايل الأرصاد الجوية على ArcGIS Online.
* [ArcGIS Online Weather Style Item](https://www.arcgis.com/home/item.html?id=c752b757271449cfa12f1cfc06dcb00c) — صفحة توثيق ستايل الطقس على ArcGIS Online.
* [Esri Living Atlas: Weather & Climate](https://livingatlas.arcgis.com/en/browse/#d=2&categories=Environment:Weather%20and%20Climate) — بوابة أطلس العالم الحي لخرائط وبيانات الطقس والمناخ.

### ب. الإدارة الوطنية للمحيطات والغلاف الجوي الأمريكية (NOAA & NWS)
* [NOAA Climate Prediction Center (CPC)](https://www.cpc.ncep.noaa.gov/) — مركز التنبؤات المناخية وتصنيفات الجفاف ومؤشرات الشذوذ.
* [NOAA Radar Operations Center (ROC)](https://www.roc.noaa.gov/) — مركز تشغيل رادارات الطقس ومعايير ألوان NEXRAD.
* [NOAA Physical Sciences Laboratory Gridded Climate](https://psl.noaa.gov/data/gridded/) — مجموعات البيانات الشبكية المناخية ومعايير العرض الكارتوجرافي.

### ج. المنظمة العالمية للأرصاد الجوية (WMO)
* [WMO Manual on Codes (WMO-No. 306)](https://library.wmo.int/records/item/35625-manual-on-codes) — الدليل الدولي للرموز والمصطلحات ونماذج المحطات الجوية (Station Models).
* [Global Climate Observing System (GCOS)](https://gcos.wmo.int/) — النظام العالمي لمراقبة المناخ والمتغيرات المناخية الأساسية (ECVs).

### د. الهيئة الحكومية الدولية المعنية بتغير المناخ (IPCC)
* [IPCC AR6 Visual Style Guide & Colour Scales](https://www.ipcc.ch/) — المعايير البصرية المعتمدة للتقارير المناخية العالمية.
* [Scientific Colour Maps (Fabio Crameri)](https://www.fabiocrameri.ch/colourmaps/) — التدرجات اللونية العلمية الدقيقة والمحايدة إدراكياً لدرجات الحرارة والمطر والضغط.

### هـ. المرجع الأكاديمي لتصميم التدرجات (ColorBrewer 2.0)
* [ColorBrewer 2.0 - Penn State University](https://colorbrewer2.org/) — تدرجات Cynthia Brewer القياسية للتدرجات المتتابعة (Sequential) وثنائية الاتجاه (Diverging) والفئوية (Qualitative).

---

## 4. خطوات تحميل الستايل داخل ArcMap 10.8

1. افتح **ArcMap**.
2. من القائمة العلوية اضغط: **`Customize`** $\rightarrow$ **`Style Manager...`**.
3. في نافذة مدير الستايلات، اضغط زر **`Styles...`** على اليمين.
4. اضغط زر **`Add Style to List...`**.
5. تصفح واختر ملف الستايل المطلوب من مجلد:
   `c:\Users\ahmad\Desktop\NASA POWER Climate Atlas Generator\Raw_Climate_Styles`
6. اضغط **Open** ثم **OK**.
7. ستجد كافة التدرجات اللونية والرموز ظهرت فوراً في نافذة **Layer Properties $\rightarrow$ Symbology** لتلوين طبقات الراستر والشيب فايل بسهولة.

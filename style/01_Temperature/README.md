# موسوعة ودليل ستايلات درجات الحرارة الكارتوجرافية القياسية
## Climatological Temperature Styles & Cartographic Color Palette System

**المشروع:** NASA POWER & Open-Meteo Climate Atlas Generator  
**البرنامج المستهدف:** ArcGIS Desktop (ArcMap 10.x / 10.8), ArcGIS Pro, QGIS  
**المجلد:** `style/01_Temperature/`  
**إجمالي الستايلات:** 12 ستايلاً كارتوجرافياً معتمداً عالمياً عبر **4 فئات رئيسية (3، 5، 7، 9 فئات)** بما يوفّر **48 نموذجاً لونياً جاهزاً** للخرائط والأطالس.

---

## 1. المعايير والمرجعيات الدولية المعتمدة
استند تصميم هذه الستايلات إلى أحدث القواعد والبحوث الكارتوجرافية العالمية لضمان سلامة التفسير البصري للبيانات المناخية وتفادي أخطاء التدرجات المشوهة:
1. **IPCC AR6 Visual Style Guide & Scientific Colour Maps**: التدرجات المعتمدة من الهيئة الحكومية الدولية المعنية بتغير المناخ بقيادة د. فابيو كراميري (Fabio Crameri) لتجنب ألوان قوس قزح (Rainbow/Jet) وتوفير تدرجات محايدة إدراكياً (Perceptually Uniform).
2. **ColorBrewer 2.0 (Cynthia Brewer)**: المرجع العالمي الأول في كارتوجرافيا وتمايز الفئات اللونية في الفضاء اللوني CIE Lab وملاءمتها للمصابين بعمى الألوان (Colorblind-Safe) وجودة الطباعة بالأبيض والأسود.
3. **WMO-No. 306 & WMO-No. 8**: أدلة المنظمة العالمية للأرصاد الجوية لترميز الخرائط السينوبتيكية والأطالس المناخية.
4. **NOAA National Weather Service (NWS) & NBM**: التدرجات اللونية المعتدلة للشبكة الوطنية الأمريكية للأرصاد.
5. **Esri 'Better Colors for Better Mapping'**: إرشادات معهد أبحاث النظم البيئية الأمريكي لاختيار التدرجات المتناغمة غير الفاقعة لخرائط نظم المعلومات الجغرافية.
6. **CPT-City Climatological Archive**: الأرشيف العالمي لتدرجات علوم الأرض والطقس.

---

## 2. فهرس الستايلات الـ 12 المتاحة وتصنيفاتها الكارتوجرافية

| كود الستايل (Style ID) | اسم الستايل بالعربية | النوع (Category) | الفئات المتاحة | المصدر والمرجعية | الخصائص الكارتوجرافية |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Temp_Seq_WarmRed` | **أحمر مرجاني متدرج (أحادي اللون دافئ)** | متتابع لون واحد موحد | **3, 5, 7, 9** | ColorBrewer 2.0 Reds / Cynthia Brewer | تدرج أحادي اللون مريح للعين في الفضاء اللوني CIE Lab، مثالي لعرض شدة الحرارة دون تشتيت بصري. |
| `Temp_Seq_AmberOrange` | **كهرماني ذهبي متدرج (أحادي اللون دافئ)** | متتابع لون واحد موحد | **3, 5, 7, 9** | ColorBrewer 2.0 Oranges / Esri Warm | تدرج برتقالي كهرماني هادئ غير فاقع، يعكس الطاقة الإشعاعية والحرارة السطحية باعتدال لوني ممتاز. |
| `Temp_Seq_CoolBlue` | **أزرق شتوي متدرج (أحادي اللون للبرودة والحرارات الدنيا)** | متتابع لون واحد موحد | **3, 5, 7, 9** | ColorBrewer 2.0 Blues / WMO Winter | مخصص للمعدلات الشتوية والنهايات الصغرى، يتدرج من الثلجي الفاتح إلى الكحلي العميق دون إجهاد للبصر. |
| `Temp_Seq_DeepPurple` | **أرجواني ماغما عميق (أحادي اللون دافئ)** | متتابع لون واحد موحد | **3, 5, 7, 9** | ColorBrewer Purples / Crameri Devonian | تدرج أرجواني ملكي حديث، معتمد في خرائط الأطالس المتقدمة كبديل كارتوجرافي للأحمر التقليدي. |
| `Temp_Div_RdBu_IPCC` | **أزرق-أبيض-أحمر (معيار IPCC ثنائي الاتجاه بمركز محايد)** | لونين متقابلين بمركز محايد | **3, 5, 7, 9** | IPCC AR6 / NOAA Climate Prediction Center | المعيار الذهبي للهيئة الحكومية الدولية لتغير المناخ وNOAA؛ يربط البرودة (أزرق) والحرارة (أحمر) بمركز محايد شاحب. |
| `Temp_Div_RdYlBu_Brewer` | **كحلي-أصفر-قرمزي (كولور بروير القياسي بمركز أصفر دافئ)** | لونين متقابلين بمركز محايد | **3, 5, 7, 9** | Cynthia Brewer / ColorBrewer 2.0 RdYlBu | التدرج الكارتوجرافي الأكثر توازناً في أطالس العالم؛ المركز أصفر هادئ بدلاً من الأبيض لتجنب اختفاء الخلفية الورقية. |
| `Temp_Div_TealCoral` | **تركواز مائي-عاجي-مرجاني دافئ (ثنائي الاتجاه حديث)** | لونين متقابلين بمركز محايد | **3, 5, 7, 9** | Esri 'Better Colors for Better Mapping' / Crameri | تصميم كارتوجرافي عصري يوفر تبايناً فائق النقاء وجماليات طباعية مع ملاءمة تامة لفاقدي تمييز الألوان. |
| `Temp_Div_PuOr` | **بنفسجي عميق-رمادي لؤلؤي-برتقالي برونزي (ثنائي الاتجاه متوازن)** | لونين متقابلين بمركز محايد | **3, 5, 7, 9** | ColorBrewer 2.0 PuOr / CPT-City | مثالي لخرائط الشذوذ الحراري ومقارنة الفصول المتناقضة، بدرجات لونية راقية ومريحة كارتوجرافياً. |
| `Temp_Multi_Thermal_Crameri` | **التدرج الحراري العلمي المحايد إدراكياً (Batlow Thermal)** | ألوان منفصلة علمية متعددة | **3, 5, 7, 9** | Fabio Crameri Scientific Colour Maps / CPT-City Batlow | مبني على التدرج المنتظم في فضاء CAM02-UCS؛ يمنع تماماً الخداع البصري وحدود التدرج الزائفة في Rainbow. |
| `Temp_Multi_WMO_Standard` | **مقياس المنظمة العالمية للأرصاد الجوية (WMO Climatological Standard)** | ألوان منفصلة علمية متعددة | **3, 5, 7, 9** | WMO-No. 306 Manual on Codes / Synoptic Atlas | الألوان المعيارية لخرائط السينوبتيك والمناخ العالمي الصادرة عن WMO؛ متوازنة السطوع ومتدرجة بانسجام تام. |
| `Temp_Multi_NOAA_NWS` | **مقياس الأرصاد الوطنية الأمريكية المعتدل (NOAA NWS Blend)** | ألوان منفصلة علمية متعددة | **3, 5, 7, 9** | NOAA NWS National Blend of Models (NBM) | تدرج رصدي رسمي من NOAA يتميز بألوان هادئة غير صارخة تضمن التمييز الدقيق بين الكتل الهوائية الساخنة والباردة. |
| `Temp_Multi_SpectralMuted` | **الطيف الكارتوجرافي المتوازن غير الفاقع (Muted Spectral)** | ألوان منفصلة علمية متعددة | **3, 5, 7, 9** | Esri 'Better Colors for Better Mapping' / ColorBrewer Spectral | بديل احترافي لطيف الرينبو القديم؛ يمر عبر الأزرق الهادئ، الأخضر اللطيف، الأصفر الرملي، البرتقالي، والقرمزي. |

---

## 3. قسم التصنيف الكارتوجرافي والفئات (Classification System & Breakpoints)

### أ. طرق التصنيف المستخدمة أساساً في الستايل (Methods Used):
1. **الفواصل الطبيعية (Natural Breaks - Jenks)**:  
   * **طريقة العمل**: خوارزمية جينكس التكرارية تبحث عن التجمعات الطبيعية للبيانات وتقلل التباين الداخلي لكل فئة وتعظم التباين بين الفئات المختلفة.  
   * **سبب الاستخدام**: الخيار الكارتوجرافي الأفضل لإظهار التباينات المناخية الجغرافية الحقيقية بين الأقاليم (مثل السواحل، الدلتا، الصعيد، المناطق الجبلية) دون فرض حدود عشوائية.

2. **الفترات المتساوية (Equal Interval)**:  
   * **طريقة العمل**: تقسيم المدى الكلي للحرارة إلى فواصل ذات طول ثابت متساوٍ (مثل كل 2.5°C أو كل 5°C).  
   * **سبب الاستخدام**: الخيار الإلزامي عند إعداد سلاسل زمنية مقارنة (سنة بأخرى أو عقد بآخر) أو مقارنة الفصول، لأن ثبات طول الفئة يتيح للقارئ إدراك الفروق المكانية والزمنية الفورية.

### ب. طرق التصنيف البديلة المتاحة للاستخدام لاحقاً (Alternative Methods for Future Use):
يمكن للمستخدم تطبيق أي من هذه الطرق البديلة لاحقاً بضغطة زر داخل البرنامج:
1. **الفئات الكمية المتساوية (Quantile)**: تقسم المحطات أو المساحة بالتساوي بين الفئات (مثلاً كل فئة تحتوي 20% من مساحة الدولة). ممتازة للمقارنات الترتيبية والمئينات.
2. **الانحراف المعياري (Standard Deviation)**: تقسم البيانات حول المتوسط الحسابي بمضاعفات الانحراف المعياري ($\pm 0.5\sigma, \pm 1.0\sigma, \pm 2.0\sigma$). مثالية لخرائط **الشذوذ الحراري والتغير المناخي** (Temperature Anomaly).
3. **فترات محددة مسبقاً (Defined Interval)**: تحديد اتساع فاصل هندسي دقيق ثابت يحدده الباحث (مثلاً خطوة ثابتة قدرها 2°C أو 3°C).
4. **الحدود المناخية والفيزيولوجية المعتمدة (Manual Climatological Thresholds)**: تطبيق العتبات الصريحة المعتمدة من منظمة الأرصاد العالمية WMO (مثل خط الصفر والتجمد 0°C، حد النمو النباتي 10°C، الراحة البيولوجية 20-25°C، عتبة الموجات الحارة 35°C و 40°C).

---

### ج. جدول فواصل الفئات المعتمدة لدرجات الحرارة (Annual Mean Reference)

#### نموذج 3 فئات (3 Classes):
| رقم الفئة | الحد الفاصل الأعلى (Break °C) | المدى الحراري المقترح | التسمية الدلالية بالعربية (Label AR) | التسمية الإنجليزية (Label EN) |
| :---: | :---: | :---: | :--- | :--- |
| **1** | `20.0 °C` | < 20.0 °C | معتدل مائل للبرودة (< 20.0 °C) | Cool-Mild (< 20.0 °C) |
| **2** | `24.0 °C` | 20.0 - 24.0 °C | معتدل دافئ (20.0 - 24.0 °C) | Warm-Mild (20.0 - 24.0 °C) |
| **3** | `35.0 °C` | > 24.0 °C | حار (> 24.0 °C) | Warm-Hot (> 24.0 °C) |

#### نموذج 5 فئات (5 Classes):
| رقم الفئة | الحد الفاصل الأعلى (Break °C) | المدى الحراري المقترح | التسمية الدلالية بالعربية (Label AR) | التسمية الإنجليزية (Label EN) |
| :---: | :---: | :---: | :--- | :--- |
| **1** | `18.0 °C` | < 18.0 °C | لطيف منعش (< 18.0 °C) | Cool (< 18.0 °C) |
| **2** | `21.0 °C` | 18.0 - 21.0 °C | معتدل نموذجي (18.0 - 21.0 °C) | Mild (18.0 - 21.0 °C) |
| **3** | `24.0 °C` | 21.0 - 24.0 °C | معتدل دافئ (21.0 - 24.0 °C) | Warm-Mild (21.0 - 24.0 °C) |
| **4** | `27.0 °C` | 24.0 - 27.0 °C | حار (24.0 - 27.0 °C) | Warm-Hot (24.0 - 27.0 °C) |
| **5** | `35.0 °C` | > 27.0 °C | شديد الحرارة (> 27.0 °C) | Hot (> 27.0 °C) |

#### نموذج 7 فئات (7 Classes):
| رقم الفئة | الحد الفاصل الأعلى (Break °C) | المدى الحراري المقترح | التسمية الدلالية بالعربية (Label AR) | التسمية الإنجليزية (Label EN) |
| :---: | :---: | :---: | :--- | :--- |
| **1** | `16.0 °C` | < 16.0 °C | بارد نسبياً (< 16.0 °C) | Cold-Cool (< 16.0 °C) |
| **2** | `18.5 °C` | 16.0 - 18.5 °C | لطيف منعش (16.0 - 18.5 °C) | Cool (16.0 - 18.5 °C) |
| **3** | `21.0 °C` | 18.5 - 21.0 °C | معتدل (18.5 - 21.0 °C) | Mild (18.5 - 21.0 °C) |
| **4** | `23.5 °C` | 21.0 - 23.5 °C | معتدل دافئ (21.0 - 23.5 °C) | Warm-Mild (21.0 - 23.5 °C) |
| **5** | `26.0 °C` | 23.5 - 26.0 °C | دافئ نسبياً (23.5 - 26.0 °C) | Moderately Hot (23.5 - 26.0 °C) |
| **6** | `28.5 °C` | 26.0 - 28.5 °C | حار (26.0 - 28.5 °C) | Hot (26.0 - 28.5 °C) |
| **7** | `35.0 °C` | > 28.5 °C | شديد الحرارة (> 28.5 °C) | Very Hot (> 28.5 °C) |

#### نموذج 9 فئات (9 Classes):
| رقم الفئة | الحد الفاصل الأعلى (Break °C) | المدى الحراري المقترح | التسمية الدلالية بالعربية (Label AR) | التسمية الإنجليزية (Label EN) |
| :---: | :---: | :---: | :--- | :--- |
| **1** | `14.0 °C` | < 14.0 °C | بارد (< 14.0 °C) | Cold (< 14.0 °C) |
| **2** | `16.5 °C` | 14.0 - 16.5 °C | بارد معتدل (14.0 - 16.5 °C) | Cool-Cold (14.0 - 16.5 °C) |
| **3** | `19.0 °C` | 16.5 - 19.0 °C | لطيف (16.5 - 19.0 °C) | Cool (16.5 - 19.0 °C) |
| **4** | `21.5 °C` | 19.0 - 21.5 °C | معتدل (19.0 - 21.5 °C) | Mild (19.0 - 21.5 °C) |
| **5** | `24.0 °C` | 21.5 - 24.0 °C | معتدل دافئ (21.5 - 24.0 °C) | Warm-Mild (21.5 - 24.0 °C) |
| **6** | `26.5 °C` | 24.0 - 26.5 °C | دافئ (24.0 - 26.5 °C) | Warm (24.0 - 26.5 °C) |
| **7** | `29.0 °C` | 26.5 - 29.0 °C | حار (26.5 - 29.0 °C) | Hot (26.5 - 29.0 °C) |
| **8** | `31.5 °C` | 29.0 - 31.5 °C | حار جداً (29.0 - 31.5 °C) | Very Hot (29.0 - 31.5 °C) |
| **9** | `38.0 °C` | > 31.5 °C | شديد الحرارة قياسي (> 31.5 °C) | Extreme Hot (> 31.5 °C) |


---

## 4. الجداول التفصيلية لأكواد الألوان لجميع الستايلات (HEX / RGB / CMYK / HSV)

### الستايل: أحمر مرجاني متدرج (أحادي اللون دافئ) (`Temp_Seq_WarmRed`)
* **النوع:** متتابع لون واحد موحد | **المصدر:** ColorBrewer 2.0 Reds / Cynthia Brewer
* **الأساس العلمي:** تدرج أحادي اللون مريح للعين في الفضاء اللوني CIE Lab، مثالي لعرض شدة الحرارة دون تشتيت بصري.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFF5F0;border:1px solid #777;border-radius:2px;"></span> | `#FFF5F0` | `255, 245, 240` | `0%, 3.9%, 5.9%, 0%` | `20°, 5.9%, 100%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE0D2;border:1px solid #777;border-radius:2px;"></span> | `#FEE0D2` | `254, 224, 210` | `0%, 11.8%, 17.3%, 0.4%` | `19.1°, 17.3%, 99.6%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FCBBA1;border:1px solid #777;border-radius:2px;"></span> | `#FCBBA1` | `252, 187, 161` | `0%, 25.8%, 36.1%, 1.2%` | `17.1°, 36.1%, 98.8%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FC9272;border:1px solid #777;border-radius:2px;"></span> | `#FC9272` | `252, 146, 114` | `0%, 42.1%, 54.8%, 1.2%` | `13.9°, 54.8%, 98.8%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FB6A4A;border:1px solid #777;border-radius:2px;"></span> | `#FB6A4A` | `251, 106, 74` | `0%, 57.8%, 70.5%, 1.6%` | `10.8°, 70.5%, 98.4%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#EF3B2C;border:1px solid #777;border-radius:2px;"></span> | `#EF3B2C` | `239, 59, 44` | `0%, 75.3%, 81.6%, 6.3%` | `4.6°, 81.6%, 93.7%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#CB181D;border:1px solid #777;border-radius:2px;"></span> | `#CB181D` | `203, 24, 29` | `0%, 88.2%, 85.7%, 20.4%` | `358.3°, 88.2%, 79.6%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#A50F15;border:1px solid #777;border-radius:2px;"></span> | `#A50F15` | `165, 15, 21` | `0%, 90.9%, 87.3%, 35.3%` | `357.6°, 90.9%, 64.7%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#67000D;border:1px solid #777;border-radius:2px;"></span> | `#67000D` | `103, 0, 13` | `0%, 100%, 87.4%, 59.6%` | `352.4°, 100%, 40.4%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE5D9;border:1px solid #777;border-radius:2px;"></span> | `#FEE5D9` | `254, 229, 217` | `0%, 9.8%, 14.6%, 0.4%` | `19.5°, 14.6%, 99.6%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FCBBA1;border:1px solid #777;border-radius:2px;"></span> | `#FCBBA1` | `252, 187, 161` | `0%, 25.8%, 36.1%, 1.2%` | `17.1°, 36.1%, 98.8%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FC9272;border:1px solid #777;border-radius:2px;"></span> | `#FC9272` | `252, 146, 114` | `0%, 42.1%, 54.8%, 1.2%` | `13.9°, 54.8%, 98.8%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FB6A4A;border:1px solid #777;border-radius:2px;"></span> | `#FB6A4A` | `251, 106, 74` | `0%, 57.8%, 70.5%, 1.6%` | `10.8°, 70.5%, 98.4%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#EF3B2C;border:1px solid #777;border-radius:2px;"></span> | `#EF3B2C` | `239, 59, 44` | `0%, 75.3%, 81.6%, 6.3%` | `4.6°, 81.6%, 93.7%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#CB181D;border:1px solid #777;border-radius:2px;"></span> | `#CB181D` | `203, 24, 29` | `0%, 88.2%, 85.7%, 20.4%` | `358.3°, 88.2%, 79.6%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#99000D;border:1px solid #777;border-radius:2px;"></span> | `#99000D` | `153, 0, 13` | `0%, 100%, 91.5%, 40%` | `354.9°, 100%, 60%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE5D9;border:1px solid #777;border-radius:2px;"></span> | `#FEE5D9` | `254, 229, 217` | `0%, 9.8%, 14.6%, 0.4%` | `19.5°, 14.6%, 99.6%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FCAE91;border:1px solid #777;border-radius:2px;"></span> | `#FCAE91` | `252, 174, 145` | `0%, 31%, 42.5%, 1.2%` | `16.3°, 42.5%, 98.8%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FB6A4A;border:1px solid #777;border-radius:2px;"></span> | `#FB6A4A` | `251, 106, 74` | `0%, 57.8%, 70.5%, 1.6%` | `10.8°, 70.5%, 98.4%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#DE2D26;border:1px solid #777;border-radius:2px;"></span> | `#DE2D26` | `222, 45, 38` | `0%, 79.7%, 82.9%, 12.9%` | `2.3°, 82.9%, 87.1%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#A50F15;border:1px solid #777;border-radius:2px;"></span> | `#A50F15` | `165, 15, 21` | `0%, 90.9%, 87.3%, 35.3%` | `357.6°, 90.9%, 64.7%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE0D2;border:1px solid #777;border-radius:2px;"></span> | `#FEE0D2` | `254, 224, 210` | `0%, 11.8%, 17.3%, 0.4%` | `19.1°, 17.3%, 99.6%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FC9272;border:1px solid #777;border-radius:2px;"></span> | `#FC9272` | `252, 146, 114` | `0%, 42.1%, 54.8%, 1.2%` | `13.9°, 54.8%, 98.8%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#DE2D26;border:1px solid #777;border-radius:2px;"></span> | `#DE2D26` | `222, 45, 38` | `0%, 79.7%, 82.9%, 12.9%` | `2.3°, 82.9%, 87.1%` | حار (> 24.0 °C) |

---

### الستايل: كهرماني ذهبي متدرج (أحادي اللون دافئ) (`Temp_Seq_AmberOrange`)
* **النوع:** متتابع لون واحد موحد | **المصدر:** ColorBrewer 2.0 Oranges / Esri Warm
* **الأساس العلمي:** تدرج برتقالي كهرماني هادئ غير فاقع، يعكس الطاقة الإشعاعية والحرارة السطحية باعتدال لوني ممتاز.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFF5EB;border:1px solid #777;border-radius:2px;"></span> | `#FFF5EB` | `255, 245, 235` | `0%, 3.9%, 7.8%, 0%` | `30°, 7.8%, 100%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE6CE;border:1px solid #777;border-radius:2px;"></span> | `#FEE6CE` | `254, 230, 206` | `0%, 9.4%, 18.9%, 0.4%` | `30°, 18.9%, 99.6%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDD0A2;border:1px solid #777;border-radius:2px;"></span> | `#FDD0A2` | `253, 208, 162` | `0%, 17.8%, 36%, 0.8%` | `30.3°, 36%, 99.2%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE6B;border:1px solid #777;border-radius:2px;"></span> | `#FDAE6B` | `253, 174, 107` | `0%, 31.2%, 57.7%, 0.8%` | `27.5°, 57.7%, 99.2%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FD8D3C;border:1px solid #777;border-radius:2px;"></span> | `#FD8D3C` | `253, 141, 60` | `0%, 44.3%, 76.3%, 0.8%` | `25.2°, 76.3%, 99.2%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#F16913;border:1px solid #777;border-radius:2px;"></span> | `#F16913` | `241, 105, 19` | `0%, 56.4%, 92.1%, 5.5%` | `23.2°, 92.1%, 94.5%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#D94801;border:1px solid #777;border-radius:2px;"></span> | `#D94801` | `217, 72, 1` | `0%, 66.8%, 99.5%, 14.9%` | `19.7°, 99.5%, 85.1%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#A63603;border:1px solid #777;border-radius:2px;"></span> | `#A63603` | `166, 54, 3` | `0%, 67.5%, 98.2%, 34.9%` | `18.8°, 98.2%, 65.1%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#7F2704;border:1px solid #777;border-radius:2px;"></span> | `#7F2704` | `127, 39, 4` | `0%, 69.3%, 96.9%, 50.2%` | `17.1°, 96.9%, 49.8%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEEDDE;border:1px solid #777;border-radius:2px;"></span> | `#FEEDDE` | `254, 237, 222` | `0%, 6.7%, 12.6%, 0.4%` | `28.1°, 12.6%, 99.6%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDD0A2;border:1px solid #777;border-radius:2px;"></span> | `#FDD0A2` | `253, 208, 162` | `0%, 17.8%, 36%, 0.8%` | `30.3°, 36%, 99.2%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE6B;border:1px solid #777;border-radius:2px;"></span> | `#FDAE6B` | `253, 174, 107` | `0%, 31.2%, 57.7%, 0.8%` | `27.5°, 57.7%, 99.2%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FD8D3C;border:1px solid #777;border-radius:2px;"></span> | `#FD8D3C` | `253, 141, 60` | `0%, 44.3%, 76.3%, 0.8%` | `25.2°, 76.3%, 99.2%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#F16913;border:1px solid #777;border-radius:2px;"></span> | `#F16913` | `241, 105, 19` | `0%, 56.4%, 92.1%, 5.5%` | `23.2°, 92.1%, 94.5%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#D94801;border:1px solid #777;border-radius:2px;"></span> | `#D94801` | `217, 72, 1` | `0%, 66.8%, 99.5%, 14.9%` | `19.7°, 99.5%, 85.1%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#8C2D04;border:1px solid #777;border-radius:2px;"></span> | `#8C2D04` | `140, 45, 4` | `0%, 67.9%, 97.1%, 45.1%` | `18.1°, 97.1%, 54.9%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEEDDE;border:1px solid #777;border-radius:2px;"></span> | `#FEEDDE` | `254, 237, 222` | `0%, 6.7%, 12.6%, 0.4%` | `28.1°, 12.6%, 99.6%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDBE85;border:1px solid #777;border-radius:2px;"></span> | `#FDBE85` | `253, 190, 133` | `0%, 24.9%, 47.4%, 0.8%` | `28.5°, 47.4%, 99.2%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FD8D3C;border:1px solid #777;border-radius:2px;"></span> | `#FD8D3C` | `253, 141, 60` | `0%, 44.3%, 76.3%, 0.8%` | `25.2°, 76.3%, 99.2%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#E6550D;border:1px solid #777;border-radius:2px;"></span> | `#E6550D` | `230, 85, 13` | `0%, 63%, 94.3%, 9.8%` | `19.9°, 94.3%, 90.2%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#A63603;border:1px solid #777;border-radius:2px;"></span> | `#A63603` | `166, 54, 3` | `0%, 67.5%, 98.2%, 34.9%` | `18.8°, 98.2%, 65.1%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE6CE;border:1px solid #777;border-radius:2px;"></span> | `#FEE6CE` | `254, 230, 206` | `0%, 9.4%, 18.9%, 0.4%` | `30°, 18.9%, 99.6%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE6B;border:1px solid #777;border-radius:2px;"></span> | `#FDAE6B` | `253, 174, 107` | `0%, 31.2%, 57.7%, 0.8%` | `27.5°, 57.7%, 99.2%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#E6550D;border:1px solid #777;border-radius:2px;"></span> | `#E6550D` | `230, 85, 13` | `0%, 63%, 94.3%, 9.8%` | `19.9°, 94.3%, 90.2%` | حار (> 24.0 °C) |

---

### الستايل: أزرق شتوي متدرج (أحادي اللون للبرودة والحرارات الدنيا) (`Temp_Seq_CoolBlue`)
* **النوع:** متتابع لون واحد موحد | **المصدر:** ColorBrewer 2.0 Blues / WMO Winter
* **الأساس العلمي:** مخصص للمعدلات الشتوية والنهايات الصغرى، يتدرج من الثلجي الفاتح إلى الكحلي العميق دون إجهاد للبصر.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7FBFF;border:1px solid #777;border-radius:2px;"></span> | `#F7FBFF` | `247, 251, 255` | `3.1%, 1.6%, 0%, 0%` | `210°, 3.1%, 100%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#DEEBF7;border:1px solid #777;border-radius:2px;"></span> | `#DEEBF7` | `222, 235, 247` | `10.1%, 4.9%, 0%, 3.1%` | `208.8°, 10.1%, 96.9%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#C6DBEF;border:1px solid #777;border-radius:2px;"></span> | `#C6DBEF` | `198, 219, 239` | `17.2%, 8.4%, 0%, 6.3%` | `209.3°, 17.2%, 93.7%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#9ECAE1;border:1px solid #777;border-radius:2px;"></span> | `#9ECAE1` | `158, 202, 225` | `29.8%, 10.2%, 0%, 11.8%` | `200.6°, 29.8%, 88.2%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#6BAED6;border:1px solid #777;border-radius:2px;"></span> | `#6BAED6` | `107, 174, 214` | `50%, 18.7%, 0%, 16.1%` | `202.4°, 50%, 83.9%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#4292C6;border:1px solid #777;border-radius:2px;"></span> | `#4292C6` | `66, 146, 198` | `66.7%, 26.3%, 0%, 22.4%` | `203.6°, 66.7%, 77.6%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#2171B5;border:1px solid #777;border-radius:2px;"></span> | `#2171B5` | `33, 113, 181` | `81.8%, 37.6%, 0%, 29%` | `207.6°, 81.8%, 71%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#08519C;border:1px solid #777;border-radius:2px;"></span> | `#08519C` | `8, 81, 156` | `94.9%, 48.1%, 0%, 38.8%` | `210.4°, 94.9%, 61.2%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#08306B;border:1px solid #777;border-radius:2px;"></span> | `#08306B` | `8, 48, 107` | `92.5%, 55.1%, 0%, 58%` | `215.8°, 92.5%, 42%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#EFF3FF;border:1px solid #777;border-radius:2px;"></span> | `#EFF3FF` | `239, 243, 255` | `6.3%, 4.7%, 0%, 0%` | `225°, 6.3%, 100%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#C6DBEF;border:1px solid #777;border-radius:2px;"></span> | `#C6DBEF` | `198, 219, 239` | `17.2%, 8.4%, 0%, 6.3%` | `209.3°, 17.2%, 93.7%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#9ECAE1;border:1px solid #777;border-radius:2px;"></span> | `#9ECAE1` | `158, 202, 225` | `29.8%, 10.2%, 0%, 11.8%` | `200.6°, 29.8%, 88.2%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#6BAED6;border:1px solid #777;border-radius:2px;"></span> | `#6BAED6` | `107, 174, 214` | `50%, 18.7%, 0%, 16.1%` | `202.4°, 50%, 83.9%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#4292C6;border:1px solid #777;border-radius:2px;"></span> | `#4292C6` | `66, 146, 198` | `66.7%, 26.3%, 0%, 22.4%` | `203.6°, 66.7%, 77.6%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#2171B5;border:1px solid #777;border-radius:2px;"></span> | `#2171B5` | `33, 113, 181` | `81.8%, 37.6%, 0%, 29%` | `207.6°, 81.8%, 71%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#084594;border:1px solid #777;border-radius:2px;"></span> | `#084594` | `8, 69, 148` | `94.6%, 53.4%, 0%, 42%` | `213.9°, 94.6%, 58%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#EFF3FF;border:1px solid #777;border-radius:2px;"></span> | `#EFF3FF` | `239, 243, 255` | `6.3%, 4.7%, 0%, 0%` | `225°, 6.3%, 100%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#BDD7E7;border:1px solid #777;border-radius:2px;"></span> | `#BDD7E7` | `189, 215, 231` | `18.2%, 6.9%, 0%, 9.4%` | `202.9°, 18.2%, 90.6%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#6BAED6;border:1px solid #777;border-radius:2px;"></span> | `#6BAED6` | `107, 174, 214` | `50%, 18.7%, 0%, 16.1%` | `202.4°, 50%, 83.9%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#3182BD;border:1px solid #777;border-radius:2px;"></span> | `#3182BD` | `49, 130, 189` | `74.1%, 31.2%, 0%, 25.9%` | `205.3°, 74.1%, 74.1%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#08519C;border:1px solid #777;border-radius:2px;"></span> | `#08519C` | `8, 81, 156` | `94.9%, 48.1%, 0%, 38.8%` | `210.4°, 94.9%, 61.2%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#DEEBF7;border:1px solid #777;border-radius:2px;"></span> | `#DEEBF7` | `222, 235, 247` | `10.1%, 4.9%, 0%, 3.1%` | `208.8°, 10.1%, 96.9%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#9ECAE1;border:1px solid #777;border-radius:2px;"></span> | `#9ECAE1` | `158, 202, 225` | `29.8%, 10.2%, 0%, 11.8%` | `200.6°, 29.8%, 88.2%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#3182BD;border:1px solid #777;border-radius:2px;"></span> | `#3182BD` | `49, 130, 189` | `74.1%, 31.2%, 0%, 25.9%` | `205.3°, 74.1%, 74.1%` | حار (> 24.0 °C) |

---

### الستايل: أرجواني ماغما عميق (أحادي اللون دافئ) (`Temp_Seq_DeepPurple`)
* **النوع:** متتابع لون واحد موحد | **المصدر:** ColorBrewer Purples / Crameri Devonian
* **الأساس العلمي:** تدرج أرجواني ملكي حديث، معتمد في خرائط الأطالس المتقدمة كبديل كارتوجرافي للأحمر التقليدي.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#FCFBFD;border:1px solid #777;border-radius:2px;"></span> | `#FCFBFD` | `252, 251, 253` | `0.4%, 0.8%, 0%, 0.8%` | `270°, 0.8%, 99.2%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#EFEDF5;border:1px solid #777;border-radius:2px;"></span> | `#EFEDF5` | `239, 237, 245` | `2.4%, 3.3%, 0%, 3.9%` | `255°, 3.3%, 96.1%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#DADAEB;border:1px solid #777;border-radius:2px;"></span> | `#DADAEB` | `218, 218, 235` | `7.2%, 7.2%, 0%, 7.8%` | `240°, 7.2%, 92.2%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#BCBDDC;border:1px solid #777;border-radius:2px;"></span> | `#BCBDDC` | `188, 189, 220` | `14.5%, 14.1%, 0%, 13.7%` | `238.1°, 14.5%, 86.3%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#9E9AC8;border:1px solid #777;border-radius:2px;"></span> | `#9E9AC8` | `158, 154, 200` | `21%, 23%, 0%, 21.6%` | `245.2°, 23%, 78.4%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#807DBA;border:1px solid #777;border-radius:2px;"></span> | `#807DBA` | `128, 125, 186` | `31.2%, 32.8%, 0%, 27.1%` | `243°, 32.8%, 72.9%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#6A51A3;border:1px solid #777;border-radius:2px;"></span> | `#6A51A3` | `106, 81, 163` | `35%, 50.3%, 0%, 36.1%` | `258.3°, 50.3%, 63.9%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#54278F;border:1px solid #777;border-radius:2px;"></span> | `#54278F` | `84, 39, 143` | `41.3%, 72.7%, 0%, 43.9%` | `266°, 72.7%, 56.1%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#3F007D;border:1px solid #777;border-radius:2px;"></span> | `#3F007D` | `63, 0, 125` | `49.6%, 100%, 0%, 51%` | `270.2°, 100%, 49%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#F2F0F7;border:1px solid #777;border-radius:2px;"></span> | `#F2F0F7` | `242, 240, 247` | `2%, 2.8%, 0%, 3.1%` | `257.1°, 2.8%, 96.9%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#DADAEB;border:1px solid #777;border-radius:2px;"></span> | `#DADAEB` | `218, 218, 235` | `7.2%, 7.2%, 0%, 7.8%` | `240°, 7.2%, 92.2%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#BCBDDC;border:1px solid #777;border-radius:2px;"></span> | `#BCBDDC` | `188, 189, 220` | `14.5%, 14.1%, 0%, 13.7%` | `238.1°, 14.5%, 86.3%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#9E9AC8;border:1px solid #777;border-radius:2px;"></span> | `#9E9AC8` | `158, 154, 200` | `21%, 23%, 0%, 21.6%` | `245.2°, 23%, 78.4%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#807DBA;border:1px solid #777;border-radius:2px;"></span> | `#807DBA` | `128, 125, 186` | `31.2%, 32.8%, 0%, 27.1%` | `243°, 32.8%, 72.9%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#6A51A3;border:1px solid #777;border-radius:2px;"></span> | `#6A51A3` | `106, 81, 163` | `35%, 50.3%, 0%, 36.1%` | `258.3°, 50.3%, 63.9%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#4A1486;border:1px solid #777;border-radius:2px;"></span> | `#4A1486` | `74, 20, 134` | `44.8%, 85.1%, 0%, 47.5%` | `268.4°, 85.1%, 52.5%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#F2F0F7;border:1px solid #777;border-radius:2px;"></span> | `#F2F0F7` | `242, 240, 247` | `2%, 2.8%, 0%, 3.1%` | `257.1°, 2.8%, 96.9%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#CBC9E2;border:1px solid #777;border-radius:2px;"></span> | `#CBC9E2` | `203, 201, 226` | `10.2%, 11.1%, 0%, 11.4%` | `244.8°, 11.1%, 88.6%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#9E9AC8;border:1px solid #777;border-radius:2px;"></span> | `#9E9AC8` | `158, 154, 200` | `21%, 23%, 0%, 21.6%` | `245.2°, 23%, 78.4%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#756BB1;border:1px solid #777;border-radius:2px;"></span> | `#756BB1` | `117, 107, 177` | `33.9%, 39.5%, 0%, 30.6%` | `248.6°, 39.5%, 69.4%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#54278F;border:1px solid #777;border-radius:2px;"></span> | `#54278F` | `84, 39, 143` | `41.3%, 72.7%, 0%, 43.9%` | `266°, 72.7%, 56.1%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#EFEDF5;border:1px solid #777;border-radius:2px;"></span> | `#EFEDF5` | `239, 237, 245` | `2.4%, 3.3%, 0%, 3.9%` | `255°, 3.3%, 96.1%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#BCBDDC;border:1px solid #777;border-radius:2px;"></span> | `#BCBDDC` | `188, 189, 220` | `14.5%, 14.1%, 0%, 13.7%` | `238.1°, 14.5%, 86.3%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#756BB1;border:1px solid #777;border-radius:2px;"></span> | `#756BB1` | `117, 107, 177` | `33.9%, 39.5%, 0%, 30.6%` | `248.6°, 39.5%, 69.4%` | حار (> 24.0 °C) |

---

### الستايل: أزرق-أبيض-أحمر (معيار IPCC ثنائي الاتجاه بمركز محايد) (`Temp_Div_RdBu_IPCC`)
* **النوع:** لونين متقابلين بمركز محايد | **المصدر:** IPCC AR6 / NOAA Climate Prediction Center
* **الأساس العلمي:** المعيار الذهبي للهيئة الحكومية الدولية لتغير المناخ وNOAA؛ يربط البرودة (أزرق) والحرارة (أحمر) بمركز محايد شاحب.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2166AC;border:1px solid #777;border-radius:2px;"></span> | `#2166AC` | `33, 102, 172` | `80.8%, 40.7%, 0%, 32.5%` | `210.2°, 80.8%, 67.5%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#4393C3;border:1px solid #777;border-radius:2px;"></span> | `#4393C3` | `67, 147, 195` | `65.6%, 24.6%, 0%, 23.5%` | `202.5°, 65.6%, 76.5%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#92C5DE;border:1px solid #777;border-radius:2px;"></span> | `#92C5DE` | `146, 197, 222` | `34.2%, 11.3%, 0%, 12.9%` | `199.7°, 34.2%, 87.1%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#D1E5F0;border:1px solid #777;border-radius:2px;"></span> | `#D1E5F0` | `209, 229, 240` | `12.9%, 4.6%, 0%, 5.9%` | `201.3°, 12.9%, 94.1%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDDBC7;border:1px solid #777;border-radius:2px;"></span> | `#FDDBC7` | `253, 219, 199` | `0%, 13.4%, 21.3%, 0.8%` | `22.2°, 21.3%, 99.2%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#F4A582;border:1px solid #777;border-radius:2px;"></span> | `#F4A582` | `244, 165, 130` | `0%, 32.4%, 46.7%, 4.3%` | `18.4°, 46.7%, 95.7%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#D6604D;border:1px solid #777;border-radius:2px;"></span> | `#D6604D` | `214, 96, 77` | `0%, 55.1%, 64%, 16.1%` | `8.3°, 64%, 83.9%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#B2182B;border:1px solid #777;border-radius:2px;"></span> | `#B2182B` | `178, 24, 43` | `0%, 86.5%, 75.8%, 30.2%` | `352.6°, 86.5%, 69.8%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2166AC;border:1px solid #777;border-radius:2px;"></span> | `#2166AC` | `33, 102, 172` | `80.8%, 40.7%, 0%, 32.5%` | `210.2°, 80.8%, 67.5%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#67A9CF;border:1px solid #777;border-radius:2px;"></span> | `#67A9CF` | `103, 169, 207` | `50.2%, 18.4%, 0%, 18.8%` | `201.9°, 50.2%, 81.2%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#D1E5F0;border:1px solid #777;border-radius:2px;"></span> | `#D1E5F0` | `209, 229, 240` | `12.9%, 4.6%, 0%, 5.9%` | `201.3°, 12.9%, 94.1%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDDBC7;border:1px solid #777;border-radius:2px;"></span> | `#FDDBC7` | `253, 219, 199` | `0%, 13.4%, 21.3%, 0.8%` | `22.2°, 21.3%, 99.2%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#F4A582;border:1px solid #777;border-radius:2px;"></span> | `#F4A582` | `244, 165, 130` | `0%, 32.4%, 46.7%, 4.3%` | `18.4°, 46.7%, 95.7%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#B2182B;border:1px solid #777;border-radius:2px;"></span> | `#B2182B` | `178, 24, 43` | `0%, 86.5%, 75.8%, 30.2%` | `352.6°, 86.5%, 69.8%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#0571B0;border:1px solid #777;border-radius:2px;"></span> | `#0571B0` | `5, 113, 176` | `97.2%, 35.8%, 0%, 31%` | `202.1°, 97.2%, 69%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#92C5DE;border:1px solid #777;border-radius:2px;"></span> | `#92C5DE` | `146, 197, 222` | `34.2%, 11.3%, 0%, 12.9%` | `199.7°, 34.2%, 87.1%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#F4A582;border:1px solid #777;border-radius:2px;"></span> | `#F4A582` | `244, 165, 130` | `0%, 32.4%, 46.7%, 4.3%` | `18.4°, 46.7%, 95.7%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#CA0020;border:1px solid #777;border-radius:2px;"></span> | `#CA0020` | `202, 0, 32` | `0%, 100%, 84.2%, 20.8%` | `350.5°, 100%, 79.2%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#67A9CF;border:1px solid #777;border-radius:2px;"></span> | `#67A9CF` | `103, 169, 207` | `50.2%, 18.4%, 0%, 18.8%` | `201.9°, 50.2%, 81.2%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#EF8A62;border:1px solid #777;border-radius:2px;"></span> | `#EF8A62` | `239, 138, 98` | `0%, 42.3%, 59%, 6.3%` | `17°, 59%, 93.7%` | حار (> 24.0 °C) |

---

### الستايل: كحلي-أصفر-قرمزي (كولور بروير القياسي بمركز أصفر دافئ) (`Temp_Div_RdYlBu_Brewer`)
* **النوع:** لونين متقابلين بمركز محايد | **المصدر:** Cynthia Brewer / ColorBrewer 2.0 RdYlBu
* **الأساس العلمي:** التدرج الكارتوجرافي الأكثر توازناً في أطالس العالم؛ المركز أصفر هادئ بدلاً من الأبيض لتجنب اختفاء الخلفية الورقية.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#313695;border:1px solid #777;border-radius:2px;"></span> | `#313695` | `49, 54, 149` | `67.1%, 63.8%, 0%, 41.6%` | `237°, 67.1%, 58.4%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#4575B4;border:1px solid #777;border-radius:2px;"></span> | `#4575B4` | `69, 117, 180` | `61.7%, 35%, 0%, 29.4%` | `214.1°, 61.7%, 70.6%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#74ADD1;border:1px solid #777;border-radius:2px;"></span> | `#74ADD1` | `116, 173, 209` | `44.5%, 17.2%, 0%, 18%` | `203.2°, 44.5%, 82%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#ABD9E9;border:1px solid #777;border-radius:2px;"></span> | `#ABD9E9` | `171, 217, 233` | `26.6%, 6.9%, 0%, 8.6%` | `195.5°, 26.6%, 91.4%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE090;border:1px solid #777;border-radius:2px;"></span> | `#FEE090` | `254, 224, 144` | `0%, 11.8%, 43.3%, 0.4%` | `43.6°, 43.3%, 99.6%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#F46D43;border:1px solid #777;border-radius:2px;"></span> | `#F46D43` | `244, 109, 67` | `0%, 55.3%, 72.5%, 4.3%` | `14.2°, 72.5%, 95.7%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#D73027;border:1px solid #777;border-radius:2px;"></span> | `#D73027` | `215, 48, 39` | `0%, 77.7%, 81.9%, 15.7%` | `3.1°, 81.9%, 84.3%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#4575B4;border:1px solid #777;border-radius:2px;"></span> | `#4575B4` | `69, 117, 180` | `61.7%, 35%, 0%, 29.4%` | `214.1°, 61.7%, 70.6%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#74ADD1;border:1px solid #777;border-radius:2px;"></span> | `#74ADD1` | `116, 173, 209` | `44.5%, 17.2%, 0%, 18%` | `203.2°, 44.5%, 82%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#ABD9E9;border:1px solid #777;border-radius:2px;"></span> | `#ABD9E9` | `171, 217, 233` | `26.6%, 6.9%, 0%, 8.6%` | `195.5°, 26.6%, 91.4%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#F46D43;border:1px solid #777;border-radius:2px;"></span> | `#F46D43` | `244, 109, 67` | `0%, 55.3%, 72.5%, 4.3%` | `14.2°, 72.5%, 95.7%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#D73027;border:1px solid #777;border-radius:2px;"></span> | `#D73027` | `215, 48, 39` | `0%, 77.7%, 81.9%, 15.7%` | `3.1°, 81.9%, 84.3%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2C7BB6;border:1px solid #777;border-radius:2px;"></span> | `#2C7BB6` | `44, 123, 182` | `75.8%, 32.4%, 0%, 28.6%` | `205.7°, 75.8%, 71.4%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#ABD9E9;border:1px solid #777;border-radius:2px;"></span> | `#ABD9E9` | `171, 217, 233` | `26.6%, 6.9%, 0%, 8.6%` | `195.5°, 26.6%, 91.4%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#D7191C;border:1px solid #777;border-radius:2px;"></span> | `#D7191C` | `215, 25, 28` | `0%, 88.4%, 87%, 15.7%` | `359.1°, 88.4%, 84.3%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#91BFDB;border:1px solid #777;border-radius:2px;"></span> | `#91BFDB` | `145, 191, 219` | `33.8%, 12.8%, 0%, 14.1%` | `202.7°, 33.8%, 85.9%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FC8D59;border:1px solid #777;border-radius:2px;"></span> | `#FC8D59` | `252, 141, 89` | `0%, 44%, 64.7%, 1.2%` | `19.1°, 64.7%, 98.8%` | حار (> 24.0 °C) |

---

### الستايل: تركواز مائي-عاجي-مرجاني دافئ (ثنائي الاتجاه حديث) (`Temp_Div_TealCoral`)
* **النوع:** لونين متقابلين بمركز محايد | **المصدر:** Esri 'Better Colors for Better Mapping' / Crameri
* **الأساس العلمي:** تصميم كارتوجرافي عصري يوفر تبايناً فائق النقاء وجماليات طباعية مع ملاءمة تامة لفاقدي تمييز الألوان.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#003C30;border:1px solid #777;border-radius:2px;"></span> | `#003C30` | `0, 60, 48` | `100%, 0%, 20%, 76.5%` | `168°, 100%, 23.5%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#01665E;border:1px solid #777;border-radius:2px;"></span> | `#01665E` | `1, 102, 94` | `99%, 0%, 7.8%, 60%` | `175.2°, 99%, 40%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#35978F;border:1px solid #777;border-radius:2px;"></span> | `#35978F` | `53, 151, 143` | `64.9%, 0%, 5.3%, 40.8%` | `175.1°, 64.9%, 59.2%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#80CDC1;border:1px solid #777;border-radius:2px;"></span> | `#80CDC1` | `128, 205, 193` | `37.6%, 0%, 5.9%, 19.6%` | `170.6°, 37.6%, 80.4%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#F5F5F5;border:1px solid #777;border-radius:2px;"></span> | `#F5F5F5` | `245, 245, 245` | `0%, 0%, 0%, 3.9%` | `0°, 0%, 96.1%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDE0EF;border:1px solid #777;border-radius:2px;"></span> | `#FDE0EF` | `253, 224, 239` | `0%, 11.5%, 5.5%, 0.8%` | `329°, 11.5%, 99.2%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#F1B6DA;border:1px solid #777;border-radius:2px;"></span> | `#F1B6DA` | `241, 182, 218` | `0%, 24.5%, 9.5%, 5.5%` | `323.4°, 24.5%, 94.5%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#DE77AE;border:1px solid #777;border-radius:2px;"></span> | `#DE77AE` | `222, 119, 174` | `0%, 46.4%, 21.6%, 12.9%` | `328°, 46.4%, 87.1%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#8E0152;border:1px solid #777;border-radius:2px;"></span> | `#8E0152` | `142, 1, 82` | `0%, 99.3%, 42.3%, 44.3%` | `325.5°, 99.3%, 55.7%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#01665E;border:1px solid #777;border-radius:2px;"></span> | `#01665E` | `1, 102, 94` | `99%, 0%, 7.8%, 60%` | `175.2°, 99%, 40%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#35978F;border:1px solid #777;border-radius:2px;"></span> | `#35978F` | `53, 151, 143` | `64.9%, 0%, 5.3%, 40.8%` | `175.1°, 64.9%, 59.2%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#80CDC1;border:1px solid #777;border-radius:2px;"></span> | `#80CDC1` | `128, 205, 193` | `37.6%, 0%, 5.9%, 19.6%` | `170.6°, 37.6%, 80.4%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#F5F5F5;border:1px solid #777;border-radius:2px;"></span> | `#F5F5F5` | `245, 245, 245` | `0%, 0%, 0%, 3.9%` | `0°, 0%, 96.1%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#F1B6DA;border:1px solid #777;border-radius:2px;"></span> | `#F1B6DA` | `241, 182, 218` | `0%, 24.5%, 9.5%, 5.5%` | `323.4°, 24.5%, 94.5%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#DE77AE;border:1px solid #777;border-radius:2px;"></span> | `#DE77AE` | `222, 119, 174` | `0%, 46.4%, 21.6%, 12.9%` | `328°, 46.4%, 87.1%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#B31B69;border:1px solid #777;border-radius:2px;"></span> | `#B31B69` | `179, 27, 105` | `0%, 84.9%, 41.3%, 29.8%` | `329.2°, 84.9%, 70.2%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#01665E;border:1px solid #777;border-radius:2px;"></span> | `#01665E` | `1, 102, 94` | `99%, 0%, 7.8%, 60%` | `175.2°, 99%, 40%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#80CDC1;border:1px solid #777;border-radius:2px;"></span> | `#80CDC1` | `128, 205, 193` | `37.6%, 0%, 5.9%, 19.6%` | `170.6°, 37.6%, 80.4%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#F5F5F5;border:1px solid #777;border-radius:2px;"></span> | `#F5F5F5` | `245, 245, 245` | `0%, 0%, 0%, 3.9%` | `0°, 0%, 96.1%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#E9A3C9;border:1px solid #777;border-radius:2px;"></span> | `#E9A3C9` | `233, 163, 201` | `0%, 30%, 13.7%, 8.6%` | `327.4°, 30%, 91.4%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#C51B7D;border:1px solid #777;border-radius:2px;"></span> | `#C51B7D` | `197, 27, 125` | `0%, 86.3%, 36.5%, 22.7%` | `325.4°, 86.3%, 77.3%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#35978F;border:1px solid #777;border-radius:2px;"></span> | `#35978F` | `53, 151, 143` | `64.9%, 0%, 5.3%, 40.8%` | `175.1°, 64.9%, 59.2%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#F5F5F5;border:1px solid #777;border-radius:2px;"></span> | `#F5F5F5` | `245, 245, 245` | `0%, 0%, 0%, 3.9%` | `0°, 0%, 96.1%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#C51B7D;border:1px solid #777;border-radius:2px;"></span> | `#C51B7D` | `197, 27, 125` | `0%, 86.3%, 36.5%, 22.7%` | `325.4°, 86.3%, 77.3%` | حار (> 24.0 °C) |

---

### الستايل: بنفسجي عميق-رمادي لؤلؤي-برتقالي برونزي (ثنائي الاتجاه متوازن) (`Temp_Div_PuOr`)
* **النوع:** لونين متقابلين بمركز محايد | **المصدر:** ColorBrewer 2.0 PuOr / CPT-City
* **الأساس العلمي:** مثالي لخرائط الشذوذ الحراري ومقارنة الفصول المتناقضة، بدرجات لونية راقية ومريحة كارتوجرافياً.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#542788;border:1px solid #777;border-radius:2px;"></span> | `#542788` | `84, 39, 136` | `38.2%, 71.3%, 0%, 46.7%` | `267.8°, 71.3%, 53.3%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#762A83;border:1px solid #777;border-radius:2px;"></span> | `#762A83` | `118, 42, 131` | `9.9%, 67.9%, 0%, 48.6%` | `291.2°, 67.9%, 51.4%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#9970AB;border:1px solid #777;border-radius:2px;"></span> | `#9970AB` | `153, 112, 171` | `10.5%, 34.5%, 0%, 32.9%` | `281.7°, 34.5%, 67.1%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#C2A5CF;border:1px solid #777;border-radius:2px;"></span> | `#C2A5CF` | `194, 165, 207` | `6.3%, 20.3%, 0%, 18.8%` | `281.4°, 20.3%, 81.2%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE0B6;border:1px solid #777;border-radius:2px;"></span> | `#FEE0B6` | `254, 224, 182` | `0%, 11.8%, 28.3%, 0.4%` | `35°, 28.3%, 99.6%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDB863;border:1px solid #777;border-radius:2px;"></span> | `#FDB863` | `253, 184, 99` | `0%, 27.3%, 60.9%, 0.8%` | `33.1°, 60.9%, 99.2%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#E08214;border:1px solid #777;border-radius:2px;"></span> | `#E08214` | `224, 130, 20` | `0%, 42%, 91.1%, 12.2%` | `32.4°, 91.1%, 87.8%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#B35806;border:1px solid #777;border-radius:2px;"></span> | `#B35806` | `179, 88, 6` | `0%, 50.8%, 96.6%, 29.8%` | `28.4°, 96.6%, 70.2%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#762A83;border:1px solid #777;border-radius:2px;"></span> | `#762A83` | `118, 42, 131` | `9.9%, 67.9%, 0%, 48.6%` | `291.2°, 67.9%, 51.4%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#9970AB;border:1px solid #777;border-radius:2px;"></span> | `#9970AB` | `153, 112, 171` | `10.5%, 34.5%, 0%, 32.9%` | `281.7°, 34.5%, 67.1%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#C2A5CF;border:1px solid #777;border-radius:2px;"></span> | `#C2A5CF` | `194, 165, 207` | `6.3%, 20.3%, 0%, 18.8%` | `281.4°, 20.3%, 81.2%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDB863;border:1px solid #777;border-radius:2px;"></span> | `#FDB863` | `253, 184, 99` | `0%, 27.3%, 60.9%, 0.8%` | `33.1°, 60.9%, 99.2%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#E08214;border:1px solid #777;border-radius:2px;"></span> | `#E08214` | `224, 130, 20` | `0%, 42%, 91.1%, 12.2%` | `32.4°, 91.1%, 87.8%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#B35806;border:1px solid #777;border-radius:2px;"></span> | `#B35806` | `179, 88, 6` | `0%, 50.8%, 96.6%, 29.8%` | `28.4°, 96.6%, 70.2%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#7B3294;border:1px solid #777;border-radius:2px;"></span> | `#7B3294` | `123, 50, 148` | `16.9%, 66.2%, 0%, 42%` | `284.7°, 66.2%, 58%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#C2A5CF;border:1px solid #777;border-radius:2px;"></span> | `#C2A5CF` | `194, 165, 207` | `6.3%, 20.3%, 0%, 18.8%` | `281.4°, 20.3%, 81.2%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDB863;border:1px solid #777;border-radius:2px;"></span> | `#FDB863` | `253, 184, 99` | `0%, 27.3%, 60.9%, 0.8%` | `33.1°, 60.9%, 99.2%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#E66101;border:1px solid #777;border-radius:2px;"></span> | `#E66101` | `230, 97, 1` | `0%, 57.8%, 99.6%, 9.8%` | `25.2°, 99.6%, 90.2%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#AF8DC3;border:1px solid #777;border-radius:2px;"></span> | `#AF8DC3` | `175, 141, 195` | `10.3%, 27.7%, 0%, 23.5%` | `277.8°, 27.7%, 76.5%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#F7F7F7;border:1px solid #777;border-radius:2px;"></span> | `#F7F7F7` | `247, 247, 247` | `0%, 0%, 0%, 3.1%` | `0°, 0%, 96.9%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDB863;border:1px solid #777;border-radius:2px;"></span> | `#FDB863` | `253, 184, 99` | `0%, 27.3%, 60.9%, 0.8%` | `33.1°, 60.9%, 99.2%` | حار (> 24.0 °C) |

---

### الستايل: التدرج الحراري العلمي المحايد إدراكياً (Batlow Thermal) (`Temp_Multi_Thermal_Crameri`)
* **النوع:** ألوان منفصلة علمية متعددة | **المصدر:** Fabio Crameri Scientific Colour Maps / CPT-City Batlow
* **الأساس العلمي:** مبني على التدرج المنتظم في فضاء CAM02-UCS؛ يمنع تماماً الخداع البصري وحدود التدرج الزائفة في Rainbow.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#481567;border:1px solid #777;border-radius:2px;"></span> | `#481567` | `72, 21, 103` | `30.1%, 79.6%, 0%, 59.6%` | `277.3°, 79.6%, 40.4%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#482677;border:1px solid #777;border-radius:2px;"></span> | `#482677` | `72, 38, 119` | `39.5%, 68.1%, 0%, 53.3%` | `265.2°, 68.1%, 46.7%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#3F4788;border:1px solid #777;border-radius:2px;"></span> | `#3F4788` | `63, 71, 136` | `53.7%, 47.8%, 0%, 46.7%` | `233.4°, 53.7%, 53.3%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#33638D;border:1px solid #777;border-radius:2px;"></span> | `#33638D` | `51, 99, 141` | `63.8%, 29.8%, 0%, 44.7%` | `208°, 63.8%, 55.3%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#287D8E;border:1px solid #777;border-radius:2px;"></span> | `#287D8E` | `40, 125, 142` | `71.8%, 12%, 0%, 44.3%` | `190°, 71.8%, 55.7%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#1F968B;border:1px solid #777;border-radius:2px;"></span> | `#1F968B` | `31, 150, 139` | `79.3%, 0%, 7.3%, 41.2%` | `174.5°, 79.3%, 58.8%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#29AF7F;border:1px solid #777;border-radius:2px;"></span> | `#29AF7F` | `41, 175, 127` | `76.6%, 0%, 27.4%, 31.4%` | `158.5°, 76.6%, 68.6%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#73D055;border:1px solid #777;border-radius:2px;"></span> | `#73D055` | `115, 208, 85` | `44.7%, 0%, 59.1%, 18.4%` | `105.4°, 59.1%, 81.6%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDE725;border:1px solid #777;border-radius:2px;"></span> | `#FDE725` | `253, 231, 37` | `0%, 8.7%, 85.4%, 0.8%` | `53.9°, 85.4%, 99.2%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#440154;border:1px solid #777;border-radius:2px;"></span> | `#440154` | `68, 1, 84` | `19%, 98.8%, 0%, 67.1%` | `288.4°, 98.8%, 32.9%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#443A83;border:1px solid #777;border-radius:2px;"></span> | `#443A83` | `68, 58, 131` | `48.1%, 55.7%, 0%, 48.6%` | `248.2°, 55.7%, 51.4%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#31688E;border:1px solid #777;border-radius:2px;"></span> | `#31688E` | `49, 104, 142` | `65.5%, 26.8%, 0%, 44.3%` | `204.5°, 65.5%, 55.7%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#21908C;border:1px solid #777;border-radius:2px;"></span> | `#21908C` | `33, 144, 140` | `77.1%, 0%, 2.8%, 43.5%` | `177.8°, 77.1%, 56.5%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#35B779;border:1px solid #777;border-radius:2px;"></span> | `#35B779` | `53, 183, 121` | `71%, 0%, 33.9%, 28.2%` | `151.4°, 71%, 71.8%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#8FD744;border:1px solid #777;border-radius:2px;"></span> | `#8FD744` | `143, 215, 68` | `33.5%, 0%, 68.4%, 15.7%` | `89.4°, 68.4%, 84.3%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDE725;border:1px solid #777;border-radius:2px;"></span> | `#FDE725` | `253, 231, 37` | `0%, 8.7%, 85.4%, 0.8%` | `53.9°, 85.4%, 99.2%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#440154;border:1px solid #777;border-radius:2px;"></span> | `#440154` | `68, 1, 84` | `19%, 98.8%, 0%, 67.1%` | `288.4°, 98.8%, 32.9%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#3B528B;border:1px solid #777;border-radius:2px;"></span> | `#3B528B` | `59, 82, 139` | `57.6%, 41%, 0%, 45.5%` | `222.8°, 57.6%, 54.5%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#21908C;border:1px solid #777;border-radius:2px;"></span> | `#21908C` | `33, 144, 140` | `77.1%, 0%, 2.8%, 43.5%` | `177.8°, 77.1%, 56.5%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#5DC863;border:1px solid #777;border-radius:2px;"></span> | `#5DC863` | `93, 200, 99` | `53.5%, 0%, 50.5%, 21.6%` | `123.4°, 53.5%, 78.4%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDE725;border:1px solid #777;border-radius:2px;"></span> | `#FDE725` | `253, 231, 37` | `0%, 8.7%, 85.4%, 0.8%` | `53.9°, 85.4%, 99.2%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#33638D;border:1px solid #777;border-radius:2px;"></span> | `#33638D` | `51, 99, 141` | `63.8%, 29.8%, 0%, 44.7%` | `208°, 63.8%, 55.3%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#35B779;border:1px solid #777;border-radius:2px;"></span> | `#35B779` | `53, 183, 121` | `71%, 0%, 33.9%, 28.2%` | `151.4°, 71%, 71.8%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDE725;border:1px solid #777;border-radius:2px;"></span> | `#FDE725` | `253, 231, 37` | `0%, 8.7%, 85.4%, 0.8%` | `53.9°, 85.4%, 99.2%` | حار (> 24.0 °C) |

---

### الستايل: مقياس المنظمة العالمية للأرصاد الجوية (WMO Climatological Standard) (`Temp_Multi_WMO_Standard`)
* **النوع:** ألوان منفصلة علمية متعددة | **المصدر:** WMO-No. 306 Manual on Codes / Synoptic Atlas
* **الأساس العلمي:** الألوان المعيارية لخرائط السينوبتيك والمناخ العالمي الصادرة عن WMO؛ متوازنة السطوع ومتدرجة بانسجام تام.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#1D3B5C;border:1px solid #777;border-radius:2px;"></span> | `#1D3B5C` | `29, 59, 92` | `68.5%, 35.9%, 0%, 63.9%` | `211.4°, 68.5%, 36.1%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#346087;border:1px solid #777;border-radius:2px;"></span> | `#346087` | `52, 96, 135` | `61.5%, 28.9%, 0%, 47.1%` | `208.2°, 61.5%, 52.9%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#5885A8;border:1px solid #777;border-radius:2px;"></span> | `#5885A8` | `88, 133, 168` | `47.6%, 20.8%, 0%, 34.1%` | `206.3°, 47.6%, 65.9%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#89ABBE;border:1px solid #777;border-radius:2px;"></span> | `#89ABBE` | `137, 171, 190` | `27.9%, 10%, 0%, 25.5%` | `201.5°, 27.9%, 74.5%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#D8E0B5;border:1px solid #777;border-radius:2px;"></span> | `#D8E0B5` | `216, 224, 181` | `3.6%, 0%, 19.2%, 12.2%` | `71.2°, 19.2%, 87.8%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#EBBF82;border:1px solid #777;border-radius:2px;"></span> | `#EBBF82` | `235, 191, 130` | `0%, 18.7%, 44.7%, 7.8%` | `34.9°, 44.7%, 92.2%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#E08E54;border:1px solid #777;border-radius:2px;"></span> | `#E08E54` | `224, 142, 84` | `0%, 36.6%, 62.5%, 12.2%` | `24.9°, 62.5%, 87.8%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#CB5633;border:1px solid #777;border-radius:2px;"></span> | `#CB5633` | `203, 86, 51` | `0%, 57.6%, 74.9%, 20.4%` | `13.8°, 74.9%, 79.6%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#A32015;border:1px solid #777;border-radius:2px;"></span> | `#A32015` | `163, 32, 21` | `0%, 80.4%, 87.1%, 36.1%` | `4.6°, 87.1%, 63.9%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2B507A;border:1px solid #777;border-radius:2px;"></span> | `#2B507A` | `43, 80, 122` | `64.8%, 34.4%, 0%, 52.2%` | `211.9°, 64.8%, 47.8%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#4E7DA6;border:1px solid #777;border-radius:2px;"></span> | `#4E7DA6` | `78, 125, 166` | `53%, 24.7%, 0%, 34.9%` | `208°, 53%, 65.1%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#82A8C2;border:1px solid #777;border-radius:2px;"></span> | `#82A8C2` | `130, 168, 194` | `33%, 13.4%, 0%, 23.9%` | `204.4°, 33%, 76.1%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#CCD9A8;border:1px solid #777;border-radius:2px;"></span> | `#CCD9A8` | `204, 217, 168` | `6%, 0%, 22.6%, 14.9%` | `75.9°, 22.6%, 85.1%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#E8B378;border:1px solid #777;border-radius:2px;"></span> | `#E8B378` | `232, 179, 120` | `0%, 22.8%, 48.3%, 9%` | `31.6°, 48.3%, 91%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#DB7A48;border:1px solid #777;border-radius:2px;"></span> | `#DB7A48` | `219, 122, 72` | `0%, 44.3%, 67.1%, 14.1%` | `20.4°, 67.1%, 85.9%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#B83321;border:1px solid #777;border-radius:2px;"></span> | `#B83321` | `184, 51, 33` | `0%, 72.3%, 82.1%, 27.8%` | `7.2°, 82.1%, 72.2%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#3D6B9C;border:1px solid #777;border-radius:2px;"></span> | `#3D6B9C` | `61, 107, 156` | `60.9%, 31.4%, 0%, 38.8%` | `210.9°, 60.9%, 61.2%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#7398B5;border:1px solid #777;border-radius:2px;"></span> | `#7398B5` | `115, 152, 181` | `36.5%, 16%, 0%, 29%` | `206.4°, 36.5%, 71%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#C5D49B;border:1px solid #777;border-radius:2px;"></span> | `#C5D49B` | `197, 212, 155` | `7.1%, 0%, 26.9%, 16.9%` | `75.8°, 26.9%, 83.1%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#E8A86B;border:1px solid #777;border-radius:2px;"></span> | `#E8A86B` | `232, 168, 107` | `0%, 27.6%, 53.9%, 9%` | `29.3°, 53.9%, 91%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#C94A29;border:1px solid #777;border-radius:2px;"></span> | `#C94A29` | `201, 74, 41` | `0%, 63.2%, 79.6%, 21.2%` | `12.4°, 79.6%, 78.8%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#4A7BB0;border:1px solid #777;border-radius:2px;"></span> | `#4A7BB0` | `74, 123, 176` | `58%, 30.1%, 0%, 31%` | `211.2°, 58%, 69%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#A3B86C;border:1px solid #777;border-radius:2px;"></span> | `#A3B86C` | `163, 184, 108` | `11.4%, 0%, 41.3%, 27.8%` | `76.6°, 41.3%, 72.2%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#D35E3E;border:1px solid #777;border-radius:2px;"></span> | `#D35E3E` | `211, 94, 62` | `0%, 55.5%, 70.6%, 17.3%` | `12.9°, 70.6%, 82.7%` | حار (> 24.0 °C) |

---

### الستايل: مقياس الأرصاد الوطنية الأمريكية المعتدل (NOAA NWS Blend) (`Temp_Multi_NOAA_NWS`)
* **النوع:** ألوان منفصلة علمية متعددة | **المصدر:** NOAA NWS National Blend of Models (NBM)
* **الأساس العلمي:** تدرج رصدي رسمي من NOAA يتميز بألوان هادئة غير صارخة تضمن التمييز الدقيق بين الكتل الهوائية الساخنة والباردة.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#1C4163;border:1px solid #777;border-radius:2px;"></span> | `#1C4163` | `28, 65, 99` | `71.7%, 34.3%, 0%, 61.2%` | `208.7°, 71.7%, 38.8%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#35668C;border:1px solid #777;border-radius:2px;"></span> | `#35668C` | `53, 102, 140` | `62.1%, 27.1%, 0%, 45.1%` | `206.2°, 62.1%, 54.9%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#5A8BAE;border:1px solid #777;border-radius:2px;"></span> | `#5A8BAE` | `90, 139, 174` | `48.3%, 20.1%, 0%, 31.8%` | `205°, 48.3%, 68.2%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#94B7CD;border:1px solid #777;border-radius:2px;"></span> | `#94B7CD` | `148, 183, 205` | `27.8%, 10.7%, 0%, 19.6%` | `203.2°, 27.8%, 80.4%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FAF1D4;border:1px solid #777;border-radius:2px;"></span> | `#FAF1D4` | `250, 241, 212` | `0%, 3.6%, 15.2%, 2%` | `45.8°, 15.2%, 98%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#EDB27C;border:1px solid #777;border-radius:2px;"></span> | `#EDB27C` | `237, 178, 124` | `0%, 24.9%, 47.7%, 7.1%` | `28.7°, 47.7%, 92.9%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#DD7752;border:1px solid #777;border-radius:2px;"></span> | `#DD7752` | `221, 119, 82` | `0%, 46.2%, 62.9%, 13.3%` | `16°, 62.9%, 86.7%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#C14534;border:1px solid #777;border-radius:2px;"></span> | `#C14534` | `193, 69, 52` | `0%, 64.2%, 73.1%, 24.3%` | `7.2°, 73.1%, 75.7%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#8A1517;border:1px solid #777;border-radius:2px;"></span> | `#8A1517` | `138, 21, 23` | `0%, 84.8%, 83.3%, 45.9%` | `359°, 84.8%, 54.1%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2A5478;border:1px solid #777;border-radius:2px;"></span> | `#2A5478` | `42, 84, 120` | `65%, 30%, 0%, 52.9%` | `207.7°, 65%, 47.1%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#4B7E9F;border:1px solid #777;border-radius:2px;"></span> | `#4B7E9F` | `75, 126, 159` | `52.8%, 20.8%, 0%, 37.6%` | `203.6°, 52.8%, 62.4%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#85ABC4;border:1px solid #777;border-radius:2px;"></span> | `#85ABC4` | `133, 171, 196` | `32.1%, 12.8%, 0%, 23.1%` | `203.8°, 32.1%, 76.9%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#F3E9C6;border:1px solid #777;border-radius:2px;"></span> | `#F3E9C6` | `243, 233, 198` | `0%, 4.1%, 18.5%, 4.7%` | `46.7°, 18.5%, 95.3%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#E59D68;border:1px solid #777;border-radius:2px;"></span> | `#E59D68` | `229, 157, 104` | `0%, 31.4%, 54.6%, 10.2%` | `25.4°, 54.6%, 89.8%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#CE5F45;border:1px solid #777;border-radius:2px;"></span> | `#CE5F45` | `206, 95, 69` | `0%, 53.9%, 66.5%, 19.2%` | `11.4°, 66.5%, 80.8%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#9E2522;border:1px solid #777;border-radius:2px;"></span> | `#9E2522` | `158, 37, 34` | `0%, 76.6%, 78.5%, 38%` | `1.5°, 78.5%, 62%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#3F6E94;border:1px solid #777;border-radius:2px;"></span> | `#3F6E94` | `63, 110, 148` | `57.4%, 25.7%, 0%, 42%` | `206.8°, 57.4%, 58%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#7AA1BE;border:1px solid #777;border-radius:2px;"></span> | `#7AA1BE` | `122, 161, 190` | `35.8%, 15.3%, 0%, 25.5%` | `205.6°, 35.8%, 74.5%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#F0E5B6;border:1px solid #777;border-radius:2px;"></span> | `#F0E5B6` | `240, 229, 182` | `0%, 4.6%, 24.2%, 5.9%` | `48.6°, 24.2%, 94.1%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#DE8555;border:1px solid #777;border-radius:2px;"></span> | `#DE8555` | `222, 133, 85` | `0%, 40.1%, 61.7%, 12.9%` | `21°, 61.7%, 87.1%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#B33B32;border:1px solid #777;border-radius:2px;"></span> | `#B33B32` | `179, 59, 50` | `0%, 67%, 72.1%, 29.8%` | `4.2°, 72.1%, 70.2%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#5C82A6;border:1px solid #777;border-radius:2px;"></span> | `#5C82A6` | `92, 130, 166` | `44.6%, 21.7%, 0%, 34.9%` | `209.2°, 44.6%, 65.1%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#E0DAA7;border:1px solid #777;border-radius:2px;"></span> | `#E0DAA7` | `224, 218, 167` | `0%, 2.7%, 25.4%, 12.2%` | `53.7°, 25.4%, 87.8%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#BA4D43;border:1px solid #777;border-radius:2px;"></span> | `#BA4D43` | `186, 77, 67` | `0%, 58.6%, 64%, 27.1%` | `5°, 64%, 72.9%` | حار (> 24.0 °C) |

---

### الستايل: الطيف الكارتوجرافي المتوازن غير الفاقع (Muted Spectral) (`Temp_Multi_SpectralMuted`)
* **النوع:** ألوان منفصلة علمية متعددة | **المصدر:** Esri 'Better Colors for Better Mapping' / ColorBrewer Spectral
* **الأساس العلمي:** بديل احترافي لطيف الرينبو القديم؛ يمر عبر الأزرق الهادئ، الأخضر اللطيف، الأصفر الرملي، البرتقالي، والقرمزي.

#### تدرج 9 فئات (9 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2B83BA;border:1px solid #777;border-radius:2px;"></span> | `#2B83BA` | `43, 131, 186` | `76.9%, 29.6%, 0%, 27.1%` | `203.1°, 76.9%, 72.9%` | بارد (< 14.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#559EB1;border:1px solid #777;border-radius:2px;"></span> | `#559EB1` | `85, 158, 177` | `52%, 10.7%, 0%, 30.6%` | `192.4°, 52%, 69.4%` | بارد معتدل (14.0 - 16.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#84C1A7;border:1px solid #777;border-radius:2px;"></span> | `#84C1A7` | `132, 193, 167` | `31.6%, 0%, 13.5%, 24.3%` | `154.4°, 31.6%, 75.7%` | لطيف (16.5 - 19.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#C2E699;border:1px solid #777;border-radius:2px;"></span> | `#C2E699` | `194, 230, 153` | `15.7%, 0%, 33.5%, 9.8%` | `88.1°, 33.5%, 90.2%` | معتدل (19.0 - 21.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.5 - 24.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#FEE08B;border:1px solid #777;border-radius:2px;"></span> | `#FEE08B` | `254, 224, 139` | `0%, 11.8%, 45.3%, 0.4%` | `44.3°, 45.3%, 99.6%` | دافئ (24.0 - 26.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | حار (26.5 - 29.0 °C) |
| **8** | <span style="display:inline-block;width:24px;height:14px;background-color:#F46D43;border:1px solid #777;border-radius:2px;"></span> | `#F46D43` | `244, 109, 67` | `0%, 55.3%, 72.5%, 4.3%` | `14.2°, 72.5%, 95.7%` | حار جداً (29.0 - 31.5 °C) |
| **9** | <span style="display:inline-block;width:24px;height:14px;background-color:#D7191C;border:1px solid #777;border-radius:2px;"></span> | `#D7191C` | `215, 25, 28` | `0%, 88.4%, 87%, 15.7%` | `359.1°, 88.4%, 84.3%` | شديد الحرارة قياسي (> 31.5 °C) |

#### تدرج 7 فئات (7 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2B83BA;border:1px solid #777;border-radius:2px;"></span> | `#2B83BA` | `43, 131, 186` | `76.9%, 29.6%, 0%, 27.1%` | `203.1°, 76.9%, 72.9%` | بارد نسبياً (< 16.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#64ABB0;border:1px solid #777;border-radius:2px;"></span> | `#64ABB0` | `100, 171, 176` | `43.2%, 2.8%, 0%, 31%` | `183.9°, 43.2%, 69%` | لطيف منعش (16.0 - 18.5 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#ABDDA4;border:1px solid #777;border-radius:2px;"></span> | `#ABDDA4` | `171, 221, 164` | `22.6%, 0%, 25.8%, 13.3%` | `112.6°, 25.8%, 86.7%` | معتدل (18.5 - 21.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.0 - 23.5 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | دافئ نسبياً (23.5 - 26.0 °C) |
| **6** | <span style="display:inline-block;width:24px;height:14px;background-color:#F46D43;border:1px solid #777;border-radius:2px;"></span> | `#F46D43` | `244, 109, 67` | `0%, 55.3%, 72.5%, 4.3%` | `14.2°, 72.5%, 95.7%` | حار (26.0 - 28.5 °C) |
| **7** | <span style="display:inline-block;width:24px;height:14px;background-color:#D7191C;border:1px solid #777;border-radius:2px;"></span> | `#D7191C` | `215, 25, 28` | `0%, 88.4%, 87%, 15.7%` | `359.1°, 88.4%, 84.3%` | شديد الحرارة (> 28.5 °C) |

#### تدرج 5 فئات (5 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#2B83BA;border:1px solid #777;border-radius:2px;"></span> | `#2B83BA` | `43, 131, 186` | `76.9%, 29.6%, 0%, 27.1%` | `203.1°, 76.9%, 72.9%` | لطيف منعش (< 18.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#ABDDA4;border:1px solid #777;border-radius:2px;"></span> | `#ABDDA4` | `171, 221, 164` | `22.6%, 0%, 25.8%, 13.3%` | `112.6°, 25.8%, 86.7%` | معتدل نموذجي (18.0 - 21.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (21.0 - 24.0 °C) |
| **4** | <span style="display:inline-block;width:24px;height:14px;background-color:#FDAE61;border:1px solid #777;border-radius:2px;"></span> | `#FDAE61` | `253, 174, 97` | `0%, 31.2%, 61.7%, 0.8%` | `29.6°, 61.7%, 99.2%` | حار (24.0 - 27.0 °C) |
| **5** | <span style="display:inline-block;width:24px;height:14px;background-color:#D7191C;border:1px solid #777;border-radius:2px;"></span> | `#D7191C` | `215, 25, 28` | `0%, 88.4%, 87%, 15.7%` | `359.1°, 88.4%, 84.3%` | شديد الحرارة (> 27.0 °C) |

#### تدرج 3 فئات (3 Classes):
| الفئة | العينة | كود HEX | قيم RGB | قيم CMYK (للطباعة) | قيم HSV | الوصف والمدى |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | <span style="display:inline-block;width:24px;height:14px;background-color:#99D594;border:1px solid #777;border-radius:2px;"></span> | `#99D594` | `153, 213, 148` | `28.2%, 0%, 30.5%, 16.5%` | `115.4°, 30.5%, 83.5%` | معتدل مائل للبرودة (< 20.0 °C) |
| **2** | <span style="display:inline-block;width:24px;height:14px;background-color:#FFFFBF;border:1px solid #777;border-radius:2px;"></span> | `#FFFFBF` | `255, 255, 191` | `0%, 0%, 25.1%, 0%` | `60°, 25.1%, 100%` | معتدل دافئ (20.0 - 24.0 °C) |
| **3** | <span style="display:inline-block;width:24px;height:14px;background-color:#FC8D59;border:1px solid #777;border-radius:2px;"></span> | `#FC8D59` | `252, 141, 89` | `0%, 44%, 64.7%, 1.2%` | `19.1°, 64.7%, 98.8%` | حار (> 24.0 °C) |

---

## 5. دليل استخدام وتطبيق الستايلات داخل ArcMap 10.8 و ArcGIS Pro و QGIS

### أ. التطبيق داخل ArcMap 10.8 عبر ملفات `.clr` (الأسرع والأدق):
1. من صندوق الأدوات **ArcToolbox** افتح:  
   `Data Management Tools` $\rightarrow$ `Raster` $\rightarrow$ `Raster Properties` $\rightarrow$ **`Add Colormap`**.
2. في خانة **Input Raster**: اختر راستر درجات الحرارة المصنف (أو طبقة العرض المصنفة `_cls.tif`).
3. في خانة **Input Colormap File (.clr)**: اضغط تصفح واختر ملف `.clr` المناسب من مجلد:
   `c:\Users\ahmad\Desktop\NASA POWER Climate Atlas Generator\style\01_Temperature\CLR\`
4. اضغط **OK**؛ سيتم فوراً تطبيق الألوان الكارتوجرافية بدقة 100%.

### ب. التطبيق التلقائي عبر أداة الأطلس (Atlas Generator):
* تقوم أداة الأطلس `POWER_Climate_Atlas_Generator_10_8.pyt` تلقائياً بقراءة ملفات الستايل هذه وتطبيق تدرجات الألوان وإنشاء ملفات `.lyr` و `.lyr.json` متطابقة مع هذه المعايير.

### ج. التطبيق في QGIS:
* انقر بزر الفأرة الأيمن على طبقة الراستر $\rightarrow$ **Properties** $\rightarrow$ **Symbology** $\rightarrow$ اضغط زر **Style** بالأسفل $\rightarrow$ **Load Style...** واختر ملف `.qml` من مجلد `QML/`.

---

## 6. المصادر والمراجع الرسمية المعتمدة (Sources & References)
* 📂 **المجلد الخاص بمصادر الحرارة:** [`Source_of_Style_and_Color/`](file:///C:/Users/ahmad/Desktop/NASA POWER Climate Atlas Generator/style/01_Temperature/Source_of_Style_and_Color/)
* 📖 [دليل المراجع الخاص بستايلات الحرارة: Temperature_Sources_and_References.md](file:///C:/Users/ahmad/Desktop/NASA POWER Climate Atlas Generator/style/01_Temperature/Source_of_Style_and_Color/Temperature_Sources_and_References.md)
* 🌐 [مستودع المصادر العام لجميع العناصر: style/Source_of_Style_and_Color/README.md](file:///C:/Users/ahmad/Desktop/NASA POWER Climate Atlas Generator/style/Source_of_Style_and_Color/README.md)

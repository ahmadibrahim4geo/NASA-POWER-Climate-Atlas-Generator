# Comprehensive Climate Indicators & Fields Reference Table
# جدول المرجع الشامل لجميع المؤشرات والحقول المناخية للطبقات الـ 18 الموديلية

[![Developer](https://img.shields.io/badge/Developer-Ahmad%20Ibrahim-1F4E79.svg?style=for-the-badge&logo=github)](https://github.com/ahmadibrahim4geo)
[![Repository](https://img.shields.io/badge/Repository-NASA--POWER--Climate--Atlas--Generator-blue.svg)](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)
[![Excel Reference](https://img.shields.io/badge/Excel%20Dictionary-Fields__AR__EN__Units.xlsx-green.svg)](../Fields_AR_EN_Units.xlsx)

---

## نظرة عامة | Overview
يوثق هذا الدليل كافة الحقول الإدارية والمؤشرات المناخية والبيومناخية المصدرة في قاعدة البيانات الجغرافية المعتمدة (`Climate_Database.gdb`).
تمت مواءمة وهندسة المنظومة بالكامل لتعتمد **18 طبقة معالم موديلية منفصلة (18 Modular Feature Classes)** ومطابقة بنسبة 1:1 مع مجلدات الراستر، وتجريد كافة الطبقات من الحقول الزائدة أو المكررة، وضمان التسلسل التام للمعرف الرقمي `OBJECTID` بدون فجوات أو قيم خالية.

---

## 1. الحقول الإدارية والوصفية الموحدة (Administrative & Metadata Fields)
تتواجد هذه الحقول في بداية كل طبقة من الطبقات الـ 18 لتوثيق هوية النقطة والمعالجة:

| اسم الحقل (Field Name) | النوع (Type) | الاسم بالعربية (Name AR) | التوصيف بالإنجليزية (Description EN) | المصدر والاستخدام |
|:---|:---:|---|---|---|
| `OBJECTID` | OID | المعرف الفريد | Unique Object Identifier | معرف تسلسلي رقمي منتظم من 1 إلى N |
| `Point_ID` | LONG | معرف النقطة | Point Identifier | معرف تسلسلي للنقطة |
| `Point_Lat` | DOUBLE | دائرة العرض | Latitude (WGS 84) | الإحداثي الشمالي بالدرجات العشرية |
| `Point_Lon` | DOUBLE | خط الطول | Longitude (WGS 84) | الإحداثي الشرقي بالدرجات العشرية |
| `Elev_m` | DOUBLE | الارتفاع عن سطح البحر | Elevation (meters) | الارتفاع الطبوغرافي الرقمي |
| `Data_Start` | TEXT | بداية فترة البيانات | Start Date / Year of Time Series | بداية السلسلة الزمنية المحسوبة |
| `Data_End` | TEXT | نهاية فترة البيانات | End Date / Year of Time Series | نهاية السلسلة الزمنية المحسوبة |
| `Temporal` | TEXT | الدقة الزمنية | Temporal Frequency | دقة البيانات (Daily / Monthly / Precalc) |
| `Interp_Meth`| TEXT | خوارزمية الاستيفاء | Spatial Interpolation Method | خوارزمية السطح (IDW / Kriging / Spline) |
| `Cell_Size` | DOUBLE | حجم خلية الراستر | Base Raster Cell Size | دقة الخلية بوحدات الإسقاط |
| `Wind_Cell` | DOUBLE | حجم خلية أسهم الرياح | Wind Grid Cell Size | تباعد شبكة أسهم الرياح |
| `Status` | TEXT | حالة المعالجة | Processing Status | حالة المعالجة الحسابية (`OK` / `FAILED`) |
| `Error_Msg` | TEXT | رسالة الخطأ | Error Diagnostics | رسالة تشخيص الخطأ إن وجدت |

---

## 2. درجات الحرارة (`01_Temperature`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `T_Annual_Mean` | متوسط درجة الحرارة السنوي | Annual | °C | المتوسط الحسابي للشهور الـ 12: $\bar{T}_{ann} = \frac{1}{12}\sum T_m$ |
| `T_Winter_Mean` | متوسط درجة حرارة الشتاء | Winter (DJF) | °C | متوسط شهور ديسمبر، يناير، فبراير |
| `T_Spring_Mean` | متوسط درجة حرارة الربيع | Spring (MAM) | °C | متوسط شهور مارس، أبريل، مايو |
| `T_Summer_Mean` | متوسط درجة حرارة الصيف | Summer (JJA) | °C | متوسط شهور يونيو، يوليو، أغسطس |
| `T_Autumn_Mean` | متوسط درجة حرارة الخريف | Autumn (SON) | °C | متوسط شهور سبتمبر، أكتوبر، نوفمبر |
| `T_Annual_Range` | المدى الحراري السنوي | Annual | °C | الفارق بين أدفأ وأبرد شهور السنة: $T_{max,m} - T_{min,m}$ |
| `T_Max_Summer_Month_Mean` | متوسط أدفأ شهور الصيف | Summer | °C | أعلى متوسط شهري مسجل خلال شهور الصيف (JJA) |
| `T_Min_Winter_Month_Mean` | متوسط أبرد شهور الشتاء | Winter | °C | أدنى متوسط شهري مسجل خلال شهور الشتاء (DJF) |
| `T_Annual_Max_Mean` | المتوسط السنوي للنهايات العظمى | Annual | °C | المتوسط المناخي للنهايات العظمى اليومية ($T_{2M,MAX}$) |
| `T_Annual_Min_Mean` | المتوسط السنوي للنهايات الصغرى | Annual | °C | المتوسط المناخي للنهايات الصغرى اليومية ($T_{2M,MIN}$) |

---

## 3. التساقط والأمطار (`02_Precipitation`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `R_Annual_Mean` | المتوسط السنوي لتساقط الأمطار | Annual | مم/سنة (mm/year) | المتوسط السنوي لتساقط الأمطار (متوسط مجاميع السنين على مدار فترة الرصد) |
| `R_Month_Mean` | المتوسط الشهري لتساقط الأمطار | Monthly | مم/شهر (mm/month) | معدل الهطول الشهري المناخي: $R_{Annual\_Mean} / 12$ |
| `R_Annual_Range` | المدى السنوي لتساقط الأمطار | Annual | ملم (mm) | الفارق بين أعلى شهر مطراً وأقل شهر مطراً في السنة |
| `R_Seasonal_Range` | المدى الفصلي لتساقط الأمطار | Annual | ملم (mm) | الفارق بين أعلى فصل مطراً وأقل فصل مطراً في السنة |
| `R_Winter_Mean` | متوسط هطول الأمطار خلال فصل الشتاء | Winter (DJF) | مم/فصل (mm/season) | متوسط مجموع أمطار أشهر الشتاء (ديسمبر، يناير، فبراير) عبر السنوات |
| `R_Spring_Mean` | متوسط هطول الأمطار خلال فصل الربيع | Spring (MAM) | مم/فصل (mm/season) | متوسط مجموع أمطار أشهر الربيع (مارس، أبريل، مايو) عبر السنوات |
| `R_Summer_Mean` | متوسط هطول الأمطار خلال فصل الصيف | Summer (JJA) | مم/فصل (mm/season) | متوسط مجموع أمطار أشهر الصيف (يونيو، يوليو، أغسطس) عبر السنوات |
| `R_Autumn_Mean` | متوسط هطول الأمطار خلال فصل الخريف | Autumn (SON) | مم/فصل (mm/season) | متوسط مجموع أمطار أشهر الخريف (سبتمبر، أكتوبر، نوفمبر) عبر السنوات |

---

## 4. ضغط مستوى سطح البحر (`03_Sea_Level_Pressure`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `PSL_Annual_Mean` | متوسط الضغط عند مستوى سطح البحر | Annual | hPa / mbar | الضغط الجوي المناخي المصحح لمستوى البحر القياسي |
| `PSL_Winter_Mean` | متوسط ضغط سطح البحر شتاءً | Winter (DJF) | hPa / mbar | متوسط الضغط المصحح لشهور الشتاء |
| `PSL_Spring_Mean` | متوسط ضغط سطح البحر ربيعاً | Spring (MAM) | hPa / mbar | متوسط الضغط المصحح لشهور الربيع |
| `PSL_Summer_Mean` | متوسط ضغط سطح البحر صيفاً | Summer (JJA) | hPa / mbar | متوسط الضغط المصحح لشهور الصيف |
| `PSL_Autumn_Mean` | متوسط ضغط سطح البحر خريفاً | Autumn (SON) | hPa / mbar | متوسط الضغط المصحح لشهور الخريف |
| `PSL_Annual_Range` | المدى السنوي لضغط سطح البحر | Annual | hPa / mbar | الفارق بين أعلى وأدنى متوسط شهري للضغط |

---

## 5. الضغط الجوي السطحي الفعلي (`04_Surface_Pressure`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `PS_Annual_Mean` | متوسط الضغط الجوي السطحي الفعلي | Annual | hPa / mbar | الضغط الجوي الحقيقي عند منسوب المحطة الطبوغرافي |
| `PS_Winter_Mean` | متوسط الضغط السطحي شتاءً | Winter (DJF) | hPa / mbar | متوسط الضغط السطحي لشهور الشتاء |
| `PS_Spring_Mean` | متوسط الضغط السطحي ربيعاً | Spring (MAM) | hPa / mbar | متوسط الضغط السطحي لشهور الربيع |
| `PS_Summer_Mean` | متوسط الضغط السطحي صيفاً | Summer (JJA) | hPa / mbar | متوسط الضغط السطحي لشهور الصيف |
| `PS_Autumn_Mean` | متوسط الضغط السطحي خريفاً | Autumn (SON) | hPa / mbar | متوسط الضغط السطحي لشهور الخريف |
| `PS_Annual_Range` | المدى السنوي للضغط السطحي | Annual | hPa / mbar | التذبذب البارومتري السنوي للضغط السطحي |

---

## 6. الرياح السطحية (`05_Wind`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `W_Spd_Annual_Mean` | متوسط سرعة الرياح السنوي | Annual | m/s | متوسط سرعة الرياح عند ارتفاع 10 أمتار |
| `W_Spd_Winter_Mean` | متوسط سرعة الرياح شتاءً | Winter (DJF) | m/s | متوسط سرعة الرياح لشهور الشتاء |
| `W_Spd_Spring_Mean` | متوسط سرعة الرياح ربيعاً | Spring (MAM) | m/s | متوسط سرعة الرياح لشهور الربيع |
| `W_Spd_Summer_Mean` | متوسط سرعة الرياح صيفاً | Summer (JJA) | m/s | متوسط سرعة الرياح لشهور الصيف |
| `W_Spd_Autumn_Mean` | متوسط سرعة الرياح خريفاً | Autumn (SON) | m/s | متوسط سرعة الرياح لشهور الخريف |
| `W_Dir_Annual_Mean` | الاتجاه السائد السنوي للرياح | Annual | degrees (°) | المتوسط الدائري للمتجهات: $\text{atan2}(\sum \sin \theta, \sum \cos \theta)$ |
| `W_Dir_Winter_Mean` | اتجاه الرياح السائد شتاءً | Winter (DJF) | degrees (°) | المتوسط الدائري للاتجاه في الشتاء |
| `W_Dir_Spring_Mean` | اتجاه الرياح السائد ربيعاً | Spring (MAM) | degrees (°) | المتوسط الدائري للاتجاه في الربيع |
| `W_Dir_Summer_Mean` | اتجاه الرياح السائد صيفاً | Summer (JJA) | degrees (°) | المتوسط الدائري للاتجاه في الصيف |
| `W_Dir_Autumn_Mean` | اتجاه الرياح السائد خريفاً | Autumn (SON) | degrees (°) | المتوسط الدائري للاتجاه في الخريف |
| `W_Spd_Annual_Max_Month` | أقصى سرعة شهرية مسجلة للرياح | Annual | m/s | أعلى متوسط شهري مسجل للرياح |
| `W_Spd_Annual_Min_Month` | أدنى سرعة شهرية مسجلة للرياح | Annual | m/s | أدنى متوسط شهري مسجل للرياح |
| `W_Spd_Annual_Range` | المدى السنوي لسرعة الرياح | Annual | m/s | الفارق بين أشد وأهدأ الشهور رياحاً |

---

## 7. الرطوبة النسبية (`06_Relative_Humidity`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `RH_Annual_Mean` | متوسط الرطوبة النسبية السنوي | Annual | % | متوسط الرطوبة النسبية للهواء عند ارتفاع مترين |
| `RH_Winter_Mean` | متوسط الرطوبة النسبية شتاءً | Winter (DJF) | % | متوسط الرطوبة النسبية لشهور الشتاء |
| `RH_Spring_Mean` | متوسط الرطوبة النسبية ربيعاً | Spring (MAM) | % | متوسط الرطوبة النسبية لشهور الربيع |
| `RH_Summer_Mean` | متوسط الرطوبة النسبية صيفاً | Summer (JJA) | % | متوسط الرطوبة النسبية لشهور الصيف |
| `RH_Autumn_Mean` | متوسط الرطوبة النسبية خريفاً | Autumn (SON) | % | متوسط الرطوبة النسبية لشهور الخريف |
| `RH_Annual_Range` | المدى السنوي للرطوبة النسبية | Annual | % | الفارق بين أكثر وأقل الشهور رطوبة |

---

## 8. نقطة الندى (`07_Dew_Point`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `Td_Annual_Mean` | المتوسط السنوي لدرجة حرارة نقطة الندى | Annual | °C | متوسط درجة حرارة نقطة الندى السنوية المحسوبة عند 2 متر |
| `Td_Winter_Mean` | متوسط نقطة الندى لفصل الشتاء | Winter (DJF) | °C | متوسط نقطة الندى لشهور الشتاء (ديسمبر، يناير، فبراير) |
| `Td_Spring_Mean` | متوسط نقطة الندى لفصل الربيع | Spring (MAM) | °C | متوسط نقطة الندى لشهور الربيع (مارس، أبريل، مايو) |
| `Td_Summer_Mean` | متوسط نقطة الندى لفصل الصيف | Summer (JJA) | °C | متوسط نقطة الندى لشهور الصيف (مؤشر مباشر للرطوبة الخانقة والكتمة) |
| `Td_Autumn_Mean` | متوسط نقطة الندى لفصل الخريف | Autumn (SON) | °C | متوسط نقطة الندى لشهور الخريف (سبتمبر، أكتوبر، نوفمبر) |
| `Td_Annual_Range` | المدى السنوي لنقطة الندى | Annual | °C | الفارق بين أعلى وأدنى متوسط شهري لدرجة حرارة نقطة الندى |

---

## 9. الإشعاع الشمسي (`08_Solar_Radiation`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `Sol_Annual_Mean` | متوسط الإشعاع الشمسي اليومي | Annual | kWh/m²/day | تدفق الإشعاع الشمسي الكلي السطحي في كافة ظروف السماء |
| `Sol_Annual_Total` | إجمالي الطاقة الشمسية السنوية التراكمية | Annual | kWh/m²/year | الإشعاع التراكمي السنوي: $\sum (Sol_m \times \text{days}_m)$ |
| `Sol_Winter_Mean` | متوسط الإشعاع الشمسي شتاءً | Winter (DJF) | kWh/m²/day | متوسط الإشعاع اليومي لشهور الشتاء |
| `Sol_Spring_Mean` | متوسط الإشعاع الشمسي ربيعاً | Spring (MAM) | kWh/m²/day | متوسط الإشعاع اليومي لشهور الربيع |
| `Sol_Summer_Mean` | متوسط الإشعاع الشمسي صيفاً | Summer (JJA) | kWh/m²/day | متوسط الإشعاع اليومي لشهور الصيف |
| `Sol_Autumn_Mean` | متوسط الإشعاع الشمسي خريفاً | Autumn (SON) | kWh/m²/day | متوسط الإشعاع اليومي لشهور الخريف |
| `Sol_Annual_Range` | المدى السنوي للإشعاع الشمسي | Annual | kWh/m²/day | الفارق بين ذروة الصيف وأدنى إشعاع في الشتاء |

---

## 10. مؤشر الأشعة فوق البنفسجية (`09_UV_Index`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `UV_Annual_Mean` | متوسط مؤشر الأشعة فوق البنفسجية السنوي | Annual | index (0–15+) | مؤشر شدة الأشعة عند الظهيرة وفق منظمة الصحة العالمية |
| `UV_Winter_Mean` | متوسط مؤشر UV شتاءً | Winter (DJF) | index | متوسط مؤشر الأشعة لشهور الشتاء |
| `UV_Spring_Mean` | متوسط مؤشر UV ربيعاً | Spring (MAM) | index | متوسط مؤشر الأشعة لشهور الربيع |
| `UV_Summer_Mean` | متوسط مؤشر UV صيفاً | Summer (JJA) | index | متوسط مؤشر الأشعة لشهور الصيف (مخاطر التعرض القصوى) |
| `UV_Autumn_Mean` | متوسط مؤشر UV خريفاً | Autumn (SON) | index | متوسط مؤشر الأشعة لشهور الخريف |
| `UV_Annual_Range` | المدى السنوي لمؤشر الأشعة UV | Annual | index | الفارق بين ذروة الصيف الشديدة وأدنى مستويات الشتاء |

---

## 11. الغطاء السحابي (`10_Cloud_Cover`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `Cld_Annual_Mean` | متوسط نسبة تغطية السحب السنوي | Annual | % | النسبة المئوية للمتوسط السنوي لتغطية الغيوم |
| `Cld_Winter_Mean` | متوسط تغطية السحب شتاءً | Winter (DJF) | % | نسبة تغطية السحب لشهور الشتاء |
| `Cld_Spring_Mean` | متوسط تغطية السحب ربيعاً | Spring (MAM) | % | نسبة تغطية السحب لشهور الربيع |
| `Cld_Summer_Mean` | متوسط تغطية السحب صيفاً | Summer (JJA) | % | نسبة تغطية السحب لشهور الصيف |
| `Cld_Autumn_Mean` | متوسط تغطية السحب خريفاً | Autumn (SON) | % | نسبة تغطية السحب لشهور الخريف |
| `Cld_Annual_Range` | المدى السنوي لتغطية السحب | Annual | % | الفارق بين أكثر الشهور غيوماً وأكثرها صفاءً |

---

## 12. مؤشرات الحرارة المحسوسة والإجهاد الحراري (`11_Heat_Index`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `HI_Annual_Mean` | متوسط مؤشر الحرارة المحسوسة السنوي | Annual | °C | معادلة ستيدمان وروثفوس لحساب الحرارة الظاهرية مع الرطوبة |
| `HI_Summer_Mean` | متوسط مؤشر الحرارة المحسوسة صيفاً | Summer (JJA) | °C | متوسط مؤشر الحرارة المحسوسة خلال شهور الصيف |
| `HI_Winter_Mean` | متوسط مؤشر الحرارة المحسوسة شتاءً | Winter (DJF) | °C | مؤشر Humidex الشتوي لحساب الحرارة الظاهرية في الأجواء الباردة الرطبة |
| `HI_Annual_Range` | المدى السنوي لمؤشر الحرارة المحسوسة | Annual | °C | فارق الإجهاد الحراري السنوي بين أدفأ وأبرد الشهور |
| `WBGT_Summer_Mean` | متوسط الإجهاد الحراري الصيفي (WBGT) | Summer (JJA) | °C | الإجهاد الحراري الرطب المظلل الصيفي: $0.7 T_{nwb} + 0.3 T$ (معيار ISO 7243) |

---

## 13. مؤشر البرودة الريحية (`12_Wind_Chill`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `WC_Winter_Mean` | متوسط البرودة الريحية شتاءً | Winter (DJF) | °C | صيغة NWS لخفض الحرارة بفعل سرعة الرياح: $13.12 + 0.6215T - 11.37V^{0.16} + 0.3965TV^{0.16}$ |
| `WC_Annual_Mean` | المتوسط السنوي للبرودة الريحية | Annual | °C | المتوسط السنوي لتأثير البرودة الريحية |

---

## 14. مؤشر دي مارتون للقحولة (`13_De_Martonne_Aridity`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `DM_Aridity_Annual` | مؤشر دي مارتون للقحولة والجفاف | Annual | index | $I_{DM} = \frac{P}{T + 10}$ (<5 قاحل فائق، 5-10 جاف، 10-20 شبه جاف، 20-30 شبه رطب، >30 رطب) |

---

## 15. البخر والنتح المرجعي (`14_Evapotranspiration`)
يعتمد هذا الموديل كلياً على معادلة **Hargreaves-Samani (1985)** والمعتمدة لدى منظمة الأغذية والزراعة للأمم المتحدة في كراس الري والصرف رقم 56 (**FAO-56 Irrigation and Drainage**):
$$ET_o = 0.0023 \cdot R_a \cdot (T_{mean} + 17.8) \cdot \sqrt{T_{max} - T_{min}} \cdot \text{Days}$$
حيث يُحسب الإشعاع الشمسي خارج الغلاف الجوي ($R_a$) بدقة فلكية لكل شهر وفق دائرة العرض وزاوية الميل.

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `ET_Annual_Total` | المجموع السنوي للبخر والنتح الممكن | Annual | mm/year | التراكم السنوي للبخر والنتح بهارجريفز: $\sum ET_{month}$ |
| `ET_Annual_Mean` | المتوسط الشهري السنوي للبخر والنتح | Annual | mm/month | المعدل الشهري للبخر والنتح: $ET_{ann} / 12$ |
| `ET_Annual_Range` | المدى الشهري السنوي للبخر والنتح | Annual | mm/month | الفارق بين أعلى شهر في البخر والنتح وأدنى شهر: $\max(ET_m) - \min(ET_m)$ |
| `ET_Seasonal_Range` | المدى الفصلي للبخر والنتح | Annual | mm | الفارق بين أعلى فصل في البخر والنتح وأدنى فصل: $\max(ET_{seas}) - \min(ET_{seas})$ |
| `ET_Winter_Total` | مجموع البخر والنتح لفصل الشتاء | Winter (DJF) | mm | مجموع البخر والنتح لشهور ديسمبر، يناير، فبراير |
| `ET_Spring_Total` | مجموع البخر والنتح لفصل الربيع | Spring (MAM) | mm | مجموع البخر والنتح لشهور مارس، أبريل، مايو |
| `ET_Summer_Total` | مجموع البخر والنتح لفصل الصيف | Summer (JJA) | mm | مجموع البخر والنتح لشهور يونيو، يوليو، أغسطس |
| `ET_Autumn_Total` | مجموع البخر والنتح لفصل الخريف | Autumn (SON) | mm | مجموع البخر والنتح لشهور سبتمبر، أكتوبر، نوفمبر |
| `PET_Hargreaves_Annual` | التبخر-نتح الكامن بهارجريفز (حقل رديف) | Annual | mm/year | حقل رديف مطابق لـ `ET_Annual_Total` لضمان التوافقية مع الأنظمة القديمة |

---

## 16. مؤشر القحولة العالمي للأمم المتحدة (`15_UNEP_Aridity`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `UNEP_Aridity_Annual` | مؤشر القحولة العالمي (UNEP) | Annual | ratio | $AI = \frac{P}{ET_{ann}}$ (<0.05 قاحل جداً، 0.05-0.20 جاف، 0.20-0.50 شبه قاحل، >0.65 رطب) |

---

## 17. العجز المائي المناخي (`16_Water_Deficit`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `Water_Deficit_Annual` | الموازنة / العجز المائي المناخي | Annual | mm/year | الفائض أو العجز الصافي السنوي: $WD = P - ET_{ann}$ (القيم السالبة تمثل عجزاً مائياً) |

---

## 18. الأشهر الجافة بيولوجياً (`17_Dry_Months`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `Dry_Months_Count` | عدد الأشهر الجافة بيولوجياً | Annual | months (0–12) | عدد الشهور التي يتحقق فيها شرط والتر-ليث البيومناخي ($P_{month} < 2 \times T_{month}$) |

---

## 19. الاتجاهات والشذوذ المناخي (`18_Trends_And_Anomalies`)

| اسم الحقل (Field Name) | الاسم بالعربية (Name AR) | الفترة (Period) | الوحدة (Unit) | المعادلة والتوصيف الفيزيائي |
|:---|---|:---:|:---:|---|
| `T_Trend_Decade` | اتجاه الحرارة في العقد | Decadal | °C/decade | ميل انحدار المربعات الصغرى لدرجة الحرارة مضروباً في 10 سنوات |
| `R_Trend_Decade` | اتجاه الأمطار في العقد | Decadal | mm/decade | ميل انحدار المربعات الصغرى للتساقط مضروباً في 10 سنوات |
| `T_Anom_Annual` | شذوذ الحرارة السنوي عن 1991–2020 | Annual | °C | الفارق بين متوسط الفترة وخط الأساس المناخي المعتمد 1991–2020 |
| `T_Anom_Winter` | شذوذ حرارة الشتاء عن 1991–2020 | Winter (DJF) | °C | شذوذ حرارة شهور الشتاء مقارنة بخط أساس 1991–2020 |
| `T_Anom_Summer` | شذوذ حرارة الصيف عن 1991–2020 | Summer (JJA) | °C | شذوذ حرارة شهور الصيف مقارنة بخط أساس 1991–2020 |
| `R_Anom_Annual` | شذوذ الأمطار السنوي عن 1991–2020 | Annual | mm/year | الفارق المطلق في كمية الأمطار مقارنة بخط الأساس |
| `R_Anom_Annual_Pct` | شذوذ الأمطار السنوي بالنسبة المئوية | Annual | % | الشذوذ النسبي المئوي للأمطار: $(\Delta P / P_{base}) \times 100$ |
| `R_Anom_Winter` | شذوذ أمطار الشتاء عن 1991–2020 | Winter (DJF) | mm | الفارق المطلق لأمطار الشتاء مقارنة بخط الأساس |
| `R_Anom_Winter_Pct` | شذوذ أمطار الشتاء بالنسبة المئوية | Winter (DJF) | % | الشذوذ النسبي المئوي لأمطار الشتاء |

---

## Architectural System Statistics
* **Total Independent Modular Layers:** 18 Feature Classes and 18 1:1 matching Raster Folders.
* **Total Specialized Scientific Indicators:** 247 Climate & Bioclimatic Indicators (103 annual, seasonal, and derived + 144 climatological monthly indicators across all 12 calendar months).
* **Total Schema Columns:** 259 Total Defined Fields (including 12 administrative, geodetic, and run tracking fields).
* **Dual-Sheet Excel Workbooks:** Every element Excel workbook contains `Data` (Annual/Seasonal) and `Month` (12-month profile) sheets.
* **Export Interoperability:** Full export support for File Geodatabase (`.gdb`), Shapefiles (`.shp` with collision-free $\le 10$-character abbreviations via `SHP_FIELD_MAP`), and formatted Excel workbooks (`.xlsx` and `.xls`).

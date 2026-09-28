# ستايل أسهم الرياح — 05_Wind_Arrows.style

**100 رمز: 25 شكل × 4 اتجاهات ثابتة (N/E/S/W)** — 25 رمز في كل كاتيجوري.

## المحتوى
- مثلثات: `Tri_Black/Navy/Red_Khamsin/Blue/Orange_Dust/Green_Calm` + `SmlTri_Black/Navy`
- أسهم شمال: `Arrow_Thin_Black/Bold_Navy/Red` + `Dbl_Black/Blue` + `Heavy_Black/Red`
- مسننة/شرائط: `Barb_Black/Navy` + `Tail_Blue` + `Wedge_Orange` + `Play_Black` + `Simple_Black`
- عصاية: `Shaft_Black/Navy/Red/Blue`
- كل شكل له 4 نسخ: `..._N` `..._E` `..._S` `..._W` بزوايا ثابتة صحيحة.

## استخدامان
1. **اتجاهات ثابتة (بدون Rotation):** اختار الرمز الجاهز حسب الربع — `Unique Values` على حقل ربع الاتجاه أو اختيار يدوي.
2. **دوران مستمر (الأدق):** استخدم نسخة `_N` فقط مع `Advanced > Rotation` على حقل `Arrow_Angle` و `Style = Geographic` — النسخة `_N` صفرها شمال.

## التركيب في ArcMap
1. `Customize > Style Manager > Styles > Add Style to List` واختار `05_Wind_Arrows.style`.
2. هتلاقي كاتيجوري `Wind Arrows - North Oriented`.
3. على طبقة `Wind_Vectors_Spring` : `Symbology > Features > Single Symbol` واختار أي سهم من الستايل.
4. `Advanced > Rotation` : الحقل `Arrow_Angle` و `Rotation Style = Geographic`.
5. `Advanced > Size` : الحقل `Wind_Speed` بمقاس 10-22.

## ملاحظة مهمة
- `Wind_Dir` = جاي منين (FROM) — للأرشيف.
- `Arrow_Angle = (Wind_Dir+180)%360` = رايح فين (TO) — للرسم. استخدم `Arrow_Angle` دايماً في الـ Rotation.
- كل الرموز هنا صفرها شمال، فأي انحراف 90° بعد كده معناه `Rotation Style` غلط (Arithmetic بدل Geographic).

## إعادة البناء
شغل : `C:\Python27\ArcGIS10.8\python.exe Build_Wind_Arrows_Style.py`
الناتج بيتوزع تلقائياً على : `style/05_Wind/` + `STYLE/` + `ArcMap_Style_Files/` + `All_ArcMap_Styles_Consolidated/`

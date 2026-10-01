# تقرير فحص شامل — تجمّد أداة NASA POWER Climate Atlas Generator في وضع الأوفلاين

> **تاريخ الفحص:** فحص ثابت (static) + إعادة إنتاج آلية (mechanism reproduction)
> **الملفات المفحوصة:** `POWER_Climate_Atlas_Generator_10_8.pyt` (6,522 سطر) + `raster_atlas_generator.py` (3,077 سطر) + `tests/` + سجل Git
> **بيئة التشغيل المؤكَّدة:** ArcGIS Pro (من `POWER_Climate_Atlas_Generator_10_8.pyt.xml` → `arcToolboxHelpPath = c:\program files\arcgis\pro\...`)
> **ملف إعادة الإنتاج:** [`audit_offline_freeze_proof.py`](audit_offline_freeze_proof.py)

---

## أولًا: الملخص التنفيذي — الخلل الجذري

**التجمّد لا يحدث في مرحلة الراستر إطلاقًا. يحدث قبلها، في دالة دمج طبقات الأوفلاين `_merge_offline_layers`.**

الأداة في وضع الأوفلاين **تكتب داخل طبقات المستخدم المدخَلة نفسها** — تعيد كتابة كل صف وتُسقط أعمدة منها — لأن مسار الخرج وحساباته يتصادفان مع مسار الدخل، ولأن «المسار الآمن» الذي كان يجب أن يمنع ذلك يفشل في التعرّف على 6 عناصر من 17.

وبما أن هذه الطبقات مفتوحة داخل خريطة ArcGIS Pro (وهو ما وصفته بأنه «لما بنضيف الطبقات»)، فإن ArcGIS يتحكّم في أقفال المخطط (schema locks) على طبقة يملكها المستخدم ويُعيد تحميلها في الواجهة، فيتوقف التقدّم بلا أي رسالة ولا شريط تقدّم — أي «تجمّد». وبما أن هذا يحدث **قبل** أي استيفاء (interpolation) أو قص (clip) أو حفظ، فإن المرحلة التي طلبتها — قص الراستر على طبقة الماسك وحفظه في الفولدر المخصص — **لا تصل إليها الأداة أبدًا**.

وهذا يفسّر تمامًا لماذا لم تُصلح آخر أربع محاولات إصلاح (commits) المشكلة: كلها كانت تُرقّع **مرحلة الراستر**، والخلل في المرحلة السابقة لها.

| # | الخلل | الملف / الأسطر | الحالة |
|:-:|---|---|:-:|
| **1** | **كتابة داخل طبقات المستخدم المدخَلة** (إعادة كتابة صفوف + حذف أعمدة + AddField) | `.pyt` 5522‑5593 | 🔴 مُثبَت بإعادة إنتاج آلية |
| **2** | فشل التعرّف على 6 من 17 عنصرًا بسبب `resolve_module_canonical` | `.pyt` 244‑262 + 5313‑5337 | 🔴 مُثبَت بالتنفيذ |
| **3** | مسار GDB الخرج = مسار GDB الدخل (نفس الاسم ونفس الـ workspace) | `.pyt` 3958 مقابل 3985، 4057 | 🔴 مُثبَت |
| **4** | لا شريط تقدّم ولا رسائل داخل حلقة الدمج الثقيلة | `.pyt` 5297‑5604 | 🔴 مُثبَت |
| **5** | أي فشل يُبتلع بصمت فيبدو «تجمّدًا» لا خطأ | `.pyt` 5929‑5930، 5587‑5590 | 🔴 مُثبَت |
| **6** | مخرجات الراستر مسارات ثابتة = نفس المسارات التي تضيفها الأداة للخريطة | `.pyt` 5154‑5164 + 4765‑4786 | 🟠 عالي |
| **7** | «حارس» حجم الخلايا يكتفي بالتحذير ولا يمنع التنفيذ | `.pyt` 4119‑4135 | 🟠 عالي |
| **8** | تسريب بيئة arcpy ولا يوجد `ResetEnvironments` في أي من الملفين | `.pyt` 4091‑4150، 6496‑6510 | 🟠 عالي |
| **9** | محرّك الراستر الثاني لم يُصلَّح منه أي شيء، وبه خطأ نظام إحداثيات | `raster_atlas_generator.py` 1626‑1630، 2540، 2672‑2674 | 🟠 عالي |
| **10** | اختبار «القص الصارم» يفشل الآن (المصفوفة غير خضراء) | `tests/test_modifications.py:220` | 🟡 متوسط |

---

## ثانيًا: البنية المكتشفة — أداتان كاملتان في صندوق واحد

هذه نقطة مهمة جدًا لم تكن موثّقة، ويجب معرفتها قبل أي إصلاح:

```
POWER_Climate_Atlas_Generator_10_8.pyt   ← صندوق الأدوات (alias: powerAtlas)
   └─ Toolbox.tools = [ PowerClimateAtlasGenerator ,  RasterDataClimateAtlasGenerator ]
                       (معرَّفة داخل .pyt)          (مستوردة من raster_atlas_generator.py)
```

- `.pyt` الأسطر **2440‑2454**: صندوق واحد يعرض **أداتين منفصلتين**:
  1. `PowerClimateAtlasGenerator` — «POWER Point Climate Atlas Generator» (`.pyt` 2457 وما بعدها)
  2. `RasterDataClimateAtlasGenerator` — «POWER Raster Climate Atlas Generator» (`raster_atlas_generator.py` 929)
- `raster_atlas_generator.py` **له أيضًا** `Toolbox` خاص به (السطر 3070، alias `powerRasterAtlas`).

**النتيجة العملية:** الأداتان تنفّذان نفس خط الأنابيب تقريبًا لكنهما شفرتان منسوختان ومنفصلتان. كل إصلاحات التجمّد الأربعة الأخيرة ذُهبت إلى `.pyt` فقط؛ و`raster_atlas_generator.py` ما زال يحتفظ بكل الأنماط التي حُذفت من الملف الآخر باعتبارها سبب التجمّد:

| النمط | `.pyt` | `raster_atlas_generator.py` |
|---|---|---|
| `arcpy.env.mask = <ماسك>` | أُزيل (سطر 4086: تعليق «DO NOT set») | **موجود** — السطر 2540 |
| `rasterStatistics = "STATISTICS 1 1"` | صار `"NONE"` (4146) | **موجود** — 1610 و2647 |
| تحويل الماسك إلى راستر مسبقًا | موجود (4093‑4111) | **غير موجود** |
| `parallelProcessingFactor` | مضبوط (4138، 5813) | **غير موجود** |
| `outputCoordinateSystem` | مضبوط (4091) | **غير موجود إطلاقًا** |

لذلك: **حدّد أي أداة تستخدم.** إذا كنت تشغّل «POWER **Raster** Climate Atlas Generator» فأنت تعمل على نسخة لم تُصلَّح، والخلل رقم 9 أدناه هو الأرجح. أما «POWER **Point** Climate Atlas Generator» فهو موضوع الخللين 1 و2.

---

## ثالثًا: الخلل الجذري — الدليل الكامل خطوة بخطوة

### الخطوة 1 — وضع الداونلود ينتج قاعدة بيانات باسم مشتق من السنوات

`.pyt` السطر 4057: `gdb_name = "Climate_Database_%s.gdb" % time_tag`
`.pyt` السطر 3985 (وضع الداونلود، Year Range): `time_tag = "From_%d_To_%d" % (start_year, end_year)`

⇒ لسنوات 2015–2024: `Climate_Database_From_2015_To_2024.gdb` داخل `Output_Workspace`.

### الخطوة 2 — وضع الأوفلاين **يُعيد حساب نفس الاسم بالضبط**

`.pyt` الأسطر 3928‑3968: في الأوفلاين تُقرأ `Data_Start` و`Data_End` من طبقات المستخدم المدخَلة، ثم:

- السطر **3958**: `time_tag = "From_%d_To_%d" % (min(y0,y1), max(y0,y1))`

وهذا **نفس تنسيق وضع الداونلود حرفيًا**. وبما أن `Output_Workspace` عادةً يبقى كما هو، فإن:

```
gdb_path للأوفلاين  ==  gdb_path للداونلود  ==  المجلد الذي تعيش فيه طبقات المستخدم المدخَلة
```

### الخطوة 3 — الأداة تنوي الكتابة داخل تلك القاعدة

`.pyt` السطر **5523‑5524**:

```python
short = MODULE_SHORT.get(m, m)
fc = os.path.join(gdb_path, short)      # ← قد يكون هذا بالضبط مسار طبقة المستخدم!
```

`.pyt` السطر **3738**: `arcpy.env.overwriteOutput = True` ← لا يوجد أي سؤال تأكيد.

### الخطوة 4 — «المسار الآمن» موجود، لكنه يفشل في 6 عناصر من 17

كان يجب أن يمنع هذا كله منطق `direct_layer_map` في الأسطر **5313‑5337**: إذا تمكّنت الأداة من التعرّف على اسم الطبقة المدخَلة كعنصر مناخي، فستستخدمها كما هي (`element_fcs[m] = direct_layer_map[m]`, السطر 5328) وتعود مبكرًا بلا أي إعادة بناء (الأسطر 5334‑5337).

لكن التعرّف يعتمد على `resolve_module_canonical` (السطر **244**)، وهي تقارن الاسم **مقارنة حرفية** مع الأسماء القانونية التي تحتوي **مسافة** (`"Relative Humidity"`)، ولا تعرف الصيغة التي تستخدم فيها الأداة نفسها **شرطة سفلية** (`"Relative_Humidity"` = قيمة `MODULE_SHORT`، وهي نفسها أسماء الـ Feature Classes والأسماء في `Export_SHP`).

**النتيجة المقيسة فعليًا** (بتشغيل الدالة الحقيقية على الثوابت الحقيقية):

```
Sea_Level_Pressure     -> None   (لم يُتعرَّف عليه)
Surface_Pressure       -> None
Relative_Humidity      -> None
Solar_Radiation        -> None
UV_Index               -> None
Cloud_Cover            -> None
```

⇒ هذه الستة تخرج من المسار الآمن، وتدخل في `remaining_modules` (السطر 5334)، فتُنفَّذ عليها إعادة البناء الهدّامة.

### الخطوة 5 — إعادة البناء الهدّامة على بيانات المستخدم

`.pyt` الأسطر **5522‑5593**، لكل عنصر من الستة:

| السطر | العملية على طبقة المستخدم |
|---|---|
| 5526 | `CopyFeatures` (يُتخطّى لأن الملف موجود أصلًا) |
| 5531 / 5533 | `arcpy.management.AddField(...)` — يحتاج **قفل مخطط حصري** |
| 5538 | `AddField` لكل حقل مؤشر |
| **5540** | `with arcpy.da.UpdateCursor(fc, ...)` — **فتح طبقة المستخدم للكتابة** |
| **5581** | `ucur.updateRow(row)` — **إعادة كتابة كل صف** |
| 5584‑5588 | `keep_fields` ثم `arcpy.management.DeleteField(fc, to_delete)` — **إسقاط كل عمود خارج قائمة العنصر** |

و`DeleteField` مُغلَّف بـ `try/except/pass` (5587‑5590) فيختفي فشله بصمت، بينما `AddField` و`UpdateCursor` (5531/5540) **غير محميين** — وهنا ينتظر ArcGIS قفل المخطط.

### الخطوة 6 — لا رسائل، لا شريط تقدّم

`_merge_offline_layers` (5297‑5604) لا يستدعي `arcpy.SetProgressor` إطلاقًا، ولا يوجد أي `msg()` بين السطر 5309 والسطر 5381، ولا بين 5381 و5593. كل الـ `SetProgressor` في الملف كله هي 4332/4367/4866/4924/**5746** — أي أنها كلها في مرحلة الراستر، لا في الدمج.

⇒ أثناء انتظار أقفال ArcGIS تظهر الواجهة **متجمّدة تمامًا** بلا أي مؤشر. هذا هو «الفريز» الذي تراه.

### الخطوة 7 — لذلك لا يحدث القص ولا الحفظ

بعد الدمج، تُنادى `_interpolate_all` (السطر 4228). لكن حقول الستة عناصر إمّا اختفت أو فُرِّغت، فتخرج الأداة من الحلقة بأحد هذين التحذيرين وتتخطّى الراستر:

- السطر **5785**: `warn("Skipping raster %s: field not found in point layer." % field)`
- السطر **5798**: `warn("Skipping raster %s: only %d valid points." % field, n_valid)`

⇒ لا `ExtractByMask` (5845) ولا `CopyRaster` (5881) — **لا قص ولا حفظ في الفولدر المخصص**. وهو بالضبط ما وصفته.

---

## رابعًا: إعادة الإنتاج الآلية (الدليل التنفيذي)

شغّلت الدالة **الحقيقية** `PowerClimateAtlasGenerator._merge_offline_layers` على 17 طبقة مُهيّأة **بنفس شكل مخرجات وضع الداونلود تمامًا** (نفس GDB، نفس أسماء `MODULE_SHORT`). النتيجة من [`audit_offline_freeze_proof.py`](audit_offline_freeze_proof.py):

```
DOWNLOAD-MODE OUTPUT GDB  : Climate_Database_From_2015_To_2024.gdb
OFFLINE-MODE OUTPUT GDB   : Climate_Database_From_2015_To_2024.gdb
SAME PATH?                : True
INPUT LAYERS SUPPLIED     : 17

WRITES PERFORMED AGAINST THE USER'S OWN INPUT LAYERS
  WRITTEN: Cloud_Cover            <- DeleteField x1, updateRow x5
  WRITTEN: Relative_Humidity      <- DeleteField x1, updateRow x5
  WRITTEN: Sea_Level_Pressure     <- DeleteField x1, updateRow x5
  WRITTEN: Solar_Radiation        <- DeleteField x1, updateRow x5
  WRITTEN: Surface_Pressure       <- DeleteField x1, updateRow x5
  WRITTEN: UV_Index               <- DeleteField x1, updateRow x5

SCHEMA DAMAGE: fields removed from the user's input feature classes
  Cloud_Cover            lost 3 field(s): Feat_ID, Feat_Name, OBJECTID_1
  Relative_Humidity      lost 3 field(s): Feat_ID, Feat_Name, OBJECTID_1
  ... (الستة كلها)

MODULES THAT MISSED THE SAFE 'direct_layer_map' FAST PATH
  total: 6 of 17 modules
```

**الخلاصة:** الأداة تفتح طبقات المستخدم للكتابة، تعيد كتابة صفوفها، وتُسقط أعمدة منها. هذا يثبت الخللين 1 و2 بمخرجات قابلة للتكرار، لا بترجيح.

---

## خامسًا: لماذا لم تُصلح المحاولات الأربع السابقة المشكلة؟

سجل Git يسجّل أربع محاولات متتالية في نفس اليوم لمعالجة «التجمّد»، وكلها استهدفت **مرحلة الراستر**:

| الـ commit | ما جُرِّب | لماذا لم يُجدِ |
|---|---|---|
| `69215a6` | إزالة I/O وسيط في خط أنابيب الراستر | الخلل قبل الراستر |
| `2212818` | رسائل تقدّم وتوقيت لكل عمود راستر | الرسائل في 5746 لا في 5297 |
| `db5d3ea` | «إزالة الجمود بسبب أقفال الراستر»: حذف `arcpy.env.mask`، إزالة `CalculateStatistics`، تحرير الذاكرة | الأقفال الحقيقية على **الـ Feature Classes** في 5531/5540، لا على الراستر |
| `07515f2` | `rasterStatistics = "NONE"` + تحويل الماسك إلى راستر مسبقًا + `raster_mask` | نفس السبب |

ونتج عن المحاولة الأخيرة **انحدار وظيفي**: `tests/test_modifications.py::test_07_strict_mask_and_clip_in_code` يفشل الآن:

```
FAIL: test_07_strict_mask_and_clip_in_code
AssertionError: 'arcpy.env.mask = mask' not found in ...POWER_Climate_Atlas_Generator_10_8.pyt
```

أي أن ضمان «القص الصارم» الذي كان الاختبار يحميه أُزيل من `.pyt`، وما زال قائمًا في `raster_atlas_generator.py` — وهو تعارض بين المحرّكين.

---

## سادسًا: بقية المخاطر المؤكَّدة (مرتّبة)

### 🟠 6 — مخرجات الراستر مسارات ثابتة تُعاد الكتابة عليها
`_raster_paths` (`.pyt` **5154‑5164**) يعيد `out_ws/<MODULE_FOLDER>/<field>.tif` — **نفس المسار في كل تشغيل**. والأداة نفسها تضيف هذه المسارات إلى الخريطة في `_add_to_map` (**4765‑4786**، والسطر 4743 `m.addDataFromPath(lp)`)، والمُعامِل `Add_To_Map` **قيمته الافتراضية True** (**3199**). إعادة التشغيل على نفس `Output_Workspace` تعني `CopyRaster` فوق TIFF مفتوح ومُعروض. لاحظ أيضًا أن `_raster_paths` **لا ينشئ المجلد** — ينشئه `_build_layout` (4803‑4824) فقط، وهو تكرار هشّ.

### 🟠 7 — «حارس» حجم الخلايا يكتفي بالتحذير
`.pyt` **4119‑4135**، تعليق الكود يقول «refuse rasters that would exhaust 32-bit ArcMap» لكن الشفرة **تحذّر فقط**:
```python
if _cells > 50000000:
    warn("Cell size %.4g %s produces approximately %.1f million cells. "
         "Processing may take longer depending on hardware." % (...))
```
ثم تستمر. و`env.cellSize = eff_base` (**4118**) + `env.extent = mask` (**5810**) يعني أن نداء `Idw`/`Kriging` (5838) يجب أن يولّد **كل** الخلايا قبل أن يصل أي شيء إلى القص في 5845. وزر الإلغاء لا يعمل إلا **بين** نداءات geoprocessing، لا داخلها ⇒ تجمّد غير قابل للإلغاء. كما أن `Focal_Neighborhood` (**3835**) لا سقف له.

### 🟠 8 — تسريب بيئة arcpy
11 إسنادًا لـ `arcpy.env.*` (4091، 4104، 4105، 4118، 4138، 4143‑4146، 4150، 5720، 5810، 5813)، ولا يوجد `arcpy.ResetEnvironments()` في أي من الملفين. `_cleanup` (**6496‑6510**) يُنظّف `mask` و`extent` فقط. الباقي — `outputCoordinateSystem`، `cellSize`، `parallelProcessingFactor = "100%"`، `compression`، `tileSize`، `pyramid`، `rasterStatistics`، `scratchWorkspace` — **يتسرّب بين الحقول والعناصر وإلى جلسة ArcGIS Pro نفسها**، فيؤثر على أي معالجة لاحقة تقوم بها. والأخطر: `scratchWorkspace` يُشير إلى `_scratch` التي **تُحذف** في 6516، فتظل البيئة مشيرة إلى مجلد غير موجود في التشغيل التالي.

### 🟠 9 — محرّك الراستر الثاني: خطأ نظام إحداثيات يضاعف العمل ~110,000 مرة
في `raster_atlas_generator.py`:

- **1626‑1630**: `target_sr` يُشتق من الماسك، و`eff_cell_size = cell_size / 111320.0` إذا كان الهدف جغرافيًا.
- **لا يوجد `arcpy.env.outputCoordinateSystem` في الملف كله** (تحقّقت بالبحث: صفر نتائج)، بينما `.pyt` يضبطه في السطر 4091.
- **2187‑2195**: في الأوفلاين، «التعيين المباشر» يمرّر طبقات المستخدم كما هي بلا إسقاط.

⇒ إذا كان الماسك جغرافيًا (WGS84) ونقاط المستخدم في نظام إسقاطي (أمتار)، فسيُمرَّر حجم خلية بوحدة الدرجات (0.0045) إلى `Idw` التي تعمل في وحدة **الأمتار** ⇒ عدد الخلايا يتضاعف بنحو `111320²` ≈ **1.2×10¹⁰** ⇒ عمل غير محدود فعليًا. وباقي الأنماط غير المُصلَّحة في نفس الملف: `arcpy.env.mask = clip_layer` (**2540**، لا يُنظَّف أبدًا هناك)، `rasterStatistics = "STATISTICS 1 1"` (**1610**، **2647**)، وابتلاع كل الأخطاء في `_interpolate_and_clip` (**2672‑2674**: `warn(...); return False`) بحيث يبدو الفشل المتكرّر تمامًا كالتجمّد.

### 🟡 10 — مخالفات أخرى مؤكَّدة
- `.pyt` 3771: `mask = (pdict.get("Study_Area_Mask") or parameters[4]).valueAsText` — احتياطي **موضعي**: `parameters[4]` هو `p_precalc` (طبقات الأوفلاين) لا الماسك. يحمي منه وجود الاسم، لكنه فخّ صامت. ومثله `parameters[5]` (السطر 3816 لـ `Output_Workspace`، وهو فعليًا `p1`) و`parameters[17]` (3785 لـ `Temporal_Resolution`، وهو فعليًا `p_end_date`) و`parameters[20]` (3786 لـ `Climate_Modules`، وهو فعليًا `Point_Tolerance`).
- `.pyt` 3799: `can_mod = resolve_module_canonical(item) or item` — أي نص غير معروف يمرّ كما هو، ثم `MODULE_FOLDER[m]` في `_build_layout` (4818) يرفع `KeyError` بلا حماية. و`MODULE_SHORT`/`MODULE_FIELDS` يحتويان «Drought & Aridity» و«Climate_Models» غير الموجودة في `MODULE_FOLDER`.
- `.pyt` 6497‑6506: الحذف **بالاسم المجرّد** لا بالمسار (`"pwr_atlas_interp"`، السطر 5800)، و`Delete` بالاسم يُحلّ في ArcMap مقابل جدول المحتويات — فقد يحذف مصدر طبقة المستخدم.
- `.pyt` 2504: `canRunInBackground = True` + `arcpy.mp.ArcGISProject("CURRENT")` + `addDataFromPath` في `_add_to_map` (4720‑4747) — مزيج غير مدعوم في ArcGIS Pro (الوصول إلى CURRENT من خيط خلفي)، وهو سبب محتمل لتجمّد **بعد** انتهاء العمل. لم أستطع إثباته ثابتًا، لكن الأثر العملي: عند تفادي التشغيل التالي تُقفل ملفات الراستر التي أضافها، فتصبح جلسة `CopyRaster` التالية ممتدة الانتظار.
- `.pytc` (10:27:08) أقدم من `.pyt` (11:09:20) — كاش PyToolbox قديم/غير متزامن؛ احذفه قبل أي اختبار جديد.

---

## سابعًا: الإصلاحات المطلوبة (بأرقام الأسطر)

### إصلاح حرج — يمنع الكتابة في بيانات المستخدم

**الإصلاح الجوهري:** اجعل مخرجات الأوفلاين **مجلدًا مستقلًا** ولا تكتب أبدًا في مسار مدخل.

1. **`.pyt` 4057:** في وضع الأوفلاين، استخدم اسم GDB مختلفًا ومضمونًا، مثل
   `gdb_name = "Climate_Database_%s_Offline.gdb" % time_tag`
2. **`.pyt` 5522‑5526:** أضف حماية صريحة قبل أي كتابة:
   ```python
   fc = os.path.join(gdb_path, short)
   for _inp in layer_paths:
       if os.path.normcase(os.path.abspath(fc)) == os.path.normcase(os.path.abspath(_inp)):
           fc = os.path.join(gdb_path, short + "_Atlas")   # لا تكتب في الدخل أبدًا
           break
   ```
3. **`.pyt` 244‑262:** اجعل `resolve_module_canonical` تعرف صيغة الشرطة السفلية، بمقارنة مُطبَّعة:
   ```python
   def _norm(s):
       return str(s).strip().strip("'\"").lower().replace("_", " ").replace("-", " ")
   # أول فحص في الدالة:
   _n = _norm(name_str)
   for cm in ALL_CANONICAL_MODULES:
       if _n == _norm(cm):
           return cm
   ```
   هذا وحده يعيد الستة إلى المسار الآمن ويمنع إعادة البناء الهدّامة من الأساس.
4. **`.pyt` 4119‑4135:** حوّل التحذير إلى **منع فعلي** (أو على الأقل اسأل/أوقف) عندما يتجاوز عدد الخلايا حدًّا آمنًا:
   ```python
   if _cells > 50000000:
       raise RuntimeError("Cell size too fine: ~%.1f million cells (limit 50M). "
                          "Increase Base Cell Size." % (_cells / 1000000.0))
   ```
5. **`.pyt` 3738 / 3985:** **لا** تضع `overwriteOutput = True` كإعداد عام دائم؛ اضبطه موضعيًا حول الكتابات المقصودة فقط.

### إصلاح حرج — الشفافية (حتى لا يبدو التعليق تجمّدًا)

6. **`.pyt` 5297‑5604:** أضف `arcpy.SetProgressor` ورسائل `msg()` داخل حلقتَي 5384‑5419 و5522‑5593، مثل:
   `msg("  Merging layer %d/%d: %s ..." % (i, n, os.path.basename(lyr)))`
7. **`.pyt` 5929‑5930 و5587‑5590:** لا تبتلع الفشل بصمت — **راكم الأخطاء** وأبلغ عنها في النهاية، حتى لا يُقرأ «فشل متكرّر» كـ«تجمّد».

### إصلاح عالي

8. **`.pyt` 6496‑6510:** أضف `arcpy.ResetEnvironments()` في `_cleanup`، أو أعد ضبط المفاتيح صراحةً (`outputCoordinateSystem`, `cellSize`, `parallelProcessingFactor`, `compression`, `tileSize`, `pyramid`, `rasterStatistics`, `scratchWorkspace`).
9. **`.pyt` 5154‑5164:** اجعل `_raster_paths` ينشئ المجلد بنفسه (`makedirs_ok(rdir)`)، واجعل مسار الخرج يحمل بصمة تشغيل أو تحقّق أن الملف غير مفتوح قبل الكتابة.
10. **`.pyt` 4720‑4751:** إما `canRunInBackground = False` (2504) أو أزل `Add_To_Map` الافتراضي/استخدم مُعامِلات خرج مشتقة (Derived output) بدل `addDataFromPath` من داخل الأداة.
11. **`raster_atlas_generator.py`:**
    - **قبل 2586** أو عند 1629: اضبط `arcpy.env.outputCoordinateSystem = target_sr` (كما في `.pyt` 4091) — هذا يصلح خطأ نظام الإحداثيات.
    - **2540:** أزل `arcpy.env.mask = clip_layer` واكتفِ بـ `arcpy.env.extent` + `ExtractByMask` (كما فُعل في `.pyt`).
    - **2672‑2674:** لا تُرجِع `False` بصمت؛ سجّل الخطأ في قائمة أخطاء.
    - طبّق نفس حماية المسار (بند 2) — الملف فيه نفس نمط الكتابة في `MODULE_FOLDER.get(mod, ...)` عند 2480‑2513.
12. **`tests/test_modifications.py:220`:** حدّث `test_07` ليطابق السلوك الجديد (`ClearEnvironment("mask")` + `ExtractByMask`) بدل `arcpy.env.mask = mask`، حتى تعود المصفوفة خضراء وتعود الحماية قائمة.

---

## ثامنًا: كيف تتأكّد بنفسك في دقائق

1. **اختبار حاسم واحد:** شغّل نفس مهمة الأوفلاين بعد **إزالة طبقات الإدخال من الخريطة وإغلاق جداولها**. إن انتهت، فالسبب هو تنازع أقفال المخطط على بيانات المستخدم (الخلل 1) — وهو الأرجح. وإن بقيت متجمّدة، فالمشكلة في غياب التقدّم/الذاكرة أو في الخلل 9.
2. **افحص آثار الدمار:** افتح `Climate_Database_From_YYYY_To_YYYY.gdb` بعد تشغيل أوفلاين، وقارن أعمدة `Relative_Humidity` و`Solar_Radiation` و`UV_Index` و`Cloud_Cover` و`Surface_Pressure` و`Sea_Level_Pressure` بما كان. أي عمود مفقود = تأكيد قاطع.
3. **حلّل الكاش:** احذف `POWER_Climate_Atlas_Generator_10_8.pytc` و`.pyt.xml` قبل إعادة فتح صندوق الأدوات في ArcGIS Pro.
4. **أعد تشغيل الإثبات:** `python audit_offline_freeze_proof.py` — يجب أن يطبع قائمة الكتابات في طبقات الإدخال.
5. **قارن المحرّكين:** شغّل الخطوات نفسها على «POWER **Raster** Climate Atlas Generator» — إن ظهر الخلل 9 فسترى تجمّدًا أطول وأعمق.

---

## تاسعًا: ملاحظات منهجية وحدود الفحص

- **مُثبَت بالتنفيذ:** الخللان 1 و2 (إعادة إنتاج آلية على الشفرة الحقيقية)، وفشل اختبار `test_07`، وتناقض المحرّكين، وغياب `outputCoordinateSystem`، وتسريب البيئة.
- **مُثبَت بالقراءة المباشرة للشفرة:** الأسطر المذكورة كلها تحقّقت منها قراءةً.
- **مرجَّح لا مُثبَت:** أن التجمّد **بعينه** الذي تراه هو انتظار قفل المخطط (يعتمد على حالة ArcGIS وللأقفال سلوك بيئي لا يمكن حسمه من الشفرة وحدها)، وأن `canRunInBackground = True` مع `arcpy.mp.CURRENT` هو سبب تجمّد ثانٍ في نهاية التشغيل. استخدم الاختبار الحاسم في البند 1 للفصل بينهما.
- **مستبعَد صراحةً:** لا توجد أي حلقة `while` في الملفين، ولا استدعاء ذاتي، ولا مؤشرات متداخلة في `_merge_offline_layers`، ولا نافذة إدخال تفاعلية في مسار الأوفلاين. فالخلل ليس حلقة لا نهائية بالمعنى الحرفي، بل **انتظار قفل + غياب أي تغذية راجعة**.
- لم أشغّل ArcGIS (غير متاح في هذه البيئة)، ولا توجد `arcpy` حقيقية؛ لذلك كل سلوك يشترط محرّك Esri قُدِّم كـ«مرجَّح» مع تمييز واضح.

---

## عاشرًا: الملفات المرجعية

| الملف | الدور |
|---|---|
| [`POWER_Climate_Atlas_Generator_10_8.pyt`](POWER_Climate_Atlas_Generator_10_8.pyt) | الأداة الرئيسية — موضع الخللين 1 و2 |
| [`raster_atlas_generator.py`](raster_atlas_generator.py) | المحرّك الثاني — موضع الخلل 9، ولم تُطبَّق عليه إصلاحات التجمّد |
| [`audit_offline_freeze_proof.py`](audit_offline_freeze_proof.py) | إعادة إنتاج آلية قابلة للتشغيل |
| [`tests/test_modifications.py`](tests/test_modifications.py) | `test_07` — يفشل الآن (مؤشر انحدار) |
| [`Audit_Report.md`](Audit_Report.md) | تدقيق سابق (30 سبتمبر 2026) — لم يتناول تجمّد الأوفلاين |

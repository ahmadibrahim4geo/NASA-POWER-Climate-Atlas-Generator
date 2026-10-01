# مراجعة ما بعد الإصلاح — NASA POWER Climate Atlas Generator

> **مرجع:** مراجعة لاحقة لتقرير [`Tool_Freeze_Audit_AR.md`](Tool_Freeze_Audit_AR.md)
> **الالتزام المراجَع:** `e672977` — *"feat: unify 18 climate modules with 1:1 mapping, add seasonal Evapotranspiration (FAO-56)"*
> **حالة الشجرة:** نظيفة (`git status` فارغة)
> **طريقة المراجعة:** تشغيل فعلي للشفرات المُصلَّحة على بيئة `arcpy` وهمية، لا قراءة فرق (diff) فقط

---

## الحكم النهائي

**الخلل الجذري الذي كان يسبب التجمّد قد أُصلح فعليًا، ومُثبَت بالتنفيذ، ومحمي بطبقة دفاع ثانية.** لم يعد البرنامج الذي كان يُعيد كتابة بيانات المستخدم قابلًا لإعادة الإنتاج.

| البند | الحالة |
|---|:-:|
| الخلل الجذري: فشل `resolve_module_canonical` في 6 من 17 عنصرًا | ✅ مُصلَح ومُثبَت |
| الكتابة داخل طبقات المستخدم (إعادة كتابة صفوف + إسقاط أعمدة) | ✅ مُصلَح ومُثبَت |
| حماية إضافية عند فشل المسار السريع | ✅ مُصلَح ومُثبَت باختبار عدائي جديد |
| `parallelProcessingFactor = "100%"` | ✅ صار `"0"` في 3 مواضع |
| تغذية راجعة في مرحلة الراستر | ✅ أُضيف `SetProgressorLabel` |
| المصفوفة الاختبارية | ✅ خضراء (كان فيها فشل واحد) |
| كاش `.pytc` القديم | ✅ محذوف |
| **حارس حجم الخلايا (تحذير فقط)** | ❌ **لم يُصلَح** |
| **`outputCoordinateSystem` مفقود في المحرّك الثاني** | ❌ **لم يُصلَح** |
| **`arcpy.env.mask = clip_layer` في المحرّك الثاني** | ❌ **لم يُصلَح** |
| **`ResetEnvironments` في الملفين** | ❌ **لم يُضَف** |
| **إنشاء مجلد مخرجات الراستر داخل `_raster_paths`** | ❌ **لم يُصلَح** |
| **فصل قاعدة بيانات الأوفلاين عن قاعدة بيانات الداونلود** | ⚠️ **حُمي لكن لم يُفصَل** |
| **تغذية راجعة داخل `_merge_offline_layers`** | ❌ **لم تُضَف** |

---

## أولًا: ما أُصلح — والأدلة التنفيذية

### 1) الخلل الجذري ✅

`resolve_module_canonical` (السطر **250**) صارت تُطبّع الفواصل والشرطات وحالة الأحرف، وأُضيف جدول أسماء قديمة صريح `_DIRECT_ALIASES` (السطر **259**).

**قياس فعلي على الشفرات الجديدة:**

```
Relative_Humidity                              -> 'Relative Humidity'      ✅ (كان None)
Sea_Level_Pressure / Surface_Pressure          -> ✅ تُحلّ الآن
Solar_Radiation / UV_Index / Cloud_Cover       -> ✅ تُحلّ الآن
Dew_Point                                      -> 'Dew Point'              ✅
Trends_And_Anomalies                           -> 'Trends & Anomalies'     ✅
ET / et                                        -> 'Evapotranspiration'     ✅
Hargreaves PET / Hargreaves_PET                -> 'Evapotranspiration'     ✅
FAO-56 Hargreaves PET [Requires: Temperature]  -> 'Evapotranspiration'     ✅
MyCustomLayer                                  -> None                     (سلوك صحيح)
```

**ونتج عن ذلك أن إعادة الإنتاج الأصلية لم تعد تعمل** — وهو المطلوب:

```
BEFORE (الالتزام 07515f2):            AFTER (e672977):
  WRITTEN: Cloud_Cover  <- DeleteField x1, updateRow x5      WRITES INTO INPUTS : (none)
  WRITTEN: Relative_Humidity <- ...                          SCHEMA LOSS        : (none)
  ... 6 من 17                                                missed fast path   : 0 of 19
  lost 3 field(s): Feat_ID, Feat_Name, OBJECTID_1
```

### 2) حماية إضافية (دفاع في العمق) ✅ — وهذا اختبار **جديد** كتبته للمراجعة

بما أن إعادة الإنتاج الأصلية لم تعد تُمارس المسار الهدّام، لم يكن واضحًا هل الحماية الجديدة تعمل فعلًا أم أن المسار السريع أصبح يبتلع كل الحالات ويخفي المشكلة. لذلك بنيت اختبارًا عدائيًا: طبقات إدخال تحمل **نفس أسماء الأداة تمامًا** (`Temperature`, `Relative_Humidity`, `Solar_Radiation`) لكنها **بلا حقول مؤشرات**، فالمسار السريع **لا يستطيع** ضمّها.

**النتيجة:**

```
input FCs: Relative_Humidity, Solar_Radiation, Temperature   (بلا حقول مؤشرات)

targets chosen per module (must NOT be an input path):
   Temperature        -> Temperature_Atlas        safe (separate FC)
   Relative Humidity  -> Relative_Humidity_Atlas  safe (separate FC)
   Solar Radiation    -> Solar_Radiation_Atlas    safe (separate FC)

WRITES INTO INPUTS : NONE  -> GUARD HOLDS
input schema loss  : NONE
```

⇒ الحماية `os.path.normcase(os.path.abspath(fc)) == os.path.normcase(os.path.abspath(_inp))` تعمل حتى في أسوأ حالة، وتحوّل الهدف إلى `<short>_Atlas`. هذا هو الإصلاح الأهم في هذه المراجعة.

### 3) `parallelProcessingFactor` ✅

`"100%"` → `"0"` في ثلاثة مواضع (منها داخل حلقة الحقول). هذا يزيل المزيج غير المدعوم (معالجة متوازية من أداة سكربت تحمل كائنات راستر حيّة ومدخلات `in_memory`) الذي رشّحه المدقّق الثاني كأقوى تفسير لتجمّد صلب غير قابل للإلغاء.

### 4) المصفوفة الاختبارية ✅ — عادت خضراء

```
test_power_atlas_108_offline        ==== SUMMARY: 104 passed, 0 failed ====
test_field_filters_108              ==== SUMMARY:  23 passed, 0 failed ====
test_provider_interp_108            ==== SUMMARY:  22 passed, 0 failed ====
test_modifications                  Ran 9 tests  OK      (كان يفشل في test_07)
test_arcgis_pro_compatibility       Ran 7 tests  OK
test_workflow_and_temporal_scope    Ran 6 tests  OK
test_migrate_legacy_database        Ran 5 tests  OK
test_drought_dependencies_108       Ran 4 tests  OK
test_modes_and_inputs_108           Ran 4 tests  OK (skipped=4 — تحتاج arcpy)
test_raster_offline_and_parity      SKIP (تحتاج arcpy)
```

`test_07_strict_mask_and_clip_in_code` حُدِّث ليؤكّد السلوك الجديد (`arcpy.env.extent = mask` + `ExtractByMask(surf, effective_mask)`) بدل `arcpy.env.mask = mask` — وهذا متسق مع قرار إزالة `env.mask` عن قصد.

> **ملاحظة على بيئة المراجعة (ليست خللًا في الشفرة):** `test_excel_export_108` يظهر فيه 3 أخطاء، لكنها كلها `PermissionError: [Errno 13]` على مسار مؤقت خاص ببيئة الفحص المحصورة — أي قيد في بيئتي لا في كودك. ومثلها `test_depth_purge_help_108` و`test_elements_108` و`test_query_seq` و`test_sig_108` و`test_tol_focal_108` تفشل بـ `FileNotFoundError` على مسار `C:\Users\ahmad\Desktop\...` مكتوب صراحةً داخل الاختبار وغير موجود هنا.

### 5) كاش `.pytc` ✅ محذوف (لم يعد موجودًا).

---

## ثانيًا: ما لم يُصلَح — مرتّبًا بالأولوية

### 🔴 A) حارس حجم الخلايا ما زال **تحذيرًا فقط** — أهم بند متبقٍّ

`.pyt` الأسطر **4224‑4238**:

```python
# --- guard: refuse rasters that would exhaust 32-bit ArcMap ---
...
_cells = (_w / eff_base) * (_h / eff_base)
if _cells > 50000000:
    warn("Cell size %.4g %s produces approximately %.1f million cells. "
         "Processing may take longer depending on hardware." % (...))
```

التعليق يقول «refuse» (يرفض) والكود **يحذّر ثم يستمر**. وبما أن `arcpy.env.cellSize = eff_base` و`arcpy.env.extent = mask` مضبوطان، فإن نداء `Idw`/`Kriging` (السطر 6000 تقريبًا) **يجب** أن يولّد كل الخلايا قبل أن يصل أي شيء إلى `ExtractByMask` ثم `CopyRaster`. وزر الإلغاء في ArcGIS لا يعمل إلا **بين** نداءات geoprocessing لا داخلها ⇒ يبقى مسار تجمّد غير قابل للإلغاء.

**الإصلاح المقترح:**

```python
if _cells > 50000000:
    raise RuntimeError(
        "حجم الخلية %.4g %s ينتج ~%.1f مليون خلية (الحد 50 مليونًا). "
        "ارفع قيمة Base Cell Size ثم أعد التشغيل."
        % (base_cell, ("درجات" if is_geo else "أمتار"), _cells / 1000000.0))
```

### 🔴 B) المحرّك الثاني (`raster_atlas_generator.py`) لم يُصلَّح من فئة التجمّد

صندوق الأدوات ما زال يعرض أداتين (`Toolbox.tools`)، فيمكن للمستخدم اختيار «POWER **Raster** Climate Atlas Generator» والحصول على نسخة بلا أي إصلاح من إصلاحات التجمّد:

1. **لا يوجد `arcpy.env.outputCoordinateSystem` في الملف كله (صفر نتيجة)** — بينما `eff_cell_size` تُحسب من نظام الإحداثيات **الهدف** (السطر 1629). فإذا كان الماسك جغرافيًا والنقاط إسقاطية (أمتار)، يُمرَّر حجم خلية بالدرجات (~0.0045) إلى `Idw` تعمل في **الأمتار** ⇒ عدد الخلايا يتضاعف بنحو `111320²` ≈ **1.2×10¹⁰**. هذا عمل غير محدود فعليًا وتجمّد صلب. الـ `.pyt` يتفادى هذا بضبط `outputCoordinateSystem`.
2. **`arcpy.env.mask = clip_layer` ما زال موجودًا (السطر 2689)** — وهو بالضبط النمط الذي أُزيل من الـ `.pyt` وصار موثّقًا هناك كمنهي عنه، ولم يُنظَّف أبدًا في هذا الملف حتى بعد انتهاء كل العناصر.
3. **كل الاستثناءات تُبتلع** في `_interpolate_and_clip` (`warn(...); return False`) ⇒ فشل متكرّر يبدو تمامًا كتجمّد، بلا أي أثر.

### 🟠 C) لا `arcpy.ResetEnvironments` في أي من الملفين

11 إسنادًا لـ `arcpy.env.*`، و`_cleanup` يُنظّف `mask` و`extent` فقط. الباقي يتسرّب إلى جلسة ArcGIS Pro: `outputCoordinateSystem`، `cellSize`، `compression`، `tileSize`، `pyramid`، `rasterStatistics`، و`scratchWorkspace` الذي يشير إلى `_scratch` **التي يحذفها `_cleanup`** — أي بيئة تشير إلى مجلد غير موجود في التشغيل التالي.

**الإصلاح:** أضف `arcpy.ResetEnvironments()` في نهاية `_cleanup`، أو أعد ضبط المفاتيح صراحةً.

### 🟠 D) `_raster_paths` لا ينشئ مجلد المخرجات

الأسطر **5254‑5264**: `folder = MODULE_FOLDER[module]` ثم يعيد المسار — **بلا `makedirs_ok`**. إنشاء المجلدات موكول كليًا إلى `_build_layout`. أي انحراف بين قائمة العناصر التي تُبنى لها المجلدات وقائمة العناصر التي تُستوفى ⇒ `CopyRaster` يفشل. سطر واحد يحسم الأمر:

```python
makedirs_ok(rdir)
return os.path.join(rdir, field + ".tif"), None
```

### 🟠 E) قاعدة بيانات الأوفلاين ما زالت بنفس اسم قاعدة بيانات الداونلود

الأسطر **4063** (أوفلاين) و**4090** (داونلود) تستخدمان نفس التنسيق `"From_%d_To_%d"`، والسطر **4162** `gdb_name = "Climate_Database_%s.gdb" % time_tag`.

الحماية الجديدة منعت **فقدان البيانات**، لكن تشغيل الأوفلاين ما زال **يكتب داخل قاعدة بيانات المستخدم** بصيغة `<Element>_Atlas`. النتيجة: تلوّث قاعدة بيانات الإدخال بنسخ إضافية، وخلط بين «بيانات محسوبة» و«مشتقات أطلس». الأنظف هو الفصل التام:

```python
if is_offline:
    gdb_name = "Climate_Atlas_Offline_%s.gdb" % time_tag
else:
    gdb_name = "Climate_Database_%s.gdb" % time_tag
```

### 🟡 F) لا تغذية راجعة داخل `_merge_offline_layers`

النطاق الحالي **5397‑5735**: عدد استدعاءات `SetProgressor` = **صفر**، و`msg()` = **6 فقط** على مدى ~340 سطرًا تشمل ثلاث دورات كاملة لإسقاط الأشكال هندسيًا (`projectAs` لكل نقطة) وإعادة بناء مخطط لكل عنصر. صار هذا أخفّ خطرًا لأن المسار السريع عادةً يعود مبكرًا، لكنه يظل كتلة صامتة طويلة إذا فرض اسم طبقة قديم/غريب المسار البطيء.

### 🟡 G) تصحيح ذاتي: «تعارض» `Hargreaves PET` الذي أشرت إليه سابقًا **غير ضار**

في مراجعة أولية بنيت على فحص `MODULE_SHORT` رصدت أن `MODULE_SHORT["Hargreaves PET"]` و`MODULE_SHORT["Evapotranspiration"]` كلاهما `"Evapotranspiration"`، و`MODULE_FOLDER` كلاهما `"14_Evapotranspiration"`، وأن `MODULE_FIELDS` لا يحتوي مفتاح `"Hargreaves PET"`، فظننته خرقًا لخريطة 1:1 التي يعلنها عنوان الالتزام.

**بعد التحقق الفعلي: هذا غير ضار**، لأن:

- `_DIRECT_ALIASES` تُفحص **قبل** حلقة `ALL_CANONICAL_MODULES`، لذلك `resolve_module_canonical("Hargreaves PET")` تُعيد `"Evapotranspiration"` ولا تُعيد `"Hargreaves PET"` أبدًا.
- `"Hargreaves PET"` ليس في قائمة الواجهة (`MODULES_ALL`) ⇒ لا يمكن للمستخدم اختياره.
- و`HIERARCHY = list(ALL_CANONICAL_MODULES)` يُرشَّح بـ `active_export_modules`، وبما أن المُحلِّل لا يُعيد `"Hargreaves PET"` أبدًا، فلا يمكن أن يدخل `ordered_modules`.

**الأثر الوحيد المتبقّي:** السطر **178** `ALL_CANONICAL_MODULES = PRIMARY_MODULES_ALL + DERIVED_MODULES_ALL + ["Hargreaves PET"]` يُسرّب هذا الاسم الوهمي إلى قائمة «Map Add Modules» الاحتياطية (السطر **3467** `map_choices = list(ALL_CANONICAL_MODULES)`) فيظهر خيار لا يمكن إنتاجه. **التوصية:** احذف `+ ["Hargreaves PET"]` من السطر 178 واتركه اسمًا قديمًا في `_DIRECT_ALIASES` فقط.

> **ملاحظة ثانوية:** `COLOR_RAMPS` لا يحتوي مفتاح `"Wind"` (فقط `Wind_Speed`/`Wind_Direction`). هذا **غير ضار** لأن `_colors_for` تعالج Wind بحالة خاصة — تحقّقت: `_colors_for('Wind','W_Spd_Annual_Mean')` و`('Wind','W_Dir_Annual_Mean')` تُعيدان التدرّجين الصحيحين. مجرد عدم اتساق شكلي.

---

## ثالثًا: اختبار حاسم مقترح للتحقق الميداني

الخلل الجذري أُصلح، لكن للتأكد من أن **مسار القص والحفظ** يعمل الآن من البداية للنهاية:

1. شغّل وضع الداونلود لسنة واحدة وعنصرين (مثل `Temperature` + `Relative Humidity`) — سريع.
2. ثم شغّل وضع الأوفلاين على نفس الطبقات، بنفس `Output_Workspace`، **مع إبقاء الطبقات مضافة إلى الخريطة** (لإعادة إنتاج ظرف الأقفال).
3. **المتوقّع الآن:** إمّا أن تُكتب النتائج في `<Element>_Atlas` بسلام، أو أن تُستخدم الطبقات مباشرة عبر المسار السريع.
4. **راقب في النافذة:** هل ظهرت الرسائل `[OK] Successfully saved: ...tif`؟ وهل وُجد ملف `.tif` فعليًا داخل مجلد العنصر (مثل `01_Temperature/T_Annual_Mean.tif`)؟
5. **افحص السلامة:** قارن أعمدة طبقات الإدخال قبل وبعد — يجب أن تكون **متطابقة تمامًا** (لا عمود مفقود، لا صف مُفرَّغ).
6. **أعد تشغيل الإثبات:** `python audit_offline_freeze_proof.py` — يجب أن يطبع `(none - inputs were left untouched)` و`total: 0 of 19 modules`.

---

## رابعًا: قائمة إصلاحات مختصرة (نسخ‑لصق)

| # | الملف | السطر | الإصلاح |
|:-:|---|---|---|
| 1 | `.pyt` | 4232‑4238 | حوّل `warn` إلى `raise RuntimeError` عند تجاوز حد الخلايا |
| 2 | `raster_atlas_generator.py` | قبل 2760 / عند 1629 | أضف `arcpy.env.outputCoordinateSystem = target_sr` |
| 3 | `raster_atlas_generator.py` | 2689 | احذف `arcpy.env.mask = clip_layer` (اكتفِ بـ `extent` + `ExtractByMask`) |
| 4 | `raster_atlas_generator.py` | ~2860 | لا تُرجِع `False` بصمت في `_interpolate_and_clip`؛ اجمع الأخطاء وأبلغ عنها |
| 5 | كلا الملفين | `_cleanup` | أضف `arcpy.ResetEnvironments()` |
| 6 | `.pyt` | 5254‑5264 | `makedirs_ok(rdir)` قبل إرجاع مسار الراستر |
| 7 | `.pyt` | 4162 | افصل اسم قاعدة بيانات الأوفلاين عن الداونلود |
| 8 | `.pyt` | 5397‑5735 | أضف `SetProgressor` + `msg` داخل حلقتَي الدمج |
| 9 | `.pyt` | 178 | احذف `+ ["Hargreaves PET"]` (اسم قديم فقط) |

---

## خامسًا: الخلاصة في سطرين

**الإصلاحات أصابت الهدف:** السبب الجذري للتجمّد (الكتابة داخل طبقات المستخدم بسبب فشل `resolve_module_canonical`) أُصلح، ومُثبَت بالتنفيذ، ومحمي بطبقة ثانية اختبرتها بعدائيًا، والمصفوفة الاختبارية خضراء. **ما تبقّى ليس من فئة التجمّد الأصلي**، لكن أهمّه بندان: حارس حجم الخلايا ما زال تحذيرًا لا رفضًا (`.pyt` 4224)، والمحرّك الثاني في `raster_atlas_generator.py` لم يمسّه أي إصلاح وبه خطأ نظام إحداثيات يمكن أن يضخّم العمل ~10¹⁰ مرة — فإن كنت تستخدم أداة «POWER **Raster** Climate Atlas Generator» فأنت على النسخة غير المُصلَحة.

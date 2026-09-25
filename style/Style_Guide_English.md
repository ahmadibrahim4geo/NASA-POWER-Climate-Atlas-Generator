# ArcMap Desktop 10.8 Climate Styles User Guide
## NASA POWER & Open-Meteo Climate Atlas - Style User Guide (English)
### Developed by: Ahmad Ibrahim — [@ahmadibrahim4geo](https://github.com/ahmadibrahim4geo)

---

### 1. Cartographic System Overview (Mega Edition)
This cartographic system was engineered to serve as the definitive physical and cartographical reference for GIS, climatology, and meteorological mapping applications in Esri ArcMap 10.8 and ArcGIS Desktop:
- **125 Peer-Reviewed Scientific Styles:** Covering all atmospheric, thermal, hydrologic, solar, radiation, wind, pressure, and climate change projection variables.
- **9 Comprehensive Class Tiers:** [3, 4, 5, 6, 7, 8, 9, 10, and 11 classes] per style (covering both odd diverging schemes and even monotonic/bipolar schemes).
- **2,250 Native ArcMap Color Ramps:** Fully compiled and integrated into `NASA_POWER_Climate_Atlas_Master.style`.
- **875 Named Colors (`[Colors]`):** Available directly in color palette pickers for precise category assignment and zero-divergence neutral baselines.
- **875 Solid Polygon Fill Symbols (`[Fill Symbols]`):** Built with soft neutral outlines (0.4 pt) optimized for vector climate zones, administrative overlays, and basin polygons.

---

### 2. Color Ramp Architectures: `[Stepped]` vs. `[Smooth]`

For every style and each tier (from 3 to 11 classes), two distinct architectures are provided:
1. **`[Stepped]` Ramps (Solid Multi-Part Blocks):**
   - Each interval is rendered as a discrete, uniform solid color block (`MultipartColorRamp` of uniform algorithmic intervals) with zero internal gradients or edge bleeding.
   - **Recommended For:** Classified raster datasets (`Symbology -> Classified`), choropleth zoning, discrete vulnerability indices, drought severity classes, and radar reflectivity levels.
2. **`[Smooth]` Ramps (Continuous Perceptual Gradients):**
   - Seamless gradient transitions interpolated within the physical CIE L\*a\*b\* perceptual color space.
   - **Recommended For:** Continuous stretched raster surfaces (`Symbology -> Stretched`), digital elevation models, continuous temperature fields, and barometric pressure surfaces.

---

### 3. Diverging Symmetry Standards (Zero-Centered Anomalies)
- **11 Classes (5 - 1 - 5 Architecture):** 5 negative/cool/dry bins + 1 neutral baseline (`#FFFFFF` or `#F7F7F7`) + 5 positive/warm/wet bins.
- **9 Classes (4 - 1 - 4 Architecture):** 4 negative bins + 1 neutral baseline + 4 positive bins.
- **7 Classes (3 - 1 - 3 Architecture):** 3 negative bins + 1 neutral baseline + 3 positive bins.
- **5 Classes (2 - 1 - 2 Architecture):** 2 negative bins + 1 neutral baseline + 2 positive bins.
- **3 Classes (1 - 1 - 1 Architecture):** 1 negative bin + 1 neutral baseline + 1 positive bin.
- **Even Classes (4, 6, 8, 10 Classes):** Balanced polar contrast without an explicit zero breakpoint, ideal for quartiles, sextiles, octiles, and deciles.

---

### 4. How to Load and Apply Styles in ArcMap Desktop:

#### A. Adding Styles to Style Manager:
1. Open **ArcMap Desktop 10.8**.
2. From the main menu, navigate to **`Customize`** -> **`Style Manager...`**.
3. In the Style Manager dialog, click the **`Styles...`** button on the right-hand panel.
4. Click **`Add Style to List...`**.
5. Browse to:
   `style\All_ArcMap_Styles_Consolidated\`
6. Select the master style file: **`NASA_POWER_Climate_Atlas_Master.style`** (or any specific element file such as `01_Temperature.style`).
7. Click **Open**, then click **OK**.

#### B. Applying to Classified Raster Layers:
1. Right-click the raster layer in the **Table of Contents** -> **Properties**.
2. Select the **Symbology** tab.
3. In the left renderer pane, select **Classified**.
4. In the **Classes** dropdown, choose your desired number of classes (from 3 to 11).
5. Click the **Color Ramp** dropdown:
   - Select the ramp labeled with **`[Stepped]`** for crisp, discrete class blocks.
   - Or select **`[Smooth]`** for continuous gradient transition.
6. Click **Apply** and then **OK**.

#### C. Applying Fill Symbols to Vector Layers:
1. Click the symbology patch of your polygon layer to open the **Symbol Selector**.
2. Under Style References, ensure your loaded Climate Style is active.
3. Select from the 875 standardized **`Fill Symbols`** to instantly apply calibrated scientific colors with clean outlines (0.4 pt).

---

### 5. Included Documentation in `style/`:
- **Master Word Reference:** `Climate_Styles_Sources_and_References.docx` (comprehensive documentation of all 15 international cartographic and meteorological standards).
- **Master Visual Excel Workbook:** `NASA_POWER_Climate_Atlas_Master_Styles.xlsx` (contains all 2,250 color ramps and 875 colors rendered with true RGB background cell fills).
- **Arabic Guide:** `Style_Guide_Arabic.md`.

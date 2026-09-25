# Comprehensive Scientific and Technical Guide
# NASA POWER & Open-Meteo Climate Atlas Generator (ArcGIS 10.8)

---

## Table of Contents
1. [Overview & Engineering Goals](#1-overview--engineering-goals)
2. [Dual Operation Modes](#2-dual-operation-modes)
   - [A. Online Pipeline: Download & Generate Atlas](#a-online-pipeline-download--generate-atlas)
   - [B. Offline Mode: Interpolate & Map Existing Data](#b-offline-mode-interpolate--map-existing-data)
3. [WMO 30-Year Climatological Normals Standards](#3-wmo-30-year-climatological-normals-standards)
   - [Definition of 30-Year Climatological Normals](#definition-of-30-year-climatological-normals)
   - [Reference Periods: 1991–2020 vs. 1961–1990](#reference-periods-19912020-vs-19611990)
   - [Statistical Filtering of Interannual Noise](#statistical-filtering-of-interannual-noise)
4. [The 10 Climate Modules & Meteorological Seasons](#4-the-10-climate-modules--meteorological-seasons)
   - [Standard WMO Meteorological Seasons (DJF, MAM, JJA, SON)](#standard-wmo-meteorological-seasons-djf-mam-jja-son)
   - [Module Architecture & Indicator Coverage](#module-architecture--indicator-coverage)
5. [Drought & Aridity Indices with Auto-Dependency Resolution](#5-drought--aridity-indices-with-auto-dependency-resolution)
   - [De Martonne Aridity Index](#de-martonne-aridity-index)
   - [FAO-56 Hargreaves-Samani Potential Evapotranspiration (PET)](#fao-56-hargreaves-samani-potential-evapotranspiration-pet)
   - [UNEP Aridity Index](#unep-aridity-index)
   - [Climatic Water Deficit / Surplus](#climatic-water-deficit--surplus)
   - [Biologically Dry Months (Walter-Lieth)](#biologically-dry-months-walter-lieth)
6. [Data Quality Control & Gap-Filling Mechanisms](#6-data-quality-control--gap-filling-mechanisms)
   - [Sentinel Filtering (-999.0)](#sentinel-filtering--9990)
   - [Temporal & Spatial Imputation Algorithms](#temporal--spatial-imputation-algorithms)
   - [Point Spatial Tolerance Thinning](#point-spatial-tolerance-thinning)
7. [Atmospheric & Satellite Reanalysis Sources](#7-atmospheric--satellite-reanalysis-sources)
   - [NASA POWER: MERRA-2 & CERES SYN1deg](#nasa-power-merra-2--ceres-syn1deg)
   - [Open-Meteo: ERA5-Land (~9 km Resolution)](#open-meteo-era5-land-9-km-resolution)
8. [Formatted Excel (.xls) Workbooks & Arabic UTF-8 BOM Encoding](#8-formatted-excel-xls-workbooks--arabic-utf-8-bom-encoding)
   - [UTF-8 BOM Implementation in CSV Files](#utf-8-bom-implementation-in-csv-files)
   - [Master Multi-Sheet Excel Workbook](#master-multi-sheet-excel-workbook)
   - [Right-to-Left (RTL) Arabic Worksheets](#right-to-left-rtl-arabic-worksheets)
9. [Spatial Interpolation, Masking & Layer Styling](#9-spatial-interpolation-masking--layer-styling)
   - [IDW Gentle Decay vs. Classical Quadratic Decay](#idw-gentle-decay-vs-classical-quadratic-decay)
   - [Spline with Tension & Kriging Options](#spline-with-tension--kriging-options)
   - [Focal Smoothing & Polygon Mask Clipping](#focal-smoothing--polygon-mask-clipping)
   - [Isobars & Wind Vectors Integration](#isobars--wind-vectors-integration)

---

## 1. Overview & Engineering Goals

The **NASA POWER & Open-Meteo Climate Atlas Generator** is an enterprise-grade ArcGIS 10.8 Python Toolbox (`.pyt`) engineered in pure Python 2.7 / ArcPy. It automates the extraction, quality control, mathematical calculation, spatial interpolation, cartographic symbology, and data export of **82 climatological, hydrological, and bioclimatic indicators**.

### Key Architectural Strengths:
- **100% Standalone**: Runs in 32-bit ArcGIS 10.8 without external dependencies (uses native `arcpy`, `requests`, `urllib2`, `csv`, and `xlwt`).
- **Dual Operating Modes**: Complete online download pipeline or 100% offline interpolation of pre-existing datasets.
- **WMO Compliant**: Full adherence to World Meteorological Organization (WMO) climatological standards and meteorological seasons.
- **Multimodal Output**: File Geodatabase feature classes, shapefiles, LZW-compressed GeoTIFF rasters, ArcGIS layer files (`.lyr`), UTF-8 BOM CSV files, and professionally styled Excel workbooks (`.xls`).

---

## 2. Dual Operation Modes

A master parameter at the very top of the tool (`Operation_Mode`) dictates the operational pipeline:

### A. Online Pipeline: Download & Generate Atlas (`Download & Generate Atlas (Full Pipeline) [Default]`)
- **Use Case**: Starting from bare station coordinates or sample point features.
- **Behavior**:
  - `Input_Point_Features` is enabled; `Precalculated_Point_Layer` is disabled.
  - All internet access parameters (`Climate_Data_Source`, `OpenMeteo_Model`), time configuration (`Time_Mode`, `Single_Year`, `Start_Year`, `End_Year`, calendar controls), temporal resolution, and gap filling are active.
  - Sequentially queries NASA POWER or Open-Meteo ERA5 APIs, computes 82 indicators, writes to GDB/Shapefile, generates rasters, contours, wind arrows, styled layers, and Excel files.

### B. Offline Mode: Interpolate & Map Existing Data (`Interpolate & Map Existing Data (Offline Mode - No Internet)`)
- **Use Case**: Reprocessing, re-interpolating, re-masking, or changing cell size on point datasets generated during a previous run without requiring an internet connection.
- **Behavior**:
  - `Input_Point_Features` is disabled; `Precalculated_Point_Layer` is enabled.
  - **All online and download parameters are disabled and locked**.
  - **Automatic Field Discovery**: When a layer is chosen, the engine scans its fields, identifies which climate modules are present, and preselects them in `Climate_Modules` and `Variables Selection (Checklist)`.
  - Directly executes spatial interpolation (IDW / Kriging / Spline), mask clipping, focal smoothing, `.lyr` styling, and master Excel workbook creation directly from the local data.

---

## 3. WMO 30-Year Climatological Normals Standards

### Definition of 30-Year Climatological Normals
Under the guidelines of the World Meteorological Organization (**WMO-No. 1203: WMO Guidelines on the Calculation of Climate Normals**), a **Climatological Normal** is defined as an average of climatological data computed for the following consecutive 30-year period:
$$\text{Normal} = \frac{1}{30} \sum_{y=1}^{30} X_y$$

### Reference Periods: 1991–2020 vs. 1961–1990
- **1991–2020 (Current Standard Climatological Normal)**: Adopted internationally by WMO in 2021 as the official reference baseline for weather and climate monitoring, agricultural planning, and infrastructure design.
- **1961–1990 (Historical Reference Normal)**: Preserved as the fixed reference standard for assessing long-term global climate change and historical warming trends.

### Statistical Filtering of Interannual Noise
Climate variables naturally exhibit substantial interannual variance driven by large-scale oscillatory modes (e.g., ENSO, NAO, IOD). A short period (e.g., 5 or 10 years) can be severely distorted by an abnormal drought or high precipitation anomaly. A 30-year window provides statistical stability, minimizes sample variance, and establishes an authoritative baseline for computing climate anomalies ($\Delta X = X - X_{normal}$).

---

## 4. The 10 Climate Modules & Meteorological Seasons

### Standard WMO Meteorological Seasons (DJF, MAM, JJA, SON)
The tool strictly adheres to standard 3-month meteorological seasons based on full calendar months:
- **Winter (DJF)**: December, January, February
- **Spring (MAM)**: March, April, May
- **Summer (JJA)**: June, July, August
- **Autumn (SON)**: September, October, November

### Module Architecture & Indicator Coverage
1. **Temperature (`01_Temperature`)**: 13 indicators including annual/seasonal means, annual range, warmest summer month, coldest winter month, extreme daily means, and perceived temperature indices (Annual & Summer Steadman-Rothfusz Heat Index, Winter Humidex IH).
2. **Precipitation (`02_Precipitation`)**: 8 indicators including annual total, monthly average, seasonal totals, maximum 24h rainfall, and rain days ($\ge 0.1\text{ mm}$).
3. **Drought & Aridity (`10_Drought_And_Aridity`)**: 5 indicators (De Martonne, Hargreaves PET, UNEP Aridity Index, Climatic Water Deficit, Biologically Dry Months).
4. **Sea Level Pressure (`03_Sea_Level_Pressure`)**: 6 indicators covering annual and seasonal mean sea level pressure (MSLP).
5. **Surface Pressure (`04_Surface_Pressure`)**: 6 indicators covering actual station-level surface barometric pressure.
6. **Wind (`05_Wind`)**: 12 indicators covering 10m wind speeds and circular vector mean wind direction ($\text{atan2}$).
7. **Relative Humidity (`06_Humidity`)**: 6 indicators covering 2m relative humidity.
8. **Solar Radiation (`07_Solar_Radiation`)**: 7 indicators covering daily insolation rates and annual cumulative energy ($\text{kWh/m}^2/\text{year}$).
9. **UV Index (`08_UV_Index`)**: 6 indicators covering solar noon ultraviolet radiation hazard classes.
10. **Cloud Cover (`09_Cloud_Cover`)**: 6 indicators covering all-sky cloud fraction percentages.

---

## 5. Drought & Aridity Indices with Auto-Dependency Resolution

### Auto-Dependency Resolution
To calculate drought and evapo-transpiration metrics, 4 climate parameters are required:
`["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN"]`.
When a user selects `Drought & Aridity` alone without enabling Temperature or Precipitation, the engine **automatically requests and retrieves these required underlying parameters in the background**, calculating the drought indices without forcing the creation of unwanted temperature or rainfall layers.

### Formulations and Classifications:

#### 1. De Martonne Aridity Index (`DM_Aridity_Annual`):
$$I_{DM} = \frac{P}{T + 10}$$
- $I_{DM} < 5$: Hyper-arid
- $5 \le I_{DM} < 10$: Arid
- $10 \le I_{DM} < 20$: Semi-arid
- $20 \le I_{DM} < 30$: Sub-humid
- $I_{DM} \ge 30$: Humid

#### 2. FAO-56 Hargreaves-Samani PET (`PET_Hargreaves_Annual`):
$$PET = 0.0023 \times R_a \times (T_{mean} + 17.8) \times \sqrt{T_{max} - T_{min}}$$
Where $R_a$ is extraterrestrial solar radiation computed astronomically from station latitude and calendar month Julian days, converted to mm/day equivalent ($\times 0.408$).

#### 3. UNEP Aridity Index (`UNEP_Aridity_Annual`):
$$AI = \frac{P}{PET}$$
- $AI < 0.05$: Hyper-arid (e.g., Western Desert of Egypt)
- $0.05 \le AI < 0.20$: Arid
- $0.20 \le AI < 0.50$: Semi-arid
- $0.50 \le AI < 0.65$: Dry sub-humid
- $AI \ge 0.65$: Humid

#### 4. Climatic Water Deficit (`Water_Deficit_Annual`):
$$WD = P - PET$$
Negative values denote seasonal or annual water deficits and irrigation requirements.

#### 5. Biologically Dry Months (`Dry_Months_Count`):
Count of calendar months where precipitation is less than twice the mean monthly temperature ($P_{month} < 2 \times T_{month}$) following Walter-Lieth bioclimatological criteria.

---

## 6. Data Quality Control & Gap-Filling Mechanisms

### Sentinel Filtering (-999.0)
All NASA and reanalysis missing indicators (`-999.0`, `None`, `NaN`) are intercepted and converted to `None / NoData`. This prevents catastrophic interpolation artifacts.

### Imputation Methods (`Gap_Fill_Method`)
- **Climatological Month Mean (Recommended)**: Missing months in a given year are imputed using the long-term mean of that specific calendar month across valid years for that point.
- **Linear + Boundary Interpolation**: Fills interior missing sequences linearly and holds endpoints.
- **Spatial Nearest Neighbor Fallback**: Missing attributes at an isolated point are estimated via Inverse Distance Weighting from the nearest valid spatial neighbors.

---

## 7. Atmospheric & Satellite Reanalysis Sources

- **NASA POWER**: Integrates NASA's GMAO MERRA-2 assimilation model (~50 km horizontal resolution) and CERES satellite radiation products (~100 km).
- **Open-Meteo ERA5-Land**: Provides European Centre for Medium-Range Weather Forecasts (ECMWF) atmospheric reanalysis at **9 km (0.1°)** spatial resolution, delivering unprecedented regional fidelity.

---

## 8. Formatted Excel (.xls) Workbooks & Arabic UTF-8 BOM Encoding

### UTF-8 BOM in CSV Files
All CSV exports prepend the Byte Order Mark `\xef\xbb\xbf`, ensuring Microsoft Excel opens Arabic text cleanly without garbled characters.

### Master Styled Workbook (`Climate_Atlas_Master_Workbook.xls`)
Generated automatically using the native `xlwt` library in Python 2.7:
- Dark blue header rows (`fore_colour dark_blue`) with bold white text.
- Alternating zebra row striping.
- Thin borders on all cells.
- Automated column width fitting.
- Single multi-sheet workbook containing individual tabs for each climate element.
- Arabic metadata and field dictionaries formatted with native Right-to-Left (`rtl=True`) worksheet orientation.

---

## 9. Spatial Interpolation, Masking & Layer Styling

- **IDW Gentle Decay**: Uses power = 1.2 by default to eliminate artificial bullseye patterns around stations.
- **Spline with Tension**: Produces smooth surfaces that strictly honor station values without extreme overshooting.
- **ExtractByMask**: Clips all outputs cleanly to the polygon study area boundary with enforced LZW TIFF compression.
- **Layer Symbology (`.lyr`)**: Generates calibrated color-ramped ArcGIS layer files ready for immediate cartographic publishing.

### Raster Reclassification Options
Located directly beneath the **Interpolation Parameters** category:
- **Default State (`Enable_Raster_Reclass = False`)**:
  - Only clean, continuous floating-point surface GeoTIFFs (`.tif`) are generated, without creating additional discrete classified files. Layer files (`.lyr`) and sidecar JSONs reference the continuous raster directly.
- **When Enabled (`Enable_Raster_Reclass = True`)**:
  - **Number of Classes (`Reclass_Classes_Count`)**: User-selectable from 2 to 32 classes (default: 7).
  - **Classification Method (`Reclass_Method`)**:
    1. **Natural Breaks (Jenks)**: Minimizes squared deviations within classes while maximizing variance between classes.
    2. **Equal Interval**: Partitions the span into intervals of equal range.
    3. **Equal Area (Quantile)**: Equal number of grid cells per class.
    4. **Geometric Interval**: Geometrically distributed ranges suited for skewed climate data.
    5. **Standard Deviation**: Classifies cells relative to their mean and standard deviation.
  - Automatically generates classified display rasters (`_cls.tif`), builds Raster Attribute Tables (VAT), embeds `.clr` colormaps mathematically interpolated to the requested class count, and documents precise true-data break boundaries in layer metadata.

# Comprehensive Scientific and Technical Guide
# NASA POWER & Open-Meteo Climate Atlas Generator
## Native Dual Compatibility for ArcGIS Pro (Python 3) & ArcMap 10.8 (Python 2.7)

[![Developer](https://img.shields.io/badge/Developer-Ahmad%20Ibrahim-1F4E79.svg?style=for-the-badge&logo=github)](https://github.com/ahmadibrahim4geo)
[![Platform](https://img.shields.io/badge/Platform-ArcGIS%20Pro%20%7C%20ArcMap%2010.8-0079c1.svg)](https://www.esri.com/)
[![Repository](https://img.shields.io/badge/Repository-NASA--POWER--Climate--Atlas--Generator-blue.svg)](https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator)

---

## Table of Contents
1. [Overview & Engineering Goals](#1-overview--engineering-goals)
2. [Dual Architecture: ArcGIS Pro & ArcMap 10.8](#2-dual-architecture-arcgis-pro--arcmap-108)
3. [The Dual-Tool Workflow Architecture](#3-the-dual-tool-workflow-architecture)
4. [The 17 Modular Climate Layers](#4-the-17-modular-climate-layers)
5. [Dual Operation Modes & Smart Skip Execution](#5-dual-operation-modes--smart-skip-execution)
   - [A. Online Pipeline (Download & Generate Atlas)](#a-online-pipeline-download--generate-atlas)
   - [B. Offline Pipeline (Interpolate & Map Existing Data)](#b-offline-pipeline-interpolate--map-existing-data)
6. [Spatial Masking Rules & Non-Destructive Principles](#6-spatial-masking-rules--non-destructive-principles)
   - [Station Points Invariance Rule](#station-points-invariance-rule)
   - [Products Strictly Subject to Mask Clipping](#products-strictly-subject-to-mask-clipping)
7. [High-Efficiency Lossless LZW Block Tiling Compression](#7-high-efficiency-lossless-lzw-block-tiling-compression)
8. [Wind Vector Fields & Directional Flow Dynamics](#8-wind-vector-fields--directional-flow-dynamics)
9. [WMO 30-Year Climatological Normals Standards](#9-wmo-30-year-climatological-normals-standards)
10. [Global Bioclimatic & Aridity Models](#10-global-bioclimatic--aridity-models)
11. [Data Quality Control & Gap-Filling Protocols](#11-data-quality-control--gap-filling-protocols)
12. [Data Interoperability & Schema Standards](#12-data-interoperability--schema-standards)

---

## 1. Overview & Engineering Goals

The **NASA POWER & Open-Meteo Climate Atlas Generator** is an enterprise-grade geoprocessing platform engineered to automate the ingestion, quality assurance, climatological calculations, spatial interpolation, cartographic symbology, and multi-format dissemination of multi-decadal meteorological data.

### Primary Objectives:
1. Eliminate manual barriers to acquiring global historical reanalysis and projection datasets from **NASA POWER** (MERRA-2, CERES) and **Open-Meteo** (ERA5-Land ~9 km).
2. Automate mathematically sound spatial interpolation and climatological normal calculations following **World Meteorological Organization (WMO)** standards.
3. Deliver a robust, modular schema comprising **17 discrete thematic feature classes**.
4. Optimize raster generation pipelines using high-performance, **lossless block-tiled LZW compression** without scientific precision degradation.

---

## 2. Dual Architecture: ArcGIS Pro & ArcMap 10.8

The codebase features a cross-compatible hybrid engine providing seamless operation across both major Esri software generations:

- **ArcGIS Pro (2.x / 3.x) with Python 3.x**:
  - Full Python 3 unicode compliance, avoiding legacy `unicode()` or `str.decode()` exceptions.
  - Safe evaluation of dictionary views (`list(dict.values())`) and modern iterables.
  - Mitigation of intermediate scratch deletion routines (`arcpy.management.Delete`), guaranteeing user layers in the Contents pane / Table of Contents (TOC) remain permanently visible during and after execution.
- **ArcMap 10.8 with Python 2.7**:
  - Full 32-bit ArcObjects / COM backward compatibility.
  - Built-in interactive Tkinter visual calendar modal (`calendar_dialog.py`).
  - Professional Excel reporting (`.xls`) with explicit UTF-8 BOM encoding for uncorrupted Arabic script support.

---

## 3. The Dual-Tool Workflow Architecture

The platform operates via two complementary tools:
1. **`POWER_Climate_Atlas_Generator_10_8.pyt` (Feature Atlas Generator)**:
   - Primary user-facing Geoprocessing Toolbox.
   - Handles API communications, rate-limiting, quality control, calendar GUI interactions, and 92 climatological indicators.
   - Generates the authoritative `Climate_Database.gdb` with 17 structured feature classes.
2. **`raster_atlas_generator.py` (Raster Surface Engine)**:
   - Core backend spatial processing engine.
   - Executes spatial surface interpolation (IDW with smooth power profiles, Ordinary Kriging, Spline with Tension, Natural Neighbor).
   - Manages focal smoothing filters, polygon boundary clipping, isobar contouring, wind vector arrow grids, and lossless LZW compression.

---

## 4. The 17 Modular Climate Layers

Legacy bundled outputs have been fully refactored into **17 discrete, standalone feature classes**:

| # | Feature Class | Scientific Description | Units |
|:---:|---|---|:---:|
| **01** | `01_Temperature` | Annual/seasonal means (DJF, MAM, JJA, SON), thermal range, summer/winter extremes, and dew point temperatures (Td). | °C |
| **02** | `02_Precipitation` | Annual total, monthly mean, seasonal accumulated totals, 1-day maximum, and annual rain day frequency. | mm, days |
| **03** | `03_Sea_Level_Pressure` | Atmospheric pressure reduced to mean sea level (MSLP) annual/seasonal means and range. | hPa / mbar |
| **04** | `04_Surface_Pressure` | True atmospheric pressure at actual station topographic elevation. | hPa / mbar |
| **05** | `05_Wind` | 10-meter wind speed means, circular mean vector wind directions, and annual wind range. | m/s, degrees (°) |
| **06** | `06_Relative_Humidity` | 2-meter relative humidity annual/seasonal means and annual psychrometric range. | % |
| **07** | `07_Solar_Radiation` | All-sky shortwave downward solar irradiance daily means and accumulated annual totals. | kWh/m²/day, kWh/m²/year |
| **08** | `08_UV_Index` | Solar noon all-sky UV radiation index adhering to World Health Organization (WHO) risk scales. | index (0–15+) |
| **09** | `09_Cloud_Cover` | Annual and seasonal all-sky cloud fractions and sunshine duration dynamics. | % |
| **10** | `10_De_Martonne_Aridity` | De Martonne aridity index ($I_{DM} = P / (T + 10)$) and bioclimatic aridity classifications. | dimensionless index |
| **11** | `11_Hargreaves_PET` | FAO-56 Hargreaves-Samani potential evapotranspiration computed with astronomical solar radiation ($R_a$). | mm/year |
| **12** | `12_UNEP_Aridity` | United Nations Environment Programme aridity ratio ($AI = P / PET$) for dryland classification. | ratio |
| **13** | `13_Water_Deficit` | Annual net climatic water balance ($WD = P - PET$). | mm/year |
| **14** | `14_Dry_Months` | Walter-Lieth biologically dry months count ($P < 2T$). | months (0–12) |
| **15** | `15_Heat_Index` | Steadman-Rothfusz apparent temperature (Heat Index), winter Humidex, and summer shade WBGT heat stress. | °C |
| **16** | `16_Wind_Chill` | Osczevski-Bluestein equivalent wind chill temperature index. | °C |
| **17** | `17_Trends_And_Anomalies` | Decadal linear climate trends and annual/seasonal anomalies relative to the 1991–2020 WMO normal. | °C/decade, mm/decade, % |

---

## 5. Dual Operation Modes & Smart Skip Execution

### A. Online Pipeline (`Download & Generate Atlas`)
- Ingests raw station coordinates or point features.
- Connects to NASA POWER or Open-Meteo ERA5-Land APIs.
- Applies QA/QC, gap-fills missing dates, computes all 92 indicators, and creates `Climate_Database.gdb`.

### B. Offline Pipeline (`Interpolate & Map Existing Data`)
- 100% offline workflow without internet dependency.
- **Smart Skip Logic**: If `Climate_Database.gdb` or previously downloaded outputs exist in the project directory, the tool automatically reuses them rather than rebuilding or overwriting from scratch.
- **TOC Integrity**: Eliminates intermediate layer drops, guaranteeing that user layers remain visible in the Table of Contents / Contents pane.
- **Auto-Field Discovery**: Automatically detects present variables and pre-activates corresponding module checklists upon selecting the precalculated layer.

---

## 6. Spatial Masking Rules & Non-Destructive Principles

### Station Points Invariance Rule
- **Point features are NEVER clipped by the study area polygon**.
- Preserving the full input point set maintains geographical context, allows boundary spatial interpolation without edge distortion, and keeps the station database intact for reuse in broader or adjacent studies.

### Products Strictly Subject to Mask Clipping
Polygon mask clipping (`Study_Area_Mask`) is applied exclusively to derived spatial products:
1. **Continuous raster surfaces (GeoTIFFs)**.
2. **Atmospheric pressure isobars (Contours)**.
3. **Directional wind vector arrow grids**.

---

## 7. High-Efficiency Lossless LZW Block Tiling Compression

- Utilizes `arcpy.management.CopyRaster` configured with **LZW compression** and **`128x128` block tiling** (`tileSize="128 128"`).
- Suppresses intermediate pyramid computation overhead (`arcpy.env.pyramid = "NONE"`).
- **Verified Benchmark Results**:
  - **34.8% reduction in raster file size** on disk.
  - **100% Bit-for-Bit Lossless Precision**: Evaluated using numerical matrix differentiation via NumPy; absolute maximum cell divergence is identically zero (`max_diff = 0.000000000000000`). All floating-point decimal precision is completely conserved.

---

## 8. Wind Vector Fields & Directional Flow Dynamics

- Produces continuous wind speed surfaces alongside circular vector mean wind direction surfaces (0–360° azimuth).
- Generates a regularized point grid whose spatial density is controlled via `Wind_Factor_Cell_Size`.
- Samples speed and azimuth values onto grid points, clips the grid to the study mask, and configures directional arrow symbology to depict airflow patterns.

---

## 9. WMO 30-Year Climatological Normals Standards

- The tool aligns with **WMO-No. 1203** standards specifying 30-year consecutive averaging periods to eliminate decadal climate noise.
- Current global baseline: **1991–2020**.
- Meteorological seasons:
  - **Winter (DJF)**: December, January, February
  - **Spring (MAM)**: March, April, May
  - **Summer (JJA)**: June, July, August
  - **Autumn (SON)**: September, October, November

---

## 10. Global Bioclimatic & Aridity Models

- **De Martonne Aridity Index**: $I_{DM} = P / (T + 10)$
- **FAO-56 Hargreaves-Samani PET**: $PET = 0.0023 \cdot R_a \cdot (T_{mean} + 17.8) \cdot \sqrt{T_{max} - T_{min}}$
- **UNEP Aridity Ratio**: $AI = P / PET$
- **Climatic Water Deficit**: $WD = P - PET$
- **Biologically Dry Months (Walter-Lieth)**: $P_{month} < 2 \cdot T_{month}$

---

## 11. Data Quality Control & Gap-Filling Protocols

- Translates NASA `-999.0` missing values to `None / Null`.
- Imputation methods: Climatological month mean, linear boundary interpolation, and spatial nearest neighbor fallback.

---

## 12. Data Interoperability & Schema Standards

- **Geodatabase (`Climate_Database.gdb`)**: 17 clean feature classes with sequential, gap-free `OBJECTID` indexing and zero orphaned export fields.
- **Shapefiles (`.shp`)**: Optional clean export with 10-character field truncation.
- **Arabic Database (`Climate_Database_AR.gdb`)**: Features Arabic field aliases while preserving English physical names for offline pipeline reusability.
- **Excel Master Workbook**: Professionally styled workbooks with UTF-8 BOM encoding.
- **Authoritative Data Dictionary**: Referenced in `Fields_AR_EN_Units.xlsx`.

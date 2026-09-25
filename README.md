# NASA POWER & Open-Meteo Climate Atlas Generator for ArcGIS Desktop 10.8

[![ArcGIS Version](https://img.shields.io/badge/ArcGIS%20Desktop-10.8%20%7C%2010.x-0079c1.svg)](https://desktop.arcgis.com/)
[![Python Version](https://img.shields.io/badge/Python-2.7%20%7C%203.x-3776ab.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Sources](https://img.shields.io/badge/Data%20Sources-NASA%20POWER%20%7C%20Open--Meteo-blue.svg)](https://power.larc.nasa.gov/)
[![Styles Count](https://img.shields.io/badge/Styles-125%20Palettes%20%7C%202%2C250%20Ramps-darkgreen.svg)](#the-cartographic-mega-system-mega-edition)

An enterprise-grade, peer-reviewed Climate Atlas Generator and scientific cartography suite engineered natively for **Esri ArcMap Desktop 10.8**. 

The system automates the acquisition, climatological processing, statistical aggregation, spatial interpolation, and standardized cartographic rendering of multi-decadal historical climate records and future climate change models directly inside ArcGIS Desktop.

---

## 🌟 Key Features

- **Dual API Data Acquisition:** Direct integration with **NASA POWER API** (Prediction Of Worldwide Energy Resources) and **Open-Meteo Climate API** (ERA5 Reanalysis & CMIP6 Projections).
- **Automated Climatological Engine:** Computes annual, seasonal, monthly, daily, and custom date range statistics, standard deviations, and climatological normals.
- **Interactive Visual Calendar GUI:** Native date picker modal embedded directly into ArcMap toolbox parameters, allowing effortless month/year navigation without manual string entry.
- **Spatial Interpolation & Focal Smoothing:** Automated generation of continuous climate surfaces via IDW (Inverse Distance Weighted), Spline, and focal neighborhood filter smoothing.
- **The Cartographic Mega System (Mega Edition):**
  - **125 Scientific Styles** across 11 climate domains.
  - **9 Class Tiers** per style: `3, 4, 5, 6, 7, 8, 9, 10, and 11 classes`.
  - **2,250 Native ArcMap Color Ramps** categorized into `[Stepped]` (solid classification blocks) and `[Smooth]` (perceptually uniform CIE L\*a\*b\* gradients).
  - **875 Named Colors** and **875 Polygon Fill Symbols** with 0.4 pt neutral borders.
- **Master Visual Reference Workbook (`NASA_POWER_Climate_Atlas_Master_Styles.xlsx`):** Multi-sheet Excel reference containing all 2,250 ramps with **true background color fills** rendered in individual cells.
- **Master Reference Documentation (`Climate_Styles_Sources_and_References.docx`):** Fully documented physical foundations, peer-reviewed citations, and international standards.
- **Multi-Format Export Pipeline:** Exports into ESRI File Geodatabase (`.gdb`), Shapefile (`.shp`), GeoTIFF rasters, and formatted Excel workbooks.

---

## 🗺️ The Cartographic Mega System (Mega Edition)

The atlas provides 125 peer-reviewed color palettes organized across 11 thematic climate elements:

| # | Element Domain | Styles | Ramps (3–11 Classes) | Primary International Standards |
|---|---|:---:|:---:|---|
| **01** | **Temperature** | 16 | 288 | WMO No. 522, IPCC AR6 WGI, NOAA NCEI, ColorBrewer |
| **02** | **Precipitation** | 14 | 252 | WMO Guide No. 168, GPCC, NOAA CPC, CHIRPS |
| **03** | **Sea Level Pressure** | 10 | 180 | WMO Surface Synoptic, DWD MSLP, ECMWF ERA5 |
| **04** | **Surface Pressure** | 9 | 162 | Hypsometric Barometric, Standard Atmosphere |
| **05** | **Wind Speed & Direction** | 12 | 216 | Beaufort Scale (WMO No. 8), IEC 61400-1, NOAA NWS |
| **06** | **Relative Humidity** | 10 | 180 | Psychrometric Vapour, NOAA Vapor Pressure Deficit |
| **07** | **Solar Radiation** | 12 | 216 | NREL NSRDB, Copernicus CAMS, PVGIS Solar Atlas |
| **08** | **UV Index** | 8 | 144 | WHO / WMO Global Solar UV Index Standard |
| **09** | **Cloud Cover & Sunshine** | 10 | 180 | WMO Octas Code, ISCCP Cloud Physics, NASA CERES |
| **10** | **Drought & Aridity** | 12 | 216 | US Drought Monitor, UNEP AI, WMO SPI / SPEI |
| **11** | **Climate Change & Models** | 12 | 216 | IPCC AR6 Warming Scenarios, CMIP6 Ensemble, Crameri |
| **Total** | **All 11 Domains** | **125** | **2,250** | **15 International Meteorological & Cartographic Standards** |

### Ramp Types: `[Stepped]` vs. `[Smooth]`
- **`[Stepped]` (Solid Class Blocks):** Constructed as multi-part algorithmic ramps with zero intra-class gradient. Designed specifically for classified rasters (`Symbology -> Classified`), choropleth zones, and risk boundaries.
- **`[Smooth]` (Continuous Gradients):** Seamless mathematical transitions interpolated in perceptual color space. Designed for stretched raster surfaces (`Symbology -> Stretched`).

### Zero-Centered Diverging Symmetry
Diverging palettes feature rigorous mathematical symmetry centered around calibrated zero/neutral breakpoints:
- **11 Classes:** 5 negative/cool/dry + 1 neutral baseline (`#FFFFFF` or `#F7F7F7`) + 5 positive/warm/wet.
- **9 Classes:** 4 negative + 1 neutral + 4 positive.
- **7 Classes:** 3 negative + 1 neutral + 3 positive.
- **5 Classes:** 2 negative + 1 neutral + 2 positive.
- **3 Classes:** 1 negative + 1 neutral + 1 positive.
- **Even Tiers (4, 6, 8, 10 Classes):** Equidistant polar contrast for quartile, sextile, octile, and decile distributions.

---

## 📁 Repository Structure

```
NASA POWER Climate Atlas Generator/
├── POWER_Climate_Atlas_Generator_10_8.pyt     # Main ArcGIS Desktop 10.8 Python Toolbox
├── POWER_Climate_Atlas_Generator_10_8.pyt.xml # ArcToolbox item description metadata
├── raster_atlas_generator.py                  # Core backend engine (APIs, spatial processing)
├── LICENSE                                    # Open-source MIT License
├── README.md                                  # Repository documentation (English)
├── .gitignore                                 # Git rules for ArcGIS, Python, and OS files
│
├── docs/                                      # Comprehensive User & Technical Guides
│   ├── User_Guide_Arabic.md                   # Complete Arabic manual
│   ├── User_Guide_English.md                  # Complete English manual
│   ├── Fields_Reference_Table.md              # Climatological variable mapping & units
│   └── Interactive_Guide.html                 # Offline interactive web documentation
│
├── style/                                     # Cartographic Mega System (.style databases)
│   ├── NASA_POWER_Climate_Atlas_Master_Styles.xlsx  # Master Excel workbook with real color fills
│   ├── Climate_Styles_Sources_and_References.docx   # Master Word documentation with references
│   ├── Style_Guide_Arabic.md                  # Quick Arabic ArcMap style setup guide
│   ├── Style_Guide_English.md                 # Quick English ArcMap style setup guide
│   │
│   ├── All_ArcMap_Styles_Consolidated/        # Consolidated ArcMap Style Databases
│   │   ├── NASA_POWER_Climate_Atlas_Master.style    # Master unified style (2,250 ramps, 875 colors)
│   │   ├── 01_Temperature.style to 11_Climate_Models.style
│   │   ├── NASA_POWER_Climate_Atlas_Master_Styles.xlsx
│   │   └── Climate_Styles_Sources_and_References.docx
│   │
│   ├── 01_Temperature/ ... 11_Climate_Models/ # Individual element folders (style + README)
│   ├── Raw_Climate_Styles/                    # Reference palettes & raw source files
│   └── Source_of_Style_and_Color/             # Cartographic specifications & theory
│
├── utils/                                     # Utility modules and style generators
│   ├── __init__.py                            # Python package initialization
│   ├── calendar_dialog.py                     # Modal visual calendar GUI (Tkinter)
│   ├── build_mega_climate_styles.py           # Master 125-style compiler script
│   ├── build_true_arcmap_style_databases.py   # ArcObjects COM native .style generator
│   ├── generate_climate_styles.py             # Color palette mathematical definitions
│   ├── generate_master_styles_excel.py        # Openpyxl visual Excel workbook generator
│   ├── create_sources_word_document.py        # Python-docx master documentation generator
│   ├── fetch_egypt_stations.py                # Meteorological station network fetcher
│   └── verify_stations.py                     # Station data integrity checker
│
├── tests/                                     # Automated test suite for ArcGIS 10.8
│   ├── run_e2e_108.py                         # End-to-end integration test runner
│   ├── smoke_108_test.py                      # Smoke verification suite
│   ├── test_elements_108.py                   # Verification across all 11 climate elements
│   ├── test_excel_export_108.py               # Excel reporting verification
│   └── logs/                                  # Test run logs directory (.gitkeep)
│
└── Sample Data/                               # Sample datasets and case study files
    ├── Egypt Climate Data/                    # Study area boundary and sample GDB
    └── Egypt_Climate_Stations/                # 86 meteorological stations (GDB, SHP, Excel, CSV)
```

---

## 🚀 Getting Started

### Prerequisites
- **Esri ArcGIS Desktop 10.8** (or 10.1 - 10.8.2) with ArcMap.
- **Python 2.7** (installed automatically with ArcGIS Desktop under `C:\Python27\ArcGIS10.8`).
- **Spatial Analyst Extension** (recommended for raster surface interpolation).

### Installation in ArcMap Desktop
1. Clone or download this repository to your local machine:
   ```bash
   git clone https://github.com/ahmadibrahim4geo/NASA-POWER-Climate-Atlas-Generator.git
   ```
2. Open **ArcMap 10.8**.
3. Open the **ArcToolbox** window (`Geoprocessing` -> `ArcToolbox` or click the red toolbox icon).
4. Right-click anywhere in ArcToolbox and select **Add Toolbox...**.
5. Browse to the repository root directory and select **`POWER_Climate_Atlas_Generator_10_8.pyt`**.
6. The toolbox **NASA POWER Climate Atlas Generator** is now loaded and ready for use!

### Loading the Climate Styles into ArcMap
1. In ArcMap, navigate to **`Customize`** -> **`Style Manager...`**.
2. Click **`Styles...`** on the right side.
3. Click **`Add Style to List...`**.
4. Browse to:
   ```
   style/All_ArcMap_Styles_Consolidated/NASA_POWER_Climate_Atlas_Master.style
   ```
5. Click **Open** and then **OK**.
6. All 2,250 Color Ramps, 875 Colors, and 875 Fill Symbols are now globally available across ArcMap's Symbology dialogs!

---

## 📊 Scientific Verification & QA Testing

The system includes automated test suites verifying execution against ArcGIS 10.8 ArcPy:
```bash
# Run comprehensive smoke test
C:\Python27\ArcGIS10.8\python.exe tests/smoke_108_test.py

# Run all 11 climate element integration tests
C:\Python27\ArcGIS10.8\python.exe tests/test_elements_108.py

# Run Excel export validation
C:\Python27\ArcGIS10.8\python.exe tests/test_excel_export_108.py
```

---

## 📜 International Standards & References

The color scales and classifications within this atlas strictly adhere to physical and perceptual standards established by:
- **World Meteorological Organization (WMO):** WMO-No. 8 (CIMO Guide), WMO-No. 522 (Standard Normals), WMO-No. 168 (Hydrology).
- **Intergovernmental Panel on Climate Change (IPCC):** Sixth Assessment Report (AR6) Visual Style Guide & Colour Schemes.
- **NOAA National Centers for Environmental Information (NCEI) & Climate Prediction Center (CPC).**
- **ECMWF (European Centre for Medium-Range Weather Forecasts):** ERA5 Reanalysis visualization palettes.
- **Crameri Scientific Colour Maps:** Perceptually uniform, color-blind friendly scales (Batlow, Roma, Vik, Cork, Berlin).
- **ColorBrewer 2.0:** Standardized cartographic divergence algorithms by Cynthia Brewer.
- **World Health Organization (WHO):** Global Solar UV Index guidelines.

For exhaustive citations, equations, and hex tables, see [`style/Climate_Styles_Sources_and_References.docx`](file:///C:/Users/ahmad/Desktop/NASA%20POWER%20Climate%20Atlas%20Generator/style/Climate_Styles_Sources_and_References.docx).

---

## 📄 License

This project is licensed under the MIT License - see the [`LICENSE`](file:///C:/Users/ahmad/Desktop/NASA%20POWER%20Climate%20Atlas%20Generator/LICENSE) file for details.

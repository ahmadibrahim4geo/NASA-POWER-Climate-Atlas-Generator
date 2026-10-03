# 14. Field Name Evolution and Legacy Cross-Walk Mapping
## NASA POWER & Open-Meteo Climate Atlas Generator

---

## 1. Resolution of the Precipitation Nomenclature Evolution

In early developmental releases of the toolbox, precipitation field naming contained an ambiguity regarding annual vs. monthly aggregations. The following audit table details the exact historical evolution:

```
+----------------------------------------------------------------------------------------------------+
| PRECIPITATION FIELD EVOLUTION TIMELINE                                                             |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   1. LEGACY RELEASE (Pre-2026):                                                                    |
|      - 'R_Annual_Total' represented the multi-year mean of annual accumulations (~224 mm in Egypt) |
|      - 'R_Annual_Mean'  represented the monthly rate (annual accumulation / 12, ~18.7 mm in Egypt)|
|      - ISSUE: Users confusing 'R_Annual_Mean' with annual accumulation.                            |
|                                                                                                    |
|   2. CURRENT STANDARDIZED RELEASE (2026+ Standard):                                                |
|      - 'R_Annual_Mean' (SHP: 'R_AnnMean') = Climatological mean of annual accumulations (224 mm)   |
|      - 'R_Month_Mean'  (SHP: 'R_MonMean') = Mean monthly precipitation rate (224 / 12 = 18.67 mm)  |
|      - Fully synchronized across .pyt, .py, rasters, FGDB, shapefiles, Excel, and documentation.  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Comprehensive Legacy-to-Current Migration Cross-Walk

The script `migrate_legacy_database.py` allows existing user databases and raster folders to be migrated automatically:

| Legacy Schema Name | Current GDB & Raster Name | Current Shapefile DBF Name (10-char) | Arabic Label | Physical Meaning & Units | Migration Status |
|:---|:---|:---|:---|:---|:---:|
| `R_Annual_Total` | **`R_Annual_Mean`** | `R_AnnMean` | المتوسط السنوي لتساقط الأمطار | 30-year mean of annual accumulation (mm/year) | **Renamed & Standardized** |
| `R_Annual_Mean` | **`R_Month_Mean`** | `R_MonMean` | المتوسط الشهري لتساقط الأمطار | Monthly rate ($R_{Annual\_Mean} / 12$) (mm/month) | **Renamed & Standardized** |
| `R_Annual_Range` | `R_Annual_Range` | `R_AnnRng` | المدى السنوي لتساقط الأمطار | Max month minus Min month (mm) | Unchanged |
| `R_Season_Range` | `R_Season_Range` | `R_SeaRng` | المدى الفصلي لتساقط الأمطار | Max season minus Min season (mm) | Unchanged |
| `R_Winter_Total` | `R_Winter_Total` | `R_WinTot` | مجموع أمطار فصل الشتاء | DJF accumulated rainfall (mm) | Unchanged |
| `R_Spring_Total` | `R_Spring_Total` | `R_SprTot` | مجموع أمطار فصل الربيع | MAM accumulated rainfall (mm) | Unchanged |
| `R_Summer_Total` | `R_Summer_Total` | `R_SumTot` | مجموع أمطار فصل الصيف | JJA accumulated rainfall (mm) | Unchanged |
| `R_Autumn_Total` | `R_Autumn_Total` | `R_AutTot` | مجموع أمطار فصل الخريف | SON accumulated rainfall (mm) | Unchanged |
| `PET_Hargreaves` | `PET_Hargreaves_Annual` | `PET_HarAnn` | البخر-نتح المرجعي السنوي | Annual total Hargreaves PET (mm/year) | Clarified |
| `De_Martonne_Index`| `DM_Aridity_Annual` | `DM_AridAnn` | مؤشر دومارتون للجفاف | Annual De Martonne index ($P/(T+10)$) | Standardized |
| `UNEP_Index` | `UNEP_Aridity_Annual` | `UNEP_Arid` | مؤشر الجفاف الدولي (UNEP) | UNEP aridity ratio ($P / PET$) | Standardized |
| `Water_Deficit` | `Water_Deficit_Annual` | `WatDefAnn` | العجز المائي المناخي السنوي | Net water balance ($P - PET$) (mm/year) | Standardized |
| `Dry_Months` | `Dry_Months_Count` | `Dry_Months` | عدد الأشهر الجافة بيوكليماتياً | Months where $P < 2T$ (Count 0-12) | Clarified |

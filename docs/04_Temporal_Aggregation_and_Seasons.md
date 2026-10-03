# 04. Temporal Aggregation and Climatological Seasons
## NASA POWER & Open-Meteo Climate Atlas Generator

---

## 1. Climatological Seasons Definition

In atmospheric science and climatological analysis, standard calendar quarters do not align with physical thermal lags and radiative cycles. In accordance with the World Meteorological Organization (WMO) standards, the **Climate Atlas Generator** defines the four meteorological seasons based on whole calendar months:

| Season Name | Code | Component Months | Astronomical & Meteorological Rationale |
|:---|:---:|:---|:---|
| **Winter** | **DJF** | December, January, February | Period of lowest solar declination, minimum insolation, and peak mid-latitude cyclonic frontal incursions. |
| **Spring** | **MAM** | March, April, May | Vernal equinox transition, rapid continental surface heating, and desert depression genesis (e.g. Khamaseen). |
| **Summer** | **JJA** | June, July, August | Period of maximum solar elevation, highest insolation, and subtropical high-pressure / Indian monsoon low dominance. |
| **Autumn** | **SON** | September, October, November | Autumnal equinox transition, radiative cooling, and early-season atmospheric destabilization (e.g. Red Sea Trough). |

> **Southern Hemisphere Handling**: For study areas situated south of the equator ($	ext{Latitude} < 0$), the tool preserves meteorological month definitions while documenting that DJF corresponds to austral summer and JJA corresponds to austral winter.

---

## 2. Additive vs. Continuous / State Climate Variables

A fundamental scientific principle enforced across the platform is the rigorous distinction between **additive (flux/depth)** variables and **continuous (state/intensive)** atmospheric variables:

```
+--------------------------------------------------------------------------------------------------+
| CLIMATOLOGICAL VARIABLE TAXONOMY                                                                 |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   1. CONTINUOUS / STATE VARIABLES (Intensive Properties)                                         |
|      - Temperature (T, Tmax, Tmin), Pressure (PS, PSL), Humidity (RH), Dew Point (Td),           |
|        Cloud Cover (Cld), UV Index (UV), Daily Solar Insolation Rate (Sol_Mean).                 |
|      - Temporal Aggregation: Arithmetic Mean (or Circular Vector Mean for Wind Direction).       |
|      - Multi-Year Climatology: Mean of monthly means across 30 years.                            |
|                                                                                                  |
|   2. ADDITIVE / FLUX VARIABLES (Extensive Properties)                                            |
|      - Precipitation (R), Annual Solar Radiation Yield (Sol_Total), Evapotranspiration (ET).      |
|      - Temporal Aggregation: Time-integrated Accumulation (Sum over days/months).                |
|      - Multi-Year Climatology: Mean of annual totals across 30 years (or sum of 12 monthly totals)|
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

## 3. Dedicated Precipitation Aggregation Mathematics

### 3.1 The Physical Problem: Rate to Depth Integration
NASA POWER supplies precipitation as a flux rate: $PRECTOTCORR$ in units of $	ext{mm/day}$ (or $	ext{kg}/(	ext{m}^2\cdot	ext{s})$). Open-Meteo supplies daily or monthly accumulated depths in $	ext{mm}$.

To compute monthly precipitation depth $P_{y, m}$ for month $m$ of year $y$:
$$P_{y, m} = PRECTOTCORR_{y, m} 	imes N_{days, m}$$
where $N_{days, m}$ is the exact number of days in month $m$ (accounting for leap years in February: 29 days in 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020).

### 3.2 Annual Accumulation vs. Monthly Rate: Resolving Field Naming
In the Climate Atlas Generator schema, precipitation outputs are strictly standardized to eliminate historical confusion:

1. **Annual Mean Precipitation (`R_Annual_Mean`)**:
   - **Definition**: The 30-year climatological mean of total annual accumulated precipitation.
   - **Mathematical Formulation**:
     $$R_{Annual\_Mean} = rac{1}{N_{years}} \sum_{y=1}^{N_{years}} \left(\sum_{m=1}^{12} P_{y, m}ight) = \sum_{m=1}^{12} \overline{P}_m$$
   - **Units**: $	ext{mm/year}$.
   - **Physical Scale**: In northern Egypt (e.g. Alexandria / coastal Mediterranean), this value is approximately **$200 - 224	ext{ mm/year}$**. In Cairo it is **$pprox 25	ext{ mm/year}$**, and in Aswan it is **$< 5	ext{ mm/year}$**.
   - **Legacy Mapping**: In early prototype versions of the tool, this field was labeled `R_Annual_Total`. It was standardized to `R_Annual_Mean` because across a 30-year baseline, it represents the **climatological mean of annual accumulations**.

2. **Monthly Mean Precipitation (`R_Month_Mean`)**:
   - **Definition**: The annual mean precipitation distributed evenly across the 12 calendar months.
   - **Mathematical Formulation**:
     $$R_{Month\_Mean} = rac{R_{Annual\_Mean}}{12} = rac{1}{12} \sum_{m=1}^{12} \overline{P}_m$$
   - **Units**: $	ext{mm/month}$.
   - **Physical Scale**: In northern Egypt with $R_{Annual\_Mean} = 224.0	ext{ mm}$, $R_{Month\_Mean} = 224.0 / 12 = \mathbf{18.67	ext{ mm/month}}$.
   - **Legacy Mapping**: In early prototype versions, this field was labeled `R_Annual_Mean`. It was renamed to `R_Month_Mean` to reflect its true mathematical nature as a **monthly rate**.

3. **Seasonal Mean Precipitation (`R_WinMean`, `R_SprMean`, `R_SumMean`, `R_AutMean`)**:
   - Seasonal depth in millimeters per season ($	ext{mm/season}$):
     $$R_{Winter\_Mean} = rac{1}{N_{years}} \sum_{y=1}^{N_{years}} (P_{y,Dec} + P_{y,Jan} + P_{y,Feb}) = \overline{P}_{Dec} + \overline{P}_{Jan} + \overline{P}_{Feb}$$
     $$R_{Spring\_Mean} = rac{1}{N_{years}} \sum_{y=1}^{N_{years}} (P_{y,Mar} + P_{y,Apr} + P_{y,May}) = \overline{P}_{Mar} + \overline{P}_{Apr} + \overline{P}_{May}$$
     $$R_{Summer\_Mean} = rac{1}{N_{years}} \sum_{y=1}^{N_{years}} (P_{y,Jun} + P_{y,Jul} + P_{y,Aug}) = \overline{P}_{Jun} + \overline{P}_{Jul} + \overline{P}_{Aug}$$
     $$R_{Autumn\_Mean} = rac{1}{N_{years}} \sum_{y=1}^{N_{years}} (P_{y,Sep} + P_{y,Oct} + P_{y,Nov}) = \overline{P}_{Sep} + \overline{P}_{Oct} + \overline{P}_{Nov}$$
   - **Units**: $	ext{mm/season}$ ($	ext{مم/فصل}$).
   - **Calculation Concept**: Multi-year average of seasonal accumulated depth. Since it represents a climatological normal over $N_{years}$, the indicator is named `R_*_Mean`.
   - **Legacy Mapping**: Formerly named `R_Winter_Total` (`R_WinTot`), `R_Spring_Total` (`R_SprTot`), `R_Summer_Total` (`R_SumTot`), `R_Autumn_Total` (`R_AutTot`).
   - Note: In Mediterranean climates, $R_{Summer\_Mean} pprox 0	ext{ mm/season}$, while $R_{Winter\_Mean}$ represents 60–70% of the entire annual accumulation.

---

## 4. Circular Direction Vector Mathematics (Wind Direction)

A critical error in naive climate scripts is computing the arithmetic mean of angular wind directions (e.g. averaging $350^\circ$ and $10^\circ$ arithmetically yields $(350+10)/2 = 180^\circ$, which is due South—exactly opposite to the true prevailing Northerly wind of $0^\circ / 360^\circ$).

The Climate Atlas Generator avoids this via **Circular Trigonometric Vector Averaging** implemented in `circular_mean_deg` (line 663):

1. **Vector Decomposition**: Each directional observation $	heta_i \in [0^\circ, 360^\circ)$ is decomposed into Cartesian unit vector components:
   $$u_i = -\sin\left(rac{\pi \cdot 	heta_i}{180}ight), \quad v_i = -\cos\left(rac{\pi \cdot 	heta_i}{180}ight)$$
   *(Meteorological convention: $	heta$ represents the direction FROM which the wind blows).*

2. **Mean Component Accumulation**:
   $$\overline{u} = rac{1}{N} \sum_{i=1}^N u_i, \quad \overline{v} = rac{1}{N} \sum_{i=1}^N v_i$$

3. **Four-Quadrant Arctangent Reconstruction**:
   $$	heta_{rad} = 	ext{atan2}(-\overline{u}, -\overline{v})$$
   $$\overline{	heta}_{deg} = \left(rac{180}{\pi} \cdot 	heta_{rad}ight) \pmod{360^\circ}$$

This guarantees mathematically rigorous prevailing wind directions across annual and seasonal cycles.

---

## 5. Climatological Monthly Indicators (12 Months per Element)

In addition to annual and seasonal integrations, the platform computes and stores the 30-year climatological monthly profiles for all 12 calendar months (January through December) across 11 key biophysical elements (144 total monthly indicators):

### 5.1 Monthly Formulation by Physical Property
1. **Continuous Atmospheric State Variables (Mean of Monthly Values)**:
   - For Temperature ($T$), Sea Level Pressure ($PSL$), Surface Pressure ($PS$), Wind Speed ($W_{Spd}$), Relative Humidity ($RH$), Dew Point ($T_d$), Daily Solar Insolation ($Sol$), UV Index ($UV$), and Cloud Cover ($Cld$):
     $$\overline{X}_m = \frac{1}{N_{years}} \sum_{y=1}^{N_{years}} X_{y, m}, \quad m \in \{1, 2, \dots, 12\}$$
2. **Precipitation Accumulated Monthly Normal ($mm/month$)**:
   - Multi-year mean of monthly accumulated precipitation totals:
     $$\overline{R}_m = \frac{1}{N_{years}} \sum_{y=1}^{N_{years}} P_{y, m}, \quad m \in \{1, 2, \dots, 12\}$$
3. **Circular Vector Mean Wind Direction ($^{\circ}$)**:
   - Evaluated for each individual month using four-quadrant circular decomposition:
     $$\overline{\theta}_m = \text{atan2}\left(\frac{1}{N}\sum \sin \theta_{y,m}, \frac{1}{N}\sum \cos \theta_{y,m}\right) \pmod{360^{\circ}}$$
4. **Monthly Evapotranspiration Accumulation ($mm/month$)**:
   - Monthly Hargreaves-Samani potential evapotranspiration depth according to FAO-56 standard:
     $$\overline{ET}_m = \frac{1}{N_{years}} \sum_{y=1}^{N_{years}} ET_{y, m}, \quad m \in \{1, 2, \dots, 12\}$$

### 5.2 Climatological Overall Monthly Mean (`*_Month_Mean`)
To represent the typical climatological monthly baseline for each atmospheric variable across the full 12 calendar months:
1. **Precipitation Monthly Depth (`R_Month_Mean`)**:
   - Evaluated as the multi-year annual depth divided by 12:
     $$R_{Month\_Mean} = \frac{R_{Annual\_Mean}}{12} \quad (\text{mm/month})$$
2. **Atmospheric State Variables & Rates (`T_Month_Mean`, `PSL_Month_Mean`, etc.)**:
   - For continuous state variables (Temperature, Sea Level Pressure, Surface Pressure, Wind Speed, Relative Humidity, Dew Point, Solar Radiation daily flux, UV Index, Cloud Cover, and Evapotranspiration daily rate):
     $$\overline{X}_{Month\_Mean} = \frac{1}{12}\sum_{m=1}^{12} \overline{X}_m = X_{Annual\_Mean}$$
     *(Note: Dividing temperature or pressure by 12 would violate physical units and dimensions; the climatological monthly mean represents the mean level across all months).*
3. **Circular Vector Wind Direction (`W_Dir_Month_Mean`)**:
   - Evaluated via circular mean over the 12 monthly vector angles:
     $$W\_Dir_{Month\_Mean} = \text{atan2}\left(\frac{1}{12}\sum_{m=1}^{12} \sin \overline{\theta}_m, \frac{1}{12}\sum_{m=1}^{12} \cos \overline{\theta}_m\right) \pmod{360^{\circ}}$$

### 5.3 Structured Dual-Sheet Excel Architecture
All individual element Excel workbooks (`00_Tables_And_Reports\*.xls`) are structured with two synchronized sheets:
- **Sheet 1 (`Data`)**: Contains station coordinates, metadata, annual indicators, overall monthly mean (`*_Month_Mean`), and seasonal indicators (DJF, MAM, JJA, SON).
- **Sheet 2 (`Month`)**: Contains station coordinates, metadata, and all 12 individual climatological monthly indicators (Jan–Dec).
- **Persistent Local Raw Archive**: Complete 30-year monthly time-series JSON records are archived in `Egypt_Monthly_Raw_1996_2025.json` (~54 MB) to permit instant offline re-aggregations without network latency.
- **Cartographic Surface Generation Policy**: Surface raster interpolations are maintained for annual, seasonal, and overall monthly mean (`*_Month_Mean`) horizons across all 18 folders (114 rasters total). Individual month-by-month raster generation can optionally be toggled for fine-scale analysis into dedicated `Month` subfolders.

### 5.4 Monthly Gating Rule (≥ 2 Years)
Twelve-month climatologies are meaningful only over multi-year spans. The **Generate Monthly Climatology Rasters (Jan–Dec)** option (`GPBoolean`, default OFF) takes effect only when the selected period covers **2 years or more**; shorter spans keep the flag inert with a logged warning, while annual/seasonal/`*_Month_Mean` outputs are always produced.

---

## 6. Seasonal Range (`*_Seasonal_Range`) — All Elements
Like the annual range and annual mean, every mean-type element carries a seasonal range: the warmest (highest) seasonal mean minus the coldest (lowest) seasonal mean over Winter/Spring/Summer/Autumn:
$$X_{Seasonal\_Range} = \max(X_{Winter}, X_{Spring}, X_{Summer}, X_{Autumn}) - \min(X_{Winter}, X_{Spring}, X_{Summer}, X_{Autumn})$$
Covered fields: `T_Seasonal_Range`, `R_Seasonal_Range` (seasonal totals), `PSL_Seasonal_Range`, `PS_Seasonal_Range`, `W_Spd_Seasonal_Range`, `RH_Seasonal_Range`, `Td_Seasonal_Range`, `Sol_Seasonal_Range`, `UV_Seasonal_Range`, `Cld_Seasonal_Range`, `ET_Seasonal_Range`. Each is stored in the GDB, shapefiles, Excel, dictionaries and interpolated as a clipped raster with the user's selected method — exactly like the annual indicators. Threshold-type derived indices (Heat Index, Wind Chill, aridity/drought annual indices) intentionally carry annual ranges only.


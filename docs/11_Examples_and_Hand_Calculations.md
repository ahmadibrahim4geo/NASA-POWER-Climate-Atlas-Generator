# 11. Worked Numerical Examples and Hand Calculations
## NASA POWER & Open-Meteo Climate Atlas Generator

---

## 1. Example 1: 30-Year Precipitation Aggregation (Cairo Grid Cell)

### 1.1 Objective
Verify the calculation of `R_Annual_Mean`, `R_Month_Mean`, `R_Annual_Range`, `R_Season_Range`, and Seasonal Totals from monthly climatological values.

### 1.2 Input Climatological Monthly Totals (mm)
Assume a 30-year climatological normal (1991–2020) for a grid cell in the Cairo metropolitan region:
- January ($\overline{P}_1$): $5.2	ext{ mm}$
- February ($\overline{P}_2$): $4.8	ext{ mm}$
- March ($\overline{P}_3$): $3.5	ext{ mm}$
- April ($\overline{P}_4$): $1.2	ext{ mm}$
- May ($\overline{P}_5$): $0.5	ext{ mm}$
- June ($\overline{P}_6$): $0.0	ext{ mm}$
- July ($\overline{P}_7$): $0.0	ext{ mm}$
- August ($\overline{P}_8$): $0.0	ext{ mm}$
- September ($\overline{P}_9$): $0.1	ext{ mm}$
- October ($\overline{P}_{10}$): $1.4	ext{ mm}$
- November ($\overline{P}_{11}$): $3.8	ext{ mm}$
- December ($\overline{P}_{12}$): $5.9	ext{ mm}$

### 1.3 Step-by-Step Calculation
1. **Annual Mean Accumulated Precipitation (`R_Annual_Mean`)**:
   $$R_{Annual\_Mean} = \sum_{m=1}^{12} \overline{P}_m = 5.2 + 4.8 + 3.5 + 1.2 + 0.5 + 0.0 + 0.0 + 0.0 + 0.1 + 1.4 + 3.8 + 5.9 = \mathbf{26.40	ext{ mm/year}}$$
2. **Monthly Mean Precipitation (`R_Month_Mean`)**:
   $$R_{Month\_Mean} = rac{R_{Annual\_Mean}}{12} = rac{26.40}{12} = \mathbf{2.20	ext{ mm/month}}$$
3. **Seasonal Means**:
   - **Winter (`R_WinMean`)**: $\overline{P}_{12} + \overline{P}_1 + \overline{P}_2 = 5.9 + 5.2 + 4.8 = \mathbf{15.90	ext{ mm/season}}$
   - **Spring (`R_SprMean`)**: $\overline{P}_3 + \overline{P}_4 + \overline{P}_5 = 3.5 + 1.2 + 0.5 = \mathbf{5.20	ext{ mm/season}}$
   - **Summer (`R_SumMean`)**: $\overline{P}_6 + \overline{P}_7 + \overline{P}_8 = 0.0 + 0.0 + 0.0 = \mathbf{0.00	ext{ mm/season}}$
   - **Autumn (`R_AutMean`)**: $\overline{P}_9 + \overline{P}_{10} + \overline{P}_{11} = 0.1 + 1.4 + 3.8 = \mathbf{5.30	ext{ mm/season}}$
4. **Ranges**:
   - **Annual Monthly Range (`R_AnnRng`)**: $\max(\overline{P}_m) - \min(\overline{P}_m) = 5.9 - 0.0 = \mathbf{5.90	ext{ mm/month}}$
   - **Seasonal Range (`R_SeaRng`)**: $\max(R_{season}) - \min(R_{season}) = 15.90 - 0.00 = \mathbf{15.90	ext{ mm/season}}$

---

## 2. Example 2: Circular Mean Wind Direction (Sinai Grid Cell)

### 2.1 Objective
Verify that averaging wind angles crossing the North meridian ($0^\circ / 360^\circ$) produces the correct prevailing direction rather than an erroneous arithmetic average.

### 2.2 Input Monthly Prevailing Angles (Degrees)
Consider 4 winter months with north-northwesterly and north-northeasterly winds:
- Month 1: $340^\circ$ (NNW)
- Month 2: $355^\circ$ (NNW)
- Month 3: $5^\circ$ (NNE)
- Month 4: $20^\circ$ (NNE)

### 2.3 Step-by-Step Calculation
1. **Decompose Angles into Unit Cartesian Components**:
   - $	heta_1 = 340^\circ$: $\sin(340^\circ) = -0.3420$, $\cos(340^\circ) = 0.9397$
   - $	heta_2 = 355^\circ$: $\sin(355^\circ) = -0.0872$, $\cos(355^\circ) = 0.9962$
   - $	heta_3 = 5^\circ$: $\sin(5^\circ) = +0.0872$, $\cos(5^\circ) = 0.9962$
   - $	heta_4 = 20^\circ$: $\sin(20^\circ) = +0.3420$, $\cos(20^\circ) = 0.9397$
2. **Sum Components**:
   - $S_{\sin} = -0.3420 - 0.0872 + 0.0872 + 0.3420 = \mathbf{0.0000}$
   - $S_{\cos} = 0.9397 + 0.9962 + 0.9962 + 0.9397 = \mathbf{3.8718}$
3. **Compute 4-Quadrant Arctangent**:
   $$\overline{	heta} = 	ext{atan2}(S_{\sin}, S_{\cos}) = 	ext{atan2}(0.0000, 3.8718) = 0.0	ext{ rad} = \mathbf{0.0^\circ 	ext{ (Due North)}}$$
   *(Note: Naive arithmetic averaging would yield $(340 + 355 + 5 + 20) / 4 = 720 / 4 = 180.0^\circ$ (Due South), a catastrophic 180° inversion).*

---

## 3. Example 3: Biometeorological Heat Index and Shade WBGT

### 3.1 Objective
Calculate the Rothfusz Heat Index and ISO 7243 shade WBGT for a peak summer afternoon.

### 3.2 Inputs
- Ambient 2m Air Temperature: $T = 36.0^\circ	ext{C}$
- Relative Humidity: $RH = 55.0\%$

### 3.3 Heat Index Calculation
1. Convert $T$ to Fahrenheit: $T_f = 36.0 	imes 1.8 + 32 = 96.8^\circ	ext{F}$.
2. Because $T_f \ge 80^\circ	ext{F}$, evaluate Rothfusz polynomial:
   $$HI_f = -42.379 + 2.04901523(96.8) + 10.14333127(55) - 0.22475541(96.8)(55) - 6.83783 	imes 10^{-3}(96.8)^2 - 5.481717 	imes 10^{-2}(55)^2 + 1.22874 	imes 10^{-3}(96.8)^2(55) + 8.5282 	imes 10^{-4}(96.8)(55)^2 - 1.99 	imes 10^{-6}(96.8)^2(55)^2$$
   $$HI_f pprox 124.6^\circ	ext{F}$$
3. Convert back to Celsius:
   $$HI_c = rac{124.6 - 32}{1.8} = \mathbf{51.4^\circ	ext{C}}$$
   *(NOAA Category: "Danger" - Heat cramps or heat stroke highly likely with continued exposure).*

### 3.4 Shade WBGT Calculation
1. Natural Wet-Bulb Temperature ($T_w$) via Stull (2011) formula at $T=36^\circ	ext{C}, RH=55\%$:
   $$T_w pprox 28.2^\circ	ext{C}$$
2. ISO 7243 Shade WBGT:
   $$WBGT_{shade} = 0.7 	imes T_w + 0.3 	imes T_a = 0.7(28.2) + 0.3(36.0) = 19.74 + 10.80 = \mathbf{30.54^\circ	ext{C}}$$
   *(Work/Rest Recommendation: 25% work / 75% rest per hour under heavy physical labor).*

---

## 4. Example 4: Agroclimatic Water Balance (Hargreaves, UNEP, Deficit)

### 4.1 Inputs (Aswan Station Normal)
- Annual Mean Precipitation: $R_{Annual\_Mean} = 1.5	ext{ mm/year}$
- Annual Hargreaves PET: $PET_{Hargreaves\_Annual} = 2,450.0	ext{ mm/year}$
- Annual Mean Air Temperature: $T_{Annual\_Mean} = 26.5^\circ	ext{C}$

### 4.2 Step-by-Step Calculation
1. **De Martonne Aridity Index (`DM_AridAnn`)**:
   $$I_{DM} = rac{P}{T + 10} = rac{1.5}{26.5 + 10} = rac{1.5}{36.5} = \mathbf{0.041}$$
   *(Class: Hyper-arid, $I_{DM} < 5$).*
2. **UNEP Aridity Index (`UNEP_Arid`)**:
   $$AI_{UNEP} = rac{P}{PET} = rac{1.5}{2450.0} = \mathbf{0.00061}$$
   *(Class: Hyper-arid, $AI < 0.05$).*
3. **Climatic Water Deficit (`WatDefAnn`)**:
   $$CWD = P - PET = 1.5 - 2450.0 = \mathbf{-2,448.5	ext{ mm/year}}$$
   *(Severe net annual atmospheric moisture deficit).*

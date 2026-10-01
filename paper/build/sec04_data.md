# Data

## FAO-derived country-level file

The first source is the file `yield_df.csv` from a public Kaggle dataset that combines yield and pesticide data from FAOSTAT with rainfall and temperature series from the World Bank data portal [@patel; @faostat]. The dataset page describes its provenance; we verified the structure described below directly against the four component tables distributed with it (`yield.csv`, `pesticides.csv`, `rainfall.csv`, `temp.csv`). The file has 28,242 rows covering 101 countries, 10 crops and the years 1990–2013. Each row holds the country, crop, year, yield in hg/ha, average annual rainfall (mm), pesticide use (tonnes) and average temperature (°C). We model the logarithm of yield. We call a **record** a distinct country–crop–year combination.

## Indian district-level table

The second source is a district-level table of area and production by crop and season in India for 1997–2015 [@abhinand]. It has 246,091 rows, 33 states, 652 districts and 124 crops, and no weather variables. We removed rows with missing production or non-positive area or production, computed yield as production divided by area, dropped crops with fewer than 20 rows, and trimmed the extreme 0.1% in each tail of log-yield. The cleaned table has 238,191 rows, 90 crops, 33 states and 652 districts. The exact cleaning rule of earlier analyses may differ; the rule above is the one used for every result reported here. We did not verify the original publication source of this table beyond the dataset page, and treat it as a convenient public benchmark.

## Groups and features

For the FAO file the group is the country. For the Indian table we use two levels, the district and the state, which gives a gradient of group identifiability. Features are deliberately limited to those the files contain, so that the experiments isolate the effect of the evaluation protocol. For FAO we use crop (one-hot), year, rainfall, pesticide use and temperature. For India we use crop and season (one-hot), year and log cultivated area. One model variant adds the group identifier as a categorical feature to quantify what a model gains from recognising the place. Table 3 summarises the datasets.

Table: Table 3. Datasets and group structure. ICC is the one-way intraclass correlation of log-yield (ANOVA estimator, unbalanced design) [@shrout1979], by country and crop for FAO and by state and crop / district and crop for India.

| Dataset | Rows | Groups | Crops | Years | ICC |
|:---|---:|:---|---:|:---|:---|
| FAO file, raw rows | 28,242 | 101 countries | 10 | 1990–2013 | 0.95 |
| FAO file, distinct records | 13,130 | 101 countries | 10 | 1990–2013 | 0.94 |
| India, cleaned | 238,191 | 33 states; 652 districts | 90 | 1997–2015 | 0.88 / 0.90 |

## Audit procedure

We rebuilt `yield_df.csv` from its component tables to trace the repeated rows. For each record we counted the rows in the temperature table for the same country and year and compared the count with the number of rows in `yield_df.csv` for that record. We measured the within-country-year spread of temperature in the source, checked whether yield values agree with the FAO yield table, and computed intraclass correlations of the covariates by country on the raw rows, on the distinct records and, for pesticides, in the source table. The audit code is `src/c01_audit.py` and `src/c06_audit_origin.py`.

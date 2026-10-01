Table: Table 4. Audit of the FAO-derived file `yield_df.csv`, traced to its component tables.

| Quantity | Value |
|:---|:---|
| Rows in `yield_df.csv` | 28,242 |
| Distinct country–crop–year records | 13,130 |
| Rows that repeat an earlier record | 15,112 (53.5%) |
| Rows belonging to a repeated record | 67.1% |
| Records with more than one row | 3,837 |
| Distinct yields within a record (maximum) | 1 |
| Records whose row count equals the rows in `temp.csv` for the country-year | 100% |
| Country-years in `temp.csv` with several rows | 28% |
| Median within-country-year SD of temperature, against overall SD (°C) | 2.19 against 7.59 |
| Countries whose source rainfall is constant over years | 98% of 192 |
| Yield equals the FAO yield table (distinct records) | 100% |
| ICC by country: rainfall / temperature / pesticides (distinct records) | 1.00 / 0.995 / 0.78 |
| ICC by country: temperature / pesticides (raw rows) | 0.92 / 0.71 |
| ICC of pesticides by country in the source table | 0.94 |

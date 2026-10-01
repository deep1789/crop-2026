::: {custom-style="Title"}
Duplicated records and region shift in crop-yield benchmarks: an audit, a transfer study and calibrated uncertainty for unseen countries and districts
:::

::: {custom-style="Author"}
[Author names to be added]
:::

::: {custom-style="Affiliation"}
[Affiliations and corresponding author to be added]
:::

::: {custom-style="Heading Unnumbered"}
Highlights
:::

- 53% of rows in a public FAO-derived yield file are join fan-out duplicates
- Random splits reward memorising the country; held-out countries fall to R² 0.66
- Naive conformal intervals cover 60% instead of 90% on unseen countries
- Collapse follows how well features identify the group; ridge regression resists it
- Group-aware calibration restores nominal coverage; a learned scale helps weak groups

::: {custom-style="Heading Unnumbered"}
Abstract
:::

Public crop-yield tables are routinely used to train and compare machine-learning models, usually with random train–test splits and with prediction intervals calibrated on random hold-out rows. We audit two such sources, a publicly shared FAO-derived country-level file (28,242 rows, 101 countries, 10 crops, 1990–2013) and an Indian district-level production table (246,091 rows, 33 states, 652 districts, 1997–2015), and study what these evaluation habits hide. The FAO file contains only 13,130 distinct country–crop–year records: the rest are copies produced when yield records were joined to a temperature table that has several rows per country and year, so every record is multiplied by that row count (match in 100% of records), and 67% of all rows belong to a repeated record. Rainfall is constant within a country and temperature and pesticide use are nearly country labels (intraclass correlations 1.00, 0.995 and 0.78 on distinct records). Random splits therefore reward recognising the country: tuned gradient boosting reaches R² = 0.93 on random rows but 0.66 on held-out countries, while a crop-mean predictor scores 0.58 and 0.57; with Indian states held out, no model is distinguishable from the crop mean. For split conformal prediction at a nominal 90%, calibration on random rows gives 60% coverage on unseen countries (84% for states and 90% for districts), and group-aware calibration restores 90% in all three settings. The collapse follows the strength of the group fingerprint in the features: it is severe for random forest (47%), strong for gradient boosting (59%) and absent for ridge regression (88%) on the same data. A coverage-collapse relation, coverage ≈ 2Φ(z/ρ) − 1 with ρ the ratio of test to calibration residual scale, tracks a simulation to within 0.013 (cell means) and links the problem to the inflation ratio of group leakage. A learned residual-scale model flags difficult groups (Spearman 0.32 to 0.61 with group error, against 0.12 to 0.39 for a distance score) and modestly lifts coverage in the weakest groups at the cost of wider intervals, while five labelled local rows narrow FAO intervals by 12%. We provide an audit procedure, a protocol and open code.

::: {custom-style="Keywords"}
**Keywords:** crop yield prediction; data leakage; duplicate records; conformal prediction; distribution shift; grouped validation; FAOSTAT; uncertainty quantification
:::

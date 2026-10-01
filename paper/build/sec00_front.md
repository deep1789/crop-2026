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

- 53% of rows in a public FAO-derived yield file are join fan-out copies, traced exactly
- A country–crop lookup matches tuned boosting on random splits; held-out countries fall to R² 0.66
- Naive conformal intervals cover 60% (50% on raw rows) instead of 90% on unseen countries
- Collapse follows the group fingerprint: random forest 47%, boosting 59%, ridge 88%
- Group-aware calibration restores 90%; a learned scale helps weak groups modestly

::: {custom-style="Heading Unnumbered"}
Abstract
:::

Public crop-yield tables are routinely used to train and compare machine-learning models, usually with random train–test splits and with prediction intervals calibrated on random hold-out rows. We audit two public sources, a country-level file derived from FAOSTAT and other tables (28,242 rows, 101 countries, 10 crops, 1990–2013) and an Indian district-level production table (246,091 rows, 33 states, 652 districts, 1997–2015), and study what these habits hide. The FAO file holds 13,130 distinct country–crop–year records; the other rows are copies created when yield records were joined to a temperature table with several rows per country and year (the row count of every record equals its join multiplicity). Public code repositories have noted this duplication informally; we trace and quantify it. Rainfall is constant within a country, and temperature and pesticide use are nearly country labels (intraclass correlations 1.00, 0.995 and 0.78). Random splits therefore reward recognising the country: tuned gradient boosting reaches R² = 0.93 on random rows and 0.66 on held-out countries, a crop-mean predictor scores 0.58 and 0.57, and a country–crop lookup with no covariates already reaches 0.93 on random rows and 0.89 forward in time (tuned boosting 0.91). Within-country anomalies of temperature and pesticide use add real within-country skill (RMSE 9–11% below the lookup) but no cross-country skill. For split conformal prediction at a nominal 90%, calibration on random rows gives 60% coverage on unseen FAO countries (50% on the raw duplicated rows), 84% on unseen Indian states and 90% on districts, and group-aware calibration restores 90% in all settings. The collapse follows the group fingerprint in the features: random forest 47%, gradient boosting 59% and ridge regression 88% on the same data, and 83% when fingerprint-free features are used. A relation, coverage ≈ 2Φ(z/ρ) − 1 with ρ the ratio of test to calibration residual scale, tracks a simulation to within 0.013 (cell means) and links the problem to the inflation ratio of group leakage. Weighted conformal prediction cannot help, because calibration and test rows are perfectly separable (AUC 1.0). A learned residual-scale model flags difficult groups (group-level Spearman 0.48 to 0.61, against 0.11 to 0.39 for a distance score; clearly better only for districts) and modestly lifts coverage in the weakest groups at the cost of wider intervals, while five labelled local rows narrow FAO intervals by 12%. We provide an audit procedure, a protocol and open code.

::: {custom-style="Keywords"}
**Keywords:** crop yield prediction; data leakage; duplicate records; conformal prediction; distribution shift; grouped validation; FAOSTAT; uncertainty quantification
:::

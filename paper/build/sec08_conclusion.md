# Conclusions

A publicly shared FAO-derived crop-yield file contains 13,130 distinct country–crop–year records in 28,242 rows, the excess arising from a join to a temperature table with several rows per country and year, its covariates are nearly country identifiers and a country–crop lookup with no covariates already reaches R² = 0.93 on random rows. Random splits on this file, and on a district-level Indian table with the same hierarchical structure, measure how well a model recognises the place: tuned gradient boosting scores R² = 0.93 on random rows and 0.66 on unseen countries, a crop-mean predictor scores 0.57, and a model given the country as a feature is no better than the crop mean on unseen countries. Prediction intervals calibrated on random rows inherit the problem: they cover 60% of rows from unseen countries at a nominal 90%, 84% for unseen Indian states and 90% for districts, and the loss follows how well the features identify the group and the flexibility of the model, with random forest at 47%, gradient boosting at 59% and ridge regression at 88% on the same data. Within-country anomaly features add real skill within a country (RMSE 9–11% below the lookup) but none across countries, and they weaken the collapse (naive coverage 83%) without removing it. A simple relation between coverage and the inflation ratio of group leakage describes this loss, and calibrating on held-out groups restores nominal marginal coverage in every setting. A learned residual scale flags harder groups and modestly improves coverage in the weakest tail, and a few labelled local rows sharpen intervals on the FAO file, but group-level under-coverage remains for a sizeable share of groups.

We recommend that users of crop-yield tables audit record keys, split on the unit of intended generalisation, report a no-skill baseline and group-level coverage, and calibrate intervals on held-out groups. The code, per-fold results and figures accompanying this paper make it straightforward to apply the same audit to other tables.

# Declarations

**CRediT authorship contribution statement.** *To be completed by the authors.* (Conceptualisation; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing – original draft; Writing – review and editing; Visualisation.)

**Declaration of generative AI and AI-assisted technologies in the writing process.** During the preparation of this work the author(s) used Claude (Anthropic) to assist with writing and running the analysis code, with generating figures and tables, with drafting and editing the manuscript text, and with searching for and checking bibliographic details. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

**Declaration of competing interest.** *To be completed by the authors.*

**Funding.** *To be completed by the authors.*

**Data availability.** The datasets are public (Kaggle: Crop Yield Prediction Dataset, built from FAOSTAT and World Bank tables; Kaggle: Crop Production in India). The exact files, all code, per-fold results and figures are available at https://github.com/deep1789/crop-2026.

**Acknowledgements.** *To be completed by the authors.*

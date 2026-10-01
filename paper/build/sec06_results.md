# Results

## Audit of the FAO-derived file

Table 4 summarises the audit. Of the 28,242 rows, 15,112 (53.5%) repeat an earlier country–crop–year record and 67.1% of all rows belong to a record that occurs more than once, so a model scored on random rows is scored mostly on records it has seen under another row. Every repeated record carries one distinct yield, and the yield agrees with the FAO yield table for all 13,130 records, so the repeats are copies and not conflicting measurements. What differs between copies is the temperature, which has on average 4.3 distinct values within a repeated record.

{{tab_audit}}

The cause is a join fan-out. The temperature table has several rows for 28% of country-years, whose within-country-year standard deviation (median 2.2 °C) is a sizeable fraction of the overall spread (7.6 °C). Joining yield records to it on country and year multiplies each record by the number of temperature rows, and this number equals the number of rows of the record in `yield_df.csv` for all 13,130 records (Fig. 1a and 1b). The largest multiplicity is 22 rows, so the duplication is uneven across countries: a country with many temperature rows contributes many times more rows to any pooled evaluation than a country with one. Fig. 1c shows that the covariates are close to country identifiers: rainfall is constant within a country (intraclass correlation 1.00 and constant over years in the source for 98% of countries), temperature has an intraclass correlation of 0.995 on distinct records, and pesticide use 0.78 (0.935 in the source table, which spans more countries, and 0.71 on the raw rows). Log-yield has an intraclass correlation of 0.94 by country and crop. A learner that sees these three numbers has a very good hint about which country a row belongs to, which is the condition for memorisation in Section 3.

![Fig. 1. Audit of the FAO-derived file. (a) Number of rows per country–crop–year record (log scale). (b) Rows per record in `yield_df.csv` against rows in `temp.csv` for the same country-year; all records lie on the identity line. (c) Intraclass correlation by country of the covariates (distinct records) and of log-yield.](../figures/fig02_audit.png){width=6.4in}

The Indian table has no repeated state–district–year–season–crop keys, but its structure is also hierarchical (intraclass correlation of log-yield 0.88 by state and crop, 0.90 by district and crop). Its features carry little group information: log area has an intraclass correlation of 0.07 by state and 0.10 by district.

## Transfer: what random splits reward

Tables 5 and 6 and Fig. 2 give R² by protocol. On the FAO file, random splits rank the flexible models first (random forest 0.952, tuned gradient boosting 0.931, with group identifier 0.946) and far above the crop mean (0.580) and ridge regression (0.651). With whole countries held out all of that disappears: tuned gradient boosting scores 0.656, ridge 0.615, random forest 0.600, the crop mean 0.566, and the model that is given the country as a feature drops to 0.551, no better than the crop mean (the intervals overlap). The root-mean-square error of random forest rises from 0.247 to 0.709 (a factor of 2.9) and that of tuned gradient boosting from 0.297 to 0.657 (2.2), while ridge regression moves from 0.666 to 0.696 (1.05). Forward-in-time evaluation resembles the random split (random forest 0.924), because countries remain in training: it measures extrapolation in time within known countries, not transfer to new ones.

{{tab_transfer}}

![Fig. 2. R² (95% bootstrap interval) by protocol and model. (a) FAO file, distinct records. (b) Indian district table. Models that exploit group identity (random forest, GBM with group ID) lead under random and forward-in-time protocols on FAO and fall to or below the crop-mean baseline when groups are held out.](../figures/fig03_transfer.png){width=6.4in}

The Indian table shows the same pattern with a smaller gap, as expected from weaker fingerprints. Random-split R² is 0.778 for default gradient boosting and 0.833 when the district is given as a feature, against 0.734 for the crop mean; with districts held out the values are 0.758 (tuned gradient boosting) and 0.732 (with district ID), against 0.732 for the crop mean. With whole states held out, performance falls below the crop-mean level for the flexible models (R² 0.662 for tuned gradient boosting and 0.598 for random forest against 0.675), and none of the models is distinguishable from the crop mean given the intervals (ridge 0.683).

Two cautions apply to the apparent benefit of cleaning. In the earlier runs with default models, random forest on the raw FAO rows reaches R² = 0.976 against 0.953 on the distinct records, so duplicates inflate the random-split score further; with countries held out the raw rows give a slightly *higher* score than the distinct records (gradient boosting 0.683 against 0.636), which we suspect is because the countries with the most temperature rows are over-weighted in the raw test folds (we did not test this explanation). The direction of the duplicate effect therefore depends on the protocol, and a reported score on the raw file cannot be interpreted without knowing which rows are weighted.

## Coverage collapse on unseen groups

Table 7 and Fig. 3 give the conformal results at a nominal 90%. When intervals are calibrated on random rows, FAO coverage on unseen countries is 0.598 (95% interval 0.578–0.619) and 83% of test countries are more than 10 points below nominal; the 10th-percentile country has coverage 0.36. For Indian states naive coverage is 0.839 and for districts 0.897. Group calibration restores coverage to 0.895, 0.892 and 0.899 respectively, at the price of wider intervals where the collapse was severe (width 2.17 against 0.96 on FAO and 2.31 against 1.90 for states) and with no cost for districts (1.95 against 1.94). The pattern holds at the other levels (Table 8): at nominal 95% and 80% the FAO naive coverage is 0.724 and 0.448, against 0.946 and 0.799 for group calibration.

{{tab_conformal}}

{{tab_alpha}}

Equation (5) explains the size of the loss. The observed naive coverage implies inflation ratios $\rho$ of 1.96 (FAO), 1.17 (states) and 1.01 (districts), and hence lower bounds on the residual group share of $r\ge 0.74$, $0.27$ and $0.02$. The relation tracks the simulation closely (Fig. 3a): across the 28 simulation cells the mean actual coverage differs from Eq. (5) by at most 0.013 (by at most 0.071 for single replicates). On the FAO folds the relation is slightly pessimistic: for naive calibration the predicted coverage is 0.56 against 0.60 observed, a mean absolute error of 0.04 across folds with correlation 0.94 between predicted and observed fold coverage, which we attribute to heavier-than-Gaussian residual tails. For the Indian districts the predicted and observed values agree (0.892 and 0.897).

Table 13 gives the simulation behind Fig. 3a. With no group effect ($\tau=0$) naive and group calibration both cover about 0.90, and as $\tau$ grows naive coverage falls along Eq. (5), from 0.89 at $\tau=0.5$ to 0.42 at $\tau=3$, while group calibration stays between 0.89 and 0.90. Because the simulated residuals are Gaussian by construction, this agreement checks the algebra and the calibration logic, not the Gaussian assumption; the FAO folds, where the residuals are not Gaussian, are the real test and show the modest pessimism noted above.

{{tab_sim}}

![Fig. 3. Coverage collapse. (a) Actual coverage against the inflation ratio $\rho$: the curve is Eq. (5), dots are simulation cells with naive calibration, diamonds are the implied $\rho$ of the three data settings. (b) Naive coverage of three model families (nominal 0.90, dotted). (c) Naive coverage of gradient boosting against the accuracy with which the group can be identified from the features.](../figures/fig04_collapse.png){width=6.4in}

## Collapse follows the group fingerprint

Table 9 and Fig. 3b and 3c relate the collapse to the group fingerprint. The features identify the country in 60% of held-out FAO rows (chance 1.8%), the state in 31% of Indian rows (chance 14%) and the district in 1.9% (chance 0.4%), with mean feature intraclass correlation 0.92 on FAO and 0.07 (states) and 0.10 (districts) for India. Naive coverage of gradient boosting is 0.59, 0.85 and 0.90 in the same order. Model family matters as the theory predicts: on FAO, naive coverage is 0.47 for random forest, 0.59 for gradient boosting and 0.88 for ridge regression, while on the three settings group calibration gives about 0.89 to 0.90 for every model. Ridge regression is therefore robust to the collapse, but it is also the least accurate model under random splits, so a practitioner who chooses a model by random-split accuracy would choose one of the models whose intervals collapse. We have three settings, which show a monotone relation but not a fitted law, and the identification accuracy and feature correlation for India rest on a single continuous feature, so we read Table 9 as a consistent pattern and not as a quantitative calibration.

{{tab_fingerprint}}

## Comparing calibration schemes

All group-aware schemes restore marginal coverage (Table 7); they differ in how coverage is distributed across groups and in width. Group-CV calibration, which uses all training groups for calibration and averages five models, gives marginal coverage 0.908, 0.900 and 0.900, with intervals as narrow as the group split (2.17, 2.33 and 1.96). The weighted scheme is indistinguishable from the plain group scheme on every setting: this is consistent with a classifier that separates calibration rows from test rows almost perfectly on FAO, where the features nearly identify the country, so that clipped weights carry little usable information (we did not inspect the weight distribution). The distance score has mixed results: it does nothing on FAO (share of countries below nominal-10: 0.204 against 0.196) but lowers the share on Indian districts (0.076 against 0.116).

Normalising scores by the learned scale gives modest, consistent improvements in the weak tail (Table 10). The 10th-percentile group coverage rises by 0.051 on FAO (95% interval 0.018–0.085), by 0.024 on states (0.007–0.043) and by 0.012 on districts (0.006–0.019), and the share of groups more than 10 points below nominal falls by 0.059 on states (0.002–0.116, border of significance) and 0.016 on districts, with a non-significant change on FAO (−0.029, interval −0.078 to 0.023). The cost is width: intervals are wider by 0.26 on FAO and 0.18 on states, and slightly narrower on districts (−0.04). The method does not remove the tail: even with scaling, 17% of FAO countries and 10% of Indian districts remain more than 10 points below nominal, consistent with Eq. (7) and with the absence of group-conditional guarantees in the pooled approach.

![Fig. 4. Calibration schemes at nominal 90% on unseen groups. (a) 10th-percentile group coverage. (b) Share of groups more than 10 points below nominal. (c) Mean interval width (log-yield units). Error bars are 95% bootstrap intervals over seeds and folds.](../figures/fig05_methods.png){width=6.4in}

{{tab_paired}}

## Which groups are at risk

If intervals are to be trusted for a new place, it helps to know in advance whether the place is hard. Table 11 and Fig. 5 compare the two group-level scores. The learned scale correlates positively with a group's error in all three settings (Spearman 0.32 on FAO, 0.50 for states, 0.61 for districts), and clearly more than the distance of the group's covariate profile to the training groups (0.13, 0.12 and 0.39). The intervals are optimistic because group–fold pairs from different seeds are treated as independent, but the ordering of the two scores is stable across settings. The distance score is weak on FAO because the covariates are nearly country labels, so every new country is far from every training country and distance does not separate hard from easy ones, whereas the learned scale uses the model's own error structure. A correlation of 0.3 to 0.6 is useful for flagging, not for a decision rule.

{{tab_app}}

![Fig. 5. Learned residual scale σ(x) against the group's mean absolute error on test rows, by setting. Each point is a group in one outer fold.](../figures/fig06_applicability.png){width=6.4in}

## What a few local labels buy

Table 12 and Fig. 6 show the effect of labelled local rows. On FAO, five rows per country reduce the interval width from 2.21 to 1.95 (12%) at unchanged coverage (0.894), and twenty rows to 1.94; the RMSE after the shift falls from 0.677 to 0.592. On the Indian districts the effect is small: width 1.95 at five rows and 1.88 at twenty (4%), RMSE from 0.697 to 0.671. The share of groups below 80% coverage moves little (0.195 to 0.167 on FAO and 0.115 to 0.109 on India), so local labels sharpen the intervals but do not repair the heterogeneity across groups. The largest relative gain comes from the first few rows, in line with the shrinkage form $m/(m+3)$ of the shift.

![Fig. 6. Effect of m labelled local rows per test group on (a) interval width and (b) RMSE after the local shift, nominal 90%.](../figures/fig07_local.png){width=5.2in}

{{tab_local}}

## Checks

The group shuffle used by the split generator was corrected during the study (shuffling a pandas string array in place); we reran the FAO group-held-out point-accuracy and the first conformal experiments and the results were unchanged to the reported precision; the later experiments were run with the corrected code. Conformal coverage was measured on distinct FAO records only: with raw duplicated rows the same intervals would be scored on a pool in which heavily duplicated countries dominate, and we did not study that case. Gradient boosting in the conformal experiments uses default settings; the tuned variant was used in the point-accuracy comparison only.

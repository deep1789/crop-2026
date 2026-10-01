# Reference check C (checked 2026-10-01)

Sources: Crossref API (https://api.crossref.org/works/<DOI>), JMLR, NeurIPS proceedings page, WebSearch result text, GitHub repo pages. Kaggle and FAOSTAT pages could not be fetched directly (WebFetch returned only boilerplate); those were checked through WebSearch result text only.

## 1 breiman2001 - VERIFIED
L. Breiman, Random forests, Machine Learning 45 (1) (2001) 5-32. doi:10.1023/A:1010933404324.
NOT CONFIRMED: none. Author given as Leo Breiman. Source: https://api.crossref.org/works/10.1023/A:1010933404324

## 2 friedman2001 - VERIFIED
J.H. Friedman, Greedy function approximation: a gradient boosting machine, Annals of Statistics 29 (5) (2001) 1189-1232. doi:10.1214/aos/1013203451.
Crossref returned no page field, so the pages 1189-1232 come from WebSearch result text (Project Euclid listing; vol 29, issue 5, Oct 2001). Title, journal, volume, issue, year and DOI confirmed by Crossref.
NOT CONFIRMED: pages via Crossref; confirmed only from search text. Sources: https://api.crossref.org/works/10.1214/aos/1013203451 ; https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.full

## 3 hoerl1970 - VERIFIED (DOI added)
A.E. Hoerl, R.W. Kennard, Ridge regression: biased estimation for nonorthogonal problems, Technometrics 12 (1) (1970) 55-67. doi:10.1080/00401706.1970.10488634.
NOT CONFIRMED: none. Source: https://api.crossref.org/works/10.1080/00401706.1970.10488634

## 4 shrout1979 - VERIFIED
P.E. Shrout, J.L. Fleiss, Intraclass correlations: uses in assessing rater reliability, Psychological Bulletin 86 (2) (1979) 420-428. doi:10.1037/0033-2909.86.2.420.
NOT CONFIRMED: none. Source: https://api.crossref.org/works/10.1037/0033-2909.86.2.420

## 5 pedregosa2011 - CORRECTED (full author list)
F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, E. Duchesnay, Scikit-learn: machine learning in Python, Journal of Machine Learning Research 12 (2011) 2825-2830.
The author list (16 authors) matches the list supplied. No DOI found, so none is given. Issue number: JMLR has none.
NOT CONFIRMED: DOI (none retrieved). Source: https://jmlr.org/papers/v12/pedregosa11a.html

## 6 ke2017 - CORRECTED (full authors; pages from search text only)
G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, T.-Y. Liu, LightGBM: a highly efficient gradient boosting decision tree, Advances in Neural Information Processing Systems 30 (2017) 3146-3154.
The author list matches the current entry (Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, Tie-Yan Liu). Venue: NIPS 2017, volume 30. The NeurIPS page shows no volume or pages; pages 3146-3154 come only from WebSearch text (ACM DL listing dl.acm.org/doi/10.5555/3294996.3295074). One search result (SCIRP) gives different, garbled pages, so treat pages as a secondary confirmation only.
NOT CONFIRMED: pages (not on the NeurIPS page). Sources: https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html ; https://dl.acm.org/doi/10.5555/3294996.3295074

## 7 patel - PARTLY CONFIRMED
Entry text as proposed: R. Patel, Crop Yield Prediction Dataset, Kaggle, https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset (accessed October 2026).
Dataset exists. Search listing shows the title with an emoji ("Crop Yield Prediction Dataset") and the owner profile https://www.kaggle.com/patelris titled "Rishi Patel". So the owner display name is Rishi Patel, and the initial should be R. Patel, which matches. Stated sources (from search text): pesticides and yield data from FAO; rainfall and average temperature from the World Data Bank (World Bank); the final file is yield_df.csv. License per search text: World Bank Dataset Terms of Use. Covers 10 most-consumed crops.
NOT CONFIRMED: version number, publication/update date (page not fetchable). The license is from search text only. Source: WebSearch listing of https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset

## 8 abhinand - PARTLY CONFIRMED
Entry text: Abhinand, Crop Production in India, Kaggle, https://www.kaggle.com/datasets/abhinand05/crop-production-in-india (accessed October 2026).
Dataset exists. Description (search text): crop production in India over several years; 646 districts, 33 states, 1997-2015; 246,091 rows and 7 columns; crop_production.csv, 15.32 MB. The search text states NO origin or source (data.gov.in is not mentioned), so do not claim a source.
NOT CONFIRMED: owner display name (only the handle abhinand05 seen), origin/source, license, version, date. Source: WebSearch listing of https://www.kaggle.com/datasets/abhinand05/crop-production-in-india

## 9 faostat - PARTLY CONFIRMED
FAO, FAOSTAT: Production: Crops and livestock products (QCL), https://www.fao.org/faostat/en/#data/QCL (accessed October 2026).
Domain fao.org confirmed. Suggested citation, as reported in WebSearch text (not fetched from the page itself): "FAO. 2024. FAOSTAT: Production: Crops and livestock products. [Accessed on 28 October 2025]. https://www.fao.org/faostat/en/#data/QCL." License reported as CC-BY-4.0. The citation format is: FAO. <year of data release>. FAOSTAT: Production: Crops and livestock products. [Accessed on <date>]. <URL>. Elsevier-style suggestion: FAO, FAOSTAT: Production: Crops and livestock products (QCL), Food and Agriculture Organization of the United Nations, https://www.fao.org/faostat/en/#data/QCL (accessed October 2026).
NOT CONFIRMED: the exact current citation text and release year on the live page (page not fetchable); license is from search text only. Source: WebSearch (query on FAOSTAT suggested citation); fetch of https://www.fao.org/faostat/en/#data/QCL returned nothing useful.

## 10 pnastra - VERIFIED (repo exists; content quoted via fetch summary)
pnastra, crop-yield-forecast, GitHub repository, https://github.com/pnastra/crop-yield-forecast (accessed October 2026).
Owner shown: pnastra (no separate display name shown). Quotes (WebFetch of the README, may be lightly paraphrased by the fetch tool):
- "yield_df.csv has 28,242 rows but only 13,130 unique (country, crop, year) keys."
- "up to 22 weather-station readings per country-year (India)" (the author averaged temperature to one observation per country-year).
- Splits: "Time split (reported above)" versus "Random 80/20 (leakage demo)".
- "Beating the baseline by 9% in log RMSE, on future years, is a real but small gain." (LightGBM log RMSE 0.196 vs 0.216 baseline; MAPE 11.7% vs 12.1%.)
NOT CONFIRMED: last-commit date (page showed only "7 commits" on main); full sentences about the splits (only fragments retrieved). Source: https://github.com/pnastra/crop-yield-forecast

## 11 sivarjun - VERIFIED (repo exists; content quoted via fetch summary)
sivarjun21, crop-yield-prediction, GitHub repository, https://github.com/sivarjun21/crop-yield-prediction (accessed October 2026).
Owner shown: sivarjun21 (no separate display name). Quotes (WebFetch, may be partly paraphrased):
- "the dataset has near-duplicate rows (the same country and year appear for several crops with the same" (sentence truncated by the fetch tool).
- "similar rows can land in both train and test, so R² 0.979 is probably higher than what you would get on truly new years or countries."
Model: MLP with preprocessing, dropout and early stopping.
NOT CONFIRMED: last-commit date (page showed only "1 Commit"); the full text of the truncated duplicates sentence. Source: https://github.com/sivarjun21/crop-yield-prediction

## Note on "accessed" dates
Today's date (2026-10-01) comes from the session environment, not a web source. If you prefer to follow the instruction literally, leave "accessed 2026".

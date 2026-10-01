# Verified references

Method: each item was confirmed by a WebSearch result in this session. WebFetch was blocked by the egress proxy for arxiv.org, doi.org, sciencedirect.com, springer.com, tandfonline.com and thecvf.com, so no landing page was opened. Fields marked "(not in search result)" were not returned and were left out rather than filled from memory.

## A. Requested candidates

1. Vovk, V., Gammerman, A., Shafer, G. (2005). Algorithmic Learning in a Random World. Springer, New York. ISBN 978-0-387-00152-4. DOI: 10.1007/b106715. (Second edition 2022: 10.1007/978-3-031-06649-8.)
   Supports: foundational conformal prediction and exchangeability guarantee.

2. Angelopoulos, A. N., Bates, S. (2023). Conformal Prediction: A Gentle Introduction. Foundations and Trends in Machine Learning, 16(4), 494-591. DOI: 10.1561/2200000101. (arXiv title: "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification", arXiv:2107.07511.)
   Supports: tutorial on split/CV conformal and distribution shift.

3. Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., Wasserman, L. (2018). Distribution-Free Predictive Inference for Regression. Journal of the American Statistical Association, 113(523), 1094-1111. DOI: 10.1080/01621459.2017.1307116.
   Supports: split conformal for regression.

4. Tibshirani, R. J., Barber, R. F., Candes, E. J., Ramdas, A. (2019). Conformal Prediction Under Covariate Shift. Advances in Neural Information Processing Systems 32 (NeurIPS 2019). URL: https://proceedings.neurips.cc/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html (arXiv:1904.06019). Pages: (not in search result).
   Supports: weighted conformal under covariate shift.

5. Barber, R. F., Candes, E. J., Ramdas, A., Tibshirani, R. J. (2021). Predictive inference with the jackknife+. The Annals of Statistics, 49(1), 486-507. DOI: 10.1214/20-AOS1965.
   Supports: jackknife+ and CV+ style calibration without a held-out set.

6. Barber, R. F., Candes, E. J., Ramdas, A., Tibshirani, R. J. (2023). Conformal prediction beyond exchangeability. The Annals of Statistics, 51(2), 816-845. DOI: 10.1214/23-AOS2276.
   Supports: coverage loss when exchangeability fails; weighted quantiles.

7. Romano, Y., Patterson, E., Candes, E. J. (2019). Conformalized Quantile Regression. Advances in Neural Information Processing Systems 32 (NeurIPS 2019). URL: https://papers.nips.cc/paper/8613-conformalized-quantile-regression (arXiv:1905.03222). Pages: (not in search result).
   Supports: heteroscedasticity-adaptive intervals (locally adaptive baseline).

8. Dunn, R., Wasserman, L., Ramdas, A. (2023). Distribution-Free Prediction Sets for Two-Layer Hierarchical Models. Journal of the American Statistical Association, 118(544), 2491-2502. DOI: 10.1080/01621459.2022.2060112.
   Supports: conformal sets for grouped/hierarchical data.

9. Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schroder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., Dormann, C. F. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography, 40(8), 913-929. DOI: 10.1111/ecog.02881.
   Supports: blocked/grouped CV versus random CV.

10. Ploton, P., et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. Nature Communications, 11, Article 4540. DOI: 10.1038/s41467-020-18321-y. (Full author list: not in search result.)
    Supports: random CV overestimates skill under spatial structure.

11. Meyer, H., Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. Methods in Ecology and Evolution, 12, 1620-1633. DOI: 10.1111/2041-210X.13650.
    Supports: area-of-applicability (AOA) score.

12. Kapoor, S., Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. Patterns, 4(9). DOI: 10.1016/j.patter.2023.100804.
    Supports: leakage taxonomy and its prevalence (294 papers, 17 fields).

13. Koh, P. W., et al. (2021). WILDS: A Benchmark of in-the-Wild Distribution Shifts. Proceedings of the 38th ICML, PMLR 139, 5637-5664. URL: https://proceedings.mlr.press/v139/koh21a.html. (Full author list: not in search result.)
    Supports: group/domain shift benchmarks; in-distribution versus OOD gap.

14. van Klompenburg, T., Kassahun, A., Catal, C. (2020). Crop yield prediction using machine learning: A systematic literature review. Computers and Electronics in Agriculture, 177, Article 105709. DOI: 10.1016/j.compag.2020.105709.
    Supports: background on ML crop-yield prediction.

15. Barz, B., Denzler, J. (2020). Do We Train on Test Data? Purging CIFAR of Near-Duplicates. Journal of Imaging, 6(6), Article 41. URL: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8321059/ (arXiv:1902.00423). DOI: (not in search result). Note: the paper reports 3.3% (CIFAR-10) and 10% (CIFAR-100) of test images with a training-set duplicate.
    Supports: benchmark duplicates inflate scores.

16. Lones, M. A. (2021). How to avoid machine learning pitfalls: a guide for academic researchers. arXiv:2108.02497. URL: https://arxiv.org/abs/2108.02497. Note: only the arXiv preprint was verified. A journal version appeared to exist (ScienceDirect S2666389924001880, "Avoiding common machine learning pitfalls", Patterns), but its details were not confirmed, so cite the arXiv version unless you check the Patterns one.
    Supports: general pitfalls, including data leakage and evaluation.

17. Patel, R. (n.d.). Crop Yield Prediction Dataset (yield_df.csv; pesticides, rainfall, temp and yield files). Kaggle. URL: https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset. Description in search result: yield and pesticides from FAO, rainfall and temperature from the World Data Bank. Year published: (not in search result). Per a third-party repo description, 28,242 rows, 101 countries, 10 crops, 1990-2013; this was not checked against the dataset itself.
    Supports: dataset under audit.

18. Abhinand (Kaggle user abhinand05). Crop Production in India. Kaggle. URL: https://www.kaggle.com/datasets/abhinand05/crop-production-in-india. Described as state/district-level production, 1997-2015, crop_production.csv. Link to data.gov.in as the original source: NOT VERIFIED from the dataset page. A different Kaggle dataset (srinivas1) states data.gov.in as its source. Check the dataset description before claiming provenance.
    Supports: dataset under audit.

19. FAO. FAOSTAT: Production: Crops and livestock products (QCL). URL: https://www.fao.org/faostat/en/#data/QCL. Suggested citation form from search: "FAO. 2024. FAOSTAT: Production: Crops and livestock products. [Accessed on date]. Licence: CC-BY-4.0." Use your own access year and date.
    Supports: upstream source for yield and pesticide variables.

## B. Additional verified papers

20. Farag, M., Emam, A., Leonhardt, J., Roscher, R. (2025). Enhancing decision support in crop production: Analyzing conformal prediction for uncertainty quantification. Computers and Electronics in Agriculture, 237(Part B). DOI: 10.1016/j.compag.2025.110559. Article number: (not in search result).
    Supports: conformal prediction applied to agriculture. Note: the abstract mentions ResNet-18 and ViT-B/16, so it is image tasks, not tabular yield regression.

21. Melki, P., Bombrun, L., Diallo, B., Dias, J., da Costa, J.-P. (2023). Group-Conditional Conformal Prediction via Quantile Regression Calibration for Crop and Weed Classification. Proceedings of the IEEE/CVF ICCV Workshops, pp. 614-623. URL: https://openaccess.thecvf.com/content/ICCV2023W/CVPPA/html/Melki_Group-Conditional_Conformal_Prediction_via_Quantile_Regression_Calibration_for_Crop_and_ICCVW_2023_paper.html (arXiv:2308.15094).
    Supports: group-conditional conformal calibration in agriculture (classification).

22. Vovk, V. (2013). Conditional validity of inductive conformal predictors. Machine Learning, 92(2-3), 349-376. DOI: 10.1007/s10994-013-5355-6.
    Supports: Mondrian (group-conditional) conformal calibration.

23. Gibbs, I., Cherian, J. J., Candes, E. J. (2025). Conformal prediction with conditional guarantees. Journal of the Royal Statistical Society Series B: Statistical Methodology, 87(4), 1100-1126. DOI: 10.1093/jrsssb/qkaf008.
    Supports: group-conditional coverage over overlapping groups and covariate-shift guarantees.

24. Hajjem, A., Bellavance, F., Larocque, D. (2014). Mixed-effects random forest for clustered data. Journal of Statistical Computation and Simulation, 84(6), 1313-1328. DOI: 10.1080/00949655.2012.741599.
    Supports: standard random forest ignores within-cluster dependence. Note: this is indirect support for the "trees memorize group identity" claim, not a direct demonstration of it.

25. Filippi, P., Han, S. Y., Bishop, T. F. A. (2024). On crop yield modelling, predicting, and forecasting and addressing the common issues in published studies. Precision Agriculture. Published online 7 Dec 2024. URL: https://link.springer.com/article/10.1007/s11119-024-10212-2. Volume, pages and DOI: (not in search result). The URL suffix suggests DOI 10.1007/s11119-024-10212-2, but it was not confirmed.
    Supports: validation-design critique in crop yield studies; random versus spatial/temporal CV.

26. Adjei, Y. O. (2026). Do Foundation Model Embeddings Improve Cross-Country Crop Yield Generalisation? A Leave-One-Country-Out Evaluation in Sub-Saharan Africa. arXiv:2605.08113 (preprint, not peer reviewed as far as verified). URL: https://arxiv.org/abs/2605.08113. The search result lists only this one author. Note: R2 0.17-0.30 within-country but negative under leave-one-country-out. The search snippet also reports a 0.22-0.38 R2 inflation; I did not confirm that it comes from this paper.
    Supports: leave-one-country-out evaluation versus random CV in crop yield.

## C. NOT VERIFIED

- (1) A peer-reviewed paper that trains on the Kaggle FAO yield_df dataset and shows random-split inflation: NOT VERIFIED. Searches returned only GitHub projects (for example Mithra1112/Crop-Yield-Prediction, reporting Random Forest R2 = 0.985). They are not citable papers, and I did not check their splits. They can be cited as grey-literature examples of the claim.
- (5) A paper directly showing tree ensembles memorize group identity under grouped data: NOT VERIFIED. Only Hajjem et al. (item 24) was verified, as indirect support. A GitHub repo ("group-identifier-leakage") surfaced, but it is not a verified paper. An out-of-bag-overestimation paper in PLOS ONE (2018) also appeared, but I did not verify its authors or details, so it is omitted.
- Landing pages for the NeurIPS pages, Barz & Denzler DOI, Ploton and Koh full author lists: not retrieved because fetching was blocked.

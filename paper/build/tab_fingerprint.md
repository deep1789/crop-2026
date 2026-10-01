Table: Table 9. Group fingerprint strength and conformal coverage by model family (naive / group calibration, nominal 90%). Group-ID accuracy is the five-nearest-neighbour accuracy of identifying the group from the features, with the largest-group share in brackets. Feature ICC is the mean intraclass correlation of the continuous features (the Indian table has one, log area).

| Setting | Groups | Group-ID accuracy | Feature ICC | Ridge | GBM | Random forest |
|:---|---:|:---|---:|:---|:---|:---|
| FAO, unseen countries | 101 | 0.596 (0.018) | 0.92 | 0.881 / 0.886 | 0.589 / 0.899 | 0.466 / 0.899 |
| India, unseen states | 33 | 0.313 (0.139) | 0.07 | 0.869 / 0.885 | 0.850 / 0.891 | 0.835 / 0.891 |
| India, unseen districts | 651 | 0.019 (0.004) | 0.10 | 0.899 / 0.899 | 0.897 / 0.900 | 0.896 / 0.901 |

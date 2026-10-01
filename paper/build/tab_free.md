Table: Table 15. Place lookups and fingerprint-free features on the FAO file (distinct records). Upper block: RMSE of log-yield (R² in brackets) by protocol. Lower block: conformal coverage on unseen countries at nominal 90% with each feature set (gradient boosting; a separate three-seed run, so naive coverage with full features is 0.602 against 0.598 in Table 7).

| Model | Random | Forward in time | Country held out |
|:---|:---|:---|:---|
| Crop mean | 0.731 (0.580) | 0.749 (0.560) | 0.739 (0.566) |
| Country–crop mean (lookup) | 0.293 (0.932) | 0.369 (0.893) | 0.739 (0.566) |
| Ridge, anomaly features | 0.724 (0.587) | 0.737 (0.574) | 0.733 (0.573) |
| GBM, anomaly features | 0.609 (0.708) | 0.688 (0.629) | 0.736 (0.570) |
| GBM, full features | 0.323 (0.918) | 0.362 (0.897) | 0.670 (0.643) |
| Lookup + GBM on anomalies | 0.262 (0.946) | 0.337 (0.911) | 0.734 (0.572) |

| Features | Group-ID accuracy | Naive coverage | Group coverage | Naive width | Group width |
|:---|---:|---:|---:|---:|---:|
| full | 0.596 | 0.602 | 0.904 | 0.96 | 2.21 |
| anomaly | 0.062 | 0.829 | 0.897 | 1.91 | 2.37 |

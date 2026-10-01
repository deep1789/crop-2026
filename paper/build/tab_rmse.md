Table: Table B1. RMSE of log-yield, FAO file (distinct records), mean over seeds and folds.

| Model | Random | Forward in time | Country held out |
|:---|---:|---:|---:|
| Crop mean | 0.731 | 0.749 | 0.739 |
| Ridge | 0.666 | 0.687 | 0.696 |
| Random forest | 0.247 | 0.312 | 0.709 |
| GBM (tuned) | 0.297 | 0.344 | 0.657 |
| GBM + group ID | 0.261 | 0.313 | 0.751 |

Table: Table B2. RMSE of log-yield, Indian district table, mean over seeds and folds.

| Model | Random | Forward in time | District held out | State held out |
|:---|---:|---:|---:|---:|
| Crop mean | 0.740 | 0.735 | 0.742 | 0.815 |
| Ridge | 0.725 | 0.710 | 0.727 | 0.805 |
| Random forest | 0.706 | 0.753 | 0.731 | 0.907 |
| GBM (tuned) | 0.692 | 0.702 | 0.705 | 0.832 |
| GBM + group ID | 0.587 | 0.623 | 0.742 | 0.849 |

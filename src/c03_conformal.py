"""Usage: python c03_conformal.py <dataset>   (fao_clean | india)
Split-conformal coverage under group shift. Calibrators:
  naive  - calibration rows drawn from the same groups as the fit rows
  group  - calibration on whole groups disjoint from fit groups
  dist   - group calibration with residuals scaled by a group-distance score
Writes results/c03_<dataset>.json."""
import sys, json
from scipy.stats import norm
from crop_common import *

ds = sys.argv[1]; ALPHA = 0.1; Z = norm.ppf(1 - ALPHA / 2)
if ds == "fao_clean":
    d = load_fao(True); Xdf = design_fao(d); G = d.country.values
else:
    d = load_india(True); Xdf = design_india(d); G = d.dist_id.values
X = Xdf.values.astype(float); y = d.ly.values
# group profile: mean of standardised features per group (excludes year)
Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
prof = pd.DataFrame(Xs).groupby(pd.Series(G).values).mean()


def qhat(s, a=ALPHA):
    k = int(np.ceil((len(s) + 1) * (1 - a))); return np.sort(s)[min(k, len(s)) - 1]


def gdist(gs, ref, k=5):
    """mean distance from each group profile in gs to its k nearest groups in ref."""
    A = prof.loc[gs].values; B = prof.loc[ref].values
    D = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1))
    return pd.Series(np.sort(D, 1)[:, :k].mean(1), index=gs)


rows = []
for seed in range(3):
    for lab, tr, te in split_group(G, 5, seed):
        rng = np.random.RandomState(seed)
        trg = pd.unique(G[tr]); rng.shuffle(trg)
        ncal = max(2, int(0.3 * len(trg))); calg = set(trg[:ncal]); fitg = trg[ncal:]
        is_cal = np.array([g in calg for g in G[tr]])
        fit_g_idx = tr[~is_cal]; cal_g_idx = tr[is_cal]            # group-aware split
        r_ = rng.rand(len(tr)); fit_n_idx = tr[r_ >= 0.3]; cal_n_idx = tr[r_ < 0.3]  # naive split
        for calib in ["naive", "group", "dist"]:
            fi, ci = (fit_n_idx, cal_n_idx) if calib == "naive" else (fit_g_idx, cal_g_idx)
            mod = make_model("gbm", seed).fit(X[fi], y[fi])
            rc = np.abs(y[ci] - mod.predict(X[ci])); rt = np.abs(y[te] - mod.predict(X[te]))
            if calib == "dist":
                fg = pd.unique(G[fi])
                dc = gdist(pd.Series(G[ci]).unique(), fg).reindex(G[ci]).values
                dt = gdist(pd.Series(G[te]).unique(), fg).reindex(G[te]).values
                b, a = np.polyfit(dc, rc, 1); a = max(a, 1e-3)
                u = lambda dd: np.maximum(a + b * dd, 0.05 * rc.mean())
                q = qhat(rc / u(dc)); half = q * u(dt)
                cov_rows = rt <= half; width = 2 * half.mean()
            else:
                q = qhat(rc); cov_rows = rt <= q; width = 2 * q
            gcov = pd.Series(cov_rows).groupby(G[te]).mean()
            rho = float(np.sqrt(np.mean(rt ** 2)) / np.sqrt(np.mean(rc ** 2)))
            rows.append(dict(dataset=ds, calib=calib, seed=seed, split=lab, n_test=int(len(te)),
                             coverage=float(cov_rows.mean()), mean_group_cov=float(gcov.mean()),
                             frac_groups_below_80=float((gcov < 0.8).mean()),
                             width=float(width), rho=rho,
                             law_pred=float(2 * norm.cdf(Z / rho) - 1)))
            print(rows[-1], flush=True)
json.dump(rows, open(os.path.join(RES, f"c03_{ds}.json"), "w"), indent=1)

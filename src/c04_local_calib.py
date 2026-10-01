"""Usage: python c04_local_calib.py <dataset>. Calibration with m labelled local rows from the target group.
For each test group, m rows are used to (i) shift predictions by a shrunk mean residual and (ii) are excluded
from scoring. Conformal scores are collected the same way on disjoint calibration groups, so the
procedure is exchangeable at the group level. Writes results/c04_<dataset>.json."""
import sys, json
from crop_common import *

ds = sys.argv[1]; ALPHA = 0.1; K0 = 3.0; MS = [0, 1, 3, 5, 10, 20]
if ds == "fao_clean":
    d = load_fao(True); X = design_fao(d).values.astype(float); G = d.country.values
else:
    d = load_india(True); X = design_india(d).values.astype(float); G = d.dist_id.values
y = d.ly.values
def qhat(s):
    k = int(np.ceil((len(s) + 1) * (1 - ALPHA))); return np.sort(s)[min(k, len(s)) - 1]

def local_scores(idx, pred, m, rng):
    """for each group in idx: use m rows for a bias shift, return |residual| of the remaining rows."""
    out, shifts = [], {}
    for g, ii in pd.Series(idx).groupby(G[idx]):
        ii = ii.values
        if len(ii) <= m + 2: continue
        p = rng.permutation(ii); loc, rest = p[:m], p[m:]
        delta = 0.0 if m == 0 else (m / (m + K0)) * np.mean(y[loc] - pred[loc])
        out.append((g, rest, np.abs(y[rest] - pred[rest] - delta)))
    return out

rows = []
for seed in range(3):
    for lab, tr, te in split_group(G, 5, seed):
        rng = np.random.RandomState(seed)
        trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
        calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]])
        fi, ci = tr[~is_cal], tr[is_cal]
        mod = make_model("gbm", seed).fit(X[fi], y[fi]); pred = mod.predict(X)
        for m in MS:
            cs = local_scores(ci, pred, m, rng); ts = local_scores(te, pred, m, rng)
            q = qhat(np.concatenate([s for _, _, s in cs]))
            cov = np.concatenate([s <= q for _, _, s in ts]); gc = [np.mean(s <= q) for _, _, s in ts]
            rmse = float(np.sqrt(np.mean(np.concatenate([s for _, _, s in ts]) ** 2)))
            rows.append(dict(dataset=ds, m=m, seed=seed, split=lab, coverage=float(cov.mean()),
                             mean_group_cov=float(np.mean(gc)), frac_groups_below_80=float(np.mean(np.array(gc) < .8)),
                             width=float(2 * q), rmse_after_shift=rmse))
            print(rows[-1], flush=True)
json.dump(rows, open(os.path.join(RES, f"c04_{ds}.json"), "w"), indent=1)

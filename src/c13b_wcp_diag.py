"""Weighted conformal diagnostics on FAO (distinct records). Two calibration sets are weighted towards the test fold:
 'naive' rows (seen groups; the intended use of covariate-shift weights) and 'group' rows (unseen calibration groups).
Weights come from a cross-fitted (shuffled 3-fold) domain classifier. Reports AUC, effective sample size, clipping and coverage."""
import json
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import roc_auc_score
from crop_common import *

d = load_fao(True); X = design_fao(d).values.astype(float); y = d.ly.values; G = d.country.values
def gbm(seed): return LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, n_jobs=1, random_state=seed, verbose=-1)
def wq(s, w, a, wt):
    o = np.argsort(s); s, w = s[o], w[o]; c = np.cumsum(w) / (w.sum() + wt); i = np.searchsorted(c, 1 - a); return s[i] if i < len(s) else np.inf
rows = []
for seed in range(5):
    for lab, tr, te in split_group(G, 5, seed):
        rng = np.random.RandomState(seed); trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
        calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]]); fi, ci = tr[~is_cal], tr[is_cal]
        u = rng.rand(len(tr)); fn, cn = tr[u >= 0.3], tr[u < 0.3]
        for nm, (a, b) in {"naive": (fn, cn), "group": (fi, ci)}.items():
            m = gbm(seed).fit(X[a], y[a]); rc = np.abs(y[b] - m.predict(X[b])); rt = np.abs(y[te] - m.predict(X[te]))
            Xd = np.vstack([X[b], X[te]]); yd = np.r_[np.zeros(len(b)), np.ones(len(te))]
            clf = LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=15, n_jobs=1, random_state=seed, verbose=-1)
            p = cross_val_predict(clf, Xd, yd, cv=KFold(3, shuffle=True, random_state=seed), method="predict_proba")[:, 1]
            auc = roc_auc_score(yd, p); pc = np.clip(p[:len(b)], 1e-3, 1 - 1e-3); w = (pc / (1 - pc)) * len(b) / len(te)
            wc = np.clip(w, 0.05, 20); ess = wc.sum() ** 2 / (wc ** 2).sum() / len(wc); essu = w.sum() ** 2 / (w ** 2).sum() / len(w)
            cov_w = float((rt <= wq(rc, wc, 0.1, wc.mean())).mean()); cov_u = float((rt <= np.sort(rc)[min(int(np.ceil((len(rc) + 1) * 0.9)) - 1, len(rc) - 1)]).mean())
            rows.append(dict(cal=nm, seed=seed, split=lab, auc=float(auc), ess_unclipped=float(essu), ess_clipped=float(ess), frac_clip_lo=float((w < 0.05).mean()),
                             frac_clip_hi=float((w > 20).mean()), cov_unweighted=cov_u, cov_weighted=cov_w))
df = pd.DataFrame(rows); s = df.groupby("cal").mean(numeric_only=True).drop(columns=["seed"]); print(s.round(3).to_string())
json.dump(df.to_dict("records"), open(os.path.join(RES, "c13b_wcp_diag.json"), "w"))

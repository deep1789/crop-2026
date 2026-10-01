"""Robustness checks: (1) weighted-conformal weight diagnostics on FAO, (2) conformal on raw (duplicated) FAO rows,
(3) group-level (cluster) bootstrap of the applicability correlations."""
import json
from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
from crop_common import *

out = {}
def gbm(seed): return LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, n_jobs=1, random_state=seed, verbose=-1)
def qhat(s, a):
    k = int(np.ceil((len(s) + 1) * (1 - a))); return np.sort(s)[min(k, len(s)) - 1]

# ---- (1) weights on clean FAO and (2) raw rows
for tag, clean in [("fao_clean", True), ("fao_raw", False)]:
    d = load_fao(clean); X = design_fao(d).values.astype(float); y = d.ly.values; G = d.country.values
    rows, wd = [], []
    for seed in range(5):
        for lab, tr, te in split_group(G, 5, seed):
            rng = np.random.RandomState(seed); trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
            calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]]); fi, ci = tr[~is_cal], tr[is_cal]
            u = rng.rand(len(tr)); fn, cn = tr[u >= 0.3], tr[u < 0.3]
            res = {}
            for nm, (a, b) in {"naive": (fn, cn), "group": (fi, ci)}.items():
                m = gbm(seed).fit(X[a], y[a]); rc = np.abs(y[b] - m.predict(X[b])); rt = np.abs(y[te] - m.predict(X[te]))
                res[nm] = float((rt <= qhat(rc, 0.1)).mean()); res[nm + "_width"] = float(2 * qhat(rc, 0.1))
            rows.append(dict(seed=seed, split=lab, **res))
            if clean:   # weight diagnostics
                Xd = np.vstack([X[ci], X[te]]); yd = np.r_[np.zeros(len(ci)), np.ones(len(te))]
                clf = LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=15, n_jobs=1, random_state=seed, verbose=-1)
                pcv = cross_val_predict(clf, Xd, yd, cv=3, method="predict_proba")[:, 1]
                clf.fit(Xd, yd); p = np.clip(clf.predict_proba(X[ci])[:, 1], 1e-3, 1 - 1e-3); w = (p / (1 - p)) * len(ci) / len(te)
                wc = np.clip(w, 0.05, 20)
                wd.append(dict(auc_cv=float(roc_auc_score(yd, pcv)), ess_frac=float(wc.sum() ** 2 / (wc ** 2).sum() / len(wc)),
                               frac_clipped_hi=float((w > 20).mean()), frac_clipped_lo=float((w < 0.05).mean()), median_w=float(np.median(w))))
    r = pd.DataFrame(rows); out[tag] = {k: float(r[k].mean()) for k in ["naive", "group", "naive_width", "group_width"]}
    # weight diagnostics superseded by c13b_wcp_diag.py (shuffled cross-fitting); the unshuffled variant here was an artefact
    print(tag, out[tag], flush=True)
print("wcp diag", out.get("wcp_diag"))

# ---- (3) cluster bootstrap of applicability correlations (group-level, averaged over seeds/folds)
rng = np.random.RandomState(0); app = {}
for st in ["fao", "india_state", "india_district"]:
    g = pd.DataFrame(json.load(open(os.path.join(RES, f"c08_diag_{st}.json")))).groupby("group")[["d", "sigma", "mae"]].mean()
    for k in ["d", "sigma"]:
        r0 = spearmanr(g[k], g.mae)[0]; bs = []
        for _ in range(1000):
            i = rng.choice(len(g), len(g)); bs.append(spearmanr(g[k].values[i], g.mae.values[i])[0])
        app[f"{st}|{k}"] = [float(r0), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), int(len(g))]
out["applicability_cluster"] = app; print(app)
json.dump(out, open(os.path.join(RES, "c13_robustness.json"), "w"), indent=1)

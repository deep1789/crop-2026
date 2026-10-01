"""(1) Group-fingerprint strength per setting: row-level accuracy of identifying the group from features
    (kNN, random row split) and mean per-feature ICC. (2) Model-agnostic naive-vs-group coverage (ridge, rf, gbm)."""
import json
from sklearn.neighbors import KNeighborsClassifier
from scipy.stats import norm
from crop_common import *

Z = norm.ppf(0.95); out = {"fingerprint": {}, "models": []}
def prep(st):
    if st == "fao":
        d = load_fao(True); X = design_fao(d); G = d.country.values
    else:
        d = load_india(True); X = design_india(d); G = d.dist_id.values if st == "india_district" else d.state.values
        if len(d) > 60000: s = np.random.RandomState(0).choice(len(d), 60000, replace=False); d, X, G = d.iloc[s].reset_index(drop=True), X.iloc[s].reset_index(drop=True), G[s]
    return d, X, G
for st in ["fao", "india_state", "india_district"]:
    d, X, G = prep(st); Xv = X.values.astype(float); Xs = (Xv - Xv.mean(0)) / (Xv.std(0) + 1e-9)
    nonyear = [c for c in X.columns if c != "year"]
    # kNN group identification, random 70/30 row split; chance = majority share
    rng = np.random.RandomState(0); m = rng.rand(len(G)) < 0.7
    knn = KNeighborsClassifier(5).fit(Xs[m], G[m]); acc = float((knn.predict(Xs[~m]) == G[~m]).mean())
    chance = float(pd.Series(G).value_counts(normalize=True).iloc[0])
    cont = [c for c in X.columns if X[c].nunique() > 2 and c != "year"]
    icc = {c: icc_oneway(X[c], G) for c in cont}
    out["fingerprint"][st] = {"group_id_accuracy": acc, "majority_share": chance, "n_groups": int(len(np.unique(G))),
                              "feature_icc": icc, "mean_feature_icc": float(np.mean(list(icc.values()))) if icc else None}
    print(st, out["fingerprint"][st], flush=True)
    # model-agnostic naive vs group split-conformal at alpha=.1
    y = d.ly.values
    for mname in ["ridge", "rf", "gbm"]:
        for seed in range(2):
            for lab, tr, te in split_group(G, 5, seed):
                rng = np.random.RandomState(seed); trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
                calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]])
                fi, ci = tr[~is_cal], tr[is_cal]; u = rng.rand(len(tr)); fn, cn = tr[u >= 0.3], tr[u < 0.3]
                def q(s): k = int(np.ceil((len(s) + 1) * 0.9)); return np.sort(s)[min(k, len(s)) - 1]
                res = {}
                for nm, (a, b) in {"naive": (fn, cn), "group": (fi, ci)}.items():
                    a = a if not (mname == "rf" and len(a) > 20000) else rng.choice(a, 20000, replace=False)
                    mod = make_model(mname, seed).fit(Xv[a], y[a]); res[nm] = float((np.abs(y[te] - mod.predict(Xv[te])) <= q(np.abs(y[b] - mod.predict(Xv[b])))).mean())
                out["models"].append(dict(setting=st, model=mname, seed=seed, split=lab, **res))
    mm = pd.DataFrame(out["models"]); print(mm[mm.setting == st].groupby("model")[["naive", "group"]].mean().round(3), flush=True)
json.dump(out, open(os.path.join(RES, "c09_fingerprint.json"), "w"), indent=1)

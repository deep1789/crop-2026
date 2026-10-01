"""Fingerprint-free features on FAO (distinct records). Feature sets:
  full    : crop, year, rain, pesticides, temperature (as distributed)
  anomaly : crop, year, within-country temperature anomaly, within-country log-pesticide anomaly (country means removed; rainfall dropped, it is constant within country)
Compares point accuracy under random / forward / group protocols (with crop-mean and country-crop-mean baselines),
naive vs group conformal coverage, and group-ID accuracy from features."""
import json
from sklearn.neighbors import KNeighborsClassifier
from lightgbm import LGBMRegressor
from scipy.stats import norm
from crop_common import *

d = load_fao(True); y = d.ly.values; G = d.country.values; n = len(d)
d["temp_anom"] = d.temp - d.groupby("country").temp.transform("mean")
d["lpest"] = np.log1p(d.pest); d["pest_anom"] = d.lpest - d.groupby("country").lpest.transform("mean")
crop = pd.get_dummies(d.crop).astype(float)
FS = {"full": pd.concat([crop, d[["year", "rain", "pest", "temp"]]], axis=1).values.astype(float),
      "anomaly": pd.concat([crop, d[["year", "temp_anom", "pest_anom"]]], axis=1).values.astype(float)}
CROP = crop.values.argmax(1); CC = pd.factorize(pd.Series(G) + "|" + pd.Series(CROP.astype(str)))[0]
def gbm(seed): return LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, n_jobs=1, random_state=seed, verbose=-1)
def qhat(s, a=0.1): k = int(np.ceil((len(s) + 1) * (1 - a))); return np.sort(s)[min(k, len(s)) - 1]
def splits(proto, seed):
    if proto == "random": return list(split_random(n, 5, seed))
    if proto == "group": return list(split_group(G, 5, seed))
    return list(split_forward(d.year.values))
rows, cov = [], []
for proto in ["random", "forward", "group"]:
    for seed in ([0] if proto == "forward" else [0, 1, 2]):
        for lab, tr, te in splits(proto, seed):
            res = {}
            cm = pd.Series(y[tr]).groupby(CROP[tr]).mean(); res["crop_mean"] = cm.reindex(CROP[te]).fillna(y[tr].mean()).values
            ccm = pd.Series(y[tr]).groupby(CC[tr]).mean(); base_cc = ccm.reindex(CC[te]).values; res["country_crop_mean"] = np.where(np.isnan(base_cc), res["crop_mean"], base_cc)
            for fs, X in FS.items():
                res[f"ridge_{fs}"] = make_model("ridge").fit(X[tr], y[tr]).predict(X[te])
                res[f"gbm_{fs}"] = gbm(seed).fit(X[tr], y[tr]).predict(X[te])
            # place-aware residual model on anomalies: country-crop mean + gbm on residual (only where the country-crop is seen)
            Xa = FS["anomaly"]; ccm_tr = ccm.reindex(CC[tr]).values; r_tr = y[tr] - ccm_tr
            res["cc_mean_plus_gbm_anomaly"] = res["country_crop_mean"] + gbm(seed).fit(Xa[tr], r_tr).predict(Xa[te])
            for m, p in res.items():
                r = metrics(y[te], p); r.update(proto=proto, seed=seed, split=lab, model=m); rows.append(r)
# conformal naive vs group with each feature set (gbm)
for fs, X in FS.items():
    for seed in range(3):
        for lab, tr, te in split_group(G, 5, seed):
            rng = np.random.RandomState(seed); trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
            calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]]); fi, ci = tr[~is_cal], tr[is_cal]
            u = rng.rand(len(tr)); fn, cn = tr[u >= 0.3], tr[u < 0.3]; r = {}
            for nm, (a, b) in {"naive": (fn, cn), "group": (fi, ci)}.items():
                m = gbm(seed).fit(X[a], y[a]); q = qhat(np.abs(y[b] - m.predict(X[b]))); r[nm] = float((np.abs(y[te] - m.predict(X[te])) <= q).mean()); r[nm + "_width"] = float(2 * q)
            cov.append(dict(features=fs, seed=seed, split=lab, **r))
# fingerprint identifiability
fp = {}
for fs, X in FS.items():
    nonyear = [i for i in range(X.shape[1]) if i != X.shape[1] - 4 + (0 if fs == "full" else 0)]
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9); rng = np.random.RandomState(0); msk = rng.rand(n) < 0.7
    fp[fs] = float((KNeighborsClassifier(5).fit(Xs[msk], G[msk]).predict(Xs[~msk]) == G[~msk]).mean())
R = pd.DataFrame(rows); C = pd.DataFrame(cov)
tab = R.groupby(["proto", "model"])[["rmse", "r2"]].mean().round(3); print(tab.unstack(0).to_string())
print(C.groupby("features")[["naive", "group", "naive_width", "group_width"]].mean().round(3)); print("group-ID accuracy", fp)
out = {"point": {f"{p}|{m}": {k: [float(v) for v in (g[k].mean(), *np.percentile([np.random.RandomState(0).choice(g[k].values, len(g)).mean() for _ in range(1)], [50, 50]))] for k in ["rmse", "r2"]} for (p, m), g in R.groupby(["proto", "model"])},
       "point_ci": {}, "coverage": C.groupby("features")[["naive", "group", "naive_width", "group_width"]].mean().to_dict(), "fingerprint_id_acc": fp}
rng = np.random.RandomState(0)
def ci(x): x = np.asarray(x); b = [rng.choice(x, len(x)).mean() for _ in range(2000)]; return [float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]
out["point_ci"] = {f"{p}|{m}": {k: ci(g[k]) for k in ["rmse", "r2"]} for (p, m), g in R.groupby(["proto", "model"])}
out["coverage_ci"] = {f"{fs}|{k}": ci(g[k]) for fs, g in C.groupby("features") for k in ["naive", "group", "naive_width", "group_width"]}
json.dump(out, open(os.path.join(RES, "c14_fingerprint_free.json"), "w"), indent=1)

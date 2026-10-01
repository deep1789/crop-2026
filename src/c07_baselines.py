"""Usage: python c07_baselines.py <dataset> <protocol>   dataset: fao_clean|india ; protocol: random|group|group_state|forward
Stronger baselines over 3 split seeds: crop-mean, ridge, rf, gbm, gbm_tuned (inner protocol-matched CV), gbm_id (group id as categorical)."""
import sys, json, time
from lightgbm import LGBMRegressor
from crop_common import *

ds, proto = sys.argv[1], sys.argv[2]
if ds == "fao_clean":
    d = load_fao(True); X = design_fao(d); gcol = {"group": "country", "group_state": "country"}; idcol = "country"
    crop_cols = [c for c in X.columns if c not in ("year", "rain", "pest", "temp")]
else:
    d = load_india(True); X = design_india(d); gcol = {"group": "dist_id", "group_state": "state"}; idcol = "dist_id"
    crop_cols = [c for c in X.columns if c.startswith("crop_")]
Xv = X.values.astype(float); y = d.ly.values; n = len(y)
ids = pd.Series(d[idcol].values).astype("category").cat.codes.values.astype(float)
Xid = np.column_stack([Xv, ids]); id_col = Xv.shape[1]
CROP = Xv[:, [list(X.columns).index(c) for c in crop_cols]].argmax(1)

def splits(seed):
    if proto == "random": return list(split_random(n, 5, seed))
    if proto.startswith("group"): return list(split_group(d[gcol[proto]].values, 5, seed))
    return list(split_forward(d["year"].values))
def inner_folds(tr, seed):
    if proto == "random": rng = np.random.RandomState(seed); f = rng.randint(0, 3, len(tr)); return [(np.where(f != k)[0], np.where(f == k)[0]) for k in range(3)]
    if proto.startswith("group"):
        return [(a, b) for _, a, b in split_group(d[gcol[proto]].values[tr], 3, seed)]
    yrs = d["year"].values[tr]; cut = np.quantile(yrs, [0.5, 0.75]); return [(np.where(yrs <= c)[0], np.where((yrs > c) & (yrs <= c + 3))[0]) for c in cut]
CFG = [dict(num_leaves=7, learning_rate=0.1, n_estimators=200, min_child_samples=20),
       dict(num_leaves=15, learning_rate=0.05, n_estimators=300, min_child_samples=20),
       dict(num_leaves=31, learning_rate=0.05, n_estimators=300, min_child_samples=100),
       dict(num_leaves=63, learning_rate=0.03, n_estimators=500, min_child_samples=50)]
def gbm(cfg, seed): return LGBMRegressor(n_jobs=1, random_state=seed, verbose=-1, **cfg)

rows = []; seeds = [0] if proto == "forward" else [0, 1, 2]
for seed in seeds:
    for lab, tr, te in splits(seed):
        rng = np.random.RandomState(seed)
        res = {}
        # crop-mean
        cm = pd.Series(y[tr]).groupby(CROP[tr]).mean(); res["crop_mean"] = cm.reindex(CROP[te]).fillna(y[tr].mean()).values
        for m in ["ridge", "rf", "gbm"]:
            tri = tr if not (m == "rf" and len(tr) > 40000) else rng.choice(tr, 40000, replace=False)
            res[m] = make_model(m, seed).fit(Xv[tri], y[tri]).predict(Xv[te])
        # tuned gbm
        sub = tr if len(tr) <= 30000 else np.sort(rng.choice(tr, 30000, replace=False))
        best, bs = CFG[1], 1e9
        for cfg in CFG:
            sc = []
            for a, b in inner_folds(sub, seed):
                if len(a) < 50 or len(b) < 10: continue
                sc.append(metrics(y[sub][b], gbm(cfg, seed).fit(Xv[sub][a], y[sub][a]).predict(Xv[sub][b]))["rmse"])
            if sc and np.mean(sc) < bs: bs, best = np.mean(sc), cfg
        res["gbm_tuned"] = gbm(best, seed).fit(Xv[tr], y[tr]).predict(Xv[te])
        res["gbm_id"] = gbm(CFG[1], seed).fit(Xid[tr], y[tr], categorical_feature=[id_col]).predict(Xid[te])
        for m, p in res.items():
            r = metrics(y[te], p); r.update(split=lab, seed=seed, model=m, n_test=int(len(te)), proto=proto, dataset=ds)
            rows.append(r)
        print(ds, proto, seed, lab, {m: round(metrics(y[te], p)["rmse"], 3) for m, p in res.items()}, flush=True)
json.dump(rows, open(os.path.join(RES, f"c07_{ds}_{proto}.json"), "w"), indent=1)

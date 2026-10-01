"""Usage: python c02_transfer.py <dataset> <protocol>
dataset in {fao_raw, fao_clean, india}; protocol in {random, group, group_state, forward}.
Writes results/c02_<dataset>_<protocol>.json (one file per parallel run)."""
import sys, json, time
from crop_common import *

ds, proto = sys.argv[1], sys.argv[2]
if ds.startswith("fao"):
    d = load_fao(clean=(ds == "fao_clean")); X = design_fao(d)
    gcol = {"group": "country", "group_state": "country"}
else:
    d = load_india(True); X = design_india(d)
    gcol = {"group": "dist_id", "group_state": "state"}
X = X.values.astype(float); y = d["ly"].values; n = len(y)
if proto == "random":
    splits = list(split_random(n))
elif proto.startswith("group"):
    splits = list(split_group(d[gcol[proto]].values))
else:
    splits = list(split_forward(d["year"].values))

models = ["ridge", "gbm", "rf"]
MAXTR = {"rf": 40000}  # subsample training set for RF on the big India set
rows = []
for lab, tr, te in splits:
    for m in models:
        t0 = time.time(); rng = np.random.RandomState(0)
        tri = tr if len(tr) <= MAXTR.get(m, 10**9) else rng.choice(tr, MAXTR[m], replace=False)
        mod = make_model(m).fit(X[tri], y[tri])
        r = metrics(y[te], mod.predict(X[te]))
        r.update(split=lab, model=m, n_train=int(len(tri)), n_test=int(len(te)),
                 sec=round(time.time() - t0, 1))
        rows.append(r); print(ds, proto, r, flush=True)
json.dump(rows, open(os.path.join(RES, f"c02_{ds}_{proto}.json"), "w"), indent=1)

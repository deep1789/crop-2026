"""Usage: python c08_conformal_ext.py <setting>   setting: fao | india_district | india_state
Split / cross conformal under group shift, 6 calibration schemes, alpha in {.05,.1,.2}:
  naive    rows of fit groups (random 30% held back)
  group    whole calibration groups disjoint from fit groups
  diffnorm group + residual-scale model sigma(x) trained on out-of-group residuals (locally weighted CP)
  dist     group + residual scale a+b*d, d = kNN distance of the group's covariate profile to fit groups
  wcp      group + density-ratio weights from a cal-vs-test domain classifier (weighted CP)
  groupcv  cross-conformal: out-of-group residuals from 5 group-folds over all training groups
Also stores the group-level applicability diagnostic (distance d vs group error)."""
import sys, json
from lightgbm import LGBMClassifier, LGBMRegressor
from scipy.stats import norm, spearmanr
from crop_common import *

st = sys.argv[1]; ALPHAS = [0.05, 0.1, 0.2]
if st == "fao":
    d = load_fao(True); Xdf = design_fao(d); G = d.country.values; seeds = range(5)
elif st == "india_district":
    d = load_india(True); Xdf = design_india(d); G = d.dist_id.values; seeds = range(3)
else:
    d = load_india(True); Xdf = design_india(d); G = d.state.values; seeds = range(3)
cols = list(Xdf.columns); X = Xdf.values.astype(float); y = d.ly.values
nonyear = [i for i, c in enumerate(cols) if c != "year"]
Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
prof = pd.DataFrame(Xs[:, nonyear]).groupby(pd.Series(G).values).mean()

def gbm(seed): return LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, n_jobs=1, random_state=seed, verbose=-1)
def qhat(s, a):
    k = int(np.ceil((len(s) + 1) * (1 - a))); return np.sort(s)[min(k, len(s)) - 1]
def wq(s, w, a, wt):
    o = np.argsort(s); s, w = s[o], w[o]; c = np.cumsum(w) / (w.sum() + wt)
    i = np.searchsorted(c, 1 - a); return s[i] if i < len(s) else np.inf
def gdist(gs, ref, k=5):
    A = prof.loc[gs].values; B = prof.loc[ref].values
    D = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)); return pd.Series(np.sort(D, 1)[:, :min(k, len(ref))].mean(1), index=gs)
def rowdist(idx, ref): u = pd.unique(G[idx]); return gdist(np.asarray(u, dtype=object), ref).reindex(G[idx]).values

rows, diag = [], []
def record(method, seed, lab, te, pred_te, half):  # half: dict alpha -> array or scalar
    r = np.abs(y[te] - pred_te)
    for a in ALPHAS:
        h = half[a] if np.ndim(half[a]) else np.full(len(te), half[a])
        cov = r <= h; gc = pd.Series(cov).groupby(G[te]).mean()
        rows.append(dict(setting=st, method=method, alpha=a, seed=seed, split=lab, coverage=float(cov.mean()),
                         width=float(2 * np.mean(np.minimum(h, 50))), mean_group_cov=float(gc.mean()), sd_group_cov=float(gc.std()),
                         frac_groups_below_nom_minus10=float((gc < 1 - a - 0.10).mean()), p10_group_cov=float(gc.quantile(0.10)),
                         n_groups=int(len(gc)), rho=float(np.sqrt(np.mean(r ** 2))), ))
for seed in seeds:
    for lab, tr, te in split_group(G, 5, seed):
        rng = np.random.RandomState(seed)
        trg = np.asarray(pd.unique(G[tr]), dtype=object); rng.shuffle(trg)
        calg = set(trg[:max(2, int(0.3 * len(trg)))]); is_cal = np.array([g in calg for g in G[tr]])
        fi, ci = tr[~is_cal], tr[is_cal]
        # naive
        u = rng.rand(len(tr)); fn, cn = tr[u >= 0.3], tr[u < 0.3]; mn = gbm(seed).fit(X[fn], y[fn])
        rc = np.abs(y[cn] - mn.predict(X[cn])); record("naive", seed, lab, te, mn.predict(X[te]), {a: qhat(rc, a) for a in ALPHAS})
        # group
        mg = gbm(seed).fit(X[fi], y[fi]); pc, pt = mg.predict(X[ci]), mg.predict(X[te]); rc = np.abs(y[ci] - pc)
        record("group", seed, lab, te, pt, {a: qhat(rc, a) for a in ALPHAS})
        # diffnorm: OOF residuals within fit groups -> sigma model
        oof = np.zeros(len(fi)); fg = G[fi]
        for _, a_, b_ in split_group(fg, 3, seed):
            oof[b_] = np.abs(y[fi][b_] - gbm(seed).fit(X[fi][a_], y[fi][a_]).predict(X[fi][b_]))
        sm = LGBMRegressor(n_estimators=150, learning_rate=0.05, num_leaves=15, min_child_samples=50, n_jobs=1, random_state=seed, verbose=-1).fit(X[fi], oof)
        fl = 0.1 * oof.mean(); sc_c = np.maximum(sm.predict(X[ci]), fl); sc_t = np.maximum(sm.predict(X[te]), fl)
        record("diffnorm", seed, lab, te, pt, {a: qhat(rc / sc_c, a) * sc_t for a in ALPHAS})
        # dist
        fgs = np.asarray(pd.unique(G[fi]), dtype=object)
        dc, dt = rowdist(ci, fgs), rowdist(te, fgs); b, a0 = np.polyfit(dc, rc, 1); a0 = max(a0, 1e-3)
        uf = lambda dd: np.maximum(a0 + b * dd, 0.05 * rc.mean())
        record("dist", seed, lab, te, pt, {a: qhat(rc / uf(dc), a) * uf(dt) for a in ALPHAS})
        # applicability diagnostic: group-level distance vs group MAE (test groups)
        mae = pd.Series(np.abs(y[te] - pt)).groupby(G[te]).mean(); dg = gdist(np.asarray(mae.index, dtype=object), fgs)
        for g in mae.index: diag.append(dict(setting=st, seed=seed, split=lab, group=str(g), d=float(dg[g]), mae=float(mae[g]),
                                             sigma=float(sc_t[G[te] == g].mean())))
        # wcp
        Xd = np.vstack([X[ci], X[te]]); yd = np.r_[np.zeros(len(ci)), np.ones(len(te))]
        clf = LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=15, n_jobs=1, random_state=seed, verbose=-1).fit(Xd, yd)
        p = np.clip(clf.predict_proba(X[ci])[:, 1], 1e-3, 1 - 1e-3); w = np.clip((p / (1 - p)) * len(ci) / len(te), 0.05, 20)
        record("wcp", seed, lab, te, pt, {a: wq(rc, w, a, w.mean()) for a in ALPHAS})
        # groupcv (cross-conformal on all training groups)
        oofr = np.zeros(len(tr)); ptes = []
        for _, a_, b_ in split_group(G[tr], 5, seed):
            mk = gbm(seed).fit(X[tr][a_], y[tr][a_]); oofr[b_] = np.abs(y[tr][b_] - mk.predict(X[tr][b_])); ptes.append(mk.predict(X[te]))
        record("groupcv", seed, lab, te, np.mean(ptes, 0), {a: qhat(oofr, a) for a in ALPHAS})
        print(st, seed, lab, "done", flush=True)
json.dump(rows, open(os.path.join(RES, f"c08_{st}.json"), "w")); json.dump(diag, open(os.path.join(RES, f"c08_diag_{st}.json"), "w"))

"""Shared loading, cleaning, models and split generators for Paper 2."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np, pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
RES = os.path.join(ROOT, "results")
os.makedirs(RES, exist_ok=True)

FAO_KEY = ["country", "crop", "year"]
FAO_NUM = ["rain", "pest", "temp"]


def load_fao(clean=False):
    """FAO yield_df. clean=True collapses repeated country-crop-year rows
    (identical yield, differing avg_temp) to one record with mean temperature."""
    d = pd.read_csv(os.path.join(DATA, "fao", "yield_df.csv"), index_col=0)
    d.columns = ["country", "crop", "year", "yield", "rain", "pest", "temp"]
    d["ly"] = np.log(d["yield"])
    if clean:
        d = (d.groupby(FAO_KEY, as_index=False)
               .agg({"yield": "first", "ly": "first", "rain": "first",
                     "pest": "first", "temp": "mean"}))
    return d.reset_index(drop=True)


def load_india(clean=True, min_rows=20):
    d = pd.read_csv(os.path.join(DATA, "india", "crop_production.csv"))
    d.columns = ["state", "district", "year", "season", "crop", "area", "prod"]
    for c in ["state", "district", "season", "crop"]:
        d[c] = d[c].str.strip()
    n0 = len(d)
    if not clean:
        return d
    d = d.dropna(subset=["prod"])
    d = d[(d.area > 0) & (d["prod"] > 0)].copy()
    d["yield"] = d["prod"] / d["area"]
    d["ly"] = np.log(d["yield"])
    vc = d.crop.value_counts()
    d = d[d.crop.isin(vc[vc >= min_rows].index)]
    lo, hi = d.ly.quantile([0.001, 0.999])
    d = d[(d.ly >= lo) & (d.ly <= hi)]
    d["dist_id"] = d.state + "|" + d.district
    d.attrs["n_raw"] = n0
    return d.reset_index(drop=True)


def icc_oneway(y, g):
    """ANOVA ICC(1) of y by group g."""
    y = np.asarray(y, float); g = pd.factorize(g)[0]
    k = g.max() + 1; n = len(y)
    cnt = np.bincount(g); mean_g = np.bincount(g, y) / cnt
    gm = y.mean()
    msb = (cnt * (mean_g - gm) ** 2).sum() / (k - 1)
    msw = ((y - mean_g[g]) ** 2).sum() / (n - k)
    n0 = (n - (cnt ** 2).sum() / n) / (k - 1)
    return float((msb - msw) / (msb + (n0 - 1) * msw))


# ---------- design matrices ----------
def design_fao(d, cols=("year", "rain", "pest", "temp")):
    X = pd.get_dummies(d["crop"]).astype(float)
    for c in cols:
        X[c] = d[c].values
    return X


def design_india(d):
    X = pd.get_dummies(d[["crop", "season"]]).astype(float)
    X["year"] = d["year"].values
    X["log_area"] = np.log(d["area"].values)
    return X


def make_model(name, seed=0):
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from lightgbm import LGBMRegressor
    if name == "ridge":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    if name == "rf":
        return RandomForestRegressor(200, min_samples_leaf=2, n_jobs=1, random_state=seed)
    if name == "gbm":
        return LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31,
                             n_jobs=1, random_state=seed, verbose=-1)
    raise ValueError(name)


# ---------- split generators: yield (label, train_idx, test_idx) ----------
def split_random(n, k=5, seed=0):
    rng = np.random.RandomState(seed)
    f = rng.randint(0, k, n)
    for i in range(k):
        yield f"fold{i}", np.where(f != i)[0], np.where(f == i)[0]


def split_group(groups, k=5, seed=0):
    """Group-held-out K-fold: every group lands wholly in one test fold."""
    rng = np.random.RandomState(seed)
    u = np.asarray(pd.unique(groups), dtype=object); rng.shuffle(u)
    fold = {g: i % k for i, g in enumerate(u)}
    f = np.array([fold[g] for g in groups])
    for i in range(k):
        yield f"fold{i}", np.where(f != i)[0], np.where(f == i)[0]


def split_forward(years, n_test_years=3, n_steps=3):
    ys = np.sort(np.unique(years)); last = ys[-1]
    for s in range(n_steps):
        hi = last - s * n_test_years
        te = (years > hi - n_test_years) & (years <= hi)
        yield f"to{hi}", np.where(years <= hi - n_test_years)[0], np.where(te)[0]


def metrics(y, p):
    r = y - p
    return {"rmse": float(np.sqrt(np.mean(r ** 2))), "mae": float(np.mean(np.abs(r))),
            "r2": float(1 - np.sum(r ** 2) / np.sum((y - y.mean()) ** 2))}

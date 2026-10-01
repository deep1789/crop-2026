"""Consolidate all results into results/summary.json and results/tables.md (bootstrap 95% CIs over folds*seeds)."""
import json, glob
from scipy.stats import spearmanr
from crop_common import *
R = lambda f: json.load(open(os.path.join(RES, f)))
rng = np.random.RandomState(0)
def ci(x, B=2000):
    x = np.asarray(x, float); bs = [rng.choice(x, len(x)).mean() for _ in range(B)]; return float(x.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
def fmt(t, p=3): return f"{t[0]:.{p}f} [{t[1]:.{p}f}, {t[2]:.{p}f}]"
out, md = {}, []
# ---- audit
a, o = R("audit.json"), R("audit_origin.json"); out["audit"] = {**a, "origin": o}
# ---- transfer baselines
b = pd.concat([pd.DataFrame(R(f)) for f in glob.glob(os.path.join(RES, "c07_*.json"))])
tab = {}
for (ds, pr, m), g in b.groupby(["dataset", "proto", "model"]):
    tab[f"{ds}|{pr}|{m}"] = {"r2": ci(g.r2), "rmse": ci(g.rmse)}
out["baselines"] = tab
md.append("## Transfer: R2 (95% CI) by dataset, protocol, model\n")
for ds in ["fao_clean", "india"]:
    md.append(f"\n**{ds}**\n\n| model | " + " | ".join(sorted(b[b.dataset == ds].proto.unique())) + " |\n|---|" + "---|" * b[b.dataset == ds].proto.nunique())
    for m in ["crop_mean", "ridge", "rf", "gbm", "gbm_tuned", "gbm_id"]:
        md.append(f"| {m} | " + " | ".join(fmt(tab[f'{ds}|{p}|{m}']['r2']) for p in sorted(b[b.dataset == ds].proto.unique())) + " |")
# ---- conformal
c = pd.concat([pd.DataFrame(R(f"c08_{s}.json")) for s in ["fao", "india_district", "india_state"]])
cf = {}
for (s, m, al), g in c.groupby(["setting", "method", "alpha"]):
    cf[f"{s}|{m}|{al}"] = {k: ci(g[k]) for k in ["coverage", "width", "frac_groups_below_nom_minus10", "p10_group_cov", "sd_group_cov"]}
out["conformal"] = cf
md.append("\n## Conformal (alpha=0.1): coverage, mean width, share of groups > 10 pts under nominal, 10th pct group coverage\n")
for s in ["fao", "india_state", "india_district"]:
    md.append(f"\n**{s}**\n\n| method | coverage | width | groups below nominal-10 | p10 group cov |\n|---|---|---|---|---|")
    for m in ["naive", "group", "groupcv", "diffnorm", "dist", "wcp"]:
        v = cf[f"{s}|{m}|0.1"]; md.append(f"| {m} | {fmt(v['coverage'])} | {fmt(v['width'],2)} | {fmt(v['frac_groups_below_nom_minus10'])} | {fmt(v['p10_group_cov'])} |")
# paired difference: diffnorm vs group
pd_ = {}
for s in ["fao", "india_state", "india_district"]:
    x = c[(c.setting == s) & (c.alpha == 0.1)].pivot_table(index=["seed", "split"], columns="method", values=["frac_groups_below_nom_minus10", "p10_group_cov", "width"])
    pd_[s] = {k: ci(x[k]["diffnorm"] - x[k]["group"]) for k in ["frac_groups_below_nom_minus10", "p10_group_cov", "width"]}
out["paired_diffnorm_minus_group"] = pd_
md.append("\n## Paired difference diffnorm - group (alpha=0.1)\n\n| setting | d(groups below nominal-10) | d(p10 group cov) | d(width) |\n|---|---|---|---|")
for s, v in pd_.items(): md.append(f"| {s} | {fmt(v['frac_groups_below_nom_minus10'])} | {fmt(v['p10_group_cov'])} | {fmt(v['width'],2)} |")
# ---- applicability score: group-level Spearman with bootstrap over groups
ap = {}
for s in ["fao", "india_state", "india_district"]:
    g = pd.DataFrame(R(f"c08_diag_{s}.json"))
    for k in ["d", "sigma"]:
        r0 = spearmanr(g[k], g.mae)[0]; bs = []
        for _ in range(500):
            i = rng.choice(len(g), len(g)); bs.append(spearmanr(g[k].values[i], g.mae.values[i])[0])
        ap[f"{s}|{k}"] = [float(r0), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
out["applicability_spearman"] = ap
md.append("\n## Applicability score vs group MAE (Spearman, 95% CI)\n\n| setting | distance d | learned sigma(x) |\n|---|---|---|")
for s in ["fao", "india_state", "india_district"]: md.append(f"| {s} | {fmt(ap[s+'|d'],2)} | {fmt(ap[s+'|sigma'],2)} |")
# ---- fingerprint / model-agnostic
fp = R("c09_fingerprint.json"); out["fingerprint"] = fp["fingerprint"]
mm = pd.DataFrame(fp["models"]); out["models_agnostic"] = {f"{s}|{m}": {k: ci(g[k]) for k in ["naive", "group"]} for (s, m), g in mm.groupby(["setting", "model"])}
md.append("\n## Fingerprint strength vs naive coverage (gbm, alpha=0.1)\n\n| setting | n groups | group-id accuracy (chance) | mean feature ICC | naive coverage | ridge naive | rf naive |\n|---|---|---|---|---|---|---|")
for s in ["fao", "india_state", "india_district"]:
    f = fp["fingerprint"][s]; ma = out["models_agnostic"]
    md.append(f"| {s} | {f['n_groups']} | {f['group_id_accuracy']:.3f} ({f['majority_share']:.3f}) | {f['mean_feature_icc']:.2f} | {ma[s+'|gbm']['naive'][0]:.3f} | {ma[s+'|ridge']['naive'][0]:.3f} | {ma[s+'|rf']['naive'][0]:.3f} |")
# ---- local calibration
lc = pd.concat([pd.DataFrame(R(f"c04_{s}.json")) for s in ["fao_clean", "india"] if os.path.exists(os.path.join(RES, f"c04_{s}.json"))])
out["local"] = {f"{ds}|{m}": {k: ci(g[k]) for k in ["coverage", "width", "rmse_after_shift", "frac_groups_below_80"]} for (ds, m), g in lc.groupby(["dataset", "m"])}
md.append("\n## Local labelled rows m: width and RMSE after shift\n\n| dataset | m | coverage | width | RMSE | groups < 80% |\n|---|---|---|---|---|---|")
for k, v in out["local"].items(): ds, m = k.split("|"); md.append(f"| {ds} | {m} | {v['coverage'][0]:.3f} | {v['width'][0]:.2f} | {v['rmse_after_shift'][0]:.3f} | {v['frac_groups_below_80'][0]:.3f} |")
json.dump(out, open(os.path.join(RES, "summary.json"), "w"), indent=1); open(os.path.join(RES, "tables.md"), "w").write("\n".join(md))
print("\n".join(md))

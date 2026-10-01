"""Emit manuscript tables (markdown snippets) from results/summary.json -> paper/build/tab_*.md"""
import json
from crop_common import *
S = json.load(open(os.path.join(RES, "summary.json"))); OUT = os.path.join(ROOT, "paper", "build")
f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"; f2 = lambda t: f"{t[0]:.2f} [{t[1]:.2f}, {t[2]:.2f}]"
def w(name, text): open(os.path.join(OUT, f"tab_{name}.md"), "w").write(text.rstrip() + "\n"); print("wrote", name)
A, O = S["audit"], S["audit"]["origin"]; fa = A["fao"]
rows = [("Rows in `yield_df.csv`", f"{fa['rows']:,}"), ("Distinct country–crop–year records", f"{fa['unique_records']:,}"),
        ("Rows that repeat an earlier record", f"{fa['rows']-fa['unique_records']:,} ({100*fa['frac_rows_repeating']:.1f}%)"),
        ("Rows belonging to a repeated record", f"{100*fa['frac_rows_in_repeated_keys']:.1f}%"),
        ("Records with more than one row", f"{O['repeat']['keys_with_repeats']:,}"),
        ("Distinct yields within a record (maximum)", str(O['repeat']['max_distinct_yield'])),
        ("Records whose row count equals the rows in `temp.csv` for the country-year", f"{100*O['fanout']['frac_mult_equals_n_temp_rows']:.0f}%"),
        ("Country-years in `temp.csv` with several rows", f"{100*O['temp_source']['frac_with_multiple_rows']:.0f}%"),
        ("Median within-country-year SD of temperature, against overall SD (°C)", f"{O['temp_source']['median_within_cy_std']:.2f} against {O['temp_source']['total_std']:.2f}"),
        ("Countries whose source rainfall is constant over years", f"{100*O['rain_source']['frac_constant_over_years']:.0f}% of {O['rain_source']['countries']}"),
        ("Yield equals the FAO yield table (distinct records)", f"{100*O['yield_match']['equal']:.0f}%"),
        ("ICC by country: rainfall / temperature / pesticides (distinct records)", f"{fa['icc_country_clean']['rain']:.2f} / {fa['icc_country_clean']['temp']:.3f} / {fa['icc_country_clean']['pest']:.2f}"),
        ("ICC by country: temperature / pesticides (raw rows)", f"{fa['icc_country']['temp']:.2f} / {fa['icc_country']['pest']:.2f}"),
        ("ICC of pesticides by country in the source table", f"{O['pesticide_icc']['source_country_year']:.2f}")]
w("audit", "Table: Table 4. Audit of the FAO-derived file `yield_df.csv`, traced to its component tables.\n\n| Quantity | Value |\n|:---|:---|\n" + "\n".join(f"| {a} | {b} |" for a, b in rows))
B = S["baselines"]; M = [("crop_mean", "Crop mean"), ("ridge", "Ridge"), ("rf", "Random forest"), ("gbm_tuned", "GBM (tuned)"), ("gbm_id", "GBM + group ID")]
def tr(ds, protos, names, cap, num):
    h = "| Model | " + " | ".join(names) + " |\n|:---|" + "---:|" * len(names)
    body = "\n".join(f"| {l} | " + " | ".join(f"{B[f'{ds}|{p}|{m}']['r2'][0]:.3f} ({B[f'{ds}|{p}|{m}']['r2'][1]:.3f}–{B[f'{ds}|{p}|{m}']['r2'][2]:.3f})" for p in protos) + " |" for m, l in M)
    return f"Table: Table {num}. {cap}\n\n{h}\n{body}"
w("transfer", tr("fao_clean", ["random", "forward", "group"], ["Random", "Forward in time", "Country held out"], "R² (95% bootstrap interval) on the FAO file, distinct records, by evaluation protocol.", 5) + "\n\n" +
  tr("india", ["random", "forward", "group", "group_state"], ["Random", "Forward in time", "District held out", "State held out"], "R² (95% bootstrap interval) on the Indian district table, by evaluation protocol.", 6))
C = S["conformal"]; names = {"naive": "Naive (random calibration rows)", "group": "Group", "groupcv": "Group-CV", "diffnorm": "Scaled σ(x)", "dist": "Distance", "wcp": "Weighted"}
sets = [("fao", "FAO, unseen countries"), ("india_state", "India, unseen states"), ("india_district", "India, unseen districts")]
body = []
for k, kl in sets:
    body.append(f"| **{kl}** | | | | |")
    for m, ml in names.items():
        v = C[f"{k}|{m}|0.1"]; body.append(f"| {ml} | {v['coverage'][0]:.3f} ({v['coverage'][1]:.3f}–{v['coverage'][2]:.3f}) | {v['width'][0]:.2f} | {v['frac_groups_below_nom_minus10'][0]:.3f} | {v['p10_group_cov'][0]:.3f} |")
w("conformal", "Table: Table 7. Split-conformal intervals at nominal 90% on unseen groups (gradient boosting, mean over seeds and folds; coverage with 95% bootstrap interval). Width is the mean interval width in log-yield units. Share below is the share of test groups whose coverage is more than 10 points under nominal; p10 is the 10th percentile of group coverage.\n\n| Scheme | Coverage | Width | Share below | p10 |\n|:---|---:|---:|---:|---:|\n" + "\n".join(body))
alpha = []
for k, kl in sets:
    for m in ["naive", "group", "groupcv", "diffnorm"]:
        alpha.append(f"| {kl} | {names[m]} | " + " | ".join(f"{C[f'{k}|{m}|{a}']['coverage'][0]:.3f}" for a in [0.05, 0.1, 0.2]) + " |")
w("alpha", "Table: Table 8. Coverage at nominal 95%, 90% and 80% (mean over seeds and folds).\n\n| Setting | Scheme | 0.95 | 0.90 | 0.80 |\n|:---|:---|---:|---:|---:|\n" + "\n".join(alpha))
FP, MA = S["fingerprint"], S["models_agnostic"]
fr = "\n".join(f"| {kl} | {FP[k]['n_groups']} | {FP[k]['group_id_accuracy']:.3f} ({FP[k]['majority_share']:.3f}) | {FP[k]['mean_feature_icc']:.2f} | " + " | ".join(f"{MA[f'{k}|{m}']['naive'][0]:.3f} / {MA[f'{k}|{m}']['group'][0]:.3f}" for m in ["ridge", "gbm", "rf"]) + " |" for k, kl in sets)
w("fingerprint", "Table: Table 10. Group fingerprint strength and conformal coverage by model family (naive / group calibration, nominal 90%). Group-ID accuracy is the five-nearest-neighbour accuracy of identifying the group from the features, with the largest-group share in brackets. Feature ICC is the mean intraclass correlation of the continuous features (the Indian table has one, log area). Values come from a separate two-seed run with the Indian data subsampled to 60,000 rows (651 districts present), so they differ slightly from Table 7.\n\n| Setting | Groups | Group-ID accuracy | Feature ICC | Ridge | GBM | Random forest |\n|:---|---:|:---|---:|:---|:---|:---|\n" + fr)
P = S["paired_diffnorm_minus_group"]
w("paired", "Table: Table 12. Paired difference between scaled and plain group calibration at nominal 90% (scaled minus group; mean over seeds and folds with 95% bootstrap interval).\n\n| Setting | Share below | p10 group coverage | Width |\n|:---|---:|---:|---:|\n" + "\n".join(f"| {kl} | {f3(P[k]['frac_groups_below_nom_minus10'])} | {f3(P[k]['p10_group_cov'])} | {f2(P[k]['width'])} |" for k, kl in sets))
RB = json.load(open(os.path.join(RES, "c13_robustness.json"))); AP = RB["applicability_cluster"]
w("app", "Table: Table 13. Spearman correlation between a group-level score and the group's mean absolute error. Scores and errors are averaged over seeds and folds for each group, and the 95% interval is a bootstrap over groups.\n\n| Setting | Groups | Distance score d | Learned scale σ(x) |\n|:---|---:|:---|:---|\n" + "\n".join(f"| {kl} | {AP[k+'|d'][3]} | {f2(AP[k+'|d'][:3])} | {f2(AP[k+'|sigma'][:3])} |" for k, kl in sets))
D = pd.DataFrame(json.load(open(os.path.join(RES, "c13b_wcp_diag.json")))).groupby("cal").mean(numeric_only=True)
lab = {"naive": "Naive calibration rows (seen groups)", "group": "Calibration groups (unseen)"}
w("wcp", "Table: Table 11. Weighted conformal diagnostics on FAO (domain classifier separating calibration rows from test rows; cross-fitted weights). AUC is the cross-validated classifier AUC; ESS is the effective sample size as a share of the calibration rows; clipping is at 0.05 and 20.\n\n| Calibration set weighted | AUC | ESS, unclipped | ESS, clipped | Share of weights below 0.05 | Coverage, unweighted | Coverage, weighted |\n|:---|---:|---:|---:|---:|---:|---:|\n" + "\n".join(f"| {lab[k]} | {D.loc[k,'auc']:.3f} | {D.loc[k,'ess_unclipped']:.3f} | {D.loc[k,'ess_clipped']:.3f} | {D.loc[k,'frac_clip_lo']:.3f} | {D.loc[k,'cov_unweighted']:.3f} | {D.loc[k,'cov_weighted']:.3f} |" for k in ["naive", "group"]))
FF = json.load(open(os.path.join(RES, "c14_fingerprint_free.json"))); PC = FF["point_ci"]
mods = [("crop_mean", "Crop mean"), ("country_crop_mean", "Country–crop mean (lookup)"), ("ridge_anomaly", "Ridge, anomaly features"), ("gbm_anomaly", "GBM, anomaly features"), ("gbm_full", "GBM, full features"), ("cc_mean_plus_gbm_anomaly", "Lookup + GBM on anomalies")]
rows = "\n".join(f"| {l} | " + " | ".join(f"{PC[f'{p}|{m}']['rmse'][0]:.3f} ({PC[f'{p}|{m}']['r2'][0]:.3f})" for p in ["random", "forward", "group"]) + " |" for m, l in mods)
CI = FF["coverage_ci"]; fpid = FF["fingerprint_id_acc"]
cr = "\n".join(f"| {fs} | {fpid[fs]:.3f} | {CI[fs+'|naive'][0]:.3f} | {CI[fs+'|group'][0]:.3f} | {CI[fs+'|naive_width'][0]:.2f} | {CI[fs+'|group_width'][0]:.2f} |" for fs in ["full", "anomaly"])
w("free", "Table: Table 15. Place lookups and fingerprint-free features on the FAO file (distinct records). Upper block: RMSE of log-yield (R² in brackets) by protocol. Lower block: conformal coverage on unseen countries at nominal 90% with each feature set (gradient boosting; a separate three-seed run, so naive coverage with full features is 0.602 against 0.598 in Table 7).\n\n| Model | Random | Forward in time | Country held out |\n|:---|:---|:---|:---|\n" + rows + "\n\n| Features | Group-ID accuracy | Naive coverage | Group coverage | Naive width | Group width |\n|:---|---:|---:|---:|---:|---:|\n" + cr)
L = S["local"]
w("local", "Table: Table 14. Effect of m labelled local rows per test group (nominal 90%; mean over seeds and folds). The m = 0 rows differ slightly from the group scheme of Table 7 because the runs use different random draws.\n\n| Dataset | m | Coverage | Width | RMSE after shift | Share of groups below 80% |\n|:---|---:|---:|---:|---:|---:|\n" + "\n".join(f"| {dl} | {m} | {L[f'{ds}|{m}']['coverage'][0]:.3f} | {L[f'{ds}|{m}']['width'][0]:.2f} | {L[f'{ds}|{m}']['rmse_after_shift'][0]:.3f} | {L[f'{ds}|{m}']['frac_groups_below_80'][0]:.3f} |" for ds, dl in [("fao_clean", "FAO"), ("india", "India districts")] for m in [0, 1, 3, 5, 10, 20]))

# ---- simulation table and RMSE appendix table
sim = pd.DataFrame(json.load(open(os.path.join(RES, "c05_law_sim.json"))))
g = sim.groupby(["tau", "n_per", "calib"])[["coverage", "law", "rho"]].mean().reset_index()
lines = []
for tau in sorted(g.tau.unique()):
    for n in [10, 50]:
        a = g[(g.tau == tau) & (g.n_per == n) & (g.calib == "naive")].iloc[0]; b = g[(g.tau == tau) & (g.n_per == n) & (g.calib == "group")].iloc[0]
        lines.append(f"| {tau:g} | {n} | {a.rho:.2f} | {a.coverage:.3f} | {a.law:.3f} | {b.coverage:.3f} |")
w("sim", "Table: Table 9. Simulation check of the coverage relation (nominal 90%; mean over 20 replicates). τ is the SD of group effects relative to unit noise; n is the number of rows per group; ρ is the measured ratio of test to calibration residual scale under naive calibration.\n\n| τ | n | ρ (naive) | Naive coverage | Eq. (5) | Group coverage |\n|---:|---:|---:|---:|---:|---:|\n" + "\n".join(lines))
def trm(ds, protos, names, cap, num):
    h = "| Model | " + " | ".join(names) + " |\n|:---|" + "---:|" * len(names)
    body = "\n".join(f"| {l} | " + " | ".join(f"{B[f'{ds}|{p}|{m}']['rmse'][0]:.3f}" for p in protos) + " |" for m, l in M)
    return f"Table: Table {num}. {cap}\n\n{h}\n{body}"
w("rmse", trm("fao_clean", ["random", "forward", "group"], ["Random", "Forward in time", "Country held out"], "RMSE of log-yield, FAO file (distinct records), mean over seeds and folds.", "B1") + "\n\n" +
  trm("india", ["random", "forward", "group", "group_state"], ["Random", "Forward in time", "District held out", "State held out"], "RMSE of log-yield, Indian district table, mean over seeds and folds.", "B2"))

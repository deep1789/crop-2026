"""Figures for the manuscript -> paper/figures/figNN_*.png (300 dpi)."""
import json, glob
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm
from crop_common import *

F = os.path.join(ROOT, "paper", "figures"); os.makedirs(F, exist_ok=True)
C = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", violet="#4a3aa7", magenta="#e87ba4", green="#008300", yellow="#eda100", red="#e34948")
INK, MUT, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUT, "axes.labelcolor": INK, "xtick.color": MUT, "ytick.color": MUT,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.7, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5,
                     "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300, "figure.dpi": 150})
R = lambda f: json.load(open(os.path.join(RES, f)))
S = R("summary.json"); Zc = norm.ppf(0.95)
def tag(ax, s): ax.text(-0.02, 1.06, s, transform=ax.transAxes, fontsize=10, fontweight="bold", ha="right", va="bottom")
def save(fig, n): fig.savefig(os.path.join(F, n), bbox_inches="tight", facecolor="white"); plt.close(fig); print("saved", n)

# ---- Fig 2: audit
raw = load_fao(False); o = R("audit_origin.json")
mult = raw.groupby(FAO_KEY).size().value_counts().sort_index()
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.5), gridspec_kw={"width_ratios": [1.15, 1, 1]})
ax[0].bar(mult.index.astype(str), mult.values, color=C["blue"], width=0.7); ax[0].tick_params(axis="x", labelsize=7); ax[0].set_xlabel("rows per country–crop–year record"); ax[0].set_ylabel("records")
ax[0].set_yscale("log"); tag(ax[0], "a")
nt = raw.groupby(FAO_KEY).size().rename("m").reset_index().merge(pd.read_csv(os.path.join(DATA, "fao", "temp.csv")).groupby(["country", "year"]).size().rename("n").reset_index(), left_on=["country", "year"], right_on=["country", "year"])
ax[1].scatter(nt.n + np.random.RandomState(0).uniform(-.15, .15, len(nt)), nt.m, s=6, color=C["orange"], alpha=.4, linewidths=0)
mx = max(nt.n.max(), nt.m.max()); ax[1].plot([0, mx], [0, mx], color=MUT, lw=0.8, ls="--")
ax[1].set_xlabel("rows in temp.csv for the country-year"); ax[1].set_ylabel("rows in yield_df for the record"); tag(ax[1], "b")
icc = S["audit"]["fao"]["icc_country_clean"]; names = ["rainfall", "temperature", "pesticides"]; vals = [icc["rain"], icc["temp"], icc["pest"]]
ax[2].barh(names + ["log-yield"], vals + [S["audit"]["fao"]["icc_logyield_country_crop_clean"]], color=[C["aqua"]] * 3 + [C["violet"]], height=0.55)
for i, v in enumerate(vals + [S["audit"]["fao"]["icc_logyield_country_crop_clean"]]): ax[2].text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=8, color=INK)
ax[2].set_xlim(0, 1.15); ax[2].set_xlabel("intraclass correlation by country"); ax[2].invert_yaxis(); ax[2].grid(axis="y", visible=False); tag(ax[2], "c")
fig.tight_layout(); save(fig, "fig02_audit.png")

# ---- Fig 3: transfer
b = S["baselines"]; models = ["crop_mean", "ridge", "rf", "gbm_tuned", "gbm_id"]; lab = ["crop mean", "ridge", "random forest", "GBM (tuned)", "GBM + group ID"]
cols = [MUT, C["aqua"], C["orange"], C["blue"], C["violet"]]
panels = [("fao_clean", ["random", "forward", "group"], ["random", "forward\nin time", "country\nheld out"], "FAO (cleaned)"),
          ("india", ["random", "forward", "group", "group_state"], ["random", "forward\nin time", "district\nheld out", "state\nheld out"], "India")]
fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [3, 4]})
for ax, (ds, pr, pl, ttl) in zip(axes, panels):
    w = 0.16
    for k, (m, l, c) in enumerate(zip(models, lab, cols)):
        x = np.arange(len(pr)) + (k - 2) * w; y = [b[f"{ds}|{p}|{m}"]["r2"] for p in pr]
        ax.bar(x, [v[0] for v in y], w * 0.88, color=c, label=l if ds == "fao_clean" else None,
               yerr=[[v[0] - v[1] for v in y], [v[2] - v[0] for v in y]], error_kw=dict(lw=0.7, capsize=1.5, ecolor=INK))
    ax.set_xticks(range(len(pr))); ax.set_xticklabels(pl); ax.set_ylabel("R² (95% CI)"); ax.set_ylim(0, 1.0); ax.set_title(ttl, fontsize=9, loc="left"); ax.grid(axis="x", visible=False)
h, l_ = axes[0].get_legend_handles_labels(); fig.legend(h, l_, loc="lower center", ncol=5, fontsize=7.5, bbox_to_anchor=(0.5, -0.03)); tag(axes[0], "a"); tag(axes[1], "b")
fig.tight_layout(rect=(0, 0.07, 1, 1)); save(fig, "fig03_transfer.png")

# ---- Fig 4: coverage collapse and the law
sim = pd.DataFrame(R("c05_law_sim.json")); fp = S["fingerprint"]; mg = S["models_agnostic"]
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.6), gridspec_kw={"width_ratios": [1.1, 1, 1.1]})
rr = np.linspace(0.8, 3.4, 100); ax[0].plot(rr, 2 * norm.cdf(Zc / rr) - 1, color=INK, lw=1.2, label=r"$2\Phi(z/\rho)-1$")
s = sim[sim.calib == "naive"].groupby(["tau", "n_per"])[["rho", "coverage"]].mean().reset_index()
ax[0].scatter(s.rho, s.coverage, s=14, color=C["blue"], label="simulation", zorder=3, linewidths=0)
cc = pd.concat([pd.DataFrame(R(f"c08_{k}.json")) for k in ["fao", "india_state", "india_district"]]); cc = cc[(cc.alpha == 0.1) & (cc.method == "naive")]
# implied rho from the naive coverage per setting
for st, col, nm in [("fao", C["orange"], "FAO"), ("india_state", C["violet"], "India states"), ("india_district", C["aqua"], "India districts")]:
    cv = cc[cc.setting == st].coverage.mean(); rho = Zc / norm.ppf((1 + cv) / 2); ax[0].scatter([rho], [cv], marker="D", s=30, color=col, zorder=4, label=nm, linewidths=0)
ax[0].axhline(0.9, color=MUT, lw=0.7, ls=":"); ax[0].set_xlabel(r"inflation ratio $\rho$"); ax[0].set_ylabel("actual coverage (nominal 0.90)"); ax[0].legend(fontsize=6.8, loc="upper right"); tag(ax[0], "a")
names = ["FAO\ncountries", "India\nstates", "India\ndistricts"]; keys = ["fao", "india_state", "india_district"]; w = 0.26
for j, (m, c, l) in enumerate([("ridge", C["aqua"], "ridge"), ("gbm", C["blue"], "GBM"), ("rf", C["orange"], "random forest")]):
    ax[1].bar(np.arange(3) + (j - 1) * w, [mg[f"{k}|{m}"]["naive"][0] for k in keys], w * 0.9, color=c, label=l)
ax[1].axhline(0.9, color=MUT, lw=0.7, ls=":"); ax[1].set_xticks(range(3)); ax[1].set_xticklabels(names); ax[1].set_ylim(0.3, 1.0); ax[1].set_ylabel("naive coverage"); ax[1].legend(fontsize=6.8, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.14), columnspacing=0.8, handlelength=1.0); ax[1].grid(axis="x", visible=False); tag(ax[1], "b")
acc = [fp[k]["group_id_accuracy"] for k in keys]; cov = [mg[f"{k}|gbm"]["naive"][0] for k in keys]
for a_, c_, k, col in zip(acc, cov, names, [C["orange"], C["violet"], C["aqua"]]):
    ax[2].scatter(a_, c_, s=55, color=col, zorder=3, linewidths=0); ax[2].annotate(k.replace("\n", " "), (a_, c_), textcoords="offset points", xytext=(6, 4), fontsize=7)
ax[2].set_xscale("symlog", linthresh=0.02); ax[2].set_xlim(0, 1.0); ax[2].set_ylim(0.5, 0.95); ax[2].axhline(0.9, color=MUT, lw=0.7, ls=":")
ax[2].set_xlabel("group-ID accuracy from features"); ax[2].set_ylabel("naive coverage (GBM)"); tag(ax[2], "c")
fig.tight_layout(); save(fig, "fig04_collapse.png")

# ---- Fig 5: conformal methods
cf = S["conformal"]; meths = ["naive", "group", "groupcv", "diffnorm", "dist", "wcp"]; ml = ["naive", "group", "group-CV", "scaled σ(x)", "distance", "weighted"]
mc = [MUT, C["blue"], C["aqua"], C["orange"], C["violet"], C["magenta"]]
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.7))
for j, (k, kl) in enumerate(zip(keys, ["FAO countries", "India states", "India districts"])):
    pass
for i, (met, key, yl) in enumerate([("p10_group_cov", "p10_group_cov", "10th-percentile group coverage"), ("frac_groups_below_nom_minus10", "frac", "groups >10 pts below nominal"), ("width", "w", "mean interval width (log-yield units)")]):
    for j, (m, l, c) in enumerate(zip(meths, ml, mc)):
        x = np.arange(3) + (j - 2.5) * 0.14; v = [cf[f"{k}|{m}|0.1"][met] for k in keys]
        ax[i].bar(x, [t[0] for t in v], 0.125, color=c, label=l if i == 0 else None, yerr=[[t[0] - t[1] for t in v], [t[2] - t[0] for t in v]], error_kw=dict(lw=0.6, capsize=1, ecolor=INK))
    ax[i].set_xticks(range(3)); ax[i].set_xticklabels(["FAO\ncountries", "India\nstates", "India\ndistricts"]); ax[i].set_ylabel(yl); ax[i].grid(axis="x", visible=False); tag(ax[i], "abc"[i])
ax[0].set_ylim(0.2, 0.9); h, l_ = ax[0].get_legend_handles_labels(); fig.legend(h, l_, loc="lower center", ncol=6, fontsize=7.5, bbox_to_anchor=(0.5, -0.04)); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "fig05_methods.png")

# ---- Fig 6: applicability
fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.5))
for a, k, nm in zip(ax, keys, ["FAO countries", "India states", "India districts"]):
    g = pd.DataFrame(R(f"c08_diag_{k}.json")); a.scatter(g.sigma, g.mae, s=5, color=C["blue"], alpha=.35, linewidths=0)
    a.set_xlabel("predicted residual scale σ(x)"); a.set_ylabel("group mean absolute error")
    sp = S["applicability_spearman"][f"{k}|sigma"]; a.set_title(f"{nm}: Spearman {sp[0]:.2f}", fontsize=8.5, loc="left")
fig.tight_layout(); [tag(a, "abc"[i]) for i, a in enumerate(ax)]; save(fig, "fig06_applicability.png")

# ---- Fig 7: local calibration
lc = S["local"]; ms = [0, 1, 3, 5, 10, 20]
fig, ax = plt.subplots(1, 2, figsize=(6.2, 2.5))
for ds, c, l in [("fao_clean", C["orange"], "FAO countries"), ("india", C["aqua"], "India districts")]:
    ax[0].plot(ms, [lc[f"{ds}|{m}"]["width"][0] for m in ms], "o-", color=c, lw=1.4, ms=4, label=l)
    ax[1].plot(ms, [lc[f"{ds}|{m}"]["rmse_after_shift"][0] for m in ms], "o-", color=c, lw=1.4, ms=4, label=l)
ax[0].set_ylabel("mean 90% interval width"); ax[1].set_ylabel("RMSE after local shift"); [a.set_xlabel("labelled local rows m") for a in ax]; ax[0].legend(fontsize=7); tag(ax[0], "a"); tag(ax[1], "b")
fig.tight_layout(); save(fig, "fig07_local.png")

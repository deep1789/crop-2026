"""Simulation of the coverage-collapse law: actual coverage ~ 2*Phi(z/rho)-1, rho = test/cal residual scale.
Groups have random effects u_g ~ N(0,tau^2); the model memorises training-group means.
Naive calibration uses residuals on seen groups; group-aware uses unseen calibration groups."""
import json
from scipy.stats import norm
from crop_common import *

rng = np.random.RandomState(0); ALPHA = 0.1; Z = norm.ppf(1 - ALPHA / 2)
def qhat(s):
    k = int(np.ceil((len(s) + 1) * (1 - ALPHA))); return np.sort(s)[min(k, len(s)) - 1]
rows = []
for tau in [0, .25, .5, 1, 1.5, 2, 3]:
  for n_per in [10, 50]:
    for rep in range(20):
        sig = 1.0; ng = 60
        def grp(n):  # returns group effects and noisy outcomes (signal part known: 0)
            u = rng.randn(n) * tau; return u, u[:, None] + sig * rng.randn(n, n_per)
        u_tr, y_tr = grp(ng)                       # fit groups
        mu = y_tr.mean(1)                          # model memorises group means (seen-group predictor)
        half = n_per // 2
        # naive: calibrate on held-out rows of seen groups (second half), fit on first half
        mu_h = y_tr[:, :half].mean(1); rc_naive = np.abs(y_tr[:, half:] - mu_h[:, None]).ravel()
        # group-aware: unseen calibration groups predicted by the population mean (0)
        _, y_cal = grp(ng); rc_group = np.abs(y_cal).ravel()
        _, y_te = grp(ng); rt = np.abs(y_te).ravel()   # test groups also unseen -> prediction 0
        rho = np.sqrt(np.mean(rt**2) / np.mean(rc_naive**2))
        for name, rc in [("naive", rc_naive), ("group", rc_group)]:
            q = qhat(rc); rho_c = np.sqrt(np.mean(rt**2) / np.mean(rc**2))
            rows.append(dict(tau=tau, n_per=n_per, calib=name, coverage=float((rt <= q).mean()),
                             rho=float(rho_c), law=float(2 * norm.cdf(Z / rho_c) - 1)))
d = pd.DataFrame(rows); s = d.groupby(["tau", "n_per", "calib"])[["coverage", "law", "rho"]].mean().round(3)
print(s.to_string()); print("max |cov-law|:", float((d.coverage - d.law).abs().max()))
json.dump(rows, open(os.path.join(RES, "c05_law_sim.json"), "w"))

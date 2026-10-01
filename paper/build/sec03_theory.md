# Theory: leakage, calibration and the coverage-collapse relation

This section links the inflation of point accuracy under random splits, studied in the companion paper [@paper1], to the coverage of split conformal intervals. Section 3.1 fixes notation, Section 3.2 recalls the inflation ratio, Section 3.3 derives the coverage-collapse relation, Section 3.4 states when group-aware calibration is valid and why per-group coverage still varies, and Section 3.5 describes why model family matters. Derivations are in Appendix A and checks against simulation and data in Section 6. Table 2 lists the notation.

Table: Table 2. Notation.

| Symbol | Meaning |
|:---|:---|
| $g$, $G$ | Group (country, state or district) and number of groups |
| $y_{gj}$, $x_{gj}$ | Log-yield and features of row $j$ in group $g$ |
| $f$, $u_g$, $\varepsilon_{gj}$ | Shared signal, group offset, row noise; variances $\sigma_u^2$, $\sigma_\varepsilon^2$ |
| $r$ | Intraclass correlation of the residual, $r=\sigma_u^2/(\sigma_u^2+\sigma_\varepsilon^2)$ |
| $\rho$ | Inflation ratio: root-mean-square residual on test rows divided by that on calibration rows |
| $\alpha$, $z_{1-\alpha/2}$ | Miscoverage level and normal quantile |
| $\hat q$ | Conformal quantile of calibration scores |
| $\Phi$ | Standard normal distribution function |
| $c_g$ | Coverage of the interval within group $g$ |
| $\hat\sigma(x)$ | Learned residual scale used for normalised scores |

## Setting

Rows are indexed by group $g$ and position $j$ within the group, and we assume the random-effects structure

$$y_{gj} = f(x_{gj}) + u_g + \varepsilon_{gj}, \qquad u_g \sim (0,\sigma_u^2), \quad \varepsilon_{gj} \sim (0,\sigma_\varepsilon^2), \qquad\qquad (1)$$

with residual intraclass correlation

$$r = \frac{\sigma_u^2}{\sigma_u^2+\sigma_\varepsilon^2} . \qquad\qquad (2)$$

In crop-yield tables $u_g$ collects everything that is persistent for a place and not captured by the covariates: soil, farming practice, crop mix, reporting conventions. A learner that can recognise the group from its features, because the features are nearly constant within the group and differ between groups, can estimate $u_g$ from the group's other rows. We call such features a group fingerprint.

## The inflation ratio

Let $R_{\mathrm{rand}}$ and $R_{\mathrm{grp}}$ be the mean-squared errors on test rows from groups that are present or absent in training. The companion paper defines the inflation ratio $\rho=\sqrt{R_{\mathrm{grp}}/R_{\mathrm{rand}}}$ and shows that, for a learner that memorises group offsets and a correctly specified $f$,

$$\rho \le \frac{1}{\sqrt{1-r}} , \qquad\qquad (3)$$

so the largest possible inflation is set by the residual intraclass correlation, and an observed $\rho$ implies the lower bound $r \ge 1-1/\rho^2$ [@paper1]. For $r=0.75$ the bound is $\rho\le 2$ and for $r=0.9$ it is $\rho\le 3.2$.

## Coverage collapse

Split conformal prediction forms intervals $\hat y(x)\pm\hat q$, where $\hat q$ is the $\lceil (n+1)(1-\alpha)\rceil$-th smallest absolute residual among $n$ calibration rows [@vovk2005; @lei2018]:

$$\hat q = \operatorname{Quantile}_{\lceil (n+1)(1-\alpha)\rceil/n}\bigl(\lvert y_i-\hat y(x_i)\rvert \ : \ i\in\mathrm{cal}\bigr). \qquad\qquad (4)$$

If calibration rows are exchangeable with the test row, coverage is at least $1-\alpha$. If calibration rows come from groups already seen in training while test rows come from new groups, the two residual distributions differ. When both are approximately zero-mean Gaussian with scales $\sigma_c$ (calibration) and $\sigma_t$ (test), $\hat q\approx z_{1-\alpha/2}\sigma_c$ and the actual coverage is

$$1-\alpha_{\mathrm{eff}} = 2\,\Phi\!\left(\frac{z_{1-\alpha/2}}{\rho}\right)-1 , \qquad \rho=\frac{\sigma_t}{\sigma_c} . \qquad\qquad (5)$$

The scale ratio in Eq. (5) is the inflation ratio of Section 3.2 when calibration rows play the role of rows from seen groups, which is what random hold-out rows are. Combining Eqs. (3) and (5) gives the guideline that, under the idealised memorising learner,

$$1-\alpha_{\mathrm{eff}} \ \ge\ 2\,\Phi\!\bigl(z_{1-\alpha/2}\sqrt{1-r}\bigr)-1 . \qquad\qquad (6)$$

For example, at $\alpha=0.1$ and $r=0.9$ the coverage can fall to 0.40, and at $r=0.75$ to 0.59. Equation (5) can also be inverted: an observed naive coverage $c$ implies $\rho = z_{1-\alpha/2}/\Phi^{-1}\bigl((1+c)/2\bigr)$ and therefore $r \ge 1-1/\rho^2$, which we use in Section 6.3 as a measure of how much group-specific variance the model absorbs. Equations (5) and (6) are approximations: residuals are heavier tailed than Gaussian and Eq. (3) assumes an idealised learner, so we treat them as diagnostics and test them in simulation and on data rather than as theorems.

## Group-aware calibration and per-group coverage

The remedy is to calibrate on groups the model has not seen. 

**Proposition 1.** Let the groups be exchangeable draws from a population of groups. Fit the model on one set of groups, and compute scores on rows from a disjoint set of calibration groups. For a test group exchangeable with the calibration groups, and for one row drawn from each group with the same sampling rule, the interval $\hat y(x)\pm\hat q$ with $\hat q$ from Eq. (4) covers the test row with probability at least $1-\alpha$.

This is split conformal prediction with the group as the exchangeable unit, as in two-layer hierarchical models [@dunn2023]. When all rows of the calibration groups are pooled, as we do, the guarantee holds for a row drawn with probability proportional to its group's share of the calibration rows, and per-group coverage is not controlled. Within group $g$ with residual scale $\sigma_g$, Gaussian residuals give

$$c_g \approx 2\,\Phi\!\left(\frac{\hat q}{\sigma_g}\right)-1 , \qquad\qquad (7)$$

so groups with a larger residual scale than the pooled one are under-covered even when the pooled coverage equals $1-\alpha$. Heterogeneity of $\sigma_g$ therefore produces a spread of $c_g$ and a tail of poorly covered groups, and no single constant $\hat q$ removes it. Normalising scores by a learned scale $\hat\sigma(x)$, so that intervals are $\hat y(x)\pm\hat q\,\hat\sigma(x)$, narrows the spread to the extent that $\hat\sigma(x)$ predicts $\sigma_g$ [@romano2019; @vovk2013]; exact group-conditional guarantees require group-specific calibration sets [@gibbs2025].

## Why the model family matters

The collapse in Eq. (5) needs $\rho>1$, that is, a model whose residuals on seen groups are smaller than on unseen ones. This requires the model to exploit group identity: through features that identify the group, and through a function class flexible enough to use them. Linear models with a few covariates cannot encode hundreds of country-specific offsets from three continuous variables and a crop indicator, so we expect $\rho\approx 1$ for ridge regression, a larger $\rho$ for gradient boosting and the largest for random forests that grow deep trees [@breiman2001; @friedman2001; @hajjem2014]. We test this prediction in Section 6.4.

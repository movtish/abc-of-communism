"""Accounting sensitivities. None are estimates of unobserved migration."""

import pathlib, json, sys
import numpy as np, pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "results"
OUT.mkdir(exist_ok=True)
J = json.loads((SOURCE / "results/paper_numbers.json").read_text(encoding="utf-8"))
N = J["NUM"]
e = N["mix.e"][0]
h = N["mix.h.adult"][0]
observed = N["mix.obs"][0]
duration_old = 29 + 10 / 12
duration_new = 12 + 1 / 12
hshort = 1 - (1 - h) ** (duration_new / duration_old)
pd.DataFrame(
    [
        dict(
            scenario="historical probability transported unchanged",
            e=e,
            h=h,
            predicted_men=e + (1 - e) * h,
            observed_men=observed,
            explained_gap_pp=100 * (1 - e) * h,
        ),
        dict(
            scenario="illustration only: constant annual hazard, shorter exposure",
            e=e,
            h=hshort,
            predicted_men=e + (1 - e) * hshort,
            observed_men=observed,
            explained_gap_pp=100 * (1 - e) * hshort,
        ),
    ]
).to_csv(OUT / "mixture_duration.csv", sep=";", index=False, encoding="utf-8-sig")
est = pd.read_csv(OUT / "estimates.csv", sep=";")
rows = []
for label in ["main_female", "main_DDD", "rayon_all_female"]:
    r = est[est.model == label].iloc[0]
    for M in [0, 2, 5, 10, 15, 20]:
        rows.append(
            dict(
                model=label,
                assumed_max_abs_bias_pp=M,
                b_low=r.b - M,
                b_high=r.b + M,
                ci_low=r.ci_low_cr2 - M,
                ci_high=r.ci_high_cr2 + M,
            )
        )
pd.DataFrame(rows).to_csv(
    OUT / "bounded_bias_sensitivity.csv", sep=";", index=False, encoding="utf-8-sig"
)
ry = pd.read_csv(SOURCE / "data/linked_cohorts_rayon_1926_1939.csv", sep=";")
ry = ry[ry.age_1926.isin(["20-24", "25-29", "30-34"])].copy()
rows = []
for (area, sex), s in ry.groupby(["area", "sex"]):
    for tag, ss in [
        ("all_regions", s),
        ("marked_exact_by_author", s[s.approx_borders == 0]),
    ]:
        p0 = ss.pop_1926.sum()
        p1 = ss.pop_1939.sum()
        L0 = (ss.lit_1926 * ss.pop_1926).sum() / p0 / 100
        L1 = (ss.lit_1939 * ss.pop_1939).sum() / p1 / 100
        ret = p1 / p0
        bound = min(1, L0 / min(ret, 1)) - L0
        imm = max(0, ret * L1 - L0)
        rows.append(
            dict(
                area=area,
                sex=sex,
                sample=tag,
                pop26=p0,
                pop39=p1,
                ratio=ret,
                lit26=100 * L0,
                lit39=100 * L1,
                gain=100 * (L1 - L0),
                closed_no_learning_selection_max_pp=100 * bound,
                min_all_literate_gross_inflow_as_pct_initial=100 * imm,
            )
        )
pd.DataFrame(rows).to_csv(
    OUT / "selection_accounting.csv", sep=";", index=False, encoding="utf-8-sig"
)
# An identity exposing mathematical coupling in convergence regressions.
jj = pd.read_csv(SOURCE / "results/J1_regions.csv", sep=";")
import statsmodels.formula.api as smf

r0 = smf.ols("gain ~ l26", jj).fit()
r1 = smf.ols("l39 ~ l26", jj).fit()
assert abs(r0.params["l26"] - (r1.params["l26"] - 1)) < 1e-10
(OUT / "accounting_summary.json").write_text(
    json.dumps(
        dict(
            mixture_unadjusted=h,
            mixture_horizon_illustration=hshort,
            mixture_predicted_short=e + (1 - e) * hshort,
            convergence_slope_gain=r0.params["l26"],
            convergence_slope_followup=r1.params["l26"],
        ),
        indent=2,
    ),
    encoding="utf-8",
)
print("Accounting sensitivities written")

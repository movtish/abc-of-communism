"""Estimate institutional correlates and the intermediate-cohort age check.

Institutional placement is endogenous. The regressions are exploratory."""

from pathlib import Path
import sys, json
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from inference import Model

OUT = HERE.parent
d = pd.read_csv(OUT / "linked1924_exposure_cohort_outcomes.csv")
d["female_pupils10"] = d.female_pupil_share_pct / 10
d["female_teachers10"] = d.female_teacher_share_pct / 10
res = []
for tag, q in [
    ("all14", d),
    ("coverage80", d[d.survey_coverage >= 0.8]),
    ("coverage80_geo", d[(d.survey_coverage >= 0.8) & (~d.known_boundary_sensitivity)]),
]:
    for exposure in ["female_pupils10", "female_teachers10"]:
        for weight in [None, "cohort_population1926"]:
            formula = (
                f"relative_female_gain_pp ~ {exposure} + baseline_male_minus_female_gap"
            )
            m = Model(formula, q, weight, cluster="region_1939")
            r = m.evaluate({exposure: 1}, bootstrap=9999)
            r.update(
                sample=tag,
                exposure=exposure,
                weights=weight or "equal_regions",
                estimand="change in later relative female gain per 10pp higher female share in surveyed 1924 institutions",
                formula=formula,
            )
            res.append(r)
pd.DataFrame(res).to_csv(
    OUT / "institution_predictor_models.csv", index=False, encoding="utf-8-sig"
)
print(
    pd.DataFrame(res)[
        [
            "sample",
            "exposure",
            "weights",
            "n",
            "b",
            "ci_low_cr2",
            "ci_high_cr2",
            "p_cr2",
            "wcr_p",
            "wcr_draws",
            "loo_min",
            "loo_max",
        ]
    ].to_string(index=False)
)

# Counts, controlling for the size of the comparison cohort. That cohort is a
# size covariate, not a denominator for the full population eligible for likbez.
d["log2_schools"] = np.log2(d.schools_total)
d["log2_teachers"] = np.log2(d.teachers_B)
d["log2_cohort_population"] = np.log2(d.cohort_population1926)
counts = []
for tag, q in [
    ("all14", d),
    ("coverage80", d[d.survey_coverage >= 0.8]),
    ("coverage80_geo", d[(d.survey_coverage >= 0.8) & (~d.known_boundary_sensitivity)]),
]:
    for exposure in ["log2_schools", "log2_teachers"]:
        for weight in [None, "cohort_population1926"]:
            formula = f"relative_female_gain_pp ~ {exposure} + log2_cohort_population + baseline_male_minus_female_gap"
            r = Model(formula, q, weight, cluster="region_1939").evaluate(
                {exposure: 1}, bootstrap=9999
            )
            r.update(
                sample=tag,
                exposure=exposure,
                weights=weight or "equal_regions",
                estimand="relative female gain per doubling of school/teacher count, conditional on comparison-cohort size and baseline gap",
                formula=formula,
            )
            counts.append(r)
pd.DataFrame(counts).to_csv(
    OUT / "institution_scale_models.csv", index=False, encoding="utf-8-sig"
)
print("\nINSTITUTION SCALE")
print(
    pd.DataFrame(counts)[
        [
            "sample",
            "exposure",
            "weights",
            "n",
            "b",
            "ci_low_cr2",
            "ci_high_cr2",
            "p_cr2",
            "wcr_p",
        ]
    ].to_string(index=False)
)

w = pd.read_csv(OUT / "inputs/W2_cells.csv", sep=";")
new = []
for tag, q in [("all", w), ("no_ural", w[~w.unit_1926.str.contains("округ")])]:
    for omit_boundary_cohort in [False, True]:
        x = q[q.age_1926 != "33-37"].copy() if omit_boundary_cohort else q.copy()
        for label, contrast in [
            ("female", {"young": 1, "young:female": 1}),
            ("DDD", {"young:female": 1}),
        ]:
            m = Model(
                "gain_pp ~ young*female + middle*female + C(unit_1926)",
                x,
                "pop_1926",
                cluster="region_1939",
            )
            r = m.evaluate(contrast, bootstrap=9999)
            r.update(
                sample=tag,
                young_definition="18-32",
                specification="omit_33_37" if omit_boundary_cohort else "baseline",
                excluded_cohort="33-37" if omit_boundary_cohort else "none",
                contrast=label,
            )
            new.append(r)
pd.DataFrame(new).to_csv(
    OUT / "policy1931_age_sensitivity.csv", index=False, encoding="utf-8-sig"
)
print("\nPOLICY AGE SENSITIVITY")
print(
    pd.DataFrame(new)[
        [
            "sample",
            "young_definition",
            "specification",
            "contrast",
            "n",
            "clusters",
            "b",
            "ci_low_cr2",
            "ci_high_cr2",
            "wcr_p",
        ]
    ].to_string(index=False)
)

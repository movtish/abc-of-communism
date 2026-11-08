"""Estimate regional changes in the female-minus-male gap in 1939-1959.

Use republic and cohort effects with republic-clustered inference.
The five- and nine-republic samples retain small boundary differences.
The comparisons are descriptive."""

from pathlib import Path
import sys, json
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from inference import Model

OUT = HERE.parent
d = pd.read_csv(OUT / "linked_republic_cohorts_1939_1959.csv")
d = d[d.age1939 != "45-49"].copy()
d["female"] = (d.sex == "F").astype(int)
res = []
for core in [True, False]:
    for area in ["total", "rural", "urban"]:
        q = d[d.area == area].copy()
        if core:
            q = q[q.core_paper_republic == 1]
        for weight in ["population1939", None]:
            m = Model(
                "change_pp ~ C(region) + C(age1939) + female",
                q,
                weight=weight,
                cluster="region",
            )
            r = m.evaluate({"female": 1}, bootstrap=512)
            r.update(
                sample="paper_core5" if core else "republics9",
                area=area,
                weights=weight or "equal_cells",
                estimand="descriptive change in female-minus-male gap 1939-1959",
            )
            res.append(r)
pd.DataFrame(res).to_csv(
    OUT / "post1939_gender_gap_inference.csv", index=False, encoding="utf-8-sig"
)
print(
    pd.DataFrame(res)[
        [
            "sample",
            "area",
            "weights",
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

"""Transcribe Table XVII of the 1924 education survey.

The counts cover literacy points and schools on 1 January 1924.
General adult schools in adjacent columns are excluded. The table
counts pupils on that date, not graduates over a period."""

from pathlib import Path
import pandas as pd
import numpy as np
import json, hashlib, sys

sys.stdout.reconfigure(encoding="utf-8")
PACKAGE = Path(__file__).resolve().parent.parent
HERE = PACKAGE / "raw_sources"
OUT = PACKAGE
OUT.mkdir(exist_ok=True)
SOURCE = "https://istmat.org/files/uploads/22102/obrazovanie_1921-25_vyp.1_1924_god.pdf"
# unit name used in the paper, original row number, PDF page,
# Each total or rural row starts with registered and surveyed institutions,
# teachers male/female/both, pupils male/female/both.
manual = [
    (
        "Татарская АССР",
        44,
        68,
        [111, 111, 114, 97, 211, 2836, 724, 3560],
        [81, 81, 73, 51, 124, 2156, 298, 2454],
    ),
    (
        "Чувашская АССР",
        40,
        68,
        [41, 33, 35, 5, 40, 1289, 0, 1289],
        [41, 33, 35, 5, 40, 1289, 0, 1289],
    ),
    (
        "Марийская АО",
        39,
        68,
        [29, 11, 13, 3, 16, 112, 136, 248],
        [23, 5, 4, 1, 5, 38, 78, 116],
    ),
    (
        "Вотская АО",
        36,
        68,
        [108, 106, 90, 88, 178, 2731, 315, 3046],
        [99, 97, 87, 82, 169, 2656, 198, 2854],
    ),
    (
        "Башкирская АССР",
        41,
        68,
        [220, 220, 233, 113, 349, 7651, 537, 8188],
        [195, 195, 214, 79, 293, 7110, 284, 7394],
    ),
    (
        "Карельская АССР",
        42,
        68,
        [15, 14, 14, 7, 21, 150, 183, 333],
        [8, 8, 8, 3, 11, 92, 57, 149],
    ),
    (
        "Воронежская губ.",
        7,
        67,
        [286, 278, 133, 223, 356, 9363, 860, 10223],
        [263, 255, 117, 214, 331, 8922, 603, 9525],
    ),
    (
        "Курская губ.",
        14,
        67,
        [136, 121, 80, 71, 151, 3047, 410, 3457],
        [113, 98, 62, 52, 114, 2040, 281, 2321],
    ),
    (
        "Смоленская губ.",
        27,
        68,
        [167, 138, 94, 65, 159, 2097, 925, 3022],
        [128, 99, 71, 45, 116, 1648, 437, 2085],
    ),
    (
        "Пензенская губ.",
        21,
        68,
        [198, 193, 95, 152, 247, 5752, 588, 6340],
        [168, 164, 77, 121, 198, 4692, 200, 4892],
    ),
    (
        "Саратовская губ.",
        25,
        68,
        [137, 136, 114, 103, 217, 3663, 1401, 5064],
        [75, 74, 64, 61, 125, 2532, 480, 3012],
    ),
    (
        "Сталинградская губ.",
        33,
        68,
        [43, 43, 27, 35, 62, 993, 564, 1557],
        [14, 14, 10, 8, 18, 465, 120, 585],
    ),
    (
        "Вятская губ.",
        8,
        67,
        [63, 63, 25, 74, 99, 1007, 754, 1761],
        [40, 40, 19, 45, 64, 719, 382, 1101],
    ),
    (
        "Оренбургская губ.",
        49,
        69,
        [38, 38, 35, 20, 55, 1328, 208, 1536],
        [17, 17, 22, 6, 28, 961, 0, 961],
    ),
    (
        "Самарская губ.",
        24,
        68,
        [257, 101, 54, 74, 128, 2143, 739, 2882],
        [237, 83, 46, 57, 103, 1849, 365, 2214],
    ),
]
cols = [
    "schools_total",
    "schools_surveyed",
    "teachers_M",
    "teachers_F",
    "teachers_B",
    "pupils_M",
    "pupils_F",
    "pupils_B",
]
rows = []
for name, row, page, total, rural in manual:
    for area, values in [("total", total), ("rural", rural)]:
        r = dict(
            unit_1926=name,
            source_date="1924-01-01",
            source_row=row,
            pdf_page=page,
            printed_pages=f"{462+2*(page-67)}-{463+2*(page-67)}",
            area=area,
            source_url=SOURCE,
            territory_link="name correspondence; boundary transfers not fully harmonized",
            known_boundary_sensitivity=name in ["Чувашская АССР", "Оренбургская губ."],
        )
        r.update(dict(zip(cols, values)))
        r["teachers_sex_unallocated"] = (
            r["teachers_B"] - r["teachers_M"] - r["teachers_F"]
        )
        r["pupils_sex_unallocated"] = r["pupils_B"] - r["pupils_M"] - r["pupils_F"]
        r["survey_coverage"] = r["schools_surveyed"] / r["schools_total"]
        r["female_pupil_share_pct"] = 100 * r["pupils_F"] / r["pupils_B"]
        r["female_teacher_share_pct"] = 100 * r["teachers_F"] / r["teachers_B"]
        r["pupils_per_surveyed_school"] = r["pupils_B"] / r["schools_surveyed"]
        r["pupils_per_teacher"] = r["pupils_B"] / r["teachers_B"]
        r["dash_as_zero_fields"] = (
            "pupils_F"
            if name in ["Чувашская АССР", "Оренбургская губ."] and r["pupils_F"] == 0
            else ""
        )
        rows.append(r)
a = pd.DataFrame(rows)
assert len(a) == 30 and not a.duplicated(["unit_1926", "area"]).any()
assert (a.pupils_sex_unallocated == 0).all()
assert (a.teachers_sex_unallocated >= 0).all()
assert a.teachers_sex_unallocated.sum() == 3
assert (a.schools_total >= a.schools_surveyed).all()
# Check rural subsets without assuming that unsurveyed establishments have the
# same pupil mix or staffing as surveyed ones.
for name, g in a.groupby("unit_1926"):
    g = g.set_index("area")
    for c in cols:
        assert g.loc["rural", c] <= g.loc["total", c]
a.to_csv(OUT / "likbez1924_transcription.csv", index=False, encoding="utf-8-sig")

w = pd.read_csv(PACKAGE / "inputs/W2_cells.csv", sep=";")
y = w[w.age_1926 == "18-22"].copy()
y["weighted_lit39"] = y.lit_1939  # published rounded rates; no extra precision claimed
out = []
for unit, g in y.groupby("unit_1926"):
    if set(g.sex) != {"M", "F"}:
        continue
    g = g.set_index("sex")
    f = g.loc["F"]
    m = g.loc["M"]
    out.append(
        dict(
            unit_1926=unit,
            region_1939=f.region_1939,
            female_gain_pp=f.gain_pp,
            male_gain_pp=m.gain_pp,
            relative_female_gain_pp=f.gain_pp - m.gain_pp,
            baseline_female_literacy=f.lit_1926,
            baseline_male_literacy=m.lit_1926,
            baseline_male_minus_female_gap=m.lit_1926 - f.lit_1926,
            cohort_population1926=f.pop_1926 + m.pop_1926,
            min_tier=min(f.tier, m.tier),
        )
    )
y = pd.DataFrame(out).merge(
    a[a.area == "rural"], on="unit_1926", how="inner", validate="one_to_one"
)
assert len(y) == 14
y.to_csv(
    OUT / "linked1924_exposure_cohort_outcomes.csv", index=False, encoding="utf-8-sig"
)
print(
    "TRANSCRIPTION",
    a[
        [
            "unit_1926",
            "area",
            "survey_coverage",
            "female_pupil_share_pct",
            "female_teacher_share_pct",
            "teachers_sex_unallocated",
        ]
    ]
    .round(4)
    .to_string(index=False),
)
print("MATCHED", len(y), "HIGH_COVERAGE", sum(y.survey_coverage >= 0.8))
qc = dict(
    source_date="1924-01-01",
    transcribed_rows=len(a),
    territories=a.unit_1926.nunique(),
    source_pdf_pages=[67, 68, 69],
    all_pupil_sex_sums_exact=True,
    nonnegative_unallocated_teacher_sex=True,
    unallocated_teachers=3,
    all_rural_counts_within_total=True,
    matched_young_cohort_units=len(y),
    matched_units_coverage_at_least_80pct=int(sum(y.survey_coverage >= 0.8)),
    source_pdf_sha256=hashlib.sha256(
        (HERE / "education_1924.pdf").read_bytes()
    ).hexdigest(),
)
(OUT / "transcription_validation.json").write_text(
    json.dumps(qc, ensure_ascii=False, indent=2), encoding="utf-8"
)

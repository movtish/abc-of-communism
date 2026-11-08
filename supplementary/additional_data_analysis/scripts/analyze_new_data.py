"""Extract regional education, migration and time-use tables.

Read the included historical sources and corrected 1939 census input.
Write the 1959 long table, linked cohorts and accounting checks."""

from pathlib import Path
import sys, json, csv, hashlib, math
from collections import Counter
import xlrd
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

PACKAGE = Path(__file__).resolve().parent.parent
HERE = PACKAGE / "raw_sources"
OUT = PACKAGE
DATA = PACKAGE / "inputs"


def write_csv(name, records):
    pd.DataFrame(records).to_csv(OUT / name, index=False, encoding="utf-8-sig")


def raw_tables(id):
    s = BeautifulSoup((HERE / f"istmat_{id}.html").read_bytes(), "html.parser")
    return [
        [
            [
                c.get_text(" ", strip=True)
                for c in r.find_all(["td", "th"], recursive=False)
            ]
            for r in t.find_all("tr")
        ]
        for t in s.find_all("table")
    ]


def number(v):
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace("\xa0", "").replace(" ", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


# The workbook contains 89 canonical territorial entries, followed by derived
# Leningrad work blocks. National totals and nested districts are not independent.
s = xlrd.open_workbook(HERE / "1959_source.xls").sheet_by_index(0)
groups = [
    ("total", "B", 5),
    ("total", "M", 18),
    ("total", "F", 31),
    ("urban", "B", 44),
    ("urban", "M", 57),
    ("urban", "F", 70),
    ("rural", "B", 83),
    ("rural", "M", 96),
    ("rural", "F", 109),
]
fields = [
    "population",
    "higher",
    "higher_incomplete",
    "secondary_special",
    "secondary_general",
    "secondary_incomplete",
    "seven_year",
    "seven_year_incomplete",
    "primary",
    "literate_no_primary",
    "illiterate",
    "education_not_stated",
]
rows = []
reconciliation = []
inventory = {}
for rn in range(13, s.nrows):
    v = s.row_values(rn)
    if not (
        isinstance(v[0], float)
        and 1 <= v[0] <= 89
        and isinstance(v[3], float)
        and 1 <= v[3] <= 25
    ):
        continue
    rid = int(v[0])
    ai = int(v[3])
    name = v[2].strip()
    inventory[rid] = name
    age = str(int(v[4])) if isinstance(v[4], float) else str(v[4])
    age = {
        "Все население": "TOTAL",
        "до 9 лет": "0-8",
        "70 и старше": "70+",
        "возраст не указан": "unknown",
    }.get(age, age)
    for area, sex, base in groups:
        vals = [number(x) for x in v[base : base + 12]]
        raw_blank = [fields[i] for i, x in enumerate(vals) if x is None]
        residual = (
            None
            if vals[0] is None
            else vals[0] - sum(x for x in vals[1:] if x is not None)
        )
        # For age 9+, nonnegative, exhaustive categories and an exact zero
        # residual jointly identify any blank components as zero. Do not do this
        # for under-9s or for the all-age row, whose denominator includes them.
        fill = bool(ai >= 3 and residual == 0 and vals[0] is not None)
        if fill:
            vals = [0.0 if x is None else x for x in vals]
        r = dict(
            region_id=rid,
            region=name,
            area=area,
            sex=sex,
            age=age,
            source_excel_row=rn + 1,
            source_excel_column=base + 1,
            source_blank_fields=";".join(raw_blank),
            blank_zero_identified_by_partition=fill and bool(raw_blank),
        )
        r.update(dict(zip(fields, vals)))
        if ai >= 3:
            reconciliation.append(
                dict(region_id=rid, age=age, area=area, sex=sex, residual=residual)
            )
        # Under-9 and all-age literacy are deliberately not computed. All-age
        # literacy requires subtracting the under-9 population first.
        if (
            ai >= 3
            and r["population"] is not None
            and r["illiterate"] is not None
            and r["education_not_stated"] is not None
        ):
            den = r["population"] - r["education_not_stated"]
            lit = den - r["illiterate"]
            r.update(
                literate=lit,
                literacy_rate=100 * lit / den if den > 0 else None,
                literacy_lower=(
                    100 * lit / r["population"] if r["population"] > 0 else None
                ),
                literacy_upper=(
                    100 * (lit + r["education_not_stated"]) / r["population"]
                    if r["population"] > 0
                    else None
                ),
            )
        rows.append(r)
c59 = pd.DataFrame(rows)
assert len(c59) == 89 * 25 * 9
assert not c59.duplicated(["region_id", "area", "sex", "age"]).any()
write_csv("census1959_regions_long.csv", rows)
write_csv("census1959_partition_checks.csv", reconciliation)
assert all(x["residual"] == 0 for x in reconciliation)

# Check six population accounting identities per canonical age/territory.
accounting = []
for (rid, age), g in c59.groupby(["region_id", "age"]):
    z = g.set_index(["area", "sex"])
    for area in ["total", "urban", "rural"]:
        accounting.append(
            dict(
                region_id=int(rid),
                age=age,
                check=area + ": B-M-F",
                difference=z.loc[(area, "B"), "population"]
                - z.loc[(area, "M"), "population"]
                - z.loc[(area, "F"), "population"],
            )
        )
    for sex in ["B", "M", "F"]:
        accounting.append(
            dict(
                region_id=int(rid),
                age=age,
                check=sex + ": total-urban-rural",
                difference=z.loc[("total", sex), "population"]
                - z.loc[("urban", sex), "population"]
                - z.loc[("rural", sex), "population"],
            )
        )
write_csv("census1959_population_checks.csv", accounting)

# Four independently downloaded HTML region tables must reproduce the XLS cells.
html_checks = []
for rid in [14, 24, 36, 52]:
    soup = BeautifulSoup(
        (HERE / f"1959_region_{rid}.html").read_text(encoding="utf-8"), "html.parser"
    )
    tables = soup.find_all("table")
    table = max(tables, key=lambda t: len(t.find_all("tr")))
    area = sex = None
    for tr in table.find_all("tr"):
        cells = [
            x.get_text(" ", strip=True)
            for x in tr.find_all(["td", "th"], recursive=False)
        ]
        if len(cells) == 1:
            text = cells[0].lower()
            if text in {"городское население", "сельское население", "все население"}:
                area = {
                    "городское население": "urban",
                    "сельское население": "rural",
                    "все население": "total",
                }[text]
            if text in {"мужчины", "женщины", "оба пола"}:
                sex = {"мужчины": "M", "женщины": "F", "оба пола": "B"}[text]
        if len(cells) != 14 or not area or not sex:
            continue
        age = cells[1]
        age = {
            "Все население": "TOTAL",
            "до 9 лет": "0-8",
            "70 и старше": "70+",
            "возраст не указан": "unknown",
        }.get(age, age)
        z = c59[
            (c59.region_id == rid)
            & (c59.area == area)
            & (c59.sex == sex)
            & (c59.age == age)
        ]
        if len(z) != 1:
            continue
        for f, x in zip(fields, cells[2:]):
            val = number(x)
            src = z.iloc[0][f]
            if val is not None:
                html_checks.append(
                    dict(
                        region_id=rid,
                        area=area,
                        sex=sex,
                        age=age,
                        field=f,
                        difference=None if pd.isna(src) else src - val,
                    )
                )
write_csv("census1959_html_xls_checks.csv", html_checks)
assert len(html_checks) > 1000
assert all(x["difference"] == 0 for x in html_checks)

# Same-name republic diagnostics. This is explicitly not a completed boundary
# concordance. Karelia, deported/reconstituted republics, and split oblasts are
# excluded from the core set. Small border transfers still require verification.
maps = [
    ("Татарская АССР", 36, 1),
    ("Башкирская АССР", 52, 1),
    ("Чувашская АССР", 27, 1),
    ("Марийская АССР", 25, 1),
    ("Удмуртская АССР", 53, 1),
    ("Коми АССР", 3, 0),
    ("Мордовская АССР", 26, 0),
    ("Якутская АССР", 79, 0),
    ("Бурят-Монгольская АССР", 69, 0),
]
c39 = pd.read_csv(DATA / "census1939_literacy_by_region_age_sex.csv", sep=";")
pairs = [("30-34", "50-54"), ("35-39", "55-59"), ("40-44", "60-64"), ("45-49", "65-69")]
linked = []
for name, rid, core in maps:
    for area in ["total", "urban", "rural"]:
        for sex in ["M", "F"]:
            for a, b in pairs:
                x = c39[
                    (c39.region_1939 == name)
                    & (c39.area == area)
                    & (c39.sex == sex)
                    & (c39.age == a)
                ].iloc[0]
                y = c59[
                    (c59.region_id == rid)
                    & (c59.area == area)
                    & (c59.sex == sex)
                    & (c59.age == b)
                ].iloc[0]
                p39 = 100 * x.literate / x.population
                ratio = y.population / x.population
                linked.append(
                    dict(
                        region=name,
                        region_id=rid,
                        core_paper_republic=core,
                        geographic_status="same-name/core correspondence; small transfers not harmonized",
                        area=area,
                        sex=sex,
                        age1939=a,
                        age1959=b,
                        population1939=x.population,
                        population1959=y.population,
                        literate1939=x.literate,
                        literate1959=y.literate,
                        literacy1939=p39,
                        literacy1959=y.literacy_rate,
                        change_pp=y.literacy_rate - p39,
                        unknown_education1959=y.education_not_stated,
                        literacy1959_lower=y.literacy_lower,
                        literacy1959_upper=y.literacy_upper,
                        population_retention_ratio=ratio,
                    )
                )
z = pd.DataFrame(linked)
write_csv("linked_republic_cohorts_1939_1959.csv", linked)

agg = []
for keys, g in z[z.age1939 != "45-49"].groupby(
    ["region", "region_id", "core_paper_republic", "area", "sex"]
):
    region, rid, core, area, sex = keys
    w = g.population1939
    p39 = 100 * g.literate1939.sum() / g.population1939.sum()
    p59 = np.average(g.literacy1959, weights=w)
    agg.append(
        dict(
            region=region,
            region_id=int(rid),
            core_paper_republic=int(core),
            area=area,
            sex=sex,
            literacy1939=p39,
            literacy1959_standardized=p59,
            change_standardized_pp=p59 - p39,
            literacy1959_own_age_weights=100
            * g.literate1959.sum()
            / (g.population1959 - g.unknown_education1959).sum(),
            population1939=g.population1939.sum(),
            population1959=g.population1959.sum(),
            population_retention_ratio=g.population1959.sum() / g.population1939.sum(),
            lower_change_pp=np.average(g.literacy1959_lower, weights=w) - p39,
            upper_change_pp=np.average(g.literacy1959_upper, weights=w) - p39,
        )
    )
a = pd.DataFrame(agg)
write_csv("republic_summary_1939_1959.csv", agg)

# Transparent transcription of numeric HTML tables; commas are decimal marks.
# Never let read_html's default thousands parser turn 59,6 into 596.
mig = []
for row in raw_tables(18145)[0][2:]:
    if len(row) != 5:
        continue
    n1, n2 = number(row[1]), number(row[2])
    if n1 is None or n2 is None:
        continue
    mig.append(
        dict(
            region_source=row[0],
            rural_to_urban1931_thousand=n1,
            rural_to_urban1932_thousand=n2,
            ratio1932_1931=n2 / n1 if n1 else None,
            source="https://istmat.org/node/18145",
            header_warning="Rate columns omitted: last year printed 1935 despite 1931-1932 title",
        )
    )
write_csv("migration_rural_urban_1931_1932.csv", mig)
flows = []
for row in raw_tables(18140)[0][3:]:
    if len(row) != 10:
        continue
    nums = [number(x) for x in row[2:]]
    if any(x is None for x in nums):
        continue
    for yr, offset in [(1931, 0), (1932, 4)]:
        coverage, arrive, depart, accepted = nums[offset : offset + 4]
        flows.append(
            dict(
                region_source=row[1],
                year=yr,
                coverage_pct=coverage,
                arrivals_source=arrive,
                departures_source=depart,
                accepted_net_growth_source=accepted,
                arithmetic_arrivals_minus_departures=arrive - depart,
                difference_accepted_vs_arithmetic=accepted - (arrive - depart),
                units="original table scale; no conversion assumed",
                source="https://istmat.org/node/18140",
            )
        )
write_csv("migration_registration_1931_1932.csv", flows)
gender = []
for row in raw_tables(18139)[0][4:]:
    if len(row) != 9:
        continue
    vals = [number(x) for x in row[1:]]
    if any(x is None for x in vals):
        continue
    for yr, offset in [(1931, 0), (1932, 4)]:
        for direction, j in [("arrivals", 0), ("departures", 2)]:
            male, female = vals[offset + j : offset + j + 2]
            gender.append(
                dict(
                    republic=row[0],
                    year=yr,
                    direction=direction,
                    male_pct=male,
                    female_pct=female,
                    sum_pct=male + female,
                    source="https://istmat.org/node/18139",
                )
            )
write_csv("migration_sex_shares_1931_1932.csv", gender)

# A small contemporary time-use survey. Exact hours/minutes, not decimal-time
# confusion; selected entries are copied twice (summer/winter) for comparison.
time = []
for season, table in zip(["summer", "winter"], raw_tables(27934)[:2]):
    for row in table:
        if len(row) != 11 or "Домашний" not in row[0] and "домашний" not in row[0]:
            continue
        for label, i in [
            ("head_of_household", 1),
            ("housewife", 3),
            ("helping_men", 5),
            ("helping_women", 7),
        ]:
            h, m = number(row[i]), number(row[i + 1])
            if h is None or m is None:
                continue
            time.append(
                dict(
                    season=season,
                    role=label,
                    domestic_work_minutes=60 * h + m,
                    source_hours=h,
                    source_minutes=m,
                    survey_households=29,
                    valid_time_budgets=71,
                    survey_location="Voronezh guberniya, 3 uezds",
                    source="https://istmat.org/node/27934",
                )
            )
write_csv("time_use_1923_domestic_work.csv", time)


summaries = []
for core in [False, True]:
    for area in ["total", "urban", "rural"]:
        for sex in ["M", "F"]:
            g = a[(a.area == area) & (a.sex == sex)]
            if core:
                g = g[g.core_paper_republic == 1]
            summaries.append(
                dict(
                    sample="paper_core5" if core else "republics9",
                    area=area,
                    sex=sex,
                    regions=len(g),
                    population1939=float(g.population1939.sum()),
                    weighted_change_pp=float(
                        np.average(g.change_standardized_pp, weights=g.population1939)
                    ),
                    min_region_change_pp=float(g.change_standardized_pp.min()),
                    max_region_change_pp=float(g.change_standardized_pp.max()),
                    negative_regions=int((g.change_standardized_pp < 0).sum()),
                    weighted_lower_change_pp=float(
                        np.average(g.lower_change_pp, weights=g.population1939)
                    ),
                    weighted_upper_change_pp=float(
                        np.average(g.upper_change_pp, weights=g.population1939)
                    ),
                )
            )
write_csv("persistence_sample_summary.csv", summaries)
qc = dict(
    canonical_regions=89,
    canonical_age_rows=2225,
    long_records=len(rows),
    component_checks=len(reconciliation),
    component_nonzero_residuals=sum(x["residual"] != 0 for x in reconciliation),
    population_accounting_checks=len(accounting),
    population_accounting_discrepancies=sum(x["difference"] != 0 for x in accounting),
    html_xls_numeric_checks=len(html_checks),
    html_xls_discrepancies=sum(x["difference"] != 0 for x in html_checks),
    linked_cohort_rows=len(linked),
    region_summaries=len(agg),
    migration_region_rows=len(mig),
    migration_registration_rows=len(flows),
    migration_gender_rows=len(gender),
    time_use_rows=len(time),
    source_xls_sha256=hashlib.sha256(
        (HERE / "1959_source.xls").read_bytes()
    ).hexdigest(),
)
(OUT / "validation_summary.json").write_text(
    json.dumps(qc, ensure_ascii=False, indent=2, default=lambda x: x.item()),
    encoding="utf-8",
)
print(json.dumps(qc, ensure_ascii=False, indent=2, default=lambda x: x.item()))
print(pd.DataFrame(summaries).to_string(index=False))
print(
    a[a.core_paper_republic == 1][
        [
            "region",
            "area",
            "sex",
            "change_standardized_pp",
            "population_retention_ratio",
        ]
    ].to_string(index=False)
)

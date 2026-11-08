from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd, sys, re, json

sys.stdout.reconfigure(encoding="utf-8")
p = Path(__file__).resolve().parent.parent / "raw_sources"
d = pd.read_csv(p.parent / "inputs/census1939_literacy_by_region_age_sex.csv", sep=";")
checks = []


def tables(n):
    s = BeautifulSoup((p / n).read_text(encoding="utf-8"), "html.parser")
    t = max(s.find_all("table"), key=lambda t: len(str(t)))
    return [
        [c.get_text(" ", strip=True) for c in r.find_all(["td", "th"], recursive=False)]
        for r in t.find_all("tr")
    ]


def num(x):
    return int(re.sub(r"\s", "", x))


for key, name in [
    ("Tatar", "Татарская АССР"),
    ("Chuvash", "Чувашская АССР"),
    ("Yakut", "Якутская АССР"),
]:
    ill = tables(f"1939_{key}_ill.html")
    for ar, offset in [("urban", 1), ("rural", 4), ("total", 7)]:
        pop = tables(f"1939_{key}_{ar}.html")
        for age in ["30-34", "35-39", "40-44", "45-49"]:

            def get_row(ts):
                return next(
                    r
                    for r in ts
                    if r
                    and r[0]
                    .replace(" ", "")
                    .replace("лет", "")
                    .replace("–", "-")
                    .replace("—", "-")
                    == age
                )

            r = get_row(ill)
            lo, hi = map(int, age.split("-"))
            qs = [
                next(q for q in pop if len(q) == 4 and q[0] == str(k))
                for k in range(lo, hi + 1)
            ]
            for sx, j in [("M", 0), ("F", 1)]:
                old = d[
                    (d.region_1939 == name)
                    & (d.area == ar)
                    & (d.sex == sx)
                    & (d.age == age)
                ].iloc[0]
                checks.append(
                    dict(
                        region=name,
                        area=ar,
                        sex=sx,
                        age=age,
                        population_difference=sum(num(q[1 + j]) for q in qs)
                        - old.population,
                        illiterate_difference=num(r[offset + j]) - old.illiterate,
                    )
                )
assert len(checks) == 72
assert all(
    x["population_difference"] == 0 and x["illiterate_difference"] == 0 for x in checks
)
pd.DataFrame(checks).to_csv(
    p.parent / "census1939_online_checks.csv", index=False, encoding="utf-8-sig"
)
print(
    "Verified 72 age-sex-area cells, 144 numeric values against newly downloaded 1939 sources."
)

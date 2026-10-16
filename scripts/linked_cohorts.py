"""Linked cohorts from Vol. 9 Table XV: the same birth cohorts observed in 1897 and 1926.
Adult literacy acquisition = literacy(1926, cohort) - literacy(1897, same cohort), by region, area, sex.
Cohort born 1868-1877: age 20-29 in Feb 1897, age 49-58 in Dec 1926 -> use 1897 bands 20-24+25-29 vs 1926 bands 50-54+55-59
(one-year offset; ages 49 and 59 straddle). Also the school-age cohort born 1878-1887 (10-19 in 1897; 40-49 in 1926).
"""
import os, sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"
xv = pd.read_csv(f"{D}/tableXV_1926_1897_age_sex_literacy.csv", sep=";", encoding="utf-8-sig")
xv = xv[xv.quality.isin(["ok", "agree", "manual", "ocr2only"])]
PAIRS = [("born 1868-77 (adults in 1897)", ["20-24", "25-29"], ["50-54", "55-59"]),
         ("born 1878-87 (school-age in 1897)", ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"], ["40-44", "45-49"]),
         ("born 1858-67", ["30-34", "35-39"], ["60-64", "65-69"])]
out = []
for reg in xv.region_gosplan_1927.unique():
    for area in ("total", "urban", "rural"):
        for sex in ("M", "F"):
            for label, a97, a26 in PAIRS:
                s97 = xv[(xv.region_gosplan_1927 == reg) & (xv.census_year == 1897) & (xv.area == area) & (xv.sex == sex) & (xv.age.isin(a97))]
                s26 = xv[(xv.region_gosplan_1927 == reg) & (xv.census_year == 1926) & (xv.area == area) & (xv.sex == sex) & (xv.age.isin(a26))]
                if s97.population.sum() == 0 or s26.population.sum() == 0 or len(s97) < len(a97) or len(s26) < len(a26):
                    continue
                r97 = 100*s97.literate.sum()/s97.population.sum(); r26 = 100*s26.literate.sum()/s26.population.sum()
                out.append(dict(region=reg, area=area, sex=sex, cohort=label, pop_1897=int(s97.population.sum()), pop_1926=int(s26.population.sum()),
                                lit_1897=round(r97, 1), lit_1926=round(r26, 1), gain_pp=round(r26 - r97, 1),
                                survival_ratio=round(s26.population.sum()/s97.population.sum(), 2)))
lc = pd.DataFrame(out)
lc.to_csv(f"{D}/tableXV_linked_cohorts.csv", sep=";", index=False, encoding="utf-8-sig")
pd.set_option("display.width", 220)
sel = lc[(lc.area == "total") & (lc.cohort.str.startswith("born 1868"))].pivot(index="region", columns="sex", values=["lit_1897", "lit_1926", "gain_pp", "survival_ratio"])
print("Cohort born 1868-77 (aged 20-29 in 1897, 49-58 in 1926), area=total:")
print(sel.round(1).to_string())
sel2 = lc[(lc.area == "rural") & (lc.cohort.str.startswith("born 1868"))].pivot(index="region", columns="sex", values=["gain_pp"])
print("\nRural, same cohort, gain (pp):"); print(sel2.round(1).to_string())

"""Wave 2 by Gosplan rayon: Table XV of 1926 x regions of 1939 summed to rayons, whole RSFSR (17 rayons).
-> data/linked_cohorts_rayon_1926_1939.csv, results/B9_wave2_rayon.txt"""
import os, sys, warnings, numpy as np, pandas as pd, statsmodels.formula.api as smf
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"; R = f"{ROOT}/results"; os.makedirs(R, exist_ok=True)
xv = pd.read_csv(f"{D}/tableXV_1926_1897_age_sex_literacy.csv", sep=";", encoding="utf-8-sig")
c39 = pd.read_csv(f"{D}/census1939_literacy_by_region_age_sex.csv", sep=";", encoding="utf-8-sig")
c39 = c39[~c39.region_1939.str.startswith("в том числе")]
MAP = {
 "Северный район": ["Архангельская область", "Вологодская область", "Коми АССР"],
 "Ленинградско-Карельский район": ["Ленинградская область", "город Ленинград", "Мурманская область", "Карельская АССР"],
 "Западный район": ["Смоленская область"],
 "Центрально-Промышленный район": ["Московская область", "город Москва", "Ивановская область", "Ярославская область", "Калининская (ныне Тверская) область", "Тульская область", "Рязанская область", "Горьковская (ныне Нижегородская) область"],
 "Центрально-Черноземный район": ["Воронежская область", "Курская область", "Орловская область", "Тамбовская область"],
 "Вятский район": ["Кировская область", "Удмуртская АССР"],
 "Уральская область": ["Свердловская область", "Челябинская область", "Молотовская (ныне Пермская) область", "Омская область"],
 "Башкирская АССР": ["Башкирская АССР"],
 "Средне-Волжский район": ["Куйбышевская (ныне Самарская) область", "Пензенская область", "Чкаловская (ныне Оренбургская) область", "Татарская АССР", "Чувашская АССР", "Марийская АССР", "Мордовская АССР"],
 "Нижне-Волжский район": ["Саратовская область", "Сталинградская (ныне Волгоградская) область", "НемцевПоволжья", "Калмыцкая АССР"],
 "Крымская АССР": ["Крымская АССР"],
 "Северо-Кавказский край": ["Краснодарский край", "Орджоникедзевский (ныне Ставропольский) край", "Ростовская область", "Кабардино-Балкарская АССР", "Cеверо-Осетинская АССР", "Чечено-Ингушская АССР"],
 "Дагестанская АССР": ["Дагестанская АССР"],
 "Сибирский край": ["Новосибирская область", "Алтайский край", "Красноярский край", "Иркутская область"],
 "Бурято-Монгольская АССР": ["Бурят-Монгольская АССР"],
 "Якутская АССР": ["Якутская АССР"],
 "Дальне-Восточный край": ["Хабаровский край", "Приморский край", "Читинская область"],
}
APPROX = {"Западный район", "Уральская область", "Сибирский край", "Центрально-Черноземный район", "Ленинградско-Карельский район"}
# Table XV gives single ages only to 19, then 5-year bands; 1939 has single ages 6-19, then 5-year bands. A 12-year shift of a
# 5-year band is approximated by a 3:2 mix of the two overlapping 1939 bands (ages a+12..a+16 = 3 years of band a+10 and 2 of band a+15).
PAIRS = [("8-12", [str(v) for v in range(8, 13)], [("20-24", 1.0)]), ("13-17", [str(v) for v in range(13, 18)], [("25-29", 1.0)]),
         ("20-24", ["20-24"], [("30-34", .6), ("35-39", .4)]), ("25-29", ["25-29"], [("35-39", .6), ("40-44", .4)]),
         ("30-34", ["30-34"], [("40-44", .6), ("45-49", .4)]), ("35-39", ["35-39"], [("45-49", .6), ("50-54", .4)]),
         ("40-44", ["40-44"], [("50-54", .6), ("55-59", .4)]), ("45-49", ["45-49"], [("55-59", .6), ("60-64", .4)]),
         ("50-54", ["50-54"], [("60-64", .6), ("65-69", .4)])]   # above the age limit of the campaign: placebo
x26 = xv[(xv.census_year == 1926) & (xv.quality != "missing")].copy()
x26["age"] = x26.age.map(lambda v: str(int(float(v))) if str(v).replace(".", "", 1).isdigit() else str(v))
print(x26.groupby(["area", "sex"]).size()); print("ages:", sorted(x26.age.unique(), key=lambda s: (len(s), s))[:60])
rows = []
for ray, regs in MAP.items():
    missing = [r for r in regs if r not in set(c39.region_1939)]
    if missing: print("missing 1939 regions for", ray, missing)
    for area in ("total", "rural"):
        s26 = x26[(x26.region_gosplan_1927 == ray) & (x26.area == area)]
        s39 = c39[c39.region_1939.isin(regs) & (c39.area == area)]
        if s26.empty or s39.empty: continue
        for sex in ("M", "F"):
            for lab26, ages26, mix39 in PAIRS:
                a = s26[(s26.sex == sex) & s26.age.isin(ages26)]
                if len(a) < len(ages26) or a.population.isna().any() or a.literate.isna().any(): continue
                p39 = l39 = 0.0; ok = True
                for band39, wgt in mix39:
                    b = s39[(s39.sex == sex) & (s39.age == band39)]
                    if b.empty: ok = False; break
                    p39 += wgt * b.population.sum(); l39 += wgt * b.literate.sum()
                if not ok: continue
                p26, l26 = a.population.sum(), a.literate.sum()
                if p26 < 1000 or p39 < 1000: continue
                band39 = "+".join(b for b, _ in mix39)
                rows.append(dict(rayon=ray, area=area, sex=sex, age_1926=lab26, age_1939=band39, pop_1926=int(p26), pop_1939=int(p39),
                                 lit_1926=round(100 * l26 / p26, 1), lit_1939=round(100 * l39 / p39, 1), gain_pp=round(100 * l39 / p39 - 100 * l26 / p26, 1),
                                 survival=round(p39 / p26, 2), approx_borders=int(ray in APPROX), n_regions_1939=len(regs) - len(missing)))
lc = pd.DataFrame(rows); lc.to_csv(f"{D}/linked_cohorts_rayon_1926_1939.csv", sep=";", index=False, encoding="utf-8-sig")
out = []
def P(*a):
    s = " ".join(str(v) for v in a); print(s); out.append(s)
P("rayons:", lc.rayon.nunique(), "| cells:", len(lc))
ADULT = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
lc["female"] = (lc.sex == "F").astype(int); lc["coh"] = pd.Categorical(lc.age_1926, ["8-12", "13-17"] + ADULT)
lc["young"] = lc.age_1926.isin(["20-24", "25-29", "30-34"]).astype(int)
def fit(f, d):
    return smf.wls(f, data=d, weights=d.pop_1926).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.rayon)[0]})
def show(r, keys, label):
    P(f"\n--- {label} ---   n={int(r.nobs)}  R2={r.rsquared:.3f}")
    for k in r.params.index:
        if any(kk in k for kk in keys): P(f"  {k:40s} {r.params[k]:7.2f}  (se {r.bse[k]:5.2f})  p={r.pvalues[k]:.3f}")
for area in ("rural", "total"):
    d = lc[(lc.area == area) & lc.age_1926.isin(ADULT) & lc.gain_pp.between(-40, 90)]
    show(fit("gain_pp ~ C(coh) * female + C(rayon)", d), ["female"], f"B9a. Rayon level, area={area}: gain 1926->1939 ~ cohort x female + rayon FE")
    P("   cell means (pop-weighted):\n   " + d.groupby(["age_1926", "sex"]).apply(lambda t: np.average(t.gain_pp, weights=t.pop_1926)).unstack().round(1).to_string().replace("\n", "\n   "))
d = lc[(lc.area == "rural") & lc.age_1926.isin(ADULT) & lc.gain_pp.between(-40, 90)]
show(fit("gain_pp ~ C(coh) + female + female:young + C(rayon)", d), ["female"], "B9b. Rural pooled: female + female x young")
show(fit("gain_pp ~ C(coh) + female + female:young + C(rayon)", d[d.approx_borders == 0]), ["female"], "B9c. Rural, rayons with exact 1926/1939 correspondence only")
show(fit("gain_pp ~ C(coh) + female + female:young + survival + C(rayon)", d), ["female", "survival"], "B9d. Rural + survival")
d["age1928"] = d.age_1926.map({"20-24": 23.5, "25-29": 28.5, "30-34": 33.5, "35-39": 38.5, "40-44": 43.5, "45-49": 48.5})
show(fit("gain_pp ~ age1928 * female + C(rayon)", d), ["age1928", "female"], "B9e. Rural, linear in age x female")
g = d.pivot_table(index=["rayon", "age_1926"], columns="sex", values=["lit_1926", "lit_1939"]).reset_index()
g.columns = ["rayon", "age_1926", "l26F", "l26M", "l39F", "l39M"]; g["gap26"] = g.l26M - g.l26F; g["gap39"] = g.l39M - g.l39F
P("\nB9f. Gender gap within cohorts, rural, mean over rayons:\n" + g.groupby("age_1926")[["gap26", "gap39"]].mean().reindex(ADULT).round(1).to_string())
P("\n   Rayon table, rural women aged 23-32 in 1926: level 1926 and gain")
w = d[(d.sex == "F") & d.age_1926.isin(["25-29", "30-34"])].groupby("rayon").agg(lit26_F=("lit_1926", "mean"), gain_F=("gain_pp", "mean"), pop=("pop_1926", "sum")).reset_index()
m = d[(d.sex == "M") & d.age_1926.isin(["25-29", "30-34"])].groupby("rayon").agg(lit26_M=("lit_1926", "mean"), gain_M=("gain_pp", "mean")).reset_index()
w = w.merge(m, on="rayon"); P("   " + w.sort_values("gain_F", ascending=False).round(1).to_string(index=False).replace("\n", "\n   "))
r = smf.wls("gain_F ~ lit26_F", data=w, weights=w["pop"]).fit(cov_type="HC1"); P(f"\n   convergence women: slope {r.params['lit26_F']:.2f} (p={r.pvalues['lit26_F']:.3f})")
r = smf.wls("gain_M ~ lit26_M", data=w, weights=w["pop"]).fit(cov_type="HC1"); P(f"   convergence men:   slope {r.params['lit26_M']:.2f} (p={r.pvalues['lit26_M']:.3f})")
open(f"{R}/B9_wave2_rayon.txt", "w", encoding="utf-8").write("\n".join(out))

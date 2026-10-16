"""District-level crosswalk 1897 uezds -> 1926 autonomous units, with population fractions.
Baselines are recomputed as fraction x population weighted averages over districts and validated
against Vol. 9 Table XV (1897 figures recomputed by ЦСУ to 1927 borders).
Outputs (data/): crosswalk_1897_districts_to_1926_units.csv, baseline_pre1917_by_region1926_v2.csv,
crosswalk_validation_vs_tableXV.csv, merged_gaps_baseline.csv (updated)
"""
import os, sys
import pandas as pd, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = f"{ROOT}/external/malein"   # replication/data of ICPSR 231104, see README
D = f"{ROOT}/data"

# fraction = approximate share of the 1897 uezd's population that lay inside the 1926 unit on 17 Dec 1926
XW = {
 "TAT": [("kazanskij", 1.0), ("laishevskij", 1.0), ("mamdyshskij", 1.0), ("sviyazhskij", 1.0), ("spasskij_kazan", 1.0),
         ("tetyshskij", 1.0), ("chistopolskij", 1.0), ("menzilinskij", 1.0), ("bugulminskij", 0.70),
         ("buinskij", 0.45), ("simbirskij", 0.05), ("elabuzhskij", 0.55), ("malmyzhskij", 0.35), ("sarapulskij", 0.05)],
 "CHU": [("cheboksarskij", 0.90), ("civilskij", 1.0), ("yadrinskij", 1.0), ("kozmodemyznskij", 0.45),
         ("alatyrskij", 0.75), ("buinskij", 0.40), ("kurmyshskij", 0.50)],
 "MAR": [("tsarevokokshayskij", 1.0), ("kozmodemyznskij", 0.55), ("cheboksarskij", 0.10),
         ("urzhumskij", 0.35), ("yaranskij", 0.30), ("vasilsurskij", 0.05)],
 "VOT": [("glazovskij", 0.85), ("sarapulskij", 0.60), ("malmyzhskij", 0.45), ("elabuzhskij", 0.45)],
 "BAS": [("ufimskij", 1.0), ("birskij", 1.0), ("belebeyskij", 1.0), ("sterlitamakskij", 1.0), ("zlatoustovskij", 0.50),
         ("orenburgskij", 0.30), ("orskij", 0.40), ("verhneuralskij", 0.35), ("troitskij_orenburgskij", 0.15),
         ("chelyabinskij", 0.10), ("krasnoufimskij", 0.15), ("osinskij", 0.20), ("buguruslanskij", 0.15)],
 "KAR": [("petrozavodskoij", 1.0), ("oloneckij", 1.0), ("poveneckij", 1.0), ("pudozhskij", 1.0), ("kemskij", 0.90)],
}
NOTE = ("Expert crosswalk v1 (composition of 1926 units by 1897 uezds; fractions = approximate population shares). "
        "To be refined with the 1897 GIS (Distr_ID = Malein Id) and 1926 unit boundaries.")

p = pd.read_stata(M + "/panel1879_1911.dta", convert_categoricals=False)
g = pd.read_stata(M + "/data_from_gelbach.dta", convert_categoricals=False)
d = p.drop_duplicates("district").set_index("district")
d11 = p[p.year == 1911].set_index("district")
d94 = p[p.year == 1894].set_index("district")
gg = g.drop_duplicates("district").set_index("district")

rows = []
for code, items in XW.items():
    for dist, frac in items:
        if dist not in d.index:
            print("!! district not found:", dist); continue
        r = d.loc[dist]
        pop97 = gg["population"].get(dist, np.nan)
        pop11 = d11["pop_all"].get(dist, np.nan)
        pop = pop97 if pd.notna(pop97) else pop11
        rows.append(dict(region_code=code, district=dist, district_rus=r["district_rus"], province_rus=r["province_rus"],
            fraction=frac, pop_1897=pop97, pop_1911=pop11, weight=frac*pop,
            share_lit_1897=r["share_lit"], lit_f_1897=r["per_lit_f"],
            lit_m_1897_derived=(200*r["share_lit"] - r["per_lit_f"]) if pd.notna(r["per_lit_f"]) else np.nan,
            share_serfs_1858=r["share_serfs"], old_believers_1867=r["share_old_beleivers1867"],
            muslim_1867=r["share_muslim1867"], lingfrac_1897=gg["lingfrac_1897"].get(dist, np.nan),
            sh_russian_1897=gg["sh_russian_1897"].get(dist, np.nan), sh_muslim_1870=gg["sh_muslim_1870"].get(dist, np.nan),
            enrollment_1894=d94["enrollment_rate"].get(dist, np.nan), enrollment_1911=d11["enrollment_rate"].get(dist, np.nan),
            school_density_1911=d11["school_density"].get(dist, np.nan), teachers_pc_1911=d11["teachers_percap"].get(dist, np.nan),
            zemstvo_edu_pc_1894=d94["exp_zemstvo_edu_percap"].get(dist, np.nan), zemstvo=r["zemstvo_prov"]))
xw = pd.DataFrame(rows)
xw.to_csv(f"{D}/crosswalk_1897_districts_to_1926_units.csv", sep=";", index=False, encoding="utf-8-sig")

VARS = ["share_lit_1897", "lit_f_1897", "lit_m_1897_derived", "share_serfs_1858", "old_believers_1867", "muslim_1867",
        "lingfrac_1897", "sh_russian_1897", "sh_muslim_1870", "enrollment_1894", "enrollment_1911",
        "school_density_1911", "teachers_pc_1911", "zemstvo_edu_pc_1894", "zemstvo"]
def wavg(df, w="weight"):
    out = {}
    for c in VARS:
        m = df[c].notna() & df[w].notna() & (df[w] > 0)
        out[c] = float(np.average(df.loc[m, c], weights=df.loc[m, w])) if m.any() else np.nan
    out["n_districts"] = len(df); out["n_full"] = int((df.fraction == 1).sum())
    out["pop_1897_est"] = float(df["weight"].sum())
    return pd.Series(out)
reg = xw.groupby("region_code").apply(wavg).reset_index()
reg["method"] = "uezd crosswalk v1 (fraction x pop weights)"
reg.to_csv(f"{D}/baseline_pre1917_by_region1926_v2.csv", sep=";", index=False, encoding="utf-8-sig")

# ---- validation against Table XV 1897 (ЦСУ recomputation to 1927 borders) ----
xv = pd.read_csv(f"{D}/tableXV_1926_1897_age_sex_literacy.csv", sep=";", encoding="utf-8-sig")
t = xv[(xv.census_year == 1897) & (xv.area == "total") & (xv.age == "TOTAL")]
def xv_rate(region, sex):
    s = t[(t.region_gosplan_1927 == region) & (t.sex == sex)]
    return float(100*s["literate"].iloc[0]/s["population"].iloc[0]) if len(s) else np.nan
val = []
# Bashkir ASSR is a Gosplan unit itself -> direct check
b = reg[reg.region_code == "BAS"].iloc[0]
val.append(dict(unit="Башкирская АССР", source="crosswalk v1", lit_all=100*b["share_lit_1897"], lit_f=b["lit_f_1897"], lit_m=b["lit_m_1897_derived"]))
val.append(dict(unit="Башкирская АССР", source="Table XV 1897 (ЦСУ)", lit_all=np.nan, lit_f=xv_rate("Башкирская АССР", "F"), lit_m=xv_rate("Башкирская АССР", "M")))
# whole provinces vs Gosplan regions that contain them (sanity of level, not of crosswalk)
prov = d.reset_index()
for name, provs, gos in [("Вятский район ≈ Вятская губ.", ["вятская"], "Вятский район"),
                         ("Средне-Волжский ≈ Казанская+Симбирская+Самарская+Пензенская+Оренбургская", ["казанская", "симбирская", "самарская", "пензенская", "оренбургская"], "Средне-Волжский район"),
                         ("Лен.-Карельский ≈ СПб+Олонецкая+Новгородская+Псковская", ["санкт-петербургская", "олонецкая", "новгородская", "псковская"], "Ленинградско-Карельский район")]:
    s = prov[prov.province_rus.isin(provs)].copy()
    s["w"] = s["district"].map(gg["population"])
    m = s["w"].notna()
    la = 100*np.average(s.loc[m, "share_lit"], weights=s.loc[m, "w"]); lf = np.average(s.loc[m, "per_lit_f"], weights=s.loc[m, "w"])
    val.append(dict(unit=name, source="Malein districts (pop-weighted)", lit_all=la, lit_f=lf, lit_m=2*la-lf))
    val.append(dict(unit=name, source="Table XV 1897 (ЦСУ)", lit_all=np.nan, lit_f=xv_rate(gos, "F"), lit_m=xv_rate(gos, "M")))
val = pd.DataFrame(val).round(1)
val.to_csv(f"{D}/crosswalk_validation_vs_tableXV.csv", sep=";", index=False, encoding="utf-8-sig")

# ---- update merged gaps ----
gaps = pd.read_csv(f"{D}/tableIX_cohort_gaps.csv", sep=";", encoding="utf-8-sig")
keys = pd.read_csv(f"{D}/region_keys.csv", sep=";", encoding="utf-8-sig")
gaps["region_code"] = gaps["region"].map(dict(zip(keys["region_1926"], keys["region_code"])))
merged = gaps.merge(reg.drop(columns=["method"]), on="region_code", how="left")
merged.to_csv(f"{D}/merged_gaps_baseline.csv", sep=";", index=False, encoding="utf-8-sig")

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(reg[["region_code", "n_districts", "n_full", "pop_1897_est", "share_lit_1897", "lit_f_1897", "lit_m_1897_derived",
           "lingfrac_1897", "sh_russian_1897", "sh_muslim_1870", "enrollment_1911", "zemstvo_edu_pc_1894"]].round(3).to_string(index=False))
print("\nVALIDATION vs Table XV 1897:")
print(val.to_string(index=False))

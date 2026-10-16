"""Samples -> stata/data/*.dta (version 118, with variable labels) for stata/ABC_of_Communism.do.
Reads the cell files that paper_numbers.py writes to results/, so Stata gets exactly the same cells. Run after paper_numbers.py."""
import os, re, sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"; R = f"{ROOT}/results"; S = f"{ROOT}/stata/data"
os.makedirs(S, exist_ok=True)
for f_ in os.listdir(S):
    if f_.endswith(".dta"): os.remove(f"{S}/{f_}")
q = pd.read_csv(f"{D}/tableIX_region_quality.csv", sep=";", encoding="utf-8-sig")
LOWQ = set(q[(q.area == "rural") & (q.share_confirmed < 0.85)].region_1926)
BAD39 = {"Немцев Поволжья АССР", "Нижегородская губ.", "Ленинградская губ.", "Новгородская губ."}
URAL = {"Челябинский округ", "Свердловский округ", "Пермский округ", "Тюменский округ", "Тобольский округ", "Ишимский округ", "Курганский округ"}
MUSLIM_UNITS = {"Башкирская АССР", "Татарская АССР"}
def cname(c):
    c = re.sub(r"[^0-9a-zA-Z_]", "_", c).strip("_").lower()
    return ("v_" + c) if c[0].isdigit() else c
def save(df, name, labels, note):
    df = df.copy(); df.columns = [cname(c) for c in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]
    for c in df.columns:
        if df[c].dtype == object: df[c] = df[c].astype(str).replace("nan", "")
        if df[c].dtype == bool: df[c] = df[c].astype(int)
        if str(df[c].dtype) == "category": df[c] = df[c].astype(str)
    lab = {cname(k): v[:80] for k, v in labels.items()}
    df.to_stata(f"{S}/{name}.dta", write_index=False, version=118, variable_labels={k: v for k, v in lab.items() if k in df.columns}, data_label=note[:80])
    print(f"{name}.dta  rows={len(df)}  cols={len(df.columns)}")
def csv(name): return pd.read_csv(f"{R}/{name}", sep=";", encoding="utf-8-sig")

# 1. household regime: linked cohorts 1897 -> 1926 (Vol. 9, Table XV)
ORD1 = ["33-37", "38-42", "43-47", "48-52", "53-57", "58-62", "63-67"]
e1 = csv("E1_wave1_event_cells.csv"); e1["bin"] = e1.age_decree.map({b: i + 1 for i, b in enumerate(ORD1)}); e1["treated"] = e1.age_decree.isin(ORD1[:3]).astype(int)
e1["muslim_region"] = e1.region.isin(["Башкирская АССР", "Дагестанская АССР", "Казакская АССР", "Киргизская АССР", "Крымская АССР"]).astype(int)
e1["taught"] = 100 * e1.gain / (100 - e1.lit97); e1["illiterate97"] = e1.pop97 * (100 - e1.lit97) / 100
save(e1, "household_cells", {"region": "Gosplan region (borders of 1927)", "area": "total, urban or rural", "sex": "M or F", "age_decree": "age at the decree of December 1919", "pop97": "population of the cohort in 1897",
     "pop26": "population of the cohort in 1926", "lit97": "literacy in 1897, per cent", "lit26": "literacy in 1926, per cent", "gain": "lit26 minus lit97, points", "survival": "pop26 / pop97", "female": "1 = women",
     "bin": "cohort 1 (33-37) to 7 (63-67, reference)", "treated": "1 = aged 33-47 at the decree", "muslim_region": "1 = Bashkir, Dagestan, Kazak, Kirgiz, Crimean", "taught": "gain / (100 - lit97), per cent",
     "illiterate97": "illiterate persons of the cohort in 1897"}, "Household regime: linked five-year cohorts 1897-1926")
xv = pd.read_csv(f"{D}/tableXV_linked_cohorts.csv", sep=";", encoding="utf-8-sig"); xv = xv[xv.region != "РСФСР"].copy(); xv["female"] = (xv.sex == "F").astype(int)
xv["cohort_c"] = xv.cohort.map({"born 1878-87 (school-age in 1897)": 1, "born 1868-77 (adults in 1897)": 2, "born 1858-67": 3}); xv["muslim_region"] = xv.region.isin(["Башкирская АССР", "Дагестанская АССР", "Казакская АССР", "Киргизская АССР", "Крымская АССР"]).astype(int)
save(xv, "household_tenyear", {"cohort_c": "1 = aged 33-42 at the decree, 2 = 43-52, 3 = 53-62 (reference)", "gain_pp": "literacy 1926 minus 1897, points", "survival_ratio": "pop 1926 / pop 1897"}, "Household regime: linked ten-year cohorts 1897-1926")

# 2. state regime: linked cohorts 1926 -> 1939
ADULT = ["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48-52", "53-57"]
def state(d):
    d = d.copy(); d["coh_c"] = d.age_1926.map({b: i + 1 for i, b in enumerate(ADULT)}); d["placebo"] = d.age_1926.isin(ADULT[6:]).astype(int)
    d["lowq"] = d.unit_1926.isin(LOWQ).astype(int); d["ural"] = d.unit_1926.isin(URAL).astype(int); d["tatbash"] = d.unit_1926.isin(MUSLIM_UNITS).astype(int)
    d["taught"] = 100 * d.gain_pp / (100 - d.lit_1926); d["illiterate26"] = d.pop_1926 * (100 - d.lit_1926) / 100
    d["ncoh"] = d.groupby("unit_1926").age_1926.transform("nunique"); return d
LAB2 = {"unit_1926": "unit of 1926", "region_1939": "successor of 1939", "age_1926": "age in 1926", "pop_1926": "population of the cohort in 1926", "pop_1939": "population in 1939", "lit_1926": "literacy in 1926, per cent",
        "lit_1939": "literacy in 1939, per cent", "gain_pp": "lit_1939 minus lit_1926, points", "survival": "pop_1939 / pop_1926", "tier": "validation test passed by the 1926 cell (1, 2 or 3)", "female": "1 = women",
        "titular": "1 = autonomous republic or oblast", "coh_c": "cohort 1 (18-22) to 8 (53-57, reference)", "young": "1 = aged 18-32 in 1926", "middle": "1 = aged 33-47", "placebo": "1 = aged 48-57 (above the age limit)",
        "fy": "female x young", "fm": "female x middle", "age1928": "mid-point of the age in 1928", "lowq": "1 = low-quality rural pages of Table IX", "ural": "1 = Ural okrug matched to a larger oblast",
        "tatbash": "1 = Tatar or Bashkir republic", "taught": "gain_pp / (100 - lit_1926), per cent", "illiterate26": "illiterate persons of the cohort in 1926", "ncoh": "number of cohorts of the unit in the sample"}
save(state(csv("W2_cells.csv")), "state_cells", LAB2, "State regime: linked cohorts 1926-1939, rural, baseline sample")
save(state(csv("W2_cells_total.csv")), "state_cells_total", LAB2, "State regime: linked cohorts 1926-1939, total population")
lc = pd.read_csv(f"{D}/linked_cohorts_1926_1939.csv", sep=";", encoding="utf-8-sig"); lc["female"] = (lc.sex == "F").astype(int); lc["titular"] = lc.unit_1926.str.contains("АССР|АО").astype(int)
fl = lc[(lc.area == "rural") & lc.age_1926.isin(ADULT) & lc.gain_pp.between(-40, 90)]; fl = fl[fl.groupby(["unit_1926", "area", "age_1926"]).sex.transform("nunique") == 2].copy()
fl["young"] = fl.age_1926.isin(ADULT[:3]).astype(int); fl["middle"] = fl.age_1926.isin(ADULT[3:6]).astype(int); fl["fy"] = fl.female * fl.young; fl["fm"] = fl.female * fl.middle; fl["bad39"] = fl.unit_1926.isin(BAD39).astype(int)
save(state(fl), "state_cells_flagged", dict(LAB2, bad39="1 = unit whose successor of 1939 is not comparable"), "State regime: rural cells including the flagged units")
ry = csv("B9_rayon_cells.csv"); AD2 = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54"]; ry["coh_c"] = ry.age_1926.map({b: i + 1 for i, b in enumerate(AD2)}); ry["taught"] = 100 * ry.gain_pp / (100 - ry.lit_1926); ry["illiterate26"] = ry.pop_1926 * (100 - ry.lit_1926) / 100
save(ry, "state_region_cells", {"rayon": "Gosplan region", "gain_pp": "literacy 1939 minus 1926, points", "approx_borders": "1 = borders of 1926 and 1939 do not coincide", "coh_c": "cohort 1 (20-24) to 7 (50-54)", "young": "1 = aged 20-34 in 1926",
     "middle": "1 = aged 35-49", "taught": "gain_pp / (100 - lit_1926), per cent", "illiterate26": "illiterate persons of the cohort in 1926"}, "State regime: replication on Gosplan regions, rural")
wu = csv("B7_unit_level_wave2.csv").rename(columns={"unit_1926": "region"}); c1 = csv("C_wave1_proxy_units.csv"); rb = csv("F_russians_units.csv")
wu["tatbash"] = wu.region.isin(MUSLIM_UNITS).astype(int); PZ = ["teachers_percap_1911_z", "urban_share_M_z", "cwr_z", "agshare_1897_z"]
wu = wu.merge(rb[["region", "pg"] + PZ], on="region", how="left")
for c in ("lit26_F", "lit26_M"): wu[c + "_z"] = (wu[c] - wu[c].mean()) / wu[c].std()
wu3 = None
save(wu, "state_units", {"gain_F": "gain 1926-1939 of women aged 23-32, points", "gain_M": "gain of men aged 23-32", "lit26_F": "literacy of women aged 23-32 in 1926", "lit26_M": "literacy of men aged 23-32 in 1926", "pop": "women aged 23-32 in 1926",
     "titular": "1 = autonomous republic or oblast", "surv": "survival ratio, mean of the two cohorts", "tatbash": "1 = Tatar or Bashkir republic"}, "State regime at the unit level, cohort aged 23-32, rural")
cl = csv("W2_cells.csv"); sub = cl[cl.age_1926.isin(ADULT[:3])]
w3 = sub[sub.sex == "F"].groupby("unit_1926").agg(gain_F=("gain_pp", "mean"), lit26_F=("lit_1926", "mean"), pop=("pop_1926", "sum"), titular=("titular", "max"), ncoh=("gain_pp", "size")).reset_index()
w3 = w3.merge(sub[sub.sex == "M"].groupby("unit_1926").agg(gain_M=("gain_pp", "mean"), lit26_M=("lit_1926", "mean")).reset_index(), on="unit_1926"); w3 = w3[w3.ncoh == 3]
save(w3.rename(columns={"unit_1926": "region"}), "state_units_1832", {"gain_F": "gain 1926-1939 of women aged 18-32, points"}, "State regime at the unit level, cohorts aged 18-32, rural")
c1 = c1.merge(rb[["region", "pg"] + PZ], on="region", how="left")
save(c1, "household_units", {"w1_F": "literacy of Russian women aged 40-49 minus 60-69, rural, 1926", "w1_M": "the same for men"}, "Household regime at the unit level: Russians, 1926")

# 3. the 1926 cross-section
CB = ["40-49", "30-39", "25-29", "20-24", "15-19", "12-14"]
def within(d):
    d = d.copy(); d["band_n"] = d.band.map({b: i + 1 for i, b in enumerate(CB)}); d["lowq"] = d.region.isin(LOWQ).astype(int); d["autonomous"] = d.region.str.contains("АССР|АО").astype(int)
    d["logodds"] = np.log(d.literacy.clip(0.5, 99.5) / (100 - d.literacy.clip(0.5, 99.5))); d["with_nat"] = d.region.isin(set(d[d.nonrus == 1].region)).astype(int); d["nr_f"] = d.nonrus * d.female; d["nr_f_m"] = d.nr_f * d.muslim
    return d.drop(columns=["band_c"], errors="ignore")
LAB3 = {"region": "unit of 1926", "group": "nationality", "band": "age in 1926", "band_n": "cohort 1 (40-49) to 6 (12-14)", "population": "population of the cell", "literate": "literate persons", "literacy": "literacy, per cent",
        "tier": "validation test passed (1, 2 or 3)", "female": "1 = women", "nonrus": "1 = non-Russian", "volga": "1 = Chuvash, Mari, Mordva, Votyaks", "muslim": "1 = Tatars, Bashkirs, Mishars, Kazakhs", "other": "1 = other non-Russian",
        "young": "1 = aged 12-29", "rc": "unit x cohort", "gc": "nationality x cohort", "sc": "sex x cohort", "vf": "volga x female", "vfy": "volga x female x young", "mf": "muslim x female", "mfy": "muslim x female x young",
        "lowq": "1 = low-quality rural pages", "autonomous": "1 = autonomous republic or oblast", "logodds": "ln(literacy / (100 - literacy))", "with_nat": "1 = unit with a non-Russian nationality in the sample",
        "titular_unit": "1 = nationality in its titular unit"}
save(within(csv("D_core_cells.csv")), "within_cells", LAB3, "1926: unit x nationality x sex x cohort, rural, Russians and seven nationalities")
save(within(csv("D_all_cells.csv")), "within_cells_all", LAB3, "1926: the same with all enumerated nationalities")
save(within(csv("D_core_cells_total.csv")), "within_cells_total", LAB3, "1926: the same for the total population")
k3 = csv("E_korenizatsiya_cells.csv"); k3["band_n"] = k3.band.map({b: i + 1 for i, b in enumerate(CB)})
save(k3.drop(columns=["band_c"], errors="ignore"), "korenizatsiya_cells", dict(LAB3, soviet="1 = aged 12-19 (schooled under Soviet rule)", gsc="nationality x sex x cohort"), "1926: six nationalities inside and outside their titular units, rural")
rb["lowq"] = rb.region.isin(LOWQ).astype(int); rb["autonomous"] = rb.region.str.contains("АССР|АО").astype(int); rb["okrug"] = rb.region.str.contains("округ").astype(int)
save(rb, "russians_units", {"region": "unit of 1926", "pg": "province or provinces of 1897 from which the unit was formed (cluster)", "teachers_percap_1911": "teachers per 1,000 population, 1911", "exp_zemstvo_edu_pc_1894": "zemstvo spending on education per head, 1894", "agshare_1897": "agrarian share, 1897, per cent",
     "cwr": "children under 5 per 100 women aged 15-49, 1926", "sr_20_39": "men per 100 women aged 20-39, rural", "urban_share_M": "urban share of men aged 20-39, per cent", "per_lit_f": "female literacy in 1897, per cent",
     "gender_gap_20-24": "male minus female literacy, rural Russians aged 20-24", "lit_F_20-24": "literacy of rural Russian women aged 20-24", "lit_M_20-24": "literacy of rural Russian men aged 20-24"}, "1926: rural Russians by unit with the pre-1917 baseline")
save(csv("G_mechanism_cells.csv"), "nationalities_cells", {"ethgap_F_20-24": "Russian minus nationality literacy, women aged 20-24", "ethgap_M_20-24": "the same, men", "ethgap_F_12-14": "the same, girls aged 12-14",
     "cwr_diff": "child-woman ratio, nationality minus Russians", "sr_20_39_diff": "men per 100 women aged 20-39, difference", "urban_share_M_diff": "urban share of men, difference", "mob_gap_diff": "male minus female urban share, difference",
     "muslim": "1 = Muslim nationality", "pop": "population of the nationality in the unit"}, "1926: nationality x unit, differences from Russians of the same unit, rural")
save(pd.read_csv(f"{D}/tableIX_cohort_gaps.csv", sep=";", encoding="utf-8-sig"), "six_titular_units", {"gap_M": "Russian minus titular literacy, men", "gap_F": "the same, women"}, "1926: ethnic gaps by cohort in six titular units")

# 4. two regimes
for nm, f_ in (("tworegime_cells", "T_two_regime_cells.csv"), ("tworegime_cells_middle", "T_two_regime_cells_middle.csv")):
    t = csv(f_); t["lowq"] = t.unit.isin(LOWQ).astype(int)
    save(t.rename(columns={"T": "reach"}), nm, {"unit": "unit of 1926", "y": "literacy in 1926 (household regime) or gain 1926-1939 (state regime)", "wt": "population weight, normalised within regime", "reach": "1 = cohort the regime could reach",
         "female": "1 = women", "phase2": "1 = state regime", "cohfe": "cohort within regime", "up": "unit within regime", "lowq": "1 = low-quality unit"}, "Two-regime test: stacked cells of the two regimes")
clc = state(csv("W2_cells.csv")); w1s = csv("T_two_regime_cells.csv"); w1s = w1s[w1s.phase2 == 0][["unit", "y", "wt", "T", "female", "phase2", "cohfe"]]
w2c = clc[clc.age_1926.isin(ADULT[:3] + ADULT[6:])].copy(); w2c["T"] = w2c.young; w2c["y"] = w2c.taught; w2c["wt"] = w2c.illiterate26; w2c["unit"] = w2c.unit_1926; w2c["phase2"] = 1; w2c["cohfe"] = "p2_" + w2c.age_1926
w1s["wt"] = w1s.wt * 1.0; st = pd.concat([w1s, w2c[["unit", "y", "wt", "T", "female", "phase2", "cohfe"]]]); st["wt"] = st.wt / st.groupby("phase2").wt.transform("sum"); st["up"] = st.unit + "|" + st.phase2.astype(str)
st = st.merge(rb[["region", "pg"] + PZ], left_on="unit", right_on="region", how="left"); st["pg"] = st.pg.fillna(st.unit)
save(st.rename(columns={"T": "reach"}), "tworegime_cells_taught", {"y": "literacy in 1926 (household) or share of the illiterate taught (state)"}, "Two-regime test with the share taught as the outcome of the state regime")

# 5. legacy
save(csv("J1_ethnic_gap_2010_by_sex_age.csv"), "legacy_cohorts_2010", {"nat": "nationality", "age": "age in 2010", "gap_sec": "Russians minus nationality, share with full secondary education", "gap_higher": "the same, higher education",
     "gap_basic": "the same, eight-year schooling", "pop": "population of the cell", "female": "1 = women", "old": "1 = born before 1951", "mid": "1 = born 1951-1960", "fo": "female x old", "fmid": "female x mid",
     "na": "nationality x age", "sa": "sex x age"}, "2010: ethnic education gaps by sex and age, six nationalities")
save(csv("S_legacy_sexdiff_cells.csv"), "legacy_sexdiff_cells", {"D_ad": "female minus male ethnic literacy gap of 1926, ages 20-49", "D_yg": "the same, ages 12-29", "gF_ad": "female ethnic literacy gap of 1926", "gM_ad": "male ethnic literacy gap of 1926",
     "units_ad": "units of 1926 in which the nationality is observed"}, "2010 by nationality, sex and age with the sex difference of 1926")
J2 = csv("J2_ethnic_gaps_1926_2010.csv"); J2["six"] = J2.nat2010.isin(["Татары", "Башкиры", "Чуваши", "Марийцы", "Удмурты", "Мордва"]).astype(int)
save(J2, "legacy_subject_cells", {"subject": "subject of the Federation, 2010", "nat2010": "nationality", "area": "total or rural", "gF": "female ethnic literacy gap of 1926, ages 20-49", "gM": "male ethnic literacy gap of 1926",
     "g10": "gap of 2010 in the share with full secondary education", "g10h": "gap of 2010 in higher education", "g10i": "gap of 2010 in illiteracy (nationality minus Russians)", "g10adj": "gap of 2010 standardised to the age structure of Russians",
     "stated": "population of 2010 stating its education", "muslim": "1 = Tatars, Bashkirs", "titular": "1 = nationality in its titular subject", "rural_diff": "rural share, nationality minus Russians", "six": "1 = one of six Volga and Ural nationalities"},
     "Nationality x subject: education gaps of 2010 and literacy gaps of 1926")
save(csv("I_intergen_units.csv"), "children_1939", {"kid39F": "literacy of girls aged 9-14 in 1939, rural", "kid39M": "the same, boys", "gF": "gain 1926-1939 of women aged 18-32", "gM": "the same, men", "kid26F": "literacy of girls aged 8-12 in 1926",
     "kid26M": "the same, boys", "kidpop": "children aged 9-14 in 1939", "gap39": "boys minus girls, 1939", "gap26": "boys minus girls, 1926"}, "Children of 1939 and the gains of their parents' cohorts")

# 6. validated and raw tables
save(pd.read_csv(f"{D}/tableIX_bands_validated.csv", sep=";", encoding="utf-8-sig"), "validated_bands_1926", {"tier": "validation test passed (1, 2 or 3)"}, "1926 Table IX: validated cells by age band")
save(pd.read_csv(f"{D}/tableIX_five_year_groups_validated.csv", sep=";", encoding="utf-8-sig"), "validated_five_year_groups_1926", {"P_pop": "printed subtotal, population", "S_pop": "sum of single years, population", "val_pop": "validated population",
     "tier": "0 = dropped, 1 = printed subtotal, 2 = identity, 3 = adjacent cohorts"}, "1926 Table IX: five-year groups with the record of validation")
save(pd.read_csv(f"{D}/census1926_tableIX_long.csv", sep=";", encoding="utf-8-sig", dtype={"age": str}), "raw_tableIX_1926", {"total": "population", "literate": "literate persons"}, "RAW: 1926 census, Table IX, as transcribed")
save(pd.read_csv(f"{D}/census1939_literacy_by_region_age_sex.csv", sep=";", encoding="utf-8-sig", dtype={"age": str}), "raw_census_1939", {}, "RAW: 1939 census, RGAE 1562/336, via Demoscope")
save(pd.read_csv(f"{D}/census1959_rsfsr_edu_by_age_sex.csv", sep=";", encoding="utf-8-sig", dtype={"age": str}), "raw_census_1959", {"literacy": "literate persons per 100 persons stating their education"}, "RAW: 1959 census, RSFSR by area, sex and age, via Demoscope")
save(pd.read_csv(f"{D}/tableXV_1926_1897_age_sex_literacy.csv", sep=";", encoding="utf-8-sig", dtype={"age": str}), "raw_tableXV", {}, "RAW: 1926 census, Vol. 9, Table XV")
save(pd.read_csv(f"{D}/census2010_nat_edu_by_subject.csv", sep=";", encoding="utf-8-sig"), "raw_census2010_t14", {}, "RAW: 2010 census, Vol. 4, Table 14")
save(pd.read_csv(f"{D}/census2010_nat_edu_by_age_sex.csv", sep=";", encoding="utf-8-sig"), "raw_census2010_t13", {}, "RAW: 2010 census, Vol. 4, Table 13")
print("done ->", S)

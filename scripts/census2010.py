"""Parses three tables of the 2010 census (Rosstat, Vol. 4 t. 13 and t. 14, Vol. 3 t. 1) downloaded by rosstat_get.py.
Outputs: data/census2010_*.csv. (The first part of legacy2010.py, which also ran the tests of an earlier version.)"""
import os, re, sys, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = f"{ROOT}/sources/census2010"; D = f"{ROOT}/data"
out = []
def P(*a):
    s = " ".join(str(v) for v in a); print(s); out.append(s)
def num(v):
    try: return float(str(v).replace(" ", "").replace("\xa0", ""))
    except: return np.nan
COLS = ["total", "stated", "postgrad", "higher", "bach", "spec", "master", "inc_higher", "sec_voc", "prim_voc", "sec_gen", "basic_gen", "prim_gen", "no_prim", "illiterate", "not_stated"]
def shares(d):
    d = d.copy()
    d["sh_higher"] = 100 * (d.postgrad + d.higher) / d.stated
    d["sh_sec_plus"] = 100 * (d.postgrad + d.higher + d.inc_higher + d.sec_voc + d.prim_voc + d.sec_gen) / d.stated
    d["sh_basic_plus"] = d.sh_sec_plus + 100 * d.basic_gen / d.stated
    d["sh_illit"] = 100 * d.illiterate / d.stated
    d["sh_noprim"] = 100 * d.no_prim / d.stated
    return d
AGE = re.compile(r"^\d+\s*[–-]\s*\d+$|^70 и более$|^\d+\s*[–-]\s*\d+\s*лет$")
def area_of(s):
    s = s.strip().lower()
    if s.startswith("городское и сельское"): return "total"
    if s.startswith("городское"): return "urban"
    if s.startswith("сельское"): return "rural"
    return None

# ---------- Vol.4 t.14: nationality x subject x area (15+) ----------
a = pd.read_excel(f"{S}/pub-04-14.xlsx", header=None)
rows = []; region = None; area = None
for i in range(7, len(a)):
    lab = str(a.iat[i, 3]).replace("\n", " ").strip(); n0 = a.iat[i, 0]
    if lab == "nan": continue
    ar = area_of(lab)
    if pd.isna(n0) and ar is None: region = lab; continue
    if ar is not None:
        area = ar; nat = "ALL"
    else: nat = lab
    vals = [num(a.iat[i, c]) for c in range(4, 20)]
    if np.isnan(vals[0]): continue
    rows.append(dict(region=region, area=area, nationality=nat, **dict(zip(COLS, vals))))
t14 = shares(pd.DataFrame(rows)); t14 = t14[~t14.region.str.contains("федеральный округ|Российская Федерация", regex=True)]
t14.to_csv(f"{D}/census2010_nat_edu_by_subject.csv", sep=";", index=False, encoding="utf-8-sig")
P("t14: subjects", t14.region.nunique(), "rows", len(t14))

# ---------- Vol.4 t.13: nationality x sex x age (national) ----------
b = pd.read_excel(f"{S}/pub-04-13.xlsx", header=None)
rows = []; area = None; sex = None; nat = None; skip = False
for i in range(7, len(b)):
    lab = str(b.iat[i, 4]).replace("\n", " ").strip(); n0 = b.iat[i, 0]
    if lab == "nan": continue
    ar = area_of(lab)
    if ar is not None and pd.isna(n0): area = ar; continue
    if lab.startswith("Мужчины и женщины"): sex = "B"; continue
    if lab.startswith("Мужчины"): sex = "M"; continue
    if lab.startswith("Женщины"): sex = "F"; continue
    if lab.startswith("в том числе в возрасте"): skip = False; continue
    if lab.startswith("Из общей численности"): skip = True; continue
    if pd.isna(n0): continue
    vals = [num(b.iat[i, c]) for c in range(5, 21)]
    if AGE.match(lab):
        if skip: continue
        rows.append(dict(area=area, sex=sex, nationality=nat, age=re.sub(r"\s*[–-]\s*", "-", lab), **dict(zip(COLS, vals))))
    else:
        nat = lab; skip = False
        rows.append(dict(area=area, sex=sex, nationality=nat, age="15+", **dict(zip(COLS, vals))))
t13 = shares(pd.DataFrame(rows)); t13.to_csv(f"{D}/census2010_nat_edu_by_age_sex.csv", sep=";", index=False, encoding="utf-8-sig")
P("t13: nationalities", t13.nationality.nunique(), "rows", len(t13))

# ---------- Vol.3 t.1: subject x sex x age ----------
c = pd.read_excel(f"{S}/pub-03-01.xlsx", header=None)
rows = []; region = None; area = None; sex = None; skip = False
for i in range(8, len(c)):
    lab = str(c.iat[i, 1]).replace("\n", " ").strip(); n0 = c.iat[i, 0]
    if lab == "nan": continue
    ar = area_of(lab)
    if ar is not None: area = ar; continue
    if lab.startswith("Из общей численности - население"): skip = True; continue
    if lab.startswith("Из общей численности - мужчины") or lab.startswith("Из общей численности - женщины"): skip = False; continue
    if lab.startswith("в том числе в возрасте"): continue
    vals = [num(c.iat[i, k]) for k in range(2, 18)]
    if lab.startswith("Мужчины и женщины"): sex = "B"; skip = False; rows.append(dict(region=region, area=area, sex=sex, age="15+", **dict(zip(COLS, vals)))); continue
    if lab.startswith("Мужчины в возрасте"): sex = "M"; skip = False; rows.append(dict(region=region, area=area, sex=sex, age="15+", **dict(zip(COLS, vals)))); continue
    if lab.startswith("Женщины в возрасте"): sex = "F"; skip = False; rows.append(dict(region=region, area=area, sex=sex, age="15+", **dict(zip(COLS, vals)))); continue
    if pd.isna(n0) and not AGE.match(lab): region = lab; continue
    if AGE.match(lab) and not skip and not np.isnan(vals[0]):
        rows.append(dict(region=region, area=area, sex=sex, age=re.sub(r"\s*[–-]\s*", "-", lab), **dict(zip(COLS, vals))))
t3 = shares(pd.DataFrame(rows)); t3 = t3[~t3.region.str.contains("федеральный округ|Российская Федерация", regex=True)]
t3.to_csv(f"{D}/census2010_edu_by_subject_age_sex.csv", sep=";", index=False, encoding="utf-8-sig")
P("t3: subjects", t3.region.nunique(), "rows", len(t3), "| ages:", sorted(t3.age.unique()))

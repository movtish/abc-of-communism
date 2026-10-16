"""Downloads from Demoscope Weekly the 1959 census table "Распределение населения РСФСР по возрасту и уровню образования"
(urban, rural and total population by sex and age, with the literate and the illiterate among those without primary education)
and writes data/census1959_rsfsr_edu_by_age_sex.csv. Used for the cohort check of the 1939 literacy figures."""
import io, os, re, sys, urllib.request, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "http://www.demoscope.ru/weekly/ssp/rus_edu_59.php"
raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("cp1251")
t = [x for x in pd.read_html(io.StringIO(raw)) if x.shape[0] > 100][0]
EDU = ["higher", "higher_incomplete", "secondary_special", "secondary_general", "secondary_incomplete", "seven_year", "seven_year_incomplete", "primary"]
rows = []; area = "urban"; sex = None
AREA = {"городское население": "urban", "сельское население": "rural", "все население": "total"}; SEX = {"мужчины": "M", "женщины": "F", "оба пола": "B"}
for i in range(3, len(t)):
    v = [str(x) for x in t.iloc[i].tolist()]
    if len(set(v)) == 1:
        if v[0] in AREA: area = AREA[v[0]]
        elif v[0] in SEX: sex = SEX[v[0]]
        continue
    def num(x):
        x = x.replace(" ", "").replace("\xa0", "")
        return float(x) if re.fullmatch(r"-?\d+(\.\d+)?", x) else float("nan")
    age = v[1].replace(" и старше", "+").replace("до 9 лет", "0-8").replace("Все население", "all").replace("возраст не указан", "unknown")
    r = dict(area=area, sex=sex, age=age, total=num(v[2]))
    for k, c in zip(EDU, v[3:11]): r[k] = num(c)
    r["literate_no_primary"] = num(v[11]); r["illiterate"] = num(v[12]); r["education_not_stated"] = num(v[13])
    rows.append(r)
d = pd.DataFrame(rows)
d["with_education"] = d[EDU].sum(axis=1, min_count=1)
d["literate"] = d.with_education.fillna(0) + d.literate_no_primary.fillna(0)
d["literacy"] = 100 * d.literate / (d.total - d.education_not_stated.fillna(0))
d.loc[d.age == "0-8", ["literate", "literacy"]] = float("nan")
d.to_csv(f"{ROOT}/data/census1959_rsfsr_edu_by_age_sex.csv", sep=";", index=False, encoding="utf-8-sig")
print(d[(d.area == "rural") & d.age.isin(["30-34", "40-44", "50-54", "55-59", "60-64", "65-69", "70+"])][["area", "sex", "age", "total", "illiterate", "literacy"]].to_string(index=False))
print("rows", len(d), "->", f"{ROOT}/data/census1959_rsfsr_edu_by_age_sex.csv")

"""Write the Russian article tables with decimal commas.

Read the jl.* keys in results/paper_numbers.json and the cohort file
results/J0_cohorts_1926_1939.csv. Write jnea/tables/tab_j*.tex."""

import os, sys, json
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = f"{ROOT}/results"
TB = f"{ROOT}/jnea/tables"
os.makedirs(TB, exist_ok=True)
J = json.load(open(f"{R}/paper_numbers.json", encoding="utf-8"))
NUM = {k: tuple(v) for k, v in J["NUM"].items()}
STR = J["STR"]


def f(v, d=1):
    s = f"{abs(v):,.{d}f}".replace(",", "~").replace(".", ",")
    return ("\\m " + s) if v < 0 else s


def n(key, d=None):
    if key in STR:
        return STR[key]
    v, dd = NUM[key]
    return f(v, int(dd) if d is None else d)


def cs(key, d=None):
    v, dd = NUM[key]
    d = int(dd) if d is None else d
    return f"{f(v, d)} ({f(NUM[key + '.se'][0], d)})"


def write(name, lines):
    open(f"{TB}/{name}.tex", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("table", name)


E = r" \\"
c0 = pd.read_csv(f"{R}/J0_cohorts_1926_1939.csv", sep=";", encoding="utf-8-sig")
c0 = c0[c0.sex == "T"]

# Follow the same cohorts in 1926 and 1939.
L = [
    r"\begin{tabular}{llrrrrrr}",
    r"\toprule",
    r"Возраст & Годы & Численность & \multicolumn{2}{c}{Грамотных, \%} & Прирост, & Научились, \% & Научились, \\",
    r"\cmidrule(lr){4-5}",
    r"в 1926 г. & рождения & в 1939 г., тыс. & 1926 г. & 1939 г. & п.п. & от неграмотных & тыс. чел."
    + E,
    r"\midrule",
]
for _, q in c0.iterrows():
    lo, hi = [int(x) for x in q.age26.split("-")]
    L.append(
        f"{q.age26} & {1926 - hi}-{1926 - lo} & {f(q.p39 / 1e3, 0)} & {f(q.l26)} & {f(q.l39)} & {f(q.d)} & {f(q.t, 0)} & {f(q.new / 1e3, 0)}"
        + E
    )
L += [
    r"\midrule",
    f"Дети и подростки 8-17 лет & & & & & & & {f(NUM['jl.new.young.T'][0] * 1e3, 0)}"
    + E,
    f"Взрослые 18-52 лет & & & & & & {n('jl.share.adult.T')} & {f(NUM['jl.new.adult.T'][0] * 1e3, 0)}"
    + E,
    f"Взрослые 18-52 лет за вычетом изменения в группе 53-57 лет & & & & & & & {f(NUM['jl.new.adultnet.T'][0] * 1e3, 0)}"
    + E,
    r"\bottomrule",
    r"\end{tabular}",
]
write("tab_j1", L)

# Decompose literacy growth at ages 20-49.
L = [
    r"\begin{tabular}{lrrrrrr}",
    r"\toprule",
    r" & \multicolumn{2}{c}{Грамотных, \%} & Прирост, & \multicolumn{2}{c}{В том числе, п.п.} & Доля обучения \\",
    r"\cmidrule(lr){2-3}\cmidrule(lr){5-6}",
    r" & 1926 г. & 1939 г. & п.п. & смена поколений & обучение & взрослых" + E,
    r" & & & & и школа & взрослых & в приросте, \%" + E,
    r"\midrule",
]
for sx, lab in (("T", "Оба пола"), ("M", "Мужчины"), ("F", "Женщины")):
    L.append(
        f"{lab} & {n(f'jl.dec.{sx}.l26')} & {n(f'jl.dec.{sx}.l39')} & {n(f'jl.dec.{sx}.d')} & {n(f'jl.dec.{sx}.ab')} & {n(f'jl.dec.{sx}.c')} & {n(f'jl.dec.{sx}.c.sh')}"
        + E
    )
L += [r"\bottomrule", r"\end{tabular}"]
write("tab_j2", L)

# Compare cohort gains by age.
L = [
    r"\begin{tabular}{lcc}",
    r"\toprule",
    r" & Все регионы & Регионы с неизменными границами" + E,
    r"\midrule",
    r"\multicolumn{3}{l}{\textit{А. Прирост грамотности, п.п.}}" + E,
    f"Поколения 20-34 лет в 1926 г. & {cs('jl.did.p')} & {cs('jl.didx.p')}" + E,
    f"Поколения 35-49 лет в 1926 г. & {cs('jl.did.pm')} & {cs('jl.didx.pm')}" + E,
    r"\multicolumn{3}{l}{\textit{Б. Доля научившихся среди неграмотных 1926 г., \%}}"
    + E,
    f"Поколения 20-34 лет в 1926 г. & {cs('jl.did.t')} & {cs('jl.didx.t')}" + E,
    f"Поколения 35-49 лет в 1926 г. & {cs('jl.did.tm')} & {cs('jl.didx.tm')}" + E,
    r"\midrule",
    f"Число наблюдений (регионов) & {n('jl.did.n')} ({n('jl.did.units')}) & {n('jl.didx.n')} ({n('jl.didx.units')})"
    + E,
    r"\bottomrule",
    r"\end{tabular}",
]
write("tab_j3", L)

# Compare the cohort aged 20-34 across regions.
yj = pd.read_csv(f"{R}/J1_regions.csv", sep=";", encoding="utf-8-sig").sort_values(
    "l26"
)
yj["taught"] = 100 * yj.gain / (100 - yj.l26)
L = [
    r"\begin{tabular}{lrrrrr}",
    r"\toprule",
    r" & \multicolumn{2}{c}{Грамотных, \%} & Прирост, & Научились, \% & Прирост у поколения \\",
    r"\cmidrule(lr){2-3}",
    r"Район & 1926 г. & 1939 г. & п.п. & от неграмотных & 50-54 лет, п.п." + E,
    r"\midrule",
]
for _, q in yj.iterrows():
    L.append(
        f"{q.rayon}{'*' if q.approx else ''} & {f(q.l26)} & {f(q.l39)} & {f(q.gain)} & {f(q.taught, 0)} & {f(q.gain_ref)}"
        + E
    )
L += [r"\bottomrule", r"\end{tabular}"]
write("tab_j4", L)


# Estimate the regional determinants.
def c2(key):
    return cs(key) if key in NUM else ""


MS = [1, 2, 3, 4, 6]
L = [
    r"\begin{tabular}{lccccc}",
    r"\toprule",
    r" & \multicolumn{4}{c}{Прирост сверх поколения 50-54 лет, п.п.} & Прирост без \\",
    r"\cmidrule(lr){2-5}",
    r" & & & & Границы & вычитания, \\",
    r" & (1) & (2) & (3) & не менялись (4) & п.п. (5)" + E,
    r"\midrule",
]
for t_, lab in (
    ("l26_z", "Доля грамотных в 1926 г."),
    ("urb_z", "Доля горожан в 1926 г."),
    ("assr", "Автономная республика"),
):
    L.append(lab + " & " + " & ".join(c2(f"jl.det.m{i}.{t_}") for i in MS) + E)
L += [
    r"\midrule",
    "$R^2$ & " + " & ".join(n(f"jl.det.m{i}.r2") for i in MS) + E,
    "Число районов & " + " & ".join(n(f"jl.det.m{i}.n") for i in MS) + E,
    r"\bottomrule",
    r"\end{tabular}",
]
write("tab_j5", L)

# Compare rural and urban gains.
L = [
    r"\begin{tabular}{lcc}",
    r"\toprule",
    r" & Прирост, п.п. & Научились, \% от неграмотных" + E,
    r"\midrule",
    r"\multicolumn{3}{l}{\textit{А. Изменение прироста с возрастом, на год}}" + E,
    f"Возраст в 1926 г. & {cs('jl.age.slope')} & {cs('jl.age.tslope')}" + E,
    f"Возраст $\\times$ грамотность района (на 10 п.п.) & {cs('jl.age.int')} & {cs('jl.age.tint')}"
    + E,
    f"Число наблюдений & {n('jl.age.n')} & {n('jl.age.n')}" + E,
    r"\bottomrule",
    r"\end{tabular}",
]
write("tab_j6", L)
L = [
    r"\begin{tabular}{lrrrrrr}",
    r"\toprule",
    r" & \multicolumn{2}{c}{Грамотных, \%} & Прирост, & Смена поколений & Обучение & Доля обучения \\",
    r"\cmidrule(lr){2-3}",
    r" & 1926 г. & 1939 г. & п.п. & и школа, п.п. & взрослых, п.п. & взрослых, \%" + E,
    r"\midrule",
]
for tg, lab in (
    ("", "Все население"),
    ("u", "Городское население"),
    ("r", "Сельское население"),
):
    L.append(
        f"{lab} & {n(f'jl.dec{tg}.T.l26')} & {n(f'jl.dec{tg}.T.l39')} & {n(f'jl.dec{tg}.T.d')} & {n(f'jl.dec{tg}.T.ab')} & {n(f'jl.dec{tg}.T.c')} & {n(f'jl.dec{tg}.T.c.sh')}"
        + E
    )
L += [r"\bottomrule", r"\end{tabular}"]
write("tab_j7", L)

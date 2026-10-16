"""Table bodies -> paper/tables/*.tex, from results/paper_numbers.json."""
import os, sys, json, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = f"{ROOT}/results"; TB = f"{ROOT}/paper/tables"
os.makedirs(TB, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from names import en
J = json.load(open(f"{R}/paper_numbers.json", encoding="utf-8")); NUM = {k: tuple(v) for k, v in J["NUM"].items()}; STR = J["STR"]
def f(v, d=1):
    if v != v: return "n.i."
    s = f"{abs(v):.{d}f}"; return ("$-$" + s) if v < 0 else s
def n(key, d=None):
    if key in STR: return STR[key].replace("<", "$<$")
    if key not in NUM: return "??"
    v, dd = NUM[key]; return f(v, int(dd) if d is None else d)
def cs(key, d=None):
    if key not in NUM or key + ".se" not in NUM: return ""
    v, dd = NUM[key]; d = int(dd) if d is None else d
    if v != v: return "not identified"
    return f"{f(v, d)} ({NUM[key + '.se'][0]:.{d}f})"
def write(name, lines):
    open(f"{TB}/{name}.tex", "w", encoding="utf-8").write("\n".join(lines) + "\n"); print("table", name)
R_ = r" \\"

# ---------------- Table: layers of the dataset ----------------
write("tab_data", [r"\begin{tabular}{p{3.5cm}p{3.7cm}rrp{4.7cm}}", r"\toprule", r"Layer & Source & Units & Cells & Use" + R_, r"\midrule",
    f"1926, Table IX & Regional volumes & {n('d.units.distinct')} & {n('d.cells')} & Differences within units by sex and nationality; 1926 side of the state regime and of the legacy" + R_,
    f"1926 and 1897, Table XV & Volume 9 & 19 & {n('d.xv.cells')} & Household regime; region-level replication of the state regime" + R_,
    f"1939, literacy by age and sex & RGAE 1562/336, Demoscope & {n('d.c39.regions')} & {n('d.c39.cells')} & 1939 side of the state regime" + R_,
    r"1959, education by age and sex (RSFSR) & RGAE 1562/336, Demoscope & 1 & 225 & Check of the 1939 figures on the same cohorts" + R_,
    f"Pre-1917 baseline & Malein; Dower et al. & {n('base.units')} & - & Predictors of the gender gap; two-regime test" + R_,
    r"2010, education by nationality, sex, age and subject & Rosstat, Vol.\ 3 Table 1; Vol.\ 4 Tables 13 and 14 & 83 & 21,095 & 2010 side of the legacy" + R_, r"\bottomrule", r"\end{tabular}"])

# ---------------- Table: summary statistics ----------------
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r"Sample & Cells & Units & Outcome & Mean & SD & Survival ratio" + R_, r"\midrule",
     f"Household regime: region $\\times$ five-year cohort $\\times$ sex, rural, 1897-1926 & {n('w1.n')} & {n('w1.regions')} & change in literacy, pp & {n('ss.w1.mean')} & {n('ss.w1.sd')} & {n('ss.w1.surv')}" + R_,
     f"State regime: unit $\\times$ five-year cohort $\\times$ sex, rural, 1926-1939 & {n('w2.n')} & {n('w2.units')} & change in literacy, pp & {n('ss.w2.mean')} & {n('ss.w2.sd')} & {n('ss.w2.surv')}" + R_,
     f"Within units: unit $\\times$ nationality $\\times$ sex $\\times$ cohort, rural, 1926 & {n('dec.n')} & {n('dec.units')} & literacy, \\% & {n('dec.lit.mean')} & {n('dec.lit.sd')} &" + R_,
     f"Legacy: nationality $\\times$ subject, 2010 and 1926 & {n('leg.n')} & {n('leg.subjects')} & 2010 education gap, pp & {n('leg.g10.mean')} & {n('leg.g10.sd')} &" + R_, r"\midrule",
     r"Variable (one value per unit) & $n$ & & & Mean & SD & Range" + R_, r"\midrule"]
for k, lab, d in (("teach", "Teachers per 1,000 population, 1911", 2), ("urb", r"Urban share of men aged 20-39, 1926 (\%)", 1), ("cwr", "Child-woman ratio, 1926", 1), ("agr", r"Agrarian share, 1897 (\%)", 1), ("gap", "Rural Russian gender gap, aged 20-24, 1926 (pp)", 1)):
    L.append(f"{lab} & {n('rus.s.' + k + '.n')} & & & {n('rus.s.' + k + '.mean', d)} & {n('rus.s.' + k + '.sd', d)} & {n('rus.s.' + k + '.min', d)} to {n('rus.s.' + k + '.max', d)}" + R_)
L += [f"1926 female ethnic literacy gap, ages 20-49 (pp) & {n('leg.n')} & & & {n('leg.gF.mean')} & {n('leg.gF.sd')} &" + R_, f"1926 male ethnic literacy gap, ages 20-49 (pp) & {n('leg.n')} & & & {n('leg.gM.mean')} & {n('leg.gM.sd')} &" + R_, r"\bottomrule", r"\end{tabular}"]
write("tab_sumstat", L)

# ---------------- Table: household regime ----------------
ORD1 = ["33-37", "38-42", "43-47", "48-52", "53-57", "58-62"]
L = [r"\begin{tabular}{lcccc}", r"\toprule", r"Age at the decree of 1919 & Men, $\beta_b$ & Women, $\beta_b+\delta_b$ & Women $-$ men, $\delta_b$ & Cell means, men / women" + R_, r"\midrule"]
for b in ORD1: L.append(f"{b} & {cs('w1.m.' + b)} & {cs('w1.f.' + b)} & {cs('w1.d.' + b)} & {n('w1.cm.M.' + b)} / {n('w1.cm.F.' + b)}" + R_)
L += [f"63-67 (reference) & 0 & {cs('w1.fref')} & {cs('w1.fref')} & {n('w1.cm.M.63-67')} / {n('w1.cm.F.63-67')}" + R_, r"\midrule",
      f"Aged 33-47 against 53-67, men & \\multicolumn{{4}}{{c}}{{{cs('w1.dd.men')}}}" + R_, f"Aged 33-47 against 53-67, women & \\multicolumn{{4}}{{c}}{{{cs('w1.dd.women')}}}" + R_,
      f"Triple difference (aged 33-47 $\\times$ female) & \\multicolumn{{4}}{{c}}{{{cs('w1.ddd')}; excluding Muslim regions {cs('w1.ddd.nomus')}}}" + R_,
      f"Observations; $R^2$ & \\multicolumn{{4}}{{c}}{{{n('w1.nobs')}; {n('w1.r2')}}}" + R_, r"\bottomrule", r"\end{tabular}"]
write("tab_es1", L)

# ---------------- Table: Russians across units ----------------
L = [r"\begin{tabular}{lccccc}", r"\toprule", r"Outcome & Teachers, 1911 & Agrarian share, 1897 & Child-woman ratio & Urban share of men & $n$; $R^2$" + R_, r"\midrule", r"\multicolumn{6}{l}{\textit{A. Cohort aged 20-24 (at school in 1909-1916)}}" + R_]
for k, lab in (("gap", "Gender gap"), ("F", "Female literacy"), ("M", "Male literacy")):
    kk = f"rus.{k}.20-24"; L.append(f"{lab} & {cs(kk + '.t')} & {cs(kk + '.a')} & {cs(kk + '.c')} & & {n(kk + '.n')}; {n(kk + '.r2')}" + R_)
for k, lab in (("gap", "Gender gap"), ("F", "Female literacy"), ("M", "Male literacy")):
    kk = f"rus.{k}.20-24.u"; L.append(f"{lab} & {cs(kk + '.t')} & {cs(kk + '.a')} & {cs(kk + '.c')} & {cs(kk + '.u')} & {n(kk + '.n')}; {n(kk + '.r2')}" + R_)
L.append(r"\multicolumn{6}{l}{\textit{B. Cohort aged 12-14 (at school after 1921)}}" + R_)
for k, lab in (("gap", "Gender gap"), ("F", "Female literacy"), ("M", "Male literacy")):
    kk = f"rus.{k}.12-14"; L.append(f"{lab} & {cs(kk + '.t')} & {cs(kk + '.a')} & {cs(kk + '.c')} & & {n(kk + '.n')}; {n(kk + '.r2')}" + R_)
L.append(r"\multicolumn{6}{l}{\textit{C. Cohort aged 40-49 (at school before 1900)}}" + R_)
for k, lab in (("gap", "Gender gap"), ("F", "Female literacy"), ("M", "Male literacy")):
    kk = f"rus.{k}.40-49"; L.append(f"{lab} & {cs(kk + '.t')} & {cs(kk + '.a')} & {cs(kk + '.c')} & & {n(kk + '.n')}; {n(kk + '.r2')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_russians", L)

# ---------------- Table: decomposition ----------------
CB = ["40-49", "30-39", "25-29", "20-24", "15-19", "12-14"]
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & & \multicolumn{2}{c}{Men against Russian men} & \multicolumn{2}{c}{Additional difference for women} & Volga women against" + R_, r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}",
     r"Age in 1926 & Female & Volga & Muslim & Volga $\times$ female & Muslim $\times$ female & Russian women" + R_, r"\midrule"]
for b in CB: L.append(f"{b} & {cs('dec.f.' + b)} & {cs('dec.v.' + b)} & {cs('dec.m.' + b)} & {cs('dec.vf.' + b)} & {cs('dec.mf.' + b)} & {cs('dec.vw.' + b)}" + R_)
L += [r"\midrule", r"\multicolumn{7}{l}{\textit{Pooled triple difference, equation~\eqref{eq:ddd}}}" + R_,
      f"Cohorts aged 30-49 & & & & {cs('ddd.vf')} & {cs('ddd.mf')} &" + R_, f"Change in the cohorts aged 12-29 & & & & {cs('ddd.vfy')} & {cs('ddd.mfy')} &" + R_, f"Cohorts aged 12-29 & & & & {cs('ddd.vyoung')} & {cs('ddd.myoung')} &" + R_,
      r"\bottomrule", r"\end{tabular}"]; write("tab_decomp", L)

# ---------------- Table: differences between nationalities ----------------
L = [r"\begin{tabular}{lccccc}", r"\toprule", r" & \multicolumn{3}{c}{Female ethnic gap, aged 20-24} & Male ethnic gap, & Female ethnic gap," + R_, r"\cmidrule(lr){2-4}", r" & Baseline & Unit fixed effects & Unweighted & aged 20-24 & aged 12-14" + R_, r" & (1) & (2) & (3) & (4) & (5)" + R_, r"\midrule"]
cols = ["mech.F.u", "mech.F.ufe", "mech.F.uunw", "mech.M.u", "mech.G.u"]
for kk, lab in (("u", "Urban share of men"), ("c", "Child-woman ratio"), ("s", "Men per 100 women aged 20-39"), ("m", "Muslim nationality")):
    L.append(lab + " & " + " & ".join(cs(f"{c}.{kk}") for c in cols) + R_)
L += ["$R^2$ & " + " & ".join(n(c + ".r2") for c in cols) + R_, "Cells & " + " & ".join(n(c + ".n") for c in cols) + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_mech", L)

# ---------------- Table: state regime ----------------
AD = ["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48-52"]
L = [r"\begin{tabular}{lccccc}", r"\toprule", r"Age in 1926 & Men, $\beta_b$ & Women, $\beta_b+\delta_b$ & Women $-$ men, $\delta_b$ & Cell means, men / women & Gender gap, 1926 to 1939" + R_, r"\midrule"]
for b in AD:
    L.append(f"{b} & {cs('w2.m.' + b)} & {cs('w2.f.' + b)} & {cs('w2.d.' + b)} & {n('w2.cm.M.' + b)} / {n('w2.cm.F.' + b)} & {n('w2.gap26.' + b)} to {n('w2.gap39.' + b)}" + R_)
    if b == "43-47": L.append(r"\multicolumn{6}{l}{\textit{Above the age limit of the campaign}}" + R_)
L += [f"53-57 (reference) & 0 & {cs('w2.fref')} & {cs('w2.fref')} & {n('w2.cm.M.53-57')} / {n('w2.cm.F.53-57')} & {n('w2.gap26.53-57')} to {n('w2.gap39.53-57')}" + R_, r"\midrule",
      f"Triple difference: aged 18-32 $\\times$ female, against 48-57 & \\multicolumn{{5}}{{c}}{{{cs('w2.ddd')}; leave-one-out {n('w2.loo.min')} to {n('w2.loo.max')}; permutation $p$ {n('w2.perm')}; wild bootstrap $p$ {n('w2.wild')}}}" + R_,
      f"Aged 33-47 $\\times$ female, against 48-57 & \\multicolumn{{5}}{{c}}{{{cs('w2.ddm')}}}" + R_,
      f"Aged 18-32 $\\times$ female, against 33-47 & \\multicolumn{{5}}{{c}}{{{cs('w2.ddd33')}}}" + R_,
      f"Linear in age, cohorts aged 18-47 & \\multicolumn{{5}}{{c}}{{men {cs('w2.age.m', 2)} per year; women {cs('w2.age.f', 2)}}}" + R_,
      f"Observations; units; $R^2$ & \\multicolumn{{5}}{{c}}{{{n('w2.nobs')}; {n('w2.units')}; {n('w2.r2')}}}" + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_es2", L)

# ---------------- Table: the illiterate who became literate ----------------
L = [r"\begin{tabular}{lccccccc}", r"\toprule", r" & \multicolumn{3}{c}{Men} & \multicolumn{3}{c}{Women} & Women $-$ men," + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
     r"Cohort & Literate before & Literate after & Taught & Literate before & Literate after & Taught & taught" + R_, r"\midrule",
     r"\multicolumn{8}{l}{\textit{A. Household regime, 1897 to 1926, by age at the decree of 1919}}" + R_]
for b in ORD1 + ["63-67"]:
    L.append(f"{b} & {n('w1c.before.M.' + b)} & {n('w1c.after.M.' + b)} & {cs('w1c.M.' + b)} & {n('w1c.before.F.' + b)} & {n('w1c.after.F.' + b)} & {cs('w1c.F.' + b)} & {cs('w1c.dif.' + b)}" + R_)
L += [f"Aged 33-47 against 53-67 & & & {cs('w1c.dd.men')} & & & {cs('w1c.dd.women')} & {cs('w1c.ddd')}" + R_, r"\midrule", r"\multicolumn{8}{l}{\textit{B. State regime, 1926 to 1939, by age in 1926}}" + R_]
for b in AD + ["53-57"]:
    L.append(f"{b} & {n('w2c.before.M.' + b)} & {n('w2c.after.M.' + b)} & {cs('w2c.M.' + b)} & {n('w2c.before.F.' + b)} & {n('w2c.after.F.' + b)} & {cs('w2c.F.' + b)} & {cs('w2c.dif.' + b)}" + R_)
L += [f"Aged 18-32 against 48-57 & & & {cs('w2c.dd.men')} & & & {cs('w2c.dd.women')} & {cs('w2c.dd.dif')}" + R_,
      r"\bottomrule", r"\end{tabular}"]; write("tab_conv", L)

# ---------------- Table: two regimes ----------------
PK = [("t", "Teachers per capita, 1911"), ("c", "Child-woman ratio, 1926"), ("u", "Urban share of men, 1926"), ("a", "Agrarian share, 1897")]
pv = lambda k: "[" + STR.get(k + ".p", "").replace("<", "$<$") + "]"
L = [r"\begin{tabular}{lccccc}", r"\toprule", r"\multicolumn{6}{l}{\textit{A. Cell level: triple-difference coefficient $\psi$ of equation~\eqref{eq:regime}}}" + R_,
     r" & Household & \multicolumn{2}{c}{State regime, against cohorts aged 48-57} & \multicolumn{2}{c}{State regime, against cohorts aged 33-47}" + R_, r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}",
     r"Predictor & regime, $\psi_1$ & $\psi_2$ & $\psi_2-\psi_1$ [$p$] & $\psi_2$ & $\psi_2-\psi_1$ [$p$]" + R_, r"\midrule"]
for p, lab in PK: L.append(f"{lab} & {cs('tr.' + p + '.1')} & {cs('tr.' + p + '.2')} & {cs('tr.' + p + '.d')} {pv('tr.' + p + '.d')} & {cs('trb.' + p + '.2')} & {cs('trb.' + p + '.d')} {pv('trb.' + p + '.d')}" + R_)
u1 = sorted(int(STR[f"tr.{p}.u1"]) for p, _ in PK); u2 = sorted(int(STR[f"tr.{p}.u2"]) for p, _ in PK); u3 = sorted(int(STR[f"trb.{p}.u2"]) for p, _ in PK)
c1 = sorted(int(STR[f"tr.{p}.c1"]) for p, _ in PK); c2 = sorted(int(STR[f"tr.{p}.c2"]) for p, _ in PK); c3 = sorted(int(STR[f"trb.{p}.c2"]) for p, _ in PK)
rg = lambda a: f"{a[0]}-{a[-1]}" if a[0] != a[-1] else f"{a[0]}"
L += [f"Cells; units & {rg(c1)}; {rg(u1)} & \\multicolumn{{2}}{{c}}{{{rg(c2)}; {rg(u2)}}} & \\multicolumn{{2}}{{c}}{{{rg(c3)}; {rg(u3)}}}" + R_, r"\midrule",
      r"\multicolumn{6}{l}{\textit{B. Unit level: slope on each predictor (standardised)}}" + R_, r" & Women, household & Women, state & Men, state & &" + R_, r"\midrule"]
for p, lab in PK: L.append(f"{lab} & {cs('tru1.F.' + p)} & {cs('tru2.F.' + p)} & {cs('tru2.M.' + p)} & &" + R_)
L += [f"Own level in 1926 & & {cs('tru2.F.own')} & {cs('tru2.M.own')} & &" + R_,
      "Units & " + rg(sorted(int(STR[f'tru1.F.{p}.n']) for p, _ in PK)) + " & " + rg(sorted(int(STR[f'tru2.F.{p}.n']) for p, _ in PK)) + " & " + rg(sorted(int(STR[f'tru2.F.{p}.n']) for p, _ in PK)) + " & &" + R_, r"\bottomrule", r"\end{tabular}"]
write("tab_regimes", L)

# ---------------- Table: korenizatsiya ----------------
L = [r"\begin{tabular}{lcc}", r"\toprule", r"\multicolumn{3}{l}{\textit{A. The same nationality inside and outside its titular unit, rural, 1926}}" + R_, r" & Six nationalities & Excluding Tatars" + R_, r"\midrule",
     f"Titular unit & {cs('kor.t')} & {cs('kor.notat.t')}" + R_, f"$\\times$ cohort schooled under Soviet rule (aged 12-19) & {cs('kor.ts')} & {cs('kor.notat.ts')}" + R_, f"$\\times$ female & {cs('kor.tf')} & {cs('kor.notat.tf')}" + R_,
     f"$\\times$ cohort schooled under Soviet rule $\\times$ female & {cs('kor.tsf')} & {cs('kor.notat.tsf')}" + R_, f"Cells (inside the titular unit) & {n('kor.n')} ({n('kor.inside')}) & {n('kor.notat.n')} ({n('kor.notat.inside')})" + R_, r"\midrule",
     r"\multicolumn{3}{l}{\textit{B. Gains 1926 to 1939 of the cohort aged 23-32 in 1926, unit level}}" + R_, r" & Women & Men" + R_, r"\midrule",
     f"Own level in 1926 & {cs('w2u.F1.lit26_F', 2)} & {cs('w2u.M1.lit26_M', 2)}" + R_, f"Titular unit & {cs('w2u.F1.titular')} & {cs('w2u.M1.titular')}" + R_,
     f"Titular unit, excluding the Tatar republic & {cs('w2u.F3.titular')} &" + R_, f"Titular unit, unweighted & {cs('w2u.F4.titular')} &" + R_,
     f"Cell level: female $\\times$ aged 18-32 $\\times$ titular & {cs('w2.tit.ddd')} &" + R_, f"Units & {n('w2u.F1.n')} & {n('w2u.M1.n')}" + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_koren", L)

# ---------------- Table: cohorts of 2010 ----------------
L = [r"\begin{tabular}{lccc}", r"\toprule", r" & Female (born after 1960) & Female $\times$ born 1951-60 & Female $\times$ born before 1951" + R_, r"\midrule",
     f"Six nationalities, nationality and age fixed effects & {cs('c10.a.y')} & {cs('c10.a.m')} & {cs('c10.a.o')}" + R_, f"Six nationalities, nationality $\\times$ age fixed effects & {cs('c10.b.y')} & {cs('c10.b.m')} & {cs('c10.b.o')}" + R_,
     f"Higher education, nationality and age fixed effects & {cs('c10.h.y')} & {cs('c10.h.m')} & {cs('c10.h.o')}" + R_, r"\midrule"]
for nat in ("Tatars", "Bashkirs", "Chuvash", "Mari", "Udmurts", "Mordva"): L.append(f"{nat} & {cs('c10.' + nat + '.y')} & {cs('c10.' + nat + '.m')} & {cs('c10.' + nat + '.o')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_cohort2010", L)

# ---------------- Table: legacy, nationality by subject ----------------
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Whole population} & \multicolumn{3}{c}{Rural population}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}", r"Specification & Female gap, 1926 & Male gap, 1926 & $n$ & Female gap, 1926 & Male gap, 1926 & $n$" + R_, r"\midrule"]
for kk, lab in (("leg.nofe", "Secondary education or more, no fixed effects"), ("leg", r"\quad subject fixed effects"), ("leg.fo", r"\quad female gap only"), ("leg.mo", r"\quad male gap only"), ("leg.2029", r"\quad 1926 gaps of the cohort aged 20-29"),
                ("leg.3049", r"\quad 1926 gaps of the cohort aged 30-49"), ("leg.1219", r"\quad 1926 gaps of the cohort aged 12-19"), ("leg.h", "Higher education, subject fixed effects")):
    L.append(f"{lab} & {cs(kk + '.F', 2)} & {cs(kk + '.M', 2)} & {n(kk + '.n')} & {cs(kk + '.r.F', 2)} & {cs(kk + '.r.M', 2)} & {n(kk + '.r.n')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_legacy", L)

# ---------------- Table: legacy, sex difference ----------------
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Coefficient on female $\times$ $D^{1926}_n$ for cohorts born} & Before 1951 & Permutation & Nationalities;" + R_, r"\cmidrule(lr){2-4}",
     r"Specification & after 1960 & 1951 to 1960 & before 1951 & minus after 1960 & $p$ & cells" + R_, r"\midrule"]
for kk, lab in (("sd.six", "Six Volga and Ural nationalities"), ("sd.all", "All matched nationalities"), ("sd.nm", "Non-Muslim nationalities"), ("sd.six.unw", "Six nationalities, unweighted"),
                ("sd.six.yg", "Six nationalities, 1926 gaps of the cohorts aged 12-29"), ("sd.six.b", "Six nationalities, eight-year schooling or more"), ("sd.six.h", "Six nationalities, higher education")):
    L.append(f"{lab} & {cs(kk + '.y', 2)} & {cs(kk + '.m', 2)} & {cs(kk + '.o', 2)} & {cs(kk + '.d', 2)} & {n(kk + '.perm')} & {n(kk + '.nat')}; {n(kk + '.n')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_sexdiff", L)

# ---------------- Table: the cohorts of 1926 in the censuses of 1939 and 1959 ----------------
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Men} & \multicolumn{3}{c}{Women}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}", r"Age in 1926 & 1926 & 1939 & 1959 & 1926 & 1939 & 1959" + R_, r"\midrule"]
for lab, tag in ((r"\textit{A. Rural population}", "c3r"), (r"\textit{B. Whole population}", "c3t")):
    L.append(f"\\multicolumn{{7}}{{l}}{{{lab}}}" + R_)
    for b in ("20-24", "25-29", "30-34", "young"):
        L.append(("20-34" if b == "young" else b) + " & " + " & ".join(n(f"{tag}.{sx}.{b}.{y}") for sx in ("M", "F") for y in ("26", "39", "59")) + R_)
    L.append(f"Share of the illiterate of 1926 literate, 20-34 & & {n(tag + '.M.taught39')} & {n(tag + '.M.taught59')} & & {n(tag + '.F.taught39')} & {n(tag + '.F.taught59')}" + R_)
    if tag == "c3r": L.append(r"\midrule")
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_c59", L)

# ---------------- Table: the main estimates (the same cohorts at two censuses) ----------------
def grp(key, lab):
    return [f"{lab} & {n(key + '.l0')} & {n(key + '.l1')} & {n(key + '.d')} & {n(key + '.t')}" + R_]
L = [r"\begin{tabular}{lcccc}", r"\toprule", r" & \multicolumn{2}{c}{Literate, per cent} & Change, & Illiterate who" + R_, r"\cmidrule(lr){2-3}",
     r" & earlier census & later census & points & learned, per cent" + R_, r"\midrule", f"\\multicolumn{{5}}{{l}}{{\\textit{{A. The campaign, 1926 to 1939 ({n('w2.units')} units)}}}}" + R_]
L += grp("t1s.young.F", "Women aged 18 to 32 in 1926") + grp("t1s.old.F", "Women aged 48 to 57, above the age limit") + grp("t1s.young.M", "Men aged 18 to 32 in 1926") + grp("t1s.old.M", "Men aged 48 to 57, above the age limit")
L += [f"Women, younger minus older cohorts & & & {cs('w2.pw')} & {cs('w2.tw')}" + R_, f"Men, younger minus older cohorts & & & {cs('w2.pm')} & {cs('w2.tm')}" + R_, f"Women minus men & & & {cs('w2.pd')} & {cs('w2.td')}" + R_, r"\midrule",
      f"\\multicolumn{{5}}{{l}}{{\\textit{{B. Before the campaign, 1897 to 1926 ({n('w1.regions')} regions)}}}}" + R_]
L += grp("t1h.young.F", "Women aged 10 to 24 in 1897") + grp("t1h.old.F", "Women aged 30 to 44 in 1897") + grp("t1h.young.M", "Men aged 10 to 24 in 1897") + grp("t1h.old.M", "Men aged 30 to 44 in 1897")
L += [f"Women, younger minus older cohorts & & & {cs('w1.dd.women')} & {cs('w1c.dd.women')}" + R_, f"Men, younger minus older cohorts & & & {cs('w1.dd.men')} & {cs('w1c.dd.men')}" + R_, f"Women minus men & & & {cs('w1.ddd')} & {cs('w1c.ddd')}" + R_,
      r"\bottomrule", r"\end{tabular}"]; write("tab_main", L)

# ---------------- Table: robustness of the effect on women ----------------
L = [r"\begin{tabular}{lcccc}", r"\toprule", r" & \multicolumn{2}{c}{Women, younger minus older cohorts} & Women minus & Units;" + R_, r"\cmidrule(lr){2-3}",
     r"Sample or specification & points & illiterate who learned, per cent & men, points & cells" + R_, r"\midrule"]
for kk, lab in (("w2", "Baseline"), ("w2r.unw", "Unweighted"), ("w2r.surv", "Controlling for the change in the size of the cohort"), ("w2r.sr", "Cohorts whose size changed little"), ("w2r.rus", "Russian \\emph{gubernii} and \\emph{okrugi} only"),
                ("w2r.tit", "Autonomous republics and oblasts only"), ("w2r.mus", "Without the Tatar and Bashkir republics"), ("w2r.ural", "Without the Ural \\emph{okrugi}"), ("w2r.low", "Without the units with low-quality pages"), ("w2r.total", "Whole population of the units")):
    L.append(f"{lab} & {cs(kk + '.pw')} & {cs(kk + '.tw')} & {cs(kk + '.pd')} & {n(kk + '.nunits')}; {n(kk + '.nobs')}" + R_)
L.append(r"\midrule")
for kk, lab in (("ray", "Regions covering the whole rural RSFSR"), ("rayx", "Regions with unchanged borders")):
    L.append(f"{lab} & {cs(kk + '.pw')} & {cs(kk + '.tw')} & {cs(kk + '.pd')} & {n(kk + '.nunits')}; {n(kk + '.nobs')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_robust", L)

# ---------------- Table: every five-year group of 1926 in the census of 1939, RSFSR ----------------
L = [r"\begin{tabular}{lcccccccccccc}", r"\toprule", r" & \multicolumn{6}{c}{Rural population} & \multicolumn{6}{c}{Whole population}" + R_, r"\cmidrule(lr){2-7}\cmidrule(lr){8-13}",
     r" & \multicolumn{3}{c}{Women} & \multicolumn{3}{c}{Men} & \multicolumn{3}{c}{Women} & \multicolumn{3}{c}{Men}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}\cmidrule(lr){11-13}",
     r"Age in 1926 & 1926 & 1939 & Taught & 1926 & 1939 & Taught & 1926 & 1939 & Taught & 1926 & 1939 & Taught" + R_, r"\midrule"]
for lo in range(20, 55, 5):
    b = f"{lo}-{lo + 4}"; L.append(b + " & " + " & ".join(n(f"c4{tag}.{sx}.{b}.{k}") for tag in ("r", "t") for sx in ("F", "M") for k in ("26", "39", "t")) + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_c4", L)

# ================= Appendix tables =================
L = [r"\begin{tabular}{lccccc}", r"\toprule", r"Specification & Men 33-42 & Men 43-52 & $\times$ female 33-42 & $\times$ female 43-52 & $n$" + R_, r"\midrule"]
for kk, lab in (("base", "Baseline (rural, weighted; ten-year cohorts, reference 53-62)"), ("unw", "Unweighted"), ("surv", "With survival ratio"), ("nomus", "Excluding Muslim regions"), ("sr", "Survival ratio in $[0.4, 0.8]$"), ("total", "Total population"), ("urban", "Urban population")):
    L.append(f"{lab} & {cs('a1.' + kk + '.mA')} & {cs('a1.' + kk + '.mB')} & {cs('a1.' + kk + '.fA')} & {cs('a1.' + kk + '.fB')} & {n('a1.' + kk + '.n')}" + R_)
L.append(r"\midrule")
for kk, lab in (("w1", "Five-year bins (Table~\\ref{tab:es1}), $\\delta_b$ for 33-37 / 38-42 / 43-47"), ("w1u", "Five-year bins, unweighted"), ("w1s", "Five-year bins, with survival ratio"), ("w1t", "Five-year bins, total population")):
    L.append(f"{lab} & \\multicolumn{{5}}{{c}}{{{cs(kk + '.d.33-37')} / {cs(kk + '.d.38-42')} / {cs(kk + '.d.43-47')}}}" + R_)
L.append(f"Triple difference without the cohort aged 33-37 & \\multicolumn{{5}}{{c}}{{{cs('w1.ddd.noyoung')}; men aged 38-47 against 53-67: {cs('w1.dd.noyoung')}}}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a1", L)

L = [r"\begin{tabular}{lccccccccc}", r"\toprule", r" & \multicolumn{7}{c}{Female excess gain $\delta_b$ by age in 1926} & Triple & Cells;" + R_, r"\cmidrule(lr){2-8}", r"Specification & 18-22 & 23-27 & 28-32 & 33-37 & 38-42 & 43-47 & 48-52 & difference & units" + R_, r"\midrule"]
LAB2 = [("base", "Baseline"), ("flag", "Including flagged units"), ("surv", "With survival ratio"), ("sr", "Survival ratio in $[0.6, 1.15]$"), ("unw", "Unweighted"), ("rus", "Russian units only"), ("ural", "Excluding Ural okrugi"),
        ("mus", "Excluding Tatar and Bashkir republics"), ("low", "Excluding low-quality units"), ("t1", "Cells validated by the first rule only"), ("full", "Units with all eight cohorts"), ("total", "Total population")]
for kk, lab in LAB2:
    L.append(lab + " & " + " & ".join(cs(f"w2r.{kk}.d.{b}") for b in AD) + f" & {cs('w2r.' + kk + '.ddd')} & {n('w2r.' + kk + '.nobs')}; {n('w2r.' + kk + '.nunits')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a2", L)

L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{2}{c}{Volga $\times$ female} & \multicolumn{2}{c}{Muslim $\times$ female} & &" + R_, r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}",
     r"Specification & Aged 30-49 & Change at 12-29 & Aged 30-49 & Change at 12-29 & Cells & Units" + R_, r"\midrule"]
for kk, lab in (("ddd", "Baseline, rural"), ("ddd.nolow", "Excluding low-quality units"), ("ddd.300", "Cells of at least 300 persons"), ("ddd.unw", "Unweighted"), ("ddd.total", "Total population"), ("ddd.notit", "Excluding titular units"),
                ("ddd.with", "Units with a Volga or Ural nationality"), ("ddd.strict", "Cells validated by identities only"), ("ddd.all", "All enumerated nationalities"), ("dddl", "Log-odds of literacy as the outcome")):
    L.append(f"{lab} & {cs(kk + '.vf')} & {cs(kk + '.vfy')} & {cs(kk + '.mf')} & {cs(kk + '.mfy')} & {n(kk + '.n')} & {n(kk + '.units')}" + R_)
L += [r"\midrule", f"Leave-one-unit-out, change at 12-29 & \\multicolumn{{6}}{{l}}{{{n('ddd.loo.u.min')} to {n('ddd.loo.u.max')}}}" + R_, f"Leave-one-nationality-out & \\multicolumn{{6}}{{l}}{{{n('ddd.loo.n.min')} to {n('ddd.loo.n.max')}}}" + R_,
      f"Permutation of nationality within unit & \\multicolumn{{6}}{{l}}{{95 per cent of the null distribution between {n('ddd.perm.lo')} and {n('ddd.perm.hi')}; $p$ {n('ddd.perm')}}}" + R_,
      f"Wild cluster bootstrap & \\multicolumn{{6}}{{l}}{{$p$ {n('ddd.wild')}}}" + R_,
      f"One indicator for all non-Russian nationalities & \\multicolumn{{6}}{{l}}{{non-Russian $\\times$ female {cs('ddd.pooled.nrf')}; $\\times$ Muslim {cs('ddd.pooled.nrfm')}}}" + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_a3", L)

L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Percentage points} & \multicolumn{3}{c}{Log-odds}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
     r" & Aged 30-49 & Change at 12-29 & Aged 12-29 & Aged 30-49 & Change at 12-29 & Aged 12-29" + R_, r"\midrule"]
for sx, lab in (("M", "Volga men against Russian men"), ("F", "Volga women against Russian women")):
    L.append(f"{lab} & {cs('sx.' + sx + '.v')} & {cs('sx.' + sx + '.vy')} & {cs('sx.' + sx + '.vyoung')} & {cs('sxl.' + sx + '.v')} & {cs('sxl.' + sx + '.vy')} & {cs('sxl.' + sx + '.vyoung')}" + R_)
L += [f"Additional difference for women (Volga $\\times$ female) & {cs('ddd.vf')} & {cs('ddd.vfy')} & {cs('ddd.vyoung')} & {cs('dddl.vf')} & {cs('dddl.vfy')} & {cs('dddl.vyoung')}" + R_,
      f"Additional difference for women (Muslim $\\times$ female) & {cs('ddd.mf')} & {cs('ddd.mfy')} & {cs('ddd.myoung')} & {cs('dddl.mf')} & {cs('dddl.mfy')} & {cs('dddl.myoung')}" + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_logodds", L)

L = [r"\begin{tabular}{llccccc}", r"\toprule", r"Regime & Predictor & Baseline & Excluding low-quality units & Unweighted & All four predictors jointly & Share of the illiterate taught" + R_, r"\midrule"]
for ph, lab in (("1", "Household"), ("2", "State")):
    for p, pl in PK: L.append(f"{lab} & {pl} & {cs('tr.' + p + '.' + ph)} & {cs('trl.' + p + '.' + ph)} & {cs('tru.' + p + '.' + ph)} & {cs('trj.' + p + '.' + ph)} & {cs('trc.' + p + '.2') if ph == '2' else ''}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a4", L)

L = [r"\begin{tabular}{lcccc}", r"\toprule", r"Specification & Own level in 1926 & Titular unit & Survival ratio & Units" + R_, r"\midrule"]
for kk, lab, s in (("F0", "Women's gain, cohort aged 23-32", "F"), ("F1", r"\quad with titular indicator", "F"), ("F2", r"\quad with survival ratio", "F"), ("F3", r"\quad excluding the Tatar republic", "F"), ("F4", r"\quad unweighted", "F"), ("F5", r"\quad cohorts aged 18-32", "F"),
                   ("M0", "Men's gain, cohort aged 23-32", "M"), ("M1", r"\quad with titular indicator", "M")):
    L.append(f"{lab} & {cs('w2u.' + kk + '.lit26_' + s, 2)} & {cs('w2u.' + kk + '.titular')} & {cs('w2u.' + kk + '.surv')} & {n('w2u.' + kk + '.n')}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a5", L)

wu = pd.read_csv(f"{R}/X_unit_table_wave2.csv", sep=";", encoding="utf-8-sig").sort_values("gain_F", ascending=False)
L = [r"\begin{tabular}{lcccccc}", r"\toprule", r"Unit & Women 1926 (\%) & Women's gain & Men 1926 (\%) & Men's gain & Survival ratio & Titular" + R_, r"\midrule"]
for _, r in wu.iterrows(): L.append(f"{en(r.unit_1926)} & {r.lit26_F:.1f} & {r.gain_F:.1f} & {r.lit26_M:.1f} & {r.gain_M:.1f} & {r.surv:.2f} & {'yes' if r.titular else ''}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a6", L)

L = [r"\begin{tabular}{lcccc}", r"\toprule", r"Outcome & Mothers' cohort gain & Fathers' cohort gain & Child literacy in 1926 & $R^2$; units" + R_, r"\midrule",
     f"Girls' literacy, 1939 & {cs('ig.1.gF', 2)} & & {cs('ig.1.kid26F', 2)} & {n('ig.1.r2')}; {n('ig.1.n')}" + R_, f"Girls' literacy, 1939 & {cs('ig.2.gF', 2)} & {cs('ig.2.gM', 2)} & {cs('ig.2.kid26F', 2)} & {n('ig.2.r2')}; {n('ig.2.n')}" + R_,
     f"Boys' literacy, 1939 & {cs('ig.3.gF', 2)} & {cs('ig.3.gM', 2)} & {cs('ig.3.kid26M', 2)} & {n('ig.3.r2')}; {n('ig.3.n')}" + R_, f"Gender gap among children, 1939 & {cs('ig.4.gF', 2)} & {cs('ig.4.gM', 2)} & {cs('ig.4.gap26', 2)} & {n('ig.4.r2')}; {n('ig.4.n')}" + R_,
     r"\bottomrule", r"\end{tabular}"]; write("tab_a7", L)

L = [r"\begin{tabular}{lcccccc}", r"\toprule", r" & \multicolumn{3}{c}{Whole population} & \multicolumn{3}{c}{Rural population}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}", r"Specification & $\beta_F$ & $\beta_M$ & $n$ & $\beta_F$ & $\beta_M$ & $n$" + R_, r"\midrule"]
for kk, lab, d in (("leg", "Baseline, subject fixed effects", 2), ("leg.kal", "Excluding Kalmyks", 2), ("leg.ugk", "Excluding Ukrainians, Germans, Kazakhs", 2), ("leg.six", "Six Volga and Ural nationalities", 2), ("leg.unw", "Unweighted", 2),
                   ("leg.adj", "Age-standardised 2010 gap", 2), ("leg.rur", "Controlling for the difference in rural share", 2), ("leg.nm", "Non-Muslim nationalities only", 2), ("leg.mt", "With indicators of Muslim nationality and titular status", 2),
                   ("leg.natfe", "Nationality and subject fixed effects", 2), ("leg.illit", "Illiteracy in 2010 as outcome", 3)):
    L.append(f"{lab} & {cs(kk + '.F', d)} & {cs(kk + '.M', d)} & {n(kk + '.n')} & {cs(kk + '.r.F', d)} & {cs(kk + '.r.M', d)} & {n(kk + '.r.n')}" + R_)
L += [r"\midrule", f"Leave-one-subject-out, range of $\\beta_F$ & \\multicolumn{{3}}{{c}}{{{n('leg.loo.s.min')} to {n('leg.loo.s.max')}}} & & &" + R_, f"Leave-one-nationality-out, range of $\\beta_F$ & \\multicolumn{{3}}{{c}}{{{n('leg.loo.n.min')} to {n('leg.loo.n.max')}}} & & &" + R_,
      f"Permutation of the 1926 gaps across cells & \\multicolumn{{3}}{{c}}{{95 per cent between {n('leg.perm.lo')} and {n('leg.perm.hi')}; $p$ {n('leg.perm')}}} & & &" + R_,
      f"Wild cluster bootstrap, $p$ for $\\beta_F$ and $\\beta_M$ & \\multicolumn{{3}}{{c}}{{{n('leg.wild.F')} and {n('leg.wild.M')}}} & & &" + R_, r"\bottomrule", r"\end{tabular}"]; write("tab_a8", L)

e = pd.read_csv(f"{R}/S_legacy_sexdiff_nationalities.csv", sep=";", encoding="utf-8-sig", index_col=0).sort_values("D_ad")
L = [r"\begin{tabular}{lccccccc}", r"\toprule", r" & \multicolumn{3}{c}{Ethnic literacy gap, 1926, ages 20-49} & Units & \multicolumn{3}{c}{Female minus male education gap, 2010}" + R_, r"\cmidrule(lr){2-4}\cmidrule(lr){6-8}",
     r"Nationality & Women & Men & Difference $D^{1926}_n$ & in 1926 & Born before 1951 & 1951 to 1960 & After 1960" + R_, r"\midrule"]
for nat, r in e.iterrows(): L.append(f"{en(nat)} & {f(r.gF_ad)} & {f(r.gM_ad)} & {f(r.D_ad)} & {int(r.units_ad)} & {f(r.old)} & {f(r.mid)} & {f(r.young)}" + R_)
L += [r"\bottomrule", r"\end{tabular}"]; write("tab_a9", L)
print("tables written to", TB)

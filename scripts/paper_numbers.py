"""All numbers of the paper.
-> results/paper_numbers.json, .csv (key; value; decimals), .txt (log), samples as csv in results/
-> paper/numbers.tex (through write_numbers.py)
same specifications in stata/ABC_of_Communism.do
python scripts/paper_numbers.py [--fast]    after build_1926_v2.py, ~15 min, --fast = no permutations / bootstraps"""
import os, re, sys, json, itertools, warnings, numpy as np, pandas as pd, statsmodels.formula.api as smf
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"; R = f"{ROOT}/results"; PP = f"{ROOT}/paper"; TB = f"{PP}/tables"
os.makedirs(TB, exist_ok=True); os.makedirs(R, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maps2010 import MAP, NATMAP
FAST = "--fast" in sys.argv
SEED = 20260930
NUM, STR, LOG = {}, {}, []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)
def put(key, v, d=1):
    NUM[key] = (float(v), d)
def puts(key, s):
    STR[key] = str(s)
def fmt(v, d=1):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "n.i."
    s = f"{abs(v):.{d}f}"
    return ("$-$" + s) if v < 0 else s
def fint(v):
    return f"{int(round(v)):,}"
def pstr(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"
NI = []   # not identified (collinear with the FE)
def fit(f, d, w=None, cluster=None):
    # WLS, SE clustered (HC1 if no cluster) as in Stata: G/(G-1) * (N-1)/(N-K) with K = rank of X, t with G-1 df
    toks = set(re.split(r"[\s()*+:~,']+", f.replace("Q(", "").replace("Treatment", "")))
    d = d.dropna(subset=[c for c in d.columns if c in toks] + ([w] if w else []))
    m = smf.wls(f, data=d, weights=d[w]) if w else smf.ols(f, data=d)
    _, s_, vt_ = np.linalg.svd(m.wexog, full_matrices=False); tol = s_.max() * max(m.wexog.shape) * np.finfo(float).eps; rank = int((s_ > tol).sum())
    if cluster:
        g = pd.factorize(d[cluster])[0]; G = int(g.max()) + 1; N = len(d)
        r = m.fit(cov_type="cluster", cov_kwds={"groups": g, "use_correction": False}, use_t=True)
        r._results.cov_params_default = r._results.cov_params_default * (G / (G - 1)) * ((N - 1) / (N - rank))   # must be set on _results
    else:
        r = m.fit(cov_type="HC1", use_t=True)
    r._null = vt_[s_ <= tol].T; r._names = list(m.exog_names); r._nclu = d[cluster].nunique() if cluster else None
    return r
def identified(r, terms):
    if not hasattr(r, "_null") or r._null.shape[1] == 0: return True
    v = np.zeros(len(r._names))
    for t_ in terms: v[r._names.index(t_)] = 1
    return bool(np.abs(r._null.T @ v).max() < 1e-7)
def putna(key, d):
    put(key, np.nan, d); put(key + ".se", np.nan, d); puts(key + ".p", "n.i."); NI.append(key)
def putc(key, r, term, d=1):
    if not identified(r, [term]): return putna(key, d)
    put(key, r.params[term], d); put(key + ".se", r.bse[term], d); puts(key + ".p", pstr(r.pvalues[term]))
def putl(key, r, expr, d=1):
    if not identified(r, [t_.strip() for t_ in expr.split("=")[0].split(" + ")]): return putna(key, d)
    t = r.t_test(expr); put(key, float(t.effect[0]), d); put(key + ".se", float(t.sd[0][0]), d); puts(key + ".p", pstr(float(t.pvalue)))
def cs(key, d=None):
    v, dd = NUM[key]; s, _ = NUM[key + ".se"]; d = dd if d is None else d
    return f"{fmt(v, d)} ({s:.{d}f})"
def z(df, cols):
    df = df.copy()
    for c in cols: df[c + "_z"] = (df[c] - df[c].mean()) / df[c].std()
    return df
def table(name, lines):
    open(f"{TB}/{name}.tex", "w", encoding="utf-8").write("\n".join(lines) + "\n")

# ---------------- fast WLS with absorbed FE, for the permutation and bootstrap loops ----------------
class FWL:
    def __init__(self, d, fe_cols, w=None, cluster=None):
        n = len(d); self.sw = np.sqrt(d[w].values.astype(float)) if w else np.ones(n)
        blocks = [np.ones((n, 1))]
        for c in fe_cols:
            codes = pd.factorize(d[c])[0]; M = np.zeros((n, codes.max() + 1)); M[np.arange(n), codes] = 1; blocks.append(M[:, 1:])
        F_ = np.hstack(blocks) * self.sw[:, None]
        Q, Rm = np.linalg.qr(F_); keep = np.abs(np.diag(Rm)) > 1e-9 * np.abs(np.diag(Rm)).max(); self.Q = Q[:, keep]; self.kfe = int(keep.sum())
        self.g = pd.factorize(d[cluster])[0] if cluster else None; self.n = n
    def res(self, v):
        v = np.asarray(v, float) * (self.sw if np.ndim(v) == 1 else self.sw[:, None])
        return v - self.Q @ (self.Q.T @ v)
    def ols(self, yr, Xr, want_t=False):
        b, *_ = np.linalg.lstsq(Xr, yr, rcond=None)
        if not want_t: return b
        u = yr - Xr @ b; XtXi = np.linalg.pinv(Xr.T @ Xr); G = self.g.max() + 1; meat = np.zeros((Xr.shape[1], Xr.shape[1]))
        for k in range(G):
            s = Xr[self.g == k].T @ u[self.g == k]; meat += np.outer(s, s)
        K = Xr.shape[1] + self.kfe
        V = XtXi @ meat @ XtXi * (G / (G - 1)) * ((self.n - 1) / (self.n - K))
        return b, b / np.sqrt(np.diag(V))
def wild_p(d, fe_cols, xcols, term, y, w, cluster, B=999, seed=SEED):
    # restricted wild cluster bootstrap, Rademacher weights -> (t, p)
    rng = np.random.default_rng(seed); d = d.reset_index(drop=True)
    F_ = FWL(d, fe_cols, w, cluster); Xr = F_.res(d[xcols].values); yr = F_.res(d[y].values); j = xcols.index(term)
    b, t = F_.ols(yr, Xr, True); t0 = t[j]
    X0 = np.delete(Xr, j, axis=1); b0 = F_.ols(yr, X0); fitted = X0 @ b0; u0 = yr - fitted
    G = F_.g.max() + 1; ts = []
    for _ in range(B):
        e = rng.choice([-1.0, 1.0], size=G)[F_.g]; ystar = fitted + u0 * e
        _, tb = F_.ols(ystar, Xr, True); ts.append(tb[j])
    return float(t0), float(np.mean(np.abs(ts) >= abs(t0)))

q = pd.read_csv(f"{D}/tableIX_region_quality.csv", sep=";", encoding="utf-8-sig")
LOWQ = set(q[(q.area == "rural") & (q.share_confirmed < 0.85)].region_1926)
BAD39 = {"Немцев Поволжья АССР", "Нижегородская губ.", "Ленинградская губ.", "Новгородская губ."}
URAL = {"Челябинский округ", "Свердловский округ", "Пермский округ", "Тюменский округ", "Тобольский округ", "Ишимский округ", "Курганский округ"}
MUSLIM_UNITS = {"Башкирская АССР", "Татарская АССР"}
MUS = ["Татары", "Башкиры", "Мишари"]; VOL = ["Чуваши", "Марийцы", "Мордва", "Вотяки"]; KAZ = ["Казаки"]
EN = {"Татары": "Tatars", "Башкиры": "Bashkirs", "Мишари": "Mishars", "Чуваши": "Chuvash", "Марийцы": "Mari", "Мордва": "Mordva", "Вотяки": "Votyaks", "Удмурты": "Udmurts", "Русские": "Russians",
      "Калмыки": "Kalmyks", "Карелы": "Karelians", "Коми-пермяки": "Komi-Permyaks", "Немцы": "Germans", "Украинцы": "Ukrainians", "Евреи": "Jews", "Казахи": "Kazakhs"}

# =====================================================================================================================
# 0. Data and validation
# =====================================================================================================================
P("=== 0. Data and validation ===")
ix = pd.read_csv(f"{D}/census1926_tableIX_long.csv", sep=";", encoding="utf-8-sig", dtype={"age": str}, usecols=["region", "area", "age", "group", "group_type", "sex", "total", "literate", "quality"])
puts("d.cells", fint(len(ix))); puts("d.units", str(ix.region.nunique()))
g5 = pd.read_csv(f"{D}/tableIX_five_year_groups_validated.csv", sep=";", encoding="utf-8-sig")
a = g5[(g5.lo >= 10) & (g5.lo <= 65)]
puts("d.g5", fint(len(a)))
for t_, k in ((1, "t1"), (2, "t2"), (3, "t3"), (0, "t0")): put(f"d.g5.{k}", 100 * (a.tier == t_).mean(), 1)
ar = a[a.area == "rural"]; puts("d.g5r", fint(len(ar)))
for t_, k in ((1, "t1"), (2, "t2"), (3, "t3"), (0, "t0")): put(f"d.g5r.{k}", 100 * (ar.tier == t_).mean(), 1)
puts("d.g5.nbr", str(int((g5.src_pop == "X").sum())))
sv = pd.read_csv(f"{D}/tableIX_single_years_validated.csv", sep=";", encoding="utf-8-sig"); s_ = sv[(sv.a >= 8) & (sv.a <= 57)]
puts("d.single", fint(len(s_))); put("d.single.valid", 100 * s_.valid.mean(), 1)
bv = pd.read_csv(f"{D}/tableIX_bands_validated.csv", sep=";", encoding="utf-8-sig")
puts("d.bands", fint(len(bv))); puts("d.bands.rural", fint((bv.area == "rural").sum()))
bv = bv[bv.region != "Уральская обл."].copy()   # = sum of its 16 okrugi
ball = bv[(bv.group_type == "all") & (bv.area == "rural")]; puts("d.units.rural", str(ball.region.nunique())); puts("d.units.distinct", str(ix[ix.region != "Уральская обл."].region.nunique()))
xv = pd.read_csv(f"{D}/tableXV_1926_1897_age_sex_literacy.csv", sep=";", encoding="utf-8-sig", dtype={"age": str})
puts("d.xv.cells", fint(len(xv)))
B97 = ["10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44"]; B26 = [f"{int(b[:2]) + 30}-{int(b[:2]) + 34}" for b in B97]
x_ = xv[xv.region_gosplan_1927 != "РСФСР"]
pv = x_.pivot_table(index=["region_gosplan_1927", "census_year", "sex", "age"], columns="area", values=["population", "literate"], aggfunc="first"); pv.columns = [f"{a_}_{b_}" for a_, b_ in pv.columns]; pv = pv.reset_index()
pv = pv[((pv.census_year == 1897) & pv.age.isin(B97)) | ((pv.census_year == 1926) & pv.age.isin(B26))]
okx = [(abs(t - (u + r_)) <= max(2, 0.005 * t)) if not (pd.isna(t) or pd.isna(u) or pd.isna(r_)) else False for t, u, r_ in zip(pv.population_total, pv.population_urban, pv.population_rural)]
okl = [(abs(t - (u + r_)) <= max(2, 0.005 * t)) if not (pd.isna(t) or pd.isna(u) or pd.isna(r_)) else False for t, u, r_ in zip(pv.literate_total, pv.literate_urban, pv.literate_rural)]
puts("d.xv.used", str(len(pv))); puts("d.xv.ok", str(int(np.sum(np.array(okx) & np.array(okl)))))
# RSFSR rural literacy at ages 20-49
A2049 = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]
rs = xv[(xv.region_gosplan_1927 == "РСФСР") & (xv.area == "rural") & xv.age.isin(A2049)]
for yr in (1897, 1926):
    for sx in ("M", "F"):
        s = rs[(rs.census_year == yr) & (rs.sex == sx)]; put(f"rsfsr.{yr}.{sx}", 100 * s.literate.sum() / s.population.sum(), 0)
c39 = pd.read_csv(f"{D}/census1939_literacy_by_region_age_sex.csv", sep=";", encoding="utf-8-sig", dtype={"age": str})
puts("d.c39.cells", fint(len(c39))); puts("d.c39.regions", str(c39.region_1939.nunique()))
top = c39[~c39.region_1939.str.startswith("в том числе") & ~c39.region_1939.str.startswith("город")]
for sx in ("M", "F"):
    s = top[(top.area == "rural") & (top.sex == sx) & top.age.isin(A2049)]; put(f"rsfsr.1939.{sx}", 100 * s.literate.sum() / s.population.sum(), 0)
# age profile, rural, validated cells of the whole population
PB = ["8-11", "12-14", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69"]
pr = ball[ball.band.isin(PB)].groupby(["band", "sex"])[["population", "literate"]].sum(); pr["lit"] = 100 * pr.literate / pr.population; pr = pr.lit.unstack().reindex(PB)
for b in PB:
    put(f"prof.M.{b}", pr.loc[b, "M"], 0); put(f"prof.F.{b}", pr.loc[b, "F"], 0); put(f"prof.gap.{b}", pr.loc[b, "M"] - pr.loc[b, "F"], 0)
P(pr.round(1).to_string())

# =====================================================================================================================
# 1. Household regime: linked cohorts 1897 -> 1926 (Vol. 9, Table XV)
# =====================================================================================================================
P("\n=== 1. Household regime, 1897-1926 ===")
x2 = xv[(xv.region_gosplan_1927 != "РСФСР") & (xv.quality != "missing")]
rows = []
for (reg, area, sex), g in x2.groupby(["region_gosplan_1927", "area", "sex"]):
    g97 = g[g.census_year == 1897].set_index("age"); g26 = g[g.census_year == 1926].set_index("age")
    for b in B97:
        lo = int(b[:2]); b26 = f"{lo + 30}-{lo + 34}"
        if b in g97.index and b26 in g26.index:
            p97, l97, p26, l26 = g97.loc[b, "population"], g97.loc[b, "literate"], g26.loc[b26, "population"], g26.loc[b26, "literate"]
            if min(p97, p26) < 500 or pd.isna(l97) or pd.isna(l26): continue
            rows.append(dict(region=reg, area=area, sex=sex, age_decree=f"{lo + 23}-{lo + 27}", pop97=p97, pop26=p26, lit97=100 * l97 / p97, lit26=100 * l26 / p26, gain=100 * l26 / p26 - 100 * l97 / p97, survival=p26 / p97))
e1 = pd.DataFrame(rows); e1 = e1[e1.gain.between(-30, 45)].copy(); e1["female"] = (e1.sex == "F").astype(int); e1.to_csv(f"{R}/E1_wave1_event_cells.csv", sep=";", index=False, encoding="utf-8-sig")
ORD1 = ["33-37", "38-42", "43-47", "48-52", "53-57", "58-62", "63-67"]; e1["bin"] = pd.Categorical(e1.age_decree, ORD1)
e1["treated"] = e1.age_decree.isin(ORD1[:3]).astype(int); e1["tf"] = e1.treated * e1.female
MUSREG = ["Башкирская АССР", "Дагестанская АССР", "Казакская АССР", "Киргизская АССР", "Крымская АССР"]
d1 = e1[e1.area == "rural"]; puts("w1.n", str(len(d1))); puts("w1.regions", str(d1.region.nunique()))
put("ss.w1.mean", d1.gain.mean(), 1); put("ss.w1.sd", d1.gain.std(), 1); put("ss.w1.surv", d1.survival.mean(), 2)
FE1 = "gain ~ C(bin, Treatment('63-67')) * female + C(region)"
def es1(d, key, w="pop97", extra=""):
    r = fit(FE1 + extra, d, w=w, cluster="region")
    for b in ORD1[:-1]:
        k = f"C(bin, Treatment('63-67'))[T.{b}]"; putc(f"{key}.m.{b}", r, k); putc(f"{key}.d.{b}", r, k + ":female"); putl(f"{key}.f.{b}", r, f"{k} + {k}:female = 0")
    putc(f"{key}.fref", r, "female"); put(f"{key}.r2", r.rsquared, 2); puts(f"{key}.nobs", str(int(r.nobs)))
    return r
r = es1(d1, "w1")
cm = d1.groupby(["age_decree", "sex"]).gain.mean().unstack()
for b in ORD1: put(f"w1.cm.M.{b}", cm.loc[b, "M"]); put(f"w1.cm.F.{b}", cm.loc[b, "F"])
put("w1.slope", (NUM["w1.m.33-37"][0] - NUM["w1.m.58-62"][0]) / 25, 1)
d2 = d1[d1.age_decree != "48-52"]
rp = fit("gain ~ treated * female + C(region)", d2, w="pop97", cluster="region"); putc("w1.ddd", rp, "treated:female"); putc("w1.dd.men", rp, "treated"); puts("w1.ddd.n", str(int(rp.nobs)))
putl("w1.dd.women", rp, "treated + treated:female = 0")
put("w1.ratio", (NUM["w1.dd.women"][0]) / NUM["w1.dd.men"][0], 2)
rp2 = fit("gain ~ treated * female + C(region)", d2[~d2.region.isin(MUSREG)], w="pop97", cluster="region"); putc("w1.ddd.nomus", rp2, "treated:female")
d3 = d2[d2.age_decree != "33-37"]; rp3 = fit("gain ~ treated * female + C(region)", d3, w="pop97", cluster="region"); putc("w1.ddd.noyoung", rp3, "treated:female"); putc("w1.dd.noyoung", rp3, "treated")
es1(d1, "w1u", w=None); r_s = es1(d1, "w1s", extra=" + survival"); putc("w1s.surv", r_s, "survival"); es1(e1[e1.area == "total"], "w1t"); es1(e1[e1.area == "urban"], "w1ur")
if not FAST:
    dd = d2.copy(); t0, pw = wild_p(dd, ["region"], ["treated", "female", "tf"], "tf", "gain", "pop97", "region"); puts("w1.wild", pstr(pw)); P("wave 1 wild bootstrap", t0, pw)
# share of the illiterate taught (does not depend on the room left below 100)
def taught(d, key, coh, order, before, gain, pop, cluster):
    d = d.copy(); d["conv"] = 100 * d[gain] / (100 - d[before]); d["ill"] = d[pop] * (100 - d[before]) / 100; d["cc"] = d[coh].astype(str)
    r = fit("conv ~ 0 + C(cc) + C(cc):female", d, w="ill", cluster=cluster)
    for b in order:
        putc(f"{key}.M.{b}", r, f"C(cc)[{b}]"); putc(f"{key}.dif.{b}", r, f"C(cc)[{b}]:female"); putl(f"{key}.F.{b}", r, f"C(cc)[{b}] + C(cc)[{b}]:female = 0")
        for sx in ("M", "F"):
            s = d[(d.cc == b) & (d.sex == sx)]; put(f"{key}.before.{sx}.{b}", np.average(s[before], weights=s[pop]), 0); put(f"{key}.after.{sx}.{b}", np.average(s[before] + s[gain], weights=s[pop]), 0)
    return d
d1c = taught(d1, "w1c", "age_decree", ORD1, "lit97", "gain", "pop97", "region"); d2c = d1c[d1c.age_decree != "48-52"]
for sx in ("M", "F"):
    for t_, lab in ((1, "treated"), (0, "placebo")):
        s = d2c[(d2c.sex == sx) & (d2c.treated == t_)]; put(f"w1c.{lab}.{sx}", np.average(s.conv, weights=s.ill), 0)
s = d2c[d2c.treated == 1]; put("w1c.share.ill.F", 100 * s[s.sex == "F"].ill.sum() / s.ill.sum(), 0)
rc = fit("conv ~ treated * female + C(region)", d2c, w="ill", cluster="region"); putc("w1c.ddd", rc, "treated:female"); putc("w1c.dd.men", rc, "treated"); putl("w1c.dd.women", rc, "treated + treated:female = 0")
# Table 1, means of the two groups of cohorts
for sx in ("M", "F"):
    for lab, s in (("young", d2c[(d2c.sex == sx) & (d2c.treated == 1)]), ("old", d2c[(d2c.sex == sx) & (d2c.treated == 0)])):
        put(f"t1h.{lab}.{sx}.l0", np.average(s.lit97, weights=s.pop97), 0); put(f"t1h.{lab}.{sx}.l1", np.average(s.lit97 + s.gain, weights=s.pop97), 0); put(f"t1h.{lab}.{sx}.d", np.average(s.gain, weights=s.pop97), 1); put(f"t1h.{lab}.{sx}.t", np.average(s.conv, weights=s.ill), 0)
# ten-year cohorts (A1)
lx = pd.read_csv(f"{D}/tableXV_linked_cohorts.csv", sep=";", encoding="utf-8-sig"); lx = lx[lx.region != "РСФСР"].copy()
lx["c"] = lx.cohort.map({"born 1878-87 (school-age in 1897)": "A", "born 1868-77 (adults in 1897)": "B", "born 1858-67": "C"}); lx["female"] = (lx.sex == "F").astype(int)
lx["muslim"] = lx.region.isin(MUSREG).astype(int); lt = lx[lx.gain_pp.between(-30, 40)]
F10 = "gain_pp ~ C(c, Treatment('C')) * female + C(region)"
def ten(d, key, w="pop_1897", extra=""):
    r = fit(F10 + extra, d, w=w, cluster="region")
    putc(f"{key}.mA", r, "C(c, Treatment('C'))[T.A]"); putc(f"{key}.mB", r, "C(c, Treatment('C'))[T.B]"); putc(f"{key}.fA", r, "C(c, Treatment('C'))[T.A]:female"); putc(f"{key}.fB", r, "C(c, Treatment('C'))[T.B]:female"); puts(f"{key}.n", str(int(r.nobs)))
ru = lt[lt.area == "rural"]
ten(ru, "a1.base"); ten(ru, "a1.unw", w=None); ten(ru, "a1.surv", extra=" + survival_ratio"); ten(ru[ru.muslim == 0], "a1.nomus"); ten(ru[ru.survival_ratio.between(0.4, 0.8)], "a1.sr"); ten(lt[lt.area == "total"], "a1.total"); ten(lt[lt.area == "urban"], "a1.urban")
# mortality bound (RSFSR rural, cohort born 1878-87)
lr = pd.read_csv(f"{D}/tableXV_linked_cohorts.csv", sep=";", encoding="utf-8-sig"); lr = lr[(lr.region == "РСФСР") & (lr.area == "rural")]
m_ = lr[(lr.sex == "M") & lr.cohort.str.startswith("born 1878")].iloc[0]; f_ = lr[(lr.sex == "F") & lr.cohort.str.startswith("born 1878")].iloc[0]; pl = lr[(lr.sex == "M") & (lr.cohort == "born 1858-67")].iloc[0]
exc = 1 - m_.survival_ratio / f_.survival_ratio
put("w1.surv.M", m_.survival_ratio, 2); put("w1.surv.F", f_.survival_ratio, 2); put("w1.excess", 100 * exc, 1); put("w1.bound", m_.lit_1897 / (1 - exc) - m_.lit_1897, 1); put("w1.gainM", m_.gain_pp, 1); put("w1.gainF", f_.gain_pp, 1)
put("w1.surv.placebo", pl.survival_ratio, 2); put("w1.gain.placebo", pl.gain_pp, 1); put("w1.bound.share", (m_.lit_1897 / (1 - exc) - m_.lit_1897) / m_.gain_pp, 2)
# Whipple index, rural, whole population, ages 23-62 (validated single years)
wq = sv[(sv.group == "Всё население") & (sv.area == "rural") & sv.valid & sv.a.between(23, 62)].groupby(["sex", "a"])[["total", "literate"]].sum()
for sx in ("M", "F"):
    t = wq.loc[sx]; ill = t.total - t.literate
    for lab, v in (("all", t.total), ("lit", t.literate), ("ill", ill)): put(f"whipple.{sx}.{lab}", 500 * v[v.index % 5 == 0].sum() / v.sum(), 0)

# =====================================================================================================================
# 2. The 1926 cross-section: Russians across units, decomposition, differences between nationalities
# =====================================================================================================================
P("\n=== 2. The 1926 cross-section ===")
rb = pd.read_csv(f"{D}/russians_region_baseline.csv", sep=";", encoding="utf-8-sig")
# baseline is provincial, units carved from one province share it -> cluster by pg
rb["pg"] = rb.pre1917_province.fillna(rb.region)
_pu = sorted({x_.strip() for pp_ in rb.pre1917_province.dropna() for x_ in str(pp_).split(";")}); _pv = pd.read_csv(f"{D}/baseline_pre1917_by_province.csv", sep=";", encoding="utf-8-sig")
_pin = _pv[_pv.province_rus.isin(_pu) & _pv.teachers_percap_1911.notna()]; puts("base.provinces", str(len(_pin))); puts("base.districts", str(int(_pin.n_districts.sum()))); puts("base.units", str(int(rb.teachers_percap_1911.notna().sum())))
# 9 units have no rural pages and the file has their whole population: masked here, used only in rb_all (robustness)
RURAL_RUS = set(bv[(bv.area == "rural") & (bv.group_type == "russian")].region); rb_all = rb.copy()
rb.loc[~rb.region.isin(RURAL_RUS), [c_ for c_ in rb.columns if c_.startswith(("gender_gap_", "lit_F_", "lit_M_"))] + ["cwr", "sr_20_39", "csr_0_4"]] = np.nan
puts("rus.units.rural", str(int(rb.region.isin(RURAL_RUS).sum()))); puts("rus.units.norural", str(int((~rb.region.isin(RURAL_RUS)).sum())))
XF = ["teachers_percap_1911", "exp_zemstvo_edu_pc_1894", "agshare_1897", "cwr", "per_lit_f", "urban_share_M", "sr_20_39"]
rbz = rb.copy()
for c in [c_ for c_ in rbz.columns if c_.startswith(("gender_gap_", "lit_F_", "lit_M_"))]:
    lo_, hi_ = ((-5, 80) if c.startswith("gender_gap_") else (0, 100)); rbz.loc[~rbz[c].between(lo_, hi_), c] = np.nan
rbz = z(rbz, XF)
for c, k, dd_ in (("gender_gap_20-24", "gap", 1), ("lit_F_20-24", "litF", 1), ("lit_M_20-24", "litM", 1), ("teachers_percap_1911", "teach", 2), ("agshare_1897", "agr", 1), ("cwr", "cwr", 1), ("urban_share_M", "urb", 1)):
    v = rbz[c].dropna(); puts(f"rus.s.{k}.n", str(len(v))); put(f"rus.s.{k}.mean", v.mean(), dd_); put(f"rus.s.{k}.sd", v.std(), dd_); put(f"rus.s.{k}.min", v.min(), dd_); put(f"rus.s.{k}.max", v.max(), dd_)
rbz.to_csv(f"{R}/F_russians_units.csv", sep=";", index=False, encoding="utf-8-sig"); kr_out = None
gmin = rbz.loc[rbz["gender_gap_20-24"].idxmin()]; gmax = rbz.loc[rbz["gender_gap_20-24"].idxmax()]; P("smallest and largest Russian gender gap:", gmin.region, gmin["gender_gap_20-24"], gmax.region, gmax["gender_gap_20-24"])
BASE = "teachers_percap_1911_z + agshare_1897_z + cwr_z"; TK = {"teachers_percap_1911_z": "t", "agshare_1897_z": "a", "cwr_z": "c", "urban_share_M_z": "u"}
def rus(y, spec, key, d=None):
    d = rbz if d is None else d
    r = fit(f"Q('{y}') ~ {spec}", d, cluster="pg")
    for t_, k in TK.items():
        if t_ in r.params.index: putc(f"{key}.{k}", r, t_)
    puts(f"{key}.n", str(int(r.nobs))); put(f"{key}.r2", r.rsquared, 2); puts(f"{key}.pg", str(r._nclu)); return r
for coh in ("20-24", "12-14", "40-49"):
    for yv, k in (("gender_gap", "gap"), ("lit_F", "F"), ("lit_M", "M")):
        rus(f"{yv}_{coh}", BASE, f"rus.{k}.{coh}")
        if coh == "20-24": rus(f"{yv}_{coh}", BASE + " + urban_share_M_z", f"rus.{k}.{coh}.u")
y = "gender_gap_20-24"; dd = rbz.dropna(subset=[y, "teachers_percap_1911_z", "agshare_1897_z", "cwr_z"]); r0 = fit(f"Q('{y}') ~ {BASE}", dd, cluster="pg"); puts("rus.pg", str(dd.pg.nunique()))
lo = pd.DataFrame([fit(f"Q('{y}') ~ {BASE}", dd[dd.region != u_]).params for u_ in dd.region])
put("rus.loo.t.min", lo.teachers_percap_1911_z.min()); put("rus.loo.t.max", lo.teachers_percap_1911_z.max()); put("rus.loo.c.min", lo.cwr_z.min()); put("rus.loo.c.max", lo.cwr_z.max())
for lab, d3, k in (("low", dd[~dd.region.isin(LOWQ)], "nolow"), ("tit", dd[~dd.region.str.contains("АССР|АО")], "notit"), ("ural", dd[~dd.region.str.contains("округ")], "noural"), ("zem", dd[dd.zemstvo_prov == 1], "zem")):
    rus(y, BASE, f"rus.rob.{k}", d3)
rbz_all = rb_all.copy()
for c in [c_ for c_ in rbz_all.columns if c_.startswith(("gender_gap_", "lit_F_", "lit_M_"))]:
    lo_, hi_ = ((-5, 80) if c.startswith("gender_gap_") else (0, 100)); rbz_all.loc[~rbz_all[c].between(lo_, hi_), c] = np.nan
rbz_all = z(rbz_all, XF); rus(y, BASE, "rus.rob.all", rbz_all)
for alt, k in (("exp_zemstvo_edu_pc_1894_z", "spend"), ("per_lit_f_z", "lit97")):
    r = fit(f"Q('{y}') ~ {alt} + agshare_1897_z + cwr_z", rbz.dropna(subset=[y, alt, "agshare_1897_z", "cwr_z"]), cluster="pg"); putc(f"rus.alt.{k}", r, alt); puts(f"rus.alt.{k}.n", str(int(r.nobs)))
rb1 = fit(f"Q('{y}') ~ urban_share_M_z", rbz.dropna(subset=[y, "urban_share_M_z"]), cluster="pg"); putc("rus.urb.biv", rb1, "urban_share_M_z"); puts("rus.urb.biv.n", str(int(rb1.nobs)))
du = rbz.dropna(subset=[y, "teachers_percap_1911_z", "agshare_1897_z", "cwr_z", "urban_share_M_z"])
lo_u = [fit(f"Q('{y}') ~ {BASE} + urban_share_M_z", du[du.region != u_]).params["urban_share_M_z"] for u_ in du.region]; put("rus.urb.loo.min", min(lo_u)); put("rus.urb.loo.max", max(lo_u))
if not FAST:
    rng = np.random.default_rng(SEED)
    def perm_ols(d, f, term, draws=2000, w=None, by=None):
        # permute the regressor across units, or across groups `by` if it is constant within them
        obs = (smf.wls(f, data=d, weights=d[w]) if w else smf.ols(f, data=d)).fit().params[term]; a_ = []
        gv_ = d.groupby(by)[term].first() if by else None
        for _ in range(draws):
            d2_ = d.copy(); d2_[term] = d2_[by].map(dict(zip(gv_.index, rng.permutation(gv_.values)))) if by else rng.permutation(d2_[term].values)
            a_.append((smf.wls(f, data=d2_, weights=d2_[w]) if w else smf.ols(f, data=d2_)).fit().params[term])
        a_ = np.array(a_); return float(np.mean(np.abs(a_) >= abs(obs))), float(np.quantile(a_, .025)), float(np.quantile(a_, .975))
    p_, l_, h_ = perm_ols(dd, f"Q('{y}') ~ {BASE}", "teachers_percap_1911_z", by="pg"); puts("rus.perm.t", pstr(p_)); put("rus.perm.t.lo", l_); put("rus.perm.t.hi", h_)
    p_, l_, h_ = perm_ols(dd, f"Q('{y}') ~ {BASE}", "cwr_z"); puts("rus.perm.c", pstr(p_))
    p_, l_, h_ = perm_ols(du, f"Q('{y}') ~ {BASE} + urban_share_M_z", "urban_share_M_z"); puts("rus.perm.u", pstr(p_))

# ---- decomposition ----
kp = pd.read_csv(f"{D}/korenizatsiya_panel.csv", sep=";", encoding="utf-8-sig")
CB = ["40-49", "30-39", "25-29", "20-24", "15-19", "12-14"]
k = kp[kp.band.isin(CB) & (kp.group != "Прочие") & kp.literacy.between(0, 100)].copy()
k["female"] = (k.sex == "F").astype(int); k["nonrus"] = (k.group != "Русские").astype(int); k["muslim"] = k.group.isin(MUS + KAZ).astype(int); k["volga"] = k.group.isin(VOL).astype(int)
k["other"] = ((k.nonrus == 1) & (k.muslim == 0) & (k.volga == 0)).astype(int); k["young"] = k.band.isin(CB[2:]).astype(int); k["band_c"] = pd.Categorical(k.band, CB)
k["rc"] = k.region + "|" + k.band; k["gc"] = k.group + "|" + k.band; k["sc"] = k.sex + "|" + k.band
for c in ("volga", "muslim", "other"):
    k[c[0] + "f"] = k[c] * k.female; k[c[0] + "fy"] = k[c] * k.female * k.young
kall = k[k.area == "rural"].copy(); CORE = ["Русские"] + MUS + VOL
kr = kall[kall.group.isin(CORE)].copy(); ktot = k[(k.area == "total") & k.group.isin(CORE)].copy()
units_with = sorted(set(kr[kr.nonrus == 1].region))
kr.to_csv(f"{R}/D_core_cells.csv", sep=";", index=False, encoding="utf-8-sig"); kall.to_csv(f"{R}/D_all_cells.csv", sep=";", index=False, encoding="utf-8-sig"); ktot.to_csv(f"{R}/D_core_cells_total.csv", sep=";", index=False, encoding="utf-8-sig")
puts("dec.n", str(len(kr))); puts("dec.units", str(kr.region.nunique())); puts("dec.units.nat", str(len(units_with))); puts("dec.n.all", str(len(kall))); puts("dec.n.strict", str(int(kr.tier.isin([1, 2]).sum())))
put("dec.lit.mean", kr.literacy.mean(), 1); put("dec.lit.sd", kr.literacy.std(), 1)
gs = kr.groupby("group").apply(lambda t: pd.Series({"cells": len(t), "units": t.region.nunique(), "pop": t.population.sum() / 1000, "M": np.average(t[t.sex == "M"].literacy, weights=t[t.sex == "M"].population), "F": np.average(t[t.sex == "F"].literacy, weights=t[t.sex == "F"].population)}))
P(gs.round(1).to_string()); put("dec.pop", kr.population.sum() / 1e6, 1)
for g_, r_ in gs.iterrows():
    kk = "desc." + EN.get(g_, g_); puts(kk + ".units", str(int(r_.units))); puts(kk + ".cells", str(int(r_.cells))); puts(kk + ".pop", fint(r_["pop"])); put(kk + ".M", r_.M, 1); put(kk + ".F", r_.F, 1)
FD = "literacy ~ C(rc) + female:C(band_c) + volga:C(band_c) + muslim:C(band_c) + volga:female:C(band_c) + muslim:female:C(band_c)"
def dec(d, key, w="population", f=FD, nd=1):
    r = fit(f, d, w=w, cluster="region")
    for b in CB:
        putc(f"{key}.f.{b}", r, f"female:C(band_c)[{b}]", nd); putc(f"{key}.v.{b}", r, f"volga:C(band_c)[{b}]", nd); putc(f"{key}.m.{b}", r, f"muslim:C(band_c)[{b}]", nd)
        putc(f"{key}.vf.{b}", r, f"volga:female:C(band_c)[{b}]", nd); putc(f"{key}.mf.{b}", r, f"muslim:female:C(band_c)[{b}]", nd)
        putl(f"{key}.vw.{b}", r, f"volga:C(band_c)[{b}] + volga:female:C(band_c)[{b}] = 0", nd); putl(f"{key}.mw.{b}", r, f"muslim:C(band_c)[{b}] + muslim:female:C(band_c)[{b}] = 0", nd)
    puts(f"{key}.n", str(int(r.nobs))); put(f"{key}.r2", r.rsquared, 2)
dec(kr, "dec")
FP = "literacy ~ C(rc) + C(gc) + C(sc) + vf + vfy + mf + mfy"
def pool(d, key, w="population", f=FP, nd=1):
    r = fit(f, d, w=w, cluster="region")
    for t_ in ("vf", "vfy", "mf", "mfy"): putc(f"{key}.{t_}", r, t_, nd)
    putl(f"{key}.vyoung", r, "vf + vfy = 0", nd); putl(f"{key}.myoung", r, "mf + mfy = 0", nd); puts(f"{key}.n", str(int(r.nobs))); puts(f"{key}.units", str(d.region.nunique())); return r
pool(kr, "ddd"); pool(kr[~kr.region.isin(LOWQ)], "ddd.nolow"); pool(kr[kr.population >= 300], "ddd.300"); pool(kr, "ddd.unw", w=None); pool(ktot, "ddd.total")
# same in log-odds (the sexes are at different points of the diffusion curve)
kr["lo"] = np.log(kr.literacy.clip(0.5, 99.5) / (100 - kr.literacy.clip(0.5, 99.5)))
dec(kr, "decl", f=FD.replace("literacy ~", "lo ~"), nd=2); pool(kr, "dddl", f=FP.replace("literacy ~", "lo ~"), nd=2)
# men and women separately, old vs young cohorts
for sx in ("M", "F"):
    for yv, kk, nd in (("literacy", "sx", 1), ("lo", "sxl", 2)):
        r_ = fit(f"{yv} ~ C(rc) + volga + volga:young + muslim + muslim:young", kr[kr.sex == sx], w="population", cluster="region")
        putc(f"{kk}.{sx}.v", r_, "volga", nd); putc(f"{kk}.{sx}.vy", r_, "volga:young", nd); putl(f"{kk}.{sx}.vyoung", r_, "volga + volga:young = 0", nd); putc(f"{kk}.{sx}.m", r_, "muslim", nd); putc(f"{kk}.{sx}.my", r_, "muslim:young", nd)
pool(kr[~kr.region.str.contains("АССР|АО")], "ddd.notit"); pool(kr[kr.region.isin(units_with)], "ddd.with"); pool(kr[kr.tier.isin([1, 2])], "ddd.strict")
ra = pool(kall, "ddd.all", f=FP + " + of + ofy"); putc("ddd.all.of", ra, "of"); putc("ddd.all.ofy", ra, "ofy")
kall["nr_f"] = kall.nonrus * kall.female; kall["nr_f_m"] = kall.nr_f * kall.muslim
rn = fit("literacy ~ C(rc) + C(gc) + C(sc) + nr_f + nr_f_m", kall, w="population", cluster="region"); putc("ddd.pooled.nrf", rn, "nr_f"); putc("ddd.pooled.nrfm", rn, "nr_f_m")
lu = [fit(FP, kr[kr.region != u_], w="population", cluster="region").params for u_ in units_with]
put("ddd.loo.u.min", min(p_["vfy"] for p_ in lu)); put("ddd.loo.u.max", max(p_["vfy"] for p_ in lu))
ln = [fit(FP, kr[kr.group != g_], w="population", cluster="region").params for g_ in VOL + MUS]
put("ddd.loo.n.min", min(p_["vfy"] for p_ in ln)); put("ddd.loo.n.max", max(p_["vfy"] for p_ in ln))
if not FAST:
    rng = np.random.default_rng(SEED)
    cells = kr[kr.muslim == 0].reset_index(drop=True); F_ = FWL(cells, ["rc", "gc", "sc"], "population"); yr = F_.res(cells.literacy.values)
    def coef_vfy(v):
        X = np.column_stack([v * cells.female.values, v * cells.female.values * cells.young.values]); return F_.ols(yr, F_.res(X))[1]
    obs = coef_vfy(cells.volga.values.astype(float)); rg = cells[["region", "group", "volga"]].drop_duplicates().reset_index(drop=True); a_ = []
    for _ in range(2000):
        lab = rg.groupby("region").volga.transform(lambda s: rng.permutation(s.values)); mp_ = dict(zip(zip(rg.region, rg.group), lab))
        a_.append(coef_vfy(np.array([mp_[(x_, y_)] for x_, y_ in zip(cells.region, cells.group)], float)))
    a_ = np.array(a_); puts("ddd.perm", pstr(float(np.mean(np.abs(a_) >= abs(obs))))); put("ddd.perm.lo", np.quantile(a_, .025)); put("ddd.perm.hi", np.quantile(a_, .975)); P("decomposition permutation: observed", obs)
    t0, pw = wild_p(kr, ["rc", "gc", "sc"], ["vf", "vfy", "mf", "mfy"], "vfy", "literacy", "population", "region"); puts("ddd.wild", pstr(pw)); P("decomposition wild bootstrap", t0, pw)
# literacy by group of nationalities, sex and cohort (weighted means of the cells)
kr["type"] = np.where(kr.volga == 1, "vol", np.where(kr.muslim == 1, "mus", "rus"))
lt_ = kr.groupby(["type", "sex", "band"]).apply(lambda t: np.average(t.literacy, weights=t.population))
for (t_, sx_, b_), v_ in lt_.items(): put(f"lit26.{t_}.{sx_}.{b_}", v_, 0)
# raw gaps
wg = kr.pivot_table(index=["region", "band", "group"], columns="sex", values=["literacy", "population"]).reset_index(); wg.columns = ["region", "band", "group", "lit_F", "lit_M", "pop_F", "pop_M"]
rus_ = wg[wg.group == "Русские"].set_index(["region", "band"]); wg = wg[wg.group != "Русские"].copy()
wg["gapF"] = [rus_.lit_F.get((a_, b_), np.nan) - c_ for a_, b_, c_ in zip(wg.region, wg.band, wg.lit_F)]; wg["gapM"] = [rus_.lit_M.get((a_, b_), np.nan) - c_ for a_, b_, c_ in zip(wg.region, wg.band, wg.lit_M)]
wg = wg.dropna(subset=["gapF", "gapM"]); wg["pop"] = wg.pop_F + wg.pop_M; wg["type"] = np.where(wg.group.isin(MUS), "mus", "vol")
gt_ = wg.groupby(["type", "band"]).apply(lambda t: pd.Series({"M": np.average(t.gapM, weights=t["pop"]), "F": np.average(t.gapF, weights=t["pop"])}))
for (t_, b), r_ in gt_.iterrows(): put(f"raw.{t_}.M.{b}", r_.M, 0); put(f"raw.{t_}.F.{b}", r_.F, 0)
# the oldest women of the Tatar republic
tt = kp[(kp.region == "Татарская АССР") & (kp.area == "total") & (kp.band == "60-69") & (kp.sex == "F")].set_index("group").literacy
if "Татары" in tt.index and "Русские" in tt.index: put("tat.old.F", tt["Татары"], 1); put("rus.old.F", tt["Русские"], 1)

# ---- differences between nationalities within units ----
mp = pd.read_csv(f"{D}/mechanism_panel_clean.csv", sep=";", encoding="utf-8-sig")
m = mp[mp.area == "rural"].copy(); rusm = m[m.group == "Русские"].set_index("region"); m = m[~m.group.isin(["Русские", "Прочие"])].copy()
for c in ["cwr", "sr_20_39", "urban_share_M", "urban_share_F", "csr_0_4"]: m[c + "_diff"] = m[c] - m.region.map(rusm[c])
m["mob_gap_diff"] = (m.urban_share_M - m.urban_share_F) - m.region.map(rusm.urban_share_M - rusm.urban_share_F); m["muslim"] = m.group.isin(MUS + KAZ).astype(int)
for c_ in ("ethgap_F_20-24", "ethgap_M_20-24", "ethgap_F_12-14"): m.loc[~m[c_].between(-60, 80), c_] = np.nan
m = m.dropna(subset=["ethgap_F_20-24", "ethgap_M_20-24", "cwr_diff", "sr_20_39_diff", "mob_gap_diff"])
mz = z(m, ["cwr_diff", "sr_20_39_diff", "mob_gap_diff", "urban_share_M_diff"])
mz.to_csv(f"{R}/G_mechanism_cells.csv", sep=";", index=False, encoding="utf-8-sig")
puts("mech.n", str(len(mz))); puts("mech.units", str(mz.region.nunique())); puts("mech.nat", str(mz.group.nunique())); put("mech.urb.sd", m.urban_share_M_diff.std(), 1); put("mech.mob.sd", m.mob_gap_diff.std(), 1)
G1 = "cwr_diff_z + sr_20_39_diff_z + mob_gap_diff_z + muslim"; G2 = "cwr_diff_z + sr_20_39_diff_z + urban_share_M_diff_z + muslim"
MK = {"cwr_diff_z": "c", "sr_20_39_diff_z": "s", "mob_gap_diff_z": "g", "urban_share_M_diff_z": "u", "muslim": "m"}
def mech(yv, f, key, d=None, w="pop"):
    d = mz.dropna(subset=[yv]) if d is None else d
    r = fit(f"Q('{yv}') ~ {f}", d, w=w, cluster="region")
    for t_, kk in MK.items():
        if t_ in r.params.index: putc(f"{key}.{kk}", r, t_)
    puts(f"{key}.n", str(int(r.nobs))); put(f"{key}.r2", r.rsquared, 2); return r
for yv, kk in (("ethgap_F_20-24", "F"), ("ethgap_M_20-24", "M"), ("ethgap_F_12-14", "G")):
    mech(yv, G1, f"mech.{kk}.g"); mech(yv, G2, f"mech.{kk}.u"); mech(yv, G2 + " + C(region)", f"mech.{kk}.ufe"); mech(yv, G2, f"mech.{kk}.uunw", w=None)
yv = "ethgap_F_20-24"
lu_ = [fit(f"Q('{yv}') ~ {G2}", mz[mz.region != u_], w="pop", cluster="region").params["urban_share_M_diff_z"] for u_ in mz.region.unique()]
ln_ = [fit(f"Q('{yv}') ~ {G2}", mz[mz.group != g_], w="pop", cluster="region").params["urban_share_M_diff_z"] for g_ in mz.group.unique()]
put("mech.loo.u.min", min(lu_)); put("mech.loo.u.max", max(lu_)); put("mech.loo.n.min", min(ln_)); put("mech.loo.n.max", max(ln_))
if not FAST:
    rng = np.random.default_rng(SEED); p_, l_, h_ = perm_ols(mz, f"Q('{yv}') ~ {G2}", "urban_share_M_diff_z", w="pop"); puts("mech.perm.u", pstr(p_))
csr = mp[(mp.area == "rural") & mp.csr_0_4.notna() & (mp.group != "Прочие")].groupby("group").apply(lambda t: np.average(t.csr_0_4, weights=t["pop"]))
csr_main = csr.reindex(["Русские"] + MUS + VOL).dropna(); put("csr.min", csr_main.min(), 0); put("csr.max", csr_main.max(), 0); P("child sex ratios:\n" + csr.round(1).to_string())
cwn = mp[(mp.area == "rural") & mp.cwr.notna() & (mp.group != "Прочие")].groupby("group").apply(lambda t: np.average(t.cwr, weights=t["pop"])).reindex(["Русские"] + MUS + VOL).dropna(); put("cwr.nat.min", cwn.min(), 0); put("cwr.nat.max", cwn.max(), 0)

# =====================================================================================================================
# 3. State regime: linked cohorts 1926 -> 1939
# =====================================================================================================================
P("\n=== 3. State regime, 1926-1939 ===")
ADULT = ["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48-52", "53-57"]; YOUNG = ADULT[:3]; MIDDLE = ADULT[3:6]; PLACEBO = ADULT[6:]; REF = "53-57"
lc = pd.read_csv(f"{D}/linked_cohorts_1926_1939.csv", sep=";", encoding="utf-8-sig")
lc["female"] = (lc.sex == "F").astype(int); lc["titular"] = lc.unit_1926.str.contains("АССР|АО").astype(int)
def balanced(d): return d[d.groupby(["unit_1926", "area", "age_1926"]).sex.transform("nunique") == 2].copy()
def prep(d):
    d = d.copy(); d["coh"] = pd.Categorical(d.age_1926, ADULT); d["young"] = d.age_1926.isin(YOUNG).astype(int); d["middle"] = d.age_1926.isin(MIDDLE).astype(int); d["fy"] = d.female * d.young; d["fm"] = d.female * d.middle
    d["age1928"] = d.age_1926.map({c: int(c[:2]) + 3.5 for c in ADULT}); return d
base = prep(balanced(lc[~lc.unit_1926.isin(BAD39) & lc.gain_pp.between(-40, 90) & lc.age_1926.isin(ADULT)]))
cl = base[base.area == "rural"].copy(); cl.to_csv(f"{R}/W2_cells.csv", sep=";", index=False, encoding="utf-8-sig"); base[base.area == "total"].to_csv(f"{R}/W2_cells_total.csv", sep=";", index=False, encoding="utf-8-sig"); d_flag = None; puts("w2.n", str(len(cl))); puts("w2.units", str(cl.unit_1926.nunique())); P("cells per cohort:\n" + cl.groupby("age_1926").size().to_string())
for c in ADULT: puts(f"w2.units.{c}", str(cl[cl.age_1926 == c].unit_1926.nunique()))
put("ss.w2.mean", cl.gain_pp.mean(), 1); put("ss.w2.sd", cl.gain_pp.std(), 1); put("ss.w2.surv", cl.survival.median(), 2)
FE2 = f"gain_pp ~ C(coh, Treatment('{REF}')) * female + C(unit_1926)"; FP2 = "gain_pp ~ C(coh) + female + fm + fy + C(unit_1926)"
def es2(d, key, w="pop_1926", extra=""):
    r = fit(FE2 + extra, d, w=w, cluster="unit_1926")
    for b in ADULT[:-1]:
        kk = f"C(coh, Treatment('{REF}'))[T.{b}]"; putc(f"{key}.m.{b}", r, kk); putc(f"{key}.d.{b}", r, kk + ":female"); putl(f"{key}.f.{b}", r, f"{kk} + {kk}:female = 0")
    putc(f"{key}.fref", r, "female"); put(f"{key}.r2", r.rsquared, 2); puts(f"{key}.nobs", str(int(r.nobs))); puts(f"{key}.nunits", str(d.unit_1926.nunique()))
    rp_ = fit(FP2 + extra, d, w=w, cluster="unit_1926"); putc(f"{key}.ddd", rp_, "fy"); putc(f"{key}.ddm", rp_, "fm")
    d33 = d[d.age_1926.isin(YOUNG + MIDDLE)]; rq = fit("gain_pp ~ C(coh) + female + fy + C(unit_1926)" + extra, d33, w=w, cluster="unit_1926"); putc(f"{key}.ddd33", rq, "fy")
    # effect by sex, 18-32 vs cohorts above the age limit: points .pw .pm .pd, share taught .tw .tm .td
    dq = d.copy(); dq["conv"] = 100 * dq.gain_pp / (100 - dq.lit_1926); dq["ill"] = dq.pop_1926 * (100 - dq.lit_1926) / 100; FQ = " ~ young * female + middle * female + C(unit_1926)" + extra
    for yv, wv, tg in (("gain_pp", w, "p"), ("conv", "ill" if w else None, "t")):
        rq = fit(yv + FQ, dq, w=wv, cluster="unit_1926"); putc(f"{key}.{tg}m", rq, "young"); putl(f"{key}.{tg}w", rq, "young + young:female = 0"); putc(f"{key}.{tg}d", rq, "young:female")
    return r
es2(cl, "w2")
cm = cl.groupby(["age_1926", "sex"]).apply(lambda t: np.average(t.gain_pp, weights=t.pop_1926)).unstack()
gg = cl.pivot_table(index=["unit_1926", "age_1926"], columns="sex", values=["lit_1926", "lit_1939", "pop_1926"]).reset_index(); gg.columns = ["unit", "age", "l26F", "l26M", "l39F", "l39M", "pF", "pM"]; gg["w"] = gg.pF + gg.pM
for c in ADULT:
    put(f"w2.cm.M.{c}", cm.loc[c, "M"]); put(f"w2.cm.F.{c}", cm.loc[c, "F"]); t = gg[gg.age == c]
    put(f"w2.gap26.{c}", np.average(t.l26M - t.l26F, weights=t.w), 0); put(f"w2.gap39.{c}", np.average(t.l39M - t.l39F, weights=t.w), 0)
    put(f"w2.l26.M.{c}", np.average(t.l26M, weights=t.pM), 0); put(f"w2.l26.F.{c}", np.average(t.l26F, weights=t.pF), 0); put(f"w2.l39.M.{c}", np.average(t.l39M, weights=t.pM), 0); put(f"w2.l39.F.{c}", np.average(t.l39F, weights=t.pF), 0)
yy = cl[cl.young == 1].groupby("sex").apply(lambda t: pd.Series({"gain": np.average(t.gain_pp, weights=t.pop_1926), "l26": np.average(t.lit_1926, weights=t.pop_1926), "l39": np.average(t.lit_1939, weights=t.pop_1926), "surv": t.pop_1939.sum() / t.pop_1926.sum()}))
for sx in ("M", "F"):
    put(f"w2.young.gain.{sx}", yy.loc[sx, "gain"], 0); put(f"w2.young.l26.{sx}", yy.loc[sx, "l26"], 0); put(f"w2.young.l39.{sx}", yy.loc[sx, "l39"], 0); put(f"w2.young.surv.{sx}", yy.loc[sx, "surv"], 2)
put("w2.young.gain1.F", yy.loc["F", "gain"], 1)
exf = 1 - yy.loc["F", "surv"] / yy.loc["M", "surv"]; put("w2.excess", 100 * exf, 1); put("w2.bound", (yy.loc["F", "l26"] / (1 - exf) - yy.loc["F", "l26"]) if exf > 0 else 0.0, 1)
# bound: all women lost between the censuses were illiterate
put("w2.bound.all.F", min(100.0, yy.loc["F", "l26"] / min(yy.loc["F", "surv"], 1.0)) - yy.loc["F", "l26"], 1); put("w2.young.loss.F", 100 * (1 - min(yy.loc["F", "surv"], 1.0)), 0)
ra_ = fit("gain_pp ~ age1928 * female + C(unit_1926)", cl[cl.age_1926.isin(YOUNG + MIDDLE)], w="pop_1926", cluster="unit_1926"); putc("w2.age.m", ra_, "age1928", 2); putc("w2.age.fx", ra_, "age1928:female", 2); putl("w2.age.f", ra_, "age1928 + age1928:female = 0", 2)
lo2 = [fit(FP2, cl[cl.unit_1926 != u_], w="pop_1926", cluster="unit_1926").params["fy"] for u_ in sorted(cl.unit_1926.unique())]; put("w2.loo.min", min(lo2)); put("w2.loo.max", max(lo2))
pd.DataFrame({"dropped_unit": sorted(cl.unit_1926.unique()), "coef_female_x_young": lo2}).to_csv(f"{R}/B4_leave_one_out.csv", sep=";", index=False)
if not FAST:
    rng = np.random.default_rng(SEED); c2 = cl.reset_index(drop=True); F_ = FWL(c2, ["coh", "unit_1926"], "pop_1926"); yr = F_.res(c2.gain_pp.values)
    def coef_fy(fem):
        X = np.column_stack([fem, fem * c2.middle.values, fem * c2.young.values]); return F_.ols(yr, F_.res(X))[2]
    obs = coef_fy(c2.female.values.astype(float)); key_ = c2[["unit_1926", "age_1926"]].drop_duplicates().reset_index(drop=True); a_ = []
    for _ in range(2000):
        fl = dict(zip(zip(key_.unit_1926, key_.age_1926), rng.random(len(key_)) < 0.5)); a_.append(coef_fy(np.array([(1 - f_) if fl[(u_, c_)] else f_ for u_, c_, f_ in zip(c2.unit_1926, c2.age_1926, c2.female)], float)))
    a_ = np.array(a_); puts("w2.perm", pstr(float(np.mean(np.abs(a_) >= abs(obs))))); put("w2.perm.lo", np.quantile(a_, .025)); put("w2.perm.hi", np.quantile(a_, .975)); np.savetxt(f"{R}/B5_permutation_female_x_young.txt", a_)
    t0, pw = wild_p(cl, ["coh", "unit_1926"], ["female", "fm", "fy"], "fy", "gain_pp", "pop_1926", "unit_1926"); puts("w2.wild", pstr(pw)); P("wave 2 wild bootstrap", t0, pw)
# share taught 1926-39
clc = taught(cl, "w2c", "age_1926", ADULT, "lit_1926", "gain_pp", "pop_1926", "unit_1926")
for sx in ("M", "F"):
    for lab, s in (("young", clc[(clc.sex == sx) & (clc.young == 1)]), ("middle", clc[(clc.sex == sx) & (clc.middle == 1)]), ("placebo", clc[(clc.sex == sx) & clc.age_1926.isin(PLACEBO)])): put(f"w2c.{lab}.{sx}", np.average(s.conv, weights=s.ill), 0)
s = clc[clc.young == 1]; put("w2c.share.ill.F", 100 * s[s.sex == "F"].ill.sum() / s.ill.sum(), 0); nw = s.pop_1926 * s.gain_pp / 100; put("w2c.share.new.F", 100 * nw[s.sex == "F"].sum() / nw.sum(), 0)
rc = fit("conv ~ C(coh) + female + fm + fy + C(unit_1926)", clc, w="ill", cluster="unit_1926"); putc("w2c.ddd", rc, "fy"); putc("w2c.ddm", rc, "fm"); putc("w2c.fref", rc, "female")
rc = fit("conv ~ young * female + middle * female + C(unit_1926)", clc, w="ill", cluster="unit_1926"); putc("w2c.dd.men", rc, "young"); putl("w2c.dd.women", rc, "young + young:female = 0"); putc("w2c.dd.dif", rc, "young:female")
rc = fit("conv ~ age1928 * female + C(unit_1926)", clc[clc.age_1926.isin(YOUNG + MIDDLE)], w="ill", cluster="unit_1926"); putc("w2c.age.m", rc, "age1928", 2); putc("w2c.age.fx", rc, "age1928:female", 2); putl("w2c.age.f", rc, "age1928 + age1928:female = 0", 2)
put("w2c.ratio", NUM["w2c.young.F"][0] / NUM["w2c.young.M"][0], 2); put("w1c.ratio", max(NUM["w1c.treated.F"][0], 0) / NUM["w1c.treated.M"][0], 2)
for sx in ("M", "F"):
    for lab, s in (("young", clc[(clc.sex == sx) & (clc.young == 1)]), ("old", clc[(clc.sex == sx) & clc.age_1926.isin(PLACEBO)])):
        put(f"t1s.{lab}.{sx}.l0", np.average(s.lit_1926, weights=s.pop_1926), 0); put(f"t1s.{lab}.{sx}.l1", np.average(s.lit_1939, weights=s.pop_1926), 0); put(f"t1s.{lab}.{sx}.d", np.average(s.gain_pp, weights=s.pop_1926), 1); put(f"t1s.{lab}.{sx}.t", np.average(s.conv, weights=s.ill), 0)
# eq. (mix): women's share = reach of the state, men's = reach + household part
e_ = NUM["w2c.young.F"][0] / 100; h_ = NUM["w1c.treated.M"][0] / 100; put("mix.e", e_, 2); put("mix.h", h_, 2); put("mix.pred", e_ + (1 - e_) * h_, 2); put("mix.obs", NUM["w2c.young.M"][0] / 100, 2)
# same, household part from men of the same ages in 1897 (15-29, i.e. 38-52 at the decree)
sa = d1c[(d1c.sex == "M") & d1c.age_decree.isin(["38-42", "43-47", "48-52"])]; ha = np.average(sa.conv, weights=sa.ill) / 100
put("mix.h.adult", ha, 2); put("mix.pred.adult", e_ + (1 - e_) * ha, 2); put("mix.gap.obs", NUM["w2c.young.M"][0] - NUM["w2c.young.F"][0], 0); put("mix.gap.pred", 100 * (1 - e_) * ha, 0)
# household part by age implied by (mix): (P_m - P_f) / (1 - P_f)
for b in ADULT: put(f"mixh.{b}", 100 * (NUM[f"w2c.M.{b}"][0] - NUM[f"w2c.F.{b}"][0]) / (100 - NUM[f"w2c.F.{b}"][0]), 0)
for kk, d_ in (("unw", clc), ("total", taught(base[base.area == "total"], "w2ct", "age_1926", ADULT, "lit_1926", "gain_pp", "pop_1926", "unit_1926")), ("rus", clc[clc.titular == 0]), ("sr", clc[clc.survival.between(0.6, 1.15)])):
    r_ = fit("conv ~ C(coh) + female + fm + fy + C(unit_1926)", d_, w=None if kk == "unw" else "ill", cluster="unit_1926"); putc(f"w2c.{kk}.ddd", r_, "fy")
    for sx in ("M", "F"):
        s = d_[(d_.sex == sx) & (d_.young == 1)]; put(f"w2c.{kk}.young.{sx}", np.average(s.conv, weights=None if kk == "unw" else s.ill), 0)
# robustness (A2)
d_all = prep(balanced(lc[(lc.area == "rural") & lc.age_1926.isin(ADULT) & lc.gain_pp.between(-40, 90)]))
ROB2 = [("base", "Baseline", cl, "pop_1926", ""), ("flag", "Including flagged units", d_all, "pop_1926", ""), ("surv", "With survival ratio", cl, "pop_1926", " + survival"),
        ("sr", "Survival ratio in $[0.6, 1.15]$", balanced(cl[cl.survival.between(0.6, 1.15)]), "pop_1926", ""), ("unw", "Unweighted", cl, None, ""), ("rus", "Russian units only", cl[cl.titular == 0], "pop_1926", ""), ("tit", "Autonomous units only", cl[cl.titular == 1], "pop_1926", ""),
        ("ural", "Excluding Ural okrugi", cl[~cl.unit_1926.isin(URAL)], "pop_1926", ""), ("mus", "Excluding Tatar and Bashkir republics", cl[~cl.unit_1926.isin(MUSLIM_UNITS)], "pop_1926", ""),
        ("low", "Excluding low-quality units", cl[~cl.unit_1926.isin(LOWQ)], "pop_1926", ""), ("t1", "Cells validated by the first rule only", balanced(cl[cl.tier == 1]), "pop_1926", ""),
        ("full", "Units with all eight cohorts", cl[cl.groupby("unit_1926").age_1926.transform("nunique") == 8], "pop_1926", ""), ("total", "Total population", base[base.area == "total"], "pop_1926", "")]
for kk, lab, d_, w_, ex in ROB2:
    r_ = es2(d_, f"w2r.{kk}", w=w_, extra=ex)
    if kk == "surv": putc("w2r.surv.coef", r_, "survival")
# unit level (cohort aged 23-32)
def unit_level(sub, cohorts):
    w_ = sub[(sub.sex == "F") & sub.age_1926.isin(cohorts)].groupby("unit_1926").agg(gain_F=("gain_pp", "mean"), lit26_F=("lit_1926", "mean"), pop=("pop_1926", "sum"), titular=("titular", "max"), surv=("survival", "mean"), ncoh=("gain_pp", "size")).reset_index()
    m_ = sub[(sub.sex == "M") & sub.age_1926.isin(cohorts)].groupby("unit_1926").agg(gain_M=("gain_pp", "mean"), lit26_M=("lit_1926", "mean")).reset_index()
    o = w_.merge(m_, on="unit_1926"); return o[o.ncoh == len(cohorts)].copy()
wu = unit_level(cl, ["23-27", "28-32"]); wu3 = unit_level(cl, YOUNG); puts("w2u.n", str(len(wu)))
put("w2u.rus.min", wu[wu.titular == 0].gain_F.min(), 0); put("w2u.rus.max", wu[wu.titular == 0].gain_F.max(), 0); put("w2u.tit.min", wu[wu.titular == 1].gain_F.min(), 0); put("w2u.tit.max", wu[wu.titular == 1].gain_F.max(), 0)
def ul(f, d, key, w="pop"):
    r = fit(f, d, w=w)
    for t_ in r.params.index[1:]: putc(f"{key}.{t_}", r, t_, 2 if t_.startswith("lit26") else 1)
    puts(f"{key}.n", str(int(r.nobs))); return r
ul("gain_F ~ lit26_F", wu, "w2u.F0"); ul("gain_F ~ lit26_F + titular", wu, "w2u.F1"); ul("gain_F ~ lit26_F + titular + surv", wu, "w2u.F2"); ul("gain_F ~ lit26_F + titular", wu[~wu.unit_1926.isin(MUSLIM_UNITS)], "w2u.F3")
ul("gain_F ~ lit26_F + titular", wu, "w2u.F4", w=None); ul("gain_F ~ lit26_F + titular", wu3, "w2u.F5"); ul("gain_M ~ lit26_M", wu, "w2u.M0"); ul("gain_M ~ lit26_M + titular", wu, "w2u.M1")
cl["fyt"] = cl.fy * cl.titular; cl["ft"] = cl.female * cl.titular; cl["yt"] = cl.young * cl.titular; cl["fmt"] = cl.fm * cl.titular; cl["mt"] = cl.middle * cl.titular
rt = fit("gain_pp ~ C(unit_1926) + C(coh) + female + fm + fy + yt + mt + ft + fmt + fyt", cl, w="pop_1926", cluster="unit_1926"); putc("w2.tit.ddd", rt, "fyt")
wu.assign(unit_en=wu.unit_1926).to_csv(f"{R}/X_unit_table_wave2.csv", sep=";", index=False)
# rayons (Table XV x 1939 oblasts)
ry = pd.read_csv(f"{D}/linked_cohorts_rayon_1926_1939.csv", sep=";", encoding="utf-8-sig"); AD2 = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54"]
ry = ry[ry.age_1926.isin(AD2) & ry.gain_pp.between(-40, 90)].copy(); ry["female"] = (ry.sex == "F").astype(int); ry["young"] = ry.age_1926.isin(AD2[:3]).astype(int); ry["middle"] = ry.age_1926.isin(AD2[3:6]).astype(int)
ry["fy"] = ry.female * ry.young; ry["fm"] = ry.female * ry.middle; ry["coh"] = ry.age_1926
ry = ry[ry.groupby(["rayon", "area", "age_1926"]).sex.transform("nunique") == 2]
ry["age1928"] = ry.age_1926.map({c: int(c[:2]) + 3.5 for c in AD2}); rr_ = ry[ry.area == "rural"]; rr_.to_csv(f"{R}/B9_rayon_cells.csv", sep=";", index=False, encoding="utf-8-sig"); puts("ray.n", str(len(rr_))); puts("ray.units", str(rr_.rayon.nunique()))
r = fit("gain_pp ~ C(coh) + female + fm + fy + C(rayon)", rr_, w="pop_1926", cluster="rayon"); putc("ray.ddd", r, "fy"); putc("ray.ddm", r, "fm"); putc("ray.fref", r, "female")
r = fit("gain_pp ~ C(coh) + female + fm + fy + C(rayon)", rr_[rr_.approx_borders == 0], w="pop_1926", cluster="rayon"); putc("ray.ddd.exact", r, "fy"); puts("ray.units.exact", str(rr_[rr_.approx_borders == 0].rayon.nunique()))
r = fit("gain_pp ~ age1928 * female + C(rayon)", rr_[rr_.age_1926 != "50-54"], w="pop_1926", cluster="rayon"); putc("ray.age.m", r, "age1928", 2); putc("ray.age.fx", r, "age1928:female", 2)
rm = rr_.groupby(["age_1926", "sex"]).apply(lambda t: np.average(t.gain_pp, weights=t.pop_1926)).unstack()
for c in AD2: put(f"ray.cm.M.{c}", rm.loc[c, "M"]); put(f"ray.cm.F.{c}", rm.loc[c, "F"])
gr = rr_.pivot_table(index=["rayon", "age_1926"], columns="sex", values=["lit_1926", "lit_1939"]).reset_index(); gr.columns = ["rayon", "age", "l26F", "l26M", "l39F", "l39M"]
for c in ("20-24", "25-29"):
    t = gr[gr.age == c]; put(f"ray.gap26.{c}", (t.l26M - t.l26F).mean(), 0); put(f"ray.gap39.{c}", (t.l39M - t.l39F).mean(), 0)
# share taught, rural RSFSR, cohorts 20-34 in 1926
rc_ = rr_.copy(); rc_["conv"] = 100 * rc_.gain_pp / (100 - rc_.lit_1926); rc_["ill"] = rc_.pop_1926 * (100 - rc_.lit_1926) / 100; s = rc_[rc_.young == 1]
for sx in ("M", "F"):
    s_ = s[s.sex == sx]; put(f"ray.c.young.{sx}", np.average(s_.conv, weights=s_.ill), 0); put(f"ray.young.gain.{sx}", np.average(s_.gain_pp, weights=s_.pop_1926), 0)
put("ray.c.share.ill.F", 100 * s[s.sex == "F"].ill.sum() / s.ill.sum(), 0); put("ray.c.ratio", NUM["ray.c.young.F"][0] / NUM["ray.c.young.M"][0], 2)
# regions: 20-34 vs 50-54, all (ray) and unchanged borders only (rayx)
for kk, d_ in (("ray", rc_), ("rayx", rc_[rc_.approx_borders == 0])):
    for yv, wv, tg in (("gain_pp", "pop_1926", "p"), ("conv", "ill", "t")):
        rq = fit(yv + " ~ young * female + middle * female + C(rayon)", d_, w=wv, cluster="rayon"); putc(f"{kk}.{tg}m", rq, "young"); putl(f"{kk}.{tg}w", rq, "young + young:female = 0"); putc(f"{kk}.{tg}d", rq, "young:female")
    puts(f"{kk}.nobs", str(len(d_))); puts(f"{kk}.nunits", str(d_.rayon.nunique()))
# 1959 check, rural: literacy can't fall within a cohort, so an inflated 1939 figure would show up as a fall
c59 = pd.read_csv(f"{D}/census1959_rsfsr_edu_by_age_sex.csv", sep=";", encoding="utf-8-sig")
for sx in ("M", "F"):
    for a39, a59 in (("30-34", "50-54"), ("35-39", "55-59"), ("40-44", "60-64"), ("45-49", "65-69")):
        s = top[(top.area == "rural") & (top.sex == sx) & (top.age == a39)]; l39 = 100 * s.literate.sum() / s.population.sum()
        l59 = float(c59[(c59.area == "rural") & (c59.sex == sx) & (c59.age == a59)].literacy.iloc[0])
        put(f"c39r.{sx}.{a39}", l39, 1); put(f"c59.{sx}.{a39}", l59, 1); put(f"d5939.{sx}.{a39}", l59 - l39, 1)
s = top[(top.area == "rural") & top.age.isin(["30-34", "35-39", "40-44"])]
for sx in ("M", "F"):
    s_ = s[s.sex == sx]; l39 = 100 * s_.literate.sum() / s_.population.sum(); c_ = c59[(c59.area == "rural") & (c59.sex == sx) & c59.age.isin(["50-54", "55-59", "60-64"])]
    l59 = 100 * c_.literate.sum() / (c_.total - c_.education_not_stated).sum(); put(f"c39r.{sx}.young", l39, 0); put(f"c59.{sx}.young", l59, 0); put(f"d5939.{sx}.young", l59 - l39, 1); put(f"c39r.{sx}.young1", l39, 1); put(f"c59.{sx}.young1", l59, 1)
# same for total (village -> town migration doesn't matter there) and urban
for area, tag in (("total", "t"), ("urban", "u")):
    for sx in ("M", "F"):
        for a39, a59 in (("30-34", "50-54"), ("35-39", "55-59"), ("40-44", "60-64"), ("45-49", "65-69")):
            s = top[(top.area == area) & (top.sex == sx) & (top.age == a39)]; l39 = 100 * s.literate.sum() / s.population.sum()
            l59 = float(c59[(c59.area == area) & (c59.sex == sx) & (c59.age == a59)].literacy.iloc[0])
            put(f"c39{tag}.{sx}.{a39}", l39, 1); put(f"c59{tag}.{sx}.{a39}", l59, 1); put(f"d5939{tag}.{sx}.{a39}", l59 - l39, 1)
        s_ = top[(top.area == area) & (top.sex == sx) & top.age.isin(["30-34", "35-39", "40-44"])]; l39 = 100 * s_.literate.sum() / s_.population.sum()
        c_ = c59[(c59.area == area) & (c59.sex == sx) & c59.age.isin(["50-54", "55-59", "60-64"])]; l59 = 100 * c_.literate.sum() / (c_.total - c_.education_not_stated).sum()
        put(f"c39{tag}.{sx}.young1", l39, 1); put(f"c59{tag}.{sx}.young1", l59, 1); put(f"d5939{tag}.{sx}.young", l59 - l39, 1); put(f"c59{tag}.surv.{sx}", c_.total.sum() / s_.population.sum(), 2)
# three censuses: cohorts 20-34 in 1926 (Table XV, 17 regions = RSFSR of 1939) in 1939 and 1959
# group lo..lo+4 of 1926 is lo+12..lo+16 in Jan 1939 and lo+32..lo+36 in Jan 1959 -> 3 years of one group + 2 of the next
def mix39(area, sx, lo):
    s1 = top[(top.area == area) & (top.sex == sx) & (top.age == f"{lo + 10}-{lo + 14}")]; s2 = top[(top.area == area) & (top.sex == sx) & (top.age == f"{lo + 15}-{lo + 19}")]
    return 100 * (0.6 * s1.literate.sum() + 0.4 * s2.literate.sum()) / (0.6 * s1.population.sum() + 0.4 * s2.population.sum())
def mix59(area, sx, lo):
    t1 = c59[(c59.area == area) & (c59.sex == sx) & (c59.age == f"{lo + 30}-{lo + 34}")].iloc[0]; t2 = c59[(c59.area == area) & (c59.sex == sx) & (c59.age == f"{lo + 35}-{lo + 39}")].iloc[0]
    return 100 * (0.6 * t1.literate + 0.4 * t2.literate) / (0.6 * (t1.total - t1.education_not_stated) + 0.4 * (t2.total - t2.education_not_stated))
ry3 = pd.read_csv(f"{D}/linked_cohorts_rayon_1926_1939.csv", sep=";", encoding="utf-8-sig"); puts("c3.regions", str(ry3.rayon.nunique()))
for area, tag in (("rural", "r"), ("total", "t")):
    for sx in ("M", "F"):
        w3 = {}; v3 = {}
        for lo in (20, 25, 30):
            b = f"{lo}-{lo + 4}"; s = ry3[(ry3.area == area) & (ry3.sex == sx) & (ry3.age_1926 == b)]; w3[b] = s.pop_1926.sum(); v3[b] = (np.average(s.lit_1926, weights=s.pop_1926), mix39(area, sx, lo), mix59(area, sx, lo))
            put(f"c3{tag}.{sx}.{b}.26", v3[b][0], 1); put(f"c3{tag}.{sx}.{b}.39", v3[b][1], 1); put(f"c3{tag}.{sx}.{b}.59", v3[b][2], 1)
        l26, l39, l59 = (sum(w3[b] * v3[b][i] for b in w3) / sum(w3.values()) for i in range(3))
        put(f"c3{tag}.{sx}.young.26", l26, 1); put(f"c3{tag}.{sx}.young.39", l39, 1); put(f"c3{tag}.{sx}.young.59", l59, 1); put(f"c3{tag}.{sx}.d5939", l59 - l39, 1); put(f"c3{tag}.{sx}.gain39", l39 - l26, 1); put(f"c3{tag}.{sx}.gain59", l59 - l26, 1)
        put(f"c3{tag}.{sx}.taught39", 100 * (l39 - l26) / (100 - l26), 0); put(f"c3{tag}.{sx}.taught59", 100 * (l59 - l26) / (100 - l26), 0); put(f"c3{tag}.{sx}.kept", 100 * (l59 - l26) / (l39 - l26), 0)
# main figure: literacy by year of birth in four censuses, 17 regions (1897, 1926 from Table XV; 1939, 1959 RSFSR totals)
# each census with its own five-year groups, nothing interpolated. keys cp{r|t}.{sex}.{census}.{age group}
from names import en
x17 = xv[xv.region_gosplan_1927.isin(ry3.rayon.unique())]; puts("cp.regions", str(x17.region_gosplan_1927.nunique()))
CPB = {1897: [f"{a}-{a + 4}" for a in range(15, 65, 5)], 1926: [f"{a}-{a + 4}" for a in range(20, 75, 5)], 1939: [f"{a}-{a + 4}" for a in range(30, 70, 5)], 1959: [f"{a}-{a + 4}" for a in range(50, 70, 5)]}
for area, tag in (("rural", "r"), ("total", "t")):
    newl = {}
    for sx in ("M", "F"):
        for yr in (1897, 1926):
            s = x17[(x17.census_year == yr) & (x17.area == area) & (x17.sex == sx) & x17.age.isin(CPB[yr])]; assert s.population.notna().all() and s.literate.notna().all()
            s = s.groupby("age")[["population", "literate"]].sum()
            for b in CPB[yr]: put(f"cp{tag}.{sx}.{yr}.{b}", 100 * s.loc[b, "literate"] / s.loc[b, "population"], 1)
        s = top[(top.area == area) & (top.sex == sx)].groupby("age")[["population", "literate"]].sum()
        for b in CPB[1939]: put(f"cp{tag}.{sx}.1939.{b}", 100 * s.loc[b, "literate"] / s.loc[b, "population"], 1)
        c_ = c59[(c59.area == area) & (c59.sex == sx)].set_index("age")
        for b in CPB[1959]: put(f"cp{tag}.{sx}.1959.{b}", 100 * c_.loc[b, "literate"] / (c_.loc[b, "total"] - c_.loc[b, "education_not_stated"]), 1)
        # cohort 20-34 in 1897, thirty years later (same ages, one generation earlier)
        a_ = x17[(x17.census_year == 1897) & (x17.area == area) & (x17.sex == sx) & x17.age.isin(["20-24", "25-29", "30-34"])]; b_ = x17[(x17.census_year == 1926) & (x17.area == area) & (x17.sex == sx) & x17.age.isin(["50-54", "55-59", "60-64"])]
        l97 = 100 * a_.literate.sum() / a_.population.sum(); l26 = 100 * b_.literate.sum() / b_.population.sum()
        put(f"b4{tag}.{sx}.97", l97, 1); put(f"b4{tag}.{sx}.26", l26, 1); put(f"b4{tag}.{sx}.d", l26 - l97, 1); put(f"b4{tag}.{sx}.taught", 100 * (l26 - l97) / (100 - l97), 0)
        dd_ = [NUM[f"cp{tag}.{sx}.1926.{lo + 30}-{lo + 34}"][0] - NUM[f"cp{tag}.{sx}.1897.{lo}-{lo + 4}"][0] for lo in range(15, 45, 5)]   # 1897 groups 15-44, thirty years later
        put(f"b4{tag}.{sx}.dmin", min(dd_), 1); put(f"b4{tag}.{sx}.dmax", max(dd_), 1); put(f"b4{tag}.{sx}.maxabs", max(abs(v_) for v_ in dd_), 1)
        # every group 20-54 of 1926 in 1939; number who learned at 20-49 (cohort sizes of 1939)
        pop = ill = new = 0.0
        for lo in range(20, 55, 5):
            b = f"{lo}-{lo + 4}"; s = ry3[(ry3.area == area) & (ry3.sex == sx) & (ry3.age_1926 == b)]; p26 = s.pop_1926.sum(); l26 = np.average(s.lit_1926, weights=s.pop_1926); l39 = mix39(area, sx, lo)
            put(f"c4{tag}.{sx}.{b}.26", l26, 1); put(f"c4{tag}.{sx}.{b}.39", l39, 1); put(f"c4{tag}.{sx}.{b}.d", l39 - l26, 1); put(f"c4{tag}.{sx}.{b}.t", 100 * (l39 - l26) / (100 - l26), 0)
            if lo < 50:
                s1 = top[(top.area == area) & (top.sex == sx) & (top.age == f"{lo + 10}-{lo + 14}")]; s2 = top[(top.area == area) & (top.sex == sx) & (top.age == f"{lo + 15}-{lo + 19}")]; p39 = 0.6 * s1.population.sum() + 0.4 * s2.population.sum()
                pop += p26; ill += p26 * (100 - l26) / 100; new += p39 * (l39 - l26) / 100
        put(f"cnt{tag}.{sx}.pop", pop / 1e6, 1); put(f"cnt{tag}.{sx}.ill", ill / 1e6, 1); put(f"cnt{tag}.{sx}.new", new / 1e6, 1); newl[sx] = new
    put(f"cnt{tag}.shareF", 100 * newl["F"] / (newl["F"] + newl["M"]), 0)
# same cohort by region (rural, 20-34 in 1926), fig28
rg = ry3[(ry3.area == "rural") & ry3.age_1926.isin(["20-24", "25-29", "30-34"])].groupby(["rayon", "sex"]).apply(lambda t: pd.Series({"l26": np.average(t.lit_1926, weights=t.pop_1926), "l39": np.average(t.lit_1939, weights=t.pop_1926), "pop_1926": t.pop_1926.sum(), "approx_borders": t.approx_borders.max()})).reset_index()
rg["gain"] = rg.l39 - rg.l26; rg["taught"] = 100 * rg.gain / (100 - rg.l26); rg["region_en"] = rg.rayon.map(en); rg.to_csv(f"{R}/S1_region_gains.csv", sep=";", index=False, encoding="utf-8-sig")
f_ = rg[rg.sex == "F"].set_index("region_en"); puts("reg.n", str(len(f_))); puts("reg.F.positive", str(int((f_.gain > 0).sum())))
put("reg.F.gain.min", f_.gain.min(), 0); put("reg.F.gain.max", f_.gain.max(), 0); puts("reg.F.gain.min.name", f_.gain.idxmin()); puts("reg.F.gain.max.name", f_.gain.idxmax()); put("reg.F.l26.min", f_.l26.min(), 0); put("reg.F.l26.max", f_.l26.max(), 0)
put("reg.F.taught.min", f_.taught.min(), 0); put("reg.F.taught.max", f_.taught.max(), 0); puts("reg.F.taught.min.name", f_.taught.idxmin()); puts("reg.F.taught.max.name", f_.taught.idxmax()); put("reg.F.corr", np.corrcoef(f_.l26, f_.gain)[0, 1], 2)
put("reg.F.l39.min", f_.l39.min(), 0); puts("reg.F.l39.min.name", f_.l39.idxmin()); put("reg.F.sd26", f_.l26.std(), 0); put("reg.F.sd39", f_.l39.std(), 0)
P("regions, rural women aged 20-34 in 1926:\n" + f_[["l26", "l39", "gain", "taught", "approx_borders"]].round(1).sort_values("gain").to_string())

# =====================================================================================================================
# 4. The determinants of women's progress in the two regimes
# =====================================================================================================================
P("\n=== 4. Two regimes ===")
PRED = ["teachers_percap_1911", "urban_share_M", "cwr", "agshare_1897"]; PK = {"teachers_percap_1911": "t", "urban_share_M": "u", "cwr": "c", "agshare_1897": "a"}
rbp = z(rb[["region", "pg"] + PRED], PRED)
u = ball.rename(columns={"population": "total"})[["region", "band", "sex", "total", "literacy"]].rename(columns={"literacy": "lit"})
w1 = u[u.band.isin(["40-49", "60-69"])].copy(); w1 = w1[w1.groupby("region").lit.transform("size") == 4]
w1["T"] = (w1.band == "40-49").astype(int); w1["female"] = (w1.sex == "F").astype(int); w1["y"] = w1.lit; w1["wt"] = w1.total; w1["unit"] = w1.region; w1["phase2"] = 0; w1["cohfe"] = "p1_" + w1.band
w2 = cl[cl.age_1926.isin(YOUNG + PLACEBO)].copy(); w2["T"] = w2.young; w2["y"] = w2.gain_pp; w2["wt"] = w2.pop_1926; w2["unit"] = w2.unit_1926; w2["phase2"] = 1; w2["cohfe"] = "p2_" + w2.age_1926
w2b = cl[cl.age_1926.isin(YOUNG + MIDDLE)].copy(); w2b["T"] = w2b.young; w2b["y"] = w2b.gain_pp; w2b["wt"] = w2b.pop_1926; w2b["unit"] = w2b.unit_1926; w2b["phase2"] = 1; w2b["cohfe"] = "p2_" + w2b.age_1926
w2c_ = clc[clc.age_1926.isin(YOUNG + PLACEBO)].copy(); w2c_["T"] = w2c_.young; w2c_["y"] = w2c_.conv; w2c_["wt"] = w2c_.ill; w2c_["unit"] = w2c_.unit_1926; w2c_["phase2"] = 1; w2c_["cohfe"] = "p2_" + w2c_.age_1926
COLS = ["unit", "y", "wt", "T", "female", "phase2", "cohfe"]
def stack(a_, b_):
    s = pd.concat([a_[COLS], b_[COLS]]).merge(rbp, left_on="unit", right_on="region", how="left"); s["pg"] = s.pg.fillna(s.unit); s["up"] = s.unit + "|" + s.phase2.astype(str); s["wt"] = s.wt / s.groupby("phase2").wt.transform("sum"); return s
F3 = "y ~ C(up) + C(cohfe) + female + female:phase2 + T:female + T:female:phase2 + T:z + T:z:phase2 + female:z + female:z:phase2 + T:female:z + T:female:z:phase2"
def tworeg(st, key, w="wt"):
    for c in PRED:
        d = st.dropna(subset=[c + "_z"]).copy(); d["z"] = d[c + "_z"]; r = fit(F3, d, w=w, cluster="pg"); kk = f"{key}.{PK[c]}"
        putc(kk + ".1", r, "T:female:z"); putl(kk + ".2", r, "T:female:z + T:female:z:phase2 = 0"); putc(kk + ".d", r, "T:female:z:phase2")
        puts(kk + ".u1", str(d[d.phase2 == 0].unit.nunique())); puts(kk + ".u2", str(d[d.phase2 == 1].unit.nunique())); puts(kk + ".c1", str(int((d.phase2 == 0).sum()))); puts(kk + ".c2", str(int((d.phase2 == 1).sum())))
st = stack(w1, w2); st.to_csv(f"{R}/T_two_regime_cells.csv", sep=";", index=False, encoding="utf-8-sig"); stack(w1, w2b).to_csv(f"{R}/T_two_regime_cells_middle.csv", sep=";", index=False, encoding="utf-8-sig"); tworeg(st, "tr"); tworeg(stack(w1, w2b), "trb"); tworeg(st[~st.unit.isin(LOWQ)], "trl"); tworeg(st, "tru", w=None); tworeg(stack(w1, w2c_), "trc")
for kk_, st_ in (("tr", st),):
    d = st_.dropna(subset=[c + "_z" for c in PRED]).copy()
    for ph, lab in ((0, "1"), (1, "2")):
        dd_ = d[d.phase2 == ph]; f_ = "y ~ C(unit) + C(cohfe) + female + T:female + " + " + ".join(f"T:{c}_z + female:{c}_z + T:female:{c}_z" for c in PRED)
        r = fit(f_, dd_, w="wt", cluster="pg")
        for c in PRED: putc(f"trj.{PK[c]}.{lab}", r, f"T:female:{c}_z")
        putc(f"trj.tf.{lab}", r, "T:female"); puts(f"trj.n.{lab}", str(int(r.nobs)))
# unit level
w1u = rb[["region", "lit_F_40-49", "lit_F_60-69", "lit_M_40-49", "lit_M_60-69"]].copy()
for c in w1u.columns[1:]: w1u.loc[~w1u[c].between(0, 100), c] = np.nan
w1u["w1_F"] = w1u["lit_F_40-49"] - w1u["lit_F_60-69"]; w1u["w1_M"] = w1u["lit_M_40-49"] - w1u["lit_M_60-69"]; w1u = w1u.dropna(subset=["w1_F", "w1_M"]).merge(rbp, on="region")
w2u = wu.merge(rbp, left_on="unit_1926", right_on="region", how="left"); w2u = z(w2u, ["lit26_F", "lit26_M"])
for c in PRED:
    kk = PK[c]; d = w1u.dropna(subset=[c + "_z"]); r = fit(f"w1_F ~ {c}_z", d, cluster="pg"); putc(f"tru1.F.{kk}", r, c + "_z"); puts(f"tru1.F.{kk}.n", str(int(r.nobs)))
    d = w2u.dropna(subset=[c + "_z"]); r = fit(f"gain_F ~ lit26_F_z + {c}_z", d, w="pop", cluster="pg"); putc(f"tru2.F.{kk}", r, c + "_z"); puts(f"tru2.F.{kk}.n", str(int(r.nobs)))
    r = fit(f"gain_M ~ lit26_M_z + {c}_z", d, w="pop", cluster="pg"); putc(f"tru2.M.{kk}", r, c + "_z")
r = fit("gain_M ~ lit26_M_z", w2u, w="pop", cluster="pg"); putc("tru2.M.own", r, "lit26_M_z"); r = fit("gain_F ~ lit26_F_z", w2u, w="pop", cluster="pg"); putc("tru2.F.own", r, "lit26_F_z")
w1u[["region", "w1_F", "w1_M"]].merge(rb[["region"] + PRED], on="region").to_csv(f"{R}/C_wave1_proxy_units.csv", sep=";", index=False)
wu.to_csv(f"{R}/B7_unit_level_wave2.csv", sep=";", index=False)

# =====================================================================================================================
# 5. Korenizatsiya in 1926
# =====================================================================================================================
k3 = kr[kr.group.isin(["Татары", "Чуваши", "Марийцы", "Мордва", "Вотяки", "Башкиры"])].copy(); k3["soviet"] = k3.band.isin(["12-14", "15-19"]).astype(int); k3["gsc"] = k3.group + "|" + k3.sex + "|" + k3.band
k3.to_csv(f"{R}/E_korenizatsiya_cells.csv", sep=";", index=False, encoding="utf-8-sig"); k3["ts"] = k3.titular_unit * k3.soviet; k3["tf_"] = k3.titular_unit * k3.female; k3["tsf"] = k3.titular_unit * k3.soviet * k3.female
FK = "literacy ~ C(gsc) + C(rc) + titular_unit + ts + tf_ + tsf"
for kk, d_ in (("kor", k3), ("kor.notat", k3[k3.group != "Татары"])):
    r = fit(FK, d_, w="population", cluster="region")
    for t_, nm in (("titular_unit", "t"), ("ts", "ts"), ("tf_", "tf"), ("tsf", "tsf")): putc(f"{kk}.{nm}", r, t_)
    puts(f"{kk}.n", str(int(r.nobs))); puts(f"{kk}.inside", str(int(d_.titular_unit.sum())))

# =====================================================================================================================
# 6. The legacy in the census of 2010
# =====================================================================================================================
P("\n=== 6. Legacy ===")
t13 = pd.read_csv(f"{D}/census2010_nat_edu_by_age_sex.csv", sep=";", encoding="utf-8-sig"); t14 = pd.read_csv(f"{D}/census2010_nat_edu_by_subject.csv", sep=";", encoding="utf-8-sig")
AGES = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70 и более"]; OLD = AGES[-3:]; MID = AGES[6:8]
SIX = ["Татары", "Башкиры", "Чуваши", "Марийцы", "Удмурты", "Мордва"]
dn = t13[(t13.area == "total") & t13.age.isin(AGES) & t13.sex.isin(["M", "F"])]; rus13 = dn[dn.nationality == "Русские"].set_index(["sex", "age"])
def gaps13(nats):
    rows = []
    for nat in nats:
        for _, r_ in dn[dn.nationality == nat].iterrows():
            rows.append(dict(nat=nat, sex=r_.sex, age=r_.age, gap_sec=rus13.loc[(r_.sex, r_.age), "sh_sec_plus"] - r_.sh_sec_plus, gap_higher=rus13.loc[(r_.sex, r_.age), "sh_higher"] - r_.sh_higher,
                             gap_basic=rus13.loc[(r_.sex, r_.age), "sh_basic_plus"] - r_.sh_basic_plus, pop=r_.stated))
    o = pd.DataFrame(rows); o["female"] = (o.sex == "F").astype(int); o["old"] = o.age.isin(OLD).astype(int); o["mid"] = o.age.isin(MID).astype(int); o["fo"] = o.female * o.old; o["fmid"] = o.female * o.mid
    o["na"] = o.nat + "|" + o.age; o["sa"] = o.sex + "|" + o.age; return o
J1 = gaps13(SIX); J1.to_csv(f"{R}/J1_ethnic_gap_2010_by_sex_age.csv", sep=";", index=False, encoding="utf-8-sig")
for nat in SIX:
    for sx in ("M", "F"):
        t = J1[(J1.nat == nat) & (J1.sex == sx)].set_index("age").gap_sec; v = t.reindex(OLD); put(f"l10.{EN[nat]}.{sx}.min", v.min(), 0); put(f"l10.{EN[nat]}.{sx}.max", v.max(), 0)
for kk, yv, f_ in (("c10.a", "gap_sec", "C(nat) + C(age)"), ("c10.b", "gap_sec", "C(na)"), ("c10.h", "gap_higher", "C(nat) + C(age)")):
    r = fit(f"{yv} ~ {f_} + female + fmid + fo", J1, w="pop", cluster="nat"); putc(kk + ".y", r, "female"); putc(kk + ".m", r, "fmid"); putc(kk + ".o", r, "fo"); puts(kk + ".n", str(int(r.nobs)))
for nat in SIX:
    gq = J1[J1.nat == nat]; r = smf.wls("gap_sec ~ C(age) + female + fmid + fo", data=gq, weights=gq["pop"]).fit(cov_type="HC1"); kk = f"c10.{EN[nat]}"
    put(kk + ".y", r.params["female"]); put(kk + ".y.se", r.bse["female"]); put(kk + ".m", r.params["fmid"]); put(kk + ".m.se", r.bse["fmid"]); put(kk + ".o", r.params["fo"]); put(kk + ".o.se", r.bse["fo"])
# nationality x subject
kq = kp[kp.group.isin(NATMAP) & kp.literacy.between(0, 100)].copy(); kq["subject"] = kq.region.map(MAP); kq["nat2010"] = kq.group.map(NATMAP); kq = kq.dropna(subset=["subject"])
def gaps26(bands, tag):
    d = kq[kq.band.isin(bands)]
    g = d.groupby(["subject", "nat2010", "sex", "area"]).apply(lambda t: pd.Series({"lit": 100 * t.literate.sum() / t.population.sum(), "pop": t.population.sum()})).reset_index()
    w_ = g.pivot_table(index=["subject", "nat2010", "area"], columns="sex", values=["lit", "pop"]).reset_index(); w_.columns = ["subject", "nat2010", "area", "lit_F", "lit_M", "pop_F", "pop_M"]
    r_ = w_[w_.nat2010 == "Русские"].set_index(["subject", "area"]); w_ = w_[w_.nat2010 != "Русские"].copy()
    w_[f"gF{tag}"] = [r_.lit_F.get((s, a_), np.nan) - v for s, a_, v in zip(w_.subject, w_.area, w_.lit_F)]; w_[f"gM{tag}"] = [r_.lit_M.get((s, a_), np.nan) - v for s, a_, v in zip(w_.subject, w_.area, w_.lit_M)]
    return w_[["subject", "nat2010", "area", f"gF{tag}", f"gM{tag}"]]
w26 = gaps26(["20-24", "25-29", "30-39", "40-49"], "").merge(gaps26(["20-24", "25-29"], "2029"), on=["subject", "nat2010", "area"], how="left").merge(gaps26(["30-39", "40-49"], "3049"), on=["subject", "nat2010", "area"], how="left").merge(gaps26(["12-14", "15-19"], "1219"), on=["subject", "nat2010", "area"], how="left")
t14r = t14[t14.nationality == "Русские"].set_index(["region", "area"]); t14n = t14[t14.nationality.isin(set(NATMAP.values()) - {"Русские"})].copy()
for yv, col in (("g10", "sh_sec_plus"), ("g10h", "sh_higher")):
    t14n[yv] = [t14r[col].get((r_, a_), np.nan) - v for r_, a_, v in zip(t14n.region, t14n.area, t14n[col])]
t14n["g10i"] = [v - t14r.sh_illit.get((r_, a_), np.nan) for r_, a_, v in zip(t14n.region, t14n.area, t14n.sh_illit)]
J2 = w26.merge(t14n.rename(columns={"region": "subject", "nationality": "nat2010"})[["subject", "nat2010", "area", "stated", "g10", "g10h", "g10i"]], on=["subject", "nat2010", "area"]).dropna(subset=["gF", "gM", "g10"])
J2["muslim"] = J2.nat2010.isin(["Татары", "Башкиры"]).astype(int)
TIT = {"Татары": "Республика Татарстан", "Башкиры": "Республика Башкортостан", "Чуваши": "Чувашская Республика", "Марийцы": "Республика Марий Эл", "Удмурты": "Удмуртская Республика", "Карелы": "Республика Карелия", "Калмыки": "Республика Калмыкия"}
J2["titular"] = [int(TIT.get(n_) == s_) for n_, s_ in zip(J2.nat2010, J2.subject)]
# age standardisation and rural shares
bq = t13[(t13.area == "total") & (t13.sex == "B") & t13.age.isin(AGES)]; rB = bq[bq.nationality == "Русские"].set_index("age"); wR = rB.stated / rB.stated.sum(); adj = {}
for nat, g_ in bq.groupby("nationality"):
    g_ = g_.set_index("age").reindex(rB.index).dropna(subset=["stated", "sh_sec_plus"])
    if len(g_) == len(rB): adj[nat] = np.average(g_.sh_sec_plus, weights=wR.reindex(g_.index)) - np.average(g_.sh_sec_plus, weights=g_.stated)
J2["g10adj"] = J2.g10 - J2.nat2010.map(adj)
ts = t14[t14.area.isin(["total", "rural"])].pivot_table(index=["region", "nationality"], columns="area", values="stated").reset_index(); ts["rs"] = 100 * ts.rural.fillna(0) / ts.total; rsh = ts.set_index(["region", "nationality"]).rs.to_dict()
J2["rural_diff"] = [rsh.get((s_, n_), np.nan) - rsh.get((s_, "Русские"), np.nan) for s_, n_ in zip(J2.subject, J2.nat2010)]
J2.to_csv(f"{R}/J2_ethnic_gaps_1926_2010.csv", sep=";", index=False, encoding="utf-8-sig")
jt = J2[J2.area == "total"].copy(); jr = J2[J2.area == "rural"].copy()
puts("leg.n", str(len(jt))); puts("leg.subjects", str(jt.subject.nunique())); puts("leg.nat", str(jt.nat2010.nunique())); puts("leg.n.r", str(len(jr))); puts("leg.subjects.r", str(jr.subject.nunique()))
put("leg.g10.mean", jt.g10.mean()); put("leg.g10.sd", jt.g10.std()); put("leg.g10.wmean", np.average(jt.g10, weights=jt.stated)); put("leg.gF.mean", jt.gF.mean()); put("leg.gF.sd", jt.gF.std()); put("leg.gM.mean", jt.gM.mean()); put("leg.gM.sd", jt.gM.std())
put("leg.corr", jt.gF.corr(jt.gM), 2); put("leg.corr.nm", jt[jt.muslim == 0].gF.corr(jt[jt.muslim == 0].gM), 2)
def leg(key, f, d, w="stated", F_="gF", M_="gM"):
    need = [c for c in ("gF", "gM", "gF2029", "gM2029", "gF3049", "gM3049", "gF1219", "gM1219", "rural_diff", "g10adj", "g10h", "g10i", "g10") if c in f]
    d = d.dropna(subset=need); r = fit(f, d, w=w, cluster="subject")
    if F_ in r.params.index: putc(key + ".F", r, F_, 2)
    if M_ in r.params.index: putc(key + ".M", r, M_, 2)
    puts(key + ".n", str(int(r.nobs))); return r
for sfx, d_ in (("", jt), (".r", jr)):
    leg("leg.nofe" + sfx, "g10 ~ gF + gM", d_); leg("leg" + sfx, "g10 ~ gF + gM + C(subject)", d_); leg("leg.fo" + sfx, "g10 ~ gF + C(subject)", d_); leg("leg.mo" + sfx, "g10 ~ gM + C(subject)", d_)
    leg("leg.2029" + sfx, "g10 ~ gF2029 + gM2029 + C(subject)", d_, F_="gF2029", M_="gM2029"); leg("leg.3049" + sfx, "g10 ~ gF3049 + gM3049 + C(subject)", d_, F_="gF3049", M_="gM3049"); leg("leg.1219" + sfx, "g10 ~ gF1219 + gM1219 + C(subject)", d_, F_="gF1219", M_="gM1219")
    leg("leg.h" + sfx, "g10h ~ gF + gM + C(subject)", d_); leg("leg.kal" + sfx, "g10 ~ gF + gM + C(subject)", d_[d_.nat2010 != "Калмыки"]); leg("leg.ugk" + sfx, "g10 ~ gF + gM + C(subject)", d_[~d_.nat2010.isin(["Украинцы", "Немцы", "Казахи"])])
    leg("leg.six" + sfx, "g10 ~ gF + gM + C(subject)", d_[d_.nat2010.isin(SIX)]); leg("leg.unw" + sfx, "g10 ~ gF + gM + C(subject)", d_, w=None); leg("leg.natfe" + sfx, "g10 ~ gF + gM + C(subject) + C(nat2010)", d_)
    leg("leg.illit" + sfx, "g10i ~ gF + gM + C(subject)", d_); leg("leg.adj" + sfx, "g10adj ~ gF + gM + C(subject)", d_); leg("leg.rur" + sfx, "g10 ~ gF + gM + rural_diff + C(subject)", d_)
    leg("leg.mt" + sfx, "g10 ~ gF + gM + muslim + titular + C(subject)", d_); leg("leg.nm" + sfx, "g10 ~ gF + gM + C(subject)", d_[d_.muslim == 0]); leg("leg.nmfo" + sfx, "g10 ~ gF + C(subject)", d_[d_.muslim == 0]); leg("leg.nmmo" + sfx, "g10 ~ gM + C(subject)", d_[d_.muslim == 0])
put("leg.effect", NUM["leg.F"][0] * jt.gF.std(), 1)
ls = [fit("g10 ~ gF + gM + C(subject)", jt[jt.subject != s], w="stated", cluster="subject").params["gF"] for s in jt.subject.unique()]; lnn = [fit("g10 ~ gF + gM + C(subject)", jt[jt.nat2010 != n_], w="stated", cluster="subject").params["gF"] for n_ in jt.nat2010.unique()]
put("leg.loo.s.min", min(ls), 2); put("leg.loo.s.max", max(ls), 2); put("leg.loo.n.min", min(lnn), 2); put("leg.loo.n.max", max(lnn), 2)
if not FAST:
    rng = np.random.default_rng(SEED); j2 = jt.reset_index(drop=True); F_ = FWL(j2, ["subject"], "stated"); yr = F_.res(j2.g10.values); obs = F_.ols(yr, F_.res(j2[["gF", "gM"]].values))[0]; a_ = []
    for _ in range(5000):
        ii = rng.permutation(len(j2)); a_.append(F_.ols(yr, F_.res(j2[["gF", "gM"]].values[ii]))[0])
    a_ = np.array(a_); puts("leg.perm", pstr(float(np.mean(np.abs(a_) >= abs(obs))))); put("leg.perm.lo", np.quantile(a_, .025), 2); put("leg.perm.hi", np.quantile(a_, .975), 2); np.savetxt(f"{R}/L3_permutation_betaF.txt", a_)
    t0, pw = wild_p(jt, ["subject"], ["gF", "gM"], "gF", "g10", "stated", "subject", B=1999); puts("leg.wild.F", pstr(pw)); t0, pw = wild_p(jt, ["subject"], ["gF", "gM"], "gM", "g10", "stated", "subject", B=1999); puts("leg.wild.M", pstr(pw))
# sex-differenced design (national tables of 2010)
kn = kp[kp.group.isin(NATMAP) & kp.literacy.between(0, 100)].copy(); kn["nat"] = kn.group.map(NATMAP)
def nat26(bands, area, tag):
    d = kn[(kn.area == area) & kn.band.isin(bands)]; g = d.groupby(["region", "nat", "sex"]).agg(lit=("literate", "sum"), pop=("population", "sum"), nb=("band", "nunique")).reset_index(); g = g[g.nb == len(bands)]; g["rate"] = 100 * g.lit / g["pop"]
    w_ = g.pivot_table(index=["region", "nat"], columns="sex", values=["rate", "pop"]).reset_index(); w_.columns = ["region", "nat", "pop_F", "pop_M", "rate_F", "rate_M"]; w_ = w_.dropna(subset=["rate_F", "rate_M"])
    r_ = w_[w_.nat == "Русские"].set_index("region"); w_ = w_[w_.nat != "Русские"].copy(); w_["gF"] = [r_.rate_F.get(a_, np.nan) - b_ for a_, b_ in zip(w_.region, w_.rate_F)]; w_["gM"] = [r_.rate_M.get(a_, np.nan) - b_ for a_, b_ in zip(w_.region, w_.rate_M)]
    w_ = w_.dropna(subset=["gF", "gM"]); w_["pop"] = w_.pop_F + w_.pop_M
    n_ = w_.groupby("nat").apply(lambda t: pd.Series({f"gF_{tag}": np.average(t.gF, weights=t["pop"]), f"gM_{tag}": np.average(t.gM, weights=t["pop"]), f"units_{tag}": len(t)})); n_[f"D_{tag}"] = n_[f"gF_{tag}"] - n_[f"gM_{tag}"]; return n_
n26 = nat26(["20-24", "25-29", "30-39", "40-49"], "total", "ad").join(nat26(["12-14", "15-19", "20-24", "25-29"], "total", "yg"), how="left")
g10 = gaps13(sorted(set(n26.index) & set(dn.nationality.unique()))).merge(n26.reset_index(), on="nat"); puts("sd.nat", str(g10.nat.nunique())); puts("sd.n", str(len(g10)))
g10.to_csv(f"{R}/S_legacy_sexdiff_cells.csv", sep=";", index=False, encoding="utf-8-sig")
def sdiff(d, key, yv="gap_sec", x="D_ad", w="pop", perm=True):
    d = d.dropna(subset=[x]).reset_index(drop=True); d["fx"] = d.female * d[x]; d["fxm"] = d.fmid * d[x]; d["fxo"] = d.fo * d[x]
    r = fit(f"{yv} ~ C(na) + C(sa) + fx + fxm + fxo", d, w=w, cluster="nat"); putc(key + ".y", r, "fx", 2); putl(key + ".m", r, "fx + fxm = 0", 2); putl(key + ".o", r, "fx + fxo = 0", 2); putc(key + ".d", r, "fxo", 2)
    puts(key + ".n", str(int(r.nobs))); puts(key + ".nat", str(d.nat.nunique()))
    if perm and not FAST:
        rng = np.random.default_rng(SEED); F_ = FWL(d, ["na", "sa"], w); yr = F_.res(d[yv].values); nats = list(d.nat.unique()); vals = d.groupby("nat")[x].first().reindex(nats).values
        def co(v):
            xx = d.nat.map(dict(zip(nats, v))).values; b_ = F_.ols(yr, F_.res(np.column_stack([d.female.values * xx, d.fmid.values * xx, d.fo.values * xx]))); return b_[0] + b_[2]
        obs = co(vals); perms = list(itertools.permutations(range(len(nats)))) if len(nats) <= 7 else [rng.permutation(len(nats)) for _ in range(10000)]
        a_ = np.array([co(vals[list(p_)]) for p_ in perms]); puts(key + ".perm", pstr(float(np.mean(np.abs(a_) >= abs(obs) - 1e-12)))); puts(key + ".perm.draws", fint(len(perms)))
v6 = g10[g10.nat.isin(SIX)]
sdiff(v6, "sd.six"); sdiff(g10, "sd.all"); sdiff(g10[~g10.nat.isin(["Татары", "Башкиры", "Казахи"])], "sd.nm"); sdiff(v6, "sd.six.unw", w=None); sdiff(v6, "sd.six.yg", x="D_yg"); sdiff(v6, "sd.six.h", yv="gap_higher"); sdiff(v6, "sd.six.b", yv="gap_basic")
lo6 = []
for n_ in SIX:
    sdiff(v6[v6.nat != n_], "sd.tmp", perm=False); lo6.append(NUM["sd.tmp.o"][0])
put("sd.loo.min", min(lo6), 2); put("sd.loo.max", max(lo6), 2)
s = g10.pivot_table(index=["nat", "age"], columns="sex", values=["gap_sec", "pop"]).reset_index(); s.columns = ["nat", "age", "gF", "gM", "pF", "pM"]; s["excess"] = s.gF - s.gM; s["w"] = s.pF + s.pM
s["grp"] = np.where(s.age.isin(OLD), "old", np.where(s.age.isin(MID), "mid", "young")); e = s.groupby(["nat", "grp"]).apply(lambda t: np.average(t.excess, weights=t.w)).unstack().join(n26[["gF_ad", "gM_ad", "D_ad", "units_ad"]])
e.to_csv(f"{R}/S_legacy_sexdiff_nationalities.csv", sep=";", encoding="utf-8-sig"); P(e.round(1).sort_values("D_ad").to_string())
for n_ in e.index:
    for c in ("old", "mid", "young", "gF_ad", "gM_ad", "D_ad"): put(f"sdn.{EN.get(n_, n_)}.{c}", e.loc[n_, c])
e6 = e.loc[SIX]; put("sd.corr.six", np.corrcoef(e6.D_ad, e6.old)[0, 1], 2); put("sd.corr.all", np.corrcoef(e.D_ad, e.old)[0, 1], 2)
# children of 1939
rowsI = []
for (u_, r39), g in lc[(lc.area == "rural") & ~lc.unit_1926.isin(BAD39) & lc.gain_pp.between(-40, 90)].groupby(["unit_1926", "region_1939"]):
    def mm(sex, ages, col):
        s_ = g[(g.sex == sex) & g.age_1926.isin(ages)]; return np.average(s_[col], weights=s_.pop_1926) if len(s_) else np.nan
    kids = c39[(c39.region_1939 == r39) & (c39.area == "rural") & c39.age.isin([str(a_) for a_ in range(9, 15)])]
    if kids.empty: continue
    kk = kids.groupby("sex")[["population", "literate"]].sum()
    rowsI.append(dict(unit=u_, kid39F=100 * kk.loc["F", "literate"] / kk.loc["F", "population"], kid39M=100 * kk.loc["M", "literate"] / kk.loc["M", "population"], kidpop=kk.population.sum(), gF=mm("F", YOUNG, "gain_pp"), gM=mm("M", YOUNG, "gain_pp"), kid26F=mm("F", ["8-12"], "lit_1926"), kid26M=mm("M", ["8-12"], "lit_1926")))
ig = pd.DataFrame(rowsI); ig["gap39"] = ig.kid39M - ig.kid39F; ig["gap26"] = ig.kid26M - ig.kid26F; ig.to_csv(f"{R}/I_intergen_units.csv", sep=";", index=False, encoding="utf-8-sig"); puts("ig.units", str(len(ig))); put("ig.girls39", np.average(ig.kid39F, weights=ig.kidpop), 1); put("ig.girls39.sd", ig.kid39F.std(), 1); put("ig.girls26", ig.kid26F.mean(), 1)
def igf(f, key):
    d = ig.dropna(subset=[c for c in ig.columns if c in f]); r = smf.wls(f, data=d, weights=d.kidpop).fit(cov_type="HC1")
    for t_ in r.params.index[1:]: put(f"{key}.{t_}", r.params[t_], 2); put(f"{key}.{t_}.se", r.bse[t_], 2)
    put(key + ".r2", r.rsquared, 2); puts(key + ".n", str(int(r.nobs)))
igf("kid39F ~ gF + kid26F", "ig.1"); igf("kid39F ~ gF + gM + kid26F", "ig.2"); igf("kid39M ~ gF + gM + kid26M", "ig.3"); igf("gap39 ~ gF + gM + gap26", "ig.4")

# =====================================================================================================================
# Output
# =====================================================================================================================
flat = [dict(key=k_, value=v_[0], decimals=v_[1], text=fmt(v_[0], v_[1])) for k_, v_ in NUM.items()] + [dict(key=k_, value=np.nan, decimals=np.nan, text=v_) for k_, v_ in STR.items()]
pd.DataFrame(flat).sort_values("key").to_csv(f"{R}/paper_numbers.csv", sep=";", index=False, encoding="utf-8-sig")
json.dump({"NUM": {k_: list(v_) for k_, v_ in NUM.items()}, "STR": STR}, open(f"{R}/paper_numbers.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
P("\ncoefficients that are not identified:", ", ".join(NI) if NI else "none")
open(f"{R}/paper_numbers.txt", "w", encoding="utf-8").write("\n".join(LOG))
print("numbers:", len(NUM), "strings:", len(STR))
import write_numbers; write_numbers.write()   # paper/numbers.tex

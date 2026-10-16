"""Table IX of 1926, v2: validation, then all derived 1926 files rebuilt from data/census1926_tableIX_long.csv
under the old names in data/ (the v1 files are kept in data/v1_before_validation/). Every derived cell has `tier`.

Five-year group of (unit, area, nationality, sex), population and literates separately.
P = printed subtotal, S = sum of the five single years.
  tier 1  P and S agree (|P-S| <= max(2, 0.5%))
  tier 2  they disagree or one is missing: take the one that fits urban + rural = total or the sum over
          nationalities (computed from tier-1 cells)
  tier 3  no identity decides: take the one within 15 points of literacy (40% of population per year of age)
          of the mean of the two neighbouring groups, if the other is outside
  else dropped
A single year is valid if its group is tier 1, or S was taken in tier 2-3. Bands built from single years
(8-11, 12-14, the windows for the link to 1939) use valid single years only.
Last, plausibility rules on bands: population per year > 2.5 x median of the series, literacy > 30 points
from both neighbours, series shorter than 3.
"""
import os, sys, shutil, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"; R = f"{ROOT}/results"
V1 = f"{D}/v1_before_validation"; os.makedirs(V1, exist_ok=True); os.makedirs(R, exist_ok=True)
REBUILT = ["korenizatsiya_panel.csv", "russians_by_region.csv", "russians_region_baseline.csv", "mechanism_panel.csv", "mechanism_panel_clean.csv",
           "tableIX_cohort_gaps.csv", "linked_cohorts_1926_1939.csv"]
for f in REBUILT:
    if os.path.exists(f"{D}/{f}") and not os.path.exists(f"{V1}/{f}"): shutil.copyfile(f"{D}/{f}", f"{V1}/{f}")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

ix = pd.read_csv(f"{D}/census1926_tableIX_long.csv", sep=";", encoding="utf-8-sig", dtype={"age": str})
ix = ix[ix.area.isin(["total", "rural", "urban"])].copy()
KEY = ["region", "area", "group", "sex"]
gt = ix[["region", "group", "group_type"]].drop_duplicates(subset=["region", "group"])
ALL = ix[ix.group_type == "all"].group.iloc[0]
def close(a, b): return abs(a - b) <= max(2, 0.005 * max(abs(a), abs(b)))

# ---------------- five-year groups: printed vs sum of singles ----------------
sg = ix[ix.age.str.fullmatch(r"\d+")].copy(); sg["a"] = sg.age.astype(int); sg = sg[sg.a <= 99]
sg["g5"] = (sg.a // 5 * 5).astype(str) + "-" + (sg.a // 5 * 5 + 4).astype(str)
S = sg.groupby(KEY + ["g5"]).agg(S_pop=("total", lambda x: x.sum() if x.notna().sum() == 5 else np.nan),
                                 S_lit=("literate", lambda x: x.sum() if x.notna().sum() == 5 else np.nan)).reset_index()
Pr = ix[ix.age.str.fullmatch(r"\d+-\d+")][KEY + ["age", "total", "literate", "quality"]].rename(columns={"age": "g5", "total": "P_pop", "literate": "P_lit", "quality": "P_q"})
g = S.merge(Pr, on=KEY + ["g5"], how="outer")
g["lo"] = g.g5.str.split("-").str[0].astype(int)
g = g[g.lo >= 5].reset_index(drop=True)
for v in ("pop", "lit"):
    ok = [(not pd.isna(s)) and (not pd.isna(p)) and close(s, p) for s, p in zip(g[f"S_{v}"], g[f"P_{v}"])]
    g[f"val_{v}"] = np.where(ok, g[f"P_{v}"], np.nan); g[f"tier_{v}"] = np.where(ok, 1, 0); g[f"src_{v}"] = np.where(ok, "PS", "")
groups_by_unit = ix[ix.group_type != "all"].groupby(["region", "area"]).group.unique().to_dict()

def identity_pass(g, v):
    val = g.set_index(KEY + ["g5"])[f"val_{v}"].to_dict()
    get = lambda *k: val.get(k, np.nan)
    n = 0
    for i, r in enumerate(g.itertuples(index=False)):
        if getattr(r, f"tier_{v}") > 0: continue
        Pv, Sv = getattr(r, f"P_{v}"), getattr(r, f"S_{v}")
        targets = []
        if r.area == "total":
            u, ru = get(r.region, "urban", r.group, r.sex, r.g5), get(r.region, "rural", r.group, r.sex, r.g5)
            if not np.isnan(u) and not np.isnan(ru): targets.append(u + ru)
        else:
            other = "urban" if r.area == "rural" else "rural"
            t, o = get(r.region, "total", r.group, r.sex, r.g5), get(r.region, other, r.group, r.sex, r.g5)
            if not np.isnan(t) and not np.isnan(o): targets.append(t - o)
        gl = groups_by_unit.get((r.region, r.area), [])
        if r.group == ALL:
            vals = [get(r.region, r.area, x, r.sex, r.g5) for x in gl]
            if len(vals) and not np.isnan(vals).any(): targets.append(float(np.sum(vals)))
        else:
            a_ = get(r.region, r.area, ALL, r.sex, r.g5); vals = [get(r.region, r.area, x, r.sex, r.g5) for x in gl if x != r.group]
            if not np.isnan(a_) and len(vals) and not np.isnan(vals).any(): targets.append(a_ - float(np.sum(vals)))
        targets = [t for t in targets if t >= 0]
        if not targets: continue
        hitP = (not pd.isna(Pv)) and any(close(Pv, t) for t in targets); hitS = (not pd.isna(Sv)) and any(close(Sv, t) for t in targets)
        if hitP and not hitS: g.at[i, f"val_{v}"] = Pv; g.at[i, f"tier_{v}"] = 2; g.at[i, f"src_{v}"] = "P"; n += 1
        elif hitS and not hitP: g.at[i, f"val_{v}"] = Sv; g.at[i, f"tier_{v}"] = 2; g.at[i, f"src_{v}"] = "S"; n += 1
        elif pd.isna(Pv) and pd.isna(Sv) and len(targets) == 2 and close(targets[0], targets[1]):
            g.at[i, f"val_{v}"] = targets[0]; g.at[i, f"tier_{v}"] = 2; g.at[i, f"src_{v}"] = "I"; n += 1
    return n
for v in ("pop", "lit"):
    for it in range(4):
        n = identity_pass(g, v); P(f"identity arbitration, {v}, pass {it + 1}: {n} cells")
        if n == 0: break

# tier 3: adjacent cohorts
def adjacent_pass(g):
    g["rate"] = np.where((g.tier_pop > 0) & (g.tier_lit > 0) & (g.val_pop > 0), 100 * g.val_lit / g.val_pop, np.nan)
    rate = g.set_index(KEY + ["lo"]).rate.to_dict(); pop = g.set_index(KEY + ["lo"]).val_pop.to_dict()
    npop = nlit = 0
    for i, r in enumerate(g.itertuples(index=False)):
        k = (r.region, r.area, r.group, r.sex)
        if r.tier_pop == 0 and not pd.isna(r.P_pop) and not pd.isna(r.S_pop):
            nb = [pop.get(k + (r.lo - 5,), np.nan), pop.get(k + (r.lo + 5,), np.nan)]; nb = [x for x in nb if not pd.isna(x)]
            if len(nb) == 2 and np.mean(nb) > 0:
                m = np.mean(nb); inP = abs(r.P_pop - m) <= 0.4 * m; inS = abs(r.S_pop - m) <= 0.4 * m
                if inP != inS:
                    g.at[i, "val_pop"] = r.P_pop if inP else r.S_pop; g.at[i, "tier_pop"] = 3; g.at[i, "src_pop"] = "P" if inP else "S"; npop += 1
    g["rate"] = np.nan
    for i, r in enumerate(g.itertuples(index=False)):
        k = (r.region, r.area, r.group, r.sex)
        if r.tier_lit == 0 and r.tier_pop > 0 and r.val_pop > 0 and not pd.isna(r.P_lit) and not pd.isna(r.S_lit):
            nb = [rate.get(k + (r.lo - 5,), np.nan), rate.get(k + (r.lo + 5,), np.nan)]; nb = [x for x in nb if not pd.isna(x)]
            if len(nb) == 2:
                m = np.mean(nb); rP, rS = 100 * r.P_lit / r.val_pop, 100 * r.S_lit / r.val_pop
                inP = abs(rP - m) <= 15 and rP <= 100; inS = abs(rS - m) <= 15 and rS <= 100
                if inP != inS:
                    g.at[i, "val_lit"] = r.P_lit if inP else r.S_lit; g.at[i, "tier_lit"] = 3; g.at[i, "src_lit"] = "P" if inP else "S"; nlit += 1
    return npop, nlit
for it in range(3):
    a, b = adjacent_pass(g); P(f"adjacent-cohort arbitration, pass {it + 1}: population {a}, literates {b}")
    if a + b == 0: break
g = g.drop(columns=["rate"])
g["tier"] = np.where((g.tier_pop > 0) & (g.tier_lit > 0) & (g.val_lit <= g.val_pop), np.maximum(g.tier_pop, g.tier_lit), 0)
# neighbour rule: an error both in the subtotal and in the single years passes the identities.
# drop if literacy > 25 points from both neighbouring groups, or population > 3x or < 1/3 of both
def neighbour_rule(g):
    ok = g[g.tier > 0]; rate = (100 * ok.val_lit / ok.val_pop).where(ok.val_pop > 0)
    rd = dict(zip(zip(ok.region, ok.area, ok.group, ok.sex, ok.lo), rate)); pdict = dict(zip(zip(ok.region, ok.area, ok.group, ok.sex, ok.lo), ok.val_pop))
    bad = []
    for i, r in enumerate(g.itertuples(index=False)):
        if r.tier == 0 or r.lo > 75 or r.val_pop <= 0: continue
        k = (r.region, r.area, r.group, r.sex); a_, b_ = rd.get(k + (r.lo - 5,)), rd.get(k + (r.lo + 5,)); pa, pb = pdict.get(k + (r.lo - 5,)), pdict.get(k + (r.lo + 5,))
        rt = 100 * r.val_lit / r.val_pop
        if r.val_pop >= 100 and a_ is not None and b_ is not None and not pd.isna(a_) and not pd.isna(b_) and abs(rt - a_) > 25 and abs(rt - b_) > 25: bad.append(i); continue
        if pa is not None and pb is not None and pa > 0 and pb > 0 and (r.val_pop > 3 * max(pa, pb) or r.val_pop < min(pa, pb) / 3): bad.append(i)
    return bad
nbad = 0
for it in range(3):
    bad = neighbour_rule(g)
    if not bad: break
    nbad += len(bad); g.loc[g.index[bad], "tier"] = 0; g.loc[g.index[bad], "src_pop"] = "X"; g.loc[g.index[bad], "src_lit"] = "X"
P(f"five-year groups removed by the neighbour rule: {nbad}")
P(g[g.src_pop == "X"][KEY + ["g5", "val_pop", "val_lit"]].assign(rate=lambda t: (100 * t.val_lit / t.val_pop).round(1)).to_string())
g = g.merge(gt, on=["region", "group"], how="left")
P("\nFive-year groups, ages 5 and over:", len(g))
P(pd.crosstab(g.area, g.tier, normalize="index").round(3).to_string())
a1059 = g[(g.lo >= 10) & (g.lo <= 55)]
P("Ages 10-59:", len(a1059), "| tier shares:", a1059.tier.value_counts(normalize=True).sort_index().round(3).to_dict())
P(a1059[a1059.area == "rural"].groupby("region").apply(lambda x: pd.Series({"cells": len(x), "tier1": (x.tier == 1).mean(), "tier1-2": x.tier.isin([1, 2]).mean(), "tier1-3": (x.tier > 0).mean()})).round(3).sort_values("tier1-3").to_string())
g.to_csv(f"{D}/tableIX_five_year_groups_validated.csv", sep=";", index=False, encoding="utf-8-sig")

# ---------------- validated single years ----------------
okS = g[(g.tier > 0) & g.src_pop.isin(["PS", "S"]) & g.src_lit.isin(["PS", "S"])][KEY + ["g5", "tier"]].rename(columns={"tier": "tier5"})
sg = sg.merge(okS, on=KEY + ["g5"], how="left")
sg["valid"] = sg.tier5.notna() & sg.total.notna() & sg.literate.notna() & (sg.literate <= sg.total)
m = (sg.a >= 5) & (sg.a <= 59)
P("\nSingle-year cells, ages 5-59:", int(m.sum()), "valid share", round(sg[m].valid.mean(), 3))
sg[KEY + ["age", "a", "g5", "total", "literate", "quality", "valid", "tier5"]].to_csv(f"{D}/tableIX_single_years_validated.csv", sep=";", index=False, encoding="utf-8-sig")
G5 = g[g.tier > 0].set_index(KEY + ["g5"])[["val_pop", "val_lit", "tier"]]
SV = sg[sg.valid].set_index(KEY + ["a"])[["total", "literate", "tier5"]]
G5d = {k: tuple(v) for k, v in zip(G5.index, G5.values)}; SVd = {k: tuple(v) for k, v in zip(SV.index, SV.values)}
def from_g5(key, groups):
    vals = [G5d.get(key + (x,)) for x in groups]
    if any(v is None for v in vals): return None
    return float(sum(v[0] for v in vals)), float(sum(v[1] for v in vals)), int(max(v[2] for v in vals))
def from_single(key, ages):
    vals = [SVd.get(key + (x,)) for x in ages]
    if any(v is None for v in vals): return None
    return float(sum(v[0] for v in vals)), float(sum(v[1] for v in vals)), int(max(v[2] for v in vals))

BANDS = [("8-11", "s", list(range(8, 12))), ("12-14", "s", [12, 13, 14]), ("15-19", "g", ["15-19"]), ("20-24", "g", ["20-24"]), ("25-29", "g", ["25-29"]),
         ("30-39", "g", ["30-34", "35-39"]), ("40-49", "g", ["40-44", "45-49"]), ("50-59", "g", ["50-54", "55-59"]),
         ("60-69", "g", ["60-64", "65-69"])]
WID = {"8-11": 4, "12-14": 3, "15-19": 5, "20-24": 5, "25-29": 5, "30-39": 10, "40-49": 10, "50-59": 10, "60-69": 10}
BI = {b: i for i, (b, _, _) in enumerate(BANDS)}
rows = []
for key in ix[KEY].drop_duplicates().itertuples(index=False):
    key = tuple(key)
    for band, kind, comp in BANDS:
        v = from_single(key, comp) if kind == "s" else from_g5(key, comp)
        if v is None: continue
        rows.append(dict(region=key[0], area=key[1], group=key[2], sex=key[3], band=band, population=v[0], literate=v[1], tier=v[2]))
bp = pd.DataFrame(rows); bp["literacy"] = 100 * bp.literate / bp.population
P("\nBand cells before plausibility rules:", len(bp))
def plausibility(d, keys, bandcol, order, width, minlen=3, name=""):
    d = d.copy(); d["bi"] = d[bandcol].map(order); d["ppy"] = d.population / d[bandcol].map(width)
    d["ratio"] = d.ppy / d.groupby(keys).ppy.transform("median")
    bad1 = (d.ratio > 2.5) & (d.bi < max(order.values()))
    n1 = int(bad1.sum()); d = d[~bad1]; n2 = 0
    for _ in range(4):
        d = d.sort_values(keys + ["bi"]); gr = d.groupby(keys)
        pv, nx, pb, nb = gr.literacy.shift(1), gr.literacy.shift(-1), gr.bi.shift(1), gr.bi.shift(-1)
        adjp, adjn = (d.bi - pb) == 1, (nb - d.bi) == 1
        dp, dn = (d.literacy - pv).abs(), (d.literacy - nx).abs()
        interior = adjp & adjn & (dp > 30) & (dn > 30)
        if interior.any(): n2 += int(interior.sum()); d = d[~interior]; continue
        edge = (adjn & ~adjp & (dn > 30)) | (adjp & ~adjn & (dp > 30))
        if edge.any(): n2 += int(edge.sum()); d = d[~edge]; continue
        break
    n = d.groupby(keys)[bandcol].transform("size"); n3 = int((n < minlen).sum()); d = d[n >= minlen]
    P(f"plausibility {name}: population rule {n1}, 30-point rule {n2}, short series {n3}; kept {len(d)}")
    return d.drop(columns=["bi", "ppy", "ratio"])
bp = plausibility(bp, KEY, "band", BI, WID, name="(bands)")
# 60+: needs the four groups 60-79 validated and 60-69 kept by the rules above
have6069 = set(map(tuple, bp[bp.band == "60-69"][KEY].values))
rows = []
for key in have6069:
    v = from_g5(key, ["60-64", "65-69", "70-74", "75-79"])
    if v is None: continue
    extra = [G5d.get(key + (x,)) for x in ["80-84", "85-89", "90-94", "95-99"]]; extra = [e for e in extra if e is not None]
    pop = v[0] + sum(e[0] for e in extra); lit = v[1] + sum(e[1] for e in extra)
    rows.append(dict(region=key[0], area=key[1], group=key[2], sex=key[3], band="60+", population=pop, literate=lit, tier=v[2], literacy=100 * lit / pop))
bp = pd.concat([bp, pd.DataFrame(rows)], ignore_index=True)
bp = bp[bp.population >= 200].merge(gt, on=["region", "group"], how="left")
bp.to_csv(f"{D}/tableIX_bands_validated.csv", sep=";", index=False, encoding="utf-8-sig")
P("Validated band cells (population of 200 and more):", len(bp), "| units:", bp.region.nunique(), "| tiers:", bp.tier.value_counts().sort_index().to_dict())

# ---------------- korenizatsiya_panel.csv ----------------
TITULAR = {"Татары": "Татарская АССР", "Чуваши": "Чувашская АССР", "Марийцы": "Марийская АО", "Вотяки": "Вотская АО",
           "Башкиры": "Башкирская АССР", "Карелы, финны, вепсы": "Карельская АССР"}
kp = bp[bp.group_type != "all"].copy()
kp["population"] = kp.population.round().astype(int); kp["literate"] = kp.literate.round().astype(int); kp["literacy"] = kp.literacy.round(1)
kp["titular_unit"] = [int(TITULAR.get(gp) == rg) for gp, rg in zip(kp.group, kp.region)]; kp["has_unit_1926"] = kp.group.isin(TITULAR).astype(int)
old = pd.read_csv(f"{V1}/korenizatsiya_panel.csv", sep=";", encoding="utf-8-sig")
kp[list(old.columns) + ["tier"]].to_csv(f"{D}/korenizatsiya_panel.csv", sep=";", index=False, encoding="utf-8-sig")
P("\nkorenizatsiya_panel: old rows", len(old), "new rows", len(kp), "| rural old", int((old.area == "rural").sum()), "new", int((kp.area == "rural").sum()))
cmp = old.merge(kp, on=["region", "area", "group", "sex", "band"], how="outer", suffixes=("_old", "_new"), indicator=True)
P("   only in old:", int((cmp._merge == "left_only").sum()), "| only in new:", int((cmp._merge == "right_only").sum()), "| in both:", int((cmp._merge == "both").sum()))
both = cmp[cmp._merge == "both"]; dif = (both.literacy_old - both.literacy_new).abs()
P("   in both: literacy differs by more than 1 point in", int((dif > 1).sum()), "cells; by more than 5 in", int((dif > 5).sum()))
core = ["12-14", "15-19", "20-24", "25-29", "30-39", "40-49"]
o_ = old[(old.area == "rural") & old.band.isin(core) & (old.group != "Прочие") & old.literacy.between(0, 100)]; n_ = kp[(kp.area == "rural") & kp.band.isin(core) & (kp.group != "Прочие")]
P("   decomposition sample (rural, six cohorts, without 'other'): old", len(o_), "new", len(n_), "| units old", o_.region.nunique(), "new", n_.region.nunique(), "| strict (tier 1-2):", int(n_.tier.isin([1, 2]).sum()))

# ---------------- russians_by_region.csv ----------------
rr = bp[bp.group_type.isin(["russian", "all"])].copy()
w = rr.pivot_table(index=["region", "area", "group_type", "band"], columns="sex", values=["population", "literacy", "tier"]).reset_index()
w.columns = ["region", "area", "group", "band", "lit_F", "lit_M", "pop_F", "pop_M", "tier_F", "tier_M"]
w = w.dropna(subset=["lit_F", "lit_M"]); w = w[(w.pop_M >= 300) & (w.pop_F >= 300)].copy()
w["tier"] = w[["tier_F", "tier_M"]].max(axis=1).astype(int)
w["gender_gap"] = (w.lit_M - w.lit_F).round(1); w["lit_M"] = w.lit_M.round(1); w["lit_F"] = w.lit_F.round(1)
w["pop_M"] = w.pop_M.round().astype(int); w["pop_F"] = w.pop_F.round().astype(int)
old = pd.read_csv(f"{V1}/russians_by_region.csv", sep=";", encoding="utf-8-sig")
w[list(old.columns) + ["tier"]].to_csv(f"{D}/russians_by_region.csv", sep=";", index=False, encoding="utf-8-sig")
P("\nrussians_by_region: old rows", len(old), "new rows", len(w))

# ---------------- mechanism panel ----------------
# measures that use population counts only (fertility, sex ratio, urban shares) require the population count to be validated, not the literate count
G5pop = g[g.tier_pop > 0].set_index(KEY + ["g5"]).val_pop.to_dict()
def g5sum(key, groups):
    vals = [G5pop.get(key + (x,)) for x in groups]
    return np.nan if any(v is None or pd.isna(v) for v in vals) else float(sum(vals))
k04 = ix[ix.age == "0-4"].set_index(KEY).total
s04 = ix[ix.age.isin(["0", "1", "2", "3", "4"])].groupby(KEY).total.agg(lambda x: x.sum() if x.notna().sum() == 5 else np.nan)
kids = pd.concat([k04.rename("P"), s04.rename("S")], axis=1)
kids["v"] = [p if (not pd.isna(p) and not pd.isna(s) and close(p, s)) else np.nan for p, s in zip(kids.P, kids.S)]
kd = kids.v.to_dict()
G1549 = ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"]; G2039 = ["20-24", "25-29", "30-34", "35-39"]; G549 = [f"{a}-{a + 4}" for a in range(5, 50, 5)]
rows = []
for (reg, grp), s in ix[ix.group_type != "all"].groupby(["region", "group"]):
    areas = set(s.area)
    if "rural" not in areas and "total" not in areas: continue
    base = "rural" if "rural" in areas else "total"
    kM, kF = kd.get((reg, base, grp, "M"), np.nan), kd.get((reg, base, grp, "F"), np.nan)
    women = g5sum((reg, base, grp, "F"), G1549); m2039 = g5sum((reg, base, grp, "M"), G2039); f2039 = g5sum((reg, base, grp, "F"), G2039)
    pop = np.nansum([g5sum((reg, base, grp, sx), G549) for sx in ("M", "F")])
    raw_pop = s[(s.area == base) & s.age.str.fullmatch(r"\d+-\d+")].total.sum()
    d = dict(region=reg, group=grp, area=base, pop=pop if pop > 0 else raw_pop,
             cwr=100 * (kM + kF) / women if women and not np.isnan(women) else np.nan,
             sr_20_39=100 * m2039 / f2039 if f2039 and not np.isnan(f2039) else np.nan,
             csr_0_4=100 * kM / kF if kF and not np.isnan(kF) else np.nan)
    if "rural" in areas and "total" in areas:
        for sx in ("M", "F"):
            t = g5sum((reg, "total", grp, sx), G2039); r_ = g5sum((reg, "rural", grp, sx), G2039)
            us = 100 * (t - r_) / t if t and not np.isnan(t) and not np.isnan(r_) else np.nan
            d[f"urban_share_{sx}"] = us if (not np.isnan(us) and 0 <= us <= 100) else np.nan
    sub = bp[(bp.region == reg) & (bp.group == grp) & (bp.area == base)]
    for band in ("12-14", "20-24", "30-39"):
        for sx in ("M", "F"):
            vv = sub[(sub.band == band) & (sub.sex == sx)].literacy
            d[f"lit_{sx}_{band}"] = float(vv.iloc[0]) if len(vv) else np.nan
        d[f"gendergap_{band}"] = d[f"lit_M_{band}"] - d[f"lit_F_{band}"]
    rows.append(d)
mp = pd.DataFrame(rows)
rus = mp[mp.group == "Русские"].set_index("region")
for band in ("12-14", "20-24"):
    for sx in ("M", "F"):
        mp[f"ethgap_{sx}_{band}"] = [rus[f"lit_{sx}_{band}"].get(rg, np.nan) - v for rg, v in zip(mp.region, mp[f"lit_{sx}_{band}"])]
mp["mobility_gap"] = mp.urban_share_M - mp.urban_share_F
mp = mp[mp["pop"] > 5000]
mp.to_csv(f"{D}/mechanism_panel.csv", sep=";", index=False, encoding="utf-8-sig"); mp.to_csv(f"{D}/mechanism_panel_clean.csv", sep=";", index=False, encoding="utf-8-sig")
oldm = pd.read_csv(f"{V1}/mechanism_panel_clean.csv", sep=";", encoding="utf-8-sig")
P("\nmechanism_panel: old rows", len(oldm), "new rows", len(mp), "| rural non-Russian cells with gaps and urban shares: old",
  int(((oldm.area == "rural") & (oldm.group != "Русские") & oldm["ethgap_F_20-24"].notna() & oldm.mobility_gap.notna() & oldm.cwr.notna()).sum()),
  "new", int(((mp.area == "rural") & (mp.group != "Русские") & mp["ethgap_F_20-24"].notna() & mp.mobility_gap.notna() & mp.cwr.notna()).sum()))

# ---------------- russians_region_baseline.csv ----------------
# needs baseline_pre1917_by_province.csv from baseline_1897.py (Malein's data, see README)
if not os.path.exists(f"{D}/baseline_pre1917_by_province.csv"):
    P("\nrussians_region_baseline: data/baseline_pre1917_by_province.csv not found, skipped (run scripts/baseline_1897.py first)")
else:
    r = w[w.group == "russian"]; pref = r[r.area == "rural"]; have = set(pref.region)
    r = pd.concat([pref, r[(r.area == "total") & (~r.region.isin(have))]])
    wb = r.pivot_table(index="region", columns="band", values=["lit_M", "lit_F", "gender_gap"]); wb.columns = [f"{a}_{b}" for a, b in wb.columns]; wb = wb.reset_index()
    wb = wb.merge(ix[["region", "pre1917_province"]].drop_duplicates(), on="region", how="left")
    prov = pd.read_csv(f"{D}/baseline_pre1917_by_province.csv", sep=";", encoding="utf-8-sig")
    BV = ["share_lit", "per_lit_f", "share_serfs", "share_old_beleivers1867", "enrollment_rate_1911", "school_density_1911", "teachers_percap_1911", "exp_zemstvo_edu_pc_1894", "lingfrac_1897", "agshare_1897", "zemstvo_prov"]
    def base(pp):
        ps = [p.strip() for p in str(pp).split(";")]; s = prov[prov.province_rus.isin(ps)]
        return s[BV].mean() if len(s) else pd.Series({c: np.nan for c in BV})
    wb = pd.concat([wb, wb["pre1917_province"].apply(base)], axis=1)
    wb["lit_m_1897"] = 200 * wb.share_lit - wb.per_lit_f; wb["gendergap_1897"] = wb.lit_m_1897 - wb.per_lit_f
    wb = wb.merge(mp[mp.group == "Русские"][["region", "cwr", "sr_20_39", "urban_share_M", "urban_share_F", "csr_0_4"]], on="region", how="left")
    # columns in the v1 order, 60-69 and csr_0_4 added later
    lit = [c for c in wb.columns if c.startswith(("gender_gap_", "lit_F_", "lit_M_")) and not c.endswith("_60-69")]
    cols = ["region"] + lit + ["pre1917_province"] + BV + ["lit_m_1897", "gendergap_1897", "cwr", "sr_20_39", "urban_share_M", "urban_share_F"] + [c for c in wb.columns if c.endswith("_60-69")] + ["csr_0_4"]
    wb[cols].to_csv(f"{D}/russians_region_baseline.csv", sep=";", index=False, encoding="utf-8-sig")
    P("\nrussians_region_baseline: units", len(wb))
    if os.path.exists(f"{V1}/russians_region_baseline.csv"):
        oldb = pd.read_csv(f"{V1}/russians_region_baseline.csv", sep=";", encoding="utf-8-sig"); cmpb = oldb.merge(wb, on="region", suffixes=("_old", "_new"))
        for c in ("gender_gap_20-24", "gender_gap_12-14", "gender_gap_40-49", "lit_F_40-49", "lit_F_60+", "cwr", "urban_share_M"):
            dd = (cmpb[c + "_old"] - cmpb[c + "_new"]).abs()
            P(f"   {c:18s} n old {int(cmpb[c + '_old'].notna().sum())}, n new {int(cmpb[c + '_new'].notna().sum())}, changed by more than 1: {int((dd > 1).sum())}, largest change {dd.max():.1f}")

# ---------------- tableIX_cohort_gaps.csv (six titular units, whole unit) ----------------
oldg = pd.read_csv(f"{V1}/tableIX_cohort_gaps.csv", sep=";", encoding="utf-8-sig")
rows = []
for grp, unit in TITULAR.items():
    for band in ["8-14", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60+"]:
        d = dict(region=unit, band=band)
        for sx in ("M", "F"):
            if band == "8-14":
                def s814(gname):
                    v_ = from_single((unit, "total", gname, sx), list(range(8, 15)))
                    return pd.DataFrame([dict(literacy=100 * v_[1] / v_[0], population=v_[0])]) if v_ is not None else pd.DataFrame(columns=["literacy", "population"])
                t, r_ = s814(grp), s814("Русские")
            else:
                t = bp[(bp.region == unit) & (bp.area == "total") & (bp.group == grp) & (bp.band == band) & (bp.sex == sx)]
                r_ = bp[(bp.region == unit) & (bp.area == "total") & (bp.group == "Русские") & (bp.band == band) & (bp.sex == sx)]
            d[f"titular_{sx}"] = float(t.literacy.iloc[0]) if len(t) else np.nan; d[f"russian_{sx}"] = float(r_.literacy.iloc[0]) if len(r_) else np.nan
            d[f"gap_{sx}"] = d[f"russian_{sx}"] - d[f"titular_{sx}"]
            d[f"n_titular_{sx}"] = float(t.population.iloc[0]) if len(t) else np.nan; d[f"n_russian_{sx}"] = float(r_.population.iloc[0]) if len(r_) else np.nan
        rows.append(d)
cg = pd.DataFrame(rows)[list(oldg.columns)]
cg.to_csv(f"{D}/tableIX_cohort_gaps.csv", sep=";", index=False, encoding="utf-8-sig")
P("\ncohort gaps (six titular units): old rows", len(oldg), "old bands", sorted(oldg.band.unique()), "| new rows with both gaps", int(cg.dropna(subset=["gap_M", "gap_F"]).shape[0]))

# ---------------- linked cohorts 1926 -> 1939 ----------------
c39 = pd.read_csv(f"{D}/census1939_literacy_by_region_age_sex.csv", sep=";", encoding="utf-8-sig")
oldl = pd.read_csv(f"{V1}/linked_cohorts_1926_1939.csv", sep=";", encoding="utf-8-sig")
pairs = oldl[["unit_1926", "region_1939"]].drop_duplicates()
PAIRS = [(list(range(8, 13)), "20-24"), (list(range(13, 18)), "25-29"), (list(range(18, 23)), "30-34"), (list(range(23, 28)), "35-39"),
         (list(range(28, 33)), "40-44"), (list(range(33, 38)), "45-49"), (list(range(38, 43)), "50-54"), (list(range(43, 48)), "55-59"),
         (list(range(48, 53)), "60-64"), (list(range(53, 58)), "65-69")]   # last two above the age limit (placebo)
rows = []
for u26, r39 in pairs.itertuples(index=False):
    for area in ("total", "rural"):
        s39 = c39[(c39.region_1939 == r39) & (c39.area == area)]
        if s39.empty: continue
        for sx in ("M", "F"):
            for ages, b39 in PAIRS:
                v = from_single((u26, area, ALL, sx), ages); b = s39[(s39.sex == sx) & (s39.age == b39)]
                if v is None or b.empty: continue
                p26, l26, tr = v; p39, l39 = b.population.iloc[0], b.literate.iloc[0]
                if p26 < 500 or p39 < 500: continue
                rows.append(dict(unit_1926=u26, region_1939=r39, area=area, sex=sx, age_1926=f"{ages[0]}-{ages[-1]}", age_1939=b39, born=f"{1926 - ages[-1]}-{1926 - ages[0]}",
                                 pop_1926=int(p26), pop_1939=int(p39), lit_1926=round(100 * l26 / p26, 1), lit_1939=round(100 * l39 / p39, 1),
                                 gain_pp=round(100 * l39 / p39 - 100 * l26 / p26, 1), survival=round(p39 / p26, 2), tier=tr))
lc = pd.DataFrame(rows)
lc[list(oldl.columns) + ["tier"]].to_csv(f"{D}/linked_cohorts_1926_1939.csv", sep=";", index=False, encoding="utf-8-sig")
P("\nlinked cohorts: old rows", len(oldl), "new rows", len(lc), "| units old", oldl.unit_1926.nunique(), "new", lc.unit_1926.nunique())
cm = oldl.merge(lc, on=["unit_1926", "area", "sex", "age_1926"], how="outer", suffixes=("_old", "_new"), indicator=True)
P("   only old:", int((cm._merge == "left_only").sum()), "only new:", int((cm._merge == "right_only").sum()), "both:", int((cm._merge == "both").sum()))
b_ = cm[cm._merge == "both"]; dd = (b_.gain_pp_old - b_.gain_pp_new).abs(); P("   in both: gain differs by more than 0.5 in", int((dd > 0.5).sum()))
rur = cm[(cm.area == "rural") & cm.age_1926.isin(["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48-52", "53-57"])]
P("   rural adult cells: old", int(rur.gain_pp_old.notna().sum()), "new", int(rur.gain_pp_new.notna().sum()))
P(rur.groupby("unit_1926").agg(old=("gain_pp_old", "count"), new=("gain_pp_new", "count")).to_string())
lost = rur[rur.gain_pp_new.isna() & rur.gain_pp_old.notna()]
P("   dropped rural adult cells, old values:\n" + lost[["unit_1926", "sex", "age_1926", "pop_1926_old", "lit_1926_old", "gain_pp_old", "survival_old"]].to_string(index=False))
open(f"{R}/V_validation_1926.txt", "w", encoding="utf-8").write("\n".join(LOG))

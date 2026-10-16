"""Figures of the paper -> figures/fig*.pdf, .png (data/ and results/ from paper_numbers.py).
No titles inside the figures, captions are in the tex."""
import os, sys, json, warnings, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.collections import PatchCollection
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{ROOT}/data"; R = f"{ROOT}/results"; F = f"{ROOT}/figures"; os.makedirs(F, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from names import en
J = json.load(open(f"{R}/paper_numbers.json", encoding="utf-8")); NUM = {k: v[0] for k, v in J["NUM"].items()}; STR = J["STR"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 110})
CM, CF, CG, CP, CGR = "#1f4e79", "#c0392b", "#7f8c8d", "#8e44ad", "#27ae60"
def save(fig, name):
    fig.savefig(f"{F}/{name}.png", dpi=300, bbox_inches="tight"); fig.savefig(f"{F}/{name}.pdf", bbox_inches="tight"); plt.close(fig); print("saved", name)
def csv(name): return pd.read_csv(f"{R}/{name}", sep=";", encoding="utf-8-sig")
def place_labels(ax, xs, ys, labels, fontsize=6, sizes=None, show=None):
    # labels without overlap: 8 directions x growing distances, keep the cheapest. sizes = marker areas (pt^2). call after the axis limits are set
    fig = ax.figure; fig.canvas.draw(); rend = fig.canvas.get_renderer(); xs, ys = np.asarray(xs, float), np.asarray(ys, float); n = len(xs)
    rad = np.sqrt(np.full(n, 30.0) if sizes is None else np.asarray(sizes, float)) / 2; px_ = fig.dpi / 72.0
    pts = ax.transData.transform(np.column_stack([xs, ys])); box = ax.get_window_extent(rend); placed = []
    dirs = [(1, 0.8, "left", "bottom"), (1, -0.8, "left", "top"), (-1, 0.8, "right", "bottom"), (-1, -0.8, "right", "top"), (0, 1.3, "center", "bottom"), (0, -1.3, "center", "top"), (1.3, 0, "left", "center"), (-1.3, 0, "right", "center")]
    def draw(i, k, ux, uy, ha, va):
        dist = rad[i] + 1.5 if k == 1 else rad[i] + 2.2 * k
        return ax.annotate(labels[i], (xs[i], ys[i]), xytext=(ux * dist, uy * dist), textcoords="offset points", fontsize=fontsize, ha=ha, va=va,
                           arrowprops=dict(arrowstyle="-", lw=0.3, color="grey", shrinkA=0, shrinkB=rad[i]) if k > 1 else None)
    for i in range(n):
        if show is not None and not np.asarray(show)[i]: continue
        best = None
        for rank, k in enumerate((1, 3.2, 5, 7, 9.5, 12)):
            for ux, uy, ha, va in dirs:
                t = draw(i, k, ux, uy, ha, va); bb = t.get_window_extent(rend).expanded(1.03, 1.12); t.remove()
                outside = not (bb.x0 >= box.x0 - 2 and bb.x1 <= box.x1 + 2 and bb.y0 >= box.y0 and bb.y1 <= box.y1 + 2)
                hits = sum(bb.overlaps(p) for p in placed); r_ = 0.6 * rad * px_
                cover = sum(bb.x0 - r_[j] < pts[j, 0] < bb.x1 + r_[j] and bb.y0 - r_[j] < pts[j, 1] < bb.y1 + r_[j] for j in range(n) if j != i)
                cost = 1000 * outside + 10 * hits + 3 * cover + 0.5 * rank
                if best is None or cost < best[0]: best = (cost, k, ux, uy, ha, va, bb)
                if cost == 0: break
            if best[0] == 0: break
        draw(i, *best[1:6]); placed.append(best[6])
ADULT = ["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48-52", "53-57"]
ORD1 = ["33-37", "38-42", "43-47", "48-52", "53-57", "58-62", "63-67"]
CB = ["40-49", "30-39", "25-29", "20-24", "15-19", "12-14"]

# ---------- Figure: design ----------
fig, ax = plt.subplots(figsize=(9.2, 4.3)); ax.set_xlim(1838, 1945); ax.set_ylim(-0.6, 5.9)
bars = [("Household regime: placebo cohorts (aged 53-67 at the decree)", 1853, 1867, CG), ("Household regime: cohorts aged 33-52 at the decree", 1868, 1887, CM),
        ("State regime: placebo cohorts (aged 48-57 in 1926)", 1869, 1878, CG), ("State regime: cohorts aged 33-47 in 1926", 1879, 1893, CF), ("State regime: cohorts aged 18-32 in 1926", 1894, 1908, CF),
        ("Schooled under Soviet rule (aged 12-19 in 1926)", 1907, 1914, CGR)]
for y_, lab in zip([1897, 1926, 1939], ["Census\n1897", "Census\n1926", "Census\n1939"]):
    ax.plot([y_, y_], [-0.6, 5.4], color="k", lw=1); ax.text(y_, 5.68, lab, ha="center", va="center", fontsize=8, fontweight="bold")
ax.plot([1919.98, 1919.98], [-0.6, 5.4], color=CF, ls="--", lw=1.1); ax.text(1919.4, -0.35, "decree of\nDec. 1919", fontsize=7.5, color=CF, ha="right", va="center")
ax.add_patch(Rectangle((1928, -0.6), 4, 6.0, color=CF, alpha=0.08, lw=0)); ax.text(1930, 2.4, "cultural campaign, 1928-1932", fontsize=7.5, ha="center", va="center", color=CF, rotation=90)
for i, (lab, b0, b1, c) in enumerate(bars):
    ax.add_patch(Rectangle((b0, i - 0.3), b1 - b0 + 1, 0.6, color=c, alpha=0.4 if c != CG else 0.5)); ax.text(b0 - 1, i, lab, ha="right", va="center", fontsize=8, bbox=dict(fc="white", ec="none", pad=1.2))
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_xlabel("Year of birth of the cohort (bars); census and campaign dates (lines)"); ax.set_xticks(range(1850, 1945, 10))
save(fig, "fig01_design")

# ---------- Figure: age profile 1926 ----------
bv = pd.read_csv(f"{D}/tableIX_bands_validated.csv", sep=";", encoding="utf-8-sig"); bv = bv[bv.region != "Уральская обл."]
ball = bv[(bv.group_type == "all") & (bv.area == "rural")]
PB = ["8-11", "12-14", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69"]
pr = ball[ball.band.isin(PB)].groupby(["band", "sex"])[["population", "literate"]].sum(); pr["lit"] = 100 * pr.literate / pr.population; pr = pr.lit.unstack().reindex(PB)
fig, ax = plt.subplots(figsize=(7.5, 4.2)); x = np.arange(len(PB))
ax.plot(x, pr.M, "-o", color=CM, label="Men"); ax.plot(x, pr.F, "-s", color=CF, label="Women"); ax.fill_between(x, pr.F, pr.M, color=CG, alpha=0.15, label="Gender gap")
ax.set_xticks(x); ax.set_xticklabels(PB); ax.set_ylabel("Literate, %"); ax.set_xlabel("Age in December 1926"); ax.set_ylim(0, 100)
ax.axvspan(-0.5, 2.5, color=CGR, alpha=0.08); ax.text(1.0, 95, "schooled under\nSoviet rule", ha="center", va="top", fontsize=8, color=CGR)
ax.axvspan(4.5, 7.5, color=CF, alpha=0.05); ax.text(6.0, 95, "adults at the decree of 1919", ha="center", va="top", fontsize=8, color=CF); ax.legend(loc="lower left", frameon=False)
save(fig, "fig02_age_profile_1926")

# ---------- Figure: map ----------
base = f"{ROOT}/external/malein"   # replication/data of ICPSR 231104, see README
if os.path.exists(f"{base}/shape_files/districts_europe_collapsed.shp") and os.path.exists(f"{D}/crosswalk_1897_districts_to_1926_units.csv"):
    import shapefile
    sf = shapefile.Reader(base + "/shape_files/districts_europe_collapsed.shp")
    pan = pd.read_stata(base + "/panel1879_1911.dta", convert_categoricals=False)[["Id", "province_rus", "district"]].drop_duplicates("Id"); id2prov = dict(zip(pan.Id, pan.province_rus)); id2dist = dict(zip(pan.Id, pan.district))
    rk = pd.read_csv(f"{D}/region_keys.csv", sep=";", encoding="utf-8-sig"); cw = pd.read_csv(f"{D}/crosswalk_1897_districts_to_1926_units.csv", sep=";", encoding="utf-8-sig"); code2name = dict(zip(rk.region_code, rk.region_1926))
    val = ball[ball.band == "20-24"].pivot_table(index="region", columns="sex", values="literacy"); val["gap"] = val.M - val.F
    ixk = pd.read_csv(f"{D}/census1926_tableIX_long.csv", sep=";", encoding="utf-8-sig", usecols=["region", "pre1917_province"]).drop_duplicates(); prov2units = {}
    for _, r in ixk.iterrows():
        for p in str(r.pre1917_province).split(";"):
            p = p.strip().lower()
            if p and p != "nan": prov2units.setdefault(p, []).append(r.region)
    dist2unit = {(r.province_rus, r.district): code2name.get(r.region_code) for _, r in cw.iterrows() if r.fraction >= 0.5}
    def unit_value(rec, col):
        prov = id2prov.get(rec["Id"])
        if prov is None: return np.nan
        unit = dist2unit.get((prov, id2dist.get(rec["Id"])))
        if unit is None:
            units = [u_ for u_ in prov2units.get(prov, []) if u_ in val.index and not np.isnan(val.loc[u_, col])]
            return val.loc[units, col].mean() if units else np.nan
        return val.loc[unit, col] if unit in val.index else np.nan
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2))
    for ax, col, ttl, cmap, vmin, vmax in [(axes[0], "F", "(a) Literacy of rural women aged 20-24, per cent", "YlOrRd", 20, 80), (axes[1], "gap", "(b) Rural gender gap at ages 20-24, points", "PuBu", 5, 50)]:
        patches, colors, grey = [], [], []
        for shp, rec in zip(sf.shapes(), sf.records()):
            v = unit_value(rec.as_dict(), col); pts = np.array(shp.points); parts = list(shp.parts) + [len(pts)]
            for k in range(len(parts) - 1):
                poly = Polygon(pts[parts[k]:parts[k + 1]], closed=True)
                if np.isnan(v): grey.append(poly)
                else: patches.append(poly); colors.append(v)
        pc = PatchCollection(patches, cmap=cmap, edgecolor="white", linewidths=0.2); pc.set_array(np.array(colors)); pc.set_clim(vmin, vmax); ax.add_collection(pc)
        ax.add_collection(PatchCollection(grey, facecolor="#e6e6e6", edgecolor="white", linewidths=0.2)); ax.set_xlim(22, 68); ax.set_ylim(43, 68); ax.set_aspect(1.6); ax.axis("off"); ax.set_title(ttl, fontsize=10, loc="left")
        plt.colorbar(pc, ax=ax, shrink=0.55, pad=0.01)
    fig.tight_layout(); save(fig, "fig22_map_1926")
else:
    print("map skipped: no external/malein or crosswalk file")

# ---------- Figure: event studies ----------
def evplot(ax, key, bins, ref, xlabel, ylabel, title):
    x = np.arange(len(bins))
    for sx, col, mk, lab, off in (("m", CM, "o", "Men", -0.08), ("f", CF, "s", "Women", 0.08)):
        v = [NUM[f"{key}.{sx}.{b}"] for b in bins]; s = [NUM[f"{key}.{sx}.{b}.se"] for b in bins]
        ax.errorbar(x + off, v, yerr=1.96 * np.array(s), fmt=mk + "-", color=col, capsize=3, label=lab)
    ax.axhline(0, color="k", lw=0.6); ax.axvspan(len(bins) - 0.5, len(bins) + 0.5, color="grey", alpha=0.15)
    ax.set_xticks(list(x) + [len(bins)]); ax.set_xticklabels(list(bins) + [ref + "\n(ref.)"], fontsize=8); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title, fontsize=9, loc="left"); ax.legend(frameon=False)
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
evplot(axes[0], "w1", ORD1[:-1], "63-67", "Age at the decree of December 1919", "Gain 1897-1926 relative to the reference cohort, pp", f"(a) Household regime: rural, {STR['w1.regions']} regions")
axes[0].axvline(3.5, color="grey", ls=":", lw=1); axes[0].text(3.55, axes[0].get_ylim()[1] * 0.93, "above the age limit\nof the decree", fontsize=7, color="grey", va="top")
evplot(axes[1], "w2", ADULT[:-1], "53-57", "Age in December 1926", "Gain 1926-1939 relative to the reference cohort, pp", f"(b) State regime: rural, {STR['w2.units']} units")
axes[1].axvline(5.5, color="grey", ls=":", lw=1); axes[1].text(5.55, axes[1].get_ylim()[1] * 0.93, "above the age limit\nof the campaign", fontsize=7, color="grey", va="top")
fig.tight_layout(); save(fig, "fig19_event_studies")

# ---------- Figure: the illiterate who became literate ----------
if "w2c.M.18-22" in NUM:
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.3), sharey=True)
    for ax, key, bins, xl, ttl, cut in [(axes[0], "w1c", ORD1, "Age at the decree of December 1919", "(a) Household regime, 1897 to 1926", 3.5), (axes[1], "w2c", ADULT, "Age in December 1926", "(b) State regime, 1926 to 1939", 5.5)]:
        x = np.arange(len(bins))
        for sx, col, mk, lab, off in (("M", CM, "o", "Men", -0.06), ("F", CF, "s", "Women", 0.06)):
            v = np.array([NUM[f"{key}.{sx}.{b}"] for b in bins]); s = np.array([NUM[f"{key}.{sx}.{b}.se"] for b in bins]); ax.errorbar(x + off, v, yerr=1.96 * s, fmt=mk + "-", color=col, capsize=3, label=lab)
        ax.axhline(0, color="k", lw=0.6); ax.axvspan(cut, len(bins) - 0.5, color="grey", alpha=0.12); ax.set_xticks(x); ax.set_xticklabels(bins, fontsize=8); ax.set_xlabel(xl); ax.set_title(ttl, fontsize=9, loc="left")
        ax.text((cut + len(bins) - 0.5) / 2, 70, "above the\nage limit", ha="center", va="top", fontsize=7.5, color="grey")
    axes[0].set_ylabel("Illiterate at the earlier census who were\nliterate at the later one, %"); axes[0].legend(frameon=False, loc="upper center"); fig.tight_layout(); save(fig, "fig24_taught")

# ---------- Figure: Russians across units ----------
rb = csv("F_russians_units.csv"); rb2 = rb.dropna(subset=["gender_gap_20-24"]).copy()
fig, axes = plt.subplots(1, 3, figsize=(12.5, 5.2), gridspec_kw={"width_ratios": [1.25, 1, 1]})
ax = axes[0]; d = rb2.sort_values("gender_gap_20-24")
ax.barh(np.arange(len(d)), d["gender_gap_20-24"], color=[CF if ("АССР" in r or "АО" in r) else CM for r in d.region], alpha=0.8)
ax.set_yticks(np.arange(len(d))); ax.set_yticklabels([en(r) for r in d.region], fontsize=6.3); ax.set_xlabel("Male minus female literacy, pp"); ax.set_ylim(-0.7, len(d) - 0.3)
ax.set_title("(a) Gender gap by unit (red: Russians in titular units)", fontsize=9, loc="left")
d = rb2.dropna(subset=["teachers_percap_1911", "lit_F_20-24", "lit_M_20-24"]); ax = axes[1]
for yc, col, mk, lab in (("lit_M_20-24", CM, "o", "Men"), ("lit_F_20-24", CF, "s", "Women")):
    ax.scatter(d.teachers_percap_1911, d[yc], s=22, color=col, marker=mk, alpha=0.75, label=lab); b = np.polyfit(d.teachers_percap_1911, d[yc], 1); xs = np.linspace(d.teachers_percap_1911.min(), d.teachers_percap_1911.max(), 20); ax.plot(xs, np.polyval(b, xs), color=col, lw=1.2)
ax.set_xlabel("Teachers per 1,000 population, 1911"); ax.set_ylabel("Literate, %"); ax.legend(frameon=False, fontsize=8, loc="lower right"); ax.set_title("(b) School supply and literacy", fontsize=9, loc="left")
d = rb2.dropna(subset=["cwr", "lit_F_20-24", "lit_M_20-24"]); ax = axes[2]
for yc, col, mk, lab in (("lit_M_20-24", CM, "o", "Men"), ("lit_F_20-24", CF, "s", "Women")):
    ax.scatter(d.cwr, d[yc], s=22, color=col, marker=mk, alpha=0.75, label=lab); b = np.polyfit(d.cwr, d[yc], 1); xs = np.linspace(d.cwr.min(), d.cwr.max(), 20); ax.plot(xs, np.polyval(b, xs), color=col, lw=1.2)
ax.set_xlabel("Children under 5 per 100 women aged 15-49"); ax.set_ylabel("Literate, %"); ax.set_title("(c) Fertility and literacy", fontsize=9, loc="left")
fig.tight_layout(); save(fig, "fig11_russians_across_regions")

# ---------- Figure: decomposition ----------
x = np.arange(6); g = lambda k: np.array([NUM[f"dec.{k}.{b}"] for b in CB]); s = lambda k: np.array([NUM[f"dec.{k}.{b}.se"] for b in CB])
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
ax = axes[0]; ax.errorbar(x - 0.07, g("v"), yerr=1.96 * s("v"), fmt="-o", color=CM, capsize=3, label="Volga men against Russian men"); ax.errorbar(x + 0.07, g("vw"), yerr=1.96 * s("vw"), fmt="-s", color=CF, capsize=3, label="Volga women against Russian women")
ax.set_xticks(x); ax.set_xticklabels(CB); ax.set_xlabel("Age in 1926 (older to younger)"); ax.set_ylabel("Difference from Russians, pp"); ax.axhline(0, color="k", lw=0.6); ax.set_ylim(-41, 3); ax.legend(frameon=False, loc="lower left", fontsize=8); ax.set_title("(a) The ethnic gap by sex", fontsize=9, loc="left")
ax = axes[1]; ax.errorbar(x - 0.07, g("vf"), yerr=1.96 * s("vf"), fmt="-s", color=CF, capsize=3, label="Volga nationality x female"); ax.errorbar(x + 0.07, g("mf"), yerr=1.96 * s("mf"), fmt="-^", color=CP, capsize=3, label="Muslim nationality x female")
ax.set_xticks(x); ax.set_xticklabels(CB); ax.set_xlabel("Age in 1926 (older to younger)"); ax.set_ylabel("Interaction coefficient, pp"); ax.axhline(0, color="k", lw=0.6); ax.legend(frameon=False, fontsize=8); ax.set_title("(b) The additional difference for women", fontsize=9, loc="left")
fig.tight_layout(); save(fig, "fig10_decomposition")

# ---------- Figure: six titular units ----------
cg = pd.read_csv(f"{D}/tableIX_cohort_gaps.csv", sep=";", encoding="utf-8-sig"); bands6 = ["8-14", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60+"]
regs = ["Чувашская АССР", "Татарская АССР", "Башкирская АССР", "Марийская АО", "Вотская АО", "Карельская АССР"]
fig, axes = plt.subplots(2, 3, figsize=(11, 6.2), sharey=True)
for ax, rg in zip(axes.flat, regs):
    d = cg[cg.region == rg].set_index("band").reindex(bands6); x = np.arange(len(bands6))
    ax.plot(x, d.gap_M, "-o", color=CM, label="Men"); ax.plot(x, d.gap_F, "-s", color=CF, label="Women"); ax.axhline(0, color="k", lw=0.6); ax.set_xticks(x); ax.set_xticklabels(bands6, fontsize=7, rotation=45); ax.set_title(en(rg), fontsize=9); ax.axvspan(-0.5, 1.5, color=CGR, alpha=0.1)
axes[0, 0].legend(frameon=False, fontsize=8); axes[0, 0].set_ylabel("Russian minus titular literacy, pp"); axes[1, 0].set_ylabel("Russian minus titular literacy, pp")
for ax in axes[1]: ax.set_xlabel("Age in 1926")
fig.tight_layout(); save(fig, "fig09_ethnic_gaps_six_republics")

# ---------- Figure: differences between nationalities ----------
gm = csv("G_mechanism_cells.csv"); fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
gm = gm.sort_values("pop", ascending=False).reset_index(drop=True)
for ax, xcol, xl, ttl in [(axes[0], "urban_share_M_diff", "Urban share of men, difference from Russians, pp", "(a) Access to towns"), (axes[1], "cwr_diff", "Child-woman ratio, difference from Russians", "(b) Fertility")]:
    ax.scatter(gm[xcol], gm["ethgap_F_20-24"], c=[CP if m_ else CF for m_ in gm.muslim], s=gm["pop"] / gm["pop"].max() * 260 + 12, alpha=0.7)
    xs = np.linspace(gm[xcol].quantile(0.0), gm[xcol].quantile(0.97), 10)
    b = np.polyfit(gm[xcol], gm["ethgap_F_20-24"], 1, w=np.sqrt(gm["pop"])); ax.plot(xs, np.polyval(b, xs), color="k", lw=1, label="Weighted by population")
    b = np.polyfit(gm[xcol], gm["ethgap_F_20-24"], 1); ax.plot(xs, np.polyval(b, xs), color="k", lw=1, ls="--", label="Unweighted")
    ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5); ax.set_xlabel(xl); ax.set_title(ttl, fontsize=9, loc="left")
axes[0].set_ylabel("Female ethnic literacy gap, aged 20-24, pp"); axes[1].legend(frameon=False, fontsize=8, loc="lower right"); fig.tight_layout()
for ax, xcol in [(axes[0], "urban_share_M_diff"), (axes[1], "cwr_diff")]: place_labels(ax, gm[xcol], gm["ethgap_F_20-24"], [f"{en(r.group)}, {en(r.region)}" for _, r in gm.iterrows()], fontsize=5.6, sizes=gm["pop"] / gm["pop"].max() * 260 + 12)
save(fig, "fig14_mechanisms")

# ---------- Figure: state regime, cohort means and gender gap ----------
cl = csv("W2_cells.csv"); fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3)); ax = axes[0]
for sx, col, mk, lab in [("M", CM, "o", "Men"), ("F", CF, "s", "Women")]:
    gq = cl[cl.sex == sx].groupby("age_1926").apply(lambda t: pd.Series({"m": np.average(t.gain_pp, weights=t.pop_1926), "se": t.gain_pp.std() / np.sqrt(len(t))})).reindex(ADULT)
    ax.errorbar(np.arange(8), gq.m, yerr=1.96 * gq.se, fmt="-" + mk, color=col, label=lab, capsize=3)
ax.axvspan(5.5, 7.5, color="grey", alpha=0.12); ax.text(6.5, ax.get_ylim()[1] * 0.95, "above the\nage limit", ha="center", va="top", fontsize=7.5, color="grey")
ax.set_xticks(range(8)); ax.set_xticklabels(ADULT, fontsize=8); ax.set_xlabel("Age in 1926"); ax.set_ylabel("Change in literacy 1926-1939, pp"); ax.axhline(0, color="k", lw=0.6); ax.set_title("(a) Gains of the same cohorts, weighted means", fontsize=9, loc="left"); ax.legend(frameon=False, loc="upper center")
ax = axes[1]; y = np.arange(8); g26 = np.array([NUM[f"w2.gap26.{c}"] for c in ADULT]); g39 = np.array([NUM[f"w2.gap39.{c}"] for c in ADULT])
ax.hlines(y, g39, g26, color=CG, lw=2); ax.scatter(g26, y, color="k", zorder=3, label="1926"); ax.scatter(g39, y, color=CF, zorder=3, label="1939")
for i in range(8):
    if abs(g26[i] - g39[i]) >= 1.5: ax.text((g39[i] + g26[i]) / 2, i - 0.2, f"{g39[i] - g26[i]:+.0f}", ha="center", va="bottom", fontsize=8, color=CF)
ax.set_yticks(y); ax.set_yticklabels(ADULT); ax.set_ylabel("Age in 1926"); ax.set_xlabel("Male minus female literacy of the same cohort, pp"); ax.invert_yaxis(); ax.set_title("(b) Gender gap within cohorts", fontsize=9, loc="left"); ax.legend(frameon=False, loc="lower left")
fig.tight_layout(); save(fig, "fig04_wave2_linked_cohorts")

# ---------- Figure: age gradient ----------
fig, ax = plt.subplots(figsize=(7.6, 4.3)); rng = np.random.default_rng(2)
for sx, col, mk, lab in [("M", CM, "o", "Men"), ("F", CF, "s", "Women")]:
    d = cl[cl.sex == sx]; xa = d.age_1926.map({c: int(c[:2]) + 3.5 for c in ADULT})
    ax.scatter(xa + rng.normal(0, 0.45, len(d)), d.gain_pp, s=d.pop_1926 / cl.pop_1926.max() * 110 + 6, color=col, marker=mk, alpha=0.35, edgecolor="none")
    gq = d.groupby(xa).apply(lambda t: np.average(t.gain_pp, weights=t.pop_1926)); ax.plot(gq.index, gq.values, "-", color=col, lw=2.2, label=lab)
ax.axvline(50, color="grey", ls=":", lw=1); ax.text(50.4, ax.get_ylim()[1] * 0.95, "age limit of\nthe campaign", fontsize=7.5, color="grey", va="top")
ax.axhline(0, color="k", lw=0.6); ax.set_xlabel("Age in 1928"); ax.set_ylabel("Change in literacy 1926-1939, pp"); ax.legend(frameon=False, loc="upper center"); save(fig, "fig05_dose_response_wave2")

# ---------- Figure: two regimes, triple-difference coefficients ----------
PK = [("t", "Teachers per capita, 1911"), ("c", "Child-woman ratio, 1926"), ("u", "Urban share of men, 1926"), ("a", "Agrarian share, 1897")]
fig, ax = plt.subplots(figsize=(8.2, 4.2)); y = np.arange(len(PK))[::-1]
for j, (key, col, mk, lab) in enumerate([("tr.{}.1", CG, "o", "Household regime (levels of 1926: cohort 40-49 against 60-69)"), ("tr.{}.2", CF, "s", "State regime (gains 1926-39: cohort 18-32 against 48-57)"), ("trb.{}.2", "#e59866", "^", "State regime (gains 1926-39: cohort 18-32 against 33-47)")]):
    v = np.array([NUM[key.format(p)] for p, _ in PK]); se = np.array([NUM[key.format(p) + ".se"] for p, _ in PK])
    ax.errorbar(v, y + (1 - j) * 0.22, xerr=1.96 * se, fmt=mk, color=col, capsize=3, label=lab)
ax.axvline(0, color="k", lw=0.6); ax.set_yticks(y); ax.set_yticklabels([l_ for _, l_ in PK]); ax.set_xlabel("Triple-difference coefficient, pp per standard deviation of the predictor"); ax.set_ylim(-0.6, len(PK) - 0.4)
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.45, 1.24), ncol=1, fontsize=8); fig.tight_layout(); save(fig, "fig20_ddd_two_regimes")

# ---------- Figure: two regimes, unit level scatter ----------
c1 = csv("C_wave1_proxy_units.csv"); w2 = csv("B7_unit_level_wave2.csv").merge(rb[["region", "teachers_percap_1911"]], left_on="unit_1926", right_on="region", how="left")
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4)); lab6 = []
for ax, d, yv, ttl in [(axes[0], c1, "w1_F", "(a) Household regime: literacy of women aged 40-49\nminus that of women aged 60-69, Russians, 1926"), (axes[1], w2, "gain_F", "(b) State regime: gain 1926-1939 of women\naged 23-32 in 1926")]:
    d = d.dropna(subset=["teachers_percap_1911", yv]).reset_index(drop=True); ax.scatter(d.teachers_percap_1911, d[yv], color=CF, s=38, alpha=0.7); lab6.append((ax, d.teachers_percap_1911, d[yv], [en(r) for r in d.region]))
    b = np.polyfit(d.teachers_percap_1911, d[yv], 1); xs = np.linspace(d.teachers_percap_1911.min(), d.teachers_percap_1911.max(), 10); ax.plot(xs, np.polyval(b, xs), color="k", lw=1.3)
    ax.set_title(ttl + f" (n = {len(d)})", fontsize=8.5, loc="left"); ax.set_xlabel("Teachers per 1,000 population, 1911"); ax.set_ylabel("Percentage points")
fig.tight_layout()
for a_ in lab6: place_labels(*a_, fontsize=5.8, sizes=np.full(len(a_[1]), 38.0))
save(fig, "fig06_two_regimes")

# ---------- Figure: convergence ----------
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.4)); d = csv("B7_unit_level_wave2.csv")
for ax, sx, col in [(axes[0], "M", CM), (axes[1], "F", CF)]:
    lit, gain = d[f"lit26_{sx}"], d[f"gain_{sx}"]; t0 = d.titular == 0
    ax.scatter(lit[t0], gain[t0], color=col, s=d["pop"][t0] / d["pop"].max() * 250 + 15, alpha=0.55, label="Russian gubernii and okrugi")
    ax.scatter(lit[~t0], gain[~t0], color=col, s=d["pop"][~t0] / d["pop"].max() * 250 + 15, alpha=0.9, marker="D", edgecolor="k", label="Titular republics and oblasts")
    b = np.polyfit(lit, gain, 1, w=np.sqrt(d["pop"])); xs = np.linspace(lit.min(), lit.max(), 10); ax.plot(xs, np.polyval(b, xs), color="k", lw=1.1, ls="--")
    ax.set_xlabel(f"Literacy in 1926, % ({'men' if sx == 'M' else 'women'} aged 23-32)"); ax.set_ylabel("Gain 1926-1939, pp"); ax.set_title(f"({'a' if sx == 'M' else 'b'}) {'Men' if sx == 'M' else 'Women'}", fontsize=9, loc="left")
lg = axes[0].legend(frameon=False, fontsize=8, loc="upper right")
for h_ in lg.legend_handles: h_.set_sizes([40])
fig.tight_layout()
for ax, sx in [(axes[0], "M"), (axes[1], "F")]: place_labels(ax, d[f"lit26_{sx}"], d[f"gain_{sx}"], [en(r) for r in d.unit_1926], fontsize=6, sizes=d["pop"] / d["pop"].max() * 250 + 15)
save(fig, "fig08_convergence_titular")

# ---------- Figure: inference for the state regime ----------
if os.path.exists(f"{R}/B5_permutation_female_x_young.txt") and "w2.perm" in STR:
    loo = csv("B4_leave_one_out.csv"); perm = np.loadtxt(f"{R}/B5_permutation_female_x_young.txt"); obs = NUM["w2.ddd"]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.9)); ax = axes[0]; ax.hist(perm, bins=40, color=CG, alpha=0.7); ax.axvline(obs, color=CF, lw=2, label=f"observed ({obs:.1f})")
    ax.set_xlabel("Coefficient under random assignment of sex within unit and cohort"); ax.set_ylabel("Draws"); ax.legend(frameon=False); ax.set_title(f"(a) Permutation distribution, p {STR['w2.perm'] if STR['w2.perm'].startswith('<') else '= ' + STR['w2.perm']}", fontsize=9, loc="left")
    ax = axes[1]; d = loo.sort_values("coef_female_x_young"); ax.scatter(d.coef_female_x_young, np.arange(len(d)), color=CF, s=25); ax.set_yticks(np.arange(len(d))); ax.set_yticklabels([en(r) for r in d.dropped_unit], fontsize=6.5)
    ax.set_xlabel("Coefficient when the unit is excluded"); ax.set_title("(b) Leave-one-unit-out", fontsize=9, loc="left"); ax.axvline(obs, color="k", lw=0.6, ls="--"); fig.tight_layout(); save(fig, "fig13_inference")

# ---------- Figure: rayon-level replication ----------
ry = csv("B9_rayon_cells.csv"); AD2 = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54"]
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.7), gridspec_kw={"width_ratios": [1, 1.25]}); ax = axes[0]
for sx, col, mk, lab in [("M", CM, "o", "Men"), ("F", CF, "s", "Women")]:
    gq = ry[ry.sex == sx].groupby("age_1926").apply(lambda t: pd.Series({"m": np.average(t.gain_pp, weights=t.pop_1926), "se": t.gain_pp.std() / np.sqrt(len(t))})).reindex(AD2)
    ax.errorbar(np.arange(7), gq.m, yerr=1.96 * gq.se, fmt="-" + mk, color=col, label=lab, capsize=3)
ax.axvspan(5.5, 6.5, color="grey", alpha=0.12); ax.set_xticks(range(7)); ax.set_xticklabels(AD2, fontsize=8); ax.set_xlabel("Age in 1926"); ax.set_ylabel("Change in literacy 1926-1939, pp"); ax.axhline(0, color="k", lw=0.6); ax.set_title(f"(a) {ry.rayon.nunique()} regions covering the RSFSR, rural", fontsize=9, loc="left"); ax.legend(frameon=False)
ax = axes[1]; w_ = ry[(ry.sex == "F") & ry.age_1926.isin(["25-29", "30-34"])].groupby("rayon").agg(gain=("gain_pp", "mean")).reset_index().merge(ry[(ry.sex == "M") & ry.age_1926.isin(["25-29", "30-34"])].groupby("rayon").agg(gainM=("gain_pp", "mean")).reset_index(), on="rayon").sort_values("gain")
y = np.arange(len(w_)); ax.barh(y - 0.2, w_.gain, 0.4, color=CF, label="Women"); ax.barh(y + 0.2, w_.gainM, 0.4, color=CM, label="Men"); ax.set_yticks(y); ax.set_yticklabels([en(r) for r in w_.rayon], fontsize=7)
ax.set_xlabel("Gain 1926-1939, pp (aged 25-34 in 1926)"); ax.legend(frameon=False, loc="lower right"); ax.set_title("(b) By region", fontsize=9, loc="left"); fig.tight_layout(); save(fig, "fig16_wave2_rayons")

# ---------- Figure: 2010, ethnic gap by sex and cohort ----------
J1 = csv("J1_ethnic_gap_2010_by_sex_age.csv"); AGES = ["20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70 и более"]
fig, axes = plt.subplots(2, 3, figsize=(11, 6.4), sharey=True)
for ax, nat in zip(axes.flat, ["Татары", "Башкиры", "Чуваши", "Марийцы", "Удмурты", "Мордва"]):
    gq = J1[J1.nat == nat]
    for sx, col, mk, lab in [("M", CM, "o", "Men"), ("F", CF, "s", "Women")]:
        s_ = gq[gq.sex == sx].set_index("age").reindex(AGES); ax.plot(range(len(AGES)), s_.gap_sec, "-" + mk, color=col, label=lab, ms=4)
    ax.axhline(0, color="k", lw=0.6); ax.set_title(en(nat), fontsize=9); ax.set_xticks(range(len(AGES))); ax.set_xticklabels([a_.replace(" и более", "+") for a_ in AGES], fontsize=6.5, rotation=60)
axes[0, 0].legend(frameon=False, fontsize=8); axes[0, 0].set_ylabel("Russians minus nationality, pp"); axes[1, 0].set_ylabel("Russians minus nationality, pp")
for ax in axes[1]: ax.set_xlabel("Age in 2010")
fig.tight_layout(); save(fig, "fig17_ethnic_gap_2010_by_cohort")

# ---------- Figure: 2010 gap against the 1926 gaps ----------
J2 = csv("J2_ethnic_gaps_1926_2010.csv"); d = J2[J2.area == "total"].sort_values("stated", ascending=False).reset_index(drop=True); fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharey=True)
for ax, xv_, xl, ttl in [(axes[0], "gF", "Female ethnic literacy gap, 1926, pp", "(a) Female gap of 1926"), (axes[1], "gM", "Male ethnic literacy gap, 1926, pp", "(b) Male gap of 1926")]:
    for m_, col, lab in [(0, CF, "Other nationalities"), (1, CP, "Muslim nationalities")]:
        q = d[d.muslim == m_]; ax.scatter(q[xv_], q.g10, s=np.sqrt(q.stated) / 8 + 8, color=col, alpha=0.7, label=lab)
    b = np.polyfit(d[xv_], d.g10, 1, w=np.sqrt(d.stated)); xs = np.linspace(d[xv_].min(), d[xv_].max(), 10); ax.plot(xs, np.polyval(b, xs), color="k", lw=1.2); ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5); ax.set_xlabel(xl); ax.set_title(ttl, fontsize=9, loc="left")
axes[0].set_ylabel("Ethnic gap in secondary education, 2010, pp"); lg = axes[1].legend(frameon=False, fontsize=8, loc="lower left")
for h_ in lg.legend_handles: h_.set_sizes([35])
fig.tight_layout()
for ax, xv_ in [(axes[0], "gF"), (axes[1], "gM")]:
    place_labels(ax, d[xv_], d.g10, [f"{en(r.nat2010)}, {en(r.subject)}" for _, r in d.iterrows()], fontsize=5.4, sizes=np.sqrt(d.stated) / 8 + 8, show=(d.titular == 1) | (d.g10.abs() > 9) | (d[xv_] < -5) | (d[xv_] > 38))
save(fig, "fig18_gap2010_vs_gap1926")

# ---------- Figure: sex difference of 1926 and of 2010 ----------
e = pd.read_csv(f"{R}/S_legacy_sexdiff_nationalities.csv", sep=";", encoding="utf-8-sig", index_col=0); SIX = ["Татары", "Башкиры", "Чуваши", "Марийцы", "Удмурты", "Мордва"]
fig, axes = plt.subplots(1, 3, figsize=(12, 4.1), sharey=True)
for ax, grp, ttl in zip(axes, ["old", "mid", "young"], ["(a) Born before 1951", "(b) Born 1951 to 1960", "(c) Born after 1960"]):
    six = e.index.isin(SIX); ax.scatter(e.D_ad[six], e[grp][six], s=45, color=CF, alpha=0.85, label="Six Volga-Ural nationalities"); ax.scatter(e.D_ad[~six], e[grp][~six], s=25, color=CG, alpha=0.85, label="Other nationalities")
    b = np.polyfit(e.D_ad, e[grp], 1); xs = np.linspace(e.D_ad.min(), e.D_ad.max(), 10); ax.plot(xs, np.polyval(b, xs), color="k", lw=1.1, label="Fit, twelve nationalities")
    e6 = e.loc[SIX]; b6 = np.polyfit(e6.D_ad, e6[grp], 1); xs6 = np.linspace(e6.D_ad.min(), e6.D_ad.max(), 10); ax.plot(xs6, np.polyval(b6, xs6), color=CF, lw=1.1, ls="--", label="Fit, six nationalities")
    ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5); ax.set_title(ttl, fontsize=9, loc="left"); ax.set_xlabel("Female minus male ethnic literacy gap, 1926, pp")
axes[0].set_ylabel("Female minus male ethnic education gap, 2010, pp"); axes[0].legend(frameon=False, fontsize=7, loc="upper left"); fig.tight_layout()
for ax, grp in zip(axes, ["old", "mid", "young"]): place_labels(ax, e.D_ad, e[grp], [en(n_) for n_ in e.index], fontsize=6.5, sizes=np.where(e.index.isin(SIX), 45.0, 25.0))
save(fig, "fig23_legacy_sex_difference")

# ---------- Figure: robustness of the legacy estimates ----------
SPEC = [("leg", "Baseline, subject fixed effects"), ("leg.kal", "Excluding Kalmyks"), ("leg.ugk", "Excluding Ukrainians, Germans, Kazakhs"), ("leg.six", "Six Volga-Ural nationalities"), ("leg.unw", "Unweighted"), ("leg.h", "Higher education"),
        ("leg.adj", "Age-standardised gap"), ("leg.rur", "Controlling for rural share"), ("leg.nm", "Non-Muslim nationalities"), ("leg.mt", "With Muslim and titular indicators")]
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharey=True)
for ax, sfx, ttl in [(axes[0], "", "(a) Whole population"), (axes[1], ".r", "(b) Rural population")]:
    y = np.arange(len(SPEC)); bF = np.array([NUM[k + sfx + ".F"] for k, _ in SPEC]); sF = np.array([NUM[k + sfx + ".F.se"] for k, _ in SPEC]); bM = np.array([NUM[k + sfx + ".M"] for k, _ in SPEC]); sM = np.array([NUM[k + sfx + ".M.se"] for k, _ in SPEC])
    ax.errorbar(bF, y - 0.15, xerr=1.96 * sF, fmt="o", color=CF, capsize=3, label="Female gap of 1926"); ax.errorbar(bM, y + 0.15, xerr=1.96 * sM, fmt="s", color=CM, capsize=3, label="Male gap of 1926")
    ax.axvline(0, color="k", lw=0.6); ax.set_yticks(y); ax.set_yticklabels([l_ for _, l_ in SPEC], fontsize=8); ax.set_title(ttl, fontsize=9, loc="left"); ax.set_xlabel("Points of the 2010 gap per point of the 1926 gap")
axes[0].set_ylim(len(SPEC) - 0.4, -0.6); fig.legend(*axes[0].get_legend_handles_labels(), frameon=False, fontsize=8, loc="upper center", ncol=2, bbox_to_anchor=(0.6, 1.04)); fig.tight_layout(); save(fig, "fig21_legacy_robustness")

# ---------- Figure: heatmap of women's literacy ----------
hm = ball[ball.sex == "F"].pivot_table(index="region", columns="band", values="literacy").reindex(columns=PB); hm = hm[hm[["15-19", "20-24", "25-29", "30-39"]].notna().all(axis=1)].sort_values("20-24")
fig, ax = plt.subplots(figsize=(8, 9.4)); im = ax.imshow(np.ma.masked_invalid(hm.values), aspect="auto", cmap="YlOrRd", vmin=0, vmax=80)
ax.set_xticks(range(len(PB))); ax.set_xticklabels(PB); ax.set_yticks(range(len(hm))); ax.set_yticklabels([en(r) for r in hm.index], fontsize=7)
for i in range(len(hm)):
    for j in range(len(PB)):
        v = hm.values[i, j]
        if not np.isnan(v): ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=6, color="white" if v > 50 else "black")
plt.colorbar(im, ax=ax, label="Literate women, %"); ax.set_xlabel("Age in 1926"); save(fig, "fig12_heatmap_women_1926")

# ---------- Figure: the main picture, literacy by year of birth as recorded by four censuses ----------
INK, G97, GRID = "#2b2b2b", "#8a9399", "#e6e6e6"
CENSUS_T = {1897: 1897.11, 1926: 1926.96, 1939: 1939.05, 1959: 1959.04}
CPB = {1897: [f"{a}-{a + 4}" for a in range(15, 65, 5)], 1926: [f"{a}-{a + 4}" for a in range(20, 75, 5)], 1939: [f"{a}-{a + 4}" for a in range(30, 70, 5)], 1959: [f"{a}-{a + 4}" for a in range(50, 70, 5)]}
def cohort_profile(ax, tag, sx, col, ymax, notes=True, legend=True):
    def series(yr):
        xs = np.array([CENSUS_T[yr] - (int(b.split("-")[0]) + 2.5) for b in CPB[yr]]); ys = np.array([NUM[f"cp{tag}.{sx}.{yr}.{b}"] for b in CPB[yr]]); o = np.argsort(xs); return xs[o], ys[o]
    (x97, y97), (x26, y26), (x39, y39), (x59, y59) = series(1897), series(1926), series(1939), series(1959)
    ax.axvspan(CENSUS_T[1926] - 35, CENSUS_T[1926] - 20, color="#000000", alpha=0.045, lw=0)
    xx = np.linspace(max(x26.min(), x39.min()), min(x26.max(), x39.max()), 300); ax.fill_between(xx, np.interp(xx, x26, y26), np.interp(xx, x39, y39), color=col, alpha=0.12, lw=0)
    ax.plot(x97, y97, "-", color=G97, lw=2, marker="s", ms=5.5, mec="white", mew=1.2, label="Census of 1897", solid_capstyle="round", zorder=3)
    ax.plot(x26, y26, "-", color=INK, lw=2, marker="o", ms=6, mec="white", mew=1.2, label="Census of 1926", solid_capstyle="round", zorder=4)
    ax.plot(x39, y39, "-", color=col, lw=2, marker="o", ms=6, mec="white", mew=1.2, label="Census of 1939", solid_capstyle="round", zorder=5)
    ax.plot(x59, y59, linestyle="none", marker="D", ms=6.5, mfc="white", mec=col, mew=1.8, label="Census of 1959", zorder=6)
    ax.set_xlim(1830, 1910); ax.set_ylim(0, ymax); ax.set_xticks(range(1830, 1911, 10)); ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s_ in ("left", "bottom"): ax.spines[s_].set_color("#9a9a9a")
    ax.tick_params(colors="#444444"); ax.set_xlabel("Year of birth"); top = ax.secondary_xaxis("top", functions=(lambda v: CENSUS_T[1926] - v, lambda a_: CENSUS_T[1926] - a_))
    top.set_xticks(range(20, 91, 10)); top.set_xlabel("Age at the census of December 1926", labelpad=6); top.tick_params(colors="#444444"); top.spines["top"].set_color("#9a9a9a")
    if legend: ax.legend(frameon=False, loc="upper left", fontsize=9, handlelength=2.2, borderaxespad=0.6)
    if notes:
        xm = 1902.0; ym = (np.interp(xm, x26, y26) + np.interp(xm, x39, y39)) / 2
        ax.annotate("learned to read as adults\nbetween 1926 and 1939", (xm, ym), xytext=(1872.0, ym + 0.15 * ymax), fontsize=9, color="#222222", ha="center", va="center", arrowprops=dict(arrowstyle="-", lw=0.7, color="#666666", shrinkA=2, shrinkB=1))
        xo = 1859.0; ax.annotate("the censuses of 1897 and 1926 agree:\nno adult learning in thirty years", (xo, np.interp(xo, x26, y26) + 0.012 * ymax), xytext=(1848.5, 0.30 * ymax), fontsize=9, color="#222222", ha="center", va="center", arrowprops=dict(arrowstyle="-", lw=0.7, color="#666666", shrinkA=2, shrinkB=1))
        ax.text(CENSUS_T[1926] - 27.5, 0.022 * ymax, "aged 20 to 34\nin 1926", fontsize=8, color="#555555", ha="center", va="bottom")
if "cpr.F.1926.20-24" in NUM:
    fig, ax = plt.subplots(figsize=(7.4, 4.8)); cohort_profile(ax, "r", "F", CF, 80); ax.set_ylabel("Women who can read, per cent"); fig.tight_layout(); save(fig, "fig25_main_cohorts")
    fig, axes = plt.subplots(2, 2, figsize=(11.6, 9.0))
    for ax, tag, sx, col, ym, ttl in ((axes[0, 0], "r", "F", CF, 90, "(a) Women, rural population"), (axes[0, 1], "t", "F", CF, 90, "(b) Women, whole population"), (axes[1, 0], "r", "M", CM, 100, "(c) Men, rural population"), (axes[1, 1], "t", "M", CM, 100, "(d) Men, whole population")):
        cohort_profile(ax, tag, sx, col, ym, notes=False, legend=(ax is axes[0, 0])); ax.set_title(ttl, fontsize=9.5, loc="left", pad=34); ax.set_ylabel("Literate, per cent")
    fig.tight_layout(); save(fig, "fig26_cohorts_all")

# ---------- Figure: the share of the illiterate taught before and during the campaign, by age at the earlier census ----------
if "w2c.M.18-22" in NUM:
    A97 = [f"{int(b[:2]) - 23}-{int(b[3:]) - 23}" for b in ORD1]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)
    for ax, key, bins, labs, xl, ttl, cut in [(axes[0], "w1c", ORD1, A97, "Age at the census of February 1897", "(a) Before the campaign, 1897 to 1926", None), (axes[1], "w2c", ADULT, ADULT, "Age at the census of December 1926", "(b) The campaign, 1926 to 1939", 5.5)]:
        x = np.arange(len(bins))
        for sx, col, mk, lab, off in (("M", CM, "o", "Men", -0.06), ("F", CF, "s", "Women", 0.06)):
            v = np.array([NUM[f"{key}.{sx}.{b}"] for b in bins]); s = np.array([NUM[f"{key}.{sx}.{b}.se"] for b in bins]); ax.errorbar(x + off, v, yerr=1.96 * s, fmt=mk + "-", color=col, lw=2, ms=6.5, mec="white", mew=1.2, capsize=3, elinewidth=1.2, label=lab)
        ax.axhline(0, color="#444444", lw=0.7); ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=8.5); ax.set_xlabel(xl); ax.set_title(ttl, fontsize=9.5, loc="left")
        if cut is not None:
            ax.axvspan(cut, len(bins) - 0.5, color="#000000", alpha=0.06, lw=0); ax.text((cut + len(bins) - 0.5) / 2, 72, "above the\nage limit", ha="center", va="top", fontsize=8, color="#555555")
    axes[0].set_ylabel("Illiterate at the earlier census who\ncould read at the later one, per cent"); axes[0].legend(frameon=False, loc="upper right"); fig.tight_layout(); save(fig, "fig27_taught_periods")

# ---------- Figure: the cohort of the campaign in every region ----------
if os.path.exists(f"{R}/S1_region_gains.csv"):
    rg = csv("S1_region_gains.csv"); f_ = rg[rg.sex == "F"].sort_values("l26").reset_index(drop=True); m_ = rg[rg.sex == "M"].set_index("rayon").reindex(f_.rayon).reset_index()
    fig, ax = plt.subplots(figsize=(7.4, 5.2)); y = np.arange(len(f_))
    ax.hlines(y, f_.l26, f_.l39, color=CF, lw=2, alpha=0.35, zorder=2); ax.plot(f_.l26, y, "o", color=G97, ms=7, mec="white", mew=1.2, label="Women, census of 1926", zorder=3); ax.plot(f_.l39, y, "o", color=CF, ms=7, mec="white", mew=1.2, label="Women, census of 1939", zorder=4)
    ax.plot(m_.l39, y, linestyle="none", marker="|", ms=9, mew=1.8, color=CM, label="Men, census of 1939", zorder=3)
    ax.set_yticks(y); ax.set_yticklabels([r_ + ("*" if a_ else "") for r_, a_ in zip(f_.region_en, f_.approx_borders)], fontsize=8.5); ax.set_xlim(0, 100); ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s_ in ("left", "bottom"): ax.spines[s_].set_color("#9a9a9a")
    ax.tick_params(colors="#444444"); ax.set_xlabel("Literate, per cent (rural cohort aged 20 to 34 in 1926)"); ax.legend(frameon=False, loc="upper left", fontsize=9); fig.tight_layout(); save(fig, "fig28_regions")
print("all figures written to", F)

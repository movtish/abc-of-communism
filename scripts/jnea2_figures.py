"""Figures of the ZhNEA article on the short-run aggregate results of the literacy campaign. Grey scale and serif type, as in the journal;
deliberately different in form from the figures of the English paper. Writes jnea/figures/rj*.pdf and .png. Run after paper_numbers.py."""
import os, sys, json, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = f"{ROOT}/results"; F = f"{ROOT}/jnea/figures"
os.makedirs(F, exist_ok=True)
NUM = {k: v[0] for k, v in json.load(open(f"{R}/paper_numbers.json", encoding="utf-8"))["NUM"].items()}
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#333333", "hatch.linewidth": 0.6})
DK, MD, LT, GRID = "#3a3a3a", "#8c8c8c", "#cfcfcf", "#e4e4e4"
def save(fig, name):
    fig.savefig(f"{F}/{name}.png", dpi=300, bbox_inches="tight"); fig.savefig(f"{F}/{name}.pdf", bbox_inches="tight"); plt.close(fig); print("saved", name)
def ru(v, d=1): return f"{v:.{d}f}".replace(".", ",").replace("-", "\u2212")

# Рис. 1. Составляющие прироста грамотности населения 20-49 лет
fig, ax = plt.subplots(figsize=(7.2, 2.9)); rows = [("T", "Оба пола"), ("M", "Мужчины"), ("F", "Женщины")]; y = np.arange(len(rows))[::-1]
for yy, (sx, lab) in zip(y, rows):
    ab, c = NUM[f"jl.dec.{sx}.ab"], NUM[f"jl.dec.{sx}.c"]
    ax.barh(yy, ab, 0.5, color=LT, edgecolor=DK, lw=0.6, label="смена поколений и школа" if sx == "T" else None)
    ax.barh(yy, c, 0.5, left=ab, color=MD, edgecolor=DK, lw=0.6, hatch="///", label="обучение взрослых" if sx == "T" else None)
    ax.text(ab + c + 0.6, yy, f"{ru(ab + c)} п.п.", va="center", fontsize=10)
ax.set_yticks(y); ax.set_yticklabels([r[1] for r in rows]); ax.set_xlim(0, 40); ax.set_xlabel("Прирост доли грамотных между переписями 1926 и 1939 гг., п.п.")
ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True); ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=10); save(fig, "rj1_sostav")

# Рис. 2. Число научившихся читать по возрасту в 1926 г.
c0 = pd.read_csv(f"{R}/J0_cohorts_1926_1939.csv", sep=";", encoding="utf-8-sig"); c0 = c0[c0.sex == "T"].reset_index(drop=True)
fig, ax = plt.subplots(figsize=(7.2, 3.6)); x = np.arange(len(c0))
cols = [LT if a in ("8-12", "13-17") else (MD if a != "53-57" else "white") for a in c0.age26]; hat = ["" if a in ("8-12", "13-17") else ("///" if a != "53-57" else "...") for a in c0.age26]
for xi, v, cl, h in zip(x, c0.new / 1e3, cols, hat): ax.bar(xi, v, 0.66, color=cl, edgecolor=DK, lw=0.6, hatch=h)
lab = [f"{a}\n({1926 - int(a.split('-')[1])}-{str(1926 - int(a.split('-')[0]))[2:]})" for a in c0.age26]
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=9); ax.set_xlabel("Возраст в 1926 г. (годы рождения)"); ax.set_ylabel("Тыс. человек")
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=LT, edgecolor=DK, lw=0.6, label="дети и подростки"), Patch(facecolor=MD, edgecolor=DK, lw=0.6, hatch="///", label="взрослые"), Patch(facecolor="white", edgecolor=DK, lw=0.6, hatch="...", label="старше предельного возраста кампании")], frameon=False, fontsize=9.5, loc="upper right")
save(fig, "rj2_vozrast")

# Рис. 3. Прирост грамотности поколения 20-34 лет по регионам и исходный уровень
yj = pd.read_csv(f"{R}/J1_regions.csv", sep=";", encoding="utf-8-sig")
SHORT = {"Башкирская АССР": "Башкирская", "Бурято-Монгольская АССР": "Бурят-Монгольская", "Вятский район": "Вятский", "Дагестанская АССР": "Дагестанская", "Дальне-Восточный край": "Дальневосточный",
         "Западный район": "Западный", "Крымская АССР": "Крымская", "Ленинградско-Карельский район": "Ленинградско-Карельский", "Нижне-Волжский район": "Нижне-Волжский", "Северный район": "Северный",
         "Северо-Кавказский край": "Северо-Кавказский", "Сибирский край": "Сибирский", "Средне-Волжский район": "Средне-Волжский", "Уральская область": "Уральская", "Центрально-Промышленный район": "Центрально-Промышленный",
         "Центрально-Черноземный район": "Центрально-Черноземный", "Якутская АССР": "Якутская"}
fig, ax = plt.subplots(figsize=(7.2, 4.6))
for ap, mk, fc in ((0, "o", DK), (1, "o", "white")):
    s = yj[yj.approx == ap]; ax.scatter(s.l26, s.gain, s=34, marker=mk, facecolor=fc, edgecolor=DK, lw=0.9, zorder=3, label="границы не менялись" if ap == 0 else "границы изменились")
b, a = np.polyfit(yj.l26, yj.gain, 1); xx = np.linspace(10, 90, 50); ax.plot(xx, a + b * xx, color=MD, lw=1.2, zorder=2)
# labels only for the regions away from the central cluster, with offsets chosen by hand
LAB = {"Якутская АССР": (6, 0, "left"), "Дагестанская АССР": (6, -4, "left"), "Бурято-Монгольская АССР": (6, 2, "left"), "Башкирская АССР": (6, 2, "left"), "Сибирский край": (-6, -9, "right"),
       "Центрально-Промышленный район": (-10, -18, "center"), "Ленинградско-Карельский район": (6, -32, "right"), "Северный район": (-8, 0, "right"), "Крымская АССР": (-4, 22, "center")}
for _, q in yj.iterrows():
    if q.rayon in LAB:
        dx, dy, ha = LAB[q.rayon]; far = abs(dy) > 12
        ax.annotate(SHORT[q.rayon], (q.l26, q.gain), xytext=(dx, dy), textcoords="offset points", fontsize=8.5, ha=ha, va="center", color="#333333",
                    arrowprops=dict(arrowstyle="-", lw=0.5, color="#777777", shrinkA=1, shrinkB=4) if far else None)
ax.set_xlim(10, 92); ax.set_ylim(0, 52); ax.set_xlabel("Доля грамотных в 1926 г., %"); ax.set_ylabel("Прирост к 1939 г., п.п."); ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9.5, loc="upper right"); save(fig, "rj3_regiony")

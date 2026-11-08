"""Plot survey coverage and female participation in literacy schools."""

from pathlib import Path
import pandas as pd, numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent
d = pd.read_csv(OUT / "likbez1924_transcription.csv")
d = d[d.area == "rural"].sort_values("survey_coverage")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, axs = plt.subplots(1, 2, figsize=(12, 7), sharey=True)
pos = np.arange(len(d))
colors = np.where(d.survey_coverage < 0.8, "#b46328", "#356a9a")
axs[0].barh(pos, 100 * d.survey_coverage, color=colors)
axs[0].axvline(80, color="#777", ls="--", lw=1)
axs[0].set_xlim(0, 110)
axs[0].set_xlabel("Institutions surveyed, % of registered")
axs[1].barh(pos, d.female_pupil_share_pct, color=colors)
axs[1].set_xlim(0, 80)
axs[1].set_xlabel("Women among surveyed pupils, %")
for ax, values in [
    (axs[0], 100 * d.survey_coverage),
    (axs[1], d.female_pupil_share_pct),
]:
    ax.grid(axis="x", alpha=0.15)
    for i, value in enumerate(values):
        ax.text(value + 0.9, i, f"{value:.1f}", va="center", fontsize=9)
english_names = {
    "Татарская АССР": "Tatar",
    "Чувашская АССР": "Chuvash",
    "Марийская АО": "Mari",
    "Вотская АО": "Votyak",
    "Башкирская АССР": "Bashkir",
    "Карельская АССР": "Karelian",
    "Воронежская губ.": "Voronezh",
    "Курская губ.": "Kursk",
    "Смоленская губ.": "Smolensk",
    "Пензенская губ.": "Penza",
    "Саратовская губ.": "Saratov",
    "Сталинградская губ.": "Stalingrad",
    "Вятская губ.": "Vyatka",
    "Оренбургская губ.": "Orenburg",
    "Самарская губ.": "Samara",
    "Бурят-Монгольская АССР": "Buryat-Mongol",
    "Коми АССР": "Komi",
    "Марийская АССР": "Mari",
    "Мордовская АССР": "Mordovian",
    "Удмуртская АССР": "Udmurt",
    "Якутская АССР": "Yakut",
}
labels = d.unit_1926.map(english_names)
axs[0].set_yticks(pos, labels)
axs[0].invert_yaxis()
fig.suptitle(
    "Rural literacy points and schools on 1 January 1924",
    fontsize=12,
)
fig.text(
    0.5,
    0.02,
    "Orange marks territories with less than 80% of institutions surveyed.\nPupil shares describe surveyed institutions, not the coverage of all illiterate women.",
    ha="center",
    fontsize=9,
)
fig.tight_layout(rect=[0, 0.065, 1, 0.95])
fig.savefig(OUT / "survey_coverage_and_female_participation.png", dpi=170)

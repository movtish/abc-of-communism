"""Plot regional cohort literacy in 1939 and 1959."""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

OUT = Path(__file__).resolve().parent.parent
a = pd.read_csv(OUT / "republic_summary_1939_1959.csv")
maps = [(x,) for x in a.region.drop_duplicates()]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, axs = plt.subplots(1, 3, figsize=(15, 5.7), sharey=True)
order = [x[0] for x in maps]
for ax, area, title in zip(
    axs,
    ["total", "rural", "urban"],
    ["Total population", "Rural population", "Urban population"],
):
    for sex, color, shift, label in [
        ("M", "#356a9a", -0.14, "Men"),
        ("F", "#ad4560", 0.14, "Women"),
    ]:
        t = a[(a.area == area) & (a.sex == sex)].set_index("region").loc[order]
        ax.scatter(
            t.change_standardized_pp,
            np.arange(len(order)) + shift,
            color=color,
            s=38,
            label=label,
        )
    ax.axvline(0, color="#777777", lw=0.8)
    ax.set_title(title)
    ax.set_xlabel("Change in literacy, percentage points")
    ax.grid(axis="x", alpha=0.2)
axs[0].set_yticks(np.arange(len(order)), [english_names[n] for n in order])
axs[0].invert_yaxis()
axs[2].legend(loc="lower right")
fig.suptitle("Cohorts aged 30-44 in 1939 and 50-64 in 1959", fontsize=13)
fig.text(
    0.5,
    0.015,
    "Age composition is held at 1939 weights. Territorial cores are matched; small boundary transfers remain unresolved.\nChanges include later learning, war, selection, migration and enumeration differences.",
    ha="center",
    fontsize=9,
)
fig.tight_layout(rect=[0, 0.065, 1, 0.94])
fig.savefig(OUT / "literacy_persistence_regions.png", dpi=180)
plt.close(fig)

"""Aggregate the Malein district data to pre-1917 provinces.

Read the replication files under external/malein. Weight district means
by population in 1911, falling back to 1897 or 1867 when needed. Write
data/baseline_pre1917_by_province.csv."""

import os, sys, warnings, numpy as np, pandas as pd

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = f"{ROOT}/data"
M = f"{ROOT}/external/malein"
p = pd.read_stata(f"{M}/panel1879_1911.dta", convert_categoricals=False)
g = pd.read_stata(f"{M}/data_from_gelbach.dta", convert_categoricals=False)

# Keep one row per district for the historical census and school measures.
base = p.drop_duplicates("district")[
    [
        "district",
        "province_rus",
        "share_lit",
        "per_lit_f",
        "per_high_edu",
        "share_serfs",
        "share_old_beleivers1867",
        "share_muslim1867",
        "share_jewish1867",
        "per_germ",
        "school1867",
        "pop_all1867",
        "zemstvo_prov",
        "baltic",
    ]
].copy()
for yr in (1894, 1911):
    s = p[p.year == yr][
        [
            "district",
            "enrollment_rate",
            "enrollment_rate_f",
            "enrollment_rate_m",
            "school_density",
            "teachers_percap",
            "pop_all",
        ]
    ].copy()
    s.columns = ["district"] + [f"{c}_{yr}" for c in s.columns[1:]]
    base = base.merge(s, on="district", how="left")
z = p[p.year == 1894][["district", "exp_zemstvo_edu_percap"]].rename(
    columns={"exp_zemstvo_edu_percap": "exp_zemstvo_edu_pc_1894"}
)
base = base.merge(z, on="district", how="left")
gg = g[
    [
        "district",
        "lingfrac_1897",
        "lingpolarf4_1897",
        "sh_russian_1897",
        "sh_largestlingminority_1897",
        "religfrac_1870",
        "sh_orthodox_1870",
        "sh_muslim_1870",
        "mliteracy_1897",
        "agshare_1897",
        "population",
    ]
]
base = base.merge(gg, on="district", how="left")
base["w"] = base["pop_all_1911"].fillna(base["population"]).fillna(base["pop_all1867"])

RATE = [
    "share_lit",
    "per_lit_f",
    "per_high_edu",
    "share_serfs",
    "share_old_beleivers1867",
    "share_muslim1867",
    "share_jewish1867",
    "per_germ",
    "enrollment_rate_1894",
    "enrollment_rate_f_1894",
    "enrollment_rate_m_1894",
    "enrollment_rate_1911",
    "enrollment_rate_f_1911",
    "enrollment_rate_m_1911",
    "school_density_1894",
    "school_density_1911",
    "teachers_percap_1894",
    "teachers_percap_1911",
    "exp_zemstvo_edu_pc_1894",
    "lingfrac_1897",
    "lingpolarf4_1897",
    "sh_russian_1897",
    "sh_largestlingminority_1897",
    "religfrac_1870",
    "sh_orthodox_1870",
    "sh_muslim_1870",
    "mliteracy_1897",
    "agshare_1897",
]


def wavg(df, cols, w="w"):
    out = {}
    for c in cols:
        m = df[c].notna() & df[w].notna() & (df[w] > 0)
        # a few districts have no population in any year, then the plain mean
        out[c] = (
            float(np.average(df.loc[m, c], weights=df.loc[m, w]))
            if m.any() and df.loc[m, w].sum() > 0
            else (float(df[c].mean()) if df[c].notna().any() else np.nan)
        )
    out["n_districts"] = len(df)
    out["pop_weight"] = float(df[w].sum())
    return pd.Series(out)


prov = base.groupby("province_rus").apply(lambda d: wavg(d, RATE)).reset_index()
prov["zemstvo_prov"] = base.groupby("province_rus")["zemstvo_prov"].max().values
prov.to_csv(
    f"{D}/baseline_pre1917_by_province.csv", sep=";", index=False, encoding="utf-8-sig"
)
print("provinces:", len(prov), "| districts:", int(prov.n_districts.sum()))

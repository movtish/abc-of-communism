# The ABC of Communism

Code and data for the paper "The ABC of Communism: How Soviet Russia Taught Its Women to Read" by Mark Kreshchuk (working paper, 2026).

The paper follows the same rural birth cohorts through the censuses of 1897, 1926, 1939 and 1959. Women aged 20-34 in rural Russia in 1926 went from 43 to 61 per cent literate by 1939, while women of the same ages in 1897 had gained nothing in the thirty years before the campaign. The repository contains the census tables I transcribed, the scripts that build the samples and compute every number of the paper, and a Stata do-file that re-estimates the regressions.

## What is here

- `data/` census tables and the files built from them. CSV, separated by `;`, UTF-8. Descriptions are in `data/CODEBOOK.md`.
- `scripts/` Python scripts, listed below in the order in which they are run.
- `stata/ABC_of_Communism.do` the regressions of the paper in Stata.

Generated folders (`results/`, `figures/`, `paper/`, `stata/data/`, `stata/output/`) are not kept in the repository, the scripts create them.

## Sources

- Census of 1926 (Всесоюзная перепись населения 1926 года). Table IX of the regional volumes (population by sex, single years of age, main nationalities and literacy, for 44 units of the RSFSR) and Table XV of volume 9 (the same by Gosplan region, for 1926 and for 1897 recomputed to the borders of 1927). Scans of the Russian State Library, records 01010687703, 01009004437, 01009004436, 01009004435 and 01009004430 (https://search.rsl.ru/ru/record/ followed by the number). The tables were transcribed from the scans and checked against the printed totals, see `data/CODEBOOK.md`.
- Census of 1939. Tables of RGAE f. 1562, op. 336, d. 607 and 640 as published by Demoscope Weekly (`demoscope_1939.py` downloads them).
- Census of 1959. RGAE f. 1562, op. 336, d. 1591-1594, through Demoscope Weekly (`demoscope_1959.py`).
- Census of 2010. Rosstat, volume 3 table 1 and volume 4 tables 13 and 14 (`rosstat_get.py` downloads them, `census2010.py` reads them).

The pre-1917 district data are not included because they belong to other authors. They come from the replication package of Malein, "The Economic Power of Elites, Human Capital, and Industrial Change" (Explorations in Economic History, 2025), openICPSR project 231104, which also contains the district data of Dower, Finkel, Gehlbach and Nafziger (American Political Science Review, 2018) as `data_from_gelbach.dta`. To use them, download the package and copy its folder `replication/data` to `external/malein/`, so that the repository has

```
external/malein/panel1879_1911.dta
external/malein/data_from_gelbach.dta
external/malein/shape_files/districts_europe_collapsed.shp (and the other files of the shapefile)
```

`baseline_1897.py` then builds `data/baseline_pre1917_by_province.csv` from them, and `crosswalk.py` builds the district crosswalk used for the map. Without these files `build_1926_v2.py` still rebuilds everything except `russians_region_baseline.csv`, but `paper_numbers.py` needs that file (Russians across units, Appendix F of the paper).

## How to run

Python 3.12 with the packages in `requirements.txt`. From the root of the repository:

```
python scripts/baseline_1897.py      # pre-1917 baseline by province (needs external/malein)
python scripts/crosswalk.py          # 1897 districts -> 1926 units, for the map (needs external/malein)
python scripts/build_1926_v2.py      # validation of Table IX, rebuilds the derived 1926 files and the link to 1939
python scripts/wave2_rayon.py        # the same cohorts by Gosplan region, 1926-1939
python scripts/paper_numbers.py      # every number of the paper and paper/numbers.tex, about 15 minutes (--fast skips permutations and bootstraps)
python scripts/make_tables.py        # paper/tables/*.tex
python scripts/paper_figures.py      # figures/*.pdf and *.png
python scripts/export_stata.py       # stata/data/*.dta
```

`paper_numbers.py` writes all numbers with their keys to `results/paper_numbers.json` and `.csv`. The text of the paper contains no typed numbers, it reads them from `paper/numbers.tex` through macros (`\N{key}`), so a change in a specification goes through to the text, the tables and the figures.

For Stata, run `stata/ABC_of_Communism.do` from the folder `stata/` after `export_stata.py`, then `python scripts/compare_stata.py`, which compares the two sets of estimates key by key. In my last run 1,072 of 1,074 coefficients were identical and the other two are not identified in either program.

The scripts that download the source tables (`demoscope_1939.py`, `demoscope_1959.py`, `rosstat_get.py`) and the one that builds `tableXV_linked_cohorts.csv` (`linked_cohorts.py`) do not need to be run, their output is already in `data/`.

## Validation of the 1926 tables

Table IX prints a subtotal after every five single years of age, so every five-year figure exists twice. A five-year group is used if the printed subtotal equals the sum of the single years, or if one of the two figures satisfies another identity of the table (urban plus rural equals total, nationalities add up to the whole population), or if one of them is consistent with the adjacent cohorts and the other is not. The rest is dropped. Details are at the top of `scripts/build_1926_v2.py` and in Appendix A of the paper. `data/v1_before_validation/` keeps the derived files of the first version, before this validation, because `build_1926_v2.py` compares the new files with them.

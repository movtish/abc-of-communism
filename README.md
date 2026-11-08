# The ABC of Communism

Mark Kreshchuk  
*How Soviet Russia Taught Its Women to Read*

This paper follows birth cohorts through the censuses of 1897, 1926, 1939 and 1959 to study adult literacy during the Soviet campaign against illiteracy. Newly transcribed regional tables distinguish changes within adult cohorts from the replacement of older generations by schooled children.

The main younger-minus-older contrast for rural women is 20.354 percentage points, with a CR2 95 per cent interval of [16.679, 24.028]. Its causal interpretation depends on counterfactual learning, migration, mortality and enumeration. Regional evidence from 1924 and 1959 examines institutional correlates and later cohort composition.

[English reading package, 4.58 MB](docs/ABC_of_Communism_reader.zip) · [Paper and online appendix](paper/ABC_of_Communism.pdf) · [Russian article](jnea/article_jnea.pdf) · [Data and methods](docs/METHODS.md) · [Further evidence](docs/SUPPLEMENTARY_EVIDENCE.md) · [Sources](docs/SOURCES.md)

## Data and code

`data/` holds the census transcriptions and derived samples. The [codebook](data/CODEBOOK.md) describes fields and validation rules. Main CSV files use semicolons; supplementary files use commas. Both use UTF-8.

`scripts/` builds the main analysis. `methodology/` provides the additional cluster-inference checks. The two folders under `supplementary/` contain the 1924 institutional survey and the regional 1939-1959 follow-up, each with its own README. Source URLs, hashes and known discrepancies are retained with the data. `results/` and `figures/` contain the reported output; `paper/` and `jnea/` contain the manuscript sources.

## Reproduction

Use Python 3.12 and run from the repository root.

```sh
python -m pip install -r requirements.txt
python scripts/build_1926_v2.py
python scripts/wave2_rayon.py
python scripts/paper_numbers.py
python scripts/make_tables.py
python scripts/paper_figures.py
python methodology/test_inference.py
python methodology/run_analysis.py . methodology/results
python methodology/accounting.py . methodology/results
python scripts/run_supplementary.py
python scripts/verify_release.py
```

The main number calculation includes resampling and takes about fifteen minutes. Seeds are fixed. `--fast` omits resampling and is intended for diagnostics. [Build instructions](docs/BUILD_STATUS.md) cover the PDFs and Russian tables. Stata export is available through `scripts/export_stata.py`; running `stata/ABC_of_Communism.do` requires Stata.

The included baseline tables allow reproduction without the external Malein district package, openICPSR 231104. Rebuilding those baselines and the district map requires its data under `external/malein/`. See `scripts/baseline_1897.py` and `scripts/crosswalk.py`. No restricted third-party microdata are redistributed.

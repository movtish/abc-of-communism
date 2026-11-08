# The ABC of Communism

Mark Kreshchuk  
*How Soviet Russia Taught Its Women to Read*

This paper studies adult literacy during the Soviet campaign against illiteracy. It follows birth cohorts through the censuses of 1897, 1926, 1939 and 1959, separating changes within cohorts from the replacement of older generations by schooled children. Regional tables on literacy institutions in 1924 provide an additional comparison.

[English paper and appendix](paper/ABC_of_Communism.pdf) · [English reading package](docs/ABC_of_Communism_reader.zip) · [Russian paper](jnea/article_jnea.pdf)

The reading package contains the English paper, two research notes, the source list and the codebook. It excludes the historical scans.

## Contents

| Folder | Contents |
|---|---|
| [data](data/) | Census transcriptions, territorial keys and analysis samples |
| [scripts](scripts/) | Data preparation, estimation, tables and figures |
| [results](results/) | Saved estimates and the numbers used in the paper |
| [figures](figures/) | Figures in PDF and PNG formats |
| [methodology](methodology/) | Cluster inference and selection-accounting checks |
| [supplementary](supplementary/) | The 1924 institutional survey and the 1939-1959 regional comparison |
| [paper](paper/) | English manuscript, appendix and bibliography |
| [jnea](jnea/) | Russian manuscript, tables and figures |
| [stata](stata/) | Stata replication of the main specifications |
| [validation](validation/) | Source comparisons, known discrepancies and build records |
| [docs](docs/) | Methods, sources, file index and document builds |

[File index](docs/FILES.md) · [Codebook](data/CODEBOOK.md) · [Methods](docs/METHODS.md) · [Additional results](docs/SUPPLEMENTARY_EVIDENCE.md) · [Sources](docs/SOURCES.md)

## Replication

Use Python 3.12. Run these commands from the repository root.

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

The main calculation takes about fifteen minutes with resampling. Random seeds are fixed. The `--fast` option skips resampling for diagnostic runs. Main CSV files use semicolons; supplementary CSV files use commas. Both use UTF-8.

The included baseline tables allow replication without the external Malein package, openICPSR 231104. Rebuilding those tables and the district crosswalk requires its files under `external/malein/`. See `scripts/baseline_1897.py` and `scripts/crosswalk.py`. Restricted third-party microdata are excluded.

For Stata, run `python scripts/export_stata.py` after the main calculation, then `stata/ABC_of_Communism.do`. Document build commands are in [docs/BUILD_STATUS.md](docs/BUILD_STATUS.md).

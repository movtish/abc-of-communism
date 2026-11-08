# The ABC of Communism

Code, census transcriptions and manuscript sources for Mark Kreshchuk's working paper, *The ABC of Communism: How Soviet Russia Taught Its Women to Read*.

## Current revision: 8 November 2026

This revision brings together the local manuscript, the public replication code, the methodological audit and two new supplementary analyses. The evidence documents changes in recorded cohort literacy. Attribution to the campaign requires assumptions about counterfactual learning, migration, mortality, borders and reporting. Institutional channels are exploratory.

- Corrected the Moscow/Leningrad city–oblast population-scope mismatch in 224 urban/total rows of the 1939 data and removed double counting in aggregates. Rural female younger-minus-older contrast: **20.3537 pp**; CR2 95% interval **[16.6792, 24.0282]**. DDD: **14.3791 pp**, interval **[9.7385, 19.0197]**. DDD measures a relative change between sexes, not the female treatment effect.
- Added the 1959 regional workbook: **20,025 rows**, with partition, population and HTML/XLS consistency checks. Nine republics support a descriptive post-1939 comparison; five form the core sample. Same-name territories have not been fully harmonised for small boundary transfers. Nested territorial entries must not be added together.
- Added **30 checked rows for 15 territories** from the 1 January 1924 survey of literacy institutions. Fourteen link to the validated youngest cohort. All 24 exploratory institutional-model CR2 intervals include zero; these data do not identify causal mediation.
- Added eight age-policy checks using the 1931 plan. Narrowing the younger group changes the female contrast from **20.354 to 20.312 pp**.

Подробности по-русски: [методологическая проверка](docs/ECONOMETRICS_REVIEW_RU.md), [новые данные 1959 года](supplementary/additional_data_analysis/ADDITIONAL_DATA_ANALYSIS_RU.md), [учреждения ликбеза 1924 года](supplementary/likbez_1924_analysis/REPORT_RU.md). Исходные отчёты сохраняют исторические описания отдельных этапов работы; актуальный статус проекта задаёт этот README.

## Files

- `data/`: main census data, validated cells and published derived baselines; see [CODEBOOK](data/CODEBOOK.md). Main CSV files use `;`.
- `scripts/`: main build, tables, figures, downloaders and Stata export. Paths are relative to the checkout.
- `paper/`, `jnea/`: revised English and Russian LaTeX sources and generated tables. The English appendix includes both new analyses.
- `results/`, `figures/`: current main calculation snapshots and figures. Independent CR2 results live in `methodology/results/`.
- `methodology/`: independent inference, 88 specification checks and accounting sensitivities; CR1, CR2/Satterthwaite, cluster jackknife and restricted wild cluster bootstrap. `errors.json` records an expected unidentified specification; unavailable CR2 contrasts are explicitly flagged.
- `supplementary/additional_data_analysis/`: 1959 source workbook, regional panel, migration/time-use extracts, scripts and results.
- `supplementary/likbez_1924_analysis/`: historical PDFs and source page images, institutional transcription, 24 exploratory models and eight policy-age checks.
- `validation/`: source evidence, scope corrections and changed numerical keys; `docs/`: audit and source-search reports.

Supplementary CSV files use commas and UTF-8 with BOM. `inputs/` inside each supplement are verified snapshots of main results; the release verifier checks that these inputs still match the main project. These folders also include historical scans examined during the source search; not every scan enters a regression. Download URLs and SHA-256 hashes are in each source manifest. No restricted third-party replication microdata are redistributed.

The full 1939 extraction retains 17 unresolved cells with illiterate counts exceeding population, all in the open age group 70+ of nested territories. They are listed in `validation/1939_unresolved_70plus_cells.csv`; their values are not silently repaired. They enter neither the matched age cohorts nor the national aggregates, which exclude nested territories. The release check separately enforces nonnegative counts for non-nested territories.

## Reproduction

Python 3.12 and the dependencies in `requirements.txt`:

```sh
python -m pip install -r requirements.txt
python scripts/build_1926_v2.py
python scripts/wave2_rayon.py
python scripts/paper_numbers.py
python scripts/make_tables.py
python scripts/jnea2_tables.py
python scripts/paper_figures.py
python scripts/jnea2_figures.py
python scripts/export_stata.py
python methodology/test_inference.py
python methodology/run_analysis.py . methodology/results
python methodology/accounting.py . methodology/results
python scripts/run_supplementary.py
python scripts/verify_release.py
```

`paper_numbers.py` includes resampling and can take about 15 minutes. `--fast` omits resampling and is only a diagnostic run. `run_supplementary.py` refreshes input snapshots from the main project before regenerating both supplements. Estimation scripts set seeds. Complete sign-vector enumeration with few clusters is not an exact causal randomisation test. The main paper's original inference and the independent CR2 checks are kept distinguishable.

The checked-in baseline tables permit rebuilding the main analysis without the external Malein package. To reconstruct those historical baselines or the district shapefile map, obtain the third-party files described in [the earlier public instructions](docs/README_github_before_update.md). The map builder keeps an existing checked figure when external geometry is unavailable. Source downloaders are optional: their inputs are already included. To regenerate the Stata data, use `export_stata.py`; executing Stata and comparing its output requires a licensed installation. Earlier Stata results have not been revalidated for this revision.

The primary sources are census tables hosted by [Demoscope](https://www.demoscope.ru/weekly/ssp/census.php), the 1926 regional volumes listed in the codebook, and the 1924/1931 publications linked in the new appendix and source manifests. The downloaded files are preserved without changing their numeric tables; some HTML copies were decoded to UTF-8.

## Manuscript PDF status

Revised LaTeX sources, numbers, tables and figure files are included. Article PDFs from earlier versions are not current outputs and are not published as this revision. A successful fresh TeX build and visual review of both articles remain outstanding because the available TeX installation could not initialise in this environment. See [BUILD_STATUS](docs/BUILD_STATUS.md). The numerical and Python checks are separate from that publishing limitation.

# The ABC of Communism

Code and data for Mark Kreshchuk's working paper, *The ABC of Communism. How Soviet Russia Taught Its Women to Read*.

The paper follows birth cohorts through the censuses of 1897, 1926, 1939 and 1959. It documents a large rise in the recorded literacy of adult women during the Soviet campaign against illiteracy. The comparisons address how far that rise can be attributed to the campaign and what can be learned about its institutions.

The November 2026 revision corrects the territorial scope of the 1939 Moscow and Leningrad data, adds regional education tables from 1959 and transcribes a survey of literacy institutions in 1924. The main rural female contrast is 20.354 percentage points, with a CR2 interval of [16.679, 24.028]. The institutional comparisons are exploratory. They do not identify separate effects of enforcement, household decisions and private returns.

## Reading the project

- [English article with the online appendix](paper/ABC_of_Communism.pdf), [LaTeX source](paper/ABC_of_Communism.tex) and [appendix source](paper/appendix.tex).
- [Data and methods](docs/METHODS.md), also available as a [PDF](docs/Data_and_methods.pdf).
- [Further historical evidence](docs/SUPPLEMENTARY_EVIDENCE.md), also available as a [PDF](docs/Supplementary_evidence.pdf).
- [Source register](docs/SOURCES.md), distinguishing downloaded data, partial scans and archival leads.
- [Main census codebook](data/CODEBOOK.md).

The [Russian journal article](jnea/article_jnea.pdf) and its sources are retained in `jnea/`. Original source publications and census keys keep their Russian wording. Reader-facing documentation and the new supplementary figures are in English. Earlier local reports are preserved in the local archive rather than presented as current English documentation.

## Files

`data/` contains the main transcriptions, validated cells and derived baselines. `scripts/` builds the samples, estimates, tables, figures and Stata exports. `results/` and `figures/` contain the current outputs. The English and Russian manuscript sources and their tables are in `paper/` and `jnea/`.

`methodology/` contains independent inference and 88 specification checks. Its result files distinguish CR1, CR2/Satterthwaite, the cluster jackknife and the restricted wild cluster bootstrap. Expected failures of identification are recorded explicitly.

`supplementary/additional_data_analysis/` contains the 1959 workbook, the regional follow-up and migration and time-use extracts. `supplementary/likbez_1924_analysis/` contains the institutional transcription, source page images, 24 exploratory institutional models and eight checks omitting an intermediate age cohort. Each folder has an English README, scripts, inputs, source hashes and results.

The age-policy check keeps the younger group at ages 18-32 in 1926 in both specifications. Omitting ages 33-37 from the intermediate group changes the female contrast from 20.354 to 20.312 points. Earlier supplementary labels described the omission incorrectly. The numerical estimates are unchanged, and the corrected explanation is in the methods note.

The full 1939 extraction preserves 17 unresolved inconsistent cells, all in nested territories at ages 70+. They enter neither the matched cohorts nor the national aggregates. `validation/` lists them alongside source comparisons and release checks. The 1959 workbook also includes totals and nested territories; its 89 entries must not all be added together.

## Reproducing the results

Use Python 3.12 with the packages in `requirements.txt`. Run these commands from the project root.

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

The full number calculation includes resampling and can take about fifteen minutes. `--fast` skips resampling and is intended for diagnostics. The supplementary runner refreshes its input snapshots from the main data and results. Seeds are fixed. Enumerating every wild-bootstrap sign vector does not turn the observational design into an exact causal randomisation test.

Main CSV files use semicolons. Supplementary CSV files use commas. Both use UTF-8, usually with a byte-order mark. Source manifests give download URLs and SHA-256 hashes. No restricted third-party microdata are included.

The checked-in baseline tables are enough to rebuild the main analysis. To reconstruct them from the district data, obtain the Malein replication package, openICPSR project 231104, and place `panel1879_1911.dta`, `data_from_gelbach.dta` and the `shape_files/` directory under `external/malein/`. Then run `scripts/baseline_1897.py` and `scripts/crosswalk.py`. The shapefile is also needed to redraw the district map; otherwise the figure builder retains the included map. Original source downloaders need not be run to reproduce the checked-in analysis.

The Stata do-file reads the exported data. Running it requires a licensed installation. Stata output has not been revalidated for this revision.

## Documents

The two English PDF notes are generated from their Markdown sources.

```sh
python -m pip install -r requirements-docs.txt
python scripts/build_docs.py
```

Both current article PDFs have been built and visually checked. A local Tectonic runtime and the downloaded package cache are included in this local project folder but excluded from Git. To rebuild both articles without network access, run the following command.

```sh
python scripts/build_articles.py --offline
```

On a fresh checkout, install Tectonic 0.17.0 and run `python scripts/build_articles.py --tectonic /path/to/tectonic` once with network access. The script uses the official bundle storage directly. Build details are recorded in [BUILD_STATUS.md](docs/BUILD_STATUS.md), and source and PDF hashes in `validation/article_pdf_build.json`.

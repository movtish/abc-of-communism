# Literacy institutions in 1924

Table XVII of the education survey of 1 January 1924 records literacy schools and points, teachers and pupils. The transcription covers thirty total and rural rows in fifteen territories. The source is volume XXVIII, issue 1 of the Central Statistical Administration series, published in 1926, printed pages 462-467. These are PDF pages 67-69 in `raw_sources/education_1924.pdf`.

Fourteen territories match the validated male and female cohort aged 18-22 in 1926. Regressions compare early institutional measures with the female-minus-male literacy gain through 1939. The twenty-four specifications vary predictors, weights and geographical coverage. All CR2 intervals include zero. The early survey and endogenous placement of institutions limit causal interpretation.

| File | Contents |
|---|---|
| `likbez1924_transcription.csv` | Source counts, survey coverage and validation flags |
| `linked1924_exposure_cohort_outcomes.csv` | The fourteen territories matched to census outcomes |
| `institution_predictor_models.csv` | Twelve female pupil-share and teacher-share models |
| `institution_scale_models.csv` | Twelve institution-count and teacher-count models |
| `policy1931_age_sensitivity.csv` | Eight estimates with and without intermediate ages 33-37 |
| `transcription_validation.json` | Arithmetic checks on the source rows |
| `reproduction_check.json` | Results of rerunning the packaged analysis |
| `source_manifest.json` | Source URLs, file sizes and SHA-256 hashes |
| `inputs/` | The main-sample snapshot used to link cohorts |
| `raw_sources/` | Historical publications and inspected page images |
| `scripts/` | Transcription, estimation and plotting |

The age check keeps the younger group at 18-32. Survey coverage counts institutions surveyed; it does not measure the share of illiterate adults taught. The Bashkir teacher total exceeds the sex sum by three, which is retained. Boundaries remain partly unresolved. The geographical exclusion removes Chuvash and Orenburg.

Install the root requirements and run from the repository root.

```sh
python supplementary/likbez_1924_analysis/scripts/analyze_1924.py
python supplementary/likbez_1924_analysis/scripts/estimate_1924.py
python supplementary/likbez_1924_analysis/scripts/plot_1924.py
```

Scripts replace derived outputs in this folder. CSV files use commas and UTF-8 with a byte-order mark. Larger samples use 9,999 bootstrap draws; smaller institutional samples enumerate 2,048 or 512 sign vectors. Random seeds are fixed. See [additional results](../../docs/SUPPLEMENTARY_EVIDENCE.md) for model definitions and estimates.

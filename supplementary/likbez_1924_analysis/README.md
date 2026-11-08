# Literacy institutions in 1924

The transcription covers Table XVII of the Central Statistical Administration's education survey of 1 January 1924, published in volume XXVIII, issue 1 in 1926. Printed pages 462-467 are PDF pages 67-69 in `raw_sources/education_1924.pdf`.

Thirty checked rows cover fifteen territories, for total and rural populations. They count literacy points and schools, surveyed institutions, teachers and pupils by sex. Adjacent general adult-school columns are excluded. These are pupils on one date, not unique graduates or cohort-specific exposure.

Fourteen territories link to validated male and female cells aged 18-22 in 1926. The models ask whether early institutional measures predict the subsequent female-minus-male literacy gain. The outcome, baseline gap and cohort-size control are documented in [the English evidence note](../../docs/SUPPLEMENTARY_EVIDENCE.md). All 24 CR2 intervals include zero; this is not evidence of a zero causal effect.

Survey coverage is the share of registered institutions observed, not the share of illiterate adults taught. The Bashkir total teacher count exceeds the sex sum by three, and this residual is preserved. Boundaries have not been fully harmonised. The additional geographical filter removes only the Chuvash and Orenburg units as known concerns.

## Files and reproduction

`likbez1924_transcription.csv` contains the source rows and validation flags. `linked1924_exposure_cohort_outcomes.csv` contains the fourteen linked territories. The two institutional model CSVs report twelve share and twelve scale specifications. `policy1931_age_sensitivity.csv` reports eight checks with or without the intermediate cohort aged 33-37 in 1926. The younger group remains aged 18-32 throughout. `specification` and `excluded_cohort` identify the omission explicitly.

`raw_sources/` contains historical PDFs and the inspected page images. `source_manifest.json` records their URLs and hashes. `inputs/W2_cells.csv` is the verified main-sample snapshot. The full 1930s exposure panel remains unavailable.

After installing the root requirements, run from the project root.

```sh
python supplementary/likbez_1924_analysis/scripts/analyze_1924.py
python supplementary/likbez_1924_analysis/scripts/estimate_1924.py
python supplementary/likbez_1924_analysis/scripts/plot_1924.py
```

The scripts overwrite only derived outputs in this folder. CSV files use commas and UTF-8 with a byte-order mark. The larger samples use 9,999 wild-bootstrap draws; the smaller institutional samples enumerate 2,048 or 512 sign vectors. Seeds are fixed. These remain exploratory comparisons with endogenous institutional placement.

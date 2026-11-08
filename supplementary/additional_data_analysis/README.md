# Regional cohort literacy in 1959

This folder reads the Demoscope education workbook and follows selected regional birth cohorts from 1939 to 1959. It also includes contemporary migration extracts and a small 1923 time-use survey. The interpretation and results are in [the English evidence note](../../docs/SUPPLEMENTARY_EVIDENCE.md).

The workbook produces 20,025 rows. Component identities, population totals and four HTML tables are checked separately. The 89 territorial entries include national totals and nested units, so they cannot be summed as independent regions. Ages 70+ cannot be split into later five-year cohorts.

For ages nine and above, literacy is population minus unknown education minus illiterates, divided by population minus unknown education. Source blanks are retained in flags. A blank component becomes zero only where the other nonnegative components exhaust the total exactly.

The follow-up matches ages 30-44 in 1939 to ages 50-64 in 1959, using three five-year bands and fixed 1939 weights. Five republics form the core sample and nine the extended sample. Small boundary transfers remain unresolved. The twelve models describe later changes in the female-minus-male gap; they do not estimate the campaign's causal effect or bound misreporting in 1939.

## Files and reproduction

`raw_sources/` preserves downloaded files. `source_file_manifest.json` records their URLs and hashes. `inputs/` contains the corrected 1939 snapshot. `validation_summary.json` records the accounting checks. The long table, linked cohorts, sample summaries, model estimates and English figure are in this folder.

After installing the root requirements, run from the project root.

```sh
python supplementary/additional_data_analysis/scripts/analyze_new_data.py
python supplementary/additional_data_analysis/scripts/verify_1939_values.py
python supplementary/additional_data_analysis/scripts/estimate_post1939.py
python supplementary/additional_data_analysis/scripts/make_plot.py
```

The scripts read the included inputs and overwrite their derived outputs. CSV files use commas and UTF-8 with a byte-order mark. All 32 or 512 Rademacher vectors are used in the respective regional bootstrap checks. The extraction checks establish agreement with the digitised sources, not historical census accuracy.

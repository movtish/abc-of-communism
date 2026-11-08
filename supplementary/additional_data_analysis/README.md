# Regional cohorts in 1939 and 1959

The 1959 Demoscope workbook gives 20,025 education records. Its 89 territorial entries include national totals and nested units. The extraction checks educational components, population totals and four HTML tables. The open-ended 70+ group cannot be divided into later five-year cohorts.

For ages nine and above, literacy equals population minus unknown education minus illiterates, divided by population minus unknown education. Source blanks retain flags. A blank becomes zero only when known nonnegative components exhaust the total.

The regional comparison follows ages 30-44 in 1939 to ages 50-64 in 1959 in three five-year bands, using fixed 1939 population weights. Five republics form the core sample and nine the extended sample. Twelve models describe changes in the female-minus-male gap. They combine learning with changes in population composition and do not identify a campaign effect or a bound on 1939 misreporting. Small boundary transfers remain unresolved.

| File or folder | Contents |
|---|---|
| `census1959_regions_long.csv` | Regional education counts and source blank flags |
| `linked_republic_cohorts_1939_1959.csv` | Cohorts matched across the two censuses |
| `republic_summary_1939_1959.csv` | Literacy changes by republic, sex and residence |
| `persistence_sample_summary.csv` | The core and extended comparison samples |
| `post1939_gender_gap_inference.csv` | Twelve model estimates and cluster inference |
| `census1959_*_checks.csv` | Workbook identities and comparisons with HTML tables |
| `census1939_online_checks.csv` | Comparisons with the downloaded 1939 tables |
| `migration_*.csv` | Contemporary migration extracts for 1931-1932 |
| `time_use_1923_domestic_work.csv` | Domestic-work entries from the Voronezh survey |
| `validation_summary.json` | Extraction and accounting checks |
| `reproduction_check.json` | Results of rerunning the packaged analysis |
| `source_file_manifest.json` | Source URLs, file sizes and SHA-256 hashes |
| `inputs/` | The corrected 1939 census input |
| `raw_sources/` | Downloaded workbooks, publications and HTML tables |
| `scripts/` | Extraction, source comparisons, estimation and plotting |

Install the root requirements and run from the repository root.

```sh
python supplementary/additional_data_analysis/scripts/analyze_new_data.py
python supplementary/additional_data_analysis/scripts/verify_1939_values.py
python supplementary/additional_data_analysis/scripts/estimate_post1939.py
python supplementary/additional_data_analysis/scripts/make_plot.py
```

Scripts replace derived outputs in this folder. CSV files use commas and UTF-8 with a byte-order mark. The regional bootstrap enumerates all 32 or 512 sign vectors for the relevant sample. The [additional-results note](../../docs/SUPPLEMENTARY_EVIDENCE.md) reports the estimates and interpretation.

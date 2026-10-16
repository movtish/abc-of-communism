# Codebook

All files are CSV separated by `;`, UTF-8 with BOM. Names of units, nationalities and regions are in Russian as printed in the census.
Sex is `M` or `F`, area is `total`, `urban` or `rural`. Literacy is the share of the population able to read (in any language), in per cent.

## Census of 1926, Table IX

### census1926_tableIX_long.csv
Table IX "Население по полу, возрасту, главным народностям и грамотности" of the regional volumes (T1, T2, T3, T4), as transcribed.
One row is unit x area x age x nationality x sex. 90,642 rows.
- `region_code`, `region` unit of 1926 (republic, autonomous oblast, guberniya or okrug). "Уральская обл." is the sum of its okrugi and is not used in the samples, so that the number of distinct units is 44.
- `pre1917_province` province or provinces of 1897 from which the unit was formed, lower case as in Malein's `province_rus` (several are separated by `;`).
- `volume`, `pdf_page` where the cell is in the scans.
- `age` single years `0` ... `99`, five-year subtotals `0-4` ... `95-99`, `100+`, `unknown`, `TOTAL`.
- `group` nationality as printed (`Всё население` is the whole population). `group_type` is `all`, `russian`, `titular` (the nationality in its own unit), `minority` or `other`.
- `total`, `literate` persons. Literacy at ages 0-4 is printed as a dash and stored as 0.
- `quality` how the cell was confirmed at transcription: `ok` by at least one arithmetic identity of the table, `agree` two independent readings agree, `ocr2only` only the second reading has a value, `unresolved` the readings differ, `missing` no value, `manual` corrected against the scan.

The `quality` flag is not used to select cells any more. The analysis uses the validated files below, because a cell can pass an identity and still be wrong when the same misreading entered both the single years and the subtotal.

### tableIX_five_year_groups_validated.csv
One row is unit x area x nationality x sex x five-year group (ages 5 and over).
`P_pop`, `P_lit` printed subtotal; `S_pop`, `S_lit` sum of the five single years; `val_pop`, `val_lit` the figure used.
`tier_pop`, `tier_lit`, `tier`: 1 printed subtotal equals the sum of single years (within 2 persons or 0.5 per cent), 2 chosen by an identity of the table (urban plus rural equals total, nationalities add up to the whole population), 3 chosen by consistency with the two adjacent groups, 0 dropped.
`src_*`: `PS` both agree, `P` printed subtotal taken, `S` sum taken, `I` value implied by two identities, `X` removed by the neighbour rule (literacy more than 25 points from both adjacent groups, or population more than three times or less than a third of both).

### tableIX_single_years_validated.csv
Single years of age with `valid` (the five-year group is validated and the validated figure is the sum of the single years) and `tier5`.

### tableIX_bands_validated.csv
The age bands used in the paper (8-11, 12-14, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60-69, 60+), built from validated groups or single years, after the plausibility rules (population per year of age above 2.5 times the median of the series, literacy more than 30 points from both adjacent bands, series with fewer than three bands, cells below 200 persons).
Columns `region`, `area`, `group`, `sex`, `band`, `population`, `literate`, `literacy`, `tier`, `group_type`.

### tableIX_region_quality.csv
Share of confirmed cells by unit and area. Six units have rural pages of low quality (Astrakhan, Kungur, Volga German ASSR, Orenburg, Penza, Samara) and are dropped in one robustness check.

### Files built from the validated tables by build_1926_v2.py
- `korenizatsiya_panel.csv` literacy by unit x area x nationality x sex x band, with `titular_unit` (nationality inside its own unit) and `has_unit_1926` (the nationality had a unit in 1926). Cells below 200 persons dropped.
- `russians_by_region.csv` Russians and the whole population by unit, area and band, literacy of men and women and the gender gap.
- `mechanism_panel.csv`, `mechanism_panel_clean.csv` (the same file under two names, both are read by the scripts) one row per unit and nationality: child-woman ratio `cwr`, sex ratio at 20-39, sex ratio at 0-4, urban shares of men and women aged 20-39, literacy and gender gaps at 12-14, 20-24 and 30-39, gaps to Russians in the same unit (`ethgap_*`), and `mobility_gap` (urban share of men minus that of women).
- `tableIX_cohort_gaps.csv` literacy of the titular nationality and of Russians in the six titular units by band and sex, gap = Russian minus titular.
- `linked_cohorts_1926_1939.csv` the same birth cohorts in 1926 (single years 8-57) and 1939 (five-year groups 20-24 ... 65-69) by unit and region of 1939, area and sex: population, literacy, gain in points, survival ratio, `tier`. The cohorts aged 48-57 in 1926 were above the age limit of the campaign.
- `russians_region_baseline.csv` (not in the repository, it contains the pre-1917 baseline) Russians by unit with the provincial baseline of 1897 and 1911 merged in.

## Census of 1926, Table XV of volume 9

### tableXV_1926_1897_age_sex_literacy.csv
Table XV "Население по полу, возрасту и грамотности по переписям 17 декабря 1926 г. и 9 февраля 1897 г." (the figures of 1897 recomputed by the Central Statistical Board to the borders of 1 January 1927).
One row is Gosplan region x census year x area x sex x age. Ages are single years 0-19 with subtotals, then five-year groups. Columns `population`, `literate`, `literacy_rate`, `quality` as above. The urban population of 1897 follows the definition of 1897.

### tableXV_linked_cohorts.csv
The same birth cohorts in 1897 and 1926 (born 1858-67, 1868-77, 1878-87) by region, area and sex: literacy in both censuses, gain in points, survival ratio. Built by `linked_cohorts.py`.

### linked_cohorts_rayon_1926_1939.csv
Cohorts of Table XV in 1926 linked to the census of 1939 aggregated to the 17 Gosplan regions of the RSFSR of 1939. `approx_borders` is 1 when the regions of 1939 only approximately cover the region of 1926. Built by `wave2_rayon.py`.

## Later censuses

### census1939_literacy_by_region_age_sex.csv
Census of 1939 (RGAE f. 1562, op. 336, d. 607 and 640, from Demoscope Weekly): population, illiterate and literate by region of 1939, area, sex and five-year group.

### census1959_rsfsr_edu_by_age_sex.csv
Census of 1959, RSFSR (RGAE f. 1562, op. 336, d. 1591-1594, from Demoscope Weekly): population by area, sex, age and level of education. `literate` is everyone with any schooling plus the literate without primary schooling, `literacy` is per 100 persons who stated their education.

### census2010_nat_edu_by_subject.csv, census2010_nat_edu_by_age_sex.csv, census2010_edu_by_subject_age_sex.csv
Census of 2010 (Rosstat, volume 4 tables 14 and 13, volume 3 table 1): population aged 15 and over by level of education, by nationality and subject, by nationality, sex and age, and by subject, sex and age. Shares in per cent of those who stated their education (`sh_higher`, `sh_sec_plus`, `sh_basic_plus`, `sh_illit`, `sh_noprim`).

## Keys

### region_keys.csv
Unit of 1926 -> Gosplan region of 1927 (Table XV) -> provinces of 1897 (Malein's `province_rus`) -> subject of 2010.

## Not in the repository

`baseline_pre1917_by_province.csv` (built by `scripts/baseline_1897.py`) and `crosswalk_1897_districts_to_1926_units.csv` (built by `scripts/crosswalk.py`) are computed from Malein's replication package, see the README. The provincial baseline is the population-weighted mean of the districts of each province of 1897, so all units carved from one province share its value, and the regressions on it are clustered by that province (`pg`). `teachers_percap_1911` counts the teachers of all primary schools in Malein's panel.

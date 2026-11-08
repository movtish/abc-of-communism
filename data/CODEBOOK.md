# Census data codebook

The 1926 transcription uses RSL scans of the All-Union Population Census of 1926, section I. The extraction combines the embedded OCR layer, a second RapidOCR reading and table identities. The raw `quality` field records how each value was obtained. Validated files carry separate `tier` fields.

## Files

### tableIX_1926_age_sex_ethnicity_literacy.csv
Source publication - Таблица IX «Население по полу, возрасту, главным народностям и грамотности», regional volumes
(T1 = Северный/Ленинградско-Карельский/Западный; T3 = ЦЧО/Средне- и Нижне-Волжский; T4 = Вятский/Урал/Башкирия).
One row = region × area × age × ethnic group × sex.
- region_code / region_1926 - 1926 administrative unit (по всей республике/области = area `total`).
- pre1917_province - Malein/Dower `province_rus` value(s) the unit was carved from (for baseline merges).
- age - single years 0-99 (`0`…`99`), five-year subtotals (`0-4` … `95-99`), `100+`, `unknown`, `TOTAL`.
  Subtotal rows are as printed; single-year rows sum to them (checked).
- birth_cohort - census year minus age (census day 17 Dec 1926): `1902` or `1902-1906` for bands.
- group - ethnic group as printed; `group_type` takes the values `all` (Всё население), `titular`, `russian`, `other`.
- population, literate - persons; literacy_rate = 100*literate/population.
- quality: `ok` = confirmed by ≥1 checksum equation; `agree` = OCR layer and second OCR read the same value;
  `ocr2only` = only the second OCR could read the cell; `unresolved` = readings conflict, value is the OCR-layer read;
  `missing` = no reading. Ages 0-4 literacy is printed as «—» (not assessed) and stored as 0.
Row count - 90642; quality counts - {'unresolved': 3434, 'ocr2only': 2031, 'ok': 80958, 'missing': 1910, 'manual': 56, 'agree': 2253}.

### tableXV_1926_1897_age_sex_literacy.csv
Source publication - Т.9, Таблица XV «Население по полу, возрасту и грамотности по переписям 17 декабря 1926 г. и 9 февраля 1897 г.»
(1897 figures recomputed by ЦСУ to 1 Jan 1927 borders - see Предисловие к IX тому, method of В.П. Ефремов).
One row = Gosplan region × census year × area (total/urban/rural) × sex × age.
Age rows include single years 0-19 with subtotals `0-4`…`15-19`, then `20-24` … `95-99`, `100+`, `unknown`, `TOTAL`.
«городское население» in 1897 follows the 1897 definition (see preface).
Row count - 10320; quality counts - {'ocr2only': 170, 'missing': 287, 'ok': 9730, 'agree': 47, 'unresolved': 86}.

Territories with total or rural observations include Tatar, Chuvash, Bashkir ASSR; Mari, Votyak AO; Karelian ASSR; gubernias of
Orenburg, Penza, Samara, Ulyanovsk, Saratov, Astrakhan, Stalingrad, Vyatka, Nizhny Novgorod; Ural oblast (areas only,
no ethnic breakdown). Printed ethnic categories include Russians, Tatars (incl. Kryashens/Mishars where noted), Chuvash, Mordva,
Mari, Votyaks, Bashkirs, Mishars, Ukrainians, Germans, Kazakhs («казаки»), Karelians/Finns/Veps, Others.
`group_type`: all / russian / titular (group in its own unit) / minority (non-Russian group outside its unit or without
one) / other.

### tableIX_region_quality.csv
Share of confirmed cells (ok/agree/manual) per unit × area. Units below 0.8 (Penza rural, Astrakhan rural, Samara,
Nizhny Novgorod) come from faded scans: single-year rows for ages 50+ there should be used with care; cohorts ≤49 sit
on the left page of each spread and are generally clean.

### tableIX_cohort_gaps.csv
Titular vs Russian literacy (%) by age band and sex, area = total; gap = Russian − titular (percentage points).

### korenizatsiya_panel.csv
Literacy (%) by region × area × ethnic group × sex × age band (8-11, 12-14, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59,
60+) with `titular_unit` (group observed inside its own republic/oblast) and `has_unit_1926` (group had a titular unit in
1926; Mordva did not). Cells with population < 200 dropped.

### region_keys.csv
Crosswalk 1926 unit → Gosplan region (Table XV) → pre-1917 provinces (Malein `province_rus`) → 2010 census subject.

### crosswalk_1897_districts_to_1926_units.csv / baseline_pre1917_by_region1926_v2.csv / crosswalk_validation_vs_tableXV.csv
Uezd-level crosswalk (expert v1, population fractions for split uezds) from Malein/Dower districts to the six republics;
population-weighted baselines; validation against the ЦСУ 1897 recomputation (Bashkir ASSR: female 10.9 vs 10.8,
male 23.0 vs 22.8). `lit_m_1897_derived = 2·share_lit·100 − per_lit_f`; Dower's `mliteracy_1897` is not census male
literacy and is excluded.

### tableXV_linked_cohorts.csv
Same birth cohorts in 1897 and 1926 (born 1858-67, 1868-77, 1878-87) by Gosplan region × area × sex: literacy in both
censuses, gain in pp, cohort survival ratio.

## Validated census files
The analysis uses the validation rules implemented in `scripts/build_1926_v2.py`. Raw OCR agreement alone is insufficient. The same misreading can occur in a single-year row and its printed subtotal. Validation tiers and source-choice flags are defined below.

### tableIX_five_year_groups_validated.csv
One row = region × area × group × sex × five-year group (ages 5 and over). `P_pop`, `P_lit` printed subtotal; `S_pop`, `S_lit`
sum of the five single years; `val_pop`, `val_lit` the validated figure; `tier_pop`, `tier_lit` and `tier` use these codes.
1 = printed subtotal equals the sum of single years (within 2 persons or 0.5 %), 2 = chosen by an identity of the table
(urban + rural = total; nationalities sum to the whole population), 3 = chosen by consistency with the two adjacent
cohorts, 0 = dropped. `src_*` records the source choice. `PS` both agree, `P` printed subtotal taken, `S` sum taken, `I` value implied by two identities,
`X` removed by the neighbour rule (literacy more than 25 points from both adjacent groups, or population more than three
times or less than a third of both).

### tableIX_single_years_validated.csv
One row = single year of age with `valid` (its five-year group is validated and the validated figure is the sum of the
single years) and `tier5`.

### tableIX_bands_validated.csv
The age bands used in the paper (8-11, 12-14, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60-69, 60+), built from validated
groups or validated single years, after the plausibility rules (population per year of age above 2.5 times the median of
the series; literacy more than 30 points from both adjacent bands; series with fewer than three bands; cells below 200
persons). Fields are region, area, group, sex, band, population, literate, literacy, tier, group_type.

### Derived analysis files
`korenizatsiya_panel.csv`, `russians_by_region.csv`, `russians_region_baseline.csv`, `mechanism_panel.csv`,
`mechanism_panel_clean.csv`, `tableIX_cohort_gaps.csv`, `linked_cohorts_1926_1939.csv` (cohorts of 1926 built from validated
single years; two placebo cohorts aged 48-52 and 53-57 added). The versions built before validation are in
`v1_before_validation/`. Note that "Уральская обл." in the raw file is the sum of its sixteen okrugi and is excluded from
every sample, so that the number of distinct units is 44.

The file `russians_region_baseline.csv` requires two sample restrictions.
1. For the nine units whose volumes give no rural pages (Kalmyk AO, Komi-Permyak, Perm, Sverdlovsk, Tyumen and Chelyabinsk okrugi,
   Nizhny Novgorod, Orel and Tambov gubernii) the literacy columns are those of the total population. `paper_numbers.py` sets them to
   missing (`RURAL_RUS`) and uses these units in one robustness check only.
2. The pre-1917 columns (`teachers_percap_1911`, `agshare_1897`, ...) are provincial: the population-weighted mean of the districts of the
   province(s) of 1897 named in `pre1917_province` (`baseline_pre1917_by_province.csv`). All units of one province share the value,
   so regressions on them are clustered by that province group (`pg`). `teachers_percap_1911` counts the teachers of all primary schools
   (Malein's panel), not only zemstvo schools. The district-level crosswalk (`baseline_pre1917_by_region1926_v2.csv`) exists for six
   autonomous units and is not used in the regressions.

### census1959_rsfsr_edu_by_age_sex.csv
RSFSR, 1959 census, Table 7 (RGAE, f. 1562, op. 336, d. 1591-1594, via Demoscope `rus_edu_59.php`): population by area (urban, rural, total),
sex, age and level of education; `literate` = with any schooling + literate without primary schooling; `literacy` = literate per 100 persons
stating their education. Used for the three-census cohort check (keys `c3r.*`, `c3t.*`, Table 9 of the paper).

## External data joins
- Malein `panel1879_1911.dta`: key `province_rus` (lower-case Russian); district-level baseline (`share_lit`, `per_lit_f`,
  `share_old_beleivers1867`, `share_muslim1867`, schooling variables). Aggregate districts to `pre1917_provinces_malein`
  (population-weighted with `pop_all`) or map districts to 1926 units with the GIS file (`Id` = `Distr_ID`).
- Dower-Finkel-Gehlbach-Nafziger `data_from_gelbach.dta`: key `province_rus`; `lingfrac_1897`, `sh_russian_1897`.
- 2010 census Vol. 4 (Rosstat): key `subject_2010`; education by nationality × sex.

## Source limitations
- Karelian ASSR (T1) has the weakest OCR layer; check `quality` before using single-year rows there.
- Bashkir ASSR Table IX is printed across two page halves (36 columns); merged before checksum repair.
- 1897 pages of Table XV (columns 13-24) were extracted with an explicit column start; verify TOTAL rows against the scan
  if a region's `unresolved`/`missing` count is high.

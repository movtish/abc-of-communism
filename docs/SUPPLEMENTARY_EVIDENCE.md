# Additional results

## Literacy institutions in 1924

Table XVII of [Public Education in the USSR](https://istmat.org/files/uploads/22102/obrazovanie_1921-25_vyp.1_1924_god.pdf), volume XXVIII, issue 1, reports literacy schools and points on 1 January 1924. It was published in 1926. Printed pages 462-467 are PDF pages 67-69 in the downloaded 89-page section.

The transcription has thirty rows for fifteen territories, with total and rural categories. It records institutions, teachers and pupils by sex. General adult-school columns are excluded. Fourteen territories match the validated cohort aged 18-22 in 1926 for both sexes. Bashkiria lacks that cohort in the estimation input. A single Ural oblast total is not replicated across its districts.

| Rural territory | Institutions registered | Institutions surveyed | Male pupils | Female pupils | Female share |
|---|---:|---:|---:|---:|---:|
| Tatar republic | 81 | 81 | 2,156 | 298 | 12.14% |
| Votyak autonomous oblast | 99 | 97 | 2,656 | 198 | 6.94% |
| Mari autonomous oblast | 23 | 5 | 38 | 78 | 67.24% |
| Chuvash territory | 41 | 33 | 1,289 | 0 | 0.00% |
| Bashkir republic | 195 | 195 | 7,110 | 284 | 3.84% |
| Karelian republic | 8 | 8 | 92 | 57 | 38.26% |


The Mari female share covers five institutions, or 21.7 per cent of those registered. Rural coverage is 35.0 per cent in Samara and 77.3 per cent in Smolensk. Coverage refers to institutions surveyed. Pupil counts refer to a date and give neither unique graduates nor the proportion of illiterate adults taught. The Chuvash zero applies to the surveyed institutions.

Pupil totals agree with the sex sums. The Bashkir total teacher count is 349, while the sex sum is 346; the rural row agrees exactly. The residual of three is preserved because its cause is unknown. The 1924 Chuvash unit is an autonomous oblast. A boundary check omits Chuvash and Orenburg, without assuming full harmonisation elsewhere.

## Institutions and later cohort gains

The outcome is the female-minus-male literacy gain between 1926 and 1939 in the matched cohort. Female pupil-share and teacher-share models control for the initial male-minus-female literacy gap. Their coefficients refer to a ten-point increase in the female share. Institution and teacher-count models use base-two logarithms and also control for cohort population. That population measures territory size, rather than everyone eligible for literacy instruction.

Models use equal territory weights and cohort-population weights. There are fourteen territories in the full sample, eleven above 80 per cent survey coverage and nine after the boundary exclusions. Inference clusters by 1939 territory and reports CR2/Satterthwaite intervals, a restricted wild bootstrap and leave-one-cluster-out estimates.

| Predictor with equal weights | Territories | Coefficient | CR2 95% interval | Wild-bootstrap p |
|---|---:|---:|---:|---:|
| Female pupil share, ten points | 14 | 0.11 | [-3.79, 4.01] | 0.8470 |
| Same predictor, coverage at least 80% | 11 | -1.34 | [-6.50, 3.83] | 0.3506 |
| Female teacher share, ten points | 14 | -1.53 | [-3.47, 0.41] | 0.0526 |
| Same predictor, coverage at least 80% | 11 | -1.55 | [-4.78, 1.67] | 0.3330 |
| Doubling the number of institutions | 14 | -1.53 | [-5.58, 2.51] | 0.1592 |
| Same predictor, coverage at least 80% | 11 | -1.07 | [-8.11, 5.98] | 0.5566 |
| Doubling the number of teachers | 14 | -0.88 | [-2.53, 0.77] | 0.0175 |
| Same predictor, coverage at least 80% | 11 | -1.45 | [-9.38, 6.49] | 0.6592 |


All twenty-four CR2 intervals include zero. Some bootstrap probabilities are below 0.05, but the results vary with sample and weighting choices. Tests were exploratory. The early date, small samples, unknown pupil ages and endogenous institutional placement limit their interpretation. These regressions do not measure the expansion of instruction during the 1930s.

## Age priorities in 1931

The [1931 national economic plan](https://istmat.org/files/uploads/52124/plan_sssr_na_1931_god.pdf) specifies ages 16-50 in towns and 16-40 in rural areas, with some instruction above 40 in collectivised areas. It also records substantial non-completion, so planned contingents cannot be counted as graduates.

People aged 33-37 in 1926 straddle 40 in 1931. The omission check removes this intermediate cohort. The younger group remains aged 18-32 and the older group 48-57.

| Sample | Intermediate cohort 33-37 | Female contrast, points | CR2 95% interval | Triple difference |
|---|---|---:|---:|---:|
| Main | Included | 20.354 | [16.679, 24.028] | 14.379 |
| Main | Omitted | 20.312 | [16.606, 24.019] | 14.377 |
| Without Ural districts | Included | 20.377 | [16.551, 24.203] | 14.481 |
| Without Ural districts | Omitted | 20.338 | [16.481, 24.194] | 14.479 |


The eight estimates change little. This check does not establish that the older comparison group was untreated.

## Regional cohorts in 1959

The [education workbook](https://www.demoscope.ru/weekly/ssp/rus_edu_59.xls) supplies 20,025 observations from 89 territorial entries, 25 age rows and nine residence-by-sex categories. National totals and nested territories cannot be summed together. Four additional Leningrad working blocks are excluded.

For ages nine and above, literacy equals population minus unknown education minus illiterates, divided by population minus unknown education. A blank component is treated as zero only when the known nonnegative components exhaust the total. Blank flags remain in the extraction. The all-age row includes children under nine and has no calculated literacy rate.

The extraction passes 18,423 component identities, 13,350 population identities and 9,897 comparisons with four regional HTML tables. Another 144 numeric inputs from seventy-two 1939 cells agree with the downloaded source tables. These checks test transcription and arithmetic, while historical census accuracy remains a separate question.

The comparison follows ages 30-34, 35-39 and 40-44 in January 1939 to ages 50-54, 55-59 and 60-64 in January 1959, with fixed 1939 population weights. These cohorts overlap with the paper's ages 20-34 in December 1926, but are not identical.

The core sample covers Tatar, Bashkir, Chuvash, Mari and Udmurt republics. An extended sample adds Komi, Mordovian, Yakut and Buryat republics. Karelia is excluded over boundary concerns. Small transfers remain unresolved in the retained territorial cores.

| Core five republics | Women, points | Men, points |
|---|---:|---:|
| Total population | 2.07 | 3.00 |
| Rural population | 3.78 | 3.49 |
| Urban population | -8.10 | -0.32 |


With republic and age-group effects and population weights, the five-republic urban female-minus-male change is -7.66 points. Its CR2 interval is [-12.48, -2.83]. Enumerating all 32 wild-bootstrap sign vectors gives p = 0.0625. Both results are reported. The nine-republic estimate is -7.86 points, with CR2 interval [-10.88, -4.84] and bootstrap p = 0.00390625.

Urban female literacy declines in all nine republics. Successive cohort populations contain different people. In Tatar towns, the female cohort population reaches 120.9 per cent of its 1939 size. Migration, settlement reclassification, boundaries and enumeration must therefore enter the comparison. War, selective survival, further learning and skill loss may also contribute. The data do not identify individual losses of literacy or a bound on 1939 misreporting.

## Contextual material

Migration extracts and a 1923 Voronezh time-use survey describe possible channels. The survey covers 29 households and 71 budgets, too few to represent Soviet households as a whole.

Downloaded adult-school and political-education sections chiefly report union-republic aggregates. They provide no comparable regional panel of attendance, completion and enforcement during 1926-1939. [SOURCES.md](SOURCES.md) records the publications, downloaded files and access limits. Both supplementary folders include inputs, complete model output and fixed seeds.

# Further evidence on the literacy campaign

## Literacy institutions on 1 January 1924

The new institutional data come from Table XVII of [Public Education in the USSR](https://istmat.org/files/uploads/22102/obrazovanie_1921-25_vyp.1_1924_god.pdf), Central Statistical Administration, volume XXVIII, issue 1, published in 1926. Printed pages 462-467 correspond to PDF pages 67-69 in the downloaded 89-page section. The table reports literacy schools and points, their teachers and their pupils by sex, with rural areas shown separately. Adjacent columns for general adult schools are not included.

Thirty rows have been transcribed and checked against the page images, covering fifteen territories and two residence categories. Fourteen territories can be linked to the youngest validated cohort, aged 18-22 in 1926, for both sexes. The Bashkir republic appears in the institutional transcription but lacks that validated cohort in the estimation input. The Ural districts are not assigned duplicate observations from a single oblast total.

| Rural territory | Institutions registered | Institutions surveyed | Male pupils | Female pupils | Female share |
|---|---:|---:|---:|---:|---:|
| Tatar republic | 81 | 81 | 2,156 | 298 | 12.14% |
| Votyak autonomous oblast | 99 | 97 | 2,656 | 198 | 6.94% |
| Mari autonomous oblast | 23 | 5 | 38 | 78 | 67.24% |
| Chuvash territory | 41 | 33 | 1,289 | 0 | 0.00% |
| Bashkir republic | 195 | 195 | 7,110 | 284 | 3.84% |
| Karelian republic | 8 | 8 | 92 | 57 | 38.26% |

The Mari female share describes five institutions, only 21.7 per cent of the registered rural network. Rural survey coverage is 35.0 per cent in Samara and 77.3 per cent in Smolensk. Survey coverage measures institutions, not the proportion of illiterate adults taught. The Chuvash zero applies to the surveyed institutions and cannot establish that no woman received instruction elsewhere.

Every pupil total equals the sum of the reported sexes. The total Bashkir teacher count is 349, while male and female counts sum to 346. The difference of three is preserved. General source notes warn of incomplete sex allocation, but the cause of this particular residual cannot be established from the table. The rural Bashkir teacher row sums exactly.

Territorial keys connect records across sources; they do not certify unchanged borders. In particular, the Chuvash unit is an autonomous oblast in the 1924 source. The additional boundary filter omits Chuvash and Orenburg as known concerns. It is not full harmonisation of the remaining units.

## Do early institutions predict later gains?

The outcome is the female-minus-male literacy gain in the same cohort between 1926 and 1939. Models of the female shares of pupils and teachers control for the initial male-minus-female literacy gap. Coefficients refer to a ten-point increase in the female share. Models of institution and teacher counts use logarithms to base two and also control for cohort population. This population is a territory-size covariate, not the full population eligible for literacy instruction.

Each model is estimated with equal territory weights and with cohort-population weights. The full sample has fourteen territories. A survey-coverage threshold of 80 per cent leaves eleven; the additional boundary filter leaves nine. Inference clusters on the later-census territory and reports CR2/Satterthwaite, a restricted wild bootstrap and leave-one-cluster-out estimates.

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

All twenty-four CR2 intervals include zero. Some individual bootstrap probabilities are below 0.05, but the finding does not survive the changes in sample and weights. No confirmatory family of tests was specified in advance. Selecting an isolated small probability would not establish a mechanism.

The absence of a stable relationship does not show that instruction had no effect. The sample is small, the snapshot is early, pupil ages are unknown and institutions were not allocated at random. The data do not measure the network built in the 1930s. They are a direct but limited check of early institutional correlates, not a causal mediation analysis.

## The age priorities of 1931

The [national economic plan for 1931](https://istmat.org/files/uploads/52124/plan_sssr_na_1931_god.pdf) specifies ages 16-50 in towns and 16-40 in the countryside, with some instruction above 40 in collectivised areas. It also reports substantial non-completion among those covered. Planned contingents must not be read as graduates.

The cohort aged 33-37 in 1926 straddles 40 by 1931. It belongs to the model's intermediate group. Omitting it gives the following sensitivity check. The younger group remains aged 18-32 in every row, and the older group remains 48-57.

| Sample | Intermediate cohort 33-37 | Female contrast, points | CR2 95% interval | Triple difference |
|---|---|---:|---:|---:|
| Main | Included | 20.354 | [16.679, 24.028] | 14.379 |
| Main | Omitted | 20.312 | [16.606, 24.019] | 14.377 |
| Without Ural districts | Included | 20.377 | [16.551, 24.203] | 14.481 |
| Without Ural districts | Omitted | 20.338 | [16.481, 24.194] | 14.479 |

The eight estimates show little sensitivity to this intermediate cohort. They do not establish an untreated older comparison group. Earlier supplementary labels incorrectly called this a narrowing of the younger group. The code, CSV metadata, manuscript and documentation now describe the omission correctly.

## Regional literacy in 1959

The [downloaded education workbook](https://www.demoscope.ru/weekly/ssp/rus_edu_59.xls) yields 20,025 observations, comprising 89 territorial entries, 25 age rows and nine residence-by-sex categories. The entries include the RSFSR total and nested units, so they cannot all be summed. Four extra Leningrad working blocks are excluded.

Literacy for ages nine and above is calculated as the share literate among those with reported education. The numerator is population minus unknown education minus illiterates; the denominator is population minus unknown education. Blank educational components are interpreted as zero only where known nonnegative components exhaust the total exactly. Source blank flags are retained. Literacy is not calculated for the all-age row, which includes children under nine.

There are 18,423 component identities, 13,350 population identities and 9,897 numerical comparisons between four HTML tables and the workbook. All agree. Seventy-two 1939 age-sex-area cells, containing 144 numeric inputs, also agree with freshly downloaded source tables. These checks validate extraction and accounting, not the historical accuracy of the census.

The follow-up matches ages 30-34, 35-39 and 40-44 in January 1939 to ages 50-54, 55-59 and 60-64 in January 1959. No interpolation is needed. Age composition is fixed at 1939 weights. The groups overlap with, but do not exactly reproduce, the paper's ages 20-34 in December 1926.

The core sample contains Tatar, Bashkir, Chuvash, Mari and Udmurt republics. Karelia is excluded because of boundary concerns. An extended sample adds Komi, Mordovian, Yakut and Buryat republics. Same-name territorial cores have been matched; small transfers have not been fully harmonised.

| Core five republics | Women, points | Men, points |
|---|---:|---:|
| Total population | 2.07 | 3.00 |
| Rural population | 3.78 | 3.49 |
| Urban population | -8.10 | -0.32 |

An exploratory population-weighted regression with republic and age-group effects estimates an urban female-minus-male change of -7.66 points. The CR2 interval is [-12.48, -2.83], while enumerating all 32 wild-bootstrap sign vectors gives p = 0.0625. The methods disagree at the conventional five-per-cent threshold, and both are reported. The corresponding nine-republic urban estimate is -7.86 points, with a CR2 interval of [-10.88, -4.84] and bootstrap p = 0.00390625.

The urban female rate declines in all nine republics. That does not mean that the same women lost literacy. In the Tatar republic the female urban cohort population is 120.9 per cent of its 1939 size by 1959. Migration, settlement reclassification, boundaries or enumeration must enter the comparison. War, selective survival, further learning and possible skill loss add other components. These are descriptive changes in successive cohort populations, not linked individual transitions or a bound on 1939 misreporting.

## Other material and the remaining gap

The supplementary folder also contains contemporary migration extracts and a small 1923 Voronezh time-use survey. Its 29 households and 71 budgets cannot represent all Soviet households. The material helps specify possible channels; it cannot identify their effects in the main census sample.

Later statistical sections on adult schools and political education were downloaded, but their pupil tables chiefly report union-republic aggregates. They did not yield a comparable panel of regional exposure during 1926-1939. Some earlier volumes returned HTTP 429; repeated requests were not pursued. The gap is now specific. There is an early regional institutional snapshot and later aggregate reporting, but no harmonised panel of actual attendance, completion and enforcement during the years of the main literacy rise.

Sources and exact download status are listed in [SOURCES.md](SOURCES.md). Numerical inputs, complete model output and fixed seeds accompany both supplementary folders.

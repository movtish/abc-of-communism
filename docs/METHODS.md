# Data and methods

## What the estimates establish

The paper documents a large rise in the recorded literacy of adult female birth cohorts between the censuses of 1926 and 1939. It follows cohorts, not named individuals. Changes in their literacy combine learning with mortality, migration, territorial change and differences in enumeration. The campaign is a plausible explanation for much of the rise, but the census comparison alone cannot assign a separate effect to enforcement, household decisions or private returns.

The main female younger-minus-older contrast is 20.3537 percentage points. Its CR2 interval is [16.6792, 24.0282]. The triple difference is 14.3791 points, with an interval of [9.7385, 19.0197]. These estimates answer different questions. The first compares younger and older women. The second subtracts the corresponding contrast for men, who also received instruction.

## Correcting the territorial scope of 1939

The population and illiteracy tables do not use the same boundaries for Moscow and Leningrad. The age table includes each city within its oblast. The illiteracy table lists the city separately, with the oblast excluding it. Joining the two oblast names without adjusting their scope understates illiteracy outside the cities. Adding cities again to regional totals also counts their population twice.

The corrected data subtract each city's population from its oblast before joining the tables. Cities then enter larger aggregates once, as separate territories. The correction changes 224 urban and total-population rows. Rural rows are unchanged. The Moscow oblast population becomes 4,780,293 after subtracting Moscow's 4,137,018 from 8,917,311. The corresponding Leningrad calculation is 6,432,052 minus 3,191,304, leaving 3,240,748.

The underlying source pages were checked against 88 pairs of population and illiteracy values. This establishes the scope error in the join rather than a failure of regression arithmetic. The saved pages and the cell comparisons are in `validation/`.

| Quantity | Earlier version | Corrected version |
|---|---:|---:|
| Literacy in 1939 of female cohorts aged 20-34 in 1926, total population | 70.23% | 69.67% |
| Net equivalent of newly literate women, cohorts aged 20-49 in 1926 | 2.733 million | 2.552 million |
| Corresponding figure for men | 1.076 million | 1.055 million |
| Adult-learning equivalent without subtracting the older cohort, Russian article | 4.235 million | 3.996 million |
| Same calculation after subtracting the older-cohort change | 3.097 million | 3.627 million |
| Correlation of normalised gain with urbanisation, total population | 0.50 | 0.12 |

The resulting counts are accounting equivalents of net changes. They are not a count of identified graduates. The scope correction does not harmonise every territorial transfer between 1926, 1939 and 1959.

The full extraction also retains 17 inconsistent cells in which illiterate counts exceed population. All are open-ended 70+ groups of nested territories. They are listed in `validation/1939_unresolved_70plus_cells.csv`. They enter neither the matched age windows nor national aggregates, which exclude nested territories. Their original values are preserved pending a source-level resolution.

## Cohort comparisons

The main younger group is aged 18-32 in 1926. Intermediate cohorts are aged 33-47 and have their own coefficients. The older comparison group is aged 48-57. Observations are weighted by cohort population in 1926. Units that share a later-census territory share a cluster.

Let DD_F denote the younger-minus-older change for women and DD_M the same contrast for men. A female campaign effect can be read from DD_F only if older women were unaffected and the counterfactual age difference in learning, selection and reporting was absent after conditioning. Those assumptions concern much more than mortality. The triple difference, DD_F minus DD_M, instead requires equality of the relevant counterfactual age difference between sexes. Even if valid, it identifies a relative effect by sex, not the total effect on women. [Olden and Moen](https://doi.org/10.1093/ectj/utac010) explain this distinction.

The older cohorts were not guaranteed to be untreated. Age priorities changed across years and places. The 1931 plan targets ages 16-50 in towns and 16-40 in rural areas, with some instruction above 40 in collectivised areas. Omitting the intermediate cohort aged 33-37 in 1926, which straddles 40 by 1931, changes the female contrast to 20.3122 points. The younger group remains 18-32 in both models. Earlier supplementary labels incorrectly described this as narrowing the younger group from 18-37 to 18-32. The labels and manuscript explanation have been corrected; the eight numerical estimates are unchanged.

The regional sample uses three fifths of one later five-year age group and two fifths of the next. That interpolation supplies a wider geographical comparison, but it is less exact than matching validated single years. Different samples need not estimate the same population contrast.

## Inference with few clusters

The independent inference module reports CR1, CR2 with contrast-specific Satterthwaite degrees of freedom, a cluster jackknife and a restricted wild cluster bootstrap. The working CR2 covariance is defined after weighting. Population weights define the estimand; they are not assumed to be inverse census sampling variances.

CR1 uses the rank of the design and a t reference distribution with G minus one degrees of freedom. CR2 checks that its working variance can be recovered. A contrast is withheld if cluster leverage leaves its score in an uncorrectable null direction. Jackknife results are withheld when deleting a cluster destroys identification. The expected unidentified specification is recorded in `methodology/results/errors.json`, rather than presented as an estimate.

The wild bootstrap imposes the scalar null in the full design and refits the nuisance effects. For larger cluster counts it uses fixed seeds and 9,999 draws. For sufficiently small cluster counts the independent module enumerates all Rademacher sign vectors. Complete enumeration removes Monte Carlo sampling of those vectors; it does not make the observational comparison an exact causal randomisation experiment.

The tests compare CR1 with statsmodels, CR2 with HC2 when each cluster is a singleton, and the restricted bootstrap with explicit refits. Graphical intervals use the relevant t critical value. Weighted cohort-mean errors use weighted cluster contributions. The original paper inference and these independent checks remain separately identifiable in the files.

Small-cluster and leverage concerns follow [MacKinnon, Nielsen and Webb](https://doi.org/10.1016/j.jeconom.2022.04.001) and [Pustejovsky and Tipton](https://arxiv.org/abs/1601.01981). The latter authors' [theorem correction](https://jepusto.com/posts/Pusto-Tipton-2018-Theorem-2/) is relevant to the handling of fixed effects and singular adjustment matrices.

## Mechanisms and accounting

The historical male learning probability spans about thirty years, while the campaign comparison spans twelve. Transporting the earlier probability to men not reached by the later state is an assumption, not an independent test of the household mechanism. A shorter-exposure illustration is supplied in `methodology/results/mixture_duration.csv`.

Regional urbanisation is an outcome of the same period as literacy. A regression on it cannot by itself distinguish returns to literacy from migration selection or common regional change. A small or imprecise coefficient does not establish equivalence to zero. The equivalence diagnostics use an explicit five-point margin and remain exploratory.

The normalised gain, change in literacy divided by initial illiteracy, is a net cohort outcome. It is not the observed probability that an initially illiterate person learned. The selection accounting therefore reports conditional scenarios, not estimated migration. Net population loss cannot bound gross selective flows when inflows and outflows compensate one another. Ratios above one also rule out treating every later-to-earlier population ratio as survival.

The 1959 census confirms high literacy in later populations belonging to the relevant birth cohorts. It does not date every acquisition of literacy to the campaign. Similar national rates in 1939 and 1959 cannot bound earlier misreporting without restrictions on subsequent learning, mortality, migration, skill loss and borders. The regional follow-up illustrates these components rather than eliminating them.

The 2010 ethnic correlations are likewise descriptive. They do not connect a particular descendant to an adult taught in the 1930s. Nationality-level shocks, schools, urban settlement and selection can produce the same association. Alternative clustering and exploratory multiplicity adjustments are included, without claiming that the analysis was preregistered.

## What remains to be collected

A stronger causal design needs harmonised territories, earlier measurements of the same cohorts and variation in actual implementation that has a defensible source. Useful records would identify opening dates, attendance, completion, teachers and enforcement during the years of the largest gains. More classes or spending alone need not be exogenous, since resources may respond to illiteracy.

The available 1924 survey provides an early regional snapshot. It does not supply a panel of actual exposure during 1926-1939. Linking literacy to occupations, migration or family members would also require more detailed records than the present census aggregates. The code and additional regressions cannot supply those missing comparisons.

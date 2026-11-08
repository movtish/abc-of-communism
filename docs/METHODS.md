# Data and estimation

## Cohorts and outcomes

The census comparisons follow birth cohorts across repeated cross-sections. A change in recorded literacy combines learning, mortality, migration, boundary changes and enumeration. Individual transitions are unobserved.

The main younger-minus-older contrast for women is 20.3537 percentage points, with a CR2 95 per cent interval of [16.6792, 24.0282]. Subtracting the corresponding contrast for men gives a triple difference of 14.3791 points, with an interval of [9.7385, 19.0197]. Men also received instruction, so the triple difference measures a relative effect by sex under its identifying assumptions.

In 1926, the younger group is aged 18-32, the intermediate group 33-47 and the older group 48-57. Models include separate intermediate-cohort coefficients and use 1926 cohort-population weights. Units sharing a 1939 source territory share a cluster.

A campaign interpretation of the female contrast requires unaffected older women and no conditional counterfactual age difference in learning, selection or reporting. The triple difference instead requires equality of that age difference between sexes. See [Olden and Moen](https://doi.org/10.1093/ectj/utac010).

The older group may include participants. The 1931 plan gives priority to ages 16-50 in towns and 16-40 in rural areas, with some instruction above 40 in collectivised areas. Omitting ages 33-37 in 1926 changes the female contrast to 20.3122 points. The younger group stays aged 18-32.

The regional comparison uses three fifths of one later five-year age group and two fifths of the next. This extends geographical coverage at the cost of less exact cohort matching.

## Territorial scope in 1939

The age tables include Moscow and Leningrad within their oblast populations. The illiteracy tables list each city separately and exclude it from the corresponding oblast. The join subtracts each city's population before matching the oblast records, then counts the city once in larger aggregates.

Moscow oblast therefore has 4,780,293 people after subtracting 4,137,018 from 8,917,311. The Leningrad calculation subtracts 3,191,304 from 6,432,052, leaving 3,240,748. The correction affects 224 urban and total-population rows. Rural rows are unchanged. Saved source pages and 88 paired population and illiteracy comparisons are in `validation/`.

| Quantity | Earlier version | Corrected version |
|---|---:|---:|
| Literacy in 1939 of female cohorts aged 20-34 in 1926, total population | 70.23% | 69.67% |
| Net equivalent of newly literate women, cohorts aged 20-49 in 1926 | 2.733 million | 2.552 million |
| Corresponding figure for men | 1.076 million | 1.055 million |
| Adult-learning equivalent without subtracting the older cohort, Russian article | 4.235 million | 3.996 million |
| Same calculation after subtracting the older-cohort change | 3.097 million | 3.627 million |
| Correlation of normalised gain with urbanisation, total population | 0.50 | 0.12 |

These counts are accounting equivalents of net changes in cohort literacy. Individual graduates cannot be counted from the census aggregates.

Seventeen source cells report more illiterates than people. All concern nested territories and open-ended ages 70+. Their values remain in `validation/1939_unresolved_70plus_cells.csv`; they enter neither the matched age windows nor national aggregates. The territorial correction leaves some smaller boundary transfers unresolved.

## Cluster inference

`methodology/inference.py` calculates CR1, CR2 with contrast-specific Satterthwaite degrees of freedom, a cluster jackknife and a restricted wild cluster bootstrap. Population weights define the estimand. They are not treated as inverse census sampling variances.

CR1 uses the design rank and a t distribution with G minus one degrees of freedom. CR2 checks recovery of the working variance after weighting. The module withholds a contrast when cluster leverage leaves an uncorrectable score direction, and withholds jackknife results when a cluster deletion destroys identification. `methodology/results/errors.json` records the expected unidentified specification.

The bootstrap imposes the scalar null in the full design and refits nuisance effects. Larger samples use 9,999 draws with fixed seeds. Small samples enumerate all Rademacher sign vectors. Enumeration eliminates simulation error over those vectors, but does not make treatment assignment random.

`methodology/test_inference.py` compares CR1 with statsmodels, CR2 with HC2 for singleton clusters, and the restricted bootstrap with explicit refits. Figure intervals use the appropriate t critical values. Errors for weighted cohort means use weighted cluster contributions.

The inference follows [MacKinnon, Nielsen and Webb](https://doi.org/10.1016/j.jeconom.2022.04.001) and [Pustejovsky and Tipton](https://arxiv.org/abs/1601.01981), including the latter authors' [correction for singular adjustment matrices](https://jepusto.com/posts/Pusto-Tipton-2018-Theorem-2/).

## Selection and mechanisms

Normalised gain divides the literacy change by initial illiteracy. It describes a net cohort outcome. Interpreting it as an individual learning probability requires restrictions on selection and reporting.

The historical male comparison spans about thirty years, while the campaign comparison spans twelve. Applying the earlier learning probability to men outside the later state programme assumes that it can be transported across periods. `methodology/results/mixture_duration.csv` gives a shorter-exposure illustration.

Urbanisation and literacy change over the same period. Their regional association can reflect returns to literacy, migration selection or common changes. Equivalence checks use a five-point margin; an imprecise coefficient alone cannot establish equivalence to zero.

Selection accounting reports conditional scenarios for mortality and migration. Compensating inflows and outflows prevent net population loss from bounding gross selective flows. Later-to-earlier population ratios above one also preclude reading every ratio as survival.

The 1959 follow-up records later literacy in the same birth cohorts. Subsequent learning, migration, mortality, skill loss and boundary changes prevent it from dating all gains to the campaign or bounding 1939 misreporting. The 2010 ethnic correlations are also descriptive. They cannot link particular descendants to adults taught in the 1930s. Alternative clustering and exploratory multiplicity adjustments are reported.

## Missing evidence

A stronger causal design needs harmonised territories, earlier observations of the same cohorts and defensible variation in campaign implementation. Records of opening dates, attendance, completion, teachers and enforcement would help distinguish channels. Resources allocated in response to illiteracy would still require an identification argument.

The 1924 survey supplies an early institutional cross-section. A comparable exposure panel for 1926-1939, and records linking literacy to occupations, migration or family members, remain unavailable in this repository.

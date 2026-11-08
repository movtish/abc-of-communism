> Session record of September–October 2026 (status, decisions, open tasks, archive of the working folder): see `SESSION_NOTES_2026-09_10.md` and `archive/session_workspace_2026-09_10/`.

# The ABC of Communism: How Soviet Russia Taught Its Women to Read
Author: Mark Kreshchuk (New Economic School; Moscow State University).
State of the project: revision 12 (7 October 2026), the SHORT FOCUSED VERSION written after the mentor's (Gerhard's) comments: about 5,200 words of main text, five exhibits (three figures, two tables), 19 pages with references, followed by an online appendix of 45 pages (65 pages in all). Revision 11 (the long version, 63 pages, former title "The State, the Household and the Allocation of Literacy in Soviet Russia") is archived in `paper/drafts/ABC_of_Communism_rev11_long.tex|pdf`. The UCLouvain "Soviet Legacy" workshop rejected an earlier version on 23 September 2026; conferences are listed at the end of this file.

## Revision 12 (7 October 2026): what the mentor asked for and what was done
The comments, in substance: (1) make sure the result is new; (2) be far more concise, the argument is "female education: huge and quick", about 5,000 words and 5 figures or tables, everything else to the appendix; (3) decide what the paper is to be cited for, state it precisely and repeatedly, and have ONE main picture in which the cohort that benefited is set against the most plausible counterfactual; (4) "the state" does not do justice to the Soviet system; engage with Engels, The Origin of the Family, Private Property and the State (1884), possibly as an epigraph and as the motivation of the theory.
- **The claim to be cited for** (abstract, first paragraph, results, conclusion): the literacy of rural women aged 20-34 in 1926 rose from 42.6 to 60.7 per cent by 1939 and stood at 60.1 in 1959 (a third of the illiterate learned as adults in twelve years); the women of the same ages in 1897 went from 10.3 to 8.3 per cent in thirty years.
- **The main picture** (`fig25_main_cohorts`, Figure 1): literacy of rural women by year of birth as recorded by the censuses of 1897, 1926, 1939 and 1959, each with its own five-year groups (nothing interpolated). The lines of 1897 and 1926 coincide, the line of 1939 leaves them for the cohorts under the age limit, the points of 1959 lie on 1939.
- **Exhibits**: Figure 1 (main picture); Table 1 (`tab_main`: the same cohorts at two censuses, campaign and thirty years before; effect on women 20.4 (1.7) points, 37.2 (2.1) per cent of the illiterate; men 6.0 (1.3); women minus men 14.4 (2.1)); Figure 2 (`fig27_taught_periods`: share of the illiterate who learned by age and sex in both periods); Figure 3 (`fig28_regions`: the cohort in each of the 17 regions, gains of 9 to 45 points, all positive); Table 2 (`tab_robust`: the effect on women across samples, 18.0 to 21.5 points in units, 14.6 in the 17 regions with cohorts two years older; Russian units 20.7 (2.0), autonomous units 20.5 (3.4)).
- **Engels and the doctrine**: epigraph from The Origin of the Family; Section 2.1 "From Engels to the ABC of Communism" (Engels's diagnosis and remedy; The ABC of Communism, sections 79 and 84, translated from the Russian text; Lenin 1919 and 1921; the preamble of the decree; the poster of 1923 by Kruglikova, in which a schoolgirl tells her mother she could have helped had she been literate); Section 3 states the argument as two conditions and answers whether the externality model fits Soviet thinking: the political return named in the decree is sufficient, the campaign also used the argument from children, the data cannot tell the two apart.
- **Novelty check** (web search, 7 October 2026): no cohort-linked measurement of the campaign was found. Nearest work: Zharkov (2024, Sverdlovsk oblast, compares age groups, not cohorts), Pavlova (2006, candidate dissertation on Orenburg), Glushchenko (2015, cultural history). All three are cited. The statement in the paper is "I know of no measurement on linked cohorts"; the JEL survey (Zhuravskaya, Guriev and Markevich 2024) is cited but its text was not read in full. The user decided NOT to write to Malein or Markevich.
- **Moved to the online appendix** (`paper/appendix.tex`, assembled from revision 11 and then edited): data and validation (A), the model (B), estimating equations (C), the two periods cohort by cohort with robustness and the three-census table (D, E), regional predictors and titular units (F), nationalities (G), the census of 2010 (H), further tables and figures (I). The appendix keeps the terms "household regime" and "state regime" and labels the cohorts of the first period by age at the decree (age in 1897 plus 23).
- **New in the pipeline**: `paper_numbers.py` gives, for every sample of the state regime, the effect on each sex from one pooled regression (keys `.pw .pm .pd` in points, `.tw .tm .td` in the share taught; also `ray.*`, `rayx.*` for regions; a new sample `w2r.tit`, autonomous units only), the means of Table 1 (`t1s.*`, `t1h.*`), the cohort profiles of the four censuses (`cpr.*`, `cpt.*`), the cohort aged 20-34 in 1897 (`b4r.*`, `b4t.*`), every five-year group of 1926 in 1939 (`c4r.*`, `c4t.*`), the number who learned (`cntt.F.new` = 2.7 million women, `cntt.M.new` = 1.1 million men aged 20-49 in 1926, whole RSFSR, at the size of the cohorts in 1939) and the regional file `results/S1_region_gains.csv` (`reg.*`). The Stata do-file mirrors the new regressions: 1,074 coefficients compared, 1,072 identical, 2 not identified in either.
- **For the user to decide or check**: the new subtitle; whether to thank the mentor in the first footnote; the Engels quotations follow the standard English translation (fourth edition of 1891, International Publishers 1972) and were verified on marxists.org, while the German first edition of 1884 could not be opened, so that it is not confirmed that each quoted sentence was already in the text of 1884; the page range of Zharkov (2024) and the title of Pavlova (2006) come from web summaries.

## What the paper does (for anyone opening this folder cold)
(The list below describes the full set of results, most of which now live in the online appendix.)
The Soviet literacy campaign is used as a case of the state taking over the household's decision about who is taught to read.
The same rural birth cohorts are followed through two regimes with the censuses of 1897, 1926 and 1939, and the consequences are traced to the census of 2010.

1. **Household regime, 1897-1926** (attendance left to the household; the only institution that taught adults without its consent, the army, took men only).
   Of rural men aged 33-47 at the decree of 1919 who were illiterate in 1897, 30 % could read in 1926; of women 0 %. Triple difference -16.3 (1.5).
   The gains of men cannot be divided between the household, the army and the workplace (said so in the paper); the argument rests on the women, whom no institution reached.
2. **State regime, 1926-1939** (attendance enforced, cost borne by the state). Of illiterate women aged 18-32 in 1926, 41 % could read in 1939; of men 60 %.
   Triple difference in percentage points against the cohorts above the age limit (aged 48-57): 14.5 (2.1); 8.5 to 16.3 across samples. The state did NOT favour women: it taught the illiterate of both sexes,
   and 80 % of the illiterate were women. In the share taught the difference between women and men is -12.5 (2.7), or -10.6 (2.8) with cohort effects.
   Of the 19 points by which men exceed women, the routes open to men before the campaign (share taught under the household regime at the same ages, 18 %) account for 11.
   Rural RSFSR as a whole (17 regions, cohorts 20-34): 32 % of illiterate women and 49 % of illiterate men taught.
   Census of 1959 (three-census check, Table 9): women aged 20-34 in 1926, whole RSFSR, literacy 51.2 % (1926), 70.2 % (1939), 67.6 % (1959); rural 42.6, 60.7, 60.1.
   Measured on 1959 alone the share of illiterate women who became literate is 34 % (whole population) and 31 % (rural), against 39 % and 32 % measured in 1939. An inflation of the order of the gains is excluded; one of a few points is not.
3. **Nationalities, 1926.** Within the same unit and cohort, the gap between the Volga nationalities (Chuvash, Mari, Mordva, Votyaks) and Russians fell from 23 to 6 points among men
   and rose from 11 to 26 points among women. Pooled triple difference -15.7 (2.6). In log-odds the additional disadvantage of women is -0.46 (0.14) and its change across cohorts, -0.12 (0.10), is not distinguishable from zero.
   The source of that gendered disadvantage is not identified (the language of the school is one candidate, not a finding).
4. **Russians across units, 1926** (rural, 26 units with rural pages, 22 provinces of 1897, SE clustered by province): gender gap narrower by 4.7 (1.0) points per SD of primary-school teachers per capita in 1911.
   Fertility (child-woman ratio 1926) has the predicted sign but is NOT significant (1.5 (1.4), permutation p = 0.29) and cannot be given a direction.
5. **Legacy, 2010.** Among cohorts born before 1951 the ethnic gap in secondary education is 6.1 (2.4) points larger for women than for men; it is larger for the nationalities whose women
   stood further behind their men in 1926 (0.18 to 0.26 per point; exact permutation p = 0.119 for six nationalities, 0.004 for twelve), and it is absent among those born after 1960.
6. **Not established** (said so in the paper): the fertility channel; whether the household's predictors lost their force under the state regime (16 units, differences not significant);
   a premium of the titular republics (rests on the Tatar republic); the association with men's urban employment (rests on the weights).

## Folder layout
- `paper/` - `ABC_of_Communism.tex` (the paper: main text and, through `\input{appendix}`, the online appendix), `appendix.tex` (the online appendix), `numbers.tex` (every number quoted in the text, as macros), `tables/*.tex` (bodies of all tables), `refs.bib`, `ABC_of_Communism.pdf`.
  `numbers.tex` and `tables/` are generated; do not edit them by hand. Earlier versions are in `paper/drafts/` (`ABC_of_Communism_rev11_long.tex|pdf` is the long version of 4 October 2026; `ABC_of_Communism_v8_before_validation.tex|pdf` is the version sent to UCLouvain).
- `data/` - CSV (`;`-separated, UTF-8 with BOM): the digitised Table IX of 1926 (44 units, 90,642 cells), Vol. 9 Table XV, the 1939 census, the 2010 census tables, the pre-1917 baseline, crosswalks.
  Validated files: `tableIX_five_year_groups_validated.csv` (with the record of validation of every group), `tableIX_single_years_validated.csv`, `tableIX_bands_validated.csv`.
  The derived files of the earlier version are kept in `data/v1_before_validation/`. `CODEBOOK.md` inside.
- `scripts/` - see "Reproduce" below.
- `results/` - `paper_numbers.json|csv|txt` (all numbers with their keys), the estimation samples as CSV (`E1_...`, `W2_cells`, `D_core_cells`, `F_russians_units`, ...), `V_validation_1926.txt` (log of the validation).
  The results of the earlier version are in `results_v1_before_validation/`.
- `figures/` - fig01-fig28 (PNG 300 dpi and PDF), without titles inside the figures (captions are in LaTeX). The main text uses fig25 (main picture), fig27 and fig28; fig26 is the appendix twin of the main picture (whole population, men); fig24 is the earlier version of fig27 and is no longer used.
- `stata/` - replication package: `ABC_of_Communism.do`, `data/*.dta`, `output/` (log, `stata_results.csv`, `comparison.csv`). See `stata/README_STATA.md`.
- `jnea/` - separate Russian article for Журнал Новой экономической ассоциации on the 1926 cross-section: `article_jnea.tex`, `numbers_ru.tex`, `tables/`, `figures/ris1-3`,
  `Kreshchuk_JNEA_with_author.pdf`, `JNEA_anonymous.pdf`. It uses the same numbers as the main paper. Journal limit 40,000 characters.
- `sources/census2010/` - Rosstat xlsx tables.

## Reproduce
Use the Anaconda interpreter (`C:\ProgramData\anaconda3\python.exe`).
```
python scripts/build_1926_v2.py      # validation of Table IX; rebuilds the derived 1926 files and the link to 1939
python scripts/paper_numbers.py      # every number of the paper (about 6 minutes; --fast skips permutations and bootstraps)
python scripts/make_tables.py        # paper/tables/*.tex
python scripts/paper_figures.py      # figures/fig*.pdf
python scripts/jnea_tables.py        # jnea/tables/*.tex
python scripts/jnea_figures.py       # jnea/figures/ris*.pdf
python scripts/export_stata.py       # stata/data/*.dta
powershell scripts/build_tex.ps1     # paper/ABC_of_Communism.pdf
powershell scripts/build_jnea.ps1    # the two PDF versions of the Russian article
```
Stata: run `stata/ABC_of_Communism.do` (about one minute), then `python scripts/compare_stata.py`.
`scripts/write_numbers.py` rewrites `paper/numbers.tex` and `jnea/numbers_ru.tex` from `results/paper_numbers.json` without re-estimating anything.
Older scripts (`analysis_full.py`, `analysis_did.py`, `legacy2010.py`, `legacy_robust.py`, `demog_checks.py`, `figures.py`, `jnea_analysis*.py`) belong to the earlier version and are superseded.
The digitisation pipeline (`tab9.py`, `fix9.py`, `ocr2.py`, `assemble*.py`), `demoscope_1939.py`, `rosstat_get.py`, `wave2_rayon.py`, `maps2010.py` and `names.py` are still in use.

## How the numbers get into the text
The text contains no typed numbers. `\N{key}` prints a number of `numbers.tex`, `\NA{key}` its absolute value, `\NI{key}` and `\NIA{key}` the same rounded to integers.
The keys are listed in `results/paper_numbers.csv`. To change a specification, change it in `scripts/paper_numbers.py` and rerun; the text, the tables and the figures follow.

## Validation of the 1926 tables (what "validated" means)
Table IX prints a subtotal after every five single years of age, so every five-year figure exists twice. A group is used if
(1) the printed subtotal equals the sum of the single years (91.8 % of groups), or (2) one of the two satisfies another identity of the table (urban + rural = total; nationalities sum to the whole population; 0.9 %),
or (3) one of the two is consistent with the adjacent cohorts and the other is not (1.0 %). The rest (6.3 %) is dropped, including 39 groups that pass the identities but differ from both neighbours
by more than 25 points of literacy or by a factor of three in population. Details in Appendix B of the paper and at the top of `scripts/build_1926_v2.py`.

## What changed between the version sent to UCLouvain and revision 9
- Data: every number now comes from validated cells. Several earlier results were produced by transcription errors with large weights and are gone
  (the "mobility gap" coefficient of -6.1; the claim that school supply "no longer mattered" for the cohort aged 12-14; the change in slope of -7.9 in the two-regime test).
- Design: the state regime is now compared with true placebo cohorts (aged 48-57 in 1926, above the age limit), not with the cohort aged 43-47.
- New outcome: the share of the illiterate who were taught, which does not depend on the room left below 100 %. It shows that the state did not favour women.
- Model: a cost specific to the nationality and the state's reach e(a); five hypotheses instead of four.
- Nationalities: separate indicators for Volga and Muslim nationalities (the earlier "non-Russian" indicator mixed them and hid the result); log-odds as a check.
- Legacy: a design that compares the sexes within each nationality (Section 8.2); the qualification that the contrast between the female and the male gap in the regional regression
  rests on the comparison of Muslim with other nationalities.
- Inference as in Stata: rank-based small-sample correction, t distribution with G-1 degrees of freedom. The do-file reproduces the coefficients of `paper_numbers.py` key by key.
- Corrected facts: 44 units, not 45 (the Ural oblast row is the sum of its sixteen okrugi); 20 gubernii, not 21; rural men's literacy in 1939 is 93 %, not 90 %.

## Passes of 4 October 2026 (two referee-style re-reads; revision 10 = 60 pages, revision 11 = 63 pages)
First pass (revision 10):
- New check: the census of 1959 (Demoscope `rus_edu_59`, `scripts/demoscope_1959.py`, `data/census1959_rsfsr_edu_by_age_sex.csv`, Table 9).
- H2 corrected: the shares taught do not decline "in parallel"; comparison of the regimes on cohorts that were young adults at the start of each period (Section 7.2).
- Sample descriptions corrected: Table XV has 19 Gosplan regions, not 20; of the 29 linked units 20 have rural pages (four excluded units named in a footnote of Section 3.4); rural pages exist for 35 of the 44 units.
- Tables on nationalities and korenizatsiya and the inference and rayon figures moved to the appendix.

Second pass (revision 11, read as an economist, a demographer, a historian and a sociologist). Errors found and corrected:
- **Russians regressions mixed rural and whole-population figures.** `data/russians_region_baseline.csv` carries the whole-population figures for the nine units without rural pages. `paper_numbers.py` now masks them (`RURAL_RUS`): Table 4, Figure 5 and the unit-level household panel use the 26 to 31 rural units only; the nine others enter one robustness check (`rus.rob.all`, -4.4 (0.9)).
  Consequence: the fertility association, already marginal, is not significant (1.5 (1.4), permutation p = 0.29). The paper and the Russian article now say so; school supply is the predictor the cross-section supports.
- **Baseline was described as a district-level crosswalk; it is provincial.** Each unit carries the population-weighted mean of the districts of the province(s) of 1897 from which it was formed (41 units, 24 provinces, 227 districts). Units of one province share its values,
  so standard errors of every regression on the baseline are now clustered by province of 1897 (variable `pg`; 22 clusters in Table 4), in Python and in Stata, and the permutation of teachers is across provinces. The teacher variable is all primary-school teachers of 1911 (Malein), not "zemstvo teachers". Gregg and Nafziger's data are not used and are no longer listed as a source.
- **1959 check was shown for the rural population only.** In the whole population women's literacy of the same cohorts is 2.6 points lower in 1959 than in 1939. Table 9 is now a three-census table (1926, 1939, 1959; rural and whole population), and the text states that an inflation of a few points cannot be excluded. The 1959 table is archival (RGAE 1562/336/1591-1594), not "published".
- **Table 7, last row of panel B** mixed two regressions (49.6, 37.2, -10.6). The difference is now from the same regression (-12.5 (2.7), key `w2c.dd.dif`); -10.6 with cohort effects is given in the text.
- **Mixture reading** used the share of men taught under the household regime in cohorts that were children in 1897 (0.30). With men of the same ages (0.18) the predicted share of men is 0.52 against 0.60 observed: the earlier routes account for 11 of the 19 points; the rest means the state reached men somewhat more than women (allowed by condition (3), which now has a sex-specific reach e_s(a)). H1 and H2 restated accordingly; implied household component by age (keys `mixh.*`).
- **Army.** The first regime's gains of men coincide with exposure to military service after 1897; the text now says so (Sections 1, 3.1, 4.1, 6.1, 9, 10) and rests the argument on the women. The model treats the army as a lower cost for sons and states the unitary-household assumption.
- **History.** "Women's illiteracy named as a separate target" removed (the Central Committee resolution of 17 May 1929 set priorities by class, not by sex, which supports "the state did not favour women"); target ages of the 1923 programme are 18 to 35, not 16 to 35; "largest adult education programme on record" removed (China); Prussia removed from the opening paragraph and Sweden (Johansson) used as the precedent; Il'minskii schools (Dowler 2001) noted and the language explanation of the gendered disadvantage downgraded to a candidate.
- **Demography.** 1897 census is 29 years 10 months before 1926 (not "30 years less six weeks"); age-heaping sentence corrected; relapse into illiteracy acknowledged; reverse causality of the child-woman ratio of 1926 stated; identifying assumption of the triple difference stated correctly; extreme mortality bound for women added (5.7 of 24.4 points); survivorship footnote in Section 8.3 corrected (men are the more selected sex).
- **References.** Zhiromskaya is 2001 (ROSSPEN), not 1992 (Nauka); Gregg and Nafziger is EJ 2024, 134(661); Malein is Explorations in Economic History 2025, 97, 101697; Tolts is Demographic Review 7(5), 121-134; Castaneda Dower and Markevich pages 245-259; Becker and Lewis (1973) cited for the quantity-quality trade-off; Blunch and Portner is not a randomised study; Black et al. and Holmlund et al. described accurately.
- **Russian article (jnea/).** Same corrections; Lenin's two quotations verified against PSS vol. 3, pp. 576-578 (the first is about non-agricultural migration, the second about migration to towns); the Kostroma literacy figures (55.9 against 25.8 %) are from Zhbankov (1887), not "Bab'ya storona" (1891); G2 (fertility) is now reported as not confirmed.

## Conventions and caveats a new session should know
- Literacy is defined identically in 1897, 1926 and 1939 (ability to read in any language); Arabic-script literacy of Muslim women is therefore counted in 1897 and 1926.
- The sample of the state regime excludes the Volga German ASSR, Nizhny Novgorod, Leningrad and Novgorod (successors of 1939 not comparable: Leningrad and Novgorod were both absorbed into the Leningrad oblast of 1939, survival ratios 1.7 to 6.2; Nizhny Novgorod and the Volga German ASSR have no rural pages). Of the 29 linked units 20 have rural pages; rural pages exist for 35 of the 44 units of Table IX. Six units have low-quality rural pages (Astrakhan, Kungur, Volga German, Orenburg, Penza, Samara).
- Table XV of Vol. 9 has 19 Gosplan regions (12 regions and 7 autonomous republics), all used in the household regime; the rayon replication of the state regime uses the 17 that remained in the RSFSR in 1939.
- Seven Ural okrugi (three of them in the rural sample) are matched to the larger oblast of 1939 that contained them; survival ratios therefore depart from one. Robustness rows restrict the sample accordingly.
- The pre-1917 baseline (teachers per capita 1911, agrarian share 1897) is provincial: do not describe it as district-level, and cluster by `pg` wherever it is a regressor.
- "Rural Russians" means the 35 units with rural pages. Never fall back to whole-population figures silently.
- The paper describes the 1926 tables as transcribed by hand and checked with a neural OCR reading and arithmetic identities (author's account).
- Do not cite famine papers (author's instruction); Charnysh (2019, 2024) is cited in the state-capacity paragraph.
- Style: academic English, first person allowed, few colons, hyphens instead of dashes, no phrases that betray the history of the text.
- Lenin's quotations in the Russian article were verified on 4 October 2026 against the text of PSS vol. 3 (leninism.su); the Zhbankov figures are quoted through Lenin's footnote, not from the 1887 volume itself.
- The BSE (1938) article was read in full on 4 October 2026 (ru.wikisource, vol. 36, cols. 819-824): enrolment figures, ages 16-35 then up to 50, the 1936 decision ("under 50", Izvestiya 27 February 1936), the three- and ten-month courses and the instruction of pre-conscripts in Section 3.1 are taken from it.
- Still unverified against the originals: the number of the 1956 decree. The resolution of 17 May 1929 is cited by date only; its priority list is quoted from the secondary literature (Petrich 2015, Al'manakh sovremennoi nauki i obrazovaniya, no. 6).

## Conferences (checked on 29 September 2026)
| Conference | Dates and place | Deadline | Notes |
|---|---|---|---|
| CEPR Applied Micro-Economic History Workshop | 25-26 Feb 2027, Berlin (Kiel Institute) | 31 Oct 2026 | full paper; accommodation covered for presenters; best fit |
| EPSS annual conference | 24-26 Jun 2027, Copenhagen | 13 Nov 2026 | sections Political Economy, Historical Political Economy |
| EHS annual conference, new researcher posters | 2-4 Apr 2027, Liverpool | 16 Nov 2026 | papers closed on 14 Sep; check eligibility |
| ASREC | 5-6 Mar 2027, Arlington VA | 20 Nov 2026 | complete papers only; angle: mekteb literacy of Muslim women |
| BASEES | 9-11 Apr 2027, Cambridge | 5 Oct 2026 | area studies; abstract |
| MPSA | 1-4 Apr 2027, Chicago | 13 Oct 2026 | hybrid; graduate travel scholarship |
| PacDev | spring 2027, UBC | about 13 Dec 2026 | development economics |
| Cliometric Society, HPE workshops, EHA, EHES (Antwerp, 10-11 Sep 2027), NBER SI, BSE Summer Forum, EEA-ESEM, SIOE | 2027 | calls open between December and March | see memory file `likbez-conference-targets` |

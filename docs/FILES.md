# File index

Files are grouped by directory. CSV field definitions and sample restrictions are in [the codebook](../data/CODEBOOK.md). Build commands are in [BUILD_STATUS.md](BUILD_STATUS.md).

## Repository root

| File | Contents |
|---|---|
| [.gitattributes](../.gitattributes) | Line endings and byte-preservation rules |
| [.gitignore](../.gitignore) | Local sources, builds and tool caches excluded from Git |
| [CHANGELOG.md](../CHANGELOG.md) | Data versions |
| [README.md](../README.md) | The ABC of Communism |
| [requirements-docs.txt](../requirements-docs.txt) | Python packages for the PDF notes |
| [requirements.txt](../requirements.txt) | Python packages for the analysis |

## data

| File | Contents |
|---|---|
| [CODEBOOK.md](../data/CODEBOOK.md) | Census data codebook |
| [README.md](../data/README.md) | Census inputs |
| [baseline_pre1917_by_province.csv](../data/baseline_pre1917_by_province.csv) | Pre-1917 covariates aggregated to provinces |
| [baseline_pre1917_by_region1926.csv](../data/baseline_pre1917_by_region1926.csv) | Provincial covariates matched to 1926 territories |
| [baseline_pre1917_by_region1926_v2.csv](../data/baseline_pre1917_by_region1926_v2.csv) | District-weighted baselines for six autonomous territories |
| [census1926_tableIX_long.csv](../data/census1926_tableIX_long.csv) | 1926 Table IX extraction with page references and OCR flags |
| [census1939_literacy_by_region_age_sex.csv](../data/census1939_literacy_by_region_age_sex.csv) | 1939 population, illiterates and literacy with aligned city-oblast scope |
| [census1959_rsfsr_edu_by_age_sex.csv](../data/census1959_rsfsr_edu_by_age_sex.csv) | 1959 RSFSR education counts by age, sex and residence |
| [census2010_edu_by_subject_age_sex.csv](../data/census2010_edu_by_subject_age_sex.csv) | 2010 education by federal subject, age, sex and residence |
| [census2010_nat_edu_by_age_sex.csv](../data/census2010_nat_edu_by_age_sex.csv) | 2010 education by nationality, age, sex and residence |
| [census2010_nat_edu_by_subject.csv](../data/census2010_nat_edu_by_subject.csv) | 2010 education by nationality and federal subject |
| [crosswalk_1897_districts_to_1926_units.csv](../data/crosswalk_1897_districts_to_1926_units.csv) | District assignments and population fractions for the territorial crosswalk |
| [crosswalk_validation_vs_tableXV.csv](../data/crosswalk_validation_vs_tableXV.csv) | Crosswalk literacy baselines compared with Table XV |
| [korenizatsiya_panel.csv](../data/korenizatsiya_panel.csv) | 1926 literacy by ethnicity, age band, sex and titular-territory status |
| [linked_cohorts_1926_1939.csv](../data/linked_cohorts_1926_1939.csv) | Matched 1926-1939 cohorts with population counts and literacy changes |
| [linked_cohorts_rayon_1926_1939.csv](../data/linked_cohorts_rayon_1926_1939.csv) | Matched cohorts for seventeen Gosplan regions |
| [mechanism_panel.csv](../data/mechanism_panel.csv) | Demographic ratios, urban shares and literacy gaps by territory and ethnicity |
| [mechanism_panel_clean.csv](../data/mechanism_panel_clean.csv) | The mechanism sample after the census validation rules |
| [merged_gaps_baseline.csv](../data/merged_gaps_baseline.csv) | Ethnic literacy gaps joined to pre-1917 covariates |
| [region_keys.csv](../data/region_keys.csv) | Territorial keys linking the census and external data |
| [russians_by_region.csv](../data/russians_by_region.csv) | Russian male and female literacy by territory and age band |
| [russians_region_baseline.csv](../data/russians_region_baseline.csv) | Russian literacy profiles joined to provincial covariates |
| [tableIX_1926_age_sex_ethnicity_literacy.csv](../data/tableIX_1926_age_sex_ethnicity_literacy.csv) | 1926 population and literacy by territory, residence, age, ethnicity and sex |
| [tableIX_bands_validated.csv](../data/tableIX_bands_validated.csv) | Validated age-band counts and literacy rates |
| [tableIX_cohort_gaps.csv](../data/tableIX_cohort_gaps.csv) | Russian-minus-titular literacy gaps by age band and sex |
| [tableIX_five_year_groups_validated.csv](../data/tableIX_five_year_groups_validated.csv) | Printed and summed five-year counts, selected values and validation tiers |
| [tableIX_region_quality.csv](../data/tableIX_region_quality.csv) | OCR confirmation shares by territory and residence |
| [tableIX_single_years_validated.csv](../data/tableIX_single_years_validated.csv) | Single-year counts with five-year validation flags |
| [tableXV_1926_1897_age_sex_literacy.csv](../data/tableXV_1926_1897_age_sex_literacy.csv) | 1897 and 1926 population and literacy on the census bureau territorial definitions |
| [tableXV_linked_cohorts.csv](../data/tableXV_linked_cohorts.csv) | 1897-1926 cohort changes and later-to-earlier population ratios |

## data/v1_before_validation

| File | Contents |
|---|---|
| [korenizatsiya_panel.csv](../data/v1_before_validation/korenizatsiya_panel.csv) | Earlier version of 1926 literacy by ethnicity, age band, sex and titular-territory status |
| [linked_cohorts_1926_1939.csv](../data/v1_before_validation/linked_cohorts_1926_1939.csv) | Earlier version of matched 1926-1939 cohorts with population counts and literacy changes |
| [mechanism_panel.csv](../data/v1_before_validation/mechanism_panel.csv) | Earlier version of demographic ratios, urban shares and literacy gaps by territory and ethnicity |
| [mechanism_panel_clean.csv](../data/v1_before_validation/mechanism_panel_clean.csv) | Earlier version of the mechanism sample after the census validation rules |
| [russians_by_region.csv](../data/v1_before_validation/russians_by_region.csv) | Earlier version of russian male and female literacy by territory and age band |
| [russians_region_baseline.csv](../data/v1_before_validation/russians_region_baseline.csv) | Earlier version of russian literacy profiles joined to provincial covariates |
| [tableIX_cohort_gaps.csv](../data/v1_before_validation/tableIX_cohort_gaps.csv) | Earlier version of russian-minus-titular literacy gaps by age band and sex |

## docs

| File | Contents |
|---|---|
| [ABC_of_Communism_reader.zip](../docs/ABC_of_Communism_reader.zip) | English paper, research notes, source list and codebook |
| [BUILD_STATUS.md](../docs/BUILD_STATUS.md) | Building the PDFs |
| [Data_and_methods.pdf](../docs/Data_and_methods.pdf) | English note on census construction and estimation |
| [FILES.md](../docs/FILES.md) | This file index |
| [METHODS.md](../docs/METHODS.md) | Data and estimation |
| [README.md](../docs/README.md) | Research notes and sources |
| [SOURCES.md](../docs/SOURCES.md) | Sources |
| [SUPPLEMENTARY_EVIDENCE.md](../docs/SUPPLEMENTARY_EVIDENCE.md) | Additional results |
| [Supplementary_evidence.pdf](../docs/Supplementary_evidence.pdf) | English note on the 1924 and 1959 comparisons |

## figures

| File | Contents |
|---|---|
| [README.md](../figures/README.md) | English figures |
| [fig01_design.pdf](../figures/fig01_design.pdf) | Cohort comparison design |
| [fig01_design.png](../figures/fig01_design.png) | Cohort comparison design |
| [fig02_age_profile_1926.pdf](../figures/fig02_age_profile_1926.pdf) | Literacy by age in 1926 |
| [fig02_age_profile_1926.png](../figures/fig02_age_profile_1926.png) | Literacy by age in 1926 |
| [fig04_wave2_linked_cohorts.pdf](../figures/fig04_wave2_linked_cohorts.pdf) | Cohort literacy in 1926 and 1939 |
| [fig04_wave2_linked_cohorts.png](../figures/fig04_wave2_linked_cohorts.png) | Cohort literacy in 1926 and 1939 |
| [fig05_dose_response_wave2.pdf](../figures/fig05_dose_response_wave2.pdf) | Initial literacy and later gains |
| [fig05_dose_response_wave2.png](../figures/fig05_dose_response_wave2.png) | Initial literacy and later gains |
| [fig06_two_regimes.pdf](../figures/fig06_two_regimes.pdf) | Cohort changes across the two historical periods |
| [fig06_two_regimes.png](../figures/fig06_two_regimes.png) | Cohort changes across the two historical periods |
| [fig08_convergence_titular.pdf](../figures/fig08_convergence_titular.pdf) | Literacy convergence among titular groups |
| [fig08_convergence_titular.png](../figures/fig08_convergence_titular.png) | Literacy convergence among titular groups |
| [fig09_ethnic_gaps_six_republics.pdf](../figures/fig09_ethnic_gaps_six_republics.pdf) | Ethnic literacy gaps in six republics |
| [fig09_ethnic_gaps_six_republics.png](../figures/fig09_ethnic_gaps_six_republics.png) | Ethnic literacy gaps in six republics |
| [fig10_decomposition.pdf](../figures/fig10_decomposition.pdf) | Literacy-change decomposition |
| [fig10_decomposition.png](../figures/fig10_decomposition.png) | Literacy-change decomposition |
| [fig11_russians_across_regions.pdf](../figures/fig11_russians_across_regions.pdf) | Russian literacy across territories |
| [fig11_russians_across_regions.png](../figures/fig11_russians_across_regions.png) | Russian literacy across territories |
| [fig12_heatmap_women_1926.pdf](../figures/fig12_heatmap_women_1926.pdf) | Female literacy by territory and age |
| [fig12_heatmap_women_1926.png](../figures/fig12_heatmap_women_1926.png) | Female literacy by territory and age |
| [fig13_inference.pdf](../figures/fig13_inference.pdf) | Cohort estimates and inference intervals |
| [fig13_inference.png](../figures/fig13_inference.png) | Cohort estimates and inference intervals |
| [fig14_mechanisms.pdf](../figures/fig14_mechanisms.pdf) | Regional mechanism correlations |
| [fig14_mechanisms.png](../figures/fig14_mechanisms.png) | Regional mechanism correlations |
| [fig16_wave2_rayons.pdf](../figures/fig16_wave2_rayons.pdf) | Cohort changes in the Gosplan-region sample |
| [fig16_wave2_rayons.png](../figures/fig16_wave2_rayons.png) | Cohort changes in the Gosplan-region sample |
| [fig17_ethnic_gap_2010_by_cohort.pdf](../figures/fig17_ethnic_gap_2010_by_cohort.pdf) | Ethnic education gaps by cohort in 2010 |
| [fig17_ethnic_gap_2010_by_cohort.png](../figures/fig17_ethnic_gap_2010_by_cohort.png) | Ethnic education gaps by cohort in 2010 |
| [fig18_gap2010_vs_gap1926.pdf](../figures/fig18_gap2010_vs_gap1926.pdf) | Ethnic gaps in 1926 and 2010 |
| [fig18_gap2010_vs_gap1926.png](../figures/fig18_gap2010_vs_gap1926.png) | Ethnic gaps in 1926 and 2010 |
| [fig19_event_studies.pdf](../figures/fig19_event_studies.pdf) | Cohort profiles for the two census comparisons |
| [fig19_event_studies.png](../figures/fig19_event_studies.png) | Cohort profiles for the two census comparisons |
| [fig20_ddd_two_regimes.pdf](../figures/fig20_ddd_two_regimes.pdf) | Triple differences in the two historical periods |
| [fig20_ddd_two_regimes.png](../figures/fig20_ddd_two_regimes.png) | Triple differences in the two historical periods |
| [fig21_legacy_robustness.pdf](../figures/fig21_legacy_robustness.pdf) | Sensitivity of the later ethnic correlations |
| [fig21_legacy_robustness.png](../figures/fig21_legacy_robustness.png) | Sensitivity of the later ethnic correlations |
| [fig22_map_1926.pdf](../figures/fig22_map_1926.pdf) | Map of the 1926 territories |
| [fig23_legacy_sex_difference.pdf](../figures/fig23_legacy_sex_difference.pdf) | Sex differences in the later ethnic correlations |
| [fig23_legacy_sex_difference.png](../figures/fig23_legacy_sex_difference.png) | Sex differences in the later ethnic correlations |
| [fig24_taught.pdf](../figures/fig24_taught.pdf) | Normalised literacy changes by cohort |
| [fig24_taught.png](../figures/fig24_taught.png) | Normalised literacy changes by cohort |
| [fig25_main_cohorts.pdf](../figures/fig25_main_cohorts.pdf) | Literacy in the main birth cohorts |
| [fig25_main_cohorts.png](../figures/fig25_main_cohorts.png) | Literacy in the main birth cohorts |
| [fig26_cohorts_all.pdf](../figures/fig26_cohorts_all.pdf) | Literacy profiles across the census cohorts |
| [fig26_cohorts_all.png](../figures/fig26_cohorts_all.png) | Literacy profiles across the census cohorts |
| [fig27_taught_periods.pdf](../figures/fig27_taught_periods.pdf) | Normalised gains in the two census periods |
| [fig27_taught_periods.png](../figures/fig27_taught_periods.png) | Normalised gains in the two census periods |
| [fig28_regions.pdf](../figures/fig28_regions.pdf) | Regional literacy changes |
| [fig28_regions.png](../figures/fig28_regions.png) | Regional literacy changes |
| [fig29_why_regions.pdf](../figures/fig29_why_regions.pdf) | Regional covariates and literacy gains |
| [fig29_why_regions.png](../figures/fig29_why_regions.png) | Regional covariates and literacy gains |
| [scan_tableIX_tatar_rural_p242.jpg](../figures/scan_tableIX_tatar_rural_p242.jpg) | Table IX source-page image for the rural Tatar population |
| [scan_tableIX_tatar_rural_p242_detail.png](../figures/scan_tableIX_tatar_rural_p242_detail.png) | Table IX source-page image for the rural Tatar population |

## jnea

| File | Contents |
|---|---|
| [README.md](../jnea/README.md) | Russian paper |
| [article_jnea.pdf](../jnea/article_jnea.pdf) | Russian paper with supplementary checks and an English abstract |
| [article_jnea.tex](../jnea/article_jnea.tex) | Russian paper with supplementary checks and an English abstract |
| [numbers_ru.tex](../jnea/numbers_ru.tex) | Generated numerical macros for the Russian manuscript |
| [supplementary_checks.tex](../jnea/supplementary_checks.tex) | Russian manuscript section on additional checks |
| [supplementary_numbers.tex](../jnea/supplementary_numbers.tex) | Generated numerical macros for the supplementary comparisons |

## jnea/figures

| File | Contents |
|---|---|
| [rj1_sostav.pdf](../jnea/figures/rj1_sostav.pdf) | Russian article figure on population composition |
| [rj1_sostav.png](../jnea/figures/rj1_sostav.png) | Russian article figure on population composition |
| [rj2_vozrast.pdf](../jnea/figures/rj2_vozrast.pdf) | Russian article age profile |
| [rj2_vozrast.png](../jnea/figures/rj2_vozrast.png) | Russian article age profile |
| [rj3_regiony.pdf](../jnea/figures/rj3_regiony.pdf) | Russian article regional comparison |
| [rj3_regiony.png](../jnea/figures/rj3_regiony.png) | Russian article regional comparison |

## jnea/tables

| File | Contents |
|---|---|
| [tab_j1.tex](../jnea/tables/tab_j1.tex) | Russian article table 1 |
| [tab_j2.tex](../jnea/tables/tab_j2.tex) | Russian article table 2 |
| [tab_j3.tex](../jnea/tables/tab_j3.tex) | Russian article table 3 |
| [tab_j4.tex](../jnea/tables/tab_j4.tex) | Russian article table 4 |
| [tab_j5.tex](../jnea/tables/tab_j5.tex) | Russian article table 5 |
| [tab_j6.tex](../jnea/tables/tab_j6.tex) | Russian article table 6 |
| [tab_j7.tex](../jnea/tables/tab_j7.tex) | Russian article table 7 |

## methodology

| File | Contents |
|---|---|
| [README.md](../methodology/README.md) | Inference and accounting |
| [accounting.py](../methodology/accounting.py) | Calculate selection, equivalence and exposure-duration scenarios |
| [inference.py](../methodology/inference.py) | Calculate cluster inference for weighted least-squares contrasts |
| [run_analysis.py](../methodology/run_analysis.py) | Estimate the cohort specifications with alternative cluster inference |
| [test_inference.py](../methodology/test_inference.py) | Check cluster covariance estimates and restricted-bootstrap refits |

## methodology/results

| File | Contents |
|---|---|
| [accounting_summary.json](../methodology/results/accounting_summary.json) | Selection-accounting scenario summary |
| [bounded_bias_sensitivity.csv](../methodology/results/bounded_bias_sensitivity.csv) | Estimates under specified bounds on counterfactual bias |
| [equivalence_taught_r.csv](../methodology/results/equivalence_taught_r.csv) | Equivalence checks for normalised literacy gains |
| [equivalence_taught_t.csv](../methodology/results/equivalence_taught_t.csv) | Equivalence checks for the alternative learning measure |
| [errors.json](../methodology/results/errors.json) | Specifications withheld because a contrast is unidentified |
| [estimates.csv](../methodology/results/estimates.csv) | Cohort estimates with alternative cluster inference |
| [mixture_duration.csv](../methodology/results/mixture_duration.csv) | Exposure-duration scenarios for the historical male comparison |
| [selection_accounting.csv](../methodology/results/selection_accounting.csv) | Conditional selection scenarios by cohort |

## methodology/results_original

| File | Contents |
|---|---|
| [accounting_summary.json](../methodology/results_original/accounting_summary.json) | Earlier version of selection-accounting scenario summary |
| [bounded_bias_sensitivity.csv](../methodology/results_original/bounded_bias_sensitivity.csv) | Earlier version of estimates under specified bounds on counterfactual bias |
| [equivalence_taught_r.csv](../methodology/results_original/equivalence_taught_r.csv) | Earlier version of equivalence checks for normalised literacy gains |
| [equivalence_taught_t.csv](../methodology/results_original/equivalence_taught_t.csv) | Earlier version of equivalence checks for the alternative learning measure |
| [errors.json](../methodology/results_original/errors.json) | Earlier version of specifications withheld because a contrast is unidentified |
| [estimates.csv](../methodology/results_original/estimates.csv) | Earlier version of cohort estimates with alternative cluster inference |
| [fresh_source_matches.csv](../methodology/results_original/fresh_source_matches.csv) | Earlier version of population and illiteracy values compared with saved source pages |
| [mixture_duration.csv](../methodology/results_original/mixture_duration.csv) | Earlier version of exposure-duration scenarios for the historical male comparison |
| [scope_corrections.csv](../methodology/results_original/scope_corrections.csv) | Earlier version of city and oblast population adjustments for the 1939 join |
| [selection_accounting.csv](../methodology/results_original/selection_accounting.csv) | Earlier version of conditional selection scenarios by cohort |

## paper

| File | Contents |
|---|---|
| [ABC_of_Communism.pdf](../paper/ABC_of_Communism.pdf) | English paper and online appendix |
| [ABC_of_Communism.tex](../paper/ABC_of_Communism.tex) | English paper and online appendix |
| [README.md](../paper/README.md) | English paper |
| [appendix.tex](../paper/appendix.tex) | English manuscript appendix |
| [numbers.tex](../paper/numbers.tex) | Generated numerical macros for the English manuscript |
| [refs.bib](../paper/refs.bib) | Manuscript bibliography |
| [supplementary_1924.tex](../paper/supplementary_1924.tex) | English manuscript section on the institutional survey |
| [supplementary_1959.tex](../paper/supplementary_1959.tex) | English manuscript section on the regional follow-up |
| [supplementary_numbers.tex](../paper/supplementary_numbers.tex) | Generated numerical macros for the supplementary comparisons |

## paper/tables

| File | Contents |
|---|---|
| [tab_a1.tex](../paper/tables/tab_a1.tex) | Sensitivity of the 1897-1926 cohort estimates, LaTeX table body |
| [tab_a2.tex](../paper/tables/tab_a2.tex) | Sensitivity of the 1926-1939 sex contrasts, LaTeX table body |
| [tab_a3.tex](../paper/tables/tab_a3.tex) | Volga and Muslim female cohort contrasts, LaTeX table body |
| [tab_a4.tex](../paper/tables/tab_a4.tex) | Alternative predictors and sample restrictions, LaTeX table body |
| [tab_a5.tex](../paper/tables/tab_a5.tex) | Baseline literacy, titular status and population ratios, LaTeX table body |
| [tab_a6.tex](../paper/tables/tab_a6.tex) | Cohort changes by territory and sex, LaTeX table body |
| [tab_a7.tex](../paper/tables/tab_a7.tex) | Parent-cohort literacy gains and child literacy, LaTeX table body |
| [tab_a8.tex](../paper/tables/tab_a8.tex) | Total and rural population comparisons, LaTeX table body |
| [tab_a9.tex](../paper/tables/tab_a9.tex) | Ethnic literacy gaps in 1926 and education gaps in 2010, LaTeX table body |
| [tab_c4.tex](../paper/tables/tab_c4.tex) | National five-year cohort literacy in 1926 and 1939, LaTeX table body |
| [tab_c59.tex](../paper/tables/tab_c59.tex) | National cohort literacy in 1926, 1939 and 1959, LaTeX table body |
| [tab_cohort2010.tex](../paper/tables/tab_cohort2010.tex) | Cohort education gaps in 2010, LaTeX table body |
| [tab_conv.tex](../paper/tables/tab_conv.tex) | Regional literacy convergence, LaTeX table body |
| [tab_data.tex](../paper/tables/tab_data.tex) | Census data summary, LaTeX table body |
| [tab_decomp.tex](../paper/tables/tab_decomp.tex) | Literacy-change decomposition, LaTeX table body |
| [tab_es1.tex](../paper/tables/tab_es1.tex) | Cohort profiles for 1897-1926, LaTeX table body |
| [tab_es2.tex](../paper/tables/tab_es2.tex) | Cohort profiles for 1926-1939, LaTeX table body |
| [tab_koren.tex](../paper/tables/tab_koren.tex) | Ethnic literacy and titular-territory status, LaTeX table body |
| [tab_legacy.tex](../paper/tables/tab_legacy.tex) | Later ethnic correlations, LaTeX table body |
| [tab_logodds.tex](../paper/tables/tab_logodds.tex) | Alternative log-odds specification, LaTeX table body |
| [tab_main.tex](../paper/tables/tab_main.tex) | Main cohort regressions, LaTeX table body |
| [tab_mech.tex](../paper/tables/tab_mech.tex) | Regional mechanism regressions, LaTeX table body |
| [tab_msu_data.tex](../paper/tables/tab_msu_data.tex) | Census input summary, LaTeX table body |
| [tab_msu_sumstat.tex](../paper/tables/tab_msu_sumstat.tex) | Analysis-sample summary, LaTeX table body |
| [tab_msu_units.tex](../paper/tables/tab_msu_units.tex) | Territories in the cohort sample, LaTeX table body |
| [tab_regimes.tex](../paper/tables/tab_regimes.tex) | The two-period comparison, LaTeX table body |
| [tab_robust.tex](../paper/tables/tab_robust.tex) | Specification sensitivity, LaTeX table body |
| [tab_russians.tex](../paper/tables/tab_russians.tex) | Russian literacy by territory, LaTeX table body |
| [tab_sexdiff.tex](../paper/tables/tab_sexdiff.tex) | Sex differences in ethnic correlations, LaTeX table body |
| [tab_sumstat.tex](../paper/tables/tab_sumstat.tex) | Descriptive statistics, LaTeX table body |

## results

| File | Contents |
|---|---|
| [A_wave1_1897_1926.txt](../results/A_wave1_1897_1926.txt) | 1897-1926 1897 1926 |
| [B4_leave_one_out.csv](../results/B4_leave_one_out.csv) | Leave one out |
| [B5_permutation_female_x_young.txt](../results/B5_permutation_female_x_young.txt) | Permutation female x young |
| [B6_gender_gap_within_cohorts.csv](../results/B6_gender_gap_within_cohorts.csv) | Gender gap within cohorts |
| [B7_unit_level_wave2.csv](../results/B7_unit_level_wave2.csv) | Unit level 1926-1939 |
| [B9_rayon_cells.csv](../results/B9_rayon_cells.csv) | Rayon cells |
| [B9_wave2_rayon.txt](../results/B9_wave2_rayon.txt) | 1926-1939 rayon |
| [B_wave2_1926_1939.txt](../results/B_wave2_1926_1939.txt) | 1926-1939 1926 1939 |
| [C1_predictors_by_wave.csv](../results/C1_predictors_by_wave.csv) | Predictors by wave |
| [C_two_regimes.txt](../results/C_two_regimes.txt) | Two regimes |
| [C_wave1_proxy_units.csv](../results/C_wave1_proxy_units.csv) | 1897-1926 proxy units |
| [D_all_cells.csv](../results/D_all_cells.csv) | All cells |
| [D_core_cells.csv](../results/D_core_cells.csv) | Core cells |
| [D_core_cells_total.csv](../results/D_core_cells_total.csv) | Core cells total |
| [D_decomposition_by_cohort.csv](../results/D_decomposition_by_cohort.csv) | Decomposition by cohort |
| [D_leave_one_unit_out.csv](../results/D_leave_one_unit_out.csv) | Leave one unit out |
| [D_pooled_triple_difference.csv](../results/D_pooled_triple_difference.csv) | Pooled triple difference |
| [D_raw_gaps_by_nationality.csv](../results/D_raw_gaps_by_nationality.csv) | Raw gaps by nationality |
| [D_raw_gaps_by_type.csv](../results/D_raw_gaps_by_type.csv) | Raw gaps by type |
| [D_within_region_decomposition.txt](../results/D_within_region_decomposition.txt) | Within region decomposition |
| [E1_wave1_event_cells.csv](../results/E1_wave1_event_cells.csv) | 1897-1926 event cells |
| [E1_wave1_event_coefs.csv](../results/E1_wave1_event_coefs.csv) | 1897-1926 event coefs |
| [E2_wave2_event_coefs.csv](../results/E2_wave2_event_coefs.csv) | 1926-1939 event coefs |
| [E3_two_regime_ddd.csv](../results/E3_two_regime_ddd.csv) | Two regime triple difference |
| [E4_legacy_robustness_rural.csv](../results/E4_legacy_robustness_rural.csv) | Legacy robustness rural |
| [E4_legacy_robustness_total.csv](../results/E4_legacy_robustness_total.csv) | Legacy robustness total |
| [E_did.txt](../results/E_did.txt) | Difference in differences |
| [E_did_log.txt](../results/E_did_log.txt) | Difference in differences log |
| [E_korenizatsiya.txt](../results/E_korenizatsiya.txt) | Korenizatsiya |
| [E_korenizatsiya_cells.csv](../results/E_korenizatsiya_cells.csv) | Korenizatsiya cells |
| [F_russians.csv](../results/F_russians.csv) | Russians |
| [F_russians_across_regions.txt](../results/F_russians_across_regions.txt) | Russians across regions |
| [F_russians_units.csv](../results/F_russians_units.csv) | Russians units |
| [G_mechanism_cells.csv](../results/G_mechanism_cells.csv) | Mechanism cells |
| [G_mechanisms.csv](../results/G_mechanisms.csv) | Mechanisms |
| [G_mechanisms.txt](../results/G_mechanisms.txt) | Mechanisms |
| [H_age_profile_1926_rural.csv](../results/H_age_profile_1926_rural.csv) | Age profile 1926 rural |
| [H_age_profile_1926_total.csv](../results/H_age_profile_1926_total.csv) | Age profile 1926 total |
| [H_descriptives.txt](../results/H_descriptives.txt) | Descriptives |
| [H_unit_band_sex_rural_1926.csv](../results/H_unit_band_sex_rural_1926.csv) | Unit band sex rural 1926 |
| [I_intergen_1939.txt](../results/I_intergen_1939.txt) | Intergen 1939 |
| [I_intergen_units.csv](../results/I_intergen_units.csv) | Intergen units |
| [J0_cohorts_1926_1939.csv](../results/J0_cohorts_1926_1939.csv) | Cohorts 1926 1939 |
| [J1_ethnic_gap_2010_by_sex_age.csv](../results/J1_ethnic_gap_2010_by_sex_age.csv) | Ethnic gap 2010 by sex age |
| [J1_regions.csv](../results/J1_regions.csv) | Regions |
| [J2_ethnic_gaps_1926_2010.csv](../results/J2_ethnic_gaps_1926_2010.csv) | Ethnic gaps 1926 2010 |
| [J3_edu2010_70plus_vs_wave2.csv](../results/J3_edu2010_70plus_vs_wave2.csv) | Edu2010 70plus vs 1926-1939 |
| [J_legacy_2010.txt](../results/J_legacy_2010.txt) | Legacy 2010 |
| [L2_leave_one_out.csv](../results/L2_leave_one_out.csv) | Leave one out |
| [L3_permutation_betaF.txt](../results/L3_permutation_betaF.txt) | Permutation betaF |
| [L5_cohort_ddd_by_nationality.csv](../results/L5_cohort_ddd_by_nationality.csv) | Cohort triple difference by nationality |
| [L_legacy_cells.csv](../results/L_legacy_cells.csv) | Legacy cells |
| [L_legacy_robust.txt](../results/L_legacy_robust.txt) | Legacy robust |
| [M_budgets_regions.csv](../results/M_budgets_regions.csv) | Budgets regions |
| [M_budgets_regions.txt](../results/M_budgets_regions.txt) | Budgets regions |
| [M_demog_checks.txt](../results/M_demog_checks.txt) | Demog checks |
| [M_mechanism_regions.csv](../results/M_mechanism_regions.csv) | Mechanism regions |
| [N_jnea.txt](../results/N_jnea.txt) | Jnea |
| [N_jnea2.txt](../results/N_jnea2.txt) | Jnea2 |
| [N_jnea_core_cells.csv](../results/N_jnea_core_cells.csv) | Jnea core cells |
| [N_jnea_core_decomposition.csv](../results/N_jnea_core_decomposition.csv) | Jnea core decomposition |
| [N_jnea_decomposition.csv](../results/N_jnea_decomposition.csv) | Jnea decomposition |
| [N_jnea_ethnic_gaps.csv](../results/N_jnea_ethnic_gaps.csv) | Jnea ethnic gaps |
| [N_jnea_mechanism_cells.csv](../results/N_jnea_mechanism_cells.csv) | Jnea mechanism cells |
| [N_jnea_raw_gaps.csv](../results/N_jnea_raw_gaps.csv) | Jnea raw gaps |
| [N_jnea_raw_gaps_type.csv](../results/N_jnea_raw_gaps_type.csv) | Jnea raw gaps type |
| [N_jnea_russians_units.csv](../results/N_jnea_russians_units.csv) | Jnea russians units |
| [README.md](../results/README.md) | Estimates and analysis samples |
| [S1_region_gains.csv](../results/S1_region_gains.csv) | Region gains |
| [S_legacy_sexdiff.csv](../results/S_legacy_sexdiff.csv) | Legacy sexdiff |
| [S_legacy_sexdiff.txt](../results/S_legacy_sexdiff.txt) | Legacy sexdiff |
| [S_legacy_sexdiff_cells.csv](../results/S_legacy_sexdiff_cells.csv) | Legacy sexdiff cells |
| [S_legacy_sexdiff_nationalities.csv](../results/S_legacy_sexdiff_nationalities.csv) | Legacy sexdiff nationalities |
| [T_two_regime_cells.csv](../results/T_two_regime_cells.csv) | Two regime cells |
| [T_two_regime_cells_middle.csv](../results/T_two_regime_cells_middle.csv) | Two regime cells middle |
| [V_validation_1926.txt](../results/V_validation_1926.txt) | Validation 1926 |
| [W2_cells.csv](../results/W2_cells.csv) | Main rural cohort sample used by the 1926-1939 regressions |
| [W2_cells_total.csv](../results/W2_cells_total.csv) | Cells total |
| [X_extra.txt](../results/X_extra.txt) | Extra |
| [X_legacy_extra.csv](../results/X_legacy_extra.csv) | Legacy extra |
| [X_same_cohorts_level_gain.csv](../results/X_same_cohorts_level_gain.csv) | Same cohorts level gain |
| [X_two_regime_stacked.csv](../results/X_two_regime_stacked.csv) | Two regime stacked |
| [X_unit_table_wave2.csv](../results/X_unit_table_wave2.csv) | Unit table 1926-1939 |
| [X_wave2_robustness.csv](../results/X_wave2_robustness.csv) | 1926-1939 robustness |
| [coefficients_summary.csv](../results/coefficients_summary.csv) | Saved regression coefficients |
| [inference_df.json](../results/inference_df.json) | Degrees of freedom for the manuscript intervals |
| [paper_numbers.csv](../results/paper_numbers.csv) | Numerical keys used in the manuscript text and tables |
| [paper_numbers.json](../results/paper_numbers.json) | Numerical keys used in the manuscript text and tables |
| [paper_numbers.txt](../results/paper_numbers.txt) | Numerical keys used in the manuscript text and tables |

## scripts

| File | Contents |
|---|---|
| [README.md](../scripts/README.md) | Replication scripts |
| [baseline_1897.py](../scripts/baseline_1897.py) | Aggregate the Malein district data to pre-1917 provinces |
| [build_1926_v2.py](../scripts/build_1926_v2.py) | Validated 1926 panel (v2). Rebuilds every derived 1926 file from data/census1926_tableIX_long.csv using only |
| [build_articles.py](../scripts/build_articles.py) | Compile the English and Russian manuscripts with Tectonic |
| [build_docs.py](../scripts/build_docs.py) | Typeset the two English research notes from Markdown |
| [census2010.py](../scripts/census2010.py) | Extract education and nationality tables from the Rosstat workbooks |
| [compare_stata.py](../scripts/compare_stata.py) | Compare Stata estimates with the Python results by numerical key |
| [crosswalk.py](../scripts/crosswalk.py) | Match 1897 districts to six autonomous units in the 1926 census |
| [demoscope_1939.py](../scripts/demoscope_1939.py) | Extract 1939 population and illiteracy tables from Demoscope |
| [demoscope_1959.py](../scripts/demoscope_1959.py) | Extract the 1959 RSFSR education table from Demoscope |
| [export_stata.py](../scripts/export_stata.py) | Export the saved analysis samples to Stata format 118 |
| [jnea2_figures.py](../scripts/jnea2_figures.py) | Draw the Russian article figures from results/paper_numbers.json |
| [jnea2_tables.py](../scripts/jnea2_tables.py) | Write the Russian article tables with decimal commas |
| [linked_cohorts.py](../scripts/linked_cohorts.py) | Match birth cohorts in the 1897 and 1926 tables of census volume 9 |
| [make_tables.py](../scripts/make_tables.py) | Write the English manuscript tables from results/paper_numbers.json |
| [maps2010.py](../scripts/maps2010.py) | Match 1926 territories and nationalities to 2010 census categories |
| [names.py](../scripts/names.py) | Provide English names for territories and ethnic groups in figures |
| [paper_figures.py](../scripts/paper_figures.py) | Draw manuscript figures from the census samples and saved estimates |
| [paper_numbers.py](../scripts/paper_numbers.py) | Calculate the estimates and numerical values used in the manuscripts |
| [rosstat_get.py](../scripts/rosstat_get.py) | Download the Rosstat 2010 workbooks used by census2010.py |
| [run_supplementary.py](../scripts/run_supplementary.py) | Update census input snapshots and run the two supplementary analyses |
| [verify_release.py](../scripts/verify_release.py) | Check source hashes, analysis inputs and reported numerical values |
| [wave2_rayon.py](../scripts/wave2_rayon.py) | Compare 1926 and 1939 cohorts across seventeen Gosplan regions |
| [write_numbers.py](../scripts/write_numbers.py) | Write manuscript number macros from results/paper_numbers.json |
| [write_supplementary_numbers.py](../scripts/write_supplementary_numbers.py) | Write manuscript number macros from the supplementary model tables |

## stata

| File | Contents |
|---|---|
| [ABC_of_Communism.do](../stata/ABC_of_Communism.do) | English paper and online appendix |
| [README.md](../stata/README.md) | Stata replication |

## supplementary

| File | Contents |
|---|---|
| [README.md](../supplementary/README.md) | Additional census and institutional evidence |

## supplementary/additional_data_analysis

| File | Contents |
|---|---|
| [README.md](../supplementary/additional_data_analysis/README.md) | Regional cohorts in 1939 and 1959 |
| [article_addendum.tex](../supplementary/additional_data_analysis/article_addendum.tex) | LaTeX account of the regional 1939-1959 comparison |
| [census1939_online_checks.csv](../supplementary/additional_data_analysis/census1939_online_checks.csv) | 1939 input values compared with saved Demoscope tables |
| [census1959_html_xls_checks.csv](../supplementary/additional_data_analysis/census1959_html_xls_checks.csv) | 1959 workbook cells compared with regional HTML tables |
| [census1959_partition_checks.csv](../supplementary/additional_data_analysis/census1959_partition_checks.csv) | Education component identities in the 1959 workbook |
| [census1959_population_checks.csv](../supplementary/additional_data_analysis/census1959_population_checks.csv) | Population identities in the 1959 workbook |
| [census1959_regions_long.csv](../supplementary/additional_data_analysis/census1959_regions_long.csv) | 1959 regional education counts and source blank flags |
| [linked_republic_cohorts_1939_1959.csv](../supplementary/additional_data_analysis/linked_republic_cohorts_1939_1959.csv) | Three five-year cohorts matched between the regional censuses |
| [literacy_persistence_regions.png](../supplementary/additional_data_analysis/literacy_persistence_regions.png) | Regional cohort literacy in 1939 and 1959 |
| [migration_registration_1931_1932.csv](../supplementary/additional_data_analysis/migration_registration_1931_1932.csv) | Contemporary migration registration counts |
| [migration_rural_urban_1931_1932.csv](../supplementary/additional_data_analysis/migration_rural_urban_1931_1932.csv) | Contemporary migration counts by residence |
| [migration_sex_shares_1931_1932.csv](../supplementary/additional_data_analysis/migration_sex_shares_1931_1932.csv) | Male and female shares in the migration extracts |
| [persistence_sample_summary.csv](../supplementary/additional_data_analysis/persistence_sample_summary.csv) | Composition of the five- and nine-republic samples |
| [post1939_gender_gap_inference.csv](../supplementary/additional_data_analysis/post1939_gender_gap_inference.csv) | Twelve descriptive regional models with cluster inference |
| [reproduction_check.json](../supplementary/additional_data_analysis/reproduction_check.json) | Results of rerunning the packaged analysis |
| [republic_summary_1939_1959.csv](../supplementary/additional_data_analysis/republic_summary_1939_1959.csv) | Literacy changes by republic, residence and sex |
| [requirements.txt](../supplementary/additional_data_analysis/requirements.txt) | Python packages for the analysis |
| [source_file_manifest.json](../supplementary/additional_data_analysis/source_file_manifest.json) | Source URLs, file sizes and SHA-256 hashes |
| [time_use_1923_domestic_work.csv](../supplementary/additional_data_analysis/time_use_1923_domestic_work.csv) | Domestic-work entries from the 1923 Voronezh survey |
| [validation_summary.json](../supplementary/additional_data_analysis/validation_summary.json) | Source extraction and population-accounting checks |

## supplementary/additional_data_analysis/inputs

| File | Contents |
|---|---|
| [census1939_literacy_by_region_age_sex.csv](../supplementary/additional_data_analysis/inputs/census1939_literacy_by_region_age_sex.csv) | 1939 population, illiterates and literacy with aligned city-oblast scope |

## supplementary/additional_data_analysis/raw_sources

| File | Contents |
|---|---|
| [1937_contents.pdf](../supplementary/additional_data_analysis/raw_sources/1937_contents.pdf) | Contents pages of the published 1937 census volume |
| [1939_Chuvash_ill.html](../supplementary/additional_data_analysis/raw_sources/1939_Chuvash_ill.html) | 1939 Chuvash census table, illiteracy |
| [1939_Chuvash_rural.html](../supplementary/additional_data_analysis/raw_sources/1939_Chuvash_rural.html) | 1939 Chuvash census table, rural population |
| [1939_Chuvash_total.html](../supplementary/additional_data_analysis/raw_sources/1939_Chuvash_total.html) | 1939 Chuvash census table, total population |
| [1939_Chuvash_urban.html](../supplementary/additional_data_analysis/raw_sources/1939_Chuvash_urban.html) | 1939 Chuvash census table, urban population |
| [1939_Tatar_ill.html](../supplementary/additional_data_analysis/raw_sources/1939_Tatar_ill.html) | 1939 Tatar census table, illiteracy |
| [1939_Tatar_rural.html](../supplementary/additional_data_analysis/raw_sources/1939_Tatar_rural.html) | 1939 Tatar census table, rural population |
| [1939_Tatar_total.html](../supplementary/additional_data_analysis/raw_sources/1939_Tatar_total.html) | 1939 Tatar census table, total population |
| [1939_Tatar_urban.html](../supplementary/additional_data_analysis/raw_sources/1939_Tatar_urban.html) | 1939 Tatar census table, urban population |
| [1939_Yakut_ill.html](../supplementary/additional_data_analysis/raw_sources/1939_Yakut_ill.html) | 1939 Yakut census table, illiteracy |
| [1939_Yakut_rural.html](../supplementary/additional_data_analysis/raw_sources/1939_Yakut_rural.html) | 1939 Yakut census table, rural population |
| [1939_Yakut_total.html](../supplementary/additional_data_analysis/raw_sources/1939_Yakut_total.html) | 1939 Yakut census table, total population |
| [1939_Yakut_urban.html](../supplementary/additional_data_analysis/raw_sources/1939_Yakut_urban.html) | 1939 Yakut census table, urban population |
| [1939_download_urls.json](../supplementary/additional_data_analysis/raw_sources/1939_download_urls.json) | Addresses of the downloaded 1939 source tables |
| [1959_base.html](../supplementary/additional_data_analysis/raw_sources/1959_base.html) | Demoscope source index for the 1959 education tables |
| [1959_region_14.html](../supplementary/additional_data_analysis/raw_sources/1959_region_14.html) | 1959 regional education table, Demoscope entry 14 |
| [1959_region_24.html](../supplementary/additional_data_analysis/raw_sources/1959_region_24.html) | 1959 regional education table, Demoscope entry 24 |
| [1959_region_36.html](../supplementary/additional_data_analysis/raw_sources/1959_region_36.html) | 1959 regional education table, Demoscope entry 36 |
| [1959_region_52.html](../supplementary/additional_data_analysis/raw_sources/1959_region_52.html) | 1959 regional education table, Demoscope entry 52 |
| [1959_source.xls](../supplementary/additional_data_analysis/raw_sources/1959_source.xls) | Demoscope regional education workbook for 1959 |
| [census1920_preliminary.pdf](../supplementary/additional_data_analysis/raw_sources/census1920_preliminary.pdf) | Preliminary 1920 census results for European Russian provinces |
| [istmat_18139.html](../supplementary/additional_data_analysis/raw_sources/istmat_18139.html) | Saved Historical Materials source page, record 18139 |
| [istmat_18140.html](../supplementary/additional_data_analysis/raw_sources/istmat_18140.html) | Saved Historical Materials source page, record 18140 |
| [istmat_18145.html](../supplementary/additional_data_analysis/raw_sources/istmat_18145.html) | Saved Historical Materials source page, record 18145 |
| [istmat_27236.html](../supplementary/additional_data_analysis/raw_sources/istmat_27236.html) | Saved Historical Materials source page, record 27236 |
| [istmat_27934.html](../supplementary/additional_data_analysis/raw_sources/istmat_27934.html) | Saved Historical Materials source page, record 27934 |
| [khakassia_guide.pdf](../supplementary/additional_data_analysis/raw_sources/khakassia_guide.pdf) | National Archive of Khakassia finding aid |
| [pskov1920_page_13.jpg](../supplementary/additional_data_analysis/raw_sources/pskov1920_page_13.jpg) | Pskov 1920 census page image 13 |
| [pskov1920_page_3.jpg](../supplementary/additional_data_analysis/raw_sources/pskov1920_page_3.jpg) | Pskov 1920 census page image 3 |
| [pskov1920_page_5.jpg](../supplementary/additional_data_analysis/raw_sources/pskov1920_page_5.jpg) | Pskov 1920 census page image 5 |
| [pskov1920_page_7.jpg](../supplementary/additional_data_analysis/raw_sources/pskov1920_page_7.jpg) | Pskov 1920 census page image 7 |
| [pskov1920_page_9.jpg](../supplementary/additional_data_analysis/raw_sources/pskov1920_page_9.jpg) | Pskov 1920 census page image 9 |
| [shpl_1920.html](../supplementary/additional_data_analysis/raw_sources/shpl_1920.html) | Historical Library catalogue page for the Pskov census |
| [spravochnik_1931_obrazovanie.pdf](../supplementary/additional_data_analysis/raw_sources/spravochnik_1931_obrazovanie.pdf) | Education section of the 1931 statistical handbook |
| [tatarstan_1926_book.pdf](../supplementary/additional_data_analysis/raw_sources/tatarstan_1926_book.pdf) | Essays on the Economic Geography of the Tatar Republic |

## supplementary/additional_data_analysis/scripts

| File | Contents |
|---|---|
| [analyze_new_data.py](../supplementary/additional_data_analysis/scripts/analyze_new_data.py) | Extract regional education, migration and time-use tables |
| [estimate_post1939.py](../supplementary/additional_data_analysis/scripts/estimate_post1939.py) | Estimate regional changes in the female-minus-male gap in 1939-1959 |
| [inference.py](../supplementary/additional_data_analysis/scripts/inference.py) | Calculate cluster inference for weighted least-squares contrasts |
| [make_plot.py](../supplementary/additional_data_analysis/scripts/make_plot.py) | Plot regional cohort literacy in 1939 and 1959 |
| [verify_1939_values.py](../supplementary/additional_data_analysis/scripts/verify_1939_values.py) | Compare the 1939 cohort inputs with saved Demoscope source tables |

## supplementary/likbez_1924_analysis

| File | Contents |
|---|---|
| [README.md](../supplementary/likbez_1924_analysis/README.md) | Literacy institutions in 1924 |
| [institution_predictor_models.csv](../supplementary/likbez_1924_analysis/institution_predictor_models.csv) | Twelve institutional female-share specifications |
| [institution_scale_models.csv](../supplementary/likbez_1924_analysis/institution_scale_models.csv) | Twelve institution-count and teacher-count specifications |
| [likbez1924_transcription.csv](../supplementary/likbez_1924_analysis/likbez1924_transcription.csv) | Thirty institutional survey rows with source and validation flags |
| [linked1924_exposure_cohort_outcomes.csv](../supplementary/likbez_1924_analysis/linked1924_exposure_cohort_outcomes.csv) | Fourteen territories with institutional predictors and later cohort outcomes |
| [policy1931_age_sensitivity.csv](../supplementary/likbez_1924_analysis/policy1931_age_sensitivity.csv) | Eight estimates with and without intermediate ages 33-37 |
| [reproduction_check.json](../supplementary/likbez_1924_analysis/reproduction_check.json) | Results of rerunning the packaged analysis |
| [requirements.txt](../supplementary/likbez_1924_analysis/requirements.txt) | Python packages for the analysis |
| [source_manifest.json](../supplementary/likbez_1924_analysis/source_manifest.json) | Source URLs, file sizes and SHA-256 hashes |
| [survey_coverage_and_female_participation.png](../supplementary/likbez_1924_analysis/survey_coverage_and_female_participation.png) | Survey coverage and female shares in the 1924 institutions |
| [transcription_validation.json](../supplementary/likbez_1924_analysis/transcription_validation.json) | Arithmetic checks on the 1924 survey transcription |

## supplementary/likbez_1924_analysis/inputs

| File | Contents |
|---|---|
| [W2_cells.csv](../supplementary/likbez_1924_analysis/inputs/W2_cells.csv) | Main rural cohort sample used by the 1926-1939 regressions |

## supplementary/likbez_1924_analysis/raw_sources

| File | Contents |
|---|---|
| [downloads.json](../supplementary/likbez_1924_analysis/raw_sources/downloads.json) | Download addresses and retrieval records |
| [education1924-67.png](../supplementary/likbez_1924_analysis/raw_sources/education1924-67.png) | Table XVII page image, PDF page 67 |
| [education1924-68.png](../supplementary/likbez_1924_analysis/raw_sources/education1924-68.png) | Table XVII page image, PDF page 68 |
| [education1924-69.png](../supplementary/likbez_1924_analysis/raw_sources/education1924-69.png) | Table XVII page image, PDF page 69 |
| [education_1924.pdf](../supplementary/likbez_1924_analysis/raw_sources/education_1924.pdf) | 1924 education survey, downloaded publication section |
| [kult1930_34_polit.pdf](../supplementary/likbez_1924_analysis/raw_sources/kult1930_34_polit.pdf) | Political-education statistics for 1930-1934 |
| [kultstroy1935_adults.pdf](../supplementary/likbez_1924_analysis/raw_sources/kultstroy1935_adults.pdf) | Adult-school statistics for 1935 |
| [plan1931_page62.png](../supplementary/likbez_1924_analysis/raw_sources/plan1931_page62.png) | Page image used to check the 1931 age priorities |
| [plan_sssr_1931.pdf](../supplementary/likbez_1924_analysis/raw_sources/plan_sssr_1931.pdf) | National economic plan for 1931 |

## supplementary/likbez_1924_analysis/scripts

| File | Contents |
|---|---|
| [analyze_1924.py](../supplementary/likbez_1924_analysis/scripts/analyze_1924.py) | Extract literacy institutions from Table XVII of the 1924 survey |
| [estimate_1924.py](../supplementary/likbez_1924_analysis/scripts/estimate_1924.py) | Estimate institutional correlates and the intermediate-cohort age check |
| [inference.py](../supplementary/likbez_1924_analysis/scripts/inference.py) | Calculate cluster inference for weighted least-squares contrasts |
| [plot_1924.py](../supplementary/likbez_1924_analysis/scripts/plot_1924.py) | Plot survey coverage and female participation in literacy schools |

## validation

| File | Contents |
|---|---|
| [1939_unresolved_70plus_cells.csv](../validation/1939_unresolved_70plus_cells.csv) | Inconsistent 1939 source cells outside the matched age windows |
| [README.md](../validation/README.md) | Source and numerical checks |
| [article_pdf_build.json](../validation/article_pdf_build.json) | PDF hashes, source hashes and TeX build settings |
| [article_pdf_quality.json](../validation/article_pdf_quality.json) | Page counts and recorded PDF inspection results |
| [fresh_source_matches.csv](../validation/fresh_source_matches.csv) | Population and illiteracy values compared with saved source pages |
| [manuscript_files.json](../validation/manuscript_files.json) | The TeX source files checked against the reported numbers |
| [number_changes.csv](../validation/number_changes.csv) | Numerical values before and after the territorial correction |
| [release_checks.json](../validation/release_checks.json) | Results of the source, sample and numerical checks |
| [runtime_versions.json](../validation/runtime_versions.json) | Software versions used for the replication checks |
| [scope_corrections.csv](../validation/scope_corrections.csv) | City and oblast population adjustments for the 1939 join |

## validation/source_checks

| File | Contents |
|---|---|
| [age_35.html](../validation/source_checks/age_35.html) | 1939 population-by-age source table, entry 35 |
| [age_38.html](../validation/source_checks/age_38.html) | 1939 population-by-age source table, entry 38 |
| [age_41.html](../validation/source_checks/age_41.html) | 1939 population-by-age source table, entry 41 |
| [age_42.html](../validation/source_checks/age_42.html) | 1939 population-by-age source table, entry 42 |
| [age_index.html](../validation/source_checks/age_index.html) | Demoscope index of the 1939 age tables |
| [ill_48.html](../validation/source_checks/ill_48.html) | 1939 illiteracy source table, entry 48 |
| [ill_51.html](../validation/source_checks/ill_51.html) | 1939 illiteracy source table, entry 51 |
| [ill_54.html](../validation/source_checks/ill_54.html) | 1939 illiteracy source table, entry 54 |
| [ill_55.html](../validation/source_checks/ill_55.html) | 1939 illiteracy source table, entry 55 |
| [ill_index.html](../validation/source_checks/ill_index.html) | Demoscope index of the 1939 illiteracy tables |

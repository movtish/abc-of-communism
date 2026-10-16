*==============================================================================*
*  The ABC of Communism: How Soviet Russia Taught Its Women to Read
*  master do-file
*
*  Regressions of the paper on stata/data (from scripts/export_stata.py).
*  Coefficients go to stata/output/stata_results.dta and .csv under the keys
*  of scripts/paper_numbers.py, compare with scripts/compare_stata.py.
*  Stata 14+, no extra packages (wild bootstrap only if boottest is there).
*
*  Table numbers below are those of the long version (October 2026).
*  Blocks:   1  household regime, 1897-1926        Tables 3, 8A, A1
*            2  Russians across units              Table 4
*            3  differences within units           Tables 5, A3, A4
*            4  differences between nationalities  Table 6
*            5  state regime, 1926-1939            Tables 7, 8B, A2
*            6  two regimes                        Tables 9, A5
*            7  korenizatsiya and convergence      Tables 10, A6
*            8  legacy                             Tables 11, 12, 13, A8, A9
*==============================================================================*
version 14
clear all
set more off
cap set matsize 2000
if _rc set matsize 800
global ROOT ".."   // run from stata/, or put the full path of the repository here
global DTA  "$ROOT/stata/data"
global OUT  "$ROOT/stata/output"
cap mkdir "$OUT"
cap log close
log using "$OUT/ABC_of_Communism.log", replace text
cap which boottest
global HAVE_BOOTTEST = (_rc == 0)

tempname RES
postfile `RES' str40 key double(b se) using "$OUT/stata_results.dta", replace
global RES `RES'

* keep a coefficient under a key
cap program drop keepb
program define keepb
    args key term
    post $RES ("`key'") (_b[`term']) (_se[`term'])
end
* keep a linear combination under a key
cap program drop keepl
program define keepl
    gettoken key expr : 0
    quietly lincom `expr'
    post $RES ("`key'") (r(estimate)) (r(se))
end

*------------------------------------------------------------------------------*
* 1. Household regime: linked cohorts 1897-1926 (Tables 3, 8A, A1)
*------------------------------------------------------------------------------*
use "$DTA/household_cells.dta", clear
encode region, gen(rid)
local B1 `" "33-37" "38-42" "43-47" "48-52" "53-57" "58-62" "'
foreach spec in w1 w1u w1s w1t w1ur {
    local cond `"area == "rural""'
    local wgt "[aw=pop97]"
    local extra ""
    if "`spec'" == "w1u"  local wgt ""
    if "`spec'" == "w1s"  local extra "survival"
    if "`spec'" == "w1t"  local cond `"area == "total""'
    if "`spec'" == "w1ur" local cond `"area == "urban""'
    regress gain ib7.bin##i.female `extra' i.rid if `cond' `wgt', vce(cluster rid)
    local i = 1
    foreach b of local B1 {
        keepb `spec'.m.`b' `i'.bin
        keepb `spec'.d.`b' `i'.bin#1.female
        keepl `spec'.f.`b' `i'.bin + `i'.bin#1.female
        local ++i
    }
    keepb `spec'.fref 1.female
    if "`spec'" == "w1s" keepb w1s.surv survival
}
* pooled: cohorts aged 33-47 against 53-67 (the cohort aged 48-52 is left out)
regress gain i.treated##i.female i.rid if area == "rural" & bin != 4 [aw=pop97], vce(cluster rid)
keepb w1.ddd 1.treated#1.female
keepb w1.dd.men 1.treated
keepl w1.dd.women 1.treated + 1.treated#1.female
if $HAVE_BOOTTEST boottest 1.treated#1.female, reps(999) weighttype(rademacher) nograph
regress gain i.treated##i.female i.rid if area == "rural" & bin != 4 & muslim_region == 0 [aw=pop97], vce(cluster rid)
keepb w1.ddd.nomus 1.treated#1.female
regress gain i.treated##i.female i.rid if area == "rural" & bin != 4 & bin != 1 [aw=pop97], vce(cluster rid)
keepb w1.ddd.noyoung 1.treated#1.female
keepb w1.dd.noyoung 1.treated
* the illiterate of 1897 who were literate in 1926
regress taught ibn.bin ibn.bin#c.female if area == "rural" [aw=illiterate97], noconstant vce(cluster rid)
local i = 1
foreach b in "33-37" "38-42" "43-47" "48-52" "53-57" "58-62" "63-67" {
    keepb w1c.M.`b' `i'.bin
    keepb w1c.dif.`b' `i'.bin#c.female
    keepl w1c.F.`b' `i'.bin + `i'.bin#c.female
    local ++i
}
regress taught i.treated##i.female i.rid if area == "rural" & bin != 4 [aw=illiterate97], vce(cluster rid)
keepb w1c.ddd 1.treated#1.female
keepb w1c.dd.men 1.treated
keepl w1c.dd.women 1.treated + 1.treated#1.female
* ten-year cohorts (Table A1)
use "$DTA/household_tenyear.dta", clear
encode region, gen(rid)
keep if inrange(gain_pp, -30, 40)
foreach spec in base unw surv nomus sr total urban {
    local cond `"area == "rural""'
    local wgt "[aw=pop_1897]"
    local extra ""
    if "`spec'" == "unw"   local wgt ""
    if "`spec'" == "surv"  local extra "survival_ratio"
    if "`spec'" == "nomus" local cond `"area == "rural" & muslim_region == 0"'
    if "`spec'" == "sr"    local cond `"area == "rural" & inrange(survival_ratio, 0.4, 0.8)"'
    if "`spec'" == "total" local cond `"area == "total""'
    if "`spec'" == "urban" local cond `"area == "urban""'
    regress gain_pp ib3.cohort_c##i.female `extra' i.rid if `cond' `wgt', vce(cluster rid)
    keepb a1.`spec'.mA 1.cohort_c
    keepb a1.`spec'.mB 2.cohort_c
    keepb a1.`spec'.fA 1.cohort_c#1.female
    keepb a1.`spec'.fB 2.cohort_c#1.female
}

*------------------------------------------------------------------------------*
* 2. Russians across units (Table 4)
*------------------------------------------------------------------------------*
* baseline is provincial -> cluster by pg
use "$DTA/russians_units.dta", clear
encode pg, gen(pgid)
local BASE "teachers_percap_1911_z agshare_1897_z cwr_z"
foreach coh in 20_24 12_14 40_49 {
    local ck = subinstr("`coh'", "_", "-", .)
    foreach o in gap F M {
        local y = cond("`o'" == "gap", "gender_gap_`coh'", cond("`o'" == "F", "lit_f_`coh'", "lit_m_`coh'"))
        regress `y' `BASE', vce(cluster pgid)
        keepb rus.`o'.`ck'.t teachers_percap_1911_z
        keepb rus.`o'.`ck'.a agshare_1897_z
        keepb rus.`o'.`ck'.c cwr_z
        if "`coh'" == "20_24" {
            regress `y' `BASE' urban_share_m_z, vce(cluster pgid)
            keepb rus.`o'.`ck'.u.t teachers_percap_1911_z
            keepb rus.`o'.`ck'.u.a agshare_1897_z
            keepb rus.`o'.`ck'.u.c cwr_z
            keepb rus.`o'.`ck'.u.u urban_share_m_z
        }
    }
}
regress gender_gap_20_24 urban_share_m_z, vce(cluster pgid)
keepb rus.urb.biv urban_share_m_z
foreach spec in nolow notit noural zem {
    if "`spec'" == "nolow"  local cond "lowq == 0"
    if "`spec'" == "notit"  local cond "autonomous == 0"
    if "`spec'" == "noural" local cond "okrug == 0"
    if "`spec'" == "zem"    local cond "zemstvo_prov == 1"
    regress gender_gap_20_24 `BASE' if `cond', vce(cluster pgid)
    keepb rus.rob.`spec'.t teachers_percap_1911_z
    keepb rus.rob.`spec'.c cwr_z
}
regress gender_gap_20_24 exp_zemstvo_edu_pc_1894_z agshare_1897_z cwr_z, vce(cluster pgid)
keepb rus.alt.spend exp_zemstvo_edu_pc_1894_z
regress gender_gap_20_24 per_lit_f_z agshare_1897_z cwr_z, vce(cluster pgid)
keepb rus.alt.lit97 per_lit_f_z
* leave-one-unit-out for the coefficient on teachers
quietly count
local N = r(N)
gen long obs = _n
forvalues i = 1/`N' {
    quietly regress gender_gap_20_24 `BASE' if obs != `i', vce(robust)
    if e(N) < . di "without unit `i': teachers " %6.2f _b[teachers_percap_1911_z] "  child-woman ratio " %6.2f _b[cwr_z]
}

*------------------------------------------------------------------------------*
* 3. Differences within units (Tables 5, A3, A4)
*------------------------------------------------------------------------------*
cap program drop withinunits
program define withinunits
    args file key cond wgt y
    use "$DTA/`file'.dta", clear
    if "`cond'" != "" & "`cond'" != "." keep if `cond'
    encode region, gen(rid)
    egen rcid = group(rc)
    egen gcid = group(gc)
    egen scid = group(sc)
    if "`wgt'" == "none" local w ""
    else local w "[aw=population]"
    regress `y' i.rcid i.gcid i.scid vf vfy mf mfy `w', vce(cluster rid)
    keepb `key'.vf vf
    keepb `key'.vfy vfy
    keepb `key'.mf mf
    keepb `key'.mfy mfy
    keepl `key'.vyoung vf + vfy
    keepl `key'.myoung mf + mfy
end
use "$DTA/within_cells.dta", clear
encode region, gen(rid)
egen rcid = group(rc)
foreach y in literacy logodds {
    local k = cond("`y'" == "literacy", "dec", "decl")
    regress `y' i.rcid i.band_n#c.female i.band_n#c.volga i.band_n#c.muslim i.band_n#c.volga#c.female i.band_n#c.muslim#c.female [aw=population], vce(cluster rid)
    local i = 1
    foreach b in "40-49" "30-39" "25-29" "20-24" "15-19" "12-14" {
        keepb `k'.f.`b'  `i'.band_n#c.female
        keepb `k'.v.`b'  `i'.band_n#c.volga
        keepb `k'.m.`b'  `i'.band_n#c.muslim
        keepb `k'.vf.`b' `i'.band_n#c.volga#c.female
        keepb `k'.mf.`b' `i'.band_n#c.muslim#c.female
        keepl `k'.vw.`b' `i'.band_n#c.volga + `i'.band_n#c.volga#c.female
        keepl `k'.mw.`b' `i'.band_n#c.muslim + `i'.band_n#c.muslim#c.female
        local ++i
    }
}
* men alone and women alone
foreach sx in M F {
    foreach y in literacy logodds {
        local k = cond("`y'" == "literacy", "sx", "sxl")
        regress `y' i.rcid c.volga c.volga#c.young c.muslim c.muslim#c.young if sex == "`sx'" [aw=population], vce(cluster rid)
        keepb `k'.`sx'.v volga
        keepb `k'.`sx'.vy c.volga#c.young
        keepl `k'.`sx'.vyoung volga + c.volga#c.young
    }
}
withinunits within_cells ddd        .                 pop literacy
if $HAVE_BOOTTEST boottest vfy, reps(999) weighttype(rademacher) nograph
withinunits within_cells dddl       .                 pop logodds
withinunits within_cells ddd.nolow  "lowq == 0"       pop literacy
withinunits within_cells ddd.300    "population >= 300" pop literacy
withinunits within_cells ddd.unw    .                 none literacy
withinunits within_cells ddd.notit  "autonomous == 0" pop literacy
withinunits within_cells ddd.with   "with_nat == 1"   pop literacy
withinunits within_cells ddd.strict "inlist(tier, 1, 2)" pop literacy
withinunits within_cells_total ddd.total .            pop literacy
* all nationalities, and one dummy for non-Russians
use "$DTA/within_cells_all.dta", clear
encode region, gen(rid)
egen rcid = group(rc)
egen gcid = group(gc)
egen scid = group(sc)
regress literacy i.rcid i.gcid i.scid vf vfy mf mfy of ofy [aw=population], vce(cluster rid)
keepb ddd.all.vf vf
keepb ddd.all.vfy vfy
keepb ddd.all.mf mf
keepb ddd.all.mfy mfy
regress literacy i.rcid i.gcid i.scid nr_f nr_f_m [aw=population], vce(cluster rid)
keepb ddd.pooled.nrf nr_f
keepb ddd.pooled.nrfm nr_f_m

*------------------------------------------------------------------------------*
* 4. Differences between nationalities (Table 6)
*------------------------------------------------------------------------------*
use "$DTA/nationalities_cells.dta", clear
encode region, gen(rid)
local G2 "cwr_diff_z sr_20_39_diff_z urban_share_m_diff_z muslim"
local G1 "cwr_diff_z sr_20_39_diff_z mob_gap_diff_z muslim"
foreach o in F M G {
    local y = cond("`o'" == "F", "ethgap_f_20_24", cond("`o'" == "M", "ethgap_m_20_24", "ethgap_f_12_14"))
    regress `y' `G2' [aw=pop], vce(cluster rid)
    keepb mech.`o'.u.u urban_share_m_diff_z
    keepb mech.`o'.u.c cwr_diff_z
    keepb mech.`o'.u.s sr_20_39_diff_z
    keepb mech.`o'.u.m muslim
    regress `y' `G2' i.rid [aw=pop], vce(cluster rid)
    keepb mech.`o'.ufe.u urban_share_m_diff_z
    regress `y' `G2', vce(cluster rid)
    keepb mech.`o'.uunw.u urban_share_m_diff_z
    regress `y' `G1' [aw=pop], vce(cluster rid)
    keepb mech.`o'.g.g mob_gap_diff_z
}

*------------------------------------------------------------------------------*
* 5. State regime: linked cohorts 1926-1939 (Tables 7, 8B, A2)
*------------------------------------------------------------------------------*
cap program drop stateregime
program define stateregime
    args file key cond wgt extra
    use "$DTA/`file'.dta", clear
    if "`cond'" != "" & "`cond'" != "." keep if `cond'
    * both sexes of a cohort must be present
    bysort unit_1926 age_1926: gen nsex = _N
    keep if nsex == 2
    encode unit_1926, gen(uid)
    if "`wgt'" == "none" local w ""
    else local w "[aw=pop_1926]"
    if "`extra'" == "." local extra ""
    regress gain_pp ib8.coh_c##i.female `extra' i.uid `w', vce(cluster uid)
    local i = 1
    foreach b in "18-22" "23-27" "28-32" "33-37" "38-42" "43-47" "48-52" {
        keepb `key'.m.`b' `i'.coh_c
        keepb `key'.d.`b' `i'.coh_c#1.female
        keepl `key'.f.`b' `i'.coh_c + `i'.coh_c#1.female
        local ++i
    }
    keepb `key'.fref 1.female
    if "`extra'" == "survival" keepb w2r.surv.coef survival
    regress gain_pp i.coh_c female fm fy `extra' i.uid `w', vce(cluster uid)
    keepb `key'.ddd fy
    keepb `key'.ddm fm
    regress gain_pp i.coh_c female fy `extra' i.uid if placebo == 0 `w', vce(cluster uid)
    keepb `key'.ddd33 fy
    * effect by sex, 18-32 vs above the age limit, points and share taught
    if "`wgt'" == "none" local wt ""
    else local wt "[aw=illiterate26]"
    regress gain_pp c.young##c.female c.middle##c.female `extra' i.uid `w', vce(cluster uid)
    keepb `key'.pm young
    keepl `key'.pw young + c.young#c.female
    keepb `key'.pd c.young#c.female
    regress taught c.young##c.female c.middle##c.female `extra' i.uid `wt', vce(cluster uid)
    keepb `key'.tm young
    keepl `key'.tw young + c.young#c.female
    keepb `key'.td c.young#c.female
end
stateregime state_cells w2 . pop .
use "$DTA/state_cells.dta", clear
encode unit_1926, gen(uid)
regress gain_pp i.coh_c female fm fy i.uid [aw=pop_1926], vce(cluster uid)
if $HAVE_BOOTTEST boottest fy, reps(999) weighttype(rademacher) nograph
regress gain_pp c.age1928##c.female i.uid if placebo == 0 [aw=pop_1926], vce(cluster uid)
keepb w2.age.m age1928
keepb w2.age.fx c.age1928#c.female
keepl w2.age.f age1928 + c.age1928#c.female
* leave-one-unit-out
levelsof uid, local(units)
foreach u of local units {
    quietly regress gain_pp i.coh_c female fm fy i.uid if uid != `u' [aw=pop_1926], vce(cluster uid)
    di "without unit `u': female x aged 18-32 = " %5.2f _b[fy]
}
* the illiterate of 1926 who were literate in 1939
regress taught ibn.coh_c ibn.coh_c#c.female [aw=illiterate26], noconstant vce(cluster uid)
local i = 1
foreach b in "18-22" "23-27" "28-32" "33-37" "38-42" "43-47" "48-52" "53-57" {
    keepb w2c.M.`b' `i'.coh_c
    keepb w2c.dif.`b' `i'.coh_c#c.female
    keepl w2c.F.`b' `i'.coh_c + `i'.coh_c#c.female
    local ++i
}
regress taught i.coh_c female fm fy i.uid [aw=illiterate26], vce(cluster uid)
keepb w2c.ddd fy
keepb w2c.ddm fm
regress taught c.young##c.female c.middle##c.female i.uid [aw=illiterate26], vce(cluster uid)
keepb w2c.dd.men young
keepl w2c.dd.women young + c.young#c.female
keepb w2c.dd.dif c.young#c.female
regress taught c.age1928##c.female i.uid if placebo == 0 [aw=illiterate26], vce(cluster uid)
keepb w2c.age.m age1928
keepl w2c.age.f age1928 + c.age1928#c.female
* robustness (Table A2)
stateregime state_cells         w2r.base  .                               pop  .
stateregime state_cells_flagged w2r.flag  .                               pop  .
stateregime state_cells         w2r.surv  .                               pop  survival
stateregime state_cells         w2r.sr    "inrange(survival, 0.6, 1.15)"  pop  .
stateregime state_cells         w2r.unw   .                               none .
stateregime state_cells         w2r.rus   "titular == 0"                  pop  .
stateregime state_cells         w2r.tit   "titular == 1"                  pop  .
stateregime state_cells         w2r.ural  "ural == 0"                     pop  .
stateregime state_cells         w2r.mus   "tatbash == 0"                  pop  .
stateregime state_cells         w2r.low   "lowq == 0"                     pop  .
stateregime state_cells         w2r.t1    "tier == 1"                     pop  .
stateregime state_cells         w2r.full  "ncoh == 8"                     pop  .
stateregime state_cells_total   w2r.total .                               pop  .
* replication on the Gosplan regions
use "$DTA/state_region_cells.dta", clear
encode rayon, gen(rid)
regress gain_pp i.coh_c female fm fy i.rid [aw=pop_1926], vce(cluster rid)
keepb ray.ddd fy
keepb ray.ddm fm
regress gain_pp i.coh_c female fm fy i.rid if approx_borders == 0 [aw=pop_1926], vce(cluster rid)
keepb ray.ddd.exact fy
regress gain_pp c.age1928##c.female i.rid if age_1926 != "50-54" [aw=pop_1926], vce(cluster rid)
keepb ray.age.m age1928
keepb ray.age.fx c.age1928#c.female
* regions: all (ray), unchanged borders (rayx)
foreach k in ray rayx {
    local cond ""
    if "`k'" == "rayx" local cond "if approx_borders == 0"
    regress gain_pp c.young##c.female c.middle##c.female i.rid `cond' [aw=pop_1926], vce(cluster rid)
    keepb `k'.pm young
    keepl `k'.pw young + c.young#c.female
    keepb `k'.pd c.young#c.female
    regress taught c.young##c.female c.middle##c.female i.rid `cond' [aw=illiterate26], vce(cluster rid)
    keepb `k'.tm young
    keepl `k'.tw young + c.young#c.female
    keepb `k'.td c.young#c.female
}

*------------------------------------------------------------------------------*
* 6. Two regimes (Tables 9, A5)
*------------------------------------------------------------------------------*
cap program drop tworeg
program define tworeg
    args file key cond wgt
    use "$DTA/`file'.dta", clear
    if "`cond'" != "" & "`cond'" != "." keep if `cond'
    encode unit, gen(uid)
    encode pg, gen(pgid)
    egen upid = group(up)
    egen cfid = group(cohfe)
    if "`wgt'" == "none" local w ""
    else local w "[aw=wt]"
    foreach p in t c u a {
        if "`p'" == "t" local v "teachers_percap_1911_z"
        if "`p'" == "c" local v "cwr_z"
        if "`p'" == "u" local v "urban_share_m_z"
        if "`p'" == "a" local v "agshare_1897_z"
        cap drop z
        gen double z = `v'
        regress y i.upid i.cfid c.female c.female#c.phase2 c.reach#c.female c.reach#c.female#c.phase2 c.reach#c.z c.reach#c.z#c.phase2 ///
                c.female#c.z c.female#c.z#c.phase2 c.reach#c.female#c.z c.reach#c.female#c.z#c.phase2 if !missing(z) `w', vce(cluster pgid)
        keepb `key'.`p'.1 c.reach#c.female#c.z
        keepl `key'.`p'.2 c.reach#c.female#c.z + c.reach#c.female#c.z#c.phase2
        keepb `key'.`p'.d c.reach#c.female#c.z#c.phase2
    }
end
tworeg tworegime_cells        tr  .           wt
tworeg tworegime_cells_middle trb .           wt
tworeg tworegime_cells        trl "lowq == 0" wt
tworeg tworegime_cells        tru .           none
tworeg tworegime_cells_taught trc .           wt
* unit level
use "$DTA/household_units.dta", clear
encode pg, gen(pgid)
foreach p in t c u a {
    if "`p'" == "t" local v "teachers_percap_1911_z"
    if "`p'" == "c" local v "cwr_z"
    if "`p'" == "u" local v "urban_share_m_z"
    if "`p'" == "a" local v "agshare_1897_z"
    regress w1_f `v', vce(cluster pgid)
    keepb tru1.F.`p' `v'
}
use "$DTA/state_units.dta", clear
encode pg, gen(pgid)
foreach p in t c u a {
    if "`p'" == "t" local v "teachers_percap_1911_z"
    if "`p'" == "c" local v "cwr_z"
    if "`p'" == "u" local v "urban_share_m_z"
    if "`p'" == "a" local v "agshare_1897_z"
    regress gain_f lit26_f_z `v' [aw=pop], vce(cluster pgid)
    keepb tru2.F.`p' `v'
    regress gain_m lit26_m_z `v' [aw=pop], vce(cluster pgid)
    keepb tru2.M.`p' `v'
}
regress gain_f lit26_f_z [aw=pop], vce(cluster pgid)
keepb tru2.F.own lit26_f_z
regress gain_m lit26_m_z [aw=pop], vce(cluster pgid)
keepb tru2.M.own lit26_m_z

*------------------------------------------------------------------------------*
* 7. Korenizatsiya and convergence (Tables 10, A6)
*------------------------------------------------------------------------------*
use "$DTA/korenizatsiya_cells.dta", clear
encode region, gen(rid)
egen rcid = group(rc)
egen gscid = group(gsc)
gen ts = titular_unit * soviet
gen tf = titular_unit * female
gen tsf = titular_unit * soviet * female
regress literacy i.gscid i.rcid titular_unit ts tf tsf [aw=population], vce(cluster rid)
keepb kor.t titular_unit
keepb kor.ts ts
keepb kor.tf tf
keepb kor.tsf tsf
regress literacy i.gscid i.rcid titular_unit ts tf tsf if group != "Татары" [aw=population], vce(cluster rid)
keepb kor.notat.t titular_unit
keepb kor.notat.ts ts
keepb kor.notat.tf tf
keepb kor.notat.tsf tsf
use "$DTA/state_units.dta", clear
regress gain_f lit26_f [aw=pop], vce(robust)
keepb w2u.F0.lit26_F lit26_f
regress gain_f lit26_f titular [aw=pop], vce(robust)
keepb w2u.F1.lit26_F lit26_f
keepb w2u.F1.titular titular
regress gain_f lit26_f titular surv [aw=pop], vce(robust)
keepb w2u.F2.titular titular
regress gain_f lit26_f titular if tatbash == 0 [aw=pop], vce(robust)
keepb w2u.F3.titular titular
regress gain_f lit26_f titular, vce(robust)
keepb w2u.F4.titular titular
regress gain_m lit26_m [aw=pop], vce(robust)
keepb w2u.M0.lit26_M lit26_m
regress gain_m lit26_m titular [aw=pop], vce(robust)
keepb w2u.M1.lit26_M lit26_m
keepb w2u.M1.titular titular
use "$DTA/state_units_1832.dta", clear
regress gain_f lit26_f titular [aw=pop], vce(robust)
keepb w2u.F5.titular titular
use "$DTA/state_cells.dta", clear
encode unit_1926, gen(uid)
gen yt = young * titular
gen mt = middle * titular
gen ft = female * titular
gen fmt = fm * titular
gen fyt = fy * titular
regress gain_pp i.uid i.coh_c female fm fy yt mt ft fmt fyt [aw=pop_1926], vce(cluster uid)
keepb w2.tit.ddd fyt

*------------------------------------------------------------------------------*
* 8. Legacy (Tables 11, 12, 13, A8, A9)
*------------------------------------------------------------------------------*
* the difference between the female and the male gap of 2010 by cohort
use "$DTA/legacy_cohorts_2010.dta", clear
encode nat, gen(nid)
encode age, gen(aid)
egen naid = group(na)
regress gap_sec i.nid i.aid female fmid fo [aw=pop], vce(cluster nid)
keepb c10.a.y female
keepb c10.a.m fmid
keepb c10.a.o fo
regress gap_sec i.naid female fmid fo [aw=pop], vce(cluster nid)
keepb c10.b.y female
keepb c10.b.m fmid
keepb c10.b.o fo
regress gap_higher i.nid i.aid female fmid fo [aw=pop], vce(cluster nid)
keepb c10.h.y female
keepb c10.h.m fmid
keepb c10.h.o fo
* the sex difference of 1926 and of 2010
cap program drop sexdiff
program define sexdiff
    args key cond wgt y x
    use "$DTA/legacy_sexdiff_cells.dta", clear
    if "`cond'" != "" & "`cond'" != "." keep if `cond'
    drop if missing(`x')
    encode nat, gen(nid)
    egen naid = group(na)
    egen said = group(sa)
    gen double fx = female * `x'
    gen double fxm = fmid * `x'
    gen double fxo = fo * `x'
    if "`wgt'" == "none" local w ""
    else local w "[aw=pop]"
    regress `y' i.naid i.said fx fxm fxo `w', vce(cluster nid)
    keepb `key'.y fx
    keepl `key'.m fx + fxm
    keepl `key'.o fx + fxo
    keepb `key'.d fxo
end
local SIX `"inlist(nat, "Татары", "Башкиры", "Чуваши", "Марийцы", "Удмурты", "Мордва")"'
sexdiff sd.six     `"`SIX'"'  pop  gap_sec    d_ad
sexdiff sd.all     .          pop  gap_sec    d_ad
sexdiff sd.nm      `"!inlist(nat, "Татары", "Башкиры", "Казахи")"' pop gap_sec d_ad
sexdiff sd.six.unw `"`SIX'"'  none gap_sec    d_ad
sexdiff sd.six.yg  `"`SIX'"'  pop  gap_sec    d_yg
sexdiff sd.six.h   `"`SIX'"'  pop  gap_higher d_ad
sexdiff sd.six.b   `"`SIX'"'  pop  gap_basic  d_ad
* nationalities within regions
cap program drop legacy
program define legacy
    args key area cond wgt y f m extra
    use "$DTA/legacy_subject_cells.dta", clear
    keep if area == "`area'"
    if "`cond'" != "" & "`cond'" != "." keep if `cond'
    encode subject, gen(sid)
    encode nat2010, gen(nid)
    if "`wgt'" == "none" local w ""
    else local w "[aw=stated]"
    if "`extra'" == "." local extra ""
    if "`extra'" == "nofe" local fe ""
    else local fe "i.sid"
    if "`extra'" == "nofe" local extra ""
    local rhs ""
    if "`f'" != "." local rhs "`rhs' `f'"
    if "`m'" != "." local rhs "`rhs' `m'"
    regress `y' `rhs' `extra' `fe' `w', vce(cluster sid)
    local sfx = cond("`area'" == "rural", ".r", "")
    if "`f'" != "." keepb `key'`sfx'.F `f'
    if "`m'" != "." keepb `key'`sfx'.M `m'
end
foreach a in total rural {
    legacy leg.nofe  `a' . pop g10 gf gm nofe
    legacy leg       `a' . pop g10 gf gm .
    legacy leg.fo    `a' . pop g10 gf .  .
    legacy leg.mo    `a' . pop g10 .  gm .
    legacy leg.2029  `a' . pop g10 gf2029 gm2029 .
    legacy leg.3049  `a' . pop g10 gf3049 gm3049 .
    legacy leg.1219  `a' . pop g10 gf1219 gm1219 .
    legacy leg.h     `a' . pop g10h gf gm .
    legacy leg.kal   `a' `"nat2010 != "Калмыки""' pop g10 gf gm .
    legacy leg.ugk   `a' `"!inlist(nat2010, "Украинцы", "Немцы", "Казахи")"' pop g10 gf gm .
    legacy leg.six   `a' "six == 1" pop g10 gf gm .
    legacy leg.unw   `a' . none g10 gf gm .
    legacy leg.adj   `a' . pop g10adj gf gm .
    legacy leg.rur   `a' . pop g10 gf gm rural_diff
    legacy leg.mt    `a' . pop g10 gf gm "muslim titular"
    legacy leg.nm    `a' "muslim == 0" pop g10 gf gm .
    legacy leg.nmfo  `a' "muslim == 0" pop g10 gf . .
    legacy leg.nmmo  `a' "muslim == 0" pop g10 . gm .
    legacy leg.natfe `a' . pop g10 gf gm "i.nid"
    legacy leg.illit `a' . pop g10i gf gm .
}
use "$DTA/legacy_subject_cells.dta", clear
keep if area == "total"
encode subject, gen(sid)
regress g10 gf gm i.sid [aw=stated], vce(cluster sid)
if $HAVE_BOOTTEST boottest gf, reps(1999) weighttype(rademacher) nograph
levelsof sid, local(subs)
foreach s of local subs {
    quietly regress g10 gf gm i.sid if sid != `s' [aw=stated], vce(cluster sid)
    di "without subject `s': beta_F = " %5.3f _b[gf]
}
* children of 1939
use "$DTA/children_1939.dta", clear
regress kid39f gf kid26f [aw=kidpop], vce(robust)
keepb ig.1.gF gf
regress kid39f gf gm kid26f [aw=kidpop], vce(robust)
keepb ig.2.gF gf
keepb ig.2.gM gm
regress kid39m gf gm kid26m [aw=kidpop], vce(robust)
keepb ig.3.gF gf
regress gap39 gf gm gap26 [aw=kidpop], vce(robust)
keepb ig.4.gF gf

postclose `RES'
use "$OUT/stata_results.dta", clear
export delimited using "$OUT/stata_results.csv", replace delimiter(";")
di as txt "Coefficients saved: " _N
log close

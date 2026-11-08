import pathlib,sys,json,warnings
import numpy as np,pandas as pd
from scipy import stats
from inference import Model
warnings.filterwarnings('ignore');sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parent
SOURCE=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent
OUT=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'results';OUT.mkdir(exist_ok=True)
def read(name):return pd.read_csv(SOURCE/'results'/name,sep=';',encoding='utf-8-sig')
rows=[];errors=[]
def estimate(label,formula,d,w,cluster,terms,heavy=True,B=0):
    try:
        m=Model(formula,d,w,cluster)
        r=m.evaluate(terms,cr2=heavy,jackknife=heavy,bootstrap=B)
        r.update(model=label,formula=formula,weight=w,cluster=cluster,contrast=json.dumps(terms))
        rows.append(r);print(label, 'b=',round(r['b'],4),'CR1 p=',round(r['p_cr1'],5),'CR2 p=',r.get('p_cr2'),'df2=',r.get('df_cr2'),'WCR=',r.get('wcr_p'),flush=True)
        pd.DataFrame(rows).to_csv(OUT/'estimates.csv',sep=';',index=False,encoding='utf-8-sig')
        return m,r
    except Exception as e:
        errors.append(dict(model=label,error=str(e)));print('ERROR',label,str(e),flush=True);return None,None

d=read('W2_cells.csv');d['age']=d.age_1926.str[:2].astype(int)+2;d['us']=d.unit_1926+'|'+d.sex;d['uc']=d.unit_1926+'|'+d.age_1926
d['conv']=100*d.gain_pp/(100-d.lit_1926);d['ill']=d.pop_1926*(100-d.lit_1926)/100
F='gain_pp ~ young*female + middle*female + C(unit_1926)';FW={'young':1,'young:female':1};DDD={'young:female':1}
for label,terms in [('female',FW),('male',{'young':1}),('DDD',DDD)]:estimate('main_'+label,F,d,'pop_1926','region_1939',terms,B=9999)
estimate('main_DDD_unitsex','gain_pp ~ young*female + middle*female + C(us)',d,'pop_1926','region_1939',DDD,B=9999)
estimate('main_DDD_unitsex_unitcohort','gain_pp ~ C(us) + C(uc) + fy + fm',d,'pop_1926','region_1939',{'fy':1},B=9999)
for sex in ['F','M']:
 estimate('sex_specific_'+sex,'gain_pp ~ young + middle + C(unit_1926)',d[d.sex==sex],'pop_1926','region_1939',{'young':1})
for label,s in [('unweighted',d),('tier1',d[d.tier==1]),('complete8',d[d.groupby('unit_1926').age_1926.transform('nunique')==8]),('no_ural',d[~d.unit_1926.str.contains('округ')]),('survival',d[d.survival.between(.6,1.15)]),('russian_units',d[~d.unit_1926.str.contains('АССР|АО')])]:
 s=s[s.groupby(['unit_1926','age_1926']).sex.transform('nunique')==2]
 for name,terms in [('female',FW),('DDD',DDD)]:estimate('rob_'+label+'_'+name,F,s,None if label=='unweighted' else 'pop_1926','region_1939',terms)
for ref in ['48-52','53-57']:
 s=d[(d.young==1)|(d.age_1926==ref)]
 estimate('reference_'+ref+'_female','gain_pp ~ young*female + C(unit_1926)',s,'pop_1926','region_1939',FW)
 estimate('reference_'+ref+'_DDD','gain_pp ~ young*female + C(us)',s,'pop_1926','region_1939',DDD)
old=d[d.age_1926.isin(['48-52','53-57'])].copy();old['younger_old']=(old.age_1926=='48-52').astype(int)
estimate('old_placebo_sex_difference','gain_pp ~ younger_old*female + C(us)',old,'pop_1926','region_1939',{'younger_old:female':1},B=9999)
for sx in ['F','M']:
 estimate('old_placebo_'+sx,'gain_pp ~ younger_old + C(unit_1926)',old[old.sex==sx],'pop_1926','region_1939',{'younger_old':1})
# These age-trend models are sensitivity checks, not an alternative source of identification.
estimate('age_trend_DDD','gain_pp ~ young*female + middle*female + age*female + C(us)',d,'pop_1926','region_1939',DDD)
estimate('age_trend_female',F+' + age*female',d,'pop_1926','region_1939',FW)
estimate('normalized_female','conv ~ young*female + middle*female + C(unit_1926)',d,'ill','region_1939',FW,B=9999)
estimate('normalized_DDD','conv ~ young*female + middle*female + C(unit_1926)',d,'ill','region_1939',DDD,B=9999)
# Log odds is an outcome-scale sensitivity, not a proportion taught.
d['logchange']=np.log(d.lit_1939.clip(.5,99.5)/(100-d.lit_1939.clip(.5,99.5)))-np.log(d.lit_1926.clip(.5,99.5)/(100-d.lit_1926.clip(.5,99.5)))
estimate('logodds_DDD','logchange ~ young*female + middle*female + C(us)',d,'pop_1926','region_1939',DDD)

ry=read('B9_rayon_cells.csv')
for tag,s in [('all',ry),('exact_borders',ry[ry.approx_borders==0])]:
 for label,terms in [('female',FW),('DDD',DDD)]:estimate('rayon_'+tag+'_'+label,'gain_pp ~ young*female + middle*female + C(rayon)',s,'pop_1926','rayon',terms,B=9999 if tag=='all' else 0)

e=read('E1_wave1_event_cells.csv');e=e[e.area=='rural'].copy();e['young']=e.age_decree.isin(['33-37','38-42','43-47']).astype(int);e=e[e.age_decree!='48-52'];e['rs']=e.region+'|'+e.sex
for lab,terms in [('female',FW),('DDD',DDD)]:estimate('pre1926_'+lab,'gain ~ young*female + C(region)',e,'pop97','region',terms,B=9999)
estimate('pre1926_DDD_unitsex','gain ~ young*female + C(rs)',e,'pop97','region',DDD)
for tag,s in [('exclude_schoolage',e[e.age_decree!='33-37']),('adults20plus',e[~e.age_decree.isin(['33-37','38-42'])])]:
 estimate('pre1926_'+tag+'_female','gain ~ young*female + C(region)',s,'pop97','region',FW)

rb=read('F_russians_units.csv');base='teachers_percap_1911_z + agshare_1897_z + cwr_z'
for outcome in ['gender_gap_20-24','lit_F_20-24','lit_M_20-24']:
 for name in ['teachers_percap_1911_z','cwr_z']:
  estimate('russians_'+outcome+'_'+name,"Q('"+outcome+"') ~ "+base,rb,None,'pg',{name:1},B=9999 if outcome=='gender_gap_20-24' else 0)

kr=read('D_core_cells.csv');FP='literacy ~ C(rc) + C(gc) + C(sc) + vf + vfy + mf + mfy'
for term in ['vf','vfy','mf','mfy']:estimate('ethnic_'+term,FP,kr,'population','region',{term:1},B=9999 if term=='vfy' else 0)
kr['lo']=np.log(kr.literacy.clip(.5,99.5)/(100-kr.literacy.clip(.5,99.5)))
estimate('ethnic_logodds_vfy',FP.replace('literacy ~','lo ~'),kr,'population','region',{'vfy':1})
gm=read('G_mechanism_cells.csv');GF='cwr_diff_z + sr_20_39_diff_z + urban_share_M_diff_z + muslim'
for outcome,tag in [('ethgap_F_20-24','F'),('ethgap_M_20-24','M'),('ethgap_F_12-14','girls')]:
 estimate('within_groups_'+tag+'_urban',"Q('"+outcome+"') ~ "+GF,gm,'pop','region',{'urban_share_M_diff_z':1},B=9999 if tag=='F' else 0)
estimate('within_groups_F_fertility',"Q('ethgap_F_20-24') ~ "+GF,gm,'pop','region',{'cwr_diff_z':1})
estimate('within_groups_F_urban_unweighted',"Q('ethgap_F_20-24') ~ "+GF,gm,None,'region',{'urban_share_M_diff_z':1})
estimate('within_groups_F_urban_regionFE',"Q('ethgap_F_20-24') ~ "+GF+' + C(region)',gm,'pop','region',{'urban_share_M_diff_z':1})
estimate('within_groups_F_mobility_gap',"Q('ethgap_F_20-24') ~ cwr_diff_z + sr_20_39_diff_z + mob_gap_diff_z + muslim",gm,'pop','region',{'mob_gap_diff_z':1})
kor=read('E_korenizatsiya_cells.csv');kor['ts']=kor.titular_unit*kor.soviet;kor['tf_']=kor.titular_unit*kor.female;kor['tsf']=kor.titular_unit*kor.soviet*kor.female
FK='literacy ~ C(gsc) + C(rc) + titular_unit + ts + tf_ + tsf'
for term in ['titular_unit','ts','tsf']:estimate('koren_'+term,FK,kor,'population','region',{term:1})
estimate('koren_no_tatars_ts',FK,kor[kor.group!='Татары'],'population','region',{'ts':1})

tw=read('T_two_regime_cells.csv');TF='y ~ C(up) + C(cohfe) + female + female:phase2 + T:female + T:female:phase2 + T:z + T:z:phase2 + female:z + female:z:phase2 + T:female:z + T:female:z:phase2'
for c in ['teachers_percap_1911_z','urban_share_M_z','cwr_z','agshare_1897_z']:
 s=tw.dropna(subset=[c]).copy();s['z']=s[c]
 estimate('two_regime_change_'+c,TF,s,'wt','pg',{'T:female:z:phase2':1})

# Mechanisms: cross-sectional associations, current urbanization is post-treatment.
mm=read('M_mechanism_regions.csv');mm=mm[mm.sex=='F'].copy();mm['dz']=(mm.dUrb-mm.dUrb.mean())/mm.dUrb.std()
for outcome in ['taught_r','taught_t']:
 for tag,s in [('all',mm),('exact_borders',mm[mm.appr==0]),('no_leningrad',mm[mm.rayon!='Ленинградско-Карельский район'])]:
  estimate('mechanism_'+outcome+'_'+tag,outcome+' ~ dz',s,None,None,{'dz':1},B=9999 if tag=='all' else 0)
  if tag=='all':
   mm[outcome+'_z']=(mm[outcome]-mm[outcome].mean())/mm[outcome].std()
   estimate('mechanism_'+outcome+'_baseline_urban',outcome+' ~ dz + urb26',mm,None,None,{'dz':1})
 # Equivalence diagnostic for a substantive +/-5 pp per SD margin.
 _,r=estimate('mechanism_'+outcome+'_HC3_equiv',outcome+' ~ dz',mm,None,None,{'dz':1},heavy=False)
 if r:
  import statsmodels.formula.api as smf
  rr=smf.ols(outcome+' ~ dz',mm).fit(cov_type='HC3',use_t=True)
  b=rr.params['dz'];se=rr.bse['dz'];df=rr.df_resid
  pd.DataFrame([dict(outcome=outcome,b=b,se_HC3=se,ci90_low=b-stats.t.ppf(.95,df)*se,ci90_high=b+stats.t.ppf(.95,df)*se,margin=5,p_TOST=max(stats.t.sf((b+5)/se,df),stats.t.cdf((b-5)/se,df)))]).to_csv(OUT/('equivalence_'+outcome+'.csv'),sep=';',index=False,encoding='utf-8-sig')

leg=read('J2_ethnic_gaps_1926_2010.csv');leg=leg[leg.area=='total']
for term in ['gF','gM']:
 estimate('legacy_'+term,'g10 ~ gF + gM + C(subject)',leg,'stated','subject',{term:1},B=9999)
 estimate('legacy_nationality_FE_'+term,'g10 ~ gF + gM + C(subject) + C(nat2010)',leg,'stated','subject',{term:1})
 # Repeated ethnic shocks: nationality clustering is a separate sensitivity.
 estimate('legacy_natcluster_'+term,'g10 ~ gF + gM + C(subject)',leg,'stated','nat2010',{term:1})
sd=read('S_legacy_sexdiff_cells.csv');six=['Татары','Башкиры','Чуваши','Марийцы','Удмурты','Мордва']
for tag,s in [('all',sd),('six',sd[sd.nat.isin(six)])]:
 s=s.copy();s['fx']=s.female*s.D_ad;s['fxm']=s.fmid*s.D_ad;s['fxo']=s.fo*s.D_ad
 estimate('legacy_sexdiff_'+tag,'gap_sec ~ C(na) + C(sa) + fx + fxm + fxo',s,'pop','nat',{'fx':1,'fxo':1},B=9999)

ig=read('I_intergen_units.csv')
for term in ['gF','kid26F']:estimate('intergeneration_'+term,'kid39F ~ gF + gM + kid26F',ig,'kidpop',None,{term:1})

jj=read('J1_regions.csv');jj['l26_z']=(jj.l26-jj.l26.mean())/jj.l26.std();jj['urb_z']=(jj.urb-jj.urb.mean())/jj.urb.std()
for term in ['l26_z','urb_z','assr']:estimate('jnea_determinants_'+term,'gain ~ l26_z + urb_z + assr',jj,None,None,{term:1})

# A single family here is an exploratory sensitivity, not a retroactive
# declaration that the entire article was one prespecified test family.
from statsmodels.stats.multitest import multipletests
es=pd.DataFrame(rows)
primary_mechanisms=['mechanism_taught_r_all','mechanism_taught_t_all','russians_gender_gap_20-24_teachers_percap_1911_z','russians_gender_gap_20-24_cwr_z','koren_titular_unit','koren_ts','koren_tsf']
m=es.model.isin(primary_mechanisms)|es.model.str.startswith('two_regime_change_')
es.loc[m,'p_Holm_exploratory_family']=multipletests(es.loc[m,'p_cr1'].to_numpy(),method='holm')[1]
es.to_csv(OUT/'estimates.csv',sep=';',index=False,encoding='utf-8-sig')
(OUT/'errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',len(rows),'models;',len(errors),'not identified/errors',flush=True)

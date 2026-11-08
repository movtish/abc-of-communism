"""Check source integrity, linked inputs and economically meaningful invariants."""
from pathlib import Path
import ast
import hashlib
import json
import re
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent.parent
errors=[]
checks=[]
def check(ok, message):
    checks.append(message)
    if not ok: errors.append(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p, sep=','): return pd.read_csv(ROOT/p, sep=sep, encoding='utf-8-sig')

for directory in ['scripts','methodology','supplementary']:
    for p in (ROOT/directory).rglob('*.py'):
        ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
checks.append('All Python sources parse')
for folder, manifest in [('additional_data_analysis','source_file_manifest.json'),('likbez_1924_analysis','source_manifest.json')]:
    base=ROOT/'supplementary'/folder
    for row in json.loads((base/manifest).read_text(encoding='utf-8-sig')):
        p=base/row['file'].replace('\\','/')
        check(p.is_file() and digest(p)==row['sha256'],f'Source hash: {folder}/{row["file"]}')

a=ROOT/'supplementary/additional_data_analysis'
b=ROOT/'supplementary/likbez_1924_analysis'
check(digest(a/'inputs/census1939_literacy_by_region_age_sex.csv')==digest(ROOT/'data/census1939_literacy_by_region_age_sex.csv'),'1959 follow-up uses current corrected 1939 input')
check(digest(b/'inputs/W2_cells.csv')==digest(ROOT/'results/W2_cells.csv'),'1924 models use current main cohort cells')
q=read('data/census1939_literacy_by_region_age_sex.csv',';')
check(np.allclose(q.population-q.illiterate,q.literate),'1939 literate = population - illiterate')
bad=q[(q.illiterate<0)|(q.literate<0)]
bad.to_csv(ROOT/'validation/1939_unresolved_70plus_cells.csv',sep=';',index=False,encoding='utf-8-sig')
# Preserve source discrepancies rather than manufacturing valid counts.
# These nested-territory 70+ cells are outside every matched cohort and
# are excluded from national aggregates, which omit nested territories.
check(len(bad)==17 and bad.age.eq('70+').all() and bad.region_1939.str.startswith('в том числе').all(),
      '17 unresolved nested-territory 70+ cells isolated outside analytical scope')
scope=q[~q.region_1939.str.startswith('в том числе')]
check(((scope.illiterate>=0)&(scope.literate>=0)).all(),'1939 nonnegative counts in non-nested territories')
for file,col,expected in [('census1959_partition_checks.csv','residual',18423),('census1959_population_checks.csv','difference',13350)]:
    q=pd.read_csv(a/file)
    check(len(q)==expected and q[col].eq(0).all(),f'1959 exact accounting: {file}')
check(len(pd.read_csv(a/'census1959_regions_long.csv'))==20025,'1959 regional long table: 20,025 rows')
q=pd.read_csv(b/'likbez1924_transcription.csv')
check(len(q)==30,'1924 transcription: 30 rows')
v=json.loads((b/'transcription_validation.json').read_text())
check(v['all_pupil_sex_sums_exact'] and v['unallocated_teachers']==3,'1924 pupil identities and preserved teacher discrepancy')
models=pd.concat([pd.read_csv(b/'institution_predictor_models.csv'),pd.read_csv(b/'institution_scale_models.csv')])
check(len(models)==24 and ((models.ci_low_cr2<0)&(models.ci_high_cr2>0)).all(),'24 institutional models: CR2 intervals include zero')
check(len(pd.read_csv(b/'policy1931_age_sensitivity.csv'))==8,'Eight 1931 age-policy specifications')
est=read('methodology/results/estimates.csv',';')
check(len(est)==88,'88 independent specification estimates')
stored=json.loads((ROOT/'results/paper_numbers.json').read_text(encoding='utf-8'))
num=stored['NUM']
check(len(num)==3862 and len(stored['STR'])==1610,'Main calculation contains 3,862 numeric and 1,610 string keys')
female=est.loc[est.model=='main_female','b'].iloc[0]
check(np.isclose(female,num['w2.pw'][0]),'Independent female estimate agrees with main pipeline')
keys=set(num)|set(stored['STR'])
suppkeys=set(re.findall(r'csname supp@([^\\]+)\\endcsname',
    (ROOT/'paper/supplementary_numbers.tex').read_text(encoding='utf-8')))
manuscripts=json.loads((ROOT/'validation/manuscript_files.json').read_text(encoding='utf-8'))
for folder in ['paper','jnea']:
    for p in [ROOT/name for name in manuscripts if name.startswith(folder+'/')]:
        text='\n'.join(line for line in p.read_text(encoding='utf-8-sig').splitlines()
                       if not line.lstrip().startswith('%'))
        for macro, candidates, allowed in [
            ('main',re.findall(r'\\N(?:I|A|IA|E)?\{([^{}]+)\}',text),keys),
            ('supplementary',re.findall(r'\\SN\{([^{}]+)\}',text),suppkeys)]:
            missing=[key for key in candidates if '#' not in key and key not in allowed]
            check(not missing,f'{macro} numerical references: {p.relative_to(ROOT)}')
report={'passed':not errors,'checks':len(checks),'errors':errors,'main_female_pp':female,'article_pdf_rebuilt':False}
(ROOT/'validation/release_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors: raise SystemExit(1)

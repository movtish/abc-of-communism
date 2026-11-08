from pathlib import Path
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent.parent
d=pd.read_csv(OUT/'likbez1924_transcription.csv');d=d[d.area=='rural'].sort_values('survey_coverage')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,axs=plt.subplots(1,2,figsize=(12,7),sharey=True)
pos=np.arange(len(d));colors=np.where(d.survey_coverage<.8,'#b46328','#356a9a')
axs[0].barh(pos,100*d.survey_coverage,color=colors)
axs[0].axvline(80,color='#777',ls='--',lw=1)
axs[0].set_xlim(0,110);axs[0].set_xlabel('Обследовано учреждений, % от учтённых')
axs[1].barh(pos,d.female_pupil_share_pct,color=colors)
axs[1].set_xlim(0,80);axs[1].set_xlabel('Женщины среди учтённых учащихся, %')
for ax,values in [(axs[0],100*d.survey_coverage),(axs[1],d.female_pupil_share_pct)]:
    ax.grid(axis='x',alpha=.15)
    for i,value in enumerate(values):ax.text(value+.9,i,f'{value:.1f}',va='center',fontsize=9)
labels=d.unit_1926.str.replace(' губ.','',regex=False).str.replace(' АССР','',regex=False).str.replace(' АО','',regex=False)
axs[0].set_yticks(pos,labels);axs[0].invert_yaxis()
fig.suptitle('Ликпункты и школы грамотности в сельской местности, 1 января 1924 года',fontsize=12)
fig.text(.5,.02,'Оранжевым отмечены территории с обследованием менее 80% учреждений.\nДоли учащихся относятся к обследованным учреждениям; они не показывают охват всех неграмотных женщин.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.065,1,.95]);fig.savefig(OUT/'survey_coverage_and_female_participation.png',dpi=170)

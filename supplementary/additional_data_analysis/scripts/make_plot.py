from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent.parent
a=pd.read_csv(OUT/'republic_summary_1939_1959.csv')
maps=[(x,) for x in a.region.drop_duplicates()]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,axs=plt.subplots(1,3,figsize=(15,5.7),sharey=True)
order=[x[0] for x in maps]
for ax,area,title in zip(axs,['total','rural','urban'],['Всё население','Сельское население','Городское население']):
    for sex,color,shift,label in [('M','#356a9a',-.14,'Мужчины'),('F','#ad4560',.14,'Женщины')]:
        t=a[(a.area==area)&(a.sex==sex)].set_index('region').loc[order]
        ax.scatter(t.change_standardized_pp,np.arange(len(order))+shift,color=color,s=38,label=label)
    ax.axvline(0,color='#777777',lw=.8);ax.set_title(title)
    ax.set_xlabel('Изменение грамотности, п.п.');ax.grid(axis='x',alpha=.2)
axs[0].set_yticks(np.arange(len(order)),[n.replace(' АССР','') for n in order]);axs[0].invert_yaxis()
axs[2].legend(loc='lower right')
fig.suptitle('Когорты 30–44 лет в 1939 году и 50–64 лет в 1959 году',fontsize=13)
fig.text(.5,.015,'Возрастной состав фиксирован по 1939 г. Сопоставление по ядру территорий; границы требуют проверки.\nИзменения включают обучение после 1939 г., войну, отбор, миграцию и ошибки учёта.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.065,1,.94]);fig.savefig(OUT/'literacy_persistence_regions.png',dpi=180);plt.close(fig)

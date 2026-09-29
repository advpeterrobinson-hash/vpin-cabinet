"""Compare longitudinal clear gaps; reference plan only. CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

R=Path(__file__).resolve().parents[1]
O=R/'exports/generated/side-panel-v32'
r=json.loads((O/'simple-shelves-validation.json').read_text())
assert all(c['pass'] for c in r['checks'])
for name,digest in r['source_hashes'].items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
current=[s['y_mm'] for s in r['config']['shelves']]
fig,axes=plt.subplots(2,1,figsize=(12,7))
for ax,ys,title in zip(axes,([120,600,820],current),('Anterior — 70 mm entre S2 e S3','Revisado — 150 mm entre S2 e S3')):
    ax.add_patch(Rectangle((0,0),1308.1,600,fill=False,ec='#405164',lw=1.5))
    for i,y in enumerate(ys,1):
        ax.add_patch(Rectangle((y,20),150,560,fc='#d8b27e',ec='#866338'))
        ax.text(y+75,300,f'S{i}',ha='center',va='center',fontsize=15,fontweight='bold')
        ax.text(y+75,630,f'Y{y:g}',ha='center',fontsize=10)
    for start,end in zip([y+150 for y in ys[:-1]],ys[1:]):
        ax.annotate('',(end,300),(start,300),arrowprops=dict(arrowstyle='<->',color='#286d81'))
        ax.text((start+end)/2,365,f'{end-start:g} mm',ha='center',color='#286d81',fontsize=13)
    ax.text(-20,300,'FRENTE',rotation=90,ha='right',va='center',fontsize=10)
    ax.text(1320,300,'TRASEIRA',rotation=90,ha='left',va='center',fontsize=10)
    ax.set_title(title,loc='left',fontsize=14,pad=12)
    ax.set_xlim(-80,1390);ax.set_ylim(-15,685);ax.set_aspect(.42);ax.axis('off')
fig.suptitle('Distribuição das prateleiras — vista de cima',fontsize=18)
fig.text(.08,.075,'S2: 35 mm para a frente. S3: 45 mm para trás. Quatro parafusos por cima; retirada independente preservada.',fontsize=10)
fig.text(.08,.043,'Vãos livres entre bordas. Largura comprimida para leitura; demais componentes omitidos. Estudo, não desenho de fabricação.',fontsize=9)
fig.text(.08,.019,'CERN-OHL-S-2.0 · github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8)
fig.tight_layout(rect=(.02,.12,.98,.94), h_pad=4)
fig.savefig(O/'09-shelf-spacing.png',dpi=150)
print('SHELF_SPACING_RENDER_PASS')

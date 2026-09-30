"""Saved-CAD rear hardware illustration. CERN-OHL-S-2.0."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/rear-hardware-v32';mesh=json.loads((O/'mesh.json').read_text());r=json.loads((O/'validation.json').read_text());c=r['config']
fig,(a,b)=plt.subplots(1,2,figsize=(14,7));fig.patch.set_facecolor('#f5f6f8')
a.set_title('TAMPA VISTA POR FORA',loc='left',weight='bold',fontsize=12)
polys=[]
for rec in mesh:
 n=rec['name'];v=np.array(rec['vertices'])
 if n=='REAR':continue
 if n.startswith('CandidateReceiver') or n.startswith('CandidateRearReceiver'):continue
 color='#cfb58b' if n=='REAR_DOOR' else '#536879' if 'Guard' in n else '#c25c3d' if 'RearCoverBolt' in n else '#243744' if n=='CandidateRearHandle' else '#8a9aa5'
 for f in rec['faces']:
  pts=v[list(f)];polys.append((pts[:,1].mean(),pts[:,[0,2]],color))
polys.sort(key=lambda t:t[0]);a.add_collection(PolyCollection([p[1] for p in polys],facecolors=[p[2] for p in polys],edgecolors='none'))
a.set(xlim=(85,515),ylim=(20,415),aspect='equal');a.axis('off')
a.text(300,25,'4 parafusos externos • puxador central\nTampa + fans + grades saem juntos',ha='center',fontsize=11)
b.set_title('FIXAÇÃO — CORTE ESQUEMÁTICO',loc='left',weight='bold',fontsize=12)
# Coordinate along Y relative to exterior rear face; receiver dimensions from config.
for xy,w,h,color in [((-18,-20),18,40,'#cfb58b'),((0,-20),12,40,'#d9c5a3'),((-21,-15),3,30,'#536879'),((-26,-5),5,10,'#536879'),((12,-6),1,12,'#8a9aa5'),((-27,-2.5),40,5,'#c25c3d'),((13,-5),4,10,'#c25c3d')]:b.add_patch(Rectangle(xy,w,h,facecolor=color,edgecolor='none'))
for zz in [-10,10]:
 b.add_patch(Rectangle((-21,zz-1.5),16,3,facecolor='#8a9aa5'))
 b.add_patch(Rectangle((-23,zz-3),2,6,facecolor='#8a9aa5'))
b.annotate('Receptor metálico fixo\nPorca presa à chapa; não gira',xy=(-24,2),xytext=(-42,39),arrowprops={'arrowstyle':'->'},fontsize=10)
b.annotate('Parafuso candidato M5 × 40\nSoltura pelo lado de fora',xy=(17,0),xytext=(2,27),arrowprops={'arrowstyle':'->'},fontsize=10)
b.text(-9,-24,'Painel\n18 mm',ha='center',va='top',fontsize=10);b.text(6,-24,'Tampa\n12 mm',ha='center',va='top',fontsize=10)
b.text(-42,-44,'Receptores instalados uma vez.\nManutenção: apoiar tampa, soltar 4 parafusos,\ndesconectar fans e retirar para trás.',fontsize=10,linespacing=1.5)
b.set(xlim=(-46,49),ylim=(-60,53),aspect='equal');b.axis('off')
fig.suptitle('V32 • Traseira simples, PC mantido na base baixa',x=.04,ha='left',fontsize=18,weight='bold')
fig.text(.04,.025,'ESTUDO DE ENCAIXE • Grades, ferragens, carga e chicote ainda exigem qualificação. Não liberado para CNC. | CERN-OHL-S-2.0',fontsize=9,color='#8e4028')
fig.subplots_adjust(top=.86,bottom=.12,wspace=.2);fig.savefig(O/'01-rear-hardware.png',dpi=160,facecolor=fig.get_facecolor())

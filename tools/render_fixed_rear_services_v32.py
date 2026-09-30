"""Dimensioned layout review, original drawing. CERN-OHL-S-2.0."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyBboxPatch
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/fixed-rear-services-v32';c=json.loads((R/'config/fixed_rear_services_v32.json').read_text());fig,(a,b)=plt.subplots(1,2,figsize=(14,8));fig.patch.set_facecolor('#f5f6f8')
a.set_title('TRASEIRA • fans fixos, porta lisa',loc='left',weight='bold')
a.add_patch(Rectangle((0,0),600,596.9,facecolor='#c8aa7b',edgecolor='#6e583d'))
a.add_patch(Rectangle((102,54),396,329,facecolor='#e4c89e',edgecolor='#806b51'))
for x,z in c['fan_centers_xz_mm']:
 a.add_patch(Rectangle((x-60,z-60),120,120,facecolor='#536e7c'))
 for dz in range(-48,49,6):a.plot([x-48,x+48],[z+dz]*2,color='#e1e8eb',lw=1.5)
a.add_patch(Circle((450,350),11.5,color='#d29a2a'));a.plot([450,450],[346,354],color='#30291c');a.add_patch(Rectangle((262,184),76,12,facecolor='#536e7c'))
for x in (180,372):a.add_patch(Rectangle((x,24),48,60,facecolor='#536e7c'))
for key,label in [('mains','Energia'),('ethernet','Rede')]:
 x,z=c['direct_panel_io'][key]['center_xz_mm']
 if key=='ethernet':
  a.add_patch(Circle((x,z),12,facecolor='#536e7c'))
  for hx,hz in c['direct_panel_io']['ethernet']['footprint']['hole_centers_xz_mm']:a.add_patch(Circle((hx,hz),1.6,color='#27343c'))
 else:
  a.add_patch(FancyBboxPatch((x-14,z-24),28,48,boxstyle='round,pad=0,rounding_size=3',facecolor='#536e7c',edgecolor='none'))
  for hx,hz in c['direct_panel_io']['mains']['footprint']['hole_centers_xz_mm']:a.add_patch(Circle((hx,hz),2.25,color='#27343c'))
 a.text(x,z+36,label,ha='center',fontsize=10,color='#1d2d39')
a.text(300,100,'Chave + puxador\nLimitadores opcionais',ha='center',fontsize=10)
a.text(300,-38,'Rede: Ø24 + 2×Ø3,2. Energia: 28×48 R3 + 2×Ø4,5.\nMontagem direta na madeira; sem placas extras.',ha='center',fontsize=10)
a.set(xlim=(-25,625),ylim=(-85,645),aspect='equal');a.axis('off')
b.set_title('PISO • entrada de ar por baixo',loc='left',weight='bold')
b.add_patch(Rectangle((18,18),564,1272.1,facecolor='#d5bb92',edgecolor='#6e583d'))
sx,sy,diam=c['floor']['subwoofer_opening_xy_diameter_mm'];b.add_patch(Circle((sx,sy),diam/2,facecolor='#5a7180'));b.text(300,440,'Subwoofer\nØ139,7 ref.',ha='center',va='center',fontsize=10,color='white')
for x,y,w,h in c['floor']['intake_xywh_mm']:
 b.add_patch(Rectangle((x-10,y-10),w+20,h+20,fill=False,edgecolor='#4c687a',lw=2));b.add_patch(Rectangle((x,y),w,h,facecolor='#6f8995'));b.text(x+w/2,y+h/2,'100\n×160',ha='center',va='center',fontsize=9,color='white')
b.add_patch(Rectangle((157.5,830),285,460,fill=False,edgecolor='#354e64',ls='--'));b.text(300,1040,'PCBase baixo\ninalterado',ha='center',fontsize=10)
b.text(300,140,'Quatro furos auxiliares\nsem função removidos',ha='center',fontsize=10)
b.text(300,595,'Dois porta-filtros removíveis por baixo',ha='center',fontsize=9)
b.set(xlim=(-15,615),ylim=(1320,-20),aspect='equal');b.axis('off')
fig.suptitle('V32 • Ventilação fixa e interfaces de energia/Ethernet',x=.04,ha='left',weight='bold',fontsize=18)
fig.text(.04,.025,'PROPOSTA • Posições verificadas no CAD; conectores, fixações, elétrica e desempenho térmico ainda a qualificar. CNC não liberada.',fontsize=10,color='#8c4329')
fig.subplots_adjust(top=.87,bottom=.13,wspace=.08);fig.savefig(O/'01-fixed-rear-and-floor.png',dpi=160,facecolor=fig.get_facecolor())

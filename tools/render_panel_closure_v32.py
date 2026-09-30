"""Render saved review solids. CERN-OHL-S-2.0."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/panel-closure-v32';r=json.loads((O/'validation.json').read_text());c=r['config'];g=c['glass_study'];rear=c['rear']
fig,(a,b)=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1,1.15]});fig.patch.set_facecolor('#f4f5f7')
a.set_title('LATERAL / VIDRO — seção normal à inclinação',loc='left',weight='bold',fontsize=12)
a.add_patch(Rectangle((0,-16),18,16,color='#c8a773',label='Lateral 18 mm'))
# Actual saved solid section at its middle; projected to local normal coordinates.
import numpy as np
angle=np.radians(r['glass_angle_deg']);y0=g['front_y_mm'];z0=400.05+y0*np.tan(angle)
mesh=json.loads((O/'mesh.json').read_text())
for rec in mesh:
 if rec['name']!='CandidateGlassChannelL':continue
 v=np.array(rec['vertices']);u=(v[:,1]-y0)*np.cos(angle)+(v[:,2]-z0)*np.sin(angle);n=-(v[:,1]-y0)*np.sin(angle)+(v[:,2]-z0)*np.cos(angle)
 # end-face triangles are coplanar at local longitudinal u=0.
 for f in rec['faces']:
  if np.max(np.abs(u[list(f)]))<1e-4:a.fill(v[list(f),0],n[list(f)],color='#456680')
gx=(600-g['width_mm'])/2;a.add_patch(Rectangle((gx,g['bottom_normal_offset_mm']),26,g['thickness_mm'],facecolor='#70cad4',alpha=.7,edgecolor='#2a7d88'))
a.annotate('Vidro candidato: 575 × 1100 × 5 mm\nParalelo ao playfield; sai pela frente',xy=(31,6.5),xytext=(0,27),arrowprops={'arrowstyle':'->'},fontsize=10)
a.annotate('Canaleta substituível\nSem rasgo longitudinal na lateral',xy=(11,10),xytext=(0,18),arrowprops={'arrowstyle':'->'},fontsize=10)
a.text(1,-9,'18 mm',fontsize=11);a.text(0,-25,'Lockdown: barra sob medida + receptor WPC.\nPedido pela largura do corpo: 600 mm sem siderails.\nLinguetas, trava e furos aguardam desenho do conjunto.',fontsize=10,linespacing=1.6)
a.set(xlim=(-3,48),ylim=(-34,35),aspect='equal');a.axis('off')
b.set_title('TRASEIRA — tampa sobreposta removível',loc='left',weight='bold',fontsize=12)
b.add_patch(Rectangle((0,0),600,596.9,facecolor='#c8a773',edgecolor='#5c4830'))
x,z,w,h=rear['opening_xzwh_mm'];b.add_patch(Rectangle((x,z),w,h,facecolor='#424b57',edgecolor='black'))
x,z,w,h=rear['cover_xzwh_mm'];b.add_patch(Rectangle((x,z),w,h,facecolor='#d5dee7',alpha=.9,edgecolor='#354860'))
for xx,zz in rear['fan_centers_xz_mm']:b.add_patch(Circle((xx,zz),58,facecolor='#647d90',edgecolor='#2d4050'))
for xx,zz in rear['cover_fasteners_xz_mm']:b.plot(xx,zz,'o',color='#c75034',ms=5)
b.text(300,170,'4 parafusos pela traseira\nTampa 396 × 329 × 12 mm\nAbertura existente: 340 × 293',ha='center',va='center',fontsize=10)
b.text(300,510,'Rede e alimentação protegida:\nreservas existentes mantidas;\nsem novos recortes nesta etapa.',ha='center',fontsize=10)
b.text(300,-60,'2 ventoinhas de 120 mm\nConector removível; grades a detalhar',ha='center',fontsize=10)
b.set(xlim=(-25,625),ylim=(-100,620),aspect='equal');b.axis('off')
fig.suptitle('V32 • Interfaces laterais e traseira',x=.04,ha='left',weight='bold',fontsize=18)
fig.text(.04,.02,'ESTUDO — Ferragens importadas podem ser conferidas depois. Não liberado para CNC. | CERN-OHL-S-2.0',fontsize=10,color='#904225')
fig.subplots_adjust(top=.87,bottom=.12,wspace=.15);fig.savefig(O/'01-side-rear-interfaces.png',dpi=160,facecolor=fig.get_facecolor());plt.close(fig)

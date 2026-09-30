"""Orthographic review diagram from saved study parameters. CERN-OHL-S-2.0."""
import json,math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/rear-door-v32';r=json.loads((O/'validation.json').read_text());c=r['config'];fig,(a,b)=plt.subplots(1,2,figsize=(14,7));fig.patch.set_facecolor('#f4f5f7')
a.set_title('FECHADA • vista traseira esquemática',loc='left',weight='bold')
a.add_patch(Rectangle((0,0),600,596.9,facecolor='#c5a879'))
a.add_patch(Rectangle((102,54),396,329,facecolor='#e3c89e',edgecolor='#756046'))
for x in (230,370):
 a.add_patch(Rectangle((x-60,220),120,120,facecolor='#506876'))
 for dz in range(-48,49,6):a.plot([x-48,x+48],[280+dz]*2,color='#dbe3e7',lw=1.4)
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):a.add_patch(Circle((x+dx,280+dz),3,color='#aeb8be'))
for x in [180,372]:a.add_patch(Rectangle((x,24),48,60,facecolor='#596d78'));a.plot([x,x+48],[54,54],color='black',lw=2)
a.add_patch(Rectangle((262,184),76,12,facecolor='#354c58'));lx,lz=c['lock_center_xz_mm'];a.add_patch(Circle((lx,lz),11.5,facecolor='#d4a240'));a.plot([lx,lx],[lz-4,lz+4],color='#352a18',lw=2)
a.annotate('Fechadura de chave',xy=(450,350),xytext=(300,450),ha='center',arrowprops={'arrowstyle':'->'},fontsize=11)
a.set(xlim=(-15,615),ylim=(-45,625),aspect='equal');a.axis('off')
b.set_title('ABERTA • corte lateral no vão do PC',loc='left',weight='bold')
for z,h in [(0,72),(365,231.9)]:b.add_patch(Rectangle((1290.1,z),18,h,facecolor='#c5a879'))
b.add_patch(Rectangle((1180,36),100,18,facecolor='#567789'));b.add_patch(Rectangle((1180,54),100,128,facecolor='#8ca4b6'));b.text(1200,110,'PC\nbaixo',ha='center',va='center',fontsize=11)
axis=np.array(c['hinge_axis_xyz_mm'][1:]);angle=math.radians(-c['opening_degrees']);rot=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
def trans(points):return (np.array(points)-axis)@rot.T+axis
b.add_patch(Polygon(trans([[1308.1,54],[1320.1,54],[1320.1,383],[1308.1,383]]),facecolor='#e3c89e',edgecolor='#756046'))
b.add_patch(Polygon(trans([[1283.1,220],[1308.1,220],[1308.1,340],[1283.1,340]]),facecolor='#506876'))
b.add_patch(Circle(axis,4,color='#354c58'))
b.text(1440,270,'Limitadores opcionais.\nFeltro no contato real do miolo.',ha='center',fontsize=10)
b.annotate('110°\npose testada',xy=(1480,-20),xytext=(1345,-75),arrowprops={'arrowstyle':'->'},fontsize=10,weight='bold')
b.annotate('',xy=(1620,110),xytext=(1320,110),arrowprops={'arrowstyle':'->','color':'#486b85','lw':2});b.text(1470,140,'Rota do PC após elevar 38 mm',ha='center',fontsize=9,color='#486b85')
b.set(xlim=(1160,1660),ylim=(-120,625),aspect='equal');b.axis('off')
fig.suptitle('V32 • Abrir com chave, baixar a porta e fechar',x=.04,ha='left',fontsize=18,weight='bold')
fig.text(.05,.105,'Sem remover quatro parafusos para acessar.\nFerrolho sem chave: alternativa opcional, sem desenho.',fontsize=10)
fig.text(.54,.105,'90° obstrui a saída do PC; 110° passa no estudo.\nPorta aberta não é apoio para o computador.',fontsize=10)
fig.text(.05,.025,'ESTUDO • Recorte de fechadura e ferragens candidatos. Cargas, chicote e fabricação pendentes. | CERN-OHL-S-2.0',fontsize=9,color='#904326')
fig.subplots_adjust(top=.85,bottom=.2,left=.04,right=.96,wspace=.14);fig.savefig(O/'01-keyed-rear-door.png',dpi=160,facecolor=fig.get_facecolor())

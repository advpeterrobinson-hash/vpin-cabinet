"""Simple pictorial detail from saved CAD bounds. CERN-OHL-S-2.0."""
import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Ellipse
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/side-panel-v32'
r=json.loads((O/'simple-shelves-validation.json').read_text());assert all(c['pass'] for c in r['checks'])
for n,h in r['source_hashes'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
assert hashlib.sha256((R/r['saved_proposal']['path']).read_bytes()).hexdigest()==r['saved_proposal']['sha256']
mesh={e['name']:e for e in json.loads((O/'simple-shelves-mesh.json').read_text())}
fig=plt.figure(figsize=(12,7),facecolor='#f7f9fb');ax=fig.add_axes([.05,.21,.90,.54]);ax.set_aspect('equal');ax.axis('off')
def project(x,y,z):return (x+.48*(y-120),.42*(y-120)+1.5*(z-142))
def board(name,lift,color):
 v=mesh[name]['vertices'];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];lo[2]+=lift;hi[2]+=lift
 x0,y0,z0=lo;x1,y1,z1=hi
 for corners,shade in [([(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],color[0]), ([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],color[1]), ([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],color[2])]:
  ax.add_patch(Polygon([project(*p) for p in corners],facecolor=shade,edgecolor='#8e6f4e',lw=.7))
for name in ('SHELF_SUPPORT_1L','SHELF_SUPPORT_1R'):board(name,0,('#9f7041','#b3824e','#c69b6c'))
for a in r['axes']:
 if a['shelf']=='SHELF_1':
  x,y,_=a['xyz_mm'];px,py=project(x,y,160);ax.add_patch(Ellipse((px,py),10,5,facecolor='#728396'))
board('SHELF_1',35,('#c79860','#d4a975','#e6c798'))
for a in r['axes']:
 if a['shelf']!='SHELF_1':continue
 x,y,z=a['xyz_mm'];bottom=project(x,y,160);plate=project(x,y,z+35);tip=project(x,y,z+55);head=project(x,y,z+80)
 ax.plot([bottom[0],head[0]],[bottom[1],head[1]],':',color='#6c96b3',lw=1.2)
 ax.add_patch(Ellipse(plate,7,3,facecolor='#93734f'))
 ax.plot([tip[0],head[0]],[tip[1],head[1]],color='#24638e',lw=3,solid_capstyle='round')
 ax.add_patch(Ellipse(head,13,6,facecolor='#24638e'))
ax.set_xlim(-5,675);ax.set_ylim(-12,255)
fig.text(.06,.92,'Dois parafusos de cada lado. Todos por cima.',fontsize=22,fontweight='bold',color='#20354b')
fig.text(.06,.86,'A prateleira sai com os equipamentos. Os apoios ficam no gabinete.',fontsize=14,color='#486079')
fig.text(.06,.13,'4 parafusos removíveis',fontsize=14,fontweight='bold',color='#24638e')
fig.text(.39,.13,'2 apoios fixos',fontsize=14,fontweight='bold',color='#946334')
fig.text(.66,.13,'Roscas presas nos apoios',fontsize=14,fontweight='bold',color='#566574')
fig.text(.06,.075,'Esquema explodido: na montagem, a prateleira encosta diretamente nos apoios. Equipamentos omitidos.',fontsize=10,color='#566574')
fig.text(.06,.042,'Estudo simplificado V32 · posição real do playfield aberto ainda não validada · CNC bloqueado',fontsize=10,color='#566574')
fig.text(.06,.017,'CERN-OHL-S-2.0 · github.com/advpeterrobinson-hash/vpin-cabinet',fontsize=8,color='#566574')
fig.savefig(O/'07-simple-shelves.png',dpi=160,facecolor=fig.get_facecolor());print('SIMPLE_SHELVES_RENDER_PASS')

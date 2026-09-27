from pathlib import Path
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
OUT=Path(__file__).resolve().parent;g=json.loads((OUT/'geometry.json').read_text());parts=g['parts'];by={p['id']:p for p in parts}
colors={'shell':'#c6a376','floor':'#e3d4b9','shelf':'#268b83','support':'#ac9575','brace':'#d48436','mount':'#56768f','pcbase':'#ac9575','pc':'#414d60','audio':'#bc5471','reserved':'#c74373','door':'#c6a376','fan':'#53616a','guide':'#b68c4f','bracket':'#78858e'}
zorders={'floor':1,'support':2,'pcbase':2,'pc':3,'shelf':4,'audio':5,'guide':5,'brace':6,'bracket':6,'mount':7}
def mesh(ax,p,zorder=None):
 v=np.array(p['vertices']);kwargs={} if zorder is None else {'zorder':zorder}
 ax.add_collection3d(Poly3DCollection([v[f] for f in p['faces']],facecolor=colors[p['kind']],edgecolor='none',**kwargs))
def finish(fig,name):
 fig.text(.06,.035,'V32 · Design review · Not released for CNC or manufacturing',fontsize=10,color='#5b6065')
 fig.savefig(OUT/(name+'.png'),dpi=140,bbox_inches='tight');plt.close(fig)
for name,title,kinds in [('01-interior','Shelves and PC',{'floor','shelf','pc','pcbase','audio'}),('02-travessas','Upright crossmembers',{'floor','shelf','pc','pcbase','guide','bracket','brace','mount','audio'})]:
 fig=plt.figure(figsize=(11,9),facecolor='#f6f4ef');ax=fig.add_subplot(111,projection='3d',computed_zorder=False);ax.set_facecolor('#f6f4ef')
 for p in parts:
  if p['kind'] in kinds:mesh(ax,p,zorders.get(p['kind'],2))
 ax.set(xlim=(0,600),ylim=(0,1308.1),zlim=(0,600),xlabel='X (mm)',ylabel='Y · front → rear',zlabel='Z (mm)')
 ax.set_box_aspect((600,1308.1,600));ax.view_init(elev=30,azim=-55);ax.set_proj_type('ortho');ax.set_title(title,pad=20,fontsize=18)
 if name=='01-interior':
  for i,y,z in [(1,195,172),(2,675,192),(3,1155,252)]:ax.text(300,y,z+15,'S'+str(i),fontsize=15,weight='bold',color='#155f58',zorder=20)
  fig.text(.08,.09,'S1 / S2 / S3: 560 × 150 mm   |   StarTech: 100 × 60 × 25 mm',fontsize=12)
 else:fig.text(.08,.09,'T1 / T2 / T3 · 6 replaceable guides · 6 provisional support angles',fontsize=12)
 finish(fig,name)
# Correctly projected dimensional top plan, not a 3D raster with depth ambiguities.
fig,ax=plt.subplots(figsize=(8,11),facecolor='#f6f4ef');ax.set_facecolor('#f6f4ef')
ax.add_patch(Rectangle((0,0),600,1308.1,facecolor='#e3d4b9',edgecolor='#67533a'))
for i,y in enumerate((120,600,1080),1):
 ax.add_patch(Rectangle((20,y),560,150,facecolor='#268b83'))
 ax.text(300,y+(120 if i==1 else 75),f'S{i} · 560 × 150',ha='center',va='center',color='white',fontsize=13)
ax.add_patch(Rectangle((157.5,830),285,460,fill=False,edgecolor='#414d60',lw=2,ls='--'))
ax.add_patch(Rectangle((200,155),100,60,facecolor='#bc5471'));ax.text(310,185,'StarTech',color='white',fontsize=10)
ax.add_patch(Circle((300,440),69.85,facecolor='#f6f4ef',edgecolor='#67533a'))
ax.text(300,440,'Sub',ha='center',va='center')
ax.add_patch(Rectangle((400,630),100,160,fill=False,edgecolor='#363c42',ls=':'))
for x in (185,245,305,365):ax.add_patch(Circle((x,90),14,facecolor='#f6f4ef',edgecolor='#67533a'))
for y in (270,750):
 ax.annotate('',xy=(70,y+330),xytext=(70,y),arrowprops={'arrowstyle':'<->','color':'#28343e'});ax.text(82,y+165,'330 mm',rotation=90,va='center')
ax.set(xlim=(-20,620),ylim=(-20,1330),xlabel='Width (mm)',ylabel='Front → Rear (mm)',title='Service plan');ax.set_aspect('equal');finish(fig,'03-planta')
# Rear orthographic view includes fan cutouts and clearly reserved, uncut ports.
fig,ax=plt.subplots(figsize=(10,9),facecolor='#f6f4ef');ax.set_facecolor('#f6f4ef')
ax.add_patch(Rectangle((0,0),600,596.9,facecolor='#e3d4b9',edgecolor='#67533a'))
ax.add_patch(Rectangle((130,72),340,293,facecolor='#4a5662'))
ax.add_patch(Rectangle((132,74),336,289,facecolor='#c6a376'))
for x in (230,370):
 ax.add_patch(Rectangle((x-60,220),120,120,fill=False,edgecolor='#268b83',ls='--'))
 ax.add_patch(Circle((x,280),58,facecolor='#f6f4ef',edgecolor='#67533a'))
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):ax.add_patch(Circle((x+dx,280+dz),2.25,color='#333'))
 ax.text(x,280,'120 mm',ha='center',va='center')
ax.text(300,155,'Removable access door',ha='center',va='center',fontsize=13)
for x,z,w,h,label in [(50,395,90,70,'Mains'),(510,405,40,40,'RJ45')]:
 ax.add_patch(Rectangle((x,z),w,h,fill=False,edgecolor='#bc5471',ls='--',lw=2));ax.text(x+w/2,z+h+15,label,ha='center',fontsize=11)
ax.text(300,535,'Reserved zones — no final cutout',ha='center',fontsize=11,color='#97354e')
ax.set(xlim=(-15,615),ylim=(-15,615),xlabel='X (mm)',ylabel='Z (mm)',title='Rear access and exhaust');ax.set_aspect('equal');finish(fig,'04-traseira')
# Dimensioned guide detail: front face and plan section at crossmember height.
fig,(ax,sec)=plt.subplots(1,2,figsize=(11,8),facecolor='#f6f4ef',gridspec_kw={'width_ratios':[1,1.3]})
for a in (ax,sec):a.set_facecolor('#f6f4ef')
ax.add_patch(Rectangle((-30,0),60,145,facecolor='#b68c4f',edgecolor='#67533a'))
ax.add_patch(Rectangle((-9.2,20),18.4,125,facecolor='#dec9a4',edgecolor='#67533a'))
for y in (-22,22):
 for z in (65,120):ax.add_patch(Circle((y,z),2.75,facecolor='#f6f4ef',edgecolor='#67533a'))
for y in (-20,20):
 for z in (13,23,33):ax.add_patch(Circle((y,z),2.75,facecolor='#f6f4ef',edgecolor='#67533a'))
ax.add_patch(Rectangle((-25,42),50,3,facecolor='#78858e'))
ax.annotate('Support seat',xy=(25,43.5),xytext=(36,48),fontsize=10,arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-40,85),ylim=(-5,155),xlabel='Relative Y (mm)',ylabel='Height (mm)',title='Inner face');ax.set_aspect('equal')
# X increases inward; guide 18..36, groove 30..36, crossmember starts 30.2.
sec.add_patch(Rectangle((0,-30),18,60,facecolor='#e3d4b9',edgecolor='#67533a'))
sec.add_patch(Rectangle((18,-30),18,60,facecolor='#b68c4f',edgecolor='#67533a'))
sec.add_patch(Rectangle((30,-9.2),6,18.4,facecolor='#f6f4ef',edgecolor='#67533a'))
sec.add_patch(Rectangle((30.2,-9),50,18,facecolor='#d48436',edgecolor='#67533a'))
sec.text(9,0,'Side',ha='center',va='center',rotation=90,fontsize=11)
sec.text(26,22,'Guide',ha='center',fontsize=10)
sec.text(57,0,'Crossmember',ha='center',va='center',fontsize=10)
sec.set(xlim=(-5,85),ylim=(-45,45),xlabel='X (mm)',ylabel='Relative Y (mm)',title='Plan section');sec.set_aspect('equal')
fig.suptitle('Replaceable crossmember guide',fontsize=18)
fig.text(.07,.12,'Guide: 18 × 60 × 145 mm · Groove: 18.4 × 6 mm\nGeneric support angle · provisional fasteners',fontsize=11)
fig.subplots_adjust(bottom=.2,wspace=.35)
finish(fig,'05-encaixe')
# Front face: source CAD openings, plunger reserve clearly dashed.
fig,ax=plt.subplots(figsize=(11,8),facecolor='#f6f4ef');ax.set_facecolor('#f6f4ef');ax.add_patch(Rectangle((0,0),600,400.05,facecolor='#e3d4b9',edgecolor='#67533a'))
ax.add_patch(Rectangle((144.425,92.840625),311.15,264.31875,facecolor='#f6f4ef',edgecolor='#67533a'))
for z in (280,230):
 ax.add_patch(Circle((90,z),17.4625,facecolor='#c6a376',edgecolor='#67533a'));ax.add_patch(Circle((90,z),12.7,facecolor='#f6f4ef',edgecolor='#67533a'))
for x,z in [(136.4875,225),(463.5125,225),(300,84.903125),(300,365.096875)]:ax.add_patch(Circle((x,z),3.571875,color='#414d60'))
ax.add_patch(Rectangle((502,232),36,36,fill=False,edgecolor='#bc5471',ls='--',lw=2));ax.text(520,195,'Plunger\nreserve',ha='center',fontsize=10)
ax.text(300,225,'Coin door\n311.15 × 264.32 mm',ha='center',va='center',fontsize=13)
ax.set(xlim=(-15,615),ylim=(-15,420),xlabel='X (mm)',ylabel='Z (mm)',title='Front panel');ax.set_aspect('equal');finish(fig,'06-frente')
print('6 images generated')

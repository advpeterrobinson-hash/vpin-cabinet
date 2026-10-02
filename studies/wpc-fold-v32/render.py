"""Render original study drawings from OCC tessellation. CERN-OHL-S-2.0."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/wpc-fold-v32';B=json.loads((O/'mesh.json').read_text());Q=json.loads((O/'validation.json').read_text());P=json.loads((Path(__file__).parent/'parameters.json').read_text())
current=json.loads((R/'exports/generated/backbox-floor-v32/mesh.json').read_text())
B['v32_current']={'wood':current['wood'],'fixed':current['context'],'axis':[300,1270,508]}
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'figure.facecolor':'#f8fafc','axes.facecolor':'#f8fafc','font.family':'DejaVu Sans'})
colors={'Floor':'#d89c37','Side':'#5485a6','Rear':'#8b6f49','Top':'#ae916c','Shelf':'#3f917e','BACKBOX_BASE':'#3f917e','Channel':'#e06b54','Hinge':'#283e54','Bushing':'#9271ae','Bolt':'#9271ae','PF_':'#aaaab4','SIDE_':'#93a4ab'}
def color(n):return next((v for k,v in colors.items() if k in n),'#aeb5b9')
def vertices(m,axis=None,a=0):
 v=np.array(m['vertices']);
 if axis is not None:
  ax=np.array(axis);t=math.radians(a);rot=np.array([[1,0,0],[0,math.cos(t),-math.sin(t)],[0,math.sin(t),math.cos(t)]]);v=(v-ax)@rot.T+ax
 return v
files=[]
def finish(fig,n,title):
 fig.suptitle(title,x=.04,ha='left',fontweight='bold',fontsize=17)
 fig.text(.04,.024,'ISOLATED STUDY • accepted V32 unchanged • metal schematic only • manufacturing BLOCKED',fontsize=9,color='#4c5964')
 fig.subplots_adjust(top=.87,bottom=.12,left=.08,right=.96,wspace=.30)
 path=O/(n+'.png');fig.savefig(path,dpi=160);plt.close(fig);files.append({'file':path.name,'title':title})
def scene3d(ax,key,a):
 b=B[key]
 for role in ['fixed','wood','hardware']:
  for m in b.get(role,[]):
   # Open the left cabinet side to reveal floor/shelf; opposite side remains.
   if role=='fixed' and m['name'] in ['SIDE_L','CabinetSideL']:continue
   v=vertices(m,b['axis'],a) if role!='fixed' else vertices(m)
   pc=Poly3DCollection(v[np.array(m['faces'])],facecolor=color(m['name']),edgecolor='#34404a',linewidth=.12,alpha=.92 if role!='fixed' else .30);ax.add_collection3d(pc)
 ax.set(xlim=(-120,720),ylim=(150,1360),zlim=(390,1360),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
 ax.set_box_aspect((840,1210,970));ax.view_init(elev=22,azim=-53)
 ax.set_title(f'{a:g}° — {"reference control" if key=="reference" else "210 mm sides / inset floor"}',loc='left')
def yz(ax,key,a=0,hardware=False,side=False,limits=None):
 b=B[key]
 for role in ['fixed','wood']+(['hardware'] if hardware else []):
  for m in b.get(role,[]):
   n=m['name']
   if role=='fixed' and not any(k in n for k in ['Shelf','BACKBOX_BASE','Channel','SIDE_L','CabinetSideL']):continue
   if role=='wood' and not ('Floor' in n or (side and ('SideL' in n or 'LeftSide' in n))):continue
   if role=='hardware' and n.endswith('_R'):continue
   v=vertices(m,b['axis'],a) if role!='fixed' else vertices(m)
   alpha=.28 if ('SIDE_' in n or 'CabinetSide' in n) else .65
   ax.add_collection(PolyCollection(v[np.array(m['faces'])][:,:,[1,2]],facecolors=color(n),edgecolors=color(n),linewidth=.35,alpha=alpha))
 ax.plot(b['axis'][1],b['axis'][2],'ko',ms=5);ax.set(xlabel='Y / mm (front ← rear)',ylabel='Z / mm');ax.set_aspect('equal');ax.grid(alpha=.18)
 if limits:ax.set(xlim=limits[0],ylim=limits[1])
 else:ax.set(xlim=(1020,1330),ylim=(475,650))
def plot_bearing(ax,key):
 for m in B[key]['bearing']:
  v=vertices(m);ax.add_collection(PolyCollection(v[np.array(m['faces'])][:,:,[0,1]],facecolors='#3f917e',edgecolors='none'))
 ax.set(xlim=(-100,700),ylim=(1100,1320),xlabel='X / mm',ylabel='Y / mm');ax.set_aspect('equal');ax.grid(alpha=.2)
 ax.set_title('Exact upright floor / shelf bearing (green)')

fig=plt.figure(figsize=(12,8));scene3d(fig.add_subplot(111,projection='3d'),'reference',0);finish(fig,'01-wpc-upright','01  WPC reference — upright bearing and rigid arms')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'reference',hardware=True);axs[0].annotate('single cabinet-side pivot\nY1066.8 / Z508',(1066.8,508),xytext=(1080,476),arrowprops={'arrowstyle':'->'});axs[0].set_title('Longitudinal projection — arm outboard of cabinet')
axs[1].axis('off');axs[1].text(0,.93,'01-9011-L/R\nRigid arm + bent mounting flange\n3 fixed floor bolts: no second pivot\n\n4322-01139-12B\nSquare neck keyed to hinge arm\n\n02-4352\nConcentric bushing in round cabinet bore\n\nOne revolute degree of freedom\nNo slot, lift or sliding link in the documented assembly\n\nMetal silhouette / thickness shown schematically.\nPhysical parts required before releasing holes.',va='top',linespacing=1.6);finish(fig,'02-hinge-pivot','02  Hinge architecture — fixed offset, pure rotation')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'reference',limits=((1120,1320),(570,635)));plot_bearing(axs[1],'reference');finish(fig,'03-reference-interface','03  WPC floor / shelf — 69,304.30 mm² upright bearing')
fig,axs=plt.subplots(2,3,figsize=(13,8));
for ax,a in zip(axs.flat,[0,.25,.5,1,1.5,2]):yz(ax,'reference',a,limits=((1135,1175),(588,625)));ax.set_title(f'{a:g}°')
finish(fig,'04-initial-twist','04  WPC initial twist — actual floor edge, shelf below')
fig,axs=plt.subplots(1,2,figsize=(13,6));rows=Q['reference']['samples'];small=[q for q in rows if q['angle_deg']<=2];axs[0].plot([q['angle_deg'] for q in small],[q['floor_shelf_minimum_separation_mm'] for q in small],'o-',color='#3f917e');axs[0].set(xlabel='Angle / degrees',ylabel='Floor / shelf minimum separation / mm');axs[0].grid(alpha=.2)
axs[1].axis('off');axs[1].text(0,.95,'BEARING RELEASE\n\n0°: 69,304.30 mm² surface contact\nEvery θ > 0: no contact and no penetration\n\nRelease begins at 0°+\nFully clear for every positive angle\nInfimum: 0° (no finite waiting angle)\n\nFinal contact is the whole upright bearing region.\nThere is no persistent rolling contact edge.\n\nThe hinge and operator support the moving backbox.\nGeometric area is not a structural load certification.',va='top',linespacing=1.6);finish(fig,'05-bearing-release','05  Bearing release — immediate separation, no scraping')
for no,a in [(6,15),(7,45),(8,90)]:
 fig=plt.figure(figsize=(12,8));scene3d(fig.add_subplot(111,projection='3d'),'reference',a);finish(fig,f'{no:02}-reference-{a}',f'{no:02}  WPC reference — {a}°')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'v32_current');axs[0].plot(1270,508,'rx',ms=10);axs[0].plot(1220,596.9,'ro');axs[0].set_title('Current floor front Y1123.5; old axis marked red')
axs[1].axis('off');axs[1].text(0,.92,'OLD DATUM\nRear offset 38.1 mm (1½ in)\nAxis Y1270 / Z508\n\nP = (300,1220,596.9)\nActual wood in accepted floor and shelf\ndZ/dθ = −50 mm/rad\nAt 1°: 88,825.89 mm³ floor/shelf overlap\n\nThis projection uses the original accepted floor/shelf.\nThe P comparison uses those same accepted solids.',va='top',linespacing=1.6);finish(fig,'09-current-interpretation','09  Current V32 datum — reproduce the old failure')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'v32',hardware=True);axs[0].set_title('Corrected interpretation in isolated study')
axs[1].axis('off');axs[1].text(0,.95,'DOCUMENTED DATUM\nRear offset 241.3 mm (9½ in)\nAxis Y1066.8 / Z508\n\n203.2 mm ahead of the old interpretation\nP: dZ/dθ = +153.2 mm/rad\n\nThe original accepted floor clears the original shelf\nat 1° when only the analysis axis is corrected.\n\nA larger passage is not needed to fix that failure.\nNo accepted pivot/configuration was edited.',va='top',linespacing=1.6);finish(fig,'10-corrected-interpretation','10  Correct WPC interpretation — axis ahead of bearing')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'v32',side=True,limits=((1070,1330),(575,760)));axs[0].set_title('Outboard side 210 mm; floor front Y1146')
plot_bearing(axs[1],'v32');finish(fig,'11-deep-side-floor','11  Separate side / floor / shelf extents — broad straight floor')
fig,axs=plt.subplots(2,3,figsize=(13,8));
for ax,a in zip(axs.flat,[0,.25,.5,1,1.5,2]):yz(ax,'v32',a,limits=((1110,1170),(580,632)));ax.set_title(f'{a:g}°')
finish(fig,'12-v32-early-twist','12  V32 210 mm sides — clean early release')
fig,axs=plt.subplots(1,2,figsize=(13,6));yz(axs[0],'v32_initial',4,limits=((1100,1160),(575,625)));axs[0].set_title('Rejected Y1123.5 floor at 4° — channel collision')
axs[1].axis('off');axs[1].text(0,.95,'FIRST BOTTLENECK AFTER AXIS CORRECTION\n\nOld floor front Y1123.5\nFirst sampled collision: 4°\nRefined onset: 3.6407833…3.6407843°\nParts: floor / both glass channels\n\nStudied correction: straight floor front Y1146\nSide lower depth stays 210 mm\nShelf front stays Y1127.125\n\nNo first collision in selected 0→90° wood study.\nGlass and matrix removed for fold.',va='top',linespacing=1.6);finish(fig,'13-first-bottleneck','13  Channel bottleneck — isolated floor correction')
for no,a in [(14,45),(15,90)]:
 fig=plt.figure(figsize=(12,8));scene3d(fig.add_subplot(111,projection='3d'),'v32',a);finish(fig,f'{no:02}-v32-{a}',f'{no:02}  V32 study — {a}° / glass and matrix removed')
(O/'review-images.json').write_text(json.dumps({'images':files,'source':'actual OCC tessellation; hardware schematics clearly labeled','upstream_images_included':False},indent=2)+'\n')
print('WPC_IMAGES_PASS',len(files))

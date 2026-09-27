"""Review figures from tessellations/sections of verified saved FreeCAD solids."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'exports/generated/joinery-study-v32'
g=json.loads((OUT/'geometry.json').read_text());sections=json.loads((OUT/'sections.json').read_text());report=json.loads((OUT/'validation.json').read_text())
assert all(c['passed'] for c in report['checks'])
colors={'SIDE_L':'#c6a376','SIDE_R':'#c6a376','FLOOR':'#268b83','FRONT':'#56768f','REAR':'#56768f'}
def finish(fig,name):
    fig.text(.04,.025,'PROPOSAL ONLY • V32 unchanged • Measured hardware zones / cutter relief / load proof unresolved • CNC BLOCKED',fontsize=9)
    fig.savefig(OUT/(name+'.png'),dpi=150,bbox_inches='tight');plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(12,10),facecolor='#f6f4ef')
for row,joint in enumerate(['floor','front']):
    for col,prefix in enumerate(['baseline_','']):
        ax=axes[row,col];ax.set_facecolor('#f6f4ef')
        for p in sections[prefix+joint]:
            v=np.asarray(p['vertices']);f=np.asarray(p['faces'],dtype=int);indices=[0,2] if joint=='floor' else [0,1]
            polygons=v[f][:,:,indices]
            # Ignore edge-on faces; display actual planar cut faces without hidden depth surfaces.
            u=polygons[:,1]-polygons[:,0];w=polygons[:,2]-polygons[:,0]
            area=np.abs(u[:,0]*w[:,1]-u[:,1]*w[:,0])
            polygons=polygons[area>1e-8]
            ax.add_collection(PolyCollection(polygons,facecolor=colors[p['id']],edgecolor='#333',linewidth=.25,hatch='//' if p['id']=='SIDE_L' else '..'))
        ax.set(xlim=(-3,66),ylim=(-3,56),xlabel='X (mm)',ylabel=('Z' if joint=='floor' else 'Y')+' (mm)')
        ax.set_aspect('equal');ax.set_title(('V32 — butt joint' if col==0 else 'PROPOSAL — captured joint')+'\n'+('Floor / SideL at Y600' if joint=='floor' else 'Front / SideL at Z100'))
        ax.text(40,45,'Floor' if joint=='floor' else 'Front',ha='center',fontsize=12,color=colors['FLOOR' if joint=='floor' else 'FRONT'])
        if col==1:
            ax.annotate('12 mm skin',xy=(6,27 if joint=='floor' else 8),xytext=(28,5 if joint=='floor' else 24),arrowprops={'arrowstyle':'->'},fontsize=10)
            ax.annotate('6 mm capture',xy=(15,27 if joint=='floor' else 13),xytext=(28,38),arrowprops={'arrowstyle':'->'},fontsize=10)
fig.suptitle('Shell joint comparison — sections from saved CAD\nNominal 18 mm stock; 0.2 mm total fit allowance is a coupon trial only',fontsize=15)
fig.tight_layout(rect=(0,.06,1,.93));finish(fig,'01-joint-sections')
fig=plt.figure(figsize=(12,10),facecolor='#f6f4ef');ax=fig.add_subplot(111,projection='3d');ax.set_facecolor('#f6f4ef')
offsets={'SIDE_L':[-150,0,0],'SIDE_R':[150,0,0],'FLOOR':[0,0,-100],'FRONT':[0,-150,0],'REAR':[0,150,0]}
points=[]
for p in g['parts']:
    if p['id'] not in offsets:continue
    v=np.asarray(p['vertices'])+offsets[p['id']];f=np.asarray(p['faces'],dtype=int);points.extend(v)
    ax.add_collection3d(Poly3DCollection(v[f],facecolor=colors[p['id']],edgecolor='none',alpha=.72 if p['id'].startswith('SIDE') else .95))
    for edge in p['edges']:
        line=np.asarray(edge)+offsets[p['id']];ax.plot(line[:,0],line[:,1],line[:,2],color='#443b30',linewidth=.5)
    middle=(v.min(0)+v.max(0))/2
    ax.text(*middle,p['code']+'\nR2-PROPOSAL',ha='center',fontsize=10,weight='bold',zorder=1000,bbox=dict(facecolor='white',alpha=.8,edgecolor='none'))
v=np.asarray(points);lo=v.min(0);hi=v.max(0)
ax.set(xlim=(lo[0]-20,hi[0]+20),ylim=(lo[1]-20,hi[1]+20),zlim=(lo[2]-20,hi[2]+40),xlabel='X (mm)',ylabel='Y: front → rear',zlabel='Z (mm)')
ax.set_box_aspect(hi-lo+40);ax.view_init(elev=28,azim=-58);ax.set_proj_type('ortho')
ax.set_title('Proposed shell — exploded review\nFive changed parts; remaining 40 objects hidden and unchanged',fontsize=15,pad=20)
finish(fig,'02-exploded-shell')
fig,axes=plt.subplots(1,2,figsize=(13,7),facecolor='#f6f4ef')
changes=report['changes'];labels=[p['part_code'] for p in changes];x=np.arange(len(changes))
axes[0].bar(x-.18,[p['removed_mm3']/1000 for p in changes],width=.36,label='Removed / cm³',color='#b65542',hatch='//')
axes[0].bar(x+.18,[p['added_mm3']/1000 for p in changes],width=.36,label='Added / cm³',color='#268b83',hatch='..')
axes[0].set_xticks(x,labels);axes[0].set_ylabel('Solid volume change (cm³)');axes[0].legend();axes[0].set_title('Actual saved-solid differences')
axes[1].axis('off');axes[1].text(.02,.95,'UNCHANGED\n600 mm external width\n1308.1 mm side length\n45 single-solid objects\n40 objects retain exact geometry\n\nCHANGED IN STUDY ONLY\nFloor / Front / Rear: 564 → 576 mm\n6 mm capture each side\n12 mm nominal outer skin\nFloor cleats retained\n\nNOT YET PROVEN\nLeg/backbox hardware load zones\nCutter relief and coupon fit\nFasteners, assembly and strength',va='top',fontsize=13,linespacing=1.35)
fig.suptitle('Geometry delta and release limits — no manufacturing approval',fontsize=16)
fig.tight_layout(rect=(0,.07,1,.93));finish(fig,'03-change-summary')
print('JOINERY_RENDERS_PASS 3 English review figures')

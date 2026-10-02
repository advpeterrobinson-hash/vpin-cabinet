"""Real B-rep mesh review; individual atlas cells use independent view scales.
CERN-OHL-S-2.0. No generated art or manufacturing outlines.
"""
from pathlib import Path
import gzip,json,math,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/hardware-v33'
C=json.loads((R/'config/hardware_catalog_v33.json').read_text());items={i['id']:i for i in C['hardware']};views=json.loads((O/'review-views.json').read_text());checks=json.loads((O/'cad-library-validation.json').read_text());status={i['id']:i['model_status'] for i in checks['models']}
with gzip.open(O/'review-mesh.json.gz','rt') as f:meshes=json.load(f)
with gzip.open(O/'installed-mesh.json.gz','rt') as f:installed=json.load(f)
wood={p['object'] for p in json.loads((R/'config/wood_materials_v33.json').read_text())['parts']}
def draw(ax,m,color='#47788e',alpha=1):
    vv=np.array(m['vertices']);ff=np.array(m['faces']);ax.add_collection3d(Poly3DCollection(vv[ff],facecolor=color,alpha=alpha,edgecolor='none',linewidth=.03));return vv
def frame(ax,v):
    lo=v.min(axis=0);hi=v.max(axis=0);span=np.maximum(hi-lo,1);center=(hi+lo)/2;lim=max(span)*.57
    ax.set_xlim(center[0]-lim,center[0]+lim);ax.set_ylim(center[1]-lim,center[1]+lim);ax.set_zlim(center[2]-lim,center[2]+lim);ax.set_box_aspect((1,1,1));ax.view_init(24,-58);ax.set_axis_off()
for view in views:
    ids=view['family_ids'];num=view['number']
    cols=6 if len(ids)>35 else 4;nr=math.ceil(len(ids)/cols)
    fig=plt.figure(figsize=(cols*3.15,nr*3.05+1.5),facecolor='#f7f9fb')
    for ix,id in enumerate(ids):
        ax=fig.add_subplot(nr,cols,ix+1,projection='3d');ax.set_facecolor('#f7f9fb');bad=status[id].startswith('UNRESOLVED');it=items[id]
        vv=draw(ax,meshes[id],'#ad6537' if bad else '#49788e');frame(ax,vv)
        q='TBD' if it['quantity'] is None else str(it['quantity']);title=id+'  × '+q+'\n'+'\n'.join(textwrap.wrap(it['description_en'],31))
        ax.set_title(title,fontsize=9,pad=0,fontweight='bold',color='#263b4a')
        caption='NO FIT MODEL — measurement hold' if bad else 'TOPOLOGY ONLY — unmeasured' if 'SCHEMATIC' in status[id] else 'PROVISIONAL ENVELOPE' if 'ENVELOPE' in status[id] or 'RESERVE' in status[id] else 'NOMINAL • no threads'
        ax.text2D(.5,.02,caption,transform=ax.transAxes,ha='center',fontsize=7,color='#9c522e' if bad else '#536b7b')
    fig.suptitle(num+'  '+view['title'],y=1-.25/(nr*3.05+1.5),x=.035,ha='left',fontsize=16,fontweight='bold',color='#213744')
    fig.text(.035,.008,'ACTUAL CAD • One representative/family • independent cell scales • orange crosses are unresolved markers, NOT hardware • CNC BLOCKED • CERN-OHL-S-2.0',fontsize=8)
    fig.subplots_adjust(top=1-1.3/(nr*3.05+1.5),bottom=.055,wspace=.12,hspace=.32)
    fig.savefig(O/(num+'-review.png'),dpi=150);plt.close(fig)
    if view['installed_cad']:
        selected={n:m for n,m in installed.items() if C['object_to_id'].get(n) in ids};stages={items[id]['assembly_stage'] for id in ids}
        wparts=json.loads((R/'config/wood_materials_v33.json').read_text())['parts'];hosts={p['object'] for p in wparts if p['assembly_stage'] in stages}
        if num=='01':hosts={'SIDE_L','SIDE_R','FRONT','REAR','FLOOR','BB_SideL','BB_SideR','BB_Top','BB_Floor','BACKBOX_BASE'}
        fig=plt.figure(figsize=(13,10),facecolor='#f7f9fb');ax=fig.add_subplot(111,projection='3d');vv=[]
        for n,m in selected.items():vv.append(draw(ax,m,'#1b617c'))
        for n in hosts:
            if n in installed:vv.append(draw(ax,installed[n],'#cbb895',.07))
        frame(ax,np.concatenate(vv));fig.suptitle(num+'  '+view['title']+' — installed positions',fontsize=16,fontweight='bold')
        fig.text(.05,.04,'Exact CURRENT coordinates; wood shown as context. Unmodeled interface items appear in the family atlas, not as invented installed hardware.',fontsize=10)
        fig.savefig(O/(num+'-installed.png'),dpi=150);plt.close(fig)
assert all((O/(v['number']+'-review.png')).exists() for v in views)
print('HARDWARE_V33_REVIEW_IMAGES_PASS',len(views))

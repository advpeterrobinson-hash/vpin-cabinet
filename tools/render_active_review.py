"""Render actual saved-shape tessellations, not hand-drawn CAD approximations."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/review';OUT.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'exports/generated/active-geometry-report.json').read_text())
parts={p['name']:p for p in report['inventory']}
def regular(n):
    return not any(t in n for t in ['Ghost','Keepout','Axis','Envelope','Open','Window']) and not n.startswith('SafetyStay')
base=[n for n in parts if regular(n)]
base+=['GenericPlayfieldDisplayClosedV18']
rear=[n for n in base if n.startswith(('Rear','ClassicLegBracketR','LegSpreaderR'))]
rear+=['RearCPUOpenCaseStowedV24']
def scene(filename,title,names,elev,azim,limits=None):
    fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d');points=[]
    for name in dict.fromkeys(names):
        p=parts[name];v=np.asarray(p['mesh_vertices']);tri=np.asarray(p['mesh_triangles'],dtype=int)
        if not len(tri):continue
        color='#ad8558';alpha=.92
        if any(t in name for t in ['Case','Display']):color='#367980';alpha=.55
        elif 'Door' in name:color='#ea9e44';alpha=.85
        elif any(t in name for t in ['Slide','Bracket','Spreader','Plate','Journal','Strut','Stay']):color='#798591'
        if name in ['CabinetLeftSide','CabinetRightSide']:alpha=.28
        if name=='RearPanelWithCPUHatchV24':alpha=.55
        poly=Poly3DCollection(v[tri],facecolor=color,edgecolor='#30363a',linewidth=.12,alpha=alpha)
        ax.add_collection3d(poly);points.extend(v.tolist())
    v=np.asarray(points);lo=v.min(0);hi=v.max(0)
    if limits:lo,hi=np.asarray(limits[0]),np.asarray(limits[1])
    ax.set_xlim(lo[0]-20,hi[0]+20);ax.set_ylim(lo[1]-20,hi[1]+20);ax.set_zlim(lo[2]-20,hi[2]+20)
    ax.set_box_aspect(hi-lo+40);ax.view_init(elev=elev,azim=azim)
    ax.set_xlabel('X / mm');ax.set_ylabel('Y → REAR / mm');ax.set_zlabel('Z / mm')
    ax.set_title(title+'\nENGINEERING PACKAGING — NOT FOR CNC',fontsize=14)
    fig.text(.04,.035,'Actual FCStd tessellation • Utility openings and hardware patterns BLOCKED • Physical legs not yet modeled',fontsize=9)
    fig.savefig(OUT/(filename+'.png'),dpi=150);plt.close(fig)
scene('01-exterior','Full cabinet / selected source geometry',base,24,-60)
# Orthographic rear elevation avoids collapsed depth-axis ticks.
from matplotlib.collections import PolyCollection
fig,ax=plt.subplots(figsize=(10,9))
for name in ['RearPanelWithCPUHatchV24','RearPowerFasciaV09','RearServiceFasciaV09','RearCPUServiceDoorClosedV24']:
    p=parts[name];v=np.asarray(p['mesh_vertices']);tri=np.asarray(p['mesh_triangles'],dtype=int)
    poly=PolyCollection(v[tri][:,:,[0,2]],facecolor='#e4a14c' if 'Door' in name else '#b89b78',edgecolor='#5e5142',linewidth=.4)
    ax.add_collection(poly)
ax.set_xlim(610,-10);ax.set_ylim(-10,620);ax.set_aspect('equal');ax.set_xlabel('X / mm (rear view)');ax.set_ylabel('Z / mm')
ax.set_title('Main-cabinet rear elevation — CLOSED\n13 mm gap below door • utility windows BLOCKED')
ax.annotate('Rear-view LEFT hinge',xy=(482,250),xytext=(590,430),arrowprops={'arrowstyle':'->'},fontsize=10)
fig.tight_layout();fig.savefig(OUT/'02-rear-elevation.png',dpi=150);plt.close(fig)
scene('03-door-closed','Rear CPU door CLOSED',rear,18,65)
open_rear=[n for n in rear if n!='RearCPUServiceDoorClosedV24']+['RearCPUServiceDoorOpenGhostV24']
scene('04-door-open','Rear CPU door OPEN OUTWARD 105°',open_rear,28,65)
scene('05-pc-stowed','PC STOWED / door open / one board + two slides',open_rear,35,115)
extended=[n for n in open_rear if n not in ['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24']]+['RearCPUShelfServiceGhostV24','RearCPUOpenCaseServiceGhostV24','RearCPUServiceSlideLeftGhostV24','RearCPUServiceSlideRightGhostV24']
scene('06-pc-extended','PC EXTENDED 450 mm REARWARD',extended,30,65)
inside=[n for n in base if n not in ['CapturedBottomV20','CapturedFrontPanelV20','RearCPUServiceDoorClosedV24','BackboxServiceDoorV14','GenericPlayfieldDisplayClosedV18','PlayfieldGlassTargetV20']]
scene('07-interior','Underside / service structure (bottom hidden)',inside,-28,55)
# A text inventory is more legible than simulating a GUI screenshot.
lines=['ACTIVE FREECAD OBJECT TREE — generated solid objects','No historical model or presentation hiding dependency','']
for p in report['inventory']:lines.append(p['name']+('  ['+p['part_id']+']' if p['part_id'] else ''))
(OUT/'08-active-tree.txt').write_text('\n'.join(lines)+'\n')
html=['<!doctype html><meta charset="utf-8"><title>Active CAD review</title><style>body{font:16px sans-serif;background:#f3f1ec;margin:2rem}img{max-width:100%}section{background:white;padding:1rem;margin:1rem 0}pre{white-space:pre-wrap}</style><h1>Active engineering CAD review</h1><p>Not manufacturing approved. Review rear proportions, outward door direction, stowed and extended PC access. Utility opening layout remains pending. Images use saved FreeCAD shapes.</p>']
for p in sorted(OUT.glob('*.png')):html.append('<section><img src="'+p.name+'"></section>')
html.append('<section><pre>'+('\n'.join(lines))+'</pre></section>')
(OUT/'index.html').write_text('\n'.join(html))
print('Review:',OUT/'index.html')

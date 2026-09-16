"""Saved CAD tessellations with explicit candidate/active separation and patterned roles."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle,Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports/generated/review';OUT.mkdir(parents=True,exist_ok=True)
report=json.loads((ROOT/'exports/generated/active-geometry-report.json').read_text())
study=json.loads((ROOT/'exports/generated/rear-utility-study.json').read_text())
parts={p['name']:p for p in report['inventory']}
STYLES={'STRUCTURAL_WOOD':('#c7a171','//','1 WOOD / captured shell and load parts'),
        'LOCAL_METAL':('#6a7889','..','2 METAL / slides, brackets, backing'),
        'REMOVABLE_ADAPTER':('#a780aa','xx','3 ADAPTER / replaceable utility carrier'),
        'ELECTRONICS_ZONE':('#74aaa8','--','4 ZONE / electronics or future envelope'),
        'PROTECTED_LOAD_PATH':('#e1bd72','++','Protected joint / leg load path')}

def role(n):
    if n=='RearCPUServiceDoorOpenGhostV24' or n=='RearCPUShelfServiceGhostV24':return 'STRUCTURAL_WOOD'
    return parts[n].get('role','LOCAL_METAL')
def regular(n):
    return not n.startswith(('Utility','RearLegKeepout','BottomJointKeepout')) and not any(t in n for t in ['Ghost','Keepout','Axis','Envelope','Open','Window']) and not n.startswith('SafetyStay')
base=[n for n in parts if regular(n)]+['GenericPlayfieldDisplayClosedV18','RearCPUOpenCaseStowedV24']
rear=[n for n in base if n.startswith(('Rear','ClassicLegBracketR','LegSpreaderR','CPURail'))]
opened=[n for n in rear if n!='RearCPUServiceDoorClosedV24']+['RearCPUServiceDoorOpenGhostV24']
extended=[n for n in opened if n not in ['RearCPUShelfStowedV24','RearCPUOpenCaseStowedV24']]+['RearCPUShelfServiceGhostV24','RearCPUOpenCaseServiceGhostV24','RearCPUServiceSlideLeftGhostV24','RearCPUServiceSlideRightGhostV24']

def draw3d(ax,names,elev,azim,pattern=False,limits=None):
    points=[]
    for n in dict.fromkeys(names):
        p=parts[n];v=np.asarray(p['mesh_vertices']);tri=np.asarray(p['mesh_triangles'],dtype=int)
        if not len(tri):continue
        color,hatch,_=STYLES.get(role(n),('#b5b5b5','','Reference'))
        alpha=.9
        if n in ['CabinetLeftSide','CabinetRightSide','RearPanelWithCPUHatchV24'] or role(n) in ['ELECTRONICS_ZONE','PROTECTED_LOAD_PATH','ACCESS_ZONE']:alpha=.23
        if n.startswith('RearCPUServiceDoor'):color='#efaa42'
        collection=Poly3DCollection(v[tri],facecolor=color,edgecolor='#38404a',linewidth=.18,alpha=alpha,hatch=hatch if pattern else None)
        ax.add_collection3d(collection);points.extend(v.tolist())
    v=np.asarray(points);lo=v.min(0);hi=v.max(0)
    if limits:lo,hi=np.asarray(limits[0]),np.asarray(limits[1])
    ax.set_xlim(lo[0]-20,hi[0]+20);ax.set_ylim(lo[1]-20,hi[1]+20);ax.set_zlim(lo[2]-20,hi[2]+20)
    ax.set_box_aspect(hi-lo+40);ax.view_init(elev=elev,azim=azim)
    ax.set_xlabel('X / mm');ax.set_ylabel('Y → REAR / mm');ax.set_zlabel('Z / mm')

def scene(filename,title,names,elev=25,azim=65,pattern=False):
    fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d');draw3d(ax,names,elev,azim,pattern)
    ax.set_title(title+'\nENGINEERING ONLY — utility placement NOT SELECTED',fontsize=14)
    fig.text(.04,.025,'Saved FCStd shapes • No unmeasured drill patterns • Rail/fastener capacity and physical proof test remain open',fontsize=9)
    fig.savefig(OUT/(filename+'.png'),dpi=150);plt.close(fig)

scene('01-exterior','Full cabinet / active geometry / no utility placement committed',base,24,-60)
scene('03-door-closed','Rear CPU door CLOSED at Z98..362',rear,18,65)
scene('04-door-open','Rear-view LEFT hinge / door OPEN OUTWARD 105°',opened,28,65)
scene('05-pc-stowed','PC STOWED / narrow bottom-seated slide supports',opened,35,115)
scene('06-pc-extended','PC EXTENDED 450 mm / playfield stays closed',extended,30,65)
structural=[n for n in parts if role(n)=='STRUCTURAL_WOOD' and n not in ['CabinetRightSide','CapturedBottomV20']]
structural += [n for n in parts if n.startswith(('ClassicLegBracket','CPURailAngle','CPURailBacking','ClosedSupportSeat','SafetyStayNutPlate','GasStrutNutPlate','PivotPlate','BearingBacking'))]
scene('07-interior','ACTIVE structural parts only / right side and bottom hidden',structural,30,-55)
scene('09-rear-load-path','PC → board → slides → seated rails → clamp/backing → bottom → shell',opened+['CapturedBottomV20','LowCrossmember3V20','RearLegKeepoutRLV26','RearLegKeepoutRRV26','BottomJointKeepoutV26'],28,65,True)
scene('11-utility-A','OPTION A / two fixed rear carriers ABOVE CPU door',rear+[n for n in parts if n.startswith('UtilityA') and parts[n]['role'] in ['REMOVABLE_ADAPTER','ELECTRONICS_ZONE']],25,65)
scene('12-utility-B','OPTION B / underside carriers / mains enclosed inside',rear+['CapturedBottomV20']+[n for n in parts if n.startswith('UtilityB') and parts[n]['role'] in ['REMOVABLE_ADAPTER','ELECTRONICS_ZONE','ACCESS_ZONE']],-28,65)
scene('13-underside','Underside / four identical angle clamps with through-bolt backing',rear+['CapturedBottomV20','LowCrossmember3V20'], -38,60)

def projection(ax,names,axes=(0,2),patterns=False):
    for n in names:
        p=parts[n];v=np.asarray(p['mesh_vertices']);tri=np.asarray(p['mesh_triangles'],dtype=int)
        color,hatch,_=STYLES.get(role(n),('#c8c8c8','','reference'))
        if n.startswith('RearCPUServiceDoor'):color='#efaa42'
        poly=PolyCollection(v[tri][:,:,list(axes)],facecolor=color,edgecolor='#494949',linewidth=.35,alpha=.6 if role(n)=='PROTECTED_LOAD_PATH' else .9,hatch=hatch if patterns else None)
        ax.add_collection(poly)

fig,axs=plt.subplots(1,2,figsize=(15,7))
projection(axs[0],['RearLegKeepoutRLV26','RearLegKeepoutRRV26','CapturedBottomV20','RearCPUSupportRailLeftV24','RearCPUSupportRailRightV24','RearCPUShelfStowedV24']+[n for n in parts if n.startswith(('CPURailAngle','CPURailBacking'))],patterns=True)
axs[0].set_xlim(610,-10);axs[0].set_ylim(-5,210);axs[0].set_title('Rear section / leg brackets + planning reserves');axs[0].set_xlabel('X / mm (rear view)');axs[0].set_ylabel('Z / mm')
projection(axs[1],['CapturedBottomV20','LowCrossmember3V20','RearCPUSupportRailLeftV24','RearCPUFixedSlideLeftV24']+[n for n in parts if n.startswith(('CPURailAngleLeft','CPURailBackingLeft'))],axes=(1,2),patterns=True)
axs[1].set_xlim(800,1310);axs[1].set_ylim(-5,210);axs[1].set_title('Left rail side section / CNC saddle over crossmember');axs[1].set_xlabel('Y / mm toward rear');axs[1].set_ylabel('Z / mm')
axs[1].annotate('Slide face',xy=(980,145),xytext=(960,190),arrowprops={'arrowstyle':'->'},ha='center')
axs[1].annotate('Front uplift clamp',xy=(875,70),xytext=(850,195),arrowprops={'arrowstyle':'->'},ha='center')
axs[1].annotate('Backed bottom',xy=(1150,18),xytext=(1210,65),arrowprops={'arrowstyle':'->'},ha='center')
for ax in axs:ax.set_aspect('equal');ax.grid(alpha=.15)
fig.suptitle('PC load path: board → slides → two seated rails → clamp/backing → captured bottom → shell/legs',fontsize=14)
fig.text(.5,.08,'Four identical angle clamps + four underside backing plates. No final hole patterns.\n20 kg centered payload estimate: 138 N front uplift / 244 N rear downforce per rail; capacity and proof testing still required.\nRail-to-modeled-bracket gap: 13.8 mm (1.2 mm short of the extra 15 mm planning margin); measure actual brackets.',ha='center',fontsize=11)
fig.tight_layout(rect=(0,.16,1,.93));fig.savefig(OUT/'09-rear-load-path.png',dpi=150);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,12))
projection(ax,['RearPanelWithCPUHatchV24']+[n for n in parts if n.startswith('BackboxRearFrame')]+['BackboxServiceDoorV14','RearCPUServiceDoorClosedV24'])
ax.set_xlim(720,-120);ax.set_ylim(-20,1350);ax.set_aspect('equal');ax.set_xlabel('X / mm (rear view)');ax.set_ylabel('Z / mm')
ax.set_title('Rear elevation / ALL DOORS CLOSED\nOld low utility fascias removed; final placement pending')
fig.tight_layout();fig.savefig(OUT/'02-rear-elevation.png',dpi=150);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(15,8))
projection(axs[0],['RearPanelWithCPUHatchV24','RearCPUServiceDoorClosedV24','RearLegKeepoutRLV26','RearLegKeepoutRRV26','BottomJointKeepoutV26','UtilityAMainsCarrierV26','UtilityAEthernetCarrierV26'],patterns=True)
r=study['clear_rectangles']['rear_XZ'][0]['bounds'];axs[0].add_patch(Rectangle((r[0],r[2]),r[1]-r[0],r[3]-r[2],fill=False,linestyle='--',linewidth=2))
axs[0].text(300,535,'Clear band 524 × 176.9 mm',ha='center',fontsize=10)
axs[0].text(95,480,'MAINS\n90 × 70 carrier',ha='center',fontsize=10)
axs[0].text(530,465,'NETWORK\n40 × 40',ha='center',fontsize=10)
axs[0].set_xlim(610,-10);axs[0].set_ylim(-10,610);axs[0].set_xlabel('X / mm (rear view)');axs[0].set_ylabel('Z / mm')
axs[0].set_title('A — Rear face\nEasy-to-see connections; visible carriers')
projection(axs[1],['CapturedBottomV20','RearLegKeepoutRLV26','RearLegKeepoutRRV26']+[n for n in parts if n.startswith('CPURailBacking')]+['UtilityBMainsCarrierV26','UtilityBEthernetCarrierV26'],axes=(0,1),patterns=True)
r=study['clear_rectangles']['underside_XY'][0]['bounds'];axs[1].add_patch(Rectangle((r[0],r[2]),r[1]-r[0],r[3]-r[2],fill=False,linestyle='--',linewidth=2))
axs[1].text(300,1100,'Clear rectangle\n290.4 × 192.1 mm',ha='center',fontsize=11)
axs[1].text(215,1160,'MAINS',ha='center',va='bottom');axs[1].text(400,1178,'NETWORK',ha='center',va='bottom')
axs[1].set_xlim(0,600);axs[1].set_ylim(1010,1320);axs[1].set_xlabel('X / mm');axs[1].set_ylabel('Y / mm toward rear')
axs[1].set_title('B — Underside near rear\nClean rear face; reach underneath to connect')
for ax in axs:ax.set_aspect('equal');ax.grid(alpha=.18)
fig.suptitle('OWNER REVIEW: both layouts fit; CPU door and shelf unchanged',fontsize=16)
fig.text(.5,.07,'Both: two small metal carriers • candidate openings 70 × 50 + 24 × 24 mm • 4,076 mm² wood area\nA: rear-panel cuts. B: bottom-panel cuts. Active panels: neither option cut. Final hardware dimensions required.',ha='center',fontsize=11)
fig.tight_layout(rect=(0,.14,1,.95));fig.savefig(OUT/'10-utility-comparison.png',dpi=150);plt.close(fig)

fig=plt.figure(figsize=(14,11))
category_names=['STRUCTURAL_WOOD','LOCAL_METAL','REMOVABLE_ADAPTER','ELECTRONICS_ZONE']
rear_region=set(rear+['LowCrossmember3V20']+[n for n in parts if n.startswith('UtilityA') and role(n) in category_names])
for i,category in enumerate(category_names,1):
    ax=fig.add_subplot(2,2,i,projection='3d')
    names=[n for n in rear_region if role(n)==category]
    draw3d(ax,names,25,65,True,([0,800,0],[600,1350,600]))
    ax.set_title(STYLES[category][2],fontsize=12)
fig.suptitle('Rear construction by role — numbered titles + distinct hatch patterns\nOption A carrier locations shown for comparison only',fontsize=15)
fig.tight_layout(rect=(0,0,1,.94));fig.savefig(OUT/'14-material-roles.png',dpi=150);plt.close(fig)
lines=['ACTIVE FREECAD SOLID INVENTORY — utility candidates explicitly marked REVIEW ONLY','']
for p in report['inventory']:lines.append(p['name']+' | '+p.get('role','')+(' | '+p['part_id'] if p['part_id'] else ''))
(OUT/'08-active-tree.txt').write_text('\n'.join(lines)+'\n')
images=['10-utility-comparison','02-rear-elevation','04-door-open','05-pc-stowed','06-pc-extended','09-rear-load-path','11-utility-A','12-utility-B','13-underside','07-interior','14-material-roles','01-exterior','03-door-closed']
html=['<!doctype html><meta charset="utf-8"><title>Rear utility engineering review</title><style>body{font:16px sans-serif;background:#f3f1ec;margin:2rem;max-width:1200px}img{width:100%}section{background:white;padding:1rem;margin:1rem 0}pre{white-space:pre-wrap}table{border-collapse:collapse}td,th{padding:.6rem;border:1px solid #999}</style><h1>Rear utility comparison — owner placement review</h1><p>Only AC mains/master disconnect and optional Ethernet remain. Troubleshooting HDMI/USB are accessed on the slide-out PC. Neither utility location is committed or cut. CPU opening Z110..350; shelf Z135; door opens outward.</p><table><tr><th></th><th>A — Rear face</th><th>B — Underside</th></tr><tr><td>Wood removal candidate</td><td>4,076 mm² rear panel</td><td>4,076 mm² bottom panel</td></tr><tr><td>Carriers / generic cuts</td><td>2 / 2</td><td>2 / 2</td></tr><tr><td>Mains / signal separation</td><td>370 mm exterior; 350 mm internal</td><td>120 mm exterior; 105 mm internal</td></tr><tr><td>Access</td><td>Visible from rear</td><td>Reach underneath; confirm actual floor/plug clearance</td></tr><tr><td>Appearance</td><td>Two small visible carriers</td><td>Rear face stays clear</td></tr></table><p>Engineering preference: A for easier connection and inspection. Both fit the modeled structure. Owner chooses the visible rear versus underside interface before final placement. 36 wooden CAD part records, down from 40; laminated release parts still require splitting. Rail geometry has a connected load path, but fastener capacities and physical proof tests remain open.</p>']
for name in images:html.append(f'<section id="{name}"><h2>{name}</h2><img src="{name}.png" alt="{name}"></section>')
html.append('<section><pre>'+('\n'.join(lines))+'</pre></section>')
(OUT/'index.html').write_text('\n'.join(html))
print('Review:',OUT/'index.html')

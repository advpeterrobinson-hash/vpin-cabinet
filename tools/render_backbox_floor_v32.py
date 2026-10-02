# SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION
# Historical baseline/replay only. See studies/wpc-fold-v32/README.md; use original source HEAD for exact replay.
"""Real CAD floor correction views; success poses gated by sweep. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-floor-v32'
b=json.loads((O/'mesh.json').read_text());r=json.loads((O/'validation.json').read_text());f=r['floor']
parts={p['name']:p for group in ('wood','old_floor','context','preserved_zones','bearing','old_intersections') for p in b[group]}
colors={'wood':'#b9945f','floor':'#e69f00','cabinet':'#c6ccd1','channel':'#0072b2','glass':'#56b4e9','problem':'#d55e00','lock':'#cc79a7'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':9,'figure.facecolor':'white'})
images=[]
def save(fig,name,title,subtitle):
    fig.suptitle(title,x=.055,y=.97,ha='left',fontsize=18,weight='bold',color='#213440')
    fig.text(.055,.92,subtitle,fontsize=10,color='#4a5359')
    fig.text(.055,.03,'REAL CAD / FLOOR-ONLY INTEGRATION • zero valid / fold blocked • MANUFACTURING BLOCKED',fontsize=9)
    fig.subplots_adjust(left=.075,right=.96,top=.86,bottom=.13,wspace=.23)
    p=O/name;fig.savefig(p,dpi=160);plt.close(fig)
    images.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mesh_sha256':hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()})
    print('BACKBOX_FLOOR_IMAGE_PASS',name)
def section(ax,x,names,color,alpha=1):
    for n in names:
        for loop in b['sections'][str(x)].get(n,[]):
            ax.add_patch(plt.Polygon(loop,facecolor=color,edgecolor='#39444d',lw=.6,alpha=alpha))
def side(ax,xlim,ylim):
    ax.set(xlim=xlim,ylim=ylim,xlabel='Y / mm (front → rear)',ylabel='Z / mm');ax.set_aspect('equal',adjustable='box');ax.grid(alpha=.16)
def plan(ax,p,color,alpha=1,outline=True):
    vv=np.array(p['vertices']);polys=[vv[t][:,[0,1]] for t in p['faces']]
    ax.add_collection(PolyCollection(polys,facecolors=color,edgecolors='none',alpha=alpha))
    if outline:
        for loop in b['plan_loops'].get(p['name'],[]):
            pp=np.array(loop);ax.plot(pp[:,0],pp[:,1],color='#39444d',lw=.8)
def top(ax):
    ax.set(xlim=(-105,705),ylim=(1035,1320),xlabel='X / mm',ylabel='Y / mm (front → rear)');ax.set_aspect('equal');ax.grid(alpha=.12)
def poly3(ax,ps,alpha=1):
    faces=[];cc=[]
    for p in ps:
        vv=np.array(p['vertices']);faces.extend(vv[t] for t in p['faces'])
        color=colors['floor'] if p['name']=='BackboxFloorV32' else colors['wood']
        cc.extend([color]*len(p['faces']))
    ax.add_collection3d(Poly3DCollection(faces,facecolors=cc,edgecolors='none',alpha=alpha))
def context3(ax):
    for p in b['context_cutaway']:
        if p['name'] in ('SIDE_R','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR'):
            vv=np.array(p['vertices']);ax.add_collection3d(Poly3DCollection([vv[t] for t in p['faces']],facecolors=colors['channel'] if 'Channel' in p['name'] else colors['cabinet'],edgecolors='none',alpha=.8))
def iso(ax):
    ax.set(xlim=(-120,720),ylim=(950,1360),zlim=(440,1340));ax.set_box_aspect((840,410,900));ax.view_init(elev=23,azim=-58)
    ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_zlabel('Z / mm');ax.tick_params(labelsize=8)

# 01: old positive intersection, exact section.
fig,axs=plt.subplots(1,2,figsize=(13,8));ax=axs[0]
section(ax,13,['OldBackboxFloorV14'],colors['wood'],.65)
section(ax,13,['SIDE_L','BACKBOX_BASE'],colors['cabinet'])
section(ax,13,['CandidateGlassChannelL'],colors['channel'])
section(ax,13,['CandidateGlassChannelL_OldIntersection'],colors['problem'])
side(ax,(1045,1135),(584,624));ax.set_title('Old floor / left channel • section X=13 mm')
ax=axs[1];ax.axis('off');ax.text(0,.95,'OLD 0°: COLLISION',color=colors['problem'],fontsize=15,weight='bold')
ax.text(0,.81,'BackboxFloorV14 × glass channels\n937.450518 mm³ per side\n\nX0…18 / X582…600\nY1063.187781…1118.338155\nZ596.9…606.246801\n\nInstalled glass also intersects the old floor.\nCorner-only chamfers preserve that conflict.\n\nAccepted channels and backbox datums\nare held fixed.',va='top',linespacing=1.65)
save(fig,'01-old-upright-collision.png','V32 / OLD FLOOR INTERFERENCE','The accepted previous diagnosis is reproduced without moving any cabinet component.')

# 02: actual new floor geometry with actual inherited passport outlines.
fig,ax=plt.subplots(figsize=(13,7));plan(ax,parts['BackboxFloorV32'],colors['floor']);top(ax)
ax.annotate('',xy=(-78,1110),xytext=(678,1110),arrowprops={'arrowstyle':'<->'});ax.text(300,1098,'756 mm actual joint-resolved panel width',ha='center')
ax.annotate('',xy=(694,1123.5),xytext=(694,1302.1),arrowprops={'arrowstyle':'<->'});ax.text(696,1213,'178.6 mm',rotation=90,va='center')
ax.text(300,1142,'STRAIGHT FRONT EDGE / Y1123.5',ha='center',weight='bold')
ax.text(300,1260,'ONE 18 mm CNC PLYWOOD SOLID\nExisting 2 × 100 × 40 / R20 passports',ha='center',linespacing=1.6)
save(fig,'02-corrected-floor-alone.png','V32 / CORRECTED FLOOR PROFILE','No new concave corner, notch, tongue or dogbone. Measured stock/tool/fit remains pending.')

# 03: old/new overlay from actual meshes; removed strip never pretends to be a channel boolean.
fig,ax=plt.subplots(figsize=(13,7));plan(ax,parts['OldBackboxFloorV14'],'#d9dfe3');plan(ax,parts['BackboxFloorV32'],colors['floor']);top(ax)
ax.plot([-78,678],[1054.1,1054.1],ls='--',color=colors['channel'],lw=1.6)
ax.text(300,1080,'REMOVED: FULL-WIDTH 69.4 mm FRONT STRIP',ha='center',color='#39444d',weight='bold')
ax.text(300,1260,'Material removed: 944,395.2 mm³\nOld and new rear/side joint contours coincide',ha='center',linespacing=1.6)
ax.legend(handles=[Patch(color='#d9dfe3',label='Old floor / removed material'),Patch(color=colors['floor'],label='Corrected floor')],loc='upper left')
save(fig,'03-old-new-floor-overlay.png','V32 / OLD → NEW FLOOR','Least-removal straight-front solution on the declared 0.1 mm design grid; all rear openings retained.')

# 04: corrected source wood upright and measured local interface.
fig=plt.figure(figsize=(13,9));ax=fig.add_subplot(121,projection='3d');context3(ax);poly3(ax,b['wood']);iso(ax);ax.set_title('Reconstructed wood / current cabinet')
ax=fig.add_subplot(122);ax.axis('off');ax.text(0,.95,'UPRIGHT 0°: VALID',fontsize=15,weight='bold')
ax.text(0,.81,'Unintended positive intersection: 0 mm³\nInternal wood joints: no overlap\nGlass channels: 5.084878 mm minimum\nInstalled glass: 5.589938 mm clearance\n\nFloor ↔ shelf is intentional bearing.\nActual contact area: 84,604.626 mm²\nRetained: 100% / continuous width564 mm\n\nWPC pivot: (300,1270,508) mm\nReference inset: 59.8375 mm\n\nUpright validity does not approve folding.',va='top',linespacing=1.6)
save(fig,'04-corrected-upright.png','V32 / CORRECTED UPRIGHT ASSEMBLY','Floor changed; all seven other source wood members and all accepted V32 components unchanged.')

# 05: exact closest-point section and witness dimension.
fig,axs=plt.subplots(1,2,figsize=(13,8));ax=axs[0];x=13
section(ax,x,['BackboxFloorV32'],colors['floor'])
section(ax,x,['SIDE_L','BACKBOX_BASE'],colors['cabinet'])
section(ax,x,['CandidateGlassChannelL'],colors['channel'])
section(ax,x,['CandidateGlass'],colors['glass'],.7)
side(ax,(1100,1150),(588,623));w=f['minimum_channel_clearance_witness_xyz_mm']
ax.annotate('',xy=(w[0][1],w[0][2]),xytext=(w[1][1],w[1][2]),arrowprops={'arrowstyle':'<->','color':'#111111','lw':1.4})
ax.annotate('5.084878 mm\nactual closest-point distance',xy=((w[0][1]+w[1][1])/2,(w[0][2]+w[1][2])/2),xytext=(1101,617),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.set_title(f'Closest-point CAD section X={x:.3f} mm')
ax=axs[1];ax.axis('off');ax.text(0,.95,'5 mm PREFERRED TARGET: PASS',fontsize=14,weight='bold')
ax.text(0,.81,'New front datum: Y1123.5 mm\nMinimum channels: 5.084878 mm\nInstalled pane: 5.589938 mm\n\nCalculated 5 mm straight-edge threshold:\nY1123.413837 mm\n\nPrevious 0.1 mm grid position fails 5 mm.\nThe edge is rounded up to Y1123.5.\n\nNo channel-shaped subtraction.\nNo zero/tangent fit at this interface.',va='top',linespacing=1.65)
save(fig,'05-glass-channel-clearance.png','V32 / FLOOR ↔ GLASS CHANNEL CLEARANCE','Absolute 3 mm minimum and preferred 5 mm separation both satisfied.')

# 06: contact face is a real face-face common, not a bounding rectangle.
fig,axs=plt.subplots(1,2,figsize=(13,8));ax=axs[0]
plan(ax,parts['BackboxFloorV32'],'#e5d7bd');plan(ax,parts['NewBearingContact'],colors['channel'],.75,False);top(ax)
ax.text(300,1254,'ACTUAL BEARING FACE',ha='center',color='white',weight='bold')
ax=axs[1];ax.axis('off');ax.text(0,.95,'REAR-SHELF LOAD PATH RETAINED',fontsize=14,weight='bold')
ax.text(0,.81,'Backbox structure → floor → rear shelf\nHinges provide folding motion.\n\nOld contact: 84,604.625877 mm²\nNew contact: 84,604.625877 mm²\nRetained: 100.000%\nContinuous bearing width: 564 mm\n\nNew side-joint depth: 178.6 mm\nOld depth: 248 mm / retained72.016%\nMinimum planar ligament: 44.5 mm\n\nContact area alone is not strength proof.',va='top',linespacing=1.65)
save(fig,'06-rear-shelf-bearing.png','V32 / ACTUAL FLOOR BEARING','Blue is the exact surface intersection with the unchanged accepted rear shelf.')

# 07: unchanged zones only, not released purchased-hardware drill patterns.
fig,ax=plt.subplots(figsize=(13,8));plan(ax,parts['BackboxFloorV32'],'#e5d7bd');top(ax)
for p in b['preserved_zones']:
    plan(ax,p,colors['channel'] if p['name'].startswith('Hinge') else colors['lock'] if p['name'].startswith('Lock') else '#4a4a4a',.3)
for x in (-30.1625,630.1625):
    ax.scatter([x],[1295.4],marker='+',s=65,color='#111111')
    ax.text(x,1273,'HINGE\nMATERIAL',ha='center',fontsize=8)
for x in (120,480):
    ax.plot([x,x],f['lock_safe_center_y_interval_mm'],ls='--',color='#111111')
    ax.text(x,1197,'LOCK X\nY pending',ha='center',fontsize=8)
ax.text(300,1230,'2 × EXISTING CABLE PASSPORTS\nR20 / no new holes',ha='center',fontsize=8)
ax.text(300,1080,'HINGE / LOCK ZONES PRESERVED\nReference marks only — no final drill pattern',ha='center',fontsize=10)
save(fig,'07-preserved-hinge-lock-cable-zones.png','V32 / PRESERVED HARDWARE AND CABLE ZONES','Physical hinge and final lock Y remain measurement gates; current shelf passport matching remains unresolved.')

# 08: true first sampled collision, not a 45/90 success pose.
first=r['fold']['first_structural_collision']
if first:
    fig,axs=plt.subplots(1,2,figsize=(13,8));ax=axs[0]
    section(ax,13,['SIDE_L','BACKBOX_BASE'],colors['cabinet'])
    section(ax,13,['Fold_BackboxFloorV32'],colors['floor'],.8)
    for p in b.get('first_intersections',[]):
        section(ax,13,[p['name']],colors['problem'])
    side(ax,(1110,1305),(581,620));ax.set_title('Actual wood • first sampled angle1°')
    ax=axs[1];ax.axis('off');ax.text(0,.95,'BASELINE FOLD: BLOCKED AT 1°',fontsize=14,weight='bold',color=colors['problem'])
    ax.text(0,.81,'BackboxFloorV32 penetrates:\nBACKBOX_BASE: 88,825.889 mm³\nSIDE_L: 3,365.071 mm³\nSIDE_R: 3,365.071 mm³\n\nPivot and cabinet geometry are unchanged.\nMatrix supports are excluded from baseline\ncollision authority; they are not redesigned.\n\n45° / 90° success views: NOT GENERATED\nBaseline is invalid before those angles.',va='top',linespacing=1.65)
    save(fig,'08-first-fold-bottleneck.png','V32 / FIRST REAL FOLD BOTTLENECK','All 91 baseline poses tested; first collision at1° does not invalidate the corrected upright interface.')

# Only a clear baseline THROUGH each angle permits the corresponding review.
for number,angle in ((9,45),(10,90)):
    if not r['fold']['review_45_90_eligible'][str(angle)]:continue
    fig=plt.figure(figsize=(13,9));ax=fig.add_subplot(111,projection='3d');context3(ax);poly3(ax,b['poses']['VALID_THROUGH_'+str(angle)]);iso(ax)
    save(fig,f'{number:02d}-{angle}-degree-valid-baseline.png',f'V32 / BASELINE CLEAR THROUGH {angle}°','Actual wood collision authority; no coarse box substituted.')
(O/'review-images.json').write_text(json.dumps({'images':images,'count':len(images),
    'omitted':{str(a):'baseline collision before requested angle' for a in (45,90) if not r['fold']['review_45_90_eligible'][str(a)]},'real_cad_only':True},indent=2)+'\n')
assert len(images)==8

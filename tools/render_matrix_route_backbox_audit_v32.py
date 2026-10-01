"""Eight real-CAD diagnostic views; no concept art. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

R=Path(__file__).resolve().parents[1]
O=R/'exports/generated/matrix-route-backbox-audit-v32'
b=json.loads((O/'audit-mesh.json').read_text())
r=json.loads((O/'validation.json').read_text())
wood={p['name']:p for p in b['wood']}
ctx={p['name']:p for p in b['rear_context_cutaway']}
colors={'wood':'#b9945f','cabinet':'#c6ccd1','channel':'#0072b2','collision':'#d55e00',
        'display':'#56b4e9','dmd':'#cc79a7','support':'#e69f00','coarse':'#929ca5'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,
                     'axes.labelsize':9,'figure.facecolor':'white','axes.facecolor':'white'})
images=[]


def poly3(ax,p,color,alpha=1):
    v=np.array(p['vertices'])
    collection=Poly3DCollection([v[f] for f in p['faces']],facecolor=color,
        edgecolor='none',alpha=alpha,zsort='average')
    ax.add_collection3d(collection)


def wood3(ax,parts,alpha=1):
    # One collection depth-sorts individual faces across all eight members.
    faces=[];shades=[]
    palette={'BackboxFloorV14':'#aa8050','BackboxTopV14':'#cfad7c',
             'BackboxLeftSideV14':'#c19b67','BackboxRightSideV14':'#c19b67'}
    for p in parts:
        v=np.array(p['vertices'])
        faces.extend(v[f] for f in p['faces'])
        shades.extend([palette.get(p['name'],'#b9945f')]*len(p['faces']))
    ax.add_collection3d(Poly3DCollection(faces,facecolors=shades,edgecolor='none',alpha=alpha))


def view3(ax,rear=True):
    ax.set(xlim=(-130,730),ylim=(940,1370) if rear else (0,1390),
           zlim=(440,1370) if rear else (0,1100))
    ax.set_box_aspect((860,430,930) if rear else (860,1390,1100))
    ax.view_init(elev=23,azim=-58)
    ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_zlabel('Z / mm')
    ax.tick_params(labelsize=8)


def section(ax,x,names,color,alpha=1):
    for name in names:
        for points in b['sections'][str(x)].get(name,[]):
            ax.add_patch(plt.Polygon(points,closed=True,facecolor=color,
                         edgecolor='#39444d',lw=.6,alpha=alpha))


def side_axes(ax,xlim,ylim):
    ax.set(xlim=xlim,ylim=ylim,xlabel='Y / mm (front → rear)',ylabel='Z / mm')
    ax.set_aspect('equal',adjustable='box')
    ax.grid(alpha=.16)


def save(fig,name,title,subtitle):
    fig.suptitle(title,x=.055,ha='left',y=.97,fontsize=19,weight='bold',color='#213440')
    fig.text(.055,.92,subtitle,fontsize=10,color='#4a5359')
    fig.text(.055,.035,'REAL CAD • source reconstruction / accepted cabinet unchanged • MANUFACTURING BLOCKED',fontsize=9)
    fig.subplots_adjust(left=.07,right=.96,top=.86,bottom=.13,wspace=.23)
    path=O/name
    fig.savefig(path,dpi=160)
    plt.close(fig)
    images.append({'path':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                   'source_mesh_sha256':hashlib.sha256((O/'audit-mesh.json').read_bytes()).hexdigest()})
    print('ROUTE_BACKBOX_IMAGE_PASS',name)


# 01: real reconstructed members, not a solid envelope pretending to be wood.
fig=plt.figure(figsize=(13,9))
ax=fig.add_subplot(121,projection='3d')
for n,p in ctx.items():
    if n in ('SIDE_R','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR'):
        poly3(ax,p,colors['channel'] if 'Channel' in n else colors['cabinet'])
wood3(ax,wood.values())
view3(ax)
ax.set_title('Eight source wood members • upright')
ax2=fig.add_subplot(122)
ax2.axis('off')
ax2.text(0,.96,'0° SANITY GATE: FAIL',fontsize=16,weight='bold',color=colors['collision'])
ax2.text(0,.83,'Reconstructed from documented sources\n• floor / two sides / top\n• four fixed rear frame strips\n• existing t/3 joint recipe\n\nInternal wood joints: no overlaps\nExternal interface: floor intersects both\naccepted glass channels\n\nNo integrated detailed V32 backbox existed.\nFront structural wood is not defined.\nSource speaker carriers are removable plates;\ntheir material is still unconfirmed.',va='top',linespacing=1.7)
save(fig,'01-upright-actual-backbox-wood.png','V32 / UPRIGHT BACKBOX WOOD','Source geometry reconstructed in an isolated CAD document; not promoted to a manufacturing assembly.')

# 02: same exact section for structural members and rejected coarse representation.
fig,axs=plt.subplots(1,2,figsize=(13,8))
for ax in axs:
    section(ax,13,['SIDE_L','BACKBOX_BASE'],colors['cabinet'])
    section(ax,13,['CandidateGlassChannelL'],colors['channel'])
    side_axes(ax,(960,1340),(460,1360))
section(axs[0],13,list(wood),colors['wood'])
section(axs[1],13,['PF_BackboxCheckEnvelope'],colors['coarse'],.45)
axs[0].set_title('Structural wood • section X=13 mm')
axs[1].set_title('PF_BackboxCheckEnvelope • same section')
axs[1].text(1100,960,'EMPTY INTERIOR\nincorrectly occupied\nby the coarse solid',fontsize=11)
save(fig,'02-coarse-envelope-comparison.png','V32 / WOOD ≠ SOLID PACKAGING BOX','The coarse envelope includes the entire cavity and is not a structural collision authority.')

# 03: invariant accepted reference axis, with floor/channel section included.
fig,axs=plt.subplots(1,2,figsize=(13,8))
ax=axs[0]
section(ax,13,list(wood),colors['wood'])
section(ax,13,['SIDE_L','BACKBOX_BASE'],colors['cabinet'])
section(ax,13,['CandidateGlassChannelL'],colors['channel'])
ax.plot([1020,1320],[508,508],'--',color='#39444d',lw=.8)
ax.scatter([1270],[508],s=90,marker='+',color=colors['collision'])
ax.annotate('WPC reference axis\nY1270 / Z508\nØ12.7 reference',xy=(1270,508),xytext=(1050,485),arrowprops={'arrowstyle':'->'},fontsize=10)
ax.annotate('',xy=(1308.1,535),xytext=(1270,535),arrowprops={'arrowstyle':'<->'})
ax.text(1289,542,'38.1',ha='center')
side_axes(ax,(1000,1335),(460,675))
ax.set_title('Side datum • unchanged')
ax=axs[1]
ax.add_patch(Rectangle((-90,0),780,75,facecolor=colors['wood'],edgecolor='#39444d'))
ax.add_patch(Rectangle((0,-35),600,25,facecolor=colors['cabinet'],edgecolor='#39444d'))
for outer,ref in [(-90,-30.1625),(690,630.1625)]:
    ax.plot([ref,ref],[-5,90],'--',color=colors['channel'])
    ax.annotate('',xy=(outer,96),xytext=(ref,96),arrowprops={'arrowstyle':'<->'})
    ax.text((outer+ref)/2,107,'59.8375',ha='center',fontsize=9)
ax.text(300,34,'BACKBOX OUTER 780 mm',ha='center',weight='bold')
ax.text(300,-26,'CABINET OUTER 600 mm',ha='center')
ax.text(300,-85,'Inset = (780 − 600 − 60.325) / 2\nPhysical hinge assembly measurement required',ha='center',va='top',linespacing=1.7)
ax.set(xlim=(-150,750),ylim=(-220,180));ax.set_aspect('equal');ax.axis('off')
ax.set_title('Floor outer-edge datum • reference only')
save(fig,'03-pivot-datum-close-up.png','V32 / WPC PIVOT DATUM','No guessed bracket pattern, bend offsets, bushing length or final CNC hinge holes.')

# 04: exact OCC plane sections of the colliding objects (not bounding rectangles).
fig,axs=plt.subplots(1,2,figsize=(13,8))
ax=axs[0]
section(ax,13,['SIDE_L'],colors['cabinet'])
section(ax,13,['BackboxFloorV14'],colors['wood'],.75)
section(ax,13,['CandidateGlassChannelL'],colors['channel'])
section(ax,13,['Collision_CandidateGlassChannelL'],colors['collision'])
side_axes(ax,(1045,1135),(584,624))
ax.set_title('Exact CAD section • X=13 mm / 0°')
ax.annotate('Overlapping floor / channel',xy=(1108,604),xytext=(1050,617),arrowprops={'arrowstyle':'->'},fontsize=9)
ax=axs[1];ax.axis('off')
ax.text(0,.94,'FIRST PROBLEM: ALREADY AT 0°',fontsize=14,weight='bold',color=colors['collision'])
ax.text(0,.79,'BackboxFloorV14 × CandidateGlassChannelL/R\n\nVolume: 937.450518 mm³ per side\nY intersection: 1063.187781 … 1118.338155\nZ intersection: 596.900000 … 606.246801\nVertical extent: 9.346801 mm\n(not a minimum translation distance)\n\nLeft X: 0 … 18 mm\nRight X: 582 … 600 mm\n\nThe shelf contact plane is Z596.9.\nThe older full-depth floor starts at Y1054.1.\nIt overlaps the upward-sloping channels.',va='top',linespacing=1.55)
save(fig,'04-first-real-interface-problem.png','V32 / ZERO-STATE INTERFACE FAILURE','Two symmetric positive-volume intersections. Fold validation stops here; accepted parts remain unchanged.')

# 05/06: specifically requested static poses, prominently not motion evidence.
for angle in (45,90):
    fig=plt.figure(figsize=(13,9));ax=fig.add_subplot(111,projection='3d')
    for p in b['cabinet_context']:
        if p['name'] in ('SIDE_R','BACKBOX_BASE','PLAYFIELD_ENVELOPE','PF_BasePlywood','CandidateGlassChannelR'):
            poly3(ax,p,colors['channel'] if 'Channel' in p['name'] else colors['cabinet'],.6)
    wood3(ax,b['static_poses'][f'DIAGNOSTIC_{angle}_NOT_VALIDATED'])
    for p in b['reference_datums']:poly3(ax,p,colors['collision'])
    view3(ax,False)
    fig.text(.06,.80,'ILLUSTRATION ONLY\nINVALID 0° START\nNO SWEEP / NO CLEARANCE CLAIM',color=colors['collision'],weight='bold',fontsize=12,linespacing=1.7)
    save(fig,f'{5 if angle==45 else 6:02d}-{angle}-degree-diagnostic.png',f'V32 / {angle}° REFERENCE-AXIS POSE — NOT VALIDATED','Static transformation of reconstructed wood. The zero-state stop rule remains in force.')

# 07: display / DMD packaging logically and visually separate from wood.
fig=plt.figure(figsize=(13,9))
ax=fig.add_subplot(121,projection='3d')
wood3(ax,wood.values(),.24)
for p in b['display_reserves']:poly3(ax,p,colors['dmd'] if p['name'].startswith('DMD') else colors['display'],.85)
for p in b['front_carriers_material_unconfirmed']:poly3(ax,p,colors['support'])
view3(ax);ax.set_title('Distinct CAD groups • upright source placement')
ax2=fig.add_subplot(122);ax2.axis('off')
ax2.legend(handles=[Patch(color=colors['wood'],label='Structural wood'),Patch(color=colors['display'],label='Backglass service envelope'),Patch(color=colors['dmd'],label='Located source DMD payload'),Patch(color=colors['support'],label='Replaceable speaker carriers')],loc='upper left',frameon=False)
ax2.text(0,.62,'Backglass: 740 × 100 × 450 mm (XYZ)\nDMD located payload: 190 × 55 × 90 mm\n\nFuture DMD service requirement:\n450 × 80 × 230 mm (XYZ)\nIts position is not confirmed; not invented here.\n\nSpeaker carriers: material unconfirmed.\nFixed front structural members: not defined.\n\nHarness / pinch-zone sweep: UNVERIFIED.\nNo complete moving harness exists in this CAD.',va='top',linespacing=1.6)
save(fig,'07-display-separated-from-wood.png','V32 / STRUCTURE AND SERVICE RESERVES','Upright display/DMD packaging is separate; none of these volumes is silently treated as wood.')

# 08: only the permitted zero-state comparison; there is no valid fold baseline yet.
fig,axs=plt.subplots(1,2,figsize=(13,8))
ax=axs[0]
section(ax,45,['BackboxFloorV14'],colors['wood'])
section(ax,45,['BACKBOX_BASE'],colors['cabinet'])
section(ax,45,['MX_WoodSeatL'],colors['support'])
section(ax,45,['MX_FixedScrewL1','MX_FixedScrewL2','MX_InsertL'],'#4a4a4a')
side_axes(ax,(1050,1220),(515,635))
ax.set_title('Left support • exact CAD section X=45 mm')
ax.text(1140,620,'SOURCE BACKBOX FLOOR',fontsize=9)
ax.text(1140,583,'ACCEPTED REAR SHELF',fontsize=8)
ax.text(1080,529,'ACCEPTED MATRIX WOOD SEAT',fontsize=8)
ax=axs[1];ax.axis('off')
ax.text(0,.94,'NO ADDED CONFLICT AT 0°',fontsize=15,weight='bold')
ax.text(0,.79,'Cassette and glass explicitly removed.\nTwo stationary seats / fixed screws retained.\n\nSource backbox wood to stationary matrix\nparts: minimum 6.900 mm at screw tips.\nNo matrix part causes the channel conflict.\n\nNew conflict during fold: UNDETERMINED.\nA valid baseline is required before comparison.\n\nNo support correction or redesign applied.\nDo not read this view as a fold approval.',va='top',linespacing=1.65)
save(fig,'08-stationary-matrix-supports-zero-only.png','V32 / MATRIX SUPPORTS — BASELINE GATE PENDING','A validated fold baseline does not yet exist. This comparison is explicitly limited to 0°.')
(O/'review-images.json').write_text(json.dumps({'images':images,'count':len(images),'real_cad_only':True,
    'fold_sweep_validated':False},indent=2)+'\n')
assert len(images)==8

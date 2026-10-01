"""Actual CAD profile and reserve comparisons; no selected/fold-success fiction. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon,Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-profile-v32';b=json.loads((O/'mesh.json').read_text());r=json.loads((O/'validation.json').read_text());rows={x['bottom_depth_mm']:x for x in r['candidates']}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'figure.facecolor':'white'})
colors={210:'#0072b2',200:'#e69f00',190:'#cc79a7',180:'#4a4a4a'};images=[]
def save(fig,name,title,subtitle):
    fig.suptitle(title,x=.06,y=.97,ha='left',fontsize=18,weight='bold',color='#253743')
    fig.text(.06,.92,subtitle,fontsize=10,color='#4a4a4a')
    fig.text(.06,.025,'REAL CAD STUDY • NO PROFILE SELECTED • OWNER STOP BELOW 190 mm • MANUFACTURING BLOCKED',fontsize=9)
    fig.subplots_adjust(left=.09,right=.94,bottom=.22 if name.startswith(('10-','11-')) else .14,top=.83,wspace=.35)
    p=O/name;fig.savefig(p,dpi=150);plt.close(fig)
    images.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    print('BACKBOX_PROFILE_IMAGE_PASS',name)
def profile(ax,depth,alpha=.22):
    for pp in b['candidates'][str(depth)]['side_loops']:ax.add_patch(Polygon(pp,facecolor=matplotlib.colors.to_rgba(colors[depth],alpha),edgecolor=colors[depth],lw=1.5))
    ax.set(xlim=(1025,1340),ylim=(565,1350),xlabel='Y / mm (front → rear)',ylabel='Z / mm');ax.set_aspect('equal');ax.grid(alpha=.15)
def projected(ax,p,dims,color,alpha=1):
    vv=np.array(p['vertices']);polys=[vv[f][:,dims] for f in p['faces']]
    ax.add_collection(PolyCollection(polys,facecolors=color,edgecolors='none',alpha=alpha,antialiased=False))
def part(depth,name,group='wood'):return next(p for p in b['candidates'][str(depth)][group] if p['name']==name)
def scene(ax,depth,cutaway=False):
    faces=[];facecolors=[]
    for p in b['candidates'][str(depth)]['wood']:
        if cutaway and p['name']=='BackboxRightSideV14':continue
        vv=np.array(p['vertices']);base=np.array(matplotlib.colors.to_rgb('#be9b65' if 'Floor' not in p['name'] else colors[depth]))
        for f in p['faces']:
            triangle=vv[f];n=np.cross(triangle[1]-triangle[0],triangle[2]-triangle[0]);norm=np.linalg.norm(n)
            shade=.7+.3*abs(np.dot(n/norm,np.array([.3,-.4,.866]))) if norm>1e-9 else .8
            faces.append(triangle);facecolors.append(base*shade)
    ax.add_collection3d(Poly3DCollection(faces,facecolors=facecolors,edgecolors='none'))
    ax.set(xlim=(-110,710),ylim=(1020,1325),zlim=(575,1340));ax.set_box_aspect((820,305,765));ax.view_init(24,-55);ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z')

fig,ax=plt.subplots(figsize=(12,8))
old=next(p for p in b['legacy'] if p['name']=='BackboxLeftSideV14');projected(ax,old,[1,2],'#bc9e70')
ax.set(xlim=(1025,1340),ylim=(565,1350),xlabel='Y / mm',ylabel='Z / mm');ax.set_aspect('equal');ax.grid(alpha=.15)
ax.text(1320,920,'254 mm depth\nfull height\n723.9 mm',va='center',fontsize=12)
save(fig,'01-old-v14-side.png','01 / INHERITED RECTANGULAR SIDE','Actual reconstructed V14 wood; reference only. Its depth is not retained as the proposed lower profile.')

fig,(ax,tx)=plt.subplots(1,2,figsize=(13,8));profile(ax,210);tx.axis('off');q=rows[210]
tx.text(0,.95,f'BOTTOM OUTER DEPTH: 210 mm\nTOP DEPTH: 254 mm\nFRONT SLOPE: {q["slope_deg_from_vertical"]:.4f}° from vertical\n\n18 mm side; one CNC solid\n6 mm captured floor joint\nSquare-cut floor / top edges\n\nUPRIGHT: REJECTED\nFloor intersects accepted channels.\n\nNo fold test follows invalid zero.',va='top',linespacing=1.7)
save(fig,'02-candidate-210-side.png','02 / DEEPEST REQUESTED CANDIDATE','The sloping side profile is reconstructed first; the floor follows its lower front datum.')

fig,axs=plt.subplots(1,3,figsize=(14,8))
for ax,dep in zip(axs,[200,190,180]):
    profile(ax,dep);q=rows[dep];ax.set_title(f'{dep} mm / {q["slope_deg_from_vertical"]:.3f}°\n'+('WARNING — no selection' if dep==180 else 'ZERO REJECTED'))
save(fig,'03-200-190-180-comparison.png','03 / REMAINING DEPTH CANDIDATES','180 mm is documented only as the owner-requested warning comparison; the below-190 stop applies.')

fig,ax=plt.subplots(figsize=(12,8))
for dep in rows:profile(ax,dep,.10)
ax.legend(handles=[Patch(color=colors[d],label=f'{d} mm') for d in rows],loc='upper right',bbox_to_anchor=(1.6,1))
save(fig,'04-side-profile-overlay.png','04 / PROFILE OVERLAY','Identical 780 mm width, 723.9 mm height, 254 mm top depth, rear datum and floor height.')

fig,axs=plt.subplots(2,2,figsize=(13,9))
for ax,dep in zip(axs.flat,rows):
    q=rows[dep]
    for pp in b['candidates'][str(dep)]['floor_loops']:ax.plot(np.array(pp)[:,0],np.array(pp)[:,1],color=colors[dep])
    ax.axhline(1127.125,color='#4a4a4a',ls='--');ax.set(xlim=(-90,690),ylim=(1080,1320),xlabel='X / mm',ylabel='Y / mm');ax.set_aspect('equal');ax.set_title(f'{dep} mm candidate — panel depth {q["bottom_panel_depth_mm"]:.1f} mm')
save(fig,'06-candidate-floors-no-selection.png','06 / DERIVED CANDIDATE FLOORS — NO SELECTION','Two original cable passports retained. Dashed line: unchanged rear-shelf front Y1127.125.')

fig,(ax,tx)=plt.subplots(1,2,figsize=(13,7))
for p in b['context']:
    if p['name'] in ('BACKBOX_BASE','CandidateGlassChannelL'):projected(ax,p,[1,2],'#a9b1b8' if p['name']=='BACKBOX_BASE' else '#0072b2',.9)
for dep in rows:projected(ax,part(dep,'BackboxFloorV14'),[1,2],colors[dep],.25)
ax.set(xlim=(1085,1320),ylim=(568,630),xlabel='Y / mm',ylabel='Z / mm');ax.set_aspect('equal');ax.grid(alpha=.15);tx.axis('off')
tx.text(0,.95,'SHELF FORWARD PROJECTION\n(positive means shelf ahead of backbox)\n\n'+'\n'.join(f'{d} mm: {rows[d]["shelf_projection_forward_mm"]:+.3f} mm' for d in rows)+'\n\n210 / 200 / 190 fail upright channels.\n180 passes zero, but is below owner limit.\n\nShelf and channels remain unchanged.',va='top',linespacing=1.7)
save(fig,'08-shelf-lower-backbox-relation.png','08 / SHELF AND LOWER BACKBOX','Actual floor/channel/shelf CAD projections. Overlap is rejected, never treated as an intended mating contact.')

fig,(ax,tx)=plt.subplots(1,2,figsize=(13,8));profile(ax,180)
for p in b['context']:
    if p['name']=='BACKBOX_BASE':projected(ax,p,[1,2],'#a9b1b8')
ax.plot(1270,508,'ko',ms=8);ax.plot(1220,596.9,'o',color='#d55e00');ax.annotate('',xy=(1220,566.9),xytext=(1220,596.9),arrowprops={'arrowstyle':'->','color':'#d55e00','lw':2});ax.set_ylim(480,1350);tx.axis('off')
tx.text(0,.95,'UNCHANGED REFERENCE AXIS\nY1270 / Z508 mm\nØ12.7 reference\n\nSHARED BEARING POINT\nY1220 / Z596.9 mm\n\nInitial vertical velocity:\ndZ/dθ = Y − Ypivot = −50 mm/rad\n\nThe contact initially moves into the shelf.\nA sloped front does not change this.\n\nThis is a local analytical incompatibility,\nnot a fold sweep of a rejected candidate.',va='top',linespacing=1.6)
save(fig,'09-hinge-bearing-relationship.png','09 / PIVOT AND BEARING INCOMPATIBILITY','180 mm warning profile shown upright only. No accepted axis, shelf or floor-height datum was moved.')

zc={'DisplayStructureReserve':'#56b4e9','SpeakerDMDReserve':'#e69f00','HarnessCorridor':'#4a4a4a','HingeKeepout':'#d55e00','ServiceToolKeepout':'#bdbdbd','DisplayRailsReserve':'#cc79a7','AvailableToyAreaL':'#0072b2','AvailableToyAreaR':'#0072b2'}
for side,num in [('L','10'),('R','11')]:
    fig,axs=plt.subplots(1,4,figsize=(15,8))
    for ax,dep in zip(axs,rows):
        profile(ax,dep,.08)
        for p in b['candidates'][str(dep)]['zones']:
            if p['name'] in zc and (not p['name'].startswith('AvailableToy') or p['name'].endswith(side)):projected(ax,p,[1,2],zc[p['name']],.9)
        ax.set_title(f'{dep} mm\n{rows[dep]["toy_area_each_side_mm2"]/100:.1f} cm² available')
    fig.legend(handles=[Patch(color=v,label=k.replace('Reserve','').replace('AvailableToyAreaL','AvailableToyArea'+side)) for k,v in zc.items() if k!='AvailableToyAreaR'],loc='lower center',bbox_to_anchor=(.5,.07),ncol=4,fontsize=8)
    save(fig,f'{num}-{side.lower()}-future-toy-zones.png',f'{num} / {side} SIDE MOUNTING CAPACITY','Blue: remaining candidate area with 40 mm inward depth. No hypothetical component holes or mandatory toy BOM.')

fig=plt.figure(figsize=(13,8));ax=fig.add_subplot(121,projection='3d');scene(ax,210,True);tx=fig.add_subplot(122);tx.axis('off')
for name,col in [('RemovableRearBoardServiceReserve','#0072b2'),('LowerServiceToyReserve','#e69f00')]:
    p=part(210,name,'zones');vv=np.array(p['vertices']);ax.add_collection3d(Poly3DCollection([vv[f] for f in p['faces']],facecolors=col,edgecolors=col,alpha=.25))
tx.text(0,.95,'GENERIC REMOVABLE REAR BOARD\n240 × 300 mm mounting face\n32 mm depth reserve\n12 mm replaceable panel assumption\n\nLOWER SERVICE / TOY ZONE\n160 × 50 × 75 mm\n\nCabinet → removable board → component\nNo proprietary holes in permanent wood.\n\nZones exist in all four candidates.\nThe backbox profiles remain unselected.',va='top',linespacing=1.6)
save(fig,'12-rear-removable-board-zone.png','12 / OPTIONAL INFRASTRUCTURE RESERVES','210 mm candidate shown cutaway by omission of near side for clarity; zones are service volumes, not installed parts.')

fig,(ax,tx)=plt.subplots(1,2,figsize=(13,8))
for dep in rows:
    profile(ax,dep,.06);m=rows[dep]['mass'];ax.plot(m['cg_xyz_mm'][1],m['cg_xyz_mm'][2],'o',color=colors[dep],label=f'{dep}: {m["total_kg"]:.2f} kg')
ax.plot(1270,508,'kx',ms=10);ax.set_ylim(480,1350);ax.legend(loc='upper right',fontsize=8);tx.axis('off')
tx.text(0,.95,'PROVISIONAL MASS / CG\nDensity: assumed 650 kg/m³\nMonitor: assumed 7 kg\nDMD: 1.2 kg; speakers: 1.6 kg\nMounts: 1.5 kg; wires: 1 kg\nElectronics: 1 kg; future fans: 0.4 kg\nFuture optional toys: 4 kg\nAdditional front wood: 1.5 kg\nRear door: nominal wood volume × density\n\nAccepted matrix and cabinet fans:\n0 kg moving backbox contribution.\n\nNo vendor mass or strength certification.\nNo valid folding assembly selected.',va='top',linespacing=1.6)
save(fig,'13-mass-cg-planning.png','13 / MASS BUDGET AND CENTER OF GRAVITY','CAD plywood volumes plus explicit provisional allowances; these figures do not establish a valid motion path.')

fig=plt.figure(figsize=(14,8));ax=fig.add_subplot(121,projection='3d');scene(ax,210);ax.set_title('210 mm — zero rejected');ax=fig.add_subplot(122,projection='3d');scene(ax,180);ax.set_title('180 mm — warning / owner stop')
save(fig,'18-architecture-comparison-no-selection.png','18 / RECONSTRUCTED ARCHITECTURE COMPARISON','Both are actual sloped-side CAD candidates. Neither is selected; no accepted cabinet system is modified.')

omitted={'05':'No selected profile','07':'No selected upright assembly','14':'No authorized candidate fold after upright/below-190 stop','15':'No valid fold through 45 degrees','16':'No valid fold through 90 degrees','17':'No selected wood assembly to explode'}
(O/'review-images.json').write_text(json.dumps({'images':images,'count':len(images),'mesh_sha256':hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest(),'omitted':omitted,'adapted':{'06':'Candidate floor comparison; no selected floor','18':'Candidate architecture comparison; no selected architecture'},'real_cad_only':True},indent=2)+'\n')

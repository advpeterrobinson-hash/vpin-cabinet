"""Actual OCC-mesh review views, not generated concept art. CERN-OHL-S-2.0."""
from pathlib import Path
import json,textwrap,gzip
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/backbox-service-v32'
D=json.loads(gzip.decompress((O/'review-mesh.json.gz').read_bytes()) if (O/'review-mesh.json.gz').exists() else (O/'review-mesh.json').read_bytes());E=json.loads((O/'details.json').read_text());Q=json.loads((O/'validation.json').read_text());M=json.loads((O/'motion-validation.json').read_text())
if D.get('format')=='deduplicated-cad-mesh-v1':
    bank=D.pop('meshes')
    for field in ['parts','blanks','zones','drivers']:D[field]=[bank[key] for key in D[field]]
    D['states']={name:[bank[key] for key in keys] for name,keys in D['states'].items()}
assert all(c['pass'] for c in Q['checks']) and M['pass']
D['states']['thin-display-toys']=E['shallow_display']
assert E['shallow_display_validation']['pass']
parts={p['name']:p for p in D['parts']};files=[]
plt.rcParams.update({'font.size':10,'figure.facecolor':'#f8fafc','axes.facecolor':'#f8fafc','font.family':'DejaVu Sans'})
def color(n):
    for key,c in [('ToyZone','#38a879'),('Flex','#9b57b8'),('Gasket','#343d42'),('Liner','#424a4d'),('Pad','#424a4d'),('Backglass','#7ac5d8'),('Display32','#3e729e'),('DMDEnvelope','#527b9c'),('SpeakerEnvelope','#666b72'),('FanBlank','#a0a8ac'),('Fan','#a86555'),('Intake','#9caa94'),('Reserve','#85689f'),('Door','#bca07b'),('RearFrame','#8e765d'),('Carrier','#d5bb91'),('VESA','#d5bb91'),('Rail','#a99575'),('Side','#7b8794')]:
        if key in n:return c
    return '#bfab89'
def label(n):return n.removeprefix('BB_')
def note(ax,s):
    ax.axis('off');lines=[]
    for line in s.split('\n'):lines.extend(textwrap.wrap(line,43,break_long_words=False) or [''])
    ax.text(.03,.97,'\n'.join(lines),va='top',linespacing=1.42,fontsize=10.3)
def select(state='rear-closed',include=None,exclude=()):
    return [m for m in D['states'][state] if (include is None or any(k in m['name'] for k in include)) and not any(k in m['name'] for k in exclude)]
edge_cache={}
def edges(m):
    if id(m) in edge_cache:return edge_cache[id(m)]
    v=np.asarray(m['vertices']);adj={}
    for tri in m['faces']:
        a,b,c=v[tri];normal=np.cross(b-a,c-a);ln=np.linalg.norm(normal)
        if ln<1e-10:continue
        normal/=ln
        for ia,ib in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:
            key=tuple(sorted([tuple(np.round(v[ia],5)),tuple(np.round(v[ib],5))]));adj.setdefault(key,[]).append(normal)
    result=np.array([key for key,ns in adj.items() if len(ns)==1 or any(abs(np.dot(ns[0],n))<.995 for n in ns[1:])]);edge_cache[id(m)]=result;return result
def view3(ax,items,rear=True,explode=False,full=False,alpha_override=None):
    for m in items:
        n=m['name'];v=np.asarray(m['vertices']);f=np.asarray(m['faces']);a=.94
        if n in ['BB_SideL','BB_SideR','BB_Top','BB_TopFrontRail']:a=.16
        if 'Display32' in n:a=.26 if rear else .65
        if 'Backglass' in n:a=.15
        if 'ToyZone' in n:a=.5
        if 'Reserve' in n:a=.3
        if 'Envelope' in n:a=.65
        if 'Flex' in n:a=.8
        if full and not n.startswith('BB_'):a=.15
        if alpha_override and n in alpha_override:a=alpha_override[n]
        ax.add_collection3d(Poly3DCollection(v[f],facecolor=color(n),edgecolor='none',linewidth=0,alpha=a))
        es=edges(m)
        if len(es):ax.add_collection3d(Line3DCollection(es,colors='#38434d',linewidths=.55,alpha=min(.8,a+.15)))
    if full:
        ax.set(xlim=(-140,740),ylim=(-100,1360),zlim=(0,1370));ax.set_box_aspect((880,1460,1370));ax.view_init(elev=23,azim=-48)
    else:
        ax.set(xlim=(-160,760),ylim=((750,1700) if explode else (1020,1740)),zlim=(585,1505 if explode else 1345));ax.set_box_aspect((920,950 if explode else 720,920 if explode else 760));ax.view_init(elev=16,azim=67 if rear else -69)
    ax.set(xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm');ax.tick_params(labelsize=8)
def projection(ax,items,dims=(0,2),limits=None,alpha=.65):
    for m in items:
        v=np.asarray(m['vertices']);f=np.asarray(m['faces']);ax.add_collection(PolyCollection(v[f][:,:,dims],facecolor=color(m['name']),edgecolor='none',linewidth=0,alpha=alpha))
        es=edges(m)
        if len(es):ax.add_collection(PolyCollection([],facecolors='none'))
        for edge in es:ax.plot(edge[:,dims[0]],edge[:,dims[1]],color='#354553',lw=.5)
    ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_xlabel('XYZ'[dims[0]]+' / mm');ax.set_ylabel('XYZ'[dims[1]]+' / mm')
    if limits:ax.set(xlim=limits[0],ylim=limits[1])
def finish(fig,key,title,cad,diagnostic=False):
    fig.suptitle(key+'  '+title,x=.04,ha='left',fontweight='bold',fontsize=15)
    fig.text(.04,.025,('REJECTED ACCESSORY STUDY' if diagnostic else 'REVIEW CANDIDATE — NOT PROMOTED')+' • actual CAD • purchased hardware provisional • manufacturing BLOCKED • CERN-OHL-S-2.0',fontsize=8.5,color='#884538')
    fig.subplots_adjust(top=.87,bottom=.12,left=.055,right=.97,wspace=.2)
    fn=key+'-review.png';fig.savefig(O/fn,dpi=160);plt.close(fig);files.append({'id':key,'title':title,'file':fn,'cad':cad+'.FCStd','diagnostic_only':diagnostic})
def standard(key,title,state,text,include=None,exclude=(),rear=True,explode=False,full=False,diagnostic=False):
    fig=plt.figure(figsize=(14,8));gs=fig.add_gridspec(1,2,width_ratios=[2.3,1]);ax=fig.add_subplot(gs[0],projection='3d');view3(ax,select(state,include,exclude),rear,explode,full);
    if state=='glass-removal':ax.set_zlim(590,1835);ax.set_box_aspect((920,720,1245))
    if state=='monitor-removal':ax.set_ylim(650,1360);ax.set_box_aspect((920,710,760))
    if state in ['rear-closed','blank-fans','toy-zones','optional-shelf']:ax.set_ylim(1020,1380);ax.set_box_aspect((920,360,760))
    note(fig.add_subplot(gs[1]),text);finish(fig,key,title,state,diagnostic)
standard('A','Rear closed — two plywood leaves','rear-closed','Two 12 mm plywood doors\n628 mm high; 351 mm wide each\n\nOne continuous hinge on each outer edge.\nPassive LEFT: two internal bolts.\nActive RIGHT: one exterior key lock.\n\nNo fixed center mullion.\nBoth leaves must be latched before folding.',include=['Door','Fan','Intake','Hinge','RearFrame','Side','Top','CamLockBarrel'],exclude=['DustHood','Strain','MeshReserve'])
standard('B','Passive left door open — active leaf already released','rear-both-open','LEFT = passive leaf\nRetract its upper and lower bolts only after opening the active RIGHT leaf.\n\nShown at 100°. Right leaf remains open to clear the center overlap.\n\nOpening the passive leaf alone against a locked active leaf is intentionally not a valid service state.',exclude=['MeshReserve'])
standard('C','Active right door open','rear-active-open','RIGHT = active leaf\nUnlock cam; swing outward to 100°.\n\nThe passive leaf remains closed.\nIts retaining bolts are now accessible.\n\nThe provisional cam-body reserve has clearance through the initial 2–4° transition.',exclude=['MeshReserve'])
standard('D','Both rear doors open','rear-both-open','Clear fixed-frame aperture: 684 × 608 mm\nAbout 81% of the internal rear rectangle.\n\nMonitor rails sit inside the enclosure. Doors carry no monitor load and are not shear members.\n\nReserve at least 400 mm behind the cabinet for the modeled sweep; 450 mm is a useful planning allowance for hands.',exclude=['MeshReserve'])
fig,ax=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1.8,1]});projection(ax[0],E['sections']['center_lock_z960'],(0,1),((275,365),(1280,1330)));note(ax[1],'Actual CAD section at Z960\n\nPassive astragal: 36 × 12 mm\nActive leaf overlaps its gasket land.\nReplaceable 2 mm compressed gasket reserve.\n\nCam body / tongue / key barrel are packaging reserves. Selected lock must provide suitable throw and gasket compression.\n\nNo exact lock SKU or bore released.');finish(fig,'E','Center overlap and keyed lock','rear-closed')
fig=plt.figure(figsize=(14,8));gs=fig.add_gridspec(1,2,width_ratios=[1.8,1]);ax=fig.add_subplot(gs[0]);projection(ax,select(include=['DoorL','HingeCleatL','PianoHingeReserveL','PianoLeafFixedL','PianoLeafDoorL']),(0,1),((-90,-10),(1295,1345)));note(fig.add_subplot(gs[1]),'Outer continuous hinge — left plan projection\n\nAxis X−55 / Y1324.1\n628 mm knuckle/leaf reserve\nR2.5 knuckle packaging envelope\n\n23 × 14 mm fixed plywood hinge cleat.\nFinal hinge leaf width, screw pitch and swing offset require purchased hardware measurement.\n\nPurple geometry is a hardware reserve, not a fabricated hinge drawing.');finish(fig,'F','Piano hinge and outer mounting land','rear-closed')
standard('G','One optional 120 mm fan station per door','rear-closed','120 × 120 × 25 mm occupied envelope\n105 mm square mounting pitch\nØ116 mm door opening\n\nCommon removable guard and mesh/filter provision.\nNo fan manufacturer selected.\n\nThe shallow downward hood is NOT selected: its mouth would be only 24% of the fan opening. Fine exhaust filters also need pressure-loss testing.',include=['Door','Fan','Hinge'],exclude=['DustHood','Strain','MeshReserve'])
standard('H','Blank modules — identical door machining','blank-fans','Fan station OR blank module\nSame Ø116 opening and 105 mm reference mounting family.\n\n128 × 128 × 6 mm plywood blanks\nNo fan or flexible fan wiring required for the basic flatpack.\n\nFanless thermal performance is not qualified.',include=['Door','FanBlank','Intake','Hinge','RearFrame','Side','Top'],exclude=['MeshReserve'])
standard('I','Dedicated low passive intake','rear-closed','Two 220 × 80 mm low intake openings\nEach has a removable filter/mesh frame and an inward/downward baffle.\n\nGross area: 35,200 mm² total\n65% mesh planning area: 22,880 mm²\nBaffle throats: 15,840 mm² total\n\nThe narrowest section limits flow. Neither airflow rate nor thermal adequacy is certified. Cable passage is not an intake.',include=['Door','Intake','RearFrame'],exclude=['MeshReserve'])
fig,ax=plt.subplots(1,2,figsize=(14,8),gridspec_kw={'width_ratios':[1.7,1]});projection(ax[0],E['sections']['airflow_x155'],(1,2),((1070,1345),(590,1340)),.6)
path=[(1328,735),(1288,735),(1288,676),(1250,676),(1250,800),(1262,880),(1262,1160),(1328,1160)]
for a,b in zip(path,path[1:]):ax[0].annotate('',b,a,arrowprops={'arrowstyle':'->','lw':2,'color':'#bc553d'})
note(ax[1],'Actual CAD section at X155\nArrows show intended flow, not CFD.\n\nLow intake is directed downward toward the DMD / speaker region, then toward the rear display plenum and upper exhaust.\n\nThe two 50 mm carrier stiles create local restrictions; air can bypass them in X.\n\nNo nearby high intake is placed beside the fans. Rear-plenum bypass and filter loading require thermal testing.');finish(fig,'J','Airflow section — geometry and restrictions','rear-closed')
standard('K','32-inch display installed','rear-both-open','Primary envelope: 740 × 450 × 100 mm\nFront installation / removal\n744 mm internal width\n\nTwo fixed crossmembers support a removable plywood ladder and replaceable VESA plate.\n\nFour captive through fasteners and lower threaded stops provide positive capture through fold. No gravity-only hook.',include=['Side','Top','Floor','Monitor','Display','VESA','Backglass','Glass'],rear=False)
standard('L','Rear access to monitor adjustment','rear-both-open','Vertical: ±5 mm\nDepth: two positions, 16 mm apart\nCentering: ±1 mm for a 740 mm chassis; wider slot travel only for smaller displays.\n\nRear clamp access remains open with glass and bezel installed. Depth bolts have discrete positions; threaded lower stops are reset after vertical adjustment.\nFinal bolt, insert and thread engagement qualification pending.',include=['Monitor','VESA','Display','RearFrame','Door','Glass'],exclude=['MeshReserve'])
standard('M','Complete display removed through the front','monitor-removal','Remove top bar and backbox glass, then the replaceable bezel.\n\nReturn carrier to the nominal service alignment; support the display and remove its four rear-accessible carrier clamps.\n\nDisplay + replaceable plate withdraw 400 mm forward. Fixed side channels remain in place.\n\nNo monitor passage through the rear aperture is required.',include=['Side','Top','Floor','Monitor','VESA','Display','Glass'],rear=False)
fig,ax=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1.7,1]});projection(ax[0],E['sections']['glass_edge_z1000'],(0,1),((-92,-58),(1106,1134)));note(ax[1],'Actual CAD section at Z1000\n\n4 mm glass envelope\n8 mm groove / 2 mm liner reserves\n6 mm side rebate; 12 mm outer skin remains\n4 mm nominal glass edge capture\n\nThe channel ends at the original inner side plane, leaving the 744 mm monitor throat unobstructed.\nGlass supplier sets final clearances, liner and edge treatment.');finish(fig,'N','Recessed backglass side channels','rear-closed')
standard('O','Top retainer removed — glass lift-out','glass-removal','Two positive retainer fasteners, a padded lower channel and replaceable side liners.\n\nNominal 3–4 mm tempered glass.\n500 mm upward service travel clears the backbox top; allow this overhead space.\n\nBackbox front glass stays captured during normal folding. The playfield glass is the separate fold prerequisite.',include=['Side','Top','Backglass','Glass','Display'],rear=False)
standard('P','Independent DMD and speaker cassette','rear-closed','One removable lower assembly\nLeft baffle + DMD adapter + right baffle\n\nDMD envelope: 400 × 170 × 45 mm\nSpeakers: 130 × 130 mm; 85 mm behind frame / 103 mm behind baffle\n\nNo speaker diameter or device-specific pattern in permanent backbox wood. A larger 15.6-inch DMD chassis is not automatically supported by this stack.',include=['LowerCassette','Baffle','DMD','Speaker','Cassette'],rear=False)
standard('Q','Exploded lower-front cassette','cassette-exploded','Replaceable baffles and bezel sit on a common plywood frame. Rear adapter and simple depth ties retain the DMD.\n\nFour positive cassette attachments; front withdrawal for complete replacement.\n\nImportant review limitation: this cassette must be withdrawn to reach the original upright-lock tool columns. Reinstall and secure it before folding.',include=['LowerCassette','Baffle','DMD','Speaker','Cassette'],rear=False,explode=True)
standard('R','Reserved side toy space with maximum display','toy-zones','Upper zones, each:\n96 mm inward × 39 mm deep × 326 mm high\n\nLower zones, each:\n48 × 24 × 114 mm\n\nThese are free mounting volumes, not guarantees for every chime or toy. Shallower displays can release more depth. Use removable boards; no permanent toy-specific holes.',include=['Side','Top','Floor','Monitor','VESA','Display','ToyZone','Speaker','DMD'],rear=True)
standard('R2','Future side-toy scenario — 55 mm display','thin-display-toys','Conditional upgrade scenario\nSame 740 × 450 face envelope, 55 mm chassis depth.\n\nA central 45 mm removable-adapter reserve stays inside the validated 100 mm display envelope.\n\nEach upper side zone grows to 96 mm inward × 84 mm deep × 326 mm high, allowing useful side-mounted toy planning. No particular chime, mount or fastener is qualified.',include=['Side','Top','Floor','Monitor','VESA','Display','ToyZone','ShallowAdapter'],rear=True)
standard('S','Optional toy shelf — rejected at this location','optional-shelf','The 490 × 65 × 12 mm trial shelf intersects the populated DMD and lower monitor rail.\n\nIt also occupies the low-to-high air and service route.\n\nNOT INSTALLED. No mandatory shelf and no new side-wall supports. Future accessories require their own loaded fit and fold review.',include=['Side','Floor','MonitorRail0','Display','DMD','OptionalToyShelf'],rear=True,diagnostic=True)
standard('T','Complete mechanical backbox exploded','mechanical-exploded','Fixed shell and rear perimeter frame\nTwo rear leaves + optional fan stations\nPlywood monitor carrier / replaceable plate\nBackbox glass / removable top bar\nIndependent lower cassette\n\nExploded positions communicate assembly groups; they are not certified removal trajectories.\n\nDesign review only. Upright-lock service tradeoff blocks promotion.',rear=False,explode=True,exclude=['MeshReserve'])
for key,a in [('U',1),('V',15),('W',45),('X',90)]:
    standard(key,f'Complete populated backbox — {a}° fold',f'fold-{a}','WPC transverse axis: Y1066.8 / Z508\n210 mm sides and Y1146 floor retained.\n\nPLAYFIELD GLASS REMOVED\nMATRIX REMOVED\nRear leaves latched; all carriers secured.\nBackbox front glass remains installed.\n\nReference hardware only; no purchased hinge drilling release.',full=True,exclude=['MeshReserve','CamTongueRetracted','PassiveBoltRetracted'])
standard('Y','Complete upright V32 — service design candidate','complete-upright','Main cabinet, playfield mechanism, shelves, PC base and matrix geometry remain unchanged.\n\nThis populated backbox is a separate review candidate. CURRENT V32 and its offline viewer remain on the last promoted combined geometry.\n\nPlanning backbox mass: about 34.6 kg before optional toys. Strength and hardware qualification remain open.',full=True,exclude=['MeshReserve'])
fig,ax=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1.8,1]});items=select(include=['Floor','LowerCassette','DMD','Speaker','Cassette'])+E['lock_hinge_access'];projection(ax[0],items,(1,2),((1120,1305),(590,825)),.32);note(ax[1],'Original lock and floor-hinge tool columns are obstructed with the cassette installed.\n\nFront cassette withdrawal restores the original columns; no lock or hinge datum is moved.\n\nThis is an explicit service burden, not an approved redesign of the locking system.\n\nCandidate remains NOT PROMOTED pending the owner’s decision on this workflow or a scoped lock-access solution.');finish(fig,'Z','Promotion blocker — upright-lock access','rear-closed')
(O/'review-images.json').write_text(json.dumps({'images':files,'source':'actual OpenCascade B-rep tessellation and cut sections','upstream_assets_included':False,'manufacturing_ready':False},indent=2)+'\n')
print('BACKBOX_SERVICE_IMAGES_PASS',len(files))

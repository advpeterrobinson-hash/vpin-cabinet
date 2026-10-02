"""Twenty-three views from actual OCC CAD. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection,LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
R=Path(__file__).resolve().parents[2];O=R/'exports/generated/backbox-lock-integration-v32'
d=json.loads(gzip.decompress((O/'review-mesh.json.gz').read_bytes()));bank=d['meshes'];S={n:[bank[k] for k in keys] for n,keys in d['scenes'].items()};Q=json.loads((O/'validation.json').read_text());search=json.loads((O/'search.json').read_text());assert all(x['pass'] for x in Q['checks'])
plt.rcParams.update({'font.size':10,'figure.facecolor':'#f8fafc','axes.facecolor':'#f8fafc','font.family':'DejaVu Sans'});images=[];cache={}
def style(n):
    if any(k in n for k in ['Entry','Lower','Lift','Transfer','Palm','Finger']):return '#995bb5',.18
    if 'Old' in n:return '#c24c44',.55
    if 'WoodReserve' in n:return '#35a27b',.3
    if 'Lock' in n:return ('#bb7953' if 'ParkingPad' in n else '#367e94'),.9
    if 'Hinge' in n or 'BoreReference' in n:return '#9064ae',.32
    if 'Display32' in n or 'DMDEnvelope' in n:return '#407b9e',.4
    if 'SpeakerEnvelope' in n:return '#526479',.45
    if 'Backglass' in n:return '#63b4c5',.18
    if 'Side' in n or n=='BB_Top':return '#8996a0',.18
    if 'Fan' in n:return '#a96452',.85
    if 'Intake' in n:return '#98a78d',.75
    if 'Door' in n:return '#c0a783',.75
    return '#c2ad8c',.65

def edges(m):
    key=id(m)
    if key in cache:return cache[key]
    v=np.asarray(m['vertices']);adj={}
    for tri in m['faces']:
        a,b,c=v[tri];n=np.cross(b-a,c-a);norm=np.linalg.norm(n)
        if norm<1e-10:continue
        n/=norm
        for ia,ib in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])]:adj.setdefault(tuple(sorted((tuple(v[ia].round(5)),tuple(v[ib].round(5))))),[]).append(n)
    es=np.array([k for k,ns in adj.items() if len(ns)==1 or any(abs(np.dot(ns[0],n))<.995 for n in ns[1:])]);cache[key]=es;return es

def items(state,inc=None,exc=()):return [m for m in S[state] if (inc is None or any(k in m['name'] for k in inc)) and not any(k in m['name'] for k in exc)]
def draw(ax,mm,close=None,front=False,full=False):
    for m in mm:
        c,a=style(m['name']);v=np.array(m['vertices']);f=np.array(m['faces'])
        if full and not m['name'].startswith(('BB_','UprightLock')):a=.12
        ax.add_collection3d(Poly3DCollection(v[f],facecolor=c,edgecolor='none',alpha=a));es=edges(m)
        if len(es):ax.add_collection3d(Line3DCollection(es,colors='#42515c',linewidths=.5,alpha=min(.7,a+.15)))
    if full:lim=[(-100,700),(-50,1380),(0,1360)]
    elif close:lim=close
    else:lim=[(-130,730),(1030,1740),(570,1345)]
    ax.set(xlim=lim[0],ylim=lim[1],zlim=lim[2],xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm');ax.set_box_aspect([b-a for a,b in lim]);ax.view_init(24,-62 if front or full else 63);ax.tick_params(labelsize=8)
def note(ax,s):
    ax.axis('off');text='\n'.join('\n'.join(textwrap.wrap(line,44,break_long_words=False)) for line in s.split('\n'));ax.text(.02,.97,text,va='top',fontsize=10.5,linespacing=1.4)
def finish(fig,key,title,cad):
    fig.suptitle(key+'  '+title,x=.035,ha='left',fontsize=15,fontweight='bold');fig.text(.035,.027,'ACTUAL CAD • design candidate • reference lock hardware / bores provisional • manufacturing BLOCKED • CERN-OHL-S-2.0',fontsize=8.5,color='#87523e');fig.subplots_adjust(left=.07,right=.975,top=.88,bottom=.12,wspace=.16);fn=key+'-review.png';fig.savefig(O/fn,dpi=145);plt.close(fig);images.append({'id':key,'title':title,'file':fn,'cad':cad+'.FCStd'})
def standard(key,title,state,text,inc=None,exc=(),close=None,front=False,full=False):
    fig=plt.figure(figsize=(14,8));gs=fig.add_gridspec(1,2,width_ratios=[2.2,1]);draw(fig.add_subplot(gs[0],projection='3d'),items(state,inc,exc),close,front,full);note(fig.add_subplot(gs[1]),text);finish(fig,key,title,state)
def projection(ax,mm,dim,limits):
    for m in mm:
        v=np.array(m['vertices']);c,a=style(m['name']);ax.add_collection(PolyCollection(v[np.array(m['faces'])][:,:,dim],facecolors=c,edgecolors='none',alpha=min(a,.4)));es=edges(m)
        if len(es):ax.add_collection(LineCollection(es[:,:,dim],colors='#445462',linewidths=.6))
    ax.set(xlim=limits[0],ylim=limits[1],xlabel='XYZ'[dim[0]]+' / mm',ylabel='XYZ'[dim[1]]+' / mm');ax.set_aspect('equal');ax.grid(alpha=.15)
low=[(-95,695),(1125,1355),(568,825)];left=[(60,225),(1215,1325),(570,810)];right=[(375,540),(1215,1325),(570,810)]
standard('01','Historical lock / cassette obstruction','option-a','Old centers X120 / X480, Y1188.\nOnly 21.1 mm between floor top and DMD underside.\n\nThe original tall tool reserve and tested knob/wing/socket operation occupy the DMD envelope. This is the superseded interface.',inc=['Floor','LowerCassette','DMD','Speaker','OldLock'],close=low,front=True)
fig,ax=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[2.2,1]});projection(ax[0],items('search-map',inc=['Floor','BACKBOX_BASE']),(0,1),((0,600),(1125,1305)))
colors={'wood':'#e0c7b5','hinge':'#946a99','head_or_release':'#c87d69','hand_approach':'#d8b775','PASS':'#168969'}
for result,c in colors.items():
    rr=[r for r in search['rows'] if r['result']==result];xx=[r['x'] for r in rr];yy=[r['y'] for r in rr];ax[0].scatter(xx+[600-x for x in xx],yy+yy,c=c,s=9,marker='s',label=result)
ax[0].scatter([130,470],[1260,1260],marker='*',s=150,c='#243d82',label='selected');ax[0].legend(loc='lower left',fontsize=8)
note(ax[1],'Exact B-rep screen on a 4 mm grid.\n1,536 half-floor centers; mirror at X300.\n\n17 clear sampled centers per side. Useful strip near X126–146, Y1256–1264, mirrored on the right.\n\nSelected X130 / X470, Y1260 are independently checked, not interpolated from the grid. Green dots are candidate centers, not released machining zones.');finish(fig,'02','Lock-access search map','search-map')
standard('03','Option A — compact access still conflicts','option-a-compact','Tested head families:\nØ40 hand knob\nØ44 wing-head rotation\nØ20 compact socket corridor\n\nEven an 8 mm-high compact head needs axial release travel into the DMD underside with the studied shelf thread. No DMD cutout is permitted.\n\nA rejected; no claim that every exotic low-profile mechanism is impossible.',close=low,front=True)
standard('04','Option B — symmetric relocated pair','lower-open','Selected centers:\nL (130, 1260)\nR (470, 1260)\n\nHAND operated Ø40 knob reserve; M8 × 40 stud family. Metal-backed captive shelf threads.\n\nLoss-protection tethers retain knobs and washers. After release, screw each knob into its parking socket before folding.',inc=['Floor','RearFrame','UprightLock','LowerCassette','DMD','Speaker'],close=low)
for key,side,lim in [('05','L',left),('06','R',right)]:standard(key,'Selected lock '+side+' — engaged and captive','lock-close-'+side,'Two independent positive threaded clamps.\nFloor bears directly on rear shelf.\n\nØ32 captive load-spreading washer reserve. 26 mm-radius wood land.\n\nTwo simple 18 mm plywood pads make the separate threaded parking block. Parking carries only the released knob.\nPurchased thread, washer retention and torque remain provisional.',inc=['Floor','BACKBOX_BASE','UprightLock'+side],close=lim)
# Both access paths use the same CAD scene assembled explicitly for review.
combined=S['access-L']+[m for m in S['access-R'] if m['name'].startswith('BB_UprightLockR') and any(k in m['name'] for k in ['Entry','Lower','Lift','Transfer'])];S['both-access']=combined
standard('07','Open rear — both hand paths, lower section','both-access-section','Palm reserve: 90 × 50 × 45 mm.\nTwo bent-finger corridors reach the knob sides.\n\nEnter above the rear sill, lower to the knob, unscrew and lift, then transfer to the parking socket. Reverse to engage.\n\n4 mm minimum modeled hand clearance; physical hand/glove trial remains required.',exc=['FanMeshReserve'],close=[(-80,680),(1170,1630),(590,850)])
images[-1]['cad']='both-access-section.FCStd'
for key,side,lim in [('08','L',left),('09','R',right)]:standard(key,'Hand corridor '+side+' — approach, release and stow','hand-close-'+side,'Purple volumes are conservative swept palm/finger envelopes.\n\nNo DMD, speaker, cassette, display or backglass removal. No electrical disconnection introduced.\n\n80 mm lift clears the parking blocks before lateral transfer. The knobs stay attached to mechanical loss-protection tethers.',inc=['UprightLock'+side,'Floor','DMD','LowerCassette','RearFrame'],close=[lim[0],(1215,1535),(590,805)])
standard('10','Floor wood reserve','wood-reserves','26 mm-radius continuous wood land around each upright lock.\nØ9 floor bore is a provisional reference.\n\nFloor front Y1146 retained. Generic service passage unchanged.\n\nParking holes are 3 mm blind reliefs, leaving 15 mm floor stock; they do not pierce the bearing underside.',inc=['Floor','LockWood','WoodReserve','BoreReference'],close=low)
fig,ax=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1.7,1]});projection(ax[0],items('lock-section'),(1,2),((1230,1292),(570,660)));note(ax[1],'Actual section at X130.\n\n18 mm floor + 18 mm shelf.\nMetal-backed captive shelf thread with nominal 12 mm barrel.\nØ32 underside backing reserve.\n\nNo repeated thread operation directly in wood. Bore, anti-rotation/retention, edge distances, material and torque need physical qualification.');finish(fig,'11','Shelf / captive-thread section','lock-section')
standard('12','Generic cable passage remains clear','wood-reserves','Generic 260 × 60 passage retained.\nNo connector or disconnect system designed.\n\nSelected 26 mm-radius lock wood lands are 15.76 mm clear of the passage.\n\nParking blocks stay behind the opening; they do not form a cable panel.',inc=['Floor','BACKBOX_BASE','WoodReserve'],close=low)
standard('13','Locks separated from hinge-service reserves','wood-reserves','Minimum lock wood-land separation from hinge hardware/tool reserve: 104 mm.\n\nRoutine locks: rear hand access.\nRare WPC hinge floor service: cassette withdrawal may still be required. Side pivot service retains playfield lift-out prerequisites.\n\nNo final WPC hinge drilling released.',close=[(-100,700),(1030,1320),(475,750)])
standard('14','Cassette remains installed for locking','doors-open','Four positive cassette attachments unchanged.\nDMD adapter, speaker baffles and occupied volumes unchanged.\n\nReach the two locks from the open rear doors. The lower cassette is no longer a routine fold prerequisite.',inc=['LowerCassette','Cassette','DMD','Speaker','Floor','UprightLock'],close=low)
standard('15','DMD and speakers installed — locks accessible','doors-open','DMD: 400 × 170 × 45 occupied envelope.\nSpeaker bodies: existing 130 × 130 envelope and depth retained.\n\nNo electronics envelope is cut or reduced to create lock access. Complete cassette and individual speaker service remain clear.',inc=['DMD','Speaker','UprightLock','Floor'],close=low,front=True)
standard('16','Both doors fully open — lock operation','doors-open','Both leaves reach 100°.\nActive right opens before passive left.\n\nRelease both upright clamps and positively park each captive knob. Keep the cassette and glass installed.\n\nRear-door cam lock is distinct from these two structural upright locks.',exc=['FanMeshReserve'])
standard('17','Doors latched — upright locks engaged','locks-engaged','Upright: both floor clamps tightened and seated.\nRear leaves secured in passive/active order.\n\nBroad bearing footprint retained. Reference bores reduce net bearing by 226.2 mm² to 65,446.2 mm² (99.66% retained).\n\nFastener strength and plywood bearing require manufacturing qualification.',exc=['FanMeshReserve'])
for key,a in [('18',1),('19',45),('20',90)]:standard(key,f'Populated fold {a}° — locks parked',f'fold-{a}','LOCKS RELEASED AND PARKED\nREAR DOORS LATCHED\nPLAYFIELD GLASS + MATRIX REMOVED\n\nBackbox front glass retained.\nCassette, DMD, speakers and display retained and secured.\n\nWPC Y1066.8 / Z508; 210 mm lower sides; Y1146 floor.',full=True)
standard('21','Complete final backbox — front','locks-engaged','32-inch primary display, front installation and rear adjustment.\nTop-removable retained backglass.\nIndependent DMD / speaker cassette.\n\nThe locking solution preserves the accepted service architecture.',exc=['FanMeshReserve'],front=True)
standard('22','Complete final backbox — rear','locks-engaged','Twin 12 mm rear leaves; no permanent center mullion.\nOptional fan / blank stations, low filtered intakes and flexible low-voltage door loops retained.\n\nNo mandatory toy shelf. Side toy zones and generic cable passage preserved.',exc=['FanMeshReserve'])
standard('23','Complete final backbox — exploded','backbox-exploded','Exploded positions identify assembly groups, not a certified simultaneous removal path.\n\nNew scope: two upright threaded clamps, metal shelf receivers, captive retention and two simple plywood parking blocks.\n\nZero custom metal. Manufacturing remains blocked.',exc=['FanMeshReserve'],close=[(-140,740),(750,1580),(570,1490)],front=True)
(O/'review-images.json').write_text(json.dumps({'images':images,'source':'actual OCC B-reps / exact sections','manufacturing_ready':False},indent=2)+'\n');print('BACKBOX_LOCK_IMAGES_PASS',len(images))

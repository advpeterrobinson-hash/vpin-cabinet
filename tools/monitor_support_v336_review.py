"""V33.6 review scenes from exact native B-reps. CERN-OHL-S-2.0.
No scene grants CNC release. Held adapter window is never shown as current.
"""
from pathlib import Path
import gzip,json,sys,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,V
O=R/'exports/generated/monitor-support-v336';old=load(R/'exports/generated/structural-v335/play.FCStd');new=load(O/'play.FCStd');st=load(O/'study.FCStd');bs=load(O/'backbox-study/study.FCStd');door=load(R/'exports/generated/structural-v335/doors-open.FCStd');door.update({n:s for n,s in new.items() if n.startswith('BB_MonitorCarrier')})
C=json.loads((R/'config/monitor_support_v336.json').read_text());a=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review']['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(a))-12-55*math.cos(math.radians(a))
scenes=[];cache={}
def inv(s):q=s.copy();q.translate(V(0,-45,-bz));q.rotate(V(),V(1,0,0),-a);return q
def sub(d,names):return {n:d[n] for n in names if n in d}
def select(d,*starts):return {n:s for n,s in d.items() if n.startswith(starts)}
def slice(s,axis,low,high):
 b=s.BoundBox;pos=[b.XMin-1,b.YMin-1,b.ZMin-1];size=[b.XLength+2,b.YLength+2,b.ZLength+2];pos[axis]=low;size[axis]=high-low;return s.common(Part.makeBox(*size,V(*pos)))
def col(n):
 if 'HELD' in n or 'Held_' in n:return '#bb6352'
 if 'Cable' in n or 'Connector' in n:return '#15717e'
 if n.startswith(('LeafButton','LeafNut')):return '#984524'
 if n.startswith(('Leaf','ButtonAccess','Button')):return '#446e80'
 if 'VESA' in n or 'Clamp' in n:return '#6a879c'
 if 'Stop' in n:return '#b27b28'
 if 'Slot' in n or 'Thread' in n:return '#267568'
 if 'Display' in n or n in ['TV_ENVELOPE','PLAYFIELD_ENVELOPE']:return '#354858'
 if 'Glass' in n:return '#a9c0c9'
 if 'Screw' in n or 'Bolt' in n:return '#555b61'
 return '#c8ae8c'
def panel(label,parts,view=(1,-2,1.5),colors=None,alpha=None,limits=None,annotations=None,edges=None):
 meshes=[]
 for n,s in parts.items():
  if s.isNull():continue
  mm=MeshPart.meshFromShape(Shape=s,LinearDeflection=.45,AngularDeflection=.5,Relative=False);vv,ff=mm.Topology;meshes.append({'name':n,'vertices':[list(p) for p in vv],'faces':ff,'color':(colors or {}).get(n,col(n)),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':meshes,'view':view,'limits':limits,'annotations':annotations or [],'edges':edges or []}
def line_wire(s,y=None):
 # True native edges, projected by renderer; no traced/invented silhouette.
 out=[]
 for e in s.Edges:
  pts=e.discretize(Deflection=.12)
  if len(pts)>1:out.append([list(p) for p in pts])
 return out
def add(id,title,panels,note,legend=None):scenes.append({'id':id,'title':title,'panels':panels,'note':note,'legend':legend or []})
def lp(d):return {n:inv(s) for n,s in d.items()}
def buttonset(d):return {n:s for n,s in d.items() if n.startswith(('Leaf','Button')) and n.endswith('_L')}
localold=inv(old['PF_BasePlywood']);localnew=inv(new['PF_BasePlywood'])
add('01','V33.5 horn / finger — confirmed baseline',[panel('Front-left M025 / P034-Main detail',{'M025':localold},(0,0,1),limits=[35,145,0,180],edges=[{'lines':line_wire(localold),'color':'#50362a','width':1.8}])],'Actual old outer contour. The rounded notch leaves a thin local lip at the front edge; V33.5 protected and inherited it. Local playfield coordinates shown.')
add('02','M025 — recovered clean outer contour',[panel('New one-piece 18 mm base',{'M025':localnew},(0,0,1),edges=[{'lines':line_wire(localnew),'color':'#50362a','width':.9}])],'500 × 1020 mm clean exterior recovered from the wooden-dowel study. Functional rear window and two strain slots are the only new openings; no horn, finger or button notch remains.')
add('03','M025 contour overlay — before / after',[panel('Front-left detail · same datum',{'NewBase':localnew},(0,0,1),colors={'NewBase':'#eee6da'},limits=[35,145,0,180],edges=[{'lines':line_wire(localold),'color':'#b44428','width':2,'style':'--'},{'lines':line_wire(localnew),'color':'#213e49','width':1.3}])],'The restored lower buttons remove the old notch requirement. Dashed orange is the exact V33.5 contour; solid dark is CURRENT V33.6. Internal service openings lie farther rearward.',['Orange dashed: superseded','Dark solid: V33.6'])
for id,d,label,centers in [('04',old,'Superseded Y89 / Y127',[(89,350.5937),(127,357.2303)]),('05',new,'Restored Y255 / Y310, Z270',[(255,270),(310,270)])]:
 ann=[{'point':[0,y,z],'text':f'Y{y:g} / Z{z:g}','offset':[18,35+30*i]} for i,(y,z) in enumerate(centers)]
 add(id,'Side-button positional authority — '+label,[panel('Left exterior · cabinet front at right',{'SIDE_L':d['SIDE_L'],**buttonset(d)},(-1,0,0),annotations=ann)],'Button bodies are dark for legibility. Bore and recess geometry are reference placeholders, not purchased-hardware authority. The two position systems are not equivalent.')
baseparts=['SIDE_L','FRONT','FLOOR','BACKBOX_BASE','BB_SideL','BB_SideR','BB_Top','BB_Floor','BB_Display32','BB_LowerCassetteFrame']
add('06','Exterior comparison — owner restoration',[panel('BEFORE · V33.5',sub(old,baseparts)|buttonset(old),(-1,-1.8,.75)),panel('AFTER · V33.6',sub(new,baseparts)|buttonset(new),(-1,-1.8,.75))],'Same player-eye view. Only side-button positional authority and accepted support machining change. New positions are measured from cabinet front Y0, with 55 mm pitch and common Z270.')
parts=['FRONT','CROSS_1','CROSS_GUIDE_1L','SHELF_1','LEG_FRONT_L','PLUNGER_RESERVED']
add('07','Interior comparison — leaf button service',[panel('BEFORE · near upper front',{'SideCutaway':slice(old['SIDE_L'],1,0,440),'BaseCutaway':slice(old['PF_BasePlywood'],1,0,440),**buttonset(old)},(1,-.3,.12)),panel('AFTER · full leaf / tool reserves',{'SideCutaway':slice(new['SIDE_L'],1,0,440),'BaseCutaway':slice(new['PF_BasePlywood'],1,0,440),**buttonset(new)},(1,-.3,.12))],'True side/base sections for inspection only. Blue solids are traditional leaf-button body, wire and tool planning reserves. These move with the restored center datum; physical button selection remains HOLD.')
add('08','Restored buttons + clean playfield base',[panel('Front corner cutaway',{'Front':new['FRONT'],'M025':new['PF_BasePlywood'],**buttonset(new)},(-1,-2,1.3))],'Side panel omitted to expose the relationship. Lower button hardware clears the unnotched base. Dowel, straps, TV, VESA and both cradles retain their accepted positions.')
pflocal=lp(sub(new,['PF_BasePlywood','PF_WoodDowel','PF_VESAEnvelope'])|select(new,'PF_CommercialStrap','PF_StrapScrew'))
add('09','Playfield connector access + strain relief',[panel('Rear base underside',pflocal,(0,0,-1),annotations=[{'point':[300,785,-14],'text':'180 × 110 · R8 service window','offset':[50,20]},{'point':[300,877,-14],'text':'paired 6 × 22 · R3 strain slots','offset':[50,40]}])],'One connector-sized service window, two strap slots. Existing base edge bands remain continuous. Actual display port positions and selected cable bending requirements must be checked before adapter manufacture.')
add('10','Playfield VESA load region preserved',[panel('Local base plan',pflocal,(0,0,1),alpha={'PF_VESAEnvelope':.75},annotations=[{'point':[300,605,4],'text':'Entire existing VESA reserve kept','offset':[55,0]},{'point':[210,785,4],'text':'160 mm side bands','offset':[-120,0]}])],'Main window stays 120 mm from the modeled VESA region; minimum transverse wood width is 320 mm. No extra VESA slots are inferred from an unselected display. Load/stiffness qualification remains open.')
pf={n:s for n,s in actual(new).items() if n in pf_names(new)};context=sub(new,['SIDE_L','FLOOR','FRONT','SHELF_1','SHELF_2','SHELF_3','PF_OpenCradleL','PF_OpenCradleR'])
cables={}
for state in ['PLAY','SERVICE50','LIFT48']:
 p=O/'brep'/('CableLoop_'+state+'.brep')
 if not p.exists():raise RuntimeError('Cable study must complete before review scenes: '+str(p))
 q=Part.Shape();q.read(str(p));cables[state]=q
p50=transform(pf,angle=-50,axis=PF);lift={}
for n,s in pf.items():q=s.copy();q.translate(V(0,0,48));lift[n]=q
add('11','Playfield service 50°',[panel('Service pose · main glass / matrix removed',context|p50|{'FlexibleCableLoop':cables['SERVICE50']},(1,-2,1.25),alpha={'PLAYFIELD_ENVELOPE':.12})],'Native playfield transform around the unchanged wooden-dowel axis. Cable is a flexible constant-length planning tube, not a rigid linkage or selected harness; see sampled cable study for limits.')
add('12','48 mm lift-out — cable allowance',[panel('Lifted base / cradle underside · display envelope hidden',sub(new,['PF_OpenCradleL','PF_OpenCradleR','SHELF_3'])|{n:s for n,s in lift.items() if n!='PLAYFIELD_ENVELOPE'}|{'FlexibleCableLoop':cables['LIFT48']},(1,-1,-1))],'Complete playfield moves vertically 48 mm; display hidden only for inspection. Flexible loop: 63 sampled service/lift poses, not continuous certification. Cable/clamp hardware stays HOLD; release the S3 clamp before shelf removal.')
bbnames=['BB_MonitorCarrier0','BB_MonitorCarrier1','BB_ReplaceableVESAPlate','BB_MonitorStopRail','BB_StopAdjuster0','BB_StopAdjuster1','BB_StopInsert0','BB_StopInsert1','BB_StopLocknut0','BB_StopLocknut1']
add('13','V33.5 backbox carrier — exact baseline',[panel('Rear view of accepted support',sub(old,bbnames),(1,2,.4))],'Actual carrier Y1240–1258 and VESA plate Y1228–1240. Legacy service config is 10 mm forward of these accepted B-reps; no existing part is relocated by this task.')
held=Part.Shape();held.read(str(O/'backbox-study/brep/HELD_AdapterServiceWindow.brep'))
add('14','Backbox proposal — selected slots / held window',[panel('SELECTED · carrier strain relief',sub(new,bbnames),(0,1,0),annotations=[{'point':[160,1258,1198],'text':'2 slots per carrier','offset':[15,25]}]),panel('HOLD · adapter window NOT PROMOTED',{'HELD_AdapterWindow':held},(0,1,0))],'Only carrier slots join CURRENT geometry. Central 180 × 70 R12 window improves access but actual VESA load points are unknown; the uncut replaceable VESA plate remains current.',['Tan: selected carrier geometry','Rust: isolated HOLD'])
refnames=['ExistingSideConnectorRouteL','ExistingSideConnectorRouteR','FlexibleCableRouteL','FlexibleCableRouteR','BB_MonitorCarrier0_StrapThread','BB_MonitorCarrier1_StrapThread']
add('15','Backbox cable routing — existing side passages',[panel('Rear service routes',sub(new,bbnames)|sub(bs,refnames),(1,2,.35),alpha={'ExistingSideConnectorRouteL':.3,'ExistingSideConnectorRouteR':.3})],'50 × 30 mm generic connector cross-section with rear withdrawal; not a particular SKU. Illustrated flexible 5 mm routes use R20 bends and retain 2.5 mm modeled clearance. No new central window is required for these side routes.')
add('16','Adjustment — existing range retained',[panel('Current carrier / plate',sub(new,bbnames),(0,1,0))],'Vertical ±5 mm; two depth positions 0 / 16 mm; max-width display centering ±1 mm, smaller display ±15 mm. Added travel: 0 mm. Four positive clamps and M067 lower adjusters remain unchanged. No duplicated slotting.')
p={n:slice(s,2,895,965) for n,s in sub(new,bbnames).items()};p={n:s for n,s in p.items() if not s.isNull()}
p.update(select(new,'BB_StopRailRetention','BB_StopTip'))
add('17','M067 and capture lands — protected',[panel('Rail / lower carrier close-up',p,(1,-2,1.2))],'330 × 18 × 18 mm M067, both 6 mm captures and two M6-family adjuster/insert zones remain exact. New strain slots are at Z1190–1206, far above this assembly. No final hardware bore is released.')
physical=actual(new);bb={n:s for n,s in physical.items() if n.startswith('BB_')}
add('18','Complete backbox — front',[panel('Backglass / lower cassette remain installed',bb,(.25,-2,.15),alpha={n:.18 for n in bb if 'Backglass' in n})],'Front display service, retained backbox glass and independent DMD/speaker cassette remain unchanged. M067 and four positive display clamps retain the screen through fold.')
dphys=actual(door);bbdoor={n:s for n,s in dphys.items() if n.startswith('BB_')}
add('19','Rear service — both doors open',[panel('Twin doors at accepted service position',bbdoor,(.25,2,.3))],'Rear hand access to carrier ties, adjustment and two upright locks remains available. Fans, hinges, doors, cassette and hardware service architecture are unchanged.')
add('20','CURRENT V33.6 — complete cabinet',[panel('Player-eye mechanical review',physical,(-1.4,-2,1.15),alpha={n:.12 for n in physical if n=='CandidateGlass' or 'Backglass' in n})],'Restored side-button positions, clean M025 and support access updates. SW01, captured shell, M006, shelf, M067, WPC axis, matrix and glass systems remain protected. CNC release remains blocked.')
scenes.append({'id':'21','title':'Geometry authority — regression source and correction','diagram':True,'panels':[],'note':'Source-flow diagram, not CAD geometry. V33.6 corrects the canonical B-reps, then regenerates manufacturing pieces, native states, viewer meshes and animation geometry. Reference bores remain hardware-dependent.'})
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
print('V336_REVIEW_SCENES_PASS',len(scenes),flush=True)

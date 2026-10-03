"""Native review views12–20, isolated optional modules. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,sys,hashlib,math
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,PF,V
C=json.loads((R/'config/service_modularity_v338.json').read_text());O=R/C['output'];valid=json.loads((O/'modularity-validation.json').read_text());assert valid['pass'];ss=load(R/valid['source']);study=load(O/'modularity-study.FCStd');scenes=[]
def color(n):
 if n.startswith('Power'):return '#a3784e'
 if n.startswith('Signal'):return '#427888'
 if 'Harness' in n or 'Passage' in n or 'Anchor' in n:return '#5b9694'
 if 'Clamp' in n:return '#566570'
 if 'Payload' in n:return '#71818c'
 if 'Accessory' in n:return '#cba66e'
 if n.startswith('CROSS'):return '#a69674'
 return '#c6b594'
def panel(label,shapes,view=(1,-2,1),alpha=None,annotations=None):
 mm=[]
 for n,s in shapes.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.7,AngularDeflection=.6,Relative=False);vv,ff=m.Topology
  if ff:mm.append({'name':n,'vertices':[list(v) for v in vv],'faces':ff,'color':color(n),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':mm,'view':view,'annotations':annotations or []}
def ann(point,text,offset=(20,20)):return {'point':point,'text':text,'offset':offset}
def add(i,title,panels,note):scenes.append({'id':f'{i:02d}','title':title,'panels':panels,'note':note})
def sub(d,names):return {n:d[n] for n in names if n in d}
def pref(d,*ps):return {n:s for n,s in d.items() if n.startswith(ps)}
def clip(s,x,y,z,w,d,h):return s.common(Part.makeBox(w,d,h,V(x,y,z)))
hard=pref(ss,'SHELF_','SHELF_SUPPORT','CROSS_');hard={n:s for n,s in hard.items() if 'Payload' not in n}
add(12,'Existing S1/S2/S3 and T1/T2/T3 remain the hardpoints',[panel('Open architecture — no added wall holes',hard,(1,-2,1),annotations=[ann([300,640,195],'S2'),ann([300,940,255],'S3'),ann([300,195,175],'S1'),ann([300,380,350],'T1 — not a PF landing'),ann([300,700,405],'T2'),ann([300,980,455],'T3')])],'No permanent stations, large internal panels or universal hole grid are added. Small modules use existing removable shelves. T1/T2/T3 retain their original role and intentional playfield clearance.')
opt=pref(study,'Accessory');sample=pref(study,'AccessoryBoardS2Right');base=sub(ss,['SHELF_2','SimpleShelfBolt2R1','SimpleShelfBolt2R2','SimpleShelfBolt2R1Washer','SimpleShelfBolt2R2Washer'])
add(13,'ACC01 optional 100 ×120 ×12 mm board',[panel('S2 rear-edge clamping; gravity borne on shelf',base|sample,(1,-2,1),alpha={'SHELF_2':.4},annotations=[ann([480,650,205],'ACC01 ·12 mm\nOptional, not minimum BOM',(25,30)),ann([450,730,185],'Commodity clamp reserve\nPurchased fit / vibration HOLD',(-150,-35))]),panel('Same family on S3 left',sub(ss,['SHELF_3'])|pref(study,'AccessoryBoardS3Left'),(1,-2,1),alpha={'SHELF_3':.4})],'One small board family, two optional sample locations. No electronics holes are permanent. Two screw C-clamps per chosen board are original provisional envelopes, not selected vendor geometry or qualified impact-toy anchors. Remove modules/clamps before independent shelf extraction.')
board=study['AccessoryBoardS3Left'];b=board.BoundBox;local=board.copy();local.translate(V(-b.XMin,-b.YMin,-b.ZMin))
add(14,'Cable-management vocabulary — reuse current slots',[panel('ACC01 FACE A;6 ×22 R3 pair',{'AccessoryBoard':local},(0,0,1),annotations=[ann([43,99,12],'6 ×22 mm ·R3',(-140,30)),ann([77,99,12],'34 mm center pitch',(20,30))])],'Preferred hook-and-loop grammar reuses the M025 6 ×22 mm R3 pair. Existing protected exceptions remain: backbox carriers6 ×16 R3, underfront panel4 ×12 R2. No extra permanent slots or connector cutouts. Actual tie/strap width and edge protection require physical selection.')
interior={n:s for n,s in actual(ss).items() if not n.startswith(('PF_','BB_','Matrix','MX_','LeafButton','Button')) and n not in ['SIDE_L','SIDE_R','CandidateGlass','PLAYFIELD_ENVELOPE']}
add(15,'Low power and signal route zones',[panel('Left SIGNAL / right ELV POWER',interior|pref(study,'PowerRoute','SignalRoute'),(1,-2,1),alpha={'FLOOR':.35},annotations=[ann([90,720,100],'SIGNAL_ROUTE\nMechanical zone only',(-110,35)),ann([510,720,100],'POWER_ROUTE\nELV planning; mains separate',(25,35))])],'Two20 mm diameter low routing zones clear current occupied geometry by at least24.677 mm. Their centerlines are420 mm apart. Branches, clamps and final bundles are not pre-wired. Mains remains separately enclosed/protected and signal wiring must not pass through mains compartments.')
mov={n:ss[n] for n in json.loads((R/'exports/generated/front-landings-v3363/viewer-motion.json').read_text())['playfield_moving_names']}
add(16,'Moving playfield harness — current anchors and window',[panel('PLAY ·400 mm planning loop',sub(ss,['PF_BasePlywood','SHELF_3'])|pref(study,'MovingPFHarness_PLAY'),(1,-2,.6),alpha={'PF_BasePlywood':.3,'SHELF_3':.35},annotations=[ann([450,900,258],'Fixed removable S3 clamp',(-110,-40))]),panel('50° service geometric path only',transform(mov,angle=-50,axis=PF)|sub(ss,['SHELF_3'])|pref(study,'MovingPFHarness_SERVICE50'),(1,-2,.5),alpha={'PF_BasePlywood':.3})],'The existing8 mm packaging tube/400 mm loop passes63 sampled PLAY/service/lift configurations without disconnecting for the geometric50° motion. Clamp releases for S3 removal. This is not cable bend certification; primary raised-playfield support is unresolved, so the50° pose is not permission to work unsupported.')
passage=Part.makeBox(260,60,45,V(170,1188,575));anchors={'FixedAnchorZone':Part.makeBox(50,22,14,V(275,1249,560)),'MovingAnchorZone':Part.makeBox(24,20,24,V(288,1228,618))}
bb=sub(ss,['BB_Floor','BACKBOX_BASE','BB_MonitorCarrier0','BB_MonitorCarrier1','BB_ReplaceableVESAPlate','BB_MonitorStopRail','BB_RearFrame','BB_Display32'])
add(17,'Backbox harness zones — route remains HOLD',[panel('Existing passage and carrier strain-relief structure',bb|anchors|{'PassageZone':passage},(1,2,.6),alpha={n:.28 for n in bb if n in ['BB_Display32','BB_RearFrame','BB_ReplaceableVESAPlate']},annotations=[ann([300,1218,610],'Generic260 ×60 passage\nNo connector system',(-120,-35)),ann([160,1250,1180],'Existing carrier slots retained',(30,30))])],'Carrier slots, rear adjustment and side connector access remain. No central VESA window is cut. New universal fold-loop trials hit floor geometry or violate sensible bend curvature, so no backbox harness is validated or promoted. Cable selection and a supported continuous fold route remain explicit builder/hardware qualification holds.')
shell=sub(ss,['SIDE_L','FLOOR','FRONT','REAR','BACKBOX_BASE','SIDE_R']);expl={}
for n,s in shell.items():
 q=s.copy();q.translate(V(-90 if n=='SIDE_L' else 90 if n=='SIDE_R' else 0,0,0));expl[n]=q
add(18,'Dry-fit assembly — captured shell before closure',[panel('Documentary exploded positions, not insertion proof',expl,(1,-2,1),alpha={'SIDE_L':.45,'SIDE_R':.45},annotations=[ann([300,1000,40],'Floor / front / rear / shelf\nseat captures before SideR',(-140,25))])],'Shell shoulders provide positive datums: dry-fit, square check, then qualified adhesive/fixation. Shelf supports and cradle pilots match side references. Crossmember guides and backbox rail/hinge cleats still require qualified placement templates; no matching side-location feature is silently invented.')
add(19,'Interior without optional boards',[panel('Minimum cabinet remains open',interior|hard,(1,-2,1),alpha={'FLOOR':.4})],'Minimum geometry and BOM have no ACC01 boards or clamps. Shelf/support architecture, floor fans, PCBase, SSF, underfront module and structural members remain. No third plywood stock is introduced.')
add(20,'Interior with optional sample boards',[panel('Localized modules; open center preserved',interior|hard|opt,(1,-2,1),alpha={'FLOOR':.4},annotations=[ann([480,655,220],'Optional ACC01 on S2',(-130,25)),ann([110,925,275],'Optional ACC01 on S3',(25,30))])],'Samples preserve continuous PF0–50° clearance,48 mm lift, shelf fastener access and independent shelf routes after clamp/module removal. Neither board is a structural cabinet part. Payload, clamp dimensions and vibration/impact retention remain hardware-specific holds.')
(O/'modularity-review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0));(O/'modularity-review-sources.json').write_text(json.dumps({p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in [valid['source'],'config/service_modularity_v338.json',str((O/'modularity-study.FCStd').relative_to(R)),str((O/'modularity-validation.json').relative_to(R)),str((O/'modularity-dryfit-audit.json').relative_to(R))]},indent=2)+'\n');print('V338_MODULARITY_REVIEWS',len(scenes))

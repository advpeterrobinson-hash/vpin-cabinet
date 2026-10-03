"""24 review scenes from native V33.7 B-reps. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
All translations labelled exploded/layout are documentation only.
"""
from pathlib import Path
import gzip,json,sys,hashlib,math,re
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
from coin_door_v32 import definitions,turn
READS=set()
O=R/'exports/generated/two-stock-user-module-v337';old=load(R/'exports/generated/front-landings-v3363/play.FCStd');new=load(O/'play.FCStd');study=load(O/'module-study.FCStd');six=load(O/'modulevariants.FCStd');fallback=load(O/'module-fallback.FCStd')
C=json.loads((R/'config/underfront_user_module_v337.json').read_text());G=json.loads((O/'module-validation.json').read_text());conv=json.loads((O/'conversion-validation.json').read_text());search=json.loads((O/'module-location-search.json').read_text());reg=json.loads((O/'manufacturing-register.json').read_text());scenes=[]
assert G['pass'] and conv['pass']
assert json.loads((O/'geometry-validation.json').read_text())['native_sha256']==hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest()
def select(d,*starts):return {n:s for n,s in d.items() if n.startswith(starts)}
def sub(d,names):return {n:d[n] for n in names if n in d}
def clip(s,x0,x1,y0,y1,z0,z1):return s.common(Part.makeBox(x1-x0,y1-y0,z1-z0,V(x0,y0,z0)))
def shift(s,x=0,y=0,z=0):q=s.copy();q.translate(V(x,y,z));return q
def brep(p):
 READS.add(R/p);s=Part.Shape();s.read(str(R/p));return s
def colors(n):
 if 'Airway' in n:return '#438d9b'
 if 'Hand' in n or 'AccessButton' in n:return '#6d95a0'
 if 'BoreReference' in n or 'PocketReserve' in n:return '#995866'
 if 'Button' in n:return '#c96639'
 if 'USB' in n:return '#3b778a'
 if 'Loop' in n or 'WireReserve' in n:return '#8b879d'
 if 'Screw' in n or 'Insert' in n or 'Driver' in n or 'Bolt' in n:return '#6c7c89'
 if 'ContactPad' in n:return '#286861'
 if n.startswith('FrontLanding'):return '#a28659'
 if 'Before' in n:return '#beafa0'
 if 'Bezel' in n:return '#b39566'
 if 'Glass' in n or 'Backglass' in n:return '#91bdc3'
 if 'Display' in n:return '#314c5a'
 if 'Air' in n:return '#4c9aa1'
 if 'Side' in n or n.startswith('SIDE'):return '#c7b38b'
 if 'Underfront_Plate' in n:return '#d8ad67'
 if 'Leg' in n:return '#9b8265'
 return '#bda482'
def edges(s):return [[list(v) for v in e.discretize(Deflection=.4)] for e in s.Edges]
def panel(label,parts,view=(1,-2,1),alpha=None,annotations=None,lines=None,points=None):
 mm=[]
 for n,s in parts.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.45,AngularDeflection=.55,Relative=False);vv,ff=m.Topology
  if not ff:continue
  mm.append({'name':n,'vertices':[list(v) for v in vv],'faces':ff,'color':colors(n),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':mm,'view':view,'annotations':annotations or [],'edges':lines or [],'points':points or []}
def ann(p,t,offset=(20,20)):return {'point':p,'text':t,'offset':offset}
def clean(t):
 return re.sub(r'(?<=[a-z])(?=\d)|(?<=[,;×])(?=\S)',' ',t)
def add(i,title,pp,note,legend=None):
 for p in pp:
  p['label']=clean(p['label'])
  for a in p['annotations']:a['text']=clean(a['text'])
 scenes.append({'id':f'{i:02d}','title':clean(title),'panels':pp,'note':clean(note),'legend':legend or []})
module=select(new,'Underfront_');owner={n:s for n,s in module.items() if 'Reserve' not in n};shell=sub(new,['FRONT','SIDE_L','SIDE_R','FLOOR']);front={n:clip(s,-5,605,-30,330,-50,410) for n,s in shell.items()};frontold={n:clip(old[n],-5,605,-30,330,-50,410) for n in shell}
controls={n:s for n,s in module.items() if n.startswith('Underfront_Button') and 'Reserve' not in n};visible={n:s for n,s in owner.items() if n.endswith('_Face') or 'USB' in n or n=='Underfront_Plate'}
add(1,'Previous front / underside — historical intent',[panel('V33.6.3 front structure',frontold|sub(old,['CoinStudy_DoorLeaf','CoinStudy_CoinFrame']),(1,-2,-.65))],'The historical under-front controls were an unresolved service intent. This is the actual previous cabinet B-rep; no historical drilled centers are invented. Accepted side leaf-button centers and front structure remain protected.')
positions=[]
for layout in search['layouts']:
 if layout['count']==6 and layout['size'][0]<200:
  positions=layout['positions'];break
if not positions:positions=search['layouts'][0]['positions']
pts=[{'xyz':[p['center_xy_mm'][0],p['center_xy_mm'][1],16],'color':'#2a7d63' if p['pass'] else '#b46b59','size':4,'marker':'.'} for p in positions]
pts.append({'xyz':[300,110,15],'color':'#172f42','size':90,'marker':'x'})
add(2,'Placement search — actual cabinet constraints',[panel('Bottom view · selected center X300 / Y110',{'FLOOR':clip(new['FLOOR'],120,480,15,330,0,40)},(0,0,-1),alpha={'FLOOR':.25},points=pts,annotations=[ann([300,110,15],'Selected 160 ×116 plate\nX300 / Y110',(45,-60))])],'Computed candidate centers are overlaid on the native floor. Green dots pass the search screen; rust dots fail. Final exact B-rep, service, hand and tool tests govern the selected location. Points are search metadata, not new holes.')
common=sub(module,['Underfront_Plate']);gen=common|controls|six
add(3,'Generic six-button variant',[panel('Underside · 2 ×3 cells',gen,(0,0,-1)),panel('Rear body / switch / wire envelopes',gen|{n:s for n,s in module.items() if n.endswith('_WireReserve')},(1,-1,.6),alpha={'Underfront_Plate':.32})],'Six ordinary arcade microswitch buttons; 42 mm cell pitch and 4 mm minimum nominal nut-envelope gap. Ø28–30 mm hole class is reference only. Final purchased button bores are not cut into the blank CNC plate.')
add(4,'Owner configuration — five buttons + dual USB',[panel('Player underside',owner,(0,0,-1),annotations=[ann([342,131,0],'Dual USB seller reference\nPhysical measurement required',(35,-55))]),panel('Interior planning envelope',module,(1,-1,.7),alpha={n:.25 for n in module if 'Reserve' in n})],'Owner controls are removable user adapters. Button functions are configurable; there are no permanent function labels. USB seller dimensions conflict and are not machining authority. Default mechanical flatpack can use the same blank plate without electronics.')
add(5,'Fallback — four buttons + dual USB',[panel('Alternative adapter population',fallback,(0,0,-1))],'Fallback study remains available if the purchased USB connector or cap needs more space. It uses the same removable plate and permanent cabinet bay; it is not an extra mandatory flatpack part. Exact electrical interface remains user-configurable.')
add(6,'Removable plate — underside and FACE A',[panel('M074 underside · no device bores',common,(0,0,-1),annotations=[ann([300,110,8],'12 mm plywood\n160 ×116 mm',(50,-45))]),panel('FACE A: up / rear of controls',common,(0,0,1),annotations=[ann([279,110,20],'4 ×12 strain-relief slot',(-80,35)),ann([321,110,20],'Second generic clamp slot',(30,-35))])],'Only the two generic strain-relief slots are current plate CNC geometry. Device bores and four attachment interfaces remain purchased-hardware references. FACE B receives no CNC; use hidden-face labels rather than visible engraving.')
reach=sub(study,['Underfront_AccessButton2_palm','Underfront_AccessButton2_finger'])
add(7,'Player reach — under-front approach',[panel('70 mm palm corridor; finger curls upward',front|visible|reach,(1,-2,-.7),alpha={**{n:.3 for n in front},**{n:.6 for n in reach}})],'Actual swept palm/finger reserve clears the cabinet and neighboring controls for each of five owner buttons. Three standing-front sightline screens keep the controls hidden. Physical reach, clothing clearance and comfort still require owner trial; this is not ergonomic certification.')
usbparts=select(module,'Underfront_USB','Underfront_Harness');usbparts.update(select(study,'Underfront_USB'))
add(8,'USB depth, cap and flexible service reserve',[panel('Rear depth and lower plug / cap access',usbparts|common,(1,-1,.5),alpha={n:.22 for n in usbparts if any(t in n for t in ['Reserve','Hand','Sweep'])},annotations=[ann([342,131,78],'70 mm rear reserve',(35,25)),ann([342,131,-20],'Cap opens rearward;\nplug approaches from below',(-140,-35))])],'The cap sweep and hand/plug corridors are native study geometry. USB compatibility with a 12 mm plate is unverified; a later one-face pocket is supported but its depth is not frozen. A flexible harness reserve provides service slack; no electrical connector architecture is mandated.')
section={n:clip(s,298,302,35,180,-10,50) for n,s in {'FLOOR':new['FLOOR'],'Underfront_Plate':new['Underfront_Plate']}.items()}
add(9,'Floor shoulder — one-face 2 mm recess',[panel('Exact section through module center',section,(-1,0,0),annotations=[ann([300,56,27],'2 mm locating recess\n16 mm structural shoulder',(-125,55)),ann([300,110,8],'12 mm removable plate\n10 mm below floor underside',(20,-45))])],'The selected 2 mm recess locates the plate while preserving more floor material than the 3/4 mm alternatives. The 132 ×88 mm through bay and recess are both cut from the existing underside FACE A. Fit clearance remains measured-thickness and coupon dependent.')
attach=select(module,'Underfront_Screw','Underfront_Insert');attach.update(select(study,'Underfront_AttachmentDriver'))
add(10,'Four underside attachments — ordinary tool access',[panel('Captive metal receiver / removable screw',common|attach,(1,-1,-.2),alpha={'Underfront_Plate':.28},annotations=[ann([230,62,20],'Blind captive receiver\nReference only',(-130,50)),ann([370,158,-155],'Straight driver corridor',(10,-35))])],'Four provisional M4 screw/metal-insert interfaces are reached from below; no loose interior nut or playfield removal is needed. Hole size, insert OD/length, head seat and purchased screw stack remain HOLD. The cabinet wood is not released with assumed bores.')
exp={}
for n,s in owner.items():
 dz=-60 if n=='Underfront_Plate' else -115 if 'Screw' in n else 30 if 'Insert' in n else -85
 exp[n]=shift(s,z=dz)
exp['FLOOR_Section']=clip(new['FLOOR'],200,400,30,190,10,40)
add(11,'Module exploded — remove from below',[panel('Semantic exploded view',exp,(1,-1,-.45))],'Exploded offsets explain the parts; they are not a physical insertion certificate. The separate service proof verifies 100 mm downward rigid withdrawal and a flexible harness slack reserve. Do not pull fixed wiring or choose an electrical disconnect here.')
coin=json.loads((R/'config/front_panel_v32.json').read_text());defs=definitions(coin,True);openparts={n:turn(s,coin['coin_door'],110) if moving else s for n,(s,k,moving) in defs.items()}
add(12,'Coin door — 110° service state',[panel('Owner controls remain installed',front|openparts|module,(1,-2,.5),alpha={'FLOOR':.38})],'Coin door sweep is validated 0–110°. The control envelopes remain below the moving door by at least 1 mm in the current planning geometry; the harness loop stays behind the outward sweep. Physical hinge and latch choices remain provisional.')
land=select(new,'FrontLanding');land.update(select(new,'Button','Leaf'));land.update({'PF_BasePlywood':clip(new['PF_BasePlywood'],45,555,30,335,250,450)})
add(13,'Playfield landings — unchanged protected mechanism',[panel('Front bay below fixed side landings',land|module|{'FLOOR':clip(new['FLOOR'],10,590,30,330,0,40)},(1,-2,.55),alpha={'PF_BasePlywood':.25,'FLOOR':.3})],'The V33.6.3 side landings, adjusters, captive retainers, front relief, side buttons and accepted playfield pose remain unchanged. Module/cable reserves are checked against playfield service, lift-out and landing tool access; no support hardware is relocated.')
legs=select(new,'CandidateLegBlock','CandidateLegPlate');legs={n:s for n,s in legs.items() if n.endswith(('FL','FR'))}
add(14,'SW01 leg blocks — solid wood remains separate',[panel('Front blocks / module separation',legs|module|{'FLOOR':clip(new['FLOOR'],0,600,0,300,0,45)},(1,-2,-.5),alpha={'FLOOR':.3})],'Four SW01 shop-made solid-wood leg blocks remain outside the plywood stock-family count. They are not relabelled as 12 or18 mm plywood. Front leg hardware, floor cleats and lockdown/coin interfaces retain their current geometry.')
add(15,'M028 floor filters — 8 mm to 12 mm stock',[panel('BEFORE · 8 mm',{'BeforeFilter':old['RemovableIntakeFilterL']},(1,-1,-1)),panel('AFTER ·12 mm lands /8 mm interface web',{'Filter':new['RemovableIntakeFilterL']}|sub(new,['FloorFilterScrewL1','FloorFilterScrewL2','FloorFilterScrewL3','FloorFilterScrewL4']),(1,-1,-1),annotations=[ann([80,640,6],'4 mm underside recess\nExisting screw head retained',(-70,-55))])],'R86 ×4 mm service pocket preserves media, rotated guard and fan hardware; four R7 recesses preserve screw heads. Each holder retains 5118.85 mm² of12 mm lands. The exact continuous 80 mm downward filter-service sweep passes. All cuts enter underside FACE A.')
bezelparts={'BB_Backglass':clip(new['BB_Backglass'],-80,-40,1100,1230,835,905),'BB_Display32':clip(new['BB_Display32'],-80,-40,1100,1230,835,905),'BB_DisplayReplaceableBezel':clip(new['BB_DisplayReplaceableBezel'],-80,-40,1100,1230,835,905)}
add(16,'M045 bezel — explicit faced-stock exception',[panel('Finished bezel shape is unchanged',{'BB_DisplayReplaceableBezel':new['BB_DisplayReplaceableBezel']},(0,-1,.1)),panel('Protected glass / bezel / display section',bezelparts,(-1,0,0),annotations=[ann([-60,1123,850],'6 mm finished bezel\n12 mm stock,6 mm rear facing',(-155,-45)),ann([-60,1128,890],'2 mm display clearance',(-100,35))])],'Nominal stock is12 mm; finished bezel remains6 mm to preserve both2 mm clearances. This full-face reduction is explicit, not a hidden third stock family. FACE A is the rear; no glass, display, visible front plane or carrier datum moves.')
add(17,'M058 intake frames — preserve mating plane',[panel('BEFORE ·6 mm',{'BeforeFrame':old['BB_IntakeFilterFrameL']},(1,2,.7)),panel('AFTER ·12 mm',{'Frame':new['BB_IntakeFilterFrameL']},(1,2,.7),annotations=[ann([125,1334.1,778],'220 ×80 mm aperture\n6 mm exterior growth',(20,35))])],'Frames grow only rearward. The door mating plane and mesh aperture remain exact; a continuous80 mm rearward removal corridor passes. Selected fastener length must include6 mm additional stack. No unselected screw head is silently relocated.')
bafflemembers={p['instance_id']:brep(p['installed_brep']) for p in json.loads((O/'conversion-manufacturing-map.json').read_text())['parts'] if p['source_component']=='BB_IntakeDownBaffleL'}
bexp={n:shift(s,x=-25 if n.endswith('Side1') else 25 if n.endswith('Side2') else 0,y=-30 if n.endswith('Face') else 0,z=25 if n.endswith('Top') else 0) for n,s in bafflemembers.items()}
add(18,'M059 / M060 / M061 — four real baffle pieces',[panel('Current assembled baffle',{'Baffle':new['BB_IntakeDownBaffleL'],'PassiveBolt':new['BB_PassiveBoltBodyReserve0']},(1,-2,.8),annotations=[ann([260,1300,700],'Existing passive bolt body\nHardware reserve;2 mm gap',(-150,-55))]),panel('Four-piece exploded; same airway',bexp,(1,-2,.8))],'Outside growth uses12 mm stock. All four side members share a3 mm deep ×32 mm high exterior lower-edge rebate, leaving9 mm local wall and12 mm upper wall. This preserves2 mm clearance to the existing passive bolt. Exact four-member union difference:0 mm³.')
Air=Part.makeBox(220,36,98,V(15,1274.1,686));ap={'Airway':Air,'Baffle':new['BB_IntakeDownBaffleL'],'Frame':new['BB_IntakeFilterFrameL']}
add(19,'Airflow geometry — unchanged inner throat',[panel('Exact chamber / inlet / downward outlet',ap,(1,-2,-.4),alpha={'Baffle':.22,'Frame':.35,'Airway':.35},annotations=[ann([125,1290,686],'Downward mouth\n220 ×36 =7920 mm²',(-125,-45)),ann([125,1310.1,738],'Inlet220 ×80 =17600 mm²',(20,30))])],'Both baffles preserve the220 ×36 ×98 mm inner chamber (776160 mm³ each). Inlet and outlet areas are unchanged; no cable opening is counted as intake. Dust protection and cleaning access remain. This geometric screen is not a thermal/pressure-loss certification.')
bl={n:brep(p) for n,p in conv['optional_breps'].items()}
add(20,'M066 fan blank — same station, 12 mm stock',[panel('BEFORE ·6 mm',{'BeforeBlank':brep(conv['changes']['BB_FanBlankL']['before_brep'])},(1,2,.5)),panel('AFTER ·12 mm',{'Blank':bl['BB_FanBlankL']},(1,2,.5))],'128 ×128 mm outline,105 mm mounting pitch and door mating plane remain exact. Extra6 mm lies outside the door. Blank and fan/guard/mesh are mutually exclusive states; fastener length is a purchased-hardware hold. Optional blanks are not installed over fans.')
# Actual local manufacturing solids in simple rows, never bounding-box proxies.
stockpanels=[]
for th in [18,12]:
 parts={};x=y=rowh=0
 pp=[p for p in reg['parts'] if p['nominal_stock_thickness_mm']==th and p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART']
 for p in sorted(pp,key=lambda p:-max(p['finished_xy_size_mm'])):
  s=brep(p['finished_member_brep']);b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin));b=s.BoundBox
  if x+b.XLength>2500:x=0;y+=rowh+65;rowh=0
  s.translate(V(x,y,0));parts[p['instance_id']]=s;x+=b.XLength+65;rowh=max(rowh,b.YLength)
 stockpanels.append(panel(f'{th} mm nominal ·{len(pp)} CNC pieces',parts,(0,0,1)))
add(21,'Actual manufacturing pieces — two plywood stocks',stockpanels,'Every shape is a real finished manufacturing B-rep from the current register. This identification layout is not nesting or CAM. Nominal12/18 mm stock may retain local pockets or faced webs. Four SW01 solid-wood blocks are counted separately; no odd plywood stock family is introduced.')
nest=json.loads((O/'material-utilization.json').read_text());nestpanels=[];byid={p['instance_id']:p for p in reg['parts']}
for sheet in nest['sheets']:
 parts={};annotations=[]
 for pl in sheet['placements']:
  p=byid[pl['instance_id']];s=brep(p['finished_member_brep']);b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin))
  if pl['rotated']:s.rotate(V(),V(0,0,1),90)
  b=s.BoundBox;s.translate(V(pl['x']-b.XMin,pl['y']-b.YMin,0));parts[pl['instance_id']]=s
  if pl['w']*pl['h']>100000:annotations.append(ann([pl['x']+pl['w']/2,pl['y']+pl['h']/2,30],pl['id'],(0,0)))
 boundary=[[[0,0,0],[2500,0,0],[2500,1600,0],[0,1600,0],[0,0,0]]];usable=[[[20,20,0],[2480,20,0],[2480,1580,0],[20,1580,0],[20,20,0]]]
 p=panel(sheet['id']+' · PRELIMINARY',parts,(0,0,1),annotations=annotations,lines=[{'lines':boundary,'color':'#253b43','width':1},{'lines':usable,'color':'#8e5d4b','width':1,'style':'--'}]);p['limits']=[-20,2520,-20,1620];nestpanels.append(p)
add(22,'Preliminary sheet feasibility — NOT FOR CNC',nestpanels,'Actual manufacturing contours follow the current deterministic heuristic placements.2500 ×1600 mm sheet;20 mm border;≥15 mm finished-boundary spacing. This is non-production, not an optimized release nest. Actual thickness, fit coupon and hardware dimensions remain mandatory release gates.')
full=actual(new)
add(23,'Complete cabinet — underside inspection',[panel('Controls hidden from normal standing view',full,(1,-2,-1),alpha={'CandidateGlass':.18})],'The user module is underside-removable; the rest of the cabinet architecture is preserved. Floor fans/filter holders retain downward service. Backbox service/fold, front leg blocks and playfield landings remain integrated. Electronics are optional user equipment, not mandatory flatpack hardware.')
interior={n:s for n,s in actual(new).items() if not n.startswith(('PF_','Matrix','MX_')) and n not in ['PLAYFIELD_ENVELOPE','CandidateGlass','SIDE_L']}
interior.update({n:s for n,s in module.items() if 'Reserve' in n})
add(24,'Complete cabinet — interior inspection',[panel('Playfield/supports hidden for inspection',interior,(1,-2,1.2),alpha={n:.2 for n in interior if 'Reserve' in n})],'Viewer-only inspection hides the playfield, supports, matrix, main glass and near cabinet side. No CAD component has moved. New rear control envelopes, shelves and fixed landing structure remain visible. Manufacturing remains blocked pending hardware, material and coupon validation.')
scenes[21]['note']+=' Current preliminary study: '+', '.join(str(s['improved_study_sheets'])+' sheet(s) at '+str(s['thickness_mm'])+' mm' for s in nest['stocks'])+'.'
assert len(scenes)==24
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
READS.update([Path(__file__),R/'tools/render_two_stock_v337.py',R/'tools/coin_door_v32.py',R/'exports/generated/front-landings-v3363/play.FCStd',R/'config/underfront_user_module_v337.json',R/'config/front_panel_v32.json',O/'play.FCStd',O/'conversion.FCStd',O/'module-study.FCStd',O/'modulevariants.FCStd',O/'module-fallback.FCStd',O/'module-validation.json',O/'conversion-validation.json',O/'module-location-search.json',O/'conversion-manufacturing-map.json',O/'manufacturing-register.json',O/'geometry-validation.json',O/'material-utilization.json'])
(O/'review-source-hashes.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(READS)},indent=2)+'\n')
print('V337_REVIEW_SCENES_PASS',len(scenes),flush=True)

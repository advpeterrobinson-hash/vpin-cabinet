"""22 V33.8 native CAD review scenes; no design mutation. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import json,gzip,sys,hashlib,re
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V
from coin_door_v32 import definitions,turn
O=R/'exports/generated/service-productization-v338';READS=set();scenes=[]
def read(path):
 path=R/path if not Path(path).is_absolute() else Path(path);READS.add(path);return json.loads(path.read_text())
def native(path):
 path=R/path if not Path(path).is_absolute() else Path(path);READS.add(path);return load(path)
def brep(path):
 path=R/path;READS.add(path);s=Part.Shape();s.read(str(path));return s
new=native(O/'play.FCStd');old=native('exports/generated/two-stock-user-module-v337/play.FCStd');study=native(O/'landing-study.FCStd');released=native(O/'released.FCStd');tool=native('exports/generated/front-landings-v3363/tool-access.FCStd')
G=read(O/'geometry-validation.json');L=read(O/'landing-study.json');D=read(O/'retention-decision.json');adj=read(O/'adjustment-validation.json')
assert G['pass'] and L['pass'] and D['selected_option']=='A'
assert hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest()==G['native_sha256']
def sub(d,names):return {n:d[n] for n in names if n in d}
def sel(d,*prefix):return {n:s for n,s in d.items() if n.startswith(prefix)}
def clip(s,x0,x1,y0,y1,z0,z1):return s.common(Part.makeBox(x1-x0,y1-y0,z1-z0,V(x0,y0,z0)))
def shift(s,x=0,y=0,z=0):q=s.copy();q.translate(V(x,y,z));return q
def color(n):
 if 'Difference' in n:return '#b45352'
 if 'Hand' in n or n.startswith(('retention_','adjuster_')):return '#729ba2'
 if any(k in n for k in ['Screw','Bolt','Nut','nut','Insert','Receiver','Washer','Stem','Ring']):return '#657f88'
 if 'Pad' in n or 'Swivel' in n:return '#478b75'
 if 'Knob' in n:return '#bc7747'
 if 'Blank' in n or '_Block' in n or n.startswith('SW02'):return '#b78959'
 if 'Layer1' in n:return '#be9a63'
 if 'Layer2' in n:return '#d9bb87'
 if 'Layer3' in n:return '#a78955'
 if 'Glass' in n:return '#95babe'
 if 'ENVELOPE' in n or 'Display' in n:return '#3b5562'
 if 'SIDE' in n or 'Side' in n:return '#c8b28a'
 return '#bfa678'
def panel(label,parts,view=(1,-2,1),alpha=None,annotations=None,edges=None):
 meshes=[]
 for n,s in parts.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.45,AngularDeflection=.55,Relative=False);v,f=m.Topology
  if f:meshes.append({'name':n,'vertices':[list(x) for x in v],'faces':f,'color':color(n),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':meshes,'view':view,'annotations':annotations or [],'edges':edges or [],'points':[]}
def ann(v,t,offset=(20,20)):return {'point':list(v),'text':t,'offset':offset}
def clean(t):return re.sub(r'(?<=[a-z])(?=\d)|(?<=[;×])(?=\S)|(?<=,)(?=[^\d\s])',' ',t)
def add(i,title,panels,note):scenes.append({'id':f'{i:02d}','title':title,'panels':panels,'note':note})
z=new['FrontLandingL_Block'].BoundBox.ZMin
layers=sub(old,[f'FrontLandingL_Layer{i}' for i in [1,2,3]])
exploded={n:shift(s,z=(int(n[-1])-1)*22) for n,s in layers.items()}
add(1,'Previous landing — three plywood laminations per side',[
 panel('CURRENT before this task: exact installed layers',layers,(1,-1,.6),annotations=[ann([70,260,z+27],'3 ×18 mm plywood\n54 mm assembled depth',(-155,50))]),
 panel('Semantic exploded view · six pieces across both sides',exploded,(1,-1,.6))],
 'The native V33.7 profiles are shown, including actual reference bores. Two binder screws per side and the lamination glue-up belonged to this earlier construction. Exploded translation is documentation only; no accepted playfield or cabinet datum moves.')
add(2,'SW02 — one shop-made solid block per side',[
 panel('Shop blank · X68 ×Y70 ×Z54 mm',sub(study,['SW02_L_Blank']),(1,-1,.6),annotations=[ann([52,260,z+54],'Dry / straight / knot-free solid wood\nGrain provisionally along X68',(-125,60))]),
 panel('Finished reference geometry · one solid',sub(new,['FrontLandingL_Block']),(1,-1,.6),annotations=[ann([72,245,z+54],'Same adjuster and retention axes',(15,45))])],
 'SW02 replaces three 18 mm layers without introducing another plywood stock. Species, strength, moisture and purchased drilling sizes remain held. The woodshop supplies a square blank; qualified guide/template/manual drilling creates the reference interfaces.')
u=study['FrontLandingL_OldUnion'];b=new['FrontLandingL_Block'];diff=b.cut(u)
add(3,'SW02 / former union — exact external geometry',[
 panel('Old union translucent over new solid',{'OldUnion':u,'FrontLandingL_Block':b},(1,-1,.6),{'OldUnion':.2,'FrontLandingL_Block':.65}),
 panel('Only obsolete binder holes are filled',{'FrontLandingL_Block':b,'Difference_FilledBinderBores':diff},(1,-1,.6),{'FrontLandingL_Block':.25},[ann([38,260,z+28],f'{L["SW02"][0]["filled_binder_mm3"]:.3f} mm³ filled / side\n0 mm³ old functional wood removed',(-130,45))])],
 'External and mating surfaces remain exact. The symmetric difference is deliberately nonzero only because redundant binder bores are filled. Adjuster, retainer and side-attachment reference bores remain. No claim of byte-identical internal voids hides this manufacturing simplification.')
landL=sel(new,'FrontLandingL_');section={n:clip(s,70,74,220,300,z-35,z+105) for n,s in landL.items()}
section['M025']=clip(new['PF_BasePlywood'],70,74,225,295,z+54,z+100)
add(4,'SW02 drilling / adjuster interface',[
 panel('X72 section through both vertical axes',section,(1,0,0),{'FrontLandingL_Block':.7},[ann([72,245,z+40],'M8 metal insert / articulated pad\nPurchased bores remain HOLD',(-180,50)),ann([72,275,z+18],'Separate M6 retention path',(15,-40))]),
 panel('Four side paths retain original coordinates',landL,(1,-1,.5),{'FrontLandingL_Block':.28},[ann([86,234,z+45],'9 mm center-to-Y-end\nReference head edge ligament 4.5 mm',(-130,55))])],
 f'A scale-verified paper template locates centers; a clamped portable perpendicular guide and depth stop control the 54/68 mm drilling paths. Paper alone is insufficient. Mechanical travel remains ±3 mm, but the occupied-volume common-height setup screen is {adj["geometric_common_height_setup_window_mm"][0]:+.1f}…{adj["geometric_common_height_setup_window_mm"][1]:+.1f} mm with 1 mm margin. Restore the nominal 9.906669° pose; do not choose a new PLAY angle or twist the rigid base.')
ret_names=[n for n in landL if '_Retention' in n]+['FrontLandingL_Block']
add(5,'Selected retention A — captive M6 tool-operated bolt',[
 panel('Engaged · metal receiver / captive stop',sub(new,ret_names)|{'M025':clip(new['PF_BasePlywood'],48,98,255,294,z+54,z+110)},(1,-1,.3),{'FrontLandingL_Block':.28,'M025':.32},[ann([72,275,z+65],'7 mm nominal engagement\nQualified setting 6–8 mm',(-160,65))]),
 panel('Released · no loose support hardware',sub(released,ret_names),(1,-1,.3),{'FrontLandingL_Block':.3},[ann([72,275,z-25],'10.5 mm release / park\nWasher, stops and captive ring retained',(-150,-50))])],
 'Two independent existing M6 ×100 retainers remain selected. Release both through the open coin door before opening/lift-out. Reset stop position after setup so the blind receiver does not bottom. Captivity, anti-loosening, receiver pull-out and nudge tests still require the purchased parts and physical qualification.')
knobpan=[]
for diam in [30,35,40]:
 pp=sub(new,['FrontLandingL_Block'])|sub(study,[f'HandKnob_D{diam}_L'])
 knobpan.append(panel(f'Ø{diam} ×21 mm envelope · HOLD',pp,(1,-1,.3),{'FrontLandingL_Block':.45}))
add(6,'Hand-operated retention B — packaging pass, not promoted',knobpan,
 'All three head sizes and conservative finger/palm approach sweeps clear the modeled cabinet, including 10.5 mm retraction; minimum approach gap is 6.5 mm. A compatible long-shank captive hand assembly, grip retention and anti-release behavior are unqualified. No friction cap or short catalog knob is silently substituted for the selected retainer.')
recv=new['FrontLandingL_RetentionReceiver'];rr=clip(recv,70,74,265,285,z+50,z+110)
basecut=clip(new['PF_BasePlywood'],70,74,265,285,z+50,z+110)
add(7,'Quick-pin option C — rejected at the current receiver',[
 panel('Actual blind M6 receiver section',{'M025':basecut,'RetentionReceiver':rr},(1,0,0),{'M025':.55},[ann(list(recv.BoundBox.Center),'Blind threaded metal receiver\nNo ball-lock capture shoulder',(-165,50))])],
 'No viable quick-pin candidate is selected. A plain pin in the current threaded receiver cannot supply positive uplift retention. Adding a different bushing, shoulder or through receiver would alter protected material and add complexity. This view shows the real current interface; no invented successful quick-pin assembly is rendered.')
coin=read('config/front_panel_v32.json');coinparts={}
for n,(s,k,m) in definitions(coin,True).items():coinparts[n]=turn(s,coin['coin_door'],110) if m else s
front={n:clip(s,0,600,-40,430,0,420) for n,s in sub(new,['FRONT','SIDE_L','SIDE_R','FLOOR']).items()}
access=sel(tool,'retention_');land=sel(new,'FrontLanding');under=sel(new,'Underfront_');under={n:s for n,s in under.items() if 'Reserve' not in n}
add(8,'Selected tool access — coin door open 110°',[
 panel('Both captive retainers reached from the front',front|coinparts|land|access|under,(1,-2,.55),{**{n:.22 for n in front},**{n:.25 for n in access}},[ann([72,275,z-20],'Compact tool corridor L',(-160,45)),ann([528,275,z-20],'Compact tool corridor R',(25,45))])],
 'The actual earlier spanner/hand access geometry is retained and checked against SW02. The selected mechanism remains tool-operated. Coin door, underfront module, front buttons and plunger keep their current coordinates. Do not substitute the held hand-knob study for an approved tool-free workflow.')
for file,expected in [('safety-review-scenes.json.gz',list(range(9,12))),('modularity-review-scenes.json.gz',list(range(12,21)))]:
 path=O/file;READS.add(path);ss=json.loads(gzip.decompress(path.read_bytes()));assert [int(s['id']) for s in ss]==expected;scenes+=ss
# Aggregate-page annotation placement only; contributor/native geometry stays
# exact. Keep the ACC01 note inside its left panel at the rendered page scale.
scene13=next(s for s in scenes if s['id']=='13')
next(a for a in scene13['panels'][0]['annotations'] if a['text'].startswith('ACC01'))['offset']=[-130,60]
# True shipping solids in the preferred final packing study. Boxes/separators
# are packaging reference geometry, never substitutes for manufactured pieces.
reg=read(O/'manufacturing-register.json');packing=read(O/'packaging.json');byid={p['instance_id']:p for p in reg['parts']}
choice=next(c for c in packing['candidates'] if c['target_kg']==packing['preferred_target_kg']);bundles=choice['bundles'];packed={};packingann=[];single={}
for bi,bundle in enumerate(bundles):
 dx=(bi%3)*1600;dy=(bi//3)*1050;Lx,Wy,Hz=bundle['external_LWH_mm']
 for layer in bundle['layers']:
  for loc in layer['pieces']:
   p=byid[loc['instance_id']];s=brep(p.get('cnc_stage_brep') or p['finished_member_brep'])
   # Solid wood ships as undrilled shop blank, documented in the register.
   if p.get('manufacturing_class')=='SHOP_MADE_SOLID_WOOD_PART':
    bb=s.BoundBox;s=Part.makeBox(bb.XLength,bb.YLength,bb.ZLength)
   bb=s.BoundBox;s.translate(V(-bb.XMin,-bb.YMin,-bb.ZMin))
   if loc['rotated']:s.rotate(V(),V(0,0,1),90)
   bb=s.BoundBox;s.translate(V(loc['x']+20-bb.XMin,loc['y']+20-bb.YMin,layer['z']-bb.ZMin))
   packed[bundle['id']+'_'+loc['instance_id']]=shift(s,dx,dy)
   if bi==len(bundles)-1:single[loc['instance_id']]=shift(s,z=layer['order']*45)
 packingann.append(ann([dx+Lx/2,dy+Wy/2,Hz+10],bundle['id']+f'\n{Lx:.0f} ×{Wy:.0f} ×{Hz:.0f} mm\nHIGH {bundle["gross_high_density_kg"]:.3f} kg',(-90 if bi==2 else -45,25)))
add(21,'Packaging impact — actual contents / preliminary bundles',[
 panel(f'{len(bundles)} preferred wood bundles · hardware separate',packed,(.5,-1,1.5),annotations=packingann),
 panel('Last bundle · layer offsets for identification',single,(1,-2,1),annotations=[])],
 f'SW02 replaces six plywood layers with two solid blanks; four binder screws are eliminated. {len(reg["parts"])} wood pieces remain in the minimum set. Packing uses actual CNC-stage shipping shapes and undrilled SW01/SW02 shop blanks. Separators/edge protection and separate hardware box remain required; glass/electronics are excluded. Dimensions and HIGH masses come from the final preliminary packing report, not a shipping qualification.')
full=actual(new)
add(22,'Completed cabinet — protected architecture retained',[
 panel('Final CURRENT geometry · no optional boards / straps',full,(1,-2,1),{'CandidateGlass':.18}),
 panel('Interior inspection · SW02 with accepted systems', {n:s for n,s in full.items() if not n.startswith(('PF_','Matrix','MX_')) and n not in ['PLAYFIELD_ENVELOPE','CandidateGlass','SIDE_L']},(1,-2,1),{})],
 'Only the accepted front-landing bodies become SW02 and the obsolete binder screws retire. WPC axis, backbox, shelves, T members, main glass, M025 geometry, controls and all other protected systems remain. Optional boards are not mandatory, and no safety strap is promoted. Raised 50° primary support remains a separate unresolved qualification gate; full-sheet CNC release stays blocked.')
assert [int(s['id']) for s in scenes]==list(range(1,23))
for scene in scenes:
 scene['title']=clean(scene['title']);scene['note']=clean(scene['note'])
 for p in scene['panels']:
  p['label']=clean(p['label'])
  for a in p['annotations']:a['text']=clean(a['text'])
(O/'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
for file in ['safety-source-hashes.json','modularity-review-sources.json']:
 raw=read(O/file)
 # Contributor hash manifests are included as sources as well as verified.
 entries=raw.get('sources',raw) if isinstance(raw,dict) else raw
 if isinstance(entries,dict):
  for path,h in entries.items():
   if not isinstance(h,str) or len(h)!=64:continue
   f=R/path
   if f.exists():assert hashlib.sha256(f.read_bytes()).hexdigest()==h,('stale contributor input',path);READS.add(f)
READS.update([Path(__file__),R/'tools/render_service_productization_v338.py',R/'tools/coin_door_v32.py'])
(O/'review-source-hashes.json').write_text(json.dumps({str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(READS)},indent=2)+'\n')
print('V338_REVIEW_SCENES_PASS',len(scenes),flush=True)

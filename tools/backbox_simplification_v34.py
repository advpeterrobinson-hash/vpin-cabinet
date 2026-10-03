"""V34 independent simple backbox CAD; original CERN-OHL-S-2.0.
Run with FreeCAD Python; no vendor CAD and no production drilling authority.
"""
from pathlib import Path
import json,sys,math,hashlib,gzip,copy
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,V,WPC,PF,transform,certify,build_locks,with_tethers,route
from backbox_service_v32 import door_pose
C=json.loads((R/'config/backbox_simplification_v34.json').read_text());O=R/C['output'];O.mkdir(exist_ok=True,parents=True)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def shift(s,x=0,y=0,z=0):q=s.copy();q.translate(V(x,y,z));return q
def cy(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))
def cx(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(1,0,0))
def cz(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z))
def rr(x,y,z,w,d,h,r):
 q=box(x+r,y,z,w-2*r,d,h).fuse(box(x,y,z+r,w,d,h-2*r))
 for xx in [x+r,x+w-r]:
  for zz in [z+r,z+h-r]:q=q.fuse(cy(xx,y,zz,r,d))
 return q.removeSplitter()
def yzround(x,y,z,d,w,h,r=2):
 q=rr(y,-x-d,z,w,d,h,r);q.rotate(V(),V(0,0,1),90);return q
def slot(x,y,z,r,travel,d):return cy(x,y,z-travel/2,r,d).fuse(cy(x,y,z+travel/2,r,d)).fuse(box(x-r,y,z-travel/2,2*r,d,travel)).removeSplitter()
def diff(a,b):return 0.0 if a.exportBrepToString()==b.exportBrepToString() else a.cut(b).Volume+b.cut(a).Volume
def bb(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def mesh(s):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.6,Relative=False);v,f=m.Topology
 return {'vertices':[list(x) for x in v],'faces':f}
def save(name,ss):
 d=A.newDocument('V34_'+name.replace('-','_'))
 for n,s in ss.items():d.addObject('PartDesign::Feature',n).Shape=s
 d.recompute();assert all('Invalid' not in o.State for o in d.Objects);d.saveAs(str(O/(name+'.FCStd')));A.closeDocument(d.Name)
def dump(n,j):(O/(n+'.json')).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
p=load(R/C['source']);checks=[]
def ck(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail});print(n,bool(v),flush=True)
retire_prefix=('BB_Monitor','BB_Stop','BB_ReplaceableVESA','BB_DisplayReplaceableBezel','BB_LowerCassette','BB_SpeakerBaffle','BB_DMDReplaceable','BB_DMDRear','BB_DMDDepth','BB_Cassette','BB_Glass','BB_TopFrontRail')
retired=[n for n in p if n.startswith(retire_prefix)];s={n:q.copy() for n,q in p.items() if n not in retired};wood={};hw={};ref={}
# Shell: remove the old glass groove front lips. All machining opens to inside FACE_A.
for side,x in [('L',-78),('R',672)]:
 name='BB_Side'+side;q=p[name]
 q=q.cut(yzround(x,1000,838,6,120,483))
 # lower panel register; 4 mm capture each side, open to front
 q=q.cut(yzround(-76 if side=='L' else 672,1000,614,4,197.2,207))
 # top-open plate dado: nominal stock + explicit review clearance, not production fit.
 q=q.cut(yzround(-76 if side=='L' else 672,1239.8,852,4,18.4,470))
 s[name]=q.removeSplitter();wood[name]=s[name]
# Restore a single full top, preserving the outside envelope of old top/front rail.
top=p['BB_Top'].fuse(p['BB_TopFrontRail']).fuse(box(-78,1112,1302.8,756,8,18)).removeSplitter()
s['BB_Top']=top;wood['BB_Top']=top
m=C['monitor'];plate=box(*m['plate_box_mm']);window=rr(*m['opening_box_mm'],m['opening_radius_mm']);plate=plate.cut(window)
for pitch in m['VESA_patterns_mm']:
 for x in [300-pitch/2,300+pitch/2]:
  for z in [1069-pitch/2,1069+pitch/2]:plate=plate.cut(slot(x,1239,z,2.5,10,20))
s['BB_MONITOR_PLATE']=plate.removeSplitter();wood['BB_MONITOR_PLATE']=s['BB_MONITOR_PLATE']
for side,x in [('L',-72),('R',660)]:
 n='BB_MONITOR_STOP_'+side;s[n]=box(x,1240,824,12,40,30);wood[n]=s[n]
 # two direct screws per stop; envelopes only, no frozen pilot diameter.
 for i,y in enumerate([1248,1272]):hw[n+'_Screw'+str(i)]=cx(-84 if side=='L' else 660,y,839,2,24)
# The DMD sits IN FRONT of the single panel. Rear VESA bosses meet its front face.
# This retains actual VESA load material instead of cutting it away as a fascia aperture.
panel=box(*C['lower_panel']['box_mm'])
for x in [13,587]:panel=panel.cut(cy(x,1178,722,58,20))
for x in [262.5,337.5]:
 for z in [680.5,755.5]:panel=panel.cut(slot(x,1178,z,2.5,4,20))
# One functional cable opening below the VESA group, covered by monitor; no arbitrary grid.
panel=panel.cut(rr(260,1178,634,80,20,22,4));s['BB_DMD_SPEAKER_PANEL']=panel.removeSplitter();wood['BB_DMD_SPEAKER_PANEL']=s['BB_DMD_SPEAKER_PANEL']
s['BB_DMDEnvelope']=box(*C['lower_panel']['DMD_box_mm'])
for side in ['L','R']:
 n='BB_ToyZoneUpper'+side;s[n]=p[n].common(box(-100,1262,800,800,24,500))
for side,x in [('L',13),('R',587)]:s['BB_SpeakerEnvelope'+side]=cy(x,1197,722,65,60)
for side,xx in [('L',-72),('R',672)]:
 for i,z in enumerate(C['lower_panel']['attachment_z_mm']):
  # Side-operated bolts. Real cross-dowel dimensions/edge qualification held.
  hw['BB_PanelBolt_'+side+str(i)]=cx(-90 if side=='L' else 654,1188,z,2,36)
  hw['BB_PanelCrossDowel_'+side+str(i)]=cy(-58 if side=='L' else 658,1179,z,3,18)
# Glass front seat: bottom positive lip + side back/lateral cushions + one upper strip.
lower=box(-72,1108,828,744,18,18).cut(box(-73,1112,838,746,8,9)).removeSplitter()
s['BB_GLASS_BOTTOM_SEAT']=lower;wood['BB_GLASS_BOTTOM_SEAT']=lower
s['BB_Backglass']=box(*C['glass']['box_mm'])
s['BB_GLASS_TOP_RETAINER']=box(*C['glass']['retainer_box_mm']);wood['BB_GLASS_TOP_RETAINER']=s['BB_GLASS_TOP_RETAINER']
for side,x in [('L',-78),('R',676)]:
 s['BB_GlassSideCushion'+side]=box(x,1112,840,2,8,459)
 s['BB_GlassBackCushion'+side]=box(-76 if side=='L' else 672,1118,840,4,2,459)
s['BB_GlassBottomCushion']=box(-72,1112,838,744,8,2)
s['BB_GlassTopCushion']=box(-72,1113,1290.8,744,1,8.2)
for i,x in enumerate([100,500]):hw['BB_GlassTopScrew'+str(i)]=cz(x,1108,1290.8,2,26)
# Retainer screw guides are hardware reserves until inserts/fasteners are bought.
# Stop VESA bolt/washer reference envelopes outside plate body (not a selected SKU).
for pitch in [75,100]:
 for x in [300-pitch/2,300+pitch/2]:
  for z in [1069-pitch/2,1069+pitch/2]:
   ref[f'VesaTool_{pitch}_{x}_{z}']=cy(x,1258,z,10,160)
for i,(x,y) in enumerate([(-81,1180),(-81,1270),(681,1180),(681,1270)]):
 hw['BB_TopDirectScrew'+str(i)]=cx(-90 if x<0 else 650,y,1311.8,2.25,40)
 ref['TopTool'+str(i)]=cx(-210 if x<0 else 690,y,1311.8,18,120)
# Installed 100 mm monitor VESA example; 75 mm alternate shares flat plate.
for i,(x,z) in enumerate([(x,z) for x in [250,350] for z in [1019,1119]]):
 hw['BB_VESABolt'+str(i)]=cy(x,1223,z,2,40).fuse(cy(x,1260,z,4,3))
 hw['BB_VESASpacer'+str(i)]=cy(x,1228,z,5,12).cut(cy(x,1227,z,2.2,14))
 hw['BB_VESAWasher'+str(i)]=cy(x,1258,z,6,2).cut(cy(x,1257,z,2.2,4))
for i,(x,z) in enumerate([(x,z) for x in [262.5,337.5] for z in [680.5,755.5]]):
 hw['BB_DMDVESABolt'+str(i)]=cy(x,1174,z,2,26).fuse(cy(x,1199,z,4,3))
 hw['BB_DMDVESAWasher'+str(i)]=cy(x,1197,z,6,2).cut(cy(x,1196,z,2.2,4))
# All new hardware is explicit study packaging only; use metadata to distinguish.
s.update(hw)
for n,q in wood.items():ck('valid one wood solid '+n,q.isValid() and len(q.Solids)==1)
protected={n:q for n,q in p.items() if n not in retired and n not in wood and n not in ['BB_Backglass','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR','BB_ToyZoneUpperL','BB_ToyZoneUpperR']}
ck('all unrelated installed geometry exact',all(diff(q,s[n])<1e-5 for n,q in protected.items()),len(protected))
ck('sides retain outer envelope',all(all(abs(a-b)<1e-6 for a,b in zip(bb(s[n]),bb(p[n]))) for n in ['BB_SideL','BB_SideR']))
# Structure screen: conservative full-span strip beam under twice 12 kg normal load.
struct=[]
for t in [12,18]:
 span=744;netheight=448.8-100;I=netheight*t**3/12;self_mass=(752*448.8-400*100)*t*650/1e9;P=(12+.625*self_mass)*9.81*2;E=4000
 struct.append({'stock_mm':t,'equivalent_central_load_N':P,'plate_self_mass_kg':self_mass,'effective_height_mm':netheight,'E_MPa_provisional':E,'I_mm4':I,'stress_MPa':P*span/4*(t/2)/I,'deflection_mm':P*span**3/(48*E*I),'limit_mm':m['deflection_screen_limit_mm'],'pass':P*span**3/(48*E*I)<=m['deflection_screen_limit_mm']})
ck('18mm selected only after 12mm conservative screen fails',not struct[0]['pass'] and struct[1]['pass'],struct)
panelstruct=[]
for t in [12,18]:
 compliance=0
 for i in range(744):
  x=-72+i+.5;moment=min(x+72,672-x)/2;h=203
  for xc in [13,587]:
   if abs(x-xc)<58:h-=2*math.sqrt(58**2-(x-xc)**2)
  if 260<x<340:h-=22
  if abs(x-262.5)<2.5 or abs(x-337.5)<2.5:h-=30
  compliance+=moment**2/(4000*h*t**3/12)
 own_mass=s['BB_DMD_SPEAKER_PANEL'].Volume*(t/18)*650/1e9;delta=compliance*(6+own_mass)*9.81*2;panelstruct.append({'stock_mm':t,'fold_load_kg':6,'factor':2,'E_MPa_provisional':4000,'plate_self_mass_kg':own_mass,'deflection_mm':delta,'limit_mm':4,'pass':delta<=4,'method':'variable net-section beam, all payload concentrated at centre is conservative; 1mm integration, speaker apertures/service opening/slots deducted'})
ck('DMD panel18 required by12-first fold deflection screen',not panelstruct[0]['pass'] and panelstruct[1]['pass'],panelstruct)
# Exclude only intentional mechanical overlaps: new hardware represents shanks in held holes.
occupied={n:q for n,q in s.items() if n.startswith('BB_') and n not in hw and not any(k in n for k in ['ToyZone','Reserve','FlexCorridor','Tether'])}
def collisions(moving,fixed,skip=()):
 hits=[]
 for n,a in moving.items():
  for k,b in fixed.items():
   if n==k or tuple(sorted([n,k])) in skip:continue
   if a.BoundBox.intersect(b.BoundBox):
    v=a.common(b).Volume
    if v>1e-4:hits.append([n,k,v])
 return hits
newitems={n:q for n,q in wood.items() if n not in ['BB_SideL','BB_SideR','BB_Top']};newitems.update({n:s[n] for n in ['BB_Backglass','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR','BB_ToyZoneUpperL','BB_ToyZoneUpperR']})
h=collisions(newitems,occupied);ck('new wood and payloads clear occupied backbox',not h,h)
# Exact swept extrusion of convex payload envelope along front direction, including full path.
frontmon=box(-70,500,849,740,740,450) # covers monitor all +/-5 heights and 0..12 spacer stack
monobs={n:q for n,q in occupied.items() if n not in ['BB_Display32','BB_Backglass','BB_GLASS_TOP_RETAINER'] and 'Cushion' not in n}
# Stop sweep at plate front; all spacers move display forward, never through plate.
h=collisions({'MonitorFrontInsertion':frontmon,'MonitorInstalledAdjustment':box(-70,1128,839,740,112,460)},monobs);ck('monitor front insertion and complete adjustment envelope',not h,h)
# Direct DMD/panel removal with speakers: front translations preserve the attached assembly.
panelnames=['BB_DMD_SPEAKER_PANEL','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']
panelobs={n:q for n,q in occupied.items() if n not in panelnames}
ph=[]
for n in panelnames:
 q=s[n];b=q.BoundBox;sweep=box(b.XMin,b.YMin-500,b.ZMin,b.XLength,b.YLength+500,b.ZLength)
 ph+=collisions({n:sweep},panelobs)
ck('lower populated panel front removal',not ph,ph)
dmdadjust=[]
for dz in [-2,2]:
 q=shift(s['BB_DMDEnvelope'],z=dz);dmdadjust+=collisions({'DMD_adjust_'+str(dz):q},{n:q for n,q in occupied.items() if n!='BB_DMDEnvelope'})
ck('DMD plusminus2mm height clears shell',not dmdadjust,dmdadjust)
# Plate insertion before top, monitor, glass, lower panel, rear doors. Simple exact sweep.
plateobs={n:q for n,q in occupied.items() if n in ['BB_SideL','BB_SideR','BB_Floor','BB_MONITOR_STOP_L','BB_MONITOR_STOP_R']}
b=plate.BoundBox;platepath=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength+600)
h=collisions({'PlateTopInsertion':platepath},plateobs);ck('plate lowers from top before top assembly',not h,h)
ck('top captures plate',abs(plate.BoundBox.ZMax-top.BoundBox.ZMin)<1e-6 and plate.common(shift(top,z=-.1)).Volume>1)
ck('both stops carry plate',all(plate.common(shift(s['BB_MONITOR_STOP_'+side],z=.1)).Volume>1 for side in ['L','R']))
# Nominal glass path: rise 1 mm, pivot upper edge forward 5 degrees about lower edge.
glassobs={n:q for n,q in occupied.items() if n not in ['BB_Backglass','BB_GLASS_TOP_RETAINER'] and 'Cushion' not in n}
glasshits=[]
for i in range(41):
 q=shift(s['BB_Backglass'],z=1);q.rotate(V(300,1116,841),V(1,0,0),i*.25)
 glasshits+=collisions({'glass_tilt_'+str(i):q},glassobs)
# After top tilt, lift6 additional mm to clear the6mm lower lip. Top remains installed.
for i in range(25):
 q=shift(s['BB_Backglass'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10);q.translate(V(0,0,i*.25));glasshits+=collisions({'glass_lift_'+str(i):q},glassobs)
# Exact conservative translation envelope after lift, checked against all fixed geometry.
q=shift(s['BB_Backglass'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10);q.translate(V(0,0,6));b=q.BoundBox
frontglass=box(b.XMin,b.YMin-200,b.ZMin,b.XLength,b.YLength+200,b.ZLength)
glasshits+=collisions({'glass_continuous_front_envelope':frontglass},glassobs)
# After tilt and lift, move glass forward out of seat and below top.
for i in range(1,21):
 q=shift(s['BB_Backglass'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10);q.translate(V(0,-i*10,6));glasshits+=collisions({'glass_front_'+str(i):q},glassobs)
ck('glass front tilt/removal sample path',not glasshits,glasshits[:20])
# Positive retention: leading/back and side barriers all overlap actual glass edges.
retention={'top_overlap_mm':1299-1290.8,'top_gap_mm':1302.8-1299,'side_overlap_mm':4,'bottom_front_lip_mm':6,'glass_thickness_mm':4,'slot_width_mm':8,'liner_each_face_mm':2,'basis':'bottom U lip + side rear/lateral rebates + upper front strip; rigid-body containment, liner compressed to reference; not impact/glass strength certification'}
ck('glass upper and lower overlaps exceed top travel',min(retention['top_overlap_mm'],retention['bottom_front_lip_mm'])>retention['top_gap_mm']+2)
# Tool corridor for the two vertical retainer screws below strip, before monitor service.
rettools={str(i):cz(x,1108,1200,4,90.8) for i,x in enumerate([100,500])}
h=collisions(rettools,{n:q for n,q in occupied.items() if n!='BB_GLASS_TOP_RETAINER'});ck('glass retainer driver access from below/front',not h,h)
# Simple rear VESA approach with both doors open: no tiny-rod-only proof.
doormoving={n for n in p if any(n.startswith('BB_'+k) for k in ['Door','Fan','Intake','Center','Cam','Passive','Flex','PianoLeafDoor'])}
obsopen={n:q for n,q in occupied.items() if n not in doormoving and n not in ['BB_MONITOR_PLATE','BB_Display32']}
h=collisions(ref,obsopen);ck('rear VESA socket and top direct-driver corridors',not h,h)
# Check lock operational hand paths against only changed material; prior assembly proof inherited.
lockpaths={side+k:q for side,x in [('L',130),('R',470)] for k,q in route(x,1260).items()}
h=collisions(lockpaths,newitems);ck('rear upright lock approach unchanged and clear',not h,h)
# Changes above original lower frame are all carried by rigid backbox. Full adaptive fold vs fixed cabinet.
fixed={n:q for n,q in actual(p).items() if not n.startswith('BB_') and n not in ['CandidateGlass','PF_BackboxCheckEnvelope'] and not n.startswith('Matrix') and 'Glass' not in n and 'MATRIX' not in n.upper()}
foldmoving={n:q for n,q in newitems.items() if n!='BB_DMDEnvelope'};foldmoving['BB_DMDEnvelope']=s['BB_DMDEnvelope'];foldmoving['BB_TopAdded']=top.cut(p['BB_Top'].fuse(p['BB_TopFrontRail']))
foldmoving={n:q for n,q in foldmoving.items() if not q.isNull()}
foldsamples=[]
for a in [0,.25,.5,1,2,5,10,15,30,45,60,75,90]:
 h=collisions(transform(foldmoving,angle=a,axis=WPC),fixed);foldsamples.append({'angle':a,'hits':h})
ck('fold required samples',not any(a['hits'] for a in foldsamples),foldsamples)
try:foldcert=certify(foldmoving,fixed,0,90,WPC);ck('continuous differential fold 0 to90',True,len(foldcert['intervals']))
except AssertionError as e:foldcert={'error':str(e)};ck('continuous differential fold 0 to90',False,str(e))
# Independent old rear-door trajectories against new fixed objects.
doorchecks=[]
for side in ['L','R']:
 moving={n:q for n,q in p.items() if n in doormoving and n.endswith(side)}
 obs=newitems
 for a in [0,1,5,15,30,45,60,75,90,100]:
  doorchecks.append({'side':side,'angle':a,'hits':collisions(door_pose(moving,side,a),obs)})
ck('rear door 0 to100 differential samples',not any(a['hits'] for a in doorchecks),doorchecks)
# Write candidate even if invalid; only promoter may replace CURRENT after all gates.
save('candidate',s);save('study-hardware',hw|ref)
for n,q in wood.items():q.exportBrep(str(O/(n+'.brep')))
dump('geometry-validation',{'pass':all(a['pass'] for a in checks),'checks':checks,'retired':retired,'changed':list(wood)+['BB_Backglass','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR','BB_ToyZoneUpperL','BB_ToyZoneUpperR'],'added_hardware':list(hw),'structural_screen':struct,'panel_structural_screen':panelstruct,'glass_retention':retention,'fold_certificate':foldcert,'door_samples':doorchecks,'source_sha256':hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),'manufacturing_release':False})
dump('geometry-inventory',{'parts':{n:{'bounds_mm':bb(q),'volume_mm3':q.Volume} for n,q in s.items()},'wood':list(wood),'reference_hardware':list(hw)})
(O/'candidate-mesh.json.gz').write_bytes(gzip.compress(json.dumps({n:mesh(q) for n,q in s.items() if n.startswith('BB_')},separators=(',',':')).encode(),mtime=0))
print('V34_STUDY_DONE',all(a['pass'] for a in checks),flush=True)

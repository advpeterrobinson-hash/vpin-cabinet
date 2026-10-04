"""V34.2 native geometric study; no final hardware machining. CERN-OHL-S-2.0."""
from backbox_v342_common import *
C=json.loads((R/'config/backbox_hardening_v342.json').read_text());old=load(R/C['source']);checks=[]
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});print(n,bool(v),flush=True)
retired=[n for n in old if n.startswith(('BB_Intake','BB_FanStrainRelief','BB_FlexCorridor','BB_Backglass','BB_Glass','BB_ToyZone'))]
s={n:q.copy() for n,q in old.items() if n not in retired};wood={};refs={};variants={}
# The original guides are retired machining, not plugs in production: regenerate inside face.
for side,x in [('L',-76),('R',672)]:
 n='BB_Side'+side;healing=box(x,1239.8,852,4,18.4,470).common(box(x,1200,852,4,150,450.8))
 q=old[n].fuse(healing)
 cut=rr(1208.8,-x-4,852,18.4,4,470,2);cut.rotate(V(),V(0,0,1),90)
 s[n]=q.cut(cut).removeSplitter();wood[n]=s[n]
plate=box(-76,1209,854,752,18,448.8).cut(rr(100,1208,885,400,20,100,8))
for x in [250,350]:
 for z in [1019,1119]:plate=plate.cut(slot(x,1208,z,5,30,20))
s['BB_MONITOR_PLATE']=plate.removeSplitter();wood['BB_MONITOR_PLATE']=s['BB_MONITOR_PLATE']
for side in ['L','R']:
 n='BB_MONITOR_STOP_'+side;s[n]=shift(old[n],y=-31);wood[n]=s[n]
 for k in [n+'_Screw0',n+'_Screw1']:s[k]=shift(old[k],y=-31)
# Published outside envelope is a bounding limit. Local boss depth is an explicit sensitivity variable.
def tv(depth=75,boss=65,spacer=12,dz=0):
 front=1209-spacer-boss;z=858+dz
 # full-width thin body plus full-width conservative thick lower electronics band
 body=box(-57.5,front,z,715,boss,422).fuse(box(-57.5,front,z,715,depth,125)).removeSplitter()
 return body,{'front_y':front,'rear_max_y':front+depth,'boss_y':front+boss,'boss_depth':boss,'body_depth':depth,'spacer':spacer,'z':z}
s['BB_Display32'],tvdatum=tv()
for i,(x,z) in enumerate([(x,z) for x in [250,350] for z in [1019,1119]]):
 s['BB_VESABolt'+str(i)]=cy(x,1192,z,2,40).fuse(cy(x,1229,z,4,3))
 s['BB_VESASpacer'+str(i)]=cy(x,1197,z,5,12).cut(cy(x,1196,z,2.2,14))
 s['BB_VESAWasher'+str(i)]=cy(x,1227,z,6,2).cut(cy(x,1226,z,2.2,4))
# Three mm acrylic, same front-service seat, rear paint/film is nonstructural material.
s['BB_AcrylicFront']=box(-76,1114,840,752,3,459)
s['BB_AcrylicMask']=box(-76,1117,840,752,.05,459).cut(box(-43.5,1116.9,891,687,.3,356))
for side in ['L','R']:
 x=-78 if side=='L' else 676;s['BB_AcrylicSideLiner'+side]=box(x,1112,840,2,8,459)
 s['BB_AcrylicBackLiner'+side]=box(-76 if side=='L' else 672,1117.05,840,4,2.95,459)
s['BB_AcrylicBottomLiner']=box(-72,1112,838,744,8,2)
s['BB_AcrylicTopLiner']=box(-72,1113,1290.8,744,1,8.2)
for i,x in enumerate([100,500]):s['BB_AcrylicRetainerScrew'+str(i)]=Part.makeCylinder(2,26,V(x,1108,1290.8))
# Door CNC contains two simple fan stations only. No filter frame or duct/baffle wood.
for side,x in [('L',155),('R',445)]:
 n='BB_Door'+side;b=old[n].BoundBox;q=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength)
 for z in [738,1160]:
  q=q.cut(cy(x,1309,z,58,14))
  for xx in [x-52.5,x+52.5]:
   for zz in [z-52.5,z+52.5]:q=q.cut(cy(xx,1309,zz,2.25,14))
 s[n]=q.removeSplitter();wood[n]=s[n]
 # Commodity grille simplified as four concentric rings plus two radial wires.
 gr=None
 for radius in [15,30,45,59]:
  a=cy(x,1322.1,738,radius,2).cut(cy(x,1322,738,radius-1,2.2));gr=a if gr is None else gr.fuse(a)
 gr=gr.fuse(box(x-60,1322.1,737.5,120,2,1)).fuse(box(x-.5,1322.1,678,1,2,120))
 s['BB_LowerGrill'+side]=gr.removeSplitter()
 fan=box(x-60,1285.1,678,120,25,120) # full occupied fan envelope, including rotor sweep
 variants['BB_LowerIntakeFan'+side]=fan
 for i,(xx,zz) in enumerate([(xx,zz) for xx in [x-52.5,x+52.5] for zz in [685.5,790.5]]):s['BB_LowerGrillScrew'+side+str(i)]=cy(xx,1306,zz,2,20)
for side,x in [('L',13),('R',587)]:s['BB_SpeakerEnvelope'+side]=cy(x,1197,722,65,90)
# Derive local glass plane from largest CURRENT glass B-rep face, not PF base slope.
face=max(old['CandidateGlass'].Faces,key=lambda f:f.Area);normal=face.normalAt(0,0)
if normal.z<0:normal=-normal
angle=math.atan2(-normal.y,normal.z);ca,sa=math.cos(angle),math.sin(angle)
# Existing channel front origin recovered from its bottom plane and front-most vertices.
verts=[v.Point for v in old['CandidateGlassChannelL'].Vertexes];tvals=[v.y*ca+v.z*sa for v in verts];nv=[-v.y*sa+v.z*ca for v in verts];t0=min(tvals);n0=min(nv)
def tf(q):q=q.copy();q.rotate(V(),V(1,0,0),math.degrees(angle));q.translate(V(0,t0*ca-n0*sa,t0*sa+n0*ca));return q
L=C['playfield_glass']['rear_local_length_mm']
s['CandidateGlass']=tf(box(12.5,0,4,575,L,5))
rail=box(0,0,0,18,1100,2).fuse(box(12,0,2,6,1100,2)).fuse(box(10,0,2,2,1100,8)).fuse(box(12,0,10,6,1100,1)).removeSplitter()
s['CandidateGlassChannelL']=tf(rail);mirror=A.Matrix();mirror.A11=-1;mirror.A14=600;s['CandidateGlassChannelR']=s['CandidateGlassChannelL'].transformGeometry(mirror)
# Conventional plastic rear U. Groove opens toward player, not a custom moving clamp.
u=box(20,L-10,2,560,14,1.5).fuse(box(20,L-10,9.5,560,14,1.5)).fuse(box(20,L+.5,3.5,560,3.5,6)).removeSplitter()
s['BB_PFRearChannel']=tf(u)
# Local angled top pocket in BB_Floor under rear channel, maintaining bottom shelf bearing.
# Pocket floor n=2 follows measured channel plane; no whole-floor tilt.
cut=tf(box(10,1127,2,580,25,40));s['BB_Floor']=old['BB_Floor'].cut(cut).removeSplitter();wood['BB_Floor']=s['BB_Floor']
# Front lockdown contact envelope: reference only, hardware/mount mechanism unchanged/HOLD.
front=box(0,-18,1,600,17.5,12).fuse(box(0,-.5,10,600,12.5,3)).removeSplitter();s['PF_LockdownGlassRetainer']=tf(front)
refs['PF_GlassPlane']=tf(box(0,0,3.9,600,L+4,.1))
# Same-plane commodity interface, all exact profiles/bores remain NULL.
for n,q in wood.items():ck('valid single wood '+n,q.isValid() and len(q.Solids)==1)
for n,q in s.items():ck('valid solid '+n,q.isValid() and len(q.Solids)>0)
changed=[n for n in s if n not in old or s[n].exportBrepToString()!=old[n].exportBrepToString()]
protected=[n for n in old if n not in changed and n not in retired]
ck('unrelated source geometry byte equivalent',all(old[n].exportBrepToString()==s[n].exportBrepToString() for n in protected),len(protected))
occupied={n:q for n,q in s.items() if n in actual(s) and not any(t in n for t in ['Cushion','Liner','Mask','Tool','Reserve','ToyZone','Screw','Bolt','Washer','Spacer','CrossDowel','Tether','Grill'])}
# Differential wood-vs-old occupied, intentional joint contacts have zero volume.
ck('new fixed wood nonpenetrating',not hits(wood,{n:q for n,q in occupied.items() if n not in wood and n not in ['CandidateGlass','PF_LockdownGlassRetainer']}),hits(wood,{n:q for n,q in occupied.items() if n not in wood and n not in ['CandidateGlass','PF_LockdownGlassRetainer']}))
results=[];monobs={n:q for n,q in occupied.items() if n!='BB_Display32'}
for dep,boss,label in [(75,65,'TCL_like'),(80,70,'generic80'),(80,55,'thin_boss_limit')]:
 for stack in [0,3,6,9,12]:
  for dz in [-15,0,15]:
   q,datum=tv(dep,boss,stack,dz);h=hits({'TV':q},monobs);results.append({'case':label,'stack':stack,'vertical':dz,'datum':datum,'pass':not h,'hits':h})
ck('TCL planning LOW NOMINAL HIGH with12mm',all(a['pass'] for a in results if a['case']=='TCL_like' and a['stack']==12),[a for a in results if a['case']=='TCL_like' and a['stack']==12])
ck('generic80 planning LOW NOMINAL HIGH with12mm',all(a['pass'] for a in results if a['case']=='generic80' and a['stack']==12))
# Front insertion envelope at HIGH; actual TV boss offsets still physically held.
monob={n:q for n,q in monobs.items() if not n.startswith(('BB_Acrylic','BB_GLASS_TOP'))}
q,dd=tv(80,70,12,15);b=q.BoundBox;path=box(b.XMin,b.YMin-600,b.ZMin,b.XLength,b.YLength+600,b.ZLength);hh=hits({'front_path':path},monob);ck('TV front removal HIGH',not hh,hh)
# Rear connector reserve below VESA, via existing functional plate opening.
connector=box(220,1198,910,100,80,60);h=hits({'connector':connector},{n:q for n,q in occupied.items() if n not in ['BB_Display32']});ck('connector reserve through opening',not h,h);refs['BB_ConnectorReserve']=connector
# Acrylic rigid capture and tilt route; mechanical fit expansion/flatness remain HOLD.
barriers={n:s[n] for n in ['BB_SideL','BB_SideR','BB_Top','BB_GLASS_BOTTOM_SEAT','BB_GLASS_TOP_RETAINER']}
for axis in range(3):
 for sign in [-1,1]:
  v=[0,0,0];v[axis]=sign*4;q=s['BB_AcrylicFront'].copy();q.translate(V(*v));ck('acrylic containment '+str(v),bool(hits({'acrylic':q},barriers)))
acobs={n:q for n,q in occupied.items() if n not in ['BB_AcrylicFront','BB_GLASS_TOP_RETAINER']};ah=[]
for a in range(11):
 q=shift(s['BB_AcrylicFront'],z=1);q.rotate(V(300,1116,841),V(1,0,0),a);ah+=hits({'acrylic_tilt':q},acobs)
q=shift(s['BB_AcrylicFront'],z=1);q.rotate(V(300,1116,841),V(1,0,0),10);q.translate(V(0,0,6));b=q.BoundBox;ah+=hits({'acrylic_front':box(b.XMin,b.YMin-300,b.ZMin,b.XLength,b.YLength+300,b.ZLength)},acobs);ck('acrylic front removal',not ah,ah)
# Doors with lower grills and optional fans, no routing anchors or predefined loops.
doorresults=[];newfixed={n:q for n,q in occupied.items() if n.startswith('BB_') and not n.startswith(('BB_Door','BB_Fan','BB_LowerGrill','BB_Piano','BB_Center','BB_Passive','BB_Cam'))}
for side in ['L','R']:
 mov={n:q for n,q in (s|variants).items() if n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Lower','BB_PianoLeafDoor'))}
 for a in [0,1,5,15,30,45,60,75,90,100]:doorresults.append({'side':side,'angle':a,'hits':hits(door_pose(mov,side,a),newfixed)})
ck('rear door active fan sweeps',not any(a['hits'] for a in doorresults),[a for a in doorresults if a['hits']])
ck('speaker90 clears passive and active',not hits({n:s[n] for n in ['BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']},{n:q for n,q in occupied.items() if 'SpeakerEnvelope' not in n}|variants),hits({n:s[n] for n in ['BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']},{n:q for n,q in occupied.items() if 'SpeakerEnvelope' not in n}|variants))
# Rear lock access unaffected by low station removal/addition.
lp={side+k:q for side,x in [('L',130),('R',470)] for k,q in route(x,1260).items()};lockobs={n:q for n,q in wood.items() if not n.startswith('BB_Door')};
for side in ['L','R']:lockobs.update(door_pose({n:q for n,q in (wood|variants).items() if n.endswith(side) and n.startswith(('BB_Door','BB_Lower'))},side,100))
lh=hits(lp,lockobs);ck('locks accessible',not lh,lh)
# Glass routes: exact extrusion along derived slope, with lockdown removed only.
glassobs={n:q for n,q in occupied.items() if n not in ['CandidateGlass','PF_LockdownGlassRetainer']};gh=hits({'glass':s['CandidateGlass']},glassobs);ck('playfield glass installed',not gh,gh)
sweep=tf(box(12.5,-L,4,575,2*L,5));gh=hits({'forward_glass_sweep':sweep},glassobs);ck('playfield glass forward continuous sweep',not gh,gh)
for name,v in [('left',[-3,0,0]),('right',[3,0,0]),('front',[0,-4*ca,-4*sa]),('rear',[0,4*ca,4*sa]),('up',[0,-3*sa,3*ca]),('down',[0,3*sa,-3*ca])]:
 q=s['CandidateGlass'].copy();q.translate(V(*v));ck('playfield glass positive stop '+name,bool(hits({'glass':q},{n:s[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','BB_PFRearChannel','PF_LockdownGlassRetainer']})))
# Differential rotation: additions/changed geometry only, old protected paths inherit previous proof.
fixed={n:q for n,q in actual(s).items() if not n.startswith('BB_') and n not in ['CandidateGlass','PF_BackboxCheckEnvelope'] and 'MATRIX' not in n.upper()}
mov={n:q for n,q in s.items() if n in changed and n.startswith('BB_') and n!='BB_Floor' and not any(t in n for t in ['Liner','Mask','Screw','Bolt','Washer','Spacer','Grill'])};mov.update(variants)
fold=[]
for a in [0,.25,.5,1,2,5,10,15,30,45,60,75,90]:fold.append({'angle':a,'hits':hits(transform(mov,angle=a,axis=WPC),fixed)})
ck('fold required samples',not any(a['hits'] for a in fold),[a for a in fold if a['hits']])
try:fc=certify(mov,fixed,0,90,WPC);ck('fold continuous certificate',True,len(fc['intervals']))
except AssertionError as e:fc={'error':str(e)};ck('fold continuous certificate',False,str(e))
# Independently all populated backbox geometry vs the fixed side-channel pair.
allbb={n:q for n,q in actual(s).items() if n.startswith('BB_') and not any(t in n for t in ['Reserve','ToyZone','Liner','Mask','Tether'])}
ch={n:s[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR']}
try:cc=certify(allbb,ch,0,90,WPC);ck('all backbox vs fixed side channels continuous',True,len(cc['intervals']))
except AssertionError as e:ck('all backbox vs fixed side channels continuous',False,str(e))
# Actual changed wood and commodity volumes; no box-based mass.
save('candidate',s);save('variants',variants|refs)
dump('geometry-validation',{'pass':all(a['pass'] for a in checks),'checks':checks,'changed':changed,'retired':retired,'wood_changed':list(wood),'TV_depth_cases':results,'glass_angle_derived_deg':math.degrees(angle),'glass_local_origin_tn':[t0,n0],'glass_rear_edge_world':bb(s['CandidateGlass']),'fold':fold,'fold_certificate':fc,'doors':doorresults,'source_sha256':hashlib.sha256((R/C['source']).read_bytes()).hexdigest(),'manufacturing_release':False,'actual_TCL_boss_compatibility':'HOLD_PHYSICAL_MEASUREMENT'})
dump('geometry-inventory',{'parts':{n:{'bounds_mm':bb(q),'volume_mm3':q.Volume} for n,q in s.items()},'wood':list(wood),'reference_parts':list(variants|refs)})
for n,q in wood.items():q.exportBrep(str(O/(n+'.brep')))
print('V342_NATIVE',all(a['pass'] for a in checks),flush=True)

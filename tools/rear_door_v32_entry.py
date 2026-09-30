"""Keyed downward rear door study. CERN-OHL-S-2.0; hardware/load not certified."""
import hashlib,json,math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/rear-door-v32';O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cp=R/'config/rear_door_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());srp=R/c['shell_report'];sr=json.loads(srp.read_text());sp=R/r['saved_proposal']['path'];ssp=R/sr['saved_proposal']['path']
for report,path in [(r,sp),(sr,ssp)]:assert all(x['pass'] for x in report['checks']) and sha(path)==report['saved_proposal']['sha256']
inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,srp,sp,ssp,Path(__file__).resolve()]}
d=A.openDocument(str(sp));sd=A.openDocument(str(ssp));scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};original={n:s.copy() for n,s in scene.items()}
retired=[n for n in scene if n.startswith(('CandidateRearReceiver','CandidateReceiverAnchor','CandidateRearCoverBolt'))]
for n in retired:del scene[n]
scene['REAR']=sd.getObject('REAR').Shape.copy();V=lambda *v:A.Vector(*v);axis=V(*c['hinge_axis_xyz_mm']);L=1308.1;checks=[];new={}
def box(x,y,z,w,t,h):return Part.makeBox(w,t,h,V(x,y,z))
def cy(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))
def cx(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(1,0,0))
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def hits(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if n==k:continue
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>.01:out.append({'part':n,'obstacle':k,'mm3':vol})
 return out
# Fresh door: fan holes retained, former four closure screw holes omitted.
door=box(102,L,54,396,12,329)
for x in (230,370):
 door=door.cut(cy(x,L-1,280,58,14))
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):door=door.cut(cy(x+dx,L-1,280+dz,2.25,14))
for n in scene:
 if n.startswith(('CandidateRearHandle','CandidateHandleBolt')):scene[n].translate(V(0,0,c['handle_z_mm']-130))
for x in (268,332):door=door.cut(cy(x,L-1,c['handle_z_mm'],2.25,14))
lx,lz=c['lock_center_xz_mm'];dia=c['lock_bore_diameter_mm_candidate'];flat=c['lock_bore_across_flats_mm_candidate']
def lock_profile(y,depth):return cy(lx,y,lz,dia/2,depth).common(box(lx-flat/2,y,lz-dia/2,flat,depth,dia))
door=door.cut(lock_profile(L-1,14));scene['REAR_DOOR']=door
new['CandidateKeyLockBody']=lock_profile(L-20,32).fuse(cy(lx,L+12,lz,11.5,2))
new['CandidateKeyLockShaft']=cy(lx,L-23,lz,3,3)
cam=box(lx-6,L-23,lz,12,3,c['lock_cam_length_mm_candidate']).cut(cy(lx,L-24,lz,3,5))
new['CandidateKeyLockCam']=cam
# Keeper face ahead of wood: locked cam is behind it; key turn points cam inward toward cabinet center.
new['CandidateLockKeeper']=box(lx-10,L-20,368,20,2,24)
fixed=['CandidateLockKeeper'];hinge_moving=[]
for i,x in enumerate(c['hinge_start_x_mm'],1):
 fixedleaf=box(x,L,24,48,2,26).fuse(box(x,L+2,48,48,14,4))
 for xx in [x,x+32]:fixedleaf=fixedleaf.fuse(cx(xx,axis.y,axis.z,4,16))
 fixedleaf=fixedleaf.cut(cx(x-1,axis.y,axis.z,2,50)).cut(cx(x+16,axis.y,axis.z,4.5,16)).removeSplitter()
 mobile=box(x,L+12,60,48,2,24).fuse(box(x+16.5,L+12,56,15,4,4)).fuse(cx(x+16.5,axis.y,axis.z,4,15)).cut(cx(x-1,axis.y,axis.z,2,50)).removeSplitter()
 for dx in (10,38):
  fixedleaf=fixedleaf.cut(cy(x+dx,L-1,36,2.25,4));mobile=mobile.cut(cy(x+dx,L+11,72,2.25,4))
  # Pilot positions remain a hardware-dependent schedule, not blind drills into unselected stock.
 new[f'CandidateHingeFixed{i}']=fixedleaf;new[f'CandidateHingeMoving{i}']=mobile;new[f'CandidateHingePin{i}']=cx(x,axis.y,axis.z,2,48)
 fixed.extend([f'CandidateHingeFixed{i}',f'CandidateHingePin{i}']);hinge_moving.append(f'CandidateHingeMoving{i}')
scene.update(new)
moving=[n for n in r['cover_moving_parts'] if n in scene]+hinge_moving+['CandidateKeyLockBody','CandidateKeyLockShaft','CandidateKeyLockCam']
obstacles={n:s for n,s in scene.items() if n not in moving}
installed=hits(new,{n:s for n,s in scene.items()});check('closed hardware clearance',not installed)
unlock_conf=[]
for a in range(0,91,2):
 s=cam.copy();s.rotate(V(lx,L-23,lz),V(0,1,0),-a);unlock_conf+=hits({'cam':s},{n:t for n,t in scene.items() if n not in ['CandidateKeyLockCam','CandidateKeyLockShaft']})
check('key cam 90 degree unlock sampled clear',not unlock_conf)
unlocked=cam.copy();unlocked.rotate(V(lx,L-23,lz),V(0,1,0),-90)
closed_unlocked={n:scene[n].copy() for n in moving};closed_unlocked['CandidateKeyLockCam']=unlocked
sweep_conf=[];poses={}
for a in range(0,c['opening_degrees']+1,c['sample_step_degrees']):
 pose={n:s.copy() for n,s in closed_unlocked.items()}
 for s in pose.values():s.rotate(axis,V(1,0,0),-a)
 for hit in hits(pose,obstacles):sweep_conf.append(dict(angle_deg=a,**hit))
 if a in [90,c['opening_degrees']]:poses[a]=pose
check('downward door sampled opening clear',not sweep_conf)
locked=cam.copy();locked.rotate(axis,V(1,0,0),-2)
locked_hits=hits({'locked_cam':locked},{'keeper':scene['CandidateLockKeeper'],'rear':scene['REAR']})
check('negative locked cam blocks opening',bool(locked_hits))
# PC packaging route tested with door open, not removed; 90-degree comparison exposes protruding hardware.
pc_results={}
for angle,pose in poses.items():
 pc={n:scene[n].copy() for n in ['PC_BASE','PC_ENVELOPE']};conf=[];obs={**{n:s for n,s in obstacles.items() if n not in pc},**pose}
 for xyz in [(0,0,38),(0,500,0)]:
  v=V(*xyz)
  for n,s in pc.items():
   b=s.BoundBox;sw=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength+v.y,b.ZLength+v.z);conf+=hits({n:sw},obs);s.translate(v)
 pc_results[str(angle)]=conf
check('PC exceptional route clears door at110',not pc_results[str(c['opening_degrees'])])
check('negative 90deg door obstructs PC route',bool(pc_results['90']))
# Support cable geometry: minimum straight length when taut at110, two symmetric sides.
# No taut support represented at closed angle: it must fold/slacken into a reserved side region.
restraints=[]
for x,door_x in [(90,110),(510,490)]:
 anchor=V(x,1324.1,200);end=V(door_x,1322.1,180)
 placement=A.Placement(V(0,0,0),A.Rotation(V(1,0,0),-c['opening_degrees']),axis)
 end=placement.multVec(end);dv=end-anchor
 restraints.append({'fixed_xyz_mm':[anchor.x,anchor.y,anchor.z],'door_closed_xyz_mm':[door_x,1322.1,180],'door_open_xyz_mm':[end.x,end.y,end.z],'taut_length_mm_candidate':dv.Length,'status':'REQUIRES_REAL_ANCHORS_LOAD_RATING_AND_CLOSED_STOW'})
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for stem in ['CandidateHingeFixed','CandidateHingeMoving']:
 reflected=scene[stem+'1'].transformGeometry(mirror)
 check(stem+' left right symmetry',reflected.cut(scene[stem+'2']).Volume+scene[stem+'2'].cut(reflected).Volume<1e-5)
check('valid single solids',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
check('frozen shelves sides PC unchanged',all(scene[n].cut(original[n]).Volume+original[n].cut(scene[n]).Volume<1e-6 for n in ['SIDE_L','SIDE_R','SHELF_1','SHELF_2','SHELF_3','PC_BASE','PC_ENVELOPE']))
check('retired closures absent',not any(n in scene for n in retired))
meshes={};saved_files={}
for label,shapes in [('closed',scene),('open',dict(scene,**poses[c['opening_degrees']]))]:
 out=A.newDocument('RearDoor'+label)
 for n,s in shapes.items():
  o=out.addObject('PartDesign::Feature',n);o.Shape=s;src=d.getObject(n);o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(src,'PartCode','') if src else '';o.Label=o.PartCode or n
 out.recompute();p=O/('rear-door-'+label+'.FCStd');out.saveAs(str(p));A.closeDocument(out.Name);saved=A.openDocument(str(p));saved.recompute();actual={o.Name:o.Shape for o in saved.Objects if hasattr(o,'Shape')}
 check(label+' saved solids valid and identical',set(actual)==set(shapes) and all(s.isValid() and len(s.Solids)==1 and s.cut(shapes[n]).Volume+shapes[n].cut(s).Volume<1e-5 for n,s in actual.items()))
 saved_files[label]={'path':str(p.relative_to(R)),'sha256':sha(p),'solids':len(actual)};mesh=[]
 for n,s in actual.items():
  if n in moving or n in fixed or n in ['REAR','PC_BASE','PC_ENVELOPE']:
   vs,fs=s.tessellate(.7);mesh.append({'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':fs})
 meshes[label]=mesh;A.closeDocument(saved.Name)
check('input files unchanged',all(sha(R/n)==h for n,h in inputs.items()))
report={'manufacturing_ready':False,'config':c,'source_hashes':inputs,'checks':checks,'closed_conflicts':installed,'cam_unlock_conflicts':unlock_conf,'door_sweep_conflicts':sweep_conf,'locked_opening_rejected':locked_hits,'pc_route_conflicts':pc_results,'retired_objects':retired,'moving_objects':moving,'support_candidates':restraints,'saved_proposals':saved_files,'unverified':['Actual hinges/lock/cam/keeper fasteners and detailed wood pilots','Both support straps/anchors, load proof and folded stow','Fan harness slack/bend radius/connector placement','Sweep between2-degree samples and human access','Real legs/room/ground clearance; no use of open door as workbench','All prior safety/thermal/manufacturing qualifications remain open']}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(O/'mesh.json').write_text(json.dumps(meshes)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('REAR_DOOR_PASS',len(checks),'checks;',len(scene),'solids per pose; CNC HOLD')
A.closeDocument(d.Name);A.closeDocument(sd.Name)

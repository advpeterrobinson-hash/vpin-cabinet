"""Fixed fan / direct rear connector interface study. CERN-OHL-S-2.0; mechanical packaging only."""
import json,hashlib
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/fixed-rear-services-v32';O.mkdir(parents=True,exist_ok=True);cp=R/'config/fixed_rear_services_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/r['saved_proposals']['closed']['path'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(sp)==r['saved_proposals']['closed']['sha256'] and all(x['pass'] for x in r['checks']);inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,Path(__file__).resolve(),R/'config/lockdown_interface_v32.json']}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};old={n:s.copy() for n,s in scene.items()};checks=[];new={};L=1308.1;V=lambda *v:A.Vector(*v)
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def box(x,y,z,w,t,h):return Part.makeBox(w,t,h,V(x,y,z))
def cy(x,y,z,rad,h):return Part.makeCylinder(rad,h,V(x,y,z),V(0,1,0))
def hits(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if n==k:continue
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>.01:out.append({'part':n,'obstacle':k,'mm3':vol})
 return out
# No fan/fastener openings left in door; keep handle and keyed lock only.
door=box(102,L,54,396,12,329)
for x in (268,332):door=door.cut(cy(x,L-1,190,2.25,14))
lx,lz=r['config']['lock_center_xz_mm'];rad=r['config']['lock_bore_diameter_mm_candidate']/2;flat=r['config']['lock_bore_across_flats_mm_candidate'];door=door.cut(cy(lx,L-1,lz,rad,14).common(box(lx-flat/2,L-1,lz-rad,flat,14,2*rad)));scene['REAR_DOOR']=door
fixed_fans=[]
for n in list(scene):
 if n.startswith(('FAN_','CandidateFan')):
  fixed_fans.append(n)
  dy=-18 if n.startswith('FAN_') or 'Inner' in n or n.endswith('Nut') else -12
  scene[n].translate(V(0,dy,220))
# Fixed panel18 replaces door12: longer candidate bolts required.
for x,z in c['fan_centers_xz_mm']:
 scene['REAR']=scene['REAR'].cut(cy(x,L-19,z,58,20))
 for i,(dx,dz) in enumerate([(dx,dz) for dx in (-52.5,52.5) for dz in (-52.5,52.5)],1):
  xx,zz=x+dx,z+dz;scene['REAR']=scene['REAR'].cut(cy(xx,L-19,zz,2.25,20));name=f'CandidateFanBolt{x}_{i}';under=L+2.5;length=c['fan_bolt_length_mm_candidate'];scene[name]=cy(xx,under-length,zz,2,length).fuse(cy(xx,under,zz,4,3))
  nut=scene[name+'Nut'].BoundBox;check(name+' full candidate nut engagement',under-length<=nut.YMin)
check('fan top below backbox base with18.9mm nominal gap',abs(scene['BACKBOX_BASE'].BoundBox.ZMin-560-18.9)<1e-5)
# Only the internal enclosure opening is modeled while direct connector footprints await dimensions.
def window(spec,y,depth):
 x,z,w,h=spec;rr=c['window_corner_radius_mm_candidate'];s=box(x+rr,y,z,w-2*rr,depth,h).fuse(box(x,y,z+rr,w,depth,h-2*rr))
 for xx in (x+rr,x+w-rr):
  for zz in (z+rr,z+h-rr):s=s.fuse(cy(xx,y,zz,rr,depth))
 return s.removeSplitter()
# User correction: no carrier plates, oversized panel windows or their four-hole patterns.
# Do not substitute dimensions from visually similar connectors. An unset footprint leaves wood intact.
assert all(c['direct_panel_io'][key]['footprint'] is None for key in ('mains','ethernet')), 'Implement and validate selected footprint before enabling machining'
rear_before_io=scene['REAR'].copy()
check('direct IO awaits measured footprints with no substitute openings',all(scene['REAR'].isInside(V(x,L-9,z),1e-6,True) for x,z in [c['direct_panel_io'][key]['center_xz_mm'] for key in ('mains','ethernet')]))
# Separate covered mains enclosure: candidate mechanical shell, not an electrical rating.
x,y,z,w,t,h=c['mains_enclosure_xyzwhd_mm'];enc=box(x,y,z,w,t,h).cut(box(x+2,y+2,z+2,w-4,t-4,h-4)).cut(window(c['mains_enclosure_access_xzwh_mm'],L-20.1,4))
new['CandidateMainsEnclosure']=enc
for name in ['MAINS_RESERVED','RJ45_RESERVED']:scene.pop(name,None)
# Receiver mounting draft follows source image and keeps existing shared center.
for x,z in c['lockdown_outer_axes_xz_mm']:scene['FRONT']=scene['FRONT'].cut(cy(x,-1,z,c['lockdown_hole_diameter_mm_draft']/2,20))
# Floor ventilation follows the fixed rear exhaust; remove unassigned auxiliary holes.
floor=box(18,18,18,564,L-36,18)
sx,sy,diam=c['floor']['subwoofer_opening_xy_diameter_mm'];floor=floor.cut(Part.makeCylinder(diam/2,20,V(sx,sy,17)))
for j,(x,y,w,h) in enumerate(c['floor']['intake_xywh_mm'],1):
 floor=floor.cut(box(x,y,17,w,h,20))
 # Removable underside filter-holder frame, medium and fasteners not yet specified.
 new[f'CandidateIntakeFilterFrame{j}']=box(x-10,y-10,10,w+20,h+20,8).cut(box(x,y,9,w,h,10))
scene['FLOOR']=floor
check('four unassigned front floor bores omitted',all(floor.isInside(V(x,90,27),1e-6,True) for x in [185,245,305,365]))
check('both intake centers open',all(not floor.isInside(V(x+w/2,y+h/2,27),1e-6,True) for x,y,w,h in c['floor']['intake_xywh_mm']))
scene.update(new);installed=hits({n:scene[n] for n in fixed_fans+list(new)},scene);check('fixed fans and internal enclosure no installed collisions',not installed)
# Door closes with key and opens without any fan harness moving with it.
moving=[n for n in r['moving_objects'] if n not in fixed_fans];obs={n:s for n,s in scene.items() if n not in moving};unlocked={n:scene[n].copy() for n in moving};cam=unlocked['CandidateKeyLockCam'];cam.rotate(V(lx,L-23,lz),V(0,1,0),-90);pivot=V(*r['config']['hinge_axis_xyz_mm']);conf=[];poses={}
for angle in range(0,111,2):
 pose={n:s.copy() for n,s in unlocked.items()}
 for s in pose.values():s.rotate(pivot,V(1,0,0),-angle)
 for hit in hits(pose,obs):conf.append(dict(angle_deg=angle,**hit))
 if angle in (90,110):poses[angle]=pose
check('door sampled opening clears fixed rear services',not conf)
pc_results={}
for angle,pose in poses.items():
 pc={n:scene[n].copy() for n in ['PC_BASE','PC_ENVELOPE']};ob={**{n:s for n,s in obs.items() if n not in pc},**pose};out=[]
 for xyz in [(0,0,38),(0,500,0)]:
  v=V(*xyz)
  for n,s in pc.items():
   b=s.BoundBox;out+=hits({n:box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength+v.y,b.ZLength+v.z)},ob);s.translate(v)
 pc_results[str(angle)]=out
check('90 degree PC route still rejected by lock geometry',any(x['obstacle'].startswith('CandidateKeyLock') for x in pc_results['90']));check('PC route clear at110',not pc_results['110'])
# Low rear opening and frame are retained; interface cuts stay above door.
check('fan frames leave57mm above closed door',440-scene['REAR_DOOR'].BoundBox.ZMax==57)
check('no intermediate IO plates or oversized wood cuts',not any('Carrier' in n for n in scene) and scene['REAR'].cut(rear_before_io).Volume+rear_before_io.cut(scene['REAR']).Volume<1e-6)
check('internal enclosure separated from closed door',not hits(new,{'door':scene['REAR_DOOR']}))
check('frozen sides shelves and PC unchanged',all(scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume<1e-6 for n in ['SIDE_L','SIDE_R','SHELF_1','SHELF_2','SHELF_3','PC_BASE','PC_ENVELOPE']))
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for left,right in [('FAN_230','FAN_370'),('FLOOR','FLOOR')]:
 reflected=scene[left].transformGeometry(mirror)
 check(left+' mirror symmetry',reflected.cut(scene[right]).Volume+scene[right].cut(reflected).Volume<1e-5)
fan_tools=[]
for x,z in c['fan_centers_xz_mm']:
 for dx in (-52.5,52.5):
  for dz in (-52.5,52.5):
   fan_tools+=hits({'outer_driver':cy(x+dx,L+5.5,z+dz,8,100)},scene)
   fan_tools+=hits({'inner_driver':cy(x+dx,1159.4,z+dz,8,100).cut(cy(x+dx,1158.4,z+dz,3,102))},scene)
check('candidate fan tool access from both sides',not fan_tools)
check('valid single solids',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
# Negative: simply moving fans toZ520 would hit the backbox base.
bad=scene['FAN_230'].copy();bad.translate(V(0,0,20));check('reject fans20mm higher hitting backbox base',bool(hits({'raised_fan':bad},{'BACKBOX_BASE':scene['BACKBOX_BASE']})))
mesh={};saved_files={}
for label,shapes in [('closed',scene),('open90',dict(scene,**poses[90])),('open110',dict(scene,**poses[110]))]:
 out=A.newDocument('RearServices'+label)
 for n,s in shapes.items():
  o=out.addObject('PartDesign::Feature',n);o.Shape=s;src=d.getObject(n);o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(src,'PartCode','') if src else '';o.Label=o.PartCode or n
 out.recompute();p=O/(label+'.FCStd');out.saveAs(str(p));A.closeDocument(out.Name);saved=A.openDocument(str(p));saved.recompute();actual={o.Name:o.Shape for o in saved.Objects if hasattr(o,'Shape')}
 check(label+' reopened shapes and identities',set(actual)==set(shapes) and all(s.isValid() and len(s.Solids)==1 and s.cut(shapes[n]).Volume+shapes[n].cut(s).Volume<1e-5 and saved.getObject(n).PartCode==getattr(d.getObject(n),'PartCode','') for n,s in actual.items()))
 saved_files[label]={'path':str(p.relative_to(R)),'sha256':sha(p),'solids':len(actual)};A.closeDocument(saved.Name)
check('source files unchanged',all(sha(R/p)==h for p,h in inputs.items()))
report={'manufacturing_ready':False,'config':c,'source_hashes':inputs,'checks':checks,'installed_conflicts':installed,'door_sweep_conflicts':conf,'fan_tool_conflicts':fan_tools,'pc_route_conflicts':pc_results,'fixed_fan_objects':fixed_fans,'door_moving_objects':moving,'saved_proposals':saved_files,'unverified':['Fan thermal/noise/guard qualification and fixed wiring','Direct inlet/RJ45 cutouts and flange screw pattern; suitability for18mm plywood, local relief if required; enclosure mounting/ratings','Electrical protection PE and strain relief; no wiring design','Receiver envelope, tongues, bar profile and real fastener stack','Real door hinge/lock hardware, free resting angle/felt; optional limiters','All remaining side/playfield/SSF/floor manufacturing gates']};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']];print('FIXED_REAR_SERVICES_PASS',len(checks),'checks;',len(scene),'solids per pose; CNC HOLD');A.closeDocument(d.Name)

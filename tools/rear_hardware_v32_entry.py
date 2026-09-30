"""Rear hardware study. CERN-OHL-S-2.0; no structural/protection certification."""
import hashlib,json
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/rear-hardware-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/rear_hardware_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/r['saved_proposal']['path'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sp)==r['saved_proposal']['sha256'] and all(x['pass'] for x in r['checks'])
for p,h in r['source_hashes'].items():assert sha(R/p)==h,p
inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,Path(__file__).resolve()]}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};old={n:s.copy() for n,s in scene.items()};new={};fixed=[];moving=['REAR_DOOR','FAN_230','FAN_370'];bolts=[];checks=[];holes=[];thread_pairs=set()
L=r['config']['body']['length_mm'];T=18;cover_t=r['config']['rear']['cover_thickness_mm'];inside=L-T
V=lambda x,y,z:A.Vector(x,y,z)
def box(x,y,z,w,t,h):return Part.makeBox(w,t,h,V(x,y,z))
def cyl(x,y,z,rad,depth):return Part.makeCylinder(rad,depth,V(x,y,z),V(0,1,0))
def ring(x,y,z,rad,depth,hole):return cyl(x,y,z,rad,depth).cut(cyl(x,y-1,z,hole,depth+2))
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def hits(parts,obs,exempt=()):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if n==k or (n,k) in exempt or (k,n) in exempt:continue
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>.01:out.append({'part':n,'obstacle':k,'mm3':v})
 return out
b=c['cover_bolt'];a=c['receiver']
for i,(x,z) in enumerate(r['config']['rear']['cover_fasteners_xz_mm'],1):
 plate_y=inside-a['plate_thickness_mm'];nut_y=plate_y-a['nut_height_mm'];name=f'CandidateRearReceiver{i}'
 plate=box(x-a['plate_width_mm']/2,plate_y,z-a['plate_height_mm']/2,a['plate_width_mm'],a['plate_thickness_mm'],a['plate_height_mm']).fuse(cyl(x,nut_y,z,a['nut_outer_diameter_mm']/2,a['nut_height_mm']))
 plate=plate.cut(cyl(x,nut_y-1,z,b['diameter_mm']/2,inside-nut_y+2))
 scene['REAR']=scene['REAR'].cut(cyl(x,inside-1,z,2.75,T+2));holes.append({'part':'REAR','xyz_mm':[x,inside,z],'diameter_mm':5.5,'depth_mm':T,'operation':'THROUGH','status':'CANDIDATE'})
 for j,dz in enumerate(a['anchor_offsets_z_mm'],1):
  zz=z+dz;plate=plate.cut(cyl(x,plate_y-1,zz,1.75,a['plate_thickness_mm']+2))
  scene['REAR']=scene['REAR'].cut(cyl(x,inside-1,zz,a['pilot_diameter_mm']/2,a['pilot_depth_mm']+1))
  sn=f'CandidateReceiverAnchor{i}_{j}';new[sn]=cyl(x,plate_y,zz,a['anchor_diameter_mm']/2,a['anchor_length_mm']).fuse(cyl(x,plate_y-2,zz,3,2));fixed.append(sn);thread_pairs.add((sn,'REAR'))
  holes.append({'part':'REAR','xyz_mm':[x,inside,zz],'diameter_mm':a['pilot_diameter_mm'],'depth_mm':a['pilot_depth_mm'],'operation':'BLIND_PILOT','status':'HOLD_SCREW_AND_STOCK'})
 new[name]=plate;fixed.append(name)
 under=L+cover_t+b['washer_thickness_mm'];sn=f'CandidateRearCoverBolt{i}'
 new[sn]=cyl(x,under-b['length_mm'],z,b['diameter_mm']/2,b['length_mm']).fuse(cyl(x,under,z,b['head_diameter_mm']/2,b['head_height_mm']));bolts.append(sn)
 new[sn+'Washer']=ring(x,L+cover_t,z,b['washer_diameter_mm']/2,b['washer_thickness_mm'],2.75);bolts.append(sn+'Washer')
 check(name+' full nominal nut engagement',under-b['length_mm']<=nut_y)
check('blind pilots retain 4mm exterior skin',T-a['pilot_depth_mm']>=4)
check('receiver screw tip leaves wood beyond it',a['anchor_length_mm']-a['plate_thickness_mm']<a['pilot_depth_mm'])
g=c['guards'];fb=c['fan_bolt'];fan_records=[]
for x,z in r['config']['rear']['fan_centers_xz_mm']:
 fan_name='FAN_'+str(x);fy=scene[fan_name].BoundBox.YMin;positions=[('Inner',fy-g['thickness_mm']),('Outer',L+cover_t)]
 for label,y in positions:
  gn=f'CandidateFanGuard{x}{label}';guard=box(x-60,y,z-60,120,g['thickness_mm'],120)
  for dz in g['slot_center_offsets_z_mm']:
   rad=g['slot_width_mm']/2;half=g['slot_length_mm']/2-rad
   slot=box(x-half,y-1,z+dz-rad,2*half,g['thickness_mm']+2,2*rad).fuse(cyl(x-half,y-1,z+dz,rad,g['thickness_mm']+2)).fuse(cyl(x+half,y-1,z+dz,rad,g['thickness_mm']+2))
   guard=guard.cut(slot)
  for dx in (-52.5,52.5):
   for dz in (-52.5,52.5):guard=guard.cut(cyl(x+dx,y-1,z+dz,2.25,g['thickness_mm']+2))
  new[gn]=guard;moving.append(gn)
 for i,(dx,dz) in enumerate([(dx,dz) for dx in (-52.5,52.5) for dz in (-52.5,52.5)],1):
  xx,zz=x+dx,z+dz;scene[fan_name]=scene[fan_name].cut(cyl(xx,fy-1,zz,2.25,27))
  under=L+cover_t+g['thickness_mm']+1;sn=f'CandidateFanBolt{x}_{i}';ny=fy-g['thickness_mm']-1-fb['nut_height_mm']
  new[sn]=cyl(xx,under-fb['length_mm'],zz,2,fb['length_mm']).fuse(cyl(xx,under,zz,4,3))
  new[sn+'OuterWasher']=ring(xx,under-1,zz,4.5,1,2.25)
  new[sn+'InnerWasher']=ring(xx,ny+fb['nut_height_mm'],zz,4.5,1,2.25)
  new[sn+'Nut']=ring(xx,ny,zz,4,fb['nut_height_mm'],2)
  moving.extend([sn,sn+'OuterWasher',sn+'InnerWasher',sn+'Nut']);check(sn+' full nominal nut engagement',under-fb['length_mm']<=ny)
 # Open area is gross slot geometry only, not fan-system airflow.
 slot_area=len(g['slot_center_offsets_z_mm'])*((g['slot_length_mm']-g['slot_width_mm'])*g['slot_width_mm']+3.141592653589793*(g['slot_width_mm']/2)**2)
 fan_records.append({'x_mm':x,'z_mm':z,'gross_plate_open_fraction':slot_area/120**2,'protection_certified':False,'airflow_validated':False})
h=c['handle'];x1,x2=h['centers_x_mm'];z=h['z_mm'];sec=h['section_mm'];hy=L+cover_t;handle=box(x1-sec/2,hy,z-sec/2,sec,h['stand_off_mm'],sec).fuse(box(x2-sec/2,hy,z-sec/2,sec,h['stand_off_mm'],sec)).fuse(box(x1-sec/2,hy+h['stand_off_mm'],z-sec/2,x2-x1+sec,h['bar_depth_mm'],sec))
for i,x in enumerate((x1,x2),1):
 scene['REAR_DOOR']=scene['REAR_DOOR'].cut(cyl(x,L-1,z,2.25,cover_t+2));handle=handle.cut(cyl(x,hy-1,z,2,h['thread_pocket_depth_mm']+1))
 under=L-1;sn=f'CandidateHandleBolt{i}';new[sn]=cyl(x,under,z,2,h['bolt_length_mm']).fuse(cyl(x,under-3,z,4,3));new[sn+'Washer']=ring(x,L-1,z,4.5,1,2.25);moving.extend([sn,sn+'Washer'])
 holes.append({'part':'REAR_DOOR','xyz_mm':[x,L,z],'diameter_mm':4.5,'depth_mm':cover_t,'operation':'THROUGH','status':'HOLD_HANDLE_PATTERN'})
new['CandidateRearHandle']=handle;moving.append('CandidateRearHandle');scene.update(new)
installed=hits(new,scene,thread_pairs);check('new hardware installed clearance except declared wood thread engagement',not installed)
# Individual removal paths, then cover assembly moves as one unit after the four cover bolts are out.
def sweep(shape,dy):
 pieces=[shape]
 for f in shape.Faces:
  try:
   v=f.extrude(V(0,dy,0))
   if v.Volume>1e-6:pieces.append(v)
  except Part.OCCError:pass
 return Part.makeCompound(pieces)
obs={n:s for n,s in scene.items() if n not in moving and n not in bolts}
removal=hits({n:sweep(scene[n],c['service']['cover_withdrawal_mm']) for n in moving},obs);check('continuous cover assembly withdrawal after four bolts removed',not removal)
# Shafts pass through mating threads during axial withdrawal: exclude only their own receiver.
bolt_paths=[];tools=[]
for i,(x,z) in enumerate(r['config']['rear']['cover_fasteners_xz_mm'],1):
 names=[f'CandidateRearCoverBolt{i}',f'CandidateRearCoverBolt{i}Washer'];ob={n:s for n,s in scene.items() if n not in names and n!=f'CandidateRearReceiver{i}'}
 bolt_paths+=hits({n:sweep(scene[n],c['service']['bolt_withdrawal_mm']) for n in names},ob)
 tool=cyl(x,L+cover_t+1+b['head_height_mm'],z,c['service']['tool_radius_mm'],c['service']['tool_length_mm']);tools+=hits({'driver':tool},scene)
check('four exterior screw withdrawals clear',not bolt_paths);check('four exterior driver corridors clear',not tools)
retained=hits({'cover_moved_sideways':scene['REAR_DOOR'].translated(V(1,0,0))},{n:scene[n] for n in bolts if not n.endswith('Washer')});check('negative retained bolts block cover lateral movement',bool(retained))
check('negative through pilot violates exterior skin',T-19<4)
# Keep fixed additions out of the already screened exceptional PC removal.
pc={n:scene[n].copy() for n in ['PC_BASE','PC_ENVELOPE']};pc_conf=[]
for xyz in [(0,0,38),(0,500,0)]:
 v=V(*xyz)
 for n,s in pc.items():
  bb=s.BoundBox;sw=box(bb.XMin,bb.YMin,bb.ZMin,bb.XLength,bb.YLength+v.y,bb.ZLength+v.z);pc_conf+=hits({n:sw},{k:scene[k] for k in fixed});s.translate(v)
check('fixed receivers preserve exceptional PC route',not pc_conf)
check('frozen shelves sides and PC unchanged',all(scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume<1e-6 for n in ['SIDE_L','SIDE_R','SHELF_1','SHELF_2','SHELF_3','PC_BASE','PC_ENVELOPE']))
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for left,right in [('CandidateRearReceiver1','CandidateRearReceiver2'),('CandidateRearReceiver3','CandidateRearReceiver4'),('CandidateFanGuard230Inner','CandidateFanGuard370Inner'),('CandidateFanGuard230Outer','CandidateFanGuard370Outer'),('CandidateRearHandle','CandidateRearHandle')]:
 reflected=scene[left].transformGeometry(mirror)
 check(left+' reflected counterpart',reflected.cut(scene[right]).Volume+scene[right].cut(reflected).Volume<1e-5)
check('all shapes valid single solids',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
out=A.newDocument('RearHardwareV32')
for n,s in scene.items():
 o=out.addObject('PartDesign::Feature',n);o.Shape=s;src=d.getObject(n);o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(src,'PartCode','') if src else '';o.Label=o.PartCode or n
out.recompute();p=O/'rear-hardware-study.FCStd';out.saveAs(str(p));A.closeDocument(out.Name);saved=A.openDocument(str(p));saved.recompute();actual={o.Name:o.Shape for o in saved.Objects if hasattr(o,'Shape')}
check('saved geometry valid and identical',set(actual)==set(scene) and all(s.isValid() and len(s.Solids)==1 and s.cut(scene[n]).Volume+scene[n].cut(s).Volume<1e-5 for n,s in actual.items()))
check('saved permanent identities preserved',all(saved.getObject(n).PartCode==getattr(d.getObject(n),'PartCode','') for n in old))
check('all source bytes preserved',all(sha(R/n)==h for n,h in inputs.items()))
mesh=[]
for n in ['REAR','REAR_DOOR']+list(new):
 vs,fs=actual[n].tessellate(.5);mesh.append({'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':fs})
(O/'mesh.json').write_text(json.dumps(mesh)+'\n')
report={'manufacturing_ready':False,'config':c,'source_hashes':inputs,'checks':checks,'installed_conflicts':installed,'cover_removal_conflicts':removal,'bolt_withdrawal_conflicts':bolt_paths,'driver_conflicts':tools,'pc_conflicts':pc_conf,'holes':holes,'fans':fan_records,'fixed_parts':fixed,'cover_moving_parts':moving,'removed_first':bolts,'saved_proposal':{'path':str(p.relative_to(R)),'sha256':sha(p),'solids':len(scene)},'unverified':['Actual fastener/receiver manufacture and loads; no thread helix/torque proof','Guard access/protection and thermal/acoustic performance','Handle attachment and holding load','Low voltage fan cable slack/disconnect; no harness geometry','Actual hand access and safe supported removal','Unchanged side/lockdown/playfield/SSF and manufacturing gates']}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('REAR_HARDWARE_PASS',len(checks),'checks;',len(scene),'solids; CNC HOLD')
A.closeDocument(saved.Name);A.closeDocument(d.Name)

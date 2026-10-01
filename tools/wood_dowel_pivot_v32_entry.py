"""Owner final wooden lift-out pivot only. CERN-OHL-S-2.0."""
import FreeCAD as A
import Part
import json, math, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]; O=R/'exports/generated/wood-dowel-pivot-v32'; O.mkdir(parents=True,exist_ok=True)
c=json.loads((R/'config/wood_dowel_pivot_v32.json').read_text()); V=A.Vector
source=R/'exports/generated/service-correction-v32/play.FCStd'
d=A.openDocument(str(source));d.recompute()
original={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
old=json.loads((R/'exports/generated/service-correction-v32/validation.json').read_text())['review']
retired=[n for n in original if n.startswith('PF_') and n!='PF_BackboxCheckEnvelope' or n.startswith('MONITOR_')]
scene={n:s.copy() for n,s in original.items() if n not in retired}
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(1,0,0))
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
# Remove only holes owned by rejected pivot; preserve buttons and all other cuts.
for side,x in [('L',0),('R',582)]:
 s=scene['SIDE_'+side]
 for y,z,r in [(*old['pivot_xyz_mm'][1:],5.25),(*old['receiver_yz_mm'],4.25)]:s=s.fuse(cyl(x,y,z,r,18)).removeSplitter()
 scene['SIDE_'+side]=s
alpha=math.radians(old['closed_slope_deg']); bz=400.05+45*math.tan(alpha)-12-55*math.cos(alpha)
def tf(s):
 s=s.copy();s.rotate(V(),V(1,0,0),math.degrees(alpha));s.translate(V(0,45,bz));return s
r=c['wood_dowel_diameter_mm']/2; ay=c['axis_local_y_mm']; az=c['base_bottom_local_z_mm']-r
pivot=tf(Part.Vertex(V(300,ay,az))).Vertexes[0].Point
py,pz=pivot.y,pivot.z
scene['PF_BasePlywood']=tf(box(c['base_x_mm'],20,c['base_bottom_local_z_mm'],c['base_width_mm'],c['base_length_mm'],18))
scene['PF_WoodDowel']=cyl(20,py,pz,r,560)
# VESA reference envelope directly on the single flat base, not pivot hardware.
scene['PF_VESAEnvelope']=tf(box(200,360,4,200,250,8))
for side,x in [('L',18),('R',564)]:
 rr=r+c['cradle_radial_clearance_mm']; w=c['cradle_width_y_mm']; height=pz+24-36
 support=box(x,py-w/2,36,18,w,height)
 support=support.cut(cyl(x-1,py,pz+c['cradle_radial_clearance_mm'],rr,20)).cut(box(x-1,py-rr,pz+c['cradle_radial_clearance_mm'],20,rr*2,26)).removeSplitter()
 scene['PF_OpenCradle'+side]=support
# Four purchased saddle straps, each two ears and a lower semicircular band.
for i,x in enumerate(c['strap_x_mm'],1):
 band=cyl(x,ay,az,r+1.5,12).cut(cyl(x-1,ay,az,r,14)).common(box(x-1,ay-r-2,az-r-2,14,2*r+4,r+2))
 strap=band
 for sign in (-1,1):
  ey=ay+sign*(r+8)-7
  strap=strap.fuse(box(x,ey,az,12,14,r)).fuse(box(x,ey,az+r-1.5,12,14,1.5))
  # screw clearances through ears, screws extend into plywood only.
  sy=ay+sign*(r+8)
  hole=Part.makeCylinder(2,5,V(x+6,sy,az+r-3),V(0,0,1));strap=strap.cut(hole)
  screw=Part.makeCylinder(1.7,12,V(x+6,sy,az+r-2),V(0,0,1))
  screw=screw.fuse(Part.makeCylinder(3.2,2,V(x+6,sy,az+r-4),V(0,0,1))).removeSplitter()
  scene[f'PF_StrapScrew{i}_{sign+2}']=tf(screw)
 scene[f'PF_CommercialStrap{i}']=tf(strap.removeSplitter())
moving=[n for n in scene if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope')]+['PLAYFIELD_ENVELOPE']
def rot(s,angle):
 s=s.copy();s.rotate(pivot,V(1,0,0),-angle);return s
reservations={n for n in scene if any(t in n for t in ('Reserve','RESERVED','CandidatePayload'))}
fixed={n:s for n,s in scene.items() if n not in moving and n not in reservations and n!='CandidateGlass'}
def hits(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>0.01:out.append([n,k,round(vol,4)])
 return out
checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)});print(n,v,flush=True)
sweep=[]
for angle in range(0,int(c['service_angle_deg'])+1,2):
 h=hits({n:rot(scene[n],angle) for n in moving},fixed);sweep.append({'angle':angle,'hits':h})
check('configured opening sweep no collisions at 2 degree samples',not any(s['hits'] for s in sweep))
raised={n:rot(scene[n],c['service_angle_deg']) for n in moving}
lift=[]
for dz in range(0,43,2):
 parts={n:scene[n].copy() for n in moving}
 for s in parts.values():s.translate(V(0,0,dz))
 lift.append({'dz':dz,'hits':hits(parts,fixed)})
check('vertical lift out of open cradles no collisions',not any(s['hits'] for s in lift))
check('dowel clears cradle upper edges after lift',pz-r+42>pz+24)
check('two floor supported cradles clear unchanged cabinet',not hits({n:scene[n] for n in ('PF_OpenCradleL','PF_OpenCradleR')},{n:s for n,s in fixed.items() if n not in ('PF_OpenCradleL','PF_OpenCradleR')}))
check('all solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
preserved=[n for n in original if n not in retired+['SIDE_L','SIDE_R']]
check('all other subsystem solids exactly preserved',all(diff(original[n],scene[n])<1e-5 for n in preserved))
poses={'PLAY':scene,'SERVICE':{n:(raised[n] if n in raised else s) for n,s in scene.items() if n!='CandidateGlass'}}
poses['LIFT-OUT']={n:s.copy() for n,s in scene.items() if n!='CandidateGlass'}
for n in moving:poses['LIFT-OUT'][n].translate(V(0,0,42))
# Exploded mechanism contains only requested pivot pieces (TV/VESA omitted).
mechanism=[n for n in moving if n not in ('PLAYFIELD_ENVELOPE','PF_VESAEnvelope')]+['PF_OpenCradleL','PF_OpenCradleR']
exploded={n:scene[n].copy() for n in mechanism}
for n,s in exploded.items():
 dz=160 if n=='PF_BasePlywood' else 105 if 'Strap' in n else 50 if n=='PF_WoodDowel' else 0
 s.translate(V(0,0,dz))
poses['EXPLODED']=exploded
(O/'diagnostic.json').write_text(json.dumps({'checks':checks,'sweep':sweep,'lift':lift},indent=2))
assert all(x['pass'] for x in checks),checks
saved={}
for state,pose in poses.items():
 out=A.newDocument('WoodPivot_'+state.replace('-','_'));out.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; owner final pivot correction; manufacturing not approved'
 sheet=out.addObject('Spreadsheet::Sheet','PivotParameters');sheet.set('A1',str(c['wood_dowel_diameter_mm']));sheet.setAlias('A1','DowelDiameter')
 for n,s in pose.items():
  if n=='PF_WoodDowel':
   o=out.addObject('Part::Cylinder',n);o.Height=560;o.setExpression('Radius','PivotParameters.DowelDiameter / 2');o.Placement=A.Placement(V(20,py,pz+(50 if state=='EXPLODED' else 42 if state=='LIFT-OUT' else 0)),A.Rotation(V(0,0,1),V(1,0,0)))
  else:o=out.addObject('PartDesign::Feature',n);o.Shape=s
  o.addProperty('App::PropertyString','PartID');o.PartID=n
 out.recompute();path=O/(state.lower()+'.FCStd');out.saveAs(str(path));A.closeDocument(out.Name)
 out=A.openDocument(str(path));out.recompute()
 check(state+' saved CAD recompute and solid equivalence',all(o.Shape.isValid() and diff(o.Shape,pose[o.Name])<1e-4 for o in out.Objects if hasattr(o,'Shape')))
 if state=='PLAY':Part.export([o for o in out.Objects if hasattr(o,'Shape') and o.Name!='PF_BackboxCheckEnvelope'],str(O/'current-v32.step'))
 saved[state]=str(path.relative_to(R));A.closeDocument(out.Name)
step=O/'current-v32.step';step.write_text('\n'.join(line.rstrip() for line in step.read_text().splitlines())+'\n')
def mesh(n,s):
 vs,fs=s.tessellate(.7);return {'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':[list(f) for f in fs]}
review={k:old[k] for k in ('buttons','closed_slope_deg','structural_proof','manufacturing_ready')};review.update({'pivot_xyz_mm':[300,py,pz],'opening_deg':c['service_angle_deg'],'wood_dowel_diameter_mm':2*r,'cradle_coordinates_mm':[[18,py,36],[564,py,36]],'cradle_seat_axis_xyz_mm':[[27,py,pz],[573,py,pz]],'lift_out_mm':42,'lift_out_clearance_mm':42-r-24,'custom_metal_parts_required':0,'commodity_metal_parts':12,'commodity_metal_ids':[n for n in scene if 'Strap' in n],'counts':{'PLAYFIELD PIVOT CUSTOM METAL PARTS':0,'PLAYFIELD PIVOT BEARINGS':0,'PLAYFIELD PIVOT BUSHINGS':0,'PLAYFIELD PIVOT STEEL RODS':0,'PLAYFIELD PIVOT WOOD DOWELS':1,'PLAYFIELD PIVOT CNC WOOD SUPPORTS':2,'PLAYFIELD BASE PLYWOOD PANELS':1,'COMMERCIAL STRAPS':4},'limits':'Sampled geometry only; no load proof. Commercial strap envelope provisional. Owner final architecture supersedes previous prop requirements.'})
# 40 mm lift clears tangent dowel bottom at z+24: equality, add margin below.
bundle={'parts':[mesh(n,s) for n,s in scene.items()],'states':{},'review':review}
for state,pose in poses.items():bundle['states'][state]={n:mesh(n,pose[n]) if n in pose else None for n in scene if n not in pose or diff(scene[n],pose[n])>1e-5}
(O/'mesh.json').write_text(json.dumps(bundle))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'checks':checks,'review':review,'saved_poses':saved,'retired_objects':retired,'preserved_solids':preserved,'source_sha256':sha(source),'mesh_sha256':sha(O/'mesh.json'),'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
for n in ('LICENSE','NOTICE.md'):(O/n).write_bytes((R/n).read_bytes())
assert all(x['pass'] for x in checks)
print('WOOD_PIVOT_PASS',flush=True)

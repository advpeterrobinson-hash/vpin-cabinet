"""Read-only B-rep metrics and conservative assembly screens. CERN-OHL-S-2.0."""
from pathlib import Path
import json, math
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/assembly-v333';O.mkdir(exist_ok=True,parents=True)
read=lambda p:json.loads((R/p).read_text())
reg=read('exports/generated/flatpack-v331/manufacturing-register.json')['parts']
man=read('exports/generated/viewer-v332/assembly-manual.json');cat=read('config/hardware_catalog_v33.json')
stages={i:int(s['id']) for s in man['stages'] for i in s['pieces']}
V=A.Vector
shapes={};rows=[]
for p in reg:
 s=Part.read(str(R/p['finished_member_brep']));wire=Part.read(str(R/p['outer_contour_brep']));outer=Part.Face(wire.Wires[0])
 # Projection from actual horizontal faces, preserving holes; blind pockets are
 # filled by their bottom face. Oblique edge features remain a volume residual.
 fs=[]
 for f in s.Faces:
  if type(f.Surface).__name__=='Plane' and abs(abs(f.normalAt(0,0).z)-1)<1e-7:
   q=f.copy();q.translate(V(0,0,-f.CenterOfMass.z));fs.append(q.extrude(V(0,0,1)))
 proj=fs[0]
 for f in fs[1:]:proj=proj.fuse(f)
 net=proj.Volume
 row={'instance_id':p['instance_id'],'volume_mm3':s.Volume,'center_of_mass_local_mm':list(s.Solids[0].CenterOfMass),
 'outer_area_mm2':outer.Area,'projected_material_area_mm2':net,'projected_cutouts_mm2':max(0,outer.Area-net),
 'nominal_blank_volume_mm3':outer.Area*p['nominal_stock_thickness_mm'],
 'removed_stock_volume_mm3':outer.Area*p['nominal_stock_thickness_mm']-s.Volume,'valid':s.isValid()}
 assert abs(s.Volume-p['volume_mm3'])<1e-4
 m=A.Matrix(*p['local_to_installed_matrix']);world=s.copy();world.transformShape(m);shapes[p['instance_id']]=world
 rows.append(row)
 print('METRIC',p['instance_id'],flush=True)
(O/'brep-metrics.json').write_text(json.dumps(rows,indent=2)+'\n')
# Candidate face-normal straight paths only. Passing sparse samples is NOT a
# swept-volume proof. Same-assembly laminate mates are intentionally excluded.
samples=[.5,2,5,10,20,40,80,150,300]
screens=[]
for p in reg:
 iid=p['instance_id'];s=shapes[iid];others=[q for q in reg if stages[q['instance_id']]<=stages[iid] and q['assembly_id']!=p['assembly_id'] and q['instance_id']!=iid]
 dirs=[]
 for sign in (1,-1):
  d=V(*p['face_A_outward_world'])*sign;hits=[]
  for dist in samples:
   q=s.copy();q.translate(d*dist)
   for other in others:
    b=shapes[other['instance_id']]
    if not q.BoundBox.intersect(b.BoundBox):continue
    v=q.common(b).Volume
    if v>1e-3:
     hits.append({'distance_mm':dist,'obstacle':other['instance_id'],'overlap_mm3':v});break
   if hits:break
  dirs.append({'outward_direction':list(d),'first_sample_conflict':hits[0] if hits else None,'status':'CONFLICT' if hits else 'SAMPLED_CLEAR_NOT_TRAJECTORY_VALIDATED'})
 screens.append({'instance_id':iid,'stage':stages[iid],'candidates':dirs,'same_stage_policy':'all other assemblies already present, conservative; own laminate siblings excluded', 'continuous_path_validated':False})
 print('PATH',iid,flush=True)
(O/'insertion-screens.json').write_text(json.dumps({'samples_mm':samples,'scope':'WOOD_ONLY_CANDIDATE_FACE_NORMALS_NOT_VALIDATED_INSTALLATION_PATHS','parts':screens},indent=2)+'\n')
# Tool screening: actual part location is the authority; center coordinates are
# only reserves. Exclude the first 25 mm seating zone; test 100 mm / R10 driver.
tools=[]
for h in cat['hardware']:
 if not h['id'].startswith('F'):continue
 for inst in h['instances']:
  direction=inst.get('installation_direction');center=inst.get('coordinate_xyz_mm')
  if not direction or not center:continue
  d=V(*direction)
  if d.Length<.1:continue
  d.normalize();d=-d;start=V(*center)+d*25;env=Part.makeCylinder(10,100,start,d);hits=[]
  for p in reg:
   b=shapes[p['instance_id']]
   if env.BoundBox.intersect(b.BoundBox):
    v=env.common(b).Volume
    if v>.001:hits.append({'piece':p['instance_id'],'overlap_mm3':v,'stage':stages[p['instance_id']]})
  tools.append({'id':h['id'],'object':inst['object'],'start_mm':list(start),'direction':list(d),'radius_mm':10,'length_mm':100,'wood_conflicts':hits,'status':'CONSERVATIVE_RESERVE_CONFLICT' if hits else 'WOOD_CLEAR_ONLY','physical_tool_validated':False})
(O/'tool-screens.json').write_text(json.dumps(tools,indent=2)+'\n')
# Actual simple library forms are estimates, never envelope/marker masses.
hw=[]
for h in cat['hardware']:
 side=read(str(Path(h['model']['path']).with_suffix('.json')))
 if h['model']['kind'] not in ['screw','washer','nut','dowel','insert']:continue
 if 'MARKER' in side['model_status']:continue
 doc=A.openDocument(str(R/h['model']['path']));objs=[o for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
 if objs:hw.append({'id':h['id'],'volume_mm3':objs[0].Shape.Volume,'model_status':side['model_status'],'mass_status':'ESTIMATED_NOMINAL_SIMPLIFIED_NO_THREADS'})
 A.closeDocument(doc.Name)
(O/'hardware-volumes.json').write_text(json.dumps(hw,indent=2)+'\n')
cur=read('config/current_v32.json');doc=A.openDocument(str(R/cur['geometry_directory']/'play.FCStd'))
glass=[]
for name in ['CandidateGlass','BB_Backglass']:
 obj=doc.getObject(name)
 if obj:glass.append({'object':name,'volume_mm3':obj.Shape.Volume,'status':'ESTIMATED_REFERENCE_GLASS'})
(O/'glass-volumes.json').write_text(json.dumps(glass,indent=2)+'\n');A.closeDocument(doc.Name)
print('V333_BREP_PASS',flush=True)

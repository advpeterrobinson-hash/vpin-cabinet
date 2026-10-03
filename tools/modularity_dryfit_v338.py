"""Read-only assembly datum and orientation audit. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load
C=json.loads((R/'config/service_modularity_v338.json').read_text());O=R/C['output'];source=R/C['source'];ss=load(source)
reg=json.loads((R/'exports/generated/two-stock-user-module-v337/manufacturing-register.json').read_text());manual=json.loads((R/'exports/generated/two-stock-user-module-v337/assembly-manual.json').read_text())
def xs(s):
 out=[]
 for f in s.Faces:
  if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Axis.x)>.999:
   p=f.Surface.Center;row=[round(p.y,6),round(p.z,6),round(f.Surface.Radius,6)]
   if row not in out:out.append(row)
 return sorted(out)
records=[]
for prefix in ['SHELF_SUPPORT','CROSS_GUIDE','PF_OpenCradle','BB_MonitorRailCleat','BB_CassetteCleat','BB_HingeCleat']:
 for n,s in ss.items():
  if not n.startswith(prefix):continue
  side='SIDE_L' if n.endswith('L') or 'L0' in n or 'L1' in n else 'SIDE_R'
  if n.startswith('BB_'):side='BB_SideL' if 'L' in n else 'BB_SideR'
  bores=xs(s);all_features=list(bores)
  if n.startswith('PF_OpenCradle'):bores=[p for p in bores if abs(p[2]-2.5)<1e-6]
  if n.startswith('CROSS_GUIDE'):bores=[p for p in bores if abs(p[0]-(s.BoundBox.YMin+8))<1e-5 or abs(p[0]-(s.BoundBox.YMax-8))<1e-5]
  sidebores=xs(ss[side]);matched=[p for p in bores if any(abs(p[0]-q[0])<1e-4 and abs(p[1]-q[1])<1e-4 for q in sidebores)]
  pp=[p for p in reg['parts'] if p['source_component']==n]
  records.append({'component':n,'manufacturing_instances':[p['instance_id'] for p in pp],'ids':[p['manufacturing_part_id'] for p in pp],'x_axis_bore_centers_yzr_mm':bores,'all_cylindrical_reference_features_yzr_mm':all_features,'matching_side_reference_axes':matched,'matching_side':side,'all_axes_match':bool(bores) and len(bores)==len(matched),'face_A':[p['face_A_outward_world'] for p in pp],'local_datums':[p['local_datum'] for p in pp]})
orientation=[{'instance_id':p['instance_id'],'manufacturing_id':p['manufacturing_part_id'],'source':p['source_component'],'assembly_id':p['assembly_id'],'face_A':p['face_A_outward_world'],'opposite_face':p['opposite_face'],'local_datum':p['local_datum'],'engraving':p.get('engraving',{'status':'SHOP_LABEL_NOT_CNC'})} for p in reg['parts']]
assert len({p['instance_id'] for p in orientation})==len(orientation)
report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'register_sha256':hashlib.sha256((R/'exports/generated/two-stock-user-module-v337/manufacturing-register.json').read_bytes()).hexdigest(),'manual_sha256':hashlib.sha256((R/'exports/generated/two-stock-user-module-v337/assembly-manual.json').read_bytes()).hexdigest(),'records':records,'piece_orientation_count':len(orientation),'orientation':orientation,'positive_datum_groups':['Main shell4mm side captures: FLOOR/FRONT/REAR/RearBearingShelf before SideR closure','PF cradles floor-bearing plus matching side locators','M067 carrier-front capture shoulders; do not alter','Underfront panel2mm locating recess'],'remaining_productization_holds':['Hardware-controlled bores and guide templates require selected hardware/coupon; coordinates in CAD do not by themselves make a released paper template.','Backbox monitor rail cleat locations: no side-normal locating bore pairs or side capture in current cleat B-reps; qualify a rear/frame/height setup template before kit release.','Captured shell F06 reinforcement family/quantity remains unresolved; cannot claim all kit fasteners supplied.','SW01 diagonal jig registration and hardware pitch remain physical holds; no freehand angled drilling.','Crossmember guide and shelf support axes are checked individually below; absent matching pilots require layout/template qualification rather than silent readiness.'],'manufacturing_release':False}
(O/'modularity-dryfit-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('V338_DRYFIT_AUDIT',len(records),len(orientation),[(r['component'],len(r['x_axis_bore_centers_yzr_mm']),len(r['matching_side_reference_axes'])) for r in records],flush=True)

"""Release-blocking ledger checks; no FreeCAD dependency."""
import csv,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return list(csv.DictReader((ROOT/'bom'/name).open()))
def validate(features=None,joints=None,parts=None):
 parts=parts if parts is not None else read('ACTIVE_PARTS.csv')
 features=features if features is not None else read('CNC_FEATURES_V25.csv')
 joints=joints if joints is not None else read('STRUCTURAL_JOINTS_V25.csv')
 ids={p['part_id'] for p in parts};names={p['object_name'] for p in parts}
 assert len(parts)==len(ids)==36,'active part reconciliation'
 assert {f['part_id'] for f in features}==ids,'feature part reconciliation'
 assert len({f['feature_id'] for f in features})==len(features),'duplicate feature ID'
 hw={r['item_id'] for r in read('MEASURE_BEFORE_CNC_V25.csv')}
 for f in features:
  assert f['status'] in ('DEFINED_PARAMETRIC','BLOCKED_MEASURE_HARDWARE','BLOCKED_DESIGN'),'unknown status'
  assert f['feature_type'] in ('PROFILE','DADO','RABBET','POCKET','THROUGH_HOLE','PILOT_HOLE','INSERT_HOLE','ENGRAVING','ALIGNMENT_MARK','CABLE_PASS','VENT'),'unknown operation'
  if f['hardware_dependency']:
   assert set(f['hardware_dependency'].split(';'))<=hw,'unmapped hardware'
   assert f['status']=='BLOCKED_MEASURE_HARDWARE','hardware release without evidence'
   assert all(f[k]=='' for k in ('x','y','diameter_or_width','depth')),'guessed hardware coordinates'
  if f['status']=='DEFINED_PARAMETRIC':assert f['recipe'],'missing feature recipe'
 for pid in ids:
  assert any(f['part_id']==pid and f['feature_type']=='PROFILE' for f in features),'missing profile'
  assert any(f['part_id']==pid and f['feature_type']=='ENGRAVING' for f in features),'missing identity'
 pairs=set()
 for j in joints:
  assert j['part_a'] in ids and j['part_b'] in ids,'unknown joint member'
  assert j['object_a'] in names and j['object_b'] in names,'unknown joint object'
  key=frozenset((j['object_a'],j['object_b']));assert key not in pairs,'duplicate joint';pairs.add(key)
  assert j['joint_type']!='REVIEW_INTERFACE','unclassified joint'
  for k in ('stock_dependency','depth','glue','fastener_requirement','cnc_prelocation','notes'):assert j[k],'incomplete joint'
  if j['hardware_dependency']!='none':assert set(j['hardware_dependency'].split(';'))<=hw,'joint hardware'
 cfg=json.loads((ROOT/'config/cnc_detail_v25.json').read_text())
 assert cfg['manufacturing_ready'] is False,'manufacturing gate'
 assert cfg['fit']['capture_depth_fraction']<=1/3+1e-9,'insufficient side skin'
 assert cfg['fit']['minimum_remaining_skin_fraction']>=2/3-1e-9,'side skin policy'
 assert json.loads((ROOT/'config/active_build_v25.json').read_text())['manufacturing_ready'] is False
 assert json.loads((ROOT/'config/cabinet_structure_v20.json').read_text())['cabinet']['outer_width_mm']==600
 # Every hardware-pattern group expected by explicit source mapping is present.
 from generate_cnc_register_v25 import dependencies
 for p in parts:
  assert {int(f['hardware_dependency'][3:]) for f in features if f['part_id']==p['part_id'] and f['hardware_dependency']}==set(dependencies(p['object_name'])),'missing hardware pattern'
 return dict(parts=len(parts),features=len(features),defined=sum(f['status']=='DEFINED_PARAMETRIC' for f in features),hardware_blocked=sum(f['status']=='BLOCKED_MEASURE_HARDWARE' for f in features),design_blocked=sum(f['status']=='BLOCKED_DESIGN' for f in features),joints=len(joints))

def negative_controls():
 f=read('CNC_FEATURES_V25.csv');j=read('STRUCTURAL_JOINTS_V25.csv')
 cases=[]
 x=copy.deepcopy(f);next(r for r in x if r['hardware_dependency'])['x']='123';cases.append(('guessed coordinate',x,j))
 x=copy.deepcopy(f);next(r for r in x if r['hardware_dependency'])['status']='DEFINED_PARAMETRIC';cases.append(('false release',x,j))
 x=[r for r in f if r['part_id']!=f[0]['part_id']];cases.append(('missing part',x,j))
 x=copy.deepcopy(j);x[0]['part_a']='UNKNOWN';cases.append(('unknown joint member',f,x))
 x=copy.deepcopy(f);x.pop(next(i for i,r in enumerate(x) if r['hardware_dependency']));cases.append(('missing hardware group',x,j))
 for label,x,y in cases:
  try:validate(x,y)
  except AssertionError:print('CNC_NEGATIVE_PASS',label)
  else:raise AssertionError('Accepted mutant '+label)
if __name__=='__main__':
 print('CNC_FEATURE_REGISTER_PASS',validate());negative_controls()

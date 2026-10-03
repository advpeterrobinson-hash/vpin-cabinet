"""Current promotion manifest and immutable WPC datum regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy,hashlib
from wpc_reference_v32 import reference_axis
R=Path(__file__).resolve().parents[1];c=json.loads((R/'config/current_v32.json').read_text());o=R/c['geometry_directory'];q=json.loads((o/'validation.json').read_text());r=json.loads((o/'regression-validation.json').read_text());v=json.loads((o/'viewer-validation.json').read_text())
assert reference_axis()==[300,1066.8,508]
assert r['pass'] and v['pass'] and all(x['pass'] for x in q['checks'])
assert not c['final_hinge_drilling_released'] and not c['manufacturing_ready'] and not q['manufacturing_ready']
cradle=R/c.get('cradle_validation_directory',c['geometry_directory']);cq=json.loads((cradle/'validation.json').read_text());m=json.loads((cradle/'cradle-metrology.json').read_text())
assert cq['promoted'] and c['cradle_relief_reserve_radius_mm']==cq['selected_radius_mm']==12
chosen=next(x for x in cq['radius_study']['candidates'] if x['radius_mm']==12)
assert chosen['complete_packaging_pass'] and chosen['tool_lift_clearance_mm']>=2-1e-6
assert abs(next(x for x in m['radii'] if x['radius_mm']==12)['minimum_local_ligament_mm']-6.27966988509371)<1e-7
for x in cq['radius_study']['candidates']:
 if x['radius_mm']!=12:assert not x.get('complete_packaging_pass',False)
if 'promotion_record' in c:
 proof=json.loads((R/c['promotion_record']).read_text());assert proof['promoted'] and proof['two_independent_locks'] and proof['cassette_retained_for_normal_fold']
 assert not proof['electronics_disconnection_introduced'] and proof['backbox_glass_retained'] and proof['custom_metal_added']==0
 for report in [q,r,proof]:
  for name,digest in report['input_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,'stale '+name
 assert q['mesh_sha256']==v['mesh_sha256']==hashlib.sha256((o/'mesh.json').read_bytes()).hexdigest()
 if (R/'config/viewer_v333.json').exists() or (R/'config/viewer_v332.json').exists():
  vm=json.loads((R/('config/viewer_v333.json' if (R/'config/viewer_v333.json').exists() else 'config/viewer_v332.json')).read_text());vv=json.loads((R/vm['validation']).read_text())
  assert vv['pass'] and not vm['geometry_changed'] and not vm['manufacturing_release']
  assert vv['source_mesh_sha256']==q['mesh_sha256']
  assert vv['viewer_sha256']==hashlib.sha256((R/vm['viewer']).read_bytes()).hexdigest()
 else:
  assert v['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
 assert not c['normal_fold_cassette_removal'] and not c['normal_fold_backbox_electronics_disconnection']
p=json.loads((R/'config/wpc_kinematics_v32.json').read_text());bad=copy.deepcopy(p);bad['axis_xyz_mm']=[300,1270,508];bad['pivot_from_rear_mm']=38.1
try:reference_axis(bad)
except ValueError:pass
else:raise AssertionError('superseded pivot accepted')
print('CURRENT_V32_PROMOTION_GATES_PASS')

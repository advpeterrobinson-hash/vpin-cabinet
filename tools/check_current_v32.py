"""Current promotion manifest and immutable WPC datum regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy
from wpc_reference_v32 import reference_axis
R=Path(__file__).resolve().parents[1];c=json.loads((R/'config/current_v32.json').read_text());o=R/c['geometry_directory'];q=json.loads((o/'validation.json').read_text());r=json.loads((o/'regression-validation.json').read_text());v=json.loads((o/'viewer-validation.json').read_text());m=json.loads((o/'cradle-metrology.json').read_text())
assert reference_axis()==[300,1066.8,508]
assert q['promoted'] and r['pass'] and v['pass'] and all(x['pass'] for x in q['checks'])
assert c['cradle_relief_reserve_radius_mm']==q['selected_radius_mm']==12
assert not c['final_hinge_drilling_released'] and not c['manufacturing_ready'] and not q['manufacturing_ready']
chosen=next(x for x in q['radius_study']['candidates'] if x['radius_mm']==12)
assert chosen['complete_packaging_pass'] and chosen['tool_lift_clearance_mm']>=2-1e-6
assert abs(next(x for x in m['radii'] if x['radius_mm']==12)['minimum_local_ligament_mm']-6.27966988509371)<1e-7
for x in q['radius_study']['candidates']:
 if x['radius_mm']!=12:assert not x.get('complete_packaging_pass',False)
p=json.loads((R/'config/wpc_kinematics_v32.json').read_text());bad=copy.deepcopy(p);bad['axis_xyz_mm']=[300,1270,508];bad['pivot_from_rear_mm']=38.1
try:reference_axis(bad)
except ValueError:pass
else:raise AssertionError('superseded pivot accepted')
print('CURRENT_V32_PROMOTION_GATES_PASS')

"""Current promotion manifest and immutable WPC datum regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy,hashlib
from wpc_reference_v32 import reference_axis
import runpy,sys
_current_root=Path(__file__).resolve().parents[1]
_current_manifest=json.loads((_current_root/'config/current_v32.json').read_text())
if _current_manifest.get('structural_revision')=='V34.2':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['manufacturing_ready'] and not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['raised_playfield_service_released']
 assert _current_manifest['allowed_plywood_stock_nominal_mm']==[12,18]
 runpy.run_path(str(_current_root/'tools/check_backbox_v342.py'),run_name='__main__')
 print('CURRENT_V342_REFERENCE_DESIGN_PASS; PHYSICAL / CNC HELD')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V34':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['manufacturing_ready'] and not _current_manifest['final_hinge_drilling_released']
 assert not _current_manifest['monitor_plate_normal_removal'] and not _current_manifest['raised_playfield_service_released']
 assert _current_manifest['allowed_plywood_stock_nominal_mm']==[12,18]
 runpy.run_path(str(_current_root/'tools/check_backbox_v34.py'),run_name='__main__')
 print('CURRENT_V34_DESIGN_PASS; PHYSICAL / CNC HELD')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.8':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready'] and not _current_manifest['manufacturing_valid']
 assert _current_manifest['closed_position_support_valid'] and not _current_manifest['physical_qualification_complete']
 assert _current_manifest['allowed_plywood_stock_nominal_mm']==[12,18]
 assert _current_manifest['front_adjuster_geometric_setup_window_mm']==[-1.9,.9]
 assert _current_manifest['front_retention_selected_option']=='A'
 assert not _current_manifest['raised_playfield_service_released'] and not _current_manifest['secondary_safety_straps_promoted']
 runpy.run_path(str(_current_root/'tools/check_service_productization_v338.py'),run_name='__main__')
 print('CURRENT_V338_SCOPE_PASS; PRIMARY SERVICE SUPPORT / PHYSICAL QUALIFICATION / CNC HELD')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.7':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready'] and not _current_manifest['manufacturing_valid']
 assert _current_manifest['closed_position_support_valid'] and not _current_manifest['physical_qualification_complete']
 assert _current_manifest['allowed_plywood_stock_nominal_mm']==[12,18]
 assert _current_manifest['underfront_button_bore_mm'] is None and _current_manifest['underfront_usb_cutout_mm'] is None
 assert _current_manifest['playfield_front_inset_each_side_mm']==52 and _current_manifest['playfield_front_width_mm']==396
 expected=[[89,350.593661971831],[127,357.2302816901408]]
 assert all(abs(x-y)<1e-7 for row,want in zip(_current_manifest['side_button_centers_yz_mm'],expected) for x,y in zip(row,want))
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['side_button_final_recess_mm'] is None
 runpy.run_path(str(_current_root/'tools/check_two_stock_user_module_v337.py'),run_name='__main__')
 print('CURRENT_V337_SCOPE_PASS; PHYSICAL QUALIFICATION AND CNC BLOCKED')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.6.3':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready'] and not _current_manifest['manufacturing_valid']
 assert _current_manifest['phase']=='CLOSED_SUPPORT_ARCHITECTURE_DESIGN_CANDIDATE'
 assert _current_manifest['closed_position_support_valid'] and not _current_manifest['physical_qualification_complete']
 assert _current_manifest['playfield_front_inset_each_side_mm']==52 and _current_manifest['playfield_front_width_mm']==396
 expected=[[89,350.593661971831],[127,357.2302816901408]]
 assert all(abs(x-y)<1e-7 for row,want in zip(_current_manifest['side_button_centers_yz_mm'],expected) for x,y in zip(row,want))
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['side_button_final_recess_mm'] is None
 runpy.run_path(str(_current_root/'tools/check_front_landings_v3363.py'),run_name='__main__')
 print('CURRENT_V3363_SUPPORT_ARCHITECTURE_PASS; PHYSICAL QUALIFICATION AND CNC BLOCKED')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.6.2':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready']
 assert _current_manifest['phase']=='GEOMETRY_ONLY_TRIM'
 assert _current_manifest['closed_position_support_status']=='CLOSED_POSITION_SUPPORT_BLOCKED' and not _current_manifest['closed_position_support_valid']
 assert _current_manifest['playfield_front_inset_each_side_mm']==52 and _current_manifest['playfield_front_width_mm']==396
 expected=[[89,350.593661971831],[127,357.2302816901408]]
 assert len(_current_manifest['side_button_centers_yz_mm'])==2
 assert all(abs(x-y)<1e-7 for row,want in zip(_current_manifest['side_button_centers_yz_mm'],expected) for x,y in zip(row,want))
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['side_button_final_recess_mm'] is None
 runpy.run_path(str(_current_root/'tools/check_playfield_rest_v3362.py'),run_name='__main__')
 print('CURRENT_V3362_GEOMETRY_ONLY_TRIM_PASS; CLOSED_POSITION_SUPPORT_BLOCKED')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.6.1':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready']
 expected=[[89,350.593661971831],[127,357.2302816901408]]
 assert all(abs(x-y)<1e-7 for row,want in zip(_current_manifest['side_button_centers_yz_mm'],expected) for x,y in zip(row,want))
 assert _current_manifest['side_button_vertical_datum']=='local_side_top_minus_65_mm'
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['playfield_base_horn_absent']
 runpy.run_path(str(_current_root/'tools/check_button_relief_v3361.py'),run_name='__main__')
 print('CURRENT_V3361_PROMOTION_GATES_PASS')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.6':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready']
 assert _current_manifest['side_button_centers_yz_mm']==[[255,270],[310,270]]
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['playfield_base_horn_absent']
 runpy.run_path(str(_current_root/'tools/check_monitor_support_v336.py'),run_name='__main__')
 print('CURRENT_V336_PROMOTION_GATES_PASS')
 sys.exit(0)
if _current_manifest.get('structural_revision')=='V33.5':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready']
 runpy.run_path(str(_current_root/'tools/check_structural_v335.py'),run_name='__main__')
 print('CURRENT_V335_PROMOTION_GATES_PASS')
 sys.exit(0)
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
 if (R/'config/viewer_v334.json').exists() or (R/'config/viewer_v333.json').exists() or (R/'config/viewer_v332.json').exists():
  vm=json.loads((R/('config/viewer_v334.json' if (R/'config/viewer_v334.json').exists() else 'config/viewer_v333.json' if (R/'config/viewer_v333.json').exists() else 'config/viewer_v332.json')).read_text());vv=json.loads((R/vm['validation']).read_text())
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

"""Promote the validated V33.8 SW02 design and documentation only.
CERN-OHL-S-2.0. Never a hardware/structural/CNC release.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];P='exports/generated/service-productization-v338/'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
v=read(P+'validation.json');g=read(P+'geometry-validation.json');c=read('config/service_productization_v338.json')
assert v['pass'] and g['pass'] and not v['manufacturing_ready']
assert v['native_sha256']==g['native_sha256']==sha(P+'play.FCStd')
assert v['viewer_sha256']==sha('exports/generated/viewer-v32/index.html')
for p,h in v['evidence_sha256'].items():assert sha(p)==h,p
assert c['retention']['selected_option']=='A' and c['adjustment']['final_safe_range_mm']==[-1.9,.9]
assert not read(P+'safety-validation.json')['promoted']
f=R/'config/current_v32.json';d=json.loads(f.read_text());d.update(
 structural_revision='V33.8',geometry_directory=P.rstrip('/'),geometry_mesh=P+'mesh.json.gz',
 geometry_builder='tools/combine_service_productization_v338.py',geometry_parameters='config/service_productization_v338.json',
 source_head_before_promotion=c['head_before'],structural_promotion_record=P+'validation.json',report=P+'README.md',
 manufacturing_register='config/manufacturing/flatpack_v338.json',hardware_catalog='config/hardware_catalog_v338.json',
 wood_material_map='config/wood_materials_v338.json',stock_policy='config/manufacturing/stock_policy_v338.json',
 phase='SW02_SERVICE_MODULARITY_DESIGN_CANDIDATE',front_landings_authority='config/service_productization_v338.json',
 front_landings_geometry_reference='config/front_landings_v3363.json',solid_front_landings='config/solid_front_landings_v338.json',
 front_retention_selected_option='A',front_retention_tool_required=True,
 front_adjuster_mechanical_travel_reference_mm=[-3,3],front_adjuster_geometric_setup_window_mm=[-1.9,.9],
 front_adjuster_setup_authority=P+'adjustment-validation.json',front_adjuster_user_angle_selection=False,
 optional_accessory_and_cable_policy='config/service_modularity_v338.json',
 primary_raised_playfield_support_status='UNDEFINED_IN_CURRENT; PHYSICAL_OPERATION_HOLD',
 raised_playfield_service_released=False,secondary_safety_straps_promoted=False,
 physical_qualification_complete=False,manufacturing_valid=False,manufacturing_ready=False,
 backbox_source_note='V33.7 backbox and all unrelated geometry retained exactly. V33.8 replaces six front-landing plywood layers with two SW02 solid blocks and retires four binder screws only. Original captive M6 retention retained. Optional boards/cable zones do not add permanent holes. Primary raised support and universal backbox wiring remain unresolved; no manufacturing release.')
assert d['allowed_plywood_stock_nominal_mm']==[12,18] and not d['final_hinge_drilling_released']
assert d['underfront_button_bore_mm'] is None and d['underfront_usb_cutout_mm'] is None
f.write_text(json.dumps(d,indent=2)+'\n')
p=R/'tools/check_current_v32.py';s=p.read_text();anchor="if _current_manifest.get('structural_revision')=='V33.7':"
route="""if _current_manifest.get('structural_revision')=='V33.8':
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
"""
if "structural_revision')=='V33.8'" not in s:
 assert anchor in s;s=s.replace(anchor,route+anchor,1);p.write_text(s)
print('V338_DESIGN_PROMOTED; PRIMARY_SERVICE_SUPPORT_HOLD; MANUFACTURING_BLOCKED')

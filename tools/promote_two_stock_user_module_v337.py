"""Promote only the validated V33.7 two-stock/module design candidate.
CERN-OHL-S-2.0. Purchased control cuts, physical qualification and CNC stay held.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/two-stock-user-module-v337';P=str(O.relative_to(R))+'/'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
C=read('config/underfront_user_module_v337.json');v=read(P+'validation.json');gate=read(P+'combined-validation.json');assert v['pass'] and gate['pass'] and not v['manufacturing_ready']
assert v['native_sha256']==gate['native_sha256']==sha(P+'play.FCStd');assert v['viewer_sha256']==sha('exports/generated/viewer-v32/index.html')
for name,checksum in v['evidence_sha256'].items():assert checksum==sha(P+name),name
assert C['button']['BUTTON_BORE_MM'] is None and C['usb']['USB_CUTOUT_DIAMETER_MM'] is None and not C['manufacturing_release']
builder='tools/combine_two_stock_v337.py';assert (R/builder).is_file(),'Combined native builder must exist before promotion'
p=R/'config/current_v32.json';c=json.loads(p.read_text());c.update(structural_revision='V33.7',geometry_mesh=P+'mesh.json.gz',geometry_directory=str(O.relative_to(R)),geometry_builder=builder,geometry_parameters='config/underfront_user_module_v337.json',plywood_conversion_parameters='config/plywood_conversion_v337.json',source_head_before_promotion=C['head_before'],structural_promotion_record=P+'validation.json',report=P+'README.md',manufacturing_register='config/manufacturing/flatpack_v337.json',hardware_catalog='config/hardware_catalog_v337.json',wood_material_map='config/wood_materials_v337.json',phase='TWO_STOCK_GENERIC_USER_MODULE_DESIGN_CANDIDATE',closed_position_support_status='ARCHITECTURE_PASS_PHYSICAL_QUALIFICATION_HOLD',closed_position_support_valid=True,physical_qualification_complete=False,manufacturing_valid=False,manufacturing_ready=False,allowed_plywood_stock_nominal_mm=[12,18],underfront_user_module='config/underfront_user_module_v337.json',underfront_control_functions='USER_CONFIGURABLE',underfront_button_bore_mm=None,underfront_usb_cutout_mm=None,backbox_source_note='Scoped thin plywood stock conversion to 12 mm stock; functional interfaces validated by V33.7 combined gate. All other cabinet/backbox/playfield/WPC geometry preserved. Underfront bay is scoped one-face FLOOR machining with removable 12 mm generic user plate. Final hardware cuts, actual stock/coupon, physical qualification and CNC remain held.')
assert not c['final_hinge_drilling_released'];p.write_text(json.dumps(c,indent=2)+'\n')
vm={'version':'V33.7','authority':'TWO_STOCK_GENERIC_USER_MODULE_DESIGN_CANDIDATE','source_head':C['head_before'],'viewer':'exports/generated/viewer-v32/index.html','builder':'tools/build_viewer_v337.py','validation':P+'validation.json','manual_json':P+'assembly-manual.json','manufacturing_register':'config/manufacturing/flatpack_v337.json','hardware_catalog':'config/hardware_catalog_v337.json','unrelated_geometry_unchanged':True,'physical_qualification_complete':False,'manufacturing_release':False}
(R/'config/viewer_v337.json').write_text(json.dumps(vm,indent=2)+'\n')
p=R/'tools/build_review_viewer.py';s=p.read_text();old="'tools/build_viewer_v3363.py' if (ROOT/'config/viewer_v3363.json').exists()";new="'tools/build_viewer_v337.py' if (ROOT/'config/viewer_v337.json').exists() else "+old
if new not in s:
 assert old in s;s=s.replace(old,new,1);p.write_text(s)
p=R/'tools/check_current_v32.py';s=p.read_text();anchor="if _current_manifest.get('structural_revision')=='V33.6.3':"
route="""if _current_manifest.get('structural_revision')=='V33.7':
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
"""
if "structural_revision')=='V33.7'" not in s:
 assert anchor in s;s=s.replace(anchor,route+anchor,1);p.write_text(s)
print('V337_TWO_STOCK_MODULE_PROMOTED; PHYSICAL QUALIFICATION AND CNC BLOCKED')

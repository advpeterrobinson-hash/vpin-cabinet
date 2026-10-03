"""Route CURRENT to scoped V33.6.3 support only after complete architecture gate.
CERN-OHL-S-2.0. Physical qualification and all CNC release gates remain open.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
C=read('config/front_landings_v3363.json');v=read('exports/generated/front-landings-v3363/validation.json');gate=read('exports/generated/front-landings-v3363/support-validation.json')
assert v['pass'] and gate['architecture_pass'] and v['closed_position_support_valid']
assert not v['manufacturing_ready'] and not v['physical_qualification_complete']
assert v['native_sha256']==sha('exports/generated/front-landings-v3363/play.FCStd')
assert v['viewer_sha256']==sha('exports/generated/viewer-v32/index.html')
assert v['support_validation_sha256']==sha('exports/generated/front-landings-v3363/support-validation.json')
for name,checksum in v['evidence_sha256'].items():assert checksum==sha('exports/generated/front-landings-v3363/'+name),name
p=R/'config/current_v32.json';c=json.loads(p.read_text());c.update(structural_revision='V33.6.3',geometry_mesh='exports/generated/front-landings-v3363/mesh.json.gz',geometry_directory='exports/generated/front-landings-v3363',geometry_builder='tools/front_landings_v3363_entry.py',geometry_parameters='config/front_landings_v3363.json',source_head_before_promotion=C['head_before'],structural_promotion_record='exports/generated/front-landings-v3363/validation.json',report='exports/generated/front-landings-v3363/README.md',manufacturing_register='config/manufacturing/flatpack_v3363.json',hardware_catalog='config/hardware_catalog_v3363.json',wood_material_map='config/wood_materials_v3363.json',phase='CLOSED_SUPPORT_ARCHITECTURE_DESIGN_CANDIDATE',closed_position_support_status='ARCHITECTURE_PASS_PHYSICAL_QUALIFICATION_HOLD',closed_position_support_valid=True,physical_qualification_complete=False,manufacturing_valid=False,manufacturing_ready=False,closed_support_audit='exports/generated/front-landings-v3363/support-validation.json',front_landings_authority='config/front_landings_v3363.json',backbox_source_note='V33.6.2 geometry exactly preserved. Six18mm front-landing layers and provisional hardware added. Rear dowel/cradles plus two side landings carry PLAY load at unchanged9.906669-degree pose. T1/T2/T3 intentionally clear. ±3mm adjuster travel compensates tolerances only; it is not an authorized playfield-height or tilt adjustment. Hardware/material/load qualification and CNC remain HOLD.')
assert not c['final_hinge_drilling_released'];p.write_text(json.dumps(c,indent=2)+'\n')
vm={'version':'V33.6.3','authority':'COMPLETE_CLOSED_SUPPORT_ARCHITECTURE_DESIGN_CANDIDATE','phase':c['phase'],'source_head':C['head_before'],'viewer':'exports/generated/viewer-v32/index.html','builder':'tools/build_viewer_v3363.py','validation':'exports/generated/front-landings-v3363/validation.json','manual_json':'exports/generated/front-landings-v3363/assembly-manual.json','manufacturing_register':'config/manufacturing/flatpack_v3363.json','hardware_catalog':'config/hardware_catalog_v3363.json','geometry_changed':True,'prior_geometry_unchanged':True,'closed_position_support_valid':True,'closed_position_support_status':c['closed_position_support_status'],'physical_qualification_complete':False,'manufacturing_release':False}
(R/'config/viewer_v3363.json').write_text(json.dumps(vm,indent=2)+'\n')
p=R/'tools/build_review_viewer.py';s=p.read_text();old="'tools/build_viewer_v3362.py' if (ROOT/'config/viewer_v3362.json').exists()";new="'tools/build_viewer_v3363.py' if (ROOT/'config/viewer_v3363.json').exists() else "+old
if new not in s:
 assert old in s;s=s.replace(old,new,1);p.write_text(s)
p=R/'tools/check_current_v32.py';s=p.read_text();anchor="if _current_manifest.get('structural_revision')=='V33.6.2':"
route="""if _current_manifest.get('structural_revision')=='V33.6.3':
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
"""
if "structural_revision')=='V33.6.3'" not in s:
 assert anchor in s;s=s.replace(anchor,route+anchor,1);p.write_text(s)
print('V3363_SUPPORT_ARCHITECTURE_PROMOTED; PHYSICAL QUALIFICATION AND CNC BLOCKED')

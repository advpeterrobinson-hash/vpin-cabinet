"""Route CURRENT to requested V33.6.2 trim, retaining explicit missing-support HOLD.
CERN-OHL-S-2.0. GEOMETRY_ONLY_TRIM is not a complete mechanical qualification.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/playfield-rest-v3362'
C=json.loads((R/'config/playfield_rest_v3362.json').read_text());v=json.loads((O/'validation.json').read_text())
assert v['pass'] and not v['manufacturing_ready'] and not v['closed_position_support_valid']
assert v['closed_position_support_status']=='CLOSED_POSITION_SUPPORT_BLOCKED'
assert v['native_sha256']==hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest()
assert v['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
p=R/'config/current_v32.json';c=json.loads(p.read_text());c.update(structural_revision='V33.6.2',geometry_mesh='exports/generated/playfield-rest-v3362/mesh.json.gz',geometry_directory='exports/generated/playfield-rest-v3362',geometry_builder='tools/playfield_rest_v3362_entry.py',geometry_parameters='config/playfield_rest_v3362.json',source_head_before_promotion=C['head_before'],structural_promotion_record='exports/generated/playfield-rest-v3362/validation.json',report='exports/generated/playfield-rest-v3362/README.md',manufacturing_register='config/manufacturing/flatpack_v3362.json',side_button_positional_authority='config/button_relief_v3361.json',side_button_centers_yz_mm=[[q['y_mm'],q['z_mm']] for q in C['side_buttons']['centers']],side_button_vertical_datum='local_side_top_minus_65_mm',side_button_final_bore_mm=None,side_button_final_recess_mm=None,playfield_base_horn_absent=True,playfield_front_inset_each_side_mm=52,playfield_front_width_mm=396,phase='GEOMETRY_ONLY_TRIM',closed_position_support_status='CLOSED_POSITION_SUPPORT_BLOCKED',closed_position_support_valid=False,manufacturing_valid=False,manufacturing_ready=False,closed_support_audit='exports/generated/playfield-rest-v3362/closed-support-audit.json',backbox_source_note='V33.6.1 backbox, button datums and monitor interfaces unchanged. Only PF base front relief inset increases30mm per side to52mm. No front landing is modeled; current PLAY pitch is not mechanically stopped. Existing service collision paths do not certify static support.')
p.write_text(json.dumps(c,indent=2)+'\n')
vm={'version':'V33.6.2','authority':'CURRENT_REQUESTED_FRONT_TRIM_WITH_EXPLICIT_CLOSED_SUPPORT_BLOCKER','phase':'GEOMETRY_ONLY_TRIM','source_head':C['head_before'],'viewer':'exports/generated/viewer-v32/index.html','builder':'tools/build_viewer_v3362.py','validation':'exports/generated/playfield-rest-v3362/validation.json','manual_json':'exports/generated/playfield-rest-v3362/assembly-manual.json','manufacturing_register':'config/manufacturing/flatpack_v3362.json','geometry_changed':True,'closed_position_support_valid':False,'closed_position_support_status':'CLOSED_POSITION_SUPPORT_BLOCKED','manufacturing_release':False}
(R/'config/viewer_v3362.json').write_text(json.dumps(vm,indent=2)+'\n')
p=R/'tools/build_review_viewer.py';s=p.read_text();old="'tools/build_viewer_v3361.py' if (ROOT/'config/viewer_v3361.json').exists()";new="'tools/build_viewer_v3362.py' if (ROOT/'config/viewer_v3362.json').exists() else "+old
if new not in s:
 assert old in s;s=s.replace(old,new,1);p.write_text(s)
p=R/'tools/check_current_v32.py';s=p.read_text();anchor="if _current_manifest.get('structural_revision')=='V33.6.1':"
route="""if _current_manifest.get('structural_revision')=='V33.6.2':
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
"""
if "structural_revision')=='V33.6.2'" not in s:
 assert anchor in s;s=s.replace(anchor,route+anchor,1);p.write_text(s)
print('V3362_GEOMETRY_ONLY_TRIM_PROMOTED; CLOSED_POSITION_SUPPORT_BLOCKED; CNC BLOCKED')

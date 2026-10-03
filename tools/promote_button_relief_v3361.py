"""Promote validated V33.6.1 button/relief overlay, never machining release.
CERN-OHL-S-2.0. History/owner documentation remains separately reviewed.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/button-relief-v3361'
C=json.loads((R/'config/button_relief_v3361.json').read_text());v=json.loads((O/'validation.json').read_text())
assert v['pass'] and not v['manufacturing_ready']
assert v['native_sha256']==hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest()
assert v['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
p=R/'config/current_v32.json';c=json.loads(p.read_text());c.update(structural_revision='V33.6.1',geometry_mesh='exports/generated/button-relief-v3361/mesh.json.gz',geometry_directory='exports/generated/button-relief-v3361',geometry_builder='tools/button_relief_v3361_entry.py',geometry_parameters='config/button_relief_v3361.json',source_head_before_promotion=C['head_before'],structural_promotion_record='exports/generated/button-relief-v3361/validation.json',report='exports/generated/button-relief-v3361/README.md',manufacturing_register='config/manufacturing/flatpack_v3361.json',side_button_positional_authority='config/button_relief_v3361.json',side_button_centers_yz_mm=[[q['y_mm'],q['z_mm']] for q in C['side_buttons']['centers']],side_button_vertical_datum='local_side_top_minus_65_mm',side_button_authority_commit='87d63825e09f5ebbe85a89a7e705a49f1b0c320b',side_button_final_bore_mm=None,side_button_final_recess_mm=None,playfield_base_horn_absent=True,backbox_source_note='V33.6 monitor/carrier strain slots, M067 and every existing adjustment/retention remain unchanged. V33.6.1 restores Y89/Y127 front ergonomics and adds a clean open-front playfield relief. V33.6 rear service window and slots preserved; central VESA-plate window remains HOLD.')
p.write_text(json.dumps(c,indent=2)+'\n')
vm={'version':'V33.6.1','authority':'CURRENT_OWNER_FRONT_ERGONOMICS_AND_CLEAN_RELIEF','source_head':C['head_before'],'viewer':'exports/generated/viewer-v32/index.html','builder':'tools/build_viewer_v3361.py','validation':'exports/generated/button-relief-v3361/validation.json','manual_json':'exports/generated/button-relief-v3361/assembly-manual.json','manufacturing_register':'config/manufacturing/flatpack_v3361.json','geometry_changed':True,'manufacturing_release':False}
(R/'config/viewer_v3361.json').write_text(json.dumps(vm,indent=2)+'\n')
# Route CURRENT consumers only after the new gates pass. Historical builders and
# their old negative controls remain intact for audit/replay.
p=R/'tools/build_review_viewer.py';s=p.read_text();old="'tools/build_viewer_v336.py' if (ROOT/'config/viewer_v336.json').exists()";new="'tools/build_viewer_v3361.py' if (ROOT/'config/viewer_v3361.json').exists() else "+old
if new not in s:
 assert old in s;s=s.replace(old,new,1);p.write_text(s)
p=R/'tools/check_current_v32.py';s=p.read_text();anchor="if _current_manifest.get('structural_revision')=='V33.6':"
route="""if _current_manifest.get('structural_revision')=='V33.6.1':
 assert reference_axis()==[300,1066.8,508]
 assert not _current_manifest['final_hinge_drilling_released'] and not _current_manifest['manufacturing_ready']
 expected=[[89,350.593661971831],[127,357.2302816901408]]
 assert all(abs(x-y)<1e-7 for row,want in zip(_current_manifest['side_button_centers_yz_mm'],expected) for x,y in zip(row,want))
 assert _current_manifest['side_button_vertical_datum']=='local_side_top_minus_65_mm'
 assert _current_manifest['side_button_final_bore_mm'] is None and _current_manifest['playfield_base_horn_absent']
 runpy.run_path(str(_current_root/'tools/check_button_relief_v3361.py'),run_name='__main__')
 print('CURRENT_V3361_PROMOTION_GATES_PASS')
 sys.exit(0)
"""
if "structural_revision')=='V33.6.1'" not in s:
 assert anchor in s;s=s.replace(anchor,route+anchor,1);p.write_text(s)
print('V3361_PROMOTION_PASS; CNC BLOCKED')

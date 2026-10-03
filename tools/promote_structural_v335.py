"""Promote only after native, manufacturing and offline browser validation. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335'
read=lambda p:json.loads((R/p).read_text())
v=read('exports/generated/structural-v335/validation.json');assert v['pass'] and not v['manufacturing_ready']
assert v['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
c=read('config/current_v32.json');c.update(structural_revision='V33.5',geometry_mesh='exports/generated/structural-v335/mesh.json.gz',geometry_directory='exports/generated/structural-v335',geometry_builder='tools/structural_v335_entry.py',geometry_parameters='config/structural_simplification_v335.json',source_head_before_promotion='ca4e23eb598bb716156c41a7897ec8275e41f0ae',structural_promotion_record='exports/generated/structural-v335/validation.json',report='exports/generated/structural-v335/README.md',manufacturing_register='config/manufacturing/flatpack_v335.json',hardware_catalog='config/hardware_catalog_v335.json',backbox_source_note='Accepted twin-door/210mm/Y1146/WPC/lock architecture retained. V33.5 changes shelf side capture, two monitor carrier capture interfaces, one transverse stop rail, and documented lower-shell/fan interfaces; see exact difference register. All purchased hardware/fit/CNC holds remain.')
(R/'config/current_v32.json').write_text(json.dumps(c,indent=2)+'\n')
vm={'version':'V33.5','authority':'CURRENT_AUTHORIZED_STRUCTURAL_INTERFACE_OVERLAY','source_head':c['source_head_before_promotion'],'viewer':'exports/generated/viewer-v32/index.html','builder':'tools/build_viewer_v335.py','validation':'exports/generated/structural-v335/validation.json','manual_json':'exports/generated/structural-v335/assembly-manual.json','manufacturing_register':'config/manufacturing/flatpack_v335.json','geometry_changed':True,'manufacturing_release':False}
(R/'config/viewer_v335.json').write_text(json.dumps(vm,indent=2)+'\n')
p=R/'README.md';s=p.read_text();s=s.replace(s.splitlines()[0],'> CURRENT V33.5: [structural interfaces and owner review](exports/generated/structural-v335/README.md). 97 CNC plywood pieces + 4 unchanged SW01 shop blocks = 101 pieces / 59 families. Captured shell/shelf joints and one monitor-stop rail; M006 and original cradles retained. CNC remains BLOCKED. [Offline viewer](exports/generated/viewer-v32/index.html). [Preserved SW01 jig](exports/generated/solid-leg-v334/README.md).',1);p.write_text(s)
for f in ['docs/CABINET_JOINERY_PROPOSAL.md','docs/JOINERY_STUDY_V32.md']:
 p=R/f;s=p.read_text();banner='> Historical study retained. CURRENT captured-joint authority is [V33.5](STRUCTURAL_SIMPLIFICATION_V335.md): 4 mm nominal side capture, measured-stock/coupon fit hold, hardware-dependent underside pockets. Earlier proposal dimensions/status are not current manufacturing release.\n\n'
 if not s.startswith(banner):p.write_text(banner+s)
print('V335_PROMOTION_PASS; MANUFACTURING STILL BLOCKED')

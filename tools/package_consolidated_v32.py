"""Package explicit review artifacts, excluding backups and third-party assets. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
O=R/'exports/generated/consolidated-v32'
files=['LICENSE','NOTICE.md','docs/CONSOLIDATED_DRAWING_V32.md','library/references/links.txt','config/consolidated_audio_v32.json','config/floor_detail_v32.json','tools/consolidated_audio_v32_entry.py','tools/render_consolidated_v32.py','tools/run_consolidated_v32.sh','tools/package_consolidated_v32.py','output/pdf/v32-desenho-consolidado.pdf','exports/generated/floor-detail-v32/floor-detail.FCStd','exports/generated/floor-detail-v32/validation.json']
files += ['exports/generated/consolidated-v32/'+n for n in ['README.txt','cabinet-v32-consolidated.FCStd','cabinet-v32-consolidated.step','floor-draft-mm.dxf','floor-operations.json','validation.json','mesh.json','01-consolidated-interior.png','LICENSE','NOTICE.md']]
report=json.loads((O/'validation.json').read_text())
assert len(report['checks'])==39 and all(v['pass'] for v in report['checks'])
for p,h in report['source_hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
manifest={p:{'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'bytes':(R/p).stat().st_size} for p in files}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
zpath=O/'v32-desenho-consolidado.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(R/p,p)
 z.write(O/'manifest.json','exports/generated/consolidated-v32/manifest.json')
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for p,v in manifest.items():assert hashlib.sha256(z.read(p)).hexdigest()==v['sha256']
print('CONSOLIDATED_PACKAGE_PASS',len(files),'files;',zpath.stat().st_size,'bytes')

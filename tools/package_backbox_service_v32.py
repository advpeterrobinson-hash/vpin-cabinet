"""Offline CAD-review gallery and compressed mesh package. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,html
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-service-v32'
q=json.loads((O/'validation.json').read_text());m=json.loads((O/'motion-validation.json').read_text());r=json.loads((O/'regression-validation.json').read_text())
assert all(x['pass'] for x in q['checks']) and m['pass'] and r['pass']
for report in [q,m,r]:
    for name,digest in report['input_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest, 'stale input '+name
raw=O/'review-mesh.json';packed=O/'review-mesh.json.gz'
if raw.exists():
    full=json.loads(raw.read_bytes());visual=json.loads((O/'flex-visuals.json').read_text())
    for name,digest in visual['source_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,'stale visual mesh '+name
    for state,overrides in visual['states'].items():full['states'][state]=[overrides.get(p['name'],p) for p in full['states'][state]]
    full['parts']=[visual['states']['rear-closed'].get(p['name'],p) for p in full['parts']]
    bank={}
    def intern(part):
        part={**part,'vertices':[[round(v,6) for v in xyz] for xyz in part['vertices']]}
        encoded=json.dumps(part,separators=(',',':'));key=hashlib.sha256(encoded.encode()).hexdigest()[:24]
        if key in bank:assert bank[key]==part
        bank[key]=part;return key
    small={'format':'deduplicated-cad-mesh-v1','precision_mm':.000001,'groups':full['groups'],'metadata':full['metadata']}
    for field in ['parts','blanks','zones','drivers']:small[field]=[intern(p) for p in full[field]]
    small['states']={name:[intern(p) for p in scene] for name,scene in full['states'].items()};small['meshes']=bank
    packed.write_bytes(gzip.compress(json.dumps(small,separators=(',',':')).encode(),compresslevel=6,mtime=0))
assert packed.exists()
review=json.loads((O/'review-images.json').read_text());cards=[]
for item in review['images']:
    image=html.escape(item['file']);cad=html.escape(item['cad']);title=html.escape(item['id']+' · '+item['title'])
    cards.append(f'<article><a href="{image}"><img loading="lazy" src="{image}" alt="{title}"></a><h2>{title}</h2><a href="{image}">Full image</a> · <a href="{cad}">FreeCAD scene</a></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V32 backbox service review</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:1500px;margin:32px auto;padding:0 24px;background:#f5f7fa;color:#243244}h1{font-size:30px;margin-bottom:8px}.status{padding:16px;border-left:5px solid #a95534;background:#fff0e8}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;margin-top:28px}article{background:white;border:1px solid #cad3dc;border-radius:8px;padding:12px}img{width:100%;height:auto}h2{font-size:16px}a{color:#175b91}footer{margin:30px 0;font-size:13px}</style>
<h1>V32 backbox service architecture</h1><div class="status"><strong>REVIEW CANDIDATE — NOT PROMOTED. MANUFACTURING BLOCKED.</strong><p>Twin rear doors reach 100°. The populated backbox clears 0–90° with backbox glass retained. Playfield glass and matrix must be removed; rear leaves and carriers secured.</p><p><strong>Remaining service tradeoff:</strong> the lower cassette must be withdrawn to reach the existing upright-lock tool columns, then secured again before folding. This workflow has not been assumed acceptable. Current V32 geometry and its viewer remain unchanged.</p></div>
<p><a href="../../../studies/backbox-service-v32/README.md">Engineering report</a> · <a href="validation.json">Service checks</a> · <a href="motion-validation.json">Motion certificates</a> · <a href="regression-validation.json">Preservation regression</a></p><p>A–T are the requested new views; R2 shows a conditional future toy scenario; U–Z cover fold and integration. Images use actual CAD tessellation and sections. Purple parts are provisional hardware/cable reserves. View S is a rejected accessory, not installed geometry.</p><main class="grid">'''+''.join(cards)+'''</main><footer>Original project material: CERN-OHL-S-2.0. <a href="LICENSE">License</a> · <a href="NOTICE.md">Notice</a> · Source Location: <a href="https://github.com/advpeterrobinson-hash/vpin-cabinet">vpin-cabinet</a>. Offline gallery: no remote assets, scripts or fonts.</footer></html>'''
(O/'index.html').write_text(page)
names=['LICENSE','NOTICE.md','validation.json','motion-validation.json','regression-validation.json','details.json','front-inset-screen.json','review-images.json','review-mesh.json.gz','index.html']
names+=list(q['results']['cad_files'].values())+[i['file'] for i in review['images']]
names+=[i['cad'] for i in review['images']]
manifest={'status':'REVIEW_CANDIDATE_NOT_PROMOTED','manufacturing_ready':False,'source_head':q['source_head'],'mesh_uncompressed_sha256':hashlib.sha256(gzip.decompress(packed.read_bytes())).hexdigest(),'files':[]}
for name in sorted(set(names)):
    path=O/name;data=path.read_bytes();assert len(data)<100_000_000
    manifest['files'].append({'file':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(O/'artifact-index.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('BACKBOX_SERVICE_PACKAGE_PASS',len(manifest['files']),round(sum(x['bytes'] for x in manifest['files'])/1e6,2),'MB')

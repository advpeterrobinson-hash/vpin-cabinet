"""Offline review delivery and hash manifest; no manufacturing release. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,html
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-lock-integration-v32'
p=json.loads((O/'promotion.json').read_text());assert p['promoted']
for name,h in p['input_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h
review=json.loads((O/'review-images.json').read_text());assert len(review['images'])==23
cards=[]
for r in review['images']:
    assert (O/r['file']).exists() and (O/r['cad']).exists()
    title=html.escape(r['id']+' · '+r['title']);fn=html.escape(r['file']);cad=html.escape(r['cad'])
    cards.append(f'<article><a href="{fn}"><img src="{fn}" loading="lazy" alt="{title}"></a><h2>{title}</h2><a href="{fn}">Image</a> · <a href="{cad}">Native CAD</a></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V32 backbox upright-lock integration</title><style>body{font:16px/1.5 system-ui,sans-serif;max-width:1500px;margin:32px auto;padding:0 24px;color:#233342;background:#f6f8fa}h1{font-size:29px}.status{padding:18px;background:#e4f1e9;border-left:5px solid #298562}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}article{background:white;border:1px solid #ccd5df;border-radius:8px;padding:12px}img{width:100%}h2{font-size:16px}a{color:#185b91}footer{font-size:13px;margin-top:32px}</style>
<h1>Complete V32 backbox — rear-operated upright locks</h1><div class="status"><strong>PROMOTED TO CURRENT DESIGN. MANUFACTURING BLOCKED.</strong><p>Option B: two hand-operated clamps at X130/X470, Y1260. Open rear doors, release and positively park both captive knob/washer assemblies, secure tether slack, then latch the doors. The lower cassette and all backbox front modules remain installed.</p><p>Populated 0–90° fold passes with backbox glass retained. Main playfield glass and matrix remain removal prerequisites. Rare WPC hinge maintenance may still need cassette removal.</p></div>
<p><a href="../../../studies/backbox-lock-integration-v32/README.md">Engineering report</a> · <a href="../viewer-v32/index.html">CURRENT offline viewer</a> · <a href="search.json">Search data</a> · <a href="validation.json">CAD and motion gates</a> · <a href="regression-validation.json">Independent regression</a> · <a href="viewer-validation.json">Viewer checks</a></p>
<p>23 actual CAD review views. Option A is a rejected diagnostic. Lock hardware and bore sizes are provisional. Net bearing is 65,446.2 mm² after the two reference bores, 99.66% of the previous contact area. No custom metal or electrical connector system is introduced.</p><p>Additional native states: <a href="blank-fans.FCStd">fan blanks</a> · <a href="toy-zones.FCStd">toy zones</a> · <a href="locks-parked.FCStd">parked locks</a> · <a href="play.FCStd">complete upright cabinet</a> · <a href="backbox-fold.FCStd">complete folded cabinet</a>.</p><main class="grid">'''+''.join(cards)+'''</main><footer>Original material under CERN-OHL-S-2.0. <a href="LICENSE">License</a> · <a href="NOTICE.md">Notice</a>. Source Location: <a href="https://github.com/advpeterrobinson-hash/vpin-cabinet">vpin-cabinet</a>. No remote assets or scripts required.</footer></html>'''
(O/'index.html').write_text(page)
names=['LICENSE','NOTICE.md','index.html','search.json','validation.json','regression-validation.json','viewer-validation.json','promotion.json','review-images.json','review-mesh.json.gz','mesh.json','viewer-current.png']
names+=[r['file'] for r in review['images']];names+=[f.name for f in O.glob('*.FCStd')]
manifest={'promoted':True,'manufacturing_ready':False,'source_head_before':p['source_head_before'],'files':[],'source_sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [*R.glob('tools/*backbox_lock*.py'),R/'config/backbox_lock_integration_v32.json',R/'studies/backbox-lock-integration-v32/render.py',R/'studies/backbox-lock-integration-v32/README.md']}}
for name in sorted(set(names)):
    b=(O/name).read_bytes();assert len(b)<100_000_000
    manifest['files'].append({'file':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(O/'artifact-index.json').write_text(json.dumps(manifest,indent=2)+'\n');print('BACKBOX_LOCK_PACKAGE_PASS',len(manifest['files']),round(sum(x['bytes'] for x in manifest['files'])/1e6,2),'MB')

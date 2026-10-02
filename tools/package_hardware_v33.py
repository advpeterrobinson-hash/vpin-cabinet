"""Offline V33 delivery index and explicit artifact whitelist. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,html,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/hardware-v33'
C=json.loads((R/'config/hardware_catalog_v33.json').read_text());W=json.loads((R/'config/wood_materials_v33.json').read_text());Q=json.loads((O/'validation.json').read_text());models=json.loads((O/'cad-library-validation.json').read_text());views=json.loads((O/'review-views.json').read_text())
assert Q['pass'] and all(x['pass'] for x in Q['checks'])
for n,h in Q['input_sha256'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
status={x['id']:x['model_status'] for x in models['models']}
lines=['# Hardware status — V33','','All families remain provisional. PURCHASE_BEFORE_CNC means actual hardware must qualify the interface before dependent machining; optional/future classes remain conditional. No final SKU, strength rating, torque or price is implied.','','| ID | Description | Qty | Class | Freeze / purchase status | CAD authority |','| --- | --- | ---: | --- | --- | --- |']
for i in C['hardware']:lines.append('| '+i['id']+' | '+i['description_en']+' | '+('TBD' if i['quantity'] is None else str(i['quantity']))+' | '+i['flatpack_classification']+' | '+i['freeze_status']+' | '+status[i['id']]+' |')
(O/'hardware-status.md').write_text('\n'.join(lines)+'\n')
lines=['# Wood material-class map — V33','','Premium first. Secondary substitution is conditional on the extra-sheet nesting trigger, stock quality and payload/joint qualification; structural parts never move automatically. Quantities count current components/known leg laminations, not a final nesting release. Hardwood dowel H01 is separate from plywood.','','| ID | CURRENT object | Class | Quantity | Thickness mm | Decomposition status |','| --- | --- | --- | ---: | --- | --- |']
for p in W['parts']:lines.append('| '+p['id']+' | '+p['object']+' | '+p['material_class']+' | '+str(p['quantity'])+' | '+str(p['nominal_thickness_mm'] or 'TBD')+' | '+p['status']+' |')
(O/'wood-material-map.md').write_text('\n'.join(lines)+'\n')
tools=json.loads((O/'tools.json').read_text());lines=['# Provisional assembly tools / Ferramentas provisórias','','Exact drive/socket/pilot size follows purchased hardware. Major woodworking operations remain CNC-shop work.','','| ID | EN / PT-BR | Requirement | Application |','| --- | --- | --- | --- |']
for t in tools:lines.append('| '+t['id']+' | '+t['en']+' / '+t['pt_BR']+' | '+t['classification']+' | '+t['families']+' |')
(O/'tools.md').write_text('\n'.join(lines)+'\n')
links=[('flatpack-bom-en.md','BOM EN'),('flatpack-bom-pt-BR.md','BOM PT-BR'),('bom.json','Machine-readable BOM'),('bom.csv','CSV'),('hardware-status.md','Hardware status'),('purchase-before-cnc.md','Before CNC'),('purchase-before-assembly.md','Before assembly'),('optional-accessories.md','Optional accessories'),('future-electronics.md','Future electronics/adapters'),('tools.md','Tools'),('wood-material-map.md','Wood classes'),('assembly-dependencies.json','Assembly dependencies'),('exploded-metadata.json','Exploded metadata'),('validation.json','Validation'),('../../../config/hardware_catalog_v33.json','Canonical catalog'),('../../../library/hardware/README.md','CAD library'),('../../../studies/hardware-v33/README.md','Engineering report')]
cards=[]
for v in views:
    n=v['number'];title=html.escape(n+' — '+v['title']);installed=''
    if v['installed_cad']:installed=f'<p><a href="{n}-installed.png">Installed CAD image</a> · <a href="{v["installed_cad"]}">Installed FCStd</a></p>'
    cards.append(f'<article><h2>{title}</h2><a href="{n}-review.png"><img loading="lazy" src="{n}-review.png" alt="{title}"></a><p><a href="{v["cad"]}">Family-board FCStd</a></p>{installed}</article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V33 hardware and flatpack BOM</title><style>body{font:16px/1.55 system-ui,sans-serif;max-width:1440px;margin:32px auto;padding:0 24px;background:#f7f9fb;color:#233746}h1{font-size:30px}h2{font-size:18px}a{color:#165d82}.notice{border-left:5px solid #ad6537;padding:10px 22px;background:#fff2df}nav{display:flex;flex-wrap:wrap;gap:10px 24px;margin:24px 0}article{background:white;padding:18px;border:1px solid #d4dce0;border-radius:6px}img{width:100%;height:360px;object-fit:contain;object-position:top}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:22px}footer{font-size:13px;margin-top:32px}</style><h1>V33 mechanical hardware library + flatpack BOM</h1>
<div class="notice"><strong>INVENTORY / LIBRARY ONLY — MANUFACTURING BLOCKED</strong><p>CURRENT V32 wood, holes, poses and viewer are byte-identical to the accepted HEAD. All 438 current/blank-state CAD objects are accounted for. 148 canonical families, including 91 required and 22 optional; electronics and user adapters stay separate.</p><p>The inventory is complete as an audit. 13 required rows still need quantity/coverage decisions, and 11 wood objects need a CNC decomposition/thickness plan. Null/TBD is not zero. No prices, hardware freeze or manufacturing release.</p></div>
<nav>'''+''.join(f'<a href="{u}">{html.escape(t)}</a>' for u,t in links)+'''</nav><p>Actual CAD review atlases: one representative per family, independent image-cell scales. Native family boards are 1:1. Installed companion views use exact CURRENT coordinates. Orange crosses mark unresolved interfaces, not fabricated hardware. WPC schematics remain measurement holds.</p><main class="grid">'''+''.join(cards)+'''</main><footer>CERN-OHL-S-2.0 · <a href="LICENSE">LICENSE</a> · <a href="NOTICE.md">NOTICE</a> · Source Location: <a href="https://github.com/advpeterrobinson-hash/vpin-cabinet">vpin-cabinet</a>. Offline page; no remote assets or scripts.</footer></html>'''
(O/'index.html').write_text(page)
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
paths=[p for p in O.iterdir() if p.suffix in ['.md','.html','.json','.csv','.png','.gz','.FCStd'] and p.name!='artifact-index.json']+[O/'LICENSE']
paths += [R/i['model']['path'] for i in C['hardware']]+[(R/i['model']['path']).with_suffix('.json') for i in C['hardware']]
paths += list((R/'library/hardware').glob('*.json'))+[R/'library/hardware/README.md',R/'library/hardware/.gitignore']
paths += [R/'config/hardware_catalog_v33.json',R/'config/wood_materials_v33.json',R/'studies/hardware-v33/README.md',R/'studies/hardware-v33/render.py']+list(R.glob('tools/*hardware*v33.py'))+[R/'tools/build_bom_v33.py',R/'tools/export_bom_v33.mjs']
manifest={'source_head':C['source_head'],'manufacturing_ready':False,'files':[]}
for p in sorted(set(paths)):
    b=p.read_bytes();assert len(b)<100_000_000
    manifest['files'].append({'file':str(p.relative_to(R)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(O/'artifact-index.json').write_text(json.dumps(manifest,indent=2)+'\n')
stage=[x['file'] for x in manifest['files']]+[str((O/'artifact-index.json').relative_to(R))]
(R/'.work/hardware-v33/artifacts.nul').write_bytes(('\0'.join(stage)+'\0').encode())
print('HARDWARE_V33_PACKAGE_PASS',len(stage),'files',round(sum(x['bytes'] for x in manifest['files'])/1e6,2),'MB')

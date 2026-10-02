"""Validate and whitelist the V33.1 review package. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,csv,html,shutil,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/flatpack-v331'
read=lambda p:json.loads(Path(p).read_text())
D=read(O/'manufacturing-register.json');V=read(O/'validation.json');S=read(O/'summary.json');B=read(O/'manufacturing-bom.json');views=read(O/'review-views.json');exports=read(O/'review-export-index.json');layout=read(O/'preliminary-layout.json')
assert V['pass'] and all(x['pass'] for x in V['checks']) and V['unchanged_starting_files']==1529
assert D['generator_sha256']==hashlib.sha256((R/'tools/flatpack_v331_entry.py').read_bytes()).hexdigest()
assert len(D['parts'])==130 and len(B['rows'])==66 and sum(p['quantity'] for p in B['rows'])==130
assert all(p['manufacturing_status'] in ['ONE_SIDE_CNC_READY','ONE_SIDE_CNC_PLUS_MANUAL_FINISH'] for p in D['parts'])
assert not S['full_sheet_release'] and not layout['production_authorized'] and len(layout['sheets'])==6
assert len(views)==16 and len(exports)==66
with (O/'manufacturing-bom.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==66 and sum(int(r['quantity']) for r in rows)==130
assert {r['manufacturing_part_id'] for r in rows}=={p['manufacturing_part_id'] for p in B['rows']}
for e in exports:
 x=ET.parse(O/e['svg']);groups={g.attrib.get('id') for g in x.findall('{http://www.w3.org/2000/svg}g')}
 assert set(['CUT','POCKET','LOCATOR','ENGRAVE','REFERENCE'])<=groups
 assert 'NOT FOR CNC' in (O/e['svg']).read_text()
 dx=(O/e['dxf']).read_text().splitlines();assert len(dx)%2==0 and 'EOF' in dx and 'AC1015' in dx
for sh in layout['sheets']:
 for p in sh['placements']:
  assert p['x_mm']>=20 and p['y_mm']>=20 and p['x_mm']+p['width_mm']<=2480+1e-6 and p['y_mm']+p['height_mm']<=1580+1e-6
# Every actual source stays unchanged; source hashes cover supplier values too.
for n,h in D['source_sha256'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
links=[('manufacturing-wood-bom-en.md','Wood BOM EN'),('manufacturing-wood-bom-pt-BR.md','Wood BOM PT-BR'),('manufacturing-bom.csv','CSV'),('manufacturing-bom.json','JSON BOM'),('manufacturing-register.json','Complete one-face register'),('decomposition-report.md','Decomposition'),('operation-face-report.md','Operation faces'),('manual-finish-schedule.md','Manual finish'),('stock-thickness-families.md','Stock families'),('fit-dependent-joints.md','Fit-dependent joints'),('hardware-interface-holds.json','Hardware holds'),('sheet-feasibility.md','Sheet feasibility'),('part-id-engraving-map.json','Optional part-ID map'),('hardware-quantity-closure.md','Hardware quantities'),('validation.json','Regression evidence'),('review-export-index.json','DXF/SVG review index'),('manufacturing-members.FCStd','Local member CAD'),('installed-members.FCStd','Rebuilt installed CAD'),('exploded-wood-review.FCStd','Exploded wood CAD'),('../../../studies/flatpack-v331/README.md','Engineering report')]
cards=[]
for view in views:
 assert (O/view['image']).exists()
 cards.append('<article><h2>'+html.escape(view['number']+' '+view['title'])+'</h2><a href="'+view['image']+'"><img loading="lazy" src="'+view['image']+'" alt="'+html.escape(view['title'])+'"></a></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V33.1 flatpack manufacturing review</title><style>body{font:16px/1.5 system-ui,sans-serif;max-width:1440px;margin:32px auto;padding:0 24px;color:#243e4d;background:#f8fafb}a{color:#185c7d}nav{display:flex;flex-wrap:wrap;gap:10px 24px;margin:24px 0}.notice{background:#fff1d9;border-left:5px solid #ad6537;padding:12px 20px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:20px}article{padding:16px;background:white;border:1px solid #cbd5dc}h2{font-size:17px}img{width:100%;height:340px;object-fit:contain;object-position:top}footer{margin-top:30px;font-size:13px}</style><h1>V33.1 flatpack manufacturing decomposition</h1><div class="notice"><strong>PRELIMINARY — NOT FOR CNC</strong><p>93 installed components → 130 pieces / 66 families. All 15 decomposition holds resolved. 71 one-face CNC routes; 59 routes include explicit manual finish. Actual material, coupon, hardware and structural/finish qualification still block full-sheet release.</p><p>CURRENT geometry and supplier values unchanged. Saved member unions differ by 0 mm³. No production nesting or G-code.</p></div><nav>'''+''.join(f'<a href="{u}">{html.escape(t)}</a>' for u,t in links)+'''</nav><main class="grid">'''+''.join(cards)+'''</main><footer>CERN-OHL-S-2.0 · <a href="LICENSE">LICENSE</a> · <a href="NOTICE.md">NOTICE</a> · Source Location: <a href="https://github.com/advpeterrobinson-hash/vpin-cabinet">vpin-cabinet</a>. Offline review page; CURRENT viewer unchanged.</footer></html>'''
(O/'index.html').write_text(page)
# Keep only referenced B-reps; scratch outputs and previous failed-run orphans never enter Git.
paths=set()
def walk(x):
 if isinstance(x,dict):
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
 elif isinstance(x,str) and x.endswith('.brep'):paths.add(R/x)
walk(D)
for p in O.iterdir():
 if p.is_file() and p.suffix in ('.md','.json','.FCStd','.gz','.png','.html','.csv') and p.name!='artifact-index.json':paths.add(p)
paths.add(O/'LICENSE')
for e in exports:
 paths.add(O/e['svg']);paths.add(O/e['dxf'])
for n in ['config/manufacturing/flatpack_v331.json','config/manufacturing/part_ids_v331.json','studies/flatpack-v331/README.md','studies/flatpack-v331/render.py','tools/flatpack_v331_entry.py','tools/build_flatpack_v331_reports.py','tools/verify_flatpack_v331_entry.py','tools/export_flatpack_v331_review.py','tools/export_flatpack_bom_v331.mjs','tools/package_flatpack_v331.py']:paths.add(R/n)
manifest={'source_head':D['source_head'],'full_sheet_release':False,'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]}
(O/'artifact-index.json').write_text(json.dumps(manifest,indent=2)+'\n')
paths.add(O/'artifact-index.json');(R/'.work/flatpack-v331/artifacts.nul').write_bytes(('\0'.join(str(p.relative_to(R)) for p in sorted(paths))+'\0').encode())
print('FLATPACK_V331_PACKAGE_PASS',len(paths),'files;',round(sum(x['bytes'] for x in manifest['files'])/1e6,2),'MB')

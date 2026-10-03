"""Publish checked review evidence, never CNC release. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,html
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/solid-leg-v334'
read=lambda n:json.loads((O/n).read_text())
eng=read('engineering-validation.json');browser=read('browser-validation.json');legacy=read('legacy-browser-validation.json');geo=read('viewer-regression.json')
digest=hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
assert eng['pass'] and browser['pass'] and legacy['pass']
assert browser['viewer_sha256']==legacy['viewer_sha256']==geo['viewer_html_sha256']==digest
v={'pass':True,'head_before':eng['head_before'],'source_mesh_sha256':geo['source_mesh_sha256'],'viewer_sha256':digest,'geometry_changed':False,'manufacturing_release':False,'final_leg_drilling_released':False,'engineering_checks':len(eng['checks']),'browser_checks':len(browser['checks'])+len(legacy['checks']),'geometry_protection':'engineering-validation.json','print_qualification':'HOLD','hand_drill_clearance':'HOLD_SELECTED_HARDWARE_TOOL_CLAMP_AND_PHYSICAL_TRIAL'}
(O/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
views=read('review-views.json');gallery=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>V33.4 review</title><style>body{font:16px system-ui;max-width:1100px;margin:30px auto;padding:16px;background:#edf1f3;color:#20313c}img{width:100%;background:white}article{margin:24px 0}a{color:#165a7b}</style><h1>Solid leg blocks + drill jig · V33.4</h1><p>REFERENCE ONLY · hardware, print and drilling qualification HOLD. CURRENT geometry unchanged.</p><p><a href="README.md">Engineering report / relatório</a> · <a href="../viewer-v32/index.html">Offline viewer</a></p>']
for f in sorted(O.glob('0?-*.svg')):gallery.append(f'<article><h2>{html.escape(f.stem)}</h2><img src="{f.name}" alt="{html.escape(f.stem)}"></article>')
for view in views:gallery.append(f'<article><h2>{html.escape(view["title"])}</h2><img src="{view["image"]}" alt="{html.escape(view["title"])}"></article>')
gallery.append('<p>CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet</p></html>');(O/'index.html').write_text(''.join(gallery))
print('V334_PACKAGE_PASS',v)

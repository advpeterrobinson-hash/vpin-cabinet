"""Package the validated viewer/manual review, never CNC output. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,html,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/viewer-v332'
read=lambda n:json.loads((O/n).read_text());V=read('validation.json');B=read('browser-validation.json');views=read('review-views.json');assert V['pass'] and B['pass']
assert V['viewer_sha256']==B['viewer_sha256']==hashlib.sha256((R/'exports/generated/viewer-v32/index.html').read_bytes()).hexdigest()
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
links=[('../viewer-v32/index.html','Open offline viewer / Abrir visualizador'),('../../../docs/ASSEMBLY_MANUAL.md','Assembly manual EN'),('../../../docs/ASSEMBLY_MANUAL.pt-BR.md','Manual de montagem PT-BR'),('assembly-manual.json','Machine-readable manual'),('validation.json','Source and metadata regression'),('browser-validation.json','Browser and touch evidence'),('hardware-lod-validation.json','Hardware visualization source'),('../../../studies/viewer-v332/README.md','Engineering report')]
body=''.join(f'<article><h2>{x["number"]} · {html.escape(x["title"]["en"])}</h2><p>{html.escape(x["title"]["pt-BR"])}</p><a href="{x["image"]}"><img loading="lazy" src="{x["image"]}" alt="{html.escape(x["title"]["en"])}"></a></article>' for x in views)
(O/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V33.2 viewer and assembly framework</title><style>body{font:16px/1.5 system-ui;color:#20313c;background:#f4f7f9;max-width:1500px;margin:30px auto;padding:0 20px}nav{display:flex;gap:14px 24px;flex-wrap:wrap;margin:20px 0}a{color:#165a7b}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:20px}article{background:white;padding:16px;border:1px solid #c6d2d9}img{width:100%;height:350px;object-fit:contain}h2{font-size:17px}.hold{border-left:4px solid #9b6632;background:#fff0d8;padding:14px}</style><h1>V33.2 · Viewer and assembly-manual framework</h1><p class="hold">REVIEW ONLY — Manufacturing release remains blocked. CURRENT and V33.1 geometry unchanged. Manual statuses are preparation holds, not manufacturing approval.</p><p>18 visibility groups · 130 manufacturing pieces · V33 hardware · 19 stages / 31 steps / 31 checkpoints · EN / PT-BR · offline.</p><nav>'''+''.join(f'<a href="{u}">{html.escape(t)}</a>' for u,t in links)+'</nav><div class="grid">'+body+'</div><footer>CERN-OHL-S-2.0 · <a href="NOTICE.md">NOTICE</a> · <a href="LICENSE">LICENSE</a> · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet</footer></html>')
report=f'''# V33.2 — inspection viewer and assembly-manual framework

The CURRENT offline viewer now supports direct interior inspection, 18 visibility groups, canonical part search, metadata, semantic exploded views and an embedded bilingual assembly framework. The detailed wood mode contains **all 130 V33.1 manufacturing pieces**, not separated copies of compound installed solids.

HEAD BEFORE: `a1f8bb04f7cec6a2220355c6b7ead0e7e0e92ab4`.
HEAD AFTER: the delivery commit containing this report on `feat/cabinet-review-v32`.

[Open viewer](../../exports/generated/viewer-v32/index.html) · [20 review images](../../exports/generated/viewer-v332/index.html) · [Manual EN](../../docs/ASSEMBLY_MANUAL.md) · [Manual PT-BR](../../docs/ASSEMBLY_MANUAL.pt-BR.md) · [Manual JSON](../../exports/generated/viewer-v332/assembly-manual.json).

## Inspection and service states

- One tap hides the playfield, or playfield plus fixed cradles. Interior inspection also hides the matrix while retaining shell, shelves, PCBase, fan stations, SSF and relevant hardware.
- Backbox interior uses the saved 100° door-open geometry, saved flexible loops and retracted latch meshes. Glass/display visibility is an inspection aid. The carrier, cassette, side toy zones, passage, locks and WPC reserves remain inspectable. Individual doors can also be picked and hidden.
- Twelve named states include play, inspection, 50° playfield service, 48 mm lift-out, matrix removal, rear doors open, locks parked, 45°/90° fold and both exploded modes. States are exclusive, so the UI does not combine open doors with folding.
- Normal fold remains: open rear doors → release/park two locks → close/latch doors → remove MAIN PLAYFIELD GLASS and MATRIX → fold. Backbox glass and cassette remain installed. No routine electronics disconnection.
- Rare WPC hinge maintenance is separate and may require cassette removal and playfield lift-out/removal. Saved service geometry does not qualify a physical raised-playfield support or load case.
- Nine camera presets, clipping, shell opacity, hide/isolate/focus and image capture remain available. Group visibility does not reset the camera. The control panel collapses for the model area; no hover interaction is required.

## IDs and exploded architecture

Installed labels use readable aliases such as SideL, T1, S2 and BBFloor, linked to P assembly IDs and permanent M manufacturing families. Selection includes both language names, assembly/manual stage, material, nominal stock thickness, quantity authority, route, hardware ID and purchase/freeze status. Search accepts these aliases and M/F/H/etc IDs. Selection uses an edge overlay and bounding outline as well as contrast.

Overview offsets separate semantic assemblies moderately. Detailed offsets move sides outward, end structures longitudinally, floor vertically, shelves upward, and hardware opposite catalogued installation directions. Washers follow the same axis. Actual laminate centers establish ordered Z separation; intake faces/top/returns move along their assembly directions. Opposing FACE A normals do not collapse the retainer cap/strip into one position. Focused decomposition views carry part-ID labels.

All 148 V33 catalog families are represented with their existing authority, including reference/electronics families. **{V['unlocated_hardware_families']} families have no authoritative displayed installation position** and use one labelled exemplar in a separate tray. Unresolved crosses remain identified as markers, not purchased hardware shapes. Their tray coordinates are documentation layout only. Unknown quantities remain null/formula-driven; no hole positions or hardware counts were invented. The existing 13 unresolved required rows remain six formulas and seven genuinely TBD.

Wood/hardware filters and main-cabinet/playfield/backbox/all scopes limit clutter. Dedicated filters expose 28 leg layers, eight intake-baffle panels, the cap/strip, monitor-stop laminations and cassette-cleat laminations. Exploded offsets are **not validated removal trajectories**.

## Manual framework

The English source and complete PT-BR version contain **19 stages, 31 steps and 31 checkpoints**. Each step records component/hardware IDs, stage/global quantities, orientation, tools, FACE A/B authority, action, check, hold and a linked CAD state. Quantities repeated in multiple steps are reference totals, not repeated consumption.

The per-piece annex has 130 orientation cards plus exact CNC/manual metadata. It distinguishes CNC contour/pocket work from drilling, countersinking, corner finish and bevel sanding; the 59 manual-finish routes retain their operations and depth references. FACE B has no CNC. Actual thickness, coupon, hardware, guide/finish, adhesive and load qualification remain explicit holds. No final PDF was generated.

The embedded manual offers an exploded stage subset and a cumulative assembled stage view using real members. On desktop its panel reserves space beside the model. The sequence is a **framework**, not a physically rehearsed or released assembly procedure. Electronics remain a later optional overview.

## Performance and validation

The single-file viewer embeds compressed data and licensed Three.js/OrbitControls; it requires no server or network request. Detailed GPU objects are created only when needed. V33 source B-reps are tessellated for display at 0.8 mm linear / 0.4 rad angular settings, with no helical threads. The complete detailed dataset has approximately 315,000 triangles; that display LOD is never used for CNC or collision proof. The file is approximately {(R/'exports/generated/viewer-v32/index.html').stat().st_size/1e6:.1f} MB.

The browser suite passed **{len(B['checks'])} checks**, with networking disabled, English/Original defaults, bilingual/Accessible toggles, state prerequisites, search, non-color selection, touch emulation and 44 px controls. Desktop 1600×1050 and tablet layouts 1024×1366 / 834×1194 were checked. Measured initial load on the test machine was {B['load_ms']} ms; this is not a physical-tablet frame-rate guarantee.

The metadata/source suite passed **{len(V['checks'])} checks**. **{V['protected_file_count']} pre-existing authority files** match their starting Git blobs, including CURRENT B-reps, V33 hardware, V33.1 pieces, supplier profile and release flags. All 130 wood meshes retain original triangle topology and exact installed transforms; rendering copies round coordinates by at most {V['manufacturing_member_visual_rounding_max_mm']:.8f} mm. No accepted hole, fit or B-rep geometry changed. The prior zero-volume reconstruction proof remains unchanged; no new collision or structural certification is claimed.

[Metadata/source evidence](../../exports/generated/viewer-v332/validation.json) · [Browser evidence](../../exports/generated/viewer-v332/browser-validation.json) · [LOD source hashes](../../exports/generated/viewer-v332/hardware-lod-validation.json).

## Required report

| Field | Result |
| --- | --- |
| Hide playfield / supports | YES / YES |
| Interior / backbox inspection | YES / YES |
| Visibility groups | 18 |
| Search / part metadata | YES / YES |
| Tablet touch controls | PASS in browser touch emulation |
| Offline / EN–PT-BR | PASS / PASS |
| Original / Accessible palettes | PASS / PASS |
| Overview / detailed explosion | PASS / PASS |
| Wood-only / hardware-only | PASS / PASS |
| Real V33.1 pieces / V33 models | YES / YES |
| English / PT-BR manual | YES / YES |
| Stages / steps / checkpoints | 19 / 31 / 31 |
| Hardware uncertainty honest | YES; unknown counts preserved |
| One-sided manual finish represented | YES; all 130 preparation records, 59 affected pieces |
| CURRENT / manufacturing geometry changed | NO / NO |
| Manufacturing release | **STILL BLOCKED** |

## Reproduction

```sh
freecadcmd tools/viewer_v332_lod_entry.py
python3 tools/build_review_viewer.py
python3 tools/check_assembly_viewer_v332.py
python3 tools/check_assembly_metadata_v332.py
python3 tools/check_current_v32.py
python3 tools/package_viewer_v332.py
```

The browser runner needs an existing Playwright installation and Chrome. Set `VPIN_NODE_MODULES` if its dependency root is elsewhere. The viewer itself does not need these development dependencies. Historical V32 controls can still be generated into an isolated output using `build_review_viewer.py --legacy`; the default now follows [V33.2 documentation authority](../../config/viewer_v332.json).

Require explicit PASS sentinels for FreeCAD scripts; an exit code alone is insufficient. No supplier values, production vectors, G-code or manufacturing release were changed.

CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.
'''
(R/'studies/viewer-v332/README.md').write_text(report)
paths={p for p in O.rglob('*') if p.is_file() and (p.suffix in ['.json','.gz','.svg','.png','.html','.md'] or p.name=='LICENSE') and p.name not in ['viewer-data.json','artifact-index.json']}
for name in ['config/viewer_v332.json','docs/ASSEMBLY_MANUAL.md','docs/ASSEMBLY_MANUAL.pt-BR.md','exports/generated/viewer-v32/index.html','tools/build_review_viewer.py','tools/check_current_v32.py','tools/build_assembly_viewer_v332.py','tools/viewer_v332_lod_entry.py','tools/check_assembly_viewer_v332.py','tools/check_assembly_viewer_v332.mjs','tools/check_assembly_metadata_v332.py','tools/package_viewer_v332.py','studies/viewer-v332/README.md']:
 paths.add(R/name)
paths.update(p for p in (R/'tools/viewer-v332').iterdir() if p.is_file())
manifest={'head_before':V['head_before'],'geometry_changed':False,'manufacturing_release':False,'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]}
(O/'artifact-index.json').write_text(json.dumps(manifest,indent=2)+'\n');paths.add(O/'artifact-index.json')
(R/'.work/viewer-v332/artifacts.nul').write_bytes(('\0'.join(str(p.relative_to(R)) for p in sorted(paths))+'\0').encode());print('V332_PACKAGE_PASS',len(paths),'files')

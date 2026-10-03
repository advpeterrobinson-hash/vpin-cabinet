"""Scale-explicit SW02 shop specification / reference templates. CERN-OHL-S-2.0.
Center-location aid only; purchased hardware and guide qualification still held.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/service-productization-v338'
reg=json.loads((O/'manufacturing-register.json').read_text());a=json.loads((O/'manufacturing-audit.json').read_text());assert a['pass']
parts=[p for p in reg['parts'] if p['manufacturing_part_id']=='SW02'];assert len(parts)==2
for p in parts:
 side='L' if p['assembly_id']=='P095' else 'R'
 paths=p['reference_drill_paths'];top=[q for q in paths if q['axis_local']==[0,0,-1]];inner=[q for q in paths if q['axis_local']==[-1,0,0]]
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><rect width="210" height="297" fill="white"/><g font-family="sans-serif" fill="#111" font-size="3.2">',f'<text x="12" y="14" font-size="5">SW02 {side} — solid front landing</text>', '<text x="12" y="21" fill="#9a2317">REFERENCE ONLY — NOT RELEASED FOR DRILLING</text>', '<text x="12" y="28">Shop blank: 68 × 70 × 54 mm. No glue-up / binder screws.</text>', '<text x="12" y="34">Dry, stable, straight, knot-free structural wood; species qualification HOLD.</text>', '<text x="20" y="44">TOP A · U inward, V rearward</text>', '<text x="110" y="44">INNER B · V rearward, W up</text>', '<rect x="20" y="50" width="68" height="70" fill="none" stroke="#111" stroke-width=".25"/>','<rect x="110" y="50" width="70" height="54" fill="none" stroke="#111" stroke-width=".25"/>','<text x="20" y="125">FRONT = upper edge; wall = left edge</text>','<text x="110" y="109">TOP = upper; FRONT = left edge</text>']
 def mark(x,y):return f'<path d="M{x-3},{y}h6 M{x},{y-3}v6" fill="none" stroke="#111" stroke-width=".2"/><circle cx="{x}" cy="{y}" r=".7" fill="none" stroke="#111" stroke-width=".2"/>'
 for v,label in [(20,'M8'),(50,'M6')]:svg.extend([mark(74,50+v),f'<text x="{78}" y="{49+v}">{label}</text>'])
 for q in inner:
  _,v,w=q['entry_local_uvw_mm'];svg.append(mark(110+v,104-w))
 lines=['Datum centers below are copied from actual CURRENT bore axes; diameters remain HOLD.', 'TOP A: M8 axis U54 / V20; M6 axis U54 / V50.', 'INNER B: V9 and V61, each at W9 and W45.', 'Grain along U / 68 mm cantilever length is provisional. Label TOP / FRONT / INNER / L or R.', '', 'Paper marks positions only. A paper sheet cannot guide a long bore.', 'Use a clamped commercial 90° portable drill guide and depth stops.', 'Qualify guide reach, perpendicularity and drill-point allowance on the same wood.', 'Reference paths: top54 mm through; side68 mm through; receiver16 mm blind.', 'Final pilots, clearances, head recesses and insert depth require purchased hardware.', 'Do not copy these reference diameters into a production instruction.', 'Side-hole centers are9 mm from ends; reference Ø9 head leaves4.5 mm wood.', 'Species, splitting and attachment/load proof remain physical qualification holds.', '', 'Cabinet SIDE and M025 receiver machining remains separately held and uncut.', 'Do not glue SW02 to the cabinet wall. Keep all four existing side screws per block.', 'Use the accepted positioning template/datum; do not measure structural placement by eye.']
 for i,line in enumerate(lines):svg.append(f'<text x="12" y="{139+5*i}">{line}</text>')
 svg+=['<path d="M20,248v5 M20,250h100 M120,248v5" stroke="#111" fill="none" stroke-width=".25"/>','<text x="20" y="258">100 mm calibration — print100%, no Fit to page</text>','<path d="M190,228h5 M192,228v50 M190,278h5" stroke="#111" fill="none" stroke-width=".25"/>','<text x="130" y="274">Vertical bar =50 mm</text>','<text x="12" y="286">CERN-OHL-S-2.0 · Source: github.com/advpeterrobinson-hash/vpin-cabinet</text>','</g></svg>']
 (O/f'SW02-{side}-reference-template.svg').write_text(''.join(svg))
report={'version':'V33.8','manufacturing_release':False,'template_status':'REFERENCE_ONLY_NOT_RELEASED_FOR_DRILLING','source_register_sha256':hashlib.sha256((O/'manufacturing-register.json').read_bytes()).hexdigest(),'scale':'SVG physical210×297 mm; print100%, verify100 mm horizontal and50 mm vertical bars','templates':[f'SW02-{s}-reference-template.svg' for s in 'LR'],'guide':'Clamped commercial perpendicular portable drill guide, qualified on same wood; no precise freehand drilling','new_printed_jig_required':False,'purchased_hardware_required':True,'no_opposite_face_CNC':True}
(O/'sw02-template-status.json').write_text(json.dumps(report,indent=2)+'\n')
print('V338_SW02_TEMPLATES_PASS',2)

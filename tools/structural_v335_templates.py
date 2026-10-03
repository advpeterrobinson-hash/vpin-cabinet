"""Full-scale station-position sheets; no commercial jig/drill geometry. CERN-OHL-S-2.0."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];C=json.loads((R/'config/structural_simplification_v335.json').read_text());O=R/'templates/pocket-holes';O.mkdir(parents=True,exist_ok=True);manifest=[]
for part,id,base,length,key,prefix in [('Floor','M005',18,1272.1,'floor_y_mm','floor'),('RearBearingShelf','M018',1127.125,162.975,'shelf_y_mm','rear-bearing')]:
 for side in ['left','right']:
  H=max(length+150,380);W=250;title=f'{id} {part} {side.upper()} — UNDERSIDE / FACE A datum'
  svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">','<metadata>CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; positioning reference only; no manufacturing release</metadata>','<rect width="100%" height="100%" fill="white"/>','<g font-family="sans-serif" font-size="4" fill="black">',f'<text x="8" y="10">{title}</text>','<text x="8" y="18">PRINT AT 100% · ACTUAL SIZE · DO NOT FIT TO PAGE</text>','<text x="8" y="25">IMPRIMIR 100% · TAMANHO REAL · SEM AJUSTAR À PÁGINA</text>','<text x="8" y="33">HARDWARE-DEPENDENT — NOT A DRILLING RELEASE</text>','<text x="8" y="40">Station lines only. Kreg reference-to-bit offset: TBD.</text>','<text x="8" y="47">Face A: floor underside; shelf TOP datum, underside manual work.</text>']
  ox,oy=35,70
  svg += [f'<path d="M{ox} {oy}V{oy+length}" stroke="black" stroke-width="0.35"/>',f'<text x="8" y="{oy-5}">FRONT / FRENTE — Y{base}</text>',f'<text x="8" y="{oy+length+8}">REAR / TRASEIRA — Y{base+length}</text>',f'<path d="M20 {oy+20}v35m-3 -6l3 6 3 -6" stroke="black" fill="none"/>','<text x="55" y="62">SIDE SEATING SHOULDER / OMBRO LATERAL</text>']
  for j,y in enumerate(C['pockets'][key]):
   yy=oy+y-base
   svg += [f'<path d="M{ox-8} {yy}H{ox+85}M{ox} {yy-5}v10" stroke="black" stroke-width=".2"/>',f'<text x="{ox+90}" y="{yy+1.5}">{side[0].upper()}{j+1} · Y{y:g}</text>',f'<text x="{ox+8}" y="{yy-3}">JIG STATION / POSIÇÃO</text>']
  # Conservative end exclusion only: other station-specific obstacles are in
  # the review schedule, not silently projected into an unmeasured jig body.
  for yy in [oy,oy+length-25]:svg += [f'<rect x="{ox}" y="{yy}" width="70" height="25" fill="none" stroke="black" stroke-dasharray="2 1"/>',f'<text x="{ox+3}" y="{yy+12}">END KEEPOUT</text>']
  cy=H-118
  svg += [f'<rect x="140" y="{cy}" width="100" height="100" stroke="black" fill="none" stroke-width=".2"/>',f'<text x="147" y="{cy+48}">100 ×100 mm</text>',f'<text x="147" y="{cy+55}">VERIFY BOTH AXES</text>',f'<path d="M15 {H-25}h100m-100 -3v6m100 -6v6" stroke="black" fill="none" stroke-width=".25"/>',f'<text x="15" y="{H-31}">100 mm SCALE BAR</text>','</g></svg>']
  name=f'{prefix}-{side}.svg';(O/name).write_text('\n'.join(svg)+'\n');manifest.append({'file':name,'part_id':id,'side':side,'physical_size_mm':[W,H],'station_world_y_mm':C['pockets'][key],'datum_world_y_mm':base,'jig_reference_offset_mm':None,'print_scale':1,'calibration_square_mm':[100,100],'scale_bar_mm':100,'status':'POSITIONING_REFERENCE_HARDWARE_DEPENDENT','actual_drilling_released':False})
(O/'source-metadata.json').write_text(json.dumps(manifest,indent=2)+'\n')
(O/'README.md').write_text('''# Pocket-hole positioning sheets / Gabaritos de posicionamento

CERN-OHL-S-2.0 · [Source Location](https://github.com/advpeterrobinson-hash/vpin-cabinet)

**PRINT AT100% / ACTUAL SIZE / DO NOT FIT TO PAGE. IMPRIMIR100% / TAMANHO REAL / SEM AJUSTAR.**

Vector SVG dimensions are in millimetres. Use a vector application supporting actual-size tiled/poster printing. Browser “fit” printing is unsuitable. Verify the100×100mm square in both axes and the100mm bar after joining tiles. Never scale the drawing to fit paper. PDF can be produced later from this vector source.

These are longitudinal station-position references, NOT commercial Kreg templates. The selected jig establishes drilling angle, edge reference, drill geometry and collar. Its reference-to-bit offset remains unknown; transfer it only after physical jig/coupon qualification. Do not drill from these sheets alone. World Y is front-to-rear; use the printed front-end Y datum, not the outside cabinet edge. Left and right are viewed in installed cabinet coordinates; identify the part before turning it over.

Floor FACE_A is its underside. RearBearingShelf FACE_A remains its top; its underside pocket work is MANUAL, referenced through measured stock thickness. No second-face CNC. Counterbore, drill diameter, depth and screw remain HOLD.

M006 cleats must not be installed during underside drilling. Keep all leg, fan/filter, PCBase, WPC, lock, cable and adjacent fastener reserves clear. The full3D packaging study and selected stations are in [the V33.5 report](../../exports/generated/structural-v335/README.md). End keepouts are shown; physical jig-body/driver clearance still requires the purchased tool.

Os SVG vetoriais têm dimensões em milímetros. Imprima em mosaico em aplicativo vetorial com tamanho real. Confira quadrado100×100 e barra100mm após unir folhas. As linhas marcam posições longitudinais, não a geometria Kreg. Referência/broca, ângulo, colar e parafuso dependem do gabarito comprado e do cupom. Não fure usando apenas estas folhas. M006 entra depois. No piso, FACE_A é inferior; na prateleira traseira, FACE_A continua superior e o acabamento inferior é manual referenciado pela espessura medida. Sem CNC na segunda face.
''')
print('V335_TEMPLATES_PASS',len(manifest))

"""Generate evidence-linked V33.7 review; no manufacturing release.
CERN-OHL-S-2.0. Source https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/two-stock-user-module-v337'
def read(n):return json.loads((O/n).read_text())
module=read('module-validation.json');assert module['pass']
reg=read('manufacturing-register.json');mass=read('mass-budget.json');material=read('material-utilization.json');comparison=read('manufacturing-metrics-comparison.json');packing=read('packaging.json');checks=read('validation.json');assert checks['pass']
base='../exports/generated/two-stock-user-module-v337/'
lines=['# V33.7 — two plywood families and removable user module','',
'HEAD BEFORE: `c02f9b878f370441b2bc3e637a3030f681fe140a`.',
'HEAD AFTER: the commit containing this report; read `git log -1 --format=%H -- docs/TWO_STOCK_USER_MODULE_V337.md`. A commit cannot embed its own final hash.',
'',
'**Design architecture passes. Manufacturing release remains BLOCKED.** Only the authorized thin-stock conversions, FLOOR module bay and new removable plate change geometry. Unrelated installed parts, accepted holes, side buttons, playfield support positions/slope, SW01, M006, M067, WPC axis and all accepted mechanisms are preserved.',
'',
'## Selected module',
'',
'One **160 × 116 × 12 mm** rounded plate (R6), centered at X300 / Y110 on the underside of FLOOR. The owner variant has **five programmable arcade buttons plus one dual USB 3.0 module**. The button-only variant fits **six buttons** comfortably in the same external plate/bay. A blank plate keeps electronics optional. Four buttons plus USB also passed, but offers no footprint reduction with the conservative service envelopes, so the fifth button is retained.',
'',
'No permanent START/VOLUME/MODE/Bluetooth or other software function labels. Historical SERVICE_IO_V08 / DEC-016 and its220 × 55 fixed-function concept are preserved as historical evidence and superseded for CURRENT. Optional removable identification overlay may use numbers; no engraving is required.',
'',
'| Interface | Selected design reference |',
'|---|---|',
'| Plate | 160 × 116 × 12 mm, R6; M074 / P097-Main |',
'| Permanent bay | One opening132 × 88 mm, R8, in18 mm FLOOR / M005 |',
'| Locating recess | 160.4 × 116.4 mm reference, R6.2,2 mm deep from underside FACE_A |',
'| Recess study | 2 /3 /4 mm leave16 /15 /14 mm skin;2 mm chosen as shallowest positive locator |',
'| Plate installed bounds | X220–380 / Y52–168 / Z8–20 mm |',
'| Attachment | Four captive metal-thread receivers + M4 × 20 button-head reference screws; F62 ×4 / I19 ×4 |',
'| Reference attachment centers | X230 /370 paired with Y62 /158; final bores HOLD |',
'| Insert envelope | Ø8 × 10 mm blind reference;6 mm outer FLOOR skin remains |',
'| Button layout | Two rows, three cells per row;42 mm pitch; USB replaces rear-right button |',
'| Device positions | Reference cells X258 /300 /342 and Y89 /131; not final drilling authority |',
'| Service | Remove four underside screws, lower100 mm, unplug builder-selected harness and bench-service |',
'| Cable management | Two4 × 12 mm R2 slots in removable plate;250 mm planning service slack;60 × 44 × 60 mm fixed loop reserve |',
'',
'The reference locating gap0.2 mm each side is not final fit clearance. Regenerate from measured production-lot stock and coupon result. The permanent FLOOR receives no individual button or USB hole. Attachment holes are not silently cut: their reference envelopes are shown, but actual selected insert pilot and screw clearance remain PURCHASE_BEFORE_CNC. The plate is not counted as replacing structural FLOOR wood.',
'',
'## Layout and location search',
'',
'Compared single-row6 buttons,5 + USB and4 + USB against compact two-row arrangements. The single-row six-cell layouts need276 × 76 mm; the five-cell single row needs234 × 76 mm. All two-row candidates use160 × 116 mm. The selected two-row module reduces width by116 mm against six cells in one row without sacrificing the owner USB or fifth button.',
'',
'Physical reference pitch is40 mm (Ø38 nut plus2 mm clearance); selected42 mm leaves4 mm between nut envelopes. Button flanges areØ35; rear body/microswitch/wire envelopes reserve40 × 40 mm and85 mm depth behind the exterior face. These are conservative reference assumptions, not a selected hardware SKU.',
'',
'The search screens actual CURRENT B-reps at candidate positions. The selected center X300 is symmetric, and Y110 keeps the recess ahead of the tray while preserving the front captured joint. The tray support bounding box overlaps part of the search region, but the actual support is open there; exact geometry, not a bounding rectangle, gives19 mm minimum tray/support clearance.',
'',
'## USB reference and physical access',
'',
'Owner-supplied seller values are inconsistent: approximatelyØ26.0 orØ28 ±0.3 cutout,Ø26.5 body,Ø33 flange,46.8 mm rear body,33 mm nut width and8.2 mm nut thickness. Status: SELLER_REFERENCE_NOT_VERIFIED / PHYSICAL_MEASUREMENT_REQUIRED / PURCHASE_BEFORE_CNC. **USB_CUTOUT_DIAMETER_MM = null; BUTTON_BORE_MM = null.** No final hole diameter has been inferred from the envelope.',
'',
'USB points downward, with a rear-opening cap. A70 mm rear-depth reserve permits the body, nut, cable emergence and first bend. Compatibility with12 mm panel thickness is UNKNOWN until measured. The removable plate supports a one-face rear pocket if required; pocket depth remains null. This pocket must never migrate into the permanent FLOOR.',
'',
'Five finger approaches with a70 mm palm envelope, USB plug/hand approach, four underside screwdriver corridors, cap0–120° and coin door0–110° were screened. The actual rigid module withdrawal is bounded continuously for100 mm downward travel. The flexible loop is separately bounded behind the complete coin-door sweep; no invented flexible-wire trajectory is claimed.',
'',
'The conservative vertical bound between all moving coin-door solids (Z≥94) and button/wire envelopes (Z≤93) is1 mm over the complete sweep. The actual tray/support separation is19 mm; the fixed flexible-loop reserve is7 mm behind the analytically bounded coin-door sweep. These envelope checks must be repeated with purchased hardware and the real harness;1 mm is not a certified installation tolerance.',
'',
'Controls are hidden at three representative standing-front sightlines with the coin door closed, and do not extend below the cabinet lower edge Z0. This is geometric screening, not ergonomic certification. Purchased leg height, actual knees/feet, cap hinge form, harness bend radii, button force and physical reach remain prototype checks.',
'',
'## Structural and service clearances',
'',
'The through-opening leaves44 mm of full-thickness FLOOR in front of the aperture measured from the captured-front-joint rear boundary Y22. The shallow recess begins29.8 mm behind that boundary. Its16 mm shoulder skin remains continuous. Plate screws are10 mm from the external plate edges, with the final bore/insert dimensions still held. The module does not cut the front panel or captured joints.',
'',
'| Actual modeled region | Nearest module/device clearance mm |','|---|---:|']
for name,rows in module['nearest'].items():
 lines.append(f"| {name} | {min(r['distance_mm'] for r in rows):.3f} |")
lines += ['',
'Front landings remain X72 / X528,Y245; their hand/tool corridors stay clear. Side buttons remain separate leaf-button architecture at Y89/Y127 and local side top−65. Plunger, SW01 front blocks, leg backing, M006, S1 and its payload reserve remain unchanged. Locks, WPC motion, display/glass and rear-door architecture are unchanged.',
'',
'## Mandatory plywood conversion',
'',
'**Before:18 /12 /8 /6 mm. After:18 /12 mm ONLY. Forbidden CURRENT plywood stock pieces:0.** All15 thin-stock members are retained with their manufacturing IDs and converted to nominal12 mm stock. Four SW01 solid-wood blocks are excluded from the plywood-family rule. Commodity filters, rubber and hardware do not introduce a plywood family.',
'',
'| Family | Count | Conversion and preserved interface |',
'|---|---:|---|',
'| M028 floor filters | 2 | 8→12 stock; underside one-face R86 ×4 pocket and four R7 ×4 head recesses preserve media, guard and fastener mating planes; outer corners retain12 mm stock |',
'| M045 display bezel | 1 | 6→12 stock, faced from rear FACE_A to6 mm finished; visible plane and entire accepted B-rep unchanged |',
'| M058 intake filter frames | 2 | 6→12; grows outward, preserved door/airway surfaces; selected mounting fastener length requires +6 mm stack review |',
'| M059/M060/M061 baffle members | 8 | 6→12 stock, exterior growth, exact internal airflow surfaces retained; four identical M061 include one-face3 mm lower-edge rebate |',
'| M066 optional fan blanks | 2 | 6→12, exterior growth; same station; alternate to fans, never displayed simultaneously as installed fan covers |',
'',
'The M045 bezel is constrained between glass Y1114–1118 and monitor beginning Y1128. Its accepted Y1120–1126 envelope is preserved by explicit one-face facing from12 mm purchased stock. This is manufacturing removal, accounted as waste; no6 mm sheet is purchased. Similarly the M061 local9 mm web comes from12 mm stock, not9 mm sheet.',
'',
'Baffle chambers remain220 × 36 mm in section: **7920 mm² throat each**, with220 × 80 =17,600 mm² door inlet each. A naive exterior thickening initially conflicts with the passive-door-bolt reserve. The final broad lower-edge rebate is3 mm deep ×32 mm high ×36 mm long, leaving9 mm web there and12 mm in the upper66 mm. Passive-bolt clearance is2 mm; speaker clearance3.1 mm. This correction preserves a single repeated M061 family and all internal airflow geometry.',
'',
'M028 underside remains Z6, above the cabinet datum Z0;80 mm downward filter service passes. The retained12 mm corner land area is5118.85 mm² per holder. Ground service still depends on purchased legs, as before. Current fan/media/head stack planes are retained. F21/F22 intake frame screw lengths must be reselected for the extra6 mm stack; that uncertainty is visible in the hardware supplement.',
'',
'One-face status:43 ONE_SIDE_CNC_READY plywood pieces and61 ONE_SIDE_CNC_PLUS_MANUAL_FINISH;4 separately classified shop-made SW01 blocks.17 revised manufacturing members and11 installed aggregate reconstructions compare at0 mm³ difference.',
'',
'All new pockets and reductions originate from FACE_A only; FACE_B receives no CNC. No flip instructions, custom metal, production nest or G-code were added.',
'',
'## Material, mass and preliminary sheet study',
'',
f"Wood pieces: **{len(reg['parts'])}**; CNC plywood: **{reg['CNC_plywood_pieces']}**; SW01 solid blocks: **4**; canonical families: **{len(reg['families'])}**.",
'',
'| Nominal stock | Pieces | Outer contour area m² | Net projected material m² | Preliminary full sheets | Net utilization | Gross waste incl. offcuts |',
'|---|---:|---:|---:|---:|---:|---:|']
for s in material['stocks']:
 lines.append(f"| {s['thickness_mm']:g} mm | {s['pieces']} | {s['outer_contour_area_mm2']/1e6:.5f} | {s['projected_material_area_mm2']/1e6:.5f} | {s['improved_study_sheets']} | {s['utilization_percent_net']:.2f}% | {s['waste_percent_gross_including_offcuts']:.2f}% |")
lines += ['',
'The converted12 mm set still fits one preliminary12 mm sheet; no additional12 mm full sheet is required.18 mm remains two sheets. Retiring6/8 mm means no separate thin-stock purchase.',
'',
'PRELIMINARY — NOT FOR CNC.2500 × 1600 sheets,20 mm perimeter and15 mm minimum finished-part spacing remain unchanged. The deterministic placement study tries orderings with actual contour overlays, not a claimed optimized nest. Small12 mm parts share the same batch/offcuts; no special thin stock. Premium-first material policy remains. Supplier must qualify remnant hold-down and material quality.',
'',
'| Mass from B-reps / explicit planning assumptions | LOW kg | NOMINAL kg | HIGH kg |','|---|---:|---:|---:|']
for k,label in [('wood_flatpack_kg','Delivered wood, including manual-finishing stock'),('wood_finished_reference_kg','Finished wood references'),('mechanical_scenario_kg','Mechanical planning scenario'),('full_planning_build_kg','Full planning build')]:
 lines.append('| '+label+' | '+' | '.join(f'{v:.3f}' for v in mass[k])+' |')
lines += ['',f"Delivered wood mass difference versus V33.6.3: **{comparison['wood_shipping_mass_change_kg'][1]:+.3f} kg nominal**. Plywood nominal density650 kg/m³; LOW/HIGH and solid-wood density remain configurable. New unmeasured hardware is UNKNOWN, never silently zero. Optional fan blanks are included in the cut/packing BOM but excluded from simultaneous installed fan mass.",'',
'## Packaging','',
'Preferred20 kg planning-target bundles; each is below25 kg including HIGH-density wood and estimated protective packaging. This keeps the same four-bundle count with about5 kg margin to the25 kg handling ceiling. Compared with the25 kg candidate, total footprint rises1.61% and aggregate volume4.21%; long-panel protection is unchanged. The mixed fourth bundle is taller and requires careful labelled stacking. Hardware ships separately; glass and electronics are excluded. This is a handling/protection projection, not transit certification.','',
'| Bundle | External L × W × H mm | Nominal wood kg | Gross HIGH kg |','|---|---|---:|---:|']
pack=next(c for c in packing['candidates'] if c['target_kg']==packing['preferred_target_kg'])
for b in pack['bundles']:lines.append(f"| {b.get('id',b.get('package_id'))} | {' × '.join(f'{x:g}' for x in b['external_LWH_mm'])} | {b['wood_mass_kg']:.3f} | {b['gross_high_density_kg']:.3f} |")
lines += ['',
'## Verification and promotion','',
'| Evidence | Result |','|---|---|']
for file,label in [('module-validation.json','Module, candidates, human/tool/cap/coin service'),('conversion-validation.json','Thin-stock geometry'),('conversion-motion.json','Converted wood motion/service'),('combined-validation.json','Combined native and all named states'),('manufacturing-audit.json','One-face manufacturing'),('browser-validation.json','Offline viewer / tablet / bilingual controls'),('validation.json','Exact-scope and authority regression')]:
 q=read(file);lines.append(f"| [{label}]({base+file}) | {'PASS' if q['pass'] else 'FAIL'}; {len(q.get('checks',q.get('changed_audits',[])))} checks / member audits |")
lines += ['',
'Continuous differential checks cover playfield0–50°,48 mm lift-out and populated backbox0–90°. Unchanged interactions retain the exact preceding validated geometry. Combined evidence also requires the converted-wood motion and all preserved hardware-reserve audit hashes. Named poses reproduce the original state transforms before converted shapes are substituted; authoritative removed parts stay absent.',
'',
'Side buttons, front relief, landings/slope, SW01, M006, M067 and unrelated objects are regression-protected. The CURRENT nominal plywood gate rejects any thickness outside12/18, and requires both families. Historical snapshots remain untouched. New hardware rows are append-only; unknown quantities and bores are not frozen.',
'',
'Hardware dashboard:166 families;41 required Fxx families;180 known minimum fasteners plus6 formula-driven and6 genuinely TBD families. This is not a final screw count. New F62 ×4 and I19 ×4 are provisional; optional E15/E16 devices do not make electronics mandatory.',
'',
'Viewer shows UNDERFRONT USER MODULE, OWNER_CONFIG / GENERIC_CONFIG / HARDWARE_PENDING, exact native variants, removable-module service, plate/button/USB/screw/insert exploded components, and updated stock/mass/packing. English/PT-BR, palettes, touch controls and offline operation are preserved. Manual step07.3 documents installation and service; the historical fixed-function schematic is removed only from CURRENT.',
'',
'## Release holds','',
'- Actual18 mm and12 mm production-lot thickness; mandatory physical coupon and selected clearance.',
'- Purchased arcade buttons: bore, nut, microswitch, terminals and ergonomic verification.',
'- Physical dual USB module: inconsistent cutout, usable thread length through12 mm, cap and first cable bend; optional rear pocket depth.',
'- Purchased module inserts/screws, converted filter-frame mounting stack, landing/WPC/other previously held hardware.',
'- Physical structural, ergonomic, service-loop, vibration and transport qualification.',
'- **FULL-SHEET CNC RELEASE: BLOCKED.** No production cutting files or G-code.','',
'## Sources and review artifacts','',
'- Authority: owner V33.7 instruction and exact V33.6.3 source B-reps; all dimensions above are design/reference unless explicitly measured. No purchased new hardware is claimed measured.',
'- [Joy-IT arcade-button manufacturer reference](https://joy-it.net/files/files/Produkte/Button-XXX/Button-XXX_Datasheet_2024-10-21.pdf): ordinary microswitch example,28 mm hole/M28 and35 × 67 mm overall; not selected hardware or final bore.',
'- USB: owner-supplied AliExpress seller-image description, unverified and internally inconsistent; no licensed seller CAD/image imported.',
'- [24 actual-CAD review views]('+base+'review.html), [native assembly]('+base+'play.FCStd), [offline viewer](../exports/generated/viewer-v32/index.html).',
'- [Material/mass/packing report]('+base+'stock-mass-packing-report.md), [manufacturing register]('+base+'manufacturing-register.json), [one-face audit]('+base+'manufacturing-audit.json).','',
'Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.']
# Keep engineering prose readable without modifying IDs, numbers or file paths.
import re
text='\n'.join(lines)+'\n'
# Space numeric quantities in prose without changing IDs or link targets.
for a,b in {'its220':'its 220','opening132':'opening 132','in18':'in 18','R6.2,2':'R6.2, 2','quantity4':'quantity 4','leave16':'leave 16','mm;2':'mm; 2','lower100':'lower 100','Two4':'Two 4',';250':'; 250',';60':'; 60','gap0.2':'gap 0.2','row6':'row 6',',5 +':', 5 +','and4':'and 4','need276':'need 276','needs234':'needs 234','use160':'use 160','by116':'by 116','is40':'is 40','plus2':'plus 2','selected42':'selected 42','leaves4':'leaves 4','reserve40':'reserve 40','and85':'and 85','gives19':'gives 19','A70':'A 70','with12':'with 12','a70':'a 70','cap0':'cap 0','door0':'door 0','for100':'for 100','leaves44':'leaves 44','Y22.':'Y22.','begins29.8':'begins 29.8','Its16':'Its 16','are10':'are 10','Before:18':'Before: 18','After:18':'After: 18','pieces:0':'pieces: 0','All15':'All 15','nominal12':'nominal 12','four R7 ×4':'four R7 × 4','retain12':'retain 12','to6':'to 6','include one-face3':'include one-face 3','from12':'from 12','no6':'no 6','local9':'local 9','not9':'not 9','remain220':'remain 220','with220':'with 220','is3':'is 3','×32':'× 32','×36':'× 36','leaving9':'leaving 9','and12':'and 12','upper66':'upper 66','is2':'is 2','clearance3.1':'clearance 3.1',';80':'; 80','retained12':'retained 12','is5118':'is 5118','extra6':'extra 6','CNC.2500':'CNC. 2500',',20':', 20','and15':'and 15','Small12':'Small 12','density650':'density 650','Preferred25':'Preferred 25','below25':'below 25','playfield0':'playfield 0','backbox0':'backbox 0','step07.3':'step 07.3','Actual18':'Actual 18','and12':'and 12','through12':'through 12','example,28':'example, 28','and35':'and 35','Owner5':'Owner 5','+ dualUSB':'+ dual USB','stock:12':'stock: 12'}.items():
 text=text.replace(a,b)
segments=re.split(r'(`[^`]*`|\]\([^)]*\))',text)
for i in range(0,len(segments),2):
 segments[i]=re.sub(r'([a-z]{2,})(\d)',r'\1 \2',segments[i])
 segments[i]=re.sub(r'([;:×])(?=\d)',r'\1 ',segments[i])
text=''.join(segments)
(R/'docs/TWO_STOCK_USER_MODULE_V337.md').write_text(text)
(O/'README.md').write_text('# V33.7 — two-stock and user-module review\n\n[Engineering report](../../../docs/TWO_STOCK_USER_MODULE_V337.md) · [Offline viewer](../viewer-v32/index.html) · [Review views](review.html)\n\nDesign architecture passes; manufacturing remains BLOCKED. No full-sheet production files.\n\nCurrent nominal plywood stock:12 /18 mm only. Owner5 buttons + dualUSB,160 ×116 ×12 mm removable plate.\n\nOriginal material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.\n')
print('V337_REPORT_PASS')

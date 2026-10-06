"""Evidence-bound V35 report; incomplete commercial compatibility blocks promotion."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/widebody-v35'
def rd(n):return json.loads((O/(n+'.json')).read_text())
g=rd('geometry');v=rd('validation');m=rd('mass-counts');n=rd('nesting');pk=rd('packaging');motion=rd('continuous-motion');it=rd('interface-screen');browser=rd('browser-validation')
sets={'native construction':g,'differential/reconstruction/motions':v,'continuous PF and sampled matrix':motion,'offline browser':browser}
counts={k:{'pass':sum(x['pass'] for x in d['checks']),'fail':sum(not x['pass'] for x in d['checks'])} for k,d in sets.items()}
blockers=[{'id':'COMMERCIAL_SIDERAIL_TAIL','status':'UNRESOLVED_INTERFACE','evidence':it['uncut_rail_reference_hits'],'reason':'The full1198.5625mm commercial overall length applied to the abstract cross-section intersects the unchanged backbox. Candidate truncates that envelope by82.2375mm. Actual end/flange geometry is not documented, so this is NOT proof that an actual rail must/can be cut by that amount. Need dimensioned commercial section/end evidence to close minimum adaptation.'},{'id':'RECEIVER_INSTALLED_ENVELOPE','status':'UNRESOLVED_INTERFACE','reason':'A-17996/A-16773-1 catalogue family compatibility is verified. The520x42x25mm receiver volume is an original study reserve, not measured supplier geometry; latch/lever travel and installed relation to the high TV have not been established. This is more than an unknown drilling diameter.'},{'id':'REAR_CHANNEL_ATTACHMENT','status':'UNRESOLVED_INTERFACE','reason':'The shortened standard-glass rear stop contacts an angled seat in the existing rear shelf. Reference containment/contact passes, but physical retention of the unmeasured03-8091-2 extrusion to that seat is unresolved. Zero separation alone does not prove attachment.'}]
summary={'version':'V35','source_head':'11822cb2dc9c7c7b511348df860cb76196d641be','head_after':'UNCHANGED_NO_PROMOTION','candidate_geometry_tests':counts,'promotion_pass':False,'commercial_interface_blockers':blockers,'current_geometry_changed':False,'manufacturing_release':False,'review_views':48,'report':'docs/STANDARD_WIDEBODY_V35.md'}
(O/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
stock='\n'.join(f"| {t} mm | {a['pieces']} | {a['outer_contour_area_m2']:.4f} | {len(a['sheets'])} | {a['utilization_outer_percent']:.1f}% |" for t,a in n.items())
bundles='\n'.join(f"| {a['id']} | {' × '.join(f'{x:.1f}' for x in a['external_mm'])} | {a['nominal_wood_kg']:.2f} | {a['high_gross_kg']:.2f} |" for a in pk['bundles'])
tests='\n'.join(f"| {k} | {a['pass']} | {a['fail']} |" for k,a in counts.items())
audit=rd('width-audit');members=['SIDE_L','SIDE_R','FLOOR','FRONT','REAR','BACKBOX_BASE','FLOOR_CLEAT_18','FLOOR_CLEAT_552','CROSS_1','CROSS_2','CROSS_3','SHELF_1','SHELF_2','SHELF_3','PF_BasePlywood','PF_WoodDowel'];wt='\n'.join(f"| {k} | {audit[k]['classification']} | {audit[k]['method']} |" for k in members if k in audit)
text=f'''# V35 standard-widebody migration — engineering study

HEAD BEFORE: `11822cb2dc9c7c7b511348df860cb76196d641be`
HEAD AFTER: **unchanged**. CURRENT remains V34.2. **NOT PROMOTED; no commit/push.**

The native widebody candidate passes the modeled collision and motion screens below. Commercial ecosystem compatibility is not yet sufficiently established for promotion. This is not a hold merely on final hole diameters: the full-length siderail end, receiver operating envelope, and rear extrusion attachment remain unresolved. CNC release remains BLOCKED.

## Evidence and deliverables

- [48 native CAD review views](../exports/generated/widebody-v35/review.html), including before/after, sections, negative controls, motions and preliminary nesting.
- [Offline candidate viewer](../exports/generated/widebody-v35/viewer.html). This is a separate study viewer; CURRENT viewer is preserved.
- [Native candidate](../exports/generated/widebody-v35/candidate.FCStd), [manufacturing register](../exports/generated/widebody-v35/manufacturing-register.json), [CSV](../exports/generated/widebody-v35/manufacturing-bom.csv).
- [Machine-readable result](../exports/generated/widebody-v35/validation-summary.json), [interface measurements](../exports/generated/widebody-v35/interface-screen.json), [width audit](../exports/generated/widebody-v35/width-audit.json).
- [Public standard-parts audit](../library/references/v35-standard-parts.md), [compatibility matrix](../config/standard_parts_v35.json).

STANDARD-PARTS-FIRST is recorded in AGENTS.md, GOVERNANCE.md and the decision log; Tukkari-first remains subordinate to ordinary commercial interfaces. Sources are publicly documented functional references, with independently generated CAD. No vendor CAD or proprietary manufacturing files were imported.

## Dimensions

| Datum | V34.2 | V35 candidate |
|---|---:|---:|
| Main outside width |600|628.65 exact|
| Nominal inside width |564|592.65|
| Length |1308.10|1308.10 KEEP|
| Front/rear height |400.05 /596.90|unchanged|
| Backbox width /height |780 /723.9|unchanged|
| Backbox overhang each side |90|75.675|
| Main centerline X |300|314.325|
| Glass reference |approximately575×1142×5|603.25×1092.20×4.7625|

Backbox components are rigidly translated X+14.325 using one centerline rule. Inverse-placement topology/vertex comparisons preserve local solids, monitor plateY1209, VESA100 ±15mm, acrylic, DMD panel, doors, locks and parking. WPC Y1066.8/Z508 remains unchanged. The old moving playfield rear channel is retired only in this candidate; the fixed shorter-glass rear stop is a main-body interface. The unused old BB_Floor local rebate remains in the protected B-rep; the entire floor is horizontal. No backbox resize.

Tukkari's approximately51.6in description equals1310.64mm, 2.54mm longer. No verified hard datum requires that length change. **KEEP1308.10**; rail end compatibility remains open and cannot be solved by silently lengthening the cabinet. Conservative native bounding boxes used for packing can exceed the exact side length due to OCC spline bounds; they are not revised cabinet-length datums.

## Commercial ecosystem / promotion blockers

1. **Siderails:** A-12359-3/01-8993-2, published47-3/16in =1198.5625mm. Full-length abstract L-profile intersects BB_Floor by about1666.70mm³ per side and DMD panel by0.409mm³ per side. Candidate uses a1116.325mm reference envelope (82.2375mm shorter) to demonstrate a collision-free route. This is a trim hypothesis, **not a proven actual-part trim instruction**. Obtain actual flange/end dimensions before claiming commercial fit. No custom extrusion or mounting holes created.
2. **Lockdown/receiver:** published A-17996 widebody25in-inside family is compatible with A-16773-1.635mm reference bar leaves3.175mm per side over628.65. Reference containment works, but the receiver520×42×25mm reserve is not vendor dimensional evidence. Lever travel, bar latch engagement and TV clearance require an actual installation envelope. No new receiver drilling released; two obsolete outer reference holes are healed in the candidate front panel.
3. **Rear glass stop:**03-8091-2 published22-15/16in =582.6125mm. Reference U contacts the existing rear shelf, using a local angled TOP seat; contact area{it['rear_channel']['contact_area_mm2']:.2f}mm², separation{it['rear_channel']['distance_mm']:.3g}mm. Positive attachment of the actual extrusion is still undefined. A10mm rearward alternative was rejected: BB_Floor intersects the fixed rear channel at1° (102.68mm³),2° and5°. The selected study retains the20mm local front offset. Contact is not fastening proof. No extra wooden rail is added.

Other references:03-7135-1 side channel published42-3/8in =1076.325mm; commercial widebody glass43×23.75×3/16. Side edge engagement is5.30mm beyond each nominal inner face. Reference routing depth7.05mm leaves10.95mm outer wood; **final width/depthNULL**. Inside-face routing is the intended one-face operation; selected-profile/tool-access and coupon remain open. No manufactured extrusion is claimed from the original U-envelope.

The complete metal/polymer/glass stack gives a conventional covered edge in review09, unlike the isolatedV34.2 plastic fin. Reference polymer top6.2625mm normal (~6.36mm vertical at equalY), covered by the siderail envelope; not a purchased lip measurement. Local5mm glass is0.2375mm thicker and is **not automatically compatible** with the commercial channel.

Standard01-11400-1 inner leg bracket remains a procurement comparison; SW01×4 is retained because real bracket bolt/wood bearing cannot be proven from a catalogue family alone. No new custom leg mechanism. Ordinary500-2604-XX shooter /535-5027-00 plate is the commercial reference; exact bore/bracket holes HOLD. Coin-door opening stays centered; purchased door dimensions HOLD. WPC01-9011-L/R,02-4352,4322-01139-12B remain deliberate commercial hardware with physical-measurement hold. Main-side pivot X follows side positions; backbox local floor attachments/arm offset need measured hardware confirmation. None is purchased or released for drilling.

## High parallel playfield

Angle from native glass plane: **{g['angle_deg']:.11f}°**. Display/glass difference0°. Front/center/rear gap **7.5 /7.5 /7.5mm**. Static5/7.5/10mm reference trials clear modeled occupied solids; only7.5 has complete motion validation.7.5 is a planning allowance, not measured glass-flex/TV-tolerance qualification. No deep/sunken solution is promoted. Review12 is explicitly a50mm-lowered negative control.

| Reference, unselected | Portrait width ×length ×depth | GapL/R | Result |
|---|---|---|---|
| LG42C5 |540×932×41.1|26.325 /26.325|native envelope PASS|
| Samsung43QN93D |558.9×960.8×26.9|16.875 /16.875|native envelope PASS|
| TCL40S5K |507×892×77|42.825 /42.825|width PASS; depth FAIL against base/supports|

These are reference whole-body envelopes, not proof of VESA bosses/connector access for a bought TV. Candidate common TV envelope560×961×41.1 replaces the old560×970×55 reference; **thicker ordinary TVs are not universally supported**. Available body depth in this high setup is about45.69mm before the old lower envelope datum. No concealed claim of wider universal compatibility.

Dark side gaps work without extra parts. Optional10mm LED/diffuser envelopes clear the42-inch reference by12.325mm and43-inch by2.875mm. They are optional visual reserves only, absent from mandatory BOM, machining and wiring. The narrow TV has space laterally but still fails depth.

M025 width500 would leave7.675mm from moved landing centers to its edge, less than12mm contact-pad radius.528.65 preserves22mm original edge distance and mounting architecture, so the full28.65mm increase is justified by bearing, not scaling. Horn-free52mm side relief remains; front width becomes424.65. Mechanical support Y/Z and slope stay unchanged. TV reference shifts20mm longitudinally on the existing VESA zone; generic bolt/spacer details remain held.

DowelØ32 length588.65. Cradles follow sides; SW02 centersX72/X556.65,Y245, unchanged68×70×54 blocks. T1/T2/T3 remain structural members, not playfield gravity supports. Side buttonsY89/Y127 at localtop−65 remain; minimum reference channel clearance to modeled button/leaf geometry{it['clearances']['buttons']:.2f}mm, to front-landing hardware{it['clearances']['front_landings']:.2f}mm. Raised-service props are not designed; human raised-playfield service remains HOLD.

## Width audit and structure

| Component | Action | Method |
|---|---|---|
{wt}

PCBase, matrix and underfront module retain physical sizes and recenter; fan/subwoofer/BST equipment retains sizes, positions follow parent/centerline. Side-mounted services and legs follow their side. Shelf lateral spans widen to meet existing side supports; payload equipment is not scaled. Matrix pilot voids in the shelf are relocated with the centered matrix. Full per-object classification is in width-audit.json.

Same-thickness simple-span planning: span ratio1.05080; same total load moment×1.05080/deflection×1.16027; same distributed line load moment×1.10418/deflection×1.21921. This is a relative screen, not proof of stress, glue, plywood grade or allowable deflection. No thickness reduction or loss of floor support paths. Actual structural qualification remains open.

## Manufacturing, mass, logistics

66wood pieces /60CNC plywood /6solid blocks (SW01×4 +SW02×2) /45families. No extra wood family. Exact member reconstruction difference **{m['reconstruction_max_mm3']:.6f}mm³**.12/18mm plywood only. Supplier unchanged:2500×1600 sheet,2460×1560 usable,20border,15spacing,Ø4/R2,one-face only. Modified feature plans are provisional and profile/coupon-dependent; not CNC authorization.

| Stock | Pieces | Outer-contour area m² | Preliminary sheets | Utilization of purchased area |
|---|---:|---:|---:|---:|
{stock}

Conservative bounding-rectangle shelf first-fit with actual contours shown; **not optimized, not production nesting**. Grain rotations require confirmation. No G-code or production full-sheet files.18/12 offcuts remain useful. This projection must not be marketed as minimum purchase count. V34.2 project-metrics records preliminary_sheets as V34 HOLD, so an authoritative before/after purchased-sheet delta cannot be claimed. The V35 area-only lower bound is2 sheets18mm and1 sheet12mm; the conservative layout uses3 +1.

ActualB-rep wood mass: LOW{m['wood_LOW_kg']:.3f}, NOMINAL{m['wood_NOMINAL_kg']:.3f}, HIGH{m['wood_HIGH_kg']:.3f}kg at550/650/750kg/m³. Nominal delta **+{m['delta_nominal_kg']:.3f}kg**. Hardware mass remainsUNKNOWN, not zero. Separate commercial glass planning mass{m['glass_reference_mass_kg']:.3f}kg; not inside wood bundles.

| Bundle | ExternalL×W×H mm | Nominal wood kg | HIGH +1kg packaging kg |
|---|---|---:|---:|
{bundles}

Layered packaging proposal,3mm separators,20mm exterior protection. All modeled bundles≤25kg HIGH including1kg estimated packaging. This very small mass margin in some bundles requires weighing final protection; not a shipping certification. Hardware separate. Contents/layers/approximate center of gravity in packaging.json. No glass/displays/electronics inside wood bundles.

## Validation

| Evidence set | PASS | FAIL |
|---|---:|---:|
{tests}

These counts cover **modeled geometry**, not the three unresolved commercial-interface gates. Native checks include66individual manufacturing solids, inverse backbox placement, widthnegative controls, no new wood intersections, whole forward glass sweep, reference six-direction containment, WPC13requiredangles, continuous backbox/changed-stack bound, playfield angle/lift samples and door/main-body screens. Continuous PF rotation/lift covers base/dowel/VESA/display; dowel seat rotation uses its exact circular invariant. Matrix removal uses191samples over the accepted rocking/forward/lift path. Backbox internal door proof is inherited under rigid recentering; new main-body clearance is sampled. No physical certification.

Glass is removed before playfield service and backbox fold. Backbox locks release/park, rear doors close/latch, matrix is removed, acrylic/DMD/display remain installed. No routine electronics disconnect. WPC installation maintenance remains separate.

Offline desktop/tablet Chrome QA uses native states and66real manufacturing meshes, EN/PT-BR existing UI, Accessible palette, LED reserve toggle and touch controls; no network or JavaScript errors. Manual/CURRENT authority are **not switched to this unpromoted study**. Candidate viewer's inherited manual has aV35dimension overlay and is not a completedV35assembly manual.

## Decision / remaining blockers

**Do not promote this candidate yet.** Resolve the three commercial interface issues above with documented profiles/installation geometry, then rerun the supplied native and browser checks. The82.2375mm tail trim and520mm receiver box must not turn into manufacturing truth by repetition. This differs from leaving final holesNULL: the actual functional shape/installation remains unverified.

Other manufacturing holds: actual plywood lot; coupon and selected clearance; lockdown/receiver/siderails/channel/glass; leg/bracket/shooter/button hardware; monitor/VESA/DMD/speakers; structural/ergonomic/glass-edge qualification; raised-playfield positive support. Full-sheet CNC remainsBLOCKED.

No changes to CURRENT native/viewer/manual or any other checkout. UnpromotedV34.3files are retained separately and are not authority.
'''
(R/'docs/STANDARD_WIDEBODY_V35.md').write_text(text)
(O/'README.md').write_text(text.replace('../exports/generated/widebody-v35/','').replace('../library/','../../../library/').replace('../config/','../../../config/'))
manifest={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in O.iterdir() if x.suffix in ['.json','.FCStd','.gz'] and '.2026' not in x.name}
(O/'evidence-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('V35_REPORT',counts,'PROMOTION_BLOCKED',len(blockers))

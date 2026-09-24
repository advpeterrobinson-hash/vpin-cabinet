# Hardware arrival inspection — v27

Derived owner convenience copy. Authoritative values remain in [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). No measurements are filled; manufacturing stays **BLOCKED**. Regenerate with `python3 tools/generate_owner_execution_v27.py`; do not write bench results into generated files.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

**BUY NOW** below repeats existing authorization; no new purchasing category is introduced. **HF-030 remains the only previously new BUY NOW item.** Only HF-014 is confirmed owned. **HAVE / OWNER-SUPPLIED** can mean a required shop/prototype/assembled sample whose arrival is unknown; it never asserts ownership without evidence. **WAIT** means no current purchase instruction. **REFERENCE ONLY** means maker/drawing data, not a physical substitute.

On delivery: identify item, variant, batch and handed side; check completeness and obvious damage, retain labels, and put mating bolts/nuts/backing together. These are arrival observations, not dimensional acceptance. Record arrival on this printed copy; do not populate physical measured values from invoices/catalogues.

Shared acquisitions: legs/brackets HF-003/004; slides/clamps HF-013/026; door hardware HF-015/016/029 (separate installations); backbox hinges/locks HF-006/007; props/latches HF-010/012; mains module/enclosure HF-017/027. HF-028 reuses the corner stack; HF-002 is shop consultation. No electronics purchase is needed to start Session 0.

## Arrival summary

| ID | Item | Category | Arrival today |
|---|---|---|---|
| HF-001 | Production 18 mm plywood sheets | BUY NOW | ______ |
| HF-002 | CNC cutter/tooling and tolerance coupon | HAVE / OWNER-SUPPLIED | ______ |
| HF-003 | Classic pinball leg set | BUY NOW | ______ |
| HF-004 | Compact internal leg brackets/backing | BUY NOW | ______ |
| HF-005 | External removable PinSkates-style pair | WAIT | ______ |
| HF-006 | WPC 01-9011-L/R hinge pair + 02-4352 + pivot bolts | BUY NOW | ______ |
| HF-007 | Upright backbox lock bolts/captive threads | BUY NOW | ______ |
| HF-008 | UCFL202 15 mm flange bearing pair | BUY NOW | ______ |
| HF-009 | 15 mm pivot journals / cheek plates | HAVE / OWNER-SUPPLIED | ______ |
| HF-010 | Two captive steel prop rods with clevises/pins/keepers/stow clips | BUY NOW | ______ |
| HF-012 | Closed-position pads/latches | BUY NOW | ______ |
| HF-013 | Rear CPU full-extension slide pair | BUY NOW | ______ |
| HF-014 | Open PC case | HAVE / OWNER-SUPPLIED | ______ |
| HF-015 | Rear CPU hatch hinge | BUY NOW | ______ |
| HF-016 | Rear CPU hatch latch | BUY NOW | ______ |
| HF-017 | Rear mains inlet/disconnect module | BUY NOW | ______ |
| HF-018 | Optional Ethernet RJ45 carrier or blank | WAIT | ______ |
| HF-019 | Coin door | BUY NOW | ______ |
| HF-020 | Flipper/start/launch buttons | BUY NOW | ______ |
| HF-021 | Playfield siderail profile | HAVE / OWNER-SUPPLIED | ______ |
| HF-022 | 600 mm lockdown bar + receiver | HAVE / OWNER-SUPPLIED | ______ |
| HF-023 | Playfield tempered glass | WAIT | ______ |
| HF-024 | Playfield 42/43 inch display | WAIT | ______ |
| HF-025 | Backglass monitor | WAIT | ______ |
| HF-026 | Four identical CPU rail angle clamps + backing + retainer | BUY NOW | ______ |
| HF-027 | Touch-safe mains enclosure | BUY NOW | ______ |
| HF-028 | Rear bracket to CPU rail planning reserve | HAVE / OWNER-SUPPLIED | ______ |
| HF-029 | Backbox service door hinge/lock/gasket | BUY NOW | ______ |
| HF-030 | Mechanical/electronic plunger assembly | BUY NOW | ______ |
| HF-031 | Four exciters and local attachment adapters | WAIT | ______ |
| HF-032 | Dust-filter media and optional intake/exhaust fans | WAIT | ______ |
| HF-033 | Backbox conventional speaker modules | WAIT | ______ |

## HF-001 — Production 18 mm plywood sheets

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** all active stock fields; config/cnc_detail_v25.json:stock. Physical tasks: STOCK-THICK, STOCK-SURVEY, SHOP-COUPON.

**Measurements required:** HF-001-M01 Thickness at 9 distributed points per sheet; HF-001-M02 min/max; HF-001-M03 sheet dimensions; HF-001-M04 bow; HF-001-M05 face/core defects; HF-001-M06 grain direction; HF-001-M07 batch ID.

**Tests required:** PV-STOCK-TOOL

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Mark face A and front-left corner; thickness normal to face without crushing veneers

## HF-002 — CNC cutter/tooling and tolerance coupon

**HAVE / OWNER-SUPPLIED.** Immediate shop consultation/coupon task, not a hardware purchase. Shop tooling/evidence not confirmed.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cnc_detail_v25.json:fit; tools/generate_cnc_coupon_v20.py. Physical tasks: SHOP-COUPON.

**Measurements required:** HF-002-M01 Actual cutter diameter; HF-002-M02 runout; HF-002-M03 pocket depth accuracy; HF-002-M04 accepted groove clearance; HF-002-M05 relief radius; HF-002-M06 two-face registration accuracy.

**Tests required:** PV-STOCK-TOOL

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Coupon face A and engraved zero corner

## HF-003 — Classic pinball leg set

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_service_v21.json:leg_corners; pending measured_patterns.HF-003. Physical tasks: LEGS-BARE, LOADS.

**Measurements required:** HF-003-M01 Both bolt center coordinates; HF-003-M02 hole/slot widths; HF-003-M03 corner included angle; HF-003-M04 flange width; HF-003-M05 leg mounting face flatness; HF-003-M06 bolt head seat; HF-003-M07 leveler travel; HF-003-M08 record all four legs.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0003, CF-0012, CF-0021, CF-0029

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=inside leg mounting faces seated on 90-degree test corner; B=leg upper edge; C=corner bisector

## HF-004 — Compact internal leg brackets/backing

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_service_v21.json:leg_corners; config/cnc_detail_v25.json:leg_envelope. Physical tasks: BRACKET-BARE, REAR-STACK, LOADS.

**Measurements required:** HF-004-M01 Flange thickness; HF-004-M02 inner X at rear left/right when seated; HF-004-M03 full Y/Z extent; HF-004-M04 all hole centers/diameters; HF-004-M05 bolt/nut/washer stack; HF-004-M06 wrench access; HF-004-M07 backing contact area.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0004, CF-0013, CF-0022, CF-0030

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=inside cabinet wall plane; B=inside rear/front plane; C=bottom panel top; use measured-thickness corner fixture

## HF-005 — External removable PinSkates-style pair

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** No wood holes. Physical tasks: SKATES.

**Measurements required:** HF-005-M01 Leg engagement and stability before mobility use.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Actual installed legs

## HF-006 — WPC 01-9011-L/R hinge pair + 02-4352 + pivot bolts

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/structure_geometry_v14.json:wpc_hinges; measured_patterns.HF-006. Physical tasks: BB-HINGES, BB-LOCKS, LOADS.

**Measurements required:** HF-006-M01 Hole and slot centers; HF-006-M02 hole diameters; HF-006-M03 leaf outline/thickness; HF-006-M04 bend offsets; HF-006-M05 pivot center to both mounting faces; HF-006-M06 bushing OD/ID/flange/length; HF-006-M07 bolt shoulder and thread; HF-006-M08 full folded/upright sweep; HF-006-M09 left/right differences.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0005, CF-0014, CF-0049, CF-0055, CF-0058

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=each hinge mounting face; B=rear edge; C=bottom edge; pivot center separately recorded

## HF-007 — Upright backbox lock bolts/captive threads

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/structure_geometry_v14.json:upright_locking; measured_patterns.HF-007. Physical tasks: BB-LOCKS, LOADS.

**Measurements required:** HF-007-M01 Thread; HF-007-M02 grip length; HF-007-M03 head/tool envelope; HF-007-M04 captive plate hole pattern; HF-007-M05 engagement; HF-007-M06 shelf/floor/gasket stack; HF-007-M07 X and Y after hinge fixture.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0046, CF-0050

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=rear shelf top; B=cabinet centerline; C=rear exterior plane; upright on fixture

## HF-008 — UCFL202 15 mm flange bearing pair

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/playfield_mechanics_v18.json:pivot_interface; measured_patterns.HF-008. Physical tasks: BEARINGS, BEARING-REF, LOADS.

**Measurements required:** HF-008-M01 Bore at each bearing; HF-008-M02 flange hole/slot centers and widths; HF-008-M03 casting outline; HF-008-M04 mounting-face to bore axis; HF-008-M05 housing thickness; HF-008-M06 axial protrusions; HF-008-M07 set-screw access; HF-008-M08 misalignment range documented by maker.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0006, CF-0015

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=flat mounting face; B=bore axis; C=line joining flange bolts; record both housings

## HF-009 — 15 mm pivot journals / cheek plates

**HAVE / OWNER-SUPPLIED.** Required local prototype/drawing; not confirmed present. HF-009 follows bearing measurements; HF-021/022 prototype now per existing pack.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/playfield_mechanics_v18.json:pivot_interface; separate metal DXF/PDF after HF-008. Physical tasks: JOURNALS, LOADS.

**Measurements required:** HF-009-M01 Journal fit/finish; HF-009-M02 engagement; HF-009-M03 shoulder; HF-009-M04 axial retention; HF-009-M05 plate-to-rail stack; HF-009-M06 bolt edge distances; HF-009-M07 shop drawing revision.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0090, CF-0093, CF-0096

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Bearing axis and plate seating face; journal shoulder zero

## HF-010 — Two captive steel prop rods with clevises/pins/keepers/stow clips

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/playfield_mechanics_v18.json:safety_stays; config/playfield_fixed_anchors_v19.json:safety_stay_fixed_anchor. Physical tasks: PROPS-BARE, PROP-MOTION, PROP-LEFT, PROP-RIGHT.

**Measurements required:** HF-010-M01 Rod pin-to-pin length; HF-010-M02 section and end-eye geometry; HF-010-M03 lower clevis and upper receiver outlines/offsets/patterns; HF-010-M04 pin diameter and positive keeper engagement; HF-010-M05 stow-clip retention/pattern; HF-010-M06 complete swing; HF-010-M07 one-prop load capacity.

**Tests required:** PV-PROP-L, PV-PROP-MOTION, PV-PROP-R

**Related CF blockers:** CF-0007, CF-0016, CF-0076, CF-0080, CF-0099, CF-0103

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=each anchor mounting face; B=pivot pin center; C=stay center plane; both handed units

## HF-012 — Closed-position pads/latches

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/playfield_mechanics_v18.json:closed_support; measured_patterns.HF-012. Physical tasks: LATCH-PADS.

**Measurements required:** HF-012-M01 Latch and catch holes; HF-012-M02 closed grip range; HF-012-M03 travel/release envelope; HF-012-M04 pad footprint and loaded thickness; HF-012-M05 attachment geometry.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** CF-0077, CF-0081, CF-0100, CF-0104

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=seat/strike mounting surface; B=closed cradle rail underside; C=front end

## HF-013 — Rear CPU full-extension slide pair

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_rear_cpu_shelf_v24.json:pc_shelf; measured_patterns.HF-013. Physical tasks: SLIDES-BARE, SLIDE-REF, CPU-QUALIFY.

**Measurements required:** HF-013-M01 Body thickness each side; HF-013-M02 maker minimum/maximum side clearance; HF-013-M03 fixed/moving member outlines; HF-013-M04 hole and slot centers separately; HF-013-M05 travel; HF-013-M06 disconnect access; HF-013-M07 closed stop position; HF-013-M08 screw-head limits; HF-013-M09 rating conditions.

**Tests required:** SV-03

**Related CF blockers:** CF-0111, CF-0116, CF-0121

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=fixed-member mounting face; B=closed rear end; C=lower edge; second sheet for moving member

## HF-014 — Open PC case

**HAVE / OWNER-SUPPLIED.** Already-owned open case explicitly documented; confirm identity at bench.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_rear_cpu_shelf_v24.json:pc_shelf.case_mounting; replaceable shelf only. Physical tasks: CPU-CASE, CPU-QUALIFY.

**Measurements required:** HF-014-M01 Mounting hole centers/diameters; HF-014-M02 foot heights; HF-014-M03 standoff stack; HF-014-M04 connector and GPU restraint access.

**Tests required:** SV-03

**Related CF blockers:** CF-0112

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=case feet plane; B=installed front-left corner; X=265 direction; Y=440 direction

## HF-015 — Rear CPU hatch hinge

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_rear_cpu_shelf_v24.json:rear_service_door; measured_patterns.HF-015. Physical tasks: CPU-HINGE, CPU-QUALIFY.

**Measurements required:** HF-015-M01 Leaf widths/thickness; HF-015-M02 knuckle diameter; HF-015-M03 axis-to-leaf offsets; HF-015-M04 hole centers/diameters; HF-015-M05 screw heads; HF-015-M06 folded stack; HF-015-M07 available opening angle.

**Tests required:** SV-03

**Related CF blockers:** CF-0031, CF-0107

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=leaf seating face; B=hinge end; C=knuckle axis; measure both leaves separately

## HF-016 — Rear CPU hatch latch

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_rear_cpu_shelf_v24.json:rear_service_door; measured_patterns.HF-016. Physical tasks: CPU-LATCH, CPU-QUALIFY.

**Measurements required:** HF-016-M01 Body cutout; HF-016-M02 antirotation flat; HF-016-M03 fixing holes; HF-016-M04 cam reach; HF-016-M05 grip range; HF-016-M06 catch geometry; HF-016-M07 key/tool clearance; HF-016-M08 compressed gasket thickness.

**Tests required:** SV-03

**Related CF blockers:** CF-0032, CF-0108

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=door outside face; B=latch body center; C=cam closed axis

## HF-017 — Rear mains inlet/disconnect module

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/rear_utility_v26.json:A; measured_patterns.HF-017. Physical tasks: MAINS-FIT, ELECTRICAL.

**Measurements required:** HF-017-M01 Panel cutout; HF-017-M02 fixing holes; HF-017-M03 total depth; HF-017-M04 plug/cord bend space; HF-017-M05 disconnect travel; HF-017-M06 strain-relief footprint; HF-017-M07 mounting stack.

**Tests required:** PV-ELECTRICAL

**Related CF blockers:** CF-0033

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=carrier rear face; B=carrier lower-left; C=entry axis; no exposed terminals in service space

## HF-018 — Optional Ethernet RJ45 carrier or blank

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/rear_utility_v26.json:A; carrier drawing only. Physical tasks: ETHERNET.

**Measurements required:** HF-018-M01 Coupler/keystone aperture; HF-018-M02 clip retention; HF-018-M03 bend radius.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Carrier outside lower-left corner

## HF-019 — Coin door

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_structure_v20.json front interface; measured_patterns.HF-019. Physical tasks: COIN-FACE, COIN-OPEN.

**Measurements required:** HF-019-M01 Required cutout contour/radii; HF-019-M02 flange coverage; HF-019-M03 all mounting holes; HF-019-M04 body/depth; HF-019-M05 hinge swing; HF-019-M06 lock/key access; HF-019-M07 coin mechanism protrusion.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** CF-0023

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=front mounting face; B=cutout lower-left; C=vertical centerline

## HF-020 — Flipper/start/launch buttons

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** measured_patterns.HF-020; main-side/front CNC features. Physical tasks: BUTTON-FAMILY, CONTROLS-HANDS.

**Measurements required:** HF-020-M01 Bore and flats; HF-020-M02 bezel OD; HF-020-M03 threaded length; HF-020-M04 nut/washer OD; HF-020-M05 switch depth; HF-020-M06 connector clearance; HF-020-M07 antirotation/pilot holes.

**Tests required:** PV-CONTROLS-SSF

**Related CF blockers:** CF-0008, CF-0017, CF-0024

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=panel outside face; B=button axis; C=key orientation

## HF-021 — Playfield siderail profile

**HAVE / OWNER-SUPPLIED.** Required local prototype/drawing; not confirmed present. HF-009 follows bearing measurements; HF-021/022 prototype now per existing pack.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_structure_v20.json:siderails; metal drawing. Physical tasks: RAIL-PROFILE.

**Measurements required:** HF-021-M01 Bend radii; HF-021-M02 sheet thickness; HF-021-M03 glass capture; HF-021-M04 fastener flange; HF-021-M05 screw/head envelope; HF-021-M06 rail end relation to lockdown.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** CF-0009, CF-0018

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Cabinet side top plane and glass edge

## HF-022 — 600 mm lockdown bar + receiver

**HAVE / OWNER-SUPPLIED.** Required local prototype/drawing; not confirmed present. HF-009 follows bearing measurements; HF-021/022 prototype now per existing pack.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_structure_v20.json:lockdown; metal drawing. Physical tasks: LOCKDOWN-FIT, LOADS.

**Measurements required:** HF-022-M01 Receiver/catch pattern; HF-022-M02 latch travel; HF-022-M03 glass engagement; HF-022-M04 front overlap; HF-022-M05 fastener access; HF-022-M06 loaded deflection.

**Tests required:** PV-LOADS

**Related CF blockers:** CF-0025

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Cabinet front top and centerline; actual side/rail/glass mockup

## HF-023 — Playfield tempered glass

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_structure_v20.json:playfield_glass. Physical tasks: GLASS.

**Measurements required:** HF-023-M01 Finished supported opening; HF-023-M02 engagement and expansion clearances; HF-023-M03 thickness sample.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Assembled supported glass plane

## HF-024 — Playfield 42/43 inch display

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** display adapter; final manual lift check; no model-specific shell holes. Physical tasks: PF-DISPLAY, MOVING-MASS, LIFT.

**Measurements required:** HF-024-M01 VESA; HF-024-M02 connector access; HF-024-M03 completed moving mass and manual lifting force at the front grip.

**Tests required:** PV-ERGONOMICS, PV-MASS

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Cradle local axes and display mounting plane

## HF-025 — Backglass monitor

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** Backglass carrier only. Physical tasks: BB-MONITOR, BB-REMOVE.

**Measurements required:** HF-025-M01 VESA; HF-025-M02 bezel; HF-025-M03 connector space; HF-025-M04 mass.

**Tests required:** SV-05

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Rail cage mounting plane

## HF-026 — Four identical CPU rail angle clamps + backing + retainer

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cabinet_rear_cpu_shelf_v24.json:pc_shelf.support_detail; measured_patterns.HF-026. Physical tasks: CLAMPS, CPU-QUALIFY.

**Measurements required:** HF-026-M01 Both angle legs/length/thickness; HF-026-M02 bend radius; HF-026-M03 all holes; HF-026-M04 backing thickness/area/pattern; HF-026-M05 bolt grade/diameter/stack; HF-026-M06 retainer stroke/holes/access.

**Tests required:** SV-03

**Related CF blockers:** CF-0037, CF-0113, CF-0117, CF-0122

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=bottom top face; B=rail face; C=clamp front edge; backing measured separately

## HF-027 — Touch-safe mains enclosure

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/rear_utility_v26.json:A; measured_patterns.HF-027. Physical tasks: MAINS-FIT, ELECTRICAL.

**Measurements required:** HF-027-M01 External bounds including mounts; HF-027-M02 lid screw/service clearance; HF-027-M03 cable gland projection; HF-027-M04 mounting hole pattern; HF-027-M05 protected entry.

**Tests required:** PV-ELECTRICAL

**Related CF blockers:** CF-0034

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=rear panel inside face; B=assembly lower-left; C=lid removal direction

## HF-028 — Rear bracket to CPU rail planning reserve

**HAVE / OWNER-SUPPLIED.** Bundled measurement task using legs/brackets/slides/clamps; not another purchase. Arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/cnc_detail_v25.json:leg_envelope; pc_shelf support X coordinates. Physical tasks: REAR-STACK, CPU-QUALIFY.

**Measurements required:** HF-028-M01 Minimum actual rail-to-bracket gap including flange/bolt/nut/washer; HF-028-M02 bracket Y/Z extent; HF-028-M03 slide side clearance; HF-028-M04 clamp/backing bounds at both rear corners.

**Tests required:** SV-03

**Related CF blockers:** CF-0118, CF-0123

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Cabinet global X/Y/Z from measured-stock corner fixture; retain signed left/right coordinates

## HF-029 — Backbox service door hinge/lock/gasket

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/structure_geometry_v14.json:backbox.service_door; measured_patterns.HF-029. Physical tasks: BB-DOOR.

**Measurements required:** HF-029-M01 Hinge leaves/axis/holes; HF-029-M02 lock body/catch/cutout; HF-029-M03 gasket compressed thickness; HF-029-M04 door clearance and opening sweep.

**Tests required:** SV-04

**Related CF blockers:** CF-0061, CF-0064, CF-0067, CF-0070, CF-0073

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=backbox rear frame outer face; B=opening lower-left; C=door hinge edge

## HF-030 — Mechanical/electronic plunger assembly

**BUY NOW.** Existing authorization only; arrival/ownership unknown. HF-030 is the sole previously new addition.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/owner_services_v27.json:controls; measured_patterns.HF-030. Physical tasks: PLUNGER-FACE, PLUNGER-STROKE, CONTROLS-HANDS.

**Measurements required:** HF-030-M01 Front cutout contour; HF-030-M02 hole centers; HF-030-M03 sleeve/shaft diameter; HF-030-M04 flange and nut stack; HF-030-M05 stroke; HF-030-M06 handle projection; HF-030-M07 internal body/sensor depth; HF-030-M08 cable/connector sweep.

**Tests required:** PV-CONTROLS-SSF, PV-PLUNGER

**Related CF blockers:** CF-0026

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: A=front panel outside plane; B=plunger shaft axis; C=anti-rotation orientation; installed +Y inward

## HF-031 — Four exciters and local attachment adapters

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/owner_services_v27.json:ssf; local replaceable exciter adapters. Physical tasks: CONTROLS-HANDS, SSF-ADAPTER, SSF-REF.

**Measurements required:** HF-031-M01 Attachment footprint; HF-031-M02 adapter screw or adhesive specification; HF-031-M03 projection; HF-031-M04 cable bend and service clearance.

**Tests required:** PV-CONTROLS-SSF

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Solid sidewall inside face; local adapter zero

## HF-032 — Dust-filter media and optional intake/exhaust fans

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/owner_services_v27.json:bottom_intake/exhaust; replaceable adapter drawings. Physical tasks: FILTER, FANS, THERMAL.

**Measurements required:** HF-032-M01 Filter compression and service clearance; HF-032-M02 fan thickness; HF-032-M03 grille/finger guard; HF-032-M04 fan pattern on adapter only.

**Tests required:** PV-AIRFLOW, PV-THERMAL

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Generic cassette/adapter mounting face and project-designed mounting grid

## HF-033 — Backbox conventional speaker modules

**WAIT.** BUY LATER / optional adapter: no new purchase authorization. Actual arrival unknown.

Sample/batch/side: __________  Received date: __________  Missing/damaged: __________

**Needed for:** config/owner_services_v27.json:backbox.speaker_boxes_mm; replaceable baffle only. Physical tasks: BB-SPEAKERS.

**Measurements required:** HF-033-M01 Driver cutout; HF-033-M02 screw pattern; HF-033-M03 rear magnet/connector depth; HF-033-M04 baffle thickness; HF-033-M05 rail-cage adapter attachment.

**Tests required:** Component fit/access checks in its operations; no separately named ledger trial.

**Related CF blockers:** No current hardware-blocked wood group; adapter/global gate only.

**Physical sample:** Yes before the corresponding physical fit/test can be accepted; WAIT items do not become BUY NOW. Maker-spec-only entries remain supplemental references.

**Catalogue/drawing data:** REFERENCE ONLY; never substitute for physical measurements. Existing datum: Removable speaker module front face; centerline

## REFERENCE ONLY — document envelope

File maker identity, revision, rating conditions, clearance limits and attachment specifications alongside the physical sample. Specifically HF-008-M08, HF-013-M02/M09 and HF-031-M02 are reference-specification tasks. Do not change their measured_value from null in this cycle. Return references for engineering review. Do not infer geometry from a render, catalogue picture or CAD envelope.

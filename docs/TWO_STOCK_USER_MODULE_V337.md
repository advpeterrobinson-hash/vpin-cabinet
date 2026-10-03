# V33.7 — two plywood families and removable user module

HEAD BEFORE: `c02f9b878f370441b2bc3e637a3030f681fe140a`.
HEAD AFTER: the commit containing this report; read `git log -1 --format=%H -- docs/TWO_STOCK_USER_MODULE_V337.md`. A commit cannot embed its own final hash.

**Design architecture passes. Manufacturing release remains BLOCKED.** Only the authorized thin-stock conversions, FLOOR module bay and new removable plate change geometry. Unrelated installed parts, accepted holes, side buttons, playfield support positions/slope, SW01, M006, M067, WPC axis and all accepted mechanisms are preserved.

## Selected module

One **160 × 116 × 12 mm** rounded plate (R6), centered at X300 / Y110 on the underside of FLOOR. The owner variant has **five programmable arcade buttons plus one dual USB 3.0 module**. The button-only variant fits **six buttons** comfortably in the same external plate/bay. A blank plate keeps electronics optional. Four buttons plus USB also passed, but offers no footprint reduction with the conservative service envelopes, so the fifth button is retained.

No permanent START/VOLUME/MODE/Bluetooth or other software function labels. Historical SERVICE_IO_V08 / DEC-016 and its 220 × 55 fixed-function concept are preserved as historical evidence and superseded for CURRENT. Optional removable identification overlay may use numbers; no engraving is required.

| Interface | Selected design reference |
|---|---|
| Plate | 160 × 116 × 12 mm, R6; M074 / P097-Main |
| Permanent bay | One opening 132 × 88 mm, R8, in 18 mm FLOOR / M005 |
| Locating recess | 160.4 × 116.4 mm reference, R6.2, 2 mm deep from underside FACE_A |
| Recess study | 2 /3 /4 mm leave 16 /15 /14 mm skin; 2 mm chosen as shallowest positive locator |
| Plate installed bounds | X220–380 / Y52–168 / Z8–20 mm |
| Attachment | Four captive metal-thread receivers + M4 × 20 button-head reference screws; F62 × 4 / I19 × 4 |
| Reference attachment centers | X230 /370 paired with Y62 /158; final bores HOLD |
| Insert envelope | Ø8 × 10 mm blind reference; 6 mm outer FLOOR skin remains |
| Button layout | Two rows, three cells per row; 42 mm pitch; USB replaces rear-right button |
| Device positions | Reference cells X258 /300 /342 and Y89 /131; not final drilling authority |
| Service | Remove four underside screws, lower 100 mm, unplug builder-selected harness and bench-service |
| Cable management | Two 4 × 12 mm R2 slots in removable plate; 250 mm planning service slack; 60 × 44 × 60 mm fixed loop reserve |

The reference locating gap 0.2 mm each side is not final fit clearance. Regenerate from measured production-lot stock and coupon result. The permanent FLOOR receives no individual button or USB hole. Attachment holes are not silently cut: their reference envelopes are shown, but actual selected insert pilot and screw clearance remain PURCHASE_BEFORE_CNC. The plate is not counted as replacing structural FLOOR wood.

## Layout and location search

Compared single-row 6 buttons, 5 + USB and 4 + USB against compact two-row arrangements. The single-row six-cell layouts need 276 × 76 mm; the five-cell single row needs 234 × 76 mm. All two-row candidates use 160 × 116 mm. The selected two-row module reduces width by 116 mm against six cells in one row without sacrificing the owner USB or fifth button.

Physical reference pitch is 40 mm (Ø38 nut plus 2 mm clearance); selected 42 mm leaves 4 mm between nut envelopes. Button flanges areØ35; rear body/microswitch/wire envelopes reserve 40 × 40 mm and 85 mm depth behind the exterior face. These are conservative reference assumptions, not a selected hardware SKU.

The search screens actual CURRENT B-reps at candidate positions. The selected center X300 is symmetric, and Y110 keeps the recess ahead of the tray while preserving the front captured joint. The tray support bounding box overlaps part of the search region, but the actual support is open there; exact geometry, not a bounding rectangle, gives 19 mm minimum tray/support clearance.

## USB reference and physical access

Owner-supplied seller values are inconsistent: approximatelyØ26.0 orØ28 ±0.3 cutout,Ø26.5 body,Ø33 flange,46.8 mm rear body,33 mm nut width and 8.2 mm nut thickness. Status: SELLER_REFERENCE_NOT_VERIFIED / PHYSICAL_MEASUREMENT_REQUIRED / PURCHASE_BEFORE_CNC. **USB_CUTOUT_DIAMETER_MM = null; BUTTON_BORE_MM = null.** No final hole diameter has been inferred from the envelope.

USB points downward, with a rear-opening cap. A 70 mm rear-depth reserve permits the body, nut, cable emergence and first bend. Compatibility with 12 mm panel thickness is UNKNOWN until measured. The removable plate supports a one-face rear pocket if required; pocket depth remains null. This pocket must never migrate into the permanent FLOOR.

Five finger approaches with a 70 mm palm envelope, USB plug/hand approach, four underside screwdriver corridors, cap 0–120° and coin door 0–110° were screened. The actual rigid module withdrawal is bounded continuously for 100 mm downward travel. The flexible loop is separately bounded behind the complete coin-door sweep; no invented flexible-wire trajectory is claimed.

The conservative vertical bound between all moving coin-door solids (Z≥94) and button/wire envelopes (Z≤93) is 1 mm over the complete sweep. The actual tray/support separation is 19 mm; the fixed flexible-loop reserve is 7 mm behind the analytically bounded coin-door sweep. These envelope checks must be repeated with purchased hardware and the real harness; 1 mm is not a certified installation tolerance.

Controls are hidden at three representative standing-front sightlines with the coin door closed, and do not extend below the cabinet lower edge Z0. This is geometric screening, not ergonomic certification. Purchased leg height, actual knees/feet, cap hinge form, harness bend radii, button force and physical reach remain prototype checks.

## Structural and service clearances

The through-opening leaves 44 mm of full-thickness FLOOR in front of the aperture measured from the captured-front-joint rear boundary Y22. The shallow recess begins 29.8 mm behind that boundary. Its 16 mm shoulder skin remains continuous. Plate screws are 10 mm from the external plate edges, with the final bore/insert dimensions still held. The module does not cut the front panel or captured joints.

| Actual modeled region | Nearest module/device clearance mm |
|---|---:|
| front | 34.000 |
| SW01 | 156.840 |
| leg_hardware | 158.586 |
| M006 | 172.000 |
| coin_tray | 19.000 |
| landings | 256.908 |
| plunger | 216.640 |
| side_buttons | 295.680 |
| S1 | 67.000 |
| SSF | 16.125 |

Front landings remain X72 / X528,Y245; their hand/tool corridors stay clear. Side buttons remain separate leaf-button architecture at Y89/Y127 and local side top−65. Plunger, SW01 front blocks, leg backing, M006, S1 and its payload reserve remain unchanged. Locks, WPC motion, display/glass and rear-door architecture are unchanged.

## Mandatory plywood conversion

**Before: 18 /12 /8 /6 mm. After: 18 /12 mm ONLY. Forbidden CURRENT plywood stock pieces: 0.** All 15 thin-stock members are retained with their manufacturing IDs and converted to nominal 12 mm stock. Four SW01 solid-wood blocks are excluded from the plywood-family rule. Commodity filters, rubber and hardware do not introduce a plywood family.

| Family | Count | Conversion and preserved interface |
|---|---:|---|
| M028 floor filters | 2 | 8→12 stock; underside one-face R86 × 4 pocket and four R7 × 4 head recesses preserve media, guard and fastener mating planes; outer corners retain 12 mm stock |
| M045 display bezel | 1 | 6→12 stock, faced from rear FACE_A to 6 mm finished; visible plane and entire accepted B-rep unchanged |
| M058 intake filter frames | 2 | 6→12; grows outward, preserved door/airway surfaces; selected mounting fastener length requires +6 mm stack review |
| M059/M060/M061 baffle members | 8 | 6→12 stock, exterior growth, exact internal airflow surfaces retained; four identical M061 include one-face 3 mm lower-edge rebate |
| M066 optional fan blanks | 2 | 6→12, exterior growth; same station; alternate to fans, never displayed simultaneously as installed fan covers |

The M045 bezel is constrained between glass Y1114–1118 and monitor beginning Y1128. Its accepted Y1120–1126 envelope is preserved by explicit one-face facing from 12 mm purchased stock. This is manufacturing removal, accounted as waste; no 6 mm sheet is purchased. Similarly the M061 local 9 mm web comes from 12 mm stock, not 9 mm sheet.

Baffle chambers remain 220 × 36 mm in section: **7920 mm² throat each**, with 220 × 80 =17,600 mm² door inlet each. A naive exterior thickening initially conflicts with the passive-door-bolt reserve. The final broad lower-edge rebate is 3 mm deep × 32 mm high × 36 mm long, leaving 9 mm web there and 12 mm in the upper 66 mm. Passive-bolt clearance is 2 mm; speaker clearance 3.1 mm. This correction preserves a single repeated M061 family and all internal airflow geometry.

M028 underside remains Z6, above the cabinet datum Z0; 80 mm downward filter service passes. The retained 12 mm corner land area is 5118.85 mm² per holder. Ground service still depends on purchased legs, as before. Current fan/media/head stack planes are retained. F21/F22 intake frame screw lengths must be reselected for the extra 6 mm stack; that uncertainty is visible in the hardware supplement.

One-face status: 43 ONE_SIDE_CNC_READY plywood pieces and 61 ONE_SIDE_CNC_PLUS_MANUAL_FINISH; 4 separately classified shop-made SW01 blocks.17 revised manufacturing members and 11 installed aggregate reconstructions compare at 0 mm³ difference.

All new pockets and reductions originate from FACE_A only; FACE_B receives no CNC. No flip instructions, custom metal, production nest or G-code were added.

## Material, mass and preliminary sheet study

Wood pieces: **108**; CNC plywood: **104**; SW01 solid blocks: **4**; canonical families: **66**.

| Nominal stock | Pieces | Outer contour area m² | Net projected material m² | Preliminary full sheets | Net utilization | Gross waste incl. offcuts |
|---|---:|---:|---:|---:|---:|---:|
| 18 mm | 65 | 5.26231 | 4.40125 | 2 | 55.02% | 44.98% |
| 12 mm | 39 | 1.80767 | 1.35730 | 1 | 33.93% | 66.07% |

The converted 12 mm set still fits one preliminary 12 mm sheet; no additional 12 mm full sheet is required.18 mm remains two sheets. Retiring 6/8 mm means no separate thin-stock purchase.

PRELIMINARY — NOT FOR CNC. 2500 × 1600 sheets, 20 mm perimeter and 15 mm minimum finished-part spacing remain unchanged. The deterministic placement study tries orderings with actual contour overlays, not a claimed optimized nest. Small 12 mm parts share the same batch/offcuts; no special thin stock. Premium-first material policy remains. Supplier must qualify remnant hold-down and material quality.

| Mass from B-reps / explicit planning assumptions | LOW kg | NOMINAL kg | HIGH kg |
|---|---:|---:|---:|
| Delivered wood, including manual-finishing stock | 51.813 | 61.277 | 70.778 |
| Finished wood references | 51.785 | 61.242 | 70.734 |
| Mechanical planning scenario | 60.674 | 77.354 | 97.069 |
| Full planning build | 93.077 | 126.957 | 163.472 |

Delivered wood mass difference versus V33.6.3: **+0.552 kg nominal**. Plywood nominal density 650 kg/m³; LOW/HIGH and solid-wood density remain configurable. New unmeasured hardware is UNKNOWN, never silently zero. Optional fan blanks are included in the cut/packing BOM but excluded from simultaneous installed fan mass.

## Packaging

Preferred 20 kg planning-target bundles; each is below 25 kg including HIGH-density wood and estimated protective packaging. This keeps the same four-bundle count with about 5 kg margin to the 25 kg handling ceiling. Compared with the 25 kg candidate, total footprint rises 1.61% and aggregate volume 4.21%; long-panel protection is unchanged. The mixed fourth bundle is taller and requires careful labelled stacking. Hardware ships separately; glass and electronics are excluded. This is a handling/protection projection, not transit certification.

| Bundle | External L × W × H mm | Nominal wood kg | Gross HIGH kg |
|---|---|---:|---:|
| P20-01 | 1353.1 × 641.9 × 74 | 15.604 | 19.998 |
| P20-02 | 1317.1 × 617 × 88 | 15.568 | 19.995 |
| P20-03 | 825 × 768.9 × 128 | 15.680 | 19.999 |
| P20-04 | 1197.1 × 275 × 335.8 | 14.426 | 18.537 |

## Verification and promotion

| Evidence | Result |
|---|---|
| [Module, candidates, human/tool/cap/coin service](../exports/generated/two-stock-user-module-v337/module-validation.json) | PASS; 28 checks / member audits |
| [Thin-stock geometry](../exports/generated/two-stock-user-module-v337/conversion-validation.json) | PASS; 9 checks / member audits |
| [Converted wood motion/service](../exports/generated/two-stock-user-module-v337/conversion-motion.json) | PASS; 13 checks / member audits |
| [Combined native and all named states](../exports/generated/two-stock-user-module-v337/combined-validation.json) | PASS; 11 checks / member audits |
| [One-face manufacturing](../exports/generated/two-stock-user-module-v337/manufacturing-audit.json) | PASS; 17 checks / member audits |
| [Offline viewer / tablet / bilingual controls](../exports/generated/two-stock-user-module-v337/browser-validation.json) | PASS; 28 checks / member audits |
| [Exact-scope and authority regression](../exports/generated/two-stock-user-module-v337/validation.json) | PASS; 3939 checks / member audits |

Continuous differential checks cover playfield 0–50°,48 mm lift-out and populated backbox 0–90°. Unchanged interactions retain the exact preceding validated geometry. Combined evidence also requires the converted-wood motion and all preserved hardware-reserve audit hashes. Named poses reproduce the original state transforms before converted shapes are substituted; authoritative removed parts stay absent.

Side buttons, front relief, landings/slope, SW01, M006, M067 and unrelated objects are regression-protected. The CURRENT nominal plywood gate rejects any thickness outside 12/18, and requires both families. Historical snapshots remain untouched. New hardware rows are append-only; unknown quantities and bores are not frozen.

Hardware dashboard: 166 families; 41 required Fxx families; 180 known minimum fasteners plus 6 formula-driven and 6 genuinely TBD families. This is not a final screw count. New F62 × 4 and I19 × 4 are provisional; optional E15/E16 devices do not make electronics mandatory.

Viewer shows UNDERFRONT USER MODULE, OWNER_CONFIG / GENERIC_CONFIG / HARDWARE_PENDING, exact native variants, removable-module service, plate/button/USB/screw/insert exploded components, and updated stock/mass/packing. English/PT-BR, palettes, touch controls and offline operation are preserved. Manual step 07.3 documents installation and service; the historical fixed-function schematic is removed only from CURRENT.

## Release holds

- Actual 18 mm and 12 mm production-lot thickness; mandatory physical coupon and selected clearance.
- Purchased arcade buttons: bore, nut, microswitch, terminals and ergonomic verification.
- Physical dual USB module: inconsistent cutout, usable thread length through 12 mm, cap and first cable bend; optional rear pocket depth.
- Purchased module inserts/screws, converted filter-frame mounting stack, landing/WPC/other previously held hardware.
- Physical structural, ergonomic, service-loop, vibration and transport qualification.
- **FULL-SHEET CNC RELEASE: BLOCKED.** No production cutting files or G-code.

## Sources and review artifacts

- Authority: owner V33.7 instruction and exact V33.6.3 source B-reps; all dimensions above are design/reference unless explicitly measured. No purchased new hardware is claimed measured.
- [Joy-IT arcade-button manufacturer reference](https://joy-it.net/files/files/Produkte/Button-XXX/Button-XXX_Datasheet_2024-10-21.pdf): ordinary microswitch example, 28 mm hole/M28 and 35 × 67 mm overall; not selected hardware or final bore.
- USB: owner-supplied AliExpress seller-image description, unverified and internally inconsistent; no licensed seller CAD/image imported.
- [24 actual-CAD review views](../exports/generated/two-stock-user-module-v337/review.html), [native assembly](../exports/generated/two-stock-user-module-v337/play.FCStd), [offline viewer](../exports/generated/viewer-v32/index.html).
- [Material/mass/packing report](../exports/generated/two-stock-user-module-v337/stock-mass-packing-report.md), [manufacturing register](../exports/generated/two-stock-user-module-v337/manufacturing-register.json), [one-face audit](../exports/generated/two-stock-user-module-v337/manufacturing-audit.json).

Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

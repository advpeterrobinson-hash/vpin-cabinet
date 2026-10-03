# V33.5 — structural interfaces and owner visual corrections

HEAD BEFORE: `ca4e23eb598bb716156c41a7897ec8275e41f0ae`
HEAD AFTER: the commit containing this report (`git log -1 --format=%H -- exports/generated/structural-v335/README.md`).

[Offline viewer](../viewer-v32/index.html) · [24 review views](review.html) · [Manufacturing BOM](manufacturing-bom.md) · [BOM PT-BR](manufacturing-bom.pt-BR.md) · [Paper templates](../../../templates/pocket-holes/README.md) · [Manual](../../../docs/ASSEMBLY_MANUAL.md) · [Manual PT-BR](../../../docs/ASSEMBLY_MANUAL.pt-BR.md)

**CURRENT design candidate; full-sheet CNC release BLOCKED. No selected Kreg jig, screw, real plywood thickness or coupon clearance is inferred.**

## Decisions

| Interface | Decision | Evidence / limit |
|---|---|---|
| SW01 ×4 and universal drill jig | PRESERVED | All V33.4 source/artifact hashes retained; no laminated leg pieces resurrected |
| Floor ↔ sides | PROMOTE nominal4mm capture | Exact assembled shell union unchanged;14mm nominal residual side skin. Fit = measured thickness + coupon clearance |
| Front/rear ↔ sides | PROMOTE4mm captured open-end rabbets | Exterior and existing diagonal leg-bore voids preserved; glue plus qualified mechanical retention required |
| M006 ×2 | KEEP | Existing30mm underside ledges carry floor bearing; not unexplained floating wood |
| RearBearingShelf | PROMOTE4mm side capture | Open-top rabbets with bearing shoulders; topZ596.9 unchanged |
| Underside pockets | HARDWARE_DEPENDENT | Actual3D reference screws/counterbores/drivers screened; physical jig, screw and drilling not released |
| Rear fan fasteners | PROMOTE architecture | Interior → head → inner grill → fan → rear wood. Retire rear through-bolts/nuts; final wood pilot/length held |
| Cradles | KEEP original | Rejected trim preserves root minimum but narrows upper guide wall23.5→8.251mm. Equal root is insufficient evidence of equal ear stiffness |
| T3 −20mm | REJECT | Does not remove seat/WPC/S3 constraints; moving an accepted crossmember provides no necessary simplification |
| S3 | KEEP | No±20mm move selected or needed |
| Monitor stops | REPLACE six wood pieces with M067 ×1 | One330×18×18mm transverse rail,6mm captured end lands and two rear retention screws; two M6-family supports; main display clamps unchanged |
| M049 /4mm plywood | REMOVE | Purchased replaceable contact tips replace both pads; zero4mm wood pieces |

## Plunger and under-front controls

The latest front-panel authority (`config/front_panel_v32.json`, `tools/front_panel_v32_entry.py`) places the plunger at X520/Z280. Its internal40×202×40mm service reserve is unchanged. A front interface, shaft and handle are now visible, with a separate front extraction reference. These are original provisional visual envelopes, not a selected product. FRONT receives no plunger bore. Exact body, travel, grip, mounting and tool clearances require the purchased part.

The owner confirmed `docs/SERVICE_IO_V08.md`, `config/service_io_v08.json`, DEC-016 and historical commit `2eed36e4ff6e0871edc4d7d845288c5a629fd8b9`. The220×55mm underside-front panel intent is restored in a clearly UNLOCATED schematic in viewer/manual: master volume, OFF/AUDIO/PINBALL selector, Bluetooth pair and optional USB-C charging. There is no authoritative installed origin or drilled control-center layout. Both remain null; controls are not placed at invented cabinet coordinates. Ergonomics, internal clearance, holes and recesses are PURCHASE_BEFORE_CNC. This local hold does not block the other design studies.

## Captures, glue and load paths

Floor reaction now has continuous side capture shoulders of5088.4mm² per side, in addition to retained M006 bearing. Four rather than six millimetres retains14mm nominal side skin and improves the reference pocket-screw bite. The4–6mm study range is geometrically feasible only for the stated study screw axis; it is not a certified range for an unknown commercial jig. Front/rear use simple open-end captured rabbets, avoiding decorative tabs. The exact existing leg bores are transferred with their wood rather than filled by arbitrary new strips.

M006 provides30mm bearing under each long floor edge. Removing it changes the conservative one-way floor-strip clear span from504 to564mm: stress multiplier 1.252 and deflection multiplier 1.568 under equal distributed loading/material. This is a relative screen, not a plate strength certification. Saving 0.809kg does not justify declaring these supports redundant without the real floor load/material qualification. Glue the floor/side lands and retain F06 as the unresolved final mechanical-fixing family; no false screw count is introduced.

Two564×50×18mm transverse offcuts are shown as OPTIONAL ASSEMBLY TOOLING, not cabinet parts, not a replacement for M006, and not included in permanent mass or wood bundles. They can support a dry shell on a flat datum but must be removed before conflicting underside access. The selected sequence does not require shipping them.

SideL on flat reference → qualified SW01 work before floor closure → dry-fit Floor/Front/Rear/RearBearingShelf → close SideR → shoulders seated → diagonals and600mm external width → disassemble → approved glue → reassemble/clamp → recheck → qualify/install underside pocket retention while M006 is absent → attach retained M006 → cure → remove optional tooling. Turn/support the unloaded shell for underside access; do not drill against the workbench. Never use screws to pull a bad fit into place.

Rear shelf vertical reaction goes principally through the two4×162.975mm side shoulders, not pocket screws. The existing top datum and assembled supporting top surface stay fixed. The backbox contact assigned specifically to the shelf is 65446.205→66599.005mm² because the captured tabs are now shelf material previously belonging to the side tops. This is intentional attribution/area improvement, not a moved backbox or reduced bearing. Locks, passage and WPC axis are unchanged.

## Pocket-axis study

Reference packaging assumptions:15° screw elevation;28mm under-head cylinder;4mm nominal shank;9.5mm counterbore; head14mm inward from side inner face and6mm above panel underside. These are explicit study assumptions, NOT dimensions of a Kreg product. Driver is a conservativeR9×160mm straight corridor beginning28mm behind the head. A real drill/jig housing and stop collar have not been qualified. No pockets or screw pilots are cut into CURRENT wood from these assumptions.

| Capture mm | Nominal outside skin mm | Side screw engagement mm | Screw-tip exterior margin mm | Counterbore-to-top wood mm | Dado-edge margin mm | Result |
|---:|---:|---:|---:|---:|---:|---|
| 4 | 14 | 9.365 | 4.436 | 7.412 | 5.245 | REFERENCE GEOMETRY PASS / HARDWARE_DEPENDENT |
| 5 | 13 | 8.330 | 4.436 | 7.412 | 4.977 | REFERENCE GEOMETRY PASS / HARDWARE_DEPENDENT |
| 6 | 12 | 7.294 | 4.436 | 7.412 | 4.709 | REFERENCE GEOMETRY PASS / HARDWARE_DEPENDENT |

Each of the48 depth/station cases records entry, head, axis, tip, side-entry, margins and collisions in [geometry-validation.json](geometry-validation.json). Floor stations: Y160/340/520/840/1020/1180 per side; shelf: Y1155/1220 per side. M006 would obstruct underside operation and is deliberately installed afterwards. Leg blocks, fans/filters, PCBase, shelf/lock/WPC reserves and other wood were screened; adjacent station spacing is generous. Purchased-jig/body/hand-access qualification is still required.

Paper SVGs include canonical ID, installed FRONT/REAR/LEFT/RIGHT, numbered stations, orientation, station reference line, end keepouts,100×100mm square and100mm bar. They locate stations only: jig-reference-to-bit offset is null. PRINT100% / ACTUAL SIZE / NO FIT. No proprietary guide angle or template offset is encoded. Shelf FACE_A remains top and underside drilling is manual referenced through actual thickness; no CNC flip.

## Fan reconciliation

F56 ×8 is the optional rear wood-screw family, with diameter/length null. The nominal visual stack is1.5mm inner grill +25mm fan +12mm reference wood bite; real flange/full-length grip depends on the fan. F10 rear through bolts are historical-only. I03 now counts only the eight floor-fan nuts; rear-only washers and outer guards are removed from the active stack. No unrelated floor-fan hardware is changed. Eight oldØ4.5 rear clearance holes are withdrawn and wood restored: using them as wood-screw anchors would be invalid. Replacement pilots require purchased screw/wood qualification; no final bore is substituted.

## Monitor rail structural/access screen

M067 is one18mm stock part,330×18mm planar outline, installed Z917–935, Y1228–1246. Each50mm carrier receives a6mm front-face capture, leaving12mm nominal carrier thickness. Bearing land is300mm² per carrier. F57 ×2 rear-driven retention screws prevent disengagement; exact pilot and length remain held. Rear driverR8×90mm envelopes pass with doors open. Two M6-family adjusters sit at reference X214/386,Y1237, with required contact-top rangeZ944–954. Their inserts, locknuts and polymer tips remain purchased-hardware envelopes, not drilling authority.

The rail supports adjustment loads only. Existing four monitor-retention bolts remain responsible for normal-to-screen and fold loads. Nominal insert packaging must be qualified in the18mm rail: a provisional9mm insert OD would leave4.5mm edge wood, but no OD is selected. Straight grain along the rail, laminate quality, insert pullout, captured-land bearing, rear screw retention and deflection require coupon/load review. At a conservative32kg total planning load split across the two300mm² end lands, average bearing pressure would be0.523MPa; this area screen is not a strength rating. No custom metal or gravity-only monitor retention is introduced.

The16mm depth positions and ±5mm vertical/±1mm large-display centering remain available. The rail moves with the carriers. Front display/adapter removal, glass lift, cassette extraction, lock operation and both rear doors were screened against its new material. The continuous0–90° WPC certificate uses the unchanged Y1066.8/Z508 axis.

## Cradle decision

Current and final minimum rear ligament:6.279670mm. Current and final minimum front seat root:8.250620mm. Seat180°, Ø32 dowel, R12 WPC reserve +2mm allowance, six support screw coordinates and full foot are unchanged. The rejected candidate reduces13 exterior edges to11 but narrows the upper front wall over a substantial height; no claim of equal stiffness is made. T3−20mm was modeled as a diagnostic only. S3±20mm was not needed. No accepted playfield function or coordinate moves.

## Manufacturing, material and mass

| Measure | Before | After |
|---|---:|---:|
| Permanent wood pieces |106|101|
| CNC plywood pieces |102|97|
| Shop-made SW01 |4|4|
| Families |62|59|
|4mm plywood pieces |2|0|

Status counts: ONE_SIDE_CNC_PLUS_MANUAL_FINISH=51, ONE_SIDE_CNC_READY=46, SHOP_MADE_SOLID_WOOD_PART=4. These mean an operation plan exists, not CNC release. Changed stock widths still depend on actual material/coupon. Ø4 cutter/R2 corners are explicitly hand-finished where square mating requires it, or await a later qualified local relief.

| Stock mm | Pieces | Finished outer area m² | Full-sheet assumption | Gross net utilization % | Practical purchasing |
|---:|---:|---:|---:|---:|---|
| 18 | 59 | 5.238946 | 2 | 55.13 | Premium stock first; quoted cut-to-size rectangles or full sheets subject to supplier holding approval |
| 12 | 23 | 1.227030 | 1 | 27.79 | Premium stock first; quoted cut-to-size rectangles or full sheets subject to supplier holding approval |
| 8 | 2 | 0.057800 | 1 | 0.89 | Qualified premium offcut/small stock; do not buy full sheet solely for these pieces |
| 6 | 13 | 0.498020 | 1 | 4.64 | Qualified premium offcut/small stock; do not buy full sheet solely for these pieces |

Stock families after study:18/12/8/6mm plywood plus SW01 solid wood. No4mm sheet. Preliminary layouts keep2500×1600 sheets,20mm border and15mm spacing; they are conservative non-production feasibility studies, not optimized/released nesting. Small6/8mm needs should use qualified premium offcuts/smaller stock. Premium-first and structural-material restrictions remain unchanged.

Wood shipping mass LOW/NOMINAL/HIGH: **51.316kg / 60.690kg / 70.100kg**, from actual B-rep volumes plus the four undrilled SW01 stock blanks. Plywood densities550/650/750kg/m³; solid500/650/850kg/m³. Assembly tooling is separate. Mechanical mass is an illustrative range with explicit unknown-hardware allowances, not a weighed total.

| Bundle | External L×W×H mm | Gross nominal kg | High-density kg |
|---|---|---:|---:|
| P25-01 | 1353.1×641.9×98 | 21.958 | 24.985 |
| P25-02 | 1317.1×617×88 | 21.937 | 24.999 |
| P25-03 | 825×768.9×197.8 | 21.995 | 24.999 |
| P25-04 | 1197.1×240×182 | 2.687 | 3.005 |

All preferred bundles are≤25kg at high planning density. Long/wide bundles may still require two people. Hardware, glass and electronics are separate; SW01 retains padded layering. Transit protection and actual density require physical confirmation.

Required Fxx models: **37**. Known numeric minimum: **162**, plus formula-driven F53, F18, F36, F38, F39, F58, plus genuinely unresolved F06, F16, F19, F22, F28, F31. This is not a final screw count. F28 remains unresolved for other monitor joints; F57 separately closes the two rail-retention positions. F58 pocket schedule remains hardware-dependent.

## Validation and release

Native geometry checks: 21; differential service checks: 28; protected-source/data checks: 602; offline browser checks: 145. See [validation.json](validation.json), [motion-validation.json](motion-validation.json), [browser-validation.json](browser-validation.json).

Eight existing wood components intentionally change: SIDE_L/R, FRONT, REAR, FLOOR, BACKBOX_BASE, BB_MonitorCarrier0/1. Four obsolete installed stop/pad components are replaced by one rail. The exact per-component symmetric differences are listed below. New hardware/plunger visuals are provisional. Everything else is protected by exact B-rep/mesh comparisons and baseline file hashes. SW01 and its jig are byte-preserved; WPC, playfield, matrix, backbox210mm sides/Y1146 floor, service doors and normal fold prerequisites remain unchanged.

| Changed B-rep | Before mm³ | After mm³ | Symmetric difference mm³ |
|---|---:|---:|---:|
| SIDE_L | 12039540.439305 | 11865853.838038 | 173686.600982 |
| SIDE_R | 12039540.439305 | 11865853.838038 | 173686.600982 |
| FRONT | 2539238.518909 | 2595426.515549 | 56188.004093 |
| REAR | 3262725.043844 | 3349549.623129 | 86824.586469 |
| FLOOR | 12231841.520123 | 12415023.920123 | 183182.400000 |
| BACKBOX_BASE | 1369311.403914 | 1392779.803914 | 23468.400000 |
| BB_MonitorCarrier0 | 325865.409393 | 320465.409393 | 5400.000000 |
| BB_MonitorCarrier1 | 325865.409393 | 320465.409393 | 5400.000000 |

The joinery transfer alone preserves the exact occupied shell union. Restoring the eight obsolete rear fan bores is an additional intentional2,290.221mm³ of wood. The rail/carrier captures and retired stops are separately listed; no whole-model equality claim hides these edits.

All assembly clips remain SCHEMATIC where insertion/hand/tool trajectories are not fully qualified. Established service paths retain their separate certificates. The under-front schematic is an intent illustration, not CAD fit evidence.

**Remaining release gates:** real plywood lot and thickness; selected coupon clearance and regenerated fits; actual Kreg model/drill/collar/screws; fan screws/pilots; rail inserts/adjusters/retention hardware and load qualification; existing F06/F28 and other unresolved hardware; physical WPC family; matrix confirmation; remaining structural/ergonomic qualification. Supplier values are unchanged. No full-sheet cutting files or G-code were generated.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

# Assembly manual framework — V33.2

**FRAMEWORK — MANUFACTURING RELEASE BLOCKED. Hardware, coupon and physical qualification holds remain.**

[Offline interactive manual and CAD](../exports/generated/viewer-v32/index.html?manual=00)

Quantities below are global/stage reference totals; repeated steps do not consume another kit. Unknown counts remain unknown. A tray exemplar is not an installed position.

<a id="stage-00"></a>
## 00 — Before you start

**WAITING_FOR_COUPON** · Depends on: —

Pieces (each instance ×1): —

| ID | Hardware | Project quantity | Status |
|---|---|---|---|

### 00.1 — Confirm the preparation holds

Read the supplier profile and inventory the production lot. Do not cut full sheets until actual thickness, coupon clearance and hardware interfaces are approved.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Record the measured lot, coupon result and selected hardware; unresolved values stay HOLD.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: PLAY](../exports/generated/viewer-v32/index.html?manual=00&step=00.1&state=PLAY&lang=en)

### 00.2 — Prepare ordinary assembly tools

Prepare clamps, square, tape, drill/driver, depth stop, selected bits and qualified angle guides. Exact drive sizes follow purchased hardware. Do not improvise precise angled drilling freehand.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** A qualified guide and finish procedure must exist before each affected manual operation.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: PLAY](../exports/generated/viewer-v32/index.html?manual=00&step=00.2&state=PLAY&lang=en)

<a id="stage-01"></a>
## 01 — Identify flatpack parts

**WAITING_FOR_COUPON** · Depends on: 00

Pieces (each instance ×1): —

| ID | Hardware | Project quantity | Status |
|---|---|---|---|

### 01.1 — Match manufacturing IDs and faces

Match every M-family and P-instance against the 130-piece register. Use the orientation cards: FACE A is the finished machining datum; FACE B receives no CNC. Keep mirrored parts labelled.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Count 130 pieces in 66 families. Do not mistake 93 installed assemblies for the cut-piece count.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=01&step=01.1&state=EXPLODED%20DETAILED&lang=en)

### 01.2 — Check CNC work and builder finish

Use each piece’s preparation card. Check the contour and FACE A pockets first; then perform only the listed manual drilling, countersinking or corner/bevel finish after its holds clear. Depths refer to finished FACE A, including after face reduction.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Never request a second CNC face. Trial-fit without forcing thickness-dependent joints; physical coupon approval is mandatory.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=01&step=01.2&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-02"></a>
## 02 — Main cabinet shell

**PROVISIONAL_HARDWARE** · Depends on: 01

Pieces (each instance ×1): P001-Main (M001), P002-Main (M002), P003-Main (M003), P004-Main (M004)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F06 | Cabinet shell/floor/cleat joint fasteners | TBD — do not guess | PURCHASE_BEFORE_CNC |
| G01 | Plywood joint adhesive | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |

### 02.1 — Dry-assemble sides and ends

Orient SideL/SideR from the player position, front at Y0. Dry-assemble front and rear against the full-strength side structure. Keep the shell supported and unclamped enough to square.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** CABINET SQUARE CHECK: compare diagonals and seating on a flat reference. No numerical tolerance is released yet.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED OVERVIEW](../exports/generated/viewer-v32/index.html?manual=02&step=02.1&state=EXPLODED%20OVERVIEW&lang=en)

### 02.2 — Qualify permanent shell joints

Use the approved glue/fastener schedule when available. F06 and adhesive consumption G01 remain unresolved; this framework does not invent screw spacing. Keep joint faces free of finish until bonding is qualified.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** HOLD permanent assembly until the joint schedule and material/bond qualification are complete.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED OVERVIEW](../exports/generated/viewer-v32/index.html?manual=02&step=02.2&state=EXPLODED%20OVERVIEW&lang=en)

<a id="stage-03"></a>
## 03 — Floor and structural supports

**PROVISIONAL_HARDWARE** · Depends on: 02

Pieces (each instance ×1): P005-Main (M005), P006-Main (M006), P007-Main (M006), P028-Main (M018)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|

### 03.1 — Seat floor, cleats and rear shelf

Fit the floor and its cleats to their exact mating shoulders. Install BBBase as the upright backbox bearing shelf; preserve the generic cable passage and lock receiver material.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Confirm continuous floor support and the shelf’s broad bearing faces. Do not use screws to pull a distorted shell into alignment.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: INTERIOR INSPECTION](../exports/generated/viewer-v32/index.html?manual=03&step=03.1&state=INTERIOR%20INSPECTION&lang=en)

<a id="stage-04"></a>
## 04 — Shelves, crossmembers and PCBase

**PROVISIONAL_HARDWARE** · Depends on: 03

Pieces (each instance ×1): P009-Main (M008), P010-Main (M008), P011-Main (M009), P012-Main (M010), P013-Main (M011), P014-Main (M010), P015-Main (M011), P016-Main (M012), P017-Main (M013), P018-Main (M014), P019-Main (M014), P020-Main (M014), P021-Main (M015), P022-Main (M016), P023-Main (M015), P024-Main (M016), P025-Main (M015), P026-Main (M016), P027-Main (M017)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F03 | Shelf top-release M5 screw | 12 | PURCHASE_BEFORE_CNC |
| W01 | M5 load-spreading washer, current Ø12 ×1 | 12 | PURCHASE_BEFORE_ASSEMBLY |
| I01 | M5 shelf captive insert | 12 | PURCHASE_BEFORE_CNC |
| F04 | Fixed shelf-support wood screw | 12 | PURCHASE_BEFORE_CNC |
| W02 | Ø4 clearance washer, Ø9 ×1 | 12 | PURCHASE_BEFORE_ASSEMBLY |
| B02 | Commodity support angle, 40 ×40 ×50 ×3 reserve | 6 | PURCHASE_BEFORE_CNC |
| F05 | Crossmember guide attachment screws | 24 | PURCHASE_BEFORE_CNC |
| F52 | M5-family crossmember support-angle bolts | 12 | PURCHASE_BEFORE_CNC |
| I14 | Crossmember angle captive-thread/retention set | 12 | PURCHASE_BEFORE_CNC |
| F07 | PCBase flush M5 floor anchors | 4 | PURCHASE_BEFORE_CNC |
| I02 | PCBase M5 retaining nuts | 4 | PURCHASE_BEFORE_ASSEMBLY |
| W03 | PCBase M5 underside backing washers | 4 | PURCHASE_BEFORE_ASSEMBLY |

### 04.1 — Install guides and shelf supports

Identify S1–S3 and T1–T3 with their matching supports/guides. Use the actual mounting interfaces; F05/F52/I14 are catalog hardware, not permission to guess unlocated holes.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** SHELF HEIGHT CHECK: confirm left/right seats align and removable shelves/crossmembers can be extracted without forcing.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=04&step=04.1&state=EXPLODED%20DETAILED&lang=en)

### 04.2 — Secure removable boards

Fit shelf clamp hardware and PCBase flush floor anchors only after their stack is confirmed. PCBase is the accepted low board, not a drawer. Electronics payloads are optional later additions.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Check positive retention and service removal; keep side-wall SSF zones unbridged.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=04&step=04.2&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-05"></a>
## 05 — Playfield wooden pivot supports

**PROVISIONAL_HARDWARE** · Depends on: 03, 04

Pieces (each instance ×1): P035-Main (M026), P036-Main (M027)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F01 | Cradle support wood screw | 6 | PURCHASE_BEFORE_CNC |

### 05.1 — Install both open cradles

Place each 18 mm cradle directly on the cabinet floor and against its side. Preserve the open pivot relief and all six F01 coordinates. The screws retain against tipping/separation; vertical load bears on the floor.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** CRADLE ALIGNMENT CHECK: both seats share the accepted axis and both feet bear continuously. Do not shim or relocate the axis without a new review.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=05&step=05.1&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-06"></a>
## 06 — Playfield base, dowel and straps

**PROVISIONAL_HARDWARE** · Depends on: 05

Pieces (each instance ×1): P034-Main (M025)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F02 | Saddle-strap wood screw | 8 | PURCHASE_BEFORE_CNC |
| H01 | Wooden pivot dowel | 1 | PURCHASE_BEFORE_CNC |
| B01 | Commercial saddle strap for Ø32 wooden dowel | 4 | PURCHASE_BEFORE_CNC |

### 06.1 — Capture the wooden dowel

Attach the Ø32 wooden dowel with four commercial saddle straps B01 and eight F02 screws to the playfield base. Retain the accepted replaceable adapter interface. No metal shaft or bearings.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Check strap seating, screw engagement and no splitting after purchased strap/material qualification.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: PLAYFIELD LIFT-OUT](../exports/generated/viewer-v32/index.html?manual=06&step=06.1&state=PLAYFIELD%20LIFT-OUT&lang=en)

### 06.2 — Check seating and removal

Lower both dowel ends into the open seats. With main glass and matrix removed, demonstrate the accepted 48 mm vertical lift-out. The complete playfield assembly leaves together; fixed cradles remain.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** DOWEL LIFT-OUT CHECK: no binding, approximately semicircular support retained. The 50° service pose is a geometric view; do not work beneath an unsupported raised assembly. Support/load qualification remains pending.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: PLAYFIELD LIFT-OUT](../exports/generated/viewer-v32/index.html?manual=06&step=06.2&state=PLAYFIELD%20LIFT-OUT&lang=en)

<a id="stage-07"></a>
## 07 — Main rear services and fans

**PROVISIONAL_HARDWARE** · Depends on: 03

Pieces (each instance ×1): P008-Main (M007), P037-Main (M028), P038-Main (M028)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| H02 | Main rear door hinge assembly | 2 | PURCHASE_BEFORE_CNC |
| H03 | Main rear keyed cam-lock assembly | 1 | PURCHASE_BEFORE_CNC |
| B03 | Main rear lock keeper | 1 | PURCHASE_BEFORE_CNC |
| H04 | Main rear door handle | 1 | PURCHASE_BEFORE_CNC |
| F08 | M4 ×20 handle screw | 2 | PURCHASE_BEFORE_CNC |
| F09 | Main rear hinge fixing screws | 8 | PURCHASE_BEFORE_CNC |
| F53 | Main rear keeper fixing screws | 1 * selected_keeper.mounting_hole_count - included_fasteners | PURCHASE_BEFORE_CNC |
| G02 | Main rear door contact felt | TBD — do not guess | OPTIONAL |
| H05 | Optional main rear door limiter set | 1 | OPTIONAL |
| H06 | Optional main rear slide bolt | 1 | OPTIONAL |
| F10 | M4 ×55 main rear fan bolt | 8 | PURCHASE_BEFORE_CNC |
| I03 | M4 fan nut | 16 | OPTIONAL |
| F11 | M4 ×50 floor fan bolt | 8 | PURCHASE_BEFORE_CNC |
| F12 | M4 ×16 floor-filter screw | 8 | PURCHASE_BEFORE_CNC |
| I04 | M4 blind floor-filter insert | 8 | PURCHASE_BEFORE_CNC |
| H07 | 120 mm main/floor optional fan | 4 | PURCHASE_BEFORE_CNC |
| B04 | 120 mm main rear fan finger guard | 4 | OPTIONAL |
| B05 | Floor intake lower guard | 2 | PURCHASE_BEFORE_CNC |
| B06 | Floor fan upper finger guard | 2 | OPTIONAL |
| F13 | Short floor lower-guard attachment screws | 8 | PURCHASE_BEFORE_CNC |
| G03 | Floor intake replaceable filter media | 2 | PURCHASE_BEFORE_ASSEMBLY |

### 07.1 — Fit rear door hardware

Fit the main rear door, its two hinge assemblies, keeper and lock from the selected hardware. Main rear hinge hardware is separate from the backbox piano hinges. Keep selected-hardware quantities as formulas.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** REAR DOOR SWEEP CHECK: verify opening, latch engagement and ordinary tool access without forcing the flush door.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: INTERIOR INSPECTION](../exports/generated/viewer-v32/index.html?manual=07&step=07.1&state=INTERIOR%20INSPECTION&lang=en)

### 07.2 — Prepare optional fan/filter stations

Assemble removable filter frames and selected guards. Fans are optional; M4 fastener lengths follow the actual station stack. Do not install loose fasteners into an unused opening or assume one bolt length fits every station.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Filters remain serviceable; no fan or electronics purchase is required to understand the mechanical kit.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: INTERIOR INSPECTION](../exports/generated/viewer-v32/index.html?manual=07&step=07.2&state=INTERIOR%20INSPECTION&lang=en)

<a id="stage-08"></a>
## 08 — Backbox shell

**PROVISIONAL_HARDWARE** · Depends on: 03

Pieces (each instance ×1): P042-Main (M031), P043-Main (M032), P044-Main (M033), P045-Main (M034), P046-Main (M035), P047-Main (M036)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F16 | Backbox shell/frame/rail joint screws | TBD — do not guess | PURCHASE_BEFORE_CNC |
| F54 | Backbox side-to-floor joint screws | 6 | PURCHASE_BEFORE_CNC |

### 08.1 — Assemble the structural backbox

Assemble 210 mm lower-depth sides, Y1146 straight-front floor, top and fixed rear frame. The side projection ahead of the floor is intentional. Maintain structural validity with both rear doors open.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Confirm floor/side engagement and rear-frame squareness. F16 joint schedule and adhesive qualification remain HOLD.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=08&step=08.1&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-09"></a>
## 09 — WPC hardware and upright locks

**WAITING_FOR_PHYSICAL_MEASUREMENT** · Depends on: 05, 08

Pieces (each instance ×1): P088-Main (M064), P089-Main (M065), P090-Main (M064), P091-Main (M065)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| H08 | WPC 01-9011-L left | 1 | PURCHASE_BEFORE_CNC |
| H09 | WPC 01-9011-R right | 1 | PURCHASE_BEFORE_CNC |
| H10 | WPC 02-4352 bushing | 2 | PURCHASE_BEFORE_CNC |
| F14 | WPC 4322-01139-12B pivot bolt | 2 | PURCHASE_BEFORE_CNC |
| F15 | WPC floor attachment fasteners | 6 | PURCHASE_BEFORE_CNC |
| W06 | WPC pivot/floor washer and nut stack | sum(required_stack_items_for_2_pivots_and_6_floor_bolts) - matching_items_in_purchased_kits | PURCHASE_BEFORE_CNC |
| B16 | WPC floor backing plate | 2 | PURCHASE_BEFORE_CNC |
| H11 | M8 ×40 captive upright-lock hand knob | 2 | PURCHASE_BEFORE_CNC |
| W07 | Captive upright-lock load washer | 2 | PURCHASE_BEFORE_CNC |
| I05 | M8 metal-backed shelf captive receiver | 2 | PURCHASE_BEFORE_CNC |
| I06 | M8 metal parking insert | 2 | PURCHASE_BEFORE_CNC |
| F17 | Parking-pad countersunk wood screw | 4 | PURCHASE_BEFORE_CNC |
| H12 | Mechanical knob tether, 200 mm | 2 | PURCHASE_BEFORE_ASSEMBLY |
| W08 | Captive washer retention ring | 2 | PURCHASE_BEFORE_ASSEMBLY |
| H13 | Rotating loss-protection ring | 2 | PURCHASE_BEFORE_ASSEMBLY |
| B07 | Positive tether slack keeper | 2 | PURCHASE_BEFORE_ASSEMBLY |
| B08 | Parking-block tether anchor | 2 | PURCHASE_BEFORE_CNC |

### 09.1 — Measure and install the WPC family

Measure 01-9011-L/R, 02-4352 and 4322-01139-12B before any final hinge drilling. The reference rotation axis is Y1066.8/Z508; it is not a released drill pattern. Do not substitute metric threads into purchased imperial hardware.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** HOLD installation until bends, floor-hole pattern, bushing and complete bolt stack are measured and validated.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX UNLOCKED](../exports/generated/viewer-v32/index.html?manual=09&step=09.1&state=BACKBOX%20UNLOCKED&lang=en)

### 09.2 — Fit two rear-operated captive locks

Retain H11 ×2 at L X130/Y1260 and R X470/Y1260 with metal-backed shelf receivers, loss protection, tethers and parking sockets. Exact purchased knob/receiver details remain provisional.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** UPRIGHT LOCK CHECK: floor bears broadly on shelf; both independent clamps engage and can be released/parked through open rear doors with cassette installed.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX UNLOCKED](../exports/generated/viewer-v32/index.html?manual=09&step=09.2&state=BACKBOX%20UNLOCKED&lang=en)

<a id="stage-10"></a>
## 10 — Twin backbox rear doors

**PROVISIONAL_HARDWARE** · Depends on: 08, 09

Pieces (each instance ×1): P079-Main (M056), P080-Main (M057), P085-Reduced18 (M062), P086-Reduced18 (M062), P087-Main (M063)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| H14 | 628 mm continuous backbox door hinge | 2 | PURCHASE_BEFORE_CNC |
| H15 | Backbox active-door keyed cam lock | 1 | PURCHASE_BEFORE_CNC |
| H16 | Backbox passive-leaf retaining bolt | 2 | PURCHASE_BEFORE_CNC |
| F18 | Backbox piano-hinge fixing screws | 2 * (fixed_leaf_holes_used + moving_leaf_holes_used) - included_hinge_screws | PURCHASE_BEFORE_CNC |
| F19 | Backbox latch/astragal fasteners | TBD — do not guess | PURCHASE_BEFORE_CNC |
| G04 | Backbox perimeter door gasket | 2 | PURCHASE_BEFORE_ASSEMBLY |
| G05 | Backbox center meeting-line gasket | 1 | PURCHASE_BEFORE_ASSEMBLY |

### 10.1 — Fit hinge cleats and leaves

Use the 18 mm cleats reduced from FACE A to the accepted 14 mm finished geometry. Preserve the hinge axis. Install one continuous hinge on each outer vertical edge; screw count follows the selected hinge hole schedule.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** No permanent center mullion. Both doors must reach the validated 100° service position upright.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX REAR DOORS OPEN](../exports/generated/viewer-v32/index.html?manual=10&step=10.1&state=BACKBOX%20REAR%20DOORS%20OPEN&lang=en)

### 10.2 — Fit passive bolts, astragal and active lock

Secure passive upper/lower bolts first, then close the active leaf and keyed cam lock against the overlap. Fit replaceable perimeter and center gaskets. Open active leaf before passive leaf.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** REAR DOOR SWEEP CHECK: no clash with fan bodies, loops, overlap or lock hardware. Doors are service closures, not structural shear panels.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX REAR DOORS OPEN](../exports/generated/viewer-v32/index.html?manual=10&step=10.2&state=BACKBOX%20REAR%20DOORS%20OPEN&lang=en)

<a id="stage-11"></a>
## 11 — Backbox ventilation

**PROVISIONAL_HARDWARE** · Depends on: 10

Pieces (each instance ×1): P081-Main (M058), P082-Main (M058), P083-Face (M059), P083-Top (M060), P083-Side1 (M061), P083-Side2 (M061), P084-Face (M059), P084-Top (M060), P084-Side1 (M061), P084-Side2 (M061), P092-Main (M066), P093-Main (M066)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| H17 | Optional 120 mm backbox door fan | 2 | PURCHASE_BEFORE_CNC |
| B09 | Backbox fan finger guard | 2 | OPTIONAL |
| G06 | Backbox fan dust mesh/filter | 2 | OPTIONAL |
| G07 | Backbox low-intake filter/mesh | 2 | PURCHASE_BEFORE_ASSEMBLY |
| F20 | M4 backbox fan-station bolt, length pending | 8 | PURCHASE_BEFORE_CNC |
| F21 | M4 backbox blank-station fixing | 8 | PURCHASE_BEFORE_CNC |
| I07 | M4 station captive nut/insert | 8 | PURCHASE_BEFORE_CNC |
| F22 | Backbox intake frame/baffle/filter fixings | TBD — do not guess | PURCHASE_BEFORE_CNC |
| B10 | Flexible fan-cable clamp/strain relief | 4 | PURCHASE_BEFORE_CNC |
| F23 | Fan-loop clamp screws | TBD — do not guess | PURCHASE_BEFORE_CNC |
| B11 | Optional downward fan dust hood | 2 | OPTIONAL |
| F55 | Optional dust-hood service screws | 4 | OPTIONAL |

### 11.1 — Assemble intake baffles and filter frames

Build each baffle from its face, top and two returns using the four actual manufacturing pieces. Keep the downward mouth open and filters removable. Qualified glue seams must not obstruct the throat.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Per door: preserve 220×80 mm inlet and 220×36 mm downward mouth before mesh effects. No thermal certification is implied.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=11&step=11.1&state=EXPLODED%20DETAILED&lang=en)

### 11.2 — Choose blank or optional fan

Install the blank module for an unpowered station, or a selected 120 mm fan/accessory stack. For a moving fan, preserve the low-voltage flexible corridor and strain relief through full door motion; connectors remain builder-configurable.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Check ordinary screwdriver access with the door open; no display removal. Fine exhaust filters need later pressure-loss analysis.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=11&step=11.2&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-12"></a>
## 12 — Backglass carrier

**PROVISIONAL_HARDWARE** · Depends on: 08

Pieces (each instance ×1): P050-Main (M040), P051-Main (M041), P052-Main (M041), P053-Main (M040), P054-Main (M041), P055-Main (M041), P056-Main (M042), P057-Main (M043), P058-Main (M043), P059-Main (M042), P060-Main (M043), P061-Main (M043), P062-Main (M044), P063-Main (M045), P064-Base18 (M046), P064-Cap12 (M047), P065-Base18 (M048), P065-Cap12 (M047), P066-Main (M049), P067-Main (M049)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F25 | Monitor depth-position M6 through bolt | 4 | PURCHASE_BEFORE_CNC |
| F26 | Monitor alignment M6 clamp bolt | 4 | PURCHASE_BEFORE_CNC |
| W09 | Monitor M6 large clamping washer | 16 | PURCHASE_BEFORE_ASSEMBLY |
| I09 | Monitor M6 positive-retention nuts | 8 | PURCHASE_BEFORE_ASSEMBLY |
| F27 | Monitor M6 adjustable lower stop | 2 | PURCHASE_BEFORE_CNC |
| I10 | M6 stop captive thread | 2 | PURCHASE_BEFORE_CNC |
| I11 | M6 stop locknut | 2 | PURCHASE_BEFORE_ASSEMBLY |
| F28 | Monitor ladder/stop/cleat wood joints | TBD — do not guess | PURCHASE_BEFORE_CNC |

### 12.1 — Build rails, adjustable carriers and stops

Use the real monitor-stop bases and caps, glued on their broad faces after qualification. Fit depth shoes, clamping washers/nuts and replaceable VESA plate. Leave adjustments loose only during alignment.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** The mechanical carrier is retained without requiring a monitor purchase. No permanent display-specific hole pattern.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX INTERIOR](../exports/generated/viewer-v32/index.html?manual=12&step=12.1&state=BACKBOX%20INTERIOR&lang=en)

### 12.2 — Explain later front installation and rear adjustment

When selected, install the 31.5/32-inch display from the front, access alignment from the open rear doors and positively clamp every axis. VESA screws are user-adapter hardware and follow the display manufacturer.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** No gravity-only hook, glass support or cassette support for display mass. Recheck retention through fold before use.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX INTERIOR](../exports/generated/viewer-v32/index.html?manual=12&step=12.2&state=BACKBOX%20INTERIOR&lang=en)

<a id="stage-13"></a>
## 13 — Backbox front glass

**WAITING_FOR_PHYSICAL_MEASUREMENT** · Depends on: 12

Pieces (each instance ×1): P048-Main (M037), P049-Cap (M038), P049-Strip (M039)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F24 | Backglass top-retainer M6-family fastener | 2 | PURCHASE_BEFORE_CNC |
| I08 | Top-retainer captive metal thread | 2 | PURCHASE_BEFORE_CNC |
| G08 | Backglass side U-liners | 2 | PURCHASE_BEFORE_CNC |
| G09 | Backglass lower and top pads | 2 | PURCHASE_BEFORE_CNC |
| G10 | User-supplied backbox tempered glass | 1 | PURCHASE_BEFORE_CNC |

### 13.1 — Fit liners and removable top retainer

Assemble the actual top-retainer cap and reduced strip. Fit side liners and padded lower support. After supplier confirmation, slide the nominal 3–4 mm tempered glass from top/front and positively secure the retainer.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** GLASS RETENTION CHECK: no bare plywood contact, no loose gravity-only retention. Backbox glass stays installed for normal fold; main playfield glass is different.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=13&step=13.1&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-14"></a>
## 14 — DMD and speaker cassette

**PROVISIONAL_HARDWARE** · Depends on: 09, 12

Pieces (each instance ×1): P068-Main (M050), P069-Main (M051), P070-Main (M051), P071-Main (M052), P072-Main (M053), P073-Main (M054), P074-Main (M054), P075-Ply1 (M055), P075-Ply2 (M055), P076-Ply1 (M055), P076-Ply2 (M055), P077-Ply1 (M055), P077-Ply2 (M055), P078-Ply1 (M055), P078-Ply2 (M055)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F30 | Lower cassette M4 positive attachment | 4 | PURCHASE_BEFORE_CNC |
| I12 | Cassette M4 captive receiver | 4 | PURCHASE_BEFORE_CNC |
| W10 | Cassette M4 load washer | 4 | PURCHASE_BEFORE_ASSEMBLY |
| F31 | Replaceable baffle/bezel and DMD-adapter fixings | TBD — do not guess | PURCHASE_BEFORE_CNC |

### 14.1 — Build and retain the removable cassette

Laminate each fixed cleat from two identical 12 mm layers. Install the frame, replaceable speaker baffles and DMD adapter/bezel. Preserve four positive cassette attachments and the separate monitor carrier.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Confirm front removal, rear wiring access and clear normal lock access. F31 insert/baffle attachment count remains TBD; four cassette bolts do not resolve it.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX INTERIOR](../exports/generated/viewer-v32/index.html?manual=14&step=14.1&state=BACKBOX%20INTERIOR&lang=en)

<a id="stage-15"></a>
## 15 — Matrix mechanical carrier

**PROVISIONAL_HARDWARE** · Depends on: 06

Pieces (each instance ×1): P039-Main (M029), P040-Main (M029), P041-Main (M030)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F34 | M4 ×20 matrix thumb screw | 2 | PURCHASE_BEFORE_CNC |
| I13 | M4 matrix support insert | 2 | PURCHASE_BEFORE_CNC |
| F35 | 4 ×50 countersunk matrix-support screw | 4 | PURCHASE_BEFORE_CNC |
| B12 | Playfield glass side channel | 2 | PURCHASE_BEFORE_CNC |

### 15.1 — Fit wood seats and removable retention

Install the two fixed wood seats, inserts and removable retainer screws. The carrier is mechanical; LED panels and their model-specific fasteners remain future electronics. Follow the saved forward/lift removal path.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Check both seats and removal before playfield service or backbox fold. Do not force the matrix past installed main glass.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: MATRIX REMOVAL](../exports/generated/viewer-v32/index.html?manual=15&step=15.1&state=MATRIX%20REMOVAL&lang=en)

<a id="stage-16"></a>
## 16 — Leg and lockdown interfaces

**WAITING_FOR_PHYSICAL_MEASUREMENT** · Depends on: 02, 03

Pieces (each instance ×1): P029-L1 (M019), P029-L2 (M019), P029-L3 (M020), P029-L4 (M019), P029-L5 (M019), P029-L6 (M021), P029-L7 (M019), P030-L1 (M019), P030-L2 (M019), P030-L3 (M020), P030-L4 (M019), P030-L5 (M019), P030-L6 (M021), P030-L7 (M019), P031-L1 (M019), P031-L2 (M021), P031-L3 (M019), P031-L4 (M019), P031-L5 (M022), P031-L6 (M023), P031-L7 (M019), P032-L1 (M019), P032-L2 (M021), P032-L3 (M019), P032-L4 (M019), P032-L5 (M022), P032-L6 (M023), P032-L7 (M019)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| G11 | User-supplied playfield glass | 1 | PURCHASE_BEFORE_CNC |
| G12 | Playfield glass channel liner/seal | 2 | PURCHASE_BEFORE_ASSEMBLY |
| F36 | Playfield channel/lockdown fixing hardware | sum(selected_side_channel.mounting_holes_used) + selected_lockdown_receiver.mounting_holes_used - included_fasteners | PURCHASE_BEFORE_CNC |
| H18 | Real pinball leg | 4 | PURCHASE_BEFORE_CNC |
| B13 | Metal threaded leg backing plate | 4 | PURCHASE_BEFORE_CNC |
| F37 | Matched pinball leg bolts | 8 | PURCHASE_BEFORE_CNC |
| H19 | Leg leveler and jam-nut assembly | 4 | PURCHASE_BEFORE_CNC |
| F38 | Leg backing plate retention screws | 4 * selected_leg_backing.retention_holes_used - included_retention_screws | PURCHASE_BEFORE_CNC |
| H20 | 600 mm body lockdown bar | 1 | PURCHASE_BEFORE_CNC |
| H21 | WPC-compatible lockdown receiver | 1 | PURCHASE_BEFORE_CNC |
| H22 | Front coin-door/frame/keyed access assembly | 1 | PURCHASE_BEFORE_CNC |
| F39 | Front-door frame fixing set | selected_front_door_frame.mounting_holes_used - included_frame_fasteners | PURCHASE_BEFORE_CNC |
| H23 | Coin mechanism/tray mounting set | 1 | OPTIONAL |
| H24 | Optional pinball button mechanical set | 8 | PURCHASE_BEFORE_CNC |
| F40 | Button bracket mounting fasteners | TBD — do not guess | PURCHASE_BEFORE_CNC |
| H26 | Optional mobility skate set | 1 | OPTIONAL |

### 16.1 — Laminate real leg-block layers

Identify each seven-layer stack bottom L1 to top L7. Front L3/L6 carry bores; rear L2 carries the lower bore and L5/L6 share the upper bore. Preserve the five distinct manufacturing profiles.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** HOLD diagonal drilling until the purchased leg plate/bolt pattern and a clamped drill guide are validated. Historical 58/57.15 mm disagreement is not resolved by this manual.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=16&step=16.1&state=EXPLODED%20DETAILED&lang=en)

### 16.2 — Fit purchased legs and front interfaces

Use matched real pinball legs, bolts, backing plates and levelers. The 600 mm body uses the accepted custom-width lockdown strategy; exact receiver/fastener interfaces remain held. Mobility skates are optional external accessories.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Keep cabinet securely supported until leg/load and attachment qualification is complete. No integrated wheels.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: EXPLODED DETAILED](../exports/generated/viewer-v32/index.html?manual=16&step=16.2&state=EXPLODED%20DETAILED&lang=en)

<a id="stage-17"></a>
## 17 — Mechanical inspection and normal fold

**WAITING_FOR_PHYSICAL_MEASUREMENT** · Depends on: 04, 06, 07, 09, 10, 11, 13, 14, 15, 16

Pieces (each instance ×1): —

| ID | Hardware | Project quantity | Status |
|---|---|---|---|

### 17.1 — Perform the normal fold sequence

Open rear doors; release and park both rear-operated locks; close/latch the rear doors; remove MAIN PLAYFIELD GLASS and MATRIX; fold. Keep the cassette, secured display, DMD/speakers and backbox front glass installed. No routine electronics disconnection.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** BACKBOX FOLD CHECK: geometry supports 0–90° pure rotation around Y1066.8/Z508. Check actual retention, cable slack, surroundings and handling only after physical qualification. Reverse the sequence and positively engage both locks upright.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX FOLD 45°](../exports/generated/viewer-v32/index.html?manual=17&step=17.1&state=BACKBOX%20FOLD%2045%C2%B0&lang=en)

### 17.2 — Separate rare hinge maintenance

Rare WPC hinge service may require lower-cassette removal and playfield lift-out/removal for side-pivot access. This is not the normal fold procedure. Keep all unqualified structural/ergonomic gates visible.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Final inspection is a checkpoint framework, not structural certification or manufacturing authorization.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: BACKBOX FOLD 45°](../exports/generated/viewer-v32/index.html?manual=17&step=17.2&state=BACKBOX%20FOLD%2045%C2%B0&lang=en)

<a id="stage-18"></a>
## 18 — Future electronics overview

**OPTIONAL** · Depends on: 17

Pieces (each instance ×1): P033-Main (M024)

| ID | Hardware | Project quantity | Status |
|---|---|---|---|
| F29 | Display VESA mounting screws and spacers | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F32 | Selected speaker mounting screws | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F33 | Selected DMD mounting hardware | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| E01 | Playfield display | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E02 | Backglass display | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E03 | DMD display | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E04 | Backbox speakers | 2 | PURCHASE_BEFORE_ASSEMBLY |
| E05 | PC open chassis and computer | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E06 | SSF exciter | 4 | PURCHASE_BEFORE_ASSEMBLY |
| E07 | Bass shaker | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E08 | Subwoofer | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E09 | Amplifier | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E10 | Protected power supply | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E11 | USB sound interface | 1 | PURCHASE_BEFORE_ASSEMBLY |
| E12 | Matrix LED panel | 6 | PURCHASE_BEFORE_ASSEMBLY |
| E13 | Button switches/contacts | 6 | PURCHASE_BEFORE_ASSEMBLY |
| E14 | Optional toys/controllers/LED/relays | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| B14 | Protected mains inlet enclosure reference | 1 | PURCHASE_BEFORE_CNC |
| F42 | Subwoofer floor mounting bolts | 8 | PURCHASE_BEFORE_CNC |
| F43 | Bass-shaker carrier floor anchors | 4 | PURCHASE_BEFORE_CNC |
| F44 | Bass-shaker to carrier fasteners | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F45 | Exciter IMS mounting fasteners | TBD — do not guess | PURCHASE_BEFORE_CNC |
| F46 | PC chassis/base and component restraints | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F47 | Electronics board shelf standoffs and screws | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F48 | Matrix panel mounting fasteners | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F49 | Toy mounting board fasteners | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| F50 | Mains/network flange and enclosure fasteners | TBD — do not guess | PURCHASE_BEFORE_CNC |
| B15 | Playfield replaceable VESA attachment | 1 | PURCHASE_BEFORE_CNC |
| F51 | Playfield display-to-adapter fasteners | TBD — do not guess | PURCHASE_BEFORE_ASSEMBLY |
| H25 | Optional removable toy shelf | 1 | OPTIONAL |
| R01 | Cable / connector routing reserves | 0 | PURCHASE_BEFORE_ASSEMBLY |
| R02 | Button service approach reserves | 0 | PURCHASE_BEFORE_ASSEMBLY |
| R03 | Future toy mounting volumes | 0 | PURCHASE_BEFORE_ASSEMBLY |
| R04 | Unpopulated equipment/payload/plunger reserves | 0 | PURCHASE_BEFORE_ASSEMBLY |

### 18.1 — Use reserved zones and replaceable adapters

Add displays, PC, DMD, speakers, SSF, controllers or toys later using the reserved envelopes and replaceable mounting boards. Preserve both side toy zones and generic cable passage. No mandatory toy shelf or connector family.

**Orientation:** X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
**Faces:** FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
**Tools:** Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.

**Checkpoint:** Keep electronics separate from the mandatory mechanical kit. Heavy devices need positive retention; power/electrical design is outside this manual framework.

**HOLD:** Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

[Next-state CAD: INTERIOR INSPECTION](../exports/generated/viewer-v32/index.html?manual=18&step=18.1&state=INTERIOR%20INSPECTION&lang=en)

## Per-piece preparation and orientation cards

**FACE A → +z into stock; FACE B has NO CNC. All depths below are measured from finished FACE A. Directions are installed global vectors, not drilling templates.**

### P001-Main / M001

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P001-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 2 CUT; 2 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P001-Main-R6: POCKET · FACE A · [9.270362255620057e-15, 3.000000000000012] mm
- P001-Main-R8: POCKET · FACE A · [9.270362255620057e-15, 3.000000000000012] mm
- P001-Main-R7: CUT · FACE A · [3.0000000000000098, 18.0] mm
- P001-Main-R9: CUT · FACE A · [3.0000000000000098, 18.0] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R2 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R3 · FACE A datum [0, 12.99999999999999] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R4 · FACE A datum [0, 12.99999999999999] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R5 · FACE A datum [0, 12.99999999999999] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R10 · FACE A datum [0, 12.99999999999999] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R11 · FACE A datum [0, 12.999999999999996] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R12 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R13 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R14 · FACE A datum [0, 0.9999999999999931] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R15 · FACE A datum [0, 12.999999999999996] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R16 · FACE A datum [6.938893903907228e-15, 1.0000000000000073] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P001-Main-R17 · FACE A datum [2.1149748619109232e-14, 1.0000000000000215] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P001-Main&lang=en)

### P002-Main / M002

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P002-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 2 CUT; 2 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P002-Main-R3: POCKET · FACE A · [0, 3.0000000000000013] mm
- P002-Main-R5: POCKET · FACE A · [0, 3.0000000000000013] mm
- P002-Main-R4: CUT · FACE A · [2.999999999999999, 18.0] mm
- P002-Main-R6: CUT · FACE A · [2.999999999999999, 18.0] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R2 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R7 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R8 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R9 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R10 · FACE A datum [0, 1.0000000000000002] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R11 · FACE A datum [0, 1.0000000000000002] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R12 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R13 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R14 · FACE A datum [0, 13.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R15 · FACE A datum [0, 1.0000000000000002] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R16 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P002-Main-R17 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P002-Main&lang=en)

### P003-Main / M003

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P003-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 1.0, 0.0]

CNC PROVIDED: outer contour; 11 CUT; 0 POCKET; face reduction -3.552713678800501e-15 mm.
Fit/coupon HOLD: True

- P003-Main-R5: CUT · FACE A · [5.695444116327053e-15, 18.000000000000004] mm
- P003-Main-R6: CUT · FACE A · [0, 17.999999999999993] mm
- P003-Main-R7: CUT · FACE A · [5.695444116327053e-15, 18.000000000000004] mm
- P003-Main-R8: CUT · FACE A · [9.248157795127554e-15, 18.000000000000004] mm
- P003-Main-R9: CUT · FACE A · [6.708869570992704e-15, 18.000000000000004] mm
- P003-Main-R10: CUT · FACE A · [1.6353585152728557e-14, 18.000000000000004] mm
- P003-Main-R11: CUT · FACE A · [2.0919724286194707e-14, 18.000000000000004] mm
- P003-Main-R12: CUT · FACE A · [0, 18.000000000000004] mm
- P003-Main-R13: CUT · FACE A · [6.708869570992704e-15, 18.000000000000004] mm
- P003-Main-R14: CUT · FACE A · [2.0919724286194707e-14, 18.000000000000004] mm
- P003-Main-R15: CUT · FACE A · [2.0919724286194707e-14, 18.000000000000004] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P003-Main-R1 · FACE A datum [0, 7.778182980084499] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P003-Main-R2 · FACE A datum [0, 7.778182980084506] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P003-Main-R3 · FACE A datum [0, 7.778174593052076] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P003-Main-R4 · FACE A datum [0, 7.778174593052083] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P003-Main-R12 · FACE A datum 18.000000000000004 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P003-Main&lang=en)

### P004-Main / M004

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P004-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 15 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P004-Main-R19: POCKET · FACE A · [0, 7.999999999999943] mm
- P004-Main-R5: CUT · FACE A · [0, 18.0] mm
- P004-Main-R6: CUT · FACE A · [0, 18.0] mm
- P004-Main-R7: CUT · FACE A · [0, 18.0] mm
- P004-Main-R8: CUT · FACE A · [0, 18.0] mm
- P004-Main-R9: CUT · FACE A · [0, 18.0] mm
- P004-Main-R10: CUT · FACE A · [0, 18.0] mm
- P004-Main-R11: CUT · FACE A · [0, 18.0] mm
- P004-Main-R12: CUT · FACE A · [0, 18.0] mm
- P004-Main-R13: CUT · FACE A · [0, 18.0] mm
- P004-Main-R14: CUT · FACE A · [0, 18.0] mm
- P004-Main-R15: CUT · FACE A · [0, 18.0] mm
- P004-Main-R16: CUT · FACE A · [0, 18.0] mm
- P004-Main-R17: CUT · FACE A · [0, 18.0] mm
- P004-Main-R21: CUT · FACE A · [0, 18.0] mm
- P004-Main-R22: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R1 · FACE A datum [0, 7.7781745930520225] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R2 · FACE A datum [0, 7.7781745930520225] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R3 · FACE A datum [0, 7.778182980084677] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R4 · FACE A datum [0, 7.778182980084677] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R18 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P004-Main-R19 · FACE A datum 7.999999999999943 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: finish the narrow feature with qualified hand tools · P004-Main-R19 · FACE A datum 7.999999999999943 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R20 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P004-Main-R22 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R23 · FACE A datum [6.0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P004-Main-R24 · FACE A datum [6.0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P004-Main&lang=en)

### P005-Main / M005

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P005-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, -1.0]

CNC PROVIDED: outer contour; 27 CUT; 8 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P005-Main-R5: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R10: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R19: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R22: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R24: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R28: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R30: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R34: POCKET · FACE A · [0, 8.0] mm
- P005-Main-R1: CUT · FACE A · [0, 18.0] mm
- P005-Main-R2: CUT · FACE A · [0, 18.0] mm
- P005-Main-R3: CUT · FACE A · [0, 18.0] mm
- P005-Main-R4: CUT · FACE A · [0, 18.0] mm
- P005-Main-R6: CUT · FACE A · [0, 18.0] mm
- P005-Main-R7: CUT · FACE A · [0, 18.0] mm
- P005-Main-R8: CUT · FACE A · [0, 18.0] mm
- P005-Main-R9: CUT · FACE A · [0, 18.0] mm
- P005-Main-R11: CUT · FACE A · [0, 18.0] mm
- P005-Main-R12: CUT · FACE A · [0, 18.0] mm
- P005-Main-R13: CUT · FACE A · [0, 18.0] mm
- P005-Main-R14: CUT · FACE A · [0, 18.0] mm
- P005-Main-R15: CUT · FACE A · [0, 18.0] mm
- P005-Main-R16: CUT · FACE A · [0, 18.0] mm
- P005-Main-R17: CUT · FACE A · [0, 18.0] mm
- P005-Main-R18: CUT · FACE A · [0, 18.0] mm
- P005-Main-R20: CUT · FACE A · [0, 18.0] mm
- P005-Main-R21: CUT · FACE A · [0, 18.0] mm
- P005-Main-R23: CUT · FACE A · [0, 18.0] mm
- P005-Main-R25: CUT · FACE A · [0, 18.0] mm
- P005-Main-R26: CUT · FACE A · [0, 18.0] mm
- P005-Main-R27: CUT · FACE A · [0, 18.0] mm
- P005-Main-R29: CUT · FACE A · [0, 18.0] mm
- P005-Main-R31: CUT · FACE A · [0, 18.0] mm
- P005-Main-R32: CUT · FACE A · [0, 18.0] mm
- P005-Main-R33: CUT · FACE A · [0, 18.0] mm
- P005-Main-R35: CUT · FACE A · [0, 18.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P005-Main&lang=en)

### P006-Main / M006

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P006-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P006-Main&lang=en)

### P007-Main / M006

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P007-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P007-Main&lang=en)

### P008-Main / M007

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P008-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 12 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 3 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P008-Main-R1: CUT · FACE A · [0, 12.0] mm
- P008-Main-R2: CUT · FACE A · [0, 12.0] mm
- P008-Main-R3: CUT · FACE A · [0, 12.0] mm
- BUILDER FINISH: file/chisel the cutter-inaccessible residual to reference · P008-Main-R3 · FACE A datum 12.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P008-Main&lang=en)

### P009-Main / M008

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P009-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P009-Main-R1: CUT · FACE A · [0, 11.999999999999972] mm
- P009-Main-R2: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
- P009-Main-R3: CUT · FACE A · [0, 11.999999999999972] mm
- P009-Main-R4: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P009-Main&lang=en)

### P010-Main / M008

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P010-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P010-Main-R1: CUT · FACE A · [0, 11.999999999999972] mm
- P010-Main-R2: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
- P010-Main-R3: CUT · FACE A · [0, 11.999999999999972] mm
- P010-Main-R4: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P010-Main&lang=en)

### P011-Main / M009

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P011-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P011-Main-R1: CUT · FACE A · [0, 11.999999999999972] mm
- P011-Main-R2: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
- P011-Main-R3: CUT · FACE A · [0, 11.999999999999972] mm
- P011-Main-R4: CUT · FACE A · [2.8084931560638486e-14, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P011-Main&lang=en)

### P012-Main / M010

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P012-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P012-Main-R3: POCKET · FACE A · [0, 10.5] mm
- P012-Main-R4: POCKET · FACE A · [10.5, 12.5] mm
- P012-Main-R5: POCKET · FACE A · [0, 10.5] mm
- P012-Main-R6: POCKET · FACE A · [10.5, 12.5] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P012-Main-R1 · FACE A datum [6.749999999999995, 11.25] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P012-Main-R2 · FACE A datum [6.749999999999995, 11.25] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P012-Main&lang=en)

### P013-Main / M011

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P013-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P013-Main-R3: POCKET · FACE A · [0, 10.5] mm
- P013-Main-R4: POCKET · FACE A · [10.5, 12.5] mm
- P013-Main-R5: POCKET · FACE A · [0, 10.5] mm
- P013-Main-R6: POCKET · FACE A · [10.5, 12.5] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P013-Main-R1 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P013-Main-R2 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P013-Main&lang=en)

### P014-Main / M010

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P014-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction -2.842170943040401e-14 mm.
Fit/coupon HOLD: True

- P014-Main-R3: POCKET · FACE A · [2.7901234540766383e-14, 10.500000000000028] mm
- P014-Main-R4: POCKET · FACE A · [10.500000000000028, 12.500000000000028] mm
- P014-Main-R5: POCKET · FACE A · [2.7901234540766383e-14, 10.500000000000028] mm
- P014-Main-R6: POCKET · FACE A · [10.500000000000028, 12.500000000000028] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P014-Main-R1 · FACE A datum [6.750000000000023, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P014-Main-R2 · FACE A datum [6.750000000000023, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P014-Main&lang=en)

### P015-Main / M011

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P015-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P015-Main-R3: POCKET · FACE A · [0, 10.5] mm
- P015-Main-R4: POCKET · FACE A · [10.5, 12.5] mm
- P015-Main-R5: POCKET · FACE A · [0, 10.5] mm
- P015-Main-R6: POCKET · FACE A · [10.5, 12.5] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P015-Main-R1 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P015-Main-R2 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P015-Main&lang=en)

### P016-Main / M012

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P016-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P016-Main-R3: POCKET · FACE A · [0, 10.5] mm
- P016-Main-R4: POCKET · FACE A · [10.5, 12.5] mm
- P016-Main-R5: POCKET · FACE A · [0, 10.5] mm
- P016-Main-R6: POCKET · FACE A · [10.5, 12.5] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P016-Main-R1 · FACE A datum [6.749999999999995, 11.25] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P016-Main-R2 · FACE A datum [6.749999999999995, 11.25] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P016-Main&lang=en)

### P017-Main / M013

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P017-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 4 POCKET; face reduction 2.842170943040401e-14 mm.
Fit/coupon HOLD: True

- P017-Main-R3: POCKET · FACE A · [0, 10.5] mm
- P017-Main-R4: POCKET · FACE A · [10.5, 12.5] mm
- P017-Main-R5: POCKET · FACE A · [0, 10.5] mm
- P017-Main-R6: POCKET · FACE A · [10.5, 12.5] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P017-Main-R1 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P017-Main-R2 · FACE A datum [6.75, 11.250000000000028] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P017-Main&lang=en)

### P018-Main / M014

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P018-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 16 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P018-Main-R1-STEP2: POCKET · FACE A · see register mm
- P018-Main-R1-STEP3: POCKET · FACE A · see register mm
- P018-Main-R1-STEP4: POCKET · FACE A · see register mm
- P018-Main-R1-STEP5: POCKET · FACE A · see register mm
- P018-Main-R1-STEP6: POCKET · FACE A · see register mm
- P018-Main-R1-STEP7: POCKET · FACE A · see register mm
- P018-Main-R1-STEP8: POCKET · FACE A · see register mm
- P018-Main-R1-STEP9: POCKET · FACE A · see register mm
- P018-Main-R1-STEP10: POCKET · FACE A · see register mm
- P018-Main-R1-STEP11: POCKET · FACE A · see register mm
- P018-Main-R1-STEP12: POCKET · FACE A · see register mm
- P018-Main-R1-STEP13: POCKET · FACE A · see register mm
- P018-Main-R1-STEP14: POCKET · FACE A · see register mm
- P018-Main-R1-STEP15: POCKET · FACE A · see register mm
- P018-Main-R1-STEP16: POCKET · FACE A · see register mm
- P018-Main-R1-STEP17: POCKET · FACE A · see register mm
- BUILDER FINISH: sand to reference bevel with straightedge and angle template · P018-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P018-Main&lang=en)

### P019-Main / M014

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P019-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 16 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P019-Main-R1-STEP2: POCKET · FACE A · see register mm
- P019-Main-R1-STEP3: POCKET · FACE A · see register mm
- P019-Main-R1-STEP4: POCKET · FACE A · see register mm
- P019-Main-R1-STEP5: POCKET · FACE A · see register mm
- P019-Main-R1-STEP6: POCKET · FACE A · see register mm
- P019-Main-R1-STEP7: POCKET · FACE A · see register mm
- P019-Main-R1-STEP8: POCKET · FACE A · see register mm
- P019-Main-R1-STEP9: POCKET · FACE A · see register mm
- P019-Main-R1-STEP10: POCKET · FACE A · see register mm
- P019-Main-R1-STEP11: POCKET · FACE A · see register mm
- P019-Main-R1-STEP12: POCKET · FACE A · see register mm
- P019-Main-R1-STEP13: POCKET · FACE A · see register mm
- P019-Main-R1-STEP14: POCKET · FACE A · see register mm
- P019-Main-R1-STEP15: POCKET · FACE A · see register mm
- P019-Main-R1-STEP16: POCKET · FACE A · see register mm
- P019-Main-R1-STEP17: POCKET · FACE A · see register mm
- BUILDER FINISH: sand to reference bevel with straightedge and angle template · P019-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P019-Main&lang=en)

### P020-Main / M014

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P020-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 16 POCKET; face reduction -1.1368683772161603e-13 mm.
Fit/coupon HOLD: True

- P020-Main-R1-STEP2: POCKET · FACE A · see register mm
- P020-Main-R1-STEP3: POCKET · FACE A · see register mm
- P020-Main-R1-STEP4: POCKET · FACE A · see register mm
- P020-Main-R1-STEP5: POCKET · FACE A · see register mm
- P020-Main-R1-STEP6: POCKET · FACE A · see register mm
- P020-Main-R1-STEP7: POCKET · FACE A · see register mm
- P020-Main-R1-STEP8: POCKET · FACE A · see register mm
- P020-Main-R1-STEP9: POCKET · FACE A · see register mm
- P020-Main-R1-STEP10: POCKET · FACE A · see register mm
- P020-Main-R1-STEP11: POCKET · FACE A · see register mm
- P020-Main-R1-STEP12: POCKET · FACE A · see register mm
- P020-Main-R1-STEP13: POCKET · FACE A · see register mm
- P020-Main-R1-STEP14: POCKET · FACE A · see register mm
- P020-Main-R1-STEP15: POCKET · FACE A · see register mm
- P020-Main-R1-STEP16: POCKET · FACE A · see register mm
- P020-Main-R1-STEP17: POCKET · FACE A · see register mm
- BUILDER FINISH: sand to reference bevel with straightedge and angle template · P020-Main-R1 · FACE A datum [0, 18.000000000000114] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P020-Main&lang=en)

### P021-Main / M015

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P021-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P021-Main-R1: POCKET · FACE A · [0, 6.000000000000007] mm
- P021-Main-R2: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R3: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R4: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R5: CUT · FACE A · [0, 17.999999999999996] mm
- P021-Main-R6: CUT · FACE A · [3.247402347028583e-15, 18.0] mm
- P021-Main-R7: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R8: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R9: CUT · FACE A · [0, 17.999999999999993] mm
- P021-Main-R10: CUT · FACE A · [0, 17.999999999999996] mm
- P021-Main-R11: CUT · FACE A · [3.247402347028583e-15, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P021-Main-R1 · FACE A datum 6.000000000000007 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P021-Main&lang=en)

### P022-Main / M016

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P022-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P022-Main-R1: POCKET · FACE A · [0, 6.000000000000014] mm
- P022-Main-R2: CUT · FACE A · [0, 18.0] mm
- P022-Main-R3: CUT · FACE A · [0, 18.0] mm
- P022-Main-R4: CUT · FACE A · [0, 18.0] mm
- P022-Main-R5: CUT · FACE A · [0, 18.0] mm
- P022-Main-R6: CUT · FACE A · [0, 18.0] mm
- P022-Main-R7: CUT · FACE A · [0, 18.0] mm
- P022-Main-R8: CUT · FACE A · [0, 18.0] mm
- P022-Main-R9: CUT · FACE A · [0, 18.0] mm
- P022-Main-R10: CUT · FACE A · [0, 18.0] mm
- P022-Main-R11: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P022-Main-R1 · FACE A datum 6.000000000000014 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P022-Main&lang=en)

### P023-Main / M015

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P023-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P023-Main-R1: POCKET · FACE A · [0, 6.000000000000007] mm
- P023-Main-R2: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R3: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R4: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R5: CUT · FACE A · [0, 17.999999999999996] mm
- P023-Main-R6: CUT · FACE A · [0, 18.0] mm
- P023-Main-R7: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R8: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R9: CUT · FACE A · [0, 17.999999999999993] mm
- P023-Main-R10: CUT · FACE A · [0, 17.999999999999996] mm
- P023-Main-R11: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P023-Main-R1 · FACE A datum 6.000000000000007 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P023-Main&lang=en)

### P024-Main / M016

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P024-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P024-Main-R1: POCKET · FACE A · [0, 6.000000000000014] mm
- P024-Main-R2: CUT · FACE A · [0, 18.0] mm
- P024-Main-R3: CUT · FACE A · [0, 18.0] mm
- P024-Main-R4: CUT · FACE A · [0, 18.0] mm
- P024-Main-R5: CUT · FACE A · [0, 18.0] mm
- P024-Main-R6: CUT · FACE A · [0, 18.0] mm
- P024-Main-R7: CUT · FACE A · [0, 18.0] mm
- P024-Main-R8: CUT · FACE A · [0, 18.0] mm
- P024-Main-R9: CUT · FACE A · [0, 18.0] mm
- P024-Main-R10: CUT · FACE A · [0, 18.0] mm
- P024-Main-R11: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P024-Main-R1 · FACE A datum 6.000000000000014 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P024-Main&lang=en)

### P025-Main / M015

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P025-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction -3.552713678800501e-15 mm.
Fit/coupon HOLD: True

- P025-Main-R1: POCKET · FACE A · [0, 6.000000000000011] mm
- P025-Main-R2: CUT · FACE A · [0, 17.999999999999996] mm
- P025-Main-R3: CUT · FACE A · [0, 17.999999999999996] mm
- P025-Main-R4: CUT · FACE A · [0, 18.0] mm
- P025-Main-R5: CUT · FACE A · [0, 18.000000000000004] mm
- P025-Main-R6: CUT · FACE A · [6.800116025829084e-15, 18.000000000000004] mm
- P025-Main-R7: CUT · FACE A · [0, 17.999999999999996] mm
- P025-Main-R8: CUT · FACE A · [0, 17.999999999999996] mm
- P025-Main-R9: CUT · FACE A · [0, 18.0] mm
- P025-Main-R10: CUT · FACE A · [0, 18.000000000000004] mm
- P025-Main-R11: CUT · FACE A · [6.800116025829084e-15, 18.000000000000004] mm
- BUILDER FINISH: file/chisel corner to reference · P025-Main-R1 · FACE A datum 6.000000000000011 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P025-Main&lang=en)

### P026-Main / M016

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P026-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 10 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P026-Main-R1: POCKET · FACE A · [0, 6.000000000000014] mm
- P026-Main-R2: CUT · FACE A · [0, 18.0] mm
- P026-Main-R3: CUT · FACE A · [0, 18.0] mm
- P026-Main-R4: CUT · FACE A · [0, 18.0] mm
- P026-Main-R5: CUT · FACE A · [0, 18.0] mm
- P026-Main-R6: CUT · FACE A · [0, 18.0] mm
- P026-Main-R7: CUT · FACE A · [0, 18.0] mm
- P026-Main-R8: CUT · FACE A · [0, 18.0] mm
- P026-Main-R9: CUT · FACE A · [0, 18.0] mm
- P026-Main-R10: CUT · FACE A · [0, 18.0] mm
- P026-Main-R11: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P026-Main-R1 · FACE A datum 6.000000000000014 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P026-Main&lang=en)

### P027-Main / M017

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P027-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P027-Main-R1 · FACE A datum [0, 17.999999999999986] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P027-Main-R2 · FACE A datum [1.312382593579958e-14, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P027-Main-R3 · FACE A datum [0, 17.999999999999986] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P027-Main-R4 · FACE A datum [1.312382593579958e-14, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P027-Main&lang=en)

### P028-Main / M018

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P028-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 3 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P028-Main-R1: CUT · FACE A · [0, 18.0] mm
- P028-Main-R2: CUT · FACE A · [0, 18.0] mm
- P028-Main-R3: CUT · FACE A · [1.1295204964212762e-13, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P028-Main-R1 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P028-Main-R4 · FACE A datum [6.0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P028-Main-R5 · FACE A datum [6.0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P028-Main-R6 · FACE A datum [6.000000000000114, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P028-Main-R7 · FACE A datum [6.000000000000114, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P028-Main&lang=en)

### P029-L1 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L1.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L1&lang=en)

### P029-L2 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L2.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L2&lang=en)

### P029-L3 / M020

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L3.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P029-L3-R1 · FACE A datum [6.5, 17.500000000000007] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L3&lang=en)

### P029-L4 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L4.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L4&lang=en)

### P029-L5 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L5.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L5&lang=en)

### P029-L6 / M021

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L6.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P029-L6-R1 · FACE A datum [2.5, 13.500000000000007] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L6&lang=en)

### P029-L7 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P029-L7.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -2.842170943040401e-14 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P029-L7&lang=en)

### P030-L1 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L1.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 7.105427357601002e-15 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L1&lang=en)

### P030-L2 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L2.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L2&lang=en)

### P030-L3 / M020

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L3.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P030-L3-R1 · FACE A datum [6.499999999994714, 17.500000000005286] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L3&lang=en)

### P030-L4 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L4.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L4&lang=en)

### P030-L5 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L5.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -1.4210854715202004e-14 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L5&lang=en)

### P030-L6 / M021

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L6.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P030-L6-R1 · FACE A datum [2.499999999994742, 13.500000000005315] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L6&lang=en)

### P030-L7 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P030-L7.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P030-L7&lang=en)

### P031-L1 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L1.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 7.105427357601002e-15 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L1&lang=en)

### P031-L2 / M021

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L2.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -7.105427357601002e-15 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P031-L2-R1 · FACE A datum [2.5, 13.500000000000007] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L2&lang=en)

### P031-L3 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L3.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L3&lang=en)

### P031-L4 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L4.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L4&lang=en)

### P031-L5 / M022

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L5.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P031-L5-R1 · FACE A datum [0, 9.500000000000007] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L5&lang=en)

### P031-L6 / M023

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L6.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -1.4210854715202004e-14 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P031-L6-R1 · FACE A datum [16.5, 18.000000000000014] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L6&lang=en)

### P031-L7 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P031-L7.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P031-L7&lang=en)

### P032-L1 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L1.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 7.105427357601002e-15 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L1&lang=en)

### P032-L2 / M021

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L2.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P032-L2-R1 · FACE A datum [2.499999999999994, 13.5] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L2&lang=en)

### P032-L3 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L3.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L3&lang=en)

### P032-L4 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L4.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L4&lang=en)

### P032-L5 / M022

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L5.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P032-L5-R1 · FACE A datum [0, 9.5] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L5&lang=en)

### P032-L6 / M023

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L6.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -2.842170943040401e-14 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P032-L6-R1 · FACE A datum [16.500000000000007, 18.00000000000003] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L6&lang=en)

### P032-L7 / M019

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P032-L7.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P032-L7&lang=en)

### P033-Main / M024

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P033-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P033-Main-R1: CUT · FACE A · [0, 11.999999999999993] mm
- P033-Main-R2: CUT · FACE A · [1.0321363166635981e-14, 12.0] mm
- P033-Main-R3: CUT · FACE A · [0, 11.999999999999993] mm
- P033-Main-R4: CUT · FACE A · [1.0321363166635981e-14, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P033-Main&lang=en)

### P034-Main / M025

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P034-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, 0.172043766268355, -0.9850893068591292]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P034-Main&lang=en)

### P035-Main / M026

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P035-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P035-Main-R1 · FACE A datum [1.326716514427062e-14, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P035-Main-R2 · FACE A datum [0, 17.999999999999993] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P035-Main-R3 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P035-Main&lang=en)

### P036-Main / M027

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P036-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P036-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P036-Main-R2 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P036-Main-R3 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P036-Main&lang=en)

### P037-Main / M028

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P037-Main.svg)

**ONE_SIDE_CNC_READY** · 8 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 9 CUT; 0 POCKET; face reduction 3.552713678800501e-15 mm.
Fit/coupon HOLD: True

- P037-Main-R1: CUT · FACE A · [0, 7.999999999999989] mm
- P037-Main-R2: CUT · FACE A · [0, 7.999999999999992] mm
- P037-Main-R3: CUT · FACE A · [5.053524988392597e-15, 7.9999999999999964] mm
- P037-Main-R4: CUT · FACE A · [2.8179255993120893e-15, 7.9999999999999964] mm
- P037-Main-R5: CUT · FACE A · [0, 7.999999999999992] mm
- P037-Main-R6: CUT · FACE A · [0, 7.999999999999989] mm
- P037-Main-R7: CUT · FACE A · [0, 7.9999999999999964] mm
- P037-Main-R8: CUT · FACE A · [2.8179255993120893e-15, 7.9999999999999964] mm
- P037-Main-R9: CUT · FACE A · [5.053524988392597e-15, 7.9999999999999964] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P037-Main&lang=en)

### P038-Main / M028

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P038-Main.svg)

**ONE_SIDE_CNC_READY** · 8 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 9 CUT; 0 POCKET; face reduction -1.7763568394002505e-15 mm.
Fit/coupon HOLD: True

- P038-Main-R1: CUT · FACE A · [0, 7.999999999999993] mm
- P038-Main-R2: CUT · FACE A · [0, 7.999999999999996] mm
- P038-Main-R3: CUT · FACE A · [1.0382595506593349e-14, 8.000000000000002] mm
- P038-Main-R4: CUT · FACE A · [6.37063927811259e-15, 8.000000000000002] mm
- P038-Main-R5: CUT · FACE A · [0, 7.999999999999996] mm
- P038-Main-R6: CUT · FACE A · [0, 7.999999999999993] mm
- P038-Main-R7: CUT · FACE A · [0, 8.000000000000002] mm
- P038-Main-R8: CUT · FACE A · [6.37063927811259e-15, 8.000000000000002] mm
- P038-Main-R9: CUT · FACE A · [1.0382595506593349e-14, 8.000000000000002] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P038-Main&lang=en)

### P039-Main / M029

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P039-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, -0.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 1.4210854715202004e-14 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 17.999999999999986 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P039-Main-R1 · FACE A datum [4.999999999999979, 12.999999999999979] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P039-Main-R2 · FACE A datum [4.999999999999979, 12.999999999999979] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P039-Main-R3 · FACE A datum [5.949999999999986, 12.049999999999986] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P039-Main&lang=en)

### P040-Main / M029

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P040-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, -0.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 1.1368683772161603e-13 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 17.999999999999886 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P040-Main-R1 · FACE A datum [4.999999999999886, 12.999999999999886] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P040-Main-R2 · FACE A datum [4.999999999999886, 12.999999999999886] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P040-Main-R3 · FACE A datum [5.9499999999998865, 12.049999999999887] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P040-Main&lang=en)

### P041-Main / M030

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P041-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 12 mm · FACE A [0.0, -0.42261826174069905, 0.9063077870366502]

CNC PROVIDED: outer contour; 2 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P041-Main-R3: CUT · FACE A · [4.3576253716537394e-15, 11.99999999999996] mm
- P041-Main-R4: CUT · FACE A · [4.3576253716537394e-15, 11.99999999999996] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P041-Main-R1 · FACE A datum [9.499999999999943, 12.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P041-Main-R2 · FACE A datum [9.499999999999943, 12.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P041-Main&lang=en)

### P042-Main / M031

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P042-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 2 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P042-Main-R1: POCKET · FACE A · [1.4210854715202004e-14, 6.000000000000066] mm
- P042-Main-R2: POCKET · FACE A · [0, 5.999999999999988] mm
- BUILDER FINISH: file/chisel corner to reference · P042-Main-R1 · FACE A datum 6.000000000000066 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P042-Main-R2 · FACE A datum 5.999999999999988 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P042-Main&lang=en)

### P043-Main / M032

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P043-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 2 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P043-Main-R1: POCKET · FACE A · [0, 6.000000000000002] mm
- P043-Main-R2: POCKET · FACE A · [0, 6.000000000000057] mm
- BUILDER FINISH: file/chisel corner to reference · P043-Main-R1 · FACE A datum 6.000000000000002 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P043-Main-R2 · FACE A datum 6.000000000000057 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P043-Main&lang=en)

### P044-Main / M033

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P044-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 3 CUT; 2 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P044-Main-R3: POCKET · FACE A · [0, 3.0000000000000004] mm
- P044-Main-R5: POCKET · FACE A · [0, 3.0000000000000004] mm
- P044-Main-R1: CUT · FACE A · [0, 18.0] mm
- P044-Main-R2: CUT · FACE A · [0, 18.0] mm
- P044-Main-R4: CUT · FACE A · [1.1313574666199972e-13, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P044-Main-R1 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P044-Main&lang=en)

### P045-Main / M034

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P045-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P045-Main&lang=en)

### P046-Main / M035

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P046-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 1 CUT; 1 POCKET; face reduction -2.2737367544323206e-13 mm.
Fit/coupon HOLD: True

- P046-Main-R1: POCKET · FACE A · [0, 12.000000000000227] mm
- P046-Main-R2: CUT · FACE A · [0, 18.000000000000227] mm
- BUILDER FINISH: file/chisel corner to reference · P046-Main-R1 · FACE A datum 12.000000000000227 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P046-Main-R2 · FACE A datum 18.000000000000227 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P046-Main&lang=en)

### P047-Main / M036

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P047-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P047-Main&lang=en)

### P048-Main / M037

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P048-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P048-Main-R1: POCKET · FACE A · [0, 2.0000000000001137] mm
- BUILDER FINISH: file/chisel corner to reference · P048-Main-R1 · FACE A datum 2.0000000000001137 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P048-Main&lang=en)

### P049-Cap / M038

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P049-Cap.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 2 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P049-Cap-R1: CUT · FACE A · [0, 12.0] mm
- P049-Cap-R2: CUT · FACE A · [0, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P049-Cap&lang=en)

### P049-Strip / M039

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P049-Strip.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 1 POCKET; face reduction 4.2000000000000455 mm.
Fit/coupon HOLD: True

- P049-Strip-FACE_REDUCTION: POCKET · FACE A · see register mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P049-Strip&lang=en)

### P050-Main / M040

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P050-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P050-Main-R1 · FACE A datum [5.75, 12.250000000000005] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P050-Main-R2 · FACE A datum [5.75, 12.250000000000005] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P050-Main&lang=en)

### P051-Main / M041

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P051-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P051-Main&lang=en)

### P052-Main / M041

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P052-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P052-Main&lang=en)

### P053-Main / M040

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P053-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P053-Main-R1 · FACE A datum [5.75, 12.250000000000005] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P053-Main-R2 · FACE A datum [5.75, 12.250000000000005] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P053-Main&lang=en)

### P054-Main / M041

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P054-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 7.105427357601002e-15 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P054-Main&lang=en)

### P055-Main / M041

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P055-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P055-Main&lang=en)

### P056-Main / M042

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P056-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 2 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P056-Main-R1: CUT · FACE A · [0, 18.0] mm
- P056-Main-R2: CUT · FACE A · [1.4377388168895777e-14, 18.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P056-Main&lang=en)

### P057-Main / M043

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P057-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 2 CUT; 1 POCKET; face reduction 1.1368683772161603e-13 mm.
Fit/coupon HOLD: True

- P057-Main-R1: POCKET · FACE A · [0, 6.0] mm
- P057-Main-R2: CUT · FACE A · [5.999999999999886, 17.999999999999886] mm
- P057-Main-R3: CUT · FACE A · [0, 17.999999999999886] mm
- BUILDER FINISH: file/chisel corner to reference · P057-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P057-Main&lang=en)

### P058-Main / M043

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P058-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, -1.0]

CNC PROVIDED: outer contour; 2 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P058-Main-R1: POCKET · FACE A · [0, 6.0] mm
- P058-Main-R2: CUT · FACE A · [6.0, 18.0] mm
- P058-Main-R3: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P058-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P058-Main&lang=en)

### P059-Main / M042

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P059-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 2 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P059-Main-R1: CUT · FACE A · [0, 18.0] mm
- P059-Main-R2: CUT · FACE A · [1.4377388168895777e-14, 18.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P059-Main&lang=en)

### P060-Main / M043

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P060-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 2 CUT; 1 POCKET; face reduction 1.1368683772161603e-13 mm.
Fit/coupon HOLD: True

- P060-Main-R1: POCKET · FACE A · [0, 6.0] mm
- P060-Main-R2: CUT · FACE A · [5.999999999999886, 17.999999999999886] mm
- P060-Main-R3: CUT · FACE A · [0, 17.999999999999886] mm
- BUILDER FINISH: file/chisel corner to reference · P060-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P060-Main&lang=en)

### P061-Main / M043

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P061-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, -1.0]

CNC PROVIDED: outer contour; 2 CUT; 1 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P061-Main-R1: POCKET · FACE A · [0, 6.0] mm
- P061-Main-R2: CUT · FACE A · [6.0, 18.0] mm
- P061-Main-R3: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P061-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P061-Main&lang=en)

### P062-Main / M044

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P062-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P062-Main-R1: CUT · FACE A · [0, 12.0] mm
- P062-Main-R2: CUT · FACE A · [0, 12.0] mm
- P062-Main-R3: CUT · FACE A · [0, 12.0] mm
- P062-Main-R4: CUT · FACE A · [0, 12.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P062-Main&lang=en)

### P063-Main / M045

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P063-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 6 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P063-Main-R1: CUT · FACE A · [0, 6.0] mm
- BUILDER FINISH: file/chisel corner to reference · P063-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P063-Main&lang=en)

### P064-Base18 / M046

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P064-Base18.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P064-Base18&lang=en)

### P064-Cap12 / M047

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P064-Cap12.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P064-Cap12&lang=en)

### P065-Base18 / M048

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P065-Base18.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- BUILDER FINISH: file/chisel the reentrant root to the exact reference ·  · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P065-Base18&lang=en)

### P065-Cap12 / M047

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P065-Cap12.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P065-Cap12&lang=en)

### P066-Main / M049

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P066-Main.svg)

**ONE_SIDE_CNC_READY** · 4 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P066-Main&lang=en)

### P067-Main / M049

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P067-Main.svg)

**ONE_SIDE_CNC_READY** · 4 mm · FACE A [-0.0, -0.0, -1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P067-Main&lang=en)

### P068-Main / M050

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P068-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 3 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P068-Main-R1: CUT · FACE A · [0, 18.0] mm
- P068-Main-R2: CUT · FACE A · [0, 18.0] mm
- P068-Main-R3: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: file/chisel corner to reference · P068-Main-R1 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P068-Main-R2 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: file/chisel corner to reference · P068-Main-R3 · FACE A datum 18.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P068-Main&lang=en)

### P069-Main / M051

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P069-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P069-Main&lang=en)

### P070-Main / M051

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P070-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P070-Main&lang=en)

### P071-Main / M052

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P071-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P071-Main-R1: CUT · FACE A · [0, 12.0] mm
- BUILDER FINISH: file/chisel corner to reference · P071-Main-R1 · FACE A datum 12.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P071-Main&lang=en)

### P072-Main / M053

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P072-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P072-Main&lang=en)

### P073-Main / M054

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P073-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -1.4210854715202004e-14 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P073-Main&lang=en)

### P074-Main / M054

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P074-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [-1.0, -0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction -5.684341886080802e-14 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P074-Main&lang=en)

### P075-Ply1 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P075-Ply1.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P075-Ply1&lang=en)

### P075-Ply2 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P075-Ply2.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P075-Ply2&lang=en)

### P076-Ply1 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P076-Ply1.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P076-Ply1&lang=en)

### P076-Ply2 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P076-Ply2.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P076-Ply2&lang=en)

### P077-Ply1 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P077-Ply1.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P077-Ply1&lang=en)

### P077-Ply2 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P077-Ply2.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P077-Ply2&lang=en)

### P078-Ply1 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P078-Ply1.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P078-Ply1&lang=en)

### P078-Ply2 / M055

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P078-Ply2.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P078-Ply2&lang=en)

### P079-Main / M056

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P079-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 12 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 6 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P079-Main-R1: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P079-Main-R2: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P079-Main-R3: CUT · FACE A · [0, 12.0] mm
- P079-Main-R4: CUT · FACE A · [2.2093438190040615e-13, 12.0] mm
- P079-Main-R5: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P079-Main-R6: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- BUILDER FINISH: file/chisel corner to reference · P079-Main-R3 · FACE A datum 12.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P079-Main&lang=en)

### P080-Main / M057

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P080-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 12 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 6 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P080-Main-R1: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P080-Main-R2: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P080-Main-R3: CUT · FACE A · [2.2093438190040615e-13, 12.0] mm
- P080-Main-R4: CUT · FACE A · [0, 12.0] mm
- P080-Main-R5: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- P080-Main-R6: CUT · FACE A · [1.1343703754107537e-13, 12.0] mm
- BUILDER FINISH: file/chisel corner to reference · P080-Main-R4 · FACE A datum 12.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P080-Main&lang=en)

### P081-Main / M058

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P081-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 6 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P081-Main-R1: CUT · FACE A · [0, 6.0] mm
- BUILDER FINISH: file/chisel corner to reference · P081-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P081-Main&lang=en)

### P082-Main / M058

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P082-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 6 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P082-Main-R1: CUT · FACE A · [0, 6.0] mm
- BUILDER FINISH: file/chisel corner to reference · P082-Main-R1 · FACE A datum 6.0 mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P082-Main&lang=en)

### P083-Face / M059

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P083-Face.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 4.547473508864641e-13 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P083-Face&lang=en)

### P083-Top / M060

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P083-Top.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P083-Top&lang=en)

### P083-Side1 / M061

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P083-Side1.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P083-Side1&lang=en)

### P083-Side2 / M061

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P083-Side2.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P083-Side2&lang=en)

### P084-Face / M059

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P084-Face.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 4.547473508864641e-13 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P084-Face&lang=en)

### P084-Top / M060

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P084-Top.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P084-Top&lang=en)

### P084-Side1 / M061

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P084-Side1.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P084-Side1&lang=en)

### P084-Side2 / M061

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P084-Side2.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [1.0, 0.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P084-Side2&lang=en)

### P085-Reduced18 / M062

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P085-Reduced18.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 1 POCKET; face reduction 4.0 mm.
Fit/coupon HOLD: True

- P085-Reduced18-FACE_REDUCTION: POCKET · FACE A · see register mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P085-Reduced18&lang=en)

### P086-Reduced18 / M062

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P086-Reduced18.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, -1.0, 0.0]

CNC PROVIDED: outer contour; 0 CUT; 1 POCKET; face reduction 4.0 mm.
Fit/coupon HOLD: True

- P086-Reduced18-FACE_REDUCTION: POCKET · FACE A · see register mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P086-Reduced18&lang=en)

### P087-Main / M063

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P087-Main.svg)

**ONE_SIDE_CNC_READY** · 12 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 0 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P087-Main&lang=en)

### P088-Main / M064

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P088-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 3 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P088-Main-R1: CUT · FACE A · [0, 18.0] mm
- P088-Main-R2: CUT · FACE A · [0, 18.0] mm
- P088-Main-R3: CUT · FACE A · [0, 18.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P088-Main&lang=en)

### P089-Main / M065

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P089-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P089-Main-R2: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P089-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P089-Main-R3 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P089-Main&lang=en)

### P090-Main / M064

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P090-Main.svg)

**ONE_SIDE_CNC_READY** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 3 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P090-Main-R1: CUT · FACE A · [0, 18.0] mm
- P090-Main-R2: CUT · FACE A · [0, 18.0] mm
- P090-Main-R3: CUT · FACE A · [0, 18.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P090-Main&lang=en)

### P091-Main / M065

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P091-Main.svg)

**ONE_SIDE_CNC_PLUS_MANUAL_FINISH** · 18 mm · FACE A [0.0, 0.0, 1.0]

CNC PROVIDED: outer contour; 1 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P091-Main-R2: CUT · FACE A · [0, 18.0] mm
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P091-Main-R1 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.
- BUILDER FINISH: drill / countersink with selected bit, depth stop and qualified guide · P091-Main-R3 · FACE A datum [0, 18.0] mm. Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P091-Main&lang=en)

### P092-Main / M066

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P092-Main.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P092-Main-R1: CUT · FACE A · [0, 6.0] mm
- P092-Main-R2: CUT · FACE A · [0, 6.0] mm
- P092-Main-R3: CUT · FACE A · [0, 6.0] mm
- P092-Main-R4: CUT · FACE A · [0, 6.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P092-Main&lang=en)

### P093-Main / M066

![FACE A / FACE B](../exports/generated/viewer-v332/orientation/P093-Main.svg)

**ONE_SIDE_CNC_READY** · 6 mm · FACE A [-0.0, -1.0, -0.0]

CNC PROVIDED: outer contour; 4 CUT; 0 POCKET; face reduction 0.0 mm.
Fit/coupon HOLD: True

- P093-Main-R1: CUT · FACE A · [0, 6.0] mm
- P093-Main-R2: CUT · FACE A · [0, 6.0] mm
- P093-Main-R3: CUT · FACE A · [0, 6.0] mm
- P093-Main-R4: CUT · FACE A · [0, 6.0] mm
BUILDER FINISH: none in the nominal operation audit.

[Exact axes, depths and operations](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [Inspect member](../exports/generated/viewer-v32/index.html?part=P093-Main&lang=en)

---
CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

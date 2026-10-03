# Assembly manual — V34 framework

**NOT FOR CNC. Physical qualification, production-lot stock and coupon remain pending. Raised playfield support remains HOLD.**

Backbox plate: TOP insertion during assembly only. Monitor/glass/lower panel: FRONT service. No top disassembly for monitor replacement.

## 00 — Before you start

### 00.1 — Confirm the preparation holds

Read the supplier profile and inventory the production lot. Do not cut full sheets until actual thickness, coupon clearance and hardware interfaces are approved. CURRENT plywood purchasing uses only nominal 12 mm and 18 mm stock. Measure each actual production lot and qualify the fit coupon before release. Finished local webs can be thinner after a documented FACE_A pocket/reduction; this does not create a 6/8 mm purchase family. The backglass bezel deliberately retains its 6 mm finished web by one-face reduction from 12 mm stock because the glass/display gap is protected. SW 01 solid leg blocks remain a separate solid-wood material, not a plywood stock exception.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: PLAY
Check: Record the measured lot, coupon result and selected hardware; unresolved values stay HOLD.
WAITING_FOR_COUPON — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

### 00.2 — Prepare ordinary assembly tools

Prepare clamps, square, tape, drill/driver, depth stop, selected bits and qualified angle guides. Exact drive sizes follow purchased hardware. Do not improvise precise angled drilling freehand.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: PLAY
Check: A qualified guide and finish procedure must exist before each affected manual operation.
WAITING_FOR_COUPON — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 01 — Identify flatpack parts

### 01.1 — Match manufacturing IDs and faces

Match every M-family and P-instance against the 106-piece register (102 CNC +4 shop-made). Use the orientation cards: FACE A is the finished machining datum; FACE B receives no CNC. Keep mirrored parts labelled.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Count 106 pieces in 62 families. Do not mistake 93 installed assemblies for the cut-piece count.
WAITING_FOR_COUPON — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 01.2 — Check CNC work and builder finish

Use each piece’s preparation card. Check the contour and FACE A pockets first; then perform only the listed manual drilling, countersinking or corner/bevel finish after its holds clear. Depths refer to finished FACE A, including after face reduction.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Never request a second CNC face. Trial-fit without forcing thickness-dependent joints; physical coupon approval is mandatory.
WAITING_FOR_COUPON — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 02 — Main cabinet shell

### 02.0 — Position and qualify solid leg blocks before closing the shell

Shop-cut SW 01 × 4 from dry, straight, stable knot-free solid wood:54× 54× 126 mm square stock, then 45° rip to the accepted triangular section. Check dimensions/squareness; register FL/FR/RL/RR to the documented cabinet datums. Before FLOOR, PC_BASE or SHELF_1 installation, fit the diagonal-face/top-stop jig, clamp, drill only with physically qualified hardware parameters, then test the real backing plate and bolts. Retain temporary support throughout.

Parts: P029-Solid, P030-Solid, P031-Solid, P032-Solid.
Hardware: H18, B13, F37.
Quantity: See authoritative catalog; never multiply repeated IDs.
Diagonal backing face inward;126 mm grain/height vertical. F uses 14 mm top spacer; R uses bare top stop. Front lower/upper axes 42/100 mm from bottom; rear 28/86 mm — reference only.
SHOP DATUM A: diagonal backing face. TOP stop is datum B. No CNC and no plywood layer stack.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: HOLD: real leg/backing/bolt pitch, diameter, drilling depth, selected drill and clamp envelope, printed registration and test bore.58 mm vs 57.15 mm remains unresolved. No drilling through assembled shelves/floor; protect bore breakout and all neighboring surfaces.
WAITING_FOR_PHYSICAL_MEASUREMENT — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 02.1 — Dry-fit the captured shell

After SW 01 jig qualification at 02.0, lay SideL on a flat reference. Insert Floor, Front, Rear and RearBearingShelf into the 4 mm side captures BEFORE closing SideR. Shelf capture is an open-top rabbet. Clamp lightly, seat shoulders, measure both diagonals and 600 mm exterior width. No screw may pull a bad fit into place. M006 installs later; do not trap the floor/shelf after closing the shell.

Parts: P001-Main, P002-Main, P003-Main, P004-Main, P005-Main, P028-Main.
Hardware: F06, G01.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED OVERVIEW
Check: CABINET SQUARE CHECK: compare diagonals and seating on a flat reference. No numerical tolerance is released yet.
WAITING_FOR_COUPON — CNC RELEASE BLOCKED. Actual material, coupon, jig and selected hardware must be qualified. DRY-FIT DATUM HOLD: shelf support/cradle axes match side references. T-guide wall anchors have no matching side pilots; retained rear-door hinge cleats need qualified placement templates. Captured shell F06 reinforcement remains unresolved. Do not ask the builder to invent these permanent locations.

### 02.2 — Glue and clamp qualified captured joints

Disassemble after the dry-fit checkpoint. Apply the approved structural adhesive, reassemble on the reference, clamp and recheck square. Fit widths use measured plywood plus coupon clearance. Do not apply glue until the coupon passes. Front/rear joints retain existing SW 01/leg hardware interfaces; final shell fastener family F06 remains held.

Parts: P001-Main, P002-Main, P003-Main, P004-Main.
Hardware: F06, G01.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED OVERVIEW
Check: HOLD permanent assembly until the joint schedule and material/bond qualification are complete.
WAITING_FOR_COUPON — CNC RELEASE BLOCKED. Actual material, coupon, jig and selected hardware must be qualified.

## 03 — Floor and structural supports

### 03.1 — Retain floor and bearing shelf; then install M006

Keep M006 out while qualifying/drilling underside pockets. Paper templates locate longitudinal stations only; jig angle, stop collar, screw and depth are hardware-dependent. Check exterior skin, top-face skin and driver path on a coupon. Glue/clamp shelf shoulders at unchanged Z596.9. Install approved screws without forcing the fit. After access work, glue the two retained M006 underside ledges to floor/side; their final F06 mechanical fixing schedule remains a physical-hardware hold. Cure before loading. Optional offcut supports are tooling only and removed after cure.

Parts: P005-Main, P006-Main, P007-Main, P028-Main.
Hardware: F58.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: INTERIOR INSPECTION
Check: Confirm continuous floor support and the shelf’s broad bearing faces. Do not use screws to pull a distorted shell into alignment.
WAITING_FOR_PHYSICAL_MEASUREMENT — CNC RELEASE BLOCKED. Actual material, coupon, jig and selected hardware must be qualified.

## 04 — Shelves, crossmembers and PCBase

### 04.1 — Install guides and shelf supports

Identify S1–S3 and T1–T3 with their matching supports/guides. Use the actual mounting interfaces; F05/F52/I14 are catalog hardware, not permission to guess unlocated holes.

Parts: P009-Main, P010-Main, P011-Main, P012-Main, P013-Main, P014-Main, P015-Main, P016-Main, P017-Main, P018-Main, P019-Main, P020-Main, P021-Main, P022-Main, P023-Main, P024-Main, P025-Main, P026-Main, P027-Main.
Hardware: F03, W01, I01, F04, W02, B02, F05, F52, I14, F07, I02, W03.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: SHELF HEIGHT CHECK: confirm left/right seats align and removable shelves/crossmembers can be extracted without forcing.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 04.2 — Secure removable boards

Fit shelf clamp hardware and PCBase flush floor anchors only after their stack is confirmed. PCBase is the accepted low board, not a drawer. Electronics payloads are optional later additions.

Parts: P009-Main, P010-Main, P011-Main, P012-Main, P013-Main, P014-Main, P015-Main, P016-Main, P017-Main, P018-Main, P019-Main, P020-Main, P021-Main, P022-Main, P023-Main, P024-Main, P025-Main, P026-Main, P027-Main.
Hardware: F03, W01, I01, F04, W02, B02, F05, F52, I14, F07, I02, W03.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Check positive retention and service removal; keep side-wall SSF zones unbridged.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 05 — Playfield wooden pivot supports

### 05.1 — Install the retained open cradles

Install the real M026/M027 profiles with the six unchanged F01 coordinates and direct floor feet. The upper-wall trim was rejected: unchanged minimum root alone does not prove unchanged ear stiffness. Preserve 180° dowel seating,8.251 mm front root and 6.280 mm rear limiting ligament. S3/T3 stay at CURRENT datums. Verify 48 mm lift-out and 50° service; no bearings or metal shaft.

Parts: P035-Main, P036-Main.
Hardware: F01.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: CRADLE ALIGNMENT CHECK: both seats share the accepted axis and both feet bear continuously. Do not shim or relocate the axis without a new review.
WAITING_FOR_COUPON — PHYSICAL QUALIFICATION STILL REQUIRED: selected adjusters, inserts, retention parts, mounting screws, actual plywood/display mass, coupon and load/rattle tests. Reference hardware geometry does not release purchased-hole dimensions or CNC. Do not work below an unsupported raised playfield.

### 05.2 — Review front-landing interfaces and holds

Prepare the two SW02 shop-made solid landing bodies using step 06.0. No lamination, binder screw or glue-to-side operation remains. Preserve the eight side-retention screws and qualified M8/M6 interfaces. Do not install or drill until actual purchased hardware, wood quality and guide/coupon are qualified.

Parts: P095-Solid, P096-Solid.
Hardware: F59, F61, H27, I15, I16, I17, I18, W11, W12, B17.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
SHOP TOP A / INNER B / FRONT — NO CNC. Side-specific template plus qualified clamped portable 90° drill guide and depth stop.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: PLAYFIELD LANDINGS
Check: Verify full body-to-side bearing, screw/receiver engagement, no exterior breakthrough, retained button/wire/tool access, and clearance to plunger, S1, legs and front service. Exact purchased dimensions remain HOLD.
PROVISIONAL_HARDWARE — PHYSICAL QUALIFICATION STILL REQUIRED: selected adjusters, inserts, retention parts, mounting screws, actual plywood/display mass, coupon and load/rattle tests. Reference hardware geometry does not release purchased-hole dimensions or CNC. Do not work below an unsupported raised playfield.

## 06 — Playfield base, dowel and straps

### 06.0 — Prepare and install SW02 solid landing blocks

Order two dry, stable, straight, knot-free solid-wood blanks to the actual 68 × 70 × 54 mm specification. Check square and grain orientation. The shop-made body reproduces the accepted external/mating union; obsolete binder holes are filled because there is no lamination. Drill only after actual M8 insert, M6 retention path and side screws are selected. Clamp the qualified guide and use depth stops; no precise freehand drilling. Preserve eight side screws and the original M8 adjusters/captive M6 retention. Four F60 binder screws and all lamination glue operations are removed. Do not glue the removable landing body to the cabinet side.

Parts: P095-Solid, P096-Solid.
Hardware: F59, F61, H27, I15, I16, I17, I18, W11, W12, B17.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
SHOP DATUM: square side/rear/top faces on the SW02 drawing. No CNC sheet or plywood lamination. Use the side-specific 1:1 paper center template only with its calibration bar and a qualified clamped 90° drill guide.
Compact spanner for the selected M6 hex-head retention bolt (reference 10 mm across flats); exact tool size/access follow purchased hardware. Adjustment spanner and locknut tool also depend on the selected M8 family.
Viewer: PLAYFIELD LANDINGS
Check: Match the side-specific SW02 template and unchanged X72/X528, Y245 contact datum; verify full side contact and all selected insert/bolt bores before cabinet installation. No template is drilling release without actual hardware and coupon/guide qualification.
WAITING_FOR_PHYSICAL_MEASUREMENT — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

### 06.1 — Capture the wooden dowel

Attach the Ø 32 wooden dowel with four commercial saddle straps B01 and eight F02 screws to the playfield base. Retain the accepted replaceable adapter interface. No metal shaft or bearings. Use CURRENT M025 with the clean relief open to the front edge: narrowed straight sides and rounded return to full width, with no horn, front bridge or hooked projection. Keep the V33.6 rear 180 × 110 mm R8 service window and two strain-relief slots. Preserve the VESA load region, dowel, four straps and eight F02 coordinates. Button clearance is derived from the restored front leaf-body, terminal, wire and tool reserves. Do not move buttons to fit the plywood. Final display/button hardware and stiffness qualification remain HOLD. Owner-requested V33.6.2 relief extends 30 mm farther inward on EACH side: total inset 52 mm, remaining front width 396 mm, retained length 87 mm and R8 transition. Buttons stay atY 89/Y127, local side top minus 65 mm. Rear window, strain slots, VESA region, dowel and straps remain unchanged.

Parts: P034-Main.
Hardware: F02, H01, B01.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: PLAYFIELD LIFT-OUT
Check: Check strap seating, screw engagement and no splitting after purchased strap/material qualification.
WAITING_FOR_PHYSICAL_MEASUREMENT — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

### 06.2 — Seat rear dowel and lower onto the front landings

Remove the main playfield glass and matrix. With the assembly independently supported, release both captive retainers to their parked limits. Seat both ends of the Ø 32 wooden dowel fully in the rear cradles, then lower onto the front pads at X72/X528, Y245. SW02 solid blocks replace the former three-layer bodies without moving the mating envelope. T1/T2/T3 remain intentionally clear and are not playfield supports. Preserve the 52 mm inset, 87 mm relief length, R8 transitions and 396 mm front width. Retention release is the existing 10.5 mm reference travel after unscrewing; exact purchased stack remains held.

Parts: P034-Main, P095-Solid, P096-Solid.
Hardware: F02, H01, B01, F59, F61, H27, I15, I16, I17, I18, W11, W12, B17.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Compact spanner for the selected M6 hex-head retention bolt (reference 10 mm across flats); exact tool size/access follow purchased hardware. Adjustment spanner and locknut tool also depend on the selected M8 family.
Viewer: SUPPORT LOAD PATH
Check: REAR SEATING / FRONT CONTACT CHECK: both dowel ends fully seated; both front contacts loaded without rocking. No weight on glass, lockdown, buttons, electronics, cable or T1/T2/T3. Keep the module externally supported until the selected hardware/wood is qualified.
WAITING_FOR_PHYSICAL_MEASUREMENT — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

### 06.3 — Reproduce the approved PLAY pose and engage retention

Reproduce the unchanged 9.906669° PLAY pose with the rear dowel fully seated and equal left/right front height. Mechanical hardware travel remains ±3 mm, but the validated installed common-height geometry screen is only −1.9 to +0.9 mm about the reference, maintaining the requested 1 mm clearance. This is a setup/tolerance screen, not user-selectable angle adjustment or left/right twist permission. −3 mm hits the front button envelope; +3 mm hits the main glass. After qualified setup, lock both adjuster nuts and reset each captive M6 stop for the qualified receiver engagement; the original 7 mm reference is not a selected insert depth. Open the coin door and use the compact spanner to engage both original captive M6 × 100 hex-bolt retainers. Tool-free grip and quick-pin alternatives are not selected. Retainers resist uplift/rattle and do not replace broad pad support. For opening/lift-out, provide an independently qualified primary service support first, then release/park both retainers. The modeled 0–50° and 48 mm paths are geometric clearances only: CURRENT has no defined/proven primary support at 50°.

Parts: P095-Solid, P096-Solid.
Hardware: F59, F61, H27, I15, I16, I17, I18, W11, W12, B17.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Compact spanner for the selected M6 hex-head retention bolt (reference 10 mm across flats); exact tool size/access follow purchased hardware. Adjustment spanner and locknut tool also depend on the selected M8 family.
Viewer: PLAYFIELD LANDINGS
Check: CLOSED SUPPORT CHECK: rear seated, both pads in contact, crossmembers clear, both captive retainers engaged. SAFE ADJUSTMENT SCREEN: stay within −1.9/+0.9 mm only while reproducing the required nominal pose; purchased tolerances and differential leveling need physical verification. PRIMARY SERVICE SUPPORT HOLD before raising.
PROVISIONAL_HARDWARE — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

## 07 — Main rear services and fans

### 07.1 — Fit rear door hardware

Fit the main rear door, its two hinge assemblies, keeper and lock from the selected hardware. Main rear hinge hardware is separate from the backbox piano hinges. Keep selected-hardware quantities as formulas.

Parts: P008-Main, P037-Main, P038-Main.
Hardware: H02, H03, B03, H04, F08, F09, F53, G02, H05, H06, F10, I03, F11, F12, I04, H07, B04, B05, B06, F13, G03.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: INTERIOR INSPECTION
Check: REAR DOOR SWEEP CHECK: verify opening, latch engagement and ordinary tool access without forcing the flush door.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 07.2 — Fit rear fans from the interior

Place fan against rear wood, inner finger grill against fan, then F56 screw heads facing the interior. Drive toward the wood. Withdraw old F10 through bolts/exterior washers and rear I03 nuts. Floor fan M4 fasteners remain unchanged. Select grip length, wood bite and pilot on the purchased fan/grill; no exterior breakthrough. Fan/accessory selection remains optional.

Parts: P008-Main, P037-Main, P038-Main.
Hardware: H02, H03, B03, H04, F08, F09, F53, G02, H05, H06, I03, F11, F12, I04, H07, B04, B05, B06, F13, G03, F56.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: INTERIOR INSPECTION
Check: Filters remain serviceable; no fan or electronics purchase is required to understand the mechanical kit.
WAITING_FOR_PHYSICAL_MEASUREMENT — CNC RELEASE BLOCKED. Actual material, coupon, jig and selected hardware must be qualified.

### 07.3 — Install the removable underfront user module

Identify the existing structural 18 mm FLOOR / M005 with its scoped underside bay and the removable 12 mm plate from their FACE A cards. The bay is one-face machining in the existing floor, not a separate wooden box; preserve its authoritative underside-front datums. Retain the plate with the four positive machine-fastener/captive-insert interfaces, accessible from below. Fit a blank plate for the basic mechanical cabinet, or a replaceable user adapter after controls are selected. Alternative button/USB layouts use this same bay and are mutually exclusive. Keep a flexible harness/service-loop corridor and the rear component reserve; the electrical connector remains builder-configurable. Do not cut schematic button or USB holes into permanent wood.

Parts: P097-Main.
Hardware: F62, I19, E15, E16.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Driver/hex tool for selected four machine fasteners; exact size pending purchase. Qualified locator/depth-stop tools for held inserts where specified.
Viewer: UNDERFRONT USER MODULE
Check: MODULE RETENTION / SERVICE CHECK: all four attachments positively secure the plate; no loose hardware can drop inside. Confirm underside tool access, selected control reach and clearance to front structure, coin door, plunger, legs, playfield and landing hardware. Support the plate during removal; release its four attachments and follow the documented path. Cable flex/connector disconnection is hardware-dependent, not a validated electrical instruction.
PROVISIONAL_HARDWARE — HARDWARE_PENDING / PURCHASE BEFORE CNC: BUTTON_BORE_MM=null; USB_CUTOUT=null. Seller references are conflicting packaging evidence, not selected dimensions. The old fixed-function 220× 55 schematic is historical only.

## 08 — Simplified backbox: captured plate, front service

### 08.1 — Identify the two sides

Confirm inside FACE_A and front/back before drilling.

Parts: P042-Main, P043-Main.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Confirm inside FACE_A and front/back before drilling.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.2 — Attach both fixed stops

Use2 direct screws per12x40x30 stop; tops atZ854.

Parts: V34-BB_MONITOR_STOP_L, V34-BB_MONITOR_STOP_R.
Hardware: F64.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Use2 direct screws per12x40x30 stop; tops atZ854.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.3 — Inspect inside guides

4mm capture; width follows measured plate and coupon. R2 bottom extension clears plate corners.

Parts: P042-Main, P043-Main.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. 4mm capture; width follows measured plate and coupon. R2 bottom extension clears plate corners.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.4 — Join floor to sides

Preserve210mm lower side andY1146 floor.

Parts: P044-Main, P042-Main, P043-Main, P046-Main.
Hardware: F54, F16.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Preserve210mm lower side andY1146 floor.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.5 — Square shell

Dry fit; measure diagonals before fastening.

Parts: P044-Main, P042-Main, P043-Main.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Dry fit; measure diagonals before fastening.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.6 — Lower monitor plate from TOP

Top must not yet be installed. Plate is a permanent structural interface.

Parts: V34-BB_MONITOR_PLATE.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Top must not yet be installed. Plate is a permanent structural interface.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.7 — Engage both guides

Keep plate square; never force coupon-unqualified fit.

Parts: V34-BB_MONITOR_PLATE.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Keep plate square; never force coupon-unqualified fit.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.8 — Seat on both stops

Confirm both lower bearing contacts, no hanging corner.

Parts: V34-BB_MONITOR_PLATE, V34-BB_MONITOR_STOP_L, V34-BB_MONITOR_STOP_R.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Confirm both lower bearing contacts, no hanging corner.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.9 — Install top

Top closes guide exits and captures plate.

Parts: P045-Main.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Top closes guide exits and captures plate.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.10 — Fasten top directly to sides

Glue plus4 direct side screws; pilot/countersink qualified for actual stock. Pocket alternative not selected.

Parts: P045-Main, P042-Main, P043-Main.
Hardware: F63, G01.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Glue plus4 direct side screws; pilot/countersink qualified for actual stock. Pocket alternative not selected.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.11 — Check captured plate

No upward removal with top installed; no extra L-brackets.

Parts: V34-BB_MONITOR_PLATE, P045-Main.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. No upward removal with top installed; no extra L-brackets.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.12 — Bring monitor from FRONT

Glass/strip out. Enter at+5mm height to clear bottom glass lip, then adjust from rear.

Parts: BB_Display32.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Glass/strip out. Enter at+5mm height to clear bottom glass lip, then adjust from rear.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.13 — Fit rear VESA bolts

Use one75 or100 pattern;4 bolts. Support monitor while loose.

Parts: V34-BB_MONITOR_PLATE, BB_Display32.
Hardware: F29, W13.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Use one75 or100 pattern;4 bolts. Support monitor while loose.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.14 — Set image height

Slots permit+/-5mm. Verify visible opening; selected monitor controls exact drilling.

Parts: BB_Display32.
Hardware: F29.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Slots permit+/-5mm. Verify visible opening; selected monitor controls exact drilling.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.15 — Set depth with spacers

Study0/3/6/9/12mm. Verify engagement and no bottoming; never use wooden shoes.

Parts: BB_Display32.
Hardware: B19.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Study0/3/6/9/12mm. Verify engagement and no bottoming; never use wooden shoes.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.16 — Tighten and check monitor

Monitor retained through fold independently of glass. Purchased hardware load proof remains required.

Parts: BB_Display32.
Hardware: F29.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Monitor retained through fold independently of glass. Purchased hardware load proof remains required.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.17 — Mount DMD on loose panel

DMD sits in front of plate; rear VESA75, +/-2mm height. Body plus spacers must fit400x200x45 reserve.

Parts: V34-BB_DMD_SPEAKER_PANEL, BB_DMDEnvelope.
Hardware: F33, W13.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. DMD sits in front of plate; rear VESA75, +/-2mm height. Body plus spacers must fit400x200x45 reserve.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.18 — Mount both speakers

Direct mounts; actual diameter/pitch pending. Maximum60mm rear body reserve.

Parts: V34-BB_DMD_SPEAKER_PANEL, BB_SpeakerEnvelopeL, BB_SpeakerEnvelopeR.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Direct mounts; actual diameter/pitch pending. Maximum60mm rear body reserve.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.19 — Insert completed panel from FRONT

Electronics are optional; blank mechanical panel can be assembled first.

Parts: V34-BB_DMD_SPEAKER_PANEL, BB_DMDEnvelope, BB_SpeakerEnvelopeL, BB_SpeakerEnvelopeR.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Electronics are optional; blank mechanical panel can be assembled first.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.20 — Locate panel in side seats

Rear face seats atY1197; confirm4 attachment axes.

Parts: V34-BB_DMD_SPEAKER_PANEL.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Rear face seats atY1197; confirm4 attachment axes.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.21 — Secure four panel bolts

Two each side; cross-dowels captive in panel. No cassette frame/cleats.

Parts: V34-BB_DMD_SPEAKER_PANEL.
Hardware: F30, I12.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Two each side; cross-dowels captive in panel. No cassette frame/cleats.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.22 — Install glass from FRONT

Reverse screened removal: approach tilted10degrees with bottom elevated7mm, lower6mm, tilt upright, lower1mm onto pads. Top stays fixed.

Parts: BB_Backglass, V34-BB_GLASS_BOTTOM_SEAT.
Hardware: G08, G09, G10.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Reverse screened removal: approach tilted10degrees with bottom elevated7mm, lower6mm, tilt upright, lower1mm onto pads. Top stays fixed.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.23 — Install upper retaining strip

One12mm strip overlaps upper edge8.2mm; two upward fasteners accessible from front/below.

Parts: V34-BB_GLASS_TOP_RETAINER.
Hardware: F65, I08.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. One12mm strip overlaps upper edge8.2mm; two upward fasteners accessible from front/below.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.24 — Tighten strip screws

Do not clamp bare glass hard; fit liner and selected screw engagement.

Parts: V34-BB_GLASS_TOP_RETAINER.
Hardware: F65.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. Do not clamp bare glass hard; fit liner and selected screw engagement.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

### 08.25 — Verify retention in every orientation

6mm bottom lip exceeds3.8mm top travel. Side overlap4mm. Geometry pass is not impact qualification.

Parts: BB_Backglass, V34-BB_GLASS_TOP_RETAINER.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left/right;Y rear;Z up. Use FACE_A card.
FACE_A machined. FACE_B no CNC. Edge bores only with qualified manual guide.
Square, clamps, selected screwdriver/hex drive, qualified drill guide/depth stop.
Viewer: EXPLODED DETAILED
Check: Confirm stage fit and positive attachment before proceeding. 6mm bottom lip exceeds3.8mm top travel. Side overlap4mm. Geometry pass is not impact qualification.
WAITING_FOR_PHYSICAL_MEASUREMENT — Actual materials, coupon and purchased hardware required. No CNC release.

## 09 — WPC hardware and upright locks

### 09.1 — Measure and install the WPC family

Measure 01-9011-L/R, 02-4352 and 4322-01139-12B before any final hinge drilling. The reference rotation axis is Y1066.8/Z508; it is not a released drill pattern. Do not substitute metric threads into purchased imperial hardware.

Parts: P088-Main, P089-Main, P090-Main, P091-Main.
Hardware: H08, H09, H10, F14, F15, W06, B16, H11, W07, I05, I06, F17, H12, W08, H13, B07, B08.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX UNLOCKED
Check: HOLD installation until bends, floor-hole pattern, bushing and complete bolt stack are measured and validated.
WAITING_FOR_PHYSICAL_MEASUREMENT — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 09.2 — Fit two rear-operated captive locks

Retain H11 × 2 at L X130/Y1260 and R X470/Y1260 with metal-backed shelf receivers, loss protection, tethers and parking sockets. Exact purchased knob/receiver details remain provisional.

Parts: P088-Main, P089-Main, P090-Main, P091-Main.
Hardware: H08, H09, H10, F14, F15, W06, B16, H11, W07, I05, I06, F17, H12, W08, H13, B07, B08.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX UNLOCKED
Check: UPRIGHT LOCK CHECK: floor bears broadly on shelf; both independent clamps engage and can be released/parked through open rear doors with lower panel installed.
WAITING_FOR_PHYSICAL_MEASUREMENT — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 10 — Twin backbox rear doors

### 10.1 — Fit hinge cleats and leaves

Use the 18 mm cleats reduced from FACE A to the accepted 14 mm finished geometry. Preserve the hinge axis. Install one continuous hinge on each outer vertical edge; screw count follows the selected hinge hole schedule.

Parts: P079-Main, P080-Main, P085-Reduced18, P086-Reduced18, P087-Main.
Hardware: H14, H15, H16, F18, F19, G04, G05.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX REAR DOORS OPEN
Check: No permanent center mullion. Both doors must reach the validated 100° service position upright.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

### 10.2 — Fit passive bolts, astragal and active lock

Secure passive upper/lower bolts first, then close the active leaf and keyed cam lock against the overlap. Fit replaceable perimeter and center gaskets. Open active leaf before passive leaf.

Parts: P079-Main, P080-Main, P085-Reduced18, P086-Reduced18, P087-Main.
Hardware: H14, H15, H16, F18, F19, G04, G05.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX REAR DOORS OPEN
Check: REAR DOOR SWEEP CHECK: no clash with fan bodies, loops, overlap or lock hardware. Doors are service closures, not structural shear panels.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 11 — Backbox ventilation

### 11.1 — Assemble intake baffles and filter frames

Build each baffle from its face, top and two returns using the four actual manufacturing pieces. Keep the downward mouth open and filters removable. Qualified glue seams must not obstruct the throat.

Parts: P081-Main, P082-Main, P083-Face, P083-Top, P083-Side1, P083-Side2, P084-Face, P084-Top, P084-Side1, P084-Side2, P092-Main, P093-Main.
Hardware: H17, B09, G06, G07, F20, F21, I07, F22, B10, F23, B11, F55.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Per door: preserve 220× 80 mm inlet and 220× 36 mm downward mouth before mesh effects. No thermal certification is implied.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution. V33.7 stack re-selection HOLD: F21 blank-station stack gains 6 mm; F22 intake frame/baffle stack changes. Measure the selected hardware stack before assigning final lengths; no quantity or length is guessed. F12 main intake-filter interface is retained by 4 mm underside counter-recesses in 12 mm stock.

### 11.2 — Choose blank or optional fan

Install the blank module for an unpowered station, or a selected 120 mm fan/accessory stack. For a moving fan, preserve the low-voltage flexible corridor and strain relief through full door motion; connectors remain builder-configurable.

Parts: P081-Main, P082-Main, P083-Face, P083-Top, P083-Side1, P083-Side2, P084-Face, P084-Top, P084-Side1, P084-Side2, P092-Main, P093-Main.
Hardware: H17, B09, G06, G07, F20, F21, I07, F22, B10, F23, B11, F55.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Check ordinary screwdriver access with the door open; no display removal. Fine exhaust filters need later pressure-loss analysis.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 15 — Matrix mechanical carrier

### 15.1 — Fit wood seats and removable retention

Install the two fixed wood seats, inserts and removable retainer screws. The carrier is mechanical; LED panels and their model-specific fasteners remain future electronics. Follow the saved forward/lift removal path.

Parts: P039-Main, P040-Main, P041-Main.
Hardware: F34, I13, F35, B12.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: MATRIX REMOVAL
Check: Check both seats and removal before playfield service or backbox fold. Do not force the matrix past installed main glass.
PROVISIONAL_HARDWARE — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 16 — Leg and lockdown interfaces

### 16.2 — Fit purchased legs and front interfaces

Use matched real pinball legs, bolts, backing plates and levelers. The 600 mm body uses the accepted custom-width lockdown strategy; exact receiver/fastener interfaces remain held. Mobility skates are optional external accessories.

Parts: P029-Solid, P030-Solid, P031-Solid, P032-Solid.
Hardware: G11, G12, F36, H18, B13, F37, H19, F38, H20, H21, H22, F39, H23, H24, F40, H26.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: EXPLODED DETAILED
Check: Keep cabinet securely supported until leg/load and attachment qualification is complete. No integrated wheels.
WAITING_FOR_PHYSICAL_MEASUREMENT — Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.

## 17 — Mechanical inspection and normal fold

### 17.1 — Perform the normal fold sequence

Open rear doors; release and park both rear-operated locks; close/latch the rear doors; remove MAIN PLAYFIELD GLASS and MATRIX; fold. Keep the lower panel, secured display, DMD/speakers and backbox front glass installed. No routine electronics disconnection.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX FOLD 45°
Check: BACKBOX FOLD CHECK: geometry supports 0–90° pure rotation around Y1066.8/Z508. Check actual retention, cable slack, surroundings and handling only after physical qualification. Reverse the sequence and positively engage both locks upright.
WAITING_FOR_PHYSICAL_MEASUREMENT — PHYSICAL QUALIFICATION STILL REQUIRED: selected adjusters, inserts, retention parts, mounting screws, actual plywood/display mass, coupon and load/rattle tests. Reference hardware geometry does not release purchased-hole dimensions or CNC. Do not work below an unsupported raised playfield.

### 17.2 — Separate rare hinge maintenance

Rare WPC hinge service may require lower-panel removal and playfield lift-out/removal for side-pivot access. This is not the normal fold procedure. Keep all unqualified structural/ergonomic gates visible.

Parts: .
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: BACKBOX FOLD 45°
Check: Final inspection is a checkpoint framework, not structural certification or manufacturing authorization.
WAITING_FOR_PHYSICAL_MEASUREMENT — OPERATIONAL HOLD: do not service beneath a raised playfield until an independently qualified primary support is defined. No safety straps are promoted. Secondary straps must never replace the primary support or set the service angle. Hardware/material/load/coupon qualification and CNC remain blocked.

## 18 — Future electronics overview

### 18.1 — Identify future controls and electronics

The underfront user module is a removable generic plate in the fixed front bay. The owner configuration may use five programmable buttons plus a dual USB module; four plus USB and a button-only configuration share the same bay. Functions are assigned by the builder; the permanent wood imposes no volume, operating-mode or pairing function. Button bores and USB cutout remain unselected and hardware-dependent. The conventional front-right plunger remains a separate provisional interface at X520/Z280. Displays, controllers, power interfaces and electronics remain optional, with generic carriers and service passage.

Parts: P033-Main, P097-Main.
Hardware: F29, F32, F33, E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, B14, F42, F43, F44, F45, F46, F47, F48, F49, F50, B15, F51, H25, R01, R02, R03, R04, F62, I19, E15, E16.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: UNDERFRONT USER MODULE
Check: USER CONFIGURATION CHECK: no final machining from schematic centers; buy and measure the actual controls first. Route a flexible service loop without selecting a connector family. Confirm reach, accidental-operation protection, rear body/nut space and removal with the chosen parts. USB thread compatibility through 12 mm is unverified; any one-face rear pocket waits for physical dimensions and coupon. Keep at least the planned 70 mm rear USB reserve.
WAITING_FOR_PHYSICAL_MEASUREMENT — HARDWARE_PENDING / PURCHASE BEFORE CNC: BUTTON_BORE_MM=null; USB_CUTOUT=null. Seller references are conflicting packaging evidence, not selected dimensions. The old fixed-function 220× 55 schematic is historical only.

### 18.2 — Optional accessory boards and cable route zones

Keep the open S1/S2/S3 and T1/T2/T3 architecture. Optional ACC01 is one 100 × 120 × 12 mm board family; sampled positions are S2 right with rear-edge clamps and S3 left with front-edge clamps. Use two physically selected removable screw clamps per chosen board, with the shelf carrying gravity load. No new permanent holes or dense grid. Small impact toys require separate retention/load qualification; this screen proves clearance only. Reuse 6 × 22 R3 strain-relief slots; retain compact existing backbox 6 × 16 R3 and underfront 4 × 12 R2 exceptions. Left low SIGNAL and right low ELV POWER routes are planning zones; protected mains routing remains separate.

Parts: ACC01-S2, ACC01-S3.
Hardware: —.
Quantity: See authoritative catalog; never multiply repeated IDs.
X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.
FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.
Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.
Viewer: MODULARITY STUDY
Check: Remove optional board/clamps before independent shelf extraction and release the S3 cable-anchor clamp. The current PF400 mm loop passes 63 geometric states without routine service disconnection; primary raised support remains HOLD. Backbox generic passage/slots are retained, but no continuous selected fold harness is validated. Do not cut the held central VESA service window.
OPTIONAL — OPTIONAL; excluded from minimum BOM, sheets, mass and packing. Clamp SKU/body/throat, payload rating, actual cable bends and supported backbox route remain HOLD. No electrical connector choice is prescribed.

## CNC provided / builder finish

- **P001-Main / M001** — FACE_A [1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.00000000000003] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.762479051592436e-14, 13.000000000000018] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.762479051592436e-14, 13.000000000000018] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.762479051592436e-14, 13.000000000000018] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.762479051592436e-14, 13.000000000000018] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [2.4730217873525362e-14, 13.000000000000025] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [2.1149748619109232e-14, 1.0000000000000215] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [2.4730217873525362e-14, 13.000000000000025] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [3.5360603334311236e-14, 1.0000000000000357] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [4.957145804951324e-14, 1.00000000000005] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P002-Main / M002** — FACE_A [-1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 1.0000000000000002] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 1.0000000000000002] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 13.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 1.0000000000000002] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P003-Main / M003** — FACE_A [0.0, 1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [0, 11.77820185402092] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.778201854020924] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.778201854020885] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.778201854020889] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P004-Main / M004** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [0, 11.802118519922043] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.802118519922043] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.802118519921972] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 11.802118519921972] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 17.999999999999545] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.; NARROW_FEATURE_MANUAL_FINISH / FACE_A / HOLD — Offset has no usable Ø4 center domain; use exact reference with ordinary hand tools, subject to local access qualification.; DRILL_OR_COUNTERSINK / FACE_A / [0, 17.999999999999545] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.; DRILL_OR_COUNTERSINK / FACE_A / [5.999999999999773, 17.999999999999545] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [5.999999999999773, 17.999999999999545] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P005-Main / M005** — FACE_A [0, 0, -1]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. HARDWARE_DEPENDENT_RETENTION / FACE_A / None — V33.5 reference schedule is packaging only; qualify purchased jig, screws and inserts. Underside shelf pockets are MANUAL work referenced from top FACE_A by measured thickness; no second-face CNC.; HARDWARE_DEPENDENT_UNDERFRONT_ATTACHMENT / FACE_A / HOLD — Install four blind metal inserts from the pocket shoulder, 2 mm inward from the FLOOR underside FACE_A datum. Reference insert length10 mm; actual pilot, drill-point depth, engagement and intact opposite skin require purchased hardware and coupon before drilling. No freehand center transfer. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P006-Main / M006** — FACE_A [-0.0, -0.0, -1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P007-Main / M006** — FACE_A [-0.0, -0.0, -1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P008-Main / M007** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. R2_ACCESS_RESIDUAL_FINISH / FACE_A / HOLD — Finish the measured cutter-inaccessible residual to the exact reference boundary; no unreported rounding change. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P009-Main / M008** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P010-Main / M008** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P011-Main / M009** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P012-Main / M010** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.749999999999995, 11.25] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.749999999999995, 11.25] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P013-Main / M011** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P014-Main / M010** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.750000000000023, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.750000000000023, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P015-Main / M011** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P016-Main / M012** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.749999999999995, 11.25] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.749999999999995, 11.25] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P017-Main / M013** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.75, 11.250000000000028] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P018-Main / M014** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. BEVEL_SANDING_FINISH / FACE_A / [0, 18.0] — Hand-finish only conservative roughing terraces to the exact bevel reference. Both end profiles define the plane; no table saw, router or planer required. Verify full bearing line before assembly. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P019-Main / M014** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. BEVEL_SANDING_FINISH / FACE_A / [0, 18.0] — Hand-finish only conservative roughing terraces to the exact bevel reference. Both end profiles define the plane; no table saw, router or planer required. Verify full bearing line before assembly. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P020-Main / M014** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. BEVEL_SANDING_FINISH / FACE_A / [0, 18.000000000000114] — Hand-finish only conservative roughing terraces to the exact bevel reference. Both end profiles define the plane; no table saw, router or planer required. Verify full bearing line before assembly. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P021-Main / M015** — FACE_A [1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P022-Main / M016** — FACE_A [-1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P023-Main / M015** — FACE_A [1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P024-Main / M016** — FACE_A [-1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P025-Main / M015** — FACE_A [1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P026-Main / M016** — FACE_A [-1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P027-Main / M017** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [0, 17.999999999999986] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.312382593579958e-14, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 17.999999999999986] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [1.312382593579958e-14, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P028-Main / M018** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.; DRILL_OR_COUNTERSINK / FACE_A / [6.000000000000114, 17.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.000000000000114, 17.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.000000000000227, 17.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [6.000000000000227, 17.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; HARDWARE_DEPENDENT_RETENTION / FACE_A / None — V33.5 reference schedule is packaging only; qualify purchased jig, screws and inserts. Underside shelf pockets are MANUAL work referenced from top FACE_A by measured thickness; no second-face CNC. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P033-Main / M024** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P034-Main / M025** — FACE_A [-0.0, 0.172043766268355, -0.9850893068591292]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. MANUAL_OBLIQUE_BLIND_RECEIVER / FACE_A / None — Install two blind M6 metal receivers on the vertical retention axes. The axes are oblique to the inclined M025 underside. Qualify a rigid drill guide on production-lot scrap using the purchased receiver. Verify pilot, actual axial engagement, drill-point allowance and intact top skin before drilling. Reference maximum bore depth is a packaging limit, not a drilling instruction. FACE_B receives no CNC; this is explicitly manual builder finish. Physical qualification remains HOLD. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P035-Main / M026** — FACE_A [1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [1.326716514427062e-14, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 17.999999999999993] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P036-Main / M027** — FACE_A [-1.0, 0.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P037-Main / M028** — FACE_A [0, 0, -1]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. R2_ACCESS_RESIDUAL_FINISH / FACE_A / HOLD — Finish the measured cutter-inaccessible residual to the exact reference boundary; no unreported rounding change. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P038-Main / M028** — FACE_A [0, 0, -1]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. R2_ACCESS_RESIDUAL_FINISH / FACE_A / HOLD — Finish the measured cutter-inaccessible residual to the exact reference boundary; no unreported rounding change. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P039-Main / M029** — FACE_A [-1.0, -0.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [4.999999999999979, 12.999999999999979] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [4.999999999999979, 12.999999999999979] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [5.949999999999986, 12.049999999999986] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P040-Main / M029** — FACE_A [-1.0, -0.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. OUTER_REENTRANT_CORNER_FINISH / FACE_A / HOLD — Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.; DRILL_OR_COUNTERSINK / FACE_A / [4.999999999999886, 12.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [4.999999999999886, 12.999999999999886] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [5.9499999999998865, 12.049999999999887] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P041-Main / M030** — FACE_A [0.0, -0.42261826174069905, 0.9063077870366502]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [9.499999999999943, 12.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [9.499999999999943, 12.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P044-Main / M033** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P046-Main / M035** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.; SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P079-Main / M056** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P080-Main / M057** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P081-Main / M058** — FACE_A [0, 1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P082-Main / M058** — FACE_A [0, 1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SQUARE_CORNER_FINISH_OR_COUPON_RELIEF / FACE_A / HOLD — Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P083-Face / M059** — FACE_A [0, -1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P083-Top / M060** — FACE_A [0, 0, 1]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P083-Side1 / M061** — FACE_A [-1, 0, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P083-Side2 / M061** — FACE_A [1, 0, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P084-Face / M059** — FACE_A [0, -1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P084-Top / M060** — FACE_A [0, 0, 1]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P084-Side1 / M061** — FACE_A [-1, 0, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P084-Side2 / M061** — FACE_A [1, 0, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P085-Reduced18 / M062** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P086-Reduced18 / M062** — FACE_A [0.0, -1.0, 0.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P087-Main / M063** — FACE_A [-0.0, -1.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P088-Main / M064** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P089-Main / M065** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P090-Main / M064** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P091-Main / M065** — FACE_A [0.0, 0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.; DRILL_OR_COUNTERSINK / FACE_A / [0, 18.0] — Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P092-Main / M066** — FACE_A [0, 1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P093-Main / M066** — FACE_A [0, 1, 0]; FACE_B NO CNC. ONE_SIDE_CNC_READY.  [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P029-Solid / SW01** — FACE_A [0.7071067811865475, 0.7071067811865475, 0]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_SQUARE_STOCK_AND_45_DEG_RIP / FACE_A / HOLD — Shop supplies triangular prism; ordinary builder tools do not make the long rip.; JIG_GUIDED_DRILLING_HOLD / FACE_A / HOLD — Measure real leg/backing/bolt hardware; qualify print/bushings and hand drill before drilling. Use selected parameters, not reference58mm by default. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P030-Solid / SW01** — FACE_A [-0.7071067811865475, 0.7071067811865475, 0]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_SQUARE_STOCK_AND_45_DEG_RIP / FACE_A / HOLD — Shop supplies triangular prism; ordinary builder tools do not make the long rip.; JIG_GUIDED_DRILLING_HOLD / FACE_A / HOLD — Measure real leg/backing/bolt hardware; qualify print/bushings and hand drill before drilling. Use selected parameters, not reference58mm by default. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P031-Solid / SW01** — FACE_A [0.7071067811865475, -0.7071067811865475, 0]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_SQUARE_STOCK_AND_45_DEG_RIP / FACE_A / HOLD — Shop supplies triangular prism; ordinary builder tools do not make the long rip.; JIG_GUIDED_DRILLING_HOLD / FACE_A / HOLD — Measure real leg/backing/bolt hardware; qualify print/bushings and hand drill before drilling. Use selected parameters, not reference58mm by default. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P032-Solid / SW01** — FACE_A [-0.7071067811865475, -0.7071067811865475, 0]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_SQUARE_STOCK_AND_45_DEG_RIP / FACE_A / HOLD — Shop supplies triangular prism; ordinary builder tools do not make the long rip.; JIG_GUIDED_DRILLING_HOLD / FACE_A / HOLD — Measure real leg/backing/bolt hardware; qualify print/bushings and hand drill before drilling. Use selected parameters, not reference58mm by default. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P097-Main / M074** — FACE_A [0, 0, 1]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. HARDWARE_DEPENDENT_UNDERFRONT_ATTACHMENT / FACE_A / HOLD — Drill four through-clearance holes from rear/up FACE_A after matching the purchased M4 screw, head and receiver layout. Reference centers only; drill dimensions held. Hardware inserts from below at assembly, but the through holes require no opposite-face CNC. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P095-Solid / SW02** — FACE_A [0, 0, 1]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_RECTANGULAR_SOLID_WOOD_BLANK / TOP A / INNER B / FRONT / HOLD — Woodshop supplies68×70×54 mm rectangular dry, stable, straight, knot-free structural solid wood. Qualify species, moisture, grain and squareness; no plywood lamination, glue-up or binder screws. Grain along68 mm U/X cantilever axis is provisional.; QUALIFIED_PORTABLE_DRILL_GUIDE_HOLD / TOP A and INNER B, each indexed from FRONT and side/bottom datum / HOLD — Paper locates centers only. It cannot guide54/68 mm drill paths. Clamp a qualified perpendicular guide and test the selected pilot/insert/head stack on scrap of the same wood. No precise freehand drilling. Final drill diameters, depths, drill-point allowance and template release await purchased hardware; no new printed jig is required unless the commercial guide fails qualification.; CABINET_INTERFACE_HOLD / FACE_A / HOLD — Preserve eight side screw locations and the two held M025 receivers. No new side/M025 bores are cut in CURRENT. Use the existing qualified cabinet template/depth-stop process; do not glue SW02 to the side wall. Keep positive support/retention and reset stop after permitted leveling. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P096-Solid / SW02** — FACE_A [0, 0, 1]; FACE_B NO CNC. SHOP_MADE_SOLID_WOOD_PART. SHOP_CUT_RECTANGULAR_SOLID_WOOD_BLANK / TOP A / INNER B / FRONT / HOLD — Woodshop supplies68×70×54 mm rectangular dry, stable, straight, knot-free structural solid wood. Qualify species, moisture, grain and squareness; no plywood lamination, glue-up or binder screws. Grain along68 mm U/X cantilever axis is provisional.; QUALIFIED_PORTABLE_DRILL_GUIDE_HOLD / TOP A and INNER B, each indexed from FRONT and side/bottom datum / HOLD — Paper locates centers only. It cannot guide54/68 mm drill paths. Clamp a qualified perpendicular guide and test the selected pilot/insert/head stack on scrap of the same wood. No precise freehand drilling. Final drill diameters, depths, drill-point allowance and template release await purchased hardware; no new printed jig is required unless the commercial guide fails qualification.; CABINET_INTERFACE_HOLD / FACE_A / HOLD — Preserve eight side screw locations and the two held M025 receivers. No new side/M025 bores are cut in CURRENT. Use the existing qualified cabinet template/depth-stop process; do not glue SW02 to the side wall. Keep positive support/retention and reset stop after permitted leveling. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P042-Main / M031** — FACE_A [1.0, -0.0, -2.220446049250313e-16]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P043-Main / M032** — FACE_A [-1.0, -0.0, -2.220446049250313e-16]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **P045-Main / M034** — FACE_A [-0.0, -0.0, -1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_MONITOR_PLATE / M074** — FACE_A [-0.0, 1.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_MONITOR_STOP_L / M075** — FACE_A [1.0, -0.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_MONITOR_STOP_R / M075** — FACE_A [-1.0, -0.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_DMD_SPEAKER_PANEL / M076** — FACE_A [-0.0, 1.0, -0.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_GLASS_TOP_RETAINER / M077** — FACE_A [-0.0, -0.0, -1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
- **V34-BB_GLASS_BOTTOM_SEAT / M037** — FACE_A [-0.0, -0.0, 1.0]; FACE_B NO CNC. ONE_SIDE_CNC_PLUS_MANUAL_FINISH. SELECTED_HARDWARE_DRILLING / FACE_A / None — Reference only. Purchased screw, insert/cross-dowel, glass liner and jig dimensions required. Use clamped guide and depth stop for edge bores. No CNC flip. [Exact local axes / eixos locais](../exports/generated/backbox-v34/assembly-manual.json)
[V34 CAD review](../exports/generated/backbox-v34/review.html) · [BOM](../exports/generated/backbox-v34/manufacturing-bom.csv)

Quantities are stage totals, never multiply repeated mentions. Electronics remain optional; purchased hardware controls final bores and thread engagement.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

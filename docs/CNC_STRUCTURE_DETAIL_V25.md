# Structure detailing audit — v25

Checkpoint inspected and fetched: `628807c72d3f8aef459a3ec4eb392c5abdc3a25e`, branch `feat/active-build-cleanup-v25`. Existing owner modifications to historical `cad/master/vpin-master.FCStd` and deletion of its backup were preserved. Active source was regenerated before detailing; baseline saved-solid checks pass.

## Two artifacts, one architecture

`cad/active/vpin-active.FCStd` remains the regenerated packaging baseline used by existing checks. `exports/generated/cnc-detail/vpin-cnc-detail-preview.FCStd` is derived from that fresh source and contains the joint-detail wood geometry. It is explicitly a review artifact, with zero fit clearance and no cutter relief or hardware holes. It must not silently replace the active model in manufacturing workflows.

The detail script owns only its output, and does not modify reference models or historical CAD. Its stock-relative capture depth is `t/3`; main nominal preview uses 18 mm. `config/cnc_detail_v25.json` keeps measured thickness, fit and tooling null. It fails if a measured thickness is populated without migrating the older builders' stock values, avoiding a false claim that changing one number makes the whole legacy source production-parametric.

## Connection audit

[STRUCTURAL_JOINTS_V25.csv](../bom/STRUCTURAL_JOINTS_V25.csv) accounts for all 73 baseline wood contact pairs plus three internal two-ply lamination joints (76 records), including incidental contacts that must **not** be glued. It identifies actual part IDs, joint type/depth, stock dependency, glue, fastener requirement, whether prelocation is possible, hardware dependency and original overlap volume. Contacts are checked against a fresh saved active model, not merely counted. The register also distinguishes removable closures and bearing interfaces from permanent joints.

Implemented review details:

- Side captures for front, rear, bottom and three low crossmembers are actual receiving cuts.
- Front/rear bottom grooves accept the captured bottom.
- Rear shelf gains t/3 side capture and t/3 rear bearing instead of coincident solid wood; the backbox load reaches full-strength shell.
- Backbox sides remain full-height; floor/top enter t/3 rebates; rear frame strips seat in perimeter rebates.
- Cradle ties and pivot blocks lap into the side rails with the rail retaining 2t/3 through the capture zone; rear tie/block overlap becomes a receiving pocket.
- CPU bottom-seated rails, their crossmember saddles, hatch ligaments, small utility apertures and all baseline service geometry are retained.

All 36 detail wood objects are connected valid solids, with no positive-volume wood/wood overlap. This geometric result does **not** prove joint capacity, insertion order, tool access or proof loading. Square-bottom pockets need shop-confirmed relief or rounded mating corners; no manual routing/trimming is an accepted fallback.

Permanent glue joints require dry-fit squareness first, then full bearing-face glue and clamps. End captures locate low crossmembers; their bottom seated joints do not need redundant blocks. The four rear frame strips transfer shear into captured perimeter joints; their butt corners are not treated as independent high-strength joints. Side doublers remain full-face laminations with through-bolted metal load paths. Pivot rear-beam connections require the measured cheek-plate/bolt detail before being called complete.

Supplemental screw locations are design-locatable, but are not yet released patterns. Pilot diameter/depth must match selected screws and actual plywood, and coordinates must avoid pending hardware patterns. The CSV does not imply that a `DESIGN_LOCATABLE` connection already has CNC pilot geometry. High-load leg, hinge, pivot, safety and slide connections need through-bolts/backing, not screws into plywood edges.

## Reinforcement review — all 36 records retained

| Parts/family | Decision and actual load-path reason |
|---|---|
| 2 sides, front, rear, bottom | Keep: primary shell shear, leg and captured-panel loads. Rear hatch keeps substantial side ligaments; do not add a full second rear panel. |
| 3 low crossmembers | Keep: three spaced low torsion/shear ties; rear member also lies beneath the rail saddle. Deleting one needs a stiffness/proof basis. |
| Rear shelf | Keep, detail capture: backbox gravity and upright locking loads. It is an intentional structural shelf, not an electronics deck. |
| Backbox floor/top/2 sides | Keep: perimeter load path and display replacement volume. |
| 4 rear-frame strips | Keep: retain economical strip nesting and service aperture. A one-piece ring would reduce register count but consumes a large sheet region; no demonstrated strength/nesting benefit yet. |
| Backbox door | Keep removable: closure only; do not credit it as permanent shear bracing. |
| 2 cradle rails + 3 ties | Keep: independent display structure and adapter support without a broad deck. |
| 2 pivot blocks + rear beam | Keep: concentrated pivot/plate reactions; nominal 2t lamination is a fabrication assembly requiring two labeled plies, not a magical 36 mm stock assumption. |
| 2 combined landing/latch doublers | Keep existing union: one shaped part per side already replaces overlapping blocks while retaining both reactions. |
| 2 safety + 2 gas doublers | Keep separately: different reaction locations, independent safety path; replacing them with thin plates requires wood bearing/bolt proof, not visual simplification. |
| CPU door/shelf/2 rails | Keep: one board directly holds case; narrow seated rails + four metal angles/backing supply uplift restraint. No second sled, broad shelf or leg furniture. |

No legitimate deletion was established, so ACTIVE_PARTS remains 36 assembly records. Final flat plywood piece count will be higher when the three 2t assemblies are split into separate plies; this is explicitly a release task, not concealed by the record count.

## Feature register interpretation

[CNC_FEATURES_V25.csv](../bom/CNC_FEATURES_V25.csv) uses one record per profile, marking instruction, cut operation or **hardware pattern group**. `DEFINED_PARAMETRIC` means a contour/recipe or marking instruction exists; it does not mean released toolpath or numeric machining setup. Global removed-solid bounds are audit evidence, not rectangular cut instructions. Part-local datum/face and exact solid/recipe are authoritative for the next CAM detail.

`BLOCKED_MEASURE_HARDWARE` rows contain no guessed X/Y, diameter or depth. Each points to an HF worksheet. `BLOCKED_DESIGN` rows expose ventilation/passport work that measurements alone cannot solve. Candidate plate/axis values already present in older configs are excluded from hardware hole records.

## Structural findings and retained limits

The checkpoint's overlaps were genuine machining contradictions, resolved as joint-review cuts without changing cabinet architecture. The 13.8 mm rail/bracket gap still falls 1.2 mm below the additional 15 mm planning reserve; no extra interference was introduced and no corrective redesign is justified without actual hardware. Cradle/beam bolt detail, material strength, joint capacity and physical assembly remain unproven. The stage is a detailing and measurement checkpoint, not manufacturing approval.

## Dry-fit assembly sequence to verify with the coupon/prototype

1. Identify face/orientation marks and inspect the measured-stock coupon. Prepare the three two-ply pivot assemblies flat between cauls; keep final through-bolt access available.
2. Lay the left shell side inside-up on padded supports. Dry-seat front/rear, captured bottom, three low ties and rear shelf. Bring the right side onto all mating captures. Check diagonals, bottom squareness and hatch dimensions before any glue.
3. Remove and repeat with glue only after the complete dry fit and CNC hardware patterns are accepted. Install specified prelocated fasteners without freehand structural layout. No closed pocket may require hidden post-assembly routing.
4. Assemble backbox perimeter around the four rear-frame strips, leaving its door off. Verify rebate engagement and squareness; mount the measured hinge/lock assemblies only after the shelf/floor fixture establishes their true stack.
5. Dry-fit the cradle ties into rails and the rear pivot assemblies. Verify the full moving envelope, alignment of both bearing axes and temporary safe support before hardware proof tests. Laminations and through-bolts share concentrated load; do not infer strength from boolean-solid validity.
6. Install bottom-seated CPU rails, four clamps/backing plates, measured slides and the one case shelf. Backing fasteners must remain accessible from below; prototype the installation sequence before closing any inaccessible area. Fit both doors and verify complete opening/disconnect access.

This sequence is a review plan, not an approved assembly guide. Any required specialist trimming, inaccessible fastener, trapped part or missing locating mark stops release and returns to CNC source detailing. Final alignment marks, pilot coordinates, dogbones and nests must be included in the vendor package before wood is ordered.

# V32 210 mm backbox: structural review and integration hold

**NOT PROMOTED.** The 210 mm sides / Y1146 floor have a viable geometric joint, broad shelf bearing, usable locking material and a clear reconstructed-wood fold. However, the corrected cabinet-side pivot is obstructed internally by **both fixed playfield supports `PF_OpenCradleL/R`**. The hinge installation gate fails at upright. Changing those supports would reopen an accepted system outside this task. Neither CURRENT CAD nor the viewer was regenerated or replaced.

HEAD BEFORE: `f91ba219b824dc8de77d101a2ba68cd078ac037e`.
HEAD AFTER: the commit containing this report, obtainable with `git log -1 --format=%H -- studies/backbox-structure-v32/README.md`; the final delivery message records the pushed hash.
Branch: `feat/cabinet-review-v32`. Manufacturing: **BLOCKED**.

## Authority and scope

The [positive-control WPC study](../wpc-fold-v32/README.md) remains the validated mechanism authority: pure rotation about transverse X, Y1066.8 / Z508, derived from rear Y1308.1 minus 241.3 mm (9.5 in). This task does not reopen that result.

[Central active datum](../../config/wpc_kinematics_v32.json) and [regression guard](../../tools/wpc_reference_v32.py) now govern design kinematics. Compatibility configurations `backbox_fold_v10.json` and `structure_geometry_v14.json` use the same datum. None authorizes drilling. Final holes, arm bends, backing, bushing stack, bolt length and offsets require physical 01-9011-L, 01-9011-R, 02-4352 and 4322-01139-12B measurement.

The [candidate configuration](../../config/backbox_structure_review_v32.json) separates structural geometry from `service_passage.width/depth/x_position/y_position`. Its only cable feature is a generic 260 × 60 mm passage centered at X300/Y1218. Termination and disconnection remain **USER CONFIGURABLE**. No connector, gland, plate or harness architecture was designed.

Only 210 mm side depth was evaluated. No 200/190/180 variants were generated. The accepted cabinet, glass channels, matrix/supports, playfield, shelves, rear closure, electronics and viewer are unchanged. The candidate has isolated shelf/passage changes and fills the obsolete pivot bores, but has **no new hinge drilling**. These are study solids, not production replacements.

## Structural geometry

Both sides are symmetric. The eight reconstructed backbox wood members are valid single solids without unintended mutual penetration. Existing rear-frame/service openings are retained. The display and generic toy/board provisions of the 210 mm study are retained; this is not a review of arbitrary future payloads.

| Item | Left and right result |
|---|---:|
| Lower side depth / front | 210 mm / Y1098.1 |
| Straight floor front / rear | Y1146.0 / Y1302.1 |
| Side projection ahead of floor | 47.9 mm |
| Floor thickness | 18 mm nominal |
| Actual side–floor engagement | 156.1 mm per side |
| Horizontal capture shoulder | 6 × 156.1 = 936.6 mm² per side |
| Vertical interface | 18 × 156.1 = 2,809.8 mm² per side |
| Front end shoulder | 6 × 18 = 108 mm² per side |
| Total exact contact interface | 3,854.4 mm² per side |
| Continuous side stock alongside floor capture | 12 mm remaining |
| Lower-front projection stock | Full 18 mm |

One minimal study correction is appropriate: terminate the 6 mm capture at the actual inset floor, leaving full stock ahead of it. The earlier isolated Boolean sequence left an unused rebate there. The corrected projection is part of the broad continuous side plate; it is not a separate thin finger or horn. No crossmember, cleat, rail, metal reinforcement or forward floor extension is geometrically required. The upper/rear connected frame provides the side's continuation; the floor is not its sole connection.

The 47.9 mm projection should not be treated as a stand-alone heavy toy bracket. A deliberately narrow 18 × 18 mm cantilever-strip idealization with a provisional 2 kg tip load gives 0.967 MPa bending **demand**, or 1.933 MPa at 2× load. This is a sensitivity screen, not an allowable stress or an approved 2 kg payload. Veneer quality, grain, ply voids, adhesive and actual fasteners remain qualification inputs. Heavy equipment belongs on the existing broad removable-board zones, away from lower service access.

### Joint and fastener opportunity

The captured shoulder carries upright compression; a bonded vertical face and provisional mechanical retention transfer shear/peel when folding. Do not rely on screw count alone or assume equal load sharing proves capacity.

Three reasonable *planning* screw axes per side are Y1171 / 1224.05 / 1277.10, Z605.9, entering from X−90 or X690 toward the floor. Pitch is 53.05 mm, above the previous 50 mm planning minimum; first/last longitudinal end distance is 25 mm. The center lies 9 mm from each floor-thickness edge. For the illustrative ≤4 mm shank envelope, this leaves 7 mm wood to the edge; it is **not** a qualified edge-distance rule. The straight rear frame's front is Y1290.1, leaving 13 mm from the rear screw center (11 mm from the illustrated shaft) to that adjacent frame. All are side-accessible, without a new hole in the CAD.

The illustrative path passes through 12 mm side skin plus 20 mm floor engagement. Six path cylinders clear the split hinge/lock reserves by at least **7 mm** in 3D. Hinge floor access columns are inboard of these paths; shared Y values alone do not imply collision. The cable opening starts at X170 while left floor-thread reach ends at X−58 (right mirrored), so it is far from the joint. Lock reserves at X120/480 also remain inboard. No permanent screw SKU, pilot, countersink or final spacing release is made. A glued captured joint with modest mechanical retention is geometrically viable; coupon/load qualification must establish its actual strength. If that fails, a simple cleat/capture revision is preferable to dense screws or custom metal.

## Load path and planning loads

The existing provisional payload inventory was retained; only reconstructed wood mass and CG were recomputed at the existing assumed 650 kg/m³ plywood density. Total is **31.8725 kg**, CG **(300, 1190.5081, 968.8107) mm**, weight **312.563 N**. This is a planning model, not measured payload or certification.

Upright: side/top/rear frame and equipment → captured floor/rear structure → broad floor/shelf contact → cabinet side/rear support. The two positive locks resist separation and overturning; they are not the primary gravity bearing surfaces. Allocating the entire weight to the two 6 mm capture shoulders gives 0.1669 MPa nominal compression demand; allocating it to both vertical contact faces gives 0.0556 MPa average shear demand. The 2× sensitivity doubles these values. These averages omit stress concentration, screw withdrawal and adhesive defects.

At the existing provisional 0.3g horizontal planning load, force is 93.77 N and moment about the shelf is 34.87 Nm. Treating the bearing front Y1146 as the forward tipping line and the two locks at Y1188 as a symmetric hold-down pair gives approximately **249.55 N uplift per lock** after gravity restoration; rearward tipping about Y1290.1 gives 18.34 N each. Double the assumed mass to double these demands. These are ideal rigid-body demand estimates; no bolt, washer or plywood capacity is claimed.

Folding: side/top/rear frame and payload → floor/side captures → floor hinge-flange region → rigid WPC arms → cabinet-side pivots, with the operator controlling gravitational torque. The shelf ceases to support the box immediately after positive rotation. The current installation cannot complete that load path because the internal pivot region is occupied by the fixed cradle supports.

Calculated gravity torque is −38.67 Nm at 0°, −0.071 Nm at 15°, +74.50 Nm at 45°, and +144.03 Nm at 90°; the sign reversal is near 15°. The operator must control the box through this reversal. `loads.fold_equilibrium` records an explicitly **vertical-only** force at a provisional top-front grip. Its very large negative near-upright force is the consequence of that force direction's short lever arm, not a required human force or a valid handling prescription. A tangential force at the same approximately 813 mm radius would have a 47.57 N magnitude at upright. Actual hand position/direction, payload shift, hinge reactions and transport support require later handling validation. Do not use the vertical-only diagnostic to rate a hinge or instruct a builder.

## Shelf bearing, locks and local spans

Exact floor/shelf area is **65,672.4 mm²**, **77.6227%** of the former 84,604.625877 mm². Shelf top material remaining is **76,317.9 / 91,917.9 = 83.0283%**. Shelf front remains Y1127.125. It extends 18.875 mm ahead of the floor, without restoring floor material in the channel sweep.

The bearing footprint is X18..582, Y1146..1290.1 minus the generic opening X170..430, Y1188..1248. This leaves a continuous ring: **42 mm front**, **42.1 mm rear**, and **152 mm left/right** strips. There are no thin ligaments or arbitrary local obstacle-shaped cuts. The larger floor rear strip extends to Y1302.1, including an 12 mm overhang beyond the shelf rear. Outboard floor reaches 96 mm beyond each cabinet shelf edge to X−78/678; the side capture is at that outboard end. These are real bending spans; floor/shelf area alone cannot qualify them. The central void has no claimed bearing, and removable equipment must not treat it as a solid mounting surface. The retained broad front/rear ligaments connect the left/right floor regions.

Two provisional lock centers X120/480, Y1188 each have an uninterrupted Ø61.4 mm wood reserve through floor and shelf, a radius20 mm washer/backing allowance, and an unobstructed radius18 × 80 mm upper tool cylinder. Minimum center-to-outer-edge distance is 42 mm; center-to-passage-side distance is 50 mm. Therefore washer material margins are at least 22 mm to the outer edge and 30 mm to the passage. Lock material/access geometry is reasonable. Final holes, lower hardware attachment and tool requirements remain tied to the unselected hardware; no diameter or SKU is frozen.

## Hinge reserve and exact promotion blocker

The old Y1270-centered keepouts are superseded. Reference floor attachment rows are X−30.1625 / 630.1625, Y1181.1 / 1225.55 / 1270. **Y1270 here is the rear FLOOR FASTENER, not the pivot.** Flange, exterior arm, top access and internal cabinet pivot access are modeled separately. Blanket longitudinal exclusions would incorrectly eliminate good side/floor fastener positions.

The provisional exterior arm corridor extends from Y1044.8 near the corrected pivot to Y1295 below the backbox floor. The floor flange lies below Z596.9; reference access cylinders extend above the floor to Z655. These have gross upright wood compatibility. Their silhouette/thickness and clearances are packaging assumptions, not purchased-arm manufacture or a complete swept-hardware proof.

**Failed gate:** an R22 internal pivot access reserve overlaps each `PF_OpenCradle` by **8,826.5324 mm³**. The axis itself lies inside the cradle, so this is not merely a large tool envelope. Left support bounds are X18..36, Y995.2506..1075.2506, Z36..514.2203; right is mirrored. The accepted U-shaped upper cradle has wood directly at Y1066.8 / Z508.

A much smaller coaxial probe, radius **4.7625 mm**, length **3 mm**, from the inside cabinet wall into each cradle, overlaps **213.7672 mm³ on each side**. This probe demonstrates absence of even a small internal bolt/bushing access space. It does not pretend to be the final purchased bushing stack. With that accepted wood left in place, gross reference installation is unresolved at **0°**. Moving the validated WPC pivot to hide this conflict would be wrong. Cutting or moving the cradle would be an unrelated-system design change, and was not performed.

## Fold validation and limits

**Reconstructed wood 0→90: YES. Complete installed hinge assembly 0→90: NO — installation gate fails at 0°.** Glass and matrix are removed for every fold study. Remaining glass channels, fixed matrix support and the accepted cabinet/playfield supports remain collision obstacles. No wood self-intersection or moving-wood/fixed-wood collision occurs.

OCC/FreeCAD uses the same exact-solid common-volume/distance engine as the positive control. Required angles, every integer degree, extra 0.001/0.01/0.05/0.1° samples and 116 adaptive clearance intervals are checked. The 0..0.001° bearing transition is proved analytically from positive vertical motion at all initially contacting material; subsequent intervals use a whole-body displacement bound against exact midpoint separation. Saved 1/15/45/90° solids were reopened and checked against the rigid transform.

| Angle | Floor/shelf gap mm | Nearest channel gap mm | Wood penetration |
|---:|---:|---:|---:|
| 0 | 0 | 27.4422 | 0 |
| 0.25 | 0.3447 | 27.0753 | 0 |
| 0.5 | 0.6878 | 26.7118 | 0 |
| 1 | 1.3687 | 25.9958 | 0 |
| 2 | 2.7099 | 24.6118 | 0 |
| 5 | 6.5644 | 20.4493 | 0 |
| 10 | 12.4023 | 13.0174 | 0 |
| 15 | 18.6425 | 8.8791 | 0 |
| 30 | 42.0728 | 22.5023 | 0 |
| 45 | 68.6944 | 30.0764 | 0 |
| 60 | 96.6930 | 29.5905 | 0 |
| 75 | 124.1605 | 21.0776 | 0 |
| 90 | 149.2250 | 5.1179 | 0 |

Overall minimum modeled wood clearance is **0 mm at intentional upright bearing**; its positive-angle infimum is also zero. Smallest positive sampled global gap is **0.0013823 mm at 0.001°**, floor/cabinet side. Do not mislabel the **5.1179 mm sampled minimum channel gap** as the global minimum or a continuously certified ≥5 mm channel bound. Continuous certification establishes no contact, while sampled channel clearance exceeds the preferred 5 mm. Bearing releases at **0°+**, and the floor is clear of the shelf at every positive angle. First *wood-fold* collision: **NONE**. First *hardware-reserve* conflict: **0°, pivot / PF_OpenCradleL and R**.

## Toy capacity, promotion and manufacturing

210 mm lower side depth: **YES preserved**. Generic side zones: **YES**, 37,593.2 mm² each from the existing 210 mm study, above the lower hinge/service area. Chimes, bells, strobes, sirens, beacon, contactors, LED/DOF hardware, relays and boards remain optional on removable generic carriers. No toy-specific permanent holes were added.

| Requested report item | Result |
|---|---|
| Old active reference | Y1270 / Z508, 38.1 mm rear offset — superseded |
| New active reference | Y1066.8 / Z508, 241.3 mm rear offset, pure rotation |
| Active stale pivot references remaining | **0** in audited active engineering sources |
| Additional wood reinforcement required | **NO** by geometry screen; actual joint qualification pending |
| Shelf bearing geometry acceptable | **YES**, no area-restoration change needed |
| Lock material reserve acceptable | **YES**, provisional hardware |
| Hinge reference reserve updated | **YES**; internal pivot reserve fails |
| Final hinge holes frozen | **NO** |
| Physical hinge measurement required | **YES** |
| Generic cable passage | **YES**, independently configurable |
| Connector/disconnect architecture | **USER CONFIGURABLE** |
| Isolated architecture promoted to CURRENT V32 | **NO**, pivot/cradle integration blocker above |
| Accepted production geometry changed | **NO** |
| Viewer changed | **NO**; English/PT-BR, both palettes and offline behavior untouched |
| Manufacturing | **BLOCKED** |

Pending manufacturing gates include physical WPC hinge measurement, matrix confirmation, supplier profile, actual plywood thickness, tool/cutter data, final fasteners, joint/pocket clearance, dogbone strategy, nesting/orientation, tolerance/load coupon validation, resolved pivot installation, handling/retention validation, and remaining manufacturing freeze gates. This review is not certification or a manufacturing release.

## Review artifacts and reproducibility

[Validation](../../exports/generated/backbox-structure-v32/validation.json) contains 576 successful checks, including successful detection of the failed installation gate; `promotion_geometry_gates_pass` is **false**. [Independent saved-CAD regression](../../exports/generated/backbox-structure-v32/regression-validation.json) passes 635 checks including source/viewer Git-blob identity, symmetric solids, reproduced pivot obstruction and saved poses. A passing test runner must not be mistaken for promotion approval.

[Upright CAD](../../exports/generated/backbox-structure-v32/play.FCStd), [glass/matrix-removed CAD](../../exports/generated/backbox-structure-v32/matrix-removed.FCStd), [1°](../../exports/generated/backbox-structure-v32/fold-1.FCStd), [15°](../../exports/generated/backbox-structure-v32/fold-15.FCStd), [45°](../../exports/generated/backbox-structure-v32/fold-45.FCStd), [90°](../../exports/generated/backbox-structure-v32/backbox-fold.FCStd). All are isolated candidate files; none is a new CURRENT source.

| # | Actual CAD review view |
|---:|---|
| 01 | [Corrected vs superseded pivot](../../exports/generated/backbox-structure-v32/01-review.png) |
| 02 | [Side profile and inset floor](../../exports/generated/backbox-structure-v32/02-review.png) |
| 03 | [Floor/side joint](../../exports/generated/backbox-structure-v32/03-review.png) |
| 04 | [Lower-front projection](../../exports/generated/backbox-structure-v32/04-review.png) |
| 05 | [Shelf bearing](../../exports/generated/backbox-structure-v32/05-review.png) |
| 06 | [Hinge reserve / obstruction](../../exports/generated/backbox-structure-v32/06-review.png) |
| 07 | [Lock reserves](../../exports/generated/backbox-structure-v32/07-review.png) |
| 08 | [Generic passage](../../exports/generated/backbox-structure-v32/08-review.png) |
| 09 | [Toy side zones](../../exports/generated/backbox-structure-v32/09-review.png) |
| 10 | [1° wood release](../../exports/generated/backbox-structure-v32/10-review.png) |
| 11 | [15° wood pose](../../exports/generated/backbox-structure-v32/11-review.png) |
| 12 | [45° wood pose](../../exports/generated/backbox-structure-v32/12-review.png) |
| 13 | [90° wood pose](../../exports/generated/backbox-structure-v32/13-review.png) |
| 14 | [Complete upright candidate](../../exports/generated/backbox-structure-v32/14-review.png) |
| 15 | [Complete folded candidate](../../exports/generated/backbox-structure-v32/15-review.png) |

```sh
python3 tools/check_wpc_reference_v32.py
python3 tools/validate_backbox_fold_v10.py
freecadcmd tools/backbox_structure_review_v32_entry.py
freecadcmd tools/check_backbox_structure_v32.py
uv run --with matplotlib --with numpy python studies/backbox-structure-v32/render.py
```

FreeCAD 1.1.3 / OCC 7.8.1. Check the explicit PASS sentinels: FreeCAD command exit status alone can conceal a Python exception. Geometry construction owns only the new isolated output directory. Do not replay the historical generators as current production builds.

## Historical audit and sources

**SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION** applies to the old pivot analysis, old captured CAD bore at Y1270, and associated collision conclusions in the historical backbox-profile, backbox-floor, matrix-route-backbox-audit, matrix-hinge-study, side-panel and cabinet-v32 base-generation snapshots. Their numbers/images are historical evidence and were not silently rewritten. Linked source documents and scripts now carry explicit superseded banners; old configs have `active_engineering: false`. The unchanged viewer's historical geometry is not new drilling authority.

[Line-by-line pivot audit](pivot-audit.json) distinguishes active authority, historical comparisons, third-party quotations and unrelated dimensions. Negative regression controls reject the 38.1 mm rear offset/Y1270 pivot and a drifted 241.0 mm offset. The documented rear floor-fastener center at Y1270 remains legitimate and is explicitly distinguished from the pivot. The conflicting third-party 1.5-inch quotation is preserved and rejected as pivot authority, as documented in the positive control.

| Authority class | Source and use |
|---|---|
| DOCUMENTED DIMENSION | [Existing WPC source registry](../wpc-fold-v32/sources.json), including Michael J. Roberts' [Pinscape guide](https://head.pinscape-build-guide.pages.dev/), pivot/floor and hinge assembly figures. 9.5 in rear offset and 20 in height; rigid arm architecture and reference floor row. No imported upstream images/CAD. |
| MEASURED DIMENSION — CAD only | Starting HEAD matrix-cassette/playfield support solids; existing 210 mm toy zones and rear-frame joints. Bounds, volumes, contact areas and distances measured from B-reps. No physical part measurements claimed. |
| DERIVED DIMENSION | Inch conversions, Y1066.8 axis, 156.1 mm joint, 47.9 mm projection, contact percentages, CG and load demand calculations. |
| PROVISIONAL ASSUMPTION / design choice | 18 mm stock, 6 mm capture, generic passage, locks/reserves, screw envelopes, 650 kg/m³, retained payloads, 0.3g/2× screens, hand-force direction. Not manufacturing authority. |

For structural-review limits, APA's [Fastener Loads for Plywood — Screws, E830](https://www.apawood.org/guides-tools-training/technical-document-library/technical-notes/fastener-loads-for-plywood-screws/) identifies tested ultimate lateral/withdrawal loads and the need to adapt joints to fasteners/member properties. No tabulated capacity was applied to unselected local plywood. The [US Forest Service 2021 Fastenings chapter abstract](https://research.fs.usda.gov/treesearch/62253) likewise identifies grain-direction properties and moisture-related dimensional changes as connection-design inputs. Only these public landing-page summaries were inspected here; this report does not claim full PDF/code review. Accessed 2026-10-01; sources retain their own copyrights, with no third-party assets redistributed.

Original study code, geometry, prose and renders: CERN-OHL-S-2.0. [NOTICE](../../NOTICE.md). Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

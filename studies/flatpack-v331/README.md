# V33.1 flatpack manufacturing decomposition

**All 93 installed wood components were audited. They produce 130 manufacturing pieces in 66 canonical families.** All 15 previous decomposition holds have explicit planar members. The operation routes are 71 `ONE_SIDE_CNC_READY`, 59 `ONE_SIDE_CNC_PLUS_MANUAL_FINISH`, and zero unresolved operation-route blockers. These statuses describe the nominal preparation route, **not a CNC release**.

HEAD BEFORE: `a 9b16bd5e9a264c96b3be34de7bdce9308e6459b`.
HEAD AFTER: the delivery commit containing this report on `feat/cabinet-review-v32`.

[Review gallery and outputs](../../exports/generated/flatpack-v331/index.html) · [Manufacturing authority manifest](../../config/manufacturing/flatpack_v331.json) · [One-face register](../../exports/generated/flatpack-v331/manufacturing-register.json) · [EN BOM](../../exports/generated/flatpack-v331/manufacturing-wood-bom-en.md) · [PT-BR BOM](../../exports/generated/flatpack-v331/manufacturing-wood-bom-pt-BR.md) · [JSON](../../exports/generated/flatpack-v331/manufacturing-bom.json) · [CSV](../../exports/generated/flatpack-v331/manufacturing-bom.csv).

## Authority and preservation

The supplier profile is byte-identical: 2500 × 1600 sheet, 2460 × 1560 usable, 20 mm border, 15 mm spacing for ≤18 mm stock, Ø4 cutter/R2, controlled-depth pockets, one CNC face, physical coupon mandatory. No feeds, speeds, machine toolpaths, G-code, postprocessor or production full-sheet vectors are generated.

CURRENT CAD, its parameters, hardware, assembly states and viewer are untouched. Independent saved-member reconstruction gives **0 mm³ symmetric Boolean difference for all 93 installed components**. The retained wood, functional envelope, mating surfaces and pre-existing collision relationships are therefore unchanged; this is an equivalence proof, not a newly claimed motion/load certification. The existing glass/matrix removal rules, backbox fold architecture and normal lock workflow remain authoritative.

All **1,529 starting-HEAD files** remain byte-identical. Source hashes include the supplier profile. The old V33 inventory and first supplier operation register remain historical evidence. `config/manufacturing/flatpack_v331.json` points future manufacturing preparation to the new member BOM. The append-only ID map prevents silent renumbering of manufacturing families.

## The 15 decompositions

| Installed assembly | Chosen members | Reason / preserved interface |
| --- | --- | --- |
| Glass top retainer × 1 | 756 × 37 × 12 cap; 744 × 8 × 13.8 strip, reduced from 18 mm | One-sided cap plus glued strip avoids a 25.8 mm stock requirement. A single pocketed piece would require thicker stock; equal planar laminations add unnecessary layers. The 744 × 8 glue land, original fasteners, removal direction and glass capture remain. |
| Monitor stops × 2 | Profiled 38 × 28 × 18 base plus 18 × 28 × 12 cap | Broad 504 mm² face-to-face glue land; preferable to a 324 mm² edge-butt wing joint. Two mirrored base profiles, one identical cap family. Finished 30 mm envelope and adjuster surfaces remain. |
| Cassette cleats × 4 | Two 22 × 32 × 12 premium laminations each | One canonical layer family × 8. Finished 24 mm thickness, cassette location and access remain. |
| Intake baffles × 2 | Face 232 × 104 × 6; top 232 × 36 × 6; two 98 × 36 × 6 returns | Four simple panels per baffle; corresponding L/R panels identical. Square glued seams, no added internal cleat. |
| Hinge cleats × 2 | 23 × 628 × 18 stock, face-reduced 4 mm to 14 mm | Preserves the exact hinge mating plane/axis and door position. A 12 mm replacement alone would leave a 2 mm discrepancy; adding a separate 2 mm strip is less simple. No 14 mm sheet required. |
| Leg blocks × 4 | Seven actual 18 mm layers each | Exact triangular profiles and the diagonal bore intersections are extracted, indexed bottom L1 → top L7, then consolidated by exact rigid comparison. |

The new glued seams are specified as manufacturing joinery. Adhesive, clamping, actual bond-line thickness and structural qualification remain release gates. The report does not convert geometric equivalence into bond-strength certification. No custom metal or extra dense screw pattern is introduced.

The intake inlet remains **220 × 80 = 17,600 mm² per door**. The downward mouth remains **220 × 36 = 7,920 mm² per door** before mesh/filter effects. Exact union equivalence preserves the full passage, not just these two area figures. Thermal/filter performance remains unqualified.

The leg layers consolidate into **five final-geometry families**:

- `M019`: unbored triangular layer.
- `M020` and `M021`: full diagonal-bore layers at different heights relative to FACE_A.
- `M022` and `M023`: the two complementary rear upper-bore slices, across L5/L6.

Front L3/L6 contain the two bores; rear L2 contains the lower bore and rear L5/L6 share the upper bore. The current 58 mm bolt pitch remains a reference hold, including the earlier 57.15 mm historical discrepancy. It is not released drilling. The CNC blanks may share a triangular outline, but their finished layer identities, bore geometry and assembly order are not collapsed into seven fictitious identical finished pieces.

[Full member/joinery/volume table](../../exports/generated/flatpack-v331/decomposition-report.md).

## One CNC face and manual finish

Every member has a rigid local-to-installed matrix, FACE_A outward vector, finished local XY contour, stock thickness and finished thickness. Local z= 0 is **finished FACE_A**, and positive z enters the wood. Whole-face thickness reduction is performed first, then the finished-face depth datum is reset. FACE_B has **no CNC**.

The audit constructs a full local blank, subtracts the accepted B-rep, examines planar/cylindrical/conical surfaces, splits stepped axial recesses at their depth levels, and checks access from FACE_A. A planar outline alone never produces readiness. Exact face contours and removed volumes are retained as B-reps alongside numeric directions/depths.

The Ø4 reach test uses offset geometry to distinguish machinable regions from R2 residuals. The independent check confirms **0 mm³ CNC overcut** in every member. Where a corner or bore remains, the manual schedule names it rather than silently rounding away retained wood or pretending a smaller cutter exists.

Manual operations include:

- Sub-Ø4 pilots: use an ordinary drill/driver, selected pilot and depth stop. A permanentØ4 locator is **not** cut where it would enlarge the accepted pilot. Reference center marks can instead drive a removable full-size marking template.
- Countersinks: use selected countersink tooling and the recorded cone geometry. Cylinder/cone axes, entry/exit coordinates, diameter records and depth ranges are supplied.
- Edge/45° holes: use a qualified drill-angle guide and clamps; no freehand-angle accuracy is claimed. The exact entry, axis and reference length are recorded. Purchased WPC/leg dimensions must qualify the guide and bore pattern before release. Do not drill through or damage captive metal threads as a makeshift guide.
- Blind access from the non-CNC side, where retained: manual access only, with location/depth related to the same FACE_A datum. This is not permission for a second CNC setup.
- Square corner remnants: local chisel/file finish to the exact reference, or a separately validated coupon-dependent relief at an actual mating joint. No automatic dogbones.
- Three sloped crossmembers: FACE_A is reversed to give access from the smaller end profile. Sixteen conservative open-edge pocket steps, up to 1 mm depth increments, leave 942.4 mm³ per crossmember for sanding to the reference bevel. The final straight bearing plane must be checked with a straightedge/angle template; no table saw, router or planer is required.

A qualified manual guide and finish procedure still need physical validation. These are explicit, feasible operation routes with retained reference geometry; this is not a claim that unmeasured hardware can already be drilled or that hand-work accuracy is certified.

[Operation faces](../../exports/generated/flatpack-v331/operation-face-report.md) · [Manual schedule](../../exports/generated/flatpack-v331/manual-finish-schedule.md) · [Numeric manual operations](../../exports/generated/flatpack-v331/manual-finish-schedule.json).

## Corners, fits and engraving

The register distinguishes existing R2-or-larger features, open edges needing no dogbone, square mating relief candidates and fit-dependent captures. Nonmating openings do not automatically receive dogbones. Exact reference square corners remain hand-finished in this equivalence study; a future R2 simplification would need its own equivalence decision.

Wood slots/captures remain `measured_thickness_mm + selected_coupon_clearance_mm`; laminate heights use actual layer sums and dependent panel dimensions regenerate from fixed outer datums. Glass/liner captures use measured glass and liner allowances, rather than misapplying plywood thickness. Reference geometry retains nominal dimensions only to compare with CURRENT. **No 18.000 mm fit is frozen.**

Every ID has an optional engraving-map record. ENGRAVE is a separate semantic group and is disabled until a hidden position/tool/depth is confirmed. Use removable labels in the meantime, especially on small members. No visible finished face receives a mandatory mark; this update creates no engraving cut in CURRENT wood.

[Fit-dependent list](../../exports/generated/flatpack-v331/fit-dependent-joints.json) · [Purchased-hardware interfaces](../../exports/generated/flatpack-v331/hardware-interface-holds.json) · [ID map](../../exports/generated/flatpack-v331/part-id-engraving-map.json).

## Wood stock and sheet feasibility

| Nominal stock | Structural premium pieces | Secondary-eligible pieces | Total | Preliminary premium-first sheets |
| --- | ---: | ---: | ---: | ---: |
| 18 mm |87 |1 |88 |2 |
| 12 mm |14 |11 |25 |1 |
| 8 mm |0 |2 |2 |1 |
| 6 mm |0 |13 |13 |1 |
| 4 mm |2 |0 |2 |1 |
| **Total** |**103** |**27** |**130** |**6** |

The table is a **stock-family feasibility study, not a purchase recommendation**. In particular, the two 4 mm contact pads total only 432 mm² and should be considered for suitable premium offcuts rather than an entire sheet. Two 8 mm filter frames occupy 57,800 mm² of outer area. Existing 4/6/8 mm parts were not arbitrarily thickened. The supplier's 2500 × 1600 format is used as the preliminary study envelope for each group; availability and actual thickness of each non-18 mm stock group still need qualification.

All pieces fit the **2460 × 1560 mm usable rectangle**. The largest by area are the side panels `M001/M002`, **596.9 × 1308.1 mm** in local manufacturing XY, placed as 1308.1 × 596.9 with an in-plane 90° rotation. All rotations keep FACE_A up. The study assumes long-axis grain parallel to the 2500 sheet direction; veneer orientation and structural grain constraints must be confirmed before final nesting.

The descending-height row heuristic uses conservative bounding rectangles and actual contour overlays. It validates the 20 mm border and at least 15 mm finished-boundary spacing for every pair. It does not pack inside holes, claim optimization, prescribe holding tabs or release cut paths. Small strips/frames still require supplier hold-down planning. The area-only lower bounds equal the six demonstrated layout sheets across these separate stock groups, but this is not a proof of globally optimal purchasing or nesting after fit regeneration.

Premium-first policy remains: all pieces are first placed in premium stock. A reviewed secondary-stock alternative is allowed only under the existing small-subset/extra-premium-sheet rule; structural parts are never automatically downgraded.

[Sheet report](../../exports/generated/flatpack-v331/sheet-feasibility.md) · [Preliminary layout](../../exports/generated/flatpack-v331/15-review.png) · [Stock-family report](../../exports/generated/flatpack-v331/stock-thickness-families.md).

## Required hardware quantity closure

The 13 previous unknown rows were inspected against actual attachment geometry and current source code:

- **Exact integer counts newly closed:0.** No required attachment point count was found that justified filling one of these13 nulls.
- **Selected-hardware formulas:6** — F53, W06, F18, F36, F38, F39. Supplied kit contents are subtracted after verification; washers/nuts are not double-counted.
- **Genuinely TBD:7** — F06, G01, F16, F19, F22, F28, F31. These still need joint/attachment schedules or adhesive consumption data. New glue seams do not define the missing original cabinet screw schedules.

The four cassette attachment bolts do not also count as DMD/baffle screws. The source's two-screw filter comment concerns an upper fan cover and does not establish a complete lower-intake attachment count. No fake integer is substituted for selected piano-hinge hole pitch.

[Quantity-closure report](../../exports/generated/flatpack-v331/hardware-quantity-closure.md).

## Export and review package

The package includes all 16 requested CAD/2D views, saved installed and exploded wood assemblies, a complete per-instance operation register, EN/PT-BR wood BOMs, JSON/CSV, exact B-rep contours/removals, and 66 family-level **review-only** DXF/SVG drawings. Semantic groups are CUT, POCKET, LOCATOR, ENGRAVE and REFERENCE. Per-entity operation/depth bindings accompany the exports. Lines/arcs/ellipses retain vector geometry; raster atlas outlines are display tessellation only.

Only cutter-access contours appear as machining-intent groups; exact target boundaries and center references remain distinguishable. Review drawings are labelled **PRELIMINARY — NOT FOR CNC**. No production full-sheet vectors, CAM or G-code are present. Supplier CAM remains responsible for feeds, speeds, passes, tabs, entry strategy and postprocessing.

Reproduction from the worktree:

```sh
freecadcmd tools/flatpack_v331_entry.py
python3 tools/build_flatpack_v331_reports.py
freecadcmd tools/verify_flatpack_v331_entry.py
freecadcmd tools/export_flatpack_v331_review.py
uv run --with matplotlib --with numpy python studies/flatpack-v331/render.py
# Run export_flatpack_bom_v331.mjs beside the supplied runtime node_modules link.
node .work/flatpack-v331/export_flatpack_bom_v331.mjs
python3 tools/package_flatpack_v331.py
python3 tools/check_current_v32.py
```

FreeCAD may exit 0 after a Python error: require the explicit PASS sentinel and saved validation JSON. The saved-member suite includes a negative control that removes a leg layer and rejects the resulting assembly.

## Decision report

| Requested result | Outcome |
| --- | --- |
| Installed components audited |93 |
| Manufacturing pieces / canonical families |130 /66 |
| ONE_SIDE_CNC_READY |71 pieces |
| ONE_SIDE_CNC_PLUS_MANUAL_FINISH |59 pieces |
| Operation-route BLOCKED |0 |
| Original 15 decomposition holds resolved |15; none remaining |
| 18 mm premium pieces |87, plus 1 secondary-eligible PCBase |
| 12 mm pieces |25:14 structural,11 secondary-eligible |
| Other stock |8 mm × 2;6 mm × 13;4 mm × 2 |
| Required hardware unknowns before |13 |
| Exactly closed / formula-driven / truly TBD |0 /6 /7 |
| Largest part |M001/M002;596.9 × 1308.1 mm; fits YES |
| Preliminary layout |YES; six stock-family sheets; production-authorized NO |
| CURRENT design geometry changed |NO |
| Full-sheet release |**BLOCKED** |
| Coupon |**WAITING FOR PRODUCTION-LOT MATERIAL** |

Remaining release gates: actual stock thickness; physical coupon and selected clearance; regenerated fit-dependent joints; purchased hardware dimensions; manual-guide/finish, adhesive and structural/ergonomic qualification; supplier holding/CAM review and owner approval. Geometric decomposition and nominal one-sided route auditing are closed; those physical gates are not.

Original source: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

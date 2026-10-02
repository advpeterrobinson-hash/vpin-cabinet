> **SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION.** Pivot-dependent results below are historical, not active engineering. Correct WPC reference: Y1066.8/Z508, 241.3 mm from rear. See [positive control](../studies/wpc-fold-v32/README.md) and [structural integration review](../studies/backbox-structure-v32/README.md). Other historical findings retain their original scope.

# CURRENT V32 — backbox floor / glass-channel integration

HEAD BEFORE: `eeab1a73a4bedde40d676ae10b3980ae625248e9`.
HEAD AFTER: the commit containing this report; the exact resulting hash is included in the delivery report.

Upright 0° passes with the corrected floor. Reference-axis folding still fails at the first 1° sample. This change replaces only the proposed backbox floor; it does not move the backbox, glass channels, WPC axis or any accepted cabinet component. The previous [audit](MATRIX_ROUTE_BACKBOX_AUDIT_V32.md) remains the historical evidence for the rejected floor and accepted matrix route.

## Floor contour and upright clearance

| Property | Old | Corrected |
| --- | --- | --- |
| Part | BackboxFloorV14 | BackboxFloorV32 / BB-FLOOR-V32-R1 |
| Joint-resolved X extent | −78…678 mm | unchanged |
| Front Y | 1054.1 mm | 1123.5 mm |
| Rear Y | 1302.1 mm | unchanged |
| Z extent / plywood | 596.9…614.9 mm / 18 mm | unchanged |
| Plan dimensions | 756 × 248 mm | 756 × 178.6 mm |
| Minimum channel separation | penetration | 5.084878095 mm |
| Installed glass separation | penetration | 5.589937520 mm |
| Minimum planar wood ligament | 60 mm | 44.5 mm |

The contour is a straight, full-width forward-edge trim, removing a 69.4 mm strip: **52,466.4 mm² / 944,395.2 mm³**. Rear/side joint edges and both existing cable passports are unchanged. The floor remains one valid CNC-cut 18 mm plywood solid with no tongues, horns, added pockets or added hardware.

Simple symmetric corner trims were evaluated first at slopes 0.4, 0.5, 0.6, 0.7 and 1.0. They cleared the channels but retained positive intersection with the installed glass in the central span. The old full floor intersects that glass by 82,115.505920 mm³. A full-width front trim avoids this second conflict. Its 5 mm separation threshold is Y=1123.413837171 mm; rounding upward on the explicit 0.1 mm design grid selects Y=1123.5. Y=1123.4 fails the preferred 5 mm margin. This is the least-removal solution in the tested straight-front profile family, not a claim of global contour optimization.

The profile is not derived by subtracting channel solids. New corners are convex, so no new internal tool radius or dogbone is needed. The original R20 passport ends remain unchanged. A 6 mm cutter is a **DESIGN-PROVISIONAL review assumption only**; future internal radii remain parametric and subject to CNC shop confirmation.

## Load path and preserved interfaces

Upright load path: **backbox structure → backbox floor → cabinet rear shelf**. Hinges provide folding motion, not primary upright bearing.

| Measurement | Old | Corrected |
| --- | --- | --- |
| Exact floor-bottom / shelf-top contact area | 84,604.625877 mm² | 84,604.625877 mm² |
| Contact retained | — | 100% |
| Continuous front bearing width | 564 mm | 564 mm |
| Side-joint longitudinal engagement | 248 mm | 178.6 mm / 72.016129% retained |
| Passport to forward floor edge | 113.9 mm | 44.5 mm |
| Between passport openings | 60 mm | 60 mm |
| Passport to rear floor edge | 94.1 mm | 94.1 mm |

The accepted shelf starts at Y=1127.125 mm. All removed wood is ahead of it. Bearing area is the OCC face-to-face intersection, excluding the floor's two openings; it is not the shelf bounding rectangle. Full thickness and broad continuous wood remain. Area preservation alone does not certify strength or final fastener/joint performance.

**Hinge zones preserved: YES.** Existing wood is retained throughout both rear outboard bands: X−78…18 / 582…678, Y1197…1302.1, Z596.9…614.9 mm. The front of these reserves is derived from the reference-axis Y1270, the documented 110 mm packaging keepout and an additional 18 mm stock margin. None of their wood is removed. Reference floor inset remains 59.8375 mm from each backbox outer edge; cabinet/backbox widths remain 600/780 mm. Cabinet pivot remains Ø12.7, 38.1 mm forward of rear Y1308.1 and 508 mm above bottom.

The reference floor row remains Y1295.4, approximately 12.7 mm from rear exterior, with three Ø6.35 reference holes per side at 44.45 mm reference spacing. No final hole pattern is created. The joint-resolved rear edge is Y1302.1: it leaves only **3.525 mm** beyond the radius of a single reference Ø6.35 bore on that row. This inherited reference limitation is unchanged, explicitly unresolved and not accepted as manufacturing geometry. Purchased 01-9011-L/R, 02-4352 and 4322-01139-12B measurements must determine the final bracket/bushing/bolt zones and drilling.

**Upright lock zones preserved: YES.** Authoritative X120/480 mm remains. Final Y is not frozen. For the reference Ø25.4 access bore, floor and shelf edges plus an 18 mm wood margin yield a safe candidate center corridor Y1157.825…1259.4 mm. The retained floor material around that corridor gives at least **21.625 mm** beyond the candidate access bore; shelf perimeter margin is at least 18 mm. These are undrilled material reserves, not a released bolt pattern.

**Floor cable-passport zones preserved: YES.** Two existing 100 × 40 mm R20 passages remain at centers (220,1188) and (380,1188), with bounds X170…270 / 330…430 and Y1168…1208 mm. Neither opening nor surrounding wood is newly cut. The accepted current shelf has solid material below both passports; each projected passage overlaps 65,819.467106 mm³ of shelf wood. Therefore a usable matched through-route is **not confirmed**. Shelf machining is outside this task and remains unchanged; passport matching is a later interface freeze gate.

## First gate: upright 0°

| Test | Result |
| --- | --- |
| Old floor / channel overlap | 937.450518 mm³ per side; 1874.901037 mm³ total |
| New unintended positive intersection | **0 mm³** |
| Internal reconstructed wood joints | clear |
| Floor / channels | clear, minimum 5.084878095 mm |
| Wood / accepted cabinet sides and installed PLAY components | clear |
| Floor / shelf | intentional bearing contact only; zero penetration |
| Floor / installed matrix and stationary supports | clear |
| Floor / stationary matrix hardware minimum | 6.9 mm; wood seats 18 mm |
| Hinge, lock and floor passport material zones | preserved as described above |
| 0° valid | **YES**, for modeled solids |

The corrected upright CAD includes the installed glass and matrix cassette. Unlocated future reserve envelopes are not asserted to be physical structural wood. There is no new intended positive-volume overlap.

## Second gate: actual-wood fold

**0→90 performed: YES**, 91 samples at 1° increments about the unchanged reference axis. Preconditions are explicitly **GLASS REMOVED + MATRIX REMOVED**. Structural authority is the eight reconstructed source wooden solids, replacing only the floor. `PF_BackboxCheckEnvelope` is **REFERENCE ONLY**. The seven other wooden members from the accepted V14/V25/V27 reconstruction are unchanged. Missing authoritative members or unmeasured hardware are not invented.

| Classification | First sampled conflict | Parts / initial intersection |
| --- | --- | --- |
| A. Wood ↔ cabinet wood | **1°** | BackboxFloorV32 ↔ BACKBOX_BASE: **88,825.888892 mm³**; ↔ SIDE_L and SIDE_R: **3,365.071415 mm³ each** |
| B. Wood ↔ glass channels | 4° | BackboxFloorV32 ↔ CandidateGlassChannelL/R: 82.381800 mm³ each |
| C. Wood ↔ stationary matrix supports | **NOT EVALUATED** | Clear baseline prerequisite fails independently at 1° |
| D. Backglass/service reserve ↔ cabinet | 44° | BackglassServiceEnvelope ↔ both glass channels: 92.374800 mm³ each |
| E. Located DMD payload ↔ cabinet | 33° | DMD payload ↔ PF_BasePlywood: 147.355880 mm³ |
| F. Moving harness / pinch keepout | **UNVERIFIED** | No complete moving backbox harness geometry exists in the accepted source |

The DMD result covers only the located V27 190 × 55 × 90 mm payload; placement of the larger V12 450 × 80 × 230 mm future service reserve remains unconfirmed. The minimum structural distance is **0 mm**, with positive-volume interference; it is not a signed penetration-depth measurement. The first collision angle is the first sampled angle, not an exact continuous onset.

The new upright floor fixes the specified glass-channel interface. It does not establish a valid fold. No axis relocation, backbox relocation, shelf change or matrix-support correction is made. **Matrix supports introduce a new fold conflict: NOT EVALUATED**, because the baseline already fails. Views 09/10 and successful 45°/90° CAD poses are deliberately omitted: the baseline is not valid through those angles.

## Real CAD and review views

- [Corrected upright assembly](../exports/generated/backbox-floor-v32/corrected-upright.FCStd)
- [First 1° collision diagnostic](../exports/generated/backbox-floor-v32/first-bottleneck.FCStd)
- [01 old upright collision](../exports/generated/backbox-floor-v32/01-old-upright-collision.png)
- [02 corrected floor alone](../exports/generated/backbox-floor-v32/02-corrected-floor-alone.png)
- [03 old/new floor overlay](../exports/generated/backbox-floor-v32/03-old-new-floor-overlay.png)
- [04 corrected upright](../exports/generated/backbox-floor-v32/04-corrected-upright.png)
- [05 glass-channel clearance](../exports/generated/backbox-floor-v32/05-glass-channel-clearance.png)
- [06 rear-shelf bearing](../exports/generated/backbox-floor-v32/06-rear-shelf-bearing.png)
- [07 preserved hinge/lock/cable zones](../exports/generated/backbox-floor-v32/07-preserved-hinge-lock-cable-zones.png)
- [08 first fold bottleneck](../exports/generated/backbox-floor-v32/08-first-fold-bottleneck.png)

Images use actual CAD tessellation, OCC sections and exact bearing/intersection faces. The clearance section at X13 reproduces the same closest-edge Y/Z witness as the minimum at X0; the checker confirms both witness points lie on the actual floor/channel. No concept artwork or invalid fold-success views are included. Review colors are local to these images; accepted CAD materials and viewer palettes remain unchanged.

## Regression protection and regeneration

All accepted V32 systems preserved: **YES**. Geometry/configuration/artifacts for matrix cassette and its accepted 1.112788 mm route, playfield, wooden pivot, buttons/notches, fans/filters, shelves, PCBase, SSF, rear door, power/RJ45, viewer and WPC reference remain unchanged. The accepted matrix route is not rerun or optimized.

The builder records 548 pre-task engineering/artifact file hashes. The independent checker compares them with the specified starting Git blobs, reopens the saved assembly, verifies all 314 accepted component shapes and the seven other backbox wooden solids, and checks the live wooden-pivot expressions. Mutation controls reject accepted-geometry displacement, restoration of the old colliding floor, forward/downward floor displacement, false zero/fold approval, missing service prerequisites and premature matrix-support conclusions. **27 build checks + 1457 independent regression checks passed**; their fold result is explicitly BLOCKED, not a false motion pass.

Authoritative new parameters: [config](../config/backbox_floor_v32.json). Source files own only the new output directory and can be rerun from the repository root:

```sh
freecadcmd tools/backbox_floor_v32_entry.py
freecadcmd tools/check_backbox_floor_v32.py
uv run --with numpy --with matplotlib python tools/render_backbox_floor_v32.py
```

Require explicit `BACKBOX_FLOOR_PASS`, `BACKBOX_FLOOR_REGRESSION_PASS` and eight `BACKBOX_FLOOR_IMAGE_PASS` markers; FreeCAD process exit status alone is insufficient. Detailed [geometry report](../exports/generated/backbox-floor-v32/validation.json), [regression report](../exports/generated/backbox-floor-v32/regression-validation.json) and [image manifest](../exports/generated/backbox-floor-v32/review-images.json) accompany the CAD.

## Manufacturing

**BLOCKED**, pending purchased WPC hinge measurement, actual matrix hardware confirmation, CNC shop tool/tolerance parameters and remaining manufacturing freeze gates. The unresolved reference-axis fold, matched cable-passport interface, measured hinge/lock drilling and structural qualification remain gates. No intermediate cabinet prototype is assumed. This is a floor integration review, not final hinge CNC release or structural certification.

Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet. Preserve repository LICENSE and NOTICE.md.

# WPC pivot / wooden playfield cradle integration — CURRENT V32

**Selected and promoted:** a broad open relief at the rear-upper corner of each cradle, providing an **R12 coaxial reserve plus 2 mm clearance**, with a straight top at **Z494** and a **convex R3 corner**. No pivot, dowel, TV, base, VESA, strap, screw or shelf was moved. No extra part was added. The complete combined model passes the defined geometry gates; physical hardware fit remains provisional.

HEAD BEFORE: `ca56e7f98f119a99c6a5a28f4a903a3b6c95b997`.
HEAD AFTER: the commit containing this report (`git log -1 --format=%H -- studies/pivot-cradle-integration-v32/README.md`); the final delivery records its pushed hash.
Branch: `feat/cabinet-review-v32`. Review completed 2026-10-02. **MANUFACTURING BLOCKED.**

[Current source manifest](../../config/current_v32.json) · [Parameters](../../config/pivot_cradle_integration_v32.json) · [Current offline viewer](../../exports/generated/viewer-v32/index.html) · [Combined validation](../../exports/generated/pivot-cradle-integration-v32/validation.json).

## Exact original conflict

Measurements are from CURRENT starting-head B-reps, not scaled pictures or physical purchased parts. X remains the transverse direction; dimensions below are Y/Z unless otherwise stated.

| Quantity | CAD measurement |
|---|---:|
| WPC pivot | Y1066.8 / Z508.0 |
| Wooden dowel axis | Y1035.25061984718 / Z484.220330114907 |
| Axis separation | **39.507418 mm** |
| Dowel seat-circle center | Y1035.25061984718 / Z484.720330114907 |
| Seat radius | 16.5 mm, for Ø32 dowel with 0.5 mm nominal radial clearance |
| WPC axis to original loaded lower semicircle | **27.720514 mm** |
| WPC axis to vertical rear seat-opening wall | **15.049380 mm** |
| WPC axis to cradle rear edge | **8.450620 mm** |
| WPC axis to original cradle top | **6.220330 mm** |
| Original front seat wall / rear seat wall at seat-center height | **8.250620 / 23.500000 mm** |
| Original upper front ear width, above Z489.4801 | 23.5 mm — not the narrower wall at seat height |

The intersection is in the **rear-upper ear**, above the loaded seat. The old R4.7625 × 3 mm internal diagnostic probe overlapped each support by 213.7672 mm³. It has zero penetration after relief. The [section through both axes](../../exports/generated/pivot-cradle-integration-v32/02-review.png) distinguishes the dowel center from the 0.5 mm higher seat-circle center.

## Local profile and radius study

A small circular notch opening toward the top/rear can retain an unnecessarily thin upper ear. We instead remove the whole upper portion of that rear ear with **one straight top trim**, opening into the existing U mouth and through the rear edge. Its seat-side exterior corner is rounded R3. This is a simple CNC profile with no closed hole, copied hinge silhouette, finger or extra moving joint.

The coaxial study radius is a **packaging parameter, not a hole radius**. For reserve radius `R`, the broad trim is `Z = 508 − R − 2`; the convex R3 corner starts 3 mm below that level. The full stock thickness remains 18 mm. The largest tested radius satisfying the conservative geometry screen is **R12**. This is not a claim that R15 necessarily fractures; it fails the explicit retained-guidance margins below.

Screening decisions, established before selection: retain the full 180° lower seat, retain the existing ≥8 mm main seat web, leave ≥8 mm rear top height above the seat-circle center and ≥5 mm straight rear guide below the R3 rounding. These are engineering geometry margins, not wood-code allowables. They preserve guidance in addition to merely leaving the part as one solid. R12 gives 9.2797 mm top height and 6.2797 mm straight guide. All seven profiles remain valid, single CNC solids; solid validity alone is insufficient.

| Reserve | Local geometry | Minimum local ligament¹ | Rear top / straight guide above seat | Shared R12 tool corridor with 2 mm margin² | Decision |
|---:|---|---:|---:|---|---|
| R5 | PASS | 8.2506 mm | 16.2797 / 13.2797 mm | FAIL: tool penetrates cradle; R8 bushing and R10 hardware also interfere | Not selected |
| R8 | PASS | 8.2506 mm | 13.2797 / 10.2797 mm | FAIL: tool penetrates cradle; R10 hardware tangent | Not selected |
| R10 | PASS | 8.2506 mm | 11.2797 / 8.2797 mm | FAIL: tool tangent, zero margin | Not selected |
| **R12** | **PASS** | **6.2797 mm** | **9.2797 / 6.2797 mm** | **PASS: 2 mm** | **SELECTED** |
| R15 | FAIL | 3.2797 mm | 6.2797 / 3.2797 mm | Not advanced after geometry failure | Insufficient rear guidance/top margin |
| R18 | FAIL | 0.2797 mm | 3.2797 / 0.2797 mm | Not advanced after geometry failure | Almost no straight rear guide |
| R22 | FAIL | 0 mm | −0.7203 / −3.7203 mm | Not advanced after geometry failure | Cuts the loaded seat; wrap reduced to 177.4979° |

¹ Defined as the smaller of the unchanged 8.2506 mm front load-path web and the exact distance from the original loaded seat surface to the removed relief wood. It is **6.2797 mm locally at the rear seat end** for R12; do not incorrectly report 8.2506 mm as the new overall minimum. The main below-seat load path still has its original 8.2506 mm minimum web.

² All radii clear *their own* coaxial reserve by 2 mm. The separate R12 tool comparison tests a useful common installation corridor; it does not assume that a tiny bolt clearance proves nut/socket access. R5/R8/R10 are passing local wood studies, but **fail the complete selected hardware/tool packaging gate**. The requested R5/R10/R15 review images are diagnostic sections and explicitly not selected-success views.

[All radius results](../../exports/generated/pivot-cradle-integration-v32/radius-study.json) · [Exact local-ligament metrology](../../exports/generated/pivot-cradle-integration-v32/cradle-metrology.json).

## Cradle function and structural screen

The selected relief preserves **all 933.0530 mm² of the original R16.5 cylindrical seat surface per support**, and **180° wrap before / 180° after**. The model retains the 0.5 mm nominal radial clearance and existing gravity seating. The seat center remains 0.5 mm above the dowel center so the dowel rests on the bottom of the larger-radius seat; there is no added bearing or steel shaft.

The front and rear walls at seat height remain 8.2506 and 23.5 mm respectively. The 33 mm throat remains unchanged up to Z491, including 6.2797 mm above the seat-circle center. Through the convex rounding it widens from 33 to 36 mm by Z494, then is fully open toward the rear. That widening does not remove the lower semicircular bearing. Lateral guidance by the two 18 mm support plates and existing dowel/strap placement remains unchanged. The retained front ear is still the highest point at Z514.22033, so **48 mm lift-out still clears it by 2 mm**; the minimum vertical unseat height remains 46 mm.

The rear ear is shortened into a broad 23.5 mm-wide wall, not left as a slender vertical sliver. The R3 rounding removes a sharp exterior tip; the loaded internal seat remains R16.5, without a new sharp internal CNC corner. The rear guide height is the limiting local margin; it must not carry arbitrary new attachments. No extra rail, cleat, spacer, bracket or metal reinforcement is required by this geometry screen.

**The entire support volume below Z484.72033 is unchanged**, verified by exact Boolean comparison. Thus the dowel-seat-to-floor stem, its lower transitions, all screw ligaments and the floor foot are unchanged. Local ear stiffness is reduced where material was intentionally removed; no FEA or stiffness/load certification is claimed. Stress concentration, plywood ply quality, moisture, actual stock and fastening performance remain manufacturing qualification items.

The floor bearing remains **58.250620 × 18 = 1,048.511157 mm² per support**. Side-to-cabinet contact decreases from **27,170.3495 to 26,693.2404 mm²**, retaining **98.2440%**. Removed wood is 8,587.9651 mm³ per support. These contact areas are geometric evidence, not allowable load ratings.

Load path remains: playfield/dowel → lower semicircular seat → continuous plywood stem → cabinet floor. Side screws retain tipping, separation and longitudinal position; they are not reassigned the primary vertical load.

## Six screws and access

All six screw solids, coordinates, cabinet-side pilot geometry and cradle countersinks remain unchanged. There are still exactly four commodity saddle straps and eight strap screws; all their geometry is unchanged as well.

| Row, both sides | Y mm | Z mm | Actual relief-to-screw-solid gap |
|---|---:|---:|---:|
| Lower | 1037.000000 | 192.000000 | 294.8636 mm |
| Middle | 1042.500000 | 320.110165 | 166.6400 mm |
| Upper | 1055.250620 | 448.220330 | **38.4226 mm** |

Head positions are X36 left / X564 right; existing candidate tips X6 / X594. The 4.5 × 30 mm screw remains a candidate pending purchased-fastener and plywood confirmation. Six existing R8 × 150 mm interior driver corridors remain clear. No screws were added, shifted or used to compensate for the relief.

## Separate WPC hardware and tool corridors

These are independent **PROVISIONAL packaging envelopes**, not dimensions asserted for purchased parts:

| Function | Radial envelope | Axial reach from inside cabinet wall |
|---|---:|---:|
| Axis clearance | R5 | reference axis corridor |
| Bushing body/flange allowance | R8 | 10 mm inward |
| Nut/washer/bolt-end allowance | R10 | 24 mm inward, to X42 / X558 |
| Installation tool | R12 | through the 18 mm cradle, then 150 mm inward, to X186 / X414 |

The relief gives the installed R10 envelope 4 mm clearance from its flat top and the R12 tool corridor **2 mm minimum modeled clearance**. The actual tool corridor is checked starting at the inner cabinet wall, not merely at the cradle's inner face. The unchanged backbox floor-bolt/arm arrangement and physical parts still need measurement.

**Access sequence:** remove glass and matrix, lift the accepted complete playfield unit 48 mm and remove it for hinge installation/service. The tool cylinder is clear at the 48 mm pose and remains clear with the unit absent. It is obstructed by the base/straps in the closed state, and by the base at 50° service; do not claim routine pivot-tool access in either of those states. This uses the existing lift-out architecture; no new support or permanent mechanism is added.

This access requirement is for WPC hardware installation/service. Normal backbox folding uses the playfield closed, with glass and matrix removed. The study does not authorize simultaneous raised-playfield/backbox-fold operation.

The cabinet-side WPC hole is **not enlarged or newly drilled**. Promotion adopts the previous candidate's removal of the superseded old reference bore, but generates no replacement hardware hole or final pattern. Exact bushing bore, flange, retention stack, bolt length, socket clearance and hole location relative to the purchased arms remain manufacturing holds.

## Combined motion checks

**Playfield closed: YES. Service 0→50°: YES. Vertical lift-out 48 mm: YES. Backbox 0→90°: YES, reconstructed wood and provisional hardware corridors.** Glass/matrix removal remains explicit in CAD states and viewer. The Ø32 wooden dowel and all moving playfield components are unchanged. Fallback B/C were unnecessary and were not studied.

The engine is the same FreeCAD 1.1.3 / OCC 7.8.1 exact B-rep common-volume/distance engine used in the validated WPC positive control. Checks include cabinet sides, floor, shelves, SSF exciters, crossmember guides, matrix fixed supports, backbox wood, occupied display/VESA envelopes and the provisional hinge corridors. Reserved electronics space is not silently substituted for physical wood. Designed seat, cabinet-side and floor-face contacts are distinguished from penetration.

- All four locally viable relief candidates receive the playfield service/lift checks; each larger relief is also verified as a strict material subtraction from R5. None can introduce a new cradle collision into a previously clear pose.
- Selected combined model: **105 playfield service samples** (0.5° plus finer early angles), **54 lift samples** (1 mm plus finer initial steps), and **97 backbox samples**, including all requested angles and early 0.001/0.01/0.05/0.1° samples.
- Continuous new-interface certificates: **64 intervals** for playfield rotation, **4** for lift translation, **17** for added occupied volumes during backbox folding, and **1** for exterior arm corridors against genuinely outboard fixed parts.
- The existing **116-interval backbox wood certificate** is inherited exactly: backbox wood and all other fixed geometry are unchanged, while the cradles are strictly reduced. The analytical initial shelf-release proof is unchanged. Exterior arms remain outside the cabinet's true X planes; exact outside-volume checks handle conservative trimmed-surface bounding boxes correctly. These reference envelopes do not certify an unmeasured purchased hinge sweep.
- Baseline playfield/cabinet interfaces retain their previous authority and are resampled here; the continuous certificates specifically prove the **changed/added interfaces**. This is not a new structural certification of the entire playfield system.

No unintended penetration is found. The floor releases from the shelf at 0°+; retained upright shelf bearing stays **65,672.4 mm²**. The 210 mm side profile, Y1146 floor, rear shelf and generic cable passage are unchanged from the validated proposal. The backbox-axis datum remains Y1066.8/Z508, pure rotation. Overall clearance still includes zero at intentional bearing; smallest sampled glass-channel gap remains **5.1179 mm at 90°**.

## Promotion and required report

| Requested field | Result |
|---|---|
| Selected relief | **R12 reserve + 2 mm allowance; straight rear-ear top Z494 with convex R3 corner** |
| Dowel seat preserved | **YES** |
| Seat wrap, before / after | **180° / 180°** |
| Minimum remaining local ligament | **6.2797 mm**, rear seat end to relief; original main web **8.2506 mm** |
| Floor-bearing path preserved | **YES**, complete below-seat volume unchanged |
| Six support screw coordinates preserved | **YES** |
| Playfield closed / service / lift-out | **YES / YES / YES** |
| 210 mm backbox architecture retained | **YES** |
| Backbox 0→90° fold valid | **YES**, modeled wood and provisional corridors |
| Hinge installation reserve | **PROVISIONAL**, modeled packaging PASS; tool access requires lift-out/removal |
| Custom metal added | **0** |
| Combined architecture promoted | **YES**, CURRENT design candidate |
| Generic cable passage | **Preserved unchanged**, builder-configurable termination/disconnection |
| Final hinge drilling frozen | **NO** |
| Manufacturing | **BLOCKED** |

Promotion replaces only `PF_OpenCradleL/R` relative to the previously validated combined candidate, and adopts that candidate's WPC datum, 210 mm backbox, Y1146 floor and generic passage. The previous matrix-cassette and backbox-structure snapshots remain byte-for-byte historical inputs. The current manifest and viewer now point at `exports/generated/pivot-cradle-integration-v32/`. All existing viewer controls, English default, PT-BR toggle, Original/Accessible palettes and offline operation are preserved; fold-status text is updated to match the new geometry and hardware hold.

Physical measurements still required: **01-9011-L/R, 02-4352, 4322-01139-12B, actual plywood and selected fasteners**. Specifically measure the actual bushing/flange dimensions and internal projection; arm thickness/bends and hole offsets; bolt neck, length, nut/washer stack; required socket/wrench swept access; dowel diameter/straightness and purchased saddle straps. If actual parts exceed the reserve, reevaluate the relief parameter and its guidance margins before CNC; never move the accepted WPC axis to hide a hardware mismatch.

Other manufacturing gates remain: matrix confirmation, CNC supplier profile, stock/tool data, fit and corner-relief strategy, nesting/orientation, final fasteners, tolerance/load coupons and owner manufacturing approval. No manufacturing release is implied by promotion.

## CAD review package and validation

[Current upright CAD](../../exports/generated/pivot-cradle-integration-v32/play.FCStd) · [Playfield 50°](../../exports/generated/pivot-cradle-integration-v32/playfield-service.FCStd) · [Lift-out 48 mm](../../exports/generated/pivot-cradle-integration-v32/lift-out.FCStd) · [Backbox 90°](../../exports/generated/pivot-cradle-integration-v32/backbox-fold.FCStd).

| # | Actual CAD view |
|---:|---|
| 01 | [Original cradle/pivot collision](../../exports/generated/pivot-cradle-integration-v32/01-review.png) |
| 02 | [Section through both axes](../../exports/generated/pivot-cradle-integration-v32/02-review.png) |
| 03 | [Original cradle profile](../../exports/generated/pivot-cradle-integration-v32/03-review.png) |
| 04 | [R5 diagnostic relief](../../exports/generated/pivot-cradle-integration-v32/04-review.png) |
| 05 | [R10 diagnostic relief](../../exports/generated/pivot-cradle-integration-v32/05-review.png) |
| 06 | [R15 rejected diagnostic profile](../../exports/generated/pivot-cradle-integration-v32/06-review.png) |
| 07 | [Largest viable R12 relief](../../exports/generated/pivot-cradle-integration-v32/07-review.png) |
| 08 | [Seat ligament close-up](../../exports/generated/pivot-cradle-integration-v32/08-review.png) |
| 09 | [WPC hardware/tool corridor](../../exports/generated/pivot-cradle-integration-v32/09-review.png) |
| 10 | [Six support screw relationship](../../exports/generated/pivot-cradle-integration-v32/10-review.png) |
| 11 | [Floor load path](../../exports/generated/pivot-cradle-integration-v32/11-review.png) |
| 12 | [Playfield closed](../../exports/generated/pivot-cradle-integration-v32/12-review.png) |
| 13 | [Playfield 50° service](../../exports/generated/pivot-cradle-integration-v32/13-review.png) |
| 14 | [48 mm lift-out](../../exports/generated/pivot-cradle-integration-v32/14-review.png) |
| 15 | [Backbox early fold](../../exports/generated/pivot-cradle-integration-v32/15-review.png) |
| 16 | [Backbox 45°](../../exports/generated/pivot-cradle-integration-v32/16-review.png) |
| 17 | [Backbox 90°](../../exports/generated/pivot-cradle-integration-v32/17-review.png) |
| 18 | [Final combined architecture](../../exports/generated/pivot-cradle-integration-v32/18-review.png) |

The combined generator passes **387 checks**. [Independent saved-CAD regression](../../exports/generated/pivot-cradle-integration-v32/regression-validation.json) passes **3,815 checks**, including historical-source Git-blob identity, unchanged components in every established pose, mirrored reliefs, whole seat retention, reproduced clear pivot probes and rigid fold poses. [Viewer regression](../../exports/generated/pivot-cradle-integration-v32/viewer-validation.json) checks actual offline WebGL startup, all states, mandatory removal prerequisites, geometry preservation across both languages/palettes, selection and visible fold status. R22 provides a negative control that actually removes part of the seat; R10 demonstrates why zero tool clearance is insufficient.

```sh
freecadcmd tools/pivot_cradle_screen_v32_entry.py
freecadcmd tools/pivot_cradle_integration_v32_entry.py
freecadcmd tools/measure_pivot_cradle_v32.py
freecadcmd tools/check_pivot_cradle_integration_v32.py
freecadcmd tools/check_cradle_adjacent_access_v32.py
python3 tools/build_review_viewer.py
python3 tools/check_pivot_cradle_viewer_v32.py
python3 tools/check_current_v32.py
uv run --with matplotlib --with numpy python studies/pivot-cradle-integration-v32/render.py
```

The [adjacent-access check](../../exports/generated/pivot-cradle-integration-v32/adjacent-access-validation.json) also confirms all six screw drivers clear the provisional WPC hardware, and 275 existing matrix-rock/forward/lift route samples clear the promoted backbox/cradle wood. The matrix mechanism and its route were not redesigned.

Require the explicit PASS/DONE sentinels; FreeCAD process exit status alone can hide Python exceptions. The builders only own the new output directory. Historical generators are not current build entry points.

Sources are existing repository B-reps/configuration and the [validated WPC source register](../wpc-fold-v32/sources.json). WPC datums are **DOCUMENTED/DERIVED** reference dimensions; support bounds, areas and distances are **MEASURED FROM CAD**, not physical measurements. The relief policy, hardware envelopes and guidance thresholds are **EXPLICIT PROVISIONAL DESIGN DECISIONS**. No external CAD, vendor images or proprietary hole patterns were imported. The existing [structural-review qualification limits](../backbox-structure-v32/README.md) remain applicable.

Original source, geometry and images: CERN-OHL-S-2.0. [NOTICE](../../NOTICE.md). Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

# CURRENT V32 — matrix margin and backbox zero-state audit

HEAD BEFORE: `b4c618033805aea5cc53959a314cf77e8fb083c9`.
HEAD AFTER: the commit containing this audit; exact hash reported with delivery.

**No accepted geometry changed.** Small route refinements did not achieve 3 mm, so the accepted route is retained. The reconstructed backbox fails its 0° cabinet-interface test; the fold sweep is deliberately stopped. Requested 45°/90° images are static CAD illustrations, explicitly not validated fold states.

## Matrix route

| Field | Result |
|---|---:|
| Old minimum unintended-obstacle clearance | 1.112788 mm |
| New minimum unintended-obstacle clearance | 1.112788 mm — unchanged |
| Target / preferred margin | 3 / 5 mm — not achieved |
| Manual forward rock / forward travel / final lift | 26° / 68 mm / 100 mm |
| Installed gap / absolute tilt | 35.142373 mm / 25° |
| Minimum sampled visibility | 75% — unchanged |
| Carrier Y / Z adjustment | 0 / 0 mm |
| Architecture changed | NO |
| Locating supports / service retainers | 2 wood supports / 2 M4 retainers — unchanged |
| Custom metal | 0 |

Prerequisites remain glass removed, two retainers released, harness disconnected. Existing validation sampled every 0.25° and 1 mm, 275 poses. Those saved CAD states, validation records and viewer bytes remain identical to the accepted HEAD. The old 1 mm review target does not satisfy the new 3 mm requirement.

The two competing constraints are:

1. At the end of the 26° rock, the panel surface is **1.112788 mm** from the backbox floor's lower front edge. Replacing the coarse box with the reconstructed floor reproduces this distance: this particular bottleneck is not an empty-cavity false positive.
2. After 68 mm forward travel, the carrier is **1.120356 mm** from `PLAYFIELD_ENVELOPE`. At 69 mm travel this decreases to **1.102904 mm**. More forward travel cannot improve the earlier rock-phase minimum. Raising the carrier trades lower clearance for upper clearance; lowering reverses that trade.

The backbox underside is Z596.9, while the playfield-envelope maximum is Z574.612680. This 22.287320 mm interval accommodates an approximately 20 mm carrier/panel stack. This explains the bottleneck; it is not an alternative exact swept-volume calculation.

The ordered search below measures **upper bounds** on complete-route clearance at required intermediate poses. Failure at either pose rejects a candidate without pretending that all other obstacles, locating features or visibility pass.

| Stage | Tested changes | Cases | Best sampled upper bound |
|---|---|---:|---:|
| 1 — forward only | 68, 69, 70, 72, 75, 80, 90, 100 mm | 8 | 1.112788 mm |
| 2 — Z only | −5…+5 mm every 0.25 mm | 41 | 1.112788 mm |
| 3 — Y with Z | Y−10…+10 mm every 2 mm; same Z range | 451 | 1.102904 mm |
| 4 — rock with Y/Z | 22…30° every 0.5°; same Y/Z ranges | 7,667 | 1.102904 mm |

Stages 3–4 derive forward travel from actual rotated cassette bounds: at least 68 mm and enough to put the rear bound at least 3 mm ahead of the backbox front plane. Every longer straight translation passes this sampled position. The stages overlap; they are not 8,167 unique designs. All samples are in `route-screen.json`.

**This bounded grid is not an impossibility proof for every continuous or newly invented compound path.** No sampled small change justifies altering the approved seats, retention or location. Reaching 3 mm requires investigation beyond these small refinements, potentially involving available packaging or the provisional panel stack. None is applied. The owner's explicit fallback—retain the accepted route and explain—is used.

## Backbox reconstruction and authority

Accepted V32 contains `PF_BackboxCheckEnvelope`, not an integrated detailed wooden backbox. Available documented members were reconstructed in an isolated document from:

- `build_structure_v14.py` / `structure_geometry_v14.json`: floor, two sides, top, four fixed rear-frame strips; already 600 mm cabinet / 780 mm backbox.
- The **backbox-only** existing recipe in `detail_structure_v25.py`: nominal 18 mm stock / 6 mm captures. It resolves 12 nominal overlapping joint pairs with 24 existing profile/rebate operations. No new joint design or manufacturing release.
- `owner_features_v27.py`: existing backbox cable passages and rear-frame cuts. No accepted cabinet rear fans, shelf or other cabinet machining is rebuilt.
- `owner_services_v27.json`: separately located backglass/DMD reserves and removable front speaker carrier plates; their material is unconfirmed, so they are not asserted to be fixed structural wood.

No fixed front structural wood is defined. The located V27 DMD payload is **190 × 55 × 90 mm XYZ**; V12's future DMD service requirement is **450 × 80 × 230 mm XYZ** with no confirmed placement. Neither a new placement nor missing front structure is invented. The source reconstruction exposes the zero-state defect but is not a complete current manufacturing assembly.

## Unchanged datum

600 mm cabinet; 780 mm backbox; outer-edge inset **59.8375 mm**. Reference axis **(300, 1270, 508) mm**; Ø12.7 reference hole; **38.1 mm** forward from Y1308.1 rear exterior; **508 mm** above cabinet bottom.

The source backbox is rear-flush, with floor underside Z596.9 matching the accepted rear-shelf top. Positive +X rotation moves the top forward (−Y), independently verified. Source outer datums match the upright coarse box. No evidence of 580 mm width, mirrored fold sign, extra translation or wrong zero transform was found. The accepted datum is not changed to clear a packaging conflict.

## Exact 0° failure and root cause

Internal reconstructed **wood ↔ wood**: clear after existing joints. **Wood ↔ accepted cabinet interface**: FAIL at 0°.

| Source member | Accepted object | Intersection volume | XYZ intersection bounds, mm |
|---|---|---:|---|
| `BackboxFloorV14` | `CandidateGlassChannelL` | 937.450518 mm³ | X0…18; Y1063.187781…1118.338155; Z596.9…606.246801 |
| `BackboxFloorV14` | `CandidateGlassChannelR` | 937.450518 mm³ | X582…600; same Y/Z bounds |

Joint-resolved floor bounds: X−78…678, Y1054.1…1302.1, Z596.9…614.9. The old full-depth floor projects forward of rear-shelf edge Y1127.125 into the accepted sloping channels. Intersection vertical extent is **9.346801 mm**, not a claimed minimum separating translation. Glass and cassette are explicitly removed; stationary channels remain. Channel material is not confirmed, so this is **wood ↔ physical modeled channel**, not an asserted strictly wood-to-wood collision.

Classification:

- **B:** the solid coarse box includes empty interior and mixes structure/service space. It is **not valid as sole structural collision authority**. Its upright channel overlap nevertheless survives reconstruction of the floor.
- **E:** pre-V32 full-depth floor packaging was never integrated with the current glass/channel interface. The stale assumption is mixed-stage geometry, not 580 mm cabinet width.
- **F:** the source floor and current channels cannot coexist at 0°; the intended floor/front/channel relationship remains unresolved. No accepted part is moved, trimmed or hidden.
- **A:** no unresolved internal wood joints; strict wood-to-wood classification is unproved because channel material is unconfirmed.
- **C / D:** no reference-axis or zero-orientation error demonstrated.

## Fold gate: separate results

The owner's B3 stop rule applies. **No 0→90° sweep is performed.** The maximum permitted increment remains 1° once a valid starting assembly exists. No first later collision angle is invented.

| Category | 0° | Fold result |
|---|---|---|
| Wood ↔ wood | No internal overlap | NOT EVALUATED |
| Wood ↔ cabinet | Floor/channel interference | STOPPED AT 0° |
| Backglass service envelope ↔ cabinet | Located 740 × 100 × 450 reserve clear | NOT EVALUATED |
| Located DMD payload ↔ cabinet | Source payload clear | NOT EVALUATED; larger future reserve location unresolved |
| Harness ↔ hinge/pinch zone | Complete moving harness absent | UNVERIFIED |
| Stationary matrix parts ↔ backbox wood | No overlap; **6.9 mm** minimum at fixed screw tips | Added fold conflict UNDETERMINED without valid baseline |

The documented backbox harness requirements—250 mm loop, R50 bend, 40 mm pinch keep-out—are not replaced by an invented cable route or a clearance PASS. The existing two matrix seats and fixed hardware are unchanged. No valid baseline exists for a YES/NO judgment about new support conflicts during folding.

**0° actual wood assembly valid: NO** for the available source reconstruction against current cabinet interfaces. Complete integrated V32 authority remains absent. **Wood fold 0–90 clear: NOT VALIDATED.** First physical wood-to-cabinet interface collision: **0°**. First strictly wood-to-wood fold collision: **undetermined**. Display/service fold collision and angle: **undetermined**.

Physical **01-9011-L/R, 02-4352, 4322-01139-12B** measurements remain required. This is wood packaging/reference-axis diagnosis, never final hinge CNC release.

## Preservation / reproducibility

**All accepted V32 systems preserved: YES.** Playfield/notches; button XYZ; dowel/cradles/screws/48 mm lift-out; floor/rear fans and filters; shelves; PCBase; SSF; rear door; power/RJ45; matrix architecture/retention/location; hinge datum; viewer bilingual text, palettes and selection cues. Accepted geometry and viewer files remain byte-identical.

35 build assertions and 120 independent regression checks pass. Saved-CAD checks reproduce the channel intersections and verify all wood-joint pairs. Accepted input bytes are compared with the requested HEAD. Negative controls reject fabricated fold-clear claims with invalid 0°, detect a 0.1 mm geometry mutation, and demonstrate a point inside the coarse box but outside all wood. These passing checks establish reproducibility, **not achievement of route margin or fold clearance**.

```sh
freecadcmd tools/matrix_route_backbox_audit_v32_entry.py
freecadcmd tools/check_matrix_route_backbox_audit_v32.py
uv run --with matplotlib python tools/render_matrix_route_backbox_audit_v32.py
```

Require `ROUTE_BACKBOX_AUDIT_PASS`, `ROUTE_BACKBOX_REGRESSION_PASS` and eight `ROUTE_BACKBOX_IMAGE_PASS` markers; FreeCAD's wrapper can exit zero after an exception. Outputs are isolated in `exports/generated/matrix-route-backbox-audit-v32/`. Intersection fragments may contain multiple valid solids; each reconstructed wood member is one valid solid.

## Eight real CAD views

1. [Upright reconstructed wood](../exports/generated/matrix-route-backbox-audit-v32/01-upright-actual-backbox-wood.png)
2. [Coarse comparison](../exports/generated/matrix-route-backbox-audit-v32/02-coarse-envelope-comparison.png)
3. [Pivot datum](../exports/generated/matrix-route-backbox-audit-v32/03-pivot-datum-close-up.png)
4. [First real problem — 0°](../exports/generated/matrix-route-backbox-audit-v32/04-first-real-interface-problem.png)
5. [45° static diagnostic — NOT VALIDATED](../exports/generated/matrix-route-backbox-audit-v32/05-45-degree-diagnostic.png)
6. [90° static diagnostic — NOT VALIDATED](../exports/generated/matrix-route-backbox-audit-v32/06-90-degree-diagnostic.png)
7. [Display/service volumes separate](../exports/generated/matrix-route-backbox-audit-v32/07-display-separated-from-wood.png)
8. [Stationary matrix supports — zero only](../exports/generated/matrix-route-backbox-audit-v32/08-stationary-matrix-supports-zero-only.png)

Sections are actual OCC plane slices; 3D views are tessellated CAD. Separate 45°/90° documents carry explicit invalid-zero warnings and are not installed as accepted viewer states. View 08 is a zero-only comparison because a validated fold baseline is unavailable.

**MANUFACTURING: BLOCKED** by insufficient route tolerance, unresolved backbox zero-state integration, actual matrix hardware/WPC hinge measurement, CNC shop parameters and remaining freeze gates. No unrelated geometry or thermal analysis is changed.

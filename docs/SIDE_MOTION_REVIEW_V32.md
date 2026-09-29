# V32 continuous removal study

[Português (Brasil)](pt-BR/SIDE_MOTION_REVIEW_V32.md)

**Ten candidate routes clear; six direct-lift controls obstructed. No permanent geometry changed. CNC BLOCKED.** This advances the [guide-tool screen](SIDE_SERVICE_REVIEW_V32.md) from checking removed states to checking actual straight translation paths through the modeled cabinet.

![Shelf service routes](../exports/generated/side-panel-v32/04-shelf-service-routes.png)

## Functional result

T1/T2/T3 can move vertically out of their existing guides after the display envelope, monitor rails and bridge have been removed. Each crossmember was checked separately with the other two retained. All three collide with the monitor assembly when that prerequisite is omitted.

The three shelves cannot simply rise from their installed positions. They can translate horizontally into a clear bay, then rise, with the guides, shelf supports, other shelves, front door hardware and current low PC geometry retained. Neither shortening shelves nor recutting the shell is needed for these candidate paths.

| Shelf | Direct-rise obstruction in the modeled scene | Candidate horizontal move | Then vertical move |
|---|---|---|---|
| S1 | Stationary audio body, candidate side buttons at Y255, current plunger reservation | Rearward 310 mm: leading edge Y120 → Y430 | 446.9 mm |
| S2 | T2 guides and support angles | Forward 170 mm: Y600 → Y430 | 426.9 mm |
| S3 | BBBase | Forward 320 mm: Y1080 → Y760 | 366.9 mm |

Positive Y is rearward. All vertical moves end with the bottom of the shelf at Z606.9, 10 mm above the highest retained modeled solid; these are study endpoints, not instructions for how high a person should lift. S1 and S2 use the same bay **one at a time**. All three shelf paths assume the monitor assembly and T1/T2/T3 removed; shelf supports and guides stay installed. Other shelves remain in their normal positions.

The second set of shelf routes includes a **560 × 150 × 60 mm candidate equipment envelope above each 12 mm shelf board**. All three envelopes are present, but only the selected shelf and its payload move. The existing StarTech body is inside S1's candidate envelope and moves with S1 in this case. Each loaded route remains clear. “Loaded” here means geometric occupancy, **not a mass rating**; mounts, components and restrained wires must all fit that envelope. Higher components require another check. External cables need disconnection before translation, and equipment requires positive retention.

## Scene and method

The study reads the original V32 and the saved closed optional-coin-upgrade front study. All 43 original shapes other than Front and the superseded plunger marker are compared for equality. Door components come from the saved front study. The larger plunger box comes from the current front configuration; the obsolete Z250 marker and retired full-door inward prism are not used. Front-button and side-button reservations are included as explicit candidates.

For each moving planar solid, the algorithm unions its start/end positions with every nonzero-volume boundary-face extrusion along the translation. This covers the whole straight path, including intermediate positions, rather than sampling a few poses. A swept overlap greater than 0.01 mm³ is an obstruction. Curved moving shapes are explicitly rejected by this implementation; it makes no rotational or hinge-sweep claim.

A control places a blocker between two clear endpoint positions and verifies that the continuous sweep detects it. Moving that blocker outside the path clears it. A known cube sweep checks the analytic swept volume. The 10 intended-clear routes and six intended-obstructed controls are explicit regression gates, so a new obstruction cannot silently become a passing design result.

## Review CAD

The following separate documents show each loaded shelf at the end of its horizontal move, before the vertical lift:

- [S1 service stage](../exports/generated/side-panel-v32/service-stage-SHELF_1.FCStd)
- [S2 service stage](../exports/generated/side-panel-v32/service-stage-SHELF_2.FCStd)
- [S3 service stage](../exports/generated/side-panel-v32/service-stage-SHELF_3.FCStd)

Each contains 65 saved valid single solids, tagged MOVING or RETAINED. Identity sets and exact shapes are checked after reopening. Candidate payload volumes intentionally enclose equipment; they are not additional manufactured parts and should not be counted as BOM solids. These files are generated review poses, not new authoritative cabinet geometry.

## Assembly-interface consequences

1. Release the monitor assembly independently of the guide anchors it blocks. The vertical teardown route is geometrically clear by 290.31 mm of upward translation, but hinges, release hardware, glass, lockdown, lighting and cables are absent. It is **not** the routine raised-playfield service mode and does not replace two captive props or the mandatory one-prop proof.
2. Give crossmembers independently accessible anti-lift retention. Their tested vertical exit travels are T1 323.21, T2 267.32 and T3 218.42 mm. Do not add hardware across the guide mouths or these extraction volumes without rerunning the study.
3. Make shelf retention releasable before sliding. No screw, dowel, cable clamp or future captured joint may require the forbidden direct-lift route before horizontal release. The present model has no final shelf fixings. Sliding contact on an existing support is allowed by the geometric test; friction, grasping and support during transfer still need physical validation.
4. Keep the staging bays and equipment envelope available, including connector bodies and wire restraints. Prefer detachable harness connections on each removable shelf. A cable routed across a bay can invalidate a clear CAD result.
5. Retain current shelf positions and shell geometry while detailing fasteners. Re-run this study for adopted joinery, new prop/SSF/leg hardware, or a PC architecture change. The result is conditional on the current low PC geometry and does not settle the pending drawer decision.

These are proposed interface requirements derived from the study, not released fabrication details. Missing load, grip, restraint, electrical and physical assembly evidence remains open.

## Reproduce

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_side_motion_v32.py
```

The runner requires explicit FreeCAD success sentinels for all three audits. Expected evidence is 46 saved-side checks, 29 guide-tool checks and **99 motion/saved-pose checks**. The motion report has 16 routes: 10 clear in the modeled scene and six intentionally obstructed comparisons. [Full motion evidence](../exports/generated/side-panel-v32/motion-validation.json). Rendering refuses stale source/config hashes or failed checks. The diagram is a side projection of saved-shape bounds, not a manufacturing drawing.

The original V32 remains byte-identical, SHA256 `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`. Physical sessions remain paused. Hardware dimensions, loads, captive props, stock/tool tolerances, coupon and owner manufacturing release remain required.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

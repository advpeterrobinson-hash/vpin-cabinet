# V32 — simple top-release shelves

[Português (Brasil)](pt-BR/SIMPLE_SHELVES_V32.md)

**Current owner-directed shelf fixing direction. Supersedes the removable support/nut-cover studies for normal service. CNC BLOCKED.**

![Four top screws](../exports/generated/side-panel-v32/07-simple-shelves.png)

The intended routine is: open and positively support the playfield, disconnect the shelf harness, undo **two top screws on each side**, then slide the shelf into its extraction bay and lift it with equipment attached. Local supports remain fixed in the cabinet. No nut covers, underneath release or support-side anchors are part of this routine. Threaded receivers stay in the supports so nothing loose needs a hand underneath.

The new separate CAD implements four top screws per shelf with simple top-insert envelopes in fixed 42 mm-wide supports. Original permanent panels and all crossmembers are unchanged. The previous captured-nut covers and support replacement mechanism are superseded in the current direction; their old evidence is retained only as history. S1NutCoverL/R through S3NutCoverL/R are retired identities and must not be reused.

## Changes needed for visible access from above

| Shelf | Leading Y | Screw rows (global Y) | Removal path with crossmembers retained |
|---|---:|---:|---|
| S1 | 120, unchanged | 145 /220 | Rearward 290 mm to Y410, then lift |
| S2 | 565 | 590 /665 | Forward 135 mm to Y430, then lift |
| S3 | 865 | 880 /940 | Forward 105 mm to Y760, then lift |

Each row has left/right axes X48/552. The owner's spacing correction moves S2 forward 35 mm and S3 rearward 45 mm relative to the previous proposal. Clear longitudinal gaps are now **295 mm and 150 mm**, previously 330 mm and 70 mm. S1 stays at Y120; all shelf sizes/heights and crossmembers are retained. S2 and S3 screw rows are adjusted to avoid T2/T3 overhead obstacles. S1 now stages at Y410, leaving a nominal 5 mm longitudinal gap to installed S2 during its rise; this is geometric clearance, not validated hand clearance. Each shelf still removes independently. Prior rejected tool positions remain negative controls.

![Before and after shelf spacing](../exports/generated/side-panel-v32/09-shelf-spacing.png)

The test now reserves an entire vertical Ø16 tool column from each screw head to Z606.9, rather than testing only a short driver beneath a hidden obstruction. Three loaded removal paths also pass with **all three crossmembers, guides and supports retained**. Other shelves stay installed. The candidate equipment envelope is 60 mm above each shelf, with four Ø20 equipment/wiring exclusions for tool access. These exclusions are not large holes in the shelf. S1's modeled audio body moves with it.

## What is and is not demonstrated

Owner supplied a simple shelf reference and requested CNC-predrilled holes. The [joint assessment](SHELF_JOINT_REFERENCE_V32.md) retains bearing supports and four top screws; cam furniture connectors are a reference alternative, not an adopted replacement. Shop-located shelf, receiver and wall-support holes remain required in the final package; exact wall anchorage/pilot sizes await qualified hardware and material. No lifetime/load rating follows from the reference image.

**93 checks pass** against the stationary scene. The additional rear-axis screen now includes all four raised playfield assembly shapes. At 100 degrees of opening relative to the closed pose, all 12 top tool columns and three loaded shelf paths clear the modeled display; 51 opening samples at 2-degree intervals clear the modeled stationary scene, including payload envelopes. At 60–90 degrees some top columns remain obstructed. This is an assumed axis at X300/Y1033.186/Z496.041, derived from the saved rail rear upper edge, not a selected hinge. Actual hinge/props/receivers, cables, glass removal, upper backbox and human handling remain outside this screen. Motion between angular samples and structural safety are unverified. No safe service angle or manufacturing release is established.

Nominal candidate fastening: Ø5 ×25 shaft, Ø9 ×4 head, Ø12 ×1 washer, top receiver Ø8 ×10, Ø8.5 pocket10.5 deep and a Ø5.5 tip relief12.5 deep in the nominal18 support. There are no underside nut pockets or covers. Hardware, threads, receiver retention, fixed-cleat attachment, loads and stock/tool tolerances are unqualified; these are not purchase or machining specifications. Support installation should be a fixed cabinet-assembly operation, not another service mechanism.

- [Simplified FreeCAD proposal](../exports/generated/side-panel-v32/simple-shelves-proposal.FCStd): reopened and compared, 108 valid single solids including occupancy volumes.
- [Validation](../exports/generated/side-panel-v32/simple-shelves-validation.json): complete top columns, withdrawals, three continuous conservative translation sweeps and rejected old layouts.
- Parameters: `config/simple_shelves_v32.json`; source: `tools/simple_shelves_v32_entry.py`.

Use `bash tools/run_simple_shelves_v32.sh`, then `bash tools/run_shelf_service_pose_v32.sh` for the added raised-assembly screen. For the original fixing illustration use `uv run --with matplotlib python tools/render_simple_shelves_v32.py`. Require `SIMPLE_SHELVES_PASS`; the older five-stage side runner reproduces the superseded complexity studies and is no longer the current shelf authoring entry point.

Original V32 bytes remain unchanged. The illustration is an explanatory exploded schematic with exaggerated separation, not a fabrication drawing. Physical sessions remain paused. The PC decision is unchanged.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

## Raised-display screen and hole schedule

![Raised display screen](../exports/generated/side-panel-v32/08-shelf-raised-display.png)

The [12-row hole schedule](../exports/generated/side-panel-v32/shelf-hole-schedule-review.csv) comes from the validated axes. Global X48/552 corresponds to 28 mm from either shelf edge. All dimensions remain review-only: especially the receiver pockets are envelopes, not qualified pilot diameters. Support-to-wall drilling is not released. [Pose report](../exports/generated/side-panel-v32/shelf-service-pose-screen.json) records collisions at rejected angles and negative controls for closed display and previous S3 placement. Render with `uv run --with matplotlib python tools/render_shelf_service_pose_v32.py`.

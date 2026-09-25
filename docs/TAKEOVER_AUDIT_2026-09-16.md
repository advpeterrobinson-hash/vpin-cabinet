# Engineering audit — 2026-09-16

Starting branch: `feat/active-build-cleanup-v25`, HEAD `e9c86b6`. PR #24 targets the v24 feature branch; the earlier mechanical PRs form an open stack. No merges or history rewriting performed.

The initial working tree already contained a modified `cad/master/vpin-master.FCStd` and deleted `vpin-master.20260914-181346.FCBak`. Neither change belongs to this work. The working master was backed up locally and compared byte-for-byte after source generation.

## Read-only findings

The saved document contained 294 objects including the old OLED, playfield v04/v05, v20 drawer/leg/wheel and v21 lift-out sled geometry. Hiding did not remove historical engineering ambiguity. Marker/string verification passed despite the wrong door geometry.

Actual saved CPU geometry before correction:

- opening Z180..420;
- shelf Z205..223;
- closed door Z168..432;
- open door Y952.621..1308.1: **inside** the cabinet;
- rails Y825..1295: 4.9 mm intrusion into the rear panel outside the hatch;
- dedicated CPU harness ghost still present.

All default Python validators passed the old baseline. Requirements and build phases still described 520 mm rear hatches and 300 mm slides. The hardware freeze matrix incorrectly classified gas-strut mounts as having no CNC dependency.

## Implemented scope

Fresh source-only document generation, lower CPU package, rear-view left exterior door swing, shortened support rails, no dedicated CPU harness, low fascia targets, active wooden-part records, expanded hardware freeze matrix, current documentation and automatic geometry-based review views.

No reference file or owner working CAD was altered. No exact unmeasured hardware hole pattern was added. Historical builders still exist for investigation but are not invoked by the fresh active build.

## Verification and its limits

`make validate`: current Python config validators pass.

`make build-current`: FreeCADCmd generates a fresh document, reopens it and checks actual solids. The runner requires fresh success sentinels because FreeCADCmd can exit zero after a Python exception. Preview rendering uses an isolated matplotlib environment via uv.

`tools/test_active_geometry_entry.py`: rejects an inward door, a shelf raised by 70 mm and a restored dedicated harness object. Checks inspect saved shapes, not presentation labels.

Geometry checks cover intended solid validity, recompute state, body dimensions/symmetry, actual hatch subtraction, lower heights, case/board fit, travel, exterior accessibility, saved outward-door transform, 1° sampled angular sweep against the rear panel/rails/brackets/fascias, exact linear rectangular service sweeps and both safety-stay objects. The 1° sweep is a packaging test, not a continuous swept-volume certification.

The solid check excludes FreeCAD datum lines/planes/points because inspection proved these are intentionally non-solid coordinate geometry. It still requires valid solids for every generated `PartDesign::Feature`. The old arbitrary aperture floor Z≥175 check is replaced by clearance against actual fascia extents; the lowered fascia top is Z85 and door bottom Z98, giving 13 mm. Neither change relaxes a physical requirement.

## Open issues — not hidden by PASS

- Requested 55 mm utility windows at Z20..75 overlap the bottom capture and rear bracket region. They remain explicit blocked candidates and are **not cut**. Owner layout preference is pending.
- Internal mains enclosure remains a packaging envelope; its low position also requires resolution against the bottom/leg interfaces. No electrical safety approval is inferred.
- Compact CPU rails need detailed cabinet anchors/fasteners and the 20 kg fully extended proof test. Current geometry does not prove a complete support load path.
- External purchased legs, hinge knuckles and latches are not fully modeled; measured parts may change clearances.
- Nominal shell/backbox joints overlap pending measured-stock machining. Backbox closure/carrier, pivot/fold sweep and reinforcement still require detailed engineering.
- Landing/latch doublers overlap. Their part records call for combination after hardware freeze; they are not separate approved stacked pieces.
- Final tool radius relief, nests, grain orientation, insert pilot sizes and production drawings are not yet released.

The output is a reviewable active engineering baseline and CNC preparation inventory. It is not a manufacturing package or proof of structural/electrical safety.

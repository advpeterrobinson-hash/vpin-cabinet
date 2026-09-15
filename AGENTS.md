# AGENTS.md

## Purpose

This repository contains the engineering source for a CNC-ready virtual pinball cabinet based on Williams WPC standard-body proportions. The project is intended to be reproducible, parametric, serviceable, future-proof, and safe to manufacture.

## Source of truth

- Python/FreeCAD build scripts and documented design parameters are authoritative.
- `cad/master/vpin-master.FCStd` is a generated/working engineering artifact, not the sole source of truth.
- External reference models under `reference/` are read-only references and must not be edited or copied wholesale into production geometry.
- All production dimensions must be traceable to either a documented hardware specification, a measured part, or an explicit design decision.

## Non-negotiable design constraints

- Williams WPC geometry is the visual/proportional baseline, **not an absolute dimensional constraint**. The owner explicitly approves roughly 10–50 mm dimensional deviations where they materially improve serviceability, structural margin, replacement-part availability, or future electronics compatibility.
- Permanent cabinetry must be designed around service/replacement envelopes, not just the exact dimensions of the first-generation electronics.
- Prefer replaceable adapters, slotted carriers, filler strips, bezels, and mounting plates over monitor/board-specific holes in permanent wood panels.
- Nominal main material is 18 mm metric plywood; production geometry must ultimately use measured sheet thickness.
- Playfield display is initially LG OLED42C5, 42-inch, mounted in a separate structural cradle. The cradle and cabinet bay should be evaluated for larger future 42-inch-class replacement envelopes before cabinet width is frozen.
- The OLED must hinge upward for service and use dual gas struts plus an independent mechanical safety restraint.
- A reduced-thickness OLED side pocket is clearance only; OLED mass and gas-strut loads must be carried by full-strength structure/cradle hardware.
- Backglass is approximately 32-inch 1080p; premium image quality is not a priority there. Backbox width may depart from authentic Williams dimensions to create a durable 32-inch-class service envelope.
- PC uses a removable/open ATX chassis on a full-extension service drawer. The drawer must use a replaceable chassis adapter so a future PC frame does not require cabinet surgery.
- Real pinball legs are required; mobility must use retractable or otherwise play-isolated wheels so the cabinet rests rigidly on levelers during play.
- Force feedback, SSF, electronics shelves, power distribution, and service wiring must be designed intentionally, not fitted after cabinet completion.
- Mechanical feedback devices should be rigidly coupled to the cabinet in spatially appropriate locations.
- Electronics shelves should avoid unnecessarily bracing SSF-active cabinet walls.
- Cabinet must use one external grounded power cord with internally protected distribution.
- Operating modes: OFF, AUDIO ONLY/Bluetooth, FULL PINBALL.
- Cabinet should be normally offline after setup, while retaining deliberate service/network access.
- Assembly should require minimal tools after CNC cutting.

## Future-proofing rules

- A few millimetres of spare space are insufficient for permanent cabinetry expected to last many years.
- For major electronic classes (playfield, backglass, PC chassis, amplifiers, controller boards, power supplies), define a documented service envelope larger than the initially selected component where practical.
- Exact electronics may be required before machining removable carriers/adapters, but should not be required before cutting the permanent shell when a modular interface can decouple the two.
- Avoid trapping connectors, vents, VESA mounts, or service screws behind permanent structure.
- Preserve at least one upgrade path for electronics that are modestly wider/deeper than the initial part.
- When exact historical dimensions conflict with a clearly better long-term replacement envelope, prefer the replacement envelope while preserving the visual character of a Williams machine.

## Parametric CAD rules

- Prefer spreadsheet aliases/expressions over hard-coded geometry values.
- Do not create frozen geometry when a live FreeCAD expression can reasonably drive the part.
- Metric units are authoritative in the new design.
- Preserve clear coordinate conventions in every script:
  - X = cabinet left-to-right
  - Y = cabinet front-to-rear
  - Z = vertical
- Geometry-generation scripts must be safe to rerun and should remove/replace only objects they own.
- Scripts must fail clearly if required objects/parameters are missing.
- Changes to master dimensions must include a validation update or an explicit explanation why none is required.

## CNC rules

- No file is production-ready merely because it exports successfully.
- Final CNC output requires:
  - measured material thickness;
  - confirmed tool diameter;
  - confirmed joint/pocket clearance;
  - dogbone/T-bone strategy;
  - validation of part nesting and orientation;
  - a physical tolerance test coupon;
  - owner approval before manufacturing.
- Cutter CNC (`cuttercnc.com`, Brazil) is the current prospective fabrication provider. Provider-specific CAM assumptions remain TBD until consultation.
- Keep through-cuts, pockets, drilling, engraving, and reference geometry distinguishable in exports/layers where possible.

## Safety rules

- Never treat mains-voltage wiring as ordinary low-voltage electronics.
- Do not publish or approve exposed mains terminals inside service areas.
- Mechanical feedback must have an independent service-disable/kill path.
- OLED service position must remain safe if a gas strut fails; a positive mechanical safety device is mandatory.
- GPU and other heavy internal components require positive mechanical restraint because the cabinet will be nudged and vibrated.

## Validation policy

Before calling a design stage complete, validate at minimum:

- document recomputes without fatal errors;
- expected outer dimensions remain correct for the current approved design baseline;
- left/right geometry remains symmetric where intended;
- selected component fits within its service envelope;
- service envelope preserves documented future-replacement margin;
- remaining side skin around OLED meets the documented minimum;
- service envelopes do not obviously collide;
- generated parts are valid solids when they are intended to be solids.

Later stages must add hinge sweep, gas-strut, drawer-travel, backbox, toy, speaker, shelf, and cable-clearance checks.

## Git workflow

- Use feature branches for substantial design/tooling work.
- Keep commits narrow and descriptive.
- Do not silently overwrite owner changes.
- Do not modify or delete reference models.
- Do not merge manufacturing-ready claims without validation evidence.

## Current validated baseline

- Williams WPC reference outer cabinet width: 558.80 mm.
- Cabinet side length: 1308.10 mm.
- Cabinet front outside height: 400.05 mm.
- Cabinet rear outside height: 596.90 mm.
- Rear top flat: 180.975 mm.
- Main plywood nominal: 18.00 mm.
- LG OLED42C5 physical envelope: 932.0 x 540.0 x 41.1 mm, mass 9.8 kg.
- Current OLED target installed cross-width envelope: 542.0 mm.
- Current nominal remaining plywood skin: 8.40 mm.
- Main cabinet width is now subject to future-proofing review; the reference width is no longer presumed final.
- Backbox future-proof target under v0.6: 780 mm outer width with a 740 x 450 x 100 mm replaceable display service envelope.

These values are engineering baseline values, not final manufacturing approval.

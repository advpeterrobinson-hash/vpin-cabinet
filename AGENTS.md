# AGENTS.md

## Purpose

This repository contains the engineering source for a CNC-ready virtual pinball cabinet based on Williams WPC standard-body proportions. The project is intended to be reproducible, parametric, serviceable, and safe to manufacture.

## Source of truth

- Python/FreeCAD build scripts and documented design parameters are authoritative.
- `cad/master/vpin-master.FCStd` is a generated/working engineering artifact, not the sole source of truth.
- External reference models under `reference/` are read-only references and must not be edited or copied wholesale into production geometry.
- All production dimensions must be traceable to either a documented hardware specification, a measured part, or an explicit design decision.

## Non-negotiable design constraints

- Preserve Williams WPC standard-body external cabinet proportions unless the owner explicitly approves a change.
- Nominal main material is 18 mm metric plywood; production geometry must ultimately use measured sheet thickness.
- Playfield display is LG OLED42C5, 42-inch, mounted in a separate structural cradle.
- The OLED must hinge upward for service and use dual gas struts plus an independent mechanical safety restraint.
- A reduced-thickness OLED side pocket is clearance only; OLED mass and gas-strut loads must be carried by full-strength structure/cradle hardware.
- Backglass is approximately 32-inch 1080p; premium image quality is not a priority there.
- PC uses a removable/open ATX chassis on a full-extension service drawer.
- Real pinball legs are required; mobility must use retractable or otherwise play-isolated wheels so the cabinet rests rigidly on levelers during play.
- Force feedback, SSF, electronics shelves, power distribution, and service wiring must be designed intentionally, not fitted after cabinet completion.
- Mechanical feedback devices should be rigidly coupled to the cabinet in spatially appropriate locations.
- Electronics shelves should avoid unnecessarily bracing SSF-active cabinet walls.
- Cabinet must use one external grounded power cord with internally protected distribution.
- Operating modes: OFF, AUDIO ONLY/Bluetooth, FULL PINBALL.
- Cabinet should be normally offline after setup, while retaining deliberate service/network access.
- Assembly should require minimal tools after CNC cutting.

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
- expected outer dimensions remain correct;
- left/right geometry remains symmetric where intended;
- OLED fit/clearance is within design limits;
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

- Williams WPC outer cabinet width: 558.80 mm.
- Cabinet side length: 1308.10 mm.
- Cabinet front outside height: 400.05 mm.
- Cabinet rear outside height: 596.90 mm.
- Rear top flat: 180.975 mm.
- Main plywood nominal: 18.00 mm.
- Nominal inside width at 18 mm plywood: 522.80 mm.
- LG OLED42C5 physical envelope: 932.0 x 540.0 x 41.1 mm, mass 9.8 kg.
- OLED target installed cross-width envelope: 542.0 mm (1 mm clearance per side).
- Nominal OLED side pocket depth: 9.60 mm.
- Nominal remaining plywood skin: 8.40 mm.

These values are engineering baseline values, not final manufacturing approval.

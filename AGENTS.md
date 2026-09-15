# AGENTS.md

## Purpose

This repository contains the engineering source for a CNC-ready virtual pinball cabinet inspired by Williams WPC proportions. The project is intended to be reproducible, parametric, serviceable, future-proof, apartment-buildable, and safe to manufacture.

The primary product is not merely one cabinet. The primary product is a **replicable flat-pack CNC plan** that another builder can take to a local CNC shop, order the parts, and assemble at home without owning expensive woodworking machinery.

## Source of truth

- Python/FreeCAD build scripts and documented design parameters are authoritative.
- `cad/master/vpin-master.FCStd` is a generated/working engineering artifact, not the sole source of truth.
- External reference models under `reference/` are read-only references and must not be edited or copied wholesale into production geometry.
- All production dimensions must be traceable to either a documented hardware specification, a measured part, or an explicit design decision.

## Non-negotiable design constraints

- Williams WPC geometry is the visual/proportional baseline, **not an absolute dimensional constraint**. The owner explicitly approves roughly 10–50 mm dimensional deviations where they materially improve serviceability, structural margin, replacement-part availability, future electronics compatibility, or CNC/assembly simplicity.
- Permanent cabinetry must be designed around service/replacement envelopes, not just the exact dimensions of the first-generation electronics.
- Prefer replaceable adapters, slotted carriers, filler strips, bezels, and mounting plates over monitor/board-specific holes in permanent wood panels.
- Main-body engineering baseline width is 580 mm unless a later validation shows a substantial disadvantage. This is intentionally wider than the 558.8 mm Williams reference to provide a future 42-inch-class playfield service envelope.
- The lockdown bar may be custom-sized and therefore is **not** a blocker to the 580 mm body width.
- Nominal main material is 18 mm metric plywood; production geometry must ultimately use measured sheet thickness.
- Playfield display is initially LG OLED42C5, 42-inch, mounted in a separate structural cradle. The cradle and cabinet bay must preserve the larger documented future-replacement envelope.
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

## Flat-pack / apartment-build rules

- A builder should not need a table saw, track saw, router table, drill press, planer, jointer, welding equipment, or other major workshop machinery to assemble the wooden cabinet.
- The CNC shop should perform all practical structural cutting, pockets, dados, rabbets, slots, dogbones/T-bones, large openings, repeatable drilling, and alignment features.
- Permanent panels should be self-locating where practical through dados, tabs, slots, shoulders, or captured alignment features.
- Assembly should target ordinary hand tools only: drill/driver, hex keys/screwdrivers, clamps, mallet, glue, measuring tools, sanding/painting supplies, and simple service tools.
- Avoid joints that require precise freehand routing or table-saw tuning after CNC delivery.
- Wherever feasible, hardware holes should be CNC-located rather than marked manually by the builder.
- Repeated left/right parts should be symmetric or clearly keyed so assembly mistakes are difficult.
- Every CNC part must eventually have an unambiguous part ID that corresponds to drawings, BOM, and assembly instructions.
- The final release package should be understandable by both the CNC shop and a first-time builder without requiring FreeCAD expertise.
- Metal parts that need fabrication, such as a custom lockdown bar, brackets, or panels, should have separate dimensioned DXF/PDF fabrication files where practical so they too can be outsourced rather than fabricated with specialist tools at home.
- Design complexity is acceptable inside the CAD/CAM package if it **reduces** builder skill, tool requirements, and measurement burden during assembly.

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
- Final manufacturing package should include, at minimum: CNC-ready DXF/SVG where appropriate, dimensioned PDFs, sheet/material map, part IDs, hardware/BOM, tolerance coupon, and assembly guide.

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
- generated parts are valid solids when they are intended to be solids;
- the part can be fabricated/assembled without requiring an undocumented specialist operation.

Later stages must add hinge sweep, gas-strut, drawer-travel, backbox, toy, speaker, shelf, cable-clearance, fastener-access, and flat-pack assembly checks.

## Git workflow

- Use feature branches for substantial design/tooling work.
- Keep commits narrow and descriptive.
- Do not silently overwrite owner changes.
- Do not modify or delete reference models.
- Do not merge manufacturing-ready claims without validation evidence.

## Current validated / selected baseline

- Williams WPC reference outer cabinet width: 558.80 mm.
- Selected engineering main-body width: 580.00 mm, pending master CAD migration and final manufacturing validation.
- Cabinet side length reference: 1308.10 mm.
- Cabinet front outside height reference: 400.05 mm.
- Cabinet rear outside height reference: 596.90 mm.
- Rear top flat reference: 180.975 mm.
- Main plywood nominal: 18.00 mm.
- LG OLED42C5 physical envelope: 932.0 x 540.0 x 41.1 mm, mass 9.8 kg.
- Future playfield service envelope under v0.7: 560 x 950 x 55 mm plus 2 mm installation clearance per side.
- Backbox future-proof target under v0.6: 780 mm outer width with a 740 x 450 x 100 mm replaceable display service envelope.
- Custom-size lockdown bar is an accepted fabrication strategy.

These values are engineering baseline values, not final manufacturing approval.

# Virtual Pinball Cabinet

Parametric CNC-ready virtual pinball cabinet inspired by Williams WPC proportions, with deliberate future-proofing for replaceable electronics and apartment-friendly flat-pack assembly.

## Primary design targets

- Williams WPC-derived visual proportions rather than rigid historical dimensions
- selected **580 mm main-cabinet width** for future 42-inch-class display tolerance
- selected **780 mm backbox width** with reusable adjustable display carriers
- 18 mm metric plywood primary structure (production value = measured sheet thickness)
- LG OLED42C5 initial playfield in a replaceable structural cradle
- approximately 31.5/32-inch backglass preferred; 27/28-inch fallback supported through adjustable carriage/bezel
- Williams/Bally WPC-style folding backbox hinges and separate upright locking bolts
- keyed/gasketed rear backbox service door
- hinged structural playfield cradle with dual gas struts and independent mechanical safety support
- real pinball legs and levelers
- retractable/play-isolated wheels for moving cabinet
- full DOF / mechanical force feedback and SSF planned after structure completion
- modular electronics and feedback mounting
- slide-out ATX PC chassis on a replaceable drawer adapter
- single mains power cord with isolated protected distribution
- independent Audio Only / Bluetooth and Full Pinball modes
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Build philosophy

The primary product is a **replicable CNC flat-pack plan**, not one bespoke cabinet. Precision work should be absorbed into CAD/CAM and local fabrication so a builder can order the parts from a CNC/metal shop and assemble the machine in an apartment without owning a table saw, router table, drill press, planer or welder.

Every CNC/fabricated part will receive a stable part ID linked to the BOM and build manual. Manufacturing labels and cosmetic white-filled vintage engravings are kept on separate export layers.

## Structure-first procurement

Woodworking, displays, real pinball legs, folding backbox hardware, lockdown/siderails, playfield mechanics and the PC drawer must reach a **STRUCTURE READY** gate before the coordinated electronics/DOF purchase begins.

This reduces electronic obsolescence during the long cabinet build and prevents expensive electronics from dictating permanent wood geometry unnecessarily.

See:

- `docs/BUILD_PHASES.md` — staged purchasing / phase gates
- `bom/STRUCTURE_BOM.csv` — procurement tracker
- `bom/STRUCTURE_PARTS.csv` — labeled CNC/fabricated part registry
- `docs/STRUCTURE_BUILD_MANUAL.md` — living mechanical assembly manual
- `docs/PART_LABELING.md` — part/revision/engraving convention
- `docs/BACKBOX_HINGE_SHOPPING.md` — WPC hinge part numbers and procurement notes

## Longevity philosophy

The wooden cabinet and structural metalwork should outlive several generations of televisions, PC hardware, control boards, amplifiers, and power supplies. Permanent structure is therefore designed around service envelopes and modular interfaces rather than the exact dimensions of the first electronics installed.

Current examples:

- 580 mm main body supports the initial 540 mm-wide C5 without side routing and preserves a routed future-display envelope;
- 780 mm backbox provides a 740 x 450 x 100 mm display service envelope;
- backglass and DMD use independent adjustable rail carriages and replaceable VESA/tray adapters;
- PC and electronics mounting use replaceable adapters/panels;
- rear service I/O uses replaceable fascias/carriers rather than connector-specific permanent wood cutouts.

See `docs/FUTURE_PROOFING.md`.

## Engineering workflow

The long-term source of truth is the documented design baseline plus the Python/FreeCAD generation and validation scripts. The binary `.FCStd` master is an engineering artifact, not the only record of design intent.

Useful local commands:

```bash
make doctor
make validate
make open-master
```

`make validate` runs the current pure-Python dimensional, packaging, routing, structural-material and build-package checks. FreeCAD geometry/collision checks remain separate local gates for CAD-changing stages.

See also:

- `AGENTS.md` — engineering rules for humans and coding agents
- `config/design.json` — machine-readable design baseline
- `docs/DESIGN_DECISIONS.md` — decision log
- `docs/FUTURE_PROOFING.md` — long-term replacement/service envelope policy
- `docs/requirements.md` — system requirements
- `docs/reference-baseline.md` — dimensions extracted from the reference model
- `docs/vendors.md` — parts/services/vendor notes

## Current selected geometry

- main cabinet outer width: **580.00 mm**;
- nominal inside width at 18 mm plywood: **544.00 mm**;
- cabinet side length: **1308.10 mm**;
- front outside height: **400.05 mm**;
- rear outside height: **596.90 mm**;
- backbox target outer width: **780.00 mm**;
- LG OLED42C5 physical envelope: **932.0 x 540.0 x 41.1 mm**, 9.8 kg;
- current C5 installed cross-width envelope: **542.0 mm**;
- future playfield chassis target: **560 x 950 x 55 mm** plus installation clearance;
- backglass service envelope: **740 x 450 x 100 mm**.

The OLED and gas-strut loads are carried by an independent structural cradle. Reduced-thickness side pockets, if ever required by a future wider display, are clearance only and are not permitted to carry structural lifting loads.

## Safety baseline

This is intended to be a household entertainment appliance, not an exposed electronics test rig. Reachable hazardous voltage is a blocking defect. Backbox/service openings are guarded, gasketed and lockable; no bare mains terminals are permitted in ordinary or keyed service areas. Any service procedure that can expose mains voltage must carry an explicit shock-hazard warning and isolation instructions.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, measured sheet thickness, Cutter CNC/tooling consultation, physical tolerance coupon, local FreeCAD geometry validation and final proof testing.

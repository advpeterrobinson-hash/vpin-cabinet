# Virtual Pinball Cabinet

Parametric CNC-ready virtual pinball cabinet inspired by Williams WPC proportions, with deliberate future-proofing for replaceable electronics and apartment-friendly flat-pack assembly.

## Primary design targets

- Williams WPC-derived visual proportions rather than rigid historical dimensions
- selected **600 mm main-cabinet width** for a full-thickness 42/43-inch display bay without baseline side pockets
- selected **780 mm backbox width** with reusable adjustable display carriers
- 18 mm metric plywood primary structure (production value = measured sheet thickness)
- **model-agnostic 42/43-inch 4K high-refresh playfield display** in a replaceable structural cradle
- approximately 31.5/32-inch backglass preferred; 27/28-inch fallback supported through adjustable carriage/bezel
- Williams/Bally WPC-style folding backbox hinges and separate upright locking bolts
- keyed/gasketed rear backbox service door
- predominantly CNC-plywood playfield cradle with local steel pivot interfaces
- dual gas struts for lift assistance only
- **two independent positive mechanical safety stays** plus two positive closed-position latches/supports
- real pinball legs and levelers
- retractable/play-isolated wheels for moving cabinet
- full DOF / mechanical force feedback and SSF planned after structure completion
- modular electronics and feedback mounting
- slide-out ATX PC chassis on a replaceable drawer adapter
- single mains power cord with isolated protected distribution
- independent Audio Only / Bluetooth and Full Pinball modes
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Structure-first procurement

Woodworking, displays, real pinball legs, folding backbox hardware, lockdown/siderails, playfield mechanics and the PC drawer must reach a **STRUCTURE READY** gate before the coordinated electronics/DOF purchase begins.

The exact playfield display is selected late in the structure phase from the models actually available in Brazil, rather than locking the permanent cabinet to one LG/Samsung model.

See:

- `docs/BUILD_PHASES.md`
- `bom/STRUCTURE_BOM.csv`
- `bom/STRUCTURE_PARTS.csv`
- `docs/STRUCTURE_BUILD_MANUAL.md`
- `docs/PART_LABELING.md`
- `docs/BACKBOX_HINGE_SHOPPING.md`
- `docs/PLAYFIELD_DISPLAY_V16.md`
- `docs/PLAYFIELD_PIVOT_V15.md`
- `docs/PLAYFIELD_MECHANICS_V18.md`

## Longevity philosophy

The wooden cabinet and structural metalwork should outlive several generations of televisions, PC hardware, control boards, amplifiers and power supplies. Permanent structure is therefore designed around service envelopes and modular interfaces rather than the exact dimensions of the first electronics installed.

Current examples:

- **600 mm body + nominal 18 mm sides = 564 mm full-thickness internal width**;
- the planned **560 mm physical display width + 2 mm clearance each side = 564 mm**, so the normal 42/43-inch envelope fits without routing the side panels thinner;
- an exceptional future display could still use controlled pockets, up to a documented maximum routed cavity, but this is no longer part of the baseline build;
- longitudinal playfield target is **970 mm chassis / 980 mm clear service bay**;
- exact playfield VESA pattern lives on a replaceable adapter plate;
- the playfield cradle uses replaceable local steel wear/load interfaces instead of making the TV or permanent sidewalls model-specific;
- 780 mm backbox provides a 740 x 450 x 100 mm display service envelope;
- backglass and DMD use independent adjustable rail carriages and replaceable VESA/tray adapters;
- PC and electronics mounting use replaceable adapters/panels.

## Current selected geometry

- Williams WPC standard-body reference outer width: **558.80 mm**;
- selected main cabinet outer width: **600.00 mm**;
- increase over WPC reference: **41.20 mm total / 20.60 mm each side**;
- nominal inside width at 18 mm plywood: **564.00 mm**;
- normal playfield target fits with **zero side pocket**;
- maximum future routed cross-cavity at 8 mm remaining side skin: **584.00 mm**;
- cabinet side length: **1308.10 mm**;
- front outside height: **400.05 mm**;
- rear outside height: **596.90 mm**;
- backbox target outer width: **780.00 mm**, giving **90 mm overhang per side** over the 600 mm body;
- playfield display physical target: **<=560 x 970 x 55 mm**, <=12 kg;
- preliminary integrated moving-mass packaging value: **16.5 kg** (12.0 kg display + 4.5 kg cradle allowance);
- playfield display purchasing target: **4K, native >=120 Hz**, VRR/HDMI 2.1 preferred;
- backglass service envelope: **740 x 450 x 100 mm**.

Current fit references include LG 42-inch C-series geometry and the Samsung 43-inch QN90F/QN90D chassis class. These remain fit references, not purchase mandates.

## Playfield mechanics v0.18

The active FreeCAD mechanical review package is now intended to show the complete system rather than the old LG-specific slab:

- generic 560 x 970 x 55 mm display envelope;
- two CNC plywood side rails and three under-display crossmembers;
- 36 mm local rear pivot doublers and laminated rear beam;
- replaceable VESA carrier envelope;
- 140 x 80 x 6 mm steel pivot cheek plates;
- 15 mm short journals and UCFL202 bearing keepouts;
- two gas-strut packaging lines with force/mounts explicitly deferred;
- two positive safety stays;
- two closed structural landing pads and two positive latch keepouts;
- 300 mm / R50 moving display harness-loop keepout.

Run locally with:

```bash
make build-playfield-mechanics-v18
freecad cad/master/vpin-master.FCStd
```

The expected group is:

`PLAYFIELD MECHANICS v0.18 - GENERIC 43in / PLYWOOD CRADLE / DUAL SAFETY`

## Safety baseline

The display and gas-strut loads are carried by an independent structural cradle. Gas struts are lift assistance only; both positive mechanical safety stays must be engaged before working under the raised playfield. Cabinet mains power must be isolated before manipulating the display harness, pivot, gas struts, stays or removing the complete cradle. Reachable hazardous voltage is a blocking defect.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, measured sheet thickness, Cutter CNC/tooling consultation, physical tolerance coupon, local FreeCAD geometry validation and final proof testing.

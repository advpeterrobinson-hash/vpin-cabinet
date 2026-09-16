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
- classic pinball legs and levelers with compact steel-backed corner hardware
- **external removable PinSkates-style mobility**; no integrated/retractable cabinet wheels
- **internal lift-out PC service sled** accessed from above; no front-travel drawer
- custom/local-fabricated 600 mm lockdown bar, siderails and metric tempered playfield glass permitted
- full DOF / mechanical force feedback and SSF planned after structure completion
- modular electronics and feedback mounting with a deliberately open central service volume
- single mains power cord with isolated protected distribution
- independent Audio Only / Bluetooth and Full Pinball modes
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Structure-first procurement

Woodworking, displays, classic pinball legs, folding backbox hardware, lockdown/siderails, playfield mechanics and the PC service sled must reach a **STRUCTURE READY** gate before the coordinated electronics/DOF purchase begins.

The exact playfield display is selected late in the structure phase from the models actually available in Brazil, rather than locking the permanent cabinet to one LG/Samsung model.

See:

- `docs/BUILD_PHASES.md`
- `bom/STRUCTURE_BOM.csv`
- `bom/STRUCTURE_PARTS.csv`
- `bom/SERVICE_V21_BOM.csv`
- `bom/SERVICE_V21_PARTS.csv`
- `docs/STRUCTURE_BUILD_MANUAL.md`
- `docs/PART_LABELING.md`
- `docs/BACKBOX_HINGE_SHOPPING.md`
- `docs/PLAYFIELD_DISPLAY_V16.md`
- `docs/PLAYFIELD_PIVOT_V15.md`
- `docs/PLAYFIELD_MECHANICS_V18.md`
- `docs/CABINET_STRUCTURE_V20.md`
- `docs/CABINET_SERVICE_V21.md`

## Longevity philosophy

The wooden cabinet and structural metalwork should outlive several generations of televisions, PC hardware, control boards, amplifiers and power supplies. Permanent structure is therefore designed around service envelopes and modular interfaces rather than the exact dimensions of the first electronics installed.

Current examples:

- **600 mm body + nominal 18 mm sides = 564 mm full-thickness internal width**;
- planned **560 mm physical display width + 2 mm clearance each side = 564 mm**, so the normal 42/43-inch envelope fits without routing the side panels thinner;
- longitudinal playfield target is **970 mm chassis / 980 mm clear service bay**;
- exact playfield VESA pattern lives on a replaceable adapter plate;
- playfield pivot/wear points use replaceable local steel interfaces;
- 780 mm backbox provides a 740 x 450 x 100 mm display service envelope;
- backglass and DMD use independent adjustable rail carriages and replaceable VESA/tray adapters;
- leg, lockdown and bearing hole patterns remain blocked until the real hardware is measured;
- the PC is removed vertically through the open playfield rather than requiring a permanent front opening or long drawer slides;
- moving the complete cabinet uses removable external skates rather than built-in casters.

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
- backbox target outer width: **780.00 mm**, giving **90 mm overhang per side**;
- playfield display physical target: **<=560 x 970 x 55 mm**, <=12 kg;
- preliminary moving-mass packaging value: **16.5 kg**;
- playfield display purchasing target: **4K, native >=120 Hz**, VRR/HDMI 2.1 preferred;
- backglass service envelope: **740 x 450 x 100 mm**.

Current fit references include LG 42-inch C-series geometry and the Samsung 43-inch QN90F/QN90D chassis class. These remain fit references, not purchase mandates.

## Playfield mechanics v0.18 + fixed anchors v0.19

The active playfield mechanical architecture includes:

- generic 560 x 970 x 55 mm display envelope;
- CNC plywood cradle with three under-display crossmembers;
- 36 mm rear pivot reinforcement and laminated rear beam;
- replaceable VESA carrier;
- 140 x 80 x 6 mm steel pivot cheek plates;
- 15 mm short journals and UCFL202 bearing family;
- two gas struts with force/mounts explicitly deferred;
- two positive safety stays;
- two closed structural supports and two positive latches;
- fixed sidewall plywood/steel anchor zones for stays, struts, supports and latch receivers;
- moving display harness service loop.

## Cabinet structure v0.20

v0.20 remains the joinery/glass/SSF packaging base:

- nominal 6 mm captured joinery packaging for front/rear/bottom/crossmembers;
- nominal captured bottom blank **576 x 1284.1 mm** at 18 mm stock;
- three low 80 mm-high structural crossmembers;
- explicit sidewall SSF keepouts;
- custom **575 x 1100 x 5 mm** tempered playfield-glass target;
- custom/local-fabricated siderail and 600 mm lockdown-bar envelopes;
- mandatory measured-stock CNC tolerance coupon.

Its bulky plywood leg doublers, retractable-wheel keepouts and forward-travel PC drawer are **superseded by v0.21**.

## Cabinet service / mobility v0.21

The owner-provided reference cabinets favor compact load hardware and a large open service volume. v0.21 therefore changes three major areas:

- **classic legs:** approximately 3 mm steel compact internal corner-bracket envelopes replace the oversized 18+18 mm plywood corner blocks; exact holes remain gated by actual leg/bracket measurement and proof testing;
- **mobility:** a removable pair of external PinSkates-style assemblies moves the machine; there are no integrated/retractable casters or cabinet wheel cutouts;
- **PC service:** a **480 x 320 mm lift-out sled** sits between the mid/rear low crossmembers and removes vertically after the playfield is raised; there is no front-travel drawer mechanism.

Run locally with:

```bash
make build-cabinet-service-v21
freecad cad/master/vpin-master.FCStd
```

Expected review group:

`CABINET SERVICE v0.21 - CLASSIC LEGS / PINSKATES / LIFT-OUT PC`

## Safety baseline

The display and gas-strut loads are carried by an independent structural cradle. Gas struts are lift assistance only; both positive mechanical safety stays must be engaged before working under the raised playfield. Cabinet mains power must be isolated before manipulating the display harness, pivot, gas struts, stays, PC service sled or removing the complete cradle. Reachable hazardous voltage is a blocking defect.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, measured sheet thickness, Cutter CNC/tooling consultation, physical tolerance coupon, local FreeCAD geometry validation, dry fit and final proof testing.

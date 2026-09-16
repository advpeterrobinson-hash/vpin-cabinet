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
- **dedicated main-cabinet rear PC backdoor** with a small rearward pull-out shelf; open PC case bolts directly to the shelf
- custom/local-fabricated 600 mm lockdown bar, siderails and metric tempered playfield glass permitted
- full DOF / mechanical force feedback and SSF planned after structure completion
- modular electronics and feedback mounting with a deliberately open central service volume
- single mains power cord with isolated protected distribution
- independent Audio Only / Bluetooth and Full Pinball modes
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Structure-first procurement

Woodworking, displays, classic pinball legs, folding backbox hardware, lockdown/siderails, playfield mechanics and the rear PC service system must reach a **STRUCTURE READY** gate before the coordinated electronics/DOF purchase begins.

The exact playfield display is selected late in the structure phase from the models actually available in Brazil, rather than locking the permanent cabinet to one LG/Samsung model.

See:

- `docs/BUILD_PHASES.md`
- `docs/STRUCTURE_BUILD_MANUAL.md`
- `docs/PART_LABELING.md`
- `docs/BACKBOX_HINGE_SHOPPING.md`
- `docs/PLAYFIELD_DISPLAY_V16.md`
- `docs/PLAYFIELD_PIVOT_V15.md`
- `docs/PLAYFIELD_MECHANICS_V18.md`
- `docs/CABINET_STRUCTURE_V20.md`
- `docs/CABINET_SERVICE_V21.md`
- `docs/PC_SLIDE_V22.md` — historical/superseded PC-service direction
- `docs/CABINET_REAR_PC_SERVICE_V23.md` — active PC-service direction
- `bom/REAR_PC_SERVICE_V23_BOM.csv`
- `bom/REAR_PC_SERVICE_V23_PARTS.csv`

## Current selected geometry

- Williams WPC standard-body reference outer width: **558.80 mm**;
- selected main cabinet outer width: **600.00 mm**;
- nominal inside width at 18 mm plywood: **564.00 mm**;
- cabinet side length: **1308.10 mm**;
- front outside height: **400.05 mm**;
- rear outside height: **596.90 mm**;
- backbox target outer width: **780.00 mm**, giving **90 mm overhang per side**;
- playfield display physical target: **<=560 x 970 x 55 mm**, <=12 kg;
- playfield display purchasing target: **4K, native >=120 Hz**, VRR/HDMI 2.1 preferred;
- backglass service envelope: **740 x 450 x 100 mm**.

## PC service v0.23 — active direction

Routine PC maintenance is from the **rear of the pinball machine**, not through the playfield.

Current engineering package:

- dedicated main-cabinet rear service opening: approximately **520 x 280 mm**;
- gasketed rear service door: approximately **544 x 304 x 15 mm**;
- compact reinforced aperture frame;
- one small **460 x 285 x 18 mm** plywood PC shelf;
- open-case fit reference **440 x 265 x 128 mm**;
- open PC case bolts directly to that shelf;
- two simple **300 mm-class telescopic/full-extension slides**;
- shelf stows immediately behind the rear door and travels **300 mm rearward**, behind the machine, for service;
- no drawer box, no second sled, no front PC opening;
- routine RAM/SSD/GPU/cable service does **not** require raising the playfield;
- >=450 mm protected rearward cable service loop;
- exact slide/case/hinge/latch holes remain blocked until physical parts are measured.

Build locally with:

```bash
make build-cabinet-rear-pc-v23
freecad cad/master/vpin-master.FCStd
```

Expected review group:

`REAR PC SERVICE v0.23 - BACKDOOR / REARWARD PULL-OUT PC`

## Safety baseline

The rear PC service door may expose PC low-voltage hardware, but **must never expose bare mains terminals**. Mains distribution remains in a separate touch-safe enclosure. Isolate cabinet power before RAM/GPU/SSD/harness service.

The display and gas-strut loads are carried by an independent structural cradle. Gas struts are lift assistance only; both positive mechanical safety stays must be engaged before working under the raised playfield.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, measured sheet thickness, Cutter CNC/tooling consultation, physical tolerance coupon, local FreeCAD geometry validation, dry fit and final proof testing.

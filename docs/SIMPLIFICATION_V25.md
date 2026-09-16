# v0.25 simplification / active-build cleanup

Status: owner-directed engineering cleanup. This document defines the active build philosophy before further CNC detail is added.

## Product goal

The downloadable cabinet should arrive from the CNC/fabrication vendors as a **precision kit**, not as a woodworking project that still requires layout work.

The end builder should normally need only:

1. identify the engraved/labeled parts;
2. dry-fit the self-locating joints;
3. apply glue where specified;
4. install bolts/screws/inserts into CNC-located holes;
5. sand/finish/paint or apply graphics;
6. install the preselected mechanical hardware;
7. install electronics and harnesses;
8. perform the documented proof/safety checks.

The release workflow should **not** require the builder to measure and mark structural hole positions, freehand-align hinges/slides, rout pockets by hand, own a drill press/router/table saw, or infer where hardware belongs.

## What CNC is for in this project

CNC is primarily used to make assembly deterministic:

- final external profiles;
- captured dados/rabbets/tabs;
- all geometry-critical through holes;
- pilot holes where the chosen fastener/hardware requires them;
- insert/T-nut/captive-nut locations;
- hinge and slide hole patterns;
- cable passports and service apertures;
- ventilation/fan openings;
- part IDs, orientation marks and alignment marks;
- shallow cosmetic/service engraving where specified.

All hardware-dependent holes remain blocked during engineering only until the **physical hardware is selected and measured**. Once frozen, those holes belong in the CNC release files. “Drill to fit during assembly” is not the normal release strategy.

## Active mechanical architecture after cleanup

Keep:

- 600 mm main cabinet;
- 780 mm folding backbox;
- nominal 18 mm structural plywood, production geometry regenerated from measured stock;
- captured CNC joinery and low structural crossmembers;
- classic pinball legs + levelers;
- compact steel internal leg brackets, exact holes from measured hardware;
- external removable PinSkates-style mobility only;
- model-agnostic hinged playfield cradle with local steel pivot hardware;
- dual gas struts for lift assistance only;
- dual positive mechanical playfield safety stays;
- rear PC service hatch;
- one narrow case-sized rear CPU shelf on two full-extension slides;
- open PC case bolted directly to the shelf;
- custom 600 mm lockdown bar/siderails and local tempered glass;
- adjustable backglass/DMD carrier;
- closed/keyed service access and touch-safe mains segregation;
- reserved SSF and future DOF zones.

Remove from the active design:

- LG OLED42C5-specific permanent geometry;
- historical playfield-service mockups once the current mechanics package replaces them;
- 580 mm body assumptions;
- bulky 18+18 mm leg-corner furniture as the default;
- integrated/retractable wheels and wheel keepouts;
- front-moving PC drawer concepts;
- lift-out PC sled concept;
- center-directed PC service slide concept;
- wide v0.23 rear-PC hatch/shelf study;
- duplicate validators/build targets for superseded PC-service concepts;
- generated FreeCAD groups whose only purpose is historical comparison.

Git history remains the archive. Superseded experiments do not need to remain in the active master tree or default validation path.

## Hardware-freeze table principle

Every geometry-controlling purchased part is classified as one of:

- `MEASURE_BEFORE_CNC` — physical sample must be in hand before final hole generation;
- `DIMENSIONED_LOCAL_FAB` — project publishes the fabrication drawing;
- `ADAPTER_ONLY` — permanent wood stays generic; exact pattern belongs to a replaceable adapter;
- `NO_CNC_DEPENDENCY` — may be selected later without recutting permanent structure.

The hardware-freeze manifest is the single checklist that determines whether CNC release is allowed.

## Part-count / assembly rule

When two solutions provide similar reliability, choose the one with:

- fewer unique parts;
- fewer hidden fasteners;
- fewer adjustment steps;
- fewer hand-measured operations;
- less permanent obstruction of the cabinet interior;
- easier replacement with locally available hardware.

Do not add a bracket, shelf, rail or doubler merely because there is empty space. Every permanent part must have a documented structural, safety, service or alignment purpose.

## Current rear-PC rule

Routine PC maintenance is performed from behind the machine:

`open rear hatch -> release shelf retainer -> pull CPU shelf rearward -> service PC -> push shelf in -> lock retainer -> close hatch`

Routine RAM/SSD/GPU/cable service must not require opening the playfield.

## Manufacturing gate

A future `CNC_READY=true` release requires, at minimum:

- measured production plywood;
- physical CNC tolerance coupon accepted;
- Cutter CNC tooling/layer conventions confirmed;
- all `MEASURE_BEFORE_CNC` hardware physically measured;
- generated holes checked against those measurements;
- dry-fit/proof tests completed on the prototype;
- no unresolved hand-layout operation in the assembly manual;
- final BOM and part labels reconciled.

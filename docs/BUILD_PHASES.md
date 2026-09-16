# Build phases and procurement gates

Status: engineering planning. This document defines when materials are bought and when each subsystem is allowed to enter the build.

## Phase 0 — Design-freeze inputs

Before ordering production CNC wood, confirm:

- measured plywood thickness from the actual sheet stock;
- CNC provider tooling/layer/radius conventions;
- `CNC-COUPON-001-R1` cut and physically tested;
- **600 mm main-body** geometry;
- 780 mm backbox geometry;
- backbox hinge/pivot hardware geometry;
- real leg and steel leg-bracket geometry;
- playfield UCFL202 bearing geometry;
- PC drawer slide geometry;
- lockdown/siderail fabrication concept;
- playfield/backglass display service envelopes;
- rear service-door/lock geometry;
- cable-passport, fan and vent openings.

No coordinated electronics purchase is required for this phase. Buy only physical components whose actual geometry must be measured before CNC freeze.

## Phase 1 — Woodworking / cabinet shell

Buy first:

- 18 mm structural plywood (Brazil baseline: good-quality compensado naval, preferably virola; acceptable alternatives only after inspection);
- optional 15 mm plywood for service doors/removable panels where specified;
- glue and non-electronic structural fasteners;
- backbox keyed service-door lock, continuous hinge and gasket;
- insect mesh/filter media and finger guards if their openings are included in the CNC batch;
- any geometry-critical imported/measured hardware required for the first CNC batch.

Required process:

1. measure the production plywood;
2. cut/test the CNC tolerance coupon;
3. regenerate groove/tab dimensions from measured stock;
4. cut the cabinet/backbox parts;
5. complete a full dry fit before glue-up.

Deliverables at phase end:

- main cabinet assembled and square;
- nominal 600 mm body geometry verified;
- captured bottom/front/rear/crossmember joinery proven;
- leg-corner reinforcement installed;
- backbox shell assembled and lockable;
- rear shelf/backbox floor matched interface complete;
- CNC-located cable passports/fan/service openings present;
- no electronics required to continue.

## Phase 2 — Mechanical pinball hardware

Buy/install:

- four real pinball legs;
- levelers and actual steel brackets/backing;
- retractable/lift wheel solution;
- custom 600 mm lockdown bar and receiver prototype/final hardware;
- siderails / glass-channel metalwork;
- WPC-style backbox hinge set, pivot bushings and pivot bolts;
- backbox upright locking bolts/captive threads;
- playfield pivot hardware including actual UCFL202 pair;
- positive playfield safety-stay hardware;
- closed-position support/latch hardware;
- 500 mm-class locking PC drawer slides.

Do **not** buy final gas struts yet unless the final display/cradle mass and CG are already known.

Deliverables at phase end:

- cabinet stands safely on real legs;
- playing load transfers to levelers, not wheels;
- backbox folds and locks upright correctly;
- playfield cradle opens and positively supports service position;
- closed playfield position positively lands/latches;
- PC drawer slides/locks and supports 25 kg proof-test payload;
- lockdown/siderail/glass mockup interfaces are proven.

## Phase 3 — Displays and glazing

Select from the **actual Brazil market at that time**.

Buy/install:

- 42/43-inch 4K native-120-Hz-or-better playfield display within the permanent service envelope;
- preferred 31.5/32-inch backglass monitor;
- DMD/FullDMD only if included in the pre-electronics mechanical-fit phase;
- display-specific replaceable VESA adapters / bezel fillers;
- final playfield tempered glass only after lockdown/siderail proof fit;
- backbox protective glazing.

Deliverables at phase end:

- principal displays mechanically mounted;
- exact playfield VESA adapter frozen;
- final moving mass/CG measured;
- final gas-strut force/mount geometry solved and installed;
- backglass carriage adjusted to bezel plane;
- displays removable without destructive cabinet work;
- playfield opening sweep and folded-backbox sweep physically verified;
- display cable service loops usable.

## Phase 4 — PC mechanical integration

Buy/install:

- selected open ATX chassis/test-bench frame;
- replaceable tray adapter;
- GPU restraint if needed for mechanical fit.

The PC itself may remain electrically incomplete. The internal drawer architecture is already mechanically proven in Phase 2; this phase proves the chosen chassis adapter/removal workflow.

## PHASE GATE — STRUCTURE READY

The coordinated electronics/DOF purchase does not begin until Phases 1–4 pass inspection.

Structure-ready requires:

1. CNC coupon and measured-stock values recorded;
2. wood cabinet/backbox complete and square;
3. legs/levelers/mobility complete;
4. lockdown, siderails and final glass fit;
5. backbox hinge/fold/lock system proven;
6. keyed rear service door operational;
7. playfield cradle/pivot/safety stays/closed latches proven;
8. final display adapter and gas-strut specification validated with actual display;
9. backglass/DMD carriage envelopes proven;
10. PC drawer and chassis adapter proven;
11. fan/vent/cable-passport/raceway geometry present;
12. SSF and toy zones remain available;
13. no dangerous exposed mains provisions are present;
14. BOM and part labels reconcile with the assembled structure;
15. no foreseeable woodworking rework is required for electronics installation.

Only after this gate should the full electronics/toy purchase be made in one coordinated batch.

## Phase 5 — Electrical power and control

Purchase as a coordinated electronics batch:

- protected mains entry/distribution;
- auxiliary DC supplies;
- controller boards;
- USB/network interfaces;
- fan controllers;
- amplifiers;
- wiring, fuse blocks, connectors and harness materials.

## Phase 6 — DOF / feedback / lighting toys

Purchase/install selected contactors/impact devices, shaker, gear motor, knocker, chimes, blower, flashers/strobes/beacon, addressable LEDs and topper interfaces.

## Phase 7 — Software / commissioning

- Windows/runtime installation;
- VPX/PinUP/DOF/SSF setup;
- thermal tests;
- current/fuse verification;
- final cable dressing;
- safety inspection;
- as-built documentation.

## Procurement rule

Every BOM line has a phase. Do not buy later-phase electronics merely because they are available unless they are required as a physical fit sample. The permanent structure should be validated first so short-lived electronics are purchased as late as practical.

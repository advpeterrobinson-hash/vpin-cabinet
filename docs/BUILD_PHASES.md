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
- actual classic pinball leg and compact steel leg-bracket geometry;
- playfield UCFL202 bearing geometry;
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
- **no bulky permanent plywood leg-corner blocks installed by default**;
- backbox shell assembled and lockable;
- rear shelf/backbox floor matched interface complete;
- CNC-located cable passports/fan/service openings present;
- no electronics required to continue.

## Phase 2 — Mechanical pinball hardware

Buy/install:

- four classic pinball legs;
- four levelers;
- compact internal steel leg brackets/backing selected from actual measured hardware;
- external removable **PinSkates-style mobility pair** for moving the machine;
- custom 600 mm lockdown bar and receiver prototype/final hardware;
- siderails / glass-channel metalwork;
- WPC-style backbox hinge set, pivot bushings and pivot bolts;
- backbox upright locking bolts/captive threads;
- playfield pivot hardware including actual UCFL202 pair;
- positive playfield safety-stay hardware;
- closed-position support/latch hardware;
- compact PC-sled locator/retainer hardware.

Do **not** buy final gas struts yet unless the final display/cradle mass and CG are already known.

Deliverables at phase end:

- cabinet stands safely on classic legs and levelers;
- leg/bracket corner proof test passes without requiring oversized wooden corner furniture;
- PinSkates can be attached/removed without modifying the cabinet and are removed for play;
- backbox folds and locks upright correctly;
- playfield cradle opens and positively supports service position;
- closed playfield position positively lands/latches;
- lift-out PC sled locates securely, releases from above and supports the 25 kg proof-test payload;
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
- replaceable lift-out sled adapter;
- quick-disconnect PC service harness/connectors;
- GPU restraint if needed for mechanical fit.

The PC itself may remain electrically incomplete. This phase proves that the selected chassis fits the **top-access lift-out service sled** and can be removed vertically with the playfield raised. No front service opening or long drawer-slide mechanism is required.

## PHASE GATE — STRUCTURE READY

The coordinated electronics/DOF purchase does not begin until Phases 1–4 pass inspection.

Structure-ready requires:

1. CNC coupon and measured-stock values recorded;
2. wood cabinet/backbox complete and square;
3. classic legs/levelers and removable PinSkates mobility workflow proven;
4. lockdown, siderails and final glass fit;
5. backbox hinge/fold/lock system proven;
6. keyed rear service door operational;
7. playfield cradle/pivot/safety stays/closed latches proven;
8. final display adapter and gas-strut specification validated with actual display;
9. backglass/DMD carriage envelopes proven;
10. lift-out PC sled, retainers and chassis adapter proven;
11. fan/vent/cable-passport/raceway geometry present;
12. SSF and toy zones remain available;
13. central cabinet service volume remains accessible rather than filled with fixed furniture;
14. no dangerous exposed mains provisions are present;
15. BOM and part labels reconcile with the assembled structure;
16. no foreseeable woodworking rework is required for electronics installation.

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

Use localized removable electronics boards/rails and preserve clear top-service access. Do not permanently fill the cabinet with broad shelves if smaller modular mounts will do.

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

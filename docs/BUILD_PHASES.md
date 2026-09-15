# Build phases and procurement gates

Status: engineering planning. This document defines when materials are bought and when each subsystem is allowed to enter the build.

## Phase 0 — Design freeze inputs

Before ordering CNC wood, confirm:

- measured plywood thickness from the actual sheet stock;
- CNC provider tooling and tolerance coupon;
- 580 mm main-body geometry;
- 780 mm backbox geometry;
- backbox hinge/pivot hardware geometry;
- leg and leg-bracket geometry;
- lockdown-bar fabrication geometry;
- playfield and backglass display envelopes;
- PC drawer slide envelope;
- rear service-door/lock geometry;
- cable-passport, fan and vent openings.

No electronics purchase is required for this phase except any physical components whose geometry must be measured before CNC freeze.

## Phase 1 — Woodworking / cabinet shell

Buy first:

- 18 mm structural plywood (Brazil baseline: good-quality compensado naval, preferably virola; acceptable alternatives only after sheet-quality inspection);
- optional 15 mm plywood for removable service doors/bezels where specified;
- glue, metric bolts, threaded inserts/captive nuts, washers and screws;
- backbox keyed service-door lock, piano/continuous hinge and gasket;
- insect mesh/filter media and finger guards if their openings are included in the CNC batch;
- WPC-style backbox hinge hardware if imported/measured parts are needed to confirm CNC hole locations.

Deliverables at phase end:

- main cabinet assembled and square;
- backbox shell assembled and lockable;
- rear shelf/backbox floor matched interface complete;
- all CNC-located cable passports, fan openings, service bays and hardware pilot holes present;
- structural doublers/crossmembers installed;
- no electronics required to continue.

## Phase 2 — Mechanical pinball hardware

Buy/install:

- four real pinball legs;
- four levelers and associated plates/brackets;
- retractable/lift wheel solution;
- custom lockdown bar and receiver;
- siderails / glass channels;
- WPC-style backbox hinge set, pivot bushings and pivot bolts;
- backbox upright locking bolts/captive threads;
- playfield OLED hinge/cradle hardware, gas struts and independent safety prop;
- PC drawer slides and removable PC chassis adapter platform.

Deliverables at phase end:

- cabinet stands safely on real legs;
- cabinet can be moved using play-isolated retractable wheels;
- backbox folds and locks upright correctly;
- playfield cradle opens safely and cannot slam shut;
- PC drawer extends/locks and supports proof-test payload;
- glass/lockdown-bar/siderail mechanical interfaces are complete.

## Phase 3 — Displays

Buy/install before electronics phase:

- LG OLED42C5 playfield display (or final confirmed replacement if availability changes before purchase);
- preferred 31.5/32-inch backglass monitor;
- DMD/FullDMD display only if the user elects to include it in the pre-electronics mechanical fit phase;
- display-specific VESA adapter plates / bezel fillers;
- playfield glass / backbox protective glazing.

Deliverables at phase end:

- both principal displays mechanically mounted;
- backglass carriage adjusted to bezel plane;
- displays removable without destructive cabinet work;
- playfield hinge sweep and folded-backbox sweep physically verified;
- display cable service loops and cable passports physically usable.

## Phase 4 — PC mechanical integration

Buy/install:

- selected open ATX chassis or test-bench frame;
- drawer platform adapter;
- drawer restraints / lock-open and lock-closed hardware;
- positive GPU restraint if a GPU is already available for mechanical fit.

The PC itself may remain electrically incomplete. The purpose of this phase is to finish the cabinet's mechanical computer interface before toys/electronics are purchased.

## PHASE GATE — STRUCTURE READY

The electronics phase does not begin until Phases 1–4 have passed inspection.

The structure-ready gate requires:

1. wood cabinet and backbox complete;
2. real legs/levelers and mobility hardware complete;
3. lockdown bar, siderails and glazing fit;
4. backbox hinge/fold/lock system proven;
5. keyed rear service door operational;
6. playfield OLED cradle proven through full service sweep;
7. backglass and DMD carriage envelopes proven;
8. PC drawer proven;
9. fan/vent/cable-passport/raceway geometry present;
10. all planned electronics/toy zones remain accessible;
11. no dangerous exposed mains provisions are present;
12. BOM and part labels reconcile with the assembled structure.

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

Purchase/install the planned feedback inventory, including selected contactors/solenoids, shaker, gear motor, knocker, chimes, blower, flashers/strobes/beacon, LEDs and future topper interfaces.

## Phase 7 — Software / commissioning

- Windows/runtime installation;
- VPX/PinUP/DOF/SSF setup;
- thermal tests;
- current/fuse verification;
- final cable dressing;
- safety inspection;
- documentation of as-built substitutions.

## Procurement rule

Every BOM line has a phase. Do not buy later-phase electronics merely because they are available unless they are required as a physical fit sample. This minimizes stale electronics while ensuring the permanent structure is fully validated first.

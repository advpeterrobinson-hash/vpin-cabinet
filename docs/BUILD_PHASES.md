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
- actual 450 mm-class rear PC slide thickness/travel/hole pattern;
- rear PC service-door hinge/latch/frame geometry;
- lockdown/siderail fabrication concept;
- playfield/backglass display service envelopes;
- selected rear-face or underside mains/Ethernet geometry;
- cable-passport, fan and vent openings.

No coordinated electronics purchase is required for this phase. Buy only physical components whose actual geometry must be measured before CNC freeze.

## Phase 1 — Woodworking / cabinet shell

Buy first:

- 18 mm structural plywood (Brazil baseline: good-quality compensado naval, preferably virola; acceptable alternatives only after inspection);
- optional 15 mm plywood for service doors/removable panels where specified;
- glue and non-electronic structural fasteners;
- backbox keyed service-door lock, continuous hinge and gasket;
- main-cabinet rear PC service-door hinge/latch/frame materials once the exact local hardware is selected;
- insect mesh/filter media and finger guards if their openings are included in the CNC batch;
- any geometry-critical imported/measured hardware required for the first CNC batch.

Required process:

1. measure the production plywood;
2. cut/test the CNC tolerance coupon;
3. regenerate groove/tab dimensions from measured stock;
4. finalize the rear-panel PC-door aperture against actual leg brackets and rear I/O hardware;
5. cut the cabinet/backbox parts;
6. complete a full dry fit before glue-up.

Deliverables at phase end:

- main cabinet assembled and square;
- nominal 600 mm body geometry verified;
- captured bottom/front/rear/crossmember joinery proven;
- no bulky permanent plywood leg-corner blocks installed by default;
- main-cabinet rear PC service-door opening/frame/door dry-fit proven;
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
- actual simple **450 mm-class rear PC slide pair** and one simple positive stowed shelf retainer;
- rear PC door hinge/latch/gasket hardware.

Do **not** buy final gas struts yet unless the final display/cradle mass and CG are already known.

Deliverables at phase end:

- cabinet stands safely on classic legs and levelers;
- leg/bracket corner proof test passes without oversized wooden corner furniture;
- PinSkates can be attached/removed without modifying the cabinet and are removed for play;
- backbox folds and locks upright correctly;
- playfield cradle opens and positively supports service position;
- closed playfield position positively lands/latches;
- rear PC service door opens from behind the machine without interference;
- small flat PC shelf slides **450 mm rearward through the backdoor**, positively retains when stowed and passes the 20 kg proof test;
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
- shelf-to-case mounting bolts/spacers as required by the actual case;
- ordinary dressed PC cables/connectors;
- GPU restraint if needed for mechanical fit.

The PC itself may remain electrically incomplete. The open case bolts **directly to the small rear pull-out shelf**. There is no second sled. This phase proves the actual case mounting pattern, full 450 mm **rearward** travel, connector/cable clearances and complete removal from behind the machine.

Routine PC service must be possible without opening the playfield.

## PHASE GATE — STRUCTURE READY

The coordinated electronics/DOF purchase does not begin until Phases 1–4 pass inspection.

Structure-ready requires:

1. CNC coupon and measured-stock values recorded;
2. wood cabinet/backbox complete and square;
3. classic legs/levelers and removable PinSkates mobility workflow proven;
4. lockdown, siderails and final glass fit;
5. backbox hinge/fold/lock system proven;
6. keyed backbox rear service door operational;
7. main-cabinet rear PC backdoor operational;
8. playfield cradle/pivot/safety stays/closed latches proven;
9. final display adapter and gas-strut specification validated with actual display;
10. backglass/DMD carriage envelopes proven;
11. rear PC shelf, stowed retainer, direct-mounted open case and ordinary cable disconnection/dressing proven;
12. fan/vent/cable-passport/raceway geometry present;
13. SSF and toy zones remain available;
14. central cabinet service volume remains accessible rather than filled with fixed furniture;
15. no dangerous exposed mains provisions are present behind either rear service door;
16. BOM and part labels reconcile with the assembled structure;
17. no foreseeable woodworking rework is required for electronics installation.

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

Use localized removable electronics boards/rails and preserve clear service access. The rear PC door may expose PC hardware only; bare mains distribution remains in a separate touch-safe enclosure.

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

## v25 detailing and measurement checkpoint — 2026-09-24

Use [HARDWARE_MEASUREMENT_PACK_V25.md](HARDWARE_MEASUREMENT_PACK_V25.md) for the consolidated immediate procurement list and exact datum-based measurements. [CNC_STRUCTURE_DETAIL_V25.md](CNC_STRUCTURE_DETAIL_V25.md) records the joinery review and retained 36-part structure. Run `make cnc-detail` to regenerate the separate joint preview, ledgers and eight-view gallery. Hardware-pattern coordinates remain blank; four ventilation/passport design blockers remain explicit. This checkpoint does not advance the structure-ready or manufacturing gates.

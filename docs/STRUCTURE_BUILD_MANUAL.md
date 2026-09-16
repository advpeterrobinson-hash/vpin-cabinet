# Structure build manual

Status: living assembly manual. Dimensions/hole locations marked provisional must be generated from final CAD before manufacturing release.

This manual covers the **structure-ready phase** only: woodworking, backbox, legs, playfield/display mechanics, glazing, and PC drawer. Electrical power, control boards and DOF toys begin only after the structure-ready gate is passed.

## 0. Safety first

- Do not energize any mains-voltage wiring during the woodworking/mechanical build.
- Any later 127/220 V work must use enclosed terminals, protective earth where required, branch protection, strain relief and a documented isolation/service procedure.
- If a future step requires exposure to mains wiring, the manual must show a shock-hazard warning before the step.
- The backbox rear service door may expose low-voltage service hardware, but must not expose bare mains terminals.
- Never service the raised playfield display using gas struts alone: engage both independent positive mechanical safety stays.
- Isolate cabinet mains power before manipulating the playfield display harness, pivot, gas struts, safety stays or removing the moving module.
- Never transport the machine with the backbox upright.

## 1. Part-identification rule

Before assembly, lay out every CNC/fabricated part with its engraved ID facing upward and reconcile it against `bom/STRUCTURE_BOM.csv`, `bom/STRUCTURE_PARTS.csv` and `docs/PART_LABELING.md`.

Do not assemble any unlabeled or ambiguous CNC part until its identity is resolved.

## 2. Material inspection and CNC coupon

1. Measure plywood thickness at several points on each sheet with calipers.
2. Record the measured values in the as-built log.
3. Reject badly warped sheets, delaminated edges and sheets with large visible internal voids in critical structural areas.
4. Have the CNC shop cut `CNC-COUPON-001-R1` before the production sheets.
5. Test actual dado/tab/insert/engraving/tool-radius fits.
6. Confirm the provider's cutter compensation and internal-radius/dogbone conventions.
7. Update production clearances before cutting the cabinet.

Nominal 18 mm is a design label; **measured sheet thickness controls the final toolpaths**.

## 3. Main cabinet dry fit — v0.20

Primary parts:

- `CAB-SIDE-001L-R1`
- `CAB-SIDE-001R-R1`
- `CAB-FRONT-001-R1`
- `CAB-REAR-001-R1`
- `CAB-BOTTOM-001-R1`
- `CAB-XMEM-010-R1`
- `CAB-XMEM-011-R1`
- `CAB-XMEM-012-R1`
- `CAB-REAR-SHELF-001-R1`

Current nominal captured-joinery packaging uses a **6 mm capture depth**. At nominal 18 mm stock this leaves 12 mm of material behind the side-wall pockets. The nominal production-blank packaging is:

- front/rear captured width: **576 mm**;
- bottom captured blank: **576 x 1284.1 mm**;
- bottom panel bottom elevation: **18 mm**;
- low crossmembers: nominal **576 mm captured width x 80 mm high**, at Y 260 / 650 / 1040 mm.

These are engineering values, not final toolpaths. Actual groove width/tab values follow the measured plywood and tolerance coupon.

Procedure:

1. Dry-fit the bottom into the four-edge capture geometry.
2. Add front and rear panels without glue.
3. Install the three low crossmembers.
4. Install the reinforced rear shelf.
5. Check that all self-locating joints seat fully without hard hammering.
6. Measure both cabinet diagonals; they should match within the final release tolerance.
7. Confirm **600 mm external width**, nominal **564 mm full-thickness inner width**, and the current WPC-inspired side profile.
8. Confirm the PC drawer, playfield cradle, service-I/O, gas-strut, safety-stay and toy keepout envelopes are unobstructed.
9. Confirm low crossmembers remain below the SSF exciter-height zones.
10. Disassemble for finishing/joint preparation if the selected finish requires it.

No permanent glue-up occurs until the dry-fit inspection passes.

## 4. Leg-corner reinforcement — v0.20

Each corner uses two local plywood reinforcement parts plus the selected steel leg bracket/backing:

Front-left:
- `CAB-LEG-SIDE-DBLR-FL-R1`
- `CAB-LEG-END-DBLR-FL-R1`

Front-right:
- `CAB-LEG-SIDE-DBLR-FR-R1`
- `CAB-LEG-END-DBLR-FR-R1`

Rear-left:
- `CAB-LEG-SIDE-DBLR-RL-R1`
- `CAB-LEG-END-DBLR-RL-R1`

Rear-right:
- `CAB-LEG-SIDE-DBLR-RR-R1`
- `CAB-LEG-END-DBLR-RR-R1`

Nominal v0.20 packaging:

- sidewall doubler: about **220 x 240 x 18 mm**;
- front/rear end-panel doubler: about **160 x 240 x 18 mm**;
- local structural wood target: approximately **36 mm** before the steel bracket/backing.

Each leg load is transferred through:

`leg -> through-bolts -> steel internal bracket/backing -> doubled plywood corner -> cabinet shell/crossmembers`

The primary leg bolts are through-bolts; they are not wood screws into a single 18 mm panel.

The exact leg bracket/bolt pattern remains **blocked from CNC** until the actual legs and bracket set are selected and measured. Retractable-wheel keepout volume is reserved at each corner; playing load must remain on the levelers.

## 5. Main cabinet glue-up

After dry fit and the production joinery values are validated:

1. Protect threaded inserts and machined surfaces from glue.
2. Apply appropriate wood glue to structural joints according to the chosen plywood/finish system.
3. Seat dados/tabs fully.
4. Clamp against a flat reference.
5. Re-check diagonals before cure.
6. Install mechanical fasteners/captive hardware where specified.
7. Allow full cure before installing legs or applying dynamic loads.

The release manual will list exact clamp locations and tightening sequence after final joinery CAD.

## 6. Backbox shell dry fit

Primary parts:

- `BB-SIDE-001L-R1`
- `BB-SIDE-001R-R1`
- `BB-TOP-001-R1`
- `BB-FLOOR-001-R1`
- `BB-XMEM-001-R1` lower structural crossmember
- `BB-XMEM-002-R1` upper structural crossmember
- fixed rear perimeter/shear-frame pieces
- `BB-DOOR-001-R1` keyed service door

Check:

- 780 mm external width;
- 90 mm nominal side overhang over the centered 600 mm body;
- common centerline marked;
- rear edge datum marked;
- primary and reserve cable passports align with the main rear shelf;
- lock-bolt axes align from the shared centerline;
- 120 mm fan openings and filters remain clear of monitor rails;
- service-door aperture retains fixed structure around all four sides.

## 7. Keyed rear service door

The service door is maintenance access, **not** the primary backbox structural diaphragm.

Install:

- continuous/piano hinge;
- keyed cam/panel lock;
- full perimeter closed-cell gasket;
- door stops/captive restraint as finalized;
- optional second compression point if prototype testing shows door rattle.

With the door closed and locked, there must be no large unguarded opening into the backbox.

## 8. Backbox hinge installation

Hardware IDs:

- `BB-HNG-01` — 01-9011-L
- `BB-HNG-02` — 01-9011-R
- `BB-HNG-03` — two 02-4352 pivot bushings
- `BB-HNG-04` — two 4322-01139-12B pivot bolts

Important: the backbox rests on the **rear shelf** when upright. The side hinges provide the pivot; the dedicated lock bolts clamp/stabilize the backbox in operating position.

For the 780 mm backbox centered over the 600 mm body, the current WPC custom-width hinge-floor inset calculation is approximately **59.84 mm each side**. Exact bracket mounting holes remain blocked until actual hinge hardware is measured.

Procedure after final CAD validation:

1. Fit the left/right hinge brackets to the CNC-located backbox-floor/side pattern.
2. Install the two cabinet pivot bushings into the CNC-located cabinet side holes.
3. Engage the pivot bolts.
4. Raise the backbox to the upright position.
5. Confirm the backbox floor sits flat on the reinforced rear shelf.
6. Install the two upright lock bolts through the backbox floor into the captive shelf threads.
7. Confirm the backbox cannot rock or lift.
8. Remove/release upright locking bolts and test a controlled forward fold.
9. Verify the cable-passport service loop never pinches.
10. Verify the folded backbox lands only on dedicated padded transport rests.

Do not use the hinges as the sole operating-position restraint.

## 9. Backglass/DMD mechanical system

Install the fixed internal rail cage to the dedicated structural backbox crossmembers.

The rail cage must remain adjustable in:

- backglass vertical position;
- backglass depth/front-back position;
- limited horizontal centering;
- DMD vertical/depth position.

Use removable VESA/tray adapter plates. No permanent wood panel should contain monitor-model-specific VESA holes.

The backglass monitor should be replaceable through the front; routine cable/fan/LED/toy service should be possible through the keyed rear door.

## 10. Main playfield mechanics — v0.18/v0.19 baseline

The active moving package is `PlayfieldMechanicsV18`; cabinet-side fixed support/anchor load paths are packaged by `PlayfieldFixedAnchorsV19`. Historical LG-specific groups remain only for traceability.

Install/prepare:

- two 18 mm CNC plywood longitudinal cradle rails below the display;
- three 18 mm under-display cradle crossmembers;
- 36 mm local left/right rear pivot doublers;
- laminated rear pivot beam;
- replaceable model-specific VESA carrier;
- two 140 x 80 x 6 mm steel pivot cheek plates;
- two 15 mm short pivot journals;
- two UCFL202 15 mm flange bearings with cabinet-side steel backing plates;
- dual gas struts as lift assistance only;
- **two independent positive mechanical safety stays**;
- fixed sidewall anchor doublers/steel captive plates for stays/struts;
- two structural closed-position landing supports with cabinet-side load paths;
- two positive closed-position latch/strike assemblies;
- moving power/video/control harness service loop with strain relief.

The permanent cradle/cabinet is **not tied to one TV model**. The service envelope targets compact 42/43-inch 16:9 gaming displays up to approximately:

- 560 mm physical cross-cabinet chassis width;
- 970 mm physical front-to-rear chassis length;
- 55 mm depth;
- 12 kg display mass design limit;
- 2 mm installation clearance per side across the cabinet.

The 600 mm body provides **564 mm between full-thickness nominal 18 mm sidewalls**, so the normal 560 mm target plus 2 mm clearance each side fits with **no sidewall pockets/notches**.

### 10.1 Pivot hardware gate

Do not machine cabinet-side UCFL202 bolt holes from catalogue dimensions. Purchase the actual bearing pair first and measure the physical housing/bore/hole pattern.

Set screws alone are not accepted as axial retention. Use a positive journal-end retention feature in the final design.

### 10.2 Gas-strut gate

Do **not** buy final gas struts yet. The current 250–400 N/strut range exists only to reserve geometry and sourcing options.

Final force and both attachment points require the exact display, finished cradle mass, measured moving center of gravity, final hinge axis and physical opening-force testing.

### 10.3 Safety stays

Both stays must positively engage before a person works beneath the raised playfield. Friction-only lid stays are prohibited as the maintenance safety device.

### 10.4 Closed-position support

The playfield does not hang on the hinge/gas struts during normal play. It lands on two structural supports and is held down by two positive latches so nudge/DOF loads do not hammer the pivot or bounce the display.

### 10.5 Moving harness

Reserve at least 300 mm service-loop length, R50 dynamic bend radius and support/strain relief within 100 mm of both moving/fixed sides.

## 11. Legs, levelers and retractable mobility

1. Install the actual measured steel leg brackets/backing plates.
2. Through-bolt all four real pinball legs through the reinforced corner system.
3. Install levelers.
4. Install the retractable/lift wheel assemblies.
5. Confirm playing load transfers to the levelers, not the casters.
6. Verify cabinet stability during simulated nudge loads before displays/electronics are added.

## 12. Lockdown bar, siderails and glass — v0.20

The 600 mm cabinet intentionally permits custom/local-fabricated metalwork.

Current engineering packaging:

- custom lockdown bar outer width: **600 mm**;
- siderail top-flange envelope: about **1120 mm along the slope x 32 mm**, nominal 2 mm sheet envelope;
- playfield glass target: **575 x 1100 x 5 mm tempered glass**, where 1100 mm is the physical cut length along the cabinet slope;
- nominal side cover around the glass target: **12.5 mm per side**.

The glass is **not purchase-ready**. Install/mock up in this order:

1. temporary/mock siderail or metal-shop sample profile;
2. lockdown receiver/lever concept;
3. custom lockdown bar sample or fabrication prototype;
4. inexpensive test strip/template for glass width/length if useful;
5. verify front/rear edge capture and removal path;
6. only then order the final tempered glass.

Final metal DXF/PDF drawings and glass dimensions are frozen from the proof-fitted assembly, not from catalogue assumptions.

## 13. PC drawer — v0.20 internal service architecture

The PC drawer does **not** require a large opening cut through a cabinet wall.

Parts:

- `PC-SUBRAIL-001L-R1`
- `PC-SUBRAIL-001R-R1`
- `PC-TRAY-001-R1`
- selected 500 mm-class heavy-duty full-extension locking slide pair

Current packaging:

- tray: **470 x 400 x 18 mm**;
- stowed Y: approximately **690 mm**;
- forward service Y: approximately **220 mm**;
- internal service travel: **470 mm**;
- tray Z: approximately **165 mm**;
- service height envelope: **230 mm**;
- provisional slide thickness allowance: **12 mm each side**;
- preferred slide pair rating: **>=45 kg**;
- physical proof-test payload: **25 kg**.

Service procedure concept:

1. isolate cabinet power;
2. remove lockdown/glass as required and raise the playfield;
3. engage both positive playfield safety stays;
4. unlock the PC drawer;
5. slide the tray forward inside the cabinet;
6. service the PC from above;
7. for complete removal, release the slide disconnects and lift the tray/chassis upward through the open top.

The PC support subrails attach to low structure/crossmembers and remain inward of the SSF sidewall skins. Exact slide mounting holes remain blocked until the actual slide pair is measured.

## 14. Playfield display selection and installation

The playfield display is selected **late in the structure phase from the Brazil market**, not years in advance by model number.

Minimum purchasing target:

- 4K UHD 3840×2160;
- native 120 Hz or better;
- HDMI 2.1 / 4K120 or better strongly preferred;
- VRR and low-latency game mode preferred;
- chassis within the service envelope;
- VESA mounting or a safe replaceable adapter solution.

The Samsung QN90F/QN90D 43-inch chassis class and LG 42-inch C-series geometry are fit references, not mandated purchases.

After the exact display is bought:

1. measure the actual chassis and VESA-hole locations;
2. generate/fit the replaceable VESA adapter;
3. position the display longitudinally inside the cradle envelope;
4. re-solve the exact hinge/CG relationship if required;
5. recalculate gas-strut force and mounting points using measured moving mass/CG;
6. mount the selected 31.5/32-inch backglass monitor in its independent adjustable carriage;
7. fit replaceable bezel/filler parts and protective glazing;
8. re-test the full playfield opening sweep and 90-degree backbox fold with actual displays installed.

## 15. Structure-ready inspection

Do not start the coordinated electronics/DOF purchase until all items below pass:

- cabinet square and structurally complete;
- CNC coupon/joinery values recorded;
- 600 mm body / 780 mm backbox alignment verified;
- leg corners and backbox shelf reinforced;
- actual legs/levelers/mobility operational;
- lockdown bar, siderails and final tempered glass fit;
- backbox hinges and upright lock bolts operational;
- keyed rear service door operational;
- cable passports and raceway mounting holes present;
- playfield cradle safe with both independent positive safety stays;
- closed-position pads/latches positively restrain the cradle;
- backglass/DMD mounts adjustable and positively locked;
- PC drawer slides measured/installed and tray proof-tested at 25 kg;
- selected playfield display fits the service envelope;
- final display adapter and gas-strut specification validated against the actual display;
- all displays remain safe during service/transport motion;
- all part IDs/BOM lines accounted for;
- no woodworking rework is expected for the electronics/toy phase.

At this point the cabinet becomes the stable mechanical platform and the coordinated electronics purchase can begin.

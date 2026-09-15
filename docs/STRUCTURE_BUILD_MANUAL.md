# Structure build manual

Status: living assembly manual. Dimensions/hole locations marked provisional must be generated from final CAD before manufacturing release.

This manual covers the **structure-ready phase** only: woodworking, backbox, legs, playfield/display mechanics, glazing, and PC drawer. Electrical power, control boards and DOF toys begin only after the structure-ready gate is passed.

## 0. Safety first

- Do not energize any mains-voltage wiring during the woodworking/mechanical build.
- Any later 127/220 V work must use enclosed terminals, protective earth where required, branch protection, strain relief and a documented isolation/service procedure.
- If a future step requires exposure to mains wiring, the manual must show a shock-hazard warning before the step.
- The backbox rear service door may expose low-voltage service hardware, but must not expose bare mains terminals.
- Never service the raised OLED using gas struts alone: engage the independent mechanical safety prop.
- Never transport the machine with the backbox upright.

## 1. Part-identification rule

Before assembly, lay out every CNC part with its engraved ID facing upward and reconcile it against `bom/STRUCTURE_BOM.csv` and `docs/PART_LABELING.md`.

Do not assemble any unlabeled or ambiguous CNC part until its identity is resolved.

## 2. Material inspection and CNC coupon

1. Measure plywood thickness at several points on each sheet with calipers.
2. Record the measured values in the as-built log.
3. Reject badly warped sheets, delaminated edges and sheets with large visible internal voids in critical structural areas.
4. Have the CNC shop cut the project tolerance coupon before the production sheets.
5. Test the actual dado/tab/insert fits.
6. Update production clearances if required before cutting the cabinet.

Nominal 18 mm is a design label; **measured sheet thickness controls the final toolpaths**.

## 3. Main cabinet dry fit

Primary parts (provisional IDs):

- `CAB-SIDE-001L-R1`
- `CAB-SIDE-001R-R1`
- `CAB-FRONT-001-R1`
- `CAB-REAR-001-R1`
- `CAB-BOTTOM-001-R1`
- `CAB-XMEM-010-R1`
- `CAB-XMEM-011-R1`
- `CAB-XMEM-012-R1`
- `CAB-REAR-SHELF-001-R1`

Procedure:

1. Dry-fit the bottom into both side dados.
2. Add front and rear panels without glue.
3. Install the three low crossmembers.
4. Install the reinforced rear shelf.
5. Check that all self-locating joints seat fully without hammering hard.
6. Measure both cabinet diagonals; they should match within the final manual tolerance.
7. Confirm 580 mm external width and the current side-profile dimensions.
8. Confirm that the PC drawer, playfield cradle, service-I/O, gas-strut and toy keepout envelopes are unobstructed.
9. Disassemble for finishing/joint preparation if the selected finish requires it.

No permanent glue-up occurs until the dry-fit inspection passes.

## 4. Leg-corner reinforcement

Parts:

- `CAB-LEG-DBLR-001FL-R1`
- `CAB-LEG-DBLR-002FR-R1`
- `CAB-LEG-DBLR-003RL-R1`
- `CAB-LEG-DBLR-004RR-R1`
- four steel internal leg brackets/backing plates

Each leg load is transferred through:

`leg -> external bolts -> steel internal bracket/backing -> ~36 mm local plywood corner -> cabinet shell/crossmembers`

The primary leg bolts are through-bolts; they are not wood screws into a single 18 mm panel.

Verify all four leg-hole patterns against the **actual selected leg/bracket hardware** before CNC production.

## 5. Main cabinet glue-up

After dry fit and leg-pattern validation:

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
- common centerline marked;
- rear edge datum marked;
- primary and reserve cable passports align with the main rear shelf;
- lock-bolt axes align from the shared centerline, not from mismatched side edges;
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

## 10. Main playfield cradle

Install:

- independent structural TV cradle;
- rear hinge/pivot assembly;
- dual gas struts;
- independent positive safety prop;
- VESA adapter plate;
- cable service loop and strain relief.

Before installing the OLED, proof-operate the empty cradle through its full range and verify all gas-strut and safety-prop clearances.

After OLED installation, repeat sweep and safety checks with actual moving mass.

## 11. Legs, levelers and retractable mobility

1. Install internal leg brackets/backing plates.
2. Bolt on all four real pinball legs.
3. Install levelers.
4. Install the retractable/lift wheel assemblies.
5. Confirm playing load transfers to the levelers, not the casters.
6. Verify cabinet stability during simulated nudge loads before displays/electronics are added.

## 12. Lockdown bar, siderails and glass

The 580 mm cabinet may use custom metalwork.

Install sequence:

1. siderail/glass channels;
2. lockdown receiver;
3. custom lockdown bar;
4. test glass strip/mockup if used;
5. final tempered playfield glass only after fit is verified.

The release drawings will provide separate local-fabrication DXF/PDF files for custom metalwork.

## 13. PC drawer

Install reinforced slide subrails tied to structural crossmembers.

Install heavy-duty full-extension locking slides and `PC-TRAY-001-R1`.

Before electronics:

- proof test with at least the documented 25 kg verification payload;
- confirm lock-open and lock-closed behavior;
- confirm no contact with the bottom panel, cable routes or future toys;
- verify the drawer can be removed/reinstalled with ordinary hand tools.

## 14. Displays

Only after all structural motion tests pass:

- mount the LG OLED42C5 in the playfield cradle;
- mount the selected 31.5/32-inch backglass monitor in the adjustable carriage;
- adjust display face to bezel datum;
- fit replaceable bezel/filler parts;
- install protective glazing.

Re-test playfield service opening and 90-degree backbox fold with the actual displays installed.

## 15. Structure-ready inspection

Do not start the electronics shopping/installation phase until all items below pass:

- cabinet square and structurally complete;
- leg corners and backbox shelf reinforced;
- legs/levelers/mobility operational;
- lockdown bar, siderails and glass fit;
- backbox hinges and upright lock bolts operational;
- keyed rear service door operational;
- cable passports and raceway mounting holes present;
- playfield cradle safe with independent prop;
- backglass/DMD mounts adjustable and positively locked;
- PC drawer proof-tested;
- displays fit and remain safe during motion;
- all part IDs/BOM lines accounted for;
- no woodworking rework is expected for the electronics/toy phase.

At this point the cabinet becomes the stable mechanical platform and the coordinated electronics purchase can begin.

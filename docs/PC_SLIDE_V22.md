# PC service slide v0.22 — one shelf, two slides, open case bolted direct

Status: owner-directed engineering packaging; not manufacturing-ready.

## Owner correction

The v0.20 long drawer and v0.21 lift-out sled are both superseded for PC service. The desired architecture is intentionally simpler:

`open PC case -> bolts -> one flat sliding shelf -> two side-mount slides -> cabinet sidewalls`

There is no drawer box, no second removable sled and no front cabinet opening.

## Reference architecture

The owner-supplied open PC case reference measures approximately **440 x 265 x 128 mm**. The case is mounted as a complete open-frame PC chassis directly to the sliding shelf.

Tukkari is used only as an architectural reference: its premium cabinets advertise flexible internal shelving/partitions for the PC and feedback devices, and an open service volume rather than a closed desktop-computer compartment. Freelance Soundlabs likewise documents reinstalling its finished PC into an open case specifically to improve airflow and motherboard access.

No proprietary Tukkari dimensions are copied into this design.

## Current engineering package

- flat structural-plywood shelf: nominal **538.6 x 300 x 18 mm**;
- nominal width formula: `564 mm full inner width - 2 x 12.7 mm slide thickness`;
- actual shelf width must be regenerated after the physical slide pair is measured;
- simple **300 mm-class full-extension side-mount ball-bearing slides**;
- slides mount directly between the cabinet sidewalls and shelf edges;
- stowed shelf front datum: Y 720 mm;
- service shelf front datum: Y 420 mm;
- service travel: **300 mm**;
- the shelf remains entirely inside the cabinet and never exits through the coin-door/front panel;
- one simple positive stowed retainer is required so nudge/DOF forces cannot make the PC shelf creep or rattle.

The open case reference is centered on the shelf and has roughly 49 mm side margin and 17.5 mm fore/aft margin at nominal values.

## Service procedure

1. Physically isolate cabinet mains power before PC mechanical service.
2. Remove lockdown/glass as required.
3. Raise the playfield and positively engage both mechanical safety stays.
4. Release the simple PC-shelf stowed retainer.
5. Slide the PC shelf 300 mm toward the cabinet center.
6. Service the complete open PC case from above.
7. For complete removal, use the drawer-slide disconnect feature if provided and lift the shelf + bolted PC case through the raised-playfield opening.

Routine service should not require unplugging every PC cable; power, video, USB and network harnesses therefore need service loops sized for the full slide travel.

## Manufacturing gates

Do not machine final slide or open-case holes until the actual hardware is in hand.

Before release, measure:

- actual slide closed length and travel;
- actual slide thickness per side;
- fixed/moving member mounting-hole positions;
- disconnect-tab access requirements;
- actual open-case mounting-hole pattern;
- case protrusions/connectors that affect shelf edge clearances.

The shelf width and hole pattern are then regenerated from those physical measurements.

## Mechanical proof test

The current slide-pair target is >=30 kg rated capacity and the assembled shelf receives a **20 kg static proof-test payload** before the PC hardware is installed. The positive stowed retainer must also survive simulated cabinet nudging without releasing or loosening.

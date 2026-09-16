# Cabinet rear PC service v0.23

Status: **owner-directed engineering packaging; not manufacturing-ready**.

This revision supersedes the earlier PC-service interpretations. Routine computer service is performed from the **rear of the pinball machine** through a dedicated main-cabinet backdoor. The playfield remains closed for normal RAM, SSD, GPU, cable and PC-hardware access.

## Literal service workflow

1. Go behind the machine.
2. Isolate cabinet power before touching PC hardware.
3. Open the dedicated rear PC service door.
4. Release one simple positive shelf retainer.
5. Pull the small PC shelf **rearward**, out through the backdoor.
6. Service the open PC case while it is outside the cabinet.
7. Push the shelf back in, positively retain it, dress the cable loop and close/lock the rear door.

The architecture is intentionally simple:

`rear door -> small shelf -> two short slides -> open PC case bolted directly to shelf`

There is no drawer box, no secondary sled, no front service opening and no requirement to raise the playfield for routine PC work.

## Rear door packaging

Current engineering aperture:

- raw clear opening: **520 x 280 mm**;
- X: 40..560 mm on the 600 mm rear panel;
- Z: 180..460 mm;
- door panel: approximately **544 x 304 x 15 mm** with 12 mm overlap around the opening;
- left-side continuous/piano hinge as viewed from the rear;
- keyed or tool-controlled quarter-turn/compression latch on the opposite side;
- gasketed perimeter;
- compact steel-angle reinforcement around the aperture.

The opening is intentionally above the low rear power/service-I/O fascias and above the compact rear leg-bracket envelope. It leaves substantial fixed structure above for the rear shelf/backbox load path.

## PC shelf

Current packaging:

- shelf: **460 x 285 x 18 mm** plywood;
- open-case fit reference: **440 x 265 x 128 mm**;
- 10 mm shelf margin per side/end around the reference case;
- shelf stowed Y: 1005..1290 mm;
- shelf service Y: 1305..1590 mm;
- travel: **300 mm rearward**;
- routine service position places the case essentially outside the cabinet behind the machine.

The case bolts directly to the shelf. Model-specific case holes remain blocked until the actual purchased open case is measured.

## Slides and spacer rails

Because the shelf is intentionally only slightly larger than the PC-case footprint, it does not span the full 564 mm cabinet interior.

Nominal cross-cabinet stack:

- left compact spacer rail: 39.3 mm;
- left slide: 12.7 mm;
- shelf: 460.0 mm;
- right slide: 12.7 mm;
- right compact spacer rail: 39.3 mm;
- total: 564.0 mm.

These are packaging values only. Final spacer and shelf dimensions are regenerated from the measured physical slide pair. Slide hole patterns remain blocked until the actual rails are purchased and measured.

## Cable service loop

Reserve at least **450 mm** of protected PC harness service-loop length so power/video/USB/network/control leads can follow the complete 300 mm rearward movement without unplugging for routine access.

The loop must not drag across sharp edges, leg brackets, backbox hardware or DOF mechanisms. Complete PC removal may use quick disconnects where practical.

## Rear-panel structure

The rear aperture is large enough to require a deliberate frame rather than simply cutting a hole and relying on the remaining plywood.

Current concept uses compact **25 x 25 x 2 mm steel angle or equivalent** around the aperture, tied to the fixed rear panel/side structure. This section is a packaging envelope, not a frozen fabrication drawing.

The low rear I/O zones remain below the PC door:

- rear AC/power fascia remains in its isolated enclosed mains compartment;
- rear network/HDMI/USB service fascia remains independent and replaceable.

## Electrical safety

The rear PC service door must **never expose bare mains terminals**.

- isolate cabinet mains before RAM/GPU/SSD/PC-harness service;
- mains distribution remains in a separate touch-safe enclosure;
- the PC PSU remains a closed listed/enclosed supply with a touch-safe inlet/connector arrangement;
- opening the PC door may expose low-voltage motherboard/GPU hardware, but not open mains distribution.

## Manufacturing gates

Do not release rear-panel CNC or slide/case holes until:

- actual classic rear leg brackets are measured;
- exact rear power/service fascia positions are confirmed in the final rear panel;
- physical PC case is measured;
- physical 300 mm slide pair is measured;
- rear-door hinge/latch/frame hardware is selected;
- shelf + case passes a 20 kg proof test;
- full-extension cable-loop test passes;
- rear door/frame dry fit confirms adequate panel stiffness;
- service position does not interfere with wall clearance assumptions for the intended installation.

The design must remain usable by simply providing enough space behind the machine to open the door and pull the PC shelf outward.

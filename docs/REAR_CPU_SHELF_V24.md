# Rear CPU shelf v0.24

Status: owner-directed engineering package. Not manufacturing-ready.

## Intent

Routine PC service happens from the **rear of the main pinball cabinet**. The playfield stays closed.

Workflow:

1. stand behind the machine;
2. isolate cabinet power;
3. open the dedicated rear PC service door;
4. release one simple stowed retainer;
5. pull the PC shelf straight rearward on full-extension slides;
6. service RAM / SSD / GPU / cabling with the open case substantially outside the cabinet;
7. push shelf back in and positively retain it;
8. close/lock rear service door.

## Commercial architecture reference

The PinballCabinet.com rear CPU shelf is used only as a design-pattern reference. Its published package is a 14 x 16 inch shelf with two 16 inch 3-section full-extension side-mount ball-bearing slides rated 100 lb, plus simple base/side boards.

The project does **not** copy those dimensions because the owner's open-case reference is approximately 440 x 265 x 128 mm.

## Selected orientation

Rotate the owner's open case 90 degrees in plan:

- 265 mm across cabinet X;
- 440 mm fore-aft Y;
- 128 mm high Z.

This lets the shelf be narrow across the cabinet and long in the pull direction, matching the conventional rear CPU-shelf architecture.

Nominal engineering shelf:

- 285 mm wide;
- 460 mm deep;
- 18 mm plywood;
- 10 mm nominal case margin on every plan edge.

## Rear hatch

Nominal clear aperture:

- 340 mm wide;
- 240 mm high;
- centered at X 130..470 mm;
- Z 180..420 mm.

This is intentionally much narrower than the v0.23 520 mm aperture, preserving more rear-panel structure.

Door target:

- 364 x 264 x 15 mm panel;
- 12 mm overlap each edge;
- left-side hinge as viewed from rear;
- outward opening;
- gasket;
- keyed/tool-controlled compression or quarter-turn latch.

## Slide system

Nominal packaging uses two simple 450 mm-class 3-section full-extension side-mount ball-bearing slides.

The shelf stows at Y 830..1290 mm and travels 450 mm rearward to Y 1280..1740 mm. This puts essentially the complete 440 mm-deep open case behind the cabinet for service.

The fixed slide members mount to two narrow local support rails. These rails are not broad shelves and do not fill the cabinet center.

Exact slide thickness, hole pattern and extension are blocked until the physical pair is purchased and measured.

## Electrical safety

The rear PC service door must not expose bare mains terminals. Cabinet mains distribution remains in a separate touch-safe enclosure.

Before touching RAM, GPU, SSD, motherboard or internal PC cabling, isolate cabinet power.

## Manufacturing gates

Do not release rear-panel CNC geometry until:

- actual classic rear leg brackets are known;
- actual rear-door hinge/latch hardware is known;
- actual slide pair is measured;
- actual open case is measured;
- rear service cable loop is physically proven;
- rear-panel/hatch stiffness is proof-tested.

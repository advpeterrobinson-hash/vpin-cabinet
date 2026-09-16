# Rear CPU shelf v0.24

Status: owner-directed engineering package. Not manufacturing-ready.

## Intent

Routine PC service happens from the **rear of the main pinball cabinet**. The playfield stays closed.

Workflow:

1. stand behind the machine;
2. isolate cabinet power;
3. open the dedicated rear PC service door **outward**;
4. release one simple stowed retainer;
5. unplug/dress ordinary PC cables as required for the desired extraction distance;
6. pull the PC shelf straight rearward on full-extension slides;
7. service RAM / SSD / GPU / cabling with the open case substantially outside the cabinet;
8. push shelf back in and positively retain it;
9. close/lock rear service door.

## Commercial architecture reference

The PinballCabinet.com rear CPU shelf is used only as a design-pattern reference. Its published package is a 14 x 16 inch shelf with two 16 inch 3-section full-extension side-mount ball-bearing slides rated 100 lb, plus simple base/side boards.

The project does **not** copy those dimensions because the owner's open-case reference is approximately 440 x 265 x 128 mm.

## Selected orientation

Rotate the owner's open case 90 degrees in plan:

- 265 mm across cabinet X;
- 440 mm fore-aft Y;
- 128 mm high Z.

Nominal engineering shelf:

- 285 mm wide;
- 460 mm deep;
- 18 mm plywood;
- 10 mm nominal case margin on every plan edge;
- shelf plane at Z 135 mm.

## Rear hatch — lowered layout

The original Z 180 mm hatch was visually and spatially too high. The active package moves the entire door/shelf system **70 mm downward**, preserving the same useful internal clearance while freeing the upper rear-cabinet volume for other equipment.

Nominal clear aperture:

- 340 mm wide;
- 240 mm high;
- centered at X 130..470 mm;
- Z 110..350 mm.

Door target:

- 364 x 264 x 15 mm panel;
- bottom Z 98 mm;
- 12 mm overlap each edge;
- left-side hinge as viewed from rear;
- **opens outward / behind cabinet** approximately 105 degrees;
- gasket;
- keyed/tool-controlled compression or quarter-turn latch.

The rear power/service fascias are correspondingly compressed into a low utility strip ending at approximately Z 85 mm, leaving a nominal 13 mm physical gap below the door panel.

## Slide system

Nominal packaging uses two simple 450 mm-class 3-section full-extension side-mount ball-bearing slides.

The shelf stows at Y 830..1290 mm and travels 450 mm rearward to Y 1280..1740 mm. This puts essentially the complete 440 mm-deep open case behind the cabinet for service.

The fixed slide members mount to two narrow local support rails. These rails are not broad shelves and do not fill the cabinet center.

Exact slide thickness, hole pattern and extension are blocked until the physical pair is purchased and measured.

## Cabling simplification

There is **no dedicated rear-CPU harness or modeled 600 mm cable-loop assembly** in the active design.

The simpler service rule is:

- cabinet power isolated before PC service;
- ordinary PC cables dressed with reasonable slack;
- unplug cables as needed before full shelf extraction;
- no permanent harness structure consuming cabinet volume.

## Electrical safety

The rear PC service door must not expose bare mains terminals. Cabinet mains distribution remains in a separate touch-safe enclosure.

Before touching RAM, GPU, SSD, motherboard or internal PC cabling, isolate cabinet power.

## Manufacturing gates

Do not release rear-panel CNC geometry until:

- actual classic rear leg brackets are known;
- actual rear-door hinge/latch hardware is known;
- actual slide pair is measured;
- actual open case is measured;
- compact rear utility-strip hardware is measured;
- rear-panel/hatch stiffness is proof-tested.

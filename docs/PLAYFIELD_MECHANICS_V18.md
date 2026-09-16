# Playfield mechanics v0.18 — integrated 600 mm / generic 43-inch service package

Status: **engineering-selected packaging; not manufacturing-ready**.

This stage replaces the old LG-specific visual service mockup as the active mechanical review model. Historical v0.4/v0.5 and v0.15 groups remain in the FreeCAD master for traceability, but the new `PlayfieldMechanicsV18` group is the review target.

## Design intent

The permanent cabinet must outlive the first playfield display. The 600 mm body therefore provides a **564 mm full-thickness internal bay**, enough for the selected generic target of **560 mm display width + 2 mm installation clearance each side** without routing/notching the nominal 18 mm sidewalls.

The display itself is never a structural member. The load path is:

`display -> replaceable VESA carrier -> CNC plywood cradle -> doubled plywood pivot zones -> local 6 mm steel cheek plates -> short 15 mm journals -> cabinet-side flange bearings/backing -> cabinet structure`

## Active packaging envelope

- cabinet outer width: 600 mm;
- full-thickness inner width: 564 mm;
- display packaging envelope: 560 x 970 x 55 mm;
- display mass design limit: 12 kg;
- preliminary cradle mass allowance: 4.5 kg;
- moving-mass packaging value: 16.5 kg;
- service opening: 70 degrees;
- exact display model remains open until the structure/display-purchase phase.

The Samsung 43-inch QN90F/QN90D chassis class and LG 42-inch C-series remain fit references only.

## Closed-position visual gate refinement

The first FreeCAD closed-position review exposed an important packaging issue that a scalar setback check did not show clearly: with the generic 55 mm-thick display envelope placed only 10 mm behind the cabinet front datum, the sloped envelope projected too far forward toward/through the 18 mm front panel.

The engineering packaging datum is therefore revised to **45 mm nominal front setback**. Because the display thickness projects forward by `depth × sin(cabinet slope)`, the actual minimum Y clearance is checked against the physical front panel, not just against the nominal setback. The current pure-Python and FreeCAD verifiers require at least **15 mm clear space behind the front panel** for the worst-case generic envelope.

This is still not the final lockdown-bar/apron dimension. Final front hardware, receiver and glass geometry may require additional space before CNC release.

## CNC plywood cradle

The primary cradle is plywood rather than a welded metal frame.

Current packaging uses:

- two 18 mm longitudinal side rails below the display;
- three 18 mm transverse crossmembers;
- 36 mm local rear pivot doublers;
- a laminated rear beam tying the two pivot zones together;
- a replaceable VESA carrier envelope with no TV-model-specific holes in permanent wood.

The cradle geometry is deliberately separated from the display's full-width clearance envelope: structural rails live below the TV chassis rather than beside it.

## Pivot interface

Retained from the accepted v0.15 architecture:

- A36/SAE 1020 steel cheek plate, 140 x 80 x 6 mm, each side;
- four M8 class 8.8 through-bolts per plate;
- 15 mm short journals rather than one full-width shaft;
- preferred bearing family: UCFL202 15 mm two-bolt flange bearing;
- cabinet-side 3 mm steel spreader/backing plates;
- positive axial journal retention independent of bearing set screws.

**UCFL202 mounting holes remain blocked from CNC release until the actual purchased bearing pair is measured.**

## Hinge-axis status

The v0.18 review datum is derived from the worst-case display envelope rather than the unavailable LG C5 chassis. It places the axis behind and below the display rear so the pivot plates/doublers can remain below the chassis.

This is still an engineering packaging datum. The longitudinal axis position may move modestly after the exact display, complete cradle mass and measured center of gravity are known.

## Gas struts

Two gas struts are retained as lift assistance only.

The FreeCAD model shows packaging lines for candidate geometry, but **the gas struts are not purchase-ready**. The current force search band is 250–400 N each solely to reserve geometry and sourcing options.

Final force and both ball-stud/bracket locations must be recalculated after:

1. exact display purchase;
2. completed cradle/VESA adapter mass;
3. measured assembled center of gravity;
4. final hinge axis;
5. physical opening-force test.

Gas springs are never the maintenance safety device.

## Dual positive safety stays

The machine requires **two independent captive steel safety stays**, one left and one right.

The first open-position visual review showed the initial packaging stays were too close to vertical to provide an intuitively strong triangular brace. The fixed stay anchor is therefore moved farther forward in the cabinet, adjacent to the middle structural region, while keeping the moving mount on the cradle. The revised packaging target keeps the open stay approximately **60–80 degrees from the cabinet Y direction**; current geometry is about 69 degrees.

This is still an envelope, not a stay fabrication drawing. Final hardware must positively engage; friction-only lid stays are not accepted. A person must be able to work under the raised playfield with both gas springs failed without the cradle falling.

## Closed-position support

The hinge and gas springs are not the play-position support system.

The closed cradle uses:

- two structural landing/support pads;
- two positive latches/retainers;
- adjustable resilient contact surfaces to eliminate rattle without allowing the OLED/TV chassis to become structural.

This prevents nudge/DOF loads from hammering the hinge or allowing the playfield assembly to bounce.

## Moving display harness

The right-rear pivot area reserves a moving harness keepout with:

- at least 300 mm service-loop length;
- minimum 50 mm dynamic bend radius;
- support/strain relief within 100 mm on both fixed and moving sides;
- separation from journal, bearing, safety-stay and gas-strut sweep zones.

Normal playfield opening should not require unplugging video/power/control leads.

## Complete cradle removal

Normal maintenance does not require removing the TV/cradle module. Complete removal is designed around the short-journal architecture:

1. isolate cabinet mains power;
2. remove lockdown bar and playfield glass;
3. raise cradle;
4. positively engage both safety stays;
5. install a temporary rated secondary support/strap;
6. disconnect display power/video at the service-loop connectors;
7. release positive journal retention and bearing locking hardware;
8. unbolt/slide the two flange bearings off the short journals;
9. lift the complete module clear, preferably with two people.

No 600+ mm shaft must be pulled sideways out of the cabinet.

## Electrical / shock warning

The display is mains powered. **Cabinet power must be physically isolated before working around the raised cradle, pivot, harness, gas struts, safety stays or complete cradle removal.** A pinched/abraded display mains lead is a blocking shock/fire defect.

## Manufacturing blocks still active

Do not issue production CNC/metal files for the playfield mechanics until all of the following are resolved:

- actual UCFL202 pair measured;
- exact playfield display selected and measured;
- exact VESA adapter frozen;
- final hinge axis/CG confirmed;
- gas-strut force and mounting geometry solved;
- safety-stay hardware selected and proof-tested;
- closed-position latch/support hardware selected and proof-tested;
- lockdown-bar/receiver/front-clearance geometry finalized;
- full FreeCAD collision sweep passed for both display and complete moving cradle;
- physical load/proof tests completed.

## Visual review target

After running `make build-playfield-mechanics-v18`, inspect the FreeCAD group:

`PLAYFIELD MECHANICS v0.18 - GENERIC 43in / PLYWOOD CRADLE / DUAL SAFETY`

Review closed and service/open states separately. The old LG-specific playfield-service groups should be hidden by the builder so the integrated v0.18 model is visually unambiguous.

# Playfield fixed anchors v0.19 — cabinet-side load paths

Status: engineering packaging; **not manufacturing-ready**.

This stage responds to visual review of v0.18. The closed support pads and service rods were mechanically plausible but visually appeared to float because their fixed cabinet load paths were not yet modeled.

## Closed play-position supports

The two cradle side rails now land directly over fixed support zones centered under the rails. Each side reserves:

- 18 mm structural-plywood sidewall doubler;
- 3 mm A36/SAE1020 steel seat projecting inward under the cradle rail;
- resilient contact pad on top of the steel seat;
- nearby reinforced positive-latch receiver zone.

The playfield TV chassis is never used as a stop. Nudge/DOF loads should pass from cradle rail -> resilient pad -> steel seat -> plywood doubler -> cabinet sidewall.

## Safety-stay fixed anchors

Each positive safety stay receives a dedicated fixed anchor zone:

- 18 mm plywood doubler bonded/structurally tied to the cabinet sidewall;
- captive 6 mm steel nut/backing plate envelope;
- final pin/slot/bolt pattern deliberately TBD until the actual stay hardware is selected.

A stay may not be attached by a wood screw into one 18 mm side panel.

## Gas-strut fixed anchors

Each gas-spring fixed end receives its own reinforced zone:

- 18 mm plywood doubler;
- captive 6 mm steel plate envelope;
- final ball-stud bracket/hole pattern deferred until the exact display/cradle mass, center of gravity, gas force, and mount geometry are solved.

Gas springs remain lift assistance only.

## Positive latch receivers

The cabinet reserves left/right receiver reinforcement near the front support seats. The exact latch remains open so locally available over-center or captive-pin hardware can be selected later without recutting the permanent cabinet structure.

## Why not freeze visible through-bolts now?

The side exterior will eventually carry artwork/siderails. We do not yet know whether the preferred hardware should use through-bolts, recessed captive nut plates, or another metal-backed internal arrangement. v0.19 therefore freezes the **reinforced load zones**, not cosmetic external fastener heads.

## Remaining manufacturing blocks

- final positive safety-stay hardware and pin/slot geometry;
- final gas-spring force and ball-stud brackets;
- final closed latch/receiver hardware;
- proof-load values and prototype test;
- SSF sidewall-zone review;
- exact CNC pocket/insert geometry after measured plywood thickness and local hardware selection.

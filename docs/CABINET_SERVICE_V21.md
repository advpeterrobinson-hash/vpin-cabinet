# Cabinet service / mobility v0.21 — classic legs, PinSkates, lift-out PC sled

Status: **owner-directed engineering packaging; not manufacturing-ready**.

This stage responds to the v0.20 visual review and the owner's reference photos. The goal is to keep the cabinet interior open and serviceable, closer to successful real/virtual pinball layouts, while avoiding bulky corner furniture and unnecessary moving mechanisms.

## Owner-directed changes

1. Keep **classic pinball legs and levelers**.
2. Remove the integrated/retractable wheel concept.
3. Use **external removable PinSkates-style mobility skates** only when moving the machine.
4. Replace the large v0.20 plywood leg-corner doublers with **compact metal-backed classic leg brackets**.
5. Replace the long forward-travel PC drawer with an **internal lift-out PC service sled**, accessed from above after the playfield is raised.

## Leg corner architecture

The v0.20 18+18 mm corner blocks were visually too bulky and consumed useful service volume. v0.21 returns to a more authentic pinball load path:

`classic leg -> through bolts -> compact formed steel internal corner bracket / spreader -> nominal 18 mm plywood shell -> captured/glued cabinet joint`

Baseline packaging:

- nominal cabinet wall: 18 mm structural plywood;
- formed steel corner bracket: ~3 mm A36/SAE1020 or equivalent;
- bracket height envelope: ~150 mm;
- bracket flange envelope: ~95 mm onto each adjoining wall;
- local 3 mm steel spreader/backing plate where the final leg bolt pattern requires it;
- **no large plywood doubler by default**.

The exact bolt pattern remains blocked until the actual classic pinball leg + internal bracket hardware is selected and measured. If a physical corner proof test shows excessive plywood bearing/crush or joint movement, add only the smallest local plywood backing required by the test.

## Mobility

The cabinet contains **no casters and no retractable-wheel hardware**.

Movement uses a removable pair of external PinSkates-style assemblies that support the classic pinball legs temporarily. They are removed for play. The machine always plays on its normal levelers.

Benefits:

- no caster cutouts or wheel keepouts inside the cabinet;
- no compromise to leg corner structure;
- no wheel rattle during force-feedback/nudging;
- no extra mechanism to maintain;
- maximum interior volume retained for PC, DOF, audio and service access.

## PC service architecture

The v0.20 forward-travel drawer is superseded. The PC does **not** slide toward or through the cabinet front.

Baseline sled envelope:

- tray: 480 x 320 x 18 mm;
- open-chassis reference: ~440 x 265 x 128 mm;
- centered laterally at X=60..540 mm;
- located between the mid/rear low structural crossmembers at approximately Y=700..1020 mm;
- mounted on four compact locator/retainer points;
- service by raising the playfield, disconnecting the quick-service harness, releasing four captive retainers and lifting the complete sled vertically;
- 250 mm vertical service ghost reserved for removal/handling;
- proof-test target: 25 kg.

This removes long drawer slides, avoids a front service opening, and leaves the cabinet floor/sidewalls available for later electronics packaging.

## Reference-photo lessons incorporated

The owner-provided examples consistently suggest several useful principles:

- successful cabinets keep a large central service volume open;
- controller boards, power supplies and feedback devices can live on localized removable boards/rails rather than permanent furniture;
- PC hardware should be reachable after the playfield is raised and should be removable without destructive work;
- compact metal brackets are preferred over huge wooden corner blocks when the load can be distributed through proper steel hardware;
- service wiring should be organized along defined edges/rails with clear access paths.

These are adopted as packaging principles, not copied dimensions.

## Manufacturing blocks

Do not freeze the following yet:

- classic leg bolt pattern;
- internal leg bracket hole pattern;
- PinSkates attachment details;
- PC sled captive retainer hardware;
- PC quick-disconnect connector panel;
- electronics mounting rails/boards.

All remain subject to physical hardware measurement and proof testing.

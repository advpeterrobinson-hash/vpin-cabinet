# Playfield Service Mechanism v0.4

Status: **engineering preview only**. Nothing in this document approves a gas spring, hinge, VESA plate, or CNC cut for purchase/manufacture.

## Objective

The LG OLED42C5 playfield must lift safely for service without requiring the user to hold the display. The mechanism must:

- preserve Williams WPC standard-body exterior geometry;
- carry OLED/hinge/strut loads through full-strength structure, never the ~8.4 mm OLED pocket skin;
- use two gas springs for balanced lift assistance;
- remain gravity-dominant when closed so the playfield does not try to open by itself;
- become gas-assist dominant toward the service position;
- retain travel reserve at both gas-spring end stops;
- provide an independent positive mechanical prop/stay in case a gas spring or mount fails;
- allow cable service loops without pinching;
- preserve room below for SSF, mechanical feedback, electronics and the PC service drawer.

## Coordinate convention

- X = cabinet left to right
- Y = cabinet front to rear
- Z = vertical

The Williams side top rises from front to rear. Derived playfield slope is approximately **9.907 degrees**.

## OLED placement baseline

The selected playfield is LG OLED42C5:

- physical playfield length: 932 mm along cabinet Y;
- cross-cabinet size: 540 mm;
- maximum depth: 41.1 mm;
- display mass: 9.8 kg;
- published VESA pattern: 300 x 200 mm.

The v0.4 engineering preview retains the reference-derived OLED front setback of **44.4 mm** and positions the OLED face approximately **8 mm below the Williams cabinet top datum**. This is a packaging assumption, not yet a glass/lockbar production dimension.

The VESA *pattern size* is known, but the exact VESA-center offset relative to the LG chassis edges remains unconfirmed. No final cradle plate may be cut until that offset is verified from an authoritative mechanical drawing or the physical TV.

## Cradle concept

Current concept:

- two longitudinal 20 x 40 mm aluminum T-slot rails;
- rails run beneath the OLED and provide a rigid moving frame;
- approximately 4 mm aluminum VESA plate between OLED and rails;
- rear full-strength hinge crossmember/shaft structure;
- hinge support reacts into full-thickness cabinet/support blocks rather than the routed OLED pocket skin.

The cradle mass is provisionally estimated at **3.5 kg**. Combined moving mass used for v0.4 calculations is therefore **13.3 kg**. This must be replaced by a measured assembled mass before final gas-spring selection.

## Hinge architecture

The v0.4 hinge axis is derived from the OLED packaging rather than chosen arbitrarily:

1. place OLED at the cabinet playfield slope;
2. project its rear face position;
3. place hinge slightly behind that position;
4. place hinge below the cabinet top so the shaft/support can sit under the moving assembly.

Current parameters:

- target service rotation: 70 degrees from closed;
- hinge rear gap: 8 mm beyond projected OLED face rear edge;
- hinge axis inset: 38 mm below the Williams cabinet top at the hinge Y location;
- preview shaft diameter: 12 mm.

The 12 mm shaft is an envelope only. Final bearing/bushing/shoulder-bolt hardware remains to be selected.

## Gas-spring screening method

Manufacturer guidance was used for the calculation method, not for final product approval.

### Stabilus

Stabilus notes that gas-spring selection for a flap requires the mass and center of gravity, desired opening angle, installation space, attachment geometry and connection technology. Their published calculation uses the gravity moment and gas-spring lever arm, with a reserve factor.

Reference:
https://www.stabilus.com/media/default/STABILUS/PDF/Stabilus_Standard_Programm_EN.pdf

### SUSPA

SUSPA publishes installation guidance including:

- piston rod preferably downward for seal lubrication;
- avoid lateral loading/misalignment;
- mounting points and spring force must be selected from the actual application geometry.

References:
https://www.suspa.com/global/products/gas-struts/faq/
https://www.suspa.com/global/products/gas-struts/gas-struts-type-16-1

SUSPA's 16-1 range includes a **316 mm extended / 135 mm stroke** dimensional class with selectable F1 force in the range that covers our preliminary screening value. This makes it a useful dimensional reference, not a purchase recommendation.

## Current gas-spring candidate

Geometry-only candidate:

- quantity: 2;
- nominal extended length: 316 mm;
- nominal stroke: 135 mm;
- nominal compressed length: 181 mm;
- preliminary F1: 260 N each;
- assumed F2/F1 force progression: 1.25;
- moving attachment: 95 mm forward of hinge;
- fixed attachment: 200 mm forward of hinge and 180 mm below hinge;
- rod-down orientation when closed;
- required travel reserve: >= 8 mm from either hard end.

With the current 13.3 kg moving-mass estimate and 466 mm CG radius, the screening model predicts approximately:

- closed center distance: ~195 mm;
- open center distance: ~304 mm;
- closed assist ratio: ~0.74 (gravity remains dominant);
- open assist ratio: ~1.45 (gas springs become dominant);
- equilibrium transition occurs roughly in the middle of the opening sweep.

This is the behavior we want conceptually: the playfield does not pop open when closed, but receives increasing assistance and remains supported near the service position.

These numbers are sensitive to actual cradle mass, actual CG, real end fittings and the final hinge/mount locations. **Do not buy the springs from these values yet.**

## Independent safety support

Gas springs are convenience/support devices, not the sole service-safety mechanism.

The final cabinet must include a positive independent mechanical support such as a captured hood-style prop rod or positive locking stay. It must be usable even if one gas spring has lost pressure or detached.

A final mechanical prop is intentionally not modeled as production hardware in v0.4 because its mounting must be coordinated with toys/electronics and the final cradle.

## v0.4 visual model

`tools/build_playfield_v04.py` generates:

- OLED closed envelope;
- OLED 70-degree service envelope;
- intermediate 20/40/60-degree sweep ghosts;
- concept longitudinal cradle rails;
- concept VESA plate envelope;
- hinge shaft preview;
- closed/open gas-spring centerline envelopes;
- a FreeCAD engineering-report object;
- spreadsheet report rows for the key kinematic values.

It deliberately does **not** generate:

- final VESA holes;
- final cabinet OLED pockets;
- hinge brackets/bushings;
- safety-prop bracket cuts;
- cable holes;
- production gas-spring end fittings.

## Validation gate before v0.5

Before this mechanism is promoted beyond preview status:

1. run `python tools/run_v04.py --report-only`;
2. run `python tools/run_v04.py --open` on the FreeCAD workstation;
3. visually inspect the entire sweep against cabinet sides/backbox region;
4. verify the script-generated hinge and gas-spring envelopes are on the intended side of the OLED/cradle;
5. record exact LG C5 VESA-center offsets;
6. select a real hinge/bushing concept;
7. determine how the safety prop will engage;
8. re-weigh/recalculate once cradle hardware is selected;
9. only then convert the preview into production brackets/pockets.

## Way of the Wrench reference role

The Way of the Wrench scratch and Big Budget series remain practical references for serviceability, cabinet population and wiring/toy organization. They are not being copied mechanically here. The v0.4 OLED lift architecture is being engineered around our own OLED, CNC-first cabinet, PC drawer and force-feedback/service requirements.


## DEC-011 — Windows runtime, Linux/FreeCAD engineering

**Status:** provisional/accepted for current planning

Develop the cabinet CAD/tooling on Linux with FreeCAD and Git. The finished pinball computer is presently planned around Windows because the complete VPX/PinUP Popper/legacy DOF ecosystem is more mature there.

This decision may be revisited if the Linux pinball ecosystem reaches equivalent compatibility before software commissioning.

## DEC-012 — Cutter CNC consultation

**Status:** accepted

Cutter CNC (`cuttercnc.com`, Brazil) is the prospective CNC fabrication provider. Before manufacturing files are frozen, confirm their preferred file/layer conventions, available tooling, internal-radius requirements, two-sided registration process, material sourcing, and practical tolerances.

## DEC-013 — Future-proof electronics envelopes over exact historical dimensions

**Status:** accepted; supersedes DEC-001 where there is a conflict

The cabinet and structural metalwork are expected to outlive multiple generations of TVs, PC hardware, controller boards, amplifiers, and power supplies. Exact Williams dimensions are therefore a design reference rather than a manufacturing mandate.

The owner explicitly approves approximately **10–50 mm** dimensional deviations where they materially improve:

- future replacement compatibility;
- service access;
- structural margin;
- cable/connector access;
- modular mounting;
- availability of generic replacement hardware.

Permanent structure should use service envelopes and replaceable interfaces. Component-specific geometry should move into replaceable carriers, bezels, filler panels, and adapters where practical.

The main playfield cabinet width was subsequently selected at **580 mm** under DEC-015 to provide a larger future 42-inch-class service envelope while retaining the Williams visual character.

## DEC-014 — Future-proof backbox width and modular monitor carrier

**Status:** accepted for v0.6 engineering

Increase the backbox target outer width from the 730.25 mm reference to **780.0 mm**. This +49.75 mm deviation intentionally uses the owner-approved tolerance to avoid locking the cabinet to unusually narrow 31.5–32 inch displays.

Target monitor service envelope:

- width: 740 mm
- height: 450 mm
- depth: 100 mm

The permanent shell uses a removable/slotted monitor carrier plus a removable cosmetic bezel/filler panel. The exact backglass model is therefore not required before the permanent backbox shell is CNC-cut; it is only required before its carrier and bezel are finalized.

## DEC-015 — 580 mm CNC-flatpack main body

**Status:** accepted engineering baseline

Adopt **580.0 mm** as the main cabinet outer-width engineering baseline. The goal is not millimetre-perfect Williams replication; the goal is a long-lived, future-proof cabinet that can be replicated from CNC plans.

The target future playfield service envelope is approximately 560 × 950 × 55 mm with 2 mm installation clearance per side. The initial LG OLED42C5 remains comfortably inside that envelope.

A custom-width lockdown bar is explicitly acceptable and is not a blocker. Siderails, brackets, and other simple metal parts may likewise be supplied as dimensioned DXF/PDF fabrication drawings so a local shop can make them without requiring the builder to own metalworking equipment.

The final project should be buildable in an apartment from outsourced CNC/fabricated parts using ordinary hand tools rather than table saws, routers, drill presses, or welding equipment.

## DEC-016 — Replaceable service-I/O fascias with vintage white engraving

**Status:** accepted for v0.8 engineering

Use three service/control zones:

1. separated rear power fascia;
2. rear low-voltage service-I/O fascia;
3. hidden coin-door and under-front service/control panels.

Permanent cabinet panels receive simple rectangular service-bay openings. Connector-specific geometry belongs on small replaceable fascias/carriers so USB, HDMI, network, and other standards can be changed years later without recutting the cabinet.

The visual language is intentionally inspired by vintage hi-fi / laboratory equipment: dark wood or black-finished wood with shallow **white-filled CNC engraving** for connector names, borders, scales, and service legends.

Initial rear service ports are:

- RJ45 Ethernet (`NETWORK`);
- HDMI diagnostic output (`SERVICE DISPLAY`);
- USB-A (`USB SERVICE`);
- USB-C;
- one blank `RESERVE` position.

The rear mains bay remains physically separated and internally enclosed; the decorative wooden fascia is not relied upon as the electrical safety enclosure.

## DEC-017 — Fold-down WPC-style backbox for transport

**Status:** accepted engineering baseline for v0.10

Use a Williams/Bally WPC-style external side-pivot hinge arrangement so the complete backbox folds **forward over the playfield** for transport, storage, and moving through apartments/elevators/vehicles.

Preferred off-the-shelf hardware family:

- `01-9011-L/R` left/right WPC backbox hinge brackets;
- `02-4352` pivot bushings;
- `4322-01139-12B` pivot bolts.

The main-side pivot starts from the established WPC datum of approximately 508.0 mm above the cabinet bottom and 38.1 mm forward of the rear edge, using a 12.7 mm pivot hole.

For the selected 780 mm backbox over the 580 mm main body, use the WPC custom-width hinge-floor formula. It yields a hinge mounting-row inset of approximately **69.84 mm from each backbox-floor side edge**.

Two independent upright safety bolts clamp the backbox floor to the cabinet rear shelf/crossmember. The hinges are not relied upon as the sole upright restraint.

The folded backbox must rest on dedicated padded structural transport supports, never on the backglass display, speaker grilles, playfield OLED, or playfield glass. The front backbox fascia should therefore keep displays/speakers recessed behind a defined fold datum; protruding decorative speaker covers are to be avoided or made deliberately removable.

A protected cable service loop must permit folding without disconnecting normal HDMI/video, power, audio, USB, or lighting harnesses and without pinching cables at the hinge.

All pivot, hinge, lock, cable-opening, and transport-rest locations are CNC-located in the final flat-pack files. Hand-aligning and drilling the hinge during apartment assembly is explicitly not the release workflow.

## DEC-018 — Dedicated cooling, cable passports, and toy-routing infrastructure

**Status:** accepted engineering baseline for v0.11

Treat ventilation, toys, power distribution and cable support as structural/CNC design inputs rather than late-stage accessories.

Backbox ventilation uses a dedicated fused **AUX 12 V** cabinet bus and a standalone thermostat/PWM controller, with two quiet 120 mm exhaust-fan positions high on the backbox rear panel as the baseline. Cooling must not depend on a motherboard fan header, display USB port or the Windows operating system.

The cabinet reserves separate routing classes for AC mains, high-current DOF/DC power, logic/data/LED wiring, low-level audio and moving display harnesses. AC mains remains physically separated from low-level wiring; inductive/high-current toy wiring is likewise routed away from audio/data where practical.

The folding backbox receives two designed cable passages rather than one improvised hole:

- primary passport: **90 × 50 mm** minimum clear opening, rounded/grommeted, with ~300 mm folding service loop;
- reserve passport: **60 × 40 mm** minimum clear opening with removable blanking cover for future topper/toy/standard expansion.

Harness supports are CNC-located. Fixed harnesses target support spacing <=250 mm; moving/hinge harnesses target <=100 mm near the moving zone. Adhesive-only tie bases are not accepted as the primary support method.

Before cabinet CNC geometry is frozen, the physical zoning/routing system must reserve capacity for a full-DOF class build including flipper/slings/bumper impact outputs, shaker, gear motor, knocker, chimes/bells, blower, strobes, RGB flashers, beacon/siren-light effects, addressable LEDs, illuminated controls and a future powered topper.

This is a packaging/power-domain decision, not yet a final toy shopping list. Exact voltage, fuse, wire-gauge, connector and controller-board selections remain BOM-stage decisions based on final hardware ratings and measured current.

## DEC-019 — Backbox floor and main rear shelf are one matched structural interface

**Status:** accepted engineering baseline for v0.12

The backbox sits on the horizontal rear shelf at the top of the main cabinet when upright. The side hinges provide the folding pivot; they are not the sole structural support in the operating position.

The backbox floor and main rear shelf are designed from a shared rear-edge/back-wall datum and a shared left-right centerline. The 580 mm cabinet shelf and 780 mm backbox floor therefore differ by 100 mm per side, and corresponding holes must never be independently dimensioned from their respective outer side edges.

Two 3/8-16 locking bolts clamp the backbox floor to captive threads in the main rear shelf. The current provisional centers are ±180 mm from the common centerline. Matching cable-passport openings in the shelf and floor use the same shared datums so there is no step or partial overlap at the fold harness.

The final CNC package must cut both members as a matched pair and validate their alignment numerically before release.

## DEC-020 — Adjustable reusable backglass and DMD carrier system

**Status:** accepted engineering baseline for v0.12

Use a fixed structural back wall for backbox stiffness, but do not permanently mount either display to it. Instead, install a rear-anchored slotted/T-slot service subframe with independent backglass and DMD carriages.

The upper backglass carriage must provide substantial up/down, front/back and horizontal centering adjustment. The target is at least 160 mm total vertical travel and approximately 100–215 mm adjustable carrier depth from the rear inner plane. The removable VESA interface should support common 75x75, 100x100, 200x100 and 200x200 patterns; unusual future patterns require changing only the adapter plate.

The lower DMD/FullDMD carriage is independent, with its own vertical/depth adjustment and replaceable bezel. It should accept a 15.6-inch FullDMD class display as well as smaller traditional-DMD-aspect screens through adapter trays/bezels. Speaker mounting remains a separate removable baffle so display replacement does not disturb the speaker load path.

All display adjustment hardware must remain positively locked when the backbox folds 90 degrees. Friction-only clamps are not sufficient.

The preferred backglass class is **31.5/32 inch 16:9** because it makes better visual use of the 780 mm backbox and is a mainstream low-cost size. The mount remains deliberately compatible with 27/28-inch replacements through carriage adjustment and a different bezel, so a future supply change does not require new cabinetry.

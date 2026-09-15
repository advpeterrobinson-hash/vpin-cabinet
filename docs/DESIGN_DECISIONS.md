# Design Decisions

This log records decisions that materially constrain the cabinet design. New decisions should be appended rather than silently rewriting history.

## DEC-001 — Preserve Williams WPC standard-body exterior

**Status:** superseded by DEC-013

Preserve the Williams WPC standard-body external cabinet proportions as the baseline instead of widening the cabinet to make the OLED easier to fit.

Baseline values:

- outer width: 558.80 mm
- side length: 1308.10 mm
- front outside height: 400.05 mm
- rear outside height: 596.90 mm
- rear top flat: 180.975 mm

**Reason at the time:** authentic proportions and compatibility with real-style pinball hardware were initially prioritized over maximizing interior width.

## DEC-002 — Metric plywood redesign

**Status:** accepted

Use nominal 18 mm plywood for the new parametric design instead of retaining the reference model's 19.05 mm / 12.70 mm imperial-stock assumptions.

At 18.00 mm main side thickness and 558.80 mm fixed outer width, nominal cabinet inside width is 522.80 mm.

**Manufacturing note:** the actual measured plywood thickness replaces 18.00 mm before production CNC files are approved.

## DEC-003 — LG OLED42C5 playfield

**Status:** accepted

Use LG OLED42C5 as the initial playfield display.

Engineering envelope used at this stage:

- native width: 932.0 mm
- native height: 540.0 mm
- maximum depth: 41.1 mm
- mass without stand: 9.8 kg
- VESA: 300 x 200 mm

When installed as a pinball playfield, the 540 mm dimension runs across the cabinet and the 932 mm dimension runs front-to-rear.

## DEC-004 — OLED side clearance pocket

**Status:** accepted for the current reference-width engineering baseline; subject to DEC-013 review before manufacturing

Use 1.0 mm nominal clearance per OLED side, yielding a 542.0 mm installed cross-width envelope.

At nominal 18 mm plywood and the historical 558.8 mm body width:

- cabinet inner width: 522.8 mm
- required side pocket depth: 9.6 mm each side
- remaining outer skin: 8.4 mm each side

The side pocket is clearance only. The reduced-thickness plywood is not permitted to carry the OLED or gas-strut structural loads.

## DEC-005 — Structural hinged OLED cradle

**Status:** accepted; geometry pending refinement

The OLED mounts to an independent cradle using its VESA interface. The cradle, not the OLED plastic chassis, carries hinge and lifting loads.

Required service features:

- rear pivot/hinge;
- dual gas struts;
- independent positive mechanical safety restraint/prop;
- controlled opening angle;
- cable service loop and strain relief;
- no slam-shut condition during service.

## DEC-006 — 32-inch 1080p backglass

**Status:** accepted

Use an inexpensive approximately 32-inch 1080p display for backglass duty. The project budget and engineering priority should favor playfield quality, force feedback, audio, and serviceability over backglass resolution.

## DEC-007 — Modular slide-out PC

**Status:** accepted

Use an open ATX metal chassis on a removable/full-extension drawer platform. Current reference chassis envelope is approximately 440 x 265 x 128 mm bare, with a larger reserved service envelope.

The drawer design must support future chassis replacement without redesigning the cabinet shell.

## DEC-008 — Force feedback and SSF are primary subsystems

**Status:** accepted

Mechanical feedback and SSF are design-driving subsystems rather than accessories to be fitted later.

- feedback toys mount rigidly and spatially appropriately;
- SSF-active wall areas remain clear of unnecessary rigid bracing;
- electronics shelves are modular and should avoid degrading cabinet-wall vibration;
- PC/electronics should be isolated from sharp mechanical shock where practical.

## DEC-009 — One external mains cord, multiple internal power domains

**Status:** accepted

The finished cabinet uses one grounded external mains connection and protected internal power distribution.

Operating states:

1. OFF
2. AUDIO ONLY / Bluetooth
3. FULL PINBALL

Audio-only mode must not require the PC, OLED, backglass, or mechanical DOF system to be powered.

## DEC-010 — Normally offline appliance

**Status:** accepted

After setup the cabinet is normally offline. Retain intentional service access through Ethernet and USB passthrough, but normal play must not depend on cloud connectivity.

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

The main playfield cabinet width must be re-evaluated before CNC freeze because the current 558.8 mm body leaves little cross-width growth margin beyond the initial 540 mm OLED. A likely evaluation range is approximately 570–575 mm, but the final width remains pending a hardware-impact review covering glass, siderails, lockdown bar, cradle, and controls.

## DEC-014 — Future-proof backbox width and modular monitor carrier

**Status:** accepted for v0.6 engineering

Increase the backbox target outer width from the 730.25 mm reference to **780.0 mm**. This +49.75 mm deviation intentionally uses the owner-approved tolerance to avoid locking the cabinet to unusually narrow 31.5–32 inch displays.

Target monitor service envelope:

- width: 740 mm
- height: 450 mm
- depth: 100 mm

The permanent shell uses a removable/slotted monitor carrier plus a removable cosmetic bezel/filler panel. The exact backglass model is therefore not required before the permanent backbox shell is CNC-cut; it is only required before its carrier and bezel are finalized.

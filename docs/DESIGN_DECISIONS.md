# Design Decisions

This log records decisions that materially constrain the cabinet design. New decisions should be appended rather than silently rewriting history.

## DEC-001 — Preserve Williams WPC standard-body exterior

**Status:** accepted

Preserve the Williams WPC standard-body external cabinet proportions as the baseline instead of widening the cabinet to make the OLED easier to fit.

Baseline values:

- outer width: 558.80 mm
- side length: 1308.10 mm
- front outside height: 400.05 mm
- rear outside height: 596.90 mm
- rear top flat: 180.975 mm

**Reason:** authentic proportions and compatibility with real-style pinball hardware are higher priorities than maximizing interior width.

## DEC-002 — Metric plywood redesign

**Status:** accepted

Use nominal 18 mm plywood for the new parametric design instead of retaining the reference model's 19.05 mm / 12.70 mm imperial-stock assumptions.

At 18.00 mm main side thickness and 558.80 mm fixed outer width, nominal cabinet inside width is 522.80 mm.

**Manufacturing note:** the actual measured plywood thickness replaces 18.00 mm before production CNC files are approved.

## DEC-003 — LG OLED42C5 playfield

**Status:** accepted

Use LG OLED42C5 as the playfield display.

Engineering envelope used at this stage:

- native width: 932.0 mm
- native height: 540.0 mm
- maximum depth: 41.1 mm
- mass without stand: 9.8 kg
- VESA: 300 x 200 mm

When installed as a pinball playfield, the 540 mm dimension runs across the cabinet and the 932 mm dimension runs front-to-rear.

## DEC-004 — OLED side clearance pocket

**Status:** accepted for engineering; not manufacturing-final

Use 1.0 mm nominal clearance per OLED side, yielding a 542.0 mm installed cross-width envelope.

At nominal 18 mm plywood:

- cabinet inner width: 522.8 mm
- required side pocket depth: 9.6 mm each side
- remaining outer skin: 8.4 mm each side

The side pocket is clearance only. The reduced-thickness plywood is not permitted to carry the OLED or gas-strut structural loads.

## DEC-005 — Structural hinged OLED cradle

**Status:** accepted; geometry pending

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

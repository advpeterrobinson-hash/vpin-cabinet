# Pinscape guide: applications to V32

[English](PINSCAPE_ACCELERATION_REVIEW.md) · [Português (Brasil)](pt-BR/PINSCAPE_ACCELERATION_REVIEW.md)

**Result:** use the guide to accelerate interface planning, bench commissioning and service documentation. Do not adopt its cabinet dimensions, legacy controller recipes or woodworking operations as V32 requirements. No geometry or hardware selection changed.

## Source and scope

Michael J. Roberts, *The New Pinscape Build Guide*, version 2.1.0, 2023-10-31. Review date: 2026-09-27. The owner supplied a complete-looking MHTML book snapshot, not just the cabinet-body page indicated by its URL fragment. We inspected the contents, license and selected chapters below; this is not verification of every circuit or chapter. [Online edition](https://head.pinscape-build-guide.pages.dev/) · [snapshot identity](../reference/pinscape/source.json).

The book declares CC BY-SA 4.0; controller software and board designs have their own licenses. Only our assessment and source metadata are added here, not the book or illustrations. Contemporary product compatibility must be checked against current manufacturer documentation. The online guide could not be retrieved by our web reader during this review; chapter findings come from the supplied snapshot.

## Prioritized application matrix

The actions and acceptance criteria below are our engineering proposals, not claims that the book validates V32.

| Priority / chapter | Useful lesson | Concrete V32 deliverable | Evidence before completion |
|---|---|---|---|
| P0 — 2.2 Serviceable Design | Access and removable modules should precede internal packaging | Access sequence for PCBase, S1/S2/S3, T1/T2/T3, displays and rear fans; connector and tool envelopes | CAD removal paths and fastener access; no unintended dependency on removing another service module |
| P0 — 2.19 Cabinet Hardware / 2.33 Plunger | Plan leg interfaces, glass channels and plunger before final panel cuts | One measured-interface record per leg bracket, plunger, glass channel and lockdown interface | Purchased hardware dimensions, original parametric coupon and fit validation; no copied STL hole patterns |
| P0 — 3.22 Addressable Light Strips | Pixel data, physical arrangement and power distribution are distinct | Matrix/strip zone register: pixel count, dimensions, voltage, current, mapping, connectors, controller port | Selected panel data; electrical budget; bench pixel-order test; then removable carrier and motion clearance |
| P0 — 2.7 Power Switching / 2.21 Grounding / 3.4 Wiring / 4.19 Fuses | Power and protection are infrastructure | OFF / AUDIO ONLY / FULL PINBALL functional diagram; separate PE, DC returns and signal references; protected branch schedule | Selected-device documentation and qualified electrical verification; touch-safe mains boundary retained |
| P1 — 2.37 Audio | Music and spatial mechanical audio need intentional routing | Channel-to-amplifier-to-exciter map for the selected StarTech interface; four SSF zones | Individual channel test before mounting; room for exciters, terminals and replaceable mounts |
| P1 — 3.10 Coil Diodes / 3.11 Coil Timers | Inductive transients and stuck-on coils require separate treatment | Per-device driver/protection/duty-cycle register plus independent feedback disable | Manufacturer-compatible protection and fault testing; software-only timing is not accepted as proof |
| P1 — 2.24 Cooling Fans | Air must traverse the occupied cabinet | Air-path view including PC, shelves, LED supplies, intake filter and fan guards | Instrumented loaded thermal test with doors closed; fan count or opening area alone does not pass |
| P1 — 2.1 Road Map / 3.3 DOF Setup | Integrate and test in stages | Reproducible commissioning checklist and backed-up configuration set | One subsystem at a time, then integrated testing; explicit versions and exported controller/DOF settings |

## Immediate finding: the six LED panels

Six 16×16 panels contain **1,536 pixels**. The guide's older WS2812 planning example uses 60 mA per pixel at 5 V. Applied only as a sensitivity scenario, that gives **92.16 A / 460.8 W** for the matrix alone; one 256-pixel panel would be 15.36 A / 76.8 W. These are **not measured consumption, a supply recommendation or our finalized budget**. Actual panel model, voltage, current limits and approved operating brightness may produce materially different results. Speaker/cabinet/gap lighting is additional.

This makes the next useful step a panel specification and power/mapping worksheet, before reserving PSU space or drawing the carrier. The [current MX-DONNY product page](https://shop.arnoz.com/en/dude-s-cab/151-mx-donny.html), checked 2026-09-27, describes a Dude's Cab expansion with eight outputs and up to 4,096 addressable LEDs. That is control capacity, not load-power capacity. Keep the [existing lighting intent](LIGHTING_INTENT_V32.md); do not add the guide's Teensy/OctoWS2811 recipe or assume its connector pinout applies to Arnoz.

The guide's power-injection spacing is specific to its strip example. Do not apply a fixed LED-count spacing to unselected 16×16 panels. Model rated connectors, conductors, branch protection and voltage drop using actual panel data. Brightness settings are a commissioning parameter, not a substitute for correctly sized protection.

## What we will not copy automatically

- Inch-based WPC cuts, historical cabinet widths, hand-routed joints and workshop assembly recipes. Our 600 mm body, measured plywood, CNC joinery/coupon workflow and replaceable guides remain authoritative.
- TV geometry that sacrifices the future display envelope; supports that obstruct removal; a return to gas springs or the historical PC drawer. V32 remains low PCBase, no drawer; positive captive props remain the service safety requirement, with detailed motion/load verification still pending.
- Old OS, device availability, software-version or purchase advice. The book is a dated reference, not the current component catalog.
- Casual PE attachment by pinching braid under a removable PSU, or treating an informal continuity reading as product qualification. Our protective-bonding design must survive normal module replacement and use specified terminations and verification. No mains construction recipe is approved by this review.
- Universal suppression-component sizing or judging unknown coil duty rating by touch. Use the selected driver/load documentation, rated protection and measured tests. Do not add a generic diode blindly to electronic motor drivers or AC loads.
- “120 mm fan” as an opening diameter. It is a nominal frame size; actual cutout, hole pitch, guard and cable envelopes require the chosen drawing/hardware.

## Next three engineering packages

1. **Interface register:** leg bracket, plunger, glass/lockdown, fans and lighting panel; distinguish known dimensions from missing measurements. Produce original coupon definitions when hardware data exist. No physical measurements are assumed while sessions are paused.
2. **Electrical and logical zone map:** map LEDs, SSF, feedback, PC and displays to power/data/service interfaces and operating modes. Produce a calculation-ready load schedule without inventing device ratings.
3. **Service and commissioning review:** show removal/access envelopes in a separate study, then write reproducible bench/configuration checks and integrated acceptance evidence. Introduce geometry only as a visible proposal for approval.

The guide supplies a useful checklist and established problem decomposition; it does not close V32's load, motion, thermal, hardware-measurement or CNC release gates.

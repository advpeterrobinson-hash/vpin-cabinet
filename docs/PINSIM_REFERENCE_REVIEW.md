# PinSim reference assessment

[English](PINSIM_REFERENCE_REVIEW.md) · [Português (Brasil)](pt-BR/PINSIM_REFERENCE_REVIEW.md)

Reviewed 2026-09-27. **Useful reference; not a CNC template or structural qualification.** V32 geometry is unchanged and manufacturing remains BLOCKED.

## Two sources, different scopes

[Jerware/PinSim](https://github.com/Jerware/PinSim) is a Teensy LC XInput controller project. The reviewed commit is `d0f35c2ff881b99ffcf9fc341bdacf742de84128` (2023-02-05). Its firmware and README describe buttons, an ADXL345 accelerometer and an analog plunger input/calibration. It is useful for control-system research, but is not a full-size CNC cabinet package and does not establish compatibility with our Arnoz lighting/control choices. No controller substitution is proposed. Firmware license: GPL-3.0.

The supplied ZIP instead identifies **PinSim Cabinet by twistedream13**, [Thingiverse 5903318](https://www.thingiverse.com/thing:5903318). Its README describes a large-format 3D-printed cabinet, fit-test pieces, print-in-place hinges and mostly M4 assembly. It also reports loose finger joints and screw-hole changes that had not yet been tested. Those details are not validated CNC joint tolerances for our plywood cabinet.

## Actual mesh inspection

The ZIP passes its CRC check. All six binary STLs have consistent triangle counts and closed meshes; FreeCAD conversion yields seven valid closed solids. `Hinge_Test.stl` has two components. These are mesh-integrity findings, not load tests. The original F3D and seven images were inventoried but the F3D parametric history was not validated.

| File | Axis-aligned extents, STL coordinate units | Solids | Recommended use |
|---|---|---:|---|
| Leg_Bracket_Test.stl | 73.308 × 139.700 × 18.397 | 1 | Study a local leg-interface fit coupon |
| Plunger_test.stl | 58.738 × 1.588 × 62.706 | 1 | Study a plunger aperture fit coupon |
| Arcade_Button_Test.stl | 33.792 × 33.172 × 9.737 | 1 | Button fit reference; tilted in source coordinates |
| Paddle_Button_Test.stl | 1.588 × 44.440 × 44.445 | 1 | Button fit reference |
| StartButtonTest.stl | 31.743 × 1.588 × 31.746 | 1 | Button fit reference |
| Hinge_Test.stl | 76.200 × 12.697 × 38.100 | 2 | Printed hinge experiment; not our backbox hinge |

STL has no unit declaration. Millimetres appear plausible but are **not confirmed**. Bounds are in the original assembly coordinate system and are not manufacturing drawings. The [manifest](../reference/pinsim/manifest.json) records exact bounds, triangles, hashes, mesh closure and solid validity.

## Leg bracket: viable as an interface study

Visual inspection shows a shallow channel/corner-like coupon with two apertures. It can help explain how to test a purchased leg bracket against a local cabinet interface. It is not evidence that a printed part can carry a roughly 150 kg cabinet under nudging loads, nor evidence that its hole spacing matches our purchased steel hardware.

Retain the steel leg/bracket load path. Measure the actual bracket angle, bolt centres and diameters, plate thickness, backing/contact footprint, bolt engagement and wrench clearance before creating an original parametric CNC interface. Validate that interface on a small coupon and then perform the required load proof. Do not import this STL as the permanent bracket or copy its holes into V32.

## Plunger: viable as an aperture study

Visual inspection shows a thin plate with a rounded triangular aperture, not a complete plunger or sensor bracket. Its approximately 1.588-unit thickness does not validate mounting through 18 mm plywood.

Use the fit-coupon approach with the selected physical plunger: measure flange/aperture, fixing pattern, threaded length and nuts, permissible panel thickness, rod travel, spring/washer envelope and rear sensor/cable access. Establish a compatible sensor independently of the PinSim firmware. Generate original CNC geometry from those measurements; keep the sensor support replaceable where possible. No plunger hole or hardware code is frozen by this review.

## Archiving and publication

The local ZIP license states “Creative Commons - Attribution - Non-Commercial - Share Alike” but gives no version or legal-code URL. We could not confirm a version from the upstream page during this review. The repository's AGENTS.md prohibits importing ambiguously licensed CAD. Consequently **the STLs, F3D, screenshots and ZIP have not been published to our GitHub**. The noncommercial restriction also requires explicit consideration before any inclusion in a commercially reusable product package; it is not overridden by our CERN license or the firmware's GPL license.

The unchanged ZIP is preserved locally, with hashes and retrieval links centralized in the [reference register](../reference/pinsim/README.md). This preserves the supplied files on this host but does not provide a remote asset backup. Exact license clarification and, where needed, author permission remain open before redistribution/adaptation. No author has been contacted on the owner's behalf.

## Next engineering use

1. Retain PinSim as a reference for input handling and small fit coupons.
2. Once physical sessions resume, measure the actual leg bracket and plunger, then create independent dimensioned interfaces and coupons.
3. Resolve CAD licensing before publishing any supplied model. Neither licensing nor mesh validity releases manufacturing.

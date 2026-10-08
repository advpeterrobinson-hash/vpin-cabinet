# V35.1 — CNC blocker audit

Status date: 2026-10-07. This audit narrows manufacturing gates to decisions that can change permanent CNC geometry. It does not release full-sheet manufacturing.

## GREEN — no longer full-sheet CNC blockers

| Interface | Decision |
|---|---|
| Lockdown bar | A-17996 / A-16055 class. Protect envelope. Dry fit after CNC; purchased-bar holes are not CNC authority. |
| Rear playfield-glass channel | 03-8091-2 class. Protect RearBearingShelf envelope/bearing surface. Locate ordinary screws during dry fit. |
| Main glass material | 5 mm tempered architecture retained. Final glass size is cut and tempered only after cabinet/channel dry fit. |
| Siderails | Optional; zero in minimum BOM. |
| Playfield display purchase target | Samsung QN43QN90FAGXZD selected by owner. Selection does not by itself change the permanent shell. Exact-envelope CAD rerun remains YELLOW. |
| CNC supplier/machine capability | Supplier profile already records 2000×3000 table, 2500×1600 stock, one-face machining, controlled-depth pockets, Ø4 cutter/R2 natural radius, 20 mm perimeter hold-down, 15 mm part spacing and accepted vector formats. No further generic machine-spec request is a CNC gate. |

## YELLOW — decision/validation required, but do not invent CNC geometry

| Interface | Remaining work |
|---|---|
| QN90F exact envelope | Rerun existing PLAY, 0–50 degree rotation, 48 mm lift-out, VESA and interference checks against 960.8 x 558.9 x 26.9 mm, 9.4 kg, VESA 200 x 200. Until rerun, call it the purchase target, not a validated display. |
| Lockdown receiver | A-16773-1 / A-9174-4 remains separate from the dry-fit bar. Decide whether its final attachment is dry-fit/manual or controls permanent machining. |
| Shelf retention S1/S2/S3 | Removable architecture retained. Freeze the final screw/insert strategy; knobs are not structurally required. |
| F06 shell reinforcement | Mechanical reinforcement remains required, but CURRENT full-sheet CNC contains no F06 pocket/pilot geometry. Select and qualify the commercial pocket-hole jig/screw family before assembly after dry fit; do not keep F06 as a full-sheet CNC gate. |
| T1/T2/T3 guide attachment | M015/M016 guide geometry is already defined; current HOLD is F05/F52/I14 hardware and repeatable placement, not guide shape. Preferred path: CAD-derived positioning/drill jig or released pilot pattern, without redesigning the structural side. |
| Backbox hinge cleats | M062 left/right cleats are already CNC-ready. Remaining issue is a qualified placement/template method; treat as assembly-positioning work unless a permanent side-panel pilot pattern is deliberately promoted. |
| DOF solenoids | Install on T1/T2/T3. Do not add model-specific permanent holes until the solenoid/adapter interface is selected. |
| LED matrix | Continue as a removable cartridge concept. Keep LED-specific geometry out of permanent cabinet wood where practical. |
| DMD/speakers and controls | Prefer replaceable panels/adapters. Any feature that truly cuts permanent wood must be frozen before its relevant CNC part is released. |

## RED — real CNC gates

| Gate | Why it blocks |
|---|---|
| Side glass channel | Measure the real 03-7135-1-class profile and validate 5 mm glass fit. Slot width/depth remain NULL until a coupon proves retention without channel deformation. |
| Actual plywood lots | Measure the real 18 mm and 12 mm production stock. Run the fit/tolerance coupon on the same machine/cutter/CAM before regenerating thickness-dependent joints. The supplier profile is already known; the missing data are the physical lots and coupon result. |
| Primary raised-playfield service support | Must be independently engineered/qualified if it changes permanent wood/hardware interfaces; current raised-service support remains HOLD. |

## Release rule

A purchased item is only a full-sheet CNC gate when its actual dimensions control permanent machining. Components installed by protected-envelope dry fit, replaceable adapters, removable panels or post-CNC manual positioning must not remain mislabeled as PURCHASE_BEFORE_CNC.

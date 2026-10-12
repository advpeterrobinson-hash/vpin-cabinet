# V35.1 — CNC blocker audit

Status date: 2026-10-12. This audit narrows manufacturing gates to decisions that can change permanent CNC geometry. It does not release full-sheet manufacturing.

## GREEN — no longer full-sheet CNC blockers

| Playfield-to-glass gap | **10 mm nominal**, display parallel to glass. This is an owner-selected conservative target rather than an industry standard. Future intentional reduction may be made by broad shims/plates at support interfaces; stacked washers are not the primary leveling method. |

| Interface | Decision |
|---|---|
| Lockdown bar | A-17996 / A-16055 class. Protect envelope. Dry fit after CNC; purchased-bar holes are not CNC authority. |
| Rear playfield-glass channel | 03-8091-2 class. Protect RearBearingShelf envelope/bearing surface. Locate ordinary screws during dry fit. |
| Main glass material | 5 mm tempered architecture retained. Final glass size is cut and tempered only after cabinet/channel dry fit. |
| Siderails | Optional; zero in minimum BOM. |
| Playfield display | Samsung QN43QN90FAGXZD is the primary reference and is mechanically validated by containment inside the already validated 560 × 970 × 55 mm / 12 kg playfield envelope. Connector/cable and physical thermal qualification remain separate. |
| CNC supplier/machine capability | Supplier profile already records 2000×3000 table, 2500×1600 stock, one-face machining, controlled-depth pockets, Ø4 cutter/R2 natural radius, 20 mm perimeter hold-down, 15 mm part spacing and accepted vector formats. No further generic machine-spec request is a CNC gate. |
| Lockdown receiver | A-16773-1 / A-9174-4 moved to **dry-fit/manual alignment** with the real lockdown bar. Current flatpack contains no H21-specific pocket/pilot; receiver is not CNC hole authority. |
| S1/S2/S3 retention | **No hand knobs.** Tool-operated M5/captive-thread architecture retained. Final screw/insert bore may be drilled at assembly after hardware selection; it no longer holds full sheets. |
| T1/T2/T3 guide positioning | Positioning solved by **CAD-derived 1:1 jig/template** using installed transforms. No new side-panel CNC pilot is required. Final F05/F52/I14 dimensions remain purchase-dependent assembly details. |
| Backbox hinge-cleat positioning | M062 is already CNC-ready; placement solved by a **CAD-derived 1:1 template** referenced to finished datums. No new permanent pilot pattern required. |
| DMD/speakers/controls | Electronics-specific openings stay on replaceable panels/adapters. They do not control permanent cabinet wood. |

## YELLOW — decision/validation required, but do not invent CNC geometry

| Interface | Remaining work |
|---|---|
| F06 shell reinforcement | Mechanical reinforcement remains required, but CURRENT full-sheet CNC contains no F06 pocket/pilot geometry. Select and qualify the commercial pocket-hole jig/screw family before assembly after dry fit; do not keep F06 as a full-sheet CNC gate. |
| DOF solenoids | Install on T1/T2/T3. Do not add model-specific permanent holes until the solenoid/adapter interface is selected. |
| LED matrix | Functional architecture accepted: 3 acrylic layers + 2 printed end caps + 4 cabinet fasteners + one detachable connector. Detailed geometry remains pending selected LED hardware and optical prototype; current M030 is preserved until promotion. |

## EXTERNAL ONLY — remaining non-CAD dependencies

Everything still outside GREEN now depends on at least one of: **purchased physical hardware, shop-day measurement/coupon, or owner/external physical validation**. There is no remaining documentation-only or placement-only blocker.

## SHOP-DAY — late-bound manufacturing gates

These do **not** block design completion. They are intentionally resolved at the CNC shop from the actual material/hardware being cut.

| Gate | Shop-day rule |
|---|---|
| 18 mm / 12 mm plywood thickness | Nominal classes are frozen at 18 mm and 12 mm. Measure every production sheet, record the range, cut the V35.1 coupon on the same machine/cutter/CAM, then regenerate only fit-dependent geometry from measured thickness + selected physical clearance. If one nominal class has too much spread for one acceptable clearance, split it into thickness batches and regenerate per batch. |
| Side glass channel | Measure the real 03-7135-1-class profile and validate its slot on the 18 mm coupon with a real 5 mm glass sample. Production slot width/depth remain NULL until this shop-day test passes. |

## RED — real unresolved engineering gates

| Gate | Why it blocks |
|---|---|
| Primary raised-playfield service support | Must be independently engineered/qualified if it changes permanent wood/hardware interfaces; current raised-service support remains HOLD. |

## Release rule

A purchased item is only a full-sheet CNC gate when its actual dimensions control permanent machining. Components installed by protected-envelope dry fit, replaceable adapters, removable panels or post-CNC manual positioning must not remain mislabeled as PURCHASE_BEFORE_CNC.

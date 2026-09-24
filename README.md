# Virtual Pinball Cabinet

Parametric CNC-ready virtual pinball cabinet based on Williams WPC visual proportions, with deliberate future-proofing for replaceable electronics.


## Open-source hardware

This project is released under the **CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)**.

Official project / Source Location:

**https://github.com/advpeterrobinson-hash/vpin-cabinet**

Commercial use is allowed. If you convey modified Covered Source or Products based on it, the applicable Complete Source and modifications must remain available under CERN-OHL-S-2.0, and the project Notices / Source Location must be preserved.

In short: **you may build and sell products based on the design, but conveyed improvements may not be turned into a closed proprietary fork.**

See [LICENSE](LICENSE), [NOTICE.md](NOTICE.md), the [open-source policy](docs/OPEN_SOURCE_POLICY.md), the [licensing FAQ](docs/LICENSING_FAQ.md), and [CONTRIBUTING.md](CONTRIBUTING.md).

The licence is intentionally **commercial-friendly but strongly reciprocal**: selling cabinets, kits, fabrication, installation, or support is allowed; when modified Covered Source or Products based on it are conveyed, the applicable Complete Source must stay available under the same reciprocal licence. "Free" here means the design/source remains freely available under the licence — it does **not** require physical products or services to be sold for zero price.

The official upstream project link is part of the project Notice and should remain with redistributed designs/products:

**https://github.com/advpeterrobinson-hash/vpin-cabinet**

## Active development branch

The detailed current engineering work is presently maintained on `feat/active-build-cleanup-v25` pending the next integration into `main`. Contributors working on current CAD/manufacturing geometry should check that branch and its validation status rather than assuming every older dimension in `main` is current.


## Current product goal

The final download should behave like a **precision flat-pack kit**, not like a woodworking plan that still needs layout work.

The CNC/fabrication vendors should deliver parts with the geometry-critical work already done: profiles, captured joints, service apertures, cable/vent openings, part IDs, and — once the physical hardware is frozen — the exact hinge, slide, bracket, insert and through-hole locations.

The home builder should mainly:

1. identify the labeled parts;
2. dry-fit;
3. glue specified joints;
4. bolt/screw hardware into CNC-located holes;
5. sand/paint/finish/apply graphics;
6. install electronics and harnesses;
7. run the documented proof/safety checks.

Freehand structural layout is not the normal release workflow.

See [active BOM guidance](bom/README.md), `docs/SIMPLIFICATION_V25.md` and `bom/HARDWARE_FREEZE_V25.csv`.

## Active design

- **600 mm** main cabinet, WPC-inspired proportions
- **780 mm** folding backbox
- nominal 18 mm structural plywood; final CNC values follow measured stock
- model-agnostic 42/43-inch 4K high-refresh playfield display envelope
- predominantly CNC-plywood playfield cradle with local steel pivot interfaces
- manual playfield lift with two simple captive, positively pinned prop rods
- two narrow removable electronics carriers and filtered bottom intake
- classic pinball legs + levelers with compact measured steel brackets
- external removable PinSkates-style mobility; no built-in casters
- dedicated **rear CPU service hatch**
- one **285 x 460 x 18 mm** case-sized CPU shelf on two full-extension slides
- open PC case bolts directly to that shelf
- routine RAM/SSD/GPU/cable service from the rear with the playfield closed
- custom/local-fabricated 600 mm lockdown bar and siderails
- local tempered playfield glass after proof-fit
- adjustable backglass/DMD carrier
- reserved SSF / DOF / future electronics zones
- separate touch-safe mains enclosure and segregated routing

## Rear CPU service

The active PC-service architecture is intentionally simple:

`stand behind machine -> open rear hatch -> release one retainer -> pull CPU shelf rearward -> service PC -> push shelf in -> lock retainer -> close hatch`

The reference open case is approximately **440 x 265 x 128 mm**, rotated so 265 mm is across the cabinet and 440 mm is fore-aft. The shelf is approximately **285 x 460 mm** and travels about **450 mm rearward**. Final slide spacing and all mounting holes follow the measured physical slide pair and PC case.

## CNC / hardware freeze

All geometry-controlling purchased parts are tracked in `bom/HARDWARE_FREEZE_V25.csv` as one of:

- `MEASURE_BEFORE_CNC`
- `DIMENSIONED_LOCAL_FAB`
- `ADAPTER_ONLY`
- `NO_CNC_DEPENDENCY`

A production release is blocked until every `MEASURE_BEFORE_CNC` item that controls permanent wood/metal geometry is frozen and the prototype dry-fit/proof tests pass.

## Active local workflow

```bash
make doctor
make validate
make build-current
make open-master
```

`make build-current` generates a fresh active document from configs/builders, then reopens it for solid and service-clearance checks. It never reads or edits the historical working master.

Start with [the active engineering baseline](docs/ACTIVE_ENGINEERING.md), [part decisions](bom/ACTIVE_PARTS.csv), and [hardware gates](bom/HARDWARE_FREEZE_V25.csv).

Historical experiments remain available through Git history but are not part of the normal workflow.

## Structure-first procurement

Woodworking, classic legs, backbox hardware, playfield mechanics, rear CPU service hardware, lockdown/siderails, glazing and display fit must reach the **STRUCTURE READY** gate before the coordinated electronics/DOF purchase begins.

The exact playfield display is selected late from the Brazil market rather than hard-coded into permanent woodworking.

Primary planning documents:

- `docs/BUILD_PHASES.md`
- `docs/STRUCTURE_BUILD_MANUAL.md`
- `docs/SIMPLIFICATION_V25.md`
- `bom/HARDWARE_FREEZE_V25.csv`
- `docs/PLAYFIELD_MECHANICS_V18.md`
- `docs/REAR_CPU_SHELF_V24.md`
- `docs/BACKBOX_HINGE_SHOPPING.md`

## Safety baseline

The rear PC hatch may expose PC low-voltage hardware, but must never expose bare mains terminals. Mains distribution remains in a separate touch-safe enclosure. Isolate cabinet power before RAM/GPU/SSD/harness service.

The playfield display is carried by its independent cradle. Both captive prop rods must be positively pinned before working beneath the manually raised playfield.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC release remains blocked on measured stock, the physical tolerance coupon, Cutter CNC conventions, hardware freeze, local FreeCAD geometry validation, dry fit and proof testing.

Review outputs: `exports/generated/review/index.html`; FreeCAD presets: `tools/active_review.FCMacro`. Build tools: Python, FreeCADCmd, uv (matplotlib preview environment). See [audit evidence and unresolved engineering](docs/TAKEOVER_AUDIT_2026-09-16.md).

Owner selected [two localized rear-face interfaces](docs/REAR_UTILITY_V26.md): mains/master disconnect and optional Ethernet or blank. CPU door stays low. Generic apertures are modeled; hardware measurements and CNC release remain blocked.

## Contributing

Contributions are welcome from builders, CNC operators, mechanical designers, electricians, software developers, testers, and documentation writers.

- Start with [CONTRIBUTING.md](CONTRIBUTING.md).
- Read [GOVERNANCE.md](GOVERNANCE.md) for how engineering decisions are accepted.
- Use the GitHub issue templates for bugs, design proposals, manufacturing feedback, and hardware measurements.
- Use [SUPPORT.md](SUPPORT.md) for help and project-support boundaries.
- Report security or serious safety concerns through [SECURITY.md](SECURITY.md).
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- For reuse, forks, and commercial derivatives, read the [licensing FAQ](docs/LICENSING_FAQ.md).

Useful improvements are encouraged to come back upstream as pull requests, but the legal reciprocal obligations are governed by [LICENSE](LICENSE), not by whether a fork submits a PR.

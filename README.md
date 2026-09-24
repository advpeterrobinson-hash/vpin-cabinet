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


## Primary design targets

- Williams WPC-derived visual proportions rather than rigid historical dimensions
- owner-approved 10–50 mm dimensional deviations where they materially improve long-term serviceability or replacement compatibility
- 18 mm metric plywood construction (final production value = measured sheet thickness)
- LG OLED42C5 initial playfield in a replaceable structural cradle
- approximately 32-inch 1080p backglass in a future-proof modular backbox
- hinged structural playfield cradle
- dual gas struts
- independent mechanical safety support
- real pinball legs
- retractable wheels for moving cabinet
- full DOF / mechanical force feedback
- SSF tactile audio
- modular electronics and feedback mounting
- slide-out ATX PC chassis on a replaceable drawer adapter
- single mains power cord
- independent Audio Only / Bluetooth mode
- Full Pinball mode
- external service USB ports
- normally offline operation
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Longevity philosophy

The wooden cabinet and structural metalwork should outlive several generations of televisions, PC hardware, control boards, amplifiers, and power supplies. Permanent structure is therefore designed around service envelopes and modular interfaces rather than the exact dimensions of the first electronics installed.

Current examples:

- backbox target widened to 780 mm to provide a 740 x 450 x 100 mm replaceable display envelope;
- exact backglass model affects only the removable carrier/bezel, not the permanent shell;
- main cabinet width is under review for a modest future-proof increase before CNC freeze;
- PC and electronics mounting use replaceable adapters/panels.

See `docs/FUTURE_PROOFING.md`.

## Engineering workflow

The long-term source of truth is the documented design baseline plus the Python/FreeCAD generation and validation scripts. The binary `.FCStd` master is an engineering artifact, not the only record of design intent.

Useful local commands:

```bash
make doctor
make validate
make open-master
```

`make validate` currently checks the documented dimensional baseline without requiring FreeCAD. FreeCAD geometry/collision checks will be added as the design matures.

See:

- `AGENTS.md` — engineering rules for humans and coding agents
- `config/design.json` — machine-readable design baseline
- `docs/DESIGN_DECISIONS.md` — decision log
- `docs/FUTURE_PROOFING.md` — long-term replacement/service envelope policy
- `docs/requirements.md` — system requirements
- `docs/reference-baseline.md` — dimensions extracted from the reference model
- `docs/vendors.md` — parts/services/vendor notes

## Current validated geometry

- Williams WPC cabinet profile is live-parametric.
- Reference outer width: 558.80 mm; final main-cabinet width is now under future-proofing review.
- Current nominal 18 mm plywood gives 522.80 mm inside width at the reference body width.
- LG OLED42C5 cross-cabinet physical width: 540.0 mm.
- Current OLED cavity including clearance: 542.0 mm.
- Current nominal side pocket depth: 9.60 mm.
- Current nominal remaining side skin: 8.40 mm.

The OLED pocket is a clearance feature only; the OLED and gas-strut loads must be carried by an independent structural cradle. Before CNC freeze, the main-body width will be evaluated against a larger future 42-inch-class display service envelope and the consequences for glass, siderails, and lockdown-bar hardware.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, material measurement, provider/tooling consultation, physical tolerance coupon, and final design validation.


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

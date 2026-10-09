# Virtual Pinball Cabinet

## [OPEN THE CURRENT GALLERY →](docs/RENDERS.md)

**[ABRIR A GALERIA EM PORTUGUÊS →](docs/pt-BR/RENDERS.md)** · [Português (Brasil)](README.pt-BR.md)

**V35.1 is the current engineering / architectural review. CNC and manufacturing remain BLOCKED.** V32 is historical; passing CAD checks do not certify physical strength, purchased hardware fit or manufacturing readiness.

Parametric virtual pinball cabinet inspired by Williams WPC proportions, developed toward a reproducible flat-pack product with replaceable electronics.

## Current architecture — V35.1

The engineering review is maintained on `feat/v351-cncaudit-qn90f`. Read the [V35.1 technical report](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/aa3043cd172ed2bf0f05e0ef5ddcf1cbe9b53656/docs/STANDARD_WIDEBODY_V351.md) and [technical package](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/aa3043cd172ed2bf0f05e0ef5ddcf1cbe9b53656/exports/generated/widebody-v351/README.md). These links pin the reviewed evidence; they do not merge its CAD into `main`.

- Standard widebody: **628.65 mm** external body, **592.65 mm** nominal interior; **1308.10 mm** body length; **780 mm** backbox width.
- **66 wood components: 60 CNC plywood pieces and six solid blocks; 45 families.** Nominal plywood stock is **18 / 12 mm only**; actual lot measurement remains required.
- S1/S2/S3 removable shelves, T1/T2/T3 crossmembers and replaceable guides; low fixed PCBase, **no PC drawer**.
- Retained wooden-dowel/open-cradle playfield architecture. **Primary raised-playfield service support remains unresolved / HOLD**; no service-safety approval is implied.
- Commercial lockdown/receiver reference interfaces; siderails optional. Receiver fit/strategy remains unresolved where it controls permanent machining.
- Local **5 mm tempered playfield glass**, final size after cabinet/channel dry fit; actual side-channel profile and slot coupon still required.
- Real pinball legs; external removable mobility devices, no integrated wheels. Modular electronics and protected grounded mains distribution.

### Selected television — validation pending

**Samsung QN43QN90FAGXZD (QN90F 43-inch)** is the owner-selected purchase target. Selection does not establish compatibility: exact-envelope **PLAY / 0–50° service / 48 mm lift-out and interference checks must be rerun** before the QN90F is described as validated. The permanent cabinet remains intended for replaceable 42/43-inch-class displays.

## Review evidence and release gates

The report records 32 native-CAD review views and passing checks of the modeled reference state. Those results do not certify the selected QN90F, purchased hardware, material strength or human service safety. Preliminary nesting is a study, not production CAM.

**No CNC files are approved for manufacturing. Full-sheet release remains BLOCKED.** Open gates include receiver strategy/fit if machining-dependent; measured side channels and slot coupon; actual plywood lot and tolerance coupon; CNC-provider/tooling parameters and fit regeneration; remaining geometry-controlling hardware/control interfaces and attachment methods; exact QN90F rerun; primary raised-playfield support; and physical load/nudge/glass-edge/thermal qualification.

The lockdown bar and rear glass-channel screw locations are dry-fit interfaces with protected envelopes, not full-sheet CNC gates themselves. F06 reinforcement remains required and is qualified after shell dry fit. See the report for the precise gate boundaries.

## Documentation and history

- [Documentation index](docs/README.md) and [English gallery](docs/RENDERS.md).
- [Historical V32 gallery](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/RENDERS.md) and [V32 technical package](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/README.md): 600 mm architecture, preserved as engineering history.
- [Contradictions and documentary resolutions](docs/PUBLIC_DOCUMENTATION_AUDIT.md).

Older width, gas-strut, sliding-PC and prop studies are historical context, not current V35.1 requirements. Scripts and revision-specific parameters remain engineering authority; no legacy build command on `main` certifies V35.1. Permanent structure should outlive replaceable electronics; adapters and carriers preserve serviceability.

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

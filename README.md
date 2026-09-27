# Virtual Pinball Cabinet

## [OPEN THE CURRENT GALLERY →](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/RENDERS.md)

**[ABRIR A GALERIA EM PORTUGUÊS →](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/pt-BR/RENDERS.md)** · [Português (Brasil)](README.pt-BR.md)

Follow the current cabinet directly through the gallery. **V32 is the current visual/architectural review; CNC/manufacturing remains BLOCKED and physical sessions are paused.**

[![Current V32 interior: S1/S2/S3 and low PCBase](https://raw.githubusercontent.com/advpeterrobinson-hash/vpin-cabinet/refs/heads/feat/cabinet-review-v32/exports/generated/cabinet-v32/01-interior.png)](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/RENDERS.md)

[Interior](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/01-interior.png) · [Crossmembers](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/02-travessas.png) · [Plan](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/03-planta.png) · [Rear](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/04-traseira.png) · [Guide detail](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/05-encaixe.png) · [Front](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/06-frente.png)

Parametric virtual pinball cabinet inspired by Williams WPC proportions, designed toward a reproducible CNC flat-pack product with replaceable electronics.

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

## Current architecture

The current review is maintained on [`feat/cabinet-review-v32`](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/README.md). [Open its technical package](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/exports/generated/cabinet-v32/README.md) for CAD, STEP, dimensions and unresolved gates. Older material on this branch remains engineering history; it must not override V32.

- 600 mm cabinet; nominal 18 mm plywood, ultimately sized from measured stock.
- Model-agnostic 42/43-inch playfield envelope: 560 × 970 × 55 mm, maximum 12 kg.
- S1/S2/S3 removable shelves, T1/T2/T3 crossmembers and replaceable guides.
- Low open PC case on PCBase; no PC drawer in V32.
- Two rear reference 120 mm exhaust fans.
- Real pinball legs and external removable PinSkates-style mobility; no integrated wheels.
- **Manual playfield lift with two captive prop rods and positive pins/keepers; no gas struts.** Both props must be engaged during raised service, and each must independently pass full-load retention proof. Final pivot/prop geometry and service sweeps remain to be engineered and validated for V32.
- Modular DOF/SSF and lighting; single grounded mains input with touch-safe internal distribution.

## Longevity philosophy

The wooden cabinet and structural metalwork should outlive several generations of televisions, PC hardware, control boards, amplifiers, and power supplies. Permanent structure is therefore designed around service envelopes and modular interfaces rather than the exact dimensions of the first electronics installed.

Current examples:

- backbox target widened to 780 mm to provide a 740 x 450 x 100 mm replaceable display envelope;
- exact backglass model affects only the removable carrier/bezel, not the permanent shell;
- main cabinet width is 600 mm with 564 mm nominal clear interior;
- PC and electronics mounting use replaceable adapters/panels.

See `docs/FUTURE_PROOFING.md`.

## Review and validation

V32 has 45 valid solids and no detected positive-volume intersections above 0.01 mm³ in its packaging review. These results do **not** certify strength, movement, hardware fit or manufacturing readiness.

The documented scripts and parameters remain the source of truth. On the V32 branch, `make review-v32` regenerates CAD and the gallery, checks saved solids and bilingual metadata, and rejects unexpected geometry changes against committed evidence.

The older Make/build v25–v27 pipeline remains **PRE-V32**, with live dependencies retained until a validated replacement exists. It is not evidence that V32 is ready for manufacture. [Current local audit](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/feat/cabinet-review-v32/docs/V32_LOCAL_AUDIT.md).

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

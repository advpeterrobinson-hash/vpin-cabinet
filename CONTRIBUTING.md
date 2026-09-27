# Contributing to Virtual Pinball Cabinet

**English** · [Português (Brasil)](CONTRIBUTING.pt-BR.md)

Thanks for helping improve the project. Contributions are welcome from builders, mechanical designers, CNC operators, electricians, software developers, testers, and documentation contributors.

## Before you start

Spend a few minutes on the current contributor path before opening files from older revisions:

1. [current renders](docs/RENDERS.md);
2. [documentation index](docs/README.md);
3. [V32 review package](exports/generated/cabinet-v32/README.md);
4. [permanent part-code registry](docs/PART_CODES.md).

For substantial mechanical or architectural changes, open a **Design proposal** issue first. Small fixes, documentation corrections, tests, and clearly isolated bugs can go directly to a pull request.

Start from the current active engineering branch named in the README. Do not assume historical branches or old FreeCAD groups are current design authority.

## Engineering principles

Contributions should preserve the project's core goals:

- CNC-prelocated structural geometry rather than freehand layout;
- flat-pack / apartment-friendly assembly;
- measured hardware before geometry-critical CNC holes are frozen;
- replaceable adapters for short-lived electronics;
- simple, inspectable load paths;
- no exposed mains terminals in service areas;
- positive mechanical safety for the raised playfield;
- reproducible source-driven CAD rather than manual edits to a binary master.

Do not invent hardware hole patterns from catalog drawings when the project marks that hardware as **MEASURE_BEFORE_CNC**.

## Documentation language

English is the canonical project language for contributor-facing documentation, source identifiers and engineering source-of-truth fields. Portuguese translations are maintained for selected current documents.

A useful engineering contribution **does not need a Portuguese translation to be accepted**. Do not delay a technical fix because the PT-BR mirror has not yet been updated.

Stable part codes such as `T1`, `S1`, `S1SupL` and `SideL` are language-neutral and must not be translated or repurposed.

See [documentation language policy](docs/LANGUAGE_POLICY.md).

## Current vs historical material

Versioned v04–v28 documents, configs and helper scripts remain in the repository for design history and evidence. They are not automatically current authority.

If a proposed change depends on an older file, explain why that file is still relevant. The repository is undergoing a controlled cleanup; see [repository cleanup plan](docs/REPOSITORY_CLEANUP.md).

## Pull request workflow

1. Fork the repository or create a feature branch.
2. Keep changes focused and explain the engineering reason.
3. Update configs/source-of-truth files before generated artifacts.
4. Add or update validation when geometry or design rules change.
5. Run the relevant local checks.
6. Include screenshots or generated review views for visual changes.
7. List any hardware measurements, assumptions, or manufacturing gates that remain unresolved.

Typical checks include:

```bash
make doctor
make validate
make build-current
git diff --check
```

Use additional project validators when your change affects CNC features, part registers, hardware freeze gates, or negative controls.

## Licensing of contributions

This project is released under **CERN-OHL-S-2.0**.

By submitting a contribution, you represent that you have the right to submit it and you agree that your contribution is provided under the same CERN-OHL-S-2.0 terms as the project.

No contributor licence agreement is currently required.

Do not add third-party CAD, drawings, images, manuals, code, or data unless redistribution rights are clear and the applicable licence/source is documented.

## Attribution and official project link

Preserve the project Notices, including the official Source Location:

https://github.com/advpeterrobinson-hash/vpin-cabinet

If you publish a modified version or a product based on this project, follow `LICENSE` and `NOTICE.md`, including the Source Location and reciprocal source obligations.

## Generated files

Do not commit large generated or binary files unless they are intentionally part of the project release or are specifically requested for review. Source configs, builders, feature registers, drawings, and validation should remain sufficient to reproduce the active engineering model.

## Review expectations

A maintainer may request:

- clearer load-path reasoning;
- physical measurements;
- simpler construction;
- additional negative tests;
- a smaller or more modular change;
- removal of speculative hardware-specific geometry;
- proof that the change can be fabricated and assembled with the intended toolset.

A passing test suite is necessary but does not by itself make a design manufacturing-ready.

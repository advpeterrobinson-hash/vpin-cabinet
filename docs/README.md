# Documentation

[English](README.md) · [Português (Brasil)](pt-BR/README.md)

## New here?

You should be able to understand the project before reading historical engineering notes.

1. **[View the current renders](RENDERS.md)** — fastest way to understand what the cabinet currently looks like.
2. **[Read the V32 review package](../exports/generated/cabinet-v32/README.md)** — current geometry, dimensions, files and unresolved gates.
3. **[Learn the permanent part codes](PART_CODES.md)** — T1/T2/T3, S1/S2/S3 and other stable identities used across the project.
4. **[Read the current joinery proposal](CABINET_JOINERY_PROPOSAL.md)** — proposed self-indexing lower-cabinet CNC joints; not yet V32 geometry.
5. **[Contribute](../CONTRIBUTING.md)** — how to propose a design, measurement, test, documentation fix or fabrication result.

If you do not want to contribute yet, watching the repository and following the render/current-review pages is a valid way to observe development.

## Current authority

The current owner-facing design review is V32 on `feat/cabinet-review-v32`.

Manufacturing/CNC release remains blocked. A render or valid CAD solid is not by itself evidence that a part is structurally proven or ready to machine.

## Active contributor-facing documents

- [Renders](RENDERS.md)
- [Part codes](PART_CODES.md)
- [Lower-cabinet joinery proposal](CABINET_JOINERY_PROPOSAL.md)
- [Language policy](LANGUAGE_POLICY.md)
- [Build phases](BUILD_PHASES.md)
- [Structure build manual](STRUCTURE_BUILD_MANUAL.md)
- [Requirements](requirements.md)
- [Vendors / hardware notes](vendors.md)

## Transition pipeline

The root `Makefile` and [pre-V32 validated engineering pipeline](ACTIVE_ENGINEERING.md) still support v25–v27 validation/build evidence. They remain temporarily live dependencies during cleanup, but they are not current V32 architecture authority.

The [pre-V32 BOM entry point](../bom/README.md) is retained for the same reason.

## Historical engineering

The repository still contains many versioned v04–v28 documents, configs and tools. They preserve design history and validation evidence but should not be assumed to represent current geometry.

The next repository phase is a controlled cleanup:

- classify files as current, historical, generated, reference or removable;
- move superseded documentation into explicit history/archive areas where safe;
- remove true cache/temporary artifacts;
- reduce duplicate tools and entry points only after dependency/reference checks;
- keep Git history and engineering evidence intact;
- avoid breaking current build/review paths.

See [repository cleanup plan](REPOSITORY_CLEANUP.md).

## Languages

English is canonical. Selected current documents are mirrored under [`docs/pt-BR/`](pt-BR/README.md). See [language policy](LANGUAGE_POLICY.md).

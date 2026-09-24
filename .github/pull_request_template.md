## What changed

Describe the engineering problem and the proposed solution.

## Why

Explain why this change improves safety, manufacturability, reproducibility, serviceability, compatibility, or simplicity.

## Affected systems / part IDs

List relevant part IDs, configs, builders, hardware gates, or subsystems.

## Validation

- [ ] Relevant Python validators pass
- [ ] Fresh active FreeCAD model generated when geometry changed
- [ ] Saved-geometry checks pass
- [ ] Negative controls updated where appropriate
- [ ] `git diff --check` passes
- [ ] Part/BOM/register reconciliation passes when applicable
- [ ] Review images/screenshots attached for visual changes

## Hardware assumptions

- [ ] No geometry-critical hole pattern was guessed for hardware marked `MEASURE_BEFORE_CNC`
- [ ] New measurements include datum, tool, tolerance, and source
- [ ] Remaining blocked measurements are documented

## Safety

Describe any effect on mains, structural loads, playfield service support, moving masses, thermal management, or service access.

## Licensing / source

- [ ] I have the right to submit this material
- [ ] I submit my contribution under CERN-OHL-S-2.0
- [ ] I did not add unlicensed proprietary CAD, artwork, manuals, or other restricted third-party content
- [ ] Applicable Notices and the official project Source Location are preserved

Official project: https://github.com/advpeterrobinson-hash/vpin-cabinet

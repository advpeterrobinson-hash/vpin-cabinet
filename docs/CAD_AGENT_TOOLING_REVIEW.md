# CAD agent tooling review — text-to-cad

**Reviewed:** 2026-10-21  
**Source:** [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)  
**Review type:** README and declared license review; no installation, code execution, or CAD import.

## Assessment

This is a CAD workflow for coding agents, not only a prompt collection. The repository offers agent skills and a plugin that starts a local cadgen MCP service. Its documented stack includes Python, build123d and Open CASCADE; it generates STEP, GLB, STL and 3MF, and advertises drawing and design-for-manufacture checks. The README lists Codex among supported agents. The repository declares the MIT License.

**Relevance to VPin Cabinet: useful for a bounded, independent pilot.** It could be evaluated on a separate, low-risk component or a dimensioned test coupon, and on inspection of exported solids. The cabinet's FreeCAD parametric model, revision-specific configuration, validation scripts and approved geometry must remain the engineering authority.

## Fit and limits

- The tool's documented build123d/Open CASCADE workflow is different from the project's FreeCAD source and existing generation/validation pipeline. Generated geometry must not replace or silently modify the canonical model.
- Agent-generated geometry is a proposal. It cannot establish the dimensions of unmeasured commercial hardware, structural safety, glass fit, manufacturing tolerances or physical validation.
- The repository README says telemetry is enabled by default for usage and crash reports, with a random identifier; it says files, paths and prompts are not included and documents an opt-out. The runtime is downloaded locally on first use and requires a network connection.
- The README's install instructions can install code, skills and a local service. They are not a harmless read-only review step.

## Recommended pilot

1. Use a disposable, access-limited workspace and a separately specified non-structural part or test coupon. Do not give the agent the canonical FreeCAD working tree.
2. Pin a reviewed release/commit, inspect the package and dependencies, and disable telemetry before execution.
3. Export a neutral STEP file. Compare units, overall dimensions, placement, solid validity and assembly clearances against explicit project-controlled values.
4. Record failures and manual corrections. Keep the output outside the manufacturing release until it passes the existing project checks and human review.

**Decision:** retain as a reviewed candidate for a constrained pilot. Do not install it in the VPin repository, make it part of the normal build, or use its output for CNC release on the basis of this review alone.

## Related evidence

- [V35.1 technical report](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/docs/STANDARD_WIDEBODY_V351.md)
- [V35.1 external gates](https://github.com/advpeterrobinson-hash/vpin-cabinet/blob/e6fe42152565a167e9d4e4d0ad4eb080f09c1c28/docs/V351_REMAINING_EXTERNAL_GATES.md)
- [Current documentation audit](PUBLIC_DOCUMENTATION_AUDIT.md)

This assessment describes the upstream README and license as checked on the review date; it is not a security audit or a guarantee that future releases retain the same behavior.

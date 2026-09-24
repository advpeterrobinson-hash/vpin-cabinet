# CNC freeze gate — evidence before geometry authority

**Current state: BLOCKED.** Baseline `c1bb566`; 59 hardware-blocked feature groups stay open. This gate does not change any geometry, register status or `manufacturing_ready` flag. Passing a Python check or exporting a file is not authorization to manufacture.

## Gate 1 — collect and review physical evidence

For each affected part/feature group require:

- Identified delivered hardware or identified locally fabricated prototype, including handed pair differences, revision and batch; photographs showing datums and installed context.
- Complete physical measurements of pattern, bores/flats, seating faces, fastener/nut/backing stack, moving envelope, connectors and tool access. Raw readings, units, instrument, uncertainty, date/operator and reviewer must be recorded. Catalogue values stay supplemental and cannot fill measured fields.
- Measured production plywood/door stock range, grain/orientation and finish allowance; no substitution of nominal 18.0 mm for fit geometry.
- Approved datum transform to the actual wood machining face, complete tolerance/clearance budget and actual wood ligaments/fastener load review. Measurement uncertainty is not automatically a CNC or journal-fit tolerance.
- Passed relevant physical mockups: control/plunger ergonomics and stroke; prop deployment/retention/stow/access; door and backbox fold/access; CPU extraction/corner stack; carrier/cable removal. Load-bearing interfaces also require reviewed prototype proof evidence (each prop independently, CPU, leg/backbox/pivot/lockdown load paths as applicable). Undefined qualification loads or deflection limits keep the gate open.

The JSON worksheet records evidence without clearing a feature. `RECORDED` means captured, `REVIEWED` means evidence reviewed, neither means manufacturing-authoritative. Reviewer identity/date, source files and scope must be inspectable. Any changed hardware, stock, anchor, fastener or load invalidates the relevant evidence until reviewed/retested.

## Gate 2 — final holes, bores and authoritative hardware patterns

Only after Gate 1 for the corresponding interface:

1. In a normal new commit, create a measured-pattern source with physical evidence links and revision. Confirm independently that every coordinate, diameter, flat and depth traces to measured data plus an explicit, reviewed fit allowance. No coordinates may be inferred from a perspective image or a brand-family assumption.
2. Generate candidate final holes/bores from that source; verify transformed locations against actual handed parts, tool access, edge distances, mating stack and continuous physical sweep/tolerance results. Retain generic unmeasured placeholders elsewhere as blocked. Prototype holes in separate sacrificial fixtures are allowed before this gate but must never be called final cabinet machining geometry.
3. Machine and fit a representative coupon/fixture using the intended shop/tool/material/clearance strategy. Hardware must seat and retain correctly with no precision hand trimming or transfer drilling. Update/retest if the fit changes.
4. Review the complete feature group and all dependencies, then change its blocker status explicitly in a reviewed commit. Record reviewer, evidence IDs and affected CF IDs. Never clear an entire hardware family because one sample/one side passed. Booleans in a results worksheet alone cannot unlock CAD.

This cycle deliberately has no code that promotes results into geometry or clears blockers. A future release implementation must be separately reviewed; the guard rejects silent changes to the baseline blocked set.

## Gate 3 — production-ready CNC exports

Before any export is labelled production-ready, require all Gates 1/2 within its declared scope and:

- Reconciled active parts, physical ply IDs for laminated assemblies, feature/joint/fastener registers and a complete assembly sequence. All structural holes CNC-located; no unresolved “builder drills later”.
- Measured stock-driven regeneration, approved cutter diameter, fits, tool relief/dogbones, pocket depths, two-face setups, grain, nesting, part labels and verified toolpaths. Physical shop coupon and representative dry fit pass.
- Fresh Python/FreeCAD generation and reopened saved-geometry checks; no unexpected intersections, changed service envelopes or obsolete geometry; negative controls and register reconciliation pass. Check final exported layers/units/scale against the validated model, not merely successful file creation.
- Final local-metal drawings, specified fasteners and hardware BOM; dimensioned drawings/DXF or appropriate exports, sheet map, fit coupon, assembly/service instructions and Source Location/licence notices.
- Completed relevant load qualification, safe manual lifting/individual props, service/fold/access, leg stability and electrical/thermal commissioning or an explicitly scoped later commissioning gate. **For this baseline's complete cabinet release, outstanding commissioning remains blocking; no silent scope exception.**
- Explicit owner manufacturing approval referencing immutable source, evidence and export revisions. A release manifest must name its precise scope; omitted adapters remain conspicuously blocked and cannot be represented as included production-ready pieces.

No gas-strut measurement is required. Fans, filters, exciters, speaker/display adapters and the case shelf pattern may have separate adapter scopes, but that does not remove their physical service/load obligations or let an incomplete complete-cabinet package claim production readiness.

## Open categories beyond the 59 feature groups

The feature count excludes global stock/tool/coupon gates; supplemental pilots and final relief; laminate breakout/nesting; local-metal detailing; actual control ergonomics; individual prop/load qualification; CPU 20 kg proof; leg/backbox/lockdown load capacity; manual handling; cable/fold/service checks; thermal/electrical commissioning; export review and owner approval. These remain explicit requirements even if a future hardware-blocked count reaches zero.

# Physical-validation preparation audit — 2026-09-24

Engineering baseline and fetched remote engineering tip: `c1bb566a8eff24240434c3f084e068c20e7cd4a0`.

Recovery tag: `checkpoint/v27-physical-validation-baseline`, annotated at that exact commit; explicitly not a production release. No prior tag convention existed. No history rewrite or change to the baseline geometry.

## Audit result

Read the hardware measurement pack, owner review and prior validation record; reconciled hardware/CNC/blocked registers; inspected the current 17-image gallery contact sheet. Current gallery is engineering packaging only. No new physical measurements or proof results were supplied, and no blocker was cleared.

Before/after: 59 hardware-blocked feature groups across 22 hardware IDs; 173 defined groups; 232 total. Wood remains 29 permanent structural  / 32 total assembly records; 11 carriers separately registered. All other stock/tool/fit/coupon, load, ergonomics, service, local-metal, commissioning and export/approval gates remain open. The worksheet covers 32 component records, 186 individually blank measurement entries and 18 OPEN physical trials. HF-014's case pattern remains on the replaceable board rather than the permanent shell.

## Files changed

- `docs/PHYSICAL_VALIDATION_PLAN_V27.md`: actual-hardware procedures, independent prop proof, manual handling, controls/SSF, service and airflow.
- `docs/CNC_FREEZE_GATE_V27.md`: evidence, final pattern and production export gates.
- `docs/PHYSICAL_RESULTS_WORKSHEET_V27.md`: printable forms and all 59 feature mappings.
- `bom/PHYSICAL_VALIDATION_RESULTS_V27.json`: persistent blank evidence ledger, never a source of automatic geometry release.
- `tools/validate_physical_validation_v27.py`: coverage/provenance/release guard and seven negative controls.
- `Makefile`: evidence validation in the default suite.
- `docs/HARDWARE_MEASUREMENT_PACK_V25.md` and `docs/OWNER_REVIEW_V27.md`: links to the next physical cycle.
- This audit record.

No active geometry config, builder, CNC feature register or hardware freeze status changed. Source notices/licensing retained. The pre-existing modified master FCStd and deleted backup remain outside these commits. Master FCStd SHA256 before/after: `98be2307dbe570d8719f385cc0062af56b0cecf85f4b97d2e4f9c340d908c9e3`.

## Validation evidence

Completed successfully: `make validate`, `make cnc-detail` (fresh FreeCADCmd generation, reopened active/joint geometry, register reconciliation and gallery generation), and `python3 -m py_compile tools/validate_physical_validation_v27.py`. All 40 existing negative controls plus 7 new evidence negative controls passed: **47 distinct rejected mutations**. Checked all 59 worksheet feature rows for uniqueness and local documentation links for valid targets. `git diff --check` passed; staged whitespace check is required before commit. No physical trial was performed. Local generated logs are `.work/logs/physical-cycle-python.log` and `.work/logs/physical-cycle-full.log`, with detailed saved-geometry and negative-control logs under `.work/logs/`. The source ledger is intentionally not overwritten by the existing measurement-pack generator.

## Physical evidence next

Owner: identify and measure delivered plunger/button samples and production stock; document installed leg/rail/hinge/bearing/prop/door stacks using the existing minimal procurement list. Build sacrificial full-size control/service mockups. Have actual prop/anchor load limits and fixture reviewed before independent left/right proof; record moving mass and force-angle trials with backup support. Trial carrier cable removal, CPU path/proof, rear servicing/front monitor extraction and filter access. Complete final hardware/thermal/electrical checks when the corresponding equipment exists. Record failures and limitations, not just PASS labels.

Manufacturing remains **BLOCKED**. Catalogue dimensions, assumed mass, CAD clearances and a successful export cannot substitute for physical evidence.

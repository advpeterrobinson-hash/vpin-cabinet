# Owner measurement sheets — v27

Derived owner convenience copy. Authoritative values remain in [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). No measurements are filled; manufacturing stays **BLOCKED**. Regenerate with `python3 tools/generate_owner_execution_v27.py`; do not write bench results into generated files.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

Print one operation section at a time. Copy a sheet for each handed instance/sample, and extra rows for multi-hole patterns or sub-readings; retain the original measurement ID with a sub-reading label. Header instrument/date/sample apply to all rows unless overridden in notes. Empty spaces are intentional. OPEN is the default: a blank result is not PASS.

No direct geometry unlock. A check mark means collected, not accepted for machining. For B operations print the original reviewed procedure as well; these sheets do not authorize loading. [Detailed checklist](OWNER_PHYSICAL_CHECKLIST_V27.md) · [Evidence plan](OWNER_EVIDENCE_PLAN_V27.md)

## S00 / PREP — Prepare the bench and result folder

**A — OWNER CHECK / verify sample and support.** Dependencies: none.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks.

Samples/repeats: One preparation/handoff record; no specimen repetitions.


Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Prepared labels, blank sheets and working instruments only; no dimensional or ergonomic acceptance. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S00 / ARRIVAL — Sort delivered samples and identify missing items

**A — OWNER CHECK / verify sample and support.** Dependencies: PREP.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks.

Samples/repeats: One preparation/handoff record; no specimen repetitions.


Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Identity and arrival recorded; no fit approval. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S01 / STOCK-THICK — Measure sheet thickness once; retain all readings and min/max

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Micrometer or broad-jaw caliper; straightedge/feeler gauges

Samples/repeats: Nine points per sheet; all actual main and different door stock. Repeat readings where instrument repeatability is uncertain; no fixed repeat count otherwise specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-001-M01** — Thickness at 9 distributed points per sheet | mm; notes for condition/identity | ______ | ______ |
| **HF-001-M02** — min/max | mm; notes for condition/identity | ______ | ______ |

HF-001 datum: Mark face A and front-left corner; thickness normal to face without crushing veneers

HF-001 recording target (not machining fit): Thickness recording ±0.05 mm; retain observed min/max; do not average away sheet variation.

HF-001-M01 raw point record (one labeled sheet):

| Point on sketch | Thickness mm | Repeat mm |
|---|---|---|
| 1 | __________ | __________ |
| 2 | __________ | __________ |
| 3 | __________ | __________ |
| 4 | __________ | __________ |
| 5 | __________ | __________ |
| 6 | __________ | __________ |
| 7 | __________ | __________ |
| 8 | __________ | __________ |
| 9 | __________ | __________ |

HF-001-M02: minimum ______ mm; maximum ______ mm (from these same readings).

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Recording target ±0.05 mm; retain spread. This does not approve sheet fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S01 / STOCK-SURVEY — Survey the same labeled sheet

**A — OWNER CHECK / verify sample and support.** Dependencies: STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Steel rule/tape, straightedge, feeler gauges, pencil and labeled sheet sketch.

Samples/repeats: Every actual sheet/batch; no additional fixed repetition count in the plan.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-001-M03** — sheet dimensions | mm; notes for condition/identity | ______ | ______ |
| **HF-001-M04** — bow | mm; notes for condition/identity | ______ | ______ |
| **HF-001-M05** — face/core defects | text / instance IDs (grain also mark on sketch) | ______ | ______ |
| **HF-001-M06** — grain direction | text / instance IDs (grain also mark on sketch) | ______ | ______ |
| **HF-001-M07** — batch ID | text / instance IDs (grain also mark on sketch) | ______ | ______ |

HF-001 datum: Mark face A and front-left corner; thickness normal to face without crushing veneers

HF-001 recording target (not machining fit): Thickness recording ±0.05 mm; retain observed min/max; do not average away sheet variation.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S01 / SHOP-COUPON — Arrange shop tool readings and the physical fit coupon

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: STOCK-SURVEY.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: CNC shop supplies its tooling/runout/depth/registration instruments and identified physical coupon.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-002-M01** — Actual cutter diameter | mm; notes for condition/identity | ______ | ______ |
| **HF-002-M02** — runout | mm; notes for condition/identity | ______ | ______ |
| **HF-002-M03** — pocket depth accuracy | mm; notes for condition/identity | ______ | ______ |
| **HF-002-M04** — accepted groove clearance | mm; notes for condition/identity | ______ | ______ |
| **HF-002-M05** — relief radius | mm; notes for condition/identity | ______ | ______ |
| **HF-002-M06** — two-face registration accuracy | mm; notes for condition/identity | ______ | ______ |

HF-002 datum: Coupon face A and engraved zero corner

HF-002 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-STOCK-TOOL — Measured stock cutter clearance coupon**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Shop-confirmed tool/fit/relief/two-face setup and physical coupon/dry fit required by the freeze gate; missing criteria stay OPEN. [Source](../docs/CNC_FREEZE_GATE_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S02 / PLUNGER-FACE — Measure the plunger mounting face and seating stack

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Delivered plunger and every installed mounting variant; repeat pattern from an independent reference.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-030-M01** — Front cutout contour | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M02** — hole centers | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M03** — sleeve/shaft diameter | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M04** — flange and nut stack | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M07** — internal body/sensor depth | mm; notes for condition/identity | ______ | ______ |

HF-030 datum: A=front panel outside plane; B=plunger shaft axis; C=anti-rotation orientation; installed +Y inward

HF-030 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S02 / PLUNGER-STROKE — Check the complete plunger stroke in its mock panel

**A — OWNER CHECK / verify sample and support.** Dependencies: PLUNGER-FACE, STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: At least 20 deliberate full-stroke cycles, as required by plan A.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-030-M05** — stroke | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M06** — handle projection | mm; notes for condition/identity | ______ | ______ |
| **HF-030-M08** — cable/connector sweep | deg and mm clearance; note state | ______ | ______ |

HF-030 datum: A=front panel outside plane; B=plunger shaft axis; C=anti-rotation orientation; installed +Y inward

HF-030 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-PLUNGER — Physical plunger pattern stroke and clearance**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: No contact, snag, binding, unintended activation or pinch; full return/stroke and retained fasteners. Reviewer-approved positive clearance budget and ergonomic acceptance still required before bore release. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S02 / COIN-FACE — Measure coin-door cutout, flange and bolts together

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-019-M01** — Required cutout contour/radii | mm; notes for condition/identity | ______ | ______ |
| **HF-019-M02** — flange coverage | mm; notes for condition/identity | ______ | ______ |
| **HF-019-M03** — all mounting holes | mm; notes for condition/identity | ______ | ______ |
| **HF-019-M04** — body/depth | mm; notes for condition/identity | ______ | ______ |
| **HF-019-M07** — coin mechanism protrusion | mm; notes for condition/identity | ______ | ______ |

HF-019 datum: A=front mounting face; B=cutout lower-left; C=vertical centerline

HF-019 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S02 / COIN-OPEN — Check coin-door swing and key/tool access

**A — OWNER CHECK / verify sample and support.** Dependencies: COIN-FACE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-019-M05** — hinge swing | deg and mm clearance; note state | ______ | ______ |
| **HF-019-M06** — lock/key access | mm plus observed condition/state | ______ | ______ |

HF-019 datum: A=front mounting face; B=cutout lower-left; C=vertical centerline

HF-019 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S03 / BUTTON-FAMILY — Measure each button family in one caliper setup

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: One real sample of every final button family; identify every variant. Repeat readings to establish instrument repeatability; no fixed count supplied.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-020-M01** — Bore and flats | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M02** — bezel OD | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M03** — threaded length | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M04** — nut/washer OD | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M05** — switch depth | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M06** — connector clearance | mm; notes for condition/identity | ______ | ______ |
| **HF-020-M07** — antirotation/pilot holes | mm; notes for condition/identity | ______ | ______ |

HF-020 datum: A=panel outside face; B=button axis; C=key orientation

HF-020 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S03 / RAIL-PROFILE — Measure the local siderail/channel prototype

**A — OWNER CHECK / verify sample and support.** Dependencies: STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-021-M01** — Bend radii | mm; notes for condition/identity | ______ | ______ |
| **HF-021-M02** — sheet thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-021-M03** — glass capture | mm; notes for condition/identity | ______ | ______ |
| **HF-021-M04** — fastener flange | mm; notes for condition/identity | ______ | ______ |
| **HF-021-M05** — screw/head envelope | mm; notes for condition/identity | ______ | ______ |
| **HF-021-M06** — rail end relation to lockdown | mm; notes for condition/identity | ______ | ______ |

HF-021 datum: Cabinet side top plane and glass edge

HF-021 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S03 / LOCKDOWN-FIT — Check receiver, glass capture and hand-tool access

**A — OWNER CHECK / verify sample and support.** Dependencies: RAIL-PROFILE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-022-M01** — Receiver/catch pattern | mm; notes for condition/identity | ______ | ______ |
| **HF-022-M02** — latch travel | mm; notes for condition/identity | ______ | ______ |
| **HF-022-M03** — glass engagement | mm plus observed condition/state | ______ | ______ |
| **HF-022-M04** — front overlap | mm; notes for condition/identity | ______ | ______ |
| **HF-022-M05** — fastener access | mm plus observed condition/state | ______ | ______ |

HF-022 datum: Cabinet front top and centerline; actual side/rail/glass mockup

HF-022 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S03 / CONTROLS-HANDS — Try both hands and mark the four solid SSF zones

**A — OWNER CHECK / verify sample and support.** Dependencies: BUTTON-FAMILY, PLUNGER-STROKE, COIN-OPEN, LOCKDOWN-FIT.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-CONTROLS-SSF — Physical controls hand placement and solid SSF zones**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Owner placement/hand acceptance plus recorded internal clearance and structural ligament review. Preserve solid SSF plywood; final bores stay blocked. No fixed number of hand trials is specified. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / LEGS-BARE — Measure all four legs using the same datum jig

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: All four legs and matching installed fasteners.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-003-M01** — Both bolt center coordinates | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M02** — hole/slot widths | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M03** — corner included angle | deg and mm clearance; note state | ______ | ______ |
| **HF-003-M04** — flange width | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M05** — leg mounting face flatness | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M06** — bolt head seat | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M07** — leveler travel | mm; notes for condition/identity | ______ | ______ |
| **HF-003-M08** — record all four legs | text / instance IDs (grain also mark on sketch) | ______ | ______ |

HF-003 datum: A=inside leg mounting faces seated on 90-degree test corner; B=leg upper edge; C=corner bisector

HF-003 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / BRACKET-BARE — Measure brackets, backing and loose fastener stacks

**A — OWNER CHECK / verify sample and support.** Dependencies: LEGS-BARE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: All four bracket/backing stacks; preserve left/right differences.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-004-M01** — Flange thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-004-M04** — all hole centers/diameters | mm; notes for condition/identity | ______ | ______ |
| **HF-004-M05** — bolt/nut/washer stack | mm; notes for condition/identity | ______ | ______ |
| **HF-004-M07** — backing contact area | mm; notes for condition/identity | ______ | ______ |

HF-004 datum: A=inside cabinet wall plane; B=inside rear/front plane; C=bottom panel top; use measured-thickness corner fixture

HF-004 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / BEARINGS — Measure both bearing housings and bore interfaces

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Both housings, separately identified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-008-M01** — Bore at each bearing | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M02** — flange hole/slot centers and widths | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M03** — casting outline | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M04** — mounting-face to bore axis | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M05** — housing thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M06** — axial protrusions | mm; notes for condition/identity | ______ | ______ |
| **HF-008-M07** — set-screw access | mm plus observed condition/state | ______ | ______ |

HF-008 datum: A=flat mounting face; B=bore axis; C=line joining flange bolts; record both housings

HF-008 recording target (not machining fit): Bore/journal measurements ±0.02 mm with suitable gauges; hole centers ±0.10 mm; final fit from bearing/journal specification.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / BEARING-REF — File the maker misalignment limit as reference

**A — OWNER CHECK / verify sample and support.** Dependencies: BEARINGS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings.

Samples/repeats: Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-008-M08** — misalignment range documented by maker | reference document / maker-stated units; NOT a measured value | ______ | ______ |

HF-008 datum: A=flat mounting face; B=bore axis; C=line joining flange bolts; record both housings

HF-008 recording target (not machining fit): Bore/journal measurements ±0.02 mm with suitable gauges; hole centers ±0.10 mm; final fit from bearing/journal specification.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / JOURNALS — Inspect the physical journal/cheek-plate prototype

**A — OWNER CHECK / verify sample and support.** Dependencies: BEARINGS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-009-M01** — Journal fit/finish | mm; notes for condition/identity | ______ | ______ |
| **HF-009-M02** — engagement | mm plus observed condition/state | ______ | ______ |
| **HF-009-M03** — shoulder | mm; notes for condition/identity | ______ | ______ |
| **HF-009-M04** — axial retention | mm plus observed condition/state | ______ | ______ |
| **HF-009-M05** — plate-to-rail stack | mm; notes for condition/identity | ______ | ______ |
| **HF-009-M06** — bolt edge distances | mm; notes for condition/identity | ______ | ______ |
| **HF-009-M07** — shop drawing revision | text / instance IDs (grain also mark on sketch) | ______ | ______ |

HF-009 datum: Bearing axis and plate seating face; journal shoulder zero

HF-009 recording target (not machining fit): Bore/journal measurements ±0.02 mm with suitable gauges; hole centers ±0.10 mm; final fit from bearing/journal specification.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / PROPS-BARE — Measure both rods, clevises, pins and keepers

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Both rods and all lower/upper/stow hardware, separately labeled.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-010-M01** — Rod pin-to-pin length | mm; notes for condition/identity | ______ | ______ |
| **HF-010-M02** — section and end-eye geometry | mm; notes for condition/identity | ______ | ______ |
| **HF-010-M03** — lower clevis and upper receiver outlines/offsets/patterns | mm; notes for condition/identity | ______ | ______ |
| **HF-010-M04** — pin diameter and positive keeper engagement | mm plus observed condition/state | ______ | ______ |
| **HF-010-M05** — stow-clip retention/pattern | mm plus observed condition/state | ______ | ______ |

HF-010 datum: A=each anchor mounting face; B=pivot pin center; C=stay center plane; both handed units

HF-010 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / LATCH-PADS — Measure the closed latches and pads in the fixture

**A — OWNER CHECK / verify sample and support.** Dependencies: PROPS-BARE, JOURNALS, STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-012-M01** — Latch and catch holes | mm; notes for condition/identity | ______ | ______ |
| **HF-012-M02** — closed grip range | mm; notes for condition/identity | ______ | ______ |
| **HF-012-M03** — travel/release envelope | mm plus observed condition/state | ______ | ______ |
| **HF-012-M04** — pad footprint and loaded thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-012-M05** — attachment geometry | mm; notes for condition/identity | ______ | ______ |

HF-012 datum: A=seat/strike mounting surface; B=closed cradle rail underside; C=front end

HF-012 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S04 / PROP-MOTION — Check rod deployment and stow with independent support

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: PROPS-BARE, JOURNALS, LATCH-PADS, CONTROLS-HANDS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewed supported fixture, actual hardware, ruler/feeler gauges and camera; independent support as specified in the plan.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-010-M06** — complete swing | deg and mm clearance; note state | ______ | ______ |

HF-010 datum: A=each anchor mounting face; B=pivot pin center; C=stay center plane; both handed units

HF-010 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-PROP-MOTION — Both props deployment stow retention and accessibility**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: No rubbing, trapped fingers, snag, keeper interference or weak-skin contact; positive pins/keepers required. Narrow-corridor tolerance budget still needs approval. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / MAINS-FIT — Measure the unpowered mains module and enclosure together

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-017-M01** — Panel cutout | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M02** — fixing holes | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M03** — total depth | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M04** — plug/cord bend space | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M05** — disconnect travel | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M06** — strain-relief footprint | mm; notes for condition/identity | ______ | ______ |
| **HF-017-M07** — mounting stack | mm; notes for condition/identity | ______ | ______ |
| **HF-027-M01** — External bounds including mounts | mm; notes for condition/identity | ______ | ______ |
| **HF-027-M02** — lid screw/service clearance | mm; notes for condition/identity | ______ | ______ |
| **HF-027-M03** — cable gland projection | mm; notes for condition/identity | ______ | ______ |
| **HF-027-M04** — mounting hole pattern | mm; notes for condition/identity | ______ | ______ |
| **HF-027-M05** — protected entry | mm plus observed condition/state | ______ | ______ |

HF-017 datum: A=carrier rear face; B=carrier lower-left; C=entry axis; no exposed terminals in service space

HF-017 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

HF-027 datum: A=rear panel inside face; B=assembly lower-left; C=lid removal direction

HF-027 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / ETHERNET — Measure the optional network adapter, if selected

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-018-M01** — Coupler/keystone aperture | mm; notes for condition/identity | ______ | ______ |
| **HF-018-M02** — clip retention | mm plus observed condition/state | ______ | ______ |
| **HF-018-M03** — bend radius | mm; notes for condition/identity | ______ | ______ |

HF-018 datum: Carrier outside lower-left corner

HF-018 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / SSF-ADAPTER — Inspect exciter footprint and local cable clearance

**A — OWNER CHECK / verify sample and support.** Dependencies: CONTROLS-HANDS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Four locations; every different device/adapter type, with location IDs.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-031-M01** — Attachment footprint | mm; notes for condition/identity | ______ | ______ |
| **HF-031-M03** — projection | mm; notes for condition/identity | ______ | ______ |
| **HF-031-M04** — cable bend and service clearance | mm; notes for condition/identity | ______ | ______ |

HF-031 datum: Solid sidewall inside face; local adapter zero

HF-031 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / SSF-REF — File the adapter attachment specification

**A — OWNER CHECK / verify sample and support.** Dependencies: SSF-ADAPTER.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings.

Samples/repeats: Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-031-M02** — adapter screw or adhesive specification | reference document / maker-stated units; NOT a measured value | ______ | ______ |

HF-031 datum: Solid sidewall inside face; local adapter zero

HF-031 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / TRAYS — Remove and reinstall each tray with representative cables

**A — OWNER CHECK / verify sample and support.** Dependencies: MAINS-FIT, STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**SV-01 — Each electronics carrier with cabling**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Each tray independently removable/reinstalled with ordinary tools; no glue, cable pulling or entry into mains enclosure. Fasteners accessible/captive, strain relief and labels; record extraction direction/slack. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S05 / CENTRAL — Reach the central service area with cables installed

**A — OWNER CHECK / verify sample and support.** Dependencies: TRAYS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**SV-02 — Central service path**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Service work possible without removing permanent structure; cable bundles cannot fill the reserved access volume. No new minimum gap is defined. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / CPU-CASE — Measure the already-owned open case

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-014-M01** — Mounting hole centers/diameters | mm; notes for condition/identity | ______ | ______ |
| **HF-014-M02** — foot heights | mm; notes for condition/identity | ______ | ______ |
| **HF-014-M03** — standoff stack | mm; notes for condition/identity | ______ | ______ |
| **HF-014-M04** — connector and GPU restraint access | mm plus observed condition/state | ______ | ______ |

HF-014 datum: A=case feet plane; B=installed front-left corner; X=265 direction; Y=440 direction

HF-014 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / SLIDES-BARE — Measure the two slide members and travel

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Both slides; fixed and moving members separately.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-013-M01** — Body thickness each side | mm; notes for condition/identity | ______ | ______ |
| **HF-013-M03** — fixed/moving member outlines | mm; notes for condition/identity | ______ | ______ |
| **HF-013-M04** — hole and slot centers separately | mm; notes for condition/identity | ______ | ______ |
| **HF-013-M05** — travel | mm; notes for condition/identity | ______ | ______ |
| **HF-013-M06** — disconnect access | mm plus observed condition/state | ______ | ______ |
| **HF-013-M07** — closed stop position | mm; notes for condition/identity | ______ | ______ |
| **HF-013-M08** — screw-head limits | mm; notes for condition/identity | ______ | ______ |

HF-013 datum: A=fixed-member mounting face; B=closed rear end; C=lower edge; second sheet for moving member

HF-013 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / SLIDE-REF — File maker clearance and rating conditions

**A — OWNER CHECK / verify sample and support.** Dependencies: SLIDES-BARE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings.

Samples/repeats: Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-013-M02** — maker minimum/maximum side clearance | reference document / maker-stated units; NOT a measured value | ______ | ______ |
| **HF-013-M09** — rating conditions | reference document / maker-stated units; NOT a measured value | ______ | ______ |

HF-013 datum: A=fixed-member mounting face; B=closed rear end; C=lower edge; second sheet for moving member

HF-013 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / CLAMPS — Measure four clamps, backing and the retainer

**A — OWNER CHECK / verify sample and support.** Dependencies: SLIDES-BARE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: All four clamps/backing sets and the stowed retainer.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-026-M01** — Both angle legs/length/thickness | deg and mm clearance; note state | ______ | ______ |
| **HF-026-M02** — bend radius | mm; notes for condition/identity | ______ | ______ |
| **HF-026-M03** — all holes | mm; notes for condition/identity | ______ | ______ |
| **HF-026-M04** — backing thickness/area/pattern | mm; notes for condition/identity | ______ | ______ |
| **HF-026-M05** — bolt grade/diameter/stack | mm; notes for condition/identity | ______ | ______ |
| **HF-026-M06** — retainer stroke/holes/access | mm plus observed condition/state | ______ | ______ |

HF-026 datum: A=bottom top face; B=rail face; C=clamp front edge; backing measured separately

HF-026 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / CPU-HINGE — Measure both leaves of the CPU door hinge

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-015-M01** — Leaf widths/thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M02** — knuckle diameter | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M03** — axis-to-leaf offsets | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M04** — hole centers/diameters | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M05** — screw heads | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M06** — folded stack | mm; notes for condition/identity | ______ | ______ |
| **HF-015-M07** — available opening angle | deg and mm clearance; note state | ______ | ______ |

HF-015 datum: A=leaf seating face; B=hinge end; C=knuckle axis; measure both leaves separately

HF-015 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / CPU-LATCH — Measure latch, catch, gasket and tool access

**A — OWNER CHECK / verify sample and support.** Dependencies: CPU-HINGE.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-016-M01** — Body cutout | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M02** — antirotation flat | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M03** — fixing holes | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M04** — cam reach | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M05** — grip range | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M06** — catch geometry | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M07** — key/tool clearance | mm; notes for condition/identity | ______ | ______ |
| **HF-016-M08** — compressed gasket thickness | mm; notes for condition/identity | ______ | ______ |

HF-016 datum: A=door outside face; B=latch body center; C=cam closed axis

HF-016 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / REAR-STACK — Measure the installed rear-corner stack once

**A — OWNER CHECK / verify sample and support.** Dependencies: BRACKET-BARE, CLAMPS, CPU-CASE, CPU-LATCH, STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Both rear corners and all relevant slide positions.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-004-M02** — inner X at rear left/right when seated | mm; notes for condition/identity | ______ | ______ |
| **HF-004-M03** — full Y/Z extent | mm; notes for condition/identity | ______ | ______ |
| **HF-004-M06** — wrench access | mm plus observed condition/state | ______ | ______ |
| **HF-028-M01** — Minimum actual rail-to-bracket gap including flange/bolt/nut/washer | mm; notes for condition/identity | ______ | ______ |
| **HF-028-M02** — bracket Y/Z extent | mm; notes for condition/identity | ______ | ______ |
| **HF-028-M03** — slide side clearance | mm; notes for condition/identity | ______ | ______ |
| **HF-028-M04** — clamp/backing bounds at both rear corners | mm; notes for condition/identity | ______ | ______ |

HF-004 datum: A=inside cabinet wall plane; B=inside rear/front plane; C=bottom panel top; use measured-thickness corner fixture

HF-004 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

HF-028 datum: Cabinet global X/Y/Z from measured-stock corner fixture; retain signed left/right coordinates

HF-028 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Compare to the existing planning reserve; a nominal or positive gap alone does not release the stack. Actual clearance/fastener/load review remains required. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S06 / CPU-QUALIFY — Review CPU removal, then perform only approved CPU proof

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: REAR-STACK, CENTRAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**SV-03 — CPU service path and20kg payload proof**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Plan E SV-03 and hardware-pack CPU proof criteria apply. Existing numerical targets are proposed prototype targets requiring review, not a new certified rating. [Source](../docs/HARDWARE_MEASUREMENT_PACK_V25.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-HINGES — Measure the paired backbox hinges and pivots

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Both hinge assemblies; both leaves and mating pivot parts.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-006-M01** — Hole and slot centers | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M02** — hole diameters | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M03** — leaf outline/thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M04** — bend offsets | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M05** — pivot center to both mounting faces | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M06** — bushing OD/ID/flange/length | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M07** — bolt shoulder and thread | mm; notes for condition/identity | ______ | ______ |
| **HF-006-M09** — left/right differences | mm; notes for condition/identity | ______ | ______ |

HF-006 datum: A=each hinge mounting face; B=rear edge; C=bottom edge; pivot center separately recorded

HF-006 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-LOCKS — Measure upright locks in the supported hinge fixture

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: BB-HINGES, STOCK-THICK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewed supported fixture, actual hardware, ruler/feeler gauges and camera; independent support as specified in the plan.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-006-M08** — full folded/upright sweep | deg and mm clearance; note state | ______ | ______ |
| **HF-007-M01** — Thread | mm; notes for condition/identity | ______ | ______ |
| **HF-007-M02** — grip length | mm; notes for condition/identity | ______ | ______ |
| **HF-007-M03** — head/tool envelope | mm; notes for condition/identity | ______ | ______ |
| **HF-007-M04** — captive plate hole pattern | mm; notes for condition/identity | ______ | ______ |
| **HF-007-M05** — engagement | mm plus observed condition/state | ______ | ______ |
| **HF-007-M06** — shelf/floor/gasket stack | mm; notes for condition/identity | ______ | ______ |
| **HF-007-M07** — X and Y after hinge fixture | mm; notes for condition/identity | ______ | ______ |

HF-006 datum: A=each hinge mounting face; B=rear edge; C=bottom edge; pivot center separately recorded

HF-006 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

HF-007 datum: A=rear shelf top; B=cabinet centerline; C=rear exterior plane; upright on fixture

HF-007 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-DOOR — Measure and service the rear door

**A — OWNER CHECK / verify sample and support.** Dependencies: BB-LOCKS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-029-M01** — Hinge leaves/axis/holes | mm; notes for condition/identity | ______ | ______ |
| **HF-029-M02** — lock body/catch/cutout | mm; notes for condition/identity | ______ | ______ |
| **HF-029-M03** — gasket compressed thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-029-M04** — door clearance and opening sweep | deg and mm clearance; note state | ______ | ______ |

HF-029 datum: A=backbox rear frame outer face; B=opening lower-left; C=door hinge edge

HF-029 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**SV-04 — Backbox rear door servicing**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Outward operation/retention without rubbing; service access demonstrated. Door is not primary shear structure; no moving fan wiring required. Actual hinge and gasket fit still reviewed. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-MONITOR — Measure the later selected backglass on the bench

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. Use a suitable scale for actual mass, with stable support/assistance.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-025-M01** — VESA | mm; notes for condition/identity | ______ | ______ |
| **HF-025-M02** — bezel | mm; notes for condition/identity | ______ | ______ |
| **HF-025-M03** — connector space | mm; notes for condition/identity | ______ | ______ |
| **HF-025-M04** — mass | kg | ______ | ______ |

HF-025 datum: Rail cage mounting plane

HF-025 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-SPEAKERS — Measure later speaker modules and baffles together

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-033-M01** — Driver cutout | mm; notes for condition/identity | ______ | ______ |
| **HF-033-M02** — screw pattern | mm; notes for condition/identity | ______ | ______ |
| **HF-033-M03** — rear magnet/connector depth | mm; notes for condition/identity | ______ | ______ |
| **HF-033-M04** — baffle thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-033-M05** — rail-cage adapter attachment | mm; notes for condition/identity | ______ | ______ |

HF-033 datum: Removable speaker module front face; centerline

HF-033 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S07 / BB-REMOVE — Rehearse full monitor replacement through the front

**A — OWNER CHECK / verify sample and support.** Dependencies: BB-DOOR.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**SV-05 — Full monitor front replacement**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Front removal/reinstallation demonstrated with safe access, tools and assistance; dummy is envelope-only, not final actual-monitor acceptance. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S08 / FILTER — Inspect the later filter cassette/media and removal route

**A — OWNER CHECK / verify sample and support.** Dependencies: STOCK-SURVEY.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-032-M01** — Filter compression and service clearance | mm; notes for condition/identity | ______ | ______ |

HF-032 datum: Generic cassette/adapter mounting face and project-designed mounting grid

HF-032 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-AIRFLOW — Slots filter passages packaging**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Use existing plan F packaging dimensions/screens; no thermal adequacy from slot area. Do not trim structural wood to fit a fan. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S08 / FANS — Measure later fans, guards and removable adapters

**A — OWNER CHECK / verify sample and support.** Dependencies: FILTER.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-032-M02** — fan thickness | mm; notes for condition/identity | ______ | ______ |
| **HF-032-M03** — grille/finger guard | mm; notes for condition/identity | ______ | ______ |
| **HF-032-M04** — fan pattern on adapter only | mm; notes for condition/identity | ______ | ______ |

HF-032 datum: Generic cassette/adapter mounting face and project-designed mounting grid

HF-032 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S09 / PF-DISPLAY — Measure later playfield adapter and connector fit

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-024-M01** — VESA | mm; notes for condition/identity | ______ | ______ |
| **HF-024-M02** — connector access | mm plus observed condition/state | ______ | ______ |

HF-024 datum: Cradle local axes and display mounting plane

HF-024 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S09 / MOVING-MASS — Weigh and reconcile the actual moving assembly

**A — OWNER CHECK / verify sample and support.** Dependencies: PF-DISPLAY.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Suitable scale with recorded uncertainty and stable supports/assistance; no unsafe balancing.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-MASS — Actual completed moving mass**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Actual included mass, identity and scale uncertainty documented; the preliminary mass is not a reading. No new mass acceptance limit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S09 / LIFT — Record lift effort and the owner's controlled descent trial

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: MOVING-MASS, PROP-MOTION.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Force gauge, angle measurement, approved fixture and independent backup; actual intended grip.

Samples/repeats: Three slow cycles; closed then 10-degree increments and all local peaks through service, as in plan C.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-024-M03** — completed moving mass and manual lifting force at the front grip | kg and N; grip coordinates mm; angle deg | ______ | ______ |

HF-024 datum: Cradle local axes and display mounting plane

HF-024 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-ERGONOMICS — Measured lift effort and owner opening/closing acceptance**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Owner must accept comfortable, controllable opening/holding/prop operation/closing plus reviewed force data. Predicted ~86 N is not an acceptance threshold. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S10 / PROP-LEFT — LEFT prop independent full-load proof

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: PROP-MOTION, MOVING-MASS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-PROP-L — LEFT independent full-load qualification**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Only reviewed plan B qualification applies. Proposed residual-set screen does not supply the still-missing loaded-deflection limit. No unreviewed PASS. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S10 / PROP-RIGHT — RIGHT prop proof and reconcile the pair's capacity evidence

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: PROP-LEFT.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-010-M07** — one-prop load capacity | reviewed test report; units from approved procedure | ______ | ______ |

HF-010 datum: A=each anchor mounting face; B=pivot pin center; C=stay center plane; both handed units

HF-010 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-PROP-R — RIGHT independent full-load qualification**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Both independent proofs and qualification scope must be reviewed. A single-side pass or static hold alone cannot establish the whole qualification. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S10 / LOADS — Obtain the remaining reviewed structural load qualifications

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: LEGS-BARE, BRACKET-BARE, JOURNALS, BB-LOCKS, LOCKDOWN-FIT.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-022-M06** — loaded deflection | mm; notes for condition/identity | ______ | ______ |

HF-022 datum: Cabinet front top and centerline; actual side/rail/glass mockup

HF-022 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

**PV-LOADS — Leg backbox pivot lockdown load qualification**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Reviewed qualification scope, numerical criteria and evidence required by freeze Gate 1. Undefined tests remain OPEN. [Source](../docs/CNC_FREEZE_GATE_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S10 / SKATES — Later mobility engagement/stability check

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: LOADS.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-005-M01** — Leg engagement and stability before mobility use | reviewed test report; units from approved procedure | ______ | ______ |

HF-005 datum: Actual installed legs

HF-005 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Physical engagement/stability before mobility use as required by the measurement pack; no numerical mobility test criteria exist here. [Source](../docs/HARDWARE_MEASUREMENT_PACK_V25.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S11 / GLASS — Later final supported glass-opening measurement

**A — OWNER CHECK / verify sample and support.** Dependencies: RAIL-PROFILE, LOCKDOWN-FIT.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Measurement ID / exact item | Units | Value / sub-readings | Repeat |
|---|---|---|---|
| **HF-023-M01** — Finished supported opening | mm; notes for condition/identity | ______ | ______ |
| **HF-023-M02** — engagement and expansion clearances | mm plus observed condition/state | ______ | ______ |
| **HF-023-M03** — thickness sample | mm; notes for condition/identity | ______ | ______ |

HF-023 datum: Assembled supported glass plane

HF-023 recording target (not machining fit): Record hole centers/stack to ±0.10 mm; outline to ±0.5 mm; repeat both parts. This is measurement uncertainty, NOT machining tolerance.

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S11 / ELECTRICAL — Obtain protected electrical/cable/fold commissioning evidence

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: MAINS-FIT, BB-LOCKS, TRAYS, REAR-STACK.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Instruments and protected setup specified in the reviewed commissioning plan; none selected here.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-ELECTRICAL — Protected electrical and cable/fold commissioning**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Existing source electrical/safety and freeze gates apply; no new electrical procedure or pass limit. [Source](../docs/CNC_FREEZE_GATE_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S11 / THERMAL — Defer thermal commissioning until reviewed conditions exist

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: FANS, ELECTRICAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Instruments and protected setup specified in the reviewed commissioning plan; none selected here.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-THERMAL — Final thermal commissioning**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: Limits must come from selected equipment and the reviewed commissioning plan. Slot area and CAD arrows cannot pass this trial. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S11 / RECONCILE — Return sheets and evidence without filling gaps from estimates

**A — OWNER CHECK / verify sample and support.** Dependencies: ARRIVAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks.

Samples/repeats: One preparation/handoff record; no specimen repetitions.


Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: No unknown, duplicated or omitted authoritative IDs; unperformed work remains blank/OPEN. This is evidence handoff, not geometry release. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## S11 / PACKAGE — Engineering/owner review of the eventual final CNC package

**B — REVIEW REQUIRED BEFORE EXECUTION.** Dependencies: RECONCILE, SHOP-COUPON, PROP-RIGHT, LOADS, CPU-QUALIFY, LIFT, BB-REMOVE, FILTER, ELECTRICAL, THERMAL.

Date: __________  Operator: __________  Sample ID / side / batch: ____________________

Instrument / resolution / zero check: ____________________  Uncertainty: __________

Datum sketch / fixture revision: ____________________  Evidence prefix: ____________________

Tools: Evidence records, original freeze gate and qualified reviewers; no physical operation authorized.

Samples/repeats: Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**PV-CNC-PACKAGE — Final drawings fasteners laminate IDs nesting export review owner approval**

Approved criteria / reviewer / date: ______________________________________________

| Step / state / units | Reading | Repeat | Observation / evidence |
|---|---|---|---|
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |
| __________ | __________ | __________ | ____________________ |

Trial outcome: OPEN / FAIL / PASS ______  Reviewer / date: ____________________

Failure observations / limitations / retest: __________________________________________

Notes / sub-reading IDs / photo references: __________________________________________

________________________________________________________________________________

Collected: ____  Observed fit issue: ____  Acceptance: OPEN / FAIL / PASS / N/A ____

Existing criterion: All three existing freeze gates; no release by checklist or queue status. [Source](../docs/CNC_FREEZE_GATE_V27.md).

Collection alone does not release geometry. Unknown acceptance stays OPEN.

<div style="break-after: page; page-break-after: always;"></div>

## Extra pattern / sub-reading sheet

Parent authoritative measurement ID: __________  Operation: __________  Sample/side: __________

Date/operator: __________  Instrument/uncertainty: __________  Datum sketch: __________

Name horizontal and vertical datum axes on the sketch before measuring. Retain signed offsets; never infer a pattern from a photograph.

| Hole/slot/sub-reading label | First datum offset mm | Second datum offset mm | Diameter/width/depth mm | Repeat / evidence |
|---|---|---|---|---|
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ |

Notes: ______________________________________________________________________

# Owner physical checklist — v27

Derived owner convenience copy. Authoritative values remain in [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). No measurements are filled; manufacturing stays **BLOCKED**. Regenerate with `python3 tools/generate_owner_execution_v27.py`; do not write bench results into generated files.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

## Start here — Session 0

**First action: PREP.** Bring a pen, labels/masking tape, marker, phone/camera, steel rule/square, the available caliper/micrometer, and blank sheets or a device displaying this checklist. No cabinet hardware or ballast is needed. Identify/zero-check tools; sort whatever has arrived using the arrival sheet. Missing tools/samples can be noted now; do not buy all later electronics.

**186 authoritative measurements + 18 authoritative trials → 55 practical owner operations in 12 sessions.** The count includes three preparation/handoff operations and deferred shop/reviewer tasks; it is not a claim that all operations can be performed today.

**A — ordinary owner checks:** unpowered loose-part measurements and supported light mockups, using the source plan constraints. **B — STOP for review:** proof/load, supported heavy movement, shop work or commissioning requiring the existing reviewed setup/criteria. Both prop proofs are B. No load, safety factor, fixture design or acceptance limit is added here.

Work down each session; skip unavailable WAIT items and return later. Dependencies name operations whose evidence/setup is needed, not permission to declare their results accepted. Session 11 accepts an incomplete evidence handoff now; final review/commissioning can remain pending. Photos are selective: reuse labeled setup views rather than photographing every reading.

Print [measurement sheets](OWNER_MEASUREMENT_SHEETS_V27.md) for the next action only. See [arrival inspection](HARDWARE_ARRIVAL_INSPECTION_V27.md) and [photo plan](OWNER_EVIDENCE_PLAN_V27.md). On paper write the authoritative ID; JSON locations below are for later transcription, not instructions to interpret CAD.

## Session index

- Session 0: Tools and preparation — 2 operations
- Session 1: Sheet stock / material measurements — 3 operations
- Session 2: Plunger and visible controls — 4 operations
- Session 3: Buttons and control-panel ergonomics — 4 operations
- Session 4: Captive props and mounting hardware — 8 operations
- Session 5: Electronics carriers and cable serviceability — 6 operations
- Session 6: CPU access — 8 operations
- Session 7: Backbox / monitor access — 6 operations
- Session 8: Filter and airflow path — 2 operations
- Session 9: Moving assembly mass and lift effort — 3 operations
- Session 10: Reviewed proof testing — 4 operations
- Session 11: Final evidence reconciliation — 5 operations

## Collection savings

42 operations collect the 186 measurement records; all 18 trials are mapped once. Some measurement and trial work shares the same operation. Three preparation/handoff operations bring the total to 55.

- Thickness min/max reuse the nine-point readings. Record all four leg instances without repeating them to fill the identity record.
- Loose patterns, diameters and seating depths share a component setup; each original ID remains separate.
- One rear-corner fixture supplies both HF-004 and HF-028 readings. One mains assembly supplies HF-017 and HF-027 entries.
- Mass measurements feed the composite lift entry. Both prop proof reports feed the capacity entry; neither proof is omitted.
- Four maker/attachment specification entries are reference-only collection steps; no invented physical reading is needed.

## Ledger transcription key

For measurement paths below, enter actual value, units, raw repeats, instrument, uncertainty, source_kind and repository-relative evidence paths; identify the part, date/operator and datums on its component record. Trial paths receive fixture revision, date/operator, physical IDs, criteria/reviewer, evidence, result/limitations and status. Preserve failed trials. A composite field may need separate left/right or sub-reading values with units. Never fill unknowns from the provisional context.

**Reference mismatch:** HF-008-M08, HF-013-M02/M09 and HF-031-M02 ask for documented specifications. File reference text/revision in notes and return it for engineering review; keep measured_value null. The accepted ledger validator intentionally rejects catalogue promotion. This package does not change that schema or gate.

## Session 0 — Tools and preparation

- [ ] **PREP** (A) — Prepare the bench and result folder
- [ ] **ARRIVAL** (A) — Sort delivered samples and identify missing items

### PREP

**Component:** Prepare the bench and result folder

Open this checklist and print only the next operation sheets. Gather a pen, labels/masking tape, marker, phone/camera, ruler/square and the available measuring tools. Check instrument identity, resolution and zero; do not assume a ruler can resolve a bore fit. Make one folder per session; label every sample and handed side. No cabinet component is needed for this preparation step.

**Before starting:** None. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks. **Samples/repeats:** One preparation/handoff record; no specimen repetitions.

Record preparation/handoff notes on paper; no authoritative result ID is invented for this housekeeping step.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S00_PREP_<view>_<sequence>.jpg`.

**Existing criterion:** Prepared labels, blank sheets and working instruments only; no dimensional or ergonomic acceptance. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### ARRIVAL

**Component:** Sort delivered samples and identify missing items

Use HARDWARE_ARRIVAL_INSPECTION_V27.md. Mark arrived / missing on paper. The case HF-014 is the only sample explicitly documented as already owned. Put maker drawings/specifications in a REFERENCE folder; do not enter them as measured values. Missing equipment means defer its operation, not buy an unapproved substitute.

**Before starting:** PREP. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks. **Samples/repeats:** One preparation/handoff record; no specimen repetitions.

Record preparation/handoff notes on paper; no authoritative result ID is invented for this housekeeping step.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity Naming: `PV27_S00_ARRIVAL_<view>_<sequence>.jpg`.

**Existing criterion:** Identity and arrival recorded; no fit approval. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 1 — Sheet stock / material measurements

- [ ] **STOCK-THICK** (A) — Measure sheet thickness once; retain all readings and min/max
- [ ] **STOCK-SURVEY** (A) — Survey the same labeled sheet
- [ ] **SHOP-COUPON** (B) — Arrange shop tool readings and the physical fit coupon

### STOCK-THICK

**Component:** Production 18 mm plywood sheets

Mark nine distributed points on each actual sheet, including each door-stock batch. Measure without compressing veneers. Derive min/max from those same readings; do not remeasure just to fill M02.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Micrometer or broad-jaw caliper; straightedge/feeler gauges **Samples/repeats:** Nine points per sheet; all actual main and different door stock. Repeat readings where instrument repeatability is uncertain; no fixed repeat count otherwise specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-001-M01 | Thickness at 9 distributed points per sheet | mm; notes for condition/identity | `/components/0/measurements/0` |
| HF-001-M02 | min/max | mm; notes for condition/identity | `/components/0/measurements/1` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, datum, reading, point-map Naming: `PV27_S01_STOCK-THICK_<view>_<sequence>.jpg`.

**Existing criterion:** Recording target ±0.05 mm; retain spread. This does not approve sheet fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### STOCK-SURVEY

**Component:** Production 18 mm plywood sheets

Keep the sheet label and corner datum. Measure sheet bounds and bow; note defects, grain and batch on one sketch. Reuse the identity photo from STOCK-THICK.

**Before starting:** STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Steel rule/tape, straightedge, feeler gauges, pencil and labeled sheet sketch. **Samples/repeats:** Every actual sheet/batch; no additional fixed repetition count in the plan.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-001-M03 | sheet dimensions | mm; notes for condition/identity | `/components/0/measurements/2` |
| HF-001-M04 | bow | mm; notes for condition/identity | `/components/0/measurements/3` |
| HF-001-M05 | face/core defects | text / instance IDs (grain also mark on sketch) | `/components/0/measurements/4` |
| HF-001-M06 | grain direction | text / instance IDs (grain also mark on sketch) | `/components/0/measurements/5` |
| HF-001-M07 | batch ID | text / instance IDs (grain also mark on sketch) | `/components/0/measurements/6` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** point-map, defect-if-present Naming: `PV27_S01_STOCK-SURVEY_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SHOP-COUPON

**Component:** Production 18 mm plywood sheets; CNC cutter/tooling and tolerance coupon

Request actual cutter/runout and coupon results from the CNC shop. Do not measure a running spindle. Record each result separately using the shop instrument and coupon identity. Consultation now is already authorized; this is not a new machine/tool purchase.

**Before starting:** STOCK-SURVEY. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** CNC shop supplies its tooling/runout/depth/registration instruments and identified physical coupon. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-002-M01 | Actual cutter diameter | mm; notes for condition/identity | `/components/1/measurements/0` |
| HF-002-M02 | runout | mm; notes for condition/identity | `/components/1/measurements/1` |
| HF-002-M03 | pocket depth accuracy | mm; notes for condition/identity | `/components/1/measurements/2` |
| HF-002-M04 | accepted groove clearance | mm; notes for condition/identity | `/components/1/measurements/3` |
| HF-002-M05 | relief radius | mm; notes for condition/identity | `/components/1/measurements/4` |
| HF-002-M06 | two-face registration accuracy | mm; notes for condition/identity | `/components/1/measurements/5` |

**Trial PV-STOCK-TOOL:** Measured stock cutter clearance coupon. Record at `/physical_trials/14`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, coupon, reading Naming: `PV27_S01_SHOP-COUPON_<view>_<sequence>.jpg`.

**Existing criterion:** Shop-confirmed tool/fit/relief/two-face setup and physical coupon/dry fit required by the freeze gate; missing criteria stay OPEN. [Source](../docs/CNC_FREEZE_GATE_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 2 — Plunger and visible controls

- [ ] **PLUNGER-FACE** (A) — Measure the plunger mounting face and seating stack
- [ ] **PLUNGER-STROKE** (A) — Check the complete plunger stroke in its mock panel
- [ ] **COIN-FACE** (A) — Measure coin-door cutout, flange and bolts together
- [ ] **COIN-OPEN** (A) — Check coin-door swing and key/tool access

### PLUNGER-FACE

**Component:** Mechanical/electronic plunger assembly

Identify front seating face A, shaft axis B and antirotation C. Use one face sketch for contour/flats, all hole centers, sleeve/shaft diameters, flange/nut stack and internal body/sensor depth. Keep the pattern readings separate from the shape readings.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Delivered plunger and every installed mounting variant; repeat pattern from an independent reference.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-030-M01 | Front cutout contour | mm; notes for condition/identity | `/components/28/measurements/0` |
| HF-030-M02 | hole centers | mm; notes for condition/identity | `/components/28/measurements/1` |
| HF-030-M03 | sleeve/shaft diameter | mm; notes for condition/identity | `/components/28/measurements/2` |
| HF-030-M04 | flange and nut stack | mm; notes for condition/identity | `/components/28/measurements/3` |
| HF-030-M07 | internal body/sensor depth | mm; notes for condition/identity | `/components/28/measurements/6` |

**Linked blockers:** CF-0026 (CAB-FRONT-001-R1)

**Evidence:** identity, datum, mount-face, reading Naming: `PV27_S02_PLUNGER-FACE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### PLUNGER-STROKE

**Component:** Mechanical/electronic plunger assembly

Use the actual mechanism in a sacrificial thickness-matched panel. Record rest, full pull and inward limit; handle projection and connector/cable movement. Check adjacent controls, coin-door swing, leg stack, props and cradle using the plan. Record missing neighboring hardware as a limitation; do not mark final PASS without it.

**Before starting:** PLUNGER-FACE, STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** At least 20 deliberate full-stroke cycles, as required by plan A.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-030-M05 | stroke | mm; notes for condition/identity | `/components/28/measurements/4` |
| HF-030-M06 | handle projection | mm; notes for condition/identity | `/components/28/measurements/5` |
| HF-030-M08 | cable/connector sweep | deg and mm clearance; note state | `/components/28/measurements/7` |

**Trial PV-PLUNGER:** Physical plunger pattern stroke and clearance. Record at `/physical_trials/0`; use the existing plan/procedure.

**Linked blockers:** CF-0026 (CAB-FRONT-001-R1)

**Evidence:** rest, full-pull, inward-limit, rear-clearance, interference-if-present Naming: `PV27_S02_PLUNGER-STROKE_<view>_<sequence>.jpg`.

**Existing criterion:** No contact, snag, binding, unintended activation or pinch; full return/stroke and retained fasteners. Reviewer-approved positive clearance budget and ergonomic acceptance still required before bore release. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### COIN-FACE

**Component:** Coin door

Use one mounting-face sketch; include contour/radii, flange coverage, all holes and deepest internal protrusion.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-019-M01 | Required cutout contour/radii | mm; notes for condition/identity | `/components/17/measurements/0` |
| HF-019-M02 | flange coverage | mm; notes for condition/identity | `/components/17/measurements/1` |
| HF-019-M03 | all mounting holes | mm; notes for condition/identity | `/components/17/measurements/2` |
| HF-019-M04 | body/depth | mm; notes for condition/identity | `/components/17/measurements/3` |
| HF-019-M07 | coin mechanism protrusion | mm; notes for condition/identity | `/components/17/measurements/6` |

**Linked blockers:** CF-0023 (CAB-FRONT-001-R1)

**Evidence:** identity, mount-face, rear-clearance Naming: `PV27_S02_COIN-FACE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### COIN-OPEN

**Component:** Coin door

Check open/closed positions and access in the same front mockup used for the controls; share context photos with PLUNGER-STROKE.

**Before starting:** COIN-FACE. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-019-M05 | hinge swing | deg and mm clearance; note state | `/components/17/measurements/4` |
| HF-019-M06 | lock/key access | mm plus observed condition/state | `/components/17/measurements/5` |

**Linked blockers:** CF-0023 (CAB-FRONT-001-R1)

**Evidence:** closed, open, rear-clearance Naming: `PV27_S02_COIN-OPEN_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 3 — Buttons and control-panel ergonomics

- [ ] **BUTTON-FAMILY** (A) — Measure each button family in one caliper setup
- [ ] **RAIL-PROFILE** (A) — Measure the local siderail/channel prototype
- [ ] **LOCKDOWN-FIT** (A) — Check receiver, glass capture and hand-tool access
- [ ] **CONTROLS-HANDS** (A) — Try both hands and mark the four solid SSF zones

### BUTTON-FAMILY

**Component:** Flipper/start/launch buttons

For each distinct button family, sketch bore/flats and antirotation, then bezel, thread, nut/washer and switch/connector depths. Measure actual nuts, washers and terminals, not just the button body.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** One real sample of every final button family; identify every variant. Repeat readings to establish instrument repeatability; no fixed count supplied.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-020-M01 | Bore and flats | mm; notes for condition/identity | `/components/18/measurements/0` |
| HF-020-M02 | bezel OD | mm; notes for condition/identity | `/components/18/measurements/1` |
| HF-020-M03 | threaded length | mm; notes for condition/identity | `/components/18/measurements/2` |
| HF-020-M04 | nut/washer OD | mm; notes for condition/identity | `/components/18/measurements/3` |
| HF-020-M05 | switch depth | mm; notes for condition/identity | `/components/18/measurements/4` |
| HF-020-M06 | connector clearance | mm; notes for condition/identity | `/components/18/measurements/5` |
| HF-020-M07 | antirotation/pilot holes | mm; notes for condition/identity | `/components/18/measurements/6` |

**Linked blockers:** CF-0008 (CAB-SIDE-001L-R1), CF-0017 (CAB-SIDE-001R-R1), CF-0024 (CAB-FRONT-001-R1)

**Evidence:** identity, mount-face, rear-clearance, reading Naming: `PV27_S03_BUTTON-FAMILY_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### RAIL-PROFILE

**Component:** Playfield siderail profile

Use the already-required short local profile prototype and safe glass-thickness gauge/mock panel. Record cross-section and its relation to the lockdown. Do not order final tempered glass from this step.

**Before starting:** STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-021-M01 | Bend radii | mm; notes for condition/identity | `/components/19/measurements/0` |
| HF-021-M02 | sheet thickness | mm; notes for condition/identity | `/components/19/measurements/1` |
| HF-021-M03 | glass capture | mm; notes for condition/identity | `/components/19/measurements/2` |
| HF-021-M04 | fastener flange | mm; notes for condition/identity | `/components/19/measurements/3` |
| HF-021-M05 | screw/head envelope | mm; notes for condition/identity | `/components/19/measurements/4` |
| HF-021-M06 | rail end relation to lockdown | mm; notes for condition/identity | `/components/19/measurements/5` |

**Linked blockers:** CF-0009 (CAB-SIDE-001L-R1), CF-0018 (CAB-SIDE-001R-R1)

**Evidence:** identity, section, installed Naming: `PV27_S03_RAIL-PROFILE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### LOCKDOWN-FIT

**Component:** 600 mm lockdown bar + receiver

Use the local lockdown/receiver prototype in the same front/side mockup. No load test here; loaded deflection is collected later under LOADS.

**Before starting:** RAIL-PROFILE. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-022-M01 | Receiver/catch pattern | mm; notes for condition/identity | `/components/20/measurements/0` |
| HF-022-M02 | latch travel | mm; notes for condition/identity | `/components/20/measurements/1` |
| HF-022-M03 | glass engagement | mm plus observed condition/state | `/components/20/measurements/2` |
| HF-022-M04 | front overlap | mm; notes for condition/identity | `/components/20/measurements/3` |
| HF-022-M05 | fastener access | mm plus observed condition/state | `/components/20/measurements/4` |

**Linked blockers:** CF-0025 (CAB-FRONT-001-R1)

**Evidence:** mount-face, latched, released, tool-access Naming: `PV27_S03_LOCKDOWN-FIT_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CONTROLS-HANDS

**Component:** Flipper/start/launch buttons; Mechanical/electronic plunger assembly; Four exciters and local attachment adapters

Use intended leg height/slope and actual buttons/plunger. Try sustained play, both hands, simultaneous buttons, optional action and full plunger stroke. Check internal nuts/cables and mark all four SSF zones; use the source plan D for the existing candidate layout, never read dimensions from a render.

**Before starting:** BUTTON-FAMILY, PLUNGER-STROKE, COIN-OPEN, LOCKDOWN-FIT. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-CONTROLS-SSF:** Physical controls hand placement and solid SSF zones. Record at `/physical_trials/6`; use the existing plan/procedure.

**Linked blockers:** CF-0008 (CAB-SIDE-001L-R1), CF-0017 (CAB-SIDE-001R-R1), CF-0024 (CAB-FRONT-001-R1), CF-0026 (CAB-FRONT-001-R1)

**Evidence:** hand-placement, rear-clearance, ssf-zones Naming: `PV27_S03_CONTROLS-HANDS_<view>_<sequence>.jpg`.

**Existing criterion:** Owner placement/hand acceptance plus recorded internal clearance and structural ligament review. Preserve solid SSF plywood; final bores stay blocked. No fixed number of hand trials is specified. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 4 — Captive props and mounting hardware

- [ ] **LEGS-BARE** (A) — Measure all four legs using the same datum jig
- [ ] **BRACKET-BARE** (A) — Measure brackets, backing and loose fastener stacks
- [ ] **BEARINGS** (A) — Measure both bearing housings and bore interfaces
- [ ] **BEARING-REF** (A) — File the maker misalignment limit as reference
- [ ] **JOURNALS** (A) — Inspect the physical journal/cheek-plate prototype
- [ ] **PROPS-BARE** (A) — Measure both rods, clevises, pins and keepers
- [ ] **LATCH-PADS** (A) — Measure the closed latches and pads in the fixture
- [ ] **PROP-MOTION** (B) — Check rod deployment and stow with independent support

### LEGS-BARE

**Component:** Classic pinball leg set

Record bolt centers/slots, angle, flange/seat flatness and leveler travel for each labeled leg. M08 identifies the four instances; reuse their readings rather than repeating the entire set.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** All four legs and matching installed fasteners.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-003-M01 | Both bolt center coordinates | mm; notes for condition/identity | `/components/2/measurements/0` |
| HF-003-M02 | hole/slot widths | mm; notes for condition/identity | `/components/2/measurements/1` |
| HF-003-M03 | corner included angle | deg and mm clearance; note state | `/components/2/measurements/2` |
| HF-003-M04 | flange width | mm; notes for condition/identity | `/components/2/measurements/3` |
| HF-003-M05 | leg mounting face flatness | mm; notes for condition/identity | `/components/2/measurements/4` |
| HF-003-M06 | bolt head seat | mm; notes for condition/identity | `/components/2/measurements/5` |
| HF-003-M07 | leveler travel | mm; notes for condition/identity | `/components/2/measurements/6` |
| HF-003-M08 | record all four legs | text / instance IDs (grain also mark on sketch) | `/components/2/measurements/7` |

**Linked blockers:** CF-0003 (CAB-SIDE-001L-R1), CF-0012 (CAB-SIDE-001R-R1), CF-0021 (CAB-FRONT-001-R1), CF-0029 (CAB-REAR-001-R3)

**Evidence:** identity, mount-face, reading Naming: `PV27_S04_LEGS-BARE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BRACKET-BARE

**Component:** Compact internal leg brackets/backing

Keep each bracket with its own leg/bolts. Record thickness, pattern, assembled bolt/nut/washer stack and backing contact. Installed rear X/Y/Z readings are deferred to REAR-STACK so the corner fixture is built once.

**Before starting:** LEGS-BARE. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** All four bracket/backing stacks; preserve left/right differences.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-004-M01 | Flange thickness | mm; notes for condition/identity | `/components/3/measurements/0` |
| HF-004-M04 | all hole centers/diameters | mm; notes for condition/identity | `/components/3/measurements/3` |
| HF-004-M05 | bolt/nut/washer stack | mm; notes for condition/identity | `/components/3/measurements/4` |
| HF-004-M07 | backing contact area | mm; notes for condition/identity | `/components/3/measurements/6` |

**Linked blockers:** CF-0004 (CAB-SIDE-001L-R1), CF-0013 (CAB-SIDE-001R-R1), CF-0022 (CAB-FRONT-001-R1), CF-0030 (CAB-REAR-001-R3)

**Evidence:** mount-face, bolt-stack, backing-contact Naming: `PV27_S04_BRACKET-BARE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BEARINGS

**Component:** UCFL202 15 mm flange bearing pair

Use suitable bore/pin gauges for fit-critical bores; calipers for outline and mounting pattern. Record face-to-axis offset and access to set screws on both housings.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Both housings, separately identified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-008-M01 | Bore at each bearing | mm; notes for condition/identity | `/components/7/measurements/0` |
| HF-008-M02 | flange hole/slot centers and widths | mm; notes for condition/identity | `/components/7/measurements/1` |
| HF-008-M03 | casting outline | mm; notes for condition/identity | `/components/7/measurements/2` |
| HF-008-M04 | mounting-face to bore axis | mm; notes for condition/identity | `/components/7/measurements/3` |
| HF-008-M05 | housing thickness | mm; notes for condition/identity | `/components/7/measurements/4` |
| HF-008-M06 | axial protrusions | mm; notes for condition/identity | `/components/7/measurements/5` |
| HF-008-M07 | set-screw access | mm plus observed condition/state | `/components/7/measurements/6` |

**Linked blockers:** CF-0006 (CAB-SIDE-001L-R1), CF-0015 (CAB-SIDE-001R-R1)

**Evidence:** identity, mount-face, bore-reading, tool-access Naming: `PV27_S04_BEARINGS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BEARING-REF

**Component:** UCFL202 15 mm flange bearing pair

Save the maker document identity/revision and stated misalignment limit on the reference sheet. This ID asks for documented maker data, not a physically measured angle limit. Leave measured_value null; return the reference for engineering review without weakening the evidence validator.

**Before starting:** BEARINGS. **Hold:** REFERENCE_ONLY.

**Instrument:** Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings. **Samples/repeats:** Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-008-M08 | misalignment range documented by maker | reference document / maker-stated units; NOT a measured value | `/components/7/measurements/7` |

**Linked blockers:** CF-0006 (CAB-SIDE-001L-R1), CF-0015 (CAB-SIDE-001R-R1)

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S04_BEARING-REF_<view>_<sequence>.jpg`.

**Existing criterion:** Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### JOURNALS

**Component:** 15 mm pivot journals / cheek plates

Wait for the local prototype and its reviewed drawing. Record fit/finish, engagement, shoulders, retention, installed stack/edge distances and the actual drawing revision together.

**Before starting:** BEARINGS. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-009-M01 | Journal fit/finish | mm; notes for condition/identity | `/components/8/measurements/0` |
| HF-009-M02 | engagement | mm plus observed condition/state | `/components/8/measurements/1` |
| HF-009-M03 | shoulder | mm; notes for condition/identity | `/components/8/measurements/2` |
| HF-009-M04 | axial retention | mm plus observed condition/state | `/components/8/measurements/3` |
| HF-009-M05 | plate-to-rail stack | mm; notes for condition/identity | `/components/8/measurements/4` |
| HF-009-M06 | bolt edge distances | mm; notes for condition/identity | `/components/8/measurements/5` |
| HF-009-M07 | shop drawing revision | text / instance IDs (grain also mark on sketch) | `/components/8/measurements/6` |

**Linked blockers:** CF-0090 (WOOD-CRADLEPIVOTDOUBLERLEFT-R1), CF-0093 (WOOD-CRADLEPIVOTDOUBLERRIGHT-R1), CF-0096 (WOOD-CRADLEREARBEAM-R1)

**Evidence:** identity, shoulder, installed-stack Naming: `PV27_S04_JOURNALS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### PROPS-BARE

**Component:** Two captive steel prop rods with clevises/pins/keepers/stow clips

One setup per handed set: rod ends/length, clevis/receiver patterns, pin/keeper engagement and stow clips. Keep left/right readings separate. Do not test capacity here.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Both rods and all lower/upper/stow hardware, separately labeled.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-010-M01 | Rod pin-to-pin length | mm; notes for condition/identity | `/components/9/measurements/0` |
| HF-010-M02 | section and end-eye geometry | mm; notes for condition/identity | `/components/9/measurements/1` |
| HF-010-M03 | lower clevis and upper receiver outlines/offsets/patterns | mm; notes for condition/identity | `/components/9/measurements/2` |
| HF-010-M04 | pin diameter and positive keeper engagement | mm plus observed condition/state | `/components/9/measurements/3` |
| HF-010-M05 | stow-clip retention/pattern | mm plus observed condition/state | `/components/9/measurements/4` |

**Linked blockers:** CF-0007 (CAB-SIDE-001L-R1), CF-0016 (CAB-SIDE-001R-R1), CF-0076 (WOOD-CRADLESIDERAILLEFT-R1), CF-0080 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0099 (PF-LANDING-PROP-LEFT-R3), CF-0103 (PF-LANDING-PROP-RIGHT-R3)

**Evidence:** identity, mount-face, keeper-engaged, stow-clip Naming: `PV27_S04_PROPS-BARE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### LATCH-PADS

**Component:** Closed-position pads/latches

Record both latch patterns, grip/release envelope and pad footprint/loaded thickness. Use only the independently supported fixture described in the plan; if compression cannot be measured safely, leave it open for review.

**Before starting:** PROPS-BARE, JOURNALS, STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-012-M01 | Latch and catch holes | mm; notes for condition/identity | `/components/10/measurements/0` |
| HF-012-M02 | closed grip range | mm; notes for condition/identity | `/components/10/measurements/1` |
| HF-012-M03 | travel/release envelope | mm plus observed condition/state | `/components/10/measurements/2` |
| HF-012-M04 | pad footprint and loaded thickness | mm; notes for condition/identity | `/components/10/measurements/3` |
| HF-012-M05 | attachment geometry | mm; notes for condition/identity | `/components/10/measurements/4` |

**Linked blockers:** CF-0077 (WOOD-CRADLESIDERAILLEFT-R1), CF-0081 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0100 (PF-LANDING-PROP-LEFT-R3), CF-0104 (PF-LANDING-PROP-RIGHT-R3)

**Evidence:** closed, released, pad-stack Naming: `PV27_S04_LATCH-PADS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### PROP-MOTION

**Component:** Two captive steel prop rods with clevises/pins/keepers/stow clips

Use the reviewed full-width fixture and independent support; follow plan B. Check the complete continuous movement, both keepers, hand access and stow retention. No capacity test or work under an unproven assembly.

**Before starting:** PROPS-BARE, JOURNALS, LATCH-PADS, CONTROLS-HANDS. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewed supported fixture, actual hardware, ruler/feeler gauges and camera; independent support as specified in the plan. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-010-M06 | complete swing | deg and mm clearance; note state | `/components/9/measurements/5` |

**Trial PV-PROP-MOTION:** Both props deployment stow retention and accessibility. Record at `/physical_trials/3`; use the existing plan/procedure.

**Linked blockers:** CF-0007 (CAB-SIDE-001L-R1), CF-0016 (CAB-SIDE-001R-R1), CF-0076 (WOOD-CRADLESIDERAILLEFT-R1), CF-0080 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0099 (PF-LANDING-PROP-LEFT-R3), CF-0103 (PF-LANDING-PROP-RIGHT-R3)

**Evidence:** deployed, stowed, keeper-engaged, minimum-clearance Naming: `PV27_S04_PROP-MOTION_<view>_<sequence>.jpg`.

**Existing criterion:** No rubbing, trapped fingers, snag, keeper interference or weak-skin contact; positive pins/keepers required. Narrow-corridor tolerance budget still needs approval. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 5 — Electronics carriers and cable serviceability

- [ ] **MAINS-FIT** (A) — Measure the unpowered mains module and enclosure together
- [ ] **ETHERNET** (A) — Measure the optional network adapter, if selected
- [ ] **SSF-ADAPTER** (A) — Inspect exciter footprint and local cable clearance
- [ ] **SSF-REF** (A) — File the adapter attachment specification
- [ ] **TRAYS** (A) — Remove and reinstall each tray with representative cables
- [ ] **CENTRAL** (A) — Reach the central service area with cables installed

### MAINS-FIT

**Component:** Rear mains inlet/disconnect module; Touch-safe mains enclosure

Use the same identified enclosed assembly for both IDs; record module and enclosure dimensions separately. Keep it unplugged. Capture mount pattern, strain relief, cord bend, lid/disconnect and service access without exposing or energizing mains.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-017-M01 | Panel cutout | mm; notes for condition/identity | `/components/15/measurements/0` |
| HF-017-M02 | fixing holes | mm; notes for condition/identity | `/components/15/measurements/1` |
| HF-017-M03 | total depth | mm; notes for condition/identity | `/components/15/measurements/2` |
| HF-017-M04 | plug/cord bend space | mm; notes for condition/identity | `/components/15/measurements/3` |
| HF-017-M05 | disconnect travel | mm; notes for condition/identity | `/components/15/measurements/4` |
| HF-017-M06 | strain-relief footprint | mm; notes for condition/identity | `/components/15/measurements/5` |
| HF-017-M07 | mounting stack | mm; notes for condition/identity | `/components/15/measurements/6` |
| HF-027-M01 | External bounds including mounts | mm; notes for condition/identity | `/components/25/measurements/0` |
| HF-027-M02 | lid screw/service clearance | mm; notes for condition/identity | `/components/25/measurements/1` |
| HF-027-M03 | cable gland projection | mm; notes for condition/identity | `/components/25/measurements/2` |
| HF-027-M04 | mounting hole pattern | mm; notes for condition/identity | `/components/25/measurements/3` |
| HF-027-M05 | protected entry | mm plus observed condition/state | `/components/25/measurements/4` |

**Linked blockers:** CF-0033 (CAB-REAR-001-R3), CF-0034 (CAB-REAR-001-R3)

**Evidence:** identity, mount-face, cord-clearance, lid-access Naming: `PV27_S05_MAINS-FIT_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### ETHERNET

**Component:** Optional Ethernet RJ45 carrier or blank

WAIT unless the optional adapter is available. Record coupling aperture, retention and bend radius on its removable carrier. A blank option is not permission to invent an RJ45 measurement.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-018-M01 | Coupler/keystone aperture | mm; notes for condition/identity | `/components/16/measurements/0` |
| HF-018-M02 | clip retention | mm plus observed condition/state | `/components/16/measurements/1` |
| HF-018-M03 | bend radius | mm; notes for condition/identity | `/components/16/measurements/2` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, installed Naming: `PV27_S05_ETHERNET_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SSF-ADAPTER

**Component:** Four exciters and local attachment adapters

WAIT for later selected exciters. Keep the four solid zones intact; record adapter footprint, projection and cable/service clearance. Do not cut speaker holes.

**Before starting:** CONTROLS-HANDS. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Four locations; every different device/adapter type, with location IDs.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-031-M01 | Attachment footprint | mm; notes for condition/identity | `/components/29/measurements/0` |
| HF-031-M03 | projection | mm; notes for condition/identity | `/components/29/measurements/2` |
| HF-031-M04 | cable bend and service clearance | mm; notes for condition/identity | `/components/29/measurements/3` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, installed, rear-clearance Naming: `PV27_S05_SSF-ADAPTER_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SSF-REF

**Component:** Four exciters and local attachment adapters

Save the actual adapter screw/adhesive specification revision as supplemental reference. A specification is not a measured dimension; measured_value remains null pending review.

**Before starting:** SSF-ADAPTER. **Hold:** REFERENCE_ONLY.

**Instrument:** Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings. **Samples/repeats:** Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-031-M02 | adapter screw or adhesive specification | reference document / maker-stated units; NOT a measured value | `/components/29/measurements/1` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S05_SSF-REF_<view>_<sequence>.jpg`.

**Existing criterion:** Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### TRAYS

**Component:** Remove and reinstall each tray with representative cables

Use the two existing candidate trays, ordinary fasteners and representative low-voltage bundles/connector bodies. Follow plan E SV-01; record missing cable/device details. The plan's payload envelope is a requirement, not a newly authorized proof test.

**Before starting:** MAINS-FIT, STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial SV-01:** Each electronics carrier with cabling. Record at `/physical_trials/7`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** installed, extraction, cabling, tool-access Naming: `PV27_S05_TRAYS_<view>_<sequence>.jpg`.

**Existing criterion:** Each tray independently removable/reinstalled with ordinary tools; no glue, cable pulling or entry into mains enclosure. Fasteners accessible/captive, strain relief and labels; record extraction direction/slack. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CENTRAL

**Component:** Reach the central service area with cables installed

Use the same installed cables; avoid another fixture setup. Try the intended service tasks with hand tools and record the path, not only an empty-box clearance.

**Before starting:** TRAYS. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial SV-02:** Central service path. Record at `/physical_trials/8`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** service-path, cabling Naming: `PV27_S05_CENTRAL_<view>_<sequence>.jpg`.

**Existing criterion:** Service work possible without removing permanent structure; cable bundles cannot fill the reserved access volume. No new minimum gap is defined. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 6 — CPU access

- [ ] **CPU-CASE** (A) — Measure the already-owned open case
- [ ] **SLIDES-BARE** (A) — Measure the two slide members and travel
- [ ] **SLIDE-REF** (A) — File maker clearance and rating conditions
- [ ] **CLAMPS** (A) — Measure four clamps, backing and the retainer
- [ ] **CPU-HINGE** (A) — Measure both leaves of the CPU door hinge
- [ ] **CPU-LATCH** (A) — Measure latch, catch, gasket and tool access
- [ ] **REAR-STACK** (A) — Measure the installed rear-corner stack once
- [ ] **CPU-QUALIFY** (B) — Review CPU removal, then perform only approved CPU proof

### CPU-CASE

**Component:** Open PC case

Use the actual case; measure foot/mount/standoff stack and connector/GPU restraint access on the single replaceable board.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-014-M01 | Mounting hole centers/diameters | mm; notes for condition/identity | `/components/12/measurements/0` |
| HF-014-M02 | foot heights | mm; notes for condition/identity | `/components/12/measurements/1` |
| HF-014-M03 | standoff stack | mm; notes for condition/identity | `/components/12/measurements/2` |
| HF-014-M04 | connector and GPU restraint access | mm plus observed condition/state | `/components/12/measurements/3` |

**Linked blockers:** CF-0112 (PC-REAR-SHELF-002-R1)

**Evidence:** identity, underside, connector-access Naming: `PV27_S06_CPU-CASE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SLIDES-BARE

**Component:** Rear CPU full-extension slide pair

Identify fixed and moving members separately, left and right. Record patterns, stops, travel, disconnect and actual screw-head space from one member layout. Do not infer maker minimum clearance from these dimensions.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Both slides; fixed and moving members separately.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-013-M01 | Body thickness each side | mm; notes for condition/identity | `/components/11/measurements/0` |
| HF-013-M03 | fixed/moving member outlines | mm; notes for condition/identity | `/components/11/measurements/2` |
| HF-013-M04 | hole and slot centers separately | mm; notes for condition/identity | `/components/11/measurements/3` |
| HF-013-M05 | travel | mm; notes for condition/identity | `/components/11/measurements/4` |
| HF-013-M06 | disconnect access | mm plus observed condition/state | `/components/11/measurements/5` |
| HF-013-M07 | closed stop position | mm; notes for condition/identity | `/components/11/measurements/6` |
| HF-013-M08 | screw-head limits | mm; notes for condition/identity | `/components/11/measurements/7` |

**Linked blockers:** CF-0111 (PC-REAR-SHELF-002-R1), CF-0116 (PC-SUPPORT-LEFT-R2), CF-0121 (PC-SUPPORT-RIGHT-R2)

**Evidence:** identity, fixed-member, moving-member, closed, extended Naming: `PV27_S06_SLIDES-BARE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SLIDE-REF

**Component:** Rear CPU full-extension slide pair

Save maker min/max side clearance and rating orientation/conditions with document revision. These remain reference data; actual installed clearances are collected in REAR-STACK. Leave measured_value null on reference-only entries.

**Before starting:** SLIDES-BARE. **Hold:** REFERENCE_ONLY.

**Instrument:** Maker or approved adapter document with part number/revision; no measuring instrument or inferred readings. **Samples/repeats:** Document revision for each distinct delivered part/adapter; no physical reading or repeated measurement.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-013-M02 | maker minimum/maximum side clearance | reference document / maker-stated units; NOT a measured value | `/components/11/measurements/1` |
| HF-013-M09 | rating conditions | reference document / maker-stated units; NOT a measured value | `/components/11/measurements/8` |

**Linked blockers:** CF-0111 (PC-REAR-SHELF-002-R1), CF-0116 (PC-SUPPORT-LEFT-R2), CF-0121 (PC-SUPPORT-RIGHT-R2)

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S06_SLIDE-REF_<view>_<sequence>.jpg`.

**Existing criterion:** Reference only; cannot supply a physical measured_value or pass a fit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CLAMPS

**Component:** Four identical CPU rail angle clamps + backing + retainer

One labeled set-up per clamp: legs/bend, holes, backing and bolt stack. Record bolt markings as identification, not a measured strength. Record retainer movement and tool access.

**Before starting:** SLIDES-BARE. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** All four clamps/backing sets and the stowed retainer.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-026-M01 | Both angle legs/length/thickness | deg and mm clearance; note state | `/components/24/measurements/0` |
| HF-026-M02 | bend radius | mm; notes for condition/identity | `/components/24/measurements/1` |
| HF-026-M03 | all holes | mm; notes for condition/identity | `/components/24/measurements/2` |
| HF-026-M04 | backing thickness/area/pattern | mm; notes for condition/identity | `/components/24/measurements/3` |
| HF-026-M05 | bolt grade/diameter/stack | mm; notes for condition/identity | `/components/24/measurements/4` |
| HF-026-M06 | retainer stroke/holes/access | mm plus observed condition/state | `/components/24/measurements/5` |

**Linked blockers:** CF-0037 (CAB-BOTTOM-001-R1), CF-0113 (PC-REAR-SHELF-002-R1), CF-0117 (PC-SUPPORT-LEFT-R2), CF-0122 (PC-SUPPORT-RIGHT-R2)

**Evidence:** identity, mount-face, bolt-stack, retainer Naming: `PV27_S06_CLAMPS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CPU-HINGE

**Component:** Rear CPU hatch hinge

Measure both leaves from hinge end, seating face and axis; include folded stack and possible opening angle.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-015-M01 | Leaf widths/thickness | mm; notes for condition/identity | `/components/13/measurements/0` |
| HF-015-M02 | knuckle diameter | mm; notes for condition/identity | `/components/13/measurements/1` |
| HF-015-M03 | axis-to-leaf offsets | mm; notes for condition/identity | `/components/13/measurements/2` |
| HF-015-M04 | hole centers/diameters | mm; notes for condition/identity | `/components/13/measurements/3` |
| HF-015-M05 | screw heads | mm; notes for condition/identity | `/components/13/measurements/4` |
| HF-015-M06 | folded stack | mm; notes for condition/identity | `/components/13/measurements/5` |
| HF-015-M07 | available opening angle | deg and mm clearance; note state | `/components/13/measurements/6` |

**Linked blockers:** CF-0031 (CAB-REAR-001-R3), CF-0107 (CAB-PC-REAR-DOOR-002-R1)

**Evidence:** identity, mount-face, folded, open Naming: `PV27_S06_CPU-HINGE_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CPU-LATCH

**Component:** Rear CPU hatch latch

Use the CPU door mockup to record body cutout/flats, fixing/catch, grip and compressed gasket. Keep any shared backbox-family parts separately identified.

**Before starting:** CPU-HINGE. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-016-M01 | Body cutout | mm; notes for condition/identity | `/components/14/measurements/0` |
| HF-016-M02 | antirotation flat | mm; notes for condition/identity | `/components/14/measurements/1` |
| HF-016-M03 | fixing holes | mm; notes for condition/identity | `/components/14/measurements/2` |
| HF-016-M04 | cam reach | mm; notes for condition/identity | `/components/14/measurements/3` |
| HF-016-M05 | grip range | mm; notes for condition/identity | `/components/14/measurements/4` |
| HF-016-M06 | catch geometry | mm; notes for condition/identity | `/components/14/measurements/5` |
| HF-016-M07 | key/tool clearance | mm; notes for condition/identity | `/components/14/measurements/6` |
| HF-016-M08 | compressed gasket thickness | mm; notes for condition/identity | `/components/14/measurements/7` |

**Linked blockers:** CF-0032 (CAB-REAR-001-R3), CF-0108 (CAB-PC-REAR-DOOR-002-R1)

**Evidence:** mount-face, latched, gasket-stack, tool-access Naming: `PV27_S06_CPU-LATCH_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### REAR-STACK

**Component:** Compact internal leg brackets/backing; Rear bracket to CPU rail planning reserve

In the measured-stock corner fixture, record both rear corners including all bolts/nuts/washers. Reuse the same Y/Z and access observations for HF-004 and HF-028, keeping each ledger entry separate. Preserve signed coordinates and the actual narrowest gap/state.

**Before starting:** BRACKET-BARE, CLAMPS, CPU-CASE, CPU-LATCH, STOCK-THICK. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Both rear corners and all relevant slide positions.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-004-M02 | inner X at rear left/right when seated | mm; notes for condition/identity | `/components/3/measurements/1` |
| HF-004-M03 | full Y/Z extent | mm; notes for condition/identity | `/components/3/measurements/2` |
| HF-004-M06 | wrench access | mm plus observed condition/state | `/components/3/measurements/5` |
| HF-028-M01 | Minimum actual rail-to-bracket gap including flange/bolt/nut/washer | mm; notes for condition/identity | `/components/26/measurements/0` |
| HF-028-M02 | bracket Y/Z extent | mm; notes for condition/identity | `/components/26/measurements/1` |
| HF-028-M03 | slide side clearance | mm; notes for condition/identity | `/components/26/measurements/2` |
| HF-028-M04 | clamp/backing bounds at both rear corners | mm; notes for condition/identity | `/components/26/measurements/3` |

**Linked blockers:** CF-0004 (CAB-SIDE-001L-R1), CF-0013 (CAB-SIDE-001R-R1), CF-0022 (CAB-FRONT-001-R1), CF-0030 (CAB-REAR-001-R3), CF-0118 (PC-SUPPORT-LEFT-R2), CF-0123 (PC-SUPPORT-RIGHT-R2)

**Evidence:** installed, bolt-stack, minimum-clearance, tool-access Naming: `PV27_S06_REAR-STACK_<view>_<sequence>.jpg`.

**Existing criterion:** Compare to the existing planning reserve; a nominal or positive gap alone does not release the stack. Actual clearance/fastener/load review remains required. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### CPU-QUALIFY

**Component:** Rear CPU full-extension slide pair; Open PC case; Rear CPU hatch hinge; Rear CPU hatch latch; Four identical CPU rail angle clamps + backing + retainer; Rear bracket to CPU rail planning reserve

SV-03 combines service and load evidence. First document unpowered removal/retainer/cables. The load portion must WAIT for fixture/fastener review; follow the existing hardware-pack CPU protocol unchanged. Keep service-only success distinct from final trial PASS.

**Before starting:** REAR-STACK, CENTRAL. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial SV-03:** CPU service path and20kg payload proof. Record at `/physical_trials/9`; use the existing plan/procedure.

**Linked blockers:** CF-0031 (CAB-REAR-001-R3), CF-0032 (CAB-REAR-001-R3), CF-0037 (CAB-BOTTOM-001-R1), CF-0107 (CAB-PC-REAR-DOOR-002-R1), CF-0108 (CAB-PC-REAR-DOOR-002-R1), CF-0111 (PC-REAR-SHELF-002-R1), CF-0112 (PC-REAR-SHELF-002-R1), CF-0113 (PC-REAR-SHELF-002-R1), CF-0116 (PC-SUPPORT-LEFT-R2), CF-0117 (PC-SUPPORT-LEFT-R2), CF-0118 (PC-SUPPORT-LEFT-R2), CF-0121 (PC-SUPPORT-RIGHT-R2), CF-0122 (PC-SUPPORT-RIGHT-R2), CF-0123 (PC-SUPPORT-RIGHT-R2)

**Evidence:** closed, extended, removal-path, cabling, approved-load, deflection Naming: `PV27_S06_CPU-QUALIFY_<view>_<sequence>.jpg`.

**Existing criterion:** Plan E SV-03 and hardware-pack CPU proof criteria apply. Existing numerical targets are proposed prototype targets requiring review, not a new certified rating. [Source](../docs/HARDWARE_MEASUREMENT_PACK_V25.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 7 — Backbox / monitor access

- [ ] **BB-HINGES** (A) — Measure the paired backbox hinges and pivots
- [ ] **BB-LOCKS** (B) — Measure upright locks in the supported hinge fixture
- [ ] **BB-DOOR** (A) — Measure and service the rear door
- [ ] **BB-MONITOR** (A) — Measure the later selected backglass on the bench
- [ ] **BB-SPEAKERS** (A) — Measure later speaker modules and baffles together
- [ ] **BB-REMOVE** (A) — Rehearse full monitor replacement through the front

### BB-HINGES

**Component:** WPC 01-9011-L/R hinge pair + 02-4352 + pivot bolts

Use one datum sketch per leaf/handed assembly; include bushings, shoulder/thread and differences. Do not assume the two sides match.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Both hinge assemblies; both leaves and mating pivot parts.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-006-M01 | Hole and slot centers | mm; notes for condition/identity | `/components/5/measurements/0` |
| HF-006-M02 | hole diameters | mm; notes for condition/identity | `/components/5/measurements/1` |
| HF-006-M03 | leaf outline/thickness | mm; notes for condition/identity | `/components/5/measurements/2` |
| HF-006-M04 | bend offsets | mm; notes for condition/identity | `/components/5/measurements/3` |
| HF-006-M05 | pivot center to both mounting faces | mm; notes for condition/identity | `/components/5/measurements/4` |
| HF-006-M06 | bushing OD/ID/flange/length | mm; notes for condition/identity | `/components/5/measurements/5` |
| HF-006-M07 | bolt shoulder and thread | mm; notes for condition/identity | `/components/5/measurements/6` |
| HF-006-M09 | left/right differences | mm; notes for condition/identity | `/components/5/measurements/8` |

**Linked blockers:** CF-0005 (CAB-SIDE-001L-R1), CF-0014 (CAB-SIDE-001R-R1), CF-0049 (BB-FLOOR-001-R1), CF-0055 (BB-SIDE-001L-R1), CF-0058 (BB-SIDE-001R-R1)

**Evidence:** identity, mount-face, pivot-stack Naming: `PV27_S07_BB-HINGES_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BB-LOCKS

**Component:** WPC 01-9011-L/R hinge pair + 02-4352 + pivot bolts; Upright backbox lock bolts/captive threads

Use the supported fixture described by the source plan/pack. Collect folded/upright sweep and installed lock X/Y/engagement in the same set-up. Do not support an unproven backbox by its locks while measuring.

**Before starting:** BB-HINGES, STOCK-THICK. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewed supported fixture, actual hardware, ruler/feeler gauges and camera; independent support as specified in the plan. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-006-M08 | full folded/upright sweep | deg and mm clearance; note state | `/components/5/measurements/7` |
| HF-007-M01 | Thread | mm; notes for condition/identity | `/components/6/measurements/0` |
| HF-007-M02 | grip length | mm; notes for condition/identity | `/components/6/measurements/1` |
| HF-007-M03 | head/tool envelope | mm; notes for condition/identity | `/components/6/measurements/2` |
| HF-007-M04 | captive plate hole pattern | mm; notes for condition/identity | `/components/6/measurements/3` |
| HF-007-M05 | engagement | mm plus observed condition/state | `/components/6/measurements/4` |
| HF-007-M06 | shelf/floor/gasket stack | mm; notes for condition/identity | `/components/6/measurements/5` |
| HF-007-M07 | X and Y after hinge fixture | mm; notes for condition/identity | `/components/6/measurements/6` |

**Linked blockers:** CF-0005 (CAB-SIDE-001L-R1), CF-0014 (CAB-SIDE-001R-R1), CF-0046 (CAB-REAR-SHELF-001-R1), CF-0049 (BB-FLOOR-001-R1), CF-0050 (BB-FLOOR-001-R1), CF-0055 (BB-SIDE-001L-R1), CF-0058 (BB-SIDE-001R-R1)

**Evidence:** folded, upright, lock-engaged, tool-access Naming: `PV27_S07_BB-LOCKS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BB-DOOR

**Component:** Backbox service door hinge/lock/gasket

Identify the actual hinge/latch/gasket set separately from CPU hardware even if the family matches. Record door sweep and access to wiring, DMD, speakers, lighting and fixed fans.

**Before starting:** BB-LOCKS. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-029-M01 | Hinge leaves/axis/holes | mm; notes for condition/identity | `/components/27/measurements/0` |
| HF-029-M02 | lock body/catch/cutout | mm; notes for condition/identity | `/components/27/measurements/1` |
| HF-029-M03 | gasket compressed thickness | mm; notes for condition/identity | `/components/27/measurements/2` |
| HF-029-M04 | door clearance and opening sweep | deg and mm clearance; note state | `/components/27/measurements/3` |

**Trial SV-04:** Backbox rear door servicing. Record at `/physical_trials/10`; use the existing plan/procedure.

**Linked blockers:** CF-0061 (BB-REAR-FRAME-L-R1), CF-0064 (BB-REAR-FRAME-R-R1), CF-0067 (BB-REAR-FRAME-B-R1), CF-0070 (BB-REAR-FRAME-T-R1), CF-0073 (BB-DOOR-001-R1)

**Evidence:** closed, open, gasket-stack, service-access Naming: `PV27_S07_BB-DOOR_<view>_<sequence>.jpg`.

**Existing criterion:** Outward operation/retention without rubbing; service access demonstrated. Door is not primary shear structure; no moving fan wiring required. Actual hinge and gasket fit still reviewed. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BB-MONITOR

**Component:** Backglass monitor

WAIT for the actual monitor. Record VESA, bezel, connectors and mass; do not copy catalogue mass. Use safe supported handling/assistance; defer weighing if it cannot be done safely.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. Use a suitable scale for actual mass, with stable support/assistance. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-025-M01 | VESA | mm; notes for condition/identity | `/components/23/measurements/0` |
| HF-025-M02 | bezel | mm; notes for condition/identity | `/components/23/measurements/1` |
| HF-025-M03 | connector space | mm; notes for condition/identity | `/components/23/measurements/2` |
| HF-025-M04 | mass | kg | `/components/23/measurements/3` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, rear, connector-access, scale-reading Naming: `PV27_S07_BB-MONITOR_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BB-SPEAKERS

**Component:** Backbox conventional speaker modules

WAIT for selected modules. Measure driver pattern, magnet/connectors, baffle and rail attachment; keep these operations on replaceable modules.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-033-M01 | Driver cutout | mm; notes for condition/identity | `/components/31/measurements/0` |
| HF-033-M02 | screw pattern | mm; notes for condition/identity | `/components/31/measurements/1` |
| HF-033-M03 | rear magnet/connector depth | mm; notes for condition/identity | `/components/31/measurements/2` |
| HF-033-M04 | baffle thickness | mm; notes for condition/identity | `/components/31/measurements/3` |
| HF-033-M05 | rail-cage adapter attachment | mm; notes for condition/identity | `/components/31/measurements/4` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, mount-face, rear-clearance Naming: `PV27_S07_BB-SPEAKERS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### BB-REMOVE

**Component:** Backglass monitor

First use the full-envelope dummy, with supported handling/assistance. Record bezel/mount release, plugs, grips, extraction and reinstallation. BB-MONITOR provides later actual-device evidence; without it the trial remains OPEN for actual mass/connector/grip checks. Do not attempt to pass the full monitor flat through the rear door.

**Before starting:** BB-DOOR. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial SV-05:** Full monitor front replacement. Record at `/physical_trials/11`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** bezel-off, mount-release, front-extraction, cabling Naming: `PV27_S07_BB-REMOVE_<view>_<sequence>.jpg`.

**Existing criterion:** Front removal/reinstallation demonstrated with safe access, tools and assistance; dummy is envelope-only, not final actual-monitor acceptance. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 8 — Filter and airflow path

- [ ] **FILTER** (A) — Inspect the later filter cassette/media and removal route
- [ ] **FANS** (A) — Measure later fans, guards and removable adapters

### FILTER

**Component:** Dust-filter media and optional intake/exhaust fans

Check actual slot coupon/fixture, row webs and clear passage route against plan F; do not take dimensions from pictures. Trial external filter removal and retention. Leave final media/pressure-drop or missing hardware checks OPEN.

**Before starting:** STOCK-SURVEY. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Actual labeled samples, sacrificial mockup, ordinary hand tools, ruler/caliper, representative cables and camera; no powered mains. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-032-M01 | Filter compression and service clearance | mm; notes for condition/identity | `/components/30/measurements/0` |

**Trial PV-AIRFLOW:** Slots filter passages packaging. Record at `/physical_trials/12`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** slots, filter-installed, filter-removal, passage-obstruction Naming: `PV27_S08_FILTER_<view>_<sequence>.jpg`.

**Existing criterion:** Use existing plan F packaging dimensions/screens; no thermal adequacy from slot area. Do not trim structural wood to fit a fan. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### FANS

**Component:** Dust-filter media and optional intake/exhaust fans

WAIT for selected fans/guards. Measure thickness and pattern on replaceable adapters; maker performance data is supplemental reference only.

**Before starting:** FILTER. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-032-M02 | fan thickness | mm; notes for condition/identity | `/components/30/measurements/1` |
| HF-032-M03 | grille/finger guard | mm; notes for condition/identity | `/components/30/measurements/2` |
| HF-032-M04 | fan pattern on adapter only | mm; notes for condition/identity | `/components/30/measurements/3` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, adapter-face, rear-clearance Naming: `PV27_S08_FANS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 9 — Moving assembly mass and lift effort

- [ ] **PF-DISPLAY** (A) — Measure later playfield adapter and connector fit
- [ ] **MOVING-MASS** (A) — Weigh and reconcile the actual moving assembly
- [ ] **LIFT** (B) — Record lift effort and the owner's controlled descent trial

### PF-DISPLAY

**Component:** Playfield 42/43 inch display

WAIT for the actual display; measure its adapter pattern and connectors. Keep physical support stable; do not buy a display to close a shell hole.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-024-M01 | VESA | mm; notes for condition/identity | `/components/22/measurements/0` |
| HF-024-M02 | connector access | mm plus observed condition/state | `/components/22/measurements/1` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** identity, rear, connector-access Naming: `PV27_S09_PF-DISPLAY_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### MOVING-MASS

**Component:** Playfield 42/43 inch display

Weigh supported components and, if safely possible, the completed moving assembly. List included/excluded moving hardware and cable portions; reconcile the sum. A ballast mockup is provisional and leaves actual mass OPEN.

**Before starting:** PF-DISPLAY. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Suitable scale with recorded uncertainty and stable supports/assistance; no unsafe balancing. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-MASS:** Actual completed moving mass. Record at `/physical_trials/4`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** scale-reading, assembly-identity Naming: `PV27_S09_MOVING-MASS_<view>_<sequence>.jpg`.

**Existing criterion:** Actual included mass, identity and scale uncertainty documented; the preliminary mass is not a reading. No new mass acceptance limit. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### LIFT

**Component:** Playfield 42/43 inch display

WAIT for the approved fixture and independent backup support. Reuse MOVING-MASS results in the composite M03 entry; do not weigh twice. Record grip/direction/angle and opening/lowering/breakaway force. The observed force, not the prediction, goes on the sheet.

**Before starting:** MOVING-MASS, PROP-MOTION. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Force gauge, angle measurement, approved fixture and independent backup; actual intended grip. **Samples/repeats:** Three slow cycles; closed then 10-degree increments and all local peaks through service, as in plan C.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-024-M03 | completed moving mass and manual lifting force at the front grip | kg and N; grip coordinates mm; angle deg | `/components/22/measurements/2` |

**Trial PV-ERGONOMICS:** Measured lift effort and owner opening/closing acceptance. Record at `/physical_trials/5`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** grip, gauge-reading, keeper-reach, controlled-descent Naming: `PV27_S09_LIFT_<view>_<sequence>.jpg`.

**Existing criterion:** Owner must accept comfortable, controllable opening/holding/prop operation/closing plus reviewed force data. Predicted ~86 N is not an acceptance threshold. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 10 — Reviewed proof testing

- [ ] **PROP-LEFT** (B) — LEFT prop independent full-load proof
- [ ] **PROP-RIGHT** (B) — RIGHT prop proof and reconcile the pair's capacity evidence
- [ ] **LOADS** (B) — Obtain the remaining reviewed structural load qualifications
- [ ] **SKATES** (B) — Later mobility engagement/stability check

### PROP-LEFT

**Component:** Two captive steel prop rods with clevises/pins/keepers/stow clips

STOP until the mechanical reviewer has approved the fixture, load/distribution, angle, catch, limits and procedure in plan B. Execute the existing LEFT protocol unchanged, with the opposite prop unable to share load. No person under the unproven assembly.

**Before starting:** PROP-MOTION, MOVING-MASS. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-PROP-L:** LEFT independent full-load qualification. Record at `/physical_trials/1`; use the existing plan/procedure.

**Linked blockers:** CF-0007 (CAB-SIDE-001L-R1), CF-0016 (CAB-SIDE-001R-R1), CF-0076 (WOOD-CRADLESIDERAILLEFT-R1), CF-0080 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0099 (PF-LANDING-PROP-LEFT-R3), CF-0103 (PF-LANDING-PROP-RIGHT-R3)

**Evidence:** fixture, opposite-prop-disengaged, approved-load, deflection, keeper, after-unload Naming: `PV27_S10_PROP-LEFT_<view>_<sequence>.jpg`.

**Existing criterion:** Only reviewed plan B qualification applies. Proposed residual-set screen does not supply the still-missing loaded-deflection limit. No unreviewed PASS. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### PROP-RIGHT

**Component:** Two captive steel prop rods with clevises/pins/keepers/stow clips

Run the independent RIGHT protocol, then reconcile both reviewed reports for M07. Reuse LEFT evidence; M07 must cover both sides, never infer a generic capacity from rod diameter. Follow the source plan's post-proof settling/engagement checks.

**Before starting:** PROP-LEFT. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-010-M07 | one-prop load capacity | reviewed test report; units from approved procedure | `/components/9/measurements/6` |

**Trial PV-PROP-R:** RIGHT independent full-load qualification. Record at `/physical_trials/2`; use the existing plan/procedure.

**Linked blockers:** CF-0007 (CAB-SIDE-001L-R1), CF-0016 (CAB-SIDE-001R-R1), CF-0076 (WOOD-CRADLESIDERAILLEFT-R1), CF-0080 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0099 (PF-LANDING-PROP-LEFT-R3), CF-0103 (PF-LANDING-PROP-RIGHT-R3)

**Evidence:** fixture, opposite-prop-disengaged, approved-load, deflection, keeper, after-unload Naming: `PV27_S10_PROP-RIGHT_<view>_<sequence>.jpg`.

**Existing criterion:** Both independent proofs and qualification scope must be reviewed. A single-side pass or static hold alone cannot establish the whole qualification. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### LOADS

**Component:** Classic pinball leg set; Compact internal leg brackets/backing; WPC 01-9011-L/R hinge pair + 02-4352 + pivot bolts; Upright backbox lock bolts/captive threads; UCFL202 15 mm flange bearing pair; 15 mm pivot journals / cheek plates; 600 mm lockdown bar + receiver

WAIT for reviewed leg/backbox/pivot/lockdown fixtures and criteria. Record lockdown loaded deflection under its approved case alongside the other qualification reports; no load or safety factor is defined by this checklist.

**Before starting:** LEGS-BARE, BRACKET-BARE, JOURNALS, BB-LOCKS, LOCKDOWN-FIT. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-022-M06 | loaded deflection | mm; notes for condition/identity | `/components/20/measurements/5` |

**Trial PV-LOADS:** Leg backbox pivot lockdown load qualification. Record at `/physical_trials/15`; use the existing plan/procedure.

**Linked blockers:** CF-0003 (CAB-SIDE-001L-R1), CF-0004 (CAB-SIDE-001L-R1), CF-0005 (CAB-SIDE-001L-R1), CF-0006 (CAB-SIDE-001L-R1), CF-0012 (CAB-SIDE-001R-R1), CF-0013 (CAB-SIDE-001R-R1), CF-0014 (CAB-SIDE-001R-R1), CF-0015 (CAB-SIDE-001R-R1), CF-0021 (CAB-FRONT-001-R1), CF-0022 (CAB-FRONT-001-R1), CF-0025 (CAB-FRONT-001-R1), CF-0029 (CAB-REAR-001-R3), CF-0030 (CAB-REAR-001-R3), CF-0046 (CAB-REAR-SHELF-001-R1), CF-0049 (BB-FLOOR-001-R1), CF-0050 (BB-FLOOR-001-R1), CF-0055 (BB-SIDE-001L-R1), CF-0058 (BB-SIDE-001R-R1), CF-0090 (WOOD-CRADLEPIVOTDOUBLERLEFT-R1), CF-0093 (WOOD-CRADLEPIVOTDOUBLERRIGHT-R1), CF-0096 (WOOD-CRADLEREARBEAM-R1)

**Evidence:** fixture, approved-load, deflection, after-unload Naming: `PV27_S10_LOADS_<view>_<sequence>.jpg`.

**Existing criterion:** Reviewed qualification scope, numerical criteria and evidence required by freeze Gate 1. Undefined tests remain OPEN. [Source](../docs/CNC_FREEZE_GATE_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### SKATES

**Component:** External removable PinSkates-style pair

WAIT; external skates are BUY LATER. Before mobility use obtain reviewed safe handling/load conditions and inspect physical leg engagement/stability. No cabinet lifting or rolling trial is authorized by this sheet alone.

**Before starting:** LOADS. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Reviewer-specified fixture, independent support/catch, approved loads and displacement instruments. Do not assemble a test from this tool list alone. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-005-M01 | Leg engagement and stability before mobility use | reviewed test report; units from approved procedure | `/components/4/measurements/0` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** engagement, setup Naming: `PV27_S10_SKATES_<view>_<sequence>.jpg`.

**Existing criterion:** Physical engagement/stability before mobility use as required by the measurement pack; no numerical mobility test criteria exist here. [Source](../docs/HARDWARE_MEASUREMENT_PACK_V25.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

## Session 11 — Final evidence reconciliation

- [ ] **GLASS** (A) — Later final supported glass-opening measurement
- [ ] **ELECTRICAL** (B) — Obtain protected electrical/cable/fold commissioning evidence
- [ ] **THERMAL** (B) — Defer thermal commissioning until reviewed conditions exist
- [ ] **RECONCILE** (A) — Return sheets and evidence without filling gaps from estimates
- [ ] **PACKAGE** (B) — Engineering/owner review of the eventual final CNC package

### GLASS

**Component:** Playfield tempered glass

WAIT until the supported rail/lockdown mockup is accepted. Record opening, engagement/expansion clearances and physical thickness sample. Use safe mock material for trials; final glass remains BUY LATER.

**Before starting:** RAIL-PROFILE, LOCKDOWN-FIT. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Digital caliper, depth rod, square and steel rule; suitable pin/bore gauges for fit-critical bores. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.

| Authoritative ID | Exact result to collect | Units | JSON location |
|---|---|---|---|
| HF-023-M01 | Finished supported opening | mm; notes for condition/identity | `/components/21/measurements/0` |
| HF-023-M02 | engagement and expansion clearances | mm plus observed condition/state | `/components/21/measurements/1` |
| HF-023-M03 | thickness sample | mm; notes for condition/identity | `/components/21/measurements/2` |

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** supported-opening, engagement, thickness-reading Naming: `PV27_S11_GLASS_<view>_<sequence>.jpg`.

**Existing criterion:** Record actual values with component datum and recording uncertainty; no standalone fit acceptance specified. Apply the existing physical plan and freeze gate. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### ELECTRICAL

**Component:** Rear mains inlet/disconnect module; Touch-safe mains enclosure

WAIT for the reviewed protected electrical design and competent commissioning. Ordinary bench measurements are unpowered; do not energize exposed mains to fill this result. Include cable segregation, strain relief, protected distribution and fold/service evidence.

**Before starting:** MAINS-FIT, BB-LOCKS, TRAYS, REAR-STACK. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Instruments and protected setup specified in the reviewed commissioning plan; none selected here. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-ELECTRICAL:** Protected electrical and cable/fold commissioning. Record at `/physical_trials/16`; use the existing plan/procedure.

**Linked blockers:** CF-0033 (CAB-REAR-001-R3), CF-0034 (CAB-REAR-001-R3)

**Evidence:** protected-assembly, cable-route, fold-clearance Naming: `PV27_S11_ELECTRICAL_<view>_<sequence>.jpg`.

**Existing criterion:** Existing source electrical/safety and freeze gates apply; no new electrical procedure or pass limit. [Source](../docs/CNC_FREEZE_GATE_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### THERMAL

**Component:** Dust-filter media and optional intake/exhaust fans

WAIT for final heat-producing equipment, protected electrical commissioning and an approved thermal plan. Log ambient/modes/load/filter state and temperatures as required by plan F. No new temperature limits are supplied here.

**Before starting:** FANS, ELECTRICAL. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Instruments and protected setup specified in the reviewed commissioning plan; none selected here. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-THERMAL:** Final thermal commissioning. Record at `/physical_trials/13`; use the existing plan/procedure.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** setup, sensor-position, filter-state Naming: `PV27_S11_THERMAL_<view>_<sequence>.jpg`.

**Existing criterion:** Limits must come from selected equipment and the reviewed commissioning plan. Slot area and CAD arrows cannot pass this trial. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### RECONCILE

**Component:** Return sheets and evidence without filling gaps from estimates

Use the queue to list completed, missing, reference-only and review-required operations. Return the actual sheets/photos even if later sessions remain OPEN. Transcribe by measurement/trial ID only; preserve repeats, units, uncertainty, failures and identity. Do not mark a whole component RECORDED until all its required measurements have real evidence.

**Before starting:** ARRIVAL. **Hold:** VERIFY_SAMPLE_AND_DEPENDENCIES.

**Instrument:** Pen, labels/masking tape, marker, blank sheets, phone/camera, ruler/square; available caliper/micrometer for identification and zero checks. **Samples/repeats:** One preparation/handoff record; no specimen repetitions.

Record preparation/handoff notes on paper; no authoritative result ID is invented for this housekeeping step.

**Linked blockers:** No hardware-controlled CF group; global process/service gate or preparation only.

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S11_RECONCILE_<view>_<sequence>.jpg`.

**Existing criterion:** No unknown, duplicated or omitted authoritative IDs; unperformed work remains blank/OPEN. This is evidence handoff, not geometry release. [Source](../docs/PHYSICAL_VALIDATION_PLAN_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

### PACKAGE

**Component:** Engineering/owner review of the eventual final CNC package

DEFER. The present task generates no geometry or production exports. When corresponding physical evidence exists, engineering must apply the existing gate to drawings, fasteners, laminate IDs, nesting/exports and owner manufacturing approval. Partial evidence is not a package PASS.

**Before starting:** RECONCILE, SHOP-COUPON, PROP-RIGHT, LOADS, CPU-QUALIFY, LIFT, BB-REMOVE, FILTER, ELECTRICAL, THERMAL. **Hold:** REVIEWED_CRITERIA_REQUIRED.

**Instrument:** Evidence records, original freeze gate and qualified reviewers; no physical operation authorized. **Samples/repeats:** Every actual installed instance/handed pair/type covered by the record; repeat to establish repeatability. No additional fixed count specified.


**Trial PV-CNC-PACKAGE:** Final drawings fasteners laminate IDs nesting export review owner approval. Record at `/physical_trials/17`; use the existing plan/procedure.

**Linked blockers:** CF-0003 (CAB-SIDE-001L-R1), CF-0004 (CAB-SIDE-001L-R1), CF-0005 (CAB-SIDE-001L-R1), CF-0006 (CAB-SIDE-001L-R1), CF-0007 (CAB-SIDE-001L-R1), CF-0008 (CAB-SIDE-001L-R1), CF-0009 (CAB-SIDE-001L-R1), CF-0012 (CAB-SIDE-001R-R1), CF-0013 (CAB-SIDE-001R-R1), CF-0014 (CAB-SIDE-001R-R1), CF-0015 (CAB-SIDE-001R-R1), CF-0016 (CAB-SIDE-001R-R1), CF-0017 (CAB-SIDE-001R-R1), CF-0018 (CAB-SIDE-001R-R1), CF-0021 (CAB-FRONT-001-R1), CF-0022 (CAB-FRONT-001-R1), CF-0023 (CAB-FRONT-001-R1), CF-0024 (CAB-FRONT-001-R1), CF-0025 (CAB-FRONT-001-R1), CF-0026 (CAB-FRONT-001-R1), CF-0029 (CAB-REAR-001-R3), CF-0030 (CAB-REAR-001-R3), CF-0031 (CAB-REAR-001-R3), CF-0032 (CAB-REAR-001-R3), CF-0033 (CAB-REAR-001-R3), CF-0034 (CAB-REAR-001-R3), CF-0037 (CAB-BOTTOM-001-R1), CF-0046 (CAB-REAR-SHELF-001-R1), CF-0049 (BB-FLOOR-001-R1), CF-0050 (BB-FLOOR-001-R1), CF-0055 (BB-SIDE-001L-R1), CF-0058 (BB-SIDE-001R-R1), CF-0061 (BB-REAR-FRAME-L-R1), CF-0064 (BB-REAR-FRAME-R-R1), CF-0067 (BB-REAR-FRAME-B-R1), CF-0070 (BB-REAR-FRAME-T-R1), CF-0073 (BB-DOOR-001-R1), CF-0076 (WOOD-CRADLESIDERAILLEFT-R1), CF-0077 (WOOD-CRADLESIDERAILLEFT-R1), CF-0080 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0081 (WOOD-CRADLESIDERAILRIGHT-R1), CF-0090 (WOOD-CRADLEPIVOTDOUBLERLEFT-R1), CF-0093 (WOOD-CRADLEPIVOTDOUBLERRIGHT-R1), CF-0096 (WOOD-CRADLEREARBEAM-R1), CF-0099 (PF-LANDING-PROP-LEFT-R3), CF-0100 (PF-LANDING-PROP-LEFT-R3), CF-0103 (PF-LANDING-PROP-RIGHT-R3), CF-0104 (PF-LANDING-PROP-RIGHT-R3), CF-0107 (CAB-PC-REAR-DOOR-002-R1), CF-0108 (CAB-PC-REAR-DOOR-002-R1), CF-0111 (PC-REAR-SHELF-002-R1), CF-0112 (PC-REAR-SHELF-002-R1), CF-0113 (PC-REAR-SHELF-002-R1), CF-0116 (PC-SUPPORT-LEFT-R2), CF-0117 (PC-SUPPORT-LEFT-R2), CF-0118 (PC-SUPPORT-LEFT-R2), CF-0121 (PC-SUPPORT-RIGHT-R2), CF-0122 (PC-SUPPORT-RIGHT-R2), CF-0123 (PC-SUPPORT-RIGHT-R2)

**Evidence:** Written notes/reference document only; no extra photo required. Naming: `PV27_S11_PACKAGE_<view>_<sequence>.jpg`.

**Existing criterion:** All three existing freeze gates; no release by checklist or queue status. [Source](../docs/CNC_FREEZE_GATE_V27.md).

**Geometry:** Evidence only. Never unlocks geometry automatically; original CNC_FREEZE_GATE_V27 Gates 1–3 remain unchanged.

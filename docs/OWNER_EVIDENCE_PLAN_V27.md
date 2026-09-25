# Owner evidence and photo plan — v27

Derived owner convenience copy. Authoritative values remain in [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). No measurements are filled; manufacturing stays **BLOCKED**. Regenerate with `python3 tools/generate_owner_execution_v27.py`; do not write bench results into generated files.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

Use `PV27_S<two-digit-session>_<operation-id>_<view>_<sequence>.jpg`, for example `PV27_S02_PLUNGER-FACE_mount-face_01.jpg`. Videos/raw sheets may use the same stem with their real extension. Sequence numbers increase within an operation/view; do not overwrite. Put sample ID/handed side and datum labels in frame or on the linked written sheet.

Keep files under a repository-relative evidence folder such as `evidence/physical-v27/S02/` when submitting. The queue prescribes names only; it creates no evidence files. Return photos plus raw written readings. A photograph of a ruler is supporting evidence, not an inferred precision measurement.

One full-component/label photo and one marked datum/mounting-face view can support many IDs from the same actual sample. Photograph representative critical readings, inaccessible offsets, tight clearance states, failures and assembly context. Do not require a photo of every routine caliper repeat or document revision. Keep reference PDFs/text in a REFERENCE subfolder with part/document revision; catalogue content never goes into measured values.

| View family | Capture when useful |
|---|---|
| identity / datum / mount-face | Full actual component, label and handed side; mounting plane and datum axes; orthogonal face and side for offsets. |
| reading / bore-reading / scale-reading / gauge-reading | Instrument display and contact location, sample ID; enough context to connect the reading to the sheet. Raw reading remains written separately. |
| rest / full-pull / inward-limit / rear-clearance | Plunger/button internals and cable/nut/tool clearance at actual limiting states. |
| deployed / stowed / keeper-engaged / stow-clip | Both prop positions, captive pins and positive keeper engagement; nearest obstacle. |
| installed / extraction / cabling / removal-path | Carrier/CPU installed state, removal sequence, connectors and representative bundles. |
| open / closed / front-extraction / bezel-off | Backbox rear service and actual front replacement route; distinguish dummy from final monitor. |
| slots / filter-removal / passage-obstruction | Actual bottom/coupon webs, external filter route and occupied airflow passages. |
| fixture / approved-load / deflection / after-unload | B tests only after review: fixture ID, approved case, gauges, opposite prop disengaged and residual condition. No person beneath an unproven load. |

## Operation-specific views

| Session / action | Views to retain or share | Filename stem |
|---|---|---|
| S00 / PREP | Written/reference evidence only; no extra photo | `PV27_S00_PREP_<view>_<sequence>` |
| S00 / ARRIVAL | identity | `PV27_S00_ARRIVAL_<view>_<sequence>` |
| S01 / STOCK-THICK | identity, datum, reading, point-map | `PV27_S01_STOCK-THICK_<view>_<sequence>` |
| S01 / STOCK-SURVEY | point-map, defect-if-present | `PV27_S01_STOCK-SURVEY_<view>_<sequence>` |
| S01 / SHOP-COUPON | identity, coupon, reading | `PV27_S01_SHOP-COUPON_<view>_<sequence>` |
| S02 / PLUNGER-FACE | identity, datum, mount-face, reading | `PV27_S02_PLUNGER-FACE_<view>_<sequence>` |
| S02 / PLUNGER-STROKE | rest, full-pull, inward-limit, rear-clearance, interference-if-present | `PV27_S02_PLUNGER-STROKE_<view>_<sequence>` |
| S02 / COIN-FACE | identity, mount-face, rear-clearance | `PV27_S02_COIN-FACE_<view>_<sequence>` |
| S02 / COIN-OPEN | closed, open, rear-clearance | `PV27_S02_COIN-OPEN_<view>_<sequence>` |
| S03 / BUTTON-FAMILY | identity, mount-face, rear-clearance, reading | `PV27_S03_BUTTON-FAMILY_<view>_<sequence>` |
| S03 / RAIL-PROFILE | identity, section, installed | `PV27_S03_RAIL-PROFILE_<view>_<sequence>` |
| S03 / LOCKDOWN-FIT | mount-face, latched, released, tool-access | `PV27_S03_LOCKDOWN-FIT_<view>_<sequence>` |
| S03 / CONTROLS-HANDS | hand-placement, rear-clearance, ssf-zones | `PV27_S03_CONTROLS-HANDS_<view>_<sequence>` |
| S04 / LEGS-BARE | identity, mount-face, reading | `PV27_S04_LEGS-BARE_<view>_<sequence>` |
| S04 / BRACKET-BARE | mount-face, bolt-stack, backing-contact | `PV27_S04_BRACKET-BARE_<view>_<sequence>` |
| S04 / BEARINGS | identity, mount-face, bore-reading, tool-access | `PV27_S04_BEARINGS_<view>_<sequence>` |
| S04 / BEARING-REF | Written/reference evidence only; no extra photo | `PV27_S04_BEARING-REF_<view>_<sequence>` |
| S04 / JOURNALS | identity, shoulder, installed-stack | `PV27_S04_JOURNALS_<view>_<sequence>` |
| S04 / PROPS-BARE | identity, mount-face, keeper-engaged, stow-clip | `PV27_S04_PROPS-BARE_<view>_<sequence>` |
| S04 / LATCH-PADS | closed, released, pad-stack | `PV27_S04_LATCH-PADS_<view>_<sequence>` |
| S04 / PROP-MOTION | deployed, stowed, keeper-engaged, minimum-clearance | `PV27_S04_PROP-MOTION_<view>_<sequence>` |
| S05 / MAINS-FIT | identity, mount-face, cord-clearance, lid-access | `PV27_S05_MAINS-FIT_<view>_<sequence>` |
| S05 / ETHERNET | identity, installed | `PV27_S05_ETHERNET_<view>_<sequence>` |
| S05 / SSF-ADAPTER | identity, installed, rear-clearance | `PV27_S05_SSF-ADAPTER_<view>_<sequence>` |
| S05 / SSF-REF | Written/reference evidence only; no extra photo | `PV27_S05_SSF-REF_<view>_<sequence>` |
| S05 / TRAYS | installed, extraction, cabling, tool-access | `PV27_S05_TRAYS_<view>_<sequence>` |
| S05 / CENTRAL | service-path, cabling | `PV27_S05_CENTRAL_<view>_<sequence>` |
| S06 / CPU-CASE | identity, underside, connector-access | `PV27_S06_CPU-CASE_<view>_<sequence>` |
| S06 / SLIDES-BARE | identity, fixed-member, moving-member, closed, extended | `PV27_S06_SLIDES-BARE_<view>_<sequence>` |
| S06 / SLIDE-REF | Written/reference evidence only; no extra photo | `PV27_S06_SLIDE-REF_<view>_<sequence>` |
| S06 / CLAMPS | identity, mount-face, bolt-stack, retainer | `PV27_S06_CLAMPS_<view>_<sequence>` |
| S06 / CPU-HINGE | identity, mount-face, folded, open | `PV27_S06_CPU-HINGE_<view>_<sequence>` |
| S06 / CPU-LATCH | mount-face, latched, gasket-stack, tool-access | `PV27_S06_CPU-LATCH_<view>_<sequence>` |
| S06 / REAR-STACK | installed, bolt-stack, minimum-clearance, tool-access | `PV27_S06_REAR-STACK_<view>_<sequence>` |
| S06 / CPU-QUALIFY | closed, extended, removal-path, cabling, approved-load, deflection | `PV27_S06_CPU-QUALIFY_<view>_<sequence>` |
| S07 / BB-HINGES | identity, mount-face, pivot-stack | `PV27_S07_BB-HINGES_<view>_<sequence>` |
| S07 / BB-LOCKS | folded, upright, lock-engaged, tool-access | `PV27_S07_BB-LOCKS_<view>_<sequence>` |
| S07 / BB-DOOR | closed, open, gasket-stack, service-access | `PV27_S07_BB-DOOR_<view>_<sequence>` |
| S07 / BB-MONITOR | identity, rear, connector-access, scale-reading | `PV27_S07_BB-MONITOR_<view>_<sequence>` |
| S07 / BB-SPEAKERS | identity, mount-face, rear-clearance | `PV27_S07_BB-SPEAKERS_<view>_<sequence>` |
| S07 / BB-REMOVE | bezel-off, mount-release, front-extraction, cabling | `PV27_S07_BB-REMOVE_<view>_<sequence>` |
| S08 / FILTER | slots, filter-installed, filter-removal, passage-obstruction | `PV27_S08_FILTER_<view>_<sequence>` |
| S08 / FANS | identity, adapter-face, rear-clearance | `PV27_S08_FANS_<view>_<sequence>` |
| S09 / PF-DISPLAY | identity, rear, connector-access | `PV27_S09_PF-DISPLAY_<view>_<sequence>` |
| S09 / MOVING-MASS | scale-reading, assembly-identity | `PV27_S09_MOVING-MASS_<view>_<sequence>` |
| S09 / LIFT | grip, gauge-reading, keeper-reach, controlled-descent | `PV27_S09_LIFT_<view>_<sequence>` |
| S10 / PROP-LEFT | fixture, opposite-prop-disengaged, approved-load, deflection, keeper, after-unload | `PV27_S10_PROP-LEFT_<view>_<sequence>` |
| S10 / PROP-RIGHT | fixture, opposite-prop-disengaged, approved-load, deflection, keeper, after-unload | `PV27_S10_PROP-RIGHT_<view>_<sequence>` |
| S10 / LOADS | fixture, approved-load, deflection, after-unload | `PV27_S10_LOADS_<view>_<sequence>` |
| S10 / SKATES | engagement, setup | `PV27_S10_SKATES_<view>_<sequence>` |
| S11 / GLASS | supported-opening, engagement, thickness-reading | `PV27_S11_GLASS_<view>_<sequence>` |
| S11 / ELECTRICAL | protected-assembly, cable-route, fold-clearance | `PV27_S11_ELECTRICAL_<view>_<sequence>` |
| S11 / THERMAL | setup, sensor-position, filter-state | `PV27_S11_THERMAL_<view>_<sequence>` |
| S11 / RECONCILE | Written/reference evidence only; no extra photo | `PV27_S11_RECONCILE_<view>_<sequence>` |
| S11 / PACKAGE | Written/reference evidence only; no extra photo | `PV27_S11_PACKAGE_<view>_<sequence>` |

Before returning: check files open, IDs match the sheet, every claimed result has traceable evidence, left/right are distinguishable, and any failure/unknown remains visible. Do not publish third-party reference material without checking its licensing; a document identifier/link and owner notes can be retained instead.

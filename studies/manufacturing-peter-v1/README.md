# Peter supplier v1 — manufacturing preparation

The owner-confirmed supplier profile is **complete enough for manufacturing preparation**. The only late-bound design inputs are production-lot thickness, coupon-selected fit clearance and final purchased hardware dimensions. This does not release full sheets or change CURRENT V32 geometry.

Source: owner confirmation, 2026-10-02. Starting HEAD: `2129f4b1a301fdb072bdc550dd577bee080aa4b2`. Delivery HEAD is the commit containing this report.

[Supplier profile](../../config/manufacturing/profiles/peter_supplier_v1.json) · [Coupon review SVG](../../exports/generated/manufacturing-peter-v1/coupon-review.svg) · [Native coupon review CAD](../../exports/generated/manufacturing-peter-v1/coupon-review.FCStd) · [Feature/operation manifest](../../exports/generated/manufacturing-peter-v1/coupon-manifest.json) · [Measurement form](../../exports/generated/manufacturing-peter-v1/coupon-results-template.json) · [One-side part register](../../exports/generated/manufacturing-peter-v1/one-side-part-register.json) · [Release status](../../exports/generated/manufacturing-peter-v1/release-status.json).

## Confirmed preparation inputs

| Item | Supplier confirmation / derived preparation value |
| --- | --- |
| Machine table | 2000 × 3000 mm |
| Sheet | 2500 × 1600 mm; 2500 along the table's 3000 direction |
| Hold-down border | 20 mm on every edge |
| Usable sheet rectangle | 2460 × 1560 mm, beginning at sheet X20/Y20 |
| Part spacing | At least 15 mm between finished part boundaries for material ≤18 mm |
| Through cutter | Ø4 mm; natural internal R2 |
| Pockets | Controlled-depth pockets/recesses supported |
| Machining faces | ONE ONLY; no flip machining |
| Plywood | Nominal 18 mm naval amescla, export-grade; void-free claim is supplier-reported, not independently certified |
| Actual thickness | **Unknown** until measurements from the real production lot |
| Formats | DXF, SVG, DWG, EPS, AI, vector PDF, CDR 2018 |
| Coupon | Supplier agrees to cut a calibration sample before full production |

The dimensions above come from the owner, not generic Internet machine specifications. The profile does not prescribe feed, spindle speed, passes or G-code. Supplier CAM applies compensation once to the finished contours and chooses retention/tool-entry details. Do not reinterpret 15 mm part spacing as 15 mm tool-center spacing. Stock thicker than the confirmed range is not silently assigned the same spacing.

This profile covers the nominal 18 mm stock. Accepted thinner parts remain unchanged. Any one-face thickness reduction or additional stock must be explicitly reflected in the relevant operation plan; this update does not substitute 18 mm material into a 12 mm door.

The V20 coupon and V25 CNC files are historical. Their nominal stock / Ø6 defaults are not inherited by this profile. The V33 inventory and premium-first nesting policy remain unchanged; use this profile's sheet/tool values for this owner's preparation.

## Compact one-face coupon

The main coupon is **300 × 210 mm**, plus a **25 × 25 mm square fit key** separated by 15 mm. Overall footprint is **340 × 210 mm**. It can be placed at X20/Y20 inside the supplier border. The key is small: the supplier must retain it during the final contour cut (tabs/retention by CAM), keeping the fit-test edges intact.

All CNC operations start from face A:

| Feature | Purpose / operation |
| --- | --- |
| Six through slots | Width = measured thickness + −0.20, −0.10, 0.00, +0.10, +0.20, +0.30 mm. Allowance is **total width**, not per side. Slot straight length 36 mm; short ends have R2 T-bones. |
| R2 pocket | 30 × 30 mm, 6 mm deep, unrelieved internal R2 control |
| T-bone pocket | 30 × 30 mm, 6 mm deep; four outward R2 semicircles along its short edges |
| Shallow locator | Ø4 × 0.5 mm flat-bottom recess; not a final pilot bore |
| Screw-test locator | Same shallow locator in a broad test zone; finish a representative pilot/countersink manually from face A after selecting the screw |
| Fit key | Stand its 25 mm edge in each slot to test actual stock thickness. Lay it into a pocket and move its square corner against the pocket corner to compare unrelieved R2 versus T-bone seating. |

The T-bone contour is a single closed wire, not overlapping DXF/SVG cut entities. It is the **coupon strategy**, not blanket permission to modify every permanent joint. Select permanent-joint relief only after fit and local structural review. The coupon is a fit/process test, not a plywood strength certification.

The representative screw family is CURRENT **F01**, provisionally 4.5 × 30 countersunk. Current Ø5 clearance / Ø9 head / 90° reference geometry does not freeze the purchased screw or pilot. Record actual screw, pilot diameter/depth and countersink diameter/angle/depth before accepting this test. A Ø4 end mill cannot be treated as a selected smaller screw pilot or as a conical countersink cutter. The manual test uses ordinary drill/driver, suitable bits and a depth stop; there is no second-face CNC operation.

## Measurement and regeneration workflow

1. Identify the real production lot; measure thickness at representative locations. Store readings in `stock.thickness_measurements_mm`, lot ID in `stock.production_lot_id`, and the chosen measured design thickness in `stock.actual_thickness_mm`. The chosen thickness must fall within the readings. Do not copy nominal 18 into that field without measurement.
2. Record the selected screw test dimensions in `coupon.screw_interface.purchased_hardware_dimensions`. Required fields are `part_reference`, `shank_diameter_mm`, `length_mm`, `pilot_diameter_mm`, `pilot_depth_mm`, `countersink_diameter_mm`, `countersink_included_angle_deg`, and `countersink_depth_mm`.
3. Generate the measured coupon using the command below. The generator refuses a cutting file when real thickness/lot evidence is missing. Send **only `coupon-cut.svg` plus its operation manifest** for coupon CAM review. The labelled `coupon-review.svg` is never a cutting file.
4. Cut/test using the same production plywood, Ø4 cutter, machine and CAM process. Record all six finished slot widths and observed fits; actual pocket and locator depths; R2/T-bone results; manual screw interface result; lot and machine/CAM run reference; tester/date. Copy the package and cut-file hashes from the manifest into a saved copy of the measurement form.
5. The owner accepts the physical coupon and chooses one tested clearance. Run `--record-results` to validate and store those results, selected clearance and corner strategy in the supplier profile. No invented acceptance limits: dimensional deviations and fit must be explicitly reviewed and accepted in the result form.
6. Regenerate final manufacturing geometry with the measured thickness, accepted clearance, Ø4/R2 tooling and measured hardware. Existing canonical builders are not silently redirected to a new thickness by this inventory/preparation tool. Their manufacturing regeneration and verification remain required before release.
7. Release full sheets only after coupon, one-face operation plans, purchased-hardware-dependent interfaces, final regeneration/validation and owner manufacturing approval all pass.

```sh
# Current safe preview: emits no machining SVG and never enables sheet release.
python3 tools/manufacturing_peter_v1.py

# After entering real lot thickness (and selected screw data before acceptance):
python3 tools/manufacturing_peter_v1.py --measured-coupon

# After physical cut, measurements, test fitting and owner coupon acceptance:
python3 tools/manufacturing_peter_v1.py --record-results path/to/completed-results.json

# Regression / independent CAD checks:
python3 tools/check_manufacturing_peter_v1.py
freecadcmd tools/verify_peter_coupon_cad.py
```

The measurement template is an output template; save completed results under another filename. `--record-results` verifies the actual cut-file hash. Changes to lot readings, measured thickness, tooling or the coupon/process inputs invalidate prior acceptance. The test suite uses synthetic data only in temporary directories and never fills the owner's measurement fields.

## One-sided manufacturing gate

Every released canonical manufacturing part must be `ONE_SIDE_CNC_READY` or `ONE_SIDE_CNC_PLUS_MANUAL_FINISH`. The latter requires explicit ordinary-tool manual operations. An operation plan must identify a local part orientation, a single CNC face, depths, tool access and any manual finish. Machining from the other face or a CNC flip causes rejection. A simple face label alone is not machining proof.

The initial register covers all **93 current wood inventory components**:

- **78 `BLOCKED_OPERATION_AUDIT`**: operation-face plans are not yet verified.
- **15 `BLOCKED_DECOMPOSITION_REQUIRED`**: the eleven existing compound/stepped component holds plus four laminated leg blocks needing individual planar layer extraction.

These statuses **do not assert that 93 parts require two-sided machining**. They prevent an inventory model from being mislabelled manufacturing-ready before its operations are reviewed. No flip instructions are generated. A genuine opposing-face requirement must be blocked or proposed for simpler planar decomposition in a separately reviewed change. No accepted parts are decomposed or modified here. Reviewed register entries are preserved on regeneration.

Preparation and release are separate: the supplier profile is complete; the unperformed operation audit is engineering work, not missing supplier data.

## Verification and current status

- 25 release/profile regression checks, including refusal of nominal-only cuts, wrong lots, failed T-bone tests, untested clearance, stale coupon acceptance and opposite-face operations.
- 20 independent OpenCascade checks: valid single coupon/key solids, spacing, T-bone area, positive corner clearance versus the unrelieved control, slot-clearance signs and document recomputation.
- All **1,512 files from the starting HEAD** remain byte-identical, including CURRENT geometry, viewer and V33 inventory.
- The committed coupon CAD/SVG is a **nominal illustration only**. Actual lot thickness, selected clearance and physical coupon validation remain unset. No `coupon-cut.svg` or full-sheet manufacturing file is supplied.

**FULL-SHEET CNC RELEASE: BLOCKED until physical coupon validation and the remaining release gates pass.**

Original source: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

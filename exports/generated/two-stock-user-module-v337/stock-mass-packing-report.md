# V33.7 material, mass and packing study

PRELIMINARY — NOT FOR CNC. No production nesting, CAM or G-code. Full-sheet release remains blocked by measured stock, coupon, selected fit, purchased hardware and physical qualification.

Active plywood purchase families are nominal12 mm and18 mm only; actual production-lot thickness remains unknown. Four SW01 solid-wood leg blanks are separate. M045 retains its6 mm finished web through one-face reduction from12 mm stock, so it does not introduce a6 mm purchase family.

| Nominal stock | Pieces | Outer area m² | Net projected area m² | Full sheets | Net utilization | Gross waste incl. offcuts | Reusable rectangular offcuts m² |
|---|---:|---:|---:|---:|---:|---:|---:|
| 18 mm | 65 | 5.2623 | 4.4013 | 2 | 55.02% | 44.98% | 1.3752 |
| 12 mm | 39 | 1.8077 | 1.3573 | 1 | 33.93% | 66.07% | 1.5703 |

The full-sheet projection is an accounting assumption. The deterministic layout tries three rectangle orderings with actual contour overlays; it is not an optimized or production nest. It preserves20 mm sheet borders and reserves15 mm between finished boundaries. Spacing allocation is not cutter kerf, and contour/cutout scraps are not automatically reusable. Nest small12 mm members into the same thickness batch first; use qualified premium offcuts/cut-to-size stock if available. Do not downgrade structural members or mix nominal thickness families.

Practical procurement study for 18 mm: [[2500, 1600], [2500, 1600]] mm rectangles; supplier hold-down/defect approval still required.

Practical procurement study for 12 mm: [[2100, 1150]] mm rectangles; supplier hold-down/defect approval still required.

| Mass basis | LOW kg | NOMINAL kg | HIGH kg |
|---|---:|---:|---:|
| Delivered wood, including unfinished manual-removal stock | 51.813 | 61.277 | 70.778 |
| Finished installed wood | 51.785 | 61.242 | 70.734 |
| Mechanical planning scenario incl. explicit unknown-hardware allowance | 60.674 | 77.354 | 97.069 |
| Full planning scenario incl. glass/future electronics | 93.077 | 126.957 | 163.472 |

Plywood density is configurable LOW/NOMINAL/HIGH; nominal650 kg/m³. Solid wood uses its separate material assumptions. New purchased hardware mass remains UNKNOWN, not zero or certified by a visual envelope.

Preferred20 kg-target wood bundles provide about5 kg allowance below the25 kg practical ceiling at HIGH density plus estimated protection, without increasing the four-bundle count. Long-panel footprints/protection are retained; total footprint grows1.61% and aggregate box volume4.21% versus the25 kg candidate. The mixed small-part bundle is taller/wider and requires stack-stability/identification qualification. This is a handling projection, not transit qualification. Hardware, glass and electronics remain separate.

| Package | External dimensions mm | Wood nominal kg | Gross HIGH kg |
|---|---|---:|---:|
| P20-01 | [1353.1, 641.9, 74.00000000000003] | 15.604 | 19.998 |
| P20-02 | [1317.1, 617.0, 88.00000000000024] | 15.568 | 19.995 |
| P20-03 | [825.0, 768.9, 127.99999999999977] | 15.680 | 19.999 |
| P20-04 | [1197.1, 275.0, 335.80000000000007] | 14.426 | 18.537 |

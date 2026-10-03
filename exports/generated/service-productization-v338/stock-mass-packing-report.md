# V33.8 material, mass and packing study

PRELIMINARY — NOT FOR CNC. No production nesting, CAM or G-code. Full-sheet release remains blocked by measured stock, coupon, selected fit, purchased hardware and physical qualification.

Active plywood purchase families are nominal12 mm and18 mm only; actual production-lot thickness remains unknown. Four SW01 leg blanks and two SW02 landing blanks are separate solid wood. M045 retains its6 mm finished web through one-face reduction from12 mm stock, so it does not introduce a6 mm purchase family.

| Nominal stock | Pieces | Outer area m² | Net projected area m² | Full sheets | Net utilization | Gross waste incl. offcuts | Reusable rectangular offcuts m² |
|---|---:|---:|---:|---:|---:|---:|---:|
| 18 mm | 59 | 5.2338 | 4.3734 | 2 | 54.67% | 45.33% | 1.4258 |
| 12 mm | 39 | 1.8077 | 1.3573 | 1 | 33.93% | 66.07% | 1.5703 |

The full-sheet projection is an accounting assumption. The deterministic layout tries three rectangle orderings with actual contour overlays; it is not an optimized or production nest. It preserves20 mm sheet borders and reserves15 mm between finished boundaries. Spacing allocation is not cutter kerf, and contour/cutout scraps are not automatically reusable. Nest small12 mm members into the same thickness batch first; use qualified premium offcuts/cut-to-size stock if available. Do not downgrade structural members or mix nominal thickness families.

Practical procurement study for 18 mm: [[2500, 1600], [2500, 1600]] mm rectangles; supplier hold-down/defect approval still required.

Practical procurement study for 12 mm: [[2100, 1150]] mm rectangles; supplier hold-down/defect approval still required.

| Mass basis | LOW kg | NOMINAL kg | HIGH kg |
|---|---:|---:|---:|
| Delivered wood, including unfinished manual-removal stock | 51.787 | 61.277 | 70.829 |
| Finished installed wood | 51.762 | 61.244 | 70.786 |
| Mechanical planning scenario incl. explicit unknown-hardware allowance | 60.651 | 77.356 | 97.120 |
| Full planning scenario incl. glass/future electronics | 93.054 | 126.959 | 163.523 |

Plywood density is configurable LOW/NOMINAL/HIGH; nominal650 kg/m³. Solid wood uses its separate material assumptions. New purchased hardware mass remains UNKNOWN, not zero or certified by a visual envelope.

Preferred target 20 kg: 4 bundles, minimum margin 5.001 kg below the25 kg practical ceiling at HIGH density plus estimated protection. Footprint change versus25 kg candidate 1.61%; aggregate box volume change 2.72%. This is a handling projection, not transit qualification. Hardware, glass and electronics remain separate.

| Package | External dimensions mm | Wood nominal kg | Gross HIGH kg |
|---|---|---:|---:|
| P20-01 | [1353.1, 641.9, 74.00000000000003] | 15.604 | 19.998 |
| P20-02 | [1317.1, 617.0, 88.00000000000024] | 15.568 | 19.995 |
| P20-03 | [825.0, 768.9, 127.99999999999977] | 15.680 | 19.999 |
| P20-04 | [1197.1, 275.0, 371.8000000000002] | 14.426 | 18.652 |

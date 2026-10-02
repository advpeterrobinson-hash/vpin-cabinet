# Preliminary sheet feasibility

PRELIMINARY — NOT FOR CNC. No CAM/G-code. Not optimized. Exact contour overlays inside conservative rectangles; 20 mm border and >=15 mm spacing. All stock stays premium in this first attempt. Sheet format for non-18 mm stock is a study assumption, not a supplier stock order.

| Stock mm | Pieces | Structural | Secondary eligible | Area-only lower bound | Row-layout sheets |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 18 | 88 | 87 | 1 | 2 | 2 |
| 12 | 25 | 14 | 11 | 1 | 1 |
| 8 | 2 | 0 | 2 | 1 | 1 |
| 6 | 13 | 0 | 13 | 1 | 1 |
| 4 | 2 | 2 | 0 | 1 | 1 |

## Largest parts

| ID / instance | Finished local XY mm | Sheet rotation | Fits |
| --- | --- | --- | --- |
| M001 / P001-Main | 596.900 × 1308.100 | 90° | YES |
| M002 / P002-Main | 596.900 × 1308.100 | 90° | YES |
| M005 / P005-Main | 564.000 × 1272.100 | 90° | YES |
| M035 / P046-Main | 780.000 × 723.900 | 0° | YES |
| M025 / P034-Main | 500.000 × 1020.000 | 90° | YES |
| M045 / P063-Main | 740.000 × 457.000 | 0° | YES |
| M004 / P004-Main | 564.000 × 596.900 | 90° | YES |
| M003 / P003-Main | 564.000 × 400.050 | 0° | YES |
| M056 / P079-Main | 351.000 × 628.000 | 90° | YES |
| M057 / P080-Main | 351.000 × 628.000 | 90° | YES |
| M032 / P043-Main | 723.900 × 248.000 | 0° | YES |
| M031 / P042-Main | 723.900 × 248.000 | 0° | YES |

Every individual part fits. Every rotated part remains FACE_A up. Ninety-degree rotation is geometrically possible for all current members, but no arbitrary grain-swapping rotation was used to improve packing. Long-axis grain is a conservative planning assumption, not a verified veneer direction.
Hold-down: every piece lies inside the border; local retention for tiny parts, narrow strips and open frames still needs supplier tabs/fixtures. A perimeter fit does not certify vacuum holding.
Do not downgrade structural pieces. A secondary-stock alternative is allowed only after the small-subset/extra-premium-sheet trigger is reviewed; this task does not automatically invoke it.

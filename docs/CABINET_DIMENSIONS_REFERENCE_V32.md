# Owner-supplied cabinet dimensions reference

Owner intent, 2026-09-29: use this PDF to clarify dimensions and holes during V32 development. This is reference evidence, not selected-hardware fit or manufacturing approval.

Source: [pinball-cabinet-dimensions.pdf](https://sdssautomotive.wordpress.com/wp-content/uploads/2022/04/pinball-cabinet-dimensions.pdf), 21 pages, visually reviewed. SHA256: `c5b905f876af090e441079e9fc42e1b1083dd3f715090484431b1cd897d560d6`. Page numbers count from 1. Authorship and redistribution permission are unconfirmed; no PDF or extracted drawing is added to the repository.

Conversions use 25.4 mm/in. Preserve printed decimals; do not silently reinterpret rounded labels as exact fractional-inch specifications.

| Feature | PDF page | Printed inches | Converted mm | V32 disposition |
|---|---:|---:|---:|---|
| Side length | 20 | 51.50 | 1308.10 | Matches current reference |
| Front / rear heights | 20 | 15.75 / 23.50 | 400.05 / 596.90 | Matches current reference |
| Rear top flat | 20 | 7.13 | 181.102 | Current 180.975; retain datum pending rounding review |
| Front panel width | 8 | 25.00 | 635.00 | Not assembled outside width; keep V32 body 600, current front panel 564 |
| Coin opening width / height | 8 | 12.25 / 10.37 | 311.15 / 263.398 | Current 311.15 ×264.31875; height differs by 0.92075 |
| Front button bore | 8 | DIA 1.00 | 25.40 | Matches nominal front study; hardware unconfirmed |
| Front button recess | 8 | drill 1 3/8 DIA, 3/8 deep | Ø34.925, depth 9.525 | Reference only, not adopted |
| Side button bore label | 2, 20 | DIA 1.12 | 28.448 | Conflicts with current Ø15.875 bore; current Ø28.575 is a recess |
| Side button offsets from drawn front edge | 2 | 3.50 / 5.31 | 88.900 / 134.874 | Different from Y255/310; requires datum/ergonomic review |

Use the reference to challenge inherited dimensions and establish candidate layouts. Before adopting a dimension, record the page, printed value, conversion, cabinet datum and adoption decision in the relevant configuration/review. Actual selected parts govern their mounting holes, recesses and clearances.

Priority follow-up is the side-button stack: verify barrel, nut, washer and panel thickness against the current two-sided recesses and 5.3 mm annular web. This discrepancy does not establish a replacement stack or strength. Door height, front recesses and plunger details likewise require selected-part evidence before machining.

The PDF does not establish the four-top-screw shelf interface, actual raised-playfield clearance, hinge/prop loads or PC architecture. Continue [simple shelves](SIMPLE_SHELVES_V32.md) and the [panel closure sequence](PANEL_CLOSURE_V32.md). This registration changes no geometry; CAD reruns are not required for this documentation-only change.

Original assessment: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

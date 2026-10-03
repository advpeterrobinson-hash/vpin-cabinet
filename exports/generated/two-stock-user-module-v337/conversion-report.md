# V33.7 nominal-stock conversion audit

**Design study passed; manufacturing remains blocked.** Fifteen real manufacturing members use 12 mm nominal stock. All unaffected CURRENT B-reps remain exactly serialized-equivalent. No hardware, display, glass, door, hinge or support datum moves. The conversion document is isolated; integration/promotion belongs to the root build.

| Family | Pieces | Finished geometry and one-face process |
|---|---:|---|
| M028 floor filter holders | 2 | 12 mm corner lands; underside R86 × 4 mm service pocket and four R7 × 4 mm head recesses retain the old 8 mm media/guard/screw stack. FACE A is underside. |
| M045 backglass bezel | 1 | **12 mm stock, 6 mm finished**. Explicit 6 mm rear-face reduction preserves 2 mm glass clearance, 2 mm display clearance and the visible front plane. This is not a third stock family or a claim of 12 mm finished thickness. |
| M058 intake filter frames | 2 | 12 mm full thickness, extra 6 mm entirely rearward. Door mating plane and 220 × 80 mm aperture unchanged. FACE A is exterior. |
| M059 baffle front walls | 2 | 244 × 110 × 12 mm. Extra material outside the unchanged chamber. FACE A faces forward. |
| M060 baffle ceilings | 2 | 244 × 36 × 12 mm. Extra material above the unchanged chamber. FACE A faces up. |
| M061 baffle sides | 4 | 98 × 36 × 12 mm, common exterior lower-edge rebate 3 mm deep × 32 mm high across 36 mm width. The local finished wall remains 9 mm; the upper 66 mm remains 12 mm. FACE A faces outward. |
| M066 optional fan blanks | 2 | 128 × 128 × 12 mm, extra 6 mm rearward. Door plane and 105 mm station pitch unchanged. Mutually exclusive with fan/guard/mesh. |

Each baffle is rebuilt from four non-overlapping planar manufacturing members. Local-to-installed round trips and assembled union comparisons both give **0 mm³** difference. These are actual profiles, including the side rebate, rather than bounding rectangles.

## Functional checks

The baffle inner chamber is unchanged: 220 × 36 × 98 mm, 776,160 mm³ per side. Each inlet remains 17,600 mm² and each downward mouth remains 7,920 mm². The new front wall retains 3.1 mm modeled speaker-envelope clearance. The side rebate retains 2.0 mm clearance to the existing passive lower bolt body. Physical hardware qualification remains required; a CAD gap is not a manufacturing fit allowance.

An explicit negative trial without the rebate produced 660 mm³ overlap with the passive bolt-body reserve. The final static check uses **every** existing source shape, including hardware and service reserves, with no broad `actual()` filtering. It reports no added-wood intersection. No door hardware is relocated to achieve this result.

Each floor holder retains 5,118.852459 mm² of full 12 mm land (28.73% of its net profile). The remaining 8 mm web preserves the old screw-head bearing, media, rotated guard and fan-nut pass-through interfaces. The installed lowest wood point is Z6 mm, still above the cabinet Z0 datum; it is 0.5 mm below the old guard reserve. Actual installed leg/ground clearance remains a physical build check. A conservative exact through-hole silhouette continuously swept downward 80 mm clears all retained occupied parts; four holder screws are removed and media/guard travel with the holder.

Both rear intake frames have a clear continuous 80 mm rearward removal corridor. There are no selected intake-frame or optional-blank screw heads in the current model. Their extra 6 mm stack must be included when selecting purchased fastener lengths; no existing hardware head is silently buried or moved. Attachment quantities remain governed by the hardware catalog.

The motion proof includes continuous differential certificates for both rear doors 0–100°, the new backbox wood and optional blanks through 0–90°, the populated backbox against the new floor-holder material, and playfield service 0–50°. The playfield 48 mm lift clears a conservative full bounding-prism sweep. Fan service loops are additionally sampled at 1° through each door opening. Existing unchanged architecture certificates are retained by source hashes. Required fold-angle samples also pass.

## Mass and process cost

Using actual B-rep volumes at the configurable planning density of 650 kg/m³:

- Installed wood increase: **0.424979633 kg**.
- Optional pair of fan blanks increase: **0.127298985 kg**.
- All 15 members together increase: **0.552278618 kg**.

The M045 exception keeps its old finished volume and mass. Facing the entire 740 × 457 mm rectangular stock blank by 6 mm would remove 2,029,080 mm³ (1.318902 kg at planning density). The net finished bezel-outline reduction is 365,880 mm³; the distinction must remain visible in later CAM/material-utilization planning. No production toolpath or optimized operation order is issued here.

## Manufacturing holds

All operations enter FACE A; FACE B receives no CNC. Nominal stock is 12 mm, with actual production-lot thickness and coupon clearance late-bound. Existing square-corner manual-finish/fit obligations remain; no blanket dogbones are introduced. M028 circular recesses are compatible in principle with the supplier Ø4 mm cutter. M061 rebates are open edge strips, allowing cutter runout beyond the perimeter without a closed internal corner.

Purchased fan/filter screws, actual hinge and latch dimensions, exact accessory stack lengths, stock thickness, coupon and final CAM remain release gates. This audit changes neither manufacturing release nor hardware freeze status.

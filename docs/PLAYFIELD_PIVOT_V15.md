# Playfield pivot v0.15 — steel cheek plates on a CNC plywood cradle

> Current owner baseline: [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md). Older assist/stay descriptions below are historical; no assist hardware blocks current CNC. Use the active hardware/feature registers for procurement.

Status: engineering-selected baseline; not manufacturing-ready.

## Decision

Keep the playfield display cradle primarily CNC plywood. Concentrated hinge loads are transferred through local steel plates rather than by letting a pivot pin work directly in plywood.

The selected baseline is:

- cradle side rails and rear structure: 18 mm good-quality compensado naval;
- rear pivot zone: two laminated 18 mm plywood members (~36 mm local wood thickness);
- one 6 mm carbon-steel pivot cheek plate on each side;
- one 3 mm steel backing/spreader plate on the opposite face of each laminated pivot zone;
- four M8 class 8.8 through-bolts per side;
- short 15 mm steel pivot journal/stub axle per side;
- one external 15 mm flange bearing per cabinet side;
- positive axial retention independent of bearing set screws.

The display chassis is never the structural hinge member. The v0.16 cabinet/cradle envelope is intentionally model-agnostic for compact 42/43-inch 4K high-refresh displays available in Brazil.

## Pivot cheek plate to quote locally

Preferred material: **A36 or SAE 1020 carbon steel plate**.

Nominal thickness: **6.0 mm**.

Acceptable raw stock substitution: **6.35 mm / 1/4 inch** if the final CAD stack is updated before fabrication.

Plate envelope for each left/right plate:

- 140 mm front/rear length;
- 80 mm height;
- 6 mm thickness;
- R6 nominal external corner radius;
- four Ø9 mm holes for M8 through-bolts;
- two hole columns at 70 and 120 mm from the plate rear reference edge;
- two hole rows at 20 and 60 mm from the bottom edge;
- pivot axis datum 25 mm from rear plate edge and 40 mm from bottom edge.

The pivot-journal feature is intentionally treated as a fabrication interface rather than a simple laser-cut final hole. Final journal fit must be checked against the purchased bearing pair.

Suggested local search/quote wording:

`2 peças chapa aço carbono A36/1020 6 mm, 140 x 80 mm, corte laser, 4 furos Ø9, cantos R6, desbastada/rebarbada`

Ask the fabricator whether 6.0 mm or 6.35 mm stock is more readily available before the final DXF is issued.

## Backing plate

Each pivot cheek plate gets an inside spreader/backing plate so the M8 clamp load is distributed through the laminated plywood rather than concentrated under washers.

Baseline:

- A36/SAE 1020;
- 3 mm thickness;
- approximately 90 x 65 mm;
- same four-bolt clamping pattern as the outer plate.

Final outline may be trimmed for cable/strut clearance after the FreeCAD sweep.

## Pivot journal / stub axle

Current baseline diameter: **15 mm**.

Preferred material: SAE 1045 or equivalent turned/ground steel bar.

Current packaging candidate:

- ~65 mm projection from the pivot plate;
- ~78 mm total raw journal length.

The final projection is not frozen until the actual bearing width, cabinet-side plywood stack and any backing plate are measured.

The intended fabricated arrangement is a short journal that stays with the cradle pivot plate. The journal passes through a fitted plate feature and is jigged perpendicular during fabrication. Welding, if used, occurs on the non-bearing face; the bearing journal surface must remain clean, concentric and free of weld spatter/distortion.

This is outsourced metalwork. The cabinet builder is not expected to weld.

## Bearing selection

Preferred current family: **UCFL202, 15 mm, two-bolt oval flange bearing**.

Reason:

- cast/industrial housing is more appropriate for a premium cabinet than a light zinc KFL housing;
- self-aligning insert bearing tolerates small assembly misalignment;
- 15 mm versions are readily available in the Brazilian industrial/marketplace channel;
- bearing is replaceable without rebuilding the wood cradle.

`KFL002 15 mm` remains an inexpensive fit/mockup alternative, but is not the preferred premium final part at this stage.

**Do not CNC the cabinet bearing bolt pattern yet.** Buy the actual pair first and measure:

- housing overall width/height;
- mounting-hole center spacing;
- mounting-hole diameter;
- inner-ring width;
- set-screw locations;
- actual 15 mm bore fit.

The cabinet-side mounting uses through-bolts and a 3 mm internal steel backing plate, not wood screws into a single 18 mm wall.

## Why short journals instead of one long shaft

The cabinet is 580 mm wide, but a long full-width shaft would require a large lateral withdrawal distance for complete cradle removal. Short journals allow service from each side with only a small lateral clearance.

Complete cradle removal is intended to work as follows:

1. isolate cabinet power;
2. remove lockdown bar and playfield glass;
3. raise the playfield cradle;
4. engage both independent mechanical safety stays;
5. add a temporary rated support strap/prop for complete cradle removal;
6. disconnect display power/video service-loop connectors;
7. release positive journal retention and bearing set screws;
8. unbolt or slide each flange bearing off the short journal;
9. remove the display/cradle assembly as a module, preferably with two people.

Normal maintenance does not require removing the cradle.

## Closed-position restraint and service safety

The pivot is not used as the only play-position support.

Closed position requires structural support pads plus positive latches/retainers so DOF vibration and nudging do not bounce the display cradle against the hinge.

Gas struts are lift assistance only. They are not safety devices.

The final machine requires two independent positive mechanical safety stays. A person working under the raised display must not be exposed to a falling playfield display if one or both gas struts fail.

## Shock warning

The playfield display is expected to use mains voltage unless a future selected model uses an external low-voltage brick. Mechanical service around the raised display requires cabinet power isolation before manipulating its power lead, service loop, pivot, gas struts or safety stays. A pinched or abraded mains lead is a blocking shock/fire defect.

## Display-model dependency

The pivot plates, bearings and plywood load paths are sized independently from one LG model. Final gas-strut force and longitudinal display position remain deliberately open until the exact playfield display is purchased and its actual mass, chassis dimensions and center of gravity are measured.

The permanent cabinet targets the v0.16 service envelope:

- up to 560 mm physical chassis width across the cabinet;
- up to 970 mm physical chassis length;
- up to 55 mm depth;
- up to 12 kg display mass design limit.

## What may be researched/bought now

Reasonable to research now:

- 6 mm A36/SAE1020 plate cutting;
- 3 mm A36/SAE1020 backing plate;
- UCFL202 15 mm flange bearings;
- 15 mm SAE1045/ground shaft stock;
- M8 class 8.8 structural hardware.

Do **not** buy final gas struts, safety stays or closed-position latches yet. Their geometry is still linked to the selected display, finished cradle CG and FreeCAD motion sweep.

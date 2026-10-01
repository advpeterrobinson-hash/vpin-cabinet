# Current V32 wooden pivot — mounted support refinement

Current CAD remains `exports/generated/wood-dowel-pivot-v32/play.FCStd` and `current-v32.step`; SERVICE, LIFT-OUT and EXPLODED saved solids are beside them. Current viewer: `exports/generated/viewer-v32/index.html`. Source: `config/wood_dowel_pivot_v32.json` and `tools/wood_dowel_pivot_v32_entry.py`. Rebuild with `bash tools/run_service_correction_v32.sh`; generate review PNGs with `uv run --with matplotlib python tools/render_wood_dowel_pivot_v32.py`.

The final cleanup starts from HEAD 67605c770a0494dfe414e5bc53e46cc6a9612330. Only the old exciter relief in each support is filled and SSF_Exciter2L/R are moved rearward. The wood-dowel concept, Ø32 × 560 mm dowel, pivot axis, cradle seat, floor bearing, six mounting screw coordinates, playfield base and lift-out are unchanged. All other saved subsystem solids, including the rear door, buttons, PC/electronics, shelves, other audio and power/RJ45, were compared with that HEAD and preserved exactly.

## Support profile and open seat

Two mirrored 18 mm nominal plywood supports stand against the inner side faces, with their complete feet on the real floor top at Z36. The upper profile is widened from 24 to 80 mm in Y. The floor-bearing stem runs from Y1017 to Y1075.251 (58.251 mm wide): its front setback avoids the existing rear shelf. An upper shoulder clears the retained crossmember guide vertically by 1 mm; a local forward widening above Z453.220 clears its rear face by 0.5 mm, and the rear edge is straight, with no exciter relief. Only SSF_Exciter2L/R are translated +7.251 mm in Y to give 2 mm clearance; X, Z and orientation remain unchanged in the rear SSF zone. These are features of the same single wood profile, not added pieces. Both support shapes are valid single solids.

The prior real solid ended at Z473.396, rather than the former uncut blank top of Z508.220, because a 24 mm profile was narrower than the Ø33 seat. Its effective seat depth was 5.176 mm. The revised top is Z514.220; the bottom of the circular seat is Z468.220: **46 mm effective open-U depth**. The mouth is 33 mm wide for the Ø32 dowel. The semicircular seat radius is 16.5 mm, centre Z484.720, with the shaft axis Z484.220 to seat under gravity. There is no clip, keeper, bearing or closed top at the cradle.

Approximate circular geometric wrap: 25.9% before → 50% semicircular seat after. Straight walls extend above the cylinder and constrain lateral motion; this is geometric enclosure, not a claim that the whole semicircle carries contact pressure. Upper arm web width is 23.5 mm on either side of the slot. The rejected 1.75 mm local forward ligament is widened to 8.25 mm by extending the front edge locally to Y1010.5 from Z453.220 to the shoulder. The minimum occurs beside the unchanged straight U wall at Y1018.751. The 80 mm overall profile, cradle, floor foot and all screw coordinates remain unchanged. The fixed guide prevents reaching the preferred 10 mm without changing other accepted geometry; 8.25 mm exceeds the absolute 8 mm requirement. Physical validation remains required before manufacture.

Minimum vertical motion for the dowel bottom to reach the ear tops is 46 mm; demonstrated 48 mm unseating leaves 2 mm clearance. Take LIFT-OUT from PLAY after removing glass/releasing lockdown. The base + TV + VESA + dowel + straps remain one unit; supports and their six screws stay in the cabinet. No support screw is removed. SERVICE remains a 50° manually held opening about the same wooden axis. Sampled checks use 2° opening and 2 mm lift increments; no continuous-sweep or structural certification is claimed.

## Required internal screw mounting — no glue dependence

**SCREWS = REQUIRED**
**WOOD GLUE = OPTIONAL AFTER FINAL VALIDATION**
**NAILS = NOT USED**

The structural path is:

PLAYFIELD / DOWEL → WOOD CRADLE → WOOD SUPPORT → **DIRECT BEARING ON CABINET FLOOR**.

The lateral screws retain against tipping, separation from the side, longitudinal movement and displacement during lift/service. They are not the primary vertical load supports. Optional PVA at support↔side and support↔floor is only added after dry fit, position verification, physical pivot tests and final geometry approval. No strength or safety claim depends on glue. During prototyping the dry screwed assembly remains removable.

Candidate: fully threaded, flat countersunk wood screw, Torx preferred, **4.5 × 30 mm**, three per support. A common [SPAX family reference](https://www.spax.com/gb-en/p/stainless-steel-screw-full-thread-flat-countersunk-head-t-star-plus-4cut-stainless-steel-a2.html?variant=1197000450303) offers this diameter/length and a 3 mm hardwood predrill. This is a family reference, not a purchased final hardware selection. Nominal head envelope Ø9 × 90° must be matched to the actual screw before CNC. No proprietary vendor drawing was imported.

With a flush countersunk head, nominal length includes the head: 30 − 18 = **12 mm side engagement**, and 18 − 12 = **6 mm exterior wood beyond the tip**. The model uses a 2 mm pointed end; full-diameter shaft engagement is about 10 mm. A Ø5 support through-hole and Ø9 × 90° countersink remove 2 mm of head-seat depth, preserving 16 mm under the clearance countersink; the actual head taper extends 2.25 mm, supported by the clearance bore. Flush seating does not add extra penetration. Nominal retention geometry is suitable as a candidate; screw pullout/shear capacity in the purchased plywood and assembled pivot still require physical proof. No certified fixing capacity is claimed.

Before finalizing length, measure both pieces and the actual head/point. Compute engagement E = L − measured support thickness; exterior residual R = measured side thickness − E; and maximum safe pilot depth = measured side thickness − 3 mm retained skin. The current measured-thickness fields are unset; 18/18 mm values are nominal engineering values. Do not blindly reuse the nominal length if measured stock fails the residual margin or head geometry differs.

Screw centres are generated from actual horizontal sections of the final relieved support. Low Z is the greater of floor+20 and real PC-envelope top+driver-radius+2, so a 150 mm long, Ø16 driver probe clears the installed PC. High Z is the U bottom−20; middle Z interpolates those limits. Low/mid/high Y centres are staggered within their actual available section. Minimum centre-to-profile-edge is 20 mm; minimum actual inter-screw distance is about 128.2 mm, exceeding the 40 mm initial rule. The high centre stays at least 20 mm below the weakened-U region. L/R screws are mirrored.

| Screw | Head XYZ mm | Tip XYZ mm | Side pilot XYZ mm |
|---|---|---|---|
| PF_SupportMountScrewL1 | 36.000, 1037.000, 192.000 | 6.000, 1037.000, 192.000 | 18.000, 1037.000, 192.000 |
| PF_SupportMountScrewR1 | 564.000, 1037.000, 192.000 | 594.000, 1037.000, 192.000 | 582.000, 1037.000, 192.000 |
| PF_SupportMountScrewL2 | 36.000, 1042.500, 320.110 | 6.000, 1042.500, 320.110 | 18.000, 1042.500, 320.110 |
| PF_SupportMountScrewR2 | 564.000, 1042.500, 320.110 | 594.000, 1042.500, 320.110 | 582.000, 1042.500, 320.110 |
| PF_SupportMountScrewL3 | 36.000, 1055.251, 448.220 | 6.000, 1055.251, 448.220 | 18.000, 1055.251, 448.220 |
| PF_SupportMountScrewR3 | 564.000, 1055.251, 448.220 | 594.000, 1055.251, 448.220 | 582.000, 1055.251, 448.220 |

Left screws drive in −X from X36 to X6; right screws drive in +X from X564 to X594. No tip reaches the exterior, and no floor/exterior-side fastener is used.

## CNC and ordinary-tool assembly

Assembly drawing: `exports/generated/wood-dowel-pivot-v32/support-mounting-assembly.svg`; coordinate schedule: `support-mounting-schedule.json`.

- SUPPORT: CNC Ø5 clearance through-hole and Ø9 × 90° countersink, nominal depth 2 mm, on the interior-access face.
- SIDE INNER FACE ONLY: CNC Ø3 × **1 mm shallow pilot locator**. The saved CAD contains only these shallow locators, not a deep or exterior through-hole.
- MANUAL FINISH: pilot Ø3 to **13 mm total depth measured from the side INNER FACE**, including the existing locator and deepest drill-tip travel. **15 mm absolute maximum** for nominal 18 mm stock; retain ≥3 mm wood beyond the deepest pilot point. Recommended 13 mm retains 5 mm below the pilot. Fit a depth stop; a verified tape mark is a fallback. If drilling through the support, these correspond to 31 mm recommended and 33 mm maximum from its flush head face, including drill point.
- Dry-fit the support against floor and side datums, confirm mark alignment, finish pilots with common drill/driver and depth stop, fit all three screws flush, then test the assembled pivot/lift. Avoid countersinking past flush. Glue is optional only after final validation; no nails.

## Flush rear door, same approved hardware

The wood door outer face was Y1320.1, 12 mm beyond the real rear plane. It is now **Y1308.1 = rear exterior plane**, exactly flush. The same 12 mm door and existing handle, lock, hinge leaves and pins are moved inward 12 mm; no extra frame or hardware was introduced. A 1 mm clearance is cut around the existing inset opening; shallow/local seats accommodate the same fixed hinge leaves. The existing 20 × 24 × 2 mm flat lock keeper is reoriented horizontally under the rear header, with a small local seat, so the translated cam can engage it; its shape/volume and hardware count are unchanged. Exterior handle/lock/hinge hardware naturally projects; the flush requirement is the wooden door outer face.

Downward door opening through 110° was screened at 2° samples without collisions. Hinge-axis Y moves from 1324.1 to 1312.1 with the same door geometry. No fixed fan, power/RJ45 or electronics object moved. The new hinge recess leaves about 6 mm of nominal wood behind its leaf seat; attachment/load qualification remains provisional with the rest of the approved hardware envelopes. No structural/manufacturing release is claimed.

## Current counts

PLAYFIELD PIVOT CUSTOM METAL PARTS: 0
PLAYFIELD PIVOT BEARINGS: 0
PLAYFIELD PIVOT BUSHINGS: 0
PLAYFIELD PIVOT STEEL RODS: 0
PLAYFIELD PIVOT WOOD DOWELS: 1
PLAYFIELD PIVOT CNC WOOD SUPPORTS: 2
PLAYFIELD BASE PLYWOOD PANELS: 1
COMMERCIAL STRAPS: 4
STRAP SCREWS: 8
SUPPORT MOUNTING SCREWS: 6
TOTAL METAL PARTS IN PLAYFIELD PIVOT SYSTEM: 18

No other pivot/support metal is allowed. The exploded model includes only base, dowel, four straps, eight strap screws, two cradles and six cradle-to-side screws. Both cradles and all mounting screws are stationary in SERVICE/LIFT-OUT.

CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

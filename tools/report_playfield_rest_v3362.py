"""Owner30mm-per-side trim and honest closed-support finding. CERN-OHL-S-2.0."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/playfield-rest-v3362'
def read(n):return json.loads((O/n).read_text())
v=read('geometry-validation.json');m=read('manufacturing-audit.json');mass=read('mass-budget.json');audit=read('closed-support-audit.json');q=read('validation.json');assert q['pass'];r=v['relief']
text=f'''# V33.6.2 — wider front relief and missing closed-position support

HEAD BEFORE: `f8bffe2638469adae3f827045f6b9505d0b7300a`

HEAD AFTER: commit containing this report (`git log -1 --format=%H -- exports/generated/playfield-rest-v3362/README.md`).

[Current viewer](../viewer-v32/index.html) · [Native CAD comparisons](review.html) · [Support audit](closed-support-audit.json) · [T1 landing study](t1-rest-study/README.md) · [Wood BOM](manufacturing-bom.md)

**The enlarged M025 relief is CURRENT. CLOSED_POSITION_SUPPORT_BLOCKED: the current PLAY pose has no front landing and is not a mechanically complete supported assembly. CNC full-sheet release remains BLOCKED.**

## Requested cut

The owner confirmed **30 mm farther inward on each side**, not a rearward extension. Each front edge is now inset **52 mm total** from the original500 mm board width. The front section is **396 mm wide**, versus456 mm previously. The87 mm longitudinal extent and single R8 transition per side remain unchanged. In the existing playfield frame: X102–498 across the narrowed front; localY20–107, with the arc beginning atY99. The part remains one18 mm plywood CNC solid with no horn, bridge, finger or extra dogbone.

The enlarged cut removes **{r['removed_volume_mm3']:,.0f} mm³**, or **{r['mass_removed_kg_at650']:.6f} kg** at650 kg/m³. M025 volume is **{v['base_volume_mm3']:,.6f} mm³**. Its front section is **7,128 mm²**, retaining79.2% of the original front width. This is an owner-selected service-space allowance beyond the minimum required reference-envelope clearance; it is no longer described as the minimum-material-removal profile.

VESA load reserve remains {r['nearest_VESA_mm']:.3f} mm from the new removed region; nearest strap {r['nearest_strap_mm']:.3f} mm, nearest strap screw {r['nearest_fastener_mm']:.3f} mm. TV-to-base clearance remains {r['TV_envelope_clearance_mm']:.3f} mm. Those figures are packaging/section screening, not a structural certification.

The180×110 R8 rear service window, both rear strain slots, dowel, four straps/eight screws, TV/VESA geometry, front button centers Y89/Y127 at local top minus65, and every backbox component remain unchanged. No cabinet crossmember, shelf or front panel moves. Final side-button machining remains PURCHASE_BEFORE_CNC.

## Where the playfield currently rests

The owner’s observation is correct. **The current model has rear support only.** The wooden dowel is seated in both floor-bearing cradles. The round dowel/cradle interface permits rotation and does not set the closed angle. The base itself is not sitting on T1, T2, T3, the front panel or a front pad.

| Current part | Actual relationship to the base |
|---|---|
| Rear dowel / two cradles | Real tangent seating, rear height supported |
| T1 atY380 |22.000 mm normal gap;22.333000518 mm vertical gap at the sameY |
| T2 atY700 |22.000 mm normal gap;22.333000518 mm vertical gap at the sameY |
| T3 atY980 |22.000 mm normal gap;22.333000518 mm vertical gap at the sameY |
| Front panel / lockdown region | No modeled front landing;46.014 mm shortest base-to-front-panel separation |

The22 mm mismatch is traceable: the old T tops were designed for removed monitor rails whose underside was localZ−36. The present plywood base underside is localZ−14. Older V18/V19 documentation mentioned front rests and positive latches, but these objects were already absent from the V32 source before the wooden-dowel replacement. We do not incorrectly attribute their deletion to the dowel commit.

The audit identifies only two moving-assembly/fixed-cabinet contact pairs: dowel-to-left cradle and dowel-to-right cradle. A0.1° downward rotation is free. At0.5°, unintended component interference appears; incidental contact with buttons/electronics is not an acceptable support. The base alone produces a forward gravity moment about the rear axis. Thus pivot friction must not be treated as the missing front support.

Prior service/fold tests validated collision-free CAD trajectories. They did **not** establish a complete closed-position load path. This follow-up makes that distinction explicit in CURRENT metadata, the viewer and both manuals.

## How the completed support should work

A completed design needs **rear dowel support plus two front landing regions**. Equal left/right landing heights prevent roll; their height relative to the dowel establishes the existing9.906669° playing slope. “Level” here means level left-to-right at the intended fore/aft slope, not horizontal.

The simplest isolated option studied here uses two landing shoes on **T1**, bridging the measured22 mm normal gap without moving T1 or changing the rear axis. Load would pass:

`display → VESA/base → front shoes → T1 → its end supports/cabinet sides`

and at the rear:

`base/straps → wooden dowel → cradles → cabinet floor`

T2/T3 can remain clear as removable structural crossmembers. The glass, lockdown bar, button bodies and electronics must not carry playfield weight. T1 is about380 mm from cabinet front, so this option leaves a front overhang requiring stiffness qualification; it is not a support directly under the lockdown bar.

**The shoes are an isolated HELD proposal, not installed CURRENT parts or a BOM addition.** The comparison includes compact pads and a broader captured plywood profile; neither has frozen attachment, fit, soft-pad thickness, load qualification or positive closed uplift retention. Any felt/EPDM thickness must be included within the gap, not added on top to shift the playfield. Finalizing the front landing/retention interface remains an explicit mechanical blocker.

## Manufacturing and validation

Only M025 changes; all100 other manufacturing pieces are preserved exactly. Counts remain **101 permanent wood /97 CNC plywood /4 SW01 /59 families**. M025 reconstruction difference is **0 mm³**. Nominal planning wood mass becomes **{mass['wood_flatpack_kg'][1]:.6f} kg**, down **0.061074 kg**. Four existing preferred packages remain below25 kg at high-density planning. No support-study wood or guessed hardware enters the permanent inventory.

The existing one-face Ø4/R2 supplier rules remain. Rear openings, actual material/coupon holds, SW01/jig, captured shell, M006, M067, WPC, matrix, shelves, T1/T2/T3, fans, doors and glass are preserved.

Clearance/topology regression: **{len(q['checks'])} checks**. Native geometry:16 checks. Playfield/backbox motion:17 checks. Button metrology/access:6 checks. Flexible cable:63 sampled poses. Browser results: see [focused offline QA](browser-validation.json). Passing these tests does not override the failed closed-support gate. The support audit’s successful checks prove the deficiency; `closed_position_support_valid=false`.

[Geometry](geometry-validation.json) · [Motion](motion-validation.json) · [Manufacturing](manufacturing-audit.json) · [Regression](validation.json)

**Release:** CLOSED_POSITION_SUPPORT_BLOCKED and CNC_FULL_SHEET_RELEASE_BLOCKED. Pending closed landing and positive retention, structural qualification, actual production plywood/coupon, purchased hardware and display-specific interfaces. No CAM, G-code or production full-sheet release.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
'''
# Keep prose readable without changing canonical component IDs.
for a,b in [('original500','original 500'),('versus456','versus 456'),('The87','The 87'),('localY','local Y'),('atY','at Y'),('one18','one 18'),('at650','at 650'),('retaining79','retaining 79'),('The180','The 180'),('minus65','minus 65'),('|22.','| 22.'),(';22.','; 22.'),('sameY','same Y'),(';46.','; 46.'),('The22','The 22'),('localZ','local Z'),('A0.1','A 0.1'),('At0.5','At 0.5'),('existing9.9','existing 9.9'),('measured22','measured 22'),('about380','about 380'),('all100','all 100'),('/97','/ 97'),('/4 SW01','/ 4 SW01'),('/59','/ 59'),('below25','below 25'),('geometry:16','geometry: 16'),('motion:17','motion: 17'),('access:6','access: 6'),('cable:63','cable: 63')]:text=text.replace(a,b)
(O/'README.md').write_text(text)
(R/'docs/PLAYFIELD_REST_V3362.md').write_text('# V33.6.2 playfield trim and support audit\n\n[Report](../exports/generated/playfield-rest-v3362/README.md) · [CAD review](../exports/generated/playfield-rest-v3362/review.html) · [Viewer](../exports/generated/viewer-v32/index.html)\n\nOwner-confirmed relief is 52 mm per side, 87 mm long, R8, leaving 396 mm front width. CURRENT closed support is BLOCKED: T1/T2/T3 have a 22 mm normal gap below the base; only rear dowel seating exists. T1 landing shoes remain an isolated proposal. No CNC release.\n')
print('V3362_REPORT_PASS; CLOSED_POSITION_SUPPORT_BLOCKED')

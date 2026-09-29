# Front panel: control layout and closure review

[English](FRONT_PANEL_REVIEW_V32.md) · [Português (Brasil)](pt-BR/FRONT_PANEL_REVIEW_V32.md)

**FRONT_LAYOUT_PROPOSAL — not CNC released.** This is the first step in the owner's requested front → sides → rear → bottom sequence. Source V32 and the forum lighting proposal remain unchanged. [Review image](../exports/generated/front-panel-v32/01-front-review.png) · [Separate CAD](../exports/generated/front-panel-v32/front-layout-proposal.FCStd) · [Saved-solid evidence](../exports/generated/front-panel-v32/validation.json).

## What the supplied photos establish

`414893.jpg` and `414888.jpg` show the same cabinet with a vertical group of three illuminated controls to the left of a central coin door, a mechanical plunger upper right and separate Launch Ball control below. The second view helps distinguish the button faces from the decorative backing. The visible trim/artwork does not establish mounting dimensions, materials or a load path. Left-button labels cannot all be read reliably; Start / Extra Ball / Exit-Back are proposed functions, not transcribed labels.

Use their spatial hierarchy and serviceable separation. Do not copy the themed graphics or trace scaled hole patterns from a perspective screenshot. Neither supplied image is imported into production geometry or redistributed with this study.

## Proposed front arrangement

Coordinates are millimetres, cabinet X left-to-right as seen from the front, Z upward from the cabinet bottom. Y runs front-to-rear. Preserve the 600 mm outside body width and 400.05 mm front height. The existing butt-joint Front remains X18..582, 564 mm wide, nominally 18 mm thick. The separate captured-shell proposal would alter mating edges; that joinery choice is not adopted here.

| Function | Center X | Center Z | Evidence / status |
|---|---:|---:|---|
| Start | 90 | 310 | Visual/ergonomic proposal |
| Extra Ball / assignable | 90 | 260 | Third-button function awaiting owner response |
| Exit / Back | 90 | 210 | Separate from Start; software hold-to-exit can reduce accidental exit |
| Plunger | 520 | 280 | Z300 rejected by provisional body-versus-monitor-rail check |
| Launch Ball | 520 | 210 | Separate digital launch retained below plunger |

The left pitch is 50 mm; the plunger/launch pitch is 70 mm. Visible button diameters 35/50 mm and plunger face 60 × 60 mm are rendering assumptions. Nominal 25.4 mm button holes in the study are **not selected-device cutouts**. No plunger hole is cut. No backing plate, adapter window or permanent part code is added just to match the photographs.

Relative to the published V32 Front, the two left button centers at Z280/230 become three at Z310/260/210, and a right Launch bore is proposed. The plunger reserve moves from Z250 to Z280. Existing button counterbores are omitted because the actual mounting stack is unknown. The four existing coin-door fastener references and rectangular opening are retained exactly.

Keep coin/credit accessible at the coin door (the actual door's switch arrangement must be confirmed); PC power/reset, calibration, volume and independent feedback-disable access belong inside the service area. Button function, color and legends can change without changing panel geometry. No exterior service button bank is introduced.

## Checks that prevent downstream redesign

- **Coin door:** retain the current reference opening X144.425..455.575, Z92.840625..357.159375 (311.15 × 264.31875). Its selected model, flange, hinge sweep, lock/cam, fasteners and mechanism depth are unconfirmed. Do not reuse the smaller v27 coin-door bounding box as fit evidence for this opening.
- **Front shelf:** S1 begins at Y120; the front inner face is Y18. That leaves **102 mm to S1**, before allowing connector bends or hands. Our deliberately conservative coin-access volume extends 140 mm inward and uses a 20 mm flange allowance. It overlaps S1, the display envelope and StarTech. This is a clearance-screening finding, **not proof that a purchased door collides**; a full flange extruded through the entire depth overestimates real hardware occupancy. Measure or obtain actual hardware geometry before choosing whether to adjust S1/removable audio mounting or the door interface. Do not cut the shell around a guessed mechanism.
- **Plunger:** the assumed 40 × 202 × 40 mm body at Z300 intersects MonRailR. Lowering its center to Z280 clears the tested neighbors. Stroke, sensor, cable bends, retaining nut and hand access still require actual dimensions; a clear rectangular proxy is not a completed plunger qualification.
- **Lockdown:** the outer custom bar remains at the top. The Z380..400.05 inner band is a *proposed receiver reservation*, not proven hardware clearance. With the illustrative 20 mm door flange, only 2.84 mm separates its top from this band. Actual receiver/door fastener access must be resolved together before hole release.
- **Leg corners:** real leg brackets, backing, washers and bolt/tool sweeps are not represented by the decorative corner plates in the pictures. They remain an explicit front/side shared gate. No final leg holes or strength claims are made.

## Verification and reproducibility

`freecadcmd tools/front_panel_v32_entry.py` creates a separate document and reopens it. **20 checks pass:** 45 valid single solids, original object identities, only Front and the plunger reservation changed, original front size, preserved door aperture/fasteners, four nominal bores and surrounding wood, plunger datum and intentionally uncut plunger panel. Four negative controls reject a filled Launch bore, oversized Start bore, moved S1 and moved plunger reserve. Three conservative coin-access overlaps remain recorded as open findings. Button and lowered-plunger proxies have no positive-volume overlap with the tested saved neighbors.

`uv run --with numpy --with matplotlib python tools/render_front_panel_v32.py` generates the review view. Inputs are [front layout parameters](../config/front_panel_v32.json) and saved V32 geometry. This is saved-shape/layout validation, not tool-access, load, motion, electrical or manufacturing certification. Physical sessions remain paused.

## Evidence still needed for closure

The available repository contains the earlier V32 dimensional source, HF-019/020/022/030 hardware gates, the v27 control envelopes, the Pinscape assessment and PinSim provenance review. They were considered with their generation boundaries intact. No prior hardware PDF attachment was found in the accessible project/attachment locations in this pass; therefore none is claimed as newly reviewed. Reattach the coin-door, button, plunger and lockdown/leg drawings previously supplied, or identify their accessible paths. A missing drawing does not become a measured dimension.

For final closure: confirm the visible functions; establish the exact door and controls' mounting/service envelopes; resolve S1/door/display access, leg corner and receiver interfaces; then approve one original parametric hole set with measured stock/tool/coupon evidence. Only then freeze Front and propagate its shared interfaces to the sides. See [ordered panel closure plan](PANEL_CLOSURE_V32.md).

External context: the [Pinscape corner-brace discussion](https://mjrnet.org/pinscape/BuildGuideV2/BuildGuide.php?sid=cornerBraceCutting) identifies interference between tall front corner reinforcement and front controls; its workshop cutting recipe is not adopted. [Arnoz POTAR](https://shop.arnoz.com/en/plunger/44-potar.html) describes a sensor product, not the full mechanical shooter mounting interface. Neither page supplies a selected front-panel drilling template here.

Original project material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

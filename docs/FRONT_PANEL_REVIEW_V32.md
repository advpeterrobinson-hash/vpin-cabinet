# Front panel: illuminated door and optional working coins

[English](FRONT_PANEL_REVIEW_V32.md) · [Português (Brasil)](pt-BR/FRONT_PANEL_REVIEW_V32.md)

**Implemented study; actual hardware fit UNVERIFIED; CNC BLOCKED.** The owner-approved direction is an outward-opening illuminated coin door, coin-return buttons for credits, and optional two working mechanisms with a compact removable collection tray. No full arcade cashbox is required. This implements the first stage of front → sides → rear → bottom; it does not release permanent panel machining.

![Basic door and optional mechanism configuration](../exports/generated/front-panel-v32/02-coin-door-configurations.png)

![Outward movement and separate internal hardware depth](../exports/generated/front-panel-v32/03-coin-door-clearances.png)

## Corrected spatial model

The previous 140 mm inward extrusion of the entire coin-door outline is **retired**. It was neither a door swing nor measured hardware. Its S1/display/StarTech overlaps are withdrawn as actual-fit evidence. Those three components and all original V32 source geometry remain unchanged.

The new study represents the frame, leaf, two illuminated return-button bodies, internal light/switch bodies, lock, optional mechanisms and their mounting tabs, tray and two local tray-support brackets separately. It distinguishes:

1. Closed-door component occupancy.
2. Outward movement of the leaf **and everything attached to it**.
3. Tray withdrawal and a separate access probe through the open doorway.

Default build omits mechanisms, tabs, tray and tray supports. Upgrading adds removable door-mounted components and front-supported tray hardware using the same permanent coin-door opening. This is an upgrade architecture proposal, not a claim that arbitrary mechanisms fit. Retention and mounting details remain unqualified; no new support holes are released.

## Explicit candidate dimensions

All dimensions below are design study choices, **not manufacturer or measured hardware dimensions**. X grows left-to-right viewed from the front, Y toward the rear, Z upward from cabinet bottom; units mm.

| Element | Candidate definition |
|---|---|
| Existing coin opening | X144.425..455.575, Z92.840625..357.159375; 311.15 × 264.31875; existing reference fasteners retained |
| Frame | 20 mm outward flange allowance, 3 mm front thickness; not a full-depth box |
| Leaf | X146, Y−4, Z94; 308 × 3 × 261 |
| Hinge/sweep | Left viewed from front; vertical axis X146/Y−4; outward to 110°, checked every 1° |
| Light/switch bodies | Two 30 × 29 × 22 boxes; separate from mechanisms |
| Lock body | 18 × 36 × 22 box; actual cam and key operation still unverified |
| Mechanism reservations | Two 45 × 95 × 135 boxes at X310/370, Y8, Z170; attached to door through local removable mounting-tab concepts |
| Collection tray | 115 × 80 × 25 outer size; 2 mm candidate walls; X305/Y25/Z115; removable; no full arcade cashbox |
| Tray supports | Two small bent-bracket envelopes seated at Z115 and anchored in the lower front region; detailed fixings and positive retention pending |
| Tray withdrawal | Straight 180 mm toward the player, checked every 5 mm with door open |
| Access probe | 80 × 180 × 65 at X210/Y−100/Z210; proves only this candidate corridor, not unrestricted human/tool access |

Mechanism reservations end at Y103; S1 begins at Y120: **17 mm to its leading plane in this candidate**. That is not verified wiring or hand clearance. Two candidate coin-drop corridors terminate within the tray; actual accept/reject outlets and coin trajectories need hardware evidence. The supplied Pinscape guide supports separate optional mechanisms, return-button credit switches and a compact collector; it does not supply these study dimensions.

No current manufacturer drawing establishes the selected door or mechanism fit. Retrieval of the located SUZOHAPP `40-0696-30 B` PDF timed out; no dimensions were adopted and no vendor document was imported. The user-supplied Pinscape MHTML was read, with its hash recorded in the configuration. No proprietary drawings or photo artwork were copied.

## Front controls preserved

The photo-inspired proposal remains Start X90/Z310, Extra Ball X90/Z260, Exit/Back X90/Z210; plunger X520/Z280; Launch Ball X520/Z210. Left-button function/legends remain proposed. Nominal 25.4 mm button bores and visual face sizes are not final hardware specifications. The plunger opening is not cut. Z300 was rejected using the provisional plunger body; Z280 clears the tested neighbors. Coin/credit uses the door return buttons; PC power/reset, calibration, volume and independent feedback-disable access remain inside the service area.

The custom lockdown remains at the front top. Its actual receiver, leg brackets, hinge/lock selection, complete plunger stroke/cabling, button nuts/tools and measured door fasteners remain shared interface gates. The 600 mm body and 564 × 400.05 × 18 nominal Front are unchanged. The captured-shell joinery proposal is still separate.

## Evidence and reproduction

Run `bash tools/run_front_panel_v32.sh`. It builds/reopens the study CAD, requires success sentinels (FreeCAD may exit zero after Python exceptions), then renders the views. Geometry source remains [V32](../exports/generated/cabinet-v32/README.md); parameters are in `config/front_panel_v32.json`.

- [Base front proposal](../exports/generated/front-panel-v32/front-layout-proposal.FCStd): 20 saved-solid checks and four original negative controls.
- [Basic closed](../exports/generated/front-panel-v32/coin-basic-closed.FCStd), [upgrade closed](../exports/generated/front-panel-v32/coin-upgrade-closed.FCStd), [upgrade open](../exports/generated/front-panel-v32/coin-upgrade-open.FCStd): reopened and checked for solid validity, exact component sets/shapes, preserved 45 original study objects and component collisions.
- [Coin-door evidence](../exports/generated/front-panel-v32/coin-door-validation.json): basic/upgrade outward sampled sweeps, tray withdrawal, candidate access and coin-drop checks. Four additional negative controls reject inward motion, an interfering mechanism envelope, a blocked tray path and a serialized inward-open leaf.
- Renders use tessellated **saved component solids**, not a separate hand-drawn hardware model. [Front overview](../exports/generated/front-panel-v32/01-front-review.png).

Candidate checks report PASS or FAIL. Actual hardware fit, harness flex, real leg/receiver clearances, support/retainer strength, real outlet paths, full human access and motion between samples remain **UNVERIFIED**. A passing candidate does not turn missing evidence into verified fit. Physical sessions remain paused.

## Handoff to subsequent panels

The front layout and optional-upgrade architecture are implemented for review; permanent machining remains open. Carry these shared boundaries into [sides → rear → bottom](PANEL_CLOSURE_V32.md). Do not move S1, recut the shell, or reserve a full cashbox based on the retired prism. If selected hardware exceeds a candidate reservation, report the specific conflict and propose a localized removable-interface revision before changing permanent structure.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

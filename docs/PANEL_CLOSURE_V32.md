# V32 panel closure sequence

[English](PANEL_CLOSURE_V32.md) · [Português (Brasil)](pt-BR/PANEL_CLOSURE_V32.md)

Owner order: **Front → SideL/SideR → Rear/RearDoor → Floor**. The objective is to close shared interfaces once and keep component-specific changes on replaceable parts. A visually accepted layout and a measured CNC-ready interface are separate decisions. No panel is declared finally frozen in this pass.

| Stage | Existing V32 geometry carried forward | Close before advancing to manufacturing detail | Downstream dependency |
|---|---|---|---|
| 1 Front | 600 mm body, front height 400.05; 564 × 400.05 × 18 panel; central reference door | Photo-inspired control positions; actual door/flange/sweep; button mounting stacks; plunger complete motion/body; custom lockdown receiver; front leg corner; S1/audio/display access | Side leg datum, top glass/lockdown datum, front floor capture and service routing |
| 2 Sides | Length 1308.1; heights 400.05/596.9; rear flat 180.975; 18 mm nominal; existing paired button centers Y255/310 Z270 | Actual flipper/secondary-button bodies and SSF zones; leg bracket and fastener access; display/prop/hinge loads; glass channels; accepted joinery; backbox pivot | Preserve display parallel to glass and full replacement envelope; no geometry inferred from photo corner plates |
| 3 Rear + door | 600 mm body; rear height 596.9; reference access 340 × 293 at X130 Z72; two fan centers X230/370 Z280 | Selected fans/guards and removable harness; door fasteners/retention/access; backbox hinge sweep; compact mains and Ethernet; PC service architecture discrepancy | Rear/floor ventilation, cable path, rear leg and backbox load zones; no permanent HDMI/USB fascia |
| 4 Floor | Existing 18 mm panel at Z18; subwoofer reference opening 139.7 mm at X300 Y440; intake 100 × 160 at X400 Y630; four 28 mm auxiliary holes at Y90 | Justify each aperture against actual equipment, mounts, enclosure, air path, SSF and load paths; decide function or removal of unassigned auxiliary holes; optional undercabinet LED mounts; leg/skate clearances | Final capture/joint topology, sheet nesting, tool relief, screw access and assembly sequence |

The existing V32 side pivot reference Y1270/Z508 and rear fan reference 116 mm cutouts / 105 mm mounting pitch are **not universal hardware standards or released holes**. Retain them as documented references until selected hardware confirms them.

## Change boundaries

Keep cabinet datums in the permanent shell. Prefer replaceable display adapters, fan guards/carriers, electronics mounting boards and connector carriers for component-specific holes. An adapter cannot compensate for an undersized permanent opening, obstructed service path or missing structural load path: prove those first. Do not add carrier windows or delete reinforcement merely to avoid making the measurements.

The captured-shell joinery proposal remains separate. It changes front/floor/rear mating widths and must be decided before final panel outlines. Preserve part IDs; record each accepted revision and the exact surfaces/holes it changes.

## Current handoff

The [front proposal](FRONT_PANEL_REVIEW_V32.md) now separates the outward leaf and attached hardware, default illuminated door, optional two mechanisms and removable compact tray. Saved geometry, sampled motion and negative controls pass for the explicit candidate envelopes. The old 140 mm full-door prism is retired; its overlaps do not justify moving S1/display/audio. Actual hardware and shared interfaces remain UNVERIFIED. The side audit now verifies saved symmetry, bores and mounting webs and screens provisional button envelopes; no side cuts have changed. Rear/floor remain a dependency queue, not completed new geometry. Forum review of the playfield/LED proposal can continue independently, but the glass/lockdown and front service interfaces must eventually use the same accepted datums.

Release requires measured stock, selected tool diameter, clearances and relief, nesting/orientation, physical tolerance coupon, assembly/access evidence and owner manufacturing approval. Physical sessions remain paused. **CNC BLOCKED.**

Current continuation: [side-panel audit](SIDE_PANEL_REVIEW_V32.md) and [session handoff](SESSION_HANDOFF_V32.md).

Side interface development now has a [datum, occupied-support and load/service plan](SIDE_INTERFACE_PLAN_V32.md). Its button-stack alternatives and mounting paths remain proposals; no side machining is frozen.

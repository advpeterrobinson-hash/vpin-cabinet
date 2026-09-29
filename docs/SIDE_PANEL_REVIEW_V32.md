# V32 side-panel interface audit

[Português (Brasil)](pt-BR/SIDE_PANEL_REVIEW_V32.md) · [Session handoff](SESSION_HANDOFF_V32.md)

Read-only audit of the saved V32 solids; **hardware fit UNVERIFIED; CNC BLOCKED**. Front-panel choices remain in the separate front study. No permanent panel was recut in this audit.

Owner now prefers [traditional leaf pinball buttons](SIDE_BUTTON_OPTIONS_V32.md); retain a separately specified arcade option for other builders. The linked kit is a hardware reference, not yet a verified mounting stack.

The owner-supplied [dimension reference](CABINET_DIMENSIONS_REFERENCE_V32.md) adds a side-button discrepancy: its printed Ø1.12 inch bore is approximately Ø28.448 mm, unlike the saved Ø15.875 through-hole. Review hardware and datums before changing cuts.

| Interface | Saved geometry / result | Required before release |
|---|---|---|
| Side pair | Mirrored across X300; 18 mm thick, 1308.1 mm long; front/rear heights 400.05/596.9 mm from source | Measured stock and accepted captured-shell joinery |
| Two buttons per side | Y255/310, Z270; 55 mm pitch; through bore Ø15.875 | Selected button barrel, thread, nut and washer stack; these are not the front's nominal Ø25.4 bores |
| Button recesses | Ø28.575; outside depth 7.9375; inside depth 4.7625; remaining annular web **5.3 mm** | Verify clamp engagement and local strength in selected plywood; no automatic deeper pocket or larger bore |
| Candidate inward space | Radius 18 mm × 80 mm inward: assumed 60 mm body +20 mm cable | Actual switches, connectors, bend radius and hand access; no collision with currently modeled neighboring solids |
| Backbox pivot reference | Ø12.7 at Y1270/Z508; rear/top edge ligaments 31.75/82.55 mm | Actual pivot, washers, reinforcement, sweep and fastener access |
| Legs, feedback, display props, glass | Interfaces remain unresolved | Shared load paths, mounting hardware, service travel and assembly sequence |

The 5.3 mm web is the local annulus between two button counterbores, not an OLED side pocket. It is a measured property of the saved nominal model, not a structural approval. The candidate button space is a screening assumption, not a purchased-component specification. Missing leg/SSF/prop hardware is not covered by a collision pass.

`tools/side_panel_v32_entry.py` opens the original FCStd without saving it, tests the saved bores, both recesses and retained webs, compares reflected solids, and confirms unchanged file bytes. A 1 mm shifted-side negative control must fail the symmetry comparison. Output: [validation.json](../exports/generated/side-panel-v32/validation.json), **46 passing checks including the negative control; zero candidate-envelope collisions**.

Run from the V32 worktree:

```sh
freecadcmd tools/side_panel_v32_entry.py > /tmp/v32-side-review.log 2>&1
rg 'SIDE_REVIEW_PASS' /tmp/v32-side-review.log
```

FreeCADCmd can return zero after Python exceptions; require the pass sentinel and inspect the report. Next: resolve leg corner/lockdown datums with the front, then define SSF mounting and captive-prop/hinge service zones before changing side holes. Rear and floor follow the [panel closure sequence](PANEL_CLOSURE_V32.md).

## Hardware and service continuation

The [side interface plan](SIDE_INTERFACE_PLAN_V32.md) records shared datums, seven paired occupied support footprints, button-stack alternatives and proposed load/service paths for legs, glass, display props and feedback. The audit now additionally checks seven support mirror pairs and fourteen inner-face datums. These are packaging facts; hardware access and structural performance remain unverified.

The separate [guide-anchor service screen](SIDE_SERVICE_REVIEW_V32.md) now evaluates 24 anchors with two provisional tools in three removal states. It exposes rail/crossmember access obstructions; its passing audit sentinel does not certify every service route as clear.

The [continuous removal study](SIDE_MOTION_REVIEW_V32.md) adds shelf and crossmember paths, candidate 60 mm payload envelopes and reopened CAD service poses. Run all three side audits with `bash tools/run_side_review_v32.sh`.

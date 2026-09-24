# Owner completeness pass — validation record

2026-09-24, branch `feat/active-build-cleanup-v25`. Manufacturing ready remains **false**.

## State and history

Inspected local status and history before changing source. Local engineering HEAD was `a0ac7474498710cb45a1c2f8491f3fe9227055e5`; fetch found the published engineering tip `98d8adb`. Fast-forwarded to that tip, then merged `origin/main` (`2e2b499`) normally in merge commit `5d85d29`. Community documentation and CERN-OHL-S-2.0 notices retained. No rebase, force push or engineering merge to main.

Pre-existing modified `cad/master/vpin-master.FCStd` and deleted `cad/master/vpin-master.20260914-181346.FCBak` were left outside this work's commits. The active model is generated from source at `cad/active/vpin-active.FCStd`.

## Executed checks

- `make validate`: all current Python validators pass, including owner configuration and CNC ledger reconciliation.
- `make cnc-detail`: fresh FreeCADCmd active generation; reopened saved geometry; fresh structural joint preview; reopened saved preview; regenerated measurement/CNC ledgers; all negative controls; review render. Success sentinels checked because FreeCADCmd may return zero after a Python exception.
- 12 original active saved-file negative controls, 3 joint-detail negative controls, 6 CNC ledger negative controls, 7 owner configuration negative controls and 12 owner saved-file negative controls: **40 distinct intentional failures rejected**.
- Final `make build-current` repeated after a review-only airflow-route correction so arrows pass through the actual paired openings; no structural dimensions changed after the full negative suite.
- Gallery inspected as a contact sheet plus full-size exterior, carriers, props, rear door and panel-map views. Whole-object rendering occlusion corrected by sorting triangles together. Superseded active-renderer PNGs removed from the generated gallery.
- `git diff --check` and staged whitespace check required before commits.

Detailed local evidence is in `.work/logs/final-full.log`, `active-validation.log`, `active-build.log`, `active-geometry.log`, `cnc-detail-saved.log`, `active-negative.log`, `cnc-detail-negative.log`, `owner-negative.log`, and `final-gallery-build.log`. These generated logs are not tracked source.

## Reconciled result

32 wood assembly records: **29 permanent structural**, 2 removable doors, 1 replaceable CPU board. 11 separately registered carrier pieces include that CPU board; do not double-count it in a combined BOM. Seven carriers are new. 68 structural joint records (65 contacts and 3 internal laminations). **232 CNC feature groups: 173 defined, 59 hardware-blocked, 0 design-only blocked**. No blocked hardware pattern contains guessed coordinates.

600 mm body; CPU shelf Z135; hatch Z110..350; 105-degree outward CPU door; compact mains and optional Ethernet; no rear HDMI/USB bank, CPU harness ghost, old sled/wheels/bulky leg furniture, gas hardware or broad electronics shelf. Current nominal rear rail/bracket gap remains 13.8 mm versus the 15 mm planning reserve and awaits physical stacks.

The joint preview reports valid wood solids, zero wood overlaps and all contacts accounted. Owner checks cover solid SSF skin, exact generic intake cuts and mounting holes, carrier/CPU/central clearance, button/plunger packaging, blocked bores, both positively pinned props, receiver contact, pin/keeper capture, sampled prop deployment and outward backbox door sweep. Samples are discrete (props 2 degrees, door 1 degree), not a continuous tolerance/collision proof.

## Limits and physical gates

The old prop location had a real deployment collision despite clear endpoints. Forward anchors and outboard straight rods resolve the sampled nominal collision, allowing combined landing/prop reinforcement. Actual rod play, coatings, end geometry and narrow corridor tolerances remain unmeasured. Each prop must independently support the full assembly in a physical proof fixture. The 8 mm candidate has no certified capacity claim.

Manual effort estimate is 86.1 N peak under a 16.5 kg uniform-component assumption, excluding friction/handling margin. Measure actual force and ergonomics. The 520 mm rear door does not admit a 740 mm display flat: full display replacement uses the removable front bezel route. No thermal performance or structural load certification is claimed.

Measured stock/tooling/coupon, purchased-interface measurements, local metal drawings, final fasteners/reliefs/nesting/laminate IDs, dry fit, access/fold review, CPU and individual prop proof tests, manual effort and commissioning remain release gates. See [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md) and [HARDWARE_MEASUREMENT_PACK_V25.md](HARDWARE_MEASUREMENT_PACK_V25.md).

# CNC-detail validation — 2026-09-24

Starting remote checkpoint: `628807c72d3f8aef459a3ec4eb392c5abdc3a25e` on `feat/active-build-cleanup-v25`. Hardware pack milestone: `1e33dda`.

## Commands and outcomes

- `make cnc-detail`: PASS after fixing FreeCADCmd entry-point invocation and newline-delimited success sentinels. Runs fresh source generation, active saved-solid checks, detail generation, ledger regeneration, detail saved-solid checks, active/detail negative controls and gallery rendering. The shell fails if a success sentinel is missing even when FreeCADCmd exits zero.
- `make validate`: PASS, including the new CNC register validator.
- New Python modules compile: PASS.
- `git diff --check`: PASS.
- Gallery inspection: exploded structure, pivot/safety envelope and per-part feature status inspected. Labels were revised to overlay numbered wood/hardware identifiers; full ID legends are in the gallery.

## Evidence

- Baseline source still produces 600 mm body, 36 wood records, CPU shelf Z135, rear opening Z110..350, outward 105° CPU door, selected compact mains and optional Ethernet. Rear HDMI/USB, CPU harness, historical sled/wheels and bulky corner wood remain absent.
- Joint preview reopens with 36 valid connected wood solids and zero positive-volume wood/wood intersections. 73 baseline wood contact pairs reconcile exactly with the connection ledger; three internal laminations bring the ledger to 76 entries.
- Nominal primary sides retain at least 12 mm skin beneath captures. Rear side ligaments remain at least 118 mm; hatch-to-bottom-capture ligament is 74 mm; rail web over the crossmember is at least 55.5 mm. These are geometric checks, not strength calculations.
- CPU wood is geometrically unchanged from baseline. Both rail/bracket minimum distances remain 13.8 mm and no bracket interference is introduced. The 15 mm planning reserve is not misreported as satisfied.
- Feature register: 201 groups = 137 defined recipes (101 geometry groups plus 36 marking instructions), 60 hardware-blocked groups and four design-blocked groups. Every wood record has a profile and identity instruction. Blocked hardware coordinates/diameters/depths are empty.
- Five ledger mutants rejected: guessed coordinate, false hardware release, omitted wood part, unknown joint member, omitted hardware pattern.
- Three detail mutants rejected: restored wood overlap, displaced rail, omitted contact record.
- Twelve active-model mutants rejected: large utility cut, restored underside utility, inward door, raised shelf, restored CPU harness, raised door, bottom-joint cut, leg-zone cut, lost mains/signal spacing, incorrect wood ID, restored rear USB and floating rail.

Generated evidence is under `exports/generated/active-geometry-report.json`, `exports/generated/rear-utility-study.json`, `exports/generated/cnc-detail/geometry.json`, and `.work/logs/`. Recreate it with `make cnc-detail`; generated FCStd/meshes/PNGs are intentionally not checked into Git.

## Limits

The detail model is separate from the active packaging master and is not a production model. Its booleans do not certify load capacity, physical assembly, hardware fit, fastener design, cutter access or tolerance. Stock/tool/clearance fields remain unmeasured. The old builders require coordinated stock migration before measured-stock production regeneration; the detail generator refuses to quietly treat a nominal preview as that migration. Remaining release work is listed in the measurement pack and structure audit. Manufacturing-ready remains false.

Owner's pre-existing historical master modification and backup deletion were excluded from both commits. Reference models were not edited. No merge or force push is part of this work.

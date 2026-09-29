# V32 guide-anchor service screen

**Candidate tool access; not hardware approval. CNC BLOCKED.** No source geometry changed.

The [side interface plan](SIDE_INTERFACE_PLAN_V32.md) requires access to removable supports. This screen checks the four existing side-anchor bores in each of six T guides: **24 positions**, separately from the six support-height bores in each guide. The axes are confirmed against the saved Ø5.5 mm bores. Permanent side-panel anchor holes and actual fasteners are not yet defined.

## Assumed tool space and results

Two straight cylinders start at the inward guide face, X36 on the left or X564 on the right, and extend toward the cabinet center. The compact probe is Ø16 × 100 mm; the larger probe is Ø30 × 150 mm. These are explicit screening choices, not dimensions of purchased tools. A positive-volume overlap above 0.01 mm³ counts as an obstruction.

| State | Compact: obstructed / tested | Larger: obstructed / tested | Obstacles |
|---|---:|---:|---|
| All saved objects present | 6 / 24 | 24 / 24 | Monitor rails for compact; rails and crossmembers for larger |
| Display envelope, both monitor rails and bridge removed | 0 / 24 | 24 / 24 | Crossmembers for larger |
| Those four objects plus T1/T2/T3 removed | 0 / 24 | 0 / 24 | None among retained modeled objects |

The six compact obstructions are the **upper, forward anchor of every guide**: Y = guide center −22; Z = guide bottom +120. Both sides produce the same result. The lower row is guide bottom +65; the rearward column is center +22.

A clear cylinder proves only that particular axial space against retained saved solids. The audit does not model screw heads, sockets, hands, tool insertion, fastener withdrawal, cables, or missing leg/prop/feedback hardware. It does not demonstrate that the listed removals can actually be performed safely.

## Consequence for the interface

Keep guide anchors serviceable **after removal of the monitor assembly** as the current development target. With a larger tool, the crossmembers also need removal in this screen. The eventual assembly guide must specify real tools and accessible retention for each prerequisite removal. Reject a fastening scheme that requires removing a guide before the monitor or crossmember that blocks that guide can be released.

Do not enlarge the guide or relocate holes solely to clear the larger probe. Existing column axes are 22 mm from the crossmember center, while the crossmember has nominal half-thickness 9 mm: the probe has only 13 mm radial room toward the crossmember. A radius-15 probe therefore overlaps it. Moving the column outward also reduces material toward the guide's 30 mm half-width, so any relocation needs actual fastener edge-distance and load review. Neither candidate tool is selected by this study.

The next fastening detail should compare a real slim driver/extension against the compact probe, define heads/washers and engagement, and prove removal of the monitor assembly without relying on these blocked guide screws. Captive props and receivers must not obstruct the required route. No prop/load design is certified by temporarily omitting display solids from the collision set.

## Reproduction and evidence

Run from the V32 worktree:

```sh
freecadcmd tools/side_service_v32_entry.py > /tmp/v32-side-service.log 2>&1
rg 'SIDE_SERVICE_PASS' /tmp/v32-side-service.log
```

Require the sentinel; FreeCADCmd can exit zero after Python exceptions. The [report](../exports/generated/side-panel-v32/service-validation.json) contains 144 individual tool/state results, including obstacle identities and intersection volumes, and 29 passing audit checks. Checks include all 24 saved bores, the expected solid count, complete matrix count, unchanged source bytes, an injected obstruction detected through the collision routine, and its translated clear control. Passing audit checks do **not** mean all tool paths passed.

Parameters and explicitly removed objects are in `config/side_service_v32.json`. Source FCStd SHA256 remains `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`. The earlier 46-check side audit remains separate evidence.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

## Continuous movement follow-up

The [continuous removal study](SIDE_MOTION_REVIEW_V32.md) now checks monitor teardown, crossmember extraction and staged shelf removal. It establishes modeled translation paths for the previously assumed removed states, while actual release hardware and safe handling remain unverified.

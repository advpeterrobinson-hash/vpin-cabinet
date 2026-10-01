# Current V32 playfield pivot — final owner correction

Only the playfield pivot changed. The former steel axis, bushes, pins, plywood props, washers/nuts and rail/bridge cradle are absent from the CURRENT model. Historical source CAD and old reports remain historical inputs, not current architecture. Only prior pivot holes in the sides were filled; all non-playfield subsystem solids were compared and preserved exactly.

Current CAD: `exports/generated/wood-dowel-pivot-v32/play.FCStd` and `current-v32.step`. Service, lift-out and mechanism-only exploded FCStd files are beside them. Current viewer: `exports/generated/viewer-v32/index.html`. Rebuild: `bash tools/run_service_correction_v32.sh`; review images: `uv run --with matplotlib python tools/render_wood_dowel_pivot_v32.py`.

The playfield has one flat 500 × 1020 × 18 mm plywood base, TV service envelope and direct VESA mounting envelope. One Ø32 × 560 mm wooden dowel is attached beneath the base with exactly four commercial saddle/pipe straps, two near each side, and eight strap screws. Strap envelopes are original schematic geometry, not an imported or selected vendor part. Actual purchased straps and screw dimensions must be measured before machining their base locations.

Two identical 18 mm plywood supports stand directly on the cabinet floor at Z36 and against the inner side faces. Their top seats are open upward; no closed bearing holes, side-through bolts or retention hardware. The U seats have 0.5 mm radial clearance, their centres 0.5 mm above the shaft axis so gravity seats the wooden dowel at the bottom. Both are CNC-cut flat profiles from the same nominal stock. No additional pivot hardware is allowed.

Dimensions are explicit provisional design decisions in `config/wood_dowel_pivot_v32.json`. The dowel has a live spreadsheet diameter expression in saved CAD; regeneration from the config updates matching supports and straps. Coordinates use X left-right, Y front-rear, Z vertical.

Dowel axis: (300, 1035.251, 484.220) mm. Support origins: (18, 1023.251, 36) and (564, 1023.251, 36) mm. Each support is 18 × 24 × 472.220 mm before its open seat cut. Shaft seat positions: (27, 1035.251, 484.220) and (573, 1035.251, 484.220) mm.

PLAY is the inherited 9.907° slope. SERVICE lifts the front by a 50° rotation about the wooden dowel; no props, gas struts, linkage or stop hardware. This is a manually held inspection pose, not a claim of self-support. Higher rear-axis service angles intersect the existing conservative backbox envelope, so no higher angle is claimed. The cabinet/backbox were not altered.

LIFT-OUT is a separate extraction route from PLAY after removing glass/releasing lockdown: elevate the entire base + TV + VESA + dowel + four straps by 42 mm. The dowel then clears both open seats by 2 mm, with 2 mm axial clearance to each cabinet side. No cabinet screws are removed. Take the released unit forward out of the cabinet; do not continue lifting its rear overhang vertically through the backbox envelope. The viewer explicitly shows the vertical unseating step, not a full room/handling simulation.

Validation: all 10 recorded checks pass, including 2° opening samples through 50°, 2 mm lift samples through 42 mm, support-to-fixed-cabinet checks, valid solids, saved-CAD recompute/equivalence and exact preservation of all other subsystem solids. These are geometric checks, not structural/load proof or manufacturing approval. The parameterized nominal dowel/wood dimensions and commercial strap envelopes remain provisional. The owner final architecture supersedes historical prop requirements for this task.

Review images: `exports/generated/wood-dowel-pivot-v32/01-side-close.png` and `02-exploded.png`. Only requested mechanism pieces appear in the exploded review.

PLAYFIELD PIVOT CUSTOM METAL PARTS: 0
PLAYFIELD PIVOT BEARINGS: 0
PLAYFIELD PIVOT BUSHINGS: 0
PLAYFIELD PIVOT STEEL RODS: 0
PLAYFIELD PIVOT WOOD DOWELS: 1
PLAYFIELD PIVOT CNC WOOD SUPPORTS: 2
PLAYFIELD BASE PLYWOOD PANELS: 1
COMMERCIAL STRAPS: 4

STRAP SCREWS: 8
TOTAL COMMERCIAL METAL ITEMS: 12 (4 straps + 8 screws)
No other playfield pivot/support hardware is allowed.

CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

# V32 removable shelf-retention proposal

> Historical complexity study, superseded for current shelf service by [simple top release](SIMPLE_SHELVES_V32.md). Preserve evidence; do not resume this mechanism by default.

[Português (Brasil)](pt-BR/SHELF_RETENTION_REVIEW_V32.md)

**Separate modeled proposal; original V32 unchanged. 106 checks pass. CNC BLOCKED.** This adds a candidate way to clamp each shelf positively, release it from above and preserve the [horizontal-first removal routes](SIDE_MOTION_REVIEW_V32.md).

![Shelf retention study](../exports/generated/side-panel-v32/05-shelf-retention.png)

## What changes in the proposal

- S1/S2/S3 retain their 560 ×150 ×12 mm outlines and installed positions. Each gets four nominal Ø5.5 mm through bores.
- S1SupL/R, S2SupL/R and S3SupL/R retain their height, length and side-wall datum. Their width increases from 18 to **42 mm**, adding 24 mm inward locally. They remain separate local supports, not a new cross-cabinet brace. Their permanent part codes are preserved.
- Twelve square-nut pockets open on the underside of the six replaceable supports. Six nut covers retain the nuts. Their accepted functional codes are S1NutCoverL/R through S3NutCoverL/R; dimensions and fixings remain provisional.
- The 60 mm equipment envelope has four Ø20 mm tool-access wells per shelf. These are layout exclusions for equipment and wiring, **not Ø20 holes in the shelf**.
- No SideL, SideR, Front, Rear or Floor shape is changed by this proposal. The existing guide hardware and source model remain unchanged. Support-to-side anchorage is still unresolved; this study details shelf clamping, not the complete load path into the side wall.

Bolt axes are X48/552. Their Y offsets from each shelf's front edge are 25/100 mm: S1 Y145/220; S2 Y625/700; S3 Y1106/1180. Nominal wood ligaments from the Ø5.5 bore are at least 22.25 mm to a shelf edge and 9.25 mm to the support's side edge. These are geometric distances, not approved structural edge distances.

## Candidate fastening stack

Every dimension below is an explicit design-study choice, **not a manufacturer specification or purchase list**. Threads and screw-drive profiles are not modeled.

| Item | Quantity | Candidate envelope |
|---|---:|---|
| Shelf screw | 12 | Ø5 ×35 mm shaft; Ø9 ×4 mm head |
| Top washer | 12 | Ø12 ×1 mm; Ø5.5 hole |
| Captured square nut | 12 | 10 ×10 ×5 mm; nominal Ø5 thread envelope |
| Nut pocket | 12 | 10.4 ×10.4 ×5.2 mm, opening at support underside |
| Nut cover | 6 | 42 ×150 ×3 mm, two Ø6 bolt-tip passages |
| Cover attachment locations | 24 | Four Ø3 locations per cover; support blind depth 9 mm; actual screws not modeled |

The pocket restrains the nut against rotation and the cover intercepts a nut moving downward after screw removal. Tests rotate each nut 45° into the pocket wall and lower it 1 mm into the cover to confirm those geometric stops. This does not rate the thin cover, wood, fasteners or pocket against service loads. Positive clamping and vibration retention depend on actual threads, torque and selected hardware.

Square pocket corners require a selected cutter and a compatible relief strategy or appropriately shaped nut pocket. Do not release the square internal corners as CNC-ready. Confirm actual nut dimensions, stock thickness, pilot/clearance strategy, cover material and machining setup with the shop. All practical bores/pockets should be CNC-located; no precision freehand layout is intended for the builder.

## Access and removal evidence

With monitor assembly and T1/T2/T3 removed as in the earlier teardown study:

- All 12 top positions clear a candidate Ø16 ×100 mm axial driver probe through their equipment wells.
- Each screw and washer has a clear 40 mm upward withdrawal path; every screw tip finishes above its shelf.
- After all four screws and washers on a shelf are removed, its loaded horizontal-first route remains clear with the wider supports, covers and nuts retained. Other shelves, payloads and their fastening stacks remain present.
- Leaving a screw installed produces an intersection after only 1 mm of shelf translation, confirming a positive geometric stop. This is a negative control, not a force test.

For underside maintenance, all 24 cover locations clear a candidate Ø10 ×80 mm downward driver probe, with a 2 mm allowance for a head below the cover. The actual cover screws are absent, so head fit, engagement, withdrawal and full hand/tool insertion remain unverified. Normal shelf removal leaves these covers installed. Support the nuts and remove the shelf screws before opening a cover.

Shelf/payload paths use conservative continuous swept bounding boxes: the shelf drill holes and equipment wells are filled for this motion screen, so they cannot create false clearance. Screw/washer withdrawal uses continuous coaxial cylindrical/annular sweeps; a whole-head bounding box would incorrectly fill material around the smaller shaft bore. Neither test simulates applied loads or the helical unscrewing motion.

## Rejected first layout

A first candidate with narrower 36 mm supports and bolt X42/558, Y offsets25/125 had access conflicts: S1's rear driver hit the candidate Y255 side-button body; S2's rear driver hit T2Guide. The adopted study uses 42 mm supports, X48/552 and offsets25/100. The two original left-side conflicts remain executable controls against the saved obstacles; final access is checked on both sides.

Removing the equipment-access wells is also a failing control: the filled payload obstructs the driver. Equipment layout must honor those wells; it cannot consume the whole original rectangular volume.

## Files and validation

- [Saved retention proposal](../exports/generated/side-panel-v32/shelf-retention-proposal.FCStd): 114 valid single solids, including candidate hardware and occupancy volumes; **not 114 manufactured parts**.
- [Validation report](../exports/generated/side-panel-v32/retention-validation.json): 106 passing checks, axes, rejected layouts, top/bottom access, withdrawal and released routes.
- Parameters: `config/shelf_retention_v32.json`; source: `tools/shelf_retention_v32_entry.py`.

The saved proposal is reopened and compared by exact object set and shape. Only three shelves, six supports and three equipment-envelope shapes change relative to the reconstructed installed study scene. Source V32, front/motion evidence and input files remain byte-identical; hashes are recorded. The V32 source hash remains `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`.

Run from the V32 worktree:

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_shelf_retention_v32.py
```

The unified runner now includes the retention study after the three existing side audits, requiring each pass sentinel. Direct execution is `freecadcmd tools/shelf_retention_v32_entry.py`; require `SHELF_RETENTION_PASS` rather than trusting the FreeCAD exit code. It consumes the current verified motion report and S1 service pose, rejecting stale inputs. The diagram is schematic and not fabrication output.

Next: qualify actual fastening stacks, nut retention, support-to-side anchorage and loads; detail independent monitor/crossmember retention and captive props. The owner accepted this retention direction; keep its generated geometry separate from original V32 until those interfaces are resolved. A PC or joinery change requires rerunning relevant checks. Physical sessions remain paused; manufacturing remains blocked.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

Owner acceptance is recorded in [DEC-OWNER-V32-SHELVES](DESIGN_DECISIONS.md#dec-owner-v32-shelves--removable-shelf-retention). The separate side-anchorage study does not extend that acceptance to permanent blind bores.

The subsequent [side-anchorage study](SHELF_ANCHORAGE_REVIEW_V32.md) models removable support anchors with proposed blind side bores and rechecks all retained shelf access paths. Its side machining remains unapproved.

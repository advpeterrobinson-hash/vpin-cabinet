# V32 replaceable shelf-support anchorage

[Português (Brasil)](pt-BR/SHELF_ANCHORAGE_REVIEW_V32.md)

**Separate anchorage proposal; 138 checks pass; CNC BLOCKED.** The owner accepted the preceding [removable shelf-retention direction](SHELF_RETENTION_REVIEW_V32.md), recorded in [DEC-OWNER-V32-SHELVES](DESIGN_DECISIONS.md#dec-owner-v32-shelves--removable-shelf-retention). This new study develops its support-to-side interface; it does not extend that acceptance to permanent side machining.

![Shelf-support anchorage](../exports/generated/side-panel-v32/06-shelf-anchorage.png)

## Candidate interface

Each 42 ×150 ×18 mm support receives two inward-facing screws and washers. Each screw engages a candidate threaded insert in a blind hole in the side. Supports remain local to their respective walls; no cross-wall brace is added. Screw access is inside the cabinet, and the outside side faces remain unpierced in this proposal.

| Interface | Explicit study dimension |
|---|---|
| Anchor row | Mid-height of each support; S1 Z151, S2 Z171, S3 Z231 |
| Y offsets from support front | 55 and 125 mm |
| Global Y | S1 175/245; S2 655/725; S3 1135/1205 |
| Support clearance bore | Ø5.5 through the 42 mm support width |
| Blind side bore | Ø8.5 ×10.5 deep from inner face |
| Insert envelope | Ø8 ×10 long; nominal Ø5 central thread envelope |
| Screw envelope | Ø5 ×50 shaft; Ø9 ×4 head |
| Washer envelope | Ø12 ×1; Ø5.5 central clearance |
| Screw/insert axial overlap | 7 mm nominal; not verified effective thread engagement |
| Remaining outside wood | 7.5 mm at nominal 18 mm stock |

All are design-study choices, not a selected insert, supplier drill recommendation, load rating or approved manufacturing tolerance. A real insert may require different pilot geometry, flange, installation tooling and engagement. Do not cut these side holes until the insert and plywood performance are qualified. Blind drilling must be depth-controlled against actual stock thickness.

There are 12 screws, 12 washers and 12 inserts. Relative to the approved-direction retention scene, only SideL/SideR and the six supports change shape. The twelve side bores exist **only in the separately saved proposal**; the original V32 file remains byte-identical. Each modified side and support pair remains mirrored about X300. The six nut covers now have permanent functional codes S1NutCoverL/R through S3NutCoverL/R; original study object names remain as legacy IDs.

## Access and replacement

All 12 support screws clear an inward Ø16 ×100 mm axial driver probe and 55 mm screw/washer withdrawal. Every tip finishes clear of the support. After removal of the unloaded shelf, its four clamp screws/washers, the monitor assembly and T1/T2/T3, each support can be removed with its cover and two captured shelf nuts attached:

| Support pair | First move | Then along Y | Final upward exit |
|---|---|---|---|
| S1SupL/R | 70 mm inward | +310 mm to Y430 | 467.9 mm |
| S2SupL/R | 70 mm inward | −170 mm to Y430 | 447.9 mm |
| S3SupL/R | 70 mm inward | −320 mm to Y760 | 387.9 mm |

Each of these six routes is tested separately with the opposite support retained. The insert stays in the side. The final bottom of the moving assembly is Z606.9, above retained modeled solids. These are packaging-study endpoints, not manual handling instructions. Removing support anchors while a loaded shelf still depends on them is not the proposed service sequence.

After a support has been removed, each insert position also clears the same axial probe from the inside side face. This does not prove that an actual insert driver or extraction tool fits, nor that a failed insert can be removed without damaging the plywood.

All existing shelf clamp-tool paths, 40 mm clamp-screw withdrawals, underside cover-tool paths and three loaded horizontal-first shelf routes were rechecked against the new anchor hardware. They remain clear. Shelf release does not require disturbing these side anchors.

## Evidence and limits

- [Saved proposal](../exports/generated/side-panel-v32/shelf-anchorage-proposal.FCStd): 150 valid single solids, including retained occupancy volumes and candidate hardware; not a BOM count.
- [Validation report](../exports/generated/side-panel-v32/anchorage-validation.json): 138 passing checks, axes, source hashes, access findings and six support routes.
- Source: `tools/shelf_anchorage_v32_entry.py`; parameters: `config/shelf_anchorage_v32.json`.

The model is reopened and checked for exact object identities, preserved permanent codes, valid solids and exact shapes. The entire 7.5 mm outside skin at every hole is probed as solid wood. A through-drill mutation must fail that condition. With an anchor washer retained, a 1 mm inward support movement intersects it; this checks a positive geometric stop, not retention force.

Continuous conservative bounding sweeps cover support/shelf translations; exact coaxial sweeps cover screw/washer withdrawal. Probes test axial space only. Threads, full hand/tool insertion, friction, installation torque, cover fasteners, plywood pullout/bearing/splitting, vibration, dynamic loads and sidewall attachment strength remain unverified. This is a proposed load path, not structural certification. No new capacity is assigned to SSF mounts, playfield hardware or leg brackets.

The integrated runner now covers all five stages:

```sh
bash tools/run_side_review_v32.sh
uv run --with matplotlib python tools/render_shelf_anchorage_v32.py
```

Expected checks: 46 +29 +99 +106 +138 = **418**. Each stage requires its own pass sentinel because FreeCADCmd may exit zero after an exception. Rendering verifies hashes and passing checks. Source V32 remains SHA256 `ff973219bdc8bee6707bd29f6a44da74c895cbcbea9e0b1790d8e7723b9aa038`.

Next: choose and qualify the insert/screw stack against actual plywood, including a representative physical anchor coupon before side machining; detail independent crossmember/monitor release and captive props. The PC architecture discrepancy remains pending. Physical sessions remain paused; the shelf functional approval is not CNC approval.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

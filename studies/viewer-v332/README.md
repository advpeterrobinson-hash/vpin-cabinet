# V33.2 — inspection viewer and assembly-manual framework

The CURRENT offline viewer now supports direct interior inspection, 18 visibility groups, canonical part search, metadata, semantic exploded views and an embedded bilingual assembly framework. The detailed wood mode contains **all 130 V33.1 manufacturing pieces**, not separated copies of compound installed solids.

HEAD BEFORE: `a1f8bb04f7cec6a2220355c6b7ead0e7e0e92ab4`.
HEAD AFTER: the delivery commit containing this report on `feat/cabinet-review-v32`.

[Open viewer](../../exports/generated/viewer-v32/index.html) · [20 review images](../../exports/generated/viewer-v332/index.html) · [Manual EN](../../docs/ASSEMBLY_MANUAL.md) · [Manual PT-BR](../../docs/ASSEMBLY_MANUAL.pt-BR.md) · [Manual JSON](../../exports/generated/viewer-v332/assembly-manual.json).

## Inspection and service states

- One tap hides the playfield, or playfield plus fixed cradles. Interior inspection also hides the matrix while retaining shell, shelves, PCBase, fan stations, SSF and relevant hardware.
- Backbox interior uses the saved 100° door-open geometry, saved flexible loops and retracted latch meshes. Glass/display visibility is an inspection aid. The carrier, cassette, side toy zones, passage, locks and WPC reserves remain inspectable. Individual doors can also be picked and hidden.
- Twelve named states include play, inspection, 50° playfield service, 48 mm lift-out, matrix removal, rear doors open, locks parked, 45°/90° fold and both exploded modes. States are exclusive, so the UI does not combine open doors with folding.
- Normal fold remains: open rear doors → release/park two locks → close/latch doors → remove MAIN PLAYFIELD GLASS and MATRIX → fold. Backbox glass and cassette remain installed. No routine electronics disconnection.
- Rare WPC hinge maintenance is separate and may require cassette removal and playfield lift-out/removal. Saved service geometry does not qualify a physical raised-playfield support or load case.
- Nine camera presets, clipping, shell opacity, hide/isolate/focus and image capture remain available. Group visibility does not reset the camera. The control panel collapses for the model area; no hover interaction is required.

## IDs and exploded architecture

Installed labels use readable aliases such as SideL, T1, S2 and BBFloor, linked to P assembly IDs and permanent M manufacturing families. Selection includes both language names, assembly/manual stage, material, nominal stock thickness, quantity authority, route, hardware ID and purchase/freeze status. Search accepts these aliases and M/F/H/etc IDs. Selection uses an edge overlay and bounding outline as well as contrast.

Overview offsets separate semantic assemblies moderately. Detailed offsets move sides outward, end structures longitudinally, floor vertically, shelves upward, and hardware opposite catalogued installation directions. Washers follow the same axis. Actual laminate centers establish ordered Z separation; intake faces/top/returns move along their assembly directions. Opposing FACE A normals do not collapse the retainer cap/strip into one position. Focused decomposition views carry part-ID labels.

All 148 V33 catalog families are represented with their existing authority, including reference/electronics families. **71 families have no authoritative displayed installation position** and use one labelled exemplar in a separate tray. Unresolved crosses remain identified as markers, not purchased hardware shapes. Their tray coordinates are documentation layout only. Unknown quantities remain null/formula-driven; no hole positions or hardware counts were invented. The existing 13 unresolved required rows remain six formulas and seven genuinely TBD.

Wood/hardware filters and main-cabinet/playfield/backbox/all scopes limit clutter. Dedicated filters expose 28 leg layers, eight intake-baffle panels, the cap/strip, monitor-stop laminations and cassette-cleat laminations. Exploded offsets are **not validated removal trajectories**.

## Manual framework

The English source and complete PT-BR version contain **19 stages, 31 steps and 31 checkpoints**. Each step records component/hardware IDs, stage/global quantities, orientation, tools, FACE A/B authority, action, check, hold and a linked CAD state. Quantities repeated in multiple steps are reference totals, not repeated consumption.

The per-piece annex has 130 orientation cards plus exact CNC/manual metadata. It distinguishes CNC contour/pocket work from drilling, countersinking, corner finish and bevel sanding; the 59 manual-finish routes retain their operations and depth references. FACE B has no CNC. Actual thickness, coupon, hardware, guide/finish, adhesive and load qualification remain explicit holds. No final PDF was generated.

The embedded manual offers an exploded stage subset and a cumulative assembled stage view using real members. On desktop its panel reserves space beside the model. The sequence is a **framework**, not a physically rehearsed or released assembly procedure. Electronics remain a later optional overview.

## Performance and validation

The single-file viewer embeds compressed data and licensed Three.js/OrbitControls; it requires no server or network request. Detailed GPU objects are created only when needed. V33 source B-reps are tessellated for display at 0.8 mm linear / 0.4 rad angular settings, with no helical threads. The complete detailed dataset has approximately 315,000 triangles; that display LOD is never used for CNC or collision proof. The file is approximately 10.4 MB.

The browser suite passed **53 checks**, with networking disabled, English/Original defaults, bilingual/Accessible toggles, state prerequisites, search, non-color selection, touch emulation and 44 px controls. Desktop 1600×1050 and tablet layouts 1024×1366 / 834×1194 were checked. Measured initial load on the test machine was 1362 ms; this is not a physical-tablet frame-rate guarantee.

The metadata/source suite passed **3821 checks**. **1917 pre-existing authority files** match their starting Git blobs, including CURRENT B-reps, V33 hardware, V33.1 pieces, supplier profile and release flags. All 130 wood meshes retain original triangle topology and exact installed transforms; rendering copies round coordinates by at most 0.00005000 mm. No accepted hole, fit or B-rep geometry changed. The prior zero-volume reconstruction proof remains unchanged; no new collision or structural certification is claimed.

[Metadata/source evidence](../../exports/generated/viewer-v332/validation.json) · [Browser evidence](../../exports/generated/viewer-v332/browser-validation.json) · [LOD source hashes](../../exports/generated/viewer-v332/hardware-lod-validation.json).

## Required report

| Field | Result |
| --- | --- |
| Hide playfield / supports | YES / YES |
| Interior / backbox inspection | YES / YES |
| Visibility groups | 18 |
| Search / part metadata | YES / YES |
| Tablet touch controls | PASS in browser touch emulation |
| Offline / EN–PT-BR | PASS / PASS |
| Original / Accessible palettes | PASS / PASS |
| Overview / detailed explosion | PASS / PASS |
| Wood-only / hardware-only | PASS / PASS |
| Real V33.1 pieces / V33 models | YES / YES |
| English / PT-BR manual | YES / YES |
| Stages / steps / checkpoints | 19 / 31 / 31 |
| Hardware uncertainty honest | YES; unknown counts preserved |
| One-sided manual finish represented | YES; all 130 preparation records, 59 affected pieces |
| CURRENT / manufacturing geometry changed | NO / NO |
| Manufacturing release | **STILL BLOCKED** |

## Reproduction

```sh
freecadcmd tools/viewer_v332_lod_entry.py
python3 tools/build_review_viewer.py
python3 tools/check_assembly_viewer_v332.py
python3 tools/check_assembly_metadata_v332.py
python3 tools/check_current_v32.py
python3 tools/package_viewer_v332.py
```

The browser runner needs an existing Playwright installation and Chrome. Set `VPIN_NODE_MODULES` if its dependency root is elsewhere. The viewer itself does not need these development dependencies. Historical V32 controls can still be generated into an isolated output using `build_review_viewer.py --legacy`; the default now follows [V33.2 documentation authority](../../config/viewer_v332.json).

Require explicit PASS sentinels for FreeCAD scripts; an exit code alone is insufficient. No supplier values, production vectors, G-code or manufacturing release were changed.

CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

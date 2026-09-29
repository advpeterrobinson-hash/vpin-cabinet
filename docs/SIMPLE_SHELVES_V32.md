# V32 — simple top-release shelves

[Português (Brasil)](pt-BR/SIMPLE_SHELVES_V32.md)

**Current owner-directed shelf fixing direction. Supersedes the removable support/nut-cover studies for normal service. CNC BLOCKED.**

![Four top screws](../exports/generated/side-panel-v32/07-simple-shelves.png)

The intended routine is: open and positively support the playfield, disconnect the shelf harness, undo **two top screws on each side**, then slide the shelf into its extraction bay and lift it with equipment attached. Local supports remain fixed in the cabinet. No nut covers, underneath release or support-side anchors are part of this routine. Threaded receivers stay in the supports so nothing loose needs a hand underneath.

The new separate CAD implements four top screws per shelf with simple top-insert envelopes in fixed 42 mm-wide supports. Original permanent panels and all crossmembers are unchanged. The previous captured-nut covers and support replacement mechanism are superseded in the current direction; their old evidence is retained only as history. S1NutCoverL/R through S3NutCoverL/R are retired identities and must not be reused.

## Changes needed for visible access from above

| Shelf | Leading Y | Screw rows (global Y) | Removal path with crossmembers retained |
|---|---:|---:|---|
| S1 | 120, unchanged | 145 /220 | Rearward 310 mm to Y430, then lift |
| S2 | 600, unchanged | 625 /735 | Forward 170 mm to Y430, then lift |
| S3 | **1000, 80 mm forward of original** | 1025 /1100 | Forward 240 mm to Y760, then lift |

Each row has left/right axes X48/552. S2's old rear axis Y700 was under T2; Y725 also encountered its support angle. S3's old rear axis Y1180 was under BBBase. Those rejected cases remain executable controls. Moving S3 locally and positioning its screws forward of BBBase creates clear top access without moving the backbox structure. Shelf sizes remain 560 ×150 ×12 mm and the heights remain unchanged.

The test now reserves an entire vertical Ø16 tool column from each screw head to Z606.9, rather than testing only a short driver beneath a hidden obstruction. Three loaded removal paths also pass with **all three crossmembers, guides and supports retained**. Other shelves stay installed. The candidate equipment envelope is 60 mm above each shelf, with four Ø20 equipment/wiring exclusions for tool access. These exclusions are not large holes in the shelf. S1's modeled audio body moves with it.

## What is and is not demonstrated

**90 checks pass** against the stationary scene. The raised playfield is not yet modeled: its four assembly shapes are explicitly excluded to test the space the open display must leave available. This is therefore **not proof that the actual raised display, hinges, captive props and cables clear these paths**. That is the next integration gate; do not describe this as an already validated routine opening mechanism.

Nominal candidate fastening: Ø5 ×25 shaft, Ø9 ×4 head, Ø12 ×1 washer, top receiver Ø8 ×10, Ø8.5 pocket10.5 deep and a Ø5.5 tip relief12.5 deep in the nominal18 support. There are no underside nut pockets or covers. Hardware, threads, receiver retention, fixed-cleat attachment, loads and stock/tool tolerances are unqualified; these are not purchase or machining specifications. Support installation should be a fixed cabinet-assembly operation, not another service mechanism.

- [Simplified FreeCAD proposal](../exports/generated/side-panel-v32/simple-shelves-proposal.FCStd): reopened and compared, 108 valid single solids including occupancy volumes.
- [Validation](../exports/generated/side-panel-v32/simple-shelves-validation.json): complete top columns, withdrawals, three continuous conservative translation sweeps and rejected old layouts.
- Parameters: `config/simple_shelves_v32.json`; source: `tools/simple_shelves_v32_entry.py`.

Use `bash tools/run_simple_shelves_v32.sh`, then `uv run --with matplotlib python tools/render_simple_shelves_v32.py`. Require `SIMPLE_SHELVES_PASS`; the older five-stage side runner reproduces the superseded complexity studies and is no longer the current shelf authoring entry point.

Original V32 bytes remain unchanged. The illustration is an explanatory exploded schematic with exaggerated separation, not a fabrication drawing. Physical sessions remain paused. The PC decision is unchanged.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

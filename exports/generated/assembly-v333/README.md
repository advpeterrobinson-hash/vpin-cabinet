# V33.3 — material, mass, packaging and assembly screening

HEAD BEFORE: `254c54541548555b22e6455413e642cb32131f79`

CURRENT geometry unchanged. Full-sheet release BLOCKED. Coupon waits for production-lot material. No production nesting or G-code.

## Material dashboard

Full-sheet assumption, not an order recommendation. Exact B-rep outer/projection areas; reserved spacing is not sawdust. Potential offcuts are disjoint free rectangles at least150×150mm; kerf/tabs/holding remain CAM dependent.

| Stock | Pieces | Old/new sheets | Outer m² | Net utilization | Gross waste incl. offcuts | Potential offcuts m² | Practical stock mm |
|---|---:|---|---:|---:|---:|---:|---|
| 18 | 88 | 2/2 | 5.25614 | 55.35% | 44.65% | 1.320 | [[2500, 1600], [2500, 1600]] |
| 12 | 25 | 1/1 | 1.22804 | 27.81% | 72.19% | 2.327 | [[1300, 1300]] |
| 8 | 2 | 1/1 | 0.05780 | 0.89% | 99.11% | 3.769 | [[450, 250]] |
| 6 | 13 | 1/1 | 0.49802 | 4.64% | 95.36% | 3.197 | [[850, 800]] |
| 4 | 2 | 1/1 | 0.00043 | 0.01% | 99.99% | 3.786 | [[100, 100]] |

4/6/8mm: source qualified offcuts or smaller premium stock, not whole sheets for these small requirements. Non-18mm stock/holding requires supplier qualification. Premium-first policy retained; no automatic structural downgrade. Three guillotine orderings improve offcut recovery; this is not an optimized nesting. Detailed loss accounting and actual contour previews: [material-utilization.json](material-utilization.json).

## Mass — kg, LOW / NOMINAL / HIGH

- Wood: 51.31 / 60.64 / 69.97; exact nominal B-rep volume, density550/650/750 sensitivity.
- Required hardware: no weighed KNOWN masses. Nominal simple-form ESTIMATED subtotal 1.13; 69 required families remain UNKNOWN. Explicit unmeasured-assembly allowance8/15/25kg, not a closed BOM mass.
- Mechanical scenario: 60.21 / 76.77 / 96.33. Exact total UNKNOWN.
- Glass reference estimate: 11.40. Future electronics: 21.00 / 38.20 / 55.00.
- Full planning build: 92.62 / 126.37 / 162.73. These illustrative scenarios are not guaranteed limits; toy/electronics selections vary. See [mass-budget.json](mass-budget.json).

## Packaging

Hardware requires a separate purchased-parts box. Glass/displays/electronics excluded. Package CG uses exact wood B-rep centroids; packaging mass assumed centered. Nominal limits are not certified lifting limits. Large panels should be carried by two people.

### 20 kg target at750kg/m³ — 4 bundles

| ID | L × W × H mm | Wood kg | Packaging kg | Gross nominal kg | Gross at750kg/m³ |
|---|---|---:|---:|---:|---:|
| P20-01 | 1353.1 × 641.9 × 60.0 | 15.65 | 1.84 | 17.49 | 19.90 |
| P20-02 | 1317.1 × 609.0 × 82.0 | 15.60 | 2.00 | 17.60 | 20.00 |
| P20-03 | 825.0 × 768.9 × 142.0 | 15.58 | 2.02 | 17.60 | 20.00 |
| P20-04 | 1197.1 × 275.0 × 211.8 | 13.80 | 1.64 | 15.44 | 17.57 |
### 25 kg target at750kg/m³ — 4 bundles

| ID | L × W × H mm | Wood kg | Packaging kg | Gross nominal kg | Gross at750kg/m³ |
|---|---|---:|---:|---:|---:|
| P25-01 | 1353.1 × 641.9 × 88.0 | 19.80 | 2.15 | 21.95 | 25.00 |
| P25-02 | 1317.1 × 609.0 × 88.0 | 19.92 | 2.01 | 21.93 | 25.00 |
| P25-03 | 825.0 × 768.9 × 197.8 | 19.53 | 2.47 | 22.00 | 25.00 |
| P25-04 | 1197.1 × 240.0 × 60.0 | 1.39 | 0.89 | 2.27 | 2.49 |
### 30 kg target at750kg/m³ — 3 bundles

| ID | L × W × H mm | Wood kg | Packaging kg | Gross nominal kg | Gross at750kg/m³ |
|---|---|---:|---:|---:|---:|
| P30-01 | 1353.1 × 641.9 × 98.0 | 24.02 | 2.29 | 26.30 | 30.00 |
| P30-02 | 825.0 × 768.9 × 192.0 | 23.94 | 2.37 | 26.31 | 30.00 |
| P30-03 | 1197.1 × 545.0 × 153.8 | 12.68 | 2.28 | 14.96 | 16.91 |

Preferred25kg candidate sized at750kg/m³ sensitivity density; reweigh production lot and redistribute if gross limits exceeded. [Contents, exact CG, layers and separators](packaging.json). Rigid separators must bridge openings; compression/drop protection remains to qualify.

## Hardware dashboard

Fxx models: 54 total; 35 required; 6 optional; 13 user-adapter.
Known minimum required Fxx quantity: **160**, plus formula-dependent F53, F18, F36, F38, F39; genuinely TBD F06, F16, F19, F22, F28, F31. This is not the final screw count.
[Other hardware, units and quantities](hardware-dashboard.json). No quantities changed.

## Assembly qualification

19 stages /31steps screened against actual manufacturing members; dependency graph passes. **0 newly physically validated steps**. No continuous new insertion paths validated; all31assembly clips are labelled SCHEMATIC ASSEMBLY ANIMATION.
Both FACE_A-normal extraction candidates were sampled at0.5,2,5,10,20,40,80,150,300mm. Same-stage other assemblies were conservatively present, own laminations excluded. Sampling neither proves a sweep nor permits blindly following a conflicted path. R10×100 tool approach screens are provisional; catalog centers are not purchased screw-head datums. Full reports retain every tested piece and hardware reserve.
[Per-step results](assembly-validation.json) · [Insertion screens](insertion-screens.json) · [Tool screens](tool-screens.json). No speculative reorder: unresolved joint schedules, selected tools, fixtures and continuous insertion trials prevent declaring the31steps build-validated. Normal service proofs remain separate from these holds.

## Review / animation

[Offline viewer](../viewer-v32/index.html) includes31assembly clips,11service clips and packing/unpacking. Validated service transforms are identified separately from schematic transitions. [Geometry protection](geometry-protection.json) compares every protected blob with starting HEAD.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
<!-- V333_FINAL_SUPPLEMENT -->

## Exact area accounting and purchase comparison

All areas below are m². Spacing is the precise reserved area in this rectangle layout, not physical kerf loss. Cutouts are B-rep projected openings. Material removed by pockets, bores and face reduction is additionally itemized as volume in JSON. Potential reusable rectangles exclude cutout islands, profile scraps and final tabs.

| Thickness | Full sheet purchase | Usable | Border | Spacing reserve | Rectangle/profile loss | Cutouts | Net part area | Old/new potential reusable |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 18 | 8.000000 | 7.675200 | 0.324800 | 0.551605 | 0.323551 | 0.828539 | 4.427603 | 0.000 / 1.320 |
| 12 | 4.000000 | 3.837600 | 0.162400 | 0.158796 | 0.000000 | 0.115583 | 1.112456 | 1.969 / 2.327 |
| 8 | 4.000000 | 3.837600 | 0.162400 | 0.010650 | 0.000000 | 0.022169 | 0.035631 | 3.738 / 3.769 |
| 6 | 4.000000 | 3.837600 | 0.162400 | 0.064920 | 0.000000 | 0.312527 | 0.185493 | 2.551 / 3.197 |
| 4 | 4.000000 | 3.837600 | 0.162400 | 0.001350 | 0.000000 | 0.000000 | 0.000432 | 3.771 / 3.786 |

| Thickness | Practical procurement envelope | Net utilization in smaller stock |
|---:|---|---:|
| 18 | [[2500, 1600], [2500, 1600]] mm | 55.35% |
| 12 | [[1300, 1300]] mm | 65.83% |
| 8 | [[450, 250]] mm | 31.67% |
| 6 | [[850, 800]] mm | 27.28% |
| 4 | [[100, 100]] mm | 4.32% |

The full-sheet study recovers larger contiguous rectangles without reducing the six-sheet assumption. The separate small-stock search reduces procurement area. Neither search is an optimized production nesting; non-18 mm stock availability and small-stock retention require shop approval.

## Assembly screening result

No geometry correction or speculative reorder was applied. The fixed manufacturing members are all present in the insertion report; the exact source operations/faces remain in the manual. There are 49 unique pieces with conflicts on both tested face-normal candidates. These do not exclude a different feasible assembly direction or bench subassembly. The current screen deliberately does not invent one.
There are 76 located Fxx driver reserves, of which 30 intersect final installed wood. All are recorded, including obstacle IDs/stages; some may be cleared by performing the operation earlier. An R10 ×100 reserve is not a selected tool or hand and cannot certify ergonomics.
19 stage dependency checks and all31step evidence records are complete. **Full assembly-sequence/tool-access validation remains HOLD**: selected hardware/tool forms, joint fastener schedules, fixtures, and continuous insertion paths must be qualified. No new physically validated assembly steps are claimed. This is an explicit remaining blocker, not a manufacturing release.

## Animation and regression evidence

-31schematic assembly/checkpoint clips,11service clips,2packing clips; exact130manufacturing meshes used for packing.
-125 animation/offline/touch checks; 53 retained viewer checks; 9494 conservation/containment/authority checks.
-Touch playback: PASS in834×1194emulation. Physical tablet frame-rate qualification is not claimed.
-Service endpoints compare planar parts within0.002mm; simplified cylindrical lock meshes use0.6mm vertex-sampling tolerance because retessellation changes vertices. The motion axes/routes come from the accepted CAD builders, not from vertex interpolation.
-Current installed geometry, all130manufacturing pieces, hardware catalog and existing CNC/fit authority remain byte-identical. Entire V33.2 embedded geometry payload retained byte-for-byte.
-Release/retainer/fastener details without a proven path are explicitly schematic; shelf removal is schematic. Door flexible-loop centerline uses the accepted constant-length construction; purchased cable bend properties remain unqualified.
-Normal fold retains backbox glass/cassette and requires locks parked, rear doors latched, main playfield glass/matrix removed. Rare hinge service remains separate.

[Review gallery](index.html) · [Offline interactive viewer](../viewer-v32/index.html) · [Machine-readable manual](assembly-manual.json)

HEAD AFTER is the commit containing this report; the exact resulting commit is supplied in the delivery response. Full-sheet CNC remains BLOCKED.

## Reproduction

```sh
freecadcmd tools/assembly_v333_brep.py
freecadcmd tools/assembly_v333_motion.py
python3 tools/build_assembly_v333.py
python3 tools/build_viewer_v333.py
python3 tools/check_assembly_v333.py
python3 tools/check_metrics_v333.py
python3 tools/check_current_v32.py
python3 tools/package_assembly_v333.py
```

Require positive V333_BREP_PASS and V333_MOTION_PASS sentinels: FreeCAD can return zero on Python exceptions. Browser checks require existing Playwright and Chrome; the delivered viewer itself needs no server/network.

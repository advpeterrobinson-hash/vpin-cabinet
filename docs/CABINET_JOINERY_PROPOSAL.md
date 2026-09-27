# Lower-cabinet CNC joinery proposal

[English](CABINET_JOINERY_PROPOSAL.md) · [Português (Brasil)](pt-BR/CABINET_JOINERY_PROPOSAL.md)

**STATUS: PROPOSAL — NOT INCORPORATED INTO V32 GEOMETRY — NOT RELEASED FOR CNC.**

## Intent

Turn the lower cabinet into a self-indexing assembly: major parts should mechanically locate one another before glue and structural screws are installed, reducing squaring error and dependence on manual layout.

The original “small chamfer” idea is treated here as a **shallow CNC captured dado/rabbet**. It is not a cosmetic edge chamfer.

## Existing engineering precedent

The project already carried a captured-joinery concept in `config/cabinet_structure_v20.json`:

- nominal plywood: 18 mm;
- nominal groove depth: 6 mm;
- nominal material remaining behind the groove: 12 mm;
- initial nominal joint clearance: 0.2 mm;
- final fit controlled by measured plywood thickness and a CNC tolerance coupon.

That geometry is a useful engineering baseline, but it is **not automatically approved for V32**.

## Proposed concept

### 1. Floor ↔ SideL / SideR

Machine a shallow longitudinal capture groove in each cabinet side to receive the edge of `Floor`.

Goals:

- locate Z and keep the floor parallel;
- prevent sliding during glue-up;
- increase glue area;
- allow a complete dry fit before structural screws are installed.

Prototype starting point:

- depth: **6 mm nominal**;
- groove width: **actual measured panel thickness** plus coupon-derived clearance;
- groove must not break through the cabinet side;
- no groove may enter critical leg-bolt, insert or hardware zones.

### 2. Front / Rear ↔ SideL / SideR

Use captured rabbets/dados at the end-panel interfaces so `Front` and `Rear` locate without manual measurement.

The final detail may use:

- dado + tongue;
- captured rabbet;
- another cutter-compatible locating shoulder.

Selection should favor structural section, glue area, simple assembly and simple machining.

### 3. S1 / S2 / S3

Do **not** automatically cut deep shelf grooves into the main structural side panels. First compare:

A. keep `S#SupL/R` as replaceable shelf-support parts;  
B. shallow groove directly in the side panel;  
C. hybrid captured interface in a replaceable support, preserving the cabinet side.

Initial preference: **preserve the main side panel** and use `S1SupL/R`, `S2SupL/R`, and `S3SupL/R` as the shelf interface. This keeps the assembly repairable and avoids multiplying cuts in a large structural panel.

### 4. T1 / T2 / T3

Retain the V32 principle:

- no deep crossmember groove directly in the structural side;
- `T1GuideL/R`, `T2GuideL/R`, and `T3GuideL/R` carry wear and adjustment geometry;
- guides remain replaceable.

## Intended assembly sequence

1. place `SideL` on a flat reference;
2. dry-fit `Floor` into its capture groove;
3. install `Front` and `Rear`;
4. install `SideR` and close the cabinet shell;
5. temporarily install internal pieces that establish cabinet width;
6. verify every locating shoulder is fully seated;
7. measure cabinet diagonals and external width;
8. disassemble if required;
9. apply glue only to approved structural joints;
10. reassemble through the same self-indexing path;
11. clamp;
12. verify square again;
13. only then install the defined structural screws/fasteners.

Structural screws must not be used to pull a badly machined joint into position.

## Structural safeguards

No groove is released merely because it is convenient in CAD. Before adoption:

- measure actual plywood thickness;
- machine a tolerance coupon using the same sheet type and cutter;
- retain adequate residual section behind every groove;
- keep adequate edge distance from holes, inserts and fasteners;
- exclude leg-load and hinge-load zones;
- avoid dense clusters of nearby grooves;
- preserve outer plies where practical;
- require hand-pressure dry assembly without heavy hammering;
- physically test stiffness and failure behavior before manufacturing release.

### Initial depth rule

`6 mm in nominal 18 mm plywood` remains only a **test baseline**, leaving about 12 mm behind the groove. Final depth must follow material measurements and testing; it must not be increased merely to make the fit feel tighter.

## CNC fit control

Groove width must not be frozen at “18.0 mm” for convenience. Nominal plywood varies.

Required flow:

`measure sheet -> machine coupon -> hand-test fit -> record offset -> generate toolpath`

The joint should seat with predictable hand pressure and sufficient glue clearance. Excessive interference can prevent full seating or damage plywood plies.

## Cutter radius and dogbones

Internal corners must respect the actual cutter radius. Dogbones should appear only where a square mating tab genuinely needs to reach an internal corner; they should not be added to visible edges by default.

## Proposed next design step

For the next CAD iteration:

- recover the **captured flat-pack joinery** principle already present in v20;
- apply it first to `Floor ↔ SideL/SideR` and `Front/Rear ↔ SideL/SideR`;
- keep shelves and crossmembers on replaceable interfaces until structural comparison is complete;
- render an exploded assembly view showing the indexing sequence;
- manufacture a physical tolerance coupon before any full-cabinet CNC run;
- compare the proposed geometry against V32 for collisions, residual section and hardware keepouts.

Until those checks pass, this document remains a proposal and published V32 remains the current visual reference.

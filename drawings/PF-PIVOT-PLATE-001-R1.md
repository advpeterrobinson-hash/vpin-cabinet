# PF-PIVOT-PLATE-001-R1 — engineering fabrication sketch

**Status:** v0.15 engineering baseline for quoting/prototyping only. Not a released CNC production drawing.

Units: mm.

## Material

- A36 or SAE 1020 carbon steel plate.
- Nominal thickness: **6.0 mm**.
- 6.35 mm / 1/4 in stock is acceptable only after CAD stack is updated.
- Finish after all machining/welding: zinc plating, powder coat, or epoxy primer/paint.

## Blank

- Overall length (front/rear direction): **140.0**
- Overall height: **80.0**
- Thickness: **6.0**
- External corners: **R6** nominal

Reference origin for the coordinate table below: **rear-bottom corner of plate**.

- +Y = forward from rear plate edge.
- +Z = upward from bottom plate edge.

## Hole / datum table

| Feature | Y from rear edge | Z from bottom | Diameter / note |
|---|---:|---:|---|
| Pivot axis datum | 25.0 | 40.0 | 15 mm journal interface; final fit process after actual bearing measurement |
| M8 mount A | 70.0 | 20.0 | Ø9.0 through |
| M8 mount B | 70.0 | 60.0 | Ø9.0 through |
| M8 mount C | 120.0 | 20.0 | Ø9.0 through |
| M8 mount D | 120.0 | 60.0 | Ø9.0 through |

Left and right plates use the same 2D blank geometry; handedness comes from installation/journal orientation and part marking.

## Journal fabrication concept

- Candidate journal: Ø15 mm SAE 1045 or equivalent turned/ground steel.
- Candidate projection from finished plate face: **65 mm**.
- Journal is jigged perpendicular to the plate.
- If welding is used, weld on the non-bearing side and protect the journal surface from spatter/heat damage.
- Check journal runout/perpendicularity after welding.
- Final journal projection is **not frozen** until the actual UCFL202 bearing pair and cabinet-side stack are measured.

## Mounting to plywood cradle

Each plate clamps against a ~36 mm laminated plywood pivot zone using:

- 4 x M8 class 8.8 through-bolts;
- washers;
- prevailing-torque/nyloc nuts;
- matching 3 mm steel spreader/backing plate on opposite plywood face.

Wood screws are not the primary pivot fastener.

## Quote wording in Portuguese

`2 chapas aço carbono A36/SAE 1020, 140 x 80 x 6 mm, cantos R6, 4 furos Ø9 conforme desenho, corte laser/água, rebarbadas. Prever interface para eixo Ø15 mm; acabamento final somente após solda/usinação.`

Do not order final cabinet-side bearing holes from this drawing. Those depend on the **actual measured UCFL202 housing**.

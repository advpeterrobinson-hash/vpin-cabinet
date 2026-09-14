# Reference Cabinet Baseline

Source:
dekay/vpin-cabinet reference model
vpin-cabinet-2026-02-16.FCStd

This file records dimensions extracted from the reference model.
They are reference values only and are NOT automatically approved
manufacturing dimensions.

## Williams-style cabinet reference

Main cabinet side:
- Material thickness: 19.05 mm
- Length envelope: 1308.10 mm
- Height envelope: 596.90 mm

Cabinet external width reference:
- 558.80 mm

Cabinet internal width reference:
- 520.70 mm

Relationship:
520.70 + (2 x 19.05) = 558.80 mm

## New metric design decision

Preserve Williams external width:
- 558.80 mm

Use nominal metric plywood:
- 18.00 mm initially

Resulting nominal inside width:
- 522.80 mm

Actual plywood thickness will replace nominal 18.00 mm after
measuring the material selected for production.

## Backbox reference

Overall reference bounding box:
- Width: 730.25 mm
- Depth: 254.00 mm
- Height: 723.90 mm

## Reference playfield display

Reference model TV envelope:
- Cross-cabinet dimension: 533.40 mm
- Long dimension: 932.00 mm
- Thickness: 36.10 mm

This is NOT assumed to match the selected LG OLED42C5.

Reference playfield TV mount:
- Width: 535.78 mm
- Length: 1093.79 mm
- Thickness: 12.70 mm

## Reference internal components

Controller shelf board:
- 514.35 x 171.45 x 12.70 mm

Computer shelf:
- 355.60 x 406.40 x 12.70 mm

These are layout references only.

## Parametric redesign rules

Our FreeCAD master must use a Spreadsheet parameter source.

The existing reference model contains no Spreadsheet::Sheet objects.

The new model will separate:
- Williams external dimensions
- measured material dimensions
- OLED envelope
- manufacturing clearances
- CNC cutter dimensions
- hardware dimensions
- force-feedback zones
- electronics/service envelopes

# CNC part labeling convention

Status: accepted documentation convention; engraving implementation remains pending final part geometry.

## Goal

Every CNC-cut or separately fabricated structural part must be identifiable without opening FreeCAD or measuring it against another part. Labels must tie directly to the BOM and assembly manual.

## Part ID format

Use:

`<SYSTEM>-<GROUP>-<NUMBER><SIDE>-R<REV>`

Examples:

- `CAB-SIDE-001L-R1` — main cabinet left side
- `CAB-SIDE-001R-R1` — main cabinet right side
- `CAB-XMEM-010-R1` — main cabinet crossmember
- `BB-FLOOR-001-R1` — backbox floor
- `BB-DOOR-001-R1` — keyed rear service door
- `BB-XMEM-002-R1` — backbox upper structural crossmember
- `PF-CRADLE-001L-R1` — playfield cradle left rail
- `PC-TRAY-001-R1` — PC drawer platform
- `MET-LBAR-001-R1` — fabricated lockdown bar

## System prefixes

| Prefix | System |
|---|---|
| CAB | Main cabinet wood structure |
| BB | Backbox wood structure / service enclosure |
| PF | Playfield display cradle / service mechanism |
| PC | PC drawer / chassis adapter |
| LEG | Leg / leveler / mobility interface |
| GLASS | Glass channels / retainers |
| MET | Outsourced metalwork |
| IO | Removable I/O fascias and carriers |
| HAR | Cable supports/passports/harness brackets |
| EL | Electrical-only later-phase parts |

## Side suffix

Use `L` and `R` only for truly handed parts. Do not label a symmetric pair left/right if either part can be installed on either side.

## CNC engraving placement

Each wood part should receive a shallow CNC identification engraving in a normally hidden location:

- approximately 4–6 mm character height;
- shallow enough not to weaken the part;
- at least 12 mm from finished edges, dados, major holes and visible cosmetic surfaces;
- never placed in a high-stress hinge/leg/fastener zone;
- orientation arrow where useful (`FRONT ->`, `UP ->`, `INSIDE`).

Example:

`CAB-SIDE-001L-R1  INSIDE  FRONT ->`

## Cosmetic vs manufacturing engraving

Manufacturing labels are distinct from the vintage white-filled visible legends used on service panels.

Manufacturing export layers should ultimately distinguish at minimum:

- `CUT_THROUGH`
- `POCKET`
- `DRILL`
- `ENGRAVE_ID`
- `ENGRAVE_WHITE`
- `REFERENCE_NO_CUT`

## Assembly manual cross-reference

Every assembly step must identify parts by ID, not only by prose.

Example:

> Install `CAB-XMEM-010-R1` between `CAB-SIDE-001L-R1` and `CAB-SIDE-001R-R1`, with the engraved `FRONT ->` arrow facing the coin-door end.

## Hardware-bag labeling

Hardware should be packed/listed by build step where practical:

- `BAG A1 — MAIN SHELL`
- `BAG A2 — LEG CORNERS`
- `BAG B1 — BACKBOX HINGES`
- `BAG B2 — BACKBOX LOCK/DOOR`
- `BAG C1 — PLAYFIELD CRADLE`
- `BAG D1 — PC DRAWER`

The BOM maps every fastener to both a part ID and a bag/step ID.

## Revision discipline

If geometry, hole positions or material thickness compatibility changes, increment the part revision. A part with a changed manufacturing interface must not silently retain the same revision ID.

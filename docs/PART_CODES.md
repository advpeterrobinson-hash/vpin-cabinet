# Permanent part-code system

[English](PART_CODES.md) · [Português (Brasil)](pt-BR/PART_CODES.md)

## Purpose

The project uses a short, stable identity for each accepted part to reduce ambiguity across CAD, renders, BOMs, assembly instructions and design discussions.

A code represents **the function of the part**, not merely a temporary filename.

## Core rules

1. While a part or concept is still under evaluation, documentation shows its name in bold, for example **provisional fan bracket**.
2. Once that part proposal is accepted into the architecture, it receives a permanent code.
3. A permanent code is **never reused** for another function, even if the original part is later retired.
4. Geometry changes that preserve the function keep the same code and advance the revision, for example `T1-R2`, `T1-R3`.
5. A different function receives a different code.
6. Codes should appear in CAD, BOMs, drawings, documentation and, where legible, future renders.

## Convention

- `T#` — structural crossmember.
- `S#` — shelf.
- `S#SupL`, `S#SupR` — left/right shelf support.
- `T#GuideL`, `T#GuideR` — left/right replaceable crossmember guide.
- `T#SupL`, `T#SupR` — left/right crossmember support/bracket once finalized.
- `MonRailL`, `MonRailR`, `MonBridge` — primary monitor-support parts.
- `SideL`, `SideR`, `Front`, `Rear`, `Floor` — main cabinet panels.
- `RearDoor` — rear service door.
- `PCBase` — lower PC base.
- `BBBase` — backbox base/support.

`L` and `R` are defined while looking at the cabinet from the front unless a document explicitly states otherwise.

## V32 registry

| Permanent code | V32 legacy ID | Function | Status |
|---|---|---|---|
| SideL | SIDE_L | left cabinet side | architecture accepted; final hole details still blocked |
| SideR | SIDE_R | right cabinet side | architecture accepted; final hole details still blocked |
| Front | FRONT | front panel | architecture accepted; some cutouts still pending |
| Rear | REAR | rear panel | architecture accepted; component interfaces pending |
| RearDoor | REAR_DOOR | rear service door | architecture accepted; hardware pending |
| Floor | FLOOR | bottom panel | architecture accepted; final cutouts pending |
| S1 | SHELF_1 | front transverse shelf | accepted in V32 architecture |
| S1SupL | SHELF_SUPPORT_1L | S1 left support | accepted; fastening pending |
| S1SupR | SHELF_SUPPORT_1R | S1 right support | accepted; fastening pending |
| S2 | SHELF_2 | center transverse shelf | accepted in V32 architecture |
| S2SupL | SHELF_SUPPORT_2L | S2 left support | accepted; fastening pending |
| S2SupR | SHELF_SUPPORT_2R | S2 right support | accepted; fastening pending |
| S3 | SHELF_3 | rear transverse shelf | accepted in V32 architecture |
| S3SupL | SHELF_SUPPORT_3L | S3 left support | accepted; fastening pending |
| S3SupR | SHELF_SUPPORT_3R | S3 right support | accepted; fastening pending |
| T1 | CROSS_1 | front upright crossmember | accepted in V32 architecture |
| T1GuideL | CROSS_GUIDE_1L | T1 left replaceable guide | concept accepted; hardware pending |
| T1GuideR | CROSS_GUIDE_1R | T1 right replaceable guide | concept accepted; hardware pending |
| T2 | CROSS_2 | center upright crossmember | accepted in V32 architecture |
| T2GuideL | CROSS_GUIDE_2L | T2 left replaceable guide | concept accepted; hardware pending |
| T2GuideR | CROSS_GUIDE_2R | T2 right replaceable guide | concept accepted; hardware pending |
| T3 | CROSS_3 | rear upright crossmember | accepted in V32 architecture |
| T3GuideL | CROSS_GUIDE_3L | T3 left replaceable guide | concept accepted; hardware pending |
| T3GuideR | CROSS_GUIDE_3R | T3 right replaceable guide | concept accepted; hardware pending |
| MonRailL | MONITOR_RAIL_L | left monitor rail | architecture accepted; final fastening pending |
| MonRailR | MONITOR_RAIL_R | right monitor rail | architecture accepted; final fastening pending |
| MonBridge | MONITOR_BRIDGE | replaceable VESA bridge | function accepted; display holes pending |
| PCBase | PC_BASE | lower PC base | architecture accepted |
| BBBase | BACKBOX_BASE | backbox base/support | function accepted; Williams hardware pending |

## Owner-approved V32 shelf-retention identities

Owner accepted the removable shelf-retention direction on 2026-09-29. The covers therefore receive permanent functional identities; dimensions and manufacturing remain provisional. Original V32 geometry is not overwritten. Generated study documents retain legacy object names for traceability.

| Permanent code | Study legacy ID | Function | Status |
|---|---|---|---|
| S1NutCoverL | CandidateNutCover1L | S1 left captured-nut cover | function accepted; fastening/material pending |
| S1NutCoverR | CandidateNutCover1R | S1 right captured-nut cover | function accepted; fastening/material pending |
| S2NutCoverL | CandidateNutCover2L | S2 left captured-nut cover | function accepted; fastening/material pending |
| S2NutCoverR | CandidateNutCover2R | S2 right captured-nut cover | function accepted; fastening/material pending |
| S3NutCoverL | CandidateNutCover3L | S3 left captured-nut cover | function accepted; fastening/material pending |
| S3NutCoverR | CandidateNutCover3R | S3 right captured-nut cover | function accepted; fastening/material pending |

## Provisional names

The following intentionally remain without a permanent code:

- **T1 adjustable left/right metal support**
- **T2 adjustable left/right metal support**
- **T3 adjustable left/right metal support**
- **left rear fan**
- **right rear fan**
- **removable StarTech ICUSBAUDIO7D mount**
- **Arnoz plunger and its mount**
- **final RJ45/network interface**
- **final mains/master-disconnect interface**
- **final subwoofer**
- **fan guards**
- **detachable rear-door harness**

Legacy IDs such as `CROSS_BRACKET_*`, `FAN_*` and reserved envelopes remain in V32 for traceability but are not permanent part codes.

## CAD migration

The published V32 keeps legacy internal IDs so the existing FreeCAD/STEP files remain traceable. The generator now carries permanent identity metadata for future regeneration:

- `PartCode` stores the permanent code when assigned;
- `LegacyId` preserves the former internal ID;
- `PartStatus` identifies permanent vs provisional identity;
- future BOM/manifest generation should derive identity from the same source map.

This prevents silent renaming and preserves historical references.

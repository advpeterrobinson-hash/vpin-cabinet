# Renders

[English](RENDERS.md) · [Português (Brasil)](pt-BR/RENDERS.md)

> **Fast visual entry point to the current project state.**  
> Current owner-facing review: **V32** on `feat/cabinet-review-v32`.  
> **Not released for CNC or manufacturing.**

This page lets a new contributor understand the current cabinet direction without browsing the repository tree first. The complete technical package remains in [`exports/generated/cabinet-v32/`](../exports/generated/cabinet-v32/README.md).

## V32 — main cabinet

### R01 — Interior

[![V32 interior](../exports/generated/cabinet-v32/01-interior.png)](../exports/generated/cabinet-v32/01-interior.png)

Shows the transverse shelves, low PC position and internal structure. Some panels are hidden only to improve visual readability.

### R02 — Crossmembers

[![V32 crossmembers](../exports/generated/cabinet-v32/02-travessas.png)](../exports/generated/cabinet-v32/02-travessas.png)

Shows T1, T2 and T3, their replaceable guides and the monitor-support arrangement.

### R03 — Plan

[![V32 plan](../exports/generated/cabinet-v32/03-planta.png)](../exports/generated/cabinet-v32/03-planta.png)

Shows S1, S2 and S3 and the wiring-access corridors.

### R04 — Rear

[![V32 rear](../exports/generated/cabinet-v32/04-traseira.png)](../exports/generated/cabinet-v32/04-traseira.png)

Rear service door and two reference 120 mm exhaust fans.

### R05 — Replaceable guide

[![V32 guide detail](../exports/generated/cabinet-v32/05-encaixe.png)](../exports/generated/cabinet-v32/05-encaixe.png)

Detail of the removable crossmember interface. The groove is in the replaceable guide, not in the structural cabinet side.

### R06 — Front

[![V32 front](../exports/generated/cabinet-v32/06-frente.png)](../exports/generated/cabinet-v32/06-frente.png)

Coin-door reference, front controls and the still-provisional plunger reserve.

## Current review status

- V32 consolidates V29–V31.
- 45 valid solids in the current model.
- No positive-volume intersection above 0.01 mm³ in the current validation.
- This validates CAD packaging/interference only; it does **not** validate structural strength.
- Physical sessions remain paused.
- CNC/manufacturing release remains blocked.

## Part identity

Permanent part codes and provisional names are controlled in [`PART_CODES.md`](PART_CODES.md).

Visual rule:

- `T1`, `S2`, `S1SupR` = permanent identity already assigned.
- `**provisional name**` = concept that does not yet have a permanent code.
- A permanent code is never reused for another function.
- Later geometry changes preserve the code and add a revision when necessary.

## Technical files

- [V32 technical package](../exports/generated/cabinet-v32/README.md)
- [Parts list](../exports/generated/cabinet-v32/PECAS-PARTS.md)
- [FreeCAD](../exports/generated/cabinet-v32/vpin-central-v32.FCStd)
- [STEP](../exports/generated/cabinet-v32/vpin-central-v32.step)
- [Validation](../exports/generated/cabinet-v32/validation.json)

## Next visual update

The next design iteration may incorporate the captured CNC joinery proposal documented in [`CABINET_JOINERY_PROPOSAL.md`](CABINET_JOINERY_PROPOSAL.md). Until accepted and validated, no render should imply that those grooves are part of released V32 geometry.

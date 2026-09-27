# Parts

**English** · [Português (Brasil)](PECAS-PARTS.pt-BR.md)

V32 distinguishes a **permanent part code** from a **legacy internal ID**.

- Permanent code: short stable identity for an accepted part.
- Legacy ID: technical identifier retained for traceability in the published V32 model.
- **provisional name**: concept that does not yet have a permanent identity.
- A permanent code is never reused for another function.
- Geometry changes that preserve a function keep the code and advance its revision, for example `T1-R2`.

Master registry: [`docs/PART_CODES.md`](../../../docs/PART_CODES.md).

| Code | V32 legacy ID | English name | Group |
|---|---|---|---|
| SideL | SIDE_L | Left side | shell |
| SideR | SIDE_R | Right side | shell |
| Front | FRONT | Front panel | shell |
| Rear | REAR | Rear panel | shell |
| — | FAN_230 | **Left rear fan** | fan |
| — | FAN_370 | **Right rear fan** | fan |
| RearDoor | REAR_DOOR | Rear service door | door |
| Floor | FLOOR | Bottom panel | floor |
| — | FLOOR_CLEAT_18 | **Left floor support** | support |
| — | FLOOR_CLEAT_552 | **Right floor support** | support |
| S1 | SHELF_1 | Transverse shelf 1 | shelf |
| S1SupL | SHELF_SUPPORT_1L | S1 left support | support |
| S1SupR | SHELF_SUPPORT_1R | S1 right support | support |
| S2 | SHELF_2 | Transverse shelf 2 | shelf |
| S2SupL | SHELF_SUPPORT_2L | S2 left support | support |
| S2SupR | SHELF_SUPPORT_2R | S2 right support | support |
| S3 | SHELF_3 | Transverse shelf 3 | shelf |
| S3SupL | SHELF_SUPPORT_3L | S3 left support | support |
| S3SupR | SHELF_SUPPORT_3R | S3 right support | support |
| T1 | CROSS_1 | Upright crossmember 1 | brace |
| T1GuideL | CROSS_GUIDE_1L | T1 left guide | guide |
| — | CROSS_BRACKET_1L | **T1 left metal support** | bracket |
| T1GuideR | CROSS_GUIDE_1R | T1 right guide | guide |
| — | CROSS_BRACKET_1R | **T1 right metal support** | bracket |
| T2 | CROSS_2 | Upright crossmember 2 | brace |
| T2GuideL | CROSS_GUIDE_2L | T2 left guide | guide |
| — | CROSS_BRACKET_2L | **T2 left metal support** | bracket |
| T2GuideR | CROSS_GUIDE_2R | T2 right guide | guide |
| — | CROSS_BRACKET_2R | **T2 right metal support** | bracket |
| T3 | CROSS_3 | Upright crossmember 3 | brace |
| T3GuideL | CROSS_GUIDE_3L | T3 left guide | guide |
| — | CROSS_BRACKET_3L | **T3 left metal support** | bracket |
| T3GuideR | CROSS_GUIDE_3R | T3 right guide | guide |
| — | CROSS_BRACKET_3R | **T3 right metal support** | bracket |
| MonRailL | MONITOR_RAIL_L | Left monitor rail | mount |
| MonRailR | MONITOR_RAIL_R | Right monitor rail | mount |
| MonBridge | MONITOR_BRIDGE | VESA bridge | mount |
| — | PLAYFIELD_ENVELOPE | Display envelope | envelope |
| — | AUDIO_STARTECH | StarTech ICUSBAUDIO7D selected device | audio |
| PCBase | PC_BASE | PC base | pcbase |
| — | PC_ENVELOPE | PC envelope | pc |
| BBBase | BACKBOX_BASE | Backbox support/base | shell |
| — | PLUNGER_RESERVED | **Plunger reserve** | reserved |
| — | MAINS_RESERVED | **Mains inlet reserve** | reserved |
| — | RJ45_RESERVED | **Network reserve** | reserved |

## Provisional items

Bold provisional names are not necessarily disposable. They simply mean **final identity has not yet been granted**.

The current floor supports remain provisional because the captured CNC joinery proposal may eliminate or redefine their function. See [`docs/CABINET_JOINERY_PROPOSAL.md`](../../../docs/CABINET_JOINERY_PROPOSAL.md).

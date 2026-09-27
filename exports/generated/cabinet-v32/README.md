# V32 — Main cabinet

**English** · [Português (Brasil)](README.pt-BR.md)

> **Design review — not released for CNC or manufacturing.**

V32 consolidates the owner's current direction: a conventional 600 mm cabinet, three narrow transverse shelves, a low open-case PC base and replaceable interfaces. Dimensions are in millimetres.

**Quick access:** [dedicated render gallery](../../../docs/RENDERS.md) · [permanent part codes](../../../docs/PART_CODES.md) · [current CNC joinery proposal](../../../docs/CABINET_JOINERY_PROPOSAL.md).

## Part identity

V32 uses permanent human-readable codes for accepted parts, including `T1`, `T2`, `T3`, `S1`, `S2`, `S3`, `S1SupL` and `S1SupR`.

Concepts that are not yet finalized remain **provisional** and do not receive a permanent code until accepted. The master registry is [PART_CODES.md](../../../docs/PART_CODES.md).

The published V32 FreeCAD/STEP files still contain legacy internal object IDs for traceability. The source generator now carries permanent-code metadata so future regeneration can expose `PartCode`, `LegacyId`, `PartStatus`, and a separate Portuguese name.

## Gallery

### 1. Interior
![Shelves and PC](01-interior.png)

### 2. Upright crossmembers
![Crossmembers, guides and monitor support](02-travessas.png)

### 3. Service plan
![Shelves and access gaps](03-planta.png)

### 4. Rear
![Door with two exhaust fans](04-traseira.png)

### 5. Replaceable guide
![Guide detail](05-encaixe.png)

### 6. Front
![Coin door, controls and plunger reserve](06-frente.png)

For the easiest browsing experience, use the [dedicated render page](../../../docs/RENDERS.md).

## Incorporated in V32

| Element | Configuration |
|---|---|
| Body | 600 × 1308.1 mm; front/rear heights 400.05–596.9 mm; nominal 18 mm plywood |
| Shelves | S1/S2/S3: 3 × 560 × 150 × 12 mm; Y120, Y600, Y1080; underside heights Z160, Z180, Z240 |
| Wiring access | 330 mm between shelves; access from both edges |
| Crossmembers | T1/T2/T3: 3 upright pieces; 539.6 × 18 mm; 80 mm center height; Y380, Y700, Y980 |
| Guides | 6 replaceable guides; 18 × 60 × 145 mm; 18.4 mm wide × 6 mm deep groove; 12 mm backing retained |
| **Crossmember metal supports** | 6 provisional generic envelopes, 40 × 40 × 50 × 3 mm; positive support under beam |
| Audio | Owner-selected StarTech ICUSBAUDIO7D; 100 × 60 × 25 mm body shown near S1 |
| PC | PCBase 285 × 460 × 18 mm over cabinet floor; 265 × 440 × 128 mm retained PC envelope; no drawer |
| Ventilation | 2 provisional 120 mm rear-door exhaust fans; bottom intake |
| Coin door | 311.15 × 264.32 mm reference opening |
| Floor | provisional Ø139.7 subwoofer opening; 100 × 160 air intake; four nominal Ø28 auxiliary holes |

T1/T2/T3 lift upward after the monitor support and retention hardware are released. The groove is in the replaceable guide rather than the structural cabinet side. The crossmember top bevel follows the monitor plane and must eventually be represented in machining data. The shorter span accommodates the guides.

The three illustrated support-height rows are spaced at 10 mm increments. Screws, inserts/nuts, final edge distances and anti-lift retention remain provisional. Changing one crossmember height also changes the monitor support plane; do not adjust one independently without rechecking the system. CSD mounting holes have not been invented.

## Interfaces and purchases

- **StarTech ICUSBAUDIO7D:** owner-selected; purchase not confirmed. Body envelope is modelled; cable/port clearance and removable retention are still required.
- **Two 120 mm fans:** final electrical model not selected. A 25 mm frame and 105 mm hole pitch are reference geometry only. Ø116 and Ø4.5 remain provisional cut/drill decisions.
- **Fan guards and rear-door harness:** guards on accessible faces plus a detachable connector are required; not yet modelled.
- **Six crossmember supports:** concept quantity only. The generic envelope is not a purchase specification or load rating.
- **Covered terminal blocks:** retained as a distribution preference; quantity/current ratings pending.
- **Williams hardware:** legs, inner plates, backbox hinges and related fixings remain planned; complete mounting patterns are unresolved.

S3 ends at Y1230; fan bodies start at Y1265.1, leaving 35.1 mm gross clearance. Fans start at Z220; the PC envelope ends at Z182, leaving 38 mm gross clearance. Guards and wires are excluded from these clearances.

The bottom intake has 160 cm² gross area; the two circular exhaust openings total about 211 cm². This is **not** an airflow or thermal validation.

## Validation and remaining work

**45 valid solids; no positive-volume intersection above 0.01 mm³.**

The build script checks three shelves, three upright crossmembers and two fans. The drawings validate packaging and review readability, not tested load-bearing performance.

Still required:

1. complete fastening for guides, crossmembers, supports, shelves and rear door; nut/insert access and vibration retention;
2. monitor service motion/support hardware and loaded structural validation;
3. Williams leg pattern, backbox hinge/base fixings, cable passage and hinge sweep;
4. final selected-component openings for the Arnoz plunger, mains, RJ45, fan guards and subwoofer;
5. PSU/CSD dimensions, cable routing and thermal zones;
6. joinery, glass channels, lockdown bar, measured wood thickness, cutter diameter/radius, allowances and sheet layout.

The architecture direction is set for the current review. Machining is not released. Physical sessions remain paused.

The proposed self-indexing lower-cabinet CNC joinery is documented separately and is **not part of V32 geometry yet**: [CABINET_JOINERY_PROPOSAL.md](../../../docs/CABINET_JOINERY_PROPOSAL.md).

## Files

- [FreeCAD](vpin-central-v32.FCStd) — published review file; current binary predates the English-only metadata regeneration.
- [STEP](vpin-central-v32.step) — physical parts and generic hardware envelopes; display, PC body, audio body and reserved zones omitted.
- [Parts list](PECAS-PARTS.md).
- [CAD source](build_v32.py) — run with FreeCAD; writes outputs to this directory.
- [Render source](render_v32.py) — run after CAD generation with Python, NumPy and Matplotlib.
- [Validation](validation.json).

`geometry.json` is regenerated by the CAD script. Views 01/02 hide selected panels to expose internal parts; views 03–06 are dimensioned review drawings.

## References

- [WPC dimensional reference](https://github.com/jonaskello/wpc-cabinet) — dimensional facts only; external CAD not copied.
- [StarTech datasheet](https://media.startech.com/cms/pdfs/icusbaudio7d_datasheet.pdf).
- [120 mm fan dimensional reference](https://www.noctua.at/en/products/nf-a12x25-pwm/specifications) — dimensional reference, not a fan selection.
- [Cleveland solenoid](https://www.clevelandsoftwaredesign.com/pinball-parts/p/high-quality-solenoid) — mounting pattern still unconfirmed.

## Provenance

V32 consolidates V29–V31 and was published on a separate review branch derived from remote commit `9ec47db`. The pre-existing local master and owner changes were not overwritten or incorporated by that publication. Pre-V32 manufacturing geometry remained untouched.

Copyright © 2026 Peter Jr. and contributors. CERN-OHL-S-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE.md). Official source: https://github.com/advpeterrobinson-hash/vpin-cabinet .

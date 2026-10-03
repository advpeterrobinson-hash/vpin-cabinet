> V33.6.1 AUTHORITY CORRECTION: Y89/Y127, local side top minus65mm, is the CURRENT owner ergonomic authority. The V33.6 banner that called it superseded was erroneous. The horned M025 contour alone is superseded by the [front-open relief](BUTTON_RELIEF_V3361.md). Historical body below is retained; no final button drilling is released.

> HISTORICAL / SUPERSEDED: final current playfield pivot is documented in [WOOD_DOWEL_PIVOT_V32.md](WOOD_DOWEL_PIVOT_V32.md). The props, pins, bushes and steel axis below are rejected and absent from the current viewer/CAD.

# V32 — owner correction review

Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

HEAD BEFORE: `28f7eb82be90988cccd841b47a6f94de3710cd25` (local offline-viewer commit). Owner-reviewed remote HEAD: `1de1e05dafa1bc2186a11e87ffd235af48ac12fc`. HEAD AFTER is the correction commit containing this report; the delivery message supplies its full hash.

## Actual CAD and viewer

Open `exports/generated/viewer-v32/index.html` directly in a browser; no server or network is needed. Four selectable states: PLAY, SERVICE, SERVICE LEFT PROP ONLY, SERVICE RIGHT PROP ONLY. Both props and corrected buttons are visible. One-prop states are load-path review only, not service instructions or structural validation.

Corrected FreeCAD files: `exports/generated/service-correction-v32/play.FCStd`, `service.FCStd`, `service-left-prop-only.FCStd`, `service-right-prop-only.FCStd`. STEP: `current-v32.step` in the same directory. Rebuild with `bash tools/run_service_correction_v32.sh`; browser verification/screenshots with `python3 tools/check_review_viewer_v32.py`.

## Side buttons

Y0 is the outside front plane; Z follows the actual V32 side profile. Both sides mirror.

| Button | Old Y / Z mm | New Y / Z mm | Distance from front mm | Local top Z mm | Below local top mm |
|---|---:|---:|---:|---:|---:|
| Primary flipper | 255 / 270 | 89 / 350.594 | 89 | 415.594 | 65 |
| Secondary / magna | 310 / 270 | 127 / 357.230 | 127 | 422.230 | 65 |

Ergonomic centers are independent of the provisional true-pinball leaf hardware stack. Bore, shallow nut pocket, thread, leaf bracket and wire clearance require selected hardware measurement before machining. Original rearward holes are refilled in generated geometry.

## Routine hinged service

Old mechanism: vertical monitor-removal packaging and an assumed rotation study, without a modeled routine-service pivot or positive raised support.

New mechanism: one commodity M10 rear cross-axis, two plain polymer bushes, simplified plywood holder, TWO identical 18mm CNC plywood props captive on ordinary M8 upper bolts. Fixed local receivers use three scrap18mm layers each; there are no new cabinet crossmembers or shelf changes. Positive locking8mm receiver pins pass through each prop, laminated receiver and full-strength sidewall. Support does not depend on friction or balancing on an edge.

Service opening: **100 degrees from PLAY**. Prop upper-to-receiver centers: **319.495mm**, solved from actual CAD; end diameter24mm gives343.495mm overall blank length. Upper pivot closed Y/Z788.290/445.150; raised955.142/818.097; lower receiver985/500. Rear axis Y/Z1028.186/561.621. Each prop stows forward alongside its holder rail, positively pinned to an integral plywood stow ear; free-end closed Y/Z473.559/390.183.

Sequence: remove glass and release lockdown; withdraw BOTH stored receiver pins before lifting (otherwise their heads obstruct the sweep). Lift manually with props positively stowed. Hold the assembly, withdraw stow pins, swing props toward the player and down into the receivers; insert and lock BOTH receiver pins. Continue manual support until both are engaged. Exact pin grip/rating and fastener specifications remain provisional.

Support pieces: **2 plywood props**. Other local plywood:6 receiver blanks and2 display spacers. Commodity metal pieces: **27** (1 M10 axis,6 axis locknuts,6 axis washers,2 M8 upper bolts,2 upper locknuts,6 upper washers,2 receiver locking pins,2 stow locking pins). Plus2 nonmetal plain bushes. **Custom metal parts required:0.** The display has12mm normal spacers to clear the relocated leaf hardware, leaving4mm modeled glass clearance.

UCFL202 retained: **NO**, plain bushes replace bearing housings. Custom15mm journals retained: **NO**, ordinary threaded M10 cross-axis replaces them. Steel prop rods retained: **NO**, identical CNC plywood props replace them. Legacy clevis/keeper assemblies and metal cheek plates are retired from CURRENT architecture. Historical v18/v19 files remain unchanged; current config explicitly supersedes them. This follows the V28 simplification direction and the owner's explicit plywood-prop correction.

## Required images

Generated directly from the actual CAD-derived viewer, with dimensions:

1. `exports/generated/viewer-v32/01-player-left.png`
2. `exports/generated/viewer-v32/02-player-right.png`
3. `exports/generated/viewer-v32/03-play-oblique.png`
4. `exports/generated/viewer-v32/04-service.png`
5. `exports/generated/viewer-v32/05-side-detail.png`
6. `exports/generated/viewer-v32/06-closed-detail.png`

Inspection views hide selected shell panels/display only to expose the mechanism; CAD remains complete. Blue primary and orange secondary heads identify finger locations. Raised views show both wood props and positive pins; closed detail exposes their forward stow.

## Validation and limits

- Ergonomic drift negative control: PASS; primary above110mm or secondary above150mm rejected, independent of bore diameter.
- Missing-support negative control: PASS; absent modeled axis, bush, prop, positive pin or raised-state prop is rejected. Seven deliberate invalid cases reject correctly.
- Relevant existing V32 checks: PASS; original39-check source preserved; updated36 CAD checks pass. Valid/recomputed saved solids, mirrored sides/props, exact preservation of other approved solids, frozen three shelves/low PC/no drawer, twelve overhead tool columns and three loaded shelf routes checked.
- Opening sweep sampled every2degrees; forward prop deployment21 samples. No positive-volume conflicts in modeled states/motions. Stored receiver-pin interference is deliberately detected. This is sampled packaging verification, not continuous motion, connector/harness or load proof.
- Backbox clearance uses a conservative780mm rectangular envelope from existing v06/v12 data; the complete actual V32 backbox is not modeled. At100degrees the raised display has approximately4.7mm clearance to that envelope. Final backbox interface still requires verification.
- Four browser states and six rendered views are verified in `exports/generated/viewer-v32/browser-verification.json`; detailed CAD evidence is `exports/generated/service-correction-v32/validation.json`.

**MANUFACTURING BLOCKED: YES.** Prop geometry is DESIGN-PROVISIONAL. No fabrication or single-prop structural proof is claimed. Full-moving-load proof for either prop and the asymmetric cradle load path remains mandatory. The18mm-wide prop neck and1mm modeled stow margin require physical qualification; no load capacity is inferred from collision-free CAD.

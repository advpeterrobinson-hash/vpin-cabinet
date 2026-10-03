# V34 — simplified backbox design candidate

HEAD BEFORE: `0993d9768582290915f7166c53507ffd2aa434b6`.
HEAD AFTER: the commit containing this report (resolve with `git log -1 --format=%H -- exports/generated/backbox-v34/README.md`). A commit cannot embed its own hash.

**Geometry/service screening passes. Manufacturing and physical qualification remain BLOCKED.**

[26 native CAD review views](review.html) · [Offline viewer](../viewer-v32/index.html) · [English manual](../../../docs/ASSEMBLY_MANUAL.md) · [PT-BR manual](../../../docs/ASSEMBLY_MANUAL.pt-BR.md) · [Native assembly](play.FCStd) · [Wood BOM](manufacturing-bom.md) · [Hardware catalog](../../../config/hardware_catalog_v34.json).

## Tukkari-first audit

[Official assembly guide](https://www.tukkari.eu/advisor/assembly-guide-vpin-cabinet-essential-flat-pack) and [official kit description](https://www.tukkari.eu/p/widebody-virtual-pinball-cabinet-vpin-essential-flat-pack-kit) were inspected, including backbox steps 1,5,9,13–16,19. No source CAD, images or proprietary manufacturing geometry is redistributed. Original project geometry is independently dimensioned. See [source register](sources.json) and [mandatory deviation report](tukkari-first-audit.json).

- Monitor: public single plate uses four metal brackets. Owner explicitly requires guides/stops/top capture instead. This is an owner-directed adaptation, **not a claim that Tukkari uses our captured mechanism**.
- Lower panel: public combined panel is bent metal. Our single flat plywood panel cannot carry central VESA bosses through a large visual aperture. The DMD mounts on the **front face** of the structural panel, with bolts through the panel from rear; its own housing/bezel supplies the visible face. No hidden rear adapter.
- Glass: public front window/channel concept supports a simple seat. The exact front-tilt/one-strip mechanism requested here was not established by the public guide; our independently checked fit follows the owner sequence.
- Top: public direct top/side assembly is retained in principle. The source explicitly says backbox is not glued. Glue here is an owner-authorized departure, plus ordinary mechanical fasteners; no proprietary connector machining.

The permanent rule is in [AGENTS](../../../AGENTS.md). Added complexity requires public equivalent, evidence, measured conflict, failure of direct adaptation and minimum deviation.

## Monitor / top

One **M074 BB_MONITOR_PLATE**, 752×448.8×18 mm, enters from TOP before the top is fitted. Two identical **M075** 12×40×30 mm stops screw directly to side panels (two screws each). Two inside-face **4 mm** guides locate the plate. Guide width is measured plate thickness + coupon clearance; 18.4 mm is a review assumption, never machining authority. R2 guide ends extend 2 mm below the seated plate. The top closes the guide ends. **Zero plate-retention brackets. No normal plate removal.**

Load: monitor → VESA bolts/washers → plate → side guides/lower stops → side panels/shell. Fold normal load bears into guides; top resists upward escape. All physical strength, actual plywood and screw holding require qualification.

VESA 75×75 and 100×100: reference 5 mm-wide rounded slots, total15 mm length for **±5 mm** vertical travel. Final thread/diameter is selected-monitor dependent. A single400×100 R8 service opening retains the VESA load region. Depth adjustment is **0/3/6/9/12 mm commodity spacers/washers**, default12; screws must have correct purchased thread engagement. No wood depth mechanism.

Top: restored single top at unchanged outer envelope; shallow capture + glue + **4 direct side screws**, two per side. Outside driver corridors are clear. Four pocket screws were considered but not selected: actual Kreg jig/model/drilling unknown. No invented pocket coordinates; no corner cleats. Direct screws and edge pilots remain purchased-hardware/coupon/manual-jig holds.

Monitor service: remove two glass-strip screws and strip; front-remove glass; support monitor; remove four VESA bolts through open rear doors; raise monitor to **+5 mm** clearance position and withdraw FRONT. Shell top and captured plate remain fixed. 740×450×100 reference monitor is retained; rear socket corridors checked. Maximum structural planning monitor mass12 kg, not a certification.

### 12-first screen

Provisional E=4000 MPa, 650 kg/m³,2g planning screen including plate mass. The4 mm deflection limit preserves a residual glass clearance from the ≥10 mm modeled gap. Simplified beam calculations are screening, not orthotropic plywood FEA or tested joint capacity.

| Monitor plate stock mm | Screen deflection mm | Pass ≤4 mm |
|---:|---:|---|
| 12 | 11.270 | False |
| 18 | 3.519 | True |

18 mm selected. Purchased plywood stiffness/strength, washer load, guide bearing and edge-fastener retention are **physical holds**.

## DMD / speakers

One **M076 BB_DMD_SPEAKER_PANEL**,752×203×18 mm. Install DMD on FRONT of this panel off the cabinet; bolt from rear through VESA75 reference slots. **±2 mm** vertical adjustment: reference5 mm width +4 mm travel =9 mm overall. The earlier ±5 target does not clear the floor; it is not claimed. DMD body plus any spacers must fit **400×200×45 mm total occupied reserve**. Final15.6-inch display aperture, dimensions, thread and depth remain PURCHASE BEFORE FINAL CUT. If it lacks VESA, optional two strips/printable brackets require a selected-part study and are excluded from minimum hardware.

Speakers attach directly to the same panel; provisionalØ130 reference apertures. **Rear driver depth must be≤60 mm** in this architecture. The former103 mm reserve intersects protected rear intake baffles. No universal speaker compatibility claim; exact speaker diameter/pitch/body must be bought before final panel cuts.

Four direct **side-operated M4-family bolts into captive metal cross-dowels** secure/locate the panel in shallow side rebates. Ordinary tools from the exterior sides; no frame or cleat stack. Front removal with DMD/speakers attached passes. Screws/edge bores are hardware-dependent, guided manual finish from FACE_A datum, no CNC flip. Side installation clearance must exist at the actual location.

| Lower panel stock mm | Fold deflection mm | Pass ≤4 mm |
|---:|---:|---|
| 12 | 11.008 | False |
| 18 | 3.497 | True |

Screen uses6 kg combined payload,2g, own mass, conservative centre loading and variable net section subtracting openings. **Speaker mount: HARDWARE_DEPENDENT.**

## Backglass

Study glass **752×459×4 mm**, not a released cut size. Final3–4 mm tempered glass dimensions derive from selected liners/fit; value remains null for final CNC/glass order. Left/right6 mm front rebates retain12 mm side skin. Two mm side/bottom liners and a dedicated1 mm replaceable upper front cushion are references, not measured stock. The strip is offset1 mm to provide its cushion space.

One **M037 bottom seat**,18 mm stock, groove8 mm deep leaving10 mm bottom web; positive lower front lip **6 mm**. One **M077 upper strip**,12 mm stock, **2 upward screws** accessible from front/below. Top glass overlap **8.2 mm**, side overlap4 mm, upward clearance **3.8 mm**. The6 mm lower lip exceeds available upward escape even with2 mm planning allowance. Lower/upper lips capture front-normal motion; side rear seats and bottom/top close other directions. No gravity/friction-only retention.

Install FRONT: lower edge in padded groove, tilt into seats, install upper strip and screws. Remove: strip out → lift1 mm → tilt top forward10° → lift additional6 mm → withdraw. Top/plate remain installed. Native collision checks cover continuous tilt, sampled removal, bounded translations and rotations against retention barriers; rigid capture persists under whole-backbox upright/fold/laid orientation. **PASS geometric containment, not impact/tempered-glass/fastener certification.**

## Validation / protected systems

[Native geometry checks](geometry-validation.json): 28 checks. [Independent checks](independent-validation.json): 1184 checks, including exact manufacturing reconstruction, native invariants, continuous front-glass tilt, continuous two-door0–100° sweeps, fan-loop samples, and negative stock-policy controls. Differential backbox fold0–90° continuous certification plus all requested discrete angles passes, with main playfield glass and matrix removed, doors closed, locks parked. Backglass and populated lower panel remain installed. No routine electronics disconnection. Existing unchanged mechanisms retain their prior validation; changed geometry is tested against them, not silently excluded.

428 unrelated installed objects are unchanged by source-copy/Boolean regression. WPC axisY1066.8/Z508, outer780×723.9,210 lower depth/Y1146 floor, doors/fans/locks/parking, SW01/SW02, main playfield/underfront/shelves/matrix remain unchanged. Raised-playfield PRIMARY SUPPORT remains the inherited operational HOLD. Universal moving-backbox wiring remains a physical harness qualification hold.

Local central rear clearance gained: **32 mm** from old rail/shoe rearY1290 to new plate rearY1258. This is not universal recovered volume. Upper side toy reserve shrinks from39 to **24 mm depth** behind the full plate; explicitly changed reserve only, no toy-specific holes.

## Retired objects / hardware

All following names are absent from current native and installed viewer geometry (history remains in Git):

- `BB_GlassLinerL`
- `BB_GlassLinerR`
- `BB_TopFrontRail`
- `BB_GlassLowerRail`
- `BB_GlassLowerPad`
- `BB_GlassTopRetainer`
- `BB_GlassTopPad`
- `BB_GlassRetainerFastenerReserve0`
- `BB_GlassRetainerFastenerReserve1`
- `BB_MonitorRail0`
- `BB_MonitorRailCleatL0`
- `BB_MonitorRailCleatR0`
- `BB_MonitorRail1`
- `BB_MonitorRailCleatL1`
- `BB_MonitorRailCleatR1`
- `BB_MonitorCarrier0`
- `BB_MonitorDepthShoe00`
- `BB_MonitorDepthBoltReserve00`
- `BB_MonitorDepthShoe01`
- `BB_MonitorDepthBoltReserve01`
- `BB_MonitorCarrier1`
- `BB_MonitorDepthShoe10`
- `BB_MonitorDepthBoltReserve10`
- `BB_MonitorDepthShoe11`
- `BB_MonitorDepthBoltReserve11`
- `BB_MonitorClampReserve160994`
- `BB_MonitorClampReserve1601134`
- `BB_MonitorClampReserve440994`
- `BB_MonitorClampReserve4401134`
- `BB_ReplaceableVESAPlate`
- `BB_DisplayReplaceableBezel`
- `BB_LowerCassetteFrame`
- `BB_SpeakerBaffleL`
- `BB_SpeakerBaffleR`
- `BB_DMDReplaceableBezel`
- `BB_DMDRearAdapter`
- `BB_DMDDepthTie0`
- `BB_DMDDepthTie1`
- `BB_CassetteFixedCleatL0`
- `BB_CassetteBoltReserveL0`
- `BB_CassetteFixedCleatL1`
- `BB_CassetteBoltReserveL1`
- `BB_CassetteFixedCleatR0`
- `BB_CassetteBoltReserveR0`
- `BB_CassetteFixedCleatR1`
- `BB_CassetteBoltReserveR1`
- `BB_MonitorStopRail`
- `BB_StopAdjuster0`
- `BB_StopTip0`
- `BB_StopInsert0`
- `BB_StopLocknut0`
- `BB_StopAdjuster1`
- `BB_StopTip1`
- `BB_StopInsert1`
- `BB_StopLocknut1`
- `BB_StopRailRetention0`
- `BB_StopRailRetention1`

Retired hardware IDs: **F24, F25, F26, F27, F28, F31, F57, W09, I09, I10, I11, W10**. Their current quantities are0/statusRETIRED; historical catalog remains unchanged. [Complete attachment/90° part audit](attachment-audit.json) records retained frame, door and ventilation functions separately; these protected parts are not monitor-support leftovers.

## Counts / mass / release

| | Before | After |
|---|---:|---:|
| Wood manufacturing pieces |104|76|
| CNC plywood pieces |98|70|
| Solid blocks (4 SW01 +2 SW02) |6|6|
| Canonical families |61|48|
| Finished wood nominal kg @650 |61.243946|61.923112|

**28 fewer wood pieces. Mass increases 0.679166 kg**; no claimed mass reduction. Actual B-rep volumes, not bounding boxes. Wood LOW550=52.396 kg / HIGH750=71.450 kg. Hardware mass unknown, not zero. Plywood exactly12/18; no new stock. Existing outside-backbox source pieces remain bitwise authority-equivalent; changed pieces reconstruct with max0.00000000 mm³ union difference.

Manual: 16 stages / 56 steps;25 authoritative backbox steps, EN/PT-BR. Viewer service motions separate plate assembly from monitor service. Generic assembly animations remain schematic fade/seat, not claimed insertion validation. [Browser evidence](browser-validation.json) and [promotion evidence](validation.json) bind final files. [Packaging](packaging.json) is a preliminary one-piece-per-layer projection, not shipping qualification; no updated production nesting or CAM.

Pending: actual monitor/DMD/speakers/glass/liners, VESA/thread engagement/spacers, top/stop/panel fasteners, WPC purchased hardware, actual plywood stiffness/thickness, fit coupon, supplier/final operation checks, structural/ergonomic qualification. **FULL-SHEET RELEASE BLOCKED. No G-code.**

Rebuild: `python3 tools/rebuild_backbox_v34.py`, then browser QA with local Playwright/Chrome, `python3 tools/backbox_v34_report.py`, `python3 tools/check_backbox_v34.py`. Exact hardware machining is not released by successful export.

Original project work: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet. Tukkari linked sources retain their copyright; no source geometry imported.

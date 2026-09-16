# Active engineering baseline — 2026-09-16

Engineering packaging only. No manufacturing release or structural certification.

## Source and build

`config/*.json` + selected Python builders → **fresh** `cad/active/vpin-active.FCStd` → future separately gated manufacturing document.

`make build-current` must not read the historical `cad/master/vpin-master.FCStd`. That working file is preserved, including owner modifications. The fresh runner creates current systems only; it never deletes or reparents the old document graph. Current builders accept a caller-owned document. Historical standalone entry points remain available for investigation, not procurement or release.

The active input set is cabinet structure v20 (shell/joinery/glass only), structure v14 (backbox), playfield mechanics v18, fixed anchors v19, cabinet service v21 (legs only), rear CPU v24, and rear utility v26 (selected A rear-face interfaces). Older PC/leg fields in shared versioned configs are legacy inputs used only by standalone historical builders.

The engineering shapes are regenerated from configs, with the cabinet datums also recorded in a spreadsheet. They are not an editable manufacturing feature tree: changing a spreadsheet cell alone does not regenerate boolean solids. Change configs and rebuild. A production document must resolve measured stock, machining features and hardware before export.

## Selected dimensions

| Item | Current nominal baseline |
|---|---|
| Body | 600 × 1308.1 mm; front/rear heights 400.05/596.9 mm |
| Side material | 18 mm marine plywood; 564 mm clear width; no OLED pockets |
| Backbox | 780 × 254 × 723.9 mm; 90 mm overhang each side |
| Playfield envelope | 560 × 970 × 55 mm; ≤12 kg; replaceable VESA interface |
| CPU case | Purchased envelope 265 X × 440 Y × 128 Z mm; mounting holes unmeasured |
| CPU shelf | 285 × 460 × 18 mm, bottom Z135; Y830..1290 stowed |
| Extension | 450 mm; shelf Y1280..1740; case Y1290..1730 |
| CPU aperture | X130..470; Z110..350; 340 × 240 mm |
| CPU door | X118..482; Z98..362; 15 mm thick; 105° outward |
| Utility | Mains/master disconnect + optional Ethernet; selected A rear face; underside B rejected |

The PC case is 95.89% beyond the **exterior** rear plane at full extension; 18.1 mm remains inside. The shelf retains 28.1 mm overlap. Full extraction uses the slide disconnect and disconnected cables. No dedicated PC cable-loop mechanism is specified.

The rear-view left hinge is at high X (X482), with its axis at the door's exterior face (Y1323.1). Negative rotation about +Z swings the door behind the cabinet. This is a packaging axis; a measured hinge/gasket stack must prove it physically.

## What is retained and what remains provisional

Keep the three low shell crossmembers until stiffness and rail load-path tests justify removal. Keep the cradle's two longitudinal rails, three ties, rear laminated beam, pivot doublers and two independent safety stays. Keep local fixed safety/strut/landing reinforcement; landing/latch doublers are now combined into one union per side, preserving both load zones.

Removed from active generation: old display-specific service systems; bulky leg doublers; integrated wheel envelopes; front drawer/subrails; lift-out sled/locator blocks; center/wide rear studies; dedicated rear CPU harness ghost. The active PC has one board, two slides, two compact support rails and one retainer envelope.

Unresolved engineering includes measured rail clamp/bolt sizing and proof load, rear panel stiffness, complete measured hinges/latches, leg exterior envelope, full backbox fold sweep, fan/cable openings, display carrier/bezel closure and detailed joinery. The backbox and load interfaces remain packaging, not fabrication parts. Existing overlapping nominal joints must become matched captured cuts after stock/coupon validation.

## Assembly and service

CNC prelocates structural joints, holes, inserts, labels and alignment marks. Home assembly is identify, dry-fit, square, glue, bolt, finish, install and proof-test. No transfer-drilling critical hardware is permitted as the normal process. Do not buy CNC wood from packaging solids.

PC service: isolate mains, open rear door, release retainer, extend shelf, service, dress/disconnect ordinary cabling as needed, stow and latch. Playfield remains closed.

Raised playfield: isolate power and engage **both** independent positive stays. Gas struts assist lifting only. Heavy PC/GPU parts require positive restraint. Use compact steel-backed leg connections; playing load rests on levelers. Mobility uses removable external skates.

Mains terminals must remain inside a separate touch-safe enclosure. Small metal interface carriers are not safety enclosures. DOF requires an independent service-disable path. Electrical sizing and protection require a later qualified electrical design; the model contains only envelopes.

## Release gates

`bom/HARDWARE_FREEZE_V25.csv` controls measurement dependencies. Purchased case envelope does not freeze mounting points. Local metal fabrication needs dimensioned drawings and measured mating stacks. All part machining records stay BLOCKED until actual stock, tooling, coupon, hardware, assembly fit, proof tests and owner manufacturing approval are recorded.

The generated inventory is an engineering audit of shapes and placements. Axis-aligned bounds of rotated parts are **not** finished cut sizes. The part manifest separates blank/local dimensions and pending operations from these global bounds. Manufacturing exports must reject incomplete records.


## Visual review

Open `exports/generated/review/index.html` for the A/B comparison, service and load-path views and the active solid inventory. In FreeCAD run `tools/active_review.FCMacro` for exterior, rear elevation, door-open/stowed, extended and interior presets. The original master is untouched. Actual purchased external leg shapes are not available, so bracket-envelope clearance is proven but external leg/hinge clearance still needs measurement.

Owner selected [v26 rear-face A](REAR_UTILITY_V26.md). Two localized generic apertures avoid protected joints and rear leg keepouts; no underside utility remains. Component-specific patterns and CNC release remain measurement-blocked. CPU height, aperture and outward swing are preserved.

The active wooden register is now 36 objects (formerly 40), after removal of two decorative fascias and combination of two overlapping doubler pairs. Two bottom-seated 18 mm rails, four identical angle clamps and underside backing plates provide the modeled slide load path; fastener capacity and proof tests remain open.

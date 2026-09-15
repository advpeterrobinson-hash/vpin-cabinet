# Backbox mounting v0.12 — shelf alignment, secure service access, and reusable display carriers

Status: engineering provisional; not manufacturing-ready.

## Structural correction / confirmation

The backbox is **not** intended to hang from the side hinges when upright. The Williams/Bally WPC arrangement uses a horizontal rear shelf/crossmember at the top rear of the main cabinet. The backbox floor rests on that shelf.

Two lock bolts pass through access holes in the backbox floor and thread into captive nuts in the rear shelf. Their job is to clamp the backbox down in the operating position so it cannot tip or rock. The side hinges provide the folding pivot and transport function.

The final flat-pack design therefore treats the following as one matched interface:

1. main-cabinet rear shelf;
2. backbox floor;
3. central folding-harness opening;
4. reserve harness opening;
5. two upright lock-bolt centers;
6. rear-wall datum;
7. common left-right centerline.

The mating features must **never** be independently dimensioned from the left/right edges of the two different-width parts. The main cabinet is 580 mm wide and the backbox is 780 mm wide, so their side edges differ by 100 mm per side. The correct shared datums are the rear edge/back-wall plane and common centerline.

The current engineering layout uses lock-bolt centers at ±180 mm from the shared centerline. That maps to 110/470 mm from the left edge of the 580 mm shelf and 210/570 mm from the left edge of the 780 mm backbox floor. The numbers remain provisional until FreeCAD collision/layout validation, but the shared-datum method is non-negotiable.

The main shelf receives 11.9 mm nominal holes with underside 3/8-16 T-nuts or equivalent metal-backed captive threads. The backbox floor receives larger 25.4 mm access holes on the exact same axes so the hand-accessible lock bolts can engage the shelf threads.

## Cable-passport alignment

The primary 90 x 50 mm folding harness passage is centered on the common cabinet/backbox centerline. A secondary 60 x 40 mm reserve passage is offset to one side. Both openings are duplicated in the shelf and backbox floor from the same rear-edge datum so they overlap when the backbox is upright.

This is essential: the fold harness must not rub on a partial overlap or step between two separately laid-out openings.

## Closed backbox with keyed rear service door

The backbox is **closed in normal use**. It is not an open-backed display rack.

However, serviceability should not require dismantling the front every time a fan, cable, LED module or toy connection needs attention. The revised architecture therefore uses a **fixed structural rear frame surrounding a gasketed keyed service door**.

The service door is not the primary shear member. Structural stiffness comes from:

- 18 mm perimeter panels;
- fixed rear framing around the service aperture;
- dedicated upper and lower rear crossmembers;
- fixed upper fan panel;
- the internal monitor/DMD rail subframe tied to those fixed members.

Current provisional service opening is approximately 520 x 460 mm, closed by a minimum 12 mm plywood door. The baseline hardware is a continuous/piano hinge plus a keyed cam/quarter-turn panel lock. A two-point/compression lock may be substituted if prototype testing shows it improves anti-rattle or sealing.

The two 120 mm exhaust fans remain on the **fixed upper rear panel**, not on the door. This keeps fan wiring stationary and avoids compromising the ventilation layout whenever the door is opened.

Rear service access should expose the backglass/DMD cables, carriage locking hardware, LED controllers, low-voltage toy wiring, fan controller/wiring, filters and strain-relief points. A complete display replacement remains front-removable by design.

## Reusable backglass monitor mount

The permanent backbox must not be tied to one TV chassis or one VESA center height.

The proposed system uses a rear-anchored aluminium T-slot/service subframe:

- two fixed 20 x 40 mm vertical T-slot rails (or equivalent slotted structural rails) on fixed structural crossmembers/perimeter members;
- independent upper backglass and lower DMD carriages;
- adjustable brackets/depth arms with locking T-nuts;
- removable universal VESA adapter plates;
- replaceable front bezels/filler frames.

The backglass carriage must provide three adjustments:

- **vertical:** at least 160 mm total adjustment so different VESA center heights can be accommodated;
- **front/back:** carrier plane adjustable roughly 100–215 mm forward of the rear inner plane so the screen face can be brought exactly to the bezel datum despite different chassis depths;
- **horizontal centering:** at least 50 mm total fine adjustment.

The universal upper plate should support at least VESA 75x75, 100x100, 200x100 and 200x200. If a future display uses a different pattern, only the removable plate should need replacement.

Adjustment cannot depend on friction alone because the backbox rotates through approximately 90° for transport. Final adjustment points require positive locking hardware and a secondary stop/capture feature so the monitor cannot slide when the backbox is folded.

The whole monitor should be removable through the **front** of the backbox without removing the rear service door or structural frame. Rear access is for cables, adjustments and service, not for sacrificing the structure.

## Reusable DMD / FullDMD mount

The DMD carrier is independent of the main backglass carrier, although both may share the rear rail subframe.

Target DMD service envelope: approximately 450 x 230 x 80 mm. This is intended to support:

- 15.6-inch 16:9 FullDMD displays;
- smaller traditional-DMD-aspect screens using a replaceable bezel;
- VESA 75x75 / 100x100 monitors;
- non-VESA LCD panels using a replaceable tray/edge-clamp adapter.

The DMD carriage gets its own vertical and depth adjustment, and its own removable bezel. Replacing the DMD must not require moving the speakers. The speaker baffle is therefore a separate removable structural/cosmetic panel rather than part of either display's load path.

## Safety, pests and children

The rear service door is keyed. Internal access should not be available to a curious child without a key or tool.

The enclosure remains guarded/sealed with:

- rigid finger guards over fan openings;
- fine removable insect mesh/filter;
- gasketed rear service door;
- gasketed backbox-floor/rear-shelf seam;
- split compression/gland-style cable passports;
- blanked reserve passport when unused;
- no exposed mains screw terminals;
- any unavoidable mains splice inside a separate tool-access-only enclosure that remains closed even when the rear door is open.

Any design change that creates reachable mains potential is considered a blocking shock hazard until corrected.

## 32 inch vs 28 inch backglass

For this project, **31.5/32 inch 16:9 is the preferred backglass class**.

The 780 mm backbox was deliberately enlarged to support this size without forcing unusually narrow models. A current example, LG 32SR50F, is 731.8 x 440.5 x 45.0 mm without its stand and fits inside the 740 x 450 x 100 mm service envelope. A 28-inch Samsung UR55 is 638.8 x 374.0 x 64.0 mm and also fits, but leaves substantially more unused bezel/filler area.

A 32-class screen therefore uses the available backbox width better and gives a more convincing backglass presentation. The mount is intentionally **not** 32-inch-only. If replacement supply changes years from now, a 27/28-inch screen can be fitted by sliding the carriage, adjusting depth/height, and replacing only the bezel/adapter.

## Current recommendation

- Design and visually proportion the backbox around a 31.5/32-inch backglass.
- Keep the backbox fully enclosed during normal use.
- Provide a gasketed keyed rear service door inside a fixed structural rear frame.
- Do not make any permanent wood cut depend on one exact monitor's VESA center.
- Preserve the 740 x 450 x 100 mm service envelope.
- Use the adjustable rail/carriage system so 27/28-inch displays remain valid future fallbacks.
- Keep DMD mounting fully independent and similarly adjustable.

The next FreeCAD stage must model the shelf/floor matched interface, fixed rear structural frame, keyed service door envelope, fan panel, and adjustable monitor/DMD carriage envelopes before final CNC geometry is frozen.

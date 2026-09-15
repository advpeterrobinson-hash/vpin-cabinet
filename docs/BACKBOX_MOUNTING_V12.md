# Backbox mounting v0.12 — shelf alignment and reusable display carriers

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

The final primary passage must not remain an open brush-only hole. It should use a tool-removable split compression cable-entry/gland plate or equivalent elastomer insert around the actual bundle. The reserve passage remains closed by a gasketed removable blank until needed.

## Reusable backglass monitor mount

The permanent backbox must not be tied to one TV chassis or one VESA center height.

The proposed system uses an internal aluminium T-slot/service subframe inside a **fully closed wooden backbox**:

- two fixed 20 x 40 mm vertical T-slot rails (or equivalent slotted structural rails);
- dedicated top/bottom crossmembers or structural cleats carrying the display loads into the perimeter frame;
- independent upper backglass and lower DMD carriages;
- adjustable brackets/depth arms with locking T-nuts;
- removable universal VESA adapter plates;
- replaceable front bezels/filler frames.

The T-slot rails are **not** a substitute for the backbox structure and the backbox is not open-backed. A fixed rear plywood panel remains captured into the frame as a continuous shear diaphragm. The adjustable metal subframe carries monitor loads through dedicated crossmembers/cleats; the rear panel is not the sole monitor support.

The backglass carriage must provide three adjustments:

- **vertical:** at least 160 mm total adjustment so different VESA center heights can be accommodated;
- **front/back:** carrier plane adjustable roughly 100–215 mm forward of the rear inner plane so the screen face can be brought exactly to the bezel datum despite different chassis depths;
- **horizontal centering:** at least 50 mm total fine adjustment.

The universal upper plate should support at least VESA 75x75, 100x100, 200x100 and 200x200. If a future display uses a different pattern, only the removable plate should need replacement.

Adjustment cannot depend on friction alone because the backbox rotates through approximately 90° for transport. Final adjustment points require positive locking hardware and a secondary stop/capture feature so the monitor cannot slide when the backbox is folded.

The whole monitor should be removable through the **front** of the backbox without removing the fixed rear wall. Keeping the rear wall fixed preserves stiffness while still making screen replacement straightforward.

## Closed enclosure, pest exclusion and child safety

The backbox is designed as a **closed enclosure**, not an open rack.

Baseline structure:

- nominal 18 mm plywood side/top/floor perimeter;
- fixed rear structural plywood shear panel, minimum 12 mm;
- rear panel captured in dados/rabbets and fastened as final CNC joinery requires;
- display rail cage tied into dedicated crossmembers/perimeter structure rather than relying on the rear skin alone.

Normal display replacement is through the front. There is no need for a large removable rear panel. If a small rear service hatch is eventually justified, it must require a tool to open and use captive machine screws/tamper-resistant Torx or a keyed lock; hand-removable rear panels are prohibited.

The front also remains closed/protected:

- backglass display behind a removable 3–4 mm tempered-glass window where practical (clear polycarbonate may be used when impact resistance is preferred);
- DMD behind a closed window/bezel;
- speaker openings use perforated metal/finger guards plus acoustic material, with insect screen behind where acoustics/airflow permit.

For insects and dust:

- use a replaceable closed-cell EPDM/foam gasket around the backbox-floor/rear-shelf mating perimeter;
- use fine removable insect mesh/filter material behind ventilation openings, target mesh opening <=1.0 mm;
- keep the reserve cable passport gasketed and blanked when unused;
- use a split compression/gland interface around the active folding harness rather than leaving a permanent open slot;
- oversize vent free area because fine mesh/filtering reduces airflow.

This is not intended to claim an environmental/IP rating. The goal is practical exclusion of insects, fingers, dust and dropped objects without compromising cooling or serviceability.

## Electrical touch-safety policy

No exposed mains-voltage terminals are permitted inside normal backbox service space.

The preferred architecture keeps backbox auxiliaries on SELV/DC buses (fans on fused 12 V AUX, logic/LEDs on their documented low-voltage rails). The backglass monitor may still require mains power, but its feed must be a fully insulated jacketed cable terminating in a touch-safe enclosed connector/receptacle. Any mains splice or terminal block, if ultimately unavoidable, belongs inside a tool-access-only enclosed junction compartment.

Rear fan openings require rigid finger guards plus insect mesh/filter, with no direct finger/probe path to energized parts. Exposed conductive metal is bonded to protective earth where required by the final electrical design.

## Reusable DMD / FullDMD mount

The DMD carrier is independent of the main backglass carrier, although both may share the internal rail subframe.

Target DMD service envelope: approximately 450 x 230 x 80 mm. This is intended to support:

- 15.6-inch 16:9 FullDMD displays;
- smaller traditional-DMD-aspect screens using a replaceable bezel;
- VESA 75x75 / 100x100 monitors;
- non-VESA LCD panels using a replaceable tray/edge-clamp adapter.

The DMD carriage gets its own vertical and depth adjustment, and its own removable bezel. Replacing the DMD must not require moving the speakers. The speaker baffle is therefore a separate removable structural/cosmetic panel rather than part of either display's load path.

## 32 inch vs 28 inch backglass

For this project, **31.5/32 inch 16:9 is the preferred backglass class**.

The 780 mm backbox was deliberately enlarged to support this size without forcing unusually narrow models. A current example, LG 32SR50F, is 731.8 x 440.5 x 45.0 mm without its stand and fits inside the 740 x 450 x 100 mm service envelope. A 28-inch Samsung UR55 is 638.8 x 374.0 x 64.0 mm and also fits, but leaves substantially more unused bezel/filler area.

A 32-class screen therefore uses the available backbox width better and gives a more convincing backglass presentation. It is also a mainstream size class with inexpensive VESA-equipped choices. 28-inch 16:9 monitors exist, but are relatively often premium/4K gaming or office products rather than the inexpensive FHD class we need.

The mount is intentionally **not** 32-inch-only. If replacement supply changes years from now, a 27/28-inch screen can be fitted by sliding the carriage, adjusting depth/height, and replacing only the bezel/adapter.

## Current recommendation

- Keep the backbox fully closed and structurally diaphragm-braced at the rear.
- Design and visually proportion the backbox around a 31.5/32-inch backglass.
- Do not make any permanent wood cut depend on one exact monitor's VESA center.
- Preserve the 740 x 450 x 100 mm service envelope.
- Use the adjustable rail/carriage system so 27/28-inch displays remain valid future fallbacks.
- Keep DMD mounting fully independent and similarly adjustable.
- Keep all internal access tool-controlled, finger-guarded, and free of exposed mains terminals.
- Treat ventilation, cable passports and speaker openings as filtered/guarded penetrations rather than open holes.

The next FreeCAD stage must model the shelf/floor matched interface, fixed rear shear panel, adjustable monitor/DMD carriage envelopes, guarded ventilation openings, gasketed cable-passport interfaces and folding keepouts before final CNC geometry is frozen.

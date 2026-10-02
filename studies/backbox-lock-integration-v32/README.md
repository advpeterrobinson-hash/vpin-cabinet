# V32 rear-operated upright locks and complete backbox integration

The selected solution is **Option B: two rear-operated, loss-protected hand-knob clamps at X130/X470, Y1260**. It moves the provisional locks 72 mm rearward and 10 mm inward on each side and leaves the cassette, DMD, speakers, display, glass, doors, ventilation and WPC mechanism intact. Released knobs and their captive washers are screwed into separate parking sockets, with tether slack secured, before folding. No backbox electronics disconnection or front-module removal is introduced.

**Promoted to CURRENT V32 and the offline viewer. Manufacturing remains BLOCKED.** The passed CAD, motion, saved-file and viewer gates are recorded by `config/current_v32.json` and the generated `promotion.json`. This is not a hardware or CNC release.

HEAD BEFORE: `f3e2eee32fde61835376c53b462436b996f01794`. HEAD AFTER: the delivery commit containing this report. Branch: `feat/cabinet-review-v32`.

[23-view offline CAD gallery](../../exports/generated/backbox-lock-integration-v32/index.html) · [parameters](../../config/backbox_lock_integration_v32.json) · [validation](../../exports/generated/backbox-lock-integration-v32/validation.json) · [search map](../../exports/generated/backbox-lock-integration-v32/search.json). The previous [backbox service study](../backbox-service-v32/README.md) remains an immutable historical snapshot; its cassette-removal blocker is superseded by this integration.

## Selection and authority

The historical lock coordinates and R18 × 80 driver columns were provisional. Option A was evaluated first with the cassette installed: Ø40 knob, Ø44 wing-head rotation, Ø20 compact socket corridor, and axial release. The floor top is Z614.9 and the DMD underside Z636: only **21.1 mm**. The tested knob/wing envelopes or their release motion collide. Even a hypothetical 8 mm-high compact head, with the studied receiver, reaches the DMD during thread disengagement. This rejects the tested ordinary families, not every possible exotic low-profile mechanism. We did not cut the DMD envelope or create a cassette access window.

Option B searches the actual floor/shelf overlap, not arbitrary trial points. A 4 mm grid screens **1,536 centers on the left half**, mirrored about X300. It checks a complete R26 × 36 wood reserve in both boards, hinge reserves, head rotation/retraction, and a rear hand approach. The results distinguish wood exclusion, hardware/head exclusion and hand-access exclusion.

There are **17 clear sampled centers per side**. On the left, the clear samples are X126–142 at Y1256, and X126–146 at Y1260/1264; mirror these for the right. These are sampled centers, not an interpolated manufacturing-safe polygon. The selected X130/X470, Y1260 pair is independently checked using exact B-reps. It retains left/right symmetry and allows a wider palm envelope without clipping the speaker bodies. Options C/D are unnecessary.

| Item | Authority |
| --- | --- |
| WPC transverse axis Y1066.8/Z508; 210 mm lower sides; Y1146 floor | Previously validated design and owner instruction, unchanged |
| Complete twin-door/display/glass/cassette service architecture | Owner accepted in principle; exact prior B-reps retained apart from scoped lock machining |
| Lock positions, wood lands, hand corridors, parking blocks | Explicit design decisions; dimensions and clearances measured from generated B-reps |
| M8 × 40, Ø40 × 26 knob reserve; washers, receivers and tethers | Provisional packaging family; not a selected SKU or measured assembly |
| Hand fit, repeated-operation torque, wood strength, thread/washer retention | Physical qualification required; CAD is not structural or ergonomic certification |

A stock loss-protected star-knob family is documented by [Ganter GN 6336.13](https://www.ganternorm.com/en/products/2.2-Tensioning-clamping-withknobs/Star-knobs/GN-6336.13-Star-Knobs-Plastic-Threaded-Stud-Stainless-Steel-with-Loss-Protection), including the 40/M8/40 combination and retaining-ring variants. This establishes a purchased-hardware architecture; it is not a supplier selection or Brazilian availability claim. No vendor CAD, drawings or proprietary content were imported. Local equivalents, the washer-retention stack and tether termination must be measured before drilling is frozen.

## Operation and positive retention

Both locks are **HAND OPERATED**, through both open rear doors. Each uses a provisional M8 × 40 male hand knob, captive load-spreading washer, rotating loss-protection ring and 200 mm mechanical retaining tether. The washer must be captive on the shank using ordinary retaining hardware; a loose washer is not an accepted implementation. The tether is a mechanical loss-prevention component, unrelated to electrical cabling, and does not carry clamp load.

The moving floor clamps onto a metal-backed captive thread in the main rear shelf. Nominal receiver packaging is a 12 mm-long M8 barrel and Ø32 underside backing. Nominal engaged stud tip is Z577.9, providing engagement across the Z578.9–590.9 receiver barrel. The receiver requires positive anti-rotation and retention when the knob is released; it must not rely on repeated threading into plywood. Exact T-nut/flanged receiver, retention features, stud length, torque and washer stack are BOM/physical gates.

Released bolts must not dangle into the floor/shelf joint. Each therefore has a **positive threaded parking socket** at X185/X415, Y1268. Its support consists of two identical 50 × 32 × 18 plywood pads, bonded and retained with two flush/countersunk screws. The parking insert is metal. These small blocks support only a released knob, never the upright backbox load. Each parking bore has a 3 mm blind continuation into the floor, leaving 15 mm stock beneath; it does not open into the cabinet. The main lock and parking positions should be clearly marked `LOCK` and `PARK` in the final CNC/assembly package.

The validated hand sequence is: enter from behind above the rear sill; lower to the knob; unscrew and lift 80 mm; translate 55 mm inward and 8 mm rearward; lower into and tighten the parking socket. The stud clears the top of the parking block by 7 mm during transfer. Reverse the path to engage. The hand screen includes a 90 × 50 × 45 palm volume and two 14 × 20 × 40 bent-finger corridors; it is not a test with a thin driver rod. Full circular head reserves cover rotation, with hand re-grips. Minimum modeled hand-route clearance is **4.0 mm**, to the rear DMD adapter. Actual hands, gloves, cable dressing, chosen knob lobes and required torque need a physical service trial.

The short tethers use constant-length, hand-guided sampled routes through release, transfer and parking. In both closed operating states, surplus is wrapped and positively secured around each knob with a reusable cord keeper. A conservative R22/r3 toroidal storage envelope and a short anchored lead replace the temporary free arch. No unsupported upward cable arch is assumed during folding. Their fixed eyes are on the front faces of the parking blocks, 9 mm below their top edge; their rotating knob attachments face forward of the knob reserve. The parked tethers stay ahead of the low intake baffles. Clamp/tab geometry, bend behavior and positive washer captivity still require the purchased parts. The CAD sweep proves available space, not tether fatigue or fastening strength.

Normal fold workflow:

1. Open active right rear leaf, retract passive bolts and open the left leaf.
2. Release both upright locks; keep their knobs/washer assemblies captive and thread them into their parking sockets and secure the tether slack in its keeper.
3. Close and latch the rear leaves in passive/active order.
4. Remove main playfield glass and matrix according to the existing rules.
5. Fold with the lower cassette, DMD, speakers, backglass display and backbox front glass installed and secured.

Reverse: raise onto the shelf; open the rear leaves; return both knobs from PARK to LOCK, positively seat both washers and tighten; verify both clamps engaged; close/latch rear doors. The locking solution introduces **no DMD/speaker/fan/display unplugging step**. The existing removable matrix procedure remains separate and unchanged.

## Wood, bearing and reserves

The primary vertical load path remains backbox structure → floor → broad rear-shelf bearing. The two locks resist separation, overturning and vibration; they do not replace the shelf bearing. The 340 mm transverse separation is retained.

| Geometric result | Value |
| --- | ---: |
| Continuous wood-land radius, each board/lock | 26 mm |
| Gross reserve area per board/lock | 2,123.717 mm² |
| Floor thickness / shelf thickness | 18 / 18 mm nominal |
| Provisional floor / shelf through-bore | Ø9 / Ø12 mm |
| Shelf rear edge to lock center | 30.1 mm |
| Shelf rear edge to Ø32 backing envelope | 14.1 mm |
| Shelf rear edge to Ø12 bore | 24.1 mm |
| R26 wood land to generic passage | 15.761 mm minimum |
| R26 wood land to hinge hardware/tool reserve | 104.0 mm minimum |
| Bearing before lock reference bores | 65,672.400 mm² |
| Bearing after lock reference bores | 65,446.205 mm² |
| Net bearing retained | 99.6556% |

**Bearing area numerically unchanged: NO.** The two necessary reference Ø12 shelf bores remove 226.195 mm² from the actual contact area. The broad bearing profile, front/rear/side regions, passage and shelf extents are unchanged. This small, explicit bore-area reduction is not a shelf cutback or an attempt to force a fold pass. No strength certification is inferred from area. The hole/receiver dimensions remain provisional and must be regenerated after hardware measurement.

The parking pads remain wholly outside the service opening, with 4 mm longitudinal separation from its rear edge. The floor/side joints and all hinge reserves are preserved. No side-wall WPC opening is enlarged and no final WPC holes are released. Planning mass remains in approximately the 35 kg class before optional toys; actual hardware, toy payload, plywood and handling loads still require qualification.

## Routine locks versus rare hinge service

The installed cassette still obstructs the first floor-hinge service column on each side. **Rare WPC hinge maintenance may require cassette removal.** Cabinet-side pivot service retains the existing playfield lift-out/removal prerequisite. Neither requirement is used for routine locking/unlocking. The old R18 × 80 upright-lock columns are historical and are not active operational constraints at the old centers.

## Validation and promotion gates

- Exact B-rep option A tests, floor-area map, selected wood reserves and hand/knob/washer approach, lift, transfer and parking sweeps, including the reverse paths.
- Constant-length mechanical tether samples through every operation stage; parked and engaged tethers included in occupied service states.
- Continuous 0–100° door certificates against new lock parts in both engaged and parked states; original door/frame/fan/cable certificates retained by source hashes, with additional samples. Low-voltage fan loops remain far above the lock system.
- Display/front extraction, rear adjustment, glass lift, cassette and fan service remain clear. Their original exact geometry is unchanged; new-part separation and swept-volume checks close the integration.
- All required fold samples from 0° to 90°, including fine initial angles, with locks parked, doors latched and complete front modules retained. Continuous certificates cover new lock material versus the actual cabinet, existing populated backbox versus the new shelf hardware, and optional blank modules.
- Playfield service 0–50° and 48 mm lift-out checked against the new parts. Accepted dowel/cradle/strap geometry and all six support screws remain unchanged.
- Independent saved-CAD regression checks current poses, rigid populated fold, unchanged accepted service parts and historical artifacts. Native states and viewer meshes agree.
- Viewer uses the existing controls, English default, PT-BR, original/accessible palettes and offline implementation. Only geometry, new-part material classification and fold/lock status text are updated. Larger interior/exploded UI work remains deferred.

There are intended thread engagements, bearing contacts and fastener-to-wood interfaces. Raw mesh intersection of a screw's thread envelope with its captive receiver is not a collision failure. Conversely, no DMD, speaker or hand conflict is waived. This package models packaging reserves, not detailed purchased threads or an ergonomic certification.

| Requested decision | Result |
| --- | --- |
| Selected option | B |
| Lock L / R centers | (130,1260) / (470,1260), mm |
| Operation | HAND; loss-protected M8 × 40 knob family, provisional |
| Cassette removal for normal fold | NO |
| Added electronics disconnection | NO |
| Rear-door lock access | PASS |
| Cassette geometry / DMD / speaker envelopes | Unchanged / preserved / preserved |
| Cassette removal for rare WPC hinge maintenance | YES, may be required |
| Doors / display adjustment / glass / fans / lock operation | PASS in modeled service states |
| Populated 0–90° fold | PASS; lower cassette and backbox glass retained |
| Custom metal | 0 |
| Complete backbox promotion | YES; passing `promotion.json` and CURRENT manifest |
| Manufacturing | BLOCKED |

## Reproduce and inspect

```sh
freecadcmd tools/backbox_lock_search_v32.py
freecadcmd tools/backbox_lock_integration_v32_entry.py
freecadcmd tools/check_backbox_lock_integration_v32.py
freecadcmd tools/backbox_lock_details_v32.py
uv run --with matplotlib --with numpy python studies/backbox-lock-integration-v32/render.py
python3 tools/build_review_viewer.py --mesh exports/generated/backbox-lock-integration-v32/mesh.json
python3 tools/check_backbox_lock_viewer_v32.py
python3 tools/promote_backbox_lock_v32.py
python3 tools/package_backbox_lock_v32.py
python3 tools/check_current_v32.py
```

Require explicit PASS sentinels and passing JSON; FreeCAD may return exit zero after a Python exception. Review images are actual CAD tessellations/sections, with native FCStd links. Diagnostic Option A remains labeled rejected. Exploded geometry communicates component groups, not a simultaneous disassembly path. Historical source CAD is not overwritten.

Physical freeze still requires 01-9011-L/R, 02-4352 and 4322-01139-12B measurements; actual knob/receiver/captive washer/tether/parking insert and operating torque; plywood and mounting screws; matrix confirmation; door/cam/bolt/hinge and gasket details; glass supplier and display/DMD/speaker adapters; structural load/joint and human-access trials; cable dressing and thermal/filter trials; CNC supplier profile, cutter/tool data, nesting, dogbones/clearances, tolerance coupon and owner manufacturing approval. Generic service passage parameters remain separate and builder configurable.

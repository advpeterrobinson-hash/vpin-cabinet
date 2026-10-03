# V33.8 — optional hardpoints, routing and dry-fit audit

**Study only; no CURRENT wood or permanent hole is changed.** The minimum cabinet does not depend on these accessories. Primary support for the raised 50° playfield is not defined/qualified: all service-pose checks below are geometry screens, not instructions to work under an unsupported display.

## Decision

Keep S1/S2/S3 and T1/T2/T3 exactly. Add **zero permanent hardpoint stations**. Retain one optional ACC01 family,100 × 120 × 12 mm, R4 exterior corners and the existing 6 × 22 R3 strain-relief-pair grammar. Two sample positions fit: S2 right (X430–530,Y595–715,Z192–204) with rear-edge clamps; S3 left (X60–160,Y865–985,Z252–264) with front-edge clamps. Finished board mass at 650 kg/m³ is 0.091554 kg each. Optional boards and clamps stay outside minimum BOM, sheet nesting, mass and packing.

Each board bears vertically on its shelf. Two removable screw C-clamps provide provisional retention; they are not custom metal or an assumed selected product. Clamp jaw stack is 24 mm nominal. The occupied clamp body, screw and handle geometry is an original packaging envelope. Purchased jaw/throat/body/handle dimensions, anti-loosening behavior and load suitability must pass before use. Impact/contactors/chimes are not qualified merely because a small controller board fits. No spring clamp or adhesive-only tie base is claimed as a structural retainer.

The initial 120 mm-wide S2 sample intersected shelf washers/tool corridors. Front-edge S2 clamps blocked S1 extraction. Those candidates were rejected. The selected 100 mm-wide family and rear-edge S2 clamps pass the actual geometry screen. No permanent shelf, side or crossmember was relieved to force a fit.

## Geometry evidence

20 checks pass against `exports/generated/service-productization-v 338/play.FCStd` at SHA256 `c 78a 64794d 4ac 009e 12986aa 5adc 03f 936b 5bbf 95b 84d 0a 4da 35e 2742f 7c 4c 53`.

| Screen | Result |
|---|---|
| Optional boards/clamps/payloads vs current occupied volumes | PASS; nearest nonbearing gap 6 mm to shelf washer |
| Playfield 0–50° vs optional boards | PASS, conservative continuous arc bound |
| Playfield 48 mm lift | PASS sampled endpoints/intermediates |
| Board 100 mm upward removal after clamps released | PASS at geometric 50° service pose |
| All 12 shelf screw access columns | PASS |
| Existing three shelf routes vs other optional samples | PASS |
| Main/backbox permanent holes added |0 |

Release the optional board/clamps before removing its shelf. Detach the S3 fixed playfield-loop clamp before shelf extraction; support the free harness. This is an accessory service prerequisite, not a routine 50° electronics disconnect. Future payload wiring and shelf branch disconnects remain user-configurable.

## Cable-management grammar

| Term | Current mechanical meaning |
|---|---|
| CABLE_PASSAGE | Existing generic 260 × 60 backbox interface; no connector/count/disconnect specification |
| STRAIN_RELIEF_PAIR | Preferred 6 × 22 R3 pair,34 mm center pitch;6 × 16 R3 backbox and 4 × 12 R2 underfront remain protected compact exceptions |
| SERVICE_LOOP_ANCHOR | Removable mechanically retained clamp; cable loads bypass connector shells |
| POWER_ROUTE | Right low 20 mm diameter ELV planning zone atX510/Z100,Y300–1100 |
| SIGNAL_ROUTE | Left low 20 mm diameter planning zone atX90/Z100,Y300–1100 |
| MOVING_HARNESS_ROUTE | Existing PF loop, plus separately held backbox-harness planning |

Both low routing zones clear occupied CURRENT solids by 24.677 mm. Their centerlines are 420 mm apart. These are mechanical planning zones, not populated cables, continuous raceways or electrical certification. Mains stays in a separate enclosed/protected route. Do not route general signal bundles through a mains compartment. Final branches, supports, crossing points and bend radii require actual cables; no wire gauge, connector family, mains plug or proprietary gland is selected.

## Playfield moving harness

Preserved 400 mm reference loop,8 mm diameter packaging tube, moving anchor local(300,877,−20), fixed S3 clamp point(450,900,258). All 63 configurations pass: PLAY,1° increments through 50°, and 4 mm lift increments through 48 mm. Minimum sampled reference curvature radius is 39.270 mm, above the existing 35 mm planning threshold. This is a flexible parabolic route packaging screen, not continuous flexible-cable certification or a universal display-port location guarantee.

The rear M025 service window, original VESA load area and strain slots are unchanged. Routine geometric 50° motion needs no cable disconnect with this reference loop. Purchased cable construction, real connector access, strain-relief retention and the missing qualified primary raised support remain holds.

## Backbox harness and adjustment

Existing carrier strain slots, generic passage, rear adjustment and front display removal remain. ±5 mm vertical, two depth positions 16 mm apart, display-width-dependent lateral centering and replaceable VESA plate are sufficient; no new monitor mechanism is introduced. The central VESA service-window proposal remains uncut and HOLD.

**Backbox moving-harness route: HOLD, not PASS.** A400 mm generic parabolic fold-loop search did not establish a viable continuous path: some tested states intersect BACKBOX_BASE/BB_Floor and several have unacceptable local curvature. A collision-free isolated sample with a sharp/cusped curve is not a valid cable route. The failed trajectories are retained as diagnostic evidence only. Fixed removable-anchor and moving-anchor zones are shown without presenting them as final selected harness hardware. Do not require normal electrical disconnection as a workaround; qualify a real supported loop with the selected cable later.

## Dry-fit and part identification

The main shell uses positive 4 mm captures; install floor/front/rear/rear bearing shelf before closing SideR, dry-fit, seat shoulders, square-check, then use qualified adhesive/fixation. M067 retains its capture shoulders. The underfront plate retains its 2 mm registering recess. All 108 V33.7 source manufacturing members carry canonical IDs, FACE A direction, opposite-face policy and local datums in the audited register. SW01 uses shop datums rather than being relabeled CNC plywood. V33.8 SW02 identity is assigned by the separate manufacturing task.

| Permanent interface | Current evidence / hold |
|---|---|
| Six fixed shelf supports |12 modeled attachment axes match cabinet-side pilots; tiny pilot completion/hardware remains qualified manual finish |
| Two dowel cradles |Six side-retention axes match side locators; floor foot is positive vertical bearing |
| Six T guides |Four wall-anchor holes per guide plus six bracket-height positions; no corresponding side-wall pilot pairs in CURRENT. Placement/template qualification remains unresolved |
| Four backbox monitor rail cleats |No locating-hole pair/capture in current cleat B-reps; qualify rear/frame/height setup template |
| Two backbox rear hinge cleats |No released purchased-hinge locating schedule; preserve axis, qualify drilling/template before CNC |
| Captured shell reinforcement F06 |Family/count remain unresolved; no assertion all kit screws are known |
| SW01 |Existing diagonal/top-stop jig; purchased leg/plate/bolt pitch and drill qualification remain held |

These are productization holds, not permission to alter architecture or ask a builder to invent critical locations with a tape measure. Manual/CAD IDs are available; final 1:1 placement guides and purchased-hardware pilot instructions must be qualified before kit release. Optional accessory placement is intentionally builder-configurable and is not a missing structural datum.

## Premium flatpack principles — learn, not clone

The [Tukkari product page](https://www.tukkari.eu/p/widebody-virtual-pinball-cabinet-vpin-flat-pack-kit) was reviewed on 2026-10-03 for dry-fit-first assembly, accessible monitor holders, internal modularity, safety awareness and illustrated instructions. CURRENT provides comparable functional principles through captured shell shoulders, removable narrow shelves, front display installation/rear adjustment, twin rear doors, replaceable adapters, the generic user panel and distributed packing. This is a qualitative design review, not a measured product comparison.

Not adopted: proprietary edge connectors,5-axis dependencies, large dense internal mounting panels, their hardware patterns, copied CAD or unnecessary metal modules. Our nominal plywood stays exactly 12/18 mm; the vendor’s other stock choices are not project authority.

Brazilian commodity availability is supported by the [Vonder 50 mm C-clamp listing](https://www.vonder.com.br/produto/grampo_sargento_tipo_c_2_vonder/9120). Only the published 50 mm maximum opening is documented here. No SKU is selected and no unlisted throat/body dimension is promoted to manufacturing authority.

## Release

No new permanent machining or minimum hardware is released. Actual stock, coupon, selected accessories/cables, structural/ergonomic qualification and the primary raised-playfield support remain pending. Full-sheet CNC remains blocked.

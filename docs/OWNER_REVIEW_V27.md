# Owner review v27 — manual props and a complete service layout

Owner decisions after `a0ac747`, on published branch `feat/active-build-cleanup-v25`. Engineering packaging only; manufacturing-ready remains false. `config/owner_services_v27.json` records the new dimensions as explicit project decisions. They are not dimensions inferred from unmeasured products.

## Manual playfield lift and two simple props

No gas-assist geometry, bracket, doubler, purchase requirement, force solve or wood-hole dependency remains in the active baseline. HF-011 is retired, not reused. Historical v04/v05 experiments and dated audits are not active procurement or release authority. A future assist accessory would require its own adapter-based review and cannot silently add baseline wood holes.

The baseline has two straight captive rods, one each side. Each has a captive lower pivot, an upper receiver with a transverse captive locking pin and positive keeper, and a rearward stow U-clip closed by a captive transverse keeper. No friction support, gas spring or elaborate folding linkage is used. Both props must be positively pinned before anyone works beneath the playfield; each support and its anchors must independently pass the complete moving-load case.

Current rod candidate: **8 mm steel, approximately 896.8 mm pin-to-pin**, in planes X28 and X572. Fixed pivot Y80 Z330; receiver follows the existing cradle service datum. The candidate diameter is **not a certified load rating**. End eyes, pin dimensions, keeper retention, clevises, mounting patterns, rod buckling/end strength and installation tolerances require physical HF-010 hardware and proof testing.

The old mid-body stay position produced a real deployment collision: endpoint checks passed, but the rod crossed the raised cradle during rotation out of stow. The accepted preview moves the fixed anchors forward and the rods into the outer-rail corridors. Sampled deployment now clears the raised structure. Stowed ends are near Y976.8 at Z330; the rear SSF reserves are lower, at Z200..280, so neither rods nor clips occupy them. The outboard corridor is narrow: validate coatings, pivot play and actual rod/receiver tolerances physically before release.

Each new front prop reinforcement overlaps the existing landing/latch reinforcement. These are now **one shaped 18 mm reinforcement per side**, preserving all three reaction zones. A local steel riser reaches above the wood to the lower pivot; there is no separate safety doubler and no bulky leg furniture. This combination removes two further wood assembly records in addition to the two removed assist doublers.

At the 12 kg display + 4.5 kg preliminary cradle allowance, uniform-component CG assumptions and front grip datum give about **86.1 N peak vertical hand force (8.77 kgf)**, reducing to about 75.7 N at the service position. This excludes friction, handling margin and unusual mass distribution. Measure the completed assembly with a force gauge at the intended grip through the opening range; verify reach, keeper operation and controlled lowering. Use temporary independent support during prototype tests. Final manual handling and single-prop proof remain release gates, not CG-dependent permanent strut-hole geometry.

## Small removable electronics carriers

Two **125 × 355 × 6 mm** replaceable carrier plates occupy X50..175 and X425..550, Y285..640, bottom Z125. Each has a **3 kg** planning payload envelope extending 110 mm above the plate. The first two low crossmembers support them via four small project-fabricated end angles; standardized M6 through-bolt centers are CNC-located in the wood. Exact PSU/amplifier/controller patterns go only on replaceable plates. Use captive nuts/bolts for service; no glue and no drilling electronics patterns into permanent wood.

Left is a DC distribution/control installation envelope; right is an amplifier/controller envelope. These are intended allocation zones, not selected components. Mains equipment remains in its existing independent touch-safe rear enclosure. Low-voltage cable routes require final segregation, strain relief and electrical design.

The central access box X190..410, Y300..810, Z116..276 remains clear. No bridge is added. This leaves access and future shaker/contactors/toy choices available. All three low crossmembers are retained: 1 and 2 locate/stiffen the shell and support the removable carriers; 3 retains the rear shell/CPU rail saddle load path. Bottom, low tie, rear shelf, CPU rail and carrier are different parts with different functions.

## Bottom intake and fixed exhaust

The bottom has **18 rounded slots, each 80 × 12 mm**, in two banks centered at X250/X350. Row centers are Y330..570 in 30 mm steps. Rounded ends have R6. Nominal webs: **18 mm between rows and 20 mm between banks**. Clear distance to the first crossmember is 46 mm and to the second is 74 mm; side/corner and CPU backing zones remain intact. Total slot area is approximately **16,724 mm² (167.2 cm²)**, about 2.26% of the nominal bottom area. This is geometric open area, not airflow capacity.

A **220 × 290 mm** externally removable underside filter cassette surrounds the banks. Its generic M4 clearance grid is project-designed; future media/fan patterns belong to the cassette/adapter. Captive interior fasteners allow outside filter service. The filter does not require opening the playfield or entering the mains enclosure.

Two rounded **100 × 40 mm** matched passages through the rear shelf/backbox floor, centered X220/X380, Y1188, reserve airflow and protected low-voltage cable transit. Keep cables edge-protected and segregated within removable passage inserts. Verify flex/disconnection during backbox folding and actual lock hardware clearance before release.

Two generic **100 × 80 mm**, R10 exhaust openings are in the fixed upper rear frame, behind replaceable 130 × 110 mm plates. Later fans/guards/filter patterns stay on those plates. Fans and their wiring do not ride on the moving service door. The airflow review is bottom intake → main cabinet → matched upper passages → backbox → fixed upper exhaust. No thermal-performance claim is made; heat loads, airflow balance and filtering need commissioning tests.

## SSF and conventional audio are separate

Four **solid-wall** exciter reserves remain visible: front L/R at Y350..450 Z200..300; rear L/R at Y850..1000 Z200..280; 25 mm depth from the inside sidewall. Exciters couple vibration into plywood; there are no large holes behind them. Exact devices and local attachment adapters are HF-031, buy later. A bonded or otherwise engineered local adapter must preserve full panel skin; any proposed new wood penetration needs its own release review.

There is **no bottom subwoofer opening or reserved cutout**. A later conventional subwoofer would need a separately reviewed reinforced removable baffle/enclosure. Backbox conventional speakers are two replaceable **120 × 120 × 75 mm** module envelopes on serviceable baffles/rail-cage adapters; HF-033 is adapter-only. They are not SSF exciters.

## Controls are visible but not drilled

| Interface | Project packaging center/envelope |
|---|---|
| Left/right primary flipper | Y255 Z270; axis normal to side |
| Left/right optional action | Y310 Z270; omit/blank if not wanted |
| START | X125 Z250, front |
| EXIT/BACK | X125 Z200, front |
| Separate LAUNCH | X470 Z230, front |
| Plunger | X520 Z215, front-right; body X500..540 Y18..220 Z195..235 |
| Coin door | X175..425 Z90..300; uncut packaging reserve |
| Hidden service/feedback-disable | Inside coin-door access envelope |

Side nut/switch reserves are radius 18 mm and 60 mm deep, followed by 20 mm cable reserves. Front buttons reserve 65 mm body depth plus cable space. These envelopes clear current cradle, reinforcement, leg brackets and SSF zones. The side center positions prioritize the deep independent cradle's clearance; confirm ergonomics with a full-size hand mockup before machining.

There are **no released button, coin-door or plunger bores**. HF-020 determines actual button diameter/flats/thread/nut/switch depth; HF-019 controls coin-door cutout and flange. **HF-030 plunger is the only new BUY NOW item.** Measure flange/shaft/cutout/pattern, nut stack, stroke, handle projection, sensor body and cable sweep from the front seating plane and shaft centerline. The drawing's crosses are ergonomic datums, not drill centers authorized for CNC.

## Backbox door and access

**BB-DOOR-001-R1 remains 520 × 460 × 15 mm**. A fixed stop flange and compressed gasket space it 4 mm behind the original rear plane. The preview has a continuous-hinge envelope, keyed/tool-controlled latch and an actual **105° outward open state**. Actual HF-029 hinge/lock/gasket dimensions still control final mounting and stack. The fixed frame, floor, sides and top carry backbox shear; the door is not credited as the shear panel.

The large rear opening allows access to central display mounts, connectors, DMD, speaker modules, lighting and wiring. The flange leaves an approximately 500 × 440 clear stop opening. **A 740 mm display cannot pass flat through this door**: full monitor replacement uses the front opening after removing its replaceable bezel. Do not claim rear straight-through removal. Upper fan/filter adapters are serviced from the fixed rear frame, independently of door wiring. Final connector/tool and full-display-removal mockups remain necessary with actual electronics.

## Counts and CNC registers

| Category | Before owner pass | Current |
|---|---:|---:|
| Permanent structural wood assembly records | 33 | **29** |
| Removable wood doors | 2 | **2** |
| Replaceable CPU shelf board | 1 | **1** |
| Total active wood assembly records | 36 | **32** |
| Removable carrier plates/boards, counted separately | 4 existing | **11 total** |
| Defined wood CNC feature groups | 137 | **173** |
| Hardware-blocked wood feature groups | 60 | **59** |
| Previously design-blocked ventilation/passport groups | 4 | **0** |

The 11 carriers comprise two electronics plates, one filter cassette, two exhaust adapters, two speaker baffles, and four existing carriers (CPU board, VESA, mains and Ethernet). This is seven new replaceable pieces, **not eleven new permanent wood parts**. Count the CPU board only once when producing a combined materials list. Three nominal 2t pivot assemblies still require separate ply IDs at nesting.

Four assist-related hardware feature groups were removed. Two previously implicit sidewall prop-anchor groups were made explicit and one front plunger group added, producing the net 60 → 59 hardware-blocked count. The defined count includes profiles, cut groups and engraving instructions, not finished toolpaths. `bom/BLOCKED_CNC_FEATURES_V25.csv` is the explicit blocked subset. Adapter-specific operations are kept separate from the permanent-wood register.

## Review and release

Run `make cnc-detail`. Open `exports/generated/review/index.html` for the 16 requested views plus the five-face penetration map. Native FreeCAD presets use the same visible-object lists; the exploded layout and planar maps are PNG review outputs.

Remaining gates: measured plywood and tooling/coupon; actual leg/bearing/hinge/prop/door/button/plunger/slide/coin-door interfaces; side/rail clearance with actual fastener stacks; local metal drawings; final pilots/relief/nesting and laminate IDs; assembly/access/fold checks; individual prop and CPU proof tests; manual lift-force/ergonomic test; thermal/electrical commissioning and owner manufacturing approval. No physical test is implied by a geometric PASS.

### Exact review outputs

- [01-full-exterior.png](../exports/generated/review/01-full-exterior.png) — Full exterior / playable interfaces
- [02-left-control-side.png](../exports/generated/review/02-left-control-side.png) — LEFT side / flipper and optional action
- [03-right-control-plunger.png](../exports/generated/review/03-right-control-plunger.png) — RIGHT side / flippers and right-front plunger
- [04-front-panel.png](../exports/generated/review/04-front-panel.png) — FRONT / coin door, start, exit, launch, plunger
- [05-bottom-penetration-map.png](../exports/generated/review/05-bottom-penetration-map.png) — BOTTOM / actual slots and reserved hardware
- [06-interior-service.png](../exports/generated/review/06-interior-service.png) — Interior / playfield removed for inspection
- [07-electronics-carriers.png](../exports/generated/review/07-electronics-carriers.png) — Two removable low-voltage electronics carriers
- [08-ssf-exciter-zones.png](../exports/generated/review/08-ssf-exciter-zones.png) — Four SSF zones / solid plywood beneath exciters
- [09-airflow-path.png](../exports/generated/review/09-airflow-path.png) — Bottom intake → main cabinet → passages → backbox exhaust
- [10-playfield-raised-props.png](../exports/generated/review/10-playfield-raised-props.png) — Playfield raised / BOTH captive prop rods pinned
- [11-props-stowed.png](../exports/generated/review/11-props-stowed.png) — Both props stowed / captive positive clips
- [12-backbox-door-closed.png](../exports/generated/review/12-backbox-door-closed.png) — BB-DOOR-001-R1 / CLOSED, gasketed and keyed
- [13-backbox-door-open.png](../exports/generated/review/13-backbox-door-open.png) — BB-DOOR-001-R1 / OPEN OUTWARD 105°
- [14-backbox-service-access.png](../exports/generated/review/14-backbox-service-access.png) — Backbox / displays, DMD, speakers and wiring access
- [15-cpu-extended.png](../exports/generated/review/15-cpu-extended.png) — CPU extended / carriers do not obstruct rear service
- [16-structural-exploded.png](../exports/generated/review/16-structural-exploded.png) — Exploded structural wood / separate removable carriers
- [17-five-face-feature-map.png](../exports/generated/review/17-five-face-feature-map.png) — all five panel faces.

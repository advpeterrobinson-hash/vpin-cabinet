# Hardware measurement pack — v25

Engineering review, 2026-09-24. **Manufacturing ready: false.** No drill pattern in this pack is authorized for machining. Purchase specifications below are project requirements, not verified product availability or vendor recommendations.

The authoritative item-by-item worksheet is [MEASURE_BEFORE_CNC_V25.csv](../bom/MEASURE_BEFORE_CNC_V25.csv). It records the controlled feature, minimum specification, exact measurements, datums, tools, measurement uncertainty, photographs and target config for every HF item. Printable HTML worksheets are in [measurement-templates](measurement-templates/HF-013.html); print at any scale because they are recording forms, **not transfer/drill templates**. The CAD review lives at `exports/generated/cnc-detail/vpin-cnc-detail-preview.FCStd`; rebuild with `make cnc-detail`.

## BUY NOW — required to freeze permanent CNC interfaces

Buy matched assemblies rather than unverified loose substitutes. Shared purchases are deliberately grouped:

1. **HF-001:** production main plywood sample/batch, plus the actual door stock if different. Measure nine points per sheet and record min/max, not only average. Main design nominal is 18 mm; doors nominal 15 mm.
2. **HF-003/004:** four classic legs, levelers, matching bolts and four compact internal brackets/backing. Measure the installed corner stack, not just the bare bracket.
3. **HF-013/026:** one matched 450 mm full-extension slide pair (at least 30 kg pair rating in the intended orientation), four identical rail angle clamps with backing plates/bolts, and one positive stowed retainer.
4. **HF-015/016/029:** CPU and backbox service-door hinge/lock/latch/gasket sets. Reuse a common family if both interfaces fit; measure both installations.
5. **HF-006/007:** WPC-style hinge pair with matching pivot bolts/bushings and two upright locking bolts/captive receivers.
6. **HF-008:** matched UCFL202 pair with actual 15 mm bores.
7. **HF-010/012:** two simple captive prop rods, two closed-position latches and landing pads. Each stay must be assessed to support the complete moving load independently; pins/keepers must retain them without friction.
8. **HF-019:** coin door whose physical cutout and flange determine front-panel machining.
9. **HF-020:** one mechanical sample of each final flipper/start/launch button family. No controller/electronics purchase needed.
10. **HF-030:** selected mechanical/electronic plunger sample. The visible envelope is not a bore pattern.
11. **HF-017/027:** one selected enclosed mains-entry/disconnect assembly (including enclosure and strain relief) as a mechanical fit sample. The current carrier alone does not decouple enclosure mounts from permanent wood.

HF-028 is the combined rail/leg measurement task using items 2 and 3, **not another purchase**. Already-owned open case HF-014 needs measurement, not replacement.

## BUY LATER — no purchase needed for the current detailing pass

External skates; displays; PC components; controllers; amplifiers; feedback devices; final glass. Generic carriers and ventilation openings are defined in the owner review; adapter patterns and commissioning follow without buying all electronics now.

HF-011 is retired: no assist hardware or CG-dependent mounting pattern blocks baseline CNC. Final completed-assembly manual lift effort remains a physical check. HF-002 is the immediate CNC-shop consultation/coupon task, not a hardware purchase. **HF-030 plunger is the only new BUY NOW addition**; measure its front cutout/flange/pattern, shaft and nut stack, stroke, internal body/sensor depth and cable sweep from the front seating face and shaft axis.

## LOCAL FAB — drawing/prototype needed

- HF-009: 15 mm journals, cheek plates and retention. Measure the bearings first; freeze bearing engagement, shoulders, axial retention and plate/wood stack before publishing metal DXF/PDF. Existing candidate plate holes are not release coordinates.
- HF-021/022: prototype a short siderail/glass channel section and the custom 600 mm lockdown/receiver **now**, before front/side fastening patterns freeze. Use a safe thickness gauge/mock glass panel, not final tempered glass. Verify capture, latch travel and service removal. Final full-length profiles and final glass follow the mockup.
- Leg spreaders and CPU backing plates may be locally cut after the purchased assemblies establish outline, bolt pattern and edge distances. No fabricated plate drawing is final until its mating hardware has been measured.

## ADAPTER ONLY

HF-014 already-owned case: direct holes in the one replaceable CPU shelf. HF-018 optional RJ45 or blank: replaceable 40 × 40 carrier over the existing 24 × 24 opening. HF-024 playfield and HF-025 backglass: replaceable display adapters. HF-031 exciters, HF-032 filter/fan details and HF-033 speaker modules are adapter-only / BUY LATER. Display mass and manual effort are physically checked after assembly; no baseline assist dependency remains.

## Owner measurement procedure

1. Label every part, handed side and batch. Use mm. Mark datums A/B/C on both the part photograph and sheet. Do not infer centers from a perspective photo.
2. Measure both members of each pair, all four leg/bracket stacks, and every different door installation. Record slots as length, width, end radius and orientation; record center coordinates from the same datums rather than chained spacing.
3. General recording targets: hole centers and stacks ±0.10 mm, outlines ±0.5 mm; sheet thickness ±0.05 mm; bearing/journal fit dimensions ±0.02 mm using suitable gauges. These are measurement uncertainty targets, **not automatically allowable CNC or shaft fits**. Report instrument resolution and repeatability; leave inaccessible dimensions unknown.
4. Capture orthogonal front/back/side views with a ruler in plane, hole/slot details, actual assembled bolt stacks, labels and maker specifications. Include both fully closed and fully extended slide members, both hinge positions and stay lock engagement.
5. Return the completed CSV plus photos under item IDs. HF-010 now covers simple rod end eyes, lower clevis, upper receiver pins/keepers and stow clips; do not buy friction lid stays or folding linkages. Measurements enter a future `measured_patterns` object only after cross-checking; no such coordinate payload is currently populated. Existing source target fields are listed separately in the CSV.
6. Regenerate the entire assembly from coordinated measured stock, apply the CNC shop's accepted clearance/tool relief, then check edge distances, accessibility, sweeps and the physical coupon. The home builder must not transfer-drill unresolved structural patterns.

## CPU rail fixture and 20 kg proof case

Use [HF-013](measurement-templates/HF-013.html), [HF-026](measurement-templates/HF-026.html), [HF-028](measurement-templates/HF-028.html), and the generated `cpu-measurement.svg`. Cabinet coordinates: X left-to-right; Y front-to-rear; Z up. Reference X0 outside left, Y1308.1 rear exterior, Z0 cabinet bottom. In a corner sample also record the measured inner wall planes, bottom top and bracket attachment plane.

Required values: rear bracket innermost X including flange and bolt/nut/washer; bracket Y/Z extents; flange thickness; slide body thickness and fixed/moving member patterns; manufacturer min/max side clearance; clamp legs/bend/thickness; backing thickness/area; all fastener projections and wrench access. Measure left and right independently. Current closest modeled gap is 13.8 mm, versus a 15 mm **planning** reserve. Retain the architecture; do not move the shelf to improve one side at the expense of the other.

Wood independent of hardware: one 285 × 460 board; two bottom-seated rails with a crossmember saddle; existing Z135 shelf datum; 450 mm rearward travel; no second board or sled. Shelf thickness follows measured stock. Rail X separation, final rail width/height and saddle fit must be revalidated against actual slides/brackets. No slide, clamp, retainer or case mounting holes are supplied.

Fixture: reproduce measured bottom, third crossmember, both rails, all four clamps/underside plates, both slides and the actual shelf. Restrain fixture against sliding/overturning independently of the drawer, preserving the cabinet's actual support conditions. Keep an unloaded catch platform just below the board and people out of the fall zone. Use inert distributed weights positively secured to the shelf; no live PC or mains. The test is not permission to sit on the shelf.

Proposed acceptance protocol (engineering test plan, not a certified load rating): record zero readings; extend fully; apply 5, 10, 15, then 20 kg **payload in addition to shelf self-weight**, centered across X and the extended shelf footprint; dwell 10 minutes at each step. Record rear-tip deflection, rail rotation, clamp lift, fastener slip and bottom deformation. Unload and record permanent set. Stop immediately for cracking, sudden displacement, loosening or binding. Acceptance target: no damage/slip, no loss of retainer/disconnect function, no remaining set above 0.5 mm, and full-load deflection ≤3 mm while preserving actual hatch clearances. These are project prototype targets and require review with the real slide specification.

Repeat the 20 kg case with load center shifted ±50 mm in X to screen unequal slide sharing, and 50 mm rearward to screen a rear-heavy PC. Do not infer impact/nudge or fatigue capacity from the static test; record an additional operational cycling/load assessment before release. Each angle and backing plate must pass a bolt/bearing/crush calculation before proof loading.

At the existing 875/1150 mm support centers and Y1510 extended board center, the centered case predicts about 138 N front uplift and 244 N rear compression **per rail**, including nominal board mass. Use the generated `rear-utility-study.json` for recomputed values. The front fastener path needs positive through-bolt/backing restraint; glue or screws into rail end grain are insufficient.

## Leg corner design envelope

Keep the existing compact 95 × 95 × 150 mm corner reservation; nominal steel thickness 3 mm and 70 × 120 mm spreader faces are packaging targets, not proven capacities. Include flanges, bolts, nuts, washers, tool access and backing in the installed envelope. The rear corner must also respect actual rail and slide extents. A 95 mm flange is a maximum planning target, not an instruction to trim purchased brackets.

Load path: leg/leveler → leg bolts → compact bracket and broad backing contact → both full-thickness shell walls/end panel → captured bottom and end joints. Bolts must pass through sound wood and metal support; no load relies on reduced OLED clearance skin. No bulky corner furniture or wheel cutouts are added. If the real bracket cannot satisfy strength and clearances together, record a measured contradiction and review a local plate/angle solution.

Project screening rule for wood hole centers: ≥7 bolt diameters from a loaded end and ≥4 diameters from other free edges/cutouts, subject to actual plywood/fastener engineering. Check remaining ligament from hole edge as well as center spacing; include nearby grooves, corner cuts and countersinks. This conservative screen is not a substitute for load capacity. Exact holes remain blank; Williams historical spacing is not a release datum.

## Backbox and playfield envelopes

Backbox: retain 780 mm outer width and the 740 × 450 × 100 replacement-display envelope. The joint preview preserves shell outside bounds and removes overlapping perimeter blanks via rebates. Rear shelf is captured t/3 in the sides and rear. Floor/shelf contact supports gravity; measured hinges and independent upright locks provide pivot/retention. WPC keepouts are 110 Y × 170 Z × 5 X per side in the current baseline; actual leaves/bushings may exceed them and must be checked. Pivot ghost diameter and lock X markers are references, not holes. Measure all leaf patterns, pivot offsets, bushing/bolt stack and upright lock X/Y/engagement in an assembled mockup.

Playfield: retain 560 × 970 × 55 display envelope, independent cradle, short 15 mm journals, dual stays and closed landing/latch interfaces. UCFL housing reserves are 35 X × 120 Y × 75 Z; existing backing reserves are 3 × 120 × 70. Cheek plate reserve 6 × 140 × 80 and nominal 36 mm pivot wood are not permission to use candidate holes. Measure bearing axis offset and journal engagement/retention; record stay anchor offsets, locked/stowed lengths and release sweep; record pads under compression and latch grip. Props are straight captive rods with upper pins/keepers; see OWNER_REVIEW_V27.md. No assist mount pattern is in the baseline. No load is assigned to reduced side skin.

## Finite release queue beyond measurement

The four former ventilation/passport design blockers now have generic rounded geometry and replaceable adapters in v27. The latest dimensions, carrier load paths, prop deployment correction and remaining physical checks are recorded in [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md).

The detail model is a zero-clearance joint preview. Remaining process work is coordinated measured-stock regeneration, tool relief and mating corner strategy, supplemental fastener/CNC pilot design, laminated-ply breakout, two-face setups and nesting, dimensioned shop PDFs/DXF, coupon, dry fit, proof tests and owner manufacturing approval. It is deliberately **not** a finished CNC package.

## Next physical-validation cycle

Follow [PHYSICAL_VALIDATION_PLAN_V27.md](PHYSICAL_VALIDATION_PLAN_V27.md), record results in [PHYSICAL_RESULTS_WORKSHEET_V27.md](PHYSICAL_RESULTS_WORKSHEET_V27.md) / its linked JSON ledger, and apply [CNC_FREEZE_GATE_V27.md](CNC_FREEZE_GATE_V27.md). The c1bb566 baseline retains all 59 hardware blockers until authoritative physical evidence and the corresponding proof tests exist.

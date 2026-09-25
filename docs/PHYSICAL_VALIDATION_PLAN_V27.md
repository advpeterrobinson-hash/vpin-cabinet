# Physical validation cycle — v27

Baseline: `c1bb566a8eff24240434c3f084e068c20e7cd4a0`. **Manufacturing BLOCKED.** This plan changes neither geometry nor hardware authority. All dimensions below are project packaging candidates unless accompanied by accepted physical evidence. Numerical test screens below are proposed prototype acceptance criteria, not certified capacities or new machining tolerances.

## Recovery and audit

Annotated tag `checkpoint/v27-physical-validation-baseline` identifies the exact committed baseline. No previous tags or tag naming policy were found; this deliberately uses a checkpoint name rather than a production version. It excludes the owner's uncommitted master FCStd and deleted backup. Recover into a separate checkout/worktree from the tag and run `make cnc-detail`; do not reset the owner's working tree. Generated galleries/CAD are rebuildable outputs, not contents guaranteed by the tag.

Audited the hardware pack, owner review, validation record, current feature/joint registers and all 17 current gallery images. The record remains **173 defined + 59 hardware-blocked = 232 feature groups**, 29 permanent wood records, 32 total wood records and 11 separately counted carriers. The 59 groups span 22 hardware IDs; HF-014 is adapter-only but remains blocked on the replaceable CPU board. Zero design-only feature rows does NOT mean the process/proof gates are complete.

The gallery shows candidate envelopes and nominal discrete sweeps, not measured assemblies. Views 02–04/17 guide controls; 05/09 guide intake; 06–08 guide carriers/SSF; 10/11 guide props; 12–14 guide backbox access; 15 guides CPU service; 16 guides structure. No new structural contradiction was established by this audit. Two known limitations remain explicit: the narrow outboard prop corridor needs physical tolerance testing, and the 740 mm monitor cannot exit flat through the 520 mm rear door. The front-removal route needs a real mockup. The nominal 13.8 mm rear rail/bracket gap is still below the 15 mm planning reserve; do not adjust it without the actual stack.

## Evidence workflow and test order

1. Read [CNC_FREEZE_GATE_V27.md](CNC_FREEZE_GATE_V27.md). Obtain production-stock samples, measurement tools and the minimal hardware set in [HARDWARE_MEASUREMENT_PACK_V25.md](HARDWARE_MEASUREMENT_PACK_V25.md). No additional electronics procurement is required by this plan.
2. Label physical components by HF ID, revision, serial/batch and handed side. Photograph datums A/B/C; record instrument ID, resolution, zero check, date, operator, units, repeat readings and uncertainty. A catalogue can identify a part and specify an allowable fit/rating; it is not the measured pattern of the delivered part.
3. Use cardboard/foam/full-size printed references for hand and service mockups. Check any print's scale against a known dimension. Use outsourced sacrificial fixture panels for hardware trial holes, clearly marked PROTOTYPE. These are not final cabinet panels and do not authorize home transfer-drilling of structural holes.
4. Collect dimensions first; review fixture strength and fastener loads before load tests. Then test clearances, service actions, props, lift ergonomics and airflow packaging. Keep mains unpowered during mechanical trials.
5. Fill [PHYSICAL_VALIDATION_RESULTS_V27.json](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json). It maps all 59 blocked groups to shared component measurement records and explicit part/feature IDs. Fill each measurement separately; keep raw readings/photos/test records in repository-relative evidence files. Preserve failed attempts and superseded revisions. Reuse a measurement across groups only where the same identified physical part and datum transform apply.
6. `UNMEASURED` → `RECORDED` → `REVIEWED` describes evidence only. None of these statuses clears a CNC blocker. A separate reviewed geometry change must satisfy the gate. Unknowns stay null; never copy the provisional text into measured fields. The validator checks evidence completeness, not truth or structural adequacy.

## A — HF-030 plunger

Fixture datums: A = outside front mounting face, +Y inward; B = shaft axis; C = antirotation orientation, +Z up. Record the relation of these datums to global cabinet coordinates. Candidate center X520 Z215; body X500..540/Y18..220/Z195..235; cable reserve X500..540/Y220..255/Z185..245; handle projection 80 mm is only a reserve.

Measure the delivered mechanism, including every mounting variant actually used:

- Required panel contour, diameter(s), flats/keyways, corner radii and any stepped recess; sleeve OD and length; shaft OD; antirotation tab dimensions/orientation.
- Every hole/slot center in signed X/Z from B, diameter or slot width/length/end radius, countersink/counterbore and fastener head/tool envelope. Measure from common datums, not chained hole spacing. Record flange outline, thickness, seating flatness and coverage around the cutout.
- Thread pitch/length, usable grip range, washer/nut dimensions, required engagement and wrench space at actual measured plywood/finish thickness. Confirm mounting without crushing wood or bottoming the thread.
- Handle/rest projection, fully pulled projection, inward limit, total stroke, shaft/spring/body/sensor bounds at rest and both limits. Record moving envelopes rather than one closed bounding box.
- Connector mating direction, plug dimensions, strain relief, minimum cable bend radius, disconnect access and cable sweep through full stroke. Record maker limits separately from measured values.

Use calipers, depth rod, square and pin gauges as appropriate; target center/stack recording uncertainty ±0.10 mm and outline ±0.5 mm per the hardware pack. Those are not bore-fit tolerances. Repeat the pattern from an independent reference and test in a sacrificial thickness-matched panel.

Run at least 20 deliberate full-stroke cycles in the mockup; inspect clearance to launch/start controls, coin door and its open swing, right flipper internals, leg bracket/bolt stack, prop riser/stow and cradle throughout opening/closing. Record smallest gap, location and state, and available hand/wrench space. Acceptance requires no contact, snag, binding, unintended activation or pinch in intended use, full return/stroke and retained fasteners. Clearance after measured tolerance, coating, mounting play and cable movement must remain positive; reviewer must approve a numerical allowance for each interface before bore release. No generic zero-clearance CAD result is sufficient.

Final bore gate: identified delivered sample; complete verified pattern/stock stack; approved bore fit and antirotation; passed mockup with actual controls and owner ergonomic sign-off; clearance budget and service tools checked; dated evidence linked to HF-030 and its CF group; reviewed CAD datum transform and coupon fit. A failed envelope fit triggers a documented design review, not an invented smaller plunger.

## B — two captive props

Candidate fixed pivots Y80 Z330, rod planes X28/X572, roughly 896.8 mm pin-to-pin and 8 mm diameter; rearward stow ends near Y976.8 at Z330. These are fixture starting points only. Lower risers share the shaped landing/prop reinforcement. Do not make a freestanding jig that bypasses this actual load path.

Measure each side separately: rod straightness/section/material identification, end eyes and centers, pin fits and shoulders, clevis ear thickness/spacing, edge distances, fastener patterns/stacks, backing contact, receiver position relative to outer cradle rail, upper pin insertion/withdrawal path and positive keeper engagement. Measure stow clip throat/depth, transverse keeper, attachment pattern and rod rattle allowance. Record the lower pin's captive retention as well as the upper keeper. A rod lying in an open hook is not a positive support.

Use a full-width representative shell/cradle fixture with measured stock, combined reinforcements, actual pivot bearings, backing, bolts and both props. Install representative buttons/leg stacks/SSF reserves and cable bundles. Check all intermediate deployment/retraction positions continuously, not only the CAD's 2-degree samples. Repeat with maximum measured joint play and representative finish thickness. Record smallest rod/rail/sidewall/hardware/hand clearance; rubbing, trapped fingers, cable snagging, keeper interference or contact on a weak/reduced skin is a failure. The narrow corridor requires an explicit tolerance budget approved before pattern release.

With an independent support carrying the cradle, verify that the intended user can reach each keeper, recognize full engagement, engage both props and later unload/disengage/stow them while maintaining safe control. Document the sequence and whether a second person is needed. Either prop must resist casual unseating without friction: a defined removal action on its positive keeper/pin is required. Check stow retention during normal lid cycles and recorded gentle cabinet handling; this is not a quantified impact/fatigue qualification.

### Independent load proof: LEFT, then RIGHT

Prerequisite: have a competent mechanical reviewer approve fixture stability, wood bearing/edge distances, rod buckling/end strength, pin shear/bending, clevis bending and fastener/backing capacity using actual material and assemblies. The 8 mm candidate has no established rating. Record approved load, distribution, hold time, displacement limits and reviewer before applying load. Never use a person as ballast or work under an unproven assembly.

1. Restrain the fixture against tip/slip independently. Use inert secured ballast representing the measured moving assembly and its measured/most adverse reviewed mass distribution. The qualification mass must cover the declared maximum moving assembly, at least the current 16.5 kg planning mass; if the actual assembly is heavier, use the higher mass after revising the load review. Do not extrapolate a lighter test to the design envelope.
2. Provide an independent rated catch/support with a small documented unloaded gap; confirm it carries no normal test load. Use remote loading/observation with people out of the collapse path. Disconnect power. The opposite prop is disengaged and secured so it cannot share load; record this in the test photo.
3. Zero displacement gauges at rod midpoint, upper receiver, fixed anchor/backing and front cradle corners. Mark fasteners to expose slip. Pre-weigh empty fixture self-mass: do not count only added ballast. A loading support carries excess self-weight while establishing the lower increments.
4. At the approved service angle, transfer 25%, 50%, 75%, then 100% of the approved total gravity load to the test prop. Hold each increment 10 minutes; record actual total load, distribution, angle, deflections, twist, fastener movement and whether the catch touched. If the fixture cannot realize partial loads safely, reviewer must revise the procedure before starting.
5. Stop and fail for crack/delamination, growing lateral rod bow, sudden displacement, pin/keeper migration, fastener slip, anchor crushing/lift, receiver disengagement, catch contact or uncontrolled descent. Do not tighten under load and continue as if it passed.
6. Unload under independent support. Proposed residual-set screen: ≤0.5 mm at each recorded location, no damage/slip and fully functional pins/keepers/stow afterward. Loaded deflection must stay within a numerical limit set BEFORE testing from clearance and stability analysis; no limit currently exists, so an unreviewed test cannot be marked PASS. Record gauge uncertainty. Passing this screen alone is not capacity certification.
7. Repeat the complete sequence for the other prop. After individual passes, cycle engagement/release with both installed at least 20 times under independent backup; repeat checks after settling. Record asymmetry and reach problems. Additional off-center, disturbance and durability load cases must be specified by the reviewer before final qualification; do not improvise drop tests or infer fatigue strength from a static hold.

Failure observations: rod bow/permanent bend, eye elongation, pin bending/walkout, keeper opening, clevis spreading, bolt rotation, washer embedment, wood splitting/delamination, backing separation, cradle twist, movement toward accidental release, jammed release, snagged cables and stow rattle. Record each side's raw observations even when zero. Replacement or altered anchors invalidate the affected proof; repeat after repair. Both prop records and the final qualification scope must be reviewed before anchor holes become authoritative.

## C — moving assembly mass and ergonomics

Weigh display, complete cradle, adapters, moving journals/plates, moving latch/receiver pieces and attached cable portions; record included/excluded items and scale uncertainty. Weigh the completed moving assembly independently if possible; reconcile the component sum. Preliminary 16.5 kg = 12 kg display allowance + 4.5 kg cradle allowance, not an observation. If unavailable, use labeled ballast for a provisional trial and keep final mass/ergonomics OPEN. Do not buy a display solely to close a shell hole pattern.

With independent backup and approved fixture, use a calibrated force gauge at the intended front grip, measuring vertical force as in the model. Record grip coordinates, cabinet leg height, angle (closed then 10-degree increments and all local peaks through service), opening and lowering force, start/breakaway force and cable drag. Repeat three slow cycles; never abruptly release. Record actual service angle rather than assuming the nominal rotation. If a different force direction is used, record it and recalculate the comparison.

Compare the force-angle observations with the estimate (~86.1 N peak, ~75.7 N at service); record observed minus predicted and percentage difference. These predictions exclude friction and handling margin and are not an acceptance limit. Record actual mass distribution/CG information where safely obtainable; no balancing a heavy display precariously on an edge.

The owner must try opening, holding while securing each prop, unloading the props, closing and controlled descent, with assistance/backup available. Record reach, hand placement, pinches, awkward posture, shaking/fatigue, visibility of keepers and ability to stop at intermediate angles. PASS requires a documented comfortable, controllable procedure accepted by the intended user plus reviewed force measurements; calculation alone never passes ergonomics. If manual handling is unacceptable, keep the gate open and review an optional adapter-based assistance concept separately; no baseline gas holes return automatically.

## D — controls and SSF

Make a full-size front/side hand mockup at actual intended leg height and cabinet slope. Candidate side centers Y255/Z270 primary and Y310/Z270 optional action. Front START X125/Z250, EXIT X125/Z200, LAUNCH X470/Z230, plunger X520/Z215. Use the real button family samples including nuts/switches/terminals and real plunger; cardboard substitutes can screen placement but do not pass hardware fit.

Try both hands, sustained play, optional-action reach, simultaneous buttons, plunger pull/return and coin-door/service access. Record users, hand clearances and any unintended operation. Check internal nut/socket access and cables against leg stacks, cradle sweep and prop anchors/stow. Measure remaining wood ligament from actual proposed bore edges to profiles, joints, pockets and hardware—not just center spacing. Use the hardware pack's ≥7d loaded-end/≥4d other-edge screen where applicable to structural bolts; it is not an automatic large-button bore rule. Reviewer must approve actual sidewall ligaments and material after the final control layout.

Preserve solid SSF zones front L/R Y350..450 Z200..300 and rear L/R Y850..1000 Z200..280, 25 mm inward depth. Mark these on the mockup and check carriers/cables/clips cannot occupy them. Do not drill a speaker opening under an exciter. Exact exciter attachment remains a local adapter task; no bottom subwoofer cut is authorized. Final button and plunger bores remain blocked until both physical family measurements and ergonomics pass.

## E — serviceability checklist

For each action record mockup revision, operator, load, representative cable/connector dimensions, tools, disconnect sequence, minimum gap, photos/video and PASS/FAIL/OPEN. An empty-envelope test does not validate actual connectors. Unknown representative cable dimensions keep the corresponding final check open.

| Test ID | Trial | Acceptance required |
|---|---|---|
| SV-01 | Each 125 × 355 tray at X50/X425, Y285, Z125; representative 3 kg payload and 110 mm payload height | Remove and reinstall each independently with ordinary hand tools; fasteners captive/accessed; no glued attachment; labels and strain relief; cables unplug/reconnect without pulling other equipment or entering mains enclosure. Record extraction direction and needed slack. |
| SV-02 | Central access X190..410/Y300..810/Z116..276 | Reach intended service work without removing permanent structure; cable bundles cannot fill the reserve; verify tool/hand access and future toy space, not only a clear empty box. |
| SV-03 | One CPU board 285 × 460 at Z135, 450 mm rearward travel, door outward 105° | Actual slide/member/bracket/bolt stack clears rails/hatch/door/carriers; retainer/disconnect and connectors reachable; protected cable travel. Measure both rear-corner gaps. Run the separate 20 kg payload protocol in the hardware pack after load review; geometric service PASS alone does not pass load proof. |
| SV-04 | BB-DOOR-001-R1, 520 × 460 × 15; stop clear opening ~500 × 440 | Real hinge, keyed/tool latch and gasket allow outward opening, retention and closing without rubbing; reach DMD/speakers/lighting/wiring/central display mounts. No dependence on door for primary shear. Fixed upper fans/filters service without moving door wires. |
| SV-05 | Full 740 × 450 × 100 backglass replacement dummy and later actual monitor | Remove bezel and release mounts, disconnect cables and extract through front with safe grips/assistance; then reinstall. Record exact bezel attachment, tools, removal sequence and clearance. The rear door is NOT the full-display extraction route. Dummy validates envelope only; actual connector/mass/grip checks remain pending. |

## F — airflow and filter packaging

Inspect a representative measured-stock bottom coupon/fixture: 18 actual rounded 80 × 12 slots, R6 ends; banks X250/X350, centers Y330..570 at 30 mm pitch. Measure minimum 18 mm row webs, 20 mm center spine, crossmember/perimeter distances, edge quality and any breakout after finishing. These are baseline project screens; no weakening/trimming to fit a fan. Inspect actual rail/backing and leg zones for encroachment.

Trial the underside 220 × 290 filter cassette at X190/Y305 with planned 8 mm thickness, outside access and captive fasteners. Remove/reinstall with cabinet on actual legs, including floor/foot/hand clearance. Check media retention, seal/bypass, thickness/compression, sag, abrasion, cleaning and clearance to intake. A cardboard frame does not validate final media/filter pressure drop.

Trace both shelf/floor 100 × 40 passages and the fixed upper 100 × 80 exhaust openings with representative segregated cables, guards and installed service modules. Verify passages stay open and backbox folding does not trap the cable loops. Later fan depth/pattern, finger guard, vibration isolators, media thickness and connector access belong on replaceable adapters (HF-032); speaker modules similarly stay HF-033. Record whether a later component exceeds its adapter reserve; do not add a supplier pattern to permanent wood.

167.2 cm² nominal intake area is not evidence of cooling. After heat-producing equipment/fans/filter are selected, define thermal limits from those devices, representative operating modes/load, ambient conditions and filter state; log temperatures and airflow/noise observations through steady conditions. Commission with clean and service-due filter conditions under a reviewed test plan. Packaging can pass while thermal acceptance stays OPEN; neither slot area nor illustrative CAD arrows passes thermal commissioning.

## Owner results form (copy per trial)

Test ID / component / handed side: ______; baseline and fixture revision: ______

Physical part/batch: ______; date/operator: ______; instrument/zero check/uncertainty: ______

Approved load/angle/distribution/clearance/deflection limits and reviewer: ______

Raw readings with units and repeats: ______; measured minimum clearance/state: ______

Evidence paths/photos/video: ______; observations/failure modes: ______

Outcome OPEN / FAIL / PASS: ______; limitations: ______; reviewer/date: ______

Affected CF IDs: ______; retest or corrective action: ______

Do not erase a failure or mark final PASS where actual hardware, load scope, ergonomics or numerical acceptance criteria are still missing.

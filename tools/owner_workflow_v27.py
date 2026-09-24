"""Bench grouping only. IDs and measurement wording come from the results ledger."""
SESSIONS = [
    'Tools and preparation', 'Sheet stock / material measurements',
    'Plunger and visible controls', 'Buttons and control-panel ergonomics',
    'Captive props and mounting hardware', 'Electronics carriers and cable serviceability',
    'CPU access', 'Backbox / monitor access', 'Filter and airflow path',
    'Moving assembly mass and lift effort', 'Reviewed proof testing',
    'Final evidence reconciliation',
]
PLAN = 'docs/PHYSICAL_VALIDATION_PLAN_V27.md'
GATE = 'docs/CNC_FREEZE_GATE_V27.md'
PACK = 'docs/HARDWARE_MEASUREMENT_PACK_V25.md'

# Existing authorizations; HF-028 is a bundled measurement task, not a purchase.
BUY_NOW = {'HF-001', 'HF-003', 'HF-004', 'HF-006', 'HF-007', 'HF-008',
           'HF-010', 'HF-012', 'HF-013', 'HF-015', 'HF-016', 'HF-017',
           'HF-019', 'HF-020', 'HF-026', 'HF-027', 'HF-029', 'HF-030'}
REFERENCE_IDS = {'HF-008-M08', 'HF-013-M02', 'HF-013-M09', 'HF-031-M02'}


def specification():
    ops = []

    def add(session, key, title, groups=(), trials=(), *, category='A',
            mode='dimensional', dependencies=(), instructions='', samples=None,
            acceptance=None, source=PLAN, views=None):
        mids = [f'HF-{cid:03d}-M{number:02d}' for cid, numbers in groups for number in numbers]
        ops.append(dict(session=session, operation_id=key, title=title,
                        measurement_ids=mids, trial_ids=list(trials), category=category,
                        mode=mode, dependencies=list(dependencies), instructions=instructions,
                        samples=samples, acceptance=acceptance, acceptance_source=source,
                        views=views))

    add(0, 'PREP', 'Prepare the bench and result folder', mode='preparation',
        instructions='Open this checklist and print only the next operation sheets. Gather a pen, labels/masking tape, marker, phone/camera, ruler/square and the available measuring tools. Check instrument identity, resolution and zero; do not assume a ruler can resolve a bore fit. Make one folder per session; label every sample and handed side. No cabinet component is needed for this preparation step.',
        acceptance='Prepared labels, blank sheets and working instruments only; no dimensional or ergonomic acceptance.',
        views=[])
    add(0, 'ARRIVAL', 'Sort delivered samples and identify missing items', mode='preparation', dependencies=['PREP'],
        instructions='Use HARDWARE_ARRIVAL_INSPECTION_V27.md. Mark arrived / missing on paper. The case HF-014 is the only sample explicitly documented as already owned. Put maker drawings/specifications in a REFERENCE folder; do not enter them as measured values. Missing equipment means defer its operation, not buy an unapproved substitute.',
        acceptance='Identity and arrival recorded; no fit approval.', views=['identity'])
    add(1, 'STOCK-THICK', 'Measure sheet thickness once; retain all readings and min/max', [(1,[1,2])], dependencies=['ARRIVAL'],
        instructions='Mark nine distributed points on each actual sheet, including each door-stock batch. Measure without compressing veneers. Derive min/max from those same readings; do not remeasure just to fill M02.',
        samples='Nine points per sheet; all actual main and different door stock. Repeat readings where instrument repeatability is uncertain; no fixed repeat count otherwise specified.',
        acceptance='Recording target ±0.05 mm; retain spread. This does not approve sheet fit.', views=['identity','datum','reading','point-map'])
    add(1, 'STOCK-SURVEY', 'Survey the same labeled sheet', [(1,[3,4,5,6,7])], mode='survey', dependencies=['STOCK-THICK'],
        instructions='Keep the sheet label and corner datum. Measure sheet bounds and bow; note defects, grain and batch on one sketch. Reuse the identity photo from STOCK-THICK.',
        samples='Every actual sheet/batch; no additional fixed repetition count in the plan.', views=['point-map','defect-if-present'])
    add(1, 'SHOP-COUPON', 'Arrange shop tool readings and the physical fit coupon', [(2,[1,2,3,4,5,6])], ['PV-STOCK-TOOL'], category='B', mode='shop', dependencies=['STOCK-SURVEY'],
        instructions='Request actual cutter/runout and coupon results from the CNC shop. Do not measure a running spindle. Record each result separately using the shop instrument and coupon identity. Consultation now is already authorized; this is not a new machine/tool purchase.',
        acceptance='Shop-confirmed tool/fit/relief/two-face setup and physical coupon/dry fit required by the freeze gate; missing criteria stay OPEN.', source=GATE, views=['identity','coupon','reading'])
    add(2, 'PLUNGER-FACE', 'Measure the plunger mounting face and seating stack', [(30,[1,2,3,4,7])], dependencies=['ARRIVAL'],
        instructions='Identify front seating face A, shaft axis B and antirotation C. Use one face sketch for contour/flats, all hole centers, sleeve/shaft diameters, flange/nut stack and internal body/sensor depth. Keep the pattern readings separate from the shape readings.',
        samples='Delivered plunger and every installed mounting variant; repeat pattern from an independent reference.', views=['identity','datum','mount-face','reading'])
    add(2, 'PLUNGER-STROKE', 'Check the complete plunger stroke in its mock panel', [(30,[5,6,8])], ['PV-PLUNGER'], mode='mockup', dependencies=['PLUNGER-FACE','STOCK-THICK'],
        instructions='Use the actual mechanism in a sacrificial thickness-matched panel. Record rest, full pull and inward limit; handle projection and connector/cable movement. Check adjacent controls, coin-door swing, leg stack, props and cradle using the plan. Record missing neighboring hardware as a limitation; do not mark final PASS without it.',
        samples='At least 20 deliberate full-stroke cycles, as required by plan A.',
        acceptance='No contact, snag, binding, unintended activation or pinch; full return/stroke and retained fasteners. Reviewer-approved positive clearance budget and ergonomic acceptance still required before bore release.', views=['rest','full-pull','inward-limit','rear-clearance','interference-if-present'])
    add(2, 'COIN-FACE', 'Measure coin-door cutout, flange and bolts together', [(19,[1,2,3,4,7])], dependencies=['ARRIVAL'],
        instructions='Use one mounting-face sketch; include contour/radii, flange coverage, all holes and deepest internal protrusion.', views=['identity','mount-face','rear-clearance'])
    add(2, 'COIN-OPEN', 'Check coin-door swing and key/tool access', [(19,[5,6])], mode='mockup', dependencies=['COIN-FACE'],
        instructions='Check open/closed positions and access in the same front mockup used for the controls; share context photos with PLUNGER-STROKE.', views=['closed','open','rear-clearance'])
    add(3, 'BUTTON-FAMILY', 'Measure each button family in one caliper setup', [(20,[1,2,3,4,5,6,7])], dependencies=['ARRIVAL'],
        instructions='For each distinct button family, sketch bore/flats and antirotation, then bezel, thread, nut/washer and switch/connector depths. Measure actual nuts, washers and terminals, not just the button body.',
        samples='One real sample of every final button family; identify every variant. Repeat readings to establish instrument repeatability; no fixed count supplied.', views=['identity','mount-face','rear-clearance','reading'])
    add(3, 'RAIL-PROFILE', 'Measure the local siderail/channel prototype', [(21,[1,2,3,4,5,6])], dependencies=['STOCK-THICK'],
        instructions='Use the already-required short local profile prototype and safe glass-thickness gauge/mock panel. Record cross-section and its relation to the lockdown. Do not order final tempered glass from this step.', views=['identity','section','installed'])
    add(3, 'LOCKDOWN-FIT', 'Check receiver, glass capture and hand-tool access', [(22,[1,2,3,4,5])], mode='mockup', dependencies=['RAIL-PROFILE'],
        instructions='Use the local lockdown/receiver prototype in the same front/side mockup. No load test here; loaded deflection is collected later under LOADS.', views=['mount-face','latched','released','tool-access'])
    add(3, 'CONTROLS-HANDS', 'Try both hands and mark the four solid SSF zones', trials=['PV-CONTROLS-SSF'], mode='mockup', dependencies=['BUTTON-FAMILY','PLUNGER-STROKE','COIN-OPEN','LOCKDOWN-FIT'],
        instructions='Use intended leg height/slope and actual buttons/plunger. Try sustained play, both hands, simultaneous buttons, optional action and full plunger stroke. Check internal nuts/cables and mark all four SSF zones; use the source plan D for the existing candidate layout, never read dimensions from a render.',
        acceptance='Owner placement/hand acceptance plus recorded internal clearance and structural ligament review. Preserve solid SSF plywood; final bores stay blocked. No fixed number of hand trials is specified.', views=['hand-placement','rear-clearance','ssf-zones'])
    add(4, 'LEGS-BARE', 'Measure all four legs using the same datum jig', [(3,[1,2,3,4,5,6,7,8])], dependencies=['ARRIVAL'],
        instructions='Record bolt centers/slots, angle, flange/seat flatness and leveler travel for each labeled leg. M08 identifies the four instances; reuse their readings rather than repeating the entire set.', samples='All four legs and matching installed fasteners.', views=['identity','mount-face','reading'])
    add(4, 'BRACKET-BARE', 'Measure brackets, backing and loose fastener stacks', [(4,[1,4,5,7])], dependencies=['LEGS-BARE'],
        instructions='Keep each bracket with its own leg/bolts. Record thickness, pattern, assembled bolt/nut/washer stack and backing contact. Installed rear X/Y/Z readings are deferred to REAR-STACK so the corner fixture is built once.', samples='All four bracket/backing stacks; preserve left/right differences.', views=['mount-face','bolt-stack','backing-contact'])
    add(4, 'BEARINGS', 'Measure both bearing housings and bore interfaces', [(8,[1,2,3,4,5,6,7])], dependencies=['ARRIVAL'],
        instructions='Use suitable bore/pin gauges for fit-critical bores; calipers for outline and mounting pattern. Record face-to-axis offset and access to set screws on both housings.', samples='Both housings, separately identified.', views=['identity','mount-face','bore-reading','tool-access'])
    add(4, 'BEARING-REF', 'File the maker misalignment limit as reference', [(8,[8])], mode='reference', dependencies=['BEARINGS'],
        instructions='Save the maker document identity/revision and stated misalignment limit on the reference sheet. This ID asks for documented maker data, not a physically measured angle limit. Leave measured_value null; return the reference for engineering review without weakening the evidence validator.', views=[])
    add(4, 'JOURNALS', 'Inspect the physical journal/cheek-plate prototype', [(9,[1,2,3,4,5,6,7])], dependencies=['BEARINGS'],
        instructions='Wait for the local prototype and its reviewed drawing. Record fit/finish, engagement, shoulders, retention, installed stack/edge distances and the actual drawing revision together.', views=['identity','shoulder','installed-stack'])
    add(4, 'PROPS-BARE', 'Measure both rods, clevises, pins and keepers', [(10,[1,2,3,4,5])], dependencies=['ARRIVAL'],
        instructions='One setup per handed set: rod ends/length, clevis/receiver patterns, pin/keeper engagement and stow clips. Keep left/right readings separate. Do not test capacity here.', samples='Both rods and all lower/upper/stow hardware, separately labeled.', views=['identity','mount-face','keeper-engaged','stow-clip'])
    add(4, 'LATCH-PADS', 'Measure the closed latches and pads in the fixture', [(12,[1,2,3,4,5])], mode='mockup', dependencies=['PROPS-BARE','JOURNALS','STOCK-THICK'],
        instructions='Record both latch patterns, grip/release envelope and pad footprint/loaded thickness. Use only the independently supported fixture described in the plan; if compression cannot be measured safely, leave it open for review.', views=['closed','released','pad-stack'])
    add(4, 'PROP-MOTION', 'Check rod deployment and stow with independent support', [(10,[6])], ['PV-PROP-MOTION'], category='B', mode='motion', dependencies=['PROPS-BARE','JOURNALS','LATCH-PADS','CONTROLS-HANDS'],
        instructions='Use the reviewed full-width fixture and independent support; follow plan B. Check the complete continuous movement, both keepers, hand access and stow retention. No capacity test or work under an unproven assembly.',
        acceptance='No rubbing, trapped fingers, snag, keeper interference or weak-skin contact; positive pins/keepers required. Narrow-corridor tolerance budget still needs approval.', views=['deployed','stowed','keeper-engaged','minimum-clearance'])
    add(5, 'MAINS-FIT', 'Measure the unpowered mains module and enclosure together', [(17,[1,2,3,4,5,6,7]),(27,[1,2,3,4,5])], dependencies=['ARRIVAL'],
        instructions='Use the same identified enclosed assembly for both IDs; record module and enclosure dimensions separately. Keep it unplugged. Capture mount pattern, strain relief, cord bend, lid/disconnect and service access without exposing or energizing mains.', views=['identity','mount-face','cord-clearance','lid-access'])
    add(5, 'ETHERNET', 'Measure the optional network adapter, if selected', [(18,[1,2,3])], dependencies=['ARRIVAL'],
        instructions='WAIT unless the optional adapter is available. Record coupling aperture, retention and bend radius on its removable carrier. A blank option is not permission to invent an RJ45 measurement.', views=['identity','installed'])
    add(5, 'SSF-ADAPTER', 'Inspect exciter footprint and local cable clearance', [(31,[1,3,4])], dependencies=['CONTROLS-HANDS'],
        instructions='WAIT for later selected exciters. Keep the four solid zones intact; record adapter footprint, projection and cable/service clearance. Do not cut speaker holes.', samples='Four locations; every different device/adapter type, with location IDs.', views=['identity','installed','rear-clearance'])
    add(5, 'SSF-REF', 'File the adapter attachment specification', [(31,[2])], mode='reference', dependencies=['SSF-ADAPTER'],
        instructions='Save the actual adapter screw/adhesive specification revision as supplemental reference. A specification is not a measured dimension; measured_value remains null pending review.', views=[])
    add(5, 'TRAYS', 'Remove and reinstall each tray with representative cables', trials=['SV-01'], mode='mockup', dependencies=['MAINS-FIT','STOCK-THICK'],
        instructions='Use the two existing candidate trays, ordinary fasteners and representative low-voltage bundles/connector bodies. Follow plan E SV-01; record missing cable/device details. The plan\'s payload envelope is a requirement, not a newly authorized proof test.',
        acceptance='Each tray independently removable/reinstalled with ordinary tools; no glue, cable pulling or entry into mains enclosure. Fasteners accessible/captive, strain relief and labels; record extraction direction/slack.', views=['installed','extraction','cabling','tool-access'])
    add(5, 'CENTRAL', 'Reach the central service area with cables installed', trials=['SV-02'], mode='mockup', dependencies=['TRAYS'],
        instructions='Use the same installed cables; avoid another fixture setup. Try the intended service tasks with hand tools and record the path, not only an empty-box clearance.',
        acceptance='Service work possible without removing permanent structure; cable bundles cannot fill the reserved access volume. No new minimum gap is defined.', views=['service-path','cabling'])
    add(6, 'CPU-CASE', 'Measure the already-owned open case', [(14,[1,2,3,4])], dependencies=['ARRIVAL'],
        instructions='Use the actual case; measure foot/mount/standoff stack and connector/GPU restraint access on the single replaceable board.', views=['identity','underside','connector-access'])
    add(6, 'SLIDES-BARE', 'Measure the two slide members and travel', [(13,[1,3,4,5,6,7,8])], dependencies=['ARRIVAL'],
        instructions='Identify fixed and moving members separately, left and right. Record patterns, stops, travel, disconnect and actual screw-head space from one member layout. Do not infer maker minimum clearance from these dimensions.', samples='Both slides; fixed and moving members separately.', views=['identity','fixed-member','moving-member','closed','extended'])
    add(6, 'SLIDE-REF', 'File maker clearance and rating conditions', [(13,[2,9])], mode='reference', dependencies=['SLIDES-BARE'],
        instructions='Save maker min/max side clearance and rating orientation/conditions with document revision. These remain reference data; actual installed clearances are collected in REAR-STACK. Leave measured_value null on reference-only entries.', views=[])
    add(6, 'CLAMPS', 'Measure four clamps, backing and the retainer', [(26,[1,2,3,4,5,6])], dependencies=['SLIDES-BARE'],
        instructions='One labeled set-up per clamp: legs/bend, holes, backing and bolt stack. Record bolt markings as identification, not a measured strength. Record retainer movement and tool access.', samples='All four clamps/backing sets and the stowed retainer.', views=['identity','mount-face','bolt-stack','retainer'])
    add(6, 'CPU-HINGE', 'Measure both leaves of the CPU door hinge', [(15,[1,2,3,4,5,6,7])], dependencies=['ARRIVAL'],
        instructions='Measure both leaves from hinge end, seating face and axis; include folded stack and possible opening angle.', views=['identity','mount-face','folded','open'])
    add(6, 'CPU-LATCH', 'Measure latch, catch, gasket and tool access', [(16,[1,2,3,4,5,6,7,8])], dependencies=['CPU-HINGE'],
        instructions='Use the CPU door mockup to record body cutout/flats, fixing/catch, grip and compressed gasket. Keep any shared backbox-family parts separately identified.', views=['mount-face','latched','gasket-stack','tool-access'])
    add(6, 'REAR-STACK', 'Measure the installed rear-corner stack once', [(4,[2,3,6]),(28,[1,2,3,4])], mode='mockup', dependencies=['BRACKET-BARE','CLAMPS','CPU-CASE','CPU-LATCH','STOCK-THICK'],
        instructions='In the measured-stock corner fixture, record both rear corners including all bolts/nuts/washers. Reuse the same Y/Z and access observations for HF-004 and HF-028, keeping each ledger entry separate. Preserve signed coordinates and the actual narrowest gap/state.', samples='Both rear corners and all relevant slide positions.', acceptance='Compare to the existing planning reserve; a nominal or positive gap alone does not release the stack. Actual clearance/fastener/load review remains required.', views=['installed','bolt-stack','minimum-clearance','tool-access'])
    add(6, 'CPU-QUALIFY', 'Review CPU removal, then perform only approved CPU proof', trials=['SV-03'], category='B', mode='proof', dependencies=['REAR-STACK','CENTRAL'],
        instructions='SV-03 combines service and load evidence. First document unpowered removal/retainer/cables. The load portion must WAIT for fixture/fastener review; follow the existing hardware-pack CPU protocol unchanged. Keep service-only success distinct from final trial PASS.',
        acceptance='Plan E SV-03 and hardware-pack CPU proof criteria apply. Existing numerical targets are proposed prototype targets requiring review, not a new certified rating.', source=PACK, views=['closed','extended','removal-path','cabling','approved-load','deflection'])
    add(7, 'BB-HINGES', 'Measure the paired backbox hinges and pivots', [(6,[1,2,3,4,5,6,7,9])], dependencies=['ARRIVAL'],
        instructions='Use one datum sketch per leaf/handed assembly; include bushings, shoulder/thread and differences. Do not assume the two sides match.', samples='Both hinge assemblies; both leaves and mating pivot parts.', views=['identity','mount-face','pivot-stack'])
    add(7, 'BB-LOCKS', 'Measure upright locks in the supported hinge fixture', [(6,[8]),(7,[1,2,3,4,5,6,7])], category='B', mode='motion', dependencies=['BB-HINGES','STOCK-THICK'],
        instructions='Use the supported fixture described by the source plan/pack. Collect folded/upright sweep and installed lock X/Y/engagement in the same set-up. Do not support an unproven backbox by its locks while measuring.', views=['folded','upright','lock-engaged','tool-access'])
    add(7, 'BB-DOOR', 'Measure and service the rear door', [(29,[1,2,3,4])], ['SV-04'], mode='mockup', dependencies=['BB-LOCKS'],
        instructions='Identify the actual hinge/latch/gasket set separately from CPU hardware even if the family matches. Record door sweep and access to wiring, DMD, speakers, lighting and fixed fans.',
        acceptance='Outward operation/retention without rubbing; service access demonstrated. Door is not primary shear structure; no moving fan wiring required. Actual hinge and gasket fit still reviewed.', views=['closed','open','gasket-stack','service-access'])
    add(7, 'BB-MONITOR', 'Measure the later selected backglass on the bench', [(25,[1,2,3,4])], dependencies=['ARRIVAL'],
        instructions='WAIT for the actual monitor. Record VESA, bezel, connectors and mass; do not copy catalogue mass. Use safe supported handling/assistance; defer weighing if it cannot be done safely.', views=['identity','rear','connector-access','scale-reading'])
    add(7, 'BB-SPEAKERS', 'Measure later speaker modules and baffles together', [(33,[1,2,3,4,5])], dependencies=['ARRIVAL'],
        instructions='WAIT for selected modules. Measure driver pattern, magnet/connectors, baffle and rail attachment; keep these operations on replaceable modules.', views=['identity','mount-face','rear-clearance'])
    add(7, 'BB-REMOVE', 'Rehearse full monitor replacement through the front', trials=['SV-05'], mode='mockup', dependencies=['BB-DOOR'],
        instructions='First use the full-envelope dummy, with supported handling/assistance. Record bezel/mount release, plugs, grips, extraction and reinstallation. BB-MONITOR provides later actual-device evidence; without it the trial remains OPEN for actual mass/connector/grip checks. Do not attempt to pass the full monitor flat through the rear door.',
        acceptance='Front removal/reinstallation demonstrated with safe access, tools and assistance; dummy is envelope-only, not final actual-monitor acceptance.', views=['bezel-off','mount-release','front-extraction','cabling'])
    add(8, 'FILTER', 'Inspect the later filter cassette/media and removal route', [(32,[1])], ['PV-AIRFLOW'], mode='mockup', dependencies=['STOCK-SURVEY'],
        instructions='Check actual slot coupon/fixture, row webs and clear passage route against plan F; do not take dimensions from pictures. Trial external filter removal and retention. Leave final media/pressure-drop or missing hardware checks OPEN.',
        acceptance='Use existing plan F packaging dimensions/screens; no thermal adequacy from slot area. Do not trim structural wood to fit a fan.', views=['slots','filter-installed','filter-removal','passage-obstruction'])
    add(8, 'FANS', 'Measure later fans, guards and removable adapters', [(32,[2,3,4])], dependencies=['FILTER'],
        instructions='WAIT for selected fans/guards. Measure thickness and pattern on replaceable adapters; maker performance data is supplemental reference only.', views=['identity','adapter-face','rear-clearance'])
    add(8, 'THERMAL', 'Defer thermal commissioning until reviewed conditions exist', trials=['PV-THERMAL'], category='B', mode='commission', dependencies=['FANS'],
        instructions='WAIT for final heat-producing equipment, protected electrical commissioning and an approved thermal plan. Log ambient/modes/load/filter state and temperatures as required by plan F. No new temperature limits are supplied here.',
        acceptance='Limits must come from selected equipment and the reviewed commissioning plan. Slot area and CAD arrows cannot pass this trial.', views=['setup','sensor-position','filter-state'])
    add(9, 'PF-DISPLAY', 'Measure later playfield adapter and connector fit', [(24,[1,2])], dependencies=['ARRIVAL'],
        instructions='WAIT for the actual display; measure its adapter pattern and connectors. Keep physical support stable; do not buy a display to close a shell hole.', views=['identity','rear','connector-access'])
    add(9, 'MOVING-MASS', 'Weigh and reconcile the actual moving assembly', trials=['PV-MASS'], mode='mass', dependencies=['PF-DISPLAY'],
        instructions='Weigh supported components and, if safely possible, the completed moving assembly. List included/excluded moving hardware and cable portions; reconcile the sum. A ballast mockup is provisional and leaves actual mass OPEN.',
        acceptance='Actual included mass, identity and scale uncertainty documented; the preliminary mass is not a reading. No new mass acceptance limit.', views=['scale-reading','assembly-identity'])
    add(9, 'LIFT', 'Record lift effort and the owner\'s controlled descent trial', [(24,[3])], ['PV-ERGONOMICS'], category='B', mode='force', dependencies=['MOVING-MASS','PROP-MOTION'],
        instructions='WAIT for the approved fixture and independent backup support. Reuse MOVING-MASS results in the composite M03 entry; do not weigh twice. Record grip/direction/angle and opening/lowering/breakaway force. The observed force, not the prediction, goes on the sheet.',
        samples='Three slow cycles; closed then 10-degree increments and all local peaks through service, as in plan C.',
        acceptance='Owner must accept comfortable, controllable opening/holding/prop operation/closing plus reviewed force data. Predicted ~86 N is not an acceptance threshold.', views=['grip','gauge-reading','keeper-reach','controlled-descent'])
    add(10, 'PROP-LEFT', 'LEFT prop independent full-load proof', trials=['PV-PROP-L'], category='B', mode='proof', dependencies=['PROP-MOTION','MOVING-MASS'],
        instructions='STOP until the mechanical reviewer has approved the fixture, load/distribution, angle, catch, limits and procedure in plan B. Execute the existing LEFT protocol unchanged, with the opposite prop unable to share load. No person under the unproven assembly.',
        acceptance='Only reviewed plan B qualification applies. Proposed residual-set screen does not supply the still-missing loaded-deflection limit. No unreviewed PASS.', views=['fixture','opposite-prop-disengaged','approved-load','deflection','keeper','after-unload'])
    add(10, 'PROP-RIGHT', 'RIGHT prop proof and reconcile the pair\'s capacity evidence', [(10,[7])], ['PV-PROP-R'], category='B', mode='proof', dependencies=['PROP-LEFT'],
        instructions='Run the independent RIGHT protocol, then reconcile both reviewed reports for M07. Reuse LEFT evidence; M07 must cover both sides, never infer a generic capacity from rod diameter. Follow the source plan\'s post-proof settling/engagement checks.',
        acceptance='Both independent proofs and qualification scope must be reviewed. A single-side pass or static hold alone cannot establish the whole qualification.', views=['fixture','opposite-prop-disengaged','approved-load','deflection','keeper','after-unload'])
    add(10, 'LOADS', 'Obtain the remaining reviewed structural load qualifications', [(22,[6])], ['PV-LOADS'], category='B', mode='proof', dependencies=['LEGS-BARE','BRACKET-BARE','JOURNALS','BB-LOCKS','LOCKDOWN-FIT'],
        instructions='WAIT for reviewed leg/backbox/pivot/lockdown fixtures and criteria. Record lockdown loaded deflection under its approved case alongside the other qualification reports; no load or safety factor is defined by this checklist.',
        acceptance='Reviewed qualification scope, numerical criteria and evidence required by freeze Gate 1. Undefined tests remain OPEN.', source=GATE, views=['fixture','approved-load','deflection','after-unload'])
    add(10, 'SKATES', 'Later mobility engagement/stability check', [(5,[1])], category='B', mode='proof', dependencies=['LOADS'],
        instructions='WAIT; external skates are BUY LATER. Before mobility use obtain reviewed safe handling/load conditions and inspect physical leg engagement/stability. No cabinet lifting or rolling trial is authorized by this sheet alone.',
        acceptance='Physical engagement/stability before mobility use as required by the measurement pack; no numerical mobility test criteria exist here.', source=PACK, views=['engagement','setup'])
    add(11, 'GLASS', 'Later final supported glass-opening measurement', [(23,[1,2,3])], dependencies=['RAIL-PROFILE','LOCKDOWN-FIT'],
        instructions='WAIT until the supported rail/lockdown mockup is accepted. Record opening, engagement/expansion clearances and physical thickness sample. Use safe mock material for trials; final glass remains BUY LATER.', views=['supported-opening','engagement','thickness-reading'])
    add(11, 'ELECTRICAL', 'Obtain protected electrical/cable/fold commissioning evidence', trials=['PV-ELECTRICAL'], category='B', mode='commission', dependencies=['MAINS-FIT','BB-LOCKS','TRAYS','REAR-STACK'],
        instructions='WAIT for the reviewed protected electrical design and competent commissioning. Ordinary bench measurements are unpowered; do not energize exposed mains to fill this result. Include cable segregation, strain relief, protected distribution and fold/service evidence.',
        acceptance='Existing source electrical/safety and freeze gates apply; no new electrical procedure or pass limit.', source=GATE, views=['protected-assembly','cable-route','fold-clearance'])
    add(11, 'RECONCILE', 'Return sheets and evidence without filling gaps from estimates', mode='preparation', dependencies=['ARRIVAL'],
        instructions='Use the queue to list completed, missing, reference-only and review-required operations. Return the actual sheets/photos even if later sessions remain OPEN. Transcribe by measurement/trial ID only; preserve repeats, units, uncertainty, failures and identity. Do not mark a whole component RECORDED until all its required measurements have real evidence.',
        acceptance='No unknown, duplicated or omitted authoritative IDs; unperformed work remains blank/OPEN. This is evidence handoff, not geometry release.', views=[])
    add(11, 'PACKAGE', 'Engineering/owner review of the eventual final CNC package', trials=['PV-CNC-PACKAGE'], category='B', mode='review', dependencies=['RECONCILE','SHOP-COUPON','PROP-RIGHT','LOADS','CPU-QUALIFY','LIFT','BB-REMOVE','FILTER','ELECTRICAL','THERMAL'],
        instructions='DEFER. The present task generates no geometry or production exports. When corresponding physical evidence exists, engineering must apply the existing gate to drawings, fasteners, laminate IDs, nesting/exports and owner manufacturing approval. Partial evidence is not a package PASS.',
        acceptance='All three existing freeze gates; no release by checklist or queue status.', source=GATE, views=[])
    return ops

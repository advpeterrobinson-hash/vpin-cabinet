# V32 backbox service architecture — owner correction

**Review candidate, not promoted. Manufacturing BLOCKED.** The complete populated candidate clears the WPC fold with its backbox glass installed. Both rear doors reach 100°. A remaining service tradeoff prevents automatic promotion: the inset lower cassette obstructs the existing upright-lock tool columns. Withdrawing the cassette through the front restores those columns; it can then be secured again before folding. This is additional preparation, not an accepted change to the locking interface.

Head before this work: `79819c4375f24f4d2b6d7743f3aa4d67def35ef7`, the previously committed cradle integration following `ca56e7f…`. Branch: `feat/cabinet-review-v32`. The delivery commit identifies HEAD AFTER. No accepted cabinet or viewer B-rep was overwritten.

Start with the [offline review gallery](../../exports/generated/backbox-service-v32/index.html), [both rear doors open](../../exports/generated/backbox-service-v32/D-review.png), [retained-glass fold](../../exports/generated/backbox-service-v32/X-review.png), and [lock-access limitation](../../exports/generated/backbox-service-v32/Z-review.png). The gallery contains the requested A–T views and seven additional integration/future-capacity views. These are tessellations/sections of generated FreeCAD solids, not illustrative concept art.

## Authority and preserved architecture

The owner correction is the governing service policy. It supersedes the historical single backbox door, fixed upper fan panel, mandatory rear display passage, aluminium-rail preference, and connector-specific cable closure assumptions. Historical values in `backbox_mounting_v12.json` are explicitly marked superseded. Main-cabinet rear fans and its existing door are separate systems and remain unchanged.

- Kinematics: transverse X axis, **Y1066.8 / Z508**, pure rotation. No Y1270 datum or depth study was reopened.
- Backbox lower sides: **210 mm**; floor front **Y1146**; rear shelf, 260 × 60 generic passage and the selected cradle relief remain unchanged. Upper glass rebates are new candidate-only subtractions from the sides/top.
- The entire accepted playfield mechanism, six cradle screws, glass channels, matrix supports/cassette, shelves, SSF and PC arrangement remain intact.
- Playfield glass and matrix must be removed for backbox folding. **Backbox front glass is a different part and stays installed.** Rear doors are latched and all display/cassette fasteners secured before folding. Door opening is an upright service state only.
- `config/current_v32.json` still selects the last promoted combined package and unchanged offline viewer. It separately points to this governing service policy and unpromoted study.

The source is [config/backbox_service_v32.json](../../config/backbox_service_v32.json) and [the parametric builder](../../tools/backbox_service_v32.py). Stored initial module coordinates plus explicitly named insets produce the final layout; the glass coordinates already include its inset. Hardware envelopes are independent packaging reservations, not selected SKUs.

| Dimension/statement | Authority |
| --- | --- |
| WPC axis, 210 mm sides, Y1146 floor | Validated prior study and owner instruction |
| 740 × 450 × 100 display envelope; 120 × 120 × 25 fan family, 105 pitch, approximately Ø116 aperture | Owner requirement |
| Fan frame and mounting pitch | Also confirmed on the [manufacturer's mechanical specification page](https://www.noctua.at/en/products/nf-p12-redux-1300/specifications); reference family only, no product selected |
| Door/frame/carrier/module coordinates and service insets | Explicit design decisions in this study |
| Volumes, distances, motion intersections, retained geometry | Measured from generated OCC B-reps / mathematically derived |
| Payload masses, gasket compression, wire bend limit, mesh free area and hardware reserves | Provisional assumptions, not manufacturing authority |
| Physically measured purchased hardware | **None added in this task** |

No third-party CAD, pictures or manuals were copied. The public specification source is indexed in `library/references/links.txt`; no electrical connector or fan-performance specification was adopted from it.

## Twin rear leaves and fixed structure

Two 351 × 628 × 12 mm plywood leaves close over a 684 × 608 mm fixed-frame aperture. L/R are cabinet X datums, so they appear reversed when viewed from behind. Left is passive; right is active. Each uses a full-height continuous hinge at its outside edge. Provisional hinge axes are X−55/655, Y1324.1; the unmeasured knuckle reserve is R2.5. Fixed 23 × 14 mm hinge cleats provide mounting lands. Final hinge leaf width, offset, screw pitch and opening stop depend on the purchased hinge.

The fixed rear ring is one nominal 18 mm plywood component, with approximately 48 mm outside side borders and roughly 58 mm upper/lower borders. Captured shell joints reduce the inner side web to 30 mm in part of its depth; the wider rear tongue remains. Its existing perimeter interfaces mate to the side/floor/top geometry without wood penetration. Two small integral 30 × 30 mm pads provide real fixed mounting surfaces for cable clamps, rather than suspending those anchors in empty space. They locally intrude 30 mm into the aperture at each side. There is no permanent center post.

The nominal aperture is 81.26% of the clear internal rear rectangle before those two pads, versus the historical 520 × 460 opening. Internal monitor rails still cross the service space; “large aperture” does not mean an empty enclosure. Doors are not monitor supports or structural shear panels. The fixed ring, captured shell and fixed monitor crossmembers remain assembled with both leaves open. Racking stiffness, joint fastening and door-load testing are still required; geometric continuity is not a strength certificate.

Passive-leaf bolts have separate 30 × 60 mm body, engaged and retracted envelopes. The low intakes are offset symmetrically outward to clear these bodies without embedding hardware in the astragal. Nominal throw is 28 mm with 12 mm receiver engagement. Their final receivers/holes are not released. The active leaf has a keyed cam body/barrel and a tongue acting behind the passive astragal. The first layout clipped the astragal at 2–4°; the final body reserve is moved 10 mm away from that meeting line. Selected hardware must supply the required throw and adjustable gasket compression.

The center joint uses a 36 × 12 mm passive-leaf astragal and replaceable center gasket. Perimeter and meeting-line gasket reserves represent 2 mm compressed thickness, not a purchased foam thickness. Use suitable replaceable closed-cell foam/EPDM after compression/warpage trials. Open the active right leaf first, retract both passive bolts, then open the passive left leaf. A passive-only opening against the secured active leaf is not a valid state. Close in reverse order.

The modeled door sweep needs approximately **390.1 mm behind the original rear plane**. Reserve at least 400 mm for geometry; 450 mm is a planning allowance for hands, not an installation standard. A wall is an external installation constraint. No claim is made that a cabinet placed flush against a wall can open its doors.

## Door ventilation and flexible wiring

Each door has the same optional station: Ø116 opening and four 105 mm-pitch reference fasteners, accepting either the 120 mm fan family or a 128 × 128 × 6 blank. No different door CNC is needed for a blank. Exact through-fastener/pilot diameters remain hardware-dependent. The occupied fan envelope is shown without a vendor-specific impeller. Fan replacement is a validated inward withdrawal from an open, attached door; it requires neither monitor nor DMD removal. Common guard/accessory fasteners are accessible on the open leaf.

Selected dust provision is a removable vertical guard and mesh/filter interface. Guard finger-probe performance, mesh openings and filter media remain to be qualified. The shallow downward hood trial is **not installed**: its approximately 134 × 19 outlet is only about 24% of a Ø116 opening. Keeping it would create an obvious restriction. A deeper/louvered accessory could be evaluated later, but is not a required proprietary part.

Each leaf also has a 220 × 80 low passive intake with a removable filter frame and downward internal baffle. Gross area is 35,200 mm² total; a provisional 65% mesh factor gives 22,880 mm². The narrower baffle throats provide **15,840 mm² total**, versus approximately 21,137 mm² for the two fan apertures. Thus the throats, mesh and filters cannot be treated as zero-loss openings. Fine exhaust filters, loaded intake filters, noise, temperatures and a fanless installation all require later thermal evaluation. No flow rate or thermal adequacy is certified.

The low intakes discharge down toward the lower electronics region before the rear display plenum and upper exhaust. The drawing marks this intended route, not CFD. No high intake sits immediately beside a fan. Air can still bypass much of the lower equipment through the rear plenum; two narrow carrier stiles and two crossmembers cause local restrictions. Thermal testing must check this distribution rather than infer performance from aperture area. The generic cable passage is not counted as ventilation.

Each hinge has a **constant-length 160 mm low-voltage loop centerline** within a 3 mm-radius spatial corridor. Fixed anchors use the integral frame pads; moving clamp envelopes reach the door's inner mounting face. Geometry is checked at 59 angles per side, including the initial release, against the enclosure, other leaf and reserved toy volumes. The final screen gives approximately 19.18 mm minimum centerline bend radius and 2.10 mm minimum corridor clearance. Curvature, minimum clearance and length are recorded in `validation.json`. The closed loops also participate in the fold proof. Actual wire stiffness, fatigue, clamp bend relief and minimum dynamic bend radius need the builder's chosen cable. Connector, pin count, disconnect method and harness architecture are deliberately unspecified.

## Front display, adjustable carrier and glass

The maximum display box is **X−70…670, Y1128…1228, Z844…1294** at nominal adjustment. This is a 740 × 450 × 100 envelope for the primary 31.5/32-inch class. There are 2 mm side margins at nominal centering. Full-width centering is limited to ±1 mm; the plate's wider ±15 mm slots are for smaller displays only. Vertical adjustment is ±5 mm. Two positively located depth positions are 16 mm apart.

Two fixed 744 × 18 × 42 plywood crossmembers and side cleats support a removable ladder with two 50 mm-wide stiles. Four captured plywood shoes provide the depth interface. Their 6 mm captures leave 12 mm stock beneath the joint. The replaceable 360 × 230 × 12 VESA plate carries the display-specific pattern; no VESA pattern is cut into permanent walls. Widening this plate preserves 21.75 mm of material beyond the horizontal slot ends. Four captive through-bolts/large-washer reserves positively clamp the plate, with their front termination recessed flush into the replaceable plate to preserve the full display envelope; two ordinary threaded lower stops with locknuts carry its adjusted vertical position. Depth is set by discrete holes, not sliding friction alone. Final screws, nuts/inserts, tightening torque and thread engagement remain unselected.

The load path is display → replaceable plate → carrier/stop structure → fixed crossmembers/cleats → full-strength shell. Through-fastener capture carries normal-to-screen load when folded; no gravity-only hooks or loads on glass, bezel, DMD or speaker panels are intended. All these parts co-rotate in the collision model. The crossmember through-hole reference has only 9 mm nominal front/rear center distance; actual fastener/plywood qualification may require a broader local bearing land. No screw capacity is inferred from the clearance result.

With both doors open, modeled rear driver corridors reach plate clamps and depth attachments while the front glass and replaceable bezel stay in place. Adjust the two lower stops to the new vertical position before tightening the clamps. For front removal, first remove the backglass and bezel, return the display to nominal service alignment, support it, release its carrier clamps and withdraw the display/plate assembly 400 mm forward. This is the certified removal trajectory; arbitrary removal from every extreme adjustment position is not claimed. Side channels do not need removal, and the monitor does not pass through the rear aperture.

Backbox glass is a nominal **752 × 465 × 4 mm** envelope at Y1114…1118, Z840…1305. An 8 mm-wide lined channel is recessed 6 mm into each side, leaving 12 mm continuous outer skin. Its lips stop at the original inner side plane, preserving the 744 mm display throat. A padded lower rail and removable positively fastened top bar capture all four edges. Glass-to-plywood contact is not intended. The top passage splits the former top into a rear top panel and a fixed front rail, both still supported at their ends; the removable cap closes this service slot. It is not an upward-facing ventilation opening.

Remove two top-retainer fasteners and the bar, then lift the glass 500 mm to clear the top. Reserve that overhead service space. The display stays installed. Glass supplier confirmation must set the final 3–4 mm thickness, edge treatment, liner fit, thermal/movement clearances and fastener details. The populated fold retains this glass and its bar.

## Lower cassette, side toys and the promotion blocker

The cassette is one front-removable assembly: nominal 18 mm structural frame, replaceable left/right baffles, replaceable DMD bezel, rear adapter and two simple depth ties. Four positive attachments retain it. The 740 mm assembly has 2 mm side clearance; its provisional Ø4 attachment axes have 9 mm outer edge distance and 11 mm cleat edge distance. The speaker passage has 3 mm side clearance and at least 3 mm vertical clearance, so each baffle and attached speaker can also withdraw independently through the front. No permanent speaker diameter or device-specific DMD hole pattern is imposed on the shell. The baffles are supplied as adaptable blanks; a user speaker and grille require their own removable baffle machining. Display load paths remain independent.

The explicit occupied limits are **400 × 170 × 45 mm for DMD** and **130 × 130 mm for each speaker body, with 85 mm depth behind the structural frame** (103 mm behind the front baffle, including passage through the 18 mm frame), including magnet/body depth. These support suitable FullDMD-class panels and smaller traditional formats through replaceable VESA/non-VESA adapters. They do **not** automatically accommodate the earlier 450 × 230 × 80 reserve or every 15.6-inch display. Rear access is available for the adapter, speaker wiring and service; complete replacement is from the front. A maximum-height DMD is serviced with the complete cassette withdrawn; it is not claimed to pass through the smaller image window. Exact display/speaker geometry, connector orientation and driver approach remain adapter/BOM-stage checks.

The initial full-width front fascia collided late in the fold despite the validated eight-part shell. A scoped front-module inset screen found that 40 mm still clipped a retained playfield channel at 90°; 48 mm cleared the sampled critical poses. **52 mm** was selected for extra geometric margin. The glass/lower support similarly needed more than an 8 mm inset; **16 mm** was selected. Display/carrier moved 10 mm and the replaceable bezel 14 mm to preserve their stack. This did not move the WPC axis, floor or shelf, or reduce side depth.

The resulting cassette overlaps both original R18 × 80 upright-lock tool columns and the first floor-hinge access column on each side. These are real obstructions in the *installed* service state, not false collisions waived by renaming a reserve. Exact intersecting volumes are recorded. Complete cassette withdrawal is continuously clear with the actual cabinet and fixed matrix supports present, and restores the original tool columns. However, it means temporarily releasing the cassette before unlocking the backbox, then securing it again for the fold. Any necessary electrical disconnection is builder-specific. This workflow has not been assumed acceptable on the owner's behalf.

**Promotion: NO.** The decision still needed is whether that additional front-cassette preparation is acceptable, or whether a separate, physically informed lock-access solution is required. This task does not relocate the two positive locking points, invent a low-profile lock/driver to force a pass, or reopen the validated shell. The exact original upward access reserve is preserved in the review and its obstruction is visible in view Z.

Both walls retain visible, clear upper toy volumes of **96 mm inward × 39 mm deep × 326 mm high**, plus lower **48 × 24 × 114 mm** board zones. The maximum display and the complete moving cable corridors are included in their screen. The narrow rear depth is a real limit with the maximum-depth monitor; these volumes are not proof that every chime, bell, beacon, siren or contactor fits. The additional R2 CAD study verifies a concrete future scenario: a 55 mm-deep display and a central 45 mm removable-adapter reserve fit inside the canonical 100 mm occupied envelope. Each upper side volume then grows to **96 × 84 × 326 mm**, including allowance for the 16 mm depth setting. This makes a useful side-mounted chime/toy arrangement a viable later packaging exercise without changing permanent walls; no specific chime or adapter strength is certified. Use removable boards and measure each future device; no permanent toy-specific holes are included.

The optional 490 × 65 × 12 shelf is **rejected at the studied location**, where it intersects the DMD and lower monitor rail and occupies useful airflow/access space. It appears only in a clearly marked diagnostic state. No shelf or its supports are installed in the candidate.

## Validation and its limits

- Build/service checks and independent reopened-CAD regression; all intended parts are valid solids and documents recompute.
- Full reconstructed-wood and populated fold samples: 0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 15, 30, 45, 60, 75 and 90°.
- Continuous OCC separation certificates cover **all added material** over 0–90° and conservative envelopes of the entire allowed monitor-adjustment family. Existing material/subtractions inherit the prior validated fold. Each near pair uses its own moving-part radius and an angular displacement bound; AABBs only reject distant pairs.
- Active-first/passive-second door motion is sampled through 100° and continuously checked for rigid parts. Intentional soft-gasket contact uses a separate planar-release argument plus explicit geometry samples.
- Continuous swept-volume checks cover nominal display extraction, glass lift, cassette withdrawal and each fan's service withdrawal. Playfield 0–50° and 48 mm lift remain clear of the new architecture.
- Current CAD, current offline viewer, playfield hardware, cabinet geometry and fixed systems are independently compared with the previous committed package. No current geometry promotion occurred.

There is intentional zero separation at shelf bearing, assembled wood interfaces and gasket contacts. “Clear fold” means no unintended volume penetration within the reconstructed/reference model; it is not purchased-hardware qualification. Door-loop motion is a sampled flexible-corridor screen, not a cable fatigue certification. The motion certificates do not establish plywood strength, lock security, glass safety certification, fan guarding or thermal performance.

Planning mass is approximately **34.6 kg before optional toys**: about 15.88 kg modeled plywood at an assumed 650 kg/m³, 3.50 kg nominal glass, 7 kg display, 2 kg DMD, 3.2 kg speaker pair and 3 kg accessories/hardware/wiring. This is above the earlier approximate 32 kg planning value. It must feed the next hinge, frame-joint and handling-load qualification; no 32 kg capacity claim is carried forward as a rating.

## Files, rerun and manufacturing status

Generated package: [exports/generated/backbox-service-v32](../../exports/generated/backbox-service-v32). `review-mesh.json.gz` contains the original CAD tessellation data; FreeCAD files are independently inspectable. `validation.json`, `motion-validation.json`, `regression-validation.json`, `details.json` and `artifact-index.json` retain numeric evidence. The gallery links every review image to its associated CAD scene. View S is explicitly a rejected accessory study; exploded views describe assembly groups, not certified simultaneous disassembly paths.

```sh
freecadcmd tools/backbox_service_v32_entry.py
freecadcmd tools/backbox_service_motion_v32.py
freecadcmd tools/backbox_service_details_v32.py
freecadcmd tools/check_backbox_service_v32.py
freecadcmd tools/backbox_service_visual_mesh_v32.py
python3 tools/package_backbox_service_v32.py
uv run --with matplotlib --with numpy python studies/backbox-service-v32/render.py
python3 tools/package_backbox_service_v32.py
python3 tools/check_current_v32.py
```

FreeCAD's exit status alone is insufficient: require the PASS sentinels and passing JSON records. The package script deduplicates review meshes, rounds view coordinates to 0.000001 mm and uses a 0.3 mm absolute / 0.5 rad angular visual tessellation for cable corridors; collision proofs use full B-reps. It excludes diagnostic scratch models and FreeCAD backup files. Source scripts own only their study outputs and can be rerun; the historical reference files are not edited.

**MANUFACTURING BLOCKED.** Required before release: physical 01-9011-L/R, 02-4352 and 4322-01139-12B measurements; the remaining lock-access decision; rear hinge/bolt/cam and gasket measurements; actual monitor/DMD/speaker adapters; matrix physical confirmation; real plywood, fasteners/inserts and glass; joint and door-open frame qualification; loop/clamp trials; thermal/filter trials; CNC supplier profile, cutters, internal-corner/tool strategy, nesting and coupon validation; and the remaining manufacturing freeze gates. No final hinge drilling, cable connector/disconnect system, custom welded frame or custom metal playfield mechanism is released.

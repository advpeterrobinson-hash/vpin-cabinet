# Design simplification / architecture convergence — v28

**Owner hold: ALL physical measurement sessions, including Session 0/1, are PAUSED.** The previous v28 review's permission to start stock sessions is superseded. Do not execute the v27 186-entry checklist or any load test. Architecture acceptance and a revised execution package are required first. [Machine-readable hold](../bom/PHYSICAL_EXECUTION_STATE_V28.json).

Baseline: `f2d18c7b475b7a4b5995e193eb5804cdc6cdab1e`. This package is **DESIGN-PROVISIONAL / NOT ACCEPTED / manufacturing BLOCKED**. Active source/CAD and historical evidence remain unchanged. The proposal deletes mechanisms in a separate CAD document and supersedes their requirements conditionally; it does not claim physical proof or CNC release.

## Thirty-second architecture

**A plywood shell, a PC bolted to one floor base behind an ordinary rear door, three removable rectangular electronics boards on common brackets, and a three-piece plywood display holder on a stock cross-axis.** Two captive tension restraints and a positive opening stop must qualify the holder's service position. No slide drawer, gas assistance, rod/clevis/stow mechanism, custom bearing journals or extra board/carrier layer.

Accept this as a direction for development, not as a safe-to-build mechanism. Two issues specifically prevent structural acceptance: removing the third low shell tie, and replacing the existing pivot/prop system with the stock-axis/strap/stop arrangement. No approved stop contact geometry, hardware rating or physical fixture exists yet.

## Benchmark, without copying

The [Tukkari product page](https://www.tukkari.eu/p/widebody-virtual-pinball-cabinet-vpin-flat-pack-kit) describes prelocated interfaces, flexible shelves, a plywood monitor holder, straps, rear power and conventional fan openings. Its public holder, strap and shelving photographs were reviewed. The useful principles are few understandable assemblies, common interfaces and easy replacement. Its hidden edge connectors use 5-axis machining; we do not adopt them. Its strap arrangement depends on its own holder geometry and secured backbox, so it is not evidence that straps alone make our service position safe.

No proprietary dimensions, hole patterns, panel outlines or manufacturer CAD were copied. No measurements were extracted from photographs. No separate owner-attached photographs were available in this conversation; the reviewed images are the public product photographs. Reference images are local research files under `.work`, not redistributed production content. All proposal geometry is built from our CAD dimensions or identified provisional layout decisions.

## Counts: current → proposed

Counts refer to the proposed architecture, **not changes to the active registers**. [ID-level feature impact](../bom/SIMPLIFICATION_FEATURE_IMPACT_V28.json), [part audit](../bom/SIMPLIFICATION_PART_AUDIT_V28.json) and [count scope/object lists](../bom/SIMPLIFICATION_COUNTS_V28.json) make the arithmetic inspectable.

| Measure | Current | Proposed | Counting rule / uncertainty |
|---|---:|---:|---|
| Fixed permanent plywood pieces | 21 | 20 | Excludes removable moving holder; includes new two pivot cheeks, deletes two CPU rails and CM3 |
| Removable plywood pieces | 16 | 9 | Includes moving holder, its laminations, two doors, PC base and electronics boards; assumes wood for the two current optional-material carriers |
| Structural register records | 29 | 23 | Existing register class includes moving cradle; useful reconciliation, not a claim that cradle is glued into cabinet |
| Structural wood blanks | 32 | 23 | Three existing 36 mm laminated members require an extra 18 mm ply each; proposal eliminates those laminations |
| Doors/base/electronics boards, excluding holder | 5 | 6 | Two doors + one PC board + two → three electronics boards |
| Custom metal planning pieces | 31 | **4 target** | Explicit conservative make-to-project classification; four remaining: two siderails, lockdown bar and receiver. Commodity leg backing and speaker-angle substitutions require fit proof; fallback would be up to 10 custom pieces |
| Commodity bracket/support assemblies | 10 | 18 | Includes four leg brackets and two backbox hinges; deletes four rail angles, adds six shelf brackets, two holder angles, two shaft supports and two speaker angles |
| Moving/service component assemblies | 12 | 6 | Listed assembly scope: folding backbox, holder, props/pins/stow keepers or straps, slide carriages, two doors. Not a count of every joint inside purchased hardware |
| Known fastener families / target | ≥5 | 4 target + supplier exceptions | Wood screw, M4, M6, 3/8-16 retained; dedicated M8 cheek-plate sets disappear. Leg threads and purchased hardware internals unresolved; exact total is **unknown** |
| CNC feature groups | 232 | 201 proposed | 80 old groups superseded, 49 declarations added; new coordinates remain null. These are an architecture inventory, not toolpaths |
| Hardware-controlled CNC groups | 59 | 58 proposed | Includes replacement pivot/strap/bracket dependencies. **Active remains 59**; none cleared by assumed measurements |
| Measurement entries | 186 | 169 proposed | 142 KEEP + 27 NEW; 19 OBSOLETE + 25 REPLACED preserved as history |
| Physical trials | 18 | 18 proposed | 12 KEEP, six old trials replaced by six new trials; safety testing is not reduced merely to improve a count |
| Assembly macro-operations in changed systems | 29 | 20 | Explicit PC/holder/boards/rear-door task lists; excludes unchanged shell/backbox, preparation and individual fastener turns |

Other removable adapters (filter, speaker, exhaust, utility plates) have unresolved wood/aluminum material choices and are excluded from the plywood-piece totals on both sides. Stock channels/tube are cut-stock, not bespoke machined journals; cuts/deburring can be outsourced. Small hardware quantities and full-cabinet fastener count are not complete in the current BOM, so exact before/after screw totals would be invented. The new count file lists assemblies rather than disguising this gap.

## PC and rear door: delete the drawer

**Recommendation: DELETE slides, rail webs, four angle clamps, four backing plates and stowed retainer. SIMPLIFY the existing board into a directly supported, detachable floor base.** The open-frame case is already present in the baseline; no replacement PC case or electronics purchase is implied.

Provisional geometry uses the existing 285 × 460 × nominal-18 board at **X157.5..442.5, Y830..1290, Z36..54**. The existing case envelope sits on it at Z54..182. The physical case's mounting pattern still controls the replaceable board. Secure both case-to-board and board-to-shell against nudging; gravity/friction is not retention. A modest common-bolt interface is preferred. Final fastener stack, head access, bottom bearing and local reinforcement need qualification, not an automatic new rail system.

**CM3 is the conflict:** the current third low crossmember occupies Y1040..1058 and Z36..116, crossing this base. The proposed model removes it. The captured bottom, front/rear panels, CM1 and CM2 remain the shell load path. Removing CM3 and enlarging the opening must pass combined shell torsion/bottom/load review. If proof fails, reconsider base height or relocate a simple tie; do not silently reinstate a slide system. CM3 is not asserted to have existed only for the drawer.

The rear remains an ordinary side-hinged door with a commodity latch, not a linkage. Keep the existing **340 mm opening width and jambs**. The studied enlarged height is **293 mm, Z72..365**, bounded by a two-stock-thickness lower ligament and the existing mains enclosure minus the current planning margin. The door is approximately 364 × 317 using the existing overlap. This is the largest studied vertical opening without relocating utilities, **not a proven global maximum**. Wider cuts reduce already valuable rear leg/jamb material without helping the 285 mm base pass; no reinforcement is added speculatively.

Service: isolate/unplug, open door, disconnect accessible labeled cables, release base fasteners, lift about 38 mm above the sill and withdraw rearward with support. Saved CAD shows a clear path; actual lifting grip, cable reach and handling weight remain untested. The low PC remains ventilated in an open frame; no thermal claim follows from its position. Rear access serves the PC and nearby cable/utility connections, while front electronics remain serviced from above.

Drawer-specific blocked groups removed **in the proposal**:

- HF-013: **CF-0111, CF-0116, CF-0121** — slide interfaces.
- HF-026: **CF-0037, CF-0113, CF-0117, CF-0122** — rail clamps/backing and retainer.
- HF-028: **CF-0118, CF-0123** — rail/leg fit reserve.
- The two rail profiles, engraving and bearing pockets also disappear: **CF-0114/0115/0119/0120/0184/0185**. CM3 profile/engraving and its side capture groups are identified separately in the feature map.

HF-014 case mounting and HF-015/016 ordinary door hardware remain necessary. Deleting the drawer retires its extended 20 kg cantilever proof, not PC restraint, shell strength or safe handling qualification.

## Playfield: minimum candidate mechanism

The reference prompted a new candidate, not a revision of the old props:

1. Two nominal-18 plywood side beams preserving the existing 70 mm beam depth, extended around the existing pivot datum.
2. One nominal-18 plywood bridge carrying the replaceable display interface, replacing three ties plus the separate metal VESA plate. Hardware-specific holes remain on this removable wood piece.
3. One stock cross-axis with plain bushes and commodity shaft supports on two CNC plywood cheeks. **The shown 15 mm cylinder is the old journal-space probe, not a selected tube diameter, wall thickness, material or load rating.** No turning, welding, bespoke journals or bearing cheek plates are intended.
4. Two simple closed landing blocks/pads and positive closed retention.
5. Two captive, suitably rated tension restraints led to the locked backbox, plus a positive over-opening stop integrated into the fixed wood-support concept. No friction-only support, bungee assumption, gas strut or merely balanced service position.

The bridge connects with two ordinary angles from the same bracket family as the shelves: rail and bridge holes are drilled normal to their sheet faces. This avoids precision edge drilling or custom metalwork.

The existing eight cradle wood records (eleven physical blanks) become **three moving wood pieces**. Two fixed cheeks are added; shaped prop/landing unions become plain landing blocks. The present UCFL housings, custom plates/journals/backing, rod/clevis/receiver/keeper/stow assemblies and laminated rear beam disappear from this proposal.

| Comparison | Current | Simplified candidate |
|---|---|---|
| Moving wood | Eight records / eleven blanks + metal VESA plate | Three wood pieces; no separate metal VESA plate |
| Pivot | UCFL pair, two short journals, cheek/backing plates, laminated pivot zones | Stock cross-axis, plain bush pair, two commodity supports, two wood cheeks |
| Open retention | Two custom-integrated prop assemblies with pins, keepers and clips | Two captive straps + positive opening stop; full assembly qualification still required |
| Adjustments | Bearing alignment, journal/plate stack, prop receiver/stow fit, display adapter | Cross-axis alignment, display adapter position, restraint length/stop geometry |
| Holder installation macro-steps | 13 | 7, excluding individual fasteners |
| Hardware evidence | HF-008/009/010: 22 records | Pivot + restraint: 14 new records; no purchased geometry inferred |
| Service | Lift, deploy and positively pin each prop; reverse and clip both to close | Lift while controlled, engage/check both restraints and stop; unload/disengage in controlled order — procedure must be qualified |
| Failure modes | Loose journal/plate bolts, bearing misalignment, rod buckling, pin loss, clip/receiver issues | Shaft/support slip, bush/plywood wear, rail splitting, bridge deflection, strap abrasion/slack/stretch, anchor pullout, stop failure, backbox unlocking |

The CAD routes the straps around the display sides to the wider backbox. Their lines resist closing torque at the existing 70-degree service datum; they **do not prevent over-opening by themselves**. Red stop volumes in the views explicitly mean **contact geometry unresolved**. Backbox locking and restraint anchor loads become part of the service safety path. A simple strap-only substitution at the old lower anchors collided with the display/side/rear geometry and was rejected. The final anchor cannot be a screw driven casually into a panel edge; load distribution and edge distances require a reviewed through-fastened interface.

The new wood holder clears at closed and raised positions, and the proposed boards/PC paths clear. **A broader sampled motion check found inherited display-envelope intersections** with the lockdown reserve at closed position, side-rail reserves during opening, and backbox floor near the raised position. The same intersections occur with the unchanged baseline display envelope; they are not cleared or dismissed here. No additional frame interference was found beyond those inherited display intersections. Resolve whether these are conservative reservation overlap or real collision before accepting service geometry. Ten-degree samples are not a continuous sweep certification. The strap free paths clear; their final anchor contact intersects the intended backbox side. Closed slack, all intermediate strap motion, pinch points, safe deployment and independent full-load capability remain unresolved. Each restraint needs independent full-load qualification with reviewed criteria; no load number, safety factor, fixture or physical pass is invented. Do not work beneath this CAD concept.

The 16.5 kg assumption and previous ~86 N lift estimate are historical context, not acceptance of this changed holder. Re-establish moving mass and controlled lift/descent ergonomics after architecture acceptance. If the stock-axis/strap/stop arrangement cannot meet requirements simply, a purchased positive service stay is the fallback to compare; the old custom mechanism has no presumption of survival.

## One electronics mounting system

Replace, rather than supplement, the two existing carriers and four custom angle stations. The previous proposal's six corbel/seat stations are also discarded. Use **three rectangular boards and one common L-bracket family**, two brackets per board, with ordinary removable bolts/screws. No glue-only mounting or second adapter board is added beneath them.

| Board | Provisional envelope | Functional intent |
|---|---|---|
| A | 316 × 115 × nominal-6; X142..458/Y125..240/Z174..180 | Front controls/interfaces |
| B | 125 × 292 × nominal-6; X50..175/Y348..640/Z174..180 | DC distribution/control/fusing |
| C | 125 × 292 × nominal-6; X425..550/Y348..640/Z174..180 | Supplies/amplifiers/drivers that actually fit |

These previously checked project envelopes are starting volumes, not commitments to those exact boards forever. The side boards avoid the secondary-button envelope. Open space beneath and between them remains available. Mains and protective earth remain in a separately fixed touch-safe enclosure; board removal cannot interrupt required protective bonding inadvertently. Mechanical chimes/contactors need a qualified rigid coupling and support load path; a label assigning them to Board C does not prove a light electronics board suitable. No electronics purchases are needed now.

Support selection:

| Choice | Simplicity / strength / service / cost assessment | Decision |
|---|---|---|
| CNC cleats | Easy sheet fabrication, but elevated side boards require additional stand-offs/corbels; more pieces and joints | Fallback if a common bracket cannot fit |
| Commodity L-brackets | One bought family, six pieces, ordinary tools; load rating and actual hole layout must be checked | **Preferred**; review envelopes contain no fabricated bend/hole drawing |
| Vertical partitions | Simple flat CNC panels and potentially rigid toy supports, but obstruct floor/center access and introduce broad members | Do not add merely to carry light boards |
| Hybrid | Useful locally, but risks recreating carrier + support + adapter layers | Only after a demonstrated local need |

The six bracket volumes are maximum fit probes derived from our mounting gaps, not a claim that a specific catalog bracket matches them. Existing speaker arms and leg backing should also use stock angles/plates where their measured fit and load path permit. Do not buy unverified bracket assortments to rescue geometry.

**Sparse mounting-pattern proposal:** on each side, two longitudinal stations around the side-board ends, with two selectable elevations; use common through-bolts and accessible retained nuts where feasible. Front board mounts to CM1. This is four alternative station locations per side, not a dense pegboard. Final spacing/diameters require the selected bracket, structural edge-distance review and measured stock. Keep positions below SSF zones and out of leg, control and pivot interfaces. Pattern groups are counted as blocked declarations; no bores or guessed bracket patterns are generated. Alternate shelf positions are not automatically collision-free and need their own payload checks.

Each board disconnects independently, lifts through the top with glass removed and the playfield safely secured, then comes forward. Normal driver/Allen access must be demonstrated. A does not fit through the coin door. If top service is unacceptable, reject that placement before physical work rather than creating another hidden release mechanism.

## Explicit redundancy audit

The [part audit](../bom/SIMPLIFICATION_PART_AUDIT_V28.json) covers every active wood record. The [feature map](../bom/SIMPLIFICATION_FEATURE_IMPACT_V28.json) lists every old/new feature group and exact source record.

| Candidate | Classification | Reason |
|---|---|---|
| Two CPU wood rails, slides, four rail angles/backings, retainer | **DELETE** | No moving PC drawer remains |
| Existing CPU board | **SIMPLIFY** | One directly supported removable base still locates and restrains case |
| CM3 | **REQUIRES PROOF → DELETE in proposal** | Conflicts with floor base; shared shell role must be qualified, not dismissed |
| CM1/CM2, captured bottom and shell | **KEEP** | Concrete shell tie/shear and front-board functions remain |
| Rear opening/door | **SIMPLIFY** | Enlarge downward within studied ligaments, ordinary hinges/latch; no added reinforcement yet |
| Eight-part cradle + metal VESA adapter | **MERGE** | Three plywood pieces plus cross-axis replace overlapping frame/adapter functions |
| UCFL bearings, journals, cheek/backing plates, laminated pivot blocks/rear beam | **DELETE / REPLACED** | New stock-axis/plain-bush support concept removes those interfaces |
| Rods, fixed clevises, receivers, upper/lower pins/keepers, stow brackets/clips, nut plates | **DELETE / REPLACED** | No rod mechanism in proposal; replacement restraint/stop safety functions remain |
| Shaped prop/landing unions and metal seats | **SIMPLIFY** | Retain plain wood landing/pad/latch load path only |
| Two old electronics carriers + four custom angles | **DELETE / REPLACED** | Sole three-board system supersedes them |
| Six v28 corbel + seat stations | **DELETE proposal alternative** | Commodity brackets avoid up to twelve new wood support pieces |
| Leg spreader plates | **SIMPLIFY / REQUIRES PROOF** | Prefer commodity backing plates; do not delete concentrated-load spreading |
| Speaker arms | **SIMPLIFY** | Prefer stock angles on removable modules; verify access/load through HF-033 |
| Backbox four-piece rear frame, shelf, hinge pair, upright locks and service door | **KEEP** | Independent load/shear/access functions; restraint concept increases need to qualify locks, not weaken them |
| Siderails/custom-width lockdown/receiver | **KEEP for this pass** | Glass/front-impact function remains; 600 mm width preserved |
| Existing intake/filter and fixed upper exhaust | **KEEP** | Simple routing, structural ribs and independent fan adapters already useful |
| Rear mains, optional simple RJ45 adapter | **KEEP / SIMPLIFY** | Compact, accessible, separate from moving door; no utility bank |

## Rear power, RJ45 and ventilation

**Rear power is preferable now.** It is visible/reachable when servicing the rear door, avoids floor-clearance dependence and avoids an underbody protrusion during transport. The current left rear enclosure and cable reserve clear the proposed PC path. Actual plug bend and wall distance still need physical verification.

| Criterion | Rear | Underside |
|---|---|---|
| Plug/unplug and disconnect access | Visible from service side | Requires reaching beneath/seeing by feel |
| Transport | Rear projection must be protected | Previously reviewed plug probe projects below the base; vulnerable when legs removed |
| Cable bend / routing | Existing rear reserve; short fixed utility path | Real plug/cord bend and floor height unresolved; new internal route |
| Legs / vents / filter | Existing separated placement | Mid-left candidate clears model; floor/service mock-up still required |
| Water/debris | Exposure still needs suitable enclosure/cap/entry | Floor-facing location is not inherently sealed or safer |
| CNC / structure | Existing rear interface | New structural-bottom penetration and old rear interface closure/omission |
| Aesthetics | Visible behind cabinet | Less visible but no demonstrated service advantage |

Keep final mains cutout and enclosure anchors blocked. No new electrical safety approval is issued. One grounded feed, strain relief, protected distribution, fixed touch-safe mains and reviewed bonding remain required.

RJ45: external ordinary RJ45 → compact female/female panel coupler → ordinary internal patch lead. Prefer rear placement. Mount directly only if sample grip fits the actual panel; otherwise retain the existing small flat adapter, not a custom bracket. Cap/seal/latch and cable-bend evidence remain necessary. No proprietary harness or automatic BUY NOW expansion. HF-018's keystone/clip wording is replaced in the proposed ledger by the bulkhead-specific fields.

Ventilation: the existing 18 rounded 80 × 12 slots provide approximately **16,724 mm² geometric open area** before mesh. They preserve eighteen-millimeter webs and the established perimeter ligament. One removable flat filter frame uses the existing four mount locations. It is not a complicated moving mechanism. Keep it with simple replaceable mesh/filter media; use ordinary removable fasteners.

The comparison model fills those slots and shows two **generic 100 mm circular apertures** within the same service region, approximately 15,708 mm² before guards. These are design-comparison openings, not copied fan dimensions or release geometry. They reduce cut groups but create larger unsupported holes and need filter/fan adapter decisions. A single large passive opening has the same shear/debris/guard problem. A standard fan family may be useful later on an adapter; it does not establish adequate flow or justify weakening the bottom now. No thermal requirement is relaxed and no airflow adequacy is inferred from area. **Retain slots/filter until a real cost or service problem justifies change.** No SSF through-holes or structural-bottom subwoofer cut is added.

## Evidence and acquisition impact

[Every measurement and all trials](SIMPLIFICATION_EVIDENCE_IMPACT_V28.md) have explicit KEEP/OBSOLETE/REPLACED/NEW dispositions, with the [proposed ledger](../bom/PHYSICAL_VALIDATION_RESULTS_V28_PROPOSED.json) preserving original records and null results. Classification does not erase history or authorize execution.

- **Unnecessary if accepted:** all nine HF-013 slide records, six HF-026 clamp/backing/retainer records and four HF-028 rail-gap records — **19 records**. Leg bracket geometry remains required under HF-004; the duplicate rail-specific task disappears.
- **Replaced:** eight HF-008 bearing, seven HF-009 journal/plate, seven HF-010 prop, three HF-018 coupler/clip records — **25 records**. Their replacement requirements are seven pivot, seven restraint, five common-bracket and eight RJ45 records — **27 new**. Counts are explicit fields, not a claim that every field takes equal bench effort.
- **Trials:** old left/right prop proof, prop motion, two-carrier servicing, extended CPU servicing/proof and general old structural fixture are superseded by left/right restraint proof, new holder motion, three-board servicing, fixed-base PC handling/restraint and changed-structure qualification. The extended-slide proof and rod/keeper/stow tests cease to apply; equivalent safety functions are tested under the new architecture. Mass, ergonomics, thermal, electrical, material/coupon and manufacturing-package checks remain.

Proposed new commodity needs: stock cross-axis, matched plain bushes/supports, two rated captive service restraints with common anchors, eight matching L-brackets (six shelf, two holder), stock speaker angles and leg backing where suitable. These are **selection needs, not approved purchases or dimensions**. Existing case, legs, door hardware, controls, mains sample and sheet stock remain relevant. Defer slides, UCFL/journal hardware, bespoke props and drawer-specific clamps while the owner considers this proposal. No acquisition state in v27 is silently rewritten.

## Decision and proof boundary

Owner decisions needed:

1. Adopt floor PC base and rear lift-out instead of the drawer, accepting loss of pull-out servicing?
2. Authorize the two-tie shell / enlarged rear-opening proposal for structural evaluation, with a simple fallback if proof fails?
3. Adopt the three-piece holder / stock-axis / captive restraints / positive-stop direction, accepting dependence on locked backbox and the need to resolve the stop and anchor load paths?
4. Select the sole three-board system and common brackets, including top access rather than coin-door extraction?
5. Keep rear mains and slots/filter, and select the ordinary RJ45 sample family later?
6. Accept the proposed evidence dispositions, then authorize a revised bench workflow? Until then **all sessions remain paused**.

CNC freeze conditions remain intact: measured stock/hardware, tool/coupon fit, resolved structural joints and load evidence, service/ergonomic evidence, nesting/orientation and owner manufacturing approval. No mechanism is kept because of previous investment; no replacement is called safe because it is simpler.

## Engineering views and validation

[18-view gallery](../exports/generated/simplification-v28/review/index.html) · [separate provisional CAD](../exports/generated/simplification-v28/vpin-simplification-v28.FCStd) · [geometry/check report](../exports/generated/simplification-v28/geometry.json).

01 current interior; 02 simplified interior; 03 current/proposed exploded; 04 holder; 05 service position; 06 rear door; 07 PC location; 08 PC removal; 09–11 boards A/B/C; 12 board removal; 13 cable corridors; 14 power comparison; 15 RJ45; 16 vents comparison; 17 proposed floor map; 18 removed-parts map. All images are saved CAD meshes, with no AI concept art. Red stop volumes remain unresolved; comparison ghosts are not production objects.

Rebuild using `bash tools/run_simplification_v28.sh` after the baseline active CAD and preceding v28 review exist. Generated CAD/images remain ignored artifacts. The proposal validator checks ID coverage, untouched v27 evidence, paused/null results, feature arithmetic, retained baseline source hashes, actual CAD paths and negative controls. `make validate` continues to validate the historical active design; passing it does not approve this proposal. No physical tests have been run.

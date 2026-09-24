# Owner design change review — v28

**Review baseline:** `7a9d408de3b8bc8a9aaa311a40a3f98211fe7af5`. **Manufacturing remains BLOCKED.** This is an owner decision package, not an implementation approval or new machining definition. Current active geometry, the 186 measurements, 18 trials, acquisition states, 59 blocked CNC groups and CNC freeze criteria are unchanged. The owner's working master and its pre-existing deletion are untouched.

## Decisions before bench execution

1. **Power:** keep the rear inlet, or authorize investigation of the mid-left underside zone below? Recommend retaining the rear baseline until the underside plug/leg/handling mock-up passes. There is a viable packaging candidate, not yet a proven installation.
2. **Ethernet:** retain the small rear replaceable adapter and investigate a generic capped female-to-female RJ45 bulkhead coupler? Recommended. Separately approve obtaining one sample early if desired; it is **not added to BUY NOW** here.
3. **Boards:** accept three provisional elevated boards, including top removal with glass removed and both playfield props pinned? Recommend this layout for physical mock-up, with the shortened side boards described below.
4. **Supports:** accept CNC plywood corbel/seat-strip development using common bolts/nuts, with no new metal brackets as the starting point? Recommended, subject to fastening-stack, load and access review.

Session 0 tools/labels and Session 1 stock measurements can proceed without these choices: neither depends on connector placement or board layout. Settle the four choices **before building affected installation fixtures or executing the installed controls, carriers, electrical or airflow trials**. Do not use the v27 two-carrier worksheet to accept a three-board installation. After decisions, revise the relevant ledger descriptions and regenerate the owner queue in a separate controlled change; do not overwrite existing IDs or treat this review as measured evidence.

## Evidence and limits

The review builder opens `cad/active/vpin-active.FCStd`, checks existing shapes remain unchanged, saves a separate review FCStd, reopens it, checks valid solids and tessellates those saved shapes. The source hash and exact intersection results are in `review-analysis.json`. Original master CAD is not an input or output. No image-generation tool, vendor photograph tracing or imported concept cabinet is used.

All added shapes are **DESIGN_PROVISIONAL volumes**: boards, support stations, payloads, cable/removal reservations and connector candidate zones. They have no manufacturing patterns or cuts. Coordinates below are CAD packaging values in mm: X left-to-right, Y front-to-rear, Z upward. They are not physically measured dimensions. Nominal stock remains subject to HF-001/002.

Collision checks use saved B-rep intersections, including current controls, SSF, legs, CPU, closed cradle and the playfield cable reserve. Removal checks substitute the saved raised cradle and both deployed props, omit the removable glass, and retain the other proposed boards. A zero intersection does **not** demonstrate hand access, cable flexibility, strength, safe installation or dimensional tolerance. External floor height is not authoritative in the current model.

Sources: [physical plan](PHYSICAL_VALIDATION_PLAN_V27.md), [worksheet](PHYSICAL_RESULTS_WORKSHEET_V27.md), [ledger](../bom/PHYSICAL_VALIDATION_RESULTS_V27.json), [freeze gate](CNC_FREEZE_GATE_V27.md), [measurement pack](HARDWARE_MEASUREMENT_PACK_V25.md), [owner review](OWNER_REVIEW_V27.md), [owner validation](OWNER_VALIDATION_V27.md), current active configs/builders and saved CAD. The owner's specific RJ45 URL was absent from the message; this review evaluates the stated connector family only.

## Decision matrix

| Item / recommended status | Current → proposal / reason | CAD conflicts | Manufacturing impact | Serviceability / sourcing | Required measurements | Reversible / affects blockers |
|---|---|---|---|---|---|---|
| POWER INLET — **REQUIRES OWNER DECISION** | Rear enclosed mains interface → investigate underside mid-left to reduce rear cable projection | Preferred planning probe clear; front alternative clashes with proposed front support and lid access; center obstructs aisle | If accepted, relocate HF-017/027 interface and CF-0033/0034 to bottom, review local strength and omit/blank rear interface as appropriate; no change now | Underbody plugging less visible/reachable; needs transport protection and physical clearance. Same authorized mains assembly sample, orientation may affect selection | Complete inlet/enclosure/plug stack, cord bend, strain relief, lid/tool sweep, floor/leg height, reach and handling tests | YES while provisional; machining irreversible / YES |
| RJ45 — **REQUIRES PHYSICAL SAMPLE** | Optional rear 40 × 40 adapter → generic capped RJ45 bulkhead coupler in replaceable adapter | Side internal reserve intersects moving playfield harness; bottom unverified exposure/access | Sample-defined adapter hole only if it fits existing generic opening; permanent changes require separate review | Ordinary patch leads both ends; cap and latch access must work. Generic family preferred; actual interchangeability not established | Body/flange/nut, thread/grip, flats, panel range, cap/tether, boots/latches, both cable bends, sealing condition | YES with replaceable adapter / NO existing permanent group if adapter fits; otherwise reassess |
| ELECTRONICS SHELVES — **PROVISIONAL CHANGE** | Two elevated 125 × 355 carriers at Z125 → three smaller independent boards at Z174 | Original-depth raised payload hit secondary buttons; shortened side candidates and removal sweeps clear current model | No active wood/register change. Three replaceable board outlines plus support development if approved; no electronics-specific permanent holes | Top removal, separate cable disconnects; central floor access retained. Common sheet material; electronics purchases unnecessary | Stock, payload/connector envelopes and mass, wrench/hand access, removal with cabling, fastening stack and support qualification | YES before implementation / YES: affected installation validation and load review |
| SHELF SUPPORT — **PROVISIONAL CHANGE** | Four carrier angle stations → six CNC wood support stations | Modeled stations clear fixed objects; front station conflicts with front underside inlet | Corbels plus seat strips, measured-stock locating joints and common fasteners; no final support profiles/holes yet | Common bolts/nuts, no custom metal target. Shared CM1 interface needs access/stack review | Material/coupon, common bolt/nut/washer stack, tool approach, load criteria and physical support tests | YES if bolted / YES: fastening/load evidence remains required |

## Power inlet: location review

Current rear carrier: **X50..140, Y1308.1..1311.1, Z395..465**. Current generic wood aperture is 70 × 50, and the touch-safe enclosure reservation is **X45..155, Y1170.1..1290.1, Z385..475**. These are current provisional packaging, not the selected inlet's measured cutout.

| Candidate | CAD zone / findings | Recommendation |
|---|---|---|
| Mid-left underside | Bottom zone **X50..170, Y688..805, Z18..36** (120 × 117). After CM2 ends Y668; before CPU rail begins Y825. Outside central aisle X190..410 and filter X190..410/Y305..595. Away from leg corner reserves and CPU backing. Rotated current enclosure reserve occupies X50..160/Y688..778/Z36..156; lid probe to Z246 clears proposed boards | Best underside investigation candidate; **not a cutout** |
| Front underside | X133..467/Y133..240. Clear baseline bottom structure/legs, but rotated enclosure probe intersects front-left proposed corbel station, and lid path intersects front board/payload | Do not combine with recommended front-board layout without further design review |
| Center after CM2 | X190..410/Y688..805 | Reject: enclosure enters central service reserve |
| Rear/CPU zone | Rails from Y825, backing at front/rear rail clamps, low hatch/extended drawer and rear legs | Avoid new inlet in these load/service zones |

The mid-left zone preserves the **modeled** ventilation/filter and major structural members. Cutting even a small bottom aperture needs later ligament/shear and fastener-edge review after actual dimensions; geometric separation is not structural qualification. No filter removal path is newly proven here.

Potential benefits: less rear plug projection, separation from the CPU hatch, and a short route to an independently fixed enclosed mains assembly. Disadvantages: underside reach/visibility, floor-facing sockets, cord snagging, external projection during handling, and possible new guard/recess complexity. The reused 90 mm plug-depth probe reaches **Z−72**, below the cabinet base; putting the cabinet down without legs could damage an exposed assembly. This is a reason to test the concept, not a clearance specification.

Still required: installed floor-to-bottom clearance across actual leveler adjustment; real plug projection and insertion/removal sweep; cable bend/strain-relief space; approach with the cabinet against its intended wall; unplugging without lifting the cabinet; transport/storage contact points; enclosure lid and disconnect access; exposure to cleaning liquid, spills, dust and debris. An underside orientation does not itself supply ingress protection.

Keep one grounded external feed, a fixed touch-safe enclosure, protected distribution and strain relief. Protective-earth distribution must not depend on a removable plywood board or incidental bracket contact. Moving the inlet changes cable routing, restraint, accessible metal/bonding review and servicing; it does not remove those requirements. No wiring plan or electrical commissioning approval is issued here.

## RJ45: simplify without losing replaceability

The current solution already uses **one small 40 × 40 × 3 rear adapter** over a generic 24 × 24 opening, at X510..550/Y1308.1..1311.1/Z405..445. It is not a large bracket assembly. A bulkhead coupler can simplify connector retention, but **no substantial bracket reduction is demonstrated**. Retain the replaceable adapter so a future connector does not force permanent wood modification. Direct mounting into nominal 18 mm plywood is not assumed compatible with the sample's threaded grip.

The preferred concept is ordinary RJ45 female connections on both sides, compact panel mounting, common patch cables, a protective cap and replaceable supply. Verify whether a standard external patch plug works with the claimed seal: some sealed connector families specify protection only when properly mated or capped. This general caveat is illustrated by [Amphenol's connector FAQ](https://www.amphenol-socapex.com/faq/faq_product/218/faq_product_range/213); it is not a specification or recommendation for the owner's sample. No price, availability or IP65 performance is validated here.

Placement comparison:

- **Rear adapter: preferred.** Existing inside reserve X505..555/Y1230.1..1290.1/Z395..455, outside to Y1391.1. Test boot, latch-finger, tether and cable bend access with CPU door and backbox service conditions.
- **Right side near rear: reject the reviewed candidate.** Candidate Y1135.1..1175.1/Z405..445 and rotated inside reserve intersect `MovingHarnessKeepoutV18`. This is a real playfield cable reservation, not an obsolete CPU harness ghost. Side plugs also project into carrying/walking space.
- **Underside: lower priority.** Candidate X425..465/Y688..728 uses the existing adapter-size reserve, not a connector cutout. Internal boot, external plug/floor/handling and debris protection remain unmeasured; awkward network servicing gains little over the rear adapter.

Sample worksheet additions **to propose after approval**: threaded major diameter/flats and anti-rotation shape; required aperture; usable thread/panel clamping range; flange/gasket/nut/washer stack; internal body depth; external projection; cap diameter/open sweep/tether; ordinary plug boots and latch access on both sides; cable bend requirement from the actual cable; mounting orientation and capped/mated sealing instructions. Catalogue drawings may be reference only. HF-018 remains optional/adapter-only; an early sample is a proposed acquisition change, not an order or broadened BUY NOW list.

## Three elevated removable boards

The current carriers already stand above the floor: bottom top Z36, board underside Z125, giving 89 mm below-board clearance. The proposed board undersides are **Z174**, giving 138 mm below-board clearance. This is a modest elevation, not a cabinet-spanning shelf.

| Board | Board envelope X/Y/Z | Approximate board size | Usable payload reservation | Suggested function, conditional on physical fit |
|---|---|---|---|---|
| F — front | X142..458 / Y125..240 / Z174..180 | 316 × 115 × 6 | 306 × 85 × 110; Z180..290 | Small control interfaces / front-service electronics |
| G — left | X50..175 / Y348..640 / Z174..180 | 125 × 292 × 6 | 115 × 262 × 110; Z180..290 | DC/control distribution, low-voltage terminals/fusing; fixed mains/earth enclosure separate |
| P — right | X425..550 / Y348..640 / Z174..180 | 125 × 292 × 6 | 115 × 262 × 110; Z180..290 | Enclosed supplies, drivers/controllers or amplifiers that physically fit |

Derivation: use existing carrier thickness/insets/payload height; place board top 20 mm below the current front SSF lower Z. Front outline comes from existing inner CM1 bolt centers ± nominal stock and the coin-door/CM1 gap minus existing 20 mm planning margin. Side leading edge is the current secondary-button body rear limit plus that margin, rounded upward to the next mm. **These are explicit provisional layout decisions, not inferred hardware measurements.**

Initially lifting the full 355 mm side carriers produced payload and extraction conflicts with both secondary-button envelopes. Shortening to 292 mm avoids those modeled conflicts. The remaining area is small: do not assume a particular PSU or contactor fits. Large/heavy feedback devices and exciters should retain independent rigid shell load paths, not be assigned to these light service boards merely by functional label. No support load capacity is claimed from CAD or the old carrier planning payload.

All three proposed board/payload volumes clear current closed cradle, controls/plunger, SSF, CPU and central reserve. Four SSF solid-plywood zones remain unchanged. Low crossmembers and rear backbox shelf remain structural; none is removed. CPU service continues rearward, separate from forward board extraction. Backbox/monitor service geometry is unchanged; representative cabling can still invalidate accessibility and must be tested.

Removal: disconnect and label wiring; remove glass under the existing service procedure; raise and positively secure both props; release accessible board screws; lift above the shell, then translate toward the front. Other boards stay installed. The front board is wider than the coin-door opening and **does not exit through it**. The CAD sweep clears without removing CPU/backbox/display assemblies, but reach, screw access and controlled handling need physical trial. If glass removal for board service is unacceptable to the owner, do not accept this layout as satisfying the service requirement.

Cable reservations occupy Z131..174 below each board, using existing inset footprints. They are 43 mm planning spaces, not validated cable-bend minima. Put disconnects and slack where reachable before lifting. Do not route one board's captive harness across another's removal path. Central reserve remains X190..410/Y300..810/Z116..276; no broad bridge board is proposed. A spanning board was explicitly tested and rejected for occupying that reserve.

## Support comparison and buildability

| Approach | Advantages | Limits / recommendation |
|---|---|---|
| A — commercial L-brackets | Common hardware, compact, replaceable | Actual hole/slot pattern and stand-off depend on selected sample; can add purchases and awkward wrench access. Fallback only if wood support cannot meet clearance/load needs |
| B — CNC plywood cleats/corbels and seat strips | CNC does fabrication; simple locating faces; common bolts; easy replacement | More small wood pieces, local bending/load and bolt-edge checks required. Preferred basis |
| C — tab/slot location plus screws | Repeatable dry-fit, minimal bench layout | Fit depends on measured stock/tool/coupon. Avoid thin tabs and repeated screws into vulnerable edges; not a final joint here |
| D — wood location plus minimal metal | Useful if a measured local condition requires reinforcement | Adds sample-dependent pattern and hardware; reserve as a justified fallback, not default |

Recommend B+C: CNC-cut corbels with simple locating seats/strips, common through-bolts with retained accessible hex nuts, and independently removable board screws/bolts. Avoid repeated removal screws relying on plywood edge grip. Slotted replacement-board holes or a generic removable-board grid can accommodate future electronics; permanent wood must not inherit individual device patterns. No exotic fastening system is needed at this review stage.

Six support **stations** are modeled: two per board. A likely construction is up to six corbels plus six seat strips, not yet twelve released parts. Side-front stations extend from CM1 to the shortened boards; final shape, grain direction, bolt lever arm and load test remain unresolved. Front and side supports may share existing CM1 attachment stations on opposite faces; check the combined bolt/nut/washer stack, wood bearing and tool access before claiming those existing eight generic crossmember holes are reusable. Board removal must not require loosening a shared support bolt.

For the **proposed board support system only**: **0 custom metal parts, 0 commodity L-brackets targeted**; common screws/bolts/nuts/washers remain required and uncounted until joint detailing. The current four metal angle carriers remain in active CAD until a change is accepted. This does not eliminate the cabinet's leg, hinge, CPU, prop or mains hardware.

## Controlled impact report — do not edit the ledger yet

| Existing authority / work | Impact if accepted | Current disposition |
|---|---|---|
| HF-017 M01..M07; HF-027 measurements; CF-0033/0034 | Actual sample dimensions remain useful; change rear installation datum/context to bottom, add floor/plug/handling and enclosure access evidence. Reassign permanent part/face only after approval | Both blocked feature groups stay open; no coordinates or ledger changes |
| HF-018 M01..M03 | Aperture remains relevant; clip-retention language may be superseded by threaded nut/gasket retention. Add sample fields listed above; no automatic deletion of IDs | Optional adapter sample proposal only; no permanent CNC blocker removed |
| HF-020 / HF-030; PV-CONTROLS-SSF / PV-PLUNGER | Raw button/plunger dimensions remain necessary; installed hand/cable clearances need the accepted board layout | All existing measurements and bores remain blocked |
| SV-01 / SV-02 | Two-carrier description becomes three-board removal, disconnect, floor and center-path checks; support construction/load evidence must be revised | v27 trial descriptions retained until owner decision |
| PV-PROP-MOTION; SV-03; PV-ELECTRICAL; PV-AIRFLOW | Recheck access with changed board/mains installation; representative cables must not obstruct prop, CPU or filter service | No trial passed; no proof/load criteria invented |
| PV-PROP-L/R; PV-MASS; PV-ERGONOMICS; SV-04/05 | Existing physical evidence remains mandatory; do not infer acceptance from board collision checks | Unchanged and open |
| Active parts / generic attachment features | Three proposed adapters and new support pieces may replace current two carriers/four angles; inspect affected crossmember attachments and load paths before register update | 29 permanent structural wood records unchanged; all current registers unchanged |

**No existing collected measurement becomes obsolete: none has been populated.** Some installation descriptions, especially HF-018 clip retention and SV-01 two-carrier scope, would require revision if the proposals are selected. The **186-record ledger requires a targeted revision after owner decisions**, not an arbitrary reduction or pre-emptive rewrite. The 18 trials, 55-operation owner queue and acquisition workflow remain intact now. Added fields/trials and their exact counts should be reconciled in that later change; no provisional count is claimed here.

BUY NOW remains the existing authorized list in the measurement pack; HF-030 remains its only newly authorized addition. No electronics, brackets, fan or network connector is promoted here. Owner reconsideration is needed only for an **early optional HF-018 physical sample** and confirmation that the chosen HF-017/027 assembly can serve the preferred orientation.

## Review outputs and reproduction

Open [CAD gallery A–L](../exports/generated/owner-change-v28/review/index.html) and the separate [review FCStd](../exports/generated/owner-change-v28/vpin-owner-change-v28.FCStd). Generated outputs are ignored by Git and rebuilt by `bash tools/run_owner_change_v28.sh`; `make validate` runs the established Python suite separately. The review generator requires an existing verified current active CAD file, and refuses to claim success without saved-geometry validation.

| View | Inspect |
|---|---|
| [A](../exports/generated/owner-change-v28/review/A.png) | Current complete interior, with inspection omissions called out |
| [B](../exports/generated/owner-change-v28/review/B.png) | Actual floor, slots, filter, ties, rail/backing and utility context |
| [C](../exports/generated/owner-change-v28/review/C.png) | Underside power zones, not cutouts |
| [D](../exports/generated/owner-change-v28/review/D.png) | Rear/side/bottom RJ45 candidates and harness |
| [E](../exports/generated/owner-change-v28/review/E.png) | Available payload volumes and current controls/SSF/CPU |
| [F](../exports/generated/owner-change-v28/review/F.png) | Three boards and six provisional wood support stations |
| [G](../exports/generated/owner-change-v28/review/G.png) | Front board top removal and coin-door relationship |
| [H](../exports/generated/owner-change-v28/review/H.png) | Left distribution board service |
| [I](../exports/generated/owner-change-v28/review/I.png) | Right PSU/controller board service |
| [J](../exports/generated/owner-change-v28/review/J.png) | Independent removal with raised playfield and both props |
| [K](../exports/generated/owner-change-v28/review/K.png) | Cable loops, center and CPU service paths |
| [L](../exports/generated/owner-change-v28/review/L.png) | Rejected combinations and actual CAD conflicts |

Validation: established Python suite including negative controls; current active saved-geometry check; separate FreeCAD review save/reopen/solid validity; source SHA preservation; three board/payload/central/removal intersection checks; support checks; six intentionally colliding negative candidates; byte comparison of protected authority files; whitespace/local-link checks. Counts remain **232 CNC groups = 173 defined + 59 hardware-blocked**. No final holes, bores, production geometry or manufacturing release is generated. The [CNC freeze gate](CNC_FREEZE_GATE_V27.md) remains unchanged.

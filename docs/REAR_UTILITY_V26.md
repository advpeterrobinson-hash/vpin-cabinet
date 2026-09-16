# Rear utility simplification — v26 owner review

Status: both candidate layouts pass modeled collision checks. **Placement is not selected.** The active rear and bottom panels have no utility cuts. This is the owner-requested visual gate, not a CNC approval gate.

## Functions that remain

One fixed AC mains/master disconnect interface, and optional wired Ethernet. SERVICE HDMI, USB-A, USB-C and RESERVE disappear from the permanent rear panel. Troubleshooting ports are reached on the extended PC. PC POWER, RESET and DOF SERVICE controls remain at the coin door and are not duplicated at the rear.

The current Ethernet study uses a small replaceable RJ45 carrier, blanked if no wired connection is wanted. Alternatives:

| Interface | Benefit | Cost / unresolved input |
|---|---|---|
| Small panel-mount RJ45 on 40 × 40 carrier | Cable disconnects externally; coupler replaceable; no decorative wood | Generic 24 × 24 cabinet opening reserved; actual coupler, latch access and carrier holes unmeasured |
| Strain-relieved network cable entry | Potentially one smaller round cut; no coupler | Cable becomes tethered; passing the terminated plug or using a split gland requires measured hardware; replacement/disconnection less convenient |
| Direct panel-mount RJ45 without carrier | One less fabricated carrier | Permanent wood becomes connector-specific; replacement may require cabinet modification |

Recommend the small optional replaceable carrier. The candidate rectangular opening is a **design reservation**, not a purchased connector footprint. A measured gland could reduce cut area further, but does not justify relocating or weakening structural wood.

## Actual available rectangles

X is cabinet left-to-right, Y front-to-rear and Z vertical. Rear-view left is high X.

The maximal empty mounting rectangles are enumerated from saved solid bounds, with 20 mm bottom-joint/edge reserve, 15 mm around the rear leg bracket bounding envelopes, 20 mm around the closed CPU door and 10 mm beside the CPU support rails. These margins are explicit engineering reservations, not electrical clearance standards. The full 3D enclosures, plugs and moving PC are checked separately.

| Plane | Clear rectangle | Size |
|---|---|---|
| Rear, above door | X38..562 / Z382..558.9 | **524 × 176.9 mm** |
| Rear, beside door | X38..98 or X502..562 / Z183..558.9 | 60 × 375.9 mm each |
| Rear, below door | X128..472 / Z56..78 | Only **344 × 22 mm**; reject the old 55 mm windows |
| Underside, between support rails | X154.8..445.2 / Y1078..1270.1 | **290.4 × 192.1 mm** |

The CPU aperture remains X130..470 / Z110..350, door bottom Z98 and shelf bottom Z135. No utility solution moves the CPU upward.

## Comparison

| Criterion | A — two rear-face carriers above CPU door | B — compact underside interfaces near rear |
|---|---|---|
| Mains carrier | 90 × 70 × 3 mm, X50..140 / Z395..465 | 90 × 70 × 3 mm, X170..260 / Y1160..1230 |
| Network carrier | 40 × 40 × 3 mm, X510..550 / Z405..445 | 40 × 40 × 3 mm, X380..420 / Y1180..1220 |
| Cabinet apertures, if selected | 70 × 50 plus 24 × 24 mm through rear panel | Same areas through bottom panel |
| Structural wood removed, candidate | 4,076 mm² / 73,368 mm³ at 18 mm | Same amount, from bottom rather than rear |
| Current active wood removed | **0 utility material** | **0 utility material** |
| Parts / contour cuts | 2 metal carriers / 2 generic contours | 2 metal carriers / 2 generic contours |
| Mains–signal carrier separation | 370 mm | 120 mm |
| Enclosure–signal internal access separation | 350 mm | 105 mm |
| Independent mains enclosure reserve | 110 X × 120 Y × 90 Z mm above PC | 110 X × 120 Y × 80 Z mm below PC; 19 mm below shelf |
| Access | Visible and reachable from rear without opening a door | Requires reaching under rear; plug/floor clearance must be measured |
| Exterior | Two small visible interfaces above door | Rear face stays clear |
| Replacement | Small removable carriers; generic wood apertures | Same principle, less convenient underside access |

Both remove approximately **80.8% less wood area** than the obsolete 150 × 55 and 235 × 55 windows (21,175 mm²). Counts exclude hardware-specific mounting holes because inventing them would misrepresent CNC readiness. Final enclosure flange/gasket size and fasteners can change the envelope.

**Engineering preference: A**, for visible cable access, easier inspection and larger spatial separation. B is also geometrically viable and gives the cleaner rear face. Since the remaining tradeoff is user-facing, stop at these comparison models for owner selection, as requested. Candidate groups are review-only and must not be exported as active production panels.

## Mains safety boundaries

The removable interface is not the safety enclosure. All hazardous terminals and any mains splice belong inside an independent touch-safe, tool-access enclosure fixed to the permanent cabinet. Neither interface nor enclosure attaches to the CPU door or moving shelf. Maintain a dedicated protective-earth path and bond exposed conductive mains parts as required by the eventual electrical design. Verify earth continuity and entry strain relief during commissioning; no conductor termination carries cable pull.

No component/rating, fuse, conductor size, terminal spacing, connector hole or wiring schematic is released here. Measure the actual inlet/disconnect or captive-cord assembly, enclosure and glands. Model plug insertion/removal, insulated cable exit and access before freezing the carrier. For B also prove floor clearance and cable routing on the actual classic legs; the study reserves space to Z−74 relative to cabinet bottom datum.

## CPU support load path

The previous 25 × 55 mm rails floated above the bottom. They are replaced by **two 18 × 465 × 135.5 mm** plywood rail blanks, Z36..171.5, at X126.8..144.8 and X455.2..473.2. Slide contact faces remain unchanged, so the board and case do not move.

Each rail has a CNC saddle over the existing rear low crossmember: nominal 18.4 mm along Y and 80.2 mm upward from the rail bottom, retaining 55.3 mm rail depth above the saddle. The crossmember itself is not notched. Groove fit and tool relief remain measured-stock/coupon work.

Each rail seats on the bottom and has two identical local 3 mm angle-clamp envelopes (30 mm foot, 60 mm upright, 50 mm length), at Y875 and Y1150. Four underside 40 × 60 × 3 mm backing plates reserve through-bolt load spreading. Load path:

`PC → board → slide pair → rail web → bottom bearing + bolted angle clamps → backed bottom → captured shell / low ties → leg brackets → legs`

The extended shelf creates uplift at the forward anchors. A simplified symmetric two-anchor calculation with 20 kg payload plus estimated 1.534 kg board, CG at Y1510, gives approximately **138 N upward per front rail anchor** and **244 N downward per rear rail anchor**. This is an illustrative anchor-design input for a centered payload and the chosen two-support idealization, not a strength certificate; real continuous bottom contact changes reaction distribution. Side loads, vibration, bolt bearing, tear-out, rail deflection, brackets and bottom-panel strength still require calculation and physical proof testing. Friction, glue alone and screws in plywood edges are not accepted as the positive uplift connection.

The rail faces clear the modeled rear leg brackets by 13.8 mm, but enter the additional conservative 15 mm planning reserve by 1.2 mm at the rear. This is a **measurement/release limit**, not an actual modeled steel collision. Confirm the real bracket/bolt stack before freezing the rail profile; the utility cuts and angle clamps themselves stay outside the full reserve. Do not trim the bracket load path to recover this margin.

Do not finalize slide or clamp hole patterns before physical hardware measurement. The eventual CNC release locates all holes; the home builder does not transfer-drill or establish slide alignment by hand.

## Wooden-part review

`bom/ACTIVE_PARTS.csv` provides PART ID, CURRENT FUNCTION, LOAD PATH, KEEP/COMBINE/REMOVE/METAL/ADAPTER disposition and rationale for every active wooden solid. Current active count is **36 versus 40** on the same CAD-object basis. Three 36 mm laminated members still require individual lamination release records; this count is not a finished nesting/BOM quantity.

Implemented reductions:

- Remove both decorative rear wood fascias: −2 wooden parts. Two small functional metal carriers are only candidate adapters.
- Combine landing and latch reinforcement into one CNC union on each side: −2 wooden parts. Saved-solid checks prove each union contains both original load regions, with no added thickness.
- Keep two CPU rails, now standard 18 mm plywood with defined bottom/metal load transfer.

Retain the three low crossmembers for shell shear/torsion and bottom restraint. Retain the cradle rails/ties, rear pivot laminations, local safety/gas anchors and backbox load path. The four backbox rear frame members remain COMBINE candidates: a single CNC frame needs nesting and shear/joint verification before changing it. They were not removed merely to reduce the count. Do not substitute unverified small metal brackets at positive-stay anchors.

## Visual gate and remaining measurements

Review `10-utility-comparison.png`, then `11-utility-A.png` and `12-utility-B.png`. Confirm **rear face A versus underside B**, and whether to include the optional Ethernet carrier or leave it blank. Final placement will be committed only after that review.

Still measure: actual slides and mounting pattern; case bolt points; four angle clamps/backing/bolt stack; rear door hinge/latch; real leg/bracket envelopes; actual production plywood; mains interface/enclosure/glands; RJ45 or cable gland; floor/plug clearance if B is chosen. All manufacturing gates remain closed.


## Validation evidence

- `make validate`: current Python validators pass.
- `make build-current`: FreeCADCmd generation, saved-document recompute/solid checks and gallery generation pass.
- Saved geometry: **61 checks pass**, including unchanged CPU datums, both utility cut/plug/enclosure candidates, protected joint/leg regions, outward door sweep, exact rectangular PC travel sweeps, rail/angle/backing contacts, retained combined reinforcement and the 36-row CAD/wood register match.
- Ten negative controls reject inward door, raised shelf, raised door, restored CPU harness, bottom-joint cut, leg-zone cut, insufficient mains/signal separation, incorrect part ID, restored rear USB cut and floating rail.
- `git diff --check` passes. Owner-modified historical master remains byte-identical to the takeover backup. No reference models changed; no push or merge.

The earlier 10–15 mm door-to-low-fascia check is obsolete because those fascias no longer exist. It is replaced by actual geometric clearances for **both** alternative carriers, enclosures and plug-access volumes against the unchanged door and structure; it is not bypassed to make the old colliding windows pass.

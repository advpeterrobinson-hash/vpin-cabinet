# Selected rear utility — Option A

Owner selected two localized rear-face interfaces. Option B underside is rejected and removed from active CAD/config/gallery; the [historical comparison](history/REAR_UTILITY_V26_COMPARISON.md) retains the study. This selects architecture, not manufacturing release.

| Interface | Carrier X / Z, mm | Generic wood opening | Internal reserve |
|---|---|---|---|
| Mains/master disconnect | X50..140 / Z395..465; 90×70×3 | 70×50 at X60 / Z405 | Separate 110×120×90 enclosure at X45 / Y1170.1 / Z385 |
| Optional Ethernet or blank | X510..550 / Z405..445; 40×40×3 | 24×24 at X518 / Z413 | 50×60×60 access envelope |

The active rear panel now contains only these two generic utility apertures plus the unchanged CPU hatch. Utility material removed: **4,076 mm² / 73,368 mm³** at nominal 18 mm. Bottom utility removal: **zero**. No full-band panel or decorative fascia is created; the rest of the 524×176.9 mm available upper band remains available for future electronics/DOF/service. Exterior mains–signal gap is 370 mm; internal envelope gap is 350 mm. These are packaging margins, not a certified electrical design.

Ethernet is optional: use a blank carrier or a replaceable measured RJ45 keystone/coupler faceplate. Cabinet wood is not a component-specific RJ45 pattern. SERVICE HDMI, USB-A, USB-C and reserve cutouts are absent; access these on the extended PC. Power/reset/DOF service controls stay at the coin door.

CPU opening remains X130..470 / Z110..350, shelf Z135, door Z98..362 with 105° outward swing. Saved-solid checks protect the bottom joint and leg load regions and prove door/plug/PC travel clearance.

The mains carrier is only an interface. Hazardous terminals remain in a separate touch-safe tool-access enclosure fixed to permanent structure, never the CPU door. Preserve dedicated PE continuity and bond exposed conductive mains parts; provide rated entry strain relief so terminals carry no cable pull. Measure the inlet/disconnect, enclosure, insulated exits, glands, fasteners and plug envelope before final patterns or CNC release. No component ratings or wiring schematic are released here.

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

- Remove both decorative rear wood fascias: −2 wooden parts. Two small functional metal carriers are selected replaceable adapters.
- Combine landing and latch reinforcement into one CNC union on each side: −2 wooden parts. Saved-solid checks prove each union contains both original load regions, with no added thickness.
- Keep two CPU rails, now standard 18 mm plywood with defined bottom/metal load transfer.

Retain the three low crossmembers for shell shear/torsion and bottom restraint. Retain the cradle rails/ties, rear pivot laminations, local safety/gas anchors and backbox load path. The four backbox rear frame members remain COMBINE candidates: a single CNC frame needs nesting and shear/joint verification before changing it. They were not removed merely to reduce the count. Do not substitute unverified small metal brackets at positive-stay anchors.

## Rail planning reserve — BLOCKED on measured hardware

No geometry shift is justified: modeled bracket inner edges X113 and X487 leave 374 mm. The centered stack is 285 shelf + 2×12.7 slides + 2×18 rails = 346.4 mm, leaving (374−346.4)/2 = **13.8 mm per side**. A 2–3 mm translation improves one side and worsens the other; moving clamps alone does not move the rail edge. Achieving 15 mm on both sides needs 2.4 mm less total stack width or more measured bracket clearance. Moving both rails inward breaks slide-face contact and the fixed shelf width; no such change is made.

Measure each installed rear bracket's innermost X envelope including bolt heads/nuts/washers, flange projection, mounted Y/Z extent and leg bolt protrusion. Also measure actual slide thickness and specified side clearance, plywood thickness, and clamp/backing/bolt stack. Resolve the 1.2 mm per-side planning shortfall with those measurements before rail/support CNC freeze. Do not trim leg load paths or assume nominal hardware bounds are final.

## Review and verification

Inspect gallery `10-rear-utility-selected.png`, `02-rear-elevation.png`, `03-door-closed.png`, `04-door-open.png`, `06-pc-extended.png`, `09-rear-load-path.png`, and `11-utility-A.png`. The request is visual confirmation of the small interfaces above the unchanged low door, not manufacturing approval.

Validation checks actual saved panel subtraction, connected solid integrity, protected regions, mains/signal separation, CPU motion, rail contacts and the 36-row register. Negative controls include an oversized utility panel cut and reintroduced underside hardware. Physical hardware holes, strength/proof tests and measured-stock/coupon release remain blocked.

Validation for this selection pass: `make build-current` passed Python validation, fresh FreeCADCmd generation and 53 saved-solid checks. All 12 negative controls passed, including full-band removal and underside return. `bom/ACTIVE_PARTS.csv` exactly matches the generated register; `git diff --check` passed. The reduced check count removes tests of rejected B geometry, not checks on selected A or the CPU/load paths. Owner's historical master remains untouched.

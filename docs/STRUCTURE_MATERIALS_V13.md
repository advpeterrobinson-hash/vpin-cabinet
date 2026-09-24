# Structure and materials v0.13 — Brazil-ready CNC-flatpack strength strategy

> Current owner baseline: [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md). Older assist/stay descriptions below are historical; no assist hardware blocks current CNC. Use the active hardware/feature registers for procurement.

Status: engineering provisional; not manufacturing-ready.

## Answer to the solid-wood question

The cabinet does **not** require solid timber for primary strength if the plywood structure and load paths are designed correctly.

The baseline remains high-quality **18 mm naval/marine-grade plywood (compensado naval)** for the main cabinet and backbox perimeter. Critical load points are reinforced with additional CNC-cut plywood doublers and metal backing/brackets rather than relying on softwood/hardwood cleats that vary by region and require additional cutting at home.

This is deliberate: laminated plywood doublers are easier to reproduce from a CNC plan, easier to source in Brazil, dimensionally predictable, and compatible with the apartment-build objective.

Solid wood may remain an optional local alternative for non-critical cleats where the drawings permit it, but the released design must not depend on a builder finding a particular timber species or milling it accurately.

## Brazil-market material direction

Primary target sheet:

- 18 mm compensado virola naval, good lamination quality;
- 18 mm compensado pinus naval as an acceptable alternative if the sheet passes inspection.

Commonly available alternate thicknesses such as 15, 20 and 25 mm may be used for specific removable or reinforced parts when justified, but the base kit should minimize the number of sheet thicknesses.

Preferred rear keyed service door: **15 mm plywood**. This is thick enough for a robust keyed panel while remaining lighter than an 18 mm door.

MDF is not accepted for primary structure, hinge anchors, leg corners, backbox shelf, gas-strut anchors or the PC drawer load path.

Every build should measure the actual plywood before CNC production. '18 mm' stock often varies enough to matter for dados and tab/slot joints. A physical tolerance coupon remains mandatory.

## Main-cabinet load path

The four pinball legs do not dump the full machine weight through the bottom panel. Their loads transfer into the cabinet corner structure through metal leg brackets and the side/front/rear panels.

The bottom panel still needs to be strong because it carries internal hardware and prevents racking, but it should not be treated like an unsupported floor.

Baseline main-cabinet structure:

- 18 mm sides;
- 18 mm front;
- 18 mm rear;
- 18 mm bottom;
- bottom captured in CNC-cut dados (initial study depth 6 mm, final value after provider/coupon validation);
- three low structural crossmembers, minimum ~60 mm high, made from 18 mm plywood;
- crossmembers positioned to shorten bottom-panel span and create dedicated load paths for the PC drawer/electronics.

Heavy parts should mount to trays, rails or crossmembers rather than simply being screwed into the bottom sheet.

## Critical reinforcement zones

### Leg corners

Use doubled CNC plywood around the corner load zones: two 18 mm layers for approximately **36 mm local wood thickness**, combined with real pinball steel leg brackets or equivalent fabricated backing plates.

Critical leg loads use through-bolts. Wood screws alone are not acceptable here.

### Rear backbox shelf

The backbox floor sits on the rear shelf and is positively clamped to it. Use an 18 mm shelf with an 18 mm underside doubler/crossmember through the hinge/locking/passport zone, yielding approximately **36 mm local thickness** where loads concentrate.

The locking bolts engage metal-backed captive threads/T-nuts or an equivalent steel-backed threaded solution.

### Playfield hinge and gas struts

The OLED cradle hinge and gas-strut reactions must land on full-strength structure. Use 18+18 mm local plywood doublers or equivalent steel brackets, through-bolted or using metal-backed inserts.

The thin clearance skin of any OLED pocket is never a structural anchor.

### PC drawer

Drawer slides mount to dedicated subrails/doublers tied to lower crossmembers. The 25 kg provisional design payload is for verification; the actual computer will likely be lighter, but the extended drawer creates leverage and must not be supported only by screws into a thin panel edge.

### Lockdown bar

The custom-width lockdown bar uses a metal receiver tied into reinforced front woodwork. A local plywood doubler is required behind the receiver.

## Structural verification envelope

For engineering checks before release, use a conservative provisional gross-machine envelope of **150 kg**. This is not a prediction that the finished machine will weigh 150 kg; it gives us reserve for hardware, displays, toys, power supplies and future upgrades.

Leg corners, hinge brackets and similar local dynamic areas should be checked with a provisional **2.0 dynamic factor** for nudge/movement/shock cases.

The cabinet is not designed as a seat, ladder or person-support platform. A user standing or sitting on it is outside the intended load case.

## SSF compatibility

Strength does not mean turning the cabinet into a dead solid block.

The lower crossmembers should stay low and out of the primary SSF exciter zones. Shelves and electronics rails must avoid unnecessarily bridging the active side walls. Local reinforcement is concentrated where the loads actually enter the structure.

## Rear backbox service door

The keyed rear service door added in v0.12 does not weaken the backbox into an open frame.

The aperture is surrounded by fixed rear perimeter structure and dedicated upper/lower crossmembers. The adjustable monitor rails attach to those fixed members. The service door is a closure and local stiffener when latched, not the sole shear member.

The two 120 mm ventilation fans stay on a fixed upper rear panel.

## Shock-hazard policy

Every stage that introduces or modifies mains-voltage routing must include an explicit shock-hazard review.

The following are blocking design defects:

- reachable mains screw terminals;
- unguarded energized bus bars;
- exposed mains splices behind the keyed service door;
- accessible live parts through fan or speaker openings;
- metal parts that require protective-earth bonding but are left floating;
- cable insulation rubbing on sharp wood/metal edges.

The keyed service door may expose low-voltage service electronics, but any mains junction remains inside a separate tool-access-only enclosure.

## CNC-flatpack implication

The strength strategy should come from CNC geometry, not from an experienced carpenter improvising cleats after delivery.

Critical reinforcements should therefore be supplied as numbered CNC parts with self-locating dados/tabs/holes. The builder should mainly glue/bolt the parts together using ordinary hand tools.

The design objective remains: take the plans to a local CNC/fabrication shop, receive a complete structural kit, and assemble it in an apartment without a table saw, router table, drill press or welder.

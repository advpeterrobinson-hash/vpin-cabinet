# Cabinet structure v0.20 — joinery, legs, PC drawer and glass interfaces

Status: **engineering-selected packaging; not manufacturing-ready**.

This stage moves the project from broad shell envelopes toward a CNC-flat-pack structure that can be fabricated locally and assembled with ordinary hand tools. It does **not** yet release production toolpaths or hardware holes.

## 1. Main cabinet baseline

- outer width: **600 mm**;
- nominal structural plywood: **18 mm**;
- nominal full-thickness inner width: **564 mm**;
- side length: **1308.1 mm**;
- front outside height: **400.05 mm**;
- rear outside height: **596.9 mm**;
- rear top flat: **180.975 mm**;
- WPC-derived side slope: approximately **9.907 degrees**.

The 600 mm width is the owner-approved long-term baseline. It is intentionally wider than the Williams WPC standard-body reference so a compact 42/43-inch high-refresh display can fit between full-thickness sidewalls.

## 2. CNC joinery philosophy

The apartment-builder workflow should not depend on hand routing or visually aligning structural panels.

Current nominal joinery uses a **6 mm capture depth** into the side/end structure. This is an engineering depth only. Final groove width, tab thickness and fit clearance are regenerated from the measured plywood sheet and the CNC tolerance coupon.

At nominal 18 mm stock:

- material remaining behind a 6 mm side dado: **12 mm**;
- captured front/rear nominal blank width: **576 mm**;
- captured bottom nominal blank: **576 x 1284.1 mm**;
- bottom panel bottom elevation: **18 mm** above cabinet bottom;
- low crossmembers: three pieces, nominal **576 mm** captured width, **18 mm** thickness and **80 mm** height.

The current low crossmember Y datums are 260, 650 and 1040 mm from the cabinet front datum. They live low in the cabinet and deliberately stay below the SSF exciter-height zones.

### CNC release rules

Before production:

1. measure every structural plywood sheet at multiple points;
2. cut the project tolerance coupon;
3. confirm actual cutter diameter/runout and provider compensation policy;
4. update dado widths and mating tab/shoulder values;
5. confirm whether Cutter CNC prefers radius-compatible shoulders or dogbone reliefs for the selected joints;
6. avoid dogbones on exposed cosmetic edges;
7. perform a complete dry fit before permanent glue-up.

The final CNC package must distinguish through-cut, pocket/dado, pilot-drill and engraving layers.

## 3. Leg-corner load path

Real pinball legs remain the target.

Each of the four corners receives two local 18 mm plywood reinforcement pieces:

- an inside sidewall doubler, nominal **220 x 240 mm**;
- an inside front/rear end-panel doubler, nominal **160 x 240 mm**.

This creates local ~36 mm wood thickness at the leg load path before the steel bracket/backing hardware is added.

The intended load path is:

`leg -> through-bolts -> steel internal bracket/backing -> doubled plywood corner -> cabinet shell/crossmembers`

Leg holes are **not** released to CNC until the actual leg/bracket set is selected and measured. Retractable/lift-wheel volumes are reserved at each corner, but playing load must remain on the levelers rather than on the wheels.

## 4. PC service drawer

The PC tray does **not** require a large weakened opening in the front, side or rear cabinet wall.

The selected v0.20 architecture is an **internal fore-aft service drawer**:

- open the playfield into its positively supported service position;
- unlock the PC drawer;
- slide the PC tray forward inside the open cabinet;
- service connectors/components from above;
- if complete removal is needed, use the slide disconnect/release and lift the tray upward through the open top.

Current packaging:

- tray: **470 x 400 x 18 mm**;
- stowed Y: **690 mm**;
- service Y: **220 mm**;
- internal slide travel: **470 mm**;
- tray Z: **165 mm**;
- PC service height envelope above tray datum: **230 mm**;
- preferred slide length class: **500 mm**;
- provisional slide thickness allowance: **12 mm each side**;
- minimum preferred slide pair rating: **45 kg**;
- physical proof-test payload: **25 kg**.

The drawer uses two dedicated plywood subrails located inward of the cabinet walls. The subrails tie into the bottom/crossmember structure and are not treated as broad rigid bridges between SSF-active sidewall zones.

Exact slide hole patterns are blocked until a physical pair of locking full-extension slides is selected and measured.

## 5. SSF preservation

Sidewall exciter zones are explicit keepouts rather than an afterthought.

Current reserved zones on each side include a front and rear region. Broad shelves or braces should not clamp the left and right cabinet walls together across those zones at exciter height.

Low crossmembers and PC support structure may connect the cabinet near the bottom, where they are structurally useful without defeating the desired sidewall acoustic behavior.

## 6. Playfield glass target

The 600 mm cabinet requires custom-width playfield glass rather than relying on standard WPC glass.

Current packaging target:

- **575 mm wide**;
- **1100 mm long along the cabinet slope**;
- **5 mm thick**;
- tempered safety glass;
- polished/arrissed safe edges;
- symmetric nominal side cover: **12.5 mm per side** within the 600 mm body.

The glass is a local-fabrication target, not a purchase instruction. Do **not** order it until the siderail and lockdown-bar interfaces are physically mocked up and measured.

## 7. Siderails

Two custom/local-fabricated siderails are allowed and expected.

The FreeCAD package currently models only a top-flange envelope:

- length class: approximately **1120 mm along the slope**;
- top flange width: **32 mm**;
- nominal sheet thickness envelope: **2 mm**;
- glass edge capture target: at least **12.5 mm**.

The final folded profile, material, finish, mounting holes and anti-rattle/glass channel details remain open until the metal-shop discussion and physical glass mockup.

## 8. Lockdown bar

A standard-width lockdown bar is not required.

Current envelope:

- custom outside width: **600 mm**;
- provisional front-to-rear packaging depth: **90 mm**;
- provisional height: **35 mm**;
- positive receiver/latch required;
- local metal fabrication explicitly permitted.

The final bar section and receiver geometry should prioritize stiffness, easy service release, safe glass retention and reproducibility by a local sheet-metal/laser/bending shop.

Receiver holes remain blocked until the chosen fabricated/physical receiver is measured.

## 9. FreeCAD review package

Run:

```bash
make build-cabinet-structure-v20
freecad cad/master/vpin-master.FCStd
```

Review group:

`CABINET STRUCTURE v0.20 - JOINERY / LEGS / PC DRAWER / GLASS`

The package shows:

- captured front/rear/bottom panel geometry;
- low structural crossmembers;
- nominal dado/rabbet machining ghosts;
- doubled leg-corner zones and bracket/wheel keepouts;
- PC subrails, slide keepouts, stowed tray, forward service ghost and service envelope;
- SSF sidewall keepouts;
- sloped tempered-glass target;
- siderail envelopes;
- lockdown bar and receiver envelopes.

## 10. Manufacturing blocks still active

Do not release production CNC, metal or glass orders until all of the following are resolved:

- measured plywood thickness;
- CNC tolerance coupon;
- Cutter CNC tool/layer/radius consultation;
- actual leg/bracket set measured;
- actual PC slide pair measured;
- lockdown/siderail fabrication concept proof-fitted;
- final playfield glass size measured from that mockup;
- dry-fit validation of the cabinet;
- final service/collision review with playfield mechanics and PC tray;
- proof testing of leg, drawer and playfield-support load paths.

This stage intentionally advances the permanent structure while keeping short-lived or vendor-specific hardware on replaceable/measured interfaces.

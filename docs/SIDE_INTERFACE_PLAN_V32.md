# V32 side hardware, load and service interfaces

**Proposal for interface development; no new machining adopted. CNC BLOCKED.**

This continues the [saved-side audit](SIDE_PANEL_REVIEW_V32.md). Coordinates are mm: X left-to-right as seen from the front, Y front-to-rear, Z upward from cabinet bottom. Source is the saved V32 FCStd; the audit records its hash. Hardware dimensions and load ratings remain unselected.

## Shared datums

Use the outside front plane Y0, bottom Z0 and body center X300 for shared drawings. Outside side faces are X0/600; inside faces X18/582 at nominal stock. A change in measured thickness must regenerate mating geometry, not shift hardware by eye. The side upper profile rises from Z400.05 at Y0 to Z596.9 at Y1127.125, then stays flat to Y1308.1. This is a shell datum, **not a specified glass seating surface**. Glass thickness, channel engagement, support and removal travel must establish the final glass/lockdown stack together.

The front controls and outward door study retain their own candidate envelopes. Leg plates and the lockdown receiver must be checked against that study, including the proposed right plunger, rather than against the obsolete inward door prism. No leg bolt datum is inferred from a photograph or the backbox pivot.

## Existing occupied side interfaces

The audit now extracts these bounding footprints from both saved sides' neighboring supports and checks their mirror symmetry. Values below are rounded to 0.01 mm for reading; JSON retains full precision. X intrusion is measured inward from X18 or X582.

| Existing part pair | Y interval | Z interval | Inward extent |
|---|---:|---:|---:|
| S1SupL/R | 120–270 | 142–160 | 18 |
| S2SupL/R | 600–750 | 162–180 | 18 |
| S3SupL/R | 1080–1230 | 222–240 | 18 |
| T1GuideL/R | 350–410 | 238.69–383.69 | 18 |
| T2GuideL/R | 670–730 | 294.58–439.58 | 18 |
| T3GuideL/R | 950–1010 | 343.48–488.48 | 18 |
| **Floor cleats**, legacy FLOOR_CLEAT_18/552 | 120–1272.1 | 0–18 | 30 |

These are occupied bounding rectangles, including grooves and holes; they are neither measured contact areas nor released screw zones. Shell joints, brackets farther inward, shelves, rails and missing hardware also constrain access. Empty space between rectangles is not automatically usable.

The rear button at Y310 has a candidate radial boundary at Y328; T1Guide begins at Y350, leaving **22 mm in Y between these candidate bounds**. This is not room proven for a socket, hand, connector or SSF mount. Check actual service-tool and cable envelopes before using this region. Each T guide also needs upward extraction clearance after the monitor assembly and retention hardware are removed; putting a prop receiver or cable clamp above a guide can defeat removability even without a closed-state collision.

## Button mounting decision to develop

The existing Ø15.875 bore and Ø28.575 counterbores are references. Keep them provisional until barrel diameter, usable thread, flange seating, nut/washer diameter, switch removal and terminal orientation are known.

| Candidate stack at nominal 18 mm stock | Remaining wood under clamp | Status |
|---|---:|---|
| Existing: outside 7.9375 + inside 4.7625 recess | 5.3 | Audited geometry; strength and hardware fit unverified |
| Omit outside recess; retain inside 4.7625 | 13.2375 | Unmodeled alternative; may change button projection and thread engagement |
| Omit both recesses | 18 | Preferred first fit trial for suitable long-barrel hardware; unmodeled |

These alternatives are explicit design proposals, not strength calculations or accepted cuts. Select the least recess required by actual hardware and ergonomics. A replaceable inner mounting plate can carry switches or cable strain relief; it does not restore strength to a thin wooden clamp annulus. Reject a stack if the nut bottoms before clamping, the washer cannot seat, or the switch cannot be removed through the intended access route. No larger bore or deeper pocket is authorized by this comparison.

## Proposed load paths and service sequence

| Interface | Proposed load/service path | Evidence needed before fixing holes |
|---|---|---|
| Real pinball legs | Leg bolts → selected inner corner plate/load spreader → full-thickness corner structure. Keep plate and tool access coordinated with Front, Rear and Floor joints. | Actual plate/bolt drawing; full socket/driver engagement and bolt withdrawal; bearing/edge distances; assembled cabinet and nudging loads; corner assembly order. Do not route primary loads into a button web. |
| Glass and custom lockdown | Removable bar/receiver and glass channel use one seating datum; receiver fasteners remain accessible through the front service opening or with glass removed. | Selected glass stack; engagement and retention; bar lift/release and glass withdrawal; clashes with door flange, front controls and front leg plates. |
| Display hinge and captive props | Display adapters → independent cradle → hinge and each prop receiver → full-strength structural attachment. Existing rails/T supports show static packaging only. | Total moving mass including cradle/cables, center of gravity, pivot axis and opening limit; closed/open/stowed sweeps; receiver reinforcement and fastener access. Each prop must carry the entire moving load independently with positive pin/keeper retention; both engage for service. No load assigned to a reduced-thickness clearance pocket. |
| SSF transducers | Removable local rigid mount couples each selected device to its intended wall region. Start with a local plate, avoiding a new cross-cabinet tie through an active wall region. | Actual device/mount pattern, retention, wire exit, removal tool path, intended vibration location and interaction with existing shelf/guide anchors. No quantitative acoustic claim from geometry. |
| Mechanical feedback | Device → removable rigid mount → rated structural attachment, located for the intended effect. | Device reaction/load data, mounting access and vibration retention; independent service-disable path; cable separation from moving display/props. Existing generic T support angles have no load rating. |

For assembly planning, install inaccessible corner hardware before closing the shell only if it will still be replaceable later through a documented route. Fit supports and guides with accessible retention, then removable shelves and feedback mounts, then the display cradle. Route wiring along verified stationary corridors with strain relief and disconnects; test component removal before closing glass. This order is a proposal to validate with selected hardware, not a completed assembly proof.

Do not choose prop coordinates from empty CAD space alone: near-aligned prop geometry can demand large receiver forces. Obtain the moving assembly and support geometry before a load calculation and one-prop proof plan. Physical proof remains pending while physical sessions are paused.

## Next geometry gate

First obtain side-button stacks and leg/inner-plate dimensions; check them with the front receiver and plunger service paths. Then model separate removable mount, tool-access, wire and motion envelopes on both sides. Report conflicts with the occupied supports above before proposing local changes. Keep missing hardware explicitly unverified. Rear closure still requires the owner's PC architecture decision; this document adopts neither the low-base nor drawer alternative.

Reproduce footprint evidence with the command in [the side audit](SIDE_PANEL_REVIEW_V32.md). The extension checks seven mirrored support pairs and fourteen inner-face datums, in addition to the original 25 checks. It does not save or recut the source FCStd.

Original material: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

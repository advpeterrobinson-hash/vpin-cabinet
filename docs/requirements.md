# Cabinet Requirements

## Cabinet

Williams WPC standard-body proportions are the visual reference, not a dimensional mandate.

Current selected main-cabinet outer width: **600 mm**.

Main structural material:
- Metric structural plywood
- Nominal target: 18 mm
- Final CNC geometry must follow measured sheet thickness

Construction must prioritize:
- CNC cutting
- Self-aligning captured joints
- Minimal manual routing/drilling
- Modular service access
- Replaceable component-specific adapters
- Apartment-friendly assembly without major shop tools

## Playfield display

The cabinet is **not locked to one TV model**.

Permanent service target:
- Compact 42/43-inch 16:9 display class
- Maximum packaging target approximately 560 x 970 x 55 mm
- Display mass design limit 12 kg
- 4K UHD minimum target
- Native 120 Hz or better
- HDMI 2.1 / VRR / low-latency mode preferred
- Exact model selected late from the Brazil market

Requirements:
- Rigid independent plywood-dominant cradle
- Replaceable VESA/carrier interface
- Rear pivot/hinge
- Manual lift; final measured operating-force check required
- Two simple captive prop rods with positive pins/keepers; either supports the full service load
- Two positive closed-position restraints/supports
- Service position 65 degrees in the active engineering candidate
- Cable service loop
- Display chassis must not be structural

## Backglass

- Approx. 31.5/32-inch primary target
- 1920x1080 acceptable
- Low-cost display preferred
- Removable/replaceable mounting system
- 27/28-inch fallback supported by adjustable carrier/bezel

## Main-cabinet structure

- Nominal 6 mm captured CNC joinery depth is the engineering baseline only
- Measured plywood and tolerance coupon control final groove widths
- Bottom/front/rear/crossmembers should self-locate from CNC features
- Three low structural crossmembers should stay below SSF exciter-height zones
- Critical loads use through-bolts/metal backing rather than wood screws into single 18 mm skins

## Legs and mobility

- **Classic pinball-style legs** are retained
- Real pinball levelers are retained
- Use compact internal steel leg brackets/backing rather than large permanent plywood corner blocks
- Primary leg fasteners are through-bolts
- Exact leg/bracket hole pattern remains CNC-blocked until actual hardware is selected and measured
- Large 18+18 mm plywood leg-corner doublers are **not** part of the default design; add only compact local backing if physical proof testing shows it is needed
- Cabinet mobility uses **external removable PinSkates-style side skates** attached to the classic legs only when moving the machine
- No integrated/retractable casters or wheel keepouts are built into the cabinet
- PinSkates are removed for play; all playing load remains on the four leg levelers
- Cabinet must remain rigid for nudging and force feedback

## PC

- **Owner decision, 2026-09-29: low fixed base, no drawer or removable-tray mechanism.** This supersedes the earlier full-extension drawer requirement.
- Open-case packaging reference: 265 X × 440 Y × 128 Z mm; actual mounting points remain unmeasured.
- PCBase: one replaceable 285 × 460 × 18 mm board at X157.5/Y830/Z36, directly above the floor. No second sled, slides or raised drawer supports.
- Case bolts directly to PCBase; base and heavy PC components require positive mechanical restraint for nudging/vibration. Actual fixing patterns remain to be detailed.
- PC remains installed for use and routine service. Keyed downward-opening rear door provides access; raise the playfield for work that requires access from above. Rear-only service with the playfield closed is no longer a universal requirement.
- Existing rear aperture X130..470/Z72..365 retained; current hinged-door study and limitations are in REAR_DOOR_V32.md.
- Exceptional PC replacement may require disconnecting cables and unbolting the base/case. The modeled lift38 mm then rear500 mm route is packaging evidence only, not an approved handling procedure or routine tray.
- Separate touch-safe mains enclosure; no bare terminals behind the rear service cover.

## Playfield glass / siderails / lockdown

- Custom local playfield glass is acceptable and expected for the 600 mm body
- Current packaging target: approximately 575 x 1100 x 5 mm tempered glass
- Final glass order waits for physical siderail/lockdown mockup
- Custom/local-fabricated siderails permitted
- Custom 600 mm lockdown bar permitted
- Lockdown receiver must positively retain the glass/front assembly

## Force Feedback

Priority subsystem.

Reserve mounting positions for:
- Flipper feedback
- Sling feedback
- Bumper/impact feedback
- Knocker
- Shaker
- Gear motor
- Additional DOF toys

Feedback devices should couple mechanically to cabinet structure.

## SSF

Reserve isolated cabinet-wall areas for:
- Front-left exciter
- Front-right exciter
- Rear-left exciter
- Rear-right exciter

Do not bridge these areas unnecessarily with rigid shelves or PC support structures at exciter height.

## Electronics packaging

The reference-cabinet review favors a large open central service volume with localized removable boards/rails rather than filling the cabinet with fixed furniture.

Reserve future removable mounting panels/rails for:
- Main controller
- DOF output boards
- LED controllers
- Powered USB hub
- Audio hardware
- DC distribution

Separate high-current and signal wiring routes. Preserve clear service aisles and deliberate service access. The PC stays on its low base; use rear access or open the playfield as required by the service task.

## Power

One external grounded mains cord.

Modes:
1. OFF
2. AUDIO ONLY
3. FULL PINBALL

Audio-only mode:
- PC OFF
- playfield display OFF
- backglass OFF
- mechanical DOF OFF
- Bluetooth receiver ON
- main audio amplifier ON

Reachable hazardous voltage is a blocking defect. Ordinary/keyed service areas must not expose bare mains terminals.

Rear door: unlock with key, open downward, service and close. Opening limiters are optional per owner; a flexing low-voltage fan harness is required; no routine screw removal or fan disconnection. Optional owner-installed unkeyed slide bolt needs no project drawing.

## Service I/O

Front/underside:
- USB-A
- USB-A
- USB-C
- Hardware master volume

Rear/underside permanent functions:
- AC mains/master disconnect on a fixed small interface with independent touch-safe enclosure.
- Optional wired Ethernet on a small replaceable carrier; blank if unused.
- No permanent SERVICE HDMI, rear USB-A/USB-C or RESERVE cutouts. Access the installed PC through the service openings.
- PC POWER, RESET and DOF SERVICE remain at the coin door; no rear duplicates.
- Rear-face A versus underside B awaits owner comparison review (REAR_UTILITY_V26.md).
- Current rear aperture is X130..470/Z72..365; keyed hinged door is detailed in REAR_DOOR_V32.md. Bottom-joint and leg load paths take precedence over utility placement.

## Manufacturing

Final manufacturing package should include:
- FreeCAD source
- DXF/DWG where required by vendor
- SVG where useful
- dimensioned PDF drawings
- assembly drawings
- CNC sheet layouts
- BOM
- electrical drawings
- part labels/revisions

Before cabinet production:
- measure actual plywood
- cut a CNC tolerance/material coupon
- confirm Cutter CNC tooling/layer/radius conventions
- measure actual hardware that controls hole patterns
- complete dry-fit and collision checks
- proof-test classic leg/bracket corners and positive restraint of the fixed PC/base
- proof-fit rear PC door/hinges/key lock before final rear-panel CNC release

No current engineering branch is approved for production CNC yet.

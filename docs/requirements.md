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
- Dual gas struts for lift assistance only
- Two independent positive mechanical safety stays
- Two positive closed-position restraints/supports
- Service position approximately 70 degrees
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

- Real pinball-style legs
- Real levelers
- Local plywood reinforcement creates approximately 36 mm wood thickness at leg corners
- Steel leg brackets/backing required
- Primary leg fasteners are through-bolts
- Exact leg holes are CNC-blocked until actual hardware is selected/measured
- Wheels must retract or otherwise leave levelers firmly on floor during play
- Cabinet must remain rigid for nudging

## PC

- Open ATX test-bench/mining-style metal chassis
- Approximate reference chassis size: 440 x 265 x 128 mm
- Mounted to removable internal drawer/platform
- Full-extension locking slides
- Drawer service occurs with playfield raised; tray moves fore-aft inside cabinet and can lift out after slide release
- GPU secondary support
- PC mechanically isolated from force-feedback structure
- Drawer proof-test target: 25 kg

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

## Electronics

Modular removable mounting panels for:
- Main controller
- DOF output boards
- LED controllers
- Powered USB hub
- Audio hardware
- DC distribution

Separate high-current and signal wiring routes.

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

## Service I/O

Front/underside:
- USB-A
- USB-A
- USB-C
- Hardware master volume

Rear:
- Ethernet
- USB service
- optional HDMI service
- main disconnect

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

No current engineering branch is approved for production CNC yet.

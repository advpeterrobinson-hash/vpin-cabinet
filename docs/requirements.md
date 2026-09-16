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

- Open ATX test-bench/mining-style metal chassis
- Owner reference chassis size: approximately **440 x 265 x 128 mm**
- Routine PC maintenance is performed from the **rear of the pinball cabinet** through a dedicated main-cabinet rear service door
- The playfield **must not need to be opened** just to replace RAM, SSDs, service cables, inspect the GPU, or perform ordinary PC work
- Rear service aperture engineering target: approximately **520 x 280 mm**, above the low rear I/O zones and above the compact rear leg-bracket envelope
- Open PC case bolts **directly to one small flat plywood shelf**, nominally **460 x 285 x 18 mm**
- No drawer box and no second removable sled
- Two simple **300 mm-class full-extension slides/telescopic rails** move the shelf **rearward**, through the rear service door and behind the machine
- Stowed shelf target: Y approximately 1005..1290 mm
- Rear service shelf target: Y approximately 1305..1590 mm
- One simple positive stowed retainer prevents movement/rattle during nudge and DOF operation
- Because the shelf is case-sized rather than full-cabinet-width, compact replaceable spacer rails are permitted between cabinet walls and the slide pair
- Actual slide holes, spacer stack and open-case mounting holes remain blocked until physical hardware is measured
- PC harnesses reserve at least **450 mm** protected rearward service-loop length
- Complete shelf/case removal is from the rear using the slide disconnect/release hardware if supplied
- PC mechanically isolated from force-feedback structure
- Shelf proof-test target: 20 kg; slide-pair rating target >=30 kg
- Rear PC service door/frame must not expose bare mains terminals; cabinet power is isolated before PC hardware service

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

Separate high-current and signal wiring routes. Preserve clear service aisles and deliberate service access. PC routine service is from the rear backdoor; opening the playfield remains reserved for playfield/DOF/internal-cabinet work rather than ordinary PC maintenance.

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

Rear low zones:
- Ethernet
- USB service
- optional HDMI service
- main disconnect

Rear mid service zone:
- dedicated PC backdoor opening above the low I/O fascias
- rearward pull-out PC shelf immediately behind that door

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
- proof-test classic leg/bracket corners and the rear pull-out PC shelf
- proof-fit rear PC door/frame/hinge/latch before final rear-panel CNC release

No current engineering branch is approved for production CNC yet.

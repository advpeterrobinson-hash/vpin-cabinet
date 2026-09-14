# Cabinet Requirements

## Cabinet

Williams WPC standard-body proportions.

Main structural material:
- Metric plywood
- Nominal target: 18 mm
- Final CAD value must follow measured sheet thickness

Construction must prioritize:
- CNC cutting
- Self-aligning joints
- Minimal manual routing/drilling
- Modular service access
- Replaceable components

## Playfield

LG OLED42C5.

Requirements:
- Rigid independent cradle
- VESA-supported mounting
- Rear pivot/hinge
- Dual gas struts
- Mechanical safety prop or positive secondary restraint
- Service position approximately 60-75 degrees
- Cable service loop
- Playfield must not be structurally supported by OLED chassis

## Backglass

- Approx. 32-inch
- 1920x1080 acceptable
- Low-cost display preferred
- Removable/replaceable mounting system

## PC

- Open ATX test-bench/mining-style metal chassis
- Approximate known chassis size:
  440 x 265 x 128 mm
- Mounted to removable drawer/platform
- Full-extension locking slides
- GPU secondary support
- PC mechanically isolated from force-feedback structure

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

Do not bridge these areas unnecessarily with rigid shelves.

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

One external mains cord.

Modes:
1. OFF
2. AUDIO ONLY
3. FULL PINBALL

Audio-only mode:
- PC OFF
- OLED OFF
- backglass OFF
- mechanical DOF OFF
- Bluetooth receiver ON
- main audio amplifier ON

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

## Mobility

- Real pinball legs
- Real levelers
- Wheels must retract or otherwise leave levelers firmly on floor during play
- Cabinet must remain rigid for nudging

## Manufacturing

Final manufacturing package should include:
- FreeCAD source
- DXF
- SVG where useful
- dimensioned PDF drawings
- assembly drawings
- CNC sheet layouts
- BOM
- electrical drawings

A CNC tolerance/material test coupon must be cut before cabinet production.

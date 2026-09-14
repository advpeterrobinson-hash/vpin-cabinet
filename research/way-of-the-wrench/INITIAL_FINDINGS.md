# Initial findings from Way of the Wrench ecosystem

These are early reference findings only. They are not production specifications.

## Series identity

- The original playlist is the creator's detailed DIY / budget virtual-pinball cabinet series and is widely used by builders as a scratch-build reference.
- The later `Big Budget VPin` series uses a flat-pack cabinet as the base and deliberately focuses on a higher-end build with more expensive displays, electronics and feedback hardware.

## Creator-provided companion files

The creator publishes downloadable cabinet configuration files on the South Delta Secondary School / Way of the Wrench resource page.

### Original generation

The older cabinet configuration uses a Teensy strip controller and defines addressable-lighting toys for:

- left side playfield
- right side playfield
- matrix
- speaker lighting
- under-cabinet lighting
- backbox lighting

This proves that addressable lighting was integrated as a cabinet-wide subsystem rather than a single decorative strip.

### Big Budget generation (September 2025 file)

The later published configuration uses a Wemos D1 Mini Pro-style strip controller setup and defines a more extensive layout including:

- 96 x 16 matrix definition
- right playfield strip: 134 LEDs
- left playfield strip: 134 LEDs
- backbox strip: 304 LEDs
- right speaker: 128 LEDs
- left speaker: 128 LEDs
- under-cabinet: 346 LEDs
- right magna-save: 4 LEDs
- flippers: 8 LEDs
- left magna-save: 4 LEDs

The exact physical implementation and electrical loading must still be checked against the videos and hardware documentation before reuse.

## Controller-board direction

Community discussion around the Big Budget series indicates use of Arnoz-family boards in the later build. A community schematic created specifically to mirror the Big Budget build mentions Walter/MOS8 and an alternate implementation using two Bunny Boards. This is useful as a map of the ecosystem, not as authoritative wiring documentation.

For our cabinet, controller choice remains open until we compare:

- Arnoz board stack
- Cleveland Software Design / PinOne ecosystem
- current DOF compatibility
- Linux/Windows software requirements
- Brazilian availability and replacement cost
- number and voltage/current class of intended toys

## Design lessons already applicable

1. Build the physical layout around verified component dimensions rather than nominal screen sizes.
2. Plan service access before finalizing cabinet openings; builders who lacked a sufficiently large rear opening lost the option for a sliding PC shelf.
3. Threaded inserts / machine-fastened modules are preferable for repeatedly serviced hardware.
4. Quick-disconnect connectors and labeling materially improve maintainability in a fully populated cabinet.
5. Separate and intentionally route power, controls, video/data and speaker wiring.
6. Addressable LEDs should be treated as a power/distribution subsystem, not merely decoration.
7. SSF exciter placement and mechanical toy placement should be reserved before electronics shelves consume the available wall/floor area.
8. High-end builds accumulate many boards and wires; modular removable panels/shelves are therefore a core requirement, not an aesthetic extra.
9. Mechanical feedback, SSF, shaker and knocker are all independently useful; our architecture should allow staged installation without rebuilding the cabinet.
10. Do not order the entire electronics BOM too early. Board ecosystems and component choices change; freeze each subsystem before purchasing it.

## Differences from our design

We will not directly reproduce either build. In particular:

- CNC-first joinery replaces hand-tool / pocket-hole-centric construction.
- Our playfield is an LG OLED42C5 in an independently supported VESA cradle.
- Service position uses dual gas struts plus independent mechanical safety support.
- PC is planned on a full-extension service drawer using an open-frame ATX chassis.
- Main audio must support independent Bluetooth `AUDIO ONLY` operation with the PC/screens/DOF powered down.
- Real Williams legs remain grounded during play; mobility uses retractable wheels.
- Electronics shelves must avoid stiffening SSF-critical cabinet-wall zones.
- High-current mechanical toys and isolated logic/audio electronics receive distinct mounting and wiring treatment.

## Next research passes

Research should now proceed only when each subsystem becomes relevant:

1. Playfield cradle / monitor mounting
2. Power distribution and branch protection
3. Main controller / plunger / nudge
4. DOF output boards and high-current switching
5. Mechanical toys and spatial placement
6. SSF / subwoofer / amplifiers
7. Addressable lighting and matrix
8. Cable raceways / connectors / labeling
9. Cooling
10. Software/front-end configuration

This staged method keeps research context and token use bounded while still using the complete series as a long-term design reference.

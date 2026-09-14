# Way of the Wrench research index

This folder tracks research from the two Way of the Wrench virtual-pinball build series selected as reference material for this cabinet.

## Playlists

### Original scratch / wallet-friendly cabinet build

- Playlist ID: `PLrqlHbqP7FIO5P8e8HtrBB01xqQtAWpJ5`
- Entry video supplied by project owner: `JxilHoceiNo`
- Role in this project: cabinet construction, dimensional/layout choices, practical build sequence, lessons learned, serviceability, wiring and baseline VPIN architecture.

### Big Budget VPin

- Playlist ID: `PLrqlHbqP7FINmGgJoszVvWOOyb8shdfUn`
- Entry video supplied by project owner: `iXeMTjJhAJQ`
- Role in this project: high-end flat-pack build, DOF/feedback toys, controller boards, addressable lighting, power distribution, wiring, cable management, serviceable modules and no-expense-spared hardware choices.

## Verified companion material

The creator's South Delta Secondary School / Way of the Wrench resource page publishes downloadable cabinet configuration files for both generations of the project. The original cabinet configuration includes Teensy-controlled addressable strips for left/right playfield, matrix, speakers, under-cabinet and backbox lighting. The September 2025 Big Budget cabinet configuration uses a Wemos D1 Mini Pro-style strip controller setup and defines a much larger addressable-lighting layout including a 96x16 matrix, left/right playfield strips, backbox, speaker, under-cabinet, magna-save and flipper lighting.

A Pinball Lunatics guide page independently identifies the later series as `Big Budget VPin`, describes it as a high-end build based on a flat-pack cabinet, and notes that it follows the earlier wallet-friendly build.

Community build logs repeatedly cite the original Way of the Wrench playlist as a primary cabinet-design/build reference. This makes the series useful not merely as inspiration but as a practical source whose decisions can be cross-checked against other VPIN builds and the Pinscape guide.

## Research method

Do not ingest every video in full into normal chat context. Research is subsystem-driven:

1. Cabinet / woodworking / dimensions
2. Playfield mounting and service access
3. Power, fusing, grounding and switching
4. Main controller / plunger / nudge / inputs
5. DOF output boards
6. Mechanical feedback toys
7. SSF and main audio
8. Addressable LEDs / matrix / flashers
9. Cable routing, connectorization and serviceability
10. PC / cooling / display layout
11. Software/frontend only where it affects hardware design

For each subsystem classify observations as:

- `ADOPT`: directly applicable
- `ADAPT`: useful concept but must be changed for our CNC/OLED/service design
- `REJECT`: inferior, obsolete, unsafe or incompatible with project goals
- `VERIFY`: needs a primary hardware manual or independent source before design use

## Project-specific differences to preserve

The Way of the Wrench designs are references, not masters. Our design intentionally differs in several areas:

- Williams WPC standard-body exterior geometry retained
- 18 mm metric plywood and CNC-first joinery
- LG OLED42C5 playfield
- hinged structural VESA cradle with dual gas struts and independent mechanical safety support
- open-frame ATX PC on a service drawer
- modular isolated electronics shelves and mechanically coupled feedback rails
- retractable wheels while retaining real pinball legs/levelers
- single external mains feed with branch distribution
- independent `AUDIO ONLY` Bluetooth mode
- USB/service bulkhead access
- fabrication targeted to Cutter CNC in Brazil

## Manufacturing caution

No hardware dimensions, wire gauges, fuse values, current capacities or safety-critical construction details from video content are accepted into the production design without cross-checking against manufacturer documentation and/or independent engineering references.

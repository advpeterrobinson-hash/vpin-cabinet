# Electrical / cable-routing architecture v0.11

Status: engineering provisional; not manufacturing-ready.

## Core rule

All major toys, display wiring, cooling, control wiring, and future expansion are accounted for **before** permanent CNC geometry is frozen. The cabinet must not become a box full of improvised loose cables.

The permanent design therefore includes:

- power domains;
- cable-routing classes;
- CNC-cut cable passages ("passports");
- CNC-located cable-support holes;
- folding-backbox service loops;
- replaceable raceways/panels;
- spare capacity for future toys.

## Backbox cooling

Use two quiet 120 mm 12 V PWM fans high on the rear wall as the baseline active-exhaust system. Low intake area is provided through the lower rear/bottom area and the main-cabinet-to-backbox passage.

The fans are **not** permanent motherboard-header loads. They run from a dedicated fused `AUX 12 V` cabinet bus. A standalone temperature/PWM controller controls speed so backbox cooling does not depend on Windows, USB, or motherboard firmware.

Operating behavior:

- FULL PINBALL: the 12 V cooling branch is available whenever the full cabinet is powered; thermostat/PWM controls speed.
- AUDIO ONLY: fans normally remain off unless later thermal testing shows that backbox-mounted audio electronics require airflow.
- Failure policy: when practical, choose a controller/fan arrangement whose failure state favors cooling rather than silent shutdown.

The backbox rear panel receives CNC-cut fan openings, grille holes and intake ventilation. Fan/service parts must remain removable after assembly.

## Power domains

### A — AC mains

AC mains stays in a dedicated route and enclosed distribution areas. It must not share cable raceways with USB, audio, Ethernet or low-level signals.

### B — high-current extra-low-voltage / DOF

The design reserves distributed DC power for inductive/mechanical devices such as contactors, shaker, gear motor, knocker, chimes/bells, blower, beacon/siren modules and strobes according to their final selected voltage.

Baseline distribution planning supports:

- 12 V auxiliary bus;
- optional 24 V auxiliary bus;
- individually fused high-current branches;
- flyback/suppression appropriate to the final output-controller hardware.

### C — logic/data/LED

USB, Ethernet, controller data, button input, LED data, and 5 V logic/addressable LED power are kept away from inductive/toy power where practical.

High-current 5 V addressable LED injection is treated as power distribution, not as a tiny signal wire.

### D — audio

Low-level analog audio is routed separately from motors, contactors, mains and switching power where practical.

### E — display service wiring

HDMI/DisplayPort and display power use dedicated service routes and loops so the hinged playfield and folding backbox can move without connector strain.

## Cable passages between cabinet and backbox

The fold hinge makes this the most critical harness area.

### Primary passport

Baseline clear opening: **90 x 50 mm rounded rectangle**, edge radius 8 mm.

Requirements:

- fully grommeted edge;
- removable split-gland or brush insert preferred;
- >=35% free area remaining after the initial harness is installed;
- 300 mm moving service loop;
- >=50 mm dynamic bend radius;
- positive cable support within 100 mm on both sides of the opening;
- position outside the hinge pinch keepout.

This passage carries normal backbox wiring such as display video/power, speakers/audio, USB/data, LED/data, cooling power and other low-voltage services.

### Secondary reserved passport

Provide a second covered opening, minimum **60 x 40 mm**, initially blanked with a removable cover.

This is intentional spare infrastructure for future topper power/data, a later high-current toy harness, replacement-standard cabling, or an additional display/control path.

The permanent cabinet should not have to be drilled years later merely because the original builder filled the first passage.

## Main-cabinet routing corridors

### Left-side low-voltage/data/audio route

Reserve roughly a 35 x 25 mm raceway envelope along the left wall for service controls, USB/data and audio. Use screw-mounted reusable clips or removable slotted raceway supports.

### Right-side DOF/DC-power route

Reserve roughly 45 x 30 mm on the right side for higher-current DC distribution to flippers, slings, bumpers and rear toy zones.

### Central display route

Reserve approximately 60 x 35 mm for playfield video and display-power service loops, clear of gas struts, the positive safety prop, hinge sweep and PC drawer.

### Mains route

Mains has its own enclosed/routed path from the rear power bay to protected distribution.

## Harness support standard

Cable management is part of the CNC design, not an afterthought.

The release should include CNC-located mounting holes for:

- rubber-lined P-clamps;
- reusable screw-mounted cable clips;
- removable slotted raceways;
- strain-relief brackets;
- harness anchors near every moving assembly.

Maximum support spacing guideline:

- fixed harness: 250 mm;
- moving/hinge harness: 100 mm near the moving zone.

Do not rely on adhesive-only tie bases for primary support. All wood/metal pass-throughs need edge protection.

## Toy inventory reserved in the layout

The physical zoning/routing design reserves capacity for the following before final BOM selection:

- impact/contactors for two flippers, two slings and bumper/effect channels (10-output class);
- shaker motor;
- gear motor;
- replay knocker;
- 3–5 chime/bell channels;
- wind/blower effect;
- strobe pair;
- five RGB flasher positions;
- rotating beacon / siren-light effect;
- addressable playfield-side, backbox and undercab lighting;
- illuminated cabinet buttons;
- future topper power/data and motor reserve.

This inventory is a **space, power and routing reservation**, not yet the final shopping list.

## Toy placement philosophy

- Front zone: flipper and sling impact devices, close to their physical event location.
- Mid cabinet: bumper effects, shaker and gear motor.
- Rear main cabinet: knocker/chimes/bells/siren-mechanical devices when cabinet-mounted, plus blower source if ducted forward.
- Backbox: flashers, strobes, beacon/siren lighting, addressable LEDs, optional knocker/bell/chime module, speakers, backglass display and cooling fans.
- Topper reserve: future powered/motorized topper and light effects.

Feedback devices should be mounted to structures that intentionally transmit their effect; electronics shelves and signal wiring should not become structural bridges that spoil SSF behavior.

## Quick-disconnect / service philosophy

Every major module should be removable without cutting wires.

- locking polarized connector families;
- current ratings chosen from the measured final load;
- both ends labeled;
- keyed connectors where misconnection could damage equipment;
- no high-current daisy chains through undersized connectors;
- accessible backbox-to-cabinet service disconnect for full backbox removal;
- normal 90-degree backbox folding must **not** require disconnecting the harness.

## CNC-flatpack implications

The eventual cutting package must include:

- primary and reserve backbox cable passports;
- fan openings/grilles/intakes;
- raceway/support holes;
- strain-relief bracket holes;
- electronics-panel mounting grids;
- route/zone references in assembly drawings;
- part and harness labels.

The builder should not have to decide where to drill cable holes after the cabinet is assembled.

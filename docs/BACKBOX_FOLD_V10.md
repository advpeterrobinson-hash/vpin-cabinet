# Backbox folding / transport mechanism v0.10

Status: engineering provisional; not manufacturing-ready.

## Purpose

The backbox must fold forward over the playfield for moving, storage, and transport. This is both authentic to later Williams/Bally-style pinball construction and highly useful for an apartment-buildable machine that may need to pass through doors, elevators, vehicles, and stairwells.

The design follows the WPC-style external side-pivot concept used in real machines and in the Way of the Wrench / flat-pack virtual-pinball ecosystem.

## Selected mechanism

Preferred baseline hardware:

- left/right WPC backbox hinge set: `01-9011-L/R`;
- cabinet pivot bushing: `02-4352`;
- black hinge pivot bolt: `4322-01139-12B`;
- two independent upright safety bolts through the backbox floor into captive threads in the cabinet rear shelf.

The standard hardware is preferred because it is proven, compact, replaceable, and does not require the apartment builder to fabricate a precision hinge.

A laser-cut local-fabrication alternative can be added later after the production geometry is physically validated. It must be a true alternative, not a required fabrication step.

## Main-cabinet pivot

Use the established WPC pivot location as the starting datum:

- pivot hole diameter: 12.7 mm (1/2 in);
- 38.1 mm (1.5 in) forward of the cabinet rear edge;
- 508.0 mm (20 in) above the cabinet bottom datum.

These locations must be CNC-drilled in the side panels. The builder should not have to erect the backbox, align hardware by eye, and hand-drill the cabinet.

## Adapting WPC hinges to our 580 / 780 mm widths

The selected main body is 580 mm wide and the future-proof backbox is 780 mm wide.

Pinscape documents the WPC hinge-floor inset for custom cabinet/backbox widths as:

`Inset = (Backbox width - Cabinet width - 2 3/8 in) / 2`

Using 60.325 mm for 2 3/8 in:

`(780 - 580 - 60.325) / 2 = 69.8375 mm`

Therefore the hinge mounting rows in the 780 mm backbox floor begin approximately **69.84 mm in from each side**. Exact hole spacing along each hinge will come from the purchased hinge or a verified drawing before CNC release.

The total backbox-over-main-body width difference is 200 mm, comfortably larger than the approximately 88.9 mm minimum difference cited for WPC-style hinge geometry.

## Upright operating position

The hinge must not be treated as the only thing holding the backbox upright.

Two dedicated safety/locking bolts clamp the backbox floor to the rear shelf/crossmember. Baseline is the proven 3/8-16 WPC approach:

- captive 3/8-16 T-nut or equivalent metal-backed captive thread in the cabinet shelf;
- approximately 11.9 mm shelf hole;
- approximately 25.4 mm clearance/access hole in the backbox floor;
- wing screw, large knob bolt, or socket-head fastener accessible from inside the backbox.

The final solution should place clamp load into a reinforced shelf/crossmember, not into unsupported plywood skin.

## Folded transport position

The backbox folds **forward over the playfield** by approximately 90 degrees.

The design must include a dedicated transport load path. The folded backbox is not allowed to rest on:

- the backglass/monitor;
- speaker cones or decorative speaker covers;
- the playfield OLED;
- the playfield glass;
- USB/HDMI connectors or cable harnesses.

The structural backbox frame will land on dedicated padded transport rests coupled to the main cabinet structure.

Targets:

- >= 15 mm nominal clearance to playfield glass;
- >= 10 mm clearance after expected pad compression;
- monitor/speaker/DMD surfaces recessed at least 8 mm behind the front transport datum where practical.

Any decorative speaker cover that projects beyond the fold datum must either be redesigned flush or made intentionally tool-less/removable. The preferred production design is **flush**, because requiring removal before every move is an avoidable failure mode.

## Folded-state retention

A folded backbox still needs positive retention during movement.

Baseline solution: a simple padded 25 mm cam-buckle strap with a documented strap path that cannot slide into the display or controls. This is inexpensive, globally available, and does not add complex exterior latches.

The assembly manual must state that the machine is **never transported with the backbox upright**.

## Cable harness / service loop

The hinge feature only works if the harness is designed to move with it.

Requirements:

- central cable opening aligned between cabinet shelf and backbox floor;
- minimum 250 mm service loop reserved initially;
- >= 50 mm dynamic bend radius target for the harness bundle;
- abrasion-resistant grommet/edge protection;
- strain relief at cabinet and backbox ends;
- no connector shell takes cable weight;
- keep moving harness at least 40 mm out of hinge/pinch zones;
- HDMI/video, backbox power, speaker/audio, USB, lighting and service wiring must all be included in the fold study.

The goal is to fold the backbox without disconnecting normal wiring.

## CNC-flatpack consequence

All precision geometry belongs in the files sent to the CNC shop:

- main-side pivot holes;
- backbox-floor hinge holes;
- cable openings;
- safety-bolt holes;
- transport-rest mounting holes;
- part labels/reference marks.

No step in normal cabinet assembly should say “place the backbox approximately here and drill to match.”

## Next CAD step

After v0.9 is locally validated, add a v0.10 FreeCAD assembly state containing:

1. upright backbox envelope;
2. 15/30/45/60/75/90 degree fold ghosts;
3. WPC hinge-axis envelope;
4. cable-loop keepout;
5. transport-rest pads;
6. folded transport envelope;
7. collision checks against playfield glass, OLED service cradle, lockdown bar, rear I/O and speaker/backglass fascia.

The exact hinge bracket solid should be derived from purchased/measured hardware or a verified fabrication drawing rather than guessed from photographs.

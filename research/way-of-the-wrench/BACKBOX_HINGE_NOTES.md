# Way of the Wrench / WPC folding-backbox research notes

Research status: distilled engineering notes; not a transcript.

## Way of the Wrench relevance

The Big Budget VPin series includes a flat-pack cabinet build and dedicated backbox installation stages. Public playlist indexing identifies:

- Episode 2: **How to build a flatpack vpin cabinet**
- Episode 9: **Virtual Pinball: How to install your back box monitors & doors!**

The surrounding Way of the Wrench community discussion also confirms that his Big Budget machine is intended to retain a fold-down backbox. A later discussion about custom speaker covers notes that the covers would have to be removed before folding because they protrude beyond the backbox face. That is a useful negative design lesson for this project: our permanent speaker/front fascia should stay inside a defined fold/transport datum where possible.

## Mechanism confirmed by independent cabinet builds

A build explicitly citing Way of the Wrench as a primary reference describes side-mounted backbox hinges that let the backbox fold onto the cabinet for transport, with two internal bolts installed in the upright position to clamp/secure the backbox.

This aligns with normal Bally/Williams WPC practice.

## WPC hardware family

Common replaceable parts:

- `01-9011-L/R` — Bally/Williams WPC left/right backbox hinge set
- `02-4352` — cabinet hinge pivot bushing / sleeve nut
- `4322-01139-12B` — black backbox hinge pivot bolt

The hinge pivot is made through a 1/2-inch cabinet-side hole. The hinge set rotates around the pivot bushing/bolt and the backbox is separately locked upright with safety bolts through the backbox floor into the rear shelf.

## WPC pivot datum

Open WPC cabinet plans give the cabinet-side pivot at approximately:

- 20 in / 508.0 mm above the cabinet bottom datum
- 1.5 in / 38.1 mm forward of the rear edge
- 1/2 in / 12.7 mm hole

These are appropriate starting values because our cabinet retains the WPC side length and rear height while only changing overall width.

## Custom width adaptation

Pinscape documents a width-adaptation formula for WPC hinge mounting holes in the backbox floor:

`Inset = (Backbox Width - Cabinet Width - 2 3/8 in) / 2`

For this project:

- backbox width = 780 mm
- cabinet width = 580 mm
- 2 3/8 in = 60.325 mm
- hinge row inset = **69.8375 mm from each backbox-floor side edge**

Pinscape also notes that a WPC-style backbox should be at least about 3.5 in / 88.9 mm wider than the cabinet for this hinge arrangement. Our width difference is 200 mm, so the selected proportions provide ample lateral allowance.

## Upright safety locking

Pinscape documents two 3/8-16 captive T-nuts in the cabinet rear shelf and matching access holes in the backbox floor. Wing screws secure the backbox upright.

The safety principle is important: **do not rely on the hinge alone to hold the backbox in operating position.**

## Transport rule

Original machine instructions explicitly warn against transporting with the hinged backbox erect. The backbox is lowered forward onto the main cabinet with protective material and then retained for transport.

Our design should improve on the improvised-protective-material approach by providing dedicated structural transport rests plus a documented padded strap path.

## Design adaptations for our CNC-flatpack platform

Adopt:

- proven WPC side-pivot hinge family;
- CNC-located cabinet pivot holes;
- CNC-located backbox hinge holes using the custom-width formula;
- two independent upright safety bolts;
- central cable opening and deliberate fold service loop;
- dedicated transport rests carrying the load through the backbox frame;
- positive folded-state retention.

Adapt:

- 580 mm main body / 780 mm backbox dimensions;
- future-proof monitor carrier and removable bezel;
- flush/recessed speaker fascia so folding does not require decorative-part removal;
- harness routing for HDMI, USB, audio, addressable lighting and power rather than original pinball wiring alone.

Reject:

- hand-drilling hinge locations after assembly as the normal release workflow;
- transporting with the backbox upright;
- letting folded backbox weight land on monitor, speaker grilles, playfield glass or OLED;
- protruding permanent speaker covers that must be unscrewed before every fold.

## Public references used

- Way of the Wrench Big Budget playlist index: Pinball Lunatics
- Way of the Wrench Big Budget speaker-cover discussion: r/virtualpinball
- Pinscape Build Guide V2 — cabinet body/backbox floor/rear shelf sections
- jonaskello/wpc-cabinet — WPC standard-body cabinet plans
- Marco Specialties / VirtuaPin — WPC hinge hardware identification
- Freelance Soundlabs virtual pinball build — Way of the Wrench-referenced folding hinge implementation

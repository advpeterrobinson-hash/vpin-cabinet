# Way of the Wrench / community toy and routing notes

These are distilled design notes, not verbatim transcripts.

The Way of the Wrench cabinet series is being used as a practical reference for the physical complexity of full-DOF builds. The project therefore reserves space/routes before the toy BOM is finalized rather than treating feedback devices as late additions.

Cross-checked common full-cabinet toy classes include:

- flipper/slings/bumper impact outputs;
- RGB flashers and strobes;
- beacon/siren-style visual effect;
- shaker;
- gear motor;
- replay knocker;
- fan/blower effect;
- chimes/bells;
- addressable lighting;
- illuminated cabinet buttons.

Backbox-specific planning must account for the backglass display, speakers, lighting, optional knocker/chime/bell hardware, flashers/strobes/beacon effects, ventilation fans and the moving harness required by the fold-down backbox.

The project adapts this ecosystem around a structured power/routing architecture:

- dedicated 12 V cabinet auxiliary bus for cooling and suitable 12 V toys;
- optional 24 V domain for selected inductive hardware;
- separate high-current DOF and low-level audio/data routing;
- dual backbox cable passages with spare capacity;
- CNC-located cable supports and raceways;
- normal backbox folding without unplugging the main harness.

The specific controller-board ecosystem and exact toy voltages remain BOM-stage decisions.

# Playfield Service v0.4

Status: **engineering provisional — not for manufacturing or gas-strut purchase**.

## Objective

Create the first explicit kinematic model for the LG OLED42C5 playfield service system while preserving the Williams WPC standard-body external cabinet dimensions.

The v0.4 model is intentionally a packaging model. It answers whether the intended service concept can fit before detailed brackets, VESA plates, hinges, strut hardware, cable chains, or CNC pockets are finalized.

## Fixed inputs

- LG OLED42C5 physical envelope: 932 x 540 x 41.1 mm.
- OLED mass: 9.8 kg.
- Williams WPC cabinet baseline: 558.8 mm external width, 1308.1 mm side length, 400.05 mm front height, 596.9 mm rear height, 180.975 mm rear top flat.
- Nominal plywood: 18 mm.
- OLED installed cross-width target: 542 mm.
- Nominal OLED pocket depth: 9.6 mm/side.
- Nominal remaining outer side skin: 8.4 mm.
- Service opening target: 70 degrees relative to the closed playfield position.
- Dual gas struts plus an independent positive mechanical safety support are mandatory.

## Provisional assumptions introduced in v0.4

These are deliberately isolated in `config/playfield_v04.json` so they can change without corrupting the validated cabinet baseline.

- OLED front setback: 44.4 mm, based on the reference-build packaging position.
- Glass clearance normal to the playfield: 12 mm.
- Cradle mass estimate: 3.0 kg in addition to the 9.8 kg OLED.
- Cradle packaging rails: 20 x 20 mm envelopes.
- Hinge axis: 35 mm behind the OLED rear edge along the playfield slope.
- Hinge axis diameter envelope: 12 mm.
- First-pass gas-strut moving attachment: 400 mm forward of hinge.
- First-pass fixed attachment: 50 mm forward and 100 mm below hinge.
- First-pass gas-strut candidate: 300 N each, two struts.

None of those values are frozen hardware selections.

## Gas-strut calculation philosophy

The solver uses a 2D Y/Z side-view mechanism. It calculates:

- closed and open strut lengths;
- required stroke;
- effective moment arm;
- estimated force per strut required to balance the estimated OLED + cradle mass in the closed position;
- open-position assist/gravity ratio.

The model uses an approximate combined center of gravity at the OLED longitudinal midpoint. Actual cradle mass and center of gravity must replace this assumption before selecting struts.

The current candidate is expected to be in the neighborhood of a 300 N gas spring with roughly 125 mm stroke and ~345/471 mm closed/open pin-to-pin geometry, but catalog availability and bracket geometry have not been checked yet.

## FreeCAD objects generated

`tools/build_playfield_v04.py` adds a group named:

`PLAYFIELD SERVICE v0.4 - PROVISIONAL`

containing:

- LG OLED42C5 closed envelope;
- OLED 70-degree service-position ghost;
- hinge-axis envelope;
- provisional closed cradle rails;
- open cradle ghost;
- left/right gas-strut closed candidates;
- left/right gas-strut open ghosts.

The script is safe to rerun and removes only the group it owns.

## Validation gate before v0.5

Before this branch can be considered a validated engineering checkpoint:

1. `tools/validate.py` must still pass the cabinet/OLED baseline.
2. `tools/solve_playfield_struts.py` must pass its broad packaging guards.
3. `freecadcmd tools/build_playfield_v04.py` must complete without fatal errors.
4. The generated FreeCAD document must open and show the OLED/cradle opening toward the service position rather than through the cabinet floor.
5. The hinge location and open envelope must look mechanically plausible relative to the cabinet rear.
6. No gas strut may be purchased yet.

## Next stage after validation

v0.5 will refine the cradle into actual structural members and bracket interfaces, establish the independent safety prop/lock, and begin collision sweeps against the backbox/service envelope. Exact VESA hole placement waits for an LG mechanical drawing or physical measurement rather than being invented.

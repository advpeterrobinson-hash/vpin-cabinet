# Playfield Service v0.5 — Sweep, Backbox Keepout, and Positive Safety

## Purpose

v0.5 turns the successful v0.4 hinge concept into a more useful serviceability
model. It remains an engineering packaging stage and is **not** approved for
manufacturing.

## Added in v0.5

- OLED sweep ghosts at 0, 10, 20, 30, 40, 50, 60, and 70 degrees.
- Conservative backbox keepout envelope based on reference-model dimensions.
- Automated sweep-vs-backbox intersection checks.
- Rear hinge reinforcement/crossmember envelope tied to full-thickness cabinet regions.
- VESA carrier adjustment zone without invented hole locations.
- Independent positive mechanical safety-prop packaging candidate.
- Candidate gas-strut comparison at 250 N, 275 N, and 300 N per side.
- Headless verification of generated solids and collision state.

## Important limitations

### Backbox

The backbox *dimensions* originate from the audited reference model, but its
placement in v0.5 is intentionally conservative/provisional. Before final CAD,
we must either extract the actual reference placement or lock the exact
backbox/hinge hardware we will use.

### VESA

The LG C5 VESA pattern is known as 300 x 200 mm, but its chassis-relative centre
is not assumed. v0.5 therefore shows an adjustment zone only. No manufacturing
hole locations are generated.

### Gas struts

250/275/300 N are analytical candidates, not a shopping list. Final selection
requires actual cradle mass, actual combined centre of gravity, hinge bracket
geometry, available commercial lengths/strokes, and a practical safety margin.

### Safety prop

The v0.5 prop is a packaging envelope for an independent positive mechanical
support. The final device should be captive, easy to engage during service,
and mechanically able to hold the assembly even if both gas struts fail.
Possible final implementations include a pinned prop bar or a purpose-built
locking lid stay. The v0.5 model does not approve material section or pin size.

## Local validation

```bash
cd ~/Projetos/vpin-cabinet
git fetch origin
git switch feat/playfield-v05
git pull
bash tools/run_playfield_v05.sh
```

Successful output must include:

- baseline validation passes;
- v0.5 sweep/safety solver passes;
- v0.4 base geometry regenerates;
- v0.5 geometry generates;
- all sweep states clear the provisional backbox keepout;
- safety-prop envelope is within the initial packaging range;
- headless FreeCAD verification passes.

After that, open `cad/master/vpin-master.FCStd` and inspect the group:

`PLAYFIELD SERVICE v0.5 - SWEEP / SAFETY`

## Merge gate

Do not merge v0.5 if the local runner fails. Visual inspection should confirm
that the sweep ghosts form a plausible upward service arc, the backbox keepout
is behind the playfield, and the safety prop spans from a cabinet-side fixed
point to the raised cradle without obviously crossing the OLED body.

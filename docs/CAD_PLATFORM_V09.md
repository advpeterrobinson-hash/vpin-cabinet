# CAD platform v0.9 — 580 mm body + engraved service bays

Status: engineering migration; not manufacturing-ready.

## Purpose

Move the FreeCAD master from the historical 558.8 mm Williams reference width to the selected 580 mm CNC-flatpack platform while preserving the previously validated cabinet profile and playfield-service mechanics.

This stage also adds physical packaging envelopes for the rear removable power and service-I/O fascias defined in v0.8.

## What changes

- `CabOuterWidth`: 558.8 mm reference -> **580.0 mm selected platform**
- nominal 18 mm plywood gives **544.0 mm internal width**
- the current LG C5 542 mm installed/clearance envelope now fits without routing a side pocket
- future playfield target remains 560 mm chassis width + 2 mm clearance per side
- a future 564 mm cavity can still be achieved by routing 10 mm into each 18 mm side, leaving the required 8 mm outer skin
- existing front, rear, bottom, and right-side geometry should resize automatically because they are expression-driven
- frozen playfield-service packaging is rebuilt against the new design baseline

## Rear service-bay CAD packaging

The rear now receives packaging envelopes for:

- 170 × 120 mm removable `AC MAINS` wood fascia
- 255 × 120 mm removable service-I/O fascia
- 150 × 100 mm power cabinet-window ghost
- 235 × 100 mm low-voltage service-window ghost
- 3 mm replaceable connector carrier
- provisional 140 mm-deep enclosed mains-compartment envelope

The fascia gap is 85 mm.

These are **not final cut files**. The windows are ghost solids used to establish location and clearance. Later CNC stages will turn them into true rear-panel through-cuts with dogbones/radii and mounting holes appropriate to Cutter CNC tooling.

## Vintage engraving

The fascia faces remain standalone parts so their legends can be CNC engraved and white-filled independently of the main rear panel. Release geometry will ultimately provide a dedicated `ENGRAVE_WHITE` layer with text converted to curves.

## Local validation

Run:

```bash
cd ~/Projetos/vpin-cabinet
git fetch origin
git switch feat/cad-platform-v09
git pull
bash tools/run_platform_v09.sh
```

The runner:

1. executes pure-Python design/packaging validation;
2. changes the FreeCAD master spreadsheet to 580 mm;
3. rebuilds v0.4/v0.5 playfield-service geometry;
4. adds v0.9 rear service-I/O packaging;
5. verifies shell resizing, OLED fit, service-bay geometry, and playfield sweep.

Open the result with:

```bash
freecad cad/master/vpin-master.FCStd
```

Expected tree addition:

`SERVICE I/O v0.9 - VINTAGE ENGRAVED FASCIAS`

## Manufacturing gate

This stage does not authorize CNC production. Remaining gates include actual joinery, material-thickness measurement, provider tool/radius confirmation, port-carrier hardware selection, electrical-enclosure design, tolerance coupon, fastener access, and final assembly validation.

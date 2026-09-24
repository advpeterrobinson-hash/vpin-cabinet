# CNC Flat-Pack Build Philosophy

> Current owner baseline: [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md). Older assist/stay descriptions below are historical; no assist hardware blocks current CNC. Use the active hardware/feature registers for procurement.

## Primary project objective

The project is not only a one-off virtual pinball cabinet. It is intended to become a reproducible **CNC-first flat-pack cabinet system**.

A builder should be able to:

1. download the released plan package;
2. take the CNC files and material schedule to a local fabrication shop;
3. receive labeled, machined parts;
4. assemble, finish, wire, and commission the cabinet in an apartment or ordinary room;
5. do so without owning expensive woodworking or metalworking machinery.

The design should therefore move precision work from the builder to CAD/CAM and the fabrication shop.

## What the CNC shop should do

Where practical, the CNC package should include all repeatable woodworking operations:

- exterior panel profiles;
- through-cuts;
- dados and rabbets;
- tab/slot alignment geometry;
- pockets for display clearance and hardware;
- speaker, fan, button, coin-door and service openings;
- pilot/reference holes;
- threaded-insert/T-nut locations where appropriate;
- cable-pass openings;
- ventilation geometry;
- removable electronics-panel interfaces;
- PC-drawer mounting references;
- labels/part IDs or engraving marks where useful;
- test coupon for actual material thickness and fit.

Dogbone/T-bone relief and other router-specific geometry should be generated from confirmed provider tooling rather than improvised by the builder.

## What the builder should need

Target ordinary tools only:

- drill/driver;
- screwdrivers / hex keys;
- clamps;
- rubber mallet;
- wood glue;
- measuring tape / square;
- basic sanding and painting supplies;
- wire tools for electrical assembly.

A build step that requires a table saw, router table, precision handheld routing, drill press, welder, planer, or similar equipment should be treated as a design smell unless there is no practical outsourced/CNC alternative.

## Joinery strategy

Prefer joinery that is self-locating and forgiving:

- dados;
- rabbets;
- tabs and slots;
- captured shoulders;
- keyed left/right geometry;
- CNC-located fastener holes.

Avoid requiring the builder to establish critical dimensions by measuring from an edge with a tape measure.

The cabinet should naturally square itself during dry assembly as much as practical.

## Electronics and future replacement

Permanent cabinetry should not be tied to one generation of electronics.

Use broad service envelopes and replaceable interfaces:

- playfield TV: structural cradle + replaceable VESA/adapter plate + removable fillers;
- backglass: replaceable monitor carrier + replaceable bezel/filler panel;
- PC: fixed drawer infrastructure + replaceable chassis adapter plate;
- controllers/amplifiers/PSUs: removable electronics panels or grid/slot mounting;
- external ports: replaceable I/O panel;
- DMD/speaker area: replaceable module/panel.

Replacing electronics should normally require a new adapter/filler part, not destructive modification of the permanent cabinet.

## Metal parts

Custom metalwork is acceptable if it can also be outsourced from drawings.

Examples:

- custom-width lockdown bar;
- siderails;
- hinge brackets;
- gas-strut brackets;
- PC drawer brackets;
- wheel/retractable-caster mechanisms;
- service/I/O panels.

Where practical, provide DXF plus dimensioned PDF and fabrication notes so a local laser-cutting/bending/welding shop can reproduce the part.

The builder should not be expected to own metalworking machinery.

## Release package goal

A mature release should contain at least:

```text
release/
├── README-FIRST.pdf
├── BOM.xlsx
├── materials.pdf
├── assembly-manual.pdf
├── cnc/
│   ├── 18mm-sheet-01.dxf
│   ├── 18mm-sheet-02.dxf
│   ├── 12mm-sheet-01.dxf
│   ├── tolerance-coupon.dxf
│   └── layer-conventions.pdf
├── drawings/
│   ├── cabinet.pdf
│   ├── backbox.pdf
│   ├── playfield-cradle.pdf
│   └── electronics-layout.pdf
├── metal/
│   ├── lockdown-bar.dxf
│   ├── lockdown-bar.pdf
│   ├── hinge-brackets.dxf
│   └── hinge-brackets.pdf
└── config/
    └── design-baseline.json
```

The exact structure may evolve, but the final user should not need FreeCAD merely to build the cabinet.

## Design priority order

When objectives conflict, use this order unless safety requires otherwise:

1. safety;
2. reproducibility;
3. CNC manufacturability;
4. easy assembly with ordinary tools;
5. serviceability and future electronics replacement;
6. force-feedback/audio performance;
7. authentic Williams visual character;
8. millimetre-perfect historical dimensions.

This means a small dimensional deviation is desirable when it materially simplifies fabrication, strengthens the structure, improves replacement tolerance, or eliminates specialist-tool work at home.

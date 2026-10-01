# Backbox hinge shopping guide

Status: procurement reference. Final CNC hole locations remain subject to physical-hardware measurement and FreeCAD validation.

## Selected architecture

Use Williams/Bally WPC-style external side hinges so the 780 mm backbox folds forward over the 600 mm main cabinet for transport.

### Core hinge hardware

| ID | OEM / common part number | Qty | Description | Procurement class |
|---|---|---:|---|---|
| BB-HNG-01 | 01-9011-L | 1 | Left WPC backbox hinge bracket | Prefer OEM/reproduction import |
| BB-HNG-02 | 01-9011-R | 1 | Right WPC backbox hinge bracket | Prefer OEM/reproduction import |
| BB-HNG-03 | 02-4352 | 2 | Cabinet pivot bushing / hex-socket T-nut, 3/8-16 | Matched purchased family; measure actual assembly |
| BB-HNG-04 | 4322-01139-12B | 2 | Special 3/8-16 x 3/4 in short-neck black carriage bolt | Import preferred |

The hinge brackets are also commonly sold as set **01-9011-LR**.

## Historical price snapshot — September 2026 (not current quotation)

Prices below are product prices only and do **not** include international freight, Brazilian import tax, ICMS, courier fees or exchange-rate movement.

- Marco Specialties: `01-9011-LR` hinge set listed in stock at **US$49.99**.
- VirtuaPin: Williams/Bally black hinge set (`01-9011-R_01-9011-L`) listed at **US$29.95**.
- Marco Specialties: `02-4352` pivot bushing listed in stock at **US$2.99 each**.
- Pinball Life: `02-4352` pivot bushing listed at **US$2.95 each**.
- Marco Specialties: `4322-01139-12B` pivot bolt listed in stock at **US$1.29 each**.
- VirtuaPin: `4322-01139-12B` listed at **US$0.99 each**.

Search terms for eBay / Brazilian marketplaces:

- `Williams Bally WPC backbox hinge 01-9011-LR`
- `01-9011-L pinball hinge`
- `01-9011-R pinball hinge`
- `02-4352 pivot bushing`
- `4322-01139-12B hinge bolt`
- `Williams WPC backbox hinge set`

Do not substitute visually similar Stern hinge hardware without checking pivot geometry and thread dimensions.

## Upright locking hardware

The hinges allow folding; they are **not** the sole upright restraint.

The backbox floor rests on the main-cabinet rear shelf and is clamped down with two locking bolts into captive threads in the shelf.

Current baseline:

| ID | Qty | Item | Notes |
|---|---:|---|---|
| BB-LCK-01 | 2 | 3/8-16 captive thread / T-nut or metal-backed insert | Under rear shelf/crossmember |
| BB-LCK-02 | 2 | 3/8-16 hand-accessible lock bolt / wing screw / knob bolt | Final length after shelf+floor stack measured |
| BB-LCK-03 | 2 | large washer / load spreader as required | Prevent local crushing |

The exact locking-bolt length is deliberately **TBD** until the real shelf, gasket and backbox-floor stack are measured.

## CNC / measurement rule

Before production CNC files are released:

1. Purchase and measure the actual hinge set, both pivot bushings and both pivot bolts before CNC.
2. Measure bracket hole centers, material thickness, bend offsets and pivot-to-floor relationship.
3. Compare the measured parts with the engineering model.
4. Cut a scrap hinge-location test piece if necessary.
5. Only then freeze the cabinet pivot hole and backbox-floor mounting holes.

This preserves the project's CNC-flatpack goal: builders should receive correctly located holes and bolt the hinge on without hand layout.

## Current hardware boundary

Use the purchased WPC family. No custom hinge metal or substitute hinge architecture is introduced by this datum cleanup.

The release package should ultimately contain:

- verified hinge installation drawing;
- left/right orientation diagram;
- cabinet pivot-hole datum;
- backbox-floor hole pattern;
- locking-bolt/shelf alignment drawing;
- torque/assembly notes;
- folded and upright inspection checklist.

CURRENT V32 measurement hold: use 600 mm cabinet / 780 mm backbox and 59.8375 mm floor-row inset from each OUTER side edge. Three Ø6.35 mm reference holes per side, 44.45 mm reference pitch, row approximately 12.7 mm from rear. None is a frozen purchased-bracket pattern. Listings for 02-4352 conflict: bushing body length, exact bracket holes/bend offsets and final CNC hinge drilling remain null until the physical 01-9011-L/R + 2 × 02-4352 + 2 × 4322-01139-12B assembly is measured. Purchase/measure early (HF-006 in MEASURE_BEFORE_CNC_V25.csv); no intermediate cabinet prototype is planned. No new/custom hinge metal is authorized.

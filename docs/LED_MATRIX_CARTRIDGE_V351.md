# V35.1 — Removable LED Matrix Cartridge

Status: **functional architecture accepted; detailed geometry pending selected LED hardware**.

## Owner-selected architecture

The LED matrix is treated as a removable cartridge, not as electronics permanently built into the cabinet.

Stack, rear to front:

1. **Rear acrylic backing** — mechanical backing/protection.
2. **Opaque index acrylic** — perforated to locate/center each LED and reduce lateral light bleed.
3. **Front diffuser acrylic** — optical face.

The three sheets slide into separate grooves in two **3D-printed side end caps**. Each end cap is attached to the cabinet with **two fasteners**, for **four cabinet fasteners total**.

Routine service target:

**disconnect one connector → remove four fasteners → withdraw complete cartridge → remove/slide end caps → separate the three acrylic layers.**

No acrylic sheet should need its own routine mounting screws.

## Why the layers remain separate

The index layer and diffuser perform different jobs. The index layer controls LED position and cell-to-cell spill. The diffuser needs a deliberate optical gap from the emitters. The end-cap geometry therefore provides independent tracks rather than simply clamping three sheets into one solid stack.

The diffuser gap remains **NULL until optical prototype testing**. It is not safe to infer a universal spacing from another cabinet.

## Interface with V35.1

Current V35.1 contains the removable plywood **M030 / P041 MatrixCarrier**, approximately **540 × 95.375 mm**. It remains the manufacturing authority until the new cartridge passes CAD/service validation.

The cartridge proposal must fit the accepted matrix service region and may ultimately:

- replace M030;
- reuse M030 only as a datum/backing support; or
- coexist with it if that proves mechanically simpler.

No deletion is authorized merely by creating this document.

Permanent cabinet wood should contain only the **generic cartridge interface**. LED pitch, LED-hole pattern and PCB-specific geometry belong to replaceable acrylic/printed parts.

## End caps

Each printed end cap should ultimately provide:

- three independent acrylic tracks;
- positive longitudinal stop;
- controlled lateral clearance for acrylic expansion;
- two cabinet mounting points;
- wire exit/service-loop routing;
- strain-relief feature;
- optional keyed connector retention;
- no trapped loose nut during normal service where practical.

Preferred printable material: **PETG or ASA**. PLA is not the baseline because the module contains heat-producing electronics and may remain installed for long periods.

## Still intentionally NULL

Until the actual LED hardware is selected:

- LED pitch;
- LED count;
- LED package dimensions;
- index-hole diameter/shape;
- acrylic thicknesses;
- diffuser-to-LED spacing;
- cartridge overall depth;
- exact 4-screw cabinet pattern;
- connector family.

## Validation sequence

1. Select and measure the real LED matrix hardware.
2. Prototype the optical stack on a short section.
3. Select diffuser gap by hotspot/brightness test.
4. Model both printed end caps.
5. Check complete cartridge against current matrix keepouts and service/fold states.
6. Decide whether M030 is retained or retired.
7. Only then release acrylic cutting files and printable end-cap files.

This architecture intentionally borrows only the **service principle** of a removable layered cartridge; no third-party dimensions or proprietary geometry are imported.

# V35.1 — Removable LED Matrix Cartridge

Status: **functional architecture accepted; Cleveland Software Design 6-panel kit selected as the hardware target. Final acrylic/end-cap geometry remains pending physical measurement of the actual panel assembly.**

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

## Selected LED hardware

Target kit: **Cleveland Software Design — Addressable LED Plug and Play Kit**.

For V35.1 use the **6-panel matrix configuration**:

- 6 × addressable matrix panels;
- each panel is published as **3.125 in square** (79.375 mm nominal);
- 256 LEDs per panel, yielding **1536 matrix LEDs**;
- 2 side strips with **144 LEDs each** (288 total);
- controller: S2 Wemos-based 10-output ALED controller;
- supplied 5 V / 15 A power supply;
- right strip on output 1, left strip on output 2, matrix panels on outputs 3–8.

A 16 × 16 LED grid per panel is implied by 256 LEDs/panel; this must still be confirmed against the physical panel before releasing the index plate.

The vendor also describes the complete 6-panel matrix as approximately **18.5 in** long (~469.9 mm). Six nominal 3.125 in panels arithmetically total 18.75 in (476.25 mm). This discrepancy is small and does not threaten the current 540 mm carrier envelope, but **we will not guess which value controls manufacturing**. Measure one real panel and the assembled six-panel width before finalizing acrylics/end caps.

## Still intentionally NULL

Until the physical kit is measured:

- actual assembled six-panel width;
- actual PCB thickness and spacer stack;
- connector projection and wire-exit envelope;
- exact LED package diameter/height;
- index-hole diameter/shape;
- acrylic thicknesses;
- diffuser-to-LED spacing;
- cartridge overall depth;
- exact 4-screw cabinet pattern;
- connector family.

## Validation sequence

1. Measure one Cleveland panel, the complete six-panel assembly, connector projections and supplied spacer stack.
2. Prototype the optical stack on a short section.
3. Select diffuser gap by hotspot/brightness test.
4. Model both printed end caps.
5. Check complete cartridge against current matrix keepouts and service/fold states.
6. Decide whether M030 is retained or retired.
7. Only then release acrylic cutting files and printable end-cap files.

This architecture intentionally borrows only the **service principle** of a removable layered cartridge; no third-party dimensions or proprietary geometry are imported.

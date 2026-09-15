# Service I/O v0.8 — vintage engraved rear panels

Status: engineering provisional; not manufacturing-ready.

## Design intent

The external I/O should look like part of the cabinet rather than like a PC case. The chosen visual language is inspired by older hi-fi receivers, amplifiers, laboratory equipment, and arcade hardware: dark wood/black surfaces with small white legends, borders, scales, and connector names.

The cabinet is still a CNC-flatpack project, so the appearance must not depend on difficult hand fabrication. Precision openings and engraving belong in the CNC package; the builder should only need finishing, simple paint fill, and ordinary screw assembly.

## Core construction rule

Do **not** cut today's USB/HDMI/RJ45 connector shapes directly into permanent cabinet structure.

Instead use:

1. one simple rectangular CNC opening in the permanent rear panel;
2. a removable CNC-cut decorative wood fascia;
3. a thin replaceable connector carrier behind the fascia;
4. panel-mount pass-through connectors on the carrier;
5. CNC-engraved white-filled legends on the fascia.

If interface standards change later, the owner replaces the small fascia/carrier assembly rather than modifying the cabinet.

## Rear layout

Viewed from behind the 580 mm cabinet:

```text
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                        REAR                              │
│                                                          │
│                                                          │
│   ┌────────────────┐        ┌────────────────────────┐   │
│   │    AC MAINS    │        │        SERVICE         │   │
│   │                │        │                        │   │
│   │ inlet / cord   │        │ NETWORK   HDMI         │   │
│   │ disconnect     │        │ USB-A     USB-C        │   │
│   │                │        │ RESERVE                │   │
│   └────────────────┘        └────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Power fascia

- 170 × 120 mm removable decorative fascia
- 35 mm from cabinet left edge
- 40 mm above cabinet bottom
- cabinet window: 150 × 100 mm
- internal enclosed mains compartment mandatory
- engraved legends: `AC MAINS` and `MASTER DISCONNECT`

The wood fascia is decorative/mechanical only. It is **not** relied upon as the mains-voltage safety enclosure.

### Service I/O fascia

- 255 × 120 mm removable fascia
- 35 mm from cabinet right edge
- 40 mm above cabinet bottom
- cabinet window: 235 × 100 mm
- thin 3 mm replaceable connector carrier behind it

Initial ports:

- `NETWORK` — RJ45 Ethernet
- `SERVICE DISPLAY` — HDMI diagnostic output
- `USB SERVICE` — USB-A
- `USB-C` — USB-C data/service
- `RESERVE` — blank standardized position

The 85 mm gap between the two fascia envelopes is deliberate. Mains and low-voltage/data wiring remain separated internally.

## Why the service-display HDMI exists

The rear HDMI jack is not for normal gameplay. It is an emergency/service video path. If the playfield display or its mounting system is unavailable years later, a normal monitor can be plugged into the cabinet without dismantling the playfield assembly merely to troubleshoot the PC.

## Coin-door service panel

A hidden panel inside the coin door provides frequently needed technician access without opening the playfield:

- USB-A ×2
- USB-C ×1
- 3.5 mm AUX IN
- DOF / mechanical-feedback `SERVICE DISABLE`
- PC `POWER`
- PC `RESET`

Header engraving: `CABINET SERVICE`.

The feedback-disable control must act on the mechanical-feedback enable path independently of ordinary software control.

## Hidden front controls

A small panel under the front edge, hidden from normal standing view, carries:

- hardware master-volume knob
- three-position `OFF / AUDIO / PINBALL` selector
- `BLUETOOTH PAIR` button
- optional `USB-C CHARGE`

The volume knob gets a simple white engraved scale/tick ring in the same visual style as vintage audio equipment.

## Engraving specification

Target appearance:

- dark satin black or very dark brown wood finish;
- shallow CNC engraving;
- white enamel/paint fill;
- uppercase geometric sans-serif legends;
- simple rectangular separator lines and volume tick marks;
- no decorative clutter that makes service labels harder to read.

Engineering starting point:

- 0.6 mm nominal engraving depth;
- 0.6 mm minimum visible stroke;
- 60-degree V-bit preferred;
- text converted to curves/outlines in released fabrication files.

If a CNC provider cannot V-engrave, the release may also contain a 1 mm end-mill engraving layer or laser-engraving alternative. The geometry, labels, and layer names should remain the same.

White filling is intentionally a low-tool operation: enamel, model paint, paint marker, or another durable white infill can be applied after the dark finish and wiped/sanded back as appropriate to the finishing system.

## Panel standardization

Where practical, use standardized panel-mount/pass-through connector footprints on the thin carrier rather than permanently committing the wooden fascia to one connector brand. Candidate families include standardized circular/D-series-style mounting or keystone/pass-through modules, but the final connector family remains a BOM-stage decision.

The permanent cabinet should only know the **service-bay rectangle and mounting-hole pattern**.

## CNC release requirements

The eventual CNC package should expose separate layers/operations for:

- `CUT_THROUGH`
- `POCKET`
- `DRILL`
- `ENGRAVE_WHITE`
- `REFERENCE_DO_NOT_CUT`

The service fascia should be a standalone numbered part, so a future owner can order only that part from a CNC shop without recutting the rear cabinet panel.

## Safety

- Mains and signal/data fascia bays are physically separated.
- Mains terminals are enclosed behind the decorative panel.
- Rear low-voltage connectors should be electrically isolated from mains hardware as required.
- Mechanical-feedback disable is accessible without entering the mains compartment.
- No service connector should require the builder to expose live mains wiring during ordinary use.

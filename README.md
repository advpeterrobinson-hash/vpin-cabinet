# Virtual Pinball Cabinet

Parametric CNC-ready virtual pinball cabinet based on Williams WPC standard-body proportions.

## Primary design targets

- Williams WPC standard-body external proportions
- 18 mm metric plywood construction (final production value = measured sheet thickness)
- LG OLED42C5 playfield
- 32-inch 1080p backglass
- Hinged structural playfield cradle
- Dual gas struts
- Independent mechanical safety support
- Real pinball legs
- Retractable wheels for moving cabinet
- Full DOF / mechanical force feedback
- SSF tactile audio
- Modular electronics and feedback mounting
- Slide-out ATX PC chassis
- Single mains power cord
- Independent Audio Only / Bluetooth mode
- Full Pinball mode
- External service USB ports
- Normally offline operation
- CNC-first construction with minimal hand tools
- FreeCAD parametric master model

## Engineering workflow

The long-term source of truth is the documented design baseline plus the Python/FreeCAD generation and validation scripts. The binary `.FCStd` master is an engineering artifact, not the only record of design intent.

Useful local commands:

```bash
make doctor
make validate
make open-master
```

`make validate` currently checks the documented dimensional baseline without requiring FreeCAD. FreeCAD geometry/collision checks will be added as the design matures.

See:

- `AGENTS.md` — engineering rules for humans and coding agents
- `config/design.json` — machine-readable design baseline
- `docs/DESIGN_DECISIONS.md` — decision log
- `docs/requirements.md` — system requirements
- `docs/reference-baseline.md` — dimensions extracted from the reference model
- `docs/vendors.md` — parts/services/vendor notes

## Current validated geometry

- Williams WPC cabinet profile is live-parametric.
- Outer width: 558.80 mm.
- Nominal 18 mm plywood gives 522.80 mm inside width.
- LG OLED42C5 cross-cabinet physical width: 540.0 mm.
- Target OLED cavity including clearance: 542.0 mm.
- Nominal side pocket depth: 9.60 mm.
- Nominal remaining side skin: 8.40 mm.

The OLED pocket is a clearance feature only; the OLED and future gas-strut loads must be carried by an independent structural cradle.

## Status

Engineering / parametric-CAD development.

No CNC files are approved for manufacturing yet. CNC production remains blocked on final hardware geometry, material measurement, provider/tooling consultation, physical tolerance coupon, and final design validation.

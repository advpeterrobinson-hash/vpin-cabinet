# Addressable lighting — matrix dimensions and owner direction

[English](LIGHTING_INTENT_V32.md) · [Português (Brasil)](pt-BR/LIGHTING_INTENT_V32.md)

**Owner clarification, 2026-09-29:** use Cleveland Software Design matrix panels with the Arnoz MX-DONNY (Donny) board. The Cleveland product page is the panel/dimensional reference; its bundled controller, PSU and configuration workflow are not selected by this decision. This corrects the earlier interpretation that the complete plug-and-play control system would be used.

The design remains open. Installation, wiring, power supply, controller configuration and final arrangement will be decided by the owner. The current engineering task is to retain the matrix size reference without freezing a carrier, permanent holes or placement in V32.

## Matrix dimensions

Source: [Cleveland matrix/kit listing](https://www.clevelandsoftwaredesign.com/pinball-parts/p/addressable-led-plug-and-play-kit), checked 2026-09-29. These are published nominal dimensions, not measured hardware.

| Item | Dimension / count | Meaning |
|---|---|---|
| One panel | 3.125 × 3.125 inches = 79.375 × 79.375 mm | Published square panel size; thickness not specified |
| Six panels | 6 × 16 × 16 = 1,536 pixels | Existing planning quantity retained |
| Six panels in one row | 476.25 × 79.375 mm | Arithmetic from individual widths, without spacing or connector allowance; not a selected layout |
| Vendor's approximate six-panel length | 18.5 inches = 469.9 mm | Differs from six nominal widths by 6.35 mm; do not use as a final cut dimension |

Use the individual nominal panel size for preliminary size comparisons. Final assembled size, thickness and installation clearances remain open. No mounting envelope or cabinet geometry is changed by this record.

## Other lighting choices retained

- Two speaker LED rings are included in the owner's intent.
- Undercabinet lighting is optional, separate from side strips and optional display-gap lighting.
- The kit's two side strips remain a reference for the earlier lighting discussion; their installation and allocation are not frozen by selecting the matrix panels.

No CSD controller port map, COM-port setup, cabinet.xml preset or bundled PSU is adopted. Compatibility and installation details are for the owner's later implementation; this record makes no tested compatibility claim. Physical sessions remain paused and CNC release remains blocked.

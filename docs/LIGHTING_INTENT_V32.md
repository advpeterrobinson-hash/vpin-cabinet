# Addressable lighting — selected kit

[English](LIGHTING_INTENT_V32.md) · [Português (Brasil)](pt-BR/LIGHTING_INTENT_V32.md)

**OWNER_SELECTED 2026-09-29; integration PROVISIONAL; CNC BLOCKED.** The owner selected the [Cleveland Software Design Addressable LED Plug and Play Kit](https://www.clevelandsoftwaredesign.com/pinball-parts/p/addressable-led-plug-and-play-kit). Retain the previous six-panel intent. On 2026-09-29 the owner confirmed two speaker rings and optional undercabinet lighting; the final order SKU remains unrecorded. No purchase or receipt is asserted.

The included controller supersedes the previous Arnoz MX-DONNY plan for this kit. This does not change other Arnoz devices. Earlier Pinscape/MX-DONNY notes are historical context, not the selected controller allocation.

## Published kit facts and dimensional limits

Source checked 2026-09-29. Vendor lists a Wemos S2 controller with 10 outputs, matrix panels, two side strips, connection leads/extensions, spacers/screws, USB cable and a 5 V / 15 A supply. Six panels provide 1,536 pixels; the side strips add 288. Optional speaker rings have 45 pixels each, 5 V, and listed dimensions 120/102/9 mm (dimension roles require confirmation).

Each panel is stated as 3.125 inches square: 79.375 mm. The six-panel length is separately approximated as 18.5 inches: 469.9 mm. Six nominal widths total 476.25 mm, a 6.35 mm discrepancy. Neither figure defines a machining envelope; thickness, mounting pitch, spacing and connector clearance remain unknown.

Supply nameplate output gives 75 W by arithmetic, not measured LED consumption or proof of unrestricted brightness capability. Keep load currents unknown until kit operating limits are documented. Preserve the cabinet's single external grounded feed; the supplied cord does not authorize a second external feed or exposed mains.

## Configuration and remaining decisions

Use the vendor's [cabinet file generator](https://pinball-docs.clevelandsoftwaredesign.com/docs/AddressableLED/cabinetGenerator/) for the actual kit configuration and detected COM port. Its presets include side strips. Save the resulting configuration and verify pixel order, orientation, brightness and each zone during commissioning; do not reuse the former MX-DONNY three-output calculation. No port numbers or cabinet.xml are frozen now.

Six panels retain the prior 16×16 intent. Their physical arrangement and precise placement above the playfield remain open. Included side strips do not establish undercabinet or optional display-gap lighting coverage. The two selected speaker rings add 90 pixels, for 1,914 including the matrix and kit side strips. Optional undercabinet lighting is a separate UNDERCABINET_LED zone, with product, length, pixel count, power and controller allocation still open; its load is not included in this subtotal. Optional display-gap lighting also remains separate.

## Mechanical and electrical integration to develop

- **Matrix carrier** and **lighting trim** remain provisional names without permanent part codes. Use removable adapters with accessible fasteners and connectors; avoid new structural furniture or component-specific permanent wood holes.
- Verify playfield service motion, backbox motion, viewing angle, glass reflections and connector access before introducing CAD geometry. Matrix installation must not obstruct service or rely on the TV for support.
- Keep speaker illumination removable with the speaker assembly; reserve cabinet lighting without deciding its precise locations yet. Optional gap lighting must preserve display replacement and ventilation clearance.
- Select panels/strips before calculating voltage, worst-case current, supply capacity, branch protection, conductor sizes and power-injection locations. LED control capacity is not power-supply capacity. Preserve existing mains isolation and audio/data routing rules.
- Provide independently configurable brightness by zone and an effects-off setting; final appearance is an owner visual-review decision.

Next inputs: exact six-panel/order SKU, undercabinet product if adopted, assembled dimensions, mounting/connector envelopes, strip lengths and documented operating limits. Physical sessions remain paused; no CAD geometry was changed.

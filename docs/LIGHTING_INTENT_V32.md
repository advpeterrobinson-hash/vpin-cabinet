# Addressable lighting — owner intent

[English](LIGHTING_INTENT_V32.md) · [Português (Brasil)](pt-BR/LIGHTING_INTENT_V32.md)

Status: **PROVISIONAL planning; no V32 geometry change; CNC BLOCKED**.

The owner intends an LED matrix above the playfield using Arnoz MX-DONNY, provisionally six 16×16 LED panels (1,536 pixels). Speaker and cabinet lighting are also intended. Lighting in any remaining gap around the playfield display is optional, subject to actual clearance and visual review.

“16×16” is pixel resolution, not millimetres. Six panels could form 96×16 pixels in one row or 48×32 pixels in a three-by-two arrangement; neither layout nor physical envelope is selected. Exact placement meant by “above the playfield”, panel dimensions, pixel pitch, connector clearance and mounting orientation remain open. Do not change the cabinet or reduce the future display envelope to fit an assumed matrix size.

## Controller reference and planning limits

The [manufacturer's MX-DONNY page](https://shop.arnoz.com/en/dude-s-cab/151-mx-donny.html) describes an expansion used with Dude's Cab, with eight outputs and up to 4,096 addressable LEDs. The [Dude's Cab manual](https://dude.arnoz.com/dude_Cab_English_guide.pdf) describes 512 LEDs per output for smooth animation. Sources checked 2026-09-27; only links and a short factual summary are retained, not vendor files.

Arithmetic planning only: two 256-pixel panels equal 512 pixels, so six panels could use three data outputs if the selected chipset, panel chaining and matrix mapping support that arrangement. Five outputs would then remain for other zones, subject to their pixel counts. This is not a confirmed wiring allocation, electrical power budget or purchase approval. Confirm the actual controller/mainboard revision and LED compatibility before freezing configuration.

## Mechanical and electrical integration to develop

- **Matrix carrier** and **lighting trim** remain provisional names without permanent part codes. Use removable adapters with accessible fasteners and connectors; avoid new structural furniture or component-specific permanent wood holes.
- Verify playfield service motion, backbox motion, viewing angle, glass reflections and connector access before introducing CAD geometry. Matrix installation must not obstruct service or rely on the TV for support.
- Keep speaker illumination removable with the speaker assembly; reserve cabinet lighting without deciding its precise locations yet. Optional gap lighting must preserve display replacement and ventilation clearance.
- Select panels/strips before calculating voltage, worst-case current, supply capacity, branch protection, conductor sizes and power-injection locations. LED control capacity is not power-supply capacity. Preserve existing mains isolation and audio/data routing rules.
- Provide independently configurable brightness by zone and an effects-off setting; final appearance is an owner visual-review decision.

Next engineering input: actual panel/strip model and dimensions, LED chipset/voltage/current specification, intended physical matrix arrangement, speaker lighting dimensions and cabinet-strip lengths. Physical sessions remain paused; no hardware measurements or approvals are implied by this intent record.

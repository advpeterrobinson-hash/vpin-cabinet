# Playfield display v0.16 — Brazil-market, model-agnostic service envelope

> Current owner baseline: [OWNER_REVIEW_V27.md](OWNER_REVIEW_V27.md). Older assist/stay descriptions below are historical; no assist hardware blocks current CNC. Use the active hardware/feature registers for procurement.

Status: engineering baseline; exact display model intentionally not selected.

## Why this changed

The project was initially packaged around the LG OLED42C5. By September 2026 that model is not a dependable Brazil-market purchase target, while the LG OLED42C6 is expensive and may be out of stock. The permanent cabinet therefore must not depend on either model.

The design now treats the playfield display as a replaceable module selected late in the structure phase from models actually available in Brazil.

## Permanent cabinet target

Main cabinet outer width remains **580 mm** with nominal 18 mm plywood.

The v0.16 playfield display target is:

- physical chassis cross-cabinet width: <=560 mm;
- required cross-cavity with 2 mm clearance each side: <=564 mm;
- physical chassis front-to-rear length: <=970 mm;
- clear longitudinal service bay: 980 mm;
- maximum chassis depth: <=55 mm;
- display mass design limit: <=12 kg.

At 580 mm outer width, a 564 mm cavity leaves **8 mm minimum plywood skin per side**. This is an intentional maximum pocket condition, not the normal full-thickness wall condition.

## Performance purchasing target

The eventual playfield display should provide:

- 3840x2160 resolution;
- native 120 Hz or better;
- HDMI 2.1 / 4K120 or better strongly preferred;
- VRR preferred;
- low-latency game mode / ALLM preferred;
- VESA mounting strongly preferred;
- chassis dimensions and mass within the permanent service envelope.

For virtual pinball, high refresh and low latency take priority over smart-TV features and built-in audio.

## Current fit references — not purchase locks

### Samsung QN43QN90FAGXZD — 43-inch Neo QLED Mini LED

Current technical reference for the larger end of the envelope:

- 960.8 x 558.9 x 26.9 mm without stand;
- 9.4 kg without stand;
- VESA 200x200;
- native 120 Hz panel;
- up to 165 Hz input / Motion Xcelerator 165 Hz;
- VRR / FreeSync Premium Pro.

Pinball orientation:

- cross-cabinet: 558.9 mm;
- front-to-rear: 960.8 mm;
- depth: 26.9 mm.

With the project's 2 mm per-side clearance, the required cross cavity is 562.9 mm. In the 580 mm body this means approximately 9.45 mm side pocket per side, leaving approximately 8.55 mm plywood skin.

This makes the Samsung a useful **worst-case compact 43-inch fit reference**, but its market price may still be too high. It is not selected for purchase.

### Samsung QN43QN90DAGXZD — older 43-inch Neo QLED

Same useful 960.8 x 558.9 x 26.9 mm chassis class and 9.4 kg mass; 120 Hz native / up to 144 Hz input. Availability is variable and the official Brazil page may list it unavailable, so it is a fit reference rather than a procurement assumption.

### LG 42-inch C-series

The 932 x 540 x 41.1 mm / 9.8 kg geometry remains a useful smaller reference. C5/C6 models fit the 580 mm cabinet without side pockets, but neither is required by the design.

## Cradle consequences

The v0.15 steel pivot architecture remains valid because the Samsung 43-inch fit reference is actually slightly lighter than the original LG reference.

The following remain model-independent:

- 6 mm steel pivot cheek plates;
- 15 mm short journals;
- UCFL202 bearing concept;
- doubled plywood pivot zones;
- independent mechanical safety stays;
- positive closed-position latches.

The following stay open until the exact display is purchased:

- replaceable VESA adapter plate;
- longitudinal display position inside the cradle;
- exact gas-strut force;
- gas-strut mounting points;
- final cable-service-loop geometry around the selected display connectors.

## Purchase timing

Do not buy the playfield display at the beginning of woodworking.

Buy it in Phase 3, after the permanent cabinet/cradle envelope is physically verified but before the replaceable VESA adapter and gas-strut specification are frozen.

This keeps the expensive display purchase close to commissioning and lets the project choose the best 42/43-inch high-refresh model actually available in Brazil at that time.

# Visual Pinball Infinite — external software reference

- **Added:** 2026-10-29
- **Category:** Virtual pinball / VPX-compatible engine and table-library manager
- **Status in this repository:** RESEARCH / EVALUATE; **not installed, tested or adopted**
- **Project website:** https://visualpinballinfinite.org/
- **Upstream source:** https://github.com/VPinInfinite/VisualPinballInfinite
- **Releases:** https://github.com/VPinInfinite/VisualPinballInfinite/releases
- **Upstream licence:** GPL-3.0-or-later (as declared by upstream); check bundled third-party notices before reuse

## Why track it?

The independent Visual Pinball Infinite project describes a Rust implementation of the Visual Pinball X rendering and physics code and an integrated interface for VPX table playback, library organization, table-file matching, ROM/PinMAME management, multi-screen cabinet configuration, media generation, Virtual Pinball Spreadsheet discovery, and front-end integration. It says existing `.vpx` files are not modified.

It is **not** the official Visual Pinball X project (https://github.com/vpinball/vpinball) or Visual Pinball Engine for Unity. These projects must be evaluated separately.

## Compatibility / evaluation gates

- Upstream currently advertises **Windows 10/11 (64-bit), DirectX 12 GPU**. **No native Linux support is claimed**; do not treat Wine/Proton compatibility as verified.
- Evaluate compatibility with the existing VPX tables and ROMs, PinMAME and backglass/PinUP assets, DOF/SSF, cabinet inputs, nudging, 1–4 screens, media generation, and current launcher workflows.
- Verify claims of physical accuracy, latency, and rendering independently on representative tables. Published figures are **upstream claims**, not validation by this project.
- Test only in an isolated setup with backups and no automatic moves or rewrites of the original table collection.
- Keep cabinet engineering, CNC readiness, and hardware safety gates independent of this software reference.

## Source and relationship

External project, documented for future assessment only. No upstream code, ROMs, third-party assets or licence notices are copied into this repository. The vpin-cabinet's own hardware licence is not a relicensing of this software.

[Português (Brasil)](visual-pinball-infinite.pt-BR.md)

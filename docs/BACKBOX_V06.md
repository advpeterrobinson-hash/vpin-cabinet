# Backbox v0.6 — 32-inch-class Display Packaging

Status: engineering provisional; not manufacturing-ready.

## Why this stage exists

The cabinet body can remain authentic Williams WPC standard-body geometry while the backbox display needs its own fit check. A generic modern 32-inch monitor is often wider than the usable cavity of an authentic Williams-style backbox.

Reference-model backbox envelope:

- 730.25 mm outer width
- 254.00 mm depth
- 723.90 mm height

With a minimum 8 mm remaining side skin and 0.5 mm assembly clearance on each side, the preferred maximum monitor chassis width is:

`730.25 - 2*8 - 2*0.5 = 713.25 mm`

For procurement, use **713 mm maximum chassis width** until a specific display is selected and measured.

## Implications

- LG 32SR50F-W is 731.8 mm wide without the stand and therefore does not fit inside the authentic backbox envelope.
- Mancer Valak UZ32 is 715 mm wide and is slightly too wide if we insist on 8 mm remaining side skin.
- A Duex 31.5-inch model has been retailer-listed around 713 mm wide and is dimensionally promising, but the published dimensions are approximate and must not be used for CNC without confirmation or direct measurement.

## Design policy

The backglass remains a cost-controlled subsystem. We do not need gaming refresh rates or premium HDR. Desired characteristics are:

- approximately 31.5–32 inch diagonal;
- 1920×1080 sufficient;
- flat panel strongly preferred over curved;
- VESA mounting strongly preferred;
- chassis width <= 713 mm preferred;
- depth preferably <= 50 mm where practical;
- HDMI input;
- exact model selected before final backbox CAD/CNC.

If the best-value available monitor is only a few millimetres wider than this limit, a very small backbox-width deviation can be considered separately. We should not weaken the main cabinet or arbitrarily thin the backbox side structure merely to force-fit a display.

## Current recommendation

Do not purchase the LG 32SR50F-W for this project despite its otherwise suitable 1080p specification; its 731.8 mm chassis is too wide for the authentic backbox.

Continue shopping specifically by **chassis width**, not advertised diagonal size. A 31.5-inch flat 1080p monitor around 710–713 mm wide is the preferred target.

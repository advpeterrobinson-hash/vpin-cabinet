# LG OLED42C5 mechanical datum

Status: verified from LG's 2025 detailed-dimension drawing, with physical-TV verification still required before final machining.

## Primary sources

- LG Brazil product specification: https://www.lg.com/br/tvs-e-soundbars/oled-evo/oled42c5psa/
- LG 2025 TV detailed dimensions: https://www.lge.co.kr/kr/tv/tv_size_2025.pdf

## Published chassis data

LG Brazil specifies for OLED42C5PSA without stand:

- width: 932 mm
- height: 540 mm
- maximum depth: 41.1 mm
- mass: 9.8 kg
- VESA: 300 x 200 mm

## LG detail-drawing data for OLED42C5

The LG 2025 mechanical drawing identifies:

- H = 300 mm (VESA horizontal spacing)
- J = 200 mm (VESA vertical spacing)
- K = 316 mm on each side of the VESA horizontal pattern
- L = 134 mm above the VESA vertical pattern
- M = 207 mm below the VESA vertical pattern
- AA = 882 mm
- BB = 41 mm
- CC = 499 mm
- DD = 25 mm

The horizontal values reconcile exactly with the 932 mm chassis width:

`316 + 300 + 316 = 932 mm`

The vertical whole-millimetre drawing values total 541 mm:

`134 + 200 + 207 = 541 mm`

while the published overall chassis height is 540 mm. This is treated as normal drawing/rounding tolerance rather than silently modifying one of LG's dimensions.

## Selected pinball orientation

For the current engineering preview:

- native TV left edge -> cabinet front
- native TV right edge -> cabinet rear
- native TV top edge -> cabinet left
- native TV bottom edge -> cabinet right

With that orientation, cabinet-local VESA axes on the OLED envelope are:

- across-cabinet columns: X = 134 mm and X = 334 mm from the OLED's cabinet-left edge
- front-to-rear rows: Y = 316 mm and Y = 616 mm from the OLED's cabinet-front/native-left edge
- VESA center: X = 234 mm, Y = 466 mm

The VESA center is therefore **not centered across the 540 mm physical OLED height**; it is offset by approximately 36 mm from the physical center. Earlier centered-plate assumptions are superseded.

## Design consequence

The v0.4 cradle preview now aligns the two longitudinal cradle rails with the verified VESA columns rather than centering them symmetrically on the OLED chassis. The concept VESA plate is centered on the verified 234 x 466 mm datum.

The cross-cabinet orientation remains parameterized and can be mirrored later if physical connector access or internal clearance favors native-top toward cabinet right. Mirroring does not change the 300 x 200 VESA pattern or gas-spring kinematics; it changes only the cross-cabinet hole/rail locations.

## Production gate

Before final VESA plate machining:

1. verify the four threaded-hole centers on the actual purchased TV;
2. verify thread specification and permitted screw engagement from the TV manual/physical hardware;
3. confirm rear case protrusions/connector clearances around the plate and rails;
4. select spacers/washers so no plate or rail bears on fragile OLED rear plastic;
5. reweigh the completed moving cradle and update gas-spring sizing.

The verified LG drawing eliminates the previous unknown VESA-center offset, but it does not remove the requirement for a physical pre-machining check.

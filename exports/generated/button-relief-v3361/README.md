# V33.6.1 — front button ergonomics and open-front playfield relief

HEAD BEFORE: `fb13f88dfbd36afab18193baaf285bbffe721c7d`
HEAD AFTER: commit containing this report (`git log -1 --format=%H -- exports/generated/button-relief-v3361/README.md`).

[Offline viewer](../viewer-v32/index.html) · [CAD comparisons](review.html) · [Manufacturing BOM](manufacturing-bom.md) · [PT-BR BOM](manufacturing-bom.pt-BR.md) · [English manual](../../../docs/ASSEMBLY_MANUAL.md) · [Manual PT-BR](../../../docs/ASSEMBLY_MANUAL.pt-BR.md)

**CURRENT design geometry; CNC FULL-SHEET RELEASE remains BLOCKED.**

## Authority correction

The V33.6 task temporarily restored a superseded older button arrangement. The error was the authority decision, not a coordinate transformation or random viewer corruption. This task restores the owner’s front ergonomic datums while independently removing the horn through a clean front-open relief. Buttons do not move rearward to solve clearance.

| History | Meaning | Current status |
|---|---|---|
| Y255/Y310, Z270 | Historical initial side-panel layout | SUPERSEDED; negative control |
| `87d63825e09f5ebbe85a89a7e705a49f1b0c320b` | Owner correction to Y89/Y127, local side top minus 65 | CURRENT ergonomic authority |
| `80748804` | Later rounded side notch around front button service envelopes | Horned contour superseded |
| `fb13f88dfbd36afab18193baaf285bbffe721c7d` | V33.6 temporarily restored older rearward centers | Positional restoration and its regression rule were erroneous |
| V33.6.1 | Restore front centers and use a single rounded transition per side, open to front | CURRENT; hardware remains provisional |

## Side-button datums and service

| Button, mirrored left/right | Y from front mm | Z mm | Vertical datum |
|---|---:|---:|---|
| primary | 89 | 350.593661971831 | Actual side top 415.593661971831 minus 65 |
| secondary | 127 | 357.230281690141 | Actual side top 422.230281690141 minus 65 |

All 32 body, nut, bracket, contact, wire and tool reference objects move with the centers. The primary/secondary longitudinal ergonomic limits remain 110/150 mm. Negative controls reject Y255/Y310, Z270, the former horn, and a relief 0.1 mm shallower/shorter than the selected rounded parameters.

Final bore, counterbore/recess, nut pocket, bracket and leaf-switch drilling are **PURCHASE_BEFORE_CNC**. The visual Ø15.875 bore / Ø25×3 recess is explicitly **REFERENCE_ONLY_NOT_RELEASED**, not a selected hardware interface. Final bore/recess values remain null. Old rearward reference holes are filled before front reference shapes are applied.

Actual service proof is split into native body/leaf/wire/tool collision checks, explicit hand/tool access at playfield 50° with main glass/matrix removed, and continuous playfield service/lift certificates. Reference reserves are packaging evidence; physical ergonomics, terminal hardware and actual hand/tool use still require confirmation.

## Clean M025 relief

One 18 mm CNC part remains. Each side starts inset at the open front, follows a straight edge, turns through one tangent quarter-circle, then meets the full-width side with a straight shoulder and convex exterior corner. There is no forward bridge, finger, neck, reverse curve or new dogbone.

| Measure | Result |
|---|---:|
| Inset depth per side | 22 mm |
| Longitudinal extent from front | 87 mm |
| Transition radius | R8 |
| Local front / arc start / full-width return | 20 / 99 / 107 mm |
| Inset left/right X | 72 / 528 mm |
| Minimum width within front relief | 456 mm |
| Minimum front section, 18 mm stock | 8208 mm² |
| Original front section retained | 91.2% |
| Nearest VESA load reserve | 286.308 mm |
| Nearest saddle strap | 862.000 mm |
| Nearest strap fastener | 865.802 mm |
| Nearest dowel | 877.143 mm |
| TV envelope clearance | 8.000 mm |
| Actual M025 solid volume | 8751705.451875 mm³ |
| Relief removed volume | 68409.557368 mm³ |

Depth is derived from the restored tool reserve reaching X70 plus 2 mm margin. Length is searched against all restored occupied/service B-reps using exact separation, then rounded upward to 0.1 mm: full width returns at local Y107. A 0.1 mm shallower candidate has 1.9 mm tool clearance and fails; a 0.1 mm shorter candidate fails the 2 mm service margin. This is the shortest tested end within the selected simple R8 profile and 2 mm reference reserve policy, not an optimization over every possible contour.

The front retains 456 mm continuous section versus 500 mm before relief. The preserved rear service window still leaves two 160 mm bands / 320 mm total there; the 456 mm figure is specific to the new front relief, not the minimum across the complete perforated board. The modeled central VESA region, TV, rear dowel, four saddle straps and eight F02 screws are unchanged. Section geometry is a structural screen, not certification: actual plywood, full display load and dynamic handling remain qualification gates.

## Preserved V33.6 work and systems

The 180 × 110 R8 rear service window, two playfield strain-relief slots, connector corridor and flexible cable study remain. The two backbox carriers retain their four strain slots; M067, captures, four positive monitor-retention bolts and all adjustment remain exact. No new backbox machining is introduced; its central VESA-window proposal stays HOLD.

Captured shell joinery, M006, RearBearingShelf, SW01×4, solid-leg jig, rear fans, T1/T2/T3, S1/S2/S3, WPC Y1066.8/Z508, matrix, doors and glass are unchanged. No 4 mm plywood, laminated leg blocks or old monitor stops return. No material rationalization was performed.

## Viewer, manufacturing and accounting

Installed poses, detailed manufacturing meshes, exploded/assembly/service animations and packing derive from this current B-rep. Each selectable viewer object carries its source authority. V33.6 remains a historical snapshot; active regression now protects front ergonomic centers and the open-front topology. EN/PT-BR, offline operation, tablet controls and both palettes are retained.

Counts remain **101 permanent wood / 97 CNC plywood / 4 SW01 shop blocks / 59 families**. Operations remain 46 ONE_SIDE_CNC_READY, 51 ONE_SIDE_CNC_PLUS_MANUAL_FINISH and 4 SHOP_MADE_SOLID_WOOD_PART. The three revised wood pieces reconstruct with 0 mm³ difference; the other 98 manufacturing pieces are unchanged. New edge relief is a one-face through contour, R8 compatible with Ø4/R2; no flip machining. Held button holes are excluded from release authority.

Nominal planning wood mass is **60.452261 kg**, a change of -0.044466 kg from V33.6. LOW/NOMINAL/HIGH: 51.115172 kg / 60.452261 kg / 69.826092 kg. Actual solid volumes and unchanged density/SW01 blank allowances drive accounting. No unknown hardware mass or quantity is silently closed.

| Bundle | External L×W×H mm | Nominal gross kg | High-density gross kg |
|---|---|---:|---:|
| P25-01 | 1353.1×641.9×98 | 21.958425 | 24.984614 |
| P25-02 | 1317.1×617×88 | 21.932678 | 24.994308 |
| P25-03 | 825×768.9×197.8 | 21.993895 | 24.997653 |
| P25-04 | 1197.1×240×182 | 2.454500 | 2.736756 |

Packaging remains preliminary; glass, electronics and hardware are separate. Stock families and preliminary sheet assumptions remain 18/12/8/6 mm; small-stock/offcut procurement remains preferable for tiny groups. No production nesting, CAM or G-code is produced.

## Validation

| Gate | Result |
|---|---|
| Native geometry | 16 checks PASS |
| Motion | 17 checks PASS |
| Button metrology/access | 6 checks PASS |
| Flexible cable sampling | 63 poses PASS |
| Regression | 2091 checks PASS |
| Offline browser | 148 checks PASS |
| Playfield 0–50° and 48 mm lift-out | PASS |
| Backbox populated 0–90° | PASS |
| Horn absent / front ergonomic centers | PASS |
| Manufacturing reconstruction | 0 mm³ difference |

[Geometry](geometry-validation.json) · [Motion](motion-validation.json) · [Buttons/access](button-metrology.json) · [Cable](cable-study.json) · [Manufacturing](manufacturing-audit.json) · [Regression](validation.json) · [Browser](browser-validation.json)

The cable study is sampled flexible routing, not a continuous flexible-material certification. Rigid-motion certificates and full-assembly samples preserve MAIN PLAYFIELD GLASS/MATRIX prerequisites. Normal backbox folding retains backbox glass and lower cassette with rear doors closed/latched and locks parked; no routine electrical disconnection is introduced.

## Release holds

**CNC FULL-SHEET RELEASE: BLOCKED.** Actual production plywood thickness, calibration coupon/fit clearance, purchased leaf-button hardware and all bores/recess/leaf attachment details, display-specific mounting/connector hardware, purchased WPC/fasteners, cable/clamp limits and remaining structural/ergonomic qualification remain pending. Under-front 220 × 55 controls remain an unlocated schematic, not manufacturing coordinates.

CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

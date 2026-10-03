# V33.8 — solid front landings and service/modularity review

**Design candidate promoted; full-sheet CNC remains BLOCKED.** Only the two landing bodies and their obsolete binder screws change in CURRENT. Other geometry, all 18/12 plywood interfaces and the underfront module remain protected. Raised-playfield service is a geometric pose only until its primary support is defined and physically qualified.

HEAD BEFORE: `cdd21333ca0382cd8e99f9a96872f994136306e5`  
HEAD AFTER: the commit containing this report on `feat/cabinet-review-v32`; exact commit is returned with delivery.  
Native SHA256: `c78a64794d4ac009e12986aa5adc03f936b5bbf95b84d0a4da35e2742f7c4c53`

[22 native CAD views](review.html) · [CURRENT native](play.FCStd) · [Offline viewer](../viewer-v32/index.html) · [English manual](../../../docs/ASSEMBLY_MANUAL.md) · [PT-BR manual](../../../docs/ASSEMBLY_MANUAL.pt-BR.md)

## Decisions

| Item | Decision / evidence |
|---|---|
| SW02 | **PROMOTE** two shop-made solid blocks, exactly 68 ×70 ×54 mm |
| Front supports | X72/X528,Y245 preserved; sameØ24 contact pads, rear dowel seated |
| Slope |9.906669° nominal preserved; not a user-selectable angle |
| Retention | **A retained:** two captive M6 ×100 tool-operated bolts |
| Hand knob | Ø30/35/40 ×21 reference grips pass packaging, hand and 10.5 mm release sweeps; no selected equally captive 100 mm commodity assembly |
| Quick pin | Rejected for current blind M6 receiver: no ball-lock capture shoulder |
| Secondary straps | Two studied; **0 promoted**, no qualified independent restraint or stow |
| Permanent accessory stations | **0**; existing shelves/crossmembers retained |
| Optional board | ACC01,100 ×120 ×12 mm;2 removable commodity clamps per user-selected board; not minimum BOM |
| Cable geometry | Preserve slots/passages; add documented routing zones, no mandatory connector/harness |

## SW02 functional and manufacturing comparison

Six 18 mm plywood layers become two solid blanks. Four F60 binder screws and glue-up operations retire. The canonical counts change 108→104 wood pieces,104→98 CNC plywood pieces,4→6 solid blocks,66→61 families. SW01 and its jig remain unchanged.

Each original landing union contains 243,577.373726 mm³ of wood. SW02 contains 245,252.628008 mm³: **1,675.254283 mm³ per side is added only inside obsolete binder bores**. No original functional wood is removed. External bounds, wall mating planes, adjuster/retention paths and side-screw axes remain exact. Manufacturing members reconstruct their final installed B-reps with 0 mm³ difference. This is an explicitly equivalent interface, not a false zero-difference claim for filled holes.

The shop supplies dry, stable, straight, knot-free 68 ×70 ×54 blocks. Preferred grain follows the 68 mm cantilever direction. A scale-verified paper template, clamped commercial perpendicular portable drilling guide, depth stop and same-wood coupon replace lamination. Templates are reference-only until hardware is purchased; hand-held paper marks alone do not establish perpendicular 54/68 mm bores. SW02 is shop-made solid wood, not a third plywood stock or a two-face CNC job.

The reaction/load geometry is unchanged. At the existing 15 kg display/HIGH mass sensitivity (22.604 kg complete moving assembly), the factor 2 planning demand is 136.272 N per front support, 102.204 N per upper attachment screw, and 34.068 N average shear per side screw. These are **demands, not capacities**. The simplified root section has 3701.460 mm² net area and 0.2225 MPa calculated bending demand. Local insert/head stress, anisotropy, splitting and screw pullout remain unqualified. The 9 mm center-to-end /4.5 mm head-recess ligament and 12 mm plywood embedment require a real coupon/load test. Solid wood is not assumed stronger than plywood.

Wood orientation and qualification rationale is informed by the [USDA Wood Handbook](https://research.fs.usda.gov/fpl/wood-handbook); it supplies no selected-species allowable for this design. Original simplified hardware studies reference [manufacturer sources](landing-sources.json); no vendor CAD or proprietary geometry was imported.

## Adjustment: travel is not the installed range

Mechanical hardware travel remains **−3…+3 mm**. With rear dowel fully seated, the actual common front-height clearance screen includes the installed main glass, matrix, display and side buttons. The first physical contacts are approximately −2.837633 mm at the primary leaf-button envelope and+1.781117 mm at the main glass. A continuous native CAD certificate supports the conservatively rounded **−1.9…+0.9 mm setup window with≥1 mm modeled clearance**.

Use the adjusters to reproduce the accepted nominal plane and equal pad contact. Do not twist the rigid base by independent contrary settings or use this range to select a playing angle. Release the captive retainers for setup, then reset stops for 6–8 mm receiver engagement. Real stock, deflection and component fit still need physical checks. Earlier ±3 mm wording describes mechanical travel only and is superseded by [adjustment-validation.json](adjustment-validation.json).

## Normal retention and safety

Normal sequence: open coin door → release left and right captive M6 retainers with the existing tool → remove main playfield glass/matrix as required → raise using a defined and qualified primary support procedure. The same 110° coin-door access is preserved by SW02. A future purchased hand unit may replace tool operation only after grip captivity, metal thread, anti-release and nudge qualification. A catalogue press-fit grip is not proof of equal safety.

**CURRENT contains no fully defined/qualified primary support for the 50° raised playfield.** The accepted rear dowel/open cradles and front landings do not hold that service angle. Historical props cannot silently be restored. Therefore the native 0–50° clearance PASS is not permission to work below a raised display. No safety strap is inserted as a substitute.

The strap study considered 42 direct route cases. Front-low routes have the wrong length-change sign for closure arrest; rear-high routes cross moving wood/display; rear-tail routes have poor leverage and late take-up. A single remaining strap must take the full failure load, not half. Commodity cargo lashing is not automatically fall-arrest hardware. [Safety report](safety-report.md) records energy/load sensitivity, failed paths and sources. Decision: **NONE**, with primary-support definition, short rated assembly, independent anchors, arrest distance and stow all unresolved. No permanent anchor holes or minimum strap quantities were invented.

## Optional modules, routing and dry fit

ACC01 sample boards sit on S2 right and S3 left, using rear-edge and front-edge clamps respectively. Native checks preserve shelf screw access, extraction and playfield movement. The minimum nonbearing sample gap is 6 mm. Actual clamp jaw/throat/handle, retained payload and vibration still require qualification; a controller board fit does not qualify a contactor/chime. Remove the board/clamps before its shelf. Optional samples stay outside minimum stock, mass and packing.

Cable grammar: CABLE_PASSAGE, STRAIN_RELIEF_PAIR, SERVICE_LOOP_ANCHOR, POWER_ROUTE, SIGNAL_ROUTE and MOVING_HARNESS_ROUTE. Preferred existing slots are 6 ×22 R3,34 mm pair pitch; protected compact 6 ×16 R3 backbox and 4 ×12 R2 underfront exceptions remain. No slot is added merely for visual consistency. Left low signal and right low extra-low-voltage power planning zones are 420 mm apart, with 24.677 mm minimum modeled clearance. Mains stays separately enclosed; this is not electrical routing certification.

The existing 400 mm playfield loop passes 63 PLAY/service/lift samples, minimum sampled curvature radius 39.270 mm against 35 mm planning reference. No routine 50° disconnect is needed by that geometric example. **Backbox universal moving-harness route remains HOLD**, because a generic loop trial crossed floor geometry or violated bend curvature. Existing passage/carrier slots and service planes remain unchanged; no normal disconnection workaround is imposed. Qualify the actual supported cable loop before use. [Modularity/routing report](modularity-report.md).

Captured shell joints, floor supports, rear bearing shelf, M067 and the underfront shoulder provide positive dry-fit datums. Fixed shelf supports/cradles retain their matching locators. Unresolved kit-datum work remains at T-guide wall positions, backbox monitor rail cleats and rear hinge-cleat drilling. These are explicit template/placement holds, not hidden tape-measure instructions. All 104 final pieces have canonical IDs and orientation records. Commercial flatpack references inform dry-fit/service/modularity principles only; no proprietary joinery,5-axis dependence or large mounting panels are adopted.

## Material, mass and packing

Exactly **18 /12 mm plywood** remains active; forbidden CURRENT plywood pieces:0. Four SW01 and two SW02 blocks are explicitly solid wood. The one-face status counts are 43 CNC ready +55 CNC plus manual finish +6 shop-made solid parts. All physical manufacturing gates remain held.

| Stock | CNC pieces | Finished outer-contour area m² | Preliminary 2500 ×1600 sheets | Net utilization |
|---|---:|---:|---:|---:|
| 18 mm | 59 | 5.233752 | 2 | 54.67% |
| 12 mm | 39 | 1.807668 | 1 | 33.93% |

Nesting is PRELIMINARY, NOT FOR CNC, with 20 mm border/15 mm spacing. No new sheet family or full-sheet requirement is introduced by SW02; six small 18 mm cutouts are removed from the nesting demand.

Delivered wood LOW/NOMINAL/HIGH: **51.787 /61.277 /70.829 kg**. Finished-reference wood nominal:61.244 kg. Delivered nominal mass is unchanged because the two solid blanks equal the six former plywood shipping blanks at the planning 650 kg/m³. SW02 density is separately configurable 500/650/850 kg/m³; unknown actual wood/hardware masses are not zero.

Preferred packing: **4 wood bundles**, target 20 kg, allHIGH-density gross values≤25 kg. Glass/electronics remain separate; hardware has its own box. Optional boards and straps are excluded.

| Bundle | External L ×W ×H mm | Wood mass kg | Gross HIGH kg |
|---|---|---:|---:|
| P20-01 | 1353.1 × 641.9 × 74.0 | 15.604 | 19.998 |
| P20-02 | 1317.1 × 617.0 × 88.0 | 15.568 | 19.995 |
| P20-03 | 825.0 × 768.9 × 128.0 | 15.680 | 19.999 |
| P20-04 | 1197.1 × 275.0 × 371.8 | 14.426 | 18.652 |

Required Fxx minimum is **176 known pieces +6 formula-dependent families +6 genuinely TBD families**. F60×4 is retired. No other unknown hardware quantity is guessed. [Manufacturing BOM](manufacturing-register.json) · [Hardware dashboard](hardware-dashboard.json) · [Mass](mass-budget.json) · [Packing](packaging.json).

## Validation and remaining release gates

5329 regression/evidence checks and 38 browser checks pass. Native differential certificates cover SW02 against 0–50° playfield opening,48 mm lift and populated 0–90° backbox fold; all other interactions inherit the exact protected V33.7 geometry. Hand/knob packaging is not hardware acceptance; strap evidence completion is not a strap safety PASS.

Side buttonsY89/Y127: PASS. Horn absent/front relief: PASS. Front support contacts/slope: PASS. Geometric service/lift/fold: PASS. SW01/M067/underfront 160 ×116 ×12,5BTN+USB, six-button alternate,2 mm shoulder,70 mm USB reserve and null device cuts: unchanged. Unrelated geometry: unchanged.

Release remains BLOCKED for actual stock, coupon, purchased hardware/display/button/USB/landing dimensions, SW02 species/drilling/load qualification, structural/ergonomic proof, unresolved dry-fit templates, primary raised support and actual moving-harness qualification. No G-code, production nesting or manufacturing approval is supplied.

Original material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet

# AGENTS.md

## Mandatory Tukkari-first architecture rule — owner V34

For every new or revised cabinet subsystem/function, first look for an equivalent publicly documented Tukkari solution. When one exists, its functional architecture is the default basis; independently dimension it for this project’s 18/12 mm plywood, one-face Ø4 CNC, hardware and service constraints. Do not import proprietary CAD, drawings or manufacturing files.

Before adding complexity, record: **TUKKARI EQUIVALENT; PUBLIC EVIDENCE; OUR CONFLICT (measured); WHY DIRECT ADAPTATION FAILS; MINIMUM DEVIATION**. “More modular”, “future-proof” or preference alone is not evidence. If no public equivalent is found, record the search and uncertainty, rather than claiming absence. Explicit owner architecture corrections take precedence; distinguish them from the public source.

V34 owner authority: a single monitor plate enters from the TOP during shell assembly, seats on two side stops, and is captured by side guides plus the permanently fastened top. The monitor itself is serviced from the FRONT after front acrylic removal. Do not reintroduce a removable rail/carrier, depth shoes or M067. Scope of promotion and current validation are recorded in `config/current_v32.json`; a study does not itself replace CURRENT. Manufacturing remains blocked.


## Current V34.2 backbox authority

- Read `config/current_v32.json`, `config/backbox_hardening_v342.json` and `docs/BACKBOX_HARDENING_V342.md`. One18mm captured monitor plate atY1209, primaryVESA100 slots with±15mm reference travel;2 fixed12mm stops. No rails/shoes/M067/cassette.
- TCL32S5K published715×422×75mm,3.15kg,VESA100/M4 is the primary reference. Actual boss plane/offset, connectors and active image are unmeasured.75/65 and80/70 body/boss sensitivity cases pass with12mm spacers;80/55 fails. Do not call the purchased TV fit frozen.
- Backbox front is purchased3mm acrylic reference with REAR painted mask, padded seats and one removable strip; normal monitor/acrylic service is FRONT, never shell-top/plate removal. Final mask must resolve the disclosed image-cropping tradeoff.
- Two lower120mm stations directly in existing doors: passive grille or optional intake;2 upper exhausts retained. No backbox universal shelves, intake baffles/filter frames or cable-management anchors. Essential passages only. User qualifies fan wiring.
- One18mm DMD/speaker panel;90mm rear speaker reference depth,3.1mm to frame. Final purchased speaker/DMD dimensions held.
- Main glass:5mm tempered reference, lined side channels, front lockdown and angled rear U on a local top-face BB_Floor rebate. Whole floor stays horizontal.9.906669° derived from actual channel plane;32mm side-edge transition and5.327mm minimum front skin need physical/coupon qualification. Final channels, glass cut and lockdown hardware NULL/HOLD.
-66 wood manufacturing pieces /60 CNC plywood /6 solid /45 families. Only12/18mm plywood. No CNC release; measured stock/coupon/purchased hardware and physical qualification required. Main-cabinet and raised-service-support holds below remain active.

## Protected V33.8 main-cabinet authority (backbox superseded by V34.2)

- Start with `config/current_v32.json` and `docs/SERVICE_PRODUCTIZATION_V338.md`. Protected V33.7 architecture remains; only six front-landing plywood layers and four obsolete binder screws are replaced by two SW02 solid blocks, 68 × 70 × 54 mm.
- Plywood stock remains exactly 18 / 12 mm. SW01 and SW02 are explicit shop-made solid wood, never a third sheet family.
- Front bearing stays X72/X528, Y245. The nominal 9.906669° plane is unchanged. ±3 mm is mechanical travel only; the V33.8 common-height geometric setup window is −1.9 to +0.9 mm with 1 mm modeled margin. Adjust to the accepted plane; no arbitrary angle selection or opposite-side twisting.
- Original captive M6 ×100 tool-operated uplift retainers remain. Hand knobs/pins are studies, not selected hardware.
- **Primary support for the raised 50° playfield is not defined/qualified in CURRENT.** Historical prop descriptions below do not establish a current mechanism. Clearance validation does not release unsupported service. No secondary safety strap is promoted and no anchor holes are added.
- Optional ACC01 boards and cable zones add zero permanent hardpoints. Keep S1/S2/S3 and T1/T2/T3 unchanged; optional boards never enter the minimum BOM. The reference PF loop has sampled geometry evidence; a universal backbox fold harness remains HOLD.
- SW02 drilling needs purchased hardware, scale-verified templates, a qualified clamped portable perpendicular guide and same-wood coupon. Wood species/grain/splitting and physical load/nudge qualification remain open. No CNC or manufacturing release.


## Purpose

This repository contains the engineering source for a CNC-ready virtual pinball cabinet inspired by Williams WPC proportions. The project is intended to be reproducible, parametric, serviceable, future-proof, apartment-buildable, and safe to manufacture.

The primary product is not merely one cabinet. The primary product is a **replicable flat-pack CNC plan** that another builder can take to a local CNC shop, order the parts, and assemble at home without owning expensive woodworking machinery.

## Source of truth

- **CURRENT V33.7:** `config/current_v32.json`, `config/manufacturing/flatpack_v337.json`, `config/manufacturing/stock_policy_v337.json`; report `docs/TWO_STOCK_USER_MODULE_V337.md`. Exactly nominal 18 mm and 12 mm plywood stock is permitted. Every other CURRENT plywood stock thickness fails validation. A thinner finished web is permitted only as an explicit one-face operation from allowed stock; it is not another purchased sheet family. SW01 solid wood is separate. Manufacturing release remains BLOCKED.
- **Protected V33.6.3 architecture:** rear wooden dowel/cradles plus front landings at X72/X528,Y245 support the unchanged 9.906669° playfield pose. Two separate captive M6 uplift clamps remain. T1/T2/T3 do not carry playfield gravity load. Side buttons Y89/Y127 at local top−65; front relief 52 each side, 396 wide, 87 long, R8; rear service window/strain slots/VESA, SW01/M006/M067, WPC axis Y1066.8/Z508 and shelves remain unchanged. Physical load/ergonomic qualification and final purchased-hardware drilling are not released.
- **Closed support design:** `ARCHITECTURE_PASS_PHYSICAL_QUALIFICATION_HOLD`. Rear dowel/cradles carry the rear; two front pads carry the front directly into full cabinet sides. T1/T2/T3 intentionally remain22 mm normal clear and do not carry playfield gravity load. Historical T1 shoes are a rejected comparison only. ±3 mm is tolerance compensation to reproduce the accepted9.906669° pose with L/R level and fully seated rear dowel; a real−3 mm lowered pose collides with buttons. Do not turn this into a height/tilt adjustment. M6 jam stops are reset after leveling; exact thread-compatible captive retainer, blind guide/depth and load tests remain PURCHASE_BEFORE_CNC/physical holds.
- **CURRENT viewer:** `config/viewer_v337.json`; `tools/build_viewer_v337.py`, `tools/rebuild_two_stock_user_module_v337.py`, `tools/check_current_v32.py`. Preserve EN/PT-BR, palettes, offline controls and all named service states. Native CAD, manufacturing pieces, metadata, mass and packing must share the same source hashes.
- **Underfront user module:** `config/underfront_user_module_v337.json`. One 160×116 mm nominal 12 mm removable plate; 2 mm underside locating shoulder in 18 mm FLOOR; owner 5 arcade buttons plus dual USB, generic 6-button and blank alternatives share one bay. These are programmable controls without permanent function labels. The 220×55 fixed-function SERVICE_IO_V08 / DEC-016 concept is SUPERSEDED for CURRENT, preserved historically. Button/USB/attachment production bores remain null / PURCHASE_BEFORE_CNC; the reference positions/envelopes do not release purchased hardware. No permanent individual device holes in FLOOR. Final stock, coupon fit, USB thread/pocket and hardware dimensions remain held.

- **CURRENT complete V32 backbox:** `config/current_v32.json`, `config/backbox_lock_integration_v32.json`, `studies/backbox-lock-integration-v32/README.md`. Owner-accepted twin 12 mm rear doors, optional door fans/blanks, low intakes, front-installed/rear-adjusted display, top-removable retained backglass and independent lower cassette are integrated with two rear-operated positive hand locks at X130/X470, Y1260. Captive knobs/washer assemblies are threaded into parking sockets before fold. Routine folding retains all backbox front modules and introduces no electronics disconnection. Old Y1188 lock centers/tool columns are historical. Rare WPC hinge floor service may still require cassette removal. No final purchased-hardware/CNC drilling or manufacturing release.

- **Preserved cradle/WPC baseline:** `studies/pivot-cradle-integration-v32/README.md`. R12 coaxial reserve + 2 mm allowance, broad rear-ear relief with convex R3 corner; full 180° seat, floor bearing, six support screws and accepted playfield poses retained. 210 mm backbox sides, Y1146 floor, generic passage and WPC axis Y1066.8/Z508 remain current. Side pivot installation tools require playfield lift-out/removal. The earlier service study is an immutable snapshot; its normal-fold cassette-removal blocker is superseded by the rear-lock integration above.

- **Previous WPC integration review (superseded by the combined package above):** `config/wpc_kinematics_v32.json`, Y1066.8/Z508 (241.3 mm from rear), pure rotation. The old Y1270 pivot interpretation is superseded. See `studies/backbox-structure-v32/README.md`: 210 mm backbox wood candidate folds, but installation of the side pivot is obstructed by both fixed `PF_OpenCradle` supports. Candidate NOT promoted; accepted CAD/viewer remain unchanged. Do not move or notch playfield supports without a scoped follow-up. No final purchased-hardware drilling is released.


- **Historical service-correction gate (button ergonomic datums reaffirmed by V33.6.1; other mechanisms below historical):** Current corrected CAD/viewer comes from `config/service_correction_v32.json` and `tools/run_service_correction_v32.sh`; review `docs/OWNER_CORRECTION_REVIEW_V32.md`. Ergonomic centers Y89/Y127, local side top minus65mm. Actual rear pivot and two captive CNC plywood props replace the teardown-only service study and legacy v18/v19 bearing/journal/steel-rod architecture. All manufacturing and structural proof remain BLOCKED.

- Latest consolidated drawing: `docs/CONSOLIDATED_DRAWING_V32.md`, `tools/run_consolidated_v32.sh`. Reference Cleveland4.1 =4 EX32EP2-4 exciters +BST-1, plus separateDCS165-4 subwoofer. Source floor study retained; consolidated model adds audio reserves and floor/PCBase anchors.39checks/202solids; not manufacturing release. Do not equate reference envelopes with measured hardware or the8-sheet PDF with completed lockdown/prop/electrical fabrication drawings.

- Current stage: rear functional layout closed (not manufacturing release), see `docs/REAR_CLOSURE_STATUS_V32.md`. Separate floor study `docs/FLOOR_DETAIL_V32.md` / `tools/run_floor_detail_v32.sh`: R3 intakes, wider removable filter-holder frames and8 candidate through-holes. Rear/shelves/lowPC untouched; subwoofer hardware and floor load qualification remain pending.

- Corner relief audit: `docs/CORNER_RELIEF_V32.md`, `tools/run_corner_relief_v32.sh`. Separate R3 guide trial, not adopted production geometry. Six guide slots have25mm bottom clearance; captured-shell corner relief remains pending. Never claim all dogbones/CAM are complete; actual cutter is unconfirmed.

- Latest connector service screen: `docs/CONNECTOR_FIT_V32.md` and `tools/run_connector_fit_v32.sh`; separate fit coupon, no cabinet geometry change. Mains enclosure must allow internal nut service; RJ45 socket/body access remains unresolved. Candidate bolt stacks are not selected hardware.

- **Main-cabinet rear service baseline (separate from backbox):** `docs/FIXED_REAR_SERVICES_V32.md`, `tools/run_fixed_rear_services_v32.sh`. Two120mm fans fixed above rear door atZ500, no moving door fan harness. Owner correction: power/Ethernet flanges mount directly to plywood, no carrier plates. Old oversized IO windows/holes removed; RJ45 has draftØ24 and twoØ3.2 cuts from owner drawing416185; mains now has28x48R3 cutout and2xØ4.5at40pitch from owner drawing416187, replacing416183. See docs/DIRECT_CONNECTOR_DIMENSIONS_V32.md; real hardware fit through18mm stock remains unverified. Two floor intakes, four unassigned floor holes omitted. Draft outer lockdown bores added; real receiver/bar fit remains open. Preserve all frozen shelf and low-PC datums.


- **Current rear closure (owner correction, 2026-09-30):** keyed hinged door, downward opening study110 degrees; start with `docs/REAR_DOOR_V32.md` / `tools/run_rear_door_v32.sh`. The four-screw removable cover and its nutplates are superseded. Owner approved door and made limiters optional (2026-09-30); do not spend time detailing them. Owner will add chair-protector felt at actual lock-body/lower-cabinet contact. 110 degrees is a screened pose, not a required mechanical stop; actual resting/contact angle remains unverified. Optional unkeyed slide bolt is owner-installed without drawing/instructions. Preserve low fixed PC base.


- **Owner-frozen shelf layout (2026-09-29):** preserve `config/shelf_layout_freeze_v32.json` (Y120/565/865; gaps295/150; four top screws and independent service direction). Do not silently reopen placement. Hardware/load/CNC qualification remains pending.

- Archive new external sources through `library/README.md`: contextual plain-text links and assessments are tracked; third-party originals live in ignored `library/references/local/`. Record failed downloads and do not claim unavailable videos/PDFs were reviewed.

- The current owner-facing architecture review is **V32** on `feat/cabinet-review-v32`; start with `docs/RENDERS.md`, `docs/PART_CODES.md` and `exports/generated/cabinet-v32/README.md`.
- **Current shelf fixing direction:** four top screws per shelf (two each side), fixed supports, equipment retained on removal; start with `docs/SIMPLE_SHELVES_V32.md` and `tools/run_simple_shelves_v32.sh`. Earlier nut-cover/removable-support anchorage studies are historical; do not resume them by default. Actual raised-playfield clearance remains unverified.
- The V32 review package is generated by `exports/generated/cabinet-v32/build_v32.py` and its companion render/validation files.
- The root `Makefile` / `tools/build_active.py` path is a **pre-V32 validated engineering pipeline (v25–v27)** retained for evidence and transition. When it conflicts with the V32 review, do not silently treat the older architecture as current.
- Python/FreeCAD build scripts and documented design parameters are authoritative within the design generation they belong to.
- `cad/master/vpin-master.FCStd` is a generated/working engineering artifact, not the sole source of truth.
- External reference models under `reference/` are read-only references and must not be edited or copied wholesale into production geometry.
- All production dimensions must be traceable to either a documented hardware specification, a measured part, or an explicit design decision.

## Non-negotiable design constraints

- Williams WPC geometry is the visual/proportional baseline, **not an absolute dimensional constraint**. The owner explicitly approves roughly 10–50 mm dimensional deviations where they materially improve serviceability, structural margin, replacement-part availability, future electronics compatibility, or CNC/assembly simplicity.
- Permanent cabinetry must be designed around service/replacement envelopes, not just the exact dimensions of the first-generation electronics.
- Prefer replaceable adapters, slotted carriers, filler strips, bezels, and mounting plates over monitor/board-specific holes in permanent wood panels.
- Main-body engineering baseline width is 600 mm (DEC-020), giving 564 mm clear width with full-strength 18 mm sides.
- The lockdown bar may be custom-sized and therefore is **not** a blocker to the 600 mm body width.
- Nominal main material is 18 mm metric plywood; production geometry must ultimately use measured sheet thickness.
- Playfield is model-agnostic: compact 42/43-inch class within 560 x 970 x 55 mm and 12 kg, mounted in an independent cradle with replaceable display adapters.
- The playfield is manually raised and supported by two identical captive CNC plywood props with positive receiver pins. Either prop must support the full moving load independently; no friction stays.
- A reduced-thickness OLED side pocket is clearance only; Display mass and prop/pivot loads must be carried by full-strength structure/cradle hardware.
- Backglass is approximately 32-inch 1080p; premium image quality is not a priority there. Backbox width may depart from authentic Williams dimensions to create a durable 32-inch-class service envelope.
- **Owner-confirmed V32 PC architecture (2026-09-29):** the open ATX case sits low on `PCBase`, a 285 × 460 × 18 mm replaceable base over the cabinet floor; V32 has **no PC drawer**. Owner explicitly rejected the removable tray/drawer complexity. PC stays positively fixed during use and routine service; detach only for major replacement. This latest decision supersedes the session-supplied full-extension drawer instruction. Older rear-slide/front-drawer concepts are historical.
- Real pinball legs are required; mobility uses external removable PinSkates-style devices only; no integrated wheels or wheel cutouts.
- Force feedback, SSF, electronics shelves, power distribution, and service wiring must be designed intentionally, not fitted after cabinet completion.
- Mechanical feedback devices should be rigidly coupled to the cabinet in spatially appropriate locations.
- Electronics shelves should avoid unnecessarily bracing SSF-active cabinet walls.
- Cabinet must use one external grounded power cord with internally protected distribution.
- Operating modes: OFF, AUDIO ONLY/Bluetooth, FULL PINBALL.
- Cabinet should be normally offline after setup, while retaining deliberate service/network access.

## Flat-pack / apartment-build rules

- A builder should not need a table saw, track saw, router table, drill press, planer, jointer, welding equipment, or other major workshop machinery to assemble the wooden cabinet.
- The CNC shop should perform all practical structural cutting, pockets, dados, rabbets, slots, dogbones/T-bones, large openings, repeatable drilling, and alignment features.
- Permanent panels should be self-locating where practical through dados, tabs, slots, shoulders, or captured alignment features.
- Assembly should target ordinary hand tools only: drill/driver, hex keys/screwdrivers, clamps, mallet, glue, measuring tools, sanding/painting supplies, and simple service tools.
- Avoid joints that require precise freehand routing or table-saw tuning after CNC delivery.
- Wherever feasible, hardware holes should be CNC-located rather than marked manually by the builder.
- Repeated left/right parts should be symmetric or clearly keyed so assembly mistakes are difficult.
- Every CNC part must eventually have an unambiguous part ID that corresponds to drawings, BOM, and assembly instructions.
- The final release package should be understandable by both the CNC shop and a first-time builder without requiring FreeCAD expertise.
- Metal parts that need fabrication, such as a custom lockdown bar, brackets, or panels, should have separate dimensioned DXF/PDF fabrication files where practical so they too can be outsourced rather than fabricated with specialist tools at home.
- Design complexity is acceptable inside the CAD/CAM package if it **reduces** builder skill, tool requirements, and measurement burden during assembly.

## Future-proofing rules

- A few millimetres of spare space are insufficient for permanent cabinetry expected to last many years.
- For major electronic classes (playfield, backglass, PC chassis, amplifiers, controller boards, power supplies), define a documented service envelope larger than the initially selected component where practical.
- Exact electronics may be required before machining removable carriers/adapters, but should not be required before cutting the permanent shell when a modular interface can decouple the two.
- Avoid trapping connectors, vents, VESA mounts, or service screws behind permanent structure.
- Preserve at least one upgrade path for electronics that are modestly wider/deeper than the initial part.
- When exact historical dimensions conflict with a clearly better long-term replacement envelope, prefer the replacement envelope while preserving the visual character of a Williams machine.

## Parametric CAD rules

- Prefer spreadsheet aliases/expressions over hard-coded geometry values.
- Do not create frozen geometry when a live FreeCAD expression can reasonably drive the part.
- Metric units are authoritative in the new design.
- Preserve clear coordinate conventions in every script:
  - X = cabinet left-to-right
  - Y = cabinet front-to-rear
  - Z = vertical
- Geometry-generation scripts must be safe to rerun and should remove/replace only objects they own.
- Scripts must fail clearly if required objects/parameters are missing.
- Changes to master dimensions must include a validation update or an explicit explanation why none is required.

## CNC rules

- No file is production-ready merely because it exports successfully.
- Final CNC output requires:
  - measured material thickness;
  - confirmed tool diameter;
  - confirmed joint/pocket clearance;
  - dogbone/T-bone strategy;
  - validation of part nesting and orientation;
  - a physical tolerance test coupon;
  - owner approval before manufacturing.
- Cutter CNC (`cuttercnc.com`, Brazil) is the current prospective fabrication provider. Provider-specific CAM assumptions remain TBD until consultation.
- Keep through-cuts, pockets, drilling, engraving, and reference geometry distinguishable in exports/layers where possible.
- Final manufacturing package should include, at minimum: CNC-ready DXF/SVG where appropriate, dimensioned PDFs, sheet/material map, part IDs, hardware/BOM, tolerance coupon, and assembly guide.

## Safety rules

- Never treat mains-voltage wiring as ordinary low-voltage electronics.
- Do not publish or approve exposed mains terminals inside service areas.
- Mechanical feedback must have an independent service-disable/kill path.
- Raised playfield service requires both positive captive props engaged; one-prop retention/load proof is mandatory.
- GPU and other heavy internal components require positive mechanical restraint because the cabinet will be nudged and vibrated.

## Validation policy

Before calling a design stage complete, validate at minimum:

- document recomputes without fatal errors;
- expected outer dimensions remain correct for the current approved design baseline;
- left/right geometry remains symmetric where intended;
- selected component fits within its service envelope;
- service envelope preserves documented future-replacement margin;
- remaining side skin around OLED meets the documented minimum;
- service envelopes do not obviously collide;
- generated parts are valid solids when they are intended to be solids;
- the part can be fabricated/assembled without requiring an undocumented specialist operation.

Later stages must add hinge sweep, prop-rod/stow, fixed-PC service access, backbox, toy, speaker, shelf, cable-clearance, fastener-access, and flat-pack assembly checks.

## Git workflow

- Use feature branches for substantial design/tooling work.
- Keep commits narrow and descriptive.
- Do not silently overwrite owner changes.
- Do not modify or delete reference models.
- Do not merge manufacturing-ready claims without validation evidence.

## Current review baseline

- Current owner-facing review: **V32**.
- Main body: 600 mm.
- Shelves: `S1`, `S2`, `S3`.
- Removable upright crossmembers: `T1`, `T2`, `T3`, using replaceable guides.
- PC: low open-case layout on `PCBase`; no drawer in V32.
- CNC/manufacturing: **BLOCKED**.
- V32 validation currently demonstrates valid solids and interference packaging only; it is not structural certification.

## Pre-V32 validated / selected baseline

- Williams WPC reference outer cabinet width: 558.80 mm.
- Selected engineering main-body width: 600.00 mm; manufacturing validation remains blocked.
- Cabinet side length reference: 1308.10 mm.
- Cabinet front outside height reference: 400.05 mm.
- Cabinet rear outside height reference: 596.90 mm.
- Rear top flat reference: 180.975 mm.
- Main plywood nominal: 18.00 mm.
- Playfield display envelope: 560 x 970 x 55 mm, maximum 12 kg; exact display selected later.
- Current playfield service envelope: 560 x 970 x 55 mm plus 2 mm installation clearance per side.
- Backbox future-proof target under v0.6: 780 mm outer width with a 740 x 450 x 100 mm replaceable display service envelope.
- Custom-size lockdown bar is an accepted fabrication strategy.

These values are engineering baseline values, not final manufacturing approval.


## Open-source / licensing rules

- Original project material is released under CERN-OHL-S-2.0 unless a file explicitly states otherwise.
- Preserve `NOTICE.md`, including the official Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
- Do not add licence terms that conflict with or weaken the strong reciprocal obligations.
- Commercial use is permitted; conveyed modified Covered Source and Products remain subject to the reciprocal source obligations in `LICENSE`.
- Do not import proprietary or ambiguously licensed CAD, drawings, artwork, manuals, code, ROMs, game assets, or vendor documentation into the repository.
- Third-party references must retain their own licence/copyright status and should be documented in `THIRD_PARTY_NOTICES.md` when relevant.
- Contributions submitted upstream are expected to be provided under CERN-OHL-S-2.0; see `CONTRIBUTING.md`.
- Do not remove applicable copyright, acknowledgement, modification, licence, or Source Location notices from generated release material.

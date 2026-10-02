# V33 mechanical hardware library and flatpack BOM

The inventory covers **all 438 CURRENT CAD objects**: 436 in the accepted upright assembly and 2 alternative backbox fan blanks. The catalog has **148 canonical families**, including 91 required, 22 optional, 15 future-electronics, 16 user-adapter and 4 nonphysical-reference families. Electronics are excluded from the mandatory mechanical kit. CURRENT V32, its holes, poses, wood and offline viewer remain unchanged.

HEAD BEFORE: `0aa4ea77531c59274a0b8547a71e731626bd2cf2`.
HEAD AFTER: the delivery commit containing this report on `feat/cabinet-review-v32`.

[Review gallery and deliverables](../../exports/generated/hardware-v33/index.html) · [canonical catalog](../../config/hardware_catalog_v33.json) · [wood material map](../../config/wood_materials_v33.json) · [EN BOM](../../exports/generated/hardware-v33/flatpack-bom-en.md) · [PT-BR BOM](../../exports/generated/hardware-v33/flatpack-bom-pt-BR.md) · [JSON](../../exports/generated/hardware-v33/bom.json) · [CSV](../../exports/generated/hardware-v33/bom.csv).

## Scope and quantity authority

This is a complete **inventory coverage audit**, not a complete manufacturing cut list or a ready-to-order hardware kit. It accounts for modeled parts, purchased assemblies represented by several solids, necessary but unmodeled interfaces, and nonphysical service volumes. Missing quantities remain `null`/TBD. Price fields are null; no costs, supplier commitments or selected SKUs are invented.

The 150 audited definitions became 148 canonical families after washer deduplication; the final catalog contains 129 physical hardware/consumable/adapter families plus 19 electronics/reference families. The stable ID scheme separates wood P, fasteners F, washers W, captive threads/nuts I, mechanisms H, fittings B, consumables/glass G, electronics E and nonphysical references R. Aliases W04/W05 point to W02 and are not buy lines.

The machine-readable BOM has five layers and 245 usage/wood rows. Shared families may have required and optional usage rows; therefore row count is not unique-family count. All exact modeled quantities are reconciled to the object map. Architecture counts are distinguished from measured instances. Purchased hinge leaves/pins, lock bodies/barrels/tongues and receiver backings are not counted as separate complete mechanisms.

Basic mechanical configuration: shell, shelf/support interfaces, wooden playfield pivot, rear service doors, WPC hinge architecture, positive upright locks, display/glass mechanical supports, lower cassette with blank baffles/adapters, matrix mechanical carrier, legs and lockdown interfaces. Backbox fan stations use **two existing blank plates** by default. Optional fans replace their station bolts; they do not add a second fixing set at the same holes. Passive intake/filter provisions remain. PC, displays, DMD, speakers, amplifiers, controllers, LED panels and toys are later purchases. User-supplied glass is separately identified, with its retention hardware in the mechanical kit.

## Consolidation

**Fastener/washer/nut/insert interface families: 78 before → 76 after.** This is the audited definition count before/after deduplication, not a count of final purchased SKUs; many functional rows still have no selected size.

The actual consolidation is support, main-door handle and rear-fan washers into **W02**. CURRENT B-reps independently show the same outer radius 4.5, inner radius 2.25 and thickness 1 mm. Required/optional quantities remain separate. Neither a hole nor a washer shape was changed.

Other opportunities remain explicit holds:

| Families | Opportunity | Why not adopted now |
| --- | --- | --- |
| F02 | Commercial 3.5×12 wood screw in place of the 3.4 mm cylinder | Strap aperture, head and plywood engagement need selected-part checks |
| F10/F11/F20 | Common M4 head, washers and nut across rear/floor/backbox fans | Preserve 55/50/unknown lengths for different stacks; the 12 mm door is not the 18 mm cabinet wall |
| F17/F35 | Parking 48 mm reserve versus 4×50 stock screw | Tip penetration and countersink differ; do not change accepted wood |
| I04/I13 | M4 blind insert, nominal OD 6×8 | Current floor bore 6 and matrix 6.1 differ; both hosts must qualify against one purchased insert |
| I03/I07/I12 | M4 common thread | Nut, captive receiver and insert are different forms; 12 mm doors need a separate stack review |
| W01/W03 | M5 common washer | Floor backing area and exact stack remain unresolved |
| F24/F25/F26/F27 | M6 drive family for monitor/glass interfaces | Reference lengths and heads are not final stock sizes |
| H11/I05/I06 | M8 upright/parking family | Retained as already accepted; never substituted into WPC threads |

The project already concentrates on M4 light hardware, M5 existing shelf/anchor interfaces, M6 display/glass reserves and M8 upright locks. Removing M5 by changing accepted holes would violate this inventory-only scope. F01 remains 4.5×30; the much shorter strap screws must not be replaced with it.

## WPC and playfield

H08/H09/H10/F14 preserve **01-9011-L,01-9011-R,02-4352,4322-01139-12B** as required purchases with a physical-measurement hold. Every requested arm/bend/hole, bushing and bolt/neck/head/length/stack measurement has a null field in the catalog. The corrected transverse axis remains Y1066.8/Z508. Library arm solids are the gross CURRENT reserve; bolt and bushing cylinders are original positive-control schematics, not purchased dimensions. No final drilling is derived from them.

Metric substitution is **not approved** for mating WPC or leg/lockdown hardware. A metric variant could only be considered as a complete matched, measured and load-qualified assembly, followed by a separately authorized interface review. Similar nominal diameters do not establish thread compatibility. The historical 3/8 upright clamp is superseded by the accepted M8 architecture, not a substitution into a remaining imperial receiver.

The playfield inventory is exactly **H01×1 hardwood dowel Ø32×560, B01×4 commercial saddle straps, F02×8 strap screws, P035/P036×1 each CNC cradles, F01×6 support screws**. Current F02 geometry is a 3.4×12 cylinder with 6.4 mm pan-head reserve; current F01 is 4.5×30 countersunk. No bearings, steel shaft, journals, gas struts or legacy props are introduced. Earlier prop/metal-axis source files are historical; the accepted wood-dowel builder explicitly retired them. Custom playfield pivot metal: 0.

## Backbox locks and service

H11×2 retains the rear-operated M8×40-family knobs at X130/X470,Y1260. W07, W08, H13, H12, B07 and B08 capture load washers, washer captivity, rotating loss protection, 200 mm tethers, slack keepers and anchors. I05×2 includes metal shelf backing; I06×2 provides threaded parking at X185/X415,Y1268. Parking uses the existing four 18 mm plywood pads and four 48 mm screw reserves. Bought-as-a-kit contents must suppress duplicate ring/backing purchases.

Routine fold remains: open doors, release and positively park both locks, secure tether slack, latch doors, remove main playfield glass/matrix per existing prerequisites, fold. Cassette, display, DMD, speakers and backbox glass remain installed. No electrical disconnection procedure or connector family is added. Rare WPC hinge-floor service may still require cassette removal; side-pivot maintenance retains playfield lift-out/removal.

Main rear hinges H02 and backbox 628 mm piano hinges H14 are separate families. H03 is the main rear keyed lock; H15/H16 are the backbox active cam lock and two passive bolts. Backbox seals, center overlap, fixed/door fan strain-relief anchors and passive intake hardware remain separate inventory entries. No door hardware is assumed to fit another system merely because it is commercially common.

## Wood classes and manufacturing gaps

The wood map contains **72 STRUCTURAL_PREMIUM and 21 MODULAR_SECONDARY CAD components**. Counting each leg block's seven existing 18 mm laminations gives 96 premium and 21 secondary scheduled pieces before unresolved compound decomposition. These are not final nesting counts. H01 is hardwood dowel stock, outside the plywood nesting map.

Load-bearing display rails, carrier members, VESA plate, DMD rear adapter, lower cassette frame, glass retainer, cradle supports and critical crossmembers stay premium even where replaceable. PCBase is secondary-eligible because it bears directly on the floor; its 18 mm thickness, anchor strength and payload requirements remain unchanged. A secondary sheet still needs suitable flatness, bond quality and fastener holding. Speaker baffles, cosmetic bezels, doors, filter frames and blanks are secondary candidates, not automatic substitutions.

Machine-readable policy: **first nest every plywood part in premium stock**. Only if a small secondary-eligible subset causes an additional full premium sheet may a reviewed alternative use good-quality secondary plywood/virola. “Small subset” is deliberately not assigned an arbitrary threshold; owner/supplier review remains required. Structural parts can never be automatically downgraded. Sheet sizes, tool/kerf, grain and actual thickness are still unknown.

There are 11 explicit wood decomposition holds: the stepped glass top retainer, two monitor stop blocks, four cassette cleats, two intake baffle assemblies and two hinge cleats. Some have 24/30/14 mm stock directions or fused returns rather than a simple 18/12 mm sheet profile. The geometry is preserved; V33 does not invent a lamination/joint to turn them into cut parts. Each of four leg blocks also requires individual layer extraction around its 45° bore; seven identical rectangle copies would be wrong. World bounding boxes in the BOM are **installed dimensions**, never CNC nesting outlines.

## Findings requiring follow-up, without geometry changes

1. **Leg reference conflict:** current 58 mm candidate bolt pitch versus 57.15 mm documented WPC reference. Purchased legs/backings/levelers must resolve this before CNC. No hole moved.
2. **Unspecified joint schedules:** 13 mandatory rows have unresolved quantity/coverage: F06,G01,F53,W06,F16,F18,F19,F22,F28,F31,F36,F38,F39. These include shell joints, keeper/astragal/intake fixings, repeated hinge fasteners, WPC washer/nut stack, channel/receiver and front-door attachment. A complete parts list cannot honestly invent these counts.
3. **Missing modeled floor-fan washers:** the config requires washers but CURRENT has bolts/nuts only. W02 records 16 additional optional washer positions as a planning allowance; selected-stack fit is still held. No washers were inserted into CURRENT geometry.
4. **Unselected dimensions are not stock lengths:** F17/F25/F27/F30 use 48/72/46/65 mm reference envelopes. Head, tip, captivity and engagement need actual hardware. The Ø18 monitor-clamp reserve is not an Ø18 bolt.
5. **Plywood assemblies are not yet all flatpack cut parts:**11 records above remain decomposition/thickness holds. This is an existing manufacturing-detail gap, not authorization to change their shapes.
6. **Optional content is not a thermal or safety certification:** no fan airflow, filter loss, rated guard opening, selected mains enclosure or toy payload is certified by the inventory. Mechanical cable passage stays generic and mutable.

No new collision claim is made for unselected hardware. These are inventory, documentary and packaging uncertainties surfaced by the audit; none was silently repaired.

## Sources and Brazilian sourcing

Existing current builders/configs and B-reps were used before historical BOMs. [Ciser's screw](https://www.ciser.com.br/categoria/parafusos), [nut](https://www.ciser.com.br/categoria/porcas) and [washer](https://www.ciser.com.br/categoria/arruelas) families establish a Brazilian commodity sourcing route. They do not establish local stock of every provisional length. The existing [SPAX 4.5×30 reference](https://www.spax.com/gb-en/p/stainless-steel-screw-full-thread-flat-countersunk-head-t-star-plus-4cut-stainless-steel-a2.html?variant=1197000450303) is not a chosen brand or local-availability proof. Cabinet-lock and knob suppliers are recorded as inquiry leads only.

[Source register](../../library/hardware/sources.json) distinguishes opened HTML, search-only evidence, prior repository references and failed PDF access. No vendor CAD/document, ISO/DIN drawing or unlicensed model was imported. Standard models are original simplified parametric solids; no detailed threads. Manufacturer-specific models must wait for selected hardware and redistribution permission.

## Decision report

| Requested output | Result |
| --- | --- |
| Total canonical catalog families |148, including electronic/nonphysical references;129 physical hardware/consumable/adapter families |
| Required / optional |91 /22 families |
| Future/reference / user-adapter |19 /16 families |
| Purchase-before-CNC / provisional |90 /148 catalog families; conditional categories remain conditional |
| Fastener families before / after |78 /76 audited interface definitions, not final purchased SKUs |
| WPC physical-measurement hold |YES |
| Playfield pivot custom metal |0 |
| Backbox architecture unchanged |YES |
| Structural premium / modular secondary |72 /21 CAD components |
| Flatpack wood complete |Inventory YES; final CNC cut BOM NO — 11 decomposition holds and leg-layer extraction |
| Required mechanical BOM complete |Inventory YES; final orderable quantities NO — 13 unresolved rows |
| Optional BOM complete |Inventory YES; final SKU/length/count qualification NO |
| Future electronics separated |YES |
| CAD hardware library created |YES — 148 representative models; unresolved markers explicitly distinguished |
| Detailed threads |NO |
| CURRENT V32 wood, accepted holes and viewer unchanged |YES — full starting-HEAD byte comparison, not only bounding boxes |
| New conflicts found |Six audit findings above; no new geometry introduced |
| Manufacturing |BLOCKED pending physical hardware/material/CNC, structural and assembly qualification |

See the generated [hardware status table](../../exports/generated/hardware-v33/hardware-status.md), [before-CNC list](../../exports/generated/hardware-v33/purchase-before-cnc.md), [before-assembly list](../../exports/generated/hardware-v33/purchase-before-assembly.md), [optional list](../../exports/generated/hardware-v33/optional-accessories.md), [future list](../../exports/generated/hardware-v33/future-electronics.md), [tool list](../../exports/generated/hardware-v33/tools.json), [assembly dependencies](../../exports/generated/hardware-v33/assembly-dependencies.json) and [exploded metadata](../../exports/generated/hardware-v33/exploded-metadata.json).

## Reproduce

Run from this worktree using the existing FreeCAD CLI. Scripts own only the new V33 catalog/library/artifact paths; they do not rewrite CURRENT files.

```sh
freecadcmd tools/audit_hardware_v33.py
python3 tools/define_hardware_v33.py
python3 tools/build_bom_v33.py
freecadcmd tools/build_hardware_library_v33.py
uv run --with matplotlib --with numpy python studies/hardware-v33/render.py
# Run export_bom_v33.mjs with the supplied @oai/artifact-tool runtime dependency tree.
# The task used a copy under .work/hardware-v33 beside a runtime node_modules symlink.
node .work/hardware-v33/export_bom_v33.mjs
python3 tools/check_hardware_v33.py
python3 tools/package_hardware_v33.py
python3 tools/check_current_v32.py
```

Require explicit PASS sentinels and passing JSON: FreeCAD can return exit 0 after a Python exception. The 15 real-CAD review atlases show one representative per family with independent raster cell scales; native family boards remain 1:1. Installed companion views retain exact CURRENT coordinates. Orange crosses indicate missing dimensional models, never installable fittings. Neither those exploded boards nor the dependency map claims a validated assembly sequence.

Original material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

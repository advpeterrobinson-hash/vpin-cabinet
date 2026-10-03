# V33.6.3 — complete closed playfield support

**CLOSED_POSITION_SUPPORT: PASS — nominal design architecture. Physical qualification and full-sheet CNC release remain BLOCKED.**

HEAD BEFORE: `349f0375c78f7308e5912d389b606d26d51f4b80`.
HEAD AFTER: the commit containing this generated report (`git log -1 --format=%H -- tools/report_front_landings_v3363.py`); the exact pushed hash is provided in the owner handover. A commit cannot contain its own hash.

[Offline viewer](../viewer-v32/index.html) · [18 native CAD views](review.html) · [native PLAY assembly](play.FCStd) · [full regression](validation.json) · [support gate](support-validation.json)

## Where the base rests

The **rear** of M025 rests through its existing four straps and Ø32 wooden dowel on the two open cradles, which bear directly on the cabinet floor. The **front** rests on two adjustable pads at **X72 / X528, Y245**. Their laminated bodies attach positively to the full 18 mm cabinet sides. Those two front contacts establish the intended playing angle with the rear dowel fully seated.

“Level” means level left-to-right. The fore/aft slope remains **9.906669°**, not horizontal. Glass, lockdown, buttons, electronics, cables and T1/T2/T3 carry no normal playfield gravity load.

Before this task there was no front landing: rear rotation alone did not establish the PLAY angle. T1/T2/T3 were 22 mm normal below M025 (22.333 mm measured at common Y vertically). They remain clear intentionally: they are cabinet structural crossmembers, not closed-position playfield supports.

## Options and selected geometry

| Option | Result | Support center Y | Base front overhang |
|---|---|---:|---:|
| Historical T1 shoes | Geometry comparison passes; complete support solution rejected/unqualified | 380 mm | 315.986 mm |
| Side landings | PASS at nominal accepted pose; selected | 245 mm | 180.986 mm |
| Full-width rail | NOT NEEDED; no fabricated motion/strength pass | — | — |

The 202-candidate native search compared 36/54 mm bodies at every millimetre from Y150 through250. Y245 is the earliest simple 54 mm body retaining the specified 5 mm reserve behind the right plunger envelope. The shorter 36 mm alternative loses half the side-fastener vertical separation. Mirrored supports avoid asymmetrical assembly. The T1 pair would use fixed nominal-gap shoes (18×54 mm footprint), pass load through removable T1 and its end guides, and retain 135 mm more front overhang. It offers neither the selected tolerance adjustment nor the completed positive retention. No T1 shoe is installed or added to the BOM. A full-width 564 mm rail adds obstruction and another cross-cabinet dependency without improving the required two contacts.

Two bodies, each **68×70×54 mm**, use **three 18 mm plywood pieces**. One repeated 68×70 mm CNC contour produces all six blanks; their finished layer/handed reference bores form six documented manufacturing families, M068–M073. No new stock thickness or custom metal is introduced.

Each body has four provisional 4.5×80 side screws, with **12 mm nominal embedment / 6 mm exterior skin**. Final rows are Y234/Y286, Z rows 36 mm apart, minimum body screw-center edge distance9 mm. The eight screws transfer vertical shear plus a tension/compression couple; wall friction is not credited. There is no glue to the cabinet side. Glue joins the three layers internally, supplemented by two binder screws per body. Both complete bodies remain replaceable. Minimum measured side-panel outside-edge distance is107.838 mm; all original side machining is untouched.

The final hardware audit found and corrected an actual new-support defect: preliminary Y240/Y280 side-screw rows intersected the M8 insert/stem and M6 retention bolts. Only these new rows moved. [Exact internal hardware regression](internal-hardware-validation.json) now checks distinct purchased parts in engaged and released states. Explicit overlaps inside the single purchased articulated-foot envelope are recorded separately; they do not imply a manufactured swivel design.

## Adjustment, contact and retention

**M8 articulated leveling foot + metal insert + washer + locknut**, with40 mm stem reference, Ø24 mm compact pad and3 mm replaceable resilient tip included in the solved stack. The foot must be captive and accommodate at least10° articulation. Purchased dimensions remain provisional. Each actual B-rep footprint is452.389 mm² with zero base penetration. Margins: outer base edge10 mm; front relief81.582 mm; VESA reserve193.286 mm; nearest internal opening536.897 mm; strain slots at least685.930 mm. Wider Ø28 pads were checked:615.752 mm² contact but only8 mm outer-edge margin. The compact pads already provide the intended contact, so wider pads are not adopted.

**±3 mm travel is construction-tolerance compensation only**, used to restore the existing9.906669° pose with matching L/R height and fully seated rear dowel. It is not an adjustable playfield-height or slope range. An actual−3 mm pose collides with the buttons and is forbidden. Opposed adjusters must not twist the base against the fixed rear axis. ±5 mm also fails the selected100 mm retention-bolt stack. The nominal angle is set from the accepted datums; a new printed gauge is not required.

Gravity support and uplift retention are separate. Two **TOOL-OPERATED captive M6×100 fully-threaded hex bolts** atX72/X528,Y275 engage metal-backed M6 receiver references under M025. Two thin jamnuts per bolt and a washer set the clamping stop; after leveling, reset these stops to7 mm target thread engagement (6–8 mm envelope). Do not bottom the blind receiver. The resilient landing tip limits chatter; the two clamps resist separation without using glass or lockdown as supports.

Before opening, open the coin door to110°, release both bolts and retract10.5 mm. Thread-compatible push-on retainers keep them captive in the bodies. No support hardware, electronics or display is removed for routine opening. A generic serrated washer is **not** a validated captive retainer. The final M6 retainer/bolt/insert stack must be bought and measured; no custom bolt groove is authorized.

The current M025 and side B-reps deliberately retain their accepted geometry. The new receiver/pilot interfaces are explicit manual-finish overlays, **PURCHASE_BEFORE_CNC**, not released holes. A rigid angle/drilling guide plus depth stop is mandatory for the vertical receiver bore in sloped M025. Reference maximum depth11.3 mm leaves6.099 mm nominal minimum skin; final pilot/depth remain hardware/coupon dependent. This must never become a freehand drilling instruction.

## Access and motion

The [tool-access screen](tool-access.json) uses a60×70×28 mm palm, finger bridge, actual-size compact wrench head/handle and an envelope bounding a±15° stroke. The route enters through the open coin door, passes above retained S1 equipment, rises after the front relief and approaches behind the plunger. This is not a4 mm rod test. Four adjustment/retention paths pass; minimum modeled clearance is2.5 mm for adjustment and6.5 mm for retention. Eight side-screw driver corridors also pass with the playfield module removed for initial installation/rare body replacement. Final physical ergonomics remain to be tested.

Native geometry preserves the original button service envelopes. Body-to-button wiring reserve is76 mm; body-to-S1 payload54.447 mm; body-to-SSF64.803 mm. No button, plunger, shelf, captured-shell or leg interface moves.

Service0→50°, vertical48 mm lift-out, rear-dowel seating and subsequent2→0° lowering, and populated backbox0→90° fold pass. Initial release has an exact separating half-space proof; remaining intervals use conservative motion bounds plus B-rep checks, not just endpoint pictures. Front bolts must be released, main playfield glass/matrix removed as required and existing positive service props used. Backbox glass/cassette stay installed for backbox fold. The new receivers move with M025; landing bodies remain fixed.

## Planning load screen — not certification

Base mass comes from its actual B-rep at650 kg/m³:5.627535 kg. Existing dowel model:0.315265 kg. Strap-screw model:0.010883 kg. Actual strap/adapter/new receiver masses remain UNKNOWN; low/nominal/high allowances are explicit in [load-screen.json](load-screen.json). Nominal allowances are0.400/0.500/0.025 kg respectively. Display load uses its actual modeled center; no bounding-box plywood volume is used.

| Display payload kg | Complete moving planning mass kg | Rear dowel reaction N | Front pair reaction N | Each front pad N |
|---:|---:|---:|---:|---:|
| 10 | 16.879 | 64.895 | 100.628 | 50.314 |
| 12 | 18.879 | 71.620 | 113.516 | 56.758 |
| 15 | 21.879 | 81.708 | 132.848 | 66.424 |

All nine payload/hardware sensitivity combinations have positive reactions. For the15 kg nominal case, the inherited provisional2×force screen gives132.848 N per front body,7.174 Nm side-wall moment,99.636 N pull-out demand at each upper screw and33.212 N vertical shear demand per side screw. These are **demands, not allowable capacities**. Inclined-contact longitudinal reaction is23.202 N for the front pair at static15 kg nominal; the complete dowel/strap/side load path needs physical verification. This is no impact/drop/transport rating.

The equal-EI front-overhang analogy gives side/T1 ratios: tip moment0.573, tip deflection tendency0.188; uniform front-overhang moment0.328 and deflection tendency0.108. It does not establish actual whole-board deflection or certify the VESA load distribution. Side screw pull-out/shear at12 mm embedment, plywood/adhesive, receiver pull-out, pad articulation, uplift retention and cyclic/nudge behavior require physical qualification.

## Manufacturing, BOM and packaging

- Before:101 wood /97 CNC /4 SW01 /59 families.
- After:**107 wood /103 CNC /4 SW01 /65 finished families**.
- 45 ONE_SIDE_CNC_READY; 58 ONE_SIDE_CNC_PLUS_MANUAL_FINISH;4 shop-made SW01. All statuses still subject to release gates.
- Six added layers reconstruct exactly, zero B-rep difference; all101 earlier piece geometries are unchanged. M025's row gains mandatory receiver manual-finish/HOLD metadata only.
- Added finished reference wood:0.316651 kg. Delivered six unbored contour blanks:0.334152 kg. Finished-reference planning wood total:**60.707838 kg**; delivered-planning wood total:**60.725339 kg**. Difference is explicitly reserved manual bore stock, not silently discarded shipping mass.
- 162 catalog families,11 new provisional families. 40 required Fxx models; **176 known minimum fasteners + formula-dependent + genuinely TBD**. All11 new actual hardware masses remain UNKNOWN.
- Preliminary5-sheet projection retained; six small18 mm pieces use the existing offcut/nesting space. No stock rationalization or production nesting is authorized. Preferred25 kg packaging study retains4 wood bundles with separate hardware box; [package contents/dimensions](packaging.json) include delivered blank mass and high-density allowance. This near-limit estimate is not a shipping weight guarantee.

[Hardware BOM](landing-hardware-bom.csv) · [hardware holds/sources](hardware-status.md) · [manufacturing BOM](manufacturing-bom.md) · [PT-BR BOM](manufacturing-bom.pt-BR.md) · [manufacturing audit](manufacturing-audit.json) · [mass/packing comparison](manufacturing-metrics-comparison.json)

## Viewer, manual and validation

PLAYFIELD LANDINGS can be hidden/isolated; the support-path preset exposes both load paths. Selection gives manufacturing and hardware IDs. Updated animations show captive-bolt release, rear seating, front approach and final contact; no T1 support is depicted. The bilingual manual explains tolerance-only leveling, guided manual receivers, adjuster locknuts, jam-stop resetting, tool access and service prerequisites. EN default/PT-BR, Original/Accessible palettes, tablet controls and offline operation are retained.

Validation: 7 native geometry gates; 11 motion gates; 4 internal-hardware gates;4 operational access paths plus8 mounting-driver paths;9 load scenarios;18 support-closure gates. The [complete regression](validation.json) and [offline Chromium check](browser-validation.json) record the final exact hashes and check counts.

Every original installed object and previous manufacturing B-rep is preserved. Absolute datums remainY89/Y127 atlocal top−65,52 mm side insets,396 mm front width,87 mm relief length,R8, rear180×110R8 window, VESA/strain slots, SW01/M006/M067, all shelves/crossmembers andWPC axisY1066.8/Z508. Only the new landing wood/hardware and documentation metadata are added.

**Full-sheet CNC release remains BLOCKED.** Actual plywood, actual display/adapter, actual landing hardware, coupon-selected fit, guided manual interfaces and structural/ergonomic qualification are PENDING. Source links demonstrate available hardware families only, never selection of a final SKU or manufacturing dimensions.

## Native review views

- [01 — Previous closed pose — front support absent](01-review.png)
- [02 — Crossmember clearance is intentional after front support](02-review.png)
- [03 — T1 shoes — comparison only](03-review.png)
- [04 — Front-side search — earliest simple body](04-review.png)
- [05 — Selected landing — three 18 mm layers](05-review.png)
- [06 — Button and plunger service clearance](06-review.png)
- [07 — Positive body-to-side attachment](07-review.png)
- [08 — Adjuster stack — pad thickness included](08-review.png)
- [09 — M025 contact footprint — useful continuous wood](09-review.png)
- [10 — Left/right leveling — preserve current playing slope](10-review.png)
- [11 — Front overhang — 245 mm versus 380 mm support](11-review.png)
- [12 — Explicit closed load path](12-review.png)
- [13 — Early opening — pads release cleanly](13-review.png)
- [14 — 50° playfield service](14-review.png)
- [15 — 48 mm lift-out — clear vertical extraction](15-review.png)
- [16 — Uplift retention is separate from gravity support](16-review.png)
- [17 — Complete cabinet — closed supported playfield](17-review.png)
- [18 — Landing hardware — semantic exploded review](18-review.png)

## Reproduction and authority

`python3 tools/rebuild_front_landings_v3363.py` rebuilds native evidence sequentially. Review rendering, focused browser QA, full regression, report generation and promotion are explicit subsequent gates. See the scripts beside that driver. Supplier table/sheet/tool/spacing values are unchanged; no G-code or full-sheet production cutting file is emitted.

Original project material: CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet . Preserve NOTICE.md. No third-party CAD was copied.

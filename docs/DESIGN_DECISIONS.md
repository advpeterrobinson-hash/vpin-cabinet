# Design Decisions

Current authority: [active baseline](ACTIVE_ENGINEERING.md). Earlier decisions below are historical where superseded by DEC-020/021.

This log records decisions that materially constrain the cabinet design. New decisions should be appended rather than silently rewriting history.

## DEC-011 — Windows runtime, Linux/FreeCAD engineering

**Status:** provisional/accepted for current planning

Develop the cabinet CAD/tooling on Linux with FreeCAD and Git. The finished pinball computer is presently planned around Windows because the complete VPX/PinUP Popper/legacy DOF ecosystem is more mature there.

This decision may be revisited if the Linux pinball ecosystem reaches equivalent compatibility before software commissioning.

## DEC-012 — Cutter CNC consultation

**Status:** accepted

Cutter CNC (`cuttercnc.com`, Brazil) is the prospective CNC fabrication provider. Before manufacturing files are frozen, confirm their preferred file/layer conventions, available tooling, internal-radius requirements, two-sided registration process, material sourcing, and practical tolerances.

## DEC-013 — Future-proof electronics envelopes over exact historical dimensions

**Status:** accepted; supersedes DEC-001 where there is a conflict

The cabinet and structural metalwork are expected to outlive multiple generations of TVs, PC hardware, controller boards, amplifiers, and power supplies. Exact Williams dimensions are therefore a design reference rather than a manufacturing mandate.

The owner explicitly approves approximately **10–50 mm** dimensional deviations where they materially improve future replacement compatibility, service access, structural margin, cable/connector access, modular mounting, or availability of generic replacement hardware.

Permanent structure should use service envelopes and replaceable interfaces. Component-specific geometry should move into replaceable carriers, bezels, filler panels, and adapters where practical.

The main playfield cabinet width was subsequently selected at **580 mm** under DEC-015 to provide a larger future 42-inch-class service envelope while retaining the Williams visual character.

## DEC-014 — Future-proof backbox width and modular monitor carrier

**Status:** accepted for v0.6 engineering

Increase the backbox target outer width from the 730.25 mm reference to **780.0 mm**. This +49.75 mm deviation intentionally uses the owner-approved tolerance to avoid locking the cabinet to unusually narrow 31.5–32 inch displays.

Target monitor service envelope:

- width: 740 mm
- height: 450 mm
- depth: 100 mm

The permanent shell uses a removable/slotted monitor carrier plus a removable cosmetic bezel/filler panel. The exact backglass model is therefore not required before the permanent backbox shell is CNC-cut; it is only required before its carrier and bezel are finalized.

## DEC-015 — 580 mm CNC-flatpack main body

**Status:** superseded by DEC-020

Adopt **580.0 mm** as the main cabinet outer-width engineering baseline. The goal is not millimetre-perfect Williams replication; the goal is a long-lived, future-proof cabinet that can be replicated from CNC plans.

The target future playfield service envelope is approximately 560 × 950 × 55 mm with 2 mm installation clearance per side. The initial LG OLED42C5 remains comfortably inside that envelope.

A custom-width lockdown bar is explicitly acceptable and is not a blocker. Siderails, brackets, and other simple metal parts may likewise be supplied as dimensioned DXF/PDF fabrication drawings so a local shop can make them without requiring the builder to own metalworking equipment.

The final project should be buildable in an apartment from outsourced CNC/fabricated parts using ordinary hand tools rather than table saws, routers, drill presses, or welding equipment.

## DEC-016 — Replaceable service-I/O fascias with vintage white engraving

**Status:** accepted for v0.8 engineering

Use three service/control zones: separated rear power fascia, rear low-voltage service-I/O fascia, and hidden coin-door/under-front service/control panels.

Permanent cabinet panels receive simple rectangular service-bay openings. Connector-specific geometry belongs on small replaceable fascias/carriers so USB, HDMI, network, and other standards can be changed years later without recutting the cabinet.

The visual language is intentionally inspired by vintage hi-fi / laboratory equipment: dark wood or black-finished wood with shallow **white-filled CNC engraving** for connector names, borders, scales, and service legends.

Initial rear service ports are RJ45 Ethernet (`NETWORK`), HDMI diagnostic output (`SERVICE DISPLAY`), USB-A (`USB SERVICE`), USB-C, and one blank `RESERVE` position.

The rear mains bay remains physically separated and internally enclosed; the decorative wooden fascia is not relied upon as the electrical safety enclosure.

## DEC-017 — Fold-down WPC-style backbox for transport

**Status:** accepted engineering baseline for v0.10

Use a Williams/Bally WPC-style external side-pivot hinge arrangement so the complete backbox folds **forward over the playfield** for transport, storage, and moving through apartments/elevators/vehicles.

Preferred off-the-shelf hardware family:

- `01-9011-L/R` left/right WPC backbox hinge brackets;
- `02-4352` pivot bushings;
- `4322-01139-12B` pivot bolts.

The main-side pivot starts from the established WPC datum of approximately 508.0 mm above the cabinet bottom and 38.1 mm forward of the rear edge, using a 12.7 mm pivot hole.

For the selected 780 mm backbox over the 580 mm main body, use the WPC custom-width hinge-floor formula. It yields a hinge mounting-row inset of approximately **69.84 mm from each backbox-floor side edge**.

Two independent upright safety bolts clamp the backbox floor to the cabinet rear shelf/crossmember. The hinges are not relied upon as the sole upright restraint.

The folded backbox must rest on dedicated padded structural transport supports, never on the backglass display, speaker grilles, playfield OLED, or playfield glass. The front backbox fascia should therefore keep displays/speakers recessed behind a defined fold datum; protruding decorative speaker covers are to be avoided or made deliberately removable.

A protected cable service loop must permit folding without disconnecting normal HDMI/video, power, audio, USB, or lighting harnesses and without pinching cables at the hinge.

All pivot, hinge, lock, cable-opening, and transport-rest locations are CNC-located in the final flat-pack files. Hand-aligning and drilling the hinge during apartment assembly is explicitly not the release workflow.

## DEC-018 — Dedicated cooling, cable passports, and toy-routing infrastructure

**Status:** accepted engineering baseline for v0.11

Treat ventilation, toys, power distribution and cable support as structural/CNC design inputs rather than late-stage accessories.

Backbox ventilation uses a dedicated fused **AUX 12 V** cabinet bus and a standalone thermostat/PWM controller, with two quiet 120 mm exhaust-fan positions high on the backbox rear panel as the baseline. Cooling must not depend on a motherboard fan header, display USB port or the Windows operating system.

The cabinet reserves separate routing classes for AC mains, high-current DOF/DC power, logic/data/LED wiring, low-level audio and moving display harnesses. AC mains remains physically separated from low-level wiring; inductive/high-current toy wiring is likewise routed away from audio/data where practical.

The folding backbox receives two designed cable passages rather than one improvised hole: a primary **90 × 50 mm** rounded/grommeted passport with ~300 mm folding service loop, plus a reserve **60 × 40 mm** passport with removable blanking cover.

Harness supports are CNC-located. Fixed harnesses target support spacing <=250 mm; moving/hinge harnesses target <=100 mm near the moving zone. Adhesive-only tie bases are not accepted as the primary support method.

Before cabinet CNC geometry is frozen, the physical zoning/routing system must reserve capacity for a full-DOF class build including flipper/slings/bumper impact outputs, shaker, gear motor, knocker, chimes/bells, blower, strobes, RGB flashers, beacon/siren-light effects, addressable LEDs, illuminated controls and a future powered topper.

This is a packaging/power-domain decision, not yet a final toy shopping list. Exact voltage, fuse, wire-gauge, connector and controller-board selections remain BOM-stage decisions based on final hardware ratings and measured current.

## DEC-019 — Closed, structurally braced and child-resistant backbox enclosure

**Status:** accepted engineering baseline for v0.12

The adjustable monitor/DMD mounting system does **not** imply an open backbox. The backbox remains a closed wooden enclosure with a continuous fixed rear structural shear panel.

Baseline structure uses nominal 18 mm perimeter panels with a fixed rear plywood shear panel of at least 12 mm, captured into dados/rabbets as final CNC joinery dictates. The adjustable aluminium display subframe transfers monitor/DMD loads into dedicated top/bottom crossmembers and side/perimeter structure; the rear plywood panel is not the sole display support.

Normal monitor/DMD replacement is through the front. Large hand-removable rear panels are prohibited. Any future rear service hatch must require a tool and use captive/tamper-resistant fasteners or a keyed lock.

All penetrations are guarded/sealed rather than left open:

- backglass behind removable tempered glass or impact-resistant clear polycarbonate;
- DMD behind a closed window/bezel;
- speaker openings behind rigid perforated/finger-safe grilles plus acoustic material;
- ventilation openings behind rigid finger guards and removable fine insect mesh/filter;
- floor/shelf interface sealed with replaceable closed-cell gasket;
- active cable passport finished with a split compression/gland interface;
- reserve passport gasketed and blanked when unused.

No exposed mains terminals are permitted in the backbox. Fans and most auxiliaries remain on SELV/DC rails. If the backglass display requires AC mains, it receives power through fully insulated jacketed wiring and a touch-safe enclosed connector/receptacle; any unavoidable mains splice is confined to a tool-access-only enclosed junction compartment.

The intent is not to claim a formal IP rating. The intent is a strong, closed cabinet that resists insect/dust entry, prevents casual child access, prevents fingers/tools from reaching hazardous energized parts, and remains fully serviceable through deliberate tool-controlled access.

## DEC-020 — 600 mm main cabinet width for full-thickness 42/43-inch playfield bay

**Status:** owner accepted on 2026-09-15; selected production-direction baseline

Increase the main cabinet outer width from the previous 580 mm engineering baseline to **600.0 mm**.

With nominal 18 mm plywood sides, the full-thickness clear internal width becomes **564.0 mm**. This exactly accommodates the current model-agnostic playfield target of **560 mm maximum physical display cross-width plus 2 mm installation clearance per side** without routing long clearance pockets into the cabinet sidewalls.

Relative to the Williams WPC standard-body reference of 558.8 mm, the selected cabinet is 41.2 mm wider overall, or 20.6 mm per side. This deviation is accepted because it materially improves future display compatibility, structural simplicity, serviceability, and CNC repeatability while remaining visually close to a standard-body machine.

The 780 mm backbox is retained. Its nominal overhang over the 600 mm body becomes **90 mm per side**.

The playfield display remains selected late from the Brazil market. Permanent woodworking must not encode one TV model's VESA pattern. The cradle uses replaceable adapters, and gas-strut force/mount geometry remains a final-display-dependent calibration step.

DEC-020 supersedes the 580 mm width selection in DEC-015. Width-dependent CAD, metalwork and CNC parts must now migrate to the 600 mm datum before manufacturing release.


## DEC-021 — Fresh active source build and lower rear CPU service

Owner-directed 2026-09-16: preserve 600 mm body, classic legs/external skates and dual playfield stays. Use one 285 × 460 mm PC shelf at Z135, 340 × 240 hatch at Z110, 364 × 264 door at Z98 opening 105° outward. No dedicated CPU harness, intermediate PC sled, integrated wheels or large leg corner furniture.

Build a fresh active document from selected config/builder sections; do not delete/reparent historical master geometry. Save the active output separately and preserve the owner's working FCStd. No historical FCStd is a dependency of the fresh build. The low utility fascia window design remains a structural/hardware gate; never cut through the bottom capture or rear leg brackets merely to match a presentation target.


## DEC-022 — Minimal fixed utility functions; preserve low rear CPU geometry

Owner-directed: remove permanent rear SERVICE HDMI / USB-A / USB-C / RESERVE. The extended PC exposes troubleshooting ports. PC POWER / RESET / DOF SERVICE remain at the coin door. Keep mains/master disconnect plus optional Ethernet only. Remove decorative wood fascias. Protect bottom capture and rear leg load paths. Preserve CPU aperture Z110..350, shelf Z135 and outward door.

Owner selected two small rear-face carriers (A). Underside B is rejected and archived. Only 70×50 and 24×24 mm generic rear apertures are modeled; component patterns remain blocked. This supersedes DEC-021's low utility-window study and the earlier unselected comparison. Keep CPU heights unchanged and preserve unused upper rear space.

Combine each overlapping landing/latch doubler pair into one union retaining both load zones; active wood count becomes 36. Use 18 mm bottom-seated CPU support rails with local bolted angle clamps and underside backing. Measurement, fastener sizing and physical proof testing remain release gates.

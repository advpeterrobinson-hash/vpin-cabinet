# V32 — leaf pinball buttons and arcade alternative

Owner direction, 2026-09-29: traditional pinball leaf buttons are preferred for the side controls. Retain a conventional arcade-button option for other builders. This does not select front control hardware or release machining.

## Selected reference

[Arcade Express kit, product 538, supplied variant 12705](https://www.arcadexpress.com/en/pinball/538-12705-pinball-button-kit-with-end-of-stroke-switch-leaf-holder-bracket-nut.html), accessed 2026-09-29. The seller describes a Suzo Happ pinball button, leaf switch, bracket/nut and screws; its own bracket is printed in PLA. The listing specifies a 15 mm diameter but also mentions 34 mm in inconsistent inch wording. It provides no verified dimensioned mounting stack in the reviewed text. Neither value is adopted as a drilling instruction. Exact button manufacturer part number, usable thread, panel range and bracket dimensions remain unconfirmed.

This is the owner's preferred style/reference, not a purchase record. No vendor photographs, bracket model or drawings are copied into the repository.

## Why the holes are not automatically interchangeable

Leaf describes the contact mechanism; it does not define the button barrel or panel hole. Head/flange diameter, threaded barrel diameter, through-hole and recess diameter are separate measurements.

| Option | Evidence | Project treatment |
|---|---|---|
| Preferred pinball leaf kit | Seller lists 15 mm, with ambiguous additional diameter wording | Measure/obtain a drawing of the complete kit before setting the hole and recesses |
| Conventional SUZOHAPP arcade microswitch families | Manufacturer flyer specifies a 1-1/8 inch mounting hole = 28.575 mm and panels up to 3/4 inch | Concrete alternative family; select exact part before checking nut, body, terminals and access |
| Current saved V32 sides | Ø15.875 bore, Ø28.575 recesses, 5.3 mm remaining annular web | Existing reference geometry only; neither kit fit nor strength is established |

Arcade source: [SUZOHAPP pushbutton flyer](https://na.suzohapp.com/pdf/pushbutton_flyer.pdf). This is not a claim that all arcade buttons share one size. The [owner's cabinet PDF](CABINET_DIMENSIONS_REFERENCE_V32.md) likewise cannot establish which physical button its holes accept.

## Simple implementation direction

Develop two explicitly named machining configurations, **pinball leaf** and **arcade**, selected before CNC cutting. Preserve common cabinet datums and intended button centers where the complete assemblies permit. Each configuration must define its own bore, recesses, panel engagement and internal service envelope; export only the chosen configuration. These variants are a plan, not implemented CAD or confirmed interchangeability.

Do not enlarge the leaf hole to the arcade size by default. A universal oversized opening with a reducer or replaceable mounting patch adds a new retention/seating interface; consider that only if later in-place interchangeability is needed. The current owner request establishes builder choice, not a requirement for tool-free conversion of an already cut cabinet.

Next qualification: barrel and flange, thread/nut engagement, minimum recess, leaf travel and adjustment access, bracket orientation/fasteners, wire exits and switch removal on both sides. Replace the provisional cylindrical button envelope with the complete kit envelope before claiming clearance to guides, shelves or SSF. Preserve the simplest sufficient panel stack; the existing 5.3 mm web is not an approved target.

No CAD geometry changed for this reference registration; no new fit/structural test is claimed. See [side interface plan](SIDE_INTERFACE_PLAN_V32.md).

Original assessment: CERN-OHL-S-2.0. Preserve LICENSE and NOTICE.md. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

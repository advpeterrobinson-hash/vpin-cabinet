# V33 mechanical hardware library

This library inventories the accepted CURRENT V32 design at `0aa4ea77531c59274a0b8547a71e731626bd2cf2`. It does not replace the geometry authority in `config/current_v32.json`.

- [Canonical catalog](../../config/hardware_catalog_v33.json): permanent IDs, purchasing class, quantities, measurement holds and installed metadata.
- [Wood/material map](../../config/wood_materials_v33.json): every CURRENT plywood component, plus the independently configurable premium-first nesting policy.
- [Audit and decisions](../../studies/hardware-v33/README.md).
- [BOMs and CAD review gallery](../../exports/generated/hardware-v33/index.html).

`F` identifies a fastener/interface family; `W` a washer; `I` a captive thread/nut; `H` a mechanism; `B` a fitting; `G` a gasket, glass or consumable; `E` an electronic reference; `R` a nonphysical reserve. `P` IDs identify wood components. IDs are never renumbered or reused. `W04` and `W05` are aliases of `W02`, not additional purchases.

Each canonical family has a lightweight FCStd and JSON sidecar. Screws with a known provisional head/shank/length are generated parametrically without helical threads. Other models reuse original project B-rep envelopes. Unknown interfaces use an orange cross marker, explicitly **not hardware geometry**. The WPC arm uses the current gross reserve; bushing/bolt cylinders are original positive-control topology schematics with unmeasured head, neck and fit dimensions. None of these models authorizes drilling, collision certification of selected hardware or fabrication.

The catalog gives each object's installed bounding-box center, identified as a placement reference rather than a hole datum. Installation vectors are supplied when supported by the source; unknown vectors and unmodeled coordinates remain null with a reason. Geometry used for a representative library model is centered locally. Future exploded views must use catalog instances, not that local origin as an installed coordinate.

One purchased hinge may have three CAD objects; one keyed lock may have body, barrel and tongue. These are counted as one mechanism. Conversely, a compound plywood solid is not automatically one CNC cut part. Wood decomposition holds remain explicit.

The basic kit includes the two backbox fan blanks and their station hardware. Fitting fans substitutes the station bolts; it does not double them. Shared washers retain separate mandatory/optional usage rows. Tether retention rings may be supplied with a knob: confirm kit contents before ordering them separately.

All models and code here are original project material under CERN-OHL-S-2.0. No vendor STEP, proprietary CAD, standard drawing or downloaded document is redistributed. External sources are links and provenance only; see [source register](sources.json). Preserve the repository LICENSE and NOTICE, including Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet.

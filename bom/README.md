# Active BOM entry point

Use `ACTIVE_PARTS.csv` for current wooden-part dispositions and nominal local envelopes, and `HARDWARE_FREEZE_V25.csv` for hardware gates. The generated register is rebuilt as `exports/generated/active-parts.csv`; reconcile it before release.

Older `STRUCTURE_BOM.csv`, `WOOD_PARTS.csv`, and versioned service BOMs contain superseded purchasing/part concepts. They are historical engineering records, not an active shopping list. In particular do not order built-in wheels, a front PC drawer, a lift-out sled or a second PC carrier from those files.

Every active machining record is BLOCKED. Local envelopes are not finished cut sizes, and 36 mm laminated assemblies still need per-lamination release IDs. The CPU supports are now 18 mm plywood rails seated on the bottom, with measured local metal clamp/backing hardware still required. The register has 32 active wood records: 29 permanent structure, two doors and the CPU board. `REMOVABLE_CARRIERS_V27.csv` lists 11 carriers separately, including that same CPU board; do not double-count it. See `BLOCKED_CNC_FEATURES_V25.csv` for the measured-hardware subset.

Utility A rear face is owner-selected; two generic apertures are active engineering geometry. Underside B is rejected. Hardware-specific machining and purchasing remain blocked. See `docs/REAR_UTILITY_V26.md`.

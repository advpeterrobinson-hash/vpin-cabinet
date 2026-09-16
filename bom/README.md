# Active BOM entry point

Use `ACTIVE_PARTS.csv` for current wooden-part dispositions and nominal local envelopes, and `HARDWARE_FREEZE_V25.csv` for hardware gates. The generated register is rebuilt as `exports/generated/active-parts.csv`; reconcile it before release.

Older `STRUCTURE_BOM.csv`, `WOOD_PARTS.csv`, and versioned service BOMs contain superseded purchasing/part concepts. They are historical engineering records, not an active shopping list. In particular do not order built-in wheels, a front PC drawer, a lift-out sled or a second PC carrier from those files.

Every active machining record is BLOCKED. Local envelopes are not finished cut sizes, and 36 mm laminated assemblies still need per-lamination release IDs. The 25 mm CPU rail section is a packaging target, not a specified plywood stock thickness.

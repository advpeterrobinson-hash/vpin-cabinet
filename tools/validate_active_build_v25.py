#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "active_build_v25.json"
FREEZE = ROOT / "bom" / "HARDWARE_FREEZE_V25.csv"
V24 = ROOT / "config" / "cabinet_rear_cpu_shelf_v24.json"
V20 = ROOT / "config" / "cabinet_structure_v20.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    v24 = json.loads(V24.read_text(encoding="utf-8"))
    v20 = json.loads(V20.read_text(encoding="utf-8"))
    with FREEZE.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    cab = v20["cabinet"]
    pc = v24["pc_shelf"]
    door = v24["rear_service_door"]
    gate = cfg["cnc_release_gate"]

    freeze_classes = {r["freeze_class"] for r in rows}
    geometry_rows = [r for r in rows if r["freeze_class"] == "MEASURE_BEFORE_CNC"]
    unresolved = [r["item_id"] for r in geometry_rows if r["status"] != "FROZEN"]

    checks = [
        ("600 mm active body", abs(float(cab["outer_width_mm"]) - 600.0) <= 0.01, str(cab["outer_width_mm"])),
        ("rear CPU shelf is active service", float(pc["travel_mm"]) >= 400.0 and door["routine_pc_service_requires_playfield_open"] is False, f"travel={pc['travel_mm']} / playfield={door['routine_pc_service_requires_playfield_open']}"),
        ("assembly forbids freehand structural layout", cfg["assembly_policy"]["builder_freehand_structural_layout_allowed"] is False, str(cfg["assembly_policy"]["builder_freehand_structural_layout_allowed"])),
        ("release requires CNC-located hinge patterns", "hinge patterns" in cfg["assembly_policy"]["release_cnc_must_include"], "hinge patterns"),
        ("release requires CNC-located slide patterns", "slide patterns" in cfg["assembly_policy"]["release_cnc_must_include"], "slide patterns"),
        ("hardware freeze manifest populated", len(rows) >= 20, f"{len(rows)} rows"),
        ("hardware freeze classes complete", {"MEASURE_BEFORE_CNC", "DIMENSIONED_LOCAL_FAB", "ADAPTER_ONLY", "NO_CNC_DEPENDENCY"}.issubset(freeze_classes), ", ".join(sorted(freeze_classes))),
        ("unfrozen geometry blocks CNC release", bool(unresolved) and gate["cnc_ready"] is False, f"{len(unresolved)} unresolved geometry items / CNC_READY={gate['cnc_ready']}"),
        ("prototype dry-fit required", gate["prototype_dry_fit_required"] is True, str(gate["prototype_dry_fit_required"])),
        ("unresolved hand layout forbidden", gate["unresolved_hand_layout_operations_allowed"] is False, str(gate["unresolved_hand_layout_operations_allowed"])),
        ("superseded center/front PC concepts listed", "center-directed PC service shelf" in cfg["superseded_active_concepts"] and "front-moving PC drawer" in cfg["superseded_active_concepts"], "listed"),
        ("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])),
    ]

    print("ACTIVE BUILD v0.25 VALIDATION")
    print("=" * 80)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<50} {detail}")
        ok = ok and passed

    print()
    print(f"Hardware freeze rows                 {len(rows)}")
    print(f"MEASURE_BEFORE_CNC still open        {len(unresolved)}")
    if unresolved:
        print("Open geometry items                  " + ", ".join(unresolved))
    print("STATUS", "PASS - active build simplification policy" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

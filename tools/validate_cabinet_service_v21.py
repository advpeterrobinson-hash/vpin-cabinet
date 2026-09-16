#!/usr/bin/env python3
"""Validate v0.21 classic-leg / PinSkates / lift-out-PC service architecture."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cabinet_service_v21.json"
V20 = ROOT / "config" / "cabinet_structure_v20.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    v20 = json.loads(V20.read_text(encoding="utf-8"))

    mob = cfg["mobility"]
    leg = cfg["leg_corners"]
    pc = cfg["pc_service"]

    outer = float(v20["cabinet"]["outer_width_mm"])
    wood = float(v20["cabinet"]["nominal_wood_mm"])
    inner_x0 = wood
    inner_x1 = outer - wood

    tray_x0 = float(pc["tray_x_mm"])
    tray_x1 = tray_x0 + float(pc["tray_width_x_mm"])
    tray_y0 = float(pc["tray_y_mm"])
    tray_y1 = tray_y0 + float(pc["tray_depth_y_mm"])

    cross = [float(y) for y in v20["cnc_joinery"]["crossmember_y_mm"]]
    mid_y, rear_y = cross[1], cross[2]

    chassis_w, chassis_d, chassis_h = [float(v) for v in pc["open_chassis_reference_mm"]]

    checks: list[tuple[str, bool, str]] = []
    checks.append(("classic legs retained", "classic pinball legs" in mob["playing_support"].lower(), mob["playing_support"]))
    checks.append(("PinSkates-style external mobility selected", "pinskates" in mob["moving_method"].lower(), mob["moving_method"]))
    checks.append(("no integrated casters", mob["integrated_casters"] is False and mob["retractable_wheels"] is False, "integrated/retractable false"))
    checks.append(("no internal wheel keepouts required", mob["cabinet_internal_wheel_keepouts_required"] is False, str(mob["cabinet_internal_wheel_keepouts_required"])))
    checks.append(("large plywood leg doublers removed", leg["large_plywood_doublers"] is False, str(leg["large_plywood_doublers"])))
    checks.append(("compact steel leg bracket >=3 mm", float(leg["steel_bracket_nominal_thickness_mm"]) >= 3.0, f"{leg['steel_bracket_nominal_thickness_mm']} mm"))
    checks.append(("leg holes remain hardware-gated", "BLOCKED" in leg["exact_leg_hole_pattern"], leg["exact_leg_hole_pattern"]))
    checks.append(("leg proof test required", bool(leg["proof_test_required"]), str(leg["proof_test_required"])))
    checks.append(("PC uses lift-out sled", "lift-out" in pc["architecture"].lower(), pc["architecture"]))
    checks.append(("PC has no forward/front exit", pc["front_exit_required"] is False and pc["drawer_slides_required"] is False, "no front exit / no slides"))
    checks.append(("PC tray fits cabinet width", tray_x0 >= inner_x0 and tray_x1 <= inner_x1, f"X {tray_x0:.1f}..{tray_x1:.1f} / inner {inner_x0:.1f}..{inner_x1:.1f}"))
    checks.append(("PC tray fits between mid/rear crossmembers", tray_y0 > mid_y and tray_y1 < rear_y, f"Y {tray_y0:.1f}..{tray_y1:.1f} between {mid_y:.1f}/{rear_y:.1f}"))
    checks.append(("reference chassis fits tray", chassis_w <= float(pc["tray_width_x_mm"]) and chassis_d <= float(pc["tray_depth_y_mm"]), f"chassis {chassis_w:.0f}x{chassis_d:.0f}, tray {pc['tray_width_x_mm']}x{pc['tray_depth_y_mm']}"))
    checks.append(("vertical service lift reserved", float(pc["lift_service_height_mm"]) >= chassis_h + 100.0, f"lift {pc['lift_service_height_mm']} vs chassis H {chassis_h}"))
    checks.append(("PC quick-disconnect required", bool(pc["quick_disconnect_harness_required"]), str(pc["quick_disconnect_harness_required"])))
    checks.append(("PC proof-test target retained", float(pc["proof_test_payload_kg"]) >= 25.0, f"{pc['proof_test_payload_kg']} kg"))
    checks.append(("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])))

    print("CABINET SERVICE / MOBILITY v0.21 VALIDATION")
    print("=" * 78)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<48} {detail}")
        ok = ok and passed

    print()
    print("STATUS", "PASS - v0.21 service architecture" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

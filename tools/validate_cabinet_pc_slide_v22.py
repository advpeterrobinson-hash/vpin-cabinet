#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cabinet_pc_slide_v22.json"
V20 = ROOT / "config" / "cabinet_structure_v20.json"


def close(a: float, b: float, tol: float = 0.05) -> bool:
    return abs(a - b) <= tol


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    v20 = json.loads(V20.read_text(encoding="utf-8"))
    pc = cfg["pc_slide"]
    case = cfg["open_pc_case_reference"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_wood_mm"])
    inner = outer - 2.0 * wood

    shelf_w = float(pc["shelf_width_x_mm"])
    shelf_d = float(pc["shelf_depth_y_mm"])
    shelf_x = float(pc["shelf_x_mm"])
    stowed_y = float(pc["shelf_stowed_y_mm"])
    service_y = float(pc["shelf_service_y_mm"])
    travel = stowed_y - service_y
    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])

    case_w = float(case["width_mm"])
    case_d = float(case["depth_mm"])
    margin_x = (shelf_w - case_w) / 2.0
    margin_y = (shelf_d - case_d) / 2.0

    left_slide_outer = shelf_x - slide_t
    right_slide_outer = shelf_x + shelf_w + slide_t
    nominal_shelf_w = inner - 2.0 * slide_t
    nominal_shelf_x = wood + slide_t

    checks = [
        ("single flat shelf architecture", "single flat internal sliding shelf" in pc["architecture"], pc["architecture"]),
        ("no front cabinet exit", pc["front_cabinet_exit_required"] is False, str(pc["front_cabinet_exit_required"])),
        ("shelf remains within full-thickness cabinet bay", shelf_x >= wood - 0.05 and shelf_x + shelf_w <= outer - wood + 0.05, f"X {shelf_x:.1f}..{shelf_x+shelf_w:.1f} / bay {wood:.1f}..{outer-wood:.1f}"),
        ("shelf width derives from cabinet minus slides", close(shelf_w, nominal_shelf_w), f"shelf {shelf_w:.3f} / derived {nominal_shelf_w:.3f} mm"),
        ("shelf centered between direct side slides", close(shelf_x, nominal_shelf_x), f"shelf X {shelf_x:.3f} / derived {nominal_shelf_x:.3f} mm"),
        ("slide thickness fits each side", left_slide_outer >= wood - 0.05 and right_slide_outer <= outer - wood + 0.05, f"slide outer X {left_slide_outer:.3f}..{right_slide_outer:.3f} / bay {wood:.3f}..{outer-wood:.3f}"),
        ("300 mm slide travel", abs(travel - float(pc["travel_mm"])) <= 0.01 and abs(travel - 300.0) <= 0.01, f"{travel:.1f} mm"),
        ("service position remains well behind cabinet front", service_y >= 300.0, f"front edge Y={service_y:.1f} mm"),
        ("stowed shelf fits cabinet length", stowed_y + shelf_d <= float(cab["side_length_mm"]) - wood, f"rear edge Y={stowed_y+shelf_d:.1f} mm"),
        ("open case fits shelf width", margin_x >= float(case["required_edge_margin_x_mm"]), f"margin {margin_x:.1f} mm/side"),
        ("open case fits shelf depth", margin_y >= float(case["required_edge_margin_y_mm"]), f"margin {margin_y:.1f} mm/end"),
        ("case bolts directly to shelf", "bolts directly" in pc["case_mounting"], pc["case_mounting"]),
        ("no second sled", "no second removable sled" in pc["case_mounting"], pc["case_mounting"]),
        ("positive stowed retention", bool(pc["stowed_positive_retention_required"]), pc["stowed_retention_concept"]),
        ("slide holes blocked", "BLOCKED" in pc["slide_mounting_holes_status"], pc["slide_mounting_holes_status"]),
        ("case holes blocked", "BLOCKED" in pc["case_mounting_holes_status"], pc["case_mounting_holes_status"]),
        ("slides have proof-test margin", float(pc["minimum_slide_pair_rating_kg"]) >= 1.5 * float(pc["proof_test_payload_kg"]), f"rating {pc['minimum_slide_pair_rating_kg']} / proof {pc['proof_test_payload_kg']} kg"),
        ("v21 lift-out sled superseded", cfg["supersedes"]["v21_lift_out_pc_sled"] is True, str(cfg["supersedes"])),
        ("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])),
    ]

    print("CABINET PC SLIDE v0.22 VALIDATION")
    print("=" * 78)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<47} {detail}")
        ok = ok and passed

    print()
    print(f"Cabinet full-thickness inner width   {inner:.1f} mm")
    print(f"PC shelf                             {shelf_w:.1f} x {shelf_d:.1f} mm")
    print(f"Open case reference                  {case_w:.1f} x {case_d:.1f} x {case['height_mm']} mm")
    print(f"Service travel                       {travel:.1f} mm")
    print("STATUS", "PASS - simple PC slide packaging" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

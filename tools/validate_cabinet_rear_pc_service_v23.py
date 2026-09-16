#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cabinet_rear_pc_service_v23.json"
V20 = ROOT / "config" / "cabinet_structure_v20.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    v20 = json.loads(V20.read_text(encoding="utf-8"))
    door = cfg["rear_service_door"]
    pc = cfg["pc_slide"]
    case = cfg["open_pc_case_reference"]
    safe = cfg["electrical_safety"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_wood_mm"])
    length = float(cab["side_length_mm"])
    rear_h = float(cab["rear_height_mm"])
    rear_inner_y = length - wood

    shelf_w = float(pc["shelf_width_x_mm"])
    shelf_d = float(pc["shelf_depth_y_mm"])
    shelf_t = float(pc["shelf_thickness_z_mm"])
    shelf_x = float(pc["shelf_x_mm"])
    stowed_y = float(pc["shelf_stowed_y_mm"])
    service_y = float(pc["shelf_service_y_mm"])
    shelf_z = float(pc["shelf_z_mm"])
    travel = service_y - stowed_y
    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])
    spacer = float(pc["side_spacer_rail_thickness_each_side_mm"])

    case_w = float(case["width_x_mm"])
    case_d = float(case["depth_y_mm"])
    case_h = float(case["height_z_mm"])
    mx = (shelf_w - case_w) / 2.0
    my = (shelf_d - case_d) / 2.0

    aperture_x = float(door["aperture_x_mm"])
    aperture_w = float(door["raw_aperture_width_x_mm"])
    aperture_z = float(door["aperture_bottom_z_mm"])
    aperture_h = float(door["raw_aperture_height_z_mm"])
    aperture_top = aperture_z + aperture_h

    stack_w = 2.0 * spacer + 2.0 * slide_t + shelf_w
    stowed_rear = stowed_y + shelf_d
    service_rear = service_y + shelf_d
    case_bottom = shelf_z + shelf_t
    case_top = case_bottom + case_h

    checks = [
        ("rear-door architecture explicit", "from behind" in pc["service_access"] and "rear service door" in pc["service_access"], pc["service_access"]),
        ("routine PC service does not require playfield", pc["routine_service_requires_playfield_open"] is False, str(pc["routine_service_requires_playfield_open"])),
        ("rear aperture fits PC shelf width", aperture_w >= shelf_w + 40.0, f"door {aperture_w:.1f} / shelf {shelf_w:.1f} mm"),
        ("rear aperture vertically fits shelf + case", shelf_z >= aperture_z and case_top <= aperture_top, f"stack Z {shelf_z:.1f}..{case_top:.1f} / door {aperture_z:.1f}..{aperture_top:.1f}"),
        ("rear door clears low rear I/O", aperture_z - float(door["rear_io_top_z_mm"]) >= float(door["minimum_vertical_gap_to_rear_io_mm"]), f"gap {aperture_z-float(door['rear_io_top_z_mm']):.1f} mm"),
        ("rear door clears rear leg bracket", aperture_z - float(door["rear_leg_bracket_top_z_mm"]) >= float(door["minimum_vertical_gap_to_leg_bracket_mm"]), f"gap {aperture_z-float(door['rear_leg_bracket_top_z_mm']):.1f} mm"),
        ("rear door leaves upper rear structure", rear_h - aperture_top >= 100.0, f"upper band {rear_h-aperture_top:.1f} mm"),
        ("small shelf fits cabinet width", shelf_x >= wood and shelf_x + shelf_w <= outer - wood, f"X {shelf_x:.1f}..{shelf_x+shelf_w:.1f} / bay {wood:.1f}..{outer-wood:.1f}"),
        ("slide/spacer/shelf stack matches inner width", abs(stack_w - (outer - 2.0 * wood)) <= 0.05, f"stack {stack_w:.1f} / inner {outer-2.0*wood:.1f} mm"),
        ("open case fits small shelf width", mx >= float(case["minimum_shelf_margin_x_each_side_mm"]), f"margin {mx:.1f} mm/side"),
        ("open case fits small shelf depth", my >= float(case["minimum_shelf_margin_y_each_end_mm"]), f"margin {my:.1f} mm/end"),
        ("shelf stows against rear without crossing panel", stowed_rear <= rear_inner_y + 0.05, f"rear edge {stowed_rear:.1f} / rear inner face {rear_inner_y:.1f} mm"),
        ("service travel is rearward", service_y > stowed_y and pc["travel_direction"].startswith("rearward"), f"Y {stowed_y:.1f}->{service_y:.1f}"),
        ("300 mm rearward travel", abs(travel - float(pc["travel_mm"])) <= 0.01 and abs(travel - 300.0) <= 0.01, f"{travel:.1f} mm"),
        ("service position pulls shelf outside rear", service_rear > length + 250.0, f"service rear edge {service_rear:.1f} / cabinet rear {length:.1f} mm"),
        ("case bolts directly to shelf", "bolts directly" in pc["case_mounting"], pc["case_mounting"]),
        ("positive stowed retention", bool(pc["stowed_positive_retention_required"]), pc["stowed_retention_concept"]),
        ("slide holes blocked", "BLOCKED" in pc["slide_mounting_holes_status"], pc["slide_mounting_holes_status"]),
        ("case holes blocked", "BLOCKED" in pc["case_mounting_holes_status"], pc["case_mounting_holes_status"]),
        ("service loop >=450 mm", float(pc["cable_service_loop_minimum_mm"]) >= 450.0, f"{pc['cable_service_loop_minimum_mm']} mm"),
        ("rear service keeps mains touch-safe", all(bool(v) for v in safe.values()), str(safe)),
        ("v22 center-service direction superseded", cfg["supersedes"]["v22_internal_center_service_direction"] is True, str(cfg["supersedes"])),
        ("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])),
    ]

    print("CABINET REAR PC SERVICE v0.23 VALIDATION")
    print("=" * 86)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<54} {detail}")
        ok = ok and passed

    print()
    print(f"Rear service aperture                {aperture_w:.1f} x {aperture_h:.1f} mm")
    print(f"PC shelf                             {shelf_w:.1f} x {shelf_d:.1f} x {shelf_t:.1f} mm")
    print(f"Open case reference                  {case_w:.1f} x {case_d:.1f} x {case_h:.1f} mm")
    print(f"Stowed / service shelf Y             {stowed_y:.1f} / {service_y:.1f} mm")
    print("STATUS", "PASS - rear PC service architecture" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

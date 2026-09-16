#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cabinet_rear_cpu_shelf_v24.json"
V20 = ROOT / "config" / "cabinet_structure_v20.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    v20 = json.loads(V20.read_text(encoding="utf-8"))
    door = cfg["rear_service_door"]
    pc = cfg["pc_shelf"]
    case = cfg["open_pc_case_reference"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_wood_mm"])
    inner = outer - 2.0 * wood
    rear_inner_plane = float(cab["side_length_mm"]) - wood

    sw = float(pc["shelf_width_x_mm"])
    sd = float(pc["shelf_depth_y_mm"])
    sx = float(pc["shelf_x_mm"])
    sy0 = float(pc["shelf_stowed_y_mm"])
    sy1 = float(pc["shelf_service_y_mm"])
    travel = sy1 - sy0
    cw = float(case["installed_width_x_mm"])
    cd = float(case["installed_depth_y_mm"])
    ch = float(case["installed_height_z_mm"])
    mx = (sw - cw) / 2.0
    my = (sd - cd) / 2.0
    aw = float(door["raw_aperture_width_x_mm"])
    ax = float(door["aperture_x_mm"])
    ah = float(door["raw_aperture_height_z_mm"])
    az = float(door["aperture_bottom_z_mm"])
    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])
    left_support = float(pc["fixed_support_left_x_mm"])
    right_support = float(pc["fixed_support_right_x_mm"])
    support_w = float(pc["fixed_support_rail_width_x_mm"])

    # In the service position the shelf itself intentionally leaves a small lip
    # inside the cabinet.  What matters is that the PC case is essentially fully
    # outside the rear plane, while the shelf/slide assembly retains controlled
    # overlap.  Do not require the shelf front edge itself to clear the cabinet.
    service_shelf_rear = sy1 + sd
    service_case_front = sy1 + my
    service_case_rear = service_case_front + cd
    outside_shelf_length = max(0.0, service_shelf_rear - rear_inner_plane)
    outside_shelf_fraction = outside_shelf_length / sd if sd else 0.0

    checks = [
        ("rear-only routine PC service", door["routine_pc_service_requires_playfield_open"] is False, str(door["routine_pc_service_requires_playfield_open"])),
        ("narrow shelf orientation", sw < sd and abs(cw - 265.0) <= 0.01 and abs(cd - 440.0) <= 0.01, f"shelf {sw:.1f}x{sd:.1f}, case {cw:.1f}x{cd:.1f}"),
        ("case fits shelf with 10 mm margins", mx >= float(case["minimum_shelf_margin_x_each_side_mm"]) and my >= float(case["minimum_shelf_margin_y_each_end_mm"]), f"X {mx:.1f} / Y {my:.1f} mm"),
        ("rear aperture passes shelf", aw >= sw + 40.0, f"opening {aw:.1f}, shelf {sw:.1f}"),
        ("rear aperture passes PC height", ah >= ch + float(pc["shelf_thickness_z_mm"]) + 40.0, f"opening H {ah:.1f}"),
        ("rear aperture centered inside body", ax >= wood and ax + aw <= outer - wood, f"X {ax:.1f}..{ax+aw:.1f}"),
        ("rear aperture above low rear I/O zone", az >= 175.0, f"Z {az:.1f}..{az+ah:.1f}"),
        ("450 mm rearward travel", abs(travel - float(pc["travel_mm"])) <= 0.01 and abs(travel - 450.0) <= 0.01, f"{travel:.1f} mm"),
        ("stowed shelf stays inside cabinet", sy0 + sd <= rear_inner_plane + 0.1, f"rear edge {sy0+sd:.1f} mm / rear plane {rear_inner_plane:.1f}"),
        ("service shelf substantially exits rear", outside_shelf_fraction >= 0.90, f"outside {outside_shelf_length:.1f}/{sd:.1f} mm ({outside_shelf_fraction*100:.1f}%)"),
        ("service PC case is essentially outside rear", service_case_front >= rear_inner_plane - 1.0 and service_case_rear > rear_inner_plane, f"case Y {service_case_front:.1f}..{service_case_rear:.1f} / rear plane {rear_inner_plane:.1f}"),
        ("support rails remain inside cabinet", left_support >= wood and right_support + support_w <= outer - wood, f"supports {left_support:.1f}..{right_support+support_w:.1f}"),
        ("support/slide/shelf stack coherent", abs((left_support + support_w + slide_t) - sx) <= 0.2 and abs((sx + sw + slide_t) - right_support) <= 0.2, f"left shelf X {sx:.1f}, right support X {right_support:.1f}"),
        ("positive stowed retention", bool(pc["stowed_positive_retention_required"]), pc["stowed_retention_concept"]),
        ("slide holes blocked", "BLOCKED" in pc["slide_mounting_holes_status"], pc["slide_mounting_holes_status"]),
        ("case holes blocked", "BLOCKED" in pc["case_mounting_holes_status"], pc["case_mounting_holes_status"]),
        ("slides have proof-test margin", float(pc["minimum_slide_pair_rating_kg"]) >= 1.5 * float(pc["proof_test_payload_kg"]), f"rating {pc['minimum_slide_pair_rating_kg']} / proof {pc['proof_test_payload_kg']} kg"),
        ("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])),
    ]

    print("REAR CPU SHELF v0.24 VALIDATION")
    print("=" * 80)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<48} {detail}")
        ok = ok and passed

    print()
    print(f"Cabinet inner width             {inner:.1f} mm")
    print(f"Rear door clear opening         {aw:.1f} x {ah:.1f} mm")
    print(f"PC shelf                        {sw:.1f} x {sd:.1f} mm")
    print(f"Installed open-case orientation {cw:.1f} x {cd:.1f} x {ch:.1f} mm")
    print(f"Rearward travel                 {travel:.1f} mm")
    print(f"Shelf outside at service        {outside_shelf_fraction*100:.1f}%")
    print("STATUS", "PASS - rear CPU shelf packaging" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

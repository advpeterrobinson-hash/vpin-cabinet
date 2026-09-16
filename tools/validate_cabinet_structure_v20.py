#!/usr/bin/env python3
"""Validate cabinet CNC joinery, leg reinforcement, PC drawer and glass interfaces v0.20."""
from __future__ import annotations

import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cabinet_structure_v20.json"
DESIGN = ROOT / "config" / "design.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cab = cfg["cabinet"]
    j = cfg["cnc_joinery"]
    leg = cfg["leg_reinforcement"]
    pc = cfg["pc_drawer"]
    glass = cfg["playfield_glass"]
    rails = cfg["siderails"]
    lockdown = cfg["lockdown"]
    gates = cfg["manufacturing_gates"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_wood_mm"])
    length = float(cab["side_length_mm"])
    inner_w = outer - 2.0 * wood
    inner_l = length - 2.0 * wood
    dado = float(j["nominal_dado_depth_mm"])

    bottom_blank_w = inner_w + 2.0 * dado
    bottom_blank_l = inner_l + 2.0 * dado
    front_rear_blank_w = inner_w + 2.0 * dado

    slope_run = length - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    slope = math.atan2(slope_rise, slope_run)

    def top_z(y: float) -> float:
        if y <= slope_run:
            return float(cab["front_height_mm"]) + math.tan(slope) * y
        return float(cab["rear_height_mm"])

    tray_x0 = float(pc["tray_x_mm"])
    tray_x1 = tray_x0 + float(pc["tray_width_x_mm"])
    stowed_y0 = float(pc["tray_stowed_y_mm"])
    stowed_y1 = stowed_y0 + float(pc["tray_depth_y_mm"])
    service_y0 = float(pc["tray_service_y_mm"])
    service_y1 = service_y0 + float(pc["tray_depth_y_mm"])
    tray_top = float(pc["tray_z_mm"]) + float(pc["service_envelope_height_mm"])
    service_top_margin = min(top_z(service_y0), top_z(service_y1)) - tray_top
    stowed_top_margin = min(top_z(stowed_y0), top_z(stowed_y1)) - tray_top

    glass_side_cover = (outer - float(glass["width_mm"])) / 2.0
    glass_rear_margin_to_flat = slope_run - float(glass["rear_y_mm"])

    checks: list[tuple[str, bool, str]] = []
    checks.append(("600 mm body baseline", abs(outer - 600.0) <= 0.01, f"{outer:.1f} mm"))
    checks.append(("v0.20 follows active design width", abs(outer - float(design["cabinet"]["outer_width_mm"])) <= 0.01, f"design={design['cabinet']['outer_width_mm']} mm"))
    checks.append(("full-thickness inner width", abs(inner_w - float(cab["full_thickness_inner_width_mm"])) <= 0.01, f"{inner_w:.1f} mm"))
    checks.append(("inner cabinet length", abs(inner_l - float(cab["inner_length_between_end_panels_mm"])) <= 0.01, f"{inner_l:.1f} mm"))
    checks.append(("dado depth leaves >=12 mm wall", wood - dado >= 12.0, f"remaining {wood-dado:.1f} mm"))
    checks.append(("captured bottom width formula", abs(bottom_blank_w - float(j["bottom_blank_width_mm"])) <= 0.01, f"{bottom_blank_w:.1f} mm"))
    checks.append(("captured bottom length formula", abs(bottom_blank_l - float(j["bottom_blank_length_mm"])) <= 0.01, f"{bottom_blank_l:.1f} mm"))
    checks.append(("captured front/rear width formula", abs(front_rear_blank_w - float(j["front_rear_blank_width_mm"])) <= 0.01, f"{front_rear_blank_w:.1f} mm"))
    checks.append(("three low structural crossmembers", len(j["crossmember_y_mm"]) == 3 and float(j["crossmember_height_z_mm"]) >= 60.0, f"{len(j['crossmember_y_mm'])} x {j['crossmember_height_z_mm']} mm"))
    checks.append(("crossmembers inside cabinet length", all(wood < float(y) < length - wood for y in j["crossmember_y_mm"]), str(j["crossmember_y_mm"])))
    checks.append(("four reinforced leg corners", int(leg["corner_count"]) == 4 and float(leg["local_wood_target_mm"]) >= 36.0, f"{leg['corner_count']} corners / {leg['local_wood_target_mm']} mm local"))
    checks.append(("leg holes blocked until hardware", "BLOCKED" in leg["exact_leg_holes_status"], leg["exact_leg_holes_status"]))
    checks.append(("leg load uses metal and through-bolts", bool(leg["steel_leg_bracket_required"]) and bool(leg["through_bolts_required"]), "metal-backed through-bolt path"))
    checks.append(("PC tray fits full-thickness inner width", tray_x0 >= wood and tray_x1 <= outer - wood, f"X {tray_x0:.1f}..{tray_x1:.1f} mm"))
    checks.append(("PC stowed position inside cabinet", stowed_y0 >= wood and stowed_y1 <= length - wood, f"Y {stowed_y0:.1f}..{stowed_y1:.1f} mm"))
    checks.append(("PC service position inside cabinet", service_y0 >= wood and service_y1 <= length - wood, f"Y {service_y0:.1f}..{service_y1:.1f} mm"))
    checks.append(("PC slide travel matches positions", abs((stowed_y0 - service_y0) - float(pc["slide_travel_mm"])) <= 0.01, f"{stowed_y0-service_y0:.1f} mm"))
    checks.append(("PC service envelope clears cabinet top", service_top_margin >= 25.0, f"minimum {service_top_margin:.1f} mm"))
    checks.append(("PC stowed envelope clears cabinet top", stowed_top_margin >= 25.0, f"minimum {stowed_top_margin:.1f} mm"))
    checks.append(("PC slides have load margin", float(pc["minimum_slide_pair_rating_kg"]) >= 1.5 * float(pc["proof_test_payload_kg"]), f"rating {pc['minimum_slide_pair_rating_kg']} / proof {pc['proof_test_payload_kg']} kg"))
    checks.append(("PC slide holes blocked until sample", "BLOCKED" in pc["exact_slide_holes_status"], pc["exact_slide_holes_status"]))
    checks.append(("glass centered with symmetric side cover", abs(glass_side_cover - float(glass["side_cover_each_side_mm"])) <= 0.01, f"{glass_side_cover:.1f} mm/side"))
    checks.append(("glass remains on sloped top section", glass_rear_margin_to_flat >= 5.0, f"rear margin {glass_rear_margin_to_flat:.1f} mm"))
    checks.append(("tempered glass required", bool(glass["tempered_required"]), str(glass["tempered_required"])))
    checks.append(("siderail pair and glass capture", int(rails["quantity"]) == 2 and float(rails["glass_edge_capture_target_mm"]) >= 10.0, f"capture {rails['glass_edge_capture_target_mm']} mm"))
    checks.append(("custom lockdown matches cabinet width", bool(lockdown["custom_width_required"]) and abs(float(lockdown["outer_width_mm"]) - outer) <= 0.01, f"{lockdown['outer_width_mm']} mm"))
    checks.append(("lockdown receiver holes blocked", "BLOCKED" in lockdown["exact_receiver_holes_status"], lockdown["exact_receiver_holes_status"]))
    checks.append(("CNC gates remain active", bool(gates["measured_plywood_thickness_required"]) and bool(gates["cnc_tolerance_coupon_required"]) and gates["cnc_release_allowed"] is False, "measured stock + coupon + release false"))
    checks.append(("package remains non-manufacturing", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])))

    print("CABINET STRUCTURE v0.20 VALIDATION")
    print("=" * 82)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<51} {detail}")
        ok = ok and passed

    print()
    print(f"Cabinet inside width                 {inner_w:.1f} mm")
    print(f"Captured bottom blank                {bottom_blank_w:.1f} x {bottom_blank_l:.1f} mm nominal")
    print(f"PC service/stowed Y                  {service_y0:.1f} / {stowed_y0:.1f} mm")
    print(f"PC service top clearance             {service_top_margin:.1f} mm")
    print(f"Glass target                         {float(glass['width_mm']):.1f} x {float(glass['length_mm']):.1f} x {float(glass['thickness_mm']):.1f} mm")
    print(f"Glass side cover                     {glass_side_cover:.1f} mm/side")
    print("STATUS", "PASS - cabinet structure packaging" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

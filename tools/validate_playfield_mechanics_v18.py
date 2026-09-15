#!/usr/bin/env python3
"""Validate the integrated model-agnostic playfield mechanics package (v0.18)."""
from __future__ import annotations

import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "playfield_mechanics_v18.json"
DESIGN = ROOT / "config" / "design.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    design = json.loads(DESIGN.read_text(encoding="utf-8"))

    cab = cfg["cabinet"]
    disp = cfg["display_envelope"]
    cradle = cfg["cradle"]
    hinge = cfg["hinge_axis"]
    pivot = cfg["pivot_interface"]
    gs = cfg["gas_struts"]
    stays = cfg["safety_stays"]
    closed = cfg["closed_support"]
    harness = cfg["moving_harness"]
    loads = cfg["load_policy"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_side_thickness_mm"])
    inner = outer - 2.0 * wood
    required_cross = float(disp["cross_width_mm"]) + 2.0 * float(disp["cross_clearance_each_side_mm"])
    moving_mass = float(disp["mass_limit_kg"]) + float(cradle["estimated_cradle_mass_kg"])
    screening_each_side = moving_mass * 9.81 * float(loads["dynamic_factor_screening"]) / 2.0

    checks: list[tuple[str, bool, str]] = []
    checks.append(("600 mm cabinet baseline", abs(outer - 600.0) <= 0.01, f"{outer:.1f} mm"))
    checks.append(("config follows active design width", abs(outer - float(design["cabinet"]["outer_width_mm"])) <= 0.01, f"design={design['cabinet']['outer_width_mm']} mm"))
    checks.append(("full-thickness inner width", abs(inner - float(cab["full_thickness_inner_width_mm"])) <= 0.01, f"{inner:.1f} mm"))
    checks.append(("display envelope needs no side pockets", required_cross <= inner + 1e-6, f"required {required_cross:.1f} / inner {inner:.1f} mm"))
    checks.append(("display model remains open", design["playfield_display"]["exact_model"] is None, str(design["playfield_display"]["exact_model"])))
    checks.append(("primary cradle remains plywood", "plywood" in cradle["primary_material"].lower(), cradle["primary_material"]))
    checks.append(("two structural side rails", int(cradle["side_rail_count"]) == 2, str(cradle["side_rail_count"])))
    checks.append(("rear pivot local wood >=36 mm", float(cradle["pivot_doubler_local_thickness_x_mm"]) >= 36.0, f"{cradle['pivot_doubler_local_thickness_x_mm']} mm"))
    checks.append(("three cradle crossmembers", int(cradle["crossmember_count"]) >= 3, str(cradle["crossmember_count"])))
    checks.append(("replaceable VESA adapter", bool(disp["replaceable_vesa_adapter"]), str(disp["replaceable_vesa_adapter"])))
    checks.append(("service opening >=70 deg", float(hinge["relative_service_open_angle_deg"]) >= 70.0, f"{hinge['relative_service_open_angle_deg']} deg"))
    checks.append(("steel pivot plate >=6 mm", float(pivot["plate_thickness_mm"]) >= 6.0, f"{pivot['plate_thickness_mm']} mm"))
    checks.append(("15 mm journal", abs(float(pivot["journal_diameter_mm"]) - 15.0) <= 0.01, f"{pivot['journal_diameter_mm']} mm"))
    checks.append(("preferred UCFL202 bearing family", "UCFL202" in pivot["bearing_family"], pivot["bearing_family"]))
    checks.append(("bearing holes blocked pending sample", "BLOCKED" in pivot["bearing_mount_holes_status"], pivot["bearing_mount_holes_status"]))
    checks.append(("positive axial retention", bool(pivot["positive_axial_retention_required"]), str(pivot["positive_axial_retention_required"])))
    checks.append(("dual gas struts", int(gs["count"]) == 2, str(gs["count"])))
    checks.append(("gas struts assist only", bool(gs["assist_only"]) and gs["purchase_ready"] is False, "assist only / not purchase-ready"))
    checks.append(("dual independent safety stays", int(stays["count"]) == 2 and bool(stays["independent_of_gas_struts"]) and bool(stays["positive_lock_required"]), f"count={stays['count']}"))
    checks.append(("two closed structural pads", int(closed["structural_pad_count"]) == 2, str(closed["structural_pad_count"])))
    checks.append(("two positive closed latches", int(closed["positive_latch_count"]) == 2, str(closed["positive_latch_count"])))
    checks.append(("moving harness loop >=300 mm", float(harness["service_loop_minimum_length_mm"]) >= 300.0, f"{harness['service_loop_minimum_length_mm']} mm"))
    checks.append(("moving harness bend radius >=50 mm", float(harness["minimum_dynamic_bend_radius_mm"]) >= 50.0, f"R{harness['minimum_dynamic_bend_radius_mm']} mm"))
    checks.append(("moving mass policy consistent", abs(moving_mass - float(loads["moving_mass_design_kg"])) <= 0.01, f"{moving_mass:.1f} kg"))
    checks.append(("pivot screening load exceeds gravity dynamic split", float(loads["pivot_radial_design_load_each_side_n"]) > screening_each_side * 3.0, f"{loads['pivot_radial_design_load_each_side_n']} N vs simple {screening_each_side:.0f} N/side"))
    checks.append(("package remains non-manufacturing-ready", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])))

    print("PLAYFIELD MECHANICS v0.18 VALIDATION")
    print("=" * 78)
    ok = True
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<49} {detail}")
        ok = ok and passed

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    slope = math.degrees(math.atan2(slope_rise, slope_run))
    print()
    print(f"Cabinet slope                       {slope:.3f} deg")
    print(f"Moving mass design                  {moving_mass:.1f} kg")
    print(f"Simple dynamic gravity split        {screening_each_side:.0f} N/side")
    print(f"Pivot packaging design load         {float(loads['pivot_radial_design_load_each_side_n']):.0f} N/side")
    print("STATUS", "PASS - integrated mechanics packaging" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

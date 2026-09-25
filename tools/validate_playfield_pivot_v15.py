#!/usr/bin/env python3
"""Validate v0.15 playfield pivot plate/bearing engineering baseline."""
from __future__ import annotations

import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "playfield_pivot_v15.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    loads = cfg["loads"]
    plate = cfg["cradle_pivot_plate"]
    back = cfg["cradle_pivot_backing_plate"]
    journal = cfg["pivot_journal"]
    bearing = cfg["cabinet_side_bearing"]
    service = cfg["service_removal"]
    safety = cfg["manual_lift_and_safety"]

    ok = True
    t = float(plate["thickness_mm"])
    d = float(journal["selected_nominal_diameter_mm"])
    f = float(loads["pivot_radial_design_load_each_side_n"])
    bearing_stress_mpa = f / (t * d)

    # Conservative simple net-section check through pivot axis using the selected
    # plate height. This is a screening calculation only, not FEA/certification.
    h = float(plate["overall_height_z_mm"])
    net_area = t * (h - d)
    net_tension_equiv_mpa = f / net_area

    print("PLAYFIELD PIVOT v0.15 VALIDATION")
    print("=" * 76)
    print(f"Pivot plate                     {plate['overall_length_y_mm']} x {plate['overall_height_z_mm']} x {t:.2f} mm")
    print(f"Pivot journal                   {d:.1f} mm")
    print(f"Design radial load / side       {f:.0f} N")
    print(f"Plate hole bearing stress       {bearing_stress_mpa:.2f} MPa")
    print(f"Simple net-section equiv stress {net_tension_equiv_mpa:.2f} MPa")
    print()

    if t < 6.0:
        print("FAIL selected pivot plate is thinner than 6 mm baseline")
        ok = False
    else:
        print("PASS >= 6 mm carbon-steel pivot plate")

    if int(plate["mount_hole_count_each_plate"]) != 4 or plate["plywood_mount_bolt"][:2] != "M8":
        print("FAIL pivot plate must use four M8 through-bolts per side")
        ok = False
    else:
        print("PASS four M8 through-bolts per pivot plate")

    if float(back["thickness_mm"]) < 3.0:
        print("FAIL backing/spreader plate thinner than 3 mm")
        ok = False
    else:
        print("PASS 3 mm or thicker pivot backing plate")

    if d < 15.0:
        print("FAIL selected journal below 15 mm v0.15 baseline")
        ok = False
    else:
        print("PASS 15 mm pivot journal baseline")

    if "UCFL202" not in bearing["preferred_family"]:
        print("FAIL preferred flange-bearing family changed unexpectedly")
        ok = False
    else:
        print("PASS UCFL202 15 mm preferred bearing family")

    if "DO NOT CNC" not in bearing["exact_mount_hole_pattern_status"]:
        print("FAIL bearing hole pattern must remain blocked until hardware measurement")
        ok = False
    else:
        print("PASS cabinet bearing hole pattern blocked until physical measurement")

    if bearing["bearing_set_screws_are_not_axial_safety_retention"] is not True or cfg["axial_retention"]["secondary_positive_retention_required"] is not True:
        print("FAIL pivot requires positive axial retention independent of set screws")
        ok = False
    else:
        print("PASS independent positive axial retention required")

    if float(service["maximum_expected_lateral_clearance_for_pivot_release_mm"]) > 100.0:
        print("FAIL service removal requires excessive side clearance")
        ok = False
    else:
        print("PASS short-journal service concept keeps lateral release <=100 mm")

    if not (service["requires_mechanical_safety_stays_engaged"] and service["requires_cabinet_power_isolated"] and service["temporary_secondary_support_required_before_pivot_disassembly"]):
        print("FAIL cradle-removal safety prerequisites incomplete")
        ok = False
    else:
        print("PASS cradle-removal safety prerequisites")

    if not (safety["dual_positive_mechanical_safety_stays_required"] and safety["closed_position_positive_latches_required"] and safety["manual_lift"]):
        print("FAIL service/closed-position safety policy incomplete")
        ok = False
    else:
        print("PASS dual safety stays + positive closed latches; manual lift with captive props")

    # The screening stresses should stay far below ordinary structural carbon
    # steel yield; use 80 MPa as a deliberately conservative warning gate rather
    # than claiming a certified material safety factor.
    if max(bearing_stress_mpa, net_tension_equiv_mpa) >= 80.0:
        print("FAIL simple screening stress exceeds conservative 80 MPa engineering gate")
        ok = False
    else:
        print("PASS simple steel-plate screening stresses below conservative gate")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.15 must remain non-manufacturing-ready")
        ok = False

    print("\nSTATUS", "PASS - pivot engineering baseline only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

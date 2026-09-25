#!/usr/bin/env python3
"""Validate the current documented virtual-pinball design baseline.

Pure-Python checks intentionally avoid FreeCAD so they can run in CI.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "design.json"


@dataclass
class Check:
    name: str
    passed: bool
    value: str
    requirement: str = ""


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def load_config(path: pathlib.Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate(data: dict) -> tuple[list[Check], dict]:
    cab = data["cabinet"]
    pc = data["pc"]
    cnc = data["cnc"]
    display = data["playfield_display"]

    outer = float(cab["outer_width_mm"])
    reference_outer = float(cab["reference_outer_width_mm"])
    wood = float(cab["main_wood_nominal_mm"])
    inner = outer - 2.0 * wood
    width_deviation = outer - reference_outer

    future = cab["future_playfield_service_envelope_mm"]
    target_cross = float(future["target_display_cross_width"])
    cross_clearance = float(future["cross_clearance_each_side"])
    required_cross_cavity = target_cross + 2.0 * cross_clearance
    min_skin = float(future["minimum_remaining_side_skin"])
    full_thickness_clear = float(future["full_thickness_clear_cross_width"])
    max_routed_cross = float(future["maximum_routed_cross_width_at_minimum_skin"])
    calculated_max_routed_cross = outer - 2.0 * min_skin
    pocket_each_side_at_target = max(0.0, (required_cross_cavity - inner) / 2.0)
    remaining_skin_at_target = wood - pocket_each_side_at_target

    target_length = float(future["target_display_length"])
    clear_length = float(future["clear_bay_length"])
    target_depth = float(future["depth"])

    legacy = data["oled"]
    legacy_installed_cross = float(legacy["native_height_mm"]) + 2.0 * float(legacy["clearance_each_side_mm"])
    legacy_margin = (inner - legacy_installed_cross) / 2.0

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    slope_angle_deg = math.degrees(math.atan2(slope_rise, slope_run))
    pc_width_margin = inner - float(pc["service_width_mm"])
    approved = data["design_policy"]["owner_approved_dimensional_deviation_mm"]

    checks = [
        Check(
            "cabinet outer width selected baseline",
            close(outer, 600.0),
            f"{outer:.3f} mm",
            "600.000 mm v0.17 engineering baseline",
        ),
        Check(
            "width deviation within approved range",
            float(approved["typical_min"]) <= width_deviation <= float(approved["typical_max"]),
            f"+{width_deviation:.3f} mm",
            f"{float(approved['typical_min']):.1f}..{float(approved['typical_max']):.1f} mm typical allowance",
        ),
        Check("cabinet inside width positive", inner > 0, f"{inner:.3f} mm"),
        Check("front lower than rear", slope_rise > 0, f"rise {slope_rise:.3f} mm"),
        Check(
            "playfield model selection remains open",
            display["exact_model"] is None,
            str(display["exact_model"]),
            "permanent cabinet must not be locked to one TV model",
        ),
        Check(
            "full-thickness 43-inch-class cavity supported",
            inner + 1e-6 >= required_cross_cavity,
            f"inner {inner:.3f} / required {required_cross_cavity:.3f} mm",
            "target envelope must fit without side pockets",
        ),
        Check(
            "documented full-thickness cavity matches body",
            close(full_thickness_clear, inner),
            f"{full_thickness_clear:.3f} mm",
            f"{inner:.3f} mm from 600 mm body and two {wood:.1f} mm sides",
        ),
        Check(
            "target envelope requires no side pocket",
            close(pocket_each_side_at_target, 0.0)
            and future["side_pocket_required_for_target_envelope"] is False,
            f"{pocket_each_side_at_target:.3f} mm/side",
            "0 mm",
        ),
        Check(
            "maximum routed future cavity documented",
            close(max_routed_cross, calculated_max_routed_cross),
            f"{max_routed_cross:.3f} mm",
            f"{calculated_max_routed_cross:.3f} mm at {min_skin:.1f} mm skins",
        ),
        Check(
            "side skin retained at target display width",
            remaining_skin_at_target + 1e-6 >= min_skin,
            f"{remaining_skin_at_target:.3f} mm",
            f">= {min_skin:.3f} mm",
        ),
        Check(
            "playfield longitudinal service bay",
            clear_length >= target_length,
            f"{clear_length:.1f} mm bay / {target_length:.1f} mm target display",
        ),
        Check(
            "playfield depth service envelope positive",
            target_depth >= 50.0,
            f"{target_depth:.1f} mm",
            ">= 50 mm design envelope",
        ),
        Check(
            "legacy 42-inch LG reference still fits",
            legacy_margin >= 0,
            f"margin {legacy_margin:.3f} mm/side",
            "legacy reference only; not purchase selection",
        ),
        Check(
            "PC service envelope fits cabinet width",
            pc_width_margin >= 0,
            f"margin {pc_width_margin:.3f} mm",
        ),
        Check(
            "playfield service safety specified",
            data["playfield_service"]["captive_prop_rod_count"] == 2
            and bool(data["playfield_service"]["independent_mechanical_safety"]),
            "dual captive props + independent mechanical safety",
        ),
        Check(
            "manual lift force checked on final assembly",
            data["playfield_service"]["manual_lift_force_status"] == "check-completed-assembly",
            data["playfield_service"]["manual_lift_force_status"],
        ),
        Check(
            "CNC production values deliberately unconfirmed",
            cnc["manufacturing_values_confirmed"] is False,
            str(cnc["manufacturing_values_confirmed"]),
            "must remain false until provider/material consultation",
        ),
    ]

    derived = {
        "cabinet_inner_width_mm": inner,
        "cabinet_width_deviation_from_williams_mm": width_deviation,
        "cabinet_slope_run_mm": slope_run,
        "cabinet_slope_rise_mm": slope_rise,
        "cabinet_slope_angle_deg": slope_angle_deg,
        "playfield_target_cross_width_mm": target_cross,
        "playfield_required_cross_cavity_mm": required_cross_cavity,
        "playfield_full_thickness_clear_cross_width_mm": full_thickness_clear,
        "playfield_max_routed_cross_width_at_min_skin_mm": max_routed_cross,
        "playfield_side_pocket_each_side_at_target_mm": pocket_each_side_at_target,
        "playfield_remaining_side_skin_at_target_mm": remaining_skin_at_target,
        "playfield_target_length_mm": target_length,
        "playfield_clear_bay_length_mm": clear_length,
        "legacy_lg_reference_inner_margin_each_side_mm": legacy_margin,
        "pc_service_width_margin_mm": pc_width_margin,
    }
    return checks, derived


def print_human(checks: list[Check], derived: dict) -> None:
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        req = f" | {check.requirement}" if check.requirement else ""
        print(f"{status:4}  {check.name:46} {check.value}{req}")
    print("\nDerived values")
    for key, value in derived.items():
        unit = "deg" if key.endswith("_deg") else "mm"
        print(f"      {key:46} {value:.3f} {unit}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=pathlib.Path, default=DEFAULT_CONFIG, help="Path to design JSON")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable results")
    args = parser.parse_args()
    data = load_config(args.config)
    checks, derived = validate(data)
    success = all(check.passed for check in checks)
    if args.json:
        print(json.dumps({"ok": success, "checks": [check.__dict__ for check in checks], "derived": derived}, indent=2))
    else:
        print_human(checks, derived)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

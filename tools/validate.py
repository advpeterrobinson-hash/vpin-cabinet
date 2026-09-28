#!/usr/bin/env python3
"""Validate the current documented virtual-pinball design baseline.

This validator intentionally uses only the Python standard library so it can be
run in CI without FreeCAD. FreeCAD-specific geometry validation remains in the
stage-specific tools.
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
    oled = data["oled"]
    pc = data["pc"]
    cnc = data["cnc"]

    outer = float(cab["outer_width_mm"])
    reference_outer = float(cab["reference_outer_width_mm"])
    wood = float(cab["main_wood_nominal_mm"])
    inner = outer - 2.0 * wood
    width_deviation = outer - reference_outer

    installed_oled_width = (
        float(oled["native_height_mm"])
        + 2.0 * float(oled["clearance_each_side_mm"])
    )
    pocket_each_side = max(0.0, (installed_oled_width - inner) / 2.0)
    remaining_skin = wood - pocket_each_side
    current_oled_inner_margin_each_side = (inner - installed_oled_width) / 2.0

    future = cab["future_playfield_service_envelope_mm"]
    future_required_cavity = (
        float(future["cross_width"])
        + 2.0 * float(future["clearance_each_side"])
    )
    min_skin = float(oled["minimum_remaining_side_skin_mm"])
    max_future_cavity = inner + 2.0 * (wood - min_skin)
    future_cavity_margin = max_future_cavity - future_required_cavity

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    slope_angle_deg = math.degrees(math.atan2(slope_rise, slope_run))

    pc_width_margin = inner - float(pc["service_width_mm"])
    approved = data["design_policy"]["owner_approved_dimensional_deviation_mm"]

    checks = [
        Check(
            "cabinet outer width selected baseline",
            close(outer, 580.0),
            f"{outer:.3f} mm",
            "580.000 mm v0.7 engineering baseline",
        ),
        Check(
            "width deviation within approved range",
            float(approved["typical_min"]) <= width_deviation <= float(approved["typical_max"]),
            f"+{width_deviation:.3f} mm",
            f"{float(approved['typical_min']):.1f}..{float(approved['typical_max']):.1f} mm typical allowance",
        ),
        Check(
            "cabinet inside width positive",
            inner > 0,
            f"{inner:.3f} mm",
        ),
        Check(
            "front lower than rear",
            slope_rise > 0,
            f"rise {slope_rise:.3f} mm",
        ),
        Check(
            "C5 installed envelope fits without side pockets",
            current_oled_inner_margin_each_side >= 0,
            f"margin {current_oled_inner_margin_each_side:.3f} mm/side",
            ">= 0 mm",
        ),
        Check(
            "current OLED remaining side skin",
            remaining_skin >= min_skin,
            f"{remaining_skin:.3f} mm",
            f">= {min_skin:.3f} mm",
        ),
        Check(
            "future playfield replacement cavity",
            future_cavity_margin >= -1e-6,
            f"margin {future_cavity_margin:.3f} mm",
            f"supports {future_required_cavity:.1f} mm cavity at >= {min_skin:.1f} mm skin",
        ),
        Check(
            "PC service envelope fits cabinet width",
            pc_width_margin >= 0,
            f"margin {pc_width_margin:.3f} mm",
        ),
        Check(
            "OLED service safety specified",
            bool(data["playfield_service"]["dual_gas_struts"])
            and bool(data["playfield_service"]["independent_mechanical_safety"]),
            "dual struts + independent mechanical safety",
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
        "oled_installed_width_mm": installed_oled_width,
        "oled_required_pocket_depth_each_side_mm": pocket_each_side,
        "oled_inner_margin_each_side_mm": current_oled_inner_margin_each_side,
        "oled_remaining_side_skin_mm": remaining_skin,
        "future_playfield_required_cavity_mm": future_required_cavity,
        "future_playfield_max_cavity_at_min_skin_mm": max_future_cavity,
        "future_playfield_cavity_margin_mm": future_cavity_margin,
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
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=DEFAULT_CONFIG,
        help="Path to design JSON",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable results",
    )
    args = parser.parse_args()

    data = load_config(args.config)
    checks, derived = validate(data)
    success = all(check.passed for check in checks)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": success,
                    "checks": [check.__dict__ for check in checks],
                    "derived": derived,
                },
                indent=2,
            )
        )
    else:
        print_human(checks, derived)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

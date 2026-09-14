#!/usr/bin/env python3
"""Validate the documented virtual-pinball design baseline.

This validator intentionally uses only the Python standard library so it can be
run with ordinary Python. FreeCAD-specific geometry validation will be added as
separate checks as the model matures.
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
    wood = float(cab["main_wood_nominal_mm"])
    inner = outer - 2.0 * wood

    installed_oled_width = (
        float(oled["native_height_mm"])
        + 2.0 * float(oled["clearance_each_side_mm"])
    )
    pocket_each_side = (installed_oled_width - inner) / 2.0
    remaining_skin = wood - pocket_each_side

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    slope_angle_deg = math.degrees(math.atan2(slope_rise, slope_run))

    pc_width_margin = inner - float(pc["service_width_mm"])

    checks = [
        Check(
            "cabinet outer width",
            close(outer, 558.8),
            f"{outer:.3f} mm",
            "558.800 mm Williams WPC baseline",
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
            "OLED cross-width fit requires pockets",
            pocket_each_side > 0,
            f"{pocket_each_side:.3f} mm/side",
        ),
        Check(
            "OLED remaining side skin",
            remaining_skin >= float(oled["minimum_remaining_side_skin_mm"]),
            f"{remaining_skin:.3f} mm",
            f">= {float(oled['minimum_remaining_side_skin_mm']):.3f} mm",
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
        "cabinet_slope_run_mm": slope_run,
        "cabinet_slope_rise_mm": slope_rise,
        "cabinet_slope_angle_deg": slope_angle_deg,
        "oled_installed_width_mm": installed_oled_width,
        "oled_pocket_depth_each_side_mm": pocket_each_side,
        "oled_remaining_side_skin_mm": remaining_skin,
        "pc_service_width_margin_mm": pc_width_margin,
    }

    return checks, derived


def print_human(checks: list[Check], derived: dict) -> None:
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        req = f" | {check.requirement}" if check.requirement else ""
        print(f"{status:4}  {check.name:42} {check.value}{req}")

    print("\nDerived values")
    for key, value in derived.items():
        unit = "deg" if key.endswith("_deg") else "mm"
        print(f"      {key:42} {value:.3f} {unit}")


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

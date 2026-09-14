#!/usr/bin/env python3
"""Analyze v0.4 OLED playfield hinge and gas-spring kinematics.

This script uses only the Python standard library. It intentionally separates
kinematic screening from FreeCAD geometry generation so mounting candidates can
be rejected cheaply before touching the CAD document.

The gas-spring force curve is an engineering approximation for screening only.
Final spring selection requires measured moving mass/CG, actual mounting
hardware, and manufacturer confirmation.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from dataclasses import dataclass, asdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_CONFIG = ROOT / "config" / "design.json"
PF_CONFIG = ROOT / "config" / "playfield_v04.json"


@dataclass
class Point2D:
    y: float
    z: float


@dataclass
class SweepRow:
    angle_deg: float
    gas_length_mm: float
    gas_force_each_n: float
    gas_moment_arm_mm: float
    gravity_torque_nm: float
    gas_assist_torque_nm: float
    assist_ratio: float
    oled_y_min_mm: float
    oled_y_max_mm: float
    oled_z_min_mm: float
    oled_z_max_mm: float


@dataclass
class Check:
    name: str
    passed: bool
    value: str
    requirement: str


def load_json(path: pathlib.Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def rotate_about(point: Point2D, pivot: Point2D, angle_rad: float) -> Point2D:
    """Rotate point in the Y/Z plane using an X-axis rotation convention."""
    dy = point.y - pivot.y
    dz = point.z - pivot.z
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return Point2D(
        pivot.y + dy * c - dz * s,
        pivot.z + dy * s + dz * c,
    )


def top_z(cab: dict, y_mm: float) -> float:
    """Outer top-edge Z of the Williams side profile at cabinet Y."""
    front = float(cab["front_height_mm"])
    rear = float(cab["rear_height_mm"])
    side_len = float(cab["side_length_mm"])
    rear_flat = float(cab["rear_top_flat_mm"])
    slope_run = side_len - rear_flat

    if y_mm <= 0:
        return front
    if y_mm >= slope_run:
        return rear
    return front + (rear - front) * (y_mm / slope_run)


def closed_oled_corners(base: dict, pf: dict) -> tuple[list[Point2D], dict]:
    """Return Y/Z corners for the OLED physical envelope in closed position.

    The OLED box is defined with native width along cabinet Y and native height
    across cabinet X. The front FACE point is positioned below the Williams top
    edge by the configured face inset. The physical depth extends normal to the
    playfield plane toward the cabinet interior.
    """
    cab = base["cabinet"]
    oled = base["oled"]
    svc = pf["playfield"]

    run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    theta = math.atan2(rise, run)

    front_face_y = float(svc["oled_front_setback_mm"])
    front_face_z = top_z(cab, front_face_y) - float(
        svc["oled_face_inset_below_cabinet_top_mm"]
    )

    length = float(oled["native_width_mm"])
    depth = float(oled["max_depth_mm"])

    # Standard X-axis rotation: y' = y*cos - z*sin, z' = y*sin + z*cos.
    # Solve the back/front local origin so local z=depth lands on the desired
    # front face point.
    origin_y = front_face_y + depth * math.sin(theta)
    origin_z = front_face_z - depth * math.cos(theta)

    def p(local_y: float, local_z: float) -> Point2D:
        return Point2D(
            origin_y + local_y * math.cos(theta) - local_z * math.sin(theta),
            origin_z + local_y * math.sin(theta) + local_z * math.cos(theta),
        )

    corners = [
        p(0.0, 0.0),
        p(length, 0.0),
        p(0.0, depth),
        p(length, depth),
    ]

    face_rear_y = front_face_y + length * math.cos(theta)
    hinge_y = face_rear_y + float(svc["hinge_rear_gap_mm"])
    hinge_z = top_z(cab, hinge_y) - float(
        svc["hinge_axis_inset_below_cabinet_top_mm"]
    )

    derived = {
        "slope_angle_deg": math.degrees(theta),
        "front_face_y_mm": front_face_y,
        "front_face_z_mm": front_face_z,
        "oled_back_origin_y_mm": origin_y,
        "oled_back_origin_z_mm": origin_z,
        "face_rear_y_mm": face_rear_y,
        "hinge_y_mm": hinge_y,
        "hinge_z_mm": hinge_z,
    }
    return corners, derived


def gas_row(
    base: dict,
    pf: dict,
    theta: float,
    hinge: Point2D,
    closed_corners: list[Point2D],
    angle_deg: float,
) -> SweepRow:
    svc = pf["playfield"]
    gas = svc["gas_spring_candidate"]
    val = pf["validation"]

    phi = math.radians(angle_deg)
    moving_angle = theta - phi

    moving_r = float(gas["moving_mount_forward_of_hinge_mm"])
    moving = Point2D(
        hinge.y - moving_r * math.cos(moving_angle),
        hinge.z - moving_r * math.sin(moving_angle),
    )

    fixed = Point2D(
        hinge.y - float(gas["fixed_mount_forward_of_hinge_mm"]),
        hinge.z - float(gas["fixed_mount_below_hinge_mm"]),
    )

    dy = moving.y - fixed.y
    dz = moving.z - fixed.z
    gas_len = math.hypot(dy, dz)
    if gas_len <= 0:
        raise ValueError("degenerate gas-spring mount geometry")

    uy = dy / gas_len
    uz = dz / gas_len
    ry = moving.y - hinge.y
    rz = moving.z - hinge.z
    moment_arm_mm = abs(ry * uz - rz * uy)

    extended = float(gas["extended_length_mm"])
    stroke = float(gas["stroke_mm"])
    f1 = float(gas["nominal_extension_force_f1_n"])
    ratio = float(gas["assumed_force_ratio_f2_over_f1"])
    compression = max(0.0, min(stroke, extended - gas_len))
    compression_fraction = compression / stroke if stroke else 0.0
    force_each = f1 * (1.0 + (ratio - 1.0) * compression_fraction)

    moving_mass = float(base["oled"]["mass_kg"]) + float(
        svc["cradle_mass_estimate_kg"]
    )
    cg_r = float(svc["moving_cg_forward_of_hinge_mm"])
    cg_y = hinge.y - cg_r * math.cos(moving_angle)
    weight_n = moving_mass * float(val["gravity_m_s2"])
    gravity_torque_nm = abs((cg_y - hinge.y) / 1000.0 * weight_n)

    gas_torque_nm = (
        int(gas["quantity"]) * force_each * (moment_arm_mm / 1000.0)
    )
    assist_ratio = gas_torque_nm / gravity_torque_nm if gravity_torque_nm else math.inf

    opened = [rotate_about(p, hinge, -phi) for p in closed_corners]
    ys = [p.y for p in opened]
    zs = [p.z for p in opened]

    return SweepRow(
        angle_deg=angle_deg,
        gas_length_mm=gas_len,
        gas_force_each_n=force_each,
        gas_moment_arm_mm=moment_arm_mm,
        gravity_torque_nm=gravity_torque_nm,
        gas_assist_torque_nm=gas_torque_nm,
        assist_ratio=assist_ratio,
        oled_y_min_mm=min(ys),
        oled_y_max_mm=max(ys),
        oled_z_min_mm=min(zs),
        oled_z_max_mm=max(zs),
    )


def analyze(base: dict, pf: dict) -> tuple[list[SweepRow], list[Check], dict]:
    cab = base["cabinet"]
    oled = base["oled"]
    svc = pf["playfield"]
    gas = svc["gas_spring_candidate"]
    val = pf["validation"]

    closed_corners, derived = closed_oled_corners(base, pf)
    theta = math.radians(derived["slope_angle_deg"])
    hinge = Point2D(derived["hinge_y_mm"], derived["hinge_z_mm"])

    step = float(val["angle_step_deg"])
    target = float(svc["target_open_angle_deg"])
    angles: list[float] = []
    a = 0.0
    while a < target - 1e-9:
        angles.append(round(a, 9))
        a += step
    angles.append(target)

    rows = [gas_row(base, pf, theta, hinge, closed_corners, a) for a in angles]

    inner = float(cab["outer_width_mm"]) - 2.0 * float(cab["main_wood_nominal_mm"])
    installed_width = float(oled["native_height_mm"]) + 2.0 * float(
        oled["clearance_each_side_mm"]
    )
    pocket = (installed_width - inner) / 2.0
    remaining_skin = float(cab["main_wood_nominal_mm"]) - pocket

    compressed = float(gas["extended_length_mm"]) - float(gas["stroke_mm"])
    reserve = float(gas["minimum_end_travel_reserve_mm"])
    min_len = min(r.gas_length_mm for r in rows)
    max_len = max(r.gas_length_mm for r in rows)
    closed = rows[0]
    opened = rows[-1]

    checks = [
        Check(
            "OLED remaining side skin",
            remaining_skin >= float(val["minimum_oled_side_skin_mm"]),
            f"{remaining_skin:.3f} mm",
            f">= {float(val['minimum_oled_side_skin_mm']):.3f} mm",
        ),
        Check(
            "gas spring compressed-end reserve",
            min_len >= compressed + reserve,
            f"min {min_len:.3f} mm",
            f">= {compressed + reserve:.3f} mm",
        ),
        Check(
            "gas spring extended-end reserve",
            max_len <= float(gas["extended_length_mm"]) - reserve,
            f"max {max_len:.3f} mm",
            f"<= {float(gas['extended_length_mm']) - reserve:.3f} mm",
        ),
        Check(
            "closed position remains gravity-dominant",
            closed.assist_ratio <= float(gas["preferred_closed_assist_ratio_max"]),
            f"assist ratio {closed.assist_ratio:.3f}",
            f"<= {float(gas['preferred_closed_assist_ratio_max']):.3f}",
        ),
        Check(
            "open position remains gas-assist dominant",
            opened.assist_ratio >= float(gas["preferred_open_assist_ratio_min"]),
            f"assist ratio {opened.assist_ratio:.3f}",
            f">= {float(gas['preferred_open_assist_ratio_min']):.3f}",
        ),
        Check(
            "independent mechanical safety specified",
            bool(svc["safety_prop"]["required"]),
            str(bool(svc["safety_prop"]["required"])),
            "True",
        ),
        Check(
            "hinge axis remains inside cabinet length",
            0.0 < hinge.y < float(cab["side_length_mm"]),
            f"Y={hinge.y:.3f} mm",
            f"0 < Y < {float(cab['side_length_mm']):.3f} mm",
        ),
    ]

    derived.update(
        {
            "cabinet_inner_width_mm": inner,
            "oled_installed_cross_width_mm": installed_width,
            "oled_pocket_depth_each_side_mm": pocket,
            "oled_remaining_side_skin_mm": remaining_skin,
            "moving_mass_estimate_kg": float(oled["mass_kg"])
            + float(svc["cradle_mass_estimate_kg"]),
            "gas_compressed_length_mm": compressed,
            "gas_min_sweep_length_mm": min_len,
            "gas_max_sweep_length_mm": max_len,
            "closed_assist_ratio": closed.assist_ratio,
            "open_assist_ratio": opened.assist_ratio,
            "open_oled_max_height_mm": opened.oled_z_max_mm,
            "open_oled_min_y_mm": opened.oled_y_min_mm,
            "open_oled_max_y_mm": opened.oled_y_max_mm,
            "vesa_center_position_confirmed": bool(
                svc["cradle"]["vesa_center_position_confirmed"]
            ),
            "final_safety_prop_selected": bool(
                svc["safety_prop"]["final_hardware_selected"]
            ),
        }
    )

    return rows, checks, derived


def print_human(rows: list[SweepRow], checks: list[Check], derived: dict) -> None:
    print("v0.4 PLAYFIELD SERVICE KINEMATICS")
    print("=" * 78)
    for key in (
        "slope_angle_deg",
        "hinge_y_mm",
        "hinge_z_mm",
        "moving_mass_estimate_kg",
        "gas_compressed_length_mm",
        "gas_min_sweep_length_mm",
        "gas_max_sweep_length_mm",
        "closed_assist_ratio",
        "open_assist_ratio",
        "open_oled_max_height_mm",
    ):
        print(f"{key:36} {derived[key]:.3f}")

    print("\nSweep")
    print(
        " angle | gas len | gas F | arm   | gravity | assist  | ratio | OLED Z max"
    )
    print("-" * 86)
    for r in rows:
        print(
            f" {r.angle_deg:5.1f} |"
            f" {r.gas_length_mm:7.1f} |"
            f" {r.gas_force_each_n:5.0f} |"
            f" {r.gas_moment_arm_mm:6.1f} |"
            f" {r.gravity_torque_nm:7.1f} |"
            f" {r.gas_assist_torque_nm:7.1f} |"
            f" {r.assist_ratio:5.2f} |"
            f" {r.oled_z_max_mm:10.1f}"
        )

    print("\nChecks")
    for c in checks:
        state = "PASS" if c.passed else "FAIL"
        print(f"{state:4}  {c.name:42} {c.value} | {c.requirement}")

    if not derived["vesa_center_position_confirmed"]:
        print("\nWARN  LG C5 VESA center offset is still assumed, not physically verified.")
    if not derived["final_safety_prop_selected"]:
        print("WARN  Safety prop concept is mandatory but final hardware is not selected.")
    print("WARN  Gas-spring force curve and cradle mass are engineering estimates only.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=pathlib.Path, default=BASE_CONFIG)
    parser.add_argument("--playfield", type=pathlib.Path, default=PF_CONFIG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    base = load_json(args.base)
    pf = load_json(args.playfield)
    rows, checks, derived = analyze(base, pf)
    ok = all(c.passed for c in checks)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": ok,
                    "derived": derived,
                    "checks": [asdict(c) for c in checks],
                    "sweep": [asdict(r) for r in rows],
                },
                indent=2,
            )
        )
    else:
        print_human(rows, checks, derived)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

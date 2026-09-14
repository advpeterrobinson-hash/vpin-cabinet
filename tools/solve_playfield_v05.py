#!/usr/bin/env python3
"""Evaluate v0.5 playfield sweep, safety-prop packaging, and strut candidates.

This is an engineering packaging solver. It intentionally does not approve
hardware for purchase or manufacturing.
"""

from __future__ import annotations

import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGN = ROOT / "config" / "design.json"
V04 = ROOT / "config" / "playfield_v04.json"
V05 = ROOT / "config" / "playfield_v05.json"
G = 9.80665


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def top_z(cab: dict, y: float) -> float:
    run = cab["side_length_mm"] - cab["rear_top_flat_mm"]
    if y <= run:
        rise = cab["rear_height_mm"] - cab["front_height_mm"]
        return cab["front_height_mm"] + rise * (y / run)
    return cab["rear_height_mm"]


def main() -> int:
    d = load(DESIGN)
    p4 = load(V04)
    p5 = load(V05)
    cab = d["cabinet"]
    oled = d["oled"]
    cradle = p4["cradle"]
    svc = p4["service"]
    gs = p4["gas_strut_candidate"]

    slope_run = cab["side_length_mm"] - cab["rear_top_flat_mm"]
    slope_rise = cab["rear_height_mm"] - cab["front_height_mm"]
    alpha = math.atan2(slope_rise, slope_run)
    alpha_deg = math.degrees(alpha)
    open_rel = math.radians(svc["relative_open_angle_deg"])

    y0 = p4["oled_front_setback_mm"]
    hinge_path = oled["native_width_mm"] + cradle["hinge_offset_behind_oled_rear_mm"]
    hinge_y = y0 + hinge_path * math.cos(alpha)
    hinge_z = (
        top_z(cab, y0)
        + hinge_path * math.sin(alpha)
        - p4["glass_clearance_normal_mm"]
        - 0.5 * oled["max_depth_mm"]
    )

    # Conservative 2D sweep envelope in the Y/Z side view. The hinge is behind
    # the OLED rear edge; evaluate the four longitudinal/depth corner points.
    hinge_offset = cradle["hinge_offset_behind_oled_rear_mm"]
    tv_len = oled["native_width_mm"]
    tv_depth = oled["max_depth_mm"]
    backbox_front = p5["backbox_keepout"]["front_y_mm"]
    backbox_z0 = p5["backbox_keepout"]["bottom_z_mm"]
    backbox_z1 = backbox_z0 + p5["backbox_keepout"]["height_mm"]

    sweep_rows = []
    collision = False
    min_y_margin = float("inf")

    for deg in p5["sweep"]["angles_deg"]:
        phi = math.pi + alpha - math.radians(deg)  # hinge -> cabinet front
        normal = phi + math.pi / 2.0
        points = []
        for dist in (hinge_offset, hinge_offset + tv_len):
            for n in (-tv_depth / 2.0, tv_depth / 2.0):
                y = hinge_y + dist * math.cos(phi) + n * math.cos(normal)
                z = hinge_z + dist * math.sin(phi) + n * math.sin(normal)
                points.append((y, z))
        ymin = min(y for y, _ in points)
        ymax = max(y for y, _ in points)
        zmin = min(z for _, z in points)
        zmax = max(z for _, z in points)
        y_margin = backbox_front - ymax
        min_y_margin = min(min_y_margin, y_margin)
        z_overlap = not (zmax < backbox_z0 or zmin > backbox_z1)
        potential = ymax >= backbox_front and z_overlap
        collision = collision or potential
        sweep_rows.append((deg, ymin, ymax, zmin, zmax, y_margin, potential))

    # Positive mechanical safety prop candidate at full service opening.
    sp = p5["safety_prop_candidate"]
    fixed_y = hinge_y - sp["fixed_mount_forward_from_hinge_mm"]
    fixed_z = hinge_z - sp["fixed_mount_below_hinge_mm"]
    phi_open = math.pi + alpha - open_rel
    moving_y = hinge_y + sp["moving_mount_forward_from_hinge_mm"] * math.cos(phi_open)
    moving_z = hinge_z + sp["moving_mount_forward_from_hinge_mm"] * math.sin(phi_open)
    prop_len = math.hypot(moving_y - fixed_y, moving_z - fixed_z)

    # Reuse the v0.4 strut geometry but compare several force ratings.
    total_mass = oled["mass_kg"] + cradle["estimated_mass_kg"]
    weight = total_mass * G
    hinge_to_cg = oled["native_width_mm"] / 2.0 + cradle["hinge_offset_behind_oled_rear_mm"]
    moving_d = gs["moving_mount_forward_from_hinge_mm"]
    fixed = (-gs["fixed_mount_forward_from_hinge_mm"], -gs["fixed_mount_below_hinge_mm"])

    def moving_point(opened: bool) -> tuple[float, float]:
        phi = math.pi + alpha - (open_rel if opened else 0.0)
        return moving_d * math.cos(phi), moving_d * math.sin(phi)

    def lever(opened: bool) -> float:
        ay, az = moving_point(opened)
        vy, vz = ay - fixed[0], az - fixed[1]
        length = math.hypot(vy, vz)
        uy, uz = vy / length, vz / length
        return abs(ay * uz - az * uy)

    lever_closed = lever(False)
    lever_open = lever(True)
    cg_closed_y = hinge_to_cg * math.cos(math.pi + alpha)
    cg_open_y = hinge_to_cg * math.cos(math.pi + alpha - open_rel)
    wt_closed = abs(cg_closed_y * weight)
    wt_open = abs(cg_open_y * weight)
    count = gs["count"]
    required_closed = wt_closed / (count * lever_closed)
    required_open = wt_open / (count * lever_open)

    print("PLAYFIELD v0.5 SWEEP / SAFETY SOLVER")
    print("=" * 74)
    print(f"Cabinet slope              {alpha_deg:9.3f} deg")
    print(f"Hinge Y / Z                {hinge_y:9.3f} / {hinge_z:9.3f} mm")
    print(f"Backbox keepout front Y    {backbox_front:9.3f} mm")
    print()
    print("Angle    Ymin      Ymax      Zmin      Zmax    Y-margin   collision")
    for deg, ymin, ymax, zmin, zmax, margin, potential in sweep_rows:
        print(
            f"{deg:5.0f}  {ymin:8.1f}  {ymax:8.1f}  {zmin:8.1f}  {zmax:8.1f}"
            f"  {margin:8.1f}   {'YES' if potential else 'no'}"
        )
    print()
    print(f"Minimum backbox Y margin   {min_y_margin:9.3f} mm")
    print(f"Safety prop open length    {prop_len:9.3f} mm")
    print(f"Safety prop fixed Y/Z      {fixed_y:9.3f} / {fixed_z:9.3f} mm")
    print(f"Safety prop moving Y/Z     {moving_y:9.3f} / {moving_z:9.3f} mm")
    print()
    print(f"Strut force required closed {required_closed:8.1f} N/strut")
    print(f"Strut force required open   {required_open:8.1f} N/strut")
    for force in p5["gas_strut_force_candidates_n"]:
        print(
            f"Candidate {force:5.0f} N: closed ratio={force/required_closed:5.3f}x, "
            f"open ratio={force/required_open:5.3f}x"
        )
    print()
    print("STATUS: ENGINEERING PROVISIONAL")
    print("Backbox placement, cradle CG, prop hardware, hinge brackets, and")
    print("gas-strut ratings must be confirmed before purchasing or fabrication.")

    ok = True
    if collision:
        print("FAIL: provisional OLED sweep enters provisional backbox keepout")
        ok = False
    if min_y_margin < 20.0:
        print("FAIL: provisional backbox margin below 20 mm packaging target")
        ok = False
    if not (350.0 <= prop_len <= 800.0):
        print("FAIL: safety-prop candidate length outside initial packaging range")
        ok = False
    if p5["manufacturing_ready"] is not False:
        print("FAIL: v0.5 must remain non-manufacturing-ready")
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

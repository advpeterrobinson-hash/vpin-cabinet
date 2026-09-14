#!/usr/bin/env python3
"""Evaluate the provisional dual gas-strut geometry for playfield service.

This is a packaging/load-estimation tool, not a purchasing recommendation.
It intentionally keeps the mechanics in a 2D Y/Z side view so candidate
mounting points can be changed quickly before detailed brackets are modeled.
"""

from __future__ import annotations

import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESIGN = ROOT / "config" / "design.json"
PLAYFIELD = ROOT / "config" / "playfield_v04.json"
G = 9.80665


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    d = load(DESIGN)
    p = load(PLAYFIELD)
    cab = d["cabinet"]
    oled = d["oled"]
    cradle = p["cradle"]
    svc = p["service"]
    gs = p["gas_strut_candidate"]

    slope_run = cab["side_length_mm"] - cab["rear_top_flat_mm"]
    slope_rise = cab["rear_height_mm"] - cab["front_height_mm"]
    alpha = math.atan2(slope_rise, slope_run)
    open_rel = math.radians(svc["relative_open_angle_deg"])

    total_mass = oled["mass_kg"] + cradle["estimated_mass_kg"]
    weight = total_mass * G

    # Hinge is behind the OLED rear edge. Approximate combined CG at the
    # OLED longitudinal midpoint. This will be replaced by measured CG later.
    hinge_to_cg = (
        oled["native_width_mm"] / 2.0
        + cradle["hinge_offset_behind_oled_rear_mm"]
    )

    moving_d = gs["moving_mount_forward_from_hinge_mm"]
    fixed = (
        -gs["fixed_mount_forward_from_hinge_mm"],
        -gs["fixed_mount_below_hinge_mm"],
    )

    def moving_point(opened: bool) -> tuple[float, float]:
        # Relative vector from hinge toward cabinet front.
        phi = math.pi + alpha - (open_rel if opened else 0.0)
        return moving_d * math.cos(phi), moving_d * math.sin(phi)

    def geometry(opened: bool) -> tuple[float, float, float]:
        ay, az = moving_point(opened)
        vy = ay - fixed[0]
        vz = az - fixed[1]
        length = math.hypot(vy, vz)
        uy, uz = vy / length, vz / length
        # Torque arm per Newton for force acting away from fixed mount.
        lever = abs(ay * uz - az * uy)
        return length, lever, ay

    closed_len, closed_lever, _ = geometry(False)
    open_len, open_lever, _ = geometry(True)
    stroke = open_len - closed_len

    # Weight torque is based on horizontal Y distance from hinge to CG.
    phi_closed = math.pi + alpha
    phi_open = phi_closed - open_rel
    cg_y_closed = hinge_to_cg * math.cos(phi_closed)
    cg_y_open = hinge_to_cg * math.cos(phi_open)
    weight_torque_closed = abs(cg_y_closed * weight)
    weight_torque_open = abs(cg_y_open * weight)

    n = gs["count"]
    required_each_closed = weight_torque_closed / (n * closed_lever)
    candidate = gs["candidate_force_each_n"]
    candidate_open_torque = n * candidate * open_lever
    open_balance_ratio = candidate_open_torque / weight_torque_open

    print("PLAYFIELD GAS-STRUT PRELIMINARY SOLVER")
    print("=" * 64)
    print(f"Cabinet slope                 {math.degrees(alpha):8.3f} deg")
    print(f"Relative service opening      {math.degrees(open_rel):8.3f} deg")
    print(f"Estimated moving mass         {total_mass:8.3f} kg")
    print(f"Approx hinge-to-CG distance   {hinge_to_cg:8.3f} mm")
    print()
    print(f"Closed strut length           {closed_len:8.3f} mm")
    print(f"Open strut length             {open_len:8.3f} mm")
    print(f"Required stroke               {stroke:8.3f} mm")
    print(f"Closed effective lever        {closed_lever:8.3f} mm")
    print(f"Open effective lever          {open_lever:8.3f} mm")
    print()
    print(f"Calculated hold force/strut   {required_each_closed:8.1f} N")
    print(f"Provisional candidate/strut   {candidate:8.1f} N")
    print(f"Open assist / gravity ratio   {open_balance_ratio:8.3f} x")
    print()
    print("STATUS: ENGINEERING PROVISIONAL")
    print("Do not purchase struts from this result alone. Re-run after the")
    print("actual cradle mass, CG, hinge brackets, and available strut sizes")
    print("are known. A positive mechanical safety prop remains mandatory.")

    # Broad packaging guards only. These deliberately do not pretend the
    # preliminary candidate is a finalized mechanism.
    ok = True
    if not (80.0 <= stroke <= 220.0):
        print("FAIL: preliminary stroke outside expected packaging range")
        ok = False
    if not (150.0 <= required_each_closed <= 500.0):
        print("FAIL: estimated force outside initial design range")
        ok = False
    if closed_len >= open_len:
        print("FAIL: gas strut does not extend when playfield opens")
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

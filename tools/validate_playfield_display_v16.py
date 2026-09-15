#!/usr/bin/env python3
"""Validate the model-agnostic playfield display service envelope (v0.16/v0.17 width)."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "playfield_display_v16.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    env = cfg["permanent_cabinet_envelope"]
    buy = cfg["purchase_policy"]
    cradle = cfg["cradle_policy"]

    outer = float(env["cabinet_outer_width_mm"])
    wood = float(env["nominal_side_thickness_mm"])
    min_skin = float(env["minimum_remaining_side_skin_mm"])
    inner = outer - 2.0 * wood
    max_cavity = outer - 2.0 * min_skin
    target_cross = float(env["target_max_display_cross_width_mm"])
    clearance = float(env["cross_clearance_each_side_mm"])
    required_cross = target_cross + 2.0 * clearance

    ok = True
    print("PLAYFIELD DISPLAY v0.16/v0.17 VALIDATION")
    print("=" * 76)
    print(f"Cabinet outer width             {outer:8.2f} mm")
    print(f"Full-thickness inner width      {inner:8.2f} mm")
    print(f"Max routed cavity at min skin   {max_cavity:8.2f} mm")
    print(f"Required target cavity          {required_cross:8.2f} mm")

    if abs(inner - float(env["full_thickness_inner_width_mm"])) > 0.01:
        print("FAIL documented full-thickness inner width mismatch")
        ok = False
    else:
        print("PASS full-thickness inner width")

    documented_max = float(env["maximum_future_routed_cavity_at_minimum_skin_mm"])
    if abs(max_cavity - documented_max) > 0.01:
        print("FAIL documented maximum routed cavity mismatch")
        ok = False
    else:
        print("PASS maximum routed cavity derived from body/minimum skin")

    if required_cross > inner + 1e-6:
        print("FAIL target display requires side pockets in the selected baseline")
        ok = False
    else:
        print(f"PASS target envelope fits full-thickness bay with {inner - required_cross:.2f} mm total spare width")

    if int(buy["minimum_native_refresh_hz"]) < 120:
        print("FAIL purchase policy refresh target too low")
        ok = False
    else:
        print("PASS minimum native refresh >=120 Hz")

    if buy["exact_model_selected"] is not False:
        print("FAIL display selection must remain model-agnostic until Phase 3 purchase")
        ok = False
    else:
        print("PASS exact display model intentionally open")

    if not cradle["replaceable_vesa_adapter_required"] or not cradle["display_specific_permanent_wood_holes_prohibited"]:
        print("FAIL replaceable display-adapter policy incomplete")
        ok = False
    else:
        print("PASS permanent wood remains display-model agnostic")

    for candidate in cfg["reference_candidates"]:
        dims = candidate["pinball_orientation_mm"]
        cross = float(dims["cross_width"])
        length = float(dims["length"])
        depth = float(dims["depth"])
        mass = float(candidate["mass_without_stand_kg"])

        candidate_required_cross = cross + 2.0 * clearance
        fits = (
            candidate_required_cross <= max_cavity + 1e-6
            and length <= float(env["target_max_display_length_mm"]) + 1e-6
            and depth <= float(env["target_max_display_depth_mm"]) + 1e-6
            and mass <= float(env["display_mass_design_limit_kg"]) + 1e-6
        )
        expected = candidate["fit_status"].startswith("fits")
        if fits != expected:
            print(f"FAIL candidate fit mismatch: {candidate['manufacturer']} {candidate['model']}")
            ok = False
        else:
            pocket = max(0.0, (candidate_required_cross - inner) / 2.0)
            skin = wood - pocket
            print(
                f"PASS {candidate['manufacturer']} {candidate['model']}: "
                f"{cross:.1f} x {length:.1f} x {depth:.1f} mm, "
                f"side pocket {pocket:.2f} mm, skin {skin:.2f} mm"
            )

    if cfg["manufacturing_ready"] is not False:
        print("FAIL display envelope must remain non-manufacturing-ready")
        ok = False

    print("\nSTATUS", "PASS - display envelope engineering only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Evaluate main-cabinet width candidates against a future playfield TV envelope."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "main_body_v07.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    env = cfg["future_playfield_service_envelope"]
    wood = float(cfg["nominal_wood_mm"])
    skin = float(cfg["minimum_remaining_side_skin_mm"])
    clearance = float(env["clearance_each_side_mm"])
    required_cavity = float(env["cross_width_mm"]) + 2.0 * clearance

    print("MAIN BODY v0.7 FUTURE-PLAYFIELD WIDTH STUDY")
    print("=" * 78)
    print(f"Target future TV cross-width      {float(env['cross_width_mm']):8.2f} mm")
    print(f"Clearance each side                {clearance:8.2f} mm")
    print(f"Required cavity width             {required_cavity:8.2f} mm")
    print(f"Minimum remaining side skin       {skin:8.2f} mm")
    print()
    print("Outer W   Inner W   Max cavity @ skin   Margin to target   Status")

    passing = []
    for outer in cfg["candidate_outer_widths_mm"]:
        outer = float(outer)
        inner = outer - 2.0 * wood
        max_pocket_each = wood - skin
        max_cavity = inner + 2.0 * max_pocket_each
        margin = max_cavity - required_cavity
        ok = margin >= 0
        if ok:
            passing.append(outer)
        print(
            f"{outer:7.1f}  {inner:8.1f}  {max_cavity:18.1f}  {margin:16.1f}   "
            f"{'PASS' if ok else 'FAIL'}"
        )

    preferred = float(cfg["preferred_candidate_outer_width_mm"])
    ok = True
    if preferred not in passing:
        print(f"\nFAIL preferred width {preferred:.1f} mm does not satisfy future envelope")
        ok = False
    else:
        print(f"\nPASS preferred width {preferred:.1f} mm satisfies future envelope")

    deviation = preferred - float(cfg["reference_body_width_mm"])
    print(f"Reference-width deviation         {deviation:8.2f} mm")
    if not (10.0 <= deviation <= 50.0):
        print("FAIL preferred width deviation falls outside owner-approved 10–50 mm range")
        ok = False
    else:
        print("PASS preferred width deviation is within owner-approved range")

    current_tv_margin = float(env["cross_width_mm"]) - 540.0
    print(f"Future envelope growth vs C5      {current_tv_margin:8.2f} mm")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.7 study must remain non-manufacturing-ready")
        ok = False

    print("\nSTATUS", "PASS - width study only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

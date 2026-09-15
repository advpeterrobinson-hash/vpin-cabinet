#!/usr/bin/env python3
"""Validate v0.6 backbox/display packaging constraints."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "backbox_v06.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    ref = cfg["reference_backbox"]
    pol = cfg["display_fit_policy"]

    outer = float(ref["outer_width_mm"])
    skin = float(pol["minimum_remaining_side_skin_mm"])
    clr = float(pol["clearance_each_side_mm"])
    max_monitor = outer - 2.0 * skin - 2.0 * clr

    ok = True
    print("BACKBOX v0.6 DISPLAY FIT")
    print("=" * 64)
    print(f"Reference outer width          {outer:8.2f} mm")
    print(f"Minimum remaining side skin    {skin:8.2f} mm")
    print(f"Clearance each side            {clr:8.2f} mm")
    print(f"Maximum preferred chassis      {max_monitor:8.2f} mm")
    print()

    if abs(max_monitor - float(pol["preferred_max_chassis_width_mm"])) > 0.3:
        print("FAIL preferred max width disagrees with derived value")
        ok = False
    else:
        print("PASS preferred monitor-width acquisition limit")

    for ex in cfg["known_examples_brazil"]:
        width = ex.get("width_without_stand_mm", ex.get("width_reported_mm"))
        if width is None:
            continue
        margin = max_monitor - float(width)
        print(f"{ex['model']:<28} width={float(width):7.1f} mm   margin={margin:7.2f} mm   {ex['status']}")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.6 must remain non-manufacturing-ready")
        ok = False

    print()
    print("STATUS", "PASS - engineering packaging only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

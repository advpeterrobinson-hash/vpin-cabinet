#!/usr/bin/env python3
"""Validate the OLED42C5 mechanical drawing datum used by the v0.4 cradle."""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "config" / "design.json"
PF = ROOT / "config" / "playfield_v04.json"


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    base = load(BASE)
    pf = load(PF)
    oled = base["oled"]
    svc = pf["playfield"]
    mech = svc["lg_c5_mechanical_drawing"]
    orient = svc["oled_orientation"]
    cradle = svc["cradle"]

    width = float(oled["native_width_mm"])
    height = float(oled["native_height_mm"])
    h = float(mech["vesa_horizontal_mm"])
    j = float(mech["vesa_vertical_mm"])
    left = float(mech["vesa_left_offset_mm"])
    right = float(mech["vesa_right_offset_mm"])
    top = float(mech["vesa_top_offset_mm"])
    bottom = float(mech["vesa_bottom_offset_mm"])

    if orient["native_left_edge_maps_to"] == "cabinet_front":
        y1, y2 = left, left + h
    else:
        y1, y2 = sorted((width - left, width - left - h))

    if orient["native_top_edge_maps_to"] == "cabinet_left":
        x1, x2 = top, top + j
    else:
        x1, x2 = sorted((height - top, height - top - j))

    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0

    checks = [
        ("LG source marked verified", mech["status"] == "verified-from-LG-2025-detail-dimension-drawing", mech["status"]),
        ("horizontal pattern", abs((y2 - y1) - h) <= 1e-9, f"{y2-y1:.3f} mm"),
        ("vertical pattern", abs((x2 - x1) - j) <= 1e-9, f"{x2-x1:.3f} mm"),
        ("horizontal edge reconciliation", abs((left + h + right) - width) <= 1.0, f"{left+h+right:.3f} vs {width:.3f} mm"),
        ("vertical edge reconciliation", abs((top + j + bottom) - height) <= 1.5, f"{top+j+bottom:.3f} vs {height:.3f} mm"),
        ("configured cradle center X", abs(float(cradle["vesa_center_across_oled_mm"]) - cx) <= 1e-9, f"{cx:.3f} mm"),
        ("configured cradle center Y", abs(float(cradle["vesa_center_from_oled_front_mm"]) - cy) <= 1e-9, f"{cy:.3f} mm"),
        ("VESA center confirmed flag", bool(cradle["vesa_center_position_confirmed"]), str(bool(cradle["vesa_center_position_confirmed"]))),
    ]

    for name, ok, value in checks:
        print(f"{'PASS' if ok else 'FAIL':4}  {name:38} {value}")

    print("\nDerived selected-orientation VESA axes")
    print(f"      cabinet-local X columns: {x1:.3f}, {x2:.3f} mm")
    print(f"      OLED-local Y rows:       {y1:.3f}, {y2:.3f} mm")
    print(f"      center:                  X={cx:.3f}, Y={cy:.3f} mm")

    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    sys.exit(main())

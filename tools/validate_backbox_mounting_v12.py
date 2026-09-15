#!/usr/bin/env python3
"""Validate v0.12 backbox shelf alignment and reusable display-mount policy."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "backbox_mounting_v12.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    align = cfg["structural_alignment"]
    lock = cfg["upright_locking_interface"]
    passages = cfg["aligned_passages"]
    mount = cfg["display_mount_system"]
    policy = cfg["display_size_policy"]

    cab_w = float(align["main_cabinet_outer_width_mm"])
    bb_w = float(align["backbox_outer_width_mm"])
    overhang = (bb_w - cab_w) / 2.0
    off = float(lock["lock_bolt_center_offset_from_common_centerline_mm"])

    derived_shelf = [cab_w / 2.0 - off, cab_w / 2.0 + off]
    derived_floor = [bb_w / 2.0 - off, bb_w / 2.0 + off]

    print("BACKBOX v0.12 SHELF / DISPLAY MOUNT VALIDATION")
    print("=" * 76)
    print(f"Cabinet width                       {cab_w:8.2f} mm")
    print(f"Backbox width                       {bb_w:8.2f} mm")
    print(f"Derived side overhang               {overhang:8.2f} mm")
    print(f"Lock bolt offset from centerline     {off:8.2f} mm")
    print(f"Shelf bolt centers                   {derived_shelf}")
    print(f"Backbox-floor bolt centers           {derived_floor}")
    print()

    ok = True

    if abs(overhang - float(align["backbox_side_overhang_each_side_mm"])) > 0.01:
        print("FAIL documented side overhang does not match widths")
        ok = False
    else:
        print("PASS common-centerline side overhang")

    for actual, expected in zip(lock["bolt_centers_main_shelf_from_left_mm"], derived_shelf):
        if abs(float(actual) - expected) > 0.01:
            print("FAIL main-shelf lock-bolt centers are not derived from common centerline")
            ok = False
            break
    else:
        print("PASS main-shelf lock-bolt centers derive from common centerline")

    for actual, expected in zip(lock["bolt_centers_backbox_floor_from_left_mm"], derived_floor):
        if abs(float(actual) - expected) > 0.01:
            print("FAIL backbox-floor lock-bolt centers are not derived from common centerline")
            ok = False
            break
    else:
        print("PASS backbox-floor lock-bolt centers derive from common centerline")

    if not (align["rear_walls_flush_when_upright"] and align["backbox_floor_bears_on_rear_shelf"]):
        print("FAIL rear shelf / backbox floor structural interface incomplete")
        ok = False
    else:
        print("PASS backbox floor bears on aligned rear shelf")

    if not lock["positive_clamping_required"]:
        print("FAIL upright backbox requires positive clamping")
        ok = False
    else:
        print("PASS dedicated positive upright locking required")

    primary_half = float(passages["primary_fold_harness"]["opening_mm"][0]) / 2.0
    reserve_center = float(passages["secondary_reserve"]["center_offset_from_common_centerline_mm"])
    reserve_half = float(passages["secondary_reserve"]["opening_mm"][0]) / 2.0
    min_clear = float(passages["minimum_edge_clearance_to_lock_bolt_center_mm"])

    passage_edges = [
        (-primary_half, primary_half),
        (reserve_center - reserve_half, reserve_center + reserve_half),
    ]
    for bolt in (-off, off):
        nearest = min(
            abs(bolt - lo) if bolt < lo else abs(bolt - hi) if bolt > hi else 0.0
            for lo, hi in passage_edges
        )
        if nearest < min_clear:
            print(f"FAIL cable passage too close to lock bolt at {bolt:+.1f} mm: {nearest:.1f} mm")
            ok = False
        else:
            print(f"PASS lock bolt {bolt:+.1f} mm clears cable passages: {nearest:.1f} mm")

    upper = mount["upper_backglass_carriage"]
    lower = mount["lower_dmd_carriage"]
    if float(upper["vertical_adjustment_total_mm"]) < 120.0:
        print("FAIL upper carriage vertical adjustment too small")
        ok = False
    else:
        print("PASS upper carriage has large vertical adjustment range")

    depth_range = upper["depth_adjustment_range_from_rear_inner_plane_mm"]
    if float(depth_range[1]) - float(depth_range[0]) < 80.0:
        print("FAIL upper carriage depth adjustment range too small")
        ok = False
    else:
        print("PASS upper carriage provides substantial front/back adjustment")

    if not (upper["replaceable_universal_vesa_plate_required"] and lower["replaceable_bezel_required"]):
        print("FAIL replaceable display interfaces are mandatory")
        ok = False
    else:
        print("PASS replaceable upper VESA plate and lower DMD bezel")

    if not mount["folding_safety"]["monitor_and_dmd_must_remain_secured_at_90_deg_fold"]:
        print("FAIL display mounts must be secure in folded transport position")
        ok = False
    else:
        print("PASS display mounts designed for 90-degree folded transport")

    service = upper["service_envelope_mm"]
    sw, sh, sd = map(float, service)
    for ex in policy["known_fit_examples"]:
        w, h, d = map(float, ex["dimensions_without_stand_mm"])
        fits = w <= sw and h <= sh and d <= sd
        if fits != bool(ex["fits_service_envelope"]):
            print(f"FAIL fit status mismatch for {ex['model']}")
            ok = False
        else:
            print(f"PASS {ex['model']} fits service envelope: {fits}")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.12 must remain non-manufacturing-ready")
        ok = False

    print("\nSTATUS", "PASS - alignment/mounting engineering only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

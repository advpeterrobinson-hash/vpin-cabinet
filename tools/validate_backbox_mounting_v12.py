#!/usr/bin/env python3
"""Validate v0.12 backbox shelf alignment, reusable mounts and closed enclosure."""
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
    enclosure = cfg["enclosure_security"]
    policy = cfg["display_size_policy"]

    cab_w = float(align["main_cabinet_outer_width_mm"])
    bb_w = float(align["backbox_outer_width_mm"])
    overhang = (bb_w - cab_w) / 2.0
    off = float(lock["lock_bolt_center_offset_from_common_centerline_mm"])

    derived_shelf = [cab_w / 2.0 - off, cab_w / 2.0 + off]
    derived_floor = [bb_w / 2.0 - off, bb_w / 2.0 + off]

    print("BACKBOX v0.12 SHELF / DISPLAY / ENCLOSURE VALIDATION")
    print("=" * 80)
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
    reserve_half = float(passages["secondary_reserve"]["minimum_clear_opening_mm"][0]) / 2.0
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

    if "crossmembers" not in mount["structural_load_path"].lower():
        print("FAIL adjustable monitor frame must transfer load into dedicated structural crossmembers")
        ok = False
    else:
        print("PASS adjustable monitor frame uses independent structural load path")

    if not enclosure["closed_backbox_required"] or not enclosure["open_rear_backbox_prohibited"]:
        print("FAIL backbox must remain a closed enclosure")
        ok = False
    else:
        print("PASS closed backbox / open-rear design prohibited")

    perimeter = enclosure["perimeter_frame"]
    if float(perimeter["fixed_rear_shear_panel_min_mm"]) < 12.0:
        print("FAIL fixed rear structural shear panel too thin")
        ok = False
    else:
        print("PASS fixed structural rear shear panel retained")

    service = enclosure["service_access"]
    if not service["normal_display_service_from_front"] or not service["hand_removable_rear_panels_prohibited"]:
        print("FAIL display service / rear access policy does not protect closed structure")
        ok = False
    else:
        print("PASS display service is front-access with tool-only rear access")

    pest = enclosure["pest_and_dust_exclusion"]
    if float(pest["target_mesh_opening_max_mm"]) > 1.0:
        print("FAIL insect mesh target too open")
        ok = False
    else:
        print("PASS fine insect mesh target <= 1.0 mm")
    if not (pest["perimeter_floor_shelf_gasket_required"] and pest["primary_passage_requires_split_gland_or_compression_insert"] and pest["reserve_passage_sealed_when_unused"]):
        print("FAIL pest/dust exclusion around shelf/passports incomplete")
        ok = False
    else:
        print("PASS shelf seam and cable passports are gasketed/sealed")

    electrical = enclosure["electrical_touch_safety"]
    if not electrical["no_exposed_mains_terminals_in_backbox"]:
        print("FAIL exposed mains terminals prohibited in backbox")
        ok = False
    else:
        print("PASS no exposed mains terminals in backbox")
    if "12 V" not in electrical["fan_supply"]:
        print("FAIL ventilation fan supply is not the intended low-voltage fused bus")
        ok = False
    else:
        print("PASS ventilation remains on fused low-voltage AUX bus")

    child = enclosure["child_resistance"]
    if not (child["tool_required_for_internal_access"] and child["rear_fan_grilles_finger_safe"] and child["no_large_unprotected_service_openings"]):
        print("FAIL child-resistant enclosure policy incomplete")
        ok = False
    else:
        print("PASS tool-required, finger-guarded child-resistant enclosure")

    sw, sh, sd = map(float, upper["service_envelope_mm"])
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

    print("\nSTATUS", "PASS - alignment/mounting/enclosure engineering only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

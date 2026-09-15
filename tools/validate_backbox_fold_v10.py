#!/usr/bin/env python3
"""Validate v0.10 folding-backbox transport design parameters."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "backbox_fold_v10.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    cab = cfg["cabinet"]
    box = cfg["backbox"]
    lock = cfg["upright_locking"]
    harness = cfg["cable_harness"]
    transport = cfg["folded_transport"]
    cnc = cfg["cnc_flatpack"]

    expected_inset = (
        float(box["outer_width_mm"])
        - float(cab["outer_width_mm"])
        - 60.325
    ) / 2.0
    width_delta = float(box["outer_width_mm"]) - float(cab["outer_width_mm"])
    pivot_y = float(cab["side_length_mm"]) - float(cab["pivot_from_rear_mm"])
    pivot_z = float(cab["pivot_from_bottom_mm"])

    checks: list[tuple[str, bool, str]] = []
    checks.append((
        "custom-width WPC hinge inset",
        abs(expected_inset - float(box["hinge_floor_bolt_inset_each_side_mm"])) <= 0.05,
        f"derived {expected_inset:.3f} mm",
    ))
    checks.append((
        "backbox wide enough for WPC side hinges",
        width_delta >= float(box["minimum_width_overhang_for_wpc_hinges_mm"]),
        f"width delta {width_delta:.1f} mm",
    ))
    checks.append((
        "two independent upright safety fasteners",
        bool(lock["required"]) and int(lock["count"]) >= 2,
        f"count {lock['count']}",
    ))
    checks.append((
        "fold direction/rotation",
        transport["fold_direction"] == "forward over playfield"
        and float(transport["target_rotation_deg"]) >= 85.0,
        f"{transport['target_rotation_deg']} deg forward",
    ))
    checks.append((
        "transport rests protect glass",
        bool(transport["dedicated_transport_rest_required"])
        and float(transport["minimum_clearance_to_playfield_glass_mm"]) >= 15.0
        and float(transport["minimum_clearance_after_pad_compression_mm"]) >= 10.0,
        "dedicated structural rests + clearance",
    ))
    checks.append((
        "speaker fascia compatible with folding",
        bool(transport["speaker_grilles_must_be_flush_or_removable"]),
        "flush or removable",
    ))
    checks.append((
        "positive folded-state retention",
        bool(transport["positive_folded_retention_required"]),
        transport["baseline_retention"],
    ))
    checks.append((
        "cable service loop",
        float(harness["minimum_service_loop_mm"]) >= 250.0
        and float(harness["minimum_dynamic_bend_radius_mm"]) >= 50.0
        and bool(harness["abrasion_grommet_required"])
        and bool(harness["strain_relief_both_ends"]),
        f"loop {harness['minimum_service_loop_mm']} mm / bend R {harness['minimum_dynamic_bend_radius_mm']} mm",
    ))
    checks.append((
        "CNC locates all hinge/transport geometry",
        all(bool(cnc[k]) for k in (
            "pivot_holes_cnc_located",
            "hinge_floor_holes_cnc_located",
            "upright_lock_holes_cnc_located",
            "cable_openings_cnc_cut",
            "transport_rest_mounts_cnc_located",
        )) and cnc["builder_freehand_alignment_required"] is False,
        "no builder freehand alignment",
    ))
    checks.append((
        "not manufacturing-ready",
        cfg["manufacturing_ready"] is False,
        str(cfg["manufacturing_ready"]),
    ))

    print("BACKBOX FOLD v0.10 ENGINEERING CHECKS")
    print("=" * 72)
    print(f"Cabinet body width               {float(cab['outer_width_mm']):8.2f} mm")
    print(f"Backbox width                    {float(box['outer_width_mm']):8.2f} mm")
    print(f"Width difference                 {width_delta:8.2f} mm")
    print(f"Calculated hinge-floor inset     {expected_inset:8.3f} mm")
    print(f"Main pivot center Y/Z            {pivot_y:8.2f} / {pivot_z:8.2f} mm")
    print()

    ok = True
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        print(f"{status:4}  {name:43} {detail}")
        ok = ok and passed

    print()
    print("STATUS", "PASS - engineering design only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

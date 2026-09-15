#!/usr/bin/env python3
"""Validate service-I/O v0.8 panel packaging and separation."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "service_io_v08.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    body_w = float(cfg["body_outer_width_mm"])
    power = cfg["rear_power_fascia"]
    service = cfg["rear_service_fascia"]
    rules = cfg["rear_zone_rules"]

    p_x0 = float(power["rear_x_mm"])
    p_x1 = p_x0 + float(power["outer_width_mm"])
    s_x0 = float(service["rear_x_mm"])
    s_x1 = s_x0 + float(service["outer_width_mm"])
    gap = s_x0 - p_x1

    checks: list[tuple[str, bool, str]] = []
    checks.append(("power fascia inside body", 0 <= p_x0 < p_x1 <= body_w, f"X {p_x0:.1f}..{p_x1:.1f} / {body_w:.1f} mm"))
    checks.append(("service fascia inside body", 0 <= s_x0 < s_x1 <= body_w, f"X {s_x0:.1f}..{s_x1:.1f} / {body_w:.1f} mm"))
    checks.append(("power/service fascias do not overlap", gap > 0, f"gap {gap:.1f} mm"))
    checks.append(("power/service clear distance", gap >= float(rules["minimum_clear_distance_between_power_and_signal_fascias_mm"]), f"gap {gap:.1f} mm"))

    for name, p in (("power", power), ("service", service)):
        border_x = 0.5 * (float(p["outer_width_mm"]) - float(p["cabinet_window_width_mm"]))
        border_z = 0.5 * (float(p["outer_height_mm"]) - float(p["cabinet_window_height_mm"]))
        checks.append((f"{name} fascia has >= 8 mm window border", border_x >= 8.0 and border_z >= 8.0, f"border {border_x:.1f} x {border_z:.1f} mm"))

    checks.append(("mains enclosure explicitly required", bool(power["internal_mains_enclosure_required"]), str(power["internal_mains_enclosure_required"])))
    checks.append(("mains/signal routing separation specified", bool(rules["mains_and_signal_internal_routing_separated"]), str(rules["mains_and_signal_internal_routing_separated"])))
    checks.append(("service fascia replaceable", bool(rules["service_fascia_replaceable_without_removing_rear_panel"]), str(rules["service_fascia_replaceable_without_removing_rear_panel"])))

    theme = cfg["design_language"]
    checks.append(("white engraving defined", "white" in str(theme["legend_method"]).lower(), theme["legend_method"]))
    checks.append(("engraving text released as curves", bool(theme["text_as_curves_in_release_files"]), str(theme["text_as_curves_in_release_files"])))
    checks.append(("v0.8 remains non-manufacturing-ready", cfg["manufacturing_ready"] is False, str(cfg["manufacturing_ready"])))

    ok = True
    print("SERVICE I/O v0.8 PACKAGING")
    print("=" * 72)
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<46} {detail}")
        ok = ok and passed

    print()
    print(f"Rear power/service fascia gap: {gap:.1f} mm")
    print(f"External service ports: {len(service['ports'])}")
    print("STATUS", "PASS - engineering packaging only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

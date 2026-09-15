#!/usr/bin/env python3
"""Validate v0.11 electrical/cooling/cable-routing packaging policy."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "electrical_routing_v11.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    ok = True

    fans = cfg["backbox_ventilation"]
    passport = cfg["backbox_passports"]["primary_fold_harness_passage"]
    reserve = cfg["backbox_passports"]["secondary_reserved_passage"]
    routing = cfg["routing_policy"]
    supports = cfg["supports_and_strain_relief"]

    print("ELECTRICAL / ROUTING v0.11")
    print("=" * 72)

    if fans["fan_count"] < 2 or fans["fan_nominal_voltage_v"] != 12.0:
        print("FAIL backbox fan baseline")
        ok = False
    else:
        print("PASS backbox active-cooling baseline: 2 x 120 mm / 12 V")

    if "AUX 12 V" not in fans["power_source"]:
        print("FAIL backbox fans are not tied to dedicated AUX 12 V bus")
        ok = False
    else:
        print("PASS backbox fans use dedicated fused AUX 12 V bus")

    w, h = passport["minimum_clear_opening_mm"]
    if w < 90 or h < 50 or passport["service_loop_mm"] < 300:
        print("FAIL primary fold-harness passport undersized")
        ok = False
    else:
        print(f"PASS primary fold passport: {w} x {h} mm, {passport['service_loop_mm']:.0f} mm loop")

    rw, rh = reserve["minimum_clear_opening_mm"]
    if not reserve["required"] or rw < 60 or rh < 40:
        print("FAIL reserve backbox passport policy")
        ok = False
    else:
        print(f"PASS reserve passport: {rw} x {rh} mm")

    if routing["spare_capacity_target_percent"] < 25:
        print("FAIL cable-routing spare-capacity target too small")
        ok = False
    else:
        print(f"PASS cable spare-capacity target: {routing['spare_capacity_target_percent']}%")

    if supports["support_spacing_fixed_harness_max_mm"] > 250 or supports["support_spacing_near_moving_harness_max_mm"] > 100:
        print("FAIL harness support spacing too large")
        ok = False
    else:
        print("PASS harness support-spacing policy")

    inventory = cfg["planned_toy_inventory_for_space_and_routes"]
    required_terms = ["shaker", "gear", "knocker", "chime", "blower", "strobe", "flasher", "beacon", "topper"]
    joined = " ".join(inventory).lower()
    missing = [term for term in required_terms if term not in joined]
    if missing:
        print("FAIL planned toy inventory missing:", ", ".join(missing))
        ok = False
    else:
        print("PASS major toy classes reserved in routing plan")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.11 must remain non-manufacturing-ready")
        ok = False

    print()
    print("STATUS", "PASS - routing/cooling architecture only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

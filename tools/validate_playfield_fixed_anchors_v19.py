#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ANCH = ROOT / "config" / "playfield_fixed_anchors_v19.json"
MECH = ROOT / "config" / "playfield_mechanics_v18.json"


def main() -> int:
    a = json.loads(ANCH.read_text(encoding="utf-8"))
    m = json.loads(MECH.read_text(encoding="utf-8"))
    fs = a["closed_front_support"]
    sa = a["safety_stay_fixed_anchor"]
    ga = a["gas_strut_fixed_anchor"]
    cs = m["closed_support"]
    cr = m["cradle"]

    checks: list[tuple[str, bool, str]] = []
    left_center = float(cr["left_side_rail_x_mm"]) + float(cr["side_rail_thickness_x_mm"]) / 2.0
    right_center = float(cr["right_side_rail_x_mm"]) + float(cr["side_rail_thickness_x_mm"]) / 2.0
    pads = [float(v) for v in cs["pad_center_x_mm"]]
    checks.append(("closed pads centered under side rails", abs(pads[0]-left_center) < 0.01 and abs(pads[1]-right_center) < 0.01, f"pads={pads} rail centers={[left_center,right_center]}"))
    checks.append(("support pad narrower than/near local support zone", float(cs["pad_size_mm"][0]) <= float(fs["steel_seat_inboard_reach_x_mm"]), f"pad {cs['pad_size_mm'][0]} / seat {fs['steel_seat_inboard_reach_x_mm']} mm"))
    checks.append(("front support plywood doubler >=18 mm", float(fs["sidewall_doubler_thickness_x_mm"]) >= 18.0, str(fs["sidewall_doubler_thickness_x_mm"])))
    checks.append(("front steel seat >=3 mm", float(fs["steel_seat_thickness_z_mm"]) >= 3.0, str(fs["steel_seat_thickness_z_mm"])))
    checks.append(("safety stay anchor doubler >=18 mm", float(sa["plywood_doubler_thickness_x_mm"]) >= 18.0, str(sa["plywood_doubler_thickness_x_mm"])))
    checks.append(("safety stay captive steel >=6 mm", float(sa["steel_nut_plate_thickness_x_mm"]) >= 6.0, str(sa["steel_nut_plate_thickness_x_mm"])))
    checks.append(("gas anchor doubler >=18 mm", float(ga["plywood_doubler_thickness_x_mm"]) >= 18.0, str(ga["plywood_doubler_thickness_x_mm"])))
    checks.append(("gas anchor captive steel >=6 mm", float(ga["steel_nut_plate_thickness_x_mm"]) >= 6.0, str(ga["steel_nut_plate_thickness_x_mm"])))
    checks.append(("stay hole pattern remains open", "TBD" in sa["final_thread_and_hole_pattern_status"], sa["final_thread_and_hole_pattern_status"]))
    checks.append(("gas bracket pattern remains open", "TBD" in ga["final_thread_and_hole_pattern_status"], ga["final_thread_and_hole_pattern_status"]))
    checks.append(("package remains non-manufacturing-ready", a["manufacturing_ready"] is False, str(a["manufacturing_ready"])))

    print("PLAYFIELD FIXED ANCHORS v0.19 VALIDATION")
    print("="*76)
    ok=True
    for name,passed,detail in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {name:<48} {detail}")
        ok = ok and passed
    print("STATUS", "PASS - fixed anchor packaging" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

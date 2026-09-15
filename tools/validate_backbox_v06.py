#!/usr/bin/env python3
"""Validate v0.6 future-proof backbox/display packaging constraints."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "backbox_v06.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    ref = cfg["reference_backbox"]
    fut = cfg["future_proof_backbox"]
    pol = cfg["display_fit_policy"]

    wood = float(ref["nominal_side_material_mm"])
    target_outer = float(fut["target_outer_width_mm"])
    target_inner = target_outer - 2.0 * wood
    service_w = float(pol["service_envelope_width_mm"])
    clr = (target_inner - service_w) / 2.0

    ok = True
    print("BACKBOX v0.6 FUTURE-PROOF DISPLAY FIT")
    print("=" * 68)
    print(f"Reference outer width              {float(ref['outer_width_mm']):8.2f} mm")
    print(f"Future-proof outer width           {target_outer:8.2f} mm")
    print(f"Reference-to-target delta          {target_outer-float(ref['outer_width_mm']):8.2f} mm")
    print(f"Target inner width                 {target_inner:8.2f} mm")
    print(f"Display service envelope width     {service_w:8.2f} mm")
    print(f"Envelope clearance each side       {clr:8.2f} mm")
    print()

    if abs(target_outer - float(ref["outer_width_mm"])) > 50.0:
        print("FAIL width deviation exceeds owner-approved 50 mm future-proof allowance")
        ok = False
    else:
        print("PASS backbox width deviation remains within owner-approved allowance")

    if clr < float(pol["minimum_clearance_each_side_mm"]):
        print("FAIL service envelope has insufficient side clearance")
        ok = False
    else:
        print("PASS service envelope side clearance")

    if abs(service_w - float(pol["preferred_max_chassis_width_mm"])) > 0.1:
        print("FAIL preferred chassis acquisition limit disagrees with service envelope")
        ok = False
    else:
        print("PASS preferred chassis acquisition limit")

    if not fut["removable_monitor_carrier_required"] or not fut["removable_front_bezel_required"]:
        print("FAIL future-proof design requires removable carrier and bezel")
        ok = False
    else:
        print("PASS replaceable carrier + bezel policy")

    for ex in cfg["known_examples_brazil"]:
        width = ex.get("width_without_stand_mm", ex.get("width_reported_mm"))
        if width is None:
            continue
        margin = service_w - float(width)
        print(f"{ex['model']:<28} width={float(width):7.1f} mm   service-margin={margin:7.2f} mm   {ex['status']}")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.6 must remain non-manufacturing-ready")
        ok = False

    print()
    print("STATUS", "PASS - future-proof engineering packaging only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

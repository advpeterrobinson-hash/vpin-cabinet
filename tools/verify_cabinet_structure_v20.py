#!/usr/bin/env python3
"""Headless FreeCAD verification for cabinet structure v0.20."""
from __future__ import annotations

import json
import os

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_structure_v20.json")


def close(a: float, b: float, tol: float = 0.25) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    cab = cfg["cabinet"]
    j = cfg["cnc_joinery"]
    pc = cfg["pc_drawer"]
    glass_cfg = cfg["playfield_glass"]

    doc = App.openDocument(MASTER)
    group = doc.getObject("CabinetStructureV20")
    if group is None:
        raise RuntimeError("CabinetStructureV20 group missing")

    required = [
        "CapturedFrontPanelV20", "CapturedRearPanelV20", "CapturedBottomV20",
        "LowCrossmember1V20", "LowCrossmember2V20", "LowCrossmember3V20",
        "LeftJoineryPocketGhostV20", "RightJoineryPocketGhostV20",
        "LegSideDoublerFLV20", "LegSideDoublerFRV20", "LegSideDoublerRLV20", "LegSideDoublerRRV20",
        "LegEndDoublerFLV20", "LegEndDoublerFRV20", "LegEndDoublerRLV20", "LegEndDoublerRRV20",
        "PCSubrailLeftV20", "PCSubrailRightV20", "PCTrayStowedV20", "PCTrayServiceGhostV20",
        "PCSlideLeftKeepoutV20", "PCSlideRightKeepoutV20", "PCServiceEnvelopeV20",
        "PlayfieldGlassTargetV20", "SideRailLeftV20", "SideRailRightV20",
        "LockdownBarEnvelopeV20", "LockdownReceiverKeepoutV20",
    ]
    for suffix in ("FL", "FR", "RL", "RR"):
        required += [f"LegBracketKeepout{suffix}V20", f"WheelKeepout{suffix}V20"]
    for zone in ("Front", "Rear"):
        required += [f"SSF{zone}LeftKeepoutV20", f"SSF{zone}RightKeepoutV20"]

    ok = True
    print("CABINET STRUCTURE v0.20 FREECAD VERIFY")
    print("=" * 80)
    for name in required:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    bottom = doc.getObject("CapturedBottomV20")
    if bottom:
        bb = bottom.Shape.BoundBox
        expected = (
            float(j["bottom_blank_width_mm"]),
            float(j["bottom_blank_length_mm"]),
            float(j["bottom_panel_thickness_mm"]),
        )
        actual = (bb.XLength, bb.YLength, bb.ZLength)
        if not all(close(a, e) for a, e in zip(actual, expected)):
            print(f"FAIL captured bottom bounds {actual} expected {expected}")
            ok = False
        else:
            print(f"PASS captured bottom nominal {expected[0]:.1f} x {expected[1]:.1f} x {expected[2]:.1f} mm")

    front = doc.getObject("CapturedFrontPanelV20")
    rear = doc.getObject("CapturedRearPanelV20")
    if front and rear:
        if not close(front.Shape.BoundBox.XLength, float(j["front_rear_blank_width_mm"])):
            print("FAIL front captured width")
            ok = False
        if not close(rear.Shape.BoundBox.XLength, float(j["front_rear_blank_width_mm"])):
            print("FAIL rear captured width")
            ok = False

    # Low crossmembers must remain below the documented SSF zones.
    ssf_min_z = min(float(z["z_mm"][0]) for z in cfg["ssf_keepouts"]["sidewall_exciter_zones_each_side"])
    for idx in range(1, 4):
        obj = doc.getObject(f"LowCrossmember{idx}V20")
        if obj and obj.Shape.BoundBox.ZMax >= ssf_min_z:
            print(f"FAIL LowCrossmember{idx} enters SSF height")
            ok = False
    if ok:
        print("PASS low crossmembers remain below SSF exciter-height zones")

    tray = doc.getObject("PCTrayStowedV20")
    tray_service = doc.getObject("PCTrayServiceGhostV20")
    service_env = doc.getObject("PCServiceEnvelopeV20")
    if tray and tray_service:
        travel = tray.Shape.BoundBox.YMin - tray_service.Shape.BoundBox.YMin
        if not close(travel, float(pc["slide_travel_mm"]), 0.05):
            print(f"FAIL PC tray travel {travel:.2f} mm")
            ok = False
        else:
            print(f"PASS PC tray internal service travel {travel:.1f} mm")
    if service_env:
        shell_parts = [doc.getObject("CabinetLeftPad"), doc.getObject("CabinetRightPad")]
        for shell in shell_parts:
            if shell is not None and service_env.Shape.common(shell.Shape).Volume > 1.0:
                print(f"FAIL PC service envelope intersects sidewall {shell.Name}")
                ok = False
        print("PASS PC service envelope remains between sidewalls" if ok else "INFO PC service-envelope sidewall check failed")

    # Glass target uses outer-width side cover and must remain narrower than body.
    glass = doc.getObject("PlayfieldGlassTargetV20")
    if glass:
        bb = glass.Shape.BoundBox
        if bb.XMin < -0.1 or bb.XMax > float(cab["outer_width_mm"]) + 0.1:
            print(f"FAIL glass exceeds body X bounds {bb.XMin:.2f}..{bb.XMax:.2f}")
            ok = False
        elif not close(bb.XLength, float(glass_cfg["width_mm"]), 0.05):
            print(f"FAIL glass width {bb.XLength:.2f} mm")
            ok = False
        else:
            print(f"PASS glass target width {bb.XLength:.1f} mm within 600 mm body")

    if "BLOCKED" not in str(group.LegHoleStatus):
        print("FAIL leg-hole manufacturing block missing")
        ok = False
    else:
        print("PASS leg holes remain blocked pending hardware")
    if "BLOCKED" not in str(group.PCSlideHoleStatus):
        print("FAIL PC slide-hole manufacturing block missing")
        ok = False
    else:
        print("PASS PC slide holes remain blocked pending hardware")
    if "DO NOT ORDER" not in str(group.GlassOrderStatus):
        print("FAIL glass purchase block missing")
        ok = False
    else:
        print("PASS glass purchase remains blocked pending mockup")
    if "BLOCKED" not in str(group.LockdownHoleStatus):
        print("FAIL lockdown receiver-hole block missing")
        ok = False
    else:
        print("PASS lockdown receiver holes remain blocked")
    if "NOT FOR CNC/METAL PRODUCTION" not in str(group.Status):
        print("FAIL v0.20 production block missing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - v0.20 cabinet structure packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

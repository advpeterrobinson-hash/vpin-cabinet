#!/usr/bin/env python3
"""Headless FreeCAD verification for v0.14 structure packaging geometry.

Historical filename retained for compatibility. Width-dependent expectations are
loaded from the active v0.14 structure config so the verifier follows the 600 mm
v0.17 cabinet baseline rather than hard-coding the old 580 mm body.
"""
from __future__ import annotations

import json
import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/structure_geometry_v14.json")


def close(a: float, b: float, tol: float = 0.2) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    cab = cfg["main_cabinet"]
    backbox = cfg["backbox"]

    cab_w = float(cab["outer_width_mm"])
    wood = float(cab["wood_mm"])
    expected_inner_w = cab_w - 2.0 * wood
    bb_w = float(backbox["outer_width_mm"])
    bb_d = float(backbox["outer_depth_mm"])
    bb_wood = float(backbox["wood_mm"])
    expected_bb_xmin = (cab_w - bb_w) / 2.0
    rear_h = float(cab["rear_height_mm"])
    shelf_depth = float(cab["rear_shelf"]["depth_mm"])

    doc = App.openDocument(MASTER)
    ok = True

    group = doc.getObject("StructureV14")
    if group is None:
        raise RuntimeError("StructureV14 group missing")
    print("PASS StructureV14 group exists")

    required = [
        "RearShelfV14",
        "BackboxFloorV14",
        "BackboxLeftSideV14",
        "BackboxRightSideV14",
        "BackboxTopV14",
        "BackboxServiceDoorV14",
        "BackboxPivotAxisV14",
        "LeftPivotHoleGhostV14",
        "RightPivotHoleGhostV14",
        "WpcHingeLeftEnvelopeV14",
        "WpcHingeRightEnvelopeV14",
        "BackboxFanGhost1V14",
        "BackboxFanGhost2V14",
    ]
    for name in required:
        obj = doc.getObject(name)
        if obj is None or obj.Shape.isNull():
            print("FAIL missing/invalid", name)
            ok = False
        else:
            print("PASS", name)

    shelf = doc.getObject("RearShelfV14")
    if shelf:
        bb = shelf.Shape.BoundBox
        if not (
            close(bb.XLength, expected_inner_w)
            and close(bb.YLength, shelf_depth)
            and close(bb.ZLength, float(cab["rear_shelf"]["thickness_mm"]))
        ):
            print("FAIL rear shelf bounds", bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print(f"PASS rear shelf {expected_inner_w:.1f} x {shelf_depth:.3f} x {float(cab['rear_shelf']['thickness_mm']):.1f} mm")

    floor = doc.getObject("BackboxFloorV14")
    if floor:
        bb = floor.Shape.BoundBox
        if not (
            close(bb.XLength, bb_w)
            and close(bb.YLength, bb_d)
            and close(bb.ZLength, bb_wood)
            and close(bb.XMin, expected_bb_xmin)
            and close(bb.YMax, float(cab["side_length_mm"]))
            and close(bb.ZMin, float(backbox["floor_bottom_z_mm"]))
        ):
            print("FAIL backbox floor placement/bounds", bb.XMin, bb.YMax, bb.ZMin, bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print("PASS backbox floor centered, rear-flush and shelf-supported")

    door = doc.getObject("BackboxServiceDoorV14")
    if door:
        bb = door.Shape.BoundBox
        door_cfg = backbox["service_door"]
        if not (
            close(bb.XLength, float(door_cfg["opening_width_mm"]))
            and close(bb.YLength, float(door_cfg["door_thickness_mm"]))
            and close(bb.ZLength, float(door_cfg["opening_height_mm"]))
        ):
            print("FAIL service door envelope", bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print("PASS keyed service-door packaging matches config")

    if getattr(group, "HingeFamily", "") != "01-9011-L/R + 02-4352 + 4322-01139-12B":
        print("FAIL WPC hinge hardware family property")
        ok = False
    else:
        print("PASS WPC hinge hardware family recorded")

    status = getattr(group, "Status", "")
    if "NOT FOR CNC PRODUCTION" not in status:
        print("FAIL v0.14 must remain non-production packaging")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print(f"PASS active cabinet width reference {cab_w:.1f} mm / backbox XMin {expected_bb_xmin:.1f} mm")
    print("STATUS", "PASS - v0.14 structure packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


main()

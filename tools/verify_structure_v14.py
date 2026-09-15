#!/usr/bin/env python3
"""Headless FreeCAD verification for v0.14 structure packaging geometry."""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")


def close(a: float, b: float, tol: float = 0.2) -> bool:
    return abs(a - b) <= tol


def main() -> None:
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
        if not (close(bb.XLength, 544.0) and close(bb.YLength, 180.975) and close(bb.ZLength, 18.0)):
            print("FAIL rear shelf bounds", bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print("PASS rear shelf 544 x 180.975 x 18 mm")

    floor = doc.getObject("BackboxFloorV14")
    if floor:
        bb = floor.Shape.BoundBox
        if not (
            close(bb.XLength, 780.0)
            and close(bb.YLength, 254.0)
            and close(bb.ZLength, 18.0)
            and close(bb.XMin, -100.0)
            and close(bb.YMax, 1308.1)
            and close(bb.ZMin, 596.9)
        ):
            print("FAIL backbox floor placement/bounds", bb.XMin, bb.YMax, bb.ZMin, bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print("PASS backbox floor centered, rear-flush and shelf-supported")

    door = doc.getObject("BackboxServiceDoorV14")
    if door:
        bb = door.Shape.BoundBox
        if not (close(bb.XLength, 520.0) and close(bb.YLength, 15.0) and close(bb.ZLength, 460.0)):
            print("FAIL service door envelope", bb.XLength, bb.YLength, bb.ZLength)
            ok = False
        else:
            print("PASS keyed service-door packaging 520 x 460 x 15 mm")

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

    print("STATUS", "PASS - v0.14 structure packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


main()

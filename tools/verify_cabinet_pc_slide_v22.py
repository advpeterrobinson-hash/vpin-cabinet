#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_pc_slide_v22.json")

REQUIRED = [
    "PCSlidingShelfStowedV22",
    "PCSlidingShelfServiceGhostV22",
    "PCSlideFixedLeftV22",
    "PCSlideFixedRightV22",
    "PCSlideServiceLeftGhostV22",
    "PCSlideServiceRightGhostV22",
    "PCOpenCaseReferenceStowedV22",
    "PCOpenCaseReferenceServiceGhostV22",
    "PCShelfStowedRetainerV22",
]


def main() -> None:
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    pc = cfg["pc_slide"]

    doc = App.openDocument(MASTER)
    group = doc.getObject("CabinetPCSlideV22")
    if group is None:
        raise RuntimeError("CabinetPCSlideV22 group missing")

    ok = True
    print("PC SERVICE v0.22 FREECAD VERIFY")
    print("=" * 72)
    for name in REQUIRED:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    shelf = doc.getObject("PCSlidingShelfStowedV22")
    service = doc.getObject("PCSlidingShelfServiceGhostV22")
    case = doc.getObject("PCOpenCaseReferenceStowedV22")
    if shelf and service:
        travel = shelf.Shape.BoundBox.YMin - service.Shape.BoundBox.YMin
        if abs(travel - float(pc["travel_mm"])) > 0.1:
            print(f"FAIL slide travel {travel:.1f} mm")
            ok = False
        else:
            print(f"PASS slide travel {travel:.1f} mm")

    if shelf and case:
        bb = shelf.Shape.BoundBox
        cb = case.Shape.BoundBox
        if cb.XMin < bb.XMin or cb.XMax > bb.XMax or cb.YMin < bb.YMin or cb.YMax > bb.YMax:
            print("FAIL open case reference overhangs shelf")
            ok = False
        else:
            print("PASS open case reference fits fully on shelf")

    if "NO SECOND SLED" not in str(group.CaseMountPolicy):
        print("FAIL direct case-mount policy missing")
        ok = False
    else:
        print("PASS open case bolts directly to shelf / no second sled")

    if "BLOCKED" not in str(group.HoleStatus):
        print("FAIL physical-measurement hole gate missing")
        ok = False
    else:
        print("PASS slide/case holes remain blocked pending physical measurement")

    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL manufacturing block missing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - simple PC slide FreeCAD packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

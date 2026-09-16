#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_rear_cpu_shelf_v24.json")

REQUIRED = [
    "RearPanelWithCPUHatchV24",
    "RearCPUHatchOpeningGhostV24",
    "RearCPUServiceDoorClosedV24",
    "RearCPUServiceDoorOpenGhostV24",
    "RearCPUShelfStowedV24",
    "RearCPUShelfServiceGhostV24",
    "RearCPUSupportRailLeftV24",
    "RearCPUSupportRailRightV24",
    "RearCPUFixedSlideLeftV24",
    "RearCPUFixedSlideRightV24",
    "RearCPUOpenCaseStowedV24",
    "RearCPUOpenCaseServiceGhostV24",
    "RearCPUStowedRetainerV24",
]


def main() -> None:
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    pc = cfg["pc_shelf"]
    case = cfg["open_pc_case_reference"]

    doc = App.openDocument(MASTER)
    group = doc.getObject("CabinetRearCPUShelfV24")
    if group is None:
        raise RuntimeError("CabinetRearCPUShelfV24 group missing")

    ok = True
    print("REAR CPU SHELF v0.24 FREECAD VERIFY")
    print("=" * 78)
    for name in REQUIRED:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    shelf = doc.getObject("RearCPUShelfStowedV24")
    service = doc.getObject("RearCPUShelfServiceGhostV24")
    chassis = doc.getObject("RearCPUOpenCaseStowedV24")
    opening = doc.getObject("RearCPUHatchOpeningGhostV24")

    if shelf and service:
        travel = service.Shape.BoundBox.YMin - shelf.Shape.BoundBox.YMin
        passed = abs(travel - float(pc["travel_mm"])) <= 0.1
        print(f"{'PASS' if passed else 'FAIL'} rearward shelf travel {travel:.1f} mm")
        ok = ok and passed

    if shelf and chassis:
        sb = shelf.Shape.BoundBox
        cb = chassis.Shape.BoundBox
        passed = cb.XMin >= sb.XMin and cb.XMax <= sb.XMax and cb.YMin >= sb.YMin and cb.YMax <= sb.YMax
        print(f"{'PASS' if passed else 'FAIL'} rotated open-case reference fits case-sized shelf")
        ok = ok and passed

    if shelf and opening:
        passed = opening.Shape.BoundBox.XLength >= shelf.Shape.BoundBox.XLength + 39.0
        print(f"{'PASS' if passed else 'FAIL'} rear hatch provides lateral shelf clearance")
        ok = ok and passed

    if "REARWARD" not in str(group.ServiceDirection):
        print("FAIL rear service direction property")
        ok = False
    else:
        print("PASS routine service direction is rearward / playfield closed")

    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL manufacturing block missing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - rear CPU shelf FreeCAD packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

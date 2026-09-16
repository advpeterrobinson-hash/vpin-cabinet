#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_rear_pc_service_v23.json")

REQUIRED = [
    "RearPanelWithPCDoorV23",
    "RearPCDoorClearOpeningGhostV23",
    "RearPCFrameLeftV23", "RearPCFrameRightV23", "RearPCFrameBottomV23", "RearPCFrameTopV23",
    "RearPCServiceDoorClosedV23", "RearPCServiceDoorOpenGhostV23", "RearPCDoorLatchKeepoutV23",
    "RearPCShelfStowedV23", "RearPCShelfServiceGhostV23",
    "RearPCSpacerLeftV23", "RearPCSpacerRightV23",
    "RearPCSlideFixedLeftV23", "RearPCSlideFixedRightV23",
    "RearPCSlideServiceLeftGhostV23", "RearPCSlideServiceRightGhostV23",
    "RearPCOpenCaseStowedV23", "RearPCOpenCaseServiceGhostV23",
    "RearPCStowedRetainerV23", "RearPCCableLoopKeepoutV23",
]


def main() -> None:
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    pc = cfg["pc_slide"]
    door_cfg = cfg["rear_service_door"]

    doc = App.openDocument(MASTER)
    group = doc.getObject("CabinetRearPCServiceV23")
    if group is None:
        raise RuntimeError("CabinetRearPCServiceV23 group missing")

    ok = True
    print("REAR PC SERVICE v0.23 FREECAD VERIFY")
    print("=" * 80)
    for name in REQUIRED:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    rear = doc.getObject("RearPanelWithPCDoorV23")
    opening = doc.getObject("RearPCDoorClearOpeningGhostV23")
    shelf = doc.getObject("RearPCShelfStowedV23")
    service = doc.getObject("RearPCShelfServiceGhostV23")
    case = doc.getObject("RearPCOpenCaseStowedV23")

    if rear and opening:
        common = rear.Shape.common(opening.Shape).Volume
        if common > 1.0:
            print(f"FAIL rear panel still occupies PC-door aperture: {common:.1f} mm3")
            ok = False
        else:
            print("PASS rear panel contains actual PC-service aperture")

    if opening:
        bb = opening.Shape.BoundBox
        if abs(bb.XLength - float(door_cfg["raw_aperture_width_x_mm"])) > 0.1 or abs(bb.ZLength - float(door_cfg["raw_aperture_height_z_mm"])) > 0.1:
            print(f"FAIL rear aperture geometry {bb.XLength:.1f} x {bb.ZLength:.1f} mm")
            ok = False
        else:
            print(f"PASS rear aperture {bb.XLength:.1f} x {bb.ZLength:.1f} mm")

    if shelf and service:
        travel = service.Shape.BoundBox.YMin - shelf.Shape.BoundBox.YMin
        if abs(travel - float(pc["travel_mm"])) > 0.1 or travel <= 0:
            print(f"FAIL PC shelf rearward travel {travel:.1f} mm")
            ok = False
        else:
            print(f"PASS PC shelf travels {travel:.1f} mm toward REAR")

    if shelf and case:
        sb = shelf.Shape.BoundBox
        cb = case.Shape.BoundBox
        if cb.XMin < sb.XMin or cb.XMax > sb.XMax or cb.YMin < sb.YMin or cb.YMax > sb.YMax:
            print("FAIL open case overhangs rear PC shelf")
            ok = False
        else:
            print("PASS open case fits directly on small rear PC shelf")

    if "REAR / BACK / TRASEIRA" not in str(group.ServiceDirection):
        print("FAIL rear service direction not recorded")
        ok = False
    else:
        print("PASS service direction explicitly rear/back/traseira")

    if "NO PLAYFIELD OPENING" not in str(group.RoutineService):
        print("FAIL routine-service policy still requires playfield")
        ok = False
    else:
        print("PASS routine PC service keeps playfield closed")

    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL manufacturing block missing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - rear PC service FreeCAD packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

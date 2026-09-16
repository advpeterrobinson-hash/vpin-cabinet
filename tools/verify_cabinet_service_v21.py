#!/usr/bin/env python3
"""Headless FreeCAD verification for cabinet service/mobility v0.21."""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

REQUIRED = [
    "ClassicLegBracketFLV21",
    "ClassicLegBracketFRV21",
    "ClassicLegBracketRLV21",
    "ClassicLegBracketRRV21",
    "LegSpreaderFLV21",
    "LegSpreaderFRV21",
    "LegSpreaderRLV21",
    "LegSpreaderRRV21",
    "PCServiceSledV21",
    "PCServiceSledLiftGhostV21",
    "PCSledLocator1V21",
    "PCSledLocator2V21",
    "PCSledLocator3V21",
    "PCSledLocator4V21",
    "PCOpenChassisReferenceV21",
]

SUPERSEDED_VISIBLE = [
    "LegSideDoublerFLV20", "LegSideDoublerFRV20", "LegSideDoublerRLV20", "LegSideDoublerRRV20",
    "LegEndDoublerFLV20", "LegEndDoublerFRV20", "LegEndDoublerRLV20", "LegEndDoublerRRV20",
    "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
    "PCTrayServiceGhostV20", "PCSlideLeftKeepoutV20", "PCSlideRightKeepoutV20",
]


def main() -> None:
    doc = App.openDocument(MASTER)
    group = doc.getObject("CabinetServiceV21")
    if group is None:
        raise RuntimeError("CabinetServiceV21 group missing")

    ok = True
    print("CABINET SERVICE / MOBILITY v0.21 FREECAD VERIFY")
    print("=" * 78)
    for name in REQUIRED:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    tray = doc.getObject("PCServiceSledV21")
    ghost = doc.getObject("PCServiceSledLiftGhostV21")
    if tray and ghost:
        dz = ghost.Shape.BoundBox.ZMin - tray.Shape.BoundBox.ZMin
        if abs(dz - 250.0) > 0.2:
            print(f"FAIL PC vertical service lift {dz:.1f} mm")
            ok = False
        else:
            print("PASS PC sled service motion is vertical +250 mm, not forward")

    visible_old = []
    for name in SUPERSEDED_VISIBLE:
        obj = doc.getObject(name)
        if obj is not None:
            try:
                if obj.ViewObject.Visibility:
                    visible_old.append(name)
            except Exception:
                pass
    if visible_old:
        print("FAIL superseded v0.20 leg/wheel/drawer visuals remain visible", visible_old)
        ok = False
    else:
        print("PASS superseded bulky leg/wheel/forward-drawer visuals hidden")

    if "PINSKATES" not in str(group.MobilityMode).upper() or "NO CABINET CASTERS" not in str(group.MobilityMode).upper():
        print("FAIL PinSkates/no-caster mobility policy missing")
        ok = False
    else:
        print("PASS classic-leg + PinSkates mobility policy recorded")

    if "LARGE PLYWOOD DOUBLERS REMOVED" not in str(group.LegCornerPolicy).upper():
        print("FAIL compact leg-corner policy missing")
        ok = False
    else:
        print("PASS large plywood leg doublers removed")

    if "NO FORWARD/FRONT DRAWER TRAVEL" not in str(group.PCServicePolicy).upper():
        print("FAIL PC service-direction policy missing")
        ok = False
    else:
        print("PASS PC service is top lift-out, not front drawer")

    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL manufacturing block missing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - v0.21 service/mobility packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import os
import FreeCAD as App

ROOT=os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER=os.path.join(ROOT,"cad/master/vpin-master.FCStd")

REQUIRED=[
"ClosedSupportSeatLeftV19","ClosedSupportSeatRightV19",
"ClosedSupportDoublerLeftV19","ClosedSupportDoublerRightV19",
"SafetyStayDoublerLeftV19","SafetyStayDoublerRightV19",
"SafetyStayNutPlateLeftV19","SafetyStayNutPlateRightV19",
"GasStrutDoublerLeftV19","GasStrutDoublerRightV19",
"GasStrutNutPlateLeftV19","GasStrutNutPlateRightV19",
"LatchReceiverDoublerLeftV19","LatchReceiverDoublerRightV19"
]


def main():
    doc=App.openDocument(MASTER)
    group=doc.getObject("PlayfieldFixedAnchorsV19")
    if group is None:
        raise RuntimeError("PlayfieldFixedAnchorsV19 group missing")
    ok=True
    print("PLAYFIELD FIXED ANCHORS v0.19 FREECAD VERIFY")
    print("="*76)
    for name in REQUIRED:
        obj=doc.getObject(name)
        valid=obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok=ok and valid

    # Steel support seats must project inward far enough to overlap the cradle rails in X.
    for side,seat_name,rail_name in (
        ("LEFT","ClosedSupportSeatLeftV19","CradleSideRailLeftV18"),
        ("RIGHT","ClosedSupportSeatRightV19","CradleSideRailRightV18"),
    ):
        seat=doc.getObject(seat_name); rail=doc.getObject(rail_name)
        if seat and rail:
            sb=seat.Shape.BoundBox; rb=rail.Shape.BoundBox
            x_overlap=min(sb.XMax,rb.XMax)-max(sb.XMin,rb.XMin)
            if x_overlap < 10.0:
                print(f"FAIL {side} support seat/rail X overlap only {x_overlap:.1f} mm")
                ok=False
            else:
                print(f"PASS {side} support seat overlaps rail in X by {x_overlap:.1f} mm")

    if "TBD" not in str(group.StayAnchorStatus):
        print("FAIL stay hardware freeze block missing"); ok=False
    else:
        print("PASS stay pin/slot holes remain TBD")
    if "TBD" not in str(group.GasAnchorStatus):
        print("FAIL gas hardware freeze block missing"); ok=False
    else:
        print("PASS gas ball-stud geometry remains TBD")
    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL manufacturing block missing"); ok=False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - v0.19 fixed anchor packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Headless verification for v0.15 playfield pivot packaging."""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

EXPECTED = {
    "PlayfieldPivotPlateLeftV15",
    "PlayfieldPivotPlateRightV15",
    "PlayfieldPivotBackingLeftV15",
    "PlayfieldPivotBackingRightV15",
    "PlayfieldJournalLeftV15",
    "PlayfieldJournalRightV15",
    "UCFL202LeftKeepoutV15",
    "UCFL202RightKeepoutV15",
}


def main() -> None:
    doc = App.openDocument(MASTER)
    group = doc.getObject("PlayfieldPivotV15")
    if group is None:
        raise RuntimeError("PlayfieldPivotV15 group missing")

    names = {o.Name for o in group.Group}
    missing = EXPECTED - names
    if missing:
        raise RuntimeError(f"Missing v0.15 pivot objects: {sorted(missing)}")

    lp = doc.getObject("PlayfieldPivotPlateLeftV15")
    rp = doc.getObject("PlayfieldPivotPlateRightV15")
    if lp.Shape.isNull() or rp.Shape.isNull():
        raise RuntimeError("Pivot plate solid is null")

    if abs(lp.Shape.BoundBox.XLength - 6.0) > 0.05:
        raise RuntimeError(f"Left pivot plate thickness mismatch: {lp.Shape.BoundBox.XLength:.3f} mm")
    if abs(rp.Shape.BoundBox.XLength - 6.0) > 0.05:
        raise RuntimeError(f"Right pivot plate thickness mismatch: {rp.Shape.BoundBox.XLength:.3f} mm")

    lj = doc.getObject("PlayfieldJournalLeftV15")
    rj = doc.getObject("PlayfieldJournalRightV15")
    if lj.Shape.isNull() or rj.Shape.isNull():
        raise RuntimeError("Pivot journal solid is null")

    if "BLOCKED" not in group.BearingHoleStatus:
        raise RuntimeError("Bearing mounting holes must remain blocked until physical measurement")
    if "SAFETY STAYS" not in group.SafetyStatus:
        raise RuntimeError("Mechanical safety-stay policy missing")

    print("PLAYFIELD PIVOT v0.15 FREECAD VERIFY")
    print("=" * 68)
    print(f"Objects                  {len(group.Group)}")
    print(f"Left plate bbox          {lp.Shape.BoundBox.XLength:.1f} x {lp.Shape.BoundBox.YLength:.1f} x {lp.Shape.BoundBox.ZLength:.1f} mm")
    print(f"Right plate bbox         {rp.Shape.BoundBox.XLength:.1f} x {rp.Shape.BoundBox.YLength:.1f} x {rp.Shape.BoundBox.ZLength:.1f} mm")
    print(f"Bearing status           {group.BearingHoleStatus}")
    print("STATUS                   PASS - ENGINEERING PACKAGING ONLY")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

REQUIRED_NAMES = (
    "ActiveBuildV25",
    "CabinetStructureV20",
    "CabinetServiceV21",
    "CabinetRearCPUShelfV24",
    "PlayfieldMechanicsV18",
    "PlayfieldFixedAnchorsV19",
)

FORBIDDEN_LABEL_PREFIXES = (
    "LG OLED42C5 FIT CHECK",
    "PLAYFIELD SERVICE v0.4",
    "PLAYFIELD SERVICE v0.5",
    "PC SERVICE v0.22",
    "REAR PC SERVICE v0.23",
)

FORBIDDEN_NAMES = (
    "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
    "PCTrayStowedV20", "PCTrayServiceGhostV20",
    "PCServiceSledV21", "PCServiceSledLiftGhostV21",
)


def main() -> None:
    doc = App.openDocument(MASTER)
    ok = True
    print("ACTIVE MASTER v0.25 VERIFY")
    print("=" * 72)

    for name in REQUIRED_NAMES:
        exists = doc.getObject(name) is not None
        print(f"{'PASS' if exists else 'FAIL'} required {name}")
        ok = ok and exists

    for obj in doc.Objects:
        label = str(getattr(obj, "Label", ""))
        if any(label.startswith(p) for p in FORBIDDEN_LABEL_PREFIXES):
            print(f"FAIL obsolete group remains: {label}")
            ok = False

    for name in FORBIDDEN_NAMES:
        if doc.getObject(name) is not None:
            print(f"FAIL obsolete object remains: {name}")
            ok = False

    marker = doc.getObject("ActiveBuildV25")
    if marker and "CNC PRELOCATES" in str(marker.AssemblyGoal):
        print("PASS active assembly goal recorded")
    else:
        print("FAIL active assembly goal missing")
        ok = False

    print("STATUS", "PASS - cleaned active master" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

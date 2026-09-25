#!/usr/bin/env python3
from __future__ import annotations

import os
import traceback
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
ARCHIVE_NAME = "SupersededArchiveV25"

REQUIRED_NAMES = (
    "ActiveBuildV25",
    "CabinetStructureV20",
    "CabinetServiceV21",
    "CabinetRearCPUShelfV24",
    "PlayfieldMechanicsV18",
    "PlayfieldFixedAnchorsV19",
)

ARCHIVED_LABEL_PREFIXES = (
    "LG OLED42C5 FIT CHECK",
    "PLAYFIELD SERVICE v0.4",
    "PLAYFIELD SERVICE v0.5",
    "PC SERVICE v0.22",
    "REAR PC SERVICE v0.23",
)

ARCHIVED_NAMES = (
    "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
    "PCTrayStowedV20", "PCTrayServiceGhostV20",
    "PCServiceSledV21", "PCServiceSledLiftGhostV21",
)


def main() -> None:
    print("ACTIVE MASTER v0.25 VERIFY")
    print("=" * 72)
    try:
        doc = App.openDocument(MASTER)
    except Exception:
        traceback.print_exc()
        raise

    ok = True

    for name in REQUIRED_NAMES:
        exists = doc.getObject(name) is not None
        print(f"{'PASS' if exists else 'FAIL'} required {name}")
        ok = ok and exists

    archive = doc.getObject(ARCHIVE_NAME)
    archive_exists = archive is not None
    print(f"{'PASS' if archive_exists else 'FAIL'} superseded archive group present")
    ok = ok and archive_exists

    archive_names = set()
    if archive:
        archive_names = {obj.Name for obj in list(getattr(archive, 'Group', []) or [])}
        try:
            archive_hidden = archive.ViewObject.Visibility is False
        except Exception:
            archive_hidden = True
        print(f"{'PASS' if archive_hidden else 'FAIL'} superseded archive hidden")
        ok = ok and archive_hidden

    # Historical whole groups may still exist in the document for safety/history,
    # but they must live inside the single archive node rather than at top level.
    for obj in list(doc.Objects):
        try:
            label = str(obj.Label)
            name = str(obj.Name)
        except Exception:
            continue
        if any(label.startswith(p) for p in ARCHIVED_LABEL_PREFIXES):
            archived = name in archive_names
            print(f"{'PASS' if archived else 'FAIL'} archived historical group: {label}")
            ok = ok and archived

    for name in ARCHIVED_NAMES:
        obj = doc.getObject(name)
        if obj is None:
            # Some base builders may no longer generate a particular legacy object;
            # absence is also acceptable.
            print(f"PASS legacy object absent: {name}")
            continue
        archived = name in archive_names
        print(f"{'PASS' if archived else 'FAIL'} legacy object archived: {name}")
        ok = ok and archived

    # Ensure archived objects are not still direct children of the active cabinet groups.
    for active_name in ("CabinetStructureV20", "CabinetServiceV21"):
        active = doc.getObject(active_name)
        if not active:
            continue
        child_names = {obj.Name for obj in list(getattr(active, 'Group', []) or [])}
        conflicts = sorted(child_names.intersection(set(ARCHIVED_NAMES)))
        if conflicts:
            print(f"FAIL {active_name} still contains superseded children: {', '.join(conflicts)}")
            ok = False
        else:
            print(f"PASS {active_name} contains no superseded child geometry")

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

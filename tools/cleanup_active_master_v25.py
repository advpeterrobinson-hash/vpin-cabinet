#!/usr/bin/env python3
"""Present the generated FreeCAD master as one active product without risky graph surgery.

FreeCAD 1.1.3 on Homer proved sensitive to deleting/reparenting generated objects and
then reopening the FCStd. The active cleanup therefore does NOT delete or move
objects between groups. It only hides obsolete geometry, relabels historical review
groups, renames active groups, and adds an ACTIVE BUILD marker.

Git/config/scripts remain the engineering source of truth. A later release/export
step can generate a fresh manufacturing-only document once geometry is frozen.
"""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

ARCHIVE_LABEL_PREFIXES = (
    "LG OLED42C5 FIT CHECK",
    "PLAYFIELD SERVICE v0.4",
    "PLAYFIELD SERVICE v0.5",
    "PC SERVICE v0.22",
    "REAR PC SERVICE v0.23",
)

ARCHIVE_OBJECT_NAMES = {
    "LegSideDoublerFLV20", "LegSideDoublerFRV20", "LegSideDoublerRLV20", "LegSideDoublerRRV20",
    "LegEndDoublerFLV20", "LegEndDoublerFRV20", "LegEndDoublerRLV20", "LegEndDoublerRRV20",
    "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
    "LegBracketKeepoutFLV20", "LegBracketKeepoutFRV20", "LegBracketKeepoutRLV20", "LegBracketKeepoutRRV20",
    "PCSubrailLeftV20", "PCSubrailRightV20", "PCTrayStowedV20", "PCTrayServiceGhostV20",
    "PCSlideLeftKeepoutV20", "PCSlideRightKeepoutV20", "PCServiceEnvelopeV20",
    "PCServiceSledV21", "PCServiceSledLiftGhostV21",
    "PCSledLocator1V21", "PCSledLocator2V21", "PCSledLocator3V21", "PCSledLocator4V21",
    "PCOpenChassisReferenceV21",
}


def hide(obj) -> None:
    try:
        obj.ViewObject.Visibility = False
    except Exception:
        pass


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master: {MASTER}")

    print("ACTIVE MASTER PRESENTATION CLEANUP v0.25")
    print("=" * 76)
    doc = App.openDocument(MASTER)

    archived_groups = []
    # Snapshot stable names/labels first. Do not reparent or delete anything.
    for obj in list(doc.Objects):
        try:
            name = str(obj.Name)
            label = str(obj.Label)
        except Exception:
            continue
        if any(label.startswith(prefix) for prefix in ARCHIVE_LABEL_PREFIXES):
            live = doc.getObject(name)
            if live is None:
                continue
            hide(live)
            if not label.startswith("ARCHIVE | "):
                live.Label = f"ARCHIVE | {label}"
            archived_groups.append(label)

    archived_objects = []
    for name in sorted(ARCHIVE_OBJECT_NAMES):
        obj = doc.getObject(name)
        if obj is None:
            continue
        hide(obj)
        archived_objects.append(name)

    renames = {
        "CabinetStructureV20": "CABINET CNC BASE - JOINERY / GLASS / SSF (ACTIVE)",
        "CabinetServiceV21": "CLASSIC LEGS / PINSKATES (ACTIVE)",
        "CabinetRearCPUShelfV24": "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
        "PlayfieldMechanicsV18": "PLAYFIELD MECHANICS - CRADLE / PIVOT / DUAL SAFETY (ACTIVE)",
        "PlayfieldFixedAnchorsV19": "PLAYFIELD FIXED ANCHORS - SIDEWALL LOAD PATHS (ACTIVE)",
    }
    for name, label in renames.items():
        obj = doc.getObject(name)
        if obj:
            obj.Label = label

    marker = doc.getObject("ActiveBuildV25")
    if marker is None:
        marker = doc.addObject("App::FeaturePython", "ActiveBuildV25")
    marker.Label = "ACTIVE BUILD v0.25 - SIMPLE CNC KIT"

    props = {
        "AssemblyGoal": "CNC PRELOCATES STRUCTURAL HOLES; HOME BUILDER DRY-FITS / GLUES / BOLTS / FINISHES / INSTALLS ELECTRONICS",
        "PCService": "REAR BACKDOOR + CASE-SIZED BOARD + TWO FULL-EXTENSION SLIDES",
        "Mobility": "CLASSIC LEGS + LEVELERS; EXTERNAL REMOVABLE PINSKATES",
        "ManufacturingStatus": "NOT CNC-READY UNTIL MEASURE_BEFORE_CNC HARDWARE IS FROZEN",
        "CleanupPolicy": "NON-DESTRUCTIVE: LEGACY GEOMETRY HIDDEN/LABELED ONLY; NO DELETE OR REPARENT IN WORKING FCSTD",
    }
    for prop, value in props.items():
        if prop not in marker.PropertiesList:
            marker.addProperty("App::PropertyString", prop, "Current")
        setattr(marker, prop, value)

    doc.recompute()
    doc.save()

    required = (
        "CabinetStructureV20", "CabinetServiceV21", "CabinetRearCPUShelfV24",
        "PlayfieldMechanicsV18", "PlayfieldFixedAnchorsV19", "ActiveBuildV25",
    )
    missing = [name for name in required if doc.getObject(name) is None]
    if missing:
        raise RuntimeError("Missing active objects after presentation cleanup: " + ", ".join(missing))

    print(f"Hidden legacy groups        {len(archived_groups)}")
    for label in archived_groups:
        print(f"  - {label}")
    print(f"Hidden legacy child objects {len(archived_objects)}")
    print("Graph mutation              NONE (no delete/reparent)")
    print("Retained active systems     cabinet / legs+PinSkates / rear CPU / playfield mechanics")
    print("STATUS                      CLEAN ACTIVE PRESENTATION")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

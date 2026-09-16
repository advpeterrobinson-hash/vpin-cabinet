#!/usr/bin/env python3
"""Organize the generated FreeCAD master around the active build.

Important: this cleanup is intentionally NON-DESTRUCTIVE.

Earlier revisions recursively deleted superseded groups/objects.  FreeCAD 1.1.3
can retain internal references to those objects while saving the document, which
can leave the next open/verify pass with stale/deleted proxies.  The current
strategy instead moves superseded review geometry into one collapsed archive
group and hides it.  Git remains the long-term history, while the working tree
presents one compact archive node instead of many obsolete design branches.
"""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

ARCHIVE_NAME = "SupersededArchiveV25"
ARCHIVE_LABEL = "ARCHIVE - SUPERSEDED GEOMETRY (NOT ACTIVE BUILD)"

# Entire historical review groups that should no longer appear at top level.
ARCHIVE_LABEL_PREFIXES = (
    "LG OLED42C5 FIT CHECK",
    "PLAYFIELD SERVICE v0.4",
    "PLAYFIELD SERVICE v0.5",
    "PC SERVICE v0.22",
    "REAR PC SERVICE v0.23",
)

# Historical child objects embedded in still-useful v0.20/v0.21 groups.
ARCHIVE_OBJECT_NAMES = {
    # v0.20 bulky leg furniture / wheel concepts
    "LegSideDoublerFLV20", "LegSideDoublerFRV20", "LegSideDoublerRLV20", "LegSideDoublerRRV20",
    "LegEndDoublerFLV20", "LegEndDoublerFRV20", "LegEndDoublerRLV20", "LegEndDoublerRRV20",
    "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
    "LegBracketKeepoutFLV20", "LegBracketKeepoutFRV20", "LegBracketKeepoutRLV20", "LegBracketKeepoutRRV20",
    # v0.20 long PC drawer
    "PCSubrailLeftV20", "PCSubrailRightV20", "PCTrayStowedV20", "PCTrayServiceGhostV20",
    "PCSlideLeftKeepoutV20", "PCSlideRightKeepoutV20", "PCServiceEnvelopeV20",
    # v0.21 lift-out PC sled
    "PCServiceSledV21", "PCServiceSledLiftGhostV21",
    "PCSledLocator1V21", "PCSledLocator2V21", "PCSledLocator3V21", "PCSledLocator4V21",
    "PCOpenChassisReferenceV21",
}


def detach_from_current_groups(obj) -> None:
    """Detach obj from existing group-like parents without deleting it."""
    for parent in list(getattr(obj, "InList", []) or []):
        if parent.Name == ARCHIVE_NAME:
            continue
        remove = getattr(parent, "removeObject", None)
        if callable(remove):
            try:
                remove(obj)
            except Exception:
                pass


def hide(obj) -> None:
    try:
        obj.ViewObject.Visibility = False
    except Exception:
        pass


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master: {MASTER}")

    print("ACTIVE MASTER CLEANUP v0.25")
    print("=" * 76)
    doc = App.openDocument(MASTER)

    archive = doc.getObject(ARCHIVE_NAME)
    if archive is None:
        archive = doc.addObject("App::DocumentObjectGroup", ARCHIVE_NAME)
    archive.Label = ARCHIVE_LABEL

    # Capture names/labels first. Never retain proxies across operations that can
    # change group ownership; FreeCAD proxies can become invalid after mutation.
    whole_groups = []
    for obj in list(doc.Objects):
        try:
            name = str(obj.Name)
            label = str(obj.Label)
        except Exception:
            continue
        if name == ARCHIVE_NAME:
            continue
        if any(label.startswith(prefix) for prefix in ARCHIVE_LABEL_PREFIXES):
            whole_groups.append((name, label))

    archived_groups = []
    for name, label in whole_groups:
        obj = doc.getObject(name)
        if obj is None:
            continue
        detach_from_current_groups(obj)
        try:
            archive.addObject(obj)
        except Exception as exc:
            raise RuntimeError(f"Could not archive group {name}: {exc}") from exc
        hide(obj)
        archived_groups.append(label)

    archived_objects = []
    for name in sorted(ARCHIVE_OBJECT_NAMES):
        obj = doc.getObject(name)
        if obj is None:
            continue
        detach_from_current_groups(obj)
        try:
            archive.addObject(obj)
        except Exception as exc:
            raise RuntimeError(f"Could not archive object {name}: {exc}") from exc
        hide(obj)
        archived_objects.append(name)

    hide(archive)

    # Retained groups communicate current purpose instead of version-history noise.
    renames = {
        "CabinetStructureV20": "CABINET CNC BASE - JOINERY / GLASS / SSF (ACTIVE)",
        "CabinetServiceV21": "CLASSIC LEGS / PINSKATES (ACTIVE)",
        "CabinetRearCPUShelfV24": "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
    }
    for name, label in renames.items():
        obj = doc.getObject(name)
        if obj:
            obj.Label = label

    marker = doc.getObject("ActiveBuildV25")
    if marker is None:
        marker = doc.addObject("App::FeaturePython", "ActiveBuildV25")
    marker.Label = "ACTIVE BUILD v0.25 - SIMPLE CNC KIT"

    if "AssemblyGoal" not in marker.PropertiesList:
        marker.addProperty("App::PropertyString", "AssemblyGoal", "Current")
    marker.AssemblyGoal = "CNC PRELOCATES STRUCTURAL HOLES; HOME BUILDER DRY-FITS / GLUES / BOLTS / FINISHES / INSTALLS ELECTRONICS"

    if "PCService" not in marker.PropertiesList:
        marker.addProperty("App::PropertyString", "PCService", "Current")
    marker.PCService = "REAR BACKDOOR + CASE-SIZED BOARD + TWO FULL-EXTENSION SLIDES"

    if "Mobility" not in marker.PropertiesList:
        marker.addProperty("App::PropertyString", "Mobility", "Current")
    marker.Mobility = "CLASSIC LEGS + LEVELERS; EXTERNAL REMOVABLE PINSKATES"

    if "ManufacturingStatus" not in marker.PropertiesList:
        marker.addProperty("App::PropertyString", "ManufacturingStatus", "Current")
    marker.ManufacturingStatus = "NOT CNC-READY UNTIL MEASURE_BEFORE_CNC HARDWARE IS FROZEN"

    doc.recompute()
    doc.save()

    print(f"Archived obsolete groups  {len(archived_groups)}")
    for label in archived_groups:
        print(f"  - {label}")
    print(f"Archived obsolete objects {len(archived_objects)}")
    print("Archive node              ARCHIVE - SUPERSEDED GEOMETRY (NOT ACTIVE BUILD)")
    print("Retained active systems   cabinet CNC base / classic legs+PinSkates / rear CPU / playfield mechanics")
    print("STATUS                    CLEANED ACTIVE MASTER")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prune superseded review geometry from the generated FreeCAD master.

This does not rewrite Git history. It removes historical comparison groups/objects
from the generated working master so the owner/builder sees only active geometry.

FreeCAD object proxies become invalid immediately after ``removeObject``.  Never
continue inspecting a stale ``doc.Objects`` snapshot after recursive deletion;
collect stable internal names first, then delete by name.
"""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")

# Entire groups whose concepts are superseded by current mechanics/service design.
DROP_LABEL_PREFIXES = (
    "LG OLED42C5 FIT CHECK",
    "PLAYFIELD SERVICE v0.4",
    "PLAYFIELD SERVICE v0.5",
    "PC SERVICE v0.22",
    "REAR PC SERVICE v0.23",
)

# Superseded child objects embedded in still-useful v0.20/v0.21 review groups.
DROP_OBJECT_NAMES = {
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


def safe_name(obj) -> str | None:
    """Return an object's internal name without propagating stale-proxy errors."""
    try:
        return str(obj.Name)
    except Exception:
        return None


def safe_label(obj) -> str:
    """Return an object's visible label without propagating stale-proxy errors."""
    try:
        return str(obj.Label)
    except Exception:
        return ""


def remove_object_recursive(doc, name: str) -> None:
    """Remove a live object and its grouped children using stable object names."""
    obj = doc.getObject(name)
    if obj is None:
        return

    child_names: list[str] = []
    try:
        children = list(getattr(obj, "Group", []) or [])
    except Exception:
        children = []

    for child in children:
        child_name = safe_name(child)
        if child_name:
            child_names.append(child_name)

    for child_name in child_names:
        remove_object_recursive(doc, child_name)

    if doc.getObject(name) is not None:
        doc.removeObject(name)


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master: {MASTER}")
    doc = App.openDocument(MASTER)

    removed_groups: list[str] = []
    removed_objects: list[str] = []

    # IMPORTANT: collect stable names BEFORE deleting anything. FreeCAD's Python
    # proxies are invalid as soon as their underlying object is deleted, so a
    # snapshot of doc.Objects cannot safely be inspected during recursive removal.
    group_targets: list[tuple[str, str]] = []
    for obj in list(doc.Objects):
        name = safe_name(obj)
        if not name:
            continue
        label = safe_label(obj)
        if any(label.startswith(prefix) for prefix in DROP_LABEL_PREFIXES):
            group_targets.append((name, label))

    for name, label in group_targets:
        if doc.getObject(name) is None:
            continue
        removed_groups.append(label)
        remove_object_recursive(doc, name)

    # Drop superseded children from retained cabinet groups. Names that were
    # already removed as children of a deleted group are harmlessly skipped.
    for name in sorted(DROP_OBJECT_NAMES):
        if doc.getObject(name) is not None:
            removed_objects.append(name)
            remove_object_recursive(doc, name)

    # Rename retained groups so the tree communicates current purpose instead of historical experiments.
    renames = {
        "CabinetStructureV20": "CABINET CNC BASE - JOINERY / GLASS / SSF (ACTIVE)",
        "CabinetServiceV21": "CLASSIC LEGS / PINSKATES (ACTIVE)",
        "CabinetRearCPUShelfV24": "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
    }
    for name, label in renames.items():
        obj = doc.getObject(name)
        if obj is not None:
            obj.Label = label

    # Add one compact current-state marker to the tree.
    marker = doc.getObject("ActiveBuildV25")
    if marker is not None:
        doc.removeObject("ActiveBuildV25")
    marker = doc.addObject("App::FeaturePython", "ActiveBuildV25")
    marker.Label = "ACTIVE BUILD v0.25 - SIMPLE CNC KIT"
    marker.addProperty("App::PropertyString", "AssemblyGoal", "Current")
    marker.AssemblyGoal = "CNC PRELOCATES STRUCTURAL HOLES; HOME BUILDER DRY-FITS / GLUES / BOLTS / FINISHES / INSTALLS ELECTRONICS"
    marker.addProperty("App::PropertyString", "PCService", "Current")
    marker.PCService = "REAR BACKDOOR + CASE-SIZED BOARD + TWO FULL-EXTENSION SLIDES"
    marker.addProperty("App::PropertyString", "Mobility", "Current")
    marker.Mobility = "CLASSIC LEGS + LEVELERS; EXTERNAL REMOVABLE PINSKATES"
    marker.addProperty("App::PropertyString", "ManufacturingStatus", "Current")
    marker.ManufacturingStatus = "NOT CNC-READY UNTIL MEASURE_BEFORE_CNC HARDWARE IS FROZEN"

    doc.recompute()
    doc.save()

    print("ACTIVE MASTER CLEANUP v0.25")
    print("=" * 76)
    print(f"Removed obsolete groups   {len(removed_groups)}")
    for label in removed_groups:
        print(f"  - {label}")
    print(f"Removed obsolete objects  {len(removed_objects)}")
    print("Retained active systems   cabinet CNC base / classic legs+PinSkates / rear CPU / playfield mechanics")
    print("STATUS                    CLEANED ACTIVE MASTER")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

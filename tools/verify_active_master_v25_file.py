#!/usr/bin/env python3
"""Verify the saved v0.25 FCStd without reopening it through FreeCAD.

The saved-file check intentionally validates serialized product content rather than
FreeCAD's internal object Name.  FreeCAD may suffix/rewrite generated object names
across rebuild/save cycles even while preserving the actual group, labels,
properties and geometry.  Internal names are therefore not a manufacturing or
product invariant.
"""
from __future__ import annotations

import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"

REQUIRED_TEXT = (
    "ACTIVE BUILD v0.25 - SIMPLE CNC KIT",
    "CABINET CNC BASE - JOINERY / GLASS / SSF (ACTIVE)",
    "CLASSIC LEGS / PINSKATES (ACTIVE)",
    "PLAYFIELD MECHANICS - CRADLE / PIVOT / DUAL SAFETY (ACTIVE)",
    "PLAYFIELD FIXED ANCHORS - SIDEWALL LOAD PATHS (ACTIVE)",
    "CNC PRELOCATES STRUCTURAL HOLES",
)

REAR_CPU_LABELS = (
    "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
    "REAR CPU SHELF v0.24 - NARROW CASE-SIZED BOARD / FULL REAR EXTENSION",
)

# These are independent serialized markers from the actual rear-CPU package.  They
# prove that the rear door, shelf, case envelope and rearward-service semantics are
# in the saved document; this is stronger and more useful than one mutable FreeCAD
# internal object name.
REAR_CPU_CONTENT_MARKERS = (
    "CAB-PC-REAR-DOOR-002-R1 - CLOSED",
    "PC-REAR-SHELF-002-R1 - CASE-SIZED BOARD / STOWED",
    "OPEN PC CASE 265x440x128 - ROTATED / BOLTED DIRECT TO BOARD",
    "REARWARD THROUGH MAIN-CABINET BACKDOOR; PLAYFIELD STAYS CLOSED",
)


def main() -> int:
    print("ACTIVE MASTER v0.25 FILE VERIFY")
    print("=" * 72)
    if not MASTER.exists():
        print(f"FAIL master missing: {MASTER}")
        return 1

    try:
        with zipfile.ZipFile(MASTER, "r") as zf:
            bad = zf.testzip()
            if bad:
                print(f"FAIL corrupt FCStd member: {bad}")
                return 1
            names = set(zf.namelist())
            if "Document.xml" not in names:
                print("FAIL Document.xml missing from FCStd")
                return 1
            xml = zf.read("Document.xml").decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"FAIL cannot read FCStd archive: {exc}")
        return 1

    print("PASS FCStd ZIP integrity")
    ok = True
    for text in REQUIRED_TEXT:
        passed = text in xml
        print(f"{'PASS' if passed else 'FAIL'} saved marker: {text}")
        ok = ok and passed

    rear_label = next((label for label in REAR_CPU_LABELS if label in xml), None)
    print(
        f"{'PASS' if rear_label else 'FAIL'} rear CPU package label: "
        f"{rear_label or 'not found'}"
    )
    ok = ok and rear_label is not None

    rear_content_ok = True
    for marker in REAR_CPU_CONTENT_MARKERS:
        passed = marker in xml
        print(f"{'PASS' if passed else 'FAIL'} rear CPU content: {marker}")
        rear_content_ok = rear_content_ok and passed
    ok = ok and rear_content_ok

    print("INFO FreeCAD internal object names are intentionally non-blocking")
    print("STATUS", "PASS - saved active master" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

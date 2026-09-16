#!/usr/bin/env python3
"""Verify the saved v0.25 FCStd without reopening it through FreeCAD.

This intentionally avoids a second FreeCAD parse on Homer. The cleanup routine
already validates active objects in-memory before save. Here we only confirm that
the saved FCStd is a readable archive and contains the active marker/labels.
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
    "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
    "PLAYFIELD MECHANICS - CRADLE / PIVOT / DUAL SAFETY (ACTIVE)",
    "PLAYFIELD FIXED ANCHORS - SIDEWALL LOAD PATHS (ACTIVE)",
    "CNC PRELOCATES STRUCTURAL HOLES",
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

    print("STATUS", "PASS - saved active master" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

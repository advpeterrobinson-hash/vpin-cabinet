#!/usr/bin/env python3
"""Verify that v0.4 objects were persisted into the FCStd archive.

Uses only the Python standard library, so this catches cases where FreeCADCmd
loads a script but never actually calls the builder's main() function.
"""

from __future__ import annotations

import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"

REQUIRED = [
    "PlayfieldServiceV04",
    "OLED42C5ClosedV04",
    "OLED42C5OpenGhostV04",
    "PlayfieldHingeAxisV04",
    "CradleEnvelopeClosedV04",
    "CradleEnvelopeOpenGhostV04",
    "GasStrutLeftClosedV04",
    "GasStrutLeftOpenV04",
    "GasStrutRightClosedV04",
    "GasStrutRightOpenV04",
]


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    raise SystemExit(1)


if not MASTER.exists():
    fail(f"missing master: {MASTER}")

try:
    with zipfile.ZipFile(MASTER, "r") as zf:
        names = set(zf.namelist())
        if "Document.xml" not in names:
            fail("FCStd archive has no Document.xml")
        docxml = zf.read("Document.xml").decode("utf-8", errors="replace")
except zipfile.BadZipFile:
    fail("master is not a valid FCStd/ZIP archive")

missing = [name for name in REQUIRED if name not in docxml]
if missing:
    fail("v0.4 objects not persisted: " + ", ".join(missing))

print(f"PASS  FCStd persisted v0.4 object set: {len(REQUIRED)} markers")
print(f"PASS  Master archive: {MASTER}")
sys.exit(0)

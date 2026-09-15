#!/usr/bin/env python3
"""Headless verification for the 580 mm cabinet platform and service-I/O model."""
from __future__ import annotations

import os
import sys

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    sys.exit(1)


def q(value) -> float:
    return float(value.Value if hasattr(value, "Value") else value)


if not os.path.exists(MASTER):
    fail(f"missing master: {MASTER}")

doc = App.openDocument(MASTER)
sheet = doc.getObject("Parameters")
if sheet is None:
    fail("MASTER PARAMETERS spreadsheet missing")

# Use spreadsheet string values where possible because aliases may be Quantity
# objects depending on FreeCAD version.
def cell_float(cell: str) -> float:
    txt = sheet.get(cell).strip().split()[0]
    return float(txt)

outer = cell_float("B2")
inner = cell_float("B4")
if abs(outer - 580.0) > 0.01:
    fail(f"CabOuterWidth is {outer:.3f} mm, expected 580.000 mm")
if abs(inner - 544.0) > 0.05:
    fail(f"CabInnerWidth is {inner:.3f} mm, expected 544.000 mm")

left = doc.getObject("CabinetLeftPad")
right = doc.getObject("CabinetRightPad")
front = doc.getObject("CabinetFront")
rear = doc.getObject("CabinetRear")
if any(obj is None for obj in (left, right, front, rear)):
    fail("one or more shell objects missing")

if abs(right.Shape.BoundBox.XMin - 562.0) > 0.2:
    fail(f"right side XMin {right.Shape.BoundBox.XMin:.2f} mm, expected about 562 mm")
if abs(front.Shape.BoundBox.XLength - 544.0) > 0.2:
    fail(f"front panel width {front.Shape.BoundBox.XLength:.2f} mm, expected about 544 mm")
if abs(rear.Shape.BoundBox.XLength - 544.0) > 0.2:
    fail(f"rear panel width {rear.Shape.BoundBox.XLength:.2f} mm, expected about 544 mm")

# Existing expression-driven C5 fit mockup should have recentered automatically.
oled = doc.getObject("OLED42C5ClearanceEnvelope")
if oled is not None:
    bb = oled.Shape.BoundBox
    if abs(bb.XLength - 542.0) > 0.2:
        fail(f"C5 clearance envelope width {bb.XLength:.2f} mm")
    if abs(bb.XMin - 19.0) > 0.3:
        fail(f"C5 clearance envelope XMin {bb.XMin:.2f} mm, expected about 19 mm")

io = doc.getObject("ServiceIOV09")
if io is None:
    fail("ServiceIOV09 group missing")
required = [
    "RearPowerFasciaV09",
    "RearPowerWindowGhostV09",
    "RearServiceFasciaV09",
    "RearServiceWindowGhostV09",
    "RearServiceConnectorCarrierV09",
    "RearMainsEnclosureGhostV09",
]
for name in required:
    obj = doc.getObject(name)
    if obj is None:
        fail(f"missing service-I/O object: {name}")
    if obj.Shape.isNull() or not obj.Shape.isValid():
        fail(f"invalid service-I/O shape: {name}")

if abs(q(io.PowerSignalFasciaGap) - 85.0) > 0.1:
    fail(f"unexpected power/signal fascia gap {q(io.PowerSignalFasciaGap):.2f} mm")

# Window ghosts must remain inside the 580 mm exterior width.
for name in ("RearPowerWindowGhostV09", "RearServiceWindowGhostV09"):
    bb = doc.getObject(name).Shape.BoundBox
    if bb.XMin < -0.01 or bb.XMax > outer + 0.01:
        fail(f"{name} exceeds cabinet width: X {bb.XMin:.1f}..{bb.XMax:.1f}")

print("PASS  master platform width: 580.0 mm")
print("PASS  nominal inner width: 544.0 mm")
print("PASS  expression-driven shell resized/recentered")
if oled is not None:
    print("PASS  C5 clearance envelope fits without side pocket")
print(f"PASS  service-I/O packaging objects present/valid: {len(required)}")
print(f"PASS  rear power/signal fascia gap: {q(io.PowerSignalFasciaGap):.1f} mm")
print("STATUS  v0.9 platform headless geometry verification passed")

App.closeDocument(doc.Name)

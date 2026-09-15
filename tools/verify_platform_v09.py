#!/usr/bin/env python3
"""Headless verification for the current cabinet platform and service-I/O model.

Historical filename retained for compatibility; expected dimensions come from
config/design.json so the check follows the active 600 mm baseline.
"""
from __future__ import annotations

import json
import os
import sys

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
DESIGN = os.path.join(ROOT, "config/design.json")


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    sys.exit(1)


def q(value) -> float:
    return float(value.Value if hasattr(value, "Value") else value)


if not os.path.exists(MASTER):
    fail(f"missing master: {MASTER}")
if not os.path.exists(DESIGN):
    fail(f"missing design config: {DESIGN}")

with open(DESIGN, "r", encoding="utf-8") as fh:
    design = json.load(fh)
cab = design["cabinet"]
outer_expected = float(cab["outer_width_mm"])
wood = float(cab["main_wood_nominal_mm"])
inner_expected = outer_expected - 2.0 * wood

doc = App.openDocument(MASTER)
sheet = doc.getObject("Parameters")
if sheet is None:
    fail("MASTER PARAMETERS spreadsheet missing")


def cell_float(cell: str) -> float:
    txt = sheet.get(cell).strip().split()[0]
    return float(txt)


outer = cell_float("B2")
inner = cell_float("B4")
if abs(outer - outer_expected) > 0.01:
    fail(f"CabOuterWidth is {outer:.3f} mm, expected {outer_expected:.3f} mm")
if abs(inner - inner_expected) > 0.05:
    fail(f"CabInnerWidth is {inner:.3f} mm, expected {inner_expected:.3f} mm")

left = doc.getObject("CabinetLeftPad")
right = doc.getObject("CabinetRightPad")
front = doc.getObject("CabinetFront")
rear = doc.getObject("CabinetRear")
if any(obj is None for obj in (left, right, front, rear)):
    fail("one or more shell objects missing")

expected_right_xmin = outer_expected - wood
if abs(right.Shape.BoundBox.XMin - expected_right_xmin) > 0.2:
    fail(f"right side XMin {right.Shape.BoundBox.XMin:.2f} mm, expected about {expected_right_xmin:.2f} mm")
if abs(front.Shape.BoundBox.XLength - inner_expected) > 0.2:
    fail(f"front panel width {front.Shape.BoundBox.XLength:.2f} mm, expected about {inner_expected:.2f} mm")
if abs(rear.Shape.BoundBox.XLength - inner_expected) > 0.2:
    fail(f"rear panel width {rear.Shape.BoundBox.XLength:.2f} mm, expected about {inner_expected:.2f} mm")

# Legacy LG reference envelope remains a regression geometry only.
oled = doc.getObject("OLED42C5ClearanceEnvelope")
if oled is not None:
    bb = oled.Shape.BoundBox
    if abs(bb.XLength - 542.0) > 0.2:
        fail(f"legacy LG clearance envelope width {bb.XLength:.2f} mm")
    expected_xmin = (outer_expected - bb.XLength) / 2.0
    if abs(bb.XMin - expected_xmin) > 0.3:
        fail(f"legacy LG clearance envelope XMin {bb.XMin:.2f} mm, expected about {expected_xmin:.2f} mm")

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

if q(io.PowerSignalFasciaGap) < 75.0:
    fail(f"unexpectedly small power/signal fascia gap {q(io.PowerSignalFasciaGap):.2f} mm")

for name in ("RearPowerWindowGhostV09", "RearServiceWindowGhostV09"):
    bb = doc.getObject(name).Shape.BoundBox
    if bb.XMin < -0.01 or bb.XMax > outer + 0.01:
        fail(f"{name} exceeds cabinet width: X {bb.XMin:.1f}..{bb.XMax:.1f}")

print(f"PASS  master platform width: {outer_expected:.1f} mm")
print(f"PASS  nominal inner width: {inner_expected:.1f} mm")
print("PASS  expression-driven shell resized/recentered")
if oled is not None:
    print("PASS  legacy LG reference envelope remains centered")
print(f"PASS  service-I/O packaging objects present/valid: {len(required)}")
print(f"PASS  rear power/signal fascia gap: {q(io.PowerSignalFasciaGap):.1f} mm")
print("STATUS  current platform headless geometry verification passed")

App.closeDocument(doc.Name)

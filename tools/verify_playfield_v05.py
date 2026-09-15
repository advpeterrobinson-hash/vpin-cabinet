#!/usr/bin/env python3
"""Headless verification for playfield service model v0.5."""

from __future__ import annotations

import json
import os
import sys

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CONFIG = os.path.join(ROOT, "config/playfield_v05.json")


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    sys.exit(1)


if not os.path.exists(MASTER):
    fail(f"missing master: {MASTER}")

with open(CONFIG, "r", encoding="utf-8") as fh:
    cfg = json.load(fh)

doc = App.openDocument(MASTER)
group = doc.getObject("PlayfieldServiceV05")
if group is None:
    fail("PlayfieldServiceV05 group was not generated")

required = [
    "BackboxKeepoutV05",
    "HingeReinforcementEnvelopeV05",
    "VESAAdjustmentZoneV05",
    "SafetyPropOpenV05",
    "SafetyPropFixedPinV05",
    "SafetyPropMovingPinV05",
]

for deg in cfg["sweep"]["angles_deg"]:
    required.append(f"OLED42C5Sweep{int(deg):03d}V05")

for name in required:
    obj = doc.getObject(name)
    if obj is None:
        fail(f"missing generated object: {name}")
    try:
        if obj.Shape.isNull():
            fail(f"null shape: {name}")
        if not obj.Shape.isValid():
            fail(f"invalid shape: {name}")
    except Exception as exc:
        fail(f"cannot validate shape {name}: {exc}")

keepout = doc.getObject("BackboxKeepoutV05").Shape
tol = float(cfg["sweep"]["collision_volume_tolerance_mm3"])
collisions = []
min_y_margin = float("inf")
for deg in cfg["sweep"]["angles_deg"]:
    obj = doc.getObject(f"OLED42C5Sweep{int(deg):03d}V05")
    vol = obj.Shape.common(keepout).Volume
    if vol > tol:
        collisions.append((deg, vol))
    min_y_margin = min(min_y_margin, keepout.BoundBox.YMin - obj.Shape.BoundBox.YMax)

if collisions:
    fail(
        "sweep collides with provisional backbox keepout: "
        + ", ".join(f"{d}deg={v:.1f}mm^3" for d, v in collisions)
    )

if min_y_margin < 20.0:
    fail(f"minimum provisional backbox Y margin below 20 mm: {min_y_margin:.1f} mm")

prop_len = float(group.SafetyPropLength.Value)
if not (350.0 <= prop_len <= 800.0):
    fail(f"safety prop packaging length unexpected: {prop_len:.1f} mm")

if cfg["manufacturing_ready"] is not False:
    fail("v0.5 configuration must remain non-manufacturing-ready")

if "NOT FOR MANUFACTURING" not in str(group.Status):
    fail(f"unexpected status: {group.Status}")

print("PASS  PlayfieldServiceV05 group exists")
print(f"PASS  generated objects present/valid: {len(required)}")
print(f"PASS  OLED sweep states clear provisional backbox keepout: {len(cfg['sweep']['angles_deg'])}")
print(f"PASS  minimum provisional backbox Y margin: {min_y_margin:.1f} mm")
print(f"PASS  positive safety-prop packaging envelope present: {prop_len:.1f} mm")
print("PASS  v0.5 remains explicitly non-manufacturing-ready")
print("STATUS  v0.5 headless geometry verification passed")

App.closeDocument(doc.Name)

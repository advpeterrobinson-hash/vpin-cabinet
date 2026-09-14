#!/usr/bin/env python3
"""Headless verification for the generated playfield service model v0.4."""

from __future__ import annotations

import os
import sys

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")
    sys.exit(1)


if not os.path.exists(MASTER):
    fail(f"missing master: {MASTER}")

doc = App.openDocument(MASTER)

group = doc.getObject("PlayfieldServiceV04")
if group is None:
    fail("PlayfieldServiceV04 group was not generated")

required = [
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

for name in required:
    obj = doc.getObject(name)
    if obj is None:
        fail(f"missing generated object: {name}")
    try:
        shape = obj.Shape
        if shape.isNull():
            fail(f"null shape: {name}")
        if not shape.isValid():
            fail(f"invalid shape: {name}")
    except Exception as exc:
        fail(f"cannot validate shape {name}: {exc}")

closed = doc.getObject("OLED42C5ClosedV04").Shape.BoundBox
opened = doc.getObject("OLED42C5OpenGhostV04").Shape.BoundBox

if opened.ZMax <= closed.ZMax:
    fail(
        f"service ghost did not rise: closed ZMax={closed.ZMax:.1f}, "
        f"open ZMax={opened.ZMax:.1f}"
    )

if float(group.RelativeOpenAngle) < 60.0:
    fail(f"service angle unexpectedly small: {group.RelativeOpenAngle}")

print("PASS  PlayfieldServiceV04 group exists")
print(f"PASS  generated objects present/valid: {len(required)}")
print(
    f"PASS  service ghost rises: closed ZMax={closed.ZMax:.1f} mm, "
    f"open ZMax={opened.ZMax:.1f} mm"
)
print(f"PASS  service angle: {float(group.RelativeOpenAngle):.1f} deg")
print("STATUS  v0.4 headless geometry verification passed")

App.closeDocument(doc.Name)

#!/usr/bin/env python3
"""Migrate the FreeCAD master to the 580 mm cabinet platform baseline.

This stage updates the live spreadsheet parameters only. Existing expression-
driven shell/OLED-fit geometry should recompute from those parameters. Frozen
packaging groups (playfield service, etc.) are rebuilt separately by the runner.
"""
from __future__ import annotations

import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")


def set_param(sheet, row: int, alias: str, value: str, description: str) -> None:
    sheet.set(f"A{row}", alias)
    sheet.set(f"B{row}", value)
    sheet.set(f"C{row}", description)
    try:
        sheet.setAlias(f"B{row}", alias)
    except Exception:
        pass


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    doc = App.openDocument(MASTER)
    sheet = doc.getObject("Parameters")
    if sheet is None:
        raise RuntimeError("MASTER PARAMETERS spreadsheet not found")

    # Primary platform selection.
    sheet.set("B2", "580.00 mm")
    sheet.set("C2", "Selected future-proof cabinet outer width (v0.7/v0.9)")

    # Preserve historical/reference width explicitly for traceability.
    set_param(sheet, 40, "CabOuterWidthReference", "558.80 mm", "Williams WPC reference outer width")

    # Future replacement envelope for the playfield bay.
    set_param(sheet, 41, "FuturePlayfieldWidth", "560.00 mm", "Future 42-inch-class display cross-cabinet chassis envelope")
    set_param(sheet, 42, "FuturePlayfieldLength", "950.00 mm", "Future display front-to-rear envelope")
    set_param(sheet, 43, "FuturePlayfieldDepth", "55.00 mm", "Future display maximum thickness/bulge envelope")
    set_param(sheet, 44, "FuturePlayfieldClearance", "2.00 mm", "Per-side installation clearance for future display envelope")
    set_param(sheet, 45, "BackboxTargetWidth", "780.00 mm", "Future-proof backbox outer-width target")

    # Current C5 no longer needs a side pocket at 580 mm; keep the legacy
    # formula but clamp the engineering readout to zero using a new parameter.
    set_param(sheet, 46, "OLEDRequiredPocketDepth", "=max(0 mm;(B35-B4)/2)", "Actual required side pocket at selected cabinet width")

    doc.recompute()

    # Rename shell label to reflect selected platform without destroying the
    # original parametric objects or scripts.
    shell = doc.getObject("Shell")
    if shell:
        shell.Label = "CABINET SHELL v0.9 - 580 mm CNC PLATFORM"

    doc.recompute()
    doc.save()

    print("CABINET PLATFORM v0.9 MIGRATION COMPLETE")
    print("=" * 68)
    print("Cabinet outer width      ", sheet.get("B2"))
    print("Cabinet inner width      ", sheet.get("B4"))
    print("Future display width     ", sheet.get("B41"))
    print("Future display clearance ", sheet.get("B44"))
    try:
        print("C5 required side pocket  ", sheet.get("B46"))
    except Exception:
        pass
    print("STATUS                    ENGINEERING - NOT FOR CNC PRODUCTION")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

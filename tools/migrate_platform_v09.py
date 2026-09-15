#!/usr/bin/env python3
"""Migrate the FreeCAD master to the 580 mm cabinet platform baseline.

This stage updates the live spreadsheet parameters only. Existing expression-
driven shell/fit geometry should recompute from those parameters. Frozen
packaging groups are rebuilt separately by the runners.
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

    sheet.set("B2", "580.00 mm")
    sheet.set("C2", "Selected future-proof cabinet outer width")

    set_param(sheet, 40, "CabOuterWidthReference", "558.80 mm", "Williams WPC reference outer width")

    # v0.16 display-agnostic permanent envelope. This is intentionally sized
    # around compact 42/43-inch 4K gaming displays sold in Brazil rather than
    # around one LG chassis.
    set_param(sheet, 41, "FuturePlayfieldWidth", "560.00 mm", "Target max physical display cross-cabinet chassis width")
    set_param(sheet, 42, "FuturePlayfieldLength", "970.00 mm", "Target max physical display front-to-rear chassis length")
    set_param(sheet, 43, "FuturePlayfieldDepth", "55.00 mm", "Target max display thickness/bulge envelope")
    set_param(sheet, 44, "FuturePlayfieldClearance", "2.00 mm", "Per-side cross-cabinet installation clearance")
    set_param(sheet, 45, "BackboxTargetWidth", "780.00 mm", "Future-proof backbox outer-width target")
    set_param(sheet, 47, "FuturePlayfieldBayLength", "980.00 mm", "Clear longitudinal service bay for target display length")
    set_param(sheet, 48, "FuturePlayfieldMaxCavity", "564.00 mm", "Maximum clear cross-cavity at 8 mm minimum remaining side skin")

    # Legacy LG C-series fit readout remains for regression/reference only.
    set_param(sheet, 46, "OLEDRequiredPocketDepth", "=max(0 mm;(B35-B4)/2)", "Legacy LG reference required side pocket at selected cabinet width")

    doc.recompute()
    shell = doc.getObject("Shell")
    if shell:
        shell.Label = "CABINET SHELL - 580 mm / 42-43 in DISPLAY ENVELOPE"

    doc.recompute()
    doc.save()

    print("CABINET PLATFORM / DISPLAY ENVELOPE MIGRATION COMPLETE")
    print("=" * 72)
    print("Cabinet outer width       ", sheet.get("B2"))
    print("Cabinet inner width       ", sheet.get("B4"))
    print("Target display cross      ", sheet.get("B41"))
    print("Target display length     ", sheet.get("B42"))
    print("Clear bay length          ", sheet.get("B47"))
    print("Max cross cavity          ", sheet.get("B48"))
    print("STATUS                     ENGINEERING - NOT FOR CNC PRODUCTION")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

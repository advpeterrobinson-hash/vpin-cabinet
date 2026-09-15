#!/usr/bin/env python3
"""Migrate the FreeCAD master to the current cabinet/display baseline.

Historical filename retained for compatibility with existing runners. The values
are read from config/design.json so later width decisions cannot silently regress
the FreeCAD master to an obsolete platform width.
"""
from __future__ import annotations

import json
import os
import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
DESIGN = os.path.join(ROOT, "config/design.json")


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
    if not os.path.exists(DESIGN):
        raise RuntimeError(f"Missing design config: {DESIGN}")

    with open(DESIGN, "r", encoding="utf-8") as fh:
        design = json.load(fh)

    cab = design["cabinet"]
    env = cab["future_playfield_service_envelope_mm"]
    outer = float(cab["outer_width_mm"])
    wood = float(cab["main_wood_nominal_mm"])
    inner = outer - 2.0 * wood
    target_cross = float(env["target_display_cross_width"])
    target_len = float(env["target_display_length"])
    target_depth = float(env["depth"])
    clearance = float(env["cross_clearance_each_side"])
    bay_len = float(env["clear_bay_length"])
    full_clear = float(env["full_thickness_clear_cross_width"])
    max_routed = float(env["maximum_routed_cross_width_at_minimum_skin"])
    backbox_w = float(design["backglass"]["target_backbox_outer_width_mm"])

    doc = App.openDocument(MASTER)
    sheet = doc.getObject("Parameters")
    if sheet is None:
        raise RuntimeError("MASTER PARAMETERS spreadsheet not found")

    sheet.set("B2", f"{outer:.2f} mm")
    sheet.set("C2", "Owner-approved current cabinet outer width from config/design.json")

    set_param(sheet, 40, "CabOuterWidthReference", f"{float(cab['reference_outer_width_mm']):.2f} mm", "Williams WPC reference outer width")
    set_param(sheet, 41, "FuturePlayfieldWidth", f"{target_cross:.2f} mm", "Target max physical display cross-cabinet chassis width")
    set_param(sheet, 42, "FuturePlayfieldLength", f"{target_len:.2f} mm", "Target max physical display front-to-rear chassis length")
    set_param(sheet, 43, "FuturePlayfieldDepth", f"{target_depth:.2f} mm", "Target max display thickness/bulge envelope")
    set_param(sheet, 44, "FuturePlayfieldClearance", f"{clearance:.2f} mm", "Per-side cross-cabinet installation clearance")
    set_param(sheet, 45, "BackboxTargetWidth", f"{backbox_w:.2f} mm", "Future-proof backbox outer-width target")
    set_param(sheet, 47, "FuturePlayfieldBayLength", f"{bay_len:.2f} mm", "Clear longitudinal service bay for target display length")
    set_param(sheet, 48, "FuturePlayfieldMaxCavity", f"{max_routed:.2f} mm", "Exceptional future routed cross-cavity at minimum side skin")
    set_param(sheet, 49, "FuturePlayfieldFullClearWidth", f"{full_clear:.2f} mm", "Normal full-thickness clear cross-cabinet width")

    # Legacy LG C-series fit readout remains for regression/reference only.
    set_param(sheet, 46, "OLEDRequiredPocketDepth", "=max(0 mm;(B35-B4)/2)", "Legacy LG reference required side pocket at selected cabinet width")

    doc.recompute()
    shell = doc.getObject("Shell")
    if shell:
        shell.Label = f"CABINET SHELL - {outer:.0f} mm / 42-43 in DISPLAY ENVELOPE"

    doc.recompute()
    doc.save()

    print("CABINET PLATFORM / DISPLAY ENVELOPE MIGRATION COMPLETE")
    print("=" * 72)
    print(f"Cabinet outer width        {outer:.2f} mm")
    print(f"Cabinet inner width        {inner:.2f} mm")
    print(f"Target display cross       {target_cross:.2f} mm")
    print(f"Target display length      {target_len:.2f} mm")
    print(f"Full-thickness clear width {full_clear:.2f} mm")
    print(f"Exceptional routed cavity  {max_routed:.2f} mm")
    print(f"Clear bay length           {bay_len:.2f} mm")
    print("STATUS                     ENGINEERING - NOT FOR CNC PRODUCTION")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

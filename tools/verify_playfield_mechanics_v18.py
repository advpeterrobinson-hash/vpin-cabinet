#!/usr/bin/env python3
"""Headless FreeCAD verification for integrated playfield mechanics v0.18."""
from __future__ import annotations

import json
import os

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/playfield_mechanics_v18.json")


def close(a: float, b: float, tol: float = 0.25) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")
    with open(CFG, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)

    cab = cfg["cabinet"]
    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_side_thickness_mm"])

    doc = App.openDocument(MASTER)
    group = doc.getObject("PlayfieldMechanicsV18")
    if group is None:
        raise RuntimeError("PlayfieldMechanicsV18 group missing")

    required = [
        "GenericPlayfieldDisplayClosedV18",
        "GenericPlayfieldDisplayOpenGhostV18",
        "CradleSideRailLeftV18",
        "CradleSideRailRightV18",
        "CradleCrossmember1V18",
        "CradleCrossmember2V18",
        "CradleCrossmember3V18",
        "CradlePivotDoublerLeftV18",
        "CradlePivotDoublerRightV18",
        "CradleRearBeamV18",
        "VesaAdapterEnvelopeV18",
        "PivotPlateLeftV18",
        "PivotPlateRightV18",
        "PivotJournalLeftV18",
        "PivotJournalRightV18",
        "UCFL202LeftKeepoutV18",
        "UCFL202RightKeepoutV18",
        "BearingBackingLeftV18",
        "BearingBackingRightV18",
        "CradleOpenGhostV18",
        "GasStrutClosedLeftV18",
        "GasStrutClosedRightV18",
        "GasStrutOpenLeftGhostV18",
        "GasStrutOpenRightGhostV18",
        "SafetyStayOpenLeftV18",
        "SafetyStayOpenRightV18",
        "ClosedSupportPad1V18",
        "ClosedSupportPad2V18",
        "ClosedLatchKeepout1V18",
        "ClosedLatchKeepout2V18",
        "MovingHarnessKeepoutV18",
    ]

    ok = True
    print("PLAYFIELD MECHANICS v0.18 FREECAD VERIFY")
    print("=" * 76)
    for name in required:
        obj = doc.getObject(name)
        valid = obj is not None and not obj.Shape.isNull() and obj.Shape.isValid()
        print(f"{'PASS' if valid else 'FAIL'} {name}")
        ok = ok and valid

    display = doc.getObject("GenericPlayfieldDisplayClosedV18")
    open_display = doc.getObject("GenericPlayfieldDisplayOpenGhostV18")
    open_cradle = doc.getObject("CradleOpenGhostV18")
    if display:
        bb = display.Shape.BoundBox
        expected_w = float(cfg["display_envelope"]["cross_width_mm"])
        if not close(bb.XLength, expected_w):
            print(f"FAIL generic display X width {bb.XLength:.2f} mm, expected {expected_w:.2f}")
            ok = False
        else:
            print(f"PASS generic display cross-width {bb.XLength:.1f} mm")
        if bb.XMin < wood - 0.05 or bb.XMax > outer - wood + 0.05:
            print(f"FAIL closed display violates full-thickness sidewall bay: X={bb.XMin:.2f}..{bb.XMax:.2f}")
            ok = False
        else:
            print(f"PASS closed display stays between full-thickness sidewalls: X={bb.XMin:.1f}..{bb.XMax:.1f}")

        front = doc.getObject("CabinetFront")
        if front is None:
            print("FAIL CabinetFront missing for front-clearance check")
            ok = False
        else:
            overlap = display.Shape.common(front.Shape).Volume
            clearance = bb.YMin - front.Shape.BoundBox.YMax
            minimum = float(cfg["display_envelope"]["minimum_clearance_behind_front_panel_mm"])
            if overlap > 1.0:
                print(f"FAIL closed display intersects front panel: {overlap:.1f} mm3")
                ok = False
            elif clearance + 0.1 < minimum:
                print(f"FAIL closed display/front-panel clearance {clearance:.1f} mm < {minimum:.1f} mm")
                ok = False
            else:
                print(f"PASS closed display clears front panel by {clearance:.1f} mm")

    # The 70-degree service display and full moving cradle must clear the actual
    # v0.14 backbox structural solids. A tiny numerical/tangent volume is ignored.
    backbox_names = ["BackboxFloorV14", "BackboxLeftSideV14", "BackboxRightSideV14", "BackboxTopV14"]
    if open_display and open_cradle:
        collisions = []
        for name in backbox_names:
            obj = doc.getObject(name)
            if obj is None:
                print(f"FAIL required backbox structure missing for collision check: {name}")
                ok = False
                continue
            for moving in (open_display, open_cradle):
                volume = moving.Shape.common(obj.Shape).Volume
                if volume > 1.0:
                    collisions.append((moving.Name, name, volume))
        if collisions:
            print("FAIL service geometry collides with backbox: " + ", ".join(f"{m}/{n}={v:.1f}mm3" for m, n, v in collisions))
            ok = False
        else:
            print("PASS 70-degree display + cradle service ghosts clear actual backbox shell")

        floor = doc.getObject("BackboxFloorV14")
        if floor:
            front_y = floor.Shape.BoundBox.YMin
            hinge_y = float(group.HingeY.Value)
            margin = front_y - hinge_y
            print(f"INFO hinge axis to backbox-front Y margin: {margin:.1f} mm")

    if not close(float(group.FullThicknessDisplayBay.Value), 564.0, 0.05):
        print(f"FAIL full-thickness display bay {group.FullThicknessDisplayBay.Value}")
        ok = False
    else:
        print("PASS 600 mm body retains 564 mm full-thickness display bay")

    if "MODEL-AGNOSTIC" not in str(group.DisplayPolicy):
        print("FAIL model-agnostic display policy missing")
        ok = False
    else:
        print("PASS model-agnostic display policy recorded")

    if "TBD AFTER ACTUAL MASS+CG" not in str(group.GasStrutStatus):
        print("FAIL gas-strut deferral policy missing")
        ok = False
    else:
        print("PASS gas-strut force/mounts remain deferred")

    if "DUAL POSITIVE SAFETY STAYS" not in str(group.SafetyStatus):
        print("FAIL dual safety-stay policy missing")
        ok = False
    else:
        print("PASS dual positive safety stays + closed latches recorded")

    if "BLOCKED" not in str(group.BearingHoleStatus):
        print("FAIL UCFL202 mounting-hole manufacturing block missing")
        ok = False
    else:
        print("PASS UCFL202 holes remain blocked pending physical sample")

    if "NOT FOR MANUFACTURING" not in str(group.Status):
        print("FAIL package must remain non-manufacturing")
        ok = False
    else:
        print("PASS manufacturing block retained")

    print("STATUS", "PASS - v0.18 integrated mechanics packaging" if ok else "FAIL")
    App.closeDocument(doc.Name)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build v0.21 classic-leg / PinSkates / lift-out-PC service overlay.

This overlay intentionally supersedes the bulky v0.20 leg doublers, integrated
wheel keepouts and forward-travel PC drawer while preserving v0.20 joinery,
SSF, glass, siderail and lockdown packaging.
"""
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_service_v21.json")
V20 = os.path.join(ROOT, "config/cabinet_structure_v20.json")


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def add_shape(doc, group, name, label, shape, transparency=0, part_id=None):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    if part_id:
        obj.addProperty("App::PropertyString", "PartID", "Build Package")
        obj.PartID = part_id
    try:
        obj.ViewObject.Transparency = transparency
    except Exception:
        pass
    return obj


def main(doc=None, active_only=False) -> None:
    owns_document = doc is None
    if owns_document and not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    cfg = load(CFG)
    v20 = load(V20)
    mob = cfg["mobility"]
    leg = cfg["leg_corners"]
    pc = cfg["pc_service"]

    cab = v20["cabinet"]
    outer = float(cab["outer_width_mm"])
    length = float(cab["side_length_mm"])
    wood = float(cab["nominal_wood_mm"])

    if owns_document:
        doc = App.openDocument(MASTER)

    old = doc.getObject("CabinetServiceV21")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "CabinetServiceV21")
    group.Label = "CLASSIC LEGS / EXTERNAL PINSKATES" if active_only else "HISTORICAL SERVICE V21"

    # v0.20 remains the joinery/glass/SSF baseline, but these particular v0.20
    # visuals are explicitly superseded by the owner's v0.21 direction.
    hide_names = [
        "LegSideDoublerFLV20", "LegSideDoublerFRV20", "LegSideDoublerRLV20", "LegSideDoublerRRV20",
        "LegEndDoublerFLV20", "LegEndDoublerFRV20", "LegEndDoublerRLV20", "LegEndDoublerRRV20",
        "LegBracketKeepoutFLV20", "LegBracketKeepoutFRV20", "LegBracketKeepoutRLV20", "LegBracketKeepoutRRV20",
        "WheelKeepoutFLV20", "WheelKeepoutFRV20", "WheelKeepoutRLV20", "WheelKeepoutRRV20",
        "PCSubrailLeftV20", "PCSubrailRightV20",
        "PCTrayStowedV20", "PCTrayServiceGhostV20",
        "PCSlideLeftKeepoutV20", "PCSlideRightKeepoutV20", "PCServiceEnvelopeV20",
    ]
    for name in hide_names:
        obj = doc.getObject(name)
        if obj:
            try:
                obj.ViewObject.Visibility = False
            except Exception:
                pass

    # Compact classic pinball leg bracket envelopes. Each corner is one fused
    # L-shaped steel package: one flange on the side wall and one on the end wall.
    bt = float(leg["steel_bracket_nominal_thickness_mm"])
    bh = float(leg["bracket_height_mm"])
    bf = float(leg["bracket_flange_each_wall_mm"])
    z0 = wood

    def corner_bracket(suffix: str, left: bool, front: bool):
        sx = wood if left else outer - wood - bt
        sy = wood if front else length - wood - bf
        side = Part.makeBox(bt, bf, bh, App.Vector(sx, sy, z0))

        ex = wood if left else outer - wood - bf
        ey = wood if front else length - wood - bt
        end = Part.makeBox(bf, bt, bh, App.Vector(ex, ey, z0))
        shape = side.fuse(end)
        return add_shape(
            doc, group,
            f"ClassicLegBracket{suffix}V21",
            f"CLASSIC LEG BRACKET {suffix} - 3 mm STEEL / HOLES TBD",
            shape, 18,
            f"LEG-BRKT-{suffix}-R1",
        )

    corner_bracket("FL", True, True)
    corner_bracket("FR", False, True)
    corner_bracket("RL", True, False)
    corner_bracket("RR", False, False)

    # Small spreader/backing envelopes only around the eventual bolt region.
    # No exact hole positions are created until the real bracket/leg set is measured.
    sp_t = float(leg["local_spreader_plate_thickness_mm"])
    sp_w, sp_h = [float(v) for v in leg["local_spreader_plate_envelope_mm"]]
    side_y_front = wood + 15.0
    side_y_rear = length - wood - sp_w - 15.0
    spreaders = [
        ("FL", App.Vector(wood + bt, side_y_front, z0 + 15.0)),
        ("FR", App.Vector(outer - wood - bt - sp_t, side_y_front, z0 + 15.0)),
        ("RL", App.Vector(wood + bt, side_y_rear, z0 + 15.0)),
        ("RR", App.Vector(outer - wood - bt - sp_t, side_y_rear, z0 + 15.0)),
    ]
    for suffix, base in spreaders:
        shape = Part.makeBox(sp_t, sp_w, sp_h, base)
        add_shape(doc, group, f"LegSpreader{suffix}V21", f"LEG BOLT SPREADER {suffix} - 3 mm STEEL / PATTERN TBD", shape, 38)

    if not active_only:
        # PC lift-out sled. It stays fully inside the cabinet and lifts vertically
        # through the playfield opening; there is no forward/front drawer travel.
        tw = float(pc["tray_width_x_mm"])
        td = float(pc["tray_depth_y_mm"])
        tt = float(pc["tray_thickness_z_mm"])
        tx = float(pc["tray_x_mm"])
        ty = float(pc["tray_y_mm"])
        tz = float(pc["tray_z_mm"])
        lift = float(pc["lift_service_height_mm"])

        tray = Part.makeBox(tw, td, tt, App.Vector(tx, ty, tz))
        add_shape(doc, group, "PCServiceSledV21", "PC-SLED-001-R1 - LIFT-OUT SERVICE TRAY", tray, 18, "PC-SLED-001-R1")

        ghost = tray.copy()
        ghost.translate(App.Vector(0, 0, lift))
        add_shape(doc, group, "PCServiceSledLiftGhostV21", "PC SLED - +250 mm VERTICAL SERVICE GHOST", ghost, 85)

        # Four compact locator/retainer pedestals rise from the bottom structure to
        # the sled. Final M6/quarter-turn hardware is deliberately not modeled.
        bottom_top_z = float(v20["cnc_joinery"]["bottom_panel_bottom_z_mm"]) + float(v20["cnc_joinery"]["bottom_panel_thickness_mm"])
        ped_h = tz - bottom_top_z
        ped = 40.0
        px = [tx + 18.0, tx + tw - ped - 18.0]
        py = [ty + 18.0, ty + td - ped - 18.0]
        idx = 0
        for x in px:
            for y in py:
                idx += 1
                shape = Part.makeBox(ped, ped, ped_h, App.Vector(x, y, bottom_top_z))
                add_shape(doc, group, f"PCSledLocator{idx}V21", f"PC SLED LOCATOR / CAPTIVE RETAINER {idx} - HARDWARE TBD", shape, 32)

        # Chassis envelope centered on the tray for visual fit only.
        cw, cd, ch = [float(v) for v in pc["open_chassis_reference_mm"]]
        cx = tx + (tw - cw) / 2.0
        cy = ty + (td - cd) / 2.0
        chassis = Part.makeBox(cw, cd, ch, App.Vector(cx, cy, tz + tt))
        add_shape(doc, group, "PCOpenChassisReferenceV21", "OPEN ATX CHASSIS REFERENCE 440x265x128", chassis, 82)

    group.addProperty("App::PropertyString", "MobilityMode", "Engineering")
    group.MobilityMode = "CLASSIC PINBALL LEGS + EXTERNAL REMOVABLE PINSKATES; NO CABINET CASTERS"
    group.addProperty("App::PropertyString", "LegCornerPolicy", "Engineering")
    group.LegCornerPolicy = "COMPACT STEEL BRACKET; LARGE PLYWOOD DOUBLERS REMOVED; HOLES TBD AFTER REAL HARDWARE"
    group.addProperty("App::PropertyString", "PCServicePolicy", "Engineering")
    group.PCServicePolicy = "REAR CPU PACKAGE V24" if active_only else "HISTORICAL LIFT-OUT SLED"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    if owns_document:
        doc.save()

    print("CABINET SERVICE / MOBILITY v0.21 GENERATED")
    print("=" * 76)
    print("Mobility                  classic legs + external removable PinSkates")
    print("Integrated casters        NONE")
    print(f"Leg bracket envelope      {bf:.0f} x {bf:.0f} x {bh:.0f} mm / {bt:.1f} mm steel")
    if not active_only:
        print(f"PC lift-out sled          {tw:.0f} x {td:.0f} x {tt:.0f} mm at Y {ty:.0f}..{ty+td:.0f}")
    if not active_only:
        print(f"PC vertical service lift  {lift:.0f} mm")
    print("STATUS                    ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    if owns_document:
        App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

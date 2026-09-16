#!/usr/bin/env python3
"""Build v0.14 structure skeleton and WPC hinge packaging in FreeCAD.

This stage deliberately creates packaging/reference solids only. It does NOT cut
hinge bracket holes, lock-bolt Y locations, cable passports, or fan holes into
production panels. Exact WPC bracket hole patterns are frozen only after actual
hardware is purchased/measured.
"""
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/structure_geometry_v14.json")


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


def main(doc=None) -> None:
    owns_document = doc is None
    if owns_document and not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    cfg = load(CFG)
    cab = cfg["main_cabinet"]
    bb = cfg["backbox"]
    hinge = cfg["wpc_hinges"]
    lock = cfg["upright_locking"]

    cab_w = float(cab["outer_width_mm"])
    cab_len = float(cab["side_length_mm"])
    rear_h = float(cab["rear_height_mm"])
    wood = float(cab["wood_mm"])
    inner_w = cab_w - 2.0 * wood

    shelf = cab["rear_shelf"]
    shelf_depth = float(shelf["depth_mm"])
    shelf_t = float(shelf["thickness_mm"])
    shelf_top = float(shelf["top_z_mm"])
    shelf_y = cab_len - shelf_depth

    bb_w = float(bb["outer_width_mm"])
    bb_d = float(bb["outer_depth_mm"])
    bb_h = float(bb["outer_height_mm"])
    bb_wood = float(bb["wood_mm"])
    bb_x = (cab_w - bb_w) / 2.0
    bb_y = cab_len - bb_d
    bb_z = float(bb["floor_bottom_z_mm"])

    if owns_document:
        doc = App.openDocument(MASTER)

    old = doc.getObject("StructureV14")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "StructureV14")
    group.Label = "STRUCTURE v0.14 - SHELF / BACKBOX / WPC HINGE PACKAGE"

    # Main rear support shelf. Top aligns with the current rear-height datum.
    shelf_shape = Part.makeBox(
        inner_w,
        shelf_depth,
        shelf_t,
        App.Vector(wood, shelf_y, shelf_top - shelf_t),
    )
    add_shape(
        doc, group, "RearShelfV14",
        "CAB-REAR-SHELF-001-R1 - BACKBOX SUPPORT SHELF",
        shelf_shape, 20, "CAB-REAR-SHELF-001-R1"
    )

    # Backbox floor and shell envelope. Rear face is flush with cabinet rear.
    floor_shape = Part.makeBox(bb_w, bb_d, bb_wood, App.Vector(bb_x, bb_y, bb_z))
    add_shape(
        doc, group, "BackboxFloorV14",
        "BB-FLOOR-001-R1 - BACKBOX FLOOR / SHELF INTERFACE",
        floor_shape, 25, "BB-FLOOR-001-R1"
    )

    side_h = bb_h
    left_side = Part.makeBox(bb_wood, bb_d, side_h, App.Vector(bb_x, bb_y, bb_z))
    right_side = Part.makeBox(
        bb_wood, bb_d, side_h,
        App.Vector(bb_x + bb_w - bb_wood, bb_y, bb_z)
    )
    top = Part.makeBox(
        bb_w, bb_d, bb_wood,
        App.Vector(bb_x, bb_y, bb_z + bb_h - bb_wood)
    )
    add_shape(doc, group, "BackboxLeftSideV14", "BB-SIDE-001L-R1", left_side, 72, "BB-SIDE-001L-R1")
    add_shape(doc, group, "BackboxRightSideV14", "BB-SIDE-001R-R1", right_side, 72, "BB-SIDE-001R-R1")
    add_shape(doc, group, "BackboxTopV14", "BB-TOP-001-R1", top, 72, "BB-TOP-001-R1")

    # Keyed rear service-door frame. The opening is centered in the backbox.
    door = bb["service_door"]
    door_w = float(door["opening_width_mm"])
    door_h = float(door["opening_height_mm"])
    door_t = float(door["door_thickness_mm"])
    door_x = bb_x + (bb_w - door_w) / 2.0
    door_z = bb_z + float(door["lower_clearance_above_floor_mm"])
    rear_panel_y = cab_len - bb_wood

    left_frame_w = door_x - bb_x
    right_frame_x = door_x + door_w
    right_frame_w = (bb_x + bb_w) - right_frame_x
    lower_frame_h = door_z - bb_z
    upper_frame_z = door_z + door_h
    upper_frame_h = (bb_z + bb_h) - upper_frame_z

    if left_frame_w <= 0 or right_frame_w <= 0 or upper_frame_h <= 0:
        raise RuntimeError("Backbox service-door frame geometry is invalid")

    frame_shapes = (
        ("BackboxRearFrameLeftV14", "BB-REAR-FRAME-L-R1", Part.makeBox(left_frame_w, bb_wood, bb_h, App.Vector(bb_x, rear_panel_y, bb_z))),
        ("BackboxRearFrameRightV14", "BB-REAR-FRAME-R-R1", Part.makeBox(right_frame_w, bb_wood, bb_h, App.Vector(right_frame_x, rear_panel_y, bb_z))),
        ("BackboxRearFrameBottomV14", "BB-REAR-FRAME-B-R1", Part.makeBox(door_w, bb_wood, lower_frame_h, App.Vector(door_x, rear_panel_y, bb_z))),
        ("BackboxRearFrameTopV14", "BB-REAR-FRAME-T-R1", Part.makeBox(door_w, bb_wood, upper_frame_h, App.Vector(door_x, rear_panel_y, upper_frame_z))),
    )
    for name, pid, shape in frame_shapes:
        add_shape(doc, group, name, f"{pid} - FIXED REAR STRUCTURE", shape, 45, pid)

    door_shape = Part.makeBox(
        door_w, door_t, door_h,
        App.Vector(door_x, cab_len, door_z),
    )
    add_shape(
        doc, group, "BackboxServiceDoorV14",
        "BB-DOOR-001-R1 - KEYED GASKETED SERVICE DOOR",
        door_shape, 35, "BB-DOOR-001-R1"
    )

    # Internal adjustable monitor rail-cage packaging. Rails terminate below the
    # dedicated upper fan zone; exact brackets remain a later local-sourcing step.
    rails = bb["display_rail_cage"]
    rail_x = float(rails["vertical_profile_mm"][0])
    rail_y = float(rails["vertical_profile_mm"][1])
    rail_spacing = float(rails["rail_spacing_center_to_center_mm"])
    rail_rear_offset = float(rails["rear_offset_from_inner_face_mm"])
    center_x = cab_w / 2.0
    rail_bottom = bb_z + 45.0
    rail_top = upper_frame_z - 20.0
    rail_h = rail_top - rail_bottom
    rail_y0 = cab_len - bb_wood - rail_rear_offset - rail_y
    for side, cx in (("L", center_x - rail_spacing / 2.0), ("R", center_x + rail_spacing / 2.0)):
        shape = Part.makeBox(rail_x, rail_y, rail_h, App.Vector(cx - rail_x / 2.0, rail_y0, rail_bottom))
        add_shape(
            doc, group, f"BackglassRail{side}V14",
            f"BACKGLASS ADJUSTMENT RAIL {side} - 20x40 PACKAGING",
            shape, 55
        )

    # WPC pivot axis is based on the established cabinet datum. Actual bracket
    # outline/hole pattern is deliberately NOT modeled as manufacturing truth.
    pivot_y = cab_len - float(hinge["pivot_from_rear_mm"])
    pivot_z = float(hinge["pivot_from_bottom_mm"])
    pivot_r = float(hinge["pivot_hole_diameter_mm"]) / 2.0

    axis = Part.makeCylinder(
        2.0,
        bb_w + 20.0,
        App.Vector(bb_x - 10.0, pivot_y, pivot_z),
        App.Vector(1, 0, 0),
    )
    add_shape(doc, group, "BackboxPivotAxisV14", "WPC BACKBOX COMMON PIVOT AXIS", axis, 35)

    left_pivot = Part.makeCylinder(pivot_r, wood, App.Vector(0.0, pivot_y, pivot_z), App.Vector(1, 0, 0))
    right_pivot = Part.makeCylinder(pivot_r, wood, App.Vector(cab_w - wood, pivot_y, pivot_z), App.Vector(1, 0, 0))
    add_shape(doc, group, "LeftPivotHoleGhostV14", "02-4352 / 4322-01139-12B LEFT PIVOT - CUT GHOST", left_pivot, 82)
    add_shape(doc, group, "RightPivotHoleGhostV14", "02-4352 / 4322-01139-12B RIGHT PIVOT - CUT GHOST", right_pivot, 82)

    ky = float(hinge["bracket_keepout_y_mm"])
    kz = float(hinge["bracket_keepout_z_mm"])
    kt = float(hinge["bracket_keepout_thickness_mm"])
    keepout_y0 = pivot_y - ky / 2.0
    keepout_z0 = pivot_z - 25.0
    left_keepout = Part.makeBox(kt, ky, kz, App.Vector(-kt, keepout_y0, keepout_z0))
    right_keepout = Part.makeBox(kt, ky, kz, App.Vector(cab_w, keepout_y0, keepout_z0))
    add_shape(doc, group, "WpcHingeLeftEnvelopeV14", "01-9011-L HINGE KEEP-OUT - NOT BRACKET TOOLPATH", left_keepout, 80)
    add_shape(doc, group, "WpcHingeRightEnvelopeV14", "01-9011-R HINGE KEEP-OUT - NOT BRACKET TOOLPATH", right_keepout, 80)

    # Upright lock X datums only. Y position is intentionally not invented.
    lock_off = float(lock["x_offset_from_centerline_mm"])
    for name, x in (("Left", center_x - lock_off), ("Right", center_x + lock_off)):
        marker = Part.makeBox(2.0, shelf_depth, 3.0, App.Vector(x - 1.0, shelf_y, shelf_top + bb_wood + 2.0))
        add_shape(doc, group, f"LockAxisX{name}V14", f"UPRIGHT LOCK {name.upper()} - X DATUM ONLY / Y TBD", marker, 55)

    # Upper rear fan opening ghosts. These are packaging envelopes only; fan
    # purchase remains in the later electronics batch unless needed as a fit sample.
    fan = cfg["fan_packaging"]
    fan_r = float(fan["fan_diameter_mm"]) / 2.0
    fan_z = bb_z + bb_h - 95.0
    for idx, cx in enumerate((center_x - 145.0, center_x + 145.0), start=1):
        ghost = Part.makeCylinder(
            fan_r,
            bb_wood + 10.0,
            App.Vector(cx, cab_len - bb_wood - 5.0, fan_z),
            App.Vector(0, 1, 0),
        )
        add_shape(doc, group, f"BackboxFanGhost{idx}V14", f"120 mm FAN {idx} - OPENING GHOST", ghost, 85)

    group.addProperty("App::PropertyString", "HingeFamily", "Build Package")
    group.HingeFamily = "01-9011-L/R + 02-4352 + 4322-01139-12B"
    group.addProperty("App::PropertyString", "HingeHolePatternStatus", "Build Package")
    group.HingeHolePatternStatus = "TBD AFTER PURCHASE/MEASUREMENT - KEEP-OUT ONLY"
    group.addProperty("App::PropertyString", "StructureGate", "Build Package")
    group.StructureGate = "WOOD + HINGES + LEGS + DISPLAYS + PC DRAWER BEFORE ELECTRONICS"
    group.addProperty("App::PropertyString", "Status", "Build Package")
    group.Status = "ENGINEERING PACKAGING - NOT FOR CNC PRODUCTION"

    doc.recompute()
    if owns_document:
        doc.save()

    print("STRUCTURE v0.14 PACKAGING GENERATED")
    print("=" * 72)
    print(f"Rear shelf top           {shelf_top:.1f} mm")
    print(f"Backbox envelope         {bb_w:.1f} x {bb_d:.1f} x {bb_h:.1f} mm")
    print(f"Backbox global X         {bb_x:.1f} .. {bb_x + bb_w:.1f} mm")
    print(f"WPC pivot Y/Z            {pivot_y:.1f} / {pivot_z:.1f} mm")
    print("Hinge hardware           01-9011-L/R, 02-4352, 4322-01139-12B")
    print("Exact hinge hole pattern TBD after physical hardware measurement")
    print("STATUS                   ENGINEERING PACKAGING - NOT FOR CNC PRODUCTION")

    if owns_document:
        App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

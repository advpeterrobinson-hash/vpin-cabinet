#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_rear_pc_service_v23.json")
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


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    cfg = load(CFG)
    v20 = load(V20)
    door = cfg["rear_service_door"]
    pc = cfg["pc_slide"]
    case = cfg["open_pc_case_reference"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    length = float(cab["side_length_mm"])
    wood = float(cab["nominal_wood_mm"])
    rear_h = float(cab["rear_height_mm"])

    doc = App.openDocument(MASTER)

    old = doc.getObject("CabinetRearPCServiceV23")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "CabinetRearPCServiceV23")
    group.Label = "REAR PC SERVICE v0.23 - BACKDOOR / REARWARD PULL-OUT PC"

    # Supersede the incorrect center-directed v0.22 PC-service visuals only.
    v22 = doc.getObject("CabinetPCSlideV22")
    if v22:
        v22.ViewObject.Visibility = False
    for name in (
        "PCServiceSledV21", "PCServiceSledLiftGhostV21",
        "PCSledLocator1V21", "PCSledLocator2V21", "PCSledLocator3V21", "PCSledLocator4V21",
        "PCOpenChassisReferenceV21",
    ):
        obj = doc.getObject(name)
        if obj:
            obj.ViewObject.Visibility = False

    # Replace the simple captured rear-panel visual with a real rear PC-service aperture.
    rear = doc.getObject("CapturedRearPanelV20")
    if rear is None:
        raise RuntimeError("CapturedRearPanelV20 missing; build v0.20 first")
    rear.ViewObject.Visibility = False

    ax = float(door["aperture_x_mm"])
    az = float(door["aperture_bottom_z_mm"])
    aw = float(door["raw_aperture_width_x_mm"])
    ah = float(door["raw_aperture_height_z_mm"])
    cut = Part.makeBox(aw, wood + 4.0, ah, App.Vector(ax, length - wood - 2.0, az))
    rear_cut = rear.Shape.cut(cut)
    add_shape(doc, group, "RearPanelWithPCDoorV23", "CAB-REAR-001-R2 - REAR PC SERVICE APERTURE", rear_cut, 5, "CAB-REAR-001-R2")
    add_shape(doc, group, "RearPCDoorClearOpeningGhostV23", "REAR PC SERVICE CLEAR OPENING 520x280", cut, 88)

    # Compact fixed steel-angle-frame packaging around the opening. These are envelopes,
    # not final bent-section fabrication drawings.
    frame_w = float(door["nominal_frame_section_mm"][0])
    frame_t = float(door["nominal_frame_section_mm"][2])
    fy = length - wood - frame_t
    add_shape(doc, group, "RearPCFrameLeftV23", "REAR PC DOOR FRAME LEFT - 25x25x2 STEEL ANGLE ENVELOPE",
              Part.makeBox(frame_w, frame_t, ah, App.Vector(ax - frame_w, fy, az)), 40)
    add_shape(doc, group, "RearPCFrameRightV23", "REAR PC DOOR FRAME RIGHT - 25x25x2 STEEL ANGLE ENVELOPE",
              Part.makeBox(frame_w, frame_t, ah, App.Vector(ax + aw, fy, az)), 40)
    add_shape(doc, group, "RearPCFrameBottomV23", "REAR PC DOOR FRAME BOTTOM - 25x25x2 STEEL ANGLE ENVELOPE",
              Part.makeBox(aw + 2*frame_w, frame_t, frame_w, App.Vector(ax-frame_w, fy, az-frame_w)), 40)
    add_shape(doc, group, "RearPCFrameTopV23", "REAR PC DOOR FRAME TOP - 25x25x2 STEEL ANGLE ENVELOPE",
              Part.makeBox(aw + 2*frame_w, frame_t, frame_w, App.Vector(ax-frame_w, fy, az+ah)), 40)

    # Rear door: outward-opening, left-hinged as viewed from behind.
    dw = float(door["door_panel_width_x_mm"])
    dh = float(door["door_panel_height_z_mm"])
    dt = float(door["door_panel_thickness_y_mm"])
    dx = float(door["door_panel_x_mm"])
    dz = float(door["door_panel_bottom_z_mm"])
    closed = Part.makeBox(dw, dt, dh, App.Vector(dx, length, dz))
    add_shape(doc, group, "RearPCServiceDoorClosedV23", "CAB-PC-REAR-DOOR-001-R1 - CLOSED", closed, 20, "CAB-PC-REAR-DOOR-001-R1")
    opened = closed.copy()
    opened.rotate(App.Vector(dx, length, dz), App.Vector(0, 0, 1), -float(door["outward_open_angle_deg"]))
    add_shape(doc, group, "RearPCServiceDoorOpenGhostV23", "REAR PC SERVICE DOOR - 105deg OPEN GHOST", opened, 82)
    add_shape(doc, group, "RearPCDoorLatchKeepoutV23", "REAR PC DOOR KEYED/TOOL LATCH - HARDWARE TBD",
              Part.makeBox(30.0, 25.0, 45.0, App.Vector(dx+dw-42.0, length-10.0, dz+dh/2.0-22.5)), 70)

    # Small shelf, approximately the open-case footprint, stows directly behind the rear door.
    sw = float(pc["shelf_width_x_mm"])
    sd = float(pc["shelf_depth_y_mm"])
    st = float(pc["shelf_thickness_z_mm"])
    sx = float(pc["shelf_x_mm"])
    sy = float(pc["shelf_stowed_y_mm"])
    service_y = float(pc["shelf_service_y_mm"])
    sz = float(pc["shelf_z_mm"])
    shelf = Part.makeBox(sw, sd, st, App.Vector(sx, sy, sz))
    add_shape(doc, group, "RearPCShelfStowedV23", "PC-SHELF-REAR-001-R1 - STOWED BEHIND BACKDOOR", shelf, 12, "PC-SHELF-REAR-001-R1")
    shelf_service = shelf.copy()
    shelf_service.translate(App.Vector(0, service_y-sy, 0))
    add_shape(doc, group, "RearPCShelfServiceGhostV23", "PC SHELF - 300 mm REARWARD SERVICE GHOST", shelf_service, 80)

    # Compact side spacer rails let the shelf remain case-sized instead of spanning the cabinet.
    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])
    slide_h = float(pc["slide_packaging_height_mm"])
    spacer = float(pc["side_spacer_rail_thickness_each_side_mm"])
    spacer_l = float(pc["side_spacer_rail_length_y_mm"])
    spacer_h = float(pc["side_spacer_rail_height_z_mm"])
    rail_y = sy - 20.0
    rail_z = sz - (spacer_h - st)/2.0
    add_shape(doc, group, "RearPCSpacerLeftV23", "PC SLIDE SPACER RAIL LEFT - STACK TBD AFTER REAL SLIDES",
              Part.makeBox(spacer, spacer_l, spacer_h, App.Vector(wood, rail_y, rail_z)), 25)
    add_shape(doc, group, "RearPCSpacerRightV23", "PC SLIDE SPACER RAIL RIGHT - STACK TBD AFTER REAL SLIDES",
              Part.makeBox(spacer, spacer_l, spacer_h, App.Vector(outer-wood-spacer, rail_y, rail_z)), 25)

    left_slide_x = wood + spacer
    right_slide_x = sx + sw
    slide_y = sy - 15.0
    slide_z = sz - (slide_h-st)/2.0
    add_shape(doc, group, "RearPCSlideFixedLeftV23", "300 mm REAR PC SLIDE LEFT - HOLES TBD",
              Part.makeBox(slide_t, 300.0, slide_h, App.Vector(left_slide_x, slide_y, slide_z)), 65)
    add_shape(doc, group, "RearPCSlideFixedRightV23", "300 mm REAR PC SLIDE RIGHT - HOLES TBD",
              Part.makeBox(slide_t, 300.0, slide_h, App.Vector(right_slide_x, slide_y, slide_z)), 65)
    add_shape(doc, group, "RearPCSlideServiceLeftGhostV23", "LEFT SLIDE MOVING MEMBER - REAR SERVICE GHOST",
              Part.makeBox(slide_t, 300.0, slide_h, App.Vector(left_slide_x, service_y, slide_z)), 86)
    add_shape(doc, group, "RearPCSlideServiceRightGhostV23", "RIGHT SLIDE MOVING MEMBER - REAR SERVICE GHOST",
              Part.makeBox(slide_t, 300.0, slide_h, App.Vector(right_slide_x, service_y, slide_z)), 86)

    # Open case bolts directly to the shelf.
    cw = float(case["width_x_mm"])
    cd = float(case["depth_y_mm"])
    ch = float(case["height_z_mm"])
    cx = sx + (sw-cw)/2.0
    cy = sy + (sd-cd)/2.0
    chassis = Part.makeBox(cw, cd, ch, App.Vector(cx, cy, sz+st))
    add_shape(doc, group, "RearPCOpenCaseStowedV23", "OPEN PC CASE 440x265x128 - BOLTED DIRECT TO REAR SHELF", chassis, 72)
    chassis_service = chassis.copy()
    chassis_service.translate(App.Vector(0, service_y-sy, 0))
    add_shape(doc, group, "RearPCOpenCaseServiceGhostV23", "OPEN PC CASE - PULLED OUT THROUGH REAR DOOR", chassis_service, 88)

    # One simple positive stowed retainer and a cable-loop keepout.
    add_shape(doc, group, "RearPCStowedRetainerV23", "PC REAR SHELF POSITIVE STOWED RETAINER - HARDWARE TBD",
              Part.makeBox(20.0, 20.0, 35.0, App.Vector(sx+15.0, sy+sd-10.0, sz-8.0)), 60)
    add_shape(doc, group, "RearPCCableLoopKeepoutV23", "PC REAR SERVICE HARNESS LOOP >=450 mm",
              Part.makeBox(45.0, 360.0, 100.0, App.Vector(sx+sw-55.0, sy-40.0, sz+35.0)), 90)

    group.addProperty("App::PropertyString", "ServiceDirection", "Engineering")
    group.ServiceDirection = "REAR / BACK / TRASEIRA: OPEN BACKDOOR AND PULL PC OUT BEHIND MACHINE"
    group.addProperty("App::PropertyString", "RoutineService", "Engineering")
    group.RoutineService = "NO PLAYFIELD OPENING REQUIRED FOR ROUTINE PC SERVICE"
    group.addProperty("App::PropertyString", "Safety", "Engineering")
    group.Safety = "ISOLATE CABINET POWER BEFORE RAM/GPU/SSD/HARNESS SERVICE; NO BARE MAINS AT REAR PC DOOR"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("REAR PC SERVICE v0.23 GENERATED")
    print("=" * 80)
    print(f"Rear door aperture         {aw:.0f} x {ah:.0f} mm at Z {az:.0f}..{az+ah:.0f}")
    print(f"PC shelf                   {sw:.0f} x {sd:.0f} x {st:.0f} mm")
    print(f"Stowed -> service Y        {sy:.0f} -> {service_y:.0f} mm (rearward)")
    print(f"Open case ref              {cw:.0f} x {cd:.0f} x {ch:.0f} mm")
    print("Routine service            FROM REAR DOOR; PLAYFIELD STAYS CLOSED")
    print("STATUS                     ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_rear_cpu_shelf_v24.json")
V20 = os.path.join(ROOT, "config/cabinet_structure_v20.json")


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def set_visibility(obj, visible: bool) -> None:
    """Best-effort visibility change that is safe under headless FreeCADCmd.

    In FreeCADCmd some document objects have no ViewObject at all. Geometry creation
    and serialization must not depend on GUI-only view providers being present.
    """
    if obj is None:
        return
    try:
        view = getattr(obj, "ViewObject", None)
    except Exception:
        view = None
    if view is None:
        return
    try:
        view.Visibility = bool(visible)
    except Exception:
        pass


def add_shape(doc, group, name, label, shape, transparency=0, part_id=None):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    if part_id:
        obj.addProperty("App::PropertyString", "PartID", "Build Package")
        obj.PartID = part_id
    try:
        view = getattr(obj, "ViewObject", None)
        if view is not None:
            view.Transparency = transparency
    except Exception:
        pass
    return obj


def main() -> None:
    cfg = load(CFG)
    v20 = load(V20)
    door = cfg["rear_service_door"]
    pc = cfg["pc_shelf"]
    case = cfg["open_pc_case_reference"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    length = float(cab["side_length_mm"])
    wood = float(cab["nominal_wood_mm"])

    doc = App.openDocument(MASTER)
    old = doc.getObject("CabinetRearCPUShelfV24")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    # v0.24 supersedes the wider v0.23 shelf/door visuals, but keeps all prior
    # cabinet, classic-leg and PinSkates decisions.
    v23 = doc.getObject("CabinetRearPCServiceV23")
    set_visibility(v23, False)

    group = doc.addObject("App::Part", "CabinetRearCPUShelfV24")
    group.Label = "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)"

    rear = doc.getObject("CapturedRearPanelV20")
    if rear is None:
        raise RuntimeError("CapturedRearPanelV20 missing; build v0.20 base first")
    set_visibility(rear, False)

    # Narrower rear aperture preserves much more rear-panel structure than v0.23.
    ax = float(door["aperture_x_mm"])
    az = float(door["aperture_bottom_z_mm"])
    aw = float(door["raw_aperture_width_x_mm"])
    ah = float(door["raw_aperture_height_z_mm"])
    cut = Part.makeBox(aw, wood + 4.0, ah, App.Vector(ax, length - wood - 2.0, az))
    rear_cut = rear.Shape.cut(cut)
    add_shape(doc, group, "RearPanelWithCPUHatchV24", "CAB-REAR-001-R3 - NARROW REAR CPU HATCH", rear_cut, 5, "CAB-REAR-001-R3")
    add_shape(doc, group, "RearCPUHatchOpeningGhostV24", "REAR CPU CLEAR OPENING 340x240", cut, 88)

    # Simple overlapping rear service door, left hinged as viewed from behind.
    dw = float(door["door_panel_width_x_mm"])
    dh = float(door["door_panel_height_z_mm"])
    dt = float(door["door_panel_thickness_y_mm"])
    dx = float(door["door_panel_x_mm"])
    dz = float(door["door_panel_bottom_z_mm"])
    closed = Part.makeBox(dw, dt, dh, App.Vector(dx, length, dz))
    add_shape(doc, group, "RearCPUServiceDoorClosedV24", "CAB-PC-REAR-DOOR-002-R1 - CLOSED", closed, 20, "CAB-PC-REAR-DOOR-002-R1")
    opened = closed.copy()
    opened.rotate(App.Vector(dx, length, dz), App.Vector(0, 0, 1), -float(door["outward_open_angle_deg"]))
    add_shape(doc, group, "RearCPUServiceDoorOpenGhostV24", "REAR CPU DOOR - OPEN GHOST", opened, 82)

    # Case-sized shelf: case rotated so its narrow 265 mm dimension is cross-cabinet
    # and its 440 mm dimension runs fore-aft, matching a conventional rear CPU shelf.
    sw = float(pc["shelf_width_x_mm"])
    sd = float(pc["shelf_depth_y_mm"])
    st = float(pc["shelf_thickness_z_mm"])
    sx = float(pc["shelf_x_mm"])
    sy = float(pc["shelf_stowed_y_mm"])
    service_y = float(pc["shelf_service_y_mm"])
    sz = float(pc["shelf_z_mm"])
    shelf = Part.makeBox(sw, sd, st, App.Vector(sx, sy, sz))
    add_shape(doc, group, "RearCPUShelfStowedV24", "PC-REAR-SHELF-002-R1 - CASE-SIZED BOARD / STOWED", shelf, 12, "PC-REAR-SHELF-002-R1")
    shelf_service = shelf.copy()
    shelf_service.translate(App.Vector(0, service_y - sy, 0))
    add_shape(doc, group, "RearCPUShelfServiceGhostV24", "PC SHELF - 450 mm REARWARD FULL-SERVICE GHOST", shelf_service, 80)

    # Two narrow fixed support rails carry the fixed slide members. They are local
    # internal rails, not full-width shelves or bulky cabinet furniture.
    rw = float(pc["fixed_support_rail_width_x_mm"])
    rl = float(pc["fixed_support_rail_length_y_mm"])
    rh = float(pc["fixed_support_rail_height_z_mm"])
    rlx = float(pc["fixed_support_left_x_mm"])
    rrx = float(pc["fixed_support_right_x_mm"])
    rail_y = sy - 5.0
    rail_z = sz - (rh - st) / 2.0
    add_shape(doc, group, "RearCPUSupportRailLeftV24", "PC REAR SLIDE SUPPORT LEFT - SIMPLE LOCAL RAIL", Part.makeBox(rw, rl, rh, App.Vector(rlx, rail_y, rail_z)), 25)
    add_shape(doc, group, "RearCPUSupportRailRightV24", "PC REAR SLIDE SUPPORT RIGHT - SIMPLE LOCAL RAIL", Part.makeBox(rw, rl, rh, App.Vector(rrx, rail_y, rail_z)), 25)

    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])
    slide_h = float(pc["slide_packaging_height_mm"])
    slide_l = float(pc["travel_mm"])
    left_slide_x = rlx + rw
    right_slide_x = sx + sw
    slide_z = sz - (slide_h - st) / 2.0
    add_shape(doc, group, "RearCPUFixedSlideLeftV24", "450 mm CLASS REAR CPU SLIDE LEFT - HOLES TBD", Part.makeBox(slide_t, slide_l, slide_h, App.Vector(left_slide_x, sy, slide_z)), 65)
    add_shape(doc, group, "RearCPUFixedSlideRightV24", "450 mm CLASS REAR CPU SLIDE RIGHT - HOLES TBD", Part.makeBox(slide_t, slide_l, slide_h, App.Vector(right_slide_x, sy, slide_z)), 65)
    add_shape(doc, group, "RearCPUServiceSlideLeftGhostV24", "LEFT SLIDE MOVING MEMBER - REAR SERVICE GHOST", Part.makeBox(slide_t, slide_l, slide_h, App.Vector(left_slide_x, service_y, slide_z)), 86)
    add_shape(doc, group, "RearCPUServiceSlideRightGhostV24", "RIGHT SLIDE MOVING MEMBER - REAR SERVICE GHOST", Part.makeBox(slide_t, slide_l, slide_h, App.Vector(right_slide_x, service_y, slide_z)), 86)

    cw = float(case["installed_width_x_mm"])
    cd = float(case["installed_depth_y_mm"])
    ch = float(case["installed_height_z_mm"])
    cx = sx + (sw - cw) / 2.0
    cy = sy + (sd - cd) / 2.0
    chassis = Part.makeBox(cw, cd, ch, App.Vector(cx, cy, sz + st))
    add_shape(doc, group, "RearCPUOpenCaseStowedV24", "OPEN PC CASE 265x440x128 - ROTATED / BOLTED DIRECT TO BOARD", chassis, 72)
    chassis_service = chassis.copy()
    chassis_service.translate(App.Vector(0, service_y - sy, 0))
    add_shape(doc, group, "RearCPUOpenCaseServiceGhostV24", "OPEN PC CASE - PULLED REARWARD OUT OF PINBALL", chassis_service, 88)

    add_shape(doc, group, "RearCPUStowedRetainerV24", "ONE SIMPLE POSITIVE STOWED RETAINER - HARDWARE TBD", Part.makeBox(18.0, 18.0, 32.0, App.Vector(sx + 10.0, sy + sd - 8.0, sz - 7.0)), 60)
    add_shape(doc, group, "RearCPUHarnessLoopGhostV24", "REAR CPU HARNESS SERVICE LOOP >=600 mm", Part.makeBox(35.0, 480.0, 90.0, App.Vector(sx + sw + 20.0, sy - 15.0, sz + 25.0)), 90)

    group.addProperty("App::PropertyString", "ReferenceArchitecture", "Engineering")
    group.ReferenceArchitecture = "REAR CPU SLIDE-OUT SHELF: ONE BOARD + TWO FULL-EXTENSION SLIDES"
    group.addProperty("App::PropertyString", "ServiceDirection", "Engineering")
    group.ServiceDirection = "REARWARD THROUGH MAIN-CABINET BACKDOOR; PLAYFIELD STAYS CLOSED"
    group.addProperty("App::PropertyString", "CaseOrientation", "Engineering")
    group.CaseOrientation = "OWNER 440x265 CASE ROTATED: 265 X / 440 Y"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("REAR CPU SHELF v0.24 GENERATED")
    print("=" * 80)
    print(f"Rear hatch                 {aw:.0f} x {ah:.0f} mm")
    print(f"Case-sized shelf           {sw:.0f} x {sd:.0f} x {st:.0f} mm")
    print(f"Open case installed        {cw:.0f} x {cd:.0f} x {ch:.0f} mm")
    print(f"Rearward travel            {service_y-sy:.0f} mm")
    print("Routine service            OPEN REAR DOOR + PULL PC OUT; PLAYFIELD CLOSED")
    print("STATUS                     ENGINEERING PACKAGING - NOT FOR MANUFACTURING")
    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

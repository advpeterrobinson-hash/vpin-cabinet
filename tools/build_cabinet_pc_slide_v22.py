#!/usr/bin/env python3
"""Build the owner-directed simple PC slide overlay (v0.22).

One flat shelf rides on two direct side-mount drawer slides.  The selected open
PC case bolts directly to that shelf.  There is no drawer box, no second sled,
and no large travel toward/through the cabinet front.
"""
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_pc_slide_v22.json")
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
    pc = cfg["pc_slide"]
    case = cfg["open_pc_case_reference"]
    cab = v20["cabinet"]

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_wood_mm"])

    doc = App.openDocument(MASTER)
    old = doc.getObject("CabinetPCSlideV22")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "CabinetPCSlideV22")
    group.Label = "PC SERVICE v0.22 - SIMPLE SLIDING SHELF / OPEN CASE BOLTED DIRECT"

    # Supersede only the v0.21 PC-lift-out visuals. Classic legs / PinSkates stay.
    for name in (
        "PCServiceSledV21", "PCServiceSledLiftGhostV21",
        "PCSledLocator1V21", "PCSledLocator2V21", "PCSledLocator3V21", "PCSledLocator4V21",
        "PCOpenChassisReferenceV21",
    ):
        obj = doc.getObject(name)
        if obj:
            try:
                obj.ViewObject.Visibility = False
            except Exception:
                pass

    sw = float(pc["shelf_width_x_mm"])
    sd = float(pc["shelf_depth_y_mm"])
    st = float(pc["shelf_thickness_z_mm"])
    sx = float(pc["shelf_x_mm"])
    sy = float(pc["shelf_stowed_y_mm"])
    service_y = float(pc["shelf_service_y_mm"])
    sz = float(pc["shelf_z_mm"])
    slide_t = float(pc["slide_packaging_thickness_each_side_mm"])
    slide_h = float(pc["slide_packaging_height_mm"])
    travel = float(pc["travel_mm"])

    shelf = Part.makeBox(sw, sd, st, App.Vector(sx, sy, sz))
    add_shape(doc, group, "PCSlidingShelfStowedV22", "PC-SHELF-001-R1 - SIMPLE SLIDING SHELF / STOWED", shelf, 12, "PC-SHELF-001-R1")

    service = shelf.copy()
    service.translate(App.Vector(0, service_y - sy, 0))
    add_shape(doc, group, "PCSlidingShelfServiceGhostV22", "PC SHELF - 300 mm INTERNAL SERVICE POSITION GHOST", service, 82)

    # Fixed and moving slide packages.  Catalogue hole patterns are deliberately
    # absent; shelf width is re-derived from the measured physical slide pair.
    left_fixed = Part.makeBox(slide_t, sd, slide_h, App.Vector(wood, sy, sz - 13.5))
    right_fixed = Part.makeBox(slide_t, sd, slide_h, App.Vector(outer - wood - slide_t, sy, sz - 13.5))
    add_shape(doc, group, "PCSlideFixedLeftV22", "300 mm SIDE-MOUNT SLIDE LEFT - HOLES TBD", left_fixed, 65)
    add_shape(doc, group, "PCSlideFixedRightV22", "300 mm SIDE-MOUNT SLIDE RIGHT - HOLES TBD", right_fixed, 65)

    left_moving = Part.makeBox(slide_t, sd, slide_h, App.Vector(sx - slide_t, service_y, sz - 13.5))
    right_moving = Part.makeBox(slide_t, sd, slide_h, App.Vector(sx + sw, service_y, sz - 13.5))
    add_shape(doc, group, "PCSlideServiceLeftGhostV22", "LEFT SLIDE MOVING MEMBER - SERVICE GHOST", left_moving, 86)
    add_shape(doc, group, "PCSlideServiceRightGhostV22", "RIGHT SLIDE MOVING MEMBER - SERVICE GHOST", right_moving, 86)

    # Open case reference is directly on the shelf.  This is a fit envelope only;
    # actual mounting holes are not created until the purchased case is measured.
    cw = float(case["width_mm"])
    cd = float(case["depth_mm"])
    ch = float(case["height_mm"])
    cx = sx + (sw - cw) / 2.0
    cy = sy + (sd - cd) / 2.0
    chassis = Part.makeBox(cw, cd, ch, App.Vector(cx, cy, sz + st))
    add_shape(doc, group, "PCOpenCaseReferenceStowedV22", "OPEN PC CASE 440x265x128 - BOLTS DIRECTLY TO SHELF", chassis, 72)

    chassis_service = chassis.copy()
    chassis_service.translate(App.Vector(0, service_y - sy, 0))
    add_shape(doc, group, "PCOpenCaseReferenceServiceGhostV22", "OPEN PC CASE - SERVICE POSITION GHOST", chassis_service, 88)

    # Simple positive stowed-retention envelope near the shelf front-left corner.
    retainer = Part.makeBox(18.0, 18.0, 35.0, App.Vector(sx + 18.0, sy - 9.0, sz - 8.0))
    add_shape(doc, group, "PCShelfStowedRetainerV22", "SIMPLE POSITIVE STOWED RETAINER - HARDWARE TBD", retainer, 65)

    group.addProperty("App::PropertyString", "Architecture", "Engineering")
    group.Architecture = "ONE FLAT SHELF + TWO DIRECT SIDE-MOUNT SLIDES + ONE STOWED RETAINER"
    group.addProperty("App::PropertyString", "CaseMountPolicy", "Engineering")
    group.CaseMountPolicy = "OPEN PC CASE BOLTS DIRECTLY TO SHELF; NO SECOND SLED"
    group.addProperty("App::PropertyLength", "ServiceTravel", "Engineering")
    group.ServiceTravel = travel
    group.addProperty("App::PropertyString", "HoleStatus", "Engineering")
    group.HoleStatus = "SLIDE + OPEN-CASE HOLES BLOCKED UNTIL PHYSICAL PARTS ARE MEASURED"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("PC SERVICE v0.22 GENERATED")
    print("=" * 72)
    print(f"Shelf                     {sw:.1f} x {sd:.1f} x {st:.1f} mm")
    print(f"Stowed/service Y          {sy:.1f} / {service_y:.1f} mm")
    print(f"Internal travel           {travel:.1f} mm")
    print(f"Open PC case ref          {cw:.1f} x {cd:.1f} x {ch:.1f} mm")
    print("Architecture              flat shelf + 2 slides; open case bolts direct")
    print("STATUS                    ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

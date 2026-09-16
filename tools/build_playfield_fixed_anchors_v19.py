#!/usr/bin/env python3
"""Build fixed cabinet-side support/anchor load paths for playfield mechanics v0.19.

This stage complements v0.18 by giving the previously free-floating packaging
pads/stays/struts explicit cabinet-side structural zones. Exact hardware holes
remain intentionally blocked until physical stays, latches and gas-spring
brackets are selected.
"""
from __future__ import annotations

import json
import math
import os

import FreeCAD as App
import Part

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
MECH_CFG = os.path.join(ROOT, "config/playfield_mechanics_v18.json")
ANCHOR_CFG = os.path.join(ROOT, "config/playfield_fixed_anchors_v19.json")


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
    mech = load(MECH_CFG)
    anchors = load(ANCHOR_CFG)
    cab = mech["cabinet"]
    disp = mech["display_envelope"]
    cradle = mech["cradle"]
    gs = mech["gas_struts"]
    stays = mech["safety_stays"]
    closed = mech["closed_support"]

    if owns_document and not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    if owns_document:
        doc = App.openDocument(MASTER)
    mech_group = doc.getObject("PlayfieldMechanicsV18")
    if mech_group is None:
        raise RuntimeError("PlayfieldMechanicsV18 must be generated before v0.19 anchors")

    old = doc.getObject("PlayfieldFixedAnchorsV19")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "PlayfieldFixedAnchorsV19")
    group.Label = "PLAYFIELD FIXED ANCHORS v0.19 - SIDEWALL LOAD PATHS"

    outer = float(cab["outer_width_mm"])
    wood = float(cab["nominal_side_thickness_mm"])
    front_setback = float(disp["front_setback_mm"])

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    alpha = math.atan2(slope_rise, slope_run)
    alpha_deg = math.degrees(alpha)

    # Recover the same v0.18 local/global transform from the generated mechanics.
    hinge_y = float(mech_group.HingeY.Value)
    hinge_z = float(mech_group.HingeZ.Value)
    hinge_local_y = float(mech["hinge_axis"]["local_y_from_display_front_mm"])
    hinge_local_z = float(mech["hinge_axis"]["local_z_from_display_base_mm"])
    base_z = hinge_z - hinge_local_y * math.sin(alpha) - hinge_local_z * math.cos(alpha)

    def transform_shape(shape):
        result = shape.copy()
        result.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
        result.translate(App.Vector(0, front_setback, base_z))
        return result

    def transform_point(x: float, y: float, z: float) -> App.Vector:
        yy = y * math.cos(alpha) - z * math.sin(alpha) + front_setback
        zz = y * math.sin(alpha) + z * math.cos(alpha) + base_z
        return App.Vector(x, yy, zz)

    # ------------------------------------------------------------------
    # Front closed-position supports: fixed sidewall doublers + steel seats.
    # Seats follow playfield slope and contact the underside of each side rail.
    # ------------------------------------------------------------------
    fs = anchors["closed_front_support"]
    seat_reach = float(fs["steel_seat_inboard_reach_x_mm"])
    seat_len = float(fs["steel_seat_length_y_mm"])
    seat_t = float(fs["steel_seat_thickness_z_mm"])
    seat_y = float(fs["steel_seat_local_y_front_mm"])
    seat_z = float(fs["steel_seat_local_z_bottom_mm"])

    left_seat_local = Part.makeBox(seat_reach, seat_len, seat_t, App.Vector(wood, seat_y, seat_z))
    right_seat_local = Part.makeBox(seat_reach, seat_len, seat_t, App.Vector(outer - wood - seat_reach, seat_y, seat_z))
    left_seat = transform_shape(left_seat_local)
    right_seat = transform_shape(right_seat_local)
    add_shape(doc, group, "ClosedSupportSeatLeftV19", "PF-CLOSED-SUPPORT-SEAT-L - 3 mm STEEL", left_seat, 10, "PF-CLOSED-SUPPORT-SEAT-L-R1")
    add_shape(doc, group, "ClosedSupportSeatRightV19", "PF-CLOSED-SUPPORT-SEAT-R - 3 mm STEEL", right_seat, 10, "PF-CLOSED-SUPPORT-SEAT-R-R1")

    # Sidewall doublers are represented as vertical cabinet-fixed blocks around
    # the seat load path. Final CNC shape will follow the side profile.
    seat_center = transform_point(0.0, seat_y + seat_len / 2.0, seat_z - 35.0)
    dbl_y = float(fs["sidewall_doubler_length_y_mm"])
    dbl_z = float(fs["sidewall_doubler_height_z_mm"])
    dbl_x = float(fs["sidewall_doubler_thickness_x_mm"])
    add_shape(doc, group, "ClosedSupportDoublerLeftV19", "PF-CLOSED-SUPPORT-DBLR-L - 18 mm PLYWOOD",
              Part.makeBox(dbl_x, dbl_y, dbl_z, App.Vector(wood, seat_center.y-dbl_y/2.0, seat_center.z-dbl_z/2.0)), 20, "PF-CLOSED-SUPPORT-DBLR-L-R1")
    add_shape(doc, group, "ClosedSupportDoublerRightV19", "PF-CLOSED-SUPPORT-DBLR-R - 18 mm PLYWOOD",
              Part.makeBox(dbl_x, dbl_y, dbl_z, App.Vector(outer-wood-dbl_x, seat_center.y-dbl_y/2.0, seat_center.z-dbl_z/2.0)), 20, "PF-CLOSED-SUPPORT-DBLR-R-R1")

    # ------------------------------------------------------------------
    # Safety-stay fixed anchor zones: doubled plywood + captive 6 mm steel.
    # Exact stay pin/slot hardware remains TBD.
    # ------------------------------------------------------------------
    sa = anchors["safety_stay_fixed_anchor"]
    stay_y = hinge_y - float(stays["fixed_mount_forward_from_hinge_mm"])
    stay_z = hinge_z - float(stays["fixed_mount_below_hinge_mm"])
    sdy = float(sa["plywood_doubler_length_y_mm"])
    sdz = float(sa["plywood_doubler_height_z_mm"])
    sdx = float(sa["plywood_doubler_thickness_x_mm"])
    spy = float(sa["steel_nut_plate_length_y_mm"])
    spz = float(sa["steel_nut_plate_height_z_mm"])
    spx = float(sa["steel_nut_plate_thickness_x_mm"])
    add_shape(doc, group, "SafetyStayDoublerLeftV19", "PF-SAFETY-STAY-ANCHOR-DBLR-L - 18 mm PLYWOOD",
              Part.makeBox(sdx, sdy, sdz, App.Vector(wood, stay_y-sdy/2.0, stay_z-sdz/2.0)), 25, "PF-SAFETY-STAY-ANCHOR-DBLR-L-R1")
    add_shape(doc, group, "SafetyStayDoublerRightV19", "PF-SAFETY-STAY-ANCHOR-DBLR-R - 18 mm PLYWOOD",
              Part.makeBox(sdx, sdy, sdz, App.Vector(outer-wood-sdx, stay_y-sdy/2.0, stay_z-sdz/2.0)), 25, "PF-SAFETY-STAY-ANCHOR-DBLR-R-R1")
    add_shape(doc, group, "SafetyStayNutPlateLeftV19", "PF-SAFETY-STAY-NUTPLATE-L - 6 mm STEEL / HOLES TBD",
              Part.makeBox(spx, spy, spz, App.Vector(wood+sdx, stay_y-spy/2.0, stay_z-spz/2.0)), 20)
    add_shape(doc, group, "SafetyStayNutPlateRightV19", "PF-SAFETY-STAY-NUTPLATE-R - 6 mm STEEL / HOLES TBD",
              Part.makeBox(spx, spy, spz, App.Vector(outer-wood-sdx-spx, stay_y-spy/2.0, stay_z-spz/2.0)), 20)

    # ------------------------------------------------------------------
    # Gas-strut fixed anchor zones. Same principle; exact ball stud remains open.
    # ------------------------------------------------------------------
    ga = anchors["gas_strut_fixed_anchor"]
    gas_y = hinge_y - float(gs["fixed_mount_forward_from_hinge_mm"])
    gas_z = hinge_z - float(gs["fixed_mount_below_hinge_mm"])
    gdy = float(ga["plywood_doubler_length_y_mm"])
    gdz = float(ga["plywood_doubler_height_z_mm"])
    gdx = float(ga["plywood_doubler_thickness_x_mm"])
    gpy = float(ga["steel_nut_plate_length_y_mm"])
    gpz = float(ga["steel_nut_plate_height_z_mm"])
    gpx = float(ga["steel_nut_plate_thickness_x_mm"])
    add_shape(doc, group, "GasStrutDoublerLeftV19", "PF-GAS-ANCHOR-DBLR-L - 18 mm PLYWOOD",
              Part.makeBox(gdx, gdy, gdz, App.Vector(wood, gas_y-gdy/2.0, gas_z-gdz/2.0)), 30, "PF-GAS-ANCHOR-DBLR-L-R1")
    add_shape(doc, group, "GasStrutDoublerRightV19", "PF-GAS-ANCHOR-DBLR-R - 18 mm PLYWOOD",
              Part.makeBox(gdx, gdy, gdz, App.Vector(outer-wood-gdx, gas_y-gdy/2.0, gas_z-gdz/2.0)), 30, "PF-GAS-ANCHOR-DBLR-R-R1")
    add_shape(doc, group, "GasStrutNutPlateLeftV19", "PF-GAS-NUTPLATE-L - 6 mm STEEL / HOLES TBD",
              Part.makeBox(gpx, gpy, gpz, App.Vector(wood+gdx, gas_y-gpy/2.0, gas_z-gpz/2.0)), 35)
    add_shape(doc, group, "GasStrutNutPlateRightV19", "PF-GAS-NUTPLATE-R - 6 mm STEEL / HOLES TBD",
              Part.makeBox(gpx, gpy, gpz, App.Vector(outer-wood-gdx-gpx, gas_y-gpy/2.0, gas_z-gpz/2.0)), 35)

    # ------------------------------------------------------------------
    # Positive latch receiver reinforcement zones near the front supports.
    # These are cabinet-fixed strike/receiver envelopes, not selected hardware.
    # ------------------------------------------------------------------
    latch_local_y = float(closed["latch_front_y_mm"]) - front_setback
    latch_pt = transform_point(0.0, latch_local_y + 35.0, -105.0)
    latch_dbl_y = 100.0
    latch_dbl_z = 100.0
    add_shape(doc, group, "LatchReceiverDoublerLeftV19", "PF-LATCH-RECEIVER-DBLR-L - 18 mm PLYWOOD",
              Part.makeBox(18.0, latch_dbl_y, latch_dbl_z, App.Vector(wood, latch_pt.y-latch_dbl_y/2.0, latch_pt.z-latch_dbl_z/2.0)), 35)
    add_shape(doc, group, "LatchReceiverDoublerRightV19", "PF-LATCH-RECEIVER-DBLR-R - 18 mm PLYWOOD",
              Part.makeBox(18.0, latch_dbl_y, latch_dbl_z, App.Vector(outer-wood-18.0, latch_pt.y-latch_dbl_y/2.0, latch_pt.z-latch_dbl_z/2.0)), 35)

    group.addProperty("App::PropertyString", "ClosedSupportLoadPath", "Engineering")
    group.ClosedSupportLoadPath = "CRADLE RAIL -> RESILIENT PAD -> 3 mm STEEL SEAT -> 18 mm SIDEWALL DOUBLER -> CABINET SIDE"
    group.addProperty("App::PropertyString", "StayAnchorStatus", "Engineering")
    group.StayAnchorStatus = "DOUBLED PLYWOOD + 6 mm CAPTIVE STEEL; FINAL PIN/SLOT HOLES TBD"
    group.addProperty("App::PropertyString", "GasAnchorStatus", "Engineering")
    group.GasAnchorStatus = "DOUBLED PLYWOOD + 6 mm CAPTIVE STEEL; BALL-STUD GEOMETRY TBD AFTER MASS/CG"
    group.addProperty("App::PropertyString", "LatchStatus", "Engineering")
    group.LatchStatus = "FIXED RECEIVER REINFORCEMENT RESERVED; FINAL LATCH HARDWARE TBD"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    if owns_document:
        doc.save()

    print("PLAYFIELD FIXED ANCHORS v0.19 GENERATED")
    print("=" * 76)
    print("Closed supports          sidewall doubler + 3 mm steel seat each side")
    print("Safety-stay anchors      18 mm doubler + 6 mm captive steel each side")
    print("Gas-strut anchors        18 mm doubler + 6 mm captive steel each side")
    print("Latch receivers          reinforced cabinet-fixed zones each side")
    print("Hardware holes           TBD - PHYSICAL HARDWARE SELECTION REQUIRED")
    print("STATUS                   ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    if owns_document:
        App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

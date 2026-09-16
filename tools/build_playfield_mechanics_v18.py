#!/usr/bin/env python3
"""Build the integrated model-agnostic playfield mechanics package (v0.18).

The package replaces the old display-specific visual mockup as the active
mechanical review model.  It is still engineering packaging: exact VESA holes,
UCFL202 mounting holes, gas-strut force/mounts, stay slots and latch hardware
remain blocked until the physical parts/display are selected and measured.
"""
from __future__ import annotations

import json
import math
import os

import FreeCAD as App
import Part

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/playfield_mechanics_v18.json")


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def top_z(cab: dict, y: float) -> float:
    run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    if y <= run:
        rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
        return float(cab["front_height_mm"]) + rise * (y / run)
    return float(cab["rear_height_mm"])


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


def cylinder_between(a: App.Vector, b: App.Vector, radius: float):
    vec = b.sub(a)
    if vec.Length <= 1e-6:
        raise RuntimeError("Cannot create zero-length cylinder")
    return Part.makeCylinder(radius, vec.Length, a, vec)


def main(doc=None) -> None:
    owns_document = doc is None
    if owns_document and not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    cfg = load(CFG)
    cab = cfg["cabinet"]
    disp = cfg["display_envelope"]
    cradle = cfg["cradle"]
    hinge = cfg["hinge_axis"]
    pivot = cfg["pivot_interface"]
    vesa = cfg["vesa_adapter"]
    gs = cfg["gas_struts"]
    stays = cfg["safety_stays"]
    closed_support = cfg["closed_support"]
    harness = cfg["moving_harness"]
    loads = cfg["load_policy"]

    outer = float(cab["outer_width_mm"])
    inner = float(cab["full_thickness_inner_width_mm"])
    wood = float(cab["nominal_side_thickness_mm"])
    front_setback = float(disp["front_setback_mm"])
    display_w = float(disp["cross_width_mm"])
    display_l = float(disp["length_mm"])
    display_d = float(disp["depth_mm"])
    glass_gap = float(disp["glass_clearance_normal_mm"])

    slope_run = float(cab["side_length_mm"]) - float(cab["rear_top_flat_mm"])
    slope_rise = float(cab["rear_height_mm"]) - float(cab["front_height_mm"])
    alpha = math.atan2(slope_rise, slope_run)
    alpha_deg = math.degrees(alpha)

    # Local playfield coordinates: +Y toward the backbox, +Z normal-ish vertical
    # before the whole assembly is rotated to the cabinet slope.
    base_z = top_z(cab, front_setback) - glass_gap - display_d * math.cos(alpha)

    def transform_shape(shape):
        result = shape.copy()
        result.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
        result.translate(App.Vector(0, front_setback, base_z))
        return result

    def transform_point(x: float, y: float, z: float) -> App.Vector:
        yy = y * math.cos(alpha) - z * math.sin(alpha) + front_setback
        zz = y * math.sin(alpha) + z * math.cos(alpha) + base_z
        return App.Vector(x, yy, zz)

    def rotate_about_hinge(p: App.Vector, deg: float, hy: float, hz: float) -> App.Vector:
        theta = math.radians(deg)
        dy = p.y - hy
        dz = p.z - hz
        return App.Vector(
            p.x,
            hy + dy * math.cos(theta) - dz * math.sin(theta),
            hz + dy * math.sin(theta) + dz * math.cos(theta),
        )

    hinge_local_y = float(hinge["local_y_from_display_front_mm"])
    hinge_local_z = float(hinge["local_z_from_display_base_mm"])
    hinge_pt = transform_point(outer / 2.0, hinge_local_y, hinge_local_z)
    hinge_y = hinge_pt.y
    hinge_z = hinge_pt.z
    open_deg = float(hinge["relative_service_open_angle_deg"])

    if owns_document:
        doc = App.openDocument(MASTER)
    old = doc.getObject("PlayfieldMechanicsV18")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "PlayfieldMechanicsV18")
    group.Label = "PLAYFIELD MECHANICS v0.18 - GENERIC 43in / PLYWOOD CRADLE / DUAL SAFETY"

    # Hide superseded visual review groups without deleting historical geometry.
    for legacy_name in ("PlayfieldServiceV04", "PlayfieldServiceV05", "PlayfieldPivotV15"):
        legacy = doc.getObject(legacy_name)
        if legacy:
            try:
                legacy.ViewObject.Visibility = False
            except Exception:
                pass

    # Worst-case display envelope. This is deliberately NOT a Samsung or LG body.
    display_x0 = (outer - display_w) / 2.0
    display_local = Part.makeBox(display_w, display_l, display_d, App.Vector(display_x0, 0.0, 0.0))
    display_closed = transform_shape(display_local)
    display_obj = add_shape(
        doc, group, "GenericPlayfieldDisplayClosedV18",
        "GENERIC 42/43in DISPLAY ENVELOPE - 560x970x55 - CLOSED",
        display_closed, 65,
    )
    display_open = display_closed.copy()
    display_open.rotate(App.Vector(0, hinge_y, hinge_z), App.Vector(1, 0, 0), -open_deg)
    add_shape(
        doc, group, "GenericPlayfieldDisplayOpenGhostV18",
        "GENERIC DISPLAY - 70deg SERVICE GHOST", display_open, 88,
    )

    # Primary CNC-plywood cradle. Side rails are below the display and do not
    # consume the display's full-width service envelope.
    rail_tx = float(cradle["side_rail_thickness_x_mm"])
    rail_h = float(cradle["side_rail_height_z_mm"])
    rail_y0 = float(cradle["side_rail_front_local_y_mm"])
    rail_y1 = float(cradle["side_rail_rear_local_y_mm"])
    rail_len = rail_y1 - rail_y0
    rail_z0 = -75.0
    cradle_shapes = []
    for side, x0 in (("Left", float(cradle["left_side_rail_x_mm"])),
                     ("Right", float(cradle["right_side_rail_x_mm"]))):
        local = Part.makeBox(rail_tx, rail_len, rail_h, App.Vector(x0, rail_y0, rail_z0))
        closed_shape = transform_shape(local)
        cradle_shapes.append(closed_shape)
        add_shape(
            doc, group, f"CradleSideRail{side}V18",
            f"PF-CRADLE-SIDERAIL-{side.upper()} - 18 mm PLYWOOD",
            closed_shape, 15,
        )

    # Three flat crossmembers tie the rails together beneath the display.
    cm_w = float(cradle["crossmember_width_x_mm"])
    cm_d = float(cradle["crossmember_depth_y_mm"])
    cm_t = float(cradle["crossmember_thickness_z_mm"])
    cm_x0 = (outer - cm_w) / 2.0
    for idx, local_y in enumerate(cradle["crossmember_local_y_mm"], start=1):
        local = Part.makeBox(cm_w, cm_d, cm_t, App.Vector(cm_x0, float(local_y), -23.0))
        closed_shape = transform_shape(local)
        cradle_shapes.append(closed_shape)
        add_shape(
            doc, group, f"CradleCrossmember{idx}V18",
            f"PF-CRADLE-XMEM-{idx:02d} - 18 mm PLYWOOD",
            closed_shape, 20,
        )

    # 36 mm local pivot doublers at the two rear corners.
    dbl_x = float(cradle["pivot_doubler_local_thickness_x_mm"])
    dbl_y = float(cradle["pivot_doubler_length_y_mm"])
    dbl_z = float(cradle["pivot_doubler_height_z_mm"])
    dbl_y0 = hinge_local_y - 125.0
    dbl_z0 = hinge_local_z - dbl_z / 2.0
    for side, x0 in (("Left", float(cradle["left_pivot_doubler_x_mm"])),
                     ("Right", float(cradle["right_pivot_doubler_x_mm"]))):
        local = Part.makeBox(dbl_x, dbl_y, dbl_z, App.Vector(x0, dbl_y0, dbl_z0))
        closed_shape = transform_shape(local)
        cradle_shapes.append(closed_shape)
        add_shape(
            doc, group, f"CradlePivotDoubler{side}V18",
            f"PF-CRADLE-PIVOT-DBLR-{side.upper()} - 36 mm LOCAL PLYWOOD",
            closed_shape, 10,
        )

    # Rear laminated beam closes the load path between pivot zones.
    rear_beam_x0 = float(cradle["left_pivot_doubler_x_mm"]) + dbl_x
    rear_beam_x1 = float(cradle["right_pivot_doubler_x_mm"])
    rear_beam = Part.makeBox(
        rear_beam_x1 - rear_beam_x0,
        float(cradle["rear_crossmember_lamination_mm"]),
        70.0,
        App.Vector(rear_beam_x0, hinge_local_y - 36.0, -75.0),
    )
    rear_beam_closed = transform_shape(rear_beam)
    cradle_shapes.append(rear_beam_closed)
    add_shape(doc, group, "CradleRearBeamV18", "PF-CRADLE-REAR-BEAM - 18+18 mm LAMINATED", rear_beam_closed, 12)

    # Replaceable VESA carrier envelope - model-specific holes are intentionally absent.
    vw = float(vesa["packaging_width_x_mm"])
    vl = float(vesa["packaging_length_y_mm"])
    vt = float(vesa["packaging_thickness_z_mm"])
    vx0 = (outer - vw) / 2.0
    vy0 = float(vesa["center_local_y_mm"]) - vl / 2.0
    vesa_local = Part.makeBox(vw, vl, vt, App.Vector(vx0, vy0, -4.0))
    vesa_closed = transform_shape(vesa_local)
    cradle_shapes.append(vesa_closed)
    add_shape(doc, group, "VesaAdapterEnvelopeV18", "REPLACEABLE VESA ADAPTER ENVELOPE - HOLES TBD", vesa_closed, 45)

    # Steel pivot cheek plates move with the cradle. They sandwich the doubled
    # rear plywood zones and use the already-selected 140x80x6 mm geometry.
    pl = float(pivot["plate_length_y_mm"])
    ph = float(pivot["plate_height_z_mm"])
    pt = float(pivot["plate_thickness_mm"])
    py = float(pivot["pivot_axis_from_rear_plate_edge_mm"])
    pz = float(pivot["pivot_axis_from_bottom_plate_edge_mm"])
    rear_y = hinge_local_y + py
    plate_y0 = rear_y - pl
    plate_z0 = hinge_local_z - pz
    mount_y = [float(v) for v in pivot["mount_hole_centers_from_rear_y_mm"]]
    mount_z = [float(v) for v in pivot["mount_hole_centers_from_bottom_z_mm"]]

    def make_plate(x0: float):
        base = Part.makeBox(pt, pl, ph, App.Vector(x0, plate_y0, plate_z0))
        pivot_hole = Part.makeCylinder(
            float(pivot["journal_diameter_mm"]) / 2.0 + 0.1,
            pt + 2.0,
            App.Vector(x0 - 1.0, hinge_local_y, hinge_local_z),
            App.Vector(1, 0, 0),
        )
        result = base.cut(pivot_hole)
        for yo in mount_y:
            gy = rear_y - yo
            for zo in mount_z:
                gz = plate_z0 + zo
                hole = Part.makeCylinder(
                    float(pivot["mount_hole_diameter_mm"]) / 2.0,
                    pt + 2.0,
                    App.Vector(x0 - 1.0, gy, gz),
                    App.Vector(1, 0, 0),
                )
                result = result.cut(hole)
        return result

    left_plate_local = make_plate(float(cradle["left_pivot_doubler_x_mm"]) - pt)
    right_plate_local = make_plate(float(cradle["right_pivot_doubler_x_mm"]) + dbl_x)
    left_plate = transform_shape(left_plate_local)
    right_plate = transform_shape(right_plate_local)
    cradle_shapes.extend((left_plate, right_plate))
    add_shape(doc, group, "PivotPlateLeftV18", "PF-PIVOT-PLATE-001L-R1 - 6 mm STEEL", left_plate, 5, "PF-PIVOT-PLATE-001L-R1")
    add_shape(doc, group, "PivotPlateRightV18", "PF-PIVOT-PLATE-001R-R1 - 6 mm STEEL", right_plate, 5, "PF-PIVOT-PLATE-001R-R1")

    # Fixed-axis short journals and conservative bearing keepouts.
    jr = float(pivot["journal_diameter_mm"]) / 2.0
    jl = float(pivot["journal_projection_candidate_mm"])
    left_j = Part.makeCylinder(jr, jl, App.Vector(float(cradle["left_pivot_doubler_x_mm"]), hinge_y, hinge_z), App.Vector(-1, 0, 0))
    right_j = Part.makeCylinder(jr, jl, App.Vector(float(cradle["right_pivot_doubler_x_mm"]) + dbl_x, hinge_y, hinge_z), App.Vector(1, 0, 0))
    add_shape(doc, group, "PivotJournalLeftV18", "15 mm SHORT JOURNAL LEFT - LENGTH PROVISIONAL", left_j, 10)
    add_shape(doc, group, "PivotJournalRightV18", "15 mm SHORT JOURNAL RIGHT - LENGTH PROVISIONAL", right_j, 10)

    bearing_y = 120.0
    bearing_z = 75.0
    bearing_x = 35.0
    add_shape(doc, group, "UCFL202LeftKeepoutV18", "UCFL202 LEFT - MEASURE BEFORE CNC",
              Part.makeBox(bearing_x, bearing_y, bearing_z, App.Vector(-bearing_x, hinge_y-bearing_y/2, hinge_z-bearing_z/2)), 82)
    add_shape(doc, group, "UCFL202RightKeepoutV18", "UCFL202 RIGHT - MEASURE BEFORE CNC",
              Part.makeBox(bearing_x, bearing_y, bearing_z, App.Vector(outer, hinge_y-bearing_y/2, hinge_z-bearing_z/2)), 82)

    # 3 mm cabinet-side bearing spreader/backing envelopes.
    add_shape(doc, group, "BearingBackingLeftV18", "PF-PIVOT-BRG-BACK-001L - 3 mm STEEL",
              Part.makeBox(3.0, 120.0, 70.0, App.Vector(wood, hinge_y-60.0, hinge_z-35.0)), 35)
    add_shape(doc, group, "BearingBackingRightV18", "PF-PIVOT-BRG-BACK-001R - 3 mm STEEL",
              Part.makeBox(3.0, 120.0, 70.0, App.Vector(outer-wood-3.0, hinge_y-60.0, hinge_z-35.0)), 35)

    # One translucent open ghost of the whole moving cradle makes the service
    # envelope obvious without duplicating every component in the tree.
    cradle_closed_union = cradle_shapes[0]
    for shape in cradle_shapes[1:]:
        try:
            cradle_closed_union = cradle_closed_union.fuse(shape)
        except Exception:
            pass
    cradle_open = cradle_closed_union.copy()
    cradle_open.rotate(App.Vector(0, hinge_y, hinge_z), App.Vector(1, 0, 0), -open_deg)
    add_shape(doc, group, "CradleOpenGhostV18", "COMPLETE CRADLE - 70deg SERVICE GHOST", cradle_open, 88)

    # Gas-strut packaging. These cylinders are geometry probes only; force and
    # ball-stud brackets are not purchase/fabrication specs.
    gs_fixed_y = hinge_y - float(gs["fixed_mount_forward_from_hinge_mm"])
    gs_fixed_z = hinge_z - float(gs["fixed_mount_below_hinge_mm"])
    moving_local_y = hinge_local_y - float(gs["moving_mount_forward_from_hinge_mm"])
    moving_local_z = float(gs["moving_mount_local_z_mm"])
    for side, x in (("Left", 55.0), ("Right", outer - 55.0)):
        fixed = App.Vector(x, gs_fixed_y, gs_fixed_z)
        moving_closed = transform_point(x, moving_local_y, moving_local_z)
        moving_open = rotate_about_hinge(moving_closed, -open_deg, hinge_y, hinge_z)
        add_shape(doc, group, f"GasStrutClosed{side}V18", f"{side.upper()} GAS STRUT CLOSED - FORCE TBD",
                  cylinder_between(fixed, moving_closed, 5.0), 25)
        add_shape(doc, group, f"GasStrutOpen{side}GhostV18", f"{side.upper()} GAS STRUT OPEN GHOST - FORCE TBD",
                  cylinder_between(fixed, moving_open, 5.0), 78)

    # Two independent positive safety stays, one each side. They are shown only
    # at service position because closed stow geometry remains hardware-dependent.
    stay_fixed_y = hinge_y - float(stays["fixed_mount_forward_from_hinge_mm"])
    stay_fixed_z = hinge_z - float(stays["fixed_mount_below_hinge_mm"])
    stay_moving_local_y = hinge_local_y - float(stays["moving_mount_forward_from_hinge_mm"])
    stay_moving_local_z = float(stays["moving_mount_local_z_mm"])
    stay_r = float(stays["packaging_bar_diameter_mm"]) / 2.0
    for side, x in (("Left", 49.0), ("Right", outer - 49.0)):
        fixed = App.Vector(x, stay_fixed_y, stay_fixed_z)
        moving_closed = transform_point(x, stay_moving_local_y, stay_moving_local_z)
        moving_open = rotate_about_hinge(moving_closed, -open_deg, hinge_y, hinge_z)
        add_shape(doc, group, f"SafetyStayOpen{side}V18", f"{side.upper()} POSITIVE SAFETY STAY - OPEN",
                  cylinder_between(fixed, moving_open, stay_r), 5)

    # Closed-position structural landing pads aligned with the cabinet slope.
    psx, psy, psz = [float(v) for v in closed_support["pad_size_mm"]]
    pad_local_y = float(closed_support["pad_front_y_mm"]) - front_setback
    for idx, cx in enumerate(closed_support["pad_center_x_mm"], start=1):
        local = Part.makeBox(psx, psy, psz, App.Vector(float(cx)-psx/2.0, pad_local_y, -85.0))
        add_shape(doc, group, f"ClosedSupportPad{idx}V18", f"CLOSED STRUCTURAL SUPPORT PAD {idx}", transform_shape(local), 25)

    # Positive latch keepout envelopes - deliberately generic so the final local
    # latch can be selected without recutting the cradle.
    lsx, lsy, lsz = [float(v) for v in closed_support["latch_keepout_size_mm"]]
    latch_local_y = float(closed_support["latch_front_y_mm"]) - front_setback
    for idx, lx in enumerate(closed_support["latch_x_mm"], start=1):
        local = Part.makeBox(lsx, lsy, lsz, App.Vector(float(lx), latch_local_y, -115.0))
        add_shape(doc, group, f"ClosedLatchKeepout{idx}V18", f"POSITIVE CLOSED LATCH {idx} - KEEP-OUT", transform_shape(local), 78)

    # Moving power/video harness service-loop keepout at the right-rear pivot.
    hx, hy, hz = [float(v) for v in harness["keepout_box_mm"]]
    harness_local = Part.makeBox(
        hx, hy, hz,
        App.Vector(outer - wood - hx - 5.0, hinge_local_y - 65.0, -145.0),
    )
    add_shape(doc, group, "MovingHarnessKeepoutV18", "300 mm DISPLAY HARNESS LOOP / R50 KEEP-OUT", transform_shape(harness_local), 86)

    # Engineering readouts on the group.
    group.addProperty("App::PropertyAngle", "CabinetSlope", "Engineering")
    group.CabinetSlope = alpha_deg
    group.addProperty("App::PropertyLength", "HingeY", "Engineering")
    group.HingeY = hinge_y
    group.addProperty("App::PropertyLength", "HingeZ", "Engineering")
    group.HingeZ = hinge_z
    group.addProperty("App::PropertyLength", "FullThicknessDisplayBay", "Engineering")
    group.FullThicknessDisplayBay = inner
    group.addProperty("App::PropertyString", "DisplayPolicy", "Engineering")
    group.DisplayPolicy = "MODEL-AGNOSTIC 560x970x55 mm MAX; EXACT TV SELECTED LATE"
    group.addProperty("App::PropertyString", "GasStrutStatus", "Engineering")
    group.GasStrutStatus = "ASSIST ONLY; FORCE/MOUNTS TBD AFTER ACTUAL MASS+CG"
    group.addProperty("App::PropertyString", "SafetyStatus", "Engineering")
    group.SafetyStatus = "DUAL POSITIVE SAFETY STAYS + TWO POSITIVE CLOSED LATCHES REQUIRED"
    group.addProperty("App::PropertyString", "BearingHoleStatus", "Engineering")
    group.BearingHoleStatus = pivot["bearing_mount_holes_status"]
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    if owns_document:
        doc.save()

    print("PLAYFIELD MECHANICS v0.18 GENERATED")
    print("=" * 76)
    print(f"Cabinet / full inner      {outer:.1f} / {inner:.1f} mm")
    print(f"Display envelope          {display_w:.1f} x {display_l:.1f} x {display_d:.1f} mm")
    print(f"Cabinet slope             {alpha_deg:.3f} deg")
    print(f"Hinge axis Y/Z            {hinge_y:.1f} / {hinge_z:.1f} mm")
    print(f"Service opening           {open_deg:.1f} deg")
    print(f"Moving mass policy        {float(loads['moving_mass_design_kg']):.1f} kg")
    print("Safety                    2 positive stays + 2 closed latches")
    print("Gas struts                2 packaging ghosts; DO NOT BUY YET")
    print("Bearing holes             BLOCKED UNTIL PHYSICAL UCFL202 IS MEASURED")
    print("STATUS                     ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    if owns_document:
        App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

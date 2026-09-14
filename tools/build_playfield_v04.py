#!/usr/bin/env python3
"""Build the v0.4 LG C5 playfield service/hinge engineering model.

The generated objects are packaging/kinematic envelopes. They are intentionally
not manufacturing drawings. The physical OLED envelope, provisional cradle
rails, pivot axis, open-position ghost, and first-pass gas-strut lines are
created from documented JSON parameters.
"""

from __future__ import annotations

import json
import math
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
DESIGN = os.path.join(ROOT, "config/design.json")
PLAYFIELD = os.path.join(ROOT, "config/playfield_v04.json")


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def top_z(cab, y):
    run = cab["side_length_mm"] - cab["rear_top_flat_mm"]
    if y <= run:
        rise = cab["rear_height_mm"] - cab["front_height_mm"]
        return cab["front_height_mm"] + rise * (y / run)
    return cab["rear_height_mm"]


def add_shape(doc, group, name, label, shape, transparency=0):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    try:
        obj.ViewObject.Transparency = transparency
    except Exception:
        pass
    return obj


def cylinder_between(a, b, radius):
    vec = b.sub(a)
    if vec.Length <= 1e-6:
        raise RuntimeError("Cannot create zero-length cylinder")
    return Part.makeCylinder(radius, vec.Length, a, vec)


def main():
    d = load(DESIGN)
    p = load(PLAYFIELD)
    cab = d["cabinet"]
    oled = d["oled"]
    cradle = p["cradle"]
    svc = p["service"]
    gs = p["gas_strut_candidate"]

    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    doc = App.openDocument(MASTER)

    # Own only these generated groups/objects.
    old = doc.getObject("PlayfieldServiceV04")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "PlayfieldServiceV04")
    group.Label = "PLAYFIELD SERVICE v0.4 - PROVISIONAL"

    outer = cab["outer_width_mm"]
    tv_cross = oled["native_height_mm"]
    tv_long = oled["native_width_mm"]
    tv_depth = oled["max_depth_mm"]
    x0 = (outer - tv_cross) / 2.0
    y0 = p["oled_front_setback_mm"]

    slope_run = cab["side_length_mm"] - cab["rear_top_flat_mm"]
    slope_rise = cab["rear_height_mm"] - cab["front_height_mm"]
    alpha = math.atan2(slope_rise, slope_run)
    alpha_deg = math.degrees(alpha)
    open_deg = svc["relative_open_angle_deg"]

    # Put the upper TV face under the cabinet top by the reserved glass gap.
    # The local +Z thickness vector is rotated by the cabinet slope.
    z0 = (
        top_z(cab, y0)
        - p["glass_clearance_normal_mm"]
        - tv_depth * math.cos(alpha)
    )

    closed = Part.makeBox(tv_cross, tv_long, tv_depth, App.Vector(x0, 0, 0))
    closed.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
    closed.translate(App.Vector(0, y0, z0))
    closed_obj = add_shape(
        doc, group, "OLED42C5ClosedV04", "LG OLED42C5 - CLOSED", closed, 35
    )

    # Hinge point follows the playfield slope and sits behind the OLED rear.
    hinge_path = tv_long + cradle["hinge_offset_behind_oled_rear_mm"]
    hinge_y = y0 + hinge_path * math.cos(alpha)
    # Pivot is near the assembly mid-thickness, below the glass clearance plane.
    hinge_z = (
        top_z(cab, y0)
        + hinge_path * math.sin(alpha)
        - p["glass_clearance_normal_mm"]
        - 0.5 * tv_depth
    )

    hinge_radius = cradle["hinge_axis_diameter_mm"] / 2.0
    hinge_shape = Part.makeCylinder(
        hinge_radius,
        outer,
        App.Vector(0, hinge_y, hinge_z),
        App.Vector(1, 0, 0),
    )
    add_shape(doc, group, "PlayfieldHingeAxisV04", "PLAYFIELD HINGE AXIS", hinge_shape)

    # Open-position ghost: rotate the exact closed envelope around hinge axis.
    open_shape = closed.copy()
    open_shape.rotate(
        App.Vector(0, hinge_y, hinge_z),
        App.Vector(1, 0, 0),
        -open_deg,
    )
    open_obj = add_shape(
        doc, group, "OLED42C5OpenGhostV04", "LG OLED42C5 - 70deg SERVICE GHOST", open_shape, 75
    )

    # Provisional 20 mm cradle rails. They are packaging envelopes only; final
    # section/material/brackets depend on hardware availability and VESA offsets.
    rail = cradle["side_rail_section_mm"]
    cross = cradle["cross_rail_section_mm"]
    installed_cross = tv_cross + 2.0 * oled["clearance_each_side_mm"]
    rail_x_left = (outer - installed_cross) / 2.0
    rail_x_right = (outer + installed_cross) / 2.0 - rail
    rail_y0 = y0 - 5.0
    rail_len = tv_long + cradle["hinge_offset_behind_oled_rear_mm"] + 10.0
    rail_z0 = z0 - rail

    cradle_shapes = []
    for rx in (rail_x_left, rail_x_right):
        s = Part.makeBox(rail, rail_len, rail, App.Vector(rx, 0, 0))
        s.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
        s.translate(App.Vector(0, rail_y0, rail_z0))
        cradle_shapes.append(s)

    for local_y in (0.0, tv_long - cross):
        s = Part.makeBox(installed_cross, cross, cross, App.Vector(rail_x_left, local_y, 0))
        s.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
        s.translate(App.Vector(0, y0, rail_z0))
        cradle_shapes.append(s)

    cradle_closed = cradle_shapes[0]
    for s in cradle_shapes[1:]:
        cradle_closed = cradle_closed.fuse(s)
    add_shape(doc, group, "CradleEnvelopeClosedV04", "PROVISIONAL CRADLE - CLOSED", cradle_closed)

    cradle_open = cradle_closed.copy()
    cradle_open.rotate(
        App.Vector(0, hinge_y, hinge_z), App.Vector(1, 0, 0), -open_deg
    )
    add_shape(doc, group, "CradleEnvelopeOpenGhostV04", "PROVISIONAL CRADLE - OPEN GHOST", cradle_open, 75)

    # Gas-strut candidate in Y/Z plane, one on each side.
    moving_d = gs["moving_mount_forward_from_hinge_mm"]
    fixed_forward = gs["fixed_mount_forward_from_hinge_mm"]
    fixed_below = gs["fixed_mount_below_hinge_mm"]

    def moving_point(opened):
        phi = math.pi + alpha - (math.radians(open_deg) if opened else 0.0)
        return (
            hinge_y + moving_d * math.cos(phi),
            hinge_z + moving_d * math.sin(phi),
        )

    fixed_y = hinge_y - fixed_forward
    fixed_z = hinge_z - fixed_below
    my_c, mz_c = moving_point(False)
    my_o, mz_o = moving_point(True)

    for side, x in (("Left", 28.0), ("Right", outer - 28.0)):
        fixed_pt = App.Vector(x, fixed_y, fixed_z)
        moving_closed = App.Vector(x, my_c, mz_c)
        moving_open = App.Vector(x, my_o, mz_o)
        add_shape(
            doc,
            group,
            f"GasStrut{side}ClosedV04",
            f"{side.upper()} GAS STRUT - CLOSED CANDIDATE",
            cylinder_between(fixed_pt, moving_closed, 5.0),
        )
        add_shape(
            doc,
            group,
            f"GasStrut{side}OpenV04",
            f"{side.upper()} GAS STRUT - OPEN GHOST",
            cylinder_between(fixed_pt, moving_open, 5.0),
            70,
        )

    # Document-level readouts for quick inspection without trusting memory.
    group.addProperty("App::PropertyAngle", "CabinetSlope", "Engineering")
    group.CabinetSlope = alpha_deg
    group.addProperty("App::PropertyAngle", "RelativeOpenAngle", "Engineering")
    group.RelativeOpenAngle = open_deg
    group.addProperty("App::PropertyLength", "HingeY", "Engineering")
    group.HingeY = hinge_y
    group.addProperty("App::PropertyLength", "HingeZ", "Engineering")
    group.HingeZ = hinge_z
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "PROVISIONAL - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("PLAYFIELD SERVICE MODEL v0.4 GENERATED")
    print("=" * 64)
    print(f"Cabinet slope        {alpha_deg:.3f} deg")
    print(f"OLED front setback   {y0:.3f} mm")
    print(f"Hinge Y              {hinge_y:.3f} mm")
    print(f"Hinge Z              {hinge_z:.3f} mm")
    print(f"Service rotation     {open_deg:.3f} deg relative")
    print(f"Closed OLED bounds   X={closed_obj.Shape.BoundBox.XLength:.1f} "
          f"Y={closed_obj.Shape.BoundBox.YLength:.1f} Z={closed_obj.Shape.BoundBox.ZLength:.1f} mm")
    print(f"Open OLED bounds     X={open_obj.Shape.BoundBox.XLength:.1f} "
          f"Y={open_obj.Shape.BoundBox.YLength:.1f} Z={open_obj.Shape.BoundBox.ZLength:.1f} mm")
    print("STATUS               PROVISIONAL - visual/kinematic validation required")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

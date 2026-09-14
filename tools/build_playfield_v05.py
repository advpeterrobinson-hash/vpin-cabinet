#!/usr/bin/env python3
"""Build the v0.5 playfield sweep / safety engineering model.

v0.5 deliberately remains a packaging model. It adds a multi-angle OLED sweep,
a conservative backbox keepout, a positive mechanical safety-prop envelope,
a hinge reinforcement envelope, and a VESA adjustment zone without pretending
that bracket hole locations or purchased hardware are finalized.
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
V04 = os.path.join(ROOT, "config/playfield_v04.json")
V05 = os.path.join(ROOT, "config/playfield_v05.json")


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


def quantity_value(q):
    """Return the numeric value of a FreeCAD Quantity/property in document units."""
    return float(q.Value if hasattr(q, "Value") else q)


def main():
    d = load(DESIGN)
    p4 = load(V04)
    p5 = load(V05)
    cab = d["cabinet"]
    oled = d["oled"]
    cradle = p4["cradle"]
    svc = p4["service"]

    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    doc = App.openDocument(MASTER)
    v04 = doc.getObject("PlayfieldServiceV04")
    closed_obj = doc.getObject("OLED42C5ClosedV04")
    if v04 is None or closed_obj is None:
        raise RuntimeError(
            "v0.4 generated geometry is missing. Run build_playfield_v04_entry.py first."
        )

    old = doc.getObject("PlayfieldServiceV05")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "PlayfieldServiceV05")
    group.Label = "PLAYFIELD SERVICE v0.5 - SWEEP / SAFETY"

    outer = cab["outer_width_mm"]
    wood = cab["main_wood_nominal_mm"]
    inner = outer - 2.0 * wood
    tv_long = oled["native_width_mm"]
    tv_cross = oled["native_height_mm"]
    tv_depth = oled["max_depth_mm"]
    alpha_deg = quantity_value(v04.CabinetSlope)
    alpha = math.radians(alpha_deg)
    hinge_y = quantity_value(v04.HingeY)
    hinge_z = quantity_value(v04.HingeZ)
    open_deg = svc["relative_open_angle_deg"]
    y0 = p4["oled_front_setback_mm"]
    z0 = (
        top_z(cab, y0)
        - p4["glass_clearance_normal_mm"]
        - tv_depth * math.cos(alpha)
    )

    # Conservative backbox packaging envelope. The dimensions are from the
    # reference model; placement remains explicitly provisional until audited.
    bk = p5["backbox_keepout"]
    bk_x = 0.5 * (outer - bk["width_mm"])
    keepout_shape = Part.makeBox(
        bk["width_mm"],
        bk["depth_mm"],
        bk["height_mm"],
        App.Vector(bk_x, bk["front_y_mm"], bk["bottom_z_mm"]),
    )
    add_shape(
        doc,
        group,
        "BackboxKeepoutV05",
        "BACKBOX KEEPOUT - PROVISIONAL REFERENCE ENVELOPE",
        keepout_shape,
        88,
    )

    # Sweep the exact v0.4 closed OLED shape about the verified hinge axis.
    sweep_collision_volumes = []
    sweep_names = []
    for deg in p5["sweep"]["angles_deg"]:
        ghost = closed_obj.Shape.copy()
        ghost.rotate(
            App.Vector(0, hinge_y, hinge_z),
            App.Vector(1, 0, 0),
            -float(deg),
        )
        name = f"OLED42C5Sweep{int(deg):03d}V05"
        label = f"OLED SWEEP {int(deg):02d} deg"
        transparency = 78 if deg not in (0, open_deg) else 68
        obj = add_shape(doc, group, name, label, ghost, transparency)
        sweep_names.append(obj.Name)
        try:
            volume = ghost.common(keepout_shape).Volume
        except Exception:
            volume = float("inf")
        sweep_collision_volumes.append((float(deg), float(volume)))

    # Rear hinge reinforcement/crossmember packaging envelope. It occupies
    # full-thickness cabinet regions rather than the reduced OLED-pocket skin.
    refine = p5["cradle_refinement"]
    hy = refine["hinge_crossmember_y_mm"]
    hz = refine["hinge_crossmember_z_mm"]
    reinforcement = Part.makeBox(
        inner,
        hy,
        hz,
        App.Vector(wood, hinge_y - hy / 2.0, hinge_z - hz),
    )
    add_shape(
        doc,
        group,
        "HingeReinforcementEnvelopeV05",
        "HINGE REINFORCEMENT CROSSMEMBER - ENVELOPE",
        reinforcement,
        25,
    )

    # VESA adjustment zone: deliberately NOT a hole pattern. The exact VESA
    # centre location on the LG chassis must be measured/confirmed first.
    zone_w = refine["vesa_adjustment_zone_width_mm"]
    zone_l = refine["vesa_adjustment_zone_length_mm"]
    zone_t = refine["vesa_adjustment_zone_thickness_mm"]
    zone_x = 0.5 * (outer - zone_w)
    zone_local_y = 0.5 * (tv_long - zone_l)
    zone = Part.makeBox(
        zone_w,
        zone_l,
        zone_t,
        App.Vector(zone_x, zone_local_y, -zone_t),
    )
    zone.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
    zone.translate(App.Vector(0, y0, z0))
    add_shape(
        doc,
        group,
        "VESAAdjustmentZoneV05",
        "VESA ADJUSTMENT ZONE - NO HOLE LOCATIONS",
        zone,
        82,
    )

    # Independent positive mechanical safety prop at full-open service angle.
    sp = p5["safety_prop_candidate"]
    fixed_y = hinge_y - sp["fixed_mount_forward_from_hinge_mm"]
    fixed_z = hinge_z - sp["fixed_mount_below_hinge_mm"]
    phi_open = math.pi + alpha - math.radians(open_deg)
    moving_y = hinge_y + sp["moving_mount_forward_from_hinge_mm"] * math.cos(phi_open)
    moving_z = hinge_z + sp["moving_mount_forward_from_hinge_mm"] * math.sin(phi_open)
    x_prop = wood + 12.0
    fixed_pt = App.Vector(x_prop, fixed_y, fixed_z)
    moving_pt = App.Vector(x_prop, moving_y, moving_z)
    prop_vec = moving_pt.sub(fixed_pt)
    prop_length = prop_vec.Length
    prop_radius = 0.5 * sp["bar_envelope_diameter_mm"]
    prop_shape = cylinder_between(fixed_pt, moving_pt, prop_radius)
    add_shape(
        doc,
        group,
        "SafetyPropOpenV05",
        "POSITIVE SAFETY PROP - OPEN PACKAGING CANDIDATE",
        prop_shape,
        20,
    )

    # Simple captive-pin envelopes at both prop endpoints.
    pin_radius = 0.5 * sp["pin_diameter_mm"]
    for suffix, pt in (("Fixed", fixed_pt), ("Moving", moving_pt)):
        pin = Part.makeCylinder(
            pin_radius,
            24.0,
            App.Vector(wood, pt.y, pt.z),
            App.Vector(1, 0, 0),
        )
        add_shape(
            doc,
            group,
            f"SafetyProp{suffix}PinV05",
            f"SAFETY PROP {suffix.upper()} PIN ENVELOPE",
            pin,
            20,
        )

    collision_tol = p5["sweep"]["collision_volume_tolerance_mm3"]
    collisions = [
        (deg, vol) for deg, vol in sweep_collision_volumes if vol > collision_tol
    ]
    min_backbox_y_margin = min(
        bk["front_y_mm"] - doc.getObject(name).Shape.BoundBox.YMax
        for name in sweep_names
    )

    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "PROVISIONAL - NOT FOR MANUFACTURING"
    group.addProperty("App::PropertyString", "SweepCollisionStatus", "Engineering")
    group.SweepCollisionStatus = (
        "CLEAR against provisional backbox keepout"
        if not collisions
        else f"COLLISION at {', '.join(str(int(d)) for d, _ in collisions)} deg"
    )
    group.addProperty("App::PropertyLength", "MinimumBackboxYMargin", "Engineering")
    group.MinimumBackboxYMargin = max(0.0, min_backbox_y_margin)
    group.addProperty("App::PropertyLength", "SafetyPropLength", "Engineering")
    group.SafetyPropLength = prop_length
    group.addProperty("App::PropertyString", "GasStrutCandidates", "Engineering")
    group.GasStrutCandidates = ", ".join(
        f"{int(v)} N" for v in p5["gas_strut_force_candidates_n"]
    )
    group.addProperty("App::PropertyString", "PreferredNextStrutTest", "Engineering")
    group.PreferredNextStrutTest = (
        f"{int(p5['preferred_next_test_force_n'])} N each - analytical test only"
    )
    group.addProperty("App::PropertyString", "BackboxPlacementStatus", "Engineering")
    group.BackboxPlacementStatus = bk["status"]

    doc.recompute()
    doc.save()

    print("PLAYFIELD SERVICE MODEL v0.5 GENERATED")
    print("=" * 72)
    print(f"Sweep states                 {len(sweep_names)}")
    print(f"Hinge Y/Z                    {hinge_y:.1f} / {hinge_z:.1f} mm")
    print(f"Backbox keepout front Y      {bk['front_y_mm']:.1f} mm")
    print(f"Minimum sweep Y margin       {min_backbox_y_margin:.1f} mm")
    print(f"Safety prop endpoint length  {prop_length:.1f} mm")
    if collisions:
        print("Sweep collision              YES (provisional keepout)")
        for deg, vol in collisions:
            print(f"  {deg:.0f} deg -> {vol:.1f} mm^3")
    else:
        print("Sweep collision              none against provisional keepout")
    print("STATUS                       PROVISIONAL - visual validation required")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

"""Build the v0.4 hinged OLED/cradle engineering preview in FreeCAD.

Run with:
    freecadcmd tools/build_playfield_v04.py

This stage is deliberately a service-kinematics preview, not production CAD.
The OLED and cradle are shown closed/open, a hinge axis is rendered, and the
candidate dual gas-spring geometry is visualized. No production side pockets,
hinge brackets, safety-prop hardware, or VESA hole locations are cut here.
"""

from __future__ import annotations

import json
import math
import os
import pathlib
import sys

import FreeCAD as App
import Part

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from playfield_kinematics import analyze, closed_oled_corners, load_json, top_z

MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"
BASE_CONFIG = ROOT / "config" / "design.json"
PF_CONFIG = ROOT / "config" / "playfield_v04.json"

PREFIX = "PFV04_"
GROUP_NAME = "PlayfieldServiceV04"


def remove_owned_objects(doc: App.Document) -> None:
    # Remove generated children before their container. Reverse order is safer
    # for objects that may refer to each other.
    for obj in list(reversed(doc.Objects)):
        if obj.Name.startswith(PREFIX) or obj.Name == GROUP_NAME:
            try:
                doc.removeObject(obj.Name)
            except Exception:
                pass
    doc.recompute()


def set_view(obj, transparency=None, line_width=None) -> None:
    """Best-effort view properties; harmless under FreeCADCmd/headless."""
    try:
        if transparency is not None:
            obj.ViewObject.Transparency = int(transparency)
        if line_width is not None:
            obj.ViewObject.LineWidth = float(line_width)
    except Exception:
        pass


def feature(doc, group, name, label, shape, transparency=None):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    set_view(obj, transparency=transparency)
    return obj


def make_local_box(
    x: float,
    y: float,
    z: float,
    dx: float,
    dy: float,
    dz: float,
    placement: App.Placement,
):
    shape = Part.makeBox(dx, dy, dz, App.Vector(x, y, z))
    shape.Placement = placement
    return shape


def closed_placement(base: dict, pf: dict) -> tuple[App.Placement, dict]:
    oled = base["oled"]
    svc = pf["playfield"]
    cab = base["cabinet"]

    _, derived = closed_oled_corners(base, pf)
    theta = derived["slope_angle_deg"]
    theta_rad = math.radians(theta)

    x0 = (float(cab["outer_width_mm"]) - float(oled["native_height_mm"])) / 2.0
    origin = App.Vector(
        x0,
        derived["oled_back_origin_y_mm"],
        derived["oled_back_origin_z_mm"],
    )
    rotation = App.Rotation(App.Vector(1, 0, 0), theta)
    return App.Placement(origin, rotation), derived


def rotate_shape_about_hinge(shape: Part.Shape, hinge_y: float, hinge_z: float, angle_deg: float):
    out = shape.copy()
    out.rotate(App.Vector(0, hinge_y, hinge_z), App.Vector(1, 0, 0), -angle_deg)
    return out


def gas_points(base: dict, pf: dict, derived: dict, angle_deg: float):
    svc = pf["playfield"]
    gas = svc["gas_spring_candidate"]
    theta = math.radians(derived["slope_angle_deg"])
    phi = math.radians(angle_deg)
    moving_angle = theta - phi
    hy = derived["hinge_y_mm"]
    hz = derived["hinge_z_mm"]

    moving_r = float(gas["moving_mount_forward_of_hinge_mm"])
    moving_y = hy - moving_r * math.cos(moving_angle)
    moving_z = hz - moving_r * math.sin(moving_angle)

    fixed_y = hy - float(gas["fixed_mount_forward_of_hinge_mm"])
    fixed_z = hz - float(gas["fixed_mount_below_hinge_mm"])
    return (fixed_y, fixed_z), (moving_y, moving_z)


def cylinder_between(x: float, p1: tuple[float, float], p2: tuple[float, float], radius: float):
    start = App.Vector(x, p1[0], p1[1])
    end = App.Vector(x, p2[0], p2[1])
    direction = end.sub(start)
    length = direction.Length
    if length <= 0:
        raise RuntimeError("zero-length cylinder request")
    return Part.makeCylinder(radius, length, start, direction)


def sheet_set(sheet, row: int, alias: str, value: str, description: str) -> None:
    sheet.set(f"A{row}", alias)
    sheet.set(f"B{row}", value)
    sheet.set(f"C{row}", description)
    try:
        sheet.setAlias(f"B{row}", alias)
    except Exception:
        # Alias may already exist from a prior run; the cell value is still
        # refreshed and geometry remains rebuildable.
        pass


def main() -> int:
    if not MASTER.exists():
        raise FileNotFoundError(MASTER)

    base = load_json(BASE_CONFIG)
    pf = load_json(PF_CONFIG)
    rows, checks, report = analyze(base, pf)
    failed = [c for c in checks if not c.passed]
    if failed:
        print("Refusing to build v0.4 because kinematic checks failed:")
        for check in failed:
            print(f"  FAIL {check.name}: {check.value} ({check.requirement})")
        return 2

    doc = App.openDocument(str(MASTER))
    sheet = doc.getObject("Parameters")
    if sheet is None:
        raise RuntimeError("MASTER PARAMETERS spreadsheet not found")

    remove_owned_objects(doc)

    group = doc.addObject("App::Part", GROUP_NAME)
    group.Label = "PLAYFIELD SERVICE v0.4 - ENGINEERING PREVIEW"

    placement, derived = closed_placement(base, pf)
    cab = base["cabinet"]
    oled = base["oled"]
    svc = pf["playfield"]
    cradle = svc["cradle"]
    target_open = float(svc["target_open_angle_deg"])

    # ------------------------------------------------------------------
    # OLED closed/open envelopes
    # ------------------------------------------------------------------
    tv_local = Part.makeBox(
        float(oled["native_height_mm"]),
        float(oled["native_width_mm"]),
        float(oled["max_depth_mm"]),
    )
    tv_closed_shape = tv_local.copy()
    tv_closed_shape.Placement = placement
    tv_closed = feature(
        doc,
        group,
        PREFIX + "OLED_Closed",
        "LG OLED42C5 - CLOSED",
        tv_closed_shape,
        transparency=35,
    )

    tv_open_shape = rotate_shape_about_hinge(
        tv_closed_shape,
        derived["hinge_y_mm"],
        derived["hinge_z_mm"],
        target_open,
    )
    tv_open = feature(
        doc,
        group,
        PREFIX + "OLED_Open",
        f"LG OLED42C5 - SERVICE {target_open:.0f} deg",
        tv_open_shape,
        transparency=75,
    )

    # Intermediate swept-position ghosts help visual collision review.
    for angle in (20.0, 40.0, 60.0):
        if angle >= target_open:
            continue
        ghost_shape = rotate_shape_about_hinge(
            tv_closed_shape,
            derived["hinge_y_mm"],
            derived["hinge_z_mm"],
            angle,
        )
        feature(
            doc,
            group,
            PREFIX + f"OLED_Sweep_{int(angle):02d}",
            f"OLED SWEEP {angle:.0f} deg",
            ghost_shape,
            transparency=90,
        )

    # ------------------------------------------------------------------
    # Concept cradle: two 20x40 longitudinal rails plus VESA plate.
    # This is an envelope/architecture preview, not an extrusion cut list.
    # ------------------------------------------------------------------
    tv_cross = float(oled["native_height_mm"])
    rail_w = float(cradle["longitudinal_rail_width_mm"])
    rail_h = float(cradle["longitudinal_rail_height_mm"])
    rail_len = float(cradle["longitudinal_rail_length_mm"])
    rail_spacing = float(cradle["rail_center_spacing_mm"])
    rail_y = (float(oled["native_width_mm"]) - rail_len) / 2.0
    rail_z = -(rail_h + float(cradle["vesa_plate_thickness_mm"]))

    rail_centers = [tv_cross / 2.0 - rail_spacing / 2.0, tv_cross / 2.0 + rail_spacing / 2.0]
    rail_shapes = []
    for idx, center in enumerate(rail_centers, start=1):
        local_x = center - rail_w / 2.0
        shape = make_local_box(
            local_x,
            rail_y,
            rail_z,
            rail_w,
            rail_len,
            rail_h,
            placement,
        )
        rail_shapes.append(shape)
        feature(
            doc,
            group,
            PREFIX + f"CradleRail{idx}_Closed",
            f"CRADLE RAIL {idx} - CLOSED",
            shape,
            transparency=20,
        )
        feature(
            doc,
            group,
            PREFIX + f"CradleRail{idx}_Open",
            f"CRADLE RAIL {idx} - OPEN",
            rotate_shape_about_hinge(
                shape,
                derived["hinge_y_mm"],
                derived["hinge_z_mm"],
                target_open,
            ),
            transparency=80,
        )

    plate_w = float(cradle["vesa_plate_width_mm"])
    plate_len = float(cradle["vesa_plate_length_mm"])
    plate_t = float(cradle["vesa_plate_thickness_mm"])
    plate_x = (tv_cross - plate_w) / 2.0
    plate_y = float(cradle["vesa_center_from_oled_front_mm"]) - plate_len / 2.0
    plate_shape = make_local_box(
        plate_x,
        plate_y,
        -plate_t,
        plate_w,
        plate_len,
        plate_t,
        placement,
    )
    feature(
        doc,
        group,
        PREFIX + "VESAPLate_Closed",
        "VESA PLATE ENVELOPE - CLOSED (POSITION UNCONFIRMED)",
        plate_shape,
        transparency=35,
    )
    feature(
        doc,
        group,
        PREFIX + "VESAPlate_Open",
        "VESA PLATE ENVELOPE - OPEN",
        rotate_shape_about_hinge(
            plate_shape,
            derived["hinge_y_mm"],
            derived["hinge_z_mm"],
            target_open,
        ),
        transparency=80,
    )

    # ------------------------------------------------------------------
    # Hinge axis preview. Span only the full-strength cabinet interior.
    # ------------------------------------------------------------------
    wood = float(cab["main_wood_nominal_mm"])
    inner_w = float(cab["outer_width_mm"]) - 2.0 * wood
    shaft_d = float(cradle["hinge_shaft_diameter_preview_mm"])
    shaft_shape = Part.makeCylinder(
        shaft_d / 2.0,
        inner_w,
        App.Vector(wood, derived["hinge_y_mm"], derived["hinge_z_mm"]),
        App.Vector(1, 0, 0),
    )
    feature(
        doc,
        group,
        PREFIX + "HingeAxis",
        "HINGE AXIS PREVIEW - FULL-STRENGTH SUPPORT REQUIRED",
        shaft_shape,
    )

    # ------------------------------------------------------------------
    # Dual gas-spring centerline envelopes, closed and open.
    # Actual tube/rod diameters and end fittings remain hardware-dependent.
    # ------------------------------------------------------------------
    fixed_closed, moving_closed = gas_points(base, pf, derived, 0.0)
    fixed_open, moving_open = gas_points(base, pf, derived, target_open)
    gas_xs = [wood + 16.0, float(cab["outer_width_mm"]) - wood - 16.0]

    for side, x in zip(("L", "R"), gas_xs):
        feature(
            doc,
            group,
            PREFIX + f"Gas_{side}_Closed",
            f"GAS SPRING {side} - CLOSED CENTERLINE",
            cylinder_between(x, fixed_closed, moving_closed, 5.0),
            transparency=25,
        )
        feature(
            doc,
            group,
            PREFIX + f"Gas_{side}_Open",
            f"GAS SPRING {side} - OPEN CENTERLINE",
            cylinder_between(x, fixed_open, moving_open, 5.0),
            transparency=75,
        )

    # ------------------------------------------------------------------
    # Engineering report object for convenient inspection in FreeCAD.
    # ------------------------------------------------------------------
    eng = doc.addObject("App::FeaturePython", PREFIX + "EngineeringReport")
    eng.Label = "v0.4 ENGINEERING REPORT - NOT PURCHASE APPROVAL"
    group.addObject(eng)

    report_props = {
        "SlopeAngleDeg": report["slope_angle_deg"],
        "HingeYmm": report["hinge_y_mm"],
        "HingeZmm": report["hinge_z_mm"],
        "MovingMassEstimateKg": report["moving_mass_estimate_kg"],
        "GasCompressedLengthMm": report["gas_compressed_length_mm"],
        "GasMinSweepLengthMm": report["gas_min_sweep_length_mm"],
        "GasMaxSweepLengthMm": report["gas_max_sweep_length_mm"],
        "ClosedAssistRatio": report["closed_assist_ratio"],
        "OpenAssistRatio": report["open_assist_ratio"],
        "OpenOLEDMaxHeightMm": report["open_oled_max_height_mm"],
    }
    for prop, value in report_props.items():
        eng.addProperty("App::PropertyFloat", prop, "v0.4 Kinematics")
        setattr(eng, prop, float(value))

    eng.addProperty("App::PropertyString", "GasSpringStatus", "v0.4 Kinematics")
    eng.GasSpringStatus = svc["gas_spring_candidate"]["status"]
    eng.addProperty("App::PropertyString", "VESAStatus", "v0.4 Kinematics")
    eng.VESAStatus = "UNCONFIRMED - measure actual LG C5 before cradle fabrication"
    eng.addProperty("App::PropertyString", "SafetyPropStatus", "v0.4 Kinematics")
    eng.SafetyPropStatus = "REQUIRED - final hardware TBD"

    # ------------------------------------------------------------------
    # Render the most important v0.4 values into the master spreadsheet.
    # ------------------------------------------------------------------
    values = [
        (40, "PlayfieldSlopeAngle", f"{report['slope_angle_deg']:.6f} deg", "Derived Williams cabinet/playfield slope"),
        (41, "PlayfieldHingeY", f"{report['hinge_y_mm']:.3f} mm", "v0.4 hinge axis Y preview"),
        (42, "PlayfieldHingeZ", f"{report['hinge_z_mm']:.3f} mm", "v0.4 hinge axis Z preview"),
        (43, "CradleMassEstimate", f"{float(svc['cradle_mass_estimate_kg']):.3f} kg", "Concept cradle mass; measure before spring purchase"),
        (44, "MovingMassEstimate", f"{report['moving_mass_estimate_kg']:.3f} kg", "OLED plus concept cradle"),
        (45, "GasExtendedLength", f"{float(svc['gas_spring_candidate']['extended_length_mm']):.3f} mm", "Candidate dimensional class only"),
        (46, "GasStroke", f"{float(svc['gas_spring_candidate']['stroke_mm']):.3f} mm", "Candidate dimensional class only"),
        (47, "GasNominalF1", f"{float(svc['gas_spring_candidate']['nominal_extension_force_f1_n']):.3f} N", "Preliminary force for kinematic screening"),
        (48, "GasMinSweepLength", f"{report['gas_min_sweep_length_mm']:.3f} mm", "Minimum center distance over 0-target sweep"),
        (49, "GasMaxSweepLength", f"{report['gas_max_sweep_length_mm']:.3f} mm", "Maximum center distance over 0-target sweep"),
        (50, "GasClosedAssistRatio", f"{report['closed_assist_ratio']:.6f}", "<1 keeps closed position gravity-dominant"),
        (51, "GasOpenAssistRatio", f"{report['open_assist_ratio']:.6f}", ">1 assists holding service position"),
        (52, "OpenOLEDMaxHeight", f"{report['open_oled_max_height_mm']:.3f} mm", "Maximum OLED envelope Z at service angle"),
    ]
    for row_no, alias, value, desc in values:
        sheet_set(sheet, row_no, alias, value, desc)

    doc.recompute()

    solids = [tv_closed, tv_open]
    invalid = [o.Label for o in solids if o.Shape.isNull() or not o.Shape.isValid()]
    if invalid:
        print("Invalid v0.4 solids:", ", ".join(invalid))
        App.closeDocument(doc.Name)
        return 3

    doc.save()

    print("=" * 78)
    print("PLAYFIELD SERVICE v0.4 GENERATED")
    print("=" * 78)
    print(f"Slope angle:             {report['slope_angle_deg']:.3f} deg")
    print(f"Hinge axis:              Y={report['hinge_y_mm']:.1f} Z={report['hinge_z_mm']:.1f} mm")
    print(f"Moving mass estimate:    {report['moving_mass_estimate_kg']:.2f} kg")
    print(f"Gas sweep length:        {report['gas_min_sweep_length_mm']:.1f} .. {report['gas_max_sweep_length_mm']:.1f} mm")
    print(f"Closed assist ratio:     {report['closed_assist_ratio']:.3f}")
    print(f"Open assist ratio:       {report['open_assist_ratio']:.3f}")
    print(f"Open OLED max height:    {report['open_oled_max_height_mm']:.1f} mm")
    print()
    print("IMPORTANT:")
    print("- Gas spring is a kinematic candidate only; do not purchase yet.")
    print("- VESA center position must be measured/verified on the actual LG C5.")
    print("- Independent mechanical safety prop remains mandatory.")
    print("- No production cabinet pocket or hinge bracket is generated in v0.4.")
    print(f"Saved: {MASTER}")

    App.closeDocument(doc.Name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

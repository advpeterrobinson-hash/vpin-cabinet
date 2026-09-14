"""Apply LG's verified OLED42C5 mechanical drawing to the v0.4 preview.

This is a post-processing step after `build_playfield_v04.py`. It replaces the
provisional centered cradle rails/VESA plate with geometry driven by LG's 2025
OLED42C5 detail-dimension drawing and adds four VESA-hole markers.

It remains engineering-preview geometry: final hole diameter/thread engagement,
plate alloy/thickness, spacers and fasteners require the physical TV/manual.
"""

from __future__ import annotations

import pathlib
import sys

import FreeCAD as App
import Part

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from playfield_kinematics import load_json
from build_playfield_v04 import (
    MASTER,
    BASE_CONFIG,
    PF_CONFIG,
    PREFIX,
    closed_placement,
    feature,
    make_local_box,
    rotate_shape_about_hinge,
    sheet_set,
)

OWNED_NAMES = [
    PREFIX + "CradleRail1_Closed",
    PREFIX + "CradleRail1_Open",
    PREFIX + "CradleRail2_Closed",
    PREFIX + "CradleRail2_Open",
    PREFIX + "VESAPLate_Closed",
    PREFIX + "VESAPlate_Open",
    PREFIX + "VESAPlateVerified_Closed",
    PREFIX + "VESAPlateVerified_Open",
    PREFIX + "VESAHole1_Closed",
    PREFIX + "VESAHole2_Closed",
    PREFIX + "VESAHole3_Closed",
    PREFIX + "VESAHole4_Closed",
    PREFIX + "VESAHole1_Open",
    PREFIX + "VESAHole2_Open",
    PREFIX + "VESAHole3_Open",
    PREFIX + "VESAHole4_Open",
]


def remove_named(doc: App.Document) -> None:
    for name in OWNED_NAMES:
        obj = doc.getObject(name)
        if obj is not None:
            try:
                doc.removeObject(name)
            except Exception:
                pass
    doc.recompute()


def local_cylinder(x: float, y: float, z: float, radius: float, depth: float, placement):
    shape = Part.makeCylinder(
        radius,
        depth,
        App.Vector(x, y, z),
        App.Vector(0, 0, 1),
    )
    shape.Placement = placement
    return shape


def main() -> int:
    if not MASTER.exists():
        raise FileNotFoundError(MASTER)

    base = load_json(BASE_CONFIG)
    pf = load_json(PF_CONFIG)
    svc = pf["playfield"]
    mech = svc["lg_c5_mechanical_drawing"]
    cradle = svc["cradle"]
    orientation = svc["oled_orientation"]

    if not cradle.get("vesa_center_position_confirmed", False):
        raise RuntimeError("Refusing verified VESA pass: config is not marked confirmed")
    if mech.get("status") != "verified-from-LG-2025-detail-dimension-drawing":
        raise RuntimeError("LG mechanical-drawing source is not marked verified")

    # The current selected orientation is explicit. If we later flip the OLED
    # across cabinet X, the offsets are mirrored rather than guessed.
    native_top_to_left = orientation["native_top_edge_maps_to"] == "cabinet_left"
    native_left_to_front = orientation["native_left_edge_maps_to"] == "cabinet_front"

    oled_h = float(base["oled"]["native_height_mm"])
    oled_w = float(base["oled"]["native_width_mm"])
    top_off = float(mech["vesa_top_offset_mm"])
    bottom_off = float(mech["vesa_bottom_offset_mm"])
    left_off = float(mech["vesa_left_offset_mm"])
    right_off = float(mech["vesa_right_offset_mm"])
    vesa_x = float(mech["vesa_horizontal_mm"])
    vesa_y = float(mech["vesa_vertical_mm"])

    if native_top_to_left:
        column_1_x = top_off
        column_2_x = top_off + vesa_y
    else:
        column_1_x = oled_h - top_off
        column_2_x = oled_h - (top_off + vesa_y)
        column_1_x, column_2_x = sorted((column_1_x, column_2_x))

    if native_left_to_front:
        row_1_y = left_off
        row_2_y = left_off + vesa_x
    else:
        row_1_y = oled_w - left_off
        row_2_y = oled_w - (left_off + vesa_x)
        row_1_y, row_2_y = sorted((row_1_y, row_2_y))

    center_x = (column_1_x + column_2_x) / 2.0
    center_y = (row_1_y + row_2_y) / 2.0

    # Drawing dimensions are whole-millimetre rounded. Validate internal
    # consistency loosely rather than forcing the rounded top/bottom sum to the
    # published 540.0 mm chassis dimension.
    if abs((left_off + vesa_x + right_off) - oled_w) > 1.0:
        raise RuntimeError("LG horizontal VESA offsets do not reconcile with OLED width")
    if abs((top_off + vesa_y + bottom_off) - oled_h) > 1.5:
        raise RuntimeError("LG vertical VESA offsets do not reconcile with OLED height")

    doc = App.openDocument(str(MASTER))
    group = doc.getObject("PlayfieldServiceV04")
    sheet = doc.getObject("Parameters")
    if group is None:
        raise RuntimeError("Run build_playfield_v04.py before this post-processor")
    if sheet is None:
        raise RuntimeError("MASTER PARAMETERS spreadsheet not found")

    remove_named(doc)
    placement, derived = closed_placement(base, pf)
    target_open = float(svc["target_open_angle_deg"])

    rail_w = float(cradle["longitudinal_rail_width_mm"])
    rail_h = float(cradle["longitudinal_rail_height_mm"])
    rail_len = float(cradle["longitudinal_rail_length_mm"])
    plate_t = float(cradle["vesa_plate_thickness_mm"])
    rail_y = (oled_w - rail_len) / 2.0
    rail_z = -(rail_h + plate_t)

    # Follow the verified VESA columns rather than the OLED physical center.
    for idx, center in enumerate((column_1_x, column_2_x), start=1):
        shape = make_local_box(
            center - rail_w / 2.0,
            rail_y,
            rail_z,
            rail_w,
            rail_len,
            rail_h,
            placement,
        )
        feature(
            doc,
            group,
            PREFIX + f"CradleRail{idx}_Closed",
            f"CRADLE RAIL {idx} - VERIFIED VESA COLUMN",
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
    plate_x = center_x - plate_w / 2.0
    plate_y = center_y - plate_len / 2.0
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
        PREFIX + "VESAPlateVerified_Closed",
        "VESA PLATE - LG DRAWING VERIFIED POSITION",
        plate_shape,
        transparency=35,
    )
    feature(
        doc,
        group,
        PREFIX + "VESAPlateVerified_Open",
        "VESA PLATE - OPEN",
        rotate_shape_about_hinge(
            plate_shape,
            derived["hinge_y_mm"],
            derived["hinge_z_mm"],
            target_open,
        ),
        transparency=80,
    )

    # Mark the four VESA axes. Radius is intentionally only a visual marker;
    # do not treat this as final drill diameter.
    hole_points = [
        (column_1_x, row_1_y),
        (column_2_x, row_1_y),
        (column_1_x, row_2_y),
        (column_2_x, row_2_y),
    ]
    marker_radius = 4.0
    marker_depth = plate_t + 12.0
    marker_z = -plate_t - 6.0

    for idx, (hx, hy) in enumerate(hole_points, start=1):
        closed_shape = local_cylinder(
            hx,
            hy,
            marker_z,
            marker_radius,
            marker_depth,
            placement,
        )
        feature(
            doc,
            group,
            PREFIX + f"VESAHole{idx}_Closed",
            f"VESA AXIS {idx} - LG VERIFIED",
            closed_shape,
            transparency=10,
        )
        feature(
            doc,
            group,
            PREFIX + f"VESAHole{idx}_Open",
            f"VESA AXIS {idx} - OPEN",
            rotate_shape_about_hinge(
                closed_shape,
                derived["hinge_y_mm"],
                derived["hinge_z_mm"],
                target_open,
            ),
            transparency=80,
        )

    eng = doc.getObject(PREFIX + "EngineeringReport")
    if eng is not None and hasattr(eng, "VESAStatus"):
        eng.VESAStatus = (
            "LG 2025 detail drawing verified: 300x200; offsets "
            "K=316, L=134, M=207 mm. Physical-TV verification still required before machining."
        )

    rows = [
        (53, "LGVESAColumn1X", f"{column_1_x:.3f} mm", "Cabinet-local X of first verified VESA column"),
        (54, "LGVESAColumn2X", f"{column_2_x:.3f} mm", "Cabinet-local X of second verified VESA column"),
        (55, "LGVESARow1Y", f"{row_1_y:.3f} mm", "OLED-local Y from front/native-left edge"),
        (56, "LGVESARow2Y", f"{row_2_y:.3f} mm", "OLED-local Y from front/native-left edge"),
        (57, "LGVESACenterX", f"{center_x:.3f} mm", "Verified drawing center across OLED for selected orientation"),
        (58, "LGVESACenterY", f"{center_y:.3f} mm", "Verified drawing center along OLED"),
    ]
    for row_no, alias, value, desc in rows:
        sheet_set(sheet, row_no, alias, value, desc)

    doc.recompute()
    doc.save()

    print("=" * 78)
    print("LG OLED42C5 MECHANICAL DRAWING APPLIED")
    print("=" * 78)
    print(f"Selected orientation: native top -> {orientation['native_top_edge_maps_to']}")
    print(f"                      native left -> {orientation['native_left_edge_maps_to']}")
    print(f"VESA columns X:       {column_1_x:.1f}, {column_2_x:.1f} mm")
    print(f"VESA rows Y:          {row_1_y:.1f}, {row_2_y:.1f} mm")
    print(f"VESA center:          X={center_x:.1f}, Y={center_y:.1f} mm")
    print("Source: https://www.lge.co.kr/kr/tv/tv_size_2025.pdf (OLED42C5)")
    print("NOTE: physical-TV check remains mandatory before drilling the final plate.")

    App.closeDocument(doc.Name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

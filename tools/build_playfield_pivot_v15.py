#!/usr/bin/env python3
"""Build v0.15 playfield pivot plate/journal packaging in FreeCAD.

This creates engineering solids and keep-outs only. It does not authorize CNC
production, bearing-hole drilling, gas-strut purchase, or final journal welding.
"""
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/playfield_pivot_v15.json")

# Current validated playfield service-axis datum from v0.4/v0.5 packaging.
HINGE_Y_MM = 996.981
HINGE_Z_MM = 541.621
CAB_OUTER_W_MM = 580.0
CAB_WOOD_MM = 18.0


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


def plate_shape(length_y: float, height_z: float, thick_x: float, pivot_y_local: float,
                pivot_z_local: float, mount_y_from_rear: list[float], mount_z: list[float],
                left: bool):
    # Global rear edge of plate is +Y. Pivot is `pivot_y_local` forward from rear.
    rear_y = HINGE_Y_MM + pivot_y_local
    y0 = rear_y - length_y
    z0 = HINGE_Z_MM - pivot_z_local
    x0 = CAB_WOOD_MM if left else CAB_OUTER_W_MM - CAB_WOOD_MM - thick_x

    base = Part.makeBox(thick_x, length_y, height_z, App.Vector(x0, y0, z0))

    # Candidate 15.2 mm journal fit hole through the plate, along X.
    pivot_hole = Part.makeCylinder(
        7.6,
        thick_x + 2.0,
        App.Vector(x0 - 1.0 if left else x0 - 1.0, HINGE_Y_MM, HINGE_Z_MM),
        App.Vector(1, 0, 0),
    )
    result = base.cut(pivot_hole)

    # Four M8 clearance holes. Values in config are distances forward from the rear edge.
    for y_off in mount_y_from_rear:
        gy = rear_y - y_off
        for z_off in mount_z:
            gz = z0 + z_off
            hole = Part.makeCylinder(
                4.5,
                thick_x + 2.0,
                App.Vector(x0 - 1.0, gy, gz),
                App.Vector(1, 0, 0),
            )
            result = result.cut(hole)

    return result, (x0, y0, z0, rear_y)


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    cfg = load(CFG)
    plate = cfg["cradle_pivot_plate"]
    back = cfg["cradle_pivot_backing_plate"]
    journal = cfg["pivot_journal"]
    bearing = cfg["cabinet_side_bearing"]

    doc = App.openDocument(MASTER)

    old = doc.getObject("PlayfieldPivotV15")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "PlayfieldPivotV15")
    group.Label = "PLAYFIELD PIVOT v0.15 - 6 mm STEEL PLATES / SHORT JOURNALS"

    ly = float(plate["overall_length_y_mm"])
    hz = float(plate["overall_height_z_mm"])
    tx = float(plate["thickness_mm"])
    py = float(plate["pivot_axis_from_rear_plate_edge_mm"])
    pz = float(plate["pivot_axis_from_bottom_plate_edge_mm"])
    my = [float(v) for v in plate["plywood_mount_hole_centers_y_mm"]]
    mz = [float(v) for v in plate["plywood_mount_hole_centers_z_mm"]]

    left_shape, left_dims = plate_shape(ly, hz, tx, py, pz, my, mz, True)
    right_shape, right_dims = plate_shape(ly, hz, tx, py, pz, my, mz, False)
    add_shape(doc, group, "PlayfieldPivotPlateLeftV15",
              "PF-PIVOT-PLATE-001L-R1 - 6 mm STEEL", left_shape, 15,
              "PF-PIVOT-PLATE-001L-R1")
    add_shape(doc, group, "PlayfieldPivotPlateRightV15",
              "PF-PIVOT-PLATE-001R-R1 - 6 mm STEEL", right_shape, 15,
              "PF-PIVOT-PLATE-001R-R1")

    # 3 mm spreader plates are packaging solids, centered over the four M8 holes.
    bl = float(back["overall_length_y_mm"])
    bh = float(back["overall_height_z_mm"])
    bt = float(back["thickness_mm"])
    rear_y = HINGE_Y_MM + py
    mount_y_vals = [rear_y - v for v in my]
    mount_z_vals = [HINGE_Z_MM - pz + v for v in mz]
    by0 = (min(mount_y_vals) + max(mount_y_vals)) / 2.0 - bl / 2.0
    bz0 = (min(mount_z_vals) + max(mount_z_vals)) / 2.0 - bh / 2.0
    left_back = Part.makeBox(bt, bl, bh, App.Vector(CAB_WOOD_MM + tx, by0, bz0))
    right_back = Part.makeBox(bt, bl, bh, App.Vector(CAB_OUTER_W_MM - CAB_WOOD_MM - tx - bt, by0, bz0))
    add_shape(doc, group, "PlayfieldPivotBackingLeftV15", "PF-PIVOT-BACK-001L-R1 - 3 mm SPREADER", left_back, 35, "PF-PIVOT-BACK-001L-R1")
    add_shape(doc, group, "PlayfieldPivotBackingRightV15", "PF-PIVOT-BACK-001R-R1 - 3 mm SPREADER", right_back, 35, "PF-PIVOT-BACK-001R-R1")

    # Short 15 mm journals point outward through the cabinet side. Candidate
    # projection is deliberately longer than the side wall; final length follows
    # purchased bearing measurement.
    jr = float(journal["selected_nominal_diameter_mm"]) / 2.0
    jl = float(journal["journal_projection_from_plate_mm_candidate"])
    left_j = Part.makeCylinder(jr, jl, App.Vector(CAB_WOOD_MM, HINGE_Y_MM, HINGE_Z_MM), App.Vector(-1, 0, 0))
    right_j = Part.makeCylinder(jr, jl, App.Vector(CAB_OUTER_W_MM - CAB_WOOD_MM, HINGE_Y_MM, HINGE_Z_MM), App.Vector(1, 0, 0))
    add_shape(doc, group, "PlayfieldJournalLeftV15", "PF-PIVOT-JOURNAL-001L-R1 - 15 mm CANDIDATE", left_j, 20, "PF-PIVOT-JOURNAL-001L-R1")
    add_shape(doc, group, "PlayfieldJournalRightV15", "PF-PIVOT-JOURNAL-001R-R1 - 15 mm CANDIDATE", right_j, 20, "PF-PIVOT-JOURNAL-001R-R1")

    # Conservative UCFL202 packaging boxes only. Exact vendor housing dimensions
    # and mounting-hole centers must be measured before final side-panel drilling.
    bearing_depth_x = 35.0
    bearing_span_y = 120.0
    bearing_span_z = 75.0
    lb = Part.makeBox(
        bearing_depth_x, bearing_span_y, bearing_span_z,
        App.Vector(-bearing_depth_x, HINGE_Y_MM - bearing_span_y/2.0, HINGE_Z_MM - bearing_span_z/2.0),
    )
    rb = Part.makeBox(
        bearing_depth_x, bearing_span_y, bearing_span_z,
        App.Vector(CAB_OUTER_W_MM, HINGE_Y_MM - bearing_span_y/2.0, HINGE_Z_MM - bearing_span_z/2.0),
    )
    add_shape(doc, group, "UCFL202LeftKeepoutV15", "UCFL202 15 mm LEFT - MEASURE BEFORE CNC", lb, 82)
    add_shape(doc, group, "UCFL202RightKeepoutV15", "UCFL202 15 mm RIGHT - MEASURE BEFORE CNC", rb, 82)

    group.addProperty("App::PropertyString", "PivotPlateSpec", "Engineering")
    group.PivotPlateSpec = "A36/SAE1020 140x80x6 mm; 4x M8; R6"
    group.addProperty("App::PropertyString", "PreferredBearing", "Engineering")
    group.PreferredBearing = bearing["preferred_family"]
    group.addProperty("App::PropertyString", "BearingHoleStatus", "Engineering")
    group.BearingHoleStatus = "BLOCKED UNTIL PURCHASED UCFL202 PAIR IS MEASURED"
    group.addProperty("App::PropertyString", "SafetyStatus", "Engineering")
    group.SafetyStatus = "GAS STRUTS ASSIST ONLY; DUAL POSITIVE SAFETY STAYS REQUIRED"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("PLAYFIELD PIVOT v0.15 PACKAGING GENERATED")
    print("=" * 72)
    print(f"Hinge axis Y/Z           {HINGE_Y_MM:.3f} / {HINGE_Z_MM:.3f} mm")
    print(f"Pivot plate              {ly:.1f} x {hz:.1f} x {tx:.1f} mm")
    print(f"Journal candidate        {journal['selected_nominal_diameter_mm']} mm x {jl:.1f} mm projection")
    print(f"Preferred bearing        {bearing['preferred_family']}")
    print("Bearing mounting holes   TBD AFTER PHYSICAL PART MEASUREMENT")
    print("STATUS                   ENGINEERING PACKAGING - NOT FOR MANUFACTURING")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

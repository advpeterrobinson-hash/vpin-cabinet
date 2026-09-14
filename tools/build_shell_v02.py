import FreeCAD as App
import Part
import Sketcher
import os

project = os.path.expanduser("~/Projetos/vpin-cabinet")
path = os.path.join(project, "cad/master/vpin-master.FCStd")

doc = App.openDocument(path)

sheet = doc.getObject("Parameters")
if sheet is None:
    raise RuntimeError("MASTER PARAMETERS spreadsheet not found")


# ----------------------------------------------------------------------
# ADD WILLIAMS PROFILE PARAMETERS
# ----------------------------------------------------------------------

params = [
    (29, "CabFrontHeight",  "400.050 mm",
     "Williams cabinet front outside height"),

    (30, "CabRearHeight",   "=B6",
     "Williams cabinet rear outside height"),

    (31, "CabRearTopFlat",  "180.975 mm",
     "Horizontal rear section of cabinet top"),

    (32, "CabSlopeRun",     "=B5-B31",
     "Horizontal run of sloped cabinet top"),

    (33, "CabSlopeRise",    "=B30-B29",
     "Vertical rise of sloped cabinet top"),
]

for row, alias, value, description in params:
    sheet.set(f"A{row}", alias)
    sheet.set(f"B{row}", value)
    sheet.set(f"C{row}", description)

    try:
        sheet.setAlias(f"B{row}", alias)
    except Exception:
        pass

doc.recompute()


# ----------------------------------------------------------------------
# REMOVE OLD v0.1 SHELL
# ----------------------------------------------------------------------

names_to_remove = [
    "CabinetLeftPad",
    "CabinetLeftProfile",
    "CabinetLeftSide",

    "CabinetRightPad",
    "CabinetRightProfile",
    "CabinetRightSide",

    "CabinetFront",
    "CabinetRear",
    "CabinetBottom",

    "Shell",
]

for name in names_to_remove:
    obj = doc.getObject(name)
    if obj is not None:
        try:
            doc.removeObject(name)
        except Exception:
            pass

doc.recompute()


# ----------------------------------------------------------------------
# CREATE SHELL CONTAINER
# ----------------------------------------------------------------------

shell = doc.addObject("App::Part", "Shell")
shell.Label = "CABINET SHELL v0.2 - WILLIAMS WPC"


# ----------------------------------------------------------------------
# HELPER: PARAMETRIC SIDE BODY
# ----------------------------------------------------------------------

def create_side(body_name, label, x_offset_expression=None):

    body = doc.addObject("PartDesign::Body", body_name)
    body.Label = label
    shell.addObject(body)

    sketch_name = (
        "CabinetLeftProfile"
        if "Left" in body_name
        else "CabinetRightProfile"
    )

    pad_name = (
        "CabinetLeftPad"
        if "Left" in body_name
        else "CabinetRightPad"
    )

    sketch = doc.addObject("Sketcher::SketchObject", sketch_name)
    sketch.Label = f"{label} Profile"
    body.addObject(sketch)

    # Local sketch coordinates:
    #
    # X = cabinet front -> rear
    # Y = vertical
    #
    # Rotate sketch plane so:
    #
    # local X -> global Y
    # local Y -> global Z
    # pad normal -> global X
    #
    # Quaternion represents cyclic axis rotation:
    # X->Y, Y->Z, Z->X.
    sketch.Placement.Rotation = App.Rotation(
        0.5, 0.5, 0.5, 0.5
    )

    if x_offset_expression:
        sketch.setExpression(
            "Placement.Base.x",
            x_offset_expression
        )

    # Initial approximate geometry.
    # Constraints below drive the final dimensions.

    L = 1308.100
    HF = 400.050
    HR = 596.900
    RF = 180.975
    S = L - RF

    # 0 - bottom: front -> rear
    g0 = sketch.addGeometry(
        Part.LineSegment(
            App.Vector(0, 0, 0),
            App.Vector(L, 0, 0)
        ),
        False
    )

    # 1 - rear vertical
    g1 = sketch.addGeometry(
        Part.LineSegment(
            App.Vector(L, 0, 0),
            App.Vector(L, HR, 0)
        ),
        False
    )

    # 2 - rear horizontal top
    # Drawn slope-end -> rear so DistanceX is positive.
    g2 = sketch.addGeometry(
        Part.LineSegment(
            App.Vector(S, HR, 0),
            App.Vector(L, HR, 0)
        ),
        False
    )

    # 3 - sloped top: front top -> slope end
    g3 = sketch.addGeometry(
        Part.LineSegment(
            App.Vector(0, HF, 0),
            App.Vector(S, HR, 0)
        ),
        False
    )

    # 4 - front vertical
    g4 = sketch.addGeometry(
        Part.LineSegment(
            App.Vector(0, 0, 0),
            App.Vector(0, HF, 0)
        ),
        False
    )

    # Connectivity
    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g0, 2, g1, 1)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g1, 2, g2, 2)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g2, 1, g3, 2)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g3, 1, g4, 2)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g4, 1, g0, 1)
    )

    # Anchor front-bottom to sketch origin
    sketch.addConstraint(
        Sketcher.Constraint("Coincident", g0, 1, -1, 1)
    )

    # Geometric constraints
    sketch.addConstraint(
        Sketcher.Constraint("Horizontal", g0)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Vertical", g1)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Horizontal", g2)
    )

    sketch.addConstraint(
        Sketcher.Constraint("Vertical", g4)
    )

    # Dimensional constraints
    c_len = sketch.addConstraint(
        Sketcher.Constraint(
            "DistanceX",
            g0, 1,
            g0, 2,
            L
        )
    )

    c_rear_h = sketch.addConstraint(
        Sketcher.Constraint(
            "DistanceY",
            g1, 1,
            g1, 2,
            HR
        )
    )

    c_flat = sketch.addConstraint(
        Sketcher.Constraint(
            "DistanceX",
            g2, 1,
            g2, 2,
            RF
        )
    )

    c_front_h = sketch.addConstraint(
        Sketcher.Constraint(
            "DistanceY",
            g4, 1,
            g4, 2,
            HF
        )
    )

    # Connect dimensions directly to MASTER PARAMETERS
    sketch.setExpression(
        f"Constraints[{c_len}]",
        "Parameters.CabSideLength"
    )

    sketch.setExpression(
        f"Constraints[{c_rear_h}]",
        "Parameters.CabRearHeight"
    )

    sketch.setExpression(
        f"Constraints[{c_flat}]",
        "Parameters.CabRearTopFlat"
    )

    sketch.setExpression(
        f"Constraints[{c_front_h}]",
        "Parameters.CabFrontHeight"
    )

    doc.recompute()

    # Pad through plywood thickness
    pad = body.newObject("PartDesign::Pad", pad_name)
    pad.Label = f"{label} Pad"
    pad.Profile = sketch

    pad.setExpression(
        "Length",
        "Parameters.WoodMain"
    )

    pad.ReferenceAxis = (sketch, ["N_Axis"])
    pad.Midplane = False
    pad.Reversed = False

    doc.recompute()

    return body, sketch, pad


# ----------------------------------------------------------------------
# LEFT SIDE
# ----------------------------------------------------------------------

left_body, left_sketch, left_pad = create_side(
    "CabinetLeftSide",
    "Cabinet Left Side"
)


# ----------------------------------------------------------------------
# RIGHT SIDE
# ----------------------------------------------------------------------

right_body, right_sketch, right_pad = create_side(
    "CabinetRightSide",
    "Cabinet Right Side",
    "Parameters.CabOuterWidth - Parameters.WoodMain"
)


# ----------------------------------------------------------------------
# FRONT / REAR / BOTTOM
# ----------------------------------------------------------------------

def make_box(name, label):
    obj = doc.addObject("Part::Box", name)
    obj.Label = label
    shell.addObject(obj)
    return obj


front = make_box(
    "CabinetFront",
    "Cabinet Front"
)

front.setExpression(
    "Length",
    "Parameters.CabInnerWidth"
)
front.setExpression(
    "Width",
    "Parameters.WoodMain"
)
front.setExpression(
    "Height",
    "Parameters.CabFrontHeight"
)
front.setExpression(
    "Placement.Base.x",
    "Parameters.WoodMain"
)


rear = make_box(
    "CabinetRear",
    "Cabinet Rear"
)

rear.setExpression(
    "Length",
    "Parameters.CabInnerWidth"
)
rear.setExpression(
    "Width",
    "Parameters.WoodMain"
)
rear.setExpression(
    "Height",
    "Parameters.CabRearHeight"
)
rear.setExpression(
    "Placement.Base.x",
    "Parameters.WoodMain"
)
rear.setExpression(
    "Placement.Base.y",
    "Parameters.CabSideLength - Parameters.WoodMain"
)


bottom = make_box(
    "CabinetBottom",
    "Cabinet Bottom"
)

bottom.setExpression(
    "Length",
    "Parameters.CabInnerWidth"
)
bottom.setExpression(
    "Width",
    "Parameters.CabSideLength - 2 * Parameters.WoodMain"
)
bottom.setExpression(
    "Height",
    "Parameters.WoodMain"
)
bottom.setExpression(
    "Placement.Base.x",
    "Parameters.WoodMain"
)
bottom.setExpression(
    "Placement.Base.y",
    "Parameters.WoodMain"
)


# ----------------------------------------------------------------------
# FINISH
# ----------------------------------------------------------------------

doc.recompute()
doc.save()

print()
print("=" * 72)
print("WILLIAMS WPC PARAMETRIC SHELL v0.2")
print("=" * 72)

print(
    "Outside width:",
    sheet.get("CabOuterWidth")
)
print(
    "Inside width:",
    sheet.get("CabInnerWidth")
)
print(
    "Cabinet length:",
    sheet.get("CabSideLength")
)
print(
    "Front height:",
    sheet.get("CabFrontHeight")
)
print(
    "Rear height:",
    sheet.get("CabRearHeight")
)
print(
    "Rear top flat:",
    sheet.get("CabRearTopFlat")
)
print(
    "Slope run:",
    sheet.get("CabSlopeRun")
)
print(
    "Slope rise:",
    sheet.get("CabSlopeRise")
)

print()
print("LEFT SIDE BOUNDING BOX")
bb = left_pad.Shape.BoundBox
print(
    f"X={bb.XLength:.3f} "
    f"Y={bb.YLength:.3f} "
    f"Z={bb.ZLength:.3f}"
)

print()
print("RIGHT SIDE BOUNDING BOX")
bb = right_pad.Shape.BoundBox
print(
    f"X={bb.XLength:.3f} "
    f"Y={bb.YLength:.3f} "
    f"Z={bb.ZLength:.3f}"
)

print()
print("Saved:", path)

App.closeDocument(doc.Name)

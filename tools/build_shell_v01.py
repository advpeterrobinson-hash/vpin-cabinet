import FreeCAD as App
import os

project = os.path.expanduser("~/Projetos/vpin-cabinet")
path = os.path.join(project, "cad/master/vpin-master.FCStd")

doc = App.openDocument(path)

if doc.getObject("Parameters") is None:
    raise RuntimeError("MASTER PARAMETERS spreadsheet not found")

# Remove previous generated shell pieces.
for name in [
    "CabinetLeftSide",
    "CabinetRightSide",
    "CabinetFront",
    "CabinetRear",
    "CabinetBottom",
]:
    obj = doc.getObject(name)
    if obj:
        doc.removeObject(name)

shell = doc.getObject("Shell")
if shell:
    doc.removeObject("Shell")

doc.recompute()

shell = doc.addObject("App::Part", "Shell")
shell.Label = "CABINET SHELL v0.1 - PARAMETRIC"


def make_box(name, label):
    obj = doc.addObject("Part::Box", name)
    obj.Label = label
    shell.addObject(obj)
    return obj


# Coordinate convention:
#
# X = cabinet width, left -> right
# Y = cabinet length, front -> rear
# Z = vertical
#
# All geometry below is linked by expressions directly to the
# MASTER PARAMETERS spreadsheet.


# LEFT SIDE
left = make_box("CabinetLeftSide", "Cabinet Left Side")

left.setExpression(
    "Length",
    "Parameters.WoodMain"
)
left.setExpression(
    "Width",
    "Parameters.CabSideLength"
)
left.setExpression(
    "Height",
    "Parameters.CabSideHeightEnv"
)


# RIGHT SIDE
right = make_box("CabinetRightSide", "Cabinet Right Side")

right.setExpression(
    "Length",
    "Parameters.WoodMain"
)
right.setExpression(
    "Width",
    "Parameters.CabSideLength"
)
right.setExpression(
    "Height",
    "Parameters.CabSideHeightEnv"
)

right.setExpression(
    "Placement.Base.x",
    "Parameters.CabOuterWidth - Parameters.WoodMain"
)


# FRONT PANEL
front = make_box("CabinetFront", "Cabinet Front")

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
    "Parameters.CabSideHeightEnv"
)

front.setExpression(
    "Placement.Base.x",
    "Parameters.WoodMain"
)


# REAR PANEL
rear = make_box("CabinetRear", "Cabinet Rear")

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
    "Parameters.CabSideHeightEnv"
)

rear.setExpression(
    "Placement.Base.x",
    "Parameters.WoodMain"
)

rear.setExpression(
    "Placement.Base.y",
    "Parameters.CabSideLength - Parameters.WoodMain"
)


# BOTTOM
bottom = make_box("CabinetBottom", "Cabinet Bottom")

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


doc.recompute()
doc.save()

print()
print("PARAMETRIC SHELL CREATED")
print("------------------------")

for obj in [left, right, front, rear, bottom]:
    print(
        f"{obj.Label:22} "
        f"{obj.Length.Value:8.2f} x "
        f"{obj.Width.Value:8.2f} x "
        f"{obj.Height.Value:8.2f} mm"
    )

print()
print("Saved:", path)

App.closeDocument(doc.Name)

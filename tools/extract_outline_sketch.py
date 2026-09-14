import FreeCAD as App
import os

ref = os.path.expanduser(
    "~/Projetos/vpin-cabinet/.work/audit/reference-master.FCStd"
)

doc = App.openDocument(ref)

# Find the original cabinet-side outline sketch by label.
sketch = None
for obj in doc.Objects:
    if obj.Label == "Cab Left Outline":
        sketch = obj
        break

if sketch is None:
    raise RuntimeError("Cab Left Outline sketch not found")

print("=" * 90)
print("CAB LEFT OUTLINE")
print("=" * 90)
print("Name:", sketch.Name)
print("Label:", sketch.Label)
print("Type:", sketch.TypeId)
print("Geometry count:", sketch.GeometryCount)
print("MapMode:", getattr(sketch, "MapMode", None))
print("Placement:", sketch.Placement)
print()

try:
    gp = sketch.getGlobalPlacement()
except Exception:
    gp = sketch.Placement

def gv(p):
    """Transform a sketch-local point to document/global coordinates."""
    try:
        return gp.multVec(App.Vector(p.x, p.y, p.z))
    except Exception:
        return None

print("=" * 90)
print("GEOMETRY")
print("=" * 90)

for i, geo in enumerate(sketch.Geometry):
    construction = False
    try:
        construction = sketch.getConstruction(i)
    except Exception:
        pass

    print()
    print(f"Geometry {i}")
    print("  Type:", type(geo).__name__)
    print("  Construction:", construction)

    if hasattr(geo, "StartPoint"):
        p = geo.StartPoint
        pg = gv(p)
        print(
            "  Start local : "
            f"({p.x:.6f}, {p.y:.6f}, {p.z:.6f})"
        )
        if pg:
            print(
                "  Start global: "
                f"({pg.x:.6f}, {pg.y:.6f}, {pg.z:.6f})"
            )

    if hasattr(geo, "EndPoint"):
        p = geo.EndPoint
        pg = gv(p)
        print(
            "  End local   : "
            f"({p.x:.6f}, {p.y:.6f}, {p.z:.6f})"
        )
        if pg:
            print(
                "  End global  : "
                f"({pg.x:.6f}, {pg.y:.6f}, {pg.z:.6f})"
            )

    if hasattr(geo, "Center"):
        p = geo.Center
        pg = gv(p)
        print(
            "  Center local: "
            f"({p.x:.6f}, {p.y:.6f}, {p.z:.6f})"
        )
        if pg:
            print(
                "  Center global:"
                f" ({pg.x:.6f}, {pg.y:.6f}, {pg.z:.6f})"
            )

    if hasattr(geo, "Radius"):
        print("  Radius:", geo.Radius)

print()
print("=" * 90)
print("DIMENSIONAL CONSTRAINTS")
print("=" * 90)

for i, c in enumerate(sketch.Constraints):
    ctype = getattr(c, "Type", "")
    value = getattr(c, "Value", None)
    name = getattr(c, "Name", "")

    if ctype in (
        "Distance",
        "DistanceX",
        "DistanceY",
        "Radius",
        "Diameter",
        "Angle",
    ):
        print(
            f"{i:3d}: "
            f"{ctype:12} "
            f"value={value} "
            f"name={name!r} "
            f"first={getattr(c, 'First', None)} "
            f"firstPos={getattr(c, 'FirstPos', None)} "
            f"second={getattr(c, 'Second', None)} "
            f"secondPos={getattr(c, 'SecondPos', None)}"
        )

App.closeDocument(doc.Name)

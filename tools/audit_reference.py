import FreeCAD as App
import os

path = os.path.expanduser(
    "~/Projetos/vpin-cabinet/.work/audit/reference-master.FCStd"
)

doc = App.openDocument(path)

print("=" * 80)
print("DOCUMENT")
print("=" * 80)
print("Label:", doc.Label)
print("Objects:", len(doc.Objects))
print()

print("=" * 80)
print("TOP-LEVEL / GROUP STRUCTURE")
print("=" * 80)

def print_group(obj, indent=0, seen=None):
    if seen is None:
        seen = set()

    if obj.Name in seen:
        return

    seen.add(obj.Name)

    prefix = "  " * indent
    print(f"{prefix}- {obj.Label} [{obj.Name}] ({obj.TypeId})")

    if hasattr(obj, "Group"):
        for child in obj.Group:
            print_group(child, indent + 1, seen)

for obj in doc.Objects:
    parents = []
    if hasattr(obj, "InList"):
        parents = obj.InList

    if not parents:
        print_group(obj)

print()
print("=" * 80)
print("SPREADSHEETS")
print("=" * 80)

sheets = [o for o in doc.Objects if o.TypeId == "Spreadsheet::Sheet"]

if not sheets:
    print("No Spreadsheet::Sheet objects found.")
else:
    for sheet in sheets:
        print(f"{sheet.Label} [{sheet.Name}]")

print()
print("=" * 80)
print("OBJECTS WITH USEFUL DIMENSION-LIKE PROPERTIES")
print("=" * 80)

wanted = {
    "Length",
    "Width",
    "Height",
    "Thickness",
    "Diameter",
    "Radius",
    "Size",
}

for obj in doc.Objects:
    found = []
    for prop in obj.PropertiesList:
        if prop in wanted or any(
            word.lower() in prop.lower()
            for word in ("length", "width", "height", "thick")
        ):
            try:
                value = getattr(obj, prop)
                found.append(f"{prop}={value}")
            except Exception:
                pass

    if found:
        print(f"\n{obj.Label} [{obj.Name}] ({obj.TypeId})")
        for item in found:
            print("   ", item)

print()
print("=" * 80)
print("SHAPE BOUNDING BOXES")
print("=" * 80)

for obj in doc.Objects:
    try:
        shape = obj.Shape
        if shape.isNull():
            continue

        bb = shape.BoundBox

        if bb.XLength > 0 and bb.YLength > 0 and bb.ZLength > 0:
            print(
                f"{obj.Label:40} "
                f"X={bb.XLength:9.2f} "
                f"Y={bb.YLength:9.2f} "
                f"Z={bb.ZLength:9.2f} mm"
            )
    except Exception:
        pass

App.closeDocument(doc.Name)

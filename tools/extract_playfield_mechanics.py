import FreeCAD as App
import os

ref = os.path.expanduser(
    "~/Projetos/vpin-cabinet/.work/audit/reference-master.FCStd"
)

doc = App.openDocument(ref)


def find_label(label):
    for obj in doc.Objects:
        if obj.Label == label:
            return obj
    return None


def transformed_bounds(obj):
    try:
        gp = obj.getGlobalPlacement()
    except Exception:
        gp = obj.Placement

    pts = []

    try:
        for v in obj.Shape.Vertexes:
            pts.append(gp.multVec(v.Point))
    except Exception:
        return None

    if not pts:
        return None

    return {
        "xmin": min(p.x for p in pts),
        "xmax": max(p.x for p in pts),
        "ymin": min(p.y for p in pts),
        "ymax": max(p.y for p in pts),
        "zmin": min(p.z for p in pts),
        "zmax": max(p.z for p in pts),
    }


def dump_object(label):
    obj = find_label(label)

    print()
    print("=" * 90)
    print(label)
    print("=" * 90)

    if obj is None:
        print("NOT FOUND")
        return

    print("Name:", obj.Name)
    print("Type:", obj.TypeId)
    print("Placement:", obj.Placement)

    try:
        print("Global placement:", obj.getGlobalPlacement())
    except Exception:
        pass

    print()
    print("SELECTED PROPERTIES")

    interesting = (
        "Length",
        "Length2",
        "Type",
        "Reversed",
        "Midplane",
        "Offset",
        "Angle",
        "Profile",
        "UpToFace",
    )

    for prop in obj.PropertiesList:
        if prop in interesting or any(
            key in prop.lower()
            for key in (
                "length",
                "depth",
                "angle",
                "reverse",
                "midplane",
            )
        ):
            try:
                print(f"{prop:30} = {getattr(obj, prop)}")
            except Exception:
                pass

    try:
        bb = obj.Shape.BoundBox
        print()
        print("LOCAL SHAPE BOUNDS")
        print(
            f"X {bb.XMin:.3f} -> {bb.XMax:.3f} "
            f"({bb.XLength:.3f})"
        )
        print(
            f"Y {bb.YMin:.3f} -> {bb.YMax:.3f} "
            f"({bb.YLength:.3f})"
        )
        print(
            f"Z {bb.ZMin:.3f} -> {bb.ZMax:.3f} "
            f"({bb.ZLength:.3f})"
        )
    except Exception:
        pass

    tb = transformed_bounds(obj)

    if tb:
        print()
        print("GLOBAL VERTEX BOUNDS")
        print(
            f"X {tb['xmin']:.3f} -> {tb['xmax']:.3f} "
            f"({tb['xmax'] - tb['xmin']:.3f})"
        )
        print(
            f"Y {tb['ymin']:.3f} -> {tb['ymax']:.3f} "
            f"({tb['ymax'] - tb['ymin']:.3f})"
        )
        print(
            f"Z {tb['zmin']:.3f} -> {tb['zmax']:.3f} "
            f"({tb['zmax'] - tb['zmin']:.3f})"
        )


for label in (
    "Pocket189",
    "Playfield TV",
    "Playfield TV Mount",
    "Playfield Mount",
    "Playfield Mount - Left Support",
    "Playfield Mount - Left Stop Block",
    "Playfield Rear Channel",
    "Cabinet Left Side",
    "Cabinet Right Side",
):
    dump_object(label)


print()
print("=" * 90)
print("OBJECTS NEAR PLAYFIELD PIVOT / MOUNT")
print("=" * 90)

for obj in doc.Objects:
    text = obj.Label.lower()

    if any(
        key in text
        for key in (
            "pivot",
            "playfield mount",
            "rear channel",
            "stop block",
        )
    ):
        print(
            f"{obj.Label:50} "
            f"[{obj.Name}] "
            f"{obj.TypeId}"
        )

App.closeDocument(doc.Name)

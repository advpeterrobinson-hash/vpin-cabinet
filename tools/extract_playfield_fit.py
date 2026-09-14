import FreeCAD as App
import os

ref = os.path.expanduser(
    "~/Projetos/vpin-cabinet/.work/audit/reference-master.FCStd"
)

doc = App.openDocument(ref)


def show_object(label):
    print()
    print("=" * 90)
    print(label)
    print("=" * 90)

    objs = [o for o in doc.Objects if o.Label == label]

    if not objs:
        print("NOT FOUND")
        return None

    obj = objs[0]

    print("Name:", obj.Name)
    print("Type:", obj.TypeId)
    print("Placement:", obj.Placement)

    try:
        gp = obj.getGlobalPlacement()
        print("Global placement:", gp)
    except Exception:
        pass

    try:
        bb = obj.Shape.BoundBox

        print()
        print("BOUNDING BOX")
        print(f"XMin = {bb.XMin:.3f}")
        print(f"XMax = {bb.XMax:.3f}")
        print(f"XLen = {bb.XLength:.3f}")

        print(f"YMin = {bb.YMin:.3f}")
        print(f"YMax = {bb.YMax:.3f}")
        print(f"YLen = {bb.YLength:.3f}")

        print(f"ZMin = {bb.ZMin:.3f}")
        print(f"ZMax = {bb.ZMax:.3f}")
        print(f"ZLen = {bb.ZLength:.3f}")
    except Exception as e:
        print("No usable shape:", e)

    return obj


tv = show_object("Playfield TV")
mount = show_object("Playfield TV Mount")
pocket = show_object("Cab Left Monitor Pocket")


print()
print("=" * 90)
print("MONITOR POCKET SKETCH GEOMETRY")
print("=" * 90)

if pocket is not None and hasattr(pocket, "Geometry"):

    try:
        gp = pocket.getGlobalPlacement()
    except Exception:
        gp = pocket.Placement

    for i, geo in enumerate(pocket.Geometry):

        try:
            construction = pocket.getConstruction(i)
        except Exception:
            construction = False

        print()
        print(f"Geometry {i}: {type(geo).__name__}")
        print(" Construction:", construction)

        if hasattr(geo, "StartPoint"):
            p = geo.StartPoint
            pg = gp.multVec(
                App.Vector(p.x, p.y, p.z)
            )

            print(
                " Start local : "
                f"({p.x:.3f}, {p.y:.3f}, {p.z:.3f})"
            )
            print(
                " Start global: "
                f"({pg.x:.3f}, {pg.y:.3f}, {pg.z:.3f})"
            )

        if hasattr(geo, "EndPoint"):
            p = geo.EndPoint
            pg = gp.multVec(
                App.Vector(p.x, p.y, p.z)
            )

            print(
                " End local   : "
                f"({p.x:.3f}, {p.y:.3f}, {p.z:.3f})"
            )
            print(
                " End global  : "
                f"({pg.x:.3f}, {pg.y:.3f}, {pg.z:.3f})"
            )


print()
print("=" * 90)
print("POCKET / TV / PLAYFIELD RELATED OBJECTS")
print("=" * 90)

for obj in doc.Objects:
    text = obj.Label.lower()

    if any(
        key in text
        for key in (
            "playfield tv",
            "monitor pocket",
            "playfield mount",
            "playfield rear",
            "playfield front",
        )
    ):
        print(
            f"{obj.Label:45} "
            f"[{obj.Name}] "
            f"{obj.TypeId}"
        )

App.closeDocument(doc.Name)

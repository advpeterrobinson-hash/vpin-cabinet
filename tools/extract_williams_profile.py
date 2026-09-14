import FreeCAD as App
import os

ref = os.path.expanduser(
    "~/Projetos/vpin-cabinet/.work/audit/reference-master.FCStd"
)

doc = App.openDocument(ref)

print("=" * 80)
print("CABINET LEFT SIDE OBJECTS")
print("=" * 80)

# Show everything that looks relevant first.
for obj in doc.Objects:
    text = f"{obj.Label} {obj.Name}".lower()
    if "cabinet left" in text or "cab left" in text:
        print(
            f"{obj.Label:45} "
            f"[{obj.Name}] "
            f"{obj.TypeId}"
        )

print()
print("=" * 80)
print("SKETCHES INSIDE CABINET LEFT SIDE BODY")
print("=" * 80)

body = None

for obj in doc.Objects:
    if obj.Label == "Cabinet Left Side":
        body = obj
        break

if body is None:
    raise RuntimeError("Could not find Cabinet Left Side body")

for child in body.Group:
    print(
        f"{child.Label:45} "
        f"[{child.Name}] "
        f"{child.TypeId}"
    )

print()
print("=" * 80)
print("SIDE BODY BOUNDING BOX")
print("=" * 80)

bb = body.Shape.BoundBox

print("X:", bb.XLength)
print("Y:", bb.YLength)
print("Z:", bb.ZLength)

print()
print("=" * 80)
print("LARGEST PLANAR SIDE FACES")
print("=" * 80)

faces = []

for i, face in enumerate(body.Shape.Faces, start=1):
    try:
        area = face.Area
        center = face.CenterOfMass
        faces.append((area, i, center, face))
    except Exception:
        pass

faces.sort(reverse=True, key=lambda x: x[0])

for area, i, center, face in faces[:10]:
    print(
        f"Face {i:3d}: "
        f"Area={area:12.2f} mm²  "
        f"COM=({center.x:8.2f}, "
        f"{center.y:8.2f}, "
        f"{center.z:8.2f})"
    )

print()
print("=" * 80)
print("UNIQUE Y/Z VERTICES OF LARGEST FACE")
print("=" * 80)

largest = faces[0][3]

points = []

for v in largest.Vertexes:
    p = v.Point

    yz = (
        round(p.y, 3),
        round(p.z, 3),
    )

    if yz not in points:
        points.append(yz)

points.sort()

for y, z in points:
    print(f"Y={y:10.3f}   Z={z:10.3f}")

App.closeDocument(doc.Name)

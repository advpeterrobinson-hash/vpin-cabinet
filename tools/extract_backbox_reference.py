#!/usr/bin/env python3
"""Extract the backbox assembly envelope from the local reference FreeCAD file.

The reference model uses rear-at-Y=0 and cabinet-front-at-negative-Y. The new
project uses front-at-Y=0 and rear-at-positive-Y, so this tool also emits the
converted project-coordinate envelope. Output is local/ignored under .work/.
"""

from __future__ import annotations

import json
import os

import FreeCAD as App

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
REFERENCE = os.path.join(ROOT, ".work/audit/reference-master.FCStd")
OUT = os.path.join(ROOT, ".work/audit/backbox-reference.json")
CAB_LENGTH = 1308.10


def iter_group(obj, seen=None):
    if seen is None:
        seen = set()
    if obj.Name in seen:
        return
    seen.add(obj.Name)
    if hasattr(obj, "Group") and obj.Group:
        for child in obj.Group:
            yield from iter_group(child, seen)
    else:
        yield obj


def main():
    if not os.path.exists(REFERENCE):
        print("SKIP  reference-master.FCStd not available; keeping provisional backbox placement")
        return

    doc = App.openDocument(REFERENCE)
    backbox = next((o for o in doc.Objects if o.Label == "Backbox"), None)
    if backbox is None:
        raise RuntimeError("Reference Backbox group not found")

    points = []
    shape_count = 0
    for obj in iter_group(backbox):
        try:
            shape = obj.Shape
            if shape.isNull() or not shape.Vertexes:
                continue
            gp = obj.getGlobalPlacement()
            local_inv = obj.Placement.inverse()
            for vertex in shape.Vertexes:
                # Shape vertices already include the object's local placement;
                # undo it, then apply the complete nested/global placement.
                p_local = local_inv.multVec(vertex.Point)
                p_global = gp.multVec(p_local)
                points.append(p_global)
            shape_count += 1
        except Exception:
            continue

    if not points:
        raise RuntimeError("No usable Backbox child geometry found")

    ref = {
        "xmin": min(p.x for p in points),
        "xmax": max(p.x for p in points),
        "ymin": min(p.y for p in points),
        "ymax": max(p.y for p in points),
        "zmin": min(p.z for p in points),
        "zmax": max(p.z for p in points),
    }
    project = {
        "xmin": ref["xmin"],
        "xmax": ref["xmax"],
        "ymin": ref["ymin"] + CAB_LENGTH,
        "ymax": ref["ymax"] + CAB_LENGTH,
        "zmin": ref["zmin"],
        "zmax": ref["zmax"],
    }
    project.update(
        {
            "width": project["xmax"] - project["xmin"],
            "depth": project["ymax"] - project["ymin"],
            "height": project["zmax"] - project["zmin"],
        }
    )

    payload = {
        "source": "reference-master.FCStd Backbox recursive leaf-shape bounds",
        "shape_count": shape_count,
        "reference_coordinate_bounds": ref,
        "project_coordinate_bounds": project,
        "status": "reference-derived-packaging-envelope",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print("BACKBOX REFERENCE ENVELOPE EXTRACTED")
    print("=" * 64)
    print(f"Leaf shapes: {shape_count}")
    print(
        "Project bounds: "
        f"X {project['xmin']:.1f}..{project['xmax']:.1f}, "
        f"Y {project['ymin']:.1f}..{project['ymax']:.1f}, "
        f"Z {project['zmin']:.1f}..{project['zmax']:.1f} mm"
    )
    print(
        f"Envelope: {project['width']:.1f} x {project['depth']:.1f} x "
        f"{project['height']:.1f} mm"
    )
    print(f"Wrote: {OUT}")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

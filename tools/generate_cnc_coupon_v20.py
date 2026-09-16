#!/usr/bin/env python3
"""Generate a parameterized CNC tolerance coupon SVG + feature manifest.

The output is intentionally CAM-neutral. Layer/group names communicate through-cut,
6 mm pocket and engraving intent; the CNC provider must still assign operations.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cnc_coupon_v20.json"
DEFAULT_OUT = ROOT / ".work" / "cnc_coupon_v20"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def svg_el(tag: str, **attrs):
    return ET.Element(f"{{{SVG_NS}}}{tag}", {k.replace("_", "-"): str(v) for k, v in attrs.items()})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock-mm", type=float, default=None, help="Measured plywood thickness")
    parser.add_argument("--cutter-mm", type=float, default=None, help="Confirmed shop cutter diameter")
    parser.add_argument("--out-dir", type=pathlib.Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    c = cfg["coupon"]
    stock = float(args.stock_mm if args.stock_mm is not None else c["default_stock_thickness_mm"])
    cutter = float(args.cutter_mm if args.cutter_mm is not None else c["default_cutter_diameter_mm"])
    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    w = float(c["width_mm"])
    h = float(c["height_mm"])
    root = svg_el("svg", width=f"{w}mm", height=f"{h}mm", viewBox=f"0 0 {w} {h}")
    root.set("data-stock-mm", f"{stock:.3f}")
    root.set("data-cutter-mm", f"{cutter:.3f}")

    through = svg_el("g", id="THROUGH_CUT", fill="none", stroke="black", stroke_width="0.2")
    pocket = svg_el("g", id="POCKET_6MM", fill="none", stroke="black", stroke_width="0.2")
    engrave = svg_el("g", id="ENGRAVE_WHITE", fill="none", stroke="black")
    root.extend([through, pocket, engrave])

    features: list[dict[str, str]] = []

    # Coupon outer profile.
    margin = 1.0
    ET.SubElement(through, f"{{{SVG_NS}}}rect", {
        "x": f"{margin}", "y": f"{margin}",
        "width": f"{w-2*margin}", "height": f"{h-2*margin}",
        "rx": str(c["corner_radius_mm"]), "ry": str(c["corner_radius_mm"]),
    })
    features.append({"layer": "THROUGH_CUT", "feature": "outer_profile", "x_mm": "1", "y_mm": "1", "size": f"{w-2}x{h-2}", "depth_mm": "THROUGH", "note": "rounded coupon perimeter"})

    # Dado-width trials: insert a piece of the actual stock edge into these pockets.
    x0 = 18.0
    y0 = 28.0
    slot_len = 45.0
    spacing = 68.0
    for idx, delta in enumerate(c["dado_clearance_trials_mm"]):
        slot_w = stock + float(delta)
        x = x0 + idx * spacing
        y = y0
        ET.SubElement(pocket, f"{{{SVG_NS}}}rect", {
            "x": f"{x:.3f}", "y": f"{y:.3f}",
            "width": f"{slot_len:.3f}", "height": f"{slot_w:.3f}",
        })
        features.append({"layer": "POCKET_6MM", "feature": f"dado_trial_{idx+1}", "x_mm": f"{x:.3f}", "y_mm": f"{y:.3f}", "size": f"45x{slot_w:.3f}", "depth_mm": f"{float(c['pocket_depth_mm']):.3f}", "note": f"stock {stock:.3f} + clearance {float(delta):+.3f}"})
        text = ET.SubElement(engrave, f"{{{SVG_NS}}}text", {
            "x": f"{x:.3f}", "y": f"{y + slot_w + 6:.3f}",
            "font-size": "4", "stroke": "none", "fill": "black",
        })
        text.text = f"T{float(delta):+.2f}"

    # Through-hole diameter trials.
    hy = 92.0
    hx0 = 30.0
    hspace = 42.0
    for idx, dia in enumerate(c["through_hole_diameters_mm"]):
        dia = float(dia)
        cx = hx0 + idx * hspace
        ET.SubElement(through, f"{{{SVG_NS}}}circle", {"cx": f"{cx:.3f}", "cy": f"{hy:.3f}", "r": f"{dia/2:.3f}"})
        features.append({"layer": "THROUGH_CUT", "feature": f"hole_{dia:g}mm", "x_mm": f"{cx:.3f}", "y_mm": f"{hy:.3f}", "size": f"D{dia:g}", "depth_mm": "THROUGH", "note": "measure finished diameter"})
        text = ET.SubElement(engrave, f"{{{SVG_NS}}}text", {"x": f"{cx-5:.3f}", "y": f"{hy+10:.3f}", "font-size": "3.5", "stroke": "none", "fill": "black"})
        text.text = f"D{dia:g}"

    # Internal-corner/radius samples: one plain square pocket and one dogbone-intent sample.
    cy = 120.0
    for idx, label in enumerate(("RADIUS", "DOGBONE")):
        x = 30.0 + idx * 70.0
        ET.SubElement(pocket, f"{{{SVG_NS}}}rect", {"x": str(x), "y": str(cy), "width": "30", "height": "30"})
        if label == "DOGBONE":
            r = cutter / 2.0
            for cx, yy in ((x, cy), (x+30, cy), (x, cy+30), (x+30, cy+30)):
                ET.SubElement(pocket, f"{{{SVG_NS}}}circle", {"cx": f"{cx:.3f}", "cy": f"{yy:.3f}", "r": f"{r:.3f}"})
        features.append({"layer": "POCKET_6MM", "feature": label.lower(), "x_mm": f"{x:.3f}", "y_mm": f"{cy:.3f}", "size": "30x30", "depth_mm": f"{float(c['pocket_depth_mm']):.3f}", "note": f"cutter D{cutter:.3f}"})
        text = ET.SubElement(engrave, f"{{{SVG_NS}}}text", {"x": str(x), "y": str(cy+36), "font-size": "3.5", "stroke": "none", "fill": "black"})
        text.text = label

    # Engraving stroke trials.
    ey = 170.0
    ex = 175.0
    for idx, stroke in enumerate(c["engraving_stroke_trials_mm"]):
        stroke = float(stroke)
        y = ey + idx * 8.0
        ET.SubElement(engrave, f"{{{SVG_NS}}}line", {"x1": str(ex), "y1": str(y), "x2": str(ex+80), "y2": str(y), "stroke-width": f"{stroke:.3f}"})
        features.append({"layer": "ENGRAVE_WHITE", "feature": f"stroke_{stroke:.1f}", "x_mm": str(ex), "y_mm": f"{y:.3f}", "size": f"80mm line / {stroke:.1f} stroke", "depth_mm": "SEE_LABEL", "note": "pair with engraving-depth trials during CAM"})

    title = ET.SubElement(engrave, f"{{{SVG_NS}}}text", {"x": "18", "y": "16", "font-size": "5", "stroke": "none", "fill": "black"})
    title.text = f"VPIN CNC COUPON v0.20  STOCK={stock:.3f}  CUTTER={cutter:.3f}"

    svg_path = out / "cnc_coupon_v20.svg"
    ET.ElementTree(root).write(svg_path, encoding="utf-8", xml_declaration=True)

    csv_path = out / "cnc_coupon_v20_features.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["layer", "feature", "x_mm", "y_mm", "size", "depth_mm", "note"])
        writer.writeheader()
        writer.writerows(features)

    readme = out / "README.txt"
    readme.write_text(
        "VPIN CNC tolerance coupon v0.20\n"
        f"Measured stock: {stock:.3f} mm\n"
        f"Confirmed cutter: {cutter:.3f} mm\n"
        f"Pocket depth intent: {float(c['pocket_depth_mm']):.3f} mm\n\n"
        "SVG groups are operation-intent layers only. Confirm CAM operations with the CNC provider.\n"
        "Cut and physically evaluate the coupon before any production cabinet sheet.\n",
        encoding="utf-8",
    )

    print("CNC COUPON v0.20 GENERATED")
    print(f"Stock:  {stock:.3f} mm")
    print(f"Cutter: {cutter:.3f} mm")
    print(f"SVG:    {svg_path}")
    print(f"CSV:    {csv_path}")
    print("STATUS  COUPON TEMPLATE - VERIFY CAM WITH PROVIDER BEFORE CUTTING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

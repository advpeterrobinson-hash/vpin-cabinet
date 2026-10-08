#!/usr/bin/env python3
"""Generate V35.1 CNC qualification coupons.

Produces CAM-neutral SVG/CSV evidence for:
- plywood fit trials on 12 mm or 18 mm production stock;
- 4 mm and 6 mm controlled-depth pocket checks;
- optional 03-7135-1-class side-channel slot trials on 18 mm stock.

No output is a manufacturing release. Physical coupon inspection is mandatory.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "cnc_coupon_v351.json"
DEFAULT_OUT = ROOT / ".work" / "cnc_coupon_v351"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def svg_el(tag: str, **attrs):
    return ET.Element(
        f"{{{SVG_NS}}}{tag}",
        {k.replace("_", "-"): str(v) for k, v in attrs.items()},
    )


def add_text(group, x: float, y: float, value: str, size: float = 3.4) -> None:
    node = ET.SubElement(
        group,
        f"{{{SVG_NS}}}text",
        {
            "x": f"{x:.3f}",
            "y": f"{y:.3f}",
            "font-size": f"{size:g}",
            "stroke": "none",
            "fill": "black",
        },
    )
    node.text = value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock-class", choices=("18", "12"), required=True)
    parser.add_argument("--stock-mm", type=float, required=True)
    parser.add_argument("--cutter-mm", type=float, default=None)
    parser.add_argument("--channel-tongue-mm", type=float, default=None)
    parser.add_argument("--channel-depth-mm", type=float, default=None)
    parser.add_argument("--out-dir", type=pathlib.Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    cutter = float(
        args.cutter_mm
        if args.cutter_mm is not None
        else cfg["tooling"]["cutter_diameter_mm"]
    )
    stock = float(args.stock_mm)
    stock_class = args.stock_class
    if stock <= 0 or cutter <= 0:
        raise SystemExit("stock and cutter must be positive")

    include_channel = (
        args.channel_tongue_mm is not None or args.channel_depth_mm is not None
    )
    if include_channel and stock_class != "18":
        raise SystemExit(
            "side-channel trials are only defined on the 18 mm structural coupon"
        )
    if include_channel and (
        args.channel_tongue_mm is None or args.channel_depth_mm is None
    ):
        raise SystemExit("provide both --channel-tongue-mm and --channel-depth-mm")

    out = args.out_dir / f"{stock_class}mm"
    out.mkdir(parents=True, exist_ok=True)

    c = cfg["coupon"]
    w = float(c["width_mm"])
    h = float(c["height_mm"])
    root = svg_el(
        "svg",
        width=f"{w}mm",
        height=f"{h}mm",
        viewBox=f"0 0 {w} {h}",
    )
    root.set("data-stock-class", stock_class)
    root.set("data-stock-mm", f"{stock:.3f}")
    root.set("data-cutter-mm", f"{cutter:.3f}")

    through = svg_el(
        "g", id="THROUGH_CUT", fill="none", stroke="black", stroke_width="0.2"
    )
    p4 = svg_el(
        "g", id="POCKET_4MM", fill="none", stroke="black", stroke_width="0.2"
    )
    p6 = svg_el(
        "g", id="POCKET_6MM", fill="none", stroke="black", stroke_width="0.2"
    )
    engrave = svg_el(
        "g", id="ENGRAVE_REFERENCE", fill="none", stroke="black"
    )
    root.extend([through, p4, p6, engrave])

    features: list[dict[str, str]] = []
    margin = 1.0
    ET.SubElement(
        through,
        f"{{{SVG_NS}}}rect",
        {
            "x": f"{margin}",
            "y": f"{margin}",
            "width": f"{w - 2 * margin}",
            "height": f"{h - 2 * margin}",
            "rx": str(c["corner_radius_mm"]),
            "ry": str(c["corner_radius_mm"]),
        },
    )
    features.append(
        {
            "layer": "THROUGH_CUT",
            "feature": "outer_profile",
            "x_mm": "1",
            "y_mm": "1",
            "size": f"{w-2}x{h-2}",
            "depth_mm": "THROUGH",
            "note": "coupon perimeter",
        }
    )

    add_text(
        engrave,
        15,
        14,
        f"VPIN V35.1 {stock_class}mm STOCK={stock:.3f} CUTTER={cutter:.3f}",
        4.2,
    )

    trials = [float(x) for x in cfg["fit"]["clearance_trials_mm"]]
    x0 = 15.0
    y4 = 28.0
    y6 = 62.0
    slot_len = 34.0
    spacing = 45.0
    for idx, delta in enumerate(trials):
        slot_w = stock + delta
        x = x0 + idx * spacing
        for layer, y, depth in ((p4, y4, 4.0), (p6, y6, 6.0)):
            ET.SubElement(
                layer,
                f"{{{SVG_NS}}}rect",
                {
                    "x": f"{x:.3f}",
                    "y": f"{y:.3f}",
                    "width": f"{slot_len:.3f}",
                    "height": f"{slot_w:.3f}",
                },
            )
            features.append(
                {
                    "layer": f"POCKET_{int(depth)}MM",
                    "feature": f"fit_T{delta:+.2f}",
                    "x_mm": f"{x:.3f}",
                    "y_mm": f"{y:.3f}",
                    "size": f"{slot_len:.1f}x{slot_w:.3f}",
                    "depth_mm": f"{depth:.3f}",
                    "note": (
                        f"stock {stock:.3f} + total clearance {delta:+.3f}"
                    ),
                }
            )
        add_text(engrave, x, y4 - 4, f"T{delta:+.2f}", 3.0)

    hy = 108.0
    for idx, dia in enumerate(
        float(x) for x in cfg["metrology"]["through_hole_diameters_mm"]
    ):
        cx = 25.0 + idx * 36.0
        ET.SubElement(
            through,
            f"{{{SVG_NS}}}circle",
            {
                "cx": f"{cx:.3f}",
                "cy": f"{hy:.3f}",
                "r": f"{dia/2:.3f}",
            },
        )
        features.append(
            {
                "layer": "THROUGH_CUT",
                "feature": f"hole_D{dia:g}",
                "x_mm": f"{cx:.3f}",
                "y_mm": f"{hy:.3f}",
                "size": f"D{dia:g}",
                "depth_mm": "THROUGH",
                "note": "measure finished diameter",
            }
        )
        add_text(engrave, cx - 4, hy + 9, f"D{dia:g}", 3.0)

    cy = 128.0
    for idx, label in enumerate(("RADIUS", "TBONE")):
        x = 20.0 + idx * 55.0
        ET.SubElement(
            p6,
            f"{{{SVG_NS}}}rect",
            {"x": str(x), "y": str(cy), "width": "28", "height": "28"},
        )
        if label == "TBONE":
            radius = cutter / 2.0
            for cx, yy in ((x, cy + 14), (x + 28, cy + 14)):
                ET.SubElement(
                    p6,
                    f"{{{SVG_NS}}}circle",
                    {
                        "cx": f"{cx:.3f}",
                        "cy": f"{yy:.3f}",
                        "r": f"{radius:.3f}",
                    },
                )
        features.append(
            {
                "layer": "POCKET_6MM",
                "feature": label.lower(),
                "x_mm": f"{x:.3f}",
                "y_mm": f"{cy:.3f}",
                "size": "28x28",
                "depth_mm": "6.000",
                "note": f"cutter D{cutter:.3f}",
            }
        )
        add_text(engrave, x, cy + 34, label, 3.0)

    if include_channel:
        tongue = float(args.channel_tongue_mm)
        depth0 = float(args.channel_depth_mm)
        width_deltas = [
            float(x)
            for x in cfg["side_channel"]["slot_width_clearance_trials_mm"]
        ]
        depth_deltas = [
            float(x)
            for x in cfg["side_channel"]["slot_depth_clearance_trials_mm"]
        ]
        sx0 = 125.0
        sy0 = 126.0
        sx_step = 34.0
        sy_step = 24.0
        for row, ddelta in enumerate(depth_deltas):
            depth = depth0 + ddelta
            layer_id = f"CHANNEL_POCKET_DEPTH_{depth:.2f}MM"
            group = svg_el(
                "g",
                id=layer_id,
                fill="none",
                stroke="black",
                stroke_width="0.2",
            )
            root.insert(len(root) - 1, group)
            for col, wdelta in enumerate(width_deltas):
                slot_w = tongue + wdelta
                if slot_w + 1e-9 < cutter:
                    continue
                x = sx0 + col * sx_step
                y = sy0 + row * sy_step
                ET.SubElement(
                    group,
                    f"{{{SVG_NS}}}rect",
                    {
                        "x": f"{x:.3f}",
                        "y": f"{y:.3f}",
                        "width": "24.000",
                        "height": f"{slot_w:.3f}",
                    },
                )
                features.append(
                    {
                        "layer": layer_id,
                        "feature": (
                            f"channel_W{wdelta:+.2f}_D{ddelta:+.2f}"
                        ),
                        "x_mm": f"{x:.3f}",
                        "y_mm": f"{y:.3f}",
                        "size": f"24x{slot_w:.3f}",
                        "depth_mm": f"{depth:.3f}",
                        "note": (
                            f"tongue {tongue:.3f}+{wdelta:+.3f}; "
                            f"depth {depth0:.3f}+{ddelta:+.3f}"
                        ),
                    }
                )
                add_text(
                    engrave,
                    x,
                    y - 2.0,
                    f"W{wdelta:+.2f}/D{ddelta:+.1f}",
                    2.4,
                )

    stem = f"cnc_coupon_v351_{stock_class}mm"
    svg_path = out / f"{stem}.svg"
    ET.ElementTree(root).write(
        svg_path, encoding="utf-8", xml_declaration=True
    )

    csv_path = out / f"{stem}_features.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "layer",
                "feature",
                "x_mm",
                "y_mm",
                "size",
                "depth_mm",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(features)

    meta = {
        "version": "V35.1",
        "stock_class_mm": int(stock_class),
        "measured_stock_mm": stock,
        "cutter_mm": cutter,
        "side_channel_included": include_channel,
        "channel_tongue_mm": args.channel_tongue_mm,
        "channel_depth_mm": args.channel_depth_mm,
        "manufacturing_release": False,
        "physical_coupon_required": True,
    }
    (out / f"{stem}.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated {svg_path}")
    print(f"Generated {csv_path}")
    print("STATUS: QUALIFICATION COUPON ONLY - PHYSICAL PASS REQUIRED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

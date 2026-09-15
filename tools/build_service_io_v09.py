#!/usr/bin/env python3
"""Build rear service-I/O packaging envelopes for the 580 mm cabinet platform.

This adds removable fascia/window/enclosure envelopes only. It does not cut the
rear panel or finalize connector footprints. The manufacturing release will turn
these envelopes into CNC through-cuts, carrier drawings, and engraving layers.
"""
from __future__ import annotations

import json
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
DESIGN = os.path.join(ROOT, "config/design.json")
IOCFG = os.path.join(ROOT, "config/service_io_v08.json")


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def add_shape(doc, group, name, label, shape, transparency=0):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    try:
        obj.ViewObject.Transparency = transparency
    except Exception:
        pass
    return obj


def centered_window(panel: dict, cab_len: float, wood: float):
    bx = float(panel["rear_x_mm"]) + 0.5 * (
        float(panel["outer_width_mm"]) - float(panel["cabinet_window_width_mm"])
    )
    bz = float(panel["rear_z_mm"]) + 0.5 * (
        float(panel["outer_height_mm"]) - float(panel["cabinet_window_height_mm"])
    )
    return Part.makeBox(
        float(panel["cabinet_window_width_mm"]),
        wood,
        float(panel["cabinet_window_height_mm"]),
        App.Vector(bx, cab_len - wood, bz),
    )


def main() -> None:
    if not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")

    d = load(DESIGN)
    cfg = load(IOCFG)
    cab = d["cabinet"]
    power = cfg["rear_power_fascia"]
    service = cfg["rear_service_fascia"]

    outer = float(cab["outer_width_mm"])
    cab_len = float(cab["side_length_mm"])
    wood = float(cab["main_wood_nominal_mm"])

    if abs(outer - float(cfg["body_outer_width_mm"])) > 0.01:
        raise RuntimeError(
            f"service-I/O config width {cfg['body_outer_width_mm']} does not match design {outer}"
        )

    doc = App.openDocument(MASTER)

    old = doc.getObject("ServiceIOV09")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "ServiceIOV09")
    group.Label = "SERVICE I/O v0.9 - VINTAGE ENGRAVED FASCIAS"

    # Exterior decorative fascias: thickness projects rearward (+Y).
    for stem, p, label in (
        ("Power", power, "REAR POWER FASCIA - WHITE ENGRAVING"),
        ("Service", service, "REAR SERVICE I/O FASCIA - WHITE ENGRAVING"),
    ):
        shape = Part.makeBox(
            float(p["outer_width_mm"]),
            float(p["fascia_thickness_mm"]),
            float(p["outer_height_mm"]),
            App.Vector(float(p["rear_x_mm"]), cab_len, float(p["rear_z_mm"])),
        )
        add_shape(doc, group, f"Rear{stem}FasciaV09", label, shape, 15)

        window = centered_window(p, cab_len, wood)
        add_shape(
            doc,
            group,
            f"Rear{stem}WindowGhostV09",
            f"{stem.upper()} CABINET WINDOW - THROUGH CUT GHOST",
            window,
            82,
        )

    # Thin replaceable low-voltage connector carrier behind the wooden fascia.
    carrier_t = float(service["connector_carrier_thickness_mm"])
    sx = float(service["rear_x_mm"]) + 0.5 * (
        float(service["outer_width_mm"]) - float(service["cabinet_window_width_mm"])
    )
    sz = float(service["rear_z_mm"]) + 0.5 * (
        float(service["outer_height_mm"]) - float(service["cabinet_window_height_mm"])
    )
    carrier = Part.makeBox(
        float(service["cabinet_window_width_mm"]),
        carrier_t,
        float(service["cabinet_window_height_mm"]),
        App.Vector(sx, cab_len - carrier_t, sz),
    )
    add_shape(
        doc,
        group,
        "RearServiceConnectorCarrierV09",
        "REPLACEABLE 3 mm CONNECTOR CARRIER",
        carrier,
        45,
    )

    # Conservative internal mains-enclosure packaging envelope. Exact enclosure
    # hardware remains a later electrical/BOM decision.
    px = float(power["rear_x_mm"]) + 0.5 * (
        float(power["outer_width_mm"]) - float(power["cabinet_window_width_mm"])
    )
    pz = float(power["rear_z_mm"]) + 0.5 * (
        float(power["outer_height_mm"]) - float(power["cabinet_window_height_mm"])
    )
    enclosure_depth = 140.0
    enclosure = Part.makeBox(
        float(power["cabinet_window_width_mm"]),
        enclosure_depth,
        float(power["cabinet_window_height_mm"]),
        App.Vector(px, cab_len - wood - enclosure_depth, pz),
    )
    add_shape(
        doc,
        group,
        "RearMainsEnclosureGhostV09",
        "INTERNAL MAINS ENCLOSURE - PACKAGING GHOST",
        enclosure,
        86,
    )

    p_end = float(power["rear_x_mm"]) + float(power["outer_width_mm"])
    s_start = float(service["rear_x_mm"])
    gap = s_start - p_end

    group.addProperty("App::PropertyLength", "CabinetOuterWidth", "Engineering")
    group.CabinetOuterWidth = outer
    group.addProperty("App::PropertyLength", "PowerSignalFasciaGap", "Engineering")
    group.PowerSignalFasciaGap = gap
    group.addProperty("App::PropertyString", "VisualLanguage", "Engineering")
    group.VisualLanguage = "dark wood + white-filled CNC engraving"
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "PACKAGING ONLY - NOT FOR MANUFACTURING"

    doc.recompute()
    doc.save()

    print("SERVICE I/O v0.9 PACKAGING GENERATED")
    print("=" * 68)
    print(f"Cabinet width             {outer:.1f} mm")
    print(f"Power fascia              {power['outer_width_mm']} x {power['outer_height_mm']} mm")
    print(f"Service fascia            {service['outer_width_mm']} x {service['outer_height_mm']} mm")
    print(f"Power/signal fascia gap   {gap:.1f} mm")
    print("Mains enclosure depth     140.0 mm (provisional)")
    print("STATUS                    PACKAGING ONLY - NOT FOR MANUFACTURING")

    App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

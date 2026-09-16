#!/usr/bin/env python3
"""Build cabinet CNC joinery / legs / PC drawer / glass-interface packaging v0.20.

This is an engineering packaging model, not released CNC geometry.  Exact groove
widths follow measured plywood, and leg/slide/lockdown hole patterns remain
blocked until physical hardware is selected and measured.
"""
from __future__ import annotations

import json
import math
import os

import FreeCAD as App
import Part

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
MASTER = os.path.join(ROOT, "cad/master/vpin-master.FCStd")
CFG = os.path.join(ROOT, "config/cabinet_structure_v20.json")


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def add_shape(doc, group, name, label, shape, transparency=0, part_id=None):
    obj = doc.addObject("PartDesign::Feature", name)
    obj.Label = label
    obj.Shape = shape
    group.addObject(obj)
    if part_id:
        obj.addProperty("App::PropertyString", "PartID", "Build Package")
        obj.PartID = part_id
    try:
        obj.ViewObject.Transparency = transparency
    except Exception:
        pass
    return obj


def main(doc=None, active_only=False) -> None:
    owns_document = doc is None
    if owns_document and not os.path.exists(MASTER):
        raise RuntimeError(f"Missing master file: {MASTER}")
    cfg = load(CFG)
    cab = cfg["cabinet"]
    j = cfg["cnc_joinery"]
    leg = cfg["leg_reinforcement"]
    pc = cfg["pc_drawer"]
    ssf = cfg["ssf_keepouts"]
    glass = cfg["playfield_glass"]
    rails = cfg["siderails"]
    lockdown = cfg["lockdown"]

    outer = float(cab["outer_width_mm"])
    length = float(cab["side_length_mm"])
    wood = float(cab["nominal_wood_mm"])
    front_h = float(cab["front_height_mm"])
    rear_h = float(cab["rear_height_mm"])
    rear_flat = float(cab["rear_top_flat_mm"])
    inner = float(cab["full_thickness_inner_width_mm"])
    dado = float(j["nominal_dado_depth_mm"])
    slope_run = length - rear_flat
    slope_rise = rear_h - front_h
    alpha = math.atan2(slope_rise, slope_run)
    alpha_deg = math.degrees(alpha)

    def top_z(y: float) -> float:
        if y <= slope_run:
            return front_h + math.tan(alpha) * y
        return rear_h

    def slope_shape(shape, front_y: float, vertical_offset: float = 0.0):
        out = shape.copy()
        out.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), alpha_deg)
        out.translate(App.Vector(0, front_y, top_z(front_y) + vertical_offset))
        return out

    if owns_document:
        doc = App.openDocument(MASTER)
    old = doc.getObject("CabinetStructureV20")
    if old:
        for child in list(old.Group):
            try:
                doc.removeObject(child.Name)
            except Exception:
                pass
        doc.removeObject(old.Name)
        doc.recompute()

    group = doc.addObject("App::Part", "CabinetStructureV20")
    group.Label = "CABINET / JOINERY / GLASS / SSF" if active_only else "HISTORICAL STRUCTURE V20"

    # Focus this review on fixed cabinet structure; prior mechanics remain in the
    # document and can be re-enabled independently.
    for prior_name in ("PlayfieldMechanicsV18", "PlayfieldFixedAnchorsV19"):
        prior = doc.getObject(prior_name)
        if prior:
            try:
                prior.ViewObject.Visibility = False
            except Exception:
                pass

    # Replace the simple v0.2 front/rear/bottom visuals with nominal captured
    # production-blank packaging.  Side solids remain the active shell datum.
    for old_name in ("CabinetFront", "CabinetRear", "CabinetBottom"):
        old_obj = doc.getObject(old_name)
        if old_obj:
            try:
                old_obj.ViewObject.Visibility = False
            except Exception:
                pass

    blank_w = float(j["front_rear_blank_width_mm"])
    blank_x = wood - dado
    front = Part.makeBox(blank_w, wood, front_h, App.Vector(blank_x, 0.0, 0.0))
    rear = Part.makeBox(blank_w, wood, rear_h, App.Vector(blank_x, length - wood, 0.0))
    bottom = Part.makeBox(
        float(j["bottom_blank_width_mm"]),
        float(j["bottom_blank_length_mm"]),
        float(j["bottom_panel_thickness_mm"]),
        App.Vector(blank_x, wood - dado, float(j["bottom_panel_bottom_z_mm"])),
    )
    add_shape(doc, group, "CapturedFrontPanelV20", "CAB-FRONT-001-R1 - 6 mm SIDE CAPTURE", front, 10, "CAB-FRONT-001-R1")
    if not active_only:
        add_shape(doc, group, "CapturedRearPanelV20", "CAB-REAR-001-R1 - 6 mm SIDE CAPTURE", rear, 10, "CAB-REAR-001-R1")
    add_shape(doc, group, "CapturedBottomV20", "CAB-BOTTOM-001-R1 - FOUR-EDGE CAPTURE", bottom, 10, "CAB-BOTTOM-001-R1")

    # Low crossmembers are captured 6 mm into both side panels and sit on the
    # bottom assembly. They provide low cabinet shear/load paths without broad
    # side-to-side shelves at SSF height.
    cm_w = float(j["crossmember_blank_width_mm"])
    cm_t = float(j["crossmember_thickness_y_mm"])
    cm_h = float(j["crossmember_height_z_mm"])
    cm_z = float(j["crossmember_bottom_z_mm"])
    for idx, y in enumerate(j["crossmember_y_mm"], start=1):
        shape = Part.makeBox(cm_w, cm_t, cm_h, App.Vector(blank_x, float(y), cm_z))
        add_shape(doc, group, f"LowCrossmember{idx}V20", f"CAB-XMEM-{9+idx:03d}-R1 - 18 mm LOW STRUCTURAL", shape, 12, f"CAB-XMEM-{9+idx:03d}-R1")

    # Machining keepouts show nominal 6 mm side-wall pockets. They are not
    # subtracted from the shell yet because final groove width follows measured stock.
    left_pockets = []
    right_pockets = []
    # Bottom capture groove.
    groove_y = wood - dado
    groove_l = float(j["bottom_blank_length_mm"])
    groove_z = float(j["bottom_panel_bottom_z_mm"])
    groove_h = float(j["bottom_panel_thickness_mm"])
    left_pockets.append(Part.makeBox(dado, groove_l, groove_h, App.Vector(wood-dado, groove_y, groove_z)))
    right_pockets.append(Part.makeBox(dado, groove_l, groove_h, App.Vector(outer-wood, groove_y, groove_z)))
    # Front/rear panel side capture zones.
    left_pockets.append(Part.makeBox(dado, wood, front_h, App.Vector(wood-dado, 0.0, 0.0)))
    right_pockets.append(Part.makeBox(dado, wood, front_h, App.Vector(outer-wood, 0.0, 0.0)))
    left_pockets.append(Part.makeBox(dado, wood, rear_h, App.Vector(wood-dado, length-wood, 0.0)))
    right_pockets.append(Part.makeBox(dado, wood, rear_h, App.Vector(outer-wood, length-wood, 0.0)))
    # Crossmember side pockets.
    for y in j["crossmember_y_mm"]:
        left_pockets.append(Part.makeBox(dado, cm_t, cm_h, App.Vector(wood-dado, float(y), cm_z)))
        right_pockets.append(Part.makeBox(dado, cm_t, cm_h, App.Vector(outer-wood, float(y), cm_z)))
    left_union = left_pockets[0]
    right_union = right_pockets[0]
    for s in left_pockets[1:]:
        left_union = left_union.fuse(s)
    for s in right_pockets[1:]:
        right_union = right_union.fuse(s)
    add_shape(doc, group, "LeftJoineryPocketGhostV20", "LEFT SIDE NOMINAL 6 mm DADO/RABBET VOLUMES - STOCK TBD", left_union, 88)
    add_shape(doc, group, "RightJoineryPocketGhostV20", "RIGHT SIDE NOMINAL 6 mm DADO/RABBET VOLUMES - STOCK TBD", right_union, 88)

    if not active_only:
        # Leg-corner reinforcement: each corner gets an inside sidewall doubler and
        # an end-panel doubler. Exact steel bracket/bolt holes remain blocked.
        sd_t = float(leg["side_doubler_thickness_mm"])
        sd_l = float(leg["side_doubler_length_y_mm"])
        sd_h = float(leg["side_doubler_height_z_mm"])
        ed_t = float(leg["end_doubler_thickness_mm"])
        ed_w = float(leg["end_doubler_width_x_mm"])
        ed_h = float(leg["end_doubler_height_z_mm"])
        dz = float(leg["doubler_bottom_z_mm"])
        rear_side_y = length - wood - sd_l
        rear_end_y = length - wood - ed_t
        leg_parts = [
            ("LegSideDoublerFLV20", "CAB-LEG-SIDE-DBLR-FL-R1", Part.makeBox(sd_t, sd_l, sd_h, App.Vector(wood, wood, dz))),
            ("LegSideDoublerFRV20", "CAB-LEG-SIDE-DBLR-FR-R1", Part.makeBox(sd_t, sd_l, sd_h, App.Vector(outer-wood-sd_t, wood, dz))),
            ("LegSideDoublerRLV20", "CAB-LEG-SIDE-DBLR-RL-R1", Part.makeBox(sd_t, sd_l, sd_h, App.Vector(wood, rear_side_y, dz))),
            ("LegSideDoublerRRV20", "CAB-LEG-SIDE-DBLR-RR-R1", Part.makeBox(sd_t, sd_l, sd_h, App.Vector(outer-wood-sd_t, rear_side_y, dz))),
            ("LegEndDoublerFLV20", "CAB-LEG-END-DBLR-FL-R1", Part.makeBox(ed_w, ed_t, ed_h, App.Vector(wood, wood, dz))),
            ("LegEndDoublerFRV20", "CAB-LEG-END-DBLR-FR-R1", Part.makeBox(ed_w, ed_t, ed_h, App.Vector(outer-wood-ed_w, wood, dz))),
            ("LegEndDoublerRLV20", "CAB-LEG-END-DBLR-RL-R1", Part.makeBox(ed_w, ed_t, ed_h, App.Vector(wood, rear_end_y, dz))),
            ("LegEndDoublerRRV20", "CAB-LEG-END-DBLR-RR-R1", Part.makeBox(ed_w, ed_t, ed_h, App.Vector(outer-wood-ed_w, rear_end_y, dz))),
        ]
        for name, part_id, shape in leg_parts:
            add_shape(doc, group, name, f"{part_id} - 18 mm LEG REINFORCEMENT", shape, 25, part_id)

        # Conservative steel-bracket and retractable-wheel keepouts only.
        bracket_w = 120.0
        bracket_l = 120.0
        bracket_h = 200.0
        wheel_x, wheel_y, wheel_z = [float(v) for v in leg["wheel_keepout_each_corner_mm"]]
        corners = [
            ("FL", wood, wood),
            ("FR", outer-wood-bracket_w, wood),
            ("RL", wood, length-wood-bracket_l),
            ("RR", outer-wood-bracket_w, length-wood-bracket_l),
        ]
        for suffix, bx, by in corners:
            add_shape(doc, group, f"LegBracketKeepout{suffix}V20", f"LEG BRACKET {suffix} - MEASURE BEFORE CNC",
                      Part.makeBox(bracket_w, bracket_l, bracket_h, App.Vector(bx, by, dz)), 86)
            wx = wood if suffix.endswith("L") else outer-wood-wheel_x
            wy = wood if suffix.startswith("F") else length-wood-wheel_y
            add_shape(doc, group, f"WheelKeepout{suffix}V20", f"RETRACTABLE WHEEL {suffix} KEEP-OUT",
                      Part.makeBox(wheel_x, wheel_y, wheel_z, App.Vector(wx, wy, 0.0)), 90)

        # PC drawer: independent subrails sit inward of the sidewalls and tie into the
        # bottom/crossmember system. 500 mm-class slides occupy the gaps to the tray.
        sub_t = float(pc["fixed_subrail_thickness_x_mm"])
        sub_l = float(pc["fixed_subrail_length_y_mm"])
        sub_h = float(pc["fixed_subrail_height_z_mm"])
        sub_y = float(pc["subrail_y_mm"])
        sub_z = float(pc["subrail_z_mm"])
        left_sub_x = float(pc["left_subrail_x_mm"])
        right_sub_x = float(pc["right_subrail_x_mm"])
        add_shape(doc, group, "PCSubrailLeftV20", "PC-SUBRAIL-001L-R1 - 18 mm PLYWOOD", Part.makeBox(sub_t, sub_l, sub_h, App.Vector(left_sub_x, sub_y, sub_z)), 18, "PC-SUBRAIL-001L-R1")
        add_shape(doc, group, "PCSubrailRightV20", "PC-SUBRAIL-001R-R1 - 18 mm PLYWOOD", Part.makeBox(sub_t, sub_l, sub_h, App.Vector(right_sub_x, sub_y, sub_z)), 18, "PC-SUBRAIL-001R-R1")

        tray_w = float(pc["tray_width_x_mm"])
        tray_d = float(pc["tray_depth_y_mm"])
        tray_t = float(pc["tray_thickness_z_mm"])
        tray_x = float(pc["tray_x_mm"])
        tray_z = float(pc["tray_z_mm"])
        tray_stowed_y = float(pc["tray_stowed_y_mm"])
        tray_service_y = float(pc["tray_service_y_mm"])
        tray_stowed = Part.makeBox(tray_w, tray_d, tray_t, App.Vector(tray_x, tray_stowed_y, tray_z))
        tray_service = Part.makeBox(tray_w, tray_d, tray_t, App.Vector(tray_x, tray_service_y, tray_z))
        add_shape(doc, group, "PCTrayStowedV20", "PC-TRAY-001-R1 - STOWED", tray_stowed, 20, "PC-TRAY-001-R1")
        add_shape(doc, group, "PCTrayServiceGhostV20", "PC TRAY - FORWARD SERVICE POSITION GHOST", tray_service, 82)

        # 12 mm slide packaging gaps and 470x400x230 PC service envelope.
        slide_gap = float(pc["slide_packaging_thickness_each_side_mm"])
        slide_h = 45.0
        left_slide_x = tray_x - slide_gap
        right_slide_x = tray_x + tray_w
        slide_y = float(pc["subrail_y_mm"])
        slide_l = float(pc["preferred_slide_class_mm"])
        slide_z = tray_z - 15.0
        add_shape(doc, group, "PCSlideLeftKeepoutV20", "500 mm CLASS LOCKING SLIDE LEFT - HOLES TBD",
                  Part.makeBox(slide_gap, slide_l, slide_h, App.Vector(left_slide_x, slide_y, slide_z)), 84)
        add_shape(doc, group, "PCSlideRightKeepoutV20", "500 mm CLASS LOCKING SLIDE RIGHT - HOLES TBD",
                  Part.makeBox(slide_gap, slide_l, slide_h, App.Vector(right_slide_x, slide_y, slide_z)), 84)
        add_shape(doc, group, "PCServiceEnvelopeV20", "PC SERVICE ENVELOPE 470x400x230 - STOWED",
                  Part.makeBox(tray_w, tray_d, float(pc["service_envelope_height_mm"]), App.Vector(tray_x, tray_stowed_y, tray_z)), 88)

    # SSF exciter zones are sidewall-only keepouts; the drawer structure remains
    # inward and is not allowed to become a broad rigid bridge at those heights.
    for zone in ssf["sidewall_exciter_zones_each_side"]:
        y0, y1 = [float(v) for v in zone["y_mm"]]
        z0, z1 = [float(v) for v in zone["z_mm"]]
        depth = 10.0
        tag = zone["name"].capitalize()
        add_shape(doc, group, f"SSF{tag}LeftKeepoutV20", f"SSF {tag.upper()} LEFT SIDEWALL KEEP-OUT",
                  Part.makeBox(depth, y1-y0, z1-z0, App.Vector(wood, y0, z0)), 91)
        add_shape(doc, group, f"SSF{tag}RightKeepoutV20", f"SSF {tag.upper()} RIGHT SIDEWALL KEEP-OUT",
                  Part.makeBox(depth, y1-y0, z1-z0, App.Vector(outer-wood-depth, y0, z0)), 91)

    # Glass and siderail packaging follows the cabinet slope. Glass dimensions
    # are physical cut dimensions along the sloped plane, not horizontal projection.
    glass_w = float(glass["width_mm"])
    glass_l = float(glass["length_along_slope_mm"])
    glass_t = float(glass["thickness_mm"])
    glass_front = float(glass["front_y_projected_mm"])
    glass_x = (outer - glass_w) / 2.0
    glass_local = Part.makeBox(glass_w, glass_l, glass_t, App.Vector(glass_x, 0.0, 0.0))
    glass_shape = slope_shape(glass_local, glass_front, 3.0)
    add_shape(doc, group, "PlayfieldGlassTargetV20", "PF-GLASS-01 - 575x1100x5 TEMPERED TARGET - DO NOT ORDER YET", glass_shape, 78)

    rail_l = float(rails["packaging_length_along_slope_mm"])
    rail_w = float(rails["top_flange_width_x_mm"])
    rail_t = float(rails["nominal_sheet_thickness_mm"])
    left_rail = slope_shape(Part.makeBox(rail_w, rail_l, rail_t, App.Vector(0.0, 0.0, 0.0)), 0.0, 4.0)
    right_rail = slope_shape(Part.makeBox(rail_w, rail_l, rail_t, App.Vector(outer-rail_w, 0.0, 0.0)), 0.0, 4.0)
    add_shape(doc, group, "SideRailLeftV20", "MET-SIDERAIL-L - PROFILE TBD", left_rail, 35)
    add_shape(doc, group, "SideRailRightV20", "MET-SIDERAIL-R - PROFILE TBD", right_rail, 35)

    # Lockdown bar and receiver are fabrication envelopes only. Their final bent
    # section, receiver lever and hole pattern follow a physical mockup.
    lock_w = float(lockdown["outer_width_mm"])
    lock_d = float(lockdown["packaging_depth_y_mm"])
    lock_h = float(lockdown["packaging_height_z_mm"])
    lock_shape = Part.makeBox(lock_w, lock_d, lock_h, App.Vector(0.0, 0.0, front_h + 5.0))
    add_shape(doc, group, "LockdownBarEnvelopeV20", "CUSTOM 600 mm LOCKDOWN BAR - FABRICATION ENVELOPE", lock_shape, 65)
    rec_w = float(lockdown["receiver_keepout_width_x_mm"])
    rec_d = float(lockdown["receiver_keepout_depth_y_mm"])
    rec_h = float(lockdown["receiver_keepout_height_z_mm"])
    rec_x = (outer - rec_w) / 2.0
    rec_shape = Part.makeBox(rec_w, rec_d, rec_h, App.Vector(rec_x, wood, front_h-rec_h-20.0))
    add_shape(doc, group, "LockdownReceiverKeepoutV20", "LOCKDOWN RECEIVER / LEVER KEEP-OUT - HOLES TBD", rec_shape, 84)

    # Engineering readouts.
    group.addProperty("App::PropertyLength", "NominalDadoDepth", "Engineering")
    group.NominalDadoDepth = dado
    group.addProperty("App::PropertyString", "MeasuredStockRule", "Engineering")
    group.MeasuredStockRule = "FINAL GROOVE/TAB WIDTHS FOLLOW MEASURED PLYWOOD + TOLERANCE COUPON"
    group.addProperty("App::PropertyString", "LegHoleStatus", "Engineering")
    group.LegHoleStatus = leg["exact_leg_holes_status"]
    if not active_only:
        group.addProperty("App::PropertyString", "PCSlideHoleStatus", "Engineering")
        group.PCSlideHoleStatus = pc["exact_slide_holes_status"]
        group.addProperty("App::PropertyLength", "PCSlideTravel", "Engineering")
        group.PCSlideTravel = float(pc["slide_travel_mm"])
    group.addProperty("App::PropertyString", "GlassOrderStatus", "Engineering")
    group.GlassOrderStatus = glass["purchase_status"]
    group.addProperty("App::PropertyString", "LockdownHoleStatus", "Engineering")
    group.LockdownHoleStatus = lockdown["exact_receiver_holes_status"]
    group.addProperty("App::PropertyString", "Status", "Engineering")
    group.Status = "ENGINEERING PACKAGING - NOT FOR CNC/METAL PRODUCTION"

    doc.recompute()
    if owns_document:
        doc.save()

    print("CABINET STRUCTURE v0.20 GENERATED")
    print("=" * 78)
    print(f"Body / inside width       {outer:.1f} / {inner:.1f} mm")
    print(f"Nominal dado depth        {dado:.1f} mm")
    print(f"Bottom blank nominal      {float(j['bottom_blank_width_mm']):.1f} x {float(j['bottom_blank_length_mm']):.1f} mm")
    if not active_only:
        print(f"PC drawer travel          {float(pc['slide_travel_mm']):.1f} mm internal fore-aft")
    print(f"Glass target              {glass_w:.1f} x {glass_l:.1f} x {glass_t:.1f} mm")
    print("Leg/slide/receiver holes  BLOCKED PENDING PHYSICAL HARDWARE")
    print("STATUS                    ENGINEERING PACKAGING - NOT FOR PRODUCTION")

    if owns_document:
        App.closeDocument(doc.Name)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate v0.13 structural material and reinforcement policy."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "structure_materials_v13.json"


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    loads = cfg["design_loads"]
    mat = cfg["brazil_material_policy"]
    body = cfg["main_cabinet_structure"]
    reinf = cfg["critical_reinforcement_zones"]
    backbox = cfg["backbox_structure"]
    join = cfg["joinery_and_fasteners"]
    elec = cfg["electrical_safety_policy"]

    ok = True
    print("STRUCTURE / MATERIALS v0.13")
    print("=" * 74)

    if float(loads["gross_machine_mass_design_envelope_kg"]) < 120.0:
        print("FAIL gross design-mass envelope too low")
        ok = False
    else:
        print(f"PASS gross design-mass envelope: {loads['gross_machine_mass_design_envelope_kg']} kg")

    if float(loads["local_dynamic_factor_for_leg_corner_and_hinge_checks"]) < 1.5:
        print("FAIL dynamic factor too small")
        ok = False
    else:
        print(f"PASS local dynamic factor: {loads['local_dynamic_factor_for_leg_corner_and_hinge_checks']}x")

    if mat["solid_wood_required"]:
        print("FAIL baseline should not depend on solid timber for flat-pack reproducibility")
        ok = False
    else:
        print("PASS solid timber not required")

    if not mat["mDF_structural_use_prohibited"]:
        print("FAIL MDF must remain prohibited for primary structure")
        ok = False
    else:
        print("PASS MDF prohibited for primary structural load paths")

    if float(mat["preferred_nominal_thickness_mm"]) < 18.0:
        print("FAIL preferred main structural plywood thinner than baseline")
        ok = False
    else:
        print(f"PASS preferred structural plywood: {mat['preferred_nominal_thickness_mm']:.0f} mm")

    if not body["bottom_captured_in_dados_required"]:
        print("FAIL bottom panel must be captured in structural joinery")
        ok = False
    else:
        print("PASS bottom panel captured in dados")

    x = body["lower_structural_crossmembers"]
    if not x["required"] or int(x["provisional_count"]) < 2 or float(x["minimum_height_mm"]) < 50.0:
        print("FAIL insufficient lower crossmember strategy")
        ok = False
    else:
        print(f"PASS lower crossmembers: {x['provisional_count']} x >= {x['minimum_height_mm']} mm high")

    leg = reinf["leg_corners"]
    if float(leg["effective_wood_thickness_mm"]) < 36.0 or not leg["through_bolts_required"]:
        print("FAIL leg-corner reinforcement insufficient")
        ok = False
    else:
        print("PASS 36 mm local leg-corner wood + through-bolted metal support")

    shelf = reinf["rear_backbox_shelf"]
    if float(shelf["effective_local_thickness_mm"]) < 36.0 or not shelf["lock_bolts_use_metal_backed_captive_threads"]:
        print("FAIL rear backbox shelf reinforcement insufficient")
        ok = False
    else:
        print("PASS rear shelf locally doubled and metal-backed")

    hinge = reinf["playfield_hinge_and_gas_strut_anchors"]
    if hinge["reduced_oled_pocket_skin_may_carry_load"] or not hinge["through_bolt_or_metal_backed_insert_required"]:
        print("FAIL playfield service loads not properly transferred")
        ok = False
    else:
        print("PASS playfield hinge/strut loads use full-strength backed anchors")

    if not backbox["fixed_rear_structural_frame_required"] or backbox["door_is_primary_shear_member"]:
        print("FAIL keyed backbox door must not replace fixed structure")
        ok = False
    else:
        print("PASS keyed rear door does not weaken fixed backbox load frame")

    if join["wood_screws_into_plywood_edges_for_critical_loads"]:
        print("FAIL critical load paths may not rely on wood screws into plywood edges")
        ok = False
    else:
        print("PASS critical load fasteners use through/metal-backed methods")

    if not (
        elec["shock_hazard_review_required_at_every_stage"]
        and elec["user_warning_required_when_design_or_service_step_involves_mains_voltage"]
        and elec["no_exposed_live_mains_in_normal_or_keyed_service_areas"]
    ):
        print("FAIL electrical shock-hazard policy incomplete")
        ok = False
    else:
        print("PASS mains/shock-hazard review and user-warning policy")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL v0.13 must remain non-manufacturing-ready")
        ok = False

    print("\nSTATUS", "PASS - structural/material engineering only" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

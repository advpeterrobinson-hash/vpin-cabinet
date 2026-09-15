#!/usr/bin/env python3
"""Validate structure-first procurement, labeling and hinge build-package policy."""
from __future__ import annotations

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "structure_buildpack_v14.json"
BOM = ROOT / "bom" / "STRUCTURE_BOM.csv"
PARTS = ROOT / "bom" / "STRUCTURE_PARTS.csv"


def read_csv(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    bom = read_csv(BOM)
    parts = read_csv(PARTS)
    ok = True

    print("STRUCTURE BUILD PACKAGE v0.14")
    print("=" * 72)

    for rel in cfg["documentation_required"]:
        exists = (ROOT / rel).exists()
        print(("PASS" if exists else "FAIL"), "document", rel)
        ok &= exists

    if not cfg["structure_ready_gate_before_electronics"]:
        print("FAIL electronics gate must remain blocked until structure-ready")
        ok = False
    else:
        print("PASS electronics phase is gated behind structure-ready inspection")

    hinge_rows = {row["part_id"]: row for row in bom if row["part_id"].startswith("BB-HNG-")}
    for req in cfg["hinge_procurement"]["required_parts"]:
        pid = req["part_id"]
        row = hinge_rows.get(pid)
        if row is None:
            print("FAIL missing hinge BOM item", pid)
            ok = False
            continue
        if req["part_number"] not in row["item"]:
            print("FAIL hinge BOM part number mismatch", pid)
            ok = False
        elif int(float(row["qty"])) != int(req["qty"]):
            print("FAIL hinge BOM quantity mismatch", pid)
            ok = False
        else:
            print("PASS hinge BOM", pid, req["part_number"], "qty", req["qty"])

    part_ids = [row["part_id"] for row in parts]
    if len(part_ids) != len(set(part_ids)):
        print("FAIL duplicate structure part IDs")
        ok = False
    else:
        print(f"PASS unique structure part IDs ({len(part_ids)})")

    unlabeled = [row["part_id"] for row in parts if not row["label_text"].strip()]
    if unlabeled:
        print("FAIL unlabeled CNC/fabrication parts", unlabeled)
        ok = False
    else:
        print("PASS every registered structure part has label text")

    # Pre-electronics procurement must contain no powered toys/controller boards.
    forbidden_terms = (
        "contactor", "solenoid", "shaker motor", "gear motor", "knocker",
        "controller board", "amplifier", "power supply", "strobe", "flasher"
    )
    early_rows = [row for row in bom if int(row["phase"]) <= 4]
    violations = []
    for row in early_rows:
        item = row["item"].lower()
        if any(term in item for term in forbidden_terms):
            violations.append(row["bom_id"])
    if violations:
        print("FAIL electronics/toys leaked into structure procurement phases", violations)
        ok = False
    else:
        print("PASS structure phases contain no DOF/electronics batch purchases")

    displays = {row["part_id"] for row in bom if row["system"] == "DISPLAY"}
    if not {"PF-TV-01", "BB-TV-01"}.issubset(displays):
        print("FAIL pre-electronics display fit phase missing playfield/backglass displays")
        ok = False
    else:
        print("PASS playfield and backglass displays tracked before electronics phase")

    if cfg["manufacturing_ready"] is not False:
        print("FAIL build package must remain non-manufacturing-ready")
        ok = False
    else:
        print("PASS package explicitly remains engineering-provisional")

    print("\nSTATUS", "PASS - structure build package documentation" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

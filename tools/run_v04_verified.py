#!/usr/bin/env python3
"""Run the complete v0.4 preview including LG-verified VESA geometry."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"


def run(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true", help="Open FreeCAD after successful build")
    parser.add_argument("--report-only", action="store_true", help="Run numerical checks only")
    args = parser.parse_args()

    run([sys.executable, "tools/validate.py"])
    run([sys.executable, "tools/playfield_kinematics.py"])

    if args.report_only:
        return 0

    freecadcmd = shutil.which("freecadcmd")
    if not freecadcmd:
        print("ERROR: freecadcmd not found", file=sys.stderr)
        return 2
    if not MASTER.exists():
        print(f"ERROR: missing master file: {MASTER}", file=sys.stderr)
        return 2

    run([freecadcmd, "tools/build_playfield_v04.py"])
    run([freecadcmd, "tools/apply_lg_c5_mechanical_v04.py"])

    if args.open:
        freecad = shutil.which("freecad")
        if not freecad:
            print("WARN: FreeCAD GUI not found; build completed")
            return 0
        subprocess.Popen([freecad, str(MASTER)], cwd=ROOT)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

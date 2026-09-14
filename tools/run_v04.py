#!/usr/bin/env python3
"""One-command local runner for the v0.4 playfield-service milestone."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"


def run(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the updated master in FreeCAD after successful build",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Run kinematic validation only; do not modify the FCStd",
    )
    args = parser.parse_args()

    freecadcmd = shutil.which("freecadcmd")
    if not freecadcmd and not args.report_only:
        print("ERROR: freecadcmd not found", file=sys.stderr)
        return 2

    run([sys.executable, "tools/playfield_kinematics.py"])

    if args.report_only:
        return 0

    if not MASTER.exists():
        print(f"ERROR: missing master file: {MASTER}", file=sys.stderr)
        return 2

    run([freecadcmd, "tools/build_playfield_v04.py"])

    if args.open:
        freecad = shutil.which("freecad")
        if not freecad:
            print("WARN: freecad GUI executable not found; build completed")
            return 0
        print("\nOpening FreeCAD master...")
        subprocess.Popen([freecad, str(MASTER)], cwd=ROOT)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

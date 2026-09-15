#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/playfield-pivot-v15.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PLAYFIELD PIVOT v0.15 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== ENSURE CURRENT 580 mm STRUCTURE PACKAGE ==='
bash tools/run_structure_v14.sh

echo
echo '=== BUILD PLAYFIELD PIVOT v0.15 ==='
freecadcmd tools/build_playfield_pivot_v15_entry.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Expected FreeCAD group:'
echo '  PLAYFIELD PIVOT v0.15 - 6 mm STEEL PLATES / SHORT JOURNALS'
echo 'Open with: freecad cad/master/vpin-master.FCStd'

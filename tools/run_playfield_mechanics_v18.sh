#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/playfield-mechanics-v18.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PLAYFIELD MECHANICS v0.18 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== ENSURE CURRENT 600 mm STRUCTURE PACKAGE ==='
bash tools/run_structure_v14.sh

echo
echo '=== BUILD INTEGRATED PLAYFIELD MECHANICS ==='
freecadcmd tools/build_playfield_mechanics_v18_entry.py

echo
echo '=== VERIFY INTEGRATED PLAYFIELD MECHANICS ==='
freecadcmd tools/verify_playfield_mechanics_v18.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Expected FreeCAD group:'
echo '  PLAYFIELD MECHANICS v0.18 - GENERIC 43in / PLYWOOD CRADLE / DUAL SAFETY'
echo 'Open with: freecad cad/master/vpin-master.FCStd'

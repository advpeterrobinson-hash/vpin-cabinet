#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/cabinet-structure-v20.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN CABINET STRUCTURE v0.20 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD PLAYFIELD/FIXED-ANCHOR BASE ==='
bash tools/run_playfield_fixed_anchors_v19.sh

echo
echo '=== BUILD CABINET JOINERY / LEGS / PC / GLASS PACKAGING ==='
freecadcmd tools/build_cabinet_structure_v20_entry.py

echo
echo '=== VERIFY CABINET STRUCTURE PACKAGING ==='
freecadcmd tools/verify_cabinet_structure_v20.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: CABINET STRUCTURE v0.20 - JOINERY / LEGS / PC DRAWER / GLASS'

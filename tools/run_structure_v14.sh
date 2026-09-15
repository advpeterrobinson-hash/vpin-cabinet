#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/structure-v14.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN STRUCTURE v0.14 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== CURRENT PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== ENSURE 580 mm PLATFORM / PLAYFIELD BASELINE ==='
bash tools/run_platform_v09.sh

echo
echo '=== BUILD STRUCTURE / BACKBOX / WPC HINGE PACKAGING ==='
freecadcmd tools/build_structure_v14_entry.py

echo
echo '=== VERIFY STRUCTURE PACKAGING ==='
freecadcmd tools/verify_structure_v14.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: STRUCTURE v0.14 - SHELF / BACKBOX / WPC HINGE PACKAGE'

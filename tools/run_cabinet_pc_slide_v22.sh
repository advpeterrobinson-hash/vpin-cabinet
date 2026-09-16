#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/cabinet-pc-slide-v22.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PC SERVICE v0.22 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD v0.21 CLASSIC-LEG / PINSKATES BASE ==='
bash tools/run_cabinet_service_v21.sh

echo
echo '=== BUILD SIMPLE PC SLIDE ==='
freecadcmd tools/build_cabinet_pc_slide_v22_entry.py

echo
echo '=== VERIFY SIMPLE PC SLIDE ==='
freecadcmd tools/verify_cabinet_pc_slide_v22.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: PC SERVICE v0.22 - SIMPLE SLIDING SHELF / OPEN CASE BOLTED DIRECT'

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/cabinet-service-v21.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN CABINET SERVICE / MOBILITY v0.21 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD v0.20 CABINET STRUCTURE BASE ==='
bash tools/run_cabinet_structure_v20.sh

echo
echo '=== BUILD v0.21 CLASSIC LEG / PINSKATES / PC SLED OVERLAY ==='
freecadcmd tools/build_cabinet_service_v21_entry.py

echo
echo '=== VERIFY v0.21 SERVICE / MOBILITY PACKAGING ==='
freecadcmd tools/verify_cabinet_service_v21.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: CABINET SERVICE v0.21 - CLASSIC LEGS / PINSKATES / LIFT-OUT PC'

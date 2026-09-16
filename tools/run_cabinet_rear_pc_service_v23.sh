#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/cabinet-rear-pc-service-v23.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN REAR PC SERVICE v0.23 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD v0.22 BASE ==='
bash tools/run_cabinet_pc_slide_v22.sh

echo
echo '=== BUILD REAR-DOOR PC SERVICE OVERLAY ==='
freecadcmd tools/build_cabinet_rear_pc_service_v23_entry.py

echo
echo '=== VERIFY REAR PC SERVICE ==='
freecadcmd tools/verify_cabinet_rear_pc_service_v23.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: REAR PC SERVICE v0.23 - BACKDOOR / REARWARD PULL-OUT PC'

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/cabinet-rear-cpu-shelf-v24.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN REAR CPU SHELF v0.24 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD v0.23 REAR-SERVICE BASE ==='
bash tools/run_cabinet_rear_pc_service_v23.sh

echo
echo '=== BUILD NARROW REAR CPU SHELF v0.24 ==='
freecadcmd tools/build_cabinet_rear_cpu_shelf_v24_entry.py

echo
echo '=== VERIFY REAR CPU SHELF ==='
freecadcmd tools/verify_cabinet_rear_cpu_shelf_v24.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: REAR CPU SHELF v0.24 - NARROW CASE-SIZED BOARD / FULL REAR EXTENSION'

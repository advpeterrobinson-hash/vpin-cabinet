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
echo '=== BUILD CURRENT CABINET/SERVICE BASE ==='
# v0.24 no longer depends on the superseded v0.22/v0.23 PC concepts.
# Build through v0.21 to obtain current CNC joinery + classic legs/PinSkates,
# then add the active rear CPU shelf directly.
bash tools/run_cabinet_service_v21.sh

echo
echo '=== BUILD NARROW REAR CPU SHELF v0.24 ==='
freecadcmd tools/build_cabinet_rear_cpu_shelf_v24_entry.py

echo
echo '=== VERIFY REAR CPU SHELF ==='
freecadcmd tools/verify_cabinet_rear_cpu_shelf_v24_entry.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: REAR CPU SHELF v0.24 - NARROW CASE-SIZED BOARD / FULL REAR EXTENSION'

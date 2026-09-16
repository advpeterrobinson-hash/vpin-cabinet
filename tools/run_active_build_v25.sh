#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/active-build-v25.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN ACTIVE BUILD v0.25 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== ACTIVE VALIDATION ==='
make validate

echo
echo '=== BUILD CURRENT MECHANICAL PACKAGE ==='
bash tools/run_cabinet_rear_cpu_shelf_v24.sh

echo
echo '=== VERIFY REAR CPU WAS ACTUALLY SAVED ==='
python3 tools/verify_rear_cpu_saved_v25.py

echo
echo '=== PRESENT CLEAN ACTIVE MASTER ==='
freecadcmd tools/cleanup_active_master_v25_entry.py

echo
echo '=== VERIFY SAVED ACTIVE MASTER ==='
python3 tools/verify_active_master_v25_file.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected marker: ACTIVE BUILD v0.25 - SIMPLE CNC KIT'

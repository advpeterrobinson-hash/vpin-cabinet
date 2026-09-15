#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/platform-current.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN CABINET CURRENT PLATFORM BUILD ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON DESIGN VALIDATION ==='
make validate

echo
echo '=== MIGRATE FREECAD MASTER TO CURRENT DESIGN WIDTH ==='
freecadcmd tools/migrate_platform_v09_entry.py

echo
echo '=== REBUILD PLAYFIELD SERVICE GEOMETRY ==='
# Historical v0.4/v0.5 service geometry is rebuilt against the current design
# baseline. It remains engineering/reference geometry, not manufacturing truth.
freecadcmd tools/extract_backbox_reference_entry.py
freecadcmd tools/build_playfield_v04_entry.py
freecadcmd tools/build_playfield_v05_entry.py

echo
echo '=== BUILD SERVICE-I/O PACKAGING ==='
freecadcmd tools/build_service_io_v09_entry.py

echo
echo '=== VERIFY CURRENT PLATFORM / SERVICE I/O ==='
freecadcmd tools/verify_platform_v09.py

echo
echo '=== VERIFY PLAYFIELD SWEEP STILL VALID ==='
freecadcmd tools/verify_playfield_v05.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'

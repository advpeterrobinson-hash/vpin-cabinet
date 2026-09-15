#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/platform-v09.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN CABINET PLATFORM v0.9 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON DESIGN VALIDATION ==='
make validate

echo
echo '=== MIGRATE FREECAD MASTER TO 580 mm ==='
freecadcmd tools/migrate_platform_v09_entry.py

echo
echo '=== REBUILD PLAYFIELD SERVICE GEOMETRY ==='
# Rebuild the previously validated service models against the new 580 mm
# design baseline and current reference backbox envelope.
freecadcmd tools/extract_backbox_reference_entry.py
freecadcmd tools/build_playfield_v04_entry.py
freecadcmd tools/build_playfield_v05_entry.py

echo
echo '=== BUILD SERVICE-I/O PACKAGING ==='
freecadcmd tools/build_service_io_v09_entry.py

echo
echo '=== VERIFY 580 mm PLATFORM / SERVICE I/O ==='
freecadcmd tools/verify_platform_v09.py

echo
echo '=== VERIFY PLAYFIELD SWEEP STILL VALID ==='
freecadcmd tools/verify_playfield_v05.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'

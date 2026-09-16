#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
LOG=".work/logs/playfield-fixed-anchors-v19.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PLAYFIELD FIXED ANCHORS v0.19 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== PURE-PYTHON VALIDATION ==='
make validate

echo
echo '=== BUILD v0.18 MECHANICS BASE ==='
bash tools/run_playfield_mechanics_v18.sh

echo
echo '=== BUILD FIXED SIDEWALL LOAD PATHS ==='
freecadcmd tools/build_playfield_fixed_anchors_v19_entry.py

echo
echo '=== VERIFY FIXED ANCHOR PACKAGING ==='
freecadcmd tools/verify_playfield_fixed_anchors_v19.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'
echo 'Expected group: PLAYFIELD FIXED ANCHORS v0.19 - SIDEWALL LOAD PATHS'

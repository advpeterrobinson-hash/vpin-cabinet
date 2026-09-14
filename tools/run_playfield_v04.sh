#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/playfield-v04.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PLAYFIELD v0.4 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== BASELINE VALIDATION ==='
python3 tools/validate.py

echo
echo '=== GAS STRUT PRELIMINARY SOLVER ==='
python3 tools/solve_playfield_struts.py

echo
echo '=== FREECAD v0.4 BUILD ==='
freecadcmd tools/build_playfield_v04_entry.py

echo
echo '=== FCSTD PERSISTENCE CHECK ==='
python3 tools/check_fcstd_v04.py

echo
echo '=== FREECAD v0.4 HEADLESS VERIFY ==='
freecadcmd tools/verify_playfield_v04.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'

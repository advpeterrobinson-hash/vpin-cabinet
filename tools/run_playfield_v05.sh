#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p .work/logs
LOG=".work/logs/playfield-v05.log"
exec > >(tee "$LOG") 2>&1

echo '=== VPIN PLAYFIELD v0.5 ==='
echo "Repo:   $ROOT"
echo "Branch: $(git branch --show-current)"
echo "Commit: $(git rev-parse --short HEAD)"

echo
echo '=== BASELINE VALIDATION ==='
python3 tools/validate.py

echo
echo '=== v0.5 SWEEP / SAFETY SOLVER ==='
python3 tools/solve_playfield_v05.py

echo
echo '=== ENSURE v0.4 BASE GEOMETRY ==='
freecadcmd tools/build_playfield_v04_entry.py

echo
echo '=== FREECAD v0.5 BUILD ==='
freecadcmd tools/build_playfield_v05_entry.py

echo
echo '=== FREECAD v0.5 HEADLESS VERIFY ==='
freecadcmd tools/verify_playfield_v05.py

echo
echo '=== COMPLETE ==='
echo "Log: $LOG"
echo 'Open with: freecad cad/master/vpin-master.FCStd'

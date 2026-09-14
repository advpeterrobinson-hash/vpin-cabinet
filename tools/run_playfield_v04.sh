#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo '=== BASELINE VALIDATION ==='
python3 tools/validate.py

echo
echo '=== GAS STRUT PRELIMINARY SOLVER ==='
python3 tools/solve_playfield_struts.py

echo
echo '=== FREECAD v0.4 BUILD ==='
freecadcmd tools/build_playfield_v04.py

echo
echo '=== COMPLETE ==='
echo 'Open with: freecad cad/master/vpin-master.FCStd'

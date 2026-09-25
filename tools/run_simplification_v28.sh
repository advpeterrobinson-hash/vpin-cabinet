#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .work/simplification-v28
python3 tools/propose_simplification_v28.py
freecadcmd tools/verify_active_geometry_entry.py > .work/simplification-v28/active-check.log 2>&1
rg -q ACTIVE_GEOMETRY_PASS .work/simplification-v28/active-check.log
freecadcmd tools/build_simplification_v28_entry.py > .work/simplification-v28/cad.log 2>&1
rg -q SIMPLIFICATION_CAD_PASS .work/simplification-v28/cad.log
python3 tools/simplification_counts_v28.py
python3 tools/validate_simplification_v28.py
uv run --with matplotlib tools/render_simplification_v28.py

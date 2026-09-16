#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/logs
make validate > .work/logs/active-validation.log 2>&1
# FreeCADCmd can return zero after Python exceptions. Require a fresh success
# sentinel as well as the saved-file geometry verification, never exit code alone.
freecadcmd tools/build_active_entry.py > .work/logs/active-build.log 2>&1
rg -q '^FRESH_ACTIVE_SAVED ' .work/logs/active-build.log
freecadcmd tools/verify_active_geometry_entry.py > .work/logs/active-geometry.log 2>&1
rg -q '^ACTIVE_GEOMETRY_PASS' .work/logs/active-geometry.log
uv run --with matplotlib python tools/render_active_review.py
printf '%s\n' 'Active CAD and review generated; engineering only, CNC release BLOCKED.'

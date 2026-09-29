#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/front-panel-v32
# FreeCADCmd may return zero after Python exceptions: require both sentinels.
# Progress output can prefix a sentinel on the same line; do not anchor at column 0.
freecadcmd tools/front_panel_v32_entry.py > .work/front-panel-v32/coin-build.log 2>&1
rg -q 'COIN_DOOR_STUDY_PASS 3 saved configurations;' .work/front-panel-v32/coin-build.log
rg -q 'FRONT_STUDY_PASS 20 checks;' .work/front-panel-v32/coin-build.log
uv run --with numpy --with matplotlib python tools/render_front_panel_v32.py
uv run --with numpy --with matplotlib python tools/render_coin_door_v32.py
printf '%s\n' 'FRONT_REVIEW_COMPLETE - candidate envelopes only; actual hardware fit UNVERIFIED'

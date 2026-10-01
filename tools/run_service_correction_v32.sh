#!/usr/bin/env bash
# Current owner correction gate only. CERN-OHL-S-2.0; manufacturing BLOCKED.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/service-correction-v32
freecadcmd tools/wood_dowel_pivot_v32_entry.py > .work/service-correction-v32/build.log 2>&1
if ! rg -q '^WOOD_PIVOT_PASS( |$)' .work/service-correction-v32/build.log; then
  tail -40 .work/service-correction-v32/build.log
  exit 1
fi
rg '^WOOD_PIVOT_PASS( |$)' .work/service-correction-v32/build.log

python3 tools/build_review_viewer.py

python3 tools/render_support_mounting_v32.py

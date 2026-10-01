#!/usr/bin/env bash
# Current narrow V32 correction. CERN-OHL-S-2.0; manufacturing BLOCKED.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/service-correction-v32
freecadcmd tools/notch_floor_fans_v32_entry.py > .work/service-correction-v32/notch-fans-current.log 2>&1
rg -a '^NOTCH_FANS_PASS ' .work/service-correction-v32/notch-fans-current.log
python3 tools/build_review_viewer.py
uv run --with matplotlib python tools/render_notch_floor_fans_v32.py

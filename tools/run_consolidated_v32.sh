#!/usr/bin/env bash
# CERN-OHL-S-2.0
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/consolidated-v32
freecadcmd tools/consolidated_audio_v32_entry.py > .work/consolidated-v32/build.log 2>&1
if ! rg -q 'CONSOLIDATED_AUDIO_PASS ' .work/consolidated-v32/build.log; then
 tail -30 .work/consolidated-v32/build.log
 exit 1
fi
rg 'CONSOLIDATED_AUDIO_PASS ' .work/consolidated-v32/build.log
uv run --with reportlab --with matplotlib python tools/render_consolidated_v32.py

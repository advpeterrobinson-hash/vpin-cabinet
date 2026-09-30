#!/usr/bin/env bash
# Current owner correction gate only. CERN-OHL-S-2.0; manufacturing BLOCKED.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/service-correction-v32
freecadcmd tools/service_correction_v32_entry.py > .work/service-correction-v32/build.log 2>&1
if ! rg -q '^SERVICE_CORRECTION_PASS ' .work/service-correction-v32/build.log; then
  tail -40 .work/service-correction-v32/build.log
  exit 1
fi
rg '^SERVICE_CORRECTION_PASS ' .work/service-correction-v32/build.log
python3 tools/validate_service_correction_v32.py
python3 tools/build_review_viewer.py

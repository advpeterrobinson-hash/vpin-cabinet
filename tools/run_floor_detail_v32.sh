#!/usr/bin/env bash
# CERN-OHL-S-2.0
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/floor-detail-v32
freecadcmd tools/floor_detail_v32_entry.py > .work/floor-detail-v32/build.log 2>&1
if ! rg -q 'FLOOR_DETAIL_PASS ' .work/floor-detail-v32/build.log; then
 tail -25 .work/floor-detail-v32/build.log
 exit 1
fi
rg 'FLOOR_DETAIL_PASS ' .work/floor-detail-v32/build.log

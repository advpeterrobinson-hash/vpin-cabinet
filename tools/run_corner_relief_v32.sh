#!/usr/bin/env bash
# CERN-OHL-S-2.0
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/corner-relief-v32
freecadcmd tools/corner_relief_v32_entry.py > .work/corner-relief-v32/build.log 2>&1
if ! rg -q 'CORNER_RELIEF_PASS ' .work/corner-relief-v32/build.log; then
 tail -20 .work/corner-relief-v32/build.log
 exit 1
fi
rg 'CORNER_RELIEF_PASS ' .work/corner-relief-v32/build.log

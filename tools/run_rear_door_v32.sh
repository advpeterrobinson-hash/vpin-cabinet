#!/usr/bin/env bash
# CERN-OHL-S-2.0. Review only.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/rear-door-v32
freecadcmd tools/rear_door_v32_entry.py > .work/rear-door-v32/build.log 2>&1
if ! rg -q 'REAR_DOOR_PASS ' .work/rear-door-v32/build.log; then
 tail -20 .work/rear-door-v32/build.log
 exit 1
fi
rg 'REAR_DOOR_PASS ' .work/rear-door-v32/build.log

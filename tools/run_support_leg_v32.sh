#!/usr/bin/env bash
# CERN-OHL-S-2.0. Review only; no CNC release.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/support-leg-v32
freecadcmd tools/support_leg_machining_v32_entry.py > .work/support-leg-v32/build.log 2>&1
if ! rg -q 'SUPPORT_LEG_PLAN_PASS ' .work/support-leg-v32/build.log; then
    tail -25 .work/support-leg-v32/build.log
    exit 1
fi
rg 'SUPPORT_LEG_PLAN_PASS ' .work/support-leg-v32/build.log

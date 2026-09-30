#!/usr/bin/env bash
# CERN-OHL-S-2.0. Review evidence only.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/panel-closure-v32
freecadcmd tools/panel_closure_v32_entry.py > .work/panel-closure-v32/build.log 2>&1
if ! rg -q 'PANEL_CLOSURE_PASS ' .work/panel-closure-v32/build.log; then
 tail -20 .work/panel-closure-v32/build.log
 exit 1
fi
rg 'PANEL_CLOSURE_PASS ' .work/panel-closure-v32/build.log

#!/usr/bin/env bash
# CERN-OHL-S-2.0
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/connector-fit-v32
freecadcmd tools/connector_fit_v32_entry.py > .work/connector-fit-v32/build.log 2>&1
if ! rg -q 'CONNECTOR_FIT_PASS ' .work/connector-fit-v32/build.log; then
 tail -25 .work/connector-fit-v32/build.log
 exit 1
fi
rg 'CONNECTOR_FIT_PASS ' .work/connector-fit-v32/build.log

#!/usr/bin/env bash
# CERN-OHL-S-2.0. Packaging review only.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/rear-hardware-v32
freecadcmd tools/rear_hardware_v32_entry.py > .work/rear-hardware-v32/build.log 2>&1
if ! rg -q 'REAR_HARDWARE_PASS ' .work/rear-hardware-v32/build.log; then
 tail -20 .work/rear-hardware-v32/build.log
 exit 1
fi
rg 'REAR_HARDWARE_PASS ' .work/rear-hardware-v32/build.log

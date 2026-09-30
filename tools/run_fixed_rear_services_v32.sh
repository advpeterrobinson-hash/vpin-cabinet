#!/usr/bin/env bash
# CERN-OHL-S-2.0. Packaging evidence only.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/fixed-rear-services-v32
freecadcmd tools/fixed_rear_services_v32_entry.py > .work/fixed-rear-services-v32/build.log 2>&1
if ! rg -q 'FIXED_REAR_SERVICES_PASS ' .work/fixed-rear-services-v32/build.log; then
 tail -20 .work/fixed-rear-services-v32/build.log
 exit 1
fi
rg 'FIXED_REAR_SERVICES_PASS ' .work/fixed-rear-services-v32/build.log

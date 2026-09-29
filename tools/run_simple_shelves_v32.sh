#!/usr/bin/env bash
# Current owner-directed shelf review. Original material: CERN-OHL-S-2.0.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/side-panel-v32
freecadcmd tools/simple_shelves_v32_entry.py > .work/side-panel-v32/simple.log 2>&1
if ! rg -q 'SIMPLE_SHELVES_PASS ' .work/side-panel-v32/simple.log; then
    cat .work/side-panel-v32/simple.log
    exit 1
fi
rg 'SIMPLE_SHELVES_PASS ' .work/side-panel-v32/simple.log

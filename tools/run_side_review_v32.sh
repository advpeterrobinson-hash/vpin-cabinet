#!/usr/bin/env bash
# Original material: CERN-OHL-S-2.0.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/side-panel-v32
for stage in panel service motion; do
    freecadcmd "tools/side_${stage}_v32_entry.py" > ".work/side-panel-v32/${stage}.log" 2>&1
    case "$stage" in
        panel) sentinel=SIDE_REVIEW_PASS ;;
        service) sentinel=SIDE_SERVICE_PASS ;;
        motion) sentinel=SIDE_MOTION_PASS ;;
    esac
    if ! rg -q "${sentinel} " ".work/side-panel-v32/${stage}.log"; then
        cat ".work/side-panel-v32/${stage}.log"
        exit 1
    fi
    rg "${sentinel} " ".work/side-panel-v32/${stage}.log"
done
freecadcmd tools/shelf_retention_v32_entry.py > .work/side-panel-v32/retention.log 2>&1
if ! rg -q 'SHELF_RETENTION_PASS ' .work/side-panel-v32/retention.log; then
    cat .work/side-panel-v32/retention.log
    exit 1
fi
rg 'SHELF_RETENTION_PASS ' .work/side-panel-v32/retention.log
freecadcmd tools/shelf_anchorage_v32_entry.py > .work/side-panel-v32/anchorage.log 2>&1
if ! rg -q 'SHELF_ANCHORAGE_PASS ' .work/side-panel-v32/anchorage.log; then
    cat .work/side-panel-v32/anchorage.log
    exit 1
fi
rg 'SHELF_ANCHORAGE_PASS ' .work/side-panel-v32/anchorage.log
printf '%s\n' 'SIDE_REVIEW_COMPLETE - candidate packaging only; manufacturing BLOCKED'

#!/usr/bin/env bash
# CERN-OHL-S-2.0. Kinematic screen only; not manufacturing release.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p .work/side-panel-v32
freecadcmd tools/shelf_service_pose_v32_entry.py > .work/side-panel-v32/pose.log 2>&1
if ! rg -q 'SHELF_POSE_AUDIT_PASS ' .work/side-panel-v32/pose.log; then
    cat .work/side-panel-v32/pose.log
    exit 1
fi
rg 'SHELF_POSE_AUDIT_PASS|^POSE ' .work/side-panel-v32/pose.log

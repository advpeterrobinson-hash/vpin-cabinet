#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .work/owner-v28
freecadcmd tools/verify_active_geometry_entry.py > .work/owner-v28/baseline-verify.log 2>&1
rg -q ACTIVE_GEOMETRY_PASS .work/owner-v28/baseline-verify.log
freecadcmd tools/review_owner_change_v28_entry.py > .work/owner-v28/review-build.log 2>&1
rg -q OWNER_CHANGE_REVIEW_SAVED .work/owner-v28/review-build.log
python3 tools/validate_owner_change_v28.py
uv run --with matplotlib tools/render_owner_change_v28.py

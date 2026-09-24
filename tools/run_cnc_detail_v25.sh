#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
bash tools/run_active_build_v25.sh
freecadcmd tools/detail_structure_v25_entry.py > .work/logs/cnc-detail.log 2>&1
rg -q '^CNC_DETAIL_GEOMETRY_PASS' .work/logs/cnc-detail.log
python3 tools/generate_measurement_pack_v25.py
python3 tools/generate_cnc_register_v25.py
python3 tools/validate_cnc_detail_v25.py
freecadcmd tools/verify_cnc_detail_v25_entry.py > .work/logs/cnc-detail-saved.log 2>&1
rg -q '^CNC_DETAIL_SAVED_PASS' .work/logs/cnc-detail-saved.log
freecadcmd tools/test_active_geometry_entry.py > .work/logs/active-negative.log 2>&1
rg -q '^ACTIVE_NEGATIVE_TESTS_PASS' .work/logs/active-negative.log
freecadcmd tools/test_cnc_detail_v25_entry.py > .work/logs/cnc-detail-negative.log 2>&1
rg -q '^CNC_DETAIL_NEGATIVE_TESTS_PASS' .work/logs/cnc-detail-negative.log
freecadcmd tools/test_owner_services_v27_entry.py > .work/logs/owner-negative.log 2>&1
rg -q '^OWNER_GEOMETRY_NEGATIVE_TESTS_PASS' .work/logs/owner-negative.log
uv run --with matplotlib python tools/render_cnc_detail_v25.py
printf '%s\n' 'CNC_DETAIL_REVIEW_PASS — measurements, tooling, assembly and proof remain blocked'

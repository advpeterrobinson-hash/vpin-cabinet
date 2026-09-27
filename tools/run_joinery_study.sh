#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/joinery-study
# Read committed geometry; never read or overwrite the owner's historical master.
git show HEAD:exports/generated/cabinet-v32/vpin-central-v32.FCStd > .work/joinery-study/v32-baseline.FCStd
"${FREECADCMD:-freecadcmd}" tools/build_joinery_study_entry.py > .work/joinery-study/build.log 2>&1
grep -q '^JOINERY_STUDY_PASS ' .work/joinery-study/build.log
"${FREECADCMD:-freecadcmd}" tools/test_joinery_study_entry.py > .work/joinery-study/negative.log 2>&1
grep -q '^JOINERY_NEGATIVE_TESTS_PASS' .work/joinery-study/negative.log
uv run --with numpy --with matplotlib python tools/render_joinery_study.py > .work/joinery-study/render.log 2>&1
grep -q '^JOINERY_RENDERS_PASS ' .work/joinery-study/render.log
echo 'JOINERY_REVIEW_PASS: isolated proposal; V32 unchanged; CNC BLOCKED'

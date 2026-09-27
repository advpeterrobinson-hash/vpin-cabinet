#!/usr/bin/env bash
# Current packaging review only. Retained pre-V32 pipeline is not replaced.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .work/v32-review
OUT=exports/generated/cabinet-v32
# Compare against committed engineering evidence, not an accidentally edited local output.
git show "HEAD:$OUT/vpin-central-v32.FCStd" > .work/v32-review/baseline.FCStd
export VPIN_V32_BASELINE="$ROOT/.work/v32-review/baseline.FCStd"
"${FREECADCMD:-freecadcmd}" "$OUT/build_v32.py" > .work/v32-review/build.log 2>&1
# FreeCADCmd may exit zero after a Python exception; require positive sentinels.
grep -q '^V32_SUCCESS 45 objects; intersections \[\]' .work/v32-review/build.log
"${FREECADCMD:-freecadcmd}" tools/verify_v32_entry.py > .work/v32-review/verify.log 2>&1
grep -q '^V32_VERIFIED ' .work/v32-review/verify.log
"${FREECADCMD:-freecadcmd}" tools/test_v32_entry.py > .work/v32-review/negative.log 2>&1
grep -q '^V32_NEGATIVE_TESTS_PASS' .work/v32-review/negative.log
uv run --with numpy --with matplotlib python "$OUT/render_v32.py" > .work/v32-review/render.log 2>&1
grep -q '^6 images generated' .work/v32-review/render.log
python3 - <<'PY'
from pathlib import Path
p=Path('exports/generated/cabinet-v32')
for name in ['01-interior.png','02-travessas.png','03-planta.png','04-traseira.png','05-encaixe.png','06-frente.png','vpin-central-v32.FCStd','vpin-central-v32.step']:
    assert (p/name).stat().st_size>100, name
print('V32_REVIEW_PASS: 45 saved solids; geometry unchanged; six English previews. CNC BLOCKED.')
PY

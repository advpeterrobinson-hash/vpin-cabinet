# Repository cleanup audit — V32 transition

## Purpose

Record what can be cleaned immediately, what remains a live dependency, and what requires local dependency analysis before moving or deleting files.

This audit is intentionally conservative. The goal is a smaller, clearer repository **without losing reproducibility or engineering evidence**.

## Snapshot

Current V32 branch inventory observed at cleanup start:

- approximately 340 tracked tree entries;
- 141 tracked files under `tools/` before cache removal;
- 118 Python files under `tools/`;
- 32 `build_*.py` files;
- 24 `validate_*.py` files;
- 23 `verify_*.py` files;
- 26 `*_entry.py` wrappers;
- 16 `run_*.sh` wrappers;
- approximately 91 Markdown documents under `docs/`.

## Safe cleanup already completed

Four tracked Python bytecode/cache files under `tools/__pycache__/` were removed. They were reproducible temporary artifacts and already matched existing `.gitignore` rules.

No engineering source, CAD evidence or validation data was deleted in that step.

## Important finding: old version numbers do not mean dead code

The root `Makefile` still directly runs validators from multiple historical version numbers.

The retained pre-V32 `build-current` chain includes:

- `tools/run_active_build_v25.sh`;
- `tools/build_active_entry.py`;
- `tools/build_active.py`;
- `tools/verify_active_geometry_entry.py`;
- `tools/render_active_review.py`.

`tools/build_active.py` directly imports:

- `build_cabinet_structure_v20`;
- `build_structure_v14`;
- `build_playfield_mechanics_v18`;
- `build_playfield_fixed_anchors_v19`;
- `build_cabinet_service_v21`;
- `build_owner_services_v27`;
- `build_rear_utility_v26`;
- `build_cabinet_rear_cpu_shelf_v24`.

Therefore these files and their configs **must not be deleted merely because V32 exists**. They are transition dependencies until V32 receives its own validated integrated build path.

## Current V32 review path

The owner-facing V32 review is intentionally separate:

- `docs/RENDERS.md`;
- `docs/PART_CODES.md`;
- `exports/generated/cabinet-v32/README.md`;
- `exports/generated/cabinet-v32/build_v32.py`;
- `exports/generated/cabinet-v32/render_v32.py`;
- `exports/generated/cabinet-v32/validation.json`;
- V32 FreeCAD/STEP review files and six review images.

This is the **current architecture review**, but it is not yet the replacement for the complete pre-V32 validation/build pipeline.

## High-value cleanup candidates — dependency scan required

The largest likely simplification opportunity is wrapper/tool consolidation:

- 26 `*_entry.py` wrappers;
- 16 `run_*.sh` wrappers;
- multiple historical build/validate/verify families for v04–v28;
- old experimental shell/OLED/playfield scripts;
- generated historical review helpers.

These are **candidates**, not approved deletions.

For each candidate, local cleanup must answer:

1. Is it referenced by `Makefile`?
2. Is it imported by a current Python module?
3. Is it invoked by CI or a shell wrapper?
4. Is it linked from active documentation?
5. Does it encode a measurement/decision that is not represented elsewhere?
6. Is it only recoverable from Git history, or does current validation still depend on it?

## Documentation cleanup candidates

Versioned documents from v04–v28 should gradually move out of the default reading path once references are mapped.

Preferred result:

```text
docs/
  README.md
  RENDERS.md
  PART_CODES.md
  LANGUAGE_POLICY.md
  current/
  history/
  pt-BR/
```

Do **not** mass-move them remotely before checking relative links and source references. A broken documentation graph is worse than temporary clutter.

## Generated files

Generated output should be divided conceptually into:

- intentional review artifacts that help humans evaluate the current design;
- reproducible transient outputs that should not be committed.

The current V32 render/CAD review package is intentionally retained because it supports GitHub review without requiring FreeCAD.

Caches, temporary logs and ordinary regenerated intermediates should remain untracked.

## Next local cleanup pass on Homer

The destructive phase should run from a clean local clone/worktree.

Recommended inventory:

```bash
git status --short
git ls-files | sort > /tmp/vpin-tracked.txt

# Direct path/basename references
rg -n --glob '!*.FCStd' --glob '!*.step' \
  'build_|validate_|verify_|run_|docs/|config/|bom/' \
  Makefile .github AGENTS.md README.md CONTRIBUTING.md docs tools config bom

# Imports in Python
rg -n '^\s*(from|import) ' tools

# Shell/Make calls
rg -n 'tools/[A-Za-z0-9_.-]+' Makefile tools .github

# Obvious artifacts
find . \( -type d -name __pycache__ -o -type f -name '*.pyc' -o -type f -name '*.pyo' \) -print
```

Then run the full retained pipeline before and after each cleanup batch:

```bash
make doctor
make validate
git diff --check
```

If FreeCAD is available and the current transition pipeline is expected to build:

```bash
make build-current
```

## Target state before V33 integration

Before V33 becomes the main integrated design path:

- one obvious contributor entry path;
- one clearly named current design package;
- one part-code registry;
- one documentation language policy;
- historical docs separated from current docs;
- no tracked caches;
- no duplicate wrappers without a documented reason;
- V32/V33 integrated validation replacing the pre-V32 pipeline where appropriate;
- pre-V32 pipeline moved to history only **after** replacement validation passes.

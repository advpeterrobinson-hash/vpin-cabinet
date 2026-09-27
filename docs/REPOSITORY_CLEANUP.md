# Repository cleanup plan

## Goal

Make the repository understandable to a new contributor in minutes without destroying design history, reproducibility or engineering evidence.

## Current snapshot

At the start of this cleanup phase, the V32 branch contained approximately:

- 340 tracked tree entries;
- 141 files under `tools/`;
- 91 Markdown documents under `docs/`;
- multiple versioned design generations from v04 through v28 plus the V32 review package.

Four tracked Python `.pyc` cache artifacts were identified and removed immediately because they are reproducible temporary files and were already covered by `.gitignore`.

## Classification model

Every tracked file should end in one of these classes:

### CURRENT

Needed to understand, build, validate or review the current design.

### HISTORY

Superseded engineering that still explains decisions, measurements or validation evidence. Keep it, but move it out of the default contributor path when safe.

### GENERATED-REVIEW

Intentional generated artifacts committed because they make review possible, such as current renders, STEP/FreeCAD review packages or validation summaries.

### REFERENCE

Third-party or research material whose provenance/licensing permits retention and which supports an active design decision.

### REMOVE

Cache, temporary output, exact duplicate, obsolete generated artifact with no review value, or dead helper whose function is fully superseded and recoverable from Git history.

## Cleanup order

1. **Entry path first** — README, renders, docs index, contribution guide and language policy.
2. **Remove obvious artifacts** — caches and temporary files.
3. **Map references** — determine which docs/configs/tools are referenced by current files, Make targets and validators.
4. **Move historical docs** — consolidate superseded version notes under explicit history paths without deleting evidence.
5. **Consolidate tools** — reduce duplicate wrappers/entry points only after confirming Makefile and validator dependencies.
6. **Normalize generated outputs** — keep only intentional review artifacts in contributor-facing paths.
7. **Run validation** — build, tests, link checks and repository diff checks.
8. **Only then delete dead source** — deletion requires evidence that current workflows no longer reference it.

## Do not delete automatically

Until dependency checks are run locally, do not mass-delete:

- v04–v28 configs;
- old build/verify/validate scripts;
- physical validation records;
- measurement sheets;
- BOM history;
- FreeCAD sources or files that may still be consumed by validators;
- research notes that document provenance or hardware decisions.

Git history is a recovery mechanism, not a substitute for understanding whether a current workflow still depends on a file.

## Recommended local audit on Homer

A local clone is the right place for the destructive part of cleanup because it can run repository-wide searches and validation.

Required checks should include:

```bash
git status --short
git ls-files > /tmp/vpin-files.txt
rg -n "docs/|config/|tools/|bom/" README.md Makefile docs config tools bom .github
find . -type d -name __pycache__ -o -type f \( -name '*.pyc' -o -name '*.pyo' \)
make doctor
make validate
git diff --check
```

Before deleting a candidate file:

```bash
rg -n --fixed-strings "candidate/path/or/basename" .
```

If a candidate is referenced by Make, a validator, documentation, a config or another generator, classify it before removing it.

## Completion criteria

The cleanup phase is complete when:

- a new visitor can find renders and current status from the first screen of the README;
- active docs are clearly separated from historical material;
- English canonical / PT-BR mirror rules are visible;
- no cache or temporary artifacts are tracked;
- the current build/review path has one obvious entry point;
- redundant wrappers are removed or explicitly marked historical;
- all current links resolve;
- current validation still passes;
- no manufacturing gate is accidentally weakened or erased.

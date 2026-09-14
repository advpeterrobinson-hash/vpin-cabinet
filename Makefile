SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate open-master build-shell-v02 audit-reference status

help:
	@printf '%s\n' \
	  'vpin-cabinet engineering commands' \
	  '' \
	  '  make doctor          Check required local tools/files' \
	  '  make validate        Validate documented design baseline' \
	  '  make open-master     Open current FreeCAD master' \
	  '  make build-shell-v02 Re-run the validated WPC shell generator' \
	  '  make audit-reference Run reference audit (if local reference copy exists)' \
	  '  make status          Show concise Git state'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	printf 'FreeCAD:   '; $(FREECAD) --version; \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

validate:
	$(PYTHON) tools/validate.py

open-master:
	$(FREECAD) $(MASTER)

build-shell-v02:
	$(FREECADCMD) tools/build_shell_v02.py

audit-reference:
	@test -f .work/audit/reference-master.FCStd || \
	  (echo 'Missing .work/audit/reference-master.FCStd'; exit 1)
	$(FREECADCMD) tools/audit_reference.py > .work/audit/reference-inventory.txt 2>&1
	@echo 'Wrote .work/audit/reference-inventory.txt'

status:
	@git status --short --branch

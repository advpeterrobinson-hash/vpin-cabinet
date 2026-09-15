SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing open-master build-shell-v02 audit-reference status

help:
	@printf '%s\n' \
	  'vpin-cabinet engineering commands' \
	  '' \
	  '  make doctor                 Check required local tools/files' \
	  '  make validate               Run current pure-Python design/packaging checks' \
	  '  make validate-baseline      Validate current documented dimensional baseline' \
	  '  make validate-backbox       Validate v0.6 future-proof backbox packaging' \
	  '  make validate-main-body     Validate v0.7 future-playfield width envelope' \
	  '  make validate-service-io    Validate v0.8 service-I/O packaging' \
	  '  make validate-backbox-fold  Validate v0.10 folding-backbox transport design' \
	  '  make validate-electrical-routing Validate v0.11 cooling/toy/cable infrastructure' \
	  '  make open-master            Open current FreeCAD master' \
	  '  make build-shell-v02        Re-run the validated WPC shell generator' \
	  '  make audit-reference        Run reference audit (if local reference copy exists)' \
	  '  make status                 Show concise Git state'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	printf 'FreeCAD:   '; $(FREECAD) --version; \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

validate: validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing

validate-baseline:
	$(PYTHON) tools/validate.py

validate-backbox:
	$(PYTHON) tools/validate_backbox_v06.py

validate-main-body:
	$(PYTHON) tools/validate_main_body_v07.py

validate-service-io:
	$(PYTHON) tools/validate_service_io_v08.py

validate-backbox-fold:
	$(PYTHON) tools/validate_backbox_fold_v10.py

validate-electrical-routing:
	$(PYTHON) tools/validate_electrical_routing_v11.py

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

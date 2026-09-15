SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack open-master build-shell-v02 build-structure-v14 audit-reference status

help:
	@printf '%s\n' \
	  'vpin-cabinet engineering commands' \
	  '' \
	  '  make doctor                    Check required local tools/files' \
	  '  make validate                  Run current pure-Python design/packaging checks' \
	  '  make validate-baseline         Validate current documented dimensional baseline' \
	  '  make validate-backbox          Validate v0.6 future-proof backbox packaging' \
	  '  make validate-main-body        Validate v0.7 future-playfield width envelope' \
	  '  make validate-service-io       Validate v0.8 service-I/O packaging' \
	  '  make validate-backbox-fold     Validate v0.10 folding-backbox transport design' \
	  '  make validate-electrical-routing Validate v0.11 cooling/toy/cable infrastructure' \
	  '  make validate-backbox-mounting Validate v0.12 shelf/door/display-carriage design' \
	  '  make validate-structure-materials Validate v0.13 structural material/reinforcement policy' \
	  '  make validate-structure-buildpack Validate structure-first BOM/manual/label/hinge package' \
	  '  make open-master               Open current FreeCAD master' \
	  '  make build-shell-v02           Re-run the validated WPC shell generator' \
	  '  make build-structure-v14       Run full 580 mm platform + structure/WPC hinge packaging build' \
	  '  make audit-reference           Run reference audit (if local reference copy exists)' \
	  '  make status                    Show concise Git state'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	printf 'FreeCAD:   '; $(FREECAD) --version; \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

validate: validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack

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

validate-backbox-mounting:
	$(PYTHON) tools/validate_backbox_mounting_v12.py

validate-structure-materials:
	$(PYTHON) tools/validate_structure_materials_v13.py

validate-structure-buildpack:
	$(PYTHON) tools/validate_structure_buildpack_v14.py

open-master:
	$(FREECAD) $(MASTER)

build-shell-v02:
	$(FREECADCMD) tools/build_shell_v02.py

build-structure-v14:
	bash tools/run_structure_v14.sh

audit-reference:
	@test -f .work/audit/reference-master.FCStd || \
	  (echo 'Missing .work/audit/reference-master.FCStd'; exit 1)
	$(FREECADCMD) tools/audit_reference.py > .work/audit/reference-inventory.txt 2>&1
	@echo 'Wrote .work/audit/reference-inventory.txt'

status:
	@git status --short --branch

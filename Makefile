SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack validate-playfield-pivot validate-playfield-display open-master build-shell-v02 build-structure-v14 build-playfield-pivot-v15 audit-reference status

help:
	@printf '%s\n' \
	  'vpin-cabinet engineering commands' \
	  '' \
	  '  make doctor                    Check required local tools/files' \
	  '  make validate                  Run current pure-Python design/packaging checks' \
	  '  make validate-baseline         Validate current documented dimensional baseline' \
	  '  make validate-backbox          Validate future-proof backbox packaging' \
	  '  make validate-main-body        Validate main-body/playfield width envelope' \
	  '  make validate-service-io       Validate service-I/O packaging' \
	  '  make validate-backbox-fold     Validate folding-backbox transport design' \
	  '  make validate-electrical-routing Validate cooling/toy/cable infrastructure' \
	  '  make validate-backbox-mounting Validate shelf/door/display-carriage design' \
	  '  make validate-structure-materials Validate structural material/reinforcement policy' \
	  '  make validate-structure-buildpack Validate structure-first BOM/manual/label/hinge package' \
	  '  make validate-playfield-pivot  Validate steel-plate/short-journal playfield pivot' \
	  '  make validate-playfield-display Validate model-agnostic 42/43 inch display envelope' \
	  '  make open-master               Open current FreeCAD master' \
	  '  make build-shell-v02           Re-run the validated WPC shell generator' \
	  '  make build-structure-v14       Run current 600 mm platform + structure/WPC hinge packaging build' \
	  '  make build-playfield-pivot-v15 Build structure then playfield pivot packaging' \
	  '  make audit-reference           Run reference audit (if local reference copy exists)' \
	  '  make status                    Show concise Git state'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	command -v $(FREECAD) >/dev/null || (echo 'FreeCAD:   MISSING (install FreeCAD first)'; exit 1); \
	printf 'FreeCAD:   '; $(FREECAD) --version | tail -n 1; \
	command -v $(FREECADCMD) >/dev/null || (echo 'FreeCADCmd:MISSING (expected freecadcmd from FreeCAD package)'; exit 1); \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

validate: validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack validate-playfield-pivot validate-playfield-display

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

validate-playfield-pivot:
	$(PYTHON) tools/validate_playfield_pivot_v15.py

validate-playfield-display:
	$(PYTHON) tools/validate_playfield_display_v16.py

open-master:
	$(FREECAD) $(MASTER)

build-shell-v02:
	$(FREECADCMD) tools/build_shell_v02.py

build-structure-v14:
	bash tools/run_structure_v14.sh

build-playfield-pivot-v15:
	bash tools/run_playfield_pivot_v15.sh

audit-reference:
	@test -f .work/audit/reference-master.FCStd || \
	  (echo 'Missing .work/audit/reference-master.FCStd'; exit 1)
	$(FREECADCMD) tools/audit_reference.py > .work/audit/reference-inventory.txt 2>&1
	@echo 'Wrote .work/audit/reference-inventory.txt'

status:
	@git status --short --branch

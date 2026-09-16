SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-playfield-pivot validate-playfield-display validate-playfield-mechanics validate-playfield-fixed-anchors validate-cabinet-rear-cpu-shelf validate-active-build open-master build-current build-cabinet-rear-cpu-shelf-v24 generate-cnc-coupon audit-reference status

help:
	@printf '%s\n' \
	  'vpin-cabinet active engineering workflow' \
	  '' \
	  '  make doctor              Check local tools/files' \
	  '  make validate            Validate the CURRENT design only' \
	  '  make build-current       Build and clean the current FreeCAD master' \
	  '  make open-master         Open the current FreeCAD master' \
	  '  make generate-cnc-coupon Generate the nominal CNC fit coupon' \
	  '  make status              Show concise Git state' \
	  '' \
	  'Historical design experiments remain in Git history; they are not part of the default workflow.'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	command -v $(FREECAD) >/dev/null || (echo 'FreeCAD GUI:MISSING'; exit 1); \
	printf 'FreeCAD GUI:'; command -v $(FREECAD); \
	command -v $(FREECADCMD) >/dev/null || (echo 'FreeCADCmd:MISSING'; exit 1); \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f config/active_build_v25.json && echo 'Active:    OK' || (echo 'Active config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

# Default validation intentionally excludes superseded PC-service/leg/wheel experiments.
validate: validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-playfield-pivot validate-playfield-display validate-playfield-mechanics validate-playfield-fixed-anchors validate-cabinet-rear-cpu-shelf validate-active-build

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

validate-playfield-pivot:
	$(PYTHON) tools/validate_playfield_pivot_v15.py

validate-playfield-display:
	$(PYTHON) tools/validate_playfield_display_v16.py

validate-playfield-mechanics:
	$(PYTHON) tools/validate_playfield_mechanics_v18.py

validate-playfield-fixed-anchors:
	$(PYTHON) tools/validate_playfield_fixed_anchors_v19.py

validate-cabinet-rear-cpu-shelf:
	$(PYTHON) tools/validate_cabinet_rear_cpu_shelf_v24.py

validate-active-build:
	$(PYTHON) tools/validate_active_build_v25.py

build-current:
	bash tools/run_active_build_v25.sh

# Low-level current CPU-shelf build retained for debugging only.
build-cabinet-rear-cpu-shelf-v24:
	bash tools/run_cabinet_rear_cpu_shelf_v24.sh

open-master:
	$(FREECAD) $(MASTER)

generate-cnc-coupon:
	$(PYTHON) tools/generate_cnc_coupon_v20.py

audit-reference:
	@test -f .work/audit/reference-master.FCStd || \
	  (echo 'Missing .work/audit/reference-master.FCStd'; exit 1)
	$(FREECADCMD) tools/audit_reference.py > .work/audit/reference-inventory.txt 2>&1
	@echo 'Wrote .work/audit/reference-inventory.txt'

status:
	@git status --short --branch

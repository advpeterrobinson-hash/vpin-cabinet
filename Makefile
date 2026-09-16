SHELL := /bin/bash
PYTHON ?= python3
FREECAD ?= freecad
FREECADCMD ?= freecadcmd
MASTER := cad/master/vpin-master.FCStd

.PHONY: help doctor validate validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack validate-playfield-pivot validate-playfield-display validate-playfield-mechanics validate-playfield-fixed-anchors validate-cabinet-structure validate-cabinet-service validate-cabinet-pc-slide open-master build-shell-v02 build-structure-v14 build-playfield-pivot-v15 build-playfield-mechanics-v18 build-playfield-fixed-anchors-v19 build-cabinet-structure-v20 build-cabinet-service-v21 build-cabinet-pc-slide-v22 generate-cnc-coupon audit-reference status

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
	  '  make validate-playfield-mechanics Validate integrated v0.18 cradle/safety/latch/harness package' \
	  '  make validate-playfield-fixed-anchors Validate v0.19 fixed support/anchor load paths' \
	  '  make validate-cabinet-structure Validate v0.20 joinery/legs/PC/glass packaging' \
	  '  make validate-cabinet-service  Validate v0.21 classic legs/PinSkates service package' \
	  '  make validate-cabinet-pc-slide Validate v0.22 one-shelf/two-slide PC package' \
	  '  make open-master               Open current FreeCAD master' \
	  '  make build-shell-v02           Re-run the validated WPC shell generator' \
	  '  make build-structure-v14       Run current 600 mm platform + structure/WPC hinge packaging build' \
	  '  make build-playfield-pivot-v15 Build structure then playfield pivot packaging' \
	  '  make build-playfield-mechanics-v18 Build current structure then integrated playfield mechanics' \
	  '  make build-playfield-fixed-anchors-v19 Build v0.18 mechanics then fixed sidewall support/anchor zones' \
	  '  make build-cabinet-structure-v20 Build current mechanics then cabinet joinery/legs/PC/glass package' \
	  '  make build-cabinet-service-v21 Build v0.20 base then classic-leg/PinSkates overlay' \
	  '  make build-cabinet-pc-slide-v22 Build v0.21 base then simple sliding PC shelf' \
	  '  make generate-cnc-coupon       Generate nominal CNC coupon under .work; pass measured values directly to script for production test' \
	  '  make audit-reference           Run reference audit (if local reference copy exists)' \
	  '  make status                    Show concise Git state'

doctor:
	@set -e; \
	printf 'Python:    '; $(PYTHON) --version; \
	command -v $(FREECAD) >/dev/null || (echo 'FreeCAD GUI:MISSING (install/configure FreeCAD first)'; exit 1); \
	printf 'FreeCAD GUI:'; command -v $(FREECAD); \
	command -v $(FREECADCMD) >/dev/null || (echo 'FreeCADCmd:MISSING (expected freecadcmd from FreeCAD package)'; exit 1); \
	printf 'FreeCADCmd:'; $(FREECADCMD) --version | tail -n 1; \
	printf 'Git:       '; git --version; \
	test -f config/design.json && echo 'Config:    OK' || (echo 'Config: MISSING'; exit 1); \
	test -f $(MASTER) && echo 'Master:    OK' || (echo 'Master: MISSING'; exit 1)

validate: validate-baseline validate-backbox validate-main-body validate-service-io validate-backbox-fold validate-electrical-routing validate-backbox-mounting validate-structure-materials validate-structure-buildpack validate-playfield-pivot validate-playfield-display validate-playfield-mechanics validate-playfield-fixed-anchors validate-cabinet-structure validate-cabinet-service validate-cabinet-pc-slide

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

validate-playfield-mechanics:
	$(PYTHON) tools/validate_playfield_mechanics_v18.py

validate-playfield-fixed-anchors:
	$(PYTHON) tools/validate_playfield_fixed_anchors_v19.py

validate-cabinet-structure:
	$(PYTHON) tools/validate_cabinet_structure_v20.py

validate-cabinet-service:
	$(PYTHON) tools/validate_cabinet_service_v21.py

validate-cabinet-pc-slide:
	$(PYTHON) tools/validate_cabinet_pc_slide_v22.py

open-master:
	$(FREECAD) $(MASTER)

build-shell-v02:
	$(FREECADCMD) tools/build_shell_v02.py

build-structure-v14:
	bash tools/run_structure_v14.sh

build-playfield-pivot-v15:
	bash tools/run_playfield_pivot_v15.sh

build-playfield-mechanics-v18:
	bash tools/run_playfield_mechanics_v18.sh

build-playfield-fixed-anchors-v19:
	bash tools/run_playfield_fixed_anchors_v19.sh

build-cabinet-structure-v20:
	bash tools/run_cabinet_structure_v20.sh

build-cabinet-service-v21:
	bash tools/run_cabinet_service_v21.sh

build-cabinet-pc-slide-v22:
	bash tools/run_cabinet_pc_slide_v22.sh

generate-cnc-coupon:
	$(PYTHON) tools/generate_cnc_coupon_v20.py

audit-reference:
	@test -f .work/audit/reference-master.FCStd || \
	  (echo 'Missing .work/audit/reference-master.FCStd'; exit 1)
	$(FREECADCMD) tools/audit_reference.py > .work/audit/reference-inventory.txt 2>&1
	@echo 'Wrote .work/audit/reference-inventory.txt'

status:
	@git status --short --branch

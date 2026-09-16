#!/usr/bin/env python3
import os
import runpy

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
runpy.run_path(os.path.join(ROOT, "tools/build_cabinet_rear_pc_service_v23.py"), run_name="__main__")

#!/usr/bin/env python3
import os
import sys

ROOT = os.path.expanduser("~/Projetos/vpin-cabinet")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from tools.verify_active_master_v25 import main

main()

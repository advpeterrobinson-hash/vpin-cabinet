"""FreeCAD entry with full diagnostics. CERN-OHL-S-2.0."""
import runpy,traceback
from pathlib import Path
try:runpy.run_path(str(Path(__file__).with_name('structural_v335_motion.py')),run_name='__main__')
except Exception:traceback.print_exc();raise

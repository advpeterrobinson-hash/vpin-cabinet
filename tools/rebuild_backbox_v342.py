"""Reproduce V34.2 evidence without automatic promotion. CERN-OHL-S-2.0."""
from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parents[1];env=os.environ.copy();env['MPLCONFIGDIR']='/tmp/v342-mpl'
for f in ['backbox_hardening_v342.py','backbox_v342_manufacturing.py','check_backbox_v342_native.py','backbox_v342_export.py','backbox_v342_documentation.py','backbox_v342_reviews.py','render_backbox_v342.py','build_viewer_v342.py']:
 subprocess.run([sys.executable,str(R/'tools'/f)],cwd=R,env=env,check=True)
print('Now run offline check_backbox_v342_viewer.mjs; backbox_v342_report.py; check_backbox_v342.py. Promotion is a separate evidence-bound operation. No manufacturing release.')

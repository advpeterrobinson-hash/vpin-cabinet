"""Rebuild only the V33.4 overlay, not CURRENT geometry. CERN-OHL-S-2.0."""
from pathlib import Path
import os,subprocess
R=Path(__file__).resolve().parents[1]
subprocess.run(['freecadcmd','tools/solid_leg_v334.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},check=True)
for file in ['build_solid_leg_v334.py','build_solid_leg_metrics_v334.py','document_solid_leg_v334.py','build_viewer_v334.py','check_solid_leg_v334.py']:
 subprocess.run(['python3','tools/'+file],cwd=R,check=True)
print('V334_OVERLAY_REBUILT; run browser qualification before commit')

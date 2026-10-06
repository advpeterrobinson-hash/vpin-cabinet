"""Rebuild V35 study only. Does not promote CURRENT or release manufacturing."""
from pathlib import Path
import os,subprocess,sys
R=Path(__file__).resolve().parents[1]
for s in ['widebody_v35','widebody_v35_manufacturing','widebody_v35_pack','check_widebody_v35','widebody_v35_motion','widebody_v35_interface_screen','widebody_v35_export','widebody_v35_reviews','render_widebody_v35','build_viewer_v35']:
 subprocess.run([sys.executable,str(R/'tools'/f'{s}.py')],cwd=R,check=True,env={**os.environ,'MPLCONFIGDIR':'/tmp/v35-mpl'})
print('Run check_widebody_v35_viewer.mjs then widebody_v35_report.py. Commercial interface gates are distinct from native collision checks. No automatic promotion.')

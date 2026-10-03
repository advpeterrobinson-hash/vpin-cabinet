"""Sequential V33.6.1 rebuild; one native writer at a time. CERN-OHL-S-2.0.
Browser QA, review rendering, regression and promotion are explicit later gates.
"""
from pathlib import Path
import subprocess,sys,os,argparse
R=Path(__file__).resolve().parents[1];W=R/'.work/button-relief-v3361';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');a=p.parse_args()
if not a.derived_only:
 for name,marker in [('button_relief_v3361_entry','V3361_GEOMETRY_DONE True'),('button_relief_v3361_manufacturing','V3361_MANUFACTURING_PASS'),('button_relief_v3361_motion','V3361_MOTION_PASS'),('button_relief_v3361_button_metrology','V3361_BUTTON_METROLOGY'),('button_relief_v3361_states','V3361_STATES_PASS'),('button_relief_v3361_cables','V3361_CABLE_STUDY True'),('button_relief_v3361_review','V3361_REVIEW_SCENES_PASS')]:
  with (W/(name+'.log')).open('w') as log:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},stdout=log,stderr=subprocess.STDOUT,check=True)
  s=(W/(name+'.log')).read_text();assert marker in s and 'Exception while processing' not in s,(name,'Native success marker missing');print(marker,flush=True)
for name in ['build_button_relief_v3361_metadata','build_button_relief_v3361_metrics','build_viewer_v3361']:subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
print('V3361_REBUILD_PASS; render, offline browser, regression and promotion still required')

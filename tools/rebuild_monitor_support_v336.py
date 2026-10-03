"""Sequential V33.6 rebuild. Never overlap native writers. CERN-OHL-S-2.0.
Browser QA, review rendering and final promotion remain explicit later gates.
"""
from pathlib import Path
import subprocess,sys,os,argparse
R=Path(__file__).resolve().parents[1];W=R/'.work/monitor-support-v336';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');a=p.parse_args()
if not a.derived_only:
 for name,marker in [('backbox_support_v336_study','V336_BACKBOX_STUDY_PASS'),('monitor_support_v336_entry','V336_GEOMETRY_DONE True'),('monitor_support_v336_manufacturing','V336_MANUFACTURING_PASS'),('monitor_support_v336_motion','V336_MOTION_PASS'),('monitor_support_v336_button_metrology','V336_BUTTON_METROLOGY'),('monitor_support_v336_states','V336_STATES_PASS'),('monitor_support_v336_cables','V336_CABLE_STUDY True'),('monitor_support_v336_review','V336_REVIEW_SCENES_PASS')]:
  with (W/(name+'.log')).open('w') as log:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},stdout=log,stderr=subprocess.STDOUT,check=True)
  s=(W/(name+'.log')).read_text();assert marker in s and 'Exception while processing' not in s,(name,'Native success marker missing');print(marker,flush=True)
for name in ['build_monitor_support_v336_metadata','build_monitor_support_v336_metrics','build_viewer_v336']:subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
print('V336_REBUILD_PASS; render, offline browser, regression and promotion still required')

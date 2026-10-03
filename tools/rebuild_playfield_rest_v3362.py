"""Sequential V33.6.2 rebuild; one native writer at a time. CERN-OHL-S-2.0.
Browser QA, review rendering, regression and promotion are explicit later gates.
"""
from pathlib import Path
import subprocess,sys,os,argparse
R=Path(__file__).resolve().parents[1];W=R/'.work/playfield-rest-v3362';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');a=p.parse_args()
if not a.derived_only:
 for name,marker in [('playfield_rest_v3362_entry','V3362_GEOMETRY_DONE True'),('playfield_rest_v3362_manufacturing','V3362_MANUFACTURING_PASS'),('playfield_rest_v3362_support_audit','V3362_CLOSED_SUPPORT_AUDIT True'),('playfield_rest_v3362_motion','V3362_MOTION_PASS'),('playfield_rest_v3362_button_metrology','V3362_BUTTON_METROLOGY'),('playfield_rest_v3362_states','V3362_STATES_PASS'),('playfield_rest_v3362_cables','V3362_CABLE_STUDY True'),('playfield_rest_v3362_review','V3362_REVIEW_SCENES_PASS')]:
  with (W/(name+'.log')).open('w') as log:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},stdout=log,stderr=subprocess.STDOUT,check=True)
  s=(W/(name+'.log')).read_text();assert marker in s and 'Exception while processing' not in s,(name,'Native success marker missing');print(marker,flush=True)
for name in ['build_playfield_rest_v3362_metadata','build_playfield_rest_v3362_metrics','build_viewer_v3362']:subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
print('V3362_REBUILD_PASS; render, offline browser, regression and promotion still required')

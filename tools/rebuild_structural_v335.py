"""Ordered V33.5 rebuild; never use successful process exit alone as FreeCAD proof.
CERN-OHL-S-2.0. Browser review and final promotion are separate explicit gates.
"""
from pathlib import Path
import subprocess,sys,argparse
R=Path(__file__).resolve().parents[1];W=R/'.work/structural-v335';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--cad-only',action='store_true');p.add_argument('--derived-only',action='store_true');a=p.parse_args()
if not a.derived_only:
 for name,marker in [('structural_v335_entry','V335_GEOMETRY_DONE True'),('structural_v335_manufacturing','V335_MANUFACTURING_PASS'),('structural_v335_motion_entry','V335_MOTION_PASS'),('structural_v335_states','V335_NAMED_STATES_PASS'),('structural_v335_review','V335_REVIEW_SCENES_PASS')]:
  with (W/(name+'.log')).open('w') as log:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
  text=(W/(name+'.log')).read_text();assert marker in text and 'Exception while processing' not in text,(name,'Missing success marker or FreeCAD exception')
  print(marker,flush=True)
if not a.cad_only:
 for name in ['build_structural_v335_metadata','build_structural_v335_metrics','structural_v335_templates','build_viewer_v335','build_structural_v335_mesh']:subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
print('V335_REBUILD_PASS; CAD render / browser QA / regression / promotion still required',flush=True)

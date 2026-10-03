"""Sequential V33.6.3 rebuild; never overlap native writers. CERN-OHL-S-2.0.
Browser/review QA and promotion remain explicit separate gates.
"""
from pathlib import Path
import subprocess,sys,os,argparse,json
R=Path(__file__).resolve().parents[1];W=R/'.work/front-landings-v3363';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');a=p.parse_args()
def native(name,marker):
 log=W/(name+'.log')
 with log.open('w') as f:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},stdout=f,stderr=subprocess.STDOUT,check=True)
 text=log.read_text();assert marker in text and 'Exception while processing' not in text,(name,'Native success marker missing');print(marker,flush=True)
def py(name):subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
if not a.derived_only:
 for name,marker in [('front_landings_v3363_entry','V3363_NATIVE_DONE'),('front_landings_v3363_manufacturing','V3363_MANUFACTURING_PASS'),('front_landings_v3363_motion','V3363_MOTION_PASS'),('front_landings_v3363_metrology','V3363_METROLOGY_DONE'),('front_landings_v3363_states','V3363_STATES_PASS'),('front_landings_v3363_access','V3363_ACCESS_RESULT True'),('front_landings_v3363_loads','V3363_LOAD_SCREEN_PASS')]:native(name,marker)
 native('front_landings_v3363_internal_hardware','V3363_INTERNAL_HARDWARE_PASS')
 py('build_front_landings_v3363_hardware');py('check_front_landings_v3363_support')
 native('front_landings_v3363_viewer_export','V3363_VIEWER_NATIVE_PASS')
gate=json.loads((R/'exports/generated/front-landings-v3363/support-validation.json').read_text());assert gate['architecture_pass']
for name in ['build_front_landings_v3363_metadata','build_front_landings_v3363_metrics','build_viewer_v3363']:py(name)
print('V3363_REBUILD_PASS; review rendering, offline browser, regression and promotion still required')

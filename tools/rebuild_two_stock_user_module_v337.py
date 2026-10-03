"""Sequential scoped V33.7 rebuild. CERN-OHL-S-2.0.
Never overlap native writers; final browser/review/regression/promotion are separate.
"""
from pathlib import Path
import subprocess,sys,os,argparse,json
R=Path(__file__).resolve().parents[1];W=R/'.work/two-stock-user-module-v337';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');a=p.parse_args()
def native(name,marker):
 log=W/(name+'.log')
 with log.open('w') as f:subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen'},stdout=f,stderr=subprocess.STDOUT,check=True)
 text=log.read_text();assert marker in text and 'Exception while processing' not in text,(name,'Native success marker missing');print(marker,flush=True)
def py(name):subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
if not a.derived_only:
 for name,marker in [('plywood_conversion_v337_entry','V337_CONVERSION_PASS'),('plywood_conversion_v337_motion','V337_CONVERSION_MOTION_PASS'),('plywood_conversion_v337_hardware_audit','V337_HARDWARE_RESERVE_PASS'),('underfront_search_v337','V337_MODULE_SEARCH'),('underfront_module_v337','V337_MODULE_PASS'),('combine_two_stock_v337','V337_COMBINED_PASS'),('two_stock_v337_manufacturing','V337_MANUFACTURING_PASS')]:native(name,marker)
 py('build_two_stock_v337_hardware');native('two_stock_user_module_v337_viewer_export','V337_VIEWER_NATIVE_PASS')
gate=json.loads((R/'exports/generated/two-stock-user-module-v337/combined-validation.json').read_text());assert gate['pass']
for name in ['build_two_stock_user_module_v337_metadata','build_two_stock_v337_metrics','build_viewer_v337']:py(name)
print('V337_REBUILD_PASS; review rendering, offline browser, regression and promotion still required')

"""Sequential V33.8 native/derived rebuild; no overlapping native writers.
CERN-OHL-S-2.0. Browser QA, regression and promotion are explicit final steps.
"""
from pathlib import Path
import subprocess,sys,os,argparse
R=Path(__file__).resolve().parents[1];W=R/'.work/service-productization-v338';W.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--derived-only',action='store_true');p.add_argument('--reviews',action='store_true');args=p.parse_args()
def native(name,marker,env=None):
 log=W/(name+'-rebuild.log')
 with log.open('w') as f:
  subprocess.run(['freecadcmd','tools/'+name+'.py'],cwd=R,env={**os.environ,'QT_QPA_PLATFORM':'offscreen',**(env or {})},stdout=f,stderr=subprocess.STDOUT,check=True)
 t=log.read_text();assert marker in t and 'Exception while processing' not in t,(name,'Missing native success marker');print(marker,flush=True)
def py(name):subprocess.run([sys.executable,'tools/'+name+'.py'],cwd=R,check=True)
if not args.derived_only:
 for name,marker in [('sw02_current_v338_metrology','V338'),('front_landing_productization_v338','V338_LANDING_STUDY_PASS'),('combine_service_productization_v338','V338_COMBINED_PASS'),('front_landing_adjustment_v338','V338_ADJUSTMENT_PASS')]:native(name,marker)
py('build_service_productization_v338_decisions')
if not args.derived_only:
 native('sw02_v338_manufacturing','V338_MANUFACTURING_PASS')
 native('service_modularity_v338','V338_MODULARITY_RESULT True',{'V338_MODULARITY_SOURCE':'exports/generated/service-productization-v338/play.FCStd'})
 native('modularity_dryfit_v338','V338_DRYFIT_AUDIT')
 native('safety_straps_v338_study','V338_SAFETY_STUDY_EVIDENCE_PASS')
for name in ['build_sw02_v338_templates','build_service_productization_v338_hardware','report_service_modularity_v338','build_service_productization_v338_metadata','build_service_productization_v338_metrics']:py(name)
native('service_productization_v338_independent_qa','V338_INDEPENDENT_QA_PASS')
if not args.derived_only:native('service_productization_v338_viewer_export','V338_VIEWER_NATIVE_PASS')
py('build_viewer_v338')
if args.reviews:
 native('modularity_review_v338','V338_MODULARITY_REVIEWS')
 native('service_productization_v338_review','V338')
 py('render_service_productization_v338')
print('V338_REBUILD_COMPLETE; browser QA, independent QA, regression, report and promotion still required; CNC BLOCKED')

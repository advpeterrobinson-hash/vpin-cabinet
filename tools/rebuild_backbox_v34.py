"""Rebuild V34 sequentially; explicit browser QA/check/promotion afterwards. CERN-OHL-S-2.0."""
from pathlib import Path
import subprocess,os,sys
R=Path(__file__).resolve().parents[1];W=R/'.work/backbox-v34';W.mkdir(parents=True,exist_ok=True)
python=os.environ.get('FREECAD_PYTHON','/home/peter/.local/opt/freecad-1.1.3/usr/bin/python');lib=os.environ.get('FREECAD_LIB','/home/peter/.local/opt/freecad-1.1.3/usr/lib')
env={**os.environ,'PYTHONPATH':lib,'MPLCONFIGDIR':'/tmp/v34-mpl'}
for name,native,marker in [('backbox_simplification_v34',True,'V34_STUDY_DONE True'),('backbox_v34_manufacturing',True,'V34_MANUFACTURING'),('backbox_v34_documentation',False,'V34_DOCUMENTATION'),('backbox_v34_export',True,'V34_EXPORT'),('check_backbox_v34_native',True,'V34_INDEPENDENT True'),('backbox_v34_reviews',True,'V34_REVIEWS_NATIVE'),('render_backbox_v34',True,'V34_REVIEW_RENDER_PASS'),('build_viewer_v34',False,'V34_VIEWER')]:
 log=W/(name+'.log')
 with log.open('w') as f:subprocess.run([python if native else sys.executable,'tools/'+name+'.py'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 assert marker in log.read_text(),(name,log.read_text()[-2000:]);print(marker,flush=True)
print('V34_DERIVED_COMPLETE; browser QA, regression, report and promotion still required')

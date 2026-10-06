"""Rebuild V35.1 reference design. No automatic promotion or CNC release."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parents[1]
for s in ['widebody_v351','widebody_v351_manufacturing','widebody_v351_pack','widebody_v351_nesting','check_widebody_v351','widebody_v351_motion','widebody_v351_audit','widebody_v351_documentation','widebody_v351_export','widebody_v351_reviews','render_widebody_v351','build_viewer_v351']:
 subprocess.run([sys.executable,str(R/'tools'/f'{s}.py')],cwd=R,check=True,env={**os.environ,'MPLCONFIGDIR':'/tmp/v351-mpl'})
for n in ['geometry','validation','continuous-motion','conservative-validation']:
 assert json.loads((R/'exports/generated/widebody-v351'/f'{n}.json').read_text())['pass'],n
print('Run offline browser QA, report and promotion gate separately. CNC BLOCKED.')

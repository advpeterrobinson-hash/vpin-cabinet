"""Launch the offline Chrome/Playwright check using an existing Node dependency root."""
from pathlib import Path
import os,shutil,subprocess
R=Path(__file__).resolve().parents[1];W=R/'.work/viewer-v332';W.mkdir(parents=True,exist_ok=True)
modules=W/'node_modules'
if not modules.exists():
 candidates=[Path(os.environ['VPIN_NODE_MODULES'])] if os.environ.get('VPIN_NODE_MODULES') else [R/'.work/flatpack-v331/node_modules']
 found=next((p for p in candidates if (p/'playwright').exists()),None)
 if not found:raise SystemExit('Playwright required: set VPIN_NODE_MODULES to an existing node_modules directory containing playwright. No network runtime is needed by the viewer.')
 modules.symlink_to(found.resolve(),target_is_directory=True)
script=W/'check_assembly_viewer_v332.mjs';shutil.copyfile(R/'tools/check_assembly_viewer_v332.mjs',script)
subprocess.run(['node',str(script)],cwd=R,check=True,timeout=900)

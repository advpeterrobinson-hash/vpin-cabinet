"""Run offline animation checks with existing Playwright; no network install."""
from pathlib import Path
import subprocess,shutil
R=Path(__file__).resolve().parents[1];W=R/'.work/assembly-v333';W.mkdir(exist_ok=True)
n=W/'node_modules'
if not n.exists():n.symlink_to((R/'.work/viewer-v332/node_modules').resolve(),target_is_directory=True)
shutil.copyfile(R/'tools/check_assembly_v333.mjs',W/'check.mjs')
subprocess.run(['node',str(W/'check.mjs')],cwd=R,check=True,timeout=900)
# Run the existing53inspection/manual/palette regressions against this same HTML,
# writing evidence into an isolated temporary review directory, not V33.2 history.
legacy=W/'legacy-review';legacy.mkdir(exist_ok=True)
script=(R/'tools/check_assembly_viewer_v332.mjs').read_text().replace("path.join(root,'exports/generated/viewer-v332')","path.join(root,'.work/assembly-v333/legacy-review')")
(W/'legacy.mjs').write_text(script)
subprocess.run(['node',str(W/'legacy.mjs')],cwd=R,check=True,timeout=900)
shutil.copyfile(legacy/'browser-validation.json',R/'exports/generated/assembly-v333/legacy-browser-validation.json')

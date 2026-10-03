"""Offline V33.4 tablet, geometry and tooling animation review."""
from pathlib import Path
import subprocess,shutil
R=Path(__file__).resolve().parents[1];W=R/'.work/solid-leg-v334';W.mkdir(exist_ok=True)
n=W/'node_modules'
if not n.exists():n.symlink_to((R/'.work/viewer-v332/node_modules').resolve(),target_is_directory=True)
shutil.copyfile(R/'tools/check_solid_leg_viewer_v334.mjs',W/'check.mjs')
subprocess.run(['node',str(W/'check.mjs')],cwd=R,check=True,timeout=900)
legacy=W/'legacy-review';legacy.mkdir(exist_ok=True)
s=(R/'tools/check_assembly_viewer_v332.mjs').read_text().replace("path.join(root,'exports/generated/viewer-v332')","path.join(root,'.work/solid-leg-v334/legacy-review')").replace('Search M019','Search SW01').replace("'M019'","'SW01'").replace('===130','===106').replace('130 real manufacturing','106 real manufacturing').replace('130 pieces','106 pieces').replace('===28','===4').replace('28 real leg laminations','4 solid leg blocks').replace('Leg-block layers — 28 pieces','Solid leg blocks —4 pieces').replace('Camadas dos blocos dos pés — 28 peças','Blocos maciços dos pés —4 peças')
(W/'legacy.mjs').write_text(s)
subprocess.run(['node',str(W/'legacy.mjs')],cwd=R,check=True,timeout=900)
shutil.copyfile(legacy/'browser-validation.json',R/'exports/generated/solid-leg-v334/legacy-browser-validation.json')

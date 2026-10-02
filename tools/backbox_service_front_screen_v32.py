"""Diagnostic front-module inset study only. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
src=load(R/C['source_directory']/'matrix-removed.FCStd');p,g,m,b=build(src)
fixed={n:s for n,s in actual(src).items() if not n.startswith('BB_')};out=[]
for role,ids,ds in [('cassette',[n for n in p if g[n]=='cassette'],[24,32,40,48]),('glass',[n for n in p if n in ['BB_Backglass','BB_GlassLowerRail','BB_GlassLowerPad']],[8,12,16])]:
 for dd in ds:
  offset=dd-C['front_layout_insets_mm'][role]
  mov={n:shifted(p[n],y=offset) for n in ids};rows=[]
  for a in [75,85,90]:rows.append({'angle':a,'hits':hits(transform(mov,angle=a,axis=WPC),fixed)})
  r={'role':role,'offset_mm':dd,'samples':rows};out.append(r);print(json.dumps(r),flush=True)
(O/'front-inset-screen.json').write_text(json.dumps(out,indent=2)+'\n');print('FRONT_INSET_SCREEN_DONE',flush=True)

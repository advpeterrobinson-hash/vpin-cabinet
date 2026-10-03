"""Rebuild CURRENT named CAD states with only validated V33.5 replacements. CERN-OHL-S-2.0."""
from pathlib import Path
import json,sys,hashlib,gzip,io
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import load,transform,WPC,mesh
O=R/'exports/generated/structural-v335';source=R/'exports/generated/backbox-lock-integration-v32';p=load(O/'play.FCStd');v=json.loads((O/'geometry-validation.json').read_text());assert v['pass'];assert json.loads((O/'motion-validation.json').read_text())['pass']
changed=[r['name'] for r in v['changed']]+v['added'];removed=v['removed'];mapping=[('service','SERVICE',0),('lift-out','LIFT-OUT',0),('matrix-removed','MATRIX REMOVED',0),('doors-open','DOORS OPEN',0),('locks-parked','UNLOCKED',0),('fold-1','FOLD1',1),('fold-45','FOLD45',45),('backbox-fold','BACKBOX FOLD',90)]
states={'PLAY':'play.FCStd'}
for filename,state,a in mapping:
 ss=load(source/(filename+'.FCStd'))
 for n in removed:ss.pop(n,None)
 for n in changed:ss[n]=transform({n:p[n]},angle=a,axis=WPC)[n] if n.startswith('BB_') and a else p[n]
 states[state]=filename+'.FCStd'
 doc=A.newDocument('V335_'+filename.replace('-','_'))
 for n,s in ss.items():o=doc.addObject('PartDesign::Feature',n);o.Shape=s
 doc.recompute();doc.saveAs(str(O/(filename+'.FCStd')));A.closeDocument(doc.Name)
(O/'state-register.json').write_text(json.dumps({'native_files':states,'mesh_builder':'tools/build_structural_v335_mesh.py','release':False},indent=2)+'\n')
print('V335_NAMED_STATES_PASS',len(states),flush=True)

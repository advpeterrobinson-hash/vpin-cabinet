"""V33.6.1 native named states; replace changed geometry in every pose. CERN-OHL-S-2.0."""
from pathlib import Path
import json,sys,hashlib
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,transform,PF,WPC,V
O=R/'exports/generated/button-relief-v3361';source=R/'exports/generated/monitor-support-v336';p=load(O/'play.FCStd');v=json.loads((O/'geometry-validation.json').read_text());assert v['pass']
changed=[r['name'] for r in v['changed']]+v['added'];states={'PLAY':'play.FCStd'}
for filename,state,a in [('service','SERVICE',0),('lift-out','LIFT-OUT',0),('matrix-removed','MATRIX REMOVED',0),('doors-open','DOORS OPEN',0),('locks-parked','UNLOCKED',0),('fold-1','FOLD1',1),('fold-45','FOLD45',45),('backbox-fold','BACKBOX FOLD',90)]:
 ss=load(source/(filename+'.FCStd'))
 for n in changed:
  s=p[n].copy()
  if n=='PF_BasePlywood':
   if state=='SERVICE':s.rotate(PF,V(1,0,0),-50)
   if state=='LIFT-OUT':s.translate(V(0,0,48))
  if n.startswith('BB_') and a:s.rotate(WPC,V(1,0,0),a)
  ss[n]=s
 states[state]=filename+'.FCStd';doc=A.newDocument('V3361_'+filename.replace('-','_'))
 for n,s in ss.items():
  o=doc.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','GeometryAuthority');o.GeometryAuthority='V33.6.1 current, nominal / CNC HOLD' if n in changed else 'Unchanged V33.6 native named state'
 doc.recompute();doc.saveAs(str(O/(filename+'.FCStd')));A.closeDocument(doc.Name)
(O/'state-register.json').write_text(json.dumps({'native_files':states,'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'release':False},indent=2)+'\n');print('V3361_STATES_PASS',len(states),flush=True)

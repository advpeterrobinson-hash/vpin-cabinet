"""Exact additions in all existing named poses. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib,json,sys
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,PF,V
C=json.loads((R/'config/front_landings_v3363.json').read_text());O=R/C['output'];source=(R/C['source']).parent
p=load(O/'play.FCStd');released=load(O/'released.FCStd');g=json.loads((O/'geometry-validation.json').read_text());motion=json.loads((O/'motion-validation.json').read_text());assert motion['pass']
newnames=g['new_wood_names']+g['new_hardware_names'];states={'PLAY':'play.FCStd','PF RELEASED':'released.FCStd'}
for filename,state in [('service','SERVICE'),('lift-out','LIFT-OUT'),('matrix-removed','MATRIX REMOVED'),('doors-open','DOORS OPEN'),('locks-parked','UNLOCKED'),('fold-1','FOLD1'),('fold-45','FOLD45'),('backbox-fold','BACKBOX FOLD')]:
 ss=load(source/(filename+'.FCStd'))
 for name in newnames:
  s=(released if state in ['SERVICE','LIFT-OUT'] else p)[name].copy()
  if name in g['moving_receiver_names']:
   if state=='SERVICE':s.rotate(PF,V(1,0,0),-50)
   if state=='LIFT-OUT':s.translate(V(0,0,48))
  ss[name]=s
 d=A.newDocument('V3363_'+filename.replace('-','_'))
 for name,s in ss.items():d.addObject('PartDesign::Feature',name).Shape=s
 d.recompute();d.saveAs(str(O/(filename+'.FCStd')));A.closeDocument(d.Name);states[state]=filename+'.FCStd'
(O/'state-register.json').write_text(json.dumps({'native_files':states,'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'release':False,'closed_position_support_status':'DESIGN_CANDIDATE_PENDING_ROOT_COMPLETE_GATES','explicit_motion_metadata':'viewer-motion.json'},indent=2)+'\n')
print('V3363_STATES_PASS',len(states),flush=True)

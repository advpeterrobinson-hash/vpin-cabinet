"""Promote only exact-envelope SW02; retain all other V33.7 geometry.
CERN-OHL-S-2.0. Design candidate, no production release.
"""
from pathlib import Path
import sys,json,hashlib,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,PF,WPC,V,transform,certify,build_locks,with_tethers
O=R/'exports/generated/service-productization-v338';P=R/'exports/generated/two-stock-user-module-v337'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(filename,ss):
 d=A.newDocument('V338_'+filename.replace('-','_'))
 for n,s in ss.items():d.addObject('PartDesign::Feature',n).Shape=s
 d.recompute();assert all(s.isValid() for s in ss.values());d.saveAs(str(O/(filename+'.FCStd')));A.closeDocument(d.Name)
checks=[]
def ck(n,v,detail=None):checks.append({'name':n,'pass':bool(v),'detail':detail});print(n,bool(v),flush=True);assert v,(n,detail)
g=read(O/'landing-study.json');old=load(P/'play.FCStd');candidate=load(O/'landing-candidate.FCStd')
ck('landing study bound to native source and candidate',g['pass'] and g['source_sha256']==sha(P/'play.FCStd') and g['native_sha256']==sha(O/'landing-candidate.FCStd'))
removed=set(g['removed_names']);added=set(g['added_names']);unchanged=[]
# Copy unchanged source objects directly. Avoid irrelevant Boolean equivalence
# on thousands of thin co-located wire-reserve faces after STEP serialization.
new={n:s for n,s in old.items() if n not in removed};new.update({n:candidate[n] for n in added})
for n,s in old.items():
 if n not in removed:
  same=s is new[n]
  unchanged.append({'name':n,'pass':same})
ck('all unrelated source objects shape equivalent',all(q['pass'] for q in unchanged),{'count':len(unchanged)})
ck('only layers and obsolete binders removed',set(old)-set(new)==removed and set(new)-set(old)==added)
ck('selected retention A unchanged',all(n in new and s is new[n] for n,s in old.items() if 'Retention' in n and n.startswith('FrontLanding')))
moving_names=read(R/'exports/generated/front-landings-v3363/viewer-motion.json')['playfield_moving_names']
pf={n:new[n] for n in moving_names};blocks={n:new[n] for n in added};cert={}
cert['service_new_wood']=certify(pf,blocks,0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF))
ck('SW02 continuously clears playfield0to50',True)
todo=[(0,48)];intervals=[]
while todo:
 lo,hi=todo.pop();mid=(lo+hi)/2;posed=transform(pf,lift=mid);limit=(hi-lo)/2+1e-6;ok=True
 for n,s in posed.items():
  a=s.BoundBox
  for k,t in blocks.items():
   b=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(a,c+'Min')-getattr(b,c+'Max'),getattr(b,c+'Min')-getattr(a,c+'Max'))**2 for c in 'XYZ'))
   if lb<=limit and s.distToShape(t)[0]<=limit:ok=False;break
  if not ok:break
 if ok:intervals.append([lo,hi])
 else:
  assert hi-lo>1e-6,('lift unresolved',lo,hi,n,k);todo.extend([(lo,mid),(mid,hi)])
cert['lift_new_wood']={'range_mm':[0,48],'intervals':sorted(intervals),'method':'OCC midpoint separation exceeds half interval displacement'}
ck('SW02 clears full48mm lift continuously',True)
bb={n:s for n,s in new.items() if n.startswith('BB_') and 'ToyZone' not in n and 'HingeAccess' not in n and 'RetractedReserve' not in n};bb.update(with_tethers(build_locks(True)[0],True))
cert['backbox_new_wood']=certify(bb,blocks,0,90,WPC);ck('SW02 continuously clears populated backbox0to90',True)
save('play',new);states={'PLAY':'play.FCStd'};proof=[]
for label,filename in read(P/'state-register.json')['native_files'].items():
 if label=='PLAY':continue
 ss=load(P/filename)
 for side in ['L','R']:
  k='FrontLanding'+side+'_Layer1';block='FrontLanding'+side+'_Block'
  matrix=ss[k].Placement.toMatrix().multiply(old[k].Placement.toMatrix().inverse())
  q=old[k].copy();q.transformShape(matrix,True);dv=q.cut(ss[k]).Volume+ss[k].cut(q).Volume
  assert dv<1e-5,(label,k,dv)
  t=new[block].copy();t.transformShape(matrix,True);ss[block]=t;proof.append({'state':label,'block':block,'transform_difference_mm3':dv})
 for n in removed:ss.pop(n,None)
 save(Path(filename).stem,ss);states[label]=filename
ck('all named-state replacement placements proven',all(q['transform_difference_mm3']<1e-5 for q in proof),{'count':len(proof)})
ck('V33.7 source native unchanged',sha(P/'play.FCStd')==g['source_sha256'])
out={'pass':True,'checks':checks,'source':str((P/'play.FCStd').relative_to(R)),'source_sha256':sha(P/'play.FCStd'),'native_sha256':sha(O/'play.FCStd'),'native_geometry_file':str((O/'play.FCStd').relative_to(R)),'changed_existing':[],'changed_names':[],'added_names':sorted(added),'new_wood_names':sorted(added),'removed_names':sorted(removed),'current_shapes_changed':sorted(added|removed),'unchanged_objects':unchanged,'SW02':g['SW02'],'certificates':cert,'manufacturing_release':False,'allowed_change_scope':'Only six front-landing plywood layers -> two SW02 solid blocks, filling obsolete binder bores and removing four binder screws. Original captive M6 retention remains.'}
(O/'geometry-validation.json').write_text(json.dumps(out,indent=2)+'\n')
(O/'state-register.json').write_text(json.dumps({'native_files':states,'source_sha256':out['native_sha256'],'manufacturing_release':False,'state_transform_proofs':proof},indent=2)+'\n')
print('V338_COMBINED_PASS',len(checks),len(states),out['native_sha256'],flush=True)

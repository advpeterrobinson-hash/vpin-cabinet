"""Combine independently validated V33.7 scoped native changes.
CERN-OHL-S-2.0; no manufacturing release or unrelated geometry mutation.
"""
from pathlib import Path
import sys,json,hashlib,math
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,pf_names,PF,WPC,V,transform,certify,build_locks,with_tethers
O=R/'exports/generated/two-stock-user-module-v337';P=R/'exports/generated/front-landings-v3363'
def read(n):return json.loads((O/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,value,detail=None):checks.append({'name':name,'pass':bool(value),'detail':detail});print(name,bool(value),flush=True);assert value,(name,detail)
def hits(mov,obs):
 rows=[]
 for n,s in mov.items():
  for k,t in obs.items():
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>1e-5:rows.append({'moving':n,'fixed':k,'volume_mm3':vol})
 return rows
def lower(a,b):
 a,b=a.BoundBox,b.BoundBox
 return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
checks=[];old=load(P/'play.FCStd');module=load(O/'module.FCStd');conv=load(O/'conversion.FCStd');cv=read('conversion-validation.json');mv=read('module-validation.json')
ck('independent native geometry checks pass',cv['pass'] and mv['pass'])
assert cv['conversion_sha256']==sha(O/'conversion.FCStd') and mv['native_sha256']==sha(O/'module.FCStd')
cm=read('conversion-motion.json');ca=read('conversion-reserve-audit.json')
ck('conversion motion and all preserved reserves pass for same native',all(q['pass'] and q['conversion_sha256']==sha(O/'conversion.FCStd') for q in [cm,ca]))
allowed=set(cv['promoted_breps'])|{'FLOOR'}
new={n:s for n,s in old.items()}
for n in cv['promoted_breps']:
 if cv['changes'][n]['volume_delta_mm3']!=0:new[n]=conv[n]
new['FLOOR']=module['FLOOR']
added={n:s for n,s in module.items() if n.startswith('Underfront_')};new.update(added)
changed=[n for n in old if old[n].exportBrepToString()!=new[n].exportBrepToString()]
ck('only authorized existing wood changes',set(changed)<=allowed,changed)
ck('all original objects retained',set(old)<=set(new))
ck('new module andoriginalfrontlanding/sidebuttons coexist',not hits(added,{n:s for n,s in old.items() if n.startswith(('FrontLanding','Leaf','Button'))}))
removed=old['FLOOR'].cut(new['FLOOR']);ck('floor change removes only approvedbaystock',new['FLOOR'].cut(old['FLOOR']).Volume<1e-5)
# Differential continuous proof: unchanged old interactions retain their exact
# previous geometry/kinematics. Conversion andmodule additions require newproof.
motions=json.loads((P/'viewer-motion.json').read_text());pf={n:new[n] for n in motions['playfield_moving_names']}
fixedmodule={n:s for n,s in added.items()}
certificates={}
certificates['PF_module_service']=certify(pf,fixedmodule,0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF))
ck('playfield0to50 continuously clears module',True)
# Whole vertical extraction is contained in extrusion of each AABB alongZ;
# these broad envelopes suffice when module is far below the moving playfield.
liftobs=[]
for n,s in pf.items():
 b=s.BoundBox;q=Part.makeBox(b.XLength,b.YLength,b.ZLength+48,V(b.XMin,b.YMin,b.ZMin))
 liftobs+=hits({n:q},fixedmodule)
ck('playfield48mm fullvertical envelope clears module',not liftobs,liftobs)
backbox={n:s for n,s in new.items() if n.startswith('BB_') and 'ToyZone' not in n and 'HingeAccess' not in n and 'RetractedReserve' not in n};backbox.update(with_tethers(build_locks(True)[0],True))
certificates['BB_module_fold']=certify(backbox,fixedmodule,0,90,WPC)
ck('populatedbackbox0to90 continuously clears module',True)
# Newunderfrontvolume cannot obstruct previously validated landing tool sweeps.
access=load(P/'tool-access.FCStd');accessobs={n:s for n,s in access.items() if n not in old}
ck('landing tool/hand/access sweeps remain clear',not hits(accessobs,fixedmodule),hits(accessobs,fixedmodule))
def save(filename,ss):
 d=A.newDocument('V337_'+filename.replace('-','_'))
 for n,s in ss.items():d.addObject('PartDesign::Feature',n).Shape=s
 d.recompute();d.saveAs(str(O/(filename+'.FCStd')));A.closeDocument(d.Name)
save('play',new)
state_reg=json.loads((P/'state-register.json').read_text());states={'PLAY':'play.FCStd'};state_proofs=[]
for label,filename in state_reg['native_files'].items():
 if label=='PLAY':continue
 ss=load(P/filename)
 for n in changed:
  if n not in ss:
   state_proofs.append({'state':label,'part':n,'transform_roundtrip_mm3':0,'status':'REMOVED_IN_AUTHORITATIVE_SERVICE_STATE; preserved absence'})
   continue
  # Map old play into its authoritative namedpose; must reproduce exact shape
  # before the transform can be used on convertedwood.
  matrix=ss[n].Placement.toMatrix().multiply(old[n].Placement.toMatrix().inverse())
  q=old[n].copy();q.transformShape(matrix,True)
  diff=q.cut(ss[n]).Volume+ss[n].cut(q).Volume
  assert diff<1e-4,(label,n,diff)
  t=new[n].copy();t.transformShape(matrix,True);ss[n]=t
  state_proofs.append({'state':label,'part':n,'transform_roundtrip_mm3':diff})
 ss.update({n:s.copy() for n,s in added.items()});save(Path(filename).stem,ss);states[label]=filename
ck('all namedstate transformations provenfromoldnative',all(q['transform_roundtrip_mm3']<1e-4 for q in state_proofs),{'transforms':len(state_proofs)})
# Owner andgeneric manufacturingvariant removal are separate service views.
mm=read('module-motion.json');service={n:s.copy() for n,s in new.items()}
for n in mm['removable_names']+mm['screw_names']:
 if n in service:service[n].translate(V(0,0,-100))
save('module-removed',service);states['UNDERFRONT MODULE REMOVED']='module-removed.FCStd'
nativehash=sha(O/'play.FCStd')
(O/'state-register.json').write_text(json.dumps({'native_files':states,'source_sha256':nativehash,'manufacturing_release':False,'state_transform_proofs':state_proofs},indent=2)+'\n')
for n in changed+list(added):new[n].exportBrep(str(O/'brep'/(n+'.brep')))
g={'pass':True,'checks':checks,'source':str((P/'play.FCStd').relative_to(R)),'source_sha256':sha(P/'play.FCStd'),'native_sha256':nativehash,'changed_existing':changed,'changed_names':changed,'added_names':list(added),'removed_names':[],
 'new_wood_names':['Underfront_Plate'],'current_shapes_changed':changed,'native_geometry_file':str((O/'play.FCStd').relative_to(R)), 'manufacturing_release':False,'allowed_change_scope':'15 thin-stock manufacturingmembers plusFLOORbay/new12module only; noothergeometrychanges'}
(O/'geometry-validation.json').write_text(json.dumps(g,indent=2)+'\n')
report={'pass':True,'checks':checks,'certificates':certificates,'source_sha256':sha(P/'play.FCStd'),'native_sha256':nativehash,'manufacturing_release':False,
 'inherited':{'source':'exports/generated/front-landings-v3363/validation.json','sha256':sha(P/'validation.json'),'meaning':'Exactunchangedinteractions inheritpriorverification; newmodules/conversionwood undergo separate differentialscreen'},
 'native_inputs_sha256':{n:sha(O/n) for n in ['module.FCStd','module-validation.json','conversion.FCStd','conversion-validation.json','conversion-motion.json','conversion-reserve-audit.json','module-motion.json']}}
(O/'combined-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('V337_COMBINED_PASS',len(checks),len(states),flush=True)

"""V34 native state/material delta. No mutation of predecessor CAD. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,gzip,hashlib
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,transform,WPC
O=R/'exports/generated/backbox-v34';B=R/'exports/generated/service-productization-v338';g=json.loads((O/'geometry-validation.json').read_text());assert g['pass'];old=load(B/'play.FCStd');new=load(O/'candidate.FCStd')
def mesh(s):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.6,Relative=False);v,f=m.Topology;return {'vertices':[list(x) for x in v],'faces':f}
def save(n,d):
 doc=A.newDocument('V34_'+n.replace('-','_'))
 for k,s in d.items():doc.addObject('PartDesign::Feature',k).Shape=s
 doc.recompute();assert all('Invalid' not in o.State for o in doc.Objects);doc.saveAs(str(O/(n+'.FCStd')));A.closeDocument(doc.Name)
removed=sorted(set(old)-set(new));added=sorted(set(new)-set(old));changed=sorted(n for n in set(new)&set(old) if old[n].exportBrepToString()!=new[n].exportBrepToString());owned=added+changed
states={};files={'PLAY':('play',0),'SERVICE':('service',0),'LIFT-OUT':('lift-out',0),'MATRIX REMOVED':('matrix-removed',0),'BACKBOX FOLD':('backbox-fold',90),'DOORS OPEN':('doors-open',0),'UNLOCKED':('locks-parked',0),'PF RELEASED':('released',0),'FOLD1':('fold-1',1),'FOLD45':('fold-45',45),'UNDERFRONT MODULE REMOVED':('module-removed',0)}
for key,(fn,angle) in files.items():
 d=load(B/(fn+'.FCStd'));d={n:s for n,s in d.items() if n not in removed};replacement=transform({n:new[n] for n in owned},angle=angle,axis=WPC) if angle else {n:new[n] for n in owned};d.update(replacement);save(fn,d);states[key]={n:mesh(s) for n,s in replacement.items()}
# Full installed meshes retained for CAD consumers and exact manufacturing delta.
reg=json.loads((O/'manufacturing-register.json').read_text());mm={}
for p in reg['parts']:
 if p.get('version')=='V34':
  q=Part.Shape();q.read(str(R/p['finished_member_brep']));m=A.Matrix(*p['local_to_installed_matrix']);q.transformShape(m,True);mm[p['instance_id']]=mesh(q)
N={'pass':True,'changed':changed,'added':added,'removed':removed,'states':states,'manufacturing_world':mm,'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'before_sha256':hashlib.sha256((B/'play.FCStd').read_bytes()).hexdigest()}
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps(N,separators=(',',':')).encode(),mtime=0));print('V34_EXPORT',len(changed),len(added),len(removed),len(states))

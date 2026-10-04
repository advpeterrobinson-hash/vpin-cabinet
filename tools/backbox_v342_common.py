"""Original V34.2 CAD helpers. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,math,hashlib,gzip
import FreeCAD as A,Part,MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,V,WPC,transform,actual,certify,route
from backbox_service_v32 import door_pose
O=R/'exports/generated/backbox-v342';O.mkdir(parents=True,exist_ok=True)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def shift(s,x=0,y=0,z=0):q=s.copy();q.translate(V(x,y,z));return q
def cy(x,y,z,r,h):return Part.makeCylinder(r,h,V(x,y,z),V(0,1,0))
def rr(x,y,z,w,d,h,r):
 q=box(x+r,y,z,w-2*r,d,h).fuse(box(x,y,z+r,w,d,h-2*r))
 for xx in [x+r,x+w-r]:
  for zz in [z+r,z+h-r]:q=q.fuse(cy(xx,y,zz,r,d))
 return q.removeSplitter()
def slot(x,y,z,width,travel,d):return cy(x,y,z-travel/2,width/2,d).fuse(cy(x,y,z+travel/2,width/2,d)).fuse(box(x-width/2,y,z-travel/2,width,d,travel)).removeSplitter()
def bb(s):b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def mesh(s):
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.6,Relative=False);v,f=m.Topology;return {'vertices':[list(x) for x in v],'faces':f}
def save(n,ss):
 doc=A.newDocument('V342_'+n.replace('-','_'))
 for k,s in ss.items():doc.addObject('PartDesign::Feature',k).Shape=s
 doc.recompute();assert all('Invalid' not in o.State for o in doc.Objects);doc.saveAs(str(O/(n+'.FCStd')));A.closeDocument(doc.Name)
def dump(n,d):(O/(n+'.json')).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def hits(mov,obs,tol=.01):
 h=[]
 for n,q in mov.items():
  for k,t in obs.items():
   if n==k or not q.BoundBox.intersect(t.BoundBox):continue
   vv=q.common(t).Volume
   if vv>tol:h.append({'part':n,'obstacle':k,'mm3':vv})
 return h

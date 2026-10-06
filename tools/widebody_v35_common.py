"""Original V35 standard-widebody study. CERN-OHL-S-2.0."""
from backbox_v342_common import *
O=R/'exports/generated/widebody-v35';O.mkdir(parents=True,exist_ok=True)
W=628.65;DELTA=W-600;CENTER=W/2;DX=CENTER-300
C=json.loads((R/'config/widebody_v35.json').read_text())
def dump(n,d):(O/(n+'.json')).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def save(n,ss):
 doc=A.newDocument('V35_'+n.replace('-','_'))
 for k,s in ss.items():doc.addObject('PartDesign::Feature',k).Shape=s
 doc.recompute();doc.saveAs(str(O/(n+'.FCStd')));A.closeDocument(doc.Name)
def extend_at(q,x,amount):
 # Add an analytic constant-section span at a feature-free station. No scaling.
 left=q.common(box(-2000,-2000,-2000,x+2000,5000,5000));right=q.common(box(x,-2000,-2000,3000-x,5000,5000))
 plane=Part.Face(Part.makePolygon([V(x,-2000,-2000),V(x,3000,-2000),V(x,3000,3000),V(x,-2000,3000),V(x,-2000,-2000)]))
 section=q.common(plane)
 if not section.Faces:raise RuntimeError('No section at '+str(x))
 fill=Part.makeCompound([f.extrude(V(amount,0,0)) for f in section.Faces])
 return left.fuse(shift(right,x=amount)).fuse(fill).removeSplitter()
def widen(q):return extend_at(extend_at(q,100,DX),500+DX,DX)
def mirror(q):m=A.Matrix();m.A11=-1;m.A14=W;return q.transformGeometry(m)
G=json.loads((R/'exports/generated/backbox-v342/geometry-validation.json').read_text())
# Derive frame from unchanged source channel / glass faces.
p0=load(R/C['source']);face=max(p0['CandidateGlass'].Faces,key=lambda f:f.Area);nv=face.normalAt(0,0)
if nv.z<0:nv=-nv
ANG=math.degrees(math.atan2(-nv.y,nv.z));ca=math.cos(math.radians(ANG));sa=math.sin(math.radians(ANG))
verts=[v.Point for v in p0['CandidateGlassChannelL'].Vertexes];T0=min(v.y*ca+v.z*sa for v in verts);N0=min(-v.y*sa+v.z*ca for v in verts)
def tf(q):q=q.copy();q.rotate(V(),V(1,0,0),ANG);q.translate(V(0,T0*ca-N0*sa,T0*sa+N0*ca));return q
def local(q):q=q.copy();q.translate(V(0,-(T0*ca-N0*sa),-(T0*sa+N0*ca)));q.rotate(V(),V(1,0,0),-ANG);return q

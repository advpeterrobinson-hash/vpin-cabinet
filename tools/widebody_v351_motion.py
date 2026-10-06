"""Independent continuous clearance certificates; no raised-service load proof."""
from widebody_v351_common import *
from pivot_cradle_integration_v32 import PF
p=load(O/'candidate.FCStd');reg=json.loads((O/'manufacturing-register.json').read_text());wood={a['source_component']:p[a['source_component']] for a in reg['parts'] if a['source_component'] in p};checks=[];certs={}
def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d});print(n,bool(b),flush=True);dump('continuous-motion',{'checks':checks,'certificates':certs,'pass':all(a['pass'] for a in checks),'physical_support_qualified':False})
pfn=['PF_BasePlywood','PF_WoodDowel','PF_VESAEnvelope','PLAYFIELD_ENVELOPE'];obs={n:q for n,q in wood.items() if n not in pfn and n!='MatrixCarrier'}
obs.update({n:p[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR','CommercialSiderailL','CommercialSiderailR','PF_RearGlassChannel']})
obs.update({n:q for n,q in p.items() if n.startswith(('Leaf','Button'))})
# Translation certificate; zero-height intentional cradle tangent is handled analytically below.
def linear(mov,ob):
 todo=[(.001,48)];out=[]
 while todo:
  lo,hi=todo.pop();mid=(lo+hi)/2;ss=transform(mov,lift=mid);lim=(hi-lo)/2+1e-7;ok=True
  for n,q in ss.items():
   for m,t in ob.items():
    b,c=q.BoundBox,t.BoundBox;lb=sum(max(0,getattr(b,k+'Min')-getattr(c,k+'Max'),getattr(c,k+'Min')-getattr(b,k+'Max'))**2 for k in 'XYZ')**.5
    if lb>lim:continue
    if q.distToShape(t)[0]<=lim:ok=False;break
   if not ok:break
  if ok:out.append([lo,hi])
  else:
   assert hi-lo>1e-5,('lift unproven/collision',n,m,lo,hi)
   todo.extend([(lo,mid),(mid,hi)])
 return {'range_mm':[.001,48],'certified_intervals':out}
for n in pfn:
 ob=dict(obs)
 if n=='PF_WoodDowel':
  # Dowel is a circular cylinder concentric with PF axis; pure X rotation is invariant.
  for k in ['PF_OpenCradleL','PF_OpenCradleR']:ob.pop(k,None)
  ck('dowel seat rotation invariant',abs(p[n].BoundBox.YLength-32)<1e-6 and abs(p[n].BoundBox.ZLength-32)<1e-6 and abs(p[n].BoundBox.Center.y-PF.y)<1e-6 and abs(p[n].BoundBox.Center.z-PF.z)<1e-6)
 try:certs[n+'_rotate']=certify({n:p[n]},ob,0,50,PF,poser=lambda ss,a:transform(ss,angle=-a,axis=PF));ck('continuous PF rotation '+n,True)
 except AssertionError as e:ck('continuous PF rotation '+n,False,str(e))
 try:certs[n+'_lift']=linear({n:p[n]},dict(obs));ck('continuous PF lift '+n,True)
 except AssertionError as e:ck('continuous PF lift '+n,False,str(e))
# Accepted three-phase matrix route: rock26deg around rear edge, forward68mm, lift100mm.
mx={n:q for n,q in p.items() if n=='MatrixCarrier' or n.startswith('MatrixPanel')};mo={n:q for n,q in wood.items() if n not in mx}
mo.update({n:p[n] for n in ['PLAYFIELD_ENVELOPE','CandidateGlassChannelL','CandidateGlassChannelR','PF_RearGlassChannel']})
axis=V(CENTER,1120.0535808591117,586.6345997465683);tests=[]
for phase,values in [('rock',[i*.25 for i in range(105)]),('forward',range(0,69,2)),('lift',range(0,101,2))]:
 for value in values:
  posed=transform(mx,angle=-value if phase=='rock' else -26,axis=axis)
  if phase!='rock':posed={n:shift(q,y=-value if phase=='forward' else -68,z=value if phase=='lift' else 0) for n,q in posed.items()}
  h=hits(posed,mo)
  if h:tests.append({'phase':phase,'value':value,'hits':h})
ck('matrix accepted rock/forward/lift route',not tests,{'samples':191,'hits':tests})

assert all(a["pass"] for a in checks), "Continuous motion / matrix gate failed"

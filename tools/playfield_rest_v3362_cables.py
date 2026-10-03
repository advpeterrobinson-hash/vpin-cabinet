"""Flexible constant-length playfield cable-loop packaging study, not cable selection.
CERN-OHL-S-2.0. Numerical sampled access evidence; cable/anchor hardware stays HOLD.
"""
from pathlib import Path
import sys,json,math,gzip,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,V
O=R/'exports/generated/playfield-rest-v3362';ss=load(O/'play.FCStd');rev=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review'];a=math.radians(rev['closed_slope_deg']);bz=400.05+45*math.tan(a)-12-55*math.cos(a)
start=V(300,45+877*math.cos(a)+20*math.sin(a),bz+877*math.sin(a)-20*math.cos(a));end=V(450,900,258)
r=4.;length=400.;rows=[];scenes={}
def point(p,b,t):return p*(1-t)+end*t+V(4*b*t*(1-t),0,0)
def poly(p,b):return [point(p,b,i/80) for i in range(81)]
def plen(ps):return sum((q-p).Length for p,q in zip(ps,ps[1:]))
def loop(p):
 lo,hi=0.,250.
 for _ in range(40):
  b=(lo+hi)/2;ps=poly(p,b)
  if plen(ps)<length:lo=b
  else:hi=b
 b=(lo+hi)/2;ps=poly(p,b);s=[]
 for p,q in zip(ps,ps[1:]):s.append(Part.makeCylinder(r,(q-p).Length,p,q-p))
 for p in ps:s.append(Part.makeSphere(r,p))
 return Part.makeCompound(s),b,ps
states=[('PLAY',0,0),('SERVICE50',50,0),('LIFT48',0,48)]+[(f'SERVICE{a}',a,0) for a in range(1,50)]+[(f'LIFT{z}',0,z) for z in range(4,48,4)]
for label,ang,lift in states:
 p=Part.Vertex(start);p.rotate(PF,V(1,0,0),-ang);p.translate(V(0,0,lift));p=p.Vertexes[0].Point
 cable,b,ps=loop(p);obs=dict(actual(ss));moving={n:s for n,s in obs.items() if n in pf_names(ss)};obs.update(transform(moving,angle=-ang,axis=PF))
 if lift:
  for n in moving:q=obs[n].copy();q.translate(V(0,0,lift));obs[n]=q
 # Main glass and matrix removed for service/lift. Future optional payloads are
 # screened separately; the reserved S3 clamp sits above its shelf, never in wood.
 obs={n:s for n,s in obs.items() if n!='CandidateGlass' and not n.startswith('Matrix')}
 obs.update({n:s for n,s in ss.items() if n.startswith('SSF_') and 'Reserve' in n})
 hh=[];minimum=1e9
 for n,s in obs.items():
  if not cable.BoundBox.intersect(s.BoundBox):continue
  vol=cable.common(s).Volume
  if vol>1e-4:hh.append([n,vol])
  minimum=min(minimum,cable.distToShape(s)[0])
 radii=[]
 dp=end-p
 for i in range(81):
  t=i/80;v=dp+V(4*b*(1-2*t),0,0);acc=V(-8*b,0,0);cross=v.cross(acc).Length
  if cross>1e-8:radii.append(v.Length**3/cross)
 rows.append({'state':label,'angle_deg':ang,'lift_mm':lift,'length_mm':plen(ps),'minimum_bend_radius_mm':min(radii),'hits':hh,'screened_minimum_mm':minimum})
 if label in ['PLAY','SERVICE50','LIFT48']:
  cable.exportBrep(str(O/'brep'/('CableLoop_'+label+'.brep')))
print('CABLE_ROWS',len(rows),'failed',[(r['state'],r['hits']) for r in rows if r['hits']],flush=True)
report={'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'pass':not any(r['hits'] for r in rows),'method':'Constant 400mm flexible parabolic centerline; varying lateral bow, R4 swept packaging tube, 1 degree rotation /4mm lift samples. NOT a continuous-motion certificate or selected cable bending specification.','diameter_mm':8,'loop_length_mm':400,'minimum_required_reference_bend_radius_mm':35,'fixed_end_mm':list(end),'fixed_end_mount':'Provisional removable clamp on S3 top at X450/Y900; no permanent drill introduced. Release clamp for S3 removal. Clamp/adhesive fastening and actual cable remain hardware-dependent.','moving_end_local_mm':[300,877,-20],'rows':rows,'release':False}
report['pass']=report['pass'] and min(r['minimum_bend_radius_mm'] for r in rows)>=35
(O/'cable-study.json').write_text(json.dumps(report,indent=2)+'\n');print('V3362_CABLE_STUDY',report['pass'],flush=True)

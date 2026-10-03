"""Read-only V33.6 contour history metrology. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A, Part, json, math
R=Path(__file__).resolve().parents[2];O=R/'studies/monitor-support-v336';V=A.Vector
paths={'clean':'exports/generated/wood-dowel-pivot-v32/play.FCStd','notch':'exports/generated/notch-floor-fans-v32/play.FCStd','lock':'exports/generated/backbox-lock-integration-v32/play.FCStd','current':'exports/generated/structural-v335/play.FCStd'}
ss={}
for k,f in paths.items():
 d=A.openDocument(str(R/f));ss[k]=d.getObject('PF_BasePlywood').Shape.copy();A.closeDocument(d.Name)
r=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review'];a=r['closed_slope_deg'];bz=400.05+45*math.tan(math.radians(a))-12-55*math.cos(math.radians(a))
def inv(s):
 q=s.copy();q.translate(V(0,-45,-bz));q.rotate(V(),V(1,0,0),-a);return q
result={'sources':paths,'volume_mm3':{k:s.Volume for k,s in ss.items()},'symmetric_difference_mm3':{k:ss['current'].cut(s).Volume+s.cut(ss['current']).Volume for k,s in ss.items()},'local_bounds':{},'local_contours':{}}
for k,s in ss.items():
 q=inv(s);b=q.BoundBox;result['local_bounds'][k]=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
 faces=[f for f in q.Faces if type(f.Surface).__name__=='Plane' and abs(f.normalAt(0,0).z)>0.99]
 face=max(faces,key=lambda f:f.Area);result['local_contours'][k]=[[list(v) for v in e.discretize(20)] for e in face.OuterWire.Edges]
(O/'history-metrology.json').write_text(json.dumps(result,indent=2)+'\n');print('HISTORY_METROLOGY_PASS',result['symmetric_difference_mm3'])

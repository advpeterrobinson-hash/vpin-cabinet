"""Read-only metrology for owner V33.5 interfaces. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part,json
R=Path(__file__).resolve().parents[1];d=A.openDocument(str(R/'exports/generated/backbox-lock-integration-v32/play.FCStd'));rows=[]
for o in d.Objects:
 if not hasattr(o,'Shape') or o.Shape.isNull():continue
 s=o.Shape;b=s.BoundBox;r={'name':o.Name,'bounds':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'volume':s.Volume}
 if o.Name in ['PF_OpenCradleL','PF_OpenCradleR']:
  faces=[f for f in s.Faces if type(f.Surface).__name__=='Plane' and abs(f.normalAt(0,0).x)>.99]
  f=max(faces,key=lambda f:f.Area);r['profile']=[{'type':type(e.Curve).__name__,'vertices':[list(v.Point) for v in e.Vertexes],'length':e.Length} for e in f.OuterWire.Edges]
 rows.append(r)
(R/'.work/structural-v335/metrology.json').write_text(json.dumps(rows,indent=2));A.closeDocument(d.Name)
print('METROLOGY_PASS',len(rows))

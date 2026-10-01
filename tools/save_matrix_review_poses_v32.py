"""Save the three requested review poses as actual CAD. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/matrix-hinge-study-v32';r=json.loads((O/'validation.json').read_text());best=r['best_review'];assert best is not None
ref=A.openDocument(str(O/('gap-%0.4f-tilt-%02d.FCStd'%(best['gap_mm'],best['tilt_deg']))));matrix={o.Name:o.Shape.copy() for o in ref.Objects if hasattr(o,'Shape') and o.Name.startswith('Matrix')};checks=[]
for label,inputpose,lift in [('service','service',0),('lift-out','lift-out',0),('matrix-removal','play',100)]:
 d=A.openDocument(str(R/'exports/generated/notch-floor-fans-v32'/(inputpose+'.FCStd')));original={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
 for n,s in matrix.items():
  q=s.copy();q.translate(A.Vector(0,0,lift));o=d.addObject('PartDesign::Feature',n);o.Shape=q
 d.recompute();path=O/(label+'.FCStd');d.saveAs(str(path));A.closeDocument(d.Name);d=A.openDocument(str(path));d.recompute()
 assert all(d.getObject(n).Shape.cut(s).Volume+s.cut(d.getObject(n).Shape).Volume<1e-5 for n,s in original.items())
 assert all(d.getObject(n).Shape.isValid() and len(d.getObject(n).Shape.Solids)==1 for n in matrix)
 assert d.getObject('PF_WoodDowel').TypeId=='Part::Cylinder' and d.getObject('PF_WoodDowel').ExpressionEngine
 checks.append({'check':label+' real CAD baseline pose unchanged; matrix valid; original pivot expressions retained','pass':True});A.closeDocument(d.Name)
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in r['source_hashes'].items());checks.append({'check':'accepted source/viewer bytes unchanged after pose exports','pass':True})
(O/'pose-validation.json').write_text(json.dumps({'checks':checks,'all_pass':True,'best_review':best,'manufacturing_ready':False},indent=2)+'\n');print('MATRIX_POSES_PASS',len(checks),flush=True)

"""Read-only CURRENT landing union metrology. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part,json,hashlib,math
R=Path(__file__).resolve().parents[1];P=R/'exports/generated/two-stock-user-module-v337/play.FCStd';O=R/'exports/generated/service-productization-v338';O.mkdir(exist_ok=True)
d=A.openDocument(str(P));rows=[]
for side in 'LR':
 ss=[d.getObject(f'FrontLanding{side}_Layer{i}').Shape.copy() for i in range(1,4)]
 u=ss[0].fuse(ss[1]).fuse(ss[2]).removeSplitter();b=u.BoundBox;box=Part.makeBox(b.XLength,b.YLength,b.ZLength,A.Vector(b.XMin,b.YMin,b.ZMin))
 features=[]
 for f in u.Faces:
  if type(f.Surface).__name__ in ('Cylinder','Cone'):
   q=f.Surface;data={'surface':type(q).__name__,'radius_mm':getattr(q,'Radius',None),'axis':list(q.Axis),'center':list(q.Center),'bounds':[f.BoundBox.XMin,f.BoundBox.YMin,f.BoundBox.ZMin,f.BoundBox.XMax,f.BoundBox.YMax,f.BoundBox.ZMax]}
   if data not in features:features.append(data)
 planes=[]
 for axis in range(3):
  for edge in ('Min','Max'):
   value=getattr(b,'XYZ'[axis]+edge);faces=[f for f in u.Faces if type(f.Surface).__name__=='Plane' and abs(abs(f.normalAt(0,0)[axis])-1)<1e-6 and abs(f.CenterOfMass[axis]-value)<1e-5]
   planes.append({'axis':'XYZ'[axis],'coordinate_mm':value,'area_mm2':sum(f.Area for f in faces)})
 row={'side':side,'bounds_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'finished_external_dimensions_mm':[b.XLength,b.YLength,b.ZLength],'union_volume_mm3':u.Volume,'blank_volume_mm3':box.Volume,'blank_minus_current_reference_mm3':box.cut(u).Volume,'current_outside_blank_mm3':u.cut(box).Volume,'solids':len(u.Solids),'valid':u.isValid(),'mating_extreme_planes':planes,'reference_surface_features':features,'layer_overlap_mm3':sum(ss[i].common(ss[j]).Volume for i in range(3) for j in range(i+1,3))}
 rows.append(row);u.exportBrep(str(O/f'current-landing-{side}-union.brep'));box.exportBrep(str(O/f'current-landing-{side}-blank.brep'))
out={'version':'V33.8','source':str(P.relative_to(R)),'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'current_landing_bodies':rows,'manufacturing_release':False,'note':'Read-only current B-rep metrology; purchased hardware dimensions remain held.'};(O/'current-landing-metrology.json').write_text(json.dumps(out,indent=2)+'\n')
print('V338_CURRENT_METROLOGY',[(q['side'],q['bounds_mm'],q['union_volume_mm3']) for q in rows],flush=True)
A.closeDocument(d.Name)

"""Read-only CURRENT B-rep metrology. Original CERN-OHL-S-2.0 source."""
from pathlib import Path
import json, hashlib
import FreeCAD as A
R=Path(__file__).resolve().parents[1]; O=R/'library/hardware'; O.mkdir(exist_ok=True)
C=json.loads((R/'config/current_v32.json').read_text()); D=R/C['geometry_directory']
rows=[]; hashes={}
for filename,selection in [('play.FCStd',None),('blank-fans.FCStd',['BB_FanBlankL','BB_FanBlankR'])]:
    path=D/filename;hashes[str(path.relative_to(R))]=hashlib.sha256(path.read_bytes()).hexdigest()
    d=A.openDocument(str(path));d.recompute()
    for o in d.Objects:
        if not hasattr(o,'Shape') or o.Shape.isNull() or selection is not None and o.Name not in selection:continue
        s=o.Shape;b=s.BoundBox; cylinders=[]
        for f in s.Faces:
            surf=f.Surface
            if type(surf).__name__=='Cylinder':
                cylinders.append({'radius_mm':surf.Radius,'axis':list(surf.Axis),'center_xyz_mm':list(surf.Center)})
        rows.append({'object':o.Name,'source':str(path.relative_to(R)), 'label':o.Label,'bounds_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax], 'size_world_mm':[b.XLength,b.YLength,b.ZLength],'center_xyz_mm':list(b.Center),'volume_mm3':s.Volume,'solid_count':len(s.Solids),'valid':s.isValid(),'cylinders':cylinders})
    A.closeDocument(d.Name)
for p in [R/'config/current_v32.json',D/'mesh.json',R/'exports/generated/viewer-v32/index.html']:
    hashes[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
assert len(rows)==438 and all(x['valid'] for x in rows)
(O/'current-object-audit.json').write_text(json.dumps({'source_head':'0aa4ea77531c59274a0b8547a71e731626bd2cf2','coordinate_system':'X left-right; Y front-rear; Z up; mm','input_sha256':hashes,'objects':rows},indent=2)+'\n')
print('HARDWARE_V33_READ_ONLY_AUDIT_PASS',len(rows),flush=True)

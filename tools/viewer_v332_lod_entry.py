"""Read-only V33 hardware tessellation for tablet review. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib
import FreeCAD as A
import MeshPart
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/viewer-v332';O.mkdir(parents=True,exist_ok=True)
c=json.loads((R/'config/hardware_catalog_v33.json').read_text());manifest={'manufacturing_release':False,'linear_deflection_mm':.8,'angular_deflection_rad':.4,'source_hashes':{},'models':[]}
def load(path):
 manifest['source_hashes'][str(path.relative_to(R))]=hashlib.sha256(path.read_bytes()).hexdigest();d=A.openDocument(str(path));s={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name);return s
def mesh(n,s):
 assert s.isValid(),n
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.8,AngularDeflection=.4,Relative=False);v,f=m.Topology
 return {'name':n,'vertices':[list(x) for x in v],'faces':[list(x) for x in f]}
current=load(R/'exports/generated/backbox-lock-integration-v32/play.FCStd');installed={}
for h in c['hardware']:
 for i in h['instances']:
  if i['object'] in current:installed[i['object']]=mesh(i['object'],current[i['object']])
family={}
for h in c['hardware']:
 ss=load(R/h['model']['path']);assert h['id'] in ss;family[h['id']]=mesh(h['id'],ss[h['id']]);manifest['models'].append({'id':h['id'],'triangles':len(family[h['id']]['faces']),'model_status':json.loads((R/h['model']['path']).with_suffix('.json').read_text())['model_status']})
for n,data in [('hardware-lod-installed',installed),('hardware-lod-family',family)]:
 (O/(n+'.json.gz')).write_bytes(gzip.compress(json.dumps(data,separators=(',',':')).encode(),mtime=0))
manifest['pass']=True;manifest['installed_triangles']=sum(len(p['faces']) for p in installed.values());manifest['family_triangles']=sum(len(p['faces']) for p in family.values())
(O/'hardware-lod-validation.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('V332_HARDWARE_LOD_PASS',len(installed),len(family),manifest['installed_triangles'],manifest['family_triangles'],flush=True)

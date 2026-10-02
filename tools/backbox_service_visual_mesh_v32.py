"""Small review-only cable meshes from the saved B-reps. CERN-OHL-S-2.0.
Collision proofs use exact shapes, never these tessellations.
"""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_service_v32 import *
import MeshPart
q=json.loads((O/'validation.json').read_text());data={'states':{},'source_sha256':{}}
for state in ['rear-closed','rear-both-open','fold-1','fold-15','fold-45','fold-90']:
    file=O/q['results']['cad_files'][state];ss=load(file);out={}
    for n,s in ss.items():
        if 'FlexCorridor' not in n:continue
        meshpart=MeshPart.meshFromShape(Shape=s,LinearDeflection=.3,AngularDeflection=.5,Relative=False);vertices,faces=meshpart.Topology
        out[n]={'name':n,'label':n,'vertices':[list(v) for v in vertices],'faces':[list(f) for f in faces]}
        print(state,n,len(vertices),len(faces),flush=True)
    data['states'][state]=out;data['source_sha256'][file.name]=hashlib.sha256(file.read_bytes()).hexdigest()
(O/'flex-visuals.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
print('BACKBOX_SERVICE_VISUAL_MESH_PASS',flush=True)

"""Read-only exact native state meshes for new V33.6.3 viewer components.
CERN-OHL-S-2.0. No authored geometry, manufactured dimensions or motions here.
"""
from pathlib import Path
import json,gzip,hashlib,sys
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load
C=json.loads((R/'config/front_landings_v3363.json').read_text());O=R/C['output'];source=R/C['source'];current=O/'play.FCStd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(s):
 vv,ff=s.tessellate(.35);return {'vertices':[list(v) for v in vv],'faces':ff}
old=load(source);new=load(current);v=json.loads((O/'geometry-validation.json').read_text())
changed={r['name'] if isinstance(r,dict) else r for r in v.get('changed',[])};added=set(new)-set(old);removed=set(old)-set(new);names=changed|added
assert not removed,'Existing objects must not disappear in the support overlay'
checks=[{'name':'existing native families retained','pass':not removed}]
files={'PLAY':'play.FCStd'}
if (O/'state-register.json').exists():files.update(json.loads((O/'state-register.json').read_text())['native_files'])
motion=json.loads((O/'viewer-motion.json').read_text())
if motion.get('released_native_file'):files['PF RELEASED']=motion['released_native_file']
output={'source_sha256':sha(current),'before_sha256':sha(source),'changed':sorted(changed),'added':sorted(added),'removed':sorted(removed),'states':{},'files':{},'checks':checks}
for state,file in files.items():
 p=Path(file);p=p if p.is_absolute() else O/p
 ss=new if p==current else load(p)
 output['states'][state]={n:mesh(ss[n]) if n in ss else None for n in names}
 output['files'][state]={'path':str(p.relative_to(R)),'sha256':sha(p)}
assert sha(current)==output['source_sha256'] and sha(source)==output['before_sha256']
output['pass']=all(x['pass'] for x in checks)
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps(output,separators=(',',':')).encode(),mtime=0));print('V3363_VIEWER_NATIVE_PASS',len(added),len(changed),len(files))

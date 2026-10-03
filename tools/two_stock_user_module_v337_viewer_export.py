"""Read-only V33.7 exact native installed/state mesh overlay. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,sys
import FreeCAD as A
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load
C=json.loads((R/'config/underfront_user_module_v337.json').read_text());O=R/'exports/generated/two-stock-user-module-v337';source=R/C['source'];current=O/'play.FCStd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(s):
 vv,ff=s.tessellate(.35);return {'vertices':[list(v) for v in vv],'faces':ff}
def names(rows):return {x if isinstance(x,str) else x['name'] for x in rows}
old=load(source);new=load(current);v=json.loads((O/'geometry-validation.json').read_text())
changed=names(v['changed_names']);added=set(new)-set(old);removed=set(old)-set(new);owned=changed|added
assert added==names(v['added_names']) and removed==names(v['removed_names'])
MM=json.loads((O/'module-motion.json').read_text());variants={};variant_source=None
if MM.get('variant_only_names'):
 vp=Path(MM['variant_native_file']);variant_source=vp if vp.is_absolute() else R/vp if (R/vp).exists() else O/vp;vs=load(variant_source);variants={n:vs[n] for n in MM['variant_only_names']};assert not set(variants)&set(new)
files=json.loads((O/'state-register.json').read_text())['native_files'];assert 'PLAY' in files
output={'source_sha256':sha(current),'before_sha256':sha(source),'changed':sorted(changed),'added':sorted(added),'removed':sorted(removed),'variant_only_names':sorted(variants),'variant_source':({'path':str(variant_source.relative_to(R)),'sha256':sha(variant_source)} if variant_source else None),'states':{},'files':{},'pass':True}
for state,file in files.items():
 p=Path(file);p=p if p.is_absolute() else O/p;ss=new if p==current else load(p)
 output['states'][state]={n:mesh(ss[n]) if n in ss else None for n in owned};vv={}
 for n,s in variants.items():
  q=s.copy()
  if state=='UNDERFRONT MODULE REMOVED' and n in MM['removable_names']:q.translate(A.Vector(*MM['removal_vector_mm']))
  vv[n]=mesh(q)
 output['states'][state].update(vv);output['files'][state]={'path':str(p.relative_to(R)),'sha256':sha(p)}
assert sha(current)==output['source_sha256'] and sha(source)==output['before_sha256']
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps(output,separators=(',',':')).encode(),mtime=0));print('V337_VIEWER_NATIVE_PASS',len(changed),len(added),len(removed),len(files))

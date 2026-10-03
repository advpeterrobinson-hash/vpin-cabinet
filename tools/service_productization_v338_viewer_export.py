"""Read-only V33.8 native/state/study mesh overlay. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load
C=json.loads((R/'config/service_productization_v338.json').read_text());O=R/'exports/generated/service-productization-v338';source=R/C['source'];current=O/'play.FCStd'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(s):
 vv,ff=s.tessellate(.35);return {'vertices':[list(v) for v in vv],'faces':ff}
def names(rows):return {x if isinstance(x,str) else x['name'] for x in rows}
old=load(source);new=load(current);v=json.loads((O/'geometry-validation.json').read_text());assert v['pass'] and sha(current)==v['native_sha256']
changed=names(v['changed_names']);added=set(new)-set(old);removed=set(old)-set(new);owned=changed|added
assert added==names(v['added_names']) and removed==names(v['removed_names'])
files=json.loads((O/'state-register.json').read_text())['native_files'];assert 'PLAY' in files
output={'source_sha256':sha(current),'before_sha256':sha(source),'changed':sorted(changed),'added':sorted(added),'removed':sorted(removed),'states':{},'files':{},'pass':True}
for state,file in files.items():
 p=Path(file);p=p if p.is_absolute() else O/p;ss=new if p==current else load(p)
 output['states'][state]={n:mesh(ss[n]) if n in ss else None for n in owned};output['files'][state]={'path':str(p.relative_to(R)),'sha256':sha(p)}
sp=O/'modularity-study.FCStd';mv=json.loads((O/'modularity-validation.json').read_text());assert mv['pass'] and mv['source_sha256']==sha(current)
study=load(sp);output['study']={n:mesh(s) for n,s in study.items() if n.startswith(('Accessory','PowerRoute','SignalRoute','MovingPFHarness'))};output['study_source']={'path':str(sp.relative_to(R)),'sha256':sha(sp)}
reg=json.loads((O/'manufacturing-register.json').read_text());output['packing_meshes']={}
for p in reg['parts']:
 if p['manufacturing_part_id']=='SW02':
  s=Part.Shape();s.read(str(R/p['shop_blank_brep']));output['packing_meshes'][p['instance_id']]=mesh(s)
assert sha(current)==output['source_sha256'] and sha(source)==output['before_sha256']
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps(output,separators=(',',':')).encode(),mtime=0));print('V338_VIEWER_NATIVE_PASS',len(changed),len(added),len(removed),len(files),len(output['study']))

"""Native V34.2 state export; historical source untouched. CERN-OHL-S-2.0."""
from backbox_v342_common import *
B=R/'exports/generated/backbox-v34';g=json.loads((O/'geometry-validation.json').read_text());assert g['pass'];old=load(B/'play.FCStd');new=load(O/'candidate.FCStd');variants=load(O/'variants.FCStd')
variants['BB_Generic80TV']=box(-57.5,1127,858,715,70,422).fuse(box(-57.5,1127,858,715,80,125)).removeSplitter()
removed=sorted(set(old)-set(new));added=sorted(set(new)-set(old));changed=sorted(n for n in set(new)&set(old) if old[n].exportBrepToString()!=new[n].exportBrepToString());owned=added+changed
files={'PLAY':('play',0),'SERVICE':('service',0),'LIFT-OUT':('lift-out',0),'MATRIX REMOVED':('matrix-removed',0),'BACKBOX FOLD':('backbox-fold',90),'DOORS OPEN':('doors-open',0),'UNLOCKED':('locks-parked',0),'PF RELEASED':('released',0),'FOLD1':('fold-1',1),'FOLD45':('fold-45',45),'UNDERFRONT MODULE REMOVED':('module-removed',0)}
states={}
for key,(fn,angle) in files.items():
 d={n:s for n,s in load(B/(fn+'.FCStd')).items() if n not in removed};replacement={n:new[n] for n in owned}
 if angle:
  replacement.update(transform({n:s for n,s in replacement.items() if n.startswith('BB_')},angle=angle,axis=WPC));replacement.pop('CandidateGlass',None);d.pop('CandidateGlass',None)
 if key in ['DOORS OPEN','UNLOCKED']:
  for side in ['L','R']:
   ds={n:s for n,s in replacement.items() if n.endswith(side) and n.startswith(('BB_Door','BB_Fan','BB_Lower','BB_PianoLeafDoor'))};replacement.update(door_pose(ds,side,100))
 if key in ['SERVICE','LIFT-OUT','MATRIX REMOVED']:replacement.pop('CandidateGlass',None);d.pop('CandidateGlass',None)
 d.update(replacement);save(fn,d);states[key]={n:mesh(s) for n,s in replacement.items()}
reg=json.loads((O/'manufacturing-register.json').read_text());mm={}
for p in reg['parts']:
 if p.get('version')=='V34.2':
  q=Part.Shape();q.read(str(R/p['finished_member_brep']));q.transformShape(A.Matrix(*p['local_to_installed_matrix']),True);mm[p['instance_id']]=mesh(q)
N={'pass':True,'changed':changed,'added':added,'removed':removed,'states':states,'manufacturing_world':mm,'variants':{n:mesh(s) for n,s in variants.items()},'source_sha256':hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest(),'before_sha256':hashlib.sha256((B/'play.FCStd').read_bytes()).hexdigest()}
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps(N,separators=(',',':')).encode(),mtime=0));(O/'candidate-mesh.json.gz').write_bytes(gzip.compress(json.dumps({n:mesh(s) for n,s in new.items()},separators=(',',':')).encode(),mtime=0));print('V342_EXPORT',len(changed),len(added),len(removed))

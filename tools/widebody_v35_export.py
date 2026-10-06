"""Source-authoritative service poses, rebuilt at V35 width; offline mesh export."""
from widebody_v35_common import *
import numpy as np
p=load(O/'candidate.FCStd');audit=json.loads((O/'width-audit.json').read_text());reg=json.loads((O/'manufacturing-register.json').read_text());fallback=[];states={}
files={'PLAY':'play','SERVICE':'service','LIFT-OUT':'lift-out','MATRIX REMOVED':'matrix-removed','BACKBOX FOLD':'backbox-fold','DOORS OPEN':'doors-open','UNLOCKED':'locks-parked','PF RELEASED':'released','FOLD1':'fold-1','FOLD45':'fold-45','UNDERFRONT MODULE REMOVED':'module-removed'}
def pose(old,posed,new,dx):
 a=np.array([list(v.Point) for v in old.Vertexes]);b=np.array([list(v.Point) for v in posed.Vertexes])
 if len(a)!=len(b):return None
 ca=a.mean(0);cb=b.mean(0);u,sv,vt=np.linalg.svd((a-ca).T@(b-cb));rot=vt.T@u.T
 if np.linalg.det(rot)<0:vt[-1]*=-1;rot=vt.T@u.T
 tr=cb-rot@ca
 if np.max(np.linalg.norm(a@rot.T+tr-b,axis=1))>1e-5:return None
 # The entire source backbox is placed by common centerline translation.
 if dx is not None:off=np.array([dx,0,0]);tr=tr+off-rot@off
 mat=A.Matrix()
 for i in range(3):
  for j in range(3):setattr(mat,'A'+str(i+1)+str(j+1),float(rot[i,j]))
  setattr(mat,'A'+str(i+1)+'4',float(tr[i]))
 q=new.copy();q.transformShape(mat,True);return q
for name,fn in files.items():
 src=load(R/'exports/generated/backbox-v342'/(fn+'.FCStd'));out={}
 for n,q in p.items():
  if n in p0 and n not in src:continue
  if n not in p0:out[n]=q.copy();continue
  old=p0[n];target=src[n]
  if old.exportBrepToString()==target.exportBrepToString():out[n]=q.copy();continue
  nq=pose(old,target,q,audit.get(n,{}).get('translation_x_mm',DX))
  if nq is None:
   if n in {a['source_component'] for a in reg['parts']}:raise RuntimeError('Nonrigid wood state '+name+' '+n)
   nq=shift(target,x=audit.get(n,{}).get('translation_x_mm') or DX);fallback.append({'state':name,'part':n,'reason':'source service hardware shape differs; use exact source shape rigidly centered'})
  out[n]=nq
 if name in ['SERVICE','LIFT-OUT','MATRIX REMOVED']:
  out.pop('CandidateGlass',None);out.pop('PF_LockdownGlassRetainer',None)
  for n in list(out):
   if name!='MATRIX REMOVED' and n.startswith(('Matrix','MX_Retainer')):out.pop(n)
 if name in ['BACKBOX FOLD','FOLD1','FOLD45']:
  out.pop('CandidateGlass',None)
  for n in list(out):
   if n.startswith(('Matrix','MX_Retainer')):out.pop(n)
 save(fn,out);states[name]={n:mesh(q) for n,q in out.items()}
mm={}
for a in reg['parts']:
 q=Part.Shape();q.read(str(R/a['finished_member_brep']));q.transformShape(A.Matrix(*a['local_to_installed_matrix']),True);mm[a['instance_id']]=mesh(q)
variants={n:mesh(q) for n,q in load(O/'variants.FCStd').items()}
(O/'viewer-native.json.gz').write_bytes(gzip.compress(json.dumps({'states':states,'manufacturing_world':mm,'variants':variants,'source_pose_fallbacks':fallback},separators=(',',':')).encode(),mtime=0));dump('state-export',{'states':list(states),'source_pose_fallbacks':fallback})
print('V35_EXPORT',len(states),len(mm),len(fallback),flush=True)

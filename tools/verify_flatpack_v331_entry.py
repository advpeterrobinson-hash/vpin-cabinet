"""Independent saved-part and one-face CNC-stock regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,subprocess
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/flatpack-v331';D=json.loads((O/'manufacturing-register.json').read_text())
def load(path):s=Part.Shape();s.read(str(R/path));return s
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
checks=[]
def check(n,v,details=None):
 checks.append({'check':n,'pass':bool(v),'details':details})
 if not v:raise AssertionError((n,details))
shapes={};world={};results=[]
for p in D['parts']:
 s=load(p['finished_member_brep']);cnc=load(p['cnc_stage_brep']);inst=p['instance_id']
 check(inst+' valid single finished solid',s.isValid() and len(s.Solids)==1)
 overcut=s.cut(cnc).Volume
 check(inst+' CNC stage does not remove accepted wood',overcut<1e-3,overcut)
 remaining=cnc.cut(s).Volume
 if p['manufacturing_status']=='ONE_SIDE_CNC_READY':check(inst+' ready has no unexplained manual residual',remaining<1e-3,remaining)
 check(inst+' one face only',p['machining_face']=='FACE_A' and p['opposite_face']=='FACE_B / NO CNC' and all(op['face']=='FACE_A' for op in p['through_cuts']+p['pockets']))
 if p['manufacturing_status']=='ONE_SIDE_CNC_PLUS_MANUAL_FINISH':check(inst+' explicit manual operations',bool(p['manual_finish']))
 shapes[inst]=s
 q=s.copy();q.transformShape(A.Matrix(*p['local_to_installed_matrix']),True);world[inst]=q
 results.append({'instance':inst,'cnc_overcut_mm3':overcut,'manual_finish_material_mm3':remaining})
source={}
for file in set(p['source'][0] for p in D['parts']):
 doc=A.openDocument(str(R/file))
 for o in doc.Objects:
  if hasattr(o,'Shape'):source[o.Name]=o.Shape.copy()
 A.closeDocument(doc.Name)
assembly_results=[]
for a in D['assemblies']:
 qs=[world[i] for i in a['pieces']];u=qs[0]
 for q in qs[1:]:u=u.fuse(q)
 u=u.removeSplitter();delta=diff(u,source[a['source_component']])
 check(a['id']+' saved member union matches CURRENT',delta<1e-3,delta)
 assembly_results.append({'assembly':a['id'],'difference_mm3':delta})
for fam in D['families']:
 canonical=shapes[fam['instances'][0]]
 for inst in fam['instances']:
  row=next(p for p in D['parts'] if p['instance_id']==inst);s=shapes[inst].copy();s.transformShape(A.Matrix(*row['local_to_canonical_matrix']),True)
  check(inst+' canonical family equivalence',diff(s,canonical)<1e-3)
check('93 installed components fully mapped',len(D['assemblies'])==93 and len({p['instance_id'] for p in D['parts']})==len(D['parts']))
check('15 prior decomposition holds resolved exactly',sum(a['decomposed'] for a in D['assemblies'])==15)
check('No ready member selected from planarity alone',all(p['through_cuts'] is not None and p['pockets'] is not None and p['cnc_stage_brep'] for p in D['parts']))
for path,h in D['source_sha256'].items():check('Source unchanged '+path,hashlib.sha256((R/path).read_bytes()).hexdigest()==h)
# Full pre-task byte protection includes supplier values, V33 and CURRENT/viewer.
count=0
for line in subprocess.check_output(['git','ls-tree','-r','-z',D['source_head']],cwd=R).split(b'\0'):
 if not line:continue
 info,name=line.split(b'\t');mode,kind,sha=info.split()
 if kind!=b'blob':continue
 b=(R/name.decode()).read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest().encode()
 check('Protected '+name.decode(),actual==sha);count+=1
# Negative control: deleting one lamination demonstrably fails union equivalence.
a=next(a for a in D['assemblies'] if a['source_component']=='CandidateLegBlockFL');qs=[world[i] for i in a['pieces'][1:]];u=qs[0]
for q in qs[1:]:u=u.fuse(q)
check('Negative control rejects missing leg layer',diff(u,source[a['source_component']])>1000)
(O/'validation.json').write_text(json.dumps({'pass':True,'checks':checks,'source_head':D['source_head'],
   'unchanged_starting_files':count,'cnc_stage_results':results,'saved_union_results':assembly_results,
   'current_geometry_changed':False,'full_sheet_release':False,'load_certification':False},indent=2)+'\n')
print('FLATPACK_V331_REGRESSION_PASS',len(checks),'checks;',count,'source files unchanged',flush=True)

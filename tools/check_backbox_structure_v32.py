"""Reopen candidate B-reps; independently check hold, scope, joint and saved poses.
CERN-OHL-S-2.0. Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
"""
from pathlib import Path
import hashlib,json,subprocess,math
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-structure-v32';q=json.loads((O/'validation.json').read_text());V=A.Vector;checks=[]
def check(n,v):
 assert v,n
 checks.append(n)
def read(p):
 d=A.openDocument(str(p));d.recompute();check('valid document '+p.name,not any('Invalid' in o.State for o in d.Objects));ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name);return ss
head=q['source_head'];source=R/'exports/generated/matrix-cassette-v32'
# Source blobs, including viewer, must remain exactly as at owner starting HEAD.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',head,'exports/generated/matrix-cassette-v32','exports/generated/viewer-v32','tools/build_review_viewer.py'],cwd=R,text=True).splitlines()
for p in paths:
 data=(R/p).read_bytes();expected=subprocess.check_output(['git','rev-parse',head+':'+p],cwd=R,text=True).strip();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();check('accepted unchanged '+p,actual==expected)
s=read(O/'matrix-removed.FCStd');old=read(source/'matrix-removed.FCStd');moving={n:t for n,t in s.items() if n.startswith('BB_')};check('eight valid moving solids',len(moving)==8 and all(t.isValid() and len(t.Solids)==1 for t in moving.values()))
M=A.Matrix();M.A11=-1;M.A14=600
wood=Part.makeCompound(list(moving.values()));mirror=wood.transformGeometry(M);check('bilateral wood symmetry',wood.cut(mirror).Volume+mirror.cut(wood).Volume<1e-4)
for n,t in old.items():
 if n in ['SIDE_L','SIDE_R','BACKBOX_BASE','PF_BackboxCheckEnvelope']:continue
 check('unchanged isolated component '+n,t.cut(s[n]).Volume+s[n].cut(t).Volume<1e-5)
floor=s['BB_Floor'];shelf=s['BACKBOX_BASE'];contact=Part.makeCompound([f for f in floor.Faces if abs(f.CenterOfMass.z-596.9)<1e-7]).common(Part.makeCompound([f for f in shelf.Faces if abs(f.CenterOfMass.z-596.9)<1e-7]));check('bearing measured independently',abs(contact.Area-65672.4)<1e-5)
for side,x in [('L',18),('R',579)]:
 core=Part.makeCylinder(4.7625,3,V(x,1066.8,508),V(1,0,0));clash=core.common(s['PF_OpenCradle'+side]).Volume
 check(side+' pivot core cannot be installed',abs(clash-213.76721774425624)<1e-5)
 check(side+' actual joint length',abs(s['BB_Floor'].BoundBox.YLength-156.1)<1e-6)
for a,fn in [(1,'fold-1.FCStd'),(15,'fold-15.FCStd'),(45,'fold-45.FCStd'),(90,'backbox-fold.FCStd')]:
 state=read(O/fn)
 for n,t in moving.items():
  expected=t.copy();expected.rotate(V(300,1066.8,508),V(1,0,0),a)
  check(f'actual saved rigid pose {a} {n}',state[n].cut(expected).Volume+expected.cut(state[n]).Volume<1e-5)
check('promotion blocked, no hardware release',q['promoted'] is False and q['promotion_geometry_gates_pass'] is False and not q['manufacturing_ready'] and not q['final_holes_frozen'])
check('all required angles sampled',set([0,.25,.5,1,2,5,10,15,30,45,60,75,90])<=set(r['angle_deg'] for r in q['fold_samples']))
check('sampled wood clear',all(not r['hits'] and r['floor_shelf_penetration_mm3']<1e-6 for r in q['fold_samples']))
# Certificate leaves must form an exact partition and use a valid whole-body radius.
c=q['continuous_certificate'];radius=max(math.hypot(y-1066.8,z-508) for t in moving.values() for y in [t.BoundBox.YMin,t.BoundBox.YMax] for z in [t.BoundBox.ZMin,t.BoundBox.ZMax]);check('motion radius bound',c['radius_mm']>=radius-1e-7)
leaves=sorted(c['intervals'],key=lambda r:r['lo_deg']);end=.001
for r in leaves:
 check('certificate contiguous '+str(end),abs(r['lo_deg']-end)<1e-8)
 check('certificate displacement bound '+str(end),r['motion_bound_mm']>=radius*math.radians((r['hi_deg']-r['lo_deg'])/2)-1e-8 and r['midpoint_clearance']['mm']>r['motion_bound_mm']+1e-6);end=r['hi_deg']
check('certificate ends at 90',abs(end-90)<1e-8)
# Recompute a sparse independent midpoint distance set from reopened solids.
fixed={n:t for n,t in s.items() if n not in moving and n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ['ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'])}
for r in leaves[::20]:
 mid=(r['lo_deg']+r['hi_deg'])/2;n,m=r['midpoint_clearance']['pair'];t=moving[n].copy();t.rotate(V(300,1066.8,508),V(1,0,0),mid);check('saved midpoint distance '+str(mid),abs(t.distToShape(fixed[m])[0]-r['midpoint_clearance']['mm'])<1e-6)
check('mesh hash',hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()==q['mesh_sha256'])
(O/'regression-validation.json').write_text(json.dumps({'pass':True,'checks':checks,'promoted':False,'manufacturing_ready':False,'source_blob_count':len(paths)},indent=2)+'\n')
print('BACKBOX_STRUCTURE_REGRESSION_PASS',len(checks),flush=True)

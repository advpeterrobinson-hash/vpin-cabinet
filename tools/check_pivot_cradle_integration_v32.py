"""Independent reopened-CAD regression for the local cradle integration. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,hashlib,subprocess,math
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from pivot_cradle_integration_v32 import C,load,seat_area,PF,WPC,SR,SEAT,tools_for_pivot,keepout,actual,BASE
O=R/C['output_directory'];q=json.loads((O/'validation.json').read_text());checks=[];V=A.Vector

def check(n,v):
 assert v,n
 checks.append(n)
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
# Historical inputs stay immutable; manufacturing holes are not silently reissued.
for folder in ['exports/generated/matrix-cassette-v32','exports/generated/backbox-structure-v32']:
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['source_head'],folder],cwd=R,text=True).splitlines()
 for p in paths:
  data=(R/p).read_bytes();h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();expected=subprocess.check_output(['git','rev-parse',C['source_head']+':'+p],cwd=R,text=True).strip();check('historical unchanged '+p,h==expected)
old=load(R/C['source_directory']/'play.FCStd');now=load(O/'play.FCStd');modified=['PF_OpenCradleL','PF_OpenCradleR'];check('no added part count',set(old)==set(now))
for n,s in old.items():
 if n not in modified:check('upright preserved '+n,diff(s,now[n])<1e-5)
for side in ['L','R']:
 n='PF_OpenCradle'+side;s=now[n];check(n+' valid 18mm single solid',s.isValid() and len(s.Solids)==1 and abs(s.BoundBox.XLength-18)<1e-7);check(n+' subtractive only',s.cut(old[n]).Volume<1e-6);check(n+' all seat area retained',abs(seat_area(s)-seat_area(old[n]))<1e-7)
 cut=old[n].cut(s);check(n+' all removed wood above seat axis',cut.BoundBox.ZMin>=SEAT.z-1e-7)
 check(n+' reserve exact 2mm margin',abs(s.distToShape(keepout(12)[side])[0]-2)<1e-6)
 # Recreate R5 nominal axis probe from the blocked previous review: now clear.
 core=Part.makeCylinder(4.7625,3,V(18 if side=='L' else 579,WPC.y,WPC.z),V(1,0,0));check(n+' old obstruction gone',core.common(s).Volume<1e-7)
 # Seat floor and all mounting screws lie below the entire relief.
 check(n+' floor foot and screws below relief',max(r['head_xyz_mm'][2]+4.5 for r in BASE['support_mounting']['positions']) < cut.BoundBox.ZMin)
M=A.Matrix();M.A11=-1;M.A14=600;left=now['PF_OpenCradleL'].copy();left.transformShape(M,True);check('mirrored relief and screws',diff(left,now['PF_OpenCradleR'])<1e-5)
for state,fn in q['saved_poses'].items():
 ss=load(O/fn);oo=load(R/C['source_directory']/fn)
 for n,s in ss.items():
  if n in modified:check(state+' fixed support '+n,diff(s,now[n])<1e-5)
  else:check(state+' preserved '+n,diff(s,oo[n])<1e-5)
# Dowel axis invariant under service; accepted unseat is exactly 48 mm.
lift=load(O/'lift-out.FCStd');d=now['PF_WoodDowel'].copy();d.translate(V(0,0,48));check('48mm complete unit lift retained',diff(d,lift['PF_WoodDowel'])<1e-5)
check('dowel clears highest retained ear by 2mm',abs(lift['PF_WoodDowel'].BoundBox.ZMin-now['PF_OpenCradleL'].BoundBox.ZMax-2)<1e-7)
for a,fn in [(1,'fold-1.FCStd'),(45,'fold-45.FCStd'),(90,'backbox-fold.FCStd')]:
 ss=load(O/fn)
 for n,s in now.items():
  if not n.startswith('BB_'):continue
  expected=s.copy();expected.rotate(WPC,V(1,0,0),a);check(f'{a} exact rigid backbox pose '+n,diff(expected,ss[n])<1e-5)
check('all combined samples clear',all(not r['hits'] for key in ['playfield_service_samples','lift_samples','backbox_fold_samples'] for r in q[key]))
for kind,c in q['continuous_new_interface'].items():
 if not isinstance(c,dict) or not c.get('intervals'):continue
 end=c['range'][0]
 for r in sorted(c['intervals'],key=lambda r:r['lo']):
  check(kind+' contiguous '+str(end),abs(r['lo']-end)<1e-7);check(kind+' bound '+str(end),r['midpoint_clearance']['mm']>r['motion_bound_mm']+1e-6);end=r['hi']
 check(kind+' complete',abs(end-c['range'][1])<1e-7)
for radius in [5,8,10,12,15,18,22]:
 ss=load(O/f'R{radius}.FCStd');arc=seat_area(ss['PF_OpenCradleL'])/(SR*18)*180/math.pi
 if radius<=18:check('R'+str(radius)+' full semicircular seat',abs(arc-180)<1e-6)
 else:check('negative R22 shortens seat',arc<179)
check('R12 selected, provisional hardware, manufacturing blocked',q['selected_radius_mm']==12 and q['promoted'] and not q['final_hinge_holes_frozen'] and not q['manufacturing_ready'] and q['custom_metal_added']==0)
check('mesh hash',hashlib.sha256((O/'mesh.json').read_bytes()).hexdigest()==q['mesh_sha256'])
(O/'regression-validation.json').write_text(json.dumps({'pass':True,'checks':checks,'promoted':True,'manufacturing_ready':False},indent=2)+'\n');print('PIVOT_CRADLE_REGRESSION_PASS',len(checks),flush=True)

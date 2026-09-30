"""Screen natural cutter corners in replaceable guides. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,shutil
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/corner-relief-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/corner_relief_v32.json';c=json.loads(cp.read_text());rp=R/'exports/generated/fixed-rear-services-v32/validation.json';r=json.loads(rp.read_text());sp=R/r['saved_proposals']['closed']['path'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sp)==r['saved_proposals']['closed']['sha256'] and all(v['pass'] for v in r['checks'])
inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,Path(__file__).resolve()]}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};old={n:s.copy() for n,s in scene.items()};checks=[];records=[];V=A.Vector;rad=c['trial_cutter_diameter_mm']/2
assert 0<rad<9.2
def check(n,v):checks.append({'check':n,'pass':bool(v)})
for i in (1,2,3):
 beam=scene[f'CROSS_{i}'];bb=beam.BoundBox;center=(bb.YMin+bb.YMax)/2
 for side,x in [('L',30),('R',564)]:
  name=f'CROSS_GUIDE_{i}{side}';s=scene[name];bottom=s.BoundBox.ZMin+20
  # Material naturally left by cutter in two stopped lower groove corners.
  rem=[]
  for y,cy in [(center-9.2,center-9.2+rad),(center+9.2-rad,center+9.2-rad)]:
   square=Part.makeBox(6,rad,rad,V(x,y,bottom))
   disk=Part.makeCylinder(rad,6,V(x,cy,bottom+rad),V(1,0,0))
   rem.append(square.cut(disk))
  s=s.fuse(rem[0]).fuse(rem[1]).removeSplitter();scene[name]=s
  check(name+' valid single solid',s.isValid() and len(s.Solids)==1)
  check(name+' unchanged outer bounds',all(abs(a-b)<1e-6 for a,b in zip([s.BoundBox.XMin,s.BoundBox.XMax,s.BoundBox.YMin,s.BoundBox.YMax,s.BoundBox.ZMin,s.BoundBox.ZMax],[old[name].BoundBox.XMin,old[name].BoundBox.XMax,old[name].BoundBox.YMin,old[name].BoundBox.YMax,old[name].BoundBox.ZMin,old[name].BoundBox.ZMax])))
  check(name+' cutter remainder clears square crossmember',s.common(beam).Volume<1e-6)
  check(name+' added material matches two cutter corners',abs(s.Volume-old[name].Volume-2*6*rad**2*(1-3.141592653589793/4))<1e-5)
  conflicts=[n for n,t in scene.items() if n!=name and s.BoundBox.intersect(t.BoundBox) and s.common(t).Volume>.01]
  check(name+' no installed conflicts',not conflicts)
  # Negative: seating a square crossmember on the stopped end requires relief.
  seated=beam.copy();seated.translate(V(0,0,bottom-bb.ZMin))
  check(name+' reject square board forced to stopped groove bottom',s.common(seated).Volume>.01)
  records.append({'part':name,'groove_floor_z_mm':bottom,'crossmember_bottom_z_mm':bb.ZMin,'gap_below_crossmember_mm':bb.ZMin-bottom,'radius_mm':rad,'remaining_clearance_above_corner_mm':bb.ZMin-bottom-rad,'conflicts':conflicts})
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for i in (1,2,3):
 a=scene[f'CROSS_GUIDE_{i}L'].transformGeometry(mirror);b=scene[f'CROSS_GUIDE_{i}R'];check(f'guide pair{i} symmetric',a.cut(b).Volume+b.cut(a).Volume<1e-5)
changed=[n for n in scene if scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume>1e-6]
check('only six replaceable guides changed',set(changed)=={f'CROSS_GUIDE_{i}{s}' for i in (1,2,3) for s in ('L','R')})
out=A.newDocument('NaturalGuideCorners')
for n,s in scene.items():
 o=out.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(d.getObject(n),'PartCode','')
out.recompute();p=O/'natural-guide-corners.FCStd';out.saveAs(str(p));A.closeDocument(out.Name);out=A.openDocument(str(p));check('reopened valid solids and exact shapes',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and o.Shape.cut(scene[o.Name]).Volume+scene[o.Name].cut(o.Shape).Volume<1e-5 for o in out.Objects if hasattr(o,'Shape')));A.closeDocument(out.Name)
check('all source files unchanged',all(sha(R/p)==h for p,h in inputs.items()))
for name in ('LICENSE','NOTICE.md'):shutil.copyfile(R/name,O/name)
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'guide_results':records,'changed_parts':changed,'saved_cad_sha256':sha(p),'limitations':['Trial6mm cutter only; actual tool not confirmed.','Collision screening not structural proof; no dogbone added to accepted cabinet.','Captured-shell proposal relief and other panel corner/CAM inventory still pending.']};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(v['pass'] for v in checks),[v for v in checks if not v['pass']];print('CORNER_RELIEF_PASS',len(checks),'checks; six guide trials; source unchanged');A.closeDocument(d.Name)

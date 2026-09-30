"""Floor and removable filter mounting study. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,shutil,math
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/floor-detail-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/floor_detail_v32.json';c=json.loads(cp.read_text());rp=R/c['source_report'];r=json.loads(rp.read_text());sp=R/r['saved_proposals']['closed']['path'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sp)==r['saved_proposals']['closed']['sha256'] and all(v['pass'] for v in r['checks'])
inputs={str(p.relative_to(R)):sha(p) for p in (cp,rp,sp,Path(__file__).resolve())};d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};old={n:s.copy() for n,s in scene.items()};V=A.Vector;checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)})
def cylinder(x,y,z,rad,h):return Part.makeCylinder(rad,h,V(x,y,z))
def rounded(x,y,z,w,h,t,rr):
 s=Part.makeBox(w-2*rr,h,t,V(x+rr,y,z)).fuse(Part.makeBox(w,h-2*rr,t,V(x,y+rr,z)))
 for xx in (x+rr,x+w-rr):
  for yy in (y+rr,y+h-rr):s=s.fuse(cylinder(xx,yy,z,rr,t))
 return s.removeSplitter()
def hits(shape,ex=()):return [n for n,s in scene.items() if n not in ex and shape.BoundBox.intersect(s.BoundBox) and shape.common(s).Volume>.01]
floor=Part.makeBox(564,1272.1,18,V(18,18,18)).cut(cylinder(300,440,17,139.7/2,20));rr=c['trial_corner_radius_mm'];b=c['filter_frame_border_mm'];t=c['filter_frame_thickness_mm'];holes=c['filter_fixing_centers_xy_mm']
for i,(x,y,w,h) in enumerate(c['intakes_xywh_mm'],1):
 cut=rounded(x,y,9,w,h,28,rr);floor=floor.cut(cut)
 name=f'CandidateIntakeFilterFrame{i}';frame=rounded(x-b,y-b,18-t,w+2*b,h+2*b,t,rr).cut(cut)
 for xx,yy in holes[(i-1)*4:i*4]:
  drill=cylinder(xx,yy,9,c['filter_fixing_hole_diameter_mm']/2,28);floor=floor.cut(drill);frame=frame.cut(drill)
 scene[name]=frame
 check(name+' valid single solid',frame.isValid() and len(frame.Solids)==1)
 check(name+' lower inner corners rounded',frame.isInside(V(x+.1,y+.1,18-t/2),1e-6,True) and not frame.isInside(V(x+rr,y+rr,18-t/2),1e-6,True))
 # Exact straight removal sweep of holder for80mm below cabinet.
 sweep=rounded(x-b,y-b,18-t-80,w+2*b,h+2*b,t+80,rr).cut(rounded(x,y,18-t-81,w,h,t+82,rr))
 check(name+' withdraws downward80mm in modeled cabinet',not hits(sweep,(name,'FLOOR')))
scene['FLOOR']=floor
for i,(x,y) in enumerate(holes,1):
 check(f'filter hole{i} passes floor and frame',all(not s.isInside(V(x,y,z),1e-6,True) for s,z in [(floor,27),(scene['CandidateIntakeFilterFrame1' if i<=4 else 'CandidateIntakeFilterFrame2'],14)]))
 # Candidate M4x35 underside1mm above cabinet datum; include washer and nut envelopes.
 shaft=cylinder(x,y,1.8,2,35);washer=cylinder(x,y,9.2,4.5,.8);nut=cylinder(x,y,6,4.1,3.2);upper=cylinder(x,y,36,4.5,.8)
 check(f'filter fixing{i} candidate stack clears cabinet',all(not hits(s) for s in [shaft,washer,nut,upper]))
 # Corridor before populated electronics; no real fingers/wrench model.
 check(f'filter fixing{i} tool approach from above',not hits(cylinder(x,y,39.8,6,100)))
 check(f'filter fixing{i} tool approach from below',not hits(cylinder(x,y,-74,6,80)))
check('floor valid single solid',floor.isValid() and len(floor.Solids)==1)
check('floor external bounds preserved',abs(floor.BoundBox.XLength-564)<1e-6 and abs(floor.BoundBox.YLength-1272.1)<1e-6 and abs(floor.BoundBox.ZMin-18)<1e-6 and abs(floor.BoundBox.ZMax-36)<1e-6)
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for n,k in [('FLOOR','FLOOR'),('CandidateIntakeFilterFrame1','CandidateIntakeFilterFrame2')]:
 mirrored=scene[n].transformGeometry(mirror);check(n+' left right symmetry',mirrored.cut(scene[k]).Volume+scene[k].cut(mirrored).Volume<1e-5)
check('four retired unassigned holes remain solid',all(floor.isInside(V(x,90,27),1e-6,True) for x in (185,245,305,365)))
# Confirm actual radius material; a square full-size plug is a rejected negative.
x,y,w,h=c['intakes_xywh_mm'][0];square=Part.makeBox(w,h,18,V(x,y,18));check('square full intake plug rejected atR3 corners',floor.common(square).Volume>1)
changed=[n for n in scene if scene[n].cut(old[n]).Volume+old[n].cut(scene[n]).Volume>1e-6];check('only floor and two filter holders change',set(changed)=={'FLOOR','CandidateIntakeFilterFrame1','CandidateIntakeFilterFrame2'})
conflicts={n:hits(scene[n],(n,)) for n in changed};check('modified parts no installed conflicts',not any(conflicts.values()))
out=A.newDocument('FloorDetail')
for n,s in scene.items():
 o=out.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','PartCode');o.PartCode=getattr(d.getObject(n),'PartCode','')
out.recompute();fp=O/'floor-detail.FCStd';out.saveAs(str(fp));A.closeDocument(out.Name);out=A.openDocument(str(fp));check('saved assembly reopens with valid identical shapes',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and o.Shape.cut(scene[o.Name]).Volume+scene[o.Name].cut(o.Shape).Volume<1e-5 for o in out.Objects if hasattr(o,'Shape')));A.closeDocument(out.Name)
check('source files unchanged',all(sha(R/p)==h for p,h in inputs.items()))
for n in ('LICENSE','NOTICE.md'):shutil.copyfile(R/n,O/n)
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'changed_parts':changed,'installed_conflicts':conflicts,'gross_intake_area_mm2':2*(100*160-(4-math.pi)*rr**2),'saved_cad_sha256':sha(fp),'limitations':['Filter media, captive retention and material still unspecified. Nuts are removed for cleaning; candidate screw stack not selected hardware.','Downward80mm route assumes available external space; actual legs/floor clearance not verified.','Subwoofer opening remains reference139.7; real cutout, flange, screws, basket, grille and vibration coupling pending.','Floor strength, loading, PC anchorage, electrical distribution and optional lighting mounts not certified.']};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(v['pass'] for v in checks),[v for v in checks if not v['pass']];print('FLOOR_DETAIL_PASS',len(checks),'checks; rear and frozen interfaces unchanged');A.closeDocument(d.Name)

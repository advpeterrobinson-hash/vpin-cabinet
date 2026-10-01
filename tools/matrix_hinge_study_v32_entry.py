"""Isolated real-CAD matrix comparison; CERN-OHL-S-2.0. Never modifies accepted parts."""
from pathlib import Path
import FreeCAD as A, Part, math,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];c=json.loads((R/'config/matrix_hinge_study_v32.json').read_text());src=R/c['source_directory'];O=R/'exports/generated/matrix-hinge-study-v32';O.mkdir(parents=True,exist_ok=True);V=A.Vector
hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.is_file()};viewer_files=['tools/viewer/template.html','tools/viewer/translations.json','exports/generated/viewer-v32/index.html'];hashes.update({p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in viewer_files})
d=A.openDocument(str(src/'play.FCStd'));old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};review=json.loads((src/'validation.json').read_text())['review'];alpha=review['closed_slope_deg'];pivot=V(*review['pivot_xyz_mm']);moving=[n for n in old if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope') and not n.startswith('PF_SupportMountScrew')]+['PLAYFIELD_ENVELOPE'];real={n:s for n,s in old.items() if not any(t in n for t in ('Reserve','RESERVED','CandidatePayload','CheckEnvelope','ServiceEnvelope'))};a=math.radians(alpha)
# Actual flat rectangular display envelope: frontmost face aligned to accepted slope.
pf=old['PLAYFIELD_ENVELOPE'];rear=pf.BoundBox.YMax
# Glass top surface from its actual CAD vertices, not the old illustration's invented plane.
glass=old['CandidateGlass'];glass_intercept=min(v.Point.z-v.Point.y*math.tan(a) for v in glass.Vertexes)
def box(x,y,z,w,h,t):return Part.makeBox(w,h,t,V(x,y,z))
def tf(s,y,z,b):q=s.copy();q.rotate(V(),V(1,0,0),b);q.translate(V(0,y,z));return q
def hit(s,t):return s.BoundBox.intersect(t.BoundBox) and s.common(t).Volume>.01
def dist(parts,obs):
 pairs=[]
 for s in parts.values():
  for t in obs.values():
   b=s.BoundBox;d=t.BoundBox;lb=math.sqrt(sum(max(0,getattr(b,k+'Min')-getattr(d,k+'Max'),getattr(d,k+'Min')-getattr(b,k+'Max'))**2 for k in ('X','Y','Z')));pairs.append((lb,s,t))
 best=9999
 for lb,s,t in sorted(pairs,key=lambda q:q[0]):
  if lb>=best:break
  best=min(best,s.distToShape(t)[0])
 return best
def intersections(parts,obs):return sorted({n for s in parts.values() for n,t in obs.items() if hit(s,t)})
fixed={n:s for n,s in real.items() if n not in moving and n!='CandidateGlass'}
# Fold envelope is conservative: sweep actual backbox packaging envelope, NOT a fabricated detailed hinge.
fold=[]
for angle in range(0,91,5):
 s=old['PF_BackboxCheckEnvelope'].copy();s.rotate(V(300,1308.1-38.1,508),V(1,0,0),angle);fold.append(s)
rows=[];geoms={}
def candidate(gap,tilt):
 b=tilt;br=math.radians(b);h=c['carrier_depth_mm'];y=rear+gap
 z=glass_intercept+y*math.tan(a)-c['glass_clearance_mm']-h*(math.sin(br)-math.cos(br)*math.tan(a))-8*(math.cos(br)+math.sin(br)*math.tan(a))
 carrier=tf(box((600-c['carrier_width_mm'])/2,0,-12,c['carrier_width_mm'],h,12),y,z,b);panels={f'MatrixPanel{i+1}':tf(box((600-476.25)/2+i*79.375,8,0,79.375,79.375,8),y,z,b) for i in range(6)};parts={'MatrixCarrier':carrier,**panels}
 # Nominal thickness is a packaging reserve; glass fit includes it.
 maxexcess=max(v.Point.z-(glass_intercept+v.Point.y*math.tan(a)-2) for s in panels.values() for v in s.Vertexes)
 playobs={n:s for n,s in real.items() if n!='CandidateGlass' and s.BoundBox.YMax>950};clash=intersections(parts,playobs)
 service=[];mind=9999
 for angle in range(0,51,2):
  obs={'playfield':Part.makeCompound([old[n] for n in moving])}
  for s in obs.values():s.rotate(pivot,V(1,0,0),-angle)
  service+=intersections(parts,obs);mind=min(mind,dist(parts,obs))
 lift=[];ld=9999
 for dz in range(0,49,2):
  obs={'playfield':Part.makeCompound([old[n] for n in moving])}
  for s in obs.values():s.translate(V(0,0,dz))
  lift+=intersections(parts,obs);ld=min(ld,dist(parts,obs))
 # independent lift 100 mm with glass removed (glass is removable service access, no playfield removal).
 removal=[];rd=9999;removal_bb=[]
 for dz in range(0,101,10):
  ps={n:s.copy() for n,s in parts.items()}
  for s in ps.values():s.translate(V(0,0,dz))
  removal+=intersections(ps,playobs);rd=min(rd,dist(ps,playobs))
  if any(hit(s,old['PF_BackboxCheckEnvelope']) for s in ps.values()):removal_bb.append(dz)
 wire=box(280,1127.125,old['BACKBOX_BASE'].BoundBox.ZMin-38,40,30,20);wclash=intersections({'wire':wire},playobs);wd=dist({'wire':wire},playobs)
 fc=dist(parts,{str(i):s for i,s in enumerate(fold)});foldhit=any(hit(s,t) for s in parts.values() for t in fold)
 # Sightlines through real shell, display and backbox. Glass is transparent; matrix's own carrier behind LEDs excluded.
 occluders={n:s for n,s in real.items() if n in ('PLAYFIELD_ENVELOPE','PF_BasePlywood','SIDE_L','SIDE_R','FRONT','REAR','BACKBOX_BASE')};occluders['backbox']=old['PF_BackboxCheckEnvelope']
 visibility=[]
 for eye in c['eyes_xyz_mm']:
  seen=0;total=0
  for ix in range(6):
   for iy in range(16):
    point=V((600-476.25)/2+(ix+.5)*79.375,y+(8+(iy+.5)*79.375/16)*math.cos(br)-8*math.sin(br),z+(8+(iy+.5)*79.375/16)*math.sin(br)+8*math.cos(br));line=Part.makeLine(V(*eye),point);total+=1
    if not any(line.common(s).Length>.1 for s in occluders.values()):seen+=1
  # angular separation of screen rear top point and nearest LED row in sagittal view.
  p=V(300,rear,pf.BoundBox.ZMax);m=V(300,y+8*math.cos(br),z+8*math.sin(br));ang=lambda q:math.degrees(math.atan2(q.z-eye[2],q.y-eye[1]));visibility.append({'eye_xyz_mm':eye,'visible_row_sample_percent':100*seen/total,'apparent_gap_deg':abs(ang(m)-ang(p))})
 row={'gap_mm':gap,'tilt_deg':tilt,'absolute_tilt_deg':b,'front_xyz_mm':[300,y,z],'rear_y_mm':carrier.BoundBox.YMax,'PLAY_mm':dist(parts,playobs),'PLAY_hits':clash,'glass_plane_excess_mm':maxexcess,'glass_clearance_mm':dist(parts,{'glass':glass}),'SERVICE_mm':mind,'SERVICE_hits':sorted(set(service)),'LIFT_OUT_mm':ld,'LIFT_OUT_hits':sorted(set(lift)),'removal_mm':rd,'removal_hits':sorted(set(removal)),'removal_backbox_envelope_interference_at_mm':removal_bb,'matrix_removal_fully_qualified':False,'fold_mm':fc,'fold_hits':foldhit,'wiring_mm':wd,'wiring_hits':wclash,'visibility':visibility}
 # Preserve the exact accepted diagnostic airflow paths, without reopening thermal analysis.
 routes={}
 for path in review['floor_fans']['thermal']:
  pts=path['airflow_approach_route_xyz_mm']
  for i in range(len(pts)-1):
   p=V(*pts[i]);delta=V(*pts[i+1])-p;routes[path['side']+str(i)]=Part.makeCylinder(path['route_radius_mm'],delta.Length,p,delta)
 row['airflow_hits']=intersections(parts,routes)
 row['airflow_clearance_mm']=dist(parts,routes)
 # Four provisional top-driver probes located from carrier's side margins; no permanent cabinet holes.
 tools={}
 left=(600-c['carrier_width_mm'])/2;panelleft=(600-476.25)/2
 for xx in ((left+panelleft)/2,600-(left+panelleft)/2):
  for yy in (20,h-20):tools[str((xx,yy))]=tf(Part.makeCylinder(4,50,V(xx,yy,0)),y,z,b)
 toolobs={**playobs,**panels};toolobs.pop('CandidateGlass',None)
 row['tool_hits']=intersections(tools,toolobs);row['tool_clearance_mm']=dist(tools,toolobs)
 row['wiring_SERVICE_hits']=[];row['wiring_LIFT_OUT_hits']=[]
 for angle in range(0,51,2):
  q=Part.makeCompound([old[n] for n in moving]);q.rotate(pivot,V(1,0,0),-angle)
  if hit(wire,q):row['wiring_SERVICE_hits'].append(angle)
 for dz in range(0,49,2):
  q=Part.makeCompound([old[n] for n in moving]);q.translate(V(0,0,dz))
  if hit(wire,q):row['wiring_LIFT_OUT_hits'].append(dz)
 row['feasible']=not(clash or service or lift or removal or removal_bb or foldhit or wclash or row['airflow_hits'] or row['tool_hits'] or row['wiring_SERVICE_hits'] or row['wiring_LIFT_OUT_hits']) and maxexcess<=0 and carrier.BoundBox.YMax<=c['rear_limit_y_mm'] and min(row[k] for k in ('PLAY_mm','SERVICE_mm','LIFT_OUT_mm','removal_mm','wiring_mm'))>=2
 return row,parts
for gap in c['gaps_mm']:
 for tilt in c['tilts_deg']:
  row,parts=candidate(gap,tilt);rows.append(row);geoms[(gap,tilt)]=parts;print('MATRIX_CANDIDATE',gap,tilt,row['feasible'],row['PLAY_hits'],row['SERVICE_hits'],row['LIFT_OUT_hits'],row['removal_hits'],row['fold_hits'],row['glass_plane_excess_mm'],flush=True)
# Rearward bound from carrier rear datum, evaluated for each tilt, no magic visual offset.
for tilt in c['tilts_deg']:
 gap=c['rear_limit_y_mm']-c['carrier_depth_mm']*math.cos(math.radians(tilt))-12*math.sin(math.radians(tilt))-rear
 row,parts=candidate(gap,tilt);row['rearward_limit_candidate']=True;rows.append(row);geoms[(gap,tilt)]=parts
feasible=[r for r in rows if r['feasible']];best=max(feasible,key=lambda r:(min(v['visible_row_sample_percent'] for v in r['visibility']),r['gap_mm'])) if feasible else None
review_candidates=[r for r in rows if r.get('rearward_limit_candidate') and r['PLAY_mm']>=2-1e-6 and r['removal_mm']>=2-1e-6]
best_review=max(review_candidates,key=lambda r:(min(v['visible_row_sample_percent'] for v in r['visibility']),r['gap_mm'])) if review_candidates else None
# Archive only obsolete files owned by this study, keeping regenerated review set unambiguous.
expected={'gap-%0.4f-tilt-%02d.FCStd'%(row['gap_mm'],row['tilt_deg']) for row in rows}
for path in O.glob('gap-*.FCStd'):
 if path.name not in expected:
  archive=R/'.work/matrix-study-history';archive.mkdir(parents=True,exist_ok=True);shutil.move(path,archive/path.name)
# Save all candidates, including rejected states, with unmodified baseline objects.
for row in rows:
 parts=geoms[(row['gap_mm'],row['tilt_deg'])];out=A.newDocument('MatrixStudy');
 for n,s in {**old,**parts}.items():o=out.addObject('PartDesign::Feature',n);o.Shape=s
 out.recompute();out.saveAs(str(O/('gap-%0.4f-tilt-%02d.FCStd'%(row['gap_mm'],row['tilt_deg']))));A.closeDocument(out.Name)
def mesh(n,s):v,f=s.tessellate(1);return {'name':n,'vertices':[[q.x,q.y,q.z] for q in v],'faces':[list(q) for q in f]}
base=json.loads((src/'mesh.json').read_text());bundle={'baseline':base,'candidates':[{'result':row,'parts':[mesh(n,s) for n,s in geoms[(row['gap_mm'],row['tilt_deg'])].items()]} for row in rows],'best':best};(O/'study-mesh.json').write_text(json.dumps(bundle,separators=(',',':')))
checks=[{'check':'accepted source/viewer bytes unchanged','pass':all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items())},{'check':'hinge inset 600/780 is 59.8375','pass':abs((780-600-60.325)/2-59.8375)<1e-8},{'check':'all 12 nominal combinations and four rearward limits evaluated','pass':len(rows)==16},{'check':'all new carriers/panels valid single solids','pass':all(s.isValid() and len(s.Solids)==1 for parts in geoms.values() for s in parts.values())}]
for n in old:checks.append({'check':'unchanged CAD '+n,'pass':old[n].isSame(d.getObject(n).Shape) or old[n].cut(d.getObject(n).Shape).Volume+d.getObject(n).Shape.cut(old[n]).Volume<1e-6})
report={'source_head':c['source_head'],'hinge':c['hinge'],'candidates':rows,'best':best,'best_review':best_review,'checks':checks,'source_hashes':hashes,'manufacturing_ready':False,'limitations':['Backbox is accepted packaging envelope, not detailed folding hardware. Glass hardware/channel release remains unconfirmed. Matrix panel thickness 8 mm is reservation, not vendor dimension. No physical cabinet prototype.']};(O/'validation.json').write_text(json.dumps(report,indent=2));assert all(r['pass'] for r in checks)
for n in ('LICENSE','NOTICE.md'):shutil.copyfile(R/n,O/n)
print('MATRIX_STUDY_PASS',len(checks),'BEST',best,flush=True)

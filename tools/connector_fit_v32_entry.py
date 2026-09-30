"""Connector installation screening and physical fit coupon; CERN-OHL-S-2.0."""
import json, hashlib, math, shutil
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1]
O=R/'exports/generated/connector-fit-v32';O.mkdir(parents=True,exist_ok=True)
cp=R/'config/fixed_rear_services_v32.json';rp=R/'exports/generated/fixed-rear-services-v32/validation.json'
c=json.loads(cp.read_text());r=json.loads(rp.read_text());sp=R/r['saved_proposals']['closed']['path']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(v['pass'] for v in r['checks']) and sha(sp)==r['saved_proposals']['closed']['sha256']
inputs={str(p.relative_to(R)):sha(p) for p in [cp,rp,sp,Path(__file__).resolve()]}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
V=A.Vector;checks=[]
def check(n,v):
 checks.append({'check':n,'pass':bool(v)})
def cy(x,y,z,rad,h):return Part.makeCylinder(rad,h,V(x,y,z),V(0,1,0))
def hits(shape,exclude=()):
 return [{'part':n,'mm3':shape.common(s).Volume} for n,s in scene.items() if n not in exclude and shape.BoundBox.intersect(s.BoundBox) and shape.common(s).Volume>.01]
# Explicit trial dimensions, not selected hardware or a structural rating.
# Under-head length / flange / inner washer / nut / shaft radius / nut-envelope radius.
stacks={'mains':(30,2,.8,3.2,2,4.1),'ethernet':(30,2,.5,2.4,1.5,3.2)}
records=[];L=1308.1
for key,(length,flange,washer,nut,shaft,nrad) in stacks.items():
 spec=c['direct_panel_io'][key];f=spec['footprint']
 for i,(x,z) in enumerate(f['hole_centers_xz_mm'],1):
  tip=L+flange-length;nutend=L-18-washer-nut
  check(f'{key}{i} candidate shaft through wood bore',not hits(cy(x,tip,z,shaft,length)))
  check(f'{key}{i} trial stack leaves at least one diameter beyond nut',nutend-tip>=2*shaft)
  # Nut envelope at inner face. Does not establish flange-body clearance.
  nshape=cy(x,nutend,z,nrad,nut)
  check(f'{key}{i} nut envelope clears modeled cabinet',not hits(nshape))
  # 120mm approach from inside; central relief excludes protruding shaft.
  tool=cy(x,nutend-120,z,nrad+1,120).cut(cy(x,nutend-121,z,shaft+.5,122))
  obstruction=hits(tool)
  records.append({'interface':key,'hole':i,'axis_xz_mm':[x,z],'candidate_bolt':f'M{shaft*2:g}x{length}','flange_assumed_mm':flange,'thread_beyond_nut_mm':nutend-tip,'internal_tool_conflicts':obstruction})
  if key=='mains':
   check(f'{key}{i} enclosure obstruction explicitly detected',any(v['part']=='CandidateMainsEnclosure' for v in obstruction))
   check(f'{key}{i} corridor clear with enclosure removed',not hits(tool,('CandidateMainsEnclosure',)))
  else:check(f'{key}{i} tool corridor clears modeled cabinet',not obstruction)
# RJ45 socket versus unmodeled body: analytic necessary check, not CAD fit certification.
pitch_radius=math.hypot(9.5,12);socket_radius=4.2;body_radius=23.6/2
check('reject assumed RJ45 socket that overlaps circular body reservation',pitch_radius-socket_radius<body_radius)
check('RJ45 trial small washer has positive wood margin',pitch_radius-3.2-12>0)
# Physical test coupon. X/Y are local planar coordinates, Z=thickness; no panel-location meaning.
W,H,T=200,120,18
coupon=Part.makeBox(W,H,T);ops=[]
def circ(x,y,rad,kind):
 global coupon
 coupon=coupon.cut(Part.makeCylinder(rad,T+2,V(x,y,-1)))
 ops.append({'kind':kind,'shape':'circle','center_mm':[x,y],'radius_mm':rad})
def rounded(x,y,w,h,rr):
 global coupon
 cut=Part.makeBox(w-2*rr,h,T+2,V(x+rr,y,-1)).fuse(Part.makeBox(w,h-2*rr,T+2,V(x,y+rr,-1)))
 for xx in (x+rr,x+w-rr):
  for yy in (y+rr,y+h-rr):cut=cut.fuse(Part.makeCylinder(rr,T+2,V(xx,yy,-1)))
 coupon=coupon.cut(cut);ops.append({'kind':'mains_body','shape':'rounded_rectangle','xywh_mm':[x,y,w,h],'radius_mm':rr})
m=c['direct_panel_io']['mains']['footprint'];e=c['direct_panel_io']['ethernet']['footprint']
assert m['window_xzwh_mm']==[81,406,28,48] and m['hole_centers_xz_mm']==[[75,430],[115,430]], 'Update coupon mapping for revised mains footprint'
assert e['hole_centers_xz_mm']==[[539.5,442],[520.5,418]], 'Update coupon mapping for revised RJ45 footprint'
rounded(55-14,60-24,28,48,m['corner_radius_mm'])
for dx in (-20,20):circ(55+dx,60,m['wood_fixing_hole_diameter_mm']/2,'mains_fixing')
circ(145,60,e['opening_diameter_mm']/2,'rj45_body')
# Coupon is exterior view: top-left / bottom-right as supplier drawing.
for dx,dy in [(-9.5,12),(9.5,-12)]:circ(145+dx,60+dy,e['wood_fixing_hole_diameter_mm']/2,'rj45_fixing')
check('coupon valid single solid',coupon.isValid() and len(coupon.Solids)==1)
check('coupon200x120x18',all(abs(a-b)<1e-6 for a,b in zip([coupon.BoundBox.XLength,coupon.BoundBox.YLength,coupon.BoundBox.ZLength],[W,H,T])))
out=A.newDocument('ConnectorCoupon');o=out.addObject('PartDesign::Feature','ConnectorCoupon');o.Shape=coupon;o.addProperty('App::PropertyString','PartCode');o.PartCode='V32-CONNECTOR-COUPON-DRAFT';out.recompute();fp=O/'connector-coupon.FCStd';out.saveAs(str(fp));A.closeDocument(out.Name);out=A.openDocument(str(fp));check('coupon saved reopened',out.getObject('ConnectorCoupon').Shape.isValid() and abs(out.getObject('ConnectorCoupon').Shape.Volume-coupon.Volume)<1e-6);A.closeDocument(out.Name)
# Minimal ASCII DXF millimetres, true-size geometry, explicit layers; no tool compensation.
lines=['0','SECTION','2','HEADER','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
def ent(kind,layer,fields):
 lines.extend(['0',kind,'8',layer]);
 for code,value in fields:lines.extend([str(code),str(value)])
def line(x1,y1,x2,y2,layer='THROUGH_BODY'):ent('LINE',layer,[(10,x1),(20,y1),(11,x2),(21,y2)])
for p,q in [((0,0),(W,0)),((W,0),(W,H)),((W,H),(0,H)),((0,H),(0,0))]:line(*p,*q,'COUPON_OUTLINE')
for op in ops:
 if op['shape']=='circle':ent('CIRCLE','DRILL_THROUGH' if 'fixing' in op['kind'] else 'THROUGH_BODY',[(10,op['center_mm'][0]),(20,op['center_mm'][1]),(40,op['radius_mm'])])
 else:
  x,y,w,h=op['xywh_mm'];rr=op['radius_mm']
  for points in [(x+rr,y,x+w-rr,y),(x+w,y+rr,x+w,y+h-rr),(x+w-rr,y+h,x+rr,y+h),(x,y+h-rr,x,y+rr)]:line(*points)
  for xx,yy,aa,bb in [(x+w-rr,y+rr,270,360),(x+w-rr,y+h-rr,0,90),(x+rr,y+h-rr,90,180),(x+rr,y+rr,180,270)]:ent('ARC','THROUGH_BODY',[(10,xx),(20,yy),(40,rr),(50,aa),(51,bb)])
lines.extend(['0','ENDSEC','0','EOF']);(O/'connector-coupon-mm.dxf').write_text('\n'.join(lines)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="120mm" viewBox="0 0 200 120">','<rect width="200" height="120" fill="#e5ccaa" stroke="#333" stroke-width=".4"/>']
for op in ops:
 if op['shape']=='circle':x,y=op['center_mm'];svg.append(f'<circle cx="{x}" cy="{H-y}" r="{op["radius_mm"]}" fill="white" stroke="#345" stroke-width=".3"/>')
 else:x,y,w,h=op['xywh_mm'];svg.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" rx="{op["radius_mm"]}" fill="white" stroke="#345" stroke-width=".3"/>')
for x,y,t in [(8,10,'V32 — CUPOM DE ENCAIXE • 200 × 120 × 18 mm'),(25,26,'ENERGIA 28 × 48 R3'),(118,26,'RJ45 Ø24 provisório'),(26,98,'2 × Ø4,5 / passo40'),(117,98,'2 × Ø3,2 / 19 × 24'),(8,111,'Vista externa • Medir impressão • Não é liberação CNC')]:svg.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="3.6">{t}</text>')
svg.append('</svg>');(O/'connector-coupon.svg').write_text('\n'.join(svg))
for name in ('LICENSE','NOTICE.md'):shutil.copyfile(R/name,O/name)
check('input files unchanged',all(sha(R/p)==h for p,h in inputs.items()))
report={'manufacturing_ready':False,'source_hashes':inputs,'checks':checks,'candidate_stacks':records,'rj45_socket_body_radial_overlap_mm':body_radius+socket_radius-pitch_radius,'coupon_operations':ops,'coupon_sha256':sha(fp),'notes':['Enclosure must be removed for mains internal nut/tool service; retention and disconnection sequence remain unspecified.','RJ45 body and tools not fully modeled; socket interference is a conservative circular screen. Use real small wrench access test.','Candidate bolt lengths assume2mm flange; purchase list and strength not qualified.','Coupon geometry is nominal; measured thickness, cutter, compensation and shop review required before cutting.']};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');assert all(x['pass'] for x in checks),[v for v in checks if not v['pass']];print('CONNECTOR_FIT_PASS',len(checks),'checks; cabinet unchanged; CNC HOLD');A.closeDocument(d.Name)

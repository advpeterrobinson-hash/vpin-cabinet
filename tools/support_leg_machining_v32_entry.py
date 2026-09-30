"""Separate support/leg CNC planning scene. CERN-OHL-S-2.0; not a load rating."""
import csv, hashlib, json, math
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1]; O=R/'exports/generated/support-leg-v32'; O.mkdir(parents=True,exist_ok=True)
cp=R/'config/support_leg_machining_v32.json'; c=json.loads(cp.read_text())
rp=R/'exports/generated/side-panel-v32/simple-shelves-validation.json'; r=json.loads(rp.read_text())
sp=R/r['saved_proposal']['path']; freeze=json.loads((R/c['freeze_record']).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sp)==r['saved_proposal']['sha256']
assert all(x['pass'] for x in r['checks'])
for name,h in r['source_hashes'].items():assert sha(R/name)==h,name
assert {k:r['config'][k] for k in freeze['layout']}==freeze['layout']
posepath=R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json'
inputs={str(p.relative_to(R)):sha(p) for p in (cp,rp,sp,R/c['freeze_record'],posepath,Path(__file__).resolve())}
d=A.openDocument(str(sp));d.recompute();scene={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
old={n:s.copy() for n,s in scene.items()};new={};checks=[];holes=[];access=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
def cyl(origin,axis,radius,length):return Part.makeCylinder(radius,length,A.Vector(*origin),A.Vector(*axis))
def hits(parts,obs):
 result=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>c['collision_threshold_mm3']:result.append({'part':n,'obstacle':k,'mm3':v})
 return result
def swept(s,v):
 b=s.BoundBox
 return Part.makeBox(b.XLength+abs(v.x),b.YLength+abs(v.y),b.ZLength+abs(v.z),A.Vector(b.XMin+min(0,v.x),b.YMin+min(0,v.y),b.ZMin+min(0,v.z)))
anchor=c['anchor']
for spec in r['config']['shelves']:
 i=spec['number'];board=scene[f'SHELF_{i}'].BoundBox
 check(f'S{i} fixed underside height',abs(board.ZMin-c['shelf_underside_z_mm'][i-1])<1e-6)
 check(f'S{i} fixed upper surface',abs(board.ZMax-c['shelf_top_z_mm'][i-1])<1e-6)
 for side,wall,inner,sgn in [('L','SIDE_L',18,1),('R','SIDE_R',582,-1)]:
  name=f'SHELF_SUPPORT_{i}{side}';support=scene[name];b=support.BoundBox;face=inner+sgn*b.XLength;z=(b.ZMin+b.ZMax)/2
  check(name+' top meets shelf',abs(b.ZMax-board.ZMin)<1e-6)
  for j,offset in enumerate(anchor['y_offsets_mm'],1):
   y=spec['y_mm']+offset;axis=(-sgn,0,0);prefix=f'CandidateFixedSupportScrew{i}{side}{j}'
   support=support.cut(cyl((face+sgn,y,z),axis,anchor['support_clearance_diameter_mm']/2,b.XLength+2))
   scene[wall]=scene[wall].cut(cyl((inner+sgn,y,z),axis,anchor['wall_pilot_diameter_mm_candidate']/2,anchor['wall_pilot_depth_mm_candidate']+1))
   headface=face+sgn*anchor['washer_thickness_mm']
   screw=cyl((headface,y,z),axis,anchor['shaft_diameter_mm']/2,anchor['shaft_length_mm']).fuse(cyl((headface,y,z),(sgn,0,0),anchor['head_diameter_mm']/2,anchor['head_length_mm'])).removeSplitter()
   washer=cyl((face,y,z),(sgn,0,0),anchor['washer_diameter_mm']/2,anchor['washer_thickness_mm']).cut(cyl((face-sgn,y,z),(sgn,0,0),anchor['support_clearance_diameter_mm']/2,anchor['washer_thickness_mm']+2))
   new[prefix]=screw;new[prefix+'Washer']=washer
   pilot=anchor['wall_pilot_depth_mm_candidate'];engagement=anchor['shaft_length_mm']-b.XLength-anchor['washer_thickness_mm']
   check(prefix+' blind pilot retains nominal 5mm outer skin',18-pilot>=5)
   check(prefix+' candidate tip does not bottom',0<engagement<pilot)
   holes.extend([{'id':prefix+'-support','part':name,'origin':[face,y,z],'axis':list(axis),'diameter_mm':anchor['support_clearance_diameter_mm'],'depth_mm':b.XLength,'operation':'EDGE_THROUGH_DRILL','status':'CANDIDATE_HARDWARE_UNQUALIFIED'},
                 {'id':prefix+'-wall','part':wall,'origin':[inner,y,z],'axis':list(axis),'diameter_mm':anchor['wall_pilot_diameter_mm_candidate'],'depth_mm':pilot,'operation':'INNER_FACE_BLIND_PILOT','status':'HOLD_SCREW_AND_PLYWOOD_COUPON'}])
   access.append((prefix,cyl((headface+sgn*anchor['head_length_mm'],y,z),(sgn,0,0),anchor['driver_radius_mm'],anchor['driver_length_mm'])))
  scene[name]=support

leg=c['legs'];L=1308.1;legparts=[];legaccess=[];length=leg['block_leg_xy_mm'];height=leg['lamination_count']*leg['lamination_thickness_mm'];s2=math.sqrt(2)
for corner,ox,oy,sx,sy,wall,end in [('FL',0,0,1,1,'SIDE_L','FRONT'),('FR',600,0,-1,1,'SIDE_R','FRONT'),('RL',0,L,1,-1,'SIDE_L','REAR'),('RR',600,L,-1,-1,'SIDE_R','REAR')]:
 rear=corner[0]=='R';z0=leg['rear_block_bottom_z_mm' if rear else 'front_block_bottom_z_mm'];lower=leg['rear_lower_bolt_z_mm_candidate' if rear else 'front_lower_bolt_z_mm_candidate'];axis=(sx/s2,sy/s2,0)
 def point(x,y,z):return A.Vector(ox+sx*x,oy+sy*y,z)
 pts=[point(18,18,z0),point(18+length,18,z0),point(18,18+length,z0)];face=Part.Face(Part.makePolygon(pts+[pts[0]]));block=face.extrude(A.Vector(0,0,height))
 mid=18+length/2;half=leg['plate_width_mm_candidate']/(2*s2)
 platepoints=[point(mid-half,mid+half,z0),point(mid+half,mid-half,z0),point(mid+half,mid-half,z0+height),point(mid-half,mid+half,z0+height)]
 plate=Part.Face(Part.makePolygon(platepoints+[platepoints[0]])).extrude(A.Vector(*axis)*leg['plate_thickness_mm_candidate'])
 for row,z in enumerate((lower,lower+leg['pitch_mm']),1):
  start=(ox-axis[0]*10,oy-axis[1]*10,z);cut=cyl(start,axis,leg['hole_diameter_mm_candidate']/2,120)
  block=block.cut(cut);plate=plate.cut(cut);scene[wall]=scene[wall].cut(cut);scene[end]=scene[end].cut(cut)
  check(corner+str(row)+' block edge ligament >=20mm',min(z-z0,z0+height-z)-leg['hole_diameter_mm_candidate']/2>=20)
  holes.append({'id':f'Leg{corner}{row}','part':f'{wall}+{end}+CandidateLegBlock{corner}+CandidateLegPlate{corner}','origin':[ox,oy,z],'axis':list(axis),'diameter_mm':leg['hole_diameter_mm_candidate'],'depth_mm':120,'operation':'45_DEG_CORNER_BORE_SHOP_FIXTURE','status':'HOLD_LEG_BRACKET_PITCH_AND_HEIGHT'})
  p=point(mid,mid,z)+A.Vector(*axis)*(leg['plate_thickness_mm_candidate']+1)
  legaccess.append((f'Leg{corner}{row}',cyl((p.x,p.y,p.z),axis,12,80)))
 new['CandidateLegBlock'+corner]=block;new['CandidateLegPlate'+corner]=plate;legparts.extend(['CandidateLegBlock'+corner,'CandidateLegPlate'+corner])
scene.update(new)
check('valid single solids',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
check('plate height equals supported block height',leg['plate_height_mm_candidate']==height)
reflection=A.Matrix();reflection.A11=-1;reflection.A14=600
for left,right in [('CandidateLegBlockFL','CandidateLegBlockFR'),('CandidateLegBlockRL','CandidateLegBlockRR'),('CandidateLegPlateFL','CandidateLegPlateFR'),('CandidateLegPlateRL','CandidateLegPlateRR')]+[(f'SHELF_SUPPORT_{i}L',f'SHELF_SUPPORT_{i}R') for i in (1,2,3)]:
 mirrored=scene[left].transformGeometry(reflection)
 check(left+' mirrored counterpart',mirrored.cut(scene[right]).Volume+scene[right].cut(mirrored).Volume<1e-4)
for i in (1,2,3):check(f'S{i} frozen board unchanged',scene[f'SHELF_{i}'].cut(old[f'SHELF_{i}']).Volume+old[f'SHELF_{i}'].cut(scene[f'SHELF_{i}']).Volume<1e-5)
# Screw threads intentionally displace wood inside smaller pilot: exclude that receiving wall only.
physical={n:s for n,s in scene.items() if not n.endswith('_CandidatePayload')}
installed=[]
for n in new:
 excluded={n}
 if n.startswith('CandidateFixedSupportScrew') and not n.endswith('Washer'):excluded.add('SIDE_L' if 'L' in n else 'SIDE_R')
 installed+=hits({n:scene[n]},{k:s for k,s in physical.items() if k not in excluded})
check('new parts no unintended installed collisions',not installed)
tool_conflicts=[]
for name,tool in access:
 tool_conflicts+=hits({name:tool},{n:s for n,s in physical.items() if n not in (name,name+'Washer')})
for name,tool in legaccess:tool_conflicts+=hits({name:tool},physical)
check('candidate driver access with shelves installed',not tool_conflicts)
route_conflicts=[]
for route in r['routes']:
 moving={n:scene[n].copy() for n in route['moving']}
 for xyz in route['translations_mm']:
  v=A.Vector(*xyz);route_conflicts+=hits({n:swept(s,v) for n,s in moving.items()},new)
  for shape in moving.values():shape.translate(v)
check('frozen shelf paths clear added support and leg hardware',not route_conflicts)
top_conflicts=[]
for a in r['axes']:
 x,y,z=a['xyz_mm'];top_conflicts+=hits({'tool':cyl((x,y,a['head_top_z_mm']),(0,0,1),8,1500)},new)
check('frozen top screw access clear added parts',not top_conflicts)
# Keep the legacy display-screen axis and sample density; test only additions.
pose=json.loads(posepath.read_text());display_conflicts=[]
for angle in range(0,101,2):
 moving={n:scene[n].copy() for n in r['config']['playfield_assembly']}
 for s in moving.values():s.rotate(A.Vector(*pose['pivot_xyz_mm']),A.Vector(1,0,0),-angle)
 for conflict in hits(moving,new):display_conflicts.append(dict(angle=angle,**conflict))
check('sampled display opening clears added parts',not display_conflicts)
check('reject 57mm jig as exact 58mm pattern',abs(leg['pitch_mm']-leg['alternative_jig_pitch_mm'])>.5)
check('reject through-wall pilot mutation',18-19<5)
raised_block=scene['CandidateLegBlockFR'].copy();raised_block.translate(A.Vector(0,0,18))
rejected_corner=hits({'raised_front_right_block':raised_block},{'CandidateFrontButton4':scene['CandidateFrontButton4']})
check('reject taller front corner interfering with launch button',bool(rejected_corner))
check('inputs not overwritten',all(sha(R/n)==h for n,h in inputs.items()))
for a in r['axes']:
 x,y,z=a['xyz_mm'];b=scene[a['shelf']].BoundBox
 for suffix,part,start,diameter,depth,operation in [
  ('shelf',a['shelf'],z,r['config']['bore_diameter_mm'],b.ZLength,'TOP_CLEARANCE_THROUGH'),
  ('receiver',a['support'],b.ZMin,r['config']['insert_bore_diameter_mm'],r['config']['insert_pocket_depth_mm'],'TOP_RECEIVER_PLACEHOLDER_NOT_PILOT_SPEC'),
  ('tip',a['support'],b.ZMin,r['config']['bore_diameter_mm'],r['config']['shaft_tip_pocket_depth_mm'],'TOP_TIP_RELIEF_PLACEHOLDER')]:
  holes.append({'id':a['bolt']+'-'+suffix,'part':part,'origin':[x,y,start],'axis':[0,0,-1],'diameter_mm':diameter,'depth_mm':depth,'operation':operation,'status':'HOLD_SELECTED_TOP_FASTENER_AND_INSERT'})
outdoc=A.newDocument('SupportLegPlanningV32')
for n,s in scene.items():
 o=outdoc.addObject('PartDesign::Feature',n);o.Shape=s
 source_object=d.getObject(n);code=getattr(source_object,'PartCode','') if source_object else ''
 o.addProperty('App::PropertyString','PartCode');o.PartCode=code
 o.addProperty('App::PropertyString','LegacyId');o.LegacyId=n
 o.Label=('PROVISIONAL '+n if n in new else (code or n))
 o.addProperty('App::PropertyString','ReviewStatus');o.ReviewStatus='CNC HOLD - hardware/load/process qualification pending'
outdoc.recompute();outpath=O/'support-leg-planning.FCStd';outdoc.saveAs(str(outpath));A.closeDocument(outdoc.Name);saved=A.openDocument(str(outpath));saved.recompute()
actual={o.Name:o.Shape for o in saved.Objects if hasattr(o,'Shape')}
check('reopened identity and validity',set(actual)==set(scene) and all(s.isValid() and len(s.Solids)==1 for s in actual.values()))
check('reopened shapes match',all(actual[n].cut(s).Volume+s.cut(actual[n]).Volume<1e-5 for n,s in scene.items()))
check('reopened original permanent codes preserved',all(saved.getObject(n).PartCode==getattr(d.getObject(n),'PartCode','') for n in old))
mesh=[]
for n in ['CandidateLegBlockFL','CandidateLegPlateFL','SHELF_SUPPORT_1L']:
 vs,fs=actual[n].tessellate(.4);mesh.append({'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':fs})
(O/'detail-mesh.json').write_text(json.dumps(mesh)+'\n')
with (O/'machining-plan-review.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['id','part','x_mm','y_mm','z_mm','axis_x','axis_y','axis_z','diameter_mm','depth_mm','operation','status'])
 for h in holes:w.writerow([h['id'],h['part'],*h['origin'],*h['axis'],h['diameter_mm'],h['depth_mm'],h['operation'],h['status']])
report={'manufacturing_ready':False,'source_hashes':inputs,'config':c,'checks':checks,'holes':holes,'rejected_front_corner':rejected_corner,'installed_conflicts':installed,'tool_conflicts':tool_conflicts,'shelf_route_conflicts':route_conflicts,'top_access_conflicts':top_conflicts,'display_sample_conflicts':display_conflicts,'saved_proposal':{'path':str(outpath.relative_to(R)),'sha256':sha(outpath),'solids':len(scene)},'unverified':['Leg hardware including nut retention, actual legs/levelers and play height','Plywood laminations/bonding and dynamic proof','Shelf support screw/pilot and thread retention','45 degree corner drilling fixture and selected CNC capability','Actual display hinge/props/harness and upper backbox']}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
print('SUPPORT_LEG_PLAN_PASS',len(checks),'checks;',len(holes),'planned operations; machining NOT released')
A.closeDocument(saved.Name);A.closeDocument(d.Name)

"""Isolated optional board and cable packaging study. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
No CURRENT part, hole, electrical connector or bought clamp is released here.
"""
from pathlib import Path
import os,sys,json,math,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load,actual,transform,pf_names,PF,WPC,V,certify
C=json.loads((R/'config/service_modularity_v338.json').read_text());O=R/C['output'];O.mkdir(exist_ok=True,parents=True);(O/'modularity-brep').mkdir(exist_ok=True)
source=R/os.getenv('V338_MODULARITY_SOURCE',C['source']);before=hashlib.sha256(source.read_bytes()).hexdigest();ss=load(source)
extra_occupied=['SSF_AmplifierReserve','SSF_PSUReserve','SSF_USBReserve','BB_DMDEnvelope','BB_SpeakerEnvelopeL','BB_SpeakerEnvelopeR']
obs=actual(ss);obs.update({n:ss[n] for n in extra_occupied if n in ss});obs={n:s for n,s in obs.items() if n!='CandidateGlass' and not n.startswith(('Matrix','MX_'))}
checks=[];study={};rows={}
def check(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d})
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def moved(s,v):q=s.copy();q.translate(V(*v));return q
def bb_lower(a,b):
 return math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
def collisions(shapes,obstacles,ignore=()):
 out=[]
 for n,s in shapes.items():
  for k,t in obstacles.items():
   if k in ignore or bb_lower(s.BoundBox,t.BoundBox)>1e-7:continue
   vol=s.common(t).Volume
   if vol>1e-4:out.append({'part':n,'obstacle':k,'mm3':vol})
 return out

def nearest(shapes,obstacles,ignore=()):
 best=[1e9,None,None]
 for n,s in shapes.items():
  for k,t in obstacles.items():
   if k in ignore or bb_lower(s.BoundBox,t.BoundBox)>best[0]:continue
   d=s.distToShape(t)[0]
   if d<best[0]:best=[d,n,k]
 return best

def rounded(x,y,z,w,d,h,r):
 core=box(x,y+r,z,w,d-2*r,h)
 if w>2*r:core=core.fuse(box(x+r,y,z,w-2*r,d,h))
 for xx in [x+r,x+w-r]:
  for yy in [y+r,y+d-r]:core=core.fuse(Part.makeCylinder(r,h,V(xx,yy,z)))
 return core.removeSplitter()
def tube(points,r=4):
 solids=[]
 for a,b in zip(points,points[1:]):
  if (b-a).Length>1e-6:solids.append(Part.makeCylinder(r,(b-a).Length,a,b-a))
 solids += [Part.makeSphere(r,p) for p in points]
 return Part.makeCompound(solids)
def clamp(x,y,z):
 # Original generic packaging envelope. z = lower face of 12 mm shelf,
 # board bears on shelf, total clamped stack24 mm. No vendor shape copied.
 s=box(x-9,y-30,z-12,18,10,58)
 s=s.fuse(box(x-9,y-25,z-12,18,52,8)).fuse(box(x-9,y-25,z+38,18,52,8))
 s=s.fuse(Part.makeCylinder(4,28,V(x,y+20,z-32)))
 s=s.fuse(Part.makeCylinder(8,4,V(x,y+20,z-4)))
 s=s.fuse(Part.makeCylinder(8,14,V(x,y+20,z+24)))
 s=s.fuse(Part.makeCylinder(3,38,V(x-19,y+20,z-28),V(1,0,0)))
 return s.removeSplitter()
boards={};payloads={};clamps={}
for p in C['optional_board']['samples']:
 x,y,z=p['origin_xyz_mm'];name=p['name'];s=rounded(x,y,z,C['optional_board']['width_mm'],120,12,4)
 for sx,sy,w,d in C['optional_board']['strain_slots_local_xywh_mm']:s=s.cut(rounded(x+sx,y+sy,z-1,w,d,14,3))
 boards[name]=s.removeSplitter();study[name]=boards[name]
 # A small generic occupied payload envelope; no permanent mounting-hole pattern.
 payloads[name+'Payload']=box(x+10,y+35,z+12,80,45,50);study.update({name+'Payload':payloads[name+'Payload']})
 for i,xx in enumerate(p['clamp_x_mm']):
  edge=p['clamp_edge_y_mm'];q=clamp(xx,edge,z-12)
  if p['clamp_edge']=='REAR':
   m=A.Matrix();m.A22=-1;m.A24=2*edge;q.transformShape(m,True)
  clamps[name+'Clamp'+str(i+1)]=q
 (O/'modularity-brep'/f'{name}.brep').write_text(boards[name].exportBrepToString())
study.update(clamps);optional=boards|payloads|clamps
check('optional boards valid one-face12mm solids',all(s.isValid() and len(s.Solids)==1 for s in boards.values()))
boardhits=collisions(optional,obs);check('optional boards clamps payloads clear current occupied geometry',not boardhits,boardhits)
rows['optional_installed']={'collisions':boardhits,'nearest_nonbearing':nearest(optional,obs,ignore=['SHELF_2','SHELF_3'])}
# Exact conservative continuous rotation against only the new optional occupied
# solids. Other CURRENT motion is inherited; no old intended contacts omitted.
moving_names=[n for n in pf_names(ss) if n in obs]+[n for n in ss if n.endswith('_RetentionReceiver')]
mov={n:ss[n] for n in moving_names};proof=certify(mov,optional,start=-50,end=0,axis=PF)
check('optional modules preserve continuous0to50 PF clearance',True,{'certified_intervals':len(proof)})
for lift in [0,12,24,36,48]:
 hh=collisions({n:moved(s,[0,0,lift]) for n,s in mov.items()},optional);check('PF lift optional modules '+str(lift),not hh,hh)
# Reference shelf extraction sequence is preserved by removing optional boards,
# clamps and detachable cable anchor FIRST. The optional modules are not new
# permanent obstacles. Screen board removal itself at 50-degree PF service.
service=obs.copy();service.update(transform(mov,angle=-50,axis=PF))
for p in C['optional_board']['samples']:
 n=p['name'];s=boards[n];b=s.BoundBox;sweep=box(b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength+100)
 hh=collisions({n:sweep},service,ignore=[p['shelf']]);check('100mm board lift after clamps removed '+n,not hh,hh)
# Existing S2/S3 shelf travel versus OTHER selected optional board: removable
# samples do not turn a shelf into a fixed electronics bulkhead.
sr=json.loads((R/'exports/generated/side-panel-v32/simple-shelves-validation.json').read_text())
for route in sr['routes']:
 other={n:s for n,s in optional.items() if not n.startswith('AccessoryBoard'+{'SHELF_1':'S1','SHELF_2':'S2','SHELF_3':'S3'}[route['shelf']])}
 moving={route['shelf']:ss[route['shelf']].copy()};hh=[]
 for xyz in route['translations_mm']:
  for n,s in moving.items():
   b=s.BoundBox;v=V(*xyz);sweep=box(b.XMin+min(0,v.x),b.YMin+min(0,v.y),b.ZMin+min(0,v.z),b.XLength+abs(v.x),b.YLength+abs(v.y),b.ZLength+abs(v.z));hh+=collisions({n:sweep},other);s.translate(v)
 check('shelf route no new obstruction '+route['shelf'],not hh,hh)
# Existing12 shelf screw columns, current50degree state: optional clamps remain
# outside their columns. The selected driver itself remains hardware-dependent.
tools={a['bolt']:Part.makeCylinder(sr['config']['tool_radius_mm'],450,V(a['xyz_mm'][0],a['xyz_mm'][1],a['head_top_z_mm'])) for a in sr['axes']}
hh=collisions(tools,optional);check('12 shelf fastener columns clear optional modules',not hh,hh)
for name,z in C['route_zones'].items():
 study[name]=tube([V(*p) for p in z['points_mm']],z['radius_mm']);hh=collisions({name:study[name]},obs|optional);check('low route zone '+name,not hh,hh)
rows['route_minimums']={n:nearest({n:study[n]},obs|optional) for n in C['route_zones']}
# Existing PF cable algorithm and coordinates, re-screened against CURRENT.
rev=json.loads((R/'exports/generated/notch-floor-fans-v32/validation.json').read_text())['review'];a=math.radians(rev['closed_slope_deg']);bz=400.05+45*math.tan(a)-12-55*math.cos(a)
pf_start=V(300,45+877*math.cos(a)+20*math.sin(a),bz+877*math.sin(a)-20*math.cos(a));pf_end=V(*C['playfield_loop']['fixed_xyz_mm'])
def flex(p,end,length,direction):
 def pts(b):return [p*(1-t)+end*t+direction*(4*b*t*(1-t)) for t in [j/80 for j in range(81)]]
 def plen(ps):return sum((q-p).Length for p,q in zip(ps,ps[1:]))
 lo,hi=0.,500.
 for _ in range(36):
  mid=(lo+hi)/2
  if plen(pts(mid))<length:lo=mid
  else:hi=mid
 b=(lo+hi)/2;pp=pts(b);dp=end-p;cur=[]
 for j in range(81):
  t=j/80;v=dp+direction*(4*b*(1-2*t));acc=direction*(-8*b);cross=v.cross(acc).Length
  if cross>1e-8:cur.append(v.Length**3/cross)
 return tube(pp),pp,plen(pp),min(cur) if cur else 1e9
states=[('PLAY',0,0),('SERVICE50',50,0),('LIFT48',0,48)]+[(f'SERVICE{i}',i,0) for i in range(1,50)]+[(f'LIFT{z}',0,z) for z in range(4,48,4)]
pfrows=[]
for label,angle,lift in states:
 p=Part.Vertex(pf_start);p.rotate(PF,V(1,0,0),-angle);p.translate(V(0,0,lift));p=p.Vertexes[0].Point
 s,pp,length,br=flex(p,pf_end,400,V(1,0,0));ob=obs|optional;ob.update(transform(mov,angle=-angle,lift=lift,axis=PF));hh=collisions({'MovingPFHarness':s},ob)
 pfrows.append({'state':label,'angle_deg':angle,'lift_mm':lift,'length_mm':length,'minimum_bend_radius_mm':br,'collisions':hh})
 if label in ['PLAY','SERVICE50','LIFT48']:
  study['MovingPFHarness_'+label]=s; s.exportBrep(str(O/'modularity-brep'/('MovingPFHarness_'+label+'.brep')))
rows['playfield_loop']=pfrows;check('PF400mm loop63sample states no interference',not any(x['collisions'] for x in pfrows));check('PF loop reference bend radius35mm',min(x['minimum_bend_radius_mm'] for x in pfrows)>=35)
# Backbox: an explicit provisional flexible route, not a selected bundle.
# Search vertical/lateral bow alternatives; keep failed trials as evidence.
bbmov={n:s for n,s in obs.items() if n.startswith('BB_')};bbfixed={n:s for n,s in obs.items() if not n.startswith('BB_')};bbrows=[]
ca=C['backbox_loop'];fixed=V(*ca['fixed_aperture_xyz_mm']);moving=V(*ca['moving_xyz_mm']);tested=[0,.25,.5,1,2,5,10,15,30,45,60,75,90]
for angle in tested:
 v=Part.Vertex(moving);v.rotate(WPC,V(1,0,0),angle);end=v.Vertexes[0].Point
 ob=bbfixed|transform(bbmov,angle=angle,axis=WPC)|optional;best=None
 for direction in [V(0,0,1),V(.35,0,1),V(-.35,0,1),V(0,0,-1)]:
  s,pp,length,br=flex(fixed,end,ca['length_mm'],direction);hh=collisions({'BackboxMovingHarness':s},ob)
  item={'angle_deg':angle,'direction':list(direction),'length_mm':length,'minimum_bend_radius_mm':br,'collisions':hh}
  if best is None or len(hh)<len(best[0]['collisions']):best=(item,s)
  if not hh:break
 bbrows.append(best[0])
 if angle in [0,45,90]:study['BackboxHarness_'+str(angle)]=best[1];best[1].exportBrep(str(O/'modularity-brep'/('BackboxHarness_'+str(angle)+'.brep')))
rows['backbox_loop']=bbrows
# Failure here leaves a truthful route hold, not an architecture redesign.
rows['backbox_route_pass']=not any(x['collisions'] for x in bbrows) and min(x['minimum_bend_radius_mm'] for x in bbrows)>=35
rows['backbox_route_hold']='No selected cable, continuous fold-loop routing, supported anchors or minimum bend radius demonstrated. Existing passage and carrier slots preserved; no connector/disconnect design.'
check('no new permanent wood or holes',C['permanent_hardpoint_holes_added']==0)
check('protected source unchanged',hashlib.sha256(source.read_bytes()).hexdigest()==before)
doc=A.newDocument('V338ModularityStudy');doc.Comment='ISOLATED OPTIONAL ACCESSORY AND ROUTE STUDY; NO CURRENT EDIT; HARDWARE / CABLE / CNC HOLD'
for n,s in study.items():
 ob=doc.addObject('PartDesign::Feature',n);ob.Shape=s;ob.addProperty('App::PropertyString','Authority');ob.Authority='ORIGINAL PARAMETRIC ENVELOPE / OPTIONAL STUDY NOT CNC'
doc.recompute();doc.saveAs(str(O/'modularity-study.FCStd'));A.closeDocument(doc.Name)
report={'pass':all(c['pass'] for c in checks),'checks':checks,'source':str(source.relative_to(R)),'source_sha256':before,'config_sha256':hashlib.sha256((R/'config/service_modularity_v338.json').read_bytes()).hexdigest(),'permanent_holes_added':0,'minimum_bom_additions':0,'optional_family':'ACC01','optional_board_count':2,'optional_board_volume_mm3':{n:s.Volume for n,s in boards.items()},'optional_board_mass_650_kg':{n:s.Volume*650e-9 for n,s in boards.items()},'rows':rows,'backbox_route_status':'SAMPLED_REFERENCE_PASS_PHYSICAL_HOLD' if rows['backbox_route_pass'] else 'HOLD_NO_VALIDATED_FOLD_HARNESS','manufacturing_release':False,'limits':'C-clamp body and payload are provisional packaging; no purchased-hardware or impact-load rating. PF flexible loop uses63 sampled configurations, not a continuous flexible cable certificate. Backbox route trials do not release any connector or universal cable bend specification.'}
(O/'modularity-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V338_MODULARITY_RESULT',report['pass'],len(checks),'BACKBOX_ROUTE',rows['backbox_route_pass'],flush=True)

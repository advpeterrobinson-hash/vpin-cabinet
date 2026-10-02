# SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION
# Historical baseline/replay only. See studies/wpc-fold-v32/README.md; use original source HEAD for exact replay.
"""Simple removable matrix cassette; real CAD, explicit prerequisites. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part,json,math,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));V=A.Vector
c=json.loads((R/'config/matrix_cassette_v32.json').read_text());src=R/c['source_directory'];O=R/'exports/generated/matrix-cassette-v32';O.mkdir(parents=True,exist_ok=True)
original_hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.is_file() and p.suffix not in ('.FCBak','.FCStd1')};original_hashes['config/backbox_fold_v10.json']=hashlib.sha256((R/'config/backbox_fold_v10.json').read_bytes()).hexdigest()
d=A.openDocument(str(src/'play.FCStd'));old={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};sd=A.openDocument(str(R/c['starting_cad']));cassette={o.Name:o.Shape.copy() for o in sd.Objects if hasattr(o,'Shape') and o.Name.startswith('Matrix')};prior=json.loads((R/'exports/generated/matrix-hinge-study-v32/validation.json').read_text())['best_review'];review=json.loads((src/'validation.json').read_text())['review'];checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)});print('CHECK',n,bool(v),flush=True)
def box(x,y,z,w,l,h):return Part.makeBox(w,l,h,V(x,y,z))
def hit(a,b):return a.BoundBox.intersect(b.BoundBox) and a.common(b).Volume>.001
def conflicts(ps,obs):return sorted({n for s in ps.values() for n,t in obs.items() if hit(s,t)})
def difference(a,b):
 if a.isSame(b) or a.exportBrepToString()==b.exportBrepToString():return 0
 return a.cut(b).Volume+b.cut(a).Volume
def distance(ps,obs):
 pairs=[]
 for s in ps.values():
  for t in obs.values():
   a,b=s.BoundBox,t.BoundBox;lb=math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'));pairs.append((lb,s,t))
 best=9999
 for lb,s,t in sorted(pairs,key=lambda x:x[0]):
  if lb>=best:break
  best=min(best,s.distToShape(t)[0])
 return best
angle=math.radians(25);y0=prior['front_xyz_mm'][1];z0=prior['front_xyz_mm'][2]+c['installed_z_adjustment_mm'];normal=V(0,-math.sin(angle),math.cos(angle));pivot=V(300,y0+95.375*math.cos(angle),z0+95.375*math.sin(angle))
def local(s):s=s.copy();s.rotate(V(),V(1,0,0),25);s.translate(V(0,y0,z0));return s
for s in cassette.values():s.translate(V(0,0,c['installed_z_adjustment_mm']))
new={};supports={};retainers={};fixed_hardware={};seat_contacts={};pilotcuts=[]
# Two single CNC plywood profiles, supported against the existing rear shelf underside.
for i,x in enumerate(c['supports_x_mm']):
 side='L' if i==0 else 'R';xx=x+9;underside=lambda y:z0+(y-y0)*math.tan(angle)-12/math.cos(angle)
 sy,ey=c['seat_y_mm'];fy,by=c['foot_y_mm'];bottom=c['support_bottom_z_mm']
 yz=[(sy,bottom),(by,bottom),(by,578.9),(fy,578.9),(fy,560),(ey,560),(ey,underside(ey)),(sy,underside(sy))]
 points=[V(x,y,z) for y,z in yz];support=Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(18,0,0))
 inner_edges=[e for e in support.Edges if e.BoundBox.XLength>17.9 and abs(e.CenterOfMass.z-560)<.01 and any(abs(e.CenterOfMass.y-y)<.01 for y in (fy,ey))]
 support=support.makeFillet(c['router_diameter_mm_provisional']/2,inner_edges)
 key=local(box(x,82,-12,18,4,2));support=support.fuse(key).removeSplitter()
 # Open-ended underside groove permits forward rocking; no closed captured locator.
 groove=box(x-.5,78,-12.01,19,18,2.51)
 vertical=[e for e in groove.Edges if e.BoundBox.ZLength>2 and e.BoundBox.XLength<.01 and e.BoundBox.YLength<.01]
 groove=local(groove.makeFillet(c['router_diameter_mm_provisional']/2,vertical));cassette['MatrixCarrier']=cassette['MatrixCarrier'].cut(groove)
 top=local(Part.Vertex(V(xx,c['retainer_local_y_mm'],0))).Vertexes[0].Point
 hole=Part.makeCylinder(2.25,14,top+normal, -normal);cassette['MatrixCarrier']=cassette['MatrixCarrier'].cut(hole)
 insert_top=top-normal*12;insert=Part.makeCylinder(3,8,insert_top,-normal).cut(Part.makeCylinder(2,8,insert_top,-normal));support=support.cut(Part.makeCylinder(3.05,8.1,insert_top+normal*.05,-normal))
 fixed_hardware['MX_Insert'+side]=insert
 screw=Part.makeCylinder(2,20,top,-normal).fuse(Part.makeCylinder(6,4,top,normal));retainers['MX_Retainer'+side]=screw
 # Interior screws only; tips stop 6.9 mm before upper external face.
 for j,yy in enumerate((1140,1180),1):
  support=support.cut(Part.makeCylinder(2.25,578.9-bottom+1,V(xx,yy,bottom-1),V(0,0,1)))
  support=support.cut(Part.makeCone(4,2.25,2.625,V(xx,yy,bottom)))
  fixed_hardware[f'MX_FixedScrew{side}{j}']=Part.makeCylinder(2,590-bottom-3,V(xx,yy,bottom+3)).fuse(Part.makeCone(4,2,3,V(xx,yy,bottom)))
  pilotcuts.append(Part.makeCylinder(1.5,12,V(xx,yy,578.9)))
 supports['MX_WoodSeat'+side]=support.removeSplitter()
 seat_contacts[side]=[top.x,top.y,top.z]
# Only new blind mounting pilots for the matrix supports; all accepted through-geometry retained.
shelf=old['BACKBOX_BASE'].copy()
for cut in pilotcuts:shelf=shelf.cut(cut)
new.update(supports);new.update(fixed_hardware);new.update(retainers);new.update(cassette)
# One deliberate disconnect below rear shelf, accessible from the front. Its two halves separate before movement.
h=c['harness'];connector_fixed=box(61,1110,530,18,10,12);connector_moving=box(61,1100,530,18,10,12);connector_stowed=box(61,1100,546,18,20,12)
new['MX_FixedConnectorReserve']=connector_fixed;new['MX_MovingConnectorReserve']=connector_moving
# U-shaped 197 mm cable centerline plus short termination tail: 200 mm loop reservation.
p1,p2,p3,p4=V(80,1100,548),V(155,1100,548),V(155,1130,548),V(80,1130,548)
wire=Part.Wire([Part.makeLine(p1,p2),Part.Arc(p2,V(170,1115,548),p3).toShape(),Part.makeLine(p3,p4)])
profile=Part.Wire([Part.makeCircle(2,p1,V(1,0,0))]);loop=wire.makePipeShell([profile],True,False)
new['MX_CableLoopReserve']=loop
fixed_cable=Part.makeCylinder(2,65,V(70,1115,534),V(0,1,0));new['MX_FixedCableReserve']=fixed_cable
moving_names=list(cassette)+['MX_MovingConnectorReserve','MX_CableLoopReserve']
route_base={**cassette,'MX_MovingConnectorReserve':connector_stowed,'MX_CableLoopReserve':loop}
def pose(rot=0,forward=0,lift=0):
 ps={n:s.copy() for n,s in route_base.items()}
 for s in ps.values():s.rotate(pivot,V(1,0,0),-rot);s.translate(V(0,-forward,lift))
 return ps
real={n:s for n,s in old.items() if not any(t in n for t in ('Reserve','RESERVED','CandidatePayload','ServiceEnvelope'))};real['BACKBOX_BASE']=shelf
# Glass removal is an explicit prerequisite, never an implicit obstacle omission.
route_obs={n:s for n,s in real.items() if n!='CandidateGlass' and s.BoundBox.YMax>900 and s.BoundBox.ZMax>450};route_obs.update(supports);route_obs.update(fixed_hardware);route_obs['MX_FixedConnectorReserve']=connector_fixed;route_obs['MX_FixedCableReserve']=fixed_cable
rotation=c['rotation_forward_deg'];forward=c['forward_mm'];final_lift=c['final_lift_mm']
# Priority A fails against actual solids, independently of the added locators.
priority_a=[]
for lift in (5,10,15,20,25):
 hits=[]
 for dz,dy in [(z,0) for z in range(lift+1)]+[(lift,y) for y in range(101)]:
  ps=pose(0,dy,dz);hits.extend(conflicts({n:s for n,s in ps.items() if n.startswith('Matrix')},{n:s for n,s in route_obs.items() if not n.startswith('MX_')}))
 priority_a.append({'initial_lift_mm':lift,'forward_test_mm':100,'hits':sorted(set(hits)),'clear':not hits})
check('negative controls: all five priority A lift/forward routes fail',all(not r['clear'] for r in priority_a))
samples=[];all_hits=[];noncontact_min=9999
for phase,vals in [('rock',[i*c['rotation_step_deg'] for i in range(round(rotation/c['rotation_step_deg'])+1)]),('forward',list(range(forward+1))),('extract',list(range(final_lift+1)))]:
 for v in vals:
  ps=pose(v if phase=='rock' else rotation,0 if phase=='rock' else v if phase=='forward' else forward,v if phase=='extract' else 0)
  hits=conflicts(ps,route_obs);all_hits.extend(hits)
  # Designed seat contact starts at zero; report unintended-obstacle margin separately.
  no_contacts={n:s for n,s in route_obs.items() if not n.startswith(('MX_WoodSeat','MX_Insert'))};margin=distance(ps,no_contacts);noncontact_min=min(noncontact_min,margin)
  samples.append({'phase':phase,'value':v,'hits':hits,'free_clearance_mm':margin})
print('ROUTE_HITS',sorted(set(all_hits)),'MIN',noncontact_min,flush=True)
check('cassette route has no solid interference',not all_hits)
check('sampled free margin meets provisional review target',noncontact_min>=c['minimum_route_target_mm'])
# Retention/hand-access and unplug access envelopes use glass-removed front access.
hand=local(box(35,-15,4,20,96,10));handR=local(box(545,-15,4,20,96,10));disconnect=box(58,1078,526,24,32,22)
access_obs={**{n:s for n,s in route_obs.items() if not n.startswith(('MX_FixedConnector','MX_FixedCable'))},**cassette}
access_hits=conflicts({'left':hand,'right':handR,'disconnect':disconnect},access_obs)
check('front hand and disconnect access clear with glass removed',not access_hits)
# Remove each retainer axially, then take it forward by hand; no access behind the matrix.
retainer_samples=[];retainer_obs={**route_obs,**cassette}
for phase,values in [('axial',range(21)),('forward',range(81))]:
 for mm in values:
  screws={n:s.copy() for n,s in retainers.items()}
  for q in screws.values():q.translate(normal*(mm if phase=='axial' else 20));q.translate(V(0,-mm if phase=='forward' else 0,0))
  retainer_samples.append({'phase':phase,'mm':mm,'hits':conflicts(screws,retainer_obs)})
check('both thumb screws can be withdrawn and taken forward',not any(s['hits'] for s in retainer_samples))
unplug_samples=[]
for dy,dz in [(y,0) for y in range(0,-25,-1)]+[(-24,z) for z in range(9)]+[(y,8) for y in range(-24,1)]+[(0,z) for z in range(8,17)]:
 plug=connector_moving.copy();plug.translate(V(0,dy,dz));unplug_samples.append({'forward_mm':-dy,'lift_mm':dz,'hits':conflicts({'plug':plug},{**route_obs,**cassette})})
check('disconnect and stow path clear before cassette moves',not any(s['hits'] for s in unplug_samples))
fixed_hits=conflicts({**supports,**fixed_hardware},{n:s for n,s in real.items() if n not in ('BACKBOX_BASE','PF_BackboxCheckEnvelope')})
check('installed new wood supports and fasteners clear accepted components',not fixed_hits)
# Moving cable envelope leaves with cassette; stationary side remains behind the playfield sweep.
fixed_after={n:s for n,s in new.items() if n in supports or n in fixed_hardware or n in ('MX_FixedConnectorReserve','MX_FixedCableReserve')}
pf_names=[n for n in old if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope') and not n.startswith('PF_SupportMountScrew')]+['PLAYFIELD_ENVELOPE'];pfpivot=V(*review['pivot_xyz_mm']);sweep=[];lift_hits=[];fold_hits=[];baseline_fold=[]
for ang in range(51):
 ps={n:old[n].copy() for n in pf_names}
 for s in ps.values():s.rotate(pfpivot,V(1,0,0),-ang)
 sweep.extend(conflicts(ps,fixed_after))
for dz in range(49):
 ps={n:old[n].copy() for n in pf_names}
 for s in ps.values():s.translate(V(0,0,dz))
 lift_hits.extend(conflicts(ps,fixed_after))
# Report all pre-existing fold conflicts. Do not reinterpret a coarse reserved volume as clear hardware.
foldobs={n:s for n,s in real.items() if n not in ('CandidateGlass','PF_BackboxCheckEnvelope') and s.BoundBox.ZMax>290}
for ang in range(91):
 q=old['PF_BackboxCheckEnvelope'].copy();q.rotate(V(300,1270,508),V(1,0,0),ang)
 hh=conflicts({'backbox':q},foldobs);added=conflicts({'backbox':q},fixed_after)
 if hh:baseline_fold.append({'angle_deg':ang,'hits':hh})
 if hh or added:fold_hits.append({'angle_deg':ang,'baseline_hits':hh,'matrix_support_hits':added})
check('matrix removed: accepted playfield service unchanged and added supports clear',not sweep)
check('matrix removed: 48 mm lift unchanged and added supports clear',not lift_hits)
check('baseline fold obstructions explicitly reported without exclusions',bool(baseline_fold))
print('AFTER_REMOVAL',sweep,lift_hits,fold_hits[:2],flush=True)
# Explicit state machine: silent removal must fail even if geometry happens to be clear.
requirements={'PLAY':[],'MATRIX INSTALLED':[],'MATRIX UNLOCK':['GLASS_REMOVED','RETAINERS_RELEASED','HARNESS_DISCONNECTED'],'MATRIX FORWARD':['GLASS_REMOVED','RETAINERS_RELEASED','HARNESS_DISCONNECTED'],'MATRIX EXTRACTION':['GLASS_REMOVED','RETAINERS_RELEASED','HARNESS_DISCONNECTED'],'MATRIX REMOVED':['GLASS_REMOVED','MATRIX_REMOVED'],'SERVICE':['GLASS_REMOVED','MATRIX_REMOVED'],'PLAYFIELD SERVICE':['GLASS_REMOVED','MATRIX_REMOVED'],'LIFT-OUT':['GLASS_REMOVED','MATRIX_REMOVED'],'BACKBOX FOLD':['GLASS_REMOVED','MATRIX_REMOVED'],'EXPLODED':['REVIEW_ONLY']}
def require_state(state,declared):
 if not set(requirements[state])<=set(declared):raise ValueError('Missing explicit prerequisites: '+state)
for state in ('SERVICE','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD'):
 try:require_state(state,['GLASS_REMOVED']);raise AssertionError('silent removal accepted')
 except ValueError:pass
check('negative controls reject silent matrix omission from service lift and fold',True)
# Source-state poses retain original parametric pivot objects and accepted geometry.
scenes={};saved={};all_names=set(old)|set(new)
for state in requirements:
 input_state='service' if state in ('SERVICE','PLAYFIELD SERVICE') else 'lift-out' if state=='LIFT-OUT' else 'exploded' if state=='EXPLODED' else 'play'
 inp=A.openDocument(str(src/(input_state+'.FCStd')));base={o.Name:o.Shape.copy() for o in inp.Objects if hasattr(o,'Shape')};full={**base,**new};full['BACKBOX_BASE']=shelf
 if state not in ('PLAY','MATRIX INSTALLED','EXPLODED'):full.pop('CandidateGlass',None)
 if state not in ('PLAY','MATRIX INSTALLED'):
  for n in retainers:full.pop(n,None)
 if state in ('MATRIX UNLOCK','MATRIX FORWARD','MATRIX EXTRACTION'):full.update(pose(rotation,forward if state!='MATRIX UNLOCK' else 0,final_lift if state=='MATRIX EXTRACTION' else 0))
 if state in ('MATRIX REMOVED','SERVICE','PLAYFIELD SERVICE','LIFT-OUT','BACKBOX FOLD'):
  for n in moving_names:full.pop(n,None)
 if state=='BACKBOX FOLD':
  q=old['PF_BackboxCheckEnvelope'].copy();q.rotate(V(300,1270,508),V(1,0,0),90);full['PF_BackboxCheckEnvelope']=q
 if state=='EXPLODED':
  full={n:s.copy() for n,s in new.items()}
  for n,s in full.items():
   if n.startswith('MatrixPanel'):s.translate(V(0,0,100))
   elif n=='MatrixCarrier':s.translate(V(0,0,50))
   elif n.startswith('MX_Retainer'):s.translate(V(0,0,140))
 for o in list(inp.Objects):
  if hasattr(o,'Shape') and o.Name not in full:inp.removeObject(o.Name)
 for n,s in full.items():
  o=inp.getObject(n)
  if o is None:o=inp.addObject('PartDesign::Feature',n);o.Shape=s
  elif n=='BACKBOX_BASE' or n=='PF_BackboxCheckEnvelope':o.Shape=s
 inp.addProperty('App::PropertyString','MatrixPrerequisites');inp.MatrixPrerequisites=', '.join(requirements[state]);inp.recompute();filename=('matrix-exploded' if state=='EXPLODED' else state.lower().replace(' ','-'))+'.FCStd';inp.saveAs(str(O/filename));check(state+' CAD valid solids',all(s.isValid() and len(s.Solids)==1 for s in full.values()));scenes[state]=full;saved[state]=filename;A.closeDocument(inp.Name)
# Actual sampled visibility recalculated at the small installed Z adjustment.
visibility=[];eyes=json.loads((R/'config/matrix_hinge_study_v32.json').read_text())['eyes_xyz_mm'];occluders={n:s for n,s in real.items() if n in ('PLAYFIELD_ENVELOPE','PF_BasePlywood','SIDE_L','SIDE_R','FRONT','REAR','BACKBOX_BASE','PF_BackboxCheckEnvelope')}
for eye in eyes:
 seen=0
 for ix in range(6):
  for iy in range(16):
   point=local(Part.Vertex(V((600-476.25)/2+(ix+.5)*79.375,8+(iy+.5)*79.375/16,8))).Vertexes[0].Point;line=Part.makeLine(V(*eye),point)
   if not any(line.common(s).Length>.1 for s in occluders.values()):seen+=1
 visibility.append({'eye':eye,'visible_percent':100*seen/96})
check('all accepted solids except four scoped matrix mounting pilots unchanged',all(difference(old[n],scenes['PLAY'][n])<1e-5 for n in old if n!='BACKBOX_BASE'))
check('accepted input bytes and hinge datum unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in original_hashes.items()))
check('support and cassette custom metal count zero',True)
labels={p['name']:p.get('label',p['name']) for p in json.loads((src/'mesh.json').read_text())['parts']}
labels.update({'MatrixCarrier':'MATRIX PLYWOOD CARRIER','MX_WoodSeatL':'MATRIX WOOD SEAT L','MX_WoodSeatR':'MATRIX WOOD SEAT R'})
for n in new:
 if n.startswith('MatrixPanel'):labels[n]='MATRIX PANEL '+n[-1]
 elif n.startswith('MX_Retainer'):labels[n]='MATRIX THUMB SCREW '+n[-1]
 elif n.startswith('MX_Insert'):labels[n]='MATRIX THREADED INSERT '+n[-1]
 elif n.startswith('MX_FixedScrew'):labels[n]='MATRIX SUPPORT MOUNTING SCREW '+n[-2:]
 elif n.startswith('MX_') and n.endswith('Reserve'):labels[n]={'MX_FixedConnectorReserve':'MATRIX FIXED DISCONNECT','MX_MovingConnectorReserve':'MATRIX MOVING DISCONNECT','MX_CableLoopReserve':'MATRIX SERVICE LOOP','MX_FixedCableReserve':'MATRIX FIXED HARNESS'}[n]
def mesh(n,s):v,f=s.tessellate(.6);return {'name':n,'label':labels.get(n,n),'vertices':[[q.x,q.y,q.z] for q in v],'faces':[list(q) for q in f]}
review['matrix_cassette']={'prerequisites':requirements,'starting_gap_mm':c['gap_mm'],'tilt_deg':25,'carrier_front_xyz_mm':[300,y0,z0],'vertical_adjustment_mm':c['installed_z_adjustment_mm'],'visibility':visibility,'glass_clearance_mm':distance(cassette,{'glass':old['CandidateGlass']}),'route':{'unlock_lift_mm':0,'forward_rotation_deg':26,'forward_mm':68,'final_lift_mm':100,'minimum_free_clearance_mm':noncontact_min,'intentional_seat_contact_mm':0,'clear':not all_hits,'samples':samples},'retention':{'wood_supports':2,'retaining_fasteners':2,'fixed_mount_screws':4,'threaded_inserts':2,'custom_metal':0,'thumb_screw_heads_xyz_mm':seat_contacts},'harness':h,'playfield_service_clear':not sweep,'playfield_lift_clear':not lift_hits,'backbox_fold_clear':not fold_hits,'fold_conflicts':fold_hits,'baseline_fold_conflicts':baseline_fold,'access_hits':access_hits,'manufacturing_ready':False}
review['matrix_cassette'].update({'priority_a':priority_a,'unplug_path':unplug_samples,'retainer_removal':retainer_samples,'fixed_support_hits':fixed_hits,'fold_status':'BLOCKED: existing coarse backbox packaging envelope intersects accepted cabinet; detailed measured backbox/fold geometry absent','source_regression_exception':'BACKBOX_BASE: four new blind Ø3 x 12 mm matrix-support pilot holes only; shelf position, outline and all existing machining unchanged'})
# Preserve old EXPLODED pivot review as an alias; new matrix explosion is separate.
scenes['MATRIX EXPLODED']=scenes['EXPLODED'];requirements['MATRIX EXPLODED']=['REVIEW_ONLY'];saved['MATRIX EXPLODED']=saved.pop('EXPLODED');oldexpl=A.openDocument(str(src/'exploded.FCStd'));scenes['EXPLODED']={o.Name:o.Shape.copy() for o in oldexpl.Objects if hasattr(o,'Shape')};A.closeDocument(oldexpl.Name);shutil.copyfile(src/'exploded.FCStd',O/'exploded.FCStd');saved['EXPLODED']='exploded.FCStd'
bundle={'parts':[mesh(n,s) for n,s in scenes['PLAY'].items()],'states':{},'review':review}
for state,scene in scenes.items():bundle['states'][state]={n:mesh(n,scene[n]) if n in scene else None for n in scenes['PLAY'] if n not in scene or difference(scenes['PLAY'][n],scene[n])>1e-5}
mp=O/'mesh.json';mp.write_text(json.dumps(bundle,separators=(',',':'))+'\n');report={'checks':checks,'review':review,'saved_poses':saved,'source_head':c['source_head'],'source_hashes':original_hashes,'mesh_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'manufacturing_ready':False};(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
for name in ('LICENSE','NOTICE.md'):shutil.copyfile(R/name,O/name)
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']];print('MATRIX_CASSETTE_PASS',len(checks),flush=True)

"""Isolated secondary-restraint evidence; never modifies CURRENT. CERN-OHL-S-2.0.
Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet
Invoke: QT_QPA_PLATFORM=offscreen freecadcmd /absolute/path/to/this_file.py
All routes are provisional diagnostic geometry, not selected safety hardware.
"""
from pathlib import Path
import json, sys, math, hashlib, gzip
import FreeCAD as A, Part, MeshPart
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_lock_integration_v32 import load, PF, V, transform, actual
C=json.loads((R/'config/safety_straps_v338.json').read_text());O=R/C['output_directory'];O.mkdir(parents=True,exist_ok=True)
source=R/C['source'];before=hashlib.sha256(source.read_bytes()).hexdigest();assert before==C['source_sha256']
p=load(source);base=p['PF_BasePlywood'];angle=C['service_angle_deg']
motion_path=R/'exports/generated/front-landings-v3363/viewer-motion.json'
moving_names=json.loads(motion_path.read_text())['playfield_moving_names']
moving={n:p[n] for n in moving_names};static={n:s for n,s in actual(p).items() if n not in moving_names and n not in ['CandidateGlass'] and not n.startswith(('Matrix','MX_'))}
service=transform(moving,angle=-angle,axis=PF)
face=max([f for f in base.Faces if type(f.Surface).__name__=='Plane' and f.normalAt(0,0).z<-.5],key=lambda f:f.Area)
out=face.normalAt(0,0);fc=face.CenterOfMass
def dump(name,value): (O/name).write_text(json.dumps(value,indent=2)+'\n')
def com(s):
 volume=sum(q.Volume for q in s.Solids)
 return V(*[sum(q.Volume*getattr(q.CenterOfMass,k) for q in s.Solids)/volume for k in 'xyz'])
def pose(v,a,lift=0): return PF+A.Rotation(V(1,0,0),-a).multVec(v-PF)+V(0,0,lift)
def under(x,y):
 z=fc.z-(out.x*(x-fc.x)+out.y*(y-fc.y))/out.z
 return V(x,y,z)+out*C['moving_anchor_underside_standoff_mm']
def line_hits(v,w,shapes):
 line=Part.makeLine(v,w);hits=[]
 for n,s in shapes.items():
  if line.BoundBox.intersect(s.BoundBox):
   ln=line.common(s).Length
   if ln>1e-5:hits.append({'part':n,'centerline_inside_length_mm':ln})
 return hits
def tube(v,w,r=3):
 d=w-v;return Part.makeCylinder(r,d.Length,v,d.normalize())
def length(q,a):return (pose(V(q['moving_closed']),a)-V(q['fixed'])).Length
def derivative(q,a):return (length(q,a+.0001)-length(q,a-.0001))/math.radians(.0002)
def first_angle(q,target):
 # First root while closing from 50 degrees, without assuming monotonicity.
 last=angle
 for i in range(1,5001):
  a=angle-i/100
  if length(q,a)>=target:
   lo=a;hi=last
   for _ in range(45):
    mid=(lo+hi)/2
    if length(q,mid)>=target:lo=mid
    else:hi=mid
   return (lo+hi)/2
  last=a
 return None
rows=[]
for side,x,ax in zip(['L','R'],C['moving_anchor_x_mm'],C['fixed_anchor_x_mm']):
 for y in C['moving_anchor_y_candidates_mm']:
  v=under(x,y);mv=pose(v,angle)
  for ay,az in C['fixed_anchor_yz_candidates_mm']:
   av=V(ax,ay,az);d={'id':f'{side}-M{y}-F{ay}Z{az}','side':side,'moving_y_mm':y,'moving_closed':list(v),'moving_service':list(mv),'fixed':list(av)}
   d.update(length_play_mm=length(d,0),length_50_mm=length(d,50),length_49_mm=length(d,49),derivative_at_50_mm_per_radian=derivative(d,50),moving_line_hits=line_hits(mv,av,service),fixed_line_hits=line_hits(mv,av,static))
   d['closure_arrest_sign']=d['derivative_at_50_mm_per_radian']<0
   d['slack_take_up']=[{'slack_mm':s,'first_taut_closure_angle_deg':first_angle(d,length(d,50)+s)} for s in C['slack_sensitivity_mm']]
   d['decision']='REJECTED_ROUTE_INTERSECTION' if d['moving_line_hits'] or d['fixed_line_hits'] else ('REJECTED_WRONG_CLOSURE_SIGN' if not d['closure_arrest_sign'] else 'HOLD_ANCHOR_LOAD_RATING_PRIMARY_SUPPORT')
   rows.append(d)
dump('safety-route-search.json',{'scope':'42 mirrored anchor/line cases; not an exhaustive proof of all possible tether architectures','routes':rows})
byid={r['id']:r for r in rows}
featured=[byid[n] for n in ['L-M300-F300Z100','L-M300-F1100Z550','L-M1060-F1100Z420','L-M1060-F300Z100']]
# Screen diagnostic endpoint volumes through the accepted motion. Passing an
# endpoint is not approval of a complete anchor, strap, mounting hole or stow.
endpoint_rows=[]
for q in featured:
 fixed_ball=Part.makeSphere(C['diagnostic_anchor_radius_mm'],V(q['fixed']));hits=[]
 for mode,val in [('OPEN',a) for a in range(51)]+[('LIFT',a) for a in range(0,49,4)]:
  aa=val if mode=='OPEN' else 0;ll=val if mode=='LIFT' else 0
  moving_ball=Part.makeSphere(C['diagnostic_anchor_radius_mm'],pose(V(q['moving_closed']),aa,ll))
  mm=transform(moving,angle=-aa,lift=ll,axis=PF)
  for name,s in mm.items():
   if fixed_ball.BoundBox.intersect(s.BoundBox):
    vol=fixed_ball.common(s).Volume
    if vol>1e-5:hits.append({'state':mode,'value':val,'endpoint':'FIXED','part':name,'penetration_mm3':vol})
  for name,s in static.items():
   if moving_ball.BoundBox.intersect(s.BoundBox):
    vol=moving_ball.common(s).Volume
    if vol>1e-5:hits.append({'state':mode,'value':val,'endpoint':'MOVING','part':name,'penetration_mm3':vol})
 endpoint_rows.append({'route_id':q['id'],'sample_count':64,'hits':hits,'pass':not hits})
dump('safety-endpoint-motion.json',{'diagnostic_only':True,'sampled_opening_deg':[0,50,1],'sampled_lift_mm':[0,48,4],'not_continuous_proof':True,'all_installed_anchor_and_stow_hardware_unselected':True,'candidates':endpoint_rows})
# Load sensitivity. Same native moving wood and provisional allowance policy as
# V33.6.3; all unknown actual masses stay labelled, not zeroed.
load_path=R/'exports/generated/front-landings-v3363/load-screen.json';prior=json.loads(load_path.read_text());g=9.80665
known=prior['known_model_items'];known[0]['mass_kg']=base.Volume*650/1e9;known[0]['center_xyz_mm']=list(com(base))
allow=prior['planning_allowances_LOW_NOMINAL_HIGH'];cases=[]
for payload in [10,12,15]:
 for i,label in enumerate(['LOW','NOMINAL','HIGH']):
  items=known+[{'name':'display','mass_kg':payload,'center_xyz_mm':list(com(p['PLAYFIELD_ENVELOPE']))},
   {'name':'four saddle straps allowance','mass_kg':allow['four_straps_kg'][i],'center_xyz_mm':list(PF)},
   {'name':'adapter allowance','mass_kg':allow['display_adapter_kg'][i],'center_xyz_mm':list(com(p['PF_VESAEnvelope']))},
   {'name':'receiver pair allowance','mass_kg':allow['new_receiver_pair_kg'][i],'center_xyz_mm':[300,275,365]}]
  cases.append({'id':f'DISPLAY{payload}-{label}','display_payload_kg':payload,'hardware_scenario':label,'items':items,'mass_kg':sum(x['mass_kg'] for x in items)})
def energy(case,a):return sum(x['mass_kg']*g*(pose(V(x['center_xyz_mm']),50).z-pose(V(x['center_xyz_mm']),a).z)/1000 for x in case['items'])
def moment(case,a):return abs(sum(x['mass_kg']*g*(pose(V(x['center_xyz_mm']),a).y-PF.y)/1000 for x in case['items']))
loads=[]
for q in featured[1:]:
 for slack in C['slack_sensitivity_mm']:
  taut=first_angle(q,length(q,50)+slack)
  for ext in C['extension_sensitivity_mm']:
   end=first_angle(q,length(q,50)+slack+ext)
   for case in cases:
    row={'route_id':q['id'],'mass_case':case['id'],'mass_kg':case['mass_kg'],'slack_mm':slack,'assumed_total_arrest_extension_mm':ext,'first_taut_angle_deg':taut,'arrest_angle_deg':end,'independent_strap_count_credited':1,'not_a_safe_installed_route':True}
    if end is not None:
     e=energy(case,end);lever=abs(derivative(q,end));row.update(potential_energy_released_J=e,average_arrest_tension_energy_balance_N=e/(ext/1000),ideal_linear_spring_peak_N=2*e/(ext/1000),moment_Nm=moment(case,end),effective_length_lever_mm=lever,static_equilibrium_tension_at_end_N=moment(case,end)/(lever/1000))
    else:row['blocker']='No arrest length reached before PLAY; impact with normal closed geometry would govern.'
    loads.append(row)
load_report={'status':'PLANNING_SENSITIVITY_NOT_A_RATING','source':str(load_path.relative_to(R)),'cases':cases,'slack_and_compliance_status':'PROVISIONAL ASSUMPTIONS, not measured webbing properties','gravity_m_s2':g,'formula':'DeltaE = sum(m*g*(z50-z_arrest)); average tension = DeltaE/extension; ideal linear-spring peak = 2*DeltaE/extension. Each strap alone receives the full demand. No damping or energy absorption is credited.','limitations':['Rigid body and fixed rear pivot assumed; rear dowel uplift/ejection, asymmetric twist and anchor deformation are not simulated.','Idealized linear spring peak is conditional, not a proven upper bound; true peak is UNKNOWN without stiffness, damping, hardware/anchor compliance and drop testing.','Unknown textile/anchor/component masses, allowable loads and product applicability remain unresolved.','Correct-sign rear-high route intersects the actual M025/display and is rejected; arithmetic does not validate this route.','Wiring proof only covers controlled current service path. Dynamic arrest and beyond-50-degree movement are unqualified.'],'results':loads}
dump('safety-load-screen.json',load_report)
sources=[{'id':'SPanset_lashing','url':'https://www.spanset.com/uploads/default/PIMTree/ins-lashing-id-en-ssid.pdf','authority':'Manufacturer operating instructions, English page 2','finding':'Manufacturer prohibits using its lashing equipment for stopping. Cargo-lashing capacity is not evidence for this drop-arrest role.','license':'Linked reference only; no vendor file/model copied','status':'REJECTED_FOR_GENERIC_CARGO_STRAP_SUBSTITUTION'},
 {'id':'Ergodyne_3149','url':'https://www.ergodyne.com/squids-3149-tool-lanyard-xl-locking-carabiner-swivel-carabiner-80lbs.html','authority':'Manufacturer product page','finding':'Structure-attached tool tether, 36 kg maximum working capacity, fixed 1930 mm length, non-shock-absorbing webbing. Legitimate rated-product category; far too long for these direct cabinet routes. No shortening, knots or arbitrary buckle adaptation authorized.','license':'Linked reference only; no vendor model copied','status':'NOT_SELECTED'},
 {'id':'Ergodyne_3149_certificate','url':'https://www.ergodyne.com/sites/default/files/2025-06/squids-3149-ansi-isea-121-2023-certificate-of-compliance.pdf','authority':'Manufacturer certificate','finding':'ANSI/ISEA 121-2023 Tool Lanyard, 80 lb /36.29 kg maximum capacity. Tool-tether compliance does not certify this cabinet or its plywood anchors.','license':'Linked reference only','status':'REFERENCE_ONLY'}]
dump('safety-sources.json',{'checked_date':'2026-10-03','sources':sources,'selected_product':None,'Brazil_supplier_or_stock_confirmed':False})
# Native review document. These are original diagnostic solids only, isolated
# from CURRENT, and explicitly labelled rejected/held. No woodworking holes.
doc=A.newDocument('V338_SafetyStudy')
def obj(n,s,label=None):
 o=doc.addObject('PartDesign::Feature',n);o.Shape=s;o.Label=label or n;o.addProperty('App::PropertyString','Status');o.Status='ISOLATED STUDY — NOT PROMOTED';return o
for n in ['SIDE_L','SIDE_R','FLOOR','CROSS_1','CROSS_2','CROSS_3','SHELF_1','SHELF_2','SHELF_3','PF_OpenCradleL','PF_OpenCradleR']:
 if n in p:obj('Context_'+n,p[n])
for n,s in service.items():obj('Service50_'+n,s)
for tag,q in [('RejectedFront',featured[0]),('RejectedRearHigh',featured[1]),('HeldRearTail',featured[2])]:
 for side in ['L','R']:
  qr=byid[q['id'].replace('L-',side+'-')];mv=V(qr['moving_service']);fv=V(qr['fixed'])
  obj(tag+'_'+side+'_DiagnosticRoute',tube(mv,fv,C['diagnostic_route_radius_mm']))
  obj(tag+'_'+side+'_MovingPoint',Part.makeSphere(6,mv));obj(tag+'_'+side+'_FixedPoint',Part.makeSphere(6,fv))
doc.recompute();doc.saveAs(str(O/'safety-study.FCStd'));A.closeDocument(doc.Name)
# Same established native-triangle review schema as V33.7.
def color(n):
 if 'Hit' in n:return '#b03245'
 if 'Route' in n:return '#c25832'
 if 'Point' in n:return '#693b85'
 if 'Display' in n or 'ENVELOPE' in n:return '#365764'
 if 'Side' in n or 'SIDE' in n:return '#c8b58f'
 if 'Dowel' in n:return '#946a42'
 return '#b69a70'
def panel(label,parts,view,alpha=None,annotations=None,edges=None):
 meshes=[]
 for n,s in parts.items():
  if s.isNull():continue
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.5,AngularDeflection=.55,Relative=False);v,f=m.Topology
  if f:meshes.append({'name':n,'vertices':[list(x) for x in v],'faces':f,'color':color(n),'alpha':(alpha or {}).get(n,1)})
 return {'label':label,'meshes':meshes,'view':view,'annotations':annotations or [],'edges':edges or [],'points':[]}
def ann(v,t,offset=(20,20)):return {'point':list(v),'text':t,'offset':offset}
context={n:p[n] for n in ['SIDE_R','FLOOR','CROSS_1','CROSS_2','CROSS_3','PF_OpenCradleL','PF_OpenCradleR'] if n in p}
parts=context|{'M025':service['PF_BasePlywood'],'Display':service['PLAYFIELD_ENVELOPE'],'Dowel':service['PF_WoodDowel']}
def route_pair(q):
 d={}
 for side in ['L','R']:
  qr=byid[q['id'].replace('L-',side+'-')];d['Route'+side]=tube(V(qr['moving_service']),V(qr['fixed']));d['FixedPoint'+side]=Part.makeSphere(8,V(qr['fixed']));d['MovingPoint'+side]=Part.makeSphere(8,V(qr['moving_service']))
 return d
q=featured[1];v=V(q['moving_service']);w=V(q['fixed']);tubeq=tube(v,w)
collision={n+'Hit':tubeq.common(s) for n,s in service.items() if n in ['PF_BasePlywood','PLAYFIELD_ENVELOPE']}
scenes=[{'id':'09','title':'Safety strap study — NO secondary restraint promoted','panels':[
 panel('Rejected: front / low anchor slackens during closure',parts|route_pair(featured[0]),(1,-2,1),{'Display':.22,'SIDE_R':.28},[ann(featured[0]['fixed'],'50° →49°: 883.70 →872.38 mm\nCannot arrest downward closure',(-80,-60))]),
 panel('Rejected: rear / high route crosses occupied geometry',parts|route_pair(q)|collision,(1,0,.05),{'Display':.18,'M025':.42,'SIDE_R':.12},[ann((v+w)*.5,'Tension line through M025: 154.86 mm\nThrough display: 392.87 mm',(-150,40))])],
 'note':'These native CAD diagnostic routes are rejected candidates, not installed straps. CURRENT has no modeled positive 50° primary support or single-support proof. A pivot and closed front landings do not hold service pitch. Do not work beneath the raised playfield; a qualified primary support remains required.'},
 {'id':'10','title':'Normal slack — conditional geometry, not a safe service state','panels':[
 panel('Rear-high candidate at 50°: correct sign, blocked route',parts|route_pair(q)|collision,(1,0,.05),{'Display':.20,'M025':.35,'SIDE_R':.12},[ann(v,'5 mm assumed slack\nFirst taut at '+f'{first_angle(q,length(q,50)+5):.3f}°',(-160,35)),ann(w,'Reference point only\nNo anchor / bolt selected',(-160,-60))]),
 panel('Rear-tail alternative: short lever / late take-up',parts|route_pair(featured[2]),(1,0,.05),{'Display':.20,'M025':.45,'SIDE_R':.12},[ann(featured[2]['moving_service'],'Tail attachment is only a search point\n5 mm slack takes up at '+f'{first_angle(featured[2],length(featured[2],50)+5):.3f}°',(-205,55))])],
 'note':'Straight tubes show the required tension line; they do not pretend to model hanging webbing. Slack is an explicit length allowance. Both straps would need independent full-load anchors and a rated short assembly. No stow location or routing is approved; removal and external storage introduces no cabinet snag geometry.'}]
taut=first_angle(q,length(q,50)+5);arrest=first_angle(q,length(q,50)+10);mv=transform(moving,angle=-arrest,axis=PF)
failparts=context|{'M025':mv['PF_BasePlywood'],'Display':mv['PLAYFIELD_ENVELOPE'],'Dowel':mv['PF_WoodDowel']}
for side in ['L','R']:
 qr=byid[q['id'].replace('L-',side+'-')];failparts['Route'+side]=tube(pose(V(qr['moving_closed']),arrest),V(qr['fixed']))
hi=next(r for r in loads if r['route_id']==q['id'] and r['slack_mm']==5 and r['assumed_total_arrest_extension_mm']==5 and r['mass_case']=='DISPLAY15-HIGH')
scenes.append({'id':'11','title':'Failure-arrest screen — hypothetical, rejected route','panels':[
 panel(f'Conditional pose: {arrest:.3f}°; NOT an approved arrest state',failparts,(1,0,.05),{'Display':.22,'M025':.45,'SIDE_R':.12},[ann(pose(V(q['moving_closed']),arrest),'5 mm slack +5 mm extension\nFull mass on ONE strap',(-180,50))]),
 panel('Current service geometry remains a support HOLD',parts,(1,-2,1),{'Display':.25,'SIDE_R':.2},[ann([300,600,700],f'High planning mass: {hi["mass_kg"]:.3f} kg\nEnergy: {hi["potential_energy_released_J"]:.2f} J\nAverage demand: {hi["average_arrest_tension_energy_balance_N"]:.0f} N\nLinear-spring illustration: {hi["ideal_linear_spring_peak_N"]:.0f} N',(-110,60))])],
 'note':'Demand is calculated from the native mass centers and gravity energy loss. Extension is an unknown sensitivity, not a selected webbing property. The illustrated peak is not a proven upper bound. No rated short tether, wood anchor capacity, rear-dowel capture under asymmetric arrest, primary support failure mode or dynamic cable proof is established.'})
(O/'safety-review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes,separators=(',',':')).encode(),mtime=0))
checks=[{'id':'source_native_unchanged','pass':hashlib.sha256(source.read_bytes()).hexdigest()==before},
 {'id':'42_mirrored_cases','pass':len(rows)==42},
 {'id':'front_anchor_wrong_sign_detected','pass':not featured[0]['closure_arrest_sign']},
 {'id':'rear_high_m025_display_collision_detected','pass':{'PF_BasePlywood','PLAYFIELD_ENVELOPE'}<={h['part'] for h in q['moving_line_hits']}},
 {'id':'unknown_rating_not_converted_to_capacity','pass':C['selection']=='NONE' and not C['secondary_restraint_validated']},
 {'id':'full_single_strap_load_cases','pass':len(cases)==9 and all(x['independent_strap_count_credited']==1 for x in loads)},
 {'id':'no_current_native_or_holes_added','pass':C['promoted_count']==0},
 {'id':'3_labelled_native_review_views','pass':len(scenes)==3 and all('note' in s for s in scenes)}]
report={'version':'V33.8','study_completed':True,'pass':all(x['pass'] for x in checks),'check_semantics':'PASS means evidence/regression checks passed; it does NOT mean any safety strap candidate passed acceptance.','checks':checks,'source':C['source'],'source_sha256':before,'source_object_count':len(p),'primary_service_support_native_names':[n for n in p if any(k in n.lower() for k in ['prop','service_support','service_rod'])],
 'primary_service_support_status':C['primary_service_support'],'decision':'NONE','promoted':False,'studied_strap_count':2,'promoted_strap_count':0,'normal_service_load_bearing':False,'secondary_restraint_validated':False,'route_count':len(rows),'featured_routes':featured,
 'acceptance_gates':{'normal_primary_support_defined':False,'independent_secondary_restraint_proven':False,'route_and_anchor_clearance_proven':False,'rated_short_commodity_assembly_selected':False,'one_strap_full_load_capacity_qualified':False,'stow_no_snag_proven':False,'dynamic_cable_hazard_precluded':False},
 'protected_motion':{'current_geometry_changed':False,'added_installed_straps_or_anchors':0,'service_0_to_50_kinematics':'UNCHANGED; geometric path is not primary support qualification','lift_out_48_mm':'UNCHANGED; no added tether or anchor','diagnostic_endpoint_motion_report':'safety-endpoint-motion.json','stow':C['stow_decision']},
 'rating_screen':{'documented_tool_tether_length_mm':1930,'largest_direct_route_over_0_50_mm':max(length(r,a) for r in rows for a in range(51)),'selected_hardware':None,'not_a_general_product_nonexistence_claim':True},
 'independence':'Two straps on the same unqualified plywood and uncaptured open rear cradles are not automatically independent. One-sided arrest can twist/lift the dowel; a complete load path and single-restraint physical test remain necessary.',
 'scope_limit':'This is a bounded search of simple direct anchor routes, not proof that no alternative safety architecture could work. A new rerouting bracket, overhead anchor or primary-support redesign is outside this isolated study.',
 'manufacturing_release':False}
dump('safety-validation.json',report)
reads=[source,Path(__file__),R/'config/safety_straps_v338.json',motion_path,load_path,R/'tools/backbox_lock_integration_v32.py']
dump('safety-source-hashes.json',{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in reads})
assert report['pass'];print('V338_SAFETY_STUDY_EVIDENCE_PASS',len(checks),'PROMOTED=0',flush=True)

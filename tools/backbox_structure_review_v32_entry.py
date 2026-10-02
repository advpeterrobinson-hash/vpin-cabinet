"""Review structural geometry; promotion prohibited if any integration gate fails. CERN-OHL-S-2.0."""
from pathlib import Path
import sys,json,hashlib,math,shutil
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from backbox_structure_review_v32 import *
O=R/C['output_directory'];O.mkdir(parents=True,exist_ok=True);checks=[]
def check(n,v):
 assert v,n
 checks.append({'check':n,'pass':True})
def read(p):
 d=A.openDocument(str(R/p));d.recompute();ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};A.closeDocument(d.Name);return ss
wood=build_wood();source='exports/generated/matrix-cassette-v32';play0=read(source+'/play.FCStd');removed0=read(source+'/matrix-removed.FCStd');play=update_fixed(play0);removed=update_fixed(removed0);fixed=physical(removed);res=reserves();floor=wood['BB_Floor'];shelf=play['BACKBOX_BASE'];z=C['backbox']['bottom_z_mm']
check('eight valid single backbox wood solids',len(wood)==8 and all(s.isValid() and len(s.Solids)==1 for s in wood.values()))
check('no backbox self intersection',not [q for q in hits(wood,wood) if q['part']<q['obstacle']])
check('upright with glass and matrix passes',not hits(wood,physical(play)))
check('preferred upright glass channel gap',minimum(wood,{n:play[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR']})['mm']>=5)
# Local joint area: horizontal capture shoulder + vertical glue/retention face.
joints={};fasteners={};shaft_checks=[]
for side in ['L','R']:
 s=wood['BB_Side'+side];contact=Part.makeCompound([a.common(b) for a in s.Faces for b in floor.Faces if abs(abs(a.normalAt(0,0).dot(b.normalAt(0,0)))-1)<1e-7 and a.distToShape(b)[0]<1e-7]);horizontal=sum(f.Area for f in contact.Faces if abs(f.normalAt(0,0).z)>.99);vertical=sum(f.Area for f in contact.Faces if abs(f.normalAt(0,0).x)>.99)
 length=floor.BoundBox.YLength;ys=[floor.BoundBox.YMin+25+i*(length-50)/2 for i in range(3)]
 start=-90 if side=='L' else 690;sign=1 if side=='L' else -1
 fasteners[side]=[[start,y,z+9] for y in ys]
 for i,y in enumerate(ys):
  # Planning envelope only. Never cut it into wood or export as drilling.
  shaft=Part.makeCylinder(2,32,V(start,y,z+9),V(sign,0,0));shaft_checks.append(minimum({'axis_envelope':shaft},{n:r for n,r in res.items() if 'Hinge' in n or 'Lock' in n}))
 check(side+' shoulder has full 6 mm capture',abs(horizontal-6*length)<1e-5)
 check(side+' vertical joint face 18 mm high',abs(vertical-18*length)<1e-5)
 # Front corner now retains complete nominal stock, rather than the unused rabbet.
 corner=box(-90 if side=='L' else 672,1100,z,18,40,18)
 check(side+' lower front corner full 18 mm',abs(corner.cut(s).Volume)<1e-6)
 joints[side]={'length_mm':length,'horizontal_capture_area_mm2':horizontal,'vertical_contact_area_mm2':vertical,'total_interface_mm2':contact.Area,'remaining_skin_mm':12,'front_projection_stock_mm':18,'front_projection_mm':47.9,'fastener_points_xyz_mm':fasteners[side],'spacing_mm':ys[1]-ys[0],'longitudinal_end_distance_mm':25,'floor_thickness_edge_center_mm':9,'thread_reach_planning_mm':20}
check('side fastener planning clears hinge/lock reserves in 3D',all(q['mm']>0 for q in shaft_checks))
# Two positive lock points with material/washer/tool room; no hole diameter selected.
locks=[]
for i,(x,y) in enumerate(C['locks']['centers_xy_mm'],1):
 reserve=res['BB_LockWoodReserve'+str(i)];union=floor.fuse(shelf)
 check('lock material '+str(i),reserve.cut(union).Volume<1e-6)
 tool=res['BB_LockToolReserve'+str(i)];obs={**wood,**physical(play)};obs.pop('BB_Floor')
 check('lock upper tool access '+str(i),not hits({'tool':tool},obs))
 locks.append({'center_xy_mm':[x,y],'material_radius_mm':30.7,'washer_backing_radius_mm':20,'tool_radius_mm':18,'tool_height_mm':80,'minimum_outer_center_edge_mm':min(y-floor.BoundBox.YMin,floor.BoundBox.YMax-y,x-18,582-x),'side_of_passage_center_gap_mm':50})
# Hinge attachment corridor: lower flange and arm are intentionally below/outboard.
# Top access excludes its intended floor intersection, all other wood must clear.
access={n:s for n,s in res.items() if 'HingeAccess' in n};arm={n:s for n,s in res.items() if 'HingeArm' in n or 'HingeFlange' in n};pivotres={n:s for n,s in res.items() if 'PivotAccess' in n}
check('hinge upper hardware access gross compatibility',not hits(access,{n:s for n,s in wood.items() if n!='BB_Floor'}))
check('hinge arm/flange gross wood compatibility upright',not hits(arm,{**wood,**fixed}))
pivot_hits=hits(pivotres,{n:s for n,s in fixed.items() if n not in ['SIDE_L','SIDE_R']})
core=[]
for side,x in [('L',18),('R',579)]:
 probe=Part.makeCylinder(4.7625,3,V(x,axis().y,axis().z),V(1,0,0))
 core.extend(hits({'PivotCoreProbe'+side:probe},{'PF_OpenCradle'+side:fixed['PF_OpenCradle'+side]}))
check('gross pivot obstruction detected on both sides',len(pivot_hits)==2 and len(core)==2)
promotion=not pivot_hits
check('promotion blocked for preserved playfield cradle interference',not promotion)
# Side toy zones from historical 210 study, outside the lower service/hinge region.
prior=read('exports/generated/backbox-profile-v32/candidate-210.FCStd');zones={n:s for n,s in prior.items() if n in ['AvailableToyAreaL','AvailableToyAreaR','RemovableRearBoardServiceReserve','LowerServiceToyReserve']}
check('toy side zones exist above hinge access',all(zones[n].BoundBox.ZMin>=655 for n in ['AvailableToyAreaL','AvailableToyAreaR']))
check('generic board / toy zones clear new wood and hardware reserves',not hits(zones,{**wood,**arm,**access}))
# Preserve every unrelated shape exactly, except the two obsolete bores and passage.
changed={'SIDE_L','SIDE_R','BACKBOX_BASE','PF_BackboxCheckEnvelope'}
for n,s in play0.items():
 if n not in changed:check('preserved '+n,s.cut(play[n]).Volume+play[n].cut(s).Volume<1e-5)
# Recompute existing mass model; retain every payload assumption, update wood only.
m=json.loads((R/'exports/generated/backbox-profile-v32/validation.json').read_text())['candidates'][0]['mass']['inventory']
mapn={'BackboxFloorV14':'BB_Floor','BackboxLeftSideV14':'BB_SideL','BackboxRightSideV14':'BB_SideR','BackboxTopV14':'BB_Top','BackboxRearFrameLeftV14':'BB_RearL','BackboxRearFrameRightV14':'BB_RearR','BackboxRearFrameBottomV14':'BB_RearBottom','BackboxRearFrameTopV14':'BB_RearTop'}
for q in m:
 if q['item'] in mapn:
  sh=wood[mapn[q['item']]];q['kg']=sh.Volume*650/1e9;q['cg_xyz_mm']=[sum(v.Volume*getattr(v.CenterOfMass,k) for v in sh.Solids)/sh.Volume for k in 'xyz']
mass=sum(q['kg'] for q in m);cg=V(*[sum(q['kg']*q['cg_xyz_mm'][i] for q in m)/mass for i in range(3)]);weight=mass*9.80665
loads=[];grip=V(300,1054.1,1320.8);rel=cg-axis();gr=grip-axis()
for a in range(91):
 t=math.radians(a);ry=rel.y*math.cos(t)-rel.z*math.sin(t);gy=gr.y*math.cos(t)-gr.z*math.sin(t);hand=weight*ry/gy
 loads.append({'angle_deg':a,'gravity_torque_Nm':-weight*ry/1000,'vertical_operator_force_N':hand,'each_hinge_vertical_reaction_N':(weight-hand)/2})
# Only defined loads/demand, never allowable stress inferred from wood area.
load={'mass_kg':mass,'cg_xyz_mm':list(cg),'weight_N':weight,'inventory':m,'fold_equilibrium':loads,'sensitivity_factor':2,'joint_nominal_pressure_MPa_if_full_mass_shared':weight/(2*joints['L']['horizontal_capture_area_mm2']), 'joint_average_shear_MPa_if_full_mass_shared':weight/(2*joints['L']['vertical_contact_area_mm2']), 'projection_tip_test_load_N':2*9.80665,'projection_18x18_strip_bending_demand_MPa':6*2*9.80665*47.9/(18*18**2)}
contact=face(floor,z).common(face(shelf,z));check('bearing 65672.4 retained',abs(contact.Area-65672.4)<1e-5)
angles=sorted(set(C['angles_deg']+list(range(91))));samples=[]
for a in angles:
 moved=pose(wood,a);hit=hits(moved,fixed);check('fold actual wood '+str(a),not hit)
 gap=minimum(moved,{n:fixed[n] for n in ['CandidateGlassChannelL','CandidateGlassChannelR']})
 samples.append({'angle_deg':a,'hits':hit,'minimum_clearance':minimum(moved,fixed),'channel_clearance_mm':gap['mm'],'floor_shelf_distance_mm':moved['BB_Floor'].distToShape(shelf)[0],'floor_shelf_penetration_mm3':moved['BB_Floor'].common(shelf).Volume})
 if a in C['angles_deg']:print('FOLD',a,gap['mm'],flush=True)
check('preferred channel clearance at samples',min(q['channel_clearance_mm'] for q in samples)>=5)
# Adaptive continuous collision certificate; identical displacement bound to WPC control.
radius=max(math.hypot(y-axis().y,zz-axis().z) for s in wood.values() for y in [s.BoundBox.YMin,s.BoundBox.YMax] for zz in [s.BoundBox.ZMin,s.BoundBox.ZMax]);shift=radius*math.radians(.001);initial=[]
for n,s in wood.items():
 for mm,t in fixed.items():
  if minimum({n:s},{mm:t})['mm']>shift+1e-7:continue
  check('early contact allowed '+n+mm,mm in ['SIDE_L','SIDE_R','REAR','BACKBOX_BASE'] and s.BoundBox.ZMin>=z-1e-7 and t.BoundBox.ZMax<=z+1e-7)
  check('early rising '+n,(s.BoundBox.YMin-axis().y)*math.cos(math.radians(.001))-(s.BoundBox.ZMax-axis().z)*math.sin(math.radians(.001))>0);initial.append([n,mm])
stack=[(.001,90)];intervals=[]
while stack:
 lo,hi=stack.pop();mid=(lo+hi)/2;gap=minimum(pose(wood,mid),fixed);bound=radius*math.radians((hi-lo)/2)
 if gap['mm']>bound+1e-6:intervals.append({'lo_deg':lo,'hi_deg':hi,'midpoint_clearance':gap,'motion_bound_mm':bound})
 else:
  check('adaptive convergence',hi-lo>1e-7);stack.extend([(lo,mid),(mid,hi)])
check('adaptive covers complete range',abs(sum(q['hi_deg']-q['lo_deg'] for q in intervals)-89.999)<1e-7)
# Build full isolated candidate documents from accepted source poses, retaining original object
# properties and live playfield expressions. Only owned backbox/interface replaced.
priorbundle=json.loads((R/source/'mesh.json').read_text());base_report=json.loads((R/source/'validation.json').read_text());saved=base_report['saved_poses'];scenes={}
for state,fn in saved.items():
 d=A.openDocument(str(R/source/fn));ss={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()};ss=update_fixed(ss);ss.update(pose(wood,90) if state=='BACKBOX FOLD' else wood)
 for o in list(d.Objects):
  if o.Name=='PF_BackboxCheckEnvelope':d.removeObject(o.Name)
 for n,s in ss.items():
  o=d.getObject(n)
  if o is None:o=d.addObject('PartDesign::Feature',n);o.Shape=s
  elif n in ['SIDE_L','SIDE_R','BACKBOX_BASE']:o.Shape=s
 for n in wood:
  o=d.getObject(n);o.addProperty('App::PropertyString','DesignAuthority');o.DesignAuthority='config/backbox_structure_review_v32.json; NOT PROMOTED; HINGE / PLAYFIELD CRADLE CONFLICT; NO DRILLING'
 d.addProperty('App::PropertyString','BackboxAuthority');d.BackboxAuthority='CANDIDATE ONLY: wood fold clear; hinge / fixed cradle installation BLOCKED; WPC Y1066.8/Z508'
 d.recompute();check('saved state recompute '+state,not any('Invalid' in o.State for o in d.Objects));d.saveAs(str(O/fn));A.closeDocument(d.Name);scenes[state]=ss
# Additional diagnostic wood-fold poses; hinge installation remains blocked.
for a in [1,15,45]:
 d=A.openDocument(str(O/'matrix-removed.FCStd'))
 for n,s in pose(wood,a).items():d.getObject(n).Shape=s
 d.recompute();d.saveAs(str(O/f'fold-{a}.FCStd'));A.closeDocument(d.Name)
def mesh(n,s):
 vs,fs=s.tessellate(.6);return {'name':n,'label':n,'vertices':[list(p) for p in vs],'faces':[list(f) for f in fs]}
# Preserve original mesh entries for unchanged components, avoiding rounding drift.
oldmesh={p['name']:p for p in priorbundle['parts']};parts=[]
for n,s in scenes['PLAY'].items():parts.append(oldmesh[n] if n in oldmesh and n not in changed else mesh(n,s))
review=priorbundle['review'];review['matrix_cassette'].update({'backbox_fold_clear':True,'fold_conflicts':[],'baseline_fold_conflicts':[],'fold_status':'VALIDATED reconstructed wood 0–90; glass and matrix removed; manufacturing blocked'})
review['backbox_structure_review']={'axis_xyz_mm':list(axis()),'side_lower_depth_mm':210,'floor_front_y_mm':1146,'structural_geometry_reviewed':True,'promoted':False,'hinge_installation_blocked':True,'manufacturing_ready':False}
bundle={'parts':parts,'states':{},'review':review}
for state,ss in scenes.items():
 # Preserve existing variants byte-for-byte, only replace modified interface and BB parts.
 overrides={n:v for n,v in priorbundle['states'][state].items() if n!='PF_BackboxCheckEnvelope'}
 for n in ['SIDE_L','SIDE_R','BACKBOX_BASE']:
  if n in overrides:overrides[n]=mesh(n,ss[n]) if n in ss else None
 for n in wood:
  if state=='BACKBOX FOLD':overrides[n]=mesh(n,ss[n])
 bundle['states'][state]=overrides
raw=json.dumps(bundle,separators=(',',':'))+'\n';(O/'mesh.json').write_text(raw)
report={'source_head':C['source_head'],'checks':checks,'review':review,'mesh_sha256':hashlib.sha256(raw.encode()).hexdigest(),'saved_poses':saved,'joints':joints,'fastener_reserve_clearance':shaft_checks,'locks':locks,'loads':load,'bearing_mm2':contact.Area,'shelf_top_before_mm2':face(play0['BACKBOX_BASE'],z).Area,'shelf_top_after_mm2':face(shelf,z).Area,'toy_zones_mm2':{n:s.Volume for n,s in zones.items() if n.startswith('Available')},'fold_samples':samples,'continuous_certificate':{'initial_contacts':initial,'intervals':intervals,'radius_mm':radius},'promotion_geometry_gates_pass':False,'promoted':False,'pivot_reserve_hits':pivot_hits,'pivot_core_probes':core,'final_holes_frozen':False,'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
detail={'wood':[mesh(n,s) for n,s in wood.items()],'fixed':[mesh(n,play[n]) for n in ['SIDE_L','SIDE_R','REAR','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR','PF_BasePlywood']],'reserves':[mesh(n,s) for n,s in res.items()],'zones':[mesh(n,s) for n,s in zones.items()],'bearing':[mesh('Bearing',contact)],'axis':list(axis())}
(O/'detail-mesh.json').write_text(json.dumps(detail,separators=(',',':'))+'\n')
for n in ['LICENSE','NOTICE.md']:shutil.copyfile(R/n,O/n)
print('BACKBOX_STRUCTURE_REVIEW_PASS',len(checks),'MASS',mass,'JOINT',joints['L'],flush=True)

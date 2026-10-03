"""V33.6.3 exact additive landing manufacturing audit. CERN-OHL-S-2.0.
No existing wood geometry/record is edited. Purchased hardware and CNC release
remain held; final bores are not released by their nominal CAD envelopes.
"""
from pathlib import Path
import json,math,gzip,copy,hashlib,collections
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363';V=A.Vector
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
def slab(s,axis,lo,hi):
 b=s.BoundBox;v=[b.XMin-10,b.YMin-10,b.ZMin-10];sz=[b.XLength+20,b.YLength+20,b.ZLength+20];v[axis]=lo;sz[axis]=hi-lo
 return s.common(Part.makeBox(*sz,V(*v))).removeSplitter()
def shift(s,v):q=s.copy();q.translate(v);return q
def union(shapes):
 q=shapes[0]
 for s in shapes[1:]:q=q.fuse(s)
 return q.removeSplitter()
def dims(s):b=s.BoundBox;return [b.XLength,b.YLength,b.ZLength]
def planar(f):return type(f.Surface).__name__=='Plane'
def footprint(s):
 faces=[]
 for f in s.Faces:
  if planar(f) and abs(abs(f.normalAt(0,0).z)-1)<1e-6:
   q=Part.Face(f.OuterWire);q.translate(V(0,0,-f.CenterOfMass.z))
   if q.normalAt(0,0).z<0:q.reverse()
   faces.append(q)
 if not faces:return None
 merged=union([f.extrude(V(0,0,1)) for f in faces])
 top=[f for f in merged.Faces if planar(f) and abs(f.CenterOfMass.z-1)<1e-6]
 return union([shift(f,V(0,0,-1)) for f in top])
def inner_footprint(s):
 faces=[]
 for f in s.Faces:
  if planar(f) and abs(abs(f.normalAt(0,0).z)-1)<1e-6:
   q=f.copy();q.translate(V(0,0,-f.CenterOfMass.z))
   if q.normalAt(0,0).z<0:q.reverse()
   faces.append(q)
 if not faces:return None
 merged=union([f.extrude(V(0,0,1)) for f in faces])
 top=[f for f in merged.Faces if planar(f) and abs(f.CenterOfMass.z-1)<1e-6]
 return union([shift(f,V(0,0,-1)) for f in top])

def choose_normal(name,s,override=None):
 if override:return V(*override)
 if name in ('SIDE_L','PF_OpenCradleL') or name.startswith('BB_SideL') or name.startswith('CROSS_GUIDE_') and name.endswith('L'):return V(1,0,0)
 if name in ('SIDE_R','PF_OpenCradleR') or name.startswith('BB_SideR') or name.startswith('CROSS_GUIDE_') and name.endswith('R'):return V(-1,0,0)
 if name.startswith('CROSS_') and 'GUIDE' not in name:return V(0,-1,0)
 if name=='FRONT':return V(0,1,0)
 if name in ('REAR','REAR_DOOR') or name.startswith(('BB_Door','BB_RearFrame')):return V(0,-1,0)
 if name=='FLOOR':return V(0,0,-1)
 if name.startswith('SHELF_SUPPORT'):return V(0,0,1)
 if name in ('BB_GlassLowerRail','BB_Floor','BACKBOX_BASE','PC_BASE') or name.startswith('BB_UprightLock'):return V(0,0,1)
 if name.startswith('BB_MonitorDepthShoe'):return V(0,0,1 if s.BoundBox.ZMin<1000 else -1)
 # Largest plane sets stock normal; this is followed by actual residual-geometry audit.
 f=max((f for f in s.Faces if planar(f)),key=lambda f:f.Area);return f.normalAt(0,0)

def localize(s,normal):
 # FACE_A is at local depth z=0; +z is INTO the wood. x/y remain right handed.
 inward=-normal;inward.normalize();rot=A.Rotation(inward,V(0,0,1));q=s.copy();q.rotate(V(),rot.Axis,rot.Angle*180/math.pi)
 # Exact planar extrema avoid the loose bounding box of trimmed diagonal cylinders.
 zs=[f.CenterOfMass.z for f in q.Faces if planar(f) and abs(abs(f.normalAt(0,0).z)-1)<1e-6]
 z0=min(zs);b=q.BoundBox;off=V(b.XMin,b.YMin,z0);q.translate(-off)
 place=A.Placement(-rot.inverted().multVec(off),rot) # overwritten below by exact inverse
 world_to_local=A.Placement(-off,rot);local_to_world=world_to_local.inverse()
 return q,local_to_world,max(zs)-min(zs)


BASE=R/'exports/generated/playfield-rest-v3362'
CONFIG=R/'config/front_landings_v3363.json'
reg=json.loads((BASE/'manufacturing-register.json').read_text())
original_parts=copy.deepcopy(reg['parts']); original_families=copy.deepcopy(reg['families'])
assert (len(original_parts),len(original_families))==(101,59)
assert reg['manufacturing_release'] is False
input_paths=[O/'play.FCStd',O/'geometry-validation.json',CONFIG,BASE/'manufacturing-register.json']
input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}
validation=json.loads((O/'geometry-validation.json').read_text());assert validation['pass']
d=A.openDocument(str(O/'play.FCStd'));source={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name)
old_names={p['source_component'] for p in original_parts}
changed={x['name'] for x in validation.get('changed',[])}
assert not changed & old_names, ('Existing wood changed',changed & old_names)
assert validation.get('current_shapes_changed',[])==[], 'Native current-shape preservation gate failed'
assert validation['source_sha256']==hashlib.sha256((BASE/'play.FCStd').read_bytes()).hexdigest(), 'Wrong previous native authority'
assert not set(validation.get('removed',[])) & old_names
names=[f'FrontLanding{side}_Layer{i}' for side in 'LR' for i in range(1,4)]
assert all(n in source for n in names), 'Missing selected landing laminations'

def serial_wire(w):return [[p.x,p.y] for p in w.discretize(Deflection=.05)]
def export_shape(inst,kind,s):
 p=O/'brep'/(inst+'-'+kind+'.brep');p.parent.mkdir(exist_ok=True);s.exportBrep(str(p));return str(p.relative_to(R))

doc=A.newDocument('V3363ManufacturingReview');installed_doc=A.newDocument('V3363InstalledMembers')
parts=[];families=[];family_shapes=[];audit=[];metrics=[];meshes={};mapping={}
for index,name in enumerate(names):
 side='L' if index<3 else 'R';layer=index%3+1;assembly='P095' if side=='L' else 'P096';inst=f'{assembly}-Layer{layer}'
 native=source[name];assert native.isValid() and len(native.Solids)==1,(name,'invalid solid')
 s,placement,t=localize(native,V(0,0,1));assert abs(t-18)<1e-5,(name,t)
 fp=footprint(s);inner=inner_footprint(s);assert fp and len(fp.Faces)==1 and fp.isValid()
 blank=fp.extrude(V(0,0,t));assert s.cut(blank).Volume<1e-5,(name,'non-planar stock overhang')
 removal=blank.cut(s).removeSplitter()
 # All remaining internal detail is currently purchased-hardware geometry.
 # Keep actual nominal bores in the finished B-rep and separate them from the
 # CNC contour. Their final diameter/depth/positions require purchased parts.
 reference=[]
 for j,rem in enumerate(removal.Solids):
  surfaces=[]
  for f in rem.Faces:
   if type(f.Surface).__name__ in ('Cylinder','Cone'):
    su=f.Surface;record={'surface':type(su).__name__,'axis_local':list(su.Axis),'center_local_mm':list(su.Center),'radius_mm':getattr(su,'Radius',None)}
    if record not in surfaces:surfaces.append(record)
  reference.append({'id':f'{inst}-HW{j+1}','group':'REFERENCE','face_datum':'FACE_A',
   'reference_geometry_brep':export_shape(inst,f'reference-removal{j+1}',rem),
   'reference_volume_mm3':rem.Volume,'depth_range_from_face_A_mm':[max(0,rem.BoundBox.ZMin),min(t,rem.BoundBox.ZMax)],
   'bores':surfaces,'hardware_status':'PURCHASE_BEFORE_CNC','final_diameter_mm':None,'final_depth_mm':None,
   'production_export_policy':'REFERENCE_ONLY_UNTIL_PURCHASED_LANDING_HARDWARE_AND_ASSEMBLY_COUPON',
   'instruction':'Nominal packaging geometry only. Use purchased fitting as guide and a depth stop for manual drilling from FACE_A or an accessible assembled edge; no opposite-face CNC.'})
 # Canonical family comparison includes permitted in-plane rotations only.
 # FACE_B is never converted to a second CNC setup.
 family=None;canonical=A.Placement()
 for fi,fs in enumerate(family_shapes):
  if abs(fs.Volume-s.Volume)>1e-4:continue
  for angle in (0,90,180,270):
   rot=A.Rotation(V(0,0,1),angle);trial=s.copy();trial.rotate(V(),V(0,0,1),angle)
   offset=fs.Solids[0].CenterOfMass-trial.Solids[0].CenterOfMass;trial.translate(offset)
   if diff(trial,fs)<1e-4:
    family=families[fi];canonical=A.Placement(offset,rot);break
  if family:break
 if family is None:
  family={'manufacturing_part_id':f'M{68+len(families):03}','quantity':0,'instances':[],
   'material_class':'STRUCTURAL_PREMIUM','nominal_stock_thickness_mm':18,
   'manufacturing_status':'ONE_SIDE_CNC_PLUS_MANUAL_FINISH'}
  families.append(family);family_shapes.append(s)
 family['quantity']+=1;family['instances'].append(inst);pid=family['manufacturing_part_id']
 contour=export_shape(inst,'outline',fp.OuterWire);finished=export_shape(inst,'finished',s);cnc=export_shape(inst,'cnc-stage',blank)
 bb=fp.BoundBox
 manual=[{'operation':'HARDWARE_DEPENDENT_LANDING_ASSEMBLY','face_datum':'FACE_A','depth_mm':None,
  'tool':'drill/driver, selected pilot, depth stop and purchased-hardware/template guide',
  'instruction':'Label layers before laminating. Clamp and glue three 18 mm layers per side; install two positive lamination screws. Side retention has four screws per landing; do not glue a landing to the cabinet side. Qualify all screw lengths, pilot diameters, edge drilling, M8 adjuster receiver and M6 captive-retention corridor on actual stock before drilling. No second-face CNC.',
  'status':'PURCHASE_BEFORE_CNC','no_exterior_breakthrough':True}]
 row={'manufacturing_part_id':pid,'instance_id':inst,'source_component':name,'assembly_id':assembly,
  'description_en':f'Front playfield landing {side}, layer {layer}',
  'description_pt_BR':f'Apoio frontal do playfield {"esquerdo" if side=="L" else "direito"}, camada {layer}',
  'material_class':'STRUCTURAL_PREMIUM','nominal_stock_thickness_mm':18,'finished_reference_thickness_mm':t,
  'quantity':1,'machining_face':'FACE_A','opposite_face':'FACE_B / NO CNC','face_A_outward_world':[0,0,1],
  'local_to_canonical_matrix':list(canonical.toMatrix().A),'local_to_installed_matrix':list(placement.toMatrix().A),
  'local_datum':'XY min bounds; z=0 finished FACE_A; +z into wood; manual depths reference this datum',
  'finished_xy_bounds_mm':[bb.XMin,bb.YMin,bb.XMax,bb.YMax],'finished_xy_size_mm':[bb.XLength,bb.YLength],
  'cnc_outer_access_brep':contour,'outer_contour_brep':contour,'finished_member_brep':finished,
  'outer_profile_operation':{'group':'CUT','face':'FACE_A','depth_mm':18,'exact_boundary_brep':contour},
  'through_cuts':[],'pockets':[],'reference_features':reference,'manual_finish':manual,'blockers':[],
  'manufacturing_status':'ONE_SIDE_CNC_PLUS_MANUAL_FINISH','facing_reduction_mm':0,
  'fit_dependent':True,'coupon_dependent':True,'fit_expression':'Landing stack = sum(3 * measured_thickness_mm); adjuster nominal height compensates actual stack; receiver/pilot geometry uses measured purchased hardware and coupon',
  'corner_classes':['B_OPEN_EDGE_NO_RELIEF_NEEDED'],'grain':'Long-axis grain preferred; retain 0/180 in preliminary layout',
  'rotation_90_allowed_geometrically':True,'arbitrary_rotation_90_for_packing':False,
  'engraving':{'optional':True,'face':'FACE_A','text':pid+' '+inst,'depth_mm':None,'status':'HOLD_HIDDEN_FACE_OR_LABEL_ONLY'},
  'opposite_face_cnc':False,'mirror_relation':'Exact local geometry comparison with in-plane rotation only; explicit placement preserves handed assembly',
  'corner_policy':'External profile is open to cutter. No blanket dogbones. Purchased-hardware bores remain REFERENCE.',
  'projected_area_mm2':fp.Area,'volume_mm3':s.Volume,'blank_outside_error_mm3':s.cut(blank).Volume,
  'cnc_vs_finished_difference_before_manual_mm3':diff(blank,s),'cnc_stage_brep':cnc,
  'review_outline':serial_wire(fp.OuterWire),'source':[str((O/'play.FCStd').relative_to(R)),name],
  'joinery':'Three 18 mm XY laminations; glue plus two lamination screws per complete landing; four removable side screws per landing, no glue to the side wall. Purchased hardware and coupon govern final drilling.',
  'layer_number_bottom_to_top':layer,'assembly_stage':'05','version':'V33.6.3','manufacturing_release':False,
  'release_hold':'ACTUAL_STOCK + COUPON + PURCHASED_HARDWARE + STRUCTURAL_QUALIFICATION'}
 rebuilt=s.copy();rebuilt.Placement=placement.multiply(rebuilt.Placement);error=diff(rebuilt,native);assert error<1e-4,(name,error)
 parts.append(row);mapping[name]={'assembly_id':assembly,'instance_id':inst,'manufacturing_part_id':pid,'group':'PLAYFIELD_LANDINGS'}
 audit.append({'instance_id':inst,'manufacturing_part_id':pid,'source_component':name,'installed_reconstruction_difference_mm3':error,
  'finished_solids':len(s.Solids),'shape_valid':s.isValid(),'face_A_outward_world':[0,0,1],'opposite_face_CNC':False,
  'stock_thickness_mm':18,'measured_reference_thickness_mm':t,'through_cuts':0,'pockets':0,'reference_features':len(reference),
  'manual_operations':len(manual),'status':row['manufacturing_status'],'before_volume_mm3':0,'after_volume_mm3':s.Volume,'volume_change_mm3':s.Volume,
  'outer_contour_before_mm2':0,'outer_contour_after_mm2':fp.Area,'cutters':{'diameter_mm':4,'natural_internal_radius_mm':2}})
 v,f=s.tessellate(.15);meshes[inst]={'vertices':[list(x) for x in v],'faces':f}
 metrics.append({'instance_id':inst,'volume_mm3':s.Volume,'center_of_mass_local_mm':list(s.Solids[0].CenterOfMass),
  'outer_area_mm2':fp.Area,'projected_material_area_mm2':inner.Area,'removed_stock_volume_mm3':fp.Area*18-s.Volume})
 for dd,shape in [(doc,s),(installed_doc,native)]:
  obj=dd.addObject('PartDesign::Feature',inst.replace('-','_'));obj.Shape=shape;obj.Label=pid+' '+inst
 print('AUDIT',inst,pid,row['manufacturing_status'],s.Volume,flush=True)
# Confirm assembled layer union equals the selected native aggregate, where an
# explicit body is supplied; otherwise the six source members are the authority.
assembly_checks=[]
for side in 'LR':
 layers=[source[f'FrontLanding{side}_Layer{i}'] for i in range(1,4)];u=union(layers)
 assert u.isValid() and len(u.Solids)==1,(side,'disconnected landing stack')
 overlaps=sum(layers[i].common(layers[j]).Volume for i in range(3) for j in range(i+1,3))
 assert overlaps<1e-4,(side,'overlapping laminations',overlaps)
 body=source.get('FrontLanding'+side);delta=diff(u,body) if body else 0
 assert delta<1e-4,(side,'aggregate difference',delta)
 assembly_checks.append({'side':side,'layers':3,'nominal_stack_mm':54,'union_volume_mm3':u.Volume,'layer_overlap_mm3':overlaps,'aggregate_difference_mm3':delta,'aggregate_authority':'native body' if body else 'union of three authoritative native layers'})
# Finished reference bores make handed/layer members distinct, while the CNC
# delivered outline is one proven identical contour across all six laminations.
outline_shapes=[Part.read(str(R/p['outer_contour_brep'])) for p in parts]
outline_faces=[Part.Face(w) for w in outline_shapes]
assert all(diff(outline_faces[0].extrude(V(0,0,1)),f.extrude(V(0,0,1)))<1e-4 for f in outline_faces[1:])
cnc_contours=[{'id':'LANDING-CONTOUR-01','quantity':6,'stock_mm':18,'exact_outer_contour':parts[0]['outer_contour_brep'],'size_mm':parts[0]['finished_xy_size_mm'],'note':'One repeated external CNC contour. Six finished reference members remain distinct because their handed/layer hardware features differ.'}]
newparts=copy.deepcopy(original_parts)+parts;newfamilies=original_families+families
# Existing M025 geometry is untouched, but two new mandatory receivers cannot be
# concealed behind an unchanged historical operation schedule.
base_row=next(p for p in newparts if p['source_component']=='PF_BasePlywood')
base_shape=source['PF_BasePlywood'];to_local=A.Matrix(*base_row['local_to_installed_matrix']).inverse()
receiver_instances=[]
config=json.loads(CONFIG.read_text());lx=config['landing']['pad_left_x_mm'];cy=config['search']['selected_pad_y_mm']+config['retention']['axis_rearward_of_pad_mm']
for side,x in [('L',lx),('R',600-lx)]:
 axis=Part.makeLine(V(x,cy,-1000),V(x,cy,2000));cut=base_shape.common(axis)
 pts=[v.Point for e in cut.Edges for v in e.Vertexes];assert len(pts)>=2,(side,'receiver axis misses M025')
 entry=min(pts,key=lambda p:p.z);exit=max(pts,key=lambda p:p.z)
 receiver_instances.append({'side':side,'entry_world_xyz_mm':list(entry),'entry_local_FACE_A_xyz_mm':list(to_local.multVec(entry)),
  'axis_world':[0,0,1],'axis_local':list(to_local.multVec(entry+V(0,0,1))-to_local.multVec(entry)),
  'stock_path_length_along_axis_mm':exit.z-entry.z,'nominal_maximum_bore_depth_mm':config['retention']['maximum_blind_drill_depth_mm'],
  'final_bore_diameter_mm':None,'final_bore_depth_mm':None,'drill_point_allowance_mm':None})
receiver_op={'operation':'MANUAL_OBLIQUE_BLIND_RECEIVER','face_datum':'FACE_A',
 'working_face':'M025 underside; manual operation only. Coordinates and depth reference the existing FACE_A frame.',
 'quantity':2,'hardware_family':'M6 metal receiver','status':'PURCHASE_BEFORE_CNC',
 'instances':receiver_instances,'depth_mm':None,'geometry_changed':False,
 'tool':'Qualified rigid angle drill guide, drill, depth stop; no accurate freehand drilling claim',
 'instruction':'Install two blind M6 metal receivers on the vertical retention axes. The axes are oblique to the inclined M025 underside. Qualify a rigid drill guide on production-lot scrap using the purchased receiver. Verify pilot, actual axial engagement, drill-point allowance and intact top skin before drilling. Reference maximum bore depth is a packaging limit, not a drilling instruction. FACE_B receives no CNC; this is explicitly manual builder finish. Physical qualification remains HOLD.'}
base_row['manual_finish'].append(receiver_op);base_row['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH'
base_row['v3363_metadata_only_interface']='landing-manual-interface-overlay.json; exact B-rep/volume/profile unchanged'
assert sum(a==b for a,b in zip(newparts[:101],original_parts))==100
assert newfamilies[:59]==original_families
reg.update(version='V33.6.3',parts=newparts,families=newfamilies,manufacturing_pieces=len(newparts),CNC_plywood_pieces=103,
 canonical_families=len(newfamilies),CNC_families=len(newfamilies)-1,manufacturing_release=False,
 installed_components=len({p['source_component'] for p in newparts}),landing_installed_assemblies=2,supersedes='playfield-rest-v3362/manufacturing-register.json FOR CURRENT NESTING ONLY')
assert len(newparts)==107
for path,digest in input_hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Concurrent native writer',path)
def dump(name,data):(O/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
dump('manufacturing-register.json',reg)
dump('manufacturing-audit.json',{'version':'V33.6.3','pass':True,'manufacturing_release':False,
 'source_register':str((BASE/'manufacturing-register.json').relative_to(R)),'source_register_sha256':input_hashes[str(BASE/'manufacturing-register.json')],
 'native_geometry_sha256':input_hashes[str(O/'play.FCStd')],'geometry_validation_sha256':input_hashes[str(O/'geometry-validation.json')],
 'native_configuration_sha256':input_hashes[str(CONFIG)],'changed_audits':audit,'assembly_reconstruction':assembly_checks,'new_CNC_contour_families':cnc_contours,
 'unchanged_piece_geometries_retained':101,'unchanged_piece_rows_retained':100,'metadata_only_changed_instances':[base_row['instance_id']],'canonical_families':len(newfamilies),'counts':dict(collections.Counter(p['manufacturing_status'] for p in newparts)),
 'cutting_rule':'FACE_A external contour only; hardware-dependent bores are REFERENCE/manual HOLD. FACE_B has no CNC.',
 'geometry_rule':'Exact native finished B-reps; each layer reconstructs to its installed shape; six layers form two contiguous bodies.',
 'structural_rule':'Manufacturing audit does not replace landing load/retention qualification.'})
materials=json.loads((R/'config/wood_materials_v335.json').read_text())
for row in parts:
 shape=source[row['source_component']];b=shape.BoundBox
 bounds=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
 materials['parts'].append({'id':row['instance_id'],'assembly_id':row['assembly_id'],'object':row['source_component'],
  'description_en':row['description_en'],'description_pt_BR':row['description_pt_BR'],'quantity':1,'unit':'CAD component',
  'material':'plywood','material_class':'STRUCTURAL_PREMIUM','nominal_thickness_mm':18,
  'nominal_dimensions':{'world_bounds_mm':bounds,'world_size_mm':[b.XLength,b.YLength,b.ZLength],'note':'Installed reference bounds; exact manufacturing contour is in the V33.6.3 register'},
  'source':row['source'],'status':'DESIGN_GEOMETRY_ONLY','measurement_required':True,
  'flatpack_classification':'REQUIRED_FLATPACK_HARDWARE','assembly_stage':'05','parent_assembly':'playfield_landings',
  'notes':'Front playfield closed support; structural premium, no automatic material downgrade. Laminate three layers per side.',
  'price_BRL':None,'installed_coordinate_xyz_mm':list(shape.Solids[0].CenterOfMass),'installation_direction':[0,0,-1],
  'service_removable':True,'normal_assembly_removable':True})
materials['version']='V33.6.3';materials['current_manufacturing_register']=str((O/'manufacturing-register.json').relative_to(R))
(R/'config/wood_materials_v3363.json').write_text(json.dumps(materials,indent=2,ensure_ascii=False)+'\n')
dump('changed-piece-metrics.json',metrics);dump('landing-manufacturing-map.json',mapping)
dump('landing-manual-interface-overlay.json',{'version':'V33.6.3','manufacturing_release':False,'source_component':'PF_BasePlywood','instance_id':base_row['instance_id'],'geometry_changed':False,'operations':[receiver_op]})
(O/'manufacturing-mesh.json.gz').write_bytes(gzip.compress(json.dumps(meshes).encode(),mtime=0))
for d,n in [(doc,'changed-manufacturing-members'),(installed_doc,'changed-installed-members')]:d.recompute();d.saveAs(str(O/(n+'.FCStd')));A.closeDocument(d.Name)
for path,digest in input_hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Concurrent native writer',path)
print('V3363_MANUFACTURING_PASS',len(newparts),len(newfamilies),flush=True)

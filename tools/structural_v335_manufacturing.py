"""One-face B-rep audit reused from V33.1, scoped to authorized changed members.
CERN-OHL-S-2.0. No production release. Existing IDs retained, new IDs appended.
"""
from pathlib import Path
import json,math,gzip,copy
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335';V=A.Vector
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


reg=json.loads((R/'exports/generated/solid-leg-v334/manufacturing-register.json').read_text())
validation=json.loads((O/'geometry-validation.json').read_text());assert validation['pass']
d=A.openDocument(str(O/'play.FCStd'));source={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name)
changed={r['name'] for r in validation['changed']};removed=set(validation['removed']);members=[]
for row in reg['parts']:
 name=row['source_component']
 if name not in changed:continue
 s=source[name];normal=V(*row['face_A_outward_world']);q,placement,t=localize(s,normal)
 p={'object':name,'id':row['assembly_id'],'description_en':row['description_en'].split(' / ')[0],'description_pt_BR':row['description_pt_BR'].split(' / ')[0],'material_class':row['material_class'],'source':['exports/generated/structural-v335/play.FCStd',name]}
 members.append({'instance_id':row['instance_id'],'manufacturing_part_id':row['manufacturing_part_id'],'source':p,'shape':q,'installed_shape':s,'placement':placement,'thickness':t,'stock':row['nominal_stock_thickness_mm'],'face_normal':list(normal),'joinery':'V33.5 authorized geometry; fit regenerated only after production-lot thickness and coupon.'})
s=source['BB_MonitorStopRail'];q,placement,t=localize(s,V(0,0,1))
members.append({'instance_id':'P094-Main','manufacturing_part_id':'M067','source':{'object':'BB_MonitorStopRail','id':'P094','description_en':'Transverse monitor stop rail','description_pt_BR':'Travessa de apoio ajustável do monitor','material_class':'STRUCTURAL_PREMIUM','source':['exports/generated/structural-v335/play.FCStd','BB_MonitorStopRail']},'shape':q,'installed_shape':s,'placement':placement,'thickness':t,'stock':18,'face_normal':[0,0,1],'joinery':'18 x18 transverse rail, two50 x6 captured end lands; two rear-driven retention screws, purchased length/pilot HOLD. M6 adjusters have separate purchased-hardware hold.'})
rows=[];shapedata={};cutstage={};auditdetails={};families=[]
doc=A.newDocument('V335ManufacturingReview');installed_doc=A.newDocument('V335InstalledMembers')
def serial_wire(w):
 # Review polyline only; exact B-rep wires are saved separately. No CAM authority.
 return [[p.x,p.y] for p in w.discretize(Deflection=.05)]
def export_shape(id,kind,s):
 path=O/'brep';path.mkdir(exist_ok=True);s.exportBrep(str(path/(id+'-'+kind+'.brep')))
 return str((path/(id+'-'+kind+'.brep')).relative_to(R))
for mi,m in enumerate(members):
 p=m['source'];name=p['object'];s=m['shape'];t=m['thickness'];stock=m['stock'];inst=m['instance_id']
 wood_fit=(name in ('SIDE_L','SIDE_R','FRONT','REAR','FLOOR','BACKBOX_BASE') or name.startswith(('CROSS_GUIDE','BB_MonitorDepthShoe','BB_Side','BB_Floor','BB_Top','BB_RearFrame','CandidateLegBlock','BB_CassetteFixedCleat','BB_MonitorStopBlock','BB_UprightLock')))
 glass_fit=name.startswith(('BB_GlassLowerRail','BB_GlassTopRetainer'))
 fp=footprint(s)
 assert fp and fp.isValid() and len(fp.Faces)==1,(inst,'footprint',len(fp.Faces),fp.isValid(),[(f.Area,str(f.BoundBox)) for f in fp.Faces])
 blank=fp.extrude(V(0,0,t));outside=s.cut(blank).Volume
 # Exact local blank must contain every retained feature, including tilted walls.
 blocked=[];manual=[];ops=[]
 if outside>1e-4:blocked.append('Projection misses non-prismatic overhang; local manufacturing contour requires explicit resolution')
 remove=blank.cut(s).removeSplitter();machined=blank.copy();details=[]
 try:
  cnc_outer=fp.makeOffset2D(2).makeOffset2D(-2)
  if cnc_outer.isValid() and cnc_outer.Area>=fp.Area-1e-5:
   extra=cnc_outer.cut(fp).Area
   if extra>1e-5:
    machined=cnc_outer.extrude(V(0,0,t))
    manual.append({'operation':'OUTER_REENTRANT_CORNER_FINISH','face':'FACE_A','depth_from_face_A_mm':t,
       'extra_area_mm2':extra,'tool':'small chisel/file','instruction':'Finish only inaccessible R2 reentrant remnants to exact outline, no blanket dogbone. Exact reference and cutter-access contour separate.'})
 except Exception as e:
  cnc_outer=fp;blocked.append('Outer Ø4 cutter-access offset failed: '+str(e))
 removals=[]
 for whole in remove.Solids:
  vertical=all((planar(f) and (abs(f.normalAt(0,0).z)<1e-6 or abs(abs(f.normalAt(0,0).z)-1)<1e-6)) or
    (type(f.Surface).__name__=='Cylinder' and abs(abs(f.Surface.Axis.z)-1)<1e-6) for f in whole.Faces)
  levels=sorted(set(round(max(0,min(t,f.CenterOfMass.z)),7) for f in whole.Faces if planar(f) and abs(abs(f.normalAt(0,0).z)-1)<1e-6))
  if vertical and len(levels)>2:
   for lo,hi in zip(levels,levels[1:]):
    cut=slab(whole,2,lo,hi)
    removals.extend(cut.Solids)
  else:removals.append(whole)
 for j,rem in enumerate(removals):
  b=rem.BoundBox;zlo=max(0,b.ZMin);zhi=min(t,b.ZMax);rid=f'{inst}-R{j+1}';ff=inner_footprint(rem);prismatic=False;err=None
  if ff:
   trial=shift(ff.extrude(V(0,0,zhi-zlo)),V(0,0,zlo));err=diff(trial,rem);prismatic=err<1e-4
  types=sorted(set(type(f.Surface).__name__ for f in rem.Faces))
  top=zlo<1e-5;bottom=zhi>=t-1e-5
  circles=[]
  for f in rem.Faces:
   if type(f.Surface).__name__ in ('Cylinder','Cone'):
    su=f.Surface;axis=su.Axis
    rec={'surface':type(su).__name__,'axis_local':list(axis),'center_local_mm':list(su.Center),
         'radius_mm':getattr(su,'Radius',None),'semi_angle_rad':getattr(su,'SemiAngle',None),
         'surface_depth_range_from_face_A_mm':[max(0,f.BoundBox.ZMin),min(t,f.BoundBox.ZMax)],
         'edge_circle_diameters_mm':sorted(set(round(2*e.Curve.Radius,7) for e in f.Edges if type(e.Curve).__name__=='Circle'))}
    line=Part.makeLine(su.Center-su.Axis*5000,su.Center+su.Axis*5000)
    try:
     ends=[v.Point for e in rem.common(line).Edges for v in e.Vertexes]
     if ends:
      ordered=sorted(ends,key=lambda p:(p.z,p.x,p.y));entry,exit=ordered[0],ordered[-1]
      rec.update(entry_local_xyz_mm=list(entry),exit_local_xyz_mm=list(exit),axial_reference_length_mm=entry.distanceToPoint(exit))
    except Exception:pass
    if rec not in circles:circles.append(rec)
  small=bool(circles) and any(c['radius_mm'] is not None and c['radius_mm']<2-1e-6 for c in circles)
  orthogonal=all(abs(abs(c['axis_local'][2])-1)<1e-6 for c in circles)
  op={'id':rid,'face':'FACE_A','reference_geometry_brep':export_shape(inst,'removal'+str(j+1),rem),
      'depth_range_from_finished_face_A_mm':[zlo,zhi],'surface_types':types,
      'prismatic':prismatic,'prismatic_difference_mm3':err,'bores':circles}
  accessible=False
  if prismatic and ff:
   accessible=ff.extrude(V(0,0,zhi)).cut(remove).Volume<1e-4
  if prismatic and accessible and not small:
   op['group']='CUT' if bottom else 'POCKET';op['depth_mm']=t if bottom else zhi
   # Exact footprint is a machining boundary; sharp internal corners require a
   # local manual finish or later fit-dependent relief, never automatic dogbones.
   sharp=False
   if ff:
    for wire in ff.Wires:
     edges=wire.Edges
     for a in edges:
      if type(a.Curve).__name__=='Line' and any(type(bb.Curve).__name__=='Line' and
          any(va.Point.distanceToPoint(vb.Point)<1e-6 for va in a.Vertexes for vb in bb.Vertexes) and
          abs(a.tangentAt(a.FirstParameter).dot(bb.tangentAt(bb.FirstParameter)))<.99999 for bb in edges if bb!=a):sharp=True
   if sharp:
    manual.append({'operation':'SQUARE_CORNER_FINISH_OR_COUPON_RELIEF','feature':rid,'face':'FACE_A',
       'depth_from_face_A_mm':op['depth_mm'],'tool':'small sharp chisel/file; no power router',
       'instruction':'Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.'})
   op['internal_corner_class']=('D_FIT_DEPENDENT_WOOD_CAPTURE' if wood_fit else 'D_GLASS_LINER_HARDWARE_FIT' if glass_fit else 'A_NONMATING_R2_FUNCTIONALLY_ACCEPTABLE_REFERENCE_HAND_SQUARED') if sharp else 'A_R2_OR_LARGER'
   op['dogbone_selected']=False
   op['square_mating_relief_candidate']=bool(sharp and (wood_fit or glass_fit))
   if ff:op['review_wires']=[serial_wire(w) for w in ff.Wires]
   try:
    reachable=ff.makeOffset2D(-2).makeOffset2D(2)
    if reachable.isNull():raise ValueError('Empty cutter-center region')
    reachable=reachable.common(ff)
    op['tool_access_boundary_brep']=export_shape(inst,'cnc_access'+str(j+1),reachable)
    op['R2_residual_area_mm2']=ff.cut(reachable).Area
    if op['R2_residual_area_mm2']>1e-5 and not sharp:
     manual.append({'operation':'R2_ACCESS_RESIDUAL_FINISH','feature':rid,'face':'FACE_A','depth_from_face_A_mm':zhi,
       'residual_area_mm2':op['R2_residual_area_mm2'],'tool':'small file/chisel',
       'instruction':'Finish the measured cutter-inaccessible residual to the exact reference boundary; no unreported rounding change.'})
    machined=machined.cut(reachable.extrude(V(0,0,zhi)))
   except Exception:
    # A Ø4 plunge hole has a point center domain, which OCC cannot offset as a face.
    if circles and len(circles)==1 and abs(circles[0]['radius_mm']-2)<1e-6:
     machined=machined.cut(rem);op['R2_residual_area_mm2']=0
    else:
     manual.append({'operation':'NARROW_FEATURE_MANUAL_FINISH','feature':rid,'face':'FACE_A','depth_from_face_A_mm':zhi,
        'tool':'drill/chisel/file','instruction':'Offset has no usable Ø4 center domain; use exact reference with ordinary hand tools, subject to local access qualification.'})
   ops.append(op)
  else:
   op['group']='REFERENCE';op['reason']='sub-Ø4 bore' if small else 'edge/oblique bore or countersink' if circles else 'opposite-face recess' if bottom and not top else 'non-prismatic edge or internal feature'
   if circles:
    manual.append({'operation':'DRILL_OR_COUNTERSINK','feature':rid,'face_datum':'FACE_A',
       'depth_range_from_face_A_mm':[zlo,zhi],'bores':circles,
       'tool':'drill/driver, selected pilot/countersink and depth stop; guide for oblique/edge drilling',
       'instruction':'Use the exact local axis and reference removal B-rep. Depth and edge height are measured from finished FACE_A; selected hardware dimensions remain HOLD. For edge/45° bores use a purchased fitting as guide or a separately qualified simple drill guide. No CNC flip.'})
   elif name.startswith('CROSS_'):
    # One-face stepped open-edge pockets leave <= one depth increment of bevel
    # to be sanded to the exact planar reference with an ordinary sanding block.
    stair=[]
    for z1 in range(1,19):
     z0=z1-1
     wa=rem.slice(V(0,0,1),z0);wb=rem.slice(V(0,0,1),z1)
     if not wa or not wb:continue
     fa=union([shift(Part.Face(w),V(0,0,-z0)) for w in wa]);fb=union([shift(Part.Face(w),V(0,0,-z1)) for w in wb])
     fcut=fa.common(fb)
     if fcut.Area<1e-5:continue
     q=fcut.extrude(V(0,0,z1))
     if q.cut(remove).Volume>1e-4:continue
     stair.append(q)
     ops.append({'id':rid+'-STEP'+str(z1),'group':'POCKET','face':'FACE_A','depth_mm':z1,
       'open_edge':True,'reference_geometry_brep':export_shape(inst,'bevel_step'+str(z1),q),
       'review_wires':[serial_wire(w) for w in fcut.Wires],
       'instruction':'Open-edge conservative bevel roughing, Ø4 can overrun the stock edge; finish remaining terraces with sanding block to reference bevel.'})
    if stair:
     machined=machined.cut(union(stair))
     manual.append({'operation':'BEVEL_SANDING_FINISH','feature':rid,'face_datum':'FACE_A','depth_range_from_face_A_mm':[0,t],
       'maximum_depth_step_mm':1,'tool':'flat sanding block and angle/straightedge template',
       'instruction':'Hand-finish only conservative roughing terraces to the exact bevel reference. Both end profiles define the plane; no table saw, router or planer required. Verify full bearing line before assembly.'})
    else:blocked.append(rid+': stepped one-face bevel roughing unresolved')
   else:
    blocked.append(rid+': '+op['reason']+' cannot be asserted Ø4 one-face ready without a specific finishing/decomposition method')
   details.append(op)
 stage_difference=diff(machined,s)
 # Compact identical-family consolidation compares exact completed geometry,
 # same stock/material and machining-facing orientation, not bounding rectangles.
 family=None;canonical_transform=A.Placement()
 for f in families:
  if f['stock']==stock and f['class']==p['material_class'] and abs(f['shape'].Volume-s.Volume)<1e-5 and all(abs(a-b)<1e-5 for a,b in zip(dims(f['shape']),dims(s))):
   if diff(f['shape'],s)<1e-4:family=f;break
 if family is None and name.startswith('CandidateLegBlock'):
  for f in families:
   if f['stock']!=stock or f['class']!=p['material_class'] or abs(f['shape'].Volume-s.Volume)>1e-4:continue
   for angle in (90,180,270):
    rot=A.Rotation(V(0,0,1),angle);q=s.copy();q.rotate(V(),V(0,0,1),angle)
    offset=f['shape'].Solids[0].CenterOfMass-q.Solids[0].CenterOfMass
    if abs(offset.z)>1e-6:continue
    q.translate(offset)
    if diff(q,f['shape'])<1e-4:
     family=f;canonical_transform=A.Placement(offset,rot);break
   if family:break
 if family is None:
  family={'id':'M'+str(len(families)+1).zfill(3),'shape':s,'stock':stock,'class':p['material_class'],'instances':[]};families.append(family)
 family['instances'].append(inst);id=m['manufacturing_part_id']
 fit=wood_fit or glass_fit
 status='BLOCKED' if blocked else 'ONE_SIDE_CNC_PLUS_MANUAL_FINISH' if manual else 'ONE_SIDE_CNC_READY'
 b=fp.BoundBox
 row={'manufacturing_part_id':id,'instance_id':inst,'source_component':name,'assembly_id':p['id'],
      'description_en':p['description_en']+' / '+inst.split('-',1)[1],'description_pt_BR':p['description_pt_BR']+' / '+inst.split('-',1)[1],
      'material_class':p['material_class'],'nominal_stock_thickness_mm':stock,'finished_reference_thickness_mm':t,
      'quantity':1,'machining_face':'FACE_A','opposite_face':'FACE_B / NO CNC','face_A_outward_world':m['face_normal'],
      'local_to_canonical_matrix':list(canonical_transform.toMatrix().A),'local_to_installed_matrix':list(m['placement'].toMatrix().A),'local_datum':'XY min bounds; z=0 finished FACE_A; +z into wood; all depths from this face after any facing',
      'finished_xy_bounds_mm':[b.XMin,b.YMin,b.XMax,b.YMax], 'finished_xy_size_mm':[b.XLength,b.YLength],
      'cnc_outer_access_brep':export_shape(inst,'cnc_outline',cnc_outer.OuterWire),'outer_contour_brep':export_shape(inst,'outline',fp.OuterWire),'finished_member_brep':export_shape(inst,'finished',s),
      'through_cuts':[op for op in ops if op['group']=='CUT'],'pockets':[op for op in ops if op['group']=='POCKET'],
      'reference_features':details,'manual_finish':manual,'blockers':blocked,'manufacturing_status':status,
      'facing_reduction_mm':stock-t,'fit_dependent':fit,'coupon_dependent':True,
      'fit_expression':('measured_thickness_mm + selected_coupon_clearance_mm; laminate heights = sum(actual layer thicknesses), dependent panel widths regenerated from fixed outside datums' if wood_fit else 'measured_glass_thickness_mm + selected_liner_and_channel_clearance_mm' if glass_fit else None),
      'corner_classes':sorted(set(op.get('internal_corner_class','B_OPEN_EDGE_NO_DOGBONE') for op in ops)) or ['B_OPEN_EDGE_NO_RELIEF_NEEDED'],
      'grain':'long-axis grain preferred; use 0/180 only in conservative preliminary layout; structural direction qualification remains',
      'rotation_90_allowed_geometrically':True,'arbitrary_rotation_90_for_packing':False,
      'engraving':{'optional':True,'face':'FACE_A','text':id,'depth_mm':None,'status':'HOLD_HIDDEN_FACE_OR_LABEL_ONLY','note':'No visible-face engraving. Use removable labels unless hidden-face location verified; separate ENGRAVE group.'},
      'opposite_face_cnc':False,'mirror_relation':'Exact identical families consolidated by Boolean comparison, including in-plane rotations for leg layers; local-to-canonical and local-to-installed matrices preserve FACE_A. No CNC flip.',
      'corner_policy':'A radius >=2 / B open; square mating corners C relief proposal or D coupon HOLD, otherwise hand-square exact reference. No blanket dogbones.',
      'projected_area_mm2':fp.Area,'volume_mm3':s.Volume,'blank_outside_error_mm3':outside,
      'cnc_vs_finished_difference_before_manual_mm3':stage_difference,'cnc_stage_brep':export_shape(inst,'cnc_stage',machined),
      'review_outline':serial_wire(fp.OuterWire),'source':p['source'],'joinery':m['joinery']}
 if stock-t>1e-5:row['pockets'].insert(0,{'id':inst+'-FACE_REDUCTION','group':'POCKET','face':'FACE_A','depth_mm':stock-t,
     'whole_face':True,'instruction':'Face standard stock down to reference finished thickness; reset depth zero to finished FACE_A. Actual stock thickness replaces nominal before release.'})
 rows.append(row);shapedata[inst]=s;cutstage[inst]=machined
 obj=doc.addObject('PartDesign::Feature',inst.replace('-','_'));obj.Shape=s;obj.Label=id+' '+inst
 obj.addProperty('App::PropertyString','ManufacturingStatus');obj.ManufacturingStatus=status
 obj.addProperty('App::PropertyString','Authority');obj.Authority='NOMINAL REVIEW ONLY; FULL SHEET RELEASE BLOCKED'
 obj2=installed_doc.addObject('PartDesign::Feature',inst.replace('-','_'));obj2.Shape=m['installed_shape'];obj2.Label=id+' '+inst
 print('AUDIT',mi+1,inst,id,status,'ops',len(ops),'manual',len(manual),'block',len(blocked),flush=True)


for m in members:
 row=next(p for p in rows if p['instance_id']==m['instance_id'])
 if row['source_component'] in ['FLOOR','BACKBOX_BASE','BB_MonitorStopRail','BB_MonitorCarrier0','BB_MonitorCarrier1']:
  row['manual_finish'].append({'operation':'HARDWARE_DEPENDENT_RETENTION','face_datum':'FACE_A','tool':'selected pocket jig / drill and depth stop as appropriate','depth_mm':None,'instruction':'V33.5 reference schedule is packaging only; qualify purchased jig, screws and inserts. Underside shelf pockets are MANUAL work referenced from top FACE_A by measured thickness; no second-face CNC.'})
  row['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH' if not row['blockers'] else 'BLOCKED'
  row['fit_dependent']=True;row['fit_expression']='measured_thickness_mm + selected_coupon_clearance_mm'
 row['version']='V33.5'
assert not any(p['blockers'] for p in rows),[(p['instance_id'],p['blockers']) for p in rows if p['blockers']]
by={p['instance_id']:p for p in rows}
parts=[by.get(p['instance_id'],p) for p in reg['parts'] if p['source_component'] not in removed]+[by['P094-Main']]
fams=[]
for id in sorted({p['manufacturing_part_id'] for p in parts}):
 pp=[p for p in parts if p['manufacturing_part_id']==id]
 orig=next((f for f in reg['families'] if f.get('id',f.get('manufacturing_part_id'))==id),None)
 f=copy.deepcopy(orig) if orig else {'id':id,'stock':18,'class':'STRUCTURAL_PREMIUM'}
 f['instances']=[p['instance_id'] for p in pp];f['quantity']=len(pp);fams.append(f)
reg.update(version='V33.5',parts=parts,families=fams,manufacturing_pieces=len(parts),CNC_plywood_pieces=len(parts)-4,canonical_families=len(fams),CNC_families=len(fams)-1,manufacturing_release=False,installed_components=90)
(O/'manufacturing-register.json').write_text(json.dumps(reg,indent=2)+'\n')
meshes={};metrics=[]
for m in members:
 q=m['shape'];fp=footprint(q);inner=inner_footprint(q);v,f=q.tessellate(.15);i=m['instance_id'];meshes[i]={'vertices':[list(p) for p in v],'faces':f}
 metrics.append({'instance_id':i,'volume_mm3':q.Volume,'center_of_mass_local_mm':list(q.Solids[0].CenterOfMass),'outer_area_mm2':fp.Area,'projected_material_area_mm2':inner.Area,'removed_stock_volume_mm3':fp.Area*m['stock']-q.Volume})
(O/'changed-piece-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
(O/'manufacturing-mesh.json.gz').write_bytes(gzip.compress(json.dumps(meshes).encode(),mtime=0))
for d,n in [(doc,'changed-manufacturing-members'),(installed_doc,'changed-installed-members')]:d.recompute();d.saveAs(str(O/(n+'.FCStd')));A.closeDocument(d.Name)
print('V335_MANUFACTURING_PASS',len(parts),len(fams),flush=True)

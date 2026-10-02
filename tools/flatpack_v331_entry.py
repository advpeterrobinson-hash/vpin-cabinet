"""CURRENT B-rep decomposition and one-face operation audit. CERN-OHL-S-2.0.
No production nesting, toolpaths, G-code, or changes to accepted geometry.
"""
from pathlib import Path
import sys,json,math,hashlib,gzip
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/flatpack-v331';O.mkdir(parents=True,exist_ok=True)
V=A.Vector
wood=json.loads((R/'config/wood_materials_v33.json').read_text())['parts']
profile=json.loads((R/'config/manufacturing/profiles/peter_supplier_v1.json').read_text())
source={};hashes={}
for f in {p['source'][0] for p in wood}:
 path=R/f;hashes[f]=hashlib.sha256(path.read_bytes()).hexdigest();d=A.openDocument(str(path))
 for obj in d.Objects:
  if hasattr(obj,'Shape'):source[obj.Name]=obj.Shape.copy()
 A.closeDocument(d.Name)
hashes['config/manufacturing/profiles/peter_supplier_v1.json']=hashlib.sha256((R/'config/manufacturing/profiles/peter_supplier_v1.json').read_bytes()).hexdigest()
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

assemblies=[];members=[]
for p in wood:
 n=p['object'];s=source[n];b=s.BoundBox;parts=[];join='Original single installed part; no decomposition joint.'
 def add(tag,q,stock,normal=None):
  assert q.isValid() and len(q.Solids)==1,(n,tag)
  parts.append((tag,q,stock,normal))
 if n.startswith('CandidateLegBlock'):
  for i in range(7):add('L'+str(i+1),slab(s,2,b.ZMin+18*i,b.ZMin+18*(i+1)),18,(0,0,1))
  join='Seven numbered 18 mm layers, bottom L1 to top L7; full-face glue and clamps. Two diagonal 45-degree reference bores remain in the exact layer B-reps, with manual drilling after lamination via purchased backing/bracket guide; not seven identical bored rectangles.'
 elif n=='BB_GlassTopRetainer':
  add('Cap',slab(s,2,1320.8,1332.8),12,(0,0,1));add('Strip',slab(s,2,1307,1320.8),18,(0,0,-1))
  join='12 mm removable cap plus 744 x 8 x 13.8 strip, one-face reduced from 18. Full 744 x 8 glued land; clamp on a flat datum with 6 mm end offsets. No new holes. Retainer removes as one unit.'
 elif n.startswith('BB_MonitorStopBlock'):
  add('Base18',slab(s,2,b.ZMin,b.ZMin+18),18,(0,0,1))
  add('Cap12',slab(s,2,b.ZMin+18,b.ZMax),12,(0,0,1))
  join='18 mm profiled base plus 12 mm rectangular cap, full 18 x 28 = 504 mm² face-to-face glue land. Flush rear/upright edges locate the cap. Prefer this broad lamination over a 324 mm² edge-butt wing joint; clamp flat. Both stops retain the exact 30 mm height and adjuster envelope.'
 elif n.startswith('BB_CassetteFixedCleat'):
  for i in range(2):add('Ply'+str(i+1),slab(s,2,b.ZMin+i*12,b.ZMin+(i+1)*12),12,(0,0,1))
  join='Two identical 22 x 32 x 12 premium layers, full-face glue/clamp, eight identical layers across four cleats. Finished 24 mm thickness preserved.'
 elif n.startswith('BB_IntakeDownBaffle'):
  front=slab(s,1,b.YMin,b.YMin+6);rest=s.cut(front)
  top=slab(rest,2,b.ZMax-6,b.ZMax);sides=rest.cut(top)
  add('Face',front,6,(0,-1,0));add('Top',top,6,(0,0,1))
  for i,q in enumerate(sorted(sides.Solids,key=lambda t:t.CenterOfMass.x)):add('Side'+str(i+1),q,6,(1,0,0))
  join='Four 6 mm panels, square butt glue seams; clamp against the face panel. Identical left/right kits. Closed top/sides and downward mouth remain exactly unchanged; no added internal cleat reduces the throat.'
 elif n.startswith('BB_HingeCleat'):
  add('Reduced18',s,18,(0,-1,0))
  join='Single standard 18 mm premium blank, face-reduced by 4 mm to finished 14 mm. Rear mating plane and piano-hinge axis unchanged; no separate 14 mm stock and no new lamination.'
 else:add('Main',s,p['nominal_thickness_mm'])
 rebuilt=union([x[1] for x in parts]);delta=diff(rebuilt,s);overlap=sum(q.Volume for _,q,_,_ in parts)-rebuilt.Volume
 assert delta<1e-4 and abs(overlap)<1e-3,(n,delta,overlap)
 assemblies.append({'id':p['id'],'source_component':n,'pieces':[p['id']+'-'+x[0] for x in parts],
                    'decomposed':len(parts)>1 or n.startswith('BB_HingeCleat'),'joinery':join,
                    'symmetric_difference_mm3':delta,'overlap_mm3':overlap,'source_volume_mm3':s.Volume,
                    'rebuilt_volume_mm3':rebuilt.Volume,'functional_envelope_and_mating_surfaces':'EXACT_BREP_UNION'})
 for tag,q,stock,override in parts:
  normal=choose_normal(n,q,override);local,placement,t=localize(q,normal)
  members.append({'instance_id':p['id']+'-'+tag,'source':p,'shape':local,'installed_shape':q,'placement':placement,
                  'thickness':t,'stock':stock,'face_normal':list(normal),'joinery':join})
print('DECOMPOSITION_PASS',len(assemblies),len(members),flush=True)

rows=[];shapedata={};cutstage={};auditdetails={};families=[]
doc=A.newDocument('V331ManufacturingReview');installed_doc=A.newDocument('V331InstalledMembers')
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
 family['instances'].append(inst);id=family['id']
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

doc.recompute();installed_doc.recompute();doc.saveAs(str(O/'manufacturing-members.FCStd'));installed_doc.saveAs(str(O/'installed-members.FCStd'))
for d in (doc,installed_doc):assert all('Invalid' not in o.State for o in d.Objects);A.closeDocument(d.Name)
# Rendering meshes from actual member B-reps, no shape-generating artwork.
meshes={}
for m in members:
 v,faces=m['shape'].tessellate(.15);meshes[m['instance_id']]={'vertices':[list(p) for p in v],'faces':faces}
with gzip.open(O/'review-mesh.json.gz','wt') as f:json.dump(meshes,f)
for fam in families:fam.pop('shape')
idmap=R/'config/manufacturing/part_ids_v331.json'
if idmap.exists():
 expected=json.loads(idmap.read_text())['instance_to_manufacturing_id']
 assert {p['instance_id']:p['manufacturing_part_id'] for p in rows}==expected,'Manufacturing identities changed: revise append-only ID map explicitly, never silently renumber.'
result={'source_head':'a9b16bd5e9a264c96b3be34de7bdce9308e6459b','supplier_profile':profile['id'],'source_sha256':hashes,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'full_sheet_release':False,'geometry_authority':'CURRENT exact finished B-reps; nominal preparation only',
        'parts':rows,'families':families,'assemblies':assemblies}
(O/'manufacturing-register.json').write_text(json.dumps(result,indent=2)+'\n')
print('FLATPACK_V331_CAD_AUDIT_PASS',len(rows),'pieces',len(families),'families',flush=True)

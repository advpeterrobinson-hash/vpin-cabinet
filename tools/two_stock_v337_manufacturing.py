"""V33.7 actual B-rep one-face manufacturing audit. CERN-OHL-S-2.0.
Only authorized stock conversions and the underfront module are revised.
Nominal stocks are exactly12/18 mm, excluding SW01 solid wood. No CNC release.
"""
from pathlib import Path
import json,math,gzip,copy,hashlib,collections,sys
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from validate_plywood_stock_v337 import validate_stock_policy,negative_controls
O=R/'exports/generated/two-stock-user-module-v337';V=A.Vector
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
def center(s):
 # Boolean results may be Compounds despite containing one valid solid.
 assert s.Solids and sum(q.Volume for q in s.Solids)>0
 return sum((q.CenterOfMass*q.Volume for q in s.Solids),V())/sum(q.Volume for q in s.Solids)
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



BASE=R/'exports/generated/front-landings-v3363'
CONFIG=R/'config/underfront_user_module_v337.json'
CONVERSION_MAP=O/'conversion-manufacturing-map.json'
MODULE_MAP=O/'module-manufacturing-map.json'
reg=json.loads((BASE/'manufacturing-register.json').read_text());original_parts=copy.deepcopy(reg['parts']);prior_by={p['instance_id']:p for p in original_parts}
assert (len(original_parts),len(reg['families']))==(107,65) and not reg['manufacturing_release']
input_paths=[O/'play.FCStd',O/'geometry-validation.json',CONFIG,CONVERSION_MAP,MODULE_MAP,O/'conversion.FCStd',O/'conversion-validation.json',R/'config/manufacturing/stock_policy_v337.json',R/'tools/validate_plywood_stock_v337.py',BASE/'manufacturing-register.json']
input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}
validation=json.loads((O/'geometry-validation.json').read_text());assert validation['pass']
d=A.openDocument(str(O/'play.FCStd'));source={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name)
conversion=json.loads(CONVERSION_MAP.read_text());module=json.loads(MODULE_MAP.read_text())
conversion_validation=json.loads((O/'conversion-validation.json').read_text());assert conversion_validation['pass']
assert conversion_validation['conversion_sha256']==input_hashes[str(O/'conversion.FCStd')]
optional_sources=conversion_validation.get('optional_breps',{})
assert set(optional_sources)=={'BB_FanBlankL','BB_FanBlankR'}
for name,path in optional_sources.items():
 assert name not in source,('Optional blank must not overlap active fan state',name)
 source[name]=Part.read(str(R/path))
# Normalize the two producer maps without weakening their geometry authority.
module['parts']=module.get('parts',module.get('members',[]))
for e in module['parts']:
 e['local_brep']=e.get('local_brep',e.get('finished_member_brep'))
 e['installed_brep']=e.get('installed_brep',e.get('installed_member_brep'))
 e['operation_definitions']=e.get('operation_definitions',e.get('operations_added',[]))
entries=conversion['parts']+module['parts'];assert len({p['instance_id'] for p in entries})==len(entries)
thin={p['instance_id'] for p in original_parts if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART' and p['nominal_stock_thickness_mm'] not in (12,18)}
assert len(thin)==15 and {p['instance_id'] for p in conversion['parts']}==thin
assert all(p['nominal_stock_thickness_mm']==12 for p in conversion['parts'])
expected_old=thin|{'P005-Main'};assert {p['instance_id'] for p in entries if p['instance_id'] in prior_by}==expected_old
assert {p['instance_id'] for p in entries if p['instance_id'] not in prior_by}=={'P097-Main'}
allowed_sources={p['source_component'] for p in entries}
changed=set(validation['changed_existing']) if 'changed_existing' in validation else {r['name'] for r in validation['changed']}
assert changed,'Native validation must explicitly enumerate changed existing components'
assert not (changed & {p['source_component'] for p in original_parts})-allowed_sources
members=[];entry_by={e['instance_id']:e for e in entries}
for entry in entries:
 inst=entry['instance_id'];old=prior_by.get(inst,{});name=entry['source_component']
 normal=entry.get('face_A_outward_world',old.get('face_A_outward_world'))
 assert normal is not None,(inst,'FACE_A required')
 native=Part.read(str(R/entry['installed_brep'])) if entry.get('installed_brep') else source[name].copy()
 if entry.get('local_brep'):
  q=Part.read(str(R/entry['local_brep']));placement=A.Placement(A.Matrix(*entry['local_to_installed_matrix']));t=q.BoundBox.ZLength
 else:q,placement,t=localize(native,V(*normal))
 assert q.isValid() and len(q.Solids)==1,(inst,'invalid member')
 stock=entry['nominal_stock_thickness_mm'];assert stock in (12,18)
 assert t<=stock+1e-5,(inst,t,stock)
 if stock-t>1e-5:assert inst=='P063-Main' and abs(t-6)<1e-5,'Only explicit bezel one-face reduction permitted'
 p={'object':name,'id':entry.get('assembly_id',old.get('assembly_id','P097')),
    'description_en':entry.get('description_en',old.get('description_en','Replaceable underfront user-control plate')).split(' / ')[0],
    'description_pt_BR':entry.get('description_pt_BR',old.get('description_pt_BR','Placa substituível de controles do usuário sob a frente')).split(' / ')[0],
    'material_class':entry.get('material_class',old.get('material_class','MODULAR_SECONDARY')),
    'source':[str((O/'play.FCStd').relative_to(R)),name]}
 members.append({'instance_id':inst,'manufacturing_part_id':entry.get('manufacturing_part_id',old.get('manufacturing_part_id','M074')),
  'source':p,'shape':q,'installed_shape':native,'placement':placement,'thickness':t,'stock':stock,'face_normal':normal,
  'joinery':entry.get('joinery',old.get('joinery',''))+' V33.7: exact source profile, measured stock/coupon and purchased interface HOLD; no opposite-face CNC.'})

def open_edge_strip(ff,fp):
 # Exact rectangular strip spans an entire rectangular outer contour and exits
 # an end. A cylindrical tool can overrun the free outer edges by its radius;
 # there is no trapped internal corner at either end of the straight shoulder.
 b=ff.BoundBox;o=fp.BoundBox
 if abs(ff.Area-b.XLength*b.YLength)>1e-5 or abs(fp.Area-o.XLength*o.YLength)>1e-5:return False
 eq=lambda a,b:abs(a-b)<1e-6
 return (eq(b.XMin,o.XMin) and eq(b.XMax,o.XMax) and (eq(b.YMin,o.YMin) or eq(b.YMax,o.YMax))) or (eq(b.YMin,o.YMin) and eq(b.YMax,o.YMax) and (eq(b.XMin,o.XMin) or eq(b.XMax,o.XMax)))

def exact_tool_width_capsule(ff,radius=2):
 centers=[]
 for edge in ff.Edges:
  if type(edge.Curve).__name__=='Circle' and abs(edge.Curve.Radius-radius)<1e-6:
   c=edge.Curve.Center
   if not any(c.distanceToPoint(p)<1e-6 for p in centers):centers.append(c)
 if len(centers)!=2:return None
 a,b=centers;direction=b-a
 if direction.Length<1e-6:return None
 direction.normalize();perp=V(-direction.y,direction.x,0)*radius
 face=Part.Face(Part.makePolygon([a+perp,b+perp,b-perp,a-perp,a+perp]))
 trial=face.extrude(V(0,0,1)).fuse(Part.makeCylinder(radius,1,a)).fuse(Part.makeCylinder(radius,1,b))
 if diff(trial,ff.extrude(V(0,0,1)))>1e-5:return None
 return Part.makeLine(a,b)

rows=[];shapedata={};cutstage={};auditdetails={};families=[]
doc=A.newDocument('V337ManufacturingReview');installed_doc=A.newDocument('V337InstalledMembers')
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
   open_strip=bool(ff and open_edge_strip(ff,fp))
   if open_strip:sharp=False
   if sharp:
    manual.append({'operation':'SQUARE_CORNER_FINISH_OR_COUPON_RELIEF','feature':rid,'face':'FACE_A',
       'depth_from_face_A_mm':op['depth_mm'],'tool':'small sharp chisel/file; no power router',
       'instruction':'Ø4 leaves R2. Keep the exact reference outline; square only required residual corners by hand. Fit-mating captures may instead use coupon-qualified local T-bone in a later regeneration, never blanket relief.'})
   op['internal_corner_class']=('D_FIT_DEPENDENT_WOOD_CAPTURE' if wood_fit else 'D_GLASS_LINER_HARDWARE_FIT' if glass_fit else 'A_NONMATING_R2_FUNCTIONALLY_ACCEPTABLE_REFERENCE_HAND_SQUARED') if sharp else 'A_R2_OR_LARGER'
   op['dogbone_selected']=False
   op['square_mating_relief_candidate']=bool(sharp and (wood_fit or glass_fit))
   if ff:op['review_wires']=[serial_wire(w) for w in ff.Wires]
   try:
    reachable=ff.copy() if open_strip else ff.makeOffset2D(-2).makeOffset2D(2)
    if open_strip:op.update(open_edge=True,tool_radius_overrun_mm=2,tool_access_proof='Exact full-width rectangular strip opens through outer edges; cutter overrun outside finished contour avoids trapped corners; supplier spacing15 mm exceeds required2 mm overrun')
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
    centerline=exact_tool_width_capsule(ff)
    if centerline is not None:
     machined=machined.cut(ff.extrude(V(0,0,zhi)));op['R2_residual_area_mm2']=0
     op['cutter_center_geometry_brep']=export_shape(inst,'tool_width_slot_center'+str(j+1),centerline)
     op['tool_width_feature']='Exact Ø4 capsule; degenerate cutter-center domain is a line, not an inaccessible feature. Supplier CAM remains authoritative.'
    elif circles and len(circles)==1 and abs(circles[0]['radius_mm']-2)<1e-6:
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
 # In-plane rotations preserve FACE_A; no reflection/opposite-face machining.
 family=None;canonical_transform=A.Placement()
 for f in families:
  if f['stock']==stock and f['class']==p['material_class'] and abs(f['shape'].Volume-s.Volume)<1e-5 and all(abs(a-b)<1e-5 for a,b in zip(dims(f['shape']),dims(s))):
   if diff(f['shape'],s)<1e-4:family=f;break
 if family is None:
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



# Reconstruct exact installed manufacturing members and aggregate baffles.
audit=[];mapped={p['instance_id']:p for p in rows};newmeshes={};metrics=[]
for m in members:
 row=mapped[m['instance_id']];entry=entry_by[m['instance_id']];old=prior_by.get(m['instance_id'])
 rebuilt=m['shape'].copy();rebuilt.Placement=m['placement'].multiply(rebuilt.Placement);error=diff(rebuilt,m['installed_shape'])
 assert error<1e-4,(m['instance_id'],'reconstruction',error)
 assert row['manufacturing_status']!='BLOCKED',(m['instance_id'],row['blockers'])
 if old:
  for op in old.get('manual_finish',[]):
   if op.get('operation','').startswith('HARDWARE_DEPENDENT') and op not in row['manual_finish']:row['manual_finish'].append(copy.deepcopy(op))
  merged=copy.deepcopy(old);merged.update(row);row.clear();row.update(merged)
 row['manual_finish']+=copy.deepcopy(entry.get('manual_finish',[]))
 if row['manual_finish']:row['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH'
 row['version']='V33.7';row['manufacturing_release']=False;row['source_geometry_authority']=str((O/'play.FCStd').relative_to(R))+'#'+row['source_component']
 row['geometry_change_reason']=entry.get('note','Two-stock conversion' if m['instance_id'] in thin else 'Underfront interchangeable user module')
 row['interface_operation_definitions']=copy.deepcopy(entry.get('operation_definitions',[]))
 row['assembly_stage']=entry.get('assembly_stage',old.get('assembly_stage','07') if old else '07')
 row['outer_profile_operation']={'group':'CUT','face':'FACE_A','depth_mm':m['thickness'],'exact_boundary_brep':row['outer_contour_brep']}
 if m['instance_id']=='P097-Main':
  row['variant_policy']='ONE required installed plate; alternate layouts replace this instance and are not additive required quantities'
  row['user_controls']={'button_bore_final_mm':None,'USB_cutout_final_mm':None,'status':'USER_ADAPTER_HARDWARE / PURCHASE_BEFORE_CNC'}
 if m['instance_id'] in ('P005-Main','P097-Main'):
  is_floor=m['instance_id']=='P005-Main'
  row['manual_finish'].append({'operation':'HARDWARE_DEPENDENT_UNDERFRONT_ATTACHMENT','face':'FACE_A',
   'quantity':4,'hardware_ids':['I19'] if is_floor else ['F62'],
   'status':'PURCHASE_BEFORE_CNC / MANDATORY_INTERFACE_HOLD','final_hole_diameter_mm':None,
   'depth_from_FACE_A_mm':None,'geometry_cut_now':False,'tool':'drill/driver, qualified locator template and depth stop; purchased insert driver for floor',
   'instruction':('Install four blind metal inserts from the pocket shoulder, 2 mm inward from the FLOOR underside FACE_A datum. Reference insert length10 mm; actual pilot, drill-point depth, engagement and intact opposite skin require purchased hardware and coupon before drilling. No freehand center transfer.' if is_floor else 'Drill four through-clearance holes from rear/up FACE_A after matching the purchased M4 screw, head and receiver layout. Reference centers only; drill dimensions held. Hardware inserts from below at assembly, but the through holes require no opposite-face CNC.'),
   'axis_world':[0,0,1] if is_floor else [0,0,-1],
   'reference_centers_xy_mm':[[230,62],[370,62],[230,158],[370,158]],
   'CNC_future_locator_policy':'Optional shallow locators may be generated on FACE_A only after purchased hardware and coupon; not present in current B-rep'})
  row['manufacturing_status']='ONE_SIDE_CNC_PLUS_MANUAL_FINISH'
  # The actual 4×12 R2 cable-tie slots are geometric through-cuts, not
  # attachment pilot holes. Never turn them into fictitious hardware bores.
 row['release_hold']='ACTUAL12/18STOCK + COUPON + PURCHASED_HARDWARE + QUALIFICATION; no production nesting'
 audit.append({'instance_id':m['instance_id'],'manufacturing_part_id':row['manufacturing_part_id'],'source_component':row['source_component'],
  'installed_reconstruction_difference_mm3':error,'shape_valid':m['shape'].isValid(),'finished_solids':len(m['shape'].Solids),
  'stock_thickness_mm':m['stock'],'finished_thickness_mm':m['thickness'],'opposite_face_CNC':False,
  'before_volume_mm3':old['volume_mm3'] if old else 0,'after_volume_mm3':row['volume_mm3'],
  'volume_change_mm3':row['volume_mm3']-(old['volume_mm3'] if old else 0),
  'outer_contour_before_mm2':old['projected_area_mm2'] if old else 0,'outer_contour_after_mm2':row['projected_area_mm2'],
  'status':row['manufacturing_status'],'through_cuts':len(row['through_cuts']),'pockets':len(row['pockets']),'manual_operations':len(row['manual_finish'])})
 s=m['shape'];fp=footprint(s);inner=inner_footprint(s);cnc=cutstage[m['instance_id']];verts,faces=s.tessellate(.15)
 newmeshes[m['instance_id']]={'vertices':[list(p) for p in verts],'faces':faces}
 metrics.append({'instance_id':m['instance_id'],'volume_mm3':s.Volume,'center_of_mass_local_mm':list(center(cnc)),
  'finished_center_of_mass_local_mm':list(center(s)),'shipping_volume_mm3':cnc.Volume,'shipping_geometry_authority':row['cnc_stage_brep'],
  'outer_area_mm2':fp.Area,'projected_material_area_mm2':inner.Area,'removed_stock_volume_mm3':fp.Area*m['stock']-s.Volume})
aggregate=[]
for name in sorted({m['source']['object'] for m in members}):
 shapes=[m['installed_shape'] for m in members if m['source']['object']==name]
 united=union(shapes);err=diff(united,source[name]);assert err<1e-4,(name,'aggregate reconstruction',err)
 overlap=sum(shapes[i].common(shapes[j]).Volume for i in range(len(shapes)) for j in range(i+1,len(shapes)))
 assert overlap<1e-4,(name,'manufacturing member overlap',overlap)
 aggregate.append({'source_component':name,'members':len(shapes),'union_difference_mm3':err,'member_overlap_mm3':overlap})
parts=[mapped.get(p['instance_id'],p) for p in original_parts]+[mapped[k] for k in mapped if k not in prior_by]
assert len(parts)==108 and sum(p==prior_by[p['instance_id']] for p in parts if p['instance_id'] in prior_by)==91
cncparts=[p for p in parts if p.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART']
assert len(cncparts)==104
stock_policy=json.loads((R/'config/manufacturing/stock_policy_v337.json').read_text())
validate_stock_policy(parts,stock_policy)
# Existing family identities remain stable; compare changed members in each
# family geometrically before claiming their common manufacturing identity.
def family_id(f):return f.get('id',f.get('manufacturing_part_id'))
fams=copy.deepcopy(reg['families']);old_families={family_id(f):f for f in fams}
for pid in sorted({p['manufacturing_part_id'] for p in rows}):
 items=[p for p in parts if p['manufacturing_part_id']==pid]
 exact=[]
 for p in items:
  q=Part.read(str(R/p['finished_member_brep']));q.transformShape(A.Matrix(*p['local_to_canonical_matrix']));exact.append(q)
 assert all(diff(exact[0],q)<1e-4 for q in exact[1:]),(pid,'nonidentical canonical family')
 f=old_families.get(pid)
 if f is None:
  f={'id':pid};fams.append(f)
 f.update(stock=items[0]['nominal_stock_thickness_mm'],nominal_stock_thickness_mm=items[0]['nominal_stock_thickness_mm'],
  **{'class':items[0]['material_class']},instances=[p['instance_id'] for p in items],quantity=len(items))
reg.update(version='V33.7',parts=parts,families=fams,manufacturing_pieces=len(parts),CNC_plywood_pieces=len(cncparts),
 canonical_families=len(fams),CNC_families=len(fams)-1,installed_components=len({p['source_component'] for p in parts}),
 manufacturing_release=False,supersedes='front-landings-v3363/manufacturing-register.json FOR CURRENT NESTING ONLY',
 active_nominal_plywood_stocks_mm=[12,18],stock_policy='config/manufacturing/stock_policy_v337.json')
for path,digest in input_hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Concurrent native input writer',path)
def dump(name,value):(O/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
dump('manufacturing-register.json',reg)
negative=negative_controls(parts,stock_policy);negative.update(version='V33.7',native_sha256=input_hashes[str(O/'play.FCStd')],register_sha256=hashlib.sha256((O/'manufacturing-register.json').read_bytes()).hexdigest(),validator_sha256=input_hashes[str(R/'tools/validate_plywood_stock_v337.py')],policy_sha256=input_hashes[str(R/'config/manufacturing/stock_policy_v337.json')])
dump('stock-policy-negative-control.json',negative)
dump('manufacturing-audit.json',{'version':'V33.7','pass':True,'manufacturing_release':False,
 'native_geometry_sha256':input_hashes[str(O/'play.FCStd')],'geometry_validation_sha256':input_hashes[str(O/'geometry-validation.json')],
 'native_configuration_sha256':input_hashes[str(CONFIG)],'source_register_sha256':input_hashes[str(BASE/'manufacturing-register.json')],
 'input_sha256':input_hashes,'changed_audits':audit,'aggregate_reconstruction':aggregate,
 'unchanged_piece_rows_retained':91,'canonical_families':len(fams),'counts':dict(collections.Counter(p['manufacturing_status'] for p in parts)),
 'stocks_mm':[12,18],'solid_stock_excluded':['SW01'],'all15_previous_thin_stock_members_converted':True,
 'bezel_exception':'M045 finished6 mm preserved from nominal12 mm by explicit one-face6 mm reduction; no6 mm purchased plywood stock',
 'cutting_rule':'FACE_A only; FACE_B / NO CNC. Final hardware/button/USB fits remain held.',
 'geometry_rule':'Actual B-rep contours and volumes; exact aggregate reconstruction; no bounding rectangles substituted for finished members.'})
dump('changed-piece-metrics.json',metrics)
(O/'manufacturing-mesh.json.gz').write_bytes(gzip.compress(json.dumps(newmeshes).encode(),mtime=0))
materials=json.loads((R/'config/wood_materials_v3363.json').read_text());material_by={p['object']:p for p in materials['parts']}
for name in sorted(allowed_sources):
 related=[p for p in parts if p['source_component']==name];stock={p['nominal_stock_thickness_mm'] for p in related};assert len(stock)==1
 s=source[name];b=s.BoundBox;row=material_by.get(name)
 if row is None:
  row={'id':related[0]['assembly_id'],'object':name,'quantity':1,'unit':'CAD component','material':'plywood','material_class':related[0]['material_class'],
   'description_en':related[0]['description_en'],'description_pt_BR':related[0]['description_pt_BR'],'flatpack_classification':'REQUIRED_FLATPACK_HARDWARE',
   'assembly_stage':'07','parent_assembly':'underfront_user_module','price_BRL':None,'service_removable':True,'normal_assembly_removable':True};materials['parts'].append(row)
 row.update(nominal_thickness_mm=next(iter(stock)),source=[str((O/'play.FCStd').relative_to(R)),name],measurement_required=True,status='DESIGN_GEOMETRY_ONLY',
  nominal_dimensions={'world_bounds_mm':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'world_size_mm':[b.XLength,b.YLength,b.ZLength],'note':'Installed bounds only; exact contours and operation plans are in the manufacturing register'},
  installed_coordinate_xyz_mm=list(center(s)))
 if name=='BB_DisplayReplaceableBezel':row['finished_thickness_mm']=6;row['one_face_reduction_mm']=6
materials.update(version='V33.7',current_manufacturing_register=str((O/'manufacturing-register.json').relative_to(R)),stock_policy='config/manufacturing/stock_policy_v337.json')
(R/'config/wood_materials_v337.json').write_text(json.dumps(materials,indent=2,ensure_ascii=False)+'\n')
for d,n in [(doc,'changed-manufacturing-members'),(installed_doc,'changed-installed-members')]:d.recompute();d.saveAs(str(O/(n+'.FCStd')));A.closeDocument(d.Name)
for path,digest in input_hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Concurrent native input writer',path)
print('V337_MANUFACTURING_PASS',len(parts),len(fams),flush=True)

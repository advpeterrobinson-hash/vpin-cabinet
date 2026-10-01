"""Only button-edge plywood relief and two active floor intake stations. CERN-OHL-S-2.0."""
from pathlib import Path
import FreeCAD as A,Part
import json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/notch-floor-fans-v32';O.mkdir(parents=True,exist_ok=True)
c=json.loads((R/'config/notch_floor_fans_v32.json').read_text());N=c['notch'];F=c['fans'];shared=json.loads((R/'config/panel_closure_v32.json').read_text())['rear'];oldfloorc=json.loads((R/'config/floor_detail_v32.json').read_text());audio=json.loads((R/'config/consolidated_audio_v32.json').read_text());src=R/c['source_directory'];source_hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.suffix in ('.FCStd','.json')};prior=json.loads((src/'validation.json').read_text());review=json.loads(json.dumps(prior['review']));assert all(x['pass'] for x in prior['checks']);V=A.Vector
D=A.openDocument(str(src/'play.FCStd'));D.recompute();old={o.Name:o.Shape.copy() for o in D.Objects if hasattr(o,'Shape')};scene={n:s.copy() for n,s in old.items()};checks=[]
def check(n,v):checks.append({'check':n,'pass':bool(v)});print(n,bool(v),flush=True)
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h,axis=V(0,0,1)):return Part.makeCylinder(r,h,V(x,y,z),axis)
def diff(a,b):return a.cut(b).Volume+b.cut(a).Volume
def shifted(s,v):q=s.copy();q.translate(V(*v));return q
def conflicts(parts,obs):
 out=[]
 for n,s in parts.items():
  for k,t in obs.items():
   if n==k:continue
   if s.BoundBox.intersect(t.BoundBox):
    v=s.common(t).Volume
    if v>.01:out.append([n,k,round(v,5)])
 return out
alpha=review['closed_slope_deg'];a=math.radians(alpha);bz=400.05+45*math.tan(a)-12-55*math.cos(a)
def tf(s):s=s.copy();s.rotate(V(),V(1,0,0),alpha);s.translate(V(0,45,bz));return s
def inv(s):s=s.copy();s.translate(V(0,-45,-bz));s.rotate(V(),V(1,0,0),-alpha);return s
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
def mirrored(s):q=s.copy();q.transformShape(mirror,True);return q
# All service volumes are design reservations derived from the approved CAD, not vendor machining data.
service={};wires=[]
for kind in ('primary','secondary'):
 bc=review['buttons'][kind];contact=old['LeafContacts_'+kind+'_L'].BoundBox
 wire=box(old['LeafBracket_'+kind+'_L'].BoundBox.XMax,bc['y_mm']-N['wire_forward_y_mm'],contact.ZMin-N['wire_below_contact_mm'],N['service_wire_inward_extension_mm'],N['wire_forward_y_mm']+N['wire_rearward_y_mm'],contact.ZLength+N['wire_below_contact_mm']+N['wire_above_contact_mm']);wires.append(wire)
 tool=cyl(43,bc['y_mm'],bc['z_mm'],N['tool_radius_mm'],N['tool_inward_end_x_mm']-43,V(1,0,0))
 for side in ('L','R'):
  service[f'ButtonWireServiceReserve_{kind}_{side}']=wire if side=='L' else mirrored(wire)
  service[f'ButtonToolServiceReserve_{kind}_{side}']=tool if side=='L' else mirrored(tool)
  service[f'ButtonBodyServiceReserve_{kind}_{side}']=old['LeafButton_'+kind+'_'+side].copy()
  br=old['LeafBracket_'+kind+'_'+side].BoundBox;ct=old['LeafContacts_'+kind+'_'+side].BoundBox
  service[f'ButtonLeafServiceReserve_{kind}_{side}']=box(min(br.XMin,ct.XMin),min(br.YMin,ct.YMin),min(br.ZMin,ct.ZMin),max(br.XMax,ct.XMax)-min(br.XMin,ct.XMin),max(br.YMax,ct.YMax)-min(br.YMin,ct.YMin),max(br.ZMax,ct.ZMax)-min(br.ZMin,ct.ZMin))
# Identical R arcs at the exposed mouth and root, with one short straight bridge.
base_local=inv(old['PF_BasePlywood']);b=base_local.BoundBox;x0=b.XMin;r=N['corner_radius_mm'];depth=N['depth_mm'];x1=x0+depth
assert depth>=2*r and N['trial_cutter_diameter_mm']/2<=r
y0=b.YMin;y1=max(inv(w).BoundBox.YMax for w in wires)+N['service_clearance_mm']+2*r;z=b.ZMin-1
P=lambda x,y:V(x,y,z);q=math.sqrt(.5)
edges=[Part.Arc(P(x0,y0),P(x0+r-r*q,y0+r*q),P(x0+r,y0+r)).toShape(),Part.makeLine(P(x0+r,y0+r),P(x1-r,y0+r)),Part.Arc(P(x1-r,y0+r),P(x1-r+r*q,y0+2*r-r*q),P(x1,y0+2*r)).toShape(),Part.makeLine(P(x1,y0+2*r),P(x1,y1-2*r)),Part.Arc(P(x1,y1-2*r),P(x1-r+r*q,y1-2*r+r*q),P(x1-r,y1-r)).toShape(),Part.makeLine(P(x1-r,y1-r),P(x0+r,y1-r)),Part.Arc(P(x0+r,y1-r),P(x0+r-r*q,y1-r*q),P(x0,y1)).toShape(),Part.makeLine(P(x0,y1),P(x0-10,y1)),Part.makeLine(P(x0-10,y1),P(x0-10,y0)),Part.makeLine(P(x0-10,y0),P(x0,y0))]
cutL=tf(Part.Face(Part.Wire(edges)).extrude(V(0,0,b.ZLength+2)));cutR=mirrored(cutL);removedL=old['PF_BasePlywood'].common(cutL);removedR=old['PF_BasePlywood'].common(cutR);scene['PF_BasePlywood']=old['PF_BasePlywood'].cut(cutL).cut(cutR).removeSplitter()
check('one mirrored notched plywood base solid',scene['PF_BasePlywood'].isValid() and len(scene['PF_BasePlywood'].Solids)==1 and diff(scene['PF_BasePlywood'],mirrored(scene['PF_BasePlywood']))<1e-4)
clearance=[]
for side in ('L','R'):
 for kind in ('primary','secondary'):
  values={}
  for label,probe in [('body',old['LeafButton_'+kind+'_'+side]),('leaf',service[f'ButtonLeafServiceReserve_{kind}_{side}']),('wire',service[f'ButtonWireServiceReserve_{kind}_{side}']),('tool',service[f'ButtonToolServiceReserve_{kind}_{side}'])]:
   before=old['PF_BasePlywood'].distToShape(probe)[0];after=scene['PF_BasePlywood'].distToShape(probe)[0];penetration=old['PF_BasePlywood'].common(probe).Volume
   values[label]={'before_mm':before,'after_mm':after,'before_overlap_mm3':penetration,'after_overlap_mm3':scene['PF_BasePlywood'].common(probe).Volume}
   check(f'{side} {kind} {label} service clears notched base',values[label]['after_overlap_mm3']<.01 and after>0.1)
  clearance.append({'side':side,'button':kind,'clearance':values})
check('wire allowances retain at least 2 mm board clearance',all(row['clearance']['wire']['after_mm']>=N['service_clearance_mm']-1e-5 for row in clearance))
# VESA is the actual modeled attachment/load region. Display outline overhang is preserved, not invented as a new wood mounting footprint.
notch_near={name:min(removedL.distToShape(s)[0],removedR.distToShape(s)[0]) for name,s in old.items() if name.startswith(('CROSS_','PF_CommercialStrap','PF_StrapScrew')) or name in ('PF_VESAEnvelope','PF_WoodDowel','PLAYFIELD_ENVELOPE')}
check('notches away from straps VESA and all crossmembers',min(d for n,d in notch_near.items() if n!='PLAYFIELD_ENVELOPE')>10)
check('TV and VESA clear unchanged notched board',not conflicts({'PF_BasePlywood':scene['PF_BasePlywood']},{n:old[n] for n in ('PLAYFIELD_ENVELOPE','PF_VESAEnvelope')}))
check('both button tool routes clear TV and non-target cabinet',not conflicts({n:s for n,s in service.items() if 'Tool' in n},{n:s for n,s in old.items() if not n.startswith('Leaf') and n not in ('PF_BasePlywood','CandidateGlass') and not any(t in n for t in ('Reserve','RESERVED','CandidatePayload'))}))
# Retire only the old intake cuts and their eight obsolete filter mounting holes.
def rounded(x,y,z,w,h,t,r):
 s=box(x+r,y,z,w-2*r,h,t).fuse(box(x,y+r,z,w,h-2*r,t))
 for xx in (x+r,x+w-r):
  for yy in (y+r,y+h-r):s=s.fuse(cyl(xx,yy,z,r,t))
 return s.removeSplitter()
floor=old['FLOOR'].copy();ft=floor.BoundBox.ZMax;fb=floor.BoundBox.ZMin;thick=ft-fb
for x,y,w,h in oldfloorc['intakes_xywh_mm']:floor=floor.fuse(rounded(x,y,fb,w,h,thick,oldfloorc['trial_corner_radius_mm']))
for x,y in oldfloorc['filter_fixing_centers_xy_mm']:floor=floor.fuse(cyl(x,y,fb,oldfloorc['filter_fixing_hole_diameter_mm']/2,thick))
floor=floor.removeSplitter();fan_size=shared['fan_size_mm'][0];pitch=shared['fan_pitch_mm'];airr=shared['fan_opening_diameter_mm']/2;hole=F['mount_hole_diameter_mm_candidate'];assert shared['fan_size_mm']==[120,120,25]
newparts={};fan_rows=[];fanholes=[];filterholes=[];fan_allow={};fixture={}
# Reuse the exact existing rear fan family solid, rotated to the floor. No second fan design.
for i,(x,y,w,h) in enumerate(oldfloorc['intakes_xywh_mm']):
 side='L' if i==0 else 'R';cx=x+w/2;cy=y+h/2
 fan=old['FAN_230'].copy();fan.rotate(V(),V(1,0,0),90);bb=fan.BoundBox;fan.translate(V(cx-bb.Center.x,cy-bb.Center.y,ft-bb.ZMin))
 envelope=box(cx-60,cy-60,ft,120,120,25)
 floor=floor.cut(cyl(cx,cy,fb-1,airr,thick+2));fan_mount=[]
 frame=box(cx-F['filter_size_mm']/2,cy-F['filter_size_mm']/2,fb-F['filter_thickness_mm'],F['filter_size_mm'],F['filter_size_mm'],F['filter_thickness_mm']).cut(cyl(cx,cy,fb-F['filter_thickness_mm']-1,airr,F['filter_thickness_mm']+2))
 for j,(dx,dy) in enumerate([(dx,dy) for dx in (-pitch/2,pitch/2) for dy in (-pitch/2,pitch/2)],1):
  hx,hy=cx+dx,cy+dy;fanholes.append((hx,hy,hole/2));fan_mount.append([hx,hy]);floor=floor.cut(cyl(hx,hy,fb-1,hole/2,thick+2))
  # Four plain pass holes let the filter slide past stationary fan nuts/bolt ends.
  frame=frame.cut(cyl(hx,hy,fb-F['filter_thickness_mm']-1,6,F['filter_thickness_mm']+2))
  bolt_top=ft+25+1.5;tip=bolt_top-F['floor_bolt_length_mm_candidate'];newparts[f'FloorFanBolt{side}{j}']=cyl(hx,hy,tip,2,F['floor_bolt_length_mm_candidate']).fuse(cyl(hx,hy,bolt_top,4,3)).removeSplitter()
  newparts[f'FloorFanNut{side}{j}']=cyl(hx,hy,fb-3.2,4,3.2).cut(cyl(hx,hy,fb-4,2,5)).removeSplitter()
 for j,(dx,dy) in enumerate([(dx,dy) for dx in (-F['filter_mount_pitch_mm']/2,F['filter_mount_pitch_mm']/2) for dy in (-F['filter_mount_pitch_mm']/2,F['filter_mount_pitch_mm']/2)],1):
  hx,hy=cx+dx,cy+dy;filterholes.append((hx,hy,F['filter_insert_diameter_mm_candidate']/2));floor=floor.cut(cyl(hx,hy,fb,F['filter_insert_diameter_mm_candidate']/2,F['filter_insert_depth_mm_candidate']))
  frame=frame.cut(cyl(hx,hy,fb-F['filter_thickness_mm']-1,hole/2,F['filter_thickness_mm']+2))
  newparts[f'FloorFilterInsert{side}{j}']=cyl(hx,hy,fb,3,8).cut(cyl(hx,hy,fb-1,2,10)).removeSplitter()
  newparts[f'FloorFilterScrew{side}{j}']=cyl(hx,hy,fb-F['filter_thickness_mm'],2,16).fuse(cyl(hx,hy,fb-F['filter_thickness_mm']-3,4,3)).removeSplitter()
 # Guard/media are packaging allowances only, not proprietary production guard geometry.
 mediaz=fb-F['filter_thickness_mm']-F['filter_media_thickness_mm_allowance'];guardz=mediaz-F['commercial_guard_thickness_mm_allowance']
 newparts['FloorIntakeFan'+side]=fan;newparts['RemovableIntakeFilter'+side]=frame.removeSplitter()
 newparts['FloorFilterMediaReserve'+side]=box(cx-60,cy-60,mediaz,120,120,F['filter_media_thickness_mm_allowance'])
 guard=box(cx-60,cy-60,guardz,120,120,F['commercial_guard_thickness_mm_allowance']);guard.rotate(V(cx,cy,guardz),V(0,0,1),F['lower_guard_mount_rotation_deg_design']);newparts['FloorCommercialGuardReserve'+side]=guard
 # Upper guard allowance is open-ring packaging; guard purchase determines its mesh/net free area.
 newparts['FloorUpperGuardReserve'+side]=box(cx-60,cy-60,ft+25,120,120,1.5).cut(cyl(cx,cy,ft+24,airr,4))
 connector=box(cx-15,cy+60,ft+4,*F['connector_service_xyz_mm']);newparts['FloorFanConnectorReserve'+side]=connector
 fan_allow[side]=envelope;fixture[side]={'frame':frame,'fan':fan,'envelope':envelope,'connector':connector}
 fan_rows.append({'side':side,'center_xyz_mm':[cx,cy,ft+12.5],'mount_plane_z_mm':ft,'old_center_xy_mm':[cx,cy],'displacement_xyz_mm':[0,0,0],'fan_mount_holes_xy_mm':fan_mount,'filter_frame_bounds_xyz_mm':[cx-85,cy-85,fb-8,cx+85,cy+85,fb],'guard_lower_z_mm':guardz})
scene['FLOOR']=floor.removeSplitter();retired=['CandidateIntakeFilterFrame1','CandidateIntakeFilterFrame2']
for n in retired:scene.pop(n)
scene.update(newparts)
reserves={n for n in scene if any(t in n for t in ('Reserve','RESERVED','CandidatePayload'))}
real={n:s for n,s in scene.items() if n not in reserves and n!='PF_BackboxCheckEnvelope'}
check('floor remains valid single 18 mm CNC solid',scene['FLOOR'].isValid() and len(scene['FLOOR'].Solids)==1 and abs(scene['FLOOR'].BoundBox.ZLength-18)<1e-6)
check('all new installed parts valid single solids',all(s.isValid() and len(s.Solids)==1 for n,s in newparts.items()))
fan_conf=conflicts({n:s for n,s in newparts.items() if n not in reserves},real)
check('new fans filters and basic fasteners clear installed geometry',not fan_conf)
for row in fan_rows:
 side=row['side'];cx,cy,cz=row['center_xyz_mm'];fix=fixture[side]
 check(side+' 120 fan envelope clear actual equipment',not conflicts({'fan_envelope':fix['envelope']},{n:s for n,s in real.items() if not n.startswith(('FloorFan','FloorIntakeFan','FloorUpperGuard'))}))
 check(side+' all four fan bores pass floor and existing fan',all(scene['FLOOR'].common(cyl(x,y,fb, hole/2-.05,thick)).Volume<1e-4 and newparts['FloorIntakeFan'+side].common(cyl(x,y,ft,hole/2-.05,25)).Volume<1e-4 for x,y in row['fan_mount_holes_xy_mm']))
 check(side+' unobstructed 116 floor airflow aperture',scene['FLOOR'].common(cyl(cx,cy,fb,airr-.01,thick)).Volume<1e-4)
 check(side+' blind filter inserts leave 10 mm floor skin',thick-F['filter_insert_depth_mm_candidate']>=10)
 # A downward prism of the full frame with passage holes proves continuous withdrawal past fan nuts.
 # Every planar section extruded along -Z is the same frame profile.
 framepath=box(cx-85,cy-85,fb-8-F['filter_removal_mm'],170,170,8+F['filter_removal_mm']).cut(cyl(cx,cy,fb-9-F['filter_removal_mm'],airr,10+F['filter_removal_mm']))
 for x,y in row['fan_mount_holes_xy_mm']:framepath=framepath.cut(cyl(x,y,fb-9-F['filter_removal_mm'],6,10+F['filter_removal_mm']))
 for dx in (-70,70):
  for dy in (-70,70):framepath=framepath.cut(cyl(cx+dx,cy+dy,fb-9-F['filter_removal_mm'],hole/2,10+F['filter_removal_mm']))
 removalobs={n:s for n,s in real.items() if n not in ('RemovableIntakeFilter'+side,'FLOOR') and not n.startswith('FloorFilterScrew'+side)}
 fh=conflicts({'filter_removal':framepath},removalobs);check(side+' filter continuously removes 80 mm downward without fan removal',not fh)
 fanpath=box(cx-60,cy-60,ft,120,120,25+F['fan_removal_mm'])
 fanobs={n:s for n,s in real.items() if n!='FloorIntakeFan'+side and not n.startswith(('FloorFanBolt'+side,'FloorFanNut'+side))}
 check(side+' fan 80 mm vertical withdrawal clear after fastener removal',not conflicts({'fan_removal':fanpath},fanobs))
 check(side+' connector and cable service reserve clear',not conflicts({'connector':fix['connector']},{n:s for n,s in real.items() if n!='FloorIntakeFan'+side}))
 check(side+' filter removal obstructed negative control detected',bool(conflicts({'removal':framepath},{'injected_block':box(cx+65,cy,fb-40,10,10,10)})))
 # Synthetic 140 fan is rejected by 120 station mounting registration, not falsely by an absent cabinet collision.
 check(side+' oversized 140 fan mounting negative control rejected',any(scene['FLOOR'].isInside(V(cx+dx,cy+dy,(fb+ft)/2),1e-6,True) for dx in (-pitch*140/120/2,pitch*140/120/2) for dy in (-pitch*140/120/2,pitch*140/120/2)))
 bad=shifted(fix['envelope'],[300-cx,440-cy,0]);check(side+' fan shifted into subwoofer negative control rejected',bool(conflicts({'shifted_fan':bad},{'subwoofer':old['SSF_Subwoofer_DCS165_Reference']})))
check('new bottom hardware stays above existing cabinet underside datum',min(s.BoundBox.ZMin for n,s in newparts.items() if not n.startswith('FloorFanConnector'))>=old['FLOOR_CLEAT_18'].BoundBox.ZMin)
# Distance between cuts measured in XY; all original unrelated floor bores are retained.
openings=[(row['center_xyz_mm'][0],row['center_xyz_mm'][1],airr) for row in fan_rows]
sub=audio['subwoofer'];sx,sy=sub['center_xy_mm'];sr=sub['design_cutout_mm']/2
xygap=lambda a,b:math.hypot(a[0]-b[0],a[1]-b[1])-a[2]-b[2]
perimeter=min(min(x-r-18,582-x-r,y-r-18,1290.1-y-r) for x,y,r in openings+fanholes+filterholes)
other=[]
for e in old['FLOOR'].Edges:
 if isinstance(e.Curve,Part.Circle) and abs(e.Curve.Center.z-ft)<1e-5:
  v=(e.Curve.Center.x,e.Curve.Center.y,e.Curve.Radius)
  if abs(v[2]-2.75)<1e-5 or abs(v[2]-sr)<1e-5:other.append(v)
ligaments={'between_intake_openings_mm':xygap(*openings),'to_subwoofer_opening_mm':min(xygap(v,(sx,sy,sr)) for v in openings+fanholes+filterholes),'to_BST_anchors_mm':min(xygap(v,(x,y,audio['bass_shaker']['anchor_diameter_mm']/2)) for v in openings+fanholes+filterholes for x,y in audio['bass_shaker']['floor_anchor_holes_xy_mm']),'to_PCBase_anchors_mm':min(xygap(v,(x,y,audio['pc_base']['through_diameter_mm']/2)) for v in openings+fanholes+filterholes for x,y in audio['pc_base']['anchor_holes_xy_mm']),'to_floor_perimeter_mm':perimeter,'airflow_to_fan_bore_mm':math.hypot(pitch/2,pitch/2)-airr-hole/2,'filter_frame_airflow_to_fan_passage_mm':math.hypot(pitch/2,pitch/2)-airr-6,'to_all_unrelated_existing_through_cuts_mm':min(xygap(v,q) for v in openings+fanholes+filterholes for q in other)}
check('floor cut ligaments exceed 10 mm',min(v for n,v in ligaments.items() if not n.startswith('filter_frame'))>=10)
check('filter frame ligaments exceed 10 mm',ligaments['filter_frame_airflow_to_fan_passage_mm']>=10)
check('original subwoofer BST PC floor holes preserved',all(scene['FLOOR'].common(cyl(x,y,fb,r-.01,thick)).Volume<1e-4 for x,y,r in other))
# Project exact installed obstacles onto the aperture plane, once immediate and once up to the next shelf.
thermal=[]
for row in fan_rows:
 side=row['side'];cx,cy,_=row['center_xyz_mm'];ap=Part.Face(Part.Wire(Part.makeCircle(airr,V(cx,cy,ft+25))))
 def projected_fraction(z0,z1):
  disks=[]
  for n,s in old.items():
   if n in reserves or n in ('CandidateGlass','PF_BackboxCheckEnvelope') or s.BoundBox.ZMax<=z0 or s.BoundBox.ZMin>=z1:continue
   # Conservative projected bounding rectangle; separately report its method.
   bb=s.BoundBox;patch=box(bb.XMin,bb.YMin,ft+25-.5,bb.XLength,bb.YLength,1).common(cyl(cx,cy,ft+25-.5,airr,1))
   if patch.Volume>.01:disks.append(patch)
  if not disks:return 0,[]
  u=disks[0]
  for p in disks[1:]:u=u.fuse(p)
  return u.Volume/(math.pi*airr**2)*100,[n for n,s in old.items() if n not in reserves and s.BoundBox.ZMin<z1 and s.BoundBox.ZMax>z0 and s.BoundBox.XMin<cx+airr and s.BoundBox.XMax>cx-airr and s.BoundBox.YMin<cy+airr and s.BoundBox.YMax>cy-airr]
 immediate,imobs=projected_fraction(ft+25,ft+25+F['immediate_above_height_mm']);shelf,shobs=projected_fraction(ft+25,192.1)
 distances={n:fixture[side]['envelope'].distToShape(old[n])[0] for n in ('SSF_Subwoofer_DCS165_Reference','SSF_BST_Carrier','SSF_BST1_Reference','PC_BASE','SHELF_1','SHELF_2','SHELF_3')}
 lane=100 if side=='L' else 500;ex=230 if side=='L' else 370
 route=[[cx,cy,86],[lane,800,120],[lane,1045,180],[lane,1150,520],[ex,1250,500]];paths=[]
 for a0,b0 in zip(route,route[1:]):v=V(*b0)-V(*a0);paths.append(Part.makeCylinder(8,v.Length,V(*a0),v.normalize()))
 pathhits=conflicts({str(i):s for i,s in enumerate(paths)},real)
 check(side+' modeled exhaust approach corridor clear',not pathhits)
 check(side+' immediate 25 mm discharge column unobstructed',immediate<.01)
 direct=V(ex,1250,500)-V(cx,cy,86);directpath=Part.makeCylinder(8,direct.Length,V(cx,cy,86),direct.normalize());short=conflicts({'direct':directpath},{n:old[n] for n in ('PC_ENVELOPE','SHELF_3')})
 thermal.append({'side':side,'immediate_above_25mm_obstruction_percent':immediate,'projected_obstruction_to_shelf_top_percent':shelf,'overhead_obstacles':shobs,'nearest_equipment_clearances_mm':distances,'airflow_approach_route_xyz_mm':route,'route_radius_mm':8,'route_conflicts':pathhits,'direct_shortcut_intersects_PC_or_shelf':bool(short)})
# All unchanged systems compared with the accepted source, not regenerated.
changed={'PF_BasePlywood','FLOOR'}|set(retired)
check('all unrelated cabinet solids exactly preserved',all(n in scene and diff(s,scene[n])<1e-5 for n,s in old.items() if n not in changed))
check('rear fan family and guards unchanged',all(diff(old[n],scene[n])<1e-5 for n in old if n.startswith(('FAN_','CandidateFan'))))
check('wooden pivot straps screws and both supports unchanged',all(diff(old[n],scene[n])<1e-5 for n in old if n.startswith('PF_') and n!='PF_BasePlywood'))
# Opening/lift sweeps include newly fixed fan parts and leave approved pivots stationary.
moving=[n for n in old if n.startswith('PF_') and n not in ('PF_OpenCradleL','PF_OpenCradleR','PF_BackboxCheckEnvelope') and not n.startswith('PF_SupportMountScrew')]+['PLAYFIELD_ENVELOPE'];pivot=V(*review['pivot_xyz_mm'])
fixed={n:s for n,s in real.items() if n not in moving and n!='CandidateGlass'};sweep=[];lift=[]
for ang in range(0,int(review['opening_deg'])+1,2):
 parts={n:scene[n].copy() for n in moving}
 for s in parts.values():s.rotate(pivot,V(1,0,0),-ang)
 sweep.extend(conflicts(parts,fixed))
for dz in range(0,int(review['lift_out_mm'])+1,2):lift.extend(conflicts({n:shifted(scene[n],[0,0,dz]) for n in moving},fixed))
check('PLAY to SERVICE movement unchanged and collision free',not sweep);check('vertical lift out unchanged and collision free',not lift)
# S1/S2/S3 retain their upward service corridors; fans top61 are below shelf starts160/180/240.
check('shelf upward service paths do not meet fans',all(not conflicts({'shelf_sweep':box(s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin,s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength+80)},fan_allow) for n,s in old.items() if n in ('SHELF_1','SHELF_2','SHELF_3')))
print('FAN_CONFLICTS',fan_conf,flush=True);print('CLEARANCES',clearance,flush=True);print('LIGAMENTS',ligaments,flush=True)
(O/'diagnostic.json').write_text(json.dumps({'checks':checks,'fan_conflicts':fan_conf,'button_clearance':clearance,'thermal':thermal},indent=2)+'\n');assert all(v['pass'] for v in checks),[v for v in checks if not v['pass']]
# Mutate only owned geometry in each accepted saved pose; no pivot reimplementation.
poses={};saved={}
for state in ('PLAY','SERVICE','LIFT-OUT','EXPLODED'):
 inp=A.openDocument(str(src/(state.lower()+'.FCStd')));pose={o.Name:o.Shape.copy() for o in inp.Objects if hasattr(o,'Shape')}
 newbase=scene['PF_BasePlywood'].copy()
 if state=='SERVICE':newbase.rotate(pivot,V(1,0,0),-review['opening_deg'])
 if state=='LIFT-OUT':newbase.translate(V(0,0,review['lift_out_mm']))
 if state=='EXPLODED':newbase.translate(V(0,0,160))
 pose['PF_BasePlywood']=newbase
 if state!='EXPLODED':
  pose['FLOOR']=scene['FLOOR']
  for n in retired:pose.pop(n,None)
  pose.update(newparts);pose.update(service)
 poses[state]=pose
 out=inp;out.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; manufacturing BLOCKED'
 sheet=out.addObject('Spreadsheet::Sheet','ReviewParameters')
 for cell,key,value in [('A1','NotchRadius',r),('A2','NotchDepth',depth),('A3','FanPitch',pitch),('A4','FanOpeningDiameter',2*airr)]:sheet.set(cell,str(value));sheet.setAlias(cell,key)
 for n in retired:
  if out.getObject(n):out.removeObject(n)
 for n,s in pose.items():
  o=out.getObject(n)
  if o is None:o=out.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','PartID');o.PartID=n
  elif n in ('PF_BasePlywood','FLOOR'):o.Shape=s
 out.recompute();path=O/(state.lower()+'.FCStd');out.saveAs(str(path));A.closeDocument(out.Name);out=A.openDocument(str(path));out.recompute();check(state+' saved CAD valid identical single solids',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and diff(o.Shape,pose[o.Name])<1e-4 for o in out.Objects if hasattr(o,'Shape')))
 check(state+' existing dowel cylinder and live diameter expression preserved',out.getObject('PF_WoodDowel').TypeId=='Part::Cylinder' and bool(out.getObject('PF_WoodDowel').ExpressionEngine))
 if state=='PLAY':Part.export([o for o in out.Objects if hasattr(o,'Shape') and o.Name not in reserves and o.Name not in service and o.Name!='PF_BackboxCheckEnvelope'],str(O/'current-v32.step'))
 A.closeDocument(out.Name);saved[state]=str(path.relative_to(R))
step=O/'current-v32.step';step.write_text('\n'.join(line.rstrip() for line in step.read_text().splitlines())+'\n')
review['notch']={'local_left_bounds_xyz_mm':[x0,y0,b.ZMin,x1,y1,b.ZMax],'local_right_bounds_xyz_mm':[600-x1,y0,b.ZMin,600-x0,y1,b.ZMax],'local_frame':'X global; Y/Z inverse existing playfield transform','depth_mm':depth,'longitudinal_extent_mm':y1-y0,'corner_radius_mm':r,'provisional_cutter_diameter_mm':N['trial_cutter_diameter_mm'],'dogbones':False,'minimum_remaining_section_width_mm':b.XLength-2*depth,'minimum_remaining_section_area_mm2':(b.XLength-2*depth)*b.ZLength,'clearances':clearance,'nearest_crossmember_mm':min(d for n,d in notch_near.items() if n.startswith('CROSS_')),'nearest_VESA_mm':notch_near['PF_VESAEnvelope'],'nearest_TV_envelope_mm':notch_near['PLAYFIELD_ENVELOPE'],'nearest_strap_mm':min(d for n,d in notch_near.items() if n.startswith('PF_CommercialStrap')),'TV_support_basis':'Existing VESA attachment is unchanged. TV outline overhang over a clearance notch is not a new mounting/load area. Full display envelope is untouched.','buttons_moved':False}
review['floor_fans']={'shared_family':{k:shared[k] for k in ('fan_size_mm','fan_pitch_mm','fan_opening_diameter_mm')},'stations':fan_rows,'ligaments':ligaments,'fan_removal_mm':F['fan_removal_mm'],'filter_removal_mm':F['filter_removal_mm'],'filter_frame_xyz_mm':[170,170,8],'filter_media_guard_hardware_status':'ALLOWANCES / common candidate hardware; purchase data pending','lower_guard_fixing':F['lower_guard_fixing'],'lower_guard_mount_rotation_deg_design':F['lower_guard_mount_rotation_deg_design'],'thermal':thermal,'gross_intake_area_mm2':2*math.pi*airr**2,'gross_exhaust_area_mm2':2*math.pi*airr**2,'obvious_overhead_obstruction':any(t['projected_obstruction_to_shelf_top_percent']>0 for t in thermal),'obvious_direct_short_circuit':False,'thermal_adequacy_certified':False,'later_analytical_gate_required':True,'thermal_gate':F['thermal_gate'],'ground_note':'All added parts remain above existing Z0 cabinet underside. 80 mm underside removal corridor is clear in modeled cabinet; final imported legs/room ground clearance still a manufacturing gate.'}
labels={'FloorIntakeFanL':'FLOOR INTAKE FAN L','FloorIntakeFanR':'FLOOR INTAKE FAN R','RemovableIntakeFilterL':'REMOVABLE INTAKE FILTER L','RemovableIntakeFilterR':'REMOVABLE INTAKE FILTER R'}
for name in service:
 labels[name]='WIRE SERVICE CLEARANCE' if 'Wire' in name else 'BUTTON TOOL ACCESS' if 'Tool' in name else 'BUTTON BODY CLEARANCE' if 'Body' in name else 'LEAF SWITCH CLEARANCE'
def mesh(n,s):vs,fs=s.tessellate(.7);return {'name':n,'vertices':[[v.x,v.y,v.z] for v in vs],'faces':[list(f) for f in fs],**({'label':labels[n]} if n in labels else {})}
scene.update(service);bundle={'parts':[mesh(n,s) for n,s in scene.items()],'states':{},'review':review}
for state,pose in poses.items():bundle['states'][state]={n:mesh(n,pose[n]) if n in pose else None for n in scene if n not in pose or diff(scene[n],pose[n])>1e-5}
mp=O/'mesh.json';mp.write_text(json.dumps(bundle,separators=(',',':'))+'\n');baseline={'parts':[mesh(n,old[n]) for n in ('PF_BasePlywood','FLOOR')],'head':c['source_head']};(O/'before.json').write_text(json.dumps(baseline,separators=(',',':'))+'\n')
check('accepted source files remain byte unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in source_hashes.items()))
(O/'validation.json').write_text(json.dumps({'checks':checks,'review':review,'saved_poses':saved,'source_head':c['source_head'],'source_sha256':hashlib.sha256((src/'play.FCStd').read_bytes()).hexdigest(),'mesh_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'manufacturing_ready':False},indent=2)+'\n')
for n in ('LICENSE','NOTICE.md'):shutil.copyfile(R/n,O/n)
assert all(v['pass'] for v in checks);print('NOTCH_FANS_PASS',len(checks),flush=True)

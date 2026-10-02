# SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION
# Historical baseline/replay only. See studies/wpc-fold-v32/README.md; use original source HEAD for exact replay.
"""Backbox side-profile feasibility study; no accepted component edits. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib, json, math, subprocess, shutil, sys
import FreeCAD as A
import Part
R=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(R/'tools')); V=A.Vector
c=json.loads((R/'config/backbox_profile_v32.json').read_text()); O=R/c['output_directory']; O.mkdir(parents=True,exist_ok=True)
checks=[]
def check(n,v):
    assert v,n
    checks.append({'check':n,'pass':True})
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
def read(p):
    d=A.openDocument(str(R/p));d.recompute();s={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')};A.closeDocument(d.Name);return s
def bounds(s):
    b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
def mesh(n,s):
    vv,ff=s.tessellate(.7);return {'name':n,'vertices':[[p.x,p.y,p.z] for p in vv],'faces':[list(f) for f in ff]}
def hits(a,b):
    out=[]
    for n,s in a.items():
        for m,t in b.items():
            if s.BoundBox.intersect(t.BoundBox):
                v=s.common(t).Volume
                if v>1e-6:out.append({'part':n,'obstacle':m,'volume_mm3':v})
    return out
def plane_face(s,z):return Part.makeCompound([f for f in s.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.99])
def yz_prism(x,width,points):
    ps=[V(x,y,z) for y,z in points];return Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(V(width,0,0))
def union(ss):
    ss=list(ss);return ss[0].multiFuse(ss[1:]).removeSplitter() if len(ss)>1 else ss[0]
def centroid(s):
    solids=s.Solids;v=sum(p.Volume for p in solids)
    return V(*[sum(p.Volume*getattr(p.CenterOfMass,a) for p in solids)/v for a in 'xyz'])
source=read('exports/generated/matrix-route-backbox-audit-v32/backbox-source-audit.FCStd')
play=read('exports/generated/matrix-cassette-v32/play.FCStd')
removed=read('exports/generated/matrix-cassette-v32/matrix-removed.FCStd')
current=read('exports/generated/backbox-floor-v32/corrected-upright.FCStd')
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',c['source_head']],cwd=R,text=True).splitlines()
protected=[p for p in tracked if p.startswith(('config/','tools/','cad/','exports/')) and (R/p).is_file()]
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protected}
hinge=json.loads((R/'config/backbox_fold_v10.json').read_text()); owner=json.loads((R/'config/owner_services_v27.json').read_text())['backbox']
axis=V(*c['pivot_xyz_mm']); rear=c['rear_y_mm']; z0=c['bottom_z_mm']; h=c['height_mm'];t=c['stock_mm'];zt=z0+h
check('fixed references match accepted WPC and cabinet',list(axis)==[300,1270,508] and hinge['backbox']['hinge_floor_bolt_inset_each_side_mm']==59.8375 and rear==1308.1 and z0==596.9)
shelf=play['BACKBOX_BASE'];channels={n:play[n] for n in ('CandidateGlassChannelL','CandidateGlassChannelR')}
physical={n:s for n,s in play.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n.upper() for k in ('ENVELOPE','RESERVE','RESERVED','CANDIDATEPAYLOAD'))}
stationary={n:s for n,s in removed.items() if n.startswith('MX_')}
display=box(*owner['display_box_mm']);dmd=box(*owner['dmd_box_mm']);speakers=union(box(*b) for b in owner['speaker_boxes_mm'])
from owner_features_v27 import features
from build_owner_services_v27 import cut_shape
passages={f['key']:cut_shape(f) for f in features() if f['part']=='BackboxFloorV14'}
from build_structure_v14 import main as build_legacy
doc=A.newDocument('RawBackboxOnly');build_legacy(doc)
raw={o.Name:o.Shape.copy() for o in doc.Objects if hasattr(o,'Shape') and o.Name.startswith(('BackboxFloor','BackboxLeftSide','BackboxRightSide','BackboxTop','BackboxRearFrame'))};A.closeDocument(doc.Name)

def candidate(depth):
    front=rear-depth;k=(c['top_depth_mm']-depth)/h
    def fy(z):return front-k*(z-z0)
    shape=yz_prism(-90,780,[(front,z0),(rear,z0),(rear,zt),(rear-254,zt)])
    wood={n:s.copy() for n,s in raw.items()}
    for n in ('BackboxLeftSideV14','BackboxRightSideV14'):wood[n]=wood[n].common(shape).removeSplitter()
    wood['BackboxFloorV14']=box(-90,front,z0,780,depth,t)
    # Square-cut horizontal top front follows the side profile at its underside.
    wood['BackboxTopV14']=box(-90,fy(zt-t),zt-t,780,rear-fy(zt-t),t)
    def cut(n,s):wood[n]=wood[n].cut(s).removeSplitter()
    for n in ('BackboxFloorV14','BackboxTopV14'):
        b=wood[n].BoundBox
        cut(n,box(b.XMin-1,b.YMin-1,b.ZMin-1,t-6+1,b.YLength+2,b.ZLength+2))
        cut(n,box(b.XMax-(t-6),b.YMin-1,b.ZMin-1,t-6+1,b.YLength+2,b.ZLength+2))
        for side in ('Left','Right'):cut('Backbox'+side+'SideV14',wood[n])
    for n in [n for n in wood if n.startswith('BackboxRearFrame')]:
        for m in ('BackboxFloorV14','BackboxTopV14','BackboxLeftSideV14','BackboxRightSideV14'):
            ov=wood[n].common(wood[m])
            if ov.Volume<1e-6:continue
            b=ov.BoundBox;limit=b.YMax-6
            cut(n,box(b.XMin-1,b.YMin-1,b.ZMin-1,b.XLength+2,max(.001,limit-b.YMin+1),b.ZLength+2))
            cut(m,wood[n])
    for f in features():
        if f['part'] in wood:cut(f['part'],cut_shape(f))
    check(f'{depth}: eight single valid wood solids',len(wood)==8 and all(s.isValid() and len(s.Solids)==1 for s in wood.values()))
    internal=[r for r in hits(wood,wood) if r['part']<r['obstacle']]
    check(f'{depth}: internal joints valid',not internal)
    floor=wood['BackboxFloorV14'];bottom=plane_face(floor,z0);contact=bottom.common(plane_face(shelf,z0))
    holes=[w for w in bottom.Faces[0].Wires if not w.isSame(bottom.Faces[0].OuterWire)]
    outer=bottom.Faces[0].OuterWire;ligament=min([w.distToShape(outer)[0] for w in holes]+[holes[0].distToShape(holes[1])[0]])
    clearance=min(floor.distToShape(s)[0] for s in channels.values());zero_hits=hits(wood,physical)
    # Joint dimensions refer to the actual horizontal contact with each side's 6 mm capture.
    jointlen=floor.BoundBox.YLength;end=c['fastener_planning']['end_margin_mm'];pitch=c['fastener_planning']['minimum_pitch_mm']
    geometric_count=math.floor((jointlen-2*end)/pitch)+1
    # Do not offer screw locations inside unmeasured hinge mounting reserves.
    last=min(floor.BoundBox.YMax-end,1197-20)
    count=max(0,math.floor((last-(front+end))/pitch)+1)
    ys=[front+end+i*pitch for i in range(count)]
    positions={side:[[x,y,z0+t/2] for y in ys] for side,x in [('L',-81),('R',681)]}
    # Generic side-area mapping, conservative YZ projections of source display/payloads.
    margin=c['zone_planning']['edge_margin_mm'];za=z0+t+margin;zb=zt-t-margin;yr=rear-t-margin
    inset=margin*math.sqrt(1+k*k)
    safe=yz_prism(-72,1,[(fy(za)+inset,za),(yr,za),(yr,zb),(fy(zb)+inset,zb)])
    def proj(s,pad=0):
        b=s.BoundBox;return box(-72,b.YMin-pad,b.ZMin-pad,1,b.YLength+2*pad,b.ZLength+2*pad)
    masks={'DisplayStructureReserve':proj(display,10), 'SpeakerDMDReserve':union([proj(speakers,10),proj(dmd,10)]),
           'HarnessCorridor':box(-72,rear-t-40,za,1,40,zb-za),
           'HingeKeepout':box(-72,1215,483,1,110,170),
           'ServiceToolKeepout':box(-72,front,z0,1,depth,78),
           'DisplayRailsReserve':box(-72,1235,760,1,40,500)}
    toy=safe.cut(union(masks.values())).removeSplitter()
    zones={n:s.common(safe) for n,s in masks.items()};zones['AvailableToyAreaL']=toy
    right=toy.copy();right.translate(V(743,0,0));zones['AvailableToyAreaR']=right
    rearboard=box(180,1240,850,240,32,300);zones['RemovableRearBoardServiceReserve']=rearboard
    lower=box(220,1220,675,160,50,75);zones['LowerServiceToyReserve']=lower
    board_hits=hits({'RearBoard':rearboard},{**wood,'Display':display,'DMD':dmd,'Speakers':speakers})
    lower_hits=hits({'LowerService':lower},{**wood,'Display':display,'DMD':dmd,'Speakers':speakers})
    check(f'{depth}: proposed generic zones do not collide with modeled structure/payload',not board_hits and not lower_hits)
    # Side reserve depth is extruded only into the cabinet, not through permanent wood.
    toy_payload=toy.copy();toy_payload=union([f.extrude(V(40,0,0)) for f in toy.Faces if abs(f.CenterOfMass.x+72)<1e-6])
    check(f'{depth}: side toy depth clears modeled payload',not hits({'ToyL':toy_payload},{'Display':display,'DMD':dmd,'Speakers':speakers}))
    # Mass inventory is an explicit planning budget; it adds no geometry or BOM items.
    ma=c['mass_assumptions'];rho=ma['plywood_density_kg_m3']/1e9
    masses=[{'item':n,'kg':s.Volume*rho,'cg_xyz_mm':list(centroid(s)),'basis':'CAD volume × assumed 650 kg/m³'} for n,s in wood.items()]
    door_mass=520*460*15*rho
    def mass(n,m,p,basis='ASSUMPTION / optional allowance'):masses.append({'item':n,'kg':m,'cg_xyz_mm':list(p),'basis':basis})
    mass('Removable rear door allowance',door_mass,[300,1300.6,880],'V14 520×460×15 nominal panel × assumed density; not added to accepted CAD')
    for n,key,p in [('Backglass','backglass_kg',display.CenterOfMass),('DMD','dmd_kg',dmd.CenterOfMass),('Speakers','speakers_total_kg',centroid(speakers)),('Monitor mount','monitor_mount_kg',[300,1210,1000]),('Wiring','wiring_kg',[300,1255,980]),('Electronics','electronics_kg',rearboard.CenterOfMass),('Future backbox fans','future_backbox_fans_kg',[300,1250,1240]),('Front wood allowance','additional_front_wood_kg',[300,fy(960)+15,960])]:mass(n,ma[key],p)
    p=centroid(toy);mass('Future left toys',ma['future_toys_kg']/2,[-52,p.y,p.z]);mass('Future right toys',ma['future_toys_kg']/2,[652,p.y,p.z])
    mass('Accepted stationary matrix cassette',0,[300,1080,570],'Excluded from moving assembly; independent cabinet cassette removed before fold')
    mass('Accepted cabinet intake/exhaust fans',0,[300,0,0],'All four remain stationary cabinet components')
    total=sum(x['kg'] for x in masses);cg=V(*[sum(x['kg']*x['cg_xyz_mm'][i] for x in masses)/total for i in range(3)]);rel=cg-axis;weight=total*9.80665
    loadcases=[];grip=V(300,rear-254,zt);griprel=grip-axis
    for angle in range(91):
        a=math.radians(angle);ry=rel.y*math.cos(a)-rel.z*math.sin(a);rz=rel.y*math.sin(a)+rel.z*math.cos(a)
        gy=griprel.y*math.cos(a)-griprel.z*math.sin(a);hand=weight*ry/gy
        loadcases.append({'angle_deg':angle,'cg_xyz_mm':[cg.x,axis.y+ry,axis.z+rz],'gravity_moment_Nm':-weight*ry/1000,'upward_grip_force_N':hand,'reaction_each_hinge_N':(weight-hand)/2,'scope':'FREE-SPACE LOAD EQUILIBRIUM ONLY; not a collision-tested pose'})
    supportfront=max(front,shelf.BoundBox.YMin);supportrear=shelf.BoundBox.YMax;bolty=(supportfront+30.7+supportrear-30.7)/2
    horizontal=weight*ma['lateral_acceleration_g_for_lock_planning']; overturn=horizontal*(cg.z-z0)
    lock=max(0,overturn-weight*(cg.y-supportfront))/(bolty-supportfront)/2
    lock=max(lock,max(0,overturn-weight*(supportrear-cg.y))/(supportrear-bolty)/2)
    hinge_zones={side:box(x,1197,z0,96,105.1,t) for side,x in [('L',-78),('R',582)]}
    hinge_ok=all(current['BackboxFloorV32'].common(s).cut(floor).Volume<1e-6 for s in hinge_zones.values())
    lock_corridor=[max(front,shelf.BoundBox.YMin)+30.7,shelf.BoundBox.YMax-30.7]
    cable_ok=all(floor.common(s).Volume<1e-6 for s in passages.values())
    zero_valid=not zero_hits and not internal and clearance>=3 and hinge_ok and cable_ok
    status='REJECTED_ZERO' if not zero_valid else 'WARNING_BELOW_190_STOP'
    row={'bottom_depth_mm':depth,'slope_deg_from_vertical':math.degrees(math.atan(k)),'front_y_mm':front,'top_front_y_mm':rear-254,
         'floor_bounds_mm':bounds(floor),'bottom_panel_depth_mm':jointlen,'internal_lower_depth_mm':depth-t,
         'zero_valid':zero_valid,'zero_hits':zero_hits,'internal_hits':internal,'channel_clearance_mm':clearance,
         'shelf_projection_forward_mm':front-shelf.BoundBox.YMin,'bearing_mm2':contact.Area,'continuous_bearing_width_mm':564,
         'bearing_retained_percent':100*contact.Area/plane_face(current['BackboxFloorV32'],z0).common(plane_face(shelf,z0)).Area,
         'joint_length_mm':jointlen,'capture_width_mm':6,'engaged_area_each_side_mm2':6*jointlen,
         'fasteners_per_side_outside_hinge_reserve':count,'geometric_fastener_count_before_hinge_exclusion':geometric_count,'fastener_minimum_pitch_mm':pitch if count>1 else None,'fastener_end_distance_mm':end,'fastener_transverse_stock_center_mm':9,
         'fastener_positions_xyz_mm':positions,'minimum_planar_ligament_mm':ligament,'toy_area_each_side_mm2':toy.Volume,
         'toy_reserve_depth_mm':40,'rear_board_service_zone_mm':[240,32,300],'rear_board_replaceable_panel_assumption_mm':[240,12,300],
         'lower_service_zone_mm':[160,50,75],'hinge_zones_preserved':hinge_ok,'lock_safe_center_y_mm':lock_corridor,'lock_zones_available':lock_corridor[1]>lock_corridor[0],
         'floor_passports_preserved':cable_ok,'matched_shelf_passports_confirmed':False,
         'fold_status':status,'fold_performed':False,'fold_samples':[],'first_collision_angle_deg':0 if zero_hits else None,
         'matrix_supports_new_fold_conflict':'NOT EVALUATED: no valid baseline',
         'mass':{'inventory':masses,'total_kg':total,'cg_xyz_mm':list(cg),'cg_relative_to_pivot_mm':list(rel),'upright_shelf_reaction_N':weight,
                 'upright_cg_inside_bearing_interval':supportfront<=cg.y<=supportrear,'gravity_lock_tension_each_N':max(0,weight*(supportfront-cg.y)/(bolty-supportfront)/2,weight*(cg.y-supportrear)/(supportrear-bolty)/2),
                 'lock_tension_each_at_0_3g_N':lock,'lock_bolt_y_assumption_mm':bolty,'hinge_max_each_N_free_space':max(abs(x['reaction_each_hinge_N']) for x in loadcases),
                 'maximum_gravity_torque_Nm':max(abs(x['gravity_moment_Nm']) for x in loadcases),'loadcases':loadcases}}
    return wood,zones,row,contact

rows=[];bundle={'candidates':{},'context':[mesh(n,play[n]) for n in ('SIDE_L','BACKBOX_BASE','CandidateGlassChannelL','CandidateGlassChannelR')],
    'legacy':[mesh(n,s) for n,s in source.items() if n.startswith(('BackboxFloor','BackboxLeftSide','BackboxRightSide','BackboxTop','BackboxRearFrame'))]}
for depth in c['bottom_depth_candidates_mm']:
    wood,zones,row,contact=candidate(depth);rows.append(row)
    d=A.newDocument('BackboxProfile'+str(depth))
    for n,s in {**wood,**zones}.items():
        o=d.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','Role');o.Role='WOOD_CANDIDATE' if n in wood else 'GENERIC_RESERVE_NOT_KIT_ITEM'
    d.addProperty('App::PropertyString','ApprovalStatus');d.ApprovalStatus=row['fold_status']+'; NO SELECTED PROFILE; MANUFACTURING BLOCKED'
    d.recompute();d.saveAs(str(O/f'candidate-{depth}.FCStd'));A.closeDocument(d.Name)
    bundle['candidates'][str(depth)]={'wood':[mesh(n,s) for n,s in wood.items()],'zones':[mesh(n,s) for n,s in zones.items() if s.Volume>1e-9],
          'side_loops':[[[p.y,p.z] for p in w.discretize(Deflection=.1)] for w in wood['BackboxLeftSideV14'].slice(V(1,0,0),-85)],
          'floor_loops':[[[p.x,p.y] for p in w.discretize(Deflection=.1)] for w in wood['BackboxFloorV14'].slice(V(0,0,1),z0+9)]}
    check(f'{depth}: common bearing witness lies in retained floor',wood['BackboxFloorV14'].isInside(V(300,1220,z0+.001),1e-7,True))
    print('PROFILE_CANDIDATE',depth,'ZERO',row['zero_valid'],'GAP',row['channel_clearance_mm'],'STATUS',row['fold_status'],flush=True)

# Owner stop: no selectable (>=190 mm) profile passes zero. The warning candidate
# is dimensioned for comparison only; no lower-depth fold optimization is allowed.
check('all selectable candidates fail upright gate',all(not r['zero_valid'] for r in rows if r['bottom_depth_mm']>=190))
check('180 mm is warning only, never selected or swept',rows[-1]['fold_status']=='WARNING_BELOW_190_STOP' and not rows[-1]['fold_samples'])
check('accepted source bytes unchanged',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in hashes.items()))
limits={}
for target in (3,5):
    lo=1110;hi=1130
    for _ in range(30):
        y=(lo+hi)/2;test=box(-78,y,z0,756,1302.1-y,t)
        if min(test.distToShape(s)[0] for s in channels.values())>=target:hi=y
        else:lo=y
    limits[str(target)]={'minimum_front_y_mm':hi,'maximum_bottom_outer_depth_mm':rear-hi}
check('even absolute upright clearance requires below 190 mm',limits['3']['maximum_bottom_outer_depth_mm']<190)
check('bearing witness is above shelf interior',shelf.isInside(V(300,1220,z0-.001),1e-7,True))
report={'source_head':c['source_head'],'checks':checks,'source_hashes':hashes,'candidates':rows,'selected_depth_mm':None,
        'stop_reason':'210/200/190 fail upright channel gate. A sub-190 profile would be required; owner stop applies. No fold sweep or shallow-profile adoption.',
        'upright_depth_bounds':limits,
        'shelf_kinematic_incompatibility':{'method':'Local velocity of a shared bearing point; analytical incompatibility, NOT a fold test of a rejected candidate',
            'point_xyz_mm':[300,1220,z0],'pivot_xyz_mm':list(axis),'dz_dtheta_mm_per_radian':1220-axis.y,
            'dy_dtheta_mm_per_radian':-(z0-axis.z),'result':'The floor bearing point initially moves down into the unchanged shelf. Sloping the side front cannot change this velocity. No accepted datum or shelf was moved.'},
        'coarse_envelope_authority':'REFERENCE ONLY','manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(O/'mesh.json').write_text(json.dumps(bundle,separators=(',',':'))+'\n')
for n in ('LICENSE','NOTICE.md'):shutil.copyfile(R/n,O/n)
print('BACKBOX_PROFILE_PASS',len(checks),'SELECTED NONE',flush=True)

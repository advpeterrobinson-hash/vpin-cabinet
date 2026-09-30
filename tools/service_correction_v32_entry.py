"""Current V32 ergonomic/hinged-service correction. Original CERN-OHL-S-2.0."""
import hashlib
import json
import math
import sys
from pathlib import Path
import FreeCAD as A
import Part

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R/'tools'))
from validate_service_correction_v32 import validate_ergonomics, validate_visible_mechanism, negative_controls

O = R/'exports/generated/service-correction-v32'; O.mkdir(parents=True, exist_ok=True)
cp = R/'config/service_correction_v32.json'; c = json.loads(cp.read_text())
source = R/c['source_cad']; source_report = R/c['source_report']
old_report = json.loads(source_report.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source) == old_report['saved_cad_sha256']
assert all(x['pass'] for x in old_report['checks'])
inputs = {str(p.relative_to(R)): sha(p) for p in [cp, source, source_report, Path(__file__).resolve(),
    R/'tools/validate_service_correction_v32.py', R/'config/shelf_layout_freeze_v32.json',
    R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json',
    R/'exports/generated/side-panel-v32/simple-shelves-validation.json',
    R/'config/backbox_v06.json', R/'config/backbox_mounting_v12.json',
    R/'config/playfield_mechanics_v18.json', R/'config/playfield_fixed_anchors_v19.json']}
d = A.openDocument(str(source)); d.recompute()
scene = {o.Name: o.Shape.copy() for o in d.Objects if hasattr(o, 'Shape')}
original = {n:s.copy() for n,s in scene.items()}
V=A.Vector; checks=[]; findings={}; metadata={}; metal=[]; new_wood=[]
def check(name, result):
    checks.append({'check':name,'pass':bool(result)})
    print(('PASS ' if result else 'FAIL ')+name, flush=True)
def box(x,y,z,dx,dy,dz): return Part.makeBox(dx,dy,dz,V(x,y,z))
def cyl(x,y,z,r,h,axis=(1,0,0)): return Part.makeCylinder(r,h,V(x,y,z),V(*axis))
def diff(a,b): return a.cut(b).Volume+b.cut(a).Volume
def hits(parts, obstacles, ignore=()):
    out=[]
    for n,s in parts.items():
        for k,t in obstacles.items():
            if n==k or k in ignore: continue
            if s.BoundBox.intersect(t.BoundBox):
                volume=s.common(t).Volume
                if volume>c['collision_threshold_mm3']:out.append({'part':n,'obstacle':k,'mm3':volume})
    return out
def move(s, v):
    s=s.copy();s.translate(v);return s
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
def mirrored(s):
    s=s.copy();s.transformShape(mirror,True);return s
def put_pair(stem,left,kind):
    scene[stem+'L']=left;scene[stem+'R']=mirrored(left)
    if kind=='metal':metal.extend([stem+'L',stem+'R'])
    if kind=='wood':new_wood.extend([stem+'L',stem+'R'])

# Derive the local upper profile from the ACTUAL saved side outer-face edges.
left=scene['SIDE_L']; profile=[]
for edge in left.Edges:
    if len(edge.Vertexes)!=2:continue
    a,b=(v.Point for v in edge.Vertexes)
    if abs(a.x)<1e-7 and abs(b.x)<1e-7 and abs(a.y-b.y)>1:
        profile.append((a.y,a.z,b.y,b.z))
def top(y):
    z=[za+(y-ya)*(zb-za)/(yb-ya) for ya,za,yb,zb in profile if min(ya,yb)-1e-6<=y<=max(ya,yb)+1e-6]
    if not z:raise ValueError('No saved side-top section at '+str(y))
    return max(z)
e=c['ergonomics'];validate_ergonomics(e)
centers={name:{'y_mm':e[name+'_y_mm'],'z_mm':top(e[name+'_y_mm'])-e['below_local_top_mm'],
               'top_z_mm':top(e[name+'_y_mm']),'below_top_mm':e['below_local_top_mm']}
         for name in ('primary','secondary')}
hw=c['button_hardware']
# Restore the rejected reference holes in the source before making new ones.
# This is generated geometry, not a patch installed in the physical cabinet.
for y in (255,310):left=left.fuse(cyl(0,y,270,14.2875,18)).removeSplitter()
for name,datum in centers.items():
    y,z=datum['y_mm'],datum['z_mm']
    left=left.cut(cyl(-1,y,z,hw['reference_bore_mm']/2,20))
    left=left.cut(cyl(18-hw['candidate_nut_pocket_depth_mm'],y,z,hw['candidate_nut_pocket_diameter_mm']/2,hw['candidate_nut_pocket_depth_mm']+1))
    # Original visible pinball leaf concept, NOT vendor manufacturing geometry.
    button=cyl(-5,y,z,hw['candidate_head_diameter_mm']/2,5).fuse(cyl(0,y,z,hw['candidate_barrel_diameter_mm']/2,hw['candidate_barrel_inward_end_x_mm'])).removeSplitter()
    nut=cyl(15,y,z,hw['candidate_nut_diameter_mm']/2,3).cut(cyl(14,y,z,hw['candidate_barrel_diameter_mm']/2,5))
    bracket=box(20,y-10,z-32,22,20,16)
    # Two leaf contacts below the barrel; copper surfaces are schematic.
    contacts=box(21,y-7,z-15,20,14,.6).fuse(box(21,y-7,z-13.5,20,14,.6)).fuse(box(21,y-7,z-15,2,14,2.1)).removeSplitter()
    put_pair('LeafButton_'+name+'_',button,'reference')
    put_pair('LeafNut_'+name+'_',nut,'reference')
    put_pair('LeafBracket_'+name+'_',bracket,'reference')
    put_pair('LeafContacts_'+name+'_',contacts,'reference')
scene['SIDE_L']=left;scene['SIDE_R']=mirrored(left)
for n in list(scene):
    if n.startswith('CandidateSideButton'):scene.pop(n)
check('actual side profile is expected baseline',abs(top(0)-400.05)<1e-6 and abs(top(1308.1)-596.9)<1e-6)
check('old rejected side-button holes absent',all(scene['SIDE_L'].isInside(V(9,y,270),1e-6,True) for y in (255,310)))
for name,b in centers.items():
    check(name+' bore at ergonomic center',not scene['SIDE_L'].isInside(V(9,b['y_mm'],b['z_mm']),1e-6,True))

# Preserve holder's slope and bridge. Convert the two rails to flat CNC 18mm
# plywood side profiles with integral rear ears and integral prop-pivot pads.
p=c['playfield']; slope=(top(100)-top(0))/100; alpha=math.atan(slope)
bz=400.05+45*slope-12-55*math.cos(alpha)
def tf(s):
    s=s.copy();s.rotate(V(),V(1,0,0),math.degrees(alpha));s.translate(V(0,45,bz));return s
def local_point(y,z):return tf(Part.Vertex(V(0,y,z))).Vertexes[0].Point
screen=json.loads((R/'exports/generated/side-panel-v32/shelf-service-pose-screen.json').read_text())
py=screen['pivot_xyz_mm'][1]+p['pivot_y_adjustment_from_previous_screen_mm'];pz=top(py)-p['pivot_below_local_top_mm'];pivot=V(300,py,pz)
ly=(py-45)*math.cos(alpha)+(pz-bz)*math.sin(alpha)
lz=-(py-45)*math.sin(alpha)+(pz-bz)*math.cos(alpha)
upper=local_point(p['cradle_prop_mount_local_y_mm'],p['cradle_prop_mount_local_z_mm'])
def rotate(s,angle):
    s=s.copy();s.rotate(pivot,V(1,0,0),-angle);return s
def rotated_point(pt,angle):
    return rotate(Part.Vertex(pt),angle).Vertexes[0].Point
raised_upper=rotated_point(upper,p['service_opening_deg'])
ry,rz=p['receiver_yz_mm'];length=math.hypot(raised_upper.y-ry,raised_upper.z-rz)
stow_angle=alpha
sy=upper.y-length*math.cos(stow_angle);sz=upper.z-length*math.sin(stow_angle)
stow_local_y=(sy-45)*math.cos(alpha)+(sz-bz)*math.sin(alpha)
rad=p['candidate_wood_bore_mm']/2
railx=p['rail_x_left_mm']
rail=box(railx,60,-36,18,940,18)
for local_y,top_z in ((p['cradle_prop_mount_local_y_mm'],0),(stow_local_y,-18)):
    rail=rail.fuse(box(railx,local_y-25,-54,18,50,top_z+54))
rail=rail.fuse(box(railx,985,-36,18,max(55,ly+20-985),lz+56)).removeSplitter()
rail=tf(rail).cut(cyl(railx-1,py,pz,7.1,20)).cut(cyl(railx-1,upper.y,upper.z,rad,20)).cut(cyl(railx-1,sy,sz,rad,20))
scene['MONITOR_RAIL_L']=rail;scene['MONITOR_RAIL_R']=mirrored(rail)
# Simplify the replaceable bridge to a404mm-wide rectangle, inside both props.
# Nothing is cut in permanent crossmembers/shelves to accommodate the arms.
scene['MONITOR_BRIDGE']=tf(box(98,360,-18,404,250,18))
# Removable adapter spacers lift the maximum-thickness screen just enough to
# preserve the owner's hand location. CNC face-pocket18mm stock to12mm.
normal=V(0,-math.sin(alpha),math.cos(alpha))*p['display_raise_normal_mm']
scene['PLAYFIELD_ENVELOPE']=move(scene['PLAYFIELD_ENVELOPE'],normal)
for i,y in enumerate((400,560),1):
    scene[f'PF_DisplaySpacer{i}']=tf(box(100,y,0,400,20,p['display_raise_normal_mm']));new_wood.append(f'PF_DisplaySpacer{i}')
# Integral rail profile lies behind the display edge; no custom cheek plate.
fixed={}
for stem,y,z,thickness,dy,dz in [('PF_ReceiverBlock',ry,rz,54,30,20)]:
    s=box(18,y-dy/2,z-dz/2,thickness,dy,dz).cut(cyl(17,y,z,rad,thickness+2))
    put_pair(stem,s,'wood');fixed[stem+'L']=s;fixed[stem+'R']=mirrored(s)
    metadata[stem]={'nominal_18mm_blanks_per_side':int(thickness/18),'hole_yz_mm':[y,z],'bonded_to_full_sidewall':True}
    scene['SIDE_L']=scene['SIDE_L'].cut(cyl(-1,y,z,rad,20))
scene['SIDE_R']=mirrored(scene['SIDE_L'])
scene['SIDE_L']=scene['SIDE_L'].cut(cyl(-1,py,pz,5.25,20));scene['SIDE_R']=mirrored(scene['SIDE_L'])

def washer(x,y,z):return cyl(x,y,z,8,1).cut(cyl(x-1,y,z,4.25,3))
def nut(x,y,z):
    points=[V(x,y+7.5*math.cos(i*math.pi/3),z+7.5*math.sin(i*math.pi/3)) for i in range(7)]
    return Part.Face(Part.makePolygon(points)).extrude(V(7,0,0)).cut(cyl(x-1,y,z,4,9))
def bolt(x,y,z,span):return cyl(x,y,z,6.5,5).fuse(cyl(x+5,y,z,4,span)).removeSplitter()
for stem,y,z,start,span in [('PF_PropPivot',upper.y,upper.z,72,50)]:
    put_pair(stem+'Bolt',bolt(start,y,z,span),'metal')
    put_pair(stem+'Locknut',nut(116,y,z),'metal')
    for j,x in enumerate((77,96,115),1):
        put_pair(stem+f'Washer{j}',washer(x,y,z),'metal')

# Stock M10 rod = the cross-axis itself, not a custom machined journal.
scene['PF_RearPivotAxis']=cyl(-8,py,pz,5,616);metal.append('PF_RearPivotAxis')
def washer10(x):return cyl(x,py,pz,10,1).cut(cyl(x-1,py,pz,5.25,3))
def nut10(x):
    pts=[V(x,py+9*math.cos(i*math.pi/3),pz+9*math.sin(i*math.pi/3)) for i in range(7)]
    return Part.Face(Part.makePolygon(pts)).extrude(V(7,0,0)).cut(cyl(x-1,py,pz,5,9))
for i,x in enumerate((-1,96,115),1):put_pair(f'PF_AxisWasher{i}',washer10(x),'metal')
for i,x in enumerate((-8,89,116),1):put_pair(f'PF_AxisLocknut{i}',nut10(x),'metal')
put_pair('PF_PlainBush',cyl(97,py,pz,7,18).cut(cyl(96,py,pz,5.25,20)),'polymer')

# Two IDENTICAL flat scrap-plywood arms, with CLOSED end holes. Length is
# derived above from the opened CAD, never selected from a catalogue or guessed.
def prop(a,b):
    dy,dz=b[0]-a[0],b[1]-a[1];dist=math.hypot(dy,dz);ny,nz=-dz/dist,dy/dist;half=p['prop_width_mm']/2;x=p['prop_x_left_mm']
    pts=[V(x,a[0]+ny*half,a[1]+nz*half),V(x,b[0]+ny*half,b[1]+nz*half),V(x,b[0]-ny*half,b[1]-nz*half),V(x,a[0]-ny*half,a[1]-nz*half)]
    s=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(p['prop_thickness_mm'],0,0))
    for y,z in (a,b):s=s.fuse(cyl(x,y,z,p['prop_end_diameter_mm']/2,p['prop_thickness_mm']))
    for y,z in (a,b):s=s.cut(cyl(x-1,y,z,rad,p['prop_thickness_mm']+2))
    return s.removeSplitter()
stow_prop=prop((upper.y,upper.z),(sy,sz));engaged_prop=prop((raised_upper.y,raised_upper.z),(ry,rz))
put_pair('PF_Prop',stow_prop,'wood')
def positive_pin(y,z,start=73,end=115):
    # Generic purchased positive-lock pin: captive ball locks emerge OUTSIDE
    # sidewall; head remains inside. No clevis, journal or fabricated keeper.
    shaft=cyl(start,y,z,4,end-start).fuse(cyl(end,y,z,7,6))
    for off in (-4,4):shaft=shaft.fuse(Part.makeSphere(1.5,V(start+3,y+off,z)))
    return shaft.removeSplitter()
put_pair('PF_PositivePin',positive_pin(ry,rz,-5,96),'metal')
put_pair('PF_StowPin',positive_pin(sy,sz),'metal')

# A conservative full upper-backbox volume, not proprietary geometry nor a new
# backbox design. Existing780x254x723.9 + rear-flush/centerline datum.
bb=json.loads((R/'config/backbox_v06.json').read_text())['future_proof_backbox']
bb_front=1308.1-bb['target_outer_depth_mm']
backbox=box((600-bb['target_outer_width_mm'])/2,bb_front,596.9,bb['target_outer_width_mm'],bb['target_outer_depth_mm'],bb['target_outer_height_mm'])
scene['PF_BackboxCheckEnvelope']=backbox
metadata['PF_BackboxCheckEnvelope']={'reference_only':True,'front_y_mm':bb_front,'status':'CONSERVATIVE_ENVELOPE_NOT_COMPLETE_V32_BACKBOX'}
moving=list(p['moving_ids'])+['PF_PlainBushL','PF_PlainBushR']+[n for n in scene if n.startswith('PF_PropPivot') or n.startswith('PF_StowPin')]
glass_removed={'CandidateGlass'}
poses={'PLAY':dict(scene)}
for state,active in [('SERVICE',('L','R')),('SERVICE LEFT PROP ONLY',('L',)),('SERVICE RIGHT PROP ONLY',('R',))]:
    pose={n:s.copy() for n,s in scene.items() if n not in glass_removed}
    for n in moving:pose[n]=rotate(scene[n],p['service_opening_deg'])
    for side in ('L','R'):
        if side in active:
            pose['PF_Prop'+side]=engaged_prop if side=='L' else mirrored(engaged_prop)
        else:
            pose.pop('PF_Prop'+side);pose.pop('PF_PositivePin'+side)
    poses[state]=pose

# Honest checks: avoid counting display/PC/payload budgets as solid hardware
# whose own contents conflict. All newly added shapes are screened against
# retained wood, hardware, glass and display, including conservative backbox.
reservations={n for n in scene if 'Reserve' in n or 'RESERVED' in n or 'CandidatePayload' in n}
changed={n for n in scene if n not in original or n in ('MONITOR_RAIL_L','MONITOR_RAIL_R','PLAYFIELD_ENVELOPE')}
for state,pose in poses.items():
    involved={n:pose[n] for n in changed if n in pose and n!='PF_BackboxCheckEnvelope'}
    obstacles={n:s for n,s in pose.items() if n not in reservations}
    collision=hits(involved,obstacles)
    # Adapter spacers intentionally bear against display/bridge, not intersect.
    findings[state+'_collisions']=collision
    check(state+' new parts and supports have no positive-volume conflicts',not collision)
    check(state+' all modeled pieces valid single solids',all(s.isValid() and len(s.Solids)==1 for s in pose.values()))
check('two props geometrically identical mirrored flat18mm wood',diff(mirrored(stow_prop),scene['PF_PropR'])<1e-5 and abs(stow_prop.BoundBox.XLength-18)<1e-6)
check('left/right corrected sides symmetric',diff(mirrored(scene['SIDE_L']),scene['SIDE_R'])<1e-5)
for side in ('L','R'):
    receiver_parts=[poses['SERVICE']['PF_Prop'+side],scene['PF_ReceiverBlock'+side]]
    check(side+' raised receiver and prop closed holes coaxial',all(not shape.isInside(V(shape.BoundBox.Center.x,ry,rz),1e-6,True) and shape.isInside(V(shape.BoundBox.Center.x,ry+7,rz),1e-6,True) for shape in receiver_parts))
    check(side+' positive receiver pin spans prop and full sidewall',poses['SERVICE']['PF_PositivePin'+side].BoundBox.XLength>=107)
check('no legacy pivot bearings custom journals rods clevises or gas struts',not any(any(k in n.lower() for k in ('ucfl','journal','clevis','strut','steelprop','cheekplate')) for n in scene))
# Exact preservation comparison for every approved item outside the correction.
preserved=[n for n in original if n not in ('SIDE_L','SIDE_R','MONITOR_RAIL_L','MONITOR_RAIL_R','MONITOR_BRIDGE','PLAYFIELD_ENVELOPE') and not n.startswith('CandidateSideButton')]
check('all other original CAD solids exactly unchanged',all(diff(scene[n],original[n])<1e-5 for n in preserved))
extent=lambda s,i:(min(tuple(v.Point)[i] for v in s.Vertexes),max(tuple(v.Point)[i] for v in s.Vertexes))
check('600mm body and side profile unchanged',all(abs(a-b)<1e-5 for a,b in zip([*extent(scene['SIDE_L'],0),*extent(scene['SIDE_L'],1),*extent(scene['SIDE_L'],2),*extent(scene['SIDE_R'],0)],[0,18,0,1308.1,0,596.9,582,600])) and scene['SIDE_L'].cut(box(0,0,0,18,1308.1,596.9)).Volume<1e-5)
check('low PC no drawer and frozen three shelf datums unchanged',all(diff(scene[n],original[n])<1e-6 for n in ('PC_BASE','PC_ENVELOPE','SHELF_1','SHELF_2','SHELF_3')) and not any('Drawer' in n or 'Slide' in n for n in scene))

# Captive arms remain positively stowed on the moving holder while it is lifted.
sweep=[]
fixed_scene={n:s for n,s in scene.items() if n not in set(moving+['PF_PropL','PF_PropR','PF_PositivePinL','PF_PositivePinR'])|glass_removed|reservations}
for angle in range(0,int(p['service_opening_deg'])+1,c['sweep_step_degrees']):
    moving_shapes={n:rotate(scene[n],angle) for n in moving+['PF_PropL','PF_PropR']}
    collision=hits(moving_shapes,fixed_scene)
    sweep.append({'opening_deg':angle,'conflicts':collision})
findings['opening_sweep']=sweep
check('sampled0..100deg holder sweep clears fixed stowed props cabinet and backbox',not any(x['conflicts'] for x in sweep))
# Stored receiver pins MUST be withdrawn before lifting: their heads obstruct
# the real rail sweep. This is a verified release step, not an omitted obstacle.
pin_block=hits({n:rotate(scene[n],30) for n in moving},
              {n:scene[n] for n in ('PF_PositivePinL','PF_PositivePinR')})
check('negative control receiver pins left inserted block opening',bool(pin_block))
findings['receiver_pin_release_required']=pin_block
# Swing each released prop from carried position to engaged receiver at full
# opening. Other arm stays carried. No friction-based stop is introduced.
deployment=[]
carried=rotate(stow_prop,p['service_opening_deg'])
stowed_end=rotated_point(V(0,sy,sz),p['service_opening_deg'])
start_angle=math.atan2(stowed_end.z-raised_upper.z,stowed_end.y-raised_upper.y)
end_angle=math.atan2(rz-raised_upper.z,ry-raised_upper.y)
# Swing toward the player first; the short rearward route intersects the screen.
delta=(end_angle-start_angle)%(2*math.pi)
deploy_obstacles={n:s for n,s in poses['SERVICE'].items() if n not in ('PF_PropL','PF_PropR','PF_PositivePinL','PF_PositivePinR','PF_StowPinL','PF_StowPinR') and n not in reservations}
for i in range(21):
    arm=carried.copy();arm.rotate(V(0,raised_upper.y,raised_upper.z),V(1,0,0),math.degrees(delta)*i/20)
    collision=hits({'PF_PropL':arm,'PF_PropR':mirrored(arm)},deploy_obstacles)
    deployment.append({'sample':i,'conflicts':collision})
findings['prop_deployment']=deployment
check('sampled prop swing to receiver unobstructed',not any(x['conflicts'] for x in deployment))

# Reuse12 real tool axes and loaded routes, add new fixed/moving mechanism to
# the already checked frozen shelf scene. Carry actual amp/PSU/USB reserves.
sr=json.loads((R/'exports/generated/side-panel-v32/simple-shelves-validation.json').read_text())
service=poses['SERVICE']; ceiling=max(s.BoundBox.ZMax for n,s in service.items() if n in moving)+100
tools={a['bolt']:Part.makeCylinder(sr['config']['tool_radius_mm'],ceiling-a['head_top_z_mm'],V(a['xyz_mm'][0],a['xyz_mm'][1],a['head_top_z_mm'])) for a in sr['axes']}
mechanism={n:s for n,s in service.items() if n in changed and n!='PF_BackboxCheckEnvelope'}
tool_hits=hits(tools,mechanism);findings['tool_column_conflicts']=tool_hits
check('all12 frozen top-release tool columns clear raised mechanism',len(tools)==12 and not tool_hits)
route_results=[]
for route in sr['routes']:
    parts={n:service[n].copy() for n in route['moving'] if n in service}
    shelf=route['shelf']
    payloads={'SHELF_2':['SSF_AmplifierReserve','SSF_USBReserve'],'SHELF_3':['SSF_PSUReserve']}.get(shelf,[])
    for n in payloads:parts[n]=service[n].copy()
    collision=[]
    for xyz in route['translations_mm']:
        v=V(*xyz)
        for n,s in parts.items():
            b=s.BoundBox;sw=box(b.XMin+min(0,v.x),b.YMin+min(0,v.y),b.ZMin+min(0,v.z),b.XLength+abs(v.x),b.YLength+abs(v.y),b.ZLength+abs(v.z))
            collision+=hits({n:sw},mechanism)
            s.translate(v)
    route_results.append({'shelf':shelf,'conflicts':collision})
findings['loaded_shelf_routes']=route_results
check('all3 existing loaded shelf service routes clear new mechanism',len(route_results)==3 and not any(x['conflicts'] for x in route_results))
# Reject the OLD assumed axis against the previously omitted upper backbox.
old_open={n:original[n].copy() for n in ['PLAYFIELD_ENVELOPE','MONITOR_RAIL_L','MONITOR_RAIL_R','MONITOR_BRIDGE']}
for s in old_open.values():s.rotate(V(*screen['pivot_xyz_mm']),V(1,0,0),-100)
check('negative control rejects old axis against upper backbox',bool(hits(old_open,{'upper_backbox':backbox})))
check('negative control unraised55mm display conflicts with corrected button barrel',bool(hits({n:s for n,s in scene.items() if n.startswith('LeafButton')},{'original_display':original['PLAYFIELD_ENVELOPE']})))
check('closed display still blocks tool columns negative control',bool(hits(tools,{'closed_display':scene['PLAYFIELD_ENVELOPE']})))

review={'buttons':centers,'old_buttons':{'primary':[255,270],'secondary':[310,270]},'pivot_xyz_mm':[pivot.x,pivot.y,pivot.z],
    'previous_assumed_pivot_xyz_mm':screen['pivot_xyz_mm'],'opening_deg':p['service_opening_deg'],'closed_slope_deg':math.degrees(alpha),
    'prop_length_centers_mm':length,'prop_width_mm':p['prop_width_mm'],'prop_blank_length_mm':length+p['prop_end_diameter_mm'],
    'prop_upper_closed_yz_mm':[upper.y,upper.z],'cradle_pin_closed_yz_mm':[upper.y,upper.z],'prop_upper_service_yz_mm':[raised_upper.y,raised_upper.z],
    'receiver_yz_mm':[ry,rz],'stow_yz_mm':[sy,sz],'plywood_support_pieces':2,'commodity_metal_parts':len(metal),
    'commodity_metal_ids':metal,'local_wood_blank_count':sum(v.get('nominal_18mm_blanks_per_side',0)*2 for v in metadata.values()),
    'custom_metal_parts_required':0,'structural_proof':False,'manufacturing_ready':False,
    'backbox_envelope_front_y_mm':bb_front,'display_raise_normal_mm':p['display_raise_normal_mm'],
    'limits':'Sampled motion and original simplified hardware envelopes; no load, hardware-fit, connector/harness or continuous-sweep proof. Single-prop states are load-path REVIEW ONLY, never a service instruction.'}

diagnostic={'checks':checks,'findings':findings,'review':review,
            'side_bounds':[str(scene[n].BoundBox) for n in ('SIDE_L','SIDE_R')],
            'invalid_shapes':{state:[n for n,s in pose.items() if not s.isValid() or len(s.Solids)!=1] for state,pose in poses.items()},
            'source_hashes':inputs}
(O/'geometry-diagnostic.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
assert all(x['pass'] for x in checks),[x['check'] for x in checks if not x['pass']]

def mesh(n,s):
    vertices,faces=s.tessellate(1.0)
    return {'name':n,'vertices':[[v.x,v.y,v.z] for v in vertices],'faces':[list(f) for f in faces]}
bundle={'parts':[mesh(n,s) for n,s in scene.items()],'states':{},'review':review}
for state,pose in poses.items():
    bundle['states'][state]={n:(mesh(n,pose[n]) if n in pose else None) for n in scene if n not in pose or diff(scene[n],pose[n])>1e-5}
validate_visible_mechanism(bundle);controls=negative_controls(bundle,c)
check('ergonomic and missing-support negative controls reject regressions',len(controls)==7)

saved={}
for state,pose in poses.items():
    out=A.newDocument('V32_'+state.replace(' ','_'));out.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; DESIGN-PROVISIONAL; CNC BLOCKED; no load proof'
    for n,s in pose.items():
        o=out.addObject('PartDesign::Feature',n);o.Shape=s
        o.addProperty('App::PropertyString','EngineeringStatus');o.EngineeringStatus='DESIGN_PROVISIONAL_NOT_LOAD_PROVEN'
        o.addProperty('App::PropertyString','PartID');o.PartID=n
    out.recompute();path=O/(state.lower().replace(' ','-')+'.FCStd');out.saveAs(str(path));A.closeDocument(out.Name)
    out=A.openDocument(str(path));out.recompute()
    check(state+' saved CAD recomputes and preserves exact valid solids',all(o.Shape.isValid() and len(o.Shape.Solids)==1 and diff(o.Shape,pose[o.Name])<1e-5 and 'Invalid' not in o.State for o in out.Objects if hasattr(o,'Shape')))
    if state=='PLAY':Part.export([o for o in out.Objects if hasattr(o,'Shape') and o.Name!='PF_BackboxCheckEnvelope'],str(O/'current-v32.step'))
    saved[state]={'path':str(path.relative_to(R)),'sha256':sha(path),'solids':len(pose)};A.closeDocument(out.Name)
check('source CAD all frozen inputs legacy configs untouched',all(sha(R/name)==expected for name,expected in inputs.items()))
(O/'mesh.json').write_text(json.dumps(bundle))
report={'status':'OWNER_CORRECTION_DESIGN_PROVISIONAL','manufacturing_ready':False,'structural_proof':False,
    'source_hashes':inputs,'review':review,'config':c,'checks':checks,'findings':findings,'saved_poses':saved,
    'negative_controls':controls,'preserved_original_solids':preserved,'local_wood_metadata':metadata,
    'source_39_checks_passed':all(x['pass'] for x in old_report['checks']),'mesh_sha256':sha(O/'mesh.json')}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
A.closeDocument(d.Name)
assert all(x['pass'] for x in checks),[(x['check']) for x in checks if not x['pass']]
print('SERVICE_CORRECTION_PASS',len(checks),'checks;',len(scene),'solids; props',round(length,3),'mm; angle',p['service_opening_deg'])

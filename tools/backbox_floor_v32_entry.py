"""V32 floor-only integration; source CAD, explicit zero/fold gates. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib, json, math, shutil, subprocess
import FreeCAD as A
import Part

R=Path(__file__).resolve().parents[1]; V=A.Vector
c=json.loads((R/'config/backbox_floor_v32.json').read_text()); O=R/c['output_directory']; O.mkdir(parents=True,exist_ok=True)
checks=[]
def check(name,value):
    assert value,name
    checks.append({'check':name,'pass':True})
def load(path):
    d=A.openDocument(str(R/path));d.recompute()
    shapes={o.Name:o.Shape.copy() for o in d.Objects if hasattr(o,'Shape')}
    roles={o.Name:o.AuditRole for o in d.Objects if hasattr(o,'AuditRole')}
    A.closeDocument(d.Name);return shapes,roles
def box(x,y,z,w,h,t):return Part.makeBox(w,h,t,V(x,y,z))
def hits(moving,fixed):
    rows=[]
    for n,s in moving.items():
        for m,t in fixed.items():
            if not s.BoundBox.intersect(t.BoundBox):continue
            common=s.common(t)
            if common.Volume>1e-6:
                rows.append({'part':n,'obstacle':m,'volume_mm3':common.Volume})
    return rows
def minimum(moving,fixed):
    pairs=[]
    for n,s in moving.items():
        for m,t in fixed.items():
            a,b=s.BoundBox,t.BoundBox
            lb=math.sqrt(sum(max(0,getattr(a,k+'Min')-getattr(b,k+'Max'),getattr(b,k+'Min')-getattr(a,k+'Max'))**2 for k in 'XYZ'))
            pairs.append((lb,n,m,s,t))
    best=math.inf;pair=None
    for lb,n,m,s,t in sorted(pairs,key=lambda r:r[0]):
        if lb>=best:break
        dist=s.distToShape(t)[0]
        if dist<best:best=dist;pair=[n,m]
    return {'mm':best,'pair':pair}
def area_face(s,z):
    return Part.makeCompound([f for f in s.Faces if abs(f.CenterOfMass.z-z)<1e-7 and abs(f.normalAt(0,0).z)>.999])
def mesh(n,s):
    vv,ff=s.tessellate(.6)
    return {'name':n,'vertices':[[v.x,v.y,v.z] for v in vv],'faces':[list(f) for f in ff]}
def bounds(s):
    b=s.BoundBox;return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]

# Every pre-task tracked source/artifact is immutable, except the directly associated
# entry-point documentation. This also protects exact viewer and historical audit bytes.
tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',c['source_head']],cwd=R,text=True).splitlines()
protected=[p for p in tracked if p.startswith(('config/','tools/','cad/','exports/'))]
hashes={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in protected if (R/p).is_file()}
source,roles=load(c['source_backbox']); play,_=load(c['source_play']); removed,_=load(c['source_removed'])
wood={n:s for n,s in source.items() if roles.get(n)=='wood'};old=wood['BackboxFloorV14']; b=old.BoundBox
check('source nominal floor stock is 18 mm',abs(b.ZLength-c['stock_mm'])<1e-7)
channels={n:play[n] for n in ('CandidateGlassChannelL','CandidateGlassChannelR')}
old_hits=hits({'BackboxFloorV14':old},channels)
check('accepted old per-side collision reproduced',len(old_hits)==2 and all(abs(x['volume_mm3']-937.4505183347)<1e-6 for x in old_hits))

# Compare the owner's first preference: simple symmetric corner chamfers. A corner
# cut derived from a straight support plane is NOT a boolean copy of a channel.
corner_trials=[]
for slope in c['corner_trim_slopes_to_compare']:
    offset=max(slope*v.Point.x+v.Point.y for v in channels['CandidateGlassChannelL'].Vertexes)+c['glass_channel_target_mm']*math.sqrt(1+slope*slope)
    xf=(offset-b.YMin)/slope;yl=offset-slope*b.XMin
    points=[V(b.XMin,yl,b.ZMin),V(xf,b.YMin,b.ZMin),V(600-xf,b.YMin,b.ZMin),V(b.XMax,yl,b.ZMin),V(b.XMax,b.YMax,b.ZMin),V(b.XMin,b.YMax,b.ZMin)]
    keep=Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(0,0,c['stock_mm']))
    trial=old.common(keep)
    corner_trials.append({'slope':slope,'material_removed_mm3':old.Volume-trial.Volume,
        'channel_clearance_mm':minimum({'trial':trial},channels)['mm'],
        'glass_intersection_mm3':trial.common(play['CandidateGlass']).Volume,
        'accepted':False,'reason':'central floor still intersects installed glass'})
check('corner-only trims are rejected for installed glass interference',all(t['glass_intersection_mm3']>1 for t in corner_trials))

# Least-removal straight trim on a declared 0.1 mm design grid. The contour is
# a planar, full-width edge, never a channel subtraction or copied contour.
def floor_at(front):return old.common(box(b.XMin-1,front,b.ZMin,b.XLength+2,b.YMax-front+1,c['stock_mm'])).removeSplitter()
lo=b.YMin;hi=max(s.BoundBox.YMax for s in channels.values())+c['glass_channel_target_mm']
for _ in range(32):
    mid=(lo+hi)/2;trial=floor_at(mid)
    if minimum({'floor':trial},channels)['mm']>=c['glass_channel_target_mm']:hi=mid
    else:lo=mid
threshold=hi;grid=c['front_position_grid_mm'];front=math.ceil(threshold/grid)*grid;new=floor_at(front)
check('selected straight edge meets preferred 5 mm channel margin',minimum({'floor':new},channels)['mm']>=5)
check('previous design-grid front position fails 5 mm',minimum({'floor':floor_at(front-grid)},channels)['mm']<5)
check('floor only removes old material and remains one CNC solid',new.isValid() and len(new.Solids)==1 and new.cut(old).Volume<1e-6)
check('corrected floor clears installed glass',new.common(play['CandidateGlass']).Volume<1e-6)
wood.pop('BackboxFloorV14');wood['BackboxFloorV32']=new
internal=[x for x in hits(wood,wood) if x['part']<x['obstacle']]
check('reconstructed wood joints remain non-overlapping',not internal)

shelf=play['BACKBOX_BASE'];shelf_top=area_face(shelf,b.ZMin)
old_bottom=area_face(old,b.ZMin);new_bottom=area_face(new,b.ZMin)
old_contact=old_bottom.common(shelf_top);new_contact=new_bottom.common(shelf_top)
check('rear-shelf bearing is intended surface contact with zero penetration',new.common(shelf).Volume<1e-6 and new.distToShape(shelf)[0]<1e-7)
check('exact rear-shelf bearing area preserved',abs(new_contact.Area-old_contact.Area)<1e-6)
check('rear-shelf front datum preserved',abs(shelf.BoundBox.YMin-1127.125)<1e-7)
continuous_width=shelf.BoundBox.XLength
band=box(shelf.BoundBox.XMin,shelf.BoundBox.YMin,b.ZMin,continuous_width,1,.001)
check('full 564 mm continuous front bearing band retained',abs(new.common(band).Volume-564*.001)<1e-6)

hinge=json.loads((R/'config/backbox_fold_v10.json').read_text()); structure=json.loads((R/'config/structure_geometry_v14.json').read_text())
axis=V(300,hinge['cabinet']['side_length_mm']-hinge['cabinet']['pivot_from_rear_mm'],hinge['cabinet']['pivot_from_bottom_mm'])
check('accepted WPC references unchanged',list(axis)==[300,1270,508] and hinge['cabinet']['outer_width_mm']==600 and hinge['backbox']['outer_width_mm']==780 and hinge['backbox']['hinge_floor_bolt_inset_each_side_mm']==59.8375)

# Protect existing source wood in the whole outboard rear mounting bands, not
# an invented three-hole bracket pattern. The longitudinal reserve extends one
# stock thickness ahead of the documented 110 mm packaging keep-out.
hy0=axis.y-structure['wpc_hinges']['bracket_keepout_y_mm']/2-c['stock_mm']
zones={}
for side,x0,x1 in [('L',b.XMin,18),('R',582,b.XMax)]:
    zones['HingeMaterialZone'+side]=box(x0,hy0,b.ZMin,x1-x0,b.YMax-hy0,c['stock_mm'])
    check('entire existing hinge-zone material preserved '+side,old.common(zones['HingeMaterialZone'+side]).cut(new).Volume<1e-6)

# Only X is authoritative for upright locks. Calculate an available Y corridor
# from actual shelf/floor edges and the reference access diameter plus 18 mm wood.
hole_radius=hinge['upright_locking']['backbox_floor_access_hole_diameter_mm']/2
pad=hole_radius+c['minimum_zone_wood_margin_mm'];sy0=shelf.BoundBox.YMin;sy1=shelf.BoundBox.YMax
lock_y=[max(front,sy0)+pad,min(b.YMax,sy1)-pad]
check('substantial available lock corridor remains',lock_y[1]-lock_y[0]>100)
for side,x in [('L',120),('R',480)]:
    zones['LockMaterialZone'+side]=box(x-pad,lock_y[0]-pad,b.ZMin,2*pad,lock_y[1]-lock_y[0]+2*pad,c['stock_mm'])
    check('existing material in lock corridor preserved '+side,old.common(zones['LockMaterialZone'+side]).cut(new).Volume<1e-6)

from owner_features_v27 import features
from build_owner_services_v27 import cut_shape
passages={}
for f in features():
    if f['part']=='BackboxFloorV14':
        cut=cut_shape(f).common(box(b.XMin, b.YMin, b.ZMin,b.XLength,b.YLength,c['stock_mm']))
        passages[f['key']]=cut
        check('unchanged floor cable passport remains fully open '+f['key'],new.common(cut).Volume<1e-6 and old.common(cut).Volume<1e-6)
        zones['CablePassportZone'+f['key']]=cut
outer_face=Part.Face(Part.makePolygon([V(b.XMin,front,b.ZMin),V(b.XMax,front,b.ZMin),V(b.XMax,b.YMax,b.ZMin),V(b.XMin,b.YMax,b.ZMin),V(b.XMin,front,b.ZMin)]))
outer=Part.makeCompound(outer_face.Edges)
ligaments={}
for n,s in passages.items():ligaments[n+'_to_outer_mm']=s.distToShape(outer)[0]
keys=list(passages);ligaments['passport_to_passport_mm']=passages[keys[0]].distToShape(passages[keys[1]])[0]
min_ligament=min(ligaments.values())
check('load-bearing planar ligament remains at least two stock thicknesses',min_ligament>=2*c['stock_mm'])
shelf_passport_obstruction={}
for n,s in passages.items():
    lower=s.copy();lower.translate(V(0,0,-c['stock_mm']))
    shelf_passport_obstruction[n]=lower.common(shelf).Volume
lock_wood_margins=[]
for x in (120,480):
    for y in (lock_y[0],1188,lock_y[1]):
        bore=Part.makeCylinder(hole_radius,c['stock_mm'],V(x,y,b.ZMin))
        lock_wood_margins.append(min(bore.distToShape(outer)[0],*(bore.distToShape(s)[0] for s in passages.values())))
check('reference lock-access corridor retains 18 mm wood around potential bores',min(lock_wood_margins)>=18)

# Upright PLAY includes pane and cassette. Fold state explicitly removes both.
excluded=('Reserve','RESERVED','CandidatePayload','ServiceEnvelope')
zero_obstacles={n:s for n,s in play.items() if n!='PF_BackboxCheckEnvelope' and not any(k in n for k in excluded)}
zero_hits=hits(wood,zero_obstacles)
stationary={n:s for n,s in removed.items() if n.startswith('MX_')}
zero_valid=not zero_hits and not internal
check('upright zero passes all modeled unintended contacts',zero_valid)
check('only intentional floor-to-shelf surface contact remains',sum(r['volume_mm3'] for r in zero_hits)==0)

# Explicit structural classifications: channel material is not assumed wood.
wood_names=[n for n in removed if n in ('SIDE_L','SIDE_R','FRONT','REAR','FLOOR','BACKBOX_BASE','REAR_DOOR','PC_BASE','PF_BasePlywood','PF_WoodDowel','PF_OpenCradleL','PF_OpenCradleR','SSF_BST_Carrier')
    or n.startswith(('FLOOR_CLEAT_','CROSS_GUIDE_','CandidateLegBlock','SHELF_SUPPORT_'))
    or (n.startswith('SHELF_') and 'Candidate' not in n)
    or n in ('CROSS_1','CROSS_2','CROSS_3')]
cabwood={n:removed[n] for n in wood_names}
physical_other={n:s for n,s in removed.items() if n not in cabwood and n not in channels and n!='PF_BackboxCheckEnvelope' and not n.startswith('MX_')
    and not any(k in n.upper() for k in ('RESERVE','RESERVED','ENVELOPE','CANDIDATEPAYLOAD'))}
display={n:s for n,s in source.items() if roles.get(n)=='display_reserves' and n.startswith('Backglass')}
dmd={n:s for n,s in source.items() if roles.get(n)=='display_reserves' and n.startswith('DMD')}
def rotated(shapes,deg):
    result={n:s.copy() for n,s in shapes.items()}
    for s in result.values():s.rotate(axis,V(1,0,0),deg)
    return result
samples=[];first=None
if zero_valid:
    for deg in range(0,91,c['fold_step_deg']):
        moving=rotated(wood,deg)
        wh=hits(moving,cabwood);ch=hits(moving,channels);oh=hits(moving,physical_other)
        row={'angle_deg':deg,'A_wood_cabinet_wood':wh,'B_wood_glass_channels':ch,
             'other_physical_components':oh,'D_backglass_service_cabinet':hits(rotated(display,deg),{**cabwood,**channels,**physical_other}),
             'E_located_DMD_payload_cabinet':hits(rotated(dmd,deg),{**cabwood,**channels,**physical_other}),
             'minimum_structural_distance':minimum(moving,{**cabwood,**channels})}
        samples.append(row)
        if first is None and (wh or ch or oh):first=row
baseline_clear=zero_valid and first is None
matrix_samples=[]
if baseline_clear:
    for deg in range(91):matrix_samples.append({'angle_deg':deg,'hits':hits(rotated(wood,deg),stationary)})
matrix_conflict=any(x['hits'] for x in matrix_samples) if baseline_clear else None
eligible={str(a):baseline_clear or not any(s['angle_deg']<=a and (s['A_wood_cabinet_wood'] or s['B_wood_glass_channels'] or s['other_physical_components']) for s in samples) for a in (45,90)}
check('zero gate allows actual-wood 1 degree sweep',len(samples)==91)
check('no matrix support fold conclusion before valid baseline',baseline_clear or (not matrix_samples and matrix_conflict is None))

# Reference zones and contact faces are analysis geometry, not added hardware.
contexts={n:play[n] for n in ('SIDE_L','SIDE_R','REAR','BACKBOX_BASE','CandidateGlass','CandidateGlassChannelL','CandidateGlassChannelR','PF_BasePlywood','PLAYFIELD_ENVELOPE')}
pose_groups={'UPRIGHT':wood}
if first:pose_groups['FIRST_BOTTLENECK']=rotated(wood,first['angle_deg'])
for angle_key,ok in eligible.items():
    if ok:pose_groups['VALID_THROUGH_'+angle_key]=rotated(wood,int(angle_key))
groups={'wood':wood,'old_floor':{'OldBackboxFloorV14':old},'context':contexts,'matrix_stationary':stationary,
        'preserved_zones':zones,'display_reserves':{**display,**dmd},
        'bearing':{'OldBearingContact':old_contact,'NewBearingContact':new_contact},
        'coarse_reference_only':{'PF_BackboxCheckEnvelope':play['PF_BackboxCheckEnvelope']}}
groups['old_intersections']={r['obstacle']+'_OldIntersection':old.common(channels[r['obstacle']]) for r in old_hits}
if first:
    fp=pose_groups['FIRST_BOTTLENECK']; groups['first_intersections']={x['part']+'_'+x['obstacle']+'_FoldIntersection':fp[x['part']].common(({**cabwood,**channels,**physical_other})[x['obstacle']]) for x in first['A_wood_cabinet_wood']+first['B_wood_glass_channels']+first['other_physical_components']}
bundle={g:[mesh(n,s) for n,s in shapes.items()] for g,shapes in groups.items()}
clip=box(-120,950,440,840,410,960)
bundle['context_cutaway']=[mesh(n,s.common(clip)) for n,s in contexts.items() if s.common(clip).Volume>1e-6]
bundle['poses']={state:[mesh(n,s) for n,s in shapes.items()] for state,shapes in pose_groups.items()}
bundle['sections']={}
witness=new.distToShape(channels['CandidateGlassChannelL'])[1][0]
for x in (13,45,120,300,witness[0].x):
    sec={}
    for shapes in groups.values():
        for n,s in shapes.items():
            if s.Volume<1e-9:continue
            wires=s.slice(V(1,0,0),x)
            if wires:sec[n]=[[[p.y,p.z] for p in w.discretize(Deflection=.1)] for w in wires]
    if first:
        for n,s in pose_groups['FIRST_BOTTLENECK'].items():
            wires=s.slice(V(1,0,0),x)
            if wires:sec['Fold_'+n]=[[[p.y,p.z] for p in w.discretize(Deflection=.1)] for w in wires]
    bundle['sections'][str(x)]=sec
bundle['closest_section_x']=witness[0].x
bundle['plan_loops']={}
for g,shapes in groups.items():
    for n,s in shapes.items():
        if s.Volume>1e-9:
            bundle['plan_loops'][n]=[[[p.x,p.y] for p in w.discretize(Deflection=.1)] for w in s.slice(V(0,0,1),b.ZMin+9)]
(O/'mesh.json').write_text(json.dumps(bundle,separators=(',',':'))+'\n')

# Current proposed integration saved with every accepted PLAY component copied unchanged.
d=A.openDocument(str(R/c['source_play']))
for n,s in wood.items():
    o=d.addObject('PartDesign::Feature',n);o.Shape=s;o.addProperty('App::PropertyString','IntegrationRole');o.IntegrationRole='RECONSTRUCTED_BACKBOX_WOOD'
    if n=='BackboxFloorV32':
        for key,val in [('NominalStock',c['stock_mm']),('FrontDatumY',front),('ChannelTarget',5)]:
            o.addProperty('App::PropertyLength',key);setattr(o,key,val)
        o.addProperty('App::PropertyString','PartID');o.PartID='BB-FLOOR-V32-R1'
        o.addProperty('App::PropertyString','SourceConfiguration');o.SourceConfiguration='config/backbox_floor_v32.json'
coarse=d.getObject('PF_BackboxCheckEnvelope');coarse.addProperty('App::PropertyString','CollisionAuthority');coarse.CollisionAuthority='REFERENCE ONLY'
d.addProperty('App::PropertyString','BackboxIntegrationStatus');d.BackboxIntegrationStatus='ZERO VALID; FOLD '+('CLEAR' if baseline_clear else 'BLOCKED')+'; MANUFACTURING BLOCKED'
d.recompute();d.saveAs(str(O/'corrected-upright.FCStd'));A.closeDocument(d.Name)
for state,ss in pose_groups.items():
    if state=='UPRIGHT':continue
    d=A.newDocument('BackboxFloor_'+state)
    for n,s in {**removed,**ss}.items():
        if n=='PF_BackboxCheckEnvelope':continue
        o=d.addObject('PartDesign::Feature',n);o.Shape=s
    d.addProperty('App::PropertyString','PoseStatus');d.PoseStatus='COLLISION DIAGNOSTIC' if state=='FIRST_BOTTLENECK' else 'BASELINE VALID THROUGH '+state.rsplit('_',1)[-1]+' DEGREES'
    d.addProperty('App::PropertyString','Prerequisites');d.Prerequisites=', '.join(c['fold_prerequisites'])
    d.recompute();d.saveAs(str(O/(state.lower().replace('_','-')+'.FCStd')));A.closeDocument(d.Name)

reference_row=hinge['cabinet']['side_length_mm']-hinge['backbox']['hinge_floor_row_from_rear_mm_reference']
report={'source_head':c['source_head'],'checks':checks,'source_hashes':hashes,'floor':{
    'old_bounds_mm':bounds(old),'new_bounds_mm':bounds(new),'old_front_y_mm':b.YMin,'new_front_y_mm':front,
    'straight_edge_target_threshold_y_mm':threshold,'front_design_grid_mm':grid,'corner_only_trials':corner_trials,
    'profile':'full-width straight forward edge; no new notches, concave corners or dogbones',
    'material_removed_mm3':old.Volume-new.Volume,'material_removed_plan_area_mm2':(old.Volume-new.Volume)/c['stock_mm'],
    'old_volume_mm3':old.Volume,'new_volume_mm3':new.Volume,'stock_mm':c['stock_mm'],
    'minimum_channel_clearance':minimum({'floor':new},channels),'glass_clearance_mm':new.distToShape(play['CandidateGlass'])[0],
    'bearing_old_mm2':old_contact.Area,'bearing_new_mm2':new_contact.Area,'bearing_retained_percent':100*new_contact.Area/old_contact.Area,
    'continuous_bearing_width_mm':continuous_width,'old_side_joint_depth_mm':b.YLength,'new_side_joint_depth_mm':b.YMax-front,
    'side_joint_depth_retained_percent':100*(b.YMax-front)/b.YLength,'minimum_planar_ligament_mm':min_ligament,'ligaments':ligaments,
    'hinge_zones_preserved':True,'hinge_material_band_bounds_mm':{n:bounds(s) for n,s in zones.items() if n.startswith('Hinge')},
    'hinge_reference_row_y_mm':reference_row,'inherited_floor_edge_wood_beyond_reference_6_35_bore_mm':b.YMax-reference_row-6.35/2,
    'hinge_holes_released':False,'lock_zones_preserved':True,'lock_x_mm':[120,480],'lock_safe_center_y_interval_mm':lock_y,
    'lock_reference_access_diameter_mm':2*hole_radius,'lock_final_y_mm':None,'cable_zones_preserved':True,
    'minimum_wood_around_reference_lock_access_bore_mm':min(lock_wood_margins),
    'cable_passport_bounds_mm':{n:bounds(s) for n,s in passages.items()},
    'matching_current_shelf_passports_confirmed':not any(v>1e-6 for v in shelf_passport_obstruction.values()),
    'unchanged_shelf_under_floor_passport_obstruction_mm3':shelf_passport_obstruction,
    'minimum_channel_clearance_witness_xyz_mm':[[p.x,p.y,p.z] for p in witness],
    'structural_status':'Geometric load-path preservation, not strength certification. Substantial 18 mm wood retained; measured stock/hardware/load qualification pending.'},
    'zero':{'old_channel_hits':old_hits,'old_channel_volume_total_mm3':sum(x['volume_mm3'] for x in old_hits),
        'old_installed_glass_volume_mm3':old.common(play['CandidateGlass']).Volume,'new_hits':zero_hits,'new_unintended_volume_mm3':sum(x['volume_mm3'] for x in zero_hits),
        'internal_wood_hits':internal,'valid':zero_valid,'intentional_contact':'backbox-floor bottom ↔ rear-shelf top, positive contact area / zero penetration',
        'stationary_matrix_clearance':minimum({'floor':new},stationary)},
    'fold':{'performed':zero_valid,'step_deg':1,'prerequisites':c['fold_prerequisites'],'samples':samples,'baseline_clear':baseline_clear,
        'first_structural_collision':first,'minimum_structural_distance_mm':min(x['minimum_structural_distance']['mm'] for x in samples),
        'matrix_supports_evaluated':baseline_clear,'matrix_supports_new_conflict':matrix_conflict,'matrix_support_samples':matrix_samples,
        'review_45_90_eligible':eligible,'F_harness_keepout':'UNVERIFIED: no complete measured moving backbox harness in source; no invented route',
        'DMD_scope':'Located V27 190 x 55 x 90 payload; full V12 450 x 80 x 230 service placement unconfirmed'},
    'coarse_envelope_authority':'REFERENCE ONLY','manufacturing_ready':False}
check('all pre-task engineering, geometry and viewer bytes preserved',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
for name in ('LICENSE','NOTICE.md'):shutil.copyfile(R/name,O/name)
print('BACKBOX_FLOOR_PASS',len(checks),'ZERO',zero_valid,'FOLD',baseline_clear,'FIRST',first['angle_deg'] if first else None,flush=True)

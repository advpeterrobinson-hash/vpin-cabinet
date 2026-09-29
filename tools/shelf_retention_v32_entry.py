"""Separate shelf-retention proposal. Original material: CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import FreeCAD as A
import Part

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'exports/generated/side-panel-v32'
config_path = ROOT/'config/shelf_retention_v32.json'
cfg = json.loads(config_path.read_text())
motion_path = OUT/'motion-validation.json'
motion = json.loads(motion_path.read_text())
checks = []
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)})
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for name,value in motion['source_hashes'].items():
    if digest(ROOT/name) != value:raise RuntimeError('Stale motion evidence: '+name)
if not all(c['pass'] for c in motion['checks']):raise RuntimeError('Motion checks failed')
pose = motion['saved_poses'][0]
if digest(ROOT/pose['path']) != pose['sha256']:raise RuntimeError('Stale saved pose')
source = ROOT/'exports/generated/cabinet-v32/vpin-central-v32.FCStd'
inputs = [source, ROOT/pose['path'], motion_path, config_path, Path(__file__).resolve()]
input_hashes = {str(p.relative_to(ROOT)):digest(p) for p in inputs}
base_doc=A.openDocument(str(source))
pose_doc=A.openDocument(str(ROOT/pose['path']))
base = {o.Name:o.Shape.copy() for o in base_doc.Objects if hasattr(o,'Shape')}
# Reconstruct the loaded installed scene from the verified S1 staging pose.
route = next(r for r in motion['routes'] if r['name']==pose['route'])
undo = A.Vector(*[-v for v in route['legs'][0]['translation_mm']])
scene={o.Name:o.Shape.copy() for o in pose_doc.Objects if hasattr(o,'Shape')}
for name in route['moving']:scene[name].translate(undo)
for name in motion['config']['monitor_assembly']+motion['config']['crossmembers']:
    scene[name]=base[name].copy()
original={n:s.copy() for n,s in scene.items()}
axes, hardware, covers, cover_axes = [], {}, {}, []

def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,A.Vector(x,y,z))
def swept_bounds(shape,vector):
    """Conservative continuous AABB sweep for one-axis translation."""
    if sum(abs(v)>1e-8 for v in (vector.x,vector.y,vector.z)) != 1:
        raise ValueError('Only single-axis translations supported')
    b=shape.BoundBox
    return box(b.XMin+min(0,vector.x),b.YMin+min(0,vector.y),b.ZMin+min(0,vector.z),
               b.XLength+abs(vector.x),b.YLength+abs(vector.y),b.ZLength+abs(vector.z))
def hits(shapes,obstacles):
    result=[]
    for moving,s in shapes.items():
        for name,o in obstacles.items():
            if not s.BoundBox.intersect(o.BoundBox):continue
            vol=s.common(o).Volume
            if vol>cfg['collision_threshold_mm3']:result.append({'moving':moving,'obstacle':name,'mm3':vol})
    return result

for i in (1,2,3):
    shelf_name=f'SHELF_{i}'
    sb=scene[shelf_name].BoundBox
    payload_name=shelf_name+'_CandidatePayload'
    for side in ('L','R'):
        support_name=f'SHELF_SUPPORT_{i}{side}'
        old=scene[support_name].BoundBox
        xmin=18 if side=='L' else 582-cfg['support_width_mm']
        x=18+cfg['bolt_axis_inward_from_side_mm'] if side=='L' else 582-cfg['bolt_axis_inward_from_side_mm']
        support=box(xmin,old.YMin,old.ZMin,cfg['support_width_mm'],old.YLength,old.ZLength)
        cover_name=f'CandidateNutCover{i}{side}'
        cover=box(xmin,old.YMin,old.ZMin-cfg['cover_thickness_mm'],cfg['support_width_mm'],old.YLength,cfg['cover_thickness_mm'])
        for j,y_offset in enumerate(cfg['bolt_y_offsets_mm'],1):
            y=sb.YMin+y_offset
            prefix=f'CandidateShelfBolt{i}{side}{j}'
            r=cfg['clearance_bore_diameter_mm']/2
            scene[shelf_name]=scene[shelf_name].cut(cyl(x,y,sb.ZMin-1,r,sb.ZLength+2))
            support=support.cut(cyl(x,y,old.ZMin-1,r,old.ZLength+2))
            width=cfg['nut_pocket_width_mm']
            pocket=box(x-width/2,y-width/2,old.ZMin,width,width,cfg['nut_pocket_depth_mm'])
            support=support.cut(pocket)
            cover=cover.cut(cyl(x,y,old.ZMin-cfg['cover_thickness_mm']-1,cfg['cover_bolt_passage_diameter_mm']/2,cfg['cover_thickness_mm']+2))
            w=cfg['square_nut_width_mm']
            nut=box(x-w/2,y-w/2,old.ZMin+cfg['nut_bottom_clearance_mm'],w,w,cfg['square_nut_height_mm'])
            nut=nut.cut(cyl(x,y,old.ZMin,cfg['shaft_diameter_mm']/2,cfg['nut_pocket_depth_mm']+1))
            hardware[prefix+'Nut']=nut
            washer=cyl(x,y,sb.ZMax,cfg['washer_diameter_mm']/2,cfg['washer_thickness_mm']).cut(cyl(x,y,sb.ZMax-1,r,cfg['washer_thickness_mm']+2))
            hardware[prefix+'Washer']=washer
            head_z=sb.ZMax+cfg['washer_thickness_mm']
            shaft_z=head_z-cfg['shaft_length_mm']
            bolt=cyl(x,y,shaft_z,cfg['shaft_diameter_mm']/2,cfg['shaft_length_mm']).fuse(cyl(x,y,head_z,cfg['head_diameter_mm']/2,cfg['head_height_mm'])).removeSplitter()
            hardware[prefix]=bolt
            pb=scene[payload_name].BoundBox
            scene[payload_name]=scene[payload_name].cut(cyl(x,y,pb.ZMin-1,cfg['equipment_access_well_radius_mm'],pb.ZLength+2))
            axes.append({'shelf':shelf_name,'support':support_name,'bolt':prefix,'washer':prefix+'Washer','nut':prefix+'Nut',
                         'xyz_mm':[x,y,sb.ZMax],'head_top_z_mm':head_z+cfg['head_height_mm'],
                         'shelf_edge_ligament_mm':min(x-sb.XMin,sb.XMax-x,y-sb.YMin,sb.YMax-y)-r,
                         'support_side_ligament_mm':min(x-xmin,xmin+cfg['support_width_mm']-x)-r})
        # Bottom cover attachment locations only. Actual cover screws unselected.
        ix,iy=cfg['cover_fixing_insets_mm']
        for fx in (xmin+ix,xmin+cfg['support_width_mm']-ix):
            for fy in (old.YMin+iy,old.YMax-iy):
                hole=cyl(fx,fy,old.ZMin-cfg['cover_thickness_mm']-1,cfg['cover_fixing_bore_diameter_mm']/2,cfg['cover_thickness_mm']+cfg['cover_fixing_blind_depth_mm']+1)
                cover=cover.cut(hole)
                support=support.cut(hole)
                cover_axes.append({'cover':cover_name,'xyz_mm':[fx,fy,old.ZMin-cfg['cover_thickness_mm']-cfg['cover_head_allowance_mm']]})
        scene[support_name]=support
        covers[cover_name]=cover
scene.update(hardware)
scene.update(covers)
check('12 candidate bolt axes',len(axes)==12)
check('all proposal solids valid',all(s.isValid() and len(s.Solids)==1 for s in scene.values()))
changed={n for n in original if original[n].cut(scene[n]).Volume+scene[n].cut(original[n]).Volume>1e-4}
expected={f'SHELF_{i}' for i in (1,2,3)}|{f'SHELF_SUPPORT_{i}{side}' for i in (1,2,3) for side in ('L','R')}|{f'SHELF_{i}_CandidatePayload' for i in (1,2,3)}
check('only shelves supports and payload wells changed',changed==expected)
mirror=A.Matrix();mirror.A11=-1;mirror.A14=600
for i in (1,2,3):
    left=scene[f'SHELF_SUPPORT_{i}L'].transformGeometry(mirror)
    right=scene[f'SHELF_SUPPORT_{i}R']
    check(f'S{i} support mirror pair',left.cut(right).Volume+right.cut(left).Volume<1e-4)
# Physical candidate hardware must not consume the remaining payload allowance.
installed_conflicts=hits({n:scene[n] for n in set(hardware)|set(covers)}, {n:s for n,s in scene.items() if n not in set(hardware)|set(covers)})
check('candidate hardware clear of wood and remaining payload',not installed_conflicts)
# Check hardware against other hardware, avoiding self/duplicate comparisons.
items=list({**hardware,**covers}.items());hardware_conflicts=[]
for index,(name,shape) in enumerate(items):
    hardware_conflicts.extend(hits({name:shape},dict(items[index+1:])))
check('candidate hardware mutually clear',not hardware_conflicts)
removed=motion['config']['monitor_assembly']+motion['config']['crossmembers']
service={n:s for n,s in scene.items() if n not in removed}
access=[]
for axis in axes:
    x,y,z=axis['xyz_mm']
    exclude=[axis['bolt'],axis['washer']]
    obstacles={n:s for n,s in service.items() if n not in exclude}
    driver=cyl(x,y,axis['head_top_z_mm'],cfg['driver_radius_mm'],cfg['driver_length_mm'])
    driver_hits=hits({'driver':driver},obstacles)
    # Exact axial sweep for the coaxial cylindrical shaft/head and annular
    # washer. A whole-bolt box would falsely fill wood around its small bore.
    travel=cfg['bolt_withdrawal_mm']
    head_z=z+cfg['washer_thickness_mm']
    shaft_z=head_z-cfg['shaft_length_mm']
    bolt_sweep=cyl(x,y,shaft_z,cfg['shaft_diameter_mm']/2,cfg['shaft_length_mm']+travel).fuse(
        cyl(x,y,head_z,cfg['head_diameter_mm']/2,cfg['head_height_mm']+travel))
    washer_sweep=cyl(x,y,z,cfg['washer_diameter_mm']/2,cfg['washer_thickness_mm']+travel).cut(
        cyl(x,y,z-1,cfg['clearance_bore_diameter_mm']/2,cfg['washer_thickness_mm']+travel+2))
    withdraw={axis['bolt']:bolt_sweep,axis['washer']:washer_sweep}
    withdrawal_hits=hits(withdraw,obstacles)
    check(axis['bolt']+' axial driver space',not driver_hits)
    check(axis['bolt']+' complete upward withdrawal',not withdrawal_hits)
    check(axis['bolt']+' tip clears shelf',scene[axis['bolt']].BoundBox.ZMin+cfg['bolt_withdrawal_mm']>scene[axis['shelf']].BoundBox.ZMax)
    access.append({'bolt':axis['bolt'],'driver_conflicts':driver_hits,'withdrawal_conflicts':withdrawal_hits})
cover_access=[]
for index,axis in enumerate(cover_axes,1):
    x,y,z=axis['xyz_mm']
    probe=Part.makeCylinder(cfg['cover_driver_radius_mm'],cfg['cover_driver_length_mm'],A.Vector(x,y,z),A.Vector(0,0,-1))
    obstruction=hits({'cover_driver':probe},scene)
    check('cover attachment '+str(index)+' lower driver space',not obstruction)
    cover_access.append({'axis':axis,'conflicts':obstruction})
# Removed bolts and washers cannot be left in the horizontal-first path.
release_results=[]
for spec in motion['config']['shelf_routes']:
    name=spec['object'];moving_names=[name,name+'_CandidatePayload']+spec['removed_payload']
    relevant=[a for a in axes if a['shelf']==name]
    released=[n for a in relevant for n in (a['bolt'],a['washer'])]
    obstacles={n:s for n,s in service.items() if n not in moving_names+released}
    moving={n:scene[n].copy() for n in moving_names}
    dy=spec['stage_y_mm']-moving[name].BoundBox.YMin
    legs=[A.Vector(0,dy,0),A.Vector(0,0,606.9-moving[name].BoundBox.ZMin)]
    conflicts=[]
    for vec in legs:
        conflicts+=hits({n:swept_bounds(s,vec) for n,s in moving.items()},obstacles)
        for s in moving.values():s.translate(vec)
    check(name+' released shelf route remains clear',not conflicts)
    # A retained bolt must obstruct translation: tests positive engagement.
    retained_hit=scene[name].translated(A.Vector(0,1 if dy>0 else -1,0)).common(scene[relevant[0]['bolt']]).Volume
    check(name+' retained bolt rejects 1mm slide',retained_hit>cfg['collision_threshold_mm3'])
    release_results.append({'shelf':name,'released':released,'conflicts':conflicts,'retained_bolt_intersection_mm3':retained_hit})
# Preserve the two observed access failures from the initial layout as
# controls against actual saved obstacles, excluding hypothetical payloads.
rejected=[]
for label,x,y,z,names in [
    ('rear S1 at X42/Y245',42,245,177,['CandidateSideButtonL_255']),
    ('rear S2 at X42/Y725',42,725,197,['CROSS_GUIDE_2L'])]:
    conflict=hits({'driver':cyl(x,y,z,cfg['driver_radius_mm'],cfg['driver_length_mm'])},
                  {n:original[n] for n in names})
    check('reject initial '+label,bool(conflict))
    rejected.append({'layout':label,'conflicts':conflict})
# A missing equipment keepout must be rejected by the same driver check.
a=axes[0];x,y,z=a['xyz_mm'];driver=cyl(x,y,a['head_top_z_mm'],cfg['driver_radius_mm'],cfg['driver_length_mm'])
bb=scene[a['shelf']].BoundBox
filled=box(bb.XMin,bb.YMin,bb.ZMax,bb.XLength,bb.YLength,motion['config']['candidate_shelf_payload_height_mm'])
check('negative control filled tool well obstructs access',bool(hits({'driver':driver},{'filled_payload':filled})))
# Nut retention is verified geometrically; strength/threads remain unqualified.
for a in axes:
    nut=scene[a['nut']]
    rotated=nut.copy();rotated.rotate(A.Vector(*a['xyz_mm']),A.Vector(0,0,1),45)
    check(a['nut']+' pocket stops 45 degree turn',rotated.common(scene[a['support']]).Volume>cfg['collision_threshold_mm3'])
    cover=covers['CandidateNutCover'+a['shelf'][-1]+('L' if a['xyz_mm'][0]<300 else 'R')]
    check(a['nut']+' bottom cover intercepts dropped nut',nut.translated(A.Vector(0,0,-1)).common(cover).Volume>cfg['collision_threshold_mm3'])
# Save/reopen proposal and compare every exact shape and identity.
doc=A.newDocument('ShelfRetentionV32Proposal')
doc.Comment='CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; NOT manufacturing geometry'
for name,shape in scene.items():
    obj=doc.addObject('PartDesign::Feature',name);obj.Shape=shape
    obj.addProperty('App::PropertyString','PartCode');obj.PartCode=getattr(base_doc.getObject(name),'PartCode','') if base_doc.getObject(name) else ''
    if name.startswith('CandidateNutCover'):
        suffix=name.removeprefix('CandidateNutCover');obj.PartCode='S'+suffix[0]+'NutCover'+suffix[1]
    obj.addProperty('App::PropertyString','StudyStatus');obj.StudyStatus='PROPOSAL_NOT_RELEASED'
    obj.Label=(obj.PartCode or 'PROVISIONAL '+name)+' / retention study'
doc.recompute();path=OUT/'shelf-retention-proposal.FCStd';doc.saveAs(str(path));A.closeDocument(doc.Name)
doc=A.openDocument(str(path));doc.recompute()
actual={o.Name:o.Shape for o in doc.Objects if hasattr(o,'Shape')}
check('saved exact identity set',set(actual)==set(scene))
check('accepted nut-cover part codes preserved',all(doc.getObject(f'CandidateNutCover{i}{side}').PartCode==f'S{i}NutCover{side}' for i in (1,2,3) for side in ('L','R')))
check('saved valid single solids',all(s.isValid() and len(s.Solids)==1 for s in actual.values()))
check('saved shapes match proposal',all(actual[n].cut(s).Volume+s.cut(actual[n]).Volume<1e-4 for n,s in scene.items()))
check('source and prior evidence unchanged',all(digest(ROOT/n)==h for n,h in input_hashes.items()))
report={'status':'SHELF_RETENTION_PROPOSAL_ONLY','manufacturing_ready':False,'config':cfg,'source_hashes':input_hashes,
        'checks':checks,'axes':axes,'installed_conflicts':installed_conflicts,'hardware_conflicts':hardware_conflicts,
        'cover_access':cover_access,'rejected_initial_access':rejected,'access':access,'released_routes':release_results,'saved_proposal':{'path':str(path.relative_to(ROOT)),'sha256':digest(path),'solids':len(scene)},
        'changed_original_objects':sorted(changed),
        'limitations':['Candidate hardware envelopes only, threads and load/vibration performance unverified','Nut pockets require selected cutter corner relief and physical tolerance coupon','Cover screw bodies not modeled; 24 proposed attachment bores only','Driver is axial space, not full hand or insertion sweep','Conservative swept bounding boxes cover continuous one-axis motion; filled holes/wells may overestimate occupancy','Monitor/crossmember removal assumed from earlier packaging study, not safe handling approval']}
(OUT/'retention-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(c['pass'] for c in checks),[c for c in checks if not c['pass']]
print('SHELF_RETENTION_PASS',len(checks),'checks;',len(scene),'saved solids; hardware and CNC unverified')
for d in (doc,pose_doc,base_doc):A.closeDocument(d.Name)

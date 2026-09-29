"""Continuous translation service study; saved source read-only. CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import FreeCAD as A
import Part

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports/generated/side-panel-v32'
CONFIG_PATH = ROOT / 'config/side_motion_v32.json'
FRONT_CONFIG_PATH = ROOT / 'config/front_panel_v32.json'
SOURCE = ROOT / 'exports/generated/cabinet-v32/vpin-central-v32.FCStd'
FRONT = ROOT / 'exports/generated/front-panel-v32/coin-upgrade-closed.FCStd'
cfg = json.loads(CONFIG_PATH.read_text())
front_cfg = json.loads(FRONT_CONFIG_PATH.read_text())
paths = [SOURCE, FRONT, CONFIG_PATH, FRONT_CONFIG_PATH, Path(__file__).resolve()]
hashes = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
checks, routes, saved_poses = [], [], []
OUT.mkdir(parents=True,exist_ok=True)
def check(name, ok):
    checks.append({'check':name,'pass':bool(ok)})
def box(values):
    return Part.makeBox(*values[3:], A.Vector(*values[:3]))
def moved(shape, vector):
    result = shape.copy()
    result.translate(vector)
    return result

def translation_sweep(shape, vector):
    """Exact union of initial solid and translated boundary-face extrusions.

    For a polyhedron every newly occupied point crosses a boundary face.
    This covers all intermediate translations, not just sample positions.
    """
    if vector.Length <= 0:
        raise ValueError('Translation must be nonzero')
    if not shape.isValid() or len(shape.Solids) != 1:
        raise ValueError('Moving input must be one valid solid')
    pieces = [shape.copy(), moved(shape, vector)]
    for face in shape.Faces:
        if not isinstance(face.Surface, Part.Plane):
            raise ValueError('Continuous sweep accepts planar faces only')
        # A face extruded parallel to itself sweeps no volume.
        normal = face.normalAt(0,0)
        if abs(normal.dot(vector)) < 1e-8:
            continue
        piece = face.extrude(vector)
        if piece.Volume > 1e-8:
            pieces.append(piece)
    sweep = pieces[0].multiFuse(pieces[1:]).removeSplitter()
    if not sweep.isValid() or len(sweep.Solids) != 1:
        raise RuntimeError('Invalid continuous translation sweep')
    if shape.cut(sweep).Volume > 1e-5 or moved(shape, vector).cut(sweep).Volume > 1e-5:
        raise RuntimeError('Sweep omitted an endpoint')
    return sweep

def conflicts(sweeps, obstacles):
    result = []
    for moving_name, sweep in sweeps.items():
        for name, shape in obstacles.items():
            if not sweep.BoundBox.intersect(shape.BoundBox):
                continue
            volume = sweep.common(shape).Volume
            if volume > cfg['collision_threshold_mm3']:
                result.append({'moving':moving_name,'obstacle':name,'swept_intersection_mm3':volume})
    return result

base_doc = A.openDocument(str(SOURCE))
front_doc = A.openDocument(str(FRONT))
base_doc.recompute()
front_doc.recompute()
base = {o.Name:o.Shape.copy() for o in base_doc.Objects if hasattr(o,'Shape')}
front = {o.Name:o.Shape.copy() for o in front_doc.Objects if hasattr(o,'Shape')}
check('45 original saved solids',len(base)==45)
check('source documents recompute without invalid states', all(not any('Invalid' in str(state) or 'Error' in str(state) for state in o.State) for doc in (base_doc,front_doc) for o in doc.Objects))
check('all loaded solids valid',all(s.isValid() and len(s.Solids)==1 for s in list(base.values())+list(front.values())))
check('front study retains all base identities',set(base).issubset(front))
for name in base:
    if name in ('FRONT','PLUNGER_RESERVED'):
        continue
    check(name+' unchanged in front study',base[name].cut(front[name]).Volume+front[name].cut(base[name]).Volume < 1e-4)
scene = dict(front)
# The configured larger plunger reservation supersedes the saved visual marker.
scene['PLUNGER_RESERVED'] = box(front_cfg['plunger_internal_box'])
for i, button in enumerate(front_cfg['buttons'],1):
    scene['CandidateFrontButton'+str(i)] = Part.makeCylinder(
        front_cfg['button_internal_radius'],front_cfg['button_internal_depth_with_cable'],
        A.Vector(button['x'],18,button['z']),A.Vector(0,1,0))
b = cfg['side_button_probe']
for side,x,direction in [('L',18,1),('R',582,-1)]:
    for y in b['y_mm']:
        scene[f'CandidateSideButton{side}_{y}'] = Part.makeCylinder(
            b['radius_mm'],b['depth_mm'],A.Vector(x,y,b['z_mm']),A.Vector(direction,0,0))
monitor, crossmembers = cfg['monitor_assembly'],cfg['crossmembers']
for name in monitor+crossmembers+[r['object'] for r in cfg['shelf_routes']]:
    if name not in scene:
        raise RuntimeError('Missing configured moving object: '+name)

# Controls check the actual algorithm and collision routine, including an
# obstruction between clear endpoints that a two-position check would miss.
cube = Part.makeBox(10,10,10)
vector = A.Vector(0,0,40)
sweep = translation_sweep(cube,vector)
check('analytic cube sweep volume',abs(sweep.Volume-5000)<1e-5)
block = Part.makeBox(2,2,2,A.Vector(4,4,24))
check('negative control has clear endpoints',cube.common(block).Volume<1e-6 and moved(cube,vector).common(block).Volume<1e-6)
check('continuous sweep catches intermediate blocker',bool(conflicts({'cube':sweep},{'injected':block})))
check('translated blocker clears sweep',not conflicts({'cube':sweep},{'injected':moved(block,A.Vector(20,0,0))}))
try:
    translation_sweep(Part.makeCylinder(5,10),vector)
except ValueError:
    check('reject unsupported curved moving geometry',True)
else:
    check('reject unsupported curved moving geometry',False)

# A route is evaluated in full even when obstructed; it cannot be treated as an
# executable sequence unless every leg is clear against its retained scene.
def run_route(name, moving_names, removed_names, horizontal_dy=0):
    if set(moving_names) & set(removed_names):
        raise ValueError('Moving object also marked removed')
    missing = set(removed_names)-set(scene)
    if missing:
        raise ValueError('Unknown removals: '+str(missing))
    moving = {n:scene[n].copy() for n in moving_names}
    obstacles = {n:s for n,s in scene.items() if n not in set(moving_names+removed_names)}
    legs = []
    if horizontal_dy:
        legs.append(A.Vector(0,horizontal_dy,0))
    # Exit above every retained modeled object, not merely above the local rail.
    dz = max(s.BoundBox.ZMax for s in obstacles.values())+cfg['top_exit_margin_mm']-min(s.BoundBox.ZMin for s in moving.values())
    if dz <= 0:
        raise ValueError('Object already above scene')
    legs.append(A.Vector(0,0,dz))
    result = {'name':name,'moving':moving_names,'removed_before_route':removed_names,
              'legs':[],'status':'CLEAR_FOR_MODELED_TRANSLATION_ONLY'}
    for index,vec in enumerate(legs,1):
        sweeps = {n:translation_sweep(s,vec) for n,s in moving.items()}
        hits = conflicts(sweeps,obstacles)
        result['legs'].append({'leg':index,'translation_mm':[vec.x,vec.y,vec.z],
                              'conflicts':hits,'sweep_volumes_mm3':{n:s.Volume for n,s in sweeps.items()}})
        if hits:
            result['status']='OBSTRUCTED'
        moving = {n:moved(s,vec) for n,s in moving.items()}
        if index == 1 and name.endswith('_staged_with_payload'):
            # A review pose at the end of the horizontal leg, before lifting.
            # Save independent copies; never mutate the source document.
            pose_name = name.split('_staged_')[0]
            pose_doc = A.newDocument('ServicePose'+pose_name)
            pose_doc.Comment = 'CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet; candidate service pose only'
            expected = dict(obstacles)
            expected.update(moving)
            for obj_name,shape in expected.items():
                obj = pose_doc.addObject('PartDesign::Feature',obj_name)
                obj.Shape = shape.copy()
                obj.addProperty('App::PropertyString','StudyRole')
                obj.StudyRole = 'MOVING' if obj_name in moving else 'RETAINED'
                obj.addProperty('App::PropertyString','EvidenceStatus')
                obj.EvidenceStatus = 'CANDIDATE_SERVICE_POSE_NOT_MANUFACTURING'
                source_obj = base_doc.getObject(obj_name)
                obj.addProperty('App::PropertyString','PartCode')
                obj.PartCode = getattr(source_obj,'PartCode','') if source_obj else ''
                obj.addProperty('App::PropertyString','LegacyId')
                obj.LegacyId = obj_name
                obj.Label = (obj.PartCode or ('PROVISIONAL '+obj_name))+' ['+obj.StudyRole+']'
            pose_doc.recompute()
            pose_path = OUT/('service-stage-'+pose_name+'.FCStd')
            pose_doc.saveAs(str(pose_path))
            A.closeDocument(pose_doc.Name)
            reopened = A.openDocument(str(pose_path))
            reopened.recompute()
            actual = {o.Name:o.Shape for o in reopened.Objects if hasattr(o,'Shape')}
            check(pose_name+' saved pose identity set',set(actual)==set(expected))
            check(pose_name+' saved permanent identities',all(
                reopened.getObject(n).PartCode == (getattr(base_doc.getObject(n),'PartCode','') if base_doc.getObject(n) else '')
                and reopened.getObject(n).LegacyId == n for n in expected))
            check(pose_name+' saved pose valid single solids',all(s.isValid() and len(s.Solids)==1 for s in actual.values()))
            check(pose_name+' saved pose exact shapes',all(actual[n].cut(s).Volume+s.cut(actual[n]).Volume < 1e-4 for n,s in expected.items()))
            saved_poses.append({'route':name,'path':str(pose_path.relative_to(ROOT)),
                                'sha256':hashlib.sha256(pose_path.read_bytes()).hexdigest(),
                                'at_leg':index,'objects':len(expected)})
            A.closeDocument(reopened.Name)
    check(name+' final position above retained scene', min(s.BoundBox.ZMin for s in moving.values()) > max(s.BoundBox.ZMax for s in obstacles.values()))
    routes.append(result)
    print('MOTION_ROUTE',name,result['status'],flush=True)
    return result

run_route('monitor_vertical_teardown',monitor,[])
for name in crossmembers:
    run_route(name+'_assembled_lift',[name],[])
    run_route(name+'_after_monitor_lift',[name],monitor)
for spec in cfg['shelf_routes']:
    name = spec['object']
    removed = monitor+crossmembers
    run_route(name+'_direct_with_modeled_payload',[name],removed)
    run_route(name+'_staged_without_named_payload',[name],removed+spec['removed_payload'],
              spec['stage_y_mm']-scene[name].BoundBox.YMin)
# Loaded-shelf development envelope: all three candidate payloads remain in the
# scene; only the payload on the moving shelf (and its modeled audio) moves.
for spec in cfg['shelf_routes']:
    bounds = scene[spec['object']].BoundBox
    scene[spec['object']+'_CandidatePayload'] = Part.makeBox(
        bounds.XLength,bounds.YLength,cfg['candidate_shelf_payload_height_mm'],
        A.Vector(bounds.XMin,bounds.YMin,bounds.ZMax))
for spec in cfg['shelf_routes']:
    name = spec['object']
    moving_names = [name,name+'_CandidatePayload']+spec['removed_payload']
    for payload in spec['removed_payload']:
        check(payload+' enclosed by candidate payload',scene[payload].cut(scene[name+'_CandidatePayload']).Volume < 1e-5)
    run_route(name+'_staged_with_payload',moving_names,monitor+crossmembers,
              spec['stage_y_mm']-scene[name].BoundBox.YMin)
check('all source/config bytes unchanged',all(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p.relative_to(ROOT))] for p in paths))
check('expected 16 routes',len(routes)==16)
by_name = {r['name']:r for r in routes}
for name in cfg['required_clear_routes']:
    check(name+' required clear route',by_name[name]['status']=='CLEAR_FOR_MODELED_TRANSLATION_ONLY')
for name in cfg['required_obstructed_controls']:
    check(name+' expected obstruction retained',by_name[name]['status']=='OBSTRUCTED')
scene_bounds = {}
for name,shape in scene.items():
    b = shape.BoundBox
    scene_bounds[name] = [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
report = {'status':'CONTINUOUS_TRANSLATION_PACKAGING_ONLY','manufacturing_ready':False,
          'source_hashes':hashes,'saved_poses':saved_poses,'scene_bounds_mm':scene_bounds,'config':cfg,'checks':checks,'routes':routes,
          'method':'Union of starting/ending polyhedron and all nonzero-volume boundary-face extrusions; full continuous straight translation. No rotation or force validation.'}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(c['pass'] for c in checks),checks
print('SIDE_MOTION_PASS',len(checks),'checks;',len(routes),'routes; obstructions retained as findings')
A.closeDocument(front_doc.Name)
A.closeDocument(base_doc.Name)

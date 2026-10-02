# SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION
# Historical baseline/replay only. See studies/wpc-fold-v32/README.md; use original source HEAD for exact replay.
"""Read-only V32 route refinement / backbox zero-state audit. CERN-OHL-S-2.0.

Owns only matrix-route-backbox-audit-v32. Reconstructs documented backbox
wood in an isolated document; never upgrades old packaging to CURRENT geometry.
"""
from pathlib import Path
import hashlib
import json
import math
import shutil
import sys
import FreeCAD as A
import Part

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
V = A.Vector
cfg = json.loads((R / 'config/matrix_route_backbox_audit_v32.json').read_text())
src = R / cfg['source_directory']
out = R / cfg['output_directory']
out.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, ok):
    assert ok, name
    checks.append({'check': name, 'pass': True})


def read_cad(path):
    doc = A.openDocument(str(path))
    doc.recompute()
    shapes = {o.Name: o.Shape.copy() for o in doc.Objects if hasattr(o, 'Shape')}
    A.closeDocument(doc.Name)
    return shapes


def box(x, y, z, w, d, h):
    return Part.makeBox(w, d, h, V(x, y, z))


def bounds(s):
    # Vertex extrema avoid loose cached OCC bounding boxes after booleans.
    return [f(getattr(v.Point, k) for v in s.Vertexes) for k in 'xyz' for f in (min, max)]


def overlaps(moving, fixed):
    rows = []
    for n, s in moving.items():
        for m, t in fixed.items():
            if s.BoundBox.intersect(t.BoundBox):
                common = s.common(t)
                if common.Volume > 0.001:
                    rows.append({'part': n, 'obstacle': m, 'volume_mm3': common.Volume,
                                 'intersection_bounds_mm': bounds(common)})
    return rows


def range3(spec):
    start, stop, step = spec
    return [start + i * step for i in range(round((stop - start) / step) + 1)]


def translated(s, dy=0, dz=0):
    s = s.copy()
    s.translate(V(0, dy, dz))
    return s


inputs = list(src.glob('*')) + [R / 'exports/generated/viewer-v32/index.html']
inputs += [R / 'config' / n for n in ('matrix_cassette_v32.json', 'backbox_fold_v10.json',
           'structure_geometry_v14.json', 'cnc_detail_v25.json', 'owner_services_v27.json')]
hashes = {str(p.relative_to(R)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in inputs if p.is_file() and p.suffix not in ('.FCBak', '.FCStd1')}
installed = read_cad(src / 'play.FCStd')
removed = read_cad(src / 'matrix-removed.FCStd')
unlocked = read_cad(src / 'matrix-unlock.FCStd')
prior = json.loads((src / 'validation.json').read_text())['review']['matrix_cassette']
mc = json.loads((R / 'config/matrix_cassette_v32.json').read_text())
bb = installed['PF_BackboxCheckEnvelope']
pf = installed['PLAYFIELD_ENVELOPE']
y0, z0 = prior['carrier_front_xyz_mm'][1:]
angle = math.radians(mc['tilt_deg'])
pivot = V(300, y0 + mc['carrier_mm'][1] * math.cos(angle),
          z0 + mc['carrier_mm'][1] * math.sin(angle))
moving = {n: s.copy() for n, s in unlocked.items()
          if n.startswith('Matrix') or n in ('MX_MovingConnectorReserve', 'MX_CableLoopReserve')}
for s in moving.values():
    s.rotate(pivot, V(1, 0, 0), mc['rotation_forward_deg'])


def pose(rock):
    ps = {n: s.copy() for n, s in moving.items()}
    for s in ps.values():
        s.rotate(pivot, V(1, 0, 0), -rock)
    return ps


def screen(ps, rock, dy, dz, forward):
    panel = translated(ps['MatrixPanel1'], dy, dz)
    carrier = translated(ps['MatrixCarrier'], dy - forward, dz)
    a = panel.distToShape(bb)[0]
    b = carrier.distToShape(pf)[0]
    return {'rock_deg': rock, 'dy_mm': dy, 'dz_mm': dz, 'forward_sample_mm': forward,
            'panel_backbox_mm': a, 'carrier_playfield_mm': b, 'route_upper_bound_mm': min(a, b)}


# Follow the owner's preference order; do not modify accepted components for a failed screen.
search = cfg['search']
ps = pose(mc['rotation_forward_deg'])
stages = []
forward_rows = [screen(ps, 26, 0, 0, f) for f in search['forward_only_mm']]
z_rows = [screen(ps, 26, 0, dz, 68) for dz in range3(search['z_adjustment_mm'])]
yz_rows = []
all_rows = []
for rock in range3(search['rock_deg']):
    ps = pose(rock)
    rear = max(s.BoundBox.YMax for s in ps.values())
    for dy in range3(search['y_adjustment_mm']):
        forward = max(search['minimum_forward_mm'],
                      math.ceil(rear + dy - bb.BoundBox.YMin + cfg['route_target_mm']))
        for dz in range3(search['z_adjustment_mm']):
            row = screen(ps, rock, dy, dz, forward)
            all_rows.append(row)
            if rock == mc['rotation_forward_deg']:
                yz_rows.append(row)
for name, rows in [('1 forward only', forward_rows), ('2 Z only', z_rows),
                   ('3 Y with Z', yz_rows), ('4 rock with Y and Z', all_rows)]:
    best = max(rows, key=lambda r: r['route_upper_bound_mm'])
    stages.append({'stage': name, 'count': len(rows), 'best_upper_bound': best,
                   'target_candidates': sum(r['route_upper_bound_mm'] >= cfg['route_target_mm'] for r in rows)})
check('bounded small-change search does not reach 3 mm at required intermediate poses',
      all(s['target_candidates'] == 0 for s in stages))
check('baseline endpoint reproduces accepted bottleneck',
      abs(forward_rows[0]['route_upper_bound_mm'] - prior['route']['minimum_free_clearance_mm']) < 1e-6)
(out / 'route-screen.json').write_text(json.dumps({'stages': stages, 'forward_only': forward_rows,
    'z_only': z_rows, 'combined': all_rows}, separators=(',', ':')) + '\n')

# Regenerate only available source wood. Never call the legacy whole-cabinet pipeline.
from build_structure_v14 import main as build_structure
from owner_features_v27 import features
from build_owner_services_v27 import cut_shape
doc = A.newDocument('BackboxSourceAudit')
build_structure(doc)
wood = {o.Name: o.Shape.copy() for o in doc.Objects if hasattr(o, 'Shape') and
        o.Name.startswith(('BackboxFloor', 'BackboxLeftSide', 'BackboxRightSide',
                           'BackboxTop', 'BackboxRearFrame'))}
A.closeDocument(doc.Name)
raw_joint_overlaps = [r for r in overlaps(wood, wood) if r['part'] < r['obstacle']]
joint_ops = []


def remove(n, cut, mate):
    v = wood[n].common(cut).Volume
    if v <= 1e-5:
        return
    wood[n] = wood[n].cut(cut).removeSplitter()
    check('single valid source wood after joint: ' + n + '/' + mate,
          wood[n].isValid() and len(wood[n].Solids) == 1)
    joint_ops.append({'part': n, 'mate': mate, 'removed_mm3': v})


# Existing backbox-only recipe from detail_structure_v25.py, not a new joint design.
jc = json.loads((R / 'config/cnc_detail_v25.json').read_text())
t = jc['stock']['preview_main_mm']
depth = t * jc['fit']['capture_depth_fraction']
for n in ('BackboxFloorV14', 'BackboxTopV14'):
    b = wood[n].BoundBox
    remove(n, box(b.XMin-1, b.YMin-1, b.ZMin-1, t-depth+1, b.YLength+2, b.ZLength+2), 'BackboxLeftSideV14')
    remove(n, box(b.XMax-(t-depth), b.YMin-1, b.ZMin-1, t-depth+1, b.YLength+2, b.ZLength+2), 'BackboxRightSideV14')
    for side in ('Left', 'Right'):
        remove('Backbox'+side+'SideV14', wood[n], n)
for n in [n for n in wood if n.startswith('BackboxRearFrame')]:
    for m in ('BackboxFloorV14', 'BackboxTopV14', 'BackboxLeftSideV14', 'BackboxRightSideV14'):
        ov = wood[n].common(wood[m])
        if ov.Volume < 1e-5:
            continue
        b = ov.BoundBox
        limit = b.YMax - depth
        remove(n, box(b.XMin-1, b.YMin-1, b.ZMin-1, b.XLength+2,
                      max(.001, limit-b.YMin+1), b.ZLength+2), m)
        remove(m, wood[n], n)
for f in features():
    if f['part'] in wood:
        wood[f['part']] = wood[f['part']].cut(cut_shape(f)).removeSplitter()
wood_pairs = [r for r in overlaps(wood, wood) if r['part'] < r['obstacle']]
check('documented backbox joinery resolves nominal internal wood overlaps', not wood_pairs)
check('all eight reconstructed wood members are single valid solids',
      len(wood) == 8 and all(s.isValid() and len(s.Solids) == 1 for s in wood.values()))

# Current cabinet obstacles; independent structural / service / cassette namespaces.
# TV and coarse backbox are explicitly not classified as physical cabinet wood.
excluded = ('Envelope', 'Reserve', 'RESERVED', 'CandidatePayload', 'ServiceEnvelope')
physical = {n: s for n, s in removed.items() if n != 'PF_BackboxCheckEnvelope'
            and not n.startswith('MX_') and not any(k in n for k in excluded)}
stationary = {n: s for n, s in removed.items() if n.startswith('MX_')}
zero_hits = overlaps(wood, physical)
zero_support = overlaps(wood, stationary)
zero_coarse = overlaps({'PF_BackboxCheckEnvelope': bb}, physical)
check('zero-state blocker is specifically the two existing glass channels',
      {(r['part'], r['obstacle']) for r in zero_hits} ==
      {('BackboxFloorV14', 'CandidateGlassChannelL'), ('BackboxFloorV14', 'CandidateGlassChannelR')})
check('stationary matrix supports add no zero-state overlap', not zero_support)
check('route upper bottleneck also exists at reconstructed floor, not just empty coarse volume',
      abs(pose(26)['MatrixPanel1'].distToShape(wood['BackboxFloorV14'])[0]
          - forward_rows[0]['panel_backbox_mm']) < 1e-6)

hinge = json.loads((R / 'config/backbox_fold_v10.json').read_text())
cab = hinge['cabinet']
back = hinge['backbox']
axis = [cab['outer_width_mm']/2, cab['side_length_mm']-cab['pivot_from_rear_mm'], cab['pivot_from_bottom_mm']]
inset = (back['outer_width_mm'] - cab['outer_width_mm'] - 60.325)/2
check('reference axis and width datums retained', axis == [300, 1270, 508] and abs(inset-59.8375)<1e-9)
test = Part.Vertex(V(axis[0], axis[1], axis[2]+100))
test.rotate(V(*axis), V(1, 0, 0), 90)
check('positive reference-axis rotation folds toward player (-Y)', abs(test.Vertexes[0].Point.y-1170)<1e-6)

# Use existing located display/DMD packaging separately; do not invent a new DMD location.
oc = json.loads((R / 'config/owner_services_v27.json').read_text())['backbox']
envelopes = {'BackglassServiceEnvelope_SourceV27': box(*oc['display_box_mm']),
             'DMDPayloadEnvelope_SourceV27': box(*oc['dmd_box_mm'])}
front_carriers = {}
for side, spec in zip(('Left', 'Right'), oc['speaker_boxes_mm']):
    x, y, z, w, d, h = spec
    front_carriers['FrontSpeakerCarrier_SourceV27_'+side] = box(x, y-6, z, w, 6, h)
display_zero = overlaps({'display': envelopes['BackglassServiceEnvelope_SourceV27']}, physical)
dmd_zero = overlaps({'DMD': envelopes['DMDPayloadEnvelope_SourceV27']}, physical)
zero_valid = not zero_hits and not wood_pairs
check('invalid zero gate forbids a fold sweep', not zero_valid and cfg['fold_policy']['stop_on_invalid_zero'])
# Intentionally NO range(91) loop: the zero-degree sanity gate has failed.

contact_shapes = {f'Collision_{r["obstacle"]}': wood[r['part']].common(physical[r['obstacle']]) for r in zero_hits}
context_names = ('SIDE_L', 'SIDE_R', 'REAR', 'BACKBOX_BASE', 'PLAYFIELD_ENVELOPE', 'PF_BasePlywood',
                 'CandidateGlassChannelL', 'CandidateGlassChannelR', 'PF_WoodDowel', 'PF_OpenCradleL', 'PF_OpenCradleR')
context = {n: removed[n] for n in context_names}
references = {'ReferencePivotAxis': Part.makeCylinder(cab['pivot_hole_diameter_mm']/2, 840, V(-120, axis[1], axis[2]), V(1,0,0))}

# 45/90 are the requested static CAD illustrations only, not tested/approved fold states.
poses = {'UPRIGHT_ZERO_INVALID': wood}
for deg in cfg['fold_policy']['diagnostic_static_poses_deg']:
    poses[f'DIAGNOSTIC_{deg}_NOT_VALIDATED'] = {n: s.copy() for n, s in wood.items()}
    for s in poses[f'DIAGNOSTIC_{deg}_NOT_VALIDATED'].values():
        s.rotate(V(*axis), V(1,0,0), deg)


def mesh(n, s):
    vertices, faces = s.tessellate(.8)
    return {'name': n, 'vertices': [[v.x,v.y,v.z] for v in vertices], 'faces': [list(f) for f in faces]}


groups = {'wood': wood, 'cabinet_context': context, 'display_reserves': envelopes,
          'front_carriers_material_unconfirmed': front_carriers, 'stationary_matrix': stationary,
          'coarse_reference_only': {'PF_BackboxCheckEnvelope': bb}, 'reference_datums': references,
          'zero_intersections': contact_shapes}
bundle = {name: [mesh(n,s) for n,s in shapes.items()] for name,shapes in groups.items()}
bundle['static_poses'] = {state: [mesh(n,s) for n,s in shapes.items()] for state,shapes in poses.items()}
clip = box(-120, 950, 440, 840, 410, 960)
bundle['rear_context_cutaway'] = [mesh(n, s.common(clip)) for n,s in context.items()
                                  if s.common(clip).Volume > .001]
bundle['sections'] = {}
for x in (13,45,300):
    sections = {}
    for shapes in groups.values():
        for n,s in shapes.items():
            wires = s.slice(V(1,0,0),x)
            if wires:
                sections[n] = [[[p.y,p.z] for p in w.discretize(Deflection=.1)] for w in wires]
    bundle['sections'][str(x)] = sections
(out/'audit-mesh.json').write_text(json.dumps(bundle, separators=(',',':'))+'\n')
audit = A.newDocument('V32BackboxAudit_NotCurrentManufacturing')
for name, shapes in groups.items():
    group = audit.addObject('App::DocumentObjectGroup', name)
    for n, s in shapes.items():
        obj = audit.addObject('PartDesign::Feature', n)
        obj.Shape = s
        obj.addProperty('App::PropertyString', 'AuditRole')
        obj.AuditRole = name
        group.addObject(obj)
audit.addProperty('App::PropertyString', 'AuditStatus')
audit.AuditStatus = 'ZERO INVALID; SWEEP NOT PERMITTED; reconstructed source wood, not CURRENT release'
audit.recompute()
audit.saveAs(str(out/'backbox-source-audit.FCStd'))
A.closeDocument(audit.Name)
for state, shapes in poses.items():
    if state.startswith('DIAGNOSTIC'):
        doc = A.newDocument(state)
        for n, s in {**shapes, **context, **references}.items():
            obj = doc.addObject('PartDesign::Feature', n)
            obj.Shape = s
        doc.addProperty('App::PropertyString', 'AuditStatus')
        doc.AuditStatus = 'ILLUSTRATION ONLY. Invalid zero; no fold sweep or collision validation.'
        doc.recompute()
        doc.saveAs(str(out/(state.lower()+'.FCStd')))
        A.closeDocument(doc.Name)

report = {
    'source_head': cfg['source_head'], 'checks': checks, 'source_hashes': hashes,
    'matrix_route': {'changed': False, 'target_achieved': False, 'target_mm': cfg['route_target_mm'],
        'old_minimum_mm': prior['route']['minimum_free_clearance_mm'],
        'new_minimum_mm': prior['route']['minimum_free_clearance_mm'],
        'rock_deg': 26, 'forward_mm': 68, 'final_lift_mm': 100, 'gap_mm': mc['gap_mm'], 'tilt_deg':25,
        'visibility_min_percent': min(x['visible_percent'] for x in prior['visibility']),
        'stages': stages, 'custom_metal': 0,
        'limiting_pairs': [{'phase':'rock end', 'moving':'MatrixPanel1', 'obstacle':'BackboxFloorV14',
                            'clearance_mm':forward_rows[0]['panel_backbox_mm']},
                           {'phase':'forward end', 'moving':'MatrixCarrier', 'obstacle':'PLAYFIELD_ENVELOPE',
                            'clearance_mm':forward_rows[0]['carrier_playfield_mm']}],
        'scope': 'Bounded sampled refinement, not proof against every possible continuous compound route. No change adopted.'},
    'backbox': {
        'zero_actual_wood_assembly_valid': zero_valid,
        'internal_wood_joints_valid': not wood_pairs,
        'coarse_valid_as_wood_collision_authority': False,
        'classification': ['B', 'E', 'F'],
        'classification_notes': {'B':'Solid coarse box includes empty interior and mixes structural wood with service space.',
          'E':'Pre-V32 254 mm uniform-depth source floor has not been integrated with accepted V32 glass channels; not a 580 mm width error.',
          'F':'Reconstructed source floor physically overlaps both current modeled channels at zero. Channel material is unconfirmed; do not call this wood-to-wood without material authority.'},
        'axis_xyz_mm': axis, 'inset_mm': inset, 'cabinet_width_mm':600, 'backbox_width_mm':780,
        'raw_nominal_joint_overlaps': raw_joint_overlaps, 'reused_joint_operations': joint_ops,
        'zero_wood_pairs':wood_pairs, 'zero_wood_cabinet_hits':zero_hits,
        'zero_coarse_hits':zero_coarse, 'zero_display_hits':display_zero, 'zero_dmd_hits':dmd_zero,
        'zero_matrix_support_hits':zero_support,
        'sweep_executed':False, 'sweep_status':'STOPPED_AT_INVALID_ZERO',
        'first_wood_to_cabinet_collision_deg':0, 'first_wood_to_wood_fold_collision_deg':None,
        'wood_fold_clear':None, 'display_fold_clear':None, 'dmd_fold_clear':None,
        'harness_pinch_clear':None, 'stationary_support_new_fold_conflict':None,
        'stationary_support_zero_clearance_mm':min(s.distToShape(t)[0] for s in wood.values() for t in stationary.values()),
        'missing_authority': [
          'No integrated detailed backbox assembly in accepted V32: reconstruction uses build_structure_v14 plus backbox-only detail_structure_v25 joints and owner_features_v27 cuts.',
          'No defined fixed front structural wood; two source V27 speaker carrier plates are separate, material unconfirmed.',
          'Located V27 DMD payload 190 x 55 x 90 differs from V12 future service requirement 450 x 80 x 230; larger reserve lacks a confirmed location.',
          'No complete modeled moving backbox harness; 250 mm loop / R50 / 40 mm pinch keep-out are requirements, not a validated cable route.',
          'Physical 01-9011-L/R, 02-4352 and 4322-01139-12B measurements still required.'],
        'source_wood_inventory': {n:{'bounds_mm':bounds(s),'volume_mm3':s.Volume} for n,s in wood.items()},
        'static_diagnostic_angles_deg':[45,90], 'hinge_final_measurement_required':True
    },
    'accepted_geometry_modified':False, 'manufacturing_ready':False
}
check('accepted source and viewer bytes unchanged', all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hashes.items()))
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
for name in ('LICENSE','NOTICE.md'):
    shutil.copyfile(R/name,out/name)
print('ROUTE_BACKBOX_AUDIT_PASS',len(checks),'TARGET_NOT_ACHIEVED; ZERO_INVALID; NO_FOLD_SWEEP',flush=True)

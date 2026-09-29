"""Screen a proposed rear-axis opening; do not certify unmodeled props. CERN-OHL-S-2.0."""
import csv
import hashlib
import json
from pathlib import Path
import FreeCAD as A
import Part

R = Path(__file__).resolve().parents[1]
O = R / 'exports/generated/side-panel-v32'
source = O / 'simple-shelves-proposal.FCStd'
report_path = O / 'simple-shelves-validation.json'
config_path = R / 'config/shelf_service_pose_v32.json'
c = json.loads(config_path.read_text())
r = json.loads(report_path.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source) == r['saved_proposal']['sha256']
assert all(check['pass'] for check in r['checks'])
for name, expected in r['source_hashes'].items():
    assert sha(R / name) == expected, name
inputs = {str(p.relative_to(R)): sha(p) for p in (source, report_path, config_path, Path(__file__).resolve())}
doc = A.openDocument(str(source))
doc.recompute()
scene = {o.Name: o.Shape.copy() for o in doc.Objects if hasattr(o, 'Shape')}
moving_names = r['config']['playfield_assembly']
rail = scene['MONITOR_RAIL_L']
# The rear face has the highest mean Y; take its upper long edge midpoint.
rear = max(rail.Faces, key=lambda face: face.CenterOfMass.y)
edge = max(rear.Edges, key=lambda e: e.CenterOfMass.z)
pivot = A.Vector(300, edge.CenterOfMass.y, edge.CenterOfMass.z)

def hits(shapes, obstacles):
    found = []
    for name, shape in shapes.items():
        for other, obstacle in obstacles.items():
            if shape.BoundBox.intersect(obstacle.BoundBox):
                volume = shape.common(obstacle).Volume
                if volume > c['collision_threshold_mm3']:
                    found.append({'moving': name, 'obstacle': other, 'mm3': volume})
    return found

def rotated(angle):
    result = {n: scene[n].copy() for n in moving_names}
    for shape in result.values():
        shape.rotate(pivot, A.Vector(1, 0, 0), -angle)
    return result

def swept_box(shape, vector):
    b = shape.BoundBox
    return Part.makeBox(b.XLength + abs(vector.x), b.YLength + abs(vector.y), b.ZLength + abs(vector.z),
                        A.Vector(b.XMin + min(0, vector.x), b.YMin + min(0, vector.y), b.ZMin + min(0, vector.z)))

fixed = {n: s for n, s in scene.items() if n not in moving_names}
opening = []
for angle in range(0, max(c['opening_degrees']) + 1, c['sweep_step_degrees']):
    opening.append({'angle_deg': angle, 'conflicts': hits(rotated(angle), fixed)})
poses = []
for angle in c['opening_degrees']:
    raised = rotated(angle)
    ceiling = max(s.BoundBox.ZMax for s in raised.values()) + c['overhead_clearance_mm']
    tools = {}
    for axis in r['axes']:
        x, y, _ = axis['xyz_mm']
        z = axis['head_top_z_mm']
        tools[axis['bolt']] = Part.makeCylinder(r['config']['tool_radius_mm'], ceiling - z, A.Vector(x, y, z))
    routes = []
    for route in r['routes']:
        parts = {n: scene[n].copy() for n in route['moving']}
        conflicts = []
        for xyz in route['translations_mm']:
            v = A.Vector(*xyz)
            conflicts += hits({n: swept_box(s, v) for n, s in parts.items()}, raised)
            for shape in parts.values():
                shape.translate(v)
        routes.append({'shelf': route['shelf'], 'raised_assembly_conflicts': conflicts})
    poses.append({'opening_deg': angle, 'tool_column_conflicts': hits(tools, raised), 'routes': routes,
                  'sampled_opening_clear': not any(p['conflicts'] for p in opening if p['angle_deg'] <= angle),
                  'projected_profiles_yz': {n: [[v.Point.y, v.Point.z] for v in s.Vertexes] for n, s in raised.items()}})
# The closed display must block top access: protects against accidental omission.
closed_hits = hits(tools, rotated(0))
assert closed_hits, 'Negative control: closed display unexpectedly absent from tool check'
old_s3_tools = {f'old_S3_{x}_{y}': Part.makeCylinder(r['config']['tool_radius_mm'], ceiling-257, A.Vector(x, y, 257))
                for x in r['config']['bolt_x_mm'] for y in (1025, 1100)}
old_s3_hits = hits(old_s3_tools, rotated(100))
assert old_s3_hits, 'Negative control: previous S3 tool obstruction disappeared'
clear_poses = [p['opening_deg'] for p in poses if p['sampled_opening_clear'] and not p['tool_column_conflicts']
               and all(not route['raised_assembly_conflicts'] for route in p['routes'])]
assert clear_poses, 'No screened service pose clears; inspect audit before accepting layout'
assert all(s.isValid() for s in rotated(max(c['opening_degrees'])).values())
assert all(sha(R / name) == expected for name, expected in inputs.items())
with (O / 'shelf-hole-schedule-review.csv').open('w', newline='') as stream:
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(['status', 'shelf', 'support', 'x_global_mm', 'y_global_mm', 'y_from_shelf_front_mm', 'top_z_mm', 'shelf_through_diameter_mm', 'support_candidate_pocket_diameter_mm', 'support_candidate_pocket_depth_mm'])
    fronts = {f'SHELF_{s["number"]}': s['y_mm'] for s in r['config']['shelves']}
    for axis in r['axes']:
        x, y, z = axis['xyz_mm']
        writer.writerow(['REVIEW_ONLY_NOT_CNC', axis['shelf'], axis['support'], x, y, y-fronts[axis['shelf']], z,
                         r['config']['bore_diameter_mm'], r['config']['insert_bore_diameter_mm'], r['config']['insert_pocket_depth_mm']])
out = {'status': c['status'], 'manufacturing_ready': False, 'source_hashes': inputs,
       'pivot_xyz_mm': [pivot.x, pivot.y, pivot.z], 'config': c, 'sampled_opening': opening,
       'poses': poses, 'negative_control_closed_tool_conflicts': closed_hits,
       'negative_control_previous_s3_conflicts': old_s3_hits, 'clear_screened_opening_degrees': clear_poses,
       'scope': 'Adds raised assembly occupancy to previously checked shelf paths; assumed axis only. No prop/hinge/load certification. Opening sampled, not continuous.'}
(O / 'shelf-service-pose-screen.json').write_text(json.dumps(out, indent=2) + '\n')
A.closeDocument(doc.Name)
print('SHELF_POSE_AUDIT_PASS', 'poses', len(poses), 'opening samples', len(opening), 'hole rows', len(r['axes']))
for pose in poses:
    print('POSE', pose['opening_deg'], 'opening_clear', pose['sampled_opening_clear'], 'tool_hits', len(pose['tool_column_conflicts']), 'route_hits', [len(route['raised_assembly_conflicts']) for route in pose['routes']])

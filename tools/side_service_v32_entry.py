"""Read-only guide-anchor tool screen. Original material: CERN-OHL-S-2.0."""
import hashlib
import json
from types import SimpleNamespace
from pathlib import Path
import FreeCAD as A
import Part

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'exports/generated/cabinet-v32/vpin-central-v32.FCStd'
OUT = ROOT / 'exports/generated/side-panel-v32'
config = json.loads((ROOT / 'config/side_service_v32.json').read_text())
before = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
doc = A.openDocument(str(SOURCE))
doc.recompute()
checks, results = [], []
def check(name, passed):
    checks.append({'check': name, 'pass': bool(passed)})
def required(name):
    obj = doc.getObject(name)
    if obj is None or not hasattr(obj, 'Shape'):
        raise RuntimeError('Missing required solid: '+name)
    return obj

def hits(probe, objects):
    conflicts = []
    for obj in objects:
        volume = probe.common(obj.Shape).Volume
        if volume > config['collision_threshold_mm3']:
            conflicts.append({'object':obj.Name, 'intersection_mm3':volume})
    return conflicts

solids = [o for o in doc.Objects if hasattr(o, 'Shape')]
check('expected 45 saved solids', len(solids) == 45)
for removed in config['states'].values():
    for name in removed:
        required(name)
for i in (1, 2, 3):
    for side, direction in [('L',1), ('R',-1)]:
        guide = required(f'CROSS_GUIDE_{i}{side}')
        b = guide.Shape.BoundBox
        center_y = (b.YMin+b.YMax)/2
        # Source uses guide bottom = crossmember bottom -45.
        # Four side-anchor holes, separate from six support-height holes.
        for column in (-22,22):
            for level in (65,120):
                y, z = center_y+column, b.ZMin+level
                bore = Part.makeCylinder(2.75,20,A.Vector(b.XMin-1,y,z),A.Vector(1,0,0))
                check(f'{guide.Name} anchor {column}/{level} saved bore', guide.Shape.common(bore).Volume < 1e-5)
                x = b.XMax if side == 'L' else b.XMin
                for tool in config['tool_probes']:
                    probe = Part.makeCylinder(tool['radius_mm'],tool['inward_length_mm'],A.Vector(x,y,z),A.Vector(direction,0,0))
                    for state, removed in config['states'].items():
                        obstacles = [o for o in solids if o.Name != guide.Name and o.Name not in removed]
                        conflicts = hits(probe, obstacles)
                        results.append({'guide':guide.Name,'column_offset_mm':column,'level_above_guide_bottom_mm':level,
                                        'axis_origin_mm':[x,y,z], 'direction_x':direction,'tool':tool['name'],
                                        'state':state,'status':'OBSTRUCTED' if conflicts else 'CLEAR_FOR_PROBE_ONLY',
                                        'conflicts':conflicts})
# Independent injected obstruction verifies that collision screening can reject a blocked route.
probe = Part.makeCylinder(8,100,A.Vector(36,358,303.691375367901),A.Vector(1,0,0))
block = Part.makeBox(10,10,10,A.Vector(50,353,298.691375367901))
check('negative control detects injected obstruction', bool(hits(probe, [SimpleNamespace(Name='injected_block', Shape=block)])))
block.translate(A.Vector(0,100,0))
check('translated control clears probe', not hits(probe, [SimpleNamespace(Name='moved_block', Shape=block)]))
check('complete tool/state matrix', len(results) == 24*len(config['tool_probes'])*len(config['states']))
check('source bytes unchanged',hashlib.sha256(SOURCE.read_bytes()).hexdigest() == before)
summary = []
for tool in config['tool_probes']:
    for state in config['states']:
        selected = [r for r in results if r['tool']==tool['name'] and r['state']==state]
        summary.append({'tool':tool['name'],'state':state,'tested':len(selected),
                        'obstructed':sum(r['status']=='OBSTRUCTED' for r in selected),
                        'obstacle_objects':sorted({c['object'] for r in selected for c in r['conflicts']})})
report = {'status':'TOOL_SCREEN_ONLY','manufacturing_ready':False,'source_sha256':before,
          'config':config,'checks':checks,'summary':summary,'results':results}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'service-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(c['pass'] for c in checks),checks
print('SIDE_SERVICE_PASS',len(checks),'audit checks; obstructions are findings, not audit failures')
print(json.dumps(summary,indent=2))
A.closeDocument(doc.Name)

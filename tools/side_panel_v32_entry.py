"""Read-only saved-solid side interface audit. CERN-OHL-S-2.0."""
import hashlib
import json
from pathlib import Path
import FreeCAD as A
import Part

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'exports/generated/cabinet-v32/vpin-central-v32.FCStd'
OUT = ROOT / 'exports/generated/side-panel-v32'
OUT.mkdir(parents=True, exist_ok=True)
before = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
doc = A.openDocument(str(SOURCE))
doc.recompute()
checks = []
def check(name, result):
    checks.append({'check': name, 'pass': bool(result)})
def cylinder(x, y, z, radius, depth, direction=1):
    return Part.makeCylinder(radius, depth, A.Vector(x, y, z), A.Vector(direction, 0, 0))
def difference(a, b):
    return a.cut(b).Volume + b.cut(a).Volume
left = doc.getObject('SIDE_L').Shape
right = doc.getObject('SIDE_R').Shape
matrix = A.Matrix()
matrix.A11 = -1
matrix.A14 = 600
mirrored = left.transformGeometry(matrix)
check('saved sides mirror across X300', difference(mirrored, right) < 1e-4)
for name, x in [('SIDE_L', 0), ('SIDE_R', 582)]:
    shape = doc.getObject(name).Shape
    check(name + ' valid single solid', shape.isValid() and len(shape.Solids) == 1)
    bounds = shape.BoundBox
    check(name + ' nominal stock and profile bounds', all(abs(a-b) < 1e-6 for a,b in zip(
        [bounds.XMin, bounds.XLength, bounds.YLength, bounds.ZLength], [x,18,1308.1,596.9])))
    for y in [255,310]:
        check(f'{name} Y{y} through bore', shape.common(cylinder(x-1,y,270,7.9375,20)).Volume < 1e-5)
        outer = x if x == 0 else x+18-7.9375
        inner = x+18-4.7625 if x == 0 else x
        for label, start, depth in [('outer',outer,7.9375),('inner',inner,4.7625)]:
            check(f'{name} Y{y} {label} recess', shape.common(cylinder(start,y,270,14.2875,depth)).Volume < 1e-5)
        start = 7.9375 if x == 0 else 582+4.7625
        web = cylinder(start,y,270,14.2875,5.3).cut(cylinder(start,y,270,7.9375,5.3))
        check(f'{name} Y{y} 5.3mm annular web retained', abs(shape.common(web).Volume-web.Volume) < 1e-4)
    check(name + ' reference pivot bore', shape.common(cylinder(x-1,1270,508,6.35,20)).Volume < 1e-5)
# Candidate envelopes: radius18 and 60mm body +20mm cable are screening assumptions.
findings = []
for side,x,direction in [('left',18,1),('right',582,-1)]:
    for y in [255,310]:
        envelope = cylinder(x,y,270,18,80,direction)
        for obj in doc.Objects:
            if not hasattr(obj,'Shape') or obj.Name in ['SIDE_L','SIDE_R']:
                continue
            volume = envelope.common(obj.Shape).Volume
            if volume > .01:
                findings.append({'side':side,'button_y':y,'object':obj.Name,'intersection_mm3':volume})
# Ensure the symmetry comparison rejects positional drift, without modifying the document.
drift = right.copy()
drift.translate(A.Vector(0,1,0))
check('negative control rejects 1mm side drift', difference(mirrored, drift) > 1)
# Saved support footprints are occupied interfaces, not approved fastener zones.
# Bounding rectangles include guide grooves/holes; do not treat them as solid contact area.
support_pairs = [('SHELF_SUPPORT_'+str(i)+'L', 'SHELF_SUPPORT_'+str(i)+'R') for i in (1,2,3)]
support_pairs += [('CROSS_GUIDE_'+str(i)+'L', 'CROSS_GUIDE_'+str(i)+'R') for i in (1,2,3)]
support_pairs += [('FLOOR_CLEAT_18', 'FLOOR_CLEAT_552')]
footprints = []
for left_name, right_name in support_pairs:
    objects = [doc.getObject(n) for n in (left_name, right_name)]
    if any(o is None for o in objects):
        raise RuntimeError('Missing side support pair: '+str((left_name, right_name)))
    check(left_name+' / '+right_name+' mirrored support geometry',
          difference(objects[0].Shape.transformGeometry(matrix), objects[1].Shape) < 1e-4)
    for obj, side, face in zip(objects, ('left','right'), (18.,582.)):
        b = obj.Shape.BoundBox
        check(obj.Name+' reaches inner side datum', abs((b.XMin if side=='left' else b.XMax)-face) < 1e-6)
        footprints.append({'object':obj.Name, 'side':side, 'inner_face_x_mm':face,
                           'y_mm':[b.YMin,b.YMax], 'z_mm':[b.ZMin,b.ZMax],
                           'inward_extent_mm':b.XLength})
check('source bytes unchanged', hashlib.sha256(SOURCE.read_bytes()).hexdigest() == before)
report = {'status':'SAVED_SIDE_AUDIT_ONLY','manufacturing_ready':False,
          'source_sha256':before,'checks':checks,'candidate_button_envelope':{'radius_mm':18,'body_mm':60,'cable_mm':20,'hardware_verified':False},
          'candidate_envelope_conflicts':findings,'remaining_mounting_web_mm':5.3,
          'side_support_bounding_footprints':footprints,
          'footprint_scope':'Existing shelf supports, crossmember guides and floor cleats only. Rectangles are occupied bounds, not fastener approval or structural contact area. Shell joints and missing hardware excluded.',
          'pivot_reference_edge_ligaments_mm':{'rear':31.75,'top':82.55},
          'unverified':['selected buttons and mounting stack','leg brackets and access','SSF and feedback mounts','glass channel and lockdown datum','captive props and display load path','backbox pivot hardware','accepted shell joinery']}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(c['pass'] for c in checks), checks
print('SIDE_REVIEW_PASS',len(checks),'checks;',len(findings),'candidate envelope conflicts; CNC BLOCKED')
A.closeDocument(doc.Name)

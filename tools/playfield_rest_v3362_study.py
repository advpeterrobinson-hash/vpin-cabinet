"""Native, isolated T1 landing study; never modifies CURRENT. CERN-OHL-S-2.0.

The two shoe concepts are proposals only. Neither closes attachment, uplift
restraint, stock fit or strength qualification. No final holes are generated.
"""
from pathlib import Path
import gzip, hashlib, json, math, sys
import FreeCAD as A, Part, MeshPart

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
from backbox_lock_integration_v32 import load, actual, pf_names, PF, transform
V = A.Vector
SOURCE = R / 'exports/generated/playfield-rest-v3362/play.FCStd'
O = R / 'exports/generated/playfield-rest-v3362/t1-rest-study'
O.mkdir(parents=True, exist_ok=True)
(O / 'brep').mkdir(exist_ok=True)
source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
p = load(SOURCE)
base, t1 = p['PF_BasePlywood'], p['CROSS_1']
physical = actual(p)
moving = {n: s for n, s in physical.items() if n in pf_names(p)}
fixed = {n: s for n, s in physical.items() if n not in moving and n != 'CandidateGlass'}


def bounds(s):
    b = s.BoundBox
    return [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]


def planar_face(s, up=True):
    return max([f for f in s.Faces if type(f.Surface).__name__ == 'Plane'
                and (f.normalAt(0, 0).z > .5 if up else f.normalAt(0, 0).z < -.5)], key=lambda f: f.Area)


def plane_z(f, y, x=300):
    n, c = f.normalAt(0, 0), f.CenterOfMass
    return c.z - (n.x * (x - c.x) + n.y * (y - c.y)) / n.z


def pair(a, b):
    d, points, _ = a.distToShape(b)
    return {'distance_mm': d, 'penetration_mm3': a.common(b).Volume,
            'witnesses': [[list(u), list(v)] for u, v in points[:2]]}


def hits(shape, objects, ignore=()):
    out = []
    for n, s in objects.items():
        if n in ignore or not shape.BoundBox.intersect(s.BoundBox):
            continue
        vol = shape.common(s).Volume
        if vol > 1e-4:
            out.append({'part': n, 'penetration_mm3': vol})
    return out


def profile(x, yz):
    vv = [V(x, y, z) for y, z in yz]
    return Part.Face(Part.makePolygon(vv + [vv[0]])).extrude(V(18, 0, 0))


bottom = planar_face(base, False)
top = planar_face(t1)
normal = top.normalAt(0, 0)
y0, y1 = t1.BoundBox.YMin, t1.BoundBox.YMax
vertical_gap = plane_z(bottom, (y0 + y1) / 2) - plane_z(top, (y0 + y1) / 2)
report = {
    'source': str(SOURCE.relative_to(R)), 'source_sha256': source_hash,
    'status': 'HELD_PROPOSALS_ONLY_NOT_CURRENT_GEOMETRY', 'selected': False,
    'manufacturing_release': False, 'CAD_pose_is_not_closed_pitch_retention': True,
    'datum_changes': [], 'new_holes': [], 'new_purchased_hardware': [],
    'rear_axis_mm': list(PF), 'base_to_crossmembers': {}, 'rear_dowel_contacts': {},
    'normal_gap_mm': vertical_gap * normal.z, 'vertical_gap_mm': vertical_gap,
    'plywood_density_kg_m3': 650, 'concepts': {},
    'history': 'The 22 mm gap follows inherited crossmember tops sized for old monitor-rail underside -36 versus present base underside -14. Landing pads were already absent in the V32 service-correction source; do not attribute their loss specifically to the dowel commit.',
    'scope': 'Exact contact and geometric motion screen only. Not structural or ergonomic certification.',
    'holds': ['Owner selection of front landing architecture',
              'Positive removable attachment of shoes to T1; no SKU or drilling selected',
              'Positive closed-state uplift/vibration retention',
              'Stock-thickness + coupon-clearance fit and R2 mating-corner strategy',
              'Front-overhang and bearing/fastener structural qualification']
}
for name in ['CROSS_1', 'CROSS_2', 'CROSS_3']:
    face = planar_face(p[name]); y = face.CenterOfMass.y
    report['base_to_crossmembers'][name] = {
        **pair(base, p[name]), 'bearing_area_mm2': bottom.common(face).Area,
        'sample_y_mm': y, 'crossmember_top_z_at_same_y_mm': plane_z(face, y),
        'base_bottom_z_at_same_y_mm': plane_z(bottom, y),
        'vertical_gap_at_same_y_mm': plane_z(bottom, y) - plane_z(face, y)}
for name in ['PF_OpenCradleL', 'PF_OpenCradleR']:
    report['rear_dowel_contacts'][name] = pair(p['PF_WoodDowel'], p[name])
report['rear_dowel_explanation'] = 'Real tangent seat contact exists, but a freely rotating dowel does not set closed pitch. Current lacks a modeled front landing and positive closed retention.'
report['front_panel_to_base'] = pair(base, p['FRONT'])
report['T1_front_lever_y_mm'] = PF.y - (y0 + y1) / 2
report['T1_to_base_front_y_mm'] = (y0 + y1) / 2 - base.BoundBox.YMin

shapes = {}
for kind in ['compact_pad', 'captured_shoe']:
    members = []
    for side, x in [('L', 125), ('R', 457)]:
        if kind == 'compact_pad':
            yz = [(y0, plane_z(top, y0)), (y1, plane_z(top, y1)),
                  (y1, plane_z(bottom, y1)), (y0, plane_z(bottom, y0))]
        else:
            # A single planar piece with an open-bottom capture. Nominal contact
            # uses the exact T1 faces; manufacturing fit remains late-bound.
            a, b = y0 - 18, y1 + 18
            yz = [(a, plane_z(top, a) - 18), (y0, plane_z(top, y0) - 18),
                  (y0, plane_z(top, y0)), (y1, plane_z(top, y1)),
                  (y1, plane_z(top, y1) - 18), (b, plane_z(top, b) - 18),
                  (b, plane_z(bottom, b)), (a, plane_z(bottom, a))]
        shape = profile(x, yz)
        name = 'HELD_' + kind + '_' + side
        shapes[name] = shape
        shape.exportBrep(str(O / 'brep' / (name + '.brep')))
        actual_upper = planar_face(shape)
        upper_common = actual_upper.common(bottom).Area
        # Summing face-to-face common areas also finds the recessed crown of
        # the open-bottom shoe; solid/common area is not a bearing-area test.
        lower_common = sum(f.common(top).Area for f in shape.Faces)
        service = []
        for ang in sorted(set([0, .001, .01, .1, .25, .5] + list(range(1, 51)))):
            pose = transform(moving, angle=-ang, axis=PF)
            service.append({'angle_deg': ang, 'penetrations': hits(shape, pose),
                            'base_separation_mm': pose['PF_BasePlywood'].distToShape(shape)[0]})
        lifts = []
        for lift in [0, .01, .1] + list(range(1, 49)):
            pose = transform(moving, lift=lift)
            lifts.append({'lift_mm': lift, 'penetrations': hits(shape, pose),
                          'base_separation_mm': pose['PF_BasePlywood'].distToShape(shape)[0]})
        members.append({
            'name': name, 'brep': str((O / 'brep' / (name + '.brep')).relative_to(R)),
            'valid': shape.isValid(), 'solid_count': len(shape.Solids),
            'bounds_mm': bounds(shape), 'volume_mm3': shape.Volume,
            'mass_kg': shape.Volume * 650 / 1e9,
            'nominal_stock_thickness_mm': 18, 'stock_axis': 'X',
            'top_bearing_area_mm2': upper_common, 'T1_bearing_area_mm2': lower_common,
            'base_contact': pair(shape, base), 'T1_contact': pair(shape, t1),
            'other_fixed_collisions': hits(shape, fixed, ['CROSS_1']),
            'service_samples': service, 'lift_samples': lifts,
            'operation_plan': 'One planar Y-Z outline extruded 18 mm; through profile from FACE A only. No holes frozen.',
            'fit': 'PARAMETRIC_HOLD: measured T1 stock plus coupon clearance; current shape is zero-clearance contact study, NOT a released cut outline.' if kind == 'captured_shoe' else 'Gap height must be regenerated for actual stock and assembly datum.',
            'notch_corner': 'Mating corners need coupon-selected dogbone/T-bone or manual finish; no automatic relief generated.' if kind == 'captured_shoe' else 'Open outer corners; no internal cut corner.',
            'attachment_status': 'UNSELECTED; geometry alone is not positive attachment or uplift retention'
        })
    report['concepts'][kind] = {
        'status': 'HELD_NOT_PROMOTED', 'members': members,
        'pair_upper_bearing_mm2': sum(m['top_bearing_area_mm2'] for m in members),
        'pair_T1_bearing_mm2': sum(m['T1_bearing_area_mm2'] for m in members),
        'pair_mass_kg': sum(m['mass_kg'] for m in members),
        'new_stock_family': False, 'nominal_stock_mm': 18,
        'functional_reason': 'Two front landings plus the rear dowel establish closed pitch; separate positive retention is still required.',
        'collision_screen': 'Sampled service 0–50 degrees (1-degree plus fine initial samples), lift 0–48 mm (1-mm plus fine initial samples). Intentional zero-gap bearing at PLAY.',
        'not_a_continuous_clearance_certificate': True}

gates = {
    'actual_gaps_22_normal': all(abs(v['distance_mm'] - 22) < 1e-6 for v in report['base_to_crossmembers'].values()),
    'no_existing_crossmember_bearing': all(v['bearing_area_mm2'] < 1e-6 for v in report['base_to_crossmembers'].values()),
    'rear_dowel_actual_contact': all(v['distance_mm'] < 1e-6 and v['penetration_mm3'] < 1e-5 for v in report['rear_dowel_contacts'].values()),
    'all_proposals_valid_single_solids': all(m['valid'] and m['solid_count'] == 1 for c in report['concepts'].values() for m in c['members']),
    'all_proposals_have_true_top_and_lower_bearing': all(m['top_bearing_area_mm2'] > 300 and m['T1_bearing_area_mm2'] > 300 for c in report['concepts'].values() for m in c['members']),
    'no_unintended_fixed_collision': all(not m['other_fixed_collisions'] and m['base_contact']['penetration_mm3'] < 1e-5 and m['T1_contact']['penetration_mm3'] < 1e-5 for c in report['concepts'].values() for m in c['members']),
    'sampled_service_and_lift_clear': all(not s['penetrations'] for c in report['concepts'].values() for m in c['members'] for s in m['service_samples'] + m['lift_samples']),
    'source_bytes_unchanged': hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash,
    'no_promotion': report['selected'] is False and not report['manufacturing_release']
}
report['gates'] = gates
(O / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
assert all(gates.values()), gates

doc = A.newDocument('T1RestProposals_HELD')
for name, shape in {'CURRENT_PF_BasePlywood': base, 'CURRENT_T1': t1,
                    'CURRENT_Dowel': p['PF_WoodDowel'], **shapes}.items():
    obj = doc.addObject('PartDesign::Feature', name); obj.Label = name; obj.Shape = shape
doc.recompute(); doc.saveAs(str(O / 'study.FCStd'))


def clipped(s, x0, x1, y0, y1, z0, z1):
    return s.common(Part.makeBox(x1-x0, y1-y0, z1-z0, V(x0, y0, z0)))


def edges(s):
    return [[list(v) for v in e.discretize(Deflection=.1)] for e in s.Edges]


def panel(label, objects, view, annotations=None, edgeset=None, alpha=None):
    meshes = []
    for name, shape in objects.items():
        mm = MeshPart.meshFromShape(Shape=shape, LinearDeflection=.3, AngularDeflection=.4, Relative=False)
        vv, ff = mm.Topology
        color = '#ba682e' if name.startswith('HELD') else '#bcaa8d' if 'Base' in name else '#577681'
        meshes.append({'name': name, 'vertices': [list(v) for v in vv], 'faces': ff,
                       'color': color, 'alpha': (alpha or {}).get(name, 1)})
    return {'label': label, 'meshes': meshes, 'view': view,
            'annotations': annotations or [], 'edges': edgeset or []}


base_slice = clipped(base, 110, 155, 330, 430, 300, 450)
t1_slice = clipped(t1, 110, 155, 330, 430, 330, 450)
shoe = shapes['HELD_captured_shoe_L']
scenes = [
    {'id': '01', 'title': 'T1 landing proposal — current gap and captured shoes',
     'panels': [panel('CURRENT: no front landing at T1', {'Base': base_slice, 'T1': t1_slice}, (-1, 0, 0),
                       [{'point': [125, 380, plane_z(top, 380)+11], 'text': '22.000 normal gap\n22.333 vertical gap', 'offset': [-170, 30]}]),
                panel('HELD: two planar 18 mm shoes', {'Base': clipped(base, 75, 525, 300, 455, 300, 500),
                      'T1': t1, **{n:s for n,s in shapes.items() if 'captured_shoe' in n}}, (1, -1.4, -.8),
                      [{'point': [134, 380, plane_z(top, 380)+12], 'text': 'HELD — not selected', 'offset': [-65, -45]}],
                      alpha={'Base': .35})],
     'legend': ['Tan: current base', 'Blue: unchanged T1', 'Orange: HELD shoes'],
     'note': 'Rear dowel bearing exists but does not set closed pitch. Current T1/T2/T3 each have a 22 mm normal gap. Shoes are a geometry proposal only: attachment, closed uplift retention, coupon fit and structural qualification remain unresolved. No CURRENT part is changed.'},
    {'id': '02', 'title': 'Captured T1 shoe — exact bearing and service release',
     'panels': [panel('Left profile: open-bottom nominal capture', {'Base': base_slice, 'T1': t1_slice, 'HELD_shoe': shoe}, (-1, 0, 0),
                      [{'point': [125, 360, plane_z(bottom, 360)], 'text': '54 mm top profile\n18 mm stock in X', 'offset': [-50, 55]},
                       {'point': [125, 380, plane_z(top, 380)], 'text': 'T1 seat: 328.904 mm² / shoe\nNotch fit + R2 relief HOLD', 'offset': [-155, -95]}],
                      edgeset=[{'lines': edges(shoe), 'color': '#793915', 'width': 1.2}]),
                panel('Service 1°: landing releases without scraping',
                      {'Base': transform({'base':base_slice}, angle=-1, axis=PF)['base'], 'T1': t1_slice, 'HELD_shoe':shoe}, (-1, 0, 0),
                      [{'point': [125, 380, plane_z(bottom, 380)+6], 'text': 'Clean release\nSampled 0–50° / lift 48 mm', 'offset': [-125, 75]}])],
     'legend': ['Native B-rep triangles', 'Installed reference = 0 clearance', 'Production notch NOT frozen'],
     'note': 'One planar profile per side, cut through 18 mm stock from one face. The wider crown and two 18 mm legs avoid tiny loose pads, but still require positive attachment to T1 and separate closed-state retention. The nominal notch is not a final tool-compatible cutting outline.'}
]
(O / 'review-scenes.json.gz').write_bytes(gzip.compress(json.dumps(scenes, separators=(',', ':')).encode(), mtime=0))
(O / 'README.md').write_text('''# HELD T1 landing study — not CURRENT geometry

The rear wooden dowel has true tangent bearing in both cradle seats. It does not fix the playfield pitch. CURRENT has no modeled front landing: the base is 22 mm normal / 22.333 mm vertical above T1, T2 and T3. The vertical value is measured at the same Y on the two inclined faces.

Two isolated concepts are supplied: compact 18 × 18 mm pads, and broader captured shoes. Each captured shoe is a single 18 mm plywood profile, 54 mm along Y, with an open-bottom nominal T1 capture and two 18 mm legs. It therefore needs no 22 mm sheet stock. The exact native bearing and sampled motion data are in `result.json`; the proposal CAD is `study.FCStd`.

Neither concept is selected or promoted. No screw, hole or purchased part has been invented. Positive shoe attachment, positive closed-state uplift retention, coupon-selected fit, R2 mating-corner treatment and structural qualification remain HOLD. The shown zero-clearance capture is a contact study, not a production outline. A pair of shoes does not alone resolve all closed-state retention requirements.

The inherited crossmember tops correspond to the obsolete monitor-rail underside (local −36), while the present base underside is local −14. Landing pads were already absent from the V32 service-correction source. The loss must not be assigned specifically to the dowel change.

No strength certification is claimed from contact area. T1 is approximately 655 mm forward of the rear axis; the base still projects about 316 mm in front of T1. That overhang requires qualification. A support near the lockdown/front would require a separate projecting structure and a new clearance study; no front candidate is validated here.

Full-sheet CNC and physical cabinet release remain blocked.
''')
print('V3362_T1_REST_STUDY_PASS', len(gates), flush=True)

"""Owner supplier profile, one-face release gate and original SVG coupon.

CERN-OHL-S-2.0. Does not change CURRENT wood or emit CNC machine code.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / 'config/manufacturing/profiles/peter_supplier_v1.json'
OUT = ROOT / 'exports/generated/manufacturing-peter-v1'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def fingerprint(p):
    # Include all measured inputs and planned machining; exclude subsequent results.
    c = {k: v for k, v in p['coupon'].items() if k not in {
        'validation_status', 'selected_fit_clearance_mm', 'accepted_corner_strategy',
        'validated_package_sha256', 'results'}}
    return hashlib.sha256(json.dumps([p['machine'], p['stock'], p['tooling'], c],
                                    sort_keys=True).encode()).hexdigest()


def validate_profile(p, measured=False):
    m, s, t, c = (p[k] for k in ('machine', 'stock', 'tooling', 'coupon'))
    require(m['machining_faces'] == 1 and m['two_sided_machining'] is False
            and m['flip_operations_allowed'] is False, 'One-face rule is mandatory')
    require(s['sheet_mm'] == [2500, 1600] and m['table_mm'] == [2000, 3000], 'Unexpected supplier table/sheet')
    require(s['sheet_to_table_axes'] == [1, 0], 'Sheet orientation must fit table')
    require(all(s['sheet_mm'][i] <= m['table_mm'][s['sheet_to_table_axes'][i]] for i in range(2)), 'Sheet exceeds table')
    require(set(s['hold_down_perimeter_mm'].values()) == {20}, 'Preserve 20 mm perimeter')
    require(s['usable_rectangle_mm'] == [20, 20, 2460, 1560], 'Wrong usable area')
    require(s['minimum_part_spacing_mm'] == 15, 'Preserve 15 mm spacing')
    require(t['through_cut_cutter_diameter_mm'] == 4 and t['natural_internal_radius_mm'] == 2
            and t['coupon_pocket_tool_diameter_mm'] == 4, 'Coupon must use supplier Ø4/R2 tool')
    require(c['required_before_full_sheet_release'] is True, 'Coupon gate cannot be disabled')
    require(c['coupon_board_mm']==[300,210] and c['fit_key_mm']==[25,25] and c['fit_key_gap_mm']==15,
            'Changing coupon layout requires a reviewed generator update')
    require(len(c['clearance_trials_mm'])==6 and 0 in c['clearance_trials_mm']
            and all(finite(x) and -.5 <= x <= .5 for x in c['clearance_trials_mm']), 'Six bounded fit trials including zero required')
    require(c['representative_pocket_depth_mm']==6 and c['corner_strategy']=='T_BONE_SEMICIRCLES_ON_SHORT_EDGES_R2',
            'Coupon layout must match documented pocket and corner strategy')
    require(t['pilot_locator']['diameter_mm']==4 and t['pilot_locator']['depth_mm']==.5,
            'Coupon locator must match operation layer')
    if measured:
        a = s['actual_thickness_mm']
        samples = s['thickness_measurements_mm']
        require(finite(a) and 0 < a <= s['spacing_valid_for_thickness_up_to_mm'],
                'Measured thickness required; >18 mm is outside confirmed spacing scope')
        require(s['production_lot_id'] and samples and all(finite(x) and x > 0 for x in samples),
                'Production-lot ID and real thickness measurements required')
        require(max(samples)<=18, 'Lot includes thickness outside confirmed <=18 mm spacing scope')
        require(min(samples) <= a <= max(samples), 'Design thickness must be within measured lot samples')
        require(c['representative_pocket_depth_mm'] < min(samples), 'Pocket must retain a floor')
        require(a + min(c['clearance_trials_mm']) > 8, 'Slot must accommodate four R2 T-bone ends')


def element(parent, tag, **attrs):
    return ET.SubElement(parent, f'{{{NS}}}{tag}', {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def tbone(x, y, w, h, r=2):
    # One non-overlapping closed contour: outward half-circles at both ends of
    # each short edge. The four original square corners are relieved, not rounded.
    return (f'M {x} {y} A {r} {r} 0 0 1 {x+2*r} {y} '
            f'L {x+w-2*r} {y} A {r} {r} 0 0 1 {x+w} {y} '
            f'L {x+w} {y+h} A {r} {r} 0 0 1 {x+w-2*r} {y+h} '
            f'L {x+2*r} {y+h} A {r} {r} 0 0 1 {x} {y+h} Z')


def coupon(p, out, measured=False):
    validate_profile(p, measured)
    out.mkdir(parents=True, exist_ok=True)
    stock = p['stock']['actual_thickness_mm'] if measured else p['stock']['nominal_thickness_mm']
    c = p['coupon']
    features = []
    def add(id, op, box, **kw):
        features.append(dict(id=id, operation=op, bounds_xywh_mm=box, face='A', **kw))
    add('BOARD', 'THROUGH', [0, 0, 300, 210], shape='rect', radius_mm=4)
    add('FIT_KEY', 'THROUGH', [315, 0, 25, 25], shape='rect', radius_mm=0,
        note='Use square corner in pocket tests and production-thickness edge in slots. No sanding of fit edges before recording.')
    for i, delta in enumerate(c['clearance_trials_mm']):
        add(f'SLOT_{i+1}', 'THROUGH', [18+43*i, 35, stock+delta, 36], shape='tbone',
            total_clearance_mm=delta, nominal_slot_width_mm=stock+delta)
    add('R2_POCKET', 'POCKET_6', [18, 106, 30, 30], shape='rect', radius_mm=2, depth_mm=6)
    add('TBONE_POCKET', 'POCKET_6', [75, 106, 30, 30], shape='tbone', depth_mm=6)
    add('PILOT_LOCATOR', 'LOCATOR_0_5', [143, 118, 4, 4], shape='circle', depth_mm=.5,
        note='Ø4 flat-bottom recess; not a pilot bore or countersink')
    add('SCREW_LOCATOR', 'LOCATOR_0_5', [218, 118, 4, 4], shape='circle', depth_mm=.5,
        note='Manual pilot/countersink test here after hardware selection, face A only')
    require(315-300 >= p['stock']['minimum_part_spacing_mm'], 'Separate fit key spacing')
    for f in features[2:]:
        x, y, w, h = f['bounds_xywh_mm']
        relief = 2 if f['shape'] == 'tbone' else 0
        require(x >= 15 and y-relief >= 15 and x+w <= 285 and y+h+relief <= 195,
                f'Coupon web/border too small: {f["id"]}')
    def svg(review):
        root = ET.Element(f'{{{NS}}}svg', width='340mm', height='210mm', viewBox='0 0 340 210')
        root.set('data-authority', 'REVIEW_ONLY_NOT_FOR_CUTTING' if review else 'COUPON_ONLY_CAM_REVIEW_REQUIRED')
        root.set('data-package-sha256', fingerprint(p))
        element(root, 'title').text = 'Supplier calibration coupon — face A only; never full-sheet release'
        element(root, 'metadata').text = 'CERN-OHL-S-2.0; Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet'
        groups = {}
        for op, color in [('THROUGH', '#183d59'), ('POCKET_6', '#007c78'), ('LOCATOR_0_5', '#a04500')]:
            groups[op] = element(root, 'g', id=op, fill='none', stroke=color if review else 'black', stroke_width=.2)
        for f in features:
            x, y, w, h = f['bounds_xywh_mm'];g = groups[f['operation']]
            if f['shape'] == 'tbone':
                element(g, 'path', id=f['id'], d=tbone(x, y, w, h))
            elif f['shape'] == 'circle':
                element(g, 'circle', id=f['id'], cx=x+w/2, cy=y+h/2, r=w/2)
            else:
                element(g, 'rect', id=f['id'], x=x, y=y, width=w, height=h, rx=f['radius_mm'])
        if review:
            labels = element(root, 'g', id='REVIEW_LABELS_NOT_MACHINING', fill='#183d59', font_family='sans-serif', font_size=3.4)
            def label(x,y,text,size=3.4):
                element(labels, 'text', x=x, y=y, font_size=size).text=text
            label(10, 11, 'REVIEW ONLY — NOT A CUTTING FILE', 5)
            label(10, 19, f'FACE A | Ø4 / R2 | thickness {stock:g} mm: '+('MEASURED LOT' if measured else 'NOMINAL ILLUSTRATION ONLY'))
            label(10, 26, 'Clearance is TOTAL width allowance. Production coupon requires measured lot thickness.')
            for f in features[2:8]:
                x,y,w,h=f['bounds_xywh_mm'];label(x,85,f'{f["id"]}: {f["total_clearance_mm"]:+.2f}')
                label(x,91,f'width {w:.2f}')
            label(18, 101, 'R2 unrelieved');label(75, 101, 'T-bone R2')
            label(18, 146, 'Both pockets 6 mm deep; compare square-key seating.')
            label(130, 108, 'Shallow locator');label(199, 108, 'Manual screw test')
            label(130, 133, 'Ø4 × 0.5 deep');label(199, 133, 'Selected pilot / CSK')
            label(199, 140, 'No cutter flip / no back-face CNC')
            label(10, 167, 'Use the same production plywood, machine, cutter and CAM process.')
            label(10, 175, 'Measure slots, pocket depth, R2, T-bone seating and pilot; record manual screw fit.')
            label(10, 183, 'Fit key: actual stock edge tests slots; square corner tests relief. Protect all fit edges.')
            label(10, 192, 'No full-sheet release before coupon acceptance and regeneration.')
            label(10, 202, 'CERN-OHL-S-2.0 | github.com/advpeterrobinson-hash/vpin-cabinet', 3)
            label(318, 9, '25 × 25');label(318, 16, 'FIT KEY');label(317, 33, '15 mm gap', 3)
        return ET.tostring(root, encoding='utf-8', xml_declaration=True)
    (out/'coupon-review.svg').write_bytes(svg(True))
    machining = out/'coupon-cut.svg'
    if measured:
        machining.write_bytes(svg(False))
    elif machining.exists():
        # Only an owned generated file; prevent a previous measured file surviving a preview rebuild.
        machining.unlink()
    manifest = {'status': 'COUPON_ONLY_CAM_REVIEW_REQUIRED' if measured else 'PREVIEW_NO_MACHINING_FILE',
                'full_sheet_release': False, 'stock_thickness_mm': stock,
                'thickness_authority': 'MEASURED_PRODUCTION_LOT' if measured else 'NOMINAL_ILLUSTRATION_ONLY',
                'production_lot_id': p['stock']['production_lot_id'], 'package_sha256': fingerprint(p),
                'single_face': 'A', 'features': features, 'overall_bounds_mm': [340,210],
                'suggested_sheet_translation_xy_mm': [20,20],
                'operations': {'THROUGH': 'Through measured stock, depth and spoilboard allowance set by supplier CAM',
                               'POCKET_6': '6 mm below face A with Ø4 cutter',
                               'LOCATOR_0_5': '0.5 mm below face A with Ø4 cutter; tool-entry strategy by supplier'},
                'cam_note': 'Finished boundaries, not toolpaths. Machine internals first, outer parts last. Retention/tabs and compensation by supplier. Review labels never imported for machining.',
                'manual_test': c['screw_interface'], 'cut_svg_sha256': hashlib.sha256(machining.read_bytes()).hexdigest() if measured else None}
    write(out/'coupon-manifest.json', manifest)
    template = {'production_lot_id': None, 'package_sha256': None, 'cut_svg_sha256': None,
                'machine_cam_run_reference': None, 'tested_by': None, 'tested_on': None,
                'same_lot_machine_cutter_cam_confirmed': False,
                'measured_slot_widths_mm': {f'SLOT_{i+1}': None for i in range(6)},
                'fit_observations': {f'SLOT_{i+1}': None for i in range(6)},
                'selected_fit_clearance_mm': None, 'measured_pocket_depth_mm': None,
                'pocket_depth_accepted': False, 'r2_corner_accepted': False, 'tbone_fit_accepted': False,
                'measured_locator_depth_mm': None, 'locator_accepted': False,
                'screw_interface_accepted': False, 'screw_test_notes': None,
                'production_lot_thickness_accepted': False, 'owner_coupon_accepted': False}
    write(out/'coupon-results-template.json', template)
    return manifest


def register(out):
    wood = read(ROOT/'config/wood_materials_v33.json')
    path=out/'one-side-part-register.json'
    if path.exists():
        # Preserve subsequently reviewed operation plans; never reset them on a coupon rerun.
        return read(path)
    rows=[]
    for part in wood['parts']:
        decomposition = part['status'] == 'CNC_COMPONENT_BREAKDOWN_HOLD' or part['quantity'] != 1
        rows.append({'id':part['id'], 'current_object':part['object'], 'source':part['source'],
                     'manufacturing_status':'BLOCKED_DECOMPOSITION_REQUIRED' if decomposition else 'BLOCKED_OPERATION_AUDIT',
                     'cnc_face':None, 'cnc_operations':[], 'manual_finish_operations':[],
                     'operation_audit_complete':False, 'source_brep_preserved':True,
                     'note':'Compound/laminated component needs planar part extraction.' if decomposition else 'Inventory geometry is not an audited face-operation plan; no two-face instructions may be generated.'})
    data={'supplier_profile':'peter_supplier_v1', 'scope':'All 93 CURRENT wood inventory components; not a completed manufacturing operation audit',
          'parts':rows, 'flip_instructions':False}
    write(path,data)
    return data


def record_results(p, result, manifest):
    validate_profile(p, measured=True)
    require(manifest['status']=='COUPON_ONLY_CAM_REVIEW_REQUIRED', 'Cannot validate a nominal preview')
    require(result['production_lot_id']==p['stock']['production_lot_id'], 'Wrong production lot')
    require(result['package_sha256']==manifest['package_sha256']==fingerprint(p), 'Stale coupon input geometry')
    require(result['cut_svg_sha256']==manifest['cut_svg_sha256'] and bool(result['cut_svg_sha256']), 'Wrong cut file')
    for field in ('machine_cam_run_reference','tested_by','tested_on','screw_test_notes'):
        require(bool(result[field]), f'Required coupon evidence: {field}')
    for field in ('same_lot_machine_cutter_cam_confirmed','pocket_depth_accepted','r2_corner_accepted',
                  'tbone_fit_accepted','locator_accepted','screw_interface_accepted',
                  'production_lot_thickness_accepted','owner_coupon_accepted'):
        require(result[field] is True, f'Coupon gate not passed: {field}')
    for key in (f'SLOT_{i+1}' for i in range(6)):
        require(finite(result['measured_slot_widths_mm'][key]) and result['measured_slot_widths_mm'][key]>0
                and result['fit_observations'][key], f'Missing slot measurement/fit: {key}')
    for key in ('measured_pocket_depth_mm','measured_locator_depth_mm'):
        require(finite(result[key]) and 0 < result[key] < p['stock']['actual_thickness_mm'], f'Bad {key}')
    require(result['selected_fit_clearance_mm'] in p['coupon']['clearance_trials_mm'], 'Selected clearance must be tested')
    hardware=p['coupon']['screw_interface']['purchased_hardware_dimensions']
    require(isinstance(hardware,dict), 'Record selected screw/pilot/countersink dimensions before acceptance')
    require(bool(hardware.get('part_reference')), 'Selected screw reference required')
    for key in ('shank_diameter_mm','length_mm','pilot_diameter_mm','pilot_depth_mm',
                'countersink_diameter_mm','countersink_included_angle_deg','countersink_depth_mm'):
        require(finite(hardware.get(key)) and hardware[key]>0, 'Missing measured screw test dimension: '+key)
    p['coupon'].update(validation_status='VALIDATED', selected_fit_clearance_mm=result['selected_fit_clearance_mm'],
                       accepted_corner_strategy=p['coupon']['corner_strategy'], validated_package_sha256=fingerprint(p), results=result)
    # Coupon acceptance alone must never authorize full-sheet manufacturing.
    p['release_policy']['full_sheet_release']=False


def release_blockers(p, parts, hardware_qualified=False, owner_release=False):
    errors=[]
    try:validate_profile(p, measured=True)
    except ValueError as e:errors.append(str(e))
    c=p['coupon']
    if c['validation_status']!='VALIDATED' or c['selected_fit_clearance_mm'] is None:
        errors.append('Coupon not validated / fit clearance not selected')
    elif c['validated_package_sha256']!=fingerprint(p):
        errors.append('Coupon acceptance invalidated by changed stock/tool/process/test geometry')
    if not c['results']:errors.append('No recorded physical coupon evidence')
    elif c['validation_status']=='VALIDATED':
        try:
            record_results(copy.deepcopy(p),c['results'],{'status':'COUPON_ONLY_CAM_REVIEW_REQUIRED',
                           'package_sha256':fingerprint(p),'cut_svg_sha256':c['results'].get('cut_svg_sha256')})
        except (ValueError,KeyError,TypeError) as e:
            errors.append('Invalid recorded coupon evidence: '+str(e))
    current={x['id'] for x in read(ROOT/'config/wood_materials_v33.json')['parts']}
    if {x['id'] for x in parts['parts']}!=current or len(parts['parts'])!=len(current):errors.append('Part register incomplete or duplicated')
    for row in parts['parts']:
        ok=(row['manufacturing_status'] in p['release_policy']['allowed_part_statuses']
            and row['operation_audit_complete'] is True and row['cnc_face'] in ('A','B')
            and bool(row['cnc_operations']))
        if row['manufacturing_status']=='ONE_SIDE_CNC_PLUS_MANUAL_FINISH':
            ok=ok and bool(row['manual_finish_operations'])
        for op in row['cnc_operations']:
            ok=ok and op.get('face')==row['cnc_face'] and not op.get('flip',False)
        if not ok:errors.append(row['id']+': no verified one-face operation plan')
    if not hardware_qualified:errors.append('Purchased hardware dimensions / dependent permanent interfaces unqualified')
    if not owner_release:errors.append('Owner full-sheet manufacturing approval absent')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,default=PROFILE)
    parser.add_argument('--out',type=Path,default=OUT)
    parser.add_argument('--measured-coupon',action='store_true',help='Requires actual thickness and lot samples in profile; emits coupon-only SVG')
    parser.add_argument('--record-results',type=Path,help='Store real accepted measurements and tested fit in profile; never enables full-sheet release')
    args=parser.parse_args();p=read(args.profile)
    if args.record_results:
        manifest=read(args.out/'coupon-manifest.json')
        cut=args.out/'coupon-cut.svg'
        require(cut.exists() and hashlib.sha256(cut.read_bytes()).hexdigest()==manifest['cut_svg_sha256'], 'Cut file missing/changed')
        record_results(p,read(args.record_results),manifest);write(args.profile,p)
        write(args.out/'release-status.json',{'supplier_profile_complete_for_preparation':True,
              'full_sheet_release':False,'blockers':release_blockers(p,register(args.out)),
              'current_geometry_modified':False})
        print('COUPON_RESULTS_RECORDED_FULL_SHEET_STILL_BLOCKED');return
    coupon(p,args.out,args.measured_coupon)
    reg=register(args.out)
    errors=release_blockers(p,reg)
    write(args.out/'release-status.json',{'supplier_profile_complete_for_preparation':True,
          'full_sheet_release':False,'blockers':errors,'current_geometry_modified':False})
    print('PETER_SUPPLIER_PREPARATION_PASS; full-sheet release BLOCKED;',len(reg['parts']),'wood components registered')


if __name__=='__main__':
    main()

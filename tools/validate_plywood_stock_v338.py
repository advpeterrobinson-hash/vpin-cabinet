"""Permanent V33.8 two-stock gate and read-only negative controls.
CERN-OHL-S-2.0. No input row is modified; no CNC output is generated.
"""
import copy


def validate_stock_policy(parts, policy):
    expected = {12, 18}
    assert set(policy['allowed_nominal_plywood_stock_mm']) == expected, 'Owner stock policy must remain12/18'
    assert set(policy['required_exact_active_plywood_stock_set_mm']) == expected, 'Exact active stock set must remain12/18'
    assert policy['opposite_face_cnc_allowed'] is False
    assert policy['nominal_is_not_measured'] is True
    assert policy['coupon_required_per_actual_stock_and_fit'] is True
    plywood = []
    excluded = []
    for part in parts:
        if part.get('manufacturing_class') == 'SHOP_MADE_SOLID_WOOD_PART':
            assert part['manufacturing_part_id'] in ('SW01','SW02'), 'Only explicit SW01/SW02 solid wood is excluded'
            assert part['nominal_stock_thickness_mm'] is None, 'Solid wood must not carry a plywood stock thickness'
            excluded.append(part['instance_id'])
        else:
            assert part['manufacturing_part_id'] not in ('SW01','SW02'), 'Solid wood must retain its separate manufacturing classification'
            plywood.append(part)
    actual = {p['nominal_stock_thickness_mm'] for p in plywood}
    assert actual == expected, f'Forbidden or missing active plywood stock family: {actual}; expected {expected}'
    assert all(not p.get('opposite_face_cnc', False) for p in plywood), 'Opposite-face CNC is forbidden'
    return {'active_nominal_plywood_stock_mm': sorted(actual), 'plywood_pieces': len(plywood), 'excluded_solid_wood_instances': excluded}


def negative_controls(parts, policy):
    positive = validate_stock_policy(parts, policy)
    checks = []
    first = next(i for i, p in enumerate(parts) if p.get('manufacturing_class') != 'SHOP_MADE_SOLID_WOOD_PART')
    for forbidden in (4, 6, 8, 9, 10, 15, 24):
        trial = copy.deepcopy(parts)
        trial[first]['nominal_stock_thickness_mm'] = forbidden
        rejected = False
        try:
            validate_stock_policy(trial, policy)
        except AssertionError:
            rejected = True
        checks.append({'name': f'Forbidden{forbidden}mm plywood is rejected', 'injected_nominal_mm': forbidden, 'pass': rejected})
    trial = copy.deepcopy(parts)
    for p in trial:
        if p.get('manufacturing_class') != 'SHOP_MADE_SOLID_WOOD_PART' and p['nominal_stock_thickness_mm'] == 12:
            p['nominal_stock_thickness_mm'] = 18
    rejected = False
    try:
        validate_stock_policy(trial, policy)
    except AssertionError:
        rejected = True
    checks.append({'name': 'Missing12mm active stock is rejected', 'pass': rejected})
    trial = copy.deepcopy(parts)
    trial[first]['manufacturing_class'] = 'SHOP_MADE_SOLID_WOOD_PART'
    trial[first]['nominal_stock_thickness_mm'] = 9
    rejected = False
    try:
        validate_stock_policy(trial, policy)
    except AssertionError:
        rejected = True
    checks.append({'name': 'Forbidden plywood cannot hide behind solid-wood classification', 'pass': rejected})
    assert all(c['pass'] for c in checks), checks
    assert validate_stock_policy(parts, policy) == positive, 'Negative controls must not mutate actual rows'
    return {'pass': True, 'checks': checks, 'positive': positive, 'method': 'Deep-copy injection only; CURRENT/register rows unchanged', 'manufacturing_release': False}

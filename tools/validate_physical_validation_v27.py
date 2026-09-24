"""Evidence completeness guard. Never creates patterns or clears CNC blockers."""
import copy
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'bom/PHYSICAL_VALIDATION_RESULTS_V27.json'


def rows(name):
    with (ROOT / 'bom' / name).open() as source:
        return list(csv.DictReader(source))


def evidence(paths):
    assert paths, 'physical evidence files missing'
    for value in paths:
        path = Path(value)
        assert not path.is_absolute() and '..' not in path.parts, 'use repository-relative evidence'
        assert (ROOT / path).is_file(), 'evidence file not found: ' + value


def validate(data=None):
    data = data if data is not None else json.loads(LEDGER.read_text())
    assert data['baseline_head'] == 'c1bb566a8eff24240434c3f084e068c20e7cd4a0'
    assert data['manufacturing_ready'] is False and data['automatic_unlock'] is False, 'no automatic release'
    all_features = rows('CNC_FEATURES_V25.csv')
    blocked = [r for r in all_features if r['status'] == 'BLOCKED_MEASURE_HARDWARE']
    key = lambda r: (r['part_id'], r['feature_id'], r.get('component_id', r.get('hardware_dependency')))
    expected = {key(r) for r in blocked}
    assert len(blocked) == 59 and len(expected) == 59, 'baseline blocked set requires explicit reviewed migration'
    assert expected == {key(r) for r in rows('BLOCKED_CNC_FEATURES_V25.csv')}, 'blocked subset drift'
    groups = data['feature_groups']
    assert len(groups) == 59 and {key(r) for r in groups} == expected, 'feature coverage mismatch'
    components = {r['component_id']: r for r in data['components']}
    source = {r['item_id']: r for r in rows('MEASURE_BEFORE_CNC_V25.csv')}
    assert len(components) == len(data['components']) and set(components) == set(source), 'component coverage mismatch'
    for cid, component in components.items():
        assert component['validation_status'] in ('UNMEASURED', 'RECORDED', 'REVIEWED'), 'invalid evidence status'
        measures = component['measurements']
        assert [m['required'] for m in measures] == [s.strip() for s in source[cid]['exact_measurements'].split(';')], 'measurement scope lost'
        assert len({m['measurement_id'] for m in measures}) == len(measures), 'duplicate measurement ID'
        assert component['provisional_context'] and component['recording_tolerance'] and component['datum']
        for m in measures:
            value = m['measured_value']
            if component['validation_status'] != 'UNMEASURED':
                assert value is not None and value != '', 'recorded component has missing measurements'
            if value is not None:
                assert component['physical_part_id'] and component['operator'] and component['date'], 'unidentified physical source'
                assert m['unit'] and m['raw_readings'] and m['instrument'] and m['uncertainty'], 'incomplete measurement provenance'
                assert m['source_kind'] in ('PHYSICAL_MEASUREMENT', 'PHYSICAL_TEST'), 'catalogue/estimate is not measurement'
                evidence(m['evidence_paths'])
        if component['validation_status'] == 'REVIEWED':
            assert component['reviewer'] and component['review_date'], 'missing evidence reviewer'
            evidence(component['review_evidence_paths'])
    for group in groups:
        assert group['component_id'] in components
        assert group['validation_status'] == 'BLOCKED_MEASURE_HARDWARE', 'worksheet cannot release geometry'
        assert group['measured_pattern'] is None and group['current_pattern_value'] is None, 'patterns require a separate reviewed release change'
        assert group['unlocks_after_freeze_gate'].startswith(group['part_id'] + ':' + group['feature_id'])
    tests = data['physical_trials']
    required = {'PV-PLUNGER', 'PV-PROP-L', 'PV-PROP-R', 'PV-PROP-MOTION', 'PV-MASS', 'PV-ERGONOMICS', 'PV-CONTROLS-SSF', 'SV-01', 'SV-02', 'SV-03', 'SV-04', 'SV-05', 'PV-AIRFLOW', 'PV-THERMAL', 'PV-STOCK-TOOL', 'PV-LOADS', 'PV-ELECTRICAL', 'PV-CNC-PACKAGE'}
    assert len(tests) == len(required) and {t['test_id'] for t in tests} == required, 'physical trial coverage mismatch'
    for trial in tests:
        assert trial['status'] in ('OPEN', 'FAIL', 'PASS'), 'invalid physical test status'
        if trial['status'] != 'OPEN':
            assert trial['fixture_revision'] and trial['operator'] and trial['date'] and trial['result'], 'incomplete physical result'
            evidence(trial['evidence_paths'])
        if trial['status'] == 'PASS':
            assert trial['approved_acceptance_criteria'] and trial['reviewer'] and trial['review_date'], 'unreviewed test acceptance'
    return len(groups), len(components), len(tests)


def negatives():
    base = json.loads(LEDGER.read_text())
    def catalogue(d):
        c = d['components'][0]
        c.update(physical_part_id='catalogue-part', operator='example', date='2026-09-24')
        c['measurements'][0].update(measured_value=18, unit='mm', raw_readings=[18], instrument='catalogue', uncertainty='unknown', source_kind='CATALOGUE')
    cases = [
        ('missing feature', lambda d: d['feature_groups'].pop()),
        ('wrong component mapping', lambda d: d['feature_groups'][0].update(component_id='HF-030')),
        ('catalogue promoted', catalogue),
        ('empty reviewed evidence', lambda d: d['components'][0].update(validation_status='REVIEWED')),
        ('silent pattern release', lambda d: d['feature_groups'][0].update(measured_pattern={'x': 100})),
        ('unproved prop pass', lambda d: d['physical_trials'][1].update(status='PASS')),
        ('manufacturing claim', lambda d: d.update(manufacturing_ready=True)),
    ]
    for name, mutate in cases:
        data = copy.deepcopy(base)
        mutate(data)
        try:
            validate(data)
        except AssertionError:
            print('PHYSICAL_EVIDENCE_NEGATIVE_PASS', name)
        else:
            raise AssertionError('Accepted ' + name)


if __name__ == '__main__':
    print('PHYSICAL_EVIDENCE_PASS groups/components/trials:', validate())
    negatives()

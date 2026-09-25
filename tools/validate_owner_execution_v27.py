"""Reconcile convenience workflow, procurement scope and untouched engineering."""
import copy
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

from generate_owner_execution_v27 import DOCS, LEDGER, QUEUE, ROOT, generated_outputs
from owner_workflow_v27 import BUY_NOW, REFERENCE_IDS

BASELINE = '25bc483d7e5ae47dfe13cea3bfbdd64086074715'


def validate(queue=None):
    q = queue if queue is not None else json.loads(QUEUE.read_text())
    ledger = json.loads(LEDGER.read_text())
    measurements = {m['measurement_id']: m for c in ledger['components'] for m in c['measurements']}
    trials = {t['test_id'] for t in ledger['physical_trials']}
    assert q['convenience_only'] and q['manufacturing_ready'] is False and q['automatic_unlock'] is False, 'queue release claim'
    assert q['authoritative_ledger'] == 'bom/PHYSICAL_VALIDATION_RESULTS_V27.json'
    assert q['ledger_sha256'] == hashlib.sha256(LEDGER.read_bytes()).hexdigest(), 'stale ledger mapping'
    ops = q['operations']
    mids = [mid for o in ops for mid in o['measurement_ids']]
    tids = [tid for o in ops for tid in o['trial_ids']]
    assert Counter(mids) == Counter(measurements.keys()) and len(mids)==186, 'measurement IDs missing/duplicated/unknown'
    assert Counter(tids) == Counter(trials) and len(tids)==18, 'trial IDs missing/duplicated/unknown'
    assert q['measurement_count']==186 and q['trial_count']==18
    assert q['practical_operation_count']==len(ops) and len({o['operation_id'] for o in ops})==len(ops)
    assert q['session_count']==12 and {o['session'] for o in ops}==set(range(12))
    done = set()
    for o in ops:
        assert set(o['dependencies']) <= done, 'queue not in executable dependency order'
        done.add(o['operation_id'])
        assert o['status']=='NOT_STARTED', 'queue fabricated completion'
        assert o['category'] in ('A','B')
        assert [m['measurement_id'] for m in o['measurements']]==o['measurement_ids'], 'detail mapping mismatch'
        assert [t['trial_id'] for t in o['trials']]==o['trial_ids'], 'trial detail mismatch'
        for m in o['measurements']:
            assert m['exact_measurement']==measurements[m['measurement_id']]['required'], 'measurement changed'
            assert m['reference_only']==(m['measurement_id'] in REFERENCE_IDS), 'reference promoted'
            pointer = m['ledger_pointer'].split('/')[1:]
            record = ledger
            for p in pointer:
                record = record[int(p)] if isinstance(record,list) else record[p]
            assert record['measurement_id']==m['measurement_id'], 'wrong ledger destination'
        for t in o['trials']:
            assert ledger['physical_trials'][int(t['ledger_pointer'].split('/')[-1])]['test_id']==t['trial_id']
        if set(o['trial_ids']) & {'PV-PROP-L','PV-PROP-R','PV-LOADS','SV-03'} or 'HF-010-M07' in o['measurement_ids'] or 'HF-022-M06' in o['measurement_ids']:
            assert o['category']=='B' and o['execution_hold']=='REVIEWED_CRITERIA_REQUIRED', 'unsafe owner load task'
        assert o['gate'].startswith('Evidence only.') and o['acceptance_source'], 'missing existing gate'
    assert {a['component_id'] for a in q['arrivals'] if a['category']=='BUY NOW'}==BUY_NOW, 'BUY NOW broadened or lost'
    components = {c['component_id']:c for c in ledger['components']}
    assert len(q['arrivals'])==len(components) and {a['component_id'] for a in q['arrivals']}==set(components)
    for a in q['arrivals']:
        assert a['source_procurement_group']==components[a['component_id']]['procurement_group'], 'acquisition source changed'
        assert a['category'] in ('BUY NOW','HAVE / OWNER-SUPPLIED','WAIT','REFERENCE ONLY')
        if a['category']=='BUY NOW':
            assert a['source_procurement_group']=='BUY NOW', 'new procurement authorization'
    with (ROOT/'bom/BLOCKED_CNC_FEATURES_V25.csv').open() as f:
        blockers=list(csv.DictReader(f))
    assert len(blockers)==59 and all(r['status']=='BLOCKED_MEASURE_HARDWARE' for r in blockers), 'blockers changed'
    return len(mids), len(tids), len(ops)


def protected_sources():
    names = subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=ROOT,text=True).splitlines()
    exact = {
        'bom/PHYSICAL_VALIDATION_RESULTS_V27.json', 'docs/PHYSICAL_VALIDATION_PLAN_V27.md',
        'docs/PHYSICAL_RESULTS_WORKSHEET_V27.md', 'docs/CNC_FREEZE_GATE_V27.md',
        'docs/HARDWARE_MEASUREMENT_PACK_V25.md', 'docs/OWNER_REVIEW_V27.md',
    }
    return [n for n in names if n in exact or n.startswith(('config/','bom/'))
            or n.startswith(('tools/build_','tools/detail_structure','tools/owner_features','tools/active_parts'))]


def unchanged(overrides=None):
    for name in protected_sources():
        accepted = subprocess.check_output(['git','show',f'{BASELINE}:{name}'],cwd=ROOT)
        observed = overrides[name] if overrides and name in overrides else (ROOT/name).read_bytes()
        assert observed==accepted, 'protected baseline changed: '+name
    if overrides is None:
        print('OWNER_PROTECTED_BASELINE_PASS ledger/configs/geometry sources/registers/freeze')


def generated_and_links():
    before = {n:(ROOT/n).read_bytes() for n in protected_sources()}
    # Run the real authoring command, not just its pure function, to detect mutation.
    subprocess.run(['python3',str(ROOT/'tools/generate_owner_execution_v27.py')],cwd=ROOT,check=True,capture_output=True)
    assert all((ROOT/n).read_bytes()==b for n,b in before.items()), 'generation mutated authoritative sources'
    for path, expected in generated_outputs().items():
        assert path.read_text()==expected, 'generated convenience drift: '+str(path)
    for name in DOCS:
        path=ROOT/'docs'/name
        text=path.read_text()
        for target in re.findall(r'\]\(([^)]+)\)',text):
            assert (path.parent/target.split('#')[0]).exists(), 'broken link: '+target
        assert not any(line.rstrip()!=line for line in text.splitlines()), 'generated trailing whitespace'
        assert text.endswith('\n') and not text.endswith('\n\n'), 'generated blank EOF'
    sheet=(ROOT/'docs/OWNER_MEASUREMENT_SHEETS_V27.md').read_text()
    ids=re.findall(r'\| \*\*(HF-\d+-M\d+)\*\*',sheet)
    assert len(ids)==len(set(ids))==186, 'printable measurement loss'
    ids=re.findall(r'^\*\*((?:PV|SV)-[A-Z0-9-]+) — ',sheet,re.M)
    assert len(ids)==len(set(ids))==18, 'printable trial loss'
    print('OWNER_GENERATION_READONLY_AND_LINKS_PASS')


def negatives():
    base=json.loads(QUEUE.read_text())
    def measurement_op(q):
        return next(o for o in q['operations'] if o['measurement_ids'])
    def trial_op(q):
        return next(o for o in q['operations'] if o['trial_ids'])
    def broaden(q):
        next(a for a in q['arrivals'] if a['component_id']=='HF-032')['category']='BUY NOW'
    def unsafe(q):
        next(o for o in q['operations'] if 'PV-PROP-L' in o['trial_ids'])['category']='A'
    cases=[
        ('omit measurement',lambda q:measurement_op(q)['measurement_ids'].pop()),
        ('duplicate measurement',lambda q:measurement_op(q)['measurement_ids'].append('HF-001-M01')),
        ('invent measurement',lambda q:measurement_op(q)['measurement_ids'].append('HF-999-M01')),
        ('omit trial',lambda q:trial_op(q)['trial_ids'].pop()),
        ('duplicate trial',lambda q:trial_op(q)['trial_ids'].append('PV-STOCK-TOOL')),
        ('invent trial',lambda q:trial_op(q)['trial_ids'].append('PV-NOT-A-TEST')),
        ('buy later promoted',broaden), ('prop proof as ordinary task',unsafe),
        ('stale source ledger',lambda q:q.update(ledger_sha256='unverified')),
        ('manufacturing claim',lambda q:q.update(manufacturing_ready=True)),
    ]
    for name,mutate in cases:
        q=copy.deepcopy(base);mutate(q)
        try:
            validate(q)
        except AssertionError:
            print('OWNER_QUEUE_NEGATIVE_PASS',name)
        else:
            raise AssertionError('Accepted '+name)
    # In-memory mutations only: the tests never modify real protected files.
    for path in ['config/design.json', 'docs/CNC_FREEZE_GATE_V27.md',
                 'bom/PHYSICAL_VALIDATION_RESULTS_V27.json', 'bom/BLOCKED_CNC_FEATURES_V25.csv']:
        try:
            unchanged({path:b'UNAUTHORIZED CHANGE'})
        except AssertionError:
            print('OWNER_QUEUE_NEGATIVE_PASS protected source',path)
        else:
            raise AssertionError('Accepted protected source mutation: '+path)


if __name__=='__main__':
    unchanged()
    generated_and_links()
    print('OWNER_QUEUE_PASS measurements/trials/operations:',validate())
    negatives()

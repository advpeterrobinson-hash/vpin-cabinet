"""Independent saved-CAD / report / immutable-baseline checks. CERN-OHL-S-2.0."""
from pathlib import Path
import hashlib
import json
import subprocess
import FreeCAD as A
import Part

R = Path(__file__).resolve().parents[1]
cfg = json.loads((R/'config/matrix_route_backbox_audit_v32.json').read_text())
O = R/cfg['output_directory']
r = json.loads((O/'validation.json').read_text())
checks = []


def check(name, value):
    assert value, name
    checks.append({'check':name, 'pass':True})


def validate_claims(report):
    bb = report['backbox']
    if not bb['zero_actual_wood_assembly_valid']:
        assert bb['sweep_executed'] is False, 'Invalid zero must stop the sweep'
        assert bb['sweep_status'] == 'STOPPED_AT_INVALID_ZERO'
        for key in ('wood_fold_clear','display_fold_clear','dmd_fold_clear','harness_pinch_clear',
                    'stationary_support_new_fold_conflict'):
            assert bb[key] is None, 'No fold conclusion before a valid baseline: '+key
    assert report['manufacturing_ready'] is False
    assert not report['matrix_route']['target_achieved']
    assert report['matrix_route']['new_minimum_mm'] < cfg['route_target_mm']


validate_claims(r)
check('zero-state gate and unmet margin explicitly retained', True)
for key, value in [('sweep_executed',True), ('wood_fold_clear',True),
                   ('stationary_support_new_fold_conflict',False)]:
    altered = json.loads(json.dumps(r))
    altered['backbox'][key] = value
    try:
        validate_claims(altered)
    except AssertionError:
        pass
    else:
        raise AssertionError('False fold approval was not rejected: '+key)
    check('negative false fold approval rejected: '+key, True)

for p,h in r['source_hashes'].items():
    data = (R/p).read_bytes()
    check('source bytes unchanged: '+p, hashlib.sha256(data).hexdigest()==h)
    committed = subprocess.check_output(['git','show',cfg['source_head']+':'+p],cwd=R)
    check('source matches accepted HEAD: '+p, committed==data)

# Cover ALL accepted sources/exports, not just hand-picked subsystem names.
changed = subprocess.check_output(['git','diff',cfg['source_head'],'--name-only','--',
    'config','tools','cad','exports'],cwd=R,text=True).splitlines()
allowed = {'config/matrix_route_backbox_audit_v32.json',
           'tools/matrix_route_backbox_audit_v32_entry.py',
           'tools/check_matrix_route_backbox_audit_v32.py',
           'tools/render_matrix_route_backbox_audit_v32.py'}
check('all accepted V32 sources, CAD, manufacturing and viewer files preserved',
      all(p in allowed or p.startswith(cfg['output_directory']+'/') for p in changed))

d = A.openDocument(str(O/'backbox-source-audit.FCStd'))
d.recompute()
parts = {o.Name:o.Shape for o in d.Objects if hasattr(o,'Shape')}
wood = {o.Name:o.Shape for o in d.Objects if hasattr(o,'AuditRole') and o.AuditRole=='wood'}
check('saved audit shapes valid', all(s.isValid() for s in parts.values()))
check('saved manufactured members single solids (intersection fragments are analysis geometry)',
      all(len(o.Shape.Solids)==1 for o in d.Objects
          if hasattr(o,'AuditRole') and o.AuditRole!='zero_intersections'))
check('saved audit explicitly not a current manufacturing model', 'ZERO INVALID' in d.AuditStatus)
for n,s in wood.items():
    for m,t in wood.items():
        if n<m:
            check('wood joint no overlap: '+n+'/'+m, s.common(t).Volume<.001)
for row in r['backbox']['zero_wood_cabinet_hits']:
    common = parts[row['part']].common(parts[row['obstacle']])
    check('saved zero collision independently reproduced: '+row['obstacle'],
          abs(common.Volume-row['volume_mm3'])<1e-6 and common.Volume>900)
check('coarse box contains empty cavity; cannot stand for structural wood',
      parts['PF_BackboxCheckEnvelope'].isInside(A.Vector(300,1180,900),1e-7,False)
      and not any(s.isInside(A.Vector(300,1180,900),1e-7,False) for s in wood.values()))
floor = parts['BackboxFloorV14']
negative = floor.copy()
negative.translate(A.Vector(0,0,.1))
check('negative coordinate mutation is detectable', floor.cut(negative).Volume+negative.cut(floor).Volume>1)
A.closeDocument(d.Name)
for angle in (45,90):
    d = A.openDocument(str(O/f'diagnostic_{angle}_not_validated.FCStd'))
    d.recompute()
    check(f'{angle} degree image geometry explicitly illustration only',
          'ILLUSTRATION ONLY' in d.AuditStatus and all(o.Shape.isValid() for o in d.Objects if hasattr(o,'Shape')))
    A.closeDocument(d.Name)

screen = json.loads((O/'route-screen.json').read_text())
check('full bounded combined grid recorded',len(screen['combined'])==7667)
check('no tested upper bound reaches 3 mm',all(row['route_upper_bound_mm']<3 for row in screen['combined']))
check('larger forward travel does not improve limiting rock clearance',
      max(row['route_upper_bound_mm'] for row in screen['forward_only'])<=r['matrix_route']['old_minimum_mm']+1e-7)
check('visibility and accepted route unchanged',r['matrix_route']['visibility_min_percent']>=75
      and not r['matrix_route']['changed'] and r['matrix_route']['forward_mm']==68)
(O/'regression-validation.json').write_text(json.dumps({'checks':checks,'all_pass':True,
    'fold_validated':False,'route_margin_target_achieved':False,'manufacturing_ready':False},indent=2)+'\n')
print('ROUTE_BACKBOX_REGRESSION_PASS',len(checks),flush=True)

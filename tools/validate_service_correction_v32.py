"""Ergonomics and visible-mechanism contract, independent of machining stack. CERN-OHL-S-2.0."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = ('PLAY', 'SERVICE', 'SERVICE LEFT PROP ONLY', 'SERVICE RIGHT PROP ONLY')

def validate_ergonomics(e):
    # Owner limits are explicit guardrails, never hardware-derived.
    if e['primary_y_mm'] > 110 or e['secondary_y_mm'] > 150:
        raise ValueError('Rejected rearward ergonomic drift; explicit future owner decision required')
    if e['front_plane_y_mm'] != 0 or not 60 <= e['below_local_top_mm'] <= 65:
        raise ValueError('Incorrect front/top ergonomic datum')

def validate_visible_mechanism(bundle):
    parts = {p['name']: p for p in bundle['parts']}
    if 'PLAYFIELD_ENVELOPE' not in parts:
        raise ValueError('Missing playfield/display')
    required = ['PF_RearPivotAxis', 'PF_PlainBushL', 'PF_PlainBushR', 'PF_PropL', 'PF_PropR',
                'PF_ReceiverBlockL', 'PF_ReceiverBlockR', 'PF_PositivePinL', 'PF_PositivePinR']
    for name in required:
        if name not in parts or not parts[name]['vertices'] or not parts[name]['faces']:
            raise ValueError('Missing modeled pivot or positive support: '+name)
    if tuple(bundle['states']) != STATES:
        raise ValueError('Missing required viewer states')
    for state in STATES:
        overrides = bundle['states'][state]
        if state != 'PLAY' and not overrides.get('PLAYFIELD_ENVELOPE'):
            raise ValueError('Raised display missing from service state')
        for side in ('L', 'R'):
            active = state == 'SERVICE' or state == f'SERVICE {"LEFT" if side == "L" else "RIGHT"} PROP ONLY'
            if active and any(not overrides.get(f'PF_{kind}{side}', parts.get(f'PF_{kind}{side}')) for kind in ('Prop', 'PositivePin')):
                raise ValueError('Raised support/positive pin absent in '+state)
    if bundle['review']['structural_proof'] or bundle['review']['manufacturing_ready']:
        raise ValueError('Provisional geometry cannot claim load proof or manufacturing release')

def negative_controls(bundle, config):
    results = []
    for key, value in [('primary_y_mm', 110.01), ('secondary_y_mm', 150.01)]:
        bad = dict(config['ergonomics']); bad[key] = value
        try: validate_ergonomics(bad)
        except ValueError: results.append(key+' rejected')
        else: raise AssertionError('Ergonomic negative control failed')
    for omitted in ('PF_RearPivotAxis', 'PF_PlainBushL', 'PF_PropL', 'PF_PositivePinR'):
        bad = dict(bundle); bad['parts'] = [p for p in bundle['parts'] if p['name'] != omitted]
        try: validate_visible_mechanism(bad)
        except ValueError: results.append(omitted+' omission rejected')
        else: raise AssertionError('Missing-support negative control failed')
    bad = dict(bundle); bad['states'] = dict(bundle['states']); bad['states']['SERVICE'] = dict(bundle['states']['SERVICE']);bad['states']['SERVICE']['PF_PropR']=None
    try: validate_visible_mechanism(bad)
    except ValueError: results.append('SERVICE prop omission rejected')
    else: raise AssertionError('Service-state negative control failed')
    # Machining diameter changes cannot relax or break the ergonomic guard.
    validate_ergonomics(config['ergonomics'])
    return results

if __name__ == '__main__':
    bundle = json.loads((ROOT/'exports/generated/service-correction-v32/mesh.json').read_text())
    cfg = json.loads((ROOT/'config/service_correction_v32.json').read_text())
    validate_ergonomics(cfg['ergonomics']); validate_visible_mechanism(bundle)
    print('SERVICE_CORRECTION_CONTRACT_PASS', negative_controls(bundle, cfg))

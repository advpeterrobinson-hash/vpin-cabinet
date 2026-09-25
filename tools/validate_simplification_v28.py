"""Reconcile conditional deletions; acceptance/readiness and physical results must remain false."""
import copy,csv,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE='f2d18c7b475b7a4b5995e193eb5804cdc6cdab1e'
def load(p):return json.loads((ROOT/p).read_text())
def validate(ledger,features,state,geo):
 old=load('bom/PHYSICAL_VALIDATION_RESULTS_V27.json');measure={m['measurement_id']:m for c in old['components'] for m in c['measurements']};trials={t['test_id']:t for t in old['physical_trials']}
 assert state['status']=='PAUSED_BY_OWNER'
 assert ledger['execution_status']=='PAUSED' and not ledger['manufacturing_ready'] and not ledger['automatic_unlock']
 assert not features['manufacturing_ready'] and not geo['manufacturing_ready']
 m=ledger['measurements'];t=ledger['physical_trials'];assert len({x['id'] for x in m})==len(m);assert len({x['id'] for x in t})==len(t)
 assert {x['id'] for x in m if x['disposition']!='NEW'}==set(measure)
 assert {x['id'] for x in t if x['disposition']!='NEW'}==set(trials)
 for x in m:
  assert x['status']=='PAUSED' and x['measured_value'] is None
  if x['disposition']!='NEW':assert x['source_record']==measure[x['id']]
 for x in t:
  assert x['status']=='PAUSED' and x['result'] is None
  if x['disposition']!='NEW':assert x['source_record']==trials[x['id']]
 fs=features['features'];oldf={r['feature_id']:r for r in csv.DictReader((ROOT/'bom/CNC_FEATURES_V25.csv').open())}
 assert len({f['feature_id'] for f in fs})==len(fs)
 assert {f['feature_id'] for f in fs if f['disposition']!='NEW'}==set(oldf)
 for f in fs:
  if f['disposition']=='NEW':
   assert f['status'] in ('BLOCKED_MEASURE_HARDWARE','BLOCKED_DESIGN_REVIEW')
   assert f['x'] is None and f['y'] is None and f['diameter'] is None
  else:assert f['source_record']==oldf[f['feature_id']]
 active=[f for f in fs if f['disposition']!='OBSOLETE'];c=ledger['counts']
 assert len(active)==c['features_proposed']==201
 assert sum(f.get('original_status')=='BLOCKED_MEASURE_HARDWARE' or f['status']=='BLOCKED_MEASURE_HARDWARE' for f in active)==c['hardware_blockers_proposed']==58
 assert sum(x['disposition'] in ('KEEP','NEW') for x in m)==c['measurements_proposed']==169
 assert sum(x['disposition'] in ('KEEP','NEW') for x in t)==c['trials_proposed']==18
 assert not set(geo['proposed_names'])&set(geo['removed_names'])
 assert all(not n.startswith(('RearCPU','CPURail','PropRod','CarrierAngle')) for n in geo['proposed_names'])
 checks=geo['checks'];assert not checks['pc_out'] and not checks['pc_lift']
 for k in ('board_payload','brackets','bridge_brackets','holder_closed','board_removal','strap_free_paths'):assert all(not v for v in checks[k].values()),(k,checks[k])
 assert checks['sampled_holder_motion']==checks['inherited_display_motion'], 'new interference introduced beyond inherited display envelope'
 assert not checks['holder_open']
 assert checks['retained_CM3_conflict']==['LowCrossmember3V20']
 assert checks['straps']=={'SStrapL':['BackboxLeftSideV14'],'SStrapR':['BackboxRightSideV14']}
 assert all(s['torque_per_unit_tension_about_x']<0 for s in geo['straps'].values())
 assert all(geo['candidates']['SStop'+s]['kind']=='UNRESOLVED' for s in 'LR')
 assert geo['source_sha256']==hashlib.sha256((ROOT/'cad/active/vpin-active.FCStd').read_bytes()).hexdigest()

def main():
 args=[load('bom/PHYSICAL_VALIDATION_RESULTS_V28_PROPOSED.json'),load('bom/SIMPLIFICATION_FEATURE_IMPACT_V28.json'),load('bom/PHYSICAL_EXECUTION_STATE_V28.json'),load('exports/generated/simplification-v28/geometry.json')]
 validate(*args)
 # Every pre-existing authoritative config/register/doc/tool stays immutable.
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
 for p in paths:
  if p.startswith(('config/','bom/','docs/','tools/')):assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT),p
 mutations=[('measurement omitted',lambda a:a[0]['measurements'].pop(0)),('invented historic ID',lambda a:a[0]['measurements'][0].update(id='UNKNOWN')),('physical result invented',lambda a:a[0]['measurements'][0].update(measured_value=18)),('manufacturing claim',lambda a:a[0].update(manufacturing_ready=True)),('execution resumed',lambda a:a[2].update(status='ACTIVE')),('guessed new hole',lambda a:next(f for f in a[1]['features'] if f['disposition']=='NEW').update(x=10)),('deleted mechanism returns',lambda a:a[3]['proposed_names'].append('RearCPUSupportRailLeftV24')),('CM3 conflict concealed',lambda a:a[3]['checks'].update(retained_CM3_conflict=[]))]
 for name,mutate in mutations:
  a=copy.deepcopy(args);mutate(a)
  try:validate(*a)
  except AssertionError:print('SIMPLIFICATION_NEGATIVE_PASS',name)
  else:raise AssertionError('negative control accepted '+name)
 print('SIMPLIFICATION_VALIDATION_PASS: 186 historical measurements / 18 historical trials preserved; 169 / 18 proposed; 201 groups / 58 hardware dependencies; PAUSED')
if __name__=='__main__':main()

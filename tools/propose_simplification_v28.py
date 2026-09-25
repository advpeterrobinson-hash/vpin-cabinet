"""Generate a paused proposal and exhaustive ID impact maps, never edit v27 evidence."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'bom'
def read(name):return list(csv.DictReader((OUT/name).open()))
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
REMOVED_HW={'HF-013','HF-026','HF-028'}
REPLACED_HW={'HF-008','HF-009','HF-010','HF-018'}
DELETE_PARTS={'PC-SUPPORT-LEFT-R2','PC-SUPPORT-RIGHT-R2','CAB-XMEM-012-R1'}
REPLACE_PARTS={r['part_id'] for r in read('ACTIVE_PARTS.csv') if r['part_id'].startswith(('WOOD-','PF-LANDING'))}
NEW_MEASUREMENTS={
 'V28-PIVOT':('Stock cross-axis / plain bushes / common collars',[
 'Actual stock outside diameter', 'Stock straightness and cut length',
 'Stock material and documented load properties', 'Bush inside/outside diameter and flange/length',
 'Bush running fit in measured plywood', 'Collar/end-retention grip and tool access',
 'Complete pivot wood/washer/fastener stack and edge distances']),
 'V28-STRAP':('Two captive service restraint straps and independent anchors',[
 'Loaded and unloaded strap length', 'Strap width and end fitting dimensions',
 'Documented restraint capacity in selected direction', 'Anchor eye and bolt dimensions',
 'Washer/spreader bearing area and wood stack', 'Loaded stretch and service angle',
 'Stop contact, closed slack/stow and snagging envelope']),
 'V28-BOARD':('One commodity L-bracket family for boards/holder and ordinary fasteners',[
 'Both bracket leg lengths', 'Bracket thickness and bend radius',
 'Actual fixing hole/slot pattern', 'Documented bracket load and orientation',
 'Complete bracket/wood/bolt/nut/washer stack and screwdriver access']),
 'V28-RJ45':('Ordinary RJ45 bulkhead sample',[
 'Panel aperture and antirotation flats', 'Threaded grip and panel thickness range',
 'Flange nut washer gasket stack', 'Internal connector body depth',
 'External cap projection', 'Cap/tether opening sweep',
 'Ordinary plug boot/latch access on both sides', 'Internal and external cable bend envelopes'])}
TRIAL_REPLACEMENTS={
 'PV-PROP-L':('V28-RESTRAINT-L','Left strap/anchor independently retains full moving assembly with reviewed fixture/load/criteria'),
 'PV-PROP-R':('V28-RESTRAINT-R','Right strap/anchor independently retains full moving assembly with reviewed fixture/load/criteria'),
 'PV-PROP-MOTION':('V28-HOLDER-MOTION','Pivot/stop/strap slack, engagement, snagging and opening/closing clearance'),
 'SV-01':('V28-BOARDS','Independent removal of three boards with representative cables and ordinary tools'),
 'SV-03':('V28-PC-SERVICE','Floor base restraint and rear lift-out; no extended-slide proof'),
 'PV-LOADS':('V28-STRUCTURE','Two-crossmember shell, enlarged rear opening, floor PC base, pivot cheeks and board supports: reviewed structural qualification')}
NEW_PARTS=[('V28-PF-L','PERMANENT_STRUCTURE'),('V28-PF-R','PERMANENT_STRUCTURE'),('V28-PF-BRIDGE','PERMANENT_STRUCTURE'),('V28-PIVOT-L','PERMANENT_STRUCTURE'),('V28-PIVOT-R','PERMANENT_STRUCTURE'),('V28-LANDING-L','PERMANENT_STRUCTURE'),('V28-LANDING-R','PERMANENT_STRUCTURE')]

def main():
 ledger=json.loads((OUT/'PHYSICAL_VALIDATION_RESULTS_V27.json').read_text())
 measurements=[]
 for c in ledger['components']:
  h=c['component_id'];dis='OBSOLETE' if h in REMOVED_HW else ('REPLACED' if h in REPLACED_HW else 'KEEP')
  replacement={'HF-008':'V28-PIVOT','HF-009':'V28-PIVOT','HF-010':'V28-STRAP','HF-018':'V28-RJ45'}.get(h)
  for m in c['measurements']:
   measurements.append(dict(id=m['measurement_id'],component=h,required=m['required'],disposition=dis,
    reason=('Drawer/rail mechanism deleted; no corresponding fit remains' if dis=='OBSOLETE' else ('New mechanism/family; historic record superseded only if proposal accepted' if dis=='REPLACED' else 'Still needed; installation trial uses accepted architecture')),
    replacement_component=replacement,source_record=m,status='PAUSED',measured_value=None))
 for h,(title,items) in NEW_MEASUREMENTS.items():
  for i,item in enumerate(items,1):measurements.append(dict(id=f'{h}-M{i:02}',component=h,required=item,disposition='NEW',reason=title,status='PAUSED',measured_value=None))
 trials=[]
 for t in ledger['physical_trials']:
  new=TRIAL_REPLACEMENTS.get(t['test_id'])
  trials.append(dict(id=t['test_id'],purpose=t['purpose'],disposition='REPLACED' if new else 'KEEP',replacement_id=new[0] if new else None,source_record=t,status='PAUSED',result=None))
 for old,(new,purpose) in TRIAL_REPLACEMENTS.items():trials.append(dict(id=new,purpose=purpose,disposition='NEW',replaces=old,status='PAUSED',result=None,approved_fixture=None,approved_load=None,approved_acceptance_criteria=None))
 parts=[]
 for r in read('ACTIVE_PARTS.csv'):
  pid=r['part_id'];decision='DELETE' if pid in DELETE_PARTS else ('MERGE' if pid in REPLACE_PARTS else 'KEEP')
  if pid in ['CAB-REAR-001-R3','CAB-PC-REAR-DOOR-002-R1','PC-REAR-SHELF-002-R1']:decision='SIMPLIFY'
  parts.append(dict(part_id=pid,object_name=r['object_name'],classification=r['construction_class'],decision=decision,
   reason=('REQUIRES PROOF: CM3 removal enables floor PC base; qualify shell/bottom' if pid=='CAB-XMEM-012-R1' else ('Drawer load path deleted' if pid in DELETE_PARTS else ('Three-piece wood holder + two pivot cheeks + two landing blocks replace cradle/prop wood' if pid in REPLACE_PARTS else ('Ordinary rear door / floor base, no slides' if decision=='SIMPLIFY' else 'Retains independent shell, leg, backbox or service function'))))))
 features=[]
 for r in read('CNC_FEATURES_V25.csv'):
  removed=r['part_id'] in DELETE_PARTS|REPLACE_PARTS or r['hardware_dependency'] in REMOVED_HW|REPLACED_HW or 'CarrierMount' in r['recipe']
  # Side dado pair for removed CM3: exact original coordinate range, no new coordinates.
  removed=removed or ('1040.000' in r['notes'] and '1058.000' in r['notes'])
  features.append(dict(feature_id=r['feature_id'],part_id=r['part_id'],disposition='OBSOLETE' if removed else 'KEEP',hardware_dependency=r['hardware_dependency'],original_status=r['status'],status='SUPERSEDED_IF_ACCEPTED' if removed else 'REVIEW_REQUIRED',source_record=r))
 def feature(pid,kind,dep=''):
  features.append(dict(feature_id=f'V28-CF-{sum(x["disposition"]=="NEW" for x in features)+1:03}',part_id=pid,disposition='NEW',feature_type=kind,hardware_dependency=dep,status='BLOCKED_MEASURE_HARDWARE' if dep and dep!='HF-002' else 'BLOCKED_DESIGN_REVIEW',x=None,y=None,diameter=None))
 for pid,_ in NEW_PARTS:
  feature(pid,'PROFILE');feature(pid,'ENGRAVING')
  if 'PIVOT' in pid or pid in ('V28-PF-L','V28-PF-R'):feature(pid,'PIVOT_INTERFACE','V28-PIVOT')
  if pid in ('V28-PF-L','V28-PF-R'):feature(pid,'STRAP_ANCHOR','V28-STRAP');feature(pid,'CLOSED_RESTRAINT','HF-012')
  if 'LANDING' in pid:feature(pid,'PAD_LATCH','HF-012')
  feature(pid,'COMMON_FASTENER_INTERFACE','V28-BOARD' if pid in ('V28-PF-L','V28-PF-R','V28-PF-BRIDGE') else 'HF-002')
 for pid in ['CAB-SIDE-001L-R1','CAB-SIDE-001R-R1']:
  feature(pid,'PIVOT_CHEEK_MOUNT','V28-PIVOT');feature(pid,'SPARSE_BOARD_MOUNT','V28-BOARD')
 for pid in ['BB-SIDE-001L-R1','BB-SIDE-001R-R1']:feature(pid,'STRAP_ANCHOR','V28-STRAP')
 for pid in ['V28-BOARD-A','V28-BOARD-B','V28-BOARD-C']:
  feature(pid,'PROFILE');feature(pid,'ENGRAVING');feature(pid,'REMOVABLE_BOARD_MOUNT','V28-BOARD')
 feature('CAB-XMEM-010-R1','FRONT_BOARD_SUPPORT','V28-BOARD')
 feature('CAB-BOTTOM-001-R1','PC_BASE_RESTRAINT','HF-002')
 feature('PC-REAR-SHELF-002-R1','PC_BASE_RESTRAINT','HF-002')
 # Retained sources stay reference-only; no coordinates are production authoritative in proposal.
 proposed=[f for f in features if f['disposition']!='OBSOLETE']
 counts=dict(measurements_before=186,measurements_dispositions=dict(Counter(m['disposition'] for m in measurements)),measurements_proposed=sum(m['disposition'] in ('KEEP','NEW') for m in measurements),trials_before=18,trials_dispositions=dict(Counter(t['disposition'] for t in trials)),trials_proposed=sum(t['disposition'] in ('KEEP','NEW') for t in trials),features_before=len(read('CNC_FEATURES_V25.csv')),features_proposed=len(proposed),features_removed=sum(f['disposition']=='OBSOLETE' for f in features),features_added=sum(f['disposition']=='NEW' for f in features),hardware_blockers_before=59,hardware_blockers_proposed=sum((f.get('original_status')=='BLOCKED_MEASURE_HARDWARE' or f['status']=='BLOCKED_MEASURE_HARDWARE') for f in proposed),structural_register_before=29,structural_register_proposed=sum(p['classification']=='PERMANENT_STRUCTURE' and p['decision'] not in ('DELETE','MERGE') for p in parts)+len(NEW_PARTS))
 dump('PHYSICAL_EXECUTION_STATE_V28.json',dict(status='PAUSED_BY_OWNER',scope='ALL physical measurement sessions including v27 Session 0/1 and proof tests',reason='Architecture convergence; no execution until owner accepts architecture and revised workflow',manufacturing_ready=False))
 dump('PHYSICAL_VALIDATION_RESULTS_V28_PROPOSED.json',dict(status='PROPOSED_NOT_ACCEPTED',execution_status='PAUSED',manufacturing_ready=False,automatic_unlock=False,source_ledger='PHYSICAL_VALIDATION_RESULTS_V27.json',source_sha256=hashlib.sha256((OUT/'PHYSICAL_VALIDATION_RESULTS_V27.json').read_bytes()).hexdigest(),measurements=measurements,physical_trials=trials,counts=counts))
 dump('SIMPLIFICATION_FEATURE_IMPACT_V28.json',dict(status='PROPOSED_NOT_ACCEPTED',manufacturing_ready=False,features=features,counts=counts))
 dump('SIMPLIFICATION_PART_AUDIT_V28.json',dict(status='PROPOSED_NOT_ACCEPTED',parts=parts,new_structural_parts=NEW_PARTS,counts=counts))
 lines=['# V28 proposed evidence impact — execution PAUSED','','Generated by `tools/propose_simplification_v28.py`. KEEP means still required, never measured/passed. OBSOLETE/REPLACED apply only if the proposed architecture is accepted. V27 remains immutable history. New proof tests require reviewed fixtures, loads and criteria.','','| ID | Decision | Required evidence / reason | Replacement |','|---|---|---|---|']
 for m in measurements:lines.append(f'| {m["id"]} | {m["disposition"]} | {m["required"]} | {m.get("replacement_component") or "—"} |')
 lines+=['','## All physical trials','','| ID | Decision | Purpose | Replacement |','|---|---|---|---|']
 for t in trials:lines.append(f'| {t["id"]} | {t["disposition"]} | {t["purpose"]} | {t.get("replacement_id") or "—"} |')
 (ROOT/'docs/SIMPLIFICATION_EVIDENCE_IMPACT_V28.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(counts,indent=2))
if __name__=='__main__':main()

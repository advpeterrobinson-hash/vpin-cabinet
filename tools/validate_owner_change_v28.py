"""Validate isolated review evidence and unchanged authoritative baseline."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
BASE='7a9d408de3b8bc8a9aaa311a40a3f98211fe7af5'

def main():
 # Every existing authority file remains byte-identical, including generated queues.
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
 protected=[p for p in paths if p.startswith(('config/','bom/','docs/','tools/'))]
 for p in protected:
  assert (ROOT/p).read_bytes()==subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT),p+' changed'
 r=json.loads((ROOT/'exports/generated/owner-change-v28/review-analysis.json').read_text())
 assert not r['manufacturing_ready']
 assert r['source_sha256']==hashlib.sha256((ROOT/'cad/active/vpin-active.FCStd').read_bytes()).hexdigest()
 for b in r['boards'].values():
  for field in ('closed_conflicts','central_conflicts','removal_conflicts'):assert not b[field],(field,b[field])
 c=r['checks']
 for k,v in c['mains_MidLeft'].items():
  if k.endswith('conflicts'):assert not v,(k,v)
 assert all(not v for v in c['support_conflicts'].values())
 # Negative geometry controls are actual rejected CAD volumes, not fabricated success flags.
 assert 'CentralServiceKeepoutV27' in c['spanning_board_conflict']
 assert 'CentralServiceKeepoutV27' in c['mains_Central']['aisle_conflicts']
 assert 'ReviewBoardF' in c['mains_Front']['lid_board_conflicts']
 assert 'ReviewSupportFL' in c['mains_Front']['support_conflicts']
 assert 'MovingHarnessKeepoutV18' in c['rj45_side_internal_conflicts']
 assert 'ControlLeftActionInternalV27' in c['original_depth_payload_conflicts']
 for o in r['inventory']:
  if o['provisional']:assert o['role']=='DESIGN_PROVISIONAL'
 rows=list(csv.DictReader((ROOT/'bom/CNC_FEATURES_V25.csv').open()))
 assert len(rows)==232 and sum(x['status']=='BLOCKED_MEASURE_HARDWARE' for x in rows)==59
 print(f'OWNER_CHANGE_VALIDATION_PASS: {len(protected)} authority files unchanged; 3 board paths; 6 negative collision controls; 59 blockers remain')
if __name__=='__main__':main()

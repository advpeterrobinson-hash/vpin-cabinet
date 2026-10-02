"""Active datum regression plus classified historical audit. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy,re,subprocess
from wpc_reference_v32 import reference_axis
R=Path(__file__).resolve().parents[1]
marker='SUPERSEDED — INCORRECT LONGITUDINAL PIVOT INTERPRETATION'
c=json.loads((R/'config/wpc_kinematics_v32.json').read_text())
assert reference_axis(c)==[300,1066.8,508]
for offset in [38.1,241.0]:
 bad=copy.deepcopy(c);bad['pivot_from_rear_mm']=offset;bad['axis_xyz_mm']=[300,1308.1-offset,508]
 try:reference_axis(bad)
 except ValueError:pass
 else:raise AssertionError('stale datum accepted')
for name,key in [('backbox_fold_v10.json','cabinet'),('structure_geometry_v14.json','wpc_hinges')]:
 cfg=json.loads((R/'config'/name).read_text());p=cfg[key]
 assert p['pivot_from_rear_mm']==241.3 and p['pivot_from_bottom_mm']==508
 assert [300,1308.1-p['pivot_from_rear_mm'],p['pivot_from_bottom_mm']]==reference_axis()
 assert cfg['manufacturing_ready'] is False
r=json.loads((R/'config/backbox_structure_review_v32.json').read_text())
assert r['kinematic_reference']['axis_xyz_mm']==reference_axis()
assert r['hardware']['final_holes_frozen'] is False
assert r['backbox']['side_lower_depth_mm']==210
assert set(r['service_passage'])=={'width','depth','x_position','y_position','status'}
# Explicit coverage: source-data quotations / snapshots are not executable authority.
files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=R,text=True).splitlines()
rows=[]
for name in files:
 if name=='studies/backbox-structure-v32/pivot-audit.json':continue
 if not (name.startswith(('config/','tools/','docs/','research/','studies/')) or name=='exports/generated/cabinet-v32/build_v32.py'):continue
 if Path(name).suffix not in ['.py','.json','.md']:continue
 text=(R/name).read_text()
 found=[]
 for i,line in enumerate(text.splitlines(),1):
  if not re.search(r'1270|38\.1|1\.5.in|1-1/2|1½',line):continue
  if name.startswith('studies/wpc-fold-v32/'):
   cls='C. THIRD-PARTY SOURCE QUOTATION' if name.endswith('sources.json') and ('README says' in line or 'github.com' in line) else 'B. HISTORICAL / AUDIT (positive-control negative comparison)'
  elif name=='config/consolidated_audio_v32.json' or 'SIDE_BUTTON_OPTIONS' in name or 'LIGHTING_INTENT' in name or 'PINSIM' in name or 'history/REAR_UTILITY' in name:
   cls='NON-PIVOT DIMENSION / URL'
  elif marker in text or (name.endswith('.json') and marker in str(json.loads(text))):cls='B. HISTORICAL / AUDIT — marked superseded'
  elif name.startswith('studies/backbox-structure-v32/') or name in ['tools/check_wpc_reference_v32.py','tools/check_backbox_structure_v32.py']:
   cls='B. HISTORICAL / AUDIT (superseded comparison or negative regression control)'
  elif name=='tools/backbox_structure_review_v32.py' and '1270' in line:
   cls='B. HISTORICAL / AUDIT (repair obsolete hole in isolated candidate only)'
  elif name=='config/backbox_structure_review_v32.json' and '1270' in line:
   cls='NON-PIVOT DIMENSION: rearmost floor fastener, explicitly not axis'
  elif name=='config/backbox_fold_v10.json' and ('1270' in line):cls='NON-PIVOT DIMENSION: rearmost floor fastener, explicitly not axis'
  elif name=='tools/render_matrix_hinge_study_v32.py':cls='B. HISTORICAL / AUDIT'
  else:
   # Noise includes old tests of fixed-datum study; code still belongs to that study.
   if any(k in name for k in ['check_backbox_profile','check_backbox_floor']):cls='B. HISTORICAL / AUDIT (saved-artifact verifier)'
   else:cls='NON-PIVOT DIMENSION / unrelated wording'
  found.append({'line':i,'classification':cls,'text':line[:400]})
 if found:rows.append({'path':name,'occurrences':found})
# Narrow active allowlist: both legacy compatibility configs, central authority,
# checker, corrected package source and the new candidate geometry source.
active=['config/wpc_kinematics_v32.json','config/backbox_fold_v10.json','config/structure_geometry_v14.json','config/backbox_structure_review_v32.json','tools/wpc_reference_v32.py','tools/build_structure_v14.py','tools/validate_backbox_fold_v10.py','tools/backbox_structure_review_v32.py','tools/backbox_structure_review_v32_entry.py']
# Detect reintroduction into any actual rotation vector in active executable code.
for name in active:
 text=(R/name).read_text()
 assert not re.search(r'(?:rotate|axis\s*=).*1270',text),name
 assert not re.search(r'"pivot_from_rear_mm"\s*:\s*38\.1',text),name
payload={'active_engineering_files':active,'active_stale_pivot_references_remaining':0,'negative_controls':['reject 38.1 offset / Y1270','reject drifted offset','legacy config consistency','final drilling remains provisional'],'historical_replay_rule':'Use original source HEAD for historical outputs; do not regenerate them as CURRENT geometry.','occurrences':rows,'accepted_geometry_note':'Old reference bore still exists in unchanged accepted CAD snapshots; it is explicitly retired as engineering/drilling authority. No production geometry promoted.'}
(R/'studies/backbox-structure-v32/pivot-audit.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
print('WPC_ACTIVE_DATUM_PASS stale_active=0 classified_files='+str(len(rows)))

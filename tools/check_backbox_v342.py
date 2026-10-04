"""V34.2 CURRENT regression gate; no manufacturing release. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,gzip,subprocess
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v342';checks=[]
def j(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(n,b):checks.append({'name':n,'pass':bool(b)});assert b,n
g=j(O/'geometry-validation.json');i=j(O/'independent-validation.json');b=j(O/'browser-validation.json');r=j(O/'manufacturing-register.json');c=j(R/'config/backbox_hardening_v342.json');h=j(R/'config/hardware_catalog_v342.json');mass=j(O/'mass-counts.json');v=j(O/'viewer-authority.json');manual=j(O/'assembly-manual.json')
for name,data in [('native',g),('independent',i),('browser',b)]:ck(name,data['pass'] and all(a['pass'] for a in data['checks']))
ck('native independent evidence bound',i['native_sha256']==sha(O/'candidate.FCStd'))
ck('viewer bound',b['viewer_sha256']==sha(R/'exports/generated/viewer-v32/index.html')==v['html_sha256'])
ck('source baseline bound',g['source_sha256']==sha(R/'exports/generated/backbox-v34/play.FCStd'))
ck('hardware IDs unique',len(h['hardware'])==len({a['id'] for a in h['hardware']}))
ck('stocks exactly12/18',{a['nominal_stock_thickness_mm'] for a in r['parts'] if a['nominal_stock_thickness_mm'] is not None}=={12,18})
ck('66wood60CNC45families',r['manufacturing_pieces']==66 and r['CNC_plywood_pieces']==60 and r['canonical_families']==45)
ck('canonical family has one stock',all(len({a['nominal_stock_thickness_mm'] for a in r['parts'] if a['manufacturing_part_id']==f})==1 for f in {a['manufacturing_part_id'] for a in r['parts']}))
ck('no baffles shelves in CURRENT wood',not any(a['source_component'].startswith(('BB_Intake','BB_Shelf')) for a in r['parts']))
ck('zero changed reconstruction',mass['reconstruction_max_mm3']<1e-6)
ck('exact monitor unknowns held',c['monitor']['VESA_location_on_actual_TV'] is None and c['monitor']['production_slot_width_mm'] is None and c['monitor']['production_screw_length_mm'] is None)
ck('reference geometry not hardware release',g['actual_TCL_boss_compatibility']=='HOLD_PHYSICAL_MEASUREMENT' and not c['manufacturing_release'] and not h['manufacturing_ready'])
ck('thin boss negative control fails',all(not x['pass'] for x in g['TV_depth_cases'] if x['case']=='thin_boss_limit'))
ck('four VESA slots30travel',c['monitor']['primary_VESA_mm']==100 and c['monitor']['vertical_travel_mm']==15)
ck('acrylic final fit held',c['acrylic']['selected_reference_mm']==3 and c['acrylic']['final_thickness_mm'] is None and c['acrylic']['mask_final_size_mm'] is None)
ck('glass final cut held',c['playfield_glass']['stock_mm']==5 and c['playfield_glass']['final_cut_mm'] is None and not c['playfield_glass']['whole_floor_tilted'])
ck('30 rendered native CAD views',len(j(O/'review-index.json'))==30 and all((O/(f'{n:02d}-review.png')).exists() for n in range(1,31)))
ck('59 manual steps',sum(len(s['steps']) for s in manual['stages'])==59)
# Prior sources and generated engineering packages must remain byte-identical.
protected=['config/backbox_simplification_v34.json','config/service_productization_v338.json','exports/generated/backbox-v34','exports/generated/service-productization-v338']
for f in protected:
 changes=subprocess.check_output(['git','diff','8d951bc37a38d5e3820cbde93700f1161ff32fb1','--',f],cwd=R)
 ck('historical/protected source '+f,not changes)
evidence=[O/x for x in ['candidate.FCStd','play.FCStd','geometry-validation.json','independent-validation.json','browser-validation.json','manufacturing-register.json','mass-counts.json','viewer-authority.json','sources.json','tukkari-first-audit.json','assembly-manual.json','review-index.json']]+[R/x for x in ['config/backbox_hardening_v342.json','config/hardware_catalog_v342.json','config/manufacturing/flatpack_v342.json','tools/backbox_hardening_v342.py','tools/backbox_v342_common.py','tools/check_backbox_v342_native.py','tools/backbox_v342_manufacturing.py','tools/backbox_v342_export.py','tools/build_viewer_v342.py','tools/viewer_v342_study.html']]
report={'version':'V34.2','pass':True,'head_before':c['head_before'],'checks':checks,'counts':{'native':len(g['checks']),'independent':len(i['checks']),'browser':len(b['checks']),'regression':len(checks)},'manufacturing_ready':False,'actual_hardware_qualification':False,'viewer_sha256':sha(R/'exports/generated/viewer-v32/index.html'),'evidence_sha256':{str(p.relative_to(R)):sha(p) for p in evidence},'promotion_scope':'REFERENCE_GEOMETRY_DESIGN_CANDIDATE_ONLY; actual TV bosses, mask, channels/lockdown, material/coupon and structural qualification HOLD'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V342_PASS',report['counts'])

"""V34 derived-evidence and source-protection gate. CERN-OHL-S-2.0."""
from pathlib import Path
import json,hashlib,subprocess,gzip,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/backbox-v34';HEAD='0993d9768582290915f7166c53507ffd2aa434b6';checks=[]
def J(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(v,n):checks.append({'name':n,'pass':bool(v)});assert v,n
def j(n):return json.loads((O/n).read_text())
g=j('geometry-validation.json');i=j('independent-validation.json');b=j('browser-validation.json');reg=j('manufacturing-register.json');v=j('viewer-authority.json');d=j('manufacturing-delta.json')
for n,a in [('geometry',g),('independent',i),('browser',b)]:ck(a['pass'] and all(c['pass'] for c in a['checks']),n+' checks all pass')
ck(i['native_sha256']==v['native_sha256']==sha('exports/generated/backbox-v34/play.FCStd'),'native evidence matches')
ck(b['viewer_sha256']==v['html_sha256']==sha('exports/generated/viewer-v32/index.html'),'browser evidence matches current viewer')
ck(g['source_sha256']==i['source_sha256']==sha('exports/generated/service-productization-v338/play.FCStd'),'source native unchanged')
ck(reg['manufacturing_pieces']==len(reg['parts'])==76,'76 manufacturing pieces')
ck(reg['canonical_families']==len({a['manufacturing_part_id'] for a in reg['parts']})==48,'48 families')
ck(reg['CNC_families']==46,'46 plywood plus2 solid families')
ck(set(a['nominal_stock_thickness_mm'] for a in reg['parts'] if a.get('manufacturing_class')!='SHOP_MADE_SOLID_WOOD_PART')=={12,18},'exactly12/18 plywood')
ck(d['reconstruction_max_mm3']<1e-3,'native reconstruction tolerance')
ck(not any(a.get('manufacturing_release') for a in [g,i,reg]),'CNC remains held')
manual=j('assembly-manual.json');steps=[s for st in manual['stages'] for s in st['steps']]
ck(len([s for s in steps if s['id'].startswith('08.')])==25,'25 owner backbox steps')
ck(all(s['status'] in ['READY','PROVISIONAL_HARDWARE','WAITING_FOR_PHYSICAL_MEASUREMENT','WAITING_FOR_COUPON','OPTIONAL'] for s in steps),'manual statuses honest')
inv=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));ck(not(set(g['retired'])&{a['key'] for a in inv['installed']}),'retired native names absent viewer')
ck(not(set(d['retired_hardware_ids'])&{a['meta'].get('hardware_id') for a in inv['detail']}),'retired hardware absent detailed viewer')
# Protect all prior authority artifacts, not only the single native assembly file.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',HEAD,'exports/generated/service-productization-v338','config/service_productization_v338.json','config/solid_front_landings_v338.json','config/underfront_user_module_v337.json','config/plywood_conversion_v337.json','config/wpc_kinematics_v32.json','config/manufacturing/profiles/peter_supplier_v1.json'],cwd=R,text=True).splitlines()
for p in paths:
 before=subprocess.check_output(['git','show',HEAD+':'+p],cwd=R);ck(hashlib.sha256(before).hexdigest()==sha(p),'protected file '+p)
evidence=[str(p.relative_to(R)) for p in O.iterdir() if p.is_file() and p.suffix in ['.json','.gz','.brep','.FCStd','.png','.html','.md','.csv'] and p.name not in ['validation.json','promotion.json']]
evidence+=['config/backbox_simplification_v34.json','config/hardware_catalog_v34.json','config/manufacturing/flatpack_v34.json','config/wood_materials_v34.json','config/viewer_v34.json','docs/ASSEMBLY_MANUAL.md','docs/ASSEMBLY_MANUAL.pt-BR.md']
evidence += [str(p.relative_to(R)) for p in (R/'tools').glob('*v34*') if p.is_file()]
report={'pass':True,'head_before':HEAD,'checks':checks,'native_checks':len(g['checks']),'independent_checks':len(i['checks']),'browser_checks':len(b['checks']),'native_sha256':i['native_sha256'],'viewer_sha256':b['viewer_sha256'],'evidence_sha256':{p:sha(p) for p in evidence},'manufacturing_ready':False,'physical_qualification':False,'promotion_scope':'SIMPLIFIED_BACKBOX_DESIGN_CANDIDATE_ONLY'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V34_GATE_PASS',len(checks),'source gates; native',len(g['checks']),'independent',len(i['checks']),'browser',len(b['checks']))

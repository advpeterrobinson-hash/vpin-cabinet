"""V33.7 exact scope, two-stock and offline documentation regression.
CERN-OHL-S-2.0. Does not authorize CNC, selected controls or physical qualification.
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,collections,re
from validate_plywood_stock_v337 import validate_stock_policy,negative_controls
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/two-stock-user-module-v337';P=str(O.relative_to(R))+'/';checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/underfront_user_module_v337.json');geo=read(P+'geometry-validation.json');reg=read(P+'manufacturing-register.json');audit=read(P+'manufacturing-audit.json');browser=read(P+'browser-validation.json');MM=read(P+'module-motion.json')
combined=read(P+'combined-validation.json');ck('complete combined system gate passes',combined['pass']);
for name,h in combined['native_inputs_sha256'].items():ck('combined input '+name,sha(P+name)==h)
ck('combined gate exactnative',combined['native_sha256']==sha(P+'play.FCStd'));
ck('native geometry valid',geo['pass']);ck('one-face manufacturing audit passes',audit['pass']);ck('browser passes',browser['pass']);ck('prior source immutable',sha(C['source'])==geo['source_sha256']);ck('native manufacturing current',audit['native_geometry_sha256']==sha(P+'play.FCStd'));ck('browser current HTML',browser['viewer_sha256']==sha('exports/generated/viewer-v32/index.html'))
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));ck('native mesh current',N['source_sha256']==sha(P+'play.FCStd'))
if N.get('variant_source'):ck('variant native source current',sha(N['variant_source']['path'])==N['variant_source']['sha256'])
for state,v in N['files'].items():ck('native state input '+state,sha(v['path'])==v['sha256'])
for v in read(P+'metrics-authority.json')['sources']:ck('metrics source '+v['path'],sha(v['path'])==v['sha256'])
ck('prior browser inheritance honest',browser['inherited']['sha256']==sha(browser['inherited']['path']))
oldreg=read('exports/generated/front-landings-v3363/manufacturing-register.json');old={p['instance_id']:p for p in oldreg['parts']};new={p['instance_id']:p for p in reg['parts']};thin={p['instance_id'] for p in old.values() if p['nominal_stock_thickness_mm'] in [6,8]};changedwood={p['source_component'] for p in old.values() if p['instance_id'] in thin};ck('exact15 previous thin pieces',len(thin)==15)
stock_policy=read('config/manufacturing/stock_policy_v337.json');stock_evidence=read(P+'stock-policy-negative-control.json')
ck('permanent two-stock policy passes',validate_stock_policy(reg['parts'],stock_policy)==stock_evidence['positive'])
ck('forbidden stock negative controls reproduced',negative_controls(reg['parts'],stock_policy)['checks']==stock_evidence['checks'] and stock_evidence['pass'])
for field,path in [('native_sha256',P+'play.FCStd'),('register_sha256',P+'manufacturing-register.json'),('validator_sha256','tools/validate_plywood_stock_v337.py'),('policy_sha256','config/manufacturing/stock_policy_v337.json')]:ck('two-stock evidence '+field,stock_evidence[field]==sha(path))
ck('all old manufacturing instances retained',set(old)<=set(new));ck('only12and18nominal plywood',{p['nominal_stock_thickness_mm'] for p in new.values() if p['manufacturing_part_id']!='SW01'}=={12,18})
for k,p in old.items():
 if k in thin:ck('converted12mm '+k,new[k]['nominal_stock_thickness_mm']==12)
 elif p['source_component']!='FLOOR':ck('unrelated manufacturing row unchanged '+k,new[k]==p)
ck('only scoped native changes',set(N['changed'])<=changedwood|{'FLOOR'}|{n for n in N['changed'] if n.startswith('Underfront')})
ck('only new module objects',all(n.startswith('Underfront') for n in N['added']));ck('no old native removal',not N['removed'])
ck('one face only',all(not p.get('opposite_face_cnc') and not p.get('blockers') for p in new.values()))
cat=read('config/hardware_catalog_v337.json');hc={h['id']:h for h in cat['hardware']}
for h in read('config/hardware_catalog_v3363.json')['hardware']:ck('old hardware family unchanged '+h['id'],hc[h['id']]==h)
ck('no manufacturing release',not C['manufacturing_release'] and not audit['manufacturing_release'])
ck('final module cut interfaces unknown',MM['final_interface_status']['button_bore_mm'] is None and MM['final_interface_status']['usb_cutout'] is None)
ck('multiple samebay alternatives',len(MM['variants'])>=3 and MM['default_variant'] in [v['id'] for v in MM['variants']])
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));oldD=json.loads(gzip.decompress((R/'exports/generated/front-landings-v3363/viewer-data.json.gz').read_bytes()));G=D['geometry'];installed={a['key']:a for a in D['installed']};detail={a['key']:a for a in D['detail']};owned=set(N['changed'])|set(N['added'])
for a in oldD['installed']:
 if a['key'] not in owned:ck('unchanged installed mesh '+a['key'],G[installed[a['key']]['geometry']]==oldD['geometry'][a['geometry']])
for a in oldD['detail']:
 if a['key'] not in thin and a['meta'].get('source')!='FLOOR':ck('unchanged detail mesh '+a['key'],G[detail[a['key']]['geometry']]==oldD['geometry'][a['geometry']])
for state,e in oldD['states'].items():
 for n,g in e.items():
  if n not in owned:ck('unchanged named pose '+state+'/'+n,D['states'][state][n]==g)
for k in thin:ck('detailed converted stock '+k,detail[k]['meta']['thickness']==12)
for n in owned:ck('current changed/new authority '+n,installed[n]['meta']['geometry_authority']['sha256']==sha(P+'play.FCStd'))
ck('new visibility group',any(g['id']=='underfront' for g in D['groups']));ck('support architecture unchanged',D['landings']['architecture_pass'])
html=(R/'exports/generated/viewer-v32/index.html').read_text();Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',html,re.S).group(1));ck('oldfixedfunctionschematic removed','Unlocated owner-authorized under-front schematic' not in html and '<text x="60" y="85">MASTER VOLUME' not in html)
ck('all exact packing IDs',set(Q['pieces'])==set(new));ck('module variant contract exact',D['underfront']==Q['motions']['underfront']==MM)
for id in ['assembly-07.3','service-underfront','service-pf-close','service-pf-release']:ck('scoped service/manual clip '+id,any(c['id']==id for c in Q['clips']))
manual=read(P+'assembly-manual.json');steps={t['id']:t for s in manual['stages'] for t in s['steps']}
ck('unique manual IDs',len(steps)==sum(len(s['steps']) for s in manual['stages']))
ck('unique animation IDs',len({c['id'] for c in Q['clips']})==len(Q['clips']))
for lang in ['en','pt-BR']:
 ck('new module manualhardwarehold '+lang,'HARDWARE_PENDING' in steps['07.3']['hold'][lang] and 'null' in steps['18.1']['hold'][lang]);ck('rearfrontsupport retained '+lang,'−3' in steps['06.3']['action'][lang])
for lang,path in [('en','docs/ASSEMBLY_MANUAL.md'),('pt','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 t=(R/path).read_text();marker='REFERENCE ONLY / PURCHASE BEFORE CNC' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC';ck('eightheldsidebuttonops '+lang,t.count(marker)>=8)
packing=read(P+'packaging.json');selected=next(c for c in packing['candidates'] if c['target_kg']==packing['preferred_target_kg']);flat=[p['instance_id'] for b in selected['bundles'] for l in b['layers'] for p in l['pieces']];ck('packing uses preferred target',html.count('target_kg===Q.packaging.preferred_target_kg')==3 and 'target_kg===25' not in html);ck('eachpackingmemberonce',collections.Counter(flat)==collections.Counter(new.keys()));ck('highdensitymax25kg',all(b['gross_high_density_kg']<=25 for b in selected['bundles']))
review=read(P+'review-index.json');review_hashes=read(P+'review-source-hashes.json')
ck('complete24 actual CAD reviews',len(review)==24 and len({v['image'] for v in review})==24 and all(v.get('native_cad') for v in review))
for v in review:ck('review PNG present '+v['image'],(O/v['image']).is_file() and (O/v['image']).read_bytes()[:8]==b'\x89PNG\r\n\x1a\n')
ck('review authority source coverage',len(review_hashes)==129)
for p,h in review_hashes.items():ck('review source '+p,sha(p)==h)
protected=['exports/generated/front-landings-v3363','config/front_landings_v3363.json','config/manufacturing/flatpack_v3363.json','config/viewer_v3363.json','config/hardware_catalog_v3363.json','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','config/button_relief_v3361.json','config/service_io_v08.json','docs/SERVICE_IO_V08.md']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--',*protected],cwd=R,text=True).splitlines();prior_tools=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','tools'],cwd=R,text=True).splitlines();paths += [p for p in prior_tools if 'v3363' in Path(p).name]
for p in paths:ck('protected '+p,hashlib.sha256(subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R)).hexdigest()==sha(p))
report={'pass':True,'scope':'Two-stock geometry and generic user-module documentation; controls, physical qualification and CNC remain held.','checks':checks,'native_sha256':sha(P+'play.FCStd'),'viewer_sha256':browser['viewer_sha256'],'browser_checks':len(browser['checks']),'closed_position_support_valid':True,'physical_qualification_complete':False,'manufacturing_ready':False,'evidence_sha256':{n:sha(P+n) for n in ['geometry-validation.json','combined-validation.json','manufacturing-audit.json','browser-validation.json','viewer-native.json.gz','state-register.json','module-motion.json','assembly-manual.json','metrics-authority.json','manufacturing-register.json','stock-policy-negative-control.json','review-index.json','review-source-hashes.json']+[v['image'] for v in review]}}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V337_REGRESSION_PASS',len(checks),'browser',len(browser['checks']),'CNC BLOCKED')

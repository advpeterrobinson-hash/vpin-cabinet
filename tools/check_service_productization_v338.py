"""V33.8 scoped engineering/documentation regression. CERN-OHL-S-2.0.
Pass means evidence is complete and honest; it never releases unsupported
raised service, an unselected strap/harness, purchased hardware or CNC.
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,collections,re
from validate_plywood_stock_v338 import validate_stock_policy,negative_controls
R=Path(__file__).resolve().parents[1];P='exports/generated/service-productization-v338/';O=R/P;B='exports/generated/two-stock-user-module-v337/'
checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/service_productization_v338.json');g=read(P+'geometry-validation.json');audit=read(P+'manufacturing-audit.json');reg=read(P+'manufacturing-register.json');oldreg=read(B+'manufacturing-register.json');a=read(P+'adjustment-validation.json');ret=read(P+'retention-decision.json');safety=read(P+'safety-validation.json');mod=read(P+'modularity-validation.json');browser=read(P+'browser-validation.json')
native=sha(P+'play.FCStd');qa=read(P+'independent-qa.json')
ck('independent review passes',qa['pass'] and qa['native_sha256']==native)
for p,h in qa['source_sha256'].items():ck('independent QA input '+p,sha(p)==h)
for name,q in [('geometry',g),('manufacturing',audit),('adjustment',a),('safety evidence',safety),('modularity',mod),('browser',browser)]:ck(name+' evidence passes',q['pass'])
ck('native current',g['native_sha256']==audit['native_geometry_sha256']==native)
ck('previous native unchanged',g['source_sha256']==sha(C['source']))
ck('candidate adjustment authority',a['source_sha256']==sha(P+'landing-candidate.FCStd'))
ck('retention decision bound to final native',ret['source_sha256']['native']==native)
for p,h in audit['input_sha256'].items():ck('manufacturing input '+p,sha(p)==h)
for row in g['unchanged_objects']:ck('unrelated object unchanged '+row['name'],row['pass'])
ck('six layers and four binder screws only removed',len(g['removed_names'])==10 and all('_Layer' in n or '_LaminationScrew' in n for n in g['removed_names']))
ck('exact two solid landing additions',set(g['added_names'])=={'FrontLandingL_Block','FrontLandingR_Block'})
ck('no other native change',not g['changed_existing'])
for q in g['SW02']:
 ck('only obsolete holes filled '+q['side'],abs(q['symmetric_difference_mm3']-q['filled_binder_mm3'])<1e-5)
 ck('functional external envelope '+q['side'],all(abs(v-w)<1e-7 for v,w in zip([q['bounds_mm'][3+i]-q['bounds_mm'][i] for i in range(3)],[68,70,54])))
for q in audit['changed_audits']:ck('manufacturing reconstruction '+q['instance_id'],q['installed_reconstruction_difference_mm3']<1e-5 and q['old_functional_wood_removed_mm3']<1e-5 and q['restored_outside_obsolete_binder_corridors_mm3']<1e-5)
for q in audit['unchanged_wood_geometry']:ck('unrelated wood B-rep '+q['source_component'],q['difference_mm3']<1e-5)
old={p['instance_id']:p for p in oldreg['parts']};new={p['instance_id']:p for p in reg['parts']};retired={k for k in old if k.startswith(('P095-Layer','P096-Layer'))}
ck('piece family counts',len(new)==104 and reg['CNC_plywood_pieces']==98 and len(reg['families'])==61 and reg['shop_solid_wood_parts']==6)
ck('exact six retired manufacturing layers',len(retired)==6 and set(old)-set(new)==retired and set(new)-set(old)=={'P095-Solid','P096-Solid'})
for k,p in old.items():
 if k not in retired:ck('unrelated manufacturing row '+k,p==new[k])
policy=read('config/manufacturing/stock_policy_v338.json');neg=read(P+'stock-policy-negative-control.json')
ck('two stock positive',validate_stock_policy(reg['parts'],policy)==neg['positive'])
ck('forbidden stock negative controls',negative_controls(reg['parts'],policy)['checks']==neg['checks'] and neg['pass'])
for field,path in [('native_sha256',P+'play.FCStd'),('register_sha256',P+'manufacturing-register.json'),('validator_sha256','tools/validate_plywood_stock_v338.py'),('policy_sha256','config/manufacturing/stock_policy_v338.json')]:ck('stock evidence '+field,neg[field]==sha(path))
ck('no second-face CNC',all(not p.get('opposite_face_cnc') for p in reg['parts']))
ck('mechanical travel distinguished from installed margin',a['hardware_travel_reference_mm']==[-3,3] and a['geometric_common_height_setup_window_mm']==[-1.9,.9] and C['adjustment']['final_safe_range_mm']==[-1.9,.9])
ck('continuous adjustment margin',a['continuous_certificate']['margin_mm']==1 and len(a['continuous_certificate']['intervals'])>0)
ck('nominal slope preserved',a['nominal_play_slope_deg']==9.906669 and a['nominal_pose_delta_mm']==0 and not a['user_selectable_slope'] and not a['independent_L_R_twist_permitted'])
ck('negative travel collision retained as evidence',a['samples'][0]['hits'] and a['samples'][-1]['hits'])
ck('retention A selected',ret['selected_option']=='A' and ret['tool_required'] and ret['B']['decision']=='PACKAGING_PASS_NOT_PROMOTED' and not ret['C']['viable_candidate'])
ck('no unsupported strap promotion',not safety['promoted'] and safety['promoted_strap_count']==0 and not safety['secondary_restraint_validated'] and not safety['normal_service_load_bearing'])
ck('primary support deficiency exposed',not safety['acceptance_gates']['normal_primary_support_defined'])
ck('zero permanent hardpoint changes',mod['permanent_holes_added']==0 and mod['minimum_bom_additions']==0)
ck('backbox universal harness not falsely passed','HOLD' in mod['backbox_route_status'])
under=read('config/underfront_user_module_v337.json');ck('underfront device cuts still null',under['button']['BUTTON_BORE_MM'] is None and under['usb']['USB_CUTOUT_DIAMETER_MM'] is None)
cat=read('config/hardware_catalog_v338.json');hc={h['id']:h for h in cat['hardware']};prev=read('config/hardware_catalog_v337.json')
for h in prev['hardware']:
 if h['id']=='H27':
  ck('H27 documentation only', {k:v for k,v in h.items() if k!='notes'}=={k:v for k,v in hc['H27'].items() if k!='notes'})
  ck('H27 installed window explicit','1.9' in str(hc['H27']['notes']) and '0.9' in str(hc['H27']['notes']))
 elif h['id']!='F60':ck('unchanged hardware '+h['id'],hc[h['id']]==h)
life=read(P+'hardware-lifecycle.json');ck('four binder screws retired without invented hardware',life['retired_required']==[{'id':'F60','before':4,'after':0}] and life['new_required_hardware']==0)
ck('browser tests current HTML',browser['viewer_sha256']==sha('exports/generated/viewer-v32/index.html'))
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));ck('native viewer bound to current',N['source_sha256']==native)
for state,q in N['files'].items():ck('viewer state '+state,sha(q['path'])==q['sha256'])
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));oldD=json.loads(gzip.decompress((R/(B+'viewer-data.json.gz')).read_bytes()));G=D['geometry'];inst={q['key']:q for q in D['installed']};detail={q['key']:q for q in D['detail']}
for q in oldD['installed']:
 if q['key'] not in g['removed_names']:ck('installed viewer shape '+q['key'],G[inst[q['key']]['geometry']]==oldD['geometry'][q['geometry']])
for q in oldD['detail']:
 if q['key'] in detail and q['key'] not in retired:ck('detail viewer shape '+q['key'],G[detail[q['key']]['geometry']]==oldD['geometry'][q['geometry']])
ck('SW02 detailed pieces present',all(k in detail for k in ['P095-Solid','P096-Solid']))
ck('retired wood absent from detailed current',not any(k in detail for k in retired))
for state,rows in oldD['states'].items():
 for n,t in rows.items():
  if n not in g['removed_names']:ck('unchanged state pose '+state+'/'+n,D['states'][state][n]==t)
manual=read(P+'assembly-manual.json');steps=[t for st in manual['stages'] for t in st['steps']];ck('unique manual steps',len({t['id'] for t in steps})==len(steps))
for st in manual['stages']:
 ck('retired pieces absent manual stage '+st['id'],not retired.intersection(st.get('pieces',[])))
for lang,path in [('en','docs/ASSEMBLY_MANUAL.md'),('pt-BR','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 t=(R/path).read_text();ck('SW02 bilingual manual '+lang,'SW02' in t and ('1.9' in t or '1,9' in t) and ('0.9' in t or '0,9' in t))
for q in read(P+'metrics-authority.json')['sources']:ck('metrics input '+q['path'],sha(q['path'])==q['sha256'])
pack=read(P+'packaging.json');plan=next(q for q in pack['candidates'] if q['target_kg']==pack['preferred_target_kg']);packed=[p['instance_id'] for b in plan['bundles'] for l in b['layers'] for p in l['pieces']]
ck('each minimum part packed once',collections.Counter(packed)==collections.Counter(new.keys()))
ck('preferred bundles high density below25kg',all(b['gross_high_density_kg']<=25 for b in plan['bundles']))
ck('optional boards absent minimum',not any(k.startswith('ACC') for k in new))
views=read(P+'review-index.json');ck('22 actual CAD review views',len(views)==22 and len({q['image'] for q in views})==22 and all(q.get('native_cad') for q in views))
for q in views:ck('review image '+q['image'],(O/q['image']).read_bytes()[:8]==b'\x89PNG\r\n\x1a\n')
for p,h in read(P+'review-source-hashes.json').items():ck('review input '+p,sha(p)==h)
protected=[B.rstrip('/'),'config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','config/button_relief_v3361.json','config/front_landings_v3363.json','config/underfront_user_module_v337.json','config/plywood_conversion_v337.json','config/manufacturing/flatpack_v337.json','config/hardware_catalog_v337.json','config/solid_leg_blocks_v334.json','reference']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--',*protected],cwd=R,text=True).splitlines()
for p in paths:ck('protected baseline '+p,hashlib.sha256(subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R)).hexdigest()==sha(p))
ck('manufacturing held',not C['manufacturing_release'] and not reg['manufacturing_release'] and not audit['manufacturing_release'])
evidence=['geometry-validation.json','landing-study.json','adjustment-validation.json','retention-decision.json','SW02-load-screen.json','manufacturing-audit.json','manufacturing-register.json','stock-policy-negative-control.json','state-register.json','safety-validation.json','safety-load-screen.json','modularity-validation.json','modularity-dryfit-audit.json','browser-validation.json','viewer-native.json.gz','assembly-manual.json','metrics-authority.json','review-index.json','review-source-hashes.json','independent-qa.json']+[q['image'] for q in views]
report={'pass':True,'scope':'SW02 design simplification and service/modularity documentation; no primary raised support, strap, universal backbox harness or CNC release','checks':checks,'native_sha256':native,'viewer_sha256':browser['viewer_sha256'],'browser_checks':len(browser['checks']),'physical_qualification_complete':False,'primary_raised_service_released':False,'manufacturing_ready':False,'evidence_sha256':{P+n:sha(P+n) for n in evidence}}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V338_REGRESSION_PASS',len(checks),'browser',len(browser['checks']),'MANUFACTURING_AND_PRIMARY_RAISED_SUPPORT_HELD')

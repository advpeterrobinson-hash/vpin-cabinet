"""V33.6.3 CURRENT scope/provenance regression. CERN-OHL-S-2.0.
Architecture PASS is separate from physical qualification and CNC release.
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,collections,re
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363';P=str(O.relative_to(R))+'/';checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/front_landings_v3363.json');geo=read(P+'geometry-validation.json');gate=read(P+'support-validation.json');reg=read(P+'manufacturing-register.json');audit=read(P+'manufacturing-audit.json');motion=read(P+'motion-validation.json');access=read(P+'tool-access.json');loads=read(P+'load-screen.json');browser=read(P+'browser-validation.json');VM=read(P+'viewer-motion.json')
ck('complete architecture gate passed',gate['architecture_pass'])
ck('complete architecture gate current native',gate['native_sha256']==sha(P+'play.FCStd'))
internal=read(P+'internal-hardware-validation.json')
ck('distinct hardware and manual interfaces valid',internal['pass'] and internal['source_sha256']==sha(P+'play.FCStd'))
for p,h in gate['evidence_sha256'].items():ck('complete gate evidence '+p,sha(P+p)==h)
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()))
ck('native mesh input current',N['source_sha256']==sha(P+'play.FCStd'))
for state,r in N['files'].items():ck('native state mesh input '+state,sha(r['path'])==r['sha256'])
for label,v in [('geometry',geo),('manufacturing topology',audit),('motion',motion),('tool access',access),('loads screen',loads),('browser',browser)]:ck(label+' passes',v['pass'])
ck('prior source immutable',sha(C['source'])==geo['source_sha256'])
ck('all prior native shapes unchanged',not geo['current_shapes_changed'])
ck('six18mm bodies only',len(geo['new_wood_names'])==6 and all(n.startswith('FrontLanding') and '_Layer' in n for n in geo['new_wood_names']))
ck('newhardware scoped',all(n.startswith('FrontLanding') for n in geo['new_hardware_names']))
for label,v,key in [('manufacturing',audit,'native_geometry_sha256'),('tool access',access,'source_sha256')]:ck(label+' current native',v[key]==sha(P+'play.FCStd'))
ck('manufacturing config current',audit['native_configuration_sha256']==sha('config/front_landings_v3363.json'))
ck('manufacturing geometryvalidation current',audit['geometry_validation_sha256']==sha(P+'geometry-validation.json'))
ck('load source current',loads['source_sha256']==sha(loads['source']))
if isinstance(motion['source_sha256'],dict):
 for p,h in motion['source_sha256'].items():ck('motion source '+p,sha(p)==h)
else:ck('motion source current',motion['source_sha256']==sha(P+'play.FCStd'))
for s in read(P+'metrics-authority.json')['sources']:ck('metrics source '+s['path'],sha(s['path'])==s['sha256'])
ck('browser current HTML',browser['viewer_sha256']==sha('exports/generated/viewer-v32/index.html'))
ck('broader browser inheritance honest',browser['scope'].startswith('Focused') and browser['inherited']['sha256']==sha(browser['inherited']['path']))
oldreg=read('exports/generated/playfield-rest-v3362/manufacturing-register.json');old={p['instance_id']:p for p in oldreg['parts']};new={p['instance_id']:p for p in reg['parts']}
ck('107 pieces103 CNC4solid65families',len(new)==107 and reg['CNC_plywood_pieces']==103 and len(reg['families'])==65)
ck('prior101pieces retained',set(old)<=set(new))
for k,p in old.items():
 if p['source_component']!='PF_BasePlywood':ck('unchanged manufacturing row '+k,p==new[k])
 else:
  for field in ['brep_path','local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','volume_mm3','outer_profile_operation','fit_dependent','nominal_stock_thickness_mm']:
   if field in p:ck('M025 geometry unchanged '+field,p[field]==new[k][field])
  ck('M025 receiver manual hold',any('receiver' in json.dumps(op).lower() for op in new[k]['manual_finish']))
ck('one face operations only',all(not p.get('opposite_face_cnc') and not p.get('blockers') for p in new.values()))
cat=read('config/hardware_catalog_v3363.json');oldcat=read('config/hardware_catalog_v335.json');hc={h['id']:h for h in cat['hardware']}
for h in oldcat['hardware']:ck('old hardware family unchanged '+h['id'],hc[h['id']]==h)
ck('162families andnewscoped11',len(hc)==162 and len(hc)-len(oldcat['hardware'])==11)
for h,q in [('F59',8),('F60',4),('F61',2),('H27',2),('I15',2),('I16',2),('I17',2),('I18',4),('W11',2),('W12',2),('B17',2)]:ck('scoped quantity '+h,hc[h]['quantity']==q)
ck('material coupon hardware HOLD',C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and not C['manufacturing_release'])
ck('fixed nominal slope noheightredesign',VM['closing']['validated'] and 'tolerance' in motion['adjustment_rule'].lower())
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));oldD=json.loads(gzip.decompress((R/'exports/generated/playfield-rest-v3362/viewer-data.json.gz').read_bytes()));G=D['geometry'];oi={a['key']:a for a in oldD['installed']};od={a['key']:a for a in oldD['detail']};installed={a['key']:a for a in D['installed']};detail={a['key']:a for a in D['detail']}
for n,p in oi.items():ck('unchanged installed mesh '+n,G[installed[n]['geometry']]==oldD['geometry'][p['geometry']])
for n,p in od.items():ck('unchanged detailed mesh '+n,G[detail[n]['geometry']]==oldD['geometry'][p['geometry']])
for state,e in oldD['states'].items():
 for n,g in e.items():ck('unchanged named native pose '+state+'/'+n,D['states'][state][n]==g)
ck('dedicated landing group',any(g['id']=='landings' for g in D['groups']))
newnames=set(geo['new_wood_names'])|set(geo['new_hardware_names']);ck('exactnewinstalledobjectset',set(installed)-set(oi)==newnames)
for n in newnames:ck('current newmetadata '+n,installed[n]['meta']['geometry_authority']['sha256']==sha(P+'play.FCStd') and installed[n]['meta']['group']=='landings')
ck('all six manufacturing models present',sum(a['meta'].get('group')=='landings' and a['meta']['kind']=='wood' for a in D['detail'])==6)
ck('nominalposeonly warningENPT',all('±3' in s and '−3' in s for s in D['engineering_hold'].values()))
ck('no active missing-support claim',all('CLOSED_POSITION_SUPPORT_BLOCKED' not in s for s in D['engineering_hold'].values()))
html=(R/'exports/generated/viewer-v32/index.html').read_text();Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',html,re.S).group(1));ck('all107packing IDs',set(Q['pieces'])==set(new));ck('PFmotion names exact',Q['motions']['pf_names']==VM['playfield_moving_names'])
ck('fixed landing bodies do not rotate',not(set(VM['fixed_landing_names'])&set(VM['playfield_moving_names'])))
ck('moving blind receivers correct',set(n for n in VM['playfield_moving_names'] if n.startswith('FrontLanding'))==set(geo['moving_receiver_names']))
for id in ['service-pf-release','service-pf-close','assembly-05.2','assembly-06.2','assembly-06.3']:ck('new/revisedanimation '+id,any(c['id']==id for c in Q['clips']))
manual=read(P+'assembly-manual.json');steps={t['id']:t for s in manual['stages'] for t in s['steps']}
ck('manual architecture pass physicalhold',manual['closed_position_support_valid'] and not manual['engineering_blockers'])
for lang in ['en','pt-BR']:
 ck('manual nominalgeometryhold '+lang,'−3' in steps['06.3']['action'][lang] and '±3' in steps['06.3']['action'][lang])
 ck('manual Tsareclear '+lang,all(t in steps['06.2']['action'][lang] for t in ['T1','T2','T3']))
 ck('manual physicalqualification '+lang,'PHYSICAL' in steps['06.3']['hold'][lang] if lang=='en' else 'FÍSICA' in steps['06.3']['hold'][lang])
for lang,name in [('en','docs/ASSEMBLY_MANUAL.md'),('pt','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 text=(R/name).read_text();marker='REFERENCE ONLY / PURCHASE BEFORE CNC' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC';ck('eightheldbuttonops '+lang,text.count(marker)>=8)
packing=read(P+'packaging.json');selected=next(c for c in packing['candidates'] if c['target_kg']==25);flat=[p['instance_id'] for b in selected['bundles'] for l in b['layers'] for p in l['pieces']]
ck('packing107once andhighdensity25kg',collections.Counter(flat)==collections.Counter(new.keys()) and all(b['gross_high_density_kg']<=25 for b in selected['bundles']))
protected=['exports/generated/playfield-rest-v3362','config/playfield_rest_v3362.json','config/manufacturing/flatpack_v3362.json','config/viewer_v3362.json','config/hardware_catalog_v335.json','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','config/button_relief_v3361.json']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--',*protected],cwd=R,text=True).splitlines();prior_tools=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','tools'],cwd=R,text=True).splitlines();paths += [p for p in prior_tools if 'v3362' in Path(p).name]
for p in paths:ck('protected '+p,hashlib.sha256(subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R)).hexdigest()==sha(p))
report={'pass':True,'scope':'Closed support architecture at unchanged nominal PLAY pose; physical hardware/material/load qualification and manufacturing remain HOLD.','checks':checks,'native_geometry_checks':len(geo['checks']),'motion_checks':len(motion['checks']),'browser_checks':len(browser['checks']),'native_sha256':sha(P+'play.FCStd'),'viewer_sha256':browser['viewer_sha256'],'closed_position_support_status':'ARCHITECTURE_PASS_PHYSICAL_QUALIFICATION_HOLD','closed_position_support_valid':True,'physical_qualification_complete':False,'manufacturing_ready':False,'support_validation_sha256':sha(P+'support-validation.json'),'evidence_sha256':{n:sha(P+n) for n in ['internal-hardware-validation.json','geometry-validation.json','motion-validation.json','manufacturing-audit.json','tool-access.json','load-screen.json','browser-validation.json','state-register.json','viewer-motion.json','assembly-manual.json','metrics-authority.json','viewer-native.json.gz','manufacturing-register.json','landing-manual-interface-overlay.json']}}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V3363_REGRESSION_PASS',len(checks),'browser',len(browser['checks']),'CNC BLOCKED')

"""V33.6.2 scope regression. Passing this audit does NOT close missing PLAY rests.
CERN-OHL-S-2.0. CURRENT closed support and manufacturing remain blocked.
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,math,collections,re
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/playfield-rest-v3362';checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/playfield_rest_v3362.json');prefix=str(O.relative_to(R))+'/';v=read(prefix+'geometry-validation.json');reg=read(prefix+'manufacturing-register.json');audit=read(prefix+'manufacturing-audit.json');motion=read(prefix+'motion-validation.json');cable=read(prefix+'cable-study.json');browser=read(prefix+'browser-validation.json');states=read(prefix+'state-register.json');button=read(prefix+'button-metrology.json');support=read(prefix+'closed-support-audit.json')
for name,r in [('geometry',v),('manufacturing topology',audit),('motion clearance only',motion),('cable',cable),('browser focused',browser),('button metrology',button)]:ck(name+' passes',r['pass'])
ck('support audit honestly BLOCKED',support['audit_completed'] and not support['closed_position_support_valid'] and support['status']==C['closed_position_support_status']=='CLOSED_POSITION_SUPPORT_BLOCKED')
ck('support audit source current',support['sha256']==sha(prefix+'play.FCStd'))
ck('input baseline unchanged',sha(C['source'])==v['source_sha256'])
for name,r,key in [('manufacturing',audit,'native_geometry_sha256'),('states',states,'source_sha256'),('cable',cable,'source_sha256')]:ck(name+' native input current',sha(prefix+'play.FCStd')==r[key])
ck('button metrology input current',sha(button['source'])==button['source_sha256'])
for p,h in motion['source_sha256'].items():ck('motion input current '+p,sha(p)==h)
for src in read(prefix+'metrics-authority.json')['sources']:ck('metrics input current '+src['path'],sha(src['path'])==src['sha256'])
ck('browser current HTML',sha('exports/generated/viewer-v32/index.html')==browser['viewer_sha256'])
ck('browser broad-suite inheritance honest',sha(browser['inherited']['path'])==browser['inherited']['sha256'] and 'Focused' in browser['scope'])
ck('only PF base changed',{r['name'] for r in v['changed']}=={'PF_BasePlywood'} and not v['added'] and not v['removed'])
ck('101 pieces97 CNC4 solids59 families',len(reg['parts'])==101 and reg['CNC_plywood_pieces']==97 and len(reg['families'])==59)
old=read('exports/generated/button-relief-v3361/manufacturing-register.json');byold={p['instance_id']:p for p in old['parts']}
for p in reg['parts']:
 if p['source_component']!='PF_BasePlywood':ck('unchanged manufacturing '+p['instance_id'],p==byold[p['instance_id']])
ck('no added rest pieces or hardware families',set(p['instance_id'] for p in reg['parts'])==set(byold) and read(prefix+'hardware-dashboard.json')==read('exports/generated/button-relief-v3361/hardware-dashboard.json'))
ck('one face CNC only',all(not p.get('opposite_face_cnc') and not p.get('blockers') for p in reg['parts']))
ck('material coupon hardware remain HOLD',C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and not C['manufacturing_release'] and C['side_buttons']['final_bore_mm'] is None and C['side_buttons']['final_recess_mm'] is None)
prior=read('config/button_relief_v3361.json');ck('all ergonomic button parameters unchanged',C['side_buttons']==prior['side_buttons'])
for key in ['service_window_xywh_mm','service_window_radius_mm','strain_slots_xywh_mm','strain_slot_radius_mm']:ck('rear service openings retained '+key,C['playfield'][key]==prior['playfield'][key])
relief=v['relief'];ck('requested52inset87lengthR8 and396width',abs(relief['depth_mm']-52)<1e-6 and abs(relief['length_mm']-87)<1e-6 and relief['transition_radius_mm']==8 and abs(relief['minimum_transverse_width_mm']-396)<1e-6 and abs(relief['minimum_section_area_mm2']-7128)<1e-5)
ck('extra inset is owner preference beyond required service clearance',relief['owner_additional_inset_each_side_mm']==30 and relief['depth_is_owner_preference_beyond_service_minimum'])
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));oldD=json.loads(gzip.decompress((R/'exports/generated/button-relief-v3361/viewer-data.json.gz').read_bytes()));G=D['geometry'];installed={p['key']:p for p in D['installed']};detail={p['key']:p for p in D['detail']};oldi={p['key']:p for p in oldD['installed']};oldd={p['key']:p for p in oldD['detail']}
alpha=math.radians(9.906669253650632);bz=341.7292430523254
def local(w):
 x,y,z=w;y-=45;z-=bz;return [x,y*math.cos(alpha)+z*math.sin(alpha),-y*math.sin(alpha)+z*math.cos(alpha)]
def clean_front(g):
 vs=[local(w) for w in g['vertices']];front=[w for w in vs if abs(w[1]-20)<.002]
 if not front or abs(min(w[0] for w in front)-102)>.002 or abs(max(w[0] for w in front)-498)>.002:return False
 for right in [False,True]:
  groups={}
  for x,y,z in vs:
   x=600-x if right else x
   if x>130 or y>relief['local_y_end_mm']+.002:continue
   groups.setdefault(round(y,3),[]).append(x)
  ys=sorted(groups);xs=[max(groups[y]) for y in ys]
  if any(b>a+.002 for a,b in zip(xs,xs[1:])):return False
 return True
ck('installed52inset no horn',clean_front(G[installed['PF_BasePlywood']['geometry']]))
ck('manufacturing52inset no horn',clean_front(G[detail['P034-Main']['geometry']]))
ck('negative rejects prior22inset',not clean_front(oldD['geometry'][oldi['PF_BasePlywood']['geometry']]))
for n,p in installed.items():
 if n!='PF_BasePlywood':ck('unchanged installed mesh '+n,G[p['geometry']]==oldD['geometry'][oldi[n]['geometry']])
for n,p in detail.items():
 if n!='P034-Main':ck('unchanged detailed mesh '+n,G[p['geometry']]==oldD['geometry'][oldd[n]['geometry']])
for state,entries in D['states'].items():
 ck('PF current named state '+state,entries['PF_BasePlywood'].startswith('v3362-'))
 for n,g in entries.items():
  if n!='PF_BasePlywood':ck('unchanged named pose '+state+'/'+n,g==oldD['states'][state].get(n))
for p in D['installed']+D['detail']:ck('geometry authority '+p['key'],bool(p['meta'].get('geometry_authority',{}).get('file')))
ck('viewer explicit support HOLD',all('CLOSED_POSITION_SUPPORT_BLOCKED' in t for t in D['engineering_hold'].values()))
html=(R/'exports/generated/viewer-v32/index.html').read_text();Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',html,re.S).group(1))
ck('no corrupted version strings','V33.6.2.1' not in html and 'V33.6.1.2' not in html)
ck('packing uses current base',not Q['pieces']['P034-Main'].get('packing_mesh') and set(Q['pieces'])==set(byold))
ck('all animations disclose support HOLD',all(all('CLOSED_POSITION_SUPPORT_BLOCKED' in c['note'][lang] for lang in ['en','pt-BR']) for c in Q['clips']))
packing=read(prefix+'packaging.json');selected=next(p for p in packing['candidates'] if p['target_kg']==25);flat=[p['instance_id'] for b in selected['bundles'] for l in b['layers'] for p in l['pieces']]
ck('packing101once andhighdensity25kg',collections.Counter(flat)==collections.Counter(byold.keys()) and all(b['gross_high_density_kg']<=25 for b in selected['bundles']))
ck('native named states exist',all((O/f).is_file() for f in states['native_files'].values()))
manual=read(prefix+'assembly-manual.json');steps={t['id']:t for s in manual['stages'] for t in s['steps']}
for sid in ['00.1','05.1','06.1','06.2','17.1','17.2']:ck('manual support HOLD '+sid,all('CLOSED_POSITION_SUPPORT_BLOCKED' in txt for txt in steps[sid]['hold'].values()))
for lang,name in [('en','docs/ASSEMBLY_MANUAL.md'),('pt','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 text=(R/name).read_text();marker='REFERENCE ONLY / PURCHASE BEFORE CNC' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC'
 ck('manual button holds retained '+lang,text.count(marker)>=8)
 ck('manual explicit support blocker '+lang,text.count('CLOSED_POSITION_SUPPORT_BLOCKED')>=6)
# Previous version remains an exact audit record; new evidence is linked forward.
protected=['exports/generated/button-relief-v3361','config/button_relief_v3361.json','config/manufacturing/flatpack_v3361.json','config/viewer_v3361.json','config/hardware_catalog_v335.json','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--',*protected],cwd=R,text=True).splitlines();prior_tools=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','tools'],cwd=R,text=True).splitlines();paths += [p for p in prior_tools if 'v3361' in Path(p).name]
for p in paths:
 before=subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R);ck('protected '+p,hashlib.sha256(before).hexdigest()==sha(p))
report={'pass':True,'scope':'Requested52mm front clearance and honest support blocker; not complete mechanical support validation.','checks':checks,'native_geometry_checks':len(v['checks']),'motion_checks':len(motion['checks']),'browser_checks':len(browser['checks']),'viewer_sha256':browser['viewer_sha256'],'native_sha256':sha(prefix+'play.FCStd'),'closed_position_support_status':'CLOSED_POSITION_SUPPORT_BLOCKED','closed_position_support_valid':False,'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V3362_REGRESSION_PASS',len(checks),'browser',len(browser['checks']),'CLOSED_POSITION_SUPPORT_BLOCKED')

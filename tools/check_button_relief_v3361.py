"""Protect restored owner ergonomics and clean open-front relief in every consumer.
CERN-OHL-S-2.0. Current machining remains provisional; no release authority.
"""
from pathlib import Path
import json,gzip,hashlib,subprocess,math,collections,re,copy
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/button-relief-v3361';checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/button_relief_v3361.json');prefix='exports/generated/button-relief-v3361/';v=read(prefix+'geometry-validation.json');reg=read(prefix+'manufacturing-register.json');audit=read(prefix+'manufacturing-audit.json');motion=read(prefix+'motion-validation.json');cable=read(prefix+'cable-study.json');browser=read(prefix+'browser-validation.json');states=read(prefix+'state-register.json');button=read(prefix+'button-metrology.json')
for name,r in [('geometry',v),('manufacturing',audit),('motion',motion),('cable',cable),('browser',browser),('button metrology',button)]:ck(name+' passes',r['pass'])
ck('inherited backbox service study remains valid',read('exports/generated/monitor-support-v336/backbox-study/result.json')['pass'])
ck('button metrology source current',sha(button['source'])==button['source_sha256'])
ck('input baseline unchanged',sha(C['source'])==v['source_sha256'])
for name,r,key in [('manufacturing',audit,'native_geometry_sha256'),('states',states,'source_sha256'),('cable',cable,'source_sha256')]:ck(name+' native input current',sha(prefix+'play.FCStd')==r[key])
for p,h in motion['source_sha256'].items():ck('motion input current '+p,sha(p)==h)
for src in read(prefix+'metrics-authority.json')['sources']:ck('metrics input current '+src['path'],sha(src['path'])==src['sha256'])
ck('browser current HTML',sha('exports/generated/viewer-v32/index.html')==browser['viewer_sha256'])
changed={r['name'] for r in v['changed']};wood={p['source_component'] for p in reg['parts']};allowed={'SIDE_L','SIDE_R','PF_BasePlywood'}
ck('only authorized three wood objects change',changed&wood==allowed)
ck('other changes only32 repositioned leaf/button reserves',len(changed)==35 and all(n in allowed or n.startswith(('Leaf','Button')) for n in changed))
ck('no added or removed component families',not v['added'] and not v['removed'])
ck('101 pieces97 CNC4 solids59 families',len(reg['parts'])==101 and reg['CNC_plywood_pieces']==97 and len(reg['families'])==59)
old=read('exports/generated/monitor-support-v336/manufacturing-register.json');byold={p['instance_id']:p for p in old['parts']}
for p in reg['parts']:
 if p['source_component'] not in allowed:ck('unchanged manufacturing '+p['instance_id'],p==byold[p['instance_id']])
ck('no4mm or resurrectedleg/stop layers',not any(p['nominal_stock_thickness_mm']==4 or p['manufacturing_part_id'] in ['M019','M020','M021','M022','M023','M046','M047','M048','M049'] for p in reg['parts']))
ck('one face CNC only',all(not p.get('opposite_face_cnc') and not p.get('blockers') for p in reg['parts']))
ck('unknown actual material and coupon stay null',C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and not C['manufacturing_release'])
expected=[('primary',89,350.593661971831),('secondary',127,357.2302816901408)]
def valid_centers(cs):
 if len(cs)!=2:return False
 return all(q['kind']==kind and q['y_mm']<=(110 if kind=='primary' else 150) and abs(q['y_mm']-y)<1e-7 and abs(q['z_mm']-z)<1e-7 for q,(kind,y,z) in zip(cs,expected))
ck('owner ergonomic centers exactly restored',valid_centers(C['side_buttons']['centers']))
ck('vertical datum localtopminus65 never Z270',C['side_buttons']['vertical_datum']=='local_side_top_minus_65_mm' and C['side_buttons']['local_top_offset_mm']==65 and C['side_buttons']['candidate_z_mm'] is None)
ck('ergonomic maximums remain110/150',C['side_buttons']['maximum_primary_y_mm']==110 and C['side_buttons']['maximum_secondary_y_mm']==150)
for label,changed_rows in [('wrong V336 rearward centers',[{'kind':'primary','y_mm':255,'z_mm':270},{'kind':'secondary','y_mm':310,'z_mm':270}]),('wrong Z270',[{'kind':k,'y_mm':y,'z_mm':270} for k,y,z in expected]),('primary beyond110',[{'kind':'primary','y_mm':110.01,'z_mm':expected[0][2]},{'kind':'secondary','y_mm':127,'z_mm':expected[1][2]}]),('secondary beyond150',[{'kind':'primary','y_mm':89,'z_mm':expected[0][2]},{'kind':'secondary','y_mm':150.01,'z_mm':expected[1][2]}])]:ck('negative control rejects '+label,not valid_centers(changed_rows))
ck('final button machining independent HOLD',C['side_buttons']['final_bore_mm'] is None and C['side_buttons']['final_recess_mm'] is None and C['side_buttons']['reference_geometry_status']=='REFERENCE_ONLY_NOT_RELEASED')
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));G=D['geometry'];installed={p['key']:p for p in D['installed']};detail={p['key']:p for p in D['detail']};alpha=math.radians(9.906669253650632);bz=341.7292430523254
relief=v['relief'];depth=relief['depth_mm'];end=relief['local_y_end_mm'];radius=relief['transition_radius_mm']
def local(w):
 x,y,z=w;y-=45;z-=bz;return [x,y*math.cos(alpha)+z*math.sin(alpha),-y*math.sin(alpha)+z*math.cos(alpha)]
def clean_open_front(g):
 vs=[local(w) for w in g['vertices']];front=[w for w in vs if abs(w[1]-20)<.002]
 if not front:return False
 if abs(min(w[0] for w in front)-(50+depth))>.002 or abs(max(w[0] for w in front)-(550-depth))>.002:return False
 # A front horn would widen towards the player, then narrow: forbid that
 # reversal. Group tessellated exterior-edge vertices at each longitudinal level.
 for right in [False,True]:
  groups={}
  for x,y,z in vs:
   x=600-x if right else x
   if x>100 or y>end+.002:continue
   groups.setdefault(round(y,3),[]).append(x)
  ys=sorted(groups);maxx=[max(groups[y]) for y in ys]
  if any(b>a+.002 for a,b in zip(maxx,maxx[1:])):return False
 return True
ck('PLAYFIELD_BASE_HORN_ABSENT openfront installed',clean_open_front(G[installed['PF_BasePlywood']['geometry']]))
ck('PLAYFIELD_BASE_HORN_ABSENT actual manufacturing detail',clean_open_front(G[detail['P034-Main']['geometry']]))
oldD=json.loads(gzip.decompress((R/'exports/generated/structural-v335/viewer-data.json.gz').read_bytes()));oa=next(p for p in oldD['installed'] if p['key']=='PF_BasePlywood');ck('negative control rejects historical horned M025',not clean_open_front(oldD['geometry'][oa['geometry']]))
rectD=json.loads(gzip.decompress((R/'exports/generated/monitor-support-v336/viewer-data.json.gz').read_bytes()));ra=next(p for p in rectD['installed'] if p['key']=='PF_BasePlywood');ck('negative control rejects unrelieved V336 rectangle at front buttons',not clean_open_front(rectD['geometry'][ra['geometry']]))
ck('naturalR2 compatible no gratuitousdogbones',radius>=2 and not C['playfield']['front_relief']['dogbones'])
for key in ['service_window_xywh_mm','service_window_radius_mm','strain_slots_xywh_mm','strain_slot_radius_mm']:ck('V336 playfield opening preserved '+key,C['playfield'][key]==read('config/monitor_support_v336.json')['playfield'][key])
for kind,y,z in expected:
 for side in ['L','R']:
  vs=G[installed[f'LeafButton_{kind}_{side}']['geometry']]['vertices'];ck('current button vertices '+kind+side,abs((min(w[1] for w in vs)+max(w[1] for w in vs))/2-y)<1e-5 and abs((min(w[2] for w in vs)+max(w[2] for w in vs))/2-z)<1e-5)
for p in D['installed']+D['detail']:ck('geometry authority '+p['key'],bool(p['meta'].get('geometry_authority',{}).get('file')))
for n in changed:
 ck('changed installed native mesh '+n,installed[n]['geometry'].startswith('v3361-'))
 for state,entries in D['states'].items():ck('changed pose '+state+'/'+n,entries.get(n,'').startswith('v3361-'))
html=(R/'exports/generated/viewer-v32/index.html').read_text();Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',html,re.S).group(1))
ck('version text not duplicated','V33.6.1.1' not in html)
ck('historical V336 mistake remains correctly named in manual', 'V33.6 rearward Y255/Y310 Z270 was an erroneous' in html)
ck('packing M025 uses current detailed geometry',not Q['pieces']['P034-Main'].get('packing_mesh'))
ck('all current detailed woodIDs represented in packing',set(Q['pieces'])=={p['instance_id'] for p in reg['parts']})
# Preserve historical source/certificates; do not rewrite their old data to fake
# the new owner decision. Active routing goes to this new validator after promotion.
protected_prefixes=['exports/generated/solid-leg-v334','exports/generated/structural-v335','exports/generated/monitor-support-v336','config/solid_leg_blocks_v334.json','config/monitor_support_v336.json','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','config/hardware_catalog_v335.json']
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--',*protected_prefixes],cwd=R,text=True).splitlines()
prior_tools=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','tools'],cwd=R,text=True).splitlines()
paths+= [p for p in prior_tools if 'v336' in Path(p).name]
for p in paths:
 before=subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R)
 if p=='exports/generated/monitor-support-v336/README.md':
  banner='> V33.6.1 CORRECTION: the rearward Y255/Y310,Z270 restoration and rectangular-front-base conclusion in this historical V33.6 snapshot are superseded. Owner authority is Y89/Y127, local side top minus65mm, with a clean front-open relief. V33.6 rear monitor openings/backbox work remain retained. See [CURRENT report](../button-relief-v3361/README.md).\n\n'
  ck('historical report receives only exact correction banner',(R/p).read_bytes()==banner.encode()+before)
 else:ck('protected '+p,hashlib.sha256(before).hexdigest()==sha(p))
packing=read(prefix+'packaging.json');selected=next(p for p in packing['candidates'] if p['target_kg']==25);flat=[p['instance_id'] for b in selected['bundles'] for l in b['layers'] for p in l['pieces']]
ck('packing all101 once',collections.Counter(flat)==collections.Counter(p['instance_id'] for p in reg['parts']))
ck('packing high density <=25kg',all(b['gross_high_density_kg']<=25 for b in selected['bundles']))
ck('hardware dashboard unchanged',read(prefix+'hardware-dashboard.json')==read('exports/generated/monitor-support-v336/hardware-dashboard.json'))
ck('backbox VESAwindow and all4carrierslots unchanged',all(n not in changed for n in ['BB_ReplaceableVESAPlate','BB_MonitorCarrier0','BB_MonitorCarrier1','BB_MonitorStopRail']))
ck('minimum sample cable bend radius35',min(r['minimum_bend_radius_mm'] for r in cable['rows'])>=35)
ck('native named states exist',all((O/f).is_file() for f in states['native_files'].values()))
manual=read(prefix+'assembly-manual.json');steps={t['id']:t for s in manual['stages'] for t in s['steps']}
ck('active manual restores front ergonomic authority','CURRENT OWNER BUTTON AUTHORITY: primary Y89, secondary Y127' in steps['18.1']['action']['en'])
ck('wrong current V336 manual instruction removed','SIDE BUTTON POSITIONAL AUTHORITY: Y255 / Y310, Z270' not in steps['18.1']['action']['en'])
for lang,name in [('en','docs/ASSEMBLY_MANUAL.md'),('pt','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 text=(R/name).read_text();marker='REFERENCE ONLY / PURCHASE BEFORE CNC' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC'
 ck('manual per-feature button HOLD '+lang,text.count(marker)>=8)
 for panel in ['SIDE_L','SIDE_R']:
  iid=next(p['instance_id'] for p in reg['parts'] if p['source_component']==panel)
  block=text.split('### '+iid+' / ',1)[1].split('### ',1)[0]
  ck('all4buttonreferenceoperations held in manual '+lang+panel,block.count(marker)>=4)
report={'pass':True,'checks':checks,'native_geometry_checks':len(v['checks']),'motion_checks':len(motion['checks']),'cable_sample_states':len(cable['rows']),'browser_checks':len(browser['checks']),'viewer_sha256':browser['viewer_sha256'],'native_sha256':sha(prefix+'play.FCStd'),'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V3361_REGRESSION_PASS',len(checks),'browser',len(browser['checks']))

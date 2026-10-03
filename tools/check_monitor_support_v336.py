"""V33.6 positional/contour/current-artifact regression. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,hashlib,subprocess,math,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/monitor-support-v336';checks=[]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def ck(n,v,d=None):checks.append({'name':n,'pass':bool(v),'detail':d});assert v,(n,d)
C=read('config/monitor_support_v336.json');v=read('exports/generated/monitor-support-v336/geometry-validation.json');reg=read('exports/generated/monitor-support-v336/manufacturing-register.json');audit=read('exports/generated/monitor-support-v336/manufacturing-audit.json');motion=read('exports/generated/monitor-support-v336/motion-validation.json');cable=read('exports/generated/monitor-support-v336/cable-study.json');bb=read('exports/generated/monitor-support-v336/backbox-study/result.json');browser=read('exports/generated/monitor-support-v336/browser-validation.json');states=read('exports/generated/monitor-support-v336/state-register.json')
for name,r in [('geometry',v),('manufacturing',audit),('motion',motion),('cable',cable),('backbox',bb),('browser',browser)]:ck(name+' passes',r['pass'])
button=read('exports/generated/monitor-support-v336/button-metrology.json')
ck('button service metrology passes',button['pass'])
ck('button metrology source current',sha(button['source'])==button['source_sha256'])
ck('input baseline unchanged',sha(C['source'])==v['source_sha256'])
ck('manufacturing native input current',sha('exports/generated/monitor-support-v336/play.FCStd')==audit['native_geometry_sha256'])
ck('named-state native input current',sha('exports/generated/monitor-support-v336/play.FCStd')==states['source_sha256'])
ck('cable native input current',sha('exports/generated/monitor-support-v336/play.FCStd')==cable['source_sha256'])
for p,h in motion['source_sha256'].items():ck('motion input current '+p,sha(p)==h)
for src in read('exports/generated/monitor-support-v336/metrics-authority.json')['sources']:ck('metrics input current '+src['path'],sha(src['path'])==src['sha256'])
ck('browser current HTML',sha('exports/generated/viewer-v32/index.html')==browser['viewer_sha256'])
changed={r['name'] for r in v['changed']};wood={p['source_component'] for p in reg['parts']};allowed={'SIDE_L','SIDE_R','PF_BasePlywood','BB_MonitorCarrier0','BB_MonitorCarrier1'}
ck('only authorized five wood objects change',changed&wood==allowed)
ck('other changes only32 repositioned leaf/button reserves',len(changed)==37 and all(n in allowed or n.startswith(('Leaf','Button')) for n in changed))
ck('101 pieces97 CNC4 solids59 families',len(reg['parts'])==101 and reg['CNC_plywood_pieces']==97 and len(reg['families'])==59)
old=read('exports/generated/structural-v335/manufacturing-register.json');byold={p['instance_id']:p for p in old['parts']}
for p in reg['parts']:
 if p['source_component'] not in allowed:ck('unchanged manufacturing '+p['instance_id'],p==byold[p['instance_id']])
ck('no4mm or resurrectedleg/stop layers',not any(p['nominal_stock_thickness_mm']==4 or p['manufacturing_part_id'] in ['M019','M020','M021','M022','M023','M046','M047','M048','M049'] for p in reg['parts']))
ck('one face CNC only',all(not p.get('opposite_face_cnc') and not p.get('blockers') for p in reg['parts']))
ck('unknown actual material and coupon stay null',C['measured_thickness_mm'] is None and C['selected_coupon_clearance_mm'] is None and not C['manufacturing_release'])
ck('SIDE_BUTTON_CENTER_1_Y =255',C['side_buttons']['candidate_y_mm'][0]==255)
ck('SIDE_BUTTON_CENTER_2_Y =310',C['side_buttons']['candidate_y_mm'][1]==310)
ck('SIDE_BUTTON_Z =270',C['side_buttons']['candidate_z_mm']==270)
ck('final button machining independent HOLD',C['side_buttons']['final_bore_mm'] is None and C['side_buttons']['final_recess_mm'] is None)
D=json.loads(gzip.decompress((O/'viewer-data.json.gz').read_bytes()));G=D['geometry'];installed={p['key']:p for p in D['installed']};detail={p['key']:p for p in D['detail']};alpha=math.radians(9.906669253650632);bz=341.7292430523254
def local(v):
 x,y,z=v;y-=45;z-=bz;return [x,y*math.cos(alpha)+z*math.sin(alpha),-y*math.sin(alpha)+z*math.cos(alpha)]
def horn_test(g):
 vs=[local(v) for v in g['vertices']];front=[v for v in vs if v[1]<670]
 return all(abs(v[0]-50)<.001 or abs(v[0]-550)<.001 for v in front)
ck('PLAYFIELD_BASE_HORN_ABSENT installed',horn_test(G[installed['PF_BasePlywood']['geometry']]))
ck('PLAYFIELD_BASE_HORN_ABSENT actual manufacturing detail',horn_test(G[detail['P034-Main']['geometry']]))
oldD=json.loads(gzip.decompress((R/'exports/generated/structural-v335/viewer-data.json.gz').read_bytes()));oa=next(p for p in oldD['installed'] if p['key']=='PF_BasePlywood');ck('negative control rejects old horned base',not horn_test(oldD['geometry'][oa['geometry']]))
for kind,y in [('primary',255),('secondary',310)]:
 for side in ['L','R']:
  vs=G[installed[f'LeafButton_{kind}_{side}']['geometry']]['vertices'];ck('current button vertices '+kind+side,abs((min(p[1] for p in vs)+max(p[1] for p in vs))/2-y)<1e-5 and abs((min(p[2] for p in vs)+max(p[2] for p in vs))/2-270)<1e-5)
for p in D['installed']+D['detail']:ck('geometry authority '+p['key'],bool(p['meta'].get('geometry_authority',{}).get('file')))
for n in changed:
 ck('changed installed native mesh '+n,installed[n]['geometry'].startswith('v336-'))
 for state,entries in D['states'].items():ck('changed pose '+state+'/'+n,entries.get(n,'').startswith('v336-'))
# Protect all prior exact native geometry, universal jig and WPC/supplier authorities.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',C['head_before'],'--','exports/generated/solid-leg-v334','exports/generated/structural-v335','config/solid_leg_blocks_v334.json','config/manufacturing/profiles/peter_supplier_v1.json','config/wpc_kinematics_v32.json','config/hardware_catalog_v335.json'],cwd=R,text=True).splitlines()
for p in paths:ck('protected '+p,hashlib.sha256(subprocess.check_output(['git','show',C['head_before']+':'+p],cwd=R)).hexdigest()==sha(p))
packing=read('exports/generated/monitor-support-v336/packaging.json');selected=next(p for p in packing['candidates'] if p['target_kg']==25);flat=[p['instance_id'] for b in selected['bundles'] for l in b['layers'] for p in l['pieces']]
ck('packing all101 once',collections.Counter(flat)==collections.Counter(p['instance_id'] for p in reg['parts']))
ck('packing high density <=25kg',all(b['gross_high_density_kg']<=25 for b in selected['bundles']))
ck('hardware dashboard unchanged',read('exports/generated/monitor-support-v336/hardware-dashboard.json')==read('exports/generated/structural-v335/hardware-dashboard.json'))
ck('large backbox adapter window not promoted','BB_ReplaceableVESAPlate' not in changed)
ck('minimum sample cable bend radius35',min(r['minimum_bend_radius_mm'] for r in cable['rows'])>=35)
ck('native named states exist',all((O/f).is_file() for f in states['native_files'].values()))
for lang,name in [('en','docs/ASSEMBLY_MANUAL.md'),('pt','docs/ASSEMBLY_MANUAL.pt-BR.md')]:
 text=(R/name).read_text();ck('manual per-feature button HOLD '+lang,text.count('REFERENCE ONLY / PURCHASE BEFORE CNC' if lang=='en' else 'SOMENTE REFERÊNCIA / COMPRAR ANTES DO CNC')>=8)
report={'pass':True,'checks':checks,'native_geometry_checks':len(v['checks']),'backbox_checks':len(bb['checks']),'motion_checks':len(motion['checks']),'cable_sample_states':len(cable['rows']),'browser_checks':len(browser['checks']),'viewer_sha256':browser['viewer_sha256'],'native_sha256':sha('exports/generated/monitor-support-v336/play.FCStd'),'manufacturing_ready':False}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('V336_REGRESSION_PASS',len(checks),'browser',len(browser['checks']))

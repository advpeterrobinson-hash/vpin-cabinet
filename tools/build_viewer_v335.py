"""V33.5 exact changed-mesh overlay; offline viewer controls preserved. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,re,base64,copy,subprocess,math
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335'
read=lambda p:json.loads((R/p).read_text())
C=read('config/structural_simplification_v335.json');base=subprocess.check_output(['git','show',C['head_before']+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S).group(1))))
Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1))
val=read('exports/generated/structural-v335/geometry-validation.json');assert val['pass']
reg=read('exports/generated/structural-v335/manufacturing-register.json');manual=read('exports/generated/structural-v335/assembly-manual.json');cat=read('config/hardware_catalog_v335.json');H={h['id']:h for h in cat['hardware']}
changed=json.loads(gzip.decompress((O/'changes-mesh.json.gz').read_bytes()));pieces=json.loads(gzip.decompress((O/'manufacturing-mesh.json.gz').read_bytes()));removed=set(val['removed'])
def geometry(key,m):D['geometry'][key]=m;return key
def posed(m,angle):
 out=copy.deepcopy(m);a=math.radians(angle);c,s=math.cos(a),math.sin(a)
 out['vertices']=[[x,1066.8+(y-1066.8)*c-(z-508)*s,508+(y-1066.8)*s+(z-508)*c] for x,y,z in m['vertices']];return out
def world(m,mat):
 out=copy.deepcopy(m);out['vertices']=[[sum(mat[i*4+j]*v[j] for j in range(3))+mat[i*4+3] for i in range(3)] for v in m['vertices']];return out
D['installed']=[d for d in D['installed'] if d['key'] not in removed];D['detail']=[d for d in D['detail'] if d['meta']['source'] not in removed]
for state,items in D['states'].items():
 for n in removed:items.pop(n,None)
for n,m in changed.items():
 gid=geometry('v335-'+n,m)
 for state,items in D['states'].items():items[n]=geometry('v335-'+state+'-'+n,posed(m,90 if state=='BACKBOX FOLD' else 45)) if n.startswith('BB_') and state in ['BACKBOX FOLD','FOLD45'] else gid
 current=next((d for d in D['installed'] if d['key']==n),None)
 if current:current['geometry']=gid
 else:
  donor='BB_MonitorCarrier0' if n=='BB_MonitorStopRail' else 'BB_UprightLockLKnob' if n.startswith('BB_') else 'PLUNGER_RESERVED' if n.startswith('Plunger') else 'FAN_230'
  current=copy.deepcopy(next(d for d in D['installed'] if d['key']==donor));current.update(key=n,geometry=gid);current['meta']['source']=n;D['installed'].append(current)
 if n=='BB_MonitorStopRail':current['meta'].update(id='M067',names={'en':'M067 · Transverse monitor stop rail','pt-BR':'M067 · Travessa de apoio do monitor'},instances=['P094-Main'],families=['M067'],quantity=1,manufacturing_status=['ONE_SIDE_CNC_PLUS_MANUAL_FINISH'])
 elif n.startswith('Plunger'):
  current['meta'].update(id='PLUNGER',names={'en':'Provisional conventional plunger — purchase before CNC','pt-BR':'Plunger convencional provisório — comprar antes do CNC'},group='hardware',kind='hardware',scope='MAIN CABINET',status='PURCHASE_BEFORE_CNC',thickness=None,quantity=1,hardware_id=None,stage='16',manufacturing_status=[],families=[],instances=[])
 elif n.startswith(('RearFanWoodScrew','BB_Stop')):
  id='F56' if n.startswith('RearFan') else 'F57' if 'Retention' in n else 'I10' if 'Insert' in n else 'I11' if 'Locknut' in n else 'F27';h=H[id]
  current['meta'].update(id=id,hardware_id=id,names={'en':h['description_en'],'pt-BR':h['description_pt_BR']},kind='hardware',group='mainfans' if id=='F56' else 'bbhardware',scope='MAIN CABINET' if id=='F56' else 'BACKBOX',classification=h['flatpack_classification'],quantity=h['quantity'],stage=h['assembly_stage'],status='PURCHASE_BEFORE_CNC',manufacturing_status=[],families=[],instances=[])
 # all rail members follow carrier depth/fold; tips belong to adapter adjustment.
 if n.startswith('BB_Stop'):
  Q['motions']['groups'][n]='carrier'
  current['overview']=[0,-105,400]
 if n=='BB_MonitorStopRail':Q['motions']['groups'][n]='carrier'
# Old rear nut/washer entries and retired library-only stop entries are removed.
D['detail']=[d for d in D['detail'] if d['meta'].get('hardware_id') not in ['F10']]
for p in reg['parts']:
 i=p['instance_id'];n=p['source_component']
 if i not in pieces:continue
 a=next(x for x in D['installed'] if x['key']==n)
 a['meta'].update(families=[p['manufacturing_part_id']],instances=[i],manufacturing_status=[p['manufacturing_status']],status='WAITING_FOR_COUPON')
 d=next((x for x in D['detail'] if x['key']==i),None)
 if d is None:
  d=copy.deepcopy(a);d.update(key=i,offset=[0,-180,450],source_matrix=p['local_to_installed_matrix']);D['detail'].append(d)
 d['geometry']=geometry('v335-piece-'+i,world(pieces[i],p['local_to_installed_matrix']));d['meta']=copy.deepcopy(a['meta']);d['meta'].update(id=p['manufacturing_part_id'],instance=i);d['source_mesh']='V33.5 actual manufacturing B-rep';d['source_matrix']=p['local_to_installed_matrix']
for a in D['installed']:
 n=a['key']
 if n in val['added'] and a['meta']['kind']!='wood':
  d=copy.deepcopy(a);d['key']='HW:'+n;d['offset']=[0,-145,0] if n.startswith('RearFan') else [0,-100,490] if n.startswith('BB_StopRailRetention') else [0,-180,485];D['detail'].append(d)
# Correct fan semantics: wood -> fan -> inner grill -> head as one moves inward.
for d in D['detail']:
 n=d['meta']['source'] or ''
 if n in ['FAN_230','FAN_370']:d['offset']=[0,-65,0]
 elif n.startswith('CandidateFanGuard') and n.endswith('Inner'):d['offset']=[0,-105,0]
 if d['meta'].get('hardware_id') in H:
  h=H[d['meta']['hardware_id']];d['meta'].update(quantity=h['quantity'],classification=h['flatpack_classification'])
# Captured panels must already appear before the side shell closes.
for a in D['installed']+D['detail']:
 if a['meta']['source'] in ['FLOOR','BACKBOX_BASE']:a['meta']['stage']='02'
# Provisional internal plunger envelope visible in the hardware group.
for a in D['installed']+D['detail']:
 if a['meta']['source']=='PLUNGER_RESERVED':a['meta'].update(group='hardware',id='PLUNGER-TRAVEL',status='PURCHASE_BEFORE_CNC',names={'en':'Plunger internal travel/service reserve','pt-BR':'Reserva interna de curso/serviço do plunger'})
D.update(manual=manual,source_head=C['head_before']);D['hardware']=cat
D['quantity_overlay']=read('exports/generated/structural-v335/hardware-quantity-closure.json')['rows']
# Match original hardware schema if it was a list.
oldD=json.loads(gzip.decompress((R/'exports/generated/solid-leg-v334/viewer-data.json.gz').read_bytes()))
if isinstance(oldD['hardware'],list):D['hardware']=cat['hardware']
for k,f in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[k]=read('exports/generated/structural-v335/'+f+'.json')
Q['material']=read('exports/generated/structural-v335/material-utilization.json')['stocks']
oldpieces=Q['pieces'];Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for p in reg['parts']:
 if 'packing_mesh' in oldpieces.get(p['instance_id'],{}):Q['pieces'][p['instance_id']]['packing_mesh']=oldpieces[p['instance_id']]['packing_mesh']
steps={t['id']:t for s in manual['stages'] for t in s['steps']}
for clip in Q['clips']:
 if clip['type']=='assembly':
  t=steps[clip['step']];clip.update(title={k:t['id']+' · '+v for k,v in t['title'].items()},piece_ids=t['component_ids'],hardware_ids=t['hardware_ids'],action=t['action'],check=t['check'])
  clip['note']={'en':'SCHEMATIC ASSEMBLY ANIMATION. '+t['action']['en'],'pt-BR':'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. '+t['action']['pt-BR']}
# No invented insertion trajectory for the newly captured joints or stop rail.
Q['validation']['order_changes']=manual['order_changes']
(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n')
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
base=base.replace('../solid-leg-v334/manufacturing-bom','../structural-v335/manufacturing-bom').replace('href="../solid-leg-v334/README.md" target="_blank">${tr(\'Material','href="../structural-v335/README.md" target="_blank">${tr(\'Material').replace('V33.4','V33.5')
# Preserve SW01 jig script and data exactly. Add a separate unlocated control
# schematic rather than placing guessed button centers on current cabinetry.
ui=(R/'tools/viewer-v335-controls.js').read_text();base=base.replace("m.visible=required(m)&&!m.userData.meta.tray&&","m.visible=(required(m)||(clip.step==='07.2'&&m.userData.meta.group==='mainfans'))&&!m.userData.meta.tray&&")
base=base.replace("let visible=required(m)&&!meta.tray&&","let visible=(required(m)||(clip.step==='07.2'&&meta.group==='mainfans'))&&!meta.tray&&")
base=base.replace('</body>','<script>'+ui+'</script></body>')
(R/'exports/generated/viewer-v32/index.html').write_text(base)
print('V335_VIEWER_PASS',len(D['installed']),sum(p['meta']['kind']=='wood' for p in D['detail']),len(Q['clips']))

"""Rebind every changed installed/detail/state/packing representation to V33.6.2 CAD.
CERN-OHL-S-2.0. Offline controls/EN/PT/palettes and SW01 jig stay intact.
"""
from pathlib import Path
import json,gzip,re,base64,copy,subprocess,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/playfield-rest-v3362'
read=lambda p:json.loads((R/p).read_text());C=read('config/playfield_rest_v3362.json')
base=subprocess.check_output(['git','show',C['head_before']+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S).group(1))))
Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1));v=read('exports/generated/playfield-rest-v3362/geometry-validation.json');assert v['pass']
reg=read('exports/generated/playfield-rest-v3362/manufacturing-register.json');manual=read('exports/generated/playfield-rest-v3362/assembly-manual.json');changed=json.loads(gzip.decompress((O/'changes-mesh.json.gz').read_bytes()));pieces=json.loads(gzip.decompress((O/'manufacturing-mesh.json.gz').read_bytes()))
def geometry(k,m):D['geometry'][k]=m;return k
def pose(m,angle=0,pivot=(300,1066.8,508),dz=0):
 out=copy.deepcopy(m);a=math.radians(angle);c,s=math.cos(a),math.sin(a);px,py,pz=pivot
 out['vertices']=[[x,py+(y-py)*c-(z-pz)*s,pz+(y-py)*s+(z-pz)*c+dz] for x,y,z in m['vertices']];return out
def world(m,mat):
 out=copy.deepcopy(m);out['vertices']=[[sum(mat[i*4+j]*v[j] for j in range(3))+mat[i*4+3] for i in range(3)] for v in m['vertices']];return out
for n,m in changed.items():
 gid=geometry('v3362-'+n,m);a=next(d for d in D['installed'] if d['key']==n);a['geometry']=gid
 for state,entries in D['states'].items():
  variant=m
  if n=='PF_BasePlywood':
   if state=='SERVICE':variant=pose(m,-50,(300,1035.25061984718,484.220330114907))
   elif state=='LIFT-OUT':variant=pose(m,dz=48)
  elif n.startswith('BB_') and state in ['BACKBOX FOLD','FOLD45','FOLD1']:variant=pose(m,{'BACKBOX FOLD':90,'FOLD45':45,'FOLD1':1}[state])
  entries[n]=geometry('v3362-'+state+'-'+n,variant)
 for d in D['detail']:
  if d['meta']['source']==n and d['meta']['kind']!='wood':d['geometry']=gid
for p in reg['parts']:
 i=p['instance_id'];n=p['source_component']
 if i not in pieces:continue
 a=next(d for d in D['installed'] if d['key']==n);a['meta'].update(manufacturing_status=[p['manufacturing_status']],families=[p['manufacturing_part_id']],instances=[i],status='PURCHASE_BEFORE_CNC' if n.startswith('SIDE_') else 'WAITING_FOR_COUPON')
 d=next(d for d in D['detail'] if d['key']==i);d['geometry']=geometry('v3362-piece-'+i,world(pieces[i],p['local_to_installed_matrix']));d['meta']=copy.deepcopy(a['meta']);d['meta'].update(id=p['manufacturing_part_id'],instance=i);d['source_mesh']='V33.6.2 exact manufacturing B-rep';d['source_matrix']=p['local_to_installed_matrix']
# Every displayed object carries a traceable authority, including unchanged ones.
currenthash=hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest();priorhash=hashlib.sha256((R/C['source']).read_bytes()).hexdigest();authority=[]
for a in D['installed']+D['detail']:
 n=a['meta'].get('source');isnew=n in changed
 source='exports/generated/playfield-rest-v3362/play.FCStd' if isnew else C['source'];record={'file':source,'sha256':currenthash if isnew else priorhash,'object':n,'status':'CURRENT_V3362' if isnew else 'V3361_EXACTLY_PRESERVED'}
 if a['meta'].get('tray'):record={'file':a['meta'].get('model_path','config/hardware_catalog_v335.json'),'status':'UNLOCATED_REFERENCE_HARDWARE_LIBRARY'}
 a['meta']['geometry_authority']=record;a['meta']['model_status']=record['status']+' · '+record['file'];authority.append({'key':a['key'],**record})
 if n=='PF_BasePlywood':a['meta']['names']={'en':'Playfield base · clean front relief / rear service window','pt-BR':'Base do playfield · alívio frontal limpo / janela traseira'}
 if n and n.startswith(('Leaf','Button')):a['meta']['model_status']+=' · Y89/Y127; local top minus65mm; hardware bores HOLD'
 if n=='PF_BasePlywood':a['meta']['model_status']+=' · CLOSED_POSITION_SUPPORT_BLOCKED';a['meta']['names']={'en':'Playfield base ·52 mm front inset / closed support HOLD','pt-BR':'Base do playfield ·recuo frontal52 mm / apoio fechado PENDENTE'}
D.update(manual=manual,source_head=C['head_before']);D['geometry_revision']='V33.6.2'
HOLD={'en':'CLOSED_POSITION_SUPPORT_BLOCKED: no front landing is modeled; T1–T3 are22 mm below the base. PLAY is a reference pose, not a self-supporting build. Existing motion evidence validates clearance only.', 'pt-BR':'CLOSED_POSITION_SUPPORT_BLOCKED: não há apoio frontal modelado; T1–T3 estão22 mm abaixo da base. PLAY é posição de referência, sem apoio próprio. Evidência de movimento valida apenas folgas.'}
D['engineering_hold']=HOLD
Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for p in reg['parts']:
 if p['manufacturing_part_id']=='SW01':
  oldq=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1));prior=oldq['pieces'][p['instance_id']]
  if 'packing_mesh' in prior:Q['pieces'][p['instance_id']]['packing_mesh']=prior['packing_mesh']
for k,f in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[k]=read('exports/generated/playfield-rest-v3362/'+f+'.json')
Q['material']=read('exports/generated/playfield-rest-v3362/material-utilization.json')['stocks'];steps={t['id']:t for s in manual['stages'] for t in s['steps']}
for clip in Q['clips']:
 if clip['type']=='assembly':
  t=steps[clip['step']];clip.update(title={k:t['id']+' · '+v for k,v in t['title'].items()},piece_ids=t['component_ids'],hardware_ids=t['hardware_ids'],action=t['action'],check=t['check'],note={lang:('SCHEMATIC ASSEMBLY ANIMATION. ' if lang=='en' else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+t['action'][lang] for lang in ['en','pt-BR']})
Q['engineering_hold']=HOLD
for clip in Q['clips']:
 for lang in ['en','pt-BR']:clip['note'][lang]=HOLD[lang]+' '+clip['note'].get(lang,'')
# Drop unused historical horn geometry, never active old-state/cache fallbacks.
used={a['geometry'] for a in D['installed']+D['detail']}
for entries in D['states'].values():used.update(x for x in entries.values() if x)
D['geometry']={k:g for k,g in D['geometry'].items() if k in used}
(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n');(O/'viewer-authority.json').write_text(json.dumps({'geometry_revision':'V33.6.2','objects':authority,'changed_representations':['installed and named states','actual manufacturing detail','packing references'],'manufacturing_release':False},indent=2)+'\n')
# Rename only old HTML chrome before injecting CURRENT payloads; otherwise
# V33.6.2 would become V33.6.2.1 and historical manual notes would be altered.
base=base.replace('V33.6.1','V33.6.2')
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
base=base.replace('../button-relief-v3361/manufacturing-bom','../playfield-rest-v3362/manufacturing-bom').replace('href="../button-relief-v3361/README.md"','href="../playfield-rest-v3362/README.md"')
# Existing note area communicates the unresolved rest on every named state.
needle="$('state-note').textContent=txt;"
assert base.count(needle)==1
base=base.replace(needle,"$('state-note').textContent=L(D.engineering_hold)+' '+txt;")
(R/'exports/generated/viewer-v32/index.html').write_text(base)
# Compact sparse native-derived mesh for the CURRENT consumer.
installed={a['key']:a for a in D['installed']}
def part(n,g):return {'name':n,'label':installed[n]['meta']['names']['en'],**D['geometry'][g],'geometry_authority':installed[n]['meta']['geometry_authority']}
states={state:{n:part(n,g) if g else None for n,g in entries.items() if n in installed and g!=installed[n]['geometry']} for state,entries in D['states'].items()}
review=read('exports/generated/backbox-lock-integration-v32/mesh.json')['review'];review['buttons']={q['kind']:{'y_mm':q['y_mm'],'z_mm':q['z_mm']} for q in json.loads((R/'config/button_relief_v3361.json').read_text())['side_buttons']['centers']};review['V3362']={'authority':'config/playfield_rest_v3362.json','side_button_final_bore_mm':None,'horn_absent':True,'release':False}
(O/'mesh.json.gz').write_bytes(gzip.compress(json.dumps({'parts':[part(n,a['geometry']) for n,a in installed.items()],'states':states,'review':review},separators=(',',':')).encode(),mtime=0))
print('V3362_VIEWER_PASS',len(installed),len(authority),len(Q['clips']))

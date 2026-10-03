"""Exact V33.6.3 landing models, semantic inspection and certified motion overlay.
CERN-OHL-S-2.0. No manufacturing release or guessed purchased hardware.
"""
from pathlib import Path
import json,gzip,re,base64,copy,subprocess,hashlib,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/front-landings-v3363'
read=lambda p:json.loads((R/p).read_text());C=read('config/front_landings_v3363.json');S=read(str(O.relative_to(R))+'/support-validation.json');passed=bool(S['architecture_pass'])
base=subprocess.check_output(['git','show',C['head_before']+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S).group(1))));oldhold=D.get('engineering_hold',{})
Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1));priorQ=copy.deepcopy(Q)
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));assert N['pass'];VM=read(str(O.relative_to(R))+'/viewer-motion.json');reg=read(str(O.relative_to(R))+'/manufacturing-register.json');manual=read(str(O.relative_to(R))+'/assembly-manual.json');cat=read('config/hardware_catalog_v3363.json');hw={h['id']:h for h in cat['hardware']};objects=cat['object_to_id'];pieces=json.loads(gzip.decompress((O/'manufacturing-mesh.json.gz').read_bytes()));wood=collections.defaultdict(list)
for p in reg['parts']:wood[p['source_component']].append(p)
oldi={p['key']:p for p in D['installed']};oldd={p['key']:p for p in D['detail']};owned=set(N['added'])|set(N['changed']);landing_names=set(N['added'])
def geometry(k,m):D['geometry'][k]=m;return k
def world(m,mat):
 out=copy.deepcopy(m);out['vertices']=[[sum(mat[i*4+j]*v[j] for j in range(3))+mat[i*4+3] for i in range(3)] for v in m['vertices']];return out
def meta(n):
 ps=wood.get(n,[]);h=hw.get(objects.get(n));solid=bool(ps)
 return {'classification':h['flatpack_classification'] if h else 'REQUIRED_FLATPACK_HARDWARE','id':ps[0]['manufacturing_part_id'] if solid else h['id'] if h else n,'source':n,
 'names':{'en':('Front playfield closed support · '+ps[0]['description_en']) if solid else ('Front playfield closed support · '+h['description_en']) if h else ('Front playfield closed support · '+n),'pt-BR':('Apoio frontal do playfield fechado · '+ps[0]['description_pt_BR']) if solid else ('Apoio frontal do playfield fechado · '+h['description_pt_BR']) if h else ('Apoio frontal do playfield fechado · '+n)},
 'group':'landings','scope':'PLAYFIELD','kind':'wood' if solid else 'hardware' if h else 'reference','assembly':'playfield_front_support','stage':'05','material':ps[0]['material_class'] if solid else h['material'] if h else 'REFERENCE_ONLY','thickness':ps[0]['nominal_stock_thickness_mm'] if solid else None,'quantity':sum(p['quantity'] for p in ps) if solid else h['quantity'] if h else None,'hardware_id':h['id'] if h else None,'families':list(dict.fromkeys(p['manufacturing_part_id'] for p in ps)),'instances':[p['instance_id'] for p in ps],'manufacturing_status':[p['manufacturing_status'] for p in ps],'status':h['freeze_status'] if h else 'WAITING_FOR_COUPON','quantity_status':h['quantity_status'] if h else 'EXACT_FROM_DESIGN','formula':None}
D['groups'].insert(3,{'id':'landings','names':{'en':'PLAYFIELD LANDINGS','pt-BR':'APOIOS FRONTAIS DO PLAYFIELD'}})
for n in sorted(owned):
 mesh=N['states']['PLAY'][n];gid=geometry('v3363-'+n,mesh)
 if n in oldi:oldi[n]['geometry']=gid
 else:
  m=meta(n);xs=[v[0] for v in mesh['vertices']];off=[-90 if (min(xs)+max(xs))/2<300 else 90,-50,40]
  a={'key':n,'geometry':gid,'meta':m,'overview':off};D['installed'].append(a);oldi[n]=a
 for state,meshes in N['states'].items():
  D['states'].setdefault(state,{})[n]=geometry('v3363-'+state+'-'+n,meshes[n]) if meshes.get(n) else None
 for a in D['detail']:
  if a['meta'].get('source')==n and a['meta']['kind']!='wood':a['geometry']=gid
for n in landing_names:
 if n in wood:continue
 a=oldi[n];h=hw.get(a['meta']['hardware_id']);inst=next((i for i in h['instances'] if i['object']==n),{}) if h else {};direction=inst.get('installation_direction');off=list(a['overview'])
 if direction:off=[off[i]-direction[i]*65 for i in range(3)]
 D['detail'].append({'key':'HW:'+n,'geometry':a['geometry'],'meta':copy.deepcopy(a['meta']),'offset':off,'installation_direction':direction,'source_mesh':'V33.6.3 installed original reference hardware'})
for p in reg['parts']:
 iid=p['instance_id'];n=p['source_component']
 if iid not in pieces:continue
 a=oldi[n];m=copy.deepcopy(a['meta']);m.update(id=p['manufacturing_part_id'],instance=iid,quantity=sum(q['quantity'] for q in reg['parts'] if q['manufacturing_part_id']==p['manufacturing_part_id']),families=[p['manufacturing_part_id']],instances=[iid],face_A=p['face_A_outward_world'],thickness=p['nominal_stock_thickness_mm'],manufacturing_status=[p['manufacturing_status']],finish_count=len(p['manual_finish']))
 gid=geometry('v3363-piece-'+iid,world(pieces[iid],p['local_to_installed_matrix']))
 if iid in oldd:oldd[iid].update(geometry=gid,meta=m,source_mesh='V33.6.3 exact manufacturing B-rep',source_matrix=p['local_to_installed_matrix'])
 else:
  off=list(a['overview']);off[2]+=35*sum(1 for q in D['detail'] if (q['meta'].get('source') or '').startswith(n.rsplit('_Layer',1)[0]) and q['meta']['kind']=='wood')
  D['detail'].append({'key':iid,'geometry':gid,'meta':m,'offset':off,'source_mesh':'V33.6.3 exact manufacturing B-rep','source_matrix':p['local_to_installed_matrix']})
curhash=hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest();assert curhash==N['source_sha256'];priorhash=hashlib.sha256((R/C['source']).read_bytes()).hexdigest();authority=[]
for a in D['installed']+D['detail']:
 n=a['meta'].get('source');isnew=n in owned;src=str(O.relative_to(R))+'/play.FCStd' if isnew else C['source'];record={'file':src,'sha256':curhash if isnew else priorhash,'object':n,'status':'CURRENT_V3363' if isnew else 'V3362_EXACTLY_PRESERVED'}
 if a['meta'].get('tray'):record={'file':a['meta'].get('model_path','config/hardware_catalog_v335.json'),'status':'UNLOCATED_REFERENCE_HARDWARE_LIBRARY'}
 a['meta']['geometry_authority']=record;a['meta']['model_status']=record['status']+' · '+record['file'];authority.append({'key':a['key'],**record})
 if n in landing_names:a['meta']['model_status']+=' · FRONT PLAYFIELD CLOSED SUPPORT · '+('ARCHITECTURE_PASS / PHYSICAL QUALIFICATION HOLD' if passed else 'CLOSED_POSITION_SUPPORT_BLOCKED')
 if n=='PF_BasePlywood':a['meta']['names']={'en':'Playfield base · rear dowel + front landing support','pt-BR':'Base do playfield · cavilha traseira + apoios frontais'}
HOLD={'en':'Closed support architecture validated at the unchanged9.906669° PLAY pose; rear dowel + two front landings. ±3 mm is tolerance compensation only, not a height/tilt adjustment. Lowered−3 mm pose collides with buttons. T1–T3 intentionally clear. Physical hardware/material/load qualification and CNC release remain HOLD.','pt-BR':'Arquitetura validada na posição PLAY inalterada de9,906669°; cavilha traseira + dois apoios frontais. ±3 mm compensa tolerâncias, não altera altura/inclinação. Posição rebaixada−3 mm colide com botões. T1–T3 com folga intencional. Validação física de ferragens/material/carga e CNC permanecem PENDENTES.'} if passed else oldhold
D.update(manual=manual,hardware=cat['hardware'],source_head=C['head_before'],geometry_revision='V33.6.3',engineering_hold=HOLD,landings={'names':sorted(landing_names),'architecture_pass':passed,'motion':VM,'manufacturing_release':False})
Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for p in reg['parts']:
 if p['manufacturing_part_id']=='SW01' and priorQ['pieces'][p['instance_id']].get('packing_mesh'):Q['pieces'][p['instance_id']]['packing_mesh']=priorQ['pieces'][p['instance_id']]['packing_mesh']
for k,f in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[k]=read(str(O.relative_to(R))+'/'+f+'.json')
Q['material']=read(str(O.relative_to(R))+'/material-utilization.json')['stocks'];steps={t['id']:t for s in manual['stages'] for t in s['steps']};existing={c['step'] for c in Q['clips'] if c['type']=='assembly'}
for sid,t in steps.items():
 if sid not in existing:Q['clips'].insert(next(i for i,c in enumerate(Q['clips']) if c['type']!='assembly'),{'id':'assembly-'+sid,'type':'assembly','title':t['title'],'stage':sid.split('.')[0],'step':sid,'first_stage_step':False,'duration_s':8,'status':'SCHEMATIC_ASSEMBLY_ANIMATION'})
Q['clips']=sorted([c for c in Q['clips'] if c['type']=='assembly'],key=lambda c:tuple(int(x) for x in c['step'].split('.')))+[c for c in Q['clips'] if c['type']!='assembly']
for clip in Q['clips']:
 if clip['type']=='assembly':
  t=steps[clip['step']];clip.update(title={k:t['id']+' · '+v for k,v in t['title'].items()},piece_ids=t['component_ids'],hardware_ids=t['hardware_ids'],action=t['action'],check=t['check'],note={lang:('SCHEMATIC ASSEMBLY ANIMATION. ' if lang=='en' else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+t['action'][lang] for lang in ['en','pt-BR']})
 else:
  for lang in ['en','pt-BR']:clip['note'][lang]=clip['note'][lang].removeprefix(oldhold.get(lang,'')).strip()
 if not passed:
  for lang in ['en','pt-BR']:clip['note'][lang]=HOLD[lang]+' '+clip['note'][lang]
access=read(str(O.relative_to(R))+'/tool-access.json');coin=read('config/front_panel_v32.json')['coin_door'];Q['motions']['landing_access']={'axis':coin['hinge_axis_mm'],'open_angle_deg':access['coin_door_open_deg'],'names':access['coin_members_opened'],'authority':'tools/coin_door_v32.py turn + front-landings-v3363/tool-access.json'}
Q['engineering_hold']=HOLD;Q['motions']['pf_names']=VM['playfield_moving_names'];Q['motions']['front_landings']=VM
notes={'en':'Main glass and matrix removed; retainers released and parked. Landing bodies remain fixed; front pads separate naturally. Support raised module; physical qualification remains HOLD.','pt-BR':'Vidro principal e matriz removidos; retenções soltas/estacionadas. Apoios permanecem fixos; a base separa naturalmente das pontas. Sustente o módulo levantado; validação física PENDENTE.'}
for clip in Q['clips']:
 if clip.get('mode') in ['PF','PF_LIFT']:clip['note']=notes
for id,mode,title,note,dur in [('service-pf-release','PF_RELEASE',{'en':'Release front playfield retention','pt-BR':'Soltar retenções frontais do playfield'},{'en':'TOOL OPERATED. Open the front coin door110° first (shown). Support module; withdraw both captive hex bolts with compact spanner to the released stops. Axial reference-envelope motion only; thread turns and exact tool size follow selected hardware. Landing bodies stay installed.','pt-BR':'OPERAÇÃO POR FERRAMENTA. Abra primeiro a porta frontal de moedas110° (mostrada). Sustente o módulo; recue ambos os parafusos cativos com chave compacta até os batentes. Movimento axial de referência; voltas da rosca e chave dependem da ferragem. Apoios permanecem instalados.'},9),('service-pf-close','PF_CLOSE',{'en':'Seat rear dowel → lower front → retain','pt-BR':'Assentar cavilha → abaixar frente → reter'},{'en':'Coin door110° open for tool access. Rear seating first, then lower onto front pads and engage captive retention. Main glass/matrix removed. Rigid path is validated only where the native motion certificate explicitly says so; final hardware/load qualification remains HOLD.','pt-BR':'Porta frontal de moedas110° aberta para acesso da ferramenta. Assente primeiro a cavilha, abaixe nos apoios frontais e engate retenções. Vidro principal/matriz removidos. Trajeto rígido validado somente onde consta no certificado nativo; ferragens/carga finais PENDENTES.'},14)]:Q['clips'].append({'id':id,'type':'service','mode':mode,'title':title,'note':note,'duration_s':dur,'status':'NATIVE_PATH_AND_PROVISIONAL_AXIAL_HARDWARE_ENVELOPES' if VM.get('closing',{}).get('validated') else 'SCHEMATIC_ASSEMBLY_ANIMATION'})
used={a['geometry'] for a in D['installed']+D['detail']}
for e in D['states'].values():used.update(g for g in e.values() if g)
D['geometry']={k:g for k,g in D['geometry'].items() if k in used}
# Current document chrome only; never rewrite historical strings in new payloads.
base=base.replace('V33.6.2','V33.6.3')
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
base=base.replace('../playfield-rest-v3362/manufacturing-bom','../front-landings-v3363/manufacturing-bom').replace('href="../playfield-rest-v3362/README.md"','href="../front-landings-v3363/README.md"')
# The following bounded changes extend existing controls, preserving all older UI.
needle="const STATES=[";assert base.count(needle)==1;base=base.replace(needle,"const STATES=[['PLAYFIELD LANDINGS','PLAYFIELD LANDINGS','APOIOS FRONTAIS DO PLAYFIELD'],['SUPPORT LOAD PATH','SUPPORT LOAD PATH','CAMINHOS DE CARGA'],['PLAYFIELD RETENTION RELEASED','PLAYFIELD RETENTION RELEASED','RETENÇÕES DO PLAYFIELD SOLTAS'],")
base=base.replace("'PLAYFIELD LIFT-OUT':'LIFT-OUT'","'PLAYFIELD LIFT-OUT':'LIFT-OUT','PLAYFIELD RETENTION RELEASED':'PF RELEASED'")
base=base.replace("function colorFor(m,v){", "function colorFor(m,v){if(m.group==='landings')return m.kind==='wood'?(v==='accessible'?0xc8b878:0xd8bf91):(v==='accessible'?0x425d75:0x667985);")
base=base.replace("if(supports)groupInputs.supports.checked=false;", "if(supports){groupInputs.supports.checked=false;groupInputs.landings.checked=false;}")
base=base.replace("['playfield','supports','matrix'])groupInputs", "['playfield','supports','landings','matrix'])groupInputs")
needle="if(value.startsWith('EXPLODED'))$('explode-panel').open=true;"
assert base.count(needle)==1
extra="""if(value==='PLAYFIELD LANDINGS'){for(const g of D.groups)groupInputs[g.id].checked=g.id==='landings';}
 if(value==='SUPPORT LOAD PATH'){for(const g of D.groups)groupInputs[g.id].checked=['landings','supports','playfield','shell'].includes(g.id);for(const n of ['PLAYFIELD_ENVELOPE','CandidateGlass','SIDE_L','FRONT','REAR','BACKBOX_BASE'])hidden.add(n);}
 """
base=base.replace(needle,extra+needle)
# New service modes share the existing scrub/play/pause/speed controls.
needle="const mode=clip.mode;V.applyState(['DOORS','LOCK','FAN'].includes(mode)?'BACKBOX REAR DOORS OPEN':mode==='FOLD'?'BACKBOX FOLD 90°':'PLAY');"
assert base.count(needle)==1
base=base.replace(needle,"const mode=clip.mode;V.applyState(['PF','PF_LIFT','PF_CLOSE'].includes(mode)?'PLAYFIELD RETENTION RELEASED':['DOORS','LOCK','FAN'].includes(mode)?'BACKBOX REAR DOORS OPEN':mode==='FOLD'?'BACKBOX FOLD 90°':'PLAY');")
base=base.replace("['PF','PF_LIFT','MATRIX','SHELF']", "['PF','PF_LIFT','PF_CLOSE','PF_RELEASE','MATRIX','SHELF']")
needle="if(mode==='PF_LIFT'&&Q.motions.pf_names.includes(n))move(m,[0,0,48*p]);";assert base.count(needle)==1
new="""
   const fl=Q.motions.front_landings,release=fl.release_translation_by_object_mm?.[n]||fl.release_translation_xyz_mm||[0,0,0];
   if(['PF_RELEASE','PF_CLOSE'].includes(mode)&&Q.motions.landing_access.names.includes(n))spin(m,[0,0,1],-Q.motions.landing_access.open_angle_deg*Math.PI/180,Q.motions.landing_access.axis);
   if(mode==='PF_RELEASE'&&fl.retention_moving_names.includes(n))move(m,release.map(x=>x*p));
   if(mode==='PF_CLOSE'){
    const a=fl.closing.initial_open_angle_deg,h=fl.closing.initial_lift_mm;
    if(Q.motions.pf_names.includes(n)){const angle=p<.4?a:a*(1-clamp((p-.4)/.4));spin(m,[1,0,0],-angle*Math.PI/180,Q.motions.pf_axis);m.position.z+=h*(1-clamp(p/.4));}
    if(fl.retention_moving_names.includes(n))move(m,release.map(x=>-x*clamp((p-.8)/.2)));
   }
"""
base=base.replace(needle,needle+new)
# Counts are generated, never a stale literal31 after adding landing stages.
base=base.replace("'31 schematic assembly clips; validated rigid service paths identified separately. No manufacturing release.'", "Q.clips.filter(c=>c.type==='assembly').length+' schematic assembly clips; validated rigid service paths identified separately. No manufacturing release.'").replace("'31 animações esquemáticas; trajetos rígidos de serviço validados identificados separadamente. Sem liberação de fabricação.'", "Q.clips.filter(c=>c.type==='assembly').length+' animações esquemáticas; trajetos rígidos de serviço validados identificados separadamente. Sem liberação de fabricação.'")
base=base.replace('</body>',(R/'tools/viewer-v3363/landings.js').read_text()+'</body>')
(R/'exports/generated/viewer-v32/index.html').write_text(base)
(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n');(O/'viewer-authority.json').write_text(json.dumps({'geometry_revision':'V33.6.3','objects':authority,'native_sha256':curhash,'support_architecture_pass':passed,'manufacturing_release':False},indent=2)+'\n')
installed={a['key']:a for a in D['installed']}
def part(n,g):return {'name':n,'label':installed[n]['meta']['names']['en'],**D['geometry'][g],'geometry_authority':installed[n]['meta']['geometry_authority']}
poses={state:{n:part(n,g) if g else None for n,g in e.items() if n in installed and g!=installed[n]['geometry']} for state,e in D['states'].items()}
review=read('exports/generated/backbox-lock-integration-v32/mesh.json')['review'];review['V3363']={'authority':'config/front_landings_v3363.json','support_architecture_pass':passed,'release':False}
(O/'mesh.json.gz').write_bytes(gzip.compress(json.dumps({'parts':[part(n,a['geometry']) for n,a in installed.items()],'states':poses,'review':review},separators=(',',':')).encode(),mtime=0))
print('V3363_VIEWER_PASS',len(installed),len(authority),len(Q['clips']))

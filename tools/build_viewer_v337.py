"""V33.7 exact two-stock meshes and generic underfront variants. CERN-OHL-S-2.0.
Changes visual/documentary state only; no authored physical geometry or final bores.
"""
from pathlib import Path
import json,gzip,re,base64,copy,subprocess,hashlib,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/two-stock-user-module-v337';P=str(O.relative_to(R))+'/'
def prose(t):
 t=re.sub(r'([A-Za-zÀ-ÿ]{2,})(\d)',r'\1 \2',t);return re.sub(r'(\d)(mm|kg|deg|buttons|botões)\b',r'\1 \2',t).replace(' +dual',' + dual').replace('—5','— 5').replace('—6','— 6')
def read(p):return json.loads((R/p).read_text())
C=read('config/underfront_user_module_v337.json');base=subprocess.check_output(['git','show',C['head_before']+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S).group(1))));Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S).group(1));priorQ=copy.deepcopy(Q)
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));assert N['pass'];reg=read(P+'manufacturing-register.json');manual=read(P+'assembly-manual.json');cat=read('config/hardware_catalog_v337.json');MM=read(P+'module-motion.json');hw={h['id']:h for h in cat['hardware']};objects=cat['object_to_id'];piece_mesh=json.loads(gzip.decompress((O/'manufacturing-mesh.json.gz').read_bytes()));wood=collections.defaultdict(list)
for p in reg['parts']:wood[p['source_component']].append(p)
oldi={a['key']:a for a in D['installed']};oldd={a['key']:a for a in D['detail']};owned=set(N['changed'])|set(N['added'])|set(N.get('variant_only_names',[]));removed=set(N['removed']);modules={n for n in owned if n.startswith('Underfront')}
D['installed']=[a for a in D['installed'] if a['key'] not in removed];D['detail']=[a for a in D['detail'] if a['meta'].get('source') not in removed]
for e in D['states'].values():
 for n in removed:e.pop(n,None)
D['groups'].append({'id':'underfront','names':{'en':'UNDERFRONT USER MODULE','pt-BR':'MÓDULO DO USUÁRIO SOB A FRENTE'}})
def g(k,m):D['geometry'][k]=m;return k
def world(m,matrix):
 out=copy.deepcopy(m);out['vertices']=[[sum(matrix[i*4+j]*v[j] for j in range(3))+matrix[i*4+3] for i in range(3)] for v in m['vertices']];return out
def metadata(n):
 role=re.fullmatch(r'Underfront_Button(\d+)_(.+)',n);cfgname={'en':('Generic programmable button '+role[1]+' · '+role[2]) if role else 'Generic dual USB reference · '+n.removeprefix('Underfront_USB') if n.startswith('Underfront_USB') else 'Underfront module reference','pt-BR':('Botão programável genérico '+role[1]+' · '+{'Body':'corpo','Nut':'porca','Face':'face','Switch':'microswitch','WireReserve':'reserva de fios'}.get(role[2],role[2])) if role else 'Referência USB duplo · '+{'Body':'corpo','Nut':'porca','Flange':'flange','Cap':'tampa','CableReserve':'reserva de cabo'}.get(n.removeprefix('Underfront_USB'),n.removeprefix('Underfront_USB')) if n.startswith('Underfront_USB') else 'Referência do módulo sob a frente'}
 ps=wood.get(n,[]);h=hw.get(objects.get(n));cfg=MM.get('object_metadata',{}).get(n,{});solid=bool(ps)
 return {'classification':h['flatpack_classification'] if h else 'REQUIRED_FLATPACK_HARDWARE' if solid else 'USER_ADAPTER_HARDWARE','id':ps[0]['manufacturing_part_id'] if solid else h['id'] if h else cfg.get('id','UserModule'), 'source':n,'names':{'en':ps[0]['description_en'] if solid else h['description_en'] if h else cfg.get('names',{}).get('en',cfgname['en']),'pt-BR':ps[0]['description_pt_BR'] if solid else h['description_pt_BR'] if h else cfg.get('names',{}).get('pt-BR',cfgname['pt-BR'])},'group':'underfront','scope':'MAIN CABINET','kind':'wood' if solid else 'reference' if n.startswith(('Underfront_Button','Underfront_USB')) else 'hardware' if h else 'reference','assembly':'underfront_user_module','stage':'07','material':ps[0]['material_class'] if solid else h['material'] if h else 'REFERENCE_ONLY','thickness':ps[0]['nominal_stock_thickness_mm'] if solid else None,'quantity':sum(p['quantity'] for p in ps) if solid else h['quantity'] if h else cfg.get('quantity',1),'hardware_id':h['id'] if h else None,'families':list(dict.fromkeys(p['manufacturing_part_id'] for p in ps)),'instances':[p['instance_id'] for p in ps],'manufacturing_status':[p['manufacturing_status'] for p in ps],'status':h['freeze_status'] if h else 'WAITING_FOR_COUPON' if solid else 'HARDWARE_PENDING','quantity_status':h['quantity_status'] if h else 'EXACT_FROM_DESIGN' if solid else 'USER_CONFIGURABLE','formula':None,'configuration_status':cfg.get('configuration_status','OWNER_CONFIG / HARDWARE_PENDING' if n.startswith('Underfront_USB') else 'GENERIC_CONFIG / HARDWARE_PENDING'),'variant_ids':[v['id'] for v in MM['variants'] if n in v['object_names']]}
for n in sorted(owned):
 gid=g('v337-'+n,N['states']['PLAY'][n])
 if n in oldi:
  a=oldi[n];a['geometry']=gid
  if n in wood:a['meta'].update(thickness=wood[n][0]['nominal_stock_thickness_mm'],manufacturing_status=[p['manufacturing_status'] for p in wood[n]],families=list(dict.fromkeys(p['manufacturing_part_id'] for p in wood[n])))
 else:
  a={'key':n,'geometry':gid,'meta':metadata(n),'overview':[0,-90,-70]};D['installed'].append(a);oldi[n]=a
 for state,meshes in N['states'].items():D['states'].setdefault(state,{})[n]=g('v337-'+state+'-'+n,meshes[n]) if meshes.get(n) else None
 for a in D['detail']:
  if a['meta'].get('source')==n and a['meta']['kind']!='wood':a['geometry']=gid
# Nominal stock metadata also changes for the6mm finished bezel cut from12mm stock.
for n,ps in wood.items():
 if n in oldi:oldi[n]['meta'].update(thickness=ps[0]['nominal_stock_thickness_mm'],manufacturing_status=[p['manufacturing_status'] for p in ps],families=list(dict.fromkeys(p['manufacturing_part_id'] for p in ps)))
for n in N['added']+N.get('variant_only_names',[]):
 if n in wood:continue
 a=oldi[n];h=hw.get(a['meta']['hardware_id']);instance=next((i for i in h['instances'] if i['object']==n),{}) if h else {};direction=instance.get('installation_direction');off=list(a['overview'])
 if direction:off=[off[i]-direction[i]*55 for i in range(3)]
 D['detail'].append({'key':'HW:'+n,'geometry':a['geometry'],'meta':copy.deepcopy(a['meta']),'offset':off,'installation_direction':direction,'source_mesh':'V33.7 original reference envelope'})
for p in reg['parts']:
 iid=p['instance_id'];n=p['source_component']
 if iid not in piece_mesh:continue
 a=oldi.get(n);m=copy.deepcopy(a['meta'] if a else oldd[iid]['meta']);m.update(id=p['manufacturing_part_id'],instance=iid,quantity=sum(q['quantity'] for q in reg['parts'] if q['manufacturing_part_id']==p['manufacturing_part_id']),families=[p['manufacturing_part_id']],instances=[iid],face_A=p['face_A_outward_world'],thickness=p['nominal_stock_thickness_mm'],manufacturing_status=[p['manufacturing_status']],finish_count=len(p['manual_finish']))
 gid=g('v337-piece-'+iid,world(piece_mesh[iid],p['local_to_installed_matrix']))
 if iid in oldd:oldd[iid].update(geometry=gid,meta=m,source_mesh='V33.7 exact manufacturing B-rep',source_matrix=p['local_to_installed_matrix'])
 else:D['detail'].append({'key':iid,'geometry':gid,'meta':m,'offset':[0,-90,-70-25*len(m['instances'])],'source_mesh':'V33.7 exact manufacturing B-rep','source_matrix':p['local_to_installed_matrix']})
part_by_id={p['instance_id']:p for p in reg['parts']}
curhash=hashlib.sha256((O/'play.FCStd').read_bytes()).hexdigest();assert curhash==N['source_sha256'];priorhash=hashlib.sha256((R/C['source']).read_bytes()).hexdigest();authority=[]
for a in D['installed']+D['detail']:
 n=a['meta'].get('source');current=n in owned;src=P+'play.FCStd' if current else C['source'];record={'file':src,'sha256':curhash if current else priorhash,'object':n,'status':'CURRENT_V337' if current else 'V3363_EXACTLY_PRESERVED'}
 if n in N.get('variant_only_names',[]):record={**N['variant_source'],'file':N['variant_source']['path'],'object':n,'status':'CURRENT_V337_ALTERNATIVE_REFERENCE_ONLY'}
 if a['key'] in piece_mesh:
  bp=part_by_id[a['key']]['finished_member_brep'];record={'file':bp,'sha256':hashlib.sha256((R/bp).read_bytes()).hexdigest(),'object':n,'status':'CURRENT_V337_MANUFACTURING_PIECE','local_to_installed_matrix':part_by_id[a['key']]['local_to_installed_matrix']}
 if a['meta'].get('tray'):record={'file':a['meta'].get('model_path','config/hardware_catalog_v3363.json'),'status':'UNLOCATED_REFERENCE_HARDWARE_LIBRARY'}
 a['meta']['geometry_authority']=record;a['meta']['model_status']=record['status']+' · '+record['file'];authority.append({'key':a['key'],**record})
 if n in modules:a['meta']['model_status']+=' · '+a['meta'].get('configuration_status','GENERIC_CONFIG')+' / HARDWARE_PENDING'
for a in D['installed']+D['detail']:
 if a['meta'].get('source','') and a['meta']['source'].startswith('Underfront'):a['meta']['names']={lang:prose(t) for lang,t in a['meta']['names'].items()}
D.update(manual=manual,hardware=cat['hardware'],source_head=C['head_before'],geometry_revision='V33.7',underfront=MM)
D['engineering_hold']={lang:text+(' Current plywood uses 12/18 mm nominal stocks only; actual thickness and coupon remain held. Underfront controls are generic user configuration; final button/USB cuts are unselected.' if lang=='en' else ' Compensado atual usa apenas 12/18 mm nominais; espessura real e cupom continuam pendentes. Controles sob a frente são configuração do usuário; recortes finais de botão/USB indefinidos.') for lang,text in D['engineering_hold'].items()}
Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for p in reg['parts']:
 if p['manufacturing_part_id']=='SW01' and priorQ['pieces'][p['instance_id']].get('packing_mesh'):Q['pieces'][p['instance_id']]['packing_mesh']=priorQ['pieces'][p['instance_id']]['packing_mesh']
for key,f in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[key]=read(P+f+'.json')
Q['material']=read(P+'material-utilization.json')['stocks'];Q['engineering_hold']=D['engineering_hold'];Q['motions']['underfront']=MM;Q['motions']['underfront_screw_schematic_travel_mm']=C['module']['screw_underhead_reference_mm']+10
steps={t['id']:t for s in manual['stages'] for t in s['steps']};existing={c['step'] for c in Q['clips'] if c['type']=='assembly'}
for sid,t in steps.items():
 if sid not in existing:Q['clips'].append({'id':'assembly-'+sid,'type':'assembly','title':t['title'],'stage':sid.split('.')[0],'step':sid,'first_stage_step':False,'duration_s':8,'status':'SCHEMATIC_ASSEMBLY_ANIMATION'})
Q['clips']=sorted([c for c in Q['clips'] if c['type']=='assembly'],key=lambda c:tuple(int(x) for x in c['step'].split('.')))+[c for c in Q['clips'] if c['type']!='assembly']
for clip in Q['clips']:
 if clip['type']=='assembly':
  t=steps[clip['step']];clip.update(title={k:t['id']+' · '+v for k,v in t['title'].items()},piece_ids=t['component_ids'],hardware_ids=t['hardware_ids'],action=t['action'],check=t['check'],note={lang:('SCHEMATIC ASSEMBLY ANIMATION. ' if lang=='en' else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+t['action'][lang] for lang in ['en','pt-BR']})
Q['clips'].append({'id':'service-underfront','type':'service','mode':'UNDERFRONT','title':{'en':'Underfront user-module removal','pt-BR':'Retirada do módulo do usuário sob a frente'},'note':{'en':('Rigid panel removal path validated. ' if MM['rigid_removal_validated'] else 'SCHEMATIC ASSEMBLY ANIMATION. ')+ 'SCHEMATIC fastener unthreading first, then the panel path. Support the plate, release four attachments and lower it. Harness flex/connector interface remains hardware-dependent; no connector family is prescribed. Generic controls are translucent reference envelopes; they intentionally overlap the uncut blank plate. They are not released holes.','pt-BR':('Trajeto rígido da placa validado. ' if MM['rigid_removal_validated'] else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+ 'Desrosqueamento ESQUEMÁTICO dos fixadores primeiro, depois trajeto da placa. Sustente a placa, solte quatro fixações e abaixe. Flexão/interface do chicote depende das ferragens; não se impõe família de conector. Controles genéricos são envelopes de referência translúcidos; sobrepõem intencionalmente a placa cega sem cortes. Não são furos liberados.'},'duration_s':10,'status':'NATIVE_RIGID_PANEL_PATH_HARNESS_PROVISIONAL' if MM['rigid_removal_validated'] else 'SCHEMATIC_ASSEMBLY_ANIMATION'})
for clip in Q['clips']:
 if clip['id']=='service-underfront':clip['note']={lang:prose(t) for lang,t in clip['note'].items()}
used={a['geometry'] for a in D['installed']+D['detail']}
for e in D['states'].values():used.update(x for x in e.values() if x)
D['geometry']={k:m for k,m in D['geometry'].items() if k in used}
base=base.replace('V33.6.3','V33.7')
assert base.count('target_kg===25')==3
base=base.replace('target_kg===25','target_kg===Q.packaging.preferred_target_kg')
# Remove the earlier unlocated fixed-function schematic, retaining historical files.
pattern=r'<script>/\* Original CERN-OHL-S-2.0\. Unlocated owner-authorized under-front schematic\. \*/.*?</script>'
base,count=re.subn(pattern,'',base,flags=re.S);assert count==1,'Historical fixed-function schematic must be replaced exactly once'
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
base=base.replace('../front-landings-v3363/manufacturing-bom','../two-stock-user-module-v337/manufacturing-bom').replace('href="../front-landings-v3363/README.md"','href="../two-stock-user-module-v337/README.md"')
base=base.replace('const STATES=[',"const STATES=[['UNDERFRONT USER MODULE','UNDERFRONT USER MODULE','MÓDULO DO USUÁRIO SOB A FRENTE'],",1)
base=base.replace("if(state.startsWith('EXPLODED'))txt=","if(state==='UNDERFRONT USER MODULE')txt=t('UNDERSIDE SERVICE · the visible FLOOR contains the 18 mm bay; the 12 mm plate is removable. Controls are translucent reference envelopes overlapping an undrilled blank. Final device/attachment machining remains HOLD.','SERVIÇO INFERIOR · o FLOOR visível contém o alojamento 18 mm; a placa 12 mm é removível. Controles são envelopes translúcidos sobre a placa cega sem furos. Usinagem final de controles/fixação PENDENTE.');if(state.startsWith('EXPLODED'))txt=",1)
base=base.replace("function colorFor(m,v){","function colorFor(m,v){if(m.group==='underfront')return m.kind==='wood'?(v==='accessible'?0xc8b878:0xd8bf91):(v==='accessible'?0x456681:0x648d9c);")
base=base.replace('m.visible=!!visible;',"if(state==='UNDERFRONT USER MODULE'&&m.name==='FLOOR')visible=true;if(meta.group==='underfront'&&meta.variant_ids?.length)visible=visible&&meta.variant_ids.includes(window.underfront337?.variant||D.underfront.default_variant);m.visible=!!visible;",1)
base=base.replace("if(value.startsWith('EXPLODED'))$('explode-panel').open=true;", "if(value==='UNDERFRONT USER MODULE'){for(const g of D.groups)groupInputs[g.id].checked=g.id==='underfront';}if(value.startsWith('EXPLODED'))$('explode-panel').open=true;",1)
base=base.replace("const mode=clip.mode;V.applyState(","const mode=clip.mode;V.applyState(mode==='UNDERFRONT'?'UNDERFRONT USER MODULE':",1)
base=base.replace("V.cameraPreset(['PF'", "V.cameraPreset(mode==='UNDERFRONT'?'FRONT':['PF'",1)
base=base.replace("||m.name.startsWith('BB_')));","||clip.mode==='UNDERFRONT'&&m.name.startsWith('Underfront')||m.name.startsWith('BB_')));",1)
needle="if(mode==='PF_LIFT'&&Q.motions.pf_names.includes(n))move(m,[0,0,48*p]);";assert needle in base
extra="""
   if(mode==='UNDERFRONT'&&Q.motions.underfront.screw_names.includes(n))move(m,[0,0,-Q.motions.underfront_screw_schematic_travel_mm*clamp(p/.25)]);
   if(mode==='UNDERFRONT'&&Q.motions.underfront.removable_names.includes(n)){const q=clamp((p-.25)/.75);
    if(Q.motions.underfront.rigid_removal_validated)move(m,Q.motions.underfront.removal_vector_mm.map(x=>x*q));
    else{move(m,Q.motions.underfront.removal_vector_mm.map(x=>x*(q<.5?0:1)));m.material.opacity=Math.abs(1-2*q)*m.userData.baseOpacity;m.material.transparent=true;}
   }
"""
base=base.replace(needle,needle+extra)
base=base.replace('base=V.installed.map(m=>',"if(clip.mode==='UNDERFRONT')window.underfront337?.orient();base=V.installed.map(m=>",1)
base=base.replace('</body>',(R/'tools/viewer-v337/underfront.js').read_text()+'</body>')
(R/'exports/generated/viewer-v32/index.html').write_text(base);(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n');(O/'viewer-authority.json').write_text(json.dumps({'geometry_revision':'V33.7','objects':authority,'native_sha256':curhash,'manufacturing_release':False},indent=2)+'\n')
installed={a['key']:a for a in D['installed']}
def part(n,gid):return {'name':n,'label':installed[n]['meta']['names']['en'],**D['geometry'][gid],'geometry_authority':installed[n]['meta']['geometry_authority']}
poses={state:{n:part(n,gid) if gid else None for n,gid in e.items() if n in installed and gid!=installed[n]['geometry']} for state,e in D['states'].items()};review=read('exports/generated/backbox-lock-integration-v32/mesh.json')['review'];review['V337']={'authority':'config/underfront_user_module_v337.json','release':False}
(O/'mesh.json.gz').write_bytes(gzip.compress(json.dumps({'parts':[part(n,a['geometry']) for n,a in installed.items()],'states':poses,'review':review},separators=(',',':')).encode(),mtime=0));print('V337_VIEWER_PASS',len(installed),len(authority),len(Q['clips']))

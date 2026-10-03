"""V33.8 exact SW02, optional modularity and explicit service holds. CERN-OHL-S-2.0."""
from pathlib import Path
import json,gzip,re,base64,copy,subprocess,hashlib,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/service-productization-v338';P=str(O.relative_to(R))+'/'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def bi(en,pt):return {'en':en,'pt-BR':pt}
C=read('config/service_productization_v338.json');base=subprocess.check_output(['git','show',C['head_before']+':exports/generated/viewer-v32/index.html'],cwd=R,text=True)
D=json.loads(gzip.decompress(base64.b64decode(re.search(r'<script id="viewer-data"[^>]*>(.*?)</script>',base,re.S)[1])));Q=json.loads(re.search(r'<script id="v333-data"[^>]*>(.*?)</script>',base,re.S)[1]);priorQ=copy.deepcopy(Q)
N=json.loads(gzip.decompress((O/'viewer-native.json.gz').read_bytes()));assert N['pass'] and N['source_sha256']==sha(P+'play.FCStd')
reg=read(P+'manufacturing-register.json');manual=read(P+'assembly-manual.json');cat=read('config/hardware_catalog_v338.json');hw={h['id']:h for h in cat['hardware']};wood={p['source_component']:p for p in reg['parts'] if p['manufacturing_part_id']=='SW02'};pm=json.loads(gzip.decompress((O/'manufacturing-mesh.json.gz').read_bytes()))
owned=set(N['changed'])|set(N['added']);removed=set(N['removed']);oldi={a['key']:a for a in D['installed']};oldd={a['key']:a for a in D['detail']}
D['installed']=[a for a in D['installed'] if a['key'] not in removed];D['detail']=[a for a in D['detail'] if a['meta'].get('source') not in removed and a['meta'].get('hardware_id')!='F60']
for state in D['states'].values():
 for n in removed:state.pop(n,None)
def geom(key,m):D['geometry'][key]=m;return key
def world(m,matrix):
 q=copy.deepcopy(m);q['vertices']=[[sum(matrix[i*4+j]*v[j] for j in range(3))+matrix[i*4+3] for i in range(3)] for v in m['vertices']];return q
for n in sorted(owned):
 p=wood[n];m=copy.deepcopy(oldi[n.replace('_Block','_Layer1')]['meta']);m.update(id='SW02',source=n,names=bi(p['description_en'],p['description_pt_BR']),material=p['material_class'],thickness=None,quantity=2,families=['SW02'],instances=[p['instance_id']],manufacturing_status=[p['manufacturing_status']],status='PURCHASE_BEFORE_ASSEMBLY / QUALIFIED_GUIDE_HOLD',manufacturing_class=p['manufacturing_class'],face_A=p['face_A_outward_world'])
 m['geometry_authority']={'file':P+'play.FCStd','sha256':N['source_sha256'],'object':n,'status':'CURRENT_V338'};m['model_status']='CURRENT V33.8 · SHOP-MADE SOLID WOOD · 68 × 70 × 54 mm · NO CNC · physical qualification HOLD'
 a={'key':n,'geometry':geom('v338-'+n,N['states']['PLAY'][n]),'meta':m,'overview':[-90 if 'L_' in n else 90,-50,40]};D['installed'].append(a)
 for state,meshes in N['states'].items():D['states'].setdefault(state,{})[n]=geom('v338-'+state+'-'+n,meshes[n]) if meshes.get(n) else None
 mm=copy.deepcopy(m);mm.update(instance=p['instance_id'],instances=[p['instance_id']],finish_count=len(p['manual_finish']),face_A=p['face_A_outward_world']);mm['geometry_authority']={'file':p['finished_member_brep'],'sha256':sha(p['finished_member_brep']),'object':n,'status':'CURRENT_V338_MANUFACTURING_PIECE','local_to_installed_matrix':p['local_to_installed_matrix']}
 D['detail'].append({'key':p['instance_id'],'geometry':geom('v338-piece-'+p['instance_id'],world(pm[p['instance_id']],p['local_to_installed_matrix'])),'meta':mm,'offset':a['overview'],'source_mesh':'V33.8 exact SW02 manufacturing B-rep','source_matrix':p['local_to_installed_matrix']})
# Original catalogue rows remain intact; active metadata exposes the newer authority overlay.
for a in D['installed']+D['detail']:
 m=a['meta']
 if m.get('hardware_id')=='H27':m['model_status']+=' · Mechanical travel ±3 mm; installed common-height geometry screen −1.9/+0.9 mm only; setup to unchanged nominal pose, no differential twist';m['adjustment_authority']=cat['v338_adjustment_authority']
D['groups'] += [{'id':'accessories','names':bi('Optional accessory boards','Placas opcionais de acessórios')},{'id':'routes','names':bi('Cable route zones','Zonas de passagem de cabos')}]
for n,mesh in N['study'].items():
 if not n.startswith(('Accessory','PowerRoute','SignalRoute')):continue
 board=n in ['AccessoryBoardS2Right','AccessoryBoardS3Left'];payload='Payload' in n;route=n.startswith(('PowerRoute','SignalRoute'));iid='ACC01-S2' if 'S2Right' in n else 'ACC01-S3';desc=bi('ACC01 optional board · S2 right' if 'S2Right' in n else 'ACC01 optional board · S3 left','Placa opcional ACC01 · S2 direita' if 'S2Right' in n else 'Placa opcional ACC01 · S3 esquerda') if board else bi('Optional payload reference' if payload else 'ELV power route planning zone' if n.startswith('Power') else 'Signal route planning zone' if route else 'Removable C-clamp packaging reserve','Referência de carga opcional' if payload else 'Zona de potência ELV' if n.startswith('Power') else 'Zona de sinal' if route else 'Reserva de embalagem do grampo removível')
 m={'id':'ACC01' if board else 'POWER_ROUTE' if n.startswith('Power') else 'SIGNAL_ROUTE' if route else 'OPTIONAL_REFERENCE','source':n,'names':desc,'group':'routes' if route else 'accessories','scope':'MAIN CABINET','kind':'wood' if board else 'reference','assembly':'optional_accessories','stage':'18','material':'MODULAR_SECONDARY' if board else 'REFERENCE_ONLY','thickness':12 if board else None,'quantity':None,'hardware_id':None,'families':['ACC01'] if board else [],'instances':[iid] if board else [],'manufacturing_status':['OPTIONAL / HARDWARE_PENDING'],'status':'OPTIONAL / PHYSICAL_FIT_LOAD_HOLD','quantity_status':'USER_CONFIGURABLE','classification':'OPTIONAL_FLATPACK_HARDWARE','optional_study':True,'geometry_authority':{'file':N['study_source']['path'],'sha256':N['study_source']['sha256'],'object':n,'status':'ISOLATED_OPTIONAL_STUDY_NOT_MINIMUM'},'model_status':'OPTIONAL STUDY · not in minimum BOM, packing or mass · clamp / payload / cable physical qualification HOLD'}
 a={'key':n,'geometry':geom('v338-study-'+n,mesh),'meta':m,'overview':[0,0,40]};D['installed'].append(a)
 if board:
  dm=copy.deepcopy(m);dm['instance']=iid;D['detail'].append({'key':iid,'geometry':a['geometry'],'meta':dm,'offset':[0,0,70],'source_mesh':'Isolated ACC01 optional CAD board, not minimum manufacturing set'})
# Fixed bodies remain fixed in every semantic motion; no safety strap or hand-retention model is promoted.
for obj in [D['landings']['motion'],Q['motions']['front_landings']]:obj['fixed_landing_names']=[n for n in obj['fixed_landing_names'] if n not in removed]+N['added'];obj['status']='RIGID_PATH_GEOMETRY_ONLY; PRIMARY_50_DEG_SUPPORT_HOLD'
D['landings']['names']=[n for n in D['landings']['names'] if n not in removed]+N['added'];D['landings']['safe_adjustment_mm']=C['adjustment']['final_safe_range_mm'];D['landings']['primary_service_support_status']='HOLD_NO_DEFINED_PRIMARY_50_DEG_SUPPORT'
HOLD=bi('PRIMARY RAISED-PLAYFIELD SUPPORT: HOLD — no defined/proven primary support at 50°. Motion views show geometric paths only; do not work beneath the raised playfield. No secondary safety straps are selected. Closed PLAY support uses rear dowel + two SW02 front blocks, at unchanged 9.906669°. Installed setup screen −1.9/+0.9 mm; mechanical ±3 mm is not usable travel. Original captive M6 retention is TOOL-operated. Physical hardware, wood, coupon and CNC remain HOLD.','APOIO PRIMÁRIO DO PLAYFIELD ELEVADO: PENDENTE — sem apoio definido/comprovado em 50°. Vistas mostram apenas trajetos geométricos; não trabalhe sob o playfield elevado. Nenhuma cinta secundária foi selecionada. PLAY fechado usa cavilha traseira + dois blocos SW02, a 9,906669° inalterados. Teste instalado de ajuste −1,9/+0,9 mm; curso mecânico ±3 mm não é faixa utilizável. Retenção M6 cativa original exige FERRAMENTA. Ferragens, madeira, cupom e CNC permanecem PENDENTES.')
D.update(manual=manual,hardware=cat['hardware'],source_head=C['head_before'],geometry_revision='V33.8',engineering_hold=HOLD,modularity={'study_source':N['study_source'],'minimum_bom_includes_accessories':False,'primary_support_hold':True,'backbox_harness_validated':False})
Q['pieces']={p['instance_id']:{k:p[k] for k in ['local_to_installed_matrix','finished_xy_size_mm','finished_xy_bounds_mm','manufacturing_part_id']} for p in reg['parts']}
for iid,info in Q['pieces'].items():
 if iid in N['packing_meshes']:info['packing_mesh']=world(N['packing_meshes'][iid],info['local_to_installed_matrix'])
 elif priorQ['pieces'].get(iid,{}).get('packing_mesh'):info['packing_mesh']=priorQ['pieces'][iid]['packing_mesh']
for key,f in [('metrics','project-metrics'),('mass','mass-budget'),('hardware','hardware-dashboard'),('packaging','packaging')]:Q[key]=read(P+f+'.json')
Q['material']=read(P+'material-utilization.json')['stocks'];Q['engineering_hold']=HOLD
steps={t['id']:t for s in manual['stages'] for t in s['steps']};existing={c['step'] for c in Q['clips'] if c['type']=='assembly'}
for sid,t in steps.items():
 if sid not in existing:Q['clips'].append({'id':'assembly-'+sid,'type':'assembly','title':t['title'],'stage':sid.split('.')[0],'step':sid,'first_stage_step':True,'duration_s':8,'status':'SCHEMATIC_ASSEMBLY_ANIMATION'})
Q['clips']=sorted([c for c in Q['clips'] if c['type']=='assembly'],key=lambda c:tuple(int(x) for x in c['step'].split('.')))+[c for c in Q['clips'] if c['type']!='assembly']
for clip in Q['clips']:
 if clip['type']=='assembly':
  t=steps[clip['step']];clip.update(title={k:t['id']+' · '+v for k,v in t['title'].items()},piece_ids=t['component_ids'],hardware_ids=t['hardware_ids'],action=t['action'],check=t['check'],note={lang:('SCHEMATIC ASSEMBLY ANIMATION. ' if lang=='en' else 'ANIMAÇÃO ESQUEMÁTICA DE MONTAGEM. ')+t['action'][lang]+' '+t.get('hold',{}).get(lang,'') for lang in ['en','pt-BR']})
 if clip.get('mode') in ['PF','PF_LIFT','PF_CLOSE']:
  clip['status']='VALIDATED_RIGID_PATH_ONLY_PRIMARY_SERVICE_SUPPORT_HOLD';clip['note']={lang:HOLD[lang]+' '+clip['note'][lang] for lang in ['en','pt-BR']}
assert len({c['id'] for c in Q['clips']})==len(Q['clips'])
# Never rewrite historical action text or identifiers when changing version chrome.
base=base.replace('V33.7','V33.8')
base=base.replace("!['future','pc'].includes(g.id)","!['future','pc','accessories','routes'].includes(g.id)")
base=base.replace('const STATES=[',"const STATES=[['MODULARITY STUDY','OPTIONAL MODULARITY STUDY','ESTUDO DE MODULARIDADE OPCIONAL'],",1)
base=base.replace("if(value.startsWith('EXPLODED'))$('explode-panel').open=true;", "if(value==='MODULARITY STUDY'){for(const g of D.groups)groupInputs[g.id].checked=!['playfield','supports','matrix','pc','future','bbshell','bbglass','display','cassette','doors','bbfans','bbhardware','carrier'].includes(g.id);for(const n of ['CandidateGlass','SIDE_L','SIDE_R'])hidden.add(n);}if(value.startsWith('EXPLODED'))$('explode-panel').open=true;",1)
base=base.replace("if(state.startsWith('EXPLODED'))txt=", "if(state==='MODULARITY STUDY')txt=t('OPTIONAL STUDY · ACC01 and generic removable clamps are excluded from minimum BOM, sheets, mass and packing. Routes are planning zones; actual clamp, payload, cable and backbox harness qualification remains HOLD.','ESTUDO OPCIONAL · ACC01 e grampos removíveis genéricos estão fora da BOM mínima, chapas, massa e embalagem. Rotas são zonas de planejamento; grampo, carga, cabo e chicote do backbox permanecem PENDENTES.');if(state.startsWith('EXPLODED'))txt=",1)
base=base.replace("function colorFor(m,v){", "function colorFor(m,v){if(m.optional_study)return m.kind==='wood'?(v==='accessible'?0xbcaa6b:0xcba66e):(m.group==='routes'?0x60868c:0x73818c);",1)
# Optional animation scopes never masquerade as delivered minimum pieces.
base=base.replace("const required=m=>m.userData.meta.kind==='wood'||m.userData.meta.classification==='REQUIRED_FLATPACK_HARDWARE';", "const required=m=>!m.userData.meta.optional_study&&(m.userData.meta.kind==='wood'||m.userData.meta.classification==='REQUIRED_FLATPACK_HARDWARE');")
base=base.replace('required(m)',"(required(m)||(clip?.step==='18.2'&&m.userData.meta.optional_study))")
base=base.replace("if(clip.stage==='01')visible=meta.kind==='wood';", "if(clip.stage==='01')visible=meta.kind==='wood'&&!meta.optional_study;")
base=base.replace("same=meta.stage===clip.stage","same=meta.stage===clip.stage||clip.piece_ids?.includes(m.name)")
base=base.replace("m.visible&&m.userData.meta.stage===clip.stage","m.visible&&(m.userData.meta.stage===clip.stage||clip.piece_ids?.includes(m.name))")

base=base.replace("Front pads reproduce the approved PLAY pose and transverse level. ±3 mm only compensates tolerances; it is not a new playing-height/tilt range. T1–T3 remain clear. Release both captive retainers before opening.","SW02 solid blocks preserve the approved PLAY pose. Installed setup screen −1.9/+0.9 mm; mechanical ±3 mm is not usable travel. TOOL-operated M6 retainers remain. T1–T3 stay clear. PRIMARY 50° SERVICE SUPPORT HOLD — do not work beneath a raised playfield.")
base=base.replace("Pontas frontais reproduzem a posição PLAY aprovada e o nível transversal. ±3 mm compensa tolerâncias, não altera altura/inclinação. T1–T3 mantêm folga. Solte ambas as retenções cativas antes de abrir.","Blocos maciços SW02 preservam PLAY aprovado. Teste instalado −1,9/+0,9 mm; curso mecânico ±3 mm não é utilizável. Retenções M6 exigem FERRAMENTA. T1–T3 livres. APOIO PRIMÁRIO EM 50° PENDENTE — não trabalhe sob playfield elevado.")
used={a['geometry'] for a in D['installed']+D['detail']}
for e in D['states'].values():used.update(x for x in e.values() if x)
D['geometry']={k:m for k,m in D['geometry'].items() if k in used}
base=re.sub(r'(<script id="viewer-data"[^>]*>).*?(</script>)',lambda m:m[1]+base64.b64encode(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0)).decode()+m[2],base,flags=re.S)
base=re.sub(r'(<script id="v333-data"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(Q,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+m[2],base,flags=re.S)
base=base.replace('../two-stock-user-module-v337/manufacturing-bom','../service-productization-v338/manufacturing-bom').replace('href="../two-stock-user-module-v337/README.md"','href="../service-productization-v338/README.md"')
base=base.replace('</body>',(R/'tools/viewer-v338/modularity.js').read_text()+'</body>')
(R/'exports/generated/viewer-v32/index.html').write_text(base);(O/'viewer-data.json.gz').write_bytes(gzip.compress(json.dumps(D,separators=(',',':')).encode(),mtime=0));(O/'animations.json').write_text(json.dumps(Q['clips'],indent=2,ensure_ascii=False)+'\n')
authority=[{'key':a['key'],**a['meta'].get('geometry_authority',{})} for a in D['installed']+D['detail']];(O/'viewer-authority.json').write_text(json.dumps({'geometry_revision':'V33.8','objects':authority,'native_sha256':N['source_sha256'],'manufacturing_release':False},indent=2)+'\n')
installed={a['key']:a for a in D['installed'] if not a['meta'].get('optional_study')}
def part(n,gid):return {'name':n,'label':installed[n]['meta']['names']['en'],**D['geometry'][gid],'geometry_authority':installed[n]['meta'].get('geometry_authority')}
poses={state:{n:part(n,gid) if gid else None for n,gid in e.items() if n in installed and gid!=installed[n]['geometry']} for state,e in D['states'].items()};review=read('exports/generated/backbox-lock-integration-v32/mesh.json')['review'];review['V338']={'authority':'config/service_productization_v338.json','primary_support':'HOLD','release':False}
(O/'mesh.json.gz').write_bytes(gzip.compress(json.dumps({'parts':[part(n,a['geometry']) for n,a in installed.items()],'states':poses,'review':review},separators=(',',':')).encode(),mtime=0));print('V338_VIEWER_PASS',len(installed),len(Q['pieces']),len(Q['clips']))

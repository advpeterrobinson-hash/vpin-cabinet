"""Documentation-only viewer/manual from immutable V32/V33/V33.1. CERN-OHL-S-2.0."""
from pathlib import Path
from urllib.parse import quote
import base64,json,gzip,hashlib,re,sys,html,collections,math,subprocess
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/viewer-v332'))
from manual_content import STAGES
O=R/'exports/generated/viewer-v332';O.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads((R/p).read_text())
HEAD='a1f8bb04f7cec6a2220355c6b7ead0e7e0e92ab4'
CURRENT=read('config/current_v32.json');source=CURRENT['geometry_directory']
B=read(source+'/mesh.json');SC=read(source+'/review-mesh.json')
REG=read('exports/generated/flatpack-v331/manufacturing-register.json');WOOD=read('config/wood_materials_v33.json')['parts'];CAT=read('config/hardware_catalog_v33.json');HW={h['id']:h for h in CAT['hardware']}
CLOSE={h['id']:h for h in read('exports/generated/flatpack-v331/hardware-quantity-closure.json')['rows']}
W={p['object']:p for p in WOOD};P={p['id']:p for p in WOOD};members=collections.defaultdict(list)
for p in REG['parts']:members[p['source_component']].append(p)
family_qty=collections.Counter(p['manufacturing_part_id'] for p in REG['parts'])
GROUPS=[('shell','Main cabinet shell','Caixa principal'),('playfield','Playfield assembly','Montagem do playfield'),('supports','Playfield supports','Apoios do playfield'),('shelves','Shelves','Prateleiras'),('pc','PC / electronics envelopes','Volumes de PC / eletrônica'),('mainfans','Main cabinet fans','Ventoinhas principais'),('ssf','SSF / audio','SSF / áudio'),('matrix','Matrix cassette','Cassete da matriz'),('bbshell','Backbox shell','Estrutura do backbox'),('bbglass','Backbox front glass','Vidro frontal do backbox'),('display','Backglass display envelope','Volume do monitor do backbox'),('cassette','DMD / speaker cassette','Cassete DMD / alto-falantes'),('doors','Backbox rear doors','Portas traseiras do backbox'),('bbfans','Backbox fans','Ventoinhas do backbox'),('bbhardware','Backbox hardware','Ferragens do backbox'),('hardware','Cabinet hardware','Ferragens da caixa'),('future','Future electronics / toy envelopes','Volumes de eletrônica / brinquedos futuros'),('carrier','Display carrier','Suporte do monitor')]
# IDs below are documentation aliases, never a new engineering datum.
ALIASES={'SIDE_L':'SideL','SIDE_R':'SideR','FRONT':'Front','REAR':'Rear','FLOOR':'Floor','BACKBOX_BASE':'BBBase','PC_BASE':'PCBase','REAR_DOOR':'RearDoor','PF_BasePlywood':'PFBase','PF_OpenCradleL':'CradleL','PF_OpenCradleR':'CradleR','BB_Floor':'BBFloor','BB_SideL':'BBSideL','BB_SideR':'BBSideR','BB_Top':'BBTop','MatrixCarrier':'Matrix'}
for i in range(1,4):ALIASES['SHELF_'+str(i)]='S'+str(i);ALIASES['CROSS_'+str(i)]='T'+str(i)
def woodstage(n):
 if n=='BACKBOX_BASE' or n.startswith(('FLOOR','FLOOR_CLEAT')):return '03'
 if 'LegBlock' in n:return '16'
 if n=='SSF_BST_Carrier':return '18'
 if n=='PF_BasePlywood':return '06'
 if n.startswith('PF_OpenCradle'):return '05'
 if n.startswith(('SHELF','CROSS','PC_BASE')):return '04'
 if n.startswith(('MX_','Matrix')):return '15'
 if n.startswith('BB_'):
  if 'Parking' in n:return '09'
  if any(x in n for x in ['Intake','FanBlank']):return '11'
  if any(x in n for x in ['Door','HingeCleat','Astragal']):return '10'
  if any(x in n for x in ['Glass']):return '13'
  if any(x in n for x in ['Monitor','VESA','Display']):return '12'
  if any(x in n for x in ['Cassette','Speaker','DMD']):return '14'
  return '08'
 if n=='REAR_DOOR' or n.startswith('RemovableIntake'):return '07'
 return '02'
def hwstage(h):
 s={'01':'16','02':'04','03':'06','04':'07','05':'07','06':'09','07':'09','08':'10','09':'11','10':'12','11':'14','12':'15','13':'18'}[h['assembly_stage']]
 if h['id']=='F01':s='05'
 if h['id'] in ['F16','F54']:s='08'
 if h['id'] in ['F06','G01']:s='02'
 if h['id'] in ['F24','I08','G08','G09','G10']:s='13'
 if h['id'] in ['G11','G12','F36','H20','H21','H22','F39','H23','H24','F40']:s='16'
 return s

def group(n,h=None):
 if n.startswith('BB_Toy') or any(x in n for x in ['Payload','ConnectorReserve','CableReserve','PLUNGER_RESERVED']):return 'future'
 if n.startswith('PF_OpenCradle') or n.startswith('PF_SupportMount'):return 'supports'
 if n.startswith('PF_') or n in ['PLAYFIELD_ENVELOPE','CandidateGlass']:return 'playfield'
 if n.startswith(('Matrix','MX_')):return 'matrix'
 if n.startswith('BB_'):
  if n in ['BB_Backglass'] or 'Glass' in n:return 'bbglass'
  if n=='BB_Display32':return 'display'
  if any(x in n for x in ['Fan','Intake','Flex']):return 'bbfans'
  if any(x in n for x in ['Door','Piano','Astragal','CenterGasket','PassiveBolt','Cam']):return 'doors'
  if any(x in n for x in ['Monitor','VESA','DisplayReplaceable']):return 'carrier'
  if any(x in n for x in ['Cassette','DMD','Speaker']):return 'cassette'
  if n not in W:return 'bbhardware'
  return 'bbshell'
 if n.startswith('UprightLock') or n.startswith('Hinge') or (h and h['parent_assembly'].startswith('backbox') and not n):return 'bbhardware'
 if n.startswith('SSF'):return 'ssf'
 if n=='PC_ENVELOPE' or n.startswith('PC_') and n!='PC_BASE':return 'pc'
 if any(x in n for x in ['Fan','FAN_','Filter','Guard']):return 'mainfans'
 if n.startswith(('SHELF','CROSS','SimpleShelf','SimpleCross','PC_BASE')):return 'shelves'
 if n in W:return 'shell'
 if h and h['flatpack_classification'] in ['FUTURE_ELECTRONICS_HARDWARE','USER_ADAPTER_HARDWARE']:return 'future'
 return 'hardware'
def scope(g):return 'BACKBOX' if g in ['bbshell','bbglass','display','cassette','doors','bbfans','bbhardware','carrier'] else 'PLAYFIELD' if g in ['playfield','supports','matrix'] else 'MAIN CABINET'
def names(n):
 if n in W:
  w=W[n];a=ALIASES.get(n,w['id']);return {'en':w['description_en'].split(' — ')[0]+' · '+a,'pt-BR':w['description_pt_BR'].split(' — ')[0]+' · '+a}
 h=HW.get(CAT['object_to_id'].get(n))
 if h:return {'en':h['description_en'],'pt-BR':h['description_pt_BR']}
 return {'en':'Reference envelope','pt-BR':'Volume de referência'}
def meta(n):
 h=HW.get(CAT['object_to_id'].get(n));g=group(n,h);w=W.get(n);ps=members[n]
 return dict(classification=h['flatpack_classification'] if h else w['flatpack_classification'] if w else 'REFERENCE_ONLY_NOT_FROZEN',id=ALIASES.get(n,w['id'] if w else h['id'] if h else 'REF'),source=n,names=names(n),group=g,scope=scope(g),kind='wood' if w else 'reference' if not h or h['id'].startswith(('E','R')) else 'hardware',assembly=w['parent_assembly'] if w else h['parent_assembly'] if h else 'reference',stage=woodstage(n) if w else hwstage(h) if h else '18',model_status=json.loads((R/h['model']['path']).with_suffix('.json').read_text())['model_status'] if h else None,material=w['material_class'] if w else h['material'] if h else None,thickness=w['nominal_thickness_mm'] if w else None,quantity=w['quantity'] if w else h['quantity'] if h else None,hardware_id=h['id'] if h else None,families=sorted({p['manufacturing_part_id'] for p in ps}),instances=[p['instance_id'] for p in ps],manufacturing_status=sorted({p['manufacturing_status'] for p in ps}),status=h['freeze_status'] if h else 'WAITING_FOR_COUPON' if w else 'REFERENCE_ONLY_NOT_FROZEN',formula=CLOSE.get(h['id'],{}).get('formula') if h else None,quantity_status=CLOSE.get(h['id'],{}).get('classification',h['quantity_status']) if h else 'EXACT_FROM_DESIGN' if w else 'TRULY_TBD')
def offset(n,g,detailed=False):
 a=180 if detailed else 105
 if g=='bbshell':
  if 'SideL' in n:return [-a,0,400]
  if 'SideR' in n:return [a,0,400]
  if 'Top' in n:return [0,0,400+a]
  if 'Rear' in n:return [0,a,400]
  return [0,0,400]
 if g in ['doors','bbfans']:return [(-70 if n.endswith('L') else 70 if n.endswith('R') else 0),a*2,400]
 if g in ['display','bbglass']:return [0,-a*2,400]
 if g=='carrier':return [0,-a,400]
 if g=='cassette':return [0,-a*2.3,300]
 if g=='bbhardware':return [0,0,400]
 if g=='playfield':return [0,-80,300]
 if g=='supports':return [-a if n.endswith('L') or 'ScrewL' in n else a,0,0]
 if g=='matrix':return [0,-80,430]
 if g=='shelves':return [0,0,170+30*int(re.search(r'\d',n)[0]) if re.search(r'\d',n) else 170]
 if n=='SIDE_L':return [-a,0,0]
 if n=='SIDE_R':return [a,0,0]
 if n=='FRONT':return [0,-a,0]
 if n in ['REAR','REAR_DOOR']:return [0,a,0]
 if n=='FLOOR':return [0,0,-a]
 return [0,0,0]

def compact_mesh(p):return {'vertices':[[round(float(x),4) for x in v] for v in p['vertices']],'faces':p['faces']}
# Geometry data are rendering copies only. State meshes are deduplicated, never written back.
geometries={};geometry_hash={}
def geom(p):
 q=compact_mesh(p);raw=json.dumps(q,separators=(',',':'));h=hashlib.sha256(raw.encode()).hexdigest()
 if h not in geometry_hash:
  key='g'+str(len(geometries));geometry_hash[h]=key;geometries[key]=q
 return geometry_hash[h]
installed=[]
for p in B['parts']:
 m=meta(p['name']);installed.append({'key':p['name'],'geometry':geom(p),'meta':m,'overview':offset(p['name'],m['group'])})
# Retracted latch meshes are distinct saved service objects, not the closed tongues.
service_only=[]
for p in SC['scenes']['doors-open']:
 if 'RetractedReserve' in p['name']:
  old=p['name'].replace('RetractedReserve','ClosedReserve');m=meta(old);m['source']=p['name'];installed.append({'key':p['name'],'geometry':geom(p),'meta':m,'overview':offset(old,m['group'])});service_only.append(p['name'])
base_names={p['key'] for p in installed}
state_map={}
for state in ['PLAY','SERVICE','LIFT-OUT','MATRIX REMOVED','BACKBOX FOLD']:
 state_map[state]={n:geom(p) if p else None for n,p in B['states'][state].items() if n in base_names}
for state,scene in [('DOORS OPEN','doors-open'),('UNLOCKED','locks-parked'),('FOLD45','fold-45')]:
 src={p['name']:p for p in SC['scenes'][scene]};state_map[state]={n:geom(p) for n,p in src.items() if n in base_names}
 if state=='FOLD45':
  # Non-backbox removal is exactly the accepted fold state's prerequisite state.
  for n,v in state_map['BACKBOX FOLD'].items():
   if not n.startswith('BB_') and n not in state_map[state]:state_map[state][n]=v
for n in service_only:state_map['PLAY'][n]=None
for n in ['BB_CamTongueClosedReserve','BB_PassiveBoltClosedReserve0','BB_PassiveBoltClosedReserve1']:state_map['DOORS OPEN'][n]=None
# Use exact saved door-flex curves, not rigidly rotated cables.
flex_path=R/'exports/generated/backbox-service-v32/flex-visuals.json'
if flex_path.exists():
 fx=json.loads(flex_path.read_text())
 for dst,src in [('DOORS OPEN','rear-both-open'),('PLAY','rear-closed'),('FOLD45','fold-45'),('BACKBOX FOLD','fold-90')]:
  for n,p in fx['states'][src].items():state_map[dst][n]=geom(p)
# Reference toy volumes follow the same validated pure rotation at 45 degrees.
for p in B['parts']:
 if p['name'].startswith('BB_ToyZone'):
  c=math.sqrt(.5);v=[[x,1066.8+(y-1066.8)*c-(z-508)*c,508+(y-1066.8)*c+(z-508)*c] for x,y,z in p['vertices']]
  state_map['FOLD45'][p['name']]=geom({'vertices':v,'faces':p['faces']})
# Door-open and parked are independent accepted local overrides, composed only upright.
state_map['UNLOCKED']={**state_map['DOORS OPEN'],**{n:v for n,v in state_map['UNLOCKED'].items() if 'UprightLock' in n}}
# Hardware reserves are visually distinct and never presented as purchased holes.
for p in SC['details']['hinges']:
 m=meta(p['name']);m.update(id='WPC reserve',names={'en':'WPC hardware reserve · physical measurement required','pt-BR':'Reserva de ferragens WPC · exige medição física'},group='bbhardware',scope='BACKBOX',kind='reference',stage='09')
 installed.append({'key':p['name'],'geometry':geom(p),'meta':m,'overview':[0,0,400]})
 state_map['FOLD45'][p['name']]=None;state_map['BACKBOX FOLD'][p['name']]=None
# Detailed payload uses all 130 saved manufacturing meshes, in installed transforms.
wm=json.loads(gzip.decompress((R/'exports/generated/flatpack-v331/review-mesh.json.gz').read_bytes()))
hm=json.loads(gzip.decompress((O/'hardware-lod-installed.json.gz').read_bytes()))
lib=json.loads(gzip.decompress((O/'hardware-lod-family.json.gz').read_bytes()))
detail=[]
for p in REG['parts']:
 n=p['source_component'];m=meta(n);m.update(id=p['manufacturing_part_id'],instance=p['instance_id'],names={**m['names']},quantity=family_qty[p['manufacturing_part_id']],families=[p['manufacturing_part_id']],instances=[p['instance_id']],thickness=p['nominal_stock_thickness_mm'],manufacturing_status=[p['manufacturing_status']],face_A=p['face_A_outward_world'],finish_count=len(p['manual_finish']))
 suffix=p['instance_id'].split('-',1)[1];pt={'Main':'Principal','Cap':'Tampa','Strip':'Tira','Base18':'Base 18','Reduced18':'Reduzido 18','Face':'Face','Top':'Topo','SideL':'Lateral E','SideR':'Lateral D','ReturnL':'Retorno E','ReturnR':'Retorno D'}
 m['names']={'en':m['names']['en']+' / '+suffix,'pt-BR':m['names']['pt-BR']+' / '+pt.get(suffix,suffix.replace('Layer','Camada'))}
 v=wm[p['instance_id']];mat=p['local_to_installed_matrix'];verts=[[sum(mat[4*i+j]*x[j] for j in range(3))+mat[4*i+3] for i in range(3)] for x in v['vertices']]
 ds=offset(n,m['group'],True);siblings=members[n];idx=siblings.index(p)
 if len(siblings)>1:
  if 'IntakeDownBaffle' in n:
   role=p['instance_id'].split('-',1)[1]
   if role=='Face':ds[1]+=75
   elif role=='Top':ds[2]+=65
   else:
    center_x=(min(x[0] for x in verts)+max(x[0] for x in verts))/2
    assembly_center_x=W[n]['installed_coordinate_xyz_mm'][0]
    ds[0]+= -65 if center_x<assembly_center_x else 65
  else:
   # These accepted laminations stack in installed Z. Rank their actual centers,
   # not face-normal signs (opposed FACE A normals must not collapse an explosion).
   def center_z(q):
    mm=q['local_to_installed_matrix'];vv=wm[q['instance_id']]['vertices']
    zz=[sum(mm[8+j]*x[j] for j in range(3))+mm[11] for x in vv]
    return (min(zz)+max(zz))/2
   ordered=sorted(siblings,key=lambda q:(center_z(q),q['instance_id']))
   ds[2]+=(ordered.index(p)-(len(siblings)-1)/2)*50
 # Individual internal rails and shoes separate along FACE_A, keeping assembly order.
 elif m['group'] in ['carrier','shelves']:
  ds=[ds[i]+p['face_A_outward_world'][i]*45 for i in range(3)]
 detail.append({'key':p['instance_id'],'geometry':geom({'vertices':verts,'faces':v['faces']}),'meta':m,'offset':ds,'source_mesh':'V33.1 manufacturing member','source_matrix':mat})
tray=0
for h in CAT['hardware']:
 inst=[i for i in h['instances'] if i['object'] in hm and i['object'] not in W]
 for i in inst:
  n=i['object'];m=meta(n);d=i.get('installation_direction');off=offset(n,m['group'],True)
  if d:off=[off[j]-d[j]*(65 if h['id'].startswith('W') else 90 if h['id'].startswith('F') else 45) for j in range(3)]
  detail.append({'key':'HW:'+n,'geometry':geom(hm[n]),'meta':m,'offset':off,'installation_direction':d,'placement_status':h['installed_coordinate_status'],'source_mesh':'V33 installed hardware'})
 if not inst:
  # One exemplar per family, never a fabricated quantity/placement. Tray is labelled in UI.
  g={'playfield_pivot':'playfield','backbox_shell_wpc':'bbhardware','backbox_upright_locks':'bbhardware','backbox_doors':'doors','backbox_ventilation':'bbfans','display_glass_interfaces':'carrier','lower_cassette':'cassette','main_ventilation':'mainfans','shelves_supports':'shelves','matrix_front_interfaces':'matrix'}.get(h['parent_assembly'],'hardware')
  if h['flatpack_classification'] in ['FUTURE_ELECTRONICS_HARDWARE','USER_ADAPTER_HARDWARE','REFERENCE_ONLY_NOT_FROZEN']:g='future'
  m=dict(classification=h['flatpack_classification'],id=h['id'],model_status=json.loads((R/h['model']['path']).with_suffix('.json').read_text())['model_status'],source=None,names={'en':h['description_en'],'pt-BR':h['description_pt_BR']},group=g,scope=scope(g),kind='reference' if h['id'].startswith(('E','R')) else 'hardware',assembly=h['parent_assembly'],stage=hwstage(h),material=h['material'],thickness=None,quantity=h['quantity'],hardware_id=h['id'],families=[],instances=[],manufacturing_status=[],status=h['freeze_status'],formula=CLOSE.get(h['id'],{}).get('formula'),quantity_status=CLOSE.get(h['id'],{}).get('classification',h['quantity_status']),tray=True)
  detail.append({'key':'CAT:'+h['id'],'geometry':geom(lib[h['id']]),'meta':m,'offset':[-1200+(tray%9)*180,1600+(tray//9)*180,150],'placement_status':'UNLOCATED_FAMILY_EXEMPLAR_NOT_INSTALLED','source_mesh':'V33 original simplified family model'})
  tray+=1
# Step framework: each physical family belongs to one stage; global BOM quantities labelled explicitly.
manual={'version':'V33.2','source_head':HEAD,'language':'en','manufacturing_release':False,'status':'FRAMEWORK_NOT_VALIDATED_BUILD_INSTRUCTIONS','source_geometry_unchanged':True,'stages':[],'part_preparation':[],'hardware_quantity_overlay':list(CLOSE.values())}
view_states={'00':'PLAY','01':'EXPLODED DETAILED','02':'EXPLODED OVERVIEW','03':'INTERIOR INSPECTION','04':'EXPLODED DETAILED','05':'EXPLODED DETAILED','06':'PLAYFIELD LIFT-OUT','07':'INTERIOR INSPECTION','08':'EXPLODED DETAILED','09':'BACKBOX UNLOCKED','10':'BACKBOX REAR DOORS OPEN','11':'EXPLODED DETAILED','12':'BACKBOX INTERIOR','13':'EXPLODED DETAILED','14':'BACKBOX INTERIOR','15':'MATRIX REMOVAL','16':'EXPLODED DETAILED','17':'BACKBOX FOLD 45°','18':'INTERIOR INSPECTION'}
for idx,(en,pt,deps,steps) in enumerate(STAGES):
 sid=f'{idx:02}';pp=[p for p in REG['parts'] if woodstage(p['source_component'])==sid];hh=[h for h in CAT['hardware'] if hwstage(h)==sid]
 status='OPTIONAL' if sid=='18' else 'WAITING_FOR_COUPON' if sid in ['00','01'] else 'WAITING_FOR_PHYSICAL_MEASUREMENT' if sid in ['09','13','16','17'] else 'PROVISIONAL_HARDWARE'
 stage={'id':sid,'title':{'en':en,'pt-BR':pt},'depends_on':deps,'status':status,'pieces':[p['instance_id'] for p in pp],'hardware':[h['id'] for h in hh],'steps':[]}
 for k,(te,tp,ae,ap,ce,cp) in enumerate(steps,1):
  stage['steps'].append({'id':sid+'.'+str(k),'title':{'en':te,'pt-BR':tp},'status':status,'component_ids':stage['pieces'],'hardware_ids':stage['hardware'],'quantity_scope':'STAGE_REFERENCE_TOTALS_NOT_REPEATED_CONSUMPTION','orientation':{'en':'X left→right; Y front→rear; Z up. Follow each member’s FACE A card and installed-direction vector.','pt-BR':'X esquerda→direita; Y frente→trás; Z para cima. Siga a ficha FACE A e o vetor de orientação instalada de cada peça.'},'tools':{'en':'Clamps, square and measuring tools; selected drive/bit and depth stop for the listed hardware/finish only.','pt-BR':'Grampos, esquadro e instrumentos de medição; ponta/broca selecionada e limitador somente para as ferragens/acabamentos listados.'},'faces':{'en':'FACE A: CNC machining / finished depth datum. FACE B: NO CNC; manual access only where the preparation card explicitly specifies it.','pt-BR':'FACE A: usinagem CNC / referência acabada de profundidade. FACE B: SEM CNC; acesso manual somente quando explicitado na ficha.'},'action':{'en':ae,'pt-BR':ap},'check':{'en':ce,'pt-BR':cp},'hold':{'en':'Framework only. Clear the stage status, physical hardware/material/coupon and applicable load/finish holds before execution.','pt-BR':'Somente roteiro. Libere o estado da etapa e pendências físicas de ferragens/material/cupom e de carga/acabamento aplicáveis antes de executar.'},'next_state':view_states[sid],'checkpoint':True})
 manual['stages'].append(stage)
for p in REG['parts']:
 manual['part_preparation'].append({k:p[k] for k in ['instance_id','manufacturing_part_id','source_component','quantity','machining_face','opposite_face','face_A_outward_world','local_to_installed_matrix','local_datum','nominal_stock_thickness_mm','facing_reduction_mm','through_cuts','pockets','manual_finish','manufacturing_status','fit_dependent','coupon_dependent','joinery']})
(O/'assembly-manual.json').write_text(json.dumps(manual,ensure_ascii=False,indent=2)+'\n')
# Compact payload leaves heavy geometry as inert JSON and creates GPU buffers on demand.
payload={'groups':[{'id':k,'names':{'en':e,'pt-BR':p}} for k,e,p in GROUPS],'installed':installed,'states':state_map,'detail':detail,'geometry':geometries,'manual':manual,'hardware':CAT['hardware'],'quantity_overlay':list(CLOSE.values()),'source_head':HEAD,'source_mesh_sha256':hashlib.sha256((R/source/'mesh.json').read_bytes()).hexdigest(),'manufacturing_release':False}
packed=gzip.compress(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(),compresslevel=6,mtime=0)
(O/'viewer-data.json.gz').write_bytes(packed)
state_pt={'PLAY':'JOGO','EXPLODED DETAILED':'EXPLODIDA DETALHADA','EXPLODED OVERVIEW':'EXPLODIDA GERAL','INTERIOR INSPECTION':'INSPECIONAR INTERIOR','PLAYFIELD LIFT-OUT':'RETIRADA DO PLAYFIELD','BACKBOX UNLOCKED':'BACKBOX DESTRAVADO','BACKBOX REAR DOORS OPEN':'PORTAS DO BACKBOX ABERTAS','BACKBOX INTERIOR':'INTERIOR DO BACKBOX','MATRIX REMOVAL':'REMOÇÃO DA MATRIZ','BACKBOX FOLD 45°':'DOBRA DO BACKBOX 45°'}
# Manual preparation appendix includes every actual piece, not a bounding-box cut list.
for lang,fn in [('en','ASSEMBLY_MANUAL.md'),('pt-BR','ASSEMBLY_MANUAL.pt-BR.md')]:
 en=lang=='en';lines=['# '+('Assembly manual framework — V33.2' if en else 'Roteiro do manual de montagem — V33.2'),'','**'+('FRAMEWORK — MANUFACTURING RELEASE BLOCKED. Hardware, coupon and physical qualification holds remain.' if en else 'ROTEIRO — LIBERAÇÃO DE FABRICAÇÃO BLOQUEADA. Permanecem pendências de ferragens, cupom e validação física.')+'**','',('[Offline interactive manual and CAD](../exports/generated/viewer-v32/index.html?manual=00)' if en else '[Manual interativo e CAD offline](../exports/generated/viewer-v32/index.html?manual=00&lang=pt-BR)'),'',('Quantities below are global/stage reference totals; repeated steps do not consume another kit. Unknown counts remain unknown. A tray exemplar is not an installed position.' if en else 'As quantidades abaixo são totais de referência globais/da etapa; etapas repetidas não consomem outro kit. Quantidades desconhecidas permanecem abertas. Uma amostra na bandeja não é uma posição instalada.'),'']
 for stage in manual['stages']:
  sid=stage['id'];lines += [f"<a id=\"stage-{sid}\"></a>",f"## {sid} — {stage['title'][lang]}",f"\n**{stage['status']}** · "+('Depends on: ' if en else 'Depende de: ')+(', '.join(stage['depends_on']) or '—'),'']
  lines += [('Pieces (each instance ×1): ' if en else 'Peças (cada instância ×1): ')+(', '.join(f"{p['instance_id']} ({p['manufacturing_part_id']})" for p in REG['parts'] if p['instance_id'] in stage['pieces']) or '—'),'']
  lines += ['| ID | '+('Hardware' if en else 'Ferragem')+' | '+('Project quantity' if en else 'Quantidade no projeto')+' | Status |','|---|---|---|---|']
  for hid in stage['hardware']:
   h=HW[hid];q=CLOSE.get(hid,{});qty=str(h['quantity']) if h['quantity'] is not None else q.get('formula') or ('TBD — do not guess' if en else 'INDEFINIDA — não estimar');lines += [f"| {hid} | {h['description_en' if en else 'description_pt_BR']} | {qty} | {h['freeze_status']} |"]
  lines += ['']
  for s in stage['steps']:
   lines += [f"### {s['id']} — {s['title'][lang]}",'',s['action'][lang],'',('**Orientation:** ' if en else '**Orientação:** ')+s['orientation'][lang],('**Faces:** ' if en else '**Faces:** ')+s['faces'][lang],('**Tools:** ' if en else '**Ferramentas:** ')+s['tools'][lang],'',('**Checkpoint:** ' if en else '**Verificação:** ')+s['check'][lang],'',('**HOLD:** ' if en else '**PENDÊNCIA:** ')+s['hold'][lang],'',f"[{('Next-state CAD' if en else 'CAD do próximo estado')}: {s['next_state'] if en else state_pt[s['next_state']]}](../exports/generated/viewer-v32/index.html?manual={sid}&step={s['id']}&state={quote(s['next_state'])}&lang={lang})",'']
 lines += ['## '+('Per-piece preparation and orientation cards' if en else 'Fichas de preparação e orientação por peça'),'','**FACE A → +z '+('into stock; FACE B has NO CNC. All depths below are measured from finished FACE A. Directions are installed global vectors, not drilling templates.' if en else 'para dentro do material; FACE B SEM CNC. Todas as profundidades abaixo partem da FACE A acabada. As direções são vetores globais instalados, não gabaritos de furação.')+'**','']
 for p in REG['parts']:
  iid=p['instance_id'];card=f'../exports/generated/viewer-v332/orientation/{iid}.svg';lines += [f"### {iid} / {p['manufacturing_part_id']}",f"\n![FACE A / FACE B]({card})\n",f"**{p['manufacturing_status']}** · {p['nominal_stock_thickness_mm']} mm · FACE A {p['face_A_outward_world']}",'',('CNC PROVIDED: ' if en else 'FORNECIDO PELO CNC: ')+('outer contour; ' if en else 'contorno externo; ')+f"{len(p['through_cuts'])} CUT; {len(p['pockets'])} POCKET; "+('face reduction ' if en else 'redução da face ')+str(p['facing_reduction_mm'])+' mm.',('Fit/coupon HOLD: ' if en else 'PENDÊNCIA de ajuste/cupom: ')+str(p['fit_dependent'] or p['coupon_dependent']), '']
  for op in p['pockets']+p['through_cuts']:lines += [f"- {op['id']}: {op.get('group','CUT')} · FACE A · {op.get('depth_range_from_finished_face_A_mm',op.get('depth_range_from_face_A_mm','see register'))} mm"]
  if not p['manual_finish']:lines += [('BUILDER FINISH: none in the nominal operation audit.' if en else 'ACABAMENTO DO MONTADOR: nenhum na auditoria nominal de operações.')]
  for op in p['manual_finish']:
   typ=op['operation'];namesop={'DRILL_OR_COUNTERSINK':('drill / countersink with selected bit, depth stop and qualified guide','furar / escarear com broca selecionada, limitador e guia validada'),'SQUARE_CORNER_FINISH_OR_COUPON_RELIEF':('file/chisel corner to reference','limar/formonar canto até a referência'),'OUTER_REENTRANT_CORNER_FINISH':('file/chisel the reentrant root to the exact reference','limar/formonar a raiz reentrante até a referência exata'),'NARROW_FEATURE_MANUAL_FINISH':('finish the narrow feature with qualified hand tools','acabar a região estreita com ferramentas manuais validadas'),'R2_ACCESS_RESIDUAL_FINISH':('file/chisel the cutter-inaccessible residual to reference','limar/formonar o resíduo inacessível à fresa até a referência'),'BEVEL_SANDING_FINISH':('sand to reference bevel with straightedge and angle template','lixar até o chanfro de referência com régua e gabarito angular')};label=namesop.get(typ,(typ,typ))[0 if en else 1]
   lines += [('- BUILDER FINISH: ' if en else '- ACABAMENTO DO MONTADOR: ')+label+f" · {op.get('feature','')} · FACE A datum {op.get('depth_range_from_face_A_mm',op.get('depth_from_face_A_mm','reference geometry' if en else 'geometria de referência'))} mm. "+('Do not enlarge sub-Ø4 pilots into Ø4 locators. Physical tool/hardware qualification required.' if en else 'Não amplie pilotos menores que Ø4 para localizadores Ø4. É necessária validação física das ferramentas/ferragens.')]
  lines += ['',f"[{('Exact axes, depths and operations' if en else 'Eixos, profundidades e operações exatas')}](../exports/generated/flatpack-v331/manual-finish-schedule.json) · [{('Inspect member' if en else 'Inspecionar peça')}](../exports/generated/viewer-v32/index.html?part={iid}&lang={lang})",'']
 lines += ['---','CERN-OHL-S-2.0 · Source Location: https://github.com/advpeterrobinson-hash/vpin-cabinet','']
 (R/'docs'/fn).write_text('\n'.join(lines))
# Simple orientation cards: actual 2D profile + paired face designation and installed directions.
ori=O/'orientation';ori.mkdir(exist_ok=True)
for p in REG['parts']:
 pts=p['review_outline'];xs=[v[0] for v in pts];ys=[v[1] for v in pts];scale=min(240/max(max(xs)-min(xs),1),150/max(max(ys)-min(ys),1));path=' '.join(f'{40+(x-min(xs))*scale:.2f},{55+(y-min(ys))*scale:.2f}' for x,y in pts)
 vec=', '.join(f'{x:g}' for x in p['face_A_outward_world'])
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 245"><rect width="720" height="245" fill="#f4f6f8"/><g font-family="sans-serif" fill="#20313c"><text x="20" y="25" font-size="16">{p["instance_id"]} / {p["manufacturing_part_id"]}</text><polygon points="{path}" fill="#dbc69f" stroke="#20313c"/><text x="330" y="60" font-size="17">FACE A — CNC / USINADA</text><text x="330" y="90" font-size="17">FACE B — NO CNC / SEM CNC</text><text x="330" y="125" font-size="13">A outward / normal externa: [{vec}]</text><text x="330" y="153" font-size="13">X: left→right / esquerda→direita</text><text x="330" y="178" font-size="13">Y: front→rear / frente→trás · Z: up / cima</text><text x="20" y="232" font-size="12">REFERENCE / REFERÊNCIA · Depth / profundidade: finished FACE A acabada → +z into wood / para dentro</text></g></svg>'
 (ori/(p['instance_id']+'.svg')).write_text(svg)
# Hash every prior engineering/config/manufacturing/library input, excluding only viewer outputs/scripts allowed to change.
protected=[]
for name in subprocess.check_output(['git','ls-tree','-r','--name-only',HEAD],cwd=R,text=True).splitlines():
 if name.startswith(('config/','cad/','library/','exports/generated/flatpack-v331/','exports/generated/hardware-v33/',source+'/')):
  f=R/name
  if f.is_file():protected.append({'path':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(O/'geometry-protection.json').write_text(json.dumps({'head_before':HEAD,'files':protected},indent=2)+'\n')
# Offline single file: data blocks are inert until needed; no network runtime dependencies.
template=(R/'tools/viewer-v332/template.html').read_text()
legacy=(R/'tools/viewer/template.html').read_text()
palette_lines=[line for line in legacy.splitlines() if line.startswith(('const ORIGINAL_PALETTE=','Object.assign(ORIGINAL_PALETTE','const ACCESSIBLE_PALETTE=','function semanticRole('))]
palette_lines.append(re.search(r'function category\(n\)\{[\s\S]*?\n\}',legacy).group())
app=(R/'tools/viewer-v332/app.js').read_text().replace('__LEGACY_PALETTE_FUNCTIONS__','\n'.join(palette_lines))
for key,val in {'__THREE__':(R/'tools/viewer/vendor/three.min.js').read_text(),'__ORBIT__':(R/'tools/viewer/vendor/OrbitControls.js').read_text(),'__DATA__':base64.b64encode(packed).decode(),'__APP__':app,'__NOTICE__':html.escape((R/'NOTICE.md').read_text()),'__LICENSE__':html.escape((R/'LICENSE').read_text()),'__MIT__':html.escape((R/'tools/viewer/vendor/LICENSE.three').read_text())}.items():template=template.replace(key,val)
(R/'exports/generated/viewer-v32/index.html').write_text(template)
print('V332_BUILD_PASS',len(installed),'installed;',len(detail),'detail;',len(REG['parts']),'wood;',len(manual['stages']),'stages;',sum(len(s['steps']) for s in manual['stages']),'steps;',round(len(template.encode())/1e6,2),'MB')

"""V33.5 append-only metadata, bilingual manual and hardware overlay. CERN-OHL-S-2.0."""
from pathlib import Path
import json,copy,csv,collections
R=Path(__file__).resolve().parents[1];O=R/'exports/generated/structural-v335'
def read(p):return json.loads((R/p).read_text())
def dump(p,v):(R/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def bi(en,pt):return {'en':en,'pt-BR':pt}
def fmt(x):
 if x is None:return 'HOLD'
 if isinstance(x,(int,float)):return f'{x:.3f}'.rstrip('0').rstrip('.') or '0'
 if isinstance(x,list):return ' / '.join(fmt(v) for v in x)
 return str(x)
reg=read(str(O.relative_to(R))+'/manufacturing-register.json');val=read(str(O.relative_to(R))+'/geometry-validation.json');removed=set(val['removed']);parts=reg['parts'];by={p['instance_id']:p for p in parts};ids=set(by)
cat=read('config/hardware_catalog_v33.json');cat.update(version='V33.5',source_head='ca4e23eb598bb716156c41a7897ec8275e41f0ae',manufacturing_ready=False)
for h in cat['hardware']:
 before=h.get('instances',[]);after=[i for i in before if i.get('object') not in removed]
 if len(after)!=len(before):
  h['instances']=after
  if isinstance(h['quantity'],int) and h['quantity']==len(before):h['quantity']=len(after)
  h['notes']+=' V33.5 removed superseded rear-fan through-bolt stack or old monitor stops; unrelated instances preserved.'
  if not after:
   h['flatpack_classification']='REFERENCE_ONLY_NOT_FROZEN';h['quantity']=0;h['active']=False
 if h['id']=='F28':h['notes']='Fixed monitor-rail cleats and carrier shoe attachment still unresolved. Old stop blocks/pads retired. New stop rail retention counted separately as F57; do not claim entire F28 resolved.'
 if h['id'] in ['F27','I10','I11']:
  h['quantity']=2;h['flatpack_classification']='REQUIRED_FLATPACK_HARDWARE';h['active']=True
  h['notes']='V33.5 transverse rail: two M6-family adjusters, captive threads and locknuts. Purchased insert OD/length, tip envelope,10mm adjustment stroke, wood edge margins and assembly sequence require physical qualification.'
  h['freeze_status']='PURCHASE_BEFORE_CNC'
  h['instances']=[{'object':('BB_StopInsert' if h['id']=='I10' else 'BB_StopLocknut' if h['id']=='I11' else 'BB_StopAdjuster')+str(i),'coordinate_xyz_mm':[x,1237,935],'coordinate_meaning':'reference axis, no released bore','installation_direction':[0,0,1]} for i,x in enumerate([214,386])]
base=copy.deepcopy(next(h for h in cat['hardware'] if h['id']=='F28'))
for id,en,pt,qty,cl,stage,assembly in [
 ('F56','Main rear fan wood-anchored screw','Parafuso da ventoinha traseira ancorado na madeira',8,'OPTIONAL_FLATPACK_HARDWARE','07','main_ventilation'),
 ('F57','Captured monitor-stop rail retention screw','Parafuso de retenção da travessa capturada do monitor',2,'REQUIRED_FLATPACK_HARDWARE','12','display_glass_interfaces'),
 ('F58','Underside pocket retention screws, hardware-dependent','Parafusos de retenção em furos oblíquos inferiores, dependentes do gabarito',None,'REQUIRED_FLATPACK_HARDWARE','03','cabinet_shell')]:
 h=copy.deepcopy(base);h.update(id=id,description_en=en,description_pt_BR=pt,quantity=qty,flatpack_classification=cl,assembly_stage=stage,parent_assembly=assembly,quantity_status='HARDWARE_DEPENDENT' if qty is None else 'ARCHITECTURE_COUNT_HARDWARE_PROVISIONAL',model={'strategy':'REFERENCE_ENVELOPE_ONLY','detailed_threads':False,'path':'exports/generated/structural-v335/play.FCStd'},nominal_dimensions={'diameter_mm':None,'length_mm':None},notes='',instances=[])
 if id=='F56':
  h['notes']='Interior → head → inner grill → fan → rear wood. Supersedes F10 main rear through bolt; I03 retains floor fan nuts only. No exterior washer/nut. Length = selected grip stack + qualified wood engagement, less than18mm stock; no outside breakthrough. Existing Ø4.5 rear clearance bores withdrawn; selected pilot HOLD.'
  h['instances']=[{'object':f'RearFanWoodScrew{x}_{i+1}','coordinate_xyz_mm':[x+dx,1263.6,500+dz],'installation_direction':[0,1,0],'coordinate_meaning':'nominal fan105mm pattern; screw head plane reference'} for x in [230,370] for i,(dx,dz) in enumerate([(-52.5,-52.5),(-52.5,52.5),(52.5,-52.5),(52.5,52.5)])]
 if id=='F57':
  h['notes']='Two rear-operated retention screws, one per50mm carrier. Captured6mm end lands bear vertical load; existing four monitor clamps retain fold loads. Length, pilot and clamp performance HOLD.'
  h['instances']=[{'object':f'BB_StopRailRetention{i}','coordinate_xyz_mm':[x,1258,926],'installation_direction':[0,-1,0],'coordinate_meaning':'reference access axis only'} for i,x in enumerate([160,440])]
 if id=='F58':h['notes']='Reference12 floor +4 shelf stations. Actual quantity/pitch/axis qualified against selected Kreg jig/screw. M006 must be absent during underside drilling; no proprietary jig geometry.';h['candidate_quantity']=16;h['quantity_formula']='2 * selected_floor_stations_per_side + 2 * selected_shelf_stations_per_side'
 cat['hardware'].append(h)
cat['object_to_id']={n:id for n,id in cat['object_to_id'].items() if n not in removed}
for h in cat['hardware']:
 for i in h.get('instances',[]):cat['object_to_id'][i['object']]=h['id']
dump('config/hardware_catalog_v335.json',cat)
closure=read('exports/generated/flatpack-v331/hardware-quantity-closure.json');closure['rows'].append({'id':'F58','classification':'FORMULA_FROM_SELECTED_HARDWARE','formula':'2 * selected_floor_stations_per_side + 2 * selected_shelf_stations_per_side','reference_only_quantity':16,'quantity':None})
dump('exports/generated/structural-v335/hardware-quantity-closure.json',closure)
# Installed material map: unchanged records copied, four obsolete installed wood
# components removed, one new rail added. SW01 records are retained verbatim.
materials=read('config/wood_materials_v334.json');materials['parts']=[p for p in materials['parts'] if p['object'] not in removed]
rail=next(p for p in parts if p['manufacturing_part_id']=='M067');p=copy.deepcopy(next(p for p in materials['parts'] if p['object']=='BB_MonitorCarrier0'));p.update(id='P094',object='BB_MonitorStopRail',description_en=rail['description_en'],description_pt_BR=rail['description_pt_BR'],source=rail['source']);materials['parts'].append(p)
materials['current_manufacturing_register']='exports/generated/structural-v335/manufacturing-register.json';dump('config/wood_materials_v335.json',materials)
# Preserve all original step numbers including the early SW01 jig step.
manual=read('exports/generated/solid-leg-v334/assembly-manual.json');manual['version']='V33.5'
for s in manual['stages']:
 s['pieces']=[i for i in s['pieces'] if i in ids]
 for t in s['steps']:t['component_ids']=[i for i in t['component_ids'] if i in ids]
s12=next(s for s in manual['stages'] if s['id']=='12');s12['pieces'].append('P094-Main')
steps={t['id']:t for s in manual['stages'] for t in s['steps']}
steps['12.1']['component_ids'].append('P094-Main');steps['12.1']['hardware_ids']+=['F57']
changes={
 '02.1':('Dry-fit the captured shell','Monte a caixa capturada a seco',
 'After SW01 jig qualification at02.0, lay SideL on a flat reference. Insert Floor, Front, Rear and RearBearingShelf into the4mm side captures BEFORE closing SideR. Shelf capture is an open-top rabbet. Clamp lightly, seat shoulders, measure both diagonals and600mm exterior width. No screw may pull a bad fit into place. M006 installs later; do not trap the floor/shelf after closing the shell.',
 'Após qualificar SW01 no passo02.0, apoie SideL numa superfície plana. Encaixe piso, frente, traseira e prateleira traseira nas capturas de4mm ANTES de fechar SideR. A captura da prateleira é um rebaixo aberto no topo. Grampeie levemente, assente os ombros, meça diagonais e largura externa600mm. Não use parafusos para forçar ajuste ruim. Instale M006 depois; não prenda piso/prateleira fora da caixa já fechada.'),
 '02.2':('Glue and clamp qualified captured joints','Cole e grampeie as juntas capturadas qualificadas',
 'Disassemble after the dry-fit checkpoint. Apply the approved structural adhesive, reassemble on the reference, clamp and recheck square. Fit widths use measured plywood plus coupon clearance. Do not apply glue until the coupon passes. Front/rear joints retain existing SW01/leg hardware interfaces; final shell fastener family F06 remains held.',
 'Desmonte após verificar o ajuste seco. Aplique adesivo estrutural aprovado, remonte sobre a referência, grampeie e confira esquadro. Larguras de encaixe usam espessura medida mais folga do cupom. Não cole antes do cupom aprovado. Frente/traseira preservam interfaces SW01/pés; família final F06 permanece pendente.'),
 '03.1':('Retain floor and bearing shelf; then install M006','Retenha piso e prateleira; depois instale M006',
 'Keep M006 out while qualifying/drilling underside pockets. Paper templates locate longitudinal stations only; jig angle, stop collar, screw and depth are hardware-dependent. Check exterior skin, top-face skin and driver path on a coupon. Glue/clamp shelf shoulders at unchanged Z596.9. Install approved screws without forcing the fit. After access work, glue the two retained M006 underside ledges to floor/side; their final F06 mechanical fixing schedule remains a physical-hardware hold. Cure before loading. Optional offcut supports are tooling only and removed after cure.',
 'Mantenha M006 fora durante qualificação/furação inferior. Gabaritos de papel marcam apenas posições longitudinais; ângulo, colar, parafuso e profundidade dependem do gabarito comprado. Verifique pele externa/superior e acesso no cupom. Cole/grampeie apoios da prateleira mantendo Z596,9. Instale parafusos aprovados sem forçar ajuste. Após o acesso, cole os dois apoios M006 sob piso/laterais; fixação mecânica final F06 permanece pendente. Aguarde cura antes de carregar. Apoios de retalho opcionais são ferramentas e saem após cura.'),
 '05.1':('Install the retained open cradles','Instale os berços abertos preservados',
 'Install the real M026/M027 profiles with the six unchanged F01 coordinates and direct floor feet. The upper-wall trim was rejected: unchanged minimum root alone does not prove unchanged ear stiffness. Preserve180° dowel seating,8.251mm front root and6.280mm rear limiting ligament. S3/T3 stay at CURRENT datums. Verify48mm lift-out and50° service; no bearings or metal shaft.',
 'Instale os perfis reais M026/M027 nos seis pontos F01 inalterados e pés apoiados no piso. O recorte superior foi rejeitado: manter a raiz mínima não comprova rigidez igual da orelha. Preserve apoio180°, raiz frontal8,251mm e ligamento traseiro6,280mm. S3/T3 mantêm referências CURRENT. Confira remoção48mm e serviço50°; sem rolamentos ou eixo metálico.'),
 '07.2':('Fit rear fans from the interior','Instale ventoinhas traseiras pelo interior',
 'Place fan against rear wood, inner finger grill against fan, then F56 screw heads facing the interior. Drive toward the wood. Withdraw old F10 through bolts/exterior washers and rear I03 nuts. Floor fan M4 fasteners remain unchanged. Select grip length, wood bite and pilot on the purchased fan/grill; no exterior breakthrough. Fan/accessory selection remains optional.',
 'Encoste ventoinha na madeira traseira, grade interna na ventoinha e cabeças F56 voltadas ao interior. Parafuse para a madeira. Retire hipótese antiga F10, arruelas externas e porcas I03 traseiras. Fixação M4 das ventoinhas do piso fica igual. Selecione comprimento, penetração e piloto com ventoinha/grade reais; sem atravessar a face externa. Ventoinha/acessórios são opcionais.'),
 '12.1':('Install the single transverse stop rail','Instale a travessa única de apoio',
 'Seat M067 in the two6mm carrier-front captures. Install two rear-operated F57 retention screws after screw/pilot qualification. Fit two I10 captive threads, F27 M6-family adjusters, I11 locknuts and replaceable contact tips. Use required10mm adjustment travel. Retain the four existing F26 monitor clamps for fold and out-of-plane loads. No M049 plywood pads. Front display removal, rear adjustment and existing16mm depth choices remain.',
 'Assente M067 nas duas capturas frontais de6mm dos suportes. Instale dois F57 pelo lado traseiro após qualificar parafuso/piloto. Instale duas roscas I10, reguladores F27 M6, contraporcas I11 e pontas substituíveis. Exija curso10mm. Preserve quatro F26 para cargas de dobramento e fora do plano. Sem calços M049. Remoção frontal, ajuste traseiro e posições de profundidade16mm continuam.'),
 '18.1':('Identify future controls and electronics','Identifique controles e eletrônica futuros',
 'The conventional front-right plunger is a visible provisional interface at X520/Z280. Its bore remains PURCHASE BEFORE CNC. The220×55mm under-front panel is restored as an UNLOCATED schematic: volume, OFF/AUDIO/PINBALL selector, Bluetooth pair and optional USB-C charge. No authoritative final control centers exist; select controls, then validate ergonomics and clearances. Generic cable passage and optional electronics remain builder-configurable.',
 'O plunger convencional frontal direito aparece provisoriamente em X520/Z280. Furo: COMPRAR ANTES DO CNC. Painel inferior220×55mm restaurado como esquema SEM LOCALIZAÇÃO FINAL: volume, seletor OFF/AUDIO/PINBALL, pareamento Bluetooth e USB-C opcional. Não existem centros finais autorizados; selecione controles e valide ergonomia/folgas depois. Passagem genérica de cabos e eletrônica opcional permanecem configuráveis.')}
for id,(en,pt,ae,ap) in changes.items():
 t=steps[id];t['title']=bi(en,pt);t['action']=bi(ae,ap);t['status']='WAITING_FOR_PHYSICAL_MEASUREMENT' if id in ['03.1','07.2','12.1','18.1'] else 'WAITING_FOR_COUPON'
 t['validation']={'id':id,'status':'GEOMETRIC_SCREEN_PASS_PHYSICAL_HOLD','physical_trajectory_validated':False,'evidence':'../structural-v335/geometry-validation.json','note':'SCHEMATIC assembly animation; coupon and purchased hardware not qualified.'}
 t['hold']=bi('CNC RELEASE BLOCKED. Actual material, coupon, jig and selected hardware must be qualified.','CNC BLOQUEADO. Qualificar material real, cupom, gabarito e ferragens selecionadas.')
steps['03.1']['hardware_ids'].append('F58')
for stage,id in [('03','F58'),('07','F56'),('12','F57')]:
 st=next(t for t in manual['stages'] if t['id']==stage)
 st['hardware']=[h for h in st['hardware'] if h!='F10']+[id]
steps['07.2']['hardware_ids']=[i for i in steps['07.2']['hardware_ids'] if i!='F10']+['F56']
# Make shell closure dependency and component appearance explicit.
for i in ['P005-Main','P028-Main']:
 if i not in steps['02.1']['component_ids']:steps['02.1']['component_ids'].append(i)
manual['order_changes'].append({'from':'03.1','to':'02.1','reason':'Floor and bearing shelf enter side captures before SideR closes. Stage03.1 is retention/inspection, not impossible insertion into a closed shell.'})
prepkeys=list(manual['part_preparation'][0])
manual['part_preparation']=[{k:by[p['instance_id']].get(k) for k in prepkeys} if by[p['instance_id']].get('version')=='V33.5' else p for p in manual['part_preparation'] if p['instance_id'] in ids]
manual['part_preparation'].append({k:by['P094-Main'].get(k) for k in prepkeys})
manual['current_manufacturing_register']='exports/generated/structural-v335/manufacturing-register.json'
manual['v335_changed_part_preparation']=[{k:p.get(k) for k in ['instance_id','manufacturing_part_id','face_A_outward_world','machining_face','opposite_face','pockets','manual_finish','manufacturing_status','fit_expression']} for p in parts if p.get('version')=='V33.5']
dump('exports/generated/structural-v335/assembly-manual.json',manual)
fields=['instance_id','manufacturing_part_id','assembly_id','description_en','description_pt_BR','quantity','material_class','manufacturing_class','nominal_stock_thickness_mm','finished_xy_size_mm','manufacturing_status','fit_dependent']
with (O/'manufacturing-bom.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:p.get(k) for k in fields} for p in parts)
for lang,suffix in [('en',''),('pt_BR','.pt-BR')]:
 lines=['# V33.5 — '+('Manufacturing wood BOM' if not suffix else 'Lista de madeira para fabricação'),'','PRELIMINARY / PRELIMINAR — CNC BLOCKED / CNC BLOQUEADO','','| ID | Family | Description | Qty | Stock mm | Status |','|---|---|---|---:|---:|---|']
 lines += [f"| {p['instance_id']} | {p['manufacturing_part_id']} | {p['description_'+lang]} | 1 | {p['nominal_stock_thickness_mm']} | {p['manufacturing_status']} |" for p in parts]
 (O/('manufacturing-bom'+suffix+'.md')).write_text('\n'.join(line.rstrip() for line in lines)+'\n')
for lang,suffix in [('en',''),('pt-BR','.pt-BR')]:
 lines=['# '+('Assembly manual — V33.5' if lang=='en' else 'Manual de montagem — V33.5'),'','**'+('PREPARATION ONLY — CNC RELEASE BLOCKED' if lang=='en' else 'SOMENTE PREPARAÇÃO — CNC BLOQUEADO')+'**','','[Offline viewer / Visualizador](../exports/generated/viewer-v32/index.html) · [Pocket templates / Gabaritos](../templates/pocket-holes/README.md) · [SW01 jig / Gabarito SW01](../exports/generated/solid-leg-v334/README.md)','']
 for s in manual['stages']:
  lines+=['<a id="stage-'+s['id']+'"></a>','','## '+s['id']+' — '+s['title'][lang],'']
  for t in s['steps']:
   lines+=['### '+t['id']+' — '+t['title'][lang],'',t['status'],'',('Parts / Peças: '+', '.join(t['component_ids'])),'','Hardware / Ferragens: '+', '.join(t['hardware_ids'])+'. '+('Use catalog quantities once per assembly; formula/TBD are not zero.' if lang=='en' else 'Use quantidades do catálogo uma vez por conjunto; fórmula/TBD não são zero.'),'']
   for k in ['orientation','tools','faces','action','check','hold']:
    v=t.get(k)
    if isinstance(v,dict):v=v.get(lang,v.get('en',''))
    if v:lines += [str(v),'']
   lines+=['Viewer: '+str(t.get('viewer_state',t.get('next_state','EXPLODED DETAILED')))+' · animation assembly-'+t['id'],'']
 lines+=['## '+('CNC and builder preparation for every plywood piece' if lang=='en' else 'Preparação CNC e manual de todas as peças de compensado'),'']
 for p in manual['part_preparation']:
  lines+=['### '+p['instance_id']+' / '+p['manufacturing_part_id'],'','FACE_A: '+str(p['face_A_outward_world'])+'; FACE_B / NO CNC. '+p['manufacturing_status'],'']
  for op in p.get('through_cuts',[])+p.get('pockets',[]):
   lines += ['CNC FACE_A · '+op.get('id','')+' · '+op.get('group','POCKET')+' · '+('depth / profundidade: ')+fmt(op.get('depth_mm',op.get('depth_range_from_finished_face_A_mm','HOLD')))+' mm.']
  for op in p['manual_finish']:
   depth=op.get('depth_from_face_A_mm',op.get('depth_range_from_face_A_mm',op.get('depth_mm','HOLD')))
   lines += [('BUILDER FINISH / ACABAMENTO MANUAL · FACE_A datum · '+fmt(depth)+' mm.')]
   lines+=[('- '+op.get('instruction',op['operation'])) if lang=='en' else '- '+op['operation']+': acabamento manual referenciado pela FACE_A; consultar desenho exato. Profundidade e ferramenta dependem da ferragem/cupom. Sem CNC na FACE_B.']
  lines+=['']
 lines+=['## '+('Hardware quantities and holds' if lang=='en' else 'Quantidades e pendências das ferragens'),'','| ID | Qty / Qtd | Status |','|---|---|---|']
 used={i for s in manual['stages'] for t in s['steps'] for i in t['hardware_ids']}
 for h in cat['hardware']:
  if h['id'] in used:lines.append(f"| {h['id']} | {h['quantity'] if h['quantity'] is not None else h.get('quantity_formula','TBD / HARDWARE-DEPENDENT')} | {h['freeze_status']} |")
 (R/('docs/ASSEMBLY_MANUAL'+suffix+'.md')).write_text('\n'.join(line.rstrip() for line in lines)+'\n')
manifest={'version':'V33.5','head_before':'ca4e23eb598bb716156c41a7897ec8275e41f0ae','current_register':'exports/generated/structural-v335/manufacturing-register.json','current_BOM':'exports/generated/structural-v335/manufacturing-bom.csv','CNC_filter':'manufacturing_class != SHOP_MADE_SOLID_WOOD_PART','shop_family':'SW01','superseded_leg_families':['M019','M020','M021','M022','M023'],'superseded_stop_families':['M046','M047','M048','M049'],'installed_material_map':'config/wood_materials_v335.json','release':False}
dump('config/manufacturing/flatpack_v335.json',manifest)
print('V335_METADATA_PASS',len(parts),len(cat['hardware']))
